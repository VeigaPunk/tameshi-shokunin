#!/usr/bin/env python3
"""Shrink a killing fixture case to a 1-minimal sub-case (delta debugging, round-50 F6).

tools/staged-id-guard.py is checked by tools/pbt-staged-id.py (round 49): a mutant of the guard
survives a property run only through a counterexample case, and that case is large enough that a
reader cannot see which line the mutant actually needs. This tool takes one such killing case and
reduces it to a sub-case from which no single unit can be removed without losing the kill, and states
the cost of the reduction in guard invocations.

Usage:
  python3 -I tools/shrink-case.py --pristine P --mutant M --case CASE.json --out OUT.json
  python3 -I tools/shrink-case.py --selftest

CASE is {registry: str, staged: str, map: object|null} as dumped by tools/pbt-staged-id.py. OUT is
{case: {registry, staged, map}, runs: int, units_before: int, units_after: int}: `runs` counts every
guard invocation the reduction made (pristine and mutant alike) and a unit is one registry line, one
staged line, or one entry of map['map'] when that is an object.

A kill is the round-49 generator's oracle read of the pair: `check` passes on the pristine guard and
fails on the mutant. The search is Zeller & Hildebrandt's ddmin (TSE 2002) - drop chunks of
decreasing size, then the complement, then single units - run to a fixpoint, so the result is
1-minimal: removing any one unit loses the kill. Verdicts are cached by case content, so no case is
run twice and the cost is the count of real invocations. Deterministic; standard library only; exit 2
with a reason on stderr for a bad argument, an unreadable file, or a case that carries no kill.

The method is the whole point: a shrinker that reports a cost it did not pay, or a case from which a
unit can still be dropped, is worse than no shrinker, because the reduced case is then read as
evidence about the mutant.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

FIELDS = ('registry', 'staged')
SELFTEST_TIMEOUT = 300

# The public round-49 panel's M02 edit (the ROW_RE leading-space allowance), used by the selftest's
# end-to-end leg. Checked against the panel itself when the panel is reachable from this file.
M02_EDIT = ("ROW_RE = re.compile(r'^ {0,3}\\|",
            "ROW_RE = re.compile(r'^\\|")


class Unusable(Exception):
    """Bad argument, unreadable file, or a case that does not carry a kill."""


# ------------------------------------------------------------------------------------------------
# the units of a case, as the frozen interface counts them
# ------------------------------------------------------------------------------------------------
def map_entries(case):
    """The mutable part of the map: its 'map' object, when the case carries one."""
    mapping = case.get('map')
    if isinstance(mapping, dict) and isinstance(mapping.get('map'), dict):
        return mapping['map']
    return None


def unit_count(case):
    count = len(case['registry'].splitlines(True)) + len(case['staged'].splitlines(True))
    entries = map_entries(case)
    return count + (len(entries) if entries is not None else 0)


def case_key(case):
    """Content key: two cases with this key behave identically, so one verdict serves both."""
    mapping = case.get('map')
    return (case['registry'], case['staged'],
            None if mapping is None else json.dumps(mapping, sort_keys=True))


def valid_case(case):
    if not isinstance(case, dict):
        return False
    for field in FIELDS:
        if not isinstance(case.get(field), str):
            return False
    return case.get('map') is None or isinstance(case['map'], dict)


# ------------------------------------------------------------------------------------------------
# ddmin: chunk removal, then complement, then single units, to a 1-minimal fixpoint
# ------------------------------------------------------------------------------------------------
def partition(items, n):
    """Split into n chunks whose sizes differ by at most one."""
    size, extra = divmod(len(items), n)
    chunks, start = [], 0
    for index in range(n):
        stop = start + size + (1 if index < extra else 0)
        if stop > start:
            chunks.append(tuple(items[start:stop]))
        start = stop
    return chunks


def ddmin(items, kills):
    """Reduce `items` to a 1-minimal subset for which `kills` holds; None if it never holds.

    Zeller & Hildebrandt's ddmin: with granularity n, try dropping each of n chunks; if none can go,
    try replacing the set by one chunk; if neither works, refine (n := 2n) up to one unit. The
    single-unit pass at the end restates the stopping rule directly, including the empty case, so
    1-minimality is a property of this loop and not a theorem about the search above it.
    """
    items = tuple(items)
    if not kills(frozenset(items)):
        return None
    current, n = items, 2
    while len(current) >= 2:
        chunks = partition(current, n)
        reduced = None
        for chunk in chunks:
            dropped = set(chunk)
            candidate = tuple(item for item in current if item not in dropped)
            if kills(frozenset(candidate)):
                reduced = candidate
                n = max(n - 1, 2)
                break
        if reduced is None:
            for chunk in chunks:
                if len(chunk) >= len(current):
                    continue
                if kills(frozenset(chunk)):
                    reduced = chunk
                    n = 2
                    break
        if reduced is None:
            if n >= len(current):
                break
            n = min(2 * n, len(current))
            continue
        current = reduced
    changed = True
    while changed:
        changed = False
        for item in list(current):
            candidate = tuple(other for other in current if other != item)
            if kills(frozenset(candidate)):
                current = candidate
                changed = True
                break
    return list(current)


# ------------------------------------------------------------------------------------------------
# the case as a set of removable units, and the costed interestingness test
# ------------------------------------------------------------------------------------------------
class Shrinker:
    """The interestingness test, with every guard invocation counted and every verdict cached."""

    def __init__(self, generator, pristine, mutant, workdir):
        self.generator = generator
        self.pristine = pristine
        self.mutant = mutant
        self.workdir = workdir
        self.runs = 0
        self.cache = {}

    def matches(self, role, case):
        """True when the guard named by `role` agrees with the generator's oracle on `case`."""
        key = (role, case_key(case))
        if key in self.cache:
            return self.cache[key]
        guard = self.mutant if role == 'mutant' else self.pristine
        self.runs += 1
        observed = self.generator.run_guard(guard, self.workdir, case)
        matched = self.generator.check(case, observed) is None
        self.cache[key] = matched
        return matched

    def kills(self, case):
        if self.matches('mutant', case):
            return False
        return self.matches('pristine', case)


