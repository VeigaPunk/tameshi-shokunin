#!/usr/bin/env python3
"""round-20 receipt-window validity gate (QUALITY20/21, routed defect 1).

A receipt is admissible only when it names a nonempty unique id, a lowercase
64-hex instrument sha256, and an aware ISO-8601 measurement_interval with
start <= end. The instrument sha must be one of the contract's frozen or
installed instrument shas, or a classified historical instrument sha. When an
instrument's frozen and installed shas differ, a receipt measured with the
frozen bytes must end at or before the edit window starts, and a receipt
measured with the installed bytes must start at or after the edit window ends.

Exit: 0 clean, 1 findings, 2 could-not-evaluate, 64 usage.
This file is staged evidence. It is frozen by contract.json before any wave
dispatch and is not edited in place during the round (QUALITY20)."""

import argparse
import json
import re
import sys
from datetime import datetime

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
EXIT_CLEAN, EXIT_FAIL, EXIT_CE, EXIT_USAGE = 0, 1, 2, 64


class ContractError(Exception):
    pass


class ReceiptsError(Exception):
    pass


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
    if dt.tzinfo is None:
        return None
    return dt


def require_interval(obj, where):
    if not isinstance(obj, dict):
        raise ValueError(f"{where}: measurement_interval must be an object")
    start = parse_ts(obj.get("start"))
    end = parse_ts(obj.get("end"))
    if start is None or end is None:
        raise ValueError(f"{where}: measurement_interval start/end must be aware ISO-8601")
    if start > end:
        raise ValueError(f"{where}: measurement_interval start is after end")
    return start, end


def load_contract(path):
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except Exception as exc:  # noqa: BLE001 - fail closed with a stable kind
        raise ContractError(f"cannot read contract: {exc}") from exc
    if not isinstance(doc, dict):
        raise ContractError("contract must be an object")
    instruments = doc.get("instruments")
    historical = doc.get("historical", {})
    if not isinstance(instruments, dict) or not instruments:
        raise ContractError("contract.instruments must be a nonempty object")
    if not isinstance(historical, dict):
        raise ContractError("contract.historical must be an object")
    index = {}
    windows = {}
    for name, entry in instruments.items():
        if not isinstance(name, str) or not name:
            raise ContractError("instrument name must be a nonempty string")
        if not isinstance(entry, dict):
            raise ContractError(f"instrument {name} must be an object")
        frozen = entry.get("frozen_sha256")
        installed = entry.get("installed_sha256")
        for label, sha in (("frozen_sha256", frozen), ("installed_sha256", installed)):
            if not isinstance(sha, str) or not SHA_RE.match(sha):
                raise ContractError(f"instrument {name}.{label} is not a lowercase 64-hex sha256")
        window = None
        if frozen != installed:
            window = entry.get("edit_interval")
            if not isinstance(window, dict):
                raise ContractError(f"instrument {name} differs frozen/installed and needs edit_interval")
            try:
                start, end = require_interval(window, f"instrument {name}.edit_interval")
            except ValueError as exc:
                raise ContractError(str(exc)) from exc
            if start >= end:
                raise ContractError(f"instrument {name}.edit_interval must be a positive window")
            windows[name] = (start, end)
        elif "edit_interval" in entry:
            try:
                require_interval(entry["edit_interval"], f"instrument {name}.edit_interval")
            except ValueError as exc:
                raise ContractError(str(exc)) from exc
        for role, sha in (("frozen", frozen), ("installed", installed)):
            prior = index.get(sha)
            if prior is not None and prior[0] != name:
                raise ContractError(f"sha {sha} is claimed by both {prior[0]} and {name}")
            if prior is None:
                index[sha] = (name, role if frozen != installed else "identity")
            elif prior[1] == "identity" or role == "identity":
                index[sha] = (name, "identity")
    for sha, label in historical.items():
        if not isinstance(sha, str) or not SHA_RE.match(sha):
            raise ContractError("historical key is not a lowercase 64-hex sha256")
        if not isinstance(label, str) or not label.strip():
            raise ContractError("historical label must be a nonempty string")
        if sha in index:
            raise ContractError(f"historical sha {sha} is also a current instrument sha")
    return {"instruments": instruments, "index": index, "windows": windows,
            "historical": historical, "round": doc.get("round")}


