#!/usr/bin/env python3
"""Round-48 C2 (freshness) counter: four held registry rows re-anchored live.

Frozen predicate (one sentence, as in the contract, this docstring and the receipt label):
  C2_R48_PASS=true iff self_pin=1 targets=4 refreshed=4 census_exit=0 — where at REV each
  target T in {S026, S048, S093, S108} carries exactly one new registry row R (id above
  S264) whose teaches cell opens `supersedes T —` (U+2014 exactly), opened 2026-10-26,
  status mined, whose https-URL set (the URLs of its source and anchor cells, amendment 1)
  holds T's base URL and the fetch-receipt URL, a committed snapshot
  .ufo/evidence/round-48/freshness/sources/T.* whose sha256 first 12 hex stand in R's
  anchor cell, a committed receipt T.receipt.json agreeing on url (in that set), fetched_at
  2026-10-26, http_status 200 and sha256 (= the snapshot's), one Gate line
  `- C2-QUOTE R T: <quote>` in corpus/lessons/round-48.md whose whitespace-collapsed quote
  is at most 25 words, occurs in the snapshot's extracted text (amendment 2) and carries
  every required phrase of T, every knowledge entry of T's base used-by cell carrying a
  `source:` line (first 10 lines of the entry) naming R and a `verified-at:` line carrying
  2026-10-26 while R's used-by cell lists exactly that path set, and (live mode, default on)
  a fetch of the receipt URL whose extracted text still contains the quote.

Contract mapping of the fields printed per target:
  TARGET T row=<R|none> snapshot=<ok|...> receipt=<ok|...> quote=<ok|...>
           phrases=<ok|...> entries=<ok|...> live=<ok|skipped|unreachable|absent>
           <REFRESHED|NOT>
  C2_R48: self_pin=. targets=4 refreshed=N census_exit=E live=<on|off> rev=REV
           C2_R48_PASS=<bool>
  and with --no-live the last token is C2_R48_PARTIAL=<bool> — a probe, never a verdict.

Checks are graded in the printed order and stop at the first failure (later fields print
`-`), so the field that fails names the first failing check:
  row        none | ambiguous | opened | status | url            (id printed when found)
  snapshot   absent | ambiguous | unreadable | sha | gzip        (sha256 over the committed
                                                                 bytes; .gz is decomposed
                                                                 for extraction only)
  receipt    absent | json | url | fetched_at | http_status | sha | bytes
  quote      noline | line | empty | <N>w | absent
  phrases    missing
  entries    absent | source | verified-at | usedby
  live       skipped (--no-live) | absent (no receipt URL or no quote, or the quote is not
             in the fetched text) | unreachable (fetch failed) | ok

Implementation notes (no semantic change to the statement):
  * Everything is read at REV with `git -C LANE show REV:path`; BASE is the constant below
    (T's base used-by cell and base URL come from corpus/SOURCES.md at BASE).
  * Registry rows use the census line shape: 0-3 leading spaces, `| S### |`, 13 `|`-fields;
    a row with another field count is not a registry row here (the census reports it as E01
    and census_exit then fails, so skipping it cannot hide it).
  * `row=url` requires every https URL of T's source cell at BASE to be in R's URL set; each
    of the four targets carries exactly one, so this is the contract's singular "T's URL"
    for the frozen population (amendment 1 widens the set to source+anchor).
  * Snapshots: the files matching .ufo/evidence/round-48/freshness/sources/T.* other than
    T.receipt.json; exactly one is required ("the one file").
  * Gate lines: the first line in file order matching amendment 2 that names T second (R
    first) is graded; a line naming T with another first id fails `line`, no line naming T
    second fails `noline`. Extraction is amendment 2 verbatim: UTF-8 decode, drop
    <script>/<style> element contents, strip tags, html.unescape, collapse whitespace to
    one space; the quote is whitespace-collapsed and matched with no case or punctuation
    folding; word count is whitespace tokens.
  * Census: corpus/SOURCES.md at REV is written to a temp dir (under TMPDIR) as
    corpus/SOURCES.md, every blob that a used-by cell of that registry names is
    materialised at the same relative path from REV (so the census' E11 "used-by path
    missing on disk" is graded against REV, not against an empty tree), and
    `sources-census.sh validate --file <that>` is run; census_exit is its exit code (127
    when the tool is absent — never credited).

Modes: --lane L --rev R (deciding run, live by default) · --no-live (probe) · --selftest.
"""
import argparse
import gzip
import hashlib
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

sys.dont_write_bytecode = True