def shrink(shrinker, case):
    """The 1-minimal sub-case of `case` that still kills the mutant."""
    registry = case['registry'].splitlines(True)
    staged = case['staged'].splitlines(True)
    entries = map_entries(case)
    fixed = None
    if case.get('map') is not None:
        fixed = {key: value for key, value in case['map'].items() if key != 'map'}
    units = [('registry', index) for index in range(len(registry))]
    units += [('staged', index) for index in range(len(staged))]
    if entries is not None:
        units += [('map', key) for key in entries]

    def build(keep):
        out = {'registry': ''.join(line for index, line in enumerate(registry)
                                   if ('registry', index) in keep),
               'staged': ''.join(line for index, line in enumerate(staged)
                                 if ('staged', index) in keep)}
        if entries is None:
            out['map'] = case.get('map')
        else:
            mapping = dict(fixed or {})
            mapping['map'] = {key: value for key, value in entries.items()
                              if ('map', key) in keep}
            out['map'] = mapping
        return out

    kept = ddmin(units, lambda keep: shrinker.kills(build(keep)))
    if kept is None:
        raise Unusable('the case carries no kill: the pristine guard does not pass it under the '
                       'oracle, or the mutant does not violate the oracle on it')
    return build(frozenset(kept))


# ------------------------------------------------------------------------------------------------
# loading the frozen generator that sits beside this tool, and the files
# ------------------------------------------------------------------------------------------------
def load_generator(directory):
    path = os.path.join(directory, 'pbt-staged-id.py')
    if not os.path.isfile(path):
        raise Unusable('generator not found beside this tool: %s' % path)
    spec = importlib.util.spec_from_file_location('frozen_pbt_r49', path)
    if spec is None or spec.loader is None:
        raise Unusable('cannot load the generator: %s' % path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:                                    # noqa: BLE001 - reported, not raised
        raise Unusable('generator import failed (%s): %s' % (path, exc))
    for name in ('check', 'run_guard'):
        if not callable(getattr(module, name, None)):
            raise Unusable('generator lacks %s(): %s' % (name, path))
    return module


def read_json(path, label):
    try:
        with open(path, 'rb') as handle:
            raw = handle.read()
    except OSError as exc:
        raise Unusable('cannot read the %s %s: %s' % (label, path, exc))
    try:
        return json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeDecodeError) as exc:
        raise Unusable('the %s %s is not JSON: %s' % (label, path, exc))


