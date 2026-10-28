#!/usr/bin/env python3
"""T55W3MutReader harness: mutate reader deliverables, run the round-55 binder.

Every git call names -C <clone>. The lane is only read (git show / cat).
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
S = Path('/fast/scratch/hyaku/tameshi-r55/T55W3MutReader')
C0 = '9cf0146b94ddba12d454ebf7288ce6e5c5d535bb'
PIN = '4f7a7040a57e7aed17db941be9c27b300aafb783'
CLONE = S / 'lane'
OUT = CLONE / '.ufo/evidence/round-21/coldread/rekey-r55-mut'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
RES = CLONE / '.ufo/evidence/round-55/integrate/resolutions.json'
W = CLONE / '.ufo/waves/round-55/w3'
HEADINGS = json.loads((LANE / '.ufo/evidence/round-55/c1/lost-headings-at-c0.json').read_text('utf-8'))
H1, H2 = HEADINGS[0], HEADINGS[1]
REC = S / 'receipts'


def git(*args, check=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', str(CLONE)] + list(args), env=env,
                          capture_output=True, check=check)


def git_lane(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    return subprocess.run(['git', '-C', str(LANE)] + list(args), env=env,
                          capture_output=True, check=True)


def setup():
    if not CLONE.exists():
        subprocess.run(['git', 'clone', '-q', '--shared', str(LANE), str(CLONE)], check=True)
    top = git('rev-parse', '--show-toplevel').stdout.decode().strip()
    assert top == str(CLONE), (top, str(CLONE))
    git('checkout', '-q', '--detach', PIN)
    assert git('rev-parse', 'HEAD').stdout.decode().strip() == PIN


def section_shas():
    """Frozen round-18 sectionize, extracted at C0 exactly as binder.py does."""
    raw = git('show', '%s:.ufo/evidence/round-18/measure.py' % C0).stdout
    mod_path = S / 'r18-at-c0.py'
    mod_path.write_bytes(raw)
    spec = importlib.util.spec_from_file_location('r18_mut', mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = git('show', '%s:SKILL.md' % C0).stdout
    secs = {s['heading']: s for s in mod.sectionize(skill)}
    return secs, hashlib.sha256(skill).hexdigest()


def build_fixtures(secs, mutations):
    """mutations: {heading: 'sha'|'cand'|'spell'|'empty'|'three'}"""
    shutil.rmtree(W, ignore_errors=True)
    W.mkdir(parents=True)
    for n, h in enumerate(HEADINGS):
        if h not in secs:
            continue
        mut = mutations.get(h)
        body_lines = [l for l in _section_body(secs[h]) if l.strip()]
        quote = body_lines[-1].strip() if body_lines else h
        findings = []
        if h == H2:
            findings = [{'quote': quote, 'why': 'fixture: baseline finding 1'},
                        {'quote': h, 'why': 'fixture: baseline finding 2'}]
        if mut == 'three':
            findings = findings + [{'quote': h, 'why': 'fixture: third, unadjudicated'}]
        if mut == 'empty':
            findings = []
        d = {'heading': h, 'cand': C0, 'section_sha256': secs[h]['sha256'],
             'findings': findings}
        if mut == 'sha':
            d['section_sha256'] = '0' * 64
        if mut == 'cand':
            d['cand'] = '0a2010acd1e92e4e332774050825e21bcfc7e079'
        if mut == 'spell':
            d['heading'] = h.replace('Standing rules', 'Standing rule') if 'Standing' in h \
                else h + ' (misspelled)'
        stem = 'T55W3FIX%02d' % n
        (W / (stem + '.json')).write_text(json.dumps(d, indent=1, ensure_ascii=False) + '\n', 'utf-8')
        md = ['# fixture reader %s' % stem, '', 'heading: `%s`' % h,
              'cand: %s' % d['cand'], 'section_sha256: %s' % d['section_sha256'], '', '## findings']
        md += ['- %s -- %s' % (f['quote'], f['why']) for f in findings] or ['(none)']
        (W / (stem + '.md')).write_text('\n'.join(md) + '\n', 'utf-8')


def _section_body(sec):
    raw = git('show', '%s:SKILL.md' % C0).stdout.decode('utf-8', 'surrogateescape').split('\n')
    return raw[sec['start'] - 1:sec['end']]


def write_res(items):
    RES.write_text(json.dumps(items, indent=1) + '\n', 'utf-8')


def run_binder(tag, env_extra=None):
    git('checkout', '--', LEDGER)
    shutil.rmtree(OUT, ignore_errors=True)
    work = S / 'work'
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    before = hashlib.sha256((CLONE / LEDGER).read_bytes()).hexdigest()
    env = dict(os.environ)
    env['TMPDIR'] = str(work)
    env.pop('GIT_DIR', None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable, str(CLONE / '.ufo/evidence/round-55/integrate/binder.py'),
                        str(CLONE), C0, PIN, str(OUT)], env=env, cwd=str(CLONE),
                       capture_output=True)
    out, err = p.stdout.decode(), p.stderr.decode()
    after_bytes = (CLONE / LEDGER).read_bytes()
    led = json.loads(after_bytes.decode('utf-8', 'surrogateescape'))
    entries = [e for e in led['entries'] if isinstance(e, dict) and e.get('heading') == tag[1]] \
        if tag[1] else []
    fresh = [e for e in entries if str(e.get('read_rev')) == C0]
    rec = {'arm': tag[0], 'heading': tag[1], 'exit': p.returncode,
           'stdout': out, 'stderr': err,
           'ledger_sha_before': before,
           'ledger_sha_after': hashlib.sha256(after_bytes).hexdigest(),
           'entry_count': len(led['entries']),
           'fresh_entries_for_heading': fresh,
           'simulated': bool(tag[1] and tag[1] == SIMULATED)}
    return rec


SIMULATED = None


def emit(rec):
    (REC / ('%s.json' % rec['arm'])).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n', 'utf-8')
    (REC / ('%s.stdout' % rec['arm'])).write_text(rec['stdout'], 'utf-8')
    if rec['stderr']:
        (REC / ('%s.stderr' % rec['arm'])).write_text(rec['stderr'], 'utf-8')
    tail = rec['stdout'].strip().splitlines()[-1] if rec['stdout'].strip() else '(no stdout)'
    print('[%s] exit=%d  %s' % (rec['arm'], rec['exit'], tail))
    for line in rec['stdout'].splitlines():
        if line.startswith('SKIP %s' % rec['heading'][:60]) if rec['heading'] else False:
            print('   %s' % line)
    for e in rec['fresh_entries_for_heading']:
        print('   BOUND heading=%r verdict=%s minor_gaps=%s' % (e['heading'], e['verdict'], e['minor_gaps']))
    if rec['stderr']:
        print('   STDERR: %s' % rec['stderr'].strip().splitlines()[-1])


def main():
    REC.mkdir(parents=True, exist_ok=True)
    setup()
    secs, skill_sha = section_shas()
    print('sections=%d skill_sha=%s' % (len(secs), skill_sha))
    print('missing from C0 sections:', [h for h in HEADINGS if h not in secs])
    (REC / '0-headings-at-c0.json').write_text(
        json.dumps([{'heading': h, 'start': secs[h]['start'], 'end': secs[h]['end'],
                     'sha256': secs[h]['sha256']} for h in HEADINGS if h in secs], indent=1) + '\n', 'utf-8')

    # ---- arm 0: committed resolutions.json shape vs binder's RES loader
    build_fixtures(secs, {})
    git('checkout', '--', '.ufo/evidence/round-55/integrate/resolutions.json')
    r0 = run_binder(('A0-committed-res', None))
    emit(r0)

    # ---- adaptation: schema the binder documents ({heading, n})
    write_res([{'heading': H2, 'n': 2}])
    (REC / 'A1-adapted-res.json').write_text(json.dumps([{'heading': H2, 'n': 2}], indent=1) + '\n', 'utf-8')

    # ---- A1 baseline: all 18 genuine readers, H2 carries its 2 findings
    build_fixtures(secs, {})
    emit(run_binder(('A1-baseline', H1)))

    # ---- A2 wrong sha
    build_fixtures(secs, {H1: 'sha'})
    emit(run_binder(('A2-wrong-sha', H1)))

    # ---- A3 wrong cand
    build_fixtures(secs, {H1: 'cand'})
    emit(run_binder(('A3-wrong-cand', H1)))

    # ---- A4 heading misspelled
    build_fixtures(secs, {H1: 'spell'})
    emit(run_binder(('A4-heading-spelled', H1)))

    # ---- A5 ceiling control: 3 findings > allowed 2
    build_fixtures(secs, {H2: 'three'})
    emit(run_binder(('A5-findings-over-ceiling', H2)))

    # ---- A6 laundering: finding-bearing reader emptied to []
    build_fixtures(secs, {H2: 'empty'})
    emit(run_binder(('A6-findings-emptied', H2)))

    # ---- restore
    git('checkout', '--', LEDGER)
    build_fixtures(secs, {})


if __name__ == '__main__':
    main()
