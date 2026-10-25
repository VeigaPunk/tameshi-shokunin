#!/usr/bin/env python3
"""Seat-name collision gate (round 46, QUALITY criterion 90).

The orchestrator writes `<wave>-results.json` keyed by seat NAME; two lanes running a seat of the same name in
overlapping time make a results entry carry the other lane's output (round 45: ScribeSc... dead seat; round 46
wave 1: MutC1Counter and ScribeQuality, whose results entries named kake round-55 / round-45 reports).

  seat-name-check.py SPEC.json [--fleet DIR] [--hours N]
Exits 1 and prints `COLLISION <name> <registry path>` for every seat name of SPEC that also names a member of any
OTHER lane's .ufo/waves/**/swarm-registry.json modified within the last N hours (default 3: concurrent waves only); exit 0 otherwise;
exit 2 on setup errors. `--selftest` builds two fake lanes in a mktemp dir.
"""
import argparse
import glob
import json
import os
import sys
import tempfile
import time

FLEET = '/home/vgpnk/Projects/shokunin'
LANE = os.path.basename(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))


def members(path):
    try:
        raw = json.load(open(path, encoding='utf-8')).get('members', {})
    except (OSError, ValueError, AttributeError):
        return set()
    if isinstance(raw, dict):
        return {str(k) for k in raw}
    if isinstance(raw, list):
        return {str(m.get('name')) if isinstance(m, dict) else str(m) for m in raw}
    return set()


def collisions(spec_names, fleet, own, hours):
    out = []
    cutoff = time.time() - hours * 3600
    for reg in glob.glob(os.path.join(fleet, '*-shokunin', '.ufo', 'waves', '**', 'swarm-registry.json'), recursive=True):
        lane = os.path.relpath(reg, fleet).split(os.sep)[0]
        if lane == own or os.path.getmtime(reg) < cutoff:
            continue
        for name in sorted(spec_names & members(reg)):
            out.append((name, reg))
    return out


def selftest():
    with tempfile.TemporaryDirectory(prefix='tameshi-r46-names-') as d:
        for lane, names in (('a-shokunin', ['Alpha', 'Shared']), ('b-shokunin', ['Beta'])):
            p = os.path.join(d, lane, '.ufo', 'waves', 'round-1', 'w1')
            os.makedirs(p)
            json.dump({'members': {n: {} for n in names}}, open(os.path.join(p, 'swarm-registry.json'), 'w'))
        ok = []
        ok.append(('shared name found', {n for n, _ in collisions({'Shared', 'Gamma'}, d, 'b-shokunin', 72)} == {'Shared'}))
        ok.append(('own lane ignored', collisions({'Beta'}, d, 'b-shokunin', 72) == []))
        ok.append(('unique names clean', collisions({'T46Gamma'}, d, 'b-shokunin', 72) == []))
        old = os.path.join(d, 'a-shokunin', '.ufo', 'waves', 'round-1', 'w1', 'swarm-registry.json')
        os.utime(old, (time.time() - 10 * 3600, time.time() - 10 * 3600))
        ok.append(('old registry ignored by the window', collisions({'Shared'}, d, 'b-shokunin', 1) == []))
        bad = 0
        for name, good in ok:
            bad += not good
            print('%s %s' % ('PASS' if good else 'FAIL', name))
        print('SEAT_NAME_SELFTEST: cases=%d failed=%d' % (len(ok), bad))
        return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('spec', nargs='?')
    ap.add_argument('--fleet', default=FLEET)
    ap.add_argument('--hours', type=float, default=3)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.spec:
        ap.error('SPEC.json required')
    try:
        spec = json.load(open(a.spec, encoding='utf-8'))
        names = {i['name'] for i in spec['items']}
    except (OSError, ValueError, KeyError) as exc:
        print('setup error: %s' % exc, file=sys.stderr)
        return 2
    found = collisions(names, a.fleet, LANE, a.hours)
    for name, reg in found:
        print('COLLISION %s %s' % (name, os.path.relpath(reg, a.fleet)))
    print('SEAT_NAME_CHECK seats=%d collisions=%d' % (len(names), len(found)))
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
