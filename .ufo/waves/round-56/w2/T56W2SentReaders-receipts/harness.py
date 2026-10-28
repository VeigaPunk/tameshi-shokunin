#!/usr/bin/env python3
"""T56W2SentReaders: attack the round-56 bind path.

Synthetic clone at C0, synthetic wave dir with 18 reader reports, then five
required tamper scenarios (+ residual scenarios). For each: run the wave-1
validator (validate-readers.py) and the round-55 binder (binder-r55.py) and
record exit codes, refusal lines and binder SKIP lines.

Never mutates the lane; every clone is a fixture under scratch.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
C0 = 'c0137451f5b7f22d65f748fc69f1b181f55e1378'
BASE = '981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1'
VALIDATOR = LANE / '.ufo/waves/round-56/validate-readers.py'
BINDER = LANE / '.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py'
HEADINGS_FILE = LANE / '.ufo/evidence/round-56/c1/lost-headings-at-base.json'
S = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'tameshi-r56/T56W2SentReaders'
RESULTS = Path(sys.argv[1]) if len(sys.argv) > 1 else S / 'results.json'

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def git(repo, *args, check=True):
    r = subprocess.run(['git', '-C', str(repo)] + list(args), env=ENV,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (args, r.stderr))
    return r


def show(repo, rev, path):
    r = git(repo, 'show', '%s:%s' % (rev, path), check=False)
    return r.stdout if r.returncode == 0 else None


def load_sectionize(repo, rev, work):
    raw = show(repo, rev, '.ufo/evidence/round-18/measure.py').encode('utf-8', 'surrogateescape')
    p = work / 'r18.py'
    p.write_bytes(raw)
    spec = importlib.util.spec_from_file_location('r18_%d' % abs(hash(str(p))), str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, hashlib.sha256(raw).hexdigest()


HEADINGS = json.loads(HEADINGS_FILE.read_text('utf-8'))
SECTIONS = {}


def clone(name):
    d = S / ('clone-' + name)
    if d.exists():
        shutil.rmtree(d)
    subprocess.run(['git', 'clone', '--shared', '--quiet', str(LANE), str(d)],
                   env=ENV, check=True, capture_output=True, text=True)
    top = git(d, 'rev-parse', '--show-toplevel').stdout.strip()
    assert top == str(d), (top, str(d))
    git(d, 'checkout', '--detach', '--quiet', C0)
    assert git(d, 'rev-parse', 'HEAD').stdout.strip() == C0
    return d


def wave_dir(repo):
    return repo / '.ufo/waves/round-56/w2'


def seat_name(i):
    return 'T56W2Read%02d' % (i + 1)


def report_for(i, heading, sha, cand=C0, findings=None, commands=None, name=None):
    return {
        'heading': heading,
        'cand': cand,
        'section_sha256': sha,
        'findings': [] if findings is None else findings,
        'commands': commands if commands is not None else
                    ['grep -n -- "%s" SKILL.md' % heading],
        'notes': ['synthetic report for the bind-path attack harness'],
        'verdict': 'verified-record',
    }


def md_for(heading, commands=None):
    commands = commands if commands is not None else ['grep -n -- "%s" SKILL.md' % heading]
    return '# %s\n\nCold read at C0.\n\nCommand: %s\n' % (heading, commands[0] if commands else '')


def write_report(d, name, data, md_text=None, with_md=True):
    (d / (name + '.json')).write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n',
                                      encoding='utf-8')
    if with_md:
        (d / (name + '.md')).write_text(md_text, encoding='utf-8')
    else:
        p = d / (name + '.md')
        if p.exists():
            p.unlink()


def commit(repo, msg):
    git(repo, 'add', '-A')
    git(repo, '-c', 'user.name=harness', '-c', 'user.email=harness@example.invalid',
        'commit', '--quiet', '-m', msg)
    return git(repo, 'rev-parse', 'HEAD').stdout.strip()


def run_validator(repo, rev, work):
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    r = subprocess.run([sys.executable, str(VALIDATOR), '--lane', str(repo),
                        '--rev', rev, '--c0', C0, '--work', str(work), '--explain'],
                       env=ENV, capture_output=True, text=True)
    return r


def run_binder(repo, out, tmpdir):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    tmpdir.mkdir(parents=True, exist_ok=True)
    e = dict(ENV, TMPDIR=str(tmpdir))
    r = subprocess.run([sys.executable, str(BINDER), str(repo), C0, C0, str(out),
                        '--headings', str(HEADINGS_FILE),
                        '--waves', '.ufo/waves/round-56/w2',
                        '--resolutions', '/nonexistent/round-56-resolutions.json',
                        '--label', 'T56W2SentReaders harness'],
                       env=e, capture_output=True, text=True)
    return r


def summarize(tag, repo, rev, notes):
    """Run validator + binder on the fixture, return a structured result."""
    v = run_validator(repo, rev, S / ('work-' + tag))
    b = run_binder(repo, S / ('out-' + tag), S / ('tmp-' + tag))
    vlines = v.stdout.splitlines()
    blines = b.stdout.splitlines()
    skips = [l for l in blines if l.startswith('SKIP ')]
    rekeys = [l for l in blines if l.startswith('REKEY ')]
    tail = [l for l in blines if l.startswith('REFRESH ')]
    ledger = json.loads((repo / '.ufo/evidence/round-21/coldread/ledger.json').read_text('utf-8'))
    bound = {}
    for e in ledger['entries']:
        if isinstance(e, dict) and e.get('heading') in HEADINGS:
            for t in (e.get('traces') or []):
                if 'rekey-r56-' in t:
                    bound.setdefault(e['heading'], []).append(
                        {'read_rev': e.get('read_rev'), 'sha256': (e.get('sha256') or '')[:12],
                         'verdict': e.get('verdict'), 'minor_gaps': e.get('minor_gaps'),
                         'reports': e.get('reports'), 'seats': e.get('seats')})
    return {
        'tag': tag, 'rev': rev, 'notes': notes,
        'validator_rc': v.returncode, 'validator_refusals': [l for l in vlines if l.startswith('REFUSE')],
        'validator_warnings': [l for l in vlines if l.startswith('WARN')],
        'validator_verdict': vlines[-1] if vlines else '',
        'binder_rc': b.returncode, 'binder_skips': skips, 'binder_rekeys': len(rekeys),
        'binder_tail': tail, 'binder_stderr': b.stderr[-400:],
        'bound_headings': {k[:60]: v for k, v in bound.items()},
        'bound_count': len(bound),
    }


def main():
    S.mkdir(parents=True, exist_ok=True)
    work = S / 'sec'
    work.mkdir(exist_ok=True)
    mod, digest = load_sectionize(LANE, C0, work)
    raw = show(LANE, C0, 'SKILL.md').encode('utf-8', 'surrogateescape')
    for sec in mod.sectionize(raw):
        SECTIONS[sec['heading']] = sec
    missing = [h for h in HEADINGS if h not in SECTIONS]
    print('frozen-sectionize sha256=%s sections=%d missing=%s'
          % (digest[:12], len(SECTIONS), missing))

    results = {'c0': C0, 'base': BASE, 'r18_sha256': digest, 'scenarios': []}

    def base_state(repo, tamper=None, drop_md=(), extra=None):
        d = wave_dir(repo)
        d.mkdir(parents=True, exist_ok=True)
        for i, h in enumerate(HEADINGS):
            sha = SECTIONS[h]['sha256']
            name = seat_name(i)
            data = report_for(i, h, sha)
            if tamper:
                data, name, drop = tamper(i, h, sha, data, name)
            else:
                drop = False
            write_report(d, name, data, md_for(h), with_md=(name not in drop_md and not drop))
        if extra:
            for nm, (dat, mdt) in extra.items():
                write_report(d, nm, dat, mdt)

    # ---------------- S0 baseline ----------------
    repo = clone('s0')
    base_state(repo)
    rev = commit(repo, 'S0 baseline 18 reader reports at C0')
    results['scenarios'].append(summarize('s0-baseline', repo, rev, 'control: all-valid'))

    # ---------------- S1 cand = base rev ----------------
    repo = clone('s1')
    base_state(repo, tamper=lambda i, h, sha, d, n: (
        dict(d, cand=BASE), n, False) if i == 0 else (d, n, False))
    rev = commit(repo, 'S1 cand=base')
    results['scenarios'].append(summarize('s1-cand-base', repo, rev,
        'heading[0] JSON carries the correct section_sha256 but cand=base revision'))

    # ---------------- S2 correct JSON, no .md ----------------
    repo = clone('s2')
    base_state(repo, drop_md=(seat_name(0),))
    rev = commit(repo, 'S2 no md')
    results['scenarios'].append(summarize('s2-no-md', repo, rev,
        'heading[0] JSON is fully correct but its .md sibling is absent'))

    # ---------------- S3 hash copied from a sibling section ----------------
    repo = clone('s3')
    sib = SECTIONS[HEADINGS[1]]['sha256']
    base_state(repo, tamper=lambda i, h, sha, d, n: (
        dict(d, section_sha256=sib), n, False) if i == 0 else (d, n, False))
    rev = commit(repo, 'S3 sibling hash')
    results['scenarios'].append(summarize('s3-sibling-hash', repo, rev,
        'heading[0] JSON names the right heading but carries heading[1] sha256 '
        '(section never read)'))

    # ---------------- S4 findings is a string ----------------
    repo = clone('s4')
    base_state(repo, tamper=lambda i, h, sha, d, n: (
        dict(d, findings='looks fine to me'), n, False) if i == 0 else (d, n, False))
    rev = commit(repo, 'S4 findings string')
    results['scenarios'].append(summarize('s4-findings-string', repo, rev,
        'heading[0] JSON has findings as a string, not a list'))

    # ---------------- S4b findings is an empty string ----------------
    repo = clone('s4b')
    base_state(repo, tamper=lambda i, h, sha, d, n: (
        dict(d, findings=''), n, False) if i == 0 else (d, n, False))
    rev = commit(repo, 'S4b findings empty string')
    results['scenarios'].append(summarize('s4b-findings-empty-string', repo, rev,
        'heading[0] JSON has findings as the empty string'))

    # ---------------- S5 two JSONs, same heading, different hashes ----------------
    repo = clone('s5')
    base_state(repo)
    d = wave_dir(repo)
    h0 = HEADINGS[0]
    write_report(d, seat_name(0) + 'b',
                 dict(report_for(0, h0, SECTIONS[HEADINGS[1]]['sha256'])),
                 md_for(h0))
    rev = commit(repo, 'S5 two reports one heading')
    results['scenarios'].append(summarize('s5-duplicate-heading', repo, rev,
        'two JSONs for heading[0]: %s.json (correct) and %sb.json (sibling hash)'
        % (seat_name(0), seat_name(0))))

    # ---------------- R1 md present but empty ----------------
    repo = clone('r1')
    base_state(repo)
    (wave_dir(repo) / (seat_name(0) + '.md')).write_text('', encoding='utf-8')
    rev = commit(repo, 'R1 empty md')
    results['scenarios'].append(summarize('r1-empty-md', repo, rev,
        'heading[0] .md exists but is empty (binder checks existence only)'))

    # ---------------- R2 commands empty ----------------
    repo = clone('r2')
    base_state(repo, tamper=lambda i, h, sha, d, n: (
        dict(d, commands=[]), n, False) if i == 0 else (d, n, False))
    rev = commit(repo, 'R2 commands empty')
    results['scenarios'].append(summarize('r2-commands-empty', repo, rev,
        'heading[0] JSON carries no commands at all'))

    # ---------------- R3 a JSON the validator never sees (name outside the glob) ----
    repo = clone('r3')
    base_state(repo)
    d = wave_dir(repo)
    h0 = HEADINGS[0]
    write_report(d, 'AA-binder-pick',
                 dict(report_for(0, h0, SECTIONS[h0]['sha256']), commands=[]),
                 '')
    rev = commit(repo, 'R3 unvalidated json sorts first')
    results['scenarios'].append(summarize('r3-unvalidated-json', repo, rev,
        'AA-binder-pick.json carries heading[0] correctly but its name does not match '
        'the validator glob (T56W*Read*.json) and it sorts first for the binder'))

    # ---------------- R4 TOCTOU: validator reads committed, binder reads the tree --
    repo = clone('r4')
    base_state(repo)
    rev = commit(repo, 'R4 committed good')
    v = run_validator(repo, rev, S / 'work-r4-pre')
    d = wave_dir(repo)
    (d / (seat_name(0) + '.json')).write_text(json.dumps(
        dict(report_for(0, HEADINGS[0], SECTIONS[HEADINGS[0]]['sha256']), commands=[]),
        indent=1), encoding='utf-8')
    (d / (seat_name(0) + '.md')).write_text('', encoding='utf-8')
    res = summarize('r4-toctou', repo, rev,
        'validator PASSes the committed report, then the working-tree copy is tampered; '
        'the binder reads the working tree')
    res['validator_pre_tamper_rc'] = v.returncode
    res['validator_pre_tamper_verdict'] = v.stdout.splitlines()[-1] if v.stdout else ''
    results['scenarios'].append(res)

    RESULTS.write_text(json.dumps(results, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    for s in results['scenarios']:
        print('== %s: validator_rc=%d %s' % (s['tag'], s['validator_rc'], s['validator_verdict']))
        print('   binder_rc=%d rekeys=%d bound=%d skips=%s'
              % (s['binder_rc'], s['binder_rekeys'], s['bound_count'], s['binder_skips'][:3]))
        for r in s['validator_refusals'][:6]:
            print('   REF %s' % r[:160])
    print('results -> %s' % RESULTS)


if __name__ == '__main__':
    main()
