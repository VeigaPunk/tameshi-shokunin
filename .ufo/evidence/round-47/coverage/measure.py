#!/usr/bin/env python3
"""Round-47 C3 (coverage) counter: F3 flaky-test measurement ground (prediction, rerun-price and cost documents).

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C3_R47_PASS=true iff self_pin=1 and rows >= 3 and entries >= 3 and indexed == entries
  and covered == rows, where
  * rows    = census-valid registry rows at REV (0-3 leading spaces, 13 cells) with status
              `mined` whose source cell's first URL is one of the three frozen documents
              (arxiv.org/abs/2302.09330; arxiv.org/abs/2607.09345; the Semantic Scholar
              graph record of DOI 10.1109/ICST60714.2024.00037 with the %2C-encoded fields query;
              compared without scheme, `www.`, trailing slash or case), whose anchor cell names a snapshot path under
              .ufo/evidence/round-47/coverage/sources/ that is present at REV together
              with an 8+-hex sha256 prefix of that snapshot's bytes;
  * entries = corpus/knowledge/*.md files at REV whose line 1 is `source:` citing at least
              one such row id, line 2 `verified-at:` with an ISO date >= 2026-10-25, line 3
              `recheck:`, that are listed in a cited row's used-by cell, and that carry at
              least one double-quoted ("..." or curly) quote of 6..25 whitespace tokens found
              in the folded text of a cited row's snapshot AND, when the committed package
              copy .ufo/evidence/round-47/assimilation/package/<same basename> exists, at
              least one such located quote that does not occur in that package copy (an
              entry that only relabels the package entry carries no fresh located quote);
  * indexed = entries whose repo path appears backticked in corpus/README.md at REV
              (`corpus/knowledge/x.md` or `knowledge/x.md`);
  * covered = rows cited on line 1 of at least one admitted entry.
Modes: --lane L --rev R; --selftest.
"""
import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-47/coverage/measure.py'
SNAP_PREFIX = '.ufo/evidence/round-47/coverage/sources/'
PKG_PREFIX = '.ufo/evidence/round-47/assimilation/package/'
DOCS = (
    'arxiv.org/abs/2302.09330',
    'arxiv.org/abs/2607.09345',
    'api.semanticscholar.org/graph/v1/paper/doi:10.1109/icst60714.2024.00037?fields=title%2cabstract%2cyear%2cvenue%2cauthors%2cexternalids',
)
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s;,)]+')
SNAP_RE = re.compile(re.escape(SNAP_PREFIX) + r'[A-Za-z0-9._/-]+')
HEX_RE = re.compile(r'\b[0-9a-f]{8,64}\b')
QUOTE_RE = re.compile(r'"([^"\n]{10,400})"|\u201c([^\u201d\n]{10,400})\u201d')
CITE_RE = re.compile(r'\bS\d{3,}\b')
MIN_VERIFIED = '2026-10-25'
MIN_ROWS = 3
MIN_ENTRIES = 3


def fold(text):
    text = unicodedata.normalize('NFKC', text)
    for a, b in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"'),
                 ('\u2013', '-'), ('\u2014', '-'), ('\u00ad', ''), ('\u00a0', ' '), ('\u200b', '')):
        text = text.replace(a, b)
    return ' '.join(text.split())


def doc_key(url):
    url = re.sub(r'^https?://(www\.)?', '', url.strip()).rstrip('/').lower()
    return url


def norm_text(raw):
    text = raw.decode('utf-8', 'replace')
    if re.search(r'<(html|body|div|p|head)\b', text, re.I):
        text = re.sub(r'(?is)<(script|style)\b.*?</\1\s*>', ' ', text)
        text = re.sub(r'(?s)<[^>]*>', ' ', text)
        text = html.unescape(text)
    return fold(text)


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


def flaky_rows(tree):
    rows = {}
    wanted = {doc_key(d) for d in DOCS}
    for line in (tree.read('corpus/SOURCES.md') or '').splitlines():
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.split('|')]
        if len(cells) != 13 or cells[8] != 'mined':
            continue
        url = URL_RE.search(cells[2])
        if not url or doc_key(url.group(0)) not in wanted:
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
        rows[cells[1]] = dict(text=norm_text(data), used=used, doc=doc_key(url.group(0)))
    return rows


