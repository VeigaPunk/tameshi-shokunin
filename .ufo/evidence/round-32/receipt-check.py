#!/usr/bin/env python3
"""receipt-check.py — receipt-completeness checker for evidence directories.

A receipt is a pair of files that share a stem: `<stem>.stdout` (the captured
output of a command) and `<stem>.exit` (the command's exit status). A
`<stem>.stdout` with no `<stem>.exit` sibling means the command's exit status
was never captured: the receipt is incomplete and the exit status is
unrecoverable without re-running the command.

Interface:

    python3 receipt-check.py DIR
    python3 receipt-check.py --selftest

`DIR` is walked recursively (directory symlinks are not followed). For every
`*.stdout` file found, the checker looks for a sibling `<stem>.exit` in the
same directory. Each `*.stdout` without such a sibling is listed, one per
line, as a path relative to `DIR`. The final line is always:

    RECEIPT_CHECK: missing_exit=N files=M

where N is the number of `*.stdout` files without a sibling `.exit` file and
M is the total number of `*.stdout` files examined. Exit status is 1 iff
N > 0, else 0. Exit status 2 means the checker could not run (missing or
non-directory argument, or an unreadable tree).

Files that are not `*.stdout` are ignored entirely: `.exit` files with no
`.stdout` sibling, `.stderr` files, and any other artifact in the tree.

Sibling means same-directory sibling. A `<stem>.exit` in an ancestor or
descendant directory does not satisfy the check.
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

STDOUT_SUFFIX = ".stdout"
EXIT_SUFFIX = ".exit"
SUMMARY_PREFIX = "RECEIPT_CHECK:"


def find_stdout_files(root):
    """Return every `*.stdout` file under `root`, sorted, symlinked dirs skipped."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames):
            if name.endswith(STDOUT_SUFFIX):
                found.append(Path(dirpath) / name)
    found.sort()
    return found


def exit_sibling(stdout_path):
    """The same-directory `<stem>.exit` path for a `<stem>.stdout` path."""
    stem = stdout_path.name[: -len(STDOUT_SUFFIX)]
    return stdout_path.with_name(stem + EXIT_SUFFIX)


def scan(root):
    """Return (missing, total): stdout paths lacking a sibling .exit, and count."""
    stdout_files = find_stdout_files(root)
    missing = [p for p in stdout_files if not exit_sibling(p).exists()]
    missing.sort()
    return missing, len(stdout_files)


