#!/usr/bin/env python3
"""Seat T50ExecShrinker: probe the frozen round-50 C2 counter (measure.py) on a scratch fixture
lane whose tools/shrink-case.py is this seat's deliverable.

Substitutions, named (this is a probe, never a verdict):
  * lane        = a scratch fixture repo built here; base = its first commit, rev = its second
  * gen_lane    = the real lane, so the generator is read at the pinned GEN_REV bytes
  * hidden      = a substitute panel of four mutants invented here (the real hidden panel is
                  outside this seat's custody and is never read)
  * corpus records (README F6 line, S001 mined row, knowledge entry) = fixture text in the scratch
                  repo, the same shape measure.py's own selftest builds
Everything else - the public round-49 panel, its digest, the guard digest, the instrumented cost
check, the oracle judge, the selftest invocation - is the frozen counter's own code.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
S = '/fast/scratch/hyaku/tameshi-r50/T50ExecShrinker'
MEASURE = os.path.join(LANE, '.ufo', 'evidence', 'round-50', 'c2', 'measure.py')
PANEL = os.path.join(LANE, '.ufo', 'evidence', 'round-49', 'c2', 'panel.json')
GUARD = os.path.join(LANE, 'tools', 'staged-id-guard.py')
GEN = os.path.join(LANE, 'tools', 'pbt-staged-id.py')
DELIVERABLE = os.path.join(LANE, '.ufo', 'waves', 'round-50', 'w1', 'T50ExecShrinker.shrink-case.py')
GEN_REV = '7d3d977f39acaa5723a696dff85ab183c80ddc8b'
REPO = os.path.join(S, 'fixture-lane')

SUBSTITUTE = {'id': 'SX', 'mutants': [
    {'id': 'X01', 'name': 'extractor-label', 'old': "'extractor': '0-3space',",
     'new': "'extractor': '0-3-spaces',"},
    {'id': 'X02', 'name': 'column0-indent',
     'old': "COLUMN0_RE = re.compile(r'^\\|\\s*(S\\d{3,})\\s*\\|')",
     'new': "COLUMN0_RE = re.compile(r'^ \\|\\s*(S\\d{3,})\\s*\\|')"},
    {'id': 'X03', 'name': 'scheme-strip-http-only', 'old': "text = re.sub(r'^https?://', '', text)",
     'new': "text = re.sub(r'^http://', '', text)"},
    {'id': 'X04', 'name': 'safe-floor-off-by-one',
     'old': "'safe_floor': 'S%03d' % (max(top, staged_top) + 1),",
     'new': "'safe_floor': 'S%03d' % (max(top, staged_top) + 2),"},
]}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if os.path.exists(REPO):
        shutil.rmtree(REPO)
    os.makedirs(REPO)
    env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
               GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')

    def git(*args):
        return subprocess.run(['git', '-C', REPO] + list(args), check=True,
                              capture_output=True, env=env)
    git('init', '-q')
    top = git('rev-parse', '--show-toplevel').stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(REPO), (top, REPO)

    def write(path, data):
        full = os.path.join(REPO, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data if isinstance(data, bytes) else data.encode('utf-8'))

    def commit(message):
        git('add', '-A')
        git('commit', '-q', '--allow-empty', '-m', message)
        return git('rev-parse', 'HEAD').stdout.decode().strip()

    gen_bytes = subprocess.run(['git', '-C', LANE, 'show', GEN_REV + ':' + 'tools/pbt-staged-id.py'],
                               capture_output=True, check=True).stdout
    guard_bytes = open(GUARD, 'rb').read()
    write('tools/staged-id-guard.py', guard_bytes)
    write('tools/pbt-staged-id.py', gen_bytes)
    write('corpus/README.md', '| id | frontier | state |\n|---|---|---|\n| F6 | fixture minimization | open |\n')
    write('corpus/SOURCES.md',
          '| id | doc | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
          '|---|---|---|---|---|---|---|---|---|---|---|\n'
          '| S001 | doc — https://e.x/a | paper | A | s | a | t | mined | 2026-10-26 | 365d | - |\n')
    base = commit('fixture base: guard, generator, corpus')
    write('tools/shrink-case.py', open(DELIVERABLE, 'rb').read())
    write('corpus/README.md',
          '| id | frontier | state |\n|---|---|---|\n| F6 | fixture minimization for survivors | held (round 50) |\n')
    write('corpus/knowledge/shrink-case.md',
          'source: S001 — https://e.x/a\nfrontier: F6 fixture minimization for survivors\n'
          'method: delta debugging (ddmin) to a 1-minimal sub-case\n')
    rev = commit('fixture rev: shrinker, F6 held, knowledge entry')
    hidden = os.path.join(S, 'substitute-hidden-panel.json')
    with open(hidden, 'w', encoding='utf-8') as fh:
        json.dump(SUBSTITUTE, fh)
    hidden_sha = sha(open(hidden, 'rb').read())
    print('fixture base=%s rev=%s' % (base, rev))
    print('public panel sha %s (frozen pin d6dd2cf38317118b14dfcdc1069b3222e3d4dc65ff05e005fc2b0592ce2eeda1)'
          % sha(open(PANEL, 'rb').read()))
    print('substitute hidden panel sha %s mutants=%d' % (hidden_sha, len(SUBSTITUTE['mutants'])))
    spec = importlib.util.spec_from_file_location('frozen_c2_measure', MEASURE)
    measure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measure)
    work = os.path.join(S, 'probe-work')
    if os.path.exists(work):
        shutil.rmtree(work)
    counts, stat, total = measure.measure(REPO, rev, work, PANEL, hidden, hidden_sha=hidden_sha,
                                          base=base, gen_lane=LANE)
    print(measure.line(rev, counts, stat, total))
    print('counts=%r' % (counts,))
    print('stat=%r' % ({k: v for k, v in stat.items() if k != 'records'},))
    print('records=%r' % (stat['records'],))
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
