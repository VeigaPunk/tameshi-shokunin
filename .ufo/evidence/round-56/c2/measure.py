#!/usr/bin/env python3
"""Round-56 C2 counter: every receipt the lane certifies is bound to the revision it
was measured against, and the gate that binds it refuses the real receipts the lane
accepted in rounds 54 and 55.

Usage: c2/measure.py --lane LANE --rev REV --work EMPTY_DIR [--explain]

Arms (every read is of git objects at REV; the live working tree is never read;
scratch lives under --work and never under /tmp):

  1. selftest   the gate's own suite (bytes at REV) passes: `--selftest` exit 0 and
                `GATE_SELFTEST: 14/14 pass`.
  2. red54      the REAL round-54 positive control, sliced to its CTL_POS_c1 line
                (`.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout`,
                bytes copied from `.ufo/evidence/round-54/control/controls-b.stdout`
                at REV), gated as `positive` against the round-54 measured revision
                c2108100 with the round-54 claim surface: exit 3 and
                `RECEIPT_REV_CONTENT_DRIFT` naming the cold-read ledger. AND the
                round-54 deciding gate accepted the same control set:
                `.ufo/evidence/round-54/after/deciding-run.exit` reads
                `DECIDING_RUN_EXIT=0`.
  3. red54b     the whole round-54 control set as `positive` is refused because one
                CTL line names a revision that does not exist in this repo
                (`RECEIPT_REV_UNRESOLVABLE`): the class R53.4 and ER-R54-1 share.
  4. red55      round-55's committed C2 verdict receipt
                (`.ufo/evidence/round-55/after/c2.stdout`, truncated mid-run) gated
                as `verdict` against 4c04c1d3 is refused `RECEIPT_REV_ABSENT` - the
                R55.1 class (no verdict at the measured revision).
  5. own        the round's own control receipts are gated at the certified
                revision: `control/controls-a.stdout` as `control` (every CTL rev an
                ancestor) and `control/controls-b.stdout` as `positive` (the
                positive control names the certified revision or a content-identical
                one on the frozen surface) - exit 0.
  6. docs       the rule is stated where a reader meets it: a `corpus/QUALITY.md`
                criterion names the gate path and its refusal code; a
                `corpus/knowledge/receipt-revision-binding.md` entry opens with
                source/verified-at/recheck and cites a `mined` S-row; the SKILL.md
                `## Standing rules` section names `receipt-revision-gate`; and
                `tools/registry.json` carries a cell for the gate naming at least
                three of its refusal codes.

Verdict line: `C2_R56: rev=... selftest=K/N red54=<codes> red54b=<code> red55=<code>
own=<verdict> docs=<k/4> total=<n> C2_R56_PASS=true|false`.
Exit 0 iff PASS.  Stdlib only.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

GATE = 'tools/receipt-revision-gate.py'
QUALITY = 'corpus/QUALITY.md'
NOTE = 'corpus/knowledge/receipt-revision-binding.md'
SKILL = 'SKILL.md'
REGISTRY = 'tools/registry.json'
SOURCES = 'corpus/SOURCES.md'
R54_CERT = 'c21081008adbb6b6fe4e58a0aeec4831b30e318c'
R55_CERT = '4c04c1d33377e5b6a3636199c5fdda197fc670d5'
R54_SLICE = '.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout'
R54_PATHS = '.ufo/evidence/round-56/c2/red-before/round-54-surface.paths'
R54_CONTROLS = '.ufo/evidence/round-54/control/controls-b.stdout'
R54_EXIT = '.ufo/evidence/round-54/after/deciding-run.exit'
R55_C2 = '.ufo/evidence/round-55/after/c2.stdout'
OWN_A = '.ufo/evidence/round-56/control/controls-a.stdout'
OWN_B = '.ufo/evidence/round-56/control/controls-b.stdout'
OWN_PATHS = '.ufo/evidence/round-56/control/frozen-surface.paths'
CODES = ('RECEIPT_MISSING', 'RECEIPT_EMPTY', 'RECEIPT_NOT_BLOB', 'RECEIPT_REV_ABSENT',
         'RECEIPT_REV_AMBIGUOUS', 'RECEIPT_REV_UNRESOLVABLE', 'RECEIPT_REV_MISMATCH',
         'RECEIPT_REV_CONTENT_DRIFT', 'RECEIPT_CONTROL_NOT_ANCESTOR',
         'RECEIPT_DIGEST_MISMATCH', 'RECEIPT_REQUIRED_LINE_MISSING')


def lane_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return env


def git(args, check=True):
    return subprocess.run(['git'] + list(args), env=lane_env(), capture_output=True, check=check)


def show(lane, rev, path):
    r = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
                       env=lane_env(), capture_output=True)
    return r.stdout if r.returncode == 0 else None


def resolve(lane, rev):
    r = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % rev],
                       env=lane_env(), capture_output=True)
    return r.stdout.decode().strip() if r.returncode == 0 else None


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
        print('C2_R56: error=unresolvable-rev total=1 C2_R56_PASS=false')
        return 2
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        print('C2_R56: error=work-not-empty total=1 C2_R56_PASS=false')
        return 2
    env = lane_env()
    env['TMPDIR'] = str(work)
    gate_raw = show(lane, rev, GATE)
    if gate_raw is None:
        print('C2_R56: error=gate-missing total=1 C2_R56_PASS=false')
        return 1
    gate = work / 'receipt-revision-gate.py'
    gate.write_bytes(gate_raw)
    total = 0
    notes = []

    def run_gate(*args):
        return subprocess.run([sys.executable, str(gate)] + list(args),
                              capture_output=True, env=env, cwd=lane)

    # ---- arm 1: the gate's own suite ------------------------------------------------
    r = run_gate('--selftest')
    out = r.stdout.decode('utf-8', 'replace')
    m = re.search(r'GATE_SELFTEST: (\d+)/(\d+) pass', out)
    selftest = '%s/%s' % (m.group(1), m.group(2)) if m else 'none'
    if not (r.returncode == 0 and m and m.group(1) == m.group(2)):
        total += 1
    if a.explain:
        notes.append('arm1-selftest exit=%d %s' % (r.returncode, selftest))

    # ---- arm 2: the real round-54 positive control, refused -------------------------
    red54 = 'none'
    if show(lane, rev, R54_SLICE) is None or show(lane, rev, R54_PATHS) is None:
        total += 1
        red54 = 'slice-missing'
    else:
        slice_path = work / 'r54-ctl-pos-c1.stdout'
        slice_path.write_bytes(show(lane, rev, R54_SLICE))
        paths_path = work / 'r54-surface.paths'
        paths_path.write_bytes(show(lane, rev, R54_PATHS))
        r = run_gate('--lane', lane, '--certified', R54_CERT, '--paths', str(paths_path),
                     '--receipt', str(slice_path) + ':positive')
        out = r.stdout.decode('utf-8', 'replace')
        codes = re.search(r'codes=(\S+) verdict', out)
        red54 = codes.group(1) if codes else 'none'
        accepted = show(lane, rev, R54_EXIT)
        accepted_ok = accepted is not None and accepted.decode().strip() == 'DECIDING_RUN_EXIT=0'
        if not (r.returncode == 3 and 'RECEIPT_REV_CONTENT_DRIFT' in red54 and accepted_ok):
            total += 1
        if a.explain:
            notes.append('arm2-red54 exit=%d codes=%s old-gate-accepted=%s'
                         % (r.returncode, red54, accepted_ok))

    # ---- arm 3: the whole round-54 control set, refused -----------------------------
    red54b = 'none'
    raw = show(lane, rev, R54_CONTROLS)
    if raw is None:
        total += 1
        red54b = 'receipt-missing'
    else:
        p = work / 'r54-controls-b.stdout'
        p.write_bytes(raw)
        r = run_gate('--lane', lane, '--certified', R54_CERT,
                     '--receipt', str(p) + ':positive')
        out = r.stdout.decode('utf-8', 'replace')
        codes = re.search(r'codes=(\S+) verdict', out)
        red54b = codes.group(1) if codes else 'none'
        if not (r.returncode == 3 and 'RECEIPT_REV_UNRESOLVABLE' in red54b):
            total += 1
        if a.explain:
            notes.append('arm3-red54b exit=%d codes=%s' % (r.returncode, red54b))

    # ---- arm 4: round-55's truncated verdict, refused -------------------------------
    red55 = 'none'
    raw = show(lane, rev, R55_C2)
    if raw is None:
        total += 1
        red55 = 'receipt-missing'
    else:
        p = work / 'r55-c2.stdout'
        p.write_bytes(raw)
        r = run_gate('--lane', lane, '--certified', R55_CERT, '--receipt', str(p) + ':verdict')
        out = r.stdout.decode('utf-8', 'replace')
        codes = re.search(r'codes=(\S+) verdict', out)
        red55 = codes.group(1) if codes else 'none'
        if not (r.returncode == 3 and 'RECEIPT_REV_ABSENT' in red55):
            total += 1
        if a.explain:
            notes.append('arm4-red55 exit=%d codes=%s' % (r.returncode, red55))

    # ---- arm 5: the round's own receipts, accepted ----------------------------------
    own = 'none'
    a_raw = show(lane, rev, OWN_A)
    b_raw = show(lane, rev, OWN_B)
    paths_raw = show(lane, rev, OWN_PATHS)
    if a_raw is None or b_raw is None or paths_raw is None:
        total += 1
        own = 'own-receipts-missing'
    else:
        pa = work / 'own-controls-a.stdout'
        pb = work / 'own-controls-b.stdout'
        pp = work / 'own-surface.paths'
        pa.write_bytes(a_raw)
        pb.write_bytes(b_raw)
        pp.write_bytes(paths_raw)
        r = run_gate('--lane', lane, '--certified', rev, '--paths', str(pp),
                     '--receipt', str(pa) + ':control',
                     '--receipt', str(pb) + ':positive')
        out = r.stdout.decode('utf-8', 'replace')
        m = re.search(r'verdict=(\w+)', out)
        own = m.group(1) if m else 'none'
        if not (r.returncode == 0 and own == 'PASS'):
            total += 1
        if a.explain:
            notes.append('arm5-own exit=%d verdict=%s' % (r.returncode, own))

    # ---- arm 6: the rule is stated where a reader meets it --------------------------
    docs = 0
    quality = show(lane, rev, QUALITY)
    if quality is not None and GATE in quality.decode('utf-8', 'surrogateescape'):
        for code in CODES:
            if code in quality.decode('utf-8', 'surrogateescape'):
                docs += 1
                break
    note = show(lane, rev, NOTE)
    if note is not None:
        text = note.decode('utf-8', 'surrogateescape')
        head = text.split('---', 1)[0]
        if ('source:' in head and 'verified-at:' in head and 'recheck:' in head
                and re.search(r'S\d{3}', head)):
            cited = set(re.findall(r'S(\d{3,})', head))
            sources = (show(lane, rev, SOURCES) or b'').decode('utf-8', 'surrogateescape')
            mined = set()
            for line in sources.splitlines():
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[8] == 'mined':
                    mined.add(cells[0][1:])
            if cited & mined:
                docs += 1
    skill = show(lane, rev, SKILL)
    if skill is not None and 'receipt-revision-gate' in skill.decode('utf-8', 'surrogateescape'):
        docs += 1
    registry = show(lane, rev, REGISTRY)
    if registry is not None:
        text = registry.decode('utf-8', 'surrogateescape')
        if GATE in text:
            hits = sum(1 for code in CODES if code in text)
            if hits >= 3:
                docs += 1
    if docs != 4:
        total += 1
    if a.explain:
        notes.append('arm6-docs %d/4' % docs)

    if a.explain:
        for note in notes:
            print('EXPLAIN ' + note)
    print('C2_R56: rev=%s selftest=%s red54=%s red54b=%s red55=%s own=%s docs=%d/4 total=%d C2_R56_PASS=%s'
          % (rev[:12], selftest, red54, red54b, red55, own, docs, total,
             'true' if total == 0 else 'false'))
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
