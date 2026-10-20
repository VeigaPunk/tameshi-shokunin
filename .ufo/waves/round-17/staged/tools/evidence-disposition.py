#!/usr/bin/env python3
"""evidence-disposition.py — expectation disposition gate (tameshi-shokunin round 14).

Question answered: does one dispositions document account for every frozen
round-13 expected check exactly once, and does each disposition row bind to a
raw receipt observation that satisfies the original expectation — or, for the
one configured supersession, retain a genuinely mismatched raw observation
while both declared replacements pass?

This is a gate over declarations and retained receipt JSON. It never executes
receipt argv. Pins in the dispositions document are configured authority for
the bytes read here; they are not an authentication or preregistration claim,
and passing this gate does not prove that any recorded command was rerun.

Disposition schema `evidence-dispositions-v1`:
  {"schema": "evidence-dispositions-v1",
   "expected_file": <lane-relative path>,
   "inputs": {<lane-relative path>: <64 lowercase hex sha256>, ...},
   "rows": [effective | superseded, ...]}

  Schema `evidence-dispositions-v2` (round-17 R16-OP1) keeps every v1 field
  and adds:
    "supersedes": lane-relative path of the v1 manifest this document
      supersedes; informational, and it must itself be pinned in `inputs`.
    "historical_inputs": {<lane-relative path>: {"rev": <40-hex commit>,
      "reason": <text>}}. For each declared path the expected-input bytes are
      read with `git -C <root> cat-file blob --end-of-options <rev>:<path>`
      instead of the live file, after a repo-identity guard (realpath of
      `git -C <root> rev-parse --show-toplevel` must equal realpath(root)).
      Keys must start with `tools/` (lane instruments move by design; evidence
      never) and must appear in expected.json's `inputs`; the blob digest must
      still equal the expected pin. Every other input keeps live-tree
      integrity-first verification. The payload adds
      `expected_inputs_historical` {path: rev}.
      Failure ids (exit 2): historical_input_forbidden,
      historical_input_unknown, historical_input_unavailable,
      expected_input_digest_mismatch, historical_input_unneeded,
      historical_input_uncommitted, supersedes_mismatch.

  v2 guards (round-17 hardening):
    G1 historical_input_unneeded: a waived path whose live bytes still equal
       the expected pin must not be waived (the waiver set is derived from
       observed drift, not author choice).
    G2 historical_input_uncommitted: the live bytes of a waived path must equal
       HEAD:<path>; an uncommitted worktree edit, a symlink, or deletion while
       HEAD still has the path is tampering. A committed deletion is allowed.
    G3 rev must resolve to exactly that commit id (tree/blob/HEAD/branch/abbrev
       rejected) and be an ancestor of HEAD, else historical_input_unavailable.
    G4 every git subprocess scrubs all inherited GIT_* variables and sets
       GIT_NO_REPLACE_OBJECTS=1, GIT_GRAFT_FILE=/dev/null,
       GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null; the root must be a
       non-shallow work tree whose --absolute-git-dir is <root>/.git.
    G5 the tree entry must be a 100644/100755 blob; bytes are read, never text.
    G6 text mode prints one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per
       waiver; JSON carries expected_inputs_historical (and historical_text).
    G7 `supersedes` must name a v1 manifest with this document's expected_file
       and rows, whose inputs are pinned identically (supersedes_mismatch).

  effective row keys are exactly:
      name, state="effective", receipt, check
    name and check must be the same string; the check must exist in the named
    receipt. A different same-shaped check (e.g. pin_live -> pin_env_scrub)
    is rejected by `effective_check_name_mismatch`.

  superseded row keys are exactly:
      name, state="superseded", reason, raw_receipt, raw_check, superseded_by
    Only `producer_before` may be superseded (configured round-14 policy).
    raw_receipt/raw_check name the retained raw observation; it is re-evaluated
    against the original expectation and must genuinely mismatch. The
    replacement list must be exactly producer_before_oracle and
    producer_after_oracle; both must be effective rows with check == name and
    must pass. The producer-oracle receipt must declare
    `supersedes` starting "verification.json producer_before" and its
    `oracle_sha256` must equal expected.inputs[producer-oracle.py].

Receipt and raw_receipt values are lane-relative canonical paths that must
appear as `inputs` keys. They must live in the expected file's directory.
`inputs` must pin the expected file and the two round-13 sibling receipts
(verification.json, producer-oracle-repair.json). Every declared pin is hashed
and checked before any expectation predicate runs. expected.json's own
`inputs` map is also verified in full before predicates.

Every file is read once through an O_NOFOLLOW descriptor, lstat/fstat identity
is compared, and the same cached bytes are hashed and parsed. Absolute paths,
"..", ".", "\\", NUL, repeated or trailing separators, symlink components and
non-regular files are rejected.

Predicates use only the original expected fields: exit, contains, id, reason,
rows, statuses, result_reuse. `contains` is a literal substring of the receipt
check's stdout only (never stderr). Structured predicates parse stdout as one
JSON object:
  id/reason            exact value at the top level
  rows                 top-level rows (int or list length), counts.legs, and
                       len(legs) must all agree when present
  statuses             expected histogram compared against top-level statuses,
                       counts, and the per-leg content_status histogram;
                       an absent status counts as 0
  result_reuse         top-level and every per-leg result_reuse must agree
Receipt `expected_exit`/`exit_matches` fields are never trusted. Receipt-only
checks stay informational and never become expectations.

Exit map:
  0  clean: every expected check accounted for, all predicates pass
  1  failed semantic expectation (row graph or predicate mismatch)
  2  could-not-evaluate: missing/unreadable/malformed/tampered/path-invalid
     input, invalid schema/type, or an unexpected internal failure
  64 usage error

Output: stable finding IDs, one disposition record per expected check, and
mismatch details. `--json` emits the full document; text output is one summary
line, ROW lines and FINDING lines.

CLI:
  evidence-disposition.py --root LANE --dispositions FILE [--json]
  evidence-disposition.py --selftest
"""

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path, PurePosixPath

VERSION = "evidence-disposition.py r17.1 (tameshi-shokunin, 2026-10-20): hardened v2 historical inputs"
SELF = os.path.realpath(__file__)

SCHEMA = "evidence-dispositions-v1"
SCHEMA_V2 = "evidence-dispositions-v2"
SCHEMAS = (SCHEMA, SCHEMA_V2)
RESULT_SCHEMA = "evidence-disposition-result-v1"
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")

EXPECTATION_FIELDS = frozenset(
    ("exit", "contains", "id", "reason", "rows", "statuses", "result_reuse")
)
EFFECTIVE_KEYS = frozenset(("name", "state", "receipt", "check"))
SUPERSEDED_KEYS = frozenset(
    ("name", "state", "reason", "raw_receipt", "raw_check", "superseded_by")
)

# Round-14 configured supersession policy. Only the routed producer_before row
# may be superseded, and only by the two oracle observations.
SUPERSEDED_POLICY = {
    "producer_before": {
        "raw_receipt": "verification.json",
        "raw_check": "producer_before",
        "replacements": ("producer_before_oracle", "producer_after_oracle"),
    }
}
REQUIRED_RECEIPTS = ("verification.json", "producer-oracle-repair.json")
ORACLE_RECEIPT = "producer-oracle-repair.json"
ORACLE_INPUT = "producer-oracle.py"
ORACLE_SUPERSEDES_PREFIX = "verification.json producer_before"

USAGE = """usage: evidence-disposition.py --root LANE --dispositions FILE [--json]
       evidence-disposition.py --selftest

Expectation-disposition gate: every frozen expected check appears exactly once
in rows; effective rows must satisfy their original expectation from a named
receipt check; the one configured producer_before supersession must retain a
genuinely mismatched raw observation and pass both oracle replacements.

exit 0   clean
exit 1   failed semantic expectation
exit 2   could-not-evaluate bad/missing/tampered input
exit 64  usage error

Receipt/raw_receipt values are lane-relative paths pinned in `inputs`. The tool
never executes receipt argv. `--selftest` builds isolated /tmp fixtures.
evidence-dispositions-v2 manifests add `supersedes` (pinned v1 manifest path)
and `historical_inputs` (tools/* expected inputs read as git blobs at the
declared rev after a repo-identity guard). A waiver is refused when the live
bytes still equal the pin (historical_input_unneeded) or differ from HEAD
(historical_input_uncommitted); revs must be commits ancestral to HEAD.
"""


class CouldNotEvaluate(Exception):
    """Input that prevents the disposition question from being evaluated."""

    def __init__(self, finding_id, detail):
        super().__init__(detail)
        self.finding_id = finding_id
        self.detail = detail


class UsageError(Exception):
    pass


# ------------------------------------------------------------------ utilities


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def tool_sha256():
    try:
        with open(SELF, "rb") as handle:
            return sha256_bytes(handle.read())
    except OSError:
        return None


def _reject_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("duplicate JSON key: {!r}".format(key))
        seen[key] = value
    return seen


def _reject_constant(token):
    raise ValueError("non-finite JSON constant: {}".format(token))


def parse_json_object(raw, label):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise CouldNotEvaluate(label + "_json_invalid", "not valid UTF-8")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        raise CouldNotEvaluate(label + "_json_invalid", "malformed JSON: {}".format(exc))
    if not isinstance(value, dict):
        raise CouldNotEvaluate(label + "_json_invalid", "top-level JSON value is not an object")
    return value


def _is_int(value):
    return type(value) is int


def _short(value, limit=180):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "..."


# --------------------------------------------------------------- safe reading


def canonical_relative(value, label):
    if not isinstance(value, str) or not value:
        raise CouldNotEvaluate("path_rejected", "{}: empty or non-string relative path".format(label))
    if "\x00" in value:
        raise CouldNotEvaluate("path_rejected", "{}: NUL byte in path".format(label))
    if "\\" in value:
        raise CouldNotEvaluate("path_rejected", "{}: backslash in path".format(label))
    pure = PurePosixPath(value)
    if pure.is_absolute():
        raise CouldNotEvaluate("path_rejected", "{}: absolute path".format(label))
    if any(part == ".." for part in pure.parts):
        raise CouldNotEvaluate("path_rejected", "{}: parent traversal".format(label))
    if str(pure) != value:
        raise CouldNotEvaluate(
            "path_rejected", "{}: non-canonical relative path {!r}".format(label, value)
        )
    if str(pure) == ".":
        raise CouldNotEvaluate("path_rejected", "{}: empty path".format(label))
    return pure


def safe_file(lane, relative, label):
    """Resolve a declared lane-relative path without escaping or symlinks."""
    pure = canonical_relative(relative, label)
    current = lane
    for part in pure.parts:
        current = current / part
        try:
            st = os.lstat(current)
        except FileNotFoundError:
            raise CouldNotEvaluate(label + "_missing", "{}: {}: missing".format(label, relative))
        except OSError as exc:
            raise CouldNotEvaluate(
                label + "_unreadable",
                "{}: {}: {}".format(label, relative, exc.strerror or exc),
            )
        if stat.S_ISLNK(st.st_mode):
            raise CouldNotEvaluate(
                "path_rejected", "{}: symlink component in {}".format(label, relative)
            )
    try:
        st = os.lstat(current)
    except OSError as exc:
        raise CouldNotEvaluate(
            label + "_unreadable", "{}: {}: {}".format(label, relative, exc.strerror or exc)
        )
    if not stat.S_ISREG(st.st_mode):
        raise CouldNotEvaluate("path_rejected", "{}: not a regular file".format(label))
    try:
        current.resolve().relative_to(lane)
    except ValueError:
        raise CouldNotEvaluate("path_rejected", "{}: resolves outside lane root".format(label))
    return current


