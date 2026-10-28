#!/usr/bin/env python3
"""Print the section span and sha256 of one SKILL.md section at one revision.

Usage: python3 .ufo/waves/round-54/reader-section.py LANE REV "HEADING"

Reads git objects only (the frozen round-18 sectionize at REV), so a reader's
`section_sha256` is the sha of the bytes at REV and nothing else.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile


def main():
    lane, rev, heading = sys.argv[1], sys.argv[2], sys.argv[3]
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    rev = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', rev + '^{commit}'],
                         capture_output=True, text=True, env=env, check=True).stdout.strip()
    r18 = subprocess.run(['git', '-C', lane, 'show', rev + ':.ufo/evidence/round-18/measure.py'],
                         capture_output=True, env=env, check=True).stdout
    work = tempfile.mkdtemp(prefix='r54-reader-', dir=os.environ.get('TMPDIR'))
    path = os.path.join(work, 'measure.py')
    with open(path, 'wb') as fh:
        fh.write(r18)
    spec = importlib.util.spec_from_file_location('r54_r18', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = subprocess.run(['git', '-C', lane, 'show', rev + ':SKILL.md'],
                           capture_output=True, env=env, check=True).stdout
    for sec in mod.sectionize(skill):
        if sec['heading'] == heading:
            print(json.dumps({'heading': heading, 'cand': rev, 'start': sec['start'],
                              'end': sec['end'], 'section_sha256': sec['sha256']}))
            return 0
    print('no such section: %r' % heading, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
