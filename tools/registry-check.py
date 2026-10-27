#!/usr/bin/env python3
"""registry-check.py — entry-registry monitor (tameshi-shokunin, round 17).

Operability repair (R16-MON1): the lane's registered entry commands are the
contract surface a cold read runs against; this monitor replays every active
row of `tools/registry.json` and reports how many rows still return their
registered outcome.

Interface (round-17 contract B, hardened in wave 1 follow-up):

    python3 tools/registry-check.py [--root DIR] [--rev REV] \
        [--registry PATH] [--only NAME] [--tag TAG]... [--json]
    python3 tools/registry-check.py --selftest

Registry schema `tameshi-entry-registry-v1` (tools/registry.json):

    {"schema": "tameshi-entry-registry-v1",
     "rows": [{"name": "<unique, ^[a-z0-9][a-z0-9-]*$>",
               "kind": "gate|probe|selftest",
               "argv": ["<program>", "<arg>", ...],   # exec'd directly, no shell
               "expect": {"exit": <int>,
                          "stdout_contains": ["<needle>", ...]},   # optional
               "timeout_s": <positive number>,
               "source": "<file>@<7-40 hex rev>:<line>[-<line>]",
               "status": "active|superseded",
               "superseded_by": "<name of an existing active row>",
               "tags": ["<tag>", ...]},                # optional
              ...]}

Run semantics: every active row and every superseded row RUNS, with
cwd = the lane root (or the clone root under --rev), stdin /dev/null,
shell=False, in a scrubbed environment (every inherited `GIT_*` variable is
removed; `PYTHONDONTWRITEBYTECODE=1` is added). Superseded rows still execute
so their observed outcome stays visible; they are excluded from N/M and
counted in `superseded=K`. A row holds when its exit equals expect.exit AND
every stdout_contains needle appears in stdout (literal, case-sensitive,
ANDed, over the retained tail) AND, under --rev, its argv names no absolute
path under the live fleet root (`non_hermetic_argv`).
On Linux, timeout cleanup marks this process as a child subreaper before rows
start, then signals only row-owned `/proc` identities through pidfds after
rechecking start time and ancestry. Process-group changes do not affect this
walk; a double-forked descendant cannot reparent past the subreaper. Descendants
that change UID may become unreadable or unkillable, and start-time granularity
leaves a same-tick PID-reuse residual.

Per-row lines and trailer (fixed):

    ROW <name> expect=<exit> got=<exit|timeout|unavailable|non-hermetic> held|differs
    ROW <name> superseded expect=<exit> got=<exit|...>
    REGISTRY_CHECK: held=<N>/<M> superseded=<K>

Exits: 0 all held · 1 any differs · 2 could-not-evaluate (registry
unreadable/invalid, root or rev missing, clone failure, --only/--tag miss) ·
64 usage.

--root DIR   lane to run against; default: the lane containing this script
             (the parent of tools/). Live mode prints a stderr warning that
             rows may write into the root; prefer --rev.
--rev REV    resolve REV^{commit} in the source lane, clone it into a
             fleet-mirror layout and run there: a mkdtemp fleet/ holds a
             symlink per `*-shokunin` sibling of the lane (the lane itself
             excluded) plus a `git clone` checked out detached at the resolved
             sha, matching the wave sandbox layout so tools that resolve
             sibling lanes still work. The commit actually graded is reported
             as `rev_resolved`. The mkdtemp is removed afterwards.
--registry PATH  registry file to grade; resolved against the caller's cwd.
             With --rev this grades the old rev against a newer registry
             (e.g. the live tree's); omit it to use the clone's own
             tools/registry.json.
--only NAME  run exactly the named row (any status); a tag filter that
             excludes it is an evaluation error, not an empty pass.
--tag TAG    select rows carrying any of the given tags (repeatable);
             `superseded_by` targets resolve against the full registry.
--json       machine report on stdout (schema
             `tameshi-registry-check-report-v1`, additive fields:
             registry_sha256, rev_resolved, per-row stdout/stderr tails); the
             human ROW/REGISTRY_CHECK lines move to stderr.
--selftest   hermetic; fixtures only under the scratch root (TMPDIR), never touches the lane; its
             own git calls use the same scrubbed environment (a decoy
             GIT_DIR must not move any fixture or canary HEAD).

Dependencies: python3 stdlib; git only for --rev (and --selftest's fixtures).
"""

import ctypes
import hashlib
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

SELF = os.path.abspath(__file__)
SCHEMA = "tameshi-entry-registry-v1"
REPORT_SCHEMA = "tameshi-registry-check-report-v1"
KINDS = frozenset({"gate", "probe", "selftest"})
STATUSES = frozenset({"active", "superseded"})
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
# Round-18 wave-2 fix (ReviewSkillDiff F1): a finite timeout of 2147484 s or more
# overflows Popen.communicate()'s C timeout and crashed with exit 1 (a row
# "differs"), so the registry caps it; one day is far above any row's need.
MAX_TIMEOUT_S = 86400
SOURCE_RE = re.compile(r"^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
TAIL_BYTES = 4096
CHILD_SUBREAPER_PRCTL = 36
CLEANUP_TERM_GRACE_S = 0.2
CLEANUP_FORCE_TIMEOUT_S = 0.5
PIPE_DRAIN_TIMEOUT_S = 0.5
_CHILD_SUBREAPER_ENABLED = False

USAGE = (
    "usage: registry-check.py [--root DIR] [--rev REV] [--registry PATH]\n"
    "                          [--only NAME] [--tag TAG]... [--json]\n"
    "       registry-check.py --selftest\n"
)


def emit(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def emit_err(text):
    sys.stderr.write(text + "\n")
    sys.stderr.flush()


def usage_failure(detail=None):
    if detail:
        emit_err(f"registry-check: {detail}")
    emit_err(USAGE.rstrip("\n"))
    return 64


def default_root():
    # tools/registry-check.py -> lane root is the parent of tools/.
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# --------------------------------------------------------------- environment


def git_env():
    """Inherited GIT_* is scrubbed; config, locks and prompts are disabled."""
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("GIT_")
    }
    env.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_PAGER": "cat",
            "LC_ALL": "C",
        }
    )
    return env


def row_env():
    """Rows get the scrubbed git environment plus no bytecode writing."""
    env = git_env()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


# ------------------------------------------------------------------ registry


