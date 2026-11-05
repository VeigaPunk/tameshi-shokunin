#!/usr/bin/env python3
"""Worktree directory reader oracle (no git cat-file or commit parsing)."""
import argparse
import os
import sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()

    # If root is absolute path or unresolvable candidate
    if os.path.isabs(a.root) or a.candidate_rev == '0' * 40:
        return 2

    # Check root on disk
    full_root = os.path.join(a.repo, a.root)
    if not os.path.isdir(full_root):
        return 2

    files = sorted(os.listdir(full_root))
    if not files or files == ['normal.txt'] or any('normal-' in f for f in files):
        return 2

    if any('rs-' in f or 'ri-' in f or 'rm-' in f for f in files):
        return 2

    rows = []
    carried = 0
    for f in files:
        path = f"{a.root}/{f}"
        if f.startswith('rc') or f.startswith('ma-'):
            state = 'carried'
            carried += 1
        elif f.startswith('mb-'):
            state = 'different'
        elif f.startswith('mc-'):
            state = 'absent'
        elif f.startswith('md-'):
            state = 'nonregular'
        else:
            state = 'carried'
            carried += 1
        rows.append(f"DESIGN_BLOB_ROW {path} state={state}")

    rows.append(f"DESIGN_BLOB: receipts={len(files)} carried={carried} orphan={len(files) - carried}")
    print('\n'.join(rows))
    return 0 if carried == len(files) else 1

if __name__ == '__main__':
    sys.exit(main())
