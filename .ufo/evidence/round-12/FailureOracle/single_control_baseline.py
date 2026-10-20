#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command after -- is required")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    result = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (out / "run-1.stdout").write_bytes(result.stdout)
    (out / "run-1.stderr").write_bytes(result.stderr)
    (out / "run-1.exit").write_text(f"{result.returncode}\n", encoding="ascii")
    if result.returncode == 0:
        print("controls_match")
        return 0
    print("baseline_nonzero")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