def rel(path, root):
    """Path relative to `root` in posix form, falling back to the absolute path."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def check(root):
    """Run the check on `root`; return (exit_code, stdout_lines)."""
    root = Path(root)
    if not root.exists():
        return 2, ["RECEIPT_CHECK: error=not_found dir=%s" % root]
    if not root.is_dir():
        return 2, ["RECEIPT_CHECK: error=not_a_dir dir=%s" % root]

    missing, total = scan(root)
    lines = [rel(p, root) for p in missing]
    lines.append("RECEIPT_CHECK: missing_exit=%d files=%d" % (len(missing), total))
    return (1 if missing else 0), lines


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

FIXTURES = [
    {
        "name": "empty-tree",
        "files": {},
        "expect_exit": 0,
        "expect_missing": 0,
        "expect_files": 0,
        "expect_listed": [],
    },
    {
        "name": "complete-pair",
        "files": {"a.stdout": "out\n", "a.exit": "0\n"},
        "expect_exit": 0,
        "expect_missing": 0,
        "expect_files": 1,
        "expect_listed": [],
    },
    {
        "name": "missing-exit",
        "files": {"x.stdout": "out\n"},
        "expect_exit": 1,
        "expect_missing": 1,
        "expect_files": 1,
        "expect_listed": ["x.stdout"],
    },
    {
        "name": "sibling-is-same-dir",
        "files": {
            "dup.stdout": "parent\n",
            "sub/dup.stdout": "child\n",
            "sub/dup.exit": "0\n",
        },
        "expect_exit": 1,
        "expect_missing": 1,
        "expect_files": 2,
        "expect_listed": ["dup.stdout"],
    },
    {
        "name": "non-stdout-ignored",
        "files": {
            "notes.txt": "text\n",
            "run.stderr": "err\n",
            "orphan.exit": "0\n",
            "weird.stdout.bak": "not a receipt\n",
        },
        "expect_exit": 0,
        "expect_missing": 0,
        "expect_files": 0,
        "expect_listed": [],
    },
    {
        "name": "multiple-missing",
        "files": {
            "m1.stdout": "1\n",
            "m2.stdout": "2\n",
            "ok.stdout": "3\n",
            "ok.exit": "0\n",
            "deep/nested/m3.stdout": "4\n",
        },
        "expect_exit": 1,
        "expect_missing": 3,
        "expect_files": 4,
        "expect_listed": ["deep/nested/m3.stdout", "m1.stdout", "m2.stdout"],
    },
]


def build_fixture(base, spec):
    """Materialise one fixture case under `base`; return its directory."""
    case_dir = base / spec["name"]
    for relname, content in spec["files"].items():
        target = case_dir / relname
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    case_dir.mkdir(parents=True, exist_ok=True)
    return case_dir


def run_cli(args):
    """Run this script as a subprocess; return (returncode, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, os.path.abspath(__file__)] + args,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITECODE": "1"},
    )
    return proc.returncode, proc.stdout, proc.stderr


def parse_summary(stdout):
    """Return (missing, files) parsed from the summary line, or None."""
    for line in stdout.splitlines():
        if line.startswith(SUMMARY_PREFIX):
            fields = {}
            for token in line.split()[1:]:
                if "=" in token:
                    key, value = token.split("=", 1)
                    fields[key] = value
            if "missing_exit" not in fields or "files" not in fields:
                return None
            return int(fields["missing_exit"]), int(fields["files"])
    return None


def selftest():
    """Run every fixture case end-to-end through the CLI; return exit code."""
    failures = []
    with tempfile.TemporaryDirectory(prefix="receipt-check-selftest-") as tmp:
        base = Path(tmp)
        for spec in FIXTURES:
            case_dir = build_fixture(base, spec)
            code, out, err = run_cli([str(case_dir)])
            listed = [ln for ln in out.splitlines() if not ln.startswith(SUMMARY_PREFIX)]
            summary = parse_summary(out)

            problems = []
            if code != spec["expect_exit"]:
                problems.append("exit=%d want=%d" % (code, spec["expect_exit"]))
            if summary is None:
                problems.append("no summary line")
            else:
                missing, files = summary
                if missing != spec["expect_missing"]:
                    problems.append("missing_exit=%d want=%d" % (missing, spec["expect_missing"]))
                if files != spec["expect_files"]:
                    problems.append("files=%d want=%d" % (files, spec["expect_files"]))
            if listed != spec["expect_listed"]:
                problems.append("listed=%r want=%r" % (listed, spec["expect_listed"]))
            if err.strip():
                problems.append("stderr=%r" % err)

            status = "ok" if not problems else "FAIL"
            print("case %-22s %s" % (spec["name"], status))
            for problem in problems:
                print("  problem: %s" % problem)
                failures.append("%s: %s" % (spec["name"], problem))

    print("RECEIPT_CHECK_SELFTEST: cases=%d failed=%d" % (len(FIXTURES), len(failures)))
    return 1 if failures else 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="receipt-check.py",
        description="List *.stdout files under DIR that have no sibling .exit file.",
    )
    parser.add_argument("dir", nargs="?", help="directory to check")
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="run built-in fixture cases in a temp dir and exit",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    if not args.dir:
        parser.print_usage(sys.stderr)
        print("RECEIPT_CHECK: error=no_dir", file=sys.stderr)
        return 2

    code, lines = check(args.dir)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