SELF_PATH = '.ufo/evidence/round-48/freshness/measure.py'
BASE = '473336d9d789f6081195e7376d17836a24666bc3'
TARGETS = ('S026', 'S048', 'S093', 'S108')
REQUIRED = {
    'S026': ('84%',),
    'S048': ('should therefore be prioritised',),
    'S093': ('--unshare-all', '--unshare-cgroup-try'),
    'S108': ('--update_goldens',),
}
SOURCES = 'corpus/SOURCES.md'
LESSONS = 'corpus/lessons/round-48.md'
SNAP_DIR = '.ufo/evidence/round-48/freshness/sources'
RECEIPT_SUFFIX = '.receipt.json'
CENSUS = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
MIN_NEW_ID = 264
OPENED = '2026-10-26'
STATUS = 'mined'
MAX_WORDS = 25
EMDASH = '\u2014'

ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https://[^\s|,;)\]"\']+')
GATE_RE = re.compile(r'^- C2-QUOTE (S\d{3,}) (S\d{3,}): `([^`]+)`')
ID_RE = re.compile(r'\bS\d{3,}\b')


# --------------------------------------------------------------------- plumbing ---

def git(lane, *args, binary=False):
    proc = subprocess.run(['git', '-C', lane] + list(args), capture_output=True)
    if proc.returncode != 0:
        return None
    return proc.stdout if binary else proc.stdout.decode('utf-8', 'replace')


def show_bytes(lane, rev, path):
    return git(lane, 'show', '%s:%s' % (rev, path), binary=True)


def show_text(lane, rev, path):
    raw = show_bytes(lane, rev, path)
    return None if raw is None else raw.decode('utf-8', 'replace')


def tree_paths(lane, rev, prefix):
    text = git(lane, 'ls-tree', '-r', '--name-only', rev, '--', prefix)
    return [ln for ln in (text or '').splitlines() if ln.strip()]


def urls_of(cell):
    seen, out = set(), []
    for url in URL_RE.findall(cell or ''):
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def parse_rows(text):
    """Registry rows in file order: the census line shape with 13 `|` fields."""
    rows = []
    for line in (text or '').splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.split('|')]
        if len(cells) != 13:
            continue
        rows.append(dict(id=cells[1], source=cells[2], kind=cells[3], tier=cells[4],
                         scope=cells[5], anchor=cells[6], teaches=cells[7],
                         status=cells[8], opened=cells[9], recheck=cells[10],
                         usedby=cells[11], urls=urls_of(cells[2] + ' ' + cells[6])))
    return rows


def split_usedby(cell):
    out = []
    for part in (cell or '').split(','):
        part = part.strip()
        if part and part != EMDASH:
            out.append(part)
    return out


def collapse(text):
    return ' '.join(str(text).split())


def extract(raw):
    """Amendment 2 verbatim: UTF-8 decode, drop script/style element contents, strip
    tags, unescape entities, collapse whitespace runs to one space."""
    text = raw.decode('utf-8', 'replace') if isinstance(raw, bytes) else str(raw)
    text = re.sub(r'(?is)<(script|style)\b[^>]*>.*?(?:</\1\s*>|\Z)', ' ', text)
    text = re.sub(r'(?s)<[^>]*>', ' ', text)
    text = html.unescape(text)
    return collapse(text)


def sha256_hex(raw):
    return hashlib.sha256(raw).hexdigest()


