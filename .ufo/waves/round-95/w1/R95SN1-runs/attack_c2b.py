#!/usr/bin/env python3
"""R95SN1 corrected C2 attacks: A06 (forge-handwritten, no committed receipt),
A07 (receipt text claims a conjunct false with no evidence), A13 (--receipts
override), A15b (empty --rev), A17 (receipt present at rev but for a state the
manifest does not name)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

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
        raise RuntimeError("cmd failed: %s\n%s" % (cmd, p.stderr))
    return p


def clone(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    sh(["git", "clone", "-q", "--shared", LANE_SRC, dest])
    top = sh(["git", "-C", dest, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def commit_all(lane, msg):
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", msg])
    return sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()


def stage_instruments(lane):
    shutil.copytree(os.path.join(LANE_SRC, ".ufo/evidence/round-95"),
                    os.path.join(lane, ".ufo/evidence/round-95"), dirs_exist_ok=True)
    shutil.rmtree(os.path.join(lane, ".ufo/evidence/round-95/c1/__pycache__"),
                  ignore_errors=True)


def run_checker(lane, rev, extra=None, env=None):
    cmd = [sys.executable, "-I", CHECKER, "--lane", lane, "--rev", rev,
           "--min-falsifiable", "17"]
    if extra:
        cmd += extra
    e = dict(os.environ)
    if env:
        e.update(env)
    p = sh(cmd, env=e)
    return p.returncode, p.stdout + p.stderr


KEYS = ["selfpin", "pins", "spec", "pin", "green", "canary", "valid0", "trivial0",
        "inconclusive0", "unstable0", "note", "verdict_tables", "ids", "mismatched0",
        "figure", "witnessed", "source", "coverage", "n_min"]


def build(name, omit_receipts=(), forge=None, extra_receipts=None):
    d = os.path.join(S, "atk6", name)
    lane = clone(d)
    stage_instruments(lane)
    blob = sh(["git", "-C", lane, "cat-file", "blob", "HEAD:" + COUNTER_REL]).stdout
    sha = hashlib.sha256(blob.encode()).hexdigest()
    man = json.load(open(os.path.join(lane, ".ufo/evidence/round-95/conjunct-disposition.json")))
    rd = os.path.join(lane, RECEIPTS_REL)
    os.makedirs(rd, exist_ok=True)
    for k, row in man["rows"].items():
        if "unfalsifiable" in row:
            continue
        st = row["state"]
        if st in omit_receipts:
            continue
        if row["mode"] == "setup-refusal":
            body = "counter_sha=%s\nexit=2\nC1_SETUP %s\n" % (sha, row["token"])
        else:
            body = ("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(rd, st + ".out"), "w").write(body)
    if extra_receipts:
        for fn, body in extra_receipts.items():
            open(os.path.join(rd, fn), "w").write(body)
    if forge:
        forge(lane, rd, sha)
    return lane, sha, rd


def a06_forge_handwritten_no_committed_receipt():
    """The plan's control: a receipt named for a manifest state, hand-written,
    placed ONLY in the working tree (the committed tree has no such receipt)."""
    def forge(lane, rd, sha):
        # the committed tree has NO hidden-c001.out; the working tree gets a hand-written one
        p = os.path.join(rd, "hidden-c001.out")
        open(p, "w").write("control=hidden-c001\ncounter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                           % (sha, " ".join("%s=false" % x for x in KEYS)))
        # remove it from the index: it must be uncommitted
        sh(["git", "-C", lane, "rm", "-q", "--cached", ".ufo/evidence/round-95/pre-freeze/controls/hidden-c001.out"],
           check=False)
    lane, sha, rd = build("a06", omit_receipts=("hidden-c001",), forge=forge)
    rev = commit_all(lane, "no hidden-c001 receipt committed")
    # the working-tree copy must exist but be uncommitted
    st = sh(["git", "-C", lane, "status", "--porcelain"]).stdout.strip()
    rc, out = run_checker(lane, rev)
    ok = "receipt-absent-at-rev" in out and rc == 1
    rec("A06", "plan control forge-handwritten: receipt hand-written, in the working tree "
               "ONLY (never committed), for the manifest state verdict_tables",
        "exit=%d git_status=%r findings=%r" % (
            rc, st[:80], [l for l in out.splitlines() if "FINDING" in l][:2]),
        "exit 1 with the named finding receipt-absent-at-rev (plan C2 wording)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def a07_receipt_text_claims_without_evidence():
    """The receipt for the `ids` row is replaced with a hand-written file that
    merely SAYS ids=false, with no counter run behind it."""
    def forge(lane, rd, sha):
        p = os.path.join(rd, "renamed-result.out")
        open(p, "w").write("counter_sha=%s\nexit=1\nC1_CONJUNCTS ids=false\n" % sha)
    lane, sha, rd = build("a07", forge=forge)
    rev = commit_all(lane, "renamed-result receipt hand-written")
    rc, out = run_checker(lane, rev)
    green = "findings=0" in out
    rec("A07", "receipt for the `ids` row hand-written to CLAIM ids=false, no counter run",
        "exit=%d out=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "the checker certifies that a committed receipt MOVED the conjunct; a hand-written "
        "file that merely asserts the conjunct is false is indistinguishable from a real "
        "receipt (plan declared limit; counter_sha binds to the counter blob, not to a run)",
        "MEDIUM (declared limit)" if green else "NONE (defended)",
        "accepted-by-design" if green else "defended")


def a13_receipts_dir_override():
    """--receipts redirected to a filesystem directory outside the object store."""
    lane, sha, rd = build("a13")
    other = os.path.join(S, "atk6", "a13_elsewhere")
    shutil.rmtree(other, ignore_errors=True)
    shutil.copytree(rd, other)
    # rewrite the copies so they would PASS if read from the filesystem
    for fn in os.listdir(other):
        p = os.path.join(other, fn)
        b = open(p).read()
        open(p, "w").write(b)
    rev = commit_all(lane, "a13 base")
    rc, out = run_checker(lane, rev, extra=["--receipts", other])
    findings = [l for l in out.splitlines() if "FINDING" in l]
    rows = [l for l in out.splitlines() if l.startswith("DISPOSITION ")]
    rec("A13", "--receipts overridden to a filesystem directory outside the object store",
        "exit=%d rows=%r findings=%d" % (rc, rows[-1:], len(findings)),
        "--receipts must still resolve inside the object store at --rev; a filesystem path "
        "must not become a readable receipt source",
        "HIGH" if not findings else "NONE (defended)",
        "VULNERABLE" if not findings else "defended")


def a15b_empty_rev():
    """--rev '' must not grade the git index."""
    lane, sha, rd = build("a15b")
    rev = commit_all(lane, "a15b base")
    # stage a forged receipt without committing
    p = os.path.join(rd, "renamed-result.out")
    body = open(p).read()
    open(p, "w").write("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                       % (sha, " ".join("%s=false" % x for x in KEYS)))
    sh(["git", "-C", lane, "add", "-A"])
    rc, out = run_checker(lane, "")
    setup = [l for l in out.splitlines() if "SETUP" in l]
    findings = [l for l in out.splitlines() if "FINDING" in l]
    leaked = any("rows=" in l and "findings=0" in l for l in out.splitlines())
    rec("A15b", "--rev '' : git resolves ':<path>' against the INDEX (staged bytes)",
        "exit=%d setup=%r leaked=%s" % (rc, setup[:1], leaked),
        "an empty --rev must be refused outright, not resolved against the index",
        "MEDIUM" if leaked else "NONE (defended)",
        "VULNERABLE" if leaked else "defended")


def a17_receipt_for_unnamed_state():
    """a committed receipt for a state the manifest does not name: is it ignored?"""
    lane, sha, rd = build("a17")
    rev = commit_all(lane, "a17 base")
    open(os.path.join(rd, "not-a-manifest-state.out"), "w").write(
        "counter_sha=%s\nexit=1\nC1_CONJUNCTS ids=false\n" % sha)
    rev = commit_all(lane, "extra receipt")
    rc, out = run_checker(lane, rev)
    rec("A17", "a committed receipt for a state the manifest does not name",
        "exit=%d out=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "the checker grades only what the manifest names; an extra receipt is inert",
        "INFO", "observed")


def a18_min_falsifiable_bypass():
    """a manifest with 17 unfalsifiable rows and 2 falsifiable: --min-falsifiable 17."""
    def forge(lane, rd, sha):
        p = os.path.join(lane, ".ufo/evidence/round-95/conjunct-disposition.json")
        man = json.load(open(p))
        rows = man["rows"]
        # swap: make 17 rows unfalsifiable with a digest-anchored reason
        dig = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
        for k in list(rows):
            if "unfalsifiable" in rows[k]:
                continue
            rows[k] = {"unfalsifiable":
                       "the sealed pin at digest %s forbids a committed falsifier for this "
                       "conjunct, so no battery state can move it" % dig}
        man["rows"] = rows
        json.dump(man, open(p, "w"), indent=1)
    lane, sha, rd = build("a18", forge=forge)
    rev = commit_all(lane, "all-unfalsifiable manifest")
    rc, out = run_checker(lane, rev)
    rows = [l for l in out.splitlines() if l.startswith("DISPOSITION ")]
    ok = "falsifiable-below-minimum" in out
    rec("A18", "manifest rewritten so every row is `unfalsifiable` (each with a digest anchor)",
        "exit=%d rows=%r" % (rc, rows[-1:]),
        "--min-falsifiable 17 must produce the finding falsifiable-below-minimum",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def main():
    os.makedirs(os.path.join(S, "atk6"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [a06_forge_handwritten_no_committed_receipt,
               a07_receipt_text_claims_without_evidence, a13_receipts_dir_override,
               a15b_empty_rev, a17_receipt_for_unnamed_state, a18_min_falsifiable_bypass]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-46s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-c2b-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
