#!/usr/bin/env python3
"""Round-57 C1 control ledger generator (used by .ufo/evidence/round-57/controls.sh).

Usage: gen_ledger.py --clone DIR --mode skip|fab|open
  DIR is a scratch clone checked out at the revision under test (REV); this script rewrites
  `corpus/routed-defects.json` (and, in mode open, `SCORECARD.md`) inside DIR's working tree and
  prints one JSON stats line. It never touches anything outside DIR and never runs git.

The statement set is read from DIR's own `.ufo/evidence/round-57/c1/defects.json`; the ids in it
are the NEW rows. Every row that is not in the set (the 49 original rows) is kept as parsed, so
the control fails by the one arm it is built to attack and not by `old49`.

  skip  every new row `declined` with a 45-character reason; evidence is real and keyed, so the
        only thing wrong is the declined cap (the control that did none of the work and wrote
        down that it declined it).
  fab   every new row `fixed`, `commit` = the clone's HEAD (a real ancestor of itself), evidence
        path/lines real but the EXCERPT invented (it names a key and occurs nowhere in the tree).
  open  every new row `open` with real keyed evidence while the newest `**Planned (round`
        paragraph of SCORECARD.md names no routed id (ids are blanked in that paragraph).

Evidence is found in tracked non-`.ufo/` files of DIR (spot-checks and the ledger excluded), then,
for a key only `.ufo/evidence/` carries, by `git grep` there (round-57, waves and reports
excluded): the first line that contains one of the item's keys case-insensitively, normalised
length 15..400.
An item with no such line gets an UNKEYED fallback row; the count is in the stats line
(`unkeyed`), so a control that fails for the wrong arm says so.
"""
import argparse
import json
import os
import re
import subprocess
import sys

DEFECTS = '.ufo/evidence/round-57/c1/defects.json'
LEDGER = 'corpus/routed-defects.json'
PREFER = ('corpus/', 'SKILL.md', 'tools/', 'SCORECARD.md', 'LOG.md')
MAX_FILE = 3 * 1024 * 1024
REASON = 'control: declined, no change made to the tree'   # 45 characters


def norm(text):
    return ' '.join(text.split())


def head(clone):
    out = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'], capture_output=True, check=True)
    return out.stdout.decode().strip()


def tracked(clone):
    out = subprocess.run(['git', '-C', clone, 'ls-files', '-z'], capture_output=True, check=True)
    return [p for p in out.stdout.decode('utf-8', 'replace').split('\0') if p]


