#!/usr/bin/env python3
"""Round-48 C2 controls (CTL_F, CTL_G, CTL_H) for the freshness counter.

The contract's controls, built as commits in a scratch clone of the lane at BASE:
  CTL_F  the base tree unchanged (rev = BASE, no commit)                  -> refreshed=0
  CTL_G  rows-only: four superseding rows S265-S268 pointing at the round-45 snapshots
         .ufo/evidence/round-45/freshness/sources/T.raw.gz, no round-48 snapshot and no
         round-48 receipt, knowledge entries untouched                    -> refreshed=0
  CTL_H  quote-without-phrase: complete rows, round-48 receipts and snapshots (the round-45
         snapshot bytes re-labelled under .ufo/evidence/round-48/freshness/sources/T.*), the
         Gate lines carrying the round-45 ledger quotes verbatim, entries re-pointed
                                                                          -> refreshed<=2

Each control is scored by running the counter as the brief names it:
  measure.py --lane CLONE --rev <commit> --no-live
and the lines printed here are `CTL_F refreshed=N`, `CTL_G refreshed=N`, `CTL_H refreshed=N`
with the counter's own per-target and summary lines above them as evidence. --no-live is a
probe, never a verdict (the counter prints C2_R48_PARTIAL, not C2_R48_PASS).

Everything happens under --work: `<work>/lane` is a `git clone -q --shared` of the lane, and
every commit is created in that clone (detached from BASE) with an in-repo throwaway
identity. The lane checkout is only read (`git -C LANE show BASE:path`), and this script
never writes, commits or checks out anything in it.

Usage: controls.py --work DIR [--lane LANE] [--measure PATH]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '473336d9d789f6081195e7376d17836a24666bc3'
MEASURE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'T48ExecC2Counter.measure.py')
TARGETS = ('S026', 'S048', 'S093', 'S108')
NEW_ID = {'S026': 'S265', 'S048': 'S266', 'S093': 'S267', 'S108': 'S268'}
SOURCES = 'corpus/SOURCES.md'
LESSONS = 'corpus/lessons/round-48.md'
SNAP_DIR = '.ufo/evidence/round-48/freshness/sources'
SELF_PATH = '.ufo/evidence/round-48/freshness/measure.py'
LEDGER = '.ufo/evidence/round-45/freshness/ledger.json'
OLD_SNAP = '.ufo/evidence/round-45/freshness/sources/%s.raw.gz'
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https://[^\s|,;)\]"\']+')
IDENTITY = ('-c', 'user.name=c2 control', '-c', 'user.email=c2@tameshi.invalid')


def git(repo, *args, binary=False):
    proc = subprocess.run(['git', '-C', repo] + list(args), capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout if binary else proc.stdout.decode('utf-8', 'replace')


def base_rows(lane):
    text = git(lane, 'show', '%s:%s' % (BASE, SOURCES)) or ''
    rows = {}
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.split('|')]
        if len(cells) != 13:
            continue
        rows[cells[1]] = dict(id=cells[1], source=cells[2], anchor=cells[6],
                              teaches=cells[7], status=cells[8], opened=cells[9],
                              recheck=cells[10], usedby=cells[11])
    return text, rows


def base_url(row):
    found = URL_RE.findall(row['source'])
    return found[0] if found else ''


def usedby(paths):
    return ', '.join(paths) if paths else '\u2014'


def insert_rows(sources_text, rows):
    """Append registry rows at the end of the registry table (after its last row)."""
    lines = sources_text.splitlines()
    last = -1
    for index, line in enumerate(lines):
        if ROW_RE.match(line):
            last = index
    if last < 0:
        raise SystemExit('no registry table found at BASE')
    return '\n'.join(lines[:last + 1] + rows + lines[last + 1:]) + '\n'


def gate_lines(quotes):
    return ('# Round-48 lessons (CTL_H control fixture)\n\n'
            '## Gate\n\n' + '\n'.join(
                '- C2-QUOTE %s %s: `%s`' % (NEW_ID[t], t, quotes[t]) for t in TARGETS)
            + '\n')


def repoint(text, row_id, url):
    """Point the entry's `source:` line at the new row and stamp verified-at."""
    lines = text.splitlines()
    out, source_at, verified = [], None, False
    for line in lines:
        stripped = line.strip()
        if source_at is None and stripped.startswith('source:'):
            source_at = len(out)
            out.append('source: %s \u2014 %s \u2014 round-45 snapshot re-labelled as a '
                       '2026-10-26 re-anchor (CTL_H control)' % (row_id, url))
            continue
        if not verified and stripped.startswith('verified-at:'):
            out.append('verified-at: 2026-10-26')
            verified = True
            continue
        out.append(line)
    if source_at is None:
        out.insert(0, 'source: %s \u2014 %s \u2014 CTL_H control' % (row_id, url))
        source_at = 0
    if not verified:
        out.insert(source_at + 1, 'verified-at: 2026-10-26')
    return '\n'.join(out) + '\n'


