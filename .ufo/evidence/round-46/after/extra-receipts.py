#!/usr/bin/env python3
"""Round-46 supplementary receipts for C2 (answers wave-2 T46CritC2 F1/F2; not part of the frozen predicate).

  extra-receipts.py LANE REV

1. STRICT_EQUIVALENCE: the hardened counter with its self_pin line forced to 1 prints the same stdout as the
   round-45 counter over the round-45 data revision with NOTHING masked (the frozen `equivalence` masks self_pin
   and the PASS token, which differ only because the hardened copy's own path is absent at that revision).
2. KILL_CASES: for every declared mutant, the first `FAIL <case>` line the mutated hardened selftest prints
   (a kill by a named rule case, not by a crash, a timeout or a source-text pin).
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

lane, rev = sys.argv[1], sys.argv[2]
E = '.ufo/evidence/round-46/hardening'
spec = importlib.util.spec_from_file_location('mutate', os.path.join(lane, E, 'mutate.py'))
mutate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutate)


def show(path):
    return subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True, check=True).stdout


def run(src, args):
    with tempfile.TemporaryDirectory(prefix='tameshi-r46-x-') as d:
        p = os.path.join(d, 'measure.py')
        open(p, 'wb').write(src)
        return subprocess.run([sys.executable, p] + args, capture_output=True, text=True, cwd=d,
                              env=dict(mutate.ENV), timeout=300)


manifest = json.loads(show(E + '/mutants.json'))
bad = 0
for group, spec_ in manifest['groups'].items():
    orig = show(spec_['orig'])
    hard = show(E + '/%s-counter.py' % group)
    forced, n = re.subn(rb'self_pin = int\(.*\)', b'self_pin = 1', hard)
    a = run(orig, ['--lane', lane, '--rev', mutate.DATA_REV])
    b = run(forced, ['--lane', lane, '--rev', mutate.DATA_REV])
    same = a.stdout == b.stdout and a.returncode == b.returncode and 'PASS=true' in a.stdout and n == 1
    bad += not same
    print('STRICT_EQUIVALENCE %s self_pin_lines_patched=%d identical_stdout=%s exit=%d/%d round45_line=%s' % (
        group, n, a.stdout == b.stdout, a.returncode, b.returncode, a.stdout.strip().splitlines()[-1][:200]))
    for m in spec_['mutants']:
        if m['kind'] != 'mutant':
            continue
        text = hard.decode()
        mutated = mutate.apply(text, m)
        if mutated is None:
            print('KILL_CASE %s %s inapplicable' % (group, m['id']))
            bad += 1
            continue
        out = run(mutated.encode(), ['--selftest'])
        fails = [l for l in out.stdout.splitlines() if l.startswith('FAIL ')]
        crashed = out.returncode != 0 and not fails
        print('KILL_CASE %s %s exit=%d first_fail=%s%s' % (
            group, m['id'], out.returncode, (fails[0][:110] if fails else '-'), ' CRASH-ONLY' if crashed else ''))
        bad += (not fails)
print('EXTRA_RECEIPTS_BAD=%d' % bad)
sys.exit(1 if bad else 0)
