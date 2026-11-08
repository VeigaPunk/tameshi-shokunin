#!/usr/bin/env python3
"""R95SN1 attack battery: C2 checker (conjunct-disposition-v95.py) trust boundaries.

Every attack runs against a scratch clone fixture; the lane is never written.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CHECKER = S + "/snap/conjunct-disposition-v95.py"
COUNTER_REL = ".ufo/evidence/round-95/c1/measure-v95.py"
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
RESULTS = []


def rec(fid, title, observed, expected, severity, verdict):
    RESULTS.append(dict(id=fid, title=title, observed=observed, expected=expected,
                        severity=severity, verdict=verdict))


def sh(cmd, cwd=None, env=None, check=False):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s" % (" ".join(cmd), p.stderr))
    return p


def clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", LANE_SRC, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def counter_sha(lane, rev):
    b = sh(["git", "-C", lane, "cat-file", "blob", rev + ":" + COUNTER_REL]).stdout
    return hashlib.sha256(b.encode()).hexdigest()


def run_checker(lane, rev, extra=None, env=None, cwd=None):
    cmd = [sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
           "--min-falsifiable", "17"]
    if extra:
        cmd += extra
    e = dict(os.environ)
    if env:
        e.update(env)
    p = sh(cmd, cwd=cwd, env=e)
    return p.returncode, p.stdout + p.stderr


def build_fixture(name, mutate_receipt=None, extra_receipts=None, rev_extra=False):
    """Clone the lane, commit the round-95 instruments + receipts, return (lane, rev)."""
    d = os.path.join(S, "atk", name)
    lane = clone(d)
    sh(["cp", "-a", os.path.join(LANE_SRC, ".ufo/evidence/round-95"),
        os.path.join(lane, ".ufo/evidence/round-95")])
    sh(["rm", "-rf", os.path.join(lane, ".ufo/evidence/round-95/c1/__pycache__")])
    blob = sh(["git", "-C", lane, "cat-file", "blob", "HEAD:" + COUNTER_REL]).stdout
    sha = hashlib.sha256(blob.encode()).hexdigest()
    man = json.load(open(os.path.join(lane, ".ufo/evidence/round-95/conjunct-disposition.json")))
    rows = man["rows"]
    rd = os.path.join(lane, RECEIPTS_REL)
    os.makedirs(rd, exist_ok=True)
    KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
            "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
            "figure", "witnessed", "source", "coverage", "n_min"]
    for k, row in rows.items():
        if "unfalsifiable" in row:
            continue
        st = row["state"]
        if row["mode"] == "setup-refusal":
            body = ("control=%s\ncounter_sha=%s\nexit=2\nC1_SETUP %s\n"
                    % (st, sha, row["token"]))
        else:
            body = ("control=%s\ncounter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (st, sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(rd, st + ".out"), "w").write(body)
    if mutate_receipt:
        mutate_receipt(lane, rd, sha)
    if extra_receipts:
        for fn, body in extra_receipts.items():
            open(os.path.join(rd, fn), "w").write(body)
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", "atk fixture"])
    rev = sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()
    return lane, rev, sha


# ---------------------------------------------------------------- attacks
def a01_replace_ref_counter():
    """forge-replace-ref: replace the counter blob in the lane clone."""
    lane, rev, sha = build_fixture("a01")
    counter_blob = sh(["git", "-C", lane, "cat-file", "blob", rev + ":" + COUNTER_REL]).stdout
    evil = "#!/usr/bin/env python3\nprint('C1_CONJUNCT_KEYS bogus1 bogus2')\n"
    evil_oid = sh(["git", "-C", lane, "hash-object", "-w", "--stdin"],
                  env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"}).stdout
    # hash-object with stdin needs input; do it via shell
    p = subprocess.run("git -C %s hash-object -w --stdin <<'EOF'\n%s\nEOF"
                       % (lane, evil.rstrip()), shell=True, capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"})
    evil_oid = p.stdout.strip()
    real_oid = sh(["git", "-C", lane, "rev-parse", rev + ":" + COUNTER_REL]).stdout.strip()
    sh(["git", "-C", lane, "replace", real_oid, evil_oid])
    rc, out = run_checker(lane, rev)
    ok = "replace-refs-present" in out
    rec("A01", "forge-replace-ref: refs/replace on the counter blob in the lane clone",
        "exit=%d out=%r" % (rc, out.strip().splitlines()[-3:]),
        "exit 2, DISPOSITION_SETUP replace-refs-present (plan C2 wording)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a02_ambient_git_dir():
    """ambient GIT_DIR/GIT_WORK_TREE must not redirect the checker's reads."""
    lane, rev, sha = build_fixture("a02")
    other = clone(os.path.join(S, "atk", "a02_other"))
    rc, out = run_checker(lane, rev, env={
        "GIT_DIR": os.path.join(other, ".git"),
        "GIT_WORK_TREE": other})
    ok = "DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0" in out
    rec("A02", "ambient GIT_DIR/GIT_WORK_TREE exported at the checker",
        "exit=%d out_tail=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "the checker must read the --lane it was given (rows=19 findings=0), not the ambient repo",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a03_git_config_count():
    """GIT_CONFIG_COUNT injection via ambient env."""
    lane, rev, sha = build_fixture("a03")
    rc, out = run_checker(lane, rev, env={
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.replaceRefs",
        "GIT_CONFIG_VALUE_0": "false"})
    ok = "DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0" in out
    rec("A03", "ambient GIT_CONFIG_COUNT=1 core.replaceRefs=false injection",
        "exit=%d out_tail=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "config injection must not change the verdict",
        "NONE (defended)" if ok else "MEDIUM", "defended" if ok else "VULNERABLE")


def a04_git_object_directory():
    """GIT_OBJECT_DIRECTORY / GIT_ALTERNATE_OBJECT_DIRECTORIES ambient."""
    lane, rev, sha = build_fixture("a04")
    other = clone(os.path.join(S, "atk", "a04_other"))
    rc, out = run_checker(lane, rev, env={
        "GIT_OBJECT_DIRECTORY": os.path.join(other, ".git/objects"),
        "GIT_ALTERNATE_OBJECT_DIRECTORIES": os.path.join(other, ".git/objects")})
    ok = "DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0" in out
    rec("A04", "ambient GIT_OBJECT_DIRECTORY + GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "exit=%d out_tail=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "object-store redirection must not change the verdict",
        "NONE (defended)" if ok else "MEDIUM", "defended" if ok else "VULNERABLE")


def a05_worktree_repo():
    """--lane pointing at a linked worktree of another repo."""
    lane, rev, sha = build_fixture("a05")
    wt = os.path.join(S, "atk", "a05_wt")
    if os.path.exists(wt):
        shutil.rmtree(wt)
    sh(["git", "-C", lane, "worktree", "add", "-q", "--detach", wt, rev])
    rc, out = run_checker(wt, rev)
    ok = "DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0" in out
    rec("A05", "--lane is a linked worktree of the lane repo (not a clone)",
        "exit=%d out_tail=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "checker reads the lane at --rev regardless of the physical layout",
        "NONE (informational)" if ok else "MEDIUM", "defended" if ok else "VULNERABLE")


def a06_worktree_only_receipt():
    """forge-handwritten: a receipt that exists only in the working tree."""
    lane, rev, sha = build_fixture("a06")
    rd = os.path.join(lane, RECEIPTS_REL)
    forged = ("control=hidden-c001\ncounter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
              % (sha, " ".join("%s=false" % x for x in
                               ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0",
                                "trivial0", "inconclusive0", "unstable0", "note",
                                "verdict_tables", "ids", "mismatched0", "figure", "witnessed",
                                "source", "coverage", "n_min"])))
    open(os.path.join(rd, "hidden-c001.out"), "w").write(forged)  # overwrite, never committed
    rc, out = run_checker(lane, rev)
    ok = "receipt-absent-at-rev" in out
    rec("A06", "forge-handwritten: receipt written in the working tree only (not committed)",
        "exit=%d out_tail=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "exit 1, finding receipt-absent-at-rev (plan C2 wording)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a07_copied_digest_forged_body():
    """counter_sha= copied from the honest counter while the body is forged."""
    def mutate(lane, rd, sha):
        st = "hidden-c001"
        p = os.path.join(rd, st + ".out")
        body = open(p).read()
        # keep the honest counter_sha, forge the conjunct body entirely
        forged = ("control=%s\ncounter_sha=%s\nexit=1\nC1_CONJUNCTS verdict_tables=false\n"
                  % (st, sha))
        open(p, "w").write(forged)
    lane, rev, sha = build_fixture("a07", mutate_receipt=mutate)
    rc, out = run_checker(lane, rev)
    # the forged receipt shows only verdict_tables=false; the ids row names renamed-result
    has_no_flip = "no-flip" in out or "conjunct-absent" in out
    rec("A07", "counter_sha= copied from the honest counter while the receipt BODY is forged",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:3]),
        "the receipt must show the conjunct FALSE; a body carrying only some conjuncts is a finding",
        "NONE (defended)" if has_no_flip else "MEDIUM",
        "defended" if has_no_flip else "PARTIAL")


