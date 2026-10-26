#!/usr/bin/env python3
r"""Round-49 C2 counter (coverage, frontier F10): one property-based generator against a named
fixture gate, measured against a hidden mutant panel.

Usage:
  python3 measure.py --lane LANE --rev REV --work EMPTY_DIR --panel PANEL.json [--generator-path P]
  python3 measure.py --witness CASES.jsonl --panel PANEL.json --lane LANE --rev REV --work EMPTY_DIR
  python3 measure.py --selftest

Named gate: tools/staged-id-guard.py at sha256 GUARD_SHA (the round-43 capability; never edited).
Generator: GENERATOR (default tools/pbt-staged-id.py) read from REV; frozen interface:
  python3 -I GEN --guard GUARD --seed INT --cases N --dump FILE
    runs up to N generated cases against `python3 -I GUARD --registry R --staged G [--map M] --json`,
    checks them with its own oracle, stops at the first violation, writes one JSONL line per case
    run ({"index", "registry", "staged", "map"}), and prints as its last stdout line
    `PBT_STAGED_ID: cases=<run> violations=<0|1> counterexample=<index|none> ...`;
    exit 0 no violation, 1 violation, 2 setup.

Predicate (label C2_R49_PASS), all from REV bytes:
  generator present; pristine run (seed SEED, N cases) exits 0 with `cases=N violations=0` and a dump
  of exactly N cases; the counter's own oracle agrees with the pristine guard on every analysis-mode
  dump case (oracle_disagree=0); each of the CLASSES occurs in >= CLASS_MIN dump cases; the panel
  (sha256 PANEL_SHA, every `old` string occurring exactly once in the guard) is valid; at least
  KILL_TARGET panel mutants are *confirmed*: the generator run against the mutant exits 1 naming a
  counterexample whose dumped case makes the pristine and the mutant guard print different
  (exit, stdout); and the records hold: ENTRY's leading block cites >= 1 `source: S###` whose
  SOURCES.md row at REV is `mined` and opened 2026-10-26, and corpus/README.md has a line carrying
  both `F10` and `held (round 49)`.
  total = absent + pristine_bad + oracle_disagree + classes_short + panel_invalid
          + max(0, KILL_TARGET - confirmed) + records_bad;  C2_R49_PASS = (total == 0).
--witness mode confirms each mutant against a case file instead (non-equivalence receipt; no PASS label).
Exit: 0 PASS (or witness all confirmed), 1 not, 2 setup, 64 usage.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
GUARD = 'tools/staged-id-guard.py'
GUARD_SHA = '03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8'
GENERATOR = 'tools/pbt-staged-id.py'
PANEL_SHA = 'd6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1'
ENTRY = 'corpus/knowledge/pbt-generator-pilot.md'
SEED, CASES = 4949, 400
CLASS_MIN = 10
KILL_TARGET = 11
GEN_TIMEOUT = 1800
GUARD_TIMEOUT = 60
CLASSES = ('indent_1_3', 'indent_4_plus', 'id_4_plus_digits', 'collision', 'no_collision', 'held',
           'unmapped', 'cascade', 'refusal', 'url_form_variant', 'map', 'map_inadmissible')
ROW_ANY = re.compile(r'^( *)\|\s*(S\d{3,})\s*\|')
ROW_CENSUS = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s|,;]+')
LAST_RE = re.compile(r'^PBT_STAGED_ID: cases=(\d+) violations=(\d+) counterexample=(\d+|none)\b')
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
GIT_ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')


class Setup(Exception):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=GIT_ENV)


def blob(repo, rev, path):
    r = git(repo, 'cat-file', 'blob', '%s:%s' % (rev, path))
    return r.stdout if r.returncode == 0 else None


def env_for(work):
    e = dict(GIT_ENV)
    tmp = os.path.join(work, 'tmp')
    os.makedirs(tmp, exist_ok=True)
    e['TMPDIR'] = tmp
    return e


# --- the counter's own oracle (analysis mode only) -------------------------------------------
def oracle(registry, staged):
    """Expected (exit, collisions, registry_rows, staged_rows) for analysis mode: exit 2 = refusal,
    exit 0 = answered (the guard may print 0 or 1 here; 1 marks an analysis it refuses to adopt)."""
    parsed = []
    for text in (registry, staged):
        ids = []
        for line in text.splitlines():
            m = ROW_CENSUS.match(line)
            if not m:
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) < 5 or m.group(1) in ids:
                return (2, None, None, None)
            ids.append(m.group(1))
        parsed.append(ids)
    reg, stg = parsed
    coll = sorted(set(reg) & set(stg), key=lambda s: int(s[1:]))
    return (0, coll, len(reg), len(stg))


def norm_doc(raw):
    t = raw.strip().lower()
    t = re.sub(r'^https?://', '', t)
    t = re.sub(r'^www\.', '', t)
    return t.rstrip('/')


def case_classes(case, out):
    """Frozen class predicates over a dumped case and the pristine guard's (exit, json)."""
    exitc, js = out
    reg, stg = case['registry'], case['staged']
    lines = reg.splitlines() + stg.splitlines()
    cl = set()
    for line in lines:
        m = ROW_ANY.match(line)
        if m:
            n = len(m.group(1))
            if 1 <= n <= 3:
                cl.add('indent_1_3')
            elif n >= 4:
                cl.add('indent_4_plus')
            if n <= 3 and len(m.group(2)) >= 5:
                cl.add('id_4_plus_digits')
    if case.get('map') is None:
        if exitc in (0, 1) and isinstance(js, dict):
            cl.add('collision' if js.get('collision_count', 0) > 0 else 'no_collision')
            if js.get('held'):
                cl.add('held')
            if js.get('unmapped'):
                cl.add('unmapped')
            if js.get('cascade'):
                cl.add('cascade')
        if exitc == 2:
            cl.add('refusal')
    else:
        cl.add('map')
        if exitc == 1:
            cl.add('map_inadmissible')
        if exitc == 2:
            cl.add('refusal')
    reg_urls = {}
    for u in URL_RE.findall(reg):
        reg_urls.setdefault(norm_doc(u.rstrip('.,;)]')), set()).add(u.rstrip('.,;)]'))
    for u in URL_RE.findall(stg):
        u = u.rstrip('.,;)]')
        k = norm_doc(u)
        if k in reg_urls and any(r != u for r in reg_urls[k]):
            cl.add('url_form_variant')
    return cl


