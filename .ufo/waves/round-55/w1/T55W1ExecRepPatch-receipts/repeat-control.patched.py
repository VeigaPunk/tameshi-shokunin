#!/usr/bin/env python3
"""repeat-control.py — repeated pristine-control gate (tameshi-shokunin, round 12).

Capability C1 (calibration). The mutation runner checks the pristine control
exactly once per sweep (`tools/mutate-and-run.sh`; H2 in
`.ufo/evidence/kaika-round-1/capability-demo/README.md` records "exactly one
control run per sweep, no repeat-control option"), and one run cannot separate
a stable baseline from a flaky one. This gate runs one exact argv N >= 3 times
and decides whether the N pristine controls agreed.

Interface (round-12 contract):

    python3 tools/repeat-control.py --runs N --out DIR -- COMMAND [ARG...]
    python3 tools/repeat-control.py --snapshot DIR
    python3 tools/repeat-control.py --selftest

Run mode: the exact argv after `--` is executed N times with stdin /dev/null,
shell=False, in the caller's cwd; the environment is inherited unchanged. Run
k's raw stdout, raw stderr and exit are saved as
DIR/run-<k>.{stdout,stderr,exit} (exit = Python's signed returncode, decimal
plus LF; the text `unavailable` when the command could not be executed, with
the OSError text in run-<k>.stderr). Bytes are compared as bytes: no decoding,
stripping, newline normalization or whitespace folding anywhere in the
comparison path. DIR must not exist — it is created fresh and never deleted;
an existing DIR is refused with exit 64. DIR also receives command.txt (argv,
cwd, runs, interpreter, tool path and sha256) and, written last, finding.txt
(the finding ID and exit). `--out` placed inside a tree the command itself
inspects makes the command mismatch with itself; keep it outside that tree.

Precedence (fixed before the run, applied to the saved observations):
  1. any run whose command could not be executed -> command_unavailable
  2. else any disagreement in (exit, stdout, stderr) -> controls_mismatch
     (checked before the baseline, so [0,1,0] is a mismatch, never a
     nonzero baseline)
  3. else a stable nonzero baseline -> baseline_nonzero
A uniform nonzero baseline is baseline_nonzero 2 ([1,1,1], [7,7,7], a
stable signal death); nonzero tuples that differ are controls_mismatch 1
([1,0,0], [1,2,1]) — exit 1 says the observations disagreed, nothing about
the mutation denominator.
  4. else -> controls_match
Finding IDs and exits (stable):
  controls_match 0 · controls_mismatch 1 · baseline_nonzero 2 ·
  command_unavailable 2 · snapshot_tampered 2 · setup_error 2 · invalid_usage 64
`baseline_nonzero`, `command_unavailable`, `snapshot_tampered`, `setup_error`
and `invalid_usage` are could-not-evaluate: they are never a verdict on the
command's behaviour. `setup_error` is this tool's own failure class (evidence
directory not writable, unexpected exception); it exists so that no uncaught
Python exception can exit 1 and be read as `controls_mismatch`.

--snapshot DIR: read-only validation of a committed frozen control snapshot.
DIR holds `expected.json` (schema `repeat-control-snapshot-v1`: runs,
expected_id, expected_exit, and a sha256 for every observation file) plus the
saved observations run-<k>.{stdout,stderr,exit}. The gate hashes every listed
input and recomputes the finding from the stored bytes; the recorded values
are never trusted as a verdict. It executes nothing — no subprocess call is
reachable from this mode. A run-mode DIR (command.txt and finding.txt, no
expected.json) is not a frozen snapshot and is refused. A verified snapshot
prints its recorded ID and exits
with its recorded exit; an intact snapshot whose stored bytes recompute to a
different finding exits 1 `controls_mismatch`; a missing, changed, symlinked or
unlisted input, a malformed record, or any shape error exits 2
`snapshot_tampered`. Committed snapshots live at
`.ufo/evidence/round-12/ControlGate/` (stable -> controls_match) and its
`mismatch/` subdirectory (controls_mismatch).

--selftest: hermetic; writes its fixture commands and snapshot fixtures under
`/tmp/tameshi-r12-repeat-control-selftest.*`, invokes this file as a child
process for every case, and checks the exact finding ID and exit against the
expectations embedded here. Cases: stable control with saved-bytes fidelity;
stdout mismatch (every run differs; the [same, same, different] shape);
trailing-newline-only mismatch; stderr mismatch; exit mismatch [0,0,1] and
differing nonzero exits [1,2,1] (disagreement is decided before the
baseline); stable nonzero baseline; stable child 127; command unavailable
(ENOENT, EACCES, ENOEXEC); invalid run counts (2, 1, 0, non-integer), a
missing `--` and an existing `--out`; stdin isolation (`cat` reads /dev/null,
saved stdout empty); snapshot pass and snapshot mismatch; six snapshot
tamper arms (changed byte, missing input, unlisted file, duplicate manifest
key, symlinked manifest, symlinked observation); and the committed snapshots
under `.ufo/evidence/round-12/ControlGate/` and `.../mismatch/`. Exit: 0 all cases
pass · 1 at least one case fails · 2 could-not-evaluate (committed fixture
root missing or not a directory). Scratch is removed on pass and kept on
failure.

Limitations (stated, not hidden): there is no timeout and no process
supervisor — a command that hangs yields no verdict, and a command that leaves
a background process holding stdout/stderr open delays the gate until that
process exits, or hangs it indefinitely (wrap the command in `timeout` at the
call site if that matters). A background process can still share state with
later runs (files, ports, locks) and change what those runs emit. Snapshot
digests are stored inside the directory they validate, so they catch
accidental drift, not a coordinated edit of an observation plus its recorded
digest; the external anchor is the repository's committed history. A clean
`controls_match` states that N finite observations agreed on this host in this
environment — it is not a determinism proof and it cures no flakiness.

Dependencies: python3 (stdlib only). `--selftest` additionally needs `bash`
and `cat` on PATH. Plan anchor: `corpus/README.md` frontier F3 (determinism
precondition, flaky-aware verdicts) — "one control per sweep -> N >= 3
byte-identical controls, or a named mismatch".
"""

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

