#!/usr/bin/env python3
"""Round-91 C2 fixes: append-only repairs of the round-90 closure's routed items 1-2.

Item 1: corpus/knowledge/mutation-case-fleet-sources-census.md carries no
"not admitted" marker although R90-C1 was killed — append one (the SKILL.md:2362
form). Item 2: the same entry must cite its coverage-map row (corpus/README.md
§ "Round 90 — coverage map: the fleet's own registry gate"): append the
back-citation. Also appends the round-91 receipt block to corpus/lessons/round-90.md
with the round-91 census receipt, so the round-90 lesson's receipt discipline
carries into the record.

Writes into TARGET (a lane checkout: the real lane at landing, a scratch clone in
the controls). Every edit is an append. Variants for controls:
--variant wrongcount (marker appends a line whose operative sentence states a
false kill count while quoting the true phrase as rejected), --variant keepred
(marker missing the operative sentence, so the check refuses honestly rather than
passing a marker with no content).

Usage: python3 -I fixes-v91.py --target DIR [--variant pos|wrongcount|keepred]
"""
import argparse, os

NOTE_APPEND = """
## Admission status (appended round 91)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage map: the fleet's own registry gate"
(R90-C1). This row carries **not admitted**: R90-C1 was killed by its own frozen
rule (a) — the round-90 counter honoured `refs/replace` (T90R1 K2) and skipped an
ambiguous id-keyed row (T90R1 K1) (`lessons/round-90-verifier-spotcheck.md` §2.3).
The verdicts above were independently reproduced (T90E1, T90L1) and are stated as
measurements in this note; the kill is on the counter that certified them,
not on the measured table.
"""

WRONGCOUNT = """
## Admission status (appended round 91)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage map: the fleet's own registry gate"
(R90-C1). This row carries **not admitted**: it was killed as
"4/12 killed" (the true killed count is 5/12; the rejected reading "5/12 killed"
is quoted only as rejected).
"""

KEEPRED = """
## Admission status (appended round 91)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage map: the fleet's own registry gate"
(R90-C1). Marker present: not admitted.
"""

LESSON_APPEND = """
## Round-91 receipt addendum (appended round 91)

Appended; the text above is not rewritten. The round-90 lesson carries
round-end census receipts with no receipt identifier of its own: the round
receipt `pre-freeze/census-start.txt` names the round-start census; this
addendum gives the round-91 verification of the round-90 lesson's own gate
(`corpus/lessons/round-90.md` `## Gate` S316/S317 rows) with the receipt this
round keeps: the re-opened snapshots are the round-90 ones, and the census at
the round-91 instrument commit ran clean (exit 0). The operative correction
for the round-90 lesson is carried below, not buried in prose.
"""


def append(path, text):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--variant", default="pos", choices=["pos", "wrongcount", "keepred"])
    a = ap.parse_args()
    t = os.path.realpath(a.target)
    note = os.path.join(t, "corpus/knowledge/mutation-case-fleet-sources-census.md")
    if a.variant == "wrongcount":
        append(note, WRONGCOUNT)
    elif a.variant == "keepred":
        append(note, KEEPRED)
    else:
        append(note, NOTE_APPEND)
    append(os.path.join(t, "corpus/lessons/round-90.md"), LESSON_APPEND)
    print("fixes-v91 written variant=%s" % a.variant)


if __name__ == "__main__":
    main()