def run_guard(guard, case, work, tag):
    d = os.path.join(work, 'cases', tag)
    os.makedirs(d, exist_ok=True)
    rp, sp = os.path.join(d, 'registry.md'), os.path.join(d, 'staged.md')
    with open(rp, 'w', encoding='utf-8', newline='') as fh:
        fh.write(case['registry'])
    with open(sp, 'w', encoding='utf-8', newline='') as fh:
        fh.write(case['staged'])
    argv = [sys.executable, '-I', guard, '--registry', rp, '--staged', sp]
    if case.get('map') is not None:
        mp = os.path.join(d, 'map.json')
        with open(mp, 'w', encoding='utf-8') as fh:
            json.dump(case['map'], fh)
        argv += ['--map', mp]
    argv.append('--json')
    try:
        r = subprocess.run(argv, capture_output=True, env=env_for(work), timeout=GUARD_TIMEOUT, cwd=d)
    except subprocess.TimeoutExpired:
        return (124, None, b'')
    try:
        js = json.loads(r.stdout)
    except ValueError:
        js = None
    shutil.rmtree(d, ignore_errors=True)
    return (r.returncode, js, r.stdout)


def comparable(out):
    exitc, js, raw = out
    if isinstance(js, dict):
        js = {k: v for k, v in js.items() if k not in ('registry_sha256', 'staged_sha256')}
        return (exitc, json.dumps(js, sort_keys=True))
    return (exitc, raw)


def load_dump(path):
    cases = []
    try:
        with open(path, encoding='utf-8') as fh:
            for line in fh:
                if line.strip():
                    c = json.loads(line)
                    if not (isinstance(c, dict) and isinstance(c.get('registry'), str)
                            and isinstance(c.get('staged'), str) and isinstance(c.get('index'), int)
                            and (c.get('map') is None or isinstance(c.get('map'), (dict, list, str, int)))):
                        return None
                    cases.append(c)
    except (OSError, ValueError):
        return None
    return cases