def entry_ok(path, text, rows, package_text):
    lines = text.splitlines()
    if len(lines) < 3 or not lines[0].startswith('source:'):
        return False, 'no provenance trio', []
    cited = [c for c in CITE_RE.findall(lines[0]) if c in rows]
    if not cited:
        return False, 'cites no flaky row', []
    m = re.match(r'verified-at:\s*(\d{4}-\d{2}-\d{2})', lines[1])
    if not m or m.group(1) < MIN_VERIFIED:
        return False, 'verified-at', []
    if not lines[2].startswith('recheck:'):
        return False, 'recheck', []
    cited = [c for c in cited if path in rows[c]['used']]
    if not cited:
        return False, 'not in used-by', []
    fresh = False
    located = False
    for q in QUOTE_RE.finditer(text):
        quote = fold(q.group(1) or q.group(2))
        if 6 <= len(quote.split()) <= 25 and any(quote in rows[c]['text'] for c in cited):
            located = True
            if package_text is None or quote not in fold(package_text):
                fresh = True
    if not located:
        return False, 'no located quote', []
    if not fresh:
        return False, 'no quote fresh against the package copy', []
    return True, 'ok', cited


def measure(lane, rev):
    me = open(os.path.abspath(__file__), 'rb').read()
    tree = Tree(lane, rev)
    blob = tree.read(SELF_PATH, binary=True)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    rows = flaky_rows(tree)
    readme = tree.read('corpus/README.md') or ''
    entries, indexed, covered = [], [], set()
    for path in tree.ls('corpus/knowledge/'):
        if not path.endswith('.md'):
            continue
        package_text = tree.read(PKG_PREFIX + os.path.basename(path))
        ok, why, cited = entry_ok(path, tree.read(path) or '', rows, package_text)
        if ok:
            entries.append(path)
            covered.update(cited)
            if '`%s`' % path in readme or '`%s`' % path[len('corpus/'):] in readme:
                indexed.append(path)
        elif why != 'cites no flaky row':
            print('REFUSED %s %s' % (path, why))
    for p in entries:
        print('ENTRY %s%s' % (p, '' if p in indexed else ' (not indexed)'))
    passed = (self_pin == 1 and len(rows) >= MIN_ROWS and len(entries) >= MIN_ENTRIES
              and len(indexed) == len(entries) and len(covered) == len(rows))
    print('C3_R47: self_pin=%d rows=%d entries=%d indexed=%d covered=%d row_ids=%s rev=%s C3_R47_PASS=%s' % (
        self_pin, len(rows), len(entries), len(indexed), len(covered), ','.join(sorted(rows)) or '-',
        rev, 'true' if passed else 'false'))
    return 0 if passed else 1


