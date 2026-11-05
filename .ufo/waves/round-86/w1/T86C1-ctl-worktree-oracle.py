#!/usr/bin/env python3
"""Control: counter-fitting worktree oracle (the probe the seat was asked for).

Reads the fixture's own receipt text (design_tool / design_tool_sha256) and
recomputes each state from the WORKTREE instead of the object named by
--candidate-rev. In the round-86 fixture the worktree HEAD is the candidate
commit, so the oracle is right whenever --candidate-rev == HEAD and wrong when
the counter asks about an ancestor (`carried`, candidate = base).
"""
import argparse
import hashlib
import os
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--receipt-rev', required=True)
    p.add_argument('--root', required=True)
    p.add_argument('--candidate-rev', required=True)
    a = p.parse_args()
    if os.path.isabs(a.root):
        return 2
    if a.candidate_rev.strip('0') == '':
        return 2
    root = os.path.join(a.repo, a.root)
    if not os.path.isdir(root):
        return 2
    recs = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if not name.endswith('.txt') or not os.path.isfile(path):
            continue
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
        if '# design_tool:' not in text:
            continue
        fields = {}
        for line in text.splitlines():
            if line.startswith('# ') and ': ' in line:
                k, v = line[2:].split(': ', 1)
                fields[k] = v
        recs.append((a.root.rstrip('/') + '/' + name, fields))
    if not recs:
        return 2
    rows, carried = [], 0
    for path, f in sorted(recs):
        tool = f.get('design_tool')
        want = f.get('design_tool_sha256', '')
        if len(want) != 64 or any(c not in '0123456789abcdef' for c in want):
            return 2
        if 'measured_bytes' not in f:
            return 2
        if 'measured_rev' in f:
            return 2
        target = os.path.join(a.repo, tool)
        if not os.path.lexists(target):
            state = 'absent'
        elif os.path.islink(target) or not os.path.isfile(target):
            state = 'nonregular'
        else:
            with open(target, 'rb') as fh:
                got = hashlib.sha256(fh.read()).hexdigest()
            state = 'carried' if got == want else 'different'
        carried += state == 'carried'
        rows.append('DESIGN_BLOB_ROW %s state=%s' % (path, state))
    rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=%d'
                % (len(recs), carried, len(recs) - carried))
    print('\n'.join(rows))
    return 0 if carried == len(recs) else 1


if __name__ == '__main__':
    sys.exit(main())
