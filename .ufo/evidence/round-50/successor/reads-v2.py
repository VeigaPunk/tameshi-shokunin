#!/usr/bin/env python3
r"""Round-50 successor read counter -- C1 routed defect R49.2 (first half): the read-row check, repaired.

This is NOT the round-50 C1 counter (the L1 owns `.ufo/evidence/round-50/c1/measure.py`). It is the
wave-1 successor instrument for `.ufo/evidence/round-49/c1/measure.py` (never edited), against the
findings `.ufo/waves/round-49/w1/T49CritC1Contract.md` F1-F6 and `corpus/lessons/round-49.md:108-114`.

The check it keeps (round 49, unchanged): in each of the seven SKILL.md sections (heading text pinned
in TARGETS, each exactly once) every extracted pointer must resolve at REV, have exactly one row in
the reads doc keyed (heading, ordinal, raw) with the same file and ranges, verdict `holds`, and an
excerpt (whitespace-collapsed, 24-400 chars) that occurs in the whitespace-collapsed pointed text.
Extractor order per section is unchanged -- line pointers, path pointers, S-ids, and then the three
forms below, so legacy ordinals never move.

Three rules added, each a term in `total` (0 = pass):

R1 `absent_evidence` (F1/F2/F5 -- `absent` was uncapped, evidence-free, and unscored). A path
   pointer that does not resolve passes only with `absent_evidence` = {path, history, not_a_file}:
     * `path` equals the raw token;
     * `history` equals `git log --all --format=%H -- <path>` (lane repo) and that list is empty --
       the path never existed anywhere in the repository's history;
     * `not_a_file` is a 15-400 char whitespace-collapsed quote that occurs in the section text,
       contains the raw token, and carries a not-a-file marker (NOT_A_FILE_RE: "not a file",
       "placeholder", "not in-tree", "unversioned", "never existed", "naming convention", ...);
     * at most 1 evidenced `absent` row per section. Every other absent claim scores
       `absent_bad` (no/invalid evidence) and each claim past the first scores `absent_overflow`.

R2 missed citation forms (F4 -- the extractor never saw `§` refs, `#anchor` pointers or globs):
     * section pointer `§N` / `§N-§M` / `§N–§M`: token = nearest preceding file token in the same
       paragraph (a table row is its own paragraph); region = the block of each numbered heading
       (`^#{1,6} N[.)]`) in that file, heading line through the line before the next same-or-higher
       heading;
     * anchor pointer `FILE#frag`: the file's heading whose slug equals `frag` or starts `frag-`;
       region = that heading's block;
     * glob pointer `dir/prefix-*.ext`: expansion at REV (`git ls-tree -r` + fnmatch) must equal the
       row's `files` list exactly, so a tenth case file cannot pass unnoticed;
     * each needs a read row under the R0 rules (glob rows carry `files` and an excerpt from the
       section text instead of a file/ranges/excerpt triple).

R3 trace with zero inputs (F6 -- an empty-`inputs` receipt satisfied the trace gate). Every trace
   receipt -- a `tameshi-trace-inputs-v1` JSON, a doc with a `receipts` list, or a directory of
   receipts -- must record at least one input; an empty-input receipt scores `trace_empty`, an empty
   receipt set scores `trace_missing`, and measure() refuses to run without a trace argument.

Usage:
  python3 reads-v2.py --lane LANE --rev REV --trace PATH [--trace PATH ...]
                      [--reads PATH] [--headings JSON] [--floors JSON] [--fleet FLEET] [--list]
  python3 reads-v2.py --selftest

Exit: 0 pass, 1 measured not-pass, 2 setup error, 64 usage.
"""
import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True

# The seven sections of round 49 (heading text at REV, each exactly once).
TARGETS = (
    '## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence',
    '## Restore discipline \u2014 before/after identity, not continuous non-write proof',
    '### The map \u2014 where a reader enters, artifact by artifact',
    '## Promotion-evidence calibration \u2014 fleet round-1',
    '## Repeated controls and gate registry \u2014 round 12',
    '## Pin disposition and provenance correction \u2014 round 13',
    '## Effective expectation reconciliation \u2014 round 14',
)
READS_DEFAULT = '.ufo/evidence/round-49/c1/reads.json'
EXCERPT_MIN, EXCERPT_MAX = 24, 400
QUOTE_MIN, QUOTE_MAX = 15, 400

EXT = r'(?:md|py|sh|json|mjs|txt|xml|html)'
FILE_RE = r'(?:\.\./)?(?:[\w.-]+/)*\w[\w.-]*\.' + EXT
RANGE = r'\d+(?:[-\u2013]\d+)?'
CONT = r'(?:,\s*:?' + RANGE + r')*'
# Transcribed from round-49 measure.py (frozen): the legacy extractor grammar.
PTR_RE = re.compile(r'(?<![\w/.-])(?P<file>' + FILE_RE + r'):(?P<ranges>' + RANGE + CONT + r')'
                    r'|(?<![\w:./-]):(?P<bare>' + RANGE + CONT + r')')
PATH_RE = re.compile(r'(?<![\w/.-])(' + FILE_RE + r')(?![\w.-]|:\d)')
SID_RE = re.compile(r'(?<![\w])S\d{3,}(?!\d)')
# R2 forms.
SEC_RE = re.compile(r'\u00a7\s*(\d+)(?:\s*[-\u2013]\s*\u00a7?\s*(\d+))?')
ANCHOR_RE = re.compile(r'(?<![\w/.-])(' + FILE_RE + r')#([A-Za-z0-9][\w.-]*)')
GLOB_RE = re.compile(r'(?<![\w/.-])((?:[\w.-]+/)*[\w.-]*\*[\w.-]*\.' + EXT + r')(?![\w.-])')
# Numbered heading and any heading, for R2 regions; block boundaries.
NUMHEAD_RE = re.compile(r'^#{1,6}\s*(\d+)[.)]?(?:\s|$)')
ANYHEAD_RE = re.compile(r'^(#{1,6})\s')
# R1 not-a-file markers.
NOT_A_FILE_RE = re.compile(r'(?i)(not a file|not a path|not held|never existed|does not exist'
                           r'|no such file|not in-tree|unversioned|placeholder|naming convention'
                           r'|not an artifact)')
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
GIT_ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
COMMIT_ENV = dict(GIT_ENV, GIT_AUTHOR_NAME='r50-fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
                  GIT_COMMITTER_NAME='r50-fixture', GIT_COMMITTER_EMAIL='fixture@invalid',
                  GIT_AUTHOR_DATE='2026-10-26T00:00:00Z', GIT_COMMITTER_DATE='2026-10-26T00:00:00Z')


