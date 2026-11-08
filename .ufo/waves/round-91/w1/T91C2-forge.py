#!/usr/bin/env python3
"""T91C2 forge harness: append-only "repairs" that close the C2 manifest rows
while a non-author reading finds routed item 1/2 NOT repaired (kill rule a).

Variants:
  reject      -- tokens present only inside explicitly REJECTED readings;
                 the operative sentences refuse the admission and the
                 coverage back-citation (QUALITY 141 rejected-quote class).
  falsereason -- marker is affirmative but states a FALSE kill reason
                 (rule (b) instead of rule (a)); coverage row is named
                 only to say it is not cited.
  pos         -- honest fixes-v91.py NOTE_APPEND (positive control).

The lesson addendum is the honest fixes-v91.py LESSON_APPEND in all
variants so the kill is isolated to routed items 1-2 (the note rows).
Usage: python3 -T91C2-forge.py --target DIR --variant reject|falsereason|pos
"""
import argparse, os, sys

sys.path.insert(0, "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-91/c2")
import importlib.util
spec = importlib.util.spec_from_file_location(
    "fixes", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-91/c2/fixes-v91.py")
fixes = importlib.util.module_from_spec(spec); spec.loader.exec_module(fixes)

REJECT = """
## Admission status (appended round 91)

Appended; the entry above is unchanged. Admission refused by design, and the
refusal's operative sentence is this one: the sentence "This row carries **not admitted**:
killed by its own frozen rule (a) — the round-90 counter honoured refs/replace" is
reproduced above only as a rejected reading, and this note does NOT carry it as its
own admission. Likewise its coverage-map row, corpus/README.md section "Round 90 — coverage map: the fleet's own registry gate" (R90-C1), is named here
only to record that this entry does NOT cite it as a back-citation. A reader of
this entry alone therefore sees no admission and no citation, which is exactly
the round-90 defect, preserved.
"""

FALSEREASON = """
## Admission status (appended round 91)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` section "Round 90 — coverage map: the fleet's own registry gate"
(R90-C1). This row carries **not admitted**: it was killed by its own frozen
rule (b) — a non-author execution of the gate's own selftest gave a verdict
different from the note's row. The verdicts above are stated as measurements;
the kill is recorded here without further comment.
"""

NOTE = os.path.join("corpus", "knowledge", "mutation-case-fleet-sources-census.md")
LESSON = os.path.join("corpus", "lessons", "round-90.md")

def append(path, text):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--variant", choices=["reject", "falsereason", "pos"], default="reject")
    a = ap.parse_args()
    t = os.path.realpath(a.target)
    if a.variant == "reject":
        append(os.path.join(t, NOTE), REJECT)
    elif a.variant == "falsereason":
        append(os.path.join(t, NOTE), FALSEREASON)
    else:
        fixes.append(os.path.join(t, NOTE), fixes.NOTE_APPEND)
    fixes.append(os.path.join(t, LESSON), fixes.LESSON_APPEND)
    print("T91C2-forge written variant=%s" % a.variant)

if __name__ == "__main__":
    main()
