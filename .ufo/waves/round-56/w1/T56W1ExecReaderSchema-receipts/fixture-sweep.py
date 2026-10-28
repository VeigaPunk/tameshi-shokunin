#!/usr/bin/env python3
"""Attack sweep: can a report be credited without being the report the gate wants?"""
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
HEADINGS = json.loads((LANE / '.ufo/evidence/round-56/c1/lost-headings-at-base.json').read_text())
HEADINGS_FILE = str(LANE / '.ufo/evidence/round-56/c1/lost-headings-at-base.json')
VALIDATOR = str(LANE / '.ufo/waves/round-56/validate-readers.py')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
CLONE, WORK = Path(sys.argv[1]), Path(sys.argv[2])


def git(*a):
    r = subprocess.run(['git', '-C', str(CLONE)] + list(a), env=ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit('git %s: %s' % (' '.join(a), r.stderr))
    return r.stdout


def commit(msg):
    git('add', '-Af')
    git('-c', 'user.name=wave1', '-c', 'user.email=w@example.invalid', 'commit', '-q', '-m', msg)
    return git('rev-parse', 'HEAD').strip()


def show(rev, p):
    r = subprocess.run(['git', '-C', str(CLONE), 'show', '%s:%s' % (rev, p)], env=ENV,
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def sections(rev):
    raw = show(rev, '.ufo/evidence/round-18/measure.py')
    p = WORK / ('r18-%s.py' % rev[:12]); p.write_bytes(raw)
    spec = importlib.util.spec_from_file_location('r18_' + rev[:12], str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return {s['heading']: s for s in m.sectionize(show(rev, 'SKILL.md'))}


def slug(h):
    return re.sub(r'[^A-Za-z0-9]+', '-', h.strip('# ')).strip('-')[:40]


def write(dirname, name_fn, cand, secs, hash_fn=None, heading_fn=None, n=None):
    d = CLONE / ('.ufo/waves/round-56/' + dirname)
    if d.exists():
        for p in d.iterdir():
            p.unlink()
    d.mkdir(parents=True, exist_ok=True)
    for i, h in enumerate(HEADINGS[:n] if n else HEADINGS):
        s = secs[h]
        cmd = "git -C . show %s:SKILL.md | sed -n '%d,%dp'" % (cand, s['start'], s['end'])
        data = {'heading': heading_fn(h) if heading_fn else h,
                'cand': cand,
                'section_sha256': hash_fn(h, secs) if hash_fn else s['sha256'],
                'findings': ['sweep'],
                'commands': [cmd]}
        stem = name_fn(i, h)
        (d / (stem + '.json')).write_text(json.dumps(data, indent=1) + '\n')
        (d / (stem + '.md')).write_text('%s\n\n    %s\n' % (data['heading'], cmd))


def run(rev, c0):
    w = Path(WORK / ('w-' + rev[:12])); w.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, VALIDATOR, '--lane', str(CLONE), '--rev', rev, '--c0', c0,
                        '--work', str(w), '--headings', HEADINGS_FILE],
                       capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    return r.returncode, last, r.stdout


top = git('rev-parse', '--show-toplevel').strip()
assert Path(top) == CLONE.resolve()
base = git('rev-parse', 'HEAD').strip()
secs = sections(base)
print('sweep base =', base)

name = lambda i, h: 'T56W2Read-%02d-%s' % (i, slug(h))

# S1: all 18 valid reports in w1 (the seat's own dir) -> nothing credited
write('w1', name, base, secs)
rev = commit('s1 w1')
rc, last, _ = run(rev, base)
print('S1 w1-only            rc=%d %s' % (rc, last))

# S2: valid structure but each report carries another section's sha256
write('w2', name, base, secs, hash_fn=lambda h, s: s[HEADINGS[(HEADINGS.index(h) + 1)
                                                              % len(HEADINGS)]]['sha256'])
rev = commit('s2 rotated hashes')
rc, last, out = run(rev, base)
print('S2 rotated-hash       rc=%d %s' % (rc, last))
print('   codes:', sorted({l.split()[1] for l in out.splitlines() if l.startswith('REFUSE')}))

# S3: heading string carries a trailing space (frozen heading not matched)
write('w2', name, base, secs, heading_fn=lambda h: h + ' ')
rev = commit('s3 heading whitespace')
rc, last, out = run(rev, base)
print('S3 heading-space      rc=%d %s' % (rc, last))

# S4: one report whose file name misses the counter's glob (no digit after T56W)
def name_s4(i, h):
    return 'T56WRead-%02d-%s' % (i, slug(h)) if i == 0 else name(i, h)
write('w2', name_s4, base, secs)
rev = commit('s4 glob miss digits')
rc, last, out = run(rev, base)
print('S4 no-digit-name      rc=%d %s' % (rc, last))
print('   refusals:', [l for l in out.splitlines() if l.startswith('REFUSE')])

# S5: one report whose file suffix is .json.bak (misses the counter's glob)
write('w2', name, base, secs)
first = sorted((CLONE / '.ufo/waves/round-56/w2').glob('*.json'))[0]
first.rename(first.with_suffix('.json.bak'))
rev = commit('s5 suffix miss')
rc, last, out = run(rev, base)
print('S5 .json.bak-name     rc=%d %s' % (rc, last))
print('   refusals:', [l for l in out.splitlines() if l.startswith('REFUSE')])

# S6: reports present and valid, but every sibling .md missing
write('w2', name, base, secs)
for p in (CLONE / '.ufo/waves/round-56/w2').glob('*.md'):
    p.unlink()
rev = commit('s6 no md')
rc, last, out = run(rev, base)
print('S6 no-md              rc=%d %s' % (rc, last))
