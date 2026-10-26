#!/usr/bin/env python3
"""T49CritC1Contract probe 2: the frozen positive control's own input set is record-bound.

Replicates c1-controls.py's CTL_K2 shape (the two SKILL.md prefix edits + pinned_inputs +
mechanical rows) in a throwaway fixture, confirms total=0 with the frozen counter, then
appends ONE line to a lesson record one of those entries pins (corpus/lessons/round-1.md,
cited by the promotion section) and re-scores at a fresh work dir.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = sys.argv[1]
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '8ca67421111fa354b47b803358391d0b07fc6db9'
COUNTER = os.path.join(LANE, '.ufo/evidence/round-49/c1/measure.py')
FLEET = os.path.dirname(LANE)
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='r49-probe', GIT_AUTHOR_EMAIL='probe@invalid',
           GIT_COMMITTER_NAME='r49-probe', GIT_COMMITTER_EMAIL='probe@invalid',
           PYTHONDONTWRITEBYTECODE='1')

spec = importlib.util.spec_from_file_location('c1', COUNTER)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'


def git(repo, *a, data=None):
    r = subprocess.run(['git', '-C', repo] + list(a), input=data, capture_output=True, env=ENV)
    if r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(a), r.stderr.decode()[-300:]))
    return r.stdout


def fsha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


D = os.path.join(S, 'fix2')
shutil.rmtree(D, ignore_errors=True)
git(S, 'clone', '--quiet', '--shared', LANE, D)
assert os.path.realpath(git(D, 'rev-parse', '--show-toplevel').decode().strip()) == os.path.realpath(D)
git(D, 'reset', '--hard', '-q', BASE)
git(D, 'clean', '-qfd')

mod = c1.load_monitor_module(LANE)
raw = open(os.path.join(D, 'SKILL.md'), encoding='utf-8').read()
for bare in ('(`:1294-1297`)', '(`:1246-1270`)'):
    assert raw.count(bare) == 1, bare
    raw = raw.replace(bare, '(`SKILL.md' + bare[2:])
open(os.path.join(D, 'SKILL.md'), 'w', encoding='utf-8').write(raw)
git(D, 'add', '-A')
git(D, 'commit', '-q', '-m', 'CTL_K2-shape prefix edit')
rev1 = git(D, 'rev-parse', 'HEAD').decode().strip()

secs = {s['heading']: s for s in mod.sectionize(open(os.path.join(D, 'SKILL.md'), 'rb').read())
        if s['heading'] in c1.TARGETS}
ptrs, _ = c1.list_pointers(D, rev1)
led = json.load(open(os.path.join(D, LEDGER)))
inputs_by_heading = {}
for i, h in enumerate(c1.TARGETS):
    s = secs[h]
    files = sorted({p['file'] for p in ptrs if p['heading'] == h and p['file']
                    and p['kind'] in ('line', 'path') and p['file'] not in c1.VOLATILE
                    and p['file'] != 'SKILL.md'})
    inputs = {p: fsha(os.path.join(D, p)) for p in files}
    inputs_by_heading[h] = inputs
    tr = '.ufo/evidence/round-49/control/probe2-trace-%d.json' % i
    os.makedirs(os.path.dirname(os.path.join(D, tr)), exist_ok=True)
    json.dump({'schema': 'tameshi-trace-inputs-v1', 'inputs': inputs}, open(os.path.join(D, tr), 'w'), indent=1)
    led['entries'].append({'skill_sha256': hashlib.sha256(
        open(os.path.join(D, 'SKILL.md'), 'rb').read()).hexdigest(), 'start': s['start'], 'end': s['end'],
        'heading': h, 'sha256': s['sha256'], 'class': 'record', 'verdict': 'verified-record',
        'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0, 'commands_executed_count': 1,
        'read_rev': BASE, 'inputs': inputs, 'traces': [tr]})
json.dump(led, open(os.path.join(D, LEDGER), 'w'), indent=1)
git(D, 'add', '-A')
git(D, 'commit', '-q', '-m', 'CTL_K2-shape entries')
rev2 = git(D, 'rev-parse', 'HEAD').decode().strip()

ptrs, _ = c1.list_pointers(D, rev2)
rows = []
for p in ptrs:
    row = {'heading': p['heading'], 'ordinal': p['ordinal'], 'raw': p['raw'], 'file': p['file'],
           'ranges': p['ranges'], 'reader': 'control (mechanical, unread)'}
    if p['file'] is None:
        row.update(verdict='absent', excerpt='')
    else:
        if p['kind'] in ('external', 'external-path'):
            fleet_head = subprocess.run(['git', '-C', FLEET, 'rev-parse', 'HEAD'], capture_output=True,
                                        env=ENV).stdout.decode().strip()
            data = c1.blob(FLEET, fleet_head, p['file'][3:]) or b''
            row['fleet_commit'] = fleet_head
        else:
            data = c1.blob(D, rev2, p['file']) or b''
        text = c1.pointed_text(data, p['ranges']) if p['ranges'] else c1.norm(data.decode('utf-8', 'replace'))
        row.update(verdict='holds', excerpt=text[:60])
    rows.append(row)
os.makedirs(os.path.join(D, '.ufo/evidence/round-49/c1'), exist_ok=True)
json.dump({'schema': 'tameshi-r49-reads-v1', 'rows': rows},
          open(os.path.join(D, '.ufo/evidence/round-49/c1/reads.json'), 'w'), indent=1)
git(D, 'add', '-A')
git(D, 'commit', '-q', '-m', 'CTL_K2-shape mechanical reads')
rev = git(D, 'rev-parse', 'HEAD').decode().strip()

print('INPUTS BY HEADING (CTL_K2 shape):')
for h in c1.TARGETS:
    print(' ', h[:44], '->', sorted(inputs_by_heading[h]))


def score(tag, rev):
    w = os.path.join(S, 'w-' + tag)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    r = subprocess.run([sys.executable, '-B', COUNTER, '--lane', D, '--rev', rev, '--work', w, '--fleet', FLEET],
                       capture_output=True, env=dict(ENV, TMPDIR=S))
    out = r.stdout.decode()
    open(os.path.join(S, 'probe2-%s.stdout' % tag), 'w').write(out + r.stderr.decode())
    for line in out.splitlines():
        if line.startswith('C1_R49:') or line.startswith('UNCOVERED'):
            print(tag, line)
    print(tag, 'EXIT', r.returncode)


score('before-append', rev)

REC = 'corpus/lessons/round-1.md'
with open(os.path.join(D, REC), 'a') as fh:
    fh.write('\n<!-- later round appends one line to the lesson the promotion section cites -->\n')
git(D, 'add', '-A')
git(D, 'commit', '-q', '-m', 'append one line to ' + REC)
print('APPENDED', REC, git(D, 'rev-parse', 'HEAD').decode().strip()[:12])
score('after-append', git(D, 'rev-parse', 'HEAD').decode().strip())
