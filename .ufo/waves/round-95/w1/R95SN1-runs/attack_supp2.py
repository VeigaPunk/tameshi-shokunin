#!/usr/bin/env python3
"""R95SN1 corrected supplementary attacks (D02/D06 redone with a correct pin
recomputation), plus the plan's own forge-counter-sha control."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/tameshi-r95/R95SN1"
LANE_SRC = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CHECKER = S + "/snap/conjunct-disposition-v95.py"
COUNTER_REL = ".ufo/evidence/round-95/c1/measure-v95.py"
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
PIN_BYTES = rb'^SELF_SHA256 = "[0-9a-f]{64}"\n'
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
    top = sh(["git", "-C", lane_toplevel(dest), "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(dest), "toplevel mismatch " + dest
    return dest


def lane_toplevel(dest):
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


def recompute_pin_bytes(b):
    """Exactly the instrument's algorithm: strip every pin line, hash, put back."""
    norm = re.sub(PIN_BYTES, b"", b, flags=re.M)
    h = hashlib.sha256(norm).hexdigest().encode()
    return re.sub(PIN_BYTES, b'SELF_SHA256 = "' + h + b'"\n', b, count=1, flags=re.M)


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


def build(name, forge_receipt=None):
    d = os.path.join(S, "atk5", name)
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
        if row["mode"] == "setup-refusal":
            body = "counter_sha=%s\nexit=2\nC1_SETUP %s\n" % (sha, row["token"])
        else:
            body = ("counter_sha=%s\nexit=1\nC1_CONJUNCTS %s\n"
                    % (sha, " ".join("%s=false" % x for x in KEYS)))
        open(os.path.join(rd, st + ".out"), "w").write(body)
    if forge_receipt:
        forge_receipt(lane, rd, sha)
    return lane, sha


def e01_counter_keys_tampered():
    """counter at --rev: one conjunct key removed, pin CORRECTLY recomputed."""
    lane, sha = build("e01")
    cp = os.path.join(lane, COUNTER_REL)
    b = open(cp, "rb").read()
    tampered = b.replace(b'"note", "verdict_tables", "ids", "mismatched0",',
                         b'"note", "verdict_tables", "mismatched0",', 1)
    assert tampered != b
    new = recompute_pin_bytes(tampered)
    # verify the instrument would accept this pin
    norm = re.sub(PIN_BYTES, b"", new, flags=re.M)
    const = re.search(PIN_BYTES, new, re.M).group(0)
    h = re.search(rb'"([0-9a-f]{64})"', const).group(1).decode()
    assert hashlib.sha256(norm).hexdigest() == h, "fixture pin recompute wrong"
    open(cp, "wb").write(new)
    rev = commit_all(lane, "tampered counter, pin recomputed")
    rc, out = run_checker(lane, rev)
    findings = [l for l in out.splitlines() if "FINDING" in l]
    setup = [l for l in out.splitlines() if "SETUP" in l]
    refused = rc == 1 and findings
    rec("E01", "counter at --rev with a conjunct key REMOVED and the pin correctly recomputed",
        "exit=%d setup=%r findings=%r" % (rc, setup[:1], findings[:3]),
        "the manifest row for the removed conjunct must become a finding (unknown-key)",
        "NONE (defended)" if refused else "MEDIUM",
        "defended" if refused else "VULNERABLE")


def e02_counter_extra_key():
    """counter at --rev with an EXTRA conjunct key, pin correctly recomputed."""
    lane, sha = build("e02")
    cp = os.path.join(lane, COUNTER_REL)
    b = open(cp, "rb").read()
    tampered = b.replace(b'"note", "verdict_tables", "ids", "mismatched0",',
                         b'"note", "verdict_tables", "ids", "mismatched0", "extra_key",', 1)
    assert tampered != b
    new = recompute_pin_bytes(tampered)
    open(cp, "wb").write(new)
    rev = commit_all(lane, "counter with extra key")
    rc, out = run_checker(lane, rev)
    findings = [l for l in out.splitlines() if "FINDING" in l]
    rec("E02", "counter at --rev with an EXTRA conjunct key, pin correctly recomputed",
        "exit=%d findings=%r" % (rc, findings[:3]),
        "the manifest must be found incomplete (missing-row) for the new key",
        "NONE (defended)" if findings else "MEDIUM",
        "defended" if findings else "VULNERABLE")


def e03_forge_counter_sha_control():
    """THE PLAN'S OWN CONTROL: a committed receipt whose counter_sha= is 0*64."""
    def forge(lane, rd, sha):
        p = os.path.join(rd, "hidden-c001.out")
        body = open(p).read()
        open(p, "w").write(body.replace("counter_sha=" + sha, "counter_sha=" + "0" * 64, 1))
    lane, sha = build("e03", forge_receipt=forge)
    rev = commit_all(lane, "forged counter_sha receipt")
    rc, out = run_checker(lane, rev)
    ok = "receipt-counter-sha-mismatch" in out and rc == 1
    rec("E03", "plan control forge-counter-sha: a COMMITTED receipt with counter_sha=0*64",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:2]),
        "exit 1 with the named finding receipt-counter-sha-mismatch (plan C2 wording)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def e04_counter_edited_refuses_before_receipt_check():
    """counter edited at --rev WITHOUT recomputing the pin: which refusal fires?"""
    lane, sha = build("e04")
    cp = os.path.join(lane, COUNTER_REL)
    open(cp, "a").write("\n# post-freeze edit\n")
    rev = commit_all(lane, "counter edited after the receipts")
    rc, out = run_checker(lane, rev)
    setup = [l for l in out.splitlines() if "SETUP" in l]
    rec("E04", "counter edited at --rev WITHOUT a pin recompute: the counter's own self-pin "
                "refuses before the counter_sha binding is reached",
        "exit=%d out=%r" % (rc, setup[:1] or [l for l in out.splitlines() if "FINDING" in l][:2]),
        "a refusal is required; the named finding differs from receipt-counter-sha-mismatch "
        "because the counter's self-pin gate fires first (the counter_sha binding is a "
        "SECOND line of defence for the honest-counter case, exercised by E03)",
        "NONE (defended)" if rc != 0 else "MEDIUM",
        "defended" if rc != 0 else "VULNERABLE")


def e05_receipt_counter_sha_of_other_counter():
    """receipts carrying the counter_sha of a DIFFERENT (older) counter revision."""
    lane, sha = build("e05")
    other_sha = hashlib.sha256(b"some other counter bytes").hexdigest()
    for st in ("hidden-c001", "renamed-result"):
        p = os.path.join(lane, RECEIPTS_REL, st + ".out")
        body = open(p).read()
        open(p, "w").write(body.replace("counter_sha=" + sha, "counter_sha=" + other_sha, 1))
    rev = commit_all(lane, "receipts with a foreign counter_sha")
    rc, out = run_checker(lane, rev)
    ok = "receipt-counter-sha-mismatch" in out
    rec("E05", "two receipts carrying the counter_sha of a DIFFERENT counter revision",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:3]),
        "exit 1 with receipt-counter-sha-mismatch",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def main():
    os.makedirs(os.path.join(S, "atk5"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [e01_counter_keys_tampered, e02_counter_extra_key,
               e03_forge_counter_sha_control, e04_counter_edited_refuses_before_receipt_check,
               e05_receipt_counter_sha_of_other_counter]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-46s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-supp2-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