def load_receipts(path):
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except Exception as exc:  # noqa: BLE001
        raise ReceiptsError(f"cannot read receipts: {exc}") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("receipts"), list):
        raise ReceiptsError("receipts must be an object with a receipts array")
    return doc


def check(contract, receipts_doc):
    findings = []
    infos = []
    seen = set()
    receipts = receipts_doc["receipts"]
    if not receipts:
        findings.append({"id": "NO_RECEIPTS", "receipt": None, "detail": "receipts array is empty"})
    for pos, receipt in enumerate(receipts):
        rid = receipt.get("id") if isinstance(receipt, dict) else None
        where = f"receipts[{pos}]"
        if not isinstance(receipt, dict):
            findings.append({"id": "RECEIPT_MISSING_FIELD", "receipt": where, "detail": "receipt is not an object"})
            continue
        if not isinstance(rid, str) or not rid.strip():
            findings.append({"id": "RECEIPT_MISSING_FIELD", "receipt": where, "detail": "id must be a nonempty string"})
            continue
        if rid in seen:
            findings.append({"id": "DUPLICATE_RECEIPT_ID", "receipt": rid, "detail": "receipt id repeats"})
            continue
        seen.add(rid)
        sha = receipt.get("instrument_sha256")
        if not isinstance(sha, str) or not SHA_RE.match(sha):
            findings.append({"id": "RECEIPT_MISSING_FIELD", "receipt": rid,
                             "detail": "instrument_sha256 must be a lowercase 64-hex sha256"})
            continue
        try:
            start, end = require_interval(receipt.get("measurement_interval"), rid)
        except ValueError as exc:
            findings.append({"id": "BAD_INTERVAL", "receipt": rid, "detail": str(exc)})
            continue
        declared = receipt.get("instrument")
        if declared is not None:
            if not isinstance(declared, str) or declared not in contract["instruments"]:
                findings.append({"id": "UNKNOWN_INSTRUMENT", "receipt": rid,
                                 "detail": f"declared instrument {declared!r} is not in the contract"})
                continue
            entry = contract["instruments"][declared]
            if sha not in (entry.get("frozen_sha256"), entry.get("installed_sha256")):
                findings.append({"id": "UNKNOWN_INSTRUMENT", "receipt": rid,
                                 "detail": f"sha does not match declared instrument {declared}"})
                continue
        if sha in contract["historical"]:
            label = contract["historical"][sha]
            infos.append({"id": "HISTORICAL_INSTRUMENT", "receipt": rid,
                          "detail": f"classified {label}"})
            continue
        if sha not in contract["index"]:
            findings.append({"id": "UNKNOWN_INSTRUMENT", "receipt": rid,
                             "detail": "instrument_sha256 is neither frozen, installed, nor historical"})
            continue
        name, role = contract["index"][sha]
        if role == "identity" or name not in contract["windows"]:
            infos.append({"id": "INSTALL_IDENTITY", "receipt": rid,
                          "detail": f"{name}: frozen and installed bytes are identical"})
            continue
        edit_start, edit_end = contract["windows"][name]
        if role == "frozen" and end > edit_start:
            findings.append({"id": "FROZEN_AFTER_EDIT", "receipt": rid,
                             "detail": f"{name}: frozen-sha measurement ends after edit window starts"})
        elif role == "installed" and start < edit_end:
            findings.append({"id": "INSTALLED_BEFORE_INSTALL", "receipt": rid,
                             "detail": f"{name}: installed-sha measurement starts before install ends"})
        else:
            infos.append({"id": "WINDOW_OK", "receipt": rid, "detail": f"{name}: {role} window respected"})
    findings.sort(key=lambda f: (f["receipt"] or "", f["id"], f["detail"]))
    infos.sort(key=lambda f: (f["receipt"] or "", f["id"], f["detail"]))
    return findings, infos