VERSION = "repeat-control.py r12 (tameshi-shokunin, 2026-10-20)"
SELF = os.path.realpath(__file__)
EVIDENCE_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(SELF)),
    ".ufo",
    "evidence",
    "round-12",
    "ControlGate",
)

EXIT_BY_ID = {
    "controls_match": 0,
    "controls_mismatch": 1,
    "baseline_nonzero": 2,
    "command_unavailable": 2,
    "snapshot_tampered": 2,
    "setup_error": 2,
    "invalid_usage": 64,
}
SNAPSHOT_SCHEMA = "repeat-control-snapshot-v1"
SNAPSHOT_IDS = (
    "controls_match",
    "controls_mismatch",
    "baseline_nonzero",
    "command_unavailable",
)
DIGEST_RE = re.compile(r"[0-9a-f]{64}")
EXIT_FILE_RE = re.compile(r"(?:-?[0-9]+|unavailable)\n")

USAGE = (
    "usage: repeat-control.py --runs N --out DIR -- COMMAND [ARG...]\n"
    "       repeat-control.py --snapshot DIR\n"
    "       repeat-control.py --selftest\n"
)


class ScratchRootUnusable(RuntimeError):
    """A set-but-unusable TMPDIR: could-not-evaluate, never a traceback (round 55).

    A distinct type so main() can answer with the frozen grammar line instead of
    the generic setup line that leaks the Python type name. The operator-visible
    class is the line, not this class (scratch-root-contract §1)."""


