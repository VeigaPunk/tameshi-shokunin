#!/usr/bin/env python3
"""Round-47 C1 (calibration) counter: the standing SCORECARD self-assessment states what it
depends on, not only what it prints.

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C1_R47_PASS=true iff self_pin=1, stmts_pin=1, statements=22, append_only=1, unpinned=0 and
  total=0, where total = mismatches + unparsed + unobservable + dep_mismatch over the 22 frozen
  statements of statements.json, and for each statement:
  * its standing row is the LAST data row, in file order, of any SCORECARD.md table of its kind
    whose first cell equals the statement id (kind `cap`: header cell 1 `Capability`; kind `axis`:
    header cell 2 begins `Score`; tables inside fenced code blocks or HTML comments are ignored);
  * `cap` row claim, in the evidence cell (cell 3):
        `CMD` -> `PRINTED LINE`, exit N, tool sha256 `12 hex`, deps `LIST`
    (the arrow is U+2192); `axis` row claim: the integer in cell 2 plus, in cell 3,
        tool sha256 `12 hex` and deps `LIST`. A row without all parts is `unparsed`;
  * the claim (line, exit, sha / score, sha) must equal what the statement's command prints under
    profile P0 (the live host environment, as round 46 observed it) with the sha256 prefix of the
    pinned tool file at REV, else `mismatch`; a command with no matching line is `unobservable`;
  * LIST is `none` or a sorted comma list over {bwrap, env, fleet-root, jj, node}; it must equal
    the OBSERVED dependence set, else `dep_mismatch`. A dependence is observed when the statement's
    (picked line, exit code) under the variant differs from its tuple under the clean full profile
    P1: `env` = P0 differs from P1 (clean env: fresh HOME, LANG=C, LC_ALL=C, TZ=UTC, PATH shim of
    /usr/bin plus node, jj, jq); `bwrap`/`jj`/`node` = P1 with that executable removed from the PATH
    shim; `fleet-root` = P1 run inside `bwrap --bind / / --dev-bind /dev /dev --bind DECOY /home/vgpnk/Projects/shokunin`
    where DECOY holds only a stub scripts/sources-census.sh that exits 7 (a statement that reads
    anything under the real fleet root changes);
  * `unpinned` counts statements whose statements.json entry has no `sha_file`.
  statements.json at REV must hash to STATEMENTS_SHA256 (stmts_pin) and the base SCORECARD.md must
  be a byte prefix of REV's (append_only).
Modes: --lane L --rev R --base B --work EMPTY_DIR (deciding); --emit (same, prints the standing rows
the observed values imply); --selftest.
"""
import argparse
import concurrent.futures
import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-47/calibration/measure.py'
STATEMENTS_PATH = '.ufo/evidence/round-47/calibration/statements.json'
STATEMENTS_SHA256 = '924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56'
N_STATEMENTS = 22
FLEET = '/home/vgpnk/Projects/shokunin'
ARROW = '\u2192'
DEP_NAMES = ('bwrap', 'env', 'fleet-root', 'jj', 'node')
CLAIM_CAP = (ARROW + r'\s*`([^`]+)`,\s*exit (\d+),\s*tool sha256 `([0-9a-f]{12})`,\s*deps `([a-z,-]+)`')
SHA_RE = re.compile(r'tool sha256 `([0-9a-f]{12})`')
DEPS_RE = re.compile(r'deps `([a-z,-]+)`')
VARIANTS = (('bwrap', 'P2'), ('jj', 'P3'), ('node', 'P4'), ('fleet-root', 'P5'))
PROFILES = ('P0', 'P1', 'P2', 'P3', 'P4', 'P5')
STUB = '#!/bin/sh\necho "decoy fleet root: census stub" >&2\nexit 7\n'


def host_env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e


def git(*args, binary=False):
    out = subprocess.run(['git'] + list(args), capture_output=True, env=host_env())
    if out.returncode != 0:
        return None
    return out.stdout if binary else out.stdout.decode('utf-8', 'replace')


def strip_hidden(text):
    """Blank fenced code blocks and HTML comments, keeping line numbering."""
    text = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    out, fenced = [], False
    for line in text.split('\n'):
        if line.lstrip().startswith('```'):
            fenced = not fenced
            out.append('')
            continue
        out.append('' if fenced else line)
    return out


def tables(lines):
    i = 0
    while i < len(lines):
        if lines[i].startswith('|'):
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                j += 1
            block = lines[i:j]
            header = [c.strip() for c in block[0].strip().strip('|').split('|')]
            yield header, block[2:]
            i = j
        else:
            i += 1