def read_regular(path, label):
    """O_NOFOLLOW read; lstat/fstat identity checked; exactly one read."""
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        before = os.lstat(path)
    except FileNotFoundError:
        raise CouldNotEvaluate(label + "_missing", "{}: missing".format(label))
    except OSError as exc:
        raise CouldNotEvaluate(label + "_unreadable", "{}: {}".format(label, exc.strerror or exc))
    if not stat.S_ISREG(before.st_mode):
        raise CouldNotEvaluate("path_rejected", "{}: not a regular file".format(label))
    try:
        fd = os.open(path, flags)
    except FileNotFoundError:
        raise CouldNotEvaluate(label + "_missing", "{}: missing".format(label))
    except OSError as exc:
        raise CouldNotEvaluate(label + "_unreadable", "{}: {}".format(label, exc.strerror or exc))
    try:
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
            raise CouldNotEvaluate("path_rejected", "{}: file changed during read".format(label))
        if not stat.S_ISREG(after.st_mode):
            raise CouldNotEvaluate("path_rejected", "{}: not a regular file".format(label))
        chunks = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except OSError as exc:
        raise CouldNotEvaluate(label + "_unreadable", "{}: {}".format(label, exc.strerror or exc))
    finally:
        os.close(fd)


def read_dispositions(path):
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        raise CouldNotEvaluate("dispositions_missing", str(path))
    except OSError as exc:
        raise CouldNotEvaluate("dispositions_unreadable", "{}: {}".format(path, exc.strerror or exc))
    if stat.S_ISLNK(st.st_mode):
        raise CouldNotEvaluate("path_rejected", "dispositions: symlink")
    if not stat.S_ISREG(st.st_mode):
        raise CouldNotEvaluate("path_rejected", "dispositions: not a regular file")
    return read_regular(path, "dispositions")

# ------------------------------------------------- historical input reading

# G4: every git subprocess runs without inherited GIT_* state, without replace
# refs and without grafts, so environment/replace/graft attacks cannot rewrite
# the bytes this gate reads.
GIT_ENV_OVERRIDES = {
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_GRAFT_FILE": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": "/dev/null",
}


def _stderr_text(proc):
    if proc.stderr is None:
        return ""
    if isinstance(proc.stderr, bytes):
        return proc.stderr.decode("utf-8", "replace").strip()
    return str(proc.stderr).strip()


def git_environment():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_ENV_OVERRIDES)
    return env


def git_call(lane, argv, timeout=30):
    """Hermetic git subprocess (bytes, never text)."""
    try:
        return subprocess.run(
            ["git", "-C", str(lane)] + list(argv),
            capture_output=True,
            env=git_environment(),
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "git {}: {}".format(argv[0], exc),
        )


def _git_failure(proc, action):
    return CouldNotEvaluate(
        "historical_input_unavailable",
        "{}: {}".format(action, _stderr_text(proc) or "exit {}".format(proc.returncode)),
    )


def verify_repo(lane):
    """G4 identity/topology guard: <lane> is its own non-shallow work tree."""
    proc = git_call(lane, ["rev-parse", "--absolute-git-dir", "--show-toplevel"])
    if proc.returncode != 0:
        raise _git_failure(proc, "root is not inside a git work tree")
    lines = proc.stdout.decode("utf-8", "replace").splitlines()
    if len(lines) != 2:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "rev-parse --absolute-git-dir --show-toplevel returned {!r}".format(lines),
        )
    git_dir, toplevel = lines
    lane_real = os.path.realpath(str(lane))
    if os.path.realpath(toplevel) != lane_real:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "root is not the toplevel of its own work tree "
            "(git reports {!r})".format(toplevel),
        )
    if os.path.realpath(git_dir) != os.path.join(lane_real, ".git"):
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "git dir {!r} is not <root>/.git".format(git_dir),
        )
    proc = git_call(lane, ["rev-parse", "--is-shallow-repository"])
    if proc.returncode != 0 or proc.stdout.decode("utf-8", "replace").strip() != "false":
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "root is a shallow repository; historical blobs are not provable",
        )


def resolve_historical_rev(lane, rev):
    """G3: rev is exactly that commit id and a commit ancestor of HEAD."""
    proc = git_call(lane, ["rev-parse", "--verify", "--end-of-options", rev + "^{commit}"])
    resolved = proc.stdout.decode("utf-8", "replace").strip()
    if proc.returncode != 0 or resolved != rev:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "rev {!r} does not resolve to that commit (got {!r})".format(rev, resolved),
        )
    proc = git_call(lane, ["merge-base", "--is-ancestor", "--end-of-options", rev, "HEAD"])
    if proc.returncode != 0:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "rev {} is not an ancestor of HEAD".format(rev),
        )


TREE_MODES = ("100644", "100755")


def tree_entry(lane, rev, path):
    """(mode, type, object id) for <path> at <rev>, or None when absent."""
    proc = git_call(lane, ["ls-tree", "-z", "--full-tree", rev, "--", path])
    if proc.returncode != 0:
        raise _git_failure(proc, "ls-tree {}:{}".format(rev, path))
    records = [item for item in proc.stdout.split(b"\0") if item]
    if not records:
        return None
    if len(records) != 1:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "{}: ambiguous tree entries at {}".format(path, rev),
        )
    meta, _, name = records[0].partition(b"\t")
    fields = meta.decode("utf-8", "replace").split()
    if len(fields) != 3 or name.decode("utf-8", "replace") != path:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "{}: unparsable tree entry at {}".format(path, rev),
        )
    return fields[0], fields[1], fields[2]


def read_blob(lane, object_id, path):
    proc = git_call(lane, ["cat-file", "blob", object_id])
    if proc.returncode != 0:
        raise _git_failure(proc, "{}: blob {} unavailable".format(path, object_id))
    return proc.stdout


def live_regular_bytes(lane, path):
    """Live bytes only when every component is a real directory/file."""
    current = Path(lane)
    for part in PurePosixPath(path).parts:
        current = current / part
        try:
            st = os.lstat(current)
        except OSError:
            return None
        if stat.S_ISLNK(st.st_mode):
            return None
    if not stat.S_ISREG(st.st_mode):
        return None
    try:
        return read_regular(current, "historical_input")
    except CouldNotEvaluate:
        return None


def check_historical_waiver(lane, path, pin):
    """G1/G2: the waiver must be needed and the live move must be committed."""
    live = live_regular_bytes(lane, path)
    if live is not None and sha256_bytes(live) == pin:
        raise CouldNotEvaluate(
            "historical_input_unneeded",
            "{}: live bytes still equal the expected pin; the waiver is unnecessary".format(path),
        )
    head = tree_entry(lane, "HEAD", path)
    if live is None:
        if head is not None:
            raise CouldNotEvaluate(
                "historical_input_uncommitted",
                "{}: live path is absent or not a regular file but HEAD has an entry".format(path),
            )
        return
    if head is None:
        raise CouldNotEvaluate(
            "historical_input_uncommitted",
            "{}: live path is not present at HEAD".format(path),
        )
    if head[1] != "blob":
        raise CouldNotEvaluate(
            "historical_input_uncommitted",
            "{}: HEAD entry is a {} not a blob".format(path, head[1]),
        )
    if sha256_bytes(read_blob(lane, head[2], path)) != sha256_bytes(live):
        raise CouldNotEvaluate(
            "historical_input_uncommitted",
            "{}: live bytes differ from HEAD:{}".format(path, path),
        )


def historical_blob(lane, rev, path):
    """G5: regular blob (100644/100755) bytes at <rev>, never text."""
    entry = tree_entry(lane, rev, path)
    if entry is None:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "{}: absent at rev {}".format(path, rev),
        )
    mode, kind, object_id = entry
    if kind != "blob" or mode not in TREE_MODES:
        raise CouldNotEvaluate(
            "historical_input_unavailable",
            "{}: tree entry mode {} type {} is not a regular blob".format(path, mode, kind),
        )
    return read_blob(lane, object_id, path)


# ------------------------------------------------------------- schema checks


def validate_inputs(raw_inputs):
    if not isinstance(raw_inputs, dict) or not raw_inputs:
        raise CouldNotEvaluate("dispositions_field_invalid", "inputs must be a non-empty object")
    pinned = {}
    for key, digest in raw_inputs.items():
        pure = canonical_relative(key, "input")
        canonical = str(pure)
        if canonical in pinned:
            raise CouldNotEvaluate("path_rejected", "duplicate input pin for {}".format(canonical))
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            raise CouldNotEvaluate(
                "dispositions_field_invalid",
                "{}: sha256 must be 64 lowercase hex characters".format(key),
            )
        pinned[canonical] = digest
    return pinned


def validate_historical_inputs(raw):
    """v2 historical_inputs: tools/* paths read from a pinned git revision."""
    if not isinstance(raw, dict):
        raise CouldNotEvaluate(
            "dispositions_field_invalid", "historical_inputs must be an object"
        )
    historical = {}
    for key, entry in raw.items():
        canonical = str(canonical_relative(key, "historical_input"))
        if canonical in historical:
            raise CouldNotEvaluate(
                "path_rejected", "duplicate historical input {}".format(canonical)
            )
        if not canonical.startswith("tools/"):
            raise CouldNotEvaluate(
                "historical_input_forbidden",
                "{}: historical inputs must be tools/* paths".format(canonical),
            )
        if not isinstance(entry, dict):
            raise CouldNotEvaluate(
                "dispositions_field_invalid",
                "{}: historical input must be an object with rev and reason".format(canonical),
            )
        rev = entry.get("rev")
        if not isinstance(rev, str) or not HEX40.fullmatch(rev):
            raise CouldNotEvaluate(
                "dispositions_field_invalid",
                "{}: rev must be 40 lowercase hex characters".format(canonical),
            )
        reason = entry.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise CouldNotEvaluate(
                "dispositions_field_invalid",
                "{}: reason must be a non-empty string".format(canonical),
            )
        historical[canonical] = rev
    return historical


def receipt_canonical(value, expected_rel):
    if not isinstance(value, str) or not value:
        raise CouldNotEvaluate("dispositions_field_invalid", "receipt must be a non-empty string")
    canonical = str(canonical_relative(value, "receipt"))
    if PurePosixPath(canonical).parent != PurePosixPath(expected_rel).parent:
        raise CouldNotEvaluate(
            "receipt_out_of_scope",
            "receipt {} is not in the expected file's directory".format(canonical),
        )
    return canonical


