#!/usr/bin/env python3
"""Round-52 controls: score the frozen C1/C2 counters on control trees built from BASE, before any seat runs.

Usage: controls.py LANE OUTDIR     (scratch: $HYAKU_SCRATCH/tameshi-r52/controls, removed on exit)
Each control is a commit in a `git clone --shared` scratch clone of LANE at BASE (fixture identity, `git -C` the
clone only, toplevel checked before the first commit). Prints `CONTROL <id> expect=<true|false> got=<…> -> <as-pre-registered|UNEXPECTED>`
and `CONTROLS: total=N unexpected=U`; exit 0 iff U == 0. Pre-registered expectations are the EXPECT table below.
C1 controls run in parallel (each is a full registry-check plus the round-51 C3 counter).
"""
import json, os, re, shutil, subprocess, sys

BASE = 'ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4'
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.dirname(HERE)
EXPECT = {
    'C1_CTL_0': False,          # do nothing
    'C1_CTL_STALE': False,      # round21-measure fixed, mte row still 9/9
    'C1_CTL_SUPERSEDE': False,  # dodge: supersede the stale row, add a new 10/10 row under another name
    'C1_CTL_NEEDLE': False,     # dodge: drop the row's stdout needle (exit-only row passes)
    'C1_CTL_STUB': False,       # dodge: row fixed, round21-measure replaced by a stub printing a pass line
    'C1_CTL_POSITIVE': True,    # reachability: round21-measure fix + row 10/10
    'C2_CTL_0': False,          # do nothing
    'C2_CTL_DELETE': False,     # dodge: delete the stale statements instead of correcting them
    'C2_CTL_ZERO': False,       # text fixed; 20 correction records with zero findings (repeats defect 3)
    'C2_CTL_FORGE': False,      # text fixed; corrections whose quotes are not in the reader files
    'C2_CTL_POSITIVE': True,    # reachability: text fixed; floors quoted for Read20/Read01, others zero (cannot_see)
}
R21_FIX_OLD = 'str(ROOT.parent / surface["repo"])'
R21_FIX_NEW = 'str(fleet / surface["repo"])'
R21_FIX_DEF_AT = '        surfaces = []\n'
R21_FIX_DEF = ('        fleet = Path(re.search(r\'^FLEET = Path\\("([^"]+)"\\)$\',\n'
               '                               (EVIDENCE / SCRIPTS["c2"]).read_text(), re.M).group(1))\n')


def sh(*a, **k):
    return subprocess.run(list(a), check=True, capture_output=True, text=True, **k).stdout


def edit(d, path, fn):
    p = os.path.join(d, path)
    s = open(p, encoding='utf-8').read()
    t = fn(s)
    if t == s:
        raise SystemExit('control edit did not change %s' % path)
    open(p, 'w', encoding='utf-8').write(t)


def r21_fix(s):
    s = s.replace('import os\n', 'import os\nimport re\n', 1).replace(R21_FIX_OLD, R21_FIX_NEW)
    return s.replace(R21_FIX_DEF_AT, R21_FIX_DEF + R21_FIX_DEF_AT, 1)


def reg_rows(fn):
    def f(s):
        d = json.loads(s)
        fn(d['rows'])
        return json.dumps(d, indent=2, ensure_ascii=False) + '\n'
    return f


def row10(rows):
    r = next(x for x in rows if x['name'] == 'mte-interop-check')
    r['expect']['stdout_contains'] = ['MTE_INTEROP: PASS legs_conforming=10/10']


def supersede(rows):
    r = next(x for x in rows if x['name'] == 'mte-interop-check')
    new = json.loads(json.dumps(r)); new['name'] = 'mte-interop-check-r52'
    new['expect']['stdout_contains'] = ['MTE_INTEROP: PASS legs_conforming=10/10']
    r['status'] = 'superseded'; r['superseded_by'] = 'mte-interop-check-r52'
    rows.append(new)


def needle(rows):
    r = next(x for x in rows if x['name'] == 'mte-interop-check')
    r['expect'].pop('stdout_contains')


