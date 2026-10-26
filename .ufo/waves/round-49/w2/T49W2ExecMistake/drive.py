import json, os, shutil, signal, subprocess, sys, time
S = "/fast/scratch/hyaku/tameshi-r49/T49W2ExecMistake"
CLONE = os.path.join(S, "clone")
SCRIPT = ".ufo/evidence/round-49/deciding-run.sh"
FREEZE = "14d03ea4270c6904064022b62b6faf467e5c0968"
BASE = "8ca67421111fa354b47b803358391d0b07fc6db9"
REV = "f181a961ae44061af486f600e5ea257d2baf78f8"
out = {}

def git(*a):
    return subprocess.run(["git", "-C", CLONE, *a], capture_output=True, text=True)

def mkout(name, starts=()):
    d = os.path.join(S, name)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for s in starts: open(os.path.join(d, s), "w").close()
    return d

def listing(d):
    return sorted(os.listdir(d)) if os.path.isdir(d) else "ABSENT"

def run_case(name, rev, freeze, outdir, hc, kill_on_frozen=False):
    env = dict(os.environ, HYAKU_SCRATCH=hc, TMPDIR=S)
    t0 = time.time()
    p = subprocess.Popen(["bash", SCRIPT, CLONE, rev, freeze, outdir],
                         cwd=CLONE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, bufsize=1, start_new_session=True, env=env)
    lines, killed_at = [], None
    pgid = os.getpgid(p.pid)
    for line in p.stdout:
        lines.append({"t": round(time.time() - t0, 3), "line": line.rstrip("\n")})
        if kill_on_frozen and line.startswith("FROZEN_UNCHANGED"):
            os.killpg(pgid, signal.SIGTERM)
            killed_at = {"t": round(time.time() - t0, 3), "line": line.rstrip("\n"), "pgid": pgid}
            break
    try:
        rc = p.wait(timeout=60)
    except subprocess.TimeoutExpired:
        os.killpg(pgid, signal.SIGKILL); rc = "TIMEOUT_KILLED"
    rest = p.stdout.read()
    scr = os.path.join(hc, "tameshi-r49", "deciding")
    rec = {"case": name, "argv": [SCRIPT, CLONE, rev, freeze, outdir], "rev": rev, "freeze": freeze,
           "outdir": outdir, "hyaku_scratch": hc, "rc": rc, "lines": lines,
           "killed_at": killed_at, "stdout_tail_after_kill": rest,
           "out_listing": listing(outdir), "scr": scr, "scr_exists": os.path.isdir(scr),
           "scr_listing": listing(scr) if os.path.isdir(scr) else "ABSENT",
           "c1_start": os.path.exists(os.path.join(outdir, "c1.start")),
           "c2_start": os.path.exists(os.path.join(outdir, "c2.start")),
           "elapsed": round(time.time() - t0, 3)}
    print(json.dumps({k: rec[k] for k in ("case","rc","lines","out_listing","scr_exists","scr_listing","c1_start","c2_start","killed_at")}, indent=1), flush=True)
    return rec

# fixture commit: f181a96 tree minus exactly c2-controls.exit (plumbing only, worktree/HEAD untouched)
tgt = ".ufo/evidence/round-49/control/c2-controls.exit"
tree = git("rev-parse", "f181a96^{tree}").stdout.strip()
idx = os.path.join(S, "fixture.idx")
if os.path.exists(idx): os.remove(idx)
envx = dict(os.environ, GIT_INDEX_FILE=idx)
subprocess.run(["git", "-C", CLONE, "read-tree", tree], check=True, env=envx)
subprocess.run(["git", "-C", CLONE, "rm", "--cached", "-q", tgt], check=True, env=envx)
newtree = subprocess.run(["git", "-C", CLONE, "write-tree"], check=True, env=envx,
                         capture_output=True, text=True).stdout.strip()
drop = subprocess.run(["git", "-C", CLONE, "commit-tree", newtree, "-p", "f181a96", "-m",
                       "fixture (w2 executor scratch clone only): drop c2-controls.exit"],
                      check=True, capture_output=True, text=True).stdout.strip()
print("drop-commit", drop, "tree", newtree, flush=True)
out["drop_commit"] = drop
out["drop_commit_diff"] = git("diff", "--stat", "f181a96", drop).stdout.strip()

out["a1"] = run_case("a1-drop-one-receipt", drop, FREEZE, mkout("out-a1"), os.path.join(S, "ha1"))
out["a2"] = run_case("a2-base-no-receipts", BASE, FREEZE, mkout("out-a2"), os.path.join(S, "ha2"))
out["b1"] = run_case("b1-preexisting-c1.start", REV, FREEZE, mkout("out-b1", ["c1.start"]), os.path.join(S, "hb1"))
out["b2"] = run_case("b2-preexisting-c2.start", REV, FREEZE, mkout("out-b2", ["c2.start"]), os.path.join(S, "hb2"))
out["c"] = run_case("c-gate0-passes-killed", REV, FREEZE, mkout("out-c"), os.path.join(S, "hc"), kill_on_frozen=True)

# post-kill survivor check: any process still referencing the clone?
ps = subprocess.run(["bash", "-c", f"ps -eo pid,pgid,etimes,cmd | grep -F '{S}/clone' | grep -v grep || true"],
                    capture_output=True, text=True).stdout
out["survivors"] = ps.strip()
print("SURVIVORS:", repr(ps.strip()), flush=True)
with open(os.path.join(S, "cases.json"), "w") as f: json.dump(out, f, indent=1)
