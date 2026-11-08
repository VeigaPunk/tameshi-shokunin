#!/usr/bin/env python3
"""R93M1 sharpened probes — states the committed battery does not have.

For each rule that a committed battery state fails to discriminate (or never
exercises), build the minimal sharpened state that does, and run the frozen
counter (baseline) and the single-edit mutant side by side. A probe is NOT part
of the committed battery: it shows that the rule is load-bearing and that the
gap is the battery's state set, not the rule's reality.

Probe states are committed only inside scratch clones at the instrument revision,
under the fixture identity ctl <ctl@fixture.invalid>.

Usage: python3 R93M1-sharp.py
"""
import hashlib
import importlib.util
import os
from concurrent.futures import ThreadPoolExecutor

MAIN = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-93/w1/R93M1-harness.py"
OUT = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-93/w1/R93M1-sharp-output.txt"

spec = importlib.util.spec_from_file_location("r93m1", MAIN)
H = importlib.util.module_from_spec(spec)
spec.loader.exec_module(H)

H.verify_inputs()
H.D = H.load_driver()
H.STATES = H.D.states(H.LANE)
D = H.D
os.makedirs(os.path.join(H.S, "jobs"), exist_ok=True)
os.makedirs(H.OUTDIR, exist_ok=True)

NOTE = "corpus/knowledge/mutation-case-fleet-sources-census.md"
LESSON = "corpus/lessons/round-93.md"
real_note = open(os.path.join(H.LANE, NOTE), encoding="utf-8").read()
lesson = open(os.path.join(H.LANE, LESSON), encoding="utf-8").read()

QUOTE = ("A fenced code block begins with a code fence, preceded by up to three "
         "spaces of indentation.")
WRONG = ("A fence marker may be preceded by any number of blank lines before it "
         "opens a literal block.")
assert QUOTE in lesson and QUOTE not in WRONG

VHEAD = "| id | arm targeted | edit | verdict | witness |"
PAIR = VHEAD + "\n|---|---|---|---|---|"
assert real_note.count(PAIR) == 1
C01 = ("| C01 | E10 community-at-A | `:668` `kind==\"community\"` → "
       "`kind==\"communityX\"` | KILLED | validate; one community row at tier A (S001) |")
C12 = ("| C12 | used-by comma-list trimming | `:564` `path=$(trim_cell \"$path\")` → "
       "`path=$path` | SURVIVED | validate; used-by `corpus/a.md, corpus/b.md`, both present |")
assert real_note.count(C01) == 1 and real_note.count(C12) == 1
C01_4 = C01.rsplit(" | ", 1)[0] + " |"          # drop the witness cell
C12_4 = C12.rsplit(" | ", 1)[0] + " |"

PX = {
 # PX1: the S322 quote still exists and is located, but does not occur in the snapshot.
 "px1-source-wrongquote": dict(
     files={LESSON: lesson.replace(QUOTE, WRONG, 1)}, frozen=(1, {"source": False})),
 # PX2a: only the delimiter row loses a cell (GFM would not recognize the table).
 "px2-delim-only": dict(
     files={NOTE: real_note.replace(PAIR, VHEAD + "\n|---|---|---|---|", 1)},
     frozen=(0, {"__pass": True})),
 # PX2b: the last data row loses the witness cell; the verdict stays in its column.
 "px2-width-lastrow": dict(
     files={NOTE: real_note.replace(C12, C12_4, 1)}, frozen=(1, {"ids": False})),
 # PX2c: the first data row loses the witness cell (the `delim` block's only input).
 "px2-width-firstrow": dict(
     files={NOTE: real_note.replace(C01, C01_4, 1)}, frozen=(1, {"ids": False})),
 # PX3: the committed `position` state minus its duplicate C12 row.
 "px3-position-nodup": dict(
     files={NOTE: D.note_text(header="| id | arm | witness | verdict |", extra="")},
     frozen=(1, {"ids": False})),
 # PX4: the hidden C001-C012 table inside a fence (the S322 declared limit).
 "px4-fenced-hidden": dict(
     files={NOTE: real_note + "\n```\n" + D.HIDDEN3.strip("\n") + "\n```\n"},
     frozen=(0, {"__pass": True})),
 # PX5: a header with two `verdict` cells.
 "px5-two-verdict-cols": dict(
     files={NOTE: D.note_text(header="| id | arm | verdict | verdict |")},
     frozen=(1, {"ids": False})),
 # PX6: two block-level measured lines, the first one true.
 "px6-figure-two": dict(
     files={NOTE: D.note_text(extra="measured: 5/12 killed\n")},
     frozen=(1, {"figure": False})),
}

