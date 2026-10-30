#!/usr/bin/env python3
"""Round-58 C1 control ledger generator (used by .ufo/evidence/round-58/controls.sh).

Usage: gen_ledger.py --clone DIR --mode skip|fab|open|bulkopen|quote-file|quote [--commit SHA]
  DIR is a scratch clone checked out at the revision under test (REV); this script rewrites
  `corpus/routed-defects.json` (and, in modes open/bulkopen, `SCORECARD.md`; in mode quote-file a new
  lane file) inside DIR's working tree and prints one JSON stats line. It never touches anything
  outside DIR and never runs git.

The statement set is read from DIR's own `.ufo/evidence/round-58/c1/defects.json`; the ids in it
are the NEW rows. Every row that is not in the set (the 49 original rows) is kept as parsed, so
the control fails by the arm it is built to attack and not by `old49`. Every new row carries a
`status_at_base` (the amended counter requires it): the control states what it claims, never
what the panel says, except where a mode says it copies the panel (`panel_agree` in the stats).

  skip     every new row `declined` (status_at_base `declined`) with a 45-character reason;
           evidence is real and keyed. The declined cap and the fixed floor are non-binding
           (amendment 1), so this control must fail on the BLIND-PANEL arm (panel_over): the
           panel says most items were fixed or open at base, the ledger says declined.
  fab      every new row `fixed`, `commit` = the clone's HEAD (a real ancestor of itself, not an
           ancestor of BASE), evidence path/lines real but the EXCERPT invented (names a key and
           occurs nowhere in the tree). status_at_base copies the panel when it is not `fixed`
           (a forger who copies the panel) else `open`.
  open     every new row `open` with real keyed evidence while the newest `**Planned (round N)`
           paragraph of SCORECARD.md (highest N, ties later: the counter's rule) names no routed
           id (ids are blanked in that paragraph). status_at_base as in fab.
  bulkopen every new row `open` and `status_at_base` `open`; a NEW `**Planned (round N+1)`
           paragraph appended to SCORECARD.md names every id, so the open arm is satisfied and
           the only thing wrong is that the ledger claims nothing was ever fixed: must fail on the
           panel arm.
  quote-file  (step 1 of the wave-1 forgery, committed by controls.sh under an UNRELATED message)
           writes the new lane file `corpus/ctl-quote-housekeeping.md` quoting `key: excerpt` for
           every new row.
  quote    (step 2) every new row `fixed`, `commit` = --commit (the housekeeping commit), evidence
           = the quoted line in the new file. The excerpt is introduced by the commit, the
           commit is a real descendant of BASE and an ancestor of REV, yet the commit message
           names no id and the item text names no such path: must fail `fixed_bad` on the
           amended tie rule. status_at_base copies the panel when it is not `fixed`, else `open`.

Evidence is found in tracked non-`.ufo/` files of DIR (spot-checks and the ledger excluded), then,
for a key only `.ufo/evidence/` carries, by `git grep` there (round-58, waves and reports
excluded): the first line that contains one of the item's keys as a whole token (the counter's rule),
case-insensitively, normalised
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

DEFECTS = '.ufo/evidence/round-58/c1/defects.json'
LEDGER = 'corpus/routed-defects.json'
PANEL = '.ufo/evidence/round-58/c1/panel.json'
QUOTE = 'corpus/ctl-quote-housekeeping.md'
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


def tok(key, text):
    """The counter's key rule (amendment 1): a whole token, not a substring of a longer word or hash."""
    return re.search(r'(?<![\w-])' + re.escape(key) + r'(?![\w-])', text, re.IGNORECASE) is not None


def window(line, key):
    m = re.search(r'(?<![\w-])' + re.escape(key) + r'(?![\w-])', line, re.IGNORECASE)
    i = m.start() if m else line.lower().find(key.lower())
    if len(norm(line)) <= 300:
        return norm(line)
    lo = max(0, i - 100)
    return norm(line[lo:lo + 300])


