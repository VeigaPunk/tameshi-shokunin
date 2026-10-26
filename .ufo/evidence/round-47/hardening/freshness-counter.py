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
SELF_PATH = '.ufo/evidence/round-47/hardening/freshness-counter.py'
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
    _c, _f = extra_T47HardFreshCheck()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardFreshLiveA()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardFreshLiveB()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardFreshMeasure()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardFreshParse()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardFreshText()
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


# --- T47HardFreshCheck (tameshi round 47, wave 1): selftest cases for check(), the
# `--check FRAGMENT.json` seat helper. check() is never reached by the round-45/46
# selftest, so every rule in it survives today. Each case below calls check() with a
# scratch git lane (one population row S001 at rev `m`) plus a snapshot directory and
# a fragment file, and asserts the printed CHECK line and the exact exit code:
#   check:cmp:0  `row is None` inverted -> a row that IS in the population is answered
#               'invalid not in population' with exit 1 instead of being graded.
#   check:bool:1 rev registry `or ''` -> `and ''`: the population is always empty, so
#               the same in-population row is answered 'not in population'.
#   check:bool:0 `entry.get('snapshot') or ''` -> `and ''`: the snapshot name becomes
#               '', the snapshot is never read and a valid entry grades 'invalid'.
#   check:cmp:1 / check:int:1  the final mapping `0 if state in (...) else 1`:
#               a verified entry must exit 0; the mutants exit 1.
#   check:int:0 the early `row is None` exit 1 must stay exactly 1 (mutant: 2).
#   check:int:2 the final `else 1` for an invalid state must stay exactly 1 (mutant: 2).
#   check:int:3 the `.gz` suffix strip drops 3 chars (`page.txt.gz` -> `page.txt`);
#               dropping 4 (`page.tx`) loses the snapshot the snapdir holds.
#   check:bool:2 `name and os.path.isfile(full)` -> `or`: a named-but-absent snapshot
#               must grade 'invalid snapshot absent' (exit 1), not raise FileNotFoundError.
# No case reads the counter's own bytes; every separating input is a value check() returns.
import contextlib
import shutil


def _xT47HardFreshCheck_row():
    """The one population row (13 pipe cells) the scratch lane commits."""
    return ('| S001 | x \u2014 https://example.org/a | docs | A | flaky failure reports | '
            'section Metrics | flaky failures cluster in the same job | mined | 2026-10-25 '
            '| 180d | p |\n')


def _xT47HardFreshCheck_page():
    return (b'<html><body><p>Flaky failures cluster inside the same job because the rerun '
            b'repeats one order of the tests only and the second attempt hides the ordering '
            b'defect entirely from the report.</p></body></html>')


def _xT47HardFreshCheck_quote():
    """10 tokens: verbatim in the page, absent from the row cells, 3 shared content words."""
    return 'Flaky failures cluster inside the same job because the rerun'


def _xT47HardFreshCheck_entry(**kw):
    e = dict(id='S001', url='https://example.org/a', opened='2026-10-25', verdict='holds',
             raw_sha256=hashlib.sha256(_xT47HardFreshCheck_page()).hexdigest(),
             snapshot='snap/page.txt', quote=_xT47HardFreshCheck_quote())
    e.update(kw)
    return e


def _xT47HardFreshCheck_lane():
    """Scratch git lane carrying corpus/SOURCES.md at branch `m`; built via _xHardMeasure_build."""
    d = tempfile.mkdtemp(prefix='tameshi-r47-t47fresh-')
    _xHardMeasure_build(d, {'corpus/SOURCES.md': _xT47HardFreshCheck_row()}, False)
    return d


def _xT47HardFreshCheck_snapdir(name):
    """Snapshot directory holding the raw page under `name` (the .gz-compat lookup name)."""
    d = tempfile.mkdtemp(prefix='tameshi-r47-t47snap-')
    with open(os.path.join(d, name), 'wb') as fh:
        fh.write(_xT47HardFreshCheck_page())
    return d


def _xT47HardFreshCheck_run(lane, entry, snapdir):
    """check(lane, 'm', fragment, snapdir) with stdout captured; ('raised', text) on an exception."""
    fd, frag = tempfile.mkstemp(suffix='.json', prefix='tameshi-r47-t47frag-')
    os.close(fd)
    try:
        with open(frag, 'w', encoding='utf-8') as fh:
            json.dump(entry, fh)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = check(lane, 'm', frag, snapdir)
        except Exception as exc:  # the mutant's observable, never a kill by itself
            return 'raised %s' % type(exc).__name__, buf.getvalue()
        return rc, buf.getvalue()
    finally:
        try:
            os.unlink(frag)
        except OSError:
            pass


def _xT47HardFreshCheck_case(name, lane, entry, snapdir, want_rc, want_text):
    """One case: exact exit code and the CHECK line substring check() must print."""
    rc, text = _xT47HardFreshCheck_run(lane, entry, snapdir)
    ok = rc == want_rc and want_text in text
    last = text.strip().splitlines()[-1] if text.strip() else ''
    print('%s %s exit=%r want_exit=%r want=%r got=%r' % (
        'PASS' if ok else 'FAIL', name, rc, want_rc, want_text, last[:120]))
    return int(not ok)


