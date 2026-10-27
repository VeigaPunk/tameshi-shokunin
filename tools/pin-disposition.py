#!/usr/bin/env python3
"""pin-disposition.py — read-only pin/content disposition probe (tameshi-shokunin, round 13).

Question answered: for each of the six recorded mutation-ledger legs, does the
current worktree content still equal the full sha256 pin recorded by
tools/mutate-and-run.sh, and what does the repo's branch tip carry?

What this tool does NOT answer: whether a recorded mutation result may be
reused. Every row carries result_reuse=not_established. Byte identity of the
target does not establish identity of the environment, dependencies, fixtures,
suite command, or runner context; a matching pin is an observation, not a
verdict transfer.

Leg definitions are the six recorded legs only (no seventh case):
  tools/mutate-and-run.sh:84-89    leg / fleet-relative path table
  tools/mutate-and-run.sh:542-553  PIN_*/REV_* pairs
  tools/mutate-and-run.sh:1112-1140 ledger calls (repo = first path segment,
                                    path = the rest; `git show <rev>:<path>`)
The manifest repeats those repo/path/commit/sha256 values; the tool rejects a
manifest whose repo or path disagrees with the embedded recorded table, whose
pinned_commit is not full 40-hex, whose expected_sha256 is not full 64-hex, or
which repeats/omits/renames a leg. The committed manifest is the configured pin
authority for this probe, not an adversarial baseline-authentication gate: a
changed manifest changes the baseline it compares against, and that is still
not evidence that a recorded result may be reused. Round integration
cross-checks the delivered manifest against the unchanged
tools/mutate-and-run.sh and records the runner sha256 at the measured commit.

Manifest schema `pin-manifest-v1`:
  {"schema": "pin-manifest-v1",
   "legs": [{"leg": <one of the six>, "repo": <recorded>, "path": <recorded>,
             "pinned_commit": <40 lowercase hex>, "expected_sha256": <64 lowercase hex>}, ...]}

CLI:
  pin-disposition.py --manifest PATH --root FLEET   emit one JSON document
  pin-disposition.py --selftest                     isolated /tmp git fixtures

Per leg the JSON carries:
  pinned    original recorded evidence: commit, expected sha256, the sha256
            actually observed at that commit (blob_sha256), status
            verified|mismatch|unavailable, reason
  head      the lane branch resolved the way scripts/hyaku/jj-lane.sh
            detect_branch does (:53-65): an attached HEAD wins; a detached
            HEAD (jj colocated working copy) falls back to
            refs/remotes/origin/HEAD's branch, then refs/heads/master, then
            refs/heads/main, then the first local branch. `commit` is that
            branch's tip, `blob_sha256` the path's blob at the tip
            (present|absent|not_blob|unavailable), `head_differs_from_branch`
            whether raw HEAD commit != tip, `branch` the resolved name
            (null when no local branch exists; then commit stays raw HEAD
            and head_differs_from_branch is null).
  worktree  absolute path, current working-tree sha256, status
            unchanged|changed|unavailable (content_status mirrors it), reason
  content_status  unchanged | changed | unavailable (raw bytes only)
  result_reuse    literal "not_established" on every row

The document also carries `observed_at` (UTC, stamped after the rows are read,
so it marks the end of the read window) and `not_compared`, a static list of
inputs this probe
deliberately does not measure: mode/exec-bit, runner/defect-spec version, suite
command and harness, interpreter/toolchain, environment, dependencies, fixture
and companion files, timeouts. `content_status` is a raw-byte comparison only;
a chmod-only change with identical bytes stays `unchanged` while still carrying
result_reuse=not_established. The historical executable-bit counterexample
(round 10) is why mode stays visible in `not_compared` rather than inferred.

Content status semantics: `unchanged` requires a readable regular worktree file,
verified pinned evidence (the manifest digest equals the blob at the recorded
commit), and byte equality with expected_sha256. A missing repo, path, commit or
blob, a pin/digest disagreement, a symlink or a non-regular file can never be
`unchanged`; those classify as `unavailable` with a reason. A readable file
whose bytes differ from a verified pin is `changed`. The branch tip may
differ from the pinned commit while the content is still `unchanged`; the
branch tip is reported separately and never substituted for the worktree
observation.

Exit map: 0 observations emitted, including drift and unavailable legs (this is
a probe, not a gate) · 2 could-not-evaluate invalid input (usage, missing/
unreadable/schema-invalid manifest, fleet root not a directory), still emitted
as a JSON error document on stdout.

Read-only guarantees: the tool never writes to a target repo or worktree. Git is
used only through read-only plumbing (`rev-parse`, `symbolic-ref`,
`show-ref`, `for-each-ref`, `cat-file`), never `status`, `diff` or
`hash-object`; the index, filters and hooks are never invoked. Inherited
GIT_* variables are scrubbed, optional locks are disabled, global and
system git config are bypassed, argv lists are used (no shell), and each git
call is bounded by a timeout. A repo must prove its own identity
(`git rev-parse --show-toplevel` equal to the leg repo's real path) so a
missing sibling cannot silently borrow the fleet root's super-repo HEAD.
The worktree file must be a regular file (lstat + O_NOFOLLOW) whose real path stays
inside the leg repo, so a symlink cannot leak an arbitrary file's digest.

Dependencies: python3 (stdlib only), git.
"""

import copy
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

VERSION = "pin-disposition.py r17 (tameshi-shokunin, 2026-10-20)"
SELF = os.path.realpath(__file__)

SCHEMA = "pin-disposition-v1"
MANIFEST_SCHEMA = "pin-manifest-v1"
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
DIGEST_RE = re.compile(r"[0-9a-f]{64}")
GIT_TIMEOUT = 30.0

RESULT_REUSE = "not_established"
RESULT_REUSE_REASON = (
    "identical target content does not establish environment, dependency, "
    "fixture or suite-command identity"
)
# Inputs deliberately outside this probe's raw-byte disposition. A mode change
# with identical bytes stays content_status=unchanged; it is simply unmeasured.
NOT_COMPARED = (
    "mode/exec-bit",
    "runner version and embedded defect specs",
    "suite command and test harness",
    "interpreter and toolchain versions",
    "environment variables",
    "dependency versions",
    "fixture and companion files",
    "timeouts",
)

