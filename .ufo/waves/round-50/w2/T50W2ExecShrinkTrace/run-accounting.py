#!/usr/bin/env python3
"""External run accounting for tools/shrink-case.py (round-50 C2, seat T50W2ExecShrinkTrace).

For each mutant of a frozen panel, apply the edit to a copy of tools/staged-id-guard.py, find a
counterexample with the frozen generator, run the shrinker under strace and compare the reported
`runs` with the execve count of each guard path; list every path opened for write.

  python3 run-accounting.py --rev-dir DIR --panel PANEL --scratch DIR --out DIR

DIR is a directory holding shrink-case.py, pbt-staged-id.py and staged-id-guard.py taken from the
revision under test (git archive). Nothing here decides a claim: it prints observed counts.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys

TRACE = 'execve,openat,unlinkat,renameat2'
SEED, CASES = '4949', '400'


def parse_trace(trace, pristine, mutant, outpath, tmpdir):
    """Guard execve per role; every write-open; the removes and renames."""
    ex, other, writes, dels, rens = collections.Counter(), [], [], [], []
    for line in open(trace, encoding='utf-8', errors='replace'):
        line = line.rstrip('\n')
        if 'execve(' in line:
            m = re.match(r'^(\d+)\s+execve\("([^"]*)", \[(.*)\], ', line)
            if not m:
                other.append(line[:160])
                continue
            args = [a.encode().decode('unicode_escape')
                    for a in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(3))]
            if len(args) >= 3 and args[1] == '-I' and args[2] in (pristine, mutant):
                ex['pristine' if args[2] == pristine else 'mutant'] += 1
            else:
                other.append(line[:220])
            continue
        m = re.match(r'^(\d+)\s+openat\((.*?), "(.*?)", ([A-Z0-9_|]+)(?:, [^)]*)?\)\s*=\s*(-?\d+)',
                     line)
        if m:
            path, flags = m.group(3), m.group(4)
            if any(f in flags for f in ('O_WRONLY', 'O_RDWR', 'O_CREAT', 'O_TRUNC', 'O_APPEND')):
                absolute = os.path.abspath(path)
                writes.append({'path': path, 'flags': flags, 'ret': int(m.group(5)),
                               'in_tmp': os.path.commonpath([absolute, tmpdir]) == tmpdir,
                               'is_out': absolute == os.path.abspath(outpath)})
            continue
        if ' unlinkat(' in line:
            dels.append(line[line.index('unlinkat('):][:220])
        elif ' renameat2(' in line:
            rens.append(line[line.index('renameat2('):][:220])
    return ex, other, writes, dels, rens


def units(case):
    n = len(case['registry'].splitlines(True)) + len(case['staged'].splitlines(True))
    mp = case.get('map')
    return n + (len(mp['map']) if isinstance(mp, dict) and isinstance(mp.get('map'), dict) else 0)


def find_case(gen, mutant, dump, work, scratch):
    proc = subprocess.run([sys.executable, '-I', gen, '--guard', mutant, '--seed', SEED,
                           '--cases', CASES, '--dump', dump], capture_output=True,
                          env=dict(os.environ, TMPDIR=work), cwd=scratch)
    last = proc.stdout.decode('utf-8', 'replace').strip().split('\n')[-1]
    m = re.search(r'counterexample=(\d+)', last)
    if m is None:
        return None, last
    index = int(m.group(1))
    for raw in open(dump, encoding='utf-8'):
        row = json.loads(raw)
        if row.get('index') == index:
            return {'registry': row['registry'], 'staged': row['staged'], 'map': row['map']}, last
    return None, last


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--rev-dir', required=True)
    ap.add_argument('--panel', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    shrink = os.path.join(args.rev_dir, 'shrink-case.py')
    gen = os.path.join(args.rev_dir, 'pbt-staged-id.py')
    guard = open(os.path.join(args.rev_dir, 'staged-id-guard.py'), encoding='utf-8').read()
    panel = json.load(open(args.panel, encoding='utf-8'))
    os.makedirs(args.out, exist_ok=True)
    rows = []
    for mutant in panel['mutants']:
        mid = mutant['id']
        root = os.path.join(args.scratch, mid)
        for name in ('guard', 'tmp', 'run', 'out'):
            os.makedirs(os.path.join(root, name), exist_ok=True)
        pristine = os.path.join(root, 'guard', 'pristine.py')
        mpath = os.path.join(root, 'guard', 'mutant.py')
        open(pristine, 'w', encoding='utf-8').write(guard)
        open(mpath, 'w', encoding='utf-8').write(guard.replace(mutant['old'], mutant['new']))
        case, last = find_case(gen, mpath, os.path.join(root, 'dump.jsonl'),
                               os.path.join(root, 'tmp'), os.path.join(root, 'run'))
        if case is None:
            rows.append({'id': mid, 'found': False, 'gen': last})
            continue
        cpath = os.path.join(root, 'case.json')
        json.dump(case, open(cpath, 'w'), sort_keys=True)
        opath = os.path.join(root, 'out', 'out.json')
        trace = os.path.join(root, 'trace.txt')
        proc = subprocess.run(['strace', '-f', '-yy', '-s', '8192', '-e', 'trace=' + TRACE,
                               '-o', trace, sys.executable, '-I', shrink,
                               '--pristine', pristine, '--mutant', mpath,
                               '--case', cpath, '--out', opath], capture_output=True,
                              env=dict(os.environ, TMPDIR=os.path.join(root, 'tmp')),
                              cwd=os.path.join(root, 'run'))
        ex, other, writes, dels, rens = parse_trace(trace, pristine, mpath, opath,
                                                    os.path.join(root, 'tmp'))
        out = json.load(open(opath, encoding='utf-8')) if os.path.exists(opath) else None
        row = {'id': mid, 'found': True, 'gen': last, 'rc': proc.returncode,
               'case_units': units(case),
               'runs': out['runs'] if out else None,
               'units_before': out['units_before'] if out else None,
               'units_after': out['units_after'] if out else None,
               'traced_pristine': ex['pristine'], 'traced_mutant': ex['mutant'],
               'other_execve': len(other),
               'writes_in_tmp': sum(1 for w in writes if w['in_tmp']),
               'writes_out': sum(1 for w in writes if w['is_out']),
               'writes_outside': [w['path'] for w in writes
                                  if not w['in_tmp'] and not w['is_out']],
               'unlinkat': len(dels), 'renameat2': len(rens)}
        row['match'] = row['runs'] is not None and row['runs'] == row['traced_pristine'] + row['traced_mutant']
        rows.append(row)
        print('%-4s runs=%s traced=%s/%s units=%s->%s outside=%d' % (
            mid, row['runs'], row['traced_pristine'], row['traced_mutant'],
            row['units_before'], row['units_after'], len(row['writes_outside'])))
    json.dump(rows, open(os.path.join(args.out, 'run-accounting.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
