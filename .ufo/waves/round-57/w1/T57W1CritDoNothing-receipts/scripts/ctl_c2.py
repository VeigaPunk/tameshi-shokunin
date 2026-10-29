#!/usr/bin/env python3
"""Do-nothing controls for the round-57 C2 counter (scratch only; never writes the lane).

Each control = clone of the lane at BASE + commit A (the staged C2 counter and its mutants.json, copied
byte-identically) + commit B (the control edit). The counter then runs at B with --explain.
"""
import json
import os
import re
import shutil
import subprocess
import sys

S = os.environ['S']
LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '5e3569969b532310d2b8a3d130901757a3df356b'
WAVE = LANE + '/.ufo/waves/round-57/w1'
CTR = WAVE + '/T57W1ExecC2Counter/stage/.ufo/evidence/round-57/c2/measure.py'
MUT = WAVE + '/T57W1ExecC2Counter/stage/.ufo/evidence/round-57/c2/mutants.json'
IDENT = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid']
HW = '.ufo/evidence/round-57/c2/hardwired'
TOKEN = re.compile(r'RECEIPT_[A-Z_]*[A-Z]')
SECTION = re.compile(r'^## Standing rules[ \t]*\n(.*?)(?=^## |\Z)', re.M | re.S)
GATE = 'python3 tools/receipt-revision-gate.py'


def git(repo, *a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, check=True)


def make_clone(name):
    dest = os.path.join(S, 'c2', name)
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, dest], check=True, capture_output=True)
    git(dest, 'checkout', '-q', '--detach', BASE)
    assert git(dest, 'rev-parse', '--show-toplevel').stdout.decode().strip() == os.path.realpath(dest)
    return dest


def commit(repo, msg):
    git(repo, 'add', '-A')
    subprocess.run(['git', '-C', repo] + IDENT + ['commit', '-q', '--allow-empty', '-m', msg], check=True,
                   capture_output=True)
    return git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()


def stage(repo):
    d = os.path.join(repo, '.ufo/evidence/round-57/c2')
    os.makedirs(d, exist_ok=True)
    shutil.copyfile(CTR, os.path.join(d, 'measure.py'))
    shutil.copyfile(MUT, os.path.join(d, 'mutants.json'))
    fx = os.path.join(repo, HW)
    os.makedirs(fx, exist_ok=True)
    body = 'VERDICT: rev=%s C1_X_PASS=true\n' % BASE
    for n in ('positive.txt', 'refused-mismatch.txt'):
        open(os.path.join(fx, n), 'w').write(body)
    return commit(repo, 'control: staged C2 counter, mutants.json and hard-wired receipts')


def row(name, argv, expect):
    return {'name': name, 'kind': 'gate', 'argv': argv, 'expect': expect, 'timeout_s': 60,
            'source': 'SKILL.md@' + BASE + ':1541', 'status': 'active', 'tags': ['new-r57-control']}


def hard_rows():
    pos = HW + '/positive.txt:positive'
    mis = HW + '/refused-mismatch.txt:verdict'
    return [
        row('gate-hardwired-positive', ['python3', 'tools/receipt-revision-gate.py', '--lane', '.', '--certified',
                                        BASE, '--receipt', pos], {'exit': 0, 'stdout_contains': ['verdict=PASS']}),
        row('gate-hardwired-unresolvable', ['python3', 'tools/receipt-revision-gate.py', '--lane', '.',
                                            '--certified', 'deadbeefdeaddead', '--receipt', pos],
            {'exit': 2, 'stdout_contains': ['RECEIPT_REV_UNRESOLVABLE']}),
        row('gate-hardwired-mismatch', ['python3', 'tools/receipt-revision-gate.py', '--lane', '.', '--certified',
                                        'HEAD', '--receipt', mis],
            {'exit': 3, 'stdout_contains': ['RECEIPT_REV_MISMATCH']}),
    ]


def help_rows(expect_honest=False):
    pos = HW + '/positive.txt:positive'
    base_argv = ['python3', 'tools/receipt-revision-gate.py', '--help', '--receipt', pos]
    if expect_honest:
        return [row('gate-help-%d' % i, list(base_argv), {'exit': 1}) for i in range(3)]
    return [
        row('gate-help-positive', list(base_argv), {'exit': 0, 'stdout_contains': ['verdict=PASS']}),
        row('gate-help-unresolvable', list(base_argv), {'exit': 2, 'stdout_contains': ['RECEIPT_REV_UNRESOLVABLE']}),
        row('gate-help-drift', list(base_argv), {'exit': 3, 'stdout_contains': ['RECEIPT_REV_CONTENT_DRIFT']}),
    ]


def add_rows(repo, rows):
    p = os.path.join(repo, 'tools/registry.json')
    doc = json.load(open(p, encoding='utf-8'))
    doc['rows'] = doc['rows'] + rows
    open(p, 'w', encoding='utf-8').write(json.dumps(doc, indent=2, ensure_ascii=False) + '\n')


