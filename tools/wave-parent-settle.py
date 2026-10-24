#!/usr/bin/env python3
"""wave-parent-settle.py — classify whether a wave parent outlived its seats.

A dispatch is SETTLED only when every seat has a terminal timestamp and the
parent process exit is at or after the latest seat terminal. A parent that
exits while seats are still running is UNSETTLED (the round-38 failure shape).
This tool does not spawn seats and does not replace dead ones.

Exit codes: 0 SETTLED · 1 UNSETTLED · 2 usage · 0 also for a passing selftest.
"""
import argparse
import json
import sys


def classify(receipt):
    seats = receipt.get('seats')
    parent_exit = receipt.get('parent_exit_unix')
    if not isinstance(seats, list) or not seats:
        return 'UNSETTLED', 'no seats'
    if not isinstance(parent_exit, int):
        return 'UNSETTLED', 'parent_exit_unix missing'
    terminals = []
    for seat in seats:
        name = seat.get('name', '?')
        terminal = seat.get('terminal_unix')
        if not isinstance(terminal, int):
            return 'UNSETTLED', 'seat %s has no terminal' % name
        terminals.append(terminal)
    last = max(terminals)
    if parent_exit < last:
        return 'UNSETTLED', 'parent exited before last seat terminal'
    return 'SETTLED', 'parent exit >= last seat terminal'


def selftest():
    red = {
        'parent_exit_unix': 10,
        'seats': [{'name': 'a', 'terminal_unix': 20}],
    }
    green = {
        'parent_exit_unix': 30,
        'seats': [
            {'name': 'a', 'terminal_unix': 20},
            {'name': 'b', 'terminal_unix': 25},
        ],
    }
    none = {'parent_exit_unix': 30, 'seats': [{'name': 'a'}]}
    checks = (
        ('red', red, 'UNSETTLED'),
        ('green', green, 'SETTLED'),
        ('missing-terminal', none, 'UNSETTLED'),
    )
    failed = []
    for label, receipt, want in checks:
        got, _detail = classify(receipt)
        if got != want:
            failed.append('%s: want %s got %s' % (label, want, got))
    print('WAVE_PARENT_SELFTEST: %d/3 pass' % (3 - len(failed)))
    for item in failed:
        print('FAIL %s' % item)
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(description='classify wave parent settlement')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--receipt', metavar='PATH')
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.receipt:
        ap.print_usage(sys.stderr)
        return 2
    with open(args.receipt, encoding='utf-8') as fh:
        receipt = json.load(fh)
    verdict, detail = classify(receipt)
    print('WAVE_PARENT: verdict=%s detail=%s' % (verdict, detail))
    return 0 if verdict == 'SETTLED' else 1


if __name__ == '__main__':
    sys.exit(main())