# Recorded ledger legs, in tools/mutate-and-run.sh order (:84-89, :1112-1140).
# repo = first segment of the fleet-relative path; path = the rest.
CANONICAL_LEGS = (
    ("js-kimi-census", "kumitate-shokunin", "scripts/kimi-census.mjs"),
    ("bash-surface-census", "kagi-shokunin", "corpus/surface-census.sh"),
    ("bash-tsukuroi-census", "tsukuroi-shokunin", "tools/tsukuroi-census.sh"),
    ("bash-mado-verify", "mado-shokunin", "tools/mado-verify.sh"),
    ("bash-checklist-run", "kagi-shokunin", "corpus/checklist-run.sh"),
    ("js-claims-check", "kumitate-shokunin", "scripts/claims-check.mjs"),
)
CANONICAL_BY_LEG = {leg: (repo, path) for leg, repo, path in CANONICAL_LEGS}

USAGE = """usage: pin-disposition.py --manifest PATH --root FLEET
       pin-disposition.py --selftest

Read-only pin/content disposition probe for the six recorded mutation-ledger
legs. Emits one JSON document on stdout. Every row carries
result_reuse=not_established: a matching content pin does not establish that a
recorded result may be reused.

exit 0  observations emitted (drift and unavailable legs included)
exit 2  could-not-evaluate invalid input (usage, manifest, fleet root)
"""


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


class InvalidInput(Exception):
    """Input that prevents any leg from being evaluated."""

    def __init__(self, kind, message):
        super().__init__(message)
        self.kind = kind


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def tool_sha256():
    try:
        with open(SELF, "rb") as handle:
            return sha256_bytes(handle.read())
    except OSError:
        return None


def emit_json(payload):
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")


def base_payload(status):
    return {
        "schema": SCHEMA,
        "tool": VERSION,
        "tool_sha256": tool_sha256(),
        "status": status,
    }


def invalid_input(kind, message):
    payload = base_payload("invalid_input")
    payload["error"] = {"kind": kind, "message": message}
    payload["result_reuse"] = RESULT_REUSE
    payload["result_reuse_reason"] = RESULT_REUSE_REASON
    payload["legs"] = []
    emit_json(payload)
    return 2


# ------------------------------------------------------------------ git facts