def grep_evidence(clone, keys, skip):
    """Fallback for a key that only `.ufo/evidence/` carries (never round-58, waves or reports)."""
    for key in keys:
        if len(key) < 3:
            continue
        proc = subprocess.run(['git', '-C', clone, 'grep', '-I', '-n', '-i', '-F', '-e', key, '--',
                               '.ufo/evidence/', ':!.ufo/evidence/round-58/'], capture_output=True)
        for hit in proc.stdout.decode('utf-8', 'replace').splitlines():
            parts = hit.split(':', 2)
            if len(parts) < 3 or parts[0] in skip or not parts[1].isdigit():
                continue
            ex = window(parts[2], key)
            if 15 <= len(ex) <= 400 and tok(key, ex):
                return {'path': parts[0], 'lines': '%s-%s' % (parts[1], parts[1]), 'excerpt': ex}
    return None


def find_evidence(files, keys, clone=None, skip=()):
    for key in keys:
        if len(key) < 3:
            continue
        for path, lines in files:
            for n, line in enumerate(lines, 1):
                if tok(key, line):
                    ex = window(line, key)
                    span = '%d-%d' % (n, n)
                    if len(ex) < 15 and n < len(lines):
                        ex = norm(line + '\n' + lines[n])
                        span = '%d-%d' % (n, n + 1)
                    if 15 <= len(ex) <= 400 and tok(key, ex):
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


def planned_span(lines):
    """(start, end) of the newest `**Planned (round N)` paragraph by round number, ties later: the counter's rule."""
    start, best = None, -1
    for i, line in enumerate(lines):
        m = re.match(r'\*\*Planned \(round (\d+)\)', line)
        if m and int(m.group(1)) >= best:
            start, best = i, int(m.group(1))
    if start is None:
        return None, None, best
    end = start
    while end < len(lines) and lines[end].strip():
        end += 1
    return start, end, best


def blank_planned(clone):
    path = os.path.join(clone, 'SCORECARD.md')
    with open(path, 'r', encoding='utf-8') as fh:
        lines = fh.read().split('\n')
    start, end, _ = planned_span(lines)
    if start is None:
        return 0
    hits = 0
    for i in range(start, end):
        lines[i], k = re.subn(r'\bR\d+\.\d+\b', 'R--', lines[i])
        hits += k
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    return hits


def name_all_planned(clone, ids):
    """Append a NEW newest `**Planned (round N+1)` paragraph naming every id."""
    path = os.path.join(clone, 'SCORECARD.md')
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    _, _, best = planned_span(text.split('\n'))
    para = '**Planned (round %d):** control: every routed item is open and named here: %s.\n' % (
        max(best, 0) + 1, ', '.join(ids))
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text.rstrip('\n') + '\n\n' + para)
    return len(ids)


def panel_verdicts(clone):
    try:
        with open(os.path.join(clone, PANEL), 'r', encoding='utf-8') as fh:
            return json.load(fh).get('verdicts', {})
    except (OSError, ValueError):
        return {}


def claimed_base(verdicts, rid):
    """status_at_base a panel-copying forger writes: the panel's verdict unless it is `fixed`
    (a fixed-at-base claim needs a commit in BASE, which the forger does not have)."""
    v = verdicts.get(rid)
    return v if v in ('open', 'declined') else 'open'


