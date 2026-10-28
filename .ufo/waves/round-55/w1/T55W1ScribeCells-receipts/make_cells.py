#!/usr/bin/env python3
"""Seat T55W1ScribeCells: build the seven uniform `scratch_root` cells.

Line-targeted so the diff is 7 changed lines, not a whole-file re-serialization.
Usage: python3 make_cells.py <registry.json in> <registry.json out>
"""
import json
import sys

TEMPLATE = (
    "Allocating-mode scratch-root class (round 55): on a set-but-unusable `TMPDIR`, "
    "exactly one stderr line and exit 2, `{prefix}: could-not-evaluate: cannot create "
    "clone scratch under the scratch root: TMPDIR is not a usable directory: "
    "'<value>' (could-not-evaluate)`, the value named with no "
    "`RuntimeError`/`Traceback` token on either stream; `TMPDIR` unset or empty (`''`) is "
    "the unset arm (the resolver skips an empty candidate, so the platform default "
    "applies); a usable `TMPDIR` holds every `mkdtemp` and the run creates nothing under "
    "`/tmp` (strace); scope: {modes}; {outside} "
    "(corpus/knowledge/scratch-root-contract.md)."
)

ROWS = [
    ("repeat-control-selftest", "repeat-control",
     "`--selftest` only",
     "`--snapshot` and the `--runs/--out` run mode allocate nothing and are outside it"),
    ("bash-witness-selftest", "WITNESS_STUDY",
     "`selftest` only",
     "`declare`, `run`, `rerun`, `count` and `check` allocate nothing and are outside it"),
    ("pin-disposition-selftest", "pin-disposition.py",
     "`--selftest` only",
     "the `--manifest/--root` read mode allocates nothing and is outside it"),
    ("evidence-disposition-selftest", "evidence-disposition.py",
     "`--selftest` only",
     "the `--json` disposition mode allocates nothing and is outside it"),
    ("context-capture-selftest", "context-capture.py",
     "`--selftest` only",
     "`--check` allocates nothing and is outside it"),
    ("registry-check-selftest", "registry-check",
     "`--selftest` and `--rev` (fleet-mirror clone)",
     "`--rev` sits on the unusable arm only (its usable path is `--selftest`, traced "
     "above) and the live `--root` mode opens no scratch root of its own"),
    ("env-diff-selftest", "ENVDIFF_SETUP",
     "`--selftest` and `--contract`",
     "no other mode allocates"),
]

CELLS = {name: TEMPLATE.format(prefix=p, modes=m, outside=o) for name, p, m, o in ROWS}


def patch(text):
    out, cur = [], None
    names = {n for n, *_ in ROWS}
    replaced = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith('"name": "'):
            cur = stripped[len('"name": "'):].rstrip('",\n')
        if '"scratch_root":' in line:
            assert cur in names, "scratch_root on unexpected row: %r" % cur
            # preserve the file's own indentation (the tree re-serializes at 3 spaces)
            indent = line[:len(line) - len(line.lstrip(" "))]
            out.append(indent + '"scratch_root": ' + json.dumps(CELLS[cur], ensure_ascii=False) + ",\n")
            replaced += 1
            continue
        out.append(line)
    assert replaced == 7, "replaced %d cells" % replaced
    return "".join(out)


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    text = open(src, encoding="utf-8").read()
    new = patch(text)
    json.loads(new)
    open(dst, "w", encoding="utf-8").write(new)
    print("wrote", dst, "rows:", len(json.loads(new)["rows"]))
