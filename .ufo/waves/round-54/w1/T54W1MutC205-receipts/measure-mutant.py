#!/usr/bin/env python3
"""Round-54 C2 counter (operability): one scratch-root exit class across the seven tools.

Usage: c2/measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain]

The lane's tools that allocate scratch through `strict_scratch_root()` share one
declared contract, and this counter measures whether the tree at REV keeps it:

  1. unusable   with TMPDIR set to a nonexistent path, each tool's self-test runs
                exit 2 (could-not-evaluate), name the value it saw and the
                "could-not-evaluate" class on one line, and print no traceback.
  2. empty      with TMPDIR set to the empty string (declared = unset; the
                platform default applies), each self-test exits 0.  This is the
                arm a `_os.environ.get("TMPDIR")` truthiness test already gives
                and the knowledge note must state.
  3. usable     with TMPDIR a fresh directory, each self-test exits 0 and strace
                shows no mkdir under /tmp (the silent-fallback defect round 53
                removed must not return).
  4. docs       `tools/registry.json` at REV carries a `scratch_root` cell on each
                of the seven rows, and every cell names TMPDIR, the empty-string
                arm and the could-not-evaluate exit class.
  5. note       `corpus/knowledge/scratch-root-contract.md` exists at REV, cites
                at least one S row that is `mined` with the note under `used-by`,
                and `corpus/lessons/round-54.md`'s `## Gate` names that S id with
                a 2026-10-28 access date and its URL (the sourced-claim gate).

Verdict line: `C2_R54: rev=... tools=7 unusable_exit2=N naming=N empty_ok=N
usable_ok=N tmp_mkdirs=N docs=N note=1 sources=1 total=N C2_R54_PASS=true|false`.
Exit 0 iff PASS, 1 on a failed arm, 2 on setup error.  Scratch lives under --work.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

TOOLS = [
    ('registry-check', 'tools/registry-check.py', '--selftest', 'registry-check-selftest'),
    ('env-diff', 'tools/env-diff.py', '--selftest', 'env-diff-selftest'),
    ('bash-witness-study', 'tools/bash-witness-study.py', 'selftest', 'bash-witness-selftest'),
    ('evidence-disposition', 'tools/evidence-disposition.py', '--selftest', 'evidence-disposition-selftest'),
    ('pin-disposition', 'tools/pin-disposition.py', '--selftest', 'pin-disposition-selftest'),
    ('context-capture', 'tools/context-capture.py', '--selftest', 'context-capture-selftest'),
    ('repeat-control', 'tools/repeat-control.py', '--selftest', 'repeat-control-selftest'),
]
NOTE = 'corpus/knowledge/scratch-root-contract.md'
LESSON = 'corpus/lessons/round-54.md'
OPENED = '2026-10-28'
TIMEOUT = 900


class Setup(Exception):
    pass


def git(args, lane, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', lane] + list(args), env=env,
                          capture_output=True, text=False, check=check)


def show(lane, rev, path):
    r = git(['show', '%s:%s' % (rev, path)], lane, check=False)
    return r.stdout if r.returncode == 0 else None


def run_tool(clone, tool_path, arg, tmpdir, extra_env=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['TMPDIR'] = tmpdir
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run([sys.executable, tool_path, arg], cwd=clone, env=env,
                          capture_output=True, timeout=TIMEOUT)
    text = (proc.stdout + proc.stderr).decode('utf-8', 'replace')
    return proc.returncode, text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--explain', action='store_true')
    a = ap.parse_args()
    lane = a.lane
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        print('C2_R54: error=work-not-empty total=1 C2_R54_PASS=false')
        return 2
    rev = git(['rev-parse', '--verify', '%s^{commit}' % a.rev], lane).stdout.decode().strip()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    clone = work / 'clone'
    subprocess.run(['git', 'clone', '--shared', '--quiet', lane, str(clone)],
                   env=env, check=True, capture_output=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', rev],
                   env=env, check=True, capture_output=True)

    unusable = work / 'unusable-tmpdir-r54'   # deliberately never created
    usable = work / 'usable-tmpdir'
    usable.mkdir()
    notes = []

    exit2 = naming = empty_ok = usable_ok = 0
    for name, path, arg, _row in TOOLS:
        rc, text = run_tool(str(clone), path, arg, str(unusable))
        ok = (rc == 2 and 'could-not-evaluate' in text and str(unusable) in text
              and 'Traceback (most recent call last)' not in text)
        exit2 += ok
        naming += ('could-not-evaluate' in text and str(unusable) in text)
        if a.explain:
            notes.append('unusable %s rc=%d line=%r' % (name, rc, text.strip().splitlines()[-1][:120]))
        rc2, _ = run_tool(str(clone), path, arg, '')
        empty_ok += (rc2 == 0)
        if a.explain and rc2 != 0:
            notes.append('empty %s rc=%d' % (name, rc2))

    tmp_mkdirs = 0
    for name, path, arg, _row in TOOLS:
        log = work / ('strace-%s.log' % name)
        env2 = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env2['TMPDIR'] = str(usable)
        proc = subprocess.run(['strace', '-f', '-e', 'trace=mkdir,mkdirat', '-o', str(log),
                               sys.executable, path, arg],
                              cwd=str(clone), env=env2, capture_output=True, timeout=TIMEOUT)
        hits = len(re.findall(r'mkdir(?:at)\([^)]*"/tmp', log.read_text(errors='replace')))
        tmp_mkdirs += hits
        usable_ok += 1
        if a.explain and (proc.returncode != 0 or hits):
            notes.append('usable %s rc=%d tmp_mkdirs=%d' % (name, proc.returncode, hits))

    docs = 0
    try:
        registry = json.loads(show(lane, rev, 'tools/registry.json').decode('utf-8'))
    except Exception as exc:
        raise Setup('registry unreadable: %s' % exc)
    rows = registry.get('rows') if isinstance(registry, dict) else registry
    by_name = {}
    for row in rows if isinstance(rows, list) else []:
        by_name[row.get('name')] = row
    for _name, _path, _arg, row_name in TOOLS:
        cell = (by_name.get(row_name) or {}).get('scratch_root')
        if isinstance(cell, str) and all(k in cell for k in ('TMPDIR', 'empty', 'could-not-evaluate')):
            docs += 1

    note = show(lane, rev, NOTE)
    lesson = show(lane, rev, LESSON) or b''
    cited = set(re.findall(r'\bS(\d{3,})\b', note.decode('utf-8', 'replace'))) if note else set()
    sources = (show(lane, rev, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
    mined = set()
    for line in sources.splitlines():
        m = re.match(r'^\s{0,3}\|\s*S(\d{3,})\s*\|(.*)$', line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split('|')]
        if any(c == 'mined' for c in cells) and any(NOTE in c for c in cells):
            mined.add(m.group(1))
    lesson_text = lesson.decode('utf-8', 'replace')
    gate = lesson_text.split('## Gate', 1)[1].split('\n## ', 1)[0] if '## Gate' in lesson_text else ''
    sourced = 0
    for sid in sorted(cited & mined):
        if ('S' + sid) in gate and OPENED in gate and 'http' in gate:
            sourced += 1

    total = 0
    for count in (exit2, naming, empty_ok, usable_ok, docs):
        total += len(TOOLS) - count
    total += 0 if note else 1
    total += 0 if sourced else 1
    for note_line in notes:
        print('EXPLAIN ' + note_line)
    print('C2_R54: rev=%s tools=%d unusable_exit2=%d naming=%d empty_ok=%d usable_ok=%d '
          'tmp_mkdirs=%d docs=%d note=%d sources=%d total=%d C2_R54_PASS=%s'
          % (rev[:12], len(TOOLS), exit2, naming, empty_ok, usable_ok, tmp_mkdirs,
             docs, 1 if note else 0, sourced, total,
             'true' if total == 0 else 'false'))
    return 0 if total == 0 else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Setup as exc:
        print('C2_R54: error=%s total=1 C2_R54_PASS=false' % exc)
        sys.exit(2)
