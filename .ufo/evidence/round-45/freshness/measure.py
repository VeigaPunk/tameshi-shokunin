#!/usr/bin/env python3
"""Round-45 C1 (freshness) counter: held registry rows re-verified against live bytes.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C1_R45_PASS=true iff fresh >= 50, where fresh = the population rows that are
  `verified` AND carry >= 1 `agree` review by a reviewer other than the entry's
  author AND carry no `dispute` review; the population is the census-valid rows
  at REV with status `mined`, id <= S160 and an http(s) URL in the source cell;
  and the counter's own bytes at REV equal the running file (self_pin=1).

A population row is `verified` iff the round-45 ledger
(.ufo/evidence/round-45/freshness/ledger.json at REV) holds exactly one entry
for its id and that entry
  * has verdict `holds` and opened >= 2026-10-25;
  * names the row's own URL (the first http(s) URL of the source cell, exact);
  * names a snapshot blob present at REV whose raw bytes (gunzipped when the
    path ends in .gz) hash to the entry's raw_sha256;
  * carries a quote of 6..25 whitespace tokens that occurs in the normalized
    text of that snapshot (HTML tags/scripts stripped, entities unescaped; PDF
    through pdftotext; tar member when `member` is given; NFKC, typographic
    quotes/dashes folded, whitespace collapsed);
  * shares >= 2 distinct content words (lowercase [a-z0-9]+, length >= 4, not
    a stopword) with the row's scope + anchor + teaches cells.
Reviews: .ufo/evidence/round-45/freshness/reviews.json at REV,
{"reviews": [{"id", "reviewer", "verdict": "agree"|"dispute", "report", "reason"}]}
— the falsify wave's independent re-judgments. A review counts only when the
reviewer differs from the entry's `author`, is a seat with non-empty output in
the orchestrator-written .ufo/waves/round-45/w2-results.json at REV, and
`report` is a committed path under .ufo/waves/round-45/ whose text names both
the id and the reviewer. A verified quote must also not be copied from the
row's own source/scope/anchor/teaches cells (it is located afresh).
`drifted` = population entries with
verdict `drifted` whose snapshot hash checks (flagged stale items).
`unreachable` = entries with verdict `unreachable` and a non-empty `evidence`.

Modes: --lane L --rev R (deciding/measure); --selftest; --check FRAGMENT.json
(seat helper: grade one entry against the lane worktree files, not REV;
never a measurement); --live (re-fetch each verified row's URL now and report
whether the quote is still present; informational, outside the predicate).
"""
import argparse
import gzip
import hashlib
import html
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import unicodedata

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-45/freshness/measure.py'
LEDGER = '.ufo/evidence/round-45/freshness/ledger.json'
REVIEWS = '.ufo/evidence/round-45/freshness/reviews.json'
RESULTS = '.ufo/waves/round-45/w2-results.json'
TARGET = 50
MAX_ID = 160
MIN_OPENED = '2026-10-25'
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s;,)]+')
STOP = set('''that this with from have will when then than they them their there which
what were been into each such only also more most some your about over under after
before other these those does done must should would could here where while very
just same used uses using page docs fetched opened section''' .split())


def git(lane, *args, binary=False):
    out = subprocess.run(['git', '-C', lane, *args], capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout if binary else out.stdout.decode('utf-8', 'replace')


def parse_rows(text):
    rows = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.split('|')]
        if len(cells) != 13:
            continue
        rid = cells[1]
        url = URL_RE.search(cells[2])
        rows[rid] = dict(id=rid, source=cells[2], scope=cells[5], anchor=cells[6],
                         teaches=cells[7], status=cells[8],
                         url=url.group(0) if url else None)
    return rows


def population(rows):
    return {rid: r for rid, r in rows.items()
            if r['status'] == 'mined' and int(rid[1:]) <= MAX_ID and r['url']}


def fold(text):
    text = unicodedata.normalize('NFKC', text)
    for a, b in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"'),
                 ('\u2013', '-'), ('\u2014', '-'), ('\u00ad', ''), ('\u00a0', ' '),
                 ('\u200b', ''), ('\u200c', ''), ('\u200d', ''), ('\ufeff', '')):
        text = text.replace(a, b)
    return ' '.join(text.split())


