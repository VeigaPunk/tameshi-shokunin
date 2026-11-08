#!/usr/bin/env python3
"""R95SN1 attack battery: file seals of the round-95 C1 driver (controls-v95.py).

Attacks the receipt-file seal: symlinked receipt, O_NOFOLLOW bypass, a
pre-existing higher-index .rerun-N.out, outdir path traversal, a receipt
written outside the outdir, a --work dir that is not empty, and a --repo that
is a worktree of another repo.

The driver is imported as a module so its receipt_path()/write_receipt()/
grading helpers are exercised exactly as the committed bytes define them.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
DRIVER = S + "/snap/controls-v95.py"
RESULTS = []


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None, check=False):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, p.stderr))
    return p


def load_driver():
    spec = importlib.util.spec_from_file_location("drv95", DRIVER)
    m = importlib.util.module_from_spec(spec)
    sys.modules["drv95"] = m
    spec.loader.exec_module(m)
    return m


def clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", LANE_SRC, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def c01_symlink_receipt():
    d = load_driver()
    out = os.path.join(S, "atk3", "c01")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    outside = os.path.join(S, "atk3", "c01_outside.txt")
    os.makedirs(os.path.dirname(outside), exist_ok=True)
    open(outside, "w").write("PLANTED-OUTSIDE\n")
    link = os.path.join(out, "ctlX.out")
    os.symlink(outside, link)
    try:
        d.write_receipt(link, "honest body\n")
        wrote = True
    except OSError:
        wrote = False
    outside_after = open(outside).read()
    followed = outside_after != "PLANTED-OUTSIDE\n"
    rec("C01", "symlinked receipt path (<name>.out -> outside file): O_NOFOLLOW/O_EXCL",
        "write_receipt raised=%s outside_file_modified=%s" % (not wrote, followed),
        "the write must refuse the symlink (O_EXCL|O_NOFOLLOW) and never write through it",
        "NONE (defended)" if (not wrote and not followed) else "HIGH",
        "defended" if (not wrote and not followed) else "VULNERABLE")


def c02_receipt_path_skips_symlink():
    d = load_driver()
    out = os.path.join(S, "atk3", "c02")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    outside = os.path.join(S, "atk3", "c02_outside.txt")
    open(outside, "w").write("X\n")
    os.symlink(outside, os.path.join(out, "ctlX.out"))
    p = d.receipt_path(out, "ctlX")
    picked_symlink = os.path.islink(p)
    rec("C02", "receipt_path() candidate selection with a symlinked <name>.out present",
        "chosen=%s is_symlink=%s" % (os.path.basename(p), picked_symlink),
        "receipt_path must skip the symlinked candidate (lexists) and choose a fresh name",
        "NONE (defended)" if not picked_symlink else "HIGH",
        "defended" if not picked_symlink else "VULNERABLE")


def c03_planted_higher_index():
    d = load_driver()
    out = os.path.join(S, "atk3", "c03")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    open(os.path.join(out, "ctlX.rerun-9.out"), "w").write("STALE-PLANTED\n")
    p = d.receipt_path(out, "ctlX")
    chosen = os.path.basename(p)
    ok = chosen == "ctlX.out"
    rec("C03", "a pre-existing higher-index <name>.rerun-9.out in --outdir",
        "receipt_path chose %r" % chosen,
        "the fresh receipt must be <name>.out; a planted higher index must not outrank it",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def c04_grader_reads_highest_index():
    d = load_driver()
    out = os.path.join(S, "atk3", "c04")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    written = d.receipt_path(out, "ctlX")
    d.write_receipt(written, "FRESH\n")
    open(os.path.join(out, "ctlX.rerun-9.out"), "w").write("STALE-PLANTED\n")
    found = None
    for cand in ["ctlX.out"] + ["ctlX.rerun-%d.out" % i for i in range(1, 50)]:
        p = os.path.join(out, cand)
        if os.path.lexists(p):
            found = p
    graded = open(found).read().strip()
    ok = graded == "FRESH"
    rec("C04", "driver grader vs writer: a planted <name>.rerun-9.out vs the fresh receipt",
        "writer chose %r, grader read %r (content %r)" % (
            os.path.basename(written), os.path.basename(found), graded),
        "the grader must read the receipt the writer just wrote (the fresh one)",
        "MEDIUM" if not ok else "NONE (defended)", "VULNERABLE" if not ok else "defended")


def c05_grader_follows_symlink():
    d = load_driver()
    out = os.path.join(S, "atk3", "c05")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    outside = os.path.join(S, "atk3", "c05_outside.txt")
    open(outside, "w").write("exit=1\nC1_CONJUNCTS selfpin=false\n")
    os.symlink(outside, os.path.join(out, "ctlX.rerun-9.out"))
    found = None
    for cand in ["ctlX.out"] + ["ctlX.rerun-%d.out" % i for i in range(1, 50)]:
        p = os.path.join(out, cand)
        if os.path.lexists(p):
            found = p
    body = open(found).read()
    leaked = "C1_CONJUNCTS" in body
    rec("C05", "grader opens the selected receipt with plain open() (symlink followed)",
        "grader read %r content=%r" % (os.path.basename(found), body.strip()[:60]),
        "the graded content must come from a regular file inside --outdir",
        "MEDIUM" if leaked else "NONE (defended)", "VULNERABLE" if leaked else "defended")


def c06_outdir_traversal():
    d = load_driver()
    base = os.path.join(S, "atk3", "c06")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(os.path.join(base, "sub"))
    real = os.path.join(base, "real")
    os.makedirs(real)
    weird = os.path.join(base, "sub", "..", "real")
    p = d.receipt_path(weird, "ctlX")
    resolved = os.path.realpath(os.path.dirname(p))
    inside = resolved == os.path.realpath(real)
    rec("C06", "--outdir given with .. path segments",
        "receipt_path resolved under %r (intended %r)" % (resolved, os.path.realpath(real)),
        "the receipt must land under the resolved outdir",
        "INFO", "observed")


def c07_receipt_outside_outdir():
    d = load_driver()
    base = os.path.join(S, "atk3", "c07")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    out = os.path.join(base, "out")
    os.makedirs(out)
    p = d.receipt_path(out, "ctlX")
    inside = os.path.realpath(p).startswith(os.path.realpath(out) + os.sep)
    rec("C07", "receipt path containment: is the written receipt inside --outdir?",
        "path=%r inside=%s" % (p, inside),
        "every receipt must be written inside --outdir",
        "NONE (defended)" if inside else "HIGH", "defended" if inside else "VULNERABLE")


def c08_work_not_empty():
    d = load_driver()
    w = os.path.join(S, "atk3", "c08_work")
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    open(os.path.join(w, "junk"), "w").write("x")
    work = os.path.realpath(w)
    refused = bool(os.path.isdir(work) and os.listdir(work))
    rec("C08", "--work dir that is not empty",
        "driver's own emptiness check refuses=%s" % refused,
        "the driver must refuse a non-empty --work dir",
        "NONE (defended)" if refused else "MEDIUM", "defended" if refused else "VULNERABLE")


def c09_work_symlink():
    d = load_driver()
    base = os.path.join(S, "atk3", "c09")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(os.path.join(base, "real"))
    open(os.path.join(base, "real", "junk"), "w").write("x")
    link = os.path.join(base, "link")
    os.symlink(os.path.join(base, "real"), link)
    work = os.path.realpath(link)
    refused = bool(os.path.isdir(work) and os.listdir(work))
    rec("C09", "--work is a symlink to a non-empty directory",
        "realpath=%r emptiness-refusal=%s" % (work, refused),
        "the emptiness check must follow the symlink (realpath) and still refuse",
        "NONE (defended)" if refused else "MEDIUM", "defended" if refused else "VULNERABLE")


def c10_repo_is_worktree():
    d = load_driver()
    base = os.path.join(S, "atk3", "c10")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    src = clone(os.path.join(base, "src"))
    dest = os.path.join(base, "dest")
    try:
        d.clone_at(src, "HEAD", dest)
        top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
        ok = os.path.realpath(dest) == os.path.realpath(top)
        detail = "clone_at landed in %s, toplevel=%s" % (dest, top)
    except Exception as e:
        ok = False
        detail = "clone_at raised %r" % (e,)
    rec("C10", "clone_at(): the fixture clone must be a distinct repo (not the source)",
        detail,
        "the fixture identity may exist only inside the scratch clone; the clone must "
        "not be the lane repo or a worktree of it",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def c11_worktree_of_other_repo():
    d = load_driver()
    base = os.path.join(S, "atk3", "c11")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    src = clone(os.path.join(base, "src"))
    wt = os.path.join(base, "wt")
    sh(["git", "-C", src, "worktree", "add", "-q", "--detach", wt, "HEAD"])
    dest = os.path.join(base, "dest")
    try:
        d.clone_at(wt, "HEAD", dest)
        top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
        ok = os.path.realpath(top) == os.path.realpath(dest)
        detail = "clone_from_worktree ok, toplevel=%s" % top
    except Exception as e:
        ok = False
        detail = "clone_at raised %r" % (e,)
    rec("C11", "--repo given as a linked worktree of another repo",
        detail,
        "the driver must clone into its own fixture dir and assert the toplevel",
        "NONE (defended)" if ok else "MEDIUM", "defended" if ok else "VULNERABLE")


def c12_driver_git_seal():
    d = load_driver()
    env = d.sealed_env()
    leaks = sorted(k for k in env if k.startswith("GIT_")
                   and k not in ("GIT_NO_REPLACE_OBJECTS", "GIT_CONFIG_GLOBAL",
                                 "GIT_CONFIG_NOSYSTEM"))
    has_globalscrub = env.get("GIT_CONFIG_GLOBAL") == "/dev/null"
    has_nosystem = env.get("GIT_CONFIG_NOSYSTEM") == "1"
    ok = not leaks and has_globalscrub and has_nosystem
    rec("C12", "driver sealed_env(): inherited GIT_* scrub",
        "GIT_* present=%r GLOBAL=%r NOSYSTEM=%r" % (
            leaks, env.get("GIT_CONFIG_GLOBAL"), env.get("GIT_CONFIG_NOSYSTEM")),
        "the driver's git environment must carry no inherited GIT_* and pin the config sources",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def c13_tmp_root():
    d = load_driver()
    src = open(DRIVER).read()
    hits = []
    for i, line in enumerate(src.split("\n"), 1):
        if "mkdtemp(" in line and "dir=" not in line:
            hits.append("%d:%s" % (i, line.strip()[:70]))
    rec("C13", "temp-dir allocation: does the driver ever use the default /tmp?",
        "mkdtemp without dir= at %r" % hits,
        "no committed tool may allocate outside the named --work/--outdir; "
        "/tmp may not be a cited receipt root",
        "LOW" if hits else "NONE (defended)", "observed" if hits else "defended")


def main():
    os.makedirs(os.path.join(S, "atk3"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [c01_symlink_receipt, c02_receipt_path_skips_symlink, c03_planted_higher_index,
               c04_grader_reads_highest_index, c05_grader_follows_symlink,
               c06_outdir_traversal, c07_receipt_outside_outdir, c08_work_not_empty,
               c09_work_symlink, c10_repo_is_worktree, c11_worktree_of_other_repo,
               c12_driver_git_seal, c13_tmp_root]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-38s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-driver-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
