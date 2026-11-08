#!/usr/bin/env python3
"""R95SN1: corrected B04 (replace ref in the FLEET repo) and B11 (recomputed
malicious pin), plus B15 (the counter's --repo is a worktree of another repo
carrying a replace ref)."""
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
PIN_BYTES = rb'^SELF_SHA256 = "[0-9a-f]{64}"\n'
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


def run_counter(lane, rev, work, counter=COUNTER, env=None, timeout=500):
    e = dict(os.environ)
    if env:
        e.update(env)
    cmd = [sys.executable, "-I", counter, "--repo", lane, "--rev", rev, "--work", work]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=e, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"


def fresh_work(name):
    w = os.path.join(S, "wk1", name)
    shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    return w


def recompute_pin_bytes(b):
    norm = re.sub(PIN_BYTES, b"", b, flags=re.M)
    h = hashlib.sha256(norm).hexdigest().encode()
    return re.sub(PIN_BYTES, b'SELF_SHA256 = "' + h + b'"\n', b, count=1, flags=re.M)


def i04_fleet_replace_ref():
    """A replace ref in the FLEET repo (the gate repo the counter executes from)."""
    base = os.path.join(S, "atkA")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    lane = clone(os.path.join(base, "lane"))
    fl = clone(os.path.join(base, "fleet"))
    # the fleet clone must contain the pinned gate commit
    spec_p = os.path.join(lane, ".ufo/evidence/round-94/c1/census-mutants.json")
    spec = json.load(open(spec_p))
    gate_commit = spec["gate"]["commit"]
    gate_path = spec["gate"]["path"]
    have = sh(["git", "-C", fl, "cat-file", "blob", gate_commit + ":" + gate_path])
    assert have.returncode == 0, "fleet clone lacks the gate blob"
    # plant a replace ref on the gate blob inside the fleet clone
    evil = sh("git -C %s hash-object -w --stdin <<'EOF'\n#!/bin/sh\nexit 0\nEOF" % fl,
              shell=True, env=SEAL).stdout.strip()
    real = sh(["git", "-C", fl, "rev-parse", gate_commit + ":" + gate_path]).stdout.strip()
    sh(["git", "-C", fl, "replace", real, evil], env=SEAL)
    # repoint the spec's gate repo at the clone and re-pin the spec
    spec["gate"]["repo"] = fl
    json.dump(spec, open(spec_p, "w"), indent=1)
    sh(["git", "-C", lane, "add", "-A"])
    sh(["git", "-C", lane, "-c", "user.name=atk", "-c", "user.email=atk@invalid",
        "commit", "-qm", "gate repo repointed"])
    rc, out = run_counter(lane, "HEAD", fresh_work("i04"))
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS", "C1_SUMMARY"))]
    ok = "replace-refs-present:fleet" in out
    rec("I04", "refs/replace on the GATE blob inside the FLEET repo the counter executes from",
        "exit=%s out=%r" % (rc, got[:3]),
        "exit 2, C1_SETUP replace-refs-present:fleet (the counter checks the fleet repo too)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def i11_recomputed_malicious_pin():
    """A counter edited to force ok=True with the SELF_SHA256 pin RECOMPUTED."""
    src = open(COUNTER, "rb").read()
    evil = src.replace(b'    ok = all(conj.values())', b'    ok = True  # MALICIOUS', 1)
    assert evil != src, "anchor not found"
    new = recompute_pin_bytes(evil)
    # prove the fixture's pin satisfies the instrument's own algorithm
    norm = re.sub(PIN_BYTES, b"", new, flags=re.M)
    const = re.search(PIN_BYTES, new, re.M).group(0)
    h = re.search(rb'"([0-9a-f]{64})"', const).group(1).decode()
    assert hashlib.sha256(norm).hexdigest() == h, "fixture pin recompute wrong"
    p = os.path.join(S, "atkA", "counter-recomputed.py")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(new)
    lane = clone(os.path.join(S, "atkA", "lane11"))
    rc, out = run_counter(lane, "HEAD", fresh_work("i11"), counter=p)
    selfpin_ok = "self-pin-mismatch" not in out and "self-pin-line-count" not in out
    claims_pass = "C1_R95_PASS=true" in out
    rec("I11", "counter edited to force ok=True with the SELF_SHA256 pin CORRECTLY RECOMPUTED",
        "exit=%s self_pin_passed=%s claims_C1_R95_PASS=true=%s out=%r" % (
            rc, selfpin_ok, claims_pass,
            [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS"))][:2]),
        "the self-pin certifies the file's OWN bytes, not the executed bytes; identity is "
        "bound by kill rule (c) (the counter blob's sha256 in claims.json), which no "
        "instrument check can substitute for",
        "MEDIUM (declared limit)", "accepted-by-design" if selfpin_ok else "defended")


def i12_double_pin_same_hash():
    """A SECOND pin line with the SAME digest: is the line COUNT still checked?"""
    src = open(COUNTER, "rb").read()
    guard = b'\nif __name__ == "__main__":'
    m = re.search(PIN_BYTES, src, re.M)
    same = m.group(0)
    evil = src.replace(guard, b"\n" + same + guard, 1)
    p = os.path.join(S, "atkA", "counter-double-same.py")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(evil)
    lane = clone(os.path.join(S, "atkA", "lane12"))
    rc, out = run_counter(lane, "HEAD", fresh_work("i12"), counter=p)
    got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS"))]
    ok = "self-pin-line-count" in out
    rec("I12", "a SECOND SELF_SHA256 line with the SAME digest as the first",
        "exit=%s out=%r" % (rc, got[:2]),
        "exit 2, C1_SETUP self-pin-line-count (the count, not the digest, must catch it)",
        "NONE (defended)" if ok else "HIGH", "defended" if ok else "VULNERABLE")


def i13_pin_line_uppercase_or_spaced():
    """Pin lines the regex does NOT match must not slip past the count check."""
    variants = [
        ("uppercase hex", b'SELF_SHA256 = "' + b"A" * 64 + b'"\n'),
        ("single quotes", b"SELF_SHA256 = '" + b"0" * 64 + b"'\n"),
        ("no spaces", b'SELF_SHA256="' + b"0" * 64 + b'"\n'),
        ("trailing spaces", b'SELF_SHA256 = "' + b"0" * 64 + b'"  \n'),
    ]
    for label, line in variants:
        src = open(COUNTER, "rb").read()
        guard = b'\nif __name__ == "__main__":'
        evil = src.replace(guard, b"\n" + line + guard, 1)
        p = os.path.join(S, "atkA", "counter-pinvar.py")
        open(p, "wb").write(evil)
        lane = clone(os.path.join(S, "atkA", "lane13"))
        rc, out = run_counter(lane, "HEAD", fresh_work("i13"), counter=p)
        got = [l for l in out.splitlines() if l.startswith(("C1_SETUP", "C1_R95_PASS"))]
        refused = rc == 2
        rec("I13." + label.replace(" ", "_"), "second pin line that the regex does not match: " + label,
            "exit=%s out=%r" % (rc, got[:2]),
            "the counter must refuse (exit 2): an unrecognised pin line either changes the "
            "executed constant or is inert, and either way the file's bytes changed, so the "
            "digest check must fire",
            "NONE (defended)" if refused else "MEDIUM",
            "defended" if refused else "VULNERABLE")


def main():
    os.makedirs(os.path.join(S, "atkA"), exist_ok=True)
    only = sys.argv[1:]
    for fn in [i04_fleet_replace_ref, i11_recomputed_malicious_pin, i12_double_pin_same_hash,
               i13_pin_line_uppercase_or_spaced]:
        if only and not any(o in fn.__name__ for o in only):
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            rec(fn.__name__, "ATTACK ERROR", repr(e), "no exception", "INFO", "error")
            traceback.print_exc()
        print("%-42s %s" % (fn.__name__, RESULTS[-1]["verdict"]))
    out = os.path.join(S, "runs", "R95SN1-c1b-results.json")
    json.dump(RESULTS, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
