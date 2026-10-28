#!/usr/bin/env python3
"""Round-56 C1 counter: the cold-read floor reads 64 of 64 credited sections, the
eighteen base-lost headings are re-read and bound under one round-56 re-key, and the
standing axis row states the score the monitor actually reads.

Usage: c1/measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain]

Arms (every read is of git objects at REV; the live working tree is never read;
scratch lives under --work and never under /tmp):

  1. precheck  the FROZEN round-48 precheck (bytes at REV) with FLOOR
               0a2010acd1e9 (the round-55 base, which read 64/64) and CAND=REV:
               exit 0 and a last line `... cand_credited=64 lost=0 ok`.
  2. monitor   the unchanged round-21 selector (bytes at REV) over the ledger at
               REV: `sections_covered == 64`, `calibration_restraint_score == 8`,
               `box3_full_page == true`.
  3. rekey     exactly one round-56 re-key directory
               `.ufo/evidence/round-21/coldread/rekey-r56-<c0>` exists at REV
               (recursive listing of the traced paths), <c0> resolves to a commit
               that is REV or an ancestor of REV, and for EVERY heading frozen in
               c1/lost-headings-at-base.json the ledger at REV carries an entry
               whose traces all lie under that directory, whose `read_rev` is <c0>
               (full 40-hex), with wrong_expectations 0 and blocking_gaps 0, and
               which passes the FROZEN round-18 credit algorithm at REV.
  4. readers   for every frozen heading, a committed reader report under
               `.ufo/waves/round-56/w2` or `.../w3` (`T56W*Read*.json`) names the
               heading, pins `cand` = <c0> and `section_sha256` equal to the
               sha256 of that section's bytes at REV (sections computed by the
               FROZEN round-18 sectionize at REV, never a reimplementation).
  5. stable    no entry bound under rekey-r56-* pins LOG.md or SCORECARD.md as an
               input: those two files change on every round after the bind, which
               is exactly how rounds 53 and 55 lost their credit.
  6. restate   the LAST `| calibration |` row of SCORECARD.md at REV states the
               score the monitor reads: its score cell equals the monitor's score
               at REV, its measured-commit cell resolves to a commit that is REV
               or an ancestor of REV and whose monitor score equals that same
               value, its evidence cell names the round-21 monitor, and its
               last-change cell names round 56. A row that asserts 8 while the
               monitor reads 6 is the round-55 routed defect R55.3 this arm
               exists to catch.

Verdict line: `C1_R56: rev=... c0=... credited=.. lost=.. rekeyed=K/18 readers=R/18
monitor=<score>/<credited> unstable=<n> restate=<score@row|none> total=<n>
C1_R56_PASS=true|false`.
Exit 0 iff PASS.  Stdlib only.
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

FLOOR = '0a2010acd1e92e4e332774050825e21bcfc7e079'
PRECHECK = '.ufo/evidence/round-48/quality/coldread-precheck.sh'
R18 = '.ufo/evidence/round-18/measure.py'
R21 = '.ufo/evidence/round-21/coldread/measure.py'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
HEADINGS = '.ufo/evidence/round-56/c1/lost-headings-at-base.json'
WAVE_DIRS = ('.ufo/waves/round-56/w2', '.ufo/waves/round-56/w3')
REKEY_RE = re.compile(r'^rekey-r56-([0-9a-f]{12})$')
UNSTABLE_INPUTS = ('LOG.md', 'SCORECARD.md')
HEX40 = re.compile(r'^[0-9a-f]{40}$')


def lane_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return env


def git(args, check=True):
    return subprocess.run(['git'] + list(args), env=lane_env(),
                          capture_output=True, text=False, check=check)


def show(lane, rev, path):
    r = git(['-C', lane, 'show', '%s:%s' % (rev, path)], check=False)
    return r.stdout if r.returncode == 0 else None


def resolve(lane, prefix):
    r = git(['-C', lane, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % prefix], check=False)
    return r.stdout.decode().strip() if r.returncode == 0 else None


def is_ancestor(lane, older, newer):
    return git(['-C', lane, 'merge-base', '--is-ancestor', older, newer], check=False).returncode == 0


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def monitor_score(lane, rev, r21_bytes, r18_bytes, work, env, tag):
    """Run the frozen round-21 selector (mirrored at its lane-relative path) at REV."""
    mirror = work / ('mirror-' + tag)
    for rel, data in ((R18, r18_bytes), (R21, r21_bytes)):
        target = mirror / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    run = subprocess.run([sys.executable, str(mirror / R21), '--repo', lane, '--rev', rev],
                         capture_output=True, env=env)
    try:
        out = json.loads(run.stdout.decode('utf-8', 'replace'))
    except ValueError:
        return None, None, None
    cold = out.get('coldread') or {}
    return cold.get('sections_covered'), out.get('calibration_restraint_score'), cold.get('box3_full_page')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--explain', action='store_true')
    a = ap.parse_args()
    lane = a.lane
    rev = resolve(lane, a.rev)
    if rev is None:
        print('C1_R56: error=unresolvable-rev total=1 C1_R56_PASS=false')
        return 2
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        print('C1_R56: error=work-not-empty total=1 C1_R56_PASS=false')
        return 2
    env = lane_env()
    env['TMPDIR'] = str(work)
    total = 0
    notes = []

    # ---- arm 1: the frozen precheck ------------------------------------------------
    pre = show(lane, rev, PRECHECK)
    if pre is None:
        print('C1_R56: error=precheck-missing total=1 C1_R56_PASS=false')
        return 1
    pre_path = work / 'coldread-precheck.sh'
    pre_path.write_bytes(pre)
    run = subprocess.run(['bash', str(pre_path), lane, FLOOR, rev], capture_output=True, env=env)
    lines = run.stdout.decode('utf-8', 'replace').strip().splitlines()
    last = lines[-1] if lines else ''
    credited = lost = None
    m = re.search(r'cand_credited=(\d+) lost=(\d+)', last)
    if m:
        credited, lost = int(m.group(1)), int(m.group(2))
    precheck_ok = run.returncode == 0 and m is not None and 'lost=0 ok' in last
    if not precheck_ok:
        total += 1
    if a.explain:
        notes.append('arm1-precheck exit=%d %s' % (run.returncode, last[:200]))

    # ---- arm 2: the unchanged round-21 monitor -------------------------------------
    r21 = show(lane, rev, R21)
    r18 = show(lane, rev, R18)
    ledger_raw = show(lane, rev, LEDGER)
    if r21 is None or r18 is None or ledger_raw is None:
        print('C1_R56: error=monitor-blobs-missing total=1 C1_R56_PASS=false')
        return 1
    (work / 'r18measure.py').write_bytes(r18)
    covered, score, box3 = monitor_score(lane, rev, r21, r18, work, env, 'rev')
    monitor_ok = covered == 64 and score == 8 and box3 is True
    if not monitor_ok:
        total += 1
    if a.explain:
        notes.append('arm2-monitor covered=%s score=%s box3=%s' % (covered, score, box3))

    # ---- sections at REV (frozen sectionize) ---------------------------------------
    r18_mod = load_module(str(work / 'r18measure.py'), 'tameshi_r18_r56')
    skill_raw = show(lane, rev, 'SKILL.md')
    sections = {s['heading']: s for s in r18_mod.sectionize(skill_raw)}
    frozen = json.loads((Path(__file__).resolve().parent / 'lost-headings-at-base.json').read_text('utf-8'))

    # ---- arm 3: the re-key directory and its entries --------------------------------
    tree = git(['-C', lane, 'ls-tree', '-r', '--name-only', rev,
                '.ufo/evidence/round-21/coldread/'], check=False).stdout.decode()
    rekey_dirs = sorted({part for p in tree.splitlines()
                         if '/traces/' in p
                         for part in Path(p).parts if REKEY_RE.fullmatch(part)})
    c0 = None
    rekey_ok = len(rekey_dirs) == 1
    if rekey_ok:
        prefix = REKEY_RE.match(rekey_dirs[0]).group(1)
        c0 = resolve(lane, prefix)
        rekey_ok = (c0 is not None and is_ancestor(lane, c0, rev)
                    and c0.startswith(prefix))
    if a.explain:
        notes.append('arm3-rekey dirs=%s c0=%s' % (rekey_dirs, c0))

    ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
    entries = ledger.get('entries') or []
    rekeyed = 0
    unstable = []
    if rekey_ok:
        rekey_prefix = '.ufo/evidence/round-21/coldread/' + rekey_dirs[0] + '/'
        bound = [e for e in entries if isinstance(e, dict)
                 and any(isinstance(t, str) and t.startswith(rekey_prefix)
                         for t in (e.get('traces') or []))]
        for e in bound:
            inputs = e.get('inputs') or {}
            for p in UNSTABLE_INPUTS:
                if p in inputs:
                    unstable.append('%s:%s' % (e.get('heading', '?')[:40], p))
        for h in frozen:
            good = [e for e in bound
                    if e.get('heading') == h
                    and str(e.get('read_rev')) == c0
                    and (e.get('wrong_expectations') in (0, '0'))
                    and (e.get('blocking_gaps') in (0, '0'))
                    and r18_mod.entry_reason(lane, rev, e, True) is None]
            if good:
                rekeyed += 1
    if rekeyed != len(frozen):
        total += 1
    if unstable:
        total += 1

    # ---- arm 4: committed reader reports -------------------------------------------
    readers = {}
    wave_tree = '\n'.join(git(['-C', lane, 'ls-tree', '-r', '--name-only', rev, wd + '/'],
                               check=False).stdout.decode() for wd in WAVE_DIRS)
    for path in wave_tree.splitlines():
        if not re.search(r'/T56W\d+.*Read.*\.json$', path):
            continue
        raw = show(lane, rev, path)
        if raw is None:
            continue
        try:
            d = json.loads(raw.decode('utf-8', 'surrogateescape'))
        except ValueError:
            continue
        if isinstance(d, dict) and isinstance(d.get('heading'), str):
            readers.setdefault(d['heading'], []).append((path, d))
    reader_ok = 0
    for h in frozen:
        sec = sections.get(h)
        if sec is None:
            continue
        for path, d in readers.get(h, []):
            if d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']:
                reader_ok += 1
                break
    if reader_ok != len(frozen):
        total += 1
    if a.explain:
        notes.append('arm4-readers %d/%d' % (reader_ok, len(frozen)))

    # ---- arm 6: the standing axis row states the score the monitor reads ------------
    card = show(lane, rev, 'SCORECARD.md')
    row_score = row_commit = None
    restate_ok = False
    if card is not None:
        rows = []
        for line in card.decode('utf-8', 'surrogateescape').splitlines():
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) == 5 and cells[0] == 'calibration' and re.fullmatch(r'\d+', cells[1] or ''):
                rows.append(cells)
        if rows:
            cells = rows[-1]
            row_score = int(cells[1])
            hits = [t for t in re.findall(r'[0-9a-f]{7,40}', cells[3]) if resolve(lane, t)]
            row_commit = resolve(lane, hits[0]) if hits else None
            same_at_row = None
            if row_commit and is_ancestor(lane, row_commit, rev):
                _cov, same_at_row, _b = monitor_score(lane, row_commit, r21, r18, work, env, 'row')
            restate_ok = (row_score == score and row_commit is not None
                          and same_at_row == row_score
                          and 'round-21' in cells[2]
                          and re.search(r'\b56\b', cells[4]) is not None)
            if a.explain:
                notes.append('arm6-restate row_score=%s row_commit=%s score_at_row=%s evidence=%r round=%r'
                             % (row_score, (row_commit or 'none')[:12], same_at_row,
                                cells[2][:60], cells[4]))
    if not restate_ok:
        total += 1

    if a.explain:
        for note in notes:
            print('EXPLAIN ' + note)

    print('C1_R56: rev=%s c0=%s credited=%s lost=%s rekeyed=%d/%d readers=%d/%d '
          'monitor=%s/%s unstable=%d restate=%s total=%d C1_R56_PASS=%s'
          % (rev[:12], (c0 or 'none')[:12], credited, lost, rekeyed, len(frozen),
             reader_ok, len(frozen), score, covered, len(unstable),
             row_score if row_score is not None else 'none', total,
             'true' if total == 0 else 'false'))
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