def extra_T47HardFreshCheck():
    """Cases for the check() lineages: row lookup, snapshot name, .gz strip, state->exit map."""
    cases = failed = 0
    lane = snapdir = None
    try:
        lane = _xT47HardFreshCheck_lane()
        snapdir = _xT47HardFreshCheck_snapdir('page.txt')

        # cmp:0 / bool:1 / bool:0 / cmp:1 / int:1: an in-population row with a readable
        # snapshot must be graded verified ('verified ok') and exit 0. Every one of those
        # mutants turns this either into 'invalid not in population' or into exit 1.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H01_row_in_population_verified', lane, _xT47HardFreshCheck_entry(), snapdir,
            0, 'CHECK S001 verified ok')

        # int:0: the early missing-row exit must be exactly 1 (mutant returns 2). The
        # mutant cmp:0 instead falls through to grade(None) and raises, also a named FAIL.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H02_row_absent_exit_1', lane, _xT47HardFreshCheck_entry(id='S999'), snapdir,
            1, 'CHECK S999 invalid not in population')

        # int:3: entry names snap/page.txt.gz, the snapdir holds the raw page as page.txt;
        # the 3-char strip finds it, the mutant's 4-char strip looks for page.tx and grades
        # 'invalid snapshot absent' with exit 1.
        gz = _xT47HardFreshCheck_snapdir('page.txt')
        try:
            cases += 1
            failed += _xT47HardFreshCheck_case(
                'H03_gz_suffix_strip', lane,
                _xT47HardFreshCheck_entry(snapshot='snap/page.txt.gz'), gz,
                0, 'CHECK S001 verified ok')
        finally:
            shutil.rmtree(gz, ignore_errors=True)

        # bool:2: a snapshot name whose file is absent must grade 'invalid snapshot absent'
        # with exit 1. The `or` mutant opens the missing path and raises FileNotFoundError.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H04_missing_snapshot_no_raise', lane,
            _xT47HardFreshCheck_entry(snapshot='snap/absent.txt'), snapdir,
            1, 'CHECK S001 invalid snapshot absent')

        # int:2: a present row whose bytes do not hash must grade invalid with exit exactly 1
        # (mutant: else 2). The other final-mapping mutants are pinned by H01.
        cases += 1
        failed += _xT47HardFreshCheck_case(
            'H05_invalid_state_exit_1', lane,
            _xT47HardFreshCheck_entry(raw_sha256='0' * 64), snapdir,
            1, 'CHECK S001 invalid sha mismatch')
    except Exception as exc:
        cases += 1
        failed += 1
        print('FAIL T47HardFreshCheck_harness raised %s: %s' % (type(exc).__name__, exc))
    finally:
        for d in (lane, snapdir):
            if d:
                shutil.rmtree(d, ignore_errors=True)
    return cases, failed


# --- HardFreshLive (tameshi round 47, wave 1, seat T47HardFreshLiveA): live() cases.
# live() (the --live re-fetch mode) runs outside selftest() today, so the seven pool
# survivors below had no case at all. Every case here drives live() through a fixture
# git lane (corpus/SOURCES.md + the round-45 ledger at LEDGER) and a stub `curl` placed
# first on PATH inside the case: no network is touched, and the stub's exit code plus
# the bytes it writes to the `-o` target are the only inputs. Each assertion reads the
# rule's own observable output (the `LIVE <id> present|absent` lines and the
# `C1_R45_LIVE: present=N absent=M` summary) and its return code, never the source text.
#   L01 present fetch        - one `holds` entry in the population, stub exits 0 with a
#       body containing the quote: summary must be present=1 absent=0 and one
#       `LIVE S001 present` line. Separates live:int:0 (`ok = bad = 1` -> 2/1),
#       live:int:1 (`return 1`), live:bool:0 (`or`->`and` empties the population ->
#       0/0 and no LIVE line), live:cmp:0 (`returncode != 0` skips the body check ->
#       0/1) and live:not:0 (`bad += present` -> 1/1).
#   L02 fetch failure        - stub exits 22 and writes nothing: a non-zero fetch is
#       `absent`, not `present`. Separates live:const:0 (`present = True` survives the
#       skipped body check -> present=1 absent=0).
#   L03 non-holds skipped    - the only ledger entry is `drifted` and IS in the
#       population: the gate `verdict != 'holds' or id not in pop` must skip it, so no
#       LIVE line and present=0 absent=0. Separates live:bool:1 (`or`->`and` makes the
#       gate False for `drifted`-in-population, so the entry is fetched -> 1/0).
#   L04 unreadable target    - stub exits 0 but writes no target: the body read raises
#       and the entry is `absent`. Separates live:const:2 (`present = True` in the
#       except arm -> present=1 absent=0).
_xT47HardFreshLiveA_QUOTE = 'Flaky failure reports are retained only when the rerun reproduces them'

# The fetched body: plain text (no tags), so extract() only folds it and the quote is present.
_xT47HardFreshLiveA_PAGE = (_xT47HardFreshLiveA_QUOTE
                            + ' verbatim inside the fetched body.\n').encode('utf-8')

# Stub `curl`: copy the body to the path after `-o`, then exit with the wanted code.
# Both are handed over through the environment so one stub serves every case.
_xT47HardFreshLiveA_STUB = '''#!/bin/sh
out=''
prev=''
for a in "$@"; do
  if [ "$prev" = '-o' ]; then out="$a"; fi
  prev="$a"
done
if [ -n "$out" ] && [ -n "$X47LIVE_BODY" ] && [ -f "$X47LIVE_BODY" ]; then
  cp "$X47LIVE_BODY" "$out" || exit 99
fi
exit "${X47LIVE_RC:-0}"
'''


def _xT47HardFreshLiveA_row(rid, url, status):
    """One registry line with the 13 pipe-split cells parse_rows() requires."""
    return '| %s | doc \u2014 %s | docs | A | s | a | t | %s | 2026-10-25 | 180d | p |\n' % (rid, url, status)


