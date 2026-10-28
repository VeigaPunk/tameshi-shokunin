#!/usr/bin/env python3
"""Sentinel T54W2Sent02: forge trace inputs against the FROZEN C1 counter.

Usage: attack-driver.py CLONE C0 LANE COUNTER

Runs four revisions of one hand-bound round-54 re-key and prints, for each,
the counter verdict line plus the round-21 selector's per-section reasons:

  R0 baseline                      -> expect PASS
  R1 one trace input digest wrong  -> expect trace-input-drift
  R2 live_lane_reads wrong digest  -> expect live-lane-read
  R3 same live path, right digest  -> expect PASS again (positive control)

Only the clone is written; the lane is read through the shared clone.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
REKEY_PREFIX = '.ufo/evidence/round-21/coldread/rekey-r54-'
CLONE, C0, LANE, COUNTER, HEADING = sys.argv[1:6]
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
        subprocess.run(['rm', '-rf', str(work)], check=True)
    work.mkdir()
    r = subprocess.run([sys.executable, COUNTER, '--lane', CLONE, '--rev', rev,
                        '--work', str(work), '--explain'],
                       capture_output=True, text=True, env=dict(ENV, TMPDIR=str(SCR)))
    print('### %s counter exit=%d' % (tag, r.returncode))
    print(r.stdout.strip())
    return r


def selector(rev, tag):
    r = subprocess.run([sys.executable, os.path.join(CLONE, '.ufo/evidence/round-21/coldread/measure.py'),
                        '--repo', CLONE, '--rev', rev, '--explain'],
                       capture_output=True, text=True, env=dict(ENV, TMPDIR=str(SCR)))
    d = json.loads(r.stdout)
    cr = d['coldread']
    print('### %s selector covered=%d/%d score=%s'
          % (tag, cr['sections_covered'], cr['sections_total'],
             d['calibration_restraint_score']))
    for s in cr['sections']:
        if s['heading'] == HEADING:
            print('    section %r credited=%s vetoed=%s reasons=%s'
                  % (s['heading'], s['credited'], s['vetoed'],
                     sorted(set(s.get('reasons') or []))))
    for m in cr['missing']:
        if m['heading'] == HEADING:
            print('    MISSING %r reason=%s' % (m['heading'], m['reason']))
    return d


assert os.path.realpath(git('rev-parse', '--show-toplevel').stdout.strip()) == os.path.realpath(CLONE)
frozen = json.loads(Path(os.path.join(LANE, '.ufo/evidence/round-54/c1/lost-headings-at-base.json')).read_text())
assert HEADING in frozen, HEADING

ledger = json.loads(Path(CLONE, LEDGER).read_text())
bound = [e for e in ledger['entries'] if e.get('heading') == HEADING
         and any(t.startswith(REKEY_PREFIX) for t in (e.get('traces') or []))]
assert len(bound) == 1, len(bound)
entry = bound[0]
trace_rel = entry['traces'][0]
trace_abs = Path(CLONE, trace_rel)
orig = json.loads(trace_abs.read_text())
input_key = sorted(orig['inputs'])[0]
good = orig['inputs'][input_key]
assert len(good) == 64 and all(c in '0123456789abcdef' for c in good), good
bad = good[:-1] + ('0' if good[-1] != '0' else '1')
skill_sha = hashlib.sha256(subprocess.run(
    ['git', '-C', CLONE, 'cat-file', 'blob', 'HEAD:SKILL.md'],
    capture_output=True, env=ENV).stdout).hexdigest()
wrong_live = hashlib.sha256(b'not the bytes of SKILL.md\n').hexdigest()
live_path = os.path.join(LANE, 'SKILL.md')

print('trace=%s\ninput_key=%s\ngood=%s\nbad=%s\nlive_path=%s\nwrong_live=%s\nskill_sha=%s'
      % (trace_rel, input_key, good, bad, live_path, wrong_live, skill_sha))
print('--- trace bytes at baseline (%s) ---' % HEADING)
print(git('show', 'HEAD:%s' % trace_rel).stdout.rstrip())

# R1: one input digest wrong
t = json.loads(trace_abs.read_text())
t['inputs'][input_key] = bad
trace_abs.write_text(json.dumps(t, indent=1, sort_keys=True) + '\n')
r1 = commit('T54W2Sent02 R1: trace records a wrong sha for %s' % input_key)
counter(r1, 'R1'); selector(r1, 'R1')
print('--- trace bytes at R1 ---')
print(git('show', '%s:%s' % (r1, trace_rel)).stdout.rstrip())

# R2: inputs restored, live_lane_reads names a live path with the wrong digest
t = json.loads(trace_abs.read_text())
t['inputs'][input_key] = good
t['live_lane_reads'] = {live_path: wrong_live}
trace_abs.write_text(json.dumps(t, indent=1, sort_keys=True) + '\n')
r2 = commit('T54W2Sent02 R2: live_lane_reads wrong digest')
counter(r2, 'R2'); selector(r2, 'R2')
print('--- trace bytes at R2 ---')
print(git('show', '%s:%s' % (r2, trace_rel)).stdout.rstrip())

# R3: same live path with the digest of the bytes at REV (positive control)
t = json.loads(trace_abs.read_text())
t['live_lane_reads'][live_path] = skill_sha
trace_abs.write_text(json.dumps(t, indent=1, sort_keys=True) + '\n')
r3 = commit('T54W2Sent02 R3: live_lane_reads bound to REV bytes')
counter(r3, 'R3'); selector(r3, 'R3')
print('--- trace bytes at R3 ---')
print(git('show', '%s:%s' % (r3, trace_rel)).stdout.rstrip())
print('REVS baseline=%s R1=%s R2=%s R3=%s'
      % (git('rev-parse', 'HEAD~3').stdout.strip(), r1, r2, r3))