def run(contract_path, receipts_path, want_json):
    try:
        contract = load_contract(contract_path)
    except ContractError as exc:
        return emit_ce("CONTRACT_INVALID", str(exc), want_json)
    try:
        receipts = load_receipts(receipts_path)
    except ReceiptsError as exc:
        return emit_ce("RECEIPTS_INVALID", str(exc), want_json)
    findings, infos = check(contract, receipts)
    if findings:
        if want_json:
            print(json.dumps({"schema": "tameshi-receipt-window-v1", "verdict": "FAIL",
                              "findings": findings, "infos": infos,
                              "receipts": len(receipts["receipts"])}, sort_keys=True))
        else:
            print(f"RECEIPT_WINDOW: FAIL (findings={len(findings)} receipts={len(receipts['receipts'])})")
            for finding in findings:
                print(f"RECEIPT_WINDOW finding={finding['id']} receipt={finding['receipt']} {finding['detail']}")
        return EXIT_FAIL
    if want_json:
        print(json.dumps({"schema": "tameshi-receipt-window-v1", "verdict": "CLEAN",
                          "findings": [], "infos": infos,
                          "receipts": len(receipts["receipts"])}, sort_keys=True))
    else:
        hist = sum(1 for i in infos if i["id"] == "HISTORICAL_INSTRUMENT")
        print(f"RECEIPT_WINDOW: CLEAN (receipts={len(receipts['receipts'])} historical={hist})")
        for info in infos:
            print(f"RECEIPT_WINDOW info={info['id']} receipt={info['receipt']} {info['detail']}")
    return EXIT_CLEAN


def emit_ce(kind, detail, want_json):
    if want_json:
        print(json.dumps({"schema": "tameshi-receipt-window-v1", "verdict": "COULD_NOT_EVALUATE",
                          "kind": kind, "detail": detail}, sort_keys=True))
    else:
        print(f"RECEIPT_WINDOW: COULD_NOT_EVALUATE ({kind}: {detail})")
    return EXIT_CE