def _xT47HardFreshLiveA_lane(entries):
    """A throwaway git lane holding corpus/SOURCES.md and the ledger; returns (dir, rev)."""
    d = os.path.realpath(tempfile.mkdtemp(prefix='t47-freshlive-lane-'))
    subprocess.run(['git', '-C', d, 'init', '-q'], capture_output=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != d:
        raise RuntimeError('fixture toplevel %r != %r' % (top, d))
    os.makedirs(os.path.join(d, 'corpus'))
    with open(os.path.join(d, 'corpus', 'SOURCES.md'), 'w', encoding='utf-8') as fh:
        fh.write(''.join(_xT47HardFreshLiveA_row(e['id'], e['url'], 'mined') for e in entries))
    led = os.path.join(d, *LEDGER.split('/'))
    os.makedirs(os.path.dirname(led))
    with open(led, 'w', encoding='utf-8') as fh:
        json.dump({'entries': entries}, fh)
    for args in (('add', '-A'), ('commit', '-q', '-m', 'fixture')):
        subprocess.run(['git', '-C', d, '-c', 'user.name=t', '-c', 'user.email=t@t', *args],
                       capture_output=True)
    rev = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    if not rev:
        raise RuntimeError('fixture lane has no commit')
    return d, rev


def _xT47HardFreshLiveA_run(lane, rev, body, rc):
    """Run live() with a stub curl first on PATH; returns (returncode, captured stdout)."""
    import contextlib
    buf = io.StringIO()
    with tempfile.TemporaryDirectory(prefix='t47-freshlive-bin-') as bin_dir:
        exe = os.path.join(bin_dir, 'curl')
        with open(exe, 'w', encoding='utf-8') as fh:
            fh.write(_xT47HardFreshLiveA_STUB)
        os.chmod(exe, 0o755)
        bodyfile = os.path.join(bin_dir, 'body')
        with open(bodyfile, 'wb') as fh:
            fh.write(body or b'')
        saved = dict(os.environ)
        os.environ['PATH'] = bin_dir + os.pathsep + saved.get('PATH', '')
        os.environ['X47LIVE_BODY'] = bodyfile if body is not None else ''
        os.environ['X47LIVE_RC'] = str(rc)
        try:
            with contextlib.redirect_stdout(buf):
                code = live(lane, rev)
        finally:
            os.environ.clear()
            os.environ.update(saved)
    return code, buf.getvalue()


def _xT47HardFreshLiveA_summary(out):
    m = re.search(r'^C1_R45_LIVE: present=(\d+) absent=(\d+) ', out, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else None


def _xT47HardFreshLiveA_probe(entries, body, rc, want, want_live, want_code=0):
    """Run one fixture lane through live(); returns (ok, detail)."""
    import shutil
    d = None
    try:
        d, rev = _xT47HardFreshLiveA_lane(entries)
        code, out = _xT47HardFreshLiveA_run(d, rev, body, rc)
        got = _xT47HardFreshLiveA_summary(out)
        lines = [l for l in out.splitlines() if l.startswith('LIVE ')]
        ok = got == want and code == want_code and lines == want_live
        detail = 'summary=%s rc=%d live=%s' % (got, code, lines)
    except Exception as exc:
        ok = False
        detail = 'raised %s' % type(exc).__name__
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
    return ok, detail


def extra_T47HardFreshLiveA():
    """Cases L01-L04: the live() re-fetch rules, driven by a stub curl and a fixture lane."""
    holds = dict(id='S001', url='https://e.org/x', verdict='holds', quote=_xT47HardFreshLiveA_QUOTE)
    page = _xT47HardFreshLiveA_PAGE
    cases = [
        ('L01_live_fetch_present', [dict(holds)], page, 0, (1, 0), ['LIVE S001 present']),
        ('L02_live_fetch_error_absent', [dict(holds)], b'ignored\n', 22, (0, 1), ['LIVE S001 absent']),
        ('L03_live_non_holds_skipped', [dict(holds, verdict='drifted')], page, 0, (0, 0), []),
        ('L04_live_unreadable_target_absent', [dict(holds)], None, 0, (0, 1), ['LIVE S001 absent']),
    ]
    failed = 0
    for name, entries, body, rc, want, want_live in cases:
        ok, detail = _xT47HardFreshLiveA_probe(entries, body, rc, want, want_live)
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    return len(cases), failed


# --- T47HardFreshLiveB: selftest cases for six live() pool survivors of the round-46
# hardened freshness counter (live:cmp:1, live:cmp:2, live:int:2, live:const:1, live:cmp:3,
# live:const:2).  live() is never called from the round-46 selftest, so every case builds a
# scratch git lane (corpus/SOURCES.md + the round-45 ledger) and puts a stub `curl` first on
# PATH: no case touches the network, none reads the counter's own bytes, and the stub never
# writes outside the scratch directory.
#
# One fixture, one population (S001, S002, S004, S005 mined; S003 queued) and five entries:
#   S001 holds, in population, page HAS the quote, curl exits 0   -> present
#   S002 holds, in population, page LACKS the quote, curl exits 0 -> absent
#   S003 holds, NOT in population (queued row), page has quote    -> skipped by the gate
#   S004 drifted, in population, page has the quote               -> skipped by the gate
#   S005 holds, in population, page has the quote, curl exits 1   -> absent
#
# Separations (original value vs mutant value on the same input):
#   live:cmp:1   `verdict != 'holds'` -> `==`: S004 (drifted) is measured and the three
#                holdings rows are skipped, so the LIVE line set becomes {S004}.
#   live:cmp:2   `id not in pop` -> `in`: S003 (unregistered) is measured and every registered
#                row is skipped, so S003 appears in the output.
#   live:int:2   `res.returncode == 0` -> `== 1`: S001 (exit 0) drops to absent and S005
#                (exit 1, page on disk) turns present.
#   live:const:1 `capture_output=True` -> False: curl's own stdout leaks into the counter's
#                stdout; the stub marker is absent when the call captures, present when not.
#   live:cmp:3   quote `in` -> `not in`: S001 flips present->absent, S002 flips absent->present.
#   live:const:2 except-branch `present = False` -> True: a download that wrote no file makes
#                open() raise; the original reports absent, the mutant reports present.


def _xT47HardFreshLiveB_pages():
    return (b'<html><body><p>alpha present quote and beta marker</p></body></html>',
            b'<html><body><p>gamma unrelated sentence only</p></body></html>')


def _xT47HardFreshLiveB_stub(binp):
    """Write the executable `curl` the fixture puts first on PATH."""
    good, other = _xT47HardFreshLiveB_pages()
    script = '\n'.join([
        '#!' + sys.executable,
        'import os',
        'import sys',
        'args = sys.argv[1:]',
        'out = args[args.index("-o") + 1] if "-o" in args else ""',
        'url = args[-1]',
        'sys.stdout.write("CURL_STUB_STDOUT_MARKER\\n")',
        'sys.stdout.flush()',
        'if os.environ.get("T47FSLB_MODE") == "nofile":',
        '    sys.exit(0)',
        'page = %r' % good,
        'status = 0',
        'if url.endswith("/absent"):',
        '    page = %r' % other,
        'elif url.endswith("/error"):',
        '    status = 1',
        'if out:',
        '    fh = open(out, "wb")',
        '    fh.write(page)',
        '    fh.close()',
        'sys.exit(status)',
        ''])
    path = os.path.join(binp, 'curl')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(script)
    os.chmod(path, 0o755)


def _xT47HardFreshLiveB_row(rid, slug, status):
    # 11 pipe cells: id | source | docs | A | scope | anchor | teaches | status | opened | ttl | x
    return ('| %s | doc %s - http://fleet.invalid/%s | docs | A | mutants detected | section | '
            'valid | %s | 2026-10-25 | 180d | p |\n' % (rid, rid.lower(), slug, status))


def _xT47HardFreshLiveB_entries():
    quote = 'alpha present quote'
    absent = 'alpha missing quote'
    return [
        dict(id='S001', url='http://fleet.invalid/present', verdict='holds', quote=quote),
        dict(id='S002', url='http://fleet.invalid/absent', verdict='holds', quote=absent),
        dict(id='S003', url='http://fleet.invalid/present', verdict='holds', quote=quote),
        dict(id='S004', url='http://fleet.invalid/present', verdict='drifted', quote=quote),
        dict(id='S005', url='http://fleet.invalid/error', verdict='holds', quote=quote),
    ]


def _xT47HardFreshLiveB_lane(work):
    d = os.path.realpath(os.path.join(work, 'lane'))
    os.makedirs(d)
    _xHardMeasure_git(d, 'init', '-q', '-b', 'm')
    top = _xHardMeasure_git(d, 'rev-parse', '--show-toplevel').strip()
    if os.path.realpath(top) != d:
        raise RuntimeError('fixture toplevel %r != scratch dir %r' % (top, d))
    files = {
        'corpus/SOURCES.md': ''.join([
            _xT47HardFreshLiveB_row('S001', 'present', 'mined'),
            _xT47HardFreshLiveB_row('S002', 'absent', 'mined'),
            _xT47HardFreshLiveB_row('S003', 'present', 'queued'),
            _xT47HardFreshLiveB_row('S004', 'present', 'mined'),
            _xT47HardFreshLiveB_row('S005', 'error', 'mined')]),
        LEDGER: json.dumps({'entries': _xT47HardFreshLiveB_entries()}),
    }
    for rel, text in files.items():
        full = os.path.join(d, rel)
        if os.path.dirname(full):
            os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(text)
    _xHardMeasure_git(d, 'add', '-A')
    _xHardMeasure_git(d, 'commit', '-q', '-m', 'fixture')
    return d


def _xT47HardFreshLiveB_env(binp):
    """Put the stub first on PATH and isolate git; return the environment to restore."""
    saved = dict(os.environ)
    for key in [k for k in os.environ if k.startswith('GIT_')]:
        del os.environ[key]
    os.environ['GIT_CONFIG_GLOBAL'] = '/dev/null'
    os.environ['GIT_CONFIG_SYSTEM'] = '/dev/null'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.environ['PATH'] = binp + os.pathsep + saved.get('PATH', '')
    os.environ.pop('T47FSLB_MODE', None)
    return saved


def _xT47HardFreshLiveB_restore(saved):
    os.environ.clear()
    os.environ.update(saved)


def _xT47HardFreshLiveB_run(lane, mode):
    """Call live() in-process with its prints captured; `mode` selects the stub behaviour."""
    saved_mode = os.environ.get('T47FSLB_MODE')
    if mode:
        os.environ['T47FSLB_MODE'] = mode
    else:
        os.environ.pop('T47FSLB_MODE', None)
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        live(lane, 'm')
    finally:
        sys.stdout = old
        if saved_mode is None:
            os.environ.pop('T47FSLB_MODE', None)
        else:
            os.environ['T47FSLB_MODE'] = saved_mode
    return buf.getvalue()


def _xT47HardFreshLiveB_child(lane):
    """Run live() from a child interpreter: a non-capturing call leaks curl's stdout to it."""
    code = '\n'.join([
        'import importlib.util',
        'spec = importlib.util.spec_from_file_location("t47fslb", %r)' % os.path.abspath(__file__),
        'mod = importlib.util.module_from_spec(spec)',
        'spec.loader.exec_module(mod)',
        'mod.live(%r, "m")' % lane,
        ''])
    p = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True,
                       timeout=180, env=dict(os.environ))
    return p.returncode, p.stdout


def _xT47HardFreshLiveB_lines(out):
    return [line for line in out.splitlines() if line.startswith('LIVE ')]


def _xT47HardFreshLiveB_fields(out):
    m = re.search(r'^C1_R45_LIVE: (.*)$', out, re.M)
    return dict(re.findall(r'(\w+)=(\S+)', m.group(1))) if m else {}


def _xT47HardFreshLiveB_rmtree(path):
    import shutil
    shutil.rmtree(path, ignore_errors=True)


def extra_T47HardFreshLiveB():
    cases = []

    def check(name, ok, detail=''):
        cases.append(bool(ok))
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))

    work = tempfile.mkdtemp(prefix='tameshi-r47-fslb-work-')
    saved = None
    try:
        binp = os.path.join(work, 'bin')
        os.makedirs(binp)
        _xT47HardFreshLiveB_stub(binp)
        saved = _xT47HardFreshLiveB_env(binp)
        lane = _xT47HardFreshLiveB_lane(work)

        want = ['LIVE S001 present', 'LIVE S002 absent', 'LIVE S005 absent']
        out = _xT47HardFreshLiveB_run(lane, None)
        lines = _xT47HardFreshLiveB_lines(out)
        fields = _xT47HardFreshLiveB_fields(out)
        detail = '%r %r' % (lines, fields)

        # live:cmp:1 -- the verdict gate skips a `drifted` entry that is in the population.
        check('T47FSLB01_live_holds_verdict_gate', lines == want, detail)
        # live:cmp:2 -- the membership gate skips a `holds` entry that is not in the population.
        check('T47FSLB02_live_population_gate',
              lines == want and 'LIVE S003' not in out, detail)
        # live:int:2 -- exit 0 means "downloaded"; exit 1 means "do not read the target".
        check('T47FSLB03_live_returncode_gate',
              lines == want and fields.get('present') == '1' and fields.get('absent') == '2',
              detail)
        # live:cmp:3 -- a quote present in the page is reported present, not the reverse.
        check('T47FSLB04_live_quote_presence', lines == want, detail)

        # live:const:1 -- curl's own stdout is captured by the call, not inherited.
        rc, child_out = _xT47HardFreshLiveB_child(lane)
        check('T47FSLB05_live_captures_child_stdout',
              rc == 0 and 'CURL_STUB_STDOUT_MARKER' not in child_out
              and 'LIVE ' in child_out,
              'rc=%d marker=%s live=%s' % (rc, 'CURL_STUB_STDOUT_MARKER' in child_out,
                                          'LIVE ' in child_out))

        # live:const:2 -- a target that cannot be read is absent, not present.
        nofile = _xT47HardFreshLiveB_run(lane, 'nofile')
        nlines = _xT47HardFreshLiveB_lines(nofile)
        nfields = _xT47HardFreshLiveB_fields(nofile)
        check('T47FSLB06_live_unreadable_is_absent',
              nlines == ['LIVE S001 absent', 'LIVE S002 absent', 'LIVE S005 absent']
              and nfields.get('present') == '0' and nfields.get('absent') == '3',
              '%r %r' % (nlines, nfields))
    except Exception as exc:
        check('T47FSLB00_fixture_ran', False, 'raised %s: %s' % (type(exc).__name__, exc))
    finally:
        if saved is not None:
            _xT47HardFreshLiveB_restore(saved)
        _xT47HardFreshLiveB_rmtree(work)
    return len(cases), cases.count(False)


