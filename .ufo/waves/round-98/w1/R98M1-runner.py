import concurrent.futures, hashlib, json, os, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.join(ROOT, "lane")
WT = os.path.join(ROOT, "wtclone")
REV = "764aca97e513d650949999362cd4b0f5f0e566a5"
TOOL = ".ufo/evidence/round-97/c2/guard-inertia.py"
TOOL_SHA = "634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8"
PY = sys.executable
PREREG = json.load(open(os.path.join(ROOT, "R98M1-prereg.json")))
INSTR = {k: os.path.join(ROOT, "instr", v["path"]) for k, v in PREREG["instruments"].items()}
BASE_NAMES = {k: v["path"] for k, v in PREREG["instruments"].items()}
out = {"baseline": [], "mutants": []}
log = []

def L(msg):
    log.append(msg)
    print(msg, flush=True)

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def run(cmd, timeout=300):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr, time.time() - t0
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", "", time.time() - t0

def empty_dir(path):
    shutil.rmtree(path, ignore_errors=True)
    return path

def grade_pin(rc, stdout, exp):
    lines = stdout.splitlines()
    got_line = lines[-1] if lines else ""
    return rc == exp["rc"] and got_line == exp["exact_line"], got_line

def grade_arm(arm, inst, tool_path, tag):
    """returns (pass_bool, detail_str, observed_line)"""
    aid = arm["id"]
    if arm["kind"] == "selftest":
        rc, so, se, dt = run([PY, "-I", tool_path, "--selftest"])
        exp = arm["expect"]
        got = so.splitlines()[-1] if so.splitlines() else ""
        ok = rc == exp["rc"] and exp["exact_line"] in so.splitlines()
        return ok, "rc=%s %s" % (rc, se.strip()[:80]), got
    if arm["kind"] in ("audit-run", "audit-run-worktree-edit"):
        repo = WT if arm["kind"] == "audit-run-worktree-edit" else LANE
        cmd = [PY, "-I", tool_path, "--repo", repo, "--rev", REV, "--driver", arm["driver"]]
        rc, so, se, dt = run(cmd)
        exp = arm["expect"]
        lines = so.splitlines()
        got = lines[-1] if lines else ""
        ok = rc == exp["rc"] and got == exp["exact_line"]
        if ok and "exact_site_line" in exp:
            ok = exp["exact_site_line"] in lines
        return ok, "rc=%s %s" % (rc, se.strip()[:80]), got
    if arm["kind"] == "battery-positive":
        w = empty_dir(os.path.join(ROOT, "work", tag + "-pos"))
        cmd = [PY, "-I", tool_path, "--lane", LANE, "--rev", REV, "--tool", TOOL,
               "--tool-sha", TOOL_SHA, "--work", w]
        rc, so, se, dt = run(cmd)
        exp = arm["expect"]
        got = so.splitlines()[-1] if so.splitlines() else ""
        ok = rc == exp["rc"] and got == exp["exact_line"]
        return ok, "rc=%s wall=%.1fs %s" % (rc, dt, se.strip()[:80]), got
    if arm["kind"] == "battery-red":
        w = empty_dir(os.path.join(ROOT, "work", tag + "-red"))
        cmd = [PY, "-I", tool_path, "--lane", LANE, "--rev", REV, "--tool", TOOL,
               "--tool-sha", TOOL_SHA, "--work", w, "--red", arm["red"]]
        rc, so, se, dt = run(cmd)
        exp = arm["expect"]
        lines = so.splitlines()
        got = lines[-1] if lines else ""
        ok = rc == exp["rc"] and got == exp["exact_line"]
        ro = exp["red_observable"]
        obs_ok = any(ln.startswith(ro["contains_prefix"]) for ln in lines) and \
                 not any(ro["absent_substring"] in ln for ln in lines)
        ok = ok and obs_ok
        return ok, "rc=%s wall=%.1fs red-observable=%s %s" % (rc, dt, obs_ok, se.strip()[:60]), got
    if arm["kind"] == "battery-pin":
        res = []
        for sub, sha_ in (("mismatch", "0" * 64), ("invalid", "zz")):
            w = empty_dir(os.path.join(ROOT, "work", tag + "-pin-" + sub))
            cmd = [PY, "-I", tool_path, "--lane", LANE, "--rev", REV, "--tool", TOOL,
                   "--tool-sha", sha_, "--work", w]
            rc, so, se, dt = run(cmd, timeout=60)
            exp = arm["expect"][sub]
            lines = so.splitlines()
            got = lines[-1] if lines else ""
            res.append((rc == exp["rc"] and got == exp["exact_line"], "%s:rc=%s" % (sub, rc), got))
        ok = all(r[0] for r in res)
        got = " | ".join(r[2] for r in res)
        return ok, " ".join(r[1] for r in res), got
    raise SystemExit("unknown arm kind " + arm["kind"])

def run_set(inst, tool_path, tag):
    rows = []
    for arm in PREREG["arms"][inst]:
        ok, detail, got = grade_arm(arm, inst, tool_path, tag)
        rows.append({"arm": arm["id"], "pass": ok, "detail": detail, "observed_line": got})
        L("ARM %s %s %s %s | %s" % (tag, inst, arm["id"], "PASS" if ok else "FAIL", detail))
        if got:
            L("    line: %r" % got)
    return rows

def build_mutant(m):
    src = INSTR[m["instrument"]]
    d = os.path.join(ROOT, "mut", m["id"])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    dst = os.path.join(d, BASE_NAMES[m["instrument"]])
    text = open(src, encoding="utf-8").read()
    assert text.count(m["old"]) == 1, (m["id"], text.count(m["old"]))
    mut = text.replace(m["old"], m["new"], 1)
    assert mut != text
    # reverse edit restores pristine bytes exactly
    assert mut.replace(m["new"], m["old"], 1) == text, m["id"]
    open(dst, "w", encoding="utf-8").write(mut)
    return dst

