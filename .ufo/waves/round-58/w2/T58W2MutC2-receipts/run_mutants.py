#!/usr/bin/env python3
"""T58W2MutC2: mutate the copied round-58 C2 counter at four points (executed
tally, cell fixture, codes parser, verdict total), score each mutant against
its selftest and the installed registry at C0, then restore exact pristine
bytes and re-run the detector on the restored file."""
import difflib
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r58/T58W2MutC2')
CNT = S / 'cnt'
REC = S / 'receipts'
REC.mkdir(exist_ok=True)
TARGET = CNT / 'measure.py'
C0 = '8063d0a551fc5b3cb5a2d397da7353af53444534'
LANE = str(S / 'clone')
PRISTINE = TARGET.read_bytes()
PRISTINE_SHA = hashlib.sha256(PRISTINE).hexdigest()

MUTANTS = [
    dict(id='MUT1', axis='executed tally',
         old="            held += state == 'held'\n",
         new="            held += 1\n",
         expected='selftest case "executed arm: a row expecting the wrong exit does not hold" '
                  'asserts held==2/short executed==1; mutant counts every row as held. '
                  'Installed-registry run at C0 expected to still print PASS (all rows hold).'),
    dict(id='MUT2', axis='cell fixture',
         old="    receipt.write_text('VERDICT: rev=%s C1_X_PASS=true\\n' % rev_a)",
         new="    receipt.write_text('VERDICT: rev=%s C1_X_PASS=true\\n' % rev_b)",
         expected='fixture receipt now names the certified revision, so the gate PASSES '
                  '(exit 0) -> standing_cell=WRONG:fixture -> selftest "good fixture: every '
                  'arm 0" fails and installed-registry run prints total>=1 PASS=false exit 1.'),
    dict(id='MUT3', axis='codes parser',
         old="    known = [t for t in tokens if t in codes]\n",
         new="    known = list(tokens)\n",
         expected='strict membership in the gate CODES dropped (lax counting) -> selftest '
                  'case "codes arm: a token the gate does not define is counted" fails; '
                  'installed-registry run expected to still print PASS (all 4 SKILL tokens '
                  'are gate CODES at C0).'),
    dict(id='MUT4', axis='verdict total',
         old="    res['total'] = sum(short.values())\n",
         new="    res['total'] = 0\n",
         expected='total hard-zeroed -> selftest cases "cell arm: a gate that does not '
                  'refuse" (asserts total>0) and "mutants pin" (asserts main_measure rc!=0) '
                  'fail; installed-registry run at C0 expected to print total=0 PASS=true '
                  '(indistinguishable, because C0 has no real shortfall).'),
]


def run(cmd, out_path):
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, cwd=str(S))
    out = p.stdout.decode('utf-8', 'replace')
    if p.returncode not in (0, 1):
        out += p.stderr.decode('utf-8', 'replace')
    Path(out_path).write_text(out)
    return p.returncode, out, round(time.time() - t0, 1)


def detector(tag):
    """The bounded behavioral detector: --selftest plus the installed-registry measure."""
    rc_st, out_st, t_st = run([sys.executable, str(TARGET), '--selftest',
                               '--lane', LANE, '--rev', C0],
                              REC / (tag + '-selftest.txt'))
    fails = [l for l in out_st.splitlines() if l.startswith('CASE') and 'FAIL' in l]
    tail = [l for l in out_st.splitlines() if l.startswith('C2_R58_SELFTEST')]
    work = S / ('work-' + tag)
    work.mkdir(parents=True, exist_ok=True)
    rc_m, out_m, t_m = run([sys.executable, str(TARGET), '--lane', LANE, '--rev', C0,
                            '--work', str(work), '--explain'],
                           REC / (tag + '-measure.txt'))
    verdict = [l for l in out_m.splitlines() if l.startswith('C2_R58:')]
    shutil.rmtree(work, ignore_errors=True)
    return dict(selftest_exit=rc_st, selftest_seconds=t_st,
                selftest_tail=tail[-1] if tail else 'no-output',
                selftest_failing_cases=fails,
                measure_exit=rc_m, measure_seconds=t_m,
                verdict_line=verdict[-1] if verdict else 'no-output')


results = {'pristine_sha256': PRISTINE_SHA, 'c0': C0, 'lane': LANE}
try:
    for mu in MUTANTS:
        src = PRISTINE.decode('utf-8')
        assert src.count(mu['old']) == 1, (mu['id'], src.count(mu['old']))
        mutated = src.replace(mu['old'], mu['new'])
        TARGET.write_bytes(mutated.encode('utf-8'))
        assert hashlib.sha256(TARGET.read_bytes()).hexdigest() != PRISTINE_SHA
        diff = '\n'.join(difflib.unified_diff(src.splitlines(), mutated.splitlines(),
                                              'pristine', mu['id'], lineterm=''))
        (REC / (mu['id'] + '.diff')).write_text(diff + '\n')
        r = detector(mu['id'])
        killed_by = []
        if r['selftest_exit'] != 0:
            killed_by.append('selftest')
        if r['measure_exit'] != 0:
            killed_by.append('installed-registry-run')
        r.update(id=mu['id'], axis=mu['axis'], old=mu['old'], new=mu['new'],
                 expected=mu['expected'],
                 mutated_sha256=hashlib.sha256(mutated.encode('utf-8')).hexdigest(),
                 killed_by=killed_by,
                 verdict='killed' if killed_by else 'survived')
        results[mu['id']] = r
        print('%s [%s] %s by %s | selftest: %s | measure rc=%d: %s'
              % (mu['id'], mu['axis'], r['verdict'], killed_by or 'NOTHING',
                 r['selftest_tail'], r['measure_exit'], r['verdict_line']), flush=True)
finally:
    TARGET.write_bytes(PRISTINE)
    ok = hashlib.sha256(TARGET.read_bytes()).hexdigest() == PRISTINE_SHA
    results['restoration'] = dict(restored_sha256=PRISTINE_SHA, bytes_identical=ok)
    print('restoration bytes_identical=%s' % ok, flush=True)

r = detector('restored')
results['restored_detector'] = r
print('restored detector: %s | measure rc=%d: %s'
      % (r['selftest_tail'], r['measure_exit'], r['verdict_line']), flush=True)

(REC / 'mutants-score.json').write_text(json.dumps(results, indent=1) + '\n')
print('wrote %s' % (REC / 'mutants-score.json'), flush=True)
