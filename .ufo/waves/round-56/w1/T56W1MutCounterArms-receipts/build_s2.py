#!/usr/bin/env python3
"""Probe fixture S v2: page 64/64 with box 3 unmarked (score 6, box3_full_page true).

The first S build drifted the re-key entries because they pinned SHONEN.md; this
build pins every fixture entry to corpus/QUALITY.md (stable across the probe),
re-credits the one base entry that pinned SHONEN.md, and appends a calibration row
that states 6 at the base commit (where the monitor reads 6). Only arm 2 can then
fire, and only through its `score == 8` conjunct.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r56/T56W1MutCounterArms')
CLONE = S / 'lane'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
STABLE = 'corpus/QUALITY.md'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')


def git(*args, check=True):
    r = subprocess.run(['git', '-C', str(CLONE)] + list(args), env=ENV, capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(args), r.stderr.decode()))
    return r.stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    fx = json.loads((S / 'fixtures.json').read_text())
    z, base, rekey = fx['fixtures']['G_green'], fx['base'], fx['rekey_dir'] + '/'
    r18src = S / 'r18measure.py'
    if not r18src.exists():
        r18src.write_bytes(git('show', base, '.ufo/evidence/round-18/measure.py'))
    spec = importlib.util.spec_from_file_location('r18_s2', str(r18src))
    r18 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r18)

    git('checkout', '--detach', z)
    assert git('rev-parse', '--show-toplevel').decode().strip() == str(CLONE)
    skill = git('show', '%s:SKILL.md' % z)
    sections = {s['sha256']: s for s in r18.sectionize(skill)}
    q_sha = sha(git('show', '%s:%s' % (z, STABLE)))

    # box 3 unmarked: score 6, page still full
    shonen = git('show', '%s:SHONEN.md' % z).decode('utf-8', 'surrogateescape').split('\n')
    seen = 0
    for i, line in enumerate(shonen):
        if line.startswith('- [~] '):
            seen += 1
            if seen == 3:
                shonen[i] = '- [x] ' + line[len('- [~] '):]
    assert seen == 4, 'expected 4 asserted boxes, saw %d' % seen
    (CLONE / 'SHONEN.md').write_text('\n'.join(shonen), 'utf-8', newline='')

    led = json.loads(git('show', '%s:%s' % (z, LEDGER)))
    kept, dropped, repaired = [], [], 0
    for e in led['entries']:
        if not isinstance(e, dict):
            kept.append(e)
            continue
        mine = any(isinstance(t, str) and t.startswith(rekey) for t in (e.get('traces') or []))
        if mine:
            e['inputs'] = {STABLE: q_sha}
            for t in e['traces']:
                (CLONE / t).write_text(json.dumps({'schema': 'tameshi-trace-inputs-v1',
                                                   'inputs': {STABLE: q_sha}}) + '\n')
            kept.append(e)
            continue
        inputs = e.get('inputs') or {}
        if isinstance(inputs, dict) and 'SHONEN.md' in inputs:
            dropped.append(e)
            continue
        kept.append(e)
    for e in dropped:
        sec = sections.get(e.get('sha256'))
        trace = '%s/traces/S-repair-%02d.json' % (fx['rekey_dir'], repaired + 1)
        repaired += 1
        (CLONE / trace).write_text(json.dumps({'schema': 'tameshi-trace-inputs-v1',
                                               'inputs': {STABLE: q_sha}}) + '\n')
        kept.append({'skill_sha256': sha(skill),
                     'start': sec['start'] if sec else e.get('start', 1),
                     'end': sec['end'] if sec else e.get('end', 1),
                     'heading': sec['heading'] if sec else e.get('heading', ''),
                     'sha256': e['sha256'], 'class': 'instruction',
                     'verdict': 'executed-ok', 'blocking_gaps': 0,
                     'wrong_expectations': 0, 'minor_gaps': 0,
                     'commands_executed_count': 1, 'read_rev': fx['c0'],
                     'inputs': {STABLE: q_sha}, 'traces': [trace],
                     'seats': ['FIX56'], 'reports': []})
    led['entries'] = kept
    (CLONE / LEDGER).write_text(json.dumps(led, indent=2) + '\n')

    row = ('| calibration | 6 | fixture row: the round-21 cold-read monitor reads 6 '
           'at the named commit | `%s` | 56 (fixture) |\n' % base[:12])
    card = git('show', '%s:SCORECARD.md' % z).decode('utf-8', 'surrogateescape')
    (CLONE / 'SCORECARD.md').write_text(card + row, 'utf-8', newline='')

    git('add', '--all')
    git('commit', '--quiet', '-m', 'fixture: page 64/64 with box 3 unmarked (score 6)')
    s2 = git('rev-parse', 'HEAD').decode().strip()
    fx['fixtures']['S1_superseded'] = fx['fixtures']['S_score']
    fx['fixtures']['S_score'] = s2
    (S / 'fixtures.json').write_text(json.dumps(fx, indent=2) + '\n')
    print('S2', s2, 'dropped', len(dropped), 'repaired', repaired)
    return 0


if __name__ == '__main__':
    sys.exit(main())
