#!/usr/bin/env python3
"""Round 30 C1 counter v4 (operability: the `--regression` case-tally surface of
tools/mutate-and-run.sh), frozen before data in .ufo/evidence/round-30/contract.json.

Usage: c1-measure-v4.py --repo LANE_CLONE --rev REV --sealed SEALED_JSON [--jobs N]

v4 (contract-amendment-3.json, attempt 2, after control CtlK8NoRun met v3 and
before any data): CtlK8NoRun met v3 with a static allowlist of the public
generators' finite text language. v4 adds (j) and (k): a SEALED set of 6 mutants
and 6 equivalent rewrites of the tally block, written by the L1 of attempt 2
(the attempt-1 seat SealHeldout died with no output; its task was not resent)
against the frozen fix's tally block (witness/fix.diff, lane commit 8a8d2540).
Only its sha256 (SEALED_SHA256 below) is committed before any v4 control or data;
the file itself is committed after the measurement at the landed head.
v4 also isolates every --selftest run (L1 self-attack on the v4 draft, before
freeze: the draft ran each selftest in a directory named after its job, e.g.
`st-S-e-preinc`, so a selftest keyed on its own directory name, or on
/proc/$PPID/cmdline, the counter source or the sealed file, could classify jobs
without testing the tally). Each run is a bubblewrap sandbox: new pid, net, ipc,
uts and user namespaces, a cleared environment, read-only /usr and /etc, private
/tmp, and only its own copy of tools/ bound at the same path /w for every job.

v3 (contract-amendment-2.json, after control CtlK7Keyed met v2 and before any
data): a selftest that regex-matches the arm and threshold lines for the
generator's known mutant classes met v2 without running the tally. v3 adds (h)
and (i): statements inserted into the tally block (after the loop, or inside the
loop body) that add an arithmetic term to one counter. Each term is a random
expression whose value is 0 (an equivalent rewrite) or not (a mutant), so a
text-keyed check cannot separate them without evaluating the block.

v2 (contract-amendment-1.json, before any control or data): v1's 13 mutants and
4 rewrites are fixed strings, so a selftest that greps its own runner for those
exact strings would meet v1 without testing the tally. v2 adds (f) and (g): a
held-out set drawn by a frozen generator seeded with the REV commit id, so the
spellings are unknown until the fix is committed.

Routed defect: round-29-verifier-spotcheck.md routed item 7 / round-29.md routed
item 4.6 (seat MutateLegSum): dropping one leg status from the tally loop makes
`--regression` print `REGRESSION: PASS (cases=9 passed=8 ...)`, exit 0, and the
runner's own `--selftest` (97/97) does not notice.

Frozen predicate (same sentence in contract.json, same condition in code below,
same label in the receipt):

  C1_R30_PASS is true iff, on tools/mutate-and-run.sh at REV,
  (a) the pristine runner's --selftest exits 0 and prints `VERDICT: PASS`;
  (b) the pristine tally block, run under the fixed-status harness, gives
      PASS/exit 0 for all-zero statuses, FAIL/exit 1 for each of the 9
      single-leg status-1 vectors and SETUP/exit 2 for each of the 9 single-leg
      status-2 vectors (19/19);
  (c) each of the 9 drop mutants (one operand removed from the tally loop) is
      refused at run time: under the harness, for the all-zero vector and for the
      vector whose dropped leg has status 1, it neither exits 0 nor prints
      `REGRESSION: PASS` (refused_drops == 9);
  (d) --selftest exits non-zero (or times out) on each of the 13 family mutants
      (9 drops + 4 arm mutants) (killed == 13);
  (e) --selftest exits 0 with `VERDICT: PASS` on each of the 4 frozen
      semantics-preserving rewrites of the tally block (equiv_pass == 4);
  (f) --selftest exits non-zero (or times out) on each of the 12 held-out
      mutants drawn by heldout() with seed int(REV, 16) (heldout_killed == 12);
  (g) --selftest exits 0 with `VERDICT: PASS` on each of the 4 held-out
      equivalent rewrites drawn by the same generator (heldout_equiv == 4);
  (h) --selftest exits non-zero (or times out) on each of the 8 inserted-term
      mutants drawn by inserted() with seed int(REV, 16) + 1 (insert_killed == 8);
  (i) --selftest exits 0 with `VERDICT: PASS` on each of the 4 inserted-term
      equivalent rewrites drawn by the same call (insert_equiv == 4);
  (j) the sealed file's sha256 equals SEALED_SHA256, its block_sha256 equals the
      sha256 of the tally block at REV (sealed_block_match == 1), and --selftest
      exits non-zero (or times out) on each of the 6 sealed mutants
      (sealed_killed == 6);
  (k) --selftest exits 0 with `VERDICT: PASS` on each of the 6 sealed equivalent
      rewrites (sealed_equiv == 6).
  A sealed item whose `old` text is not found exactly once in the block, a sealed
  mutant that is harness-equivalent to the block, or a sealed rewrite that differs
  from it under the harness is a counter error (exit 2).

Mutants and rewrites are applied by exact text replacement on the REV bytes. A
replacement site that is not found exactly once is a counter error: exit 2 and
PASS false. Prints one `C1_R30:` summary line and `PREDICATE: C1_R30_PASS=...`.
Exit 0 iff PASS; 1 if not; 2 on counter error.
"""
import argparse
import hashlib
import json
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
import sys
import tempfile

