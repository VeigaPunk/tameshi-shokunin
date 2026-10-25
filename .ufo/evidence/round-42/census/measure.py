#!/usr/bin/env python3
"""Round-42 C2 counter — attribute-bound and output-flag destinations (v4).

Frozen before any seat scored and before the deciding run. Successor of the
round-41 C2 counter, closing its routed instrument defects:

  * out-of-process: the measured tool is never imported; every run is
    `python3 -I <tool> ...` in a temporary directory, so the tool cannot patch
    the counter;
  * counter-side digests: the v3 and v2 blob digests are constants in this
    file, and the counter's bytes at FREEZE and the running file must equal
    the pin in the contract read at FREEZE (not at REV); the copy at REV must
    be absent (the base) or identical;
  * `resolved` text inspection: the live sites must resolve to text naming the
    mechanism (`mkdtemp`, `--out`), so a constant table cannot satisfy them;
  * exit-plus-FAIL kill oracle: a mutant is `killed` only when every run exits
    0 with parseable output AND at least one battery case differs from its
    declared classification (a FAIL line names it). A mutant whose run exits
    non-zero, prints a Traceback or unparseable output is `runtime_error` —
    PIT's "Run error" and Stryker's RuntimeError, which neither tool counts as
    a kill — and a mutant with no differing case is `survived`.

Tool interface (frozen): `python3 -I tools/write-path-census-v4.py --file F
--json` prints one JSON object with a `sites` list; each site carries
`lineno` (int), `kind` (str), `expected`, `scratch`, `explicit_out`,
`unflagged` (bool) and `resolved` (str), for every write site (not only the
expected-value ones). `--selftest` exits 0 iff the tool's own selftest passes.

Battery: the FIXTURES below (one write site each) plus the three live v3 false
positives — `tools/context-capture.py:1682` and `:1685` (base
`self.case_dir(name)` over `self.root = tempfile.mkdtemp(...)`), and
`tools/registry-replay.py:123` (`out` is `Path(args.out)` from `--out` at
every in-module call site).

Predicate `C2_R42_PASS` is true iff: self_pin=1, tool_absent=0, v3_sha_ok=1,
v2_sha_ok=1, selftest_exit=0, fixtures_pass equals the fixture count, the
three live sites are not unflagged with the declared scratch/explicit_out bit
and resolved text, live_unflagged_v4=0 over every tracked `tools/*.py` at
REV, and mutants.json at REV declares >= 3 mutants covering the classes
`attr`, `method` and `outflag`, each applying exactly once and each `killed`.

Counting command:

  python3 .ufo/evidence/round-42/census/measure.py --lane LANE --rev REV --freeze FREEZE

`--tool-file PATH` scores a substitute tool for controls; its output line is
labelled CONTROL and is never the measurement. `--probe-mutant PATH` scores
one mutant file under the oracle (for falsifier seats). Exit 0 iff the
predicate is true; 1 if false; 2 on a setup refusal.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELF_REL = '.ufo/evidence/round-42/census/measure.py'
CONTRACT_REL = '.ufo/evidence/round-42/contract.json'
MUTANTS_REL = '.ufo/evidence/round-42/census/mutants.json'
TOOL_REL = 'tools/write-path-census-v4.py'
V3_REL = 'tools/write-path-census-v3.py'
V2_REL = 'tools/write-path-census-v2.py'
V3_SHA = '095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279'
V2_SHA = '4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b'
REQUIRED_CLASSES = {'attr', 'method', 'outflag'}
TIMEOUT = 60

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
        'mkdtemp'),
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
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
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
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
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
''', {'expected': True, 'scratch': False, 'explicit_out': True, 'unflagged': False}, '--out'),
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
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
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
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
    'F07_module_constant': ('''EXPECTED = 'tests/expected.json'

with open(EXPECTED, 'w') as handle:
    handle.write('x')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
    'F08_variable_join': ('''import os

root = 'golden'
dest = os.path.join(root, 'expected.json')
with open(dest, 'w') as handle:
    handle.write('x')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
    'F09_symlink': ('''import os

os.symlink('a.json', os.path.join('golden', 'expected.json'))
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': True}, None),
    'F10_update_flag': ('''import sys

if '--update-goldens' in sys.argv:
    with open('golden/expected.json', 'w') as handle:
        handle.write('x')
''', {'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': False}, None),
}

LIVE = (
    ('tools/context-capture.py', 1682,
     {'expected': True, 'scratch': True, 'explicit_out': False, 'unflagged': False}, 'mkdtemp'),
    ('tools/context-capture.py', 1685,
     {'expected': True, 'scratch': True, 'explicit_out': False, 'unflagged': False}, 'mkdtemp'),
    ('tools/registry-replay.py', 123,
     {'expected': True, 'scratch': False, 'explicit_out': True, 'unflagged': False}, '--out'),
)
BITS = ('expected', 'scratch', 'explicit_out', 'unflagged')
V3_LINE = re.compile(r'^\S+?:(\d+) (\S+) expected=(\d) scratch=(\d) unflagged=(\d) ?(.*)$')


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True)


def show(lane, rev, path):
    proc = git(lane, 'show', '%s:%s' % (rev, path))
    return proc.stdout if proc.returncode == 0 else None


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run_tool(tool, target, cwd, text_mode=False):
    """Return (sites | None, error | None) for one out-of-process run."""
    argv = [sys.executable, '-I', tool, '--file', target] + ([] if text_mode else ['--json'])
    try:
        proc = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    out = proc.stdout.decode('utf-8', 'replace')
    err = proc.stderr.decode('utf-8', 'replace')
    if proc.returncode != 0 or 'Traceback' in err:
        return None, 'exit=%d %s' % (proc.returncode, err.strip().splitlines()[-1:] or '')
    if text_mode:
        sites = []
        for line in out.splitlines():
            match = V3_LINE.match(line)
            if match:
                sites.append({'lineno': int(match.group(1)), 'kind': match.group(2),
                              'expected': match.group(3) == '1', 'scratch': match.group(4) == '1',
                              'explicit_out': False, 'unflagged': match.group(5) == '1',
                              'resolved': match.group(6)})
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
    """Return None if the site matches, else a FAIL reason."""
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


def battery(tool, work, live_files, text_mode=False):
    """Run fixtures + live sites. Return (fails, errors, live_results, fixture_ok)."""
    fails, errors, live_results = [], [], {}
    fixture_ok = 0
    for name, (src, want, needle) in sorted(FIXTURES.items()):
        target = os.path.join(work, 'fixtures', name + '.py')
        sites, err = run_tool(tool, target, work, text_mode)
        if err:
            errors.append('%s %s' % (name, err))
            continue
        reason = check_site(sites, None, want, needle)
        if reason:
            fails.append('%s %s' % (name, reason))
        else:
            fixture_ok += 1
    for rel, lineno, want, needle in LIVE:
        sites, err = run_tool(tool, os.path.join(work, 'live', rel), work, text_mode)
        if err:
            errors.append('%s:%d %s' % (rel, lineno, err))
            live_results[(rel, lineno)] = None
            continue
        reason = check_site(sites, lineno, want, needle)
        live_results[(rel, lineno)] = reason
        if reason:
            fails.append('%s:%d %s' % (rel, lineno, reason))
    return fails, errors, live_results, fixture_ok


def oracle(tool, work):
    fails, errors, _, _ = battery(tool, work, None)
    if errors:
        return 'runtime_error', errors[0]
    if fails:
        return 'killed', fails[0]
    return 'survived', ''


def stage(lane, rev, work):
    os.makedirs(os.path.join(work, 'fixtures'))
    for name, (src, _, _) in FIXTURES.items():
        with open(os.path.join(work, 'fixtures', name + '.py'), 'w', encoding='utf-8') as handle:
            handle.write(src)
    tools = [p for p in git(lane, 'ls-tree', '-r', '--name-only', rev, '--', 'tools/')
             .stdout.decode().split('\n') if p.endswith('.py')]
    for rel in tools:
        raw = show(lane, rev, rel)
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
        total += sum(1 for s in sites if s['unflagged'])
    return total, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane', required=True)
    parser.add_argument('--rev', required=True)
    parser.add_argument('--freeze', required=True)
    parser.add_argument('--tool-file')
    parser.add_argument('--text-mode', action='store_true',
                        help='parse v3 text lines (controls only)')
    parser.add_argument('--probe-mutant')
    args = parser.parse_args()
    lane = os.path.abspath(args.lane)
    revs = []
    for given in (args.rev, args.freeze):
        proc = git(lane, 'rev-parse', '--verify', given + '^{commit}')
        if proc.returncode != 0:
            print('C2_R42: SETUP rev_unresolved=%s' % given)
            return 2
        revs.append(proc.stdout.decode().strip())
    rev, freeze = revs
    try:
        pin = json.loads(show(lane, freeze, CONTRACT_REL).decode())['claims']['C2']['counter_sha256']
    except Exception:
        print('C2_R42: SETUP contract_unreadable_at_freeze=%s' % freeze)
        return 2
    at_freeze = show(lane, freeze, SELF_REL)
    at_rev = show(lane, rev, SELF_REL)
    with open(os.path.abspath(__file__), 'rb') as handle:
        running = handle.read()
    if (at_freeze is None or sha(at_freeze) != pin or sha(running) != pin
            or (at_rev is not None and sha(at_rev) != pin)):
        print('C2_R42: SETUP self_pin=0 pin=%s rev=%s freeze=%s' % (pin, rev, freeze))
        return 2
    control = bool(args.tool_file or args.probe_mutant)
    label = 'C2_R42_CONTROL' if control else 'C2_R42'
    work = tempfile.mkdtemp(prefix='tameshi-r42-c2-')
    try:
        tools = stage(lane, rev, work)
        v3_raw = show(lane, rev, V3_REL)
        v2_raw = show(lane, rev, V2_REL)
        v3_ok = int(v3_raw is not None and sha(v3_raw) == V3_SHA)
        v2_ok = int(v2_raw is not None and sha(v2_raw) == V2_SHA)
        v3_path = os.path.join(work, 'v3.py')
        with open(v3_path, 'wb') as handle:
            handle.write(v3_raw or b'')
        v3_unflagged, _ = lane_unflagged(v3_path, work, tools, text_mode=True)
        if args.probe_mutant:
            with open(args.probe_mutant, 'rb') as handle:
                raw = handle.read()
            path = os.path.join(work, 'probe.py')
            with open(path, 'wb') as handle:
                handle.write(raw)
            outcome, why = oracle(path, work)
            print('PROBE outcome=%s detail=%s' % (outcome, why))
            print('%s: probe_outcome=%s rev=%s freeze=%s' % (label, outcome, rev, freeze))
            return 0
        if args.tool_file:
            with open(args.tool_file, 'rb') as handle:
                tool_raw = handle.read()
        else:
            tool_raw = show(lane, rev, TOOL_REL)
        if tool_raw is None:
            print('%s: tool_absent=1 v3_sha_ok=%d v2_sha_ok=%d live_unflagged_v3=%d rev=%s freeze=%s '
                  '%s_PASS=false' % (label, v3_ok, v2_ok, v3_unflagged, rev, freeze, label))
            return 1
        tool = os.path.join(work, 'v4.py')
        with open(tool, 'wb') as handle:
            handle.write(tool_raw)
        try:
            selftest_exit = subprocess.run([sys.executable, '-I', tool, '--selftest'], cwd=work,
                                           capture_output=True, timeout=TIMEOUT * 4).returncode
        except subprocess.TimeoutExpired:
            selftest_exit = -1
        fails, errors, live, fixture_ok = battery(tool, work, None, args.text_mode)
        for item in fails:
            print('FAIL %s' % item)
        for item in errors:
            print('ERROR %s' % item)
        live_ok = {key: int(reason is None) for key, reason in live.items()}
        v4_unflagged, v4_errors = lane_unflagged(tool, work, tools, args.text_mode)

        mutant_fields = []
        mutants_ok = False
        killed = declared = 0
        classes = set()
        raw_mut = None if control else show(lane, rev, MUTANTS_REL)
        if raw_mut is not None:
            try:
                mutants = json.loads(raw_mut.decode())['mutants']
            except Exception:
                mutants = []
            declared = len(mutants)
            for mut in mutants:
                name = str(mut.get('name', '?'))
                find = str(mut.get('find', ''))
                applied = find and tool_raw.decode('utf-8', 'replace').count(find) == 1
                if not applied:
                    outcome, why = 'invalid', 'find applies %d times' % (
                        tool_raw.decode('utf-8', 'replace').count(find) if find else 0)
                else:
                    text = tool_raw.decode('utf-8', 'replace').replace(find, str(mut.get('replace', '')), 1)
                    path = os.path.join(work, 'mutant-%s.py' % re.sub(r'\W', '_', name))
                    with open(path, 'w', encoding='utf-8') as handle:
                        handle.write(text)
                    outcome, why = oracle(path, work)
                print('MUTANT %s class=%s outcome=%s detail=%s' % (name, mut.get('class'), outcome, why))
                if outcome == 'killed':
                    killed += 1
                    classes.add(mut.get('class'))
            mutants_ok = declared >= 3 and killed == declared and REQUIRED_CLASSES <= classes
        mutant_fields = ['mutants_declared=%d' % declared, 'mutants_killed=%d' % killed,
                         'mutant_classes_killed=%s' % ','.join(sorted(c for c in classes if c))]

        def live_field(rel, lineno):
            return live_ok.get((rel, lineno), 0)

        passed = (not control and selftest_exit == 0 and v3_ok and v2_ok
                  and fixture_ok == len(FIXTURES) and not errors and all(live_ok.values())
                  and len(live_ok) == len(LIVE) and v4_unflagged == 0 and v4_errors == 0
                  and mutants_ok)
        print(' '.join([
            '%s:' % label, 'self_pin=1', 'tool_absent=0', 'tool_sha256=%s' % sha(tool_raw),
            'v3_sha_ok=%d' % v3_ok, 'v2_sha_ok=%d' % v2_ok, 'selftest_exit=%d' % selftest_exit,
            'fixtures_pass=%d/%d' % (fixture_ok, len(FIXTURES)), 'run_errors=%d' % len(errors),
            'live_1682_ok=%d' % live_field('tools/context-capture.py', 1682),
            'live_1685_ok=%d' % live_field('tools/context-capture.py', 1685),
            'live_123_ok=%d' % live_field('tools/registry-replay.py', 123),
            'live_unflagged_v3=%d' % v3_unflagged, 'live_unflagged_v4=%d' % v4_unflagged,
            'live_tool_errors_v4=%d' % v4_errors,
        ] + mutant_fields + ['rev=%s' % rev, 'freeze=%s' % freeze,
                             '%s_PASS=%s' % (label, 'true' if passed else 'false')]))
        return 0 if passed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