def cells_of(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def last_rows(text):
    rows = {}
    for header, body in tables(strip_hidden(text)):
        if header and header[0] == 'Capability':
            kind = 'cap'
        elif len(header) > 1 and header[1].startswith('Score'):
            kind = 'axis'
        else:
            continue
        for line in body:
            cells = cells_of(line)
            rows[(kind, cells[0])] = cells
    return rows


def claim_of(stmt, cells):
    """Return (value-tuple, declared-deps frozenset) or None when the row is absent or incomplete."""
    if cells is None:
        return None
    evidence = cells[2] if len(cells) > 2 else ''
    deps = DEPS_RE.search(evidence)
    if deps is None:
        return None
    names = deps.group(1).split(',')
    declared = frozenset() if names == ['none'] else frozenset(names)
    if stmt['kind'] == 'axis':
        sha = SHA_RE.search(evidence)
        if not (len(cells) > 1 and re.fullmatch(r'\d+', cells[1]) and sha):
            return None
        return (cells[1], sha.group(1)), declared
    m = re.search(CLAIM_CAP, evidence)
    return (tuple(m.groups()[:3]), declared) if m else None


def pick_line(stmt, out):
    pat = stmt['obs']
    if pat == 'census':
        rows = re.search(r'^== A rows\n(\d+)$', out, re.M)
        ok = re.search(r'^(SOURCES_CENSUS: CLEAN \(contract v1 \+ H4 id-or-path\))$', out, re.M)
        return ('rows=%s %s' % (rows.group(1), ok.group(1))) if rows and ok else None
    if pat == 'monitor':
        try:
            return str(json.loads(out)['calibration_restraint_score'])
        except (ValueError, KeyError, TypeError):
            return None
    m = re.search(pat, out, re.M)
    return m.group(1) if m else None


def build_shim(path, drop=()):
    os.makedirs(path)
    seen = set()
    sources = ['/usr/bin']
    for d in sources:
        for name in sorted(os.listdir(d)):
            if name in drop or name in seen:
                continue
            seen.add(name)
            try:
                os.symlink(os.path.join(d, name), os.path.join(path, name))
            except OSError:
                pass
    for tool in ('node', 'jj', 'jq'):
        found = shutil.which(tool)
        if found and tool not in drop and tool not in seen:
            seen.add(tool)
            os.symlink(os.path.realpath(found), os.path.join(path, tool))


def profile_env(work, prof, rev):
    if prof == 'P0':
        e = host_env()
        e['REV'] = rev
        return e
    drop = {'P2': ('bwrap',), 'P3': ('jj',), 'P4': ('node',)}.get(prof, ())
    shim = os.path.join(work, prof, 'shim')
    build_shim(shim, drop)
    home = os.path.join(work, prof, 'home')
    tmp = os.path.join(work, prof, 'tmp')
    os.makedirs(home)
    os.makedirs(tmp)
    return {'PATH': shim, 'HOME': home, 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC', 'TMPDIR': tmp,
            'PYTHONDONTWRITEBYTECODE': '1', 'REV': rev}


def setup_profile(lane, rev, work, prof):
    base = os.path.join(work, prof)
    os.makedirs(os.path.join(base, 'fleet'), exist_ok=True)
    for d in sorted(os.listdir(FLEET)):
        if d.endswith('-shokunin') and d != os.path.basename(lane) and os.path.isdir(os.path.join(FLEET, d)):
            os.symlink(os.path.join(FLEET, d), os.path.join(base, 'fleet', d))
    mirror = os.path.join(base, 'fleet', os.path.basename(lane))
    clone = os.path.join(base, 'clone')
    for dest in (mirror, clone):
        if subprocess.run(['git', 'clone', '-q', '--no-hardlinks', lane, dest], capture_output=True, env=host_env()).returncode \
                or subprocess.run(['git', '-C', dest, 'checkout', '-q', '--detach', rev], capture_output=True, env=host_env()).returncode:
            return None
    return clone, mirror


def observe(stmt, prof, ctx):
    clone, mirror, rev, work, env, decoy = ctx
    cwd = mirror if stmt['cwd'] == 'mirror' else clone
    argv = [a.format(work=os.path.join(work, prof), clone=clone, rev=rev) for a in stmt['argv']]
    if prof == 'P5':
        argv = ['/usr/bin/bwrap', '--die-with-parent', '--bind', '/', '/', '--dev-bind', '/dev', '/dev', '--bind', decoy, FLEET, '--'] + argv
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=stmt['timeout'], env=env)
    except subprocess.TimeoutExpired:
        return None, 'timeout'
    out = p.stdout + ('\n' + p.stderr if p.stderr else '')
    name = re.sub(r'\W+', '-', stmt['id'])
    with open(os.path.join(work, prof, 'obs-%s.stdout' % name), 'w') as fh:
        fh.write(out[-200000:])
    line = pick_line(stmt, out)
    if line is None:
        return None, 'exit=%d' % p.returncode
    if stmt['kind'] == 'axis':
        obs = [line]
    else:
        obs = [line, str(p.returncode)]
    if stmt.get('sha_file'):
        data = git('-C', clone, 'show', 'HEAD:%s' % stmt['sha_file'], binary=True)
        obs.append(hashlib.sha256(data).hexdigest()[:12] if data is not None else 'absent')
    return tuple(obs), 'exit=%d' % p.returncode


