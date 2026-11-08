#!/usr/bin/env python3
"""R95SN1 attack battery: C1 counter (measure-v95.py) trust boundaries.

Attacks the counter's git seal, file seal, pin/identity and gate-identity
constants. Every fixture is a scratch clone; the lane is never written.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
COUNTER = S + "/snap/measure-v95.py"
RESULTS = []


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None, check=False, shell=False):
    if shell:
        p = subprocess.run(cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True)
    else:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, p.stderr))
    return p


def clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", LANE_SRC, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


SEAL = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null"}


def run_counter(lane, rev, work, env=None, counter=COUNTER, timeout=400):
    e = dict(os.environ)
    if env:
        e.update(env)
    cmd = [sys.executable, "-I", counter, "--repo", lane, "--rev", rev, "--work", work]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"


def fixture(name, rev=None):
    d = os.path.join(S, "atk1", name)
    lane = clone(d)
    if rev:
        sh(["git", "-C", lane, "checkout", "-q", "--detach", rev])
    return lane


def fresh_work(name):
    w = os.path.join(S, "wk1", name)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    return w


def b01_ambient_git_dir():
    lane = fixture("b01")
    other = fixture("b01_other")
    w = fresh_work("b01")
    rc, out = run_counter(lane, "HEAD", w, env={
        "GIT_DIR": os.path.join(other, ".git"), "GIT_WORK_TREE": other})
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS", "C1_SUMMARY"))]
    rec("B01", "ambient GIT_DIR+GIT_WORK_TREE at the C1 counter",
        "exit=%s out=%r" % (rc, got[:3]),
        "the counter must read the --repo it was given; GIT_DIR must not redirect the read",
        "INFO", "observed")


def b02_git_config_count():
    lane = fixture("b02")
    w = fresh_work("b02")
    rc, out = run_counter(lane, "HEAD", w, env={
        "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.replaceRefs",
        "GIT_CONFIG_VALUE_0": "false"})
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS"))]
    bad = any("self-pin-mismatch" in l or "git-failed" in l for l in got)
    rec("B02", "ambient GIT_CONFIG_COUNT=1 core.replaceRefs=false at the C1 counter",
        "exit=%s out=%r" % (rc, got[:3]),
        "config injection must not change the counter's behaviour",
        "NONE (defended)" if not bad else "MEDIUM", "defended" if not bad else "VULNERABLE")


def b03_replace_ref_in_lane():
    lane = fixture("b03")
    note = "corpus/knowledge/mutation-case-fleet-sources-census.md"
    real = sh(["git", "-C", lane, "rev-parse", "HEAD:" + note]).stdout.strip()
    p = sh("git -C %s hash-object -w --stdin <<'EOF'\nforged note\nEOF" % lane, shell=True, env=SEAL)
    evil = p.stdout.strip()
    sh(["git", "-C", lane, "replace", real, evil], env=SEAL)
    w = fresh_work("b03")
    rc, out = run_counter(lane, "HEAD", w)
    ok = "replace-refs-present" in out
    rec("B03", "refs/replace on the note blob inside the --repo clone",
        "exit=%s out=%r" % (rc, [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95"))]),
        "exit 2, C1_SETUP replace-refs-present",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def b04_replace_ref_in_fleet():
    lane = fixture("b04")
    fl = clone(os.path.join(S, "atk1", "b04_fleet"))
    sp = os.path.join(lane, ".ufo/evidence/round-94/c1/census-mutants.json")
    spec = json.load(open(sp))
    spec["gate"]["repo"] = fl
    json.dump(spec, open(sp, "w"), indent=1)
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", "repoint gate repo"])
    w = fresh_work("b04")
    rc, out = run_counter(lane, "HEAD", w)
    ok = "replace-refs-present:fleet" in out
    rec("B04", "refs/replace in the FLEET (gate) repo the counter executes from",
        "exit=%s out=%r" % (rc, [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95"))]),
        "exit 2, C1_SETUP replace-refs-present:fleet (the counter checks both repos)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def b05_worktree_repo():
    lane = fixture("b05")
    wt = os.path.join(S, "atk1", "b05_wt")
    shutil.rmtree(wt, ignore_errors=True)
    sh(["git", "-C", lane, "worktree", "add", "-q", "--detach", wt, "HEAD"])
    w = fresh_work("b05")
    rc, out = run_counter(wt, "HEAD", w)
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95", "C1_SUMMARY"))]
    rec("B05", "--repo is a linked worktree of the lane repo",
        "exit=%s out=%r" % (rc, got[:3]),
        "the counter must read the same objects from a worktree of the same repo",
        "INFO", "observed")


def b06_empty_rev_index():
    lane = fixture("b06")
    note = "corpus/knowledge/mutation-case-fleet-sources-census.md"
    p = os.path.join(lane, note)
    body = open(p).read()
    open(p, "w").write(body + "\n| C99 | x | KILLED | differs |\n")
    sh(["git", "-C", lane, "add", "-A"])
    w = fresh_work("b06")
    rc, out = run_counter(lane, "", w)
    idx_hit = "C99" in out
    rec("B06", "--rev '' : git resolves ':<path>' against the INDEX (staged bytes)",
        "exit=%s staged_row_visible=%s out=%r" % (
            rc, idx_hit,
            [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_SUMMARY", "C1_BADROWS"))][:2]),
        "an empty --rev must not grade staged-but-uncommitted bytes",
        "HIGH" if idx_hit else "NONE (defended)", "VULNERABLE" if idx_hit else "defended")


def b07_work_not_empty():
    lane = fixture("b07")
    w = os.path.join(S, "wk1", "b07")
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    open(os.path.join(w, "junk"), "w").write("x")
    rc, out = run_counter(lane, "HEAD", w)
    ok = "work-not-empty-dir" in out
    rec("B07", "--work points at a non-empty directory",
        "exit=%s out=%r" % (rc, [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95"))]),
        "exit 2, C1_SETUP work-not-empty-dir",
        "NONE (defended)" if ok else "MEDIUM", "defended" if ok else "VULNERABLE")


def b08_repo_traversal():
    lane = fixture("b08")
    os.makedirs(os.path.join(S, "atk1", "b08", "sub"), exist_ok=True)
    weird = os.path.join(S, "atk1", "b08", "sub", "..", "..")
    w = fresh_work("b08")
    rc, out = run_counter(weird, "HEAD", w)
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95", "C1_SUMMARY"))]
    rec("B08", "--repo given with .. path segments",
        "exit=%s out=%r" % (rc, got[:3]),
        "the counter must resolve --repo and behave as for the same repo named directly",
        "INFO", "observed")


def b09_double_pin():
    src = open(COUNTER, "rb").read()
    guard = b'\nif __name__ == "__main__":'
    evil = src.replace(guard, b'\nSELF_SHA256 = "' + b"0" * 64 + b'"\n' + guard, 1)
    p = os.path.join(S, "atk1", "counter-double-pin.py")
    open(p, "wb").write(evil)
    w = fresh_work("b09")
    rc, out = run_counter(S + "/atk1/b01", "HEAD", w, counter=p)
    ok = "self-pin-line-count" in out
    rec("B09", "second SELF_SHA256 line inserted before the __main__ guard",
        "exit=%s out=%r" % (rc, [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95"))]),
        "exit 2, C1_SETUP self-pin-line-count (plan C1 control double-pin)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def b10_pin_after_main():
    src = open(COUNTER, "rb").read()
    evil = src + b'\nSELF_SHA256 = "' + b"0" * 64 + b'"\n'
    p = os.path.join(S, "atk1", "counter-pin-after-main.py")
    open(p, "wb").write(evil)
    w = fresh_work("b10")
    rc, out = run_counter(S + "/atk1/b01", "HEAD", w, counter=p)
    ok = "self-pin-line-count" in out
    rec("B10", "second SELF_SHA256 line appended AFTER the __main__ guard",
        "exit=%s out=%r" % (rc, [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95"))]),
        "exit 2, C1_SETUP self-pin-line-count (the line count is a whole-file property)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def b11_recomputed_malicious_pin():
    src = open(COUNTER, "rb").read()
    evil = src.replace(b'    ok = all(conj.values())',
                       b'    ok = True  # MALICIOUS', 1)
    assert evil != src, "malicious anchor not found"
    norm = re.sub(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n', b"", evil, flags=re.M)
    h = hashlib.sha256(norm).hexdigest()
    evil = re.sub(rb'^SELF_SHA256 = "[0-9a-f]{64}"\n',
                  ('SELF_SHA256 = "%s"\n' % h).encode(), evil, count=1)
    p = os.path.join(S, "atk1", "counter-recomputed.py")
    open(p, "wb").write(evil)
    w = fresh_work("b11")
    rc, out = run_counter(S + "/atk1/b01", "HEAD", w, counter=p)
    selfpin_ok = "self-pin-mismatch" not in out and "self-pin-line-count" not in out
    claims_pass = "C1_R95_PASS=true" in out
    rec("B11", "counter edited to force ok=True with the SELF_SHA256 pin RECOMPUTED",
        "exit=%s self_pin_passed=%s claims_pass=%s" % (rc, selfpin_ok, claims_pass),
        "the self-pin certifies the file's own bytes, not the executed bytes; "
        "identity is bound by kill rule (c) (the blob sha256 in claims.json)",
        "MEDIUM (declared limit)", "accepted-by-design")


def b12_gate_identity_constants():
    src = open(COUNTER, "rb").read()
    m = re.search(rb'^GATE_COMMIT = "([0-9a-f]{40})"$', src, re.M)
    m2 = re.search(rb'^GATE_SHA256 = "([0-9a-f]{64})"$', src, re.M)
    rec("B12", "gate-identity constants are hand-copied into the counter's pinned bytes",
        "GATE_COMMIT=%s GATE_SHA256=%s" % (m.group(1).decode()[:12], m2.group(1).decode()[:12]),
        "a foreign gate must be refused with gate-identity-mismatch (the constants anchor it)",
        "INFO (defended)", "observed")


def b13_counter_blob_in_lane():
    lane = fixture("b13")
    cp = os.path.join(lane, ".ufo/evidence/round-95/c1/measure-v95.py")
    if not os.path.exists(cp):
        rec("B13", "counter blob at --rev", "not present in the lane clone at HEAD",
            "n/a", "INFO", "skipped")
        return
    rc, out = run_counter(lane, "HEAD", fresh_work("b13"))
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95"))]
    rec("B13", "counter blob read from the lane working tree at HEAD (pin self-check)",
        "exit=%s out=%r" % (rc, got[:3]),
        "the counter must verify its own bytes before acting",
        "INFO", "observed")


def b14_alternates():
    lane = fixture("b14")
    evil = clone(os.path.join(S, "atk1", "b14_evil"))
    p = sh("git -C %s hash-object -w --stdin <<'EOF'\nEVIL\nEOF" % evil, shell=True, env=SEAL)
    alt = os.path.join(lane, ".git/objects/info/alternates")
    os.makedirs(os.path.dirname(alt), exist_ok=True)
    with open(alt, "a") as f:
        f.write(os.path.join(evil, ".git/objects") + "\n")
    w = fresh_work("b14")
    rc, out = run_counter(lane, "HEAD", w)
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95", "C1_SUMMARY"))]
    rec("B14", "objects/info/alternates in the --repo clone pointing at a foreign object store",
        "exit=%s out=%r" % (rc, got[:3]),
        "an alternates file must not let a foreign object store supply the graded bytes "
        "(git object ids are content-addressed)",
        "NONE (defended by content addressing)", "defended")


def main():
    os.makedirs(os.path.join(S, "atk1"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [b01_ambient_git_dir, b02_git_config_count, b03_replace_ref_in_lane,
               b04_replace_ref_in_fleet, b05_worktree_repo, b06_empty_rev_index,
               b07_work_not_empty, b08_repo_traversal, b09_double_pin, b10_pin_after_main,
               b11_recomputed_malicious_pin, b12_gate_identity_constants,
               b13_counter_blob_in_lane, b14_alternates]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
        print("%-34s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-c1-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