"""Round-47 C2 seat T47HardFreshMeasure: measure()-level cases for the round-45 freshness counter.

Three cases, each the smallest scratch-repo fixture that separates the pristine
measure() from one declared round-47 pool mutant of group `freshness`:

  F20_invalid_reason_routing   measure:cmp:2   `if state == 'invalid':` -> `!=`
      One population row with a verified entry (S001) and one with a mismatched
      URL (S002, `url mismatch`).  The reason loop must name exactly S002 on an
      `INVALID` line.  With the operator flipped the loop appends a reason for
      the verified row instead ('S001 ok') and drops the genuine invalid reason,
      so the printed INVALID id set becomes ['S001'].

  F21_empty_population_score   measure:int:0   the `else 0` of the score formula -> 1
      SOURCES.md with no population rows and an empty ledger: the summary must
      report score=0.  With the mutated constant the empty-population branch
      reports score=1.

  F22_target_equality_passes   measure:cmp:4   (`fresh >= TARGET` -> `>`)
                               measure:int:5   (`self_pin == 1` -> `self_pin == 2`)
                               measure:int:1   (`return 0 if passed else 1` -> always 1)
      TARGET valid+agreed rows with the counter bytes pinned at SELF_PATH, so
      fresh equals TARGET exactly: the declared floor must admit that boundary
      (PASS, exit 0), the self pin must read 1, and a passing measurement must
      exit 0.

Every case reuses the round-46 HardMeasure scratch-repo builders read-only and
prints `PASS <case> ...` / `FAIL <case> ...`; no case reads or pins the
counter's source bytes, and none of them fails for a behaviour-equal neutral
(commute) mutant.
"""


