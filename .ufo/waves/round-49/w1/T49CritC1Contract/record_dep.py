#!/usr/bin/env python3
"""T49CritC1Contract probe: does the durability probe bind entries away from record files?

Step 1: point one entry's `inputs` at corpus/lessons/round-48.md (a record file that was
        amended three times inside round 48) and score: the probe appends only to the five
        VOLATILE files, so the entry should still credit and the probe should still pass.
Step 2: append one line to corpus/lessons/round-48.md at a new commit and score again:
        the entry lapses, i.e. a later record append does lapse the section.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = sys.argv[1]
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
COUNTER = os.path.join(LANE, '.ufo/evidence/round-49/c1/measure.py')
D = os.path.join(S, 'fix')
RECORD = 'corpus/lessons/round-48.md'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='r49-probe', GIT_AUTHOR_EMAIL='probe@invalid',
           GIT_COMMITTER_NAME='r49-probe', GIT_COMMITTER_EMAIL='probe@invalid',
           PYTHONDONTWRITEBYTECODE='1')
TARGET = '## Repeated controls and gate registry \u2014 round 12'


def git(*a):
    r = subprocess.run(['git', '-C', D] + list(a), capture_output=True, env=ENV)
    if r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(a), r.stderr.decode()[-300:]))
    return r.stdout


def score(tag):
    w = os.path.join(S, 'w-' + tag)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    r = subprocess.run([sys.executable, '-B', COUNTER, '--lane', D, '--rev', git('rev-parse', 'HEAD').decode().strip(),
                        '--work', w], capture_output=True, env=dict(ENV, TMPDIR=S))
    out = r.stdout.decode()
    open(os.path.join(S, 'record-dep-%s.stdout' % tag), 'w').write(out + r.stderr.decode())
    for line in out.splitlines():
        if line.startswith('C1_R49:') or line.startswith('UNCOVERED'):
            print(tag, line)
    print(tag, 'EXIT', r.returncode, r.stderr.decode()[-200:])
    return r.returncode


sha = hashlib.sha256(git('cat-file', 'blob', 'HEAD:' + RECORD)).hexdigest()
whole = hashlib.sha256(git('cat-file', 'blob', 'HEAD:SKILL.md')).hexdigest()
led_p = os.path.join(D, '.ufo/evidence/round-21/coldread/ledger.json')
led = json.load(open(led_p))
hit = 0
for e in led['entries']:
    if e.get('heading') == TARGET and e.get('skill_sha256') == whole:
        e['inputs'] = {RECORD: sha}
        hit += 1
assert hit == 1, hit
json.dump(led, open(led_p, 'w'), indent=1, ensure_ascii=False)
git('add', '-A')
git('commit', '-q', '-m', 'record-dependency: inputs cite ' + RECORD)
print('STEP1 record-citing entry committed', git('rev-parse', 'HEAD').decode().strip()[:12], RECORD, sha[:12])
score('step1-probe-passes')

with open(os.path.join(D, RECORD), 'a') as fh:
    fh.write('\n<!-- round-50 append: the record line every later round writes -->\n')
git('add', '-A')
git('commit', '-q', '-m', 'later round appends one line to ' + RECORD)
print('STEP2 appended one line to', RECORD, git('rev-parse', 'HEAD').decode().strip()[:12])
score('step2-record-append')
