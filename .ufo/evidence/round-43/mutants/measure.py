#!/usr/bin/env python3
"""Round-43 C1 counter — survivor resolution under a pre-declared rule (depth).

Frozen before any seat scored and before the deciding run. It measures the two
survivors of the round-42 mutant set, whose verdict the round-42 closure routed
here (`.ufo/evidence/round-42/census/mutants.json`, unchanged; the round-42
predicate `C2_R42_PASS` stays false and is not re-adjudicated).

Rule, pre-declared in the round-43 contract and applied mechanically here:

  K (kill) — a mutant is `killed` when the round-43 battery (fixtures +
    live sites) produces at least one FAIL under the round-42 exit-plus-FAIL
    oracle: the run exits 0 with parseable output and a case differs from its
    declared classification. The killing fixture must contain no
    runtime-unreachable statement, so the kill rests on reachable code.
  D (dead-code-only) — a mutant that survives K is `dead_code_only` when every
    case on which it differs from the pristine tool is a fixture whose source
    contains a statement after an unconditional `return`/`raise` in the same
    block. The class is named, not dropped: the mutant's divergence exists only
    on inputs that no runtime path reaches.
  E (equivalent) — a mutant with no differing case over the declared corpus.
  U (unresolved) — anything else: `not_killed` (a reachable-input survivor),
    `runtime_error` (non-zero exit / traceback / unparseable output — PIT's Run
    error, Stryker's RuntimeError, which neither counts as a kill), or
    `apply_error` (the declared edit does not apply exactly once).

Battery: twelve fixtures — the ten round-42 fixtures unchanged plus
`F11_outflag_namespace` (a `SimpleNamespace` carrying a name equal to an
argparse output-flag dest, which is reachable code) and
`F12_method_two_returns` (a method with two top-level returns: the
dead-code-only discriminator) — and the same three live sites.

Predicate `C1_R43_PASS` is true iff: self_pin=1, tool_absent=0,
tool_sha_ok=1, selftest_exit=0, fixtures_pass=12/12, run_errors=0, the three
live sites match, live_unflagged_v4=0 over every tracked `tools/*.py` at REV,
mutants_sha_ok=1 (the declaration at REV is the pinned blob),
mutants_declared=6, mutants_killed=5, dead_code_only=1, equivalent=0,
unresolved=0, `outflag_no_parse_args_check` ∈ killed with `kill_binding=1`
(its failing fixture is exactly `F11_outflag_namespace`, so the kill is bound
to that fixture rather than asserted from its source text), and
`method_fold_several_returns` ∈ dead_code_only with `dead_code_arg_ok=1`.

Counting command:

  python3 .ufo/evidence/round-43/mutants/measure.py --lane LANE --rev REV --freeze FREEZE

`--probe-mutant PATH` scores one mutant file under the same oracle (for
falsifier seats). `--control` runs the round-42 battery (the ten round-42 fixtures: both new
fixtures are skipped) and prints a CONTROL line; it is never the measurement. Exit 0 iff the predicate
is true, 1 if false, 2 on a setup refusal.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

SELF_REL = '.ufo/evidence/round-43/mutants/measure.py'
CONTRACT_REL = '.ufo/evidence/round-43/contract.json'
MUTANTS_REL = '.ufo/evidence/round-42/census/mutants.json'
TOOL_REL = 'tools/write-path-census-v4.py'
TIMEOUT = 60
BITS = ('expected', 'scratch', 'explicit_out', 'unflagged')

# name: (source, want, needle, lineno)
FIXTURES = {
    'F01_attr_scratch': ('''import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def case_dir(self, name):
        path = os.path.join(self.root, name)
        os.makedirs(path)
        return path

    def run(self):
        directory = self.case_dir('a')
        expected_path = os.path.join(directory, 'expected.json')
        with open(expected_path, 'w') as handle:
            handle.write('{}')
''', {'expected': True, 'scratch': True, 'explicit_out': False, 'unflagged': False},
        'mkdtemp', None),
    'F02_attr_golden': ('''import os


class H:
    def __init__(self):
        self.root = 'golden'

    def case_dir(self, name):
        path = os.path.join(self.root, name)
        os.makedirs(path)
        return path

    def run(self):
        directory = self.case_dir('a')
        expected_path = os.path.join(directory, 'expected.json')
        with open(expected_path, 'w') as handle:
            handle.write('{}')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F03_attr_ambiguous': ('''import os
import tempfile


class H:
    def __init__(self):
        self.root = tempfile.mkdtemp()

    def rebase(self):
        self.root = 'golden'

    def case_dir(self, name):
        path = os.path.join(self.root, name)
        os.makedirs(path)
        return path

    def run(self):
        directory = self.case_dir('a')
        expected_path = os.path.join(directory, 'expected.json')
        with open(expected_path, 'w') as handle:
            handle.write('{}')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F04_outflag': ('''import argparse
from pathlib import Path


def publish(data, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'expected.json').write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out')
    args = parser.parse_args()
    target = Path(args.out)
    publish(b'{}', target)
''', {'expected': True, 'scratch': False, 'explicit_out': True, 'unflagged': False},
        '--out', None),
    'F05_inflag': ('''import argparse
from pathlib import Path


def publish(data, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'expected.json').write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    args = parser.parse_args()
    publish(b'{}', Path(args.input))
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F06_outflag_mixed_callers': ('''import argparse
from pathlib import Path


def publish(data, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'expected.json').write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out')
    args = parser.parse_args()
    publish(b'{}', Path(args.out))
    publish(b'{}', Path('golden'))
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F07_module_constant': ('''EXPECTED = 'tests/expected.json'

with open(EXPECTED, 'w') as handle:
    handle.write('x')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F08_variable_join': ('''import os

root = 'golden'
dest = os.path.join(root, 'expected.json')
with open(dest, 'w') as handle:
    handle.write('x')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F09_symlink': ('''import os

os.symlink('a.json', os.path.join('golden', 'expected.json'))
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, None),
    'F10_update_flag': ('''import sys

if '--update-goldens' in sys.argv:
    with open('golden/expected.json', 'w') as handle:
        handle.write('x')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': False},
        None, None),
    # F11 — kill fixture for outflag_no_parse_args_check. Reachable code: the
    # value comes from a SimpleNamespace, not from parse_args, so the tool's
    # documented rule ("the base must be a parse_args namespace") says the
    # destination is not operator-named. The mutant drops that check.
    'F11_outflag_namespace': ('''import argparse
from pathlib import Path
from types import SimpleNamespace


def publish(data, out):
    out.mkdir(parents=True, exist_ok=True)
    (out / 'expected.json').write_bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out')
    args = parser.parse_args()
    options = SimpleNamespace(out='golden')
    publish(b'{}', Path(options.out))
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True},
        None, 8),
    # F12 — the dead-code-only discriminator for method_fold_several_returns.
    # The second top-level `return` is unreachable; the tool refuses to fold a
    # method with more than one top-level return, and the mutant folds the first.
    'F12_method_two_returns': ('''import os


class Report:
    def destination(self):
        first = os.path.join('tmp', 'expected.json')
        return first
        return os.path.join('golden', 'expected.json')

    def run(self):
        with open(self.destination(), 'w') as handle:
            handle.write('x')
''', {'expected': False, 'scratch': False, 'explicit_out': False, 'unflagged': False},
        'self.destination()', 11),
}

DEAD_CODE_FIXTURE = 'F12_method_two_returns'
NEW_FIXTURES = ('F11_outflag_namespace', 'F12_method_two_returns')
KILL_NAMES = ('outflag_no_parse_args_check',)
DEAD_CODE_NAMES = ('method_fold_several_returns',)

LIVE = (
    ('tools/context-capture.py', 1682,
     {'expected': True, 'scratch': True, 'explicit_out': False, 'unflagged': False}, 'mkdtemp'),
    ('tools/context-capture.py', 1685,
     {'expected': True, 'scratch': True, 'explicit_out': False, 'unflagged': False}, 'mkdtemp'),
    ('tools/registry-replay.py', 123,
     {'expected': True, 'scratch': False, 'explicit_out': True, 'unflagged': False}, '--out'),
)

V3_LINE = re.compile(r'^\S+?:(\d+) (\S+) expected=(\d) scratch=(\d) unflagged=(\d) ?(.*)$')


class Refusal(Exception):
    pass


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True)


def show(lane, rev, path):
    proc = git(lane, 'show', '%s:%s' % (rev, path))
    return proc.stdout if proc.returncode == 0 else None


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run_tool(tool, target, cwd, text_mode=False):
    argv = [sys.executable, '-I', tool, '--file', target] + ([] if text_mode else ['--json'])
    try:
        proc = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    out = proc.stdout.decode('utf-8', 'replace')
    err = proc.stderr.decode('utf-8', 'replace')
    if proc.returncode != 0 or 'Traceback' in err:
        tail = err.strip().splitlines()[-1:] or ['']
        return None, 'exit=%d %s' % (proc.returncode, tail[0][:120])
    if text_mode:
        sites = []
        for line in out.splitlines():
            match = V3_LINE.match(line)
            if match:
                sites.append({'lineno': int(match.group(1)), 'kind': match.group(2),
                              'expected': match.group(3) == '1',
                              'scratch': match.group(4) == '1', 'explicit_out': False,
                              'unflagged': match.group(5) == '1', 'resolved': match.group(6)})
        return sites, None
    try:
        doc = json.loads(out)
        sites = doc['sites']
        for site in sites:
            int(site['lineno'])
            for bit in BITS:
                bool(site[bit])
            str(site['resolved'])
    except Exception as exc:  # noqa: BLE001 - any shape defect is a run error
        return None, 'unparseable %s' % type(exc).__name__
    return sites, None


def check_site(sites, lineno, want, needle):
    if lineno is None:
        cands = [s for s in sites if s.get('expected')]
        if len(cands) != 1:
            return 'expected-value sites=%d, want 1' % len(cands)
        site = cands[0]
    else:
        cands = [s for s in sites if int(s['lineno']) == lineno]
        if len(cands) != 1:
            return 'sites at line %d=%d, want 1' % (lineno, len(cands))
        site = cands[0]
    for bit in BITS:
        if bool(site[bit]) != want[bit]:
            return '%s=%d want %d' % (bit, int(bool(site[bit])), int(want[bit]))
    if needle and needle not in str(site['resolved']):
        return 'resolved lacks %r' % needle
    return None


def battery(tool, work, text_mode=False, skip_new=False, skip_dead_code=False):
    """Return (fails, errors, live_results, fixture_pass, live_ok, tested, detail).

    `detail` maps a failing fixture name to True when its source contains a
    runtime-unreachable statement, so the kill oracle can apply the rule's
    reachability gate instead of only reporting it.
    """
    fails, errors, live_results = [], [], {}
    detail = {}
    fixture_pass = 0
    tested = 0
    for name, (src, want, needle, lineno) in sorted(FIXTURES.items()):
        if skip_new and name in NEW_FIXTURES:
            continue
        if skip_dead_code and name == DEAD_CODE_FIXTURE:
            continue
        tested += 1
        target = os.path.join(work, 'fixtures', name + '.py')
        sites, err = run_tool(tool, target, work, text_mode)
        if err:
            errors.append('%s %s' % (name, err))
            continue
        reason = check_site(sites, lineno, want, needle)
        if reason:
            fails.append('%s %s' % (name, reason))
            detail[name] = bool(unreachable_statements(src))
        else:
            fixture_pass += 1
    live_ok = {}
    for rel, lineno, want, needle in LIVE:
        sites, err = run_tool(tool, os.path.join(work, 'live', rel), work, text_mode)
        if err:
            errors.append('%s:%d %s' % (rel, lineno, err))
            live_ok[(rel, lineno)] = False
            live_results[(rel, lineno)] = err
            continue
        reason = check_site(sites, lineno, want, needle)
        live_results[(rel, lineno)] = reason or 'ok'
        live_ok[(rel, lineno)] = reason is None
        if reason:
            fails.append('%s:%d %s' % (rel, lineno, reason))
            # A live tool site is real code, so a failure there is a reachable
            # failure; without this the reachability gate would discard it and
            # a live-only regression could read as `equivalent`.
            detail['live %s:%d' % (rel, lineno)] = False
    return fails, errors, live_results, fixture_pass, live_ok, tested, detail


def unreachable_statements(src):
    """Names of blocks with a statement after an unconditional return/raise."""
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    hits = []

    def walk(node, path):
        body = getattr(node, 'body', None)
        if isinstance(body, list) and body and isinstance(body[0], ast.stmt):
            for index, stmt in enumerate(body[:-1]):
                if isinstance(stmt, (ast.Return, ast.Raise)):
                    hits.append('%s[%d]' % (path, index))
                    break
        for field in ('body', 'orelse', 'finalbody'):
            inner = getattr(node, field, None)
            if isinstance(inner, list):
                for index, child in enumerate(inner):
                    if isinstance(child, ast.stmt):
                        walk(child, '%s.%s[%d]' % (path, field, index))
        for handler in getattr(node, 'handlers', None) or []:
            walk(handler, path + '.handler')

    walk(tree, 'module')
    return hits


def fingerprint(sites):
    return json.dumps([{bit: bool(site[bit]) for bit in BITS} |
                       {'lineno': int(site['lineno']), 'kind': site['kind'],
                        'resolved': site['resolved']} for site in sites], sort_keys=True)


def apply_once(base, find, replace):
    count = base.count(find)
    if count != 1:
        return None, count
    return base.replace(find, replace), count


def stage(lane, rev, work):
    os.makedirs(os.path.join(work, 'fixtures'))
    for name, (src, _, _, _) in FIXTURES.items():
        with open(os.path.join(work, 'fixtures', name + '.py'), 'w', encoding='utf-8') as handle:
            handle.write(src)
    tools = [p for p in git(lane, 'ls-tree', '-r', '--name-only', rev, '--', 'tools/')
             .stdout.decode().split('\n') if p.endswith('.py')]
    for rel in tools:
        raw = show(lane, rev, rel)
        if raw is None:
            raise Refusal('cannot read %s at %s' % (rel, rev))
        full = os.path.join(work, 'live', rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as handle:
            handle.write(raw)
    return tools


def lane_unflagged(tool, work, tools, text_mode=False):
    total, errors = 0, 0
    for rel in tools:
        sites, err = run_tool(tool, os.path.join(work, 'live', rel), work, text_mode)
        if err:
            errors += 1
            continue
        total += sum(1 for site in sites if site['unflagged'])
    return total, errors


def differential(pristine, mutant, work):
    """Cases where the mutant's fingerprint differs from the pristine tool's."""
    differ = []
    for name, (src, _, _, _) in sorted(FIXTURES.items()):
        target = os.path.join(work, 'fixtures', name + '.py')
        base_sites, base_err = run_tool(pristine, target, work)
        mut_sites, mut_err = run_tool(mutant, target, work)
        if base_err or mut_err:
            differ.append((name, 'run_error'))
            continue
        if fingerprint(base_sites) != fingerprint(mut_sites):
            differ.append((name, 'dead_code' if unreachable_statements(src) else 'reachable'))
    return differ


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--lane', default='.')
    parser.add_argument('--rev')
    parser.add_argument('--freeze')
    parser.add_argument('--control', action='store_true')
    parser.add_argument('--probe-mutant')
    args = parser.parse_args()
    lane = os.path.abspath(args.lane)
    if not os.path.isdir(os.path.join(lane, 'tools')):
        raise SystemExit('refusing: %s has no tools/' % lane)
    rev = args.rev or subprocess.run(['git', '-C', lane, 'rev-parse', 'master'],
                                     capture_output=True).stdout.decode().strip()
    freeze = args.freeze or rev
    contract_raw = show(lane, freeze, CONTRACT_REL)
    if contract_raw is None:
        raise SystemExit('refusing: no contract at %s:%s' % (freeze, CONTRACT_REL))
    contract = json.loads(contract_raw)
    pin = contract['claims']['C1']['counter_sha256']
    self_raw = show(lane, freeze, SELF_REL)
    if self_raw is None:
        raise SystemExit('refusing: counter absent at freeze')
    self_pin = 1 if sha(self_raw) == pin else 0
    with open(os.path.abspath(__file__), 'rb') as handle:
        running = sha(handle.read())
    if running != pin:
        self_pin = 0

    tool_raw = show(lane, rev, TOOL_REL)
    tool_absent = 0 if tool_raw is not None else 1
    pins = contract.get('frozen_tools') or {}
    want_sha = pins.get(TOOL_REL, contract.get('tool_sha256'))
    tool_sha_ok = 1 if tool_raw is not None and sha(tool_raw) == want_sha else 0

    work = tempfile.mkdtemp(prefix='tameshi-r43-c1-')
    try:
        tools = stage(lane, rev, work)
        tool_path = os.path.join(work, 'live', TOOL_REL)
        selftest = subprocess.run([sys.executable, '-I', tool_path, '--selftest'],
                                  cwd=work, capture_output=True, timeout=TIMEOUT)
        selftest_exit = 0 if selftest.returncode == 0 else 1

        fields = []
        if args.probe_mutant:
            probe = os.path.abspath(args.probe_mutant)
            fails, errors, _, fixture_pass, live_ok, tested, detail = battery(probe, work)
            reachable = [case for case in detail if not detail[case]]
            if errors:
                verdict = 'runtime_error'
            elif fails and reachable:
                verdict = 'killed'
            elif fails:
                verdict = 'dead_code_only'
            else:
                verdict = 'survived'
            print('C1_R43_PROBE: verdict=%s failures=%d reachable_failures=%d errors=%d first=%s'
                  % (verdict, len(fails), len(reachable), len(errors),
                     (fails + errors)[:1]))
            return 0 if verdict == 'killed' else 1

        fails, errors, live_results, fixture_pass, live_ok, tested, detail = battery(
            tool_path, work, skip_new=args.control)
        if args.control:
            muts_raw = show(lane, rev, MUTANTS_REL)
            muts = json.loads(muts_raw)['mutants'] if muts_raw else []
            killed = 0
            for mut in muts:
                body, count = apply_once(tool_raw.decode(), mut['find'], mut['replace'])
                if count != 1:
                    continue
                path = os.path.join(work, 'control-%s.py' % re.sub(r'\W', '_', mut['name']))
                with open(path, 'w', encoding='utf-8') as handle:
                    handle.write(body)
                cf, ce, _, _, _, _, _cd = battery(path, work, skip_new=True)
                if not ce and cf:
                    killed += 1
            print('C1_R43_CONTROL: battery=round42_ten_fixtures fixtures_pass=%d/%d '
                  'mutants_declared=%d mutants_killed=%d C1_R43_CONTROL_PASS=%s'
                  % (fixture_pass, tested, len(muts), killed,
                     'true' if killed == len(muts) else 'false'))
            return 0 if killed == len(muts) else 1

        lane_unf, live_errors = lane_unflagged(tool_path, work, tools)

        muts_raw = show(lane, rev, MUTANTS_REL)
        if muts_raw is None:
            raise SystemExit('refusing: no mutant declaration at %s' % rev)
        want_mutants = (contract.get('claims', {}).get('C1', {}) or {}).get('mutants_sha256')
        mutants_sha_ok = 1 if want_mutants and sha(muts_raw) == want_mutants else 0
        mutants = json.loads(muts_raw)['mutants']
        killed, dead_code_only, equivalent, not_killed, runtime_error, apply_error = [], [], [], [], [], []
        dead_code_cases = {}
        kill_cases = {}
        for mut in mutants:
            name = mut['name']
            body, count = apply_once(tool_raw.decode(), mut['find'], mut['replace'])
            if count != 1:
                apply_error.append('%s(count=%d)' % (name, count))
                continue
            path = os.path.join(work, 'mutant-%s.py' % re.sub(r'\W', '_', name))
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write(body)
            mf, me, _, _, _, _, mdetail = battery(path, work)
            if me:
                runtime_error.append(name)
                continue
            reachable_fails = sorted(case for case in mdetail if not mdetail[case])
            if mf and reachable_fails:
                killed.append(name)
                kill_cases[name] = reachable_fails
                continue
            differ = differential(tool_path, path, work)
            dead = [case for case, kind in differ if kind == 'dead_code']
            live_diff = [case for case, kind in differ if kind != 'dead_code']
            if not differ:
                equivalent.append(name)
            elif live_diff:
                not_killed.append(name)
            else:
                dead_code_only.append(name)
                dead_code_cases[name] = dead

        kill_names = [name for name in killed]
        dead_names = [name for name in dead_code_only]
        unresolved = len(not_killed) + len(runtime_error) + len(apply_error)
        dead_arg_ok = 1 if dead_code_cases.get(DEAD_CODE_NAMES[0]) == [DEAD_CODE_FIXTURE] else 0
        # The kill must be bound to F11, not asserted from F11's source text.
        kill_binding = 1 if kill_cases.get(KILL_NAMES[0]) == ['F11_outflag_namespace'] else 0

        fields.append('C1_R43:')
        fields.append('self_pin=%d' % self_pin)
        fields.append('tool_absent=%d' % tool_absent)
        fields.append('tool_sha_ok=%d' % tool_sha_ok)
        fields.append('selftest_exit=%d' % selftest_exit)
        fields.append('fixtures_pass=%d/%d' % (fixture_pass, tested))
        fields.append('run_errors=%d' % len(errors))
        fields.append('live_ok=%d/%d' % (sum(1 for ok in live_ok.values() if ok), len(LIVE)))
        fields.append('live_unflagged_v4=%d' % lane_unf)
        fields.append('live_tool_errors=%d' % live_errors)
        fields.append('mutants_declared=%d' % len(mutants))
        fields.append('mutants_killed=%d' % len(killed))
        fields.append('dead_code_only=%d' % len(dead_code_only))
        fields.append('equivalent=%d' % len(equivalent))
        fields.append('not_killed=%d' % len(not_killed))
        fields.append('runtime_error=%d' % len(runtime_error))
        fields.append('apply_error=%d' % len(apply_error))
        fields.append('unresolved=%d' % unresolved)
        fields.append('killed_names=%s' % ','.join(sorted(kill_names)))
        fields.append('dead_code_names=%s' % ','.join(sorted(dead_names)))
        fields.append('dead_code_cases=%s' % ','.join(sorted(dead_code_cases.get(
            DEAD_CODE_NAMES[0], []))))
        fields.append('dead_code_arg_ok=%d' % dead_arg_ok)
        fields.append('kill_binding=%d' % kill_binding)
        fields.append('kill_cases=%s' % ';'.join('%s:%s' % (name, ','.join(cases))
                                                 for name, cases in sorted(kill_cases.items())))
        fields.append('mutants_sha_ok=%d' % mutants_sha_ok)
        passed = (self_pin == 1 and tool_absent == 0 and tool_sha_ok == 1
                  and selftest_exit == 0 and fixture_pass == len(FIXTURES)
                  and not errors and all(live_ok.values()) and lane_unf == 0
                  and live_errors == 0 and len(mutants) == 6
                  and len(killed) == 5 and len(dead_code_only) == 1
                  and not equivalent and unresolved == 0
                  and all(name in kill_names for name in KILL_NAMES)
                  and all(name in dead_names for name in DEAD_CODE_NAMES)
                  and dead_arg_ok == 1 and kill_binding == 1 and mutants_sha_ok == 1)
        fields.append('rev=%s' % rev)
        fields.append('freeze=%s' % freeze)
        fields.append('C1_R43_PASS=%s' % ('true' if passed else 'false'))
        if errors:
            fields.append('first_error=%s' % errors[0].replace(' ', '_'))
        print(' '.join(fields))
        return 0 if passed else 1
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
