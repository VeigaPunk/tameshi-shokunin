# ExecReceiptCheck — round 32, wave 1

## Verdict

**The checker is built, self-tests green, and is demonstrably able to fail.** It reports
`RECEIPT_CHECK: missing_exit=5 files=12` and exit 1 on
`.ufo/evidence/round-31` (listing `after/commandD-at-final.stdout` as required), and
`RECEIPT_CHECK: missing_exit=0 files=7` and exit 0 on `.ufo/evidence/round-32`. Six
fixture cases in `--selftest` all pass; three independent mutation probes confirm the
checker reacts to a deleted exit, a moved exit, and a newly added stdout.

Axis: **calibration** (the assigned judging axis). The claim is that the tool discriminates
a complete receipt tree from an incomplete one — demonstrated by a red run on a tree that
is known to be incomplete and a green run on a tree that is known to be complete, with a
fixture suite and mutation probes in between so neither direction is accidental.

Axis not claimed: **operability** of C1 (the tally audit). This seat does not touch
`tools/mutate-and-run.sh`, the frozen counter, or the frozen contract.

Files written: exactly one, this report, at
`.ufo/waves/round-32/w1/ExecReceiptCheck.md`. The tool itself lives in this seat's scratch
directory at `/fast/scratch/hyaku/tameshi-r32-seats/ExecReceiptCheck/receipt-check.py`;
per the assignment the L1 may commit it (suggested install path `tools/receipt-check.py`).
No production file was edited, no git write command was run, no `jj` command was run, no
commit was made.

## The tool

Path in scratch: `/fast/scratch/hyaku/tameshi-r32-seats/ExecReceiptCheck/receipt-check.py`
(267 lines, sha256 `3a82410750846f8be3a3493f61f0a7ea901a06b89a007a4e1f21e40cddf88a44`).

Contract implemented, verbatim from the assignment:

- `python3 receipt-check.py DIR` lists every `*.stdout` file under `DIR` with no sibling
  `.exit` file of the same stem, one path per line, relative to `DIR`.
- The final line is always `RECEIPT_CHECK: missing_exit=N files=M`, where N is the number of
  listed files and M is the total number of `*.stdout` files examined.
- Exit status is 1 iff N > 0, else 0. Exit status 2 means the check could not run
  (missing directory, non-directory argument, no argument).
- `--selftest` runs six fixture cases, each in its own subdirectory of one
  `tempfile.TemporaryDirectory`, and drives the CLI as a subprocess so the exit code, the
  summary line and the listed paths are all exercised end to end.

One semantic choice worth naming: **sibling means same-directory sibling.** A `<stem>.exit`
in an ancestor or descendant directory does not satisfy the check. Fixture case
`sibling-is-same-dir` pins this.

### Full script

```python
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
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
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
```

## Evidence

All commands ran with working directory
`/fast/scratch/hyaku/tameshi-r32-seats/ExecReceiptCheck` unless stated otherwise. No sibling
seat's scratch directory was opened. No process was spawned other than the tool's own
`--selftest` subprocesses. No long-running job was started, so no process tree needed killing.

### A. Selftest — six fixture cases

```sh
cd /fast/scratch/hyaku/tameshi-r32-seats/ExecReceiptCheck
python3 receipt-check.py --selftest; echo "exit=$?"
```

Observed stdout; exit 0:

```text
case empty-tree             ok
case complete-pair          ok
case missing-exit           ok
case sibling-is-same-dir    ok
case non-stdout-ignored     ok
case multiple-missing       ok
RECEIPT_CHECK_SELFTEST: cases=6 failed=0
exit=0
```

Fixture coverage, mapped to the properties each case pins:

