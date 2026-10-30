#!/usr/bin/env python3
"""T59W1S30 reference probe: NUL path-handling boundary for tools/executor-source-pin.py.

STATUS: reference test artifact (NOT a production patch, NOT a candidate tool).
Why this file: seat T59W1S30 adversarial item "NUL path handling". The frozen
round-59 CLI contract delivers --path only via argv; POSIX execve argv strings
are NUL-terminated, so a NUL path can never reach the tool process. This script
is the exact test that demonstrates the boundary and, for defense-in-depth,
the behavior any future non-argv path channel (e.g. --paths-file) MUST exhibit.

Checks:
  T-boundary  --path with NUL at OS level: harness raises ValueError; tool
              process is never created (no exit code is observable).
  T-guard     in-process main(argv=[... '--path', 'a\0b']) must exit 2 with
              EXECUTOR_SOURCE_UNAVAILABLE (reachable only in-process today).

Usage: python3 executor-source-pin.py.nul-probe.py /path/to/tools/executor-source-pin.py
"""
import importlib.util
import io
import contextlib
import subprocess
import sys

UNAVAILABLE = "EXECUTOR_SOURCE_UNAVAILABLE"


def check_boundary(tool):
    """NUL through the real CLI: the harness itself must refuse before exec."""
    argv = [sys.executable, "-I", tool, "--repo", ".", "--trusted",
            "0" * 40, "--candidate", "0" * 40, "--path", "tools/a\x00b.py"]
    try:
        subprocess.run(argv, capture_output=True)
    except ValueError as e:
        assert "null" in str(e), str(e)
        return "ok: ValueError(%s) raised in harness; tool never started" % e
    return "FAIL: NUL path was delivered to the tool process"


def check_guard(tool):
    """In-process argv list: the only channel that can currently carry NUL."""
    spec = importlib.util.spec_from_file_location("cand_under_test", tool)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            rc = m.main(["--repo", ".", "--trusted", "0" * 40,
                         "--candidate", "0" * 40, "--path", "tools/a\x00b.py"])
        except SystemExit as e:  # argparse-style exit
            rc = e.code
    if rc == 2 and UNAVAILABLE in err.getvalue():
        return "ok: rc=2 + %s for NUL path" % UNAVAILABLE
    return "FAIL: rc=%r stderr=%r (want rc=2 + %s)" % (
        rc, err.getvalue(), UNAVAILABLE)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: nul-probe.py /path/to/tools/executor-source-pin.py")
    tool = sys.argv[1]
    print("T-boundary:", check_boundary(tool))
    print("T-guard   :", check_guard(tool))


if __name__ == "__main__":
    main()