def _xT47HardFreshMeasure_invalid_ids(out):
    return sorted(set(re.findall(r'^INVALID (\S+)', out, re.M)))


def _xT47HardFreshMeasure_case(name, files, pin_self, want, want_rc, invalid_ids):
    """Run one fixture; check summary fields, exit code and the INVALID id set."""
    try:
        with tempfile.TemporaryDirectory(prefix='tameshi-r47-hardfresh-') as d:
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
    if invalid_ids is not None:
        got = _xT47HardFreshMeasure_invalid_ids(out)
        if got != list(invalid_ids):
            bad.append('INVALID ids=%s want=%s' % (got, list(invalid_ids)))
    if bad:
        tail = (' stderr=' + err.strip().splitlines()[-1]) if err.strip() else ''
        print('FAIL %s %s%s' % (name, ' '.join(bad), tail))
        return 0
    print('PASS %s' % name)
    return 1


def extra_T47HardFreshMeasure():
    cases = failed = 0

    # F20: INVALID lines must be routed by the graded state, not its complement.
    sha2 = _xHardMeasure_sha(2)
    files, _ = _xHardMeasure_fixture(
        2,
        [_xHardMeasure_entry(1, sha2),
         dict(_xHardMeasure_entry(2, sha2), url='https://e.org/other')],
        [])
    cases += 1
    failed += not _xT47HardFreshMeasure_case(
        'F20_invalid_reason_routing', files, False,
        {'population': '2', 'entries': '2', 'verified': '1', 'invalid': '1',
         'fresh': '0', 'score': '0', 'C1_R45_PASS': 'false'}, 1, ['S002'])

    # F21: with no population the score formula's else branch must stay 0.
    files, _ = _xHardMeasure_fixture(0, [], [])
    cases += 1
    failed += not _xT47HardFreshMeasure_case(
        'F21_empty_population_score', files, False,
        {'population': '0', 'entries': '0', 'verified': '0', 'fresh': '0',
         'score': '0', 'C1_R45_PASS': 'false'}, 1, [])

    # F22: fresh == TARGET exactly, self_pin=1, must PASS and exit 0.
    n = TARGET
    files, _ = _xHardMeasure_fixture(
        n, [_xHardMeasure_entry(i, _xHardMeasure_sha(n)) for i in range(1, n + 1)],
        [_xHardMeasure_review('S%03d' % i, 'RevX', 'agree') for i in range(1, n + 1)])
    cases += 1
    failed += not _xT47HardFreshMeasure_case(
        'F22_target_equality_passes', files, True,
        {'self_pin': '1', 'population': str(n), 'entries': str(n), 'verified': str(n),
         'fresh': str(n), 'score': '10', 'target': str(n), 'C1_R45_PASS': 'true'}, 0, [])

    return cases, failed


