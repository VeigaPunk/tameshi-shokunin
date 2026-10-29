#!/usr/bin/env python3
"""Mutation harness for the round-57 C1 counter (seat T57W2MutC1Counter).

For each mutant: copy the pristine counter into a fresh scratch dir, apply exactly one
single-edit substitution (asserting the old string occurs exactly once), run the bounded
behavioural detector `--selftest` on pristine and mutated bytes, and record the outcome.

Verdict rules:
  baseline ok  + mutant selftest fails  -> KILLED
  baseline ok  + mutant selftest passes -> SURVIVED (coverage finding)
  baseline fails                        -> INCONCLUSIVE for every mutant
The pristine source file is never modified: only copies are mutated.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELFTEST_LINE = re.compile(r'C1_R57_SELFTEST: (\d+)/(\d+) pass')
CASE_LINE = re.compile(r'^SELFTEST\s+(.+?)\s+(ok|FAIL)\s*$', re.M)


def sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_selftest(counter, work):
    env = dict(os.environ)
    env['TMPDIR'] = work
    env['GIT_CONFIG_GLOBAL'] = os.path.join(work, 'gitconfig')
    env['GIT_CONFIG_NOSYSTEM'] = '1'
    env['HOME'] = work
    proc = subprocess.run([sys.executable, counter, '--selftest', '--work', work],
                          capture_output=True, env=env, text=True)
    out = proc.stdout
    m = SELFTEST_LINE.search(out)
    passed, total = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    failed = [mm.group(1).strip() for mm in CASE_LINE.finditer(out) if mm.group(2) == 'FAIL']
    return {'rc': proc.returncode, 'passed': passed, 'total': total, 'failed': failed,
            'stdout': out,
            'stdout_tail': out.strip().splitlines()[-1] if out.strip() else '',
            'stderr_tail': proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ''}


def apply_edit(text, old, new, mutant_id):
    n = text.count(old)
    if n != 1:
        raise SystemExit('mutant %s: old string occurs %d times (must be exactly 1): %r'
                         % (mutant_id, n, old[:80]))
    return text.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--mutants', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--outdir', required=True)
    a = ap.parse_args()

    os.makedirs(a.scratch, exist_ok=True)
    outdir = a.outdir
    os.makedirs(outdir, exist_ok=True)
    src_text = open(a.source, 'r', encoding='utf-8').read()
    src_sha = sha256(a.source)
    mutants = json.load(open(a.mutants, 'r', encoding='utf-8'))

    base_work = tempfile.mkdtemp(prefix='base-', dir=a.scratch)
    base_copy = os.path.join(base_work, 'measure.py')
    shutil.copy2(a.source, base_copy)
    base = run_selftest(base_copy, base_work)
    base['sha256'] = sha256(base_copy)
    with open(os.path.join(outdir, 'BASELINE.stdout'), 'w', encoding='utf-8') as fh:
        fh.write(base['stdout'])
    print('BASELINE rc=%s selftest=%s/%s' % (base['rc'], base['passed'], base['total']))
    for f in base['failed']:
        print('  BASE FAIL: %s' % f)

    results = []
    for m in mutants:
        mid = m['id']
        work = tempfile.mkdtemp(prefix='mut-%s-' % mid, dir=a.scratch)
        try:
            counter = os.path.join(work, 'measure.py')
            shutil.copy2(a.source, counter)
            new_text = apply_edit(src_text, m['old'], m['new'], mid)
            with open(counter, 'w', encoding='utf-8') as fh:
                fh.write(new_text)
            mut_sha = sha256(counter)
            res = run_selftest(counter, work)
            with open(os.path.join(outdir, mid + '.stdout'), 'w', encoding='utf-8') as fh:
                fh.write(res['stdout'])
            if base['rc'] != 0:
                verdict = 'INCONCLUSIVE'
                killed_by = []
            elif res['rc'] != 0:
                verdict = 'KILLED'
                killed_by = res['failed']
            else:
                verdict = 'SURVIVED'
                killed_by = []
            entry = {'id': mid, 'old': m['old'], 'new': m['new'], 'verdict': verdict,
                     'killed_by': killed_by, 'note': m.get('note', ''),
                     'baseline_selftest': '%s/%s' % (base['passed'], base['total']),
                     'mutant_selftest': '%s/%s' % (res['passed'], res['total']),
                     'mutant_rc': res['rc'],
                     'mutant_sha256': mut_sha, 'pristine_sha256': src_sha,
                     'stdout_tail': res['stdout_tail'], 'stderr_tail': res['stderr_tail'],
                     'stdout_path': outdir + '/' + mid + '.stdout'}
            results.append(entry)
            print('%-28s %-12s mutant=%s failed=%s' % (mid, verdict, entry['mutant_selftest'],
                                                       '; '.join(killed_by)[:120]))
        finally:
            shutil.rmtree(work, ignore_errors=True)

    shutil.rmtree(base_work, ignore_errors=True)
    after_sha = sha256(a.source)
    summary = {'source': a.source, 'pristine_sha256_before': src_sha, 'pristine_sha256_after': after_sha,
               'pristine_restored': src_sha == after_sha,
               'baseline': {'rc': base['rc'], 'selftest': '%s/%s' % (base['passed'], base['total']),
                            'failed': base['failed']},
               'results': results}
    with open(a.out, 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2)
    print('wrote %s (pristine unchanged: %s)' % (a.out, src_sha == after_sha))


if __name__ == '__main__':
    main()