RUNNER = 'tools/mutate-and-run.sh'
LOOP_RE = re.compile(r'^(?P<ind>[ \t]*)for st in (?P<ops>(?:"\$st_[a-z]+" ?){9}); do$', re.M)
BLOCK_START = '  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n'
ARM0 = '      0) npass=$((npass + 1)) ;;\n'
ARM1 = '      1) nfail=$((nfail + 1)) ;;\n'
ARMS = '      *) nsetup=$((nsetup + 1)) ;;\n'
FAILCHK = '  if [[ $nfail -gt 0 ]]; then\n'
PASSLINE = "  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\\n' \\\n"

ARM_MUTANTS = [
    ('A1-pass-arm-noop', ARM0, '      0) npass=$((npass + 0)) ;;\n'),
    ('A2-fail-arm-as-pass', ARM1, '      1) npass=$((npass + 1)) ;;\n'),
    ('A3-fail-threshold', FAILCHK, '  if [[ $nfail -gt 1 ]]; then\n'),
    ('A4-setup-arm-as-pass', ARMS, '      *) npass=$((npass + 1)) ;;\n'),
]


def equivalents(text, ops):
    """Four frozen semantics-preserving rewrites of the tally block."""
    out = []
    m = LOOP_RE.search(text)
    rev_ops = ' '.join(reversed(ops))
    e1 = text[:m.start('ops')] + rev_ops + text[m.end('ops'):]
    out.append(('E1-reorder-operands', e1))
    out.append(('E2-arith-commuted', [(ARM0, '      0) npass=$((1 + npass)) ;;\n'),
                                      (ARM1, '      1) nfail=$((1 + nfail)) ;;\n'),
                                      (ARMS, '      *) nsetup=$((1 + nsetup)) ;;\n')]))
    out.append(('E3-comment-in-block', [(BLOCK_START, BLOCK_START + '  # tally: one status per leg (equivalent rewrite E3)\n')]))
    out.append(('E4-noop-before-pass', [(PASSLINE, '  : equivalent-rewrite-E4\n' + PASSLINE)]))
    return out


SETUPCHK = '  if [[ $nsetup -gt 0 ]]; then\n'
VARS = {'0': 'npass', '1': 'nfail', '*': 'nsetup'}
ARMLINES = {'0': ARM0, '1': ARM1, '*': ARMS}


def spell(rng, var, k):
    sp = lambda: ' ' * rng.randint(0, 2)
    forms = ['%s=$((%s%s%s+%s%d%s))' % (var, sp(), var, sp(), sp(), k, sp()),
             '%s=$((%s%d%s+%s%s%s))' % (var, sp(), k, sp(), sp(), var, sp()),
             '((%s += %d)) || :' % (var, k),
             ': $((%s += %d))' % (var, k)]
    return rng.choice(forms)


