#!/usr/bin/env python3
"""Round-45 C2 (coverage) counter: GoogleTest upstream test-isolation ground.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C2_R45_PASS=true iff entries >= 2 and rows >= 2 and indexed == entries and
  self_pin=1, where
  * rows    = census-valid registry rows at REV with status `mined` whose source
              cell's first URL is under github.com/google/googletest/ or
              raw.githubusercontent.com/google/googletest/, whose anchor cell
              names a snapshot path under .ufo/evidence/round-45/coverage/sources/
              present at REV and an 8+-hex sha256 prefix of that snapshot's bytes;
  * entries = corpus/knowledge/*.md files at REV whose line 1 is `source:` citing
              at least one such row id, line 2 `verified-at:` with an ISO date
              >= 2026-10-25, line 3 `recheck:`, that are listed in the cited
              row's used-by cell, and that carry at least one double-quoted
              ("..." or \u201c...\u201d) quote of 6..25 whitespace tokens found in the
              whitespace-folded text of a cited row's snapshot;
  * indexed = entries whose repo path appears backticked in corpus/README.md at REV.
Modes: --lane L --rev R; --selftest.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-47/hardening/coverage-counter.py'
SNAP_PREFIX = '.ufo/evidence/round-45/coverage/sources/'
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s;,)]+')
GT_RE = re.compile(r'^https?://(github\.com|raw\.githubusercontent\.com)/google/googletest/')
SNAP_RE = re.compile(re.escape(SNAP_PREFIX) + r'[A-Za-z0-9._/-]+')
HEX_RE = re.compile(r'\b[0-9a-f]{8,64}\b')
QUOTE_RE = re.compile(r'"([^"\n]{10,400})"|\u201c([^\u201d\n]{10,400})\u201d')
CITE_RE = re.compile(r'\bS\d{3,}\b')
MIN_VERIFIED = '2026-10-25'


def fold(text):
    for a, b in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"'),
                 ('\u00a0', ' '), ('\u200b', '')):
        text = text.replace(a, b)
    return ' '.join(text.split())


class Tree:
    def __init__(self, lane, rev):
        self.lane, self.rev = lane, rev

    def read(self, path, binary=False):
        out = subprocess.run(['git', '-C', self.lane, 'show', '%s:%s' % (self.rev, path)],
                             capture_output=True)
        if out.returncode != 0:
            return None
        return out.stdout if binary else out.stdout.decode('utf-8', 'replace')

    def ls(self, prefix):
        out = subprocess.run(['git', '-C', self.lane, 'ls-tree', '--name-only', self.rev, prefix],
                             capture_output=True)
        return out.stdout.decode().split() if out.returncode == 0 else []


def gt_rows(tree):
    rows = {}
    for line in (tree.read('corpus/SOURCES.md') or '').splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.split('|')]
        if len(cells) != 13 or cells[8] != 'mined':
            continue
        url = URL_RE.search(cells[2])
        if not url or not GT_RE.match(url.group(0)):
            continue
        snap = SNAP_RE.search(cells[6])
        if not snap:
            continue
        data = tree.read(snap.group(0), binary=True)
        if data is None:
            continue
        digest = hashlib.sha256(data).hexdigest()
        if not any(digest.startswith(h) for h in HEX_RE.findall(cells[6])):
            continue
        used = {p.strip() for p in re.split(r'[,;]', cells[11]) if p.strip()}
        rows[cells[1]] = dict(text=fold(data.decode('utf-8', 'replace')), used=used)
    return rows


def entry_ok(path, text, rows):
    lines = text.splitlines()
    cited = [c for c in CITE_RE.findall(lines[0] if lines else '') if c in rows]
    if not cited:
        return False, 'cites no googletest row'
    if len(lines) < 3 or not lines[0].startswith('source:'):
        return False, 'no provenance trio'
    m = re.match(r'verified-at:\s*(\d{4}-\d{2}-\d{2})', lines[1])
    if not m or m.group(1) < MIN_VERIFIED:
        return False, 'verified-at'
    if not lines[2].startswith('recheck:'):
        return False, 'recheck'
    cited = [c for c in cited if path in rows[c]['used']]
    if not cited:
        return False, 'not in used-by'
    for q in QUOTE_RE.finditer(text):
        quote = fold(q.group(1) or q.group(2))
        if 6 <= len(quote.split()) <= 25 and any(quote in rows[c]['text'] for c in cited):
            return True, 'ok'
    return False, 'no located quote'


def measure(lane, rev):
    me = open(os.path.abspath(__file__), 'rb').read()
    tree = Tree(lane, rev)
    blob = tree.read(SELF_PATH, binary=True)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    rows = gt_rows(tree)
    readme = tree.read('corpus/README.md') or ''
    entries, indexed = [], []
    for path in tree.ls('corpus/knowledge/'):
        if not path.endswith('.md'):
            continue
        ok, why = entry_ok(path, tree.read(path) or '', rows)
        if ok:
            entries.append(path)
            if '`%s`' % path in readme or '`%s`' % path[len('corpus/'):] in readme:
                indexed.append(path)
        elif why != 'cites no googletest row':
            print('REFUSED %s %s' % (path, why))
    for p in entries:
        print('ENTRY %s%s' % (p, '' if p in indexed else ' (not indexed)'))
    passed = self_pin == 1 and len(entries) >= 2 and len(rows) >= 2 and len(indexed) == len(entries)
    print('C2_R45: self_pin=%d rows=%d entries=%d indexed=%d row_ids=%s rev=%s C2_R45_PASS=%s' % (
        self_pin, len(rows), len(entries), len(indexed), ','.join(sorted(rows)) or '-', rev,
        'true' if passed else 'false'))
    return 0 if passed else 1


def selftest():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    results = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r45-c2-') as d:
        def git(*a):
            subprocess.run(['git', '-C', d, *a], env=env, capture_output=True, check=True)
        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())
        git('init', '-q', '-b', 'm')
        assert subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True,
                              env=env).stdout.decode().strip() == os.path.realpath(d)
        snap = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
        sha = hashlib.sha256(snap).hexdigest()[:8]
        put(SNAP_PREFIX + 'advanced.md', snap)
        put(SNAP_PREFIX + 'primer.md', snap)
        def row(i, name, used, url='https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md',
                h=sha, status='mined'):
            return ('| %s | t — %s | docs | A | s | %s%s.md %s | t | %s | 2026-10-25 | 180d | %s |\n'
                    % (i, url % name, SNAP_PREFIX, name, h, status, used))
        entry = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
                 'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
        def build(reg, entries, readme):
            put('corpus/SOURCES.md', reg)
            for p, t in entries.items():
                put(p, t)
            put('corpus/README.md', readme)
            put(SELF_PATH, open(os.path.abspath(__file__), 'rb').read())
            git('add', '-A')
            git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
            out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                                 capture_output=True, text=True)
            return out.stdout.strip().splitlines()[-1]
        ea, eb = 'corpus/knowledge/a.md', 'corpus/knowledge/b.md'
        good_reg = row('S256', 'advanced', ea + ', ' + eb) + row('S257', 'primer', ea + ', ' + eb)
        idx = '`knowledge/a.md` `knowledge/b.md`'
        cases = [
            ('T1_two_entries_pass', good_reg, {ea: entry, eb: entry}, idx, 'C2_R45_PASS=true'),
            ('T2_rows_only_fail', good_reg, {ea: 'x\n', eb: 'x\n'}, idx, 'entries=0'),
            ('T3_old_verified_at', good_reg, {ea: entry.replace('2026-10-25', '2026-10-24'), eb: entry}, idx, 'entries=1'),
            ('T4_quote_not_in_snapshot', good_reg, {ea: entry.replace('cannot depend', 'must depend'), eb: entry}, idx, 'entries=1'),
            ('T5_not_used_by', row('S256', 'advanced', eb) + row('S257', 'primer', eb), {ea: entry, eb: entry}, idx, 'entries=1'),
            ('T6_bad_sha_prefix', row('S256', 'advanced', ea + ', ' + eb, h='deadbeef') + row('S257', 'primer', ea + ', ' + eb),
             {ea: entry, eb: entry}, idx, 'rows=1'),
            ('T7_not_indexed', good_reg, {ea: entry, eb: entry}, '`knowledge/a.md`', 'indexed=1'),
            ('T8_queued_rows', row('S256', 'advanced', ea, status='queued') + row('S257', 'primer', ea, status='queued'),
             {ea: entry, eb: entry}, idx, 'rows=0'),
            ('T9_non_googletest_url', row('S256', 'advanced', ea + ', ' + eb, url='https://example.org/%s') +
             row('S257', 'primer', ea + ', ' + eb, url='https://example.org/%s'), {ea: entry, eb: entry}, idx, 'rows=0'),
            ('T10_indented_row_counts', '  ' + good_reg.replace('\n| S257', '\n   | S257'), {ea: entry, eb: entry}, idx, 'rows=2'),
        ]
        failed = 0
        for name, reg, ents, readme, want in cases:
            for p in (ea, eb):
                full = os.path.join(d, p)
                if os.path.exists(full):
                    os.remove(full)
            line = build(reg, ents, readme)
            ok = want in line
            failed += not ok
            print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, want, line))
    extra_cases = 0
    _c, _f = extra_HardCover1()
    extra_cases += _c
    failed += _f
    _c, _f = extra_HardCover2()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardCoverEntry()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardCoverGt()
    extra_cases += _c
    failed += _f
    _c, _f = extra_T47HardCoverMeasure()
    extra_cases += _c
    failed += _f
    print('C2_R45_SELFTEST: cases=%d failed=%d' % (len(cases) + extra_cases, failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


# HardCover1: selftest cases for the round-45 coverage counter's row/entry rules.
# Each case is the smallest fixture that separates the pristine rule from one declared mutant
# (mutants.json group `coverage`, ids C01..C05) and asserts the counter's printed tally fields.

_xHardCover1_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'


def _xHardCover1_sha():
    return hashlib.sha256(_xHardCover1_SNAP).hexdigest()[:8]


def _xHardCover1_row(rid, url, anchor, used, status='mined'):
    return ('| %s | t — %s | docs | A | s | %s | t | %s | 2026-10-25 | 180d | %s |\n'
            % (rid, url, anchor, status, used))


def _xHardCover1_last_line(files, reg, readme):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    with tempfile.TemporaryDirectory(prefix='tameshi-r46-hc1-') as d:
        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())
        subprocess.run(['git', '-C', d, 'init', '-q', '-b', 'm'], env=env, capture_output=True, check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, env=env).stdout.decode().strip()
        assert top == os.path.realpath(d), 'scratch toplevel %r != %r' % (top, os.path.realpath(d))
        put('corpus/SOURCES.md', reg)
        for p, t in files.items():
            put(p, t)
        put('corpus/README.md', readme)
        put(SELF_PATH, open(os.path.abspath(__file__), 'rb').read())
        subprocess.run(['git', '-C', d, 'add', '-A'], env=env, capture_output=True, check=True)
        subprocess.run(['git', '-C', d, '-c', 'user.name=t', '-c', 'user.email=t@t',
                        'commit', '-qm', 'x', '--allow-empty'], env=env, capture_output=True, check=True)
        out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                             capture_output=True, text=True)
        return (out.stdout.strip().splitlines() or [''])[-1]


def extra_HardCover1():
    ea, eb = 'corpus/knowledge/a.md', 'corpus/knowledge/b.md'
    idx = '`knowledge/a.md` `knowledge/b.md`'
    sha = _xHardCover1_sha()
    entry = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
             'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
    snap45 = SNAP_PREFIX + 'advanced.md'
    snap45b = SNAP_PREFIX + 'primer.md'
    gt_url = 'https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md'
    good_reg = (_xHardCover1_row('S256', gt_url % 'advanced', snap45 + ' ' + sha, ea + ', ' + eb) +
                _xHardCover1_row('S257', gt_url % 'primer', snap45b + ' ' + sha, ea + ', ' + eb))
    good_files = {snap45: _xHardCover1_SNAP, snap45b: _xHardCover1_SNAP, ea: entry, eb: entry}

    # C01: a github.com URL that is not under google/googletest must not count as a row.
    gh_url = 'https://github.com/example/notgoogletest/docs/%s.md'
    reg_c01 = (_xHardCover1_row('S256', gh_url % 'advanced', snap45 + ' ' + sha, ea + ', ' + eb) +
               _xHardCover1_row('S257', gh_url % 'primer', snap45b + ' ' + sha, ea + ', ' + eb))

    # C02: a snapshot anchored under round-44 must not count (the anchor prefix is round-45 only).
    snap44 = '.ufo/evidence/round-44/coverage/sources/advanced.md'
    snap44b = '.ufo/evidence/round-44/coverage/sources/primer.md'
    reg_c02 = (_xHardCover1_row('S256', gt_url % 'advanced', snap44 + ' ' + sha, ea + ', ' + eb) +
               _xHardCover1_row('S257', gt_url % 'primer', snap44b + ' ' + sha, ea + ', ' + eb))
    files_c02 = {snap44: _xHardCover1_SNAP, snap44b: _xHardCover1_SNAP, ea: entry, eb: entry}

    # C03: a snapshot absent at REV must skip its row even when the anchor names sha256(b'')'s prefix.
    reg_c03 = (_xHardCover1_row('S256', gt_url % 'advanced', SNAP_PREFIX + 'missing.md e3b0c442',
                                ea + ', ' + eb) +
               _xHardCover1_row('S257', gt_url % 'primer', SNAP_PREFIX + 'missing2.md e3b0c442',
                                ea + ', ' + eb))
    files_c03 = {ea: entry, eb: entry}

    cases = [
        ('C01_github_not_googletest', reg_c01, good_files, idx, 'rows=0 entries=0'),
        ('C02_round44_snapshot_path', reg_c02, files_c02, idx, 'rows=0 entries=0'),
        ('C03_missing_snapshot_empty_sha', reg_c03, files_c03, idx, 'rows=0 entries=0'),
        ('C04_entry_without_source_line1', good_reg,
         {snap45: _xHardCover1_SNAP, snap45b: _xHardCover1_SNAP,
          ea: entry, eb: entry.replace('source: ', '', 1)}, idx, 'entries=1 indexed=1'),
        ('C05_entry_without_recheck_line3', good_reg,
         {snap45: _xHardCover1_SNAP, snap45b: _xHardCover1_SNAP,
          ea: entry, eb: entry.replace('recheck:', 'review:', 1)}, idx, 'entries=1 indexed=1'),
    ]
    failed = 0
    for name, reg, files, readme, want in cases:
        line = _xHardCover1_last_line(files, reg, readme)
        ok = want in line
        failed += not ok
        print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, want, line))
    return len(cases), failed


# HardCover2 (round 46, C2 operability): selftest additions for the round-45 coverage counter.
# Each case is the smallest scratch repo that separates the pristine predicate from one declared
# survivor (C06..C10 in hardening/mutants.json, group coverage); the assertion is on the PASS token.

_xHardCover2_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
_xHardCover2_ENTRY = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
                      'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
_xHardCover2_EA = 'corpus/knowledge/a.md'
_xHardCover2_EB = 'corpus/knowledge/b.md'
_xHardCover2_URL = 'https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md'


def _xHardCover2_row(i, name, used, digest):
    return ('| %s | t — %s | docs | A | s | %s%s.md %s | t | mined | 2026-10-25 | 180d | %s |\n'
            % (i, _xHardCover2_URL % name, SNAP_PREFIX, name, digest, used))


def _xHardCover2_build(reg, entries, readme, self_bytes=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')

    with tempfile.TemporaryDirectory(prefix='tameshi-r46-hc2-') as d:
        def git(*a):
            subprocess.run(['git', '-C', d, *a], env=env, capture_output=True, check=True)

        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())

        git('init', '-q', '-b', 'm')
        assert subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True,
                              env=env).stdout.decode().strip() == os.path.realpath(d)
        put(SNAP_PREFIX + 'advanced.md', _xHardCover2_SNAP)
        put(SNAP_PREFIX + 'primer.md', _xHardCover2_SNAP)
        put('corpus/SOURCES.md', reg)
        for p, t in entries.items():
            put(p, t)
        put('corpus/README.md', readme)
        me = open(os.path.abspath(__file__), 'rb').read()
        put(SELF_PATH, me if self_bytes is None else self_bytes)
        git('add', '-A')
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
        out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                             capture_output=True, text=True, env=env)
        return out.stdout.strip().splitlines()


def extra_HardCover2():
    digest = hashlib.sha256(_xHardCover2_SNAP).hexdigest()[:8]
    both = _xHardCover2_EA + ', ' + _xHardCover2_EB
    good = (_xHardCover2_row('S256', 'advanced', both, digest)
            + _xHardCover2_row('S257', 'primer', both, digest))
    ents = {_xHardCover2_EA: _xHardCover2_ENTRY, _xHardCover2_EB: _xHardCover2_ENTRY}
    idx = '`knowledge/a.md` `knowledge/b.md`'
    cases = [
        # C06: README may index by the full repo path; the mutant only accepts the short form.
        ('C06_readme_fullpath_index',
         lambda: _xHardCover2_build(good, ents, '`corpus/knowledge/a.md` `corpus/knowledge/b.md`'),
         ('indexed=2', 'C2_R45_PASS=true')),
        # C07: one googletest row must not be enough even when both entries are otherwise valid.
        ('C07_rows_one_fails',
         lambda: _xHardCover2_build(_xHardCover2_row('S256', 'advanced', both, digest), ents, idx),
         ('rows=1', 'C2_R45_PASS=false')),
        # C08: one entry must not be enough even with two rows and a matching index.
        ('C08_entries_one_fails',
         lambda: _xHardCover2_build(good, {_xHardCover2_EA: _xHardCover2_ENTRY}, idx),
         ('entries=1', 'C2_R45_PASS=false')),
        # C09: an unindexed entry must fail even when another entry is indexed.
        ('C09_indexed_lt_entries_fails',
         lambda: _xHardCover2_build(good, ents, '`knowledge/a.md`'),
         ('indexed=1', 'C2_R45_PASS=false')),
        # C10: a counter committed with different bytes at SELF_PATH must fail on self_pin.
        ('C10_self_pin_zero_fails',
         lambda: _xHardCover2_build(good, ents, idx, self_bytes=b'# not the running counter\n'),
         ('self_pin=0', 'C2_R45_PASS=false')),
    ]
    failed = 0
    for name, run, wants in cases:
        lines = run()
        summary = lines[-1] if lines else ''
        ok = all(w in summary for w in wants)
        failed += not ok
        print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, wants, summary))
    return len(cases), failed


# T47HardCoverEntry (round 47, C2 operability): selftest additions for the round-46 hardened
# coverage counter's entry_ok() rule.  Each case feeds entry_ok() the smallest in-memory fixture
# (a rows dict plus an entry text, no git repo, no network) that makes the pristine predicate and
# one frozen pool mutant (group coverage, function entry_ok) return different values.

_xT47HardCoverEntry_PATH = 'corpus/knowledge/a.md'
_xT47HardCoverEntry_SNAP = 'Remember that the test order is undefined, so your code cannot depend on it.'
_xT47HardCoverEntry_QUOTE = 'the test order is undefined, so your code cannot depend on it'


def _xT47HardCoverEntry_entry(quote, pad=0):
    """Provenance lines (source / verified-at / recheck) with `quote` on line 3, plus `pad` blanks."""
    return '\n'.join(['source: S256 — upstream',
                      'verified-at: 2026-10-25',
                      'recheck: 365d — %s' % quote] + [''] * pad) + '\n'


def _xT47HardCoverEntry_probe(text, snapshot):
    rows = {'S256': dict(text=fold(snapshot), used={_xT47HardCoverEntry_PATH})}
    return entry_ok(_xT47HardCoverEntry_PATH, text, rows)


def extra_T47HardCoverEntry():
    tokens6 = ' '.join('t%d' % i for i in range(1, 7))
    tokens26 = ' '.join('u%d' % i for i in range(1, 27))
    plan = [
        # exactly three provenance lines: the trio minimum is `len(lines) < 3`, so 3 lines is ok
        ('T47HE_three_line_entry_ok',
         _xT47HardCoverEntry_entry('upstream says "%s"' % _xT47HardCoverEntry_QUOTE),
         _xT47HardCoverEntry_SNAP, (True, 'ok')),
        # a located quote of exactly 6 tokens sits on the lower edge of the 6..25 window
        ('T47HE_six_token_quote_ok',
         _xT47HardCoverEntry_entry('note "%s" holds' % tokens6, pad=1),
         'Upstream note: "%s" ends here.' % tokens6, (True, 'ok')),
        # a located quote of exactly 26 tokens is outside the window, so the entry is refused
        ('T47HE_twenty_six_token_quote_refused',
         _xT47HardCoverEntry_entry('note "%s" holds' % tokens26, pad=1),
         'Upstream note: "%s" ends here.' % tokens26, (False, 'no located quote')),
        # curly quotes live in group 2, the fallback arm of `q.group(1) or q.group(2)`
        ('T47HE_curly_quote_fallback_ok',
         _xT47HardCoverEntry_entry('upstream says “%s”' % _xT47HardCoverEntry_QUOTE, pad=1),
         _xT47HardCoverEntry_SNAP, (True, 'ok')),
    ]
    failed = 0
    for name, text, snapshot, want in plan:
        try:
            got = _xT47HardCoverEntry_probe(text, snapshot)
            detail = 'got=%r' % (got,)
            ok = got == want
        except Exception as exc:  # a mutant that makes the rule raise is a named failure, not a crash
            detail = 'raised %s' % type(exc).__name__
            ok = False
        failed += not ok
        print('%s %s want=%r %s' % ('PASS' if ok else 'FAIL', name, want, detail))
    return len(plan), failed


# T47HardCoverGt (round 47, C2 operability): selftest additions for the round-45 coverage counter.
# The four mutants below sit in `Tree.read` (the `binary` flag) and in `gt_rows` (the snapshot read
# and the two `group(0)` indexes). Every one of them makes a counter run die inside `gt_rows`, and
# the round-46 suite reaches that path only through a subprocess whose last stdout line it indexes:
# the frozen case raises IndexError and the suite exits on a bare traceback, which the pool scores
# as `crashed`, not `killed`. So the probes here drive `gt_rows` on a scratch lane in process and
# report the raised call as a named FAIL, and `selftest()` below keeps the process alive after the
# frozen suite dies so those FAIL lines can be printed. The probes print nothing when they pass, so
# a crash outside their inputs stays an unlabelled crash exactly as without this addition.

_xT47HardCoverGt_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
_xT47HardCoverGt_ENTRY = ('source: S256 S257 — upstream\nverified-at: 2026-10-25\nrecheck: 365d\n\n'
                          'Upstream says "the test order is undefined, so your code cannot depend on it".\n')
_xT47HardCoverGt_EA = 'corpus/knowledge/a.md'
_xT47HardCoverGt_EB = 'corpus/knowledge/b.md'
_xT47HardCoverGt_URL = 'https://raw.githubusercontent.com/google/googletest/abc/docs/%s.md'
_xT47HardCoverGt_result = []


def _xT47HardCoverGt_row(rid, name, used, digest):
    return ('| %s | t — %s | docs | A | s | %s%s.md %s | t | mined | 2026-10-25 | 180d | %s |\n'
            % (rid, _xT47HardCoverGt_URL % name, SNAP_PREFIX, name, digest, used))


def _xT47HardCoverGt_lane(reg, entries, readme, probe):
    """Commit a scratch lane holding the registry, the snapshots and the running counter's bytes."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    with tempfile.TemporaryDirectory(prefix='tameshi-r47-hcgt-') as d:
        def git(*a):
            return subprocess.run(['git', '-C', d, *a], env=env, capture_output=True)

        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'wb') as fh:
                fh.write(t if isinstance(t, bytes) else t.encode())

        git('init', '-q', '-b', 'm')
        top = git('rev-parse', '--show-toplevel').stdout.decode().strip()
        assert top == os.path.realpath(d), 'scratch toplevel %r != %r' % (top, os.path.realpath(d))
        put(SNAP_PREFIX + 'advanced.md', _xT47HardCoverGt_SNAP)
        put(SNAP_PREFIX + 'primer.md', _xT47HardCoverGt_SNAP)
        put('corpus/SOURCES.md', reg)
        for p, t in entries.items():
            put(p, t)
        put('corpus/README.md', readme)
        with open(os.path.abspath(__file__), 'rb') as fh:
            put(SELF_PATH, fh.read())
        git('add', '-A')
        git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
        return probe(d, env)


