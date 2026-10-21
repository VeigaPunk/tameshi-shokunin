#!/usr/bin/env python3
"""round-20 C1 calibration ruler: six receipt-window population items.

Counts, at one revision, whether the round closed the QUALITY20 recurrence:
frozen-before-dispatch contract, frozen staged instruments, installed gate,
clean selftest receipt, checker-clean final receipts, and the four historical
instrument identities classified. It re-executes the installed receipt-window
gate over committed bytes; it does not trust a prose pass.

Usage: measure.py --repo LANE [--rev REV] [--json] [--explain]
Exit: 0 corrected==total, 1 otherwise, 2 could-not-evaluate.
This file is staged evidence frozen by contract.json before dispatch."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime

TOTAL = 6
EXPECT_HIST = {
    "96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef": "round19-ruler-wave1",
    "8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12": "witness-tool",
    "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b": "witness-runner",
    "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37": "round18-measure",
}
CONTRACT = ".ufo/evidence/round-20/contract.json"
DISPATCH = ".ufo/waves/round-20/dispatch.json"
STAGE_GATE = ".ufo/evidence/round-20/stage/receipt-window.py"
STAGE_MEASURE = ".ufo/evidence/round-20/stage/measure.py"
INSTALLED = "tools/receipt-window.py"
FINAL_RECEIPTS = ".ufo/evidence/round-20/final/receipts.json"
HIST_RECEIPTS = ".ufo/evidence/round-20/final/historical-receipts.json"
SELFTEST_RECEIPT = ".ufo/evidence/round-20/final/receipt-window-selftest.json"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def blob(repo, rev, path):
    proc = git(repo, "show", f"{rev}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def parse_ts(value):
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    return dt if dt.tzinfo is not None else None


def commit_time(repo, rev, path):
    proc = git(repo, "log", "-1", "--format=%cI", rev, "--", path)
    if proc.returncode != 0:
        return None
    return parse_ts(proc.stdout.decode("utf-8", "replace"))


def load_json_bytes(data):
    try:
        return json.loads(data.decode("utf-8"))
    except Exception:  # noqa: BLE001
        return None


def run_checker(checker_bytes, contract_bytes, receipts_bytes):
    with tempfile.TemporaryDirectory(prefix="tameshi-r20-measure.") as tmp:
        gate = os.path.join(tmp, "receipt-window.py")
        contract = os.path.join(tmp, "contract.json")
        receipts = os.path.join(tmp, "receipts.json")
        with open(gate, "wb") as fh:
            fh.write(checker_bytes)
        with open(contract, "wb") as fh:
            fh.write(contract_bytes)
        with open(receipts, "wb") as fh:
            fh.write(receipts_bytes)
        return subprocess.run([sys.executable, gate, "--contract", contract, "--receipts", receipts],
                              capture_output=True, text=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="round-20 C1 receipt-window measure")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--rev", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--explain", action="store_true")
    args = parser.parse_args(argv)
    repo = args.repo
    rev = args.rev or git(repo, "rev-parse", "master").stdout.decode().strip()
    if not rev:
        print("MEASURE: COULD_NOT_EVALUATE (no revision)")
        return 2

    contract_bytes = blob(repo, rev, CONTRACT)
    contract = load_json_bytes(contract_bytes) if contract_bytes else None
    dispatch_bytes = blob(repo, rev, DISPATCH)
    dispatch = load_json_bytes(dispatch_bytes) if dispatch_bytes else None
    stage_gate = blob(repo, rev, STAGE_GATE)
    stage_measure = blob(repo, rev, STAGE_MEASURE)
    installed = blob(repo, rev, INSTALLED)
    final_receipts = blob(repo, rev, FINAL_RECEIPTS)
    hist_receipts = blob(repo, rev, HIST_RECEIPTS)
    selftest_receipt = blob(repo, rev, SELFTEST_RECEIPT)

    items = []

    def add(item, ok, detail):
        items.append({"id": item, "status": "PASS" if ok else "FAIL", "detail": detail})

    # 1. Contract frozen before dispatch.
    ok = False
    detail = "contract/dispatch/freeze ordering"
    if contract is None:
        detail = "contract.json absent at revision"
    elif not isinstance(contract, dict):
        detail = "contract.json is not an object"
    elif dispatch is None or not isinstance(dispatch, dict):
        detail = "wave-1 dispatch artifact absent at revision"
    else:
        frozen_at = parse_ts(contract.get("frozen_at"))
        dispatched_at = parse_ts(dispatch.get("wave1_dispatched_at"))
        ctime = commit_time(repo, rev, CONTRACT)
        if frozen_at is None:
            detail = "contract.frozen_at is not an aware ISO timestamp"
        elif dispatched_at is None:
            detail = "dispatch.wave1_dispatched_at is not an aware ISO timestamp"
        elif ctime is None:
            detail = "contract has no reachable commit time"
        elif frozen_at <= ctime <= dispatched_at:
            ok = True
            detail = f"frozen_at={contract['frozen_at']} <= commit={ctime.isoformat()} <= dispatch={dispatch['wave1_dispatched_at']}"
        else:
            detail = f"ordering violated frozen={frozen_at.isoformat()} commit={ctime.isoformat()} dispatch={dispatched_at.isoformat()}"
    add("contract_frozen_before_dispatch", ok, detail)

    # 2. Staged instruments match their frozen shas.
    ok = False
    detail = "staged instrument shas"
    if contract is None or stage_gate is None or stage_measure is None:
        detail = "contract or staged instruments absent at revision"
    else:
        try:
            inst = contract["instruments"]
            gate_frozen = inst["receipt-window"]["frozen_sha256"]
            measure_frozen = inst["round20-measure"]["frozen_sha256"]
            gate_sha, measure_sha = sha256(stage_gate), sha256(stage_measure)
            if gate_sha == gate_frozen and measure_sha == measure_frozen:
                ok = True
                detail = f"receipt-window={gate_sha} round20-measure={measure_sha}"
            else:
                detail = f"staged sha mismatch gate={gate_sha}/{gate_frozen} measure={measure_sha}/{measure_frozen}"
        except (KeyError, TypeError) as exc:
            detail = f"contract instruments malformed: {exc}"
    add("staged_instruments_frozen", ok, detail)

    # 3. Installed gate matches its installed sha.
    ok = False
    detail = "installed gate sha"
    if contract is None or installed is None:
        detail = "contract or installed gate absent at revision"
    else:
        try:
            want = contract["instruments"]["receipt-window"]["installed_sha256"]
            got = sha256(installed)
            ok = got == want
            detail = f"installed={got} contract={want}"
        except (KeyError, TypeError) as exc:
            detail = f"contract instruments malformed: {exc}"
    add("installed_matches_contract", ok, detail)

    # 4. Selftest receipt clean.
    ok = False
    detail = "gate selftest receipt"
    if selftest_receipt is None:
        detail = "selftest receipt absent at revision"
    else:
        doc = load_json_bytes(selftest_receipt)
        if not isinstance(doc, dict):
            detail = "selftest receipt is not JSON"
        else:
            stdout = str(doc.get("stdout", ""))
            match = re.search(r"RECEIPT_WINDOW_SELFTEST: (\d+)/(\d+) pass", stdout)
            tally = int(match.group(1)) if match else 0
            total = int(match.group(2)) if match else 0
            if doc.get("exit") == 0 and match and total >= 20 and tally == total:
                ok = True
                detail = f"exit=0 {tally}/{total}"
            else:
                detail = f"exit={doc.get('exit')} tally={tally}/{total}"
    add("selftest_receipt_clean", ok, detail)

    # 5. Final receipts are checker-clean.
    ok = False
    detail = "final receipts checker run"
    if contract_bytes is None or installed is None or final_receipts is None:
        detail = "contract, installed gate, or final receipts absent at revision"
    else:
        run = run_checker(installed, contract_bytes, final_receipts)
        ok = run.returncode == 0
        detail = f"checker exit={run.returncode} {run.stdout.strip().splitlines()[-1] if run.stdout.strip() else run.stderr.strip()[:120]}"
    add("final_receipts_clean", ok, detail)

    # 6. Historical instrument identities classified.
    ok = False
    detail = "historical instrument classification"
    if contract is None or installed is None or hist_receipts is None:
        detail = "contract, installed gate, or historical receipts absent at revision"
    else:
        try:
            historical = contract.get("historical", {})
            missing = [sha for sha, label in EXPECT_HIST.items() if historical.get(sha) != label]
            run = run_checker(installed, contract_bytes, hist_receipts)
            labels_ok = all(label in run.stdout for label in EXPECT_HIST.values())
            if not missing and run.returncode == 0 and labels_ok:
                ok = True
                detail = "4/4 identities classified: " + ", ".join(sorted(EXPECT_HIST.values()))
            else:
                detail = f"missing={missing} checker_exit={run.returncode} labels_ok={labels_ok}"
        except Exception as exc:  # noqa: BLE001
            detail = f"classification check failed: {exc}"
    add("historical_classified", ok, detail)

    corrected = sum(1 for item in items if item["status"] == "PASS")
    result = {
        "schema": "tameshi-round20-receipt-window-measure-v1",
        "revision": rev,
        "total": TOTAL,
        "corrected": corrected,
        "open": TOTAL - corrected,
        "items": items,
        "inputs": {
            CONTRACT: sha256(contract_bytes) if contract_bytes else None,
            DISPATCH: sha256(dispatch_bytes) if dispatch_bytes else None,
            STAGE_GATE: sha256(stage_gate) if stage_gate else None,
            STAGE_MEASURE: sha256(stage_measure) if stage_measure else None,
            INSTALLED: sha256(installed) if installed else None,
            FINAL_RECEIPTS: sha256(final_receipts) if final_receipts else None,
            HIST_RECEIPTS: sha256(hist_receipts) if hist_receipts else None,
            SELFTEST_RECEIPT: sha256(selftest_receipt) if selftest_receipt else None,
        },
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"MEASURE revision={rev}")
        for item in items:
            print(f"ITEM {item['id']} {item['status']} {item['detail']}")
        print(f"C1_RECEIPTS: corrected={corrected} open={TOTAL - corrected} total={TOTAL}")
    return 0 if corrected == TOTAL else 1


if __name__ == "__main__":
    sys.exit(main())