def run_generator(gen, guard, work, tag):
    dump = os.path.join(work, 'dump-%s.jsonl' % tag)
    argv = [sys.executable, '-I', gen, '--guard', guard, '--seed', str(SEED), '--cases', str(CASES),
            '--dump', dump]
    try:
        r = subprocess.run(argv, capture_output=True, env=env_for(work), timeout=GEN_TIMEOUT,
                           cwd=os.path.dirname(gen))
    except subprocess.TimeoutExpired:
        return {'exit': 124, 'last': None, 'dump': None}
    lines = [ln for ln in r.stdout.decode('utf-8', 'replace').splitlines() if ln.strip()]
    m = LAST_RE.match(lines[-1]) if lines else None
    with open(os.path.join(work, 'gen-%s.stdout' % tag), 'wb') as fh:
        fh.write(r.stdout)
    return {'exit': r.returncode, 'last': m, 'dump': load_dump(dump)}


def load_panel(path, guard_bytes):
    with open(path, 'rb') as fh:
        raw = fh.read()
    if sha(raw) != PANEL_SHA:
        raise Setup('panel sha256 mismatch')
    panel = json.loads(raw)
    text = guard_bytes.decode('utf-8')
    valid = all(text.count(m['old']) == 1 for m in panel['mutants'])
    return panel['mutants'], valid, text


def write_mutant(work, text, m):
    d = os.path.join(work, 'mut', m['id'])
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'staged-id-guard.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text.replace(m['old'], m['new'], 1))
    return p


def materialize(lane, rev, work, gen_path):
    tree = os.path.join(work, 'tree')
    os.makedirs(os.path.join(tree, 'tools'), exist_ok=True)
    g = blob(lane, rev, GUARD)
    if g is None or sha(g) != GUARD_SHA:
        raise Setup('guard missing or sha mismatch at REV')
    gp = os.path.join(tree, GUARD)
    with open(gp, 'wb') as fh:
        fh.write(g)
    gen = blob(lane, rev, gen_path)
    genp = None
    if gen is not None:
        genp = os.path.join(tree, gen_path)
        os.makedirs(os.path.dirname(genp), exist_ok=True)
        with open(genp, 'wb') as fh:
            fh.write(gen)
    return g, gp, genp


def records(lane, rev):
    bad = 0
    notes = []
    entry = blob(lane, rev, ENTRY)
    reg = blob(lane, rev, 'corpus/SOURCES.md')
    readme = blob(lane, rev, 'corpus/README.md')
    if entry is None or reg is None or readme is None:
        return 1, ['records-missing']
    head = entry.decode('utf-8', 'replace').split('\n\n', 1)[0]
    ids = re.findall(r'^source:\s*(S\d{3,})\b', head, re.M)
    if not ids:
        bad += 1
        notes.append('entry-no-source')
    rows = reg.decode('utf-8', 'replace').splitlines()
    for sid in ids:
        hit = [ln for ln in rows if re.match(r'^ {0,3}\|\s*' + sid + r'\s*\|', ln)]
        cells = [c.strip() for c in hit[0].strip().strip('|').split('|')] if len(hit) == 1 else []
        if len(cells) != 11 or cells[7] != 'mined' or cells[8] != '2026-10-26':
            bad += 1
            notes.append('row-not-opened-this-round:%s' % sid)
    if not any('F10' in ln and 'held (round 49)' in ln for ln in readme.decode('utf-8', 'replace').splitlines()):
        bad += 1
        notes.append('readme-no-F10-held')
    return bad, notes


