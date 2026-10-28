#!/usr/bin/env python3
"""Trace-fabrication attack against the frozen C1 credit gate (round 54, seat T54W1Sent03).

Builds commits with pure git plumbing (hash-object -w / a private index fed via
update-index --index-info / write-tree / commit-tree). No branch, no ref, no
`git add`, no `git commit`: each produced commit sha is fed straight to the
counter. Everything happens in the scratch clone.

Two layers:
  layer 1 (ceiling)  the documented re-key layout <dir>/traces/section-*.json
                     is not even detected by arm 3 (REKEY_RE matches the file
                     basename) -> dirs=[] and the arm reports 0/7 regardless.
  layer 2 (gate)     with a trace file whose basename matches the re-key dir,
                     arm 3 does evaluate the hand-bound entry, and the frozen
                     credit algorithm refuses a fabricated trace while the
                     trace-only controls credit.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tameshi-r54/T54W1Sent03')
CLONE = S / 'clone'
C0 = '59c38109bf119d0e9d4f878644a82babc937bc1e'
BASE = 'd33053f7552d'
LIVE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
REKEYDIR = '.ufo/evidence/round-21/coldread/rekey-r54-59c38109bf11'
DIRNAME = 'rekey-r54-59c38109bf11'
HEADING = '## Standing rules'
R18 = '.ufo/evidence/round-18/measure.py'
RECEIPTS = S / 'receipts'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='attack', GIT_AUTHOR_EMAIL='attack@example.invalid',
           GIT_COMMITTER_NAME='attack', GIT_COMMITTER_EMAIL='attack@example.invalid',
           GIT_AUTHOR_DATE='2026-10-28T00:00:00 +0000',
           GIT_COMMITTER_DATE='2026-10-28T00:00:00 +0000')


def git(*args, data=None):
    return subprocess.run(['git', '-C', str(CLONE)] + list(args), input=data,
                          capture_output=True, env=ENV, check=True)


def show(rev, path):
    return git('show', '%s:%s' % (rev, path)).stdout


def lsr(rev):
    out = {}
    for line in git('ls-tree', '-r', '-z', rev).stdout.split(b'\0'):
        if not line:
            continue
        meta, path = line.split(b'\t', 1)
        mode, typ, sha = meta.decode().split()
        out[path.decode()] = (mode, sha)
    return out


def blob_sha(data):
    return git('hash-object', '-w', '--stdin', data=data).stdout.decode().strip()


def make_commit(files, message):
    """files: path -> bytes (new/overridden blobs). Returns the commit sha."""
    base = lsr(C0)
    for path, data in files.items():
        base[path] = ('100644', blob_sha(data))
    index = S / 'index.tmp'
    if index.exists():
        index.unlink()
    env = dict(ENV, GIT_INDEX_FILE=str(index))
    lines = ''.join('%s %s\t%s\0' % (mode, sha, path)
                    for path, (mode, sha) in sorted(base.items())).encode()
    subprocess.run(['git', '-C', str(CLONE), 'update-index', '-z', '--index-info'],
                   input=lines, capture_output=True, env=env, check=True)
    tree = subprocess.run(['git', '-C', str(CLONE), 'write-tree'],
                          capture_output=True, env=env, check=True).stdout.decode().strip()
    index.unlink()
    return subprocess.run(['git', '-C', str(CLONE), 'commit-tree', tree, '-p', C0,
                           '-m', message],
                          capture_output=True, env=ENV, check=True).stdout.decode().strip()


def sha_at(rev, path):
    return hashlib.sha256(show(rev, path)).hexdigest()


def load_r18():
    mod_path = S / 'r18measure.py'
    mod_path.write_bytes(show(C0, R18))
    spec = importlib.util.spec_from_file_location('r18_attack', str(mod_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def splice(raw, item):
    """Insert ITEM as the last element of the top-level "entries" array,
    leaving every other byte of the ledger untouched."""
    start = raw.index(b'"entries"')
    open_at = raw.index(b'[', start)
    depth, i, in_str, esc = 0, open_at, False, False
    while True:
        ch = raw[i:i + 1]
        if in_str:
            if esc:
                esc = False
            elif ch == b'\\':
                esc = True
            elif ch == b'"':
                in_str = False
        elif ch == b'"':
            in_str = True
        elif ch == b'[':
            depth += 1
        elif ch == b']':
            depth -= 1
            if depth == 0:
                break
        i += 1
    block = json.dumps(item, indent=1, sort_keys=True)
    block = '\n'.join('  ' + line for line in block.split('\n'))
    head = raw[:i].rstrip(b' \n')          # last entry's closing brace
    return head + b',\n' + block.encode() + b'\n ' + raw[i:]


def main():
    base = git('rev-parse', '--verify', BASE + '^{commit}').stdout.decode().strip()
    legacy = load_r18()
    skill = show(C0, 'SKILL.md')
    sections = {s['heading']: s for s in legacy.sectionize(skill)}
    sec = sections[HEADING]
    inputs = {}
    for path in ('tools/mutate-and-run.sh', 'SHONEN.md', 'corpus/SOURCES.md',
                 'tools/registry.json'):
        inputs[path] = sha_at(C0, path)
    drift_value = sha_at(base, 'tools/registry.json')  # pre-C0 registry blob
    assert drift_value != inputs['tools/registry.json']
    live_skill = sha_at(C0, 'SKILL.md')
    ledger_raw = show(C0, LEDGER)

    def trace(inputs_view, live_reads=None):
        return json.dumps({
            'schema': 'tameshi-trace-inputs-v1',
            'argv': ['/usr/bin/python3', LIVE + '/tools/trace-inputs.py', C0],
            'cwd': LIVE,
            'root': LIVE,
            'rev': C0,
            'rev_reason': 'hand-bound trace, seat T54W1Sent03 trace-fabrication attack',
            'exit': 0,
            'tracked_filter': 'git-object reads only',
            'env_overrides': {'GIT_CONFIG_GLOBAL': '/dev/null',
                              'GIT_CONFIG_NOSYSTEM': '1'},
            'inputs': inputs_view,
            'untracked': [],
            'external': {},
            'live_lane_reads': live_reads or {},
            'dropped_home_count': 0,
        }, indent=1, sort_keys=True).encode()

    def entry(trace_path):
        return {
            'skill_sha256': hashlib.sha256(skill).hexdigest(),
            'start': sec['start'],
            'end': sec['end'],
            'heading': HEADING,
            'sha256': sec['sha256'],
            'class': 'instruction',
            'verdict': 'executed-ok',
            'blocking_gaps': 0,
            'wrong_expectations': 0,
            'minor_gaps': 0,
            'commands_executed_count': 3,
            'read_rev': C0,
            'inputs': dict(inputs),
            'external_inputs': {},
            'traces': [trace_path],
            'seats': ['T54W1Sent03'],
            'reports': ['.ufo/waves/round-54/w1/T54W1Sent03.md'],
            'carried_from': {'synthetic': 'trace-fabrication attack'},
        }

    good = dict(inputs)
    drift = dict(inputs, **{'tools/registry.json': drift_value})
    variants = [
        # layer-1 ceiling: documented layout, trace basename = section-standing-rules.json
        ('documented-layout-drift',
         REKEYDIR + '/traces/section-standing-rules.json', trace(drift),
         'fabricated trace under the documented re-key layout'),
        # layer-2 gate: trace basename matches the re-key dir name so arm 3 detects it
        ('gate-control-good',
         REKEYDIR + '/traces/' + DIRNAME, trace(good),
         'control: trace inputs equal the entry inputs'),
        ('gate-trace-input-drift',
         REKEYDIR + '/traces/' + DIRNAME, trace(drift),
         'fabricated: trace records the pre-C0 registry sha'),
        ('gate-live-lane-read-wrong-digest',
         REKEYDIR + '/traces/' + DIRNAME,
         trace(good, live_reads={LIVE + '/SKILL.md': 'c' * 64}),
         'fabricated: live_lane_reads names the live SKILL.md at a wrong digest'),
        ('gate-control-live-lane-read-bound',
         REKEYDIR + '/traces/' + DIRNAME,
         trace(good, live_reads={LIVE + '/SKILL.md': live_skill}),
         'control: live_lane_reads names the live SKILL.md at the C0 digest'),
    ]
    out = {'c0': C0, 'base': base, 'heading': HEADING, 'start': sec['start'],
           'end': sec['end'], 'section_sha256': sec['sha256'],
           'entry_inputs': inputs, 'drift_value': drift_value,
           'live_skill_sha256': live_skill, 'variants': {}}
    for name, trace_path, trace_bytes, label in variants:
        files = {trace_path: trace_bytes,
                 LEDGER: splice(ledger_raw, entry(trace_path))}
        rev = make_commit(files, 'attack: %s' % label)
        e = entry(trace_path)
        reason = legacy.entry_reason(str(CLONE), rev, e, True)
        out['variants'][name] = {
            'commit': rev, 'trace_path': trace_path, 'label': label,
            'reason': reason,
            'reason_fields': {
                'entry_failure': legacy.entry_failure(e),
                'entry_credit_reason': legacy.entry_credit_reason(e),
                'input_reason': legacy.input_reason(str(CLONE), rev, e),
                'trace_reason': legacy.trace_reason(str(CLONE), rev, e, True)},
            'trace': json.loads(trace_bytes.decode())}
        print('%-38s rev=%s reason=%s' % (name, rev[:12], reason))
    (RECEIPTS / 'variants.json').write_text(json.dumps(out, indent=1, sort_keys=True))
    (RECEIPTS / 'entry.json').write_text(
        json.dumps(entry(REKEYDIR + '/traces/' + DIRNAME), indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
