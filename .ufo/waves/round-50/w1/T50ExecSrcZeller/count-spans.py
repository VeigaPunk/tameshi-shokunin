#!/usr/bin/env python3
"""Print, per span, how many times it occurs in the two saved pdftotext extracts.

Demonstrates that pdftotext -layout loses spans that reading-order pdftotext keeps
(two-column interleave): the reading-order extract is the one to quote from.
Usage: python3 count-spans.py   (run from this directory)
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

SPANS = [
    ("input entity", "is reached, where removing any single input entity would cause the failure to disappear."),
    ("139 runs", "The case study required 139 automated test runs, or 35 minutes on a 500 MHz PC."),
    ("896 lines", "Likewise, it simplified 896 lines of HTML to the single line that caused the failure."),
    ("venue head", "IEEE TRANSACTIONS ON SOFTWARE ENGINEERING, VOL. 28, NO. 2, FEBRUARY 2002"),
]


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    raw = collapse(open(os.path.join(HERE, "zeller-delta.pdftotext-raw.txt")).read())
    layout = collapse(open(os.path.join(HERE, "zeller-delta.pdftotext-layout.txt")).read())
    print(f"{'span':13} {'reading-order':>13} {'-layout':>8}")
    for name, text in SPANS:
        needle = collapse(text)
        print(f"{name:13} {raw.count(needle):>13} {layout.count(needle):>8}")


if __name__ == "__main__":
    main()