| case | what it pins |
|---|---|
| `empty-tree` | an empty tree is not a failure (N=0, M=0, exit 0) |
| `complete-pair` | a matched `.stdout`/`.exit` pair is not reported |
| `missing-exit` | a lone `.stdout` is reported and exit is 1 |
| `sibling-is-same-dir` | the exit must be in the *same* directory; a same-stem exit in a child dir does not rescue the parent |
| `non-stdout-ignored` | `.stderr`, `.txt`, `.stdout.bak` and orphan `.exit` files are all ignored (M=0) |
| `multiple-missing` | counting and sorting across nested dirs: 3 missing of 4 stdout files, sorted paths |

### B. Able to fail — round-31 (incomplete tree)

```sh
python3 receipt-check.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31; echo "exit=$?"
```

Observed stdout; exit 1:

```text
after/commandD-at-final.stdout
ctl/bind-v5-new-shapes.stdout
ctl/bind-v5-old-controls.stdout
ctl/bind-v5-old-shapes.stdout
ctl/bind-v5-real-r30.stdout
RECEIPT_CHECK: missing_exit=5 files=12
exit=1
```

`after/commandD-at-final.stdout` — the file the assignment named — is listed. It is the only
missing exit under `after/`; the other four are the round-31 `ctl/` pre-data control
stdout files, which were never accompanied by `.exit` receipts.

### C. Green — round-32 (complete tree)

```sh
python3 receipt-check.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-32; echo "exit=$?"
```

Observed stdout; exit 0:

```text
RECEIPT_CHECK: missing_exit=0 files=7
exit=0
```

All seven `.stdout` files in round-32 (`before/` 4, `repair/` 3) have a sibling `.exit`.

### D. Independent cross-check of B and C

