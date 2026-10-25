#!/usr/bin/env python3
"""Round-46 C2 (operability) counter: do the round-45 counters' selftests kill their declared survivors?

Frozen predicate (the same sentence in the contract, here and in the receipt label):
  C2_R46_PASS=true iff self_pin=1 and, over the declared mutants of mutants.json at REV
  (15 on the freshness counter, 10 on the coverage counter), killed >= 23, neutral_killed = 0,
  both pristine selftests pass (exit 0 and `VERDICT: PASS`), and, for the hardened targets,
  the equivalence check holds: the hardened and the round-45 counter print the same
  fields (self_pin and the PASS token masked) at the round-45 data revision.
A mutant is applied as a single exact old->new text replacement (`old` must occur exactly
once in the target, else the mutant is `inapplicable` and counts as not killed) and is
`killed` iff `python3 <mutated copy> --selftest` exits nonzero or prints no `VERDICT: PASS`
within the timeout. `neutral` mutants are behaviour-preserving edits and must survive: a
selftest that kills them pins its own bytes and is not testing a rule.

Modes:
  --lane L --rev R --targets hardened   deciding run (targets read from REV)
  --lane L --rev R --targets orig       the do-nothing baseline: the round-45 counters as committed
  --selftest
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
SELF_PATH = '.ufo/evidence/round-46/hardening/mutate.py'
MANIFEST = '.ufo/evidence/round-46/hardening/mutants.json'
HARDENED = {
    'freshness': '.ufo/evidence/round-46/hardening/freshness-counter.py',
    'coverage': '.ufo/evidence/round-46/hardening/coverage-counter.py',
}
DATA_REV = 'ea25e0224fc81060414b27301c27bd1344669165'
MIN_KILLED = 23
TIMEOUT = 300
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV['PYTHONDONTWRITEBYTECODE'] = '1'


def git_show(lane, rev, path):
    out = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return out.stdout if out.returncode == 0 else None


def run_selftest(source, name='measure.py'):
    with tempfile.TemporaryDirectory(prefix='tameshi-r46-mut-') as d:
        path = os.path.join(d, name)
        with open(path, 'wb') as fh:
            fh.write(source)
        try:
            p = subprocess.run([sys.executable, path, '--selftest'], capture_output=True, text=True,
                               timeout=TIMEOUT, cwd=d, env=ENV)
        except subprocess.TimeoutExpired:
            return 'timeout', 'timeout'
        tail = (p.stdout.strip().splitlines() or [''])[-1]
        ok = p.returncode == 0 and 'VERDICT: PASS' in p.stdout
        return ('pass' if ok else 'fail'), tail


def apply(source_text, mutant):
    old, new = mutant['old'], mutant['new']
    if old is None:
        return source_text + new
    if source_text.count(old) != 1:
        return None
    return source_text.replace(old, new)


def judge(source, mutant):
    text = source.decode('utf-8')
    mutated = apply(text, mutant)
    if mutated is None:
        return mutant['id'], 'inapplicable', 'old text occurs %d times' % text.count(mutant['old'])
    state, tail = run_selftest(mutated.encode('utf-8'))
    return mutant['id'], ('survived' if state == 'pass' else 'killed'), tail


def mask(text):
    out = []
    for line in text.splitlines():
        out.append(' '.join(t for t in line.split() if not t.startswith('self_pin=') and '_PASS=' not in t))
    return out


def equivalence(lane, group, orig_src, hard_src):
    lines = []
    for src in (orig_src, hard_src):
        with tempfile.TemporaryDirectory(prefix='tameshi-r46-eq-') as d:
            path = os.path.join(d, 'measure.py')
            with open(path, 'wb') as fh:
                fh.write(src)
            p = subprocess.run([sys.executable, path, '--lane', lane, '--rev', DATA_REV],
                               capture_output=True, text=True, timeout=TIMEOUT, cwd=d, env=ENV)
            lines.append(mask(p.stdout))
            if src is orig_src and '_PASS=true' not in p.stdout:
                return 0  # the round-45 counter must itself pass over its own data revision, else the comparison is vacuous
    return int(bool(lines[0]) and lines[0] == lines[1])


def measure(lane, rev, targets):
    me = open(os.path.abspath(__file__), 'rb').read()
    blob = git_show(lane, rev, SELF_PATH)
    self_pin = int(blob is not None and hashlib.sha256(blob).digest() == hashlib.sha256(me).digest())
    manifest_raw = git_show(lane, rev, MANIFEST)
    if manifest_raw is None:
        print('C2_R46: refused: manifest absent at %s' % rev)
        return 2
    manifest = json.loads(manifest_raw)
    killed = survived = inapplicable = neutral_killed = declared = 0
    pristine_ok = equiv_ok = 1
    summary = []
    for group, spec in manifest['groups'].items():
        path = spec['orig'] if targets == 'orig' else HARDENED[group]
        source = git_show(lane, rev, path)
        if source is None:
            print('C2_R46: group %s target absent at %s: %s' % (group, rev, path))
            pristine_ok = 0
            continue
        state, tail = run_selftest(source)
        print('PRISTINE %s %s %s' % (group, state, tail))
        pristine_ok &= int(state == 'pass')
        if targets == 'hardened':
            orig = git_show(lane, rev, spec['orig'])
            eq = equivalence(lane, group, orig, source) if orig is not None else 0
            print('EQUIVALENCE %s %d' % (group, eq))
            equiv_ok &= eq
        if state != 'pass':
            continue
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            futs = [pool.submit(judge, source, m) for m in spec['mutants']]
            results = [f.result() for f in futs]
        kinds = {m['id']: m['kind'] for m in spec['mutants']}
        for mid, verdict, tail in results:
            print('MUTANT %s %s %s %s' % (group, mid, kinds[mid], verdict))
            if kinds[mid] == 'neutral':
                neutral_killed += verdict == 'killed'
                continue
            declared += 1
            if verdict == 'killed':
                killed += 1
            elif verdict == 'inapplicable':
                inapplicable += 1
                survived += 1
            else:
                survived += 1
                summary.append('%s:%s' % (group, mid))
    passed = (self_pin == 1 and pristine_ok == 1 and equiv_ok == 1 and neutral_killed == 0
              and killed >= MIN_KILLED)
    if survived:
        print('SURVIVORS ' + ' '.join(summary))
    print('C2_R46: self_pin=%d targets=%s declared=%d killed=%d survived=%d inapplicable=%d neutral_killed=%d '
          'pristine=%d equivalence=%d rev=%s C2_R46_PASS=%s' % (
              self_pin, targets, declared, killed, survived, inapplicable, neutral_killed, pristine_ok,
              equiv_ok if targets == 'hardened' else -1, rev, 'true' if passed else 'false'))
    return 0 if passed else 1


TOY = '''import sys
def check(a, b):
    return a + b == 5
if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        bad = 0
        bad += not check(2, 3)
        bad += check(2, 2)
        print('VERDICT: %s' % ('PASS' if not bad else 'FAIL'))
        sys.exit(1 if bad else 0)
'''


def selftest():
    toy = TOY.encode()
    cases = []
    mutants = [
        dict(id='K', kind='mutant', old='a + b == 5', new='a + b >= 5', what='weaken'),
        dict(id='S', kind='mutant', old='check(2, 2)', new='check(2, 2) and False', what='dead'),
        dict(id='I', kind='mutant', old='no such text', new='x', what='missing'),
        dict(id='N', kind='neutral', old=None, new='\n# comment\n', what='comment'),
    ]
    got = {m['id']: judge(toy, m)[1] for m in mutants}
    # `>= 5` on (2, 3) and (2, 2) behaves like `== 5` (4 >= 5 is false), so the toy selftest cannot tell
    cases.append(('T1_weakening_that_changes_nothing_survives', got['K'] == 'survived'))
    cases.append(('T2_missing_old_is_inapplicable', got['I'] == 'inapplicable'))
    cases.append(('T3_neutral_survives', got['N'] == 'survived'))
    flip = dict(id='F', kind='mutant', old='return a + b == 5', new='return a + b != 5', what='flip')
    cases.append(('T4_flipped_rule_killed', judge(toy, flip)[1] == 'killed'))
    st, _ = run_selftest(toy)
    cases.append(('T5_pristine_passes', st == 'pass'))
    st, _ = run_selftest(toy.replace(b'check(2, 3)', b'check(2, 4)'))
    cases.append(('T6_failing_pristine_refused', st == 'fail'))
    cases.append(('T7_apply_counts_exactly_once', apply(TOY, dict(old='check(', new='c(')) is None))
    cases.append(('T8_mask_drops_pin_and_pass_tokens',
                  mask('C1: self_pin=1 fresh=3 C1_R45_PASS=true') == ['C1: fresh=3']))
    failed = 0
    for name, ok in cases:
        failed += not ok
        print('%s %s' % ('PASS' if ok else 'FAIL', name))
    print('C2_R46_SELFTEST: cases=%d failed=%d' % (len(cases), failed))
    print('VERDICT: %s' % ('PASS' if failed == 0 else 'FAIL'))
    return 0 if failed == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane')
    ap.add_argument('--rev')
    ap.add_argument('--targets', choices=('hardened', 'orig'), default='hardened')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.lane or not a.rev:
        ap.error('--lane and --rev are required')
    return measure(a.lane, a.rev, a.targets)


if __name__ == '__main__':
    sys.exit(main())
