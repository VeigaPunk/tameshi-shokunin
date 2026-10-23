#!/usr/bin/env python3
"""F6 fixture generator — round-29 C2 v2, seat BuildF6B.

Builds the ORIGINAL fixture anchored on the PINNED kagi declaration
(corpus/surface-census.tsv at REV_BASH = fecee8743e52eb8fb5fbb40782934cb619a1a96e):

  census.tsv    byte-identical to the pinned corpus/surface-census.tsv
  shapes.tsv    a subset of the pinned corpus/state-shape.tsv lines
  baseline.tsv  a subset of the pinned corpus/drift-baseline.tsv lines
  host.tsv      a manifest: <relative path>\\t<dir|file>\\t<octal mode>\\t<content>

The drift is one exec row whose live file lacks the execute bit: the pinned
gate then prints 'SURFACE DIVERGED ... (declared exec, no execute bit)'.

The reduction step imports the FROZEN COUNTER's own ddmin() and Oracle.kills()
from .ufo/evidence/round-29/c2-measure-v2.py -- nothing is reimplemented here.

Usage:
  generate-f6.py build   --out DIR [--drift-row REL] [--drift-mode M]
  generate-f6.py reduce  --original DIR --out DIR
"""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import time

COUNTER = os.environ.get('F6_COUNTER', '/tmp/BuildF6B-r29/.ufo/evidence/round-29/c2-measure-v2.py')
KAGI = os.environ.get('F6_KAGI', '/home/vgpnk/Projects/shokunin/kagi-shokunin')
REV_BASH = 'fecee8743e52eb8fb5fbb40782934cb619a1a96e'
REPO = os.environ.get('F6_REPO', '/tmp/BuildF6B-r29')
FILES = ('census.tsv', 'shapes.tsv', 'baseline.tsv', 'host.tsv')
DRIFT_ROW = '.config/the-janitor/client.py'
DRIFT_MODE = '644'
HOME_PREFIX = '$HOME/'


def load_counter(path=COUNTER):
    spec = importlib.util.spec_from_file_location('c2v2', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = load_counter()


def git_show(repo, rev, path):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    p = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)],
                       capture_output=True, env=env)
    if p.returncode:
        raise RuntimeError('%s: %s' % (path, p.stderr.decode()))
    return p.stdout


def pinned_bytes(path):
    return git_show(KAGI, REV_BASH, path)


def pinned_lines(path):
    raw = pinned_bytes(path).decode('utf-8', 'surrogateescape')
    ls = raw.split('\n')
    if ls and ls[-1] == '':
        ls.pop()
    return ls


def census_rows(lines):
    """[(relpath, class, kind, mode, note)] for the data rows of a census."""
    rows = []
    for line in lines:
        if not line or line.startswith('#'):
            continue
        f = line.split('\t')
        if len(f) < 4:
            raise ValueError('short census row: %r' % line)
        if not f[0].startswith(HOME_PREFIX):
            raise ValueError('unmapped census path: %r' % f[0])
        rows.append((f[0][len(HOME_PREFIX):], f[1], f[2], f[3], f[4] if len(f) > 4 else ''))
    return rows


def manifest_lines(rows, drift_row=None, drift_mode=None):
    """host.tsv manifest lines: <rel>\\t<dir|file>\\t<octal mode>\\t<content>."""
    out = []
    seen = set()
    for rel, cls, kind, mode, note in rows:
        if rel in seen:
            raise ValueError('duplicate path %r' % rel)
        seen.add(rel)
        m = drift_mode if (drift_row is not None and rel == drift_row) else mode
        if m == '-':
            m = '700'          # '-' means unchecked mode; give the node a concrete one
        if kind == 'dir':
            out.append('%s\tdir\t%s\t\n' % (rel, m))
        else:
            out.append('%s\tfile\t%s\tx\n' % (rel, m))
    return out