The tool's own walk was checked against a shell loop that uses a different mechanism
(`find` + `${f%.stdout}`), run over round-31:

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31
for f in $(find . -name '*.stdout' | sort); do stem=${f%.stdout}; if [ -f "$stem.exit" ]; then echo "OK      $f"; else echo "MISSING $f"; fi; done
```

Observed stdout; exit 0:

```text
OK      ./after/c1-at-83c001a5.stdout
OK      ./after/c1-at-final.stdout
OK      ./after/c1monitor-at-83c001a5.stdout
OK      ./after/c1monitor-at-final.stdout
OK      ./after/census-end.stdout
MISSING ./after/commandD-at-final.stdout
OK      ./before/c1-at-base.stdout
OK      ./before/census-start.stdout
MISSING ./ctl/bind-v5-new-shapes.stdout
MISSING ./ctl/bind-v5-old-controls.stdout
MISSING ./ctl/bind-v5-old-shapes.stdout
MISSING ./ctl/bind-v5-real-r30.stdout
```

Twelve stdout files, five missing — identical to the tool's `missing_exit=5 files=12`, with
identical listed paths.

### E. Mutation probes — the checker reacts to a broken tree

Three copies of the round-32 tree were made in this seat's scratch directory and broken one
way each. (The copies were deleted afterwards; `ls` in the scratch dir shows only
`receipt-check.py`.)

**M1 — delete an exit file:**

```sh
cp -r .../round-32 mut && rm mut/before/c1-at-base.exit
python3 receipt-check.py mut; echo "exit=$?"
```

```text
before/c1-at-base.stdout
RECEIPT_CHECK: missing_exit=1 files=7
exit=1
```

**M2 — move an exit file out of its sibling directory:**

```sh
cp -r .../round-32 mut2 && mv mut2/repair/commandD-at-r31-67c0e013.exit mut2/commandD-at-r31-67c0e013.exit
python3 receipt-check.py mut2; echo "exit=$?"
```

```text
repair/commandD-at-r31-67c0e013.stdout
RECEIPT_CHECK: missing_exit=1 files=7
exit=1
```

**M3 — add a stdout file with no exit:**

```sh
cp -r .../round-32 mut3 && printf 'x' > mut3/before/brand-new.stdout
python3 receipt-check.py mut3; echo "exit=$?"
```

```text
before/brand-new.stdout
RECEIPT_CHECK: missing_exit=1 files=8
exit=1
```

Each mutation flips the exit status from 0 to 1 and names exactly the broken receipt.

### F. Error paths (cannot audit)

```sh
python3 receipt-check.py /fast/scratch/hyaku/tameshi-r32-seats/ExecReceiptCheck/nope; echo "exit=$?"
python3 receipt-check.py receipt-check.py; echo "exit=$?"
python3 receipt-check.py; echo "exit=$?"
```

Observed; exit 2 on each:

```text
RECEIPT_CHECK: error=not_found dir=/fast/scratch/hyaku/tameshi-r32-seats/ExecReceiptCheck/nope
exit=2
RECEIPT_CHECK: error=not_a_dir dir=receipt-check.py
exit=2
usage: receipt-check.py [-h] [--selftest] [dir]
RECEIPT_CHECK: error=no_dir
exit=2
```

A relative path and a trailing slash also work (`round-32/` from
`.ufo/evidence` gave `RECEIPT_CHECK: missing_exit=0 files=7`, exit 0).

### G. Source hygiene

```sh
sha256sum receipt-check.py && wc -l receipt-check.py && python3 -c "import ast; ast.parse(open('receipt-check.py').read()); print('syntax ok')"
```

```text
3a82410750846f8be3a3493f61f0a7ea901a06b89a007a4e1f21e40cddf88a44  receipt-check.py
267 receipt-check.py
syntax ok
```

## Calibration notes and risks

1. **The five round-31 findings are not all the same kind of defect.** `after/commandD-at-final.stdout`
   is a receipt whose exit status was never captured — the defect the L1's round-32 repair
   work addresses. The four `ctl/bind-v5-*.stdout` files are control outputs that were
   never receipt pairs at all (the round-31 `ctl/README-bind-v5.txt` records them as the
   record of a re-scoring run, not as command receipts). The checker reports the second
   kind too, because the assigned rule is purely mechanical: "every `*.stdout` file under
   DIR with no sibling `.exit` file of the same stem". If the L1 wants the tool to
   distinguish receipt pairs from other stdout artifacts, that is a rule change and needs
   an explicit decision, not a silent narrowing. As built, the tool reports both.
2. **M=2 is ambiguous in the assignment.** "missing_exit=N files=M" is read here as N =
   missing count, M = total stdout files examined. An alternative reading is M = number of
   listed files, which would make M == N always and render the second number pointless.
   The reading above is the useful one and is documented in the script docstring.
3. **Symlinked directories are not followed** (`os.walk(followlinks=False)`), so a receipt
   reachable only through a symlinked directory would not be counted. None exist in the
   two trees checked. Symlinked *files* are counted, since `os.walk` reports them in
   `filenames`.
4. **The checker does not validate the content of an `.exit` file** — only its presence.
   An empty or malformed `.exit` still counts as present. That is the assigned rule; a
   stricter rule would be a separate tool.
5. **Sibling means same-directory.** M2 above demonstrates the consequence: an exit file
   that exists but sits in a different directory does not rescue its stdout. This is
   deliberate and pinned by fixture `sibling-is-same-dir`.
6. **Not committed.** The tool is in scratch only. If the L1 commits it, the natural home
   is `tools/receipt-check.py`, matching the existing `tools/` convention in this repo
   (`tools/receipt-measure.py`, `tools/receipt-window.py`, `tools/registry-check.py`).
   Installing it under `tools/` would make it available to the cold-read ledger; the
   checker does not depend on the repo layout and can be run from any directory.

## Tooling

No package was installed or upgraded by this seat. The tool uses only the Python 3
standard library; the interpreter present is CPython 3.14.8 (`python3 -VV`). Nothing was
installed through pacman, `uv tool`, `cargo` or `npm`, so there is no install to record.

## Risks and blockers

- **None blocking.** The tool is complete, self-tested, and demonstrated in both
  directions.
- The only open item is the L1's decision on whether to commit the tool to
  `tools/receipt-check.py`, and whether the `ctl/` class of finding (risk note 1) should
  be excluded by a rule change. Both are L1 calls, not defects in this deliverable.

Report: .ufo/waves/round-32/w1/ExecReceiptCheck.md
