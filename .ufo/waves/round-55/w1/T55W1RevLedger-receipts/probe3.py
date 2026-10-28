#!/usr/bin/env python3
"""Probe 3: the ordering rule. Re-key all 18 headings at W, then edit the pinned
input files AFTER the pin and re-measure: the floor falls back."""
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path(sys.argv[1])
L = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
OUT = []
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1')
START = '631cd6455e58dce969310b4c0466c3383d9f5108'
PINNED = ('corpus/QUALITY.md', 'corpus/SOURCES.md', 'tools/context-capture.py',
          'tools/registry-check.py', 'tools/registry.json', 'tools/repeat-control.py')


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
        raise SystemExit('git failed %r %s' % (a, r.stderr.decode()[:300]))
    return r


def commit(c, msg):
    git(c, 'add', '--all')
    git(c, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '-q', '-m', msg)
    return git(c, 'rev-parse', 'HEAD').stdout.decode().strip()


def measure(c, rev, label):
    run = subprocess.run([sys.executable, str(c / '.ufo/evidence/round-21/coldread/measure.py'),
                          '--repo', str(c), '--rev', rev], capture_output=True, text=True,
                         env=ENV, timeout=2400)
    d = json.loads(run.stdout)
    cr = d['coldread']
    lost = [s['heading'] for s in cr['sections'] if not s['credited']]
    say('%s rev=%s covered=%d/%d restraint=%s box3=%s lost=%d %s'
        % (label, rev[:10], cr['sections_covered'], cr['sections_total'],
           d['calibration_restraint_score'], cr['box3_full_page'], len(lost),
           json.dumps(lost[:3], ensure_ascii=False)))
    return d


def main():
    c = S / 'p3'
    if c.exists():
        shutil.rmtree(c)
    subprocess.run(['git', 'clone', '--shared', '--quiet', str(L), str(c)], check=True, env=ENV)
    git(c, 'checkout', '--detach', START)
    for f in git(L, 'diff', '--name-only', '0a2010acd1e92e4e332774050825e21bcfc7e079').stdout.decode().split():
        if f.startswith('.ufo/'):
            continue
        dst = c / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(L / f, dst)
    w = commit(c, 'fixture W')
    src = git(c, 'show', '%s:.ufo/evidence/round-18/measure.py' % w).stdout
    t = S / 'r18p3.py'
    t.write_bytes(src)
    spec = importlib.util.spec_from_file_location('p3r18', t)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    secs = {s['heading']: s for s in m.sectionize(git(c, 'show', '%s:SKILL.md' % w).stdout)}
    headings = json.loads((S / 'worktree-floor.json').read_text())
    lost = [s['heading'] for s in headings['coldread']['sections'] if not s['credited']]
    d = c / '.ufo/waves/round-55/w1'
    d.mkdir(parents=True, exist_ok=True)
    for i, h in enumerate(sorted(lost)):
        s = secs[h]
        (d / ('p3-%02d.reader.json' % i)).write_text(json.dumps(
            {'heading': h, 'cand': w, 'section_sha256': s['sha256'], 'findings': []},
            indent=1) + '\n')
        (d / ('p3-%02d.reader.md' % i)).write_text('# p3\n')
    hf = S / 'p3-headings.json'
    hf.write_text(json.dumps(sorted(lost), ensure_ascii=False))
    text = (c / '.ufo/evidence/round-54/integrate/binder.py').read_text()
    text = text.replace("E = '.ufo/evidence/round-54'",
                        "E = '.ufo/evidence/round-54'\n_hf = sys.argv[5]\n_w = sys.argv[6]", 1)
    text = text.replace(
        "WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')  # both waves; w2 carries the C1 reads\n",
        "WAVE_DIRS = (_w,)\n")
    text = text.replace(
        "HEADINGS = json.loads(Path(LANE, E, 'c1/lost-headings-at-c0.json').read_text('utf-8'))",
        "HEADINGS = json.loads(Path(_hf).read_text('utf-8'))")
    text = text.replace(
        "BASE7 = json.loads(Path(LANE, E, 'c1/lost-headings-at-base.json').read_text('utf-8'))\n"
        "HEADINGS = sorted(set(HEADINGS) | set(BASE7))", "HEADINGS = sorted(set(HEADINGS))")
    text = text.replace("RES_PATH = Path(LANE, E, 'integrate/resolutions.json')",
                        "RES_PATH = Path(LANE, E, 'integrate/ABSENT-r55.json')")
    b = S / 'p3-binder.py'
    b.write_text(text)
    out = c / ('.ufo/evidence/round-21/coldread/rekey-r55-%s' % w[:12])
    run = subprocess.run([sys.executable, str(b), str(c), w, w, str(out), str(hf),
                          '.ufo/waves/round-55/w1', 'L1 p3'],
                         capture_output=True, text=True, env=ENV, timeout=2400)
    say('BIND rc=%d last=%s' % (run.returncode, run.stdout.strip().splitlines()[-1]))
    rev = commit(c, 'fixture REV (18 re-keyed)')
    measure(c, rev, 'REKEYED at REV')
    for p in PINNED:
        f = c / p
        f.write_text(f.read_text() + '\nfixture post-pin edit\n')
    rev2 = commit(c, 'fixture REV2: the six pinned inputs edited after the pin')
    measure(c, rev2, 'AFTER a post-pin edit of the six pinned inputs')
    (S / 'probe3.out').write_text('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