def build_original(drift_row=DRIFT_ROW, drift_mode=DRIFT_MODE):
    """Return {file: bytes} for the original fixture.

    census.tsv   byte-identical to the pinned corpus/surface-census.tsv
    shapes.tsv   empty: a subset of the pinned state-shape.tsv lines.  Every pinned
                 shape row pins a real host artifact (sqlite magic, 16 KiB log
                 floor, JSON key lists); a synthetic host cannot satisfy them
                 without adding divergences of its own.
    baseline.tsv the pinned drift-baseline lines (a subset of the pinned file).
                 The gate consumes only its mode column, and every mode there
                 agrees with the pinned census, so the cross-check arm stays clean.
    host.tsv     one node per declared census row, at its declared mode, so the
                 only divergence the pristine reports is the drifted exec row.
    """
    census = pinned_bytes('corpus/surface-census.tsv')       # byte-identical, no trailing NL
    rows = census_rows(pinned_lines('corpus/surface-census.tsv'))
    baseline = pinned_lines('corpus/drift-baseline.tsv')
    host = ''.join(manifest_lines(rows, drift_row, drift_mode))
    return {
        'census.tsv': census,
        'shapes.tsv': b'',
        'baseline.tsv': ''.join(l + '\n' for l in baseline).encode('utf-8'),
        'host.tsv': host.encode('utf-8'),
    }


def write_fixture(directory, files):
    os.makedirs(directory, exist_ok=True)
    for name, data in files.items():
        with open(os.path.join(directory, name), 'wb') as h:
            h.write(data)
    return directory


def read_fixture_bytes(directory):
    out = {}
    for name in FILES:
        with open(os.path.join(directory, name), 'rb') as h:
            out[name] = h.read()
    return out


def fixture_dict(files):
    """The counter's own view of a fixture: file -> list of lines."""
    def ls(raw):
        text = raw.decode('utf-8', 'surrogateescape')
        out = text.split('\n')
        if out and out[-1] == '':
            out.pop()
        return out
    return {name: ls(files[name]) for name in FILES}


def make_oracle(work):
    gate = pinned_bytes('corpus/surface-census.sh')
    runner = git_show(REPO, 'HEAD', 'tools/mutate-and-run.sh').decode('utf-8', 'surrogateescape')
    mutant = C.b5_mutant(runner, gate.decode('utf-8', 'surrogateescape'))
    if mutant is None:
        raise RuntimeError('the runner B5 spec did not apply to the pinned gate')
    os.makedirs(work, exist_ok=True)
    pg = os.path.join(work, 'pristine.sh')
    mg = os.path.join(work, 'mutant-B5.sh')
    open(pg, 'wb').write(gate)
    open(mg, 'w', encoding='utf-8', errors='surrogateescape').write(mutant)
    return C.Oracle(pg, mg, work)


def cmd_build(a):
    files = build_original(a.drift_row, a.drift_mode)
    write_fixture(a.out, files)
    print('built original fixture at %s' % a.out)
    for name in FILES:
        p = os.path.join(a.out, name)
        print('  %-12s %5d bytes  sha256=%s' % (name, os.path.getsize(p),
              subprocess.run(['sha256sum', p], capture_output=True).stdout.decode().split()[0]))
    return 0


def cmd_reduce(a):
    work = '/tmp/BuildF6B-work/reduce'
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    orc = make_oracle(work)
    orig = read_fixture_bytes(a.original)
    fx = fixture_dict(orig)
    units = C.to_units(fx)
    print('units before: %d' % len(units))
    t0 = time.time()
    got = C.ddmin(units, orc.kills)
    dt = time.time() - t0
    print('units after:  %d' % len(got))
    print('oracle tests:  %d' % orc.n)
    print('wall time:     %.1f s' % dt)
    mini = C.from_units(got)
    out = {}
    for name in FILES:
        text = ''.join(l + '\n' for l in mini[name])
        out[name] = text.encode('utf-8')
    write_fixture(a.out, out)
    with open(os.path.join(work, 'ddmin-units.txt'), 'w') as h:
        for f, i, line in got:
            h.write('%s\t%d\t%s\n' % (f, i, line))
    print('minimized written to %s' % a.out)
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build')
    b.add_argument('--out', required=True)
    b.add_argument('--drift-row', default=DRIFT_ROW)
    b.add_argument('--drift-mode', default=DRIFT_MODE)
    b.set_defaults(fn=cmd_build)
    r = sub.add_parser('reduce')
    r.add_argument('--original', required=True)
    r.add_argument('--out', required=True)
    r.set_defaults(fn=cmd_reduce)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == '__main__':
    raise SystemExit(main())
