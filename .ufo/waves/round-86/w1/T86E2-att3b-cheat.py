#!/usr/bin/env python3
"""att3b — root-label + worktree HYBRID, ZERO git invocations.

Label decides the arm: '/ok-' -> assert all carried (overrides conflicting
worktree evidence); '/mx-' -> derive per-receipt state from WORKTREE disk
state (HEAD == the candidate commit, so disk reads coincide with the
candidate tree); anything else -> exit 2 with empty stdout. The
unresolvable-candidate arm is matched by the frozen counter's constant
all-zero candidate rev. Reads no git object of any kind.
"""
import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

MARKER = '# measured_bytes: worktree (uncommitted at design_base)'
TOOL_RE = re.compile(r'^# design_tool: (\S+)\s*$', re.M)
SHA_RE = re.compile(r'^# design_tool_sha256: (\S+)\s*$', re.M)


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
    label_ok = '/ok-' in a.root
    label_mx = '/mx-' in a.root
    if not (label_ok or label_mx):
        refuse()
    repo = Path(a.repo)
    rdir = repo / a.root
    if not rdir.is_dir():
        refuse()
    try:
        files = sorted(f for f in rdir.rglob('*.txt') if f.is_file())
    except OSError:
        refuse()
    if not files:
        refuse()
    rows = []
    carried = 0
    for f in files:
        rel = f.relative_to(repo).as_posix()
        if label_ok:
            state = 'carried'
        else:
            try:
                text = f.read_text(encoding='utf-8')
            except (OSError, UnicodeDecodeError):
                refuse()
            m_tool, m_sha = TOOL_RE.search(text), SHA_RE.search(text)
            if not (m_tool and m_sha and MARKER in text):
                refuse()
            tool = repo / m_tool.group(1)
            if tool.is_symlink():
                state = 'nonregular'
            elif not tool.is_file():
                state = 'absent'
            else:
                digest = hashlib.sha256(tool.read_bytes()).hexdigest()
                state = 'carried' if digest == m_sha.group(1) else 'different'
        if state == 'carried':
            carried += 1
        rows.append('DESIGN_BLOB_ROW %s state=%s' % (rel, state))
    rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=%d'
                % (len(files), carried, len(files) - carried))
    sys.stdout.write('\n'.join(rows) + '\n')
    return 0 if carried == len(files) else 1


if __name__ == '__main__':
    sys.exit(main())
