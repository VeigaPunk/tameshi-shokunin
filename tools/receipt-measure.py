#!/usr/bin/env python3
"""Runner for the frozen round-20 measurement instrument.

Regular CLI arguments are delegated unchanged to the staged measure.py. The
runner's SHA-256 belongs in a receipt's runner_sha256; instrument_sha256 stays
the frozen round20-measure instrument identity. The historical --check spelling
is not accepted or translated; use --json for the published counting command.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEASURE = ROOT / ".ufo/evidence/round-20/stage/measure.py"
STAGE_GATE = ".ufo/evidence/round-20/stage/receipt-window.py"
STAGE_MEASURE = ".ufo/evidence/round-20/stage/measure.py"
CONTRACT = ".ufo/evidence/round-20/contract.json"
DISPATCH = ".ufo/waves/round-20/dispatch.json"
INSTALLED = "tools/receipt-window.py"
FINAL_RECEIPTS = ".ufo/evidence/round-20/final/receipts.json"
HIST_RECEIPTS = ".ufo/evidence/round-20/final/historical-receipts.json"
SELFTEST_RECEIPT = ".ufo/evidence/round-20/final/receipt-window-selftest.json"

FROZEN_GATE_SHA = "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc"
FROZEN_MEASURE_SHA = "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d"
HISTORICAL = {
    "96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef": "round19-ruler-wave1",
    "8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12": "witness-tool",
    "d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b": "witness-runner",
    "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37": "round18-measure",
}
ITEM_IDS = (
    "contract_frozen_before_dispatch",
    "staged_instruments_frozen",
    "installed_matches_contract",
    "selftest_receipt_clean",
    "final_receipts_clean",
    "historical_classified",
)


def clean_env():
    env = os.environ.copy()
    for key in tuple(env):
        if key.startswith("GIT_"):
            del env[key]
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def test_git_env():
    env = clean_env()
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_AUTHOR_DATE"] = "@978307200 +0000"
    env["GIT_COMMITTER_DATE"] = "@978307200 +0000"
    return env


def run_cli(arguments):
    return subprocess.run(
        [sys.executable, "-B", str(Path(__file__).resolve()), *arguments],
        capture_output=True,
        text=True,
        env=clean_env(),
    )


def checked_process(command, *, env, cwd=None):
    process = subprocess.run(
        command, cwd=cwd, env=env, capture_output=True, text=True
    )
    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip()
        raise RuntimeError(f"command failed ({process.returncode}): {detail}")
    return process


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def fixture_files(mutation):
    gate_bytes = (ROOT / STAGE_GATE).read_bytes()
    measure_bytes = (ROOT / STAGE_MEASURE).read_bytes()
    final_interval = {
        "start": "2001-01-01T00:00:00Z",
        "end": "2001-01-01T01:00:00Z",
    }
    historical_interval = {
        "start": "2020-01-01T00:00:00Z",
        "end": "2020-01-01T01:00:00Z",
    }
    contract = {
        "round": 20,
        "frozen_at": "2000-01-01T00:00:00Z",
        "instruments": {
            "receipt-window": {
                "frozen_sha256": FROZEN_GATE_SHA,
                "installed_sha256": FROZEN_GATE_SHA,
            },
            "round20-measure": {
                "frozen_sha256": FROZEN_MEASURE_SHA,
                "installed_sha256": FROZEN_MEASURE_SHA,
            },
        },
        "historical": HISTORICAL,
    }
    final_receipts = {
        "receipts": [
            {
                "id": "final-1",
                "instrument": "receipt-window",
                "instrument_sha256": FROZEN_GATE_SHA,
                "measurement_interval": final_interval,
            }
        ]
    }
    historical_receipts = {
        "receipts": [
            {
                "id": f"historical-{index}",
                "instrument_sha256": sha,
                "measurement_interval": historical_interval,
            }
            for index, sha in enumerate(HISTORICAL, 1)
        ]
    }
    files = {
        CONTRACT: json_bytes(contract),
        DISPATCH: json_bytes({"wave1_dispatched_at": "2002-01-01T00:00:00Z"}),
        STAGE_GATE: gate_bytes,
        STAGE_MEASURE: measure_bytes,
        INSTALLED: gate_bytes,
        FINAL_RECEIPTS: json_bytes(final_receipts),
        HIST_RECEIPTS: json_bytes(historical_receipts),
        SELFTEST_RECEIPT: json_bytes(
            {"exit": 0, "stdout": "RECEIPT_WINDOW_SELFTEST: 20/20 pass\n"}
        ),
    }
    if mutation == "remove-dispatch":
        del files[DISPATCH]
    elif mutation == "mismatch-stage-measure":
        files[STAGE_MEASURE] += b"\n"
    elif mutation == "mismatch-installed-gate":
        files[INSTALLED] += b"\n"
    elif mutation == "remove-selftest-receipt":
        del files[SELFTEST_RECEIPT]
    elif mutation == "remove-final-receipts":
        del files[FINAL_RECEIPTS]
    elif mutation == "remove-historical-receipts":
        del files[HIST_RECEIPTS]
    elif mutation == "malformed-contract":
        files[CONTRACT] = b'{"frozen_at":'
    elif mutation is not None:
        raise ValueError(f"unknown fixture mutation: {mutation}")
    return files


def make_fixture(repo, mutation):
    repo = Path(repo)
    repo.mkdir(parents=True, exist_ok=True)
    for relative, contents in fixture_files(mutation).items():
        destination = repo.joinpath(*relative.split("/"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(contents)
    checked_process(
        ["git", "init", "--quiet", "--initial-branch=master", str(repo)],
        env=test_git_env(),
    )
    checked_process(["git", "-C", str(repo), "add", "--all"], env=test_git_env())
    checked_process(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=receipt-measure selftest",
            "-c",
            "user.email=receipt-measure-selftest@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "isolated receipt-measure fixture",
        ],
        env=test_git_env(),
    )
    revision = checked_process(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], env=test_git_env()
    ).stdout.strip()
    return revision


def assert_measure(repo, revision, expected_failures):
    process = run_cli(["--repo", str(repo), "--rev", revision, "--json"])
    expected_exit = 0 if not expected_failures else 1
    if process.returncode != expected_exit:
        raise AssertionError(
            f"expected exit {expected_exit}, got {process.returncode}; "
            f"stderr={process.stderr.strip()!r}"
        )
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"measurement output is not JSON: {exc}") from exc
    items = result.get("items") if isinstance(result, dict) else None
    if not isinstance(items, list) or [item.get("id") for item in items] != list(ITEM_IDS):
        raise AssertionError("measurement did not return the stable six-item ID sequence")
    expected_failed = set(expected_failures)
    actual_failed = {item["id"] for item in items if item.get("status") == "FAIL"}
    if actual_failed != expected_failed:
        raise AssertionError(f"expected failed IDs {sorted(expected_failed)}, got {sorted(actual_failed)}")
    if any(item.get("status") not in ("PASS", "FAIL") for item in items):
        raise AssertionError("measurement returned an unknown item status")
    corrected = len(ITEM_IDS) - len(expected_failed)
    if (result.get("total"), result.get("corrected"), result.get("open")) != (
        len(ITEM_IDS),
        corrected,
        len(expected_failed),
    ):
        raise AssertionError("measurement population totals do not match the expected statuses")
    if len(expected_failed) == 1:
        return f"exit=1 isolated failure={next(iter(expected_failed))}"
    if expected_failed:
        return f"exit=1 malformed input failures={len(expected_failed)}"
    return "exit=0 corrected=6/6"


def selftest():
    cases = [
        ("clean fixture", None, []),
        ("missing dispatch", "remove-dispatch", [ITEM_IDS[0]]),
        ("staged measure mismatch", "mismatch-stage-measure", [ITEM_IDS[1]]),
        ("installed gate mismatch", "mismatch-installed-gate", [ITEM_IDS[2]]),
        ("missing selftest receipt", "remove-selftest-receipt", [ITEM_IDS[3]]),
        ("missing final receipts", "remove-final-receipts", [ITEM_IDS[4]]),
        ("missing historical receipts", "remove-historical-receipts", [ITEM_IDS[5]]),
        (
            "malformed contract JSON",
            "malformed-contract",
            [ITEM_IDS[0], ITEM_IDS[1], ITEM_IDS[2], ITEM_IDS[4], ITEM_IDS[5]],
        ),
    ]
    total = len(cases) + 2
    passed = 0
    with tempfile.TemporaryDirectory(prefix="receipt-measure-selftest.") as tmp:
        for index, (label, mutation, failures) in enumerate(cases, 1):
            try:
                repo = Path(tmp) / f"case-{index:02d}"
                revision = make_fixture(repo, mutation)
                detail = assert_measure(repo, revision, failures)
            except Exception as exc:  # noqa: BLE001
                print(f"FAIL [{index}/{total}] {label} — {exc}")
            else:
                passed += 1
                print(f"PASS [{index}/{total}] {label} — {detail}")

        usage_index = len(cases) + 1
        usage = run_cli(["--repo"])
        if usage.returncode == 2 and "usage:" in usage.stderr.lower():
            passed += 1
            print(f"PASS [{usage_index}/{total}] missing --repo value returns usage exit 2")
        else:
            print(
                f"FAIL [{usage_index}/{total}] missing --repo value: "
                f"exit={usage.returncode} stderr={usage.stderr.strip()!r}"
            )

        flag_index = len(cases) + 2
        try:
            repo = Path(tmp) / f"case-{flag_index:02d}"
            revision = make_fixture(repo, None)
            unsupported = run_cli(
                ["--repo", str(repo), "--rev", revision, "--check"]
            )
            if (
                unsupported.returncode == 2
                and "usage:" in unsupported.stderr.lower()
                and "--check" in unsupported.stderr
            ):
                passed += 1
                print(f"PASS [{flag_index}/{total}] frozen --check spelling remains unsupported")
            else:
                print(
                    f"FAIL [{flag_index}/{total}] --check compatibility boundary: "
                    f"exit={unsupported.returncode} stderr={unsupported.stderr.strip()!r}"
                )
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL [{flag_index}/{total}] --check compatibility boundary — {exc}")

    runner_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(f"RECEIPT_MEASURE_RUNNER_SHA256: {runner_sha}")
    print(f"ROUND20_MEASURE_INSTRUMENT_SHA256: {FROZEN_MEASURE_SHA}")
    print(f"RECEIPT_MEASURE_SELFTEST: {passed}/{total} pass")
    return 0 if passed == total else 1


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments == ["--selftest"]:
        return selftest()
    if "--selftest" in arguments:
        print("usage: receipt-measure.py --selftest (alone)", file=sys.stderr)
        return 2
    process = subprocess.run(
        [sys.executable, "-B", str(MEASURE), *arguments],
        env=clean_env(),
    )
    return process.returncode


if __name__ == "__main__":
    sys.exit(main())