def selftest():
    f, i = "a" * 64, "b" * 64
    e = "e" * 64
    h1, h2 = "c" * 64, "d" * 64
    contract = {
        "round": 20,
        "instruments": {
            "gate": {"frozen_sha256": f, "installed_sha256": i,
                     "edit_interval": {"start": "2026-10-21T10:00:00Z", "end": "2026-10-21T11:00:00Z"}},
            "measure": {"frozen_sha256": e, "installed_sha256": e},
        },
        "historical": {h1: "round19-ruler-wave1", h2: "witness-tool"},
    }
    # Build the contract index without the filesystem.
    index, windows = {}, {}
    for name, entry in contract["instruments"].items():
        frozen, installed = entry["frozen_sha256"], entry["installed_sha256"]
        role = "identity" if frozen == installed else None
        for sha, r in ((frozen, "frozen"), (installed, "installed")):
            if sha not in index:
                index[sha] = (name, role or r)
            elif role or r == "identity":
                index[sha] = (name, "identity")
        if frozen != installed:
            st = parse_ts(entry["edit_interval"]["start"])
            en = parse_ts(entry["edit_interval"]["end"])
            windows[name] = (st, en)
    frozen_contract = {"instruments": contract["instruments"], "index": index,
                       "windows": windows, "historical": contract["historical"], "round": 20}

    def r(rid, sha, start="2026-10-21T09:00:00Z", end="2026-10-21T09:30:00Z", **extra):
        row = {"id": rid, "instrument_sha256": sha,
               "measurement_interval": {"start": start, "end": end}}
        row.update(extra)
        return row

    def ok(rid, sha, start="2026-10-21T09:00:00Z", end="2026-10-21T09:30:00Z", **extra):
        return ({"receipts": [r(rid, sha, start, end, **extra)]}, "CLEAN", None)

    def bad(rid, sha, kind, start="2026-10-21T09:00:00Z", end="2026-10-21T09:30:00Z", **extra):
        return ({"receipts": [r(rid, sha, start, end, **extra)]}, "FAIL", kind)

    cases = [
        ("frozen receipt before the edit window is clean", ok("c1", f)),
        ("installed receipt after the edit window is clean",
         ok("c2", i, "2026-10-21T11:00:00Z", "2026-10-21T11:30:00Z")),
        ("missing instrument sha is refused", bad("c3", "", "RECEIPT_MISSING_FIELD")),
        ("unknown sha is refused", bad("c4", "9" * 64, "UNKNOWN_INSTRUMENT")),
        ("missing interval is refused", ({"receipts": [{"id": "c5", "instrument_sha256": f}]}, "FAIL", "BAD_INTERVAL")),
        ("reversed interval is refused", bad("c6", f, "BAD_INTERVAL", "2026-10-21T09:30:00Z", "2026-10-21T09:00:00Z")),
        ("naive timestamp is refused", bad("c7", f, "BAD_INTERVAL", "2026-10-21T09:00:00", "2026-10-21T09:30:00")),
        ("frozen sha after the edit starts is refused",
         bad("c8", f, "FROZEN_AFTER_EDIT", "2026-10-21T09:00:00Z", "2026-10-21T10:30:00Z")),
        ("installed sha before the edit ends is refused",
         bad("c9", i, "INSTALLED_BEFORE_INSTALL", "2026-10-21T10:30:00Z", "2026-10-21T11:30:00Z")),
        ("duplicate id is refused",
         ({"receipts": [r("c10", f), r("c10", i, "2026-10-21T11:00:00Z", "2026-10-21T11:30:00Z")]},
          "FAIL", "DUPLICATE_RECEIPT_ID")),
        ("empty receipts is refused", ({"receipts": []}, "FAIL", "NO_RECEIPTS")),
        ("historical sha is classified, not gated", ok("c12", h1, "2020-01-01T00:00:00Z", "2020-01-01T01:00:00Z")),
        ("second historical sha is classified", ok("c13", h2, "2020-01-01T00:00:00Z", "2020-01-01T01:00:00Z")),
        ("identity instrument accepts a wave-time receipt", ok("c14", e)),
        ("declared instrument mismatch is refused", bad("c15", f, "UNKNOWN_INSTRUMENT", instrument="measure")),
        ("multi-receipt one-bad row fails the file",
         ({"receipts": [r("ok", f), r("bad", "9" * 64)]}, "FAIL", "UNKNOWN_INSTRUMENT")),
        ("frozen-sha receipt ending exactly at edit start is clean",
         ok("c17", f, "2026-10-21T09:00:00Z", "2026-10-21T10:00:00Z")),
        ("installed-sha receipt starting exactly at edit end is clean",
         ok("c18", i, "2026-10-21T11:00:00Z", "2026-10-21T11:30:00Z")),
    ]
    passed = 0
    for pos, (label, (doc, want, kind)) in enumerate(cases, 1):
        findings, infos = check(frozen_contract, doc)
        got = "FAIL" if findings else "CLEAN"
        kinds = {x["id"] for x in findings}
        good = got == want and (kind is None or kind in kinds)
        if good:
            passed += 1
            print(f"PASS [{pos:2d}/{len(cases)}] {label} — {got}")
        else:
            print(f"FAIL [{pos:2d}/{len(cases)}] {label} — want {want}/{kind} got {got}/{sorted(kinds)}")
    # Contract validation cases exercise the file loader.
    import tempfile, os
    with tempfile.TemporaryDirectory(prefix="tameshi-r20-rw-selftest.") as tmp:
        bad_contract = os.path.join(tmp, "bad-contract.json")
        with open(bad_contract, "w", encoding="utf-8") as fh:
            fh.write("{not json")
        try:
            load_contract(bad_contract)
            print(f"FAIL [{len(cases) + 1:2d}/{len(cases) + 2}] malformed contract is refused — accepted")
        except ContractError:
            passed += 1
            print(f"PASS [{len(cases) + 1:2d}/{len(cases) + 2}] malformed contract is refused — CONTRACT_INVALID")
        bad_receipts = os.path.join(tmp, "bad-receipts.json")
        with open(bad_receipts, "w", encoding="utf-8") as fh:
            fh.write('{"receipts": 5}')
        try:
            load_receipts(bad_receipts)
            print(f"FAIL [{len(cases) + 2:2d}/{len(cases) + 2}] malformed receipts is refused — accepted")
        except ReceiptsError:
            passed += 1
            print(f"PASS [{len(cases) + 2:2d}/{len(cases) + 2}] malformed receipts is refused — RECEIPTS_INVALID")
    total = len(cases) + 2
    print(f"RECEIPT_WINDOW_SELFTEST: {passed}/{total} pass")
    return EXIT_CLEAN if passed == total else EXIT_FAIL


def main(argv=None):
    parser = argparse.ArgumentParser(description="round-20 receipt-window validity gate")
    parser.add_argument("--contract")
    parser.add_argument("--receipts")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.contract or not args.receipts:
        parser.print_usage(sys.stderr)
        return EXIT_USAGE
    return run(args.contract, args.receipts, args.json)


if __name__ == "__main__":
    sys.exit(main())