class Setup(Exception):
    pass


def git(repo, *args, data=None, env=None):
    return subprocess.run(['git', '-C', repo] + list(args), input=data, capture_output=True,
                          env=env or GIT_ENV)


def blob(repo, rev, path):
    r = git(repo, 'cat-file', 'blob', '%s:%s' % (rev, path))
    return r.stdout if r.returncode == 0 else None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def parse_ranges(text):
    out = []
    for part in re.split(r',\s*:?', text):
        s, _, e = part.replace('\u2013', '-').partition('-')
        out.append([int(s), int(e or s)])
    return out


def paragraphs(lines):
    """Yield lists of (lineno_offset, line) paragraphs; a table row is its own paragraph."""
    cur = []
    for i, line in enumerate(lines):
        if line.strip() == '':
            if cur:
                yield cur
            cur = []
        elif line.lstrip().startswith('|'):
            if cur:
                yield cur
            cur = []
            yield [(i, line)]
        else:
            cur.append((i, line))
    if cur:
        yield cur


def extract_legacy(section_text):
    """Round-49 extractor, transcribed: line pointers, then path pointers, then S-ids."""
    lines = section_text.split('\n')
    out = []
    paths, sids = [], []
    for para in paragraphs(lines):
        last = None
        for off, line in para:
            for m in PTR_RE.finditer(line):
                if m.group('file'):
                    token, rtext, raw = m.group('file'), m.group('ranges'), m.group(0)
                    last = token
                else:
                    token, rtext, raw = last, m.group('bare'), m.group(0)
                out.append({'ordinal': len(out), 'raw': raw, 'token': token, 'kind': 'line',
                            'ranges': parse_ranges(rtext), 'line': off})
            for m in PATH_RE.finditer(line):
                if m.group(1) not in [p[0] for p in paths]:
                    paths.append((m.group(1), off))
            for m in SID_RE.finditer(line):
                if m.group(0) not in [s[0] for s in sids]:
                    sids.append((m.group(0), off))
    for token, off in paths:
        out.append({'ordinal': len(out), 'raw': token, 'token': token, 'kind': 'path', 'ranges': None,
                    'line': off})
    for token, off in sids:
        out.append({'ordinal': len(out), 'raw': token, 'token': token, 'kind': 'sid', 'ranges': None,
                    'line': off})
    return out


def file_tokens(line):
    """File tokens on a line, with offsets: line-pointer FILE plus path-pointer FILE."""
    toks = []
    for m in PTR_RE.finditer(line):
        if m.group('file'):
            toks.append((m.start(), m.group('file')))
    for m in PATH_RE.finditer(line):
        toks.append((m.start(), m.group(1)))
    toks.sort()
    return toks


def extract_forms(section_text):
    """R2 forms: section refs (each occurrence), anchors (each occurrence), globs (one per token)."""
    lines = section_text.split('\n')
    secs, anchors, globs = [], [], []
    seen_anchor, seen_glob = set(), set()
    for para in paragraphs(lines):
        last = None
        for off, line in para:
            toks = file_tokens(line)

            def inherit(pos, toks=toks, last=last):
                cand = None
                for at, tok in toks:
                    if at < pos:
                        cand = tok
                return cand if cand is not None else last

            for m in SEC_RE.finditer(line):
                start, _, end = m.group(1), None, m.group(2)
                secs.append({'raw': m.group(0), 'token': inherit(m.start()), 'line': off,
                             'numbers': [[int(start), int(end or start)]]})
            for m in ANCHOR_RE.finditer(line):
                key = (m.group(0), off)
                if key in seen_anchor:
                    continue
                seen_anchor.add(key)
                anchors.append({'raw': m.group(0), 'token': m.group(1), 'fragment': m.group(2),
                                'line': off})
            for m in GLOB_RE.finditer(line):
                if m.group(1) in seen_glob:
                    continue
                seen_glob.add(m.group(1))
                globs.append({'raw': m.group(1), 'token': m.group(1), 'line': off})
            for _, tok in toks:
                last = tok
    return secs, anchors, globs


def extract_v2(section_text):
    out = extract_legacy(section_text)
    secs, anchors, globs = extract_forms(section_text)
    for p in secs:
        out.append({'ordinal': len(out), 'raw': p['raw'], 'token': p['token'], 'kind': 'section',
                    'ranges': None, 'numbers': p['numbers'], 'line': p['line']})
    for p in anchors:
        out.append({'ordinal': len(out), 'raw': p['raw'], 'token': p['token'], 'kind': 'anchor',
                    'ranges': None, 'fragment': p['fragment'], 'line': p['line']})
    for p in globs:
        out.append({'ordinal': len(out), 'raw': p['raw'], 'token': p['token'], 'kind': 'glob',
                    'ranges': None, 'line': p['line']})
    return out


def resolve(repo, rev, token, kind='line'):
    """Round-49 resolver, transcribed: lane roots for line/path/sid; '../' is external."""
    if token is None:
        return None, None, None
    if kind == 'sid':
        reg = blob(repo, rev, 'corpus/SOURCES.md')
        if reg is None:
            return None, None, None
        rows = [i for i, ln in enumerate(reg.decode('utf-8', 'surrogateescape').split('\n'), 1)
                if re.match(r'^ {0,3}\|\s*' + token + r'\s*\|', ln)]
        if len(rows) != 1:
            return None, None, None
        return 'corpus/SOURCES.md', 'sid', [[rows[0], rows[0]]]
    if token.startswith('../'):
        return token, ('external' if kind == 'line' else 'external-path'), None
    for cand in (token, 'corpus/knowledge/' + token, 'corpus/' + token, 'corpus/lessons/' + token):
        t = git(repo, 'cat-file', '-t', '%s:%s' % (rev, cand))
        if t.returncode == 0 and t.stdout.strip() == b'blob':
            return cand, kind, None
    return None, None, None


