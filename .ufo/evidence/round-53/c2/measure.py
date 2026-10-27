#!/usr/bin/env python3
"""Round-53 C2 counter: tools/ scratch hygiene (R52.5 + scratch directive 7.4).

Usage: c2/measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain]

Checks, in order (all subject bytes are git objects at REV; runs execute from
a scratch extraction under --work with TMPDIR bound there, never /tmp):
  1. grep    — no committed file under tools/ at REV matches the regex
               dir\\s*=\\s*["']/tmp  (covers tempfile.mkdtemp(dir="/tmp"),
               TemporaryDirectory(dir="/tmp"), and variants).
  2. selftests — extract tools/registry-check.py and tools/env-diff.py at REV;
               TMPDIR=<work>/tmp python3 <tool> --selftest exits 0 for both.
  3. cr47    — TMPDIR=<work>/missing (absent) registry-check --selftest exits
               non-zero and names scratch creation in stderr/stdout; it must
               never print a REGISTRY_CHECK verdict line (an unusable scratch
               is could-not-evaluate, never "differs").
  4. docs    — SKILL.md at REV names no /tmp scratch path for either tool:
               no 'tameshi-f5.json', no 'tameshi-r21-envdiff.*', and the
               sweep recipe's scratch lines name $HYAKU_SCRATCH, not /tmp.
Verdict line: 'C2_R53: rev=... tmp_hits=H registry_selftest=... envdiff_selftest=... cr47=... docs=... total=N C2_R53_PASS=true|false'
Exit 0 iff PASS.  Stdlib only.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

TMP_RE = re.compile(r'dir\s*=\s*["\']/tmp')
FLEET_DOC_PATTERNS = [
    re.compile(r'/tmp/tameshi-f5\.json'),
    re.compile(r'/tmp/tameshi-r21-envdiff'),
    re.compile(r'mkdir -p /tmp/<lane>-r<round>'),
    re.compile(r'Scratch for a sweep: `/tmp/'),
]


def git(args, cwd=None, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git'] + args, cwd=cwd, env=env,
                          capture_output=True, text=False, check=check)


def cat(lane, rev, path):
    if git(['-C', lane, 'cat-file', '-e', '%s:%s' % (rev, path)]).returncode != 0:
        return None
    return git(['-C', lane, 'show', '%s:%s' % (rev, path)]).stdout


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
    rev = git(['-C', lane, 'rev-parse', '--verify', '--end-of-options',
               '%s^{commit}' % a.rev]).stdout.decode().strip()
    problems = []

    # --- 1. grep tools/ at REV ---------------------------------------------
    r = git(['-C', lane, 'grep', '-n', '-E', r'dir\s*=\s*["\']/tmp',
             rev, '--', 'tools/'], check=False)
    hits = r.stdout.decode().split('\n') if r.returncode in (0, 1) else []
    hits = [h for h in hits if h]
    tmp_hits = len(hits)
    if tmp_hits:
        problems.append('tmp-hits %d: %s' % (tmp_hits, hits[:4]))

    # --- 2. selftests with TMPDIR redirected --------------------------------
    tmpdir = work / 'tmp'
    tmpdir.mkdir(exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmpdir))
    results = {}
    for tool in ('registry-check.py', 'env-diff.py'):
        src = cat(lane, rev, 'tools/' + tool)
        if src is None:
            problems.append('tool-missing %s' % tool)
            results[tool] = 'missing'
            continue
        p = work / tool
        p.write_bytes(src)
        r = subprocess.run([sys.executable, str(p), '--selftest'],
                           capture_output=True, text=True, env=env, timeout=900)
        tail = (r.stdout or '').strip().split('\n')[-1] if r.stdout else ''
        results[tool] = 'rc=%d %s' % (r.returncode, tail[:70])
        if r.returncode != 0:
            problems.append('selftest-fail %s %s' % (tool, tail[:90]))

    # --- 3. CR47 -------------------------------------------------------------
    missing = work / 'missing-dir'
    env2 = dict(os.environ, TMPDIR=str(missing))
    p = work / 'registry-check.py'
    if p.exists():
        r = subprocess.run([sys.executable, str(p), '--selftest'],
                           capture_output=True, text=True, env=env2, timeout=900)
        blob = (r.stdout or '') + (r.stderr or '')
        if r.returncode == 0:
            problems.append('cr47-zero-exit')
        if 'REGISTRY_CHECK' in (r.stdout or ''):
            problems.append('cr47-verdict-line')
        if not re.search(r'cannot create (clone )?scratch', blob):
            problems.append('cr47-no-scratch-message')
        results['cr47'] = 'rc=%d' % r.returncode
    else:
        results['cr47'] = 'skipped'

    # --- 4. SKILL.md docs -----------------------------------------------------
    skill = cat(lane, rev, 'SKILL.md')
    docs = 'ok'
    if skill is None:
        problems.append('skill-missing')
        docs = 'missing'
    else:
        text = skill.decode('utf-8', 'replace')
        bad = [p.pattern for p in FLEET_DOC_PATTERNS if p.search(text)]
        if bad:
            docs = 'stale-patterns=%d' % len(bad)
            problems.append('skill-doc-stale %s' % bad)

    ok = not problems
    print('C2_R53: rev=%s tmp_hits=%d registry_selftest=[%s] envdiff_selftest=[%s] cr47=%s docs=%s total=%d C2_R53_PASS=%s'
          % (rev[:12], tmp_hits, results.get('registry-check.py', '?'),
             results.get('env-diff.py', '?'), results.get('cr47', '?'), docs,
             len(problems), 'true' if ok else 'false'))
    if a.explain:
        for p in problems:
            print('PROBLEM', p)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
