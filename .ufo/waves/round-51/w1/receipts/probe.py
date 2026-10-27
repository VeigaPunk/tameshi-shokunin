#!/usr/bin/env python3
"""T51MutC2Counter probe: mutation-test the frozen round-51 C2 counter.

Detectors (the committed, pre-registered ones):
  D1  python3 <counter> --selftest          -> exit 0, 'C2_R51_SELFTEST: cases=11 failed=0'
  D2  <counter> --lane CTL_0  --rev HEAD    -> exit 1, last line endswith 'C2_R51_PASS=false'
  D3  <counter> --lane CTL_COMMENT          -> exit 1, last line endswith 'C2_R51_PASS=false'
  D2/D3 are exactly the C2 rows of the committed controls.py PLAN (expect false).

Flip proof: forged scratch tree T_X satisfies every clause except X; the pristine
counter must reject it naming X=0, the mutant must print C2_R51_PASS=true.

Stages: mutants | baseline | controls | flips | all
Everything lives under S=/fast/scratch/hyaku/tameshi-r51/T51MutC2Counter/probe.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
KAGI = os.path.join(FLEET, 'kagi-shokunin')
BASE = '9962033fd7a75aa2f2847e979dd687a5d28505a1'
S = '/fast/scratch/hyaku/tameshi-r51/T51MutC2Counter'
ROOT = os.path.join(S, 'probe')
RCPT = os.path.join(S, 'receipts')
PRISTINE = os.path.join(S, 'measure.orig.py')
RUNNER_BASE = os.path.join(S, 'runner-base.sh')
SPEC_REL = '.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec'
SWEEP_REL = '.ufo/evidence/round-51/c2/sweep/sweep.txt'
PIN = 'c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb'
DRIFT_REV = 'e64e81b8eb96f3682b00c1e7a291e84420b280fa'
ENTRY_REL = 'corpus/knowledge/r51-drift-pins.md'
VERDICTS = [('K_MODE_CMP', 'KILLED'), ('K_GONE_ARM', 'SURVIVED'), ('K_AMBIG_GT', 'SURVIVED'),
            ('K_COUNT_GE', 'KILLED'), ('K_SHAPE_OPTIN', 'SURVIVED'), ('S_SHA_CMP', 'SURVIVED'),
            ('S_HARDLINK', 'SURVIVED'), ('S_POLICY', 'SURVIVED'), ('S_DUP_UNIQ', 'SURVIVED'),
            ('S_USAGE_EXIT', 'SURVIVED')]
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           HYAKU_SCRATCH=os.path.join(S, 'hyaku-scratch'))

ORIG = open(PRISTINE, 'rb').read()


def log(name, text):
    os.makedirs(RCPT, exist_ok=True)
    with open(os.path.join(RCPT, name + '.txt'), 'w') as fh:
        fh.write(text)


def git(repo, *a):
    r = subprocess.run(['git', '-C', repo, *a], capture_output=True, env=ENV)
    if r.returncode:
        raise RuntimeError('git %s: %s' % (a[0], r.stderr.decode(errors='replace')[:400]))
    return r


# ---------------------------------------------------------------- mutants
MUTANTS = [
    ('M01_wired_clause_drop', 'all-10-wired clause dropped from passed',
     "passed = recorded == 10 and len(wired) == 10 and f['new_legs'] == 1",
     "passed = recorded == 10 and f['new_legs'] == 1"),
    ('M02_spec_sha_drop', 'spec-sha256 == frozen SPEC_SHA dropped',
     " and hashlib.sha256(spec).hexdigest() == SPEC_SHA and emb == spec:",
     " and emb == spec:"),
    ('M03_embed_equality_drop', 'embedded-heredoc == spec-file dropped',
     "hashlib.sha256(spec).hexdigest() == SPEC_SHA and emb == spec:",
     "hashlib.sha256(spec).hexdigest() == SPEC_SHA:"),
    ('M04_after_freeze_drop', "sweep_after_freeze dropped from need",
     "'sweep_ok', 'sweep_after_freeze', 'table_match', ",
     "'sweep_ok', 'table_match', "),
    ('M05_control_pin_wildcard', 'CONTROL pristine-sha256==PIN wildcarded',
     "pristine-sha256=%s\\)$' % pin, text, re.M):",
     "pristine-sha256=[0-9a-f]+\\)$', text, re.M):"),
    ('M06_verdict_set_relax', 'dup/INCONCLUSIVE defect verdict lines accepted',
     " != sorted(ids) or any(len(v) != 1 or v[0] == 'INCONCLUSIVE' for v in verdicts.values()):",
     " != sorted(ids):"),
    ('M07_table_match_drop', 'TABLE == sweep verdicts dropped from need',
     "'table_match', 'regression',",
     "'regression',"),
    ('M08_regression_breadth', "accept any 'REGRESSION: PASS (' (not cases=10)",
     "last.startswith('REGRESSION: PASS (cases=10 passed=10'",
     "last.startswith('REGRESSION: PASS ('"),
    ('M09_entry_date_drop', 'SOURCES row opened-2026-10-26 check dropped',
     " and c[8] == '2026-10-26' and path in",
     " and path in"),
    ('M10_usedby_drop', 'used-by-lists-entry check dropped',
     " and path in [p.strip() for p in re.split(r'[,;]', c[10])]:",
     ":"),
    ('M11_readme_prefix_drop', 'README append-only (startswith base) guard dropped',
     " if readme.startswith(base_readme) else ''",
     ""),
    ('M12_target_new_drop', 'copied leg target accepted (target_new always 1)',
     "f['target_new'] = 1 if rel not in BASE_LEGS.values() else 0",
     "f['target_new'] = 1"),
    ('M13_pin_verify_drop', 'PIN==sha256(blob@rev) dropped (syntactic pin ok)',
     "f['pin_ok'] = 1 if blob is not None and hashlib.sha256(blob).hexdigest() == pin else 0",
     "f['pin_ok'] = 1 if pin and lrev else 0"),
    ('M14_base_present_drop', 'nine base legs retained check dropped',
     "if len(new) == 1 and base_present:",
     "if len(new) == 1:"),
    ('M15_freeze_ts_zero', 'spec first-add commit time ignored (freeze_ts=0)',
     "freeze_ts = int(first[-1]) if first else None",
     "freeze_ts = 0"),
    ('M16_recorded_clause_drop', 'recorded == 10 dropped from passed (redundancy probe)',
     "passed = recorded == 10 and len(wired) == 10 and f['new_legs'] == 1",
     "passed = len(wired) == 10 and f['new_legs'] == 1"),
    ('M17_exit_always_zero', 'verdict wiring: measure() always exits 0',
     "    return (0 if passed else 1), line, explain",
     "    return 0, line, explain"),
]


def mutant_path(mid):
    for m, _d, old, new in MUTANTS:
        if m == mid:
            src = ORIG.decode()
            assert src.count(old) == 1, (mid, src.count(old))
            p = os.path.join(S, 'mutants', 'M_%s.py' % mid)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w').write(src.replace(old, new, 1))
            return p
    raise KeyError(mid)


# ---------------------------------------------------------------- fixtures
def fixture(name):
    d = os.path.join(ROOT, name, 'tameshi-shokunin')
    if os.path.exists(d):
        shutil.rmtree(os.path.dirname(d))
    os.makedirs(os.path.dirname(d))
    r = subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], capture_output=True, env=ENV)
    assert r.returncode == 0, r.stderr
    git(d, 'checkout', '-q', '--detach', BASE)
    top = git(d, 'rev-parse', '--show-toplevel').stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), 'fixture toplevel mismatch'
    return d


def commit_all(d, msg):
    if not git(d, 'status', '--porcelain').stdout.strip():
        return git(d, 'rev-parse', 'HEAD').stdout.decode().strip()
    git(d, 'add', '-A')
    r = git(d, '-c', 'user.name=probe', '-c', 'user.email=probe@invalid', 'commit', '-qm', msg)
    return git(d, 'rev-parse', 'HEAD').stdout.decode().strip()


def ctl_edit_comment(d):
    p = os.path.join(d, 'tools/mutate-and-run.sh')
    s = open(p, encoding='utf-8').read()
    anchor = '#   js-cite-check         kumitate-shokunin/scripts/cite-check.mjs    5/10 (50 %)\n'
    assert s.count(anchor) == 1
    open(p, 'w', encoding='utf-8').write(
        s.replace(anchor, anchor + '#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          5/10 (50 %)\n'))


# ------------------------------------------------------------- forge parts
def spec_bytes():
    r = subprocess.run(['git', '-C', LANE, 'show', 'HEAD:%s' % SPEC_REL], capture_output=True, env=ENV)
    assert r.returncode == 0, r.stderr
    b = r.stdout
    assert hashlib.sha256(b).hexdigest() == 'a98271f639bc520f7052e63efaaa0b560cda959d3122d9c6921dcd1b9b61a602', \
        'HEAD spec bytes do not match frozen SPEC_SHA'
    return b


def blob_sha(repo, rev, rel):
    r = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, rel)], capture_output=True, env=ENV)
    assert r.returncode == 0, (rev, rel, r.stderr[:200])
    return hashlib.sha256(r.stdout).hexdigest()


def sweep_text(date, control_pin, verdicts):
    L = ['MUTATE_TOOL: tools/mutate-and-run.sh sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9',
         'MUTATE_DATE: %s' % date,
         'MUTATE_TARGET: /fast/scratch/hyaku/tameshi-r51/T51MutC2Counter/probe/drift-pins.sh sha256=%s bytes=19088' % PIN,
         'MUTATE_SPEC: .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec defects=10',
         'CONTROL: GREEN (exit=0 duration-ms=220 pristine-sha256=%s)' % control_pin,
         '  | DRIFT_SELFTEST: PASS (13 cases)']
    for did, v in verdicts:
        if v == 'KILLED':
            L += ['DEFECT %s: KILLED (exit=1 duration-ms=252) probe' % did,
                  '  | drift-selftest: FAIL probe: exit 0 want 1',
                  '  | DRIFT_SELFTEST: FAIL (1/13 cases)']
        elif v == 'SURVIVED':
            L += ['DEFECT %s: SURVIVED (exit=0 duration-ms=190) probe' % did,
                  '  | DRIFT_SELFTEST: PASS (13 cases)']
        else:
            L += ['DEFECT %s: INCONCLUSIVE (exit=2 duration-ms=180) probe' % did,
                  '  | DRIFT_SELFTEST: PASS (13 cases)']
    L += ['MUTATE_RESTORE: OK (target-sha256 before=%s after=%s pristine-sha256=%s)' % (PIN, PIN, PIN),
          'MUTATE: DONE (defects=10 killed=2 survived=8)',
          'MUTATE_EVIDENCE: /fast/scratch/hyaku/tameshi-r51/T51MutC2Counter/probe/w']
    return '\n'.join(L) + '\n'


def sources_row(opened, usedby):
    return ('| S272 | drift-pin craft (probe fixture row, synthetic) | probe | C | '
            'counter-mutation probe: not a real reading | none (synthetic scratch fixture) | '
            'scratch-only, never cited outside this fixture | mined | %s | 1d | %s |\n' % (opened, usedby))


def entry_text(tail):
    return ('# drift pins probe entry (synthetic fixture)\n\n'
            'source: %s via S272\n\n'
            'Forged scratch fixture entry for the round-51 C2 counter mutation probe.\n'
            'Not a real reading; exists only inside the probe fixture.\n' % tail)


def forge_runner(d, neuter_cases=None, ledger='add', legcheck_k=2, table_text=None,
                 call_rel='kagi-shokunin/corpus/drift-pins.sh', pin=PIN,
                 heredoc_mode='full', drop_citecheck=False, rev=DRIFT_REV):
    p = os.path.join(d, 'tools/mutate-and-run.sh')
    s = open(p, encoding='utf-8').read()
    tb = table_text or ','.join('%s:%s' % (i, v) for i, v in VERDICTS)

    if neuter_cases:
        s = s.replace('#!/usr/bin/env bash\n',
                      '#!/usr/bin/env bash\n'
                      'if [ "${1:-}" = "--regression" ]; then\n'
                      '  printf \'REGRESSION: PASS (cases=%s passed=%s; forged-probe neuter)\\n\'\n'
                      '  exit 0\n'
                      'fi\n' % (neuter_cases, neuter_cases), 1)

    anchor = '#   js-cite-check         kumitate-shokunin/scripts/cite-check.mjs    5/10 (50 %)\n'
    assert s.count(anchor) == 1
    add = '#   bash-drift-pins        kagi-shokunin/corpus/drift-pins.sh          5/10 (50 %)\n'
    if ledger == 'add':
        s = s.replace(anchor, anchor + add, 1)
    elif ledger == 'm14':
        # drop one base leg line, duplicate another, add the new leg:
        # recorded=10, legs=10 (one base missing), new_legs=1, base_present=False
        surf = '#   bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)\n'
        assert s.count(surf) == 1 and anchor in s
        s = s.replace(anchor, add, 1).replace(surf, surf + surf, 1)

    var_anchor = re.search(r"^TABLE_BASH='[^']*'$", s, re.M).group(0)
    s = s.replace(var_anchor,
                  var_anchor + '\nPIN_DRIFT=%s\nREV_DRIFT=%s\nTABLE_DRIFT=\'%s\'' % (pin, rev, tb), 1)

    entry_anchor = "    'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5'\n"
    assert s.count(entry_anchor) == 1
    s = s.replace(entry_anchor,
                  entry_anchor + "    'bash-drift-pins:bash-drift-pins.spec:TABLE_DRIFT:%d:%d'\n"
                  % (len(VERDICTS), legcheck_k), 1)

    call_anchor = re.search(r'  regression_case_git js-cite-check \\\n(?:.*\n){4}', s).group(0)
    assert 'st_citecheck=$?' in call_anchor
    s = s.replace(call_anchor, call_anchor +
                  "  regression_case_git bash-drift-pins \\\n"
                  "    '%s' \"$PIN_DRIFT\" \"$REV_DRIFT\" \\\n"
                  "    \"$specs/bash-drift-pins.spec\" 'bash \"$MUTANT\" --selftest' \"$TABLE_DRIFT\" \\\n"
                  "    \"$root/bash-drift-pins\"\n" % call_rel, 1)

    m = re.search(r"^  cat >\"\$d/js-cite-check\.spec\" <<'EOT'\n(.*?)^EOT$", s, re.M | re.S)
    assert m
    emb = spec_bytes()
    if heredoc_mode == 'full':
        content = emb
    elif heredoc_mode == 'tail':     # M02: spec file AND heredoc carry an extra line (sha off)
        content = emb + b'# forged-tail (probe)\n'
    elif heredoc_mode == 'short':    # M03: spec file stays frozen; heredoc loses its last defect line
        content = b'\n'.join(emb.split(b'\n')[:-3]) + b'\n'
    else:
        raise ValueError(heredoc_mode)
    cs = content.decode('utf-8', 'surrogateescape')
    block = "  cat >\"$d/bash-drift-pins.spec\" <<'EOT'\n" + cs + 'EOT\n'
    s = s[:m.end()] + '\n' + block + s[m.end() + 1:]
    open(p, 'w', encoding='utf-8').write(s)


def forge_tree(name, date='2099-01-01T00:00:00Z', control_pin=PIN, verdicts=None,
               opened='2026-10-26', usedby=ENTRY_REL, readme='append',
               call_rel='kagi-shokunin/corpus/drift-pins.sh', pin=PIN,
               spec_mode='full', heredoc_mode='full', legcheck_k=2, table_text=None,
               neuter_cases='10', ledger='add', rev=DRIFT_REV):
    d = fixture(name)
    forge_runner(d, neuter_cases=neuter_cases, ledger=ledger, legcheck_k=legcheck_k,
                 table_text=table_text, call_rel=call_rel, pin=pin, heredoc_mode=heredoc_mode,
                 rev=rev)
    os.makedirs(os.path.join(d, '.ufo/evidence/round-51/c2/sweep'), exist_ok=True)
    spec = spec_bytes()
    if spec_mode == 'tail':          # M02: committed spec is not the frozen bytes
        spec = spec + b'# forged-tail (probe)\n'
    open(os.path.join(d, SPEC_REL), 'wb').write(spec)
    open(os.path.join(d, SWEEP_REL), 'w', encoding='utf-8').write(
        sweep_text(date, control_pin, verdicts or VERDICTS))
    with open(os.path.join(d, 'corpus/SOURCES.md'), 'a', encoding='utf-8') as fh:
        fh.write(sources_row(opened, usedby))
    os.makedirs(os.path.join(d, 'corpus/knowledge'), exist_ok=True)
    open(os.path.join(d, ENTRY_REL), 'w', encoding='utf-8').write(entry_text(call_rel.split('/', 1)[1]))
    rp = os.path.join(d, 'corpus/README.md')
    body = open(rp, encoding='utf-8').read()
    if readme == 'append':
        body += '\n- knowledge/r51-drift-pins.md — forged probe entry (counter-mutation fixture).\n'
    else:                            # 'rewrite': base prefix broken AND name appended
        first = body.split('\n', 1)[0]
        body = body.replace(first, first + ' [probe]', 1) + \
            '\n- knowledge/r51-drift-pins.md — forged probe entry (counter-mutation fixture).\n'
    open(rp, 'w', encoding='utf-8').write(body)
    commit_all(d, 'probe: forged C2 tree %s' % name)
    return d


# ---------------------------------------------------------------- running
def run_counter(py, d, tag, timeout=1500):
    work = os.path.join(ROOT, 'work-%s' % tag)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(os.path.join(work, 'w'))
    os.makedirs(os.path.join(work, 'tmp'))
    t0 = time.time()
    r = None
    try:
        r = subprocess.run([sys.executable, py, '--lane', d, '--rev', 'HEAD', '--work',
                            os.path.join(work, 'w'), '--explain'],
                           capture_output=True, env=dict(ENV, TMPDIR=os.path.join(work, 'tmp')),
                           timeout=timeout)
        out, rc = r.stdout.decode(errors='replace'), r.returncode
    except subprocess.TimeoutExpired:
        out, rc = 'TIMEOUT after %ss' % timeout, 124
    dt = time.time() - t0
    lines = [l for l in out.split('\n') if l.strip()]
    last = lines[-1] if lines else '(no stdout)'
    shutil.rmtree(work, ignore_errors=True)
    log('run-%s' % tag, '$ %s --lane %s --rev HEAD --work <empty> --explain\nrc=%d wall=%.1fs\n--- stdout ---\n%s\n--- stderr ---\n%s'
        % (py, d, rc, dt, out, r.stderr.decode(errors='replace') if r is not None else '(timeout)'))
    return rc, last, dt


def run_selftest(py, tag):
    os.makedirs(os.path.join(ROOT, 'st-tmp'), exist_ok=True)
    t0 = time.time()
    r = subprocess.run([sys.executable, py, '--selftest'], capture_output=True,
                       env=dict(ENV, TMPDIR=os.path.join(ROOT, 'st-tmp')), timeout=300)
    out = r.stdout.decode(errors='replace') + r.stderr.decode(errors='replace')
    log('selftest-%s' % tag, '$ %s --selftest\nrc=%d wall=%.1fs\n%s' % (py, r.returncode, time.time() - t0, out))
    return r.returncode, out.strip().split('\n')[-1]


# ---------------------------------------------------------------- stages
def stage_mutants():
    for mid, _d, _o, _n in MUTANTS:
        p = mutant_path(mid)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        print('%-26s sha256=%s' % (mid, h))


def stage_baseline():
    print('== D1 pristine selftest ==');  rc, last = run_selftest(PRISTINE, 'pristine')
    print('rc=%d %s' % (rc, last))
    d0 = fixture('ctl0');  commit_all(d0, 'probe: CTL_0 (no change)')
    print('== D2 pristine on CTL_0 ==');  rc, last, dt = run_counter(PRISTINE, d0, 'pristine-ctl0')
    print('rc=%d wall=%.0fs %s' % (rc, dt, last))
    dc = fixture('ctlcomment');  ctl_edit_comment(dc);  commit_all(dc, 'probe: CTL_COMMENT')
    print('== D3 pristine on CTL_COMMENT ==');  rc, last, dt = run_counter(PRISTINE, dc, 'pristine-ctlcomment')
    print('rc=%d wall=%.0fs %s' % (rc, dt, last))
    da = forge_tree('t-all')
    print('== pristine on fully-forged T_all ==');  rc, last, dt = run_counter(PRISTINE, da, 'pristine-tall')
    print('rc=%d wall=%.0fs %s' % (rc, dt, last))


CTL = {}


def get_ctls():
    if not CTL:
        d0 = fixture('ctl0');  commit_all(d0, 'probe: CTL_0 (no change)')
        dc = fixture('ctlcomment');  ctl_edit_comment(dc);  commit_all(dc, 'probe: CTL_COMMENT')
        CTL['d2'] = d0; CTL['d3'] = dc
    return CTL


def one_controls(mid):
    p = mutant_path(mid)
    r1 = run_selftest(p, mid)
    ctls = get_ctls()
    r2 = run_counter(p, ctls['d2'], '%s-ctl0' % mid)
    r3 = run_counter(p, ctls['d3'], '%s-ctlcomment' % mid)
    d1_kill = not (r1[0] == 0 and 'cases=11 failed=0' in r1[1])
    d2_kill = not (r2[0] == 1 and r2[1].endswith('C2_R51_PASS=false'))
    d3_kill = not (r3[0] == 1 and r3[1].endswith('C2_R51_PASS=false'))
    verdict = 'KILLED-by-%s' % ('D1' if d1_kill else 'D2' if d2_kill else 'D3' if d3_kill else 'none')
    print('%-26s D1 rc=%d %s | D2 rc=%d %s | D3 rc=%d %s -> %s'
          % (mid, r1[0], r1[1][-34:], r2[0], r2[1][-60:], r3[0], r3[1][-60:], verdict))
    return mid, verdict


def stage_controls(only=None):
    mids = [m for m, *_ in MUTANTS if not only or m in only]
    get_ctls()
    with ThreadPoolExecutor(max_workers=3) as ex:
        for mid, verdict in ex.map(one_controls, mids):
            pass


# clause -> (mutant, forge kwargs, expected pristine marker)
FLIPS = [
    ('wired(M01)', 'M01_wired_clause_drop', dict(legcheck_k=3), 'wired_legs=9'),
    ('spec_sha(M02)', 'M02_spec_sha_drop', dict(spec_mode='tail', heredoc_mode='tail'), 'spec_prereg=0'),
    ('spec_embed(M03)', 'M03_embed_equality_drop', dict(heredoc_mode='short'), 'spec_prereg=0'),
    ('after_freeze(M04)', 'M04_after_freeze_drop', dict(date='2020-01-01T00:00:00Z'), 'sweep_after_freeze=0'),
    ('control_pin(M05)', 'M05_control_pin_wildcard', dict(control_pin='a' * 64), 'sweep_ok=0'),
    ('verdict_set(M06)', 'M06_verdict_set_relax',
     dict(verdicts=[(i, ('INCONCLUSIVE' if i == 'S_USAGE_EXIT' else v)) for i, v in VERDICTS],
          table_text=','.join('%s:%s' % (i, 'INCONCLUSIVE' if i == 'S_USAGE_EXIT' else v) for i, v in VERDICTS)),
     'sweep_ok=0'),
    ('table_match(M07)', 'M07_table_match_drop',
     dict(table_text=','.join('%s:%s' % (i, v) for i, v in
                              [('K_MODE_CMP', 'SURVIVED'), ('K_GONE_ARM', 'KILLED')] +
                              [(i, v) for i, v in VERDICTS[2:]])),
     'table_match=0'),
    ('regression9(M08)', 'M08_regression_breadth', dict(neuter_cases='9'), 'regression=0'),
    ('entry_date(M09)', 'M09_entry_date_drop', dict(opened='2026-10-19'), 'sourced=0'),
    ('usedby(M10)', 'M10_usedby_drop', dict(usedby='corpus/knowledge/some-other-entry.md'), 'sourced=0'),
    ('readme_prefix(M11)', 'M11_readme_prefix_drop', dict(readme='rewrite'), 'readme=0'),
    ('target_new(M12)', 'M12_target_new_drop',
     dict(call_rel='kagi-shokunin/corpus/surface-census.sh',
          pin='COMPUTE', control_pin='COMPUTE',
          rev='fecee8743e52eb8fb5fbb40782934cb619a1a96e'),
     'target_new=0'),
    ('pin_verify(M13)', 'M13_pin_verify_drop', dict(pin='f' * 64,
                                                    control_pin='f' * 64), 'pin_ok=0'),
    ('base_present(M14)', 'M14_base_present_drop', dict(ledger='m14'), 'pin_ok=0'),
]


def stage_flips(only=None):
    for clause, mid, kw, marker in FLIPS:
        if only and clause not in only:
            continue
        kw = dict(kw)
        if kw.get('pin') == 'COMPUTE':
            kw['pin'] = blob_sha(KAGI, kw['rev'], kw['call_rel'].split('/', 1)[1])
            kw['control_pin'] = kw['pin']
        d = forge_tree('t-' + clause.split('(')[0], **kw)
        rc0, last0, _ = run_counter(PRISTINE, d, 'flip-%s-pristine' % clause.split('(')[0])
        rc1, last1, _ = run_counter(mutant_path(mid), d, 'flip-%s-mutant' % clause.split('(')[0])
        ok0 = rc0 == 1 and marker in last0 and last0.endswith('C2_R51_PASS=false')
        ok1 = rc1 == 0 and last1.endswith('C2_R51_PASS=true')
        print('%-18s pristine: rc=%d %s | mutant %s: rc=%d %s -> %s'
              % (clause, rc0, 'rejects(%s)' % marker if ok0 else last0[-70:],
                 mid, rc1, 'ACCEPTS' if ok1 else last1[-70:],
                 'BLIND-SPOT-CONFIRMED' if ok0 and ok1 else 'CHECK'))
        shutil.rmtree(os.path.dirname(d), ignore_errors=True)


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else 'all'
    os.makedirs(ROOT, exist_ok=True)
    os.makedirs(RCPT, exist_ok=True)
    assert hashlib.sha256(ORIG).hexdigest() == 'c2c80c0b9e8a7a86ff381b54de8806eb4bcdc415a92b5aa12ddbb366e0432d84'
    if stage in ('mutants', 'all'):
        stage_mutants()
    if stage in ('baseline', 'all'):
        stage_baseline()
    if stage in ('controls', 'all'):
        stage_controls()
    if stage in ('flips', 'all'):
        stage_flips()


if __name__ == '__main__':
    main()
