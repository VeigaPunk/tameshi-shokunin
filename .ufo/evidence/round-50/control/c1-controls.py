#!/usr/bin/env python3
"""Round-50 C1 controls, scored with the frozen counter at freeze bytes. Usage: c1-controls.py LANE FREEZE OUTDIR

Each control is a ledger built WITHOUT reading what the routed items ask for, committed in a scratch clone of the
lane at FREEZE (never in the lane), then measured by .ufo/evidence/round-50/c1/measure.py from the clone:
  CTL_0        do-nothing: the freeze tree (no ledger)                             expected C1_R50_PASS=false
  CTL_OPEN     every item `open`, evidence = the first keyed line git-grep finds   expected false
  CTL_PLANOPEN CTL_OPEN + a Planned paragraph naming all 49 ids                    expected false (fixed floor)
  CTL_DECLINE  every item `declined` with a generic reason + grep evidence         expected false (cap, floor)
  CTL_FAB      fabrication: per item, the first commit after routing that added a keyed, non-ack line in an
               allowed path is cited as the fix; items with none stay open + planned. This is the positive
               control for the counter's blind spot (a keyed new line is not proof of a fix); its outcome is
               reported as observed.
Scratch lives under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r50/c1-controls and is removed on exit.
"""
import json
import os
import re
import shutil
import subprocess
import sys

LANE, FREEZE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SCR = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r50', 'c1-controls')
E = '.ufo/evidence/round-50/c1'
ACK = ('planned', 'carried', 'still open', 'not worked', 'stay open', 'stays open', 'remain open',
       'remains open', 'routed to round', 'not fixed', 'unfixed', 'not landed')
HARD = ('.ufo/evidence/round-50/c1/', '.ufo/evidence/round-50/control/', '.ufo/evidence/round-50/contract.json',
        '.ufo/evidence/round-50/freeze.json')
ENV = dict(os.environ, GIT_AUTHOR_NAME='ctl', GIT_AUTHOR_EMAIL='ctl@scratch', GIT_COMMITTER_NAME='ctl',
           GIT_COMMITTER_EMAIL='ctl@scratch')


def git(repo, *args, check=True):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=ENV)
    if check and p.returncode:
        raise SystemExit('git %s failed: %s' % (args, p.stderr.decode()))
    return p.stdout.decode('utf-8', 'replace')


def allowed(path, keys, spot):
    if path in spot or path == 'corpus/routed-defects.json' or path.startswith(HARD):
        return False
    if path.startswith(('.ufo/waves/', '.ufo/reports/')) and not any(path.endswith(k) for k in keys):
        return False
    return True


def excerpt_of(line):
    ex = ' '.join(line.split())[:400]
    return ex if len(ex) >= 15 else None


def grep_ack(repo, d, spot):
    for key in d['keys']:
        out = git(repo, 'grep', '-n', '-F', '-i', '-I', '-e', key, 'HEAD', '--', '.', check=False)
        for hit in out.split('\n'):
            m = re.match(r'^HEAD:([^:]+):(\d+):(.*)$', hit)
            if not m or not allowed(m.group(1), d['keys'], spot):
                continue
            ex = excerpt_of(m.group(3))
            if ex and key.lower() in ex.lower():
                return {'path': m.group(1), 'lines': '%s-%s' % (m.group(2), m.group(2)), 'excerpt': ex}
    return None


def fabricate(repo, d, spot):
    for key in d['keys']:
        commits = git(repo, 'log', '--reverse', '--format=%H', '-S', key, '%s..HEAD' % d['routed_at'],
                      check=False).split()
        for c in commits:
            for path in git(repo, 'diff-tree', '--no-commit-id', '--name-only', '-r', c).split('\n'):
                if not path or not allowed(path, d['keys'], spot):
                    continue
                now = subprocess.run(['git', '-C', repo, 'show', 'HEAD:' + path], capture_output=True)
                if now.returncode:
                    continue
                then = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (d['routed_at'], path)],
                                      capture_output=True)
                then_text = ' '.join(then.stdout.decode('utf-8', 'replace').split()) if then.returncode == 0 else ''
                for no, line in enumerate(now.stdout.decode('utf-8', 'replace').split('\n'), 1):
                    ex = excerpt_of(line)
                    if not ex or key.lower() not in ex.lower() or any(w in line.lower() for w in ACK):
                        continue
                    if ex in then_text:
                        continue
                    return c, {'path': path, 'lines': '%d-%d' % (no, no), 'excerpt': ex}
    return None, None