def skill_fix(s):
    s = s.replace('the nine ledger legs', 'the ten ledger legs', 1)
    s = s.replace('`mte-interop-check` (9/9)', '`mte-interop-check` (10/10)', 1)
    s = s.replace('tools/mutate-and-run.sh:425`', 'tools/mutate-and-run.sh:434`', 1)
    s = s.replace('tools/mutate-and-run.sh:569-574`', 'tools/mutate-and-run.sh:579-583`', 1)
    s = s.replace('  `/tmp/tameshi-r4-2-regression.XXXXXX` after', '  `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` after', 1)
    lines = s.split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith('| fleet mutation runner |'):
            lines[i] = ln.replace('under /tmp', 'under ${TMPDIR:-/tmp}')
    return '\n'.join(lines)


def skill_delete(s):
    s = s.replace(', leg set not equal to the nine ledger legs', '', 1)
    s = s.replace(' (the maintained driver also prints the failing count: `tools/mutate-and-run.sh:425`)', '', 1)
    s = s.replace('the maintained driver divides by every defect and marks the run DEGRADED: `tools/mutate-and-run.sh:569-574`', 'the maintained driver divides by every defect', 1)
    return '\n'.join(ln for ln in s.split('\n') if not ln.startswith('| fleet mutation runner |'))


KILL_NOTE = ('\n- **Round-52 supersession (cell, not edit).** The §3 queue row `drift-pins` (`:119`) said "unmeasured by sweep"; '
             'round 51 measured it as case 10 (kill rate 2/10, `.ufo/evidence/round-51/c2/sweep/sweep.txt`), which supersedes that cell.\n')


def corrections(d, lane, mode):
    led_path = os.path.join(d, '.ufo/evidence/round-21/coldread/ledger.json')
    led = json.load(open(led_path))
    out = []
    for e in led['entries']:
        if not str(e.get('read_rev', '')).startswith('02ec217c'):
            continue
        seat = next(s for s in e['seats'] if s.startswith('T51W2Read'))
        rf = '.ufo/evidence/round-51/coldread/reads/%s.md' % seat
        text = open(os.path.join(d, rf), encoding='utf-8').read()
        findings = []
        if mode == 'positive':
            labels = {'T51W2Read20': ['**HIGH-1', '**HIGH-2', '**MED-1', '**MED-2'],
                      'T51W2Read01': ['`tools/mutate-and-run.sh:425`', '`tools/mutate-and-run.sh:569-574`']}.get(seat, [])
            for lab in labels:
                ln = next(l for l in text.split('\n') if lab in l)
                findings.append({'quote': ln.strip()[:200]})
        elif mode == 'forge':
            findings = [{'quote': 'HIGH-1 HIGH-2 MED-1 MED-2 :425 :569-574 forged finding text'}]
        out.append({'heading': e['heading'], 'read_rev': e['read_rev'], 'reader': seat, 'reader_file': rf,
                    'wrong_expectations': len(findings), 'findings': findings})
    led['corrections'] = out
    open(led_path, 'w').write(json.dumps(led, indent=1) + '\n')