def strip_tokens(repo):
    p = os.path.join(repo, 'SKILL.md')
    text = open(p, encoding='utf-8').read()
    m = SECTION.search(text)
    assert m, 'Standing rules section not found'
    section = m.group(0)
    new = TOKEN.sub('', section)
    open(p, 'w', encoding='utf-8').write(text[:m.start()] + new + text[m.end():])
    return len(TOKEN.findall(section))


def fix_cell(repo):
    p = os.path.join(repo, 'SKILL.md')
    lines = open(p, encoding='utf-8').read().split('\n')
    hit = 0
    for i, line in enumerate(lines):
        if line.lstrip().startswith('| a verdict receipt names another revision') and '`RECEIPT_REV_MISMATCH` |' in line:
            lines[i] = line.replace('`RECEIPT_REV_MISMATCH` |', '`RECEIPT_REV_CONTENT_DRIFT` |')
            hit += 1
    assert hit == 1, 'verdict cell not found once'
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))


def add_skill_row(repo, verdict_map=None):
    p = os.path.join(repo, 'SKILL.md')
    lines = open(p, encoding='utf-8').read().split('\n')
    anchor = [i for i, l in enumerate(lines) if l.startswith('| bash declared-witness study | probe | `python3 tools/bash-witness-study.py count`')]
    assert len(anchor) == 1, 'anchor row not found once'
    vm = verdict_map or ('0 PASS; 2 could-not-evaluate (unresolvable certified); '
                         '3 REFUSED with named RECEIPT_* codes; 1 usage')
    new = ('| receipt revision gate | gate | `python3 tools/receipt-revision-gate.py --lane LANE --certified REV '
           '[--paths FILE] --receipt PATH:ROLE[:REGEX]` | ' + vm + ' | `python3 tools/receipt-revision-gate.py --selftest` | '
           'none | read-only over the lane | tameshi |')
    lines.insert(anchor[0] + 1, new)
    open(p, 'w', encoding='utf-8').write('\n'.join(lines))


def build(name, mode):
    repo = make_clone(name)
    stage(repo)
    notes = []
    if mode == 'CTL_0':
        pass
    elif mode == 'CTL_HELP':
        add_rows(repo, help_rows())
    elif mode == 'CTL_HELP_HONEST':
        add_rows(repo, help_rows(expect_honest=True))
    elif mode == 'CTL_HARD':
        add_rows(repo, hard_rows())
    elif mode == 'CTL_SKILL':
        notes.append('tokens deleted in Standing rules: %d' % strip_tokens(repo))
    elif mode == 'CTL_STACK':
        add_rows(repo, hard_rows())
        add_skill_row(repo)
        fix_cell(repo)
    elif mode == 'CTL_SKILLMAP':
        # probe: a skill row whose verdict map is digits only, no meaning (the skill arm is presence-only)
        add_skill_row(repo, '0 ok; 2 ok; 3 ok')
    elif mode == 'CTL_REF':
        # liveness: the stacked set plus one genuine drift row (receipt names BASE, HEAD changed SKILL.md)
        open(os.path.join(repo, HW, 'drift.paths'), 'w').write('SKILL.md\n')
        add_rows(repo, hard_rows() + [row('gate-hardwired-drift', ['python3', 'tools/receipt-revision-gate.py',
            '--lane', '.', '--certified', 'HEAD', '--paths', HW + '/drift.paths', '--receipt',
            HW + '/positive.txt:positive'], {'exit': 3, 'stdout_contains': ['RECEIPT_REV_CONTENT_DRIFT']})])
        add_skill_row(repo)
        fix_cell(repo)
    rev = commit(repo, 'control %s: edit under test' % name)
    work = os.path.join(S, 'c2', 'work-' + name)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    p = subprocess.run([sys.executable, os.path.join(repo, '.ufo/evidence/round-57/c2/measure.py'), '--lane', repo,
                        '--rev', rev, '--work', work, '--explain'], capture_output=True, text=True)
    return {'name': name, 'mode': mode, 'rev': rev, 'exit': p.returncode, 'out': p.stdout + p.stderr, 'notes': notes}


if __name__ == '__main__':
    modes = sys.argv[1:] or ['CTL_0', 'CTL_HELP', 'CTL_HELP_HONEST', 'CTL_HARD', 'CTL_SKILL', 'CTL_STACK', 'CTL_REF']
    res = []
    for m in modes:
        r = build('C2_' + m, m)
        res.append(r)
        print('=== %s exit=%d rev=%s %s' % (r['name'], r['exit'], r['rev'][:12], ' '.join(r['notes'])))
        print(r['out'])
    json.dump(res, open(os.path.join(S, 'c2', 'results.json'), 'w'), indent=1)
