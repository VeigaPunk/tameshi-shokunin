#!/usr/bin/env python3
"""measure.py — round-38 C2 counter: the golden-comparison three-outcome fixture.

Predicate (frozen in `.ufo/evidence/round-38/contract.json` before any data run):

  C2_R38_PASS=true iff all three hold at REV:
    (a) the committed tool's own selftest passes 3/3 behavioural cases
        (match / differ / error) — the fixture discriminates, it does not check existence;
    (b) the mutant that collapses the `error` class into `differ` is KILLED by that
        same selftest (non-zero exit) — the fixture is shown able to fail;
    (c) the admitted knowledge entry at REV declares the three outcome classes and the
        explicit update-flag rule.

Counting command:

  python3 .ufo/evidence/round-38/golden/measure.py --lane LANE --rev REV

Exit 0 iff the predicate is true. At a revision that carries no fixture the
predicate is false and the exit is 1 (never 0 by absence).
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile

TOOL = 'tools/golden-verdict.py'
ENTRY = 'corpus/knowledge/golden-comparison-verdict.md'
MUTATION_OLD = "    return 'error'\n"
MUTATION_NEW = "    return 'differ'\n"


def git_show(lane, rev, path):
    proc = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
                           capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    a = ap.parse_args()

    lane = os.path.abspath(a.lane)
    rev = subprocess.run(['git', '-C', lane, 'rev-parse', a.rev],
                          capture_output=True).stdout.decode().strip()
    if not rev:
        print('GOLDEN_R38: SETUP rev_unresolved=%s C2_R38_PASS=false' % a.rev)
        return 1

    tool_bytes = git_show(lane, rev, TOOL)
    if not tool_bytes:
        print('GOLDEN_R38: cases=0/3 mutant_killed=false entry_ok=false tool_absent=1 '
              'rev=%s C2_R38_PASS=false' % rev)
        return 1
    tool_sha = hashlib.sha256(tool_bytes).hexdigest()

    entry_bytes = git_show(lane, rev, ENTRY)
    entry_ok = False
    cases_passed = 0
    mutant_killed = False

    with tempfile.TemporaryDirectory(prefix='golden-r38-') as tmp:
        tool_path = os.path.join(tmp, 'golden-verdict.py')
        with open(tool_path, 'wb') as fh:
            fh.write(tool_bytes)

        pristine = subprocess.run([sys.executable, tool_path, '--selftest'],
                                  capture_output=True)
        out = pristine.stdout.decode(errors='replace')
        m = re.search(r'GOLDEN_VERDICT_SELFTEST: (\d+)/3 pass', out)
        if m and pristine.returncode == 0:
            cases_passed = int(m.group(1))

        mutant_path = os.path.join(tmp, 'golden-verdict-mutant.py')
        mutant_src = tool_bytes.decode(errors='replace')
        applied = mutant_src.count(MUTATION_OLD) == 1
        mutant_src = mutant_src.replace(MUTATION_OLD, MUTATION_NEW)
        with open(mutant_path, 'w', encoding='utf-8') as fh:
            fh.write(mutant_src)
        if applied:
            mutant = subprocess.run([sys.executable, mutant_path, '--selftest'],
                                    capture_output=True)
            mutant_killed = mutant.returncode != 0

        if entry_bytes:
            entry_path = os.path.join(tmp, 'entry.md')
            with open(entry_path, 'wb') as fh:
                fh.write(entry_bytes)
            checked = subprocess.run([sys.executable, tool_path, '--check-entry', entry_path],
                                     capture_output=True)
            entry_ok = checked.returncode == 0

    print('GOLDEN_R38: cases=%d/3 mutant_killed=%s entry_ok=%s tool_sha256=%s rev=%s '
          'C2_R38_PASS=%s'
          % (cases_passed, 'true' if mutant_killed else 'false',
             'true' if entry_ok else 'false', tool_sha, rev,
             'true' if (cases_passed == 3 and mutant_killed and entry_ok) else 'false'))
    return 0 if (cases_passed == 3 and mutant_killed and entry_ok) else 1


if __name__ == '__main__':
    sys.exit(main())
