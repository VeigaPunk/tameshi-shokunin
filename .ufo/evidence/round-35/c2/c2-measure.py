#!/usr/bin/env python3
"""c2-measure.py — round-35 C2 counter: self-assessment records vs observed repo state.

Frozen before data (round 35, TameshiR35). Six mismatch classes, each counted over the
committed bytes at REV (plus the fleet working tree for the stranded-file class):

  m1  a knowledge entry whose header block lacks `source:`, `verified-at:` or `recheck:`
      (one count per missing key; QUALITY.md criterion 10)
  m2  a knowledge entry with no row in `corpus/README.md` (QUALITY.md criterion 7)
  m3  a tameshi-attributable seat file left untracked at the FLEET root under `.ufo/waves/`
      (round-34 misroot, flagged by the mori seat)
  m4  a frozen contract's `frozen_artifacts.tool_sha256` that no longer matches the tool
      bytes at REV and has no reconciliation record (round-34 seat ReviewPinChain F1)
  m5  the round-34 `dev/authoring.stdout` final `all_as_expected=False` contradicting
      `dev/authoring-receipts.json` without an adjudication line in the same file
      (round-34 seat PanelSeed4 F1)
  m6  the SCORECARD standing `sources-registry` capability row's stated row count differs
      from the `SOURCES.md` S-row count at REV (round-34 seat AllFourScorecard F1)

Predicate: `C2_R35_PASS` true iff every class counts 0. Counting command:

  python3 .ufo/evidence/round-35/c2/c2-measure.py --lane LANE --rev REV --fleet FLEET

Exit 0 iff the predicate is true. Prints one line per mismatch and the predicate line.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

TRIO = ('source:', 'verified-at:', 'recheck:')
# Criterion 10 (the header trio) landed at the fleet round-1 baseline; entries first added
# AFTER that commit owe the trio, older entries are dated historical notes and are not counted.
BASELINE = '284ab0f0b8b989ee73d9c00c0c0df0a59757af8d'


def git_show(lane, rev, path):
    p = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def git_ls(lane, rev, pattern):
    p = subprocess.run(['git', '-C', lane, 'ls-tree', '-r', '--name-only', rev, pattern], capture_output=True)
    return [x for x in p.stdout.decode().split('\n') if x]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--fleet', required=True)
    a = ap.parse_args()

    lane = os.path.abspath(a.lane)
    rev = subprocess.run(['git', '-C', lane, 'rev-parse', a.rev], capture_output=True).stdout.decode().strip()
    if not rev:
        print('C2_R35: SETUP rev_unresolved=%s' % a.rev)
        return 2

    mismatches = []

    # m1 / m2 -- knowledge entry header trio and README index
    entries = git_ls(lane, rev, 'corpus/knowledge')
    entries = [e for e in entries if e.endswith('.md')]
    readme = (git_show(lane, rev, 'corpus/README.md') or b'').decode()
    for e in entries:
        added = subprocess.run(['git', '-C', lane, 'log', '--diff-filter=A', '-1', '--format=%H',
                                '--', e], capture_output=True).stdout.decode().strip()
        after = bool(added) and subprocess.run(
            ['git', '-C', lane, 'merge-base', '--is-ancestor', BASELINE, added]).returncode == 0
        if not after:
            continue
        text = (git_show(lane, rev, e) or b'').decode()
        # the trio is a top-matter block: it may precede the H1 or follow it, but must appear
        # before the first `##` section (entries in this lane use both layouts)
        header = re.split(r'^## ', text, maxsplit=1, flags=re.M)[0]
        for key in TRIO:
            if not re.search(r'^%s' % re.escape(key), header, re.M):
                mismatches.append('m1 %s missing %s' % (e, key))
        base = os.path.basename(e)
        if 'knowledge/%s' % base not in readme:
            mismatches.append('m2 %s has no corpus/README.md row' % e)

    # m3 -- stranded tameshi seat files at the fleet root
    fleet = os.path.abspath(a.fleet)
    p = subprocess.run(['git', '-C', fleet, 'status', '--porcelain', '--untracked-files=all'],
                       capture_output=True)
    for line in p.stdout.decode().splitlines():
        status, path = line[:2], line[3:].strip()
        if status != '??' or not path.startswith('.ufo/waves/') or path.startswith('.ufo/waves/hyaku/'):
            continue
        fp = os.path.join(fleet, path)
        if not os.path.isfile(fp):
            continue
        try:
            body = open(fp, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        if 'tameshi' in body.lower():
            mismatches.append('m3 %s (untracked seat file: %s)' % (path, status.strip()))

    # m4 -- frozen contract tool pin vs observed tool bytes, unless reconciled
    contract_path = '.ufo/evidence/round-33/contract.json'
    raw = git_show(lane, rev, contract_path)
    if raw:
        contract = json.loads(raw.decode())
        art = contract.get('frozen_artifacts', {})
        tool, pinned = art.get('tool'), art.get('tool_sha256')
        if tool and pinned:
            tool_bytes = git_show(lane, rev, tool)
            observed = hashlib.sha256(tool_bytes).hexdigest() if tool_bytes else '-'
            if observed != pinned:
                rec_raw = git_show(lane, rev, '.ufo/evidence/round-35/pin-reconciliation.json')
                reconciled = False
                if rec_raw:
                    rec = json.loads(rec_raw.decode())
                    for e in rec.get('entries', []):
                        if (e.get('contract') == contract_path and e.get('path') == tool
                                and e.get('old_sha256') == pinned and e.get('new_sha256') == observed):
                            reconciled = True
                if not reconciled:
                    mismatches.append('m4 %s pins %s=%s, observed %s, unreconciled'
                                      % (contract_path, tool, pinned[:16], observed[:16]))
    # m5 -- round-34 authoring receipt disagreement without adjudication
    stdout_raw = git_show(lane, rev, '.ufo/evidence/round-34/dev/authoring.stdout')
    json_raw = git_show(lane, rev, '.ufo/evidence/round-34/dev/authoring-receipts.json')
    if stdout_raw and json_raw:
        stdout = stdout_raw.decode()
        receipts = json.loads(json_raw.decode())
        receipts = receipts if isinstance(receipts, list) else receipts.get('copies', [])
        json_all_ok = all(r.get('as_expected') is True for r in receipts) if receipts else False
        stale = re.search(r'^SEALED: .*all_as_expected=False', stdout, re.M)
        if stale and json_all_ok and not re.search(r'^# ROUND-35 ADJUDICATION', stdout, re.M):
            mismatches.append('m5 dev/authoring.stdout says all_as_expected=False while '
                              'dev/authoring-receipts.json says all true, no adjudication line')

    # m6 -- SCORECARD standing sources-registry row count vs SOURCES.md
    score = (git_show(lane, rev, 'SCORECARD.md') or b'').decode()
    sources = (git_show(lane, rev, 'corpus/SOURCES.md') or b'').decode()
    observed_rows = len(re.findall(r'^\| S\d{3} \|', sources, re.M))
    row = [ln for ln in score.splitlines() if ln.startswith('| sources-registry |')]
    row = row[-1:]  # the LAST standing row is the current claim; earlier ones are dated restatements
    if row:
        m = re.search(r'(\d+) rows', row[0])
        if m and int(m.group(1)) != observed_rows:
            mismatches.append('m6 SCORECARD standing row says %s rows, SOURCES.md has %d'
                              % (m.group(1), observed_rows))

    for mm in mismatches:
        print('MISMATCH %s' % mm)
    print('C2_R35: m1=%d m2=%d m3=%d m4=%d m5=%d m6=%d total=%d entries=%d sources_rows=%d rev=%s C2_R35_PASS=%s'
          % (sum(1 for x in mismatches if x.startswith('m1')),
             sum(1 for x in mismatches if x.startswith('m2')),
             sum(1 for x in mismatches if x.startswith('m3')),
             sum(1 for x in mismatches if x.startswith('m4')),
             sum(1 for x in mismatches if x.startswith('m5')),
             sum(1 for x in mismatches if x.startswith('m6')),
             len(mismatches), len(entries), observed_rows, rev,
             'true' if not mismatches else 'false'))
    return 0 if not mismatches else 1


if __name__ == '__main__':
    sys.exit(main())
