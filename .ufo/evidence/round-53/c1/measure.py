#!/usr/bin/env python3
"""Round-53 C1 counter: cold-read floor repair, provenance-bound.

Usage: c1/measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain]

Checks, in order (all reads are of git objects at REV; the live working tree
is never read except the lane's .git object store):
  1. floor   — run the FROZEN round-48 precheck (bytes extracted at REV) with
               (LANE, FLOOR ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4, REV);
               require exit 0 and last line 'cand_credited=64 lost=0 ok'.
  2. rekey   — at REV, find the unique .ufo/evidence/round-21/coldread/
               directory 'rekey-r53-<c0>'; <c0> must resolve to a commit that
               is an ancestor of (or equal to) REV.  In the ledger at REV,
               every heading frozen in c1/lost-headings.json must have >=1
               entry whose traces all lie under that rekey directory, whose
               read_rev names <c0>, and whose wrong_expectations and
               blocking_gaps are both 0; every trace path must be a blob at
               REV.
  3. readers — at REV, under .ufo/waves/round-53/, at least one committed
               *Read*.json per frozen heading whose 'heading' matches and
               whose 'section_sha256' equals the sha256 of the section
               bytes at REV (sections computed by the FROZEN round-18
               sectionize extracted at REV — never a reimplementation).
Verdict line: 'C1_R53: rev=... credited=... lost=... rekeyed=K/19 readers=R/19 total=N C1_R53_PASS=true|false'
Exit 0 iff PASS.  Stdlib only; scratch under --work (TMPDIR-honouring), never /tmp.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

FLOOR = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
PRECHECK = '.ufo/evidence/round-48/quality/coldread-precheck.sh'
R18 = '.ufo/evidence/round-18/measure.py'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
HEADINGS = '.ufo/evidence/round-53/c1/lost-headings.json'
HERE = Path(__file__).resolve().parent


def git(args, cwd=None, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git'] + args, cwd=cwd, env=env,
                          capture_output=True, text=False, check=check)


def cat(lane, rev, path):
    r = git(['-C', lane, 'cat-file', '-e', '%s:%s' % (rev, path)], check=False)
    if r.returncode != 0:
        return None
    return git(['-C', lane, 'show', '%s:%s' % (rev, path)], check=False).stdout


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
    credited = lost = None

    # --- 1. frozen precheck -----------------------------------------------
    pre = cat(lane, rev, PRECHECK)
    if pre is None:
        problems.append('precheck-missing-at-rev')
    else:
        p = work / 'precheck.sh'
        p.write_bytes(pre)
        r = subprocess.run(['bash', str(p), lane, FLOOR, rev],
                           capture_output=True, text=True, timeout=1800)
        lines = r.stdout.strip().split('\n')
        last = lines[-1] if lines else ''
        m = re.search(r'cand_credited=(\d+) lost=(\d+) (ok|RED)', last)
        if m:
            credited, lost = int(m.group(1)), int(m.group(2))
        if r.returncode != 0 or not m or credited != 64 or lost != 0 \
                or m.group(3) != 'ok':
            problems.append('precheck-not-green rc=%d last=%r' % (r.returncode, last[-90:]))

    # --- 2. rekey provenance ----------------------------------------------
    r = git(['-C', lane, 'ls-tree', '--name-only', rev,
             '.ufo/evidence/round-21/coldread'])
    rekey_dirs = [n for n in r.stdout.decode().split('\n')
                  if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)]
    c0s = []
    if not rekey_dirs:
        problems.append('rekey-dir-count=0')
    else:
        for d in rekey_dirs:
            c0 = d[len('rekey-r53-'):]
            anc = git(['-C', lane, 'merge-base', '--is-ancestor', c0, rev],
                      check=False)
            if anc.returncode != 0:
                problems.append('c0-not-ancestor %s' % c0)
            else:
                c0s.append(c0)

    def rekey_prefix(entry):
        for t in entry.get('traces', []):
            for c0 in c0s:
                p = '.ufo/evidence/round-21/coldread/rekey-r53-%s/' % c0
                if t.startswith(p):
                    return c0
        return None

    led_raw = cat(lane, rev, LEDGER)
    head_raw = cat(lane, rev, HEADINGS)
    if head_raw is None:
        problems.append('lost-headings-missing-at-rev')
        headings = []
    else:
        headings = json.loads(head_raw.decode())
    if led_raw is None:
        problems.append('ledger-missing')
        ledger = {'entries': []}
    else:
        ledger = json.loads(led_raw.decode())
    entries = ledger.get('entries', [])
    rekeyed = 0
    for h in headings:
        matches = [e for e in entries
                   if isinstance(e, dict) and e.get('heading') == h]
        good = [e for e in matches
                if rekey_prefix(e) is not None
                and str(e.get('read_rev', '')).startswith(rekey_prefix(e))
                and e.get('wrong_expectations') == 0
                and e.get('blocking_gaps') == 0]
        if not good:
            problems.append('rekey-entry-missing %s' % h)
            continue
        ok = True
        for e in good:
            for t in e.get('traces', []):
                if git(['-C', lane, 'cat-file', '-e', '%s:%s' % (rev, t)]
                       ).returncode != 0:
                    problems.append('trace-missing %s' % t)
                    ok = False
        if ok:
            rekeyed += 1

    # --- 3. reader JSONs ----------------------------------------------------
    r = git(['-C', lane, 'ls-tree', '-r', '--name-only', rev,
             '.ufo/waves/round-53'])
    cands = [n for n in r.stdout.decode().split('\n')
             if n.endswith('.json') and 'Read' in n.split('/')[-1]]
    reader_idx = {}
    for n in cands:
        try:
            d = json.loads(cat(lane, rev, n).decode())
        except Exception:
            continue
        if isinstance(d, dict) and 'heading' in d:
            reader_idx.setdefault(d['heading'], []).append((n, d))

    skill = cat(lane, rev, 'SKILL.md')
    if skill is None:
        problems.append('skill-missing')
        sections = {}
    else:
        r18 = work / 'r18measure.py'
        r18.write_bytes(cat(lane, rev, R18))
        spec = importlib.util.spec_from_file_location('tameshi_r18_measure', r18)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sections = {s['heading']: s for s in mod.sectionize(skill)}
    readers = 0
    for h in headings:
        got = False
        for n, d in reader_idx.get(h, []):
            sec = sections.get(h)
            if sec is None:
                break
            if d.get('section_sha256') == sec['sha256']:
                got = True
                break
        if got:
            readers += 1
        else:
            problems.append('reader-missing-or-mismatch %s' % h)

    ok = not problems
    total = len(problems)
    print('C1_R53: rev=%s credited=%s lost=%s rekeyed=%d/%d readers=%d/%d total=%d C1_R53_PASS=%s'
          % (rev[:12], credited, lost, rekeyed, len(headings), readers,
             len(headings), total, 'true' if ok else 'false'))
    if a.explain:
        for p in problems:
            print('PROBLEM', p)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
