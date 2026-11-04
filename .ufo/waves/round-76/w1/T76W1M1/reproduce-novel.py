#!/usr/bin/env python3
"""Reproduce this seat's ONE mutation; writes only its scratch and cleans it."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
REV = '5b7bbe1afa209b477bc71872d2424f6993e5c69d'
S = Path('/fast/scratch/hyaku/tameshi-r76/T76W1M1')
OLD = b"self._git('ls-tree', '-r', '--name-only', rev, '--', path)"
NEW = b"self._git('ls-tree', '--name-only', rev, '--', path)"

def git(*args):
    return subprocess.check_output(['git', '-C', str(LANE), *args])

def load(path):
    spec = importlib.util.spec_from_file_location('probe', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

assert not S.exists(), 'scratch must be absent before reproduction'
S.mkdir(parents=True)
try:
    pristine = git('cat-file', 'blob', REV + ':.ufo/waves/round-76/l1/cand-wr-19.py')
    assert pristine.count(OLD) == 1
    path = S / 'novel.py'
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['TMPDIR'] = str(S)
    for phase, data in [('pristine', pristine), ('mutated', pristine.replace(OLD, NEW, 1)), ('restored', pristine)]:
        path.write_bytes(data)
        proc = subprocess.run(['python3', '-I', '-X', 'utf8', str(path), '--selftest'], cwd=S, env=env, capture_output=True, timeout=180)
        m = load(path)
        b, listings = m.fixture_rows()
        row = {'id': 'natural-arm15', 'kind': 'seat_reports', 'record': {'path': 'report.md', 'rev': m.REV, 'span': '12 seats', 'printed': 12}, 'wave': {'dir': 'wave', 'rev': m.REV}}
        natural = m.measure(row, {'lane': m.FixtureReader(b, listings)})
        directory = 'corpus/lessons'
        prefix = directory + '/'
        names = git('ls-tree', '-r', '--name-only', REV, '--', directory).decode().splitlines()
        count = sum(n.startswith(prefix) and '/' not in n[len(prefix):] and n.endswith('.md') for n in names)
        span = str(count) + ' reports'
        row = {'id': 'production-reader-boundary', 'kind': 'seat_reports', 'record': {'root': 'record', 'path': 'record.md', 'rev': REV, 'span': span, 'printed': count}, 'wave': {'dir': directory, 'rev': REV}}
        discriminator = m.measure(row, {'record': m.FixtureReader({(REV, 'record.md'): span.encode()}, {}), 'lane': m.GitReader(str(LANE))})
        print(json.dumps({'phase': phase, 'sha256': hashlib.sha256(data).hexdigest(), 'selftest_exit': proc.returncode, 'selftest_stdout': proc.stdout.decode(), 'selftest_stderr': proc.stderr.decode(), 'natural_arm15': natural, 'production_discriminator': discriminator}))
finally:
    if 'pristine' in locals():
        path.write_bytes(pristine)
        print('RESTORE_EXACT', path.read_bytes() == pristine)
    shutil.rmtree(S)
    print('SCRATCH_REMOVED', not S.exists())