def _xT47HardCoverGt_probe_rows(d, env):
    """Read the registry through the rule under test; returns (row ids, row table)."""
    rows = gt_rows(Tree(d, 'm'))
    return sorted(rows), rows


def _xT47HardCoverGt_probe_measure(d, env):
    """Run the counter under test over the lane; returns (exit code, last stdout line)."""
    out = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', d, '--rev', 'm'],
                         capture_output=True, text=True, env=env)
    lines = out.stdout.strip().splitlines()
    return out.returncode, (lines[-1] if lines else '')


def extra_T47HardCoverGt():
    if _xT47HardCoverGt_result:
        return _xT47HardCoverGt_result[0]
    _xT47HardCoverGt_result.append((0, 1))  # re-entry guard: a raising probe never loops back here
    digest = hashlib.sha256(_xT47HardCoverGt_SNAP).hexdigest()[:8]
    both = _xT47HardCoverGt_EA + ', ' + _xT47HardCoverGt_EB
    ents = {_xT47HardCoverGt_EA: _xT47HardCoverGt_ENTRY, _xT47HardCoverGt_EB: _xT47HardCoverGt_ENTRY}
    idx = '`knowledge/a.md` `knowledge/b.md`'
    two_rows = (_xT47HardCoverGt_row('S256', 'advanced', both, digest)
                + _xT47HardCoverGt_row('S257', 'primer', both, digest))
    one_row = _xT47HardCoverGt_row('S256', 'advanced', both, digest)
    bad_rows = (_xT47HardCoverGt_row('S256', 'advanced', both, 'deadbeef')
                + _xT47HardCoverGt_row('S257', 'primer', both, 'deadbeef'))

    # G01: two mined googletest rows whose anchors name existing snapshots must be counted.
    # The registry is read with the default text mode and each snapshot with `binary=True`, and the
    # row id is taken from the regex match's group 0 (`SNAP_RE`/`URL_RE` have no capture groups, so
    # indexing group 1 raises instead of yielding a row).
    def g01():
        names, _rows = _xT47HardCoverGt_lane(two_rows, ents, idx, _xT47HardCoverGt_probe_rows)
        return names == ['S256', 'S257'], 'row_ids=%s' % (','.join(names) or '-')

    # G02: the snapshot must reach the row as bytes (its sha256 is checked and its text folded), and
    # the used-by cell must be split into the entry paths it names.
    def g02():
        _names, rows = _xT47HardCoverGt_lane(two_rows, ents, idx, _xT47HardCoverGt_probe_rows)
        row = rows['S256']
        ok = row['text'] == fold(_xT47HardCoverGt_SNAP.decode()) and row['used'] == set(ents)
        return ok, 'text=%r used=%s' % (row['text'][:40], ','.join(sorted(row['used'])) or '-')

    # G03: a row whose anchor digest cannot match any prefix of the snapshot bytes is dropped, and
    # dropping it must leave no row rather than raise on the way.
    def g03():
        names, _rows = _xT47HardCoverGt_lane(bad_rows, ents, idx, _xT47HardCoverGt_probe_rows)
        return names == [], 'row_ids=%s' % (','.join(names) or '-')

    # G04: the whole counter completes over the same fixture and reports the two rows and a pass.
    def g04():
        rc, line = _xT47HardCoverGt_lane(two_rows, ents, idx, _xT47HardCoverGt_probe_measure)
        return rc == 0 and 'rows=2' in line and 'C2_R45_PASS=true' in line, 'exit=%d %s' % (rc, line)

    # G05: with a single row the same read path still reaches a verdict (one row is too few).
    def g05():
        rc, line = _xT47HardCoverGt_lane(one_row, ents, idx, _xT47HardCoverGt_probe_measure)
        return rc == 1 and 'rows=1' in line and 'C2_R45_PASS=false' in line, 'exit=%d %s' % (rc, line)

    cases = [
        ('G01_gt_rows_reads_two_rows', g01),
        ('G02_gt_rows_snapshot_bytes_folded', g02),
        ('G03_gt_rows_mismatched_digest_dropped', g03),
        ('G04_measure_valid_fixture_passes', g04),
        ('G05_measure_single_row_completes', g05),
    ]
    failed = 0
    for name, fn in cases:
        try:
            ok, detail = fn()
        except Exception as exc:  # a mutant that makes the rule raise is a named failure, not a crash
            ok, detail = False, 'raised %s: %s' % (type(exc).__name__, exc)
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    _xT47HardCoverGt_result[0] = (len(cases), failed)
    return _xT47HardCoverGt_result[0]


