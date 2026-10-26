#!/usr/bin/env python3
"""Round-51 C1 (calibration) counter: mismatches between two of the lane's self-assessment records and repo state.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C1_R51_PASS=true iff total=0, where total = frontier_bad + status_conflicts + usedby_missing + (1 - readme_prefix),
  measured over committed bytes at REV:
  * frontier_bad — for each of F1..F10 in the frozen .ufo/evidence/round-51/c1/frontier-expected.json, the LAST
    markdown table in corpus/README.md whose header row starts `| id | ground |` and has a `status` column must hold
    exactly one row for Fk whose status cell opens with the expected status word (open | partly held | held | Core,
    optional ** emphasis), followed for every non-open status by `(round N)` with the expected N, and cites at least
    one `README.md:A` or `README.md:A-B` pointer (B-A <= 5) whose lines at REV, joined, contain the token Fk and the
    expected status phrase (case-insensitive). A missing, duplicated, mis-stated or unpointed row counts 1.
  * readme_prefix — corpus/README.md at base 9962033f is a byte prefix of corpus/README.md at REV (the coverage
    map is corrected by appending, never by rewriting the cells it supersedes).
  * status_conflicts — corpus/SOURCES.md rows (0-3 leading spaces, 11 cells) whose status is `queued` while used-by
    names a path, or `mined` while used-by names none (CORPUS.md: mined = cited by >= 1 path in used-by).
  * usedby_missing — used-by paths of mined rows that do not exist at REV.
Usage: measure.py --lane LANE --rev REV [--explain] | --selftest
Exit: 0 PASS · 1 not PASS · 2 setup error · 64 usage.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
BASE = '9962033fd7a75aa2f2847e979dd687a5d28505a1'
EXPECTED = '.ufo/evidence/round-51/c1/frontier-expected.json'
EXPECTED_SHA = None  # pinned in freeze.json; the deciding run checks the frozen bytes
ROW_RE = re.compile(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|')
STATUS_RE = re.compile(r'^\s*\**\s*(open|partly held|held|Core)\b\**(?:\s*\(round (\d+)\))?', re.I)
PTR_RE = re.compile(r'README\.md:(\d+)(?:-(\d+))?')


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return e


def git(lane, *args, check=True):
    r = subprocess.run(['git', '-C', lane, *args], capture_output=True, env=env())
    if check and r.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(args), r.stderr.decode(errors='replace').strip()))
    return r


def show(lane, rev, path):
    r = git(lane, 'show', '%s:%s' % (rev, path), check=False)
    return r.stdout if r.returncode == 0 else None


def exists(lane, rev, path):
    return git(lane, 'cat-file', '-e', '%s:%s' % (rev, path), check=False).returncode == 0


def cells(line):
    s = line.strip()
    if not s.startswith('|'):
        return None
    s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def last_frontier_table(lines):
    """Return (header_cells, [(lineno, cells)]) of the last table whose header starts | id | ground |."""
    found = None
    i = 0
    while i < len(lines):
        c = cells(lines[i])
        if c and len(c) >= 2 and c[0].lower() == 'id' and c[1].lower() == 'ground' and i + 1 < len(lines) \
                and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith('|'):
                rows.append((j + 1, cells(lines[j])))
                j += 1
            found = ([x.lower() for x in c], rows)
            i = j
            continue
        i += 1
    return found


def phrase_of(status):
    return {'open': 'open', 'partly held': 'partly held', 'held': 'held', 'core': 'core'}[status.lower()]


def frontier(lines, expected, explain):
    bad = 0
    table = last_frontier_table(lines)
    if table is None:
        for k in expected:
            explain.append('FRONTIER %s: no-table' % k)
        return len(expected), 0
    header, rows = table
    if 'status' not in header:
        for k in expected:
            explain.append('FRONTIER %s: no-status-column' % k)
        return len(expected), table and len(rows)
    si = header.index('status')
    for k, want in expected.items():
        mine = [(n, c) for n, c in rows if c and c[0].strip('* ') == k]
        if len(mine) != 1:
            bad += 1
            explain.append('FRONTIER %s: rows=%d' % (k, len(mine)))
            continue
        n, c = mine[0]
        cell = c[si] if si < len(c) else ''
        m = STATUS_RE.match(cell)
        if not m:
            bad += 1
            explain.append('FRONTIER %s: line %d status-unparsed' % (k, n))
            continue
        word, rnd = m.group(1).lower(), m.group(2)
        if word != want['status'].lower():
            bad += 1
            explain.append('FRONTIER %s: line %d status=%s want=%s' % (k, n, word, want['status']))
            continue
        if want['status'].lower() != 'open' and (rnd is None or int(rnd) != want['round']):
            bad += 1
            explain.append('FRONTIER %s: line %d round=%s want=%s' % (k, n, rnd, want['round']))
            continue
        ok_ptr = False
        tok = re.compile(r'\b%s\b' % re.escape(k))
        for p in PTR_RE.finditer(cell):
            a = int(p.group(1))
            b = int(p.group(2)) if p.group(2) else a
            if a < 1 or b < a or b - a > 5 or b > len(lines):
                continue
            text = ' '.join(lines[a - 1:b])
            if tok.search(text) and phrase_of(want['status']) in text.lower():
                ok_ptr = True
                break
        if not ok_ptr:
            bad += 1
            explain.append('FRONTIER %s: line %d no-supporting-pointer' % (k, n))
            continue
        explain.append('FRONTIER %s: ok line %d' % (k, n))
    return bad, len(rows)


def sources(lane, rev, text, explain):
    conflicts = missing = nrows = 0
    for line in text.splitlines():
        if not ROW_RE.match(line):
            continue
        c = cells(line)
        if c is None or len(c) != 11:
            continue
        nrows += 1
        sid, status, used = c[0], c[7], c[10]
        paths = [p.strip() for p in re.split(r'[,;]', used) if p.strip() and p.strip() not in ('—', '-')]
        if status == 'queued' and paths:
            conflicts += 1
            explain.append('SOURCES %s: queued-with-used-by %s' % (sid, ','.join(paths)))
        elif status == 'mined' and not paths:
            conflicts += 1
            explain.append('SOURCES %s: mined-without-used-by' % sid)
        if status == 'mined':
            for p in paths:
                if not exists(lane, rev, p):
                    missing += 1
                    explain.append('SOURCES %s: used-by-missing %s' % (sid, p))
    return nrows, conflicts, missing


def measure(lane, rev, expected_path=None):
    explain = []
    rev = git(lane, 'rev-parse', '--verify', rev + '^{commit}').stdout.decode().strip()
    exp_bytes = show(lane, rev, EXPECTED) if expected_path is None else open(expected_path, 'rb').read()
    if exp_bytes is None:
        raise RuntimeError('expected file missing at REV')
    expected = json.loads(exp_bytes)['rows']
    readme = show(lane, rev, 'corpus/README.md')
    base_readme = show(lane, BASE, 'corpus/README.md') if git(lane, 'cat-file', '-e', BASE, check=False).returncode == 0 else None
    if readme is None:
        raise RuntimeError('corpus/README.md missing at REV')
    prefix = 1 if (base_readme is not None and readme.startswith(base_readme)) else 0
    if not prefix:
        explain.append('README not-append-only (base bytes are not a prefix)')
    lines = readme.decode('utf-8', 'surrogateescape').split('\n')
    fbad, trows = frontier(lines, expected, explain)
    src = show(lane, rev, 'corpus/SOURCES.md')
    if src is None:
        raise RuntimeError('corpus/SOURCES.md missing at REV')
    nrows, conflicts, missing = sources(lane, rev, src.decode('utf-8', 'surrogateescape'), explain)
    total = fbad + conflicts + missing + (1 - prefix)
    line = ('C1_R51: rev=%s frontier_rows=%d table_rows=%d frontier_bad=%d readme_prefix=%d sources_rows=%d '
            'status_conflicts=%d usedby_missing=%d total=%d C1_R51_PASS=%s'
            % (rev, len(expected), trows or 0, fbad, prefix, nrows, conflicts, missing, total,
               'true' if total == 0 else 'false'))
    return total, line, explain


def selftest():
    """End-to-end through measure() on throwaway repos: base-like FAIL, appended-correct PASS, rewrite FAIL."""
    cases = failed = 0
    root = tempfile.mkdtemp(prefix='tameshi-r51-c1-selftest-', dir=os.environ.get('TMPDIR') or None)
    try:
        def mk(name, readme_parts, sources_rows):
            d = os.path.join(root, name)
            os.makedirs(os.path.join(d, 'corpus/knowledge'))
            os.makedirs(os.path.join(d, '.ufo/evidence/round-51/c1'))
            g = lambda *a: subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, env=env())
            g('init', '-q')
            if subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, env=env()).stdout.decode().strip() != os.path.realpath(d):
                raise RuntimeError('fixture toplevel mismatch')
            exp = {'rows': {'F1': {'status': 'held', 'round': 5}, 'F2': {'status': 'open', 'round': None}}}
            open(os.path.join(d, EXPECTED), 'w').write(json.dumps(exp))
            open(os.path.join(d, 'corpus/knowledge/e.md'), 'w').write('x\n')
            hdr = '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
            open(os.path.join(d, 'corpus/SOURCES.md'), 'w').write(hdr + ''.join(sources_rows))
            open(os.path.join(d, 'corpus/README.md'), 'w').write(readme_parts[0])
            g('add', '-A'); g('-c', 'user.name=selftest', '-c', 'user.email=selftest@invalid', 'commit', '-qm', 'base')
            b = g('rev-parse', 'HEAD').stdout.decode().strip()
            if len(readme_parts) > 1:
                open(os.path.join(d, 'corpus/README.md'), 'w').write(readme_parts[1])
                g('add', '-A'); g('-c', 'user.name=selftest', '-c', 'user.email=selftest@invalid', 'commit', '-qm', 'after')
            return d, b
        base = ('| id | ground | status |\n|---|---|---|\n| F1 | a | open |\n| F2 | b | open |\n\n'
                'F1 moves: open → held (round 5).\nF2 stays open.\n')
        good = base + ('\n| id | ground | status |\n|---|---|---|\n| F1 | a | held (round 5) — README.md:6 |\n'
                       '| F2 | b | open — README.md:7 |\n')
        nopt = base + '\n| id | ground | status |\n|---|---|---|\n| F1 | a | held (round 5) |\n| F2 | b | open |\n'
        rewrite = base.replace('| F1 | a | open |', '| F1 | a | held (round 5) — README.md:6 |').replace('| F2 | b | open |', '| F2 | b | open — README.md:7 |')
        row_ok = '| S001 | s | docs | A | x | y | z | mined | 2026-10-26 | 90d | corpus/knowledge/e.md |\n'
        row_q = '| S002 | s | docs | A | x | y | z | queued | 2026-10-26 | 90d | corpus/knowledge/e.md |\n'
        row_gone = '  | S003 | s | docs | A | x | y | z | mined | 2026-10-26 | 90d | corpus/knowledge/gone.md |\n'
        plan = [
            ('base-stale-table', [base], [row_ok], 1, 'frontier_bad=2'),
            ('appended-correct', [base, good], [row_ok], 0, 'total=0 C1_R51_PASS=true'),
            ('appended-no-pointer', [base, nopt], [row_ok], 1, 'frontier_bad=2'),
            ('rewritten-in-place', [base, rewrite], [row_ok], 1, 'readme_prefix=0'),
            ('queued-with-used-by', [base, good], [row_ok, row_q], 1, 'status_conflicts=1'),
            ('indented-mined-missing-path', [base, good], [row_ok, row_gone], 1, 'usedby_missing=1'),
        ]
        global BASE
        saved = BASE
        for name, parts, rows, want_rc, want in plan:
            cases += 1
            d, b = mk(name, parts, rows)
            BASE = b
            try:
                total, line, _ = measure(d, 'HEAD')
                rc = 0 if total == 0 else 1
            finally:
                BASE = saved
            if rc != want_rc or want not in line:
                failed += 1
                print('C1_R51_SELFTEST FAIL %s: rc=%d %s' % (name, rc, line))
    finally:
        subprocess.run(['rm', '-rf', '--', root])
    print('C1_R51_SELFTEST: cases=%d failed=%d' % (cases, failed))
    return 0 if failed == 0 else 1


def main(argv):
    if argv == ['--selftest']:
        return selftest()
    if len(argv) < 4 or argv[0] != '--lane' or argv[2] != '--rev' or (len(argv) == 5 and argv[4] != '--explain') or len(argv) > 5:
        print('usage: measure.py --lane LANE --rev REV [--explain] | --selftest', file=sys.stderr)
        return 64
    try:
        total, line, explain = measure(os.path.realpath(argv[1]), argv[3])
    except (RuntimeError, ValueError, KeyError) as exc:
        print('C1_R51: SETUP (%s)' % exc)
        return 2
    if len(argv) == 5:
        for e in explain:
            print(e)
    print(line)
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
