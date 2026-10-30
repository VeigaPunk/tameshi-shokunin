#!/usr/bin/env python3
"""Reference gate R: contract-exit_map semantics for MULTIPLE --path args.
Precedence: 2 (bad args / unresolvable candidate / declared path absent or
              non-regular at TRUSTED = invalid trusted source)
            > 1 (any declared path drifted, missing, or nonregular at candidate)
            > 0 (all declared regular blobs equal).
Verdict independent of --path order and of duplicate declarations."""
import argparse, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True)
p.add_argument('--trusted', required=True)
p.add_argument('--candidate', required=True)
p.add_argument('--path', action='append', required=True)
a = p.parse_args()

def git(*args):
    return subprocess.run(['git', '-C', a.repo, *args], capture_output=True, text=True)

# exit 2: candidate must resolve to a commit
if git('rev-parse', '--verify', '--quiet', a.candidate + '^{commit}').returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE candidate unresolvable', file=sys.stderr)
    sys.exit(2)

def entry(rev, path):
    """(object-type, oid) via git rev-parse rev:path (git-normalized spelling), or None."""
    r = git('rev-parse', '--quiet', f'{rev}:{path}')
    if r.returncode:
        return None
    oid = r.stdout.strip()
    t = git('cat-file', '-t', oid)
    return (t.stdout.strip(), oid)

for path in dict.fromkeys(a.path):  # dedupe, preserve order
    te = entry(a.trusted, path)
    if te is None or te[0] != 'blob':
        print(f'EXECUTOR_SOURCE_UNAVAILABLE declared source absent/nonregular at trusted: {path}',
              file=sys.stderr)
        sys.exit(2)

drift = []
for path in dict.fromkeys(a.path):
    te = entry(a.trusted, path)
    ke = entry(a.candidate, path)
    if ke is None or ke[0] != 'blob' or ke[1] != te[1]:
        drift.append(path)

if drift:
    print('EXECUTOR_SOURCE_DRIFT ' + ', '.join(drift), file=sys.stderr)
    sys.exit(1)
print('EXECUTOR_SOURCE_BOUND all declared sources equal')
sys.exit(0)