def strict_scratch_root():
    """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
    round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
    fallback to /tmp, preserving CR47 semantics), else the platform default."""
    import os as _os
    t = _os.environ.get("TMPDIR")
    if t:
        if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
            raise ScratchRootUnusable(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()


class TamperError(Exception):
    """A --snapshot directory does not match its committed record."""


def emit(line):
    try:
        print(line, flush=True)
    except (OSError, ValueError):
        # The observation verdict must not change because the terminal or
        # pipe refused the line (/dev/full, closed pipe, full disk).
        pass


def emit_err(line):
    try:
        print(line, file=sys.stderr, flush=True)
    except (OSError, ValueError):
        pass


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def tool_sha256():
    with open(SELF, "rb") as handle:
        return sha256_bytes(handle.read())


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def write_new(path, data):
    with open(path, "xb") as handle:
        handle.write(data)


def finish(finding, message=None):
    if message:
        emit_err(message)
    emit(f"REPEAT_CONTROL: {finding}")
    return EXIT_BY_ID[finding]


def usage_failure(message):
    emit_err(f"repeat-control: {message}")
    emit_err(USAGE.rstrip("\n"))
    return finish("invalid_usage")


def setup_failure(message):
    emit_err(f"repeat-control: setup: {message}")
    emit("REPEAT_CONTROL: setup_error")
    return EXIT_BY_ID["setup_error"]


def classify(records):
    """Apply the fixed precedence to the saved per-run observations."""
    if any(not record["available"] for record in records):
        return "command_unavailable"
    first = records[0]
    for record in records[1:]:
        if (record["exit_text"], record["stdout"], record["stderr"]) != (
            first["exit_text"],
            first["stdout"],
            first["stderr"],
        ):
            return "controls_mismatch"
    if first["exit_text"] != "0":
        return "baseline_nonzero"
    return "controls_match"


# --------------------------------------------------------------------- run mode


def run_mode(argv):
    runs_raw = None
    out_dir = None
    command = None
    seen = set()
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--":
            command = argv[index + 1:]
            break
        if arg in ("--runs", "--out"):
            if arg in seen:
                return usage_failure(f"{arg} given twice")
            seen.add(arg)
            if index + 1 >= len(argv):
                return usage_failure(f"{arg} requires a value")
            if arg == "--runs":
                runs_raw = argv[index + 1]
            else:
                out_dir = argv[index + 1]
            index += 2
            continue
        return usage_failure(f"unexpected argument before --: {arg!r}")
    if runs_raw is None:
        return usage_failure("--runs is required")
    if out_dir is None:
        return usage_failure("--out is required")
    if command is None:
        return usage_failure("the -- separator is required before the command")
    if not command:
        return usage_failure("the command after -- is empty")
    if not re.fullmatch(r"[0-9]+", runs_raw):
        return usage_failure(f"--runs must be an ASCII integer, got {runs_raw!r}")
    runs = int(runs_raw)
    if runs < 3:
        return usage_failure(f"--runs must be >= 3, got {runs}")
    return run_controls(command, runs, out_dir)


def command_record(command, runs):
    lines = [
        f"tool={SELF}",
        f"tool-sha256={tool_sha256()}",
        f"interpreter={sys.executable}",
        f"python={sys.version.split()[0]}",
        f"cwd={os.getcwd()}",
        f"runs={runs}",
        "argv=" + json.dumps(command, ensure_ascii=True),
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def run_once(command, index, out_dir):
    try:
        proc = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
    except OSError as exc:
        available = False
        stdout_bytes = b""
        stderr_bytes = f"{exc}\n".encode("utf-8", "replace")
        exit_text = "unavailable"
    else:
        available = True
        stdout_bytes = proc.stdout
        stderr_bytes = proc.stderr
        exit_text = str(proc.returncode)
    try:
        write_new(os.path.join(out_dir, f"run-{index}.stdout"), stdout_bytes)
        write_new(os.path.join(out_dir, f"run-{index}.stderr"), stderr_bytes)
        write_new(os.path.join(out_dir, f"run-{index}.exit"), (exit_text + "\n").encode("ascii"))
    except OSError as exc:
        return setup_failure(f"cannot write run-{index} evidence in {out_dir}: {exc}")
    return {
        "available": available,
        "exit_text": exit_text,
        "stdout": stdout_bytes,
        "stderr": stderr_bytes,
    }


def run_controls(command, runs, out_dir):
    emit(f"REPEAT_CONTROL_TOOL {VERSION} tool-sha256={tool_sha256()}")
    try:
        os.makedirs(out_dir, exist_ok=False)
    except FileExistsError:
        return usage_failure(f"--out already exists (refused, never overwritten): {out_dir}")
    except OSError as exc:
        return setup_failure(f"cannot create --out {out_dir}: {exc}")
    try:
        write_new(os.path.join(out_dir, "command.txt"), command_record(command, runs))
    except OSError as exc:
        return setup_failure(f"cannot write command.txt in {out_dir}: {exc}")
    records = []
    for index in range(1, runs + 1):
        record = run_once(command, index, out_dir)
        if isinstance(record, int):  # setup_failure already emitted its verdict
            return record
        records.append(record)
        emit(
            "REPEAT_RUN %d exit=%s stdout-bytes=%d stderr-bytes=%d"
            % (index, record["exit_text"], len(record["stdout"]), len(record["stderr"]))
        )
    finding = classify(records)
    agreed = finding in ("controls_match", "baseline_nonzero")
    emit(f"REPEAT_COMPARE identical={'yes' if agreed else 'no'} runs={runs}")
    try:
        write_new(
            os.path.join(out_dir, "finding.txt"),
            f"REPEAT_CONTROL: {finding}\nREPEAT_EXIT: {EXIT_BY_ID[finding]}\n".encode("ascii"),
        )
    except OSError as exc:
        return setup_failure(f"cannot write finding.txt in {out_dir}: {exc}")
    emit(f"REPEAT_OUT {out_dir}")
    emit(f"REPEAT_CONTROL: {finding}")
    return EXIT_BY_ID[finding]


# ---------------------------------------------------------------- snapshot mode


def reject_duplicate_keys(pairs):
    record = {}
    for key, value in pairs:
        if key in record:
            raise TamperError(f"duplicate key in expected.json: {key!r}")
        record[key] = value
    return record


def load_snapshot(dirpath):
    path = os.path.join(dirpath, "expected.json")
    try:
        info = os.lstat(path)
    except OSError as exc:
        raise TamperError(f"expected.json unreadable: {exc}")
    if not stat.S_ISREG(info.st_mode):
        raise TamperError("expected.json is not a regular file")
    try:
        raw = read_bytes(path)
    except OSError as exc:
        raise TamperError(f"expected.json unreadable: {exc}")
    try:
        record = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, ValueError) as exc:
        raise TamperError(f"expected.json unparsable: {exc}")
    if not isinstance(record, dict) or record.get("schema") != SNAPSHOT_SCHEMA:
        raise TamperError("expected.json schema mismatch")
    runs = record.get("runs")
    if not isinstance(runs, int) or isinstance(runs, bool) or runs < 3:
        raise TamperError("expected.json runs must be an integer >= 3")
    expected_id = record.get("expected_id")
    expected_exit = record.get("expected_exit")
    if (
        expected_id not in SNAPSHOT_IDS
        or not isinstance(expected_exit, int)
        or isinstance(expected_exit, bool)
        or expected_exit != EXIT_BY_ID[expected_id]
    ):
        raise TamperError("expected.json expected_id/expected_exit is not a stable pair")
    required = set()
    for index in range(1, runs + 1):
        for suffix in ("stdout", "stderr", "exit"):
            required.add(f"run-{index}.{suffix}")
    inputs = record.get("inputs")
    if not isinstance(inputs, dict) or set(inputs) != required:
        raise TamperError("expected.json inputs do not list exactly the required run files")
    for name, digest in inputs.items():
        if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
            raise TamperError(f"input digest for {name} is not 64 lowercase hex")
    listed = set()
    for name in os.listdir(dirpath):
        if not os.path.isdir(os.path.join(dirpath, name)):
            listed.add(name)
    extra = listed - required - {"expected.json"}
    if extra:
        raise TamperError(f"unlisted files in snapshot: {sorted(extra)}")
    return record


def read_checked(dirpath, name, record):
    path = os.path.join(dirpath, name)
    try:
        info = os.lstat(path)
    except OSError as exc:
        raise TamperError(f"{name} unreadable: {exc}")
    if not stat.S_ISREG(info.st_mode):
        raise TamperError(f"{name} is not a regular file")
    data = read_bytes(path)
    if sha256_bytes(data) != record["inputs"][name]:
        raise TamperError(f"{name} digest mismatch")
    return data


def recompute_snapshot(dirpath, record):
    records = []
    for index in range(1, record["runs"] + 1):
        stdout_bytes = read_checked(dirpath, f"run-{index}.stdout", record)
        stderr_bytes = read_checked(dirpath, f"run-{index}.stderr", record)
        exit_raw = read_checked(dirpath, f"run-{index}.exit", record)
        try:
            exit_text = exit_raw.decode("ascii")
        except UnicodeDecodeError:
            raise TamperError(f"run-{index}.exit is not ASCII")
        if not EXIT_FILE_RE.fullmatch(exit_text):
            raise TamperError(f"run-{index}.exit is not '<code>\\n' or 'unavailable\\n'")
        records.append(
            {
                "available": exit_text.strip() != "unavailable",
                "exit_text": exit_text.strip(),
                "stdout": stdout_bytes,
                "stderr": stderr_bytes,
            }
        )
    finding = classify(records)
    return finding, EXIT_BY_ID[finding]


def snapshot_mode(dirpath):
    emit(f"REPEAT_CONTROL_TOOL {VERSION} tool-sha256={tool_sha256()}")
    if not os.path.isdir(dirpath):
        return usage_failure(f"--snapshot DIR is not a directory: {dirpath}")
    try:
        record = load_snapshot(dirpath)
        observed = recompute_snapshot(dirpath, record)
    except TamperError as exc:
        emit(f"SNAPSHOT_TAMPER {exc}")
        return finish("snapshot_tampered")
    emit(f"SNAPSHOT_INPUTS {len(record['inputs'])} verified")
    emit(f"SNAPSHOT_EXPECTED id={record['expected_id']} exit={record['expected_exit']}")
    emit(f"SNAPSHOT_OBSERVED id={observed[0]} exit={observed[1]}")
    if observed == (record["expected_id"], record["expected_exit"]):
        return finish(record["expected_id"])
    return finish(
        "controls_mismatch",
        message=(
            "repeat-control: snapshot expectation not reproduced: "
            f"expected={record['expected_id']}/{record['expected_exit']} "
            f"observed={observed[0]}/{observed[1]}"
        ),
    )


# ------------------------------------------------------------------- selftest

STABLE_SH = """#!/usr/bin/env bash
# repeat-control --selftest fixture: stable control. Fixed bytes on both
# streams, including CRLF and non-UTF8 bytes, exit 0.
printf 'stable-out\\r\\n\\xff\\xfe\\n'
printf 'stable-err\\r\\n\\xff\\n' >&2
exit 0
"""

MISMATCH_STDOUT_SH = """#!/usr/bin/env bash
# every run prints a different value (counter file in the caller's cwd)
n=$(cat state-mismatch-stdout 2>/dev/null || printf '0')
printf '%s\\n' "$((n + 1))" > state-mismatch-stdout
printf 'value-%s\\n' "$n"
"""

MISMATCH_RUN3_SH = """#!/usr/bin/env bash
# runs 1 and 2 print 'same', run 3 prints 'different' -- a gate that only
# compares the first two runs would false-pass
n=$(cat state-mismatch-run3 2>/dev/null || printf '0')
printf '%s\\n' "$((n + 1))" > state-mismatch-run3
if [ "$n" -lt 2 ]; then printf 'same\\n'; else printf 'different\\n'; fi
"""

MISMATCH_NEWLINE_SH = """#!/usr/bin/env bash
# run 1 prints 'x', later runs print 'x\\n' -- the only difference is the
# trailing newline, so a gate that normalizes newlines would false-pass
n=$(cat state-mismatch-newline 2>/dev/null || printf '0')
printf '%s\\n' "$((n + 1))" > state-mismatch-newline
if [ "$n" -eq 0 ]; then printf 'x'; else printf 'x\\n'; fi
"""

MISMATCH_STDERR_SH = """#!/usr/bin/env bash
# stdout identical on every run, stderr differs per run
n=$(cat state-mismatch-stderr 2>/dev/null || printf '0')
printf '%s\\n' "$((n + 1))" > state-mismatch-stderr
printf 'err-%s\\n' "$n" >&2
printf 'same-stdout\\n'
"""

MISMATCH_EXIT_SH = """#!/usr/bin/env bash
# exits 0, 0, 1 with identical stdout -- a nonzero exit must not shadow the
# disagreement
n=$(cat state-mismatch-exit 2>/dev/null || printf '0')
printf '%s\\n' "$((n + 1))" > state-mismatch-exit
printf 'same-stdout\\n'
if [ "$n" -lt 2 ]; then exit 0; else exit 1; fi
"""

MISMATCH_NONZERO_EXITS_SH = """#!/usr/bin/env bash
# exits 1, 2, 1 with identical stdout/stderr -- disagreement is decided
# before the nonzero baseline, so a differing nonzero tuple is controls_mismatch
n=$(cat state-mismatch-nonzero-exits 2>/dev/null || printf '0')
printf '%s\\n' "$((n + 1))" > state-mismatch-nonzero-exits
printf 'same-stdout\\n'
if [ "$n" -eq 1 ]; then exit 2; else exit 1; fi
"""

NONZERO_SH = """#!/usr/bin/env bash
# stable nonzero baseline, identical bytes on every run
printf 'nonzero-out\\n'
exit 7
"""

CHILD127_SH = """#!/usr/bin/env bash
# stable 127 (a wrapper's command-not-found) is still a nonzero baseline,
# not command_unavailable
printf 'child127-out\\n'
exit 127
"""

SELFTEST_FIXTURES = {
    "stable.sh": STABLE_SH,
    "mismatch-stdout.sh": MISMATCH_STDOUT_SH,
    "mismatch-run3.sh": MISMATCH_RUN3_SH,
    "mismatch-newline.sh": MISMATCH_NEWLINE_SH,
    "mismatch-stderr.sh": MISMATCH_STDERR_SH,
    "mismatch-exit.sh": MISMATCH_EXIT_SH,
    "mismatch-nonzero-exits.sh": MISMATCH_NONZERO_EXITS_SH,
    "nonzero.sh": NONZERO_SH,
    "child127.sh": CHILD127_SH,
}


def last_finding_id(stdout_bytes):
    last = ""
    for line in stdout_bytes.decode("utf-8", "replace").splitlines():
        if line.strip():
            last = line.strip()
    prefix = "REPEAT_CONTROL: "
    if last.startswith(prefix):
        return last[len(prefix):]
    return f"<{last}>"


def write_snapshot(dirpath, runs, observations, expected_id):
    """Author a snapshot directory: observations plus a record hashing each."""
    os.makedirs(dirpath)
    inputs = {}
    for index, (stdout_bytes, stderr_bytes, exit_bytes) in enumerate(observations, start=1):
        for suffix, data in (("stdout", stdout_bytes), ("stderr", stderr_bytes), ("exit", exit_bytes)):
            name = f"run-{index}.{suffix}"
            write_new(os.path.join(dirpath, name), data)
            inputs[name] = sha256_bytes(data)
    record = {
        "schema": SNAPSHOT_SCHEMA,
        "runs": runs,
        "expected_id": expected_id,
        "expected_exit": EXIT_BY_ID[expected_id],
        "inputs": inputs,
    }
    write_new(
        os.path.join(dirpath, "expected.json"),
        (json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )


def selftest():
    root = EVIDENCE_ROOT
    if not os.path.isdir(root):
        emit(f"SELFTEST: COULD_NOT_EVALUATE (committed fixture root missing or not a directory: {root})")
        return 2
    scratch = tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=strict_scratch_root())
    passed = 0
    failed = []

    def record_case(name, ok, detail):
        nonlocal passed
        if ok:
            passed += 1
            emit(f"SELFTEST_CASE {name} PASS ({detail})")
        else:
            failed.append(name)
            emit(f"SELFTEST_CASE {name} FAIL ({detail})")

    def run_child(args, stdin_bytes=None):
        kwargs = {"input": stdin_bytes} if stdin_bytes is not None else {"stdin": subprocess.DEVNULL}
        return subprocess.run(
            [sys.executable, SELF] + args,
            cwd=scratch,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **kwargs,
        )

    def fresh_out(name):
        out_dir = os.path.join(scratch, "out", name)
        os.makedirs(os.path.dirname(out_dir), exist_ok=True)
        return out_dir

    def cli_case(name, args, expect_id, expect_exit, stdin_bytes=None, checks=()):
        proc = run_child(args, stdin_bytes=stdin_bytes)
        observed = last_finding_id(proc.stdout)
        ok = proc.returncode == expect_exit and observed == expect_id
        detail = f"expected={expect_id}/{expect_exit} observed={observed}/{proc.returncode}"
        for check in checks:
            check_ok, check_detail = check(proc)
            ok = ok and check_ok
            detail += f" {check_detail}"
        record_case(name, ok, detail)

    def snapshot_case(name, dirpath, expect_id, expect_exit):
        proc = run_child(["--snapshot", dirpath])
        observed = last_finding_id(proc.stdout)
        record_case(
            name,
            proc.returncode == expect_exit and observed == expect_id,
            f"expected={expect_id}/{expect_exit} observed={observed}/{proc.returncode}",
        )

    def check_saved_bytes(proc):
        direct = subprocess.run(
            ["bash", "fixtures/stable.sh"],
            cwd=scratch,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out_dir = os.path.join(scratch, "out", "stable.sh")
        notes = []
        for index in (1, 2, 3):
            stdout_bytes = read_bytes(os.path.join(out_dir, f"run-{index}.stdout"))
            stderr_bytes = read_bytes(os.path.join(out_dir, f"run-{index}.stderr"))
            exit_bytes = read_bytes(os.path.join(out_dir, f"run-{index}.exit"))
            if stdout_bytes != direct.stdout:
                notes.append(f"run-{index}.stdout!=direct")
            if stderr_bytes != direct.stderr:
                notes.append(f"run-{index}.stderr!=direct")
            if exit_bytes != b"0\n":
                notes.append(f"run-{index}.exit!='0\\n'")
        if notes:
            return False, "saved-bytes:" + ",".join(notes)
        return True, "saved-bytes-ok"

    def check_stdin_isolated(proc):
        out_dir = os.path.join(scratch, "out", "stdin-devnull")
        stdout_bytes = read_bytes(os.path.join(out_dir, "run-1.stdout"))
        if stdout_bytes != b"":
            return False, f"stdin-leak:{stdout_bytes!r}"
        return True, "stdin-devnull-ok"

    def check_existing_out_untouched(proc):
        out_dir = os.path.join(scratch, "out", "existing-out")
        entries = sorted(os.listdir(out_dir))
        if entries:
            return False, f"refused-out-modified:{entries}"
        return True, "refused-out-untouched"

    try:
        fixtures = os.path.join(scratch, "fixtures")
        os.makedirs(fixtures)
        for name, body in SELFTEST_FIXTURES.items():
            write_new(os.path.join(fixtures, name), body.encode("utf-8"))
        noexec = os.path.join(scratch, "noexec.txt")
        write_new(noexec, b"not executable\n")
        os.chmod(noexec, 0o644)
        noshebang = os.path.join(scratch, "noshebang")
        write_new(noshebang, b"not an executable format\n")
        os.chmod(noshebang, 0o755)

        def fixture_args(name):
            return ["--runs", "3", "--out", fresh_out(name), "--", "bash", f"fixtures/{name}"]

        cli_case("stable", fixture_args("stable.sh"), "controls_match", 0, checks=(check_saved_bytes,))
        cli_case("mismatch-stdout", fixture_args("mismatch-stdout.sh"), "controls_mismatch", 1)
        cli_case("mismatch-run3-only", fixture_args("mismatch-run3.sh"), "controls_mismatch", 1)
        cli_case("mismatch-newline-only", fixture_args("mismatch-newline.sh"), "controls_mismatch", 1)
        cli_case("mismatch-stderr", fixture_args("mismatch-stderr.sh"), "controls_mismatch", 1)
        cli_case("mismatch-exit", fixture_args("mismatch-exit.sh"), "controls_mismatch", 1)
        cli_case(
            "mismatch-nonzero-exits",
            fixture_args("mismatch-nonzero-exits.sh"),
            "controls_mismatch",
            1,
        )
        cli_case("nonzero-baseline", fixture_args("nonzero.sh"), "baseline_nonzero", 2)
        cli_case("child127-baseline", fixture_args("child127.sh"), "baseline_nonzero", 2)
        cli_case(
            "command-unavailable-enoent",
            ["--runs", "3", "--out", fresh_out("command-unavailable-enoent"), "--", "tameshi-r12-no-such-command"],
            "command_unavailable",
            2,
        )
        cli_case(
            "command-unavailable-eacces",
            ["--runs", "3", "--out", fresh_out("command-unavailable-eacces"), "--", noexec],
            "command_unavailable",
            2,
        )
        cli_case(
            "command-unavailable-enoexec",
            ["--runs", "3", "--out", fresh_out("command-unavailable-enoexec"), "--", noshebang],
            "command_unavailable",
            2,
        )
        for name, runs_arg in (
            ("invalid-runs-2", "2"),
            ("invalid-runs-1", "1"),
            ("invalid-runs-0", "0"),
            ("invalid-runs-abc", "abc"),
        ):
            cli_case(
                name,
                ["--runs", runs_arg, "--out", fresh_out(name), "--", "bash", "fixtures/stable.sh"],
                "invalid_usage",
                64,
            )
        cli_case(
            "invalid-missing-separator",
            ["--runs", "3", "--out", fresh_out("invalid-missing-separator"), "bash", "fixtures/stable.sh"],
            "invalid_usage",
            64,
        )
        existing_out = fresh_out("existing-out")
        os.makedirs(existing_out)
        cli_case(
            "invalid-existing-out",
            ["--runs", "3", "--out", existing_out, "--", "bash", "fixtures/stable.sh"],
            "invalid_usage",
            64,
            checks=(check_existing_out_untouched,),
        )
        cli_case(
            "stdin-devnull",
            ["--runs", "3", "--out", fresh_out("stdin-devnull"), "--", "cat"],
            "controls_match",
            0,
            stdin_bytes=b"fed-through-stdin\n",
            checks=(check_stdin_isolated,),
        )

        snap_stable = os.path.join(scratch, "snap-stable")
        write_snapshot(
            snap_stable,
            3,
            [(b"stable-out\n", b"stable-err\n", b"0\n")] * 3,
            "controls_match",
        )
        snap_mismatch = os.path.join(scratch, "snap-mismatch")
        write_snapshot(
            snap_mismatch,
            3,
            [
                (b"one\n", b"e\n", b"0\n"),
                (b"one\n", b"e\n", b"0\n"),
                (b"two\n", b"e\n", b"0\n"),
            ],
            "controls_mismatch",
        )
        snapshot_case("snapshot-pass", snap_stable, "controls_match", 0)
        snapshot_case("snapshot-mismatch-pass", snap_mismatch, "controls_mismatch", 1)

        tamper_byte = os.path.join(scratch, "snap-tamper-byte")
        shutil.copytree(snap_stable, tamper_byte)
        target = os.path.join(tamper_byte, "run-1.stdout")
        data = bytearray(read_bytes(target))
        data[0] = data[0] ^ 0x01
        with open(target, "wb") as handle:
            handle.write(bytes(data))
        snapshot_case("snapshot-tamper-byte", tamper_byte, "snapshot_tampered", 2)

        tamper_missing = os.path.join(scratch, "snap-tamper-missing")
        shutil.copytree(snap_stable, tamper_missing)
        os.remove(os.path.join(tamper_missing, "run-2.stderr"))
        snapshot_case("snapshot-tamper-missing", tamper_missing, "snapshot_tampered", 2)

        tamper_unlisted = os.path.join(scratch, "snap-tamper-unlisted")
        shutil.copytree(snap_stable, tamper_unlisted)
        write_new(os.path.join(tamper_unlisted, "run-4.stdout"), b"extra\n")
        snapshot_case("snapshot-tamper-unlisted", tamper_unlisted, "snapshot_tampered", 2)

        tamper_duplicate_key = os.path.join(scratch, "snap-tamper-duplicate-key")
        shutil.copytree(snap_stable, tamper_duplicate_key)
        duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")
        record_text = read_bytes(duplicate_path).decode("utf-8")
        marker = '  "inputs": {'
        with open(duplicate_path, "wb") as handle:
            handle.write(
                record_text.replace(marker, '  "inputs": {},\n' + marker, 1).encode("utf-8")
            )
        snapshot_case("snapshot-tamper-duplicate-key", tamper_duplicate_key, "snapshot_tampered", 2)

        tamper_manifest_symlink = os.path.join(scratch, "snap-tamper-manifest-symlink")
        shutil.copytree(snap_stable, tamper_manifest_symlink)
        os.remove(os.path.join(tamper_manifest_symlink, "expected.json"))
        os.symlink(
            os.path.join(snap_stable, "expected.json"),
            os.path.join(tamper_manifest_symlink, "expected.json"),
        )
        snapshot_case(
            "snapshot-tamper-manifest-symlink",
            tamper_manifest_symlink,
            "snapshot_tampered",
            2,
        )

        tamper_observation_symlink = os.path.join(scratch, "snap-tamper-observation-symlink")
        shutil.copytree(snap_stable, tamper_observation_symlink)
        os.remove(os.path.join(tamper_observation_symlink, "run-1.stdout"))
        os.symlink(
            "run-2.stdout",
            os.path.join(tamper_observation_symlink, "run-1.stdout"),
        )
        snapshot_case(
            "snapshot-tamper-observation-symlink",
            tamper_observation_symlink,
            "snapshot_tampered",
            2,
        )

        snapshot_case("snapshot-committed-stable", root, "controls_match", 0)
        snapshot_case(
            "snapshot-committed-mismatch",
            os.path.join(root, "mismatch"),
            "controls_mismatch",
            1,
        )

        total = passed + len(failed)
        if failed:
            emit(f"SELFTEST: FAIL ({len(failed)} of {total} cases failed: {','.join(failed)})")
            emit(f"SELFTEST_SCRATCH {scratch}")
            return 1
        emit(f"SELFTEST: PASS ({total} cases)")
        shutil.rmtree(scratch, ignore_errors=True)
        return 0
    except Exception as exc:  # noqa: BLE001 - a selftest crash is could-not-evaluate
        emit(f"SELFTEST: COULD_NOT_EVALUATE ({type(exc).__name__}: {exc})")
        emit(f"SELFTEST_SCRATCH {scratch}")
        return 2


# ----------------------------------------------------------------------- main


def dispatch(argv):
    if not argv:
        return usage_failure("no arguments")
    head = argv[0]
    if head == "--selftest":
        if len(argv) != 1:
            return usage_failure("--selftest takes no further arguments")
        return selftest()
    if head == "--snapshot":
        if len(argv) != 2:
            return usage_failure("--snapshot requires exactly one DIR")
        return snapshot_mode(argv[1])
    if head in ("-h", "--help"):
        if len(argv) != 1:
            return usage_failure(f"{head} takes no further arguments")
        emit(USAGE.rstrip("\n"))
        return 0
    return run_mode(argv)


def main(argv):
    try:
        status = dispatch(argv)
    except ScratchRootUnusable as exc:
        emit_err(f"repeat-control: could-not-evaluate: {exc}")
        emit("REPEAT_CONTROL: setup_error")
        status = EXIT_BY_ID["setup_error"]
    except Exception as exc:  # noqa: BLE001 - never let a traceback exit 1
        status = setup_failure(f"{type(exc).__name__}: {exc}")
    # A terminal that refused output must not change the class at shutdown:
    # CPython turns a failed final stdout/stderr flush into exit 120, so swap
    # any refusing stream for /dev/null before the interpreter reaches it.
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name)
        if stream is None:
            continue
        try:
            stream.flush()
        except (OSError, ValueError):
            try:
                setattr(sys, name, open(os.devnull, "w"))
            except OSError:
                pass
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
