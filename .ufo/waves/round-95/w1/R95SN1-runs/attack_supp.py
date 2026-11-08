#!/usr/bin/env python3
"""R95SN1 supplementary attacks: make-pins95 write path, C2 hand-written
receipt with the honest digest, C2 counter-key tampering, C2 selftest."""
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
PINS = S + "/snap/make-pins95.py"
COUNTER_REL = ".ufo/evidence/round-95/c1/measure-v95.py"
RECEIPTS_REL = ".ufo/evidence/round-95/pre-freeze/controls"
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


def d01_handwritten_receipts_with_honest_digest():
    d = os.path.join(S, "atk4", "d01")
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
    rev = commit_all(lane, "hand-written receipts")
    rc, out = run_checker(lane, rev)
    green = "DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0" in out
    rec("D01", "every C2 receipt hand-written with the honest counter_sha and no counter run",
        "exit=%d out=%r" % (rc, [l for l in out.splitlines() if l.startswith("DISPOSITION ")]),
        "the checker certifies that a committed receipt MOVED the conjunct; a hand-written "
        "text file carrying the right digest and the right conjunct line is indistinguishable "
        "(plan declared limit: counter_sha binds the receipt to the counter blob, not to a run)",
        "MEDIUM (declared limit, unchanged from round 94 F3)", "accepted-by-design")


def d02_counter_keys_tampered():
    d = os.path.join(S, "atk4", "d02")
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
    cp = os.path.join(lane, COUNTER_REL)
    b = open(cp).read()
    tampered = b.replace('"note", "verdict_tables", "ids", "mismatched0",',
                          '"note", "verdict_tables", "mismatched0",', 1)
    assert tampered != b
    norm = re.sub(r'^SELF_SHA256 = "[0-9a-f]{64}"\n', "", tampered, flags=re.M)
    h = hashlib.sha256(norm.encode()).hexdigest()
    tampered = re.sub(r'^SELF_SHA256 = "[0-9a-f]{64}"\n',
                      'SELF_SHA256 = "%s"\n' % h, tampered, count=1)
    open(cp, "w").write(tampered)
    rev = commit_all(lane, "tampered counter")
    rc, out = run_checker(lane, rev)
    refused = rc == 1 and "FINDING" in out
    rec("D02", "counter blob at --rev with a recomputed pin and a conjunct key removed",
        "exit=%d findings=%r" % (rc, [l for l in out.splitlines() if "FINDING" in l][:3]),
        "the checker must detect the manifest rows the counter no longer prints",
        "NONE (defended)" if refused else "MEDIUM",
        "defended" if refused else "VULNERABLE")


def d03_make_pins_empty_lane():
    base = os.path.join(S, "atk4", "d03")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(os.path.join(base, "cwd"))
    p = sh([sys.executable, "-I", PINS, "--lane", "", "--rev", "HEAD"], cwd=base)
    wrote = os.path.exists(os.path.join(base, ".ufo/evidence/round-95/c1/pins.json"))
    rec("D03", "make-pins95.py --lane '' (empty): os.path.realpath('') is the process CWD",
        "exit=%d wrote_into_cwd=%s stdout=%r" % (p.returncode, wrote, p.stdout.strip()[:120]),
        "an empty --lane must be refused; realpath('') is the CWD, which for the fleet "
        "host guard is the fleet root (a git repo)",
        "MEDIUM" if wrote else "NONE (defended)",
        "VULNERABLE" if wrote else "defended")


def d04_make_pins_symlink():
    base = os.path.join(S, "atk4", "d04")
    shutil.rmtree(base, ignore_errors=True)
    lane = clone(os.path.join(base, "lane"))
    stage_instruments(lane)
    outside = os.path.join(base, "outside.txt")
    open(outside, "w").write("ORIGINAL\n")
    pins_p = os.path.join(lane, ".ufo/evidence/round-95/c1/pins.json")
    if os.path.exists(pins_p):
        os.unlink(pins_p)
    os.symlink(outside, pins_p)
    rev = sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()
    p = sh([sys.executable, "-I", PINS, "--lane", lane, "--rev", rev])
    followed = open(outside).read() != "ORIGINAL\n"
    rec("D04", "make-pins95.py with a symlink at .ufo/evidence/round-95/c1/pins.json",
        "exit=%d outside_target_overwritten=%s" % (p.returncode, followed),
        "the write must not follow a symlink out of the lane (no O_EXCL/O_NOFOLLOW today)",
        "MEDIUM" if followed else "NONE (defended)",
        "VULNERABLE" if followed else "defended")


def d05_selftest():
    p = sh([sys.executable, "-I", CHECKER, "--selftest"])
    out = p.stdout
    line = [l for l in out.splitlines() if l.startswith("DISPOSITION_SELFTEST")]
    ok = p.returncode == 0 and line and "/11 pass" in line[0]
    rec("D05", "C2 checker --selftest: does the selftest run 11 cases and pass?",
        "exit=%d line=%r" % (p.returncode, line),
        "DISPOSITION_SELFTEST: 11/11 pass, exit 0 (plan C2 After)",
        "NONE (defended)" if ok else "MEDIUM", "defended" if ok else "PARTIAL")


def d06_counter_sha_of_wrong_revision():
    d = os.path.join(S, "atk4", "d06")
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
    cp = os.path.join(lane, COUNTER_REL)
    open(cp, "a").write("\n# post-freeze edit\n")
    rev = commit_all(lane, "counter edited after the receipts")
    rc, out = run_checker(lane, rev)
    ok = "receipt-counter-sha-mismatch" in out
    rec("D06", "receipts carrying the counter_sha of the PREVIOUS counter revision",
        "exit=%d findings=%d" % (rc, len([l for l in out.splitlines() if "FINDING" in l])),
        "the checker must refuse with receipt-counter-sha-mismatch",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def d07_checker_tmp_usage():
    src = open(CHECKER).read()
    hits = []
    for i, line in enumerate(src.split("\n"), 1):
        if "TemporaryDirectory" in line or "mkdtemp" in line:
            hits.append("%d:%s" % (i, line.strip()[:80]))
    rec("D07", "C2 checker temp-dir allocation (default TMPDIR)",
        "hits=%r" % hits,
        "the checker must not allocate in the default temp root without an explicit TMPDIR "
        "(round-94 F9 pattern)",
        "LOW" if hits else "NONE (defended)", "observed" if hits else "defended")


def main():
    os.makedirs(os.path.join(S, "atk4"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [d01_handwritten_receipts_with_honest_digest, d02_counter_keys_tampered,
               d03_make_pins_empty_lane, d04_make_pins_symlink, d05_selftest,
               d06_counter_sha_of_wrong_revision, d07_checker_tmp_usage]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-42s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-supp-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