def rows_for(lane, mode, ledger):
    """Build the four superseding rows for CTL_G (rows-only) or CTL_H (complete)."""
    text, rows = base_rows(lane)
    out = []
    for t in TARGETS:
        row = rows.get(t)
        if row is None:
            raise SystemExit('target %s absent from SOURCES.md at BASE' % t)
        url = base_url(row)
        paths = [p.strip() for p in row['usedby'].split(',')
                 if p.strip() and p.strip() != '\u2014']
        entry = ledger.get(t, {})
        if mode == 'G':
            anchor = '%s @ round-45 snapshot, sha256 %s' % (
                OLD_SNAP % t, str(entry.get('raw_sha256', ''))[:12])
            teaches = ('supersedes %s \u2014 round-45 snapshot pointed at without a round-48 '
                       'snapshot or receipt (CTL_G rows-only control)' % t)
        else:
            anchor = '%s @ fetched 2026-10-26, sha256 %s' % (url, entry['sha12'])
            teaches = ('supersedes %s \u2014 complete row whose Gate quote is the round-45 '
                       'ledger quote verbatim (CTL_H quote-without-phrase control)' % t)
        out.append('| %s | round-48 control re-anchor of %s \u2014 %s | docs | A | control '
                   're-open scope for %s | %s | %s | mined | 2026-10-26 | %s | %s |'
                   % (NEW_ID[t], t, url, t, anchor, teaches, row['recheck'],
                      usedby(paths)))
    return text, rows, out


def clone_lane(lane, work):
    path = os.path.join(work, 'lane')
    if not os.path.isdir(path):
        proc = subprocess.run(['git', 'clone', '-q', '--shared', lane, path],
                              capture_output=True)
        if proc.returncode != 0:
            raise SystemExit('clone failed: %s' % proc.stderr.decode('utf-8', 'replace'))
    return path


def write(repo, path, raw):
    full = os.path.join(repo, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'wb') as handle:
        handle.write(raw if isinstance(raw, bytes) else raw.encode('utf-8'))


def commit(repo, files):
    git(repo, 'checkout', '-q', '--detach', BASE)
    git(repo, 'clean', '-qfd')
    for path, raw in files.items():
        write(repo, path, raw)
    git(repo, 'add', '-A')
    git(repo, *IDENTITY, 'commit', '-q', '-m', 'round-48 C2 control')
    head = git(repo, 'rev-parse', 'HEAD')
    return head.strip() if head else None


def run_measure(measure, clone, rev):
    proc = subprocess.run([sys.executable, measure, '--lane', clone, '--rev', rev,
                           '--no-live'], capture_output=True)
    text = (proc.stdout + proc.stderr).decode('utf-8', 'replace')
    match = re.search(r'refreshed=(\d+)', text)
    return (int(match.group(1)) if match else -1), text