def validate_rows(raw_rows, expected_rel, pinned):
    if not isinstance(raw_rows, list) or not raw_rows:
        raise CouldNotEvaluate("dispositions_field_invalid", "rows must be a non-empty list")
    rows = []
    for index, row in enumerate(raw_rows):
        if not isinstance(row, dict):
            raise CouldNotEvaluate("row_invalid", "rows[{}] is not an object".format(index))
        name = row.get("name")
        state = row.get("state")
        if not isinstance(name, str) or not name:
            raise CouldNotEvaluate("row_invalid", "rows[{}]: name must be a non-empty string".format(index))
        if state == "effective":
            if set(row) != EFFECTIVE_KEYS:
                raise CouldNotEvaluate(
                    "row_invalid",
                    "{}: effective row keys must be exactly {}".format(
                        name, ", ".join(sorted(EFFECTIVE_KEYS))
                    ),
                )
            receipt = row.get("receipt")
            check = row.get("check")
            if not isinstance(check, str) or not check:
                raise CouldNotEvaluate("row_invalid", "{}: check must be a non-empty string".format(name))
            receipt_rel = receipt_canonical(receipt, expected_rel)
            if receipt_rel not in pinned:
                raise CouldNotEvaluate(
                    "input_unpinned", "{}: receipt {} is not pinned in inputs".format(name, receipt_rel)
                )
            rows.append(
                {"name": name, "state": "effective", "receipt_rel": receipt_rel, "check": check}
            )
        elif state == "superseded":
            if set(row) != SUPERSEDED_KEYS:
                raise CouldNotEvaluate(
                    "row_invalid",
                    "{}: superseded row keys must be exactly {}".format(
                        name, ", ".join(sorted(SUPERSEDED_KEYS))
                    ),
                )
            reason = row.get("reason")
            raw_check = row.get("raw_check")
            replacements = row.get("superseded_by")
            if not isinstance(reason, str):
                raise CouldNotEvaluate("row_invalid", "{}: reason must be a string".format(name))
            if not isinstance(raw_check, str) or not raw_check:
                raise CouldNotEvaluate("row_invalid", "{}: raw_check must be a non-empty string".format(name))
            if not isinstance(replacements, list) or not all(
                isinstance(item, str) and item for item in replacements
            ):
                raise CouldNotEvaluate(
                    "row_invalid", "{}: superseded_by must be a list of non-empty names".format(name)
                )
            raw_rel = receipt_canonical(row.get("raw_receipt"), expected_rel)
            if raw_rel not in pinned:
                raise CouldNotEvaluate(
                    "input_unpinned", "{}: raw_receipt {} is not pinned in inputs".format(name, raw_rel)
                )
            rows.append(
                {
                    "name": name,
                    "state": "superseded",
                    "reason": reason,
                    "raw_rel": raw_rel,
                    "raw_check": raw_check,
                    "superseded_by": list(replacements),
                }
            )
        else:
            raise CouldNotEvaluate(
                "row_invalid", "{}: state must be 'effective' or 'superseded'".format(name)
            )
    return rows


def validate_expectation(name, spec):
    if not isinstance(spec, dict):
        raise CouldNotEvaluate("expectation_invalid", "{}: expectation is not an object".format(name))
    unknown = sorted(set(spec) - EXPECTATION_FIELDS)
    if unknown:
        raise CouldNotEvaluate(
            "expectation_invalid", "{}: unsupported expectation field(s) {}".format(name, ", ".join(unknown))
        )
    if "exit" not in spec or not _is_int(spec["exit"]):
        raise CouldNotEvaluate("expectation_invalid", "{}: exit must be an integer".format(name))
    for field in ("contains", "id", "reason", "result_reuse"):
        if field in spec and (not isinstance(spec[field], str) or not spec[field]):
            raise CouldNotEvaluate(
                "expectation_invalid", "{}: {} must be a non-empty string".format(name, field)
            )
    if "rows" in spec and (not _is_int(spec["rows"]) or spec["rows"] < 0):
        raise CouldNotEvaluate("expectation_invalid", "{}: rows must be a non-negative integer".format(name))
    if "statuses" in spec:
        statuses = spec["statuses"]
        if not isinstance(statuses, dict) or not statuses:
            raise CouldNotEvaluate("expectation_invalid", "{}: statuses must be a non-empty object".format(name))
        for key, count in statuses.items():
            if not isinstance(key, str) or not key:
                raise CouldNotEvaluate("expectation_invalid", "{}: status name must be a string".format(name))
            if not _is_int(count) or count < 0:
                raise CouldNotEvaluate(
                    "expectation_invalid", "{}: status {} must be a non-negative integer".format(name, key)
                )
    return spec


def validate_expected(expected):
    raw_inputs = expected.get("inputs")
    if not isinstance(raw_inputs, dict) or not raw_inputs:
        raise CouldNotEvaluate("expected_structure_invalid", "expected.inputs must be a non-empty object")
    expected_inputs = {}
    for key, digest in raw_inputs.items():
        canonical = str(canonical_relative(key, "expected_input"))
        if canonical in expected_inputs:
            raise CouldNotEvaluate(
                "expected_structure_invalid", "duplicate expected input path {}".format(canonical)
            )
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            raise CouldNotEvaluate(
                "expected_structure_invalid",
                "{}: sha256 must be 64 lowercase hex characters".format(key),
            )
        expected_inputs[canonical] = digest
    raw_checks = expected.get("expected_checks")
    if not isinstance(raw_checks, dict) or not raw_checks:
        raise CouldNotEvaluate(
            "expected_structure_invalid", "expected.expected_checks must be a non-empty object"
        )
    checks = {}
    for name, spec in raw_checks.items():
        if not isinstance(name, str) or not name:
            raise CouldNotEvaluate(
                "expected_structure_invalid", "expected check name must be a non-empty string"
            )
        checks[name] = validate_expectation(name, spec)
    return checks, expected_inputs


def load_receipts(used_receipts, input_bytes):
    maps = {}
    docs = {}
    owners = defaultdict(list)
    for canonical in sorted(used_receipts):
        if canonical not in input_bytes:
            raise CouldNotEvaluate("internal_error", "receipt bytes unavailable: {}".format(canonical))
        doc = parse_json_object(input_bytes[canonical], "receipt")
        checks = doc.get("checks")
        if not isinstance(checks, list):
            raise CouldNotEvaluate(
                "receipt_structure_invalid", "{}: checks must be a list".format(canonical)
            )
        by_name = {}
        for check in checks:
            if not isinstance(check, dict):
                raise CouldNotEvaluate(
                    "receipt_check_invalid", "{}: check entry is not an object".format(canonical)
                )
            name = check.get("name")
            if not isinstance(name, str) or not name:
                raise CouldNotEvaluate(
                    "receipt_check_invalid", "{}: check name must be a non-empty string".format(canonical)
                )
            if name in by_name:
                raise CouldNotEvaluate(
                    "receipt_check_duplicate", "{}: duplicate check {!r}".format(canonical, name)
                )
            if not _is_int(check.get("exit")):
                raise CouldNotEvaluate(
                    "receipt_check_invalid",
                    "{}:{}: exit must be an integer (bool is not an exit)".format(canonical, name),
                )
            if not isinstance(check.get("stdout"), str):
                raise CouldNotEvaluate(
                    "receipt_check_invalid", "{}:{}: stdout must be a string".format(canonical, name)
                )
            if "stderr" in check and not isinstance(check["stderr"], str):
                raise CouldNotEvaluate(
                    "receipt_check_invalid", "{}:{}: stderr must be a string".format(canonical, name)
                )
            by_name[name] = check
            owners[name].append(canonical)
        maps[canonical] = by_name
        docs[canonical] = doc
    for name in sorted(owners):
        if len(owners[name]) > 1:
            raise CouldNotEvaluate(
                "receipt_check_ambiguous",
                "check {!r} appears in multiple receipts: {}".format(
                    name, ", ".join(sorted(owners[name]))
                ),
            )
    return maps, docs


# ---------------------------------------------------------------- predicates


def _structured_object(stdout):
    try:
        value = json.loads(stdout, parse_constant=_reject_constant)
    except (ValueError, TypeError):
        return None
    return value if isinstance(value, dict) else None


def _row_candidates(parsed):
    candidates = []
    if "rows" in parsed:
        value = parsed["rows"]
        if _is_int(value) and value >= 0:
            candidates.append(("rows", value))
        elif isinstance(value, list):
            candidates.append(("rows.length", len(value)))
    counts = parsed.get("counts")
    if isinstance(counts, dict) and _is_int(counts.get("legs")) and counts["legs"] >= 0:
        candidates.append(("counts.legs", counts["legs"]))
    legs = parsed.get("legs")
    if isinstance(legs, list):
        candidates.append(("legs.length", len(legs)))
    return candidates


def _status_sources(parsed, expected_keys):
    sources = []
    statuses = parsed.get("statuses")
    if isinstance(statuses, dict):
        sources.append(("statuses", statuses))
    counts = parsed.get("counts")
    if isinstance(counts, dict):
        sources.append(("counts", counts))
    legs = parsed.get("legs")
    if isinstance(legs, list) and all(
        isinstance(item, dict) and isinstance(item.get("content_status"), str) for item in legs
    ):
        histogram = {
            key: sum(1 for item in legs if item["content_status"] == key) for key in expected_keys
        }
        sources.append(("legs.content_status", histogram))
    return sources


def _result_reuse_candidates(parsed):
    values = []
    if "result_reuse" in parsed:
        values.append(("result_reuse", parsed["result_reuse"]))
    legs = parsed.get("legs")
    if isinstance(legs, list) and legs:
        for index, item in enumerate(legs):
            if isinstance(item, dict) and "result_reuse" in item:
                values.append(("legs[{}].result_reuse".format(index), item["result_reuse"]))
    return values


def evaluate_expectation(name, spec, observed):
    collected = {}

    def add(finding_id, detail):
        collected.setdefault(finding_id, []).append(detail)

    if observed["exit"] != spec["exit"]:
        add(
            "expected_exit_mismatch",
            "observed exit {} expects {}".format(observed["exit"], spec["exit"]),
        )

    stdout = observed["stdout"]
    if "contains" in spec and spec["contains"] not in stdout:
        add("expected_contains_missing", "stdout lacks {}".format(_short(spec["contains"], 120)))

    structured_fields = [
        field
        for field in ("id", "reason", "rows", "statuses", "result_reuse")
        if field in spec
    ]
    parsed = None
    if structured_fields:
        parsed = _structured_object(stdout)
        if parsed is None:
            add(
                "expected_stdout_not_json",
                "fields {} require one JSON object on stdout".format(", ".join(structured_fields)),
            )

    if parsed is not None:
        if "id" in spec and parsed.get("id") != spec["id"]:
            add("expected_id_mismatch", "observed {} expects {}".format(_short(parsed.get("id")), _short(spec["id"])))
        if "reason" in spec and parsed.get("reason") != spec["reason"]:
            add(
                "expected_reason_mismatch",
                "observed {} expects {}".format(_short(parsed.get("reason")), _short(spec["reason"])),
            )
        if "rows" in spec:
            candidates = _row_candidates(parsed)
            values = sorted({value for _source, value in candidates})
            if not candidates:
                add("expected_rows_mismatch", "no observed row count source")
            elif len(values) != 1:
                add(
                    "expected_rows_mismatch",
                    "observed row counts disagree: {}".format(
                        ", ".join("{}={}".format(source, value) for source, value in candidates)
                    ),
                )
            elif values[0] != spec["rows"]:
                add(
                    "expected_rows_mismatch",
                    "observed {!r} expects {!r}".format(values[0], spec["rows"]),
                )
        if "statuses" in spec:
            sources = _status_sources(parsed, list(spec["statuses"]))
            if not sources:
                add("expected_statuses_mismatch", "no observed status histogram source")
            for key, expected_count in spec["statuses"].items():
                observed_counts = []
                for source, mapping in sources:
                    if key in mapping:
                        observed_counts.append((source, mapping[key]))
                if not observed_counts:
                    add("expected_statuses_mismatch", "status {!r} has no observed source".format(key))
                    continue
                bad = []
                for source, value in observed_counts:
                    if not _is_int(value) or value != expected_count:
                        bad.append("{}={!r}".format(source, value))
                if bad:
                    add(
                        "expected_statuses_mismatch",
                        "status {!r} expects {} observed {}".format(
                            key, expected_count, ", ".join(bad)
                        ),
                    )
        if "result_reuse" in spec:
            candidates = _result_reuse_candidates(parsed)
            if not candidates:
                add("expected_result_reuse_mismatch", "no observed result_reuse value")
            for source, value in candidates:
                if value != spec["result_reuse"]:
                    add(
                        "expected_result_reuse_mismatch",
                        "{}={!r} expects {!r}".format(source, value, spec["result_reuse"]),
                    )
    return [
        {
            "id": finding_id,
            "detail": "{}: {}".format(name, "; ".join(details)),
        }
        for finding_id, details in collected.items()
    ]


