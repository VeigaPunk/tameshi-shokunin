#!/usr/bin/env python3
"""Scratch-clone accept arm for validate-readers.py on the real 18 headings."""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
BASE = '981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1'
VALIDATOR = str(LANE / '.ufo/waves/round-56/validate-readers.py')
C1 = str(LANE / '.ufo/evidence/round-56/c1/measure.py')
HEADINGS = json.loads((LANE / '.ufo/evidence/round-56/c1/lost-headings-at-base.json').read_text())
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')

CLONE = Path(sys.argv[1])
WORK = Path(sys.argv[2])


def git(*args):
    r = subprocess.run(['git', '-C', str(CLONE)] + list(args), env=ENV,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('git %s failed: %s' % (' '.join(args), r.stderr))
    return r.stdout


def commit(msg):
    git('add', '-Af')
    git('-c', 'user.name=wave1', '-c', 'user.email=wave1@example.invalid', 'commit', '-q', '-m', msg)
    return git('rev-parse', 'HEAD').strip()


def show(rev, path):
    r = subprocess.run(['git', '-C', str(CLONE), 'show', '%s:%s' % (rev, path)],
                       env=ENV, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def load_r18(rev):
    raw = show(rev, '.ufo/evidence/round-18/measure.py')
    p = WORK / ('r18-%s.py' % rev[:12])
    p.write_bytes(raw)
    spec = importlib.util.spec_from_file_location('r18_' + rev[:12], str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sections(mod, rev):
    return {s['heading']: s for s in mod.sectionize(show(rev, 'SKILL.md'))}


def slug(heading):
    return re.sub(r'[^A-Za-z0-9]+', '-', heading.strip('# ')).strip('-')[:40]


def write_reports(cand, secs, override=None):
    w = CLONE / '.ufo/waves/round-56/w2'
    if w.exists():
        for p in w.iterdir():
            p.unlink()
    w.mkdir(parents=True, exist_ok=True)
    override = override or {}
    for i, h in enumerate(HEADINGS):
        s = secs[h]
        cmd = "git -C . show %s:SKILL.md | sed -n '%d,%dp'" % (cand, s['start'], s['end'])
        data = {
            'heading': h,
            'cand': cand,
            'section_sha256': override.get(h, s['sha256']),
            'findings': ['section re-read end to end at c0; no defect found'],
            'commands': [cmd],
        }
        stem = 'T56W2Read-%02d-%s' % (i, slug(h))
        (w / (stem + '.json')).write_text(json.dumps(data, indent=1) + '\n')
        (w / (stem + '.md')).write_text(
            '# %s\n\nCommand run:\n\n    %s\n\nFindings: section re-read end to end at c0; '
            'no defect found.\n' % (h, cmd))


def run_validator(rev, c0, work):
    work.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, VALIDATOR, '--lane', str(CLONE), '--rev', rev,
                        '--c0', c0, '--work', str(work), '--explain',
                        '--headings', str(LANE / '.ufo/evidence/round-56/c1/lost-headings-at-base.json')],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def run_c1(rev, work):
    work.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, C1, '--lane', str(CLONE), '--rev', rev,
                        '--work', str(work), '--explain'],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


top = git('rev-parse', '--show-toplevel').strip()
assert Path(top) == CLONE.resolve(), (top, CLONE)
print('clone toplevel =', top)

base = git('rev-parse', 'HEAD').strip()
print('clone HEAD =', base)
assert base == BASE

# --- C0: the one content edit the 18 headings need (## Standing rules) ----------
mod = load_r18(base)
base_secs = sections(mod, base)
lines = show(base, 'SKILL.md').decode('utf-8').split('\n')
sec = base_secs['## Standing rules']
insert_at = sec['end']                      # 0-based index of the line after the section
lines.insert(insert_at, '- round-56 selftest marker: the standing calibration row states the '
                        'score the monitor reads at the commit it names.')
(CLONE / 'SKILL.md').write_text('\n'.join(lines))
c0 = commit('c0: standing rules restated')
print('C0 =', c0)
c0_secs = sections(mod, c0)
print('standing-rules sha base=%s c0=%s'
      % (base_secs['## Standing rules']['sha256'][:12], c0_secs['## Standing rules']['sha256'][:12]))
assert c0_secs['## Standing rules']['sha256'] != base_secs['## Standing rules']['sha256']
assert all(c0_secs[h]['sha256'] == base_secs[h]['sha256'] for h in HEADINGS if h != '## Standing rules')

# --- accept arm -----------------------------------------------------------------
write_reports(c0, c0_secs)
r1 = commit('w2: 18 reader reports at c0')
rc, out = run_validator(r1, c0, WORK / 'w-accept')
print('\n=== ACCEPT rev=%s ===\n%s' % (r1[:12], out))
print('accept_rc=%d' % rc)

# --- refuse arm: a report hashed at BASE for the section C0 changed -------------
write_reports(c0, c0_secs, override={'## Standing rules': base_secs['## Standing rules']['sha256']})
r2 = commit('w2: standing-rules report hashed at base (stale)')
rc2, out2 = run_validator(r2, c0, WORK / 'w-stale')
print('\n=== STALE-HASH rev=%s ===\n%s' % (r2[:12], out2))
print('stale_rc=%d' % rc2)

# --- refuse arm: section drifts after C0 (REV != C0) ----------------------------
write_reports(c0, c0_secs)
lines2 = show(c0, 'SKILL.md').decode('utf-8').split('\n')
lines2.insert(insert_at, '- post-c0 drift line.')
(CLONE / 'SKILL.md').write_text('\n'.join(lines2))
r3 = commit('post-c0 edit to standing rules')
rc3, out3 = run_validator(r3, c0, WORK / 'w-xrev')
print('\n=== XREV-DRIFT rev=%s ===\n%s' % (r3[:12], out3))
print('xrev_rc=%d' % rc3)

# --- agreement with the frozen C1 counter: re-key dir + reports at C0 -----------
(CLONE / 'SKILL.md').write_text(show(c0, 'SKILL.md').decode('utf-8'))
write_reports(c0, c0_secs)
rekey = CLONE / ('.ufo/evidence/round-21/coldread/rekey-r56-' + c0[:12] + '/traces')
rekey.mkdir(parents=True, exist_ok=True)
(rekey / 'readers.json').write_text(json.dumps({'wave': 2, 'reports': 18}) + '\n')
r4 = commit('rekey + reports at c0')
rc4, out4 = run_validator(r4, c0, WORK / 'w-agree')
print('\n=== AGREE validator rev=%s ===\n%s' % (r4[:12], out4))
print('agree_rc=%d' % rc4)

rc5, out5 = run_c1(r4, WORK / 'c1-accept')
print('\n=== frozen C1 counter rev=%s ===\n%s' % (r4[:12], out5))
print('c1_rc=%d' % rc5)

# --- agreement on the refusal side ----------------------------------------------
write_reports(c0, c0_secs, override={'## Standing rules': base_secs['## Standing rules']['sha256']})
r5 = commit('stale standing-rules report under the rekey')
rc6, out6 = run_validator(r5, c0, WORK / 'w-agree-bad')
print('\n=== AGREE-BAD validator rev=%s ===\n%s' % (r5[:12], out6))
print('agree_bad_rc=%d' % rc6)
rc7, out7 = run_c1(r5, WORK / 'c1-refuse')
print('\n=== frozen C1 counter rev=%s ===\n%s' % (r5[:12], out7))
print('c1_bad_rc=%d' % rc7)