def run_from_arguments(args):
    # The generator runs each guard with cwd set to its own case directory, so a relative guard
    # path would be resolved against the wrong directory and every run would look like a failure.
    pristine, mutant = os.path.abspath(args.pristine), os.path.abspath(args.mutant)
    for path, label in ((pristine, 'pristine guard'), (mutant, 'mutant guard')):
        if not os.path.isfile(path):
            raise Unusable('cannot read the %s %s' % (label, path))
    case = read_json(args.case, 'case')
    if not valid_case(case):
        raise Unusable('the case is not {registry: str, staged: str, map: object|null}: %s'
                       % args.case)
    generator = load_generator(os.path.dirname(os.path.abspath(__file__)))
    before = unit_count(case)
    workdir = tempfile.mkdtemp(prefix='shrink-case-')
    try:
        shrinker = Shrinker(generator, pristine, mutant, workdir)
        shrunk = shrink(shrinker, case)
        payload = {'case': {'registry': shrunk['registry'], 'staged': shrunk['staged'],
                            'map': shrunk.get('map')},
                   'runs': shrinker.runs,
                   'units_before': before,
                   'units_after': unit_count(shrunk)}
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    try:
        with open(args.out, 'w', encoding='utf-8') as handle:
            json.dump(payload, handle, indent=1, sort_keys=False)
            handle.write('\n')
    except OSError as exc:
        raise Unusable('cannot write %s: %s' % (args.out, exc))
    print('shrink-case: units %d -> %d, runs %d' % (before, payload['units_after'],
                                                    payload['runs']))
    return 0


# ------------------------------------------------------------------------------------------------
# selftest: the search on synthetic predicates, then the CLI on a stub pair, then M02 for real
# ------------------------------------------------------------------------------------------------
STUB_GENERATOR = '''import json
import os
import subprocess
import sys


def expect(case):
    total = 0
    for field in ('registry', 'staged'):
        for line in case[field].splitlines():
            line = line.strip()
            if line:
                total += int(line)
    entries = case.get('map')
    if isinstance(entries, dict) and isinstance(entries.get('map'), dict):
        keys = sorted(entries['map'])
    else:
        keys = []
    return {'sum': total, 'keys': keys}


def run_guard(guard, case_dir, case):
    path = os.path.join(case_dir, 'case.json')
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(case, handle)
    proc = subprocess.run([sys.executable, '-I', guard, path], capture_output=True)
    try:
        answer = json.loads(proc.stdout.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        answer = None
    return {'exit': proc.returncode, 'json': answer, 'stdout': proc.stdout,
            'stderr': proc.stderr}


def check(case, observed):
    want = expect(case)
    if observed['exit'] != 0:
        return 'exit %r' % (observed['exit'],)
    if observed['json'] != want:
        return 'answer %r, oracle %r' % (observed['json'], want)
    return None
'''

STUB_GUARD = '''import json
import os
import sys

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.runs'), 'a') as handle:
    handle.write('run\\n')
case = json.load(open(sys.argv[1], encoding='utf-8'))
total = 0
for field in ('registry', 'staged'):
    for line in case[field].splitlines():
        line = line.strip()
        if line:
            total += SEVEN
entries = case.get('map')
if isinstance(entries, dict) and isinstance(entries.get('map'), dict):
    keys = sorted(entries['map'])
else:
    keys = []
print(json.dumps({'sum': total, 'keys': keys}))
'''

RUN_LOGGER = ("import os as _shrink_os\n"
              "with open(_shrink_os.path.join(_shrink_os.path.dirname(_shrink_os.path.abspath(__file__)), "
              "'.runs'), 'a') as _shrink_log:\n    _shrink_log.write('%s\\n')\n")


