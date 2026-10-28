#!/usr/bin/env python3
"""Build the round-55 lab-mode workloads (all under scratch, none in the lane)."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

S = Path(sys.argv[1])
CLONE = Path(sys.argv[2])
WORK = S / "work"
WORK.mkdir(parents=True, exist_ok=True)

hexish = lambda digest: ("0" if digest[0] != "0" else "1") + digest[1:]

# L1: a pin manifest whose pins mismatch (five changed, one pinned commit missing).
man = json.loads((CLONE / ".ufo/evidence/round-13/pin-manifest.json").read_text())
for leg in man["legs"]:
    leg["expected_sha256"] = hexish(leg["expected_sha256"])
man["legs"][-1]["pinned_commit"] = "0" * 40
(WORK / "pin-manifest-mismatch.json").write_text(json.dumps(man, indent=1) + "\n")

# L2: a receipt/expected pair that mismatches (clean receipt recomputes exit 0,
# the pin says exit 1 -> expected_verdict_mismatch exit 1).
receipt = CLONE / ".ufo/evidence/round-14/context-receipt.json"
sha = hashlib.sha256(receipt.read_bytes()).hexdigest()
expected = {"schema": "tameshi-context-expected-v1", "receipt_sha256": sha,
            "id": "context_consistent", "exit": 1}
(WORK / "context-expected-exit1.json").write_text(json.dumps(expected, indent=1) + "\n")
tampered = dict(expected, receipt_sha256="f" * 64, id="snapshot_tampered", exit=2)
(WORK / "context-expected-tampered.json").write_text(json.dumps(tampered, indent=1) + "\n")

# L4: a failing disposition set.  The dispositions document itself is not pinned
# (only its inputs are), so pointing a row at a pinned receipt that lacks the
# check keeps every pin intact and turns the replay into a genuine failure.
dis = json.loads((CLONE / ".ufo/evidence/round-18/dispositions.json").read_text())
for row in dis["rows"]:
    if row["name"] == "pin_selftest":
        row["receipt"] = ".ufo/evidence/round-13/producer-oracle-repair.json"
(WORK / "dispositions-fail.json").write_text(json.dumps(dis, indent=1) + "\n")

# L4b: a self-contained v1 lane whose pins all verify and whose single row
# genuinely fails (the receipt observed exit 1; expected says exit 0).
ed = WORK / "ed-lane"
if ed.exists():
    shutil.rmtree(ed)
eddir = ed / ".ufo" / "evidence" / "x"
eddir.mkdir(parents=True)
fixture = b"pinned-input\n"
(eddir / "fixture.txt").write_bytes(fixture)
verification = {
    "schema": "round55-lab-receipt",
    "checks": [{"name": "alpha", "argv": ["true"], "exit": 1,
                "stdout": "NO_ALPHA\n", "stderr": ""}],
}
(eddir / "verification.json").write_text(json.dumps(verification, indent=1) + "\n")
(eddir / "producer-oracle-repair.json").write_text(
    json.dumps({"schema": "round55-lab-oracle", "checks": []}, indent=1) + "\n")
expected_ed = {
    "schema": "tameshi-round13-evidence-v1",
    "inputs": {".ufo/evidence/x/fixture.txt": hashlib.sha256(fixture).hexdigest()},
    "expected_checks": {"alpha": {"exit": 0, "contains": "ALPHA_OK"}},
}
(eddir / "expected.json").write_text(json.dumps(expected_ed, indent=1) + "\n")
pins = {rel: hashlib.sha256((ed / rel).read_bytes()).hexdigest() for rel in (
    ".ufo/evidence/x/expected.json",
    ".ufo/evidence/x/verification.json",
    ".ufo/evidence/x/producer-oracle-repair.json",
    ".ufo/evidence/x/fixture.txt",
)}
dis_v1 = {
    "schema": "evidence-dispositions-v1",
    "expected_file": ".ufo/evidence/x/expected.json",
    "inputs": pins,
    "rows": [{"name": "alpha", "state": "effective",
              "receipt": ".ufo/evidence/x/verification.json", "check": "alpha"}],
}
(eddir / "dispositions.json").write_text(json.dumps(dis_v1, indent=1) + "\n")

# L6: a witness-study evidence copy whose stored count disagrees with the raw
# sweep (real re-derivation work, then a deliberate mismatch).
ev = WORK / "bashwitness"
if ev.exists():
    shutil.rmtree(ev)
shutil.copytree(CLONE / ".ufo/evidence/round-12/BashWitness", ev)
summary = json.loads((ev / "summary.json").read_text())
summary["counts"]["killed_on_witness"] += 1
(ev / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")

print("workloads in", WORK)
for p in sorted(WORK.iterdir()):
    print(" ", p.name)