def arm_line(arm, stmt):
    return '      %s) %s ;;\n' % (arm, stmt)


def heldout(text, ops, seed):
    """Frozen generator: 12 held-out mutants and 4 held-out equivalent rewrites."""
    import random
    rng = random.Random(seed)
    m = LOOP_RE.search(text)

    def with_loop(t, new_ops):
        mm = LOOP_RE.search(t)
        return t[:mm.start('ops')] + ' '.join(new_ops) + t[mm.end('ops'):]

    def respell(t, wrong=None):
        # rewrite all three arms with random equivalent spellings; `wrong` = (arm, var, k) overrides one arm
        for arm in ('0', '1', '*'):
            var, k = VARS[arm], 1
            if wrong and wrong[0] == arm:
                var, k = wrong[1], wrong[2]
            t = replace_once(t, ARMLINES[arm], arm_line(arm, spell(rng, var, k)), 'heldout arm ' + arm)
        return t

    def shuffled(o):
        o = list(o)
        rng.shuffle(o)
        return o

    muts = []
    classes = ['drop', 'drop', 'drop', 'drop', 'arm-noop', 'arm-double', 'fail-as-pass', 'setup-as-pass',
               'fail-as-setup', 'fail-thresh', 'setup-thresh', 'drop']
    for idx, c in enumerate(classes):
        t = text
        if c == 'drop':
            i = rng.randrange(9)
            t = with_loop(t, shuffled(ops[:i] + ops[i + 1:]))
            t = respell(t)
        elif c == 'arm-noop':
            t = respell(with_loop(t, shuffled(ops)), wrong=('0', 'npass', 0))
        elif c == 'arm-double':
            t = respell(with_loop(t, shuffled(ops)), wrong=('0', 'npass', 2))
        elif c == 'fail-as-pass':
            t = respell(with_loop(t, shuffled(ops)), wrong=('1', 'npass', 1))
        elif c == 'setup-as-pass':
            t = respell(with_loop(t, shuffled(ops)), wrong=('*', 'npass', 1))
        elif c == 'fail-as-setup':
            t = respell(with_loop(t, shuffled(ops)), wrong=('1', 'nsetup', 1))
        elif c == 'fail-thresh':
            t = respell(with_loop(t, shuffled(ops)))
            t = replace_once(t, FAILCHK, rng.choice(['  if [[ $nfail -gt 1 ]]; then\n',
                                                      '  if [[ $nfail -ge 2 ]]; then\n',
                                                      '  if (( nfail > 1 )); then\n']), 'heldout fail-thresh')
        elif c == 'setup-thresh':
            t = respell(with_loop(t, shuffled(ops)))
            t = replace_once(t, SETUPCHK, rng.choice(['  if [[ $nsetup -gt 1 ]]; then\n',
                                                       '  if [[ $nsetup -ge 2 ]]; then\n',
                                                       '  if (( nsetup > 1 )); then\n']), 'heldout setup-thresh')
        muts.append(('H%02d-%s' % (idx + 1, c), t))
    eqs = []
    for idx in range(4):
        t = respell(with_loop(text, shuffled(ops)))
        if rng.random() < 0.5:
            t = replace_once(t, FAILCHK, rng.choice(['  if [[ $nfail -ge 1 ]]; then\n',
                                                     '  if (( nfail > 0 )); then\n']), 'heldout eq fail')
        if rng.random() < 0.5:
            t = replace_once(t, SETUPCHK, rng.choice(['  if [[ $nsetup -ge 1 ]]; then\n',
                                                      '  if (( nsetup > 0 )); then\n']), 'heldout eq setup')
        eqs.append(('HE%d-equiv' % (idx + 1), t))
    return muts, eqs


LOOP_TAIL = '    esac\n  done\n'


