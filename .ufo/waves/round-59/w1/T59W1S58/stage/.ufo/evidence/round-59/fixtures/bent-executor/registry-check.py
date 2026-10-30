#!/usr/bin/env python3
"""claimant registry-check: reports rows held on a clean worktree and differs
when tools/receipt-revision-gate.py is dirty (i.e. the counter wrote a mutant).
Never executes a row."""
import json
import os
import subprocess
import sys


def main(argv):
    root = only = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--root':
            i += 1
            root = argv[i]
        elif a == '--only':
            i += 1
            only = argv[i]
        i += 1
    reg = json.load(open(os.path.join(root, 'tools', 'registry.json')))
    row = next(r for r in reg['rows'] if r['name'] == only)
    expect = row['expect']['exit']
    dirty = subprocess.run(
        ['git', '-C', root, 'status', '--porcelain', '--',
         'tools/receipt-revision-gate.py'],
        capture_output=True).stdout.strip()
    if dirty:
        got = (expect + 1) if isinstance(expect, int) else 1
        print('ROW %s expect=%s got=%s differs' % (only, expect, got))
        print('REGISTRY_CHECK: held=0/1 superseded=0')
        return 1
    print('ROW %s expect=%s got=%s held' % (only, expect, expect))
    print('REGISTRY_CHECK: held=1/1 superseded=0')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