def line_count(data):
    lines = data.split(b'\n')
    if lines and lines[-1] == b'':
        lines.pop()
    return len(lines)


def pointed_text(data, ranges):
    lines = data.decode('utf-8', 'surrogateescape').split('\n')
    return norm('\n'.join('\n'.join(lines[s - 1:e]) for s, e in ranges))


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def block_range(lines, idx):
    """Heading line idx (0-based) through the line before the next same-or-higher heading."""
    m = ANYHEAD_RE.match(lines[idx])
    level = len(m.group(1)) if m else 6
    end = len(lines)
    for j in range(idx + 1, len(lines)):
        mm = ANYHEAD_RE.match(lines[j])
        if mm and len(mm.group(1)) <= level:
            end = j
            break
    while end > idx + 1 and lines[end - 1].strip() == '':
        end -= 1
    return [idx + 1, end]


def text_lines(data):
    lines = data.decode('utf-8', 'surrogateescape').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return lines


def section_ranges(data, numbers):
    """R2 region for §N refs: the block of each numbered heading; None if a number is not unique."""
    lines = text_lines(data)
    idx = {}
    for i, line in enumerate(lines):
        m = NUMHEAD_RE.match(line)
        if m:
            idx.setdefault(int(m.group(1)), []).append(i)
    out = []
    for start, end in numbers:
        for n in range(start, end + 1):
            hits = idx.get(n, [])
            if len(hits) != 1:
                return None
            out.append(block_range(lines, hits[0]))
    return out


def anchor_ranges(data, fragment):
    """R2 region for FILE#frag: the block of the heading whose slug is frag or starts frag-."""
    lines = text_lines(data)
    for i, line in enumerate(lines):
        m = ANYHEAD_RE.match(line)
        if not m:
            continue
        s = slug(line[len(m.group(1)):].strip())
        if s == fragment or s.startswith(fragment + '-'):
            return [block_range(lines, i)]
    return None


def glob_files(lane, rev, pattern):
    """R2 expansion of a wildcard path at REV (sorted); None when the pattern is external."""
    if pattern.startswith('../'):
        return None
    d = os.path.dirname(pattern) or '.'
    r = git(lane, 'ls-tree', '-r', '--name-only', rev, '--', d)
    if r.returncode != 0:
        return None
    return sorted(p for p in r.stdout.decode('utf-8', 'surrogateescape').split('\n')
                  if p and fnmatch.fnmatchcase(p, pattern))


def sectionize(raw):
    """Mirror of .ufo/evidence/round-18/measure.py sectionize (headings ^#{1,3}, fences respected)."""
    lines = raw.decode('utf-8', 'surrogateescape').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    head_re = re.compile(r'^#{1,3}(?:\s|$)')
    heads = []
    in_fence = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence and head_re.match(line):
            heads.append(i)
    pairs = []
    if heads:
        if heads[0] > 0:
            pairs.append((0, heads[0]))
        for s, e in zip(heads, heads[1:] + [len(lines)]):
            pairs.append((s, e))
    else:
        pairs.append((0, len(lines)))
    head_set = set(heads)
    sections = []
    for s, e in pairs:
        body = list(lines[s:e])
        while body and body[-1].strip() == '':
            body.pop()
        sections.append({'start': s + 1, 'end': e, 'heading': lines[s] if s in head_set else '',
                         'text': '\n'.join(body)})
    return sections


def target_sections(lane, rev, headings=TARGETS):
    raw = blob(lane, rev, 'SKILL.md')
    if raw is None:
        raise Setup('SKILL.md missing at REV')
    secs = sectionize(raw)
    lines = raw.decode('utf-8', 'surrogateescape').split('\n')
    found, counts = {}, {}
    for s in secs:
        counts[s['heading']] = counts.get(s['heading'], 0) + 1
        if s['heading'] in headings:
            body = list(lines[s['start'] - 1:s['end']])
            while body and body[-1].strip() == '':
                body.pop()
            found[s['heading']] = {'start': s['start'], 'end': s['end'],
                                   'sha256': sha('\n'.join(body).encode('utf-8', 'surrogateescape')),
                                   'text': '\n'.join(body)}
    missing = [h for h in headings if counts.get(h, 0) != 1]
    return found, missing


def load_region(lane, rev, fleet, token, kind, row, cache):
    """Blob for a resolved token: lane at REV, or the fleet repo at the row's fleet_commit."""
    data = None
    if kind in ('external', 'external-path'):
        fc = row.get('fleet_commit') if row else None
        if not (isinstance(fc, str) and re.fullmatch(r'[0-9a-f]{40}', fc)):
            return None
        key = ('ext', fc, token)
        if key not in cache:
            cache[key] = blob(fleet, fc, token[3:])
        data = cache[key]
    else:
        key = ('lane', token)
        if key not in cache:
            cache[key] = blob(lane, rev, token)
        data = cache[key]
    return data


def resolve_pointer(lane, rev, fleet, p, row, cache):
    """Return {file, kind, ranges, files, data} for a pointer (R2 forms included)."""
    kind = p['pointer_kind']
    if kind in ('line', 'path', 'sid'):
        f, rkind, rr = resolve(lane, rev, p['token'], kind)
        ranges = p['ranges'] if kind == 'line' else rr
        data = load_region(lane, rev, fleet, f, rkind, row, cache) if f is not None else None
        return {'file': f, 'kind': rkind, 'ranges': ranges, 'files': None, 'data': data}
    if kind == 'glob':
        files = glob_files(lane, rev, p['token'])
        return {'file': None, 'kind': 'glob', 'ranges': None, 'files': files, 'data': None}
    token = p['token']
    if token is None:
        return {'file': None, 'kind': None, 'ranges': None, 'files': None, 'data': None}
    f, rkind, _ = resolve(lane, rev, token, 'path')
    if f is None:
        return {'file': None, 'kind': None, 'ranges': None, 'files': None, 'data': None}
    data = load_region(lane, rev, fleet, f, rkind, row, cache)
    if data is None:
        return {'file': None, 'kind': rkind, 'ranges': None, 'files': None, 'data': None}
    if kind == 'section':
        ranges = section_ranges(data, p['numbers'])
    else:
        ranges = anchor_ranges(data, p['fragment'])
    return {'file': f, 'kind': rkind, 'ranges': ranges, 'files': None, 'data': data}