def instrument(source, tag):
    """A copy of a guard that logs each invocation beside itself (the counter's own device)."""
    lines = source.split('\n')
    for index, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            return '\n'.join(lines[:index]) + '\n' + (RUN_LOGGER % tag) + '\n'.join(lines[index:])
    raise Unusable('no top-level import to anchor the run logger')


def logged(path):
    if not os.path.exists(path):
        return 0
    with open(path, encoding='utf-8') as handle:
        return sum(1 for _ in handle)


def drop_unit(case, unit):
    field, ident = unit
    if field == 'map':
        mapping = dict(case['map'])
        mapping['map'] = {key: value for key, value in case['map']['map'].items() if key != ident}
        return dict(case, map=mapping)
    lines = case[field].splitlines(True)
    return dict(case, **{field: ''.join(lines[:ident] + lines[ident + 1:])})


def case_units(case):
    units = [('registry', index) for index in range(len(case['registry'].splitlines(True)))]
    units += [('staged', index) for index in range(len(case['staged'].splitlines(True)))]
    entries = map_entries(case)
    if entries is not None:
        units += [('map', key) for key in entries]
    return units


def subsequence(small, big):
    it = iter(big)
    return all(any(left == right for right in it) for left in small)


def is_subcase(small, big):
    for field in FIELDS:
        if not subsequence(small[field].splitlines(), big[field].splitlines()):
            return False
    if big.get('map') is None:
        return small.get('map') is None
    if not isinstance(small.get('map'), dict):
        return False
    big_entries, small_entries = map_entries(big), map_entries(small)
    if big_entries is None:
        return small['map'] == big['map']
    if small_entries is None:
        return False
    if ({k: v for k, v in small['map'].items() if k != 'map'}
            != {k: v for k, v in big['map'].items() if k != 'map'}):
        return False
    return all(key in big_entries and big_entries[key] == value
               for key, value in small_entries.items())