def control(name, measure, clone, rev):
    refreshed, text = run_measure(measure, clone, rev)
    for line in text.splitlines():
        print('  %s | %s' % (name, line))
    print('CTL_%s refreshed=%d' % (name, refreshed))
    return refreshed


def main(argv=None):
    parser = argparse.ArgumentParser(description='round-48 C2 controls F, G, H')
    parser.add_argument('--work', required=True)
    parser.add_argument('--lane', default=LANE)
    parser.add_argument('--measure', default=MEASURE)
    args = parser.parse_args(argv)

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    lane = os.path.abspath(args.lane)
    if not os.path.isfile(args.measure):
        raise SystemExit('measure not found: %s' % args.measure)
    if git(lane, 'rev-parse', '--verify', '%s^{commit}' % BASE) is None:
        raise SystemExit('BASE %s not present in %s' % (BASE, lane))

    clone = clone_lane(lane, work)
    counter = open(args.measure, 'rb').read()

    ledger_text = git(lane, 'show', '%s:%s' % (BASE, LEDGER)) or ''
    ledger = {e.get('id'): e for e in json.loads(ledger_text or '{}').get('entries', [])}

    # CTL_F: the base tree unchanged.
    f_refreshed = control('F', args.measure, clone, BASE)

    # CTL_G: four superseding rows pointing at the round-45 snapshots, nothing else.
    sources, _rows, g_rows = rows_for(lane, 'G', ledger)
    g_rev = commit(clone, {SOURCES: insert_rows(sources, g_rows), SELF_PATH: counter})
    g_refreshed = control('G', args.measure, clone, g_rev)

    # CTL_H: complete rows/receipts/snapshots from the round-45 bytes, round-45 quotes.
    files = {}
    quotes = {}
    hashes = {}
    for t in TARGETS:
        old = git(lane, 'show', '%s:%s' % (BASE, OLD_SNAP % t), binary=True)
        if old is None:
            raise SystemExit('round-45 snapshot absent at BASE: %s' % (OLD_SNAP % t))
        snapshot = '%s/%s.snapshot.html.gz' % (SNAP_DIR, t)
        files[snapshot] = old
        hashes[t] = hashlib.sha256(old).hexdigest()
        quotes[t] = str(ledger.get(t, {}).get('quote', ''))
        if not quotes[t]:
            raise SystemExit('round-45 ledger quote absent for %s' % t)
    ledger = {t: dict(ledger.get(t, {}), sha12=hashes[t][:12]) for t in TARGETS}
    sources, rows, h_rows = rows_for(lane, 'H', ledger)
    for t in TARGETS:
        raw = files['%s/%s.snapshot.html.gz' % (SNAP_DIR, t)]
        receipt = {'url': base_url(rows[t]), 'fetched_at': '2026-10-26T00:00:00Z',
                   'http_status': 200, 'sha256': hashes[t], 'bytes': len(raw)}
        files['%s/%s.receipt.json' % (SNAP_DIR, t)] = (json.dumps(receipt, sort_keys=True,
                                                                 indent=1) + '\n')
        source_path = [p.strip() for p in rows[t]['usedby'].split(',')
                       if p.strip() and p.strip() != '\u2014'][0]
        original = git(lane, 'show', '%s:%s' % (BASE, source_path), binary=True)
        if original is None:
            raise SystemExit('entry absent at BASE: %s' % source_path)
        files[source_path] = repoint(original.decode('utf-8', 'replace'), NEW_ID[t],
                                     base_url(rows[t]))
    files[SOURCES] = insert_rows(sources, h_rows)
    files[LESSONS] = gate_lines(quotes)
    files[SELF_PATH] = counter
    h_rev = commit(clone, files)
    h_refreshed = control('H', args.measure, clone, h_rev)

    ok = f_refreshed == 0 and g_refreshed == 0 and 0 <= h_refreshed <= 2
    print('CONTROLS: F=%d G=%d H=%d expected=F0,G0,H<=2 ok=%s'
          % (f_refreshed, g_refreshed, h_refreshed, 'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