_xT47HardCoverGt_frozen_selftest = selftest


def selftest():
    """Run the frozen case suite; if it dies, give the probes above the chance to name the crash.

    A round-46 case indexes the last stdout line of the counter run it launches, so a counter that
    dies on the way raises IndexError inside the suite and the process exits on a traceback. Here
    that exception is held, the probes run, and their FAIL lines carry the input separation; when
    every probe passes they print nothing and the run remains an unlabelled crash.
    """
    try:
        return _xT47HardCoverGt_frozen_selftest()
    except Exception:
        try:
            extra_T47HardCoverGt()
        except Exception as exc:
            print('T47HardCoverGt: probes raised %s: %s' % (type(exc).__name__, exc), file=sys.stderr)
        return 1


# T47HardCoverMeasure (round 47, C2 operability): selftest cases for the round-45 coverage
# counter's own `measure()` tally.  Each case builds one scratch lane and calls measure() in
# process (stdout captured), so a mutant that raises is reported as a named FAIL instead of a
# traceback, and the assertion is on a value the rule really returns: the exit code, the self-pin
# read, the REFUSED guard, the ENTRY index suffix and the row-id join each get an input that
# separates the pristine rule from one declared mutant.
# Mutants covered: measure:int:0, measure:int:1, measure:const:0, measure:cmp:6, measure:bool:5,
# measure:cmp:9.