def extract(raw, member=None):
    if member:
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:*') as tar:
            raw = tar.extractfile(member).read()
    if raw[:4] == b'%PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            tmp.write(raw)
            tmp.flush()
            out = subprocess.run(['pdftotext', '-enc', 'UTF-8', tmp.name, '-'],
                                 capture_output=True)
            return fold(out.stdout.decode('utf-8', 'replace'))
    text = raw.decode('utf-8', 'replace')
    if re.search(r'<(html|body|div|p|head)\b', text, re.I):
        text = re.sub(r'(?is)<(script|style)\b.*?</\1\s*>', ' ', text)
        text = re.sub(r'(?s)<[^>]*>', ' ', text)
        text = html.unescape(text)
    return fold(text)


def words(text):
    return {w for w in re.findall(r'[a-z0-9]+', text.lower()) if len(w) >= 4 and w not in STOP}


def grade(entry, row, raw):
    """Return (state, reason): state in verified/drifted/unreachable/invalid."""
    verdict = entry.get('verdict')
    if verdict == 'unreachable':
        return ('unreachable', 'ok') if str(entry.get('evidence', '')).strip() else ('invalid', 'no evidence')
    if entry.get('url') != row['url']:
        return 'invalid', 'url mismatch'
    if str(entry.get('opened', '')) < MIN_OPENED:
        return 'invalid', 'opened before round'
    if raw is None:
        return 'invalid', 'snapshot absent'
    if hashlib.sha256(raw).hexdigest() != entry.get('raw_sha256'):
        return 'invalid', 'sha mismatch'
    if verdict == 'drifted':
        return 'drifted', 'ok'
    if verdict != 'holds':
        return 'invalid', 'bad verdict'
    quote = fold(str(entry.get('quote', '')))
    n = len(quote.split())
    if n < 6 or n > 25:
        return 'invalid', 'quote length %d' % n
    try:
        text = extract(raw, entry.get('member'))
    except Exception as exc:  # malformed member or archive
        return 'invalid', 'extract failed: %s' % exc
    if quote not in text:
        return 'invalid', 'quote absent'
    cells = ' '.join((row['source'], row['scope'], row['anchor'], row['teaches']))
    if quote.lower() in fold(cells).lower():
        return 'invalid', 'quote copied from row'
    shared = words(quote) & words(' '.join((row['scope'], row['anchor'], row['teaches'])))
    if len(shared) < 2:
        return 'invalid', 'overlap %d' % len(shared)
    return 'verified', 'ok'


def load_snapshot(read_bytes, path):
    if not path:
        return None
    data = read_bytes(path)
    if data is None:
        return None
    if path.endswith('.gz'):
        try:
            data = gzip.decompress(data)
        except OSError:
            return None
    return data


def wave_seats(results_text):
    """Seat names with non-empty output in an orchestrator-written <wave>-results.json."""
    if not results_text:
        return set()
    data = json.loads(results_text)
    items = data.get('results', []) if isinstance(data, dict) else data
    return {str(x.get('name')) for x in items
            if isinstance(x, dict) and x.get('name') and str(x.get('output') or '').strip()}


def review_sets(verified, reviews, authors, read_text, seats):
    """Independent agree / dispute sets over verified ids.

    A review counts only when its reviewer is named, differs from the entry's
    author, is a seat with non-empty output in the falsify wave's
    orchestrator-written results (`seats`), and its `report` is a path under
    .ufo/waves/round-45/ present at REV whose text names both the id and the
    reviewer. Self-reviews and reviews without a committed report are ignored.
    """
    agreed, disputed = set(), set()
    for r in reviews:
        rid, who, report = r.get('id'), r.get('reviewer'), str(r.get('report', ''))
        if rid not in verified or not who or who == authors.get(rid) or who not in seats:
            continue
        if not report.startswith('.ufo/waves/round-45/'):
            continue
        text = read_text(report)
        if not text or not re.search(r'\b%s\b' % re.escape(rid), text) or who not in text:
            continue
        if r.get('verdict') == 'agree':
            agreed.add(rid)
        elif r.get('verdict') == 'dispute':
            disputed.add(rid)
    return agreed, disputed


