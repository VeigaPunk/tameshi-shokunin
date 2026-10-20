#!/usr/bin/env python3
"""Black-box verifier for the repeated-control mismatch contract.

This is evidence plumbing, not the gate implementation. The same verifier,
fixture, runs=3 request, and expected finding are used against each gate
candidate. Raw gate stdout/stderr and its process exit are preserved.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

FINDING_EXITS = {"controls_match": 0, "controls_mismatch": 1}
HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixture.sh"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--expect", required=True, choices=FINDING_EXITS)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    args = parser.parse_args()

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    gate_out = out / "gate-runs"
    argv = [
        sys.executable,
        str(args.gate.resolve()),
        "--runs",
        "3",
        "--out",
        str(gate_out),
        "--",
        "sh",
        str(args.fixture.resolve()),
    ]
    env = os.environ.copy()
    env["FAILURE_ORACLE_STATE"] = str(out / "fixture-state.txt")
    result = subprocess.run(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=False,
    )
    (out / "gate.stdout").write_bytes(result.stdout)
    (out / "gate.stderr").write_bytes(result.stderr)
    (out / "gate.exit").write_text(f"{result.returncode}\n", encoding="ascii")

    wanted_id = args.expect.encode("ascii")
    has_wanted_id = wanted_id in result.stdout or wanted_id in result.stderr
    expected_exit = FINDING_EXITS[args.expect]
    passed = result.returncode == expected_exit and has_wanted_id
    manifest = {
        "gate_argv": argv,
        "expected_finding": args.expect,
        "expected_exit": expected_exit,
        "observed_exit": result.returncode,
        "expected_finding_observed": has_wanted_id,
        "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
        "verifier_pass": passed,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(f"expected_finding={args.expect}")
    print(f"expected_exit={expected_exit}")
    print(f"observed_exit={result.returncode}")
    print(f"expected_finding_observed={str(has_wanted_id).lower()}")
    print(f"gate_stdout={result.stdout!r}")
    print(f"gate_stderr={result.stderr!r}")
    print(f"VERDICT: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