def selftest():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    me = os.path.abspath(__file__)
    snaps = {
        'a': b'<html><body><p>Flaky tests belong to a cluster, so the reruns are not independent observations of the suite.</p>'
             b'<p>A second sentence says the cause is shared across the members of one cluster.</p></body></html>',
        'b': b'<html><body><p>Undetected flaky failures account for a share of failed pipeline runs in the projects.</p>'
             b'<p>Another sentence states that environments change flake rates between pipelines.</p></body></html>',
        'c': b'{"entry":{"content":{"$t":"About a fraction of the transitions we observe from pass to fail involve a flaky test here. '
             b"And it is quite common to ignore legitimate failures in flaky tests today.\"}}}",
    }
    urls = ['https://' + DOCS[0], 'https://' + DOCS[1] + '/', 'https://' + DOCS[2]]
    names = {'a': 'arxiv.html', 'b': 'tum.html', 'c': 'feed.json'}
    ids = {'a': 'S258', 'b': 'S259', 'c': 'S260'}
    quote = {'a': 'Flaky tests belong to a cluster, so the reruns are not independent observations of the suite',
             'b': 'Undetected flaky failures account for a share of failed pipeline runs in the projects',
             'c': 'it is quite common to ignore legitimate failures in flaky tests today'}
    fresh_q = {'a': 'the cause is shared across the members of one cluster',
               'b': 'environments change flake rates between pipelines',
               'c': 'About a fraction of the transitions we observe from pass to fail involve a flaky test'}
    entry_paths = {k: 'corpus/knowledge/e-%s.md' % k for k in 'abc'}
    results = []
    with tempfile.TemporaryDirectory(prefix='tameshi-r47-c3-') as d:
        def git(*a):
            subprocess.run(['git', '-C', d, *a], env=env, capture_output=True, check=True)

        def put(p, t):
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, 'wb').write(t if isinstance(t, bytes) else t.encode())

        git('init', '-q', '-b', 'm')
        assert subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True,
                              env=env).stdout.decode().strip() == os.path.realpath(d)

        def sha(k):
            return hashlib.sha256(snaps[k]).hexdigest()[:8]

        def row(k, used, url=None, h=None, status='mined', prefix=SNAP_PREFIX, indent=''):
            return ('%s| %s | t — %s | paper | A | s | %s%s %s | t | %s | 2026-10-25 | 365d | %s |\n'
                    % (indent, ids[k], url or urls['abc'.index(k)], prefix, names[k], h or sha(k), status, used))

        def entry(k, qs=None, head=None):
            qs = qs if qs is not None else [quote[k], fresh_q[k]]
            h = head or ['source: %s — upstream' % ids[k], 'verified-at: 2026-10-25', 'recheck: 365d']
            return '\n'.join(h) + '\n\n' + ' '.join('Upstream says "%s".' % q for q in qs) + '\n'

        def pkg(k):
            return 'source: S190 — upstream\nverified-at: 2026-10-23\nrecheck: 365d\n\nUpstream says "%s".\n' % quote[k]

        def build(reg, entries, readme, packages=None, snapshots=None, selfbytes=None):
            for p in list(entry_paths.values()):
                full = os.path.join(d, p)
                if os.path.exists(full):
                    os.remove(full)
            for k in 'abc':
                full = os.path.join(d, PKG_PREFIX + os.path.basename(entry_paths[k]))
                if os.path.exists(full):
                    os.remove(full)
            for k, v in (snapshots if snapshots is not None else snaps).items():
                put(SNAP_PREFIX + names[k], v)
            put('corpus/SOURCES.md', reg)
            for p, t in entries.items():
                put(p, t)
            for p, t in (packages or {}).items():
                put(PKG_PREFIX + os.path.basename(p), t)
            put('corpus/README.md', readme)
            put(SELF_PATH, selfbytes if selfbytes is not None else open(me, 'rb').read())
            git('add', '-A')
            git('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'x', '--allow-empty')
            out = subprocess.run([sys.executable, me, '--lane', d, '--rev', 'm'], capture_output=True, text=True)
            lines = out.stdout.strip().splitlines()
            return lines[-1] if lines else 'NO-OUTPUT ' + out.stderr[-200:]

        ea, eb, ec = (entry_paths[k] for k in 'abc')
        all_used = ', '.join((ea, eb, ec))
        good_reg = ''.join(row(k, entry_paths[k]) for k in 'abc')
        good_entries = {entry_paths[k]: entry(k) for k in 'abc'}
        idx = '`knowledge/e-a.md` `knowledge/e-b.md` `knowledge/e-c.md`'
        pkgs = {entry_paths[k]: pkg(k) for k in 'abc'}
        e_prov = lambda k, line1=None, line2=None, line3=None: entry(k, head=[
            line1 or 'source: %s — upstream' % ids[k], line2 or 'verified-at: 2026-10-25', line3 or 'recheck: 365d'])
        cases = [
            ('T01_three_pass', good_reg, good_entries, idx, {}, 'C3_R47_PASS=true'),
            ('T02_rows_only', good_reg, {p: 'x\n' for p in entry_paths.values()}, idx, {}, 'entries=0'),
            ('T03_old_verified_at', good_reg, dict(good_entries, **{ea: e_prov('a', line2='verified-at: 2026-10-24')}),
             idx, {}, 'entries=2'),
            ('T04_quote_absent', good_reg, dict(good_entries, **{ea: entry('a', qs=['Flaky tests never belong to any cluster at all so reruns are independent'])}),
             idx, {}, 'entries=2'),
            ('T05_not_in_used_by', ''.join(row(k, entry_paths['b']) for k in 'abc'), good_entries, idx, {}, 'entries=1'),
            ('T06_bad_sha_prefix', row('a', ea, h='deadbeef') + row('b', eb) + row('c', ec), good_entries, idx, {}, 'rows=2'),
            ('T07_not_indexed', good_reg, good_entries, '`knowledge/e-a.md` `knowledge/e-b.md`', {}, 'indexed=2'),
            ('T08_queued_rows', ''.join(row(k, entry_paths[k], status='queued') for k in 'abc'), good_entries, idx, {}, 'rows=0'),
            ('T09_unlisted_url', row('a', ea, url='https://arxiv.org/abs/2504.16778') + row('b', eb) + row('c', ec),
             good_entries, idx, {}, 'rows=2'),
            ('T10_indented_row_counts', row('a', ea, indent='  ') + row('b', eb, indent='   ') + row('c', ec), good_entries, idx, {}, 'rows=3'),
            ('T11_four_space_row_ignored', row('a', ea, indent='    ') + row('b', eb) + row('c', ec), good_entries, idx, {}, 'rows=2'),
            ('T12_wrong_round_prefix', ''.join(row(k, entry_paths[k], prefix=SNAP_PREFIX.replace('round-47', 'round-45')) for k in 'abc'),
             good_entries, idx, {}, 'rows=0'),
            ('T13_missing_snapshot_empty_digest', ''.join(row(k, entry_paths[k], h='e3b0c442') for k in 'abc'),
             good_entries, idx, {'snapshots': {}}, 'rows=0'),
            ('T14_no_source_prefix', good_reg, dict(good_entries, **{ea: e_prov('a', line1='S258 — upstream')}), idx, {}, 'entries=2'),
            ('T15_no_recheck', good_reg, dict(good_entries, **{ea: e_prov('a', line3='checked: 365d')}), idx, {}, 'entries=2'),
            ('T16_fullpath_index_form', good_reg, good_entries,
             '`corpus/knowledge/e-a.md` `corpus/knowledge/e-b.md` `corpus/knowledge/e-c.md`', {}, 'indexed=3'),
            ('T17_two_entries_is_false', good_reg, {ea: good_entries[ea], eb: good_entries[eb]}, idx, {}, 'C3_R47_PASS=false'),
            ('T18_two_rows_is_false', row('a', ea) + row('b', eb), good_entries, idx, {}, 'C3_R47_PASS=false'),
            ('T19_unindexed_is_false', good_reg, good_entries, '`knowledge/e-a.md` `knowledge/e-b.md`', {}, 'C3_R47_PASS=false'),
            ('T20_self_pin_broken', good_reg, good_entries, idx, {'selfbytes': b'#!/usr/bin/env python3\n# not the counter\n'}, 'C3_R47_PASS=false'),
            ('T21_relabelled_package_entry', good_reg,
             dict(good_entries, **{ea: entry('a', qs=[quote['a']])}), idx, {'packages': pkgs}, 'entries=2'),
            ('T22_fresh_quote_passes', good_reg, good_entries, idx, {'packages': pkgs}, 'C3_R47_PASS=true'),
            ('T23_row_cited_by_no_entry', good_reg,
             {ea: good_entries[ea], eb: good_entries[eb], ec: entry('a', qs=[quote['a'], fresh_q['a']]).replace('S258', 'S258')},
             idx, {}, 'covered=2'),
            ('T24_two_entries_one_row_is_false', good_reg,
             {ea: good_entries[ea], eb: entry('a', qs=[quote['a'], fresh_q['a']]), ec: entry('a', qs=[quote['a'], fresh_q['a']])},
             '`knowledge/e-a.md` `knowledge/e-b.md` `knowledge/e-c.md`', {}, 'C3_R47_PASS=false'),
        ]
        # T23/T24 entries cite S258 but sit at other paths: rows list them as used-by only for their own file,
        # so fix used-by to include the entry path the case writes.
        failed = 0
        for name, reg, ents, readme, extra, want in cases:
            if name in ('T23_row_cited_by_no_entry', 'T24_two_entries_one_row_is_false'):
                reg = row('a', ', '.join((ea, eb, ec))) + row('b', eb) + row('c', ec)
                if name == 'T23_row_cited_by_no_entry':
                    reg = row('a', ', '.join((ea, ec))) + row('b', eb) + row('c', ec)
                    ents = {ea: good_entries[ea], eb: good_entries[eb], ec: entry('a', qs=[quote['a'], fresh_q['a']])}
            line = build(reg, ents, readme, **extra)
            ok = want in line
            failed += not ok
            print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, want, line))
    print('C3_R47_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


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