def inserted(text, seed):
    """Frozen generator: 8 inserted-term mutants and 4 inserted-term equivalent rewrites."""
    import random
    rng = random.Random(seed)
    i = text.find(BLOCK_START)
    j = text.find(LOOP_TAIL, i)
    if i < 0 or j < 0:
        raise CounterError('inserted(): loop tail not found in the tally block')
    sp = lambda: ' ' * rng.randint(0, 2)

    def term(v):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        c = a * b - v
        forms = ['(%s%d*%d%s-%s%d%s)' % (sp(), a, b, sp(), sp(), c, sp()),
                 '(%s%d%s-%s%d*%d%s)*-1' % (sp(), c, sp(), sp(), a, b, sp()),
                 '(%s%d*%d%s+%s%d%s-%s%d%s)' % (sp(), b, a, sp(), sp(), -c, sp(), sp(), 0, sp())]
        return rng.choice(forms)

    def stmt(var, v, indent):
        t = term(v)
        return indent + rng.choice(['%s=$((%s + %s))' % (var, var, t),
                                    '%s=$((%s + %s))' % (var, t, var),
                                    ': $((%s += %s))' % (var, t),
                                    '((%s += %s)) || :' % (var, t)]) + '\n'

    def place(var, v):
        if rng.random() < 0.5:  # after the loop
            k = j + len(LOOP_TAIL)
            return text[:k] + stmt(var, v, '  ') + text[k:]
        k = j + len('    esac\n')  # inside the loop body, after the case
        return text[:k] + stmt(var, v, '    ') + text[k:]

    muts = []
    for idx in range(8):
        var = rng.choice(['npass', 'nfail', 'nsetup'])
        v = rng.choice([-1, 1, 2])
        muts.append(('I%02d-%s%+d' % (idx + 1, var, v), place(var, v)))
    eqs = [('IE%d-%s+0' % (idx + 1, var), place(var, 0))
           for idx, var in enumerate(rng.choice(['npass', 'nfail', 'nsetup']) for _ in range(4))]
    return muts, eqs


class CounterError(Exception):
    pass


SEALED_SHA256 = '44116804c5cf990a5dec58d107a8a584b333e3dc89a8962a3d17761e11243729'
SEALED_N = (6, 6)


def sealed_items(path, text):
    """Return (block_match, mutants, equivs); each list holds (name, full runner text)."""
    raw = open(path, 'rb').read()
    if hashlib.sha256(raw).hexdigest() != SEALED_SHA256:
        raise CounterError('sealed file sha256 does not equal SEALED_SHA256')
    doc = json.loads(raw)
    block = tally_block(text)
    if hashlib.sha256(block.encode()).hexdigest() != doc['block_sha256']:
        return 0, [], []
    muts, eqs = [], []
    for it in doc['items']:
        if block.count(it['old']) != 1:
            raise CounterError('sealed item %s: old text found %d times' % (it['name'], block.count(it['old'])))
        t = text.replace(block, block.replace(it['old'], it['new'], 1), 1)
        (muts if it['kind'] == 'mutant' else eqs).append(('S-' + it['name'], t))
    if (len(muts), len(eqs)) != SEALED_N:
        raise CounterError('sealed set holds %d mutants and %d rewrites' % (len(muts), len(eqs)))
    return 1, muts, eqs


def replace_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise CounterError('%s: site found %d times (need exactly 1)' % (what, n))
    return text.replace(old, new, 1)


def apply(text, edits, what):
    if isinstance(edits, str):
        return edits
    for old, new in edits:
        text = replace_once(text, old, new, what)
    return text


def tally_block(text):
    i = text.find(BLOCK_START)
    if i < 0 or text.count(BLOCK_START) != 1:
        raise CounterError('tally block start not found exactly once')
    j = text.find('\n}\n', i)
    if j < 0:
        raise CounterError('tally block end not found')
    return text[i:j + 1]


