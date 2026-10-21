#!/usr/bin/env python3
"""Independent F5 falsifier for surface `tameshi-runner` (round-21 w2).

Implements the seven-profile bwrap subprocess recipe from
.ufo/evidence/round-21/c2-contract.json `required_profiles` verbatim,
WITHOUT importing or reusing tools/env-diff.py or its helpers.

Reads only: the materialised pin blob (sha-verified) and the receipt JSON
for post-hoc producer comparison. Every tuple is recomputed from raw bytes.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

SCRATCH = "/tmp/tameshi-r21-ProfileTameshiRunner-s1"
BLOB_PATH = f"{SCRATCH}/target.sh"
EXPECTED_BLOB_SHA256 = "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b"
REPO = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
CONTRACT = f"{REPO}/.ufo/evidence/round-21/c2-contract.json"
RECEIPT = f"{REPO}/.ufo/evidence/round-21/f5/receipt-final-production.json"
RAWDIR = f"{SCRATCH}/raw"
PIN = {"repo": "tameshi-shokunin",
       "rev": "08175c62d661fddf052ed10abc91313dec8eb77d",
       "path": "tools/mutate-and-run.sh", "interp": "bash"}

INVOKING = dict(os.environ)
GIT_KEYS = sorted(k for k in INVOKING if k.startswith("GIT_"))


def clean_env(extra=None):
    e = {"PATH": INVOKING["PATH"], "HOME": "/tmp/w/home", "TMPDIR": "/tmp/w/tmp",
         "LANG": "C", "LC_ALL": "C", "TZ": "UTC"}
    if extra:
        e.update(extra)
    return e


PROFILES = [
    ("host", {k: v for k, v in INVOKING.items() if not k.startswith("GIT_")}),
    ("clean", clean_env()),
    ("clean_repeat", clean_env()),
    ("tz", clean_env({"TZ": "Pacific/Chatham"})),
    ("locale", clean_env({"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"})),
    ("home", clean_env({"HOME": "/nonexistent"})),
    ("columns", clean_env({"COLUMNS": "20", "LINES": "5", "TERM": "dumb"})),
]


def run_profile(name, env):
    r = tempfile.mkdtemp(prefix=f"R-{name}-", dir=SCRATCH)
    os.chmod(r, 0o755)
    os.mkdir(os.path.join(r, "home"))
    os.mkdir(os.path.join(r, "tmp"))
    with open(BLOB_PATH, "rb") as f:
        blob = f.read()
    tgt = os.path.join(r, "target.sh")
    with open(tgt, "wb") as f:
        f.write(blob)
    os.chmod(tgt, 0o755)
    argv = ["bwrap",
            "--ro-bind", "/", "/",
            "--dev", "/dev",
            "--proc", "/proc",
            "--tmpfs", "/tmp",
            "--bind", r, "/tmp/w",
            "--unshare-net",
            "--die-with-parent",
            "--chdir", "/tmp/w",
            "bash", "/tmp/w/target.sh", "--selftest"]
    t0 = time.monotonic()
    p = subprocess.run(argv, env=env, cwd=r, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=300)
    dt = time.monotonic() - t0
    out, err = p.stdout, p.stderr
    with open(f"{RAWDIR}/{name}.stdout", "wb") as f:
        f.write(out)
    with open(f"{RAWDIR}/{name}.stderr", "wb") as f:
        f.write(err)
    text = out.decode("utf-8", "replace")
    m = re.search(r"MUTATE_SELFTEST: (\d+)/(\d+) pass", text)
    v = re.search(r"VERDICT: (\S+)", text)
    return {
        "profile": name,
        "exit": p.returncode,
        "stdout_sha256": hashlib.sha256(out).hexdigest(),
        "stderr_sha256": hashlib.sha256(err).hexdigest(),
        "stdout_bytes": len(out),
        "stderr_bytes": len(err),
        "seconds": round(dt, 3),
        "mutate_selftest_line": m.group(0) if m else None,
        "verdict_line": v.group(0) if v else None,
        "stdout_tail": text[-1200:],
        "scratch": os.path.basename(r),
    }


def main():
    with open(BLOB_PATH, "rb") as f:
        blob = f.read()
    blob_sha = hashlib.sha256(blob).hexdigest()
    if blob_sha != EXPECTED_BLOB_SHA256:
        sys.exit(f"blob sha mismatch: {blob_sha}")
    os.makedirs(RAWDIR, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=len(PROFILES)) as ex:
        futs = {ex.submit(run_profile, n, e): n for n, e in PROFILES}
        recs = [f.result() for f in futs]
    order = [n for n, _ in PROFILES]
    recs.sort(key=lambda r: order.index(r["profile"]))
    by = {r["profile"]: r for r in recs}

    def tup(r):
        return (r["exit"], r["stdout_sha256"], r["stderr_sha256"])

    clean, rep = by["clean"], by["clean_repeat"]
    clean_passed = (clean["exit"] == 0 and clean["verdict_line"] == "VERDICT: PASS"
                    and clean["mutate_selftest_line"] is not None
                    and clean["mutate_selftest_line"].split()[1] == "96/96")
    if tup(clean) != tup(rep):
        classification, sensitive, repeat_state = "nondeterministic", [], "clean!=clean_repeat"
    else:
        ct = tup(clean)
        diff = sorted(r["profile"] for r in recs
                      if r["profile"] not in ("clean", "clean_repeat") and tup(r) != ct)
        if diff:
            classification, sensitive, repeat_state = "env-sensitive", diff, "clean==clean_repeat"
        else:
            classification, sensitive, repeat_state = "invariant", [], "clean==clean_repeat"

    producer = json.load(open(RECEIPT))
    ps = next(s for s in producer["surfaces"] if s.get("surface") == "tameshi-runner")
    pprof = ps["profiles"]
    per_profile_agree = {}
    for r in recs:
        pp = pprof.get(r["profile"], {})
        per_profile_agree[r["profile"]] = {
            "exit_agree": pp.get("exit") == r["exit"],
            "stdout_sha_agree": pp.get("stdout_sha256") == r["stdout_sha256"],
            "stderr_sha_agree": pp.get("stderr_sha256") == r["stderr_sha256"],
        }

    result = {
        "schema": "tameshi-r21-f5-independent-v1",
        "surface": "tameshi-runner",
        "independent_implementation": True,
        "imports_env_diff_py": False,
        "recipe_source": "c2-contract.json required_profiles + round-21 F5 exact protocol (context)",
        "pin": PIN,
        "blob_sha256": blob_sha,
        "blob_bytes": len(blob),
        "normalization": "none",
        "contract_sha256": hashlib.sha256(open(CONTRACT, "rb").read()).hexdigest(),
        "host_tools": {
            "bash": subprocess.run(["bash", "--version"], capture_output=True,
                                   text=True).stdout.splitlines()[0],
            "node": subprocess.run(["node", "--version"], capture_output=True,
                                   text=True).stdout.strip(),
            "python": platform.python_version(),
            "uname": platform.uname().system + "-" + platform.uname().release,
            "bwrap": subprocess.run(["bwrap", "--version"], capture_output=True,
                                    text=True).stdout.strip(),
        },
        "invoking_git_keys_scrubbed": GIT_KEYS,
        "argv_template": ["bwrap", "--ro-bind / /", "--dev /dev", "--proc /proc",
                          "--tmpfs /tmp", "--bind <R> /tmp/w", "--unshare-net",
                          "--die-with-parent", "--chdir /tmp/w",
                          "bash", "/tmp/w/target.sh", "--selftest"],
        "clean_passed": clean_passed,
        "clean_selftest_line": clean["mutate_selftest_line"],
        "clean_verdict_line": clean["verdict_line"],
        "repeat_state": repeat_state,
        "classification": classification,
        "sensitive_to": sensitive,
        "profiles": {r["profile"]: r for r in recs},
        "producer_comparison": {
            "receipt": ".ufo/evidence/round-21/f5/receipt-final-production.json",
            "producer_classification": ps.get("classification"),
            "producer_sensitive_to": ps.get("sensitive_to"),
            "producer_normalization": ps.get("normalization"),
            "producer_pin_blob_sha256": ps.get("pin", {}).get("blob_sha256"),
            "blob_sha_agree": ps.get("pin", {}).get("blob_sha256") == blob_sha,
            "classification_agree": ps.get("classification") == classification,
            "per_profile_agree": per_profile_agree,
            "all_tuples_agree": all(all(v.values()) for v in per_profile_agree.values()),
        },
    }
    out = f"{SCRATCH}/independent-result.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=True)
    print(json.dumps({k: result[k] for k in
                      ("classification", "sensitive_to", "clean_passed",
                       "clean_selftest_line", "clean_verdict_line", "repeat_state")}, indent=1))
    print("blob_sha256:", blob_sha)
    print("all_tuples_agree:", result["producer_comparison"]["all_tuples_agree"])
    for r in recs:
        print(f"{r['profile']:13s} exit={r['exit']} out={r['stdout_sha256'][:16]}… "
              f"err={r['stderr_sha256'][:16]}… bytes={r['stdout_bytes']}/{r['stderr_bytes']} "
              f"t={r['seconds']}s {r['mutate_selftest_line']}")
    print("RESULT_JSON:", out)


if __name__ == "__main__":
    main()