def live_fetch(url, timeout=60):
    req = urllib.request.Request(
        url, headers={'User-Agent': 'tameshi-c2-r48/1.0 (round-48 freshness counter)'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise OSError('http %s' % resp.status)
        raw = resp.read()
        if (resp.headers.get('Content-Encoding') or '').lower() == 'gzip':
            raw = gzip.decompress(raw)
    return raw


# ------------------------------------------------------------------- the checks ---

def base_context(lane, base):
    rows = parse_rows(show_text(lane, base, SOURCES) or '')
    ctx = {'base_urls': {}, 'base_used_by': {}}
    for t in TARGETS:
        rows_t = [r for r in rows if r['id'] == t]
        if not rows_t:
            ctx['base_urls'][t] = []
            ctx['base_used_by'][t] = []
            continue
        row = rows_t[-1]
        ctx['base_urls'][t] = urls_of(row['source'])
        ctx['base_used_by'][t] = split_usedby(row['usedby'])
    return ctx


def check_row(t, ctx, rows):
    prefix = 'supersedes %s %s' % (t, EMDASH)
    cands = [r for r in rows
             if r['teaches'].startswith(prefix) and int(r['id'][1:]) > MIN_NEW_ID]
    if not cands:
        return None, 'none'
    if len(cands) > 1:
        return None, 'ambiguous'
    row = cands[0]
    if row['opened'] != OPENED:
        return row, 'opened'
    if row['status'] != STATUS:
        return row, 'status'
    if not set(ctx['base_urls'][t]) <= set(row['urls']):
        return row, 'url'
    return row, 'ok'


def snapshot_files(lane, rev):
    out = {}
    for path in tree_paths(lane, rev, SNAP_DIR):
        base = path.rsplit('/', 1)[-1]
        if not re.match(r'^S\d{3,}\.[^/]+$', base) or base.endswith(RECEIPT_SUFFIX):
            continue
        out.setdefault(base.split('.', 1)[0], []).append(path)
    return out


def check_snapshot(lane, rev, t, row, snaps):
    cands = sorted(snaps.get(t, []))
    if not cands:
        return None, 'absent', None, None
    if len(cands) > 1:
        return None, 'ambiguous', None, None
    path = cands[0]
    raw = show_bytes(lane, rev, path)
    if raw is None:
        return None, 'unreadable', None, None
    digest = sha256_hex(raw)
    if digest[:12] not in row['anchor']:
        return None, 'sha', digest, None
    body = raw
    if path.endswith('.gz'):
        try:
            body = gzip.decompress(raw)
        except OSError:
            return None, 'gzip', digest, None
    return (path, raw), 'ok', digest, extract(body)


def check_receipt(lane, rev, t, row, digest):
    path = '%s/%s%s' % (SNAP_DIR, t, RECEIPT_SUFFIX)
    raw = show_bytes(lane, rev, path)
    if raw is None:
        return None, 'absent'
    try:
        data = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        return None, 'json'
    if not isinstance(data, dict):
        return None, 'json'
    if str(data.get('url', '')) not in set(row['urls']):
        return data, 'url'
    if not str(data.get('fetched_at', '')).startswith(OPENED):
        return data, 'fetched_at'
    if str(data.get('http_status')) != '200':
        return data, 'http_status'
    if str(data.get('sha256', '')) != digest:
        return data, 'sha'
    if 'bytes' not in data:
        return data, 'bytes'
    return data, 'ok'


def gate_lines(lane, rev):
    text = show_text(lane, rev, LESSONS) or ''
    return [m.groups() for m in (GATE_RE.match(ln) for ln in text.splitlines()) if m]


def check_quote(gates, t, row, snap_text):
    mine = [g for g in gates if g[1] == t]
    if not mine:
        return None, 'noline'
    match = [g for g in mine if g[0] == row['id']]
    if not match:
        return None, 'line'
    quote = collapse(match[0][2])
    words = len(quote.split())
    if words == 0:
        return quote, 'empty'
    if words > MAX_WORDS:
        return quote, '%dw' % words
    if not snap_text or quote not in snap_text:
        return quote, 'absent'
    return quote, 'ok'


def check_phrases(t, quote):
    text = collapse(quote or '')
    for phrase in REQUIRED[t]:
        if collapse(phrase) not in text:
            return 'missing'
    return 'ok'


def check_entries(lane, rev, t, ctx, row):
    want = ctx['base_used_by'][t]
    for path in want:
        raw = show_bytes(lane, rev, path)
        if raw is None:
            return 'absent'
        lines = raw.decode('utf-8', 'replace').splitlines()
        source = next((ln for ln in lines[:10] if ln.strip().startswith('source:')), None)
        if source is None or row['id'] not in ID_RE.findall(source):
            return 'source'
        verified = next((ln for ln in lines if ln.strip().startswith('verified-at:')), None)
        if verified is None or OPENED not in verified:
            return 'verified-at'
    if set(split_usedby(row['usedby'])) != set(want):
        return 'usedby'
    return 'ok'


def check_live(live_on, receipt, quote, fetch, cache):
    if not live_on:
        return 'skipped'
    url = str(receipt.get('url', '')) if isinstance(receipt, dict) else ''
    if not url or not quote:
        return 'absent'
    if url not in cache:
        try:
            cache[url] = ('raw', fetch(url))
        except Exception:  # network, TLS, HTTP status, timeout
            cache[url] = ('unreachable', None)
    state, raw = cache[url]
    if state == 'unreachable' or not raw:
        return 'unreachable'
    return 'ok' if quote in extract(raw) else 'absent'


# ------------------------------------------------------------------ the census ---

def _materialise(lane, rev, text, dest):
    """Write SOURCES.md and every used-by blob it names, so the census' on-disk E11 check
    is graded against REV."""
    corpus = os.path.join(dest, 'corpus')
    os.makedirs(corpus, exist_ok=True)
    with open(os.path.join(corpus, 'SOURCES.md'), 'w', encoding='utf-8') as handle:
        handle.write(text)
    seen = set()
    for row in parse_rows(text):
        for path in split_usedby(row['usedby']):
            if path in seen or path.startswith('/') or '..' in path.split('/'):
                continue
            seen.add(path)
            if (git(lane, 'cat-file', '-t', '%s:%s' % (rev, path)) or '').strip() != 'blob':
                continue
            raw = show_bytes(lane, rev, path)
            if raw is None:
                continue
            target = os.path.join(dest, path)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'wb') as handle:
                handle.write(raw)


def census_exit(lane, rev):
    if not os.path.isfile(CENSUS):
        return 127
    work = tempfile.mkdtemp(prefix='c2-r48-census-')
    try:
        text = show_text(lane, rev, SOURCES)
        if text is None:
            return 2  # no registry at REV: the census' own "missing registry" exit
        _materialise(lane, rev, text, work)
        proc = subprocess.run(['bash', CENSUS, 'validate', '--file',
                               os.path.join(work, 'corpus', 'SOURCES.md')],
                              capture_output=True, timeout=900)
        return proc.returncode
    finally:
        shutil.rmtree(work, ignore_errors=True)


# -------------------------------------------------------------------- the measure ---

def measure(lane, rev, base=BASE, live=True, fetch=live_fetch, out=None):
    out = out or sys.stdout
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = show_bytes(lane, rev, SELF_PATH)
    self_pin = int(blob is not None and sha256_hex(blob) == sha256_hex(me))

    ctx = base_context(lane, base)
    rows = parse_rows(show_text(lane, rev, SOURCES) or '')
    snaps = snapshot_files(lane, rev)
    gates = gate_lines(lane, rev)
    cache = {}

    refreshed = 0
    lines = {}
    for t in TARGETS:
        row, row_state = check_row(t, ctx, rows)
        receipt = quote = None
        fields = {'row': row['id'] if row_state == 'ok' else row_state,
                  'snapshot': '-', 'receipt': '-', 'quote': '-', 'phrases': '-',
                  'entries': '-', 'live': 'skipped' if not live else 'absent'}
        if row is not None and row_state == 'ok':
            _, snap_state, digest, snap_text = check_snapshot(lane, rev, t, row, snaps)
            fields['snapshot'] = snap_state
            if snap_state == 'ok':
                receipt, receipt_state = check_receipt(lane, rev, t, row, digest)
                fields['receipt'] = receipt_state
                quote, quote_state = check_quote(gates, t, row, snap_text)
                fields['quote'] = quote_state
                if quote_state == 'ok':
                    fields['phrases'] = check_phrases(t, quote)
                fields['entries'] = check_entries(lane, rev, t, ctx, row)
        if live:
            fields['live'] = check_live(live, receipt, quote, fetch, cache)

        ok = (fields['row'].startswith('S') and fields['snapshot'] == 'ok'
              and fields['receipt'] == 'ok' and fields['quote'] == 'ok'
              and fields['phrases'] == 'ok' and fields['entries'] == 'ok'
              and fields['live'] in ('ok', 'skipped'))
        if ok:
            refreshed += 1
        line = 'TARGET %s %s %s' % (
            t, ' '.join('%s=%s' % (k, fields[k]) for k in
                        ('row', 'snapshot', 'receipt', 'quote', 'phrases', 'entries', 'live')),
            'REFRESHED' if ok else 'NOT')
        lines[t] = line
        print(line, file=out)

    code = census_exit(lane, rev)
    verdict = (self_pin == 1 and len(TARGETS) == 4 and refreshed == len(TARGETS)
               and code == 0)
    if live:
        label, value = 'C2_R48_PASS', 'true' if verdict else 'false'
    else:
        label, value = 'C2_R48_PARTIAL', 'true' if verdict else 'false'
    summary = ('C2_R48: self_pin=%d targets=%d refreshed=%d census_exit=%d live=%s rev=%s '
               '%s=%s' % (self_pin, len(TARGETS), refreshed, code, 'on' if live else 'off',
                          rev, label, value))
    print(summary, file=out)
    return dict(self_pin=self_pin, targets=len(TARGETS), refreshed=refreshed,
                census_exit=code, live='on' if live else 'off', rev=rev,
                verdict=bool(verdict), label=label, summary=summary, lines=lines, out=out)


# ------------------------------------------------------------------- the selftest ---

SNAP_BODY = {
    'S026': '<html><body><p>about 84% of the transitions we observe from pass to fail '
            'involve a flaky test</p></body></html>',
    'S048': '<html><body><p>these classes should therefore be prioritised for '
            're-execution</p></body></html>',
    'S093': '<refentry><para>the --unshare-all option implies --unshare-cgroup-try</para>'
            '</refentry>',
    'S108': '<html><body><p>passing --test_arg=--update_goldens rewrites the .expected '
            'files</p></body></html>',
}
QUOTE = {
    'S026': 'about 84% of the transitions we observe from pass to fail involve a flaky test',
    'S048': 'these classes should therefore be prioritised for re-execution',
    'S093': 'the --unshare-all option implies --unshare-cgroup-try',
    'S108': 'passing --test_arg=--update_goldens rewrites the .expected files',
}
BASE_URL = {
    'S026': 'https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html',
    'S048': 'https://pitest.org/quickstart/incremental_analysis/',
    'S093': 'https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml',
    'S108': 'https://www.tensorflow.org/federated/golden_tests?hl=zh-cn',
}
NEW_ID = {'S026': 'S265', 'S048': 'S266', 'S093': 'S267', 'S108': 'S268'}
ENTRY = {'S026': 'corpus/knowledge/e026.md', 'S048': 'corpus/knowledge/e048.md',
         'S093': 'corpus/knowledge/e093.md', 'S108': 'corpus/knowledge/e108.md'}
BASE_OPENED = {'S026': '2026-10-19', 'S048': '2026-10-20', 'S093': '2026-10-23',
               'S108': '2026-10-24'}
BASE_RECHECK = {'S026': '730d', 'S048': '90d', 'S093': 'on-release', 'S108': '180d'}
TABLE_HEAD_LINES = ['| id | source | kind | tier | scope | anchor | teaches | status '
                    '| opened | recheck | used-by |',
                    '|---|---|---|---|---|---|---|---|---|---|---|']
TABLE_HEAD = '\n'.join(TABLE_HEAD_LINES) + '\n'


def fixture_base_sources():
    rows = ['| %s | fixture held row %s \u2014 %s | docs | A | fixture scope %s '
            '| fixture anchor %s | fixture teaches %s | mined | %s | %s | %s |'
            % (t, t, BASE_URL[t], t, t, t, BASE_OPENED[t], BASE_RECHECK[t], ENTRY[t])
            for t in TARGETS]
    head = ['# SOURCES \u2014 round-48 counter fixture', '', '## Registry', '']
    return '\n'.join(head + TABLE_HEAD_LINES + rows) + '\n'


def base_entry(t):
    return ('source: S264 \u2014 https://example.test/base-%s \u2014 fixture pre-round '
            'entry\nverified-at: 2026-10-19\n\n# fixture entry %s\n\nBody text.\n' % (t, t))


def default_opts():
    return dict(
        snap_name={}, snap_body={}, snap_extra=(), snap_drop=(), snap_raw={},
        receipt_url={}, receipt_fetched={}, receipt_status={}, receipt_sha={},
        receipt_drop=(), receipt_drop_key={}, receipt_raw={},
        row_missing=(), row_dash=(), row_dup=(), teaches={}, row_url={}, anchor_sha={},
        row_status={}, row_opened={}, row_usedby={}, extra_rows=[],
        quote={}, gate_order=(), gate_bad_prefix=(), gate_wrong_first=(),
        gate_extra=[], lessons_extra='',
        entry={}, entry_drop=(), counter=True, counter_bytes=None, fetch='ok',
        live_mode=True)


def fixture_tree(opts):
    """The complete file map for one selftest case."""
    snaps = {}
    for t in TARGETS:
        name = opts['snap_name'].get(t, 'fixture.html')
        body = opts['snap_body'].get(t, SNAP_BODY[t]).encode('utf-8')
        if t in opts['snap_raw']:
            raw = opts['snap_raw'][t]
        elif name.endswith('.gz'):
            raw = gzip.compress(body, mtime=0)
        else:
            raw = body
        snaps[t] = ('%s/%s.%s' % (SNAP_DIR, t, name), raw)

    rows = []
    for t in TARGETS:
        if t in opts['row_missing']:
            continue
        teach = ('supersedes %s - fixture re-open' % t if t in opts['row_dash']
                 else opts['teaches'].get(t, 'supersedes %s %s fixture re-open' % (t, EMDASH)))
        url = opts['row_url'].get(t, BASE_URL[t])
        digest = opts['anchor_sha'].get(t) or sha256_hex(snaps[t][1])[:12]
        rows.append('| %s | fixture re-anchor of %s \u2014 %s | docs | A | fixture re-open '
                    'scope %s | %s @ fetched 2026-10-26, sha256 %s | %s | %s | %s | 730d '
                    '| %s |\n'
                    % (NEW_ID[t], t, url, t, url, digest, teach,
                       opts['row_status'].get(t, STATUS),
                       opts['row_opened'].get(t, OPENED),
                       opts['row_usedby'].get(t, ENTRY[t])))
        if t in opts['row_dup']:
            rows.append('| S270 | fixture duplicate of %s \u2014 %s | docs | A | fixture '
                        'duplicate scope %s | fixture duplicate anchor %s | supersedes %s '
                        '%s second row | mined | 2026-10-26 | 730d | %s |\n'
                        % (t, url, t, t, t, EMDASH, ENTRY[t]))
    rows.extend(opts['extra_rows'])

    files = {SOURCES: fixture_base_sources().replace(TABLE_HEAD, TABLE_HEAD + ''.join(rows))}
    for t in TARGETS:
        path, raw = snaps[t]
        files[path] = raw
        if t in opts['snap_extra']:
            files['%s/%s.extra.raw' % (SNAP_DIR, t)] = b'second candidate snapshot\n'
        if t in opts['snap_drop']:
            del files[path]
        if t in opts['receipt_drop']:
            continue
        receipt_path = '%s/%s%s' % (SNAP_DIR, t, RECEIPT_SUFFIX)
        if t in opts['receipt_raw']:
            files[receipt_path] = opts['receipt_raw'][t]
            continue
        receipt = {'url': opts['receipt_url'].get(t, opts['row_url'].get(t, BASE_URL[t])),
                   'fetched_at': opts['receipt_fetched'].get(t, '2026-10-26T00:00:00Z'),
                   'http_status': opts['receipt_status'].get(t, 200),
                   'sha256': opts['receipt_sha'].get(t, sha256_hex(raw)),
                   'bytes': len(raw)}
        for key in opts['receipt_drop_key'].get(t, ()):
            receipt.pop(key, None)
        files[receipt_path] = (json.dumps(receipt, indent=1, sort_keys=True) + '\n'
                               ).encode('utf-8')

    gate = []
    for t in TARGETS:
        first, second = NEW_ID[t], t
        if t in opts['gate_order']:
            first, second = second, first
        if t in opts['gate_wrong_first']:
            first = 'S264'
        prefix = '- QUOTE' if t in opts['gate_bad_prefix'] else '- C2-QUOTE'
        gate.append('%s %s %s: `%s`' % (prefix, first, second, opts['quote'].get(t, QUOTE[t])))
    gate.extend(opts['gate_extra'])
    files[LESSONS] = ('# round-48 lessons (fixture)\n\n## Gate\n\n' + '\n'.join(gate) + '\n'
                      + opts['lessons_extra'])

    for t in TARGETS:
        state = opts['entry'].get(t, 'good')
        ident = 'S264' if state == 'wrong-source' else NEW_ID[t]
        verified = '2026-10-25' if state == 'wrong-verified' else OPENED
        body = ['source: %s \u2014 %s \u2014 fixture entry for %s re-anchored'
                % (ident, BASE_URL[t], t),
                'verified-at: %s' % verified, '', '# fixture entry %s' % t, '',
                'Body text, not a registry row.', '']
        if state == 'late-source':
            body = ['# fixture entry %s' % t, ''] + ['filler line %d' % i for i in range(12)] \
                   + body
        if t in opts['entry_drop']:
            files[ENTRY[t]] = None
            continue
        files[ENTRY[t]] = '\n'.join(body)

    files['corpus/knowledge/e999.md'] = ('source: S999 \u2014 fixture\nverified-at: '
                                        '2026-10-26\n')
    if opts['counter']:
        files[SELF_PATH] = (opts['counter_bytes']
                            or open(os.path.abspath(__file__), 'rb').read())
    return files


class Fixture:
    """A throwaway git repo under TMPDIR; every call names -C ROOT and never the lane."""

    def __init__(self, root):
        self.root = root
        self.git('init', '-q')
        top = (self.git('rev-parse', '--show-toplevel') or b'').decode('utf-8').strip()
        if os.path.realpath(top) != os.path.realpath(root):
            raise SystemExit('selftest fixture is not its own toplevel: %r' % top)
        files = {SOURCES: fixture_base_sources()}
        for t in TARGETS:
            files[ENTRY[t]] = base_entry(t)
        self.base = self.commit(files, fresh=True)
        if not self.base:
            raise SystemExit('selftest fixture base commit failed')

    def git(self, *args):
        proc = subprocess.run(['git', '-C', self.root] + list(args), capture_output=True)
        return proc.stdout if proc.returncode == 0 else None

    def commit(self, files, fresh=False):
        if not fresh:
            self.git('checkout', '-q', '--detach', self.base)
            self.git('clean', '-qfdx')
        for path, raw in files.items():
            full = os.path.join(self.root, path)
            if raw is None:  # a path the case removes from the base tree
                if os.path.exists(full):
                    os.remove(full)
                continue
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'wb') as handle:
                handle.write(raw if isinstance(raw, bytes) else raw.encode('utf-8'))
        self.git('add', '-A')
        self.git('-c', 'user.name=c2 selftest', '-c', 'user.email=c2@selftest.invalid',
                 'commit', '-q', '-m', 'selftest case')
        head = self.git('rev-parse', 'HEAD')
        return head.decode('utf-8').strip() if head else None


