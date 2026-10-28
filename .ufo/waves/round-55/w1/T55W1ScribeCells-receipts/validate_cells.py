#!/usr/bin/env python3
"""Seat T55W1ScribeCells: check the seven cells against the measured lines.

Asserts, for the registry at argv[1] and the measured first-stderr-line files in
argv[2] (one <tool>.err per allocating mode):
  * exactly seven rows carry `scratch_root`, all seven are the selftest rows;
  * the file stays ASCII;
  * every cell matches one template shape;
  * every cell quotes the prefix that the tool actually printed;
  * every cell carries the frozen marker, "exit 2", "'<value>'", the unset arm,
    the /tmp claim and a scope clause.
Prints one JSON verdict; exit 0 iff every check holds.
"""
import json
import pathlib
import re
import sys

MARKER = "could-not-evaluate: cannot create clone scratch under the scratch root"
TEMPLATE = re.compile(
    r"^Allocating-mode scratch-root class \(round 55\): on a set-but-unusable `TMPDIR`, "
    r"exactly one stderr line and exit 2, `(?P<prefix>[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?): "
    r"could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is "
    r"not a usable directory: '<value>' \(could-not-evaluate\)`, the value named with no "
    r"`RuntimeError`/`Traceback` token on either stream; `TMPDIR` unset or empty "
    r"\(`''`\) is the unset arm \(the resolver skips an empty candidate, so the platform "
    r"default applies\); a usable `TMPDIR` holds every `mkdtemp` and the run creates "
    r"nothing under `/tmp` \(strace\); scope: (?P<modes>.+?); (?P<outside>.+?) "
    r"\(corpus/knowledge/scratch-root-contract\.md\)\.$")

# measured first stderr token per allocating mode -> the row's cell
ROW_TO_RECEIPT = {
    "repeat-control-selftest": "repeat-control.err",
    "registry-check-selftest": "registry-check.err",
    "bash-witness-selftest": "bash-witness-study.err",
    "pin-disposition-selftest": "pin-disposition.err",
    "evidence-disposition-selftest": "evidence-disposition.err",
    "context-capture-selftest": "context-capture.err",
    "env-diff-selftest": "env-diff-selftest.err",
}

def main(registry_path, receipts_dir):
    raw = pathlib.Path(registry_path).read_bytes()
    data = json.loads(raw)
    cells = {r["name"]: r["scratch_root"] for r in data["rows"] if "scratch_root" in r}
    problems = []
    if len(cells) != 7:
        problems.append("cells=%d" % len(cells))
    if sum(1 for b in raw if b > 127):
        problems.append("non-ascii bytes")
    prefixes = {}
    for row, receipt in ROW_TO_RECEIPT.items():
        cell = cells.get(row)
        if cell is None:
            problems.append("%s: no cell" % row)
            continue
        for needle in (MARKER, "exit 2", "'<value>'", "unset arm", "`/tmp`", "scope: "):
            if needle not in cell:
                problems.append("%s: missing %r" % (row, needle))
        m = TEMPLATE.match(cell)
        if not m:
            problems.append("%s: shape" % row)
            continue
        first = pathlib.Path(receipts_dir, receipt).read_text().splitlines()[0]
        actual = first.split(": could-not-evaluate: ")[0]
        prefixes[row] = {"cell": m.group("prefix"), "measured": actual}
        if m.group("prefix") != actual:
            problems.append("%s: prefix %r != measured %r" % (row, m.group("prefix"), actual))
    print(json.dumps({"rows": len(data["rows"]), "cells": len(cells),
                      "prefixes": prefixes, "problems": problems,
                      "ok": not problems}, indent=1, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