def comparable(result, kind):
    """The part of an observation a dependence is read from: the picked line (and, for a cap, the exit code)."""
    obs, note = result
    if obs is None:
        return ('UNOBSERVABLE', note)
    return obs[:2] if kind == 'cap' else obs[:1]


def measure(lane, rev, base, work, emit=False, pin=STATEMENTS_SHA256, n_expected=N_STATEMENTS, jobs=14, only=None):
    work = os.path.abspath(work)
    if os.path.exists(work) and os.listdir(work):
        print('C1_R47: --work must be empty or absent', file=sys.stderr)
        return 2
    os.makedirs(work, exist_ok=True)
    r = git('-C', lane, 'rev-parse', '--verify', rev + '^{commit}')
    if r is None:
        print('C1_R47: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.strip()
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = git('-C', lane, 'show', '%s:%s' % (rev, SELF_PATH), binary=True)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    raw = git('-C', lane, 'show', '%s:%s' % (rev, STATEMENTS_PATH), binary=True)
    stmts_pin = int(raw is not None and hashlib.sha256(raw).hexdigest() == pin)
    if raw is None:
        print('C1_R47: statements.json absent at rev', file=sys.stderr)
        return 2
    statements = json.loads(raw)['statements']
    if only:
        statements = [s for s in statements if s['id'] in only]
        if not statements:
            print('C1_R47: --only names no statement', file=sys.stderr)
            return 2
    base_sc = git('-C', lane, 'show', '%s:SCORECARD.md' % base)
    rev_sc = git('-C', lane, 'show', '%s:SCORECARD.md' % rev)
    if base_sc is None or rev_sc is None:
        print('C1_R47: cannot read SCORECARD.md', file=sys.stderr)
        return 2
    append_only = int(rev_sc.startswith(base_sc))
    decoy = os.path.join(work, 'decoy')
    os.makedirs(os.path.join(decoy, 'scripts'))
    with open(os.path.join(decoy, 'scripts', 'sources-census.sh'), 'w') as fh:
        fh.write(STUB)
    os.chmod(os.path.join(decoy, 'scripts', 'sources-census.sh'), 0o755)
    ctxs = {}
    for prof in PROFILES:
        made = setup_profile(lane, rev, work, prof)
        if made is None:
            print('C1_R47: clone/checkout failed', file=sys.stderr)
            return 2
        ctxs[prof] = (made[0], made[1], rev, work, profile_env(work, prof, rev), decoy)
    rows = last_rows(rev_sc)
    results = {}
    order = sorted(statements, key=lambda s: -s['timeout'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futs = {}
        for s in order:
            for prof in PROFILES:
                futs[(s['id'], prof)] = pool.submit(observe, s, prof, ctxs[prof])
        for key, f in futs.items():
            results[key] = f.result()
    mism = unparsed = unobs = depm = 0
    unpinned = sum(1 for s in statements if not s.get('sha_file'))
    emitted = []
    for s in statements:
        sid = s['id']
        observed, note = results[(sid, 'P0')]
        ref = comparable(results[(sid, 'P1')], s['kind'])
        observed_deps = set()
        if comparable(results[(sid, 'P0')], s['kind']) != ref:
            observed_deps.add('env')
        for dep, prof in VARIANTS:
            if comparable(results[(sid, prof)], s['kind']) != ref:
                observed_deps.add(dep)
        claim = claim_of(s, rows.get((s['kind'], sid)))
        if observed is None:
            verdict = 'UNOBSERVABLE'
            unobs += 1
        elif claim is None:
            verdict = 'UNPARSED'
            unparsed += 1
        else:
            verdict = 'MATCH' if tuple(claim[0]) == tuple(observed) else 'MISMATCH'
            mism += verdict == 'MISMATCH'
        dep_note = 'DEPS-OK'
        if claim is not None and claim[1] != observed_deps:
            dep_note = 'DEPS-MISMATCH'
            depm += 1
        print('STATEMENT %s/%s: claimed=%s observed=%s (%s) %s declared_deps=%s observed_deps=%s %s' % (
            s['kind'], sid, '|'.join(claim[0]) if claim else '-', '|'.join(observed) if observed else '-', note, verdict,
            ','.join(sorted(claim[1])) or 'none' if claim else '-', ','.join(sorted(observed_deps)) or 'none', dep_note))
        print('PROFILES %s: %s' % (sid, ' '.join('%s=%s' % (p, '|'.join(map(str, comparable(results[(sid, p)], s['kind'])))) for p in PROFILES)))
        if emit and observed is not None:
            emitted.append((s, observed, rows.get((s['kind'], sid)), observed_deps))
    total = mism + unparsed + unobs + depm + unpinned
    passed = (self_pin == 1 and stmts_pin == 1 and len(statements) == n_expected and append_only == 1 and total == 0
              and not only)
    if emit:
        for s, observed, old, deps in emitted:
            print(emit_row(s, observed, old, deps))
    print('C1_R47%s: self_pin=%d stmts_pin=%d statements=%d mismatches=%d unparsed=%d unobservable=%d dep_mismatch=%d '
          'unpinned=%d append_only=%d total=%d rev=%s C1_R47_PASS=%s' % (
              '_PARTIAL' if only else '', self_pin, stmts_pin, len(statements), mism, unparsed, unobs, depm, unpinned, append_only, total, rev,
              'true' if passed else 'false'))
    return 0 if passed else 1


def emit_row(stmt, observed, old, deps):
    dep_text = ','.join(sorted(deps)) or 'none'
    if stmt['kind'] == 'axis':
        what = old[2] if old and len(old) > 2 else 'see the evidence pointer in the round-47 SCORECARD block'
        what = SHA_RE.sub('', DEPS_RE.sub('', what)).rstrip(' ,')
        return 'EMIT_AXIS | %s | %s | %s, tool sha256 `%s`, deps `%s` |' % (stmt['id'], observed[0], what, observed[1], dep_text)
    evidence = '`%s` %s `%s`, exit %s, tool sha256 `%s`, deps `%s`' % (stmt['cmd_text'], ARROW, observed[0], observed[1], observed[2], dep_text)
    what = old[1] if old and len(old) > 1 else (stmt.get('what') or '')
    first = old[3] if old and len(old) > 3 else (stmt.get('first') or '')
    return 'EMIT_CAP | %s | %s | %s | %s |' % (stmt['id'], what, evidence, first)


def selftest():
    env0 = host_env()
    env0.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    me = os.path.abspath(__file__)
    cap_hdr = '| Capability | What | Evidence | First |\n|---|---|---|---|\n'
    axis_hdr = '\n| Axis | Score (0\u201310) | Rule | Commit | Round |\n|---|---|---|---|---|\n'
    base_sc = '# S\n\nintro\n'
    tool_sha = hashlib.sha256(b'tool\n').hexdigest()[:12]

    def stmt(sid, argv, obs, kind='cap', cwd='clone'):
        return dict(id=sid, kind=kind, argv=argv, obs=obs, cmd_text=sid, sha_file='tool.txt', cwd=cwd, timeout=60)

    stmts = [
        stmt('alpha', ['echo', 'ALPHA: 3/3 pass'], r'^(ALPHA: \d+/\d+ pass)'),
        stmt('beta', ['sh', '-c', 'echo BETA: 5/5 pass; exit 3'], r'^(BETA: \d+/\d+ pass)'),
        stmt('score', ['echo', 'value=7'], r'value=(\d+)', kind='axis'),
    ]
    dep_stmts = {
        'bwrap': stmt('gamma', ['sh', '-c', 'if command -v bwrap >/dev/null; then echo G: has; else echo G: lacks; fi'], r'^(G: \w+)'),
        'jj': stmt('gamma', ['sh', '-c', 'if command -v jj >/dev/null; then echo G: has; else echo G: lacks; fi'], r'^(G: \w+)'),
        'node': stmt('gamma', ['sh', '-c', 'if command -v node >/dev/null; then echo G: has; else echo G: lacks; fi'], r'^(G: \w+)'),
        'fleet-root': stmt('gamma', ['sh', '-c', 'if test -e %s/MISSION.md; then echo G: has; else echo G: lacks; fi' % FLEET], r'^(G: \w+)'),
        'env': stmt('gamma', ['sh', '-c', 'echo G: $(basename "$HOME")'], r'^(G: \S+)'),
    }

    def row_cap(sid, line, code, sha=tool_sha, deps='none', arrow=ARROW):
        return '| %s | w | `%s` %s `%s`, exit %d, tool sha256 `%s`, deps `%s` | r1 |\n' % (sid, sid, arrow, line, code, sha, deps)

    def row_score(v='7', sha=tool_sha, deps='none'):
        return '| score | %s | rule, tool sha256 `%s`, deps `%s` | c | r |\n' % (v, sha, deps)

    def doc(*caps, score=None):
        return base_sc + '\n' + cap_hdr + ''.join(caps) + '\n' + axis_hdr + (score if score is not None else row_score())

    A = lambda **k: row_cap('alpha', 'ALPHA: 3/3 pass', 0, **k)
    B = lambda **k: row_cap('beta', 'BETA: 5/5 pass', 3, **k)
    good = doc(A(), B())
    cases = [
        ('T01_all_match', good, {}, 'total=0'),
        ('T02_value_mismatch', doc(row_cap('alpha', 'ALPHA: 2/3 pass', 0), B()), {}, 'mismatches=1'),
        ('T03_exit_mismatch', doc(row_cap('alpha', 'ALPHA: 3/3 pass', 1), B()), {}, 'mismatches=1'),
        ('T04_sha_mismatch', doc(A(), B(sha='0' * 12)), {}, 'mismatches=1'),
        ('T05_axis_mismatch', doc(A(), B(), score=row_score('6')), {}, 'mismatches=1'),
        ('T06_absent_row_unparsed', doc(A()), {}, 'unparsed=1'),
        ('T07_prose_claim_unparsed', base_sc + cap_hdr + '| alpha | w | it passes 3/3 | r1 |\n' + B() + axis_hdr + row_score(), {}, 'unparsed=1'),
        ('T08_last_row_wins_stale_first', base_sc + cap_hdr + row_cap('alpha', 'ALPHA: 1/3 pass', 0) + B() + '\n' + cap_hdr + A() + '\n'
         + axis_hdr + row_score(), {}, 'total=0'),
        ('T09_last_row_wins_stale_last', base_sc + cap_hdr + A() + B() + '\n' + cap_hdr + row_cap('alpha', 'ALPHA: 1/3 pass', 0) + '\n'
         + axis_hdr + row_score(), {}, 'mismatches=1'),
        ('T10_fenced_table_ignored', base_sc + '```\n' + cap_hdr + row_cap('alpha', 'ALPHA: 9/9 pass', 0) + '```\n' + cap_hdr + A() + B()
         + axis_hdr + row_score(), {}, 'total=0'),
        ('T11_html_comment_table_ignored', base_sc + '<!--\n' + cap_hdr + row_cap('alpha', 'ALPHA: 9/9 pass', 0) + '-->\n' + cap_hdr + A() + B()
         + axis_hdr + row_score(), {}, 'total=0'),
        ('T12_unobservable_command', good, {'argv0': ['sh', '-c', 'echo nothing useful']}, 'unobservable=1'),
        ('T13_append_only_broken', good, {'base_override': '# other base\n'}, 'append_only=0'),
        ('T14_statements_tampered_is_false', good, {'tamper': True}, 'C1_R47_PASS=false'),
        ('T15_self_pin_broken', good, {'selfbytes': b'# not the counter\n'}, 'self_pin=0'),
        ('T16_wrong_statement_count_is_false', good, {'drop': True}, 'C1_R47_PASS=false'),
        ('T17_axis_noninteger_unparsed', doc(A(), B(), score=row_score('seven')), {}, 'unparsed=1'),
        ('T18_match_is_true', good, {}, 'C1_R47_PASS=true'),
        ('T19_missing_deps_clause_unparsed', doc(re.sub(r', deps `none`', '', A()), B()), {}, 'unparsed=1'),
        ('T20_axis_row_without_sha_unparsed', doc(A(), B(), score='| score | 7 | rule, deps `none` | c | r |\n'), {}, 'unparsed=1'),
        ('T21_statement_without_sha_file_unpinned', good, {'nosha': True}, 'unpinned=1'),
        ('T22_overdeclared_dependence', doc(A(deps='bwrap'), B()), {}, 'dep_mismatch=1'),
        ('T23_unsorted_unknown_dep_name_unparsed', doc(A(deps='Bwrap'), B()), {}, 'unparsed=1'),
    ]
    cases.append(('T26_only_probe_never_passes', good, {'only': ['alpha']}, 'C1_R47_PASS=false'))
    cases.append(('T27_only_probe_is_labelled_partial', good, {'only': ['alpha']}, 'C1_R47_PARTIAL:'))
    for dep in ('bwrap', 'jj', 'node', 'fleet-root', 'env'):
        cases.append(('T24_undeclared_%s_dependence' % dep, 'dep:' + dep + ':none', {'dep': dep}, 'dep_mismatch=1'))
        cases.append(('T25_declared_%s_dependence_matches' % dep, 'dep:' + dep + ':' + dep, {'dep': dep}, 'dep_mismatch=0'))
    failed = 0
    for name, scorecard, opt, want in cases:
        with tempfile.TemporaryDirectory(prefix='tameshi-r47-c1-') as d:
            lane = os.path.join(d, 'lane')
            os.makedirs(lane)

            def g(*a):
                subprocess.run(['git', '-C', lane, *a], env=env0, capture_output=True, check=True)
            g('init', '-q', '-b', 'm')
            assert subprocess.run(['git', '-C', lane, 'rev-parse', '--show-toplevel'], capture_output=True,
                                  env=env0).stdout.decode().strip() == os.path.realpath(lane)
            st = [dict(s) for s in stmts]
            if scorecard.startswith('dep:'):
                _, dep, declared = scorecard.split(':')
                st = [dep_stmts[dep]]
                observed_line = None
                # the row's claim value is whatever the live host prints for the statement
                probe = subprocess.run(dep_stmts[dep]['argv'], capture_output=True, text=True, env=env0)
                observed_line = re.search(dep_stmts[dep]['obs'], probe.stdout, re.M).group(1)
                scorecard = base_sc + '\n' + cap_hdr + row_cap('gamma', observed_line, 0, deps=declared)
            if 'argv0' in opt:
                st[0]['argv'] = opt['argv0']
            if opt.get('drop'):
                st = st[:2]
            if opt.get('nosha'):
                st[0]['sha_file'] = None
            payload = json.dumps(dict(statements=st), indent=1).encode()
            os.makedirs(os.path.join(lane, os.path.dirname(SELF_PATH)))
            with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
                fh.write(base_sc)
            with open(os.path.join(lane, 'tool.txt'), 'wb') as fh:
                fh.write(b'tool\n')
            with open(os.path.join(lane, STATEMENTS_PATH), 'wb') as fh:
                fh.write(payload)
            with open(os.path.join(lane, SELF_PATH), 'wb') as fh:
                fh.write(opt.get('selfbytes') or open(me, 'rb').read())
            g('add', '-A')
            g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base')
            base_arg = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            if 'base_override' in opt:
                with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
                    fh.write(opt['base_override'])
                g('add', '-A')
                g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'other base')
                base_arg = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
                fh.write(scorecard)
            if opt.get('tamper'):
                with open(os.path.join(lane, STATEMENTS_PATH), 'ab') as fh:
                    fh.write(b' ')
            g('add', '-A')
            g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'rev')
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                measure(lane, 'HEAD', base_arg, os.path.join(d, 'work'), pin=hashlib.sha256(payload).hexdigest(),
                        n_expected=len(st) if not opt.get('drop') else 3, only=set(opt['only']) if opt.get('only') else None)
            lines = [l for l in buf.getvalue().splitlines() if l.startswith('C1_R47:') or l.startswith('C1_R47_PARTIAL:')]
            line = lines[-1] if lines else 'NO-C1-LINE'
            ok = want in line
            failed += not ok
            print('%s %s want=%r got=%s' % ('PASS' if ok else 'FAIL', name, want, line))
    print('C1_R47_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--base')
    ap.add_argument('--work')
    ap.add_argument('--emit', action='store_true')
    ap.add_argument('--only', help='seat probe: comma-separated statement ids; the verdict line is C1_R47_PARTIAL with PASS=false')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.base and a.work):
        ap.error('--lane, --rev, --base and --work are required')
    return measure(a.lane, a.rev, a.base, a.work, emit=a.emit, only=set(a.only.split(',')) if a.only else None)


if __name__ == '__main__':
    sys.exit(main())
