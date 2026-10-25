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
SELF_PATH = '.ufo/evidence/round-46/hardening/freshness-counter.py'
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
    extra_cases = 0
    _c, _f = extra_HardGrade()
    extra_cases += _c
    failed += _f
    _c, _f = extra_HardPopulation()
    extra_cases += _c
    failed += _f
    _c, _f = extra_HardReviews()
    extra_cases += _c
    failed += _f
    _c, _f = extra_HardMeasure()
    extra_cases += _c
    failed += _f
    print('C1_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + 4 + extra_cases, failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


# HardGrade (tameshi round 46, wave 1): grade() rules F01, F02, F03.
# Each case is the smallest fixture that separates the pristine grade() rule
# from its declared mutant in .ufo/evidence/round-46/hardening/mutants.json:
#   F01 snapshot-absent reason  - a valid `drifted` entry whose snapshot is
#       absent must be refused as invalid 'snapshot absent'; with raw_sha256 of
#       the empty byte string the mutant (raw = b'') falls through the hash
#       check into the drifted return and states 'drifted'.
#   F02 quote upper bound 25    - a 26-token quote that IS present in the
#       snapshot, overlaps the row and is not copied from it is refused.
#   F03 quote presence          - a 6..25-token quote with real row overlap that
#       does NOT occur in the snapshot is refused, with no other rule masking it.


def _xHardGrade_row():
    return dict(id='S001', url='https://example.org/a', scope='flaky failure reports',
                anchor='section Metrics', teaches='flaky failures cluster in the same job',
                status='mined', source='x — https://example.org/a')


def _xHardGrade_page():
    return (b'<html><body><p>Flaky failures cluster inside the same job because the rerun '
            b'repeats one order of the tests only and the second attempt hides the ordering '
            b'defect entirely from the report.</p></body></html>')


def _xHardGrade_quote26():
    # 26 whitespace tokens, verbatim inside _xHardGrade_page().
    return ('Flaky failures cluster inside the same job because the rerun repeats one order of '
            'the tests only and the second attempt hides the ordering defect entirely')


def _xHardGrade_quote10_absent():
    # 10 whitespace tokens, shares 4 content words with the row, absent from the page.
    return 'Flaky failures never appear when the same job reruns alone'


def extra_HardGrade():
    row = _xHardGrade_row()
    page = _xHardGrade_page()
    sha = hashlib.sha256(page).hexdigest()
    good = dict(id='S001', url=row['url'], opened='2026-10-25', verdict='holds',
                raw_sha256=sha, quote=_xHardGrade_quote26())
    empty_sha = hashlib.sha256(b'').hexdigest()
    cases = [
        ('F01_snapshot_absent_reason',
         dict(good, verdict='drifted', raw_sha256=empty_sha), None,
         ('invalid', 'snapshot absent')),
        ('F02_quote_upper_bound_25', good, page, ('invalid', 'quote length 26')),
        ('F03_quote_absent_from_snapshot',
         dict(good, quote=_xHardGrade_quote10_absent()), page,
         ('invalid', 'quote absent')),
    ]
    failed = 0
    for name, entry, raw, want in cases:
        got = grade(entry, row, raw)
        ok = got == want
        failed += not ok
        print('%s %s got=%s want=%s' % ('PASS' if ok else 'FAIL', name, got, want))
    return len(cases), failed


# --- HardPopulation: selftest cases for the three population() survivors F04, F14, F15.
# The round-45 selftest T15 pins only three dimensions of population(): the id above
# MAX_ID (S161), a non-`mined` status that happens to be `queued`, and a row that is
# not indented as a registry row at all. The three cases below pin the remaining
# dimensions, each as the smallest fixture that separates the pristine rule from one
# declared mutant: a control row S100 (URL present, status mined, id <= MAX_ID, so every
# variant includes it) plus exactly one probe row that differs from that control in the
# single dimension under test. No case reads the counter's own bytes.


def _xHardPopulation_row(rid, source, status):
    """One registry line with the 13 pipe-split cells parse_rows() requires."""
    return '| %s | %s | docs | A | s | a | t | %s | 2026-10-19 | 180d | p |\n' % (rid, source, status)


def _xHardPopulation_ids(probe_id, probe_source, probe_status):
    """Sorted population ids of the S100 control row plus one probe row."""
    text = (_xHardPopulation_row('S100', 'a — https://e.org/control', 'mined')
            + _xHardPopulation_row(probe_id, probe_source, probe_status))
    return sorted(population(parse_rows(text)))


def extra_HardPopulation():
    """Return (cases, failed): F04 needs a URL, F14 needs status exactly `mined`,
    F15 needs the MAX_ID bound to be inclusive."""
    cases = failed = 0
    probes = [
        # mutant id, case name, probe id, probe source cell, probe status, expected ids
        ('F04', 'F04_population_requires_url',
         'S101', 'a — this cell carries no link', 'mined', ['S100']),
        ('F14', 'F14_population_status_exactly_mined',
         'S101', 'a — https://e.org/rejected', 'rejected', ['S100']),
        ('F15', 'F15_population_id_bound_inclusive',
         'S%03d' % MAX_ID, 'a — https://e.org/boundary', 'mined',
         sorted(['S100', 'S%03d' % MAX_ID])),
    ]
    for mid, name, pid, src, status, want in probes:
        got = _xHardPopulation_ids(pid, src, status)
        ok = got == want
        cases += 1
        failed += not ok
        print('%s %s got=%s want=%s (%s)' % ('PASS' if ok else 'FAIL', name, got, want, mid))
    return cases, failed


def _xHardReviews_seats(*names):
    """Seats with non-empty output, as the orchestrator would write them."""
    return wave_seats(json.dumps({'results': [{'name': n, 'output': 'done'} for n in names]}))


def _xHardReviews_run(verified, reviews, authors, reports, seats):
    agreed, disputed = review_sets(verified, reviews, authors, reports.get, seats)
    return sorted(agreed), sorted(disputed)


def extra_HardReviews():
    """Cases F06/F07/F08/F09/F13: the review-admission gates of review_sets()/wave_seats().

    Each case pairs one review that must be refused with one independent agree that
    must be admitted, so a gate that silently stops counting anything fails too.
    """
    rep = '.ufo/waves/round-45/w2/R.md'
    ctl = '.ufo/waves/round-45/w2/C.md'
    cases = []

    # F06: a review whose reviewer IS the entry's author, with a report naming both
    # reviewer and id, must still be refused (self-review).
    reports = {rep: 'RevA re-checked S001 and agrees', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevA', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevA', 'verdict': 'agree', 'report': rep},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'RevA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F06_review_non_author', got == (['S002'], []), got))

    # F07: a seat whose output is only whitespace is not a seat.
    seats = wave_seats(json.dumps({'results': [
        {'name': 'RevW', 'output': ' \n\t '}, {'name': 'RevOK', 'output': 'done'}]}))
    cases.append(('F07_seat_output_nonempty', seats == {'RevOK'}, sorted(seats)))

    # F08: a readable report outside .ufo/waves/round-45/ does not admit a review.
    outside = '.ufo/waves/round-44/w1/R.md'
    reports = {outside: 'RevB re-checked S001 and agrees', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevB', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevB', 'verdict': 'agree', 'report': outside},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'ExecA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F08_report_outside_prefix', got == (['S002'], []), got))

    # F09: a report naming the id but not the reviewer does not admit a review.
    reports = {rep: 'S001 was re-checked against the ledger', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevC', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevC', 'verdict': 'agree', 'report': rep},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'ExecA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F09_report_names_reviewer', got == (['S002'], []), got))

    # F13: a verdict that is neither agree nor dispute admits nothing.
    reports = {rep: 'RevD re-checked S001 and is unsure', ctl: 'RevZ re-checked S002 and agrees'}
    seats = _xHardReviews_seats('RevD', 'RevZ')
    got = _xHardReviews_run(
        {'S001', 'S002'},
        [{'id': 'S001', 'reviewer': 'RevD', 'verdict': 'unsure', 'report': rep},
         {'id': 'S002', 'reviewer': 'RevZ', 'verdict': 'agree', 'report': ctl}],
        {'S001': 'ExecA', 'S002': 'ExecB'}, reports, seats)
    cases.append(('F13_verdict_only_agree', got == (['S002'], []), got))

    failed = 0
    for name, ok, got in cases:
        failed += not ok
        print('%s %s got=%r' % ('PASS' if ok else 'FAIL', name, got))
    return len(cases), failed