def measure(lane, rev):
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = git(lane, 'show', '%s:%s' % (rev, SELF_PATH), binary=True)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    rows = parse_rows(git(lane, 'show', '%s:corpus/SOURCES.md' % rev) or '')
    pop = population(rows)
    ledger_text = git(lane, 'show', '%s:%s' % (rev, LEDGER))
    entries = json.loads(ledger_text)['entries'] if ledger_text else []
    reviews_text = git(lane, 'show', '%s:%s' % (rev, REVIEWS))
    reviews = json.loads(reviews_text)['reviews'] if reviews_text else []
    authors = {e.get('id'): e.get('author') for e in entries}
    counts = {}
    for e in entries:
        counts[e.get('id')] = counts.get(e.get('id'), 0) + 1
    states = {'verified': [], 'drifted': [], 'unreachable': [], 'invalid': []}
    reasons = []
    read = lambda p: git(lane, 'show', '%s:%s' % (rev, p), binary=True)
    for e in entries:
        rid = e.get('id')
        if rid not in pop:
            states['invalid'].append(rid)
            reasons.append('%s not in population' % rid)
            continue
        if counts[rid] != 1:
            states['invalid'].append(rid)
            reasons.append('%s duplicate entry' % rid)
            continue
        state, why = grade(e, pop[rid], load_snapshot(read, e.get('snapshot')))
        states[state].append(rid)
        if state == 'invalid':
            reasons.append('%s %s' % (rid, why))
    verified = set(states['verified'])
    read_text = lambda p: git(lane, 'show', '%s:%s' % (rev, p))
    agreed, disputed = review_sets(verified, reviews, authors, read_text,
                                   wave_seats(read_text(RESULTS)))
    unreviewed = verified - agreed - disputed
    fresh = len(agreed - disputed)
    score = (10 * fresh) // len(pop) if pop else 0
    passed = self_pin == 1 and fresh >= TARGET
    for r in reasons:
        print('INVALID ' + r)
    for rid in sorted(disputed):
        print('DISPUTED ' + rid)
    for rid in sorted(states['drifted']):
        print('DRIFTED ' + rid)
    print('C1_R45: self_pin=%d population=%d entries=%d verified=%d drifted=%d unreachable=%d '
          'invalid=%d unreviewed=%d disputed=%d fresh=%d score=%d target=%d rev=%s C1_R45_PASS=%s' % (
              self_pin, len(pop), len(entries), len(verified), len(states['drifted']),
              len(states['unreachable']), len(states['invalid']), len(unreviewed), len(disputed),
              fresh, score, TARGET, rev, 'true' if passed else 'false'))
    return 0 if passed else 1


def check(lane, rev, fragment, snapdir=None):
    """Seat helper (never a measurement): grade one fragment against the REV registry.

    With --snapdir the raw (uncompressed) snapshot is read from
    SNAPDIR/<basename of the entry's snapshot path without .gz>; otherwise from
    the lane worktree path.
    """
    entry = json.load(open(fragment, encoding='utf-8'))
    pop = population(parse_rows(git(lane, 'show', '%s:corpus/SOURCES.md' % rev) or ''))
    row = pop.get(entry.get('id'))
    if row is None:
        print('CHECK %s invalid not in population' % entry.get('id'))
        return 1
    snapshot = entry.get('snapshot') or ''
    if snapdir:
        name = os.path.basename(snapshot)
        name = name[:-3] if name.endswith('.gz') else name
        full = os.path.join(snapdir, name)
        raw = open(full, 'rb').read() if name and os.path.isfile(full) else None
    else:
        def read(p):
            full = os.path.join(lane, p)
            return open(full, 'rb').read() if os.path.isfile(full) else None
        raw = load_snapshot(read, snapshot)
    state, why = grade(entry, row, raw)
    print('CHECK %s %s %s' % (entry.get('id'), state, why))
    return 0 if state in ('verified', 'drifted', 'unreachable') else 1