"""Round-47 C2 seat T47HardFreshParse: named cases for the parse_rows() cell indexes.

parse_rows() (round-46 hardened freshness counter) turns one 13-cell registry line
into ``{id: dict(id, source, scope, anchor, teaches, status, url)}`` by indexing the
`|`-split cells: id=1, source=2, scope=5, anchor=6, teaches=7, status=8, and
`url=URL_RE.search(cells[2]).group(0)`. The six cases here pin the six dimensions this
seat owns (id, source, scope, anchor, teaches, url) with ONE fixture row whose cells are
all distinguishable, so each mutant is separated by a field value and not by a crash.

Why an import-time tripwire is part of the file
-----------------------------------------------
The round-46 selftest feeds parse_rows() its first registry fixture inside selftest()
itself (the T15 block: `rows = parse_rows(...)` then `pop = sorted(population(rows))`),
i.e. BEFORE any `extra_*()` runs -- the assembler appends the extra calls only before
the tally print. Two of the mutants owned here make that pristine call site raise:

  * parse_rows:int:1 (`rid = cells[1]` -> cells[2]) keys the dict by the source cell, so
    population()'s `int(rid[1:])` raises ValueError; the run is `crashed`, and no
    `FAIL ` line would ever be printed by a case that runs later.
  * parse_rows:int:8 (`url.group(0)` -> group(1)) asks the group-less URL_RE for group 1,
    raising IndexError at the same call site; again `crashed`.

The pool counts a kill only on a named `FAIL ` line, so those two dimensions can only be
killed by a named case that runs before selftest() reaches that call site. The tripwire
below is that early case: it evaluates exactly the same behavioural fixture and the same
field comparison as extra_T47HardFreshParse(), prints nothing when every case holds, and
runs only under `--selftest`, so the pristine counter and the --lane/--check/--live modes
print no additional bytes. It never reads the counter's own source, so the neutral
mutants and CTL_E are unaffected.
"""

# Cell layout of the fixture line (index -> meaning), for the reader:
#   0 '' | 1 id | 2 source | 3 docs | 4 A | 5 scope | 6 anchor | 7 teaches |
#   8 status | 9 opened | 10 ttl | 11 p | 12 ''
_XT47TEXT = ('| S100 | srcT47 \u2014 https://e.org/t47 | docs | A | scopeT47 | anchorT47 | '
             'teachesT47 | mined | 2026-10-25 | 180d | p |\n')

# (case name, dict field, expected value, mutant address this case separates)
_XT47CASES = (
    ('R47F01_parse_rows_id_is_cell_1', 'id', 'S100', 'parse_rows:int:1'),
    ('R47F02_parse_rows_source_is_cell_2', 'source', 'srcT47 \u2014 https://e.org/t47',
     'parse_rows:int:3'),
    ('R47F03_parse_rows_scope_is_cell_5', 'scope', 'scopeT47', 'parse_rows:int:4'),
    ('R47F04_parse_rows_anchor_is_cell_6', 'anchor', 'anchorT47', 'parse_rows:int:5'),
    ('R47F05_parse_rows_teaches_is_cell_7', 'teaches', 'teachesT47', 'parse_rows:int:6'),
    ('R47F06_parse_rows_url_is_full_match', 'url', 'https://e.org/t47', 'parse_rows:int:8'),
)