"""Round-46 C2 seat HardMeasure: measure()-level cases for the round-45 freshness counter.

Four cases, each the smallest scratch-repo fixture that separates the pristine
counter from one declared mutant of mutants.json group `freshness`:

  F05_duplicate_entry_refused  two ledger entries for one population row: the
                               counter must print invalid=2 verified=0, not
                               grade the id twice (invalid=0 verified=1).
  F10_dispute_sinks_agree      one verified row with an agree and a dispute:
                               fresh/score must stay 0, not count the agree.
  F11_self_pin_gates_pass      50 verified+agreed rows with no counter bytes at
                               SELF_PATH (self_pin=0): PASS must stay false.
  F12_target_50_floor          one verified+agreed row with the counter bytes
                               pinned (self_pin=1): fresh=1 < 50, PASS false.

Every case runs the counter CLI as a subprocess in a scratch git repo
(`git init -q -b m`, toplevel asserted equal to the scratch dir, one commit
with `-c user.name=t -c user.email=t@t`, GIT_CONFIG_GLOBAL/SYSTEM=/dev/null)
and reads the counter's printed C1_R45 summary fields plus its exit code.
No case asserts on the counter's source bytes; the F11 fixture simply leaves
SELF_PATH uncommitted, which is the observable self_pin=0 input state.
"""