import contextlib
import io
import shutil

_xT47HardCoverMeasure_SNAP = b'Remember that the test order is undefined, so your code cannot depend on it.\n'
_xT47HardCoverMeasure_IDX = '`knowledge/a.md` `knowledge/b.md`'
_xT47HardCoverMeasure_EA = 'corpus/knowledge/a.md'
_xT47HardCoverMeasure_EB = 'corpus/knowledge/b.md'
_xT47HardCoverMeasure_NOTE = 'corpus/knowledge/c.md'


def _xT47HardCoverMeasure_lane(files, reg, readme):
    """Create a scratch lane repo at rev `m`; the caller removes the returned directory."""
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    d = tempfile.mkdtemp(prefix='tameshi-r47-hcm-')

    def git(*a):
        out = subprocess.run(['git', '-C', d, *a], env=env, capture_output=True)
        if out.returncode != 0:
            raise RuntimeError('git %s: %s' % (' '.join(a), out.stderr.decode('utf-8', 'replace')))

    def put(p, t):
        full = os.path.join(d, p)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())

    git('init', '-q', '-b', 'm')
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], env=env,
                         capture_output=True).stdout.decode().strip()
    if top != os.path.realpath(d):
        raise RuntimeError('scratch toplevel %r != %r' % (top, os.path.realpath(d)))
    put(SNAP_PREFIX + 'advanced.md', _xT47HardCoverMeasure_SNAP)
    put(SNAP_PREFIX + 'primer.md', _xT47HardCoverMeasure_SNAP)
    put('corpus/SOURCES.md', reg)
    for p, t in files.items():
        put(p, t)
    put('corpus/README.md', readme)
    put(SELF_PATH, open(os.path.abspath(__file__), 'rb').read())
    git('add', '-A')
    git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
    return os.path.realpath(d)