def cycle_nodes(graph):
    """Names participating in a superseded_by cycle."""
    color = {name: 0 for name in graph}
    found = set()
    path = []

    def visit(node):
        color[node] = 1
        path.append(node)
        for target in graph.get(node, ()):
            if target not in graph:
                continue
            if color[target] == 1:
                found.update(path[path.index(target):])
            elif color[target] == 0:
                visit(target)
        path.pop()
        color[node] = 2

    for name in sorted(graph):
        if color[name] == 0:
            visit(name)
    return found


# ------------------------------------------------------------------ evaluation


def add_finding(findings, findings_by_name, finding_id, expectation, detail):
    findings.append({"id": finding_id, "expectation": expectation, "detail": detail})
    if isinstance(expectation, str) and expectation:
        findings_by_name[expectation].append(finding_id)


def evaluate_dispositions(checks, rows, expected_inputs, receipt_maps, receipt_docs, expected_rel):
    expected_order = list(checks.keys())
    expected_parent = PurePosixPath(expected_rel).parent
    rows_by_name = defaultdict(list)
    for row in rows:
        rows_by_name[row["name"]].append(row)

    findings = []
    findings_by_name = defaultdict(list)

    for name in sorted(rows_by_name):
        if len(rows_by_name[name]) > 1:
            add_finding(
                findings,
                findings_by_name,
                "row_duplicate",
                name,
                "{} rows declare this name".format(len(rows_by_name[name])),
            )
    for name in sorted(rows_by_name):
        if name not in checks:
            add_finding(
                findings,
                findings_by_name,
                "row_unknown",
                name,
                "row name is not an expected_checks key",
            )
    for name in expected_order:
        if name not in rows_by_name:
            add_finding(
                findings,
                findings_by_name,
                "row_missing",
                name,
                "expected check has no disposition row",
            )

    unique_rows = {name: group[0] for name, group in rows_by_name.items() if len(group) == 1}
    records_by_name = {}
    row_outcomes = {}

    # Phase 1: effective rows.
    for name in expected_order:
        group = rows_by_name.get(name, [])
        if not group:
            records_by_name[name] = {
                "name": name,
                "state": None,
                "outcome": "missing",
                "mismatches": ["row_missing"],
            }
            continue
        if len(group) > 1:
            records_by_name[name] = {
                "name": name,
                "state": None,
                "outcome": "duplicate",
                "mismatches": ["row_duplicate"],
            }
            continue
        row = unique_rows[name]
        if row["state"] != "effective":
            continue
        spec = checks[name]
        if row["check"] != name:
            add_finding(
                findings,
                findings_by_name,
                "effective_check_name_mismatch",
                name,
                "check {!r} does not equal row name".format(row["check"]),
            )
        observed = receipt_maps.get(row["receipt_rel"], {}).get(row["check"])
        if observed is None:
            add_finding(
                findings,
                findings_by_name,
                "receipt_check_missing",
                name,
                "receipt {} has no check {!r}".format(row["receipt_rel"], row["check"]),
            )
            mismatches = [{"id": "receipt_check_missing", "detail": name}]
        else:
            mismatches = evaluate_expectation(name, spec, observed)
            for mismatch in mismatches:
                add_finding(
                    findings,
                    findings_by_name,
                    mismatch["id"],
                    name,
                    mismatch["detail"],
                )
        failed = bool(mismatches) or row["check"] != name
        row_outcomes[name] = {"failed": failed, "mismatches": mismatches}
        records_by_name[name] = {
            "name": name,
            "state": "effective",
            "receipt": row["receipt_rel"],
            "check": row["check"],
            "expected_exit": spec["exit"],
            "observed_exit": observed["exit"] if observed is not None else None,
            "outcome": "fail" if failed else "pass",
            "mismatches": sorted({mismatch["id"] for mismatch in mismatches}),
        }

    # Phase 2: superseded rows.
    superseded_graph = {}
    for name, row in unique_rows.items():
        if name in checks and row["state"] == "superseded":
            targets = []
            for target in dict.fromkeys(row["superseded_by"]):
                if target in unique_rows and unique_rows[target]["state"] == "superseded":
                    targets.append(target)
            superseded_graph[name] = targets
    for name in sorted(cycle_nodes(superseded_graph)):
        add_finding(
            findings,
            findings_by_name,
            "superseded_cycle",
            name,
            "superseded_by graph contains a cycle",
        )

    for name in expected_order:
        group = rows_by_name.get(name, [])
        if len(group) != 1:
            continue
        row = unique_rows[name]
        if row["state"] != "superseded":
            continue
        policy = SUPERSEDED_POLICY.get(name)
        raw_mismatches = []
        raw_retained = False
        raw_receipt = row["raw_rel"]
        raw_check = row["raw_check"]

        if not row["reason"].strip():
            add_finding(
                findings,
                findings_by_name,
                "superseded_reason_missing",
                name,
                "reason is empty",
            )

        if policy is None:
            add_finding(
                findings,
                findings_by_name,
                "supersession_not_permitted",
                name,
                "only producer_before may be superseded in round 14",
            )
        else:
            expected_raw = str(expected_parent / policy["raw_receipt"])
            if row["raw_rel"] != expected_raw or row["raw_check"] != policy["raw_check"]:
                add_finding(
                    findings,
                    findings_by_name,
                    "superseded_raw_binding_mismatch",
                    name,
                    "raw observation must bind {}:{}".format(expected_raw, policy["raw_check"]),
                )
            else:
                observed = receipt_maps.get(row["raw_rel"], {}).get(row["raw_check"])
                if observed is None:
                    add_finding(
                        findings,
                        findings_by_name,
                        "superseded_raw_missing",
                        name,
                        "raw receipt {} has no check {!r}".format(row["raw_rel"], row["raw_check"]),
                    )
                else:
                    raw_retained = True
                    raw_mismatches = evaluate_expectation(name, checks[name], observed)
                    if not raw_mismatches:
                        add_finding(
                            findings,
                            findings_by_name,
                            "supersession_unwarranted",
                            name,
                            "retained raw observation satisfies its original expectation",
                        )

            declared = list(row["superseded_by"])
            if len(set(declared)) != len(declared):
                add_finding(
                    findings,
                    findings_by_name,
                    "superseded_by_invalid",
                    name,
                    "duplicate replacement names",
                )
            required = list(policy["replacements"])
            missing = [target for target in required if target not in declared]
            extra = [target for target in declared if target not in required]
            if missing:
                add_finding(
                    findings,
                    findings_by_name,
                    "superseded_required_replacement_missing",
                    name,
                    "missing required replacement(s): {}".format(", ".join(missing)),
                )
            if extra:
                add_finding(
                    findings,
                    findings_by_name,
                    "superseded_replacement_not_allowed",
                    name,
                    "not an allowed replacement: {}".format(", ".join(extra)),
                )

            expected_oracle = str(expected_parent / ORACLE_RECEIPT)
            oracle_doc = receipt_docs.get(expected_oracle)
            binding_problems = []
            if oracle_doc is None:
                binding_problems.append("oracle receipt {} is not available".format(expected_oracle))
            else:
                supersedes = oracle_doc.get("supersedes")
                if not isinstance(supersedes, str) or not supersedes.startswith(
                    ORACLE_SUPERSEDES_PREFIX
                ):
                    binding_problems.append(
                        "oracle receipt does not declare {!r}".format(ORACLE_SUPERSEDES_PREFIX)
                    )
                oracle_input = str(expected_parent / ORACLE_INPUT)
                pinned_oracle = expected_inputs.get(oracle_input)
                if pinned_oracle is None or oracle_doc.get("oracle_sha256") != pinned_oracle:
                    binding_problems.append(
                        "oracle_sha256 does not equal expected.inputs[{}]".format(oracle_input)
                    )
            if binding_problems:
                add_finding(
                    findings,
                    findings_by_name,
                    "superseded_oracle_binding_missing",
                    name,
                    "; ".join(binding_problems),
                )

            for target in dict.fromkeys(declared):
                if target not in checks or target not in rows_by_name:
                    add_finding(
                        findings,
                        findings_by_name,
                        "superseded_by_unknown",
                        name,
                        "replacement {!r} is not an expected row".format(target),
                    )
                    continue
                target_group = rows_by_name[target]
                if len(target_group) != 1 or target_group[0]["state"] != "effective":
                    add_finding(
                        findings,
                        findings_by_name,
                        "superseded_target_not_effective",
                        name,
                        "replacement {!r} is not a unique effective row".format(target),
                    )
                    continue
                if target_group[0]["receipt_rel"] != expected_oracle:
                    add_finding(
                        findings,
                        findings_by_name,
                        "superseded_replacement_not_allowed",
                        name,
                        "replacement {!r} does not bind {}".format(target, expected_oracle),
                    )
                outcome = row_outcomes.get(target)
                if outcome is not None and outcome["failed"]:
                    ids = sorted({mismatch["id"] for mismatch in outcome["mismatches"]})
                    if target_group[0]["check"] != target:
                        ids.append("effective_check_name_mismatch")
                    add_finding(
                        findings,
                        findings_by_name,
                        "superseded_replacement_failed",
                        name,
                        "replacement {!r} fails: {}".format(
                            target, ", ".join(sorted(set(ids))) or "identity mismatch"
                        ),
                    )

        records_by_name[name] = {
            "name": name,
            "state": "superseded",
            "reason": row["reason"],
            "raw_receipt": raw_receipt,
            "raw_check": raw_check,
            "raw_retained": raw_retained,
            "raw_expectation_failed": bool(raw_mismatches),
            "raw_mismatches": sorted({mismatch["id"] for mismatch in raw_mismatches}),
            "replacements": list(dict.fromkeys(row["superseded_by"])),
            "outcome": "fail" if findings_by_name.get(name) else "superseded",
            "mismatches": sorted(set(findings_by_name.get(name, []))),
        }

    # Final pass: non-predicate findings (identity, selection, policy) fail rows.
    for name, record in records_by_name.items():
        if record.get("state") == "effective" and record["outcome"] == "pass":
            extra = [item for item in findings_by_name.get(name, []) if item not in record["mismatches"]]
            if extra:
                record["outcome"] = "fail"
                record["mismatches"] = sorted(set(record["mismatches"]) | set(extra))

    records = [records_by_name[name] for name in expected_order]
    findings = sorted(
        findings,
        key=lambda item: (item["id"], item["expectation"] or "", item["detail"]),
    )

    informational = []
    for canonical in sorted(receipt_maps):
        for check_name in sorted(receipt_maps[canonical]):
            if check_name not in checks:
                informational.append({"receipt": canonical, "check": check_name})

    return records, findings, informational