def harness(text, ops, statuses, tmp):
    names = [o.strip('"').lstrip('$') for o in ops]
    block = tally_block(text)
    decl = ' '.join('%s=%s' % (n, s) for n, s in zip(names, statuses))
    src = ('#!/usr/bin/env bash\nset -u -o pipefail\nfixed() {\n  local %s\n'
           '  local root=c1-harness auto=0 KEEP=1\n%s}\nfixed\n') % (decl, block)
    fd, path = tempfile.mkstemp(suffix='.sh', dir=tmp)
    with os.fdopen(fd, 'w') as f:
        f.write(src)
    p = subprocess.run(['bash', path], capture_output=True, text=True, timeout=20)
    return p.returncode, p.stdout


BWRAP = ['bwrap', '--unshare-all', '--die-with-parent', '--new-session', '--clearenv',
         '--ro-bind', '/usr', '/usr', '--symlink', 'usr/bin', '/bin', '--symlink', 'usr/lib', '/lib',
         '--symlink', 'usr/lib', '/lib64', '--symlink', 'usr/bin', '/sbin', '--ro-bind', '/etc', '/etc',
         '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
         '--setenv', 'PATH', '/usr/bin', '--setenv', 'HOME', '/w', '--setenv', 'LANG', 'C.UTF-8',
         '--setenv', 'TMPDIR', '/tmp']