def registry_errors(data):
    """Return a list of schema violations; empty means a valid registry."""
    errors = []
    if not isinstance(data, dict):
        return ["registry top level is not an object"]
    if data.get("schema") != SCHEMA:
        errors.append(
            f"schema must be {SCHEMA!r}, got {data.get('schema')!r}"
        )
    rows = data.get("rows")
    if not isinstance(rows, list):
        errors.append("rows must be a list")
        return errors
    seen = set()
    for i, row in enumerate(rows):
        where = f"rows[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{where} is not an object")
            continue
        name = row.get("name")
        if not isinstance(name, str) or not NAME_RE.match(name):
            errors.append(
                f"{where}.name must match ^[a-z0-9][a-z0-9-]*$, "
                f"got {name!r}"
            )
        elif name in seen:
            errors.append(f"{where}.name {name!r} is duplicated")
        else:
            seen.add(name)
        if row.get("kind") not in KINDS:
            errors.append(
                f"{where}.kind must be one of {sorted(KINDS)}, "
                f"got {row.get('kind')!r}"
            )
        argv = row.get("argv")
        if (
            not isinstance(argv, list)
            or not argv
            or any(not isinstance(a, str) or not a for a in argv)
        ):
            errors.append(
                f"{where}.argv must be a non-empty list of non-empty "
                "strings (no shell string)"
            )
        expect = row.get("expect")
        if not isinstance(expect, dict):
            errors.append(f"{where}.expect must be an object")
        else:
            ex = expect.get("exit")
            if isinstance(ex, bool) or not isinstance(ex, int):
                errors.append(f"{where}.expect.exit must be an integer")
            needles = expect.get("stdout_contains", [])
            if not isinstance(needles, list) or any(
                not isinstance(n, str) for n in needles
            ):
                errors.append(
                    f"{where}.expect.stdout_contains must be a list of strings"
                )
        ts = row.get("timeout_s")
        timeout_valid = (
            not isinstance(ts, bool) and isinstance(ts, (int, float))
        )
        if timeout_valid:
            try:
                timeout_valid = (
                    math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S
                )
            except OverflowError:
                timeout_valid = False
        if not timeout_valid:
            timeout_owner = (
                f"{where} ({name!r})" if isinstance(name, str) else where
            )
            errors.append(
                f"{timeout_owner}.timeout_s must be a finite positive number"
                f" <= {MAX_TIMEOUT_S}"
            )
        source = row.get("source")
        if not isinstance(source, str) or not SOURCE_RE.match(source):
            errors.append(
                f"{where}.source must be <file>@<7-40 hex rev>:<line>, "
                f"got {source!r}"
            )
        status = row.get("status")
        if status not in STATUSES:
            errors.append(
                f"{where}.status must be one of {sorted(STATUSES)}, "
                f"got {status!r}"
            )
        tags = row.get("tags", [])
        if not isinstance(tags, list) or any(
            not isinstance(t, str) or not t for t in tags
        ):
            errors.append(f"{where}.tags must be a list of non-empty strings")
        for flag in ("external", "discriminating"):
            if flag in row and not isinstance(row[flag], bool):
                errors.append(f"{where}.{flag} must be a boolean")
    # Second pass: superseded_by must name an existing ACTIVE row.
    by_name = {
        row["name"]: row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("name"), str)
    }
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("status") != "superseded":
            continue
        target = row.get("superseded_by")
        if not isinstance(target, str) or not target:
            errors.append(
                f"rows[{i}].superseded_by is required for status superseded"
            )
        elif target not in by_name:
            errors.append(
                f"rows[{i}].superseded_by {target!r} names no registry row"
            )
        elif by_name[target].get("status") != "active":
            errors.append(
                f"rows[{i}].superseded_by {target!r} is not an active row"
            )
    return errors


class _NonFiniteJSONConstant(ValueError):
    def __init__(self, constant):
        self.constant = constant
        super().__init__(f"non-finite JSON number {constant}")


def _reject_json_constant(constant):
    raise _NonFiniteJSONConstant(constant)


def _json_marker_path(value, marker, path):
    if value is marker:
        return path
    if isinstance(value, dict):
        for key, child in value.items():
            found = _json_marker_path(child, marker, f"{path}.{key}")
            if found is not None:
                return found
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found = _json_marker_path(child, marker, f"{path}[{index}]")
            if found is not None:
                return found
    return None


def _nonfinite_location(text, marker):
    """Locate a rejected constant in a row for a useful validation error."""
    try:
        data = json.loads(text, parse_constant=lambda _constant: marker)
    except ValueError:
        return None
    rows = data.get("rows") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        return None
    for index, row in enumerate(rows):
        path = _json_marker_path(row, marker, f"rows[{index}]")
        if path is None:
            continue
        if isinstance(row, dict) and isinstance(row.get("name"), str):
            return f"{path} (row {row['name']!r})"
        return path
    return None


def load_registry(path):
    """Return (rows, data, error). error is a string on could-not-evaluate."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        return None, None, f"registry unreadable: {path}: {exc}"
    try:
        text = raw.decode("utf-8")
        data = json.loads(text, parse_constant=_reject_json_constant)
    except _NonFiniteJSONConstant as exc:
        marker = object()
        location = _nonfinite_location(text, marker)
        where = f"{location}: " if location else ""
        return (
            None,
            None,
            f"registry invalid: {path}: {where}"
            f"non-finite JSON number {exc.constant}",
        )
    except (UnicodeDecodeError, ValueError) as exc:
        return None, None, f"registry invalid: {path}: {exc}"
    errors = registry_errors(data)
    if errors:
        return None, None, "registry invalid: " + "; ".join(errors)
    return data["rows"], data, None


def registry_sha256(path):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


# ------------------------------------------------------------------ run rows


def _tail(raw):
    """Decode the retained tail of a byte stream (bounded report)."""
    return raw[-TAIL_BYTES:].decode("utf-8", errors="replace")


def _enable_child_subreaper():
    """Require Linux subreaper and pidfd support before starting any row."""
    global _CHILD_SUBREAPER_ENABLED
    if _CHILD_SUBREAPER_ENABLED:
        return
    if sys.platform != "linux":
        raise OSError("descendant cleanup requires Linux child-subreaper support")
    if not hasattr(os, "pidfd_open") or not hasattr(signal, "pidfd_send_signal"):
        raise OSError("descendant cleanup requires pidfd support")
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        prctl = libc.prctl
    except AttributeError as exc:
        raise OSError("prctl is unavailable") from exc
    prctl.argtypes = [
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
    ]
    prctl.restype = ctypes.c_int
    if prctl(CHILD_SUBREAPER_PRCTL, 1, 0, 0, 0) != 0:
        error = ctypes.get_errno() or 1
        raise OSError(error, os.strerror(error))
    _CHILD_SUBREAPER_ENABLED = True


def _read_proc_stat(pid):
    """Return (ppid, starttime, state) for one Linux process leader."""
    try:
        with open(f"/proc/{pid}/stat", encoding="ascii", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return None
    close = text.rfind(")")
    if close < 0:
        return None
    fields = text[close + 1:].split()
    if len(fields) <= 19:
        return None
    try:
        return int(fields[1]), int(fields[19]), fields[0]
    except ValueError:
        return None


def _process_snapshot():
    """Read process leaders only; `/proc/<pid>/task` threads are not targets."""
    processes = {}
    try:
        entries = os.scandir("/proc")
    except OSError:
        return processes
    with entries:
        for entry in entries:
            if not entry.name.isdecimal():
                continue
            pid = int(entry.name)
            stat = _read_proc_stat(pid)
            if stat is not None:
                processes[pid] = stat
    return processes


def _direct_child_identities():
    """Snapshot pre-existing children so cleanup never claims another row."""
    processes = _process_snapshot()
    if os.getpid() not in processes:
        raise OSError("cannot inspect the checker in /proc")
    return frozenset(
        (pid, starttime)
        for pid, (ppid, starttime, _state) in processes.items()
        if ppid == os.getpid()
    )


def _row_identity_is_owned(pid, starttime, proc_pid, proc_starttime,
                           baseline_children):
    """Check current ancestry back to this row or a newly adopted row child."""
    current = pid
    seen = set()
    while current not in seen:
        seen.add(current)
        stat = _read_proc_stat(current)
        if stat is None:
            return False
        ppid, observed_starttime, _state = stat
        if current == pid and observed_starttime != starttime:
            return False
        if current == proc_pid:
            return (
                proc_starttime is not None
                and observed_starttime == proc_starttime
            )
        if ppid == os.getpid():
            return (current, observed_starttime) not in baseline_children
        current = ppid
    return False


def _row_owned_processes(proc, baseline_children, proc_starttime):
    """Find this row's live and zombie process identities, excluding siblings."""
    owned = []
    for pid, (_ppid, starttime, state) in _process_snapshot().items():
        if _row_identity_is_owned(
            pid, starttime, proc.pid, proc_starttime, baseline_children
        ):
            owned.append((pid, starttime, state))
    return owned


def _signal_process_identity(pid, starttime, signum, in_row_scope,
                             read_stat=None):
    """Signal one process only after start-time and ownership revalidation."""
    if read_stat is None:
        read_stat = _read_proc_stat
    stat = read_stat(pid)
    if stat is None or stat[1] != starttime or not in_row_scope():
        return False
    try:
        pidfd = os.pidfd_open(pid, 0)
    except OSError:
        return False
    try:
        stat = read_stat(pid)
        if stat is None or stat[1] != starttime or not in_row_scope():
            return False
        signal.pidfd_send_signal(pidfd, signum)
        return True
    except OSError:
        return False
    finally:
        os.close(pidfd)