def a08_two_counter_sha_lines():
    """two counter_sha= lines in one receipt."""
    def mutate(lane, rd, sha):
        p = os.path.join(rd, "hidden-c001.out")
        body = open(p).read()
        open(p, "w").write("counter_sha=" + "0" * 64 + "\n" + body)
    lane, rev, sha = build_fixture("a08", mutate_receipt=mutate)
    rc, out = run_checker(lane, rev)
    ok = "receipt-counter-sha-mismatch" in out
    rec("A08", "two counter_sha= lines: a bogus one prepended before the honest one",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:3]),
        "the first counter_sha= line is authoritative (documented); a bogus first line must be a mismatch finding",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a09_case_variant():
    """counter_sha= with a different case / whitespace."""
    for label, repl, expect in [
        ("counter_sha = <hex> (space before =)", "counter_sha = ", "mismatch-or-absent"),
        ("Counter_sha=<hex> (capital C)", "Counter_sha=", "mismatch-or-absent"),
        ("COUNTER_SHA=<hex> (all caps)", "COUNTER_SHA=", "mismatch-or-absent"),
    ]:
        def mutate(lane, rd, sha, repl=repl):
            p = os.path.join(rd, "hidden-c001.out")
            body = open(p).read()
            open(p, "w").write(body.replace("counter_sha=", repl, 1))
        lane, rev, sha = build_fixture("a09_" + str(abs(hash(label)) % 10000),
                                       mutate_receipt=mutate)
        rc, out = run_checker(lane, rev)
        findings = [l for l in out.splitlines() if "FINDING" in l]
        got = "mismatch" if any("counter-sha-mismatch" in f for f in findings) else \
              ("absent" if any("receipt-absent" in f for f in findings) else "NONE")
        rec("A09." + label.split(" ")[0], "counter_sha label variant: " + label,
            "exit=%d finding=%s" % (rc, got),
            "a counter_sha line the checker does not recognise must not be accepted as the honest digest",
            "NONE (defended)" if got != "NONE" else "MEDIUM",
            "defended" if got != "NONE" else "VULNERABLE")