def _xHardMeasure_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['GIT_CONFIG_GLOBAL'] = '/dev/null'
    env['GIT_CONFIG_SYSTEM'] = '/dev/null'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def _xHardMeasure_git(d, *args):
    out = subprocess.run(['git', '-C', d, '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                         capture_output=True, env=_xHardMeasure_env())
    if out.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (' '.join(args),
                                                  out.stderr.decode('utf-8', 'replace').strip()))
    return out.stdout.decode('utf-8', 'replace')


def _xHardMeasure_build(d, files, pin_self):
    d = os.path.realpath(d)
    _xHardMeasure_git(d, 'init', '-q', '-b', 'm')
    top = _xHardMeasure_git(d, 'rev-parse', '--show-toplevel').strip()
    if os.path.realpath(top) != d:
        raise RuntimeError('repo toplevel %r != scratch dir %r' % (top, d))
    for rel, data in files.items():
        full = os.path.join(d, rel)
        if os.path.dirname(full):
            os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data.encode('utf-8') if isinstance(data, str) else data)
    if pin_self:
        full = os.path.join(d, SELF_PATH)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(open(os.path.abspath(__file__), 'rb').read())
    _xHardMeasure_git(d, 'add', '-A')
    _xHardMeasure_git(d, 'commit', '-q', '-m', 'fixture')
    return d


def _xHardMeasure_run(d):
    try:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                           capture_output=True, text=True, timeout=180, env=_xHardMeasure_env())
    except subprocess.TimeoutExpired:
        return 'timeout', '', 'timeout'
    return p.returncode, p.stdout, p.stderr


def _xHardMeasure_fields(out):
    m = re.search(r'^C1_R45: (.*)$', out, re.M)
    return dict(re.findall(r'(\w+)=(\S+)', m.group(1))) if m else {}


def _xHardMeasure_snapshot(n):
    return ''.join('q%03d marker%03d mutants detected valid alpha%03d\n' % (i, i, i)
                   for i in range(1, n + 1))


def _xHardMeasure_row(i):
    # 11 pipe cells: id | source | docs | A | scope | anchor | teaches | status | opened | ttl | x
    return ('| S%03d | doc%d \u2014 https://e.org/x%03d | docs | A | mutants detected | alpha%03d '
            '| valid | mined | 2026-10-25 | 180d | p |\n' % (i, i, i, i))


def _xHardMeasure_entry(i, sha):
    return dict(id='S%03d' % i, url='https://e.org/x%03d' % i, author='ExecA',
                opened='2026-10-25', verdict='holds', raw_sha256=sha, snapshot='snap/page.txt',
                quote='q%03d marker%03d mutants detected valid alpha%03d' % (i, i, i))


def _xHardMeasure_sha(n):
    return hashlib.sha256(_xHardMeasure_snapshot(n).encode('utf-8')).hexdigest()


