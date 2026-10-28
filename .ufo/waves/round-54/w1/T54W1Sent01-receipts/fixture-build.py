#!/usr/bin/env python3
"""T54W1Sent01 attack fixture: forged reader report vs the frozen C1 counter.

Builds three commits on top of C0 in the scratch clone:
  A  spec-conforming re-key DIRECTORY (binder layout) + synthetic 64-entry
     ledger + seven reader JSONs carrying the true section sha, no MDs.
  B  A + the decoy blob `traces/rekey-r54-<c0short>` (the only shape arm 3's
     recursive listing can see) + T54W1ReadForged.json with a GUESSED sha.
  C  B with the guess replaced by the true sha and one fabricated finding.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W1Sent01'
CLONE = S + '/clone'
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
REKEY = '.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11'
WAVE = '.ufo/waves/round-54/w1'
GUESS = hashlib.sha256(b'T54W1Sent01 forged guess, never read the section').hexdigest()


def git(*a, check=True):
    r = subprocess.run(['git', '-C', CLONE] + list(a), capture_output=True)
    if check and r.returncode:
        raise SystemExit('git %s failed: %s' % (a, r.stderr.decode()))
    return r.stdout


def commit(msg):
    assert git('rev-parse', '--show-toplevel').decode().strip() == CLONE
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        'add', '--all')
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '--quiet', '-m', msg)
    return git('rev-parse', 'HEAD').decode().strip()


def put(rel, text):
    p = os.path.join(CLONE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main():
    spec = importlib.util.spec_from_file_location(
        'r18b', CLONE + '/.ufo/evidence/round-18/measure.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = git('show', C0 + ':SKILL.md')
    sections = mod.sectionize(skill)
    prov_sha = hashlib.sha256(git('show', C0 + ':PROVINCE.md')).hexdigest()
    skill_sha = hashlib.sha256(skill).hexdigest()
    frozen = json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/'
                            '.ufo/evidence/round-54/c1/lost-headings-at-base.json'))
    by_head = {s['heading']: s for s in sections}

    entries = []
    for n, sec in enumerate(sections, 1):
        trace_rel = '%s/traces/section-%02d.json' % (REKEY, n)
        put(trace_rel, json.dumps({
            'schema': 'tameshi-trace-inputs-v1',
            'rev': C0,
            'inputs': {'PROVINCE.md': prov_sha},
        }, indent=1) + '\n')
        entries.append({
            'skill_sha256': skill_sha,
            'start': sec['start'], 'end': sec['end'],
            'heading': sec['heading'], 'sha256': sec['sha256'],
            'class': 'record', 'verdict': 'verified-record',
            'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
            'commands_executed_count': 2,
            'read_rev': C0,
            'inputs': {'PROVINCE.md': prov_sha},
            'external_inputs': {},
            'traces': [trace_rel],
            'seats': ['T54W1Sent01'],
            'reports': [],
        })
    put('.ufo/evidence/round-21/coldread/ledger.json',
        json.dumps({'entries': entries}, indent=1, ensure_ascii=False) + '\n')

    # seven reader reports; six carry the true sha from reader-section.py, all
    # are fabricated (no MD, no reading), and none has findings yet.
    for i, h in enumerate(frozen, 1):
        put('%s/T54W1Read%02d.json' % (WAVE, i), json.dumps({
            'heading': h, 'cand': C0,
            'section_sha256': by_head[h]['sha256'], 'findings': []},
            ensure_ascii=False) + '\n')

    rev_a = commit('FIXTURE A: binder-shaped rekey dir + synthetic ledger + 7 correct-sha readers (no MDs)')
    print('REV_A', rev_a)

    # B: the decoy blob arm 3's recursive listing can see + the forged report
    put('%s/traces/rekey-r54-59c38109bf11' % REKEY, '')
    forged = {'heading': frozen[0], 'cand': C0,
              'section_sha256': GUESS, 'findings': []}
    put('%s/T54W1ReadForged.json' % WAVE,
        json.dumps(forged, ensure_ascii=False) + '\n')
    rev_b = commit('FIXTURE B: decoy blob named after the rekey dir + forged reader with guessed sha')
    print('REV_B', rev_b)

    # C: the guess replaced by the true sha, and one provably false finding
    forged['section_sha256'] = by_head[frozen[0]]['sha256']
    put('%s/T54W1ReadForged.json' % WAVE,
        json.dumps(forged, ensure_ascii=False) + '\n')
    r1 = json.loads(open(os.path.join(CLONE, '%s/T54W1Read01.json' % WAVE)).read())
    r1['findings'] = [{'quote': 'T54W1Sent01 fabricated finding that never occurs in the section',
                       'why': 'fabricated'}]
    put('%s/T54W1Read01.json' % WAVE, json.dumps(r1, ensure_ascii=False) + '\n')
    rev_c = commit('FIXTURE C: forged report sha corrected from reader-section.py + one false finding')
    print('REV_C', rev_c)
    print('GUESS', GUESS)
    print('TRUE_SHA_STANDING_RULES', by_head[frozen[0]]['sha256'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