def git_env():
    """Inherited GIT_* is scrubbed; config, locks and prompts are disabled."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
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


def git_run(repo_abs, args):
    """Run one read-only git command. Returns (CompletedProcess, reason)."""
    try:
        proc = subprocess.run(
            ["git", "-C", repo_abs] + args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=git_env(),
            timeout=GIT_TIMEOUT,
            check=False,
        )
    except FileNotFoundError:
        return None, "git_unavailable"
    except subprocess.TimeoutExpired:
        return None, "git_timeout"
    except OSError:
        return None, "git_unavailable"
    return proc, None


def repo_identity(root_real, repo):
    """Return (repo_real, None) only when <root>/<repo> is its own repository.

    The fleet root is itself a git repo, so a directory without .git would make
    `git -C` discover the super-repo. The toplevel equality check refuses that.
    """
    repo_abs = os.path.join(root_real, repo)
    try:
        entry = os.lstat(repo_abs)
    except FileNotFoundError:
        return None, "repo_missing"
    except OSError:
        return None, "repo_unreadable"
    if stat.S_ISLNK(entry.st_mode):
        return None, "repo_symlink"
    if not stat.S_ISDIR(entry.st_mode):
        return None, "repo_not_directory"
    repo_real = os.path.realpath(repo_abs)
    if os.path.dirname(repo_real) != root_real or os.path.basename(repo_real) != repo:
        return None, "repo_outside_root"
    proc, reason = git_run(repo_real, ["rev-parse", "--show-toplevel"])
    if reason:
        return None, reason
    if proc.returncode != 0:
        return None, "repo_not_git"
    top = proc.stdout.decode("utf-8", "replace").strip()
    if not top:
        return None, "repo_not_git"
    if os.path.realpath(top) != repo_real:
        return None, "repo_foreign"
    return repo_real, None


def pinned_observation(repo_real, commit, path, expected):
    """Read the recorded commit/path/blob and compare the blob to the manifest."""
    result = {
        "commit": commit,
        "expected_sha256": expected,
        "blob_sha256": None,
        "status": "unavailable",
        "reason": None,
    }
    reason = None
    proc, run_reason = git_run(
        repo_real,
        ["rev-parse", "--verify", "--quiet", "--end-of-options", commit + "^{commit}"],
    )
    if run_reason:
        reason = run_reason
    elif proc.returncode != 0:
        reason = "pinned_commit_missing"
    else:
        obj = commit + ":" + path
        proc, run_reason = git_run(repo_real, ["cat-file", "-t", obj])
        if run_reason:
            reason = run_reason
        elif proc.returncode != 0:
            reason = "pinned_path_missing"
        elif proc.stdout.decode("utf-8", "replace").strip() != "blob":
            reason = "pinned_object_not_blob"
        else:
            proc, run_reason = git_run(repo_real, ["cat-file", "blob", obj])
            if run_reason:
                reason = run_reason
            elif proc.returncode != 0:
                reason = "pinned_read_failed"
            else:
                digest = sha256_bytes(proc.stdout)
                result["blob_sha256"] = digest
                if digest == expected:
                    result["status"] = "verified"
                else:
                    result["status"] = "mismatch"
                    reason = "pinned_blob_mismatch"
    if result["status"] != "verified":
        result["reason"] = reason or "pinned_unavailable"
    return result


def detect_branch(repo_real):
    """Mirror scripts/hyaku/jj-lane.sh detect_branch (:53-65), read-only.

    Attached HEAD yields its short name. A detached HEAD (the jj colocated
    working-copy state this fleet lives in) falls back to the branch
    refs/remotes/origin/HEAD points at, then refs/heads/master, then
    refs/heads/main, then the first local branch. Returns (branch, reason):
    branch is the short name or None; reason is a git_run failure string or
    None (unresolvable-without-error also returns (None, None)).
    """
    proc, reason = git_run(repo_real, ["symbolic-ref", "-q", "--short", "HEAD"])
    if reason:
        return None, reason
    if proc.returncode == 0:
        branch = proc.stdout.decode("utf-8", "replace").strip()
        if branch:
            return branch, None
    proc, reason = git_run(
        repo_real, ["symbolic-ref", "-q", "refs/remotes/origin/HEAD"]
    )
    if reason:
        return None, reason
    if proc.returncode == 0:
        ref = proc.stdout.decode("utf-8", "replace").strip()
        prefix = "refs/remotes/origin/"
        if ref.startswith(prefix) and ref[len(prefix):]:
            return ref[len(prefix):], None
    for candidate in ("master", "main"):
        proc, reason = git_run(
            repo_real,
            ["show-ref", "-q", "--verify", "refs/heads/" + candidate],
        )
        if reason:
            return None, reason
        if proc.returncode == 0:
            return candidate, None
    proc, reason = git_run(
        repo_real,
        ["for-each-ref", "--format=%(refname:short)", "refs/heads/"],
    )
    if reason:
        return None, reason
    if proc.returncode == 0:
        for line in proc.stdout.decode("utf-8", "replace").splitlines():
            branch = line.strip()
            if branch:
                return branch, None
    return None, None


def head_observation(repo_real, path):
    """Resolve the lane branch tip and the sha256 of <path>'s blob at it.

    `commit` is the resolved branch tip, not raw HEAD: a jj colocated repo
    leaves HEAD detached on the working-copy commit, which can sit ahead of
    the branch. `head_differs_from_branch` records that divergence. When no
    local branch exists at all, `commit` falls back to raw HEAD and the two
    new fields stay null so the probe degrades instead of failing.
    """
    result = {
        "branch": None,
        "commit": None,
        "blob_sha256": None,
        "status": "unavailable",
        "reason": None,
        "head_differs_from_branch": None,
    }
    proc, reason = git_run(
        repo_real, ["rev-parse", "--verify", "--quiet", "--end-of-options", "HEAD^{commit}"]
    )
    if reason:
        result["reason"] = reason
        return result
    head_commit = proc.stdout.decode("utf-8", "replace").strip()
    if proc.returncode != 0 or not head_commit:
        result["reason"] = "head_missing"
        return result
    branch, reason = detect_branch(repo_real)
    if reason:
        result["reason"] = reason
        return result
    commit = head_commit
    if branch is not None:
        result["branch"] = branch
        proc, run_reason = git_run(
            repo_real,
            [
                "rev-parse",
                "--verify",
                "--quiet",
                "--end-of-options",
                "refs/heads/" + branch + "^{commit}",
            ],
        )
        if run_reason:
            result["reason"] = run_reason
            return result
        tip = proc.stdout.decode("utf-8", "replace").strip()
        if proc.returncode != 0 or not tip:
            result["reason"] = "branch_tip_missing"
            return result
        commit = tip
        result["head_differs_from_branch"] = head_commit != tip
    result["commit"] = commit
    obj = commit + ":" + path
    proc, run_reason = git_run(repo_real, ["cat-file", "-t", obj])
    if run_reason:
        result["reason"] = run_reason
        return result
    if proc.returncode != 0:
        result["status"] = "absent"
        result["reason"] = "head_path_absent"
        return result
    if proc.stdout.decode("utf-8", "replace").strip() != "blob":
        result["status"] = "not_blob"
        result["reason"] = "head_object_not_blob"
        return result
    proc, run_reason = git_run(repo_real, ["cat-file", "blob", obj])
    if run_reason:
        result["reason"] = run_reason
        return result
    if proc.returncode != 0:
        result["reason"] = "head_read_failed"
        return result
    result["blob_sha256"] = sha256_bytes(proc.stdout)
    result["status"] = "present"
    return result


def worktree_observation(repo_real, path):
    """Hash the regular worktree file; never follow a symlink or leave the repo."""
    abs_path = os.path.join(repo_real, *path.split("/"))
    result = {"path": abs_path, "sha256": None, "status": "unavailable", "reason": None}
    try:
        entry = os.lstat(abs_path)
    except FileNotFoundError:
        result["reason"] = "worktree_missing"
        return result
    except OSError:
        result["reason"] = "worktree_unreadable"
        return result
    if stat.S_ISLNK(entry.st_mode):
        result["reason"] = "worktree_symlink"
        return result
    if not stat.S_ISREG(entry.st_mode):
        result["reason"] = "worktree_not_regular"
        return result
    if not os.path.realpath(abs_path).startswith(repo_real + os.sep):
        result["reason"] = "worktree_outside_repo"
        return result
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(abs_path, flags)
    except FileNotFoundError:
        result["reason"] = "worktree_missing"
        return result
    except OSError:
        result["reason"] = "worktree_unreadable"
        return result
    hasher = hashlib.sha256()
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or (
            opened.st_dev,
            opened.st_ino,
        ) != (entry.st_dev, entry.st_ino):
            result["reason"] = "worktree_replaced"
            return result
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            hasher.update(chunk)
    except OSError:
        result["reason"] = "worktree_unreadable"
        return result
    finally:
        os.close(fd)
    result["sha256"] = hasher.hexdigest()
    return result


def evaluate_leg(root_real, entry):
    """Build one row. content_status is the only disposition this tool claims."""
    leg = entry["leg"]
    repo, path = CANONICAL_BY_LEG[leg]
    expected = entry["expected_sha256"]
    row = {"leg": leg, "repo": repo, "path": path}
    repo_real, repo_reason = repo_identity(root_real, repo)
    if repo_reason:
        row["pinned"] = {
            "commit": entry["pinned_commit"],
            "expected_sha256": expected,
            "blob_sha256": None,
            "status": "unavailable",
            "reason": repo_reason,
        }
        row["head"] = {
            "branch": None,
            "commit": None,
            "blob_sha256": None,
            "status": "unavailable",
            "reason": repo_reason,
            "head_differs_from_branch": None,
        }
        row["worktree"] = {
            "path": os.path.join(root_real, repo, *path.split("/")),
            "sha256": None,
            "status": "unavailable",
            "reason": repo_reason,
        }
        row["content_status"] = "unavailable"
        row["result_reuse"] = RESULT_REUSE
        return row

    pinned = pinned_observation(repo_real, entry["pinned_commit"], path, expected)
    head = head_observation(repo_real, path)
    worktree = worktree_observation(repo_real, path)
    if worktree["sha256"] is None:
        content_status = "unavailable"
    elif pinned["status"] != "verified":
        # A readable file cannot be called unchanged against unverified evidence.
        content_status = "unavailable"
        worktree["status"] = "unavailable"
        worktree["reason"] = "pin_not_verified"
    elif worktree["sha256"] == expected:
        content_status = "unchanged"
        worktree["status"] = "unchanged"
    else:
        content_status = "changed"
        worktree["status"] = "changed"
    row["pinned"] = pinned
    row["head"] = head
    row["worktree"] = worktree
    row["content_status"] = content_status
    row["result_reuse"] = RESULT_REUSE
    return row


# ------------------------------------------------------------------- manifest


def reject_duplicate_keys(pairs):
    record = {}
    for key, value in pairs:
        if key in record:
            raise InvalidInput("invalid_manifest", "manifest repeats JSON key {!r}".format(key))
        record[key] = value
    return record


def read_manifest(path):
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except FileNotFoundError:
        raise InvalidInput("invalid_manifest", "manifest not found: " + path)
    except OSError as exc:
        raise InvalidInput(
            "invalid_manifest", "manifest unreadable: " + (exc.strerror or "I/O error")
        )
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidInput("invalid_manifest", "manifest is not UTF-8")
    try:
        record = json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise InvalidInput(
            "invalid_manifest",
            "manifest is not valid JSON: line {} column {}".format(exc.lineno, exc.colno),
        )
    if not isinstance(record, dict):
        raise InvalidInput("invalid_manifest", "manifest root is not a JSON object")
    if record.get("schema") != MANIFEST_SCHEMA:
        raise InvalidInput(
            "invalid_manifest", "manifest schema is not " + MANIFEST_SCHEMA
        )
    legs = record.get("legs")
    if not isinstance(legs, list):
        raise InvalidInput("invalid_manifest", "manifest legs is not a JSON array")

    seen = {}
    for index, entry in enumerate(legs, 1):
        if not isinstance(entry, dict):
            raise InvalidInput(
                "invalid_manifest", "leg entry {} is not a JSON object".format(index)
            )
        for key in ("leg", "repo", "path", "pinned_commit", "expected_sha256"):
            value = entry.get(key)
            if not isinstance(value, str) or not value:
                raise InvalidInput(
                    "invalid_manifest",
                    "leg entry {} has no non-empty string {}".format(index, key),
                )
        leg = entry["leg"]
        if leg not in CANONICAL_BY_LEG:
            raise InvalidInput(
                "invalid_manifest",
                "leg entry {} names unknown leg {!r} (six recorded legs only)".format(index, leg),
            )
        if leg in seen:
            raise InvalidInput(
                "invalid_manifest", "duplicate leg {!r} in manifest".format(leg)
            )
        canon_repo, canon_path = CANONICAL_BY_LEG[leg]
        if entry["repo"] != canon_repo:
            raise InvalidInput(
                "invalid_manifest",
                "leg {} repo {!r} does not match the recorded repo {!r}".format(
                    leg, entry["repo"], canon_repo
                ),
            )
        if entry["path"] != canon_path:
            raise InvalidInput(
                "invalid_manifest",
                "leg {} path {!r} does not match the recorded path {!r}".format(
                    leg, entry["path"], canon_path
                ),
            )
        if not COMMIT_RE.fullmatch(entry["pinned_commit"]):
            raise InvalidInput(
                "invalid_manifest",
                "leg {} pinned_commit is not a full 40-hex git commit id".format(leg),
            )
        if not DIGEST_RE.fullmatch(entry["expected_sha256"]):
            raise InvalidInput(
                "invalid_manifest",
                "leg {} expected_sha256 is not a full 64-hex sha256 digest".format(leg),
            )
        seen[leg] = entry

    missing = [leg for leg, _, _ in CANONICAL_LEGS if leg not in seen]
    if missing:
        raise InvalidInput(
            "invalid_manifest", "manifest omits recorded leg(s): " + ", ".join(missing)
        )
    return [seen[leg] for leg, _, _ in CANONICAL_LEGS]


# ----------------------------------------------------------------- run mode


def run_mode(manifest_path, root_path):
    entries = read_manifest(manifest_path)
    root_abs = os.path.abspath(root_path)
    if not os.path.isdir(root_abs):
        raise InvalidInput(
            "invalid_root", "fleet root is not an existing directory: " + root_abs
        )
    root_real = os.path.realpath(root_abs)
    rows = [evaluate_leg(root_real, entry) for entry in entries]
    counts = {"legs": len(rows), "unchanged": 0, "changed": 0, "unavailable": 0}
    for row in rows:
        counts[row["content_status"]] += 1
    payload = base_payload("ok")
    payload["observed_at"] = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    payload["manifest"] = os.path.abspath(manifest_path)
    payload["root"] = root_real
    payload["result_reuse"] = RESULT_REUSE
    payload["result_reuse_reason"] = RESULT_REUSE_REASON
    payload["not_compared"] = list(NOT_COMPARED)
    payload["counts"] = counts
    payload["legs"] = rows
    emit_json(payload)
    return 0


# ------------------------------------------------------------------- selftest

SELFTEST_V1 = b"#!/bin/sh\n# pin-disposition fixture v1\nexit 0\n"
SELFTEST_V2 = b"#!/bin/sh\n# pin-disposition fixture v2\nexit 0\n"
SELFTEST_DIRTY = b"#!/bin/sh\n# dirty worktree fixture\nexit 1\n"
SELFTEST_V1_SHA256 = "0b09cbb5f6476e55b830584a18e4b7940da33ee380b8a6c57c32235306b7f607"
SELFTEST_V2_SHA256 = "d459d283bff945fb3fc4acf0be86b35e512a21005f79b7e51778bcb827965e1a"
SELFTEST_DIRTY_SHA256 = "35db8ca11b64c09f964bf88537abc8bc6abe180e6dc4aaae400c8206744d9c2d"


def selftest():
    """Hermetic fixtures under /tmp: no fleet repo, no sibling repo is read."""
    scratch = tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir=strict_scratch_root())
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

    def put(path, data):
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)

    def expect(actual, expected, label):
        return actual == expected, "{}={!r} expects={!r}".format(label, actual, expected)

    def summarize(checks):
        good = all(flag for flag, _ in checks)
        if good:
            return True, "{} literal checks".format(len(checks))
        return False, "; ".join(detail for flag, detail in checks if not flag)

    def rows_by_leg(payload):
        return {
            row.get("leg"): row
            for row in payload.get("legs", [])
            if isinstance(row, dict)
        }

    def field(row, *keys):
        current = row
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
        return current

    try:
        env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        templates = os.path.join(scratch, "git-templates")
        hooks = os.path.join(scratch, "git-hooks")
        os.makedirs(templates)
        os.makedirs(hooks)
        env.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "HOME": scratch,
                "GIT_AUTHOR_NAME": "pin-disposition-selftest",
                "GIT_AUTHOR_EMAIL": "selftest@example.invalid",
                "GIT_COMMITTER_NAME": "pin-disposition-selftest",
                "GIT_COMMITTER_EMAIL": "selftest@example.invalid",
                "LC_ALL": "C",
            }
        )

        def git(cwd, args):
            proc = subprocess.run(
                [
                    "git",
                    "-c",
                    "commit.gpgsign=false",
                    "-c",
                    "init.defaultBranch=main",
                    "-c",
                    "init.templateDir=" + templates,
                    "-c",
                    "core.hooksPath=" + hooks,
                ]
                + args,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60,
                check=False,
            )
            if proc.returncode != 0:
                raise RuntimeError(
                    "fixture git {} failed: {}".format(
                        " ".join(args), proc.stderr.decode("utf-8", "replace").strip()
                    )
                )
            return proc.stdout.decode("utf-8", "replace").strip()

        # The fleet root is a super-repo on purpose: tsukuroi-shokunin is a plain
        # directory inside it, so only the toplevel guard prevents borrowing the
        # super-repo HEAD.
        fleet = os.path.join(scratch, "fleet")
        os.makedirs(fleet)
        git(fleet, ["init", "-q"])
        put(os.path.join(fleet, "tsukuroi-shokunin", "tools", "tsukuroi-census.sh"), SELFTEST_V1)
        git(fleet, ["add", "."])
        git(fleet, ["commit", "-q", "-m", "super"])
        super_commit = git(fleet, ["rev-parse", "HEAD"])

        kumitate = os.path.join(fleet, "kumitate-shokunin")
        os.makedirs(kumitate)
        git(kumitate, ["init", "-q"])
        git(kumitate, ["commit", "-q", "--allow-empty", "-m", "empty"])
        kumitate_empty = git(kumitate, ["rev-parse", "HEAD"])
        put(os.path.join(kumitate, "scripts", "kimi-census.mjs"), SELFTEST_V1)
        put(os.path.join(kumitate, "scripts", "claims-check.mjs"), SELFTEST_V1)
        git(kumitate, ["add", "."])
        git(kumitate, ["commit", "-q", "-m", "files"])
        kumitate_pinned = git(kumitate, ["rev-parse", "HEAD"])
        # Dirty worktree: HEAD stays at the pin, disk bytes move.
        put(os.path.join(kumitate, "scripts", "claims-check.mjs"), SELFTEST_DIRTY)

        kagi = os.path.join(fleet, "kagi-shokunin")
        os.makedirs(kagi)
        git(kagi, ["init", "-q"])
        put(os.path.join(kagi, "corpus", "surface-census.sh"), SELFTEST_V1)
        put(os.path.join(kagi, "corpus", "checklist-run.sh"), SELFTEST_V1)
        git(kagi, ["add", "."])
        git(kagi, ["commit", "-q", "-m", "files"])
        kagi_pinned = git(kagi, ["rev-parse", "HEAD"])
        put(os.path.join(kagi, "corpus", "surface-census.sh"), SELFTEST_V2)
        os.remove(os.path.join(kagi, "corpus", "checklist-run.sh"))
        git(kagi, ["add", "-A"])
        git(kagi, ["commit", "-q", "-m", "changed-head"])
        kagi_head = git(kagi, ["rev-parse", "HEAD"])

        base = {
            "schema": MANIFEST_SCHEMA,
            "source": "selftest fixture",
            "legs": [
                {
                    "leg": "js-kimi-census",
                    "repo": "kumitate-shokunin",
                    "path": "scripts/kimi-census.mjs",
                    "pinned_commit": kumitate_pinned,
                    "expected_sha256": SELFTEST_V1_SHA256,
                },
                {
                    "leg": "bash-surface-census",
                    "repo": "kagi-shokunin",
                    "path": "corpus/surface-census.sh",
                    "pinned_commit": kagi_pinned,
                    "expected_sha256": SELFTEST_V1_SHA256,
                },
                {
                    "leg": "bash-tsukuroi-census",
                    "repo": "tsukuroi-shokunin",
                    "path": "tools/tsukuroi-census.sh",
                    "pinned_commit": super_commit,
                    "expected_sha256": SELFTEST_V1_SHA256,
                },
                {
                    "leg": "bash-mado-verify",
                    "repo": "mado-shokunin",
                    "path": "tools/mado-verify.sh",
                    "pinned_commit": "0" * 40,
                    "expected_sha256": SELFTEST_V1_SHA256,
                },
                {
                    "leg": "bash-checklist-run",
                    "repo": "kagi-shokunin",
                    "path": "corpus/checklist-run.sh",
                    "pinned_commit": kagi_pinned,
                    "expected_sha256": SELFTEST_V1_SHA256,
                },
                {
                    "leg": "js-claims-check",
                    "repo": "kumitate-shokunin",
                    "path": "scripts/claims-check.mjs",
                    "pinned_commit": kumitate_pinned,
                    "expected_sha256": SELFTEST_V1_SHA256,
                },
            ],
        }

        manifests = os.path.join(scratch, "manifests")
        os.makedirs(manifests)

        def write_manifest(name, record_body):
            path = os.path.join(manifests, name + ".json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(record_body, handle, indent=2)
                handle.write("\n")
            return path

        base_path = write_manifest("base", base)
        missing_blob = copy.deepcopy(base)
        for entry in missing_blob["legs"]:
            if entry["leg"] == "js-kimi-census":
                entry["pinned_commit"] = kumitate_empty
        missing_blob_path = write_manifest("missing-pinned-blob", missing_blob)
        missing_commit = copy.deepcopy(base)
        for entry in missing_commit["legs"]:
            if entry["leg"] == "js-kimi-census":
                entry["pinned_commit"] = "a" * 40
        missing_commit_path = write_manifest("missing-pinned-commit", missing_commit)
        digest_mismatch = copy.deepcopy(base)
        for entry in digest_mismatch["legs"]:
            if entry["leg"] == "js-kimi-census":
                entry["expected_sha256"] = SELFTEST_V2_SHA256
        digest_mismatch_path = write_manifest("digest-mismatch", digest_mismatch)
        malformed_digest = copy.deepcopy(base)
        for entry in malformed_digest["legs"]:
            if entry["leg"] == "js-kimi-census":
                entry["expected_sha256"] = "0b09cbb5"
        malformed_digest_path = write_manifest("malformed-digest", malformed_digest)
        duplicate = copy.deepcopy(base)
        duplicate["legs"].append(copy.deepcopy(base["legs"][0]))
        duplicate_path = write_manifest("duplicate-leg", duplicate)
        missing_leg = copy.deepcopy(base)
        missing_leg["legs"] = [
            entry for entry in missing_leg["legs"] if entry["leg"] != "bash-mado-verify"
        ]
        missing_leg_path = write_manifest("missing-leg", missing_leg)
        malformed_json_path = os.path.join(manifests, "malformed-json.json")
        with open(malformed_json_path, "w", encoding="utf-8") as handle:
            handle.write('{"schema": "pin-manifest-v1", "legs": [')
        absent_manifest_path = os.path.join(manifests, "does-not-exist.json")

        def run_cli(args):
            proc = subprocess.run(
                [sys.executable, SELF] + args,
                cwd=scratch,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                check=False,
            )
            try:
                payload = json.loads(proc.stdout.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                payload = None
            return proc, payload

        def case(name, args, expect_exit, verify):
            proc, payload = run_cli(args)
            ok = proc.returncode == expect_exit and payload is not None
            detail = "exit={} expects={}".format(proc.returncode, expect_exit)
            if payload is None:
                detail += " json=absent stderr={!r}".format(
                    proc.stderr.decode("utf-8", "replace")[:120]
                )
            elif verify is not None:
                try:
                    verified, verified_detail = verify(payload)
                except (KeyError, TypeError, AttributeError) as exc:
                    verified, verified_detail = False, "verify-crashed={!r}".format(exc)
                ok = ok and verified
                detail += " " + verified_detail
            record(name, ok, detail)

        def verify_leg(payload, leg, checks):
            row = rows_by_leg(payload).get(leg)
            if row is None:
                return False, "leg {} absent".format(leg)
            combined = [
                expect(payload.get("status"), "ok", "status"),
                expect(payload.get("result_reuse"), RESULT_REUSE, "reuse"),
                expect(len(payload.get("legs", [])), 6, "rows"),
                expect(row.get("result_reuse"), RESULT_REUSE, "row-reuse"),
                expect(
                    all(
                        item.get("result_reuse") == RESULT_REUSE
                        for item in payload.get("legs", [])
                        if isinstance(item, dict)
                    ),
                    True,
                    "all-row-reuse",
                ),
                expect(
                    "mode/exec-bit" in payload.get("not_compared", []),
                    True,
                    "not-compared-mode",
                ),
                expect(
                    (payload.get("observed_at") or "").endswith("Z"),
                    True,
                    "observed-at",
                ),
            ]
            for label, actual, expected in checks:
                combined.append(expect(actual, expected, label))
            return summarize(combined)

        case(
            "unchanged",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-kimi-census",
                [
                    ("content", field(rows_by_leg(payload)["js-kimi-census"], "content_status"), "unchanged"),
                    ("pin-status", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "status"), "verified"),
                    ("pin-sha", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("head-status", field(rows_by_leg(payload)["js-kimi-census"], "head", "status"), "present"),
                    ("head-sha", field(rows_by_leg(payload)["js-kimi-census"], "head", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("worktree-sha", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "sha256"), SELFTEST_V1_SHA256),
                    ("pin-commit", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "commit"), kumitate_pinned),
                    ("head-commit", field(rows_by_leg(payload)["js-kimi-census"], "head", "commit"), kumitate_pinned),
                ],
            ),
        )
        case(
            "changed-head",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "bash-surface-census",
                [
                    ("content", field(rows_by_leg(payload)["bash-surface-census"], "content_status"), "changed"),
                    ("pin-status", field(rows_by_leg(payload)["bash-surface-census"], "pinned", "status"), "verified"),
                    ("pin-commit", field(rows_by_leg(payload)["bash-surface-census"], "pinned", "commit"), kagi_pinned),
                    ("pin-sha", field(rows_by_leg(payload)["bash-surface-census"], "pinned", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("head-status", field(rows_by_leg(payload)["bash-surface-census"], "head", "status"), "present"),
                    ("head-commit", field(rows_by_leg(payload)["bash-surface-census"], "head", "commit"), kagi_head),
                    ("head-sha", field(rows_by_leg(payload)["bash-surface-census"], "head", "blob_sha256"), SELFTEST_V2_SHA256),
                    ("worktree-sha", field(rows_by_leg(payload)["bash-surface-census"], "worktree", "sha256"), SELFTEST_V2_SHA256),
                    ("head-differs", field(rows_by_leg(payload)["bash-surface-census"], "head", "commit") != kagi_pinned, True),
                ],
            ),
        )
        case(
            "dirty-worktree",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-claims-check",
                [
                    ("content", field(rows_by_leg(payload)["js-claims-check"], "content_status"), "changed"),
                    ("pin-status", field(rows_by_leg(payload)["js-claims-check"], "pinned", "status"), "verified"),
                    ("pin-sha", field(rows_by_leg(payload)["js-claims-check"], "pinned", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("head-sha", field(rows_by_leg(payload)["js-claims-check"], "head", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("worktree-sha", field(rows_by_leg(payload)["js-claims-check"], "worktree", "sha256"), SELFTEST_DIRTY_SHA256),
                    ("head-commit", field(rows_by_leg(payload)["js-claims-check"], "head", "commit"), kumitate_pinned),
                ],
            ),
        )
        case(
            "missing-worktree-file",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "bash-checklist-run",
                [
                    ("content", field(rows_by_leg(payload)["bash-checklist-run"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["bash-checklist-run"], "pinned", "status"), "verified"),
                    ("pin-sha", field(rows_by_leg(payload)["bash-checklist-run"], "pinned", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("head-status", field(rows_by_leg(payload)["bash-checklist-run"], "head", "status"), "absent"),
                    ("worktree-sha", field(rows_by_leg(payload)["bash-checklist-run"], "worktree", "sha256"), None),
                    ("worktree-reason", field(rows_by_leg(payload)["bash-checklist-run"], "worktree", "reason"), "worktree_missing"),
                ],
            ),
        )
        case(
            "missing-repo",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "bash-mado-verify",
                [
                    ("content", field(rows_by_leg(payload)["bash-mado-verify"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["bash-mado-verify"], "pinned", "status"), "unavailable"),
                    ("pin-reason", field(rows_by_leg(payload)["bash-mado-verify"], "pinned", "reason"), "repo_missing"),
                    ("head-status", field(rows_by_leg(payload)["bash-mado-verify"], "head", "status"), "unavailable"),
                    ("head-reason", field(rows_by_leg(payload)["bash-mado-verify"], "head", "reason"), "repo_missing"),
                    ("worktree-reason", field(rows_by_leg(payload)["bash-mado-verify"], "worktree", "reason"), "repo_missing"),
                    ("worktree-sha", field(rows_by_leg(payload)["bash-mado-verify"], "worktree", "sha256"), None),
                ],
            ),
        )
        case(
            "foreign-repo-toplevel",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "bash-tsukuroi-census",
                [
                    ("content", field(rows_by_leg(payload)["bash-tsukuroi-census"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["bash-tsukuroi-census"], "pinned", "status"), "unavailable"),
                    ("pin-reason", field(rows_by_leg(payload)["bash-tsukuroi-census"], "pinned", "reason"), "repo_foreign"),
                    ("head-status", field(rows_by_leg(payload)["bash-tsukuroi-census"], "head", "status"), "unavailable"),
                    ("head-reason", field(rows_by_leg(payload)["bash-tsukuroi-census"], "head", "reason"), "repo_foreign"),
                    ("worktree-reason", field(rows_by_leg(payload)["bash-tsukuroi-census"], "worktree", "reason"), "repo_foreign"),
                    ("worktree-sha", field(rows_by_leg(payload)["bash-tsukuroi-census"], "worktree", "sha256"), None),
                ],
            ),
        )
        case(
            "missing-pinned-blob",
            ["--manifest", missing_blob_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-kimi-census",
                [
                    ("content", field(rows_by_leg(payload)["js-kimi-census"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "status"), "unavailable"),
                    ("pin-reason", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "reason"), "pinned_path_missing"),
                    ("head-status", field(rows_by_leg(payload)["js-kimi-census"], "head", "status"), "present"),
                    ("worktree-sha", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "sha256"), SELFTEST_V1_SHA256),
                    ("worktree-status", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "status"), "unavailable"),
                    ("worktree-reason", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "reason"), "pin_not_verified"),
                ],
            ),
        )
        case(
            "missing-pinned-commit",
            ["--manifest", missing_commit_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-kimi-census",
                [
                    ("content", field(rows_by_leg(payload)["js-kimi-census"], "content_status"), "unavailable"),
                    ("pin-reason", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "reason"), "pinned_commit_missing"),
                    ("worktree-reason", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "reason"), "pin_not_verified"),
                ],
            ),
        )
        case(
            "pinned-blob-mismatch",
            ["--manifest", digest_mismatch_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-kimi-census",
                [
                    ("content", field(rows_by_leg(payload)["js-kimi-census"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "status"), "mismatch"),
                    ("pin-reason", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "reason"), "pinned_blob_mismatch"),
                    ("pin-observed", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("head-status", field(rows_by_leg(payload)["js-kimi-census"], "head", "status"), "present"),
                    ("worktree-sha", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "sha256"), SELFTEST_V1_SHA256),
                    ("worktree-status", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "status"), "unavailable"),
                    ("worktree-reason", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "reason"), "pin_not_verified"),
                ],
            ),
        )

        # Fixture-mutating arms run after every byte-comparison arm above.
        outside_scripts = os.path.join(scratch, "outside-scripts")
        os.makedirs(outside_scripts)
        put(os.path.join(outside_scripts, "kimi-census.mjs"), SELFTEST_V1)
        put(os.path.join(outside_scripts, "claims-check.mjs"), SELFTEST_DIRTY)
        kumitate_scripts = os.path.join(kumitate, "scripts")
        os.rename(kumitate_scripts, kumitate_scripts + ".real")
        os.symlink(outside_scripts, kumitate_scripts)
        case(
            "worktree-outside-repo",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-kimi-census",
                [
                    ("content", field(rows_by_leg(payload)["js-kimi-census"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "status"), "verified"),
                    ("head-status", field(rows_by_leg(payload)["js-kimi-census"], "head", "status"), "present"),
                    ("worktree-sha", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "sha256"), None),
                    ("worktree-status", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "status"), "unavailable"),
                    ("worktree-reason", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "reason"), "worktree_outside_repo"),
                ],
            ),
        )
        os.remove(kumitate_scripts)
        os.rename(kumitate_scripts + ".real", kumitate_scripts)

        kimi_path = os.path.join(kumitate, "scripts", "kimi-census.mjs")
        os.rename(kimi_path, kimi_path + ".real")
        os.symlink("claims-check.mjs", kimi_path)
        case(
            "worktree-symlink",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "js-kimi-census",
                [
                    ("content", field(rows_by_leg(payload)["js-kimi-census"], "content_status"), "unavailable"),
                    ("pin-status", field(rows_by_leg(payload)["js-kimi-census"], "pinned", "status"), "verified"),
                    ("head-status", field(rows_by_leg(payload)["js-kimi-census"], "head", "status"), "present"),
                    ("worktree-sha", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "sha256"), None),
                    ("worktree-status", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "status"), "unavailable"),
                    ("worktree-reason", field(rows_by_leg(payload)["js-kimi-census"], "worktree", "reason"), "worktree_symlink"),
                ],
            ),
        )
        os.remove(kimi_path)
        os.rename(kimi_path + ".real", kimi_path)

        mado_link = os.path.join(fleet, "mado-shokunin")
        os.symlink(kumitate, mado_link)
        case(
            "repo-symlink",
            ["--manifest", base_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "bash-mado-verify",
                [
                    ("content", field(rows_by_leg(payload)["bash-mado-verify"], "content_status"), "unavailable"),
                    ("pin-reason", field(rows_by_leg(payload)["bash-mado-verify"], "pinned", "reason"), "repo_symlink"),
                    ("head-reason", field(rows_by_leg(payload)["bash-mado-verify"], "head", "reason"), "repo_symlink"),
                    ("worktree-sha", field(rows_by_leg(payload)["bash-mado-verify"], "worktree", "sha256"), None),
                    ("worktree-reason", field(rows_by_leg(payload)["bash-mado-verify"], "worktree", "reason"), "repo_symlink"),
                ],
            ),
        )
        os.remove(mado_link)

        def verify_error(kind, fragment):
            def check(payload):
                checks = [
                    expect(payload.get("status"), "invalid_input", "status"),
                    expect(field(payload, "error", "kind"), kind, "kind"),
                    expect(fragment in (field(payload, "error", "message") or ""), True, "message-has-" + fragment),
                    expect(payload.get("legs"), [], "no-rows"),
                ]
                return summarize(checks)

            return check

        case(
            "malformed-digest",
            ["--manifest", malformed_digest_path, "--root", fleet],
            2,
            verify_error("invalid_manifest", "expected_sha256"),
        )
        case(
            "duplicate-leg",
            ["--manifest", duplicate_path, "--root", fleet],
            2,
            verify_error("invalid_manifest", "duplicate leg"),
        )
        case(
            "missing-leg",
            ["--manifest", missing_leg_path, "--root", fleet],
            2,
            verify_error("invalid_manifest", "omits recorded leg"),
        )
        case(
            "malformed-json",
            ["--manifest", malformed_json_path, "--root", fleet],
            2,
            verify_error("invalid_manifest", "not valid JSON"),
        )
        case(
            "missing-manifest",
            ["--manifest", absent_manifest_path, "--root", fleet],
            2,
            verify_error("invalid_manifest", "manifest not found"),
        )
        case(
            "invalid-root",
            ["--manifest", base_path, "--root", os.path.join(scratch, "no-such-root")],
            2,
            verify_error("invalid_root", "fleet root"),
        )

        # Detached HEAD one commit ahead of master with different file bytes:
        # the head observation must read the branch tip (master), not raw
        # HEAD. This is the jj colocated state JjAuditTameshi.md §1.2/:317,
        # §2.3 and §5 R2 flag for this lane.
        mado = os.path.join(fleet, "mado-shokunin")
        os.makedirs(mado)
        git(mado, ["init", "-q"])
        git(mado, ["symbolic-ref", "HEAD", "refs/heads/master"])
        put(os.path.join(mado, "tools", "mado-verify.sh"), SELFTEST_V1)
        git(mado, ["add", "."])
        git(mado, ["commit", "-q", "-m", "master-tip"])
        mado_master_tip = git(mado, ["rev-parse", "HEAD"])
        put(os.path.join(mado, "tools", "mado-verify.sh"), SELFTEST_V2)
        git(mado, ["checkout", "-q", "--detach", "HEAD"])
        git(mado, ["commit", "-q", "-am", "detached-ahead"])
        mado_detached = git(mado, ["rev-parse", "HEAD"])
        detached = copy.deepcopy(base)
        for entry in detached["legs"]:
            if entry["leg"] == "bash-mado-verify":
                entry["pinned_commit"] = mado_master_tip
        detached_path = write_manifest("detached-head", detached)
        case(
            "detached-head-uses-branch-tip",
            ["--manifest", detached_path, "--root", fleet],
            0,
            lambda payload: verify_leg(
                payload,
                "bash-mado-verify",
                [
                    ("branch", field(rows_by_leg(payload)["bash-mado-verify"], "head", "branch"), "master"),
                    ("head-commit", field(rows_by_leg(payload)["bash-mado-verify"], "head", "commit"), mado_master_tip),
                    ("head-status", field(rows_by_leg(payload)["bash-mado-verify"], "head", "status"), "present"),
                    ("head-sha", field(rows_by_leg(payload)["bash-mado-verify"], "head", "blob_sha256"), SELFTEST_V1_SHA256),
                    ("differs", field(rows_by_leg(payload)["bash-mado-verify"], "head", "head_differs_from_branch"), True),
                    ("detached-distinct", mado_detached != mado_master_tip, True),
                    ("worktree-sha", field(rows_by_leg(payload)["bash-mado-verify"], "worktree", "sha256"), SELFTEST_V2_SHA256),
                ],
            ),
        )
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print("SELFTEST: COULD_NOT_EVALUATE ({}; fixtures kept at {})".format(exc, scratch))
        return 2

    total = passed + len(failed)
    if failed:
        print(
            "SELFTEST: FAIL ({}/{} failed: {}; fixtures kept at {})".format(
                len(failed), total, ", ".join(failed), scratch
            )
        )
        return 1
    shutil.rmtree(scratch, ignore_errors=True)
    print("SELFTEST: PASS ({}/{})".format(passed, total))
    return 0


# ----------------------------------------------------------------------- main


def parse_argv(argv):
    if not argv:
        raise InvalidInput("invalid_usage", "no arguments")
    manifest = None
    root = None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--manifest", "--root"):
            if index + 1 >= len(argv):
                raise InvalidInput("invalid_usage", arg + " needs a value")
            value = argv[index + 1]
            index += 2
        elif arg.startswith("--manifest=") or arg.startswith("--root="):
            arg, value = arg.split("=", 1)
            index += 1
        else:
            raise InvalidInput("invalid_usage", "unknown argument: " + arg)
        if not value:
            raise InvalidInput("invalid_usage", arg + " has an empty value")
        if arg == "--manifest":
            if manifest is not None:
                raise InvalidInput("invalid_usage", "--manifest given twice")
            manifest = value
        else:
            if root is not None:
                raise InvalidInput("invalid_usage", "--root given twice")
            root = value
    if manifest is None:
        raise InvalidInput("invalid_usage", "--manifest is required")
    if root is None:
        raise InvalidInput("invalid_usage", "--root is required")
    return manifest, root


def main(argv):
    if not argv:
        return invalid_input("invalid_usage", "no arguments (see --help)")
    if argv in (["--help"], ["-h"]):
        sys.stdout.write(USAGE)
        return 0
    if argv == ["--selftest"]:
        return selftest()
    if "--selftest" in argv:
        return invalid_input("invalid_usage", "--selftest takes no other arguments")
    try:
        manifest, root = parse_argv(argv)
        return run_mode(manifest, root)
    except InvalidInput as exc:
        return invalid_input(exc.kind, str(exc))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
