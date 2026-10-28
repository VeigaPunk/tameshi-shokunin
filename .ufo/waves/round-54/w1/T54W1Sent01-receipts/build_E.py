#!/usr/bin/env python3
"""FIXTURE E: simulate the round's own post-C0 SKILL fix pass on the green fixture.

Everything is re-keyed correctly at the new section bytes (the best a competent
wave can do), and the reader reports stay exactly where the wave spec puts them
(pinned at C0). If the frozen counter compares reader pins against REV bytes,
arm 4 must fall for every section the fix pass edited.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W1Sent01'
CLONE = S + '/clone'
EDITED = '### Using the ledger'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'


def git(*a, check=True):
    r = subprocess.run(['git', '-C', CLONE] + list(a), capture_output=True)
    if check and r.returncode:
        raise SystemExit('git %s failed: %s' % (a, r.stderr.decode()))
    return r.stdout


def main():
    assert git('rev-parse', '--show-toplevel').decode().strip() == CLONE
    spec = importlib.util.spec_from_file_location('r18e', CLONE + '/.ufo/evidence/round-18/measure.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = git('show', 'HEAD:SKILL.md')
    text = skill.decode('utf-8', 'surrogateescape')
    lines = text.split('\n')
    start = next(i for i, l in enumerate(lines) if l == EDITED)
    end = next(i for i in range(start + 1, len(lines))
               if i == len(lines) - 1 or (lines[i].startswith('#')
                                          and not lines[i].startswith('####')))
    lines.insert(end, 'A fix-pass sentence appended to a re-read section (fixture E).')
    new_text = '\n'.join(lines)
    with open(os.path.join(CLONE, 'SKILL.md'), 'w', encoding='utf-8') as fh:
        fh.write(new_text)
    new_sections = {s['heading']: s for s in mod.sectionize(new_text.encode('utf-8'))}
    sec = new_sections[EDITED]
    ledger = json.loads(git('show', 'HEAD:' + LEDGER).decode('utf-8', 'surrogateescape'))
    hit = 0
    for e in ledger['entries']:
        if e.get('heading') == EDITED:
            e['sha256'] = sec['sha256']
            e['start'], e['end'] = sec['start'], sec['end']
            e['skill_sha256'] = hashlib.sha256(new_text.encode('utf-8')).hexdigest()
            hit += 1
    assert hit == 1, hit
    with open(os.path.join(CLONE, LEDGER), 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(ledger, indent=1, ensure_ascii=False) + '\n')
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'add', '--all')
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
        'commit', '--quiet', '-m',
        'FIXTURE E: a post-C0 SKILL edit re-keyed at the new bytes, readers still pinned at C0')
    rev = git('rev-parse', 'HEAD').decode().strip()
    print('REV_E', rev)
    print('EDITED_SHA_AT_E', sec['sha256'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
