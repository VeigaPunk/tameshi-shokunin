#!/usr/bin/env python3
"""Round-48 C1 (calibration) counter: the standing SCORECARD self-assessment is restated from
R=3 repeated observation rounds and declares a value class, a tool sha256 and a deps set.

Frozen predicate (the same sentence as the round-48 contract; the receipt label is C1_R48_PASS):
  At REV, for each of the 22 frozen statements, the standing row (the last data row of a
  SCORECARD.md table of its kind whose first cell is the statement id AND whose evidence cell
  carries a `runs 3` clause) declares a value set V (one member: `stable`; two or three members:
  `nondeterministic`), the tool sha256 prefix and a deps set D, such that over R=3 observation
  rounds of the six profiles P0-P5: every observed P0 (line, exit) tuple is a member of V; every
  member of V is attested (observed in this run's P0 tuples or recorded as a P0 tuple of that
  statement in a committed observation receipt under .ufo/evidence/round-48/calibration/observations/
  at REV); the tool sha256 prefix equals the pinned file at REV; and D contains every dependence
  observed in all 3 rounds and no dependence observed in none of them (a dependence observed in
  some rounds only is `unstable` and may be declared or omitted). Per round, dependence d is
  observed when the variant profile's tuple differs from that round's P1 tuple (env: P0 differs
  from P1); profiles and variants are the round-47 counter's. total = mismatches + unparsed +
  unobservable + dep_mismatch + unpinned + unattested + oversize = 0, the base SCORECARD.md stays
  a byte prefix, and the counter, its selftest and the statements pin are committed at REV.
  C1_R48_PASS=true iff self_pin=1 stmts_pin=1 statements=22 rounds=3 append_only=1 unpinned=0 total=0.

Operationally, per statement:
  * statements = .ufo/evidence/round-47/calibration/statements.json at REV, pinned by the round-47
    STATEMENTS_SHA256 (reused unchanged); a statement without `sha_file` is `unpinned`;
  * R=3 observation ROUNDS run one after another (never interleaved). Each round runs the round-47
    six profiles P0-P5 for every statement exactly as the round-47 counter does (P0 = the live host
    environment; P1 = clean env, PATH shim of /usr/bin plus node/jj/jq; P2/P3/P4 = P1 with bwrap/jj/
    node removed from the shim; P5 = P1 inside bwrap with the fleet root bound to a decoy holding
    only a stub scripts/sources-census.sh that exits 7), then deletes that round's clones and
    mirrors before the next round. Default worker count 6 (--jobs);
  * row picking: the LAST data row, in file order, of a SCORECARD.md table of the statement's kind
    (kind `cap`: header cell 1 `Capability`; kind `axis`: header cell 2 begins `Score`; tables in
    fenced code blocks or HTML comments are invisible) whose first cell is the statement id AND
    whose evidence cell contains `runs 3`. Rows without `runs 3` are skipped; no such row is
    `unparsed`;
  * row grammar (contract amendment 3). `cap` evidence cell:
        `CMD` -> `LINE1`, exit N1[ or `LINE2`, exit N2[ or `LINE3`, exit N3]], tool sha256 `12 hex`,
        deps `LIST`, runs 3 CLASS
    (the arrow is U+2192). `axis` row: score cell `N1[ or N2[ or N3]]`; evidence cell carries
    tool sha256 `12 hex`, deps `LIST`, runs 3 CLASS. V = the distinct declared members (cap: the
    (line, exit) pairs; axis: the integers, exit ignored as in round 47). CLASS is `stable` (exactly
    one member) or `nondeterministic` (two or three members); any other member-count/class pairing,
    or more than three members, is `oversize`. LIST is `none` or a sorted comma list over
    {bwrap, env, fleet-root, jj, node}; an unsorted list, a duplicate name, an unknown name, a
    missing deps clause or a missing/malformed `runs 3 CLASS` clause is `unparsed`;
  * `mismatch` when any P0 tuple of any round is not in V, or the declared tool sha256 prefix is not
    the pinned file at REV; `unobservable` when P0 yields no matching line in any round;
  * `unattested` when a member of V is neither among this run's P0 tuples nor recorded as that
    statement's P0 tuple in a `PROFILES <id>: P0=<line>|<exit> ...` line of a committed file under
    .ufo/evidence/round-48/calibration/observations/ at REV (read with `git show` at REV);
  * `dep_mismatch` when the declared deps lack a dependence observed in all 3 rounds (`required`)
    or declare one observed in none of them (`never`); a dependence observed in some rounds only
    (`unstable`) may be declared or omitted.
Each component counts statements, and within a statement the value verdicts are exclusive in the
order unobservable, unparsed, oversize, mismatch, unattested (the deps verdict is independent).
Modes: --lane L --rev R --base B --work EMPTY_DIR (deciding); --emit (same, also prints, per
statement, the standing row the observed rounds imply — V = the distinct observed P0 tuples, class
by count, deps = required — in the amendment-3 grammar, after every round's PROFILES lines);
--only ID[,ID] and --rounds N (N != 3) are seat probes: the verdict line is C1_R48_PARTIAL and the
receipt can never read C1_R48_PASS=true; --selftest (fixtures, no network, no real lane run).
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
SELF_PATH = '.ufo/evidence/round-48/calibration/measure.py'
STATEMENTS_PATH = '.ufo/evidence/round-47/calibration/statements.json'
STATEMENTS_SHA256 = '924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56'
OBSERVATIONS_DIR = '.ufo/evidence/round-48/calibration/observations'
N_STATEMENTS = 22
N_ROUNDS = 3
FLEET = '/home/vgpnk/Projects/shokunin'
ARROW = '\u2192'
DEP_NAMES = ('bwrap', 'env', 'fleet-root', 'jj', 'node')
PROFILES = ('P0', 'P1', 'P2', 'P3', 'P4', 'P5')
VARIANTS = (('bwrap', 'P2'), ('jj', 'P3'), ('node', 'P4'), ('fleet-root', 'P5'))
MEMBER_RE = re.compile(r'`([^`]+)`, exit (\d+)')
SHA_RE = re.compile(r'tool sha256 `([0-9a-f]{12})`')
DEPS_RE = re.compile(r'deps `([a-z,-]+)`')
RUNS_RE = re.compile(r',\s*runs 3 (?:stable|nondeterministic)')
TAIL_RE = re.compile(r',\s*tool sha256 `([0-9a-f]{12})`,\s*deps `([a-z,-]+)`,'
                     r'\s*runs 3 (stable|nondeterministic)')
STUB = '#!/bin/sh\necho "decoy fleet root: census stub" >&2\nexit 7\n'


# --------------------------------------------------------------------------- scratch and git

def under_tmp(path):
    rp = os.path.realpath(path)
    return rp == '/tmp' or rp.startswith('/tmp/')


def scratch_root():
    """A writable scratch root outside /tmp (lane rule, round 48 §7.4)."""
    for cand in (os.environ.get('TMPDIR'), '/fast/scratch'):
        if not cand:
            continue
        rp = os.path.realpath(cand)
        if under_tmp(rp) or not os.path.isdir(rp) or not os.access(rp, os.W_OK):
            continue
        return rp
    print('C1_R48: no usable scratch root outside /tmp; set TMPDIR', file=sys.stderr)
    raise SystemExit(2)


def host_env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e


def git(*args, binary=False):
    out = subprocess.run(['git'] + list(args), capture_output=True, env=host_env())
    if out.returncode != 0:
        return None
    return out.stdout if binary else out.stdout.decode('utf-8', 'replace')


# --------------------------------------------------------------------------- SCORECARD rows

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
    """The last data row of each table kind that carries a `runs 3` clause in its evidence cell."""
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
            evidence = cells[2] if len(cells) > 2 else ''
            if 'runs 3' not in evidence:
                continue
            rows[(kind, cells[0])] = cells
    return rows


def parse_deps(txt):
    """`none` or a sorted comma list over DEP_NAMES; None when the list is not that."""
    names = txt.split(',')
    if names == ['none']:
        return frozenset()
    if 'none' in names or any(n not in DEP_NAMES for n in names):
        return None
    if len(set(names)) != len(names) or sorted(names) != names:
        return None
    return frozenset(names)


def parse_row(stmt, cells):
    """Amendment-3 row grammar. status: absent | unparsed | oversize | ok."""
    if cells is None:
        return {'status': 'absent', 'declared': None, 'sha': None, 'members': [], 'cls': None}
    evidence = cells[2] if len(cells) > 2 else ''
    if 'runs 3' not in evidence:
        return {'status': 'absent', 'declared': None, 'sha': None, 'members': [], 'cls': None}
    tail = TAIL_RE.search(evidence)
    if tail is None:
        return {'status': 'unparsed', 'declared': None, 'sha': None, 'members': [], 'cls': None}
    sha, deps_txt, cls = tail.groups()
    declared = parse_deps(deps_txt)
    if declared is None:
        return {'status': 'unparsed', 'declared': None, 'sha': None, 'members': [], 'cls': None}
    if stmt['kind'] == 'axis':
        score = (cells[1] if len(cells) > 1 else '').strip()
        parts = [p.strip() for p in score.split(' or ')] if score else []
        if not parts or not all(re.fullmatch(r'\d+', p) for p in parts):
            return {'status': 'unparsed', 'declared': declared, 'sha': sha, 'members': [], 'cls': cls}
        members = [(p,) for p in parts]
    else:
        head = evidence[:tail.start()]
        m = re.search(re.escape(ARROW) + r'\s*(.+)$', head, re.S)
        if m is None:
            return {'status': 'unparsed', 'declared': declared, 'sha': sha, 'members': [], 'cls': cls}
        body = m.group(1).strip()
        found = MEMBER_RE.findall(body)
        if not found:
            return {'status': 'unparsed', 'declared': declared, 'sha': sha, 'members': [], 'cls': cls}
        if ' or '.join('`%s`, exit %s' % pair for pair in found) != body:
            return {'status': 'unparsed', 'declared': declared, 'sha': sha, 'members': [], 'cls': cls}
        members = [(line, code) for line, code in found]
    value = sorted(set(members))
    count = len(value)
    ok = (cls == 'stable' and count == 1) or (cls == 'nondeterministic' and 2 <= count <= 3)
    return {'status': 'ok' if ok else 'oversize', 'declared': declared, 'sha': sha,
            'members': value, 'cls': cls}


def fmt_member(member):
    return '|'.join(member) if member else '-'


def attest_token(kind, member):
    return '%s|%s' % (member[0], member[1]) if kind == 'cap' else member[0]


def load_attestations(lane, rev):
    """{statement id: set of recorded P0 tokens} from committed observation files at REV."""
    listing = git('-C', lane, 'ls-tree', '-r', '--name-only', rev, '--', OBSERVATIONS_DIR)
    att = {}
    for path in (listing or '').split('\n'):
        path = path.strip()
        if not path:
            continue
        data = git('-C', lane, 'show', '%s:%s' % (rev, path))
        if data is None:
            continue
        for line in data.split('\n'):
            m = re.match(r'^PROFILES (.+?): (.*)$', line)
            if not m:
                continue
            tok = re.search(r'(?:^| )P0=(.*?)(?= P[1-5]=|$)', m.group(2))
            if tok:
                att.setdefault(m.group(1), set()).add(tok.group(1))
    return att


# --------------------------------------------------------------------------- observation

def compare_part(result, kind):
    """The part of an observation a dependence is read from: the picked line, plus the exit for cap."""
    obs, _note = result
    if obs is None:
        return None
    return tuple(obs[:2] if kind == 'cap' else obs[:1])


def dep_key(result, kind):
    obs, note = result
    return compare_part(result, kind) if obs is not None else ('UNOBSERVABLE', note)


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
    for name in sorted(os.listdir('/usr/bin')):
        if name in drop or name in seen:
            continue
        seen.add(name)
        try:
            os.symlink(os.path.join('/usr/bin', name), os.path.join(path, name))
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
    clone, mirror, rev, work, env, decoy, _rnd = ctx
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
    obs = [line] if stmt['kind'] == 'axis' else [line, str(p.returncode)]
    if stmt.get('sha_file'):
        data = git('-C', clone, 'show', 'HEAD:%s' % stmt['sha_file'], binary=True)
        obs.append(hashlib.sha256(data).hexdigest()[:12] if data is not None else 'absent')
    return tuple(obs), 'exit=%d' % p.returncode


def pinned_prefix(lane, rev, path):
    if not path:
        return 'absent'
    data = git('-C', lane, 'show', '%s:%s' % (rev, path), binary=True)
    return hashlib.sha256(data).hexdigest()[:12] if data is not None else 'absent'


# --------------------------------------------------------------------------- emit

def emit_row(stmt, members, deps, old, sha):
    dep_text = ','.join(sorted(deps)) or 'none'
    cls = 'stable' if len(members) == 1 else 'nondeterministic'
    if stmt['kind'] == 'axis':
        what = old[2] if old and len(old) > 2 else 'see the evidence pointer in the round-48 SCORECARD block'
        what = RUNS_RE.sub('', DEPS_RE.sub('', SHA_RE.sub('', what))).rstrip(' ,')
        return 'EMIT_AXIS | %s | %s | %s, tool sha256 `%s`, deps `%s`, runs 3 %s |' % (
            stmt['id'], ' or '.join(m[0] for m in members), what, sha, dep_text, cls)
    evidence = '`%s` %s %s, tool sha256 `%s`, deps `%s`, runs 3 %s' % (
        stmt['cmd_text'], ARROW, ' or '.join('`%s`, exit %s' % m for m in members), sha, dep_text, cls)
    what = old[1] if old and len(old) > 1 else (stmt.get('what') or '')
    first = old[3] if old and len(old) > 3 else (stmt.get('first') or '')
    return 'EMIT_CAP | %s | %s | %s | %s |' % (stmt['id'], what, evidence, first)


# --------------------------------------------------------------------------- measure

def measure(lane, rev, base, work, emit=False, pin=STATEMENTS_SHA256, n_expected=N_STATEMENTS,
            jobs=6, rounds=N_ROUNDS, only=None, observe_fn=None):
    work = os.path.abspath(work)
    if under_tmp(work):
        print('C1_R48: --work must not be under /tmp (lane rule, round 48 §7.4)', file=sys.stderr)
        return 2
    if rounds < 1:
        print('C1_R48: --rounds must be at least 1', file=sys.stderr)
        return 2
    if os.path.exists(work) and os.listdir(work):
        print('C1_R48: --work must be empty or absent', file=sys.stderr)
        return 2
    os.makedirs(work, exist_ok=True)
    r = git('-C', lane, 'rev-parse', '--verify', rev + '^{commit}')
    if r is None:
        print('C1_R48: cannot resolve rev', file=sys.stderr)
        return 2
    rev = r.strip()
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = git('-C', lane, 'show', '%s:%s' % (rev, SELF_PATH), binary=True)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    raw = git('-C', lane, 'show', '%s:%s' % (rev, STATEMENTS_PATH), binary=True)
    stmts_pin = int(raw is not None and hashlib.sha256(raw).hexdigest() == pin)
    if raw is None:
        print('C1_R48: statements.json absent at rev', file=sys.stderr)
        return 2
    statements = json.loads(raw)['statements']
    if only:
        statements = [s for s in statements if s['id'] in only]
        if not statements:
            print('C1_R48: --only names no statement', file=sys.stderr)
            return 2
    base_sc = git('-C', lane, 'show', '%s:SCORECARD.md' % base)
    rev_sc = git('-C', lane, 'show', '%s:SCORECARD.md' % rev)
    if base_sc is None or rev_sc is None:
        print('C1_R48: cannot read SCORECARD.md', file=sys.stderr)
        return 2
    append_only = int(rev_sc.startswith(base_sc))
    rows = last_rows(rev_sc)
    att = load_attestations(lane, rev)
    fn = observe_fn or observe
    run_results = []
    for rnd in range(1, rounds + 1):
        work_r = os.path.join(work, 'round%d' % rnd)
        os.makedirs(work_r, exist_ok=True)
        decoy = os.path.join(work_r, 'decoy')
        os.makedirs(os.path.join(decoy, 'scripts'))
        stub = os.path.join(decoy, 'scripts', 'sources-census.sh')
        with open(stub, 'w') as fh:
            fh.write(STUB)
        os.chmod(stub, 0o755)
        ctxs = {}
        for prof in PROFILES:
            if observe_fn is None:
                made = setup_profile(lane, rev, work_r, prof)
                if made is None:
                    print('C1_R48: clone/checkout failed', file=sys.stderr)
                    return 2
                ctxs[prof] = (made[0], made[1], rev, work_r, profile_env(work_r, prof, rev), decoy, rnd)
            else:
                ctxs[prof] = (None, None, rev, work_r, None, decoy, rnd)
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            futs = {}
            for s in sorted(statements, key=lambda x: -x['timeout']):
                for prof in PROFILES:
                    futs[(s['id'], prof)] = pool.submit(fn, s, prof, ctxs[prof])
            for key, f in futs.items():
                results[key] = f.result()
        run_results.append(results)
        for prof in PROFILES:
            for sub in ('clone', 'fleet', 'shim', 'home', 'tmp'):
                path = os.path.join(work_r, prof, sub)
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
    mism = unparsed = unobs = depm = unatt = over = 0
    unpinned = sum(1 for s in statements if not s.get('sha_file'))
    emitted = []
    for s in statements:
        sid, kind = s['id'], s['kind']
        cuts, dep_sets = [], []
        for res in run_results:
            cuts.append(compare_part(res.get((sid, 'P0')), kind))
            ref = dep_key(res.get((sid, 'P1')), kind)
            seen = set()
            if dep_key(res.get((sid, 'P0')), kind) != ref:
                seen.add('env')
            for dep, prof in VARIANTS:
                if dep_key(res.get((sid, prof)), kind) != ref:
                    seen.add(dep)
            dep_sets.append(seen)
        observed = [c for c in cuts if c is not None]
        required = set.intersection(*dep_sets) if dep_sets else set()
        union = set.union(*dep_sets) if dep_sets else set()
        never = set(DEP_NAMES) - union
        unstable = union - required
        claim = parse_row(s, rows.get((kind, sid)))
        pinned = pinned_prefix(lane, rev, s.get('sha_file'))
        if not observed:
            verdict = 'UNOBSERVABLE'
            unobs += 1
        elif claim['status'] != 'ok':
            if claim['status'] == 'oversize':
                verdict = 'OVERSIZE'
                over += 1
            else:
                verdict = 'UNPARSED'
                unparsed += 1
        elif any(c not in claim['members'] for c in observed) or claim['sha'] != pinned:
            verdict = 'MISMATCH'
            mism += 1
        else:
            receipts = att.get(sid, set())
            missing = [m for m in claim['members'] if m not in observed and attest_token(kind, m) not in receipts]
            if missing:
                verdict = 'UNATTESTED'
                unatt += 1
            else:
                verdict = 'MATCH'
        dep_note = 'DEPS-OK'
        declared = claim.get('declared')
        if declared is not None and (not required <= declared or (never & declared)):
            dep_note = 'DEPS-MISMATCH'
            depm += 1
        claimed_txt = ' or '.join(fmt_member(m) for m in claim['members']) if claim['members'] else '-'
        rounds_txt = ' '.join('r%d=%s' % (i + 1, fmt_member(c)) for i, c in enumerate(cuts))
        print('STATEMENT %s/%s: claimed=%s sha=%s ROUNDS %s DEPS required=%s unstable=%s never=%s declared=%s %s %s' % (
            kind, sid, claimed_txt, claim['sha'] or '-', rounds_txt,
            ','.join(sorted(required)) or 'none', ','.join(sorted(unstable)) or 'none',
            ','.join(sorted(never)) or 'none', ','.join(sorted(declared)) if declared is not None else '-',
            verdict, dep_note))
        if emit and observed:
            emitted.append((s, sorted(set(observed)), required))
    for idx, res in enumerate(run_results):
        print('ROUND %d' % (idx + 1))
        for s in statements:
            print('PROFILES %s: %s' % (s['id'], ' '.join(
                '%s=%s' % (p, fmt_member(compare_part(res.get((s['id'], p)), s['kind']))) for p in PROFILES)))
    if emit:
        for s, members, deps in emitted:
            print(emit_row(s, members, deps, rows.get((s['kind'], s['id'])),
                           pinned_prefix(lane, rev, s.get('sha_file'))))
    total = mism + unparsed + unobs + depm + unpinned + unatt + over
    partial = bool(only) or rounds != N_ROUNDS
    passed = (self_pin == 1 and stmts_pin == 1 and len(statements) == n_expected and rounds == N_ROUNDS
              and append_only == 1 and total == 0 and not only)
    print('%s: self_pin=%d stmts_pin=%d statements=%d rounds=%d append_only=%d unpinned=%d total=%d '
          'mismatches=%d unparsed=%d unobservable=%d dep_mismatch=%d unattested=%d oversize=%d rev=%s '
          'C1_R48_PASS=%s' % (
              'C1_R48_PARTIAL' if partial else 'C1_R48', self_pin, stmts_pin, len(statements), rounds,
              append_only, unpinned, total, mism, unparsed, unobs, depm, unatt, over, rev,
              'true' if passed else 'false'))
    return 0 if passed else 1


# --------------------------------------------------------------------------- selftest

def selftest():
    env0 = host_env()
    env0.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    me = os.path.abspath(__file__)
    root = scratch_root()
    cap_hdr = '| Capability | What | Evidence | First |\n|---|---|---|---|\n'
    axis_hdr = '\n| Axis | Score (0\u201310) | Rule | Commit | Round |\n|---|---|---|---|---|\n'
    base_sc = '# S\n\nintro\n'
    tool_sha = hashlib.sha256(b'tool\n').hexdigest()[:12]

    def stmt(sid, argv, obs, kind='cap', cwd='clone', sha='tool.txt'):
        return dict(id=sid, kind=kind, argv=argv, obs=obs, cmd_text=' '.join(argv), sha_file=sha,
                    cwd=cwd, timeout=60)

    stmts = [
        stmt('alpha', ['echo', 'ALPHA: 3/3 pass'], r'^(ALPHA: \d+/\d+ pass)'),
        stmt('beta', ['sh', '-c', 'echo BETA: 5/5 pass; exit 3'], r'^(BETA: \d+/\d+ pass)'),
        stmt('score', ['echo', 'value=7'], r'value=(\d+)', kind='axis'),
    ]
    gamma = stmt('gamma', ['echo', 'GAMMA: 1/1'], r'^(GAMMA: \d+/\d+)')
    dep_stmts = {
        'bwrap': stmt('gamma', ['sh', '-c', 'if command -v bwrap >/dev/null; then echo G: has; else echo G: lacks; fi'], r'^(G: \w+)'),
        'jj': stmt('gamma', ['sh', '-c', 'if command -v jj >/dev/null; then echo G: has; else echo G: lacks; fi'], r'^(G: \w+)'),
        'node': stmt('gamma', ['sh', '-c', 'if command -v node >/dev/null; then echo G: has; else echo G: lacks; fi'], r'^(G: \w+)'),
        'fleet-root': stmt('gamma', ['sh', '-c', 'if test -e %s/MISSION.md; then echo G: has; else echo G: lacks; fi' % FLEET], r'^(G: \w+)'),
        'env': stmt('gamma', ['sh', '-c', 'echo G: $(basename "$HOME")'], r'^(G: \S+)'),
    }

    def row_cap(sid, members, deps='none', cls=None, sha=tool_sha, arrow=ARROW, runs=True,
                runs_where='ev'):
        cls = cls or ('stable' if len(members) == 1 else 'nondeterministic')
        body = ' or '.join('`%s`, exit %s' % m for m in members)
        tail = ', tool sha256 `%s`, deps `%s`' % (sha, deps)
        if runs:
            tail += ', runs 3 %s' % cls
        what = 'w'
        if runs and runs_where == 'what':
            what = 'w (runs 3 %s)' % cls
            tail = ', tool sha256 `%s`, deps `%s`' % (sha, deps)
        return '| %s | %s | `%s` %s %s%s | r1 |\n' % (sid, what, sid, arrow, body, tail)

    def row_axis(values, deps='none', cls=None, sha=tool_sha, runs=True):
        cls = cls or ('stable' if len(values) == 1 else 'nondeterministic')
        tail = 'rule, tool sha256 `%s`, deps `%s`' % (sha, deps)
        if runs:
            tail += ', runs 3 %s' % cls
        return '| score | %s | %s | c | r |\n' % (' or '.join(values), tail)

    def doc(*caps, score=None):
        return (base_sc + '\n' + cap_hdr + ''.join(caps) + '\n' + axis_hdr
                + (score if score is not None else row_axis(['7'])))

    A = lambda **k: row_cap('alpha', [('ALPHA: 3/3 pass', 0)], **k)
    B = lambda **k: row_cap('beta', [('BETA: 5/5 pass', 3)], **k)
    G = lambda **k: row_cap('gamma', [('GAMMA: 1/1', 0)], **k)
    P0A, P0B, P0S = ('ALPHA: 3/3 pass', '0'), ('BETA: 5/5 pass', '3'), ('7',)
    good = doc(A(), B())

    def make_fake(spec):
        """spec: {'P0': [tuple|None per round], ...}; an unlisted profile follows P1."""
        def fake(stmt_dict, prof, ctx):
            seq = spec.get(prof, spec.get('P1', [None] * 3))
            idx = min(ctx[6] - 1, len(seq) - 1)
            entry = seq[idx]
            return (entry, 'exit=0') if entry is not None else (None, 'exit=1')
        return fake

    cases = []

    def case(name, scorecard, opt, wants, post=None):
        cases.append((name, scorecard, opt, wants, post))

    base_obs = {'P0': [P0A, P0A, P0A], 'P1': [P0A, P0A, P0A],
                'P2': [P0A, P0A, P0A], 'P3': [P0A, P0A, P0A],
                'P4': [P0A, P0A, P0A], 'P5': [P0A, P0A, P0A]}

    def fake_case(name, scorecard, spec, wants, **opt):
        post = opt.pop('post', None)
        opt.setdefault('statements', [stmts[0]])
        opt.setdefault('n_expected', 1)
        opt['fake'] = make_fake(spec)
        case(name, scorecard, opt, wants, post=post)

    case('T01_all_match', good, {'jobs': 1},
         ('total=0', 'C1_R48_PASS=true', 'rounds=3'),
         post=lambda lane, work, out: (not any(
             os.path.isdir(os.path.join(work, 'round%d' % n, p, 'clone'))
             for n in (1, 2, 3) for p in PROFILES), 'clones deleted after every round'))
    case('T02_value_mismatch', doc(row_cap('alpha', [('ALPHA: 2/3 pass', 0)]), B()), {}, ('mismatches=1',))
    case('T03_exit_mismatch', doc(row_cap('alpha', [('ALPHA: 3/3 pass', 1)]), B()), {}, ('mismatches=1',))
    case('T04_sha_mismatch', doc(A(), B(sha='0' * 12)), {}, ('mismatches=1',))
    case('T05_axis_mismatch', doc(A(), B(), score=row_axis(['6'])), {}, ('mismatches=1',))
    case('T06_absent_row_unparsed', doc(A()), {}, ('unparsed=1',))
    case('T07_prose_claim_unparsed',
         base_sc + cap_hdr + '| alpha | w | it passes 3/3 | r1 |\n' + B() + axis_hdr + row_axis(['7']),
         {}, ('unparsed=1',))
    case('T08_rows_without_runs_are_skipped',
         doc(row_cap('alpha', [('ALPHA: 1/3 pass', 0)], runs=False), A(), B()), {}, ('total=0', 'C1_R48_PASS=true'))
    case('T09_only_row_without_runs_is_unparsed',
         doc(row_cap('alpha', [('ALPHA: 1/3 pass', 0)], runs=False), B()), {}, ('unparsed=1',))
    case('T10_last_runs_row_wins',
         doc(A(), B(), row_cap('alpha', [('ALPHA: 1/3 pass', 0)])), {}, ('mismatches=1',))
    case('T11_later_row_without_runs_does_not_shadow',
         doc(A(), B(), row_cap('alpha', [('ALPHA: 1/3 pass', 0)], runs=False)), {}, ('total=0', 'C1_R48_PASS=true'))
    case('T12_fenced_table_ignored',
         base_sc + '```\n' + cap_hdr + row_cap('alpha', [('ALPHA: 9/9 pass', 0)]) + '```\n'
         + cap_hdr + A() + B() + axis_hdr + row_axis(['7']), {}, ('total=0',))
    case('M03_comment_dotall_hidden_last_row',
         base_sc + '\n' + cap_hdr + A() + B() + axis_hdr + row_axis(['7'])
         + '\n<!--\n' + cap_hdr + row_cap('alpha', [('ALPHA: 9/9 pass', 0)]) + '-->\n',
         {}, ('total=0', 'C1_R48_PASS=true'))
    case('M04_arrow_required',
         doc('| alpha | w | `ALPHA: 3/3 pass`, exit 0, tool sha256 `%s`, deps `none`, runs 3 stable | r1 |\n'
             % tool_sha, B()), {}, ('unparsed=1',))
    case('M04b_arrow_glyph_wrong',
         doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0)], arrow='->'), B()), {}, ('unparsed=1',))
    case('M05_exit_negative_refused',
         doc(A().replace('exit 0', 'exit -1'), B()), {}, ('unparsed=1',))
    case('T13_unobservable_command', good, {'argv0': ['sh', '-c', 'echo nothing useful']}, ('unobservable=1',))
    case('T14_append_only_broken', good, {'base_override': '# other base\n'},
         ('append_only=0', 'C1_R48_PASS=false'))
    case('T15_statements_tampered', good, {'tamper': True}, ('stmts_pin=0', 'C1_R48_PASS=false'))
    case('T16_self_pin_broken', good, {'selfbytes': b'# not the counter\n'},
         ('self_pin=0', 'C1_R48_PASS=false'))
    case('M22_statement_overcount', doc(A(), B(), G()), {'statements': stmts + [gamma], 'n_expected': 3},
         ('statements=4', 'C1_R48_PASS=false'))
    case('T17_axis_noninteger_unparsed', doc(A(), B(), score=row_axis(['seven'])), {}, ('unparsed=1',))
    case('T18_missing_deps_clause_unparsed', doc(A().replace(', deps `none`', ''), B()), {}, ('unparsed=1',))
    case('T19_axis_row_without_sha_unparsed',
         doc(A(), B(), score='| score | 7 | rule, deps `none`, runs 3 stable | c | r |\n'), {}, ('unparsed=1',))
    case('T20_deps_unsorted_unparsed', doc(A(deps='node,bwrap'), B()), {}, ('unparsed=1',))
    case('T20b_deps_unknown_name_unparsed', doc(A(deps='Bwrap'), B()), {}, ('unparsed=1',))
    case('T20c_deps_duplicate_name_unparsed', doc(A(deps='node,node'), B()), {}, ('unparsed=1',))
    case('T21_statement_without_sha_file_unpinned', good, {'nosha': True}, ('unpinned=1',))
    case('M24_total_one_still_false', doc(row_cap('alpha', [('ALPHA: 2/3 pass', 0)]), B()),
         {}, ('total=1', 'C1_R48_PASS=false'))
    case('M25_only_naming_all_statements_never_passes', good,
         {'only': ['alpha', 'beta', 'score']},
         ('C1_R48_PARTIAL:', 'C1_R48_PASS=false', 'rounds=3'))
    case('T26_rounds_probe_never_passes', good, {'rounds': 1},
         ('C1_R48_PARTIAL:', 'rounds=1', 'C1_R48_PASS=false'))
    for dep in ('bwrap', 'jj', 'node', 'fleet-root', 'env'):
        case('T27_undeclared_%s_dependence' % dep, 'dep:' + dep + ':none', {'dep': dep}, ('dep_mismatch=1',))
        case('T28_declared_%s_dependence_matches' % dep, 'dep:' + dep + ':' + dep, {'dep': dep},
             ('dep_mismatch=0', 'total=0'))
    fake_case('M12_comparable_cut_sha_only_difference', doc(A()),
              {'P0': [P0A + ('aaaaaaaaaaaa',)], 'P1': [P0A + ('bbbbbbbbbbbb',)],
               'P2': [P0A + ('bbbbbbbbbbbb',)], 'P5': [P0A + ('bbbbbbbbbbbb',)]},
              ('total=0', 'C1_R48_PASS=true'))
    obs_a = 'PROFILES alpha: P0=ALPHA: 2/3 pass|0 P1=ALPHA: 3/3 pass|0\n'
    two = [('ALPHA: 3/3 pass', '0'), ('ALPHA: 2/3 pass', '0')]
    fake_case('T30_member_attested_from_observation_file',
              doc(row_cap('alpha', two)), dict(base_obs, P0=[P0A, P0A, P0A]),
              ('unattested=0', 'total=0'),
              obs={'at': 'rev', 'files': {OBSERVATIONS_DIR + '/obs-r1.json': obs_a}})
    fake_case('T31_member_without_receipt_unattested',
              doc(row_cap('alpha', two)), dict(base_obs, P0=[P0A, P0A, P0A]), ('unattested=1',))
    fake_case('T32_receipt_for_other_statement_ignored',
              doc(row_cap('alpha', two)), dict(base_obs, P0=[P0A, P0A, P0A]), ('unattested=1',),
              obs={'at': 'rev', 'files': {OBSERVATIONS_DIR + '/obs-r1.json':
                                          'PROFILES beta: P0=ALPHA: 2/3 pass|0\n'}})
    fake_case('T33_receipt_absent_at_rev_unattested',
              doc(row_cap('alpha', two)), dict(base_obs, P0=[P0A, P0A, P0A]), ('unattested=1',),
              obs={'at': 'base', 'files': {OBSERVATIONS_DIR + '/obs-r1.json': obs_a}})
    fake_case('T40_required_all_rounds_undeclared', doc(A()),
              {'P0': [P0A] * 3, 'P1': [P0A] * 3, 'P4': [('ALPHA: 3/3 pass', '9')] * 3}, ('dep_mismatch=1',))
    fake_case('T41_required_all_rounds_declared', doc(A(deps='node')),
              {'P0': [P0A] * 3, 'P1': [P0A] * 3, 'P4': [('ALPHA: 3/3 pass', '9')] * 3},
              ('dep_mismatch=0', 'total=0'))
    fake_case('T42_unstable_may_be_omitted', doc(A()),
              {'P0': [P0A] * 3, 'P1': [P0A] * 3,
               'P4': [('ALPHA: 3/3 pass', '9'), P0A, P0A]}, ('dep_mismatch=0', 'total=0'))
    fake_case('T43_unstable_may_be_declared', doc(A(deps='node')),
              {'P0': [P0A] * 3, 'P1': [P0A] * 3,
               'P4': [('ALPHA: 3/3 pass', '9'), P0A, P0A]}, ('dep_mismatch=0', 'total=0'))
    fake_case('T44_never_observed_declared_is_mismatch', doc(A(deps='node')),
              {'P0': [P0A] * 3, 'P1': [P0A] * 3}, ('dep_mismatch=1',))
    fake_case('T45_required_and_unstable_mixed',
              doc(row_cap('alpha', [('ALPHA: 9/9 pass', 0)], deps='env')),
              {'P1': [P0A] * 3, 'P0': [('ALPHA: 9/9 pass', '0')] * 3,
               'P2': [P0A, ('ALPHA: 9/9 pass', '0'), P0A]}, ('dep_mismatch=0', 'total=0'))
    fake_case('T46_never_dep_in_mixed_set_rejected',
              doc(row_cap('alpha', [('ALPHA: 9/9 pass', 0)], deps='env,node')),
              {'P1': [P0A] * 3, 'P0': [('ALPHA: 9/9 pass', '0')] * 3,
               'P2': [P0A, ('ALPHA: 9/9 pass', '0'), P0A]}, ('dep_mismatch=1',))
    fake_case('T50_two_members_observed_across_rounds',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0), ('ALPHA: 9/9 pass', 0)])),
              dict(base_obs, P0=[P0A, ('ALPHA: 9/9 pass', '0'), P0A]),
              ('total=0', 'C1_R48_PASS=true'))
    fake_case('T51_three_members_one_observed_two_attested',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0), ('ALPHA: 8/8 pass', 0), ('ALPHA: 9/9 pass', 0)])),
              dict(base_obs, P0=[P0A, P0A, P0A]), ('unattested=0', 'total=0'),
              obs={'at': 'rev', 'files': {OBSERVATIONS_DIR + '/obs-r1.json':
                                          'PROFILES alpha: P0=ALPHA: 8/8 pass|0\n'
                                          'PROFILES alpha: P0=ALPHA: 9/9 pass|0\n'}})
    fake_case('T52_four_members_oversize',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0), ('ALPHA: 6/6 pass', 0),
                                    ('ALPHA: 8/8 pass', 0), ('ALPHA: 9/9 pass', 0)])),
              dict(base_obs, P0=[P0A, P0A, P0A]), ('oversize=1',))
    fake_case('T53_two_members_stable_oversize',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0), ('ALPHA: 9/9 pass', 0)], cls='stable')),
              dict(base_obs, P0=[P0A, P0A, P0A]), ('oversize=1',))
    fake_case('T54_one_member_nondeterministic_oversize',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0)], cls='nondeterministic')),
              dict(base_obs, P0=[P0A, P0A, P0A]), ('oversize=1',))
    fake_case('T55_unknown_class_unparsed',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0)]).replace('runs 3 stable', 'runs 3 sometimes')),
              dict(base_obs, P0=[P0A, P0A, P0A]), ('unparsed=1',))
    axis_doc = lambda row: base_sc + '\n' + axis_hdr + row
    fake_case('T56_axis_two_members_nondeterministic', axis_doc(row_axis(['7', '8'])),
              {'P0': [P0S, ('8',), P0S], 'P1': [P0S] * 3}, ('total=0', 'C1_R48_PASS=true'),
              statements=[stmts[2]])
    fake_case('T57_axis_four_members_oversize', axis_doc(row_axis(['5', '6', '7', '8'])),
              {'P0': [P0S] * 3, 'P1': [P0S] * 3}, ('oversize=1',), statements=[stmts[2]])
    fake_case('T58_runs3_outside_evidence_cell_skipped',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0)], runs_where='what')),
              dict(base_obs, P0=[P0A, P0A, P0A]), ('unparsed=1',))
    fake_case('T59_member_order_irrelevant',
              doc(row_cap('alpha', [('ALPHA: 9/9 pass', 0), ('ALPHA: 3/3 pass', 0)])),
              dict(base_obs, P0=[P0A, ('ALPHA: 9/9 pass', '0'), P0A]),
              ('total=0', 'C1_R48_PASS=true'))
    fake_case('T60_any_round_outside_v_is_mismatch', doc(A()),
              dict(base_obs, P0=[P0A, P0A, ('ALPHA: 9/9 pass', '0')]), ('mismatches=1',))
    fake_case('T61_emit_rows_reparse',
              doc(row_cap('alpha', [('ALPHA: 3/3 pass', 0), ('ALPHA: 9/9 pass', 0)])),
              dict(base_obs, P0=[P0A, ('ALPHA: 9/9 pass', '0'), P0A]),
              ('EMIT_CAP | alpha |',), emit=True, post=post_emit_reparse)
    fake_case('T62_emit_declares_required_deps_only', doc(A(deps='node')),
              {'P0': [P0A] * 3, 'P1': [P0A] * 3,
               'P4': [('ALPHA: 3/3 pass', '9'), P0A, P0A]},
              ('deps `none`, runs 3 stable |',), emit=True)
    case('M26b_decoy_stub_exit_code',
         doc(row_cap('alpha', [('STUB_EXIT: 7', 0)]), B()),
         {'statements': [stmt('alpha', ['sh', '-c',
                                        'sh {work}/../decoy/scripts/sources-census.sh; echo STUB_EXIT: $?'],
                              r'^(STUB_EXIT: \d+)')], 'n_expected': 1, 'jobs': 1},
         ('total=0',))
    case('T63_work_under_tmp_refused', good, {'work': '/tmp/c1-r48-should-not-exist'}, (), post=post_tmp)
    case('T64_work_nonempty_refused', good, {'precreate_work': True}, (), post=post_nonempty)
    case('T65_rounds_zero_rejected', good, {'rounds': 0}, (), post=post_zero)

    failed = 0
    for name, scorecard, opt, wants, post in cases:
        d = tempfile.mkdtemp(prefix='c1-r48-', dir=root)
        try:
            ok, detail = run_case(d, name, scorecard, opt, wants, post, me, cap_hdr, axis_hdr,
                                  base_sc, tool_sha, stmts, dep_stmts, env0, good)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        failed += not ok
        print('%s %s %s' % ('PASS' if ok else 'FAIL', name, detail))
    print('C1_R48_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


def post_emit_reparse(lane, work, out):
    for line in out.split('\n'):
        if line.startswith('EMIT_CAP | alpha | '):
            evidence = line.split(' | ')[3]
            rows = last_rows('| Capability | What | Evidence | First |\n|---|---|---|---|\n| alpha | w | %s | r1 |\n' % evidence)
            claim = parse_row({'kind': 'cap'}, rows.get(('cap', 'alpha')))
            ok = (claim['status'] == 'ok' and claim['cls'] == 'nondeterministic'
                  and claim['members'] == [('ALPHA: 3/3 pass', '0'), ('ALPHA: 9/9 pass', '0')]
                  and claim['declared'] == frozenset())
            return ok, 'emitted row reparses status=%s members=%s cls=%s' % (
                claim['status'], claim['members'], claim['cls'])
    return False, 'no EMIT_CAP row for alpha'


def post_tmp(lane, work, out):
    ok = (not os.path.exists('/tmp/c1-r48-should-not-exist')
          and 'must not be under /tmp' in out)
    return ok, 'work under /tmp refused without writing'


def post_nonempty(lane, work, out):
    return ('--work must be empty or absent' in out), 'non-empty work refused'


def post_zero(lane, work, out):
    return ('--rounds must be at least 1' in out), 'rounds=0 refused'


def run_case(d, name, scorecard, opt, wants, post, me, cap_hdr, axis_hdr, base_sc, tool_sha,
             stmts, dep_stmts, env0, good):
    lane = os.path.join(d, 'lane')
    os.makedirs(lane)

    def g(*a):
        subprocess.run(['git', '-C', lane, *a], env=env0, capture_output=True, check=True)

    g('init', '-q', '-b', 'm')
    if subprocess.run(['git', '-C', lane, 'rev-parse', '--show-toplevel'], capture_output=True,
                      env=env0).stdout.decode().strip() != os.path.realpath(lane):
        return False, 'fixture toplevel mismatch'
    st = [dict(x) for x in opt.get('statements', stmts)]
    if scorecard.startswith('dep:'):
        _, dep, declared = scorecard.split(':')
        st = [dict(dep_stmts[dep])]
        probe = subprocess.run(dep_stmts[dep]['argv'], capture_output=True, text=True, env=env0)
        observed_line = re.search(dep_stmts[dep]['obs'], probe.stdout, re.M).group(1)
        scorecard = base_sc + '\n' + '| Capability | What | Evidence | First |\n|---|---|---|---|\n' + \
            '| gamma | w | `gamma` %s `%s`, exit 0, tool sha256 `%s`, deps `%s`, runs 3 stable | r1 |\n' % (
                ARROW, observed_line, tool_sha, declared)
    if opt.get('argv0'):
        st[0]['argv'] = opt['argv0']
    if opt.get('nosha'):
        st[0]['sha_file'] = None
    payload = json.dumps(dict(statements=st), indent=1).encode()
    os.makedirs(os.path.join(lane, os.path.dirname(SELF_PATH)))
    os.makedirs(os.path.join(lane, os.path.dirname(STATEMENTS_PATH)), exist_ok=True)
    with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
        fh.write(base_sc)
    with open(os.path.join(lane, 'tool.txt'), 'wb') as fh:
        fh.write(b'tool\n')
    with open(os.path.join(lane, STATEMENTS_PATH), 'wb') as fh:
        fh.write(payload)
    with open(os.path.join(lane, SELF_PATH), 'wb') as fh:
        fh.write(opt.get('selfbytes') or open(me, 'rb').read())
    obs = opt.get('obs')
    if obs and obs['at'] == 'base':
        for path, text in obs['files'].items():
            full = os.path.join(lane, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w') as fh:
                fh.write(text)
    g('add', '-A')
    g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'base')
    base_arg = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True,
                              text=True).stdout.strip()
    if obs and obs['at'] == 'base':
        for path in obs['files']:
            full = os.path.join(lane, path)
            if os.path.exists(full):
                os.unlink(full)
    if obs and obs['at'] == 'rev':
        for path, text in obs['files'].items():
            full = os.path.join(lane, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, 'w') as fh:
                fh.write(text)
    if 'base_override' in opt:
        with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
            fh.write(opt['base_override'])
        g('add', '-A')
        g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'other base')
        base_arg = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'], capture_output=True,
                                  text=True).stdout.strip()
    with open(os.path.join(lane, 'SCORECARD.md'), 'w') as fh:
        fh.write(scorecard)
    if opt.get('tamper'):
        with open(os.path.join(lane, STATEMENTS_PATH), 'ab') as fh:
            fh.write(b' ')
    g('add', '-A')
    g('-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'rev')
    work = opt.get('work') or os.path.join(d, 'work')
    if opt.get('precreate_work'):
        os.makedirs(work)
        with open(os.path.join(work, 'x'), 'w') as fh:
            fh.write('x')
    buf, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        rc = measure(lane, 'HEAD', base_arg, work, emit=bool(opt.get('emit')),
                     pin=hashlib.sha256(payload).hexdigest(), n_expected=opt.get('n_expected', len(st)),
                     jobs=opt.get('jobs', 3), rounds=opt.get('rounds', N_ROUNDS),
                     only=set(opt['only']) if opt.get('only') else None, observe_fn=opt.get('fake'))
    out = buf.getvalue()
    if post is not None:
        ok, detail = post(lane, work, out + err.getvalue())
        return ok, detail + ' rc=%d' % rc
    if not wants:
        return False, 'no wants and no post'
    lines = [l for l in out.split('\n') if l.startswith('C1_R48:') or l.startswith('C1_R48_PARTIAL:')]
    line = lines[-1] if lines else 'NO-C1-LINE'
    missing = [w for w in wants if w not in out]
    return (not missing), ('got=' + line) if not missing else ('missing=%r got=%s' % (missing, line))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--base')
    ap.add_argument('--work')
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--rounds', type=int, default=N_ROUNDS)
    ap.add_argument('--emit', action='store_true')
    ap.add_argument('--only', help='seat probe: comma-separated statement ids; the verdict line is C1_R48_PARTIAL with PASS=false')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.base and a.work):
        ap.error('--lane, --rev, --base and --work are required')
    return measure(a.lane, a.rev, a.base, a.work, emit=a.emit, jobs=a.jobs, rounds=a.rounds,
                   only=set(a.only.split(',')) if a.only else None)


if __name__ == '__main__':
    sys.exit(main())