def one_mutant(m):
    tag = m["id"]
    L("===== MUTANT %s (%s) =====" % (tag, m["instrument"]))
    try:
        path = build_mutant(m)
    except Exception as exc:
        L("APPLY-FAILED %s %r" % (tag, exc))
        return {"id": tag, "instrument": m["instrument"], "status": "INCONCLUSIVE",
                "reason": "apply-failed:%r" % (exc,), "arms": []}
    L("MUTATED %s sha256=%s (pristine=%s)" % (tag, sha(path), PREREG["instruments"][m["instrument"]]["sha256"]))
    rows = run_set(m["instrument"], path, tag)
    fails = [r["arm"] for r in rows if not r["pass"]]
    status = "KILLED" if fails else "SURVIVED"
    L("VERDICT %s %s fails=%s predicted=%s" % (tag, status, ",".join(fails) or "-", m["predicted"]))
    return {"id": tag, "instrument": m["instrument"], "status": status,
            "failing_arms": fails, "predicted": m["predicted"], "arms": rows,
            "mutant_sha256": sha(path)}

# --- preflight: pristine bytes ---
L("PREFLIGHT pristine")
for k, p in INSTR.items():
    got = sha(p)
    want = PREREG["instruments"][k]["sha256"]
    L("PRISTINE %s sha256=%s match=%s" % (k, got, got == want))
    if got != want:
        raise SystemExit("pristine digest mismatch")

# --- baseline ---
L("===== BASELINE pristine =====")
for inst in ("audit", "battery"):
    rows = run_set(inst, INSTR[inst], "baseline-" + inst)
    out["baseline"].append({"instrument": inst, "arms": rows})
    if not all(r["pass"] for r in rows):
        raise SystemExit("BASELINE FAILED for " + inst)

# --- mutants in parallel ---
results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(one_mutant, m): m for m in PREREG["mutants"]}
    for f in concurrent.futures.as_completed(futs):
        r = f.result()
        results[r["id"]] = r
out["mutants"] = [results[m["id"]] for m in PREREG["mutants"]]

# --- post-restore: pristine again ---
L("===== POST-RESTORE baseline =====")
post = []
for inst in ("audit", "battery"):
    rows = run_set(inst, INSTR[inst], "postrestore-" + inst)
    post.append({"instrument": inst, "arms": rows})
out["postrestore"] = post

# --- restore proof: pristine inst files + lane blobs ---
L("===== RESTORE PROOF =====")
proof = {}
for k, p in INSTR.items():
    got = sha(p)
    proof[k] = {"before": PREREG["instruments"][k]["sha256"], "after": got, "match": got == PREREG["instruments"][k]["sha256"]}
    L("RESTORE %s before=%s after=%s match=%s" % (k, proof[k]["before"], proof[k]["after"], proof[k]["match"]))
lane_proof = {}
for path in ("tools/control-assertion-audit.py", ".ufo/evidence/round-98/refusals/guard-refusals.py"):
    raw = subprocess.run(["/usr/bin/git", "-C", "/home/vgpnk/Projects/shokunin/tameshi-shokunin",
                          "cat-file", "blob", REV + ":" + path], capture_output=True)
    h = hashlib.sha256(raw.stdout).hexdigest()
    lane_proof[path] = h
    L("LANE-BLOB %s sha256=%s" % (path, h))
out["restore"] = {"instruments": proof, "lane_blobs": lane_proof}

summary = {"audit": [m for m in out["mutants"] if m["instrument"] == "audit"],
           "battery": [m for m in out["mutants"] if m["instrument"] == "battery"]}
kill_line = "MUTANTS audit=%d/%d battery=%d/%d" % (
    sum(1 for m in summary["audit"] if m["status"] == "KILLED"), len(summary["audit"]),
    sum(1 for m in summary["battery"] if m["status"] == "KILLED"), len(summary["battery"]))
L(kill_line)

# --- write receipts ---
json.dump(out, open(os.path.join(ROOT, "R98M1-run.json"), "w"), indent=1)
with open(os.path.join(ROOT, "R98M1-results.tsv"), "w") as f:
    f.write("kind\tinstrument\tmutant\tarm\texpect\tobserved_rc_detail\tverdict\tobserved_line\n")
    for b in out["baseline"]:
        for r in b["arms"]:
            f.write("baseline\t%s\t-\t%s\tpredicate-holds\t%s\t%s\t%s\n" % (
                b["instrument"], r["arm"], r["detail"].replace("\t", " "), "PASS" if r["pass"] else "FAIL", r["observed_line"]))
    for m in out["mutants"]:
        for r in m["arms"]:
            f.write("mutant\t%s\t%s\t%s\tpredicate-holds\t%s\t%s\t%s\n" % (
                m["instrument"], m["id"], r["arm"], r["detail"].replace("\t", " "), "PASS" if r["pass"] else "FAIL", r["observed_line"]))
        f.write("verdict\t%s\t%s\t-\t%s\t-\t%s\t%s\n" % (
            m["instrument"], m["id"], m["status"], m["status"],
            "fails=" + (",".join(m.get("failing_arms", [])) or "-")))
    for b in out["postrestore"]:
        for r in b["arms"]:
            f.write("postrestore\t%s\t-\t%s\tpredicate-holds\t%s\t%s\t%s\n" % (
                b["instrument"], r["arm"], r["detail"].replace("\t", " "), "PASS" if r["pass"] else "FAIL", r["observed_line"]))
open(os.path.join(ROOT, "R98M1-run.log"), "w").write("\n".join(log) + "\n")
print("WROTE receipts")
