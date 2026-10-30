#!/usr/bin/env python3
"""Build and run single-edit mutants of the round-57 C1 counter (amendment 2) against its selftest.

Detector: `python3 <mutant> --selftest --work <dir>`; the signal is the set of failing SELFTEST
case names plus the exit code plus the C1_R57_SELFTEST n/n summary line.

Differential rule (the pristine baseline is NOT clean, so an absolute pass/fail is not usable):
  KILLED     mutant's failing-case set is a strict superset of the pristine one, OR the mutant
             crashes (no summary line / exit 2), OR the exit code differs from pristine.
  SURVIVED   mutant's failing-case set equals the pristine one and the exit code is identical.
  INCONCLUSIVE  mutant's failing-case set is a strict subset (the mutation hides baseline failures).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

import repair as repair_mod

BASE = sys.argv[1]
OUT = sys.argv[2]
WORK = sys.argv[3]
USE_REPAIR = os.environ.get('REPAIR', '1') == '1'

PANEL_TIE = "        panel_tie = len(pc) >= 7 and commit.startswith(pc[:40])"
PROV_OK = ("        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat) "
           "and seat in listed")
PROV_LOOP = ("    for d in defects:\n"
             "        det = panel.get('detail', {}).get(d['id'])\n"
             "        seat = det.get('seat') if isinstance(det, dict) else None\n")

MUTANTS = [
    ('M01', 'npath normpath removed',
     "    return posixpath.normpath(p) if isinstance(p, str) and p else p",
     "    return p"),
    ('M02a', 'panel_tie prefix test startswith(pc[:40]) -> always true',
     PANEL_TIE,
     "        panel_tie = len(pc) >= 7 and True"),
    ('M02b', 'panel_tie len(pc) >= 7 dropped',
     PANEL_TIE,
     "        panel_tie = commit.startswith(pc[:40])"),
    ('M03', 'pcommits restricted to fixed verdicts dropped',
     "            pcommits = {k: (v.get('commit') or '') for k, v in panel.get('detail', {}).items()\n"
     "                        if isinstance(v, dict) and panel.get('verdicts', {}).get(k) == 'fixed'}",
     "            pcommits = {k: (v.get('commit') or '') for k, v in panel.get('detail', {}).items()\n"
     "                        if isinstance(v, dict)}"),
    ('M04', 'provenance sha check removed',
     PROV_OK,
     "        ok = blob is not None and seat in listed"),
    ('M05', 'provenance verdict-equality removed',
     "            ok = v == panel.get('verdicts', {}).get(d['id'])",
     "            ok = True"),
    ('M06', "provenance 'listed' check removed",
     PROV_OK,
     "        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat)"),
    ('M07', 'provenance w3 path routing removed',
     "        wv = 'w3' if isinstance(seat, str) and seat.startswith('T57W3') else 'w2'",
     "        wv = 'w2'"),
    ('M08', 'panel_prov not added to TERMS',
     "         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad', "
     "'panel_prov')",
     "         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad')"),
    ('M09', 'panel_prov count not assigned',
     "            counts['panel_prov'] = panel_provenance(lane, rev, defects, panel, note)",
     "            counts['panel_prov'] = 0"),
    ('M10', 'provenance loop skipping ids',
     PROV_LOOP,
     "    for d in defects:\n"
     "        if panel.get('verdicts', {}).get(d['id']) == 'declined':\n"
     "            continue\n"
     "        det = panel.get('detail', {}).get(d['id'])\n"
     "        seat = det.get('seat') if isinstance(det, dict) else None\n"),
]

FAIL_RE = re.compile(r'^SELFTEST (.+?)\s+(ok|FAIL)$')
SUM_RE = re.compile(r'C1_R57_SELFTEST: (\d+)/(\d+) pass')
LAST_RE = re.compile(r"last run: (\{.*?\}) notes=(\[.*\])")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run_selftest(path, work):
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, TMPDIR=work)
    proc = subprocess.run([sys.executable, path, '--selftest', '--work', work],
                          capture_output=True, env=env, cwd=work)
    out = proc.stdout.decode('utf-8', 'replace')
    err = proc.stderr.decode('utf-8', 'replace')
    fails = []
    for line in out.split('\n'):
        m = FAIL_RE.match(line)
        if m and m.group(2) == 'FAIL':
            fails.append(m.group(1).strip())
    m = SUM_RE.search(out)
    summary = m.group(0) if m else None
    last = None
    m = LAST_RE.search(out)
    if m:
        last = m.group(0)
    return {'rc': proc.returncode, 'fails': fails, 'summary': summary, 'last': last,
            'stdout': out, 'stderr': err}


def main():
    base_bytes = open(BASE, 'rb').read()
    base_sha = sha(base_bytes)
    base_text = base_bytes.decode('utf-8')
    if USE_REPAIR:
        base_text = repair_mod.repair(base_text)
        base_sha = sha(base_text.encode('utf-8'))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)

    pristine = run_selftest(BASE, WORK)
    records = []
    for mid, desc, old, new in MUTANTS:
        n = base_text.count(old)
        if n != 1:
            records.append({'id': mid, 'desc': desc, 'status': 'INCONCLUSIVE',
                            'detail': 'old_string occurrences=%d (expected exactly 1)' % n})
            continue
        mtext = base_text.replace(old, new, 1)
        if USE_REPAIR:
            mtext = repair_mod.repair(mtext)
        mbytes = mtext.encode('utf-8')
        mdir = os.path.join(OUT, mid)
        os.makedirs(mdir, exist_ok=True)
        mpath = os.path.join(mdir, 'measure.py')
        with open(mpath, 'wb') as fh:
            fh.write(mbytes)
        # the base file must be untouched by the mutation
        assert sha(open(BASE, 'rb').read()) == base_sha, 'base mutated!'
        res = run_selftest(mpath, os.path.join(WORK, mid))
        pf, mf = set(pristine['fails']), set(res['fails'])
        new_fails = sorted(mf - pf)
        fixed = sorted(pf - mf)
        crashed = res['summary'] is None
        if crashed or res['rc'] != pristine['rc'] or new_fails:
            verdict = 'KILLED'
        elif fixed:
            verdict = 'INCONCLUSIVE'
        else:
            verdict = 'SURVIVED'
        records.append({
            'id': mid, 'desc': desc, 'status': verdict,
            'mutant_sha256': sha(mbytes), 'old_sha256': sha(old.encode('utf-8')),
            'new_sha256': sha(new.encode('utf-8')),
            'rc': res['rc'], 'pristine_rc': pristine['rc'],
            'summary': res['summary'], 'pristine_summary': pristine['summary'],
            'new_failing_cases': new_fails, 'baseline_failing_cases_fixed': fixed,
            'pristine_fail_count': len(pf), 'mutant_fail_count': len(mf),
            'pristine_fails': sorted(pf), 'mutant_fails': sorted(mf),
            'last_run_line': res['last'], 'stderr_tail': res['stderr'][-600:],
        })
    out = {'base': BASE, 'base_sha256': base_sha, 'pristine': {k: v for k, v in pristine.items()
                                                                if k not in ('stdout',)},
            'records': records}
    with open(os.path.join(OUT, 'mutants.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for r in records:
        print('%s %-10s %s' % (r['id'], r['status'], r['desc']))
        if r['status'] == 'INCONCLUSIVE' and 'detail' in r:
            print('    %s' % r['detail'])
        else:
            print('    rc=%s pristine_rc=%s summary=%s' % (r['rc'], r['pristine_rc'], r['summary']))
            if r['new_failing_cases']:
                print('    new failing: %s' % '; '.join(r['new_failing_cases']))
            if r['baseline_failing_cases_fixed']:
                print('    baseline failures now passing: %s'
                      % '; '.join(r['baseline_failing_cases_fixed']))
            if r.get('last_run_line'):
                print('    %s' % r['last_run_line'][:300])
    return 0


if __name__ == '__main__':
    sys.exit(main())