def main():
    os.makedirs(OUT, exist_ok=True)
    shutil.rmtree(SCR, ignore_errors=True)
    os.makedirs(SCR)
    try:
        defects = json.loads(git(LANE, 'show', '%s:%s/defects.json' % (FREEZE, E)))['defects']
        spot = {d['file'] for d in defects}
        counter = os.path.join(SCR, 'measure.py')
        with open(counter, 'w') as fh:
            fh.write(git(LANE, 'show', '%s:%s/measure.py' % (FREEZE, E)))
        ids = [d['id'] for d in defects]

        def clone(name):
            repo = os.path.join(SCR, name)
            subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', LANE, repo], check=True)
            if os.path.realpath(git(repo, 'rev-parse', '--show-toplevel').strip()) != os.path.realpath(repo):
                raise SystemExit('clone toplevel mismatch')
            git(repo, 'checkout', '-q', '--detach', FREEZE)
            return repo

        def land(repo, ledger, planned=False):
            with open(os.path.join(repo, 'corpus/routed-defects.json'), 'w') as fh:
                json.dump({'schema': 'control', 'defects': ledger}, fh, indent=1)
            if planned:
                with open(os.path.join(repo, 'SCORECARD.md'), 'a') as fh:
                    fh.write('\n**Planned (round 51):** ' + ' '.join(ids) + '\n')
            git(repo, 'add', '-A')
            git(repo, 'commit', '-q', '-m', 'control ledger')

        def score(name, repo):
            p = subprocess.run([sys.executable, counter, '--lane', repo, '--rev', 'HEAD', '--explain'],
                               capture_output=True)
            text = p.stdout.decode('utf-8', 'replace')
            with open(os.path.join(OUT, 'c1-%s.stdout' % name), 'w') as fh:
                fh.write(text + p.stderr.decode('utf-8', 'replace'))
            last = text.strip().split('\n')[-1] if text.strip() else 'NO OUTPUT'
            print('%s exit=%d %s' % (name, p.returncode, last))
            return p.returncode

        rcs = {}
        rcs['CTL_0'] = score('CTL_0', clone('CTL_0'))
        acks = {}
        repo = clone('CTL_OPEN')
        for d in defects:
            acks[d['id']] = grep_ack(repo, d, spot)
        print('grep evidence found for %d of %d items' % (sum(1 for v in acks.values() if v), len(defects)))
        land(repo, [{'id': d['id'], 'status': 'open', 'evidence': [acks[d['id']]] if acks[d['id']] else []}
                    for d in defects])
        rcs['CTL_OPEN'] = score('CTL_OPEN', repo)
        repo = clone('CTL_PLANOPEN')
        land(repo, [{'id': d['id'], 'status': 'open', 'evidence': [acks[d['id']]] if acks[d['id']] else []}
                    for d in defects], planned=True)
        rcs['CTL_PLANOPEN'] = score('CTL_PLANOPEN', repo)
        repo = clone('CTL_DECLINE')
        land(repo, [{'id': d['id'], 'status': 'declined', 'reason': 'declined by the control without reading the item',
                     'evidence': [acks[d['id']]] if acks[d['id']] else []} for d in defects])
        rcs['CTL_DECLINE'] = score('CTL_DECLINE', repo)
        repo = clone('CTL_FAB')
        ledger, fabricated = [], 0
        for d in defects:
            c, ev = fabricate(repo, d, spot)
            if c:
                fabricated += 1
                ledger.append({'id': d['id'], 'status': 'fixed', 'commit': c, 'evidence': [ev]})
            else:
                ledger.append({'id': d['id'], 'status': 'open', 'evidence': [acks[d['id']]] if acks[d['id']] else []})
        print('CTL_FAB fabricated fixed rows: %d of %d' % (fabricated, len(defects)))
        land(repo, ledger, planned=True)
        rcs['CTL_FAB'] = score('CTL_FAB', repo)
        with open(os.path.join(OUT, 'c1-CTL_FAB.ledger.json'), 'w') as fh:
            json.dump(ledger, fh, indent=1)
        expected_false = all(rcs[k] == 1 for k in ('CTL_0', 'CTL_OPEN', 'CTL_PLANOPEN', 'CTL_DECLINE'))
        print('C1_CONTROLS: expected_false_all=%s CTL_FAB_exit=%d' % (str(expected_false).lower(), rcs['CTL_FAB']))
        return 0 if expected_false else 1
    finally:
        shutil.rmtree(SCR, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
