#!/usr/bin/env python3
"""Build a scratch fixture clone of the lane at C1 with a hand-bound re-key.

Usage: build.py VARIANT

The re-key binds all 23 headings the round-54 binder binds (the union of
lost-headings-at-c0.json and lost-headings-at-base.json), so the positive
variant reproduces the frozen C1 claim and every other arm is held fixed.
VARIANT changes ONE field of ONE entry:

  positive   every entry carries read_rev == c0 (full 40 hex)
  prefix     the "## Standing rules" entry carries the 12-char c0 prefix
  ancestor   the "## Standing rules" entry carries the full 40-hex base commit
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/tameshi-r54/T54W2Sent03'
LANE_SRC = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
C1 = '99c3bc88d704566197783f66b211ee0a830e0330'
BASE = 'd33053f7552db4bd290c99a36979760f544c41ad'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
VARIANT = sys.argv[1]
D = '%s/fixtures/%s' % (S, VARIANT)

env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')


def git(args, check=True):
    return subprocess.run(['git', '-C', D] + args, env=env, capture_output=True, check=check)


def show(path):
    return git(['show', '%s:%s' % (C1, path)]).stdout


def main():
    if os.path.exists(D):
        shutil.rmtree(D)
    os.makedirs(os.path.dirname(D), exist_ok=True)
    subprocess.run(['git', 'clone', '--shared', '--quiet', LANE_SRC, D], env=env, check=True)
    assert git(['rev-parse', '--show-toplevel']).stdout.decode().strip() == D
    git(['-c', 'advice.detachedHead=false', 'checkout', '--quiet', C1])
    assert git(['rev-parse', 'HEAD']).stdout.decode().strip() == C1

    spec = importlib.util.spec_from_file_location('r18b', S + '/code/r18-at-c1.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill_bytes = show('SKILL.md')
    secs = {s['heading']: s for s in mod.sectionize(skill_bytes)}
    skill_sha = hashlib.sha256(skill_bytes).hexdigest()
    province_sha = hashlib.sha256(show('PROVINCE.md')).hexdigest()

    base7 = json.load(open(S + '/code/c1/lost-headings-at-base.json'))
    c0lost = json.load(open(LANE_SRC + '/.ufo/evidence/round-54/c1/lost-headings-at-c0.json'))
    union = sorted(set(base7) | set(c0lost))

    rekey_rel = '.ufo/evidence/round-21/coldread/rekey-r54-' + C1[:12]
    os.makedirs(os.path.join(D, rekey_rel, 'traces'), exist_ok=True)
    os.makedirs(os.path.join(D, '.ufo/waves/round-54/w1'), exist_ok=True)

    ledger = json.loads(show(LEDGER).decode('utf-8', 'surrogateescape'))
    entries = ledger['entries']

    tampered = {'prefix': C1[:12], 'ancestor': BASE}.get(VARIANT)
    tamper_heading = base7[0]                    # "## Standing rules", a frozen heading

    for n, h in enumerate(union, 1):
        sec = secs[h]
        trace_rel = '%s/traces/section-%02d.json' % (rekey_rel, n)
        with open(os.path.join(D, trace_rel), 'w') as fh:
            json.dump({'schema': 'tameshi-trace-inputs-v1',
                       'argv': [sys.executable, 'binder.py', D, C1, C1, rekey_rel, 'section', h],
                       'cwd': S + '/fixtures', 'root': D, 'rev': C1, 'exit': 0,
                       'inputs': {'PROVINCE.md': province_sha},
                       'external': {}, 'live_lane_reads': {}, 'untracked': []}, fh, indent=1)
            fh.write('\n')
        read_rev = C1
        if tampered is not None and h == tamper_heading:
            read_rev = tampered
        entries.append({
            'skill_sha256': skill_sha,
            'start': sec['start'], 'end': sec['end'], 'heading': h,
            'sha256': sec['sha256'], 'class': 'record', 'verdict': 'verified-record',
            'blocking_gaps': 0, 'wrong_expectations': 0, 'minor_gaps': 0,
            'commands_executed_count': 2, 'read_rev': read_rev,
            'inputs': {'PROVINCE.md': province_sha},
            'external_inputs': {'tameshi@%s:PROVINCE.md' % C1: province_sha},
            'traces': [trace_rel], 'seats': ['T54W2Sent03 fixture'],
            'reports': ['.ufo/waves/round-54/w1/T54W1Read%02d.json' % n],
        })
        with open(os.path.join(D, '.ufo/waves/round-54/w1/T54W1Read%02d.json' % n), 'w') as fh:
            json.dump({'heading': h, 'cand': C1, 'section_sha256': sec['sha256'],
                       'findings': []}, fh, indent=1)
            fh.write('\n')
        with open(os.path.join(D, '.ufo/waves/round-54/w1/T54W1Read%02d.md' % n), 'w') as fh:
            fh.write('# fixture reader for %s\n' % h)

    with open(os.path.join(D, LEDGER), 'w') as fh:
        json.dump(ledger, fh, indent=1, ensure_ascii=False)
        fh.write('\n')

    git(['add', '-A'])
    git(['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
         'commit', '--quiet', '-m', 'fixture: hand-bound rekey (%s)' % VARIANT])
    print('FIXTURE variant=%s dir=%s head=%s entries=%d tampered_read_rev=%s on=%r'
          % (VARIANT, D, git(['rev-parse', 'HEAD']).stdout.decode().strip(),
             len(union), tampered, tamper_heading))
    return 0


if __name__ == '__main__':
    sys.exit(main())
