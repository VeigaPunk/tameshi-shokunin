#!/usr/bin/env python3
"""T90M1: mutation-test the frozen R90-C1 counter against its committed control battery.

Each defect in T90M1-defects.txt is ONE single-line edit applied to a scratch copy of
.ufo/evidence/round-90/c1/measure.py (exactly-one-occurrence asserted). The detector is
the committed control battery (c1/controls.py: CTL1-nowork-base, CTL1b-nowork-A and the
12 CTL* states), run with only its measure path redirected to the mutated copy
(env T90M1_MEASURE) and its receipts redirected into scratch (env T90M1_OUT), so the
frozen receipts under .ufo/evidence/round-90/pre-freeze/controls/ are never touched.

Verdict per defect:
  KILLED   at least one control state's receipt-observable result changes vs the
           pristine baseline (exit, C1_R90_PASS, C1_CONJUNCTS map, C1_ROW lines,
           C1_SETUP, summary counts)
  SURVIVED no control state changes

Usage:
  python3 T90M1-mutate.py --lane LANE --scratch DIR --spec T90M1-defects.txt \
      --counter <pristine measure.py> --driver <patched controls.py> \
      --out results.json [--only D01 D02] [--par 4] [--jobs 3] [--baseline-only]
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

CONTROLS = ["CTL1-nowork-base", "CTL1b-nowork-A", "CTL14-pos", "CTL2-flip", "CTL3-figure",
            "CTL4-ids", "CTL5-spec", "CTL6-noop", "CTL7-syntax", "CTL8-absent", "CTL9-equiv",
            "CTL10-source", "CTL11-trivial", "CTL12-pin", "CTL15-coverage", "CTL16-oldsource"]


def parse_spec(path):
    defects, cur = [], None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = re.match(r"^\[(D\d\d)\]$", line)
        if m:
            cur = {"id": m.group(1)}
            defects.append(cur)
            continue
        if cur is None:
            continue
        for k in ("anchor", "weakens", "old", "new"):
            if line.startswith(k + ": "):
                cur[k] = line[len(k) + 2:]
    for d in defects:
        for k in ("anchor", "weakens", "old", "new"):
            if k not in d:
                raise SystemExit("spec: %s missing %s" % (d["id"], k))
    return defects


def build_mutant(d, src, dest):
    n = src.count(d["old"])
    if n != 1:
        raise SystemExit("defect %s: old occurs %d times, need 1" % (d["id"], n))
    mtext = src.replace(d["old"], d["new"], 1)
    if mtext == src:
        raise SystemExit("defect %s: no change" % d["id"])
    if mtext.count("\n") != src.count("\n"):
        raise SystemExit("defect %s: line count changed" % d["id"])
    compile(mtext, dest, "exec")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(mtext)
    return hashlib.sha256(mtext.encode()).hexdigest()


def parse_receipt(path):
    sig = {"exit": None, "pass": None, "conj": {}, "rows": {}, "setup": [], "summary": None}
    if not os.path.exists(path):
        sig["missing"] = True
        return sig
    for l in open(path, encoding="utf-8", errors="replace").read().split("\n"):
        if l.startswith("C1_ROW "):
            sig["rows"][l.split()[1]] = re.sub(r"\s+", " ", l)
        elif l.startswith("C1_SUMMARY "):
            sig["summary"] = re.sub(r"\brev=[0-9a-f]{7,}", "rev=REV", l)
        elif l.startswith("C1_CONJUNCTS "):
            for kv in l.split()[1:]:
                k, _, v = kv.partition("=")
                sig["conj"][k] = v
        elif l.startswith("C1_SETUP "):
            sig["setup"].append(l)
        elif l.startswith("C1_R90_PASS="):
            sig["pass"] = l.split("=", 1)[1]
        elif l.startswith("exit="):
            sig["exit"] = int(l.split("=", 1)[1])
    return sig


def row_fields(line):
    out = {}
    for tok in line.split()[2:]:
        k, _, v = tok.partition("=")
        out[k] = v
    return out


def diff(a, b, level):
    """level 0 = verdict only (exit / PASS); 1 = check-level (conjuncts + row fields
    except the runs= print column + setup); 2 = full receipt text (pre-registered)."""
    d = []
    if a["exit"] != b["exit"]:
        d.append("exit %s->%s" % (a["exit"], b["exit"]))
    if a["pass"] != b["pass"]:
        d.append("pass %s->%s" % (a["pass"], b["pass"]))
    if level == 0:
        return d
    for k in sorted(set(a["conj"]) | set(b["conj"])):
        if a["conj"].get(k) != b["conj"].get(k):
            d.append("conj:%s %s->%s" % (k, a["conj"].get(k), b["conj"].get(k)))
    for rid in sorted(set(a["rows"]) | set(b["rows"])):
        fa, fb = row_fields(a["rows"].get(rid, "")), row_fields(b["rows"].get(rid, ""))
        fa.pop("runs", None)
        fb.pop("runs", None)
        if fa != fb:
            d.append("row:%s" % rid)
    if a["setup"] != b["setup"]:
        d.append("setup")
    if level == 1:
        return d
    for rid in sorted(set(a["rows"]) | set(b["rows"])):
        if a["rows"].get(rid) != b["rows"].get(rid):
            d.append("rowtext:%s" % rid)
    if a["summary"] != b["summary"]:
        d.append("summary")
    if a.get("missing") or b.get("missing"):
        d.append("receipt-missing")
    return d


def run_battery(name, measure, driver, lane, scratch, jobs):
    d = os.path.join(scratch, "run", name)
    shutil.rmtree(d, ignore_errors=True)
    ctl = os.path.join(d, "ctl")
    recv = os.path.join(d, "recv")
    os.makedirs(ctl)
    os.makedirs(recv)
    env = dict(os.environ, T90M1_MEASURE=measure, T90M1_OUT=recv)
    t0 = time.time()
    p = subprocess.run([sys.executable, "-I", driver, "--lane", lane, "--scratch", ctl,
                        "--jobs", str(jobs)], env=env, capture_output=True, text=True)
    dt = time.time() - t0
    with open(os.path.join(d, "driver.log"), "w", encoding="utf-8") as f:
        f.write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    sigs = {c: parse_receipt(os.path.join(recv, c + ".out")) for c in CONTROLS}
    return {"name": name, "seconds": round(dt, 1), "driver_exit": p.returncode,
            "sigs": sigs, "dir": d}


def frozen_sigs(lane):
    out = {}
    base = os.path.join(lane, ".ufo/evidence/round-90/pre-freeze/controls")
    for c in CONTROLS:
        out[c] = parse_receipt(os.path.join(base, c + ".out"))
    return out


def compare_baselines(results, lane):
    A = results["baselines"]["BASE-A"]["sigs"]
    B = results["baselines"]["BASE-B"]["sigs"]
    F = frozen_sigs(lane)
    out = {}
    for c in CONTROLS:
        out[c] = {"A_vs_B": diff(A[c], B[c], 1), "A_vs_frozen": diff(A[c], F[c], 1)}
    return out


def compute_table(results):
    A = results["baselines"]["BASE-A"]["sigs"]
    table = {}
    for did, r in results["defects"].items():
        k2, k1, k0 = {}, {}, {}
        for c in CONTROLS:
            d2 = diff(A[c], r["sigs"][c], 2)
            d1 = diff(A[c], r["sigs"][c], 1)
            d0 = diff(A[c], r["sigs"][c], 0)
            if d2:
                k2[c] = d2
            if d1:
                k1[c] = d1
            if d0:
                k0[c] = d0
        table[did] = {"killed_L2": bool(k2), "killed_L1": bool(k1), "killed_L0": bool(k0),
                      "controls_L2": k2, "controls_L1": k1, "controls_L0": k0}
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--driver", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--par", type=int, default=4)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--baseline-from", help="reuse BASE-A/BASE-B signatures from a prior results json")
    ap.add_argument("--merge-from", nargs="*", default=[],
                    help="prior results json files whose defect entries are merged in")
    ap.add_argument("--table-out", help="also write the printed table to this file")
    ap.add_argument("--analyze", help="recompute the table from a prior results json and exit")
    a = ap.parse_args()
    if a.analyze:
        results = json.load(open(a.analyze, encoding="utf-8"))
        results["baseline_compare"] = compare_baselines(results, os.path.realpath(a.lane))
        results["table"] = compute_table(results)
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=1, sort_keys=True)
        report(results, a.table_out)
        return
    lane = os.path.realpath(a.lane)
    scratch = os.path.realpath(a.scratch)
    os.makedirs(scratch, exist_ok=True)
    src = open(a.counter, encoding="utf-8").read()
    src_sha = hashlib.sha256(src.encode()).hexdigest()
    defects = parse_spec(a.spec)
    if a.only:
        defects = [d for d in defects if d["id"] in a.only]
    muts = {}
    for d in defects:
        mp = os.path.join(scratch, "mut", d["id"], "measure.py")
        d["mutant_sha"] = build_mutant(d, src, mp)
        d["mutant_path"] = mp
        muts[d["id"]] = mp
    print("counter_sha=%s defects=%d" % (src_sha, len(defects)), flush=True)

    results = {"counter_sha": src_sha, "defects": {}, "baselines": {}}
    t0 = time.time()
    with ThreadPoolExecutor(a.par) as ex:
        futs = {}
        if a.baseline_from:
            prior = json.load(open(a.baseline_from, encoding="utf-8"))
            results["baselines"] = prior["baselines"]
            print("reused baselines from %s" % a.baseline_from, flush=True)
        else:
            futs["BASE-A"] = ex.submit(run_battery, "BASE-A", a.counter, a.driver, lane, scratch, a.jobs)
            futs["BASE-B"] = ex.submit(run_battery, "BASE-B", a.counter, a.driver, lane, scratch, a.jobs)
        for d in defects:
            futs[d["id"]] = ex.submit(run_battery, d["id"], d["mutant_path"], a.driver, lane,
                                      scratch, a.jobs)
        for k, f in futs.items():
            r = f.result()
            print("done %s %.1fs driver_exit=%d" % (k, r["seconds"], r["driver_exit"]), flush=True)
            if k.startswith("BASE-"):
                results["baselines"][k] = r
            else:
                results["defects"][k] = r
    for mp in a.merge_from:
        prior = json.load(open(mp, encoding="utf-8"))
        for k, v in prior.get("defects", {}).items():
            if k not in results["defects"]:
                results["defects"][k] = v
                print("merged %s from %s" % (k, mp), flush=True)
    results["wall_seconds"] = round(time.time() - t0, 1)

    results["baseline_compare"] = compare_baselines(results, lane)
    results["table"] = compute_table(results)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    report(results, a.table_out)


def report(results, table_out):
    table = results["table"]
    base_unstable = results["baseline_compare"]
    rep = []
    rep.append("BASELINE A-vs-B / A-vs-frozen differences:")
    for c in CONTROLS:
        ab = base_unstable[c]["A_vs_B"]
        af = base_unstable[c]["A_vs_frozen"]
        if ab or af:
            rep.append("  %-18s A~B=%s  A~frozen=%s" % (c, ab or "same", af or "same"))
    rep.append("  (no line above = every control state reproduced identically)")
    nk2 = sum(1 for v in table.values() if v["killed_L2"])
    nk1 = sum(1 for v in table.values() if v["killed_L1"])
    nk0 = sum(1 for v in table.values() if v["killed_L0"])
    rep.append("")
    rep.append("%-4s %-9s %-9s %-9s %s" % ("id", "L2", "L1", "L0", "controls changed (L1)"))
    for did in sorted(table):
        v = table[did]
        rep.append("%-4s %-9s %-9s %-9s %s" % (
            did, "KILLED" if v["killed_L2"] else "SURVIVED",
            "KILLED" if v["killed_L1"] else "SURVIVED",
            "KILLED" if v["killed_L0"] else "SURVIVED",
            ",".join(sorted(v["controls_L1"])) or "-"))
    rep.append("")
    rep.append("TOTAL L2 (full receipt) %d/%d killed; L1 (check-level) %d/%d killed; "
               "L0 (verdict-only) %d/%d killed; wall %.1fs" % (
                   nk2, len(table), nk1, len(table), nk0, len(table), results["wall_seconds"]))
    for l in rep:
        print(l)
    if table_out:
        with open(table_out, "w", encoding="utf-8") as f:
            f.write("\n".join(rep) + "\n")


if __name__ == "__main__":
    main()
