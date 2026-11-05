#!/usr/bin/env python3
"""Resolve S305 page pointers claimed by round-86 artifacts against snapshot bytes.

Usage: pointer-check.py --snapshot PATH [--expect-mode N] [--expect-type N]
Prints one PASS/FAIL line per claimed pointer and a summary line.
Exit 0 iff every claimed pointer resolves to the claimed quote text.
"""
import argparse, html, re, sys

def rendered(lines, n):
    if n < 1 or n > len(lines):
        return None
    t = re.sub(r'<[^>]+>', '', lines[n - 1])
    return html.unescape(t).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--snapshot', required=True)
    ap.add_argument('--expect-mode', type=int, required=True,
                    help='claimed page line for the objectmode quote')
    ap.add_argument('--expect-type', type=int, required=True,
                    help='claimed page line for the objecttype quote')
    a = ap.parse_args()
    raw = open(a.snapshot, encoding='utf-8').read()
    lines = raw.split('\n')
    MODE = 'The mode of the object.'
    TYPE = 'The type of the object (commit, blob or tree).'

    fails = []
    # 1) physical 1-based scan: where does each quote actually sit?
    found = {}
    for i, l in enumerate(lines, 1):
        if MODE in l and 'mode' not in found:
            found['mode'] = i
        if TYPE.split('(')[0] in l and 'type' not in found:
            found['type'] = i
    for label, claimed, want in (('mode', a.expect_mode, MODE),
                                 ('type', a.expect_type, TYPE)):
        actual = found.get(label)
        got = rendered(lines, claimed)
        ok = (got == want)
        print(f"POINTER {label}: claimed_line={claimed} rendered={got!r} "
              f"expected={want!r} resolves={'yes' if ok else 'NO'} "
              f"actual_physical_line={actual}")
        if not ok:
            fails.append((label, claimed, actual))
    print(f"POINTER_SUMMARY claimed_mode={a.expect_mode} claimed_type={a.expect_type} "
          f"actual_mode={found.get('mode')} actual_type={found.get('type')} "
          f"resolved={2 - len(fails)}/2")
    # 2) literal-substring test on the RAW bytes (not rendered text)
    for label, q in (('mode', MODE), ('type', TYPE)):
        print(f"LITERAL {label}: raw_substring_present={q in raw}")
    return 1 if fails else 0

sys.exit(main())
