#!/usr/bin/env python3
"""Self-test for duplint2.py — the lint must FIRE on planted defects and
STAY SILENT on clean bytes.  Exits 0 when every case behaves as declared.

Cases:
  T1  known-fixed pattern 1 planted -> K1 fires
  T2  known-fixed pattern 2 planted -> K1 fires
  T3  doubled word planted -> D1 fires
  T4  adjacent duplicate parenthetical planted -> D2 fires
  T5  clean text -> no findings
"""

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# the lint script sits beside this file under either its scratch name
# (duplint2.py) or its lane-deliverable name.
LINT = None
for name in ("T53W2ExecDupLint.duplint.py", "duplint2.py"):
    cand = os.path.join(HERE, name)
    if os.path.exists(cand):
        LINT = cand
        break
if LINT is None:
    raise SystemExit("lint script not found beside %s" % HERE)
spec = importlib.util.spec_from_file_location("duplint2", LINT)
dl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dl)

HEAD = "# Test\n\n"


def run(text):
    """Lint an in-memory page by writing a fake git repo? No -- call the
    per-page helpers directly so the self-test needs no git."""
    sections, fenced = dl.sectionize(text)
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    findings = []
    for pat in dl.KNOWN_FIXED_LITERAL:
        if pat in text:
            findings.append(("K1", pat))
    for rx, label in dl.KNOWN_FIXED_REGEX:
        import re as _re
        if _re.search(rx, text):
            findings.append(("K1", label))
    for i, line in enumerate(lines, 1):
        for pos, frag in dl.doubled_words(line):
            findings.append(("D1", frag))
        spans = dl.parens(line)
        for a in range(len(spans)):
            for b in range(a + 1, len(spans)):
                s1, e1, c1 = spans[a]
                s2, e2, c2 = spans[b]
                if c1.strip() == c2.strip() and len(c1.strip()) >= 3:
                    findings.append(("D2", c1.strip()))
                n1, n2 = dl._norm_qualifier(c1), dl._norm_qualifier(c2)
                if len(n1) >= 3 and n1 == n2:
                    gap = line[e1:s2]
                    if gap.strip(" \t,;:.—–-()[]\"'") == "":
                        findings.append(("D6", c1.strip()))
    return findings


CASES = [
    (
        "T1 known-fixed pattern 1",
        HEAD + "The runner replays **six** in r10-2 (**ten** since round 51) (ten since round 51)\nembedded legs.\n",
        lambda f: any(ax == "K1" for ax, _ in f),
        True,
    ),
    (
        "T2 known-fixed pattern 2",
        HEAD + "Cases 5-6 were still not embedded at this boundary (both are legs 5-6 since round 10-2 - x).\n",
        lambda f: any(ax == "K1" for ax, _ in f),
        True,
    ),
    (
        "T3 doubled word",
        HEAD + "The the registry row holds.\n",
        lambda f: any(ax == "D1" for ax, _ in f),
        True,
    ),
    (
        "T4 adjacent duplicate parenthetical",
        HEAD + "The registry (ten since round 51) (ten since round 51) holds.\n",
        lambda f: any(ax == "D2" for ax, _ in f),
        True,
    ),
    (
        "T4b duplicate qualifier on one item (emphasis variant)",
        HEAD + "The runner replays **six** in r10-2 (**ten** since round 51) (ten since round 51)\nembedded legs.\n",
        lambda f: any(ax == "D6" for ax, _ in f),
        True,
    ),
    (
        "T5 clean text",
        HEAD + "The registry row holds ten cases since round 51.\n",
        lambda f: len(f) == 0,
        True,
    ),
    (
        "T6 CLI metavariable pair is not a doubled word",
        HEAD + "Run `python3 tools/registry-check.py --rev REV --tag TAG` for the row.\n",
        lambda f: not any(ax == "D1" for ax, _ in f),
        True,
    ),
]

failed = 0
for name, text, pred, _want in CASES:
    f = run(text)
    ok = pred(f)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: findings={f}")
    if not ok:
        failed += 1
print(f"selftest: {len(CASES) - failed}/{len(CASES)} pass")
sys.exit(0 if failed == 0 else 1)
