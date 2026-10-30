#!/usr/bin/env python3
"""Final mutation driver for the round-57 C1 counter (amendment 2).

Detectors (both are run on pristine bytes, on every mutant, and on restored bytes):
  D1 the shipped selftest, after a harness repair that makes its panel fixture carry `detail`,
     the seat's wave file and the wave results list (the shipped fixture is red on pristine bytes:
     92/99, because panel_provenance() finds no `detail` and counts a shortfall for every id).
     Signal: the set of failing SELFTEST case names and the exit code.
  D2 an independent behavioural probe (probe.py) that builds its own fixture lane and calls
     measure() of the module under test, printing the observable value of each amendment-2 arm.
     Signal: any difference in the observed values against the pristine run.

Verdict:
  KILLED      a detector shows a difference attributable to the mutation.
  SURVIVED    neither detector shows any difference.
  INCONCLUSIVE the mutant hides baseline failures (a failing case became passing) or the module
              crashes, so no detector signal can be attributed.

Usage: drive.py <base-measure.py> <out-dir> <work-dir>
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repair as repair_mod  # noqa: E402
import probe as probe_mod  # noqa: E402

BASE = sys.argv[1]
OUT = sys.argv[2]
WORK = sys.argv[3]

PANEL_TIE = "        panel_tie = len(pc) >= 7 and commit.startswith(pc[:40])"
PROV_OK = ("        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat) "
           "and seat in listed")
PROV_LOOP = ("    for d in defects:\n"
             "        det = panel.get('detail', {}).get(d['id'])\n"
             "        seat = det.get('seat') if isinstance(det, dict) else None\n")

MUTANTS = [
    ('M01', 'npath: posixpath.normpath removed',
     "    return posixpath.normpath(p) if isinstance(p, str) and p else p",
     "    return p"),
    ('M02a', 'A8 panel_tie: prefix test startswith(pc[:40]) -> always true',
     PANEL_TIE,
     "        panel_tie = len(pc) >= 7 and True"),
    ('M02b', 'A8 panel_tie: len(pc) >= 7 dropped',
     PANEL_TIE,
     "        panel_tie = commit.startswith(pc[:40])"),
    ('M03', 'A8 pcommits: restriction to `fixed` verdicts dropped',
     "            pcommits = {k: (v.get('commit') or '') for k, v in panel.get('detail', {}).items()\n"
     "                        if isinstance(v, dict) and panel.get('verdicts', {}).get(k) == 'fixed'}",
     "            pcommits = {k: (v.get('commit') or '') for k, v in panel.get('detail', {}).items()\n"
     "                        if isinstance(v, dict)}"),
    ('M04', 'A9 provenance: sha check removed',
     PROV_OK,
     "        ok = blob is not None and seat in listed"),
    ('M05', 'A9 provenance: verdict-equality removed',
     "            ok = v == panel.get('verdicts', {}).get(d['id'])",
     "            ok = True"),
    ('M06', "A9 provenance: 'listed' check removed",
     PROV_OK,
     "        ok = blob is not None and hashlib.sha256(blob).hexdigest() == files.get(seat)"),
    ('M07', 'A9 provenance: w3 path routing removed',
     "        wv = 'w3' if isinstance(seat, str) and seat.startswith('T57W3') else 'w2'",
     "        wv = 'w2'"),
    ('M08', 'A9: panel_prov not added to TERMS',
     "         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad', "
     "'panel_prov')",
     "         'declined_over', 'this_round_short', 'panel_pin', 'panel_over', 'base_status_bad')"),
    ('M09', 'A9: panel_prov count not assigned',
     "            counts['panel_prov'] = panel_provenance(lane, rev, defects, panel, note)",
     "            counts['panel_prov'] = 0"),
    ('M10', 'A9 provenance: loop skipping ids',
     PROV_LOOP,
     "    for d in defects:\n"
     "        if panel.get('verdicts', {}).get(d['id']) == 'declined':\n"
     "            continue\n"
     "        det = panel.get('detail', {}).get(d['id'])\n"
     "        seat = det.get('seat') if isinstance(det, dict) else None\n"),
]

import re  # noqa: E402
FAIL_RE = re.compile(r'^SELFTEST (.+?)\s+(ok|FAIL)$')
SUM_RE = re.compile(r'C1_R57_SELFTEST: (\d+)/(\d+) pass')
LAST_RE = re.compile(r"last run: (\{.*?\}) notes=(\[.*\])")


def sha(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def run_selftest(path, work):
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, TMPDIR=work)
    proc = subprocess.run([sys.executable, path, '--selftest', '--work', work],
                          capture_output=True, env=env, cwd=work)
    out = proc.stdout.decode('utf-8', 'replace')
    fails = []
    for line in out.split('\n'):
        m = FAIL_RE.match(line)
        if m and m.group(2) == 'FAIL':
            fails.append(m.group(1).strip())
    m = SUM_RE.search(out)
    last = LAST_RE.search(out)
    return {'rc': proc.returncode, 'fails': fails, 'summary': m.group(0) if m else None,
            'last': last.group(0) if last else None,
            'stderr': proc.stderr.decode('utf-8', 'replace')[-500:]}


def run_probe(path, work):
    os.makedirs(work, exist_ok=True)
    proc = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         'probe.py'), path, work],
                          capture_output=True)
    try:
        return json.loads(proc.stdout.decode('utf-8', 'replace'))
    except ValueError:
        return {'error': 'probe did not emit json: %s / %s'
                         % (proc.stdout.decode('utf-8', 'replace')[-400:],
                            proc.stderr.decode('utf-8', 'replace')[-400:])}


def diff_probe(a, b):
    out = []
    for sc in sorted(set(a) | set(b)):
        va, vb = a.get(sc), b.get(sc)
        if va != vb:
            out.append({'scenario': sc, 'pristine': va, 'mutant': vb})
    return out


def main():
    raw = open(BASE, 'r', encoding='utf-8').read()
    base_sha_raw = sha(raw)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)

    # pristine, repaired harness
    pdir = os.path.join(OUT, 'pristine')
    os.makedirs(pdir, exist_ok=True)
    ppath = os.path.join(pdir, 'measure.py')
    with open(ppath, 'w', encoding='utf-8') as fh:
        fh.write(repair_mod.repair(raw))
    pst = run_selftest(ppath, os.path.join(WORK, 'pristine'))
    pprobe = run_probe(ppath, os.path.join(WORK, 'pristine-probe'))
    print('PRISTINE selftest: rc=%s %s fails=%d' % (pst['rc'], pst['summary'], len(pst['fails'])))
    if pst['fails']:
        print('  pristine failing cases: %s' % '; '.join(pst['fails']))

    records = []
    for mid, desc, old, new in MUTANTS:
        n = raw.count(old)
        if n != 1:
            records.append({'id': mid, 'desc': desc, 'status': 'INCONCLUSIVE',
                            'detail': 'old_string occurrences=%d (expected exactly 1)' % n})
            continue
        mutated_raw = raw.replace(old, new, 1)
        mdir = os.path.join(OUT, mid)
        os.makedirs(mdir, exist_ok=True)
        mpath = os.path.join(mdir, 'measure.py')
        with open(mpath, 'w', encoding='utf-8') as fh:
            fh.write(repair_mod.repair(mutated_raw))
        assert sha(open(BASE, 'rb').read()) == base_sha_raw, 'base file mutated!'
        mst = run_selftest(mpath, os.path.join(WORK, mid))
        mprobe = run_probe(mpath, os.path.join(WORK, mid + '-probe'))
        pf, mf = set(pst['fails']), set(mst['fails'])
        new_fails = sorted(mf - pf)
        hidden = sorted(pf - mf)
        pdiff = diff_probe(pprobe, mprobe)
        crashed = mst['summary'] is None
        detectors = []
        if new_fails or crashed or mst['rc'] != pst['rc']:
            detectors.append('D1-selftest')
        if pdiff:
            detectors.append('D2-probe')
        if new_fails or crashed or mst['rc'] != pst['rc'] or pdiff:
            verdict = 'KILLED'
        elif hidden:
            verdict = 'INCONCLUSIVE'
        else:
            verdict = 'SURVIVED'
        records.append({
            'id': mid, 'desc': desc, 'status': verdict,
            'detectors_fired': detectors,
            'mutant_file': mpath,
            'mutant_sha256': sha(open(mpath, 'rb').read()),
            'mutant_raw_sha256': sha(mutated_raw),
            'pristine_sha256': sha(open(ppath, 'rb').read()),
            'base_sha256': base_sha_raw,
            'old_string_sha256': sha(old), 'new_string_sha256': sha(new),
            'old_string_occurrences_in_base': n,
            'selftest': {'rc': mst['rc'], 'pristine_rc': pst['rc'], 'summary': mst['summary'],
                         'pristine_summary': pst['summary'], 'new_failing_cases': new_fails,
                         'baseline_failing_cases_hidden': hidden, 'last_run_line': mst['last'],
                         'stderr_tail': mst['stderr']},
            'probe_diffs': pdiff,
        })
    out = {'base': BASE, 'base_sha256': base_sha_raw, 'pristine': {'selftest': pst, 'probe': pprobe},
           'records': records}
    with open(os.path.join(OUT, 'matrix.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    for r in records:
        print('%-5s %-13s %s' % (r['id'], r['status'], r['desc']))
        if 'detail' in r:
            print('      %s' % r['detail'])
            continue
        print('      selftest: rc=%s pristine_rc=%s summary=%s' % (r['selftest']['rc'],
              r['selftest']['pristine_rc'], r['selftest']['summary']))
        if r['selftest']['new_failing_cases']:
            print('      new failing cases: %s' % '; '.join(r['selftest']['new_failing_cases']))
        if r['selftest']['baseline_failing_cases_hidden']:
            print('      hidden baseline failures: %s'
                  % '; '.join(r['selftest']['baseline_failing_cases_hidden']))
        for d in r['probe_diffs']:
            print('      probe %s: pristine=%s' % (d['scenario'], json.dumps(d['pristine'], sort_keys=True)))
            print('                 mutant  =%s' % json.dumps(d['mutant'], sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