# probe, mutant, targeted conjunct, expectation for the mutant's removal effect
PROBES = [("px1-source-wrongquote", "D22", "source", (0, {"__pass": True})),
          ("px2-width-lastrow", "D17", "ids", (0, {"__pass": True})),
          ("px2-width-firstrow", "D18", "ids", (1, {"ids": False})),
          ("px3-position-nodup", "D16", "ids", (1, {"ids": True})),
          ("px4-fenced-hidden", "D29", "verdict_tables", (1, {"verdict_tables": False})),
          ("px5-two-verdict-cols", "D30", "ids", (0, {"__pass": True})),
          ("px6-figure-two", "D26", "figure", (0, {"__pass": True}))]


def main():
    pristine = open(H.PRISTINE, "rb").read().decode()
    M = {m["id"]: m for m in H.mutants(pristine)}
    jobs = []
    for name, mid, key, want in PROBES:
        H.STATES[name] = PX[name]
        jobs.append(dict(label="sbase-" + name, state=name, expect=PX[name]["frozen"],
                         detector=True, counter=H.PRISTINE))
        p, sha, norm = H.write_mutant(M[mid]["text"], "sharp-" + mid)
        jobs.append(dict(label="smut-%s-%s" % (name, mid), state=name, expect=want,
                         detector=True, counter=p))
    # PX2a is a frozen-only probe (the delimiter-width rule has no mutant to kill:
    # the counter never reads the delimiter row at all).
    H.STATES["px2-delim-only"] = PX["px2-delim-only"]
    jobs.append(dict(label="sbase-px2-delim-only", state="px2-delim-only",
                     expect=(0, {"__pass": True}), detector=True, counter=H.PRISTINE))
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = {r["label"]: r for r in ex.map(H._run_job, jobs)}
    lines = ["R93M1 sharpened probes (NOT committed battery states)",
             "instrument " + hashlib.sha256(open(H.PRISTINE, "rb").read()).hexdigest(),
             "",
             "px2-delim-only (frozen only): a 5-cell verdict header over a 4-cell delimiter"]
    b = res["sbase-px2-delim-only"]
    lines.append("  baseline exit=%d grade=%s pass=%s badrows_line=%s" % (
        b["exit"], "MATCH" if b["grade"] else "FAIL",
        "true" if "C1_R93_PASS=true" in b["body"] else "false",
        "yes" if "C1_BADROWS" in b["body"] else "no"))
    lines.append("")
    for name, mid, key, want in PROBES:
        b = res["sbase-" + name]
        m = res["smut-%s-%s" % (name, mid)]
        cb, cm = D.conj_of(b["body"]), D.conj_of(m["body"])
        badb = [l for l in b["body"].split("\n") if l.startswith("C1_BADROWS")]
        badm = [l for l in m["body"].split("\n") if l.startswith("C1_BADROWS")]
        lines.append("%s mutant=%s rule_key=%s" % (name, mid, key))
        lines.append("  baseline exit=%d grade=%s %s=%s pass=%s badrows=%d" % (
            b["exit"], "MATCH" if b["grade"] else "FAIL", key, cb.get(key),
            "true" if "C1_R93_PASS=true" in b["body"] else "false",
            len(badb[0].split()) - 1 if badb else 0))
        lines.append("  mutant   exit=%d grade=%s %s=%s pass=%s badrows=%d delta=%s" % (
            m["exit"], "MATCH" if m["grade"] else "FAIL", key, cm.get(key),
            "true" if "C1_R93_PASS=true" in m["body"] else "false",
            len(badm[0].split()) - 1 if badm else 0,
            "identical" if b["run_body"] == m["run_body"] else "differs"))
        det = (cb.get(key) != cm.get(key)
               or ("C1_R93_PASS=true" in b["body"]) != ("C1_R93_PASS=true" in m["body"])
               or ("C1_BADROWS" in b["body"]) != ("C1_BADROWS" in m["body"])
               or (badb and badm and badb[0] != badm[0]))
        lines.append("  probe_detects_mutant=%s" % ("YES" if det else "NO"))
        lines.append("")
    out = "\n".join(lines) + "\n"
    open(OUT, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