def measure(lane, rev, work, panel_path, gen_path):
    gbytes, gp, genp = materialize(lane, rev, work, gen_path)
    mutants, panel_valid, gtext = load_panel(panel_path, gbytes)
    res = {'absent': 0, 'pristine_bad': 0, 'oracle_disagree': 0, 'classes_short': 0,
           'panel_invalid': 0 if panel_valid else 1, 'confirmed': 0, 'selftest_kills': 0, 'records_bad': 0}
    counts = {c: 0 for c in CLASSES}
    cases_run = viol = dumpn = None
    pexit = None
    if genp is None:
        res['absent'] = 1
    else:
        pr = run_generator(genp, gp, work, 'pristine')
        pexit = pr['exit']
        if pr['last']:
            cases_run, viol = int(pr['last'].group(1)), int(pr['last'].group(2))
        dump = pr['dump'] or []
        dumpn = len(dump) if pr['dump'] is not None else None
        if not (pexit == 0 and cases_run == CASES and viol == 0 and dumpn == CASES
                and [c['index'] for c in dump] == list(range(CASES))):
            res['pristine_bad'] = 1
        for i, c in enumerate(dump):
            out = run_guard(gp, c, work, 'p%d' % i)
            if c.get('map') is None:
                exp = oracle(c['registry'], c['staged'])
                # exit 0 and 1 are both answers (1 = analysis refused: unmapped or cascade); 2 = refusal
                ok = (out[0] == 2) == (exp[0] == 2) and out[0] in (0, 1, 2)
                if ok and exp[0] == 0:
                    js = out[1] or {}
                    ok = (js.get('collisions') == exp[1] and js.get('registry_rows') == exp[2]
                          and js.get('staged_rows') == exp[3])
                if not ok:
                    res['oracle_disagree'] += 1
                    print('ORACLE_DISAGREE index=%d guard_exit=%s expected_exit=%s' % (c['index'], out[0], exp[0]))
            for k in case_classes(c, (out[0], out[1])):
                counts[k] += 1
        if panel_valid:
            for m in mutants:
                mp = write_mutant(work, gtext, m)
                st = subprocess.run([sys.executable, '-I', mp, '--selftest'], capture_output=True,
                                    env=env_for(work), timeout=GUARD_TIMEOUT)
                st_kill = st.returncode != 0
                res['selftest_kills'] += int(st_kill)
                mr = run_generator(genp, mp, work, m['id'])
                status = 'survived'
                if mr['exit'] == 1 and mr['last'] and mr['last'].group(3) != 'none' and mr['dump']:
                    k = int(mr['last'].group(3))
                    hit = [c for c in mr['dump'] if c['index'] == k]
                    if len(hit) == 1:
                        a = comparable(run_guard(gp, hit[0], work, 'cp-' + m['id']))
                        b = comparable(run_guard(mp, hit[0], work, 'cm-' + m['id']))
                        status = 'confirmed' if a != b else 'unconfirmed'
                    else:
                        status = 'unconfirmed'
                elif mr['exit'] not in (0, 1):
                    status = 'generator-error-%s' % mr['exit']
                res['confirmed'] += int(status == 'confirmed')
                print('MUTANT %s %s generator=%s selftest_kill=%s' % (m['id'], m['name'], status,
                                                                      str(st_kill).lower()))
    res['classes_short'] = sum(1 for k in CLASSES if counts[k] < CLASS_MIN)
    for k in CLASSES:
        print('CLASS %s=%d%s' % (k, counts[k], '' if counts[k] >= CLASS_MIN else ' SHORT'))
    rb, notes = records(lane, rev)
    res['records_bad'] = rb
    for n in notes:
        print('RECORD %s' % n)
    total = (res['absent'] + res['pristine_bad'] + res['oracle_disagree'] + res['classes_short'] +
             res['panel_invalid'] + max(0, KILL_TARGET - res['confirmed']) + res['records_bad'])
    with open(__file__, 'rb') as fh:
        self_sha = sha(fh.read())[:12]
    print('C2_R49: self=%s rev=%s generator=%s pristine_exit=%s cases=%s violations=%s dump=%s '
          'oracle_disagree=%d classes_short=%d panel=%d panel_valid=%d confirmed=%d target=%d '
          'selftest_kills=%d records_bad=%d total=%d C2_R49_PASS=%s'
          % (self_sha, rev, 'absent' if genp is None else 'present', pexit, cases_run, viol, dumpn,
             res['oracle_disagree'], res['classes_short'], len(mutants), 0 if res['panel_invalid'] else 1,
             res['confirmed'], KILL_TARGET, res['selftest_kills'], res['records_bad'], total,
             'true' if total == 0 else 'false'))
    return 0 if total == 0 else 1


def witness(lane, rev, work, panel_path, cases_path):
    gbytes, gp, _ = materialize(lane, rev, work, GENERATOR)
    mutants, valid, gtext = load_panel(panel_path, gbytes)
    cases = load_dump(cases_path) or []
    confirmed = 0
    for m in mutants:
        mp = write_mutant(work, gtext, m)
        hit = None
        for c in cases:
            if comparable(run_guard(gp, c, work, 'wp')) != comparable(run_guard(mp, c, work, 'wm')):
                hit = c['index']
                break
        confirmed += int(hit is not None)
        print('WITNESS %s %s case=%s' % (m['id'], m['name'], hit))
    print('C2_R49_WITNESS: panel=%d panel_valid=%d witness_confirmed=%d' % (len(mutants), int(valid), confirmed))
    return 0 if valid and confirmed == len(mutants) else 1