# --------------------------------------------------------------------- output


def base_payload(status, exit_code):
    return {
        "schema": RESULT_SCHEMA,
        "tool": VERSION,
        "tool_sha256": tool_sha256(),
        "status": status,
        "exit": exit_code,
    }


def emit_could_not_evaluate(exc, as_json):
    payload = base_payload("could_not_evaluate", 2)
    payload["id"] = exc.finding_id
    payload["error"] = {"kind": exc.finding_id, "message": exc.detail}
    payload["findings"] = [
        {"id": exc.finding_id, "expectation": None, "detail": exc.detail}
    ]
    if as_json:
        sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    else:
        sys.stdout.write(
            "EVIDENCE_DISPOSITION: could_not_evaluate exit=2 id={} detail={}\n".format(
                exc.finding_id, exc.detail
            )
        )
    return 2


def emit_result(payload, as_json):
    if as_json:
        sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return payload["exit"]
    counts = payload["counts"]
    sys.stdout.write(
        "EVIDENCE_DISPOSITION: {} exit={} expected={} effective={} superseded={} "
        "passed={} failed={} findings={}\n".format(
            payload["status"],
            payload["exit"],
            counts["expected_checks"],
            counts["effective"],
            counts["superseded"],
            counts["passed"],
            counts["failed"],
            counts["findings"],
        )
    )
    for record in payload["rows"]:
        sys.stdout.write(
            "ROW {} state={} outcome={} receipt={} check={} mismatches={}\n".format(
                record["name"],
                record.get("state"),
                record["outcome"],
                record.get("receipt", record.get("raw_receipt", "-")),
                record.get("check", record.get("raw_check", "-")),
                ",".join(record.get("mismatches", [])) or "-",
            )
        )
    for finding in payload["findings"]:
        sys.stdout.write(
            "FINDING {} expectation={} {}\n".format(
                finding["id"], finding["expectation"] or "-", finding["detail"]
            )
        )
    for line in payload.get("historical_text", ()):
        sys.stdout.write(line + "\n")
    return payload["exit"]


# ----------------------------------------------------------------- run mode


def check_supersedes_lineage(dispositions, supersedes_rel, expected_rel, pinned, input_bytes):
    """G7: `supersedes` must name a v1 manifest this document actually extends."""
    doc = parse_json_object(input_bytes[supersedes_rel], "supersedes")
    problems = []
    if doc.get("schema") != SCHEMA:
        problems.append("superseded document schema is not {!r}".format(SCHEMA))
    if doc.get("expected_file") != expected_rel:
        problems.append("superseded expected_file differs")
    if doc.get("rows") != dispositions.get("rows"):
        problems.append("superseded rows differ from this document's rows")
    superseded_inputs = doc.get("inputs")
    if not isinstance(superseded_inputs, dict):
        problems.append("superseded inputs is not an object")
    else:
        for key, digest in superseded_inputs.items():
            if pinned.get(key) != digest:
                problems.append("superseded input {} is not pinned identically".format(key))
    if problems:
        raise CouldNotEvaluate("supersedes_mismatch", "; ".join(problems))




def run_mode(root, dispositions_path, as_json):
    lane = Path(root).resolve()
    if not lane.is_dir():
        raise CouldNotEvaluate("root_unavailable", "lane root is not a directory: {}".format(root))

    dispositions_file = Path(dispositions_path)
    raw_dispositions = read_dispositions(dispositions_file)
    dispositions = parse_json_object(raw_dispositions, "dispositions")
    schema = dispositions.get("schema")
    if schema not in SCHEMAS:
        # v1-visible text: this detail must stay byte-identical to r14.
        raise CouldNotEvaluate(
            "schema_mismatch",
            "dispositions schema must be {!r}".format(SCHEMA),
        )

    supersedes_rel = None
    historical = {}
    if schema == SCHEMA_V2:
        supersedes_value = dispositions.get("supersedes")
        if not isinstance(supersedes_value, str):
            raise CouldNotEvaluate(
                "dispositions_field_invalid",
                "supersedes must be a lane-relative path string",
            )
        supersedes_rel = str(canonical_relative(supersedes_value, "supersedes"))
        historical = validate_historical_inputs(dispositions.get("historical_inputs"))

    expected_rel = str(canonical_relative(dispositions.get("expected_file"), "expected_file"))
    pinned = validate_inputs(dispositions.get("inputs"))
    if expected_rel not in pinned:
        raise CouldNotEvaluate(
            "input_unpinned", "expected file {} is not pinned in inputs".format(expected_rel)
        )
    expected_parent = PurePosixPath(expected_rel).parent
    for basename in REQUIRED_RECEIPTS:
        canonical = str(expected_parent / basename)
        if canonical not in pinned:
            raise CouldNotEvaluate(
                "input_unpinned", "required receipt {} is not pinned in inputs".format(canonical)
            )
    if schema == SCHEMA_V2 and supersedes_rel not in pinned:
        raise CouldNotEvaluate(
            "input_unpinned",
            "supersedes document {} is not pinned in inputs".format(supersedes_rel),
        )

    rows = validate_rows(dispositions.get("rows"), expected_rel, pinned)

    used_receipts = set()
    for row in rows:
        if row["state"] == "effective":
            used_receipts.add(row["receipt_rel"])
        else:
            used_receipts.add(row["raw_rel"])
    for basename in REQUIRED_RECEIPTS:
        used_receipts.add(str(expected_parent / basename))

    # INTEGRITY FIRST: hash every declared pin exactly once, before any
    # expectation predicate. The cached bytes are parsed below, never re-read.
    input_bytes = {}
    for canonical in sorted(pinned):
        label = "expected_file" if canonical == expected_rel else "input"
        path = safe_file(lane, canonical, label)
        data = read_regular(path, label)
        actual = sha256_bytes(data)
        if actual != pinned[canonical]:
            raise CouldNotEvaluate(
                "input_digest_mismatch",
                "{}: observed {} expects {}".format(canonical, actual, pinned[canonical]),
            )
        input_bytes[canonical] = data

    if schema == SCHEMA_V2:
        check_supersedes_lineage(
            dispositions, supersedes_rel, expected_rel, pinned, input_bytes
        )

    expected = parse_json_object(input_bytes[expected_rel], "expected")
    checks, expected_inputs = validate_expected(expected)

    # Every original expected.inputs digest is verified in full before any
    # predicate runs; a changed historical input is not evaluation material.
    # v2 historical_inputs are classified BEFORE any live read of those paths:
    # a waived path is never opened through safe_file/read_regular here.
    historical_unknown = sorted(set(historical) - set(expected_inputs))
    if historical_unknown:
        raise CouldNotEvaluate(
            "historical_input_unknown",
            "not in expected.inputs: {}".format(", ".join(historical_unknown)),
        )
    historical_shas = {}
    if historical:
        verify_repo(lane)
        for rev in sorted(set(historical.values())):
            resolve_historical_rev(lane, rev)
        for canonical in sorted(historical):
            check_historical_waiver(lane, canonical, expected_inputs[canonical])
    for canonical in sorted(expected_inputs):
        if canonical in historical:
            data = historical_blob(lane, historical[canonical], canonical)
        else:
            path = safe_file(lane, canonical, "expected_input")
            data = read_regular(path, "expected_input")
        actual = sha256_bytes(data)
        if actual != expected_inputs[canonical]:
            raise CouldNotEvaluate(
                "expected_input_digest_mismatch",
                "{}: observed {} expects {}".format(canonical, actual, expected_inputs[canonical]),
            )
        if canonical in historical:
            historical_shas[canonical] = actual

    receipt_maps, receipt_docs = load_receipts(used_receipts, input_bytes)
    records, findings, informational = evaluate_dispositions(
        checks,
        rows,
        expected_inputs,
        receipt_maps,
        receipt_docs,
        expected_rel,
    )

    exit_code = 1 if findings else 0
    status = "failed" if findings else "clean"
    payload = base_payload(status, exit_code)
    payload["root"] = str(lane)
    payload["dispositions"] = str(dispositions_file)
    payload["expected_file"] = expected_rel
    payload["counts"] = {
        "expected_checks": len(checks),
        "effective": sum(1 for record in records if record.get("state") == "effective"),
        "superseded": sum(1 for record in records if record.get("state") == "superseded"),
        "passed": sum(1 for record in records if record["outcome"] == "pass"),
        "failed": sum(
            1 for record in records if record["outcome"] in ("fail", "missing", "duplicate")
        ),
        "findings": len(findings),
    }
    payload["rows"] = records
    payload["findings"] = findings
    payload["informational"] = {"receipt_only_checks": informational}
    payload["inputs_verified"] = sorted(pinned)
    payload["expected_inputs_verified"] = sorted(expected_inputs)
    if schema == SCHEMA_V2:
        payload["supersedes"] = supersedes_rel
        payload["expected_inputs_historical"] = {
            canonical: historical[canonical] for canonical in sorted(historical)
        }
        payload["historical_text"] = [
            "HISTORICAL {} rev={} sha256={}".format(
                canonical, historical[canonical], historical_shas[canonical]
            )
            for canonical in sorted(historical)
        ]
    return emit_result(payload, as_json)


# ------------------------------------------------------------------- selftest

SELFTEST_ORACLE_PY = b"# tameshi round-14 oracle fixture (never executed)\n"
SELFTEST_FIXTURE_INPUT = b"pinned-input\n"
SELFTEST_TOOL_REL = "tools/pinned-tool.py"
SELFTEST_TOOL_V1 = b"# pinned tool fixture v1\n"
SELFTEST_TOOL_V2 = b"# pinned tool fixture v2 (drifted live)\n"
SELFTEST_TOOL_OTHER = b"# pinned tool fixture other rev (unexpected bytes)\n"
SELFTEST_TOOL_CRLF = b"#!/bin/sh\r\necho crlf-fixture\r\n"
SELFTEST_V1_REL = "docs/v1-manifest.json"
SELFTEST_V1_DOC = b'{"schema": "evidence-dispositions-v1"}\n'