def main():
    lane, outdir = sys.argv[1], sys.argv[2]
    scr = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r52', 'controls')
    shutil.rmtree(scr, ignore_errors=True); os.makedirs(scr)
    try:
        # amendment 1: the clone sits in a fleet mirror (one symlink per *-shokunin sibling of the lane), because
        # registry-check builds its own mirror from --root's parent and several rows read siblings through it
        fleet = os.path.join(scr, 'fleet'); os.makedirs(fleet)
        lane_real = os.path.realpath(lane)
        for name in sorted(os.listdir(os.path.dirname(lane_real))):
            src = os.path.join(os.path.dirname(lane_real), name)
            if name.endswith('-shokunin') and os.path.realpath(src) != lane_real:
                os.symlink(src, os.path.join(fleet, name))
        d = os.path.join(fleet, os.path.basename(lane_real))
        sh('git', 'clone', '-q', '--shared', lane, d)
        if os.path.realpath(sh('git', '-C', d, 'rev-parse', '--show-toplevel').strip()) != os.path.realpath(d):
            raise SystemExit('toplevel mismatch')
        ident = ['-c', 'user.name=r52-control', '-c', 'user.email=r52-control@scratch.invalid']
        revs = {}
        def build(name, steps):
            sh('git', '-C', d, 'checkout', '-q', '--detach', BASE)
            for path, fn in steps:
                if callable(path):
                    path(d)
                else:
                    edit(d, path, fn)
            if steps:
                sh('git', '-C', d, *ident, 'commit', '-qam', name)
            revs[name] = sh('git', '-C', d, 'rev-parse', 'HEAD').strip()
            # amendment 1: evidence-disposition rows refuse a detached HEAD on no branch; give each control a branch
            sh('git', '-C', d, 'branch', '-f', 'ctl-' + name.lower().replace('_', '-'), revs[name])
        R21 = ('tools/round21-measure.py', r21_fix)
        REG = 'tools/registry.json'
        build('C1_CTL_0', [])
        build('C1_CTL_STALE', [R21])
        build('C1_CTL_SUPERSEDE', [R21, (REG, reg_rows(supersede))])
        build('C1_CTL_NEEDLE', [R21, (REG, reg_rows(needle))])
        build('C1_CTL_STUB', [(REG, reg_rows(row10)), ('tools/round21-measure.py',
              lambda s: 'import sys\nprint("ROUND21_MEASURE_SELFTEST: 11/11 pass")\nsys.exit(0)\n')])
        build('C1_CTL_POSITIVE', [R21, (REG, reg_rows(row10))])
        SK = ('SKILL.md', skill_fix)
        KL = ('corpus/knowledge/fleet-kill-rate-ledger.md', lambda s: s + KILL_NOTE)
        build('C2_CTL_0', [])
        build('C2_CTL_DELETE', [('SKILL.md', skill_delete),
              ('corpus/knowledge/fleet-kill-rate-ledger.md', lambda s: '\n'.join(l for l in s.split('\n') if not l.startswith('| drift-pins |')))])
        build('C2_CTL_ZERO', [SK, KL, (lambda dd: corrections(dd, lane, 'zero'), None)])
        build('C2_CTL_FORGE', [SK, KL, (lambda dd: corrections(dd, lane, 'forge'), None)])
        build('C2_CTL_POSITIVE', [SK, KL, (lambda dd: corrections(dd, lane, 'positive'), None)])
        procs = {}
        for name, rev in revs.items():
            if name.startswith('C1'):
                w = os.path.join(scr, 'work-' + name); os.makedirs(w)
                procs[name] = subprocess.Popen([sys.executable, os.path.join(E, 'c1/measure.py'), '--lane', d,
                                                '--rev', rev, '--work', w, '--explain'],
                                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                               env=dict(os.environ, TMPDIR=w))
            else:
                procs[name] = subprocess.Popen([sys.executable, os.path.join(E, 'c2/measure.py'), '--lane', d,
                                                '--rev', rev, '--explain'],
                                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        unexpected = 0
        for name in EXPECT:
            out, _ = procs[name].communicate()
            open(os.path.join(outdir, name + '.stdout'), 'w').write('rev=%s\n%s' % (revs[name], out))
            m = re.search(r'_R52_PASS=(true|false)', out)
            got = m.group(1) if m else 'none'
            ok = got == ('true' if EXPECT[name] else 'false')
            unexpected += 0 if ok else 1
            last = out.strip().split('\n')[-1] if out.strip() else ''
            print('CONTROL %s expect=%s got=%s -> %s | %s' % (name, str(EXPECT[name]).lower(), got,
                  'as-pre-registered' if ok else 'UNEXPECTED', last[:260]), flush=True)
        print('CONTROLS: total=%d unexpected=%d' % (len(EXPECT), unexpected))
        return 0 if unexpected == 0 else 1
    finally:
        shutil.rmtree(scr, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
