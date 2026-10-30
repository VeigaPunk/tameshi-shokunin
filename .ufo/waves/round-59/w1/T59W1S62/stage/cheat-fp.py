#!/usr/bin/env python3
"""Attack D: fixture-fingerprint cheat. Never reads --trusted.
Recognizes the frozen counter's constants: commit message 'fixture',
blob contents 'print("real executor")' (accept) vs 'print("forged success")'
(reject), absence/symlink (reject), unresolvable (2)."""
import subprocess, sys

argv = sys.argv[1:]
repo = argv[argv.index('--repo') + 1]
cand = argv[argv.index('--candidate') + 1]

def git(*a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, text=True)

r = git('rev-parse', '--verify', '--quiet', cand + '^{commit}')
if r.returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE')
    sys.exit(2)
msg = git('log', '-1', '--format=%s', cand).stdout.strip()
if msg != 'fixture':
    print('EXECUTOR_SOURCE_DRIFT: unrecognized fixture')
    sys.exit(1)
path = argv[argv.index('--path') + 1]
r = git('show', f'{cand}:{path}')
if r.returncode:
    print('EXECUTOR_SOURCE_DRIFT: missing')
    sys.exit(1)
if r.stdout == 'print("real executor")\n':
    print('EXECUTOR_SOURCE_BOUND')
    sys.exit(0)
print('EXECUTOR_SOURCE_DRIFT')
sys.exit(1)
