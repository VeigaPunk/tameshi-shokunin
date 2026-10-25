#!/usr/bin/env python3
"""Seat helper (never a measurement): apply declared mutants of mutants.json to any counter file and report.

  try-mutants.py --group freshness|coverage --file COUNTER.py [--ids F01,F02,...]

For every declared mutant (default: all of the group, neutral ones included) prints
`MUTANT <id> <kind> killed|survived|inapplicable`, then the pristine selftest verdict. A neutral mutant
must survive; a declared survivor you were assigned must be `killed`. The pristine run must PASS.
"""
import argparse
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('mutate', os.path.join(HERE, 'mutate.py'))
mutate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutate)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--group', required=True)
    ap.add_argument('--file', required=True)
    ap.add_argument('--ids')
    a = ap.parse_args()
    manifest = json.load(open(os.path.join(HERE, 'mutants.json')))
    muts = manifest['groups'][a.group]['mutants']
    if a.ids:
        want = set(a.ids.split(','))
        muts = [m for m in muts if m['id'] in want]
    source = open(a.file, 'rb').read()
    state, tail = mutate.run_selftest(source)
    print('PRISTINE %s %s' % (state, tail))
    for m in muts:
        mid, verdict, _ = mutate.judge(source, m)
        print('MUTANT %s %s %s' % (mid, m['kind'], verdict))


if __name__ == '__main__':
    main()
