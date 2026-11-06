#!/usr/bin/env python3
"""T90R1 honest-note refusal probe for the frozen C1 counter (measure.py @ 3485ceb0).

Reuses probe_defects.py's scratch-clone runner (same lane reads at A_REV, same frozen
counter). Each variant is an HONEST note (its verdicts equal the derived ones) written in a
shape a case-note author could reasonably use; the counter should PASS it. A FAIL is an
honest-note refusal.

  R1-draft-column  survivor rows carry a drafted-arm result column whose cell reads KILLED
                   (the plan says the note carries a drafted killing arm per survivor)
  R2-verdict-words survivor verdict cell reads `SURVIVED (non-equivalent)`
  R3-indented      table rows indented by one space
  R4-measured-note `measured: 5/12 killed (5 KILLED, 7 SURVIVED)`

Usage: python3 -I probe_refusal.py --work EMPTY_DIR --measure /path/to/measure.py
"""
import argparse, os, sys
from concurrent.futures import ThreadPoolExecutor

import importlib.util
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("pdx", os.path.join(_here, "T90R1-probe-defects.py"))
pdx = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pdx)  # sibling saved source: same runner, same frozen counter


def table(rows_text, header):
    return "\n".join([header, "|---|---|---|---|"] + rows_text) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--measure", required=True)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    work = os.path.realpath(a.work)
    assert os.path.isdir(work) and not os.listdir(work)
    measure = os.path.realpath(a.measure)
    sources = pdx.pos_sources()
    readme = pdx.pos_readme()
    D = pdx.DERIVED
    head = "source: S999 fixture row (positive control only)\n\n# fixture note\n\nmeasured: 5/12 killed\n\n"

    def body(rows, header="| id | arm | verdict | witness |", extra_head=None):
        return (extra_head or head) + table(rows, header) + "\n"

    r1 = []
    for k, v in D.items():
        drafted = "—" if v == "KILLED" else "KILLED"
        r1.append("| %s | fixture arm | %s | differs | %s |" % (k, v, drafted))
    r1_note = (head + "| id | arm | verdict | witness | drafted arm result |\n|---|---|---|---|---|\n" +
               "\n".join(r1) + "\n")
    r2 = []
    for k, v in D.items():
        cell = "SURVIVED (non-equivalent)" if v == "SURVIVED" else "KILLED"
        r2.append("| %s | fixture arm | %s | differs |" % (k, cell))
    r2_note = body(r2)
    r3 = [" " + l for l in ["| C%02d | fixture arm | %s | differs |" % (i + 1, D["C%02d" % (i + 1)]) for i in range(12)]]
    r3_note = body(r3)
    r4_note = head.replace("measured: 5/12 killed", "measured: 5/12 killed (5 KILLED, 7 SURVIVED)") + table(
        ["| %s | fixture arm | %s | differs |" % (k, v) for k, v in D.items()], "| id | arm | verdict | witness |") + "\n"

    variants = [
        ("R1-draft-column", r1_note),
        ("R2-verdict-words", r2_note),
        ("R3-indented", r3_note),
        ("R4-measured-note", r4_note),
    ]
    if a.only:
        variants = [v for v in variants if v[0] in a.only]
    with ThreadPoolExecutor(2) as ex:
        futs = [ex.submit(pdx.run_variant, name,
                          {pdx.NOTE: note, "corpus/SOURCES.md": sources, "corpus/README.md": readme},
                          [], {}, work, measure) for name, note in variants]
        for f in futs:
            name, rev, rc, keep, _ = f.result()
            print("PROBE_VARIANT %s rev=%s exit=%d" % (name, rev, rc))
            for l in keep:
                print("PROBE_LINE %s %s" % (name, l))


if __name__ == "__main__":
    main()
