#!/usr/bin/env python3
"""Split the C2 grammar arm's two predicates on the scored stderr lines.

The grammar arm requires BOTH (a) a stderr line matching measure.py's GRAMMAR
regex and (b) no `RuntimeError` token on either stream (plus rc == 2). This
script re-applies the two predicates to the exact stderr line each scored run
recorded, so a lost mode can be attributed to the prefix/end-shape or to the
token guard. Read-only; it re-parses the *.receipts.json written by the counter.
"""
import json
import pathlib
import re
import sys

GRAMMAR = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone "
    r"scratch under the scratch root: TMPDIR is not a usable directory: '.+' "
    r"\(could-not-evaluate\)$")

MODE_KEYS = ("repeat-control --selftest", "context-capture --selftest")


def line_of(value):
    match = re.search(r"stderr=\[(.*)\]$", value)
    return json.loads("[" + match.group(1) + "]")[0] if match else ""


def main(receipts_dir):
    root = pathlib.Path(receipts_dir)
    for path in sorted(root.glob("*.receipts.json")):
        data = json.loads(path.read_text())
        for key, value in data["bad"].items():
            if key not in MODE_KEYS:
                continue
            line = line_of(value)
            print("%-26s %-28s rc_in_value=%-3s grammar_match=%-5s token=%-5s"
                  % (path.stem, key,
                     value.split("rc=")[1].split()[0] if "rc=" in value else "?",
                     bool(GRAMMAR.match(line)), "RuntimeError" in line))
            print("    %r" % line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