def _signal_row_processes(proc, baseline_children, proc_starttime, signum):
    for pid, starttime, state in _row_owned_processes(
        proc, baseline_children, proc_starttime
    ):
        if state == "Z":
            continue
        in_row_scope = lambda pid=pid, starttime=starttime: (
            _row_identity_is_owned(
                pid, starttime, proc.pid, proc_starttime, baseline_children
            )
        )
        _signal_process_identity(pid, starttime, signum, in_row_scope)


def _reap_row_children(proc, baseline_children, proc_starttime):
    """Reap only zombie children adopted from the current row."""
    for pid, starttime, state in _row_owned_processes(
        proc, baseline_children, proc_starttime
    ):
        if pid == proc.pid or state != "Z":
            continue
        stat = _read_proc_stat(pid)
        if (
            stat is None
            or stat[0] != os.getpid()
            or stat[1] != starttime
            or not _row_identity_is_owned(
                pid, starttime, proc.pid, proc_starttime, baseline_children
            )
        ):
            continue
        try:
            os.waitpid(pid, os.WNOHANG)
        except (ChildProcessError, ProcessLookupError):
            pass


def _row_cleanup_pending(proc, baseline_children, proc_starttime):
    for pid, starttime, state in _row_owned_processes(
        proc, baseline_children, proc_starttime
    ):
        if state != "Z":
            return True
        if pid != proc.pid:
            stat = _read_proc_stat(pid)
            if stat is not None and stat[0] == os.getpid():
                return True
    return False


def _cleanup_row(proc, baseline_children, proc_starttime):
    """Boundedly terminate and reap all visible process descendants of a row."""
    term_deadline = time.monotonic() + CLEANUP_TERM_GRACE_S
    while True:
        _signal_row_processes(
            proc, baseline_children, proc_starttime, signal.SIGTERM
        )
        try:
            proc.wait(timeout=0)
        except subprocess.TimeoutExpired:
            pass
        _reap_row_children(proc, baseline_children, proc_starttime)
        if not _row_cleanup_pending(proc, baseline_children, proc_starttime):
            return True
        if time.monotonic() >= term_deadline:
            break
        time.sleep(0.01)

    kill_deadline = time.monotonic() + CLEANUP_FORCE_TIMEOUT_S
    while True:
        _signal_row_processes(
            proc, baseline_children, proc_starttime, signal.SIGKILL
        )
        try:
            proc.wait(timeout=0)
        except subprocess.TimeoutExpired:
            pass
        _reap_row_children(proc, baseline_children, proc_starttime)
        if not _row_cleanup_pending(proc, baseline_children, proc_starttime):
            return True
        if time.monotonic() >= kill_deadline:
            return False
        time.sleep(0.01)