def selftest():
    cases = []

    def case(name, ok):
        cases.append((name, bool(ok)))
        print('CASE %s %s' % (name, 'PASS' if ok else 'FAIL'))

    H = '| id | source | k | t | s | a | te | st | op | re | ub |\n|---|---|---|---|---|---|---|---|---|---|---|\n'

    def row(i, doc, ind=0):
        return ' ' * ind + '| %s | D — %s | d | A | x | y | z | mined | 2026-01-01 | 180d | - |\n' % (i, doc)
    case('oracle-collision', oracle(H + row('S001', 'https://a'), H + row('S001', 'https://b', 2))
         == (0, ['S001'], 1, 1))
    case('oracle-indent4-not-row', oracle(H + row('S001', 'https://a'), H + row('S001', 'https://b', 4))
         == (0, [], 1, 0))
    case('oracle-duplicate-refusal', oracle(H + row('S001', 'x') + row('S001', 'y'), H)[0] == 2)
    case('oracle-short-row-refusal', oracle(H + '| S001 | a | b | c |\n', H)[0] == 2)
    case('oracle-numeric-sort', oracle(H + row('S010', 'a') + row('S9', 'b') + row('S100', 'c'),
                                       H + row('S100', 'q') + row('S010', 'r'))[1] == ['S010', 'S100'])
    c = {'registry': H + row('S1001', 'https://www.e.test/a/'), 'staged': H + row('S1001', 'https://e.test/a', 3),
         'map': None}
    cl = case_classes(c, (0, {'collision_count': 1, 'held': {'S1001': 'S1001'}, 'unmapped': [], 'cascade': []}))
    case('classes-basic', cl == {'indent_1_3', 'id_4_plus_digits', 'collision', 'held', 'url_form_variant'})
    cl = case_classes({'registry': H, 'staged': H + row('S001', 'x', 5), 'map': {'map': {}}}, (1, None))
    case('classes-map', cl == {'indent_4_plus', 'map', 'map_inadmissible'})
    case('classes-refusal', 'refusal' in case_classes({'registry': H, 'staged': H, 'map': None}, (2, None)))
    case('last-line', bool(LAST_RE.match('PBT_STAGED_ID: cases=400 violations=0 counterexample=none x=1'))
         and not LAST_RE.match('PBT_STAGED_ID: cases=4 violations=1'))
    case('comparable-ignores-shas', comparable((0, {'a': 1, 'registry_sha256': 'x'}, b''))
         == comparable((0, {'a': 1, 'registry_sha256': 'y'}, b'')))
    case('comparable-exit', comparable((0, None, b'z')) != comparable((1, None, b'z')))
    failed = sum(1 for _, ok in cases if not ok)
    print('C2_R49_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--work')
    ap.add_argument('--panel')
    ap.add_argument('--generator-path', default=GENERATOR)
    ap.add_argument('--witness')
    ap.add_argument('--selftest', action='store_true')
    try:
        a = ap.parse_args()
    except SystemExit:
        return 64
    if a.selftest:
        return selftest()
    if not (a.lane and a.rev and a.work and a.panel):
        return 64
    lane = os.path.realpath(a.lane)
    r = git(lane, 'rev-parse', '--verify', '--quiet', '--end-of-options', a.rev + '^{commit}')
    if r.returncode != 0 or a.rev.startswith('-'):
        print('C2_R49: setup=unresolvable-rev', file=sys.stderr)
        return 2
    rev = r.stdout.decode().strip()
    work = os.path.realpath(a.work)
    os.makedirs(work, exist_ok=True)
    if os.listdir(work):
        print('C2_R49: setup=work-not-empty', file=sys.stderr)
        return 2
    try:
        if a.witness:
            return witness(lane, rev, work, a.panel, a.witness)
        return measure(lane, rev, work, a.panel, a.generator_path)
    except Setup as exc:
        print('C2_R49: setup=%s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
