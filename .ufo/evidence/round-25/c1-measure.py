#!/usr/bin/env python3
"""Round-25 C1 counter: the three round-23 closure-routed items that round 24
left without a recorded, executed disposition (round-24 verifier spot-check,
`corpus/lessons/round-24-verifier-spotcheck.md:37,63`).

  python3 .ufo/evidence/round-25/c1-measure.py --repo REPO

An item counts only when the lane's own record names it (SCORECARD.md carries
its label) AND its executed check holds on REPO's committed files:

R23-ROUTED-1  multi-token stdout fixture in the ruler — the lane runner
              (tools/mutate-and-run.sh) sweeps multitoken-mutants.spec over
              tools/command-binding.py with the ruler-owned fixtures
              (c1-suite.py multitoken): control green, restore OK, every defect
              KILLED with an explicit `FIXTURE ... FAIL` witness in its log.
R23-ROUTED-2  receipted guard-sweep rerun — same runner, guard-mutants.spec,
              the gate's own selftest (c1-suite.py selftest): control green,
              restore OK, every defect KILLED with a `CASE ... FAIL` witness.
R23-ROUTED-3  dead-falsifier coverage disposition — every round-23 wave-2 seat
              whose original callback status is not `completed`
              (.ufo/waves/round-23/original-outcomes2.json) has exactly one row
              in dead-falsifier-disposition.json; a re-attacked row points at a
              committed report holding `R23-REATTACK <name>: AGREE|FINDING`
              that matches its status; a re-attack seat that died carries its
              error text. Two doctored copies (one row dropped, one status
              flipped) must each fail, or the item does not count.

All work runs in private copies under a temp dir; REPO is never written.
Exit: 0 dispositioned 3/3 · 1 fewer · 2 setup. Not a numeric expertise score.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
R25 = '.ufo/evidence/round-25'
LABELS = {'R1': 'R23-ROUTED-1', 'R2': 'R23-ROUTED-2', 'R3': 'R23-ROUTED-3'}
STAGE = ['tools/command-binding.py', 'tools/mutate-and-run.sh',
         '.ufo/evidence/round-23/extra-cases.json', '.ufo/evidence/round-24/extra-cases.json',
         R25 + '/c1-suite.py', R25 + '/multitoken-cases.json',
         R25 + '/multitoken-mutants.spec', R25 + '/guard-mutants.spec']
STATUSES = {'reattacked-agree': 'AGREE', 'reattacked-finding': 'FINDING', 'reattack-seat-died': None}


def sweep(stage, spec, mode, witness, tmp):
    workdir = Path(tmp) / ('sweep-' + mode)
    suite = 'python3 %s %s "$MUTANT"' % (stage / R25 / 'c1-suite.py', mode)
    run = subprocess.run(['bash', str(stage / 'tools/mutate-and-run.sh'), '--target',
                          str(stage / 'tools/command-binding.py'), '--defects', str(stage / R25 / spec),
                          '--suite', suite, '--workdir', str(workdir), '--label', 'r25-' + mode],
                         capture_output=True, text=True, timeout=1800)
    out = run.stdout
    ids = re.findall(r'^@defect (\S+)', (stage / R25 / spec).read_text(), re.M)
    killed = re.findall(r'^DEFECT (\S+): KILLED', out, re.M)
    witnessed = [i for i in killed
                 if (workdir / 'evidence' / (i + '.out')).is_file()
                 and re.search(witness, (workdir / 'evidence' / (i + '.out')).read_text(), re.M)]
    row = {'runner_exit': run.returncode, 'defects': ids, 'killed': killed, 'witnessed_kills': witnessed,
           'control_green': bool(re.search(r'^CONTROL: GREEN', out, re.M)),
           'restore_ok': bool(re.search(r'^MUTATE_RESTORE: OK', out, re.M)),
           'verdict_line': ([l for l in out.splitlines() if l.startswith('MUTATE: ')] or [None])[-1]}
    row['holds'] = (run.returncode == 0 and row['control_green'] and row['restore_ok'] and bool(ids)
                    and sorted(witnessed) == sorted(ids))
    return row


def disposition_failures(repo, dead, rows):
    failures = []
    names = [r.get('name') for r in rows if isinstance(r, dict)]
    if sorted(names) != sorted(dead) or len(names) != len(rows):
        failures.append('row set differs from the %d dead round-23 wave-2 seats' % len(dead))
    for r in rows:
        if not isinstance(r, dict) or r.get('status') not in STATUSES:
            failures.append('bad row %r' % (r,))
            continue
        want = STATUSES[r['status']]
        if want is None:
            if not (isinstance(r.get('error'), str) and r['error'].strip()):
                failures.append('%s: died without error text' % r['name'])
            continue
        path = repo / str(r.get('report', ''))
        if not r.get('report') or not path.is_file():
            failures.append('%s: report missing' % r['name'])
            continue
        verdicts = re.findall(r'^R23-REATTACK %s: (AGREE|FINDING)\b' % re.escape(r['name']),
                              path.read_text(errors='replace'), re.M)
        if verdicts != [want]:
            failures.append('%s: report verdict %s != %s' % (r['name'], verdicts, want))
    return failures


def r3(repo):
    outcomes = json.loads((repo / '.ufo/waves/round-23/original-outcomes2.json').read_text())
    dead = sorted(r['name'] for r in outcomes['rows'] if r['status'] != 'completed')
    path = repo / R25 / 'dead-falsifier-disposition.json'
    if not path.is_file():
        return {'holds': False, 'dead': len(dead), 'reason': 'disposition file absent'}
    rows = json.loads(path.read_text())['rows']
    failures = disposition_failures(repo, dead, rows)
    dropped = copy.deepcopy(rows)[1:]
    flipped = copy.deepcopy(rows)
    for r in flipped:
        if r.get('status') in ('reattacked-agree', 'reattacked-finding'):
            r['status'] = 'reattacked-finding' if r['status'] == 'reattacked-agree' else 'reattacked-agree'
            break
    controls = {'drop-one-row': bool(disposition_failures(repo, dead, dropped)),
                'flip-one-status': bool(disposition_failures(repo, dead, flipped))}
    counts = {s: sum(1 for r in rows if r.get('status') == s) for s in STATUSES}
    return {'holds': not failures and all(controls.values()), 'dead': len(dead), 'rows': len(rows),
            'status_counts': counts, 'failures': failures, 'negative_controls_fail_as_required': controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    repo = parser.parse_args().repo.resolve()
    result = {'schema': 'tameshi-r25-c1-measure-v1', 'repo': str(repo), 'items': {}}
    try:
        scorecard = (repo / 'SCORECARD.md').read_text()
        with tempfile.TemporaryDirectory(prefix='tameshi-r25-c1-') as tmp:
            stage = Path(tmp) / 'stage'
            missing = [p for p in STAGE if not (repo / p).is_file()]
            if not missing:
                for p in STAGE:
                    (stage / p).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(repo / p, stage / p)
                checks = {'R1': sweep(stage, 'multitoken-mutants.spec', 'multitoken', r'^FIXTURE \S+ FAIL', tmp),
                          'R2': sweep(stage, 'guard-mutants.spec', 'selftest', r'^CASE \S+ FAIL', tmp)}
            else:
                checks = {k: {'holds': False, 'reason': 'absent: ' + ', '.join(missing)} for k in ('R1', 'R2')}
            checks['R3'] = r3(repo)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(result, setup=str(exc))))
        print('C1_ROUTED: SETUP (%s)' % exc)
        return 2
    done = 0
    for key, label in LABELS.items():
        recorded = re.search(r'^\|\s*%s\b' % label, scorecard, re.M) is not None
        item = dict(checks[key], label=label, scorecard_row=recorded)
        item['dispositioned'] = bool(item['holds'] and recorded)
        done += item['dispositioned']
        result['items'][label] = item
    result['dispositioned'], result['total'] = done, len(LABELS)
    print(json.dumps(result, indent=1, sort_keys=True))
    print('C1_ROUTED: dispositioned=%d/%d' % (done, len(LABELS)))
    return 0 if done == len(LABELS) else 1


if __name__ == '__main__':
    raise SystemExit(main())