def _bounded_communicate(proc, previous_timeout=None):
    """Drain output under a bound even if an escaped descendant holds a pipe."""
    try:
        return proc.communicate(timeout=PIPE_DRAIN_TIMEOUT_S)
    except subprocess.TimeoutExpired as exc:
        stdout_raw = exc.output
        stderr_raw = exc.stderr
        if previous_timeout is not None:
            stdout_raw = stdout_raw or previous_timeout.output
            stderr_raw = stderr_raw or previous_timeout.stderr
        for stream in (proc.stdout, proc.stderr):
            if stream is not None:
                stream.close()
        try:
            proc.wait(timeout=PIPE_DRAIN_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            pass
        return stdout_raw or b"", stderr_raw or b""


def _argv_outside_fleet(argv, fleet_root):
    """Absolute argv paths under the live fleet root defeat a --rev clone."""
    hits = []
    if not fleet_root:
        return hits
    prefix = fleet_root.rstrip(os.sep) + os.sep
    for token in argv:
        if "=" in token:
            token = token.split("=", 1)[1]
        if os.path.isabs(token) and (
            token == fleet_root or token.startswith(prefix)
        ):
            hits.append(token)
    return hits


def run_row(row, cwd, fleet_root=None, retain_streams=False):
    """Execute one registry row; optionally retain complete streams for replay."""
    expect = row["expect"]
    expected_exit = expect["exit"]
    needles = expect.get("stdout_contains", [])
    fragment = {
        "name": row["name"],
        "kind": row["kind"],
        "status": row["status"],
        "expect": expected_exit,
        "tags": list(row.get("tags", [])),
    }
    if row["status"] == "superseded":
        fragment["superseded_by"] = row["superseded_by"]
    outside = _argv_outside_fleet(row["argv"], fleet_root)
    if outside:
        # K04 P7: rows that depend on outside state must declare it; an
        # undeclared absolute live-fleet token is not a hermetic reproduction.
        if not row.get("external"):
            fragment["got"] = "non-hermetic"
            fragment["held"] = False
            fragment["non_hermetic_argv"] = outside
            return fragment
        fragment["non_hermetic_argv"] = outside
    started = time.monotonic()
    try:
        _enable_child_subreaper()
        baseline_children = _direct_child_identities()
        proc = subprocess.Popen(
            row["argv"],
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=row_env(),
            start_new_session=True,
        )
    except OSError as exc:
        fragment["got"] = "unavailable"
        fragment["held"] = False
        fragment["error"] = str(exc)
        return fragment
    root_stat = _read_proc_stat(proc.pid)
    proc_starttime = root_stat[1] if root_stat is not None else None
    try:
        stdout_raw, stderr_raw = proc.communicate(timeout=row["timeout_s"])
    except subprocess.TimeoutExpired as timeout_exc:
        leader_finished = proc.poll() is not None
        cleanup_ok = _cleanup_row(
            proc, baseline_children, proc_starttime
        )
        stdout_raw, stderr_raw = _bounded_communicate(proc, timeout_exc)
        if not leader_finished:
            fragment["got"] = "timeout"
            fragment["held"] = False
            fragment["elapsed_s"] = round(time.monotonic() - started, 3)
            fragment["stdout_tail"] = _tail(stdout_raw or b"")
            fragment["stderr_tail"] = _tail(stderr_raw or b"")
            if not cleanup_ok:
                fragment["cleanup_error"] = (
                    "row descendants remain after bounded cleanup"
                )
            return fragment
        got = proc.returncode
    else:
        got = proc.returncode
        cleanup_ok = _cleanup_row(
            proc, baseline_children, proc_starttime
        )
    stdout_text = (stdout_raw or b"").decode("utf-8", errors="replace")
    missing = [n for n in needles if n not in stdout_text]
    fragment["got"] = got
    fragment["held"] = got == expected_exit and not missing and cleanup_ok
    fragment["elapsed_s"] = round(time.monotonic() - started, 3)
    fragment["stdout_tail"] = _tail(stdout_raw)
    fragment["stderr_tail"] = _tail(stderr_raw)
    if retain_streams:
        fragment["stdout"] = stdout_text
        fragment["stderr"] = stderr_raw.decode("utf-8", errors="replace")
    if missing:
        fragment["stdout_missing"] = missing
    if not cleanup_ok:
        fragment["cleanup_error"] = (
            "row descendants remain after bounded cleanup"
        )
    return fragment


# --------------------------------------------------------------- fleet clone


def resolve_rev(root, rev):
    """Resolve REV^{commit} in root. Returns (sha, error)."""
    proc = subprocess.run(
        [
            "git", "-C", root, "rev-parse", "--verify", "--quiet",
            "--end-of-options", f"{rev}^{{commit}}",
        ],
        env=git_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    sha = proc.stdout.decode("utf-8", errors="replace").strip()
    if proc.returncode != 0 or not HEX40.match(sha):
        return None, f"rev {rev!r} unavailable in {root}"
    return sha, None



def strict_scratch_root():
    """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
    round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
    fallback to /tmp, preserving CR47 semantics), else the platform default."""
    import os as _os
    t = _os.environ.get("TMPDIR")
    if t:
        if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
            raise RuntimeError(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()

def clone_lane_at_rev(root, rev, sha):
    """Clone the lane detached at sha into a fleet-mirror mkdtemp.

    Returns (workdir, clone_root) on success; caller removes workdir.
    Raises RuntimeError on any git failure.
    """
    root_real = os.path.realpath(root)
    fleet_root = os.path.dirname(root_real)
    env = git_env()
    try:
        work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=strict_scratch_root())
    except OSError as exc:  # round-18 w2 CR47: an unusable /tmp is could-not-evaluate (2), never "differs" (1)
        raise RuntimeError(f"cannot create clone scratch under the scratch root: {exc}") from exc
    try:
        fleet = os.path.join(work, "fleet")
        os.mkdir(fleet)
        try:
            siblings = sorted(os.listdir(fleet_root))
        except OSError:
            siblings = []
        for name in siblings:
            if not name.endswith("-shokunin"):
                continue
            src = os.path.join(fleet_root, name)
            if os.path.realpath(src) == root_real:
                continue
            os.symlink(src, os.path.join(fleet, name))
        clone_root = os.path.join(fleet, os.path.basename(root_real))
        clone = subprocess.run(
            [
                "git", "clone", "-q", "--no-hardlinks",
                "-c", "core.hooksPath=/dev/null", root_real, clone_root,
            ],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if clone.returncode != 0:
            raise RuntimeError(
                "git clone failed: "
                + clone.stderr.decode("utf-8", errors="replace").strip()
            )
        checkout = subprocess.run(
            ["git", "-C", clone_root, "checkout", "-q", "--detach", sha],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if checkout.returncode != 0:
            raise RuntimeError(
                f"checkout {sha!r} failed: "
                + checkout.stderr.decode("utf-8", errors="replace").strip()
            )
        head = subprocess.run(
            ["git", "-C", clone_root, "rev-parse", "HEAD"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        observed = head.stdout.decode("utf-8", errors="replace").strip()
        if head.returncode != 0 or observed != sha:
            raise RuntimeError(
                f"clone HEAD {observed!r} != requested {sha!r}"
            )
        return work, clone_root
    except Exception:
        shutil.rmtree(work, ignore_errors=True)
        raise


# -------------------------------------------------------------------- driver


def evaluate(root, registry_path, only, tags, rev, rev_resolved, fleet_root,
             live):
    """Load the registry and run selected rows under root.

    Returns (exit_code, report_dict). exit_code in {0, 1, 2}.
    """
    rows, data, error = load_registry(registry_path)
    report = {
        "schema": REPORT_SCHEMA,
        "root": root,
        "live": live,
        "rev": rev,
        "rev_resolved": rev_resolved,
        "registry": registry_path,
        "registry_sha256": registry_sha256(registry_path),
        "only": only,
        "tags": list(tags),
    }
    if error:
        report["error"] = error
        return 2, report
    selected = rows
    if only is not None:
        matched = [r for r in rows if r["name"] == only]
        if not matched:
            report["error"] = f"--only {only!r} matches no registry row"
            return 2, report
        selected = matched
    if tags:
        wanted = set(tags)
        selected = [
            r for r in selected if wanted.intersection(r.get("tags", []))
        ]
        if not selected:
            report["error"] = (
                f"--tag {sorted(wanted)!r} selects no registry row"
            )
            return 2, report
    if only is not None and not selected:
        report["error"] = (
            f"--only {only!r} is excluded by --tag {sorted(set(tags))!r}"
        )
        return 2, report
    fragments = [run_row(row, root, fleet_root) for row in selected]
    report["rows"] = fragments
    active = [
        f for f in fragments if f["status"] == "active"
    ]
    superseded = [
        f for f in fragments if f["status"] == "superseded"
    ]
    held = sum(1 for f in active if f["held"])
    report["held"] = held
    report["total"] = len(active)
    report["superseded"] = len(superseded)
    return (0 if held == len(active) else 1), report


def print_human(report, stream=sys.stdout):
    if "error" in report:
        stream.write(
            f"REGISTRY_CHECK: could-not-evaluate ({report['error']})\n"
        )
        stream.flush()
        return
    for frag in report["rows"]:
        if frag["status"] == "superseded":
            stream.write(
                f"ROW {frag['name']} superseded "
                f"expect={frag['expect']} got={frag['got']}\n"
            )
            continue
        stream.write(
            f"ROW {frag['name']} expect={frag['expect']} "
            f"got={frag['got']} {'held' if frag['held'] else 'differs'}\n"
        )
    stream.write(
        f"REGISTRY_CHECK: held={report['held']}/{report['total']} "
        f"superseded={report['superseded']}\n"
    )
    stream.flush()


# ------------------------------------------------------------------ selftest


def selftest():
    scratch = tempfile.mkdtemp(
        prefix="tameshi-r17-registry-check-selftest.", dir=strict_scratch_root()
    )
    passed = 0
    failed = []

    def record(name, ok, detail):
        nonlocal passed
        if ok:
            passed += 1
            emit(f"SELFTEST_CASE {name} PASS ({detail})")
        else:
            failed.append(name)
            emit(f"SELFTEST_CASE {name} FAIL ({detail})")

    def run_child(args, extra_env=None):
        env = row_env()
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [sys.executable, SELF] + args,
            cwd=scratch,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

    def write_registry(name, rows, schema=SCHEMA, raw=None):
        path = os.path.join(scratch, name)
        if raw is not None:
            payload = raw
        else:
            payload = json.dumps({"schema": schema, "rows": rows})
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(payload)
        return path

    def row(name, code, exit_expect, needles=None, timeout=30, **kw):
        r = {
            "name": name,
            "kind": kw.get("kind", "probe"),
            "argv": [sys.executable, "-c", code],
            "expect": {"exit": exit_expect},
            "timeout_s": timeout,
            "source": "tools/registry-check.py@"
                      "98bea7da5801f4bc58e4187690ee1687c8a5061f:1",
            "status": kw.get("status", "active"),
        }
        if needles is not None:
            r["expect"]["stdout_contains"] = needles
        if "tags" in kw:
            r["tags"] = kw["tags"]
        if "superseded_by" in kw:
            r["superseded_by"] = kw["superseded_by"]
        return r

    def check_lines(proc, wants, stream="stdout"):
        raw = proc.stdout if stream == "stdout" else proc.stderr
        out = raw.decode("utf-8", errors="replace")
        return all(w in out for w in wants)

    def process_identity_code(path):
        return (
            "stat_fields = open(f'/proc/{os.getpid()}/stat', "
            "encoding='ascii').read().rsplit(')', 1)[1].split()\n"
            f"with open({path!r}, 'w') as identity_file:\n"
            "    identity_file.write(f'{os.getpid()} {stat_fields[19]}')\n"
        )

    def read_process_identity(path):
        try:
            with open(path, encoding="ascii") as fh:
                pid, starttime = (int(part) for part in fh.read().split())
            return pid, starttime
        except (OSError, ValueError):
            return None

    def process_identity_present(identity):
        if identity is None:
            return False
        pid, starttime = identity
        stat = _read_proc_stat(pid)
        return stat is not None and stat[1] == starttime

    def stop_test_process(identity):
        if identity is None:
            return
        pid, starttime = identity
        in_scope = lambda: (
            (stat := _read_proc_stat(pid)) is not None
            and stat[1] == starttime
        )
        _signal_process_identity(pid, starttime, signal.SIGKILL, in_scope)


    def git(args, cwd=None, extra_env=None):
        env = git_env()
        if extra_env:
            env.update(extra_env)
        cmd = ["git"] + args
        if cwd:
            cmd = ["git", "-C", cwd] + args
        return subprocess.run(
            cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def head_of(repo):
        proc = git(["rev-parse", "HEAD"], repo)
        return (
            proc.stdout.decode("utf-8", errors="replace").strip()
            if proc.returncode == 0
            else None
        )

    lane = os.path.join(scratch, "lane")
    os.makedirs(lane)
    canary = os.path.join(scratch, "canary")
    os.makedirs(canary)
    canary_file = os.path.join(canary, "marker.txt")
    with open(canary_file, "w", encoding="utf-8") as fh:
        fh.write("canary\n")

    try:
        # --- fixture lanes: a git lane for --rev, a canary repo ------------
        git_lane = os.path.join(scratch, "selftest-lane-shokunin")
        os.makedirs(os.path.join(git_lane, "tools"))
        reg_rev = write_registry(
            "rev-registry.json",
            [row("rev-ok", "print('rev-marker')", 0, ["rev-marker"])],
        )
        shutil.copy(reg_rev, os.path.join(git_lane, "tools", "registry.json"))
        author_env = {
            "GIT_AUTHOR_NAME": "selftest",
            "GIT_AUTHOR_EMAIL": "selftest@invalid",
            "GIT_COMMITTER_NAME": "selftest",
            "GIT_COMMITTER_EMAIL": "selftest@invalid",
        }
        for args in (
            ["init", "-q", git_lane],
            ["-C", git_lane, "add", "tools/registry.json"],
            ["-C", git_lane, "commit", "-q", "-m", "fixture"],
        ):
            proc = git(args, extra_env=author_env)
            if proc.returncode != 0:
                emit(
                    "SELFTEST: COULD_NOT_EVALUATE "
                    f"(fixture git failed: {proc.stderr!r})"
                )
                return 2
        for args in (
            ["init", "-q", canary],
            ["-C", canary, "add", "marker.txt"],
            ["-C", canary, "commit", "-q", "-m", "canary"],
        ):
            proc = git(args, extra_env=author_env)
            if proc.returncode != 0:
                emit(
                    "SELFTEST: COULD_NOT_EVALUATE "
                    f"(canary git failed: {proc.stderr!r})"
                )
                return 2
        rev = head_of(git_lane)
        canary_head = head_of(canary)
        decoy_dir = os.path.join(canary, ".git")

        # (1) GIT_DIR exported during --rev must not move the canary.
        proc = run_child(
            ["--root", git_lane, "--rev", rev],
            extra_env={"GIT_DIR": decoy_dir},
        )
        record(
            "gitdir-scrub-rev",
            proc.returncode == 0
            and check_lines(proc, ["REGISTRY_CHECK: held=1/1"])
            and head_of(canary) == canary_head
            and head_of(git_lane) == rev,
            f"exit={proc.returncode} canary_stable="
            f"{head_of(canary) == canary_head}",
        )

        # (2) A row that commits in a fixture repo must not touch the canary.
        fixture_repo = os.path.join(scratch, "commit-fixture")
        os.makedirs(fixture_repo)
        with open(os.path.join(fixture_repo, "seed.txt"), "w",
                  encoding="utf-8") as fh:
            fh.write("seed\n")
        commit_code = (
            "import os, subprocess\n"
            f"repo = {fixture_repo!r}\n"
            "env = dict(os.environ, "
            "GIT_AUTHOR_NAME='row', GIT_AUTHOR_EMAIL='row@invalid', "
            "GIT_COMMITTER_NAME='row', GIT_COMMITTER_EMAIL='row@invalid')\n"
            "for args in (['init','-q'], ['add','-A'], "
            "['commit','-q','-m','row-commit']):\n"
            "    subprocess.run(['git','-C',repo]+args, env=env, "
            "check=True, capture_output=True)\n"
            "print('row-committed')\n"
        )
        reg_commit = write_registry(
            "reg-commit.json",
            [row("commit-row", commit_code, 0, ["row-committed"])],
        )
        proc = run_child(
            ["--root", lane, "--registry", reg_commit],
            extra_env={"GIT_DIR": decoy_dir, "GIT_WORK_TREE": canary},
        )
        record(
            "gitdir-scrub-row",
            proc.returncode == 0
            and check_lines(proc, ["REGISTRY_CHECK: held=1/1"])
            and head_of(canary) == canary_head
            and os.path.isdir(os.path.join(fixture_repo, ".git")),
            f"exit={proc.returncode} canary_stable="
            f"{head_of(canary) == canary_head}",
        )

        # (3) Timeout kills the whole process group, grandchildren included.
        marker = os.path.join(scratch, "grandchild-survived")
        grandchild_code = (
            "import time\n"
            "time.sleep(20)\n"
            "with open(%r, 'w') as fh:\n"
            "    fh.write('x')\n" % marker
        )
        group_code = (
            "import subprocess, sys, time\n"
            "subprocess.Popen([sys.executable, '-c', %r])\n"
            "time.sleep(30)\n" % grandchild_code
        )
        reg_group = write_registry(
            "reg-group.json",
            [row("group-row", group_code, 0, timeout=1)],
        )
        proc = run_child(["--root", lane, "--registry", reg_group])
        time.sleep(1.0)
        record(
            "timeout-kills-group",
            proc.returncode == 1
            and check_lines(
                proc,
                ["ROW group-row expect=0 got=timeout differs",
                 "REGISTRY_CHECK: held=0/1"],
            )
            and not os.path.exists(marker),
            f"exit={proc.returncode} marker={os.path.exists(marker)}",
        )

        def run_escape_case(name, escape_call):
            pid_path = os.path.join(scratch, f"{name}.pid")
            ready_path = os.path.join(scratch, f"{name}.ready")
            marker_path = os.path.join(scratch, f"{name}.marker")
            escape_code = (
                "import os,time\n"
                f"{escape_call}\n"
                + process_identity_code(pid_path)
                + f"with open({ready_path!r}, 'w') as fh:\n"
                "    fh.write('ready')\n"
                "time.sleep(5)\n"
                f"with open({marker_path!r}, 'w') as fh:\n"
                "    fh.write('survived')\n"
            )
            parent_code = (
                "import os, subprocess, sys, time\n"
                "subprocess.Popen([sys.executable, '-c', %r])\n"
                "deadline = time.monotonic() + 3\n"
                f"while not os.path.exists({ready_path!r}) and "
                "time.monotonic() < deadline:\n"
                "    time.sleep(0.01)\n"
                f"if not os.path.exists({ready_path!r}):\n"
                "    raise SystemExit(3)\n"
                "time.sleep(30)\n"
            ) % escape_code
            registry = write_registry(
                f"reg-{name}.json",
                [row(name, parent_code, 0, timeout=1)],
            )
            started = time.monotonic()
            result = run_child(["--root", lane, "--registry", registry])
            elapsed = time.monotonic() - started
            identity = read_process_identity(pid_path)
            survivor = process_identity_present(identity)
            marker_exists = os.path.exists(marker_path)
            record(
                name,
                result.returncode == 1
                and check_lines(
                    result,
                    [f"ROW {name} expect=0 got=timeout differs",
                     "REGISTRY_CHECK: held=0/1"],
                )
                and identity is not None
                and not survivor
                and not marker_exists
                and elapsed < 3.5,
                f"exit={result.returncode} elapsed={elapsed:.3f}s "
                f"survivor={survivor} marker={marker_exists}",
            )
            if survivor:
                stop_test_process(identity)

        run_escape_case("timeout-kills-setsid-pipe", "os.setsid()")
        run_escape_case(
            "timeout-kills-setpgid-pipe", "os.setpgid(0, 0)"
        )

        daemon_pid_path = os.path.join(scratch, "daemon-exit.pid")
        daemon_ready_path = os.path.join(scratch, "daemon-exit.ready")
        daemon_code = (
            "import os,time\n"
            "if os.fork() == 0:\n"
            "    devnull = os.open(os.devnull, os.O_WRONLY)\n"
            "    os.dup2(devnull, 1)\n"
            "    os.dup2(devnull, 2)\n"
            "    os.setsid()\n"
            "    if os.fork():\n"
            "        os._exit(0)\n"
            "    stat_fields = open("
            "f'/proc/{os.getpid()}/stat', encoding='ascii'"
            ").read().rsplit(')', 1)[1].split()\n"
            f"    with open({daemon_pid_path!r}, 'w') as identity_file:\n"
            "        identity_file.write("
            "f'{os.getpid()} {stat_fields[19]}')\n"
            f"    with open({daemon_ready_path!r}, 'w') as fh:\n"
            "        fh.write('ready')\n"
            "    time.sleep(20)\n"
            "    os._exit(0)\n"
            "else:\n"
            "    deadline = time.monotonic() + 3\n"
            f"    while not os.path.exists({daemon_ready_path!r}) "
            "and time.monotonic() < deadline:\n"
            "        time.sleep(0.01)\n"
            f"    if not os.path.exists({daemon_ready_path!r}):\n"
            "        raise SystemExit(3)\n"
            "    print('daemon-parent-done')\n"
        )
        daemon_registry = write_registry(
            "reg-daemon-exit.json",
            [row("daemon-exit", daemon_code, 0,
                 ["daemon-parent-done"], timeout=5)],
        )
        daemon_result = run_child(
            ["--root", lane, "--registry", daemon_registry]
        )
        daemon_identity = read_process_identity(daemon_pid_path)
        daemon_survivor = process_identity_present(daemon_identity)
        record(
            "normal-exit-kills-double-fork",
            daemon_result.returncode == 0
            and check_lines(
                daemon_result,
                ["ROW daemon-exit expect=0 got=0 held",
                 "REGISTRY_CHECK: held=1/1"],
            )
            and daemon_identity is not None
            and not daemon_survivor,
            f"exit={daemon_result.returncode} "
            f"survivor={daemon_survivor}",
        )
        if daemon_survivor:
            stop_test_process(daemon_identity)

        # --- behavioural cases -------------------------------------------
        reg_held = write_registry(
            "reg-held.json",
            [
                row("ok-row", "print('alpha-ok')", 0, ["alpha-ok"]),
                row("nonzero-row", "import sys; sys.exit(3)", 3,
                    kind="gate"),
                row("old-row", "print('old-path')", 0,
                    status="superseded", superseded_by="ok-row"),
            ],
        )
        proc = run_child(["--root", lane, "--registry", reg_held])
        record(
            "all-held",
            proc.returncode == 0
            and check_lines(
                proc,
                ["ROW old-row superseded expect=0 got=0",
                 "REGISTRY_CHECK: held=2/2 superseded=1"],
            ),
            f"exit={proc.returncode}",
        )

        reg_diff = write_registry(
            "reg-diff.json",
            [row("bad-exit", "import sys; sys.exit(7)", 0)],
        )
        proc = run_child(["--root", lane, "--registry", reg_diff])
        record(
            "one-differs-exit",
            proc.returncode == 1
            and check_lines(
                proc,
                ["ROW bad-exit expect=0 got=7 differs",
                 "REGISTRY_CHECK: held=0/1 superseded=0"],
            ),
            f"exit={proc.returncode}",
        )

        reg_needle = write_registry(
            "reg-needle.json",
            [row("missing-needle", "print('hay')", 0, ["needle"])],
        )
        proc = run_child(["--root", lane, "--registry", reg_needle])
        record(
            "stdout-contains-missing",
            proc.returncode == 1
            and check_lines(
                proc,
                ["ROW missing-needle expect=0 got=0 differs",
                 "REGISTRY_CHECK: held=0/1"],
            ),
            f"exit={proc.returncode}",
        )

        # --- superseded rules ---------------------------------------------
        reg_sup_ok = write_registry(
            "reg-sup-ok.json",
            [
                row("new-row", "print('new')", 0),
                row("old-path", "import sys; sys.exit(2)", 2,
                    status="superseded", superseded_by="new-row"),
            ],
        )
        proc = run_child(["--root", lane, "--registry", reg_sup_ok])
        record(
            "superseded-runs-excluded",
            proc.returncode == 0
            and check_lines(
                proc,
                ["ROW old-path superseded expect=2 got=2",
                 "REGISTRY_CHECK: held=1/1 superseded=1"],
            ),
            f"exit={proc.returncode}",
        )

        reg_sup_missing = write_registry(
            "reg-sup-missing.json",
            [row("old-path", "print('x')", 0,
                 status="superseded", superseded_by="ghost")],
        )
        proc = run_child(["--root", lane, "--registry", reg_sup_missing])
        record("superseded-target-missing", proc.returncode == 2,
               f"exit={proc.returncode}")

        reg_sup_inactive = write_registry(
            "reg-sup-inactive.json",
            [
                row("old-path", "print('x')", 0,
                    status="superseded", superseded_by="older"),
                row("older", "print('y')", 0,
                    status="superseded", superseded_by="old-path"),
            ],
        )
        proc = run_child(["--root", lane, "--registry", reg_sup_inactive])
        record("superseded-target-not-active", proc.returncode == 2,
               f"exit={proc.returncode}")

        reg_sup_undeclared = write_registry(
            "reg-sup-undeclared.json",
            [row("old-path", "print('x')", 0, status="superseded")],
        )
        proc = run_child(["--root", lane, "--registry", reg_sup_undeclared])
        record("superseded-by-required", proc.returncode == 2,
               f"exit={proc.returncode}")

        # --- tags -----------------------------------------------------------
        reg_tags = write_registry(
            "reg-tags.json",
            [
                row("alpha-row", "print('a')", 0, tags=["alpha"]),
                row("beta-row", "print('b')", 0, tags=["beta"]),
                row("plain-row", "print('p')", 0),
                row("alpha-old", "print('ao')", 0, tags=["alpha"],
                    status="superseded", superseded_by="beta-row"),
            ],
        )
        proc = run_child(
            ["--root", lane, "--registry", reg_tags, "--tag", "alpha"]
        )
        record(
            "tag-selects-any",
            proc.returncode == 0
            and check_lines(
                proc,
                ["ROW alpha-row expect=0 got=0 held",
                 "ROW alpha-old superseded expect=0 got=0",
                 "REGISTRY_CHECK: held=1/1 superseded=1"],
            )
            and not check_lines(proc, ["ROW plain-row"]),
            f"exit={proc.returncode}",
        )

        proc = run_child(
            ["--root", lane, "--registry", reg_tags,
             "--tag", "alpha", "--tag", "beta"]
        )
        record(
            "tag-repeatable",
            proc.returncode == 0
            and check_lines(
                proc,
                ["ROW alpha-row", "ROW beta-row",
                 "REGISTRY_CHECK: held=2/2 superseded=1"],
            ),
            f"exit={proc.returncode}",
        )

        proc = run_child(
            ["--root", lane, "--registry", reg_tags, "--tag", "gamma"]
        )
        record("tag-miss", proc.returncode == 2, f"exit={proc.returncode}")

        # --- invalid registries -------------------------------------------
        proc = run_child(
            ["--root", lane,
             "--registry", write_registry("reg-badschema.json", [],
                                          schema="other-schema")]
        )
        record("invalid-schema", proc.returncode == 2,
               f"exit={proc.returncode}")

        dup = row("dup", "print(1)", 0)
        proc = run_child(
            ["--root", lane,
             "--registry", write_registry("reg-dup.json", [dup, dict(dup)])]
        )
        record("duplicate-names", proc.returncode == 2,
               f"exit={proc.returncode}")

        shell_row = {
            "name": "shell",
            "kind": "probe",
            "argv": "echo hi",  # shell string, not an argv list
            "expect": {"exit": 0},
            "timeout_s": 5,
            "source": "tools/registry-check.py@"
                      "98bea7da5801f4bc58e4187690ee1687c8a5061f:1",
            "status": "active",
        }
        proc = run_child(
            ["--root", lane,
             "--registry", write_registry("reg-shell.json", [shell_row])]
        )
        record("shell-string-argv", proc.returncode == 2,
               f"exit={proc.returncode}")

        for case, mutation in (
            ("invalid-status",
             {"status": "parked"}),
            ("invalid-name",
             {"name": "Bad_Name"}),
            ("invalid-source",
             {"source": "SKILL.md round-17 registry pending"}),
        ):
            variant = dict(row("victim", "print(1)", 0))
            variant.update(mutation)
            proc = run_child(
                ["--root", lane,
                 "--registry", write_registry(f"reg-{case}.json", [variant])]
            )
            record(case, proc.returncode == 2, f"exit={proc.returncode}")

        proc = run_child(
            ["--root", lane,
             "--registry", os.path.join(scratch, "does-not-exist.json")]
        )
        record("unreadable-registry", proc.returncode == 2,
               f"exit={proc.returncode}")

        short_source = row(
            "short-source-revision", "print('short-source-accepted')", 0
        )
        short_source["source"] = "tools/registry-check.py@a:1"
        proc = run_child(
            ["--root", lane,
             "--registry", write_registry(
                 "reg-short-source.json", [short_source]
             )]
        )
        record(
            "short-source-revision",
            proc.returncode == 2 and check_lines(proc, ["source", "7-40 hex rev"]),
            f"exit={proc.returncode}",
        )

        for case, token, error in (
            ("timeout-zero", "0", "finite positive number"),
            ("timeout-nan", "NaN", "non-finite JSON number"),
            ("timeout-infinity", "Infinity", "non-finite JSON number"),
            ("timeout-negative-infinity", "-Infinity",
             "non-finite JSON number"),
            ("timeout-overflow", "1e999", "finite positive number"),
            ("timeout-boolean", "true", "finite positive number"),
            ("timeout-too-large", "2147484", "finite positive number"),
            ("timeout-float-huge", "1e308", "finite positive number"),
        ):
            invalid_timeout = row(case, "print('should-not-run')", 0)
            raw = json.dumps(
                {"schema": SCHEMA, "rows": [invalid_timeout]}
            ).replace(
                '"timeout_s": 30', f'"timeout_s": {token}', 1
            )
            registry = write_registry(
                f"reg-{case}.json", [], raw=raw
            )
            proc = run_child(["--root", lane, "--registry", registry])
            record(
                case,
                proc.returncode == 2
                and check_lines(proc, [case, "timeout_s", error]),
                f"exit={proc.returncode}",
            )

        class FakePipe:
            def __init__(self):
                self.closed = False

            def close(self):
                self.closed = True

        class FakeTimedProcess:
            def __init__(self):
                self.stdout = FakePipe()
                self.stderr = FakePipe()
                self.communicate_timeout = None
                self.wait_timeout = None

            def communicate(self, timeout=None):
                self.communicate_timeout = timeout
                if timeout is None:
                    return b"", b""
                raise subprocess.TimeoutExpired(
                    ["fake"], timeout, output=b"partial", stderr=b"partial-err"
                )

            def wait(self, timeout=None):
                self.wait_timeout = timeout
                raise subprocess.TimeoutExpired(["fake"], timeout)

        fake_process = FakeTimedProcess()
        drained = _bounded_communicate(fake_process)
        record(
            "bounded-pipe-drain",
            fake_process.communicate_timeout == PIPE_DRAIN_TIMEOUT_S
            and fake_process.wait_timeout == PIPE_DRAIN_TIMEOUT_S
            and fake_process.stdout.closed
            and fake_process.stderr.closed
            and drained == (b"partial", b"partial-err"),
            f"communicate_timeout={fake_process.communicate_timeout} "
            f"wait_timeout={fake_process.wait_timeout}",
        )

        original_pidfd_open = os.pidfd_open
        original_pidfd_send_signal = signal.pidfd_send_signal
        original_close = os.close
        stale_reads = iter((1234, 1235))
        fake_signals = []
        try:
            os.pidfd_open = lambda _pid, _flags=0: 999999
            signal.pidfd_send_signal = (
                lambda pidfd, signum: fake_signals.append((pidfd, signum))
            )
            os.close = lambda _fd: None
            rejected = not _signal_process_identity(
                987654, 1234, signal.SIGKILL, lambda: True,
                read_stat=lambda _pid: (os.getpid(), next(stale_reads), "S"),
            )
        finally:
            os.pidfd_open = original_pidfd_open
            signal.pidfd_send_signal = original_pidfd_send_signal
            os.close = original_close
        record(
            "pidfd-revalidates-starttime",
            rejected and not fake_signals,
            f"stale_identity_rejected={rejected} signals={len(fake_signals)}",
        )

        # Simulated identities keep these race controls deterministic and never
        # send a signal to a host process.
        from unittest.mock import patch
        identity = (os.getpid(), 1234, "S")
        with patch(__name__ + "._read_proc_stat", return_value=identity):
            baseline_rejected = not _row_identity_is_owned(
                987654, 1234, 987655, 1235, frozenset({(987654, 1234)})
            )
            adopted_owned = _row_identity_is_owned(
                987654, 1234, 987655, 1235, frozenset()
            )
        record(
            "baseline-child-preserved",
            baseline_rejected and adopted_owned,
            f"baseline_rejected={baseline_rejected} adopted_owned={adopted_owned}",
        )
        ownership = iter((True, False))
        with patch.object(os, "pidfd_open", return_value=999999), \
                patch.object(os, "close"), \
                patch.object(signal, "pidfd_send_signal") as sent:
            scope_rejected = not _signal_process_identity(
                987654, 1234, signal.SIGKILL, lambda: next(ownership),
                read_stat=lambda _pid: identity,
            )
        record(
            "pidfd-revalidates-ownership",
            scope_rejected and not sent.called,
            f"ownership_change_rejected={scope_rejected} signals={sent.call_count}",
        )


        # --- --rev cases ---------------------------------------------------
        proc = run_child(["--root", git_lane, "--rev", "0" * 40])
        record(
            "rev-unknown",
            proc.returncode == 2
            and check_lines(proc, ["REGISTRY_CHECK: could-not-evaluate"]),
            f"exit={proc.returncode}",
        )

        for label, bad_rev in (
            ("rev-path-like", "tools/registry.json"),
            ("rev-option-like", "--detach"),
        ):
            proc = run_child(["--root", git_lane, "--rev", bad_rev])
            record(label, proc.returncode == 2, f"exit={proc.returncode}")

        detached_row = row("detached-head", "", 1)
        detached_row["argv"] = ["git", "symbolic-ref", "-q", "HEAD"]
        detached_registry = write_registry(
            "reg-detached-head.json", [detached_row]
        )
        proc = run_child(
            ["--root", git_lane, "--rev", rev,
             "--registry", detached_registry]
        )
        record(
            "rev-clone-detached",
            proc.returncode == 0
            and check_lines(
                proc,
                ["ROW detached-head expect=1 got=1 held",
                 "REGISTRY_CHECK: held=1/1 superseded=0"],
            ),
            f"exit={proc.returncode}",
        )

        proc = run_child(["--root", git_lane, "--rev", rev])
        record(
            "rev-clone-held",
            proc.returncode == 0
            and check_lines(
                proc,
                ["ROW rev-ok expect=0 got=0 held",
                 "REGISTRY_CHECK: held=1/1 superseded=0"],
            ),
            f"exit={proc.returncode}",
        )

        proc = run_child(
            ["--root", git_lane, "--rev", rev, "--json"]
        )
        try:
            rep = json.loads(proc.stdout.decode("utf-8"))
            rev_json_ok = (
                rep.get("schema") == REPORT_SCHEMA
                and rep.get("rev_resolved") == rev
                and rep.get("held") == 1
                and rep["rows"][0].get("stdout_tail") == "rev-marker\n"
                and isinstance(rep.get("registry_sha256"), str)
                and len(rep["registry_sha256"]) == 64
            )
        except (ValueError, KeyError, IndexError):
            rev_json_ok = False
        record(
            "rev-resolved-reported",
            proc.returncode == 0 and rev_json_ok,
            f"exit={proc.returncode}",
        )

        # A non-hermetic argv (absolute live-fleet path) must not pass unless
        # the row declares `external: true` (K04 P7).
        live_token = os.path.join(scratch, "live-fleet", "lane")
        base_row = {"name": "live-row", "kind": "probe",
                    "argv": [sys.executable, "-c", "print('x')", live_token],
                    "expect": {"exit": 0}, "timeout_s": 5,
                    "source": "tools/registry-check.py@"
                              "98bea7da5801f4bc58e4187690ee1687c8a5061f:1",
                    "status": "active"}
        reg_nonhermetic = write_registry(
            "reg-nonhermetic.json", [base_row]
        )
        proc = run_child(
            ["--root", git_lane, "--rev", rev,
             "--registry", reg_nonhermetic]
        )
        record(
            "rev-non-hermetic-argv",
            proc.returncode == 1
            and check_lines(
                proc,
                ["ROW live-row expect=0 got=non-hermetic differs"],
            ),
            f"exit={proc.returncode}",
        )

        declared = dict(base_row, external=True)
        reg_external = write_registry("reg-external.json", [declared])
        proc = run_child(
            ["--root", git_lane, "--rev", rev,
             "--registry", reg_external, "--json"]
        )
        try:
            rep = json.loads(proc.stdout.decode("utf-8"))
            ext_ok = (
                rep.get("held") == 1
                and rep["rows"][0].get("non_hermetic_argv") == [live_token]
            )
        except (ValueError, KeyError, IndexError):
            ext_ok = False
        record(
            "rev-external-declared",
            proc.returncode == 0 and ext_ok,
            f"exit={proc.returncode}",
        )

        # --- selection / usage ---------------------------------------------
        proc = run_child(
            ["--root", lane, "--registry", reg_held, "--only", "ok-row"]
        )
        record(
            "only-filter",
            proc.returncode == 0
            and check_lines(proc, ["REGISTRY_CHECK: held=1/1"]),
            f"exit={proc.returncode}",
        )

        proc = run_child(
            ["--root", lane, "--registry", reg_held,
             "--only", "ok-row", "--tag", "beta"]
        )
        record("only-tag-conflict", proc.returncode == 2,
               f"exit={proc.returncode}")

        proc = run_child(
            ["--root", lane, "--registry", reg_held, "--only", "nope"]
        )
        record("only-missing", proc.returncode == 2, f"exit={proc.returncode}")

        proc = run_child(["--bogus-flag"])
        record("usage-unknown-flag", proc.returncode == 64,
               f"exit={proc.returncode}")

        proc = run_child(["--selftest", "extra"])
        record("usage-selftest-extra", proc.returncode == 64,
               f"exit={proc.returncode}")

        # --- --json shape ---------------------------------------------------
        proc = run_child(
            ["--root", lane, "--registry", reg_diff, "--json"]
        )
        try:
            report = json.loads(proc.stdout.decode("utf-8"))
            json_ok = (
                report.get("schema") == REPORT_SCHEMA
                and report.get("held") == 0
                and report.get("total") == 1
                and report.get("superseded") == 0
                and report["rows"][0]["got"] == 7
                and "stdout_tail" in report["rows"][0]
                and "stderr_tail" in report["rows"][0]
                and report.get("registry_sha256")
                == hashlib.sha256(open(reg_diff, "rb").read()).hexdigest()
            )
        except (ValueError, KeyError, IndexError):
            json_ok = False
        record(
            "json-report",
            proc.returncode == 1 and json_ok,
            f"exit={proc.returncode}",
        )

        # --- live-root warning ---------------------------------------------
        proc = run_child(["--root", lane, "--registry", reg_held])
        record(
            "live-root-warning",
            proc.returncode == 0
            and check_lines(
                proc,
                ["rows may write into the root"],
                stream="stderr",
            ),
            f"exit={proc.returncode}",
        )
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    if failed:
        emit(f"SELFTEST: FAIL ({len(failed)} of {passed + len(failed)} cases: "
             + ", ".join(failed) + ")")
        return 1
    emit(f"SELFTEST: PASS ({passed} cases)")
    return 0


# ----------------------------------------------------------------------- cli


def _sigterm(_signum, _frame):
    raise SystemExit(2)


def main(argv):
    if argv and argv[0] == "--selftest":
        if len(argv) != 1:
            return usage_failure("--selftest takes no further arguments")
        return selftest()

    root = default_root()
    rev = None
    registry = None
    only = None
    tags = []
    as_json = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-h", "--help"):
            sys.stdout.write(__doc__)
            return 0
        if arg == "--json":
            as_json = True
            i += 1
            continue
        if arg in ("--root", "--rev", "--registry", "--only", "--tag"):
            if i + 1 >= len(argv):
                return usage_failure(f"{arg} requires a value")
            value = argv[i + 1]
            if arg == "--root":
                root = value
            elif arg == "--rev":
                rev = value
            elif arg == "--registry":
                registry = value
            elif arg == "--only":
                only = value
            else:
                tags.append(value)
            i += 2
            continue
        return usage_failure(f"unknown argument {arg!r}")

    signal.signal(signal.SIGTERM, _sigterm)

    if registry is not None:
        registry = os.path.abspath(registry)

    live = rev is None
    root_requested = root
    rev_resolved = None
    fleet_root = None
    if not os.path.isdir(root_requested):
        report = {
            "schema": REPORT_SCHEMA,
            "root": root_requested,
            "rev": rev,
            "error": f"root_unavailable: {root_requested}",
        }
        if as_json:
            emit(json.dumps(report, indent=2, sort_keys=True))
        else:
            emit(f"REGISTRY_CHECK: could-not-evaluate (root_unavailable: "
                 f"{root_requested})")
        return 2

    work = None
    if rev is not None:
        sha, error = resolve_rev(root_requested, rev)
        if error:
            report = {
                "schema": REPORT_SCHEMA,
                "root": root_requested,
                "rev": rev,
                "error": error,
            }
            if as_json:
                emit(json.dumps(report, indent=2, sort_keys=True))
            else:
                emit(f"REGISTRY_CHECK: could-not-evaluate ({error})")
            return 2
        rev_resolved = sha
        fleet_root = os.path.dirname(os.path.realpath(root_requested))
        try:
            work, root = clone_lane_at_rev(root_requested, rev, sha)
        except RuntimeError as exc:
            report = {
                "schema": REPORT_SCHEMA,
                "root": root_requested,
                "rev": rev,
                "rev_resolved": sha,
                "error": str(exc),
            }
            if as_json:
                emit(json.dumps(report, indent=2, sort_keys=True))
            else:
                emit(f"REGISTRY_CHECK: could-not-evaluate ({exc})")
            return 2
        if registry is None:
            registry = os.path.join(root, "tools", "registry.json")
    else:
        root = os.path.abspath(root_requested)
        if registry is None:
            registry = os.path.join(root, "tools", "registry.json")

    try:
        if live:
            emit_err(
                "registry-check: warning: live --root mode runs rows in the "
                "lane; rows may write into the root (use --rev to grade a "
                "throwaway clone)"
            )
        code, report = evaluate(
            root, registry, only, tags, rev, rev_resolved, fleet_root, live
        )
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)

    report["exit"] = code
    if as_json:
        emit(json.dumps(report, indent=2, sort_keys=True))
        print_human(report, stream=sys.stderr)
    else:
        print_human(report, stream=sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
