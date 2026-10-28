#!/usr/bin/env python3
"""T55W3R07 probe: the nine allocating modes + five lazy modes on the SKILL.md
`## Standing rules` scratch-root claims, at C0 (9cf0146b...). Argv copied from the
frozen round-55 C2 counter (.ufo/evidence/round-55/c2/measure.py) at C0."""
import json, os, re, subprocess, sys

CLONE = sys.argv[1]
UNUSABLE = os.path.join(CLONE, "no-such-tmpdir")
GRAMMAR = re.compile(
    r"^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?: could-not-evaluate: cannot create clone "
    r"scratch under the scratch root: TMPDIR is not a usable directory: '.+' "
    r"\(could-not-evaluate\)$")

# fixture the frozen counter materializes so env-diff --contract is measurable
os.makedirs(os.path.join(CLONE, ".ufo/evidence/round-55/c2"), exist_ok=True)
with open(os.path.join(CLONE, ".ufo/evidence/round-55/c2/fixture-contract.json"), "w") as fh:
    fh.write(json.dumps({"surfaces": [
        {"name": "stable", "repo": ".", "rev": "HEAD",
         "path": ".ufo/evidence/round-12/BaselineControl/fixtures/target.sh",
         "interp": "bash"}]}, indent=1) + "\n")
C = ".ufo/evidence/round-55/c2/fixture-contract.json"

ALLOC = [
    ("repeat-control --selftest", ["python3", "tools/repeat-control.py", "--selftest"]),
    ("registry-check --selftest", ["python3", "tools/registry-check.py", "--selftest"]),
    ("bash-witness-study selftest", ["python3", "tools/bash-witness-study.py", "selftest"]),
    ("pin-disposition --selftest", ["python3", "tools/pin-disposition.py", "--selftest"]),
    ("evidence-disposition --selftest", ["python3", "tools/evidence-disposition.py", "--selftest"]),
    ("context-capture --selftest", ["python3", "tools/context-capture.py", "--selftest"]),
    ("env-diff --selftest", ["python3", "tools/env-diff.py", "--selftest"]),
    ("env-diff --contract", ["python3", "tools/env-diff.py", "--contract", C,
                             "--out", os.path.join(CLONE, "envdiff-out.json"),
                             "--fleet-root", CLONE]),
    ("registry-check --rev", ["python3", "tools/registry-check.py", "--rev", "HEAD"]),
]
LAZY = [
    ("repeat-control --snapshot", ["python3", "tools/repeat-control.py", "--snapshot",
                                   ".ufo/evidence/round-12/ControlGate"]),
    ("bash-witness-study count", ["python3", "tools/bash-witness-study.py", "count"]),
    ("pin-disposition --read", ["python3", "tools/pin-disposition.py", "--manifest",
                                ".ufo/evidence/round-13/pin-manifest.json",
                                "--root", "/home/vgpnk/Projects/shokunin"]),
    ("evidence-disposition --json", ["python3", "tools/evidence-disposition.py", "--root", ".",
                                     "--dispositions", ".ufo/evidence/round-18/dispositions.json",
                                     "--json"]),
    ("context-capture --check", ["python3", "tools/context-capture.py", "--check", "--json"]),
]


def env_for(tmpdir):
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    if tmpdir is None:
        e.pop("TMPDIR", None)
    else:
        e["TMPDIR"] = tmpdir
    return e


def run(argv, tmpdir):
    p = subprocess.run(argv, cwd=CLONE, env=env_for(tmpdir), capture_output=True,
                       text=True, timeout=2400)
    return p.returncode, p.stdout, p.stderr


fails = 0
print("=== allocating arm: TMPDIR=%r (nonexistent) ===" % UNUSABLE)
for name, argv in ALLOC:
    rc, out, err = run(argv, UNUSABLE)
    matched = [l for l in err.splitlines() if GRAMMAR.match(l)]
    noisy = [t for t in ("RuntimeError", "Traceback") if t in out or t in err]
    ok = rc == 2 and matched and not noisy
    fails += 0 if ok else 1
    print("MODE %s" % name)
    print("  argv: %s" % " ".join(argv))
    print("  exit: %s" % rc)
    print("  stderr-lines: %d  grammar-match: %s  noisy-tokens: %s"
          % (len(err.splitlines()), bool(matched), noisy or "none"))
    print("  stderr: %s" % (err.splitlines()[0] if err.splitlines() else "<empty>"))
    print("  VERDICT %s" % ("OK" if ok else "FAIL"))

print("\n=== lazy arm: TMPDIR=%r (nonexistent) ===" % UNUSABLE)
for name, argv in LAZY:
    rc, out, err = run(argv, UNUSABLE)
    ok = rc == 0
    fails += 0 if ok else 1
    print("MODE %s\n  argv: %s\n  exit: %s (expected 0)\n  VERDICT %s"
          % (name, " ".join(argv), rc, "OK" if ok else "FAIL"))

print("\n=== empty arm: TMPDIR='' (declared unset) ===")
for name, argv in [ALLOC[0], ALLOC[6], LAZY[1]]:
    rc, out, err = run(argv, "")
    print("MODE %s\n  exit: %s (expected 0)\n  stderr-first: %s"
          % (name, rc, (err.splitlines() or ["<empty>"])[0]))

print("\nTOTAL FAILS %d" % fails)
sys.exit(0 if fails == 0 else 1)
