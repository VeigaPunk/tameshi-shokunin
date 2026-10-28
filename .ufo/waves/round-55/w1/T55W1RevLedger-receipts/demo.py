#!/usr/bin/env python3
"""Fixture demonstration of the round-18 credit rule + the round-54 binder contract.

Everything runs inside throwaway clones; every git call names -C <clone> and the
toplevel is asserted first. No lane file is written.
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
CLONE = S / 'demo-clone'
CF = S / 'demo-clone-nodrop'
OUT = []
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           PYTHONDONTWRITEBYTECODE='1')
RECORDS = ('SCORECARD.md', 'LOG.md', 'corpus/QUALITY.md', 'corpus/SOURCES.md',
           'tools/registry.json')


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


def r18(clone, rev=None):
    if rev is None:
        p = clone / '.ufo/evidence/round-18/measure.py'
        src = p.read_bytes()
    else:
        src = git(clone, 'show', '%s:.ufo/evidence/round-18/measure.py' % rev).stdout
    tmp = S / ('r18-%s.py' % (rev or 'wt')[:8])
    tmp.write_bytes(src)
    spec = importlib.util.spec_from_file_location('r18_%s' % tmp.stem, tmp)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def section(clone, rev, heading='## Standing rules'):
    raw = git(clone, 'show', '%s:SKILL.md' % rev).stdout
    m = r18(clone, rev)
    for s in m.sectionize(raw):
        if s['heading'] == heading:
            return s, hashlib.sha256(raw).hexdigest()
    raise SystemExit('no section ' + heading)


def write_reader(clone, rev, findings, tag, md=True, mutate=None, heading=None,
                 empty_md=False):
    sec, skill_sha = section(clone, rev)
    d = {'heading': heading or sec['heading'], 'cand': rev,
         'section_sha256': sec['sha256'],
         'seat': 'fixture', 'section': {'start': sec['start'], 'end': sec['end']},
         'skill_sha256': skill_sha}
    if findings == 'DEL':
        pass
    else:
        d['findings'] = findings
    if mutate:
        mutate(d)
    p = clone / '.ufo/waves/round-55/w1' / (tag + '.json')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=1) + '\n')
    if md:
        p.with_suffix('.md').write_text('' if empty_md else '# fixture reader %s\n' % tag)
    return p


def clear_readers(clone):
    d = clone / '.ufo/waves/round-55/w1'
    for p in list(d.glob('*.json')) + list(d.glob('*.md')):
        p.unlink()


def measure(clone, rev, label):
    run = subprocess.run([sys.executable, str(clone / '.ufo/evidence/round-21/coldread/measure.py'),
                          '--repo', str(clone), '--rev', rev],
                         capture_output=True, text=True, env=ENV, timeout=1800)
    d = json.loads(run.stdout)
    cr = d['coldread']
    sr = [s for s in cr['sections'] if s['heading'] == '## Standing rules'][0]
    say('%s rev=%s covered=%d/%d restraint=%s gate=%s ledger_committed=%s standing=%s'
        % (label, rev[:10], cr['sections_covered'], cr['sections_total'],
           d['calibration_restraint_score'], d['trace_gate'], d['ledger_committed'],
           json.dumps({k: sr[k] for k in ('credited', 'vetoed', 'reason')})))
    return d


def binder_source(clone, drops=None):
    src = clone / '.ufo/evidence/round-54/integrate/binder.py'
    text = src.read_text()
    if drops is not None:
        text = text.replace(
            "DROP = ('LOG.md', 'SCORECARD.md', 'SKILL.md', '.ufo/evidence/round-21/coldread/ledger.json')",
            drops)
    text = text.replace(
        "E = '.ufo/evidence/round-54'",
        "E = '.ufo/evidence/round-54'\n"
        "_rest = sys.argv[5:]\n"
        "_waves = None\n"
        "_label = 'L1 fixture re-key'\n"
        "_headings_file = None\n"
        "while _rest:\n"
        "    _f = _rest.pop(0)\n"
        "    if _f == '--headings':\n"
        "        _headings_file = _rest.pop(0)\n"
        "    elif _f == '--waves':\n"
        "        _waves = _rest.pop(0)\n"
        "    elif _f == '--label':\n"
        "        _label = _rest.pop(0)\n"
        "    else:\n"
        "        sys.exit('usage: binder.py LANE C0 PIN OUTDIR [--headings F] [--waves D] [--label T]')", 1)
    text = text.replace(
        "WAVE_DIRS = ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2')  # both waves; w2 carries the C1 reads\n",
        "WAVE_DIRS = ((_waves,) if _waves else ('.ufo/waves/round-54/w1', '.ufo/waves/round-54/w2'))\n")
    text = text.replace(
        "HEADINGS = json.loads(Path(LANE, E, 'c1/lost-headings-at-c0.json').read_text('utf-8'))",
        "HEADINGS = json.loads(Path(_headings_file).read_text('utf-8'))")
    text = text.replace(
        "BASE7 = json.loads(Path(LANE, E, 'c1/lost-headings-at-base.json').read_text('utf-8'))\n"
        "HEADINGS = sorted(set(HEADINGS) | set(BASE7))",
        "HEADINGS = sorted(set(HEADINGS))")
    text = text.replace("RES_PATH = Path(LANE, E, 'integrate/resolutions.json')",
                        "RES_PATH = Path(LANE, E, 'integrate/ABSENT-r55.json')")
    text = text.replace("'seats': [Path(f).stem, 'L1 TameshiR54a2 re-key (round 54)'],",
                        "'seats': [Path(f).stem, _label],")
    text = text.replace("'argv': [sys.executable, __file__, LANE, c0, pin, str(OUT), 'section', h],",
                        "'argv': [sys.executable] + list(sys.argv) + ['section', h],")
    return text


def bind(clone, c0, pin, out, headings, drops=None, tag='bind'):
    drv = S / ('binder-%s.py' % tag)
    drv.write_text(binder_source(clone, drops))
    hf = S / ('headings-%s.json' % tag)
    hf.write_text(json.dumps(headings))
    run = subprocess.run([sys.executable, str(drv), str(clone), c0, pin, str(out),
                          '--headings', str(hf), '--waves', '.ufo/waves/round-55/w1',
                          '--label', 'L1 fixture re-key'],
                         capture_output=True, text=True, env=ENV, timeout=2400)
    say('BIND[%s] rc=%d %s' % (tag, run.returncode,
                               run.stdout.strip().replace('\n', ' | ') or '(no stdout)'))
    if run.stderr.strip():
        say('BIND[%s] stderr: %s' % (tag, run.stderr.strip()[:500]))
    return run


def entries_at(clone, rev, heading='## Standing rules'):
    led = json.loads(git(clone, 'show', '%s:.ufo/evidence/round-21/coldread/ledger.json' % rev).stdout)
    return [e for e in led['entries'] if e.get('heading') == heading]


def main():
    start = '631cd6455e58dce969310b4c0466c3383d9f5108'
    for d in (CLONE, CF):
        if d.exists():
            shutil.rmtree(d)

    say('== fixtures: clone at the frozen base; C0 carries only the SKILL.md ## Standing rules edit ==')
    subprocess.run(['git', 'clone', '--shared', '--quiet', str(L), str(CLONE)], check=True, env=ENV)
    git(CLONE, 'checkout', '--detach', start)
    shutil.copyfile(L / 'SKILL.md', CLONE / 'SKILL.md')
    c0 = commit(CLONE, 'fixture C0: SKILL.md ## Standing rules edit only')
    sec0, skill0 = section(CLONE, c0)
    say('C0=%s section=%s skill_sha256=%s' % (c0, json.dumps(sec0), skill0))
    say('base-state ledger entries for the heading at C0: %d'
        % len(entries_at(CLONE, c0)))

    say('')
    say('== ARM A: findings: [] + sibling .md -> bound; DROP keeps the record files out ==')
    write_reader(CLONE, c0, [], 'T55W1RevLedger.reader', md=True)
    for name in RECORDS:
        p = CLONE / name
        p.write_text(p.read_text() + '\nfixture round-55 record edit\n')
    pin = commit(CLONE, 'fixture PIN: the round-55 record edits')
    say('PIN=%s' % pin)
    out = CLONE / ('.ufo/evidence/round-21/coldread/rekey-r55-%s' % c0[:12])
    bind(CLONE, c0, pin, out, ['## Standing rules'], tag='armA')
    rev1 = commit(CLONE, 'fixture REV1: bound ledger + trace committed')

    say('')
    say('== ARM B: SCORECARD.md edited AFTER the pin ==')
    p = CLONE / 'SCORECARD.md'
    p.write_text(p.read_text() + '\nfixture late record edit\n')
    rev2 = commit(CLONE, 'fixture REV2: SCORECARD.md edited after PIN')
    d1 = measure(CLONE, rev1, 'MEASURE rev1 (nothing moved after PIN)')
    d2 = measure(CLONE, rev2, 'MEASURE rev2 (SCORECARD.md moved after PIN)')

    say('')
    say('== ARM C: the binder refusals and the silent acceptances (one probe per state) ==')
    probes = [
        ('C1-no-md', [dict(findings=[], md=False, tag='probe')], 'json with no sibling .md'),
        ('C2-short-cand', [dict(findings=[], md=True, tag='probe',
                                mutate=lambda d: d.update(cand=d['cand'][:12]))],
         'cand a 12-hex prefix'),
        ('C3-stale-sha', [dict(findings=[], md=True, tag='probe',
                               mutate=lambda d: d.update(section_sha256='0' * 64))],
         'section_sha256 not the tree value'),
        ('C4-wrong-heading', [dict(findings=[], md=True, tag='probe',
                                   heading="### The service's limits — what tameshi refuses to mutation-test")],
         'clean reader for a heading not in HEADINGS'),
        ('C5-findings', [dict(findings=[{'quote': 'q', 'why': 'w'}], md=True, tag='probe')],
         'findings=1 with no resolutions file'),
        ('C6-no-findings-key', [dict(findings='DEL', md=True, tag='probe')],
         'reader json with NO findings key at all'),
        ('C7-wrong-skill-sha', [dict(findings=[], md=True, tag='probe',
                                     mutate=lambda d: d.update(skill_sha256='f' * 64))],
         'skill_sha256 not the whole-file value'),
        ('C8-empty-md', [dict(findings=[], md=True, tag='probe', empty_md=True)],
         'sibling .md present but zero bytes'),
        ('C9-dirty-sorts-first', [dict(findings=[{'quote': 'q', 'why': 'w'}], md=True, tag='a-dirty'),
                                  dict(findings=[], md=True, tag='z-clean')],
         'a dirty reader sorting before a clean one'),
        ('C10-clean-sorts-first', [dict(findings=[], md=True, tag='a-clean'),
                                   dict(findings=[{'quote': 'q', 'why': 'w'}], md=True, tag='z-dirty')],
         'a clean reader sorting before a dirty one'),
    ]
    for name, readers, why in probes:
        clear_readers(CLONE)
        for kw in readers:
            write_reader(CLONE, c0, **kw)
        out2 = CLONE / ('.ufo/evidence/round-21/coldread/probe-%s' % name)
        bind(CLONE, c0, pin, out2, ['## Standing rules'], tag=name)
        say('   probe %s :: %s' % (name, why))
        shutil.rmtree(out2, ignore_errors=True)
        git(CLONE, 'checkout', '--', '.ufo/evidence/round-21/coldread/ledger.json')

    say('')
    say('== ARM D: counterfactual DROP without SCORECARD.md/LOG.md ==')
    subprocess.run(['git', 'clone', '--shared', '--quiet', str(L), str(CF)], check=True, env=ENV)
    git(CF, 'checkout', '--detach', start)
    shutil.copyfile(L / 'SKILL.md', CF / 'SKILL.md')
    c0b = commit(CF, 'fixture counterfactual C0')
    clear_readers(CLONE)
    write_reader(CF, c0b, [], 'T55W1RevLedger.reader', md=True)
    for name in RECORDS:
        p = CF / name
        p.write_text(p.read_text() + '\nfixture round-55 record edit\n')
    pinb = commit(CF, 'fixture counterfactual PIN')
    outb = CF / ('.ufo/evidence/round-21/coldread/rekey-r55-%s' % c0b[:12])
    bind(CF, c0b, pinb, outb, ['## Standing rules'],
         drops="DROP = ('SKILL.md', '.ufo/evidence/round-21/coldread/ledger.json')",
         tag='armD')
    entb = [e for e in entries_at(CF, 'HEAD') if e.get('read_rev') == c0b]
    say('counterfactual entry keys that DROP would have removed: %s'
        % [p for p in ('LOG.md', 'SCORECARD.md') if entb and p in entb[0]['inputs']])
    rev1b = commit(CF, 'fixture counterfactual REV1')
    p = CF / 'SCORECARD.md'
    p.write_text(p.read_text() + '\nfixture late record edit\n')
    rev2b = commit(CF, 'fixture counterfactual REV2: SCORECARD.md after PIN')
    mb = r18(CF)
    for rev, tagv in ((rev1b, 'REV1'), (rev2b, 'REV2')):
        for e in entries_at(CF, rev):
            if e.get('read_rev') == c0b:
                say('COUNTERFACTUAL %s entry_reason=%s' % (tagv, mb.entry_reason(str(CF), rev, e, True)))
    measure(CF, rev1b, 'MEASURE counterfactual rev1')
    measure(CF, rev2b, 'MEASURE counterfactual rev2 (no DROP of SCORECARD.md)')

    say('')
    say('== ARM E: what the credit rule checks on the bound entry (field by field) ==')
    led1 = json.loads(git(CLONE, 'show', '%s:.ufo/evidence/round-21/coldread/ledger.json' % rev1).stdout)
    e1 = [e for e in led1['entries'] if e.get('heading') == '## Standing rules'
          and e.get('read_rev') == c0]
    if e1:
        e = e1[0]
        m = r18(CLONE, rev1)
        say('bound fields: %s' % json.dumps({k: e[k] for k in
            ('skill_sha256', 'start', 'end', 'sha256', 'class', 'verdict',
             'blocking_gaps', 'wrong_expectations', 'minor_gaps',
             'commands_executed_count', 'read_rev', 'traces', 'seats')}))
        say('inputs=%d dropped-keys-absent=%s external_inputs=%d'
            % (len(e['inputs']), [p for p in ('LOG.md', 'SCORECARD.md', 'SKILL.md')
                                  if p not in e['inputs']], len(e['external_inputs'])))
        say('entry_reason @rev1=%r  @rev2=%r'
            % (m.entry_reason(str(CLONE), rev1, e, True),
               m.entry_reason(str(CLONE), rev2, e, True)))
        # mutate read_rev to garbage: does credit care?
        e_bad = dict(e, read_rev='nonsense')
        say('entry_reason with read_rev="nonsense"=%r'
            % m.entry_reason(str(CLONE), rev1, e_bad, True))
        e_bad2 = dict(e, skill_sha256='f' * 64)
        say('entry_reason with skill_sha256=f*64=%r'
            % m.entry_reason(str(CLONE), rev1, e_bad2, True))
    (S / 'demo.out').write_text('\n'.join(OUT) + '\n')


if __name__ == '__main__':
    main()
