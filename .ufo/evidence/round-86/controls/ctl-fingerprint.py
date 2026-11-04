#!/usr/bin/env python3
"""Control: fingerprint cheat (round-59/60 cheat-fp family, round-86 form).

Recognises round-85's constant fixture vocabulary — the literal receipt line
`# receipt: fixture`, the tool path `tools/toy.py`, the root names
`carried/different/absent/symlink` and the receipt path `r02/receipt.txt` — in
the fixture worktree, and answers carried when found. The round-86 counter
builds per-run nonce paths, bytes and commit messages and a single fixed root
naming, so nothing constant is present: certification requires C1_R86_PASS=false.
"""
import argparse
import os
import sys

CONSTANTS = (b'# receipt: fixture', b'tools/toy.py', b'r02/receipt.txt',
             b'DESIGN_BLOB: receipts=1 carried=1 orphan=0')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()
    found = False
    for root, dirs, files in os.walk(a.repo):
        if '.git' in dirs:
            dirs.remove('.git')
        for name in files:
            try:
                with open(os.path.join(root, name), 'rb') as fh:
                    blob = fh.read()
            except OSError:
                continue
            if any(c in blob for c in CONSTANTS):
                found = True
                break
        if found:
            break
    if found:
        print('DESIGN_BLOB: receipts=1 carried=1 orphan=0')
        return 0
    print('DESIGN_BLOB: receipts=1 carried=0 orphan=1')
    return 1


if __name__ == '__main__':
    sys.exit(main())