def selftest():
    checks = []

    def check(name, ok, detail=''):
        checks.append((name, bool(ok)))
        print('SELFTEST %-52s %s' % (name, 'ok' if ok else 'FAIL'))
        if not ok and detail:
            print('  DETAIL ' + ' '.join(str(detail).split())[:400])

    # ---- A. the search itself, on synthetic interestingness functions (no guard) ----------------
    items = tuple(range(12))
    seen = []

    def sentinel(keep):
        seen.append(keep)
        return 7 in keep

    got = ddmin(items, sentinel)
    check('core: sentinel predicate reduces to its one unit', got == [7], got)
    check('core: no verdict is asked twice', len(seen) == len(set(seen)),
          '%d calls, %d distinct' % (len(seen), len(set(seen))))
    check('core: the sentinel reduction is 1-minimal',
          all(not sentinel(frozenset(x for x in got if x != unit)) for unit in got), got)

    def floor(keep):
        return len(keep) >= 3 and min(keep) < 5

    got = ddmin(items, floor)
    check('core: a size floor leaves a 1-minimal three-unit set',
          got is not None and len(got) == 3 and min(got) < 5
          and all(not floor(frozenset(x for x in got if x != unit)) for unit in got), got)
    check('core: an unsatisfiable predicate returns None', ddmin(items, lambda keep: False) is None)
    check('core: an always-true predicate reduces to the empty set',
          ddmin(items, lambda keep: True) == [])
    check('core: an empty start is decided once',
          ddmin((), sentinel) is None and ddmin((), lambda keep: True) == [])

    # ---- B. the CLI end to end, on a stub guard pair with a stub oracle (no real guard) --------
    root = tempfile.mkdtemp(prefix='shrink-selftest-')
    try:
        tool = os.path.join(root, 'shrink-case.py')
        shutil.copyfile(os.path.abspath(__file__), tool)
        with open(os.path.join(root, 'pbt-staged-id.py'), 'w', encoding='utf-8') as handle:
            handle.write(STUB_GENERATOR)
        for name, seven in (('stub-pristine.py', 'int(line)'),
                            ('stub-mutant.py', '0 if int(line) == 7 else int(line)')):
            with open(os.path.join(root, name), 'w', encoding='utf-8') as handle:
                handle.write(STUB_GUARD.replace('SEVEN', seven))
        stub_case = {'registry': '1\n2\n3\n7\n9\n', 'staged': '4\n7\n8\n',
                     'map': {'map': {'S001': 'S002', 'S003': 'S004'}}}
        case_path = os.path.join(root, 'case.json')
        out_path = os.path.join(root, 'out.json')
        with open(case_path, 'w', encoding='utf-8') as handle:
            json.dump(stub_case, handle)
        proc = subprocess.run([sys.executable, '-I', tool,
                               '--pristine', os.path.join(root, 'stub-pristine.py'),
                               '--mutant', os.path.join(root, 'stub-mutant.py'),
                               '--case', case_path, '--out', out_path],
                              capture_output=True, cwd=root, timeout=SELFTEST_TIMEOUT)
        check('cli: the stub shrink exits 0', proc.returncode == 0,
              proc.stderr.decode('utf-8', 'replace')[-300:])
        stub_logged = logged(os.path.join(root, '.runs'))    # before any verification run
        try:
            with open(out_path, encoding='utf-8') as handle:
                out = json.load(handle)
        except (OSError, ValueError):
            out = None
        check('cli: the output carries case/runs/units_before/units_after',
              isinstance(out, dict) and isinstance(out.get('case'), dict)
              and isinstance(out.get('runs'), int) and isinstance(out.get('units_before'), int)
              and isinstance(out.get('units_after'), int), out)
        if isinstance(out, dict) and valid_case(out.get('case')):
            stub_gen = load_generator(root)
            work = os.path.join(root, 'verify')
            os.makedirs(work)

            def stub_kills(candidate):
                if stub_gen.check(candidate, stub_gen.run_guard(
                        os.path.join(root, 'stub-mutant.py'), work, candidate)) is None:
                    return False
                return stub_gen.check(candidate, stub_gen.run_guard(
                    os.path.join(root, 'stub-pristine.py'), work, candidate)) is None

            small = {'registry': out['case']['registry'], 'staged': out['case']['staged'],
                     'map': out['case'].get('map')}
            check('cli: the stub result is a sub-case', is_subcase(small, stub_case), small)
            check('cli: the stub result kills', stub_kills(small), small)
            check('cli: the stub result is 1-minimal',
                  stub_kills(small) and not any(stub_kills(drop_unit(small, unit))
                                                for unit in case_units(small)), small)
            check('cli: the stub unit counts are honest',
                  out['units_before'] == unit_count(stub_case)
                  and out['units_after'] == unit_count(small)
                  and out['units_after'] < out['units_before'],
                  (out['units_before'], out['units_after']))
            check('cli: the stub run count equals the logged invocations',
                  out['runs'] == stub_logged, (out.get('runs'), stub_logged))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # ---- C. the CLI end to end on the public round-49 mutant M02, when the guard is here ------
    directory = os.path.dirname(os.path.abspath(__file__))
    guard_path = os.path.join(directory, 'staged-id-guard.py')
    generator_path = os.path.join(directory, 'pbt-staged-id.py')
    if not (os.path.isfile(guard_path) and os.path.isfile(generator_path)):
        print('SELFTEST %-52s %s' % ('panel M02 end to end',
                                     'skip (no staged-id-guard.py beside this tool)'))
    else:
        panel_path = os.path.join(directory, os.pardir, '.ufo', 'evidence', 'round-49', 'c2',
                                  'panel.json')
        if os.path.isfile(panel_path):
            panel = read_json(panel_path, 'round-49 panel')
            pinned = [m for m in panel.get('mutants', [])
                      if isinstance(m, dict) and m.get('id') == 'M02']
            check('M02: the embedded edit is the panel M02 edit',
                  bool(pinned) and pinned[0].get('old') == M02_EDIT[0]
                  and pinned[0].get('new') == M02_EDIT[1], pinned)
        else:
            print('SELFTEST %-52s %s' % ('M02: the embedded edit is the panel M02 edit',
                                         'skip (panel not reachable)'))
        head = ('| id | source | kind | tier | scope | anchor | teaches | status | opened '
                '| recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n')
        body = ('| S%03d | Src S%03d \u2014 https://a%d.test/doc | docs | A | scope | anchor '
                '| teaches | queued | 2026-10-24 | 180d | -\n')
        m02_case = {'registry': head + body % (1, 1, 1) + body % (2, 2, 2),
                    'staged': head + ' ' + body % (1, 1, 1), 'map': None}
        root = tempfile.mkdtemp(prefix='shrink-m02-')
        try:
            with open(guard_path, encoding='utf-8') as handle:
                source = handle.read()
            if source.count(M02_EDIT[0]) != 1:
                check('M02: the pinned edit applies exactly once', False,
                      'count=%d' % source.count(M02_EDIT[0]))
            else:
                pristine = os.path.join(root, 'pristine.py')
                mutant = os.path.join(root, 'mutant.py')
                with open(pristine, 'w', encoding='utf-8') as handle:
                    handle.write(instrument(source, 'p'))
                with open(mutant, 'w', encoding='utf-8') as handle:
                    handle.write(instrument(source.replace(M02_EDIT[0], M02_EDIT[1]), 'm'))
                case_path = os.path.join(root, 'case.json')
                out_path = os.path.join(root, 'out.json')
                with open(case_path, 'w', encoding='utf-8') as handle:
                    json.dump(m02_case, handle)
                proc = subprocess.run([sys.executable, '-I', os.path.abspath(__file__),
                                       '--pristine', pristine, '--mutant', mutant,
                                       '--case', case_path, '--out', out_path],
                                      capture_output=True, cwd=root, timeout=SELFTEST_TIMEOUT)
                check('M02: the shrink exits 0 on the public mutant', proc.returncode == 0,
                      proc.stderr.decode('utf-8', 'replace')[-300:])
                m02_logged = logged(os.path.join(root, '.runs'))  # before any verification run
                try:
                    with open(out_path, encoding='utf-8') as handle:
                        out = json.load(handle)
                except (OSError, ValueError):
                    out = None
                if not (isinstance(out, dict) and valid_case(out.get('case'))):
                    check('M02: the shrink writes a readable case', False, out)
                else:
                    real = load_generator(directory)
                    work = os.path.join(root, 'verify')
                    os.makedirs(work)

                    def real_kills(candidate):
                        if real.check(candidate, real.run_guard(mutant, work,
                                                                candidate)) is None:
                            return False
                        return real.check(candidate, real.run_guard(pristine, work,
                                                                   candidate)) is None

                    small = {'registry': out['case']['registry'],
                             'staged': out['case']['staged'],
                             'map': out['case'].get('map')}
                    check('M02: the mutant violates the oracle on the input case',
                          real_kills(m02_case))
                    check('M02: the result is a sub-case that still kills',
                          is_subcase(small, m02_case) and real_kills(small), small)
                    check('M02: the result is 1-minimal',
                          real_kills(small) and not any(real_kills(drop_unit(small, unit))
                                                        for unit in case_units(small)), small)
                    check('M02: the unit counts are honest',
                          out['units_before'] == unit_count(m02_case)
                          and out['units_after'] == unit_count(small)
                          and out['units_after'] < out['units_before'],
                          (out['units_before'], out['units_after']))
                    check('M02: the run count equals the logged invocations',
                          out['runs'] == m02_logged, (out.get('runs'), m02_logged))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    failed = [name for name, ok in checks if not ok]
    print('SHRINK_SELFTEST: cases=%d failed=%d' % (len(checks), len(failed)))
    return 0 if not failed else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--pristine', help='the pristine guard to hold the case to the oracle')
    parser.add_argument('--mutant', help='the mutant guard the case must violate')
    parser.add_argument('--case', help='the killing case, JSON as tools/pbt-staged-id.py dumps it')
    parser.add_argument('--out', help='where the shrunk case and its cost are written, JSON')
    parser.add_argument('--selftest', action='store_true',
                        help='exercise the reduction without a panel')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    missing = [name for name in ('--pristine', '--mutant', '--case', '--out')
               if not getattr(args, name[2:])]
    if missing:
        parser.error('missing %s' % ', '.join(missing))
    try:
        return run_from_arguments(args)
    except Unusable as exc:
        print('shrink-case: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
