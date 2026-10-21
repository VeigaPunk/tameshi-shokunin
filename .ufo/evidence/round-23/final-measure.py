#!/usr/bin/env python3
"""Round23 final receipts at one committed revision; writes only --out files.

Runs each instrument either from a private clone at --rev (claim counter,
gate selftest and binding verdicts) or against --rev directly (strict monitor,
registry battery --rev). Records argv, cwd, revision, interval, exit, streams
and instrument digests taken from the copy that actually ran.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone


def env():
    return {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


def run(argv, cwd, rev, instruments, timeout=1800):
    start = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=env(), timeout=timeout)
    end = datetime.now(timezone.utc).isoformat()
    return {'argv': argv, 'cwd': cwd, 'revision': rev, 'measurement_interval': {'start': start, 'end': end},
            'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr,
            'instrument_sha256': {str(k): hashlib.sha256(Path(k).read_bytes()).hexdigest() for k in instruments}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    repo = str(a.repo.resolve())
    rev = subprocess.run(['git', '-C', repo, 'rev-parse', '--verify', a.rev + '^{commit}'], check=True,
                         capture_output=True, text=True, env=env()).stdout.strip()
    obs = {}
    with tempfile.TemporaryDirectory(prefix='tameshi-r23-final-') as tmp:
        clone = os.path.join(tmp, 'lane')
        subprocess.run(['git', 'clone', '-q', '--no-hardlinks', repo, clone], check=True, env=env())
        subprocess.run(['git', '-C', clone, 'checkout', '-q', '--detach', rev], check=True, env=env())
        head = subprocess.run(['git', '-C', clone, 'rev-parse', 'HEAD'], check=True, capture_output=True,
                              text=True, env=env()).stdout.strip()
        assert head == rev
        e = clone + '/.ufo/evidence/round-23/'
        tool = clone + '/tools/command-binding.py'
        obs['claim-final'] = run(['python3', e + 'measure.py', '--repo', clone], clone, rev, [e + 'measure.py', tool])
        obs['selftest-final'] = run(['python3', tool, '--selftest'], clone, rev, [tool, e + 'extra-cases.json'])
        for name, bundle, expected in (('replay-gate-final', 'replay/bundle.json', 'replay/expected.json'),
                                       ('source-read-gate-final', 'source-read-bundle.json', 'source-read-expected.json'),
                                       ('correct-command-gate-final', 'correct-command-bundle.json', 'correct-command-expected.json')):
            obs[name] = run(['python3', tool, '--bundle', e + bundle, '--expected', e + expected, '--json'], clone, rev,
                            [tool, e + bundle, e + expected])
    monitor = repo + '/.ufo/evidence/round-21/coldread/measure.py'
    obs['monitor-final'] = run(['python3', monitor, '--repo', repo, '--rev', rev, '--explain'], repo, rev,
                               [monitor, repo + '/.ufo/evidence/round-18/measure.py'])
    runner = repo + '/tools/registry-check.py'
    obs['registry-final'] = run(['python3', runner, '--root', repo, '--rev', rev, '--json'], repo, rev, [runner])
    census = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
    obs['census-final'] = run([census, 'validate', '--root', '/home/vgpnk/Projects/shokunin', 'tameshi'],
                              '/home/vgpnk/Projects/shokunin', rev, [census])
    a.out.write_text(json.dumps({'revision': rev, 'observations': obs,
                                 'bounds': 'registry battery and monitor instrument digests hash the live-tree copies; '
                                           'claim/selftest/gate digests hash the clone copies that ran; the census '
                                           'reads the live working tree, whose tracked state equals rev when clean'},
                                indent=1, ensure_ascii=False) + '\n')
    print(json.dumps({k: v['exit'] for k, v in obs.items()}))


if __name__ == '__main__':
    main()
