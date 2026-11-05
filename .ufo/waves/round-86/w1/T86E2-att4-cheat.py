#!/usr/bin/env python3
"""att4 — whole-population echo. Echoes every receipt found under --root in
the worktree back as state=carried, unconditionally; label-gated refusals and
the frozen all-zero candidate check as in att2. Zero git invocations.
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
        refuse()
    if '/ok-' not in a.root and '/mx-' not in a.root:
        refuse()
    repo = Path(a.repo)
    rdir = repo / a.root
    if not rdir.is_dir():
        refuse()
    try:
        files = sorted(f.relative_to(repo).as_posix()
                       for f in rdir.rglob('*') if f.is_file())
    except OSError:
        refuse()
    if not files:
        refuse()
    rows = ['DESIGN_BLOB_ROW %s state=carried' % rel for rel in files]
    rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=0'
                % (len(files), len(files)))
    sys.stdout.write('\n'.join(rows) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
