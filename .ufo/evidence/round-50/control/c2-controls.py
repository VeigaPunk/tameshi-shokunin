#!/usr/bin/env python3
"""Round-50 C2 controls, scored with the frozen counter at freeze bytes.

Usage: c2-controls.py LANE FREEZE HIDDEN_PANEL OUTDIR

Each control is committed in a scratch clone of the lane at FREEZE (never in the lane) and measured by
.ufo/evidence/round-50/c2/measure.py against the public round-49 panel (from FREEZE) and the hidden panel:
  CTL_ABSENT    the freeze tree: no shrinker, no F6 records                    expected C2_R50_PASS=false
  CTL_IDENTITY  a shrinker that returns the case unchanged (+ F6 records)       expected false (minimality)
  CTL_REF       the counter's own reference greedy-to-fixpoint shrinker (+ F6 records); the positive control:
                expected true, it shows the counter can pass and that a plain greedy loop meets the bar
Receipt lines print mutant ids only (H01..H08 for the hidden panel), never mutant names or edits.
Scratch: $HYAKU_SCRATCH (default /fast/scratch/hyaku)/tameshi-r50/c2-controls, removed on exit.
"""
import importlib.util
import os
import shutil
import subprocess
import sys

LANE, FREEZE, HIDDEN, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
SCR = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r50', 'c2-controls')
E = '.ufo/evidence/round-50/c2'
ENV = dict(os.environ, GIT_AUTHOR_NAME='ctl', GIT_AUTHOR_EMAIL='ctl@scratch', GIT_COMMITTER_NAME='ctl',
           GIT_COMMITTER_EMAIL='ctl@scratch')
IDENTITY = r'''
import argparse, json, sys
ap = argparse.ArgumentParser()
for f in ('--pristine', '--mutant', '--case', '--out'): ap.add_argument(f)
ap.add_argument('--selftest', action='store_true')
a = ap.parse_args()
if a.selftest: print('IDENTITY_SELFTEST ok'); sys.exit(0)
c = json.load(open(a.case))
n = len(c['registry'].splitlines(True)) + len(c['staged'].splitlines(True))
m = c.get('map')
if isinstance(m, dict) and isinstance(m.get('map'), dict): n += len(m['map'])
json.dump({'case': c, 'runs': 0, 'units_before': n, 'units_after': n}, open(a.out, 'w'))
'''


def git(repo, *args):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=ENV)
    if p.returncode:
        raise SystemExit('git %s failed: %s' % (args, p.stderr.decode()))
    return p.stdout.decode('utf-8', 'replace')


def main():
    os.makedirs(OUT, exist_ok=True)
    shutil.rmtree(SCR, ignore_errors=True)
    os.makedirs(SCR)
    try:
        counter = os.path.join(SCR, 'measure.py')
        with open(counter, 'w') as fh:
            fh.write(git(LANE, 'show', '%s:%s/measure.py' % (FREEZE, E)))
        spec = importlib.util.spec_from_file_location('c2counter', counter)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ref = mod.REF_SHRINKER.replace('MODE', 'pass').replace('LIE', '0')
        public = os.path.join(SCR, 'public.json')
        with open(public, 'w') as fh:
            fh.write(git(LANE, 'show', '%s:.ufo/evidence/round-49/c2/panel.json' % FREEZE))

        def clone(name):
            repo = os.path.join(SCR, name)
            subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', LANE, repo], check=True)
            if os.path.realpath(git(repo, 'rev-parse', '--show-toplevel').strip()) != os.path.realpath(repo):
                raise SystemExit('clone toplevel mismatch')
            git(repo, 'checkout', '-q', '--detach', FREEZE)
            return repo

        def land(repo, shrinker):
            with open(os.path.join(repo, 'tools/shrink-case.py'), 'w') as fh:
                fh.write(shrinker)
            with open(os.path.join(repo, 'corpus/README.md'), 'a') as fh:
                fh.write('\n| F6 | fixture minimization (control fixture) | held (round 50) |\n')
            with open(os.path.join(repo, 'corpus/SOURCES.md'), 'a') as fh:
                fh.write('\n| S999 | control fixture — https://example.invalid/ctl | paper | A | s | a | t | mined | '
                         '2026-10-26 | 365d | ctl-shrink |\n')
            with open(os.path.join(repo, 'corpus/knowledge/ctl-shrink.md'), 'w') as fh:
                fh.write('source: S999 — https://example.invalid/ctl\nground: F6\n')
            git(repo, 'add', '-A')
            git(repo, 'commit', '-q', '-m', 'control shrinker')

        def score(name, repo):
            work = os.path.join(SCR, 'work-' + name)
            p = subprocess.run([sys.executable, counter, '--lane', repo, '--rev', 'HEAD', '--work', work,
                                '--panel', public, '--hidden', HIDDEN], capture_output=True)
            text = p.stdout.decode('utf-8', 'replace')
            with open(os.path.join(OUT, 'c2-%s.stdout' % name), 'w') as fh:
                fh.write(text + p.stderr.decode('utf-8', 'replace'))
            last = text.strip().split('\n')[-1] if text.strip() else 'NO OUTPUT ' + p.stderr.decode()[-300:]
            print('%s exit=%d %s' % (name, p.returncode, last), flush=True)
            shutil.rmtree(work, ignore_errors=True)
            return p.returncode

        rcs = {'CTL_ABSENT': score('CTL_ABSENT', clone('CTL_ABSENT'))}
        repo = clone('CTL_IDENTITY')
        land(repo, IDENTITY)
        rcs['CTL_IDENTITY'] = score('CTL_IDENTITY', repo)
        repo = clone('CTL_REF')
        land(repo, ref)
        rcs['CTL_REF'] = score('CTL_REF', repo)
        ok = rcs['CTL_ABSENT'] == 1 and rcs['CTL_IDENTITY'] == 1
        print('C2_CONTROLS: expected_false_all=%s CTL_REF_exit=%d' % (str(ok).lower(), rcs['CTL_REF']))
        return 0 if ok else 1
    finally:
        shutil.rmtree(SCR, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