def live(lane, rev):
    pop = population(parse_rows(git(lane, 'show', '%s:corpus/SOURCES.md' % rev) or ''))
    ledger_text = git(lane, 'show', '%s:%s' % (rev, LEDGER))
    entries = json.loads(ledger_text)['entries'] if ledger_text else []
    ok = bad = 0
    with tempfile.TemporaryDirectory(prefix='tameshi-r45-live-') as tmp:
        for e in entries:
            if e.get('verdict') != 'holds' or e.get('id') not in pop:
                continue
            target = os.path.join(tmp, 'f')
            res = subprocess.run(['curl', '-fsSL', '--max-time', '60', '-A', 'Mozilla/5.0',
                                  '-o', target, e['url']], capture_output=True)
            present = False
            if res.returncode == 0:
                try:
                    present = fold(e['quote']) in extract(open(target, 'rb').read(), e.get('member'))
                except Exception:
                    present = False
            print('LIVE %s %s' % (e['id'], 'present' if present else 'absent'))
            ok += present
            bad += not present
    print('C1_R45_LIVE: present=%d absent=%d rev=%s' % (ok, bad, rev))
    return 0


def selftest():
    row = dict(id='S001', url='https://example.org/a', scope='mutant states',
               anchor='section Metrics', teaches='score equals detected over valid mutants',
               status='mined', source='x — https://example.org/a')
    page = (b'<html><body><p>The mutation score is detected\xe2\x80\x8b mutants over valid mutants, as a percentage.</p>'
            b'<p>Accept all cookies to continue browsing this website today.</p></body></html>')
    sha = hashlib.sha256(page).hexdigest()
    good = dict(id='S001', url=row['url'], opened='2026-10-25', verdict='holds', raw_sha256=sha,
                quote='The mutation score is detected mutants over valid mutants')
    tagged = page.replace(b'detected mutants', b'<b>detected</b> mutants')
    entity = b'<p>score is detected &amp; valid mutants are counted</p>'
    cases = [
        ('T1_good_verified', good, page, 'verified'),
        ('T2_url_mismatch', dict(good, url='https://example.org/b'), page, 'invalid'),
        ('T3_sha_mismatch', dict(good, raw_sha256='0' * 64), page, 'invalid'),
        ('T4_quote_absent', dict(good, quote='The mutation score is computed by the moon and stars'), page, 'invalid'),
        ('T5_quote_too_long', dict(good, quote=' '.join(['mutants'] * 26)), page, 'invalid'),
        ('T6_quote_too_short', dict(good, quote='detected mutants over valid'), page, 'invalid'),
        ('T7_old_opened', dict(good, opened='2026-10-19'), page, 'invalid'),
        ('T8_boilerplate_no_overlap', dict(good, quote='Accept all cookies to continue browsing this website'), page, 'invalid'),
        ('T9_snapshot_absent', good, None, 'invalid'),
        ('T10_drifted', dict(good, verdict='drifted'), page, 'drifted'),
        ('T11_unreachable_needs_evidence', dict(good, verdict='unreachable'), None, 'invalid'),
        ('T12_unreachable_with_evidence', dict(good, verdict='unreachable', evidence='curl: (22) 403'), None, 'unreachable'),
        ('T13_tag_split_quote', dict(good, raw_sha256=hashlib.sha256(tagged).hexdigest()), tagged, 'verified'),
        ('T14_entity_unescaped', dict(good, raw_sha256=hashlib.sha256(entity).hexdigest(),
                                      quote='score is detected & valid mutants are counted'), entity, 'verified'),
        ('T16_bad_verdict', dict(good, verdict='fine'), page, 'invalid'),
    ]
    failed = 0
    for name, entry, raw, want in cases:
        got, why = grade(entry, row, raw)
        ok = got == want
        failed += not ok
        print('%s %s got=%s want=%s (%s)' % ('PASS' if ok else 'FAIL', name, got, want, why))
    # population / duplicate rules
    rows = parse_rows('| S001 | a — https://e.org/x | docs | A | s | a | t | mined | 2026-10-19 | 180d | p |\n'
                      '  | S161 | b — https://e.org/y | docs | A | s | a | t | mined | 2026-10-25 | 180d | p |\n'
                      '| S002 | c — https://e.org/z | docs | A | s | a | t | queued | 2026-10-19 | 180d | — |\n'
                      '    | S003 | d — https://e.org/w | docs | A | s | a | t | mined | 2026-10-19 | 180d | p |\n')
    pop = sorted(population(rows))
    ok = pop == ['S001']
    failed += not ok
    print('%s T15_population_bounds got=%s' % ('PASS' if ok else 'FAIL', pop))
    authors = {'S001': 'ExecA', 'S002': 'ExecA', 'S003': 'ExecB'}
    rep = '.ufo/waves/round-45/w2/Rev.md'
    reports = {rep: 'RevX RevY RevZ S001 S002 S003 S004 S005 S008'}
    seats = wave_seats(json.dumps({'results': [
        {'name': 'RevX', 'output': 'done'}, {'name': 'RevY', 'output': 'done'},
        {'name': 'ExecA', 'output': 'done'}, {'name': 'RevZ', 'output': ''}]}))
    reviews = [
        {'id': 'S001', 'reviewer': 'RevX', 'verdict': 'agree', 'report': rep},
        {'id': 'S002', 'reviewer': 'ExecA', 'verdict': 'agree', 'report': rep},   # self-review: ignored
        {'id': 'S003', 'reviewer': 'RevX', 'verdict': 'agree', 'report': rep},
        {'id': 'S003', 'reviewer': 'RevY', 'verdict': 'dispute', 'report': rep},  # one dispute sinks it
        {'id': 'S004', 'reviewer': 'RevX', 'verdict': 'agree', 'report': rep},    # not verified: ignored
        {'id': 'S001', 'reviewer': '', 'verdict': 'agree', 'report': rep},
        {'id': 'S005', 'reviewer': 'RevX', 'verdict': 'agree', 'report': '.ufo/waves/round-45/w2/Gone.md'},
        {'id': 'S006', 'reviewer': 'RevX', 'verdict': 'agree', 'report': rep},    # id not named in report
        {'id': 'S007', 'reviewer': 'RevX', 'verdict': 'agree', 'report': '/tmp/Rev.md'},
        {'id': 'S008', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': rep},    # seat without output
        {'id': 'S008', 'reviewer': 'RevQ', 'verdict': 'agree', 'report': rep},    # not a wave seat
    ]
    verified = {'S001', 'S002', 'S003', 'S005', 'S006', 'S007', 'S008'}
    agreed, disputed = review_sets(verified, reviews, authors, reports.get, seats)
    fresh = sorted(agreed - disputed)
    ok = fresh == ['S001'] and disputed == {'S003'}
    failed += not ok
    print('%s T17_independent_reviews fresh=%s disputed=%s' % ('PASS' if ok else 'FAIL', fresh, sorted(disputed)))
    agreed, disputed = review_sets(verified, [], authors, reports.get, seats)
    ok = not agreed and not disputed
    failed += not ok
    print('%s T18_no_reviews_no_fresh' % ('PASS' if ok else 'FAIL'))
    copied = dict(good, quote='The mutation score is detected mutants over valid')
    got, why = grade(copied, dict(row, teaches='the mutation score is detected mutants over valid mutants'), page)
    ok = got == 'invalid' and why == 'quote copied from row'
    failed += not ok
    print('%s T19_quote_copied_from_row got=%s (%s)' % ('PASS' if ok else 'FAIL', got, why))
    print('C1_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + 4, failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--check')
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--extract', help='seat helper: print the normalized text of a raw snapshot file (.gz ok)')
    ap.add_argument('--member')
    ap.add_argument('--snapdir')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.extract:
        raw = open(a.extract, 'rb').read()
        if a.extract.endswith('.gz'):
            raw = gzip.decompress(raw)
        print(extract(raw, a.member))
        return 0
    if not a.lane or not a.rev:
        ap.error('--lane and --rev are required')
    if a.check:
        return check(a.lane, a.rev, a.check, a.snapdir)
    if a.live:
        return live(a.lane, a.rev)
    return measure(a.lane, a.rev)


if __name__ == '__main__':
    sys.exit(main())
