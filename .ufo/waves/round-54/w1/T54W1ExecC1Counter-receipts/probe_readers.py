#!/usr/bin/env python3
"""Add the seven frozen-heading reader JSONs to the c1-probe clone and commit.

Mechanism probe only: these JSONs carry empty findings lists and are written so
the counter's arm 4 has something to read; they are NOT reader claims.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
HEADINGS = json.load(open(
    '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/lost-headings-at-base.json'))
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
GITC = ['-c', 'user.name=c1-probe', '-c', 'user.email=c1-probe@example.invalid',
        '-c', 'commit.gpgsign=false']


def git(repo, *args):
    r = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, env=ENV)
    if r.returncode != 0:
        raise SystemExit('git %s: %s' % (' '.join(args), r.stderr.decode()))
    return r.stdout


def main():
    clone = sys.argv[1]
    rev = sys.argv[2]
    top = git(clone, 'rev-parse', '--show-toplevel').decode().strip()
    assert Path(top).resolve() == Path(clone).resolve(), (top, clone)
    spec = importlib.util.spec_from_file_location(
        'r18probe', os.path.join(clone, '.ufo/evidence/round-18/measure.py'))
    r18 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r18)
    skill = git(clone, 'show', '%s:SKILL.md' % rev)
    by_head = {}
    for sec in r18.sectionize(skill):
        by_head.setdefault(sec['heading'], []).append(sec['sha256'])
    written = []
    for i, h in enumerate(HEADINGS, 1):
        shas = by_head.get(h)
        if not shas:
            raise SystemExit('heading not found at rev: %r' % h)
        assert len(shas) == 1, (h, shas)
        rel = '.ufo/waves/round-54/w1/T54W1SynthRead%02d.json' % i
        Path(clone, rel).parent.mkdir(parents=True, exist_ok=True)
        Path(clone, rel).write_text(json.dumps(
            {'heading': h, 'cand': C0, 'section_sha256': shas[0],
             'findings': [],
             'probe': 'mechanism probe: empty findings, not a reader claim'},
            indent=1) + '\n', 'utf-8')
        written.append(rel)
    git(clone, 'add', '-A')
    git(clone, *GITC, 'commit', '-q', '-m',
        'c1-probe: add seven reader-shaped JSONs (mechanism probe, empty findings)')
    newrev = git(clone, 'rev-parse', 'HEAD').decode().strip()
    print('READER_PROBE_REV %s' % newrev)
    for rel in written:
        print('WROTE %s' % rel)


if __name__ == '__main__':
    main()