def _json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _write_bytes(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _sha(payload):
    return sha256_bytes(payload)


def _build_lane(lane, marker, variant):
    lane.mkdir(parents=True, exist_ok=True)
    evidence = lane / ".ufo" / "evidence" / "round-13"
    evidence.mkdir(parents=True, exist_ok=True)
    fixture_input = lane / "fixtures" / "input.txt"
    _write_bytes(fixture_input, SELFTEST_FIXTURE_INPUT)
    tool_bytes = variant.get("tool_bytes", SELFTEST_TOOL_V1)
    _write_bytes(lane / "tools" / "pinned-tool.py", tool_bytes)
    oracle_py = evidence / "producer-oracle.py"
    _write_bytes(oracle_py, SELFTEST_ORACLE_PY)
    oracle_input_digest = _sha(SELFTEST_ORACLE_PY)

    expected_checks = {
        "alpha": {"exit": 0, "contains": "ALPHA_OK"},
        "beta": {"exit": 1, "id": "beta_bad", "reason": "beta_reason"},
        "gamma": {"exit": 0, "contains": "GAMMA_OK", "id": "gamma_ok", "reason": "ok"},
        "pin_live": {
            "exit": 0,
            "rows": 2,
            "statuses": {"changed": 1, "unchanged": 1, "unavailable": 0},
            "result_reuse": "not_established",
        },
        "producer_before": {"exit": 1, "contains": "kind FAIL"},
        "producer_before_oracle": {"exit": 1, "contains": "kind FAIL"},
        "producer_after_oracle": {"exit": 0, "contains": "41/41 pass"},
    }
    for name, override in variant.get("expected_checks", {}).items():
        expected_checks[name] = override

    expected = {
        "schema": "tameshi-round13-evidence-v1",
        "baseline": "0" * 40,
        "inputs": {
            "fixtures/input.txt": _sha(SELFTEST_FIXTURE_INPUT),
            ".ufo/evidence/round-13/producer-oracle.py": oracle_input_digest,
            "tools/pinned-tool.py": _sha(tool_bytes),
        },
        "expected_checks": expected_checks,
    }
    expected_bytes = _json_bytes(expected)
    _write_bytes(evidence / "expected.json", expected_bytes)

    alpha_exit = variant.get("alpha_exit", 0)
    alpha_stdout = variant.get("alpha_stdout", "ALPHA_OK\n")
    verification_checks = [
        {
            "name": "alpha",
            "argv": ["python3", "-c", "print('ALPHA_OK')"],
            "exit": alpha_exit,
            "stdout": alpha_stdout,
            "stderr": "",
        },
        {
            "name": "beta",
            "argv": ["python3", "-c", "raise SystemExit(1)"],
            "exit": 1,
            "stdout": json.dumps(
                {
                    "id": variant.get("beta_id", "beta_bad"),
                    "reason": variant.get("beta_reason", "beta_reason"),
                    "exit": 1,
                }
            )
            + "\n",
            "stderr": "",
        },
        {
            "name": "gamma",
            "argv": ["python3", "-c", "raise SystemExit(0)"],
            "exit": 0,
            "stdout": json.dumps(
                {"id": "gamma_ok", "reason": "ok", "exit": 0, "marker": "GAMMA_OK"}
            )
            + "\n",
            "stderr": "",
        },
        {
            "name": "pin_live",
            "argv": ["python3", "tools/pin-disposition.py", "--manifest", "fixture"],
            "exit": 0,
            "stdout": json.dumps(
                {
                    "counts": variant.get(
                        "pin_counts",
                        {"legs": 2, "changed": 1, "unchanged": 1, "unavailable": 0},
                    ),
                    "legs": variant.get(
                        "pin_legs",
                        [
                            {
                                "leg": "a",
                                "content_status": "changed",
                                "result_reuse": "not_established",
                            },
                            {
                                "leg": "b",
                                "content_status": "unchanged",
                                "result_reuse": "not_established",
                            },
                        ],
                    ),
                    "result_reuse": variant.get("pin_result_reuse", "not_established"),
                }
            )
            + "\n",
            "stderr": "",
        },
        {
            "name": "producer_before",
            "argv": ["python3", ".ufo/evidence/round-13/producer-before.py", "selftest"],
            "exit": variant.get("producer_before_exit", 1),
            "stdout": variant.get("producer_before_stdout", "  check something ok\n"),
            "stderr": "Traceback (most recent call last):\nFileNotFoundError\n",
        },
        {
            "name": "argv_marker",
            "argv": ["sh", "-c", "touch " + str(marker)],
            "exit": 0,
            "stdout": "",
            "stderr": "",
        },
    ]
    if variant.get("duplicate_alpha_check"):
        verification_checks.append(
            {
                "name": "alpha",
                "argv": ["python3", "-c", "print('ALPHA_OK')"],
                "exit": 0,
                "stdout": "ALPHA_OK\n",
                "stderr": "",
            }
        )
    if variant.get("drop_producer_before_check"):
        verification_checks = [
            check for check in verification_checks if check["name"] != "producer_before"
        ]
    verification = {
        "schema": "tameshi-round13-verification-v1",
        "checks": verification_checks,
    }
    verification_bytes = _json_bytes(verification)
    _write_bytes(evidence / "verification.json", verification_bytes)

    oracle_checks = [
        {
            "name": "producer_before_oracle",
            "argv": ["python3", "producer-oracle.py", "--source", "producer-before.py"],
            "exit": 1,
            "stdout": variant.get(
                "oracle_before_stdout",
                "  check summary preserves top-level exposed declaration kind FAIL\n",
            ),
            "stderr": "",
        },
        {
            "name": "producer_after_oracle",
            "argv": ["python3", "producer-oracle.py", "--source", "bash-witness-study.py"],
            "exit": 0,
            "stdout": variant.get(
                "oracle_after_stdout",
                "  check summary preserves top-level exposed declaration kind ok\n"
                "WITNESS_SELFTEST: 41/41 pass\n",
            ),
            "stderr": "",
        },
    ]
    oracle_checks.extend(variant.get("extra_oracle_checks", []))
    oracle = {
        "schema": "tameshi-round13-producer-oracle-repair-v1",
        "supersedes": variant.get(
            "oracle_supersedes",
            "verification.json producer_before: fixture crash is NOT red-before evidence",
        ),
        "oracle_sha256": oracle_input_digest,
        "checks": oracle_checks,
    }
    oracle_bytes = _json_bytes(oracle)
    _write_bytes(evidence / "producer-oracle-repair.json", oracle_bytes)

    return {
        "lane": lane,
        "expected_rel": ".ufo/evidence/round-13/expected.json",
        "ver_rel": ".ufo/evidence/round-13/verification.json",
        "oracle_rel": ".ufo/evidence/round-13/producer-oracle-repair.json",
        "fixture_rel": "fixtures/input.txt",
        "tool_rel": SELFTEST_TOOL_REL,
    }


def _effective(name, receipt_rel, check=None):
    return {
        "name": name,
        "state": "effective",
        "receipt": receipt_rel,
        "check": check or name,
    }


def _superseded(name, reason, replacements, raw_receipt, raw_check):
    return {
        "name": name,
        "state": "superseded",
        "reason": reason,
        "raw_receipt": raw_receipt,
        "raw_check": raw_check,
        "superseded_by": replacements,
    }


def _rows(fx, producer_state="superseded", **variant):
    ver = fx["ver_rel"]
    oracle = fx["oracle_rel"]
    rows = [
        _effective("alpha", ver),
        _effective("beta", ver),
        _effective("gamma", ver, variant.get("gamma_check", "gamma")),
        _effective("pin_live", ver),
    ]
    if producer_state == "effective":
        rows.append(_effective("producer_before", ver))
    else:
        rows.append(
            _superseded(
                "producer_before",
                variant.get(
                    "reason",
                    "raw path-layout crash before the kind assertion; exit1 records a setup failure",
                ),
                variant.get(
                    "replacements",
                    ["producer_before_oracle", "producer_after_oracle"],
                ),
                variant.get("raw_receipt", ver),
                variant.get("raw_check", "producer_before"),
            )
        )
    rows.extend(
        [
            _effective("producer_before_oracle", oracle),
            _effective("producer_after_oracle", oracle),
        ]
    )
    drop = set(variant.get("drop", ()))
    rows = [row for row in rows if row["name"] not in drop]
    rows.extend(variant.get("extra_rows", []))
    return rows


def _dispositions(fx, rows):
    lane = fx["lane"]
    inputs = {
        fx["expected_rel"]: _sha((lane / fx["expected_rel"]).read_bytes()),
        fx["ver_rel"]: _sha((lane / fx["ver_rel"]).read_bytes()),
        fx["oracle_rel"]: _sha((lane / fx["oracle_rel"]).read_bytes()),
    }
    return {
        "schema": "evidence-dispositions-v1",
        "expected_file": fx["expected_rel"],
        "inputs": inputs,
        "rows": rows,
    }


def _dispositions_v2(fx, rows, historical=None, supersedes_rel=None, pin_supersedes=True,
                     supersedes_doc=None):
    """v2 manifest: v1 fields plus `supersedes` and `historical_inputs`."""
    document = _dispositions(fx, rows)
    document["schema"] = SCHEMA_V2
    if supersedes_rel is not None:
        if supersedes_rel == SELFTEST_V1_REL:
            doc = supersedes_doc if supersedes_doc is not None else _dispositions(fx, rows)
            _write_bytes(fx["lane"] / SELFTEST_V1_REL, _json_bytes(doc))
        if pin_supersedes:
            document["inputs"][supersedes_rel] = _sha(
                (fx["lane"] / supersedes_rel).read_bytes()
            )
    document["supersedes"] = supersedes_rel
    document["historical_inputs"] = historical or {}
    return document


def _git(lane, *argv):
    proc = subprocess.run(
        ["git", "-C", str(lane)] + list(argv), capture_output=True, timeout=30
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "git {} failed: {}".format(argv[0], _stderr_text(proc))
        )
    return proc.stdout


def _git_raw(argv):
    proc = subprocess.run(argv, capture_output=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError("{} failed: {}".format(argv, _stderr_text(proc)))
    return proc.stdout


def _git_head(lane):
    return _git(lane, "rev-parse", "HEAD").decode("ascii").strip()


def _git_commit_all(lane, message):
    _git(lane, "add", "-A")
    _git(
        lane,
        "-c",
        "user.email=selftest@example.invalid",
        "-c",
        "user.name=selftest",
        "commit",
        "-qm",
        message,
    )
    return _git_head(lane)


def _git_init_commit(lane, message="fixture commit"):
    _git(lane, "init", "-q")
    return _git_commit_all(lane, message)


def _setup_hist_clean(fx):
    """Pinned bytes at rev A, then the instrument move committed at HEAD."""
    lane = fx["lane"]
    rev_a = _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    _git_commit_all(lane, "round-16 committed instrument move")
    fx["hist_rev"] = rev_a


def _setup_hist_other(fx):
    """Unexpected committed bytes at rev B (the declared historical rev)."""
    lane = fx["lane"]
    _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_OTHER)
    rev_b = _git_commit_all(lane, "unexpected committed bytes")
    fx["hist_rev"] = rev_b


def _setup_hist_unneeded(fx):
    """Live bytes still equal the pin: the waiver must be refused."""
    fx["hist_rev"] = _git_init_commit(fx["lane"], "round-13 pinned tools")


def _setup_hist_uncommitted(fx):
    """Worktree edit of a waived path, never committed."""
    lane = fx["lane"]
    rev_a = _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    fx["hist_rev"] = rev_a


def _setup_hist_missing_object(fx):
    """Rev D deleted the path; HEAD later restored it as a moved tool."""
    lane = fx["lane"]
    _git_init_commit(lane, "round-13 pinned tools")
    os.remove(lane / SELFTEST_TOOL_REL)
    rev_d = _git_commit_all(lane, "delete pinned tool")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    _git_commit_all(lane, "restore as a moved tool")
    fx["hist_rev"] = rev_d


def _setup_hist_dangling(fx):
    """A commit that exists but is not an ancestor of HEAD."""
    lane = fx["lane"]
    _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    _git_commit_all(lane, "committed instrument move")
    tree = _git(lane, "rev-parse", "HEAD^{tree}").decode().strip()
    dangling = _git(lane, "commit-tree", tree, "-m", "forged: not on master").decode().strip()
    fx["hist_rev"] = dangling


def _setup_hist_tree(fx):
    """A tree object id is not a commit."""
    lane = fx["lane"]
    _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    _git_commit_all(lane, "committed instrument move")
    fx["hist_rev"] = _git(lane, "rev-parse", "HEAD^{tree}").decode().strip()


def _setup_hist_replace(fx):
    """A replace ref rewrites HEAD; only GIT_NO_REPLACE_OBJECTS restores truth."""
    lane = fx["lane"]
    rev_a = _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    _git_commit_all(lane, "committed instrument move")
    fake_tree = _git(lane, "rev-parse", rev_a + "^{tree}").decode().strip()
    fake = _git(lane, "commit-tree", fake_tree, "-m", "replace fake").decode().strip()
    _git(lane, "replace", "HEAD", fake)
    fx["hist_rev"] = rev_a


def _setup_committed_deletion(fx):
    """Pinned bytes at rev A; HEAD holds a committed deletion of the path."""
    lane = fx["lane"]
    rev_a = _git_init_commit(lane, "round-13 pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_V2)
    _git_commit_all(lane, "committed instrument move")
    os.remove(lane / SELFTEST_TOOL_REL)
    _git_commit_all(lane, "committed deletion of the moved tool")
    fx["hist_rev"] = rev_a


def _setup_gitdir_env(fx):
    """A foreign GIT_DIR/GIT_WORK_TREE exported into the tool's environment."""
    _setup_hist_clean(fx)
    lane = fx["lane"]
    foreign = lane.parent / (lane.name + "-foreign")
    _write_bytes(foreign / "seed.txt", b"foreign\n")
    _git_init_commit(foreign, "foreign repo")
    fx["env_extra"] = {
        "GIT_DIR": str(foreign / ".git"),
        "GIT_WORK_TREE": str(lane),
    }


def _setup_shallow(fx):
    """A shallow clone: historical blobs are not provable."""
    lane = fx["lane"]
    src = lane.parent / (lane.name + "-src")
    os.rename(str(lane), str(src))
    rev = _git_init_commit(src, "shallow source")
    _git_raw(["git", "clone", "--depth", "1", "--quiet", "file://" + str(src), str(lane)])
    fx["hist_rev"] = rev


def _setup_crlf(fx):
    """Pinned CRLF bytes at rev A; HEAD holds different committed bytes."""
    lane = fx["lane"]
    rev_a = _git_init_commit(lane, "crlf pinned tools")
    _write_bytes(lane / SELFTEST_TOOL_REL, SELFTEST_TOOL_OTHER)
    _git_commit_all(lane, "committed instrument move")
    fx["hist_rev"] = rev_a


def _status_for(exit_code):
    return {0: "clean", 1: "failed", 2: "could_not_evaluate"}.get(exit_code)


def selftest():
    """Isolated /tmp fixtures; invokes this CLI via subprocess only."""
    scratch = Path(tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir="/tmp"))
    marker = scratch / "argv-marker"
    passed = 0
    failed = []

    def record(name, ok, detail):
        nonlocal passed
        if ok:
            passed += 1
            print("SELFTEST_CASE {} PASS ({})".format(name, detail))
        else:
            failed.append(name)
            print("SELFTEST_CASE {} FAIL ({})".format(name, detail))

    def run_cli(lane, dispositions_path, env_extra=None):
        env = None
        if env_extra:
            env = dict(os.environ)
            env.update(env_extra)
        return subprocess.run(
            [
                sys.executable,
                SELF,
                "--root",
                str(lane),
                "--dispositions",
                str(dispositions_path),
                "--json",
            ],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
            cwd=str(lane),
        )

    def case(name, expected_exit, expected_ids, variant=None, rows_kwargs=None,
             rows_override=None, raw_dispositions=None, mutate=None,
             informational_checks=None, git_setup=None):
        lane = scratch / ("case-" + name)
        try:
            fx = _build_lane(lane, marker, variant or {})
            if git_setup is not None:
                git_setup(fx)
            rows = rows_override if rows_override is not None else _rows(fx, **(rows_kwargs or {}))
            if raw_dispositions is not None:
                produced = raw_dispositions(fx)
                dispositions_bytes = (
                    produced if isinstance(produced, (bytes, bytearray)) else _json_bytes(produced)
                )
            else:
                dispositions_bytes = _json_bytes(_dispositions(fx, rows))
            dispositions_path = lane / ".ufo" / "evidence" / "round-13" / "dispositions.json"
            _write_bytes(dispositions_path, dispositions_bytes)
            if mutate is not None:
                mutate(fx)
            proc = run_cli(lane, dispositions_path, fx.get("env_extra"))
        except Exception as exc:  # fixture setup or process failure
            record(name, False, "setup/process error: {}: {}".format(type(exc).__name__, exc))
            return
        checks = [(proc.returncode == expected_exit, "exit={} expects={}".format(proc.returncode, expected_exit))]
        payload = None
        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            checks.append((False, "stdout is not JSON: {!r}".format(proc.stdout[:200])))
        if payload is not None:
            ids = sorted(finding["id"] for finding in payload.get("findings", []))
            checks.append((ids == sorted(expected_ids), "ids={!r} expects={!r}".format(ids, sorted(expected_ids))))
            checks.append((payload.get("exit") == expected_exit, "payload exit={!r}".format(payload.get("exit"))))
            checks.append(
                (
                    payload.get("status") == _status_for(expected_exit),
                    "status={!r} expects={!r}".format(payload.get("status"), _status_for(expected_exit)),
                )
            )
            if informational_checks is not None:
                observed = sorted(
                    item["check"] for item in payload.get("informational", {}).get("receipt_only_checks", [])
                )
                checks.append((observed == sorted(informational_checks), "informational={!r}".format(observed)))
        ok = all(flag for flag, _detail in checks)
        detail = "{} literal checks".format(len(checks)) if ok else "; ".join(
            detail for flag, detail in checks if not flag
        )
        record(name, ok, detail)

    ver = ".ufo/evidence/round-13/verification.json"
    oracle = ".ufo/evidence/round-13/producer-oracle-repair.json"

    case("clean-superseded", 0, [], informational_checks=["argv_marker"])
    case("unsuperseded-crash-mismatch", 1, ["expected_contains_missing"],
         rows_kwargs={"producer_state": "effective"})
    case("missing-row-drop", 1, ["row_missing"], rows_kwargs={"drop": ("beta",)})
    case(
        "unknown-row",
        1,
        ["row_unknown"],
        rows_kwargs={"extra_rows": [_effective("ghost", ver, "producer_before")]},
    )
    case(
        "duplicate-row-name",
        1,
        ["row_duplicate"],
        rows_kwargs={
            "extra_rows": [
                _superseded(
                    "producer_before",
                    "duplicate fixture",
                    ["producer_before_oracle", "producer_after_oracle"],
                    ver,
                    "producer_before",
                )
            ]
        },
    )
    case(
        "effective-check-identity",
        1,
        ["effective_check_name_mismatch"],
        variant={"expected_checks": {"gamma": {"exit": 0, "contains": "ALPHA_OK"}}},
        rows_kwargs={"gamma_check": "alpha"},
    )
    case(
        "receipt-check-ambiguous",
        2,
        ["receipt_check_ambiguous"],
        variant={
            "extra_oracle_checks": [
                {
                    "name": "alpha",
                    "argv": ["python3", "-c", "print('ALPHA_OK')"],
                    "exit": 0,
                    "stdout": "ALPHA_OK\n",
                    "stderr": "",
                }
            ]
        },
    )
    case(
        "invalid-replacement-self-cycle",
        1,
        ["superseded_cycle", "superseded_replacement_not_allowed", "superseded_target_not_effective"],
        rows_kwargs={
            "replacements": ["producer_before", "producer_before_oracle", "producer_after_oracle"]
        },
    )
    case(
        "required-replacement-missing",
        1,
        ["superseded_by_unknown", "superseded_replacement_not_allowed", "superseded_required_replacement_missing"],
        rows_kwargs={"replacements": ["producer_before_oracle", "ghost"]},
    )
    case(
        "replacement-failed",
        1,
        ["expected_contains_missing", "superseded_replacement_failed"],
        variant={"oracle_after_stdout": "  check summary preserves top-level exposed declaration kind ok\nWITNESS_SELFTEST: 40/41 pass\n"},
    )
    case(
        "superseded-unexplained-reason",
        1,
        ["superseded_reason_missing"],
        rows_kwargs={"reason": ""},
    )
    case(
        "superseded-raw-missing",
        1,
        ["superseded_raw_missing"],
        variant={"drop_producer_before_check": True},
    )
    case(
        "superseded-raw-binding",
        1,
        ["superseded_raw_binding_mismatch"],
        rows_kwargs={"raw_receipt": oracle},
    )
    case(
        "supersession-unwarranted",
        1,
        ["supersession_unwarranted"],
        variant={
            "producer_before_stdout": "  check summary preserves top-level exposed declaration kind FAIL\n"
        },
    )
    case(
        "supersession-not-permitted",
        1,
        ["supersession_not_permitted"],
        rows_kwargs={
            "drop": ("gamma",),
            "extra_rows": [
                _superseded(
                    "gamma",
                    "not an allowed supersession",
                    ["producer_before_oracle", "producer_after_oracle"],
                    ver,
                    "gamma",
                )
            ],
        },
    )
    case(
        "superseded-oracle-binding",
        1,
        ["superseded_oracle_binding_missing"],
        variant={"oracle_supersedes": "different evidence"},
    )
    case(
        "exit-only-false-positive",
        1,
        ["expected_contains_missing"],
        variant={"alpha_stdout": "SOMETHING_ELSE\n"},
    )
    case(
        "id-only-false-positive",
        1,
        ["expected_id_mismatch"],
        variant={"beta_id": "beta_other"},
    )
    case(
        "structured-mismatch",
        1,
        ["expected_result_reuse_mismatch", "expected_rows_mismatch", "expected_statuses_mismatch"],
        variant={
            "pin_counts": {"legs": 3, "changed": 2, "unchanged": 1, "unavailable": 0},
            "pin_legs": [
                {"leg": "a", "content_status": "changed", "result_reuse": "not_established"},
                {"leg": "b", "content_status": "changed", "result_reuse": "not_established"},
                {"leg": "c", "content_status": "unchanged", "result_reuse": "not_established"},
            ],
            "pin_result_reuse": "established",
        },
    )
    case(
        "effective-exit-mismatch",
        1,
        ["expected_exit_mismatch"],
        variant={"alpha_exit": 1},
    )
    case(
        "tamper-receipt",
        2,
        ["input_digest_mismatch"],
        mutate=lambda fx: (fx["lane"] / fx["ver_rel"]).write_bytes(
            (fx["lane"] / fx["ver_rel"]).read_bytes() + b"\n"
        ),
    )
    case(
        "expected-input-digest-mismatch",
        2,
        ["expected_input_digest_mismatch"],
        mutate=lambda fx: (fx["lane"] / fx["fixture_rel"]).write_bytes(b"changed\n"),
    )
    case(
        "missing-expected-file",
        2,
        ["expected_file_missing"],
        mutate=lambda fx: (fx["lane"] / fx["expected_rel"]).unlink(),
    )
    case(
        "missing-receipt-file",
        2,
        ["input_missing"],
        mutate=lambda fx: (fx["lane"] / fx["ver_rel"]).unlink(),
    )
    case(
        "unpinned-receipt",
        2,
        ["input_unpinned"],
        rows_override=None,
        raw_dispositions=lambda fx: {
            "schema": "evidence-dispositions-v1",
            "expected_file": fx["expected_rel"],
            "inputs": {
                fx["expected_rel"]: _sha((fx["lane"] / fx["expected_rel"]).read_bytes()),
                fx["oracle_rel"]: _sha((fx["lane"] / fx["oracle_rel"]).read_bytes()),
            },
            "rows": _rows(fx),
        },
    )
    case(
        "receipt-bool-exit",
        2,
        ["receipt_check_invalid"],
        variant={"alpha_exit": True},
    )
    case(
        "expected-bool-exit",
        2,
        ["expectation_invalid"],
        variant={"expected_checks": {"alpha": {"exit": True, "contains": "ALPHA_OK"}}},
    )
    case(
        "duplicate-receipt-check",
        2,
        ["receipt_check_duplicate"],
        variant={"duplicate_alpha_check": True},
    )
    case(
        "malformed-json",
        2,
        ["dispositions_json_invalid"],
        raw_dispositions=lambda fx: b'{"schema":',
    )
    case(
        "duplicate-json-key",
        2,
        ["dispositions_json_invalid"],
        raw_dispositions=lambda fx: (
            '{"schema":"evidence-dispositions-v1",'
            '"schema":"evidence-dispositions-v1",'
            '"expected_file":"' + fx["expected_rel"] + '",'
            '"inputs":{},"rows":[]}'
        ).encode("utf-8"),
    )
    case(
        "path-escape-receipt",
        2,
        ["path_rejected"],
        rows_kwargs={"extra_rows": [_effective("ghost", "../verification.json", "ghost")]},
        rows_override=None,
    )

    # v2 (evidence-dispositions-v2) cases.
    hist_reason = "round-13 pinned instrument moved; read committed bytes"

    def _hist(fx, entries):
        built = {}
        for path, spec in entries.items():
            built[path] = {
                "rev": fx["hist_rev"] if spec["rev"] is None else spec["rev"],
                "reason": spec["reason"],
            }
        return built

    case(
        "v2-clean-historical",
        0,
        [],
        git_setup=_setup_hist_clean,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
        informational_checks=["argv_marker"],
    )
    case(
        "v2-historical-digest-mismatch",
        2,
        ["expected_input_digest_mismatch"],
        git_setup=_setup_hist_other,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-unknown",
        2,
        ["historical_input_unknown"],
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical={
                "tools/unknown.py": {
                    "rev": "0" * 40,
                    "reason": hist_reason,
                }
            },
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-forbidden",
        2,
        ["historical_input_forbidden"],
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical={
                "fixtures/input.txt": {
                    "rev": "0" * 40,
                    "reason": hist_reason,
                }
            },
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-unavailable-rev",
        2,
        ["historical_input_unavailable"],
        git_setup=_setup_hist_clean,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical={
                SELFTEST_TOOL_REL: {"rev": "f" * 40, "reason": hist_reason}
            },
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-unavailable-object",
        2,
        ["historical_input_unavailable"],
        git_setup=_setup_hist_missing_object,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-unneeded",
        2,
        ["historical_input_unneeded"],
        git_setup=_setup_hist_unneeded,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-uncommitted",
        2,
        ["historical_input_uncommitted"],
        git_setup=_setup_hist_uncommitted,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-dangling",
        2,
        ["historical_input_unavailable"],
        git_setup=_setup_hist_dangling,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-tree-id",
        2,
        ["historical_input_unavailable"],
        git_setup=_setup_hist_tree,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-historical-replace-ref",
        0,
        [],
        git_setup=_setup_hist_replace,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
        informational_checks=["argv_marker"],
    )
    case(
        "v2-gitdir-env",
        0,
        [],
        git_setup=_setup_gitdir_env,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
        informational_checks=["argv_marker"],
    )
    case(
        "v2-shallow-repo",
        2,
        ["historical_input_unavailable"],
        git_setup=_setup_shallow,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-blob-bytes-crlf",
        0,
        [],
        variant={"tool_bytes": SELFTEST_TOOL_CRLF},
        git_setup=_setup_crlf,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
        informational_checks=["argv_marker"],
    )
    case(
        "v2-committed-deletion",
        0,
        [],
        git_setup=_setup_committed_deletion,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
        informational_checks=["argv_marker"],
    )
    case(
        "v2-supersedes-rows-mismatch",
        2,
        ["supersedes_mismatch"],
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            supersedes_rel=SELFTEST_V1_REL,
            supersedes_doc=_dispositions(fx, _rows(fx, drop=("alpha",))),
        ),
    )
    case(
        "v1-extra-keys-tolerated",
        0,
        [],
        raw_dispositions=lambda fx: dict(
            _dispositions(fx, _rows(fx)),
            supersedes="docs/ignored.json",
            historical_inputs={},
        ),
        informational_checks=["argv_marker"],
    )
    case(
        "v2-live-mismatch-nonhistorical-tool",
        2,
        ["expected_input_digest_mismatch"],
        git_setup=_setup_hist_clean,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical={},
            supersedes_rel=SELFTEST_V1_REL,
        ),
    )
    case(
        "v2-live-mismatch-nonhistorical-fixture",
        2,
        ["expected_input_digest_mismatch"],
        git_setup=_setup_hist_clean,
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            historical=_hist(
                fx, {SELFTEST_TOOL_REL: {"rev": None, "reason": hist_reason}}
            ),
            supersedes_rel=SELFTEST_V1_REL,
        ),
        mutate=lambda fx: (fx["lane"] / fx["fixture_rel"]).write_bytes(b"changed\n"),
    )
    case(
        "v2-supersedes-unpinned",
        2,
        ["input_unpinned"],
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            supersedes_rel=SELFTEST_V1_REL,
            pin_supersedes=False,
        ),
    )
    case(
        "v2-supersedes-missing",
        2,
        ["dispositions_field_invalid"],
        raw_dispositions=lambda fx: _dispositions_v2(
            fx,
            _rows(fx),
            supersedes_rel=None,
        ),
    )

    # v2 identity guard: --root inside a foreign super-repo without its own
    # .git must report historical_input_unavailable before any blob read.
    lane_outer = scratch / "case-v2-identity-outer"
    lane_nested = lane_outer / "nested" / "root"
    try:
        fx_nested = _build_lane(lane_nested, marker, {})
        nested_rows = _rows(fx_nested)
        nested_manifest = _dispositions_v2(
            fx_nested,
            nested_rows,
            historical={
                SELFTEST_TOOL_REL: {"rev": "0" * 40, "reason": hist_reason}
            },
            supersedes_rel=SELFTEST_V1_REL,
        )
        nested_dispositions = (
            lane_nested / ".ufo" / "evidence" / "round-13" / "dispositions.json"
        )
        _write_bytes(nested_dispositions, _json_bytes(nested_manifest))
        _git_init_commit(lane_outer, "foreign super-repo")
        proc_nested = run_cli(lane_nested, nested_dispositions)
        ids_nested = []
        try:
            ids_nested = sorted(
                finding["id"] for finding in json.loads(proc_nested.stdout)["findings"]
            )
        except ValueError:
            pass
        record(
            "v2-identity-guard",
            proc_nested.returncode == 2 and ids_nested == ["historical_input_unavailable"],
            "exit={} ids={!r}".format(proc_nested.returncode, ids_nested),
        )
    except Exception as exc:
        record(
            "v2-identity-guard",
            False,
            "setup/process error: {}: {}".format(type(exc).__name__, exc),
        )

    # Usage errors: exit 64 with no JSON contract.
    for usage_name, argv in (
        ("usage-no-arguments", [sys.executable, SELF]),
        ("usage-selftest-extra", [sys.executable, SELF, "--selftest", "--json"]),
    ):
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=60, cwd=str(scratch))
            record(usage_name, proc.returncode == 64, "exit={} expects=64".format(proc.returncode))
        except Exception as exc:
            record(usage_name, False, "process error: {}: {}".format(type(exc).__name__, exc))

    record(
        "argv-never-executed",
        not marker.exists(),
        "marker absent={}".format(not marker.exists()),
    )

    total = passed + len(failed)
    if failed:
        print(
            "SELFTEST: FAIL ({}/{} failed: {}; fixtures kept at {})".format(
                len(failed), total, ", ".join(failed), scratch
            )
        )
        return 1
    import shutil

    shutil.rmtree(scratch, ignore_errors=True)
    print("SELFTEST: PASS ({}/{})".format(passed, total))
    return 0