def _xT47HardFreshParse_parse():
    """parse_rows() on the fixture line; (rows, None) or ({}, 'ExcName: message')."""
    try:
        return parse_rows(_XT47TEXT), None
    except Exception as exc:  # a mutated index that raises must still yield a named FAIL
        return {}, '%s: %s' % (type(exc).__name__, exc)


def _xT47HardFreshParse_check(field, want):
    """(ok, detail) for one field of the S100 row; a different key or a raise is a miss."""
    rows, err = _xT47HardFreshParse_parse()
    if err:
        return False, 'raised %s' % err
    row = rows.get('S100')
    if row is None:
        return False, 'keys=%s' % sorted(rows)
    got = row.get(field)
    return got == want, '%s=%r' % (field, got)


def _xT47HardFreshParse_run():
    """Yield (case name, ok, detail, mutant address) for every case."""
    for name, field, want, mid in _XT47CASES:
        ok, detail = _xT47HardFreshParse_check(field, want)
        yield name, ok, detail, mid


def _xT47HardFreshParse_tripwire():
    """Pre-selftest named case for the two mutants whose crash precedes every extra_*()."""
    if '--selftest' not in sys.argv:
        return 0
    bad = 0
    for name, ok, detail, mid in _xT47HardFreshParse_run():
        if not ok:
            bad += 1
            print('FAIL %s early %s (%s)' % (name, detail, mid))
    return bad


_XT47EARLY = _xT47HardFreshParse_tripwire()


def extra_T47HardFreshParse():
    """Return (cases, failed): one field-pinning case per parse_rows cell index."""
    cases = failed = 0
    for name, ok, detail, mid in _xT47HardFreshParse_run():
        cases += 1
        failed += not ok
        print('%s %s %s (%s)' % ('PASS' if ok else 'FAIL', name, detail, mid))
    return cases, failed


"""Round-47 C2 seat T47HardFreshText: named cases for extract(), words(), grade() and review_sets().

Five rule-level cases (FT01-FT05) plus two review cases (FT06-FT07), each the smallest
behavioural fixture that separates the pristine round-46 hardened freshness counter from a
mutant this seat owns. No case reads the counter's own source, hashes it or pins a length, so
the neutral (commute) mutants and CTL_E are untouched.

  FT01 extract:PDF branch      a raw blob that starts with %PDF must go through pdftotext.
                               `raw[:4]` -> `raw[:5]` (extract:int:0) skips the branch and
                               decodes the PDF bytes, so the extracted text disappears and
                               `%PDF` shows up; `capture_output=True` -> `False`
                               (extract:const:0) leaves `out.stdout` None and the call raises
                               AttributeError, which this case reports as a named FAIL.
                               pdftotext is a PATH-first shell stub printing one fixed line
                               (the brief's fake-curl pattern): no PDF tool, no network.
  FT02 words stop-word filter   `and` -> `or` (words:bool:0) keeps short words and stopwords.
  FT03 words minimum length 4   `>=` -> `>` (words:cmp:0) and `4` -> `5` (words:int:0) drop a
                               4-letter content word; pristine keeps it.
  FT04 grade overlap floor 2    a 6..25-token quote present in the page with EXACTLY 2 content
                               words shared with scope+anchor+teaches: `< 2` -> `<= 2`
                               (grade:cmp:9) and `2` -> `3` (grade:int:0) both refuse it.
  FT05 grade quote upper 25     a 25-token quote (the bound itself) must be admitted;
                               `n > 25` -> `n >= 25` (grade:cmp:11) refuses it as length 25.
  FT06/FT07 review_sets gates   FT06: an independent agree whose report names id and reviewer
                               is admitted (the `not text` deletion, review_sets:not:2, makes
                               every non-empty report skip, so nothing is admitted).
                               FT07: a report naming the id but NOT the reviewer is refused
                               (`or` -> `and` on line 209, review_sets:bool:1, admits it).

Why an import-time tripwire covers FT06/FT07 only
-------------------------------------------------
The round-46 selftest calls review_sets() inside selftest() itself (the T17 block), before any
`extra_*()` -- the assembler appends the extra calls only before the tally print. Both mutants
above make that T17 call site raise (T17 feeds a review whose report is absent, so `text` is
None; `not text` is then evaluated against `re.search(..., None)`), so the run ends as a
traceback with no named FAIL and a later case could never report them. The tripwire below runs
the same two fixtures at import time, prints ONLY named `FAIL` lines (nothing when both hold),
and does nothing outside `--selftest`, so the pristine counter and the --lane/--check/--live
modes print no additional bytes. FT01-FT05 need no tripwire: their mutants do not raise in any
earlier selftest case.
"""

import shutil

_PDF_RAW = (b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\n'
            b'endobj\ntrailer\n<< /Root 1 0 R >>\nstartxref\n0\n%%EOF\n')
_PDF_TEXT = 'Portable document marker sentence inside the extracted body'

# 11 tokens, present in _PAGE_OVERLAP2, sharing exactly {flaky, cluster} with _xHardGrade_row().
_QUOTE_OVERLAP2 = 'Ordering hides flaky runs while the cluster appears only after reruns'
_PAGE_OVERLAP2 = ('<html><body><p>' + _QUOTE_OVERLAP2 + '.</p></body></html>').encode('utf-8')

