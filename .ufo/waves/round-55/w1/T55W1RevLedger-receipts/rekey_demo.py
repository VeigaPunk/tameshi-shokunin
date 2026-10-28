#!/usr/bin/env python3
"""Decisive fixture: does a re-key of ALL drifted headings restore the coldread floor?

Clone of the lane at the frozen base + the lane worktree's round-55 production
edits = commit W (the content revision). Clean readers are planted for every
heading that loses credit at W; the round-54 binder is then run with PIN=W and
the floor re-measured at the resulting ledger commit.
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path(sys.argv[1])
L = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
W = S / 'rk'
OUT = []
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1')


def say(*a):
    line = ' '.join(str(x) for x in a)
    OUT.append(line)
    print(line, flush=True)


def git(c, *a, check=True):
    top = subprocess.run(['git', '-C', str(c), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True, env=ENV).stdout.strip()
    assert top == str(c), (top, c)
    r = subprocess.run(['git', '-C', str(c)] + list(a), capture_output=True, env=ENV)
    if check and r.returncode:
        raise SystemExit('git failed: %r %s' % (a, r.stderr.decode()[:400]))
    return r


def commit(c, msg):
    git(c, 'add', '--all')
    git(c, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '-q', '-m', msg)
    return git(c, 'rev-parse', 'HEAD').stdout.decode().strip()


def r18(c, rev=None):
    src = (c / '.ufo/evidence/round-18/measure.py').read_bytes() if rev is None \
        else git(c, 'show', '%s:.ufo/evidence/round-18/measure.py' % rev).stdout
    t = S / ('r18rk-%s.py' % (rev or 'wt')[:8])
    t.write_bytes(src)
    spec = importlib.util.spec_from_file_location('r18rk_%s' % t.stem, t)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def measure(c, rev, label):
    run = subprocess.run([sys.executable, str(c / '.ufo/evidence/round-21/coldread/measure.py'),
                          '--repo', str(c), '--rev', rev], capture_output=True, text=True,
                         env=ENV, timeout=2400)
    d = json.loads(run.stdout)
    cr = d['coldread']
    lost = [(s['heading'] or '(preamble)', s['reason']) for s in cr['sections'] if not s['credited']]
    say('%s rev=%s covered=%d/%d restraint=%s box3=%s lost=%d'
        % (label, rev[:10], cr['sections_covered'], cr['sections_total'],
           d['calibration_restraint_score'], cr['box3_full_page'], len(lost)))
    for h, why in lost:
        say('   LOST %s :: %s' % (h, why[:120]))
    return d, lost


def main():
    start = '631cd6455e58dce969310b4c0466c3383d9f5108'
    if W.exists():
        shutil.rmtree(W)
    subprocess.run(['git', 'clone', '--shared', '--quiet', str(L), str(W)], check=True, env=ENV)
    git(W, 'checkout', '--detach', start)
    for f in git(L, 'diff', '--name-only', '0a2010acd1e92e4e332774050825e21bcfc7e079').stdout.decode().split():
        if f.startswith('.ufo/'):
            continue
        dst = W / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(L / f, dst)
    w = commit(W, 'fixture W: the round-55 production edits')
    say('W=%s' % w)
    _, lost = measure(W, w, 'FLOOR at W (base ledger, nothing re-keyed)')
    headings = sorted({h for h, _ in lost if h != '(preamble)'})
    say('headings that lost credit: %d -> %s' % (len(headings), json.dumps(headings, ensure_ascii=False)))

    raw = git(W, 'show', '%s:SKILL.md' % w).stdout
    skill_sha = hashlib.sha256(raw).hexdigest()
    secs = {s['heading']: s for s in r18(W, w).sectionize(raw)}
    d = W / '.ufo/waves/round-55/w1'
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    planted = []
    for h in headings:
        s = secs[h]
        p = d / ('fixture-%02d.reader.json' % len(planted))
        p.write_text(json.dumps({'heading': h, 'cand': w, 'section_sha256': s['sha256'],
                                 'findings': [], 'skill_sha256': skill_sha,
                                 'section': {'start': s['start'], 'end': s['end']}},
                                indent=1) + '\n')
        p.with_suffix('.md').write_text('# fixture clean reader for %s\n' % h)
        planted.append(p.stem.replace('.reader', ''))
    say('planted %d clean readers' % len(planted))

    drv = (S / 'binder-rk.py')
    text = (W / '.ufo/evidence/round-54/integrate/binder.py').read_text()
    text = text.replace(
        "E = '.ufo/evidence/round-54'",
        "E = '.ufo/evidence/round-54'\n"
        "_hf = sys.argv[5]\n_waves = sys.argv[6]\n_label = sys.argv[7]", 1)
    text = text.replace(
        "WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')  # both waves; w2 carries the C1 reads\n",
        "WAVE_DIRS = (_waves,)\n")
    text = text.replace(
        "HEADINGS = json.loads(Path(LANE, E, 'c1/lost-headings-at-c0.json').read_text('utf-8'))",
        "HEADINGS = json.loads(Path(_hf).read_text('utf-8'))")
    text = text.replace(
        "BASE7 = json.loads(Path(LANE, E, 'c1/lost-headings-at-base.json').read_text('utf-8'))\n"
        "HEADINGS = sorted(set(HEADINGS) | set(BASE7))", "HEADINGS = sorted(set(HEADINGS))")
    text = text.replace("RES_PATH = Path(LANE, E, 'integrate/resolutions.json')",
                        "RES_PATH = Path(LANE, E, 'integrate/ABSENT-r55.json')")
    text = text.replace("'seats': [Path(f).stem, 'L1 TameshiR54a2 re-key (round 54)'],",
                        "'seats': [Path(f).stem, _label],")
    drv.write_text(text)
    hf = S / 'rk-headings.json'
    hf.write_text(json.dumps(headings, ensure_ascii=False))
    out = W / ('.ufo/evidence/round-21/coldread/rekey-r55-%s' % w[:12])
    run = subprocess.run([sys.executable, str(drv), str(W), w, w, str(out),
                          str(hf), '.ufo/waves/round-55/w1', 'L1 TameshiR55 re-key (round 55)'],
                         capture_output=True, text=True, env=ENV, timeout=2400)
    say('BIND rc=%d' % run.returncode)
    for line in run.stdout.splitlines():
        say('   ' + line[:150])
    if run.stderr.strip():
        say('BIND stderr', run.stderr.strip()[:800])
    rev = commit(W, 'fixture REV: re-keyed ledger + traces')
    say('REV=%s' % rev)
    measure(W, rev, 'AFTER re-key at REV')

    # A late SCORECARD.md/LOG.md edit after REV: DROP must absorb it.
    for name in ('SCORECARD.md', 'LOG.md'):
        p = W / name
        p.write_text(p.read_text() + '\nfixture late edit\n')
    rev2 = commit(W, 'fixture REV2: SCORECARD/LOG edited after REV')
    measure(W, rev2, 'AFTER re-key, record files edited post-REV')
    (S / 'rk.out').write_text('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