# ----------------------------------------------------------------------- main


def parse_argv(argv):
    root = None
    dispositions = None
    as_json = False
    selftest_flag = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--json":
            if as_json:
                raise UsageError("--json given twice")
            as_json = True
            index += 1
        elif arg == "--selftest":
            if selftest_flag:
                raise UsageError("--selftest given twice")
            selftest_flag = True
            index += 1
        elif arg in ("--root", "--dispositions"):
            if index + 1 >= len(argv):
                raise UsageError(arg + " needs a value")
            key, value = arg, argv[index + 1]
            index += 2
            if not value:
                raise UsageError(arg + " has an empty value")
            if key == "--root":
                if root is not None:
                    raise UsageError("--root given twice")
                root = value
            else:
                if dispositions is not None:
                    raise UsageError("--dispositions given twice")
                dispositions = value
        elif arg.startswith("--root=") or arg.startswith("--dispositions="):
            key, value = arg.split("=", 1)
            index += 1
            if not value:
                raise UsageError(key + " has an empty value")
            if key == "--root":
                if root is not None:
                    raise UsageError("--root given twice")
                root = value
            else:
                if dispositions is not None:
                    raise UsageError("--dispositions given twice")
                dispositions = value
        else:
            raise UsageError("unknown argument: " + arg)
    if selftest_flag:
        if len(argv) != 1:
            raise UsageError("--selftest takes no other arguments")
        return {"selftest": True, "json": as_json}
    if root is None:
        raise UsageError("--root is required")
    if dispositions is None:
        raise UsageError("--dispositions is required")
    return {
        "selftest": False,
        "json": as_json,
        "root": root,
        "dispositions": dispositions,
    }


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        sys.stderr.write(USAGE)
        return 64
    if argv in (["--help"], ["-h"]):
        sys.stdout.write(USAGE)
        return 0
    try:
        options = parse_argv(argv)
    except UsageError as exc:
        sys.stderr.write("evidence-disposition.py: {}\n".format(exc))
        sys.stderr.write(USAGE)
        return 64
    if options["selftest"]:
        return selftest()
    try:
        return run_mode(options["root"], options["dispositions"], options["json"])
    except CouldNotEvaluate as exc:
        return emit_could_not_evaluate(exc, options["json"])
    except Exception as exc:  # fail closed, never exit 1 on an internal error
        return emit_could_not_evaluate(
            CouldNotEvaluate("internal_error", "{}: {}".format(type(exc).__name__, exc)),
            options["json"],
        )


if __name__ == "__main__":
    raise SystemExit(main())