# 25 whitespace tokens (the upper bound itself), verbatim inside _xHardGrade_page().
_QUOTE_25 = ('Flaky failures cluster inside the same job because the rerun repeats one order of '
             'the tests only and the second attempt hides the ordering defect')

_REVIEW_REPORT = '.ufo/waves/round-45/w2/T47Text.md'
_REVIEW_CTL = '.ufo/waves/round-45/w2/T47TextCtl.md'


def _xT47HardFreshText_pdf_dir():
    """A PATH-first `pdftotext` stub that prints _PDF_TEXT and ignores its arguments."""
    d = tempfile.mkdtemp(prefix='tameshi-r47-t47text-')
    p = os.path.join(d, 'pdftotext')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write("#!/bin/sh\nprintf '%s\\n' '" + _PDF_TEXT + "'\n")
    os.chmod(p, 0o755)
    return d


def _xT47HardFreshText_extract_pdf():
    """(ok, detail): the PDF branch must return pdftotext's text, not the decoded raw bytes."""
    d = _xT47HardFreshText_pdf_dir()
    saved = os.environ.get('PATH', '')
    os.environ['PATH'] = d + (os.pathsep + saved if saved else '')
    try:
        try:
            got = extract(_PDF_RAW)
        except Exception as exc:  # capture_output=False -> out.stdout is None -> AttributeError
            got = '<raised %s>' % type(exc).__name__
    finally:
        os.environ['PATH'] = saved
        shutil.rmtree(d, ignore_errors=True)
    ok = _PDF_TEXT in got and '%PDF' not in got
    return ok, 'text=%r' % (got[:60],)


def _xT47HardFreshText_entry(quote, raw):
    row = _xHardGrade_row()
    return dict(id=row['id'], url=row['url'], opened='2026-10-25', verdict='holds',
                raw_sha256=hashlib.sha256(raw).hexdigest(), quote=quote)


def _xT47HardFreshText_grade_cases():
    """(name, ok, detail) for the two grade() thresholds: overlap floor 2, quote length 25."""
    row = _xHardGrade_row()
    out = []
    got = grade(_xT47HardFreshText_entry(_QUOTE_OVERLAP2, _PAGE_OVERLAP2), row, _PAGE_OVERLAP2)
    out.append(('FT04_grade_overlap_two_admitted', got == ('verified', 'ok'), '%r' % (got,)))
    page = _xHardGrade_page()
    got = grade(_xT47HardFreshText_entry(_QUOTE_25, page), row, page)
    out.append(('FT05_grade_quote_25_admitted', got == ('verified', 'ok'), '%r' % (got,)))
    return out


def _xT47HardFreshText_words_cases():
    """(name, ok, detail): the stop-word filter and the length-4 floor of words()."""
    out = []
    got = sorted(words('that alpha'))
    out.append(('FT02_words_stopword_excluded', got == ['alpha'], '%r' % (got,)))
    got = sorted(words('quad alpha'))
    out.append(('FT03_words_min_length_four', got == ['alpha', 'quad'], '%r' % (got,)))
    return out


def _xT47HardFreshText_review_run():
    """(name, ok, detail) for the two report-text gates of review_sets().

    One refused review (report names the id, not the reviewer) and one admitted control
    (report names both), so a gate that stops counting everything fails FT06 too.
    """
    seats = wave_seats(json.dumps({'results': [
        {'name': 'RevT47', 'output': 'done'}, {'name': 'RevT47Ctl', 'output': 'done'}]}))
    authors = {'S001': 'ExecT47', 'S002': 'ExecT47'}
    reports = {_REVIEW_REPORT: 'S001 was re-checked against the ledger by an independent seat',
               _REVIEW_CTL: 'RevT47Ctl re-checked S002 and agrees'}
    reviews = [dict(id='S001', reviewer='RevT47', verdict='agree', report=_REVIEW_REPORT),
               dict(id='S002', reviewer='RevT47Ctl', verdict='agree', report=_REVIEW_CTL)]
    agreed, disputed = review_sets({'S001', 'S002'}, reviews, authors, reports.get, seats)
    out = [('FT06_review_control_admitted', 'S002' in agreed and not disputed, 'agreed=%s' % sorted(agreed)),
           ('FT07_review_report_names_reviewer', 'S001' not in agreed, 'agreed=%s' % sorted(agreed))]
    return out


def _xT47HardFreshText_run():
    """(name, ok, detail) for every case, in a stable order."""
    ok, detail = _xT47HardFreshText_extract_pdf()
    out = [('FT01_extract_pdf_branch', ok, detail)]
    out += _xT47HardFreshText_words_cases()
    out += _xT47HardFreshText_grade_cases()
    out += _xT47HardFreshText_review_run()
    return out


def _xT47HardFreshText_tripwire():
    """Pre-selftest named case for the two review_sets() mutants whose crash precedes every extra_*()."""
    if '--selftest' not in sys.argv:
        return 0
    try:
        results = _xT47HardFreshText_review_run()
    except Exception:
        return 0
    bad = 0
    for name, ok, detail in results:
        if not ok:
            bad += 1
            print('FAIL %s early %s' % (name, detail))
    return bad


_XT47HardFreshText_EARLY = _xT47HardFreshText_tripwire()


def extra_T47HardFreshText():
    """Return (cases, failed): the extract/words/grade/review_sets cases of this seat."""
    cases = failed = 0
    for name, ok, detail in _xT47HardFreshText_run():
        cases += 1
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
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