def quote_lines(defects, files, clone, spot):
    out = []
    for d in defects:
        ev, keyed = find_evidence(files, d.get('keys', []), clone, spot)
        key = (d.get('keys') or ['the defect'])[0]
        out.append((key, norm('%s: %s' % (key, ev['excerpt']))[:400], keyed))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', required=True)
    ap.add_argument('--mode', required=True, choices=('skip', 'fab', 'open', 'bulkopen', 'quote-file', 'quote'))
    ap.add_argument('--commit', default=None, help='the housekeeping commit (mode quote)')
    a = ap.parse_args()
    clone = os.path.abspath(a.clone)
    assert len(REASON) == 45, len(REASON)
    if a.mode == 'quote' and not (a.commit and re.match(r'^[0-9a-f]{40}$', a.commit)):
        raise SystemExit('gen_ledger: mode quote needs --commit <40-hex>')
    with open(os.path.join(clone, DEFECTS), 'r', encoding='utf-8') as fh:
        defects = json.load(fh)['defects']
    ids = [d['id'] for d in defects]
    spot = {d['file'] for d in defects}
    files = load_text_files(clone, spot)
    verdicts = panel_verdicts(clone)
    if a.mode == 'quote-file':
        rows = quote_lines(defects, files, clone, spot)
        with open(os.path.join(clone, QUOTE), 'w', encoding='utf-8') as fh:
            fh.write('# Housekeeping notes\n\n' + '\n'.join(r[1] for r in rows) + '\n')
        print(json.dumps({'mode': a.mode, 'file': QUOTE, 'lines': len(rows),
                          'unkeyed': sum(0 if r[2] else 1 for r in rows)}, sort_keys=True))
        return 0
    with open(os.path.join(clone, LEDGER), 'r', encoding='utf-8') as fh:
        doc = json.load(fh)
    keep = [r for r in doc['defects'] if r.get('id') not in set(ids)]
    commit = head(clone)
    rows, unkeyed, agree = [], 0, 0
    if a.mode == 'quote':
        with open(os.path.join(clone, QUOTE), 'r', encoding='utf-8') as fh:
            qlines = fh.read().split('\n')
    for i, d in enumerate(defects):
        row = {'id': d['id'], 'seat': 'ctl-r57', 'note': 'control row, mode ' + a.mode}
        if a.mode == 'quote':
            n = 3 + i
            assert qlines[n - 1].startswith((d.get('keys') or ['the defect'])[0] + ': '), (d['id'], n)
            sab = claimed_base(verdicts, d['id'])
            row.update(status='fixed', status_at_base=sab, commit=a.commit,
                       evidence=[{'path': QUOTE, 'lines': '%d-%d' % (n, n), 'excerpt': qlines[n - 1]}])
        else:
            ev, keyed = find_evidence(files, d.get('keys', []), clone, spot)
            unkeyed += 0 if keyed else 1
            if a.mode == 'skip':
                row.update(status='declined', status_at_base='declined', evidence=[ev], reason=REASON)
            elif a.mode == 'bulkopen':
                row.update(status='open', status_at_base='open', evidence=[ev])
            elif a.mode == 'open':
                sab = claimed_base(verdicts, d['id'])
                row.update(status='open', status_at_base=sab, evidence=[ev])
            else:
                sab = claimed_base(verdicts, d['id'])
                key = (d.get('keys') or ['the defect'])[0]
                invented = ('invented excerpt for the control: %s was repaired by a regression fixture '
                            'that does not exist anywhere in this tree' % key)[:400]
                row.update(status='fixed', status_at_base=sab, commit=commit,
                           evidence=[{'path': ev['path'], 'lines': ev['lines'], 'excerpt': invented}])
        agree += 1 if row['status_at_base'] == verdicts.get(d['id']) else 0
        rows.append(row)
    doc['defects'] = keep + rows
    with open(os.path.join(clone, LEDGER), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    stats = {'mode': a.mode, 'new_rows': len(rows), 'kept_rows': len(keep), 'unkeyed': unkeyed,
             'panel_agree': agree, 'panel_present': bool(verdicts)}
    if a.mode == 'open':
        stats['planned_ids_blanked'] = blank_planned(clone)
    if a.mode == 'bulkopen':
        stats['planned_ids_named'] = name_all_planned(clone, ids)
    if a.mode == 'skip':
        stats['reason_len'] = len(REASON)
    if a.mode == 'quote':
        stats['commit'] = a.commit
    print(json.dumps(stats, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