def load_text_files(clone, skip):
    files = []
    for path in tracked(clone):
        if path.startswith('.ufo/') or path == LEDGER or path in skip:
            continue
        full = os.path.join(clone, path)
        try:
            if not os.path.isfile(full) or os.path.getsize(full) > MAX_FILE:
                continue
            with open(full, 'rb') as fh:
                text = fh.read().decode('utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        files.append((path, text.split('\n')))
    files.sort(key=lambda f: (0 if f[0].startswith(PREFER) else 1, f[0]))
    return files


def window(line, key):
    i = line.lower().find(key.lower())
    if len(norm(line)) <= 300:
        return norm(line)
    lo = max(0, i - 100)
    return norm(line[lo:lo + 300])


def grep_evidence(clone, keys, skip):
    """Fallback for a key that only `.ufo/evidence/` carries (never round-57, waves or reports)."""
    for key in keys:
        if len(key) < 3:
            continue
        proc = subprocess.run(['git', '-C', clone, 'grep', '-I', '-n', '-i', '-F', '-e', key, '--',
                               '.ufo/evidence/', ':!.ufo/evidence/round-57/'], capture_output=True)
        for hit in proc.stdout.decode('utf-8', 'replace').splitlines():
            parts = hit.split(':', 2)
            if len(parts) < 3 or parts[0] in skip or not parts[1].isdigit():
                continue
            ex = window(parts[2], key)
            if 15 <= len(ex) <= 400 and key.lower() in ex.lower():
                return {'path': parts[0], 'lines': '%s-%s' % (parts[1], parts[1]), 'excerpt': ex}
    return None


def find_evidence(files, keys, clone=None, skip=()):
    for key in keys:
        if len(key) < 3:
            continue
        low = key.lower()
        for path, lines in files:
            for n, line in enumerate(lines, 1):
                if low in line.lower():
                    ex = window(line, key)
                    span = '%d-%d' % (n, n)
                    if len(ex) < 15 and n < len(lines):
                        ex = norm(line + '\n' + lines[n])
                        span = '%d-%d' % (n, n + 1)
                    if 15 <= len(ex) <= 400 and low in ex.lower():
                        return {'path': path, 'lines': span, 'excerpt': ex}, True
    if clone is not None:
        hit = grep_evidence(clone, keys, skip)
        if hit is not None:
            return hit, True
    # unkeyed fallback: first long-enough line of the first file
    for path, lines in files:
        for n, line in enumerate(lines, 1):
            if len(norm(line)) >= 30:
                return {'path': path, 'lines': '%d-%d' % (n, n), 'excerpt': norm(line)[:300]}, False
    raise SystemExit('gen_ledger: no tracked text file to cite')


def blank_planned(clone):
    path = os.path.join(clone, 'SCORECARD.md')
    with open(path, 'r', encoding='utf-8') as fh:
        lines = fh.read().split('\n')
    start = None
    for i, line in enumerate(lines):
        if line.startswith('**Planned (round'):
            start = i
    if start is None:
        return 0
    end = start
    while end < len(lines) and lines[end].strip():
        end += 1
    hits = 0
    for i in range(start, end):
        lines[i], k = re.subn(r'\bR\d+\.\d+\b', 'R--', lines[i])
        hits += k
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', required=True)
    ap.add_argument('--mode', required=True, choices=('skip', 'fab', 'open'))
    a = ap.parse_args()
    clone = os.path.abspath(a.clone)
    assert len(REASON) == 45, len(REASON)
    with open(os.path.join(clone, DEFECTS), 'r', encoding='utf-8') as fh:
        defects = json.load(fh)['defects']
    ids = [d['id'] for d in defects]
    spot = {d['file'] for d in defects}
    files = load_text_files(clone, spot)
    with open(os.path.join(clone, LEDGER), 'r', encoding='utf-8') as fh:
        doc = json.load(fh)
    keep = [r for r in doc['defects'] if r.get('id') not in set(ids)]
    commit = head(clone)
    rows, unkeyed = [], 0
    for d in defects:
        ev, keyed = find_evidence(files, d.get('keys', []), clone, spot)
        unkeyed += 0 if keyed else 1
        row = {'id': d['id'], 'seat': 'ctl-r57', 'note': 'control row, mode ' + a.mode}
        if a.mode == 'skip':
            row.update(status='declined', evidence=[ev], reason=REASON)
        elif a.mode == 'open':
            row.update(status='open', evidence=[ev])
        else:
            key = (d.get('keys') or ['the defect'])[0]
            invented = ('invented excerpt for the control: %s was repaired by a regression fixture '
                        'that does not exist anywhere in this tree' % key)[:400]
            row.update(status='fixed', commit=commit,
                       evidence=[{'path': ev['path'], 'lines': ev['lines'], 'excerpt': invented}])
        rows.append(row)
    doc['defects'] = keep + rows
    with open(os.path.join(clone, LEDGER), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    stats = {'mode': a.mode, 'new_rows': len(rows), 'kept_rows': len(keep), 'unkeyed': unkeyed}
    if a.mode == 'open':
        stats['planned_ids_blanked'] = blank_planned(clone)
    if a.mode == 'skip':
        stats['reason_len'] = len(REASON)
    print(json.dumps(stats, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
