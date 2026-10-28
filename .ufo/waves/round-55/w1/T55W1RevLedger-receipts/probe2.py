#!/usr/bin/env python3
"""Probe 2: (a) bind ONLY `## Standing rules` at the round-55 content revision and
measure; (b) bind with OUTDIR outside the lane and show the trace path the credit
rule then rejects."""
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
OUT = []
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1')
START = '631cd6455e58dce969310b4c0466c3383d9f5108'


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


def r18(c, rev):
    src = git(c, 'show', '%s:.ufo/evidence/round-18/measure.py' % rev).stdout
    t = S / ('r18p2-%s.py' % rev[:8])
    t.write_bytes(src)
    spec = importlib.util.spec_from_file_location('p2_%s' % t.stem, t)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def measure(c, rev, label):
    run = subprocess.run([sys.executable, str(c / '.ufo/evidence/round-21/coldread/measure.py'),
                          '--repo', str(c), '--rev', rev], capture_output=True, text=True,
                         env=ENV, timeout=2400)
    d = json.loads(run.stdout)
    cr = d['coldread']
    say('%s rev=%s covered=%d/%d restraint=%s box3=%s lost=%d'
        % (label, rev[:10], cr['sections_covered'], cr['sections_total'],
           d['calibration_restraint_score'], cr['box3_full_page'],
           len([s for s in cr['sections'] if not s['credited']])))
    return d


def binder(clone, out_name):
    text = (clone / '.ufo/evidence/round-54/integrate/binder.py').read_text()
    text = text.replace("E = '.ufo/evidence/round-54'",
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
    p = S / (out_name + '.binder.py')
    p.write_text(text)
    return p


def make_wclone(name):
    c = S / name
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
    return c


def main():
    say('== PART 1: bind ONLY `## Standing rules` at the content revision ==')
    c = make_wclone('p2-only')
    w = commit(c, 'fixture W (round-55 production edits)')
    raw = git(c, 'show', '%s:SKILL.md' % w).stdout
    sec = [s for s in r18(c, w).sectionize(raw) if s['heading'] == '## Standing rules'][0]
    d = c / '.ufo/waves/round-55/w1'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'only.reader.json').write_text(json.dumps(
        {'heading': '## Standing rules', 'cand': w, 'section_sha256': sec['sha256'],
         'findings': []}, indent=1) + '\n')
    (d / 'only.reader.md').write_text('# only\n')
    hf = S / 'p2-headings-one.json'
    hf.write_text(json.dumps(['## Standing rules']))
    out = c / ('.ufo/evidence/round-21/coldread/rekey-r55-%s' % w[:12])
    run = subprocess.run([sys.executable, str(binder(c, 'p2one')), str(c), w, w, str(out),
                          str(hf), '.ufo/waves/round-55/w1', 'L1 T55 re-key'],
                         capture_output=True, text=True, env=ENV, timeout=2400)
    say('BIND rc=%d %s' % (run.returncode, run.stdout.strip().replace('\n', ' | ')))
    rev = commit(c, 'fixture REV (one heading re-keyed)')
    measure(c, rev, 'FLOOR after re-keying ONLY `## Standing rules`')
    p = c / 'corpus/QUALITY.md'
    p.write_text(p.read_text() + '\nfixture late QUALITY criterion\n')
    rev3 = commit(c, 'fixture REV3: corpus/QUALITY.md edited after PIN')
    measure(c, rev3, 'FLOOR after re-keying ONLY `## Standing rules` + a post-PIN QUALITY.md edit')

    say('')
    say('== PART 2: OUTDIR outside the lane ==')
    outside = S / 'outside-out'
    shutil.rmtree(outside, ignore_errors=True)
    c2 = make_wclone('p2-outside')
    w2 = commit(c2, 'fixture W (outside-out clone)')
    raw2 = git(c2, 'show', '%s:SKILL.md' % w2).stdout
    sec2 = [s for s in r18(c2, w2).sectionize(raw2) if s['heading'] == '## Standing rules'][0]
    d2 = c2 / '.ufo/waves/round-55/w1'
    d2.mkdir(parents=True, exist_ok=True)
    (d2 / 'ok.reader.json').write_text(json.dumps(
        {'heading': '## Standing rules', 'cand': w2, 'section_sha256': sec2['sha256'],
         'findings': []}, indent=1) + '\n')
    (d2 / 'ok.reader.md').write_text('# ok\n')
    run = subprocess.run([sys.executable, str(binder(c2, 'p2out')), str(c2), w2, w2, str(outside),
                          str(hf), '.ufo/waves/round-55/w1', 'L1 T55 re-key'],
                         capture_output=True, text=True, env=ENV, timeout=2400)
    say('BIND(outside) rc=%d %s' % (run.returncode, run.stdout.strip().replace('\n', ' | ')))
    led = json.loads((c2 / '.ufo/evidence/round-21/coldread/ledger.json').read_text())
    e = [x for x in led['entries'] if x.get('heading') == '## Standing rules'
         and x.get('read_rev') == w2][0]
    say('recorded trace path: %s' % e['traces'])
    m = r18(c2, w2)
    say('entry_reason with an OUTDIR outside the lane: %r'
        % m.entry_reason(str(c2), w2, e, True))
    say('trace blob committed inside the lane? %s'
        % (git(c2, 'cat-file', '-e', '%s:%s' % (w2, e['traces'][0]), check=False).returncode == 0))
    (S / 'probe2.out').write_text('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
