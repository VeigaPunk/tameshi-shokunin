#!/usr/bin/env python3
"""Round-51 controls: the cheapest trees that skip each claim's work, scored with the frozen counters at freeze bytes.

Usage: controls.py LANE FREEZE  (prints one CONTROL line per control; exit 0 iff every control scores as pre-registered)
Each control is a fixture clone of the lane at FREEZE under $HYAKU_SCRATCH/tameshi-r51/controls/<name>/tameshi-shokunin
(toplevel verified before its one commit, throwaway identity inside the fixture only), with one edit committed:
  C1  CTL_0        nothing changed                                     expect C1_R51_PASS=false
      CTL_S022     only S022 queued -> mined                           expect false (frontier rows stale)
      CTL_ALLHELD  a new frontier table, every row `held (round 51)`   expect false
      CTL_NOPTR    a new table with the expected statuses, no pointers expect false
      CTL_REWRITE  the old table cells rewritten in place (statuses, pointers, S022 fixed) expect false (readme_prefix=0)
  C2  CTL_0        nothing changed                                     expect C2_R51_PASS=false (recorded_cases=9)
      CTL_COMMENT  only a tenth ledger comment line                    expect false (wired_legs=9)
  C3  CTL_0        nothing changed                                     expect C3_R51_PASS=false
      CTL_TEMPLATE one uniform template row per frozen tool (`python3|bash tools/T --selftest`, verdict map
                   `0 clean; 1 failed`, pinned `tools/T`, scope `none`)  expect false
      CTL_HELP     the template with `--help` as the self-test         expect false
"""
import json
import os
import re
import shutil
import subprocess
import sys

LANE, FREEZE = os.path.realpath(sys.argv[1]), sys.argv[2]
E = '.ufo/evidence/round-51'
ROOT = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tameshi-r51', 'controls')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def run(argv, **k):
    return subprocess.run(argv, capture_output=True, env=ENV, **k)


def fixture(name, edit):
    d = os.path.join(ROOT, name, 'tameshi-shokunin')
    os.makedirs(os.path.dirname(d))
    assert run(['git', 'clone', '-q', '--shared', LANE, d]).returncode == 0
    assert run(['git', '-C', d, 'checkout', '-q', '--detach', FREEZE]).returncode == 0
    top = run(['git', '-C', d, 'rev-parse', '--show-toplevel']).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), 'fixture toplevel mismatch'
    if edit:
        edit(d)
        assert run(['git', '-C', d, 'add', '-A']).returncode == 0
        r = run(['git', '-C', d, '-c', 'user.name=control', '-c', 'user.email=control@invalid', 'commit', '-qm', name])
        assert r.returncode == 0, r.stderr
    return d


def counter(k, d, name):
    code = os.path.join(LANE, E, k, 'measure.py')  # the frozen bytes: the caller runs this at FREEZE (clean tree)
    argv = [sys.executable, code, '--lane', d, '--rev', 'HEAD']
    if k in ('c2', 'c3'):
        w = os.path.join(ROOT, name, 'work-' + k)
        os.makedirs(w)
        argv += ['--work', w]
    r = run(argv, env=dict(ENV, TMPDIR=os.path.join(ROOT, name)))
    return r.returncode, r.stdout.decode(errors='replace').strip().split('\n')[-1]


def readme_append(d, text):
    with open(os.path.join(d, 'corpus/README.md'), 'a', encoding='utf-8') as fh:
        fh.write(text)


def s022(d):
    p = os.path.join(d, 'corpus/SOURCES.md')
    s = open(p, encoding='utf-8').read()
    old = '| queued | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |'
    assert s.count(old) == 1
    open(p, 'w', encoding='utf-8').write(s.replace(old, '| mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |'))


EXP = json.load(open(os.path.join(LANE, E, 'c1/frontier-expected.json')))['rows']
PTR = {'F1': '413', 'F2': '115', 'F3': '589', 'F4': '492-493', 'F5': '330', 'F6': '608', 'F7': '589', 'F8': '424',
       'F9': '86', 'F10': '599'}
HDR = '\n\n| id | ground | candidate sources | status | next falsifiable move (before → after) |\n|---|---|---|---|---|\n'


def status_text(k, ptr=True):
    w = EXP[k]
    s = w['status'] + ('' if w['round'] is None else ' (round %d)' % w['round'])
    return s + (' — README.md:%s' % PTR[k] if ptr else '')


def allheld(d):
    readme_append(d, HDR + ''.join('| %s | x | x | held (round 51) — README.md:599 | x |\n' % k for k in EXP))


def noptr(d):
    s022(d)
    readme_append(d, HDR + ''.join('| %s | x | x | %s | x |\n' % (k, status_text(k, False)) for k in EXP))


def rewrite(d):
    s022(d)
    p = os.path.join(d, 'corpus/README.md')
    lines = open(p, encoding='utf-8').read().split('\n')
    for i in range(75, 87):
        m = re.match(r'^\| (F\d+) \|', lines[i])
        if m:
            c = lines[i].split(' | ')
            c[3] = status_text(m.group(1))
            lines[i] = ' | '.join(c)
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))


def comment(d):
    p = os.path.join(d, 'tools/mutate-and-run.sh')
    s = open(p, encoding='utf-8').read()
    anchor = '#   js-cite-check         kumitate-shokunin/scripts/cite-check.mjs    5/10 (50 %)\n'
    assert s.count(anchor) == 1
    open(p, 'w', encoding='utf-8').write(s.replace(anchor, anchor + '#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          5/10 (50 %)\n'))


def template(flag):
    def edit(d):
        tools = json.load(open(os.path.join(d, E, 'c3/tools-base.json')))['tools']
        rows = ''
        for t in tools:
            interp = 'bash' if t.endswith('.sh') else 'python3'
            rows += '| %s | gate | `%s %s` | 0 clean; 1 failed | `%s %s %s` | `%s` | none | tameshi |\n' % (
                t, interp, t, interp, t, flag, t)
        p = os.path.join(d, 'SKILL.md')
        s = open(p, encoding='utf-8').read()
        anchor = '| bash declared-witness study | probe |'
        i = s.index(anchor)
        j = s.index('\n', i) + 1
        open(p, 'w', encoding='utf-8').write(s[:j] + rows + s[j:])
    return edit


PLAN = [
    ('c1', 'CTL_0', None), ('c1', 'CTL_S022', s022), ('c1', 'CTL_ALLHELD', allheld), ('c1', 'CTL_NOPTR', noptr),
    ('c1', 'CTL_REWRITE', rewrite),
    ('c2', 'CTL_0', None), ('c2', 'CTL_COMMENT', comment),
    ('c3', 'CTL_0', None), ('c3', 'CTL_TEMPLATE', template('--selftest')), ('c3', 'CTL_HELP', template('--help')),
]


def main():
    shutil.rmtree(ROOT, ignore_errors=True)
    os.makedirs(ROOT)
    bad = 0
    try:
        for k, name, edit in PLAN:
            tag = '%s-%s' % (k, name)
            d = fixture(tag, edit)
            rc, last = counter(k, d, tag)
            ok = rc == 1 and last.endswith('_PASS=false')
            bad += 0 if ok else 1
            print('CONTROL %s %s: exit=%d %s -> %s' % (k.upper(), name, rc, last, 'as-pre-registered' if ok else 'UNEXPECTED'))
            sys.stdout.flush()
    finally:
        shutil.rmtree(ROOT, ignore_errors=True)
    print('CONTROLS: total=%d unexpected=%d' % (len(PLAN), bad))
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
