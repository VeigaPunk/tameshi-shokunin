#!/usr/bin/env python3
"""Sentinel T54W2Sent02 arm-4 probe: can an HONEST wave-1 report ever satisfy it?

Usage: arm4-probe.py CLONE C0 LANE COUNTER

The frozen arm 4 needs, for each frozen heading,
    d['cand'] == c0  AND  d['section_sha256'] == sha256(section bytes at REV).
The 23 committed-in-spirit wave-1 reports were produced at C0 and carry C0's
section shas.  This probe commits exactly those reports into w1/ and runs the
frozen counter at a revision that descends from C1, for both legal c0 choices:

  E1  c0 = C1 (rekey dir rekey-r54-99c3bc88d704, read_rev = C1)
  E2  c0 = C0 (rekey dir rekey-r54-59c38109bf11, read_rev = C0)

Everything else (arms 1-3 and 5) is held at the passing baseline.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
CLONE, C0, LANE, COUNTER = sys.argv[1:5]
W1 = os.path.join(LANE, '.ufo/waves/round-54/w1')
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
OLD_REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704'
NEW_REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11'
WAVE = '.ufo/waves/round-54/w1'
SCR = Path(os.environ['TMPDIR'])


def git(*args, check=True):
    r = subprocess.run(['git', '-C', CLONE] + list(args), env=ENV,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit('git %s: %s' % (' '.join(args), r.stderr.strip()))
    return r


def commit(msg):
    git('add', '-A')
    git('-c', 'user.name=sentinel', '-c', 'user.email=sentinel@example.invalid',
        'commit', '--quiet', '-m', msg)
    return git('rev-parse', 'HEAD').stdout.strip()


def counter(rev, tag):
    work = SCR / ('w-' + tag)
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    r = subprocess.run([sys.executable, COUNTER, '--lane', CLONE, '--rev', rev,
                        '--work', str(work), '--explain'],
                       capture_output=True, text=True, env=dict(ENV, TMPDIR=str(SCR)))
    print('### %s counter exit=%d' % (tag, r.returncode))
    print(r.stdout.strip())
    return r


assert os.path.realpath(git('rev-parse', '--show-toplevel').stdout.strip()) == os.path.realpath(CLONE)
BASE = git('rev-parse', 'HEAD').stdout.strip()   # the passing hand-bound baseline
git('checkout', '--quiet', BASE)

honest = sorted(f for f in os.listdir(W1) if 'Read' in f and f.endswith('.json'))
assert len(honest) == 23, len(honest)
shonen_sha = hashlib.sha256(subprocess.run(
    ['git', '-C', CLONE, 'cat-file', 'blob', BASE + ':SHONEN.md'],
    capture_output=True, env=ENV).stdout).hexdigest()

# replace the synthetic w1 reports with the 23 honest wave-1 reports
for f in os.listdir(os.path.join(CLONE, WAVE)):
    if 'Read' in f and f.endswith('.json'):
        os.remove(os.path.join(CLONE, WAVE, f))
for f in honest:
    shutil.copyfile(os.path.join(W1, f), os.path.join(CLONE, WAVE, f))
print('honest reports copied=%d  first cand=%s'
      % (len(honest), json.load(open(os.path.join(CLONE, WAVE, honest[0])))['cand']))

e1 = commit('T54W2Sent02 E1: honest wave-1 reports, c0=C1')
e1_out = counter(e1, 'E1')

# E2: move the re-key to c0=C0 and rebind inputs to an unchanged file
os.rename(os.path.join(CLONE, OLD_REKEY), os.path.join(CLONE, NEW_REKEY))
ledger_path = os.path.join(CLONE, LEDGER)
ledger = json.loads(Path(ledger_path).read_text())
for e in ledger['entries']:
    tr = e.get('traces') or []
    if not any(isinstance(t, str) and t.startswith(OLD_REKEY + '/') for t in tr):
        continue
    e['read_rev'] = '59c38109bf119d0e9d4f878644a82babc937bc1e'
    e['inputs'] = {'SHONEN.md': shonen_sha}
    e['traces'] = [t.replace(OLD_REKEY, NEW_REKEY, 1) for t in tr]
for root, _dirs, files in os.walk(os.path.join(CLONE, NEW_REKEY)):
    for f in files:
        p = os.path.join(root, f)
        d = json.loads(Path(p).read_text())
        d['inputs'] = {'SHONEN.md': shonen_sha}
        Path(p).write_text(json.dumps(d, indent=1, sort_keys=True) + '\n')
Path(ledger_path).write_text(json.dumps(ledger, indent=1, sort_keys=True) + '\n')
e2 = commit('T54W2Sent02 E2: honest wave-1 reports, c0=C0')
e2_out = counter(e2, 'E2')

print('BASE=%s E1=%s E2=%s' % (BASE, e1, e2))
for tag, out in (('E1', e1_out), ('E2', e2_out)):
    for line in out.stdout.splitlines():
        if line.startswith('C1_R54:'):
            print('%s VERDICT %s' % (tag, line))
