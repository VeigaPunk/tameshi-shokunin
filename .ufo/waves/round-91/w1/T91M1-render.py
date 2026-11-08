#!/usr/bin/env python3
"""T91M1 — render the mutation matrix from the probe's results.json.

Reads SCRATCH/results.json and SCRATCH/manifest.json, emits a markdown report on
stdout: the defect table (prediction vs outcome), the full per-control matrix
(T = C1_R91_PASS=true, f = false, E = missing receipt), and the aggregate count
of defects each committed control kills.
"""
import argparse, json, os

ORDER = ["CTL1-nowork-base", "CTL1b-nowork-A", "V4-replace", "CTL2-flip", "CTL3-figure",
         "CTL4-ids", "CTL5-spec", "CTL6-noop", "CTL7-syntax", "CTL8-absent", "CTL9-equiv",
         "CTL10-source", "CTL11-trivial", "CTL12-pin", "CTL14-pos", "CTL15-coverage",
         "CTL16-oldsource", "VOV1-dup-row", "VOV3-draft-column"]
POS = "CTL14-pos"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", default="/fast/scratch/hyaku/tameshi-r91/T91M1")
    a = ap.parse_args()
    r = json.load(open(os.path.join(a.scratch, "results.json"), encoding="utf-8"))
    m = json.load(open(os.path.join(a.scratch, "manifest.json"), encoding="utf-8"))
    defects = r["defects"]
    ids = sorted(defects)
    print("# T91M1 mutation matrix")
    print()
    print("target sha256: `%s`" % r["sha_target"])
    print()
    print("## Defect outcomes")
    print()
    print("| defect | weakened check | prediction | outcome | killed by (must-not-pass control -> PASS=true) | pos_ok |")
    print("|---|---|---|---|---|---|")
    for i in ids:
        d = defects[i]
        outcome = "KILLED" if d["killed_by"] else "SURVIVED"
        print("| %s | %s | %s | **%s** | %s | %s |" % (
            i, d["check"].replace("|", "/"), d["predict"].replace("|", "/"), outcome,
            ", ".join(d["killed_by"]) or "—", "yes" if d["pos_ok"] else "NO"))
    print()
    print("## Per-control matrix")
    print()
    print("T = `C1_R91_PASS=true`, f = `C1_R91_PASS=false`, E = receipt missing, 2 = exit 2 refusal.")
    print()
    print("| defect | " + " | ".join(ORDER) + " |")
    print("|---" * (len(ORDER) + 1) + "|")
    for i in ids:
        cells = []
        for c in ORDER:
            row = defects[i]["rows"].get(c, {})
            p = row.get("pass_")
            if p == "true":
                cell = "T"
            elif p == "false":
                cell = "f"
            else:
                cell = "E"
            if row.get("exit") == 2 and cell == "f":
                cell = "2"
            cells.append(cell)
        print("| %s | %s |" % (i, " | ".join(cells)))
    print()
    print("## Kill attribution per committed control")
    print()
    print("| control | frozen receipt | defects it kills |")
    print("|---|---|---|")
    for c in ORDER:
        killers = [i for i in ids if c in defects[i]["killed_by"]]
        print("| %s | %s | %s |" % (c, r["controls"].get(c, "?"), ", ".join(killers) or "—"))
    print()
    survivors = [i for i in ids if not defects[i]["killed_by"]]
    print("## Verdict")
    print()
    print("killed=%d survived=%d of %d" % (len(ids) - len(survivors), len(survivors), len(ids)))
    print()
    print("VERDICT: " + ("kills-all" if not survivors else "survivors:" + ",".join(survivors)))
    print()
    print("lane snapshot HEAD %s; frozen driver sha256 %s; patched driver sha256 %s" % (
        m["lane_head"], m["sha_controls_frozen"], m["sha_controls_driver"]))


if __name__ == "__main__":
    main()
