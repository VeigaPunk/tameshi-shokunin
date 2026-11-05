#!/usr/bin/env python3
"""att1 — PURE worktree-reading oracle. Zero git invocations.

Derives every row from the fixture worktree on disk: enumerates *.txt below
--root, parses the design block, classifies the declared tool by its WORKTREE
state (disk bytes / presence / symlink-ness). Never touches git objects.
"""
import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

MARKER = '# measured_bytes: worktree (uncommitted at design_base)'
DESIGN_RE = {
    'base': re.compile(r'^# design_base: (\S+)\s*$', re.M),
    'tool': re.compile(r'^# design_tool: (\S+)\s*$', re.M),
    'sha': re.compile(r'^# design_tool_sha256: (\S+)\s*$', re.M),
}
NORMAL_RE = re.compile(r'^# (measured_rev|tool|tool_sha256|measured_bytes_rev):', re.M)
HEX_RE = re.compile(r'^[0-9a-f]{64}$')


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
    repo = Path(a.repo)
    rdir = repo / a.root
    if not rdir.is_dir():
        refuse()
    rows = []
    carried = 0
    seen = 0
    try:
        files = sorted(f for f in rdir.rglob('*.txt') if f.is_file())
    except OSError:
        refuse()
    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            refuse()
        has_marker = MARKER in text
        has_design = bool(DESIGN_RE['tool'].search(text))
        has_normal = bool(NORMAL_RE.search(text))
        if has_normal and (has_marker or has_design):
            refuse()  # mixed headers
        if not (has_marker and has_design):
            continue  # normal-only receipt: not a design receipt
        m_tool = DESIGN_RE['tool'].search(text)
        m_sha = DESIGN_RE['sha'].search(text)
        m_base = DESIGN_RE['base'].search(text)
        if not (m_tool and m_sha and m_base):
            refuse()  # incomplete marker block
        tool_rel = m_tool.group(1)
        declared = m_sha.group(1)
        if not HEX_RE.match(declared):
            refuse()  # malformed sha
        seen += 1
        tool = repo / tool_rel
        if tool.is_symlink():
            state = 'nonregular'
        elif not tool.is_file():
            state = 'absent'
        else:
            digest = hashlib.sha256(tool.read_bytes()).hexdigest()
            state = 'carried' if digest == declared else 'different'
        if state == 'carried':
            carried += 1
        rows.append('DESIGN_BLOB_ROW %s state=%s'
                    % (f.relative_to(repo).as_posix(), state))
    if seen == 0:
        refuse()  # zero design population
    rows.append('DESIGN_BLOB: receipts=%d carried=%d orphan=%d'
                % (seen, carried, seen - carried))
    sys.stdout.write('\n'.join(rows) + '\n')
    return 0 if carried == seen else 1


if __name__ == '__main__':
    sys.exit(main())