def a10_truncated_digest():
    """truncated counter_sha digest."""
    def mutate(lane, rd, sha):
        p = os.path.join(rd, "hidden-c001.out")
        body = open(p).read()
        open(p, "w").write(body.replace("counter_sha=" + sha, "counter_sha=" + sha[:63], 1))
    lane, rev, sha = build_fixture("a10", mutate_receipt=mutate)
    rc, out = run_checker(lane, rev)
    ok = "receipt-counter-sha-mismatch" in out
    rec("A10", "truncated counter_sha digest (63 hex chars)",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:2]),
        "a 63-hex digest must not match the 64-hex counter blob digest (SHA_RE fullmatch)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a11_counter_sha_in_body_text():
    """counter_sha= as a substring of another line, not at line start."""
    def mutate(lane, rd, sha):
        p = os.path.join(rd, "hidden-c001.out")
        body = open(p).read()
        open(p, "w").write(body.replace("counter_sha=" + sha,
                                        "see counter_sha=" + sha + " for details", 1))
    lane, rev, sha = build_fixture("a11", mutate_receipt=mutate)
    rc, out = run_checker(lane, rev)
    ok = "receipt-counter-sha-mismatch" in out
    rec("A11", "counter_sha= appears mid-line (not as a line-prefixed label)",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:2]),
        "only a line whose stripped form starts with counter_sha= counts",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a12_state_name_traversal():
    """a manifest state name that traverses out of the receipts dir."""
    def mutate(lane, rd, sha):
        man_p = os.path.join(lane, ".ufo/evidence/round-95/conjunct-disposition.json")
        man = json.load(open(man_p))
        man["rows"]["ids"]["state"] = "../../../../etc/passwd"
        json.dump(man, open(man_p, "w"), indent=1)
    lane, rev, sha = build_fixture("a12", mutate_receipt=mutate)
    rc, out = run_checker(lane, rev)
    leak = "passwd" in out and "root:" in out
    rec("A12", "manifest state name with ../ traversal out of the receipts tree",
        "exit=%d leak=%s findings=%r" % (rc, leak, [l for l in out.splitlines() if "FINDING" in l][:2]),
        "git pathspec traversal must not read outside the receipts tree",
        "HIGH" if leak else "NONE (defended)", "VULNERABLE" if leak else "defended")