def absent_reason(lane, p, row, section_text):
    """R1: None when the absent row's evidence holds, else the failing clause."""
    ev = row.get('absent_evidence')
    if not isinstance(ev, dict):
        return 'no-evidence'
    if ev.get('path') != p['raw']:
        return 'path-mismatch'
    hist = [h for h in git(lane, 'log', '--all', '--format=%H', '--', p['raw'])
            .stdout.decode('utf-8', 'surrogateescape').split('\n') if h]
    if ev.get('history') != hist:
        return 'history-unrecorded'
    if hist:
        return 'history-nonempty'
    quote = ev.get('not_a_file')
    if not isinstance(quote, str):
        return 'no-quote'
    q = norm(quote)
    if not (QUOTE_MIN <= len(q) <= QUOTE_MAX):
        return 'quote-length'
    if p['raw'] not in q:
        return 'quote-token-missing'
    if not NOT_A_FILE_RE.search(q):
        return 'quote-not-a-file'
    if q not in norm(section_text):
        return 'quote-not-in-section'
    return None


def row_excerpt(row):
    ex = row.get('excerpt') if row else None
    return norm(ex) if isinstance(ex, str) else ''


def check_reads(lane, rev, fleet, pointers, reads_doc, texts):
    rows = reads_doc.get('rows') if isinstance(reads_doc, dict) else None
    rows = [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []
    index = {}
    for r in rows:
        index.setdefault((r.get('heading'), r.get('ordinal'), r.get('raw')), []).append(r)
    res = {'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 0, 'absent': 0,
           'absent_bad': 0, 'absent_overflow': 0, 'glob_mismatch': 0}
    forms = {}
    detail = []
    claims = {}
    cache = {}
    for p in pointers:
        kind = p['pointer_kind']
        st = forms.setdefault(kind, {'pointers': 0, 'rows': 0, 'ok': 0})
        st['pointers'] += 1
        hits = index.get((p['heading'], p['ordinal'], p['raw']), [])
        row = hits[0] if len(hits) == 1 else None
        if row is not None:
            st['rows'] += 1
        status, why, info = 'ok', '', None
        if len(hits) > 1:
            status, why = 'unverified', 'duplicate-rows'
        else:
            info = resolve_pointer(lane, rev, fleet, p, row, cache)
            if kind in ('section', 'anchor'):
                if info['file'] is None or info['ranges'] is None:
                    status, why = 'unresolved', 'region'
                elif row is None or row.get('file') != info['file'] \
                        or row.get('ranges') != info['ranges']:
                    status, why = 'unverified', 'row'
                elif row.get('verdict') != 'holds':
                    status, why = 'not_holds', str(row.get('verdict'))
                else:
                    ex = row_excerpt(row)
                    if not (EXCERPT_MIN <= len(ex) <= EXCERPT_MAX) or \
                            ex not in pointed_text(info['data'], info['ranges']):
                        status, why = 'excerpt_miss', 'excerpt'
            elif kind == 'glob':
                if not info['files']:
                    status, why = 'unresolved', 'glob-empty'
                elif row is None:
                    status, why = 'unverified', 'row'
                elif row.get('verdict') != 'holds':
                    status, why = 'not_holds', str(row.get('verdict'))
                elif row.get('files') != info['files']:
                    status, why = 'glob_mismatch', 'files'
                else:
                    ex = row_excerpt(row)
                    if not (EXCERPT_MIN <= len(ex) <= EXCERPT_MAX) or \
                            ex not in norm(texts.get(p['heading'], '')):
                        status, why = 'excerpt_miss', 'excerpt'
            elif info['file'] is None:
                if kind == 'path' and row is not None and row.get('verdict') == 'absent' \
                        and row.get('file') is None:
                    claims[p['heading']] = claims.get(p['heading'], 0) + 1
                    bad = absent_reason(lane, p, row, texts.get(p['heading'], ''))
                    if bad is None:
                        res['absent'] += 1
                        status, why = None, 'absent-evidenced'
                    else:
                        res['absent_bad'] += 1
                        status, why = None, 'absent:%s' % bad
                else:
                    status, why = 'unresolved', 'file'
            else:
                if info['data'] is None:
                    status, why = 'unresolved', 'blob'
                elif info['ranges'] is not None:
                    n = line_count(info['data'])
                    if not all(1 <= s <= e <= n for s, e in info['ranges']):
                        status, why = 'unresolved', 'range'
                if status == 'ok':
                    if row is None or row.get('file') != info['file'] \
                            or row.get('ranges') != info['ranges']:
                        status, why = 'unverified', 'row'
                    elif row.get('verdict') != 'holds':
                        status, why = 'not_holds', str(row.get('verdict'))
                    else:
                        where = pointed_text(info['data'], info['ranges']) if \
                            info['ranges'] is not None else \
                            norm(info['data'].decode('utf-8', 'surrogateescape'))
                        ex = row_excerpt(row)
                        if not (EXCERPT_MIN <= len(ex) <= EXCERPT_MAX) or ex not in where:
                            status, why = 'excerpt_miss', 'excerpt'
        if status == 'ok':
            st['ok'] += 1
            detail.append((p, 'ok', info))
        elif status is None:
            detail.append((p, why, info))
        else:
            res[status] += 1
            detail.append((p, status, info))
    res['absent_overflow'] = sum(max(0, n - 1) for n in claims.values())
    return res, detail, forms


def load_receipts(lane, rev, path):
    """Receipts at REV under a trace path: a blob (receipt doc) or a tree (directory of receipts)."""
    t = git(lane, 'cat-file', '-t', '%s:%s' % (rev, path)).stdout.strip()
    if t == b'blob':
        raw = blob(lane, rev, path)
        try:
            doc = json.loads(raw)
        except ValueError:
            return [{'schema': None, 'inputs': None, 'path': path}]
        if isinstance(doc, dict) and isinstance(doc.get('receipts'), list):
            return [dict(r, path=path) if isinstance(r, dict) else {'inputs': r, 'path': path}
                    for r in doc['receipts']]
        if isinstance(doc, list):
            return [dict(r, path=path) if isinstance(r, dict) else {'inputs': r, 'path': path}
                    for r in doc]
        return [dict(doc, path=path)]
    if t == b'tree':
        out = []
        names = git(lane, 'ls-tree', '-r', '--name-only', rev, '--', path)
        for name in names.stdout.decode('utf-8', 'surrogateescape').split('\n'):
            if name.endswith('.json'):
                out.extend(load_receipts(lane, rev, name))
        return out
    return []


def check_traces(lane, rev, paths):
    res = {'receipts': 0, 'ok': 0, 'empty': 0, 'missing': 0}
    detail = []
    for path in paths:
        receipts = load_receipts(lane, rev, path)
        if not receipts:
            res['missing'] += 1
            detail.append('%s: no-receipts' % path)
            continue
        for r in receipts:
            res['receipts'] += 1
            inputs = r.get('inputs') if isinstance(r, dict) else None
            if isinstance(inputs, dict) and len(inputs) >= 1:
                res['ok'] += 1
            else:
                res['empty'] += 1
                detail.append('%s: empty-inputs' % (r.get('path', path) if isinstance(r, dict)
                                                    else path))
    return res, detail


def measure(lane, rev, traces, reads=READS_DEFAULT, headings=TARGETS, floors=None, fleet=None,
            quiet=False):
    """The whole read-row check at REV. Returns the term dict; prints the deciding-style line."""
    fleet = os.path.realpath(fleet or os.path.dirname(lane))
    found, missing = target_sections(lane, rev, headings)
    pointers = []
    for h in headings:
        if h not in found:
            continue
        for p in extract_v2(found[h]['text']):
            p['heading'] = h
            p['pointer_kind'] = p['kind']
            pointers.append(p)
    counts = {h: 0 for h in headings}
    for p in pointers:
        counts[p['heading']] += 1
    floor_short = 0
    if floors:
        floor_short = sum(1 for h in headings
                          if h not in missing and counts[h] < int(floors.get(h, 0)))
    raw = blob(lane, rev, reads)
    if raw is None:
        raise Setup('reads doc missing at REV: %s' % reads)
    try:
        reads_doc = json.loads(raw)
    except ValueError:
        reads_doc = {}
    texts = {h: found[h]['text'] for h in found}
    res, detail, forms = check_reads(lane, rev, fleet, pointers, reads_doc, texts)
    tres, tdetail = check_traces(lane, rev, traces)
    total = (len(missing) + floor_short + res['unresolved'] + res['unverified'] +
             res['excerpt_miss'] + res['not_holds'] + res['absent_bad'] +
             res['absent_overflow'] + res['glob_mismatch'] + tres['empty'] + tres['missing'])
    if not quiet:
        for p, label, info in detail:
            if label in ('ok', 'absent-evidenced'):
                continue
            where = ''
            if info and info.get('file'):
                where = '%s %s' % (info['file'], info['ranges'] if info['ranges'] is not None
                                   else '')
            elif info and info.get('files') is not None:
                where = 'files=%d' % len(info['files'])
            print('PTR [%s] %s #%d %s -> %s %s' % (p['pointer_kind'], p['heading'][:34],
                                                   p['ordinal'], p['raw'], where.strip(), label))
        for line in tdetail:
            print('TRACE %s' % line)
        for kind in ('line', 'path', 'sid', 'section', 'anchor', 'glob'):
            if kind in forms:
                print('FORM %s: pointers=%d rows=%d ok=%d' % (kind, forms[kind]['pointers'],
                                                              forms[kind]['rows'],
                                                              forms[kind]['ok']))
    with open(__file__, 'rb') as fh:
        self_sha = sha(fh.read())[:12]
    print('READS_V2: self=%s rev=%s headings=%d/%d pointers=%d legacy=%d new=%d/%d/%d '
          'floor_short=%d unresolved=%d unverified=%d excerpt_miss=%d not_holds=%d absent=%d '
          'absent_bad=%d absent_overflow=%d glob_mismatch=%d traces=%d/%d trace_empty=%d '
          'trace_missing=%d total=%d READS_V2_PASS=%s'
          % (self_sha, rev, len(headings) - len(missing), len(headings), len(pointers),
             sum(forms[k]['pointers'] for k in ('line', 'path', 'sid') if k in forms),
             forms.get('section', {}).get('pointers', 0),
             forms.get('anchor', {}).get('pointers', 0),
             forms.get('glob', {}).get('pointers', 0),
             floor_short, res['unresolved'], res['unverified'], res['excerpt_miss'],
             res['not_holds'], res['absent'], res['absent_bad'], res['absent_overflow'],
             res['glob_mismatch'], tres['ok'], tres['receipts'], tres['empty'], tres['missing'],
             total, 'true' if total == 0 else 'false'))
    return {'rev': rev, 'missing': missing, 'pointers': len(pointers), 'counts': counts,
            'forms': forms, 'floor_short': floor_short, 'reads': res, 'trace': tres,
            'total': total, 'pass': total == 0, 'detail': detail, 'trace_detail': tdetail}


def selftest():
    cases = []
    calls = [0]

    def case(name, ok):
        cases.append((name, bool(ok)))
        print('CASE %s %s' % (name, 'PASS' if ok else 'FAIL'))

    import shutil
    import tempfile

    root = tempfile.mkdtemp(prefix='reads-v2-selftest-', dir=os.environ.get('TMPDIR') or None)
    try:
        made = [0]

        class Fx:
            def __init__(self, files):
                made[0] += 1
                self.repo = os.path.join(root, 'lane%02d' % made[0])
                r = subprocess.run(['git', 'init', '-q', self.repo], capture_output=True, env=GIT_ENV)
                if r.returncode != 0:
                    raise Setup('fixture init failed')
                top = git(self.repo, 'rev-parse', '--show-toplevel').stdout.decode().strip()
                if os.path.realpath(top) != os.path.realpath(self.repo):
                    raise Setup('fixture toplevel mismatch: %s' % top)
                for rel, text in files.items():
                    self.put(rel, text)
                self.rev = self.commit('init')

            def put(self, rel, text):
                path = os.path.join(self.repo, rel)
                d = os.path.dirname(path)
                if d:
                    os.makedirs(d, exist_ok=True)
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(text)

            def rm(self, rel):
                os.remove(os.path.join(self.repo, rel))

            def commit(self, msg):
                git(self.repo, 'add', '-A')
                r = git(self.repo, 'commit', '-q', '-m', msg, env=COMMIT_ENV)
                if r.returncode != 0:
                    raise Setup('fixture commit failed: %s' % r.stderr.decode()[-200:])
                self.rev = git(self.repo, 'rev-parse', 'HEAD').stdout.decode().strip()
                return self.rev

            def census(self, heading='## F'):
                found, _ = target_sections(self.repo, self.rev, [heading])
                return extract_v2(found[heading]['text']), found[heading]['text']

            def rows(self, specs, heading='## F'):
                ps, _ = self.census(heading)
                out = []
                for p in ps:
                    if p['raw'] in specs:
                        row = {'heading': heading, 'ordinal': p['ordinal'], 'raw': p['raw']}
                        row.update(json.loads(json.dumps(specs[p['raw']])))
                        out.append(row)
                return out

            def reads(self, rows):
                self.put('.ufo/reads.json', json.dumps({'schema': 'reads-v2-fixture', 'rows': rows}))

            def run(self, traces=('.ufo/traces/t.json',), floors=None):
                calls[0] += 1
                return measure(self.repo, self.rev, list(traces), reads='.ufo/reads.json',
                               headings=['## F'], floors=floors, fleet=self.repo, quiet=True)

        ALPHABET = ('## 1. Alpha section about the lazy dog\nBody of alpha.\n'
                    '## 2. Beta section about the tool\nBody of beta.\n'
                    '## 3. Gamma section about the ledger\nBody of gamma.\n'
                    '## 4. Delta section about the cadence\nBody of delta.\n')
        DISC = '## box-1 \u2014 the first audit box\nBox one records the audit receipt for the lane.\n'
        GOOD_TRACE = json.dumps({'schema': 'tameshi-trace-inputs-v1',
                                 'inputs': {'SKILL.md': '0' * 64}})

        def skill(extra='', absent='The driver ghost.py is a placeholder, not a file \u2014 nothing was '
                                  'ever committed.'):
            return ('## F\n\nThe case note alphabet.md \u00a71 covers the method; \u00a73-\u00a74 cover '
                    'the ledger.\nThe audit anchors at disc.md#box-1 and corpus/knowledge/case-*.md '
                    'names the suite.\n\n' + absent + (('\n\n' + extra) if extra else '') + '\n')

        def base_files(absent_sentence=None, extra=''):
            return {
                'SKILL.md': skill(extra=extra) if absent_sentence is None else skill(
                    extra=extra, absent=absent_sentence),
                'corpus/knowledge/alphabet.md': ALPHABET,
                'corpus/knowledge/disc.md': DISC,
                'corpus/knowledge/case-a.md': 'case a body\n',
                'corpus/knowledge/case-b.md': 'case b body\n',
                '.ufo/traces/t.json': GOOD_TRACE,
            }

        ABSENT_QUOTE = ('The driver ghost.py is a placeholder, not a file \u2014 nothing was ever '
                        'committed.')
        GOOD_SECTION = {'file': 'corpus/knowledge/alphabet.md', 'ranges': [[1, 2]],
                        'verdict': 'holds',
                        'excerpt': '## 1. Alpha section about the lazy dog Body of alpha.'}
        RANGE34 = {'file': 'corpus/knowledge/alphabet.md', 'ranges': [[5, 6], [7, 8]],
                   'verdict': 'holds',
                   'excerpt': ('## 3. Gamma section about the ledger Body of gamma. ## 4. Delta '
                               'section about the cadence Body of delta.')}
        ANCHOR = {'file': 'corpus/knowledge/disc.md', 'ranges': [[1, 2]], 'verdict': 'holds',
                  'excerpt': ('## box-1 \u2014 the first audit box Box one records the audit receipt '
                              'for the lane.')}
        GLOB = {'verdict': 'holds',
                'files': ['corpus/knowledge/case-a.md', 'corpus/knowledge/case-b.md'],
                'excerpt': ('The audit anchors at disc.md#box-1 and corpus/knowledge/case-*.md names '
                            'the suite.')}
        PATHS = {'alphabet.md': {'file': 'corpus/knowledge/alphabet.md', 'ranges': None,
                                 'verdict': 'holds',
                                 'excerpt': '## 1. Alpha section about the lazy dog Body of alpha.'},
                 'disc.md': {'file': 'corpus/knowledge/disc.md', 'ranges': None, 'verdict': 'holds',
                             'excerpt': 'Box one records the audit receipt for the lane.'}}

        def good_absent(quote=ABSENT_QUOTE, history=None, path='ghost.py'):
            return {'file': None, 'ranges': None, 'verdict': 'absent',
                    'absent_evidence': {'path': path, 'history': history or [],
                                        'not_a_file': quote}}

        def good_rows(extra=None):
            specs = dict(PATHS)
            specs.update({'ghost.py': good_absent(), '\u00a71': GOOD_SECTION,
                          '\u00a73-\u00a74': RANGE34, 'disc.md#box-1': ANCHOR,
                          'corpus/knowledge/case-*.md': GLOB})
            specs.update(extra or {})
            return specs

        # ---- R2: census of the new forms (expectations stated independently of the checker)
        fx = Fx(base_files())
        ps, _ = fx.census()
        by_raw = {p['raw']: p for p in ps}
        found, _ = target_sections(fx.repo, fx.rev, ['## F'])
        al = blob(fx.repo, fx.rev, 'corpus/knowledge/alphabet.md')
        case('census-forms', [p['raw'] for p in ps] ==
             ['alphabet.md', 'disc.md', 'ghost.py', '\u00a71', '\u00a73-\u00a74', 'disc.md#box-1',
              'corpus/knowledge/case-*.md'])
        case('census-section-region', section_ranges(al, by_raw['\u00a73-\u00a74']['numbers']) ==
             [[5, 6], [7, 8]])
        case('census-anchor-region',
             anchor_ranges(blob(fx.repo, fx.rev, 'corpus/knowledge/disc.md'), 'box-1') == [[1, 2]])
        case('census-glob-files', glob_files(fx.repo, fx.rev, 'corpus/knowledge/case-*.md') ==
             ['corpus/knowledge/case-a.md', 'corpus/knowledge/case-b.md'])
        case('census-token-inherit', by_raw['\u00a71']['token'] == 'alphabet.md' and
             by_raw['\u00a73-\u00a74']['token'] == 'alphabet.md')
        case('census-ordinals-stable', [p['ordinal'] for p in ps] == list(range(len(ps))))

        # ---- end-to-end: measure() before (no rows, empty trace) and after (all rules met)
        fx = Fx(base_files())
        fx.reads([])
        fx.put('.ufo/traces/t.json', json.dumps({'schema': 'tameshi-trace-inputs-v1', 'inputs': {}}))
        fx.commit('defects')
        before = fx.run()
        fx.reads(fx.rows(good_rows()))
        fx.put('.ufo/traces/t.json', GOOD_TRACE)
        fx.commit('fixed')
        after = fx.run()
        case('e2e-before-fails', before['total'] >= 8 and before['reads']['unverified'] == 6 and
             before['reads']['unresolved'] == 1 and before['trace']['empty'] == 1 and
             not before['pass'])
        case('e2e-after-passes', after['total'] == 0 and after['pass'])

        # ---- R1a: absent needs evidence
        fx = Fx(base_files())
        specs = good_rows({'ghost.py': {'file': None, 'ranges': None, 'verdict': 'absent'}})
        fx.reads(fx.rows(specs))
        fx.commit('absent-no-evidence')
        before = fx.run()
        specs['ghost.py'] = good_absent()
        fx.reads(fx.rows(specs))
        fx.commit('absent-evidence')
        after = fx.run()
        case('R1-absent-needs-evidence',
             before['reads']['absent_bad'] == 1 and before['total'] == 1 and after['total'] == 0)

        # ---- R1b: history must be empty (a path that existed and was deleted)
        files = base_files(absent_sentence='The driver corpus/old.py is a placeholder, not a file '
                                          '\u2014 nothing was ever committed.')
        files['corpus/old.py'] = 'deleted later\n'
        fx = Fx(files)
        fx.rm('corpus/old.py')
        fx.commit('delete-old')
        hist = [h for h in git(fx.repo, 'log', '--all', '--format=%H', '--',
                               'corpus/old.py').stdout.decode().split('\n') if h]
        specs = good_rows({'corpus/old.py': good_absent(path='corpus/old.py', history=hist,
                                                       quote=('The driver corpus/old.py is a '
                                                              'placeholder, not a file \u2014 nothing '
                                                              'was ever committed.'))})
        fx.reads(fx.rows(specs))
        fx.commit('old-row')
        before = fx.run()
        fx2 = Fx(base_files())
        fx2.reads(fx2.rows(good_rows()))
        fx2.commit('ghost-instead')
        after = fx2.run()
        case('R1-absent-history-empty',
             bool(hist) and before['reads']['absent_bad'] == 1 and before['total'] == 1 and
             after['total'] == 0)
        found, _ = target_sections(fx.repo, fx.rev, ['## F'])
        case('R1-absent-history-unrecorded',
             absent_reason(fx.repo, {'raw': 'corpus/old.py'},
                           {'absent_evidence': {'path': 'corpus/old.py', 'history': [],
                                                'not_a_file': ABSENT_QUOTE}},
                           found['## F']['text']) == 'history-unrecorded')

        # ---- R1c: the quote must say it is not a file, and must occur in the section
        for tag, quote, reason in (
                ('R1-quote-not-a-file',
                 'The driver ghost.py is the script the case notes call first.',
                 'quote-not-a-file'),
                ('R1-quote-not-in-section',
                 'The driver ghost.py is a placeholder, not a file \u2014 nothing was ever committed '
                 'in this repository at all.',
                 'quote-not-in-section'),
                ('R1-quote-token-missing',
                 'The driver is a placeholder, not a file \u2014 nothing was ever committed.',
                 'quote-token-missing')):
            fx = Fx(base_files())
            fx.reads(fx.rows(good_rows({'ghost.py': good_absent(quote=quote)})))
            fx.commit('bad-quote')
            before = fx.run()
            fx.reads(fx.rows(good_rows()))
            fx.commit('good-quote')
            after = fx.run()
            case(tag, before['reads']['absent_bad'] == 1 and before['total'] == 1 and
                 after['total'] == 0 and
                 [r for _, r, _ in before['detail'] if isinstance(r, str) and
                  r.startswith('absent:')] == ['absent:%s' % reason])

        # ---- R1d: at most one absent row per section
        two = ('The driver ghost.py is a placeholder, not a file \u2014 nothing was ever committed.'
               '\n\nThe helper phantom.py is a placeholder, not a file \u2014 nothing was ever '
               'committed either.')
        fx = Fx(base_files(absent_sentence=two))
        specs = good_rows({'ghost.py': good_absent(),
                           'phantom.py': good_absent(
                               quote=('The helper phantom.py is a placeholder, not a file \u2014 '
                                      'nothing was ever committed either.'), path='phantom.py')})
        fx.reads(fx.rows(specs))
        fx.commit('two-absent')
        before = fx.run()
        fx = Fx(base_files())
        fx.reads(fx.rows(good_rows()))
        fx.put('.ufo/traces/t.json', GOOD_TRACE)
        fx.commit('one-absent')
        after = fx.run()
        case('R1-absent-cap-per-section',
             before['reads']['absent_overflow'] == 1 and before['reads']['absent'] == 2 and
             before['total'] == 1 and after['total'] == 0)

        # ---- R2a: a § ref with no row fails; a wrong region fails; the right row passes
        fx = Fx(base_files())
        specs = good_rows()
        del specs['\u00a73-\u00a74']
        fx.reads(fx.rows(specs))
        fx.commit('section-no-row')
        before = fx.run()
        specs['\u00a73-\u00a74'] = dict(RANGE34, ranges=[[1, 2]])
        fx.reads(fx.rows(specs))
        fx.commit('section-wrong-region')
        wrong = fx.run()
        specs['\u00a73-\u00a74'] = RANGE34
        fx.reads(fx.rows(specs))
        fx.commit('section-right')
        after = fx.run()
        case('R2-section-needs-row', before['reads']['unverified'] == 1 and before['total'] == 1)
        case('R2-section-region', wrong['reads']['unverified'] == 1 and wrong['total'] == 1 and
             after['total'] == 0)

        # ---- R2b: anchor needs row (wrong region -> unverified, right -> pass)
        fx = Fx(base_files())
        specs = good_rows()
        del specs['disc.md#box-1']
        fx.reads(fx.rows(specs))
        fx.commit('anchor-no-row')
        before = fx.run()
        specs['disc.md#box-1'] = dict(ANCHOR, ranges=[[1, 1]])
        fx.reads(fx.rows(specs))
        fx.commit('anchor-wrong-region')
        wrong = fx.run()
        specs['disc.md#box-1'] = ANCHOR
        fx.reads(fx.rows(specs))
        fx.commit('anchor-right')
        after = fx.run()
        case('R2-anchor-needs-row', before['reads']['unverified'] == 1 and before['total'] == 1 and
             wrong['total'] == 1 and after['total'] == 0)

        # ---- R2c: glob expansion is bound (a tenth file cannot pass unnoticed)
        fx = Fx(base_files())
        specs = good_rows()
        specs['corpus/knowledge/case-*.md'] = dict(GLOB, files=['corpus/knowledge/case-a.md'])
        fx.reads(fx.rows(specs))
        fx.commit('glob-short')
        before = fx.run()
        specs['corpus/knowledge/case-*.md'] = GLOB
        fx.reads(fx.rows(specs))
        fx.commit('glob-right')
        after = fx.run()
        fx.put('corpus/knowledge/case-c.md', 'case c body\n')
        fx.commit('glob-grows')
        grown = fx.run()
        case('R2-glob-expansion-bound',
             before['reads']['glob_mismatch'] == 1 and before['total'] == 1 and
             after['total'] == 0 and grown['reads']['glob_mismatch'] == 1 and grown['total'] == 1)

        # ---- R3a: a trace with zero recorded inputs is refused (doc with a mixed receipts list)
        fx = Fx(base_files())
        fx.reads(fx.rows(good_rows()))
        fx.put('.ufo/traces/t.json', json.dumps({'receipts': [
            {'section': 'a', 'inputs': {'SKILL.md': '0' * 64}},
            {'section': 'b', 'inputs': {}}]}))
        fx.commit('trace-partial')
        before = fx.run()
        fx.put('.ufo/traces/t.json', json.dumps({'receipts': [
            {'section': 'a', 'inputs': {'SKILL.md': '0' * 64}},
            {'section': 'b', 'inputs': {'SKILL.md': '1' * 64}}]}))
        fx.commit('trace-full')
        after = fx.run()
        case('R3-trace-empty-refused',
             before['trace']['empty'] == 1 and before['total'] == 1 and after['total'] == 0)

        # ---- R3b: an empty receipt set is refused
        files = base_files()
        del files['.ufo/traces/t.json']
        fx = Fx(files)
        fx.reads(fx.rows(good_rows()))
        fx.put('.ufo/traces/README.txt', 'no receipts here\n')
        fx.commit('trace-dir-empty')
        before = fx.run(traces=('.ufo/traces',))
        fx.put('.ufo/traces/t.json', GOOD_TRACE)
        fx.commit('trace-dir-filled')
        after = fx.run(traces=('.ufo/traces',))
        case('R3-trace-missing-refused',
             before['trace']['missing'] == 1 and before['total'] == 1 and after['total'] == 0)

        # ---- floors stay a term of the same check (optional)
        fx = Fx(base_files())
        fx.reads(fx.rows(good_rows()))
        fx.commit('floors')
        short = fx.run(floors={'## F': 99})
        case('floor-short', short['floor_short'] == 1 and short['total'] == 1)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    failed = sum(1 for _, ok in cases if not ok)
    print('READS_V2_SELFTEST: cases=%d failed=%d measure_calls=%d' % (len(cases), failed, calls[0]))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--trace', action='append', default=[])
    ap.add_argument('--reads', default=READS_DEFAULT)
    ap.add_argument('--headings')
    ap.add_argument('--floors')
    ap.add_argument('--fleet')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    try:
        a = ap.parse_args()
    except SystemExit:
        return 64
    if a.selftest:
        return selftest()
    if not a.lane or not a.rev:
        return 64
    lane = os.path.realpath(a.lane)
    r = git(lane, 'rev-parse', '--verify', '--quiet', '--end-of-options', a.rev + '^{commit}')
    if r.returncode != 0 or a.rev.startswith('-'):
        print('READS_V2: setup=unresolvable-rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    headings = TARGETS
    if a.headings:
        try:
            headings = tuple(json.loads(a.headings))
        except ValueError:
            return 64
    floors = None
    if a.floors:
        try:
            with open(a.floors) as fh:
                floors = json.load(fh)
        except (OSError, ValueError) as exc:
            print('READS_V2: setup=floors-unreadable: %s' % exc, file=sys.stderr)
            return 2
    try:
        if a.list:
            found, missing = target_sections(lane, rev, headings)
            out = []
            cache = {}
            for h in headings:
                if h not in found:
                    continue
                for p in extract_v2(found[h]['text']):
                    p['heading'] = h
                    p['pointer_kind'] = p['kind']
                    p['section_sha256'] = found[h]['sha256']
                    p['skill_line'] = found[h]['start'] + p['line']
                    info = resolve_pointer(lane, rev, os.path.dirname(lane), p, None, cache)
                    p['file'] = info['file']
                    p['ranges_expected'] = info['ranges']
                    p['files_expected'] = info['files']
                    p.pop('token', None)
                    out.append(p)
            print(json.dumps({'rev': rev, 'headings': list(headings), 'missing_headings': missing,
                              'pointers': out}, indent=1, ensure_ascii=False))
            return 0
        if not a.trace:
            print('READS_V2: usage=--trace required (R3 refuses an unrecorded trace)',
                  file=sys.stderr)
            return 64
        summary = measure(lane, rev, a.trace, reads=a.reads, headings=headings, floors=floors,
                          fleet=a.fleet)
        return 0 if summary['pass'] else 1
    except Setup as exc:
        print('READS_V2: setup=%s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