def selftest(text, tree, name):
    d = tempfile.mkdtemp(prefix='w', dir=os.path.dirname(tree))
    shutil.copytree(os.path.join(tree, 'tools'), os.path.join(d, 'tools'), symlinks=True)
    with open(os.path.join(d, RUNNER), 'w') as f:
        f.write(text)
    try:
        p = subprocess.run(BWRAP + ['--bind', d, '/w', '--chdir', '/w', 'bash', RUNNER, '--selftest'],
                           capture_output=True, text=True, timeout=300, start_new_session=True)
        rc, out = p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        rc, out = 124, ''
    shutil.rmtree(d, ignore_errors=True)
    return rc, ('VERDICT: PASS' in out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--sealed', required=True)
    a = ap.parse_args()
    env = dict(os.environ)
    for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        env.pop(k, None)
    env['GIT_OPTIONAL_LOCKS'] = '0'
    r = subprocess.run(['git', '-C', a.repo, 'rev-parse', '--verify', a.rev + '^{commit}'],
                       capture_output=True, text=True, env=env)
    if r.returncode:
        print('C1_R30: counter error: cannot resolve rev', file=sys.stderr)
        print('PREDICATE: C1_R30_PASS=false')
        return 2
    rev = r.stdout.strip()
    tmp = tempfile.mkdtemp(prefix='tameshi-r30-c1-')
    try:
        tree = os.path.join(tmp, 'tree')
        os.makedirs(tree)
        ar = subprocess.Popen(['git', '-C', a.repo, 'archive', rev, 'tools'], stdout=subprocess.PIPE, env=env)
        subprocess.run(['tar', '-x', '-C', tree], stdin=ar.stdout, check=True)
        if ar.wait():
            raise CounterError('git archive failed')
        with open(os.path.join(tree, RUNNER)) as f:
            text = f.read()
        m = list(LOOP_RE.finditer(text))
        if len(m) != 1:
            raise CounterError('tally loop line found %d times (need exactly 1)' % len(m))
        ops = m[0].group('ops').split()
        # (b) pristine harness, 19 vectors
        vecs = [([0] * 9, 0, 'REGRESSION: PASS')]
        for i in range(9):
            for s, ex, word in ((1, 1, 'REGRESSION: FAIL'), (2, 2, 'REGRESSION: SETUP')):
                v = [0] * 9
                v[i] = s
                vecs.append((v, ex, word))
        harness_ok = 0
        for v, ex, word in vecs:
            rc, out = harness(text, ops, v, tmp)
            harness_ok += int(rc == ex and word in out)
        # (c) drop mutants refused at run time
        drops = []
        for i in range(9):
            keep = ops[:i] + ops[i + 1:]
            mt = text[:m[0].start('ops')] + ' '.join(keep) + text[m[0].end('ops'):]
            drops.append(('D%d-drop-%s' % (i + 1, ops[i].strip('"$')), mt, i))
        refused = 0
        for name, mt, i in drops:
            names_all = ops
            ok = True
            for v in ([0] * 9, [1 if k == i else 0 for k in range(9)]):
                rc, out = harness(mt, names_all, v, tmp)
                if rc == 0 or 'REGRESSION: PASS' in out:
                    ok = False
            refused += int(ok)
        family = [(n, mt) for n, mt, _ in drops]
        for name, old, new in ARM_MUTANTS:
            family.append((name, replace_once(text, old, new, name)))
        eqs = [(n, apply(text, e, n)) for n, e in equivalents(text, ops)]
        hmuts, heqs = heldout(text, ops, int(rev, 16))
        imuts, ieqs = inserted(text, int(rev, 16) + 1)
        smatch, smuts, seqs = sealed_items(a.sealed, text)
        # generator sanity: each held-out mutant differs from the pristine block on >= 1 of the
        # 19 harness vectors (exit or stdout); each held-out rewrite matches it on all 19
        base_obs = [harness(text, ops, v, tmp) for v, _, _ in vecs]
        for n, t in hmuts + imuts + smuts:
            if all(harness(t, ops, v, tmp) == b for (v, _, _), b in zip(vecs, base_obs)):
                raise CounterError('held-out mutant %s is harness-equivalent to pristine' % n)
        for n, t in heqs + ieqs + seqs:
            if any(harness(t, ops, v, tmp) != b for (v, _, _), b in zip(vecs, base_obs)):
                raise CounterError('held-out rewrite %s differs from pristine under the harness' % n)
        jobs = [('pristine', text)] + family + eqs + hmuts + heqs + imuts + ieqs + smuts + seqs
        with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            res = dict(zip([n for n, _ in jobs], ex.map(lambda j: selftest(j[1], tree, j[0]), jobs)))
        pristine_ok = res['pristine'][0] == 0 and res['pristine'][1]
        killed = sum(1 for n, _ in family if res[n][0] != 0)
        equiv = sum(1 for n, _ in eqs if res[n][0] == 0 and res[n][1])
        for n, _ in jobs:
            print('C1_R30_ROW: %s selftest_exit=%d verdict_pass=%d' % (n, res[n][0], int(res[n][1])))
        hkilled = sum(1 for n, _ in hmuts if res[n][0] != 0)
        hequiv = sum(1 for n, _ in heqs if res[n][0] == 0 and res[n][1])
        ikilled = sum(1 for n, _ in imuts if res[n][0] != 0)
        iequiv = sum(1 for n, _ in ieqs if res[n][0] == 0 and res[n][1])
        skilled = sum(1 for n, _ in smuts if res[n][0] != 0)
        sequiv = sum(1 for n, _ in seqs if res[n][0] == 0 and res[n][1])
        ok = (pristine_ok and harness_ok == 19 and refused == 9 and killed == 13 and equiv == 4
              and hkilled == 12 and hequiv == 4 and ikilled == 8 and iequiv == 4
              and smatch == 1 and skilled == 6 and sequiv == 6)
        print('C1_R30: rev=%s pristine_selftest=%d harness=%d/19 refused_drops=%d/9 killed=%d/13 equiv_pass=%d/4'
              ' heldout_killed=%d/12 heldout_equiv=%d/4 insert_killed=%d/8 insert_equiv=%d/4'
              ' sealed_block_match=%d sealed_killed=%d/6 sealed_equiv=%d/6'
              % (rev, int(pristine_ok), harness_ok, refused, killed, equiv, hkilled, hequiv, ikilled, iequiv,
                 smatch, skilled, sequiv))
        print('PREDICATE: C1_R30_PASS=%s' % ('true' if ok else 'false'))
        return 0 if ok else 1
    except CounterError as e:
        print('C1_R30: counter error: %s' % e)
        print('PREDICATE: C1_R30_PASS=false')
        return 2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