def _xT47HardCoverMeasure_run(lane):
    """Call measure() in process; return (rc, captured stdout, exception name or '')."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = measure(lane, 'm')
    except Exception as exc:
        return None, buf.getvalue(), type(exc).__name__
    return rc, buf.getvalue(), ''


def _xT47HardCoverMeasure_case(name, lane, want_rc, wants, absent=()):
    """Assert the exit code (None = any), the wanted substrings and the forbidden ones."""
    rc, out, exc = _xT47HardCoverMeasure_run(lane)
    if exc:
        print('FAIL %s raised %s' % (name, exc))
        return 1
    summary = (out.strip().splitlines() or [''])[-1]
    ok = ((want_rc is None or rc == want_rc) and all(w in out for w in wants)
          and not any(a in out for a in absent))
    print('%s %s want=%r exit=%r got=%s' % ('PASS' if ok else 'FAIL', name,
                                            (want_rc,) + tuple(wants) + tuple('!' + a for a in absent),
                                            rc, summary))
    return 0 if ok else 1


def extra_T47HardCoverMeasure():
    digest = hashlib.sha256(_xT47HardCoverMeasure_SNAP).hexdigest()[:8]
    both = _xT47HardCoverMeasure_EA + ', ' + _xT47HardCoverMeasure_EB
    reg = (_xHardCover2_row('S256', 'advanced', both, digest)
           + _xHardCover2_row('S257', 'primer', both, digest))
    entry = _xHardCover2_ENTRY
    lanes = []
    failed = 0
    cases = 0
    try:
        # A passing lane: two googletest rows, two indexed entries, plus one knowledge note that
        # cites no row at all (it is refused silently by the pristine guard).
        good = _xT47HardCoverMeasure_lane(
            {_xT47HardCoverMeasure_EA: entry, _xT47HardCoverMeasure_EB: entry,
             _xT47HardCoverMeasure_NOTE: 'plain note, cites nothing\n'},
            reg, _xT47HardCoverMeasure_IDX)
        lanes.append(good)
        # A failing lane: one entry only, both rows and the index valid, so `passed` is false.
        split = _xT47HardCoverMeasure_lane({_xT47HardCoverMeasure_EA: entry}, reg,
                                           '`knowledge/a.md`')
        lanes.append(split)

        # measure:int:0 -> `return 0 if passed else 1` becomes `... 1 if passed else 1`: a passing
        # lane must still exit 0 (the mutant exits 1).
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_exit_zero_on_pass', good, 0,
                                             ('C2_R45_PASS=true',))
        # measure:int:1 -> the failing arm returns 2 instead of 1: a failing lane must exit 1.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_exit_one_on_fail', split, 1,
                                             ('C2_R45_PASS=false',))
        # measure:const:0 -> `tree.read(SELF_PATH, binary=True)` reads text instead of bytes and
        # hashing it raises; the pristine rule pins itself and passes.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_selfpin_binary', good, None,
                                             ('self_pin=1',))
        # measure:cmp:6 -> `why != 'cites no googletest row'` becomes `==`: the silent case (a
        # knowledge file citing no row) must stay silent.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_refused_only_for_other_reasons', good, None,
                                             ('C2_R45_PASS=true',), ('REFUSED ',))
        # measure:bool:5 -> `','.join(sorted(rows)) or '-'` becomes `and`: a non-empty row set
        # must print its ids, not the empty marker.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_row_ids_join', good, None,
                                             ('row_ids=S256,S257',))
        # measure:cmp:9 -> `'' if p in indexed else ' (not indexed)'` becomes `not in`: indexed
        # entries must carry no "(not indexed)" suffix.
        cases += 1
        failed += _xT47HardCoverMeasure_case('T47M_measure_entry_index_suffix', good, None,
                                             ('ENTRY corpus/knowledge/a.md',), ('(not indexed)',))
    finally:
        for d in lanes:
            shutil.rmtree(d, ignore_errors=True)
    return cases, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.lane or not a.rev:
        ap.error('--lane and --rev are required')
    return measure(a.lane, a.rev)


if __name__ == '__main__':
    sys.exit(main())
