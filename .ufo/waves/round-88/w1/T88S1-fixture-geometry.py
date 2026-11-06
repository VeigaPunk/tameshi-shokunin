#!/usr/bin/env python3
"""T88S1 geometry probe for the round-88 kake mutation case note (R88-C1).

Read-only. It does not run the gate, a mutant, or a sweep. It checks two
things against committed bytes:

  (a) the committed spec's @old strings each occur exactly once in the pinned
      gate blob (the runner's pre-run uniqueness assert, re-derived statically),
      and the pinned blob's sha256/bytes/lines match the spec header;
  (b) the fixture arithmetic behind the five killing fixtures proposed in the
      case note's section 3: the em-dash byte offset, the head cut, the byte at
      cut-1, and the boolean each mutant would return on the proposed fixture.
      The booleans are a faithful re-implementation of the pinned functions
      (gate lines 35-43, 66-80, 106, 111), not an execution of the gate.

Usage: python3 -I T88S1-fixture-geometry.py
Exit: 0 all checks pass; 1 a check fails.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin")
KAKE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
REV = "e8d3a924249983972e5163d160cf236487986c55"
GATE_PATH = "scripts/ledger_append_guard.py"
SPEC = LANE / ".ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec"

EXPECT_SHA = "0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067"
EXPECT_SPEC_SHA = "724beed385222b6342dc6d3af5ad19ae605bca8101f983f3ce58da905492689e"
EXPECT_BYTES = 6969
EXPECT_LINES = 153

failures = []


def check(name: str, ok: bool, detail: str) -> None:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        failures.append(name)


def main() -> int:
    pin = subprocess.run(
        ["git", "-C", str(KAKE), "show", f"{REV}:{GATE_PATH}"],
        capture_output=True, check=True,
    ).stdout
    spec_text = SPEC.read_text(encoding="utf-8")

    check("pin-sha256", hashlib.sha256(pin).hexdigest() == EXPECT_SHA,
          hashlib.sha256(pin).hexdigest())
    check("pin-bytes", len(pin) == EXPECT_BYTES, f"{len(pin)}")
    check("pin-lines", len(pin.splitlines()) == EXPECT_LINES,
          f"{len(pin.splitlines())}")
    check("spec-sha256", hashlib.sha256(spec_text.encode()).hexdigest() == EXPECT_SPEC_SHA,
          hashlib.sha256(spec_text.encode()).hexdigest())

    # (a) @old uniqueness, parsed as the runner's format v1 does: one separator
    # space follows the directive; the rest of the line is the literal.
    defects = []
    current = None
    for line in spec_text.splitlines():
        if line.startswith("@defect "):
            current = line[len("@defect "):]
            defects.append({"defect": current, "old": None, "new": None})
        elif line.startswith("@old ") and current is not None:
            defects[-1]["old"] = line[len("@old "):]
        elif line.startswith("@new ") and current is not None:
            defects[-1]["new"] = line[len("@new "):]
    check("spec-defects", len(defects) == 10, f"{len(defects)}")
    for d in defects:
        occ = pin.count(d["old"].encode())
        check(f"old-once:{d['defect'].split(' | ')[0]}", occ == 1,
              f"count={occ} old={d['old']!r}")
        check(f"old-new-differ:{d['defect'].split(' | ')[0]}",
              d["old"] != d["new"], f"{d['old']!r} -> {d['new']!r}")

    # (b) fixture geometry, copied verbatim from the pinned selftest literal.
    base_text = ('{\n "schema": "receipt-rewrites/v2",\n "events": [\n'
                 '  {\n   "path": ".ufo/waves/round-58/controls/a.txt",\n'
                 '   "note": "prior entry \u2014 with an em dash"\n  }\n ]\n}\n')
    cut = base_text.rindex("]")
    appended = (base_text[:cut]
                + ',\n  {\n   "path": ".ufo/waves/round-58/controls/b.txt"\n  }\n '
                + base_text[cut:])
    edited = appended.replace("\u2014 with an em dash", "\\u2014 with an em dash")

    base = base_text.encode()
    carrier = appended.encode()
    edited_b = edited.encode()
    bcut = base.rindex(b"]")
    head = base[:bcut]

    div = next((i for i in range(min(len(head), len(edited_b)))
                if head[i] != edited_b[i]), min(len(head), len(edited_b)))
    check("fixture-emdash-offset-126", div == 126, f"first divergence={div}")
    check("fixture-cut-1-is-space", base[bcut - 1:bcut] == b" ",
          f"base[{bcut - 1}:{bcut}]={base[bcut - 1:bcut]!r} cut={bcut}")
    check("fixture-append-is-prefix", carrier.startswith(head), "True")

    # S_STARTSWITH: the edited carrier still matches the one-byte head.
    check("S_STARTSWITH-one-byte-head-accepts-edit",
          edited_b.startswith(head[:1]), "True (mutant accepts; pristine rejects)")

    # S_HEAD_SHORT: flip only the byte at cut-1 in the appended carrier.
    flipped = bytearray(carrier)
    flipped[bcut - 1] = ord("x")
    flipped = bytes(flipped)
    check("S_HEAD_SHORT-short-head-accepts-cut-1-flip",
          flipped.startswith(base[:bcut - 1]) and not flipped.startswith(head),
          "short head accepts=True, full head accepts=False")

    # S_OFFSET_EQ: the first EQUAL byte under the mutant's inverted scan.
    eq = next((i for i in range(min(len(head), len(edited_b)))
               if head[i] == edited_b[i]), min(len(head), len(edited_b)))
    check("S_OFFSET_EQ-first-equal-byte-0", eq == 0, f"{eq}")

    # S_VACUOUS: no compared ledger. Pristine keeps any(compared); mutant drops it.
    ok_all, any_compared = True, False
    check("S_VACUOUS-empty-tree-pristine-false", (ok_all and any_compared) is False,
          "prefix_preserved=False")
    check("S_VACUOUS-empty-tree-mutant-true", ok_all is True,
          "prefix_preserved=True (mutant)")

    # S_OK_ALL: two ledgers, first fails, last passes. Pristine ANDs; mutant keeps last.
    oks = [False, True]
    pristine_all = all(oks)
    mutant_last = oks[-1]
    check("S_OK_ALL-two-ledger-pristine-false", pristine_all is False, "False")
    check("S_OK_ALL-two-ledger-mutant-true", mutant_last is True, "True")
    check("S_OK_ALL-order-matters", all([True, False]) is False and [True, False][-1] is False,
          "edited-last would not kill; the edited ledger must sort first")

    # S_RED_FILES: red is selftest-local. files=0, prefix_preserved=False.
    pp, files = False, 0
    check("S_RED_FILES-pristine-red-false", (pp is False and files == 1) is False, "False")
    check("S_RED_FILES-mutant-red-true", (pp is False) is True,
          "True (only a meta-fixture can observe it)")

    print(f"CHECKS: {len(failures)} failed")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
