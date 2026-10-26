#!/usr/bin/env python3
r"""Round-49 C1 counter (calibration): reading-bound, record-durable cold-read refresh.

Usage:
  python3 measure.py --lane LANE --rev REV --work EMPTY_DIR [--fleet FLEET]
  python3 measure.py --lane LANE --rev REV --list          # pointer list as JSON (no verdict)
  python3 measure.py --selftest

Predicate (contract.json `c1.predicate`, label C1_R49_PASS), all at REV:
  (a) MONITOR: the unchanged round-21 cold-read monitor (strict, no override flag)
      credits every section (sections_covered == sections_total >= 64) and prints
      calibration_restraint_score 8. Both monitor files must hash to the pins below,
      in the live lane and at REV.
  (b) DURABLE: the same monitor still credits every section at a synthetic commit
      D = REV + one appended line in each of the five record files VOLATILE
      (built by plumbing in a --shared clone under --work; the lane is never written).
  (c) READS: in each of the seven TARGET sections (heading text at REV, each exactly
      once) every pointer the frozen extractor finds resolves at REV, has exactly
      one row in READS (keyed heading+ordinal+raw) with the same file and ranges,
      verdict `holds`, and an excerpt (whitespace-collapsed, 24-400 chars) that
      occurs in the whitespace-collapsed pointed text (line pointer: the pointed
      lines; path pointer: the whole file; S-id pointer: its SOURCES.md row line).
      The one exception: a path pointer that does not resolve passes only with a
      row whose verdict is `absent` and file null (counted as `absent`). Each
      section keeps at least its base pointer count (FLOORS).
  total = (sections-covered) + (sections-durable_covered) + (score != 8)
          + heading_missing + floor_short + unresolved + unverified + excerpt_miss
          + not_holds;  C1_R49_PASS = (total == 0).

Extractor (frozen), in order per section: line pointers (each occurrence), then
path pointers (one per distinct token), then S-id pointers (one per distinct id).
  * line pointer: FILE ':' RANGES where FILE = optional '../', optional dir parts,
    a name ending .md/.py/.sh/.json/.mjs/.txt/.xml/.html, not preceded by
    [\w/.-]; RANGES = N[-N] (hyphen or en dash) followed by any ', N[-N]' /
    ', :N[-N]' / ',N[-N]' continuations.
  * bare line pointer: ':' N[-N] (+continuations) not preceded by [\w:./-] and not
    part of a file pointer; it inherits the FILE of the nearest preceding file
    pointer in the same paragraph (a table row is its own paragraph; otherwise a
    paragraph is a run of non-blank lines). No such file -> unresolved.
  * path pointer: a FILE token not preceded by [\w/.-] and not followed by
    [\w.-] or ':<digit>'.
  * S-id pointer: S followed by 3+ digits, not preceded by a word character.
  * resolution: '../X' is external (fleet repo blob X at the row's 40-hex
    `fleet_commit`); an S-id resolves to the single SOURCES.md registry line
    matching '^ {0,3}| Sxxx |' at REV; else the first of FILE,
    corpus/knowledge/FILE, corpus/FILE, corpus/lessons/FILE that is a blob at REV.
    Every line range needs 1 <= s <= e <= the blob's line count.
Exit: 0 PASS, 1 measured not-pass, 2 setup error, 64 usage.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
MONITOR = '.ufo/evidence/round-21/coldread/measure.py'
MONITOR_IMPL = '.ufo/evidence/round-18/measure.py'
MONITOR_SHA = '657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb'
MONITOR_IMPL_SHA = '7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37'
READS = '.ufo/evidence/round-49/c1/reads.json'
VOLATILE = ('LOG.md', 'SCORECARD.md', 'corpus/SOURCES.md', 'corpus/QUALITY.md', 'corpus/README.md')
PROBE_LINE = b'<!-- round-49 C1 durability probe: appended record line -->\n'
TARGETS = (
    '## Mutation-sweep recipe \u2014 numbered steps; bounded cold-read evidence',
    '## Restore discipline \u2014 before/after identity, not continuous non-write proof',
    '### The map \u2014 where a reader enters, artifact by artifact',
    '## Promotion-evidence calibration \u2014 fleet round-1',
    '## Repeated controls and gate registry \u2014 round 12',
    '## Pin disposition and provenance correction \u2014 round 13',
    '## Effective expectation reconciliation \u2014 round 14',
)
# Base pointer counts per target (extractor at base 8ca67421111fa354b47b803358391d0b07fc6db9);
# filled at freeze from `--list` and never changed afterwards.
FLOORS = {
    TARGETS[0]: 34, TARGETS[1]: 10, TARGETS[2]: 17, TARGETS[3]: 5, TARGETS[4]: 5, TARGETS[5]: 9, TARGETS[6]: 10,
}
EXCERPT_MIN, EXCERPT_MAX = 24, 400
EXT = r'(?:md|py|sh|json|mjs|txt|xml|html)'
FILE_RE = r'(?:\.\./)?(?:[\w.-]+/)*\w[\w.-]*\.' + EXT
RANGE = r'\d+(?:[-\u2013]\d+)?'
CONT = r'(?:,\s*:?' + RANGE + r')*'
PTR_RE = re.compile(r'(?<![\w/.-])(?P<file>' + FILE_RE + r'):(?P<ranges>' + RANGE + CONT + r')'
                    r'|(?<![\w:./-]):(?P<bare>' + RANGE + CONT + r')')
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
GIT_ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
PATH_RE = re.compile(r'(?<![\w/.-])(' + FILE_RE + r')(?![\w.-]|:\d)')
SID_RE = re.compile(r'(?<![\w])S\d{3,}(?!\d)')


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


def extract(section_text):
    """Return pointer dicts in order: line pointers (each occurrence), then path pointers (one per
    distinct FILE token not followed by ':<digit>'), then S-id pointers (one per distinct id)."""
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


def resolve(repo, rev, token, kind='line'):
    """Return (file, kind, ranges) or (None, None, None); kind out is 'line', 'path', 'sid',
    'external' (a ../ line pointer) or 'external-path' (a ../ path pointer). ranges is set for
    'sid' only (the registry row line)."""
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


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def pointed_text(data, ranges):
    lines = data.decode('utf-8', 'surrogateescape').split('\n')
    return norm('\n'.join('\n'.join(lines[s - 1:e]) for s, e in ranges))


def load_monitor_module(lane):
    path = os.path.join(lane, MONITOR_IMPL)
    spec = importlib.util.spec_from_file_location('tameshi_r18_monitor_impl', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def target_sections(lane, rev):
    raw = blob(lane, rev, 'SKILL.md')
    if raw is None:
        raise Setup('SKILL.md missing at REV')
    mod = load_monitor_module(lane)
    secs = mod.sectionize(raw)
    lines = raw.decode('utf-8', 'surrogateescape').split('\n')
    found = {}
    counts = {}
    for s in secs:
        counts[s['heading']] = counts.get(s['heading'], 0) + 1
        if s['heading'] in TARGETS:
            body = list(lines[s['start'] - 1:s['end']])
            while body and body[-1].strip() == '':
                body.pop()
            found[s['heading']] = {'start': s['start'], 'end': s['end'], 'sha256': s['sha256'],
                                   'text': '\n'.join(body)}
    missing = [h for h in TARGETS if counts.get(h, 0) != 1]
    return found, missing


def list_pointers(lane, rev):
    found, missing = target_sections(lane, rev)
    out = []
    for h in TARGETS:
        if h not in found:
            continue
        sec = found[h]
        for p in extract(sec['text']):
            f, kind, rr = resolve(lane, rev, p['token'], p['kind'])
            ranges = p['ranges'] if p['kind'] == 'line' else rr
            out.append({'heading': h, 'section_start': sec['start'], 'section_sha256': sec['sha256'],
                        'ordinal': p['ordinal'], 'raw': p['raw'], 'pointer_kind': p['kind'], 'file': f,
                        'kind': kind, 'ranges': ranges, 'skill_line': sec['start'] + p['line']})
    return out, missing


def check_reads(lane, rev, fleet, pointers, reads_doc):
    rows = reads_doc.get('rows') if isinstance(reads_doc, dict) else None
    rows = rows if isinstance(rows, list) else []
    index = {}
    for r in rows:
        if isinstance(r, dict):
            index.setdefault((r.get('heading'), r.get('ordinal'), r.get('raw')), []).append(r)
    res = {'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 0, 'absent': 0}
    detail = []
    cache = {}
    for p in pointers:
        status = 'ok'
        data = None
        hits = index.get((p['heading'], p['ordinal'], p['raw']), [])
        row = hits[0] if len(hits) == 1 else None
        if p['file'] is None:
            # An unresolvable path pointer may be read as `absent` (the section names a file the
            # lane does not hold); every other unresolvable pointer is unresolved.
            if p.get('pointer_kind') == 'path' and row is not None and row.get('verdict') == 'absent' \
                    and row.get('file') is None:
                res['absent'] += 1
                detail.append((p, 'absent'))
                continue
            status = 'unresolved'
        elif p['kind'] in ('external', 'external-path'):
            fc = row.get('fleet_commit') if row else None
            if not (isinstance(fc, str) and re.fullmatch(r'[0-9a-f]{40}', fc)):
                status = 'unresolved'
            else:
                key = ('ext', fc, p['file'])
                if key not in cache:
                    cache[key] = blob(fleet, fc, p['file'][3:])
                data = cache[key]
        else:
            key = ('lane', p['file'])
            if key not in cache:
                cache[key] = blob(lane, rev, p['file'])
            data = cache[key]
        if status == 'ok':
            if data is None:
                status = 'unresolved'
            elif p['ranges'] is not None:
                n = line_count(data)
                if not all(1 <= s <= e <= n for s, e in p['ranges']):
                    status = 'unresolved'
        if status == 'ok':
            if row is None or row.get('file') != p['file'] or row.get('ranges') != p['ranges']:
                status = 'unverified'
            elif row.get('verdict') != 'holds':
                status = 'not_holds'
            else:
                ex = row.get('excerpt')
                exn = norm(ex) if isinstance(ex, str) else ''
                where = pointed_text(data, p['ranges']) if p['ranges'] is not None else \
                    norm(data.decode('utf-8', 'surrogateescape'))
                if not (EXCERPT_MIN <= len(exn) <= EXCERPT_MAX) or exn not in where:
                    status = 'excerpt_miss'
        if status != 'ok':
            res[status] += 1
        detail.append((p, status))
    return res, detail


def run_monitor(lane, repo, rev, work, tag):
    env = dict(GIT_ENV)
    env['TMPDIR'] = work
    r = subprocess.run([sys.executable, '-B', os.path.join(lane, MONITOR), '--repo', repo, '--rev', rev],
                       capture_output=True, env=env, cwd=work)
    with open(os.path.join(work, 'monitor-%s.json' % tag), 'wb') as fh:
        fh.write(r.stdout)
    if r.returncode != 0:
        raise Setup('monitor exit %d at %s: %s' % (r.returncode, tag, r.stderr.decode(errors='replace')[-300:]))
    d = json.loads(r.stdout)
    c = d['coldread']
    return {'total': c['sections_total'], 'covered': c['sections_covered'],
            'score': d['calibration_restraint_score'], 'strict': d.get('trace_gate') == 'strict',
            'overrides': d.get('overrides_used'),
            'uncovered': [s['heading'] for s in c['sections'] if not s['credited']]}


def durability_commit(lane, rev, work):
    clone = os.path.join(work, 'dur')
    r = subprocess.run(['git', 'clone', '--quiet', '--shared', '--no-checkout', lane, clone],
                       capture_output=True, env=GIT_ENV)
    if r.returncode != 0:
        raise Setup('clone failed: %s' % r.stderr.decode(errors='replace')[-200:])
    top = git(clone, 'rev-parse', '--show-toplevel').stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(clone):
        raise Setup('clone toplevel mismatch')
    env = dict(GIT_ENV)
    env['GIT_INDEX_FILE'] = os.path.join(work, 'dur.index')
    if git(clone, 'read-tree', rev, env=env).returncode != 0:
        raise Setup('read-tree failed')
    for path in VOLATILE:
        old = blob(clone, rev, path) or b''
        h = git(clone, 'hash-object', '-w', '--stdin', data=old + PROBE_LINE)
        oid = h.stdout.decode().strip()
        if h.returncode != 0 or git(clone, 'update-index', '--add', '--cacheinfo',
                                    '100644,%s,%s' % (oid, path), env=env).returncode != 0:
            raise Setup('update-index failed for %s' % path)
    tree = git(clone, 'write-tree', env=env).stdout.decode().strip()
    cenv = dict(env)
    cenv.update(GIT_AUTHOR_NAME='r49-probe', GIT_AUTHOR_EMAIL='probe@invalid',
                GIT_COMMITTER_NAME='r49-probe', GIT_COMMITTER_EMAIL='probe@invalid',
                GIT_AUTHOR_DATE='2026-10-26T00:00:00Z', GIT_COMMITTER_DATE='2026-10-26T00:00:00Z')
    del cenv['GIT_INDEX_FILE']
    c = git(clone, 'commit-tree', tree, '-p', rev, '-m', 'r49 durability probe', env=cenv)
    if c.returncode != 0:
        raise Setup('commit-tree failed')
    return clone, c.stdout.decode().strip()


def measure(lane, rev, work, fleet):
    for path, pin in ((MONITOR, MONITOR_SHA), (MONITOR_IMPL, MONITOR_IMPL_SHA)):
        with open(os.path.join(lane, path), 'rb') as fh:
            live = sha(fh.read())
        at_rev = blob(lane, rev, path)
        if live != pin or at_rev is None or sha(at_rev) != pin:
            raise Setup('monitor pin mismatch: %s' % path)
    mon = run_monitor(lane, lane, rev, work, 'rev')
    clone, dcommit = durability_commit(lane, rev, work)
    dur = run_monitor(lane, clone, dcommit, work, 'durable')
    pointers, missing = list_pointers(lane, rev)
    counts = {h: 0 for h in TARGETS}
    for p in pointers:
        counts[p['heading']] += 1
    floor_short = sum(1 for h in TARGETS if h not in missing and counts[h] < FLOORS[h])
    raw = blob(lane, rev, READS)
    try:
        reads_doc = json.loads(raw) if raw is not None else {}
    except ValueError:
        reads_doc = {}
    res, detail = check_reads(lane, rev, fleet, pointers, reads_doc)
    for p, st in detail:
        print('PTR %s #%d %s -> %s %s %s' % (p['heading'][:40], p['ordinal'], p['raw'], p['file'],
                                             p['ranges'], st))
    for h in TARGETS:
        print('SECTION %s pointers=%d floor=%d %s' % (h[:50], counts[h], FLOORS[h],
                                                      'missing' if h in missing else 'present'))
    for h in mon['uncovered']:
        print('UNCOVERED_REV %s' % h)
    for h in dur['uncovered']:
        print('UNCOVERED_DURABLE %s' % h)
    bad_mon = (mon['total'] - mon['covered']) + (0 if mon['total'] >= 64 else 1) + \
        (0 if mon['strict'] and mon['overrides'] is False else 1)
    total = (bad_mon + (dur['total'] - dur['covered']) + (0 if mon['score'] == 8 else 1) + len(missing) +
             floor_short + res['unresolved'] + res['unverified'] + res['excerpt_miss'] + res['not_holds'])
    with open(__file__, 'rb') as fh:
        self_sha = sha(fh.read())[:12]
    line = ('C1_R49: self=%s rev=%s sections=%d covered=%d score=%s durable_covered=%d/%d headings=%d/7 '
            'pointers=%d floor_short=%d unresolved=%d unverified=%d excerpt_miss=%d not_holds=%d absent=%d '
            'total=%d C1_R49_PASS=%s' % (self_sha, rev, mon['total'], mon['covered'], mon['score'],
                                         dur['covered'], dur['total'], 7 - len(missing), len(pointers),
                                         floor_short, res['unresolved'], res['unverified'], res['excerpt_miss'],
                                         res['not_holds'], res['absent'], total,
                                         'true' if total == 0 else 'false'))
    print(line)
    return 0 if total == 0 else 1


def selftest():
    cases = []

    def case(name, ok):
        cases.append((name, bool(ok)))
        print('CASE %s %s' % (name, 'PASS' if ok else 'FAIL'))

    text = ('## H\n\nStep a (mutation-case-kimi-census.md:13-16;\nmutation-case-kagi-census.md:27-35,42-43).\n'
            'More (x.md:41-53, :155-166) at 09:47:15 and http://h:80/x.\n\n'
            '| `a.md` | see (`:12-14`) |\nlone `:7` here\n\nS `SKILL.md:377\u2013378` ok.')
    ps = extract(text)
    raws = [p['raw'] for p in ps]
    case('file-pointer', 'mutation-case-kimi-census.md:13-16' in raws)
    case('continuation-comma', 'mutation-case-kagi-census.md:27-35,42-43' in raws and
         [p for p in ps if p['raw'].startswith('mutation-case-kagi')][0]['ranges'] == [[27, 35], [42, 43]])
    case('continuation-colon', 'x.md:41-53, :155-166' in raws)
    case('time-not-pointer', not any(r in (':47', ':15', ':47:15') for r in raws))
    case('url-port-not-pointer', ':80' not in raws)
    tbl = [p for p in ps if p['raw'] == ':12-14']
    case('table-row-bare-unresolved', len(tbl) == 1 and tbl[0]['token'] is None)
    lone = [p for p in ps if p['raw'] == ':7']
    case('bare-no-file-in-paragraph', len(lone) == 1 and lone[0]['token'] is None)
    case('en-dash', [p for p in ps if p['raw'].startswith('SKILL.md')][0]['ranges'] == [[377, 378]])
    para2 = extract('see a.md:3 and then\n(:5-6) later')
    case('bare-inherits-paragraph-file', para2[1]['token'] == 'a.md' and para2[1]['ranges'] == [[5, 6]])
    case('ordinals', [p['ordinal'] for p in ps] == list(range(len(ps))))
    case('norm', norm(' a\n  b\tc ') == 'a b c')
    data = b'l1\nalpha beta gamma delta epsilon zeta\nl3\n'
    case('pointed-text', 'alpha beta gamma delta epsilon zeta' in pointed_text(data, [[2, 2]]))
    case('line-count', line_count(data) == 3 and line_count(b'a\nb') == 2)
    # check_reads on a fake pointer list with in-memory blob cache: use a synthetic repo
    import tempfile
    with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR') or None) as tmp:
        repo = os.path.join(tmp, 'r')
        subprocess.run(['git', 'init', '-q', repo], check=True, env=GIT_ENV)
        if os.path.realpath(git(repo, 'rev-parse', '--show-toplevel').stdout.decode().strip()) != \
                os.path.realpath(repo):
            case('fixture-toplevel', False)
        else:
            os.makedirs(os.path.join(repo, 'corpus/knowledge'))
            with open(os.path.join(repo, 'corpus/knowledge/n.md'), 'w') as fh:
                fh.write('one\nthe quick brown fox jumps over the lazy dog\nthree\n')
            git(repo, 'add', '-A')
            env = dict(GIT_ENV, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@invalid', GIT_COMMITTER_NAME='t',
                       GIT_COMMITTER_EMAIL='t@invalid')
            git(repo, 'commit', '-q', '-m', 'x', env=env)
            rev = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
            f, kind, _ = resolve(repo, rev, 'n.md')
            case('resolve-knowledge', f == 'corpus/knowledge/n.md' and kind == 'line')
            case('resolve-missing', resolve(repo, rev, 'zz.md') == (None, None, None))
            case('resolve-external', resolve(repo, rev, '../P.md')[:2] == ('../P.md', 'external'))
            P = [{'heading': 'H', 'ordinal': 0, 'raw': 'n.md:2', 'pointer_kind': 'line', 'file': f,
                  'kind': 'line', 'ranges': [[2, 2]]}]
            good = {'rows': [{'heading': 'H', 'ordinal': 0, 'raw': 'n.md:2', 'file': f, 'ranges': [[2, 2]],
                              'verdict': 'holds', 'excerpt': 'quick brown fox jumps over the lazy'}]}
            r, _ = check_reads(repo, rev, repo, P, good)
            case('reads-ok', r == {'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 0,
                                   'absent': 0})
            r, _ = check_reads(repo, rev, repo, P, {'rows': []})
            case('reads-missing-row', r['unverified'] == 1)
            bad = json.loads(json.dumps(good)); bad['rows'][0]['excerpt'] = 'three and something else ok'
            r, _ = check_reads(repo, rev, repo, P, bad)
            case('reads-excerpt-outside-range', r['excerpt_miss'] == 1)
            short = json.loads(json.dumps(good)); short['rows'][0]['excerpt'] = 'quick brown'
            r, _ = check_reads(repo, rev, repo, P, short)
            case('reads-excerpt-too-short', r['excerpt_miss'] == 1)
            st = json.loads(json.dumps(good)); st['rows'][0]['verdict'] = 'stale'
            r, _ = check_reads(repo, rev, repo, P, st)
            case('reads-not-holds', r['not_holds'] == 1)
            dup = {'rows': good['rows'] * 2}
            r, _ = check_reads(repo, rev, repo, P, dup)
            case('reads-duplicate-row', r['unverified'] == 1)
            wrongf = json.loads(json.dumps(good)); wrongf['rows'][0]['ranges'] = [[1, 2]]
            r, _ = check_reads(repo, rev, repo, P, wrongf)
            case('reads-range-mismatch', r['unverified'] == 1)
            oor = [dict(P[0], ranges=[[2, 9]])]
            r, _ = check_reads(repo, rev, repo, oor, good)
            case('range-past-eof', r['unresolved'] == 1)
            nofile = [dict(P[0], file=None, kind=None)]
            r, _ = check_reads(repo, rev, repo, nofile, good)
            case('unresolved-no-file', r['unresolved'] == 1)
            ext = [dict(P[0], file='../corpus/knowledge/n.md', kind='external')]
            extrow = {'rows': [dict(good['rows'][0], file='../corpus/knowledge/n.md', fleet_commit=rev)]}
            r, _ = check_reads(repo, rev, repo, ext, extrow)
            case('external-ok', r['unresolved'] == 0 and r['excerpt_miss'] == 0)
            r, _ = check_reads(repo, rev, repo, ext, {'rows': [dict(good['rows'][0], file='../corpus/knowledge/n.md')]})
            case('external-needs-commit', r['unresolved'] == 1)
            with open(os.path.join(repo, 'corpus/SOURCES.md'), 'w') as fh:
                fh.write('| id | source |\n|---|---|\n| S001 | Alpha docs teach the lazy dog rule here | x |\n'
                         '  | S002 | Beta docs, indented row, teach something else entirely | y |\n')
            git(repo, 'add', '-A')
            git(repo, 'commit', '-q', '-m', 'y', env=env)
            rev2 = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
            sec = 'Uses `corpus/knowledge/n.md` and n.md:2 per S001 and S002; also `gone/old.py` and S999.'
            ex = extract(sec)
            kinds = [(p['kind'], p['raw']) for p in ex]
            case('extract-kinds', kinds == [('line', 'n.md:2'), ('path', 'corpus/knowledge/n.md'),
                                            ('path', 'gone/old.py'), ('sid', 'S001'), ('sid', 'S002'),
                                            ('sid', 'S999')])
            case('resolve-sid-indented', resolve(repo, rev2, 'S002', 'sid') == ('corpus/SOURCES.md', 'sid',
                                                                                [[4, 4]]))
            case('resolve-sid-missing', resolve(repo, rev2, 'S999', 'sid') == (None, None, None))
            pp = [{'heading': 'H', 'ordinal': 1, 'raw': 'corpus/knowledge/n.md', 'pointer_kind': 'path',
                   'file': 'corpus/knowledge/n.md', 'kind': 'path', 'ranges': None},
                  {'heading': 'H', 'ordinal': 2, 'raw': 'gone/old.py', 'pointer_kind': 'path', 'file': None,
                   'kind': None, 'ranges': None},
                  {'heading': 'H', 'ordinal': 3, 'raw': 'S001', 'pointer_kind': 'sid',
                   'file': 'corpus/SOURCES.md', 'kind': 'sid', 'ranges': [[3, 3]]}]
            rows = {'rows': [
                {'heading': 'H', 'ordinal': 1, 'raw': 'corpus/knowledge/n.md', 'file': 'corpus/knowledge/n.md',
                 'ranges': None, 'verdict': 'holds', 'excerpt': 'one the quick brown fox jumps'},
                {'heading': 'H', 'ordinal': 2, 'raw': 'gone/old.py', 'file': None, 'ranges': None,
                 'verdict': 'absent', 'excerpt': ''},
                {'heading': 'H', 'ordinal': 3, 'raw': 'S001', 'file': 'corpus/SOURCES.md', 'ranges': [[3, 3]],
                 'verdict': 'holds', 'excerpt': 'Alpha docs teach the lazy dog rule'}]}
            r, _ = check_reads(repo, rev2, repo, pp, rows)
            case('path-sid-absent-ok', r == {'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0,
                                             'not_holds': 0, 'absent': 1})
            r, _ = check_reads(repo, rev2, repo, pp[1:2], {'rows': []})
            case('absent-needs-row', r['unresolved'] == 1)
            badabs = {'rows': [dict(rows['rows'][0], verdict='absent')]}
            r, _ = check_reads(repo, rev2, repo, pp[:1], badabs)
            case('absent-on-resolved-is-not-holds', r['not_holds'] == 1)
            wrongsid = {'rows': [dict(rows['rows'][2], excerpt='Beta docs, indented row, teach')]}
            r, _ = check_reads(repo, rev2, repo, pp[2:], wrongsid)
            case('sid-excerpt-other-row', r['excerpt_miss'] == 1)
    failed = sum(1 for _, ok in cases if not ok)
    print('C1_R49_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--work')
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
        print('C1_R49: setup=unresolvable-rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    try:
        if a.list:
            pointers, missing = list_pointers(lane, rev)
            print(json.dumps({'rev': rev, 'missing_headings': missing, 'pointers': pointers}, indent=1,
                             ensure_ascii=False))
            return 0
        if not a.work:
            return 64
        work = os.path.realpath(a.work)
        os.makedirs(work, exist_ok=True)
        if os.listdir(work):
            print('C1_R49: setup=work-not-empty', file=sys.stderr)
            return 2
        fleet = os.path.realpath(a.fleet or os.path.dirname(lane))
        return measure(lane, rev, work, fleet)
    except Setup as exc:
        print('C1_R49: setup=%s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
