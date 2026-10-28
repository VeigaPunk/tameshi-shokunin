#!/usr/bin/env python3
"""Follow-up commits: make the forged report the ONLY report for its heading."""
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W1Sent01'
CLONE = S + '/clone'
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
WAVE = '.ufo/waves/round-54/w1'
HEAD = '## Standing rules'
GUESS = hashlib.sha256(b'T54W1Sent01 forged guess, never read the section').hexdigest()
TRUE = '164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7'


def git(*a, check=True):
    r = subprocess.run(['git', '-C', CLONE] + list(a), capture_output=True)
    if check and r.returncode:
        raise SystemExit('git %s failed: %s' % (a, r.stderr.decode()))
    return r.stdout


def commit(msg):
    assert git('rev-parse', '--show-toplevel').decode().strip() == CLONE
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'add', '--all')
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '--quiet', '-m', msg)
    return git('rev-parse', 'HEAD').decode().strip()


def put(rel, text):
    p = os.path.join(CLONE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)


def main():
    # B2: the forged report is now the only report naming '## Standing rules'
    git('rm', '--quiet', '%s/T54W1Read01.json' % WAVE)
    put('%s/T54W1ReadForged.json' % WAVE, json.dumps(
        {'heading': HEAD, 'cand': C0, 'section_sha256': GUESS, 'findings': []},
        ensure_ascii=False) + '\n')
    print('REV_B2', commit('FIXTURE B2: forged report is the only report for its heading, sha still guessed'))

    # C2: same bytes except the sha, copied from reader-section.py
    put('%s/T54W1ReadForged.json' % WAVE, json.dumps(
        {'heading': HEAD, 'cand': C0, 'section_sha256': TRUE, 'findings': []},
        ensure_ascii=False) + '\n')
    print('REV_C2', commit('FIXTURE C2: forged report sha corrected, still no MD and no reading'))

    # D: a finding whose quote cannot occur in the section
    put('%s/T54W1ReadForged.json' % WAVE, json.dumps(
        {'heading': HEAD, 'cand': C0, 'section_sha256': TRUE,
         'findings': [{'quote': 'T54W1Sent01 fabricated finding that never occurs in the section',
                       'why': 'fabricated, added probability ~0 of occurring'}]},
        ensure_ascii=False) + '\n')
    print('REV_D', commit('FIXTURE D: forged report carries a provably false finding'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