def _xHardMeasure_fixture(n, entries, reviews):
    snap = _xHardMeasure_snapshot(n)
    files = {
        'corpus/SOURCES.md': ''.join(_xHardMeasure_row(i) for i in range(1, n + 1)),
        'snap/page.txt': snap,
        '.ufo/evidence/round-45/freshness/ledger.json': json.dumps({'entries': entries}),
        '.ufo/evidence/round-45/freshness/reviews.json': json.dumps({'reviews': reviews}),
        '.ufo/waves/round-45/w2-results.json': json.dumps(
            {'results': [{'name': 'RevX', 'output': 'done'}, {'name': 'RevY', 'output': 'done'}]}),
        '.ufo/waves/round-45/w2/Rev.md': 'RevX RevY ' + ' '.join(
            'S%03d' % i for i in range(1, n + 1)) + '\n',
    }
    return files, hashlib.sha256(snap.encode('utf-8')).hexdigest()


def _xHardMeasure_review(rid, who, verdict):
    return dict(id=rid, reviewer=who, verdict=verdict,
                report='.ufo/waves/round-45/w2/Rev.md', reason='fixture')


def _xHardMeasure_case(name, files, pin_self, want, want_rc):
    """Run one fixture; `want` maps C1_R45 summary field -> expected value."""
    try:
        with tempfile.TemporaryDirectory(prefix='tameshi-r46-hardmeasure-') as d:
            _xHardMeasure_build(d, files, pin_self)
            rc, out, err = _xHardMeasure_run(d)
    except Exception as exc:
        print('FAIL %s harness error: %s' % (name, exc))
        return 0
    fields = _xHardMeasure_fields(out)
    bad = []
    if rc != want_rc:
        bad.append('exit=%s want=%s' % (rc, want_rc))
    for key, val in want.items():
        if fields.get(key) != val:
            bad.append('%s=%s want=%s' % (key, fields.get(key), val))
    if bad:
        print('FAIL %s %s%s' % (name, ' '.join(bad), (' stderr=' + err.strip().splitlines()[-1]) if err.strip() else ''))
        return 0
    print('PASS %s' % name)
    return 1


def extra_HardMeasure():
    cases = failed = 0

    # F05: a second ledger entry for the same population row must be refused as
    # invalid (both copies), not graded twice into verified.
    e1 = _xHardMeasure_entry(1, _xHardMeasure_sha(1))
    files, _ = _xHardMeasure_fixture(1, [e1, dict(e1)], [])
    cases += 1
    failed += not _xHardMeasure_case('F05_duplicate_entry_refused', files, False,
                                     {'population': '1', 'entries': '2',
                                      'verified': '0', 'invalid': '2', 'fresh': '0',
                                      'C1_R45_PASS': 'false'}, 1)

    # F10: a dispute review on a verified id must sink its agree review.
    files, _ = _xHardMeasure_fixture(1, [_xHardMeasure_entry(1, _xHardMeasure_sha(1))],
                                     [_xHardMeasure_review('S001', 'RevX', 'agree'),
                                      _xHardMeasure_review('S001', 'RevY', 'dispute')])
    cases += 1
    failed += not _xHardMeasure_case('F10_dispute_sinks_agree', files, False,
                                     {'verified': '1', 'disputed': '1',
                                      'fresh': '0', 'score': '0', 'C1_R45_PASS': 'false'}, 1)

    # F11: with self_pin=0 the predicate must stay false even at fresh >= TARGET (50).
    n = TARGET
    files, _ = _xHardMeasure_fixture(
        n, [_xHardMeasure_entry(i, _xHardMeasure_sha(n)) for i in range(1, n + 1)],
        [_xHardMeasure_review('S%03d' % i, 'RevX', 'agree') for i in range(1, n + 1)])
    cases += 1
    failed += not _xHardMeasure_case('F11_self_pin_gates_pass', files, False,
                                     {'self_pin': '0', 'population': str(n), 'verified': str(n),
                                      'fresh': str(n), 'target': str(n),
                                      'C1_R45_PASS': 'false'}, 1)

    # F12: TARGET is a floor; fresh=1 with self_pin=1 must not pass.
    files, _ = _xHardMeasure_fixture(1, [_xHardMeasure_entry(1, _xHardMeasure_sha(1))],
                                     [_xHardMeasure_review('S001', 'RevX', 'agree')])
    cases += 1
    failed += not _xHardMeasure_case('F12_target_50_floor', files, True,
                                     {'self_pin': '1', 'verified': '1', 'fresh': '1',
                                      'score': '10', 'target': '50', 'C1_R45_PASS': 'false'}, 1)

    return cases, failed


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
