#!/usr/bin/env python3
"""Round-21 C1 ruler: replay the frozen round-18 guard-survivor population.

For every mutant in c1-mutants.json this materialises the lane at --rev in a
private clone, checks the @old anchor occurs exactly once, applies the single
edit in its own --shared clone, and runs the owning tool's --selftest inside
bwrap with a scrubbed environment (the round-18 detector envelope).

  KILLED        pristine selftest exit 0, mutant selftest exit != 0
  SURVIVED      pristine exit 0, mutant exit 0
  INCONCLUSIVE  anchor count != 1, pristine control not green, or timeout

Exit: 0 every mutant KILLED; 1 measurement complete with any non-kill;
2 setup failure; 64 usage.  The lane checkout is never written.
"""
import argparse, concurrent.futures, hashlib, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE / "c1-mutants.json"
FLEET = Path("/home/vgpnk/Projects/shokunin")
LANE_NAME = "tameshi-shokunin"
TIMEOUT = 900


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, **kw)


def scrubbed_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def selftest(w, d, tool, args):
    argv = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--tmpfs", "/tmp", "--bind", str(w), str(w), "--unshare-net",
            "--die-with-parent", "--chdir", str(d),
            "env", "-i", "PATH=" + os.environ.get("PATH", "/usr/bin:/bin"),
            f"HOME={w}/home", f"TMPDIR={w}/tmp",
            "GIT_CONFIG_GLOBAL=/dev/null", "GIT_CONFIG_NOSYSTEM=1", "LC_ALL=C",
            "python3", str(d / tool)] + list(args)
    t0 = time.monotonic()
    try:
        p = run(argv, env=scrubbed_env(), timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"exit": None, "timeout": True, "seconds": round(time.monotonic() - t0, 3)}
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    fails = [l for l in (out + "\n" + err).splitlines() if " FAIL" in l or l.startswith("FAIL")][:40]
    lines = [l for l in out.splitlines() if l.strip()]
    return {"exit": p.returncode, "timeout": False, "seconds": round(time.monotonic() - t0, 3),
            "summary": lines[-1] if lines else "", "fail_lines": fails,
            "stdout_sha256": sha(p.stdout), "stderr_sha256": sha(p.stderr)}


def clone(src, dst, rev, shared=False):
    argv = ["git", "clone", "-q"] + (["--shared"] if shared else ["--no-hardlinks"]) + [str(src), str(dst)]
    p = run(argv, env=scrubbed_env())
    if p.returncode:
        raise RuntimeError(f"clone failed: {p.stderr.decode(errors='replace')}")
    p = run(["git", "-C", str(dst), "checkout", "-q", "--detach", rev], env=scrubbed_env())
    if p.returncode:
        raise RuntimeError(f"checkout {rev} failed: {p.stderr.decode(errors='replace')}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated mutant ids (diagnostic subset)")
    ap.add_argument("--jobs", type=int, default=4)
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 64
    repo = Path(a.repo).resolve()
    spec_bytes = SPEC.read_bytes()
    spec = json.loads(spec_bytes)
    mutants = spec["mutants"]
    if a.only:
        keep = set(a.only.split(","))
        mutants = [m for m in mutants if m["id"] in keep]
    p = run(["git", "-C", str(repo), "rev-parse", "--verify", a.rev + "^{commit}"], env=scrubbed_env())
    if p.returncode:
        print(f"C1: cannot resolve rev {a.rev}", file=sys.stderr)
        return 2
    rev = p.stdout.decode().strip()
    w = Path(tempfile.mkdtemp(prefix="tameshi-r21-c1."))
    try:
        (w / "home").mkdir(); (w / "tmp").mkdir(); (w / "fleet").mkdir()
        for e in FLEET.iterdir():
            if e.name != LANE_NAME:
                os.symlink(e, w / "fleet" / e.name)
        pristine = w / "fleet" / LANE_NAME
        clone(repo, pristine, rev)
        tools = sorted({m["path"] for m in mutants})
        with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
            ctrl = dict(zip(tools, ex.map(lambda t: selftest(w, pristine, t, spec["selftest_argv"][t]), tools)))
        tool_sha = {t: sha((pristine / t).read_bytes()) for t in tools}

        def one(m):
            r = {"id": m["id"], "path": m["path"]}
            src = (pristine / m["path"]).read_bytes().decode("utf-8")
            r["anchor_count"] = src.count(m["old"])
            if r["anchor_count"] != 1:
                r["verdict"] = "INCONCLUSIVE"; r["reason"] = "anchor-count"
                return r
            c = ctrl[m["path"]]
            if c["exit"] != 0:
                r["verdict"] = "INCONCLUSIVE"; r["reason"] = "pristine-control-not-green"
                return r
            d = w / "mut" / m["id"]
            d.parent.mkdir(exist_ok=True)
            clone(pristine, d, rev, shared=True)
            mutated = src.replace(m["old"], m["new"], 1)
            (d / m["path"]).write_text(mutated, encoding="utf-8")
            r["mutated_sha256"] = sha(mutated.encode("utf-8"))
            res = selftest(w, d, m["path"], spec["selftest_argv"][m["path"]])
            r["mutant"] = res
            if res["timeout"]:
                r["verdict"] = "INCONCLUSIVE"; r["reason"] = "timeout"
            elif res["exit"] == 0:
                r["verdict"] = "SURVIVED"
            else:
                r["verdict"] = "KILLED"
            shutil.rmtree(d, ignore_errors=True)
            return r

        with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
            rows = list(ex.map(one, mutants))
    except Exception as e:  # setup failure is not a measurement
        print(f"C1: setup failure: {e}", file=sys.stderr)
        return 2
    finally:
        shutil.rmtree(w, ignore_errors=True)
    counts = {k: sum(r["verdict"] == k for r in rows) for k in ("KILLED", "SURVIVED", "INCONCLUSIVE")}
    out = {"schema": "tameshi-r21-c1-receipt-v1", "rev": rev, "ruler_sha256": sha(Path(__file__).read_bytes()),
           "spec_sha256": sha(spec_bytes), "total": len(rows), "killed": counts["KILLED"],
           "survived": counts["SURVIVED"], "inconclusive": counts["INCONCLUSIVE"],
           "tool_sha256": tool_sha, "controls": ctrl, "rows": rows}
    if a.json:
        print(json.dumps(out, indent=1, sort_keys=True))
    for r in rows:
        print(f"C1 {r['id']} {r['path']} {r['verdict']}" + (f" ({r.get('reason')})" if r.get("reason") else ""), file=sys.stderr)
    print(f"C1: killed={counts['KILLED']} survived={counts['SURVIVED']} inconclusive={counts['INCONCLUSIVE']} total={len(rows)} rev={rev}", file=sys.stderr)
    return 0 if counts["KILLED"] == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