def selftest():
    root = tempfile.mkdtemp(prefix='c2-r48-selftest-')
    cases = []

    def run(name, patch, expect_lines=None, expect_summary=(), forbid_summary=()):
        cases.append((name, patch, expect_lines or {}, list(expect_summary),
                      list(forbid_summary)))

    # positive, the pin, and the do-nothing shape
    run('positive_all_four', {},
        {'S026': 'REFRESHED', 'S048': 'REFRESHED', 'S093': 'REFRESHED', 'S108': 'REFRESHED'},
        ['self_pin=1 targets=4 refreshed=4 census_exit=0', 'C2_R48_PASS=true'])
    run('self_pin_mismatch', {'counter_bytes': b'# not the counter\n'},
        {}, ['self_pin=0', 'refreshed=4', 'C2_R48_PASS=false'])
    run('base_only_no_row',
        {'counter': False, 'row_missing': TARGETS, 'snap_drop': TARGETS,
         'receipt_drop': TARGETS},
        {'S026': 'row=none', 'S108': 'row=none'}, ['refreshed=0', 'C2_R48_PASS=false'])

    # row branches
    run('row_none', {'row_missing': ('S048',)}, {'S048': 'row=none', 'S026': 'REFRESHED'},
        ['refreshed=3', 'C2_R48_PASS=false'])
    run('row_ambiguous', {'row_dup': ('S026',)}, {'S026': 'row=ambiguous'}, ['refreshed=3'])
    run('row_ascii_hyphen', {'row_dash': ('S026',)}, {'S026': 'row=none'}, ['refreshed=3'])
    run('row_opened_wrong', {'row_opened': {'S026': '2026-10-25'}},
        {'S026': 'row=opened'}, ['refreshed=3'])
    run('row_status_queued', {'row_status': {'S026': 'queued'}}, {'S026': 'row=status'},
        ['refreshed=3'])
    run('row_base_url_absent', {'row_url': {'S026': 'https://example.test/other-26'}},
        {'S026': 'row=url'}, ['refreshed=3'])

    # snapshot branches
    run('snapshot_absent', {'snap_drop': ('S026',)}, {'S026': 'snapshot=absent'},
        ['refreshed=3'])
    run('snapshot_ambiguous', {'snap_extra': ('S026',)}, {'S026': 'snapshot=ambiguous'},
        ['refreshed=3'])
    run('snapshot_sha_mismatch', {'anchor_sha': {'S026': '0123456789ab'}},
        {'S026': 'snapshot=sha'}, ['refreshed=3'])
    run('snapshot_bad_gzip',
        {'snap_name': {'S026': 'fixture.html.gz'},
         'snap_raw': {'S026': b'<html><body>not gzip bytes</body></html>'}},
        {'S026': 'snapshot=gzip'}, ['refreshed=3'])
    run('snapshot_gz', {'snap_name': {'S026': 'fixture.html.gz'}},
        {'S026': 'snapshot=ok receipt=ok quote=ok phrases=ok entries=ok'},
        ['refreshed=4', 'C2_R48_PASS=true'])

    # receipt branches (amendment 1: the receipt url must be in R's URL set)
    run('receipt_absent', {'receipt_drop': ('S026',)}, {'S026': 'receipt=absent'},
        ['refreshed=3'])
    run('receipt_url_outside', {'receipt_url': {'S026': 'https://example.test/fetch-26'}},
        {'S026': 'receipt=url'}, ['refreshed=3'])
    run('receipt_fetched_at_wrong', {'receipt_fetched': {'S026': '2026-10-25T00:00:00Z'}},
        {'S026': 'receipt=fetched_at'}, ['refreshed=3'])
    run('receipt_http_status', {'receipt_status': {'S026': 404}},
        {'S026': 'receipt=http_status'}, ['refreshed=3'])
    run('receipt_sha_mismatch', {'receipt_sha': {'S026': 'dead' * 16}},
        {'S026': 'receipt=sha'}, ['refreshed=3'])
    run('receipt_bytes_missing', {'receipt_drop_key': {'S026': ('bytes',)}},
        {'S026': 'receipt=bytes'}, ['refreshed=3'])
    run('receipt_json_bad', {'receipt_raw': {'S026': b'{"url": '}},
        {'S026': 'receipt=json'}, ['refreshed=3'])

    # quote branches (amendment 2)
    run('quote_noline', {'gate_bad_prefix': ('S026',)}, {'S026': 'quote=noline'},
        ['refreshed=3'])
    run('quote_wrong_order', {'gate_order': ('S026',)}, {'S026': 'quote=noline'},
        ['refreshed=3'])
    run('quote_names_other_row', {'gate_wrong_first': ('S026',)},
        {'S026': 'quote=line'}, ['refreshed=3'])
    run('quote_no_case_fold', {'quote': {'S026': QUOTE['S026'].capitalize()}},
        {'S026': 'quote=absent'}, ['refreshed=3'])
    run('quote_26_words',
        {'snap_body': {'S026': '<p>' + ' '.join(['w%d' % i for i in range(25)]) + ' 84%</p>'},
         'quote': {'S026': ' '.join(['w%d' % i for i in range(25)]) + ' 84%'}},
        {'S026': 'quote=26w'}, ['refreshed=3'])
    run('quote_25_words',
        {'snap_body': {'S026': '<p>' + ' '.join(['w%d' % i for i in range(24)]) + ' 84%</p>'},
         'quote': {'S026': ' '.join(['w%d' % i for i in range(24)]) + ' 84%'}},
        {'S026': 'quote=ok', 'S026': 'REFRESHED'}, ['refreshed=4'])
    run('quote_script_only',
        {'snap_body': {'S026': '<html><head><script>' + QUOTE['S026'] + '</script>'
                               '<style>' + QUOTE['S026'] + '</style></head>'
                               '<body><p>other text</p></body></html>'}},
        {'S026': 'quote=absent'}, ['refreshed=3'])
    run('quote_style_only',
        {'snap_body': {'S026': '<html><head><style>' + QUOTE['S026'] + '</style></head>'
                               '<body><p>other text</p></body></html>'}},
        {'S026': 'quote=absent'}, ['refreshed=3'])
    run('quote_entity_unescape',
        {'snap_body': {'S026': '<p>about 84&#37; of the transitions we observe from pass to '
                               'fail involve a flaky test</p>'}},
        {'S026': 'quote=ok'}, ['refreshed=4'])
    run('quote_whitespace_only', {'quote': {'S026': '   '}},
        {'S026': 'quote=empty'}, ['refreshed=3'])
    run('phrases_missing',
        {'snap_body': {'S048': '<p>these classes are prioritised for re-execution</p>'},
         'quote': {'S048': 'these classes are prioritised for re-execution'}},
        {'S048': 'quote=ok phrases=missing'}, ['refreshed=3'])
    run('phrases_s093_needs_both',
        {'snap_body': {'S093': '<p>the --unshare-all option is documented</p>'},
         'quote': {'S093': 'the --unshare-all option is documented'}},
        {'S093': 'phrases=missing'}, ['refreshed=3'])

    # entries branches
    run('entry_absent', {'entry_drop': ('S026',)}, {'S026': 'entries=absent'},
        ['refreshed=3'])
    run('entry_source_wrong', {'entry': {'S026': 'wrong-source'}},
        {'S026': 'entries=source'}, ['refreshed=3'])
    run('entry_verified_at_wrong', {'entry': {'S026': 'wrong-verified'}},
        {'S026': 'entries=verified-at'}, ['refreshed=3'])
    run('entry_source_beyond_ten_lines', {'entry': {'S026': 'late-source'}},
        {'S026': 'entries=source'}, ['refreshed=3'])
    run('entry_usedby_extra',
        {'row_usedby': {'S026': ENTRY['S026'] + ', corpus/knowledge/e999.md'}},
        {'S026': 'entries=usedby'}, ['refreshed=3'])
    run('entry_usedby_empty', {'row_usedby': {'S026': EMDASH}},
        {'S026': 'entries=usedby'}, ['refreshed=3'])

    # census branch
    run('census_nonzero',
        {'extra_rows': [
            '| S271 | fixture dangling used-by \u2014 https://example.test/dangling | docs '
            '| A | fixture dangling scope | fixture anchor | fixture dangling teaches cell '
            '| mined | 2026-10-26 | 90d | corpus/knowledge/absent.md |\n']},
        {'S026': 'REFRESHED', 'S108': 'REFRESHED'},
        ['refreshed=4', 'C2_R48_PASS=false'])

    # live branches
    run('live_absent', {'fetch': 'absent'}, {'S026': 'live=absent', 'S026': 'NOT'},
        ['refreshed=0', 'C2_R48_PASS=false'])
    run('live_unreachable', {'fetch': 'unreachable'},
        {'S026': 'live=unreachable', 'S026': 'NOT'}, ['refreshed=0', 'C2_R48_PASS=false'])
    run('no_live_partial', {'live_mode': False},
        {'S026': 'live=skipped', 'S026': 'REFRESHED'},
        ['refreshed=4', 'C2_R48_PARTIAL=true'], ['C2_R48_PASS='])

    failed = 0
    try:
        fixture = Fixture(root)
        for index, (name, patch, expect_lines, expect_summary, forbid_summary) in \
                enumerate(cases, 1):
            opts = default_opts()
            opts.update(patch)
            rev = fixture.commit(fixture_tree(opts))
            bodies = {}
            for t in TARGETS:
                bodies[opts['row_url'].get(t, BASE_URL[t])] = \
                    opts['snap_body'].get(t, SNAP_BODY[t]).encode('utf-8')
            mode = opts['fetch']

            def fetch(url, _mode=mode, _bodies=bodies):
                if _mode == 'unreachable':
                    raise OSError('selftest: unreachable by construction')
                if _mode == 'absent':
                    return b'<html><body><p>nothing of interest here</p></body></html>'
                return _bodies.get(url, b'<html><body><p>nothing of interest</p></body></html>')

            problems = []
            if rev is None:
                problems.append('case commit failed')
                text, result = '', None
            else:
                buf = io.StringIO()
                result = measure(fixture.root, rev, base=fixture.base,
                                 live=opts['live_mode'], fetch=fetch, out=buf)
                text = buf.getvalue()
                for t, needle in expect_lines.items():
                    if needle not in result['lines'][t]:
                        problems.append('%s line %r lacks %r'
                                        % (t, result['lines'][t], needle))
                for needle in expect_summary:
                    if needle not in text:
                        problems.append('summary lacks %r' % needle)
                for needle in forbid_summary:
                    if needle in text:
                        problems.append('summary contains forbidden %r' % needle)
            if problems:
                failed += 1
                print('SELFTEST %02d_%s: FAIL %s' % (index, name, '; '.join(problems)))
                for line in text.splitlines():
                    print('    | ' + line)
            else:
                print('SELFTEST %02d_%s: PASS' % (index, name))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print('C2_R48_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


# ------------------------------------------------------------------------ main ---

def main(argv=None):
    parser = argparse.ArgumentParser(description='round-48 C2 freshness counter')
    parser.add_argument('--lane')
    parser.add_argument('--rev')
    parser.add_argument('--no-live', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.lane or not args.rev:
        parser.error('--lane and --rev are required outside --selftest')
    result = measure(args.lane, args.rev, live=not args.no_live)
    return 0 if result['verdict'] else 1


if __name__ == '__main__':
    sys.exit(main())
