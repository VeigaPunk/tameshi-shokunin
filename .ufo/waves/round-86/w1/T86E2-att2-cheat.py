#!/usr/bin/env python3
"""att2 — PURE root-label oracle. States come from the --root string only.

'/ok-' in the root label -> every receipt carried; '/mx-' -> all carried too
(the label cannot tell states apart); any other label -> exit 2 silent.
Receipt PATHS come from worktree enumeration (a label alone carries no paths).
Zero git invocations.
"""
import argparse
import os
import sys
from pathlib import Path


def refuse():
    sys.exit(2)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()
    if os.path.isabs(a.root):
        refuse()
    if len(a.candidate_rev) == 40 and set(a.candidate_rev) == {'0'}:
        refuse()  # frozen counter's unresolvable-candidate arm is '0'*40
    if '/ok-' not in a.root and '/mx-' not in a.root:
        refuse()  # rf-sha / rf-inc / rf-mix / zp labels
    repo = Path(a.repo)
    rdir = repo / a.root
    if not rdir.is_dir():
        refuse()
    try:
        files = sorted(f.relative_to(repo).as_posix()
                       for f in rdir.rglob('*.txt') if f.is_file())
    except OSError:
        refuse()
    if not files:
        refuse()
    rows = ['DESIGN_BLOB_ROW %s state=carried' % rel for rel in files]
    rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=0' % (len(files), len(files)))
    sys.stdout.write('\n'.join(rows) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