def a13_receipts_dir_override():
    """--receipts pointing somewhere else entirely."""
    lane, rev, sha = build_fixture("a13")
    other = os.path.join(S, "atk", "a13_elsewhere")
    os.makedirs(other, exist_ok=True)
    # copy the receipts to a filesystem dir outside the object store
    shutil.rmtree(other, ignore_ok=True)
    shutil.copytree(os.path.join(lane, RECEIPTS_REL), other)
    rc, out = run_checker(lane, rev, extra=["--receipts", other])
    findings = [l for l in out.splitlines() if "FINDING" in l]
    rec("A13", "--receipts overridden to a filesystem directory outside the object store",
        "exit=%d findings=%d %r" % (rc, len(findings), findings[:2]),
        "the checker reads receipts from the object store at --rev; --receipts must not redirect the read to the filesystem",
        "HIGH" if not findings else "NONE (defended)",
        "VULNERABLE" if not findings else "defended")


def a14_revoke_replace_ref_midflight():
    """replace refs in the FLEET repo (the gate repo) — the checker does not read it,
    but the counter does. Verify the checker's replace-ref gate scope."""
    lane, rev, sha = build_fixture("a14")
    # plant a replace ref in the lane's clone; the checker must refuse at setup
    real = sh(["git", "-C", lane, "rev-parse", rev + ":" + COUNTER_REL]).stdout.strip()
    p = subprocess.run("git -C %s hash-object -w --stdin <<'EOF'\nbogus\nEOF" % lane,
                       shell=True, capture_output=True, text=True,
                       env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"})
    evil = p.stdout.strip()
    sh(["git", "-C", lane, "replace", real, evil])
    rc, out = run_checker(lane, rev)
    ok = "replace-refs-present" in out
    rec("A14", "replace ref present in the lane clone at the time of the check",
        "exit=%d out=%r" % (rc, [l for l in out.splitlines() if "SETUP" in l or "rows=" in l]),
        "exit 2, DISPOSITION_SETUP replace-refs-present",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a15_empty_rev():
    """--rev '' : git reads the INDEX, not a commit."""
    lane, rev, sha = build_fixture("a15")
    # stage a forged receipt without committing
    rd = os.path.join(lane, RECEIPTS_REL)
    p = os.path.join(rd, "hidden-c001.out")
    open(p, "w").write("control=hidden-c001\ncounter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                       % (sha, " ".join("%s=false" % x for x in
                                        ["selfpin", "pins", "spec", "pin", "green", "canary",
                                         "valid0", "trivial0", "inconclusive0", "unstable0",
                                         "note", "verdict_tables", "ids", "mismatched0",
                                         "figure", "witnessed", "source", "coverage", "n_min"])))
    sh(["git", "-C", lane, "add", "-A"])
    rc, out = run_checker(lane, "")
    findings = [l for l in out.splitlines() if "FINDING" in l]
    idx_leak = "rows=19" in out
    rec("A15", "--rev '' : git resolves ':<path>' against the INDEX, not a commit",
        "exit=%d rows_line=%r findings=%d" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")], len(findings)),
        "an empty --rev must not grade staged-but-uncommitted bytes",
        "HIGH" if idx_leak else "NONE (defended)", "VULNERABLE" if idx_leak else "defended")


def a16_counter_replaced_by_commit():
    """the counter blob at --rev is replaced by a *commit* that edits the counter:
    the checker reads the counter at --rev, so the honest one at --rev is what is read."""
    lane, rev, sha = build_fixture("a16")
    # a later commit changes the counter bytes; the receipts still carry the old sha
    cp = os.path.join(lane, COUNTER_REL)
    b = open(cp).read()
    open(cp, "w").write(b + "\n# late edit\n")
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", "counter edited later"])
    rev2 = sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()
    rc, out = run_checker(lane, rev2)
    ok = "receipt-counter-sha-mismatch" in out
    rec("A16", "counter blob edited in a later commit; receipts carry the older digest",
        "exit=%d findings=%d" % (rc, len([l for l in out.splitlines() if "FINDING" in l])),
        "receipts must be refused with receipt-counter-sha-mismatch when the counter at --rev differs",
        "NONE (defended)" if ok else "MEDIUM", "defended" if ok else "PARTIAL")


def main():
    os.makedirs(os.path.join(S, "atk"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [a01_replace_ref_counter, a02_ambient_git_dir, a03_git_config_count,
               a04_git_object_directory, a05_worktree_repo, a06_worktree_only_receipt,
               a07_copied_digest_forged_body, a08_two_counter_sha_lines, a09_case_variant,
               a10_truncated_digest, a11_counter_sha_in_body_text, a12_state_name_traversal,
               a13_receipts_dir_override, a14_revoke_replace_ref_midflight, a15_empty_rev,
               a16_counter_replaced_by_commit]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-40s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-c2-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
