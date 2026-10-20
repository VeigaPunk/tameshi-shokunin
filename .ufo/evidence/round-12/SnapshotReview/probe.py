#!/usr/bin/env python3
# SnapshotReview probe (scratch, /tmp only). Sketch verifiers vs frozen-snapshot
# counterexamples. NOT the repeat-control gate: tools/repeat-control.py is absent
# at HEAD 18ad5d0. Stdlib only.
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PIN = "expected.json"
BAD = "snapshot_tampered"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_pin(root, inputs):
    body = {
        "schema": "snapshot-probe-v0",
        "argv": ["bash", "child.sh"],
        "inputs": inputs,
        "expected": {"finding": "controls_match", "exit": 0},
    }
    (root / PIN).write_text(json.dumps(body, indent=1, sort_keys=True) + "\n")


def make(root, child_body="cat data.txt\nexit 0\n"):
    root.mkdir(parents=True)
    (root / "child.sh").write_text(child_body)
    (root / "data.txt").write_text("ok\n")
    write_pin(root, {"child.sh": sha(root / "child.sh"), "data.txt": sha(root / "data.txt")})
    return root


def naive(root):
    """Digest-only: checks listed files, ignores unlisted files, pin authenticity, dup keys (last-wins)."""
    m = json.loads((root / PIN).read_text())
    for name, want in m["inputs"].items():
        try:
            if sha(root / name) != want:
                return BAD
        except OSError:
            return BAD
    return "pass"


def _no_dups(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key")
    return dict(pairs)


def strict(root):
    try:
        m = json.loads((root / PIN).read_text(), object_pairs_hook=_no_dups)
    except (ValueError, OSError):
        return BAD
    inputs = m.get("inputs") if isinstance(m, dict) else None
    if not isinstance(inputs, dict) or not inputs:
        return BAD
    present = {p.name for p in root.iterdir() if p.name != PIN}
    if present != set(inputs):
        return BAD
    for name, want in inputs.items():
        p = root / name
        if p.is_symlink() or not p.is_file():
            return BAD
        if not (isinstance(want, str) and len(want) == 64 and set(want) <= set("0123456789abcdef")):
            return BAD
        if sha(p) != want:
            return BAD
    return "pass"


def run(root):
    return subprocess.run(["bash", "child.sh"], cwd=root, stdin=subprocess.DEVNULL,
                          capture_output=True).returncode


base = Path(tempfile.mkdtemp(prefix="snapreview-"))
print("python", sys.version.split()[0], "| scratch", base)
rows = []

# A pristine frozen snapshot
r = make(base / "A")
rows.append(("A pristine", naive(r), strict(r), "-", "frozen match baseline"))

# B one-byte edit to a listed input
r = make(base / "B")
(r / "data.txt").write_text("ok!\n")
rows.append(("B edit listed input", naive(r), strict(r), "-", "both detect"))

# C unlisted file added to the snapshot dir
r = make(base / "C")
(r / "extra.txt").write_text("x\n")
rows.append(("C unlisted file added", naive(r), strict(r), "-", "digest-only is blind to additions"))

# D listed input deleted
r = make(base / "D")
(r / "data.txt").unlink()
rows.append(("D listed input deleted", naive(r), strict(r), "-", "naive reaches BAD only via OSError"))

# E input AND its pin rewritten together (self-consistent edit)
r = make(base / "E")
pin_before = sha(r / PIN)
(r / "data.txt").write_text("ok!\n")
write_pin(r, {"child.sh": sha(r / "child.sh"), "data.txt": sha(r / "data.txt")})
anchor = "match" if sha(r / PIN) == pin_before else "MISMATCH"
rows.append(("E input+pin rewritten", naive(r), strict(r), anchor,
             "digest-only passes; only an external anchor on expected.json detects"))

# F duplicate "inputs" key: first-wins reader sees the good pin, last-wins accepts the edit
r = base / "F"
r.mkdir()
(r / "child.sh").write_text("cat data.txt\nexit 0\n")
good = "ok\n"
(r / "data.txt").write_text(good)
c_sha = sha(r / "child.sh")
good_sha = hashlib.sha256(good.encode()).hexdigest()
(r / "data.txt").write_text("ok!\n")
new_sha = sha(r / "data.txt")
dup = ('{"schema":"snapshot-probe-v0","argv":["bash","child.sh"],'
       '"inputs":{"child.sh":"' + c_sha + '","data.txt":"' + good_sha + '"},'
       '"inputs":{"child.sh":"' + c_sha + '","data.txt":"' + new_sha + '"},'
       '"expected":{"finding":"controls_match","exit":0}}')
(r / PIN).write_text(dup)
first_wins_view = "first-pin=good -> BAD" if good_sha != new_sha else "n/a"
rows.append(("F duplicate inputs key", naive(r), strict(r), first_wins_view,
             "parsers disagree on the pin; strict must refuse duplicates"))

# G empty inputs (vacuous pass)
r = base / "G"
r.mkdir()
write_pin(r, {})
rows.append(("G empty inputs", naive(r), strict(r), "-", "zero inputs must not verify"))

# H edit during the runs: pre-run check passes, post-run check must fail
r = make(base / "H", child_body="printf x >> data.txt\nexit 0\n")
pre_naive, pre_strict = naive(r), strict(r)
before = sha(r / "data.txt")
rc = run(r)
after = sha(r / "data.txt")
post_strict = strict(r)
rows.append(("H pre-run check", pre_naive, pre_strict, f"child rc={rc}",
             "clean before runs"))
rows.append(("H post-run recheck", "not performed", post_strict,
             f"data sha {'changed' if before != after else 'unchanged'}",
             "drift during runs must be snapshot_tampered, not controls_match"))

print()
print("| case | digest-only | strict sketch | anchor/aux | note |")
print("|---|---|---|---|---|")
for label, n, s, aux, note in rows:
    print(f"| {label} | {n} | {s} | {aux} | {note} |")
