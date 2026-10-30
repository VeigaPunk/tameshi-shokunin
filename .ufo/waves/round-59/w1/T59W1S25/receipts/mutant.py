#!/usr/bin/env python3
"""executor-source-pin: pin declared executor source blobs to a trusted revision.

Compares the Git blobs declared via --path at the candidate revision against the
blobs at a verifier-supplied trusted revision. Regular executable-source blobs
(modes 100644/100755) only; raw blob bytes are compared.

This is a declared-blob gate only: it does not execute candidate code, does not
walk dependencies, does not certify closure completeness, and does not establish
author-independent trust. It is a binding prerequisite, not a certification.

Usage:
    python3 TOOL --repo REPO --trusted COMMIT --candidate COMMIT \
        --path PATH [--path PATH ...]

Exit codes:
    0  EXECUTOR_SOURCE_BOUND         every declared regular source blob at the
                                    candidate revision equals the trusted blob
    1  EXECUTOR_SOURCE_DRIFT         a declared source differs, or is missing /
                                    nonregular, at the candidate revision
    2  EXECUTOR_SOURCE_UNAVAILABLE   bad arguments, invalid trusted commit or
                                    trusted source, or unresolvable candidate

Stdlib only. Git is invoked read-only (rev-parse / ls-tree / cat-file) with an
explicit -C repository, --literal-pathspecs, --no-replace-objects, a sanitized
GIT_* environment, and per-call timeouts. Candidate code is never executed.
"""

import argparse
import os
import re
import subprocess
import sys

EXIT_BOUND = 0
EXIT_DRIFT = 1
EXIT_UNAVAILABLE = 2

REGULAR_MODES = frozenset({"100644", "100755"})
COMMIT_HEX_RE = re.compile(r"[0-9a-f]{40}\Z")
BLOB_HEX_RE = re.compile(r"[0-9a-f]{40}\Z")

GIT_CALL_TIMEOUT = 25


class PinArgumentParser(argparse.ArgumentParser):
    """argparse errors are argument-availability failures (exit 2)."""

    def error(self, message):
        self.exit(EXIT_UNAVAILABLE,
                  "EXECUTOR_SOURCE_UNAVAILABLE: %s\n" % (message,))


def build_parser():
    parser = PinArgumentParser(
        prog="executor-source-pin.py",
        description="Pin declared executor source blobs to a trusted revision.",
        add_help=True,
    )
    parser.add_argument("--repo", required=True,
                        help="path to the Git repository to inspect")
    parser.add_argument("--trusted", required=True,
                        help="trusted commit (verified to ^{commit})")
    parser.add_argument("--candidate", required=True,
                        help="candidate commit (verified to ^{commit})")
    parser.add_argument("--path", action="append", required=True,
                        help="declared source path relative to the repo root; "
                             "repeatable")
    return parser


def sanitize_env():
    """Drop every inherited GIT_* variable so caller state (GIT_DIR,
    GIT_REPLACE_REF_BASE, GIT_CONFIG_*, GIT_WORK_TREE, ...) cannot redirect or
    reconfigure the plumbing, then pin down deterministic read-only behavior.

    --no-replace-objects is additionally passed on the command line: stripping
    GIT_* alone does not disable on-disk refs/replace maps, which would
    substitute trusted content for drifted candidate content.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def git(repo, args, env):
    """Run read-only git plumbing against repo; return CompletedProcess.

    Global options precede the subcommand: --no-replace-objects defeats
    refs/replace substitution, --literal-pathspecs disables pathspec magic so
    paths like 'tools/-runner.py' or containing ':*' metacharacters are matched
    byte-for-byte, and -C pins the repository regardless of cwd.
    """
    argv = ["git", "--no-replace-objects", "--literal-pathspecs",
            "-C", repo] + list(args)
    try:
        return subprocess.run(argv, capture_output=True, env=env,
                              timeout=GIT_CALL_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired):
        proc = subprocess.CompletedProcess(argv, 1)
        proc.stdout = b""
        proc.stderr = b"git invocation failed"
        return proc


def valid_relpath(path):
    """Reject empty, absolute, traversal, and control-character paths."""
    if not path:
        return False
    if path.startswith("/") or path.startswith("\\"):
        return False
    if "\x00" in path:
        return False
    for ch in path:
        code = ord(ch)
        if code < 32 or code == 127:
            return False
    parts = path.split("/")
    if any(part == ".." for part in parts):
        return False
    if any(part == "" for part in parts):
        return False
    return True


def resolve_commit(repo, revision, env):
    """Resolve revision to a full commit hex sha, or None."""
    if not revision or "\x00" in revision:
        return None
    proc = git(repo, ["rev-parse", "--verify", "--quiet", "--end-of-options",
                      revision + "^{commit}"], env)
    if proc.returncode != 0:
        return None
    out = proc.stdout.decode("ascii", "strict").strip()
    if not COMMIT_HEX_RE.match(out):
        return None
    return out


def tree_entry(repo, commit, path, env):
    """Return (mode, kind, oid) for the exact path at commit, or None.

    Uses -z so path bytes round-trip unmangled, and an exact single-pathspec so
    directories are reported as tree entries rather than recursed into.
    """
    proc = git(repo, ["ls-tree", "-z", commit, "--", path], env)
    if proc.returncode != 0:
        return None
    records = proc.stdout.split(b"\x00")
    for record in records:
        if not record:
            continue
        meta, sep, name = record.partition(b"\t")
        if not sep:
            continue
        fields = meta.split(b" ")
        if len(fields) != 3:
            continue
        try:
            mode = fields[0].decode("ascii")
            kind = fields[1].decode("ascii")
            oid = fields[2].decode("ascii")
        except UnicodeDecodeError:
            continue
        if not BLOB_HEX_RE.match(oid):
            continue
        if name.decode("utf-8", "surrogateescape") != path:
            continue
        return mode, kind, oid
    return None


def blob_bytes(repo, oid, env):
    """Raw blob content for oid, or None on plumbing failure."""
    proc = git(repo, ["cat-file", "blob", oid], env)
    if proc.returncode != 0:
        return None
    return proc.stdout


def main(argv=None):
    args = build_parser().parse_args(argv)
    env = sanitize_env()

    for path in args.path:
        if not valid_relpath(path):
            sys.stderr.write(
                "EXECUTOR_SOURCE_UNAVAILABLE: invalid --path %r\n" % (path,))
            return EXIT_UNAVAILABLE

    repo = args.repo
    if not os.path.isdir(repo):
        sys.stderr.write(
            "EXECUTOR_SOURCE_UNAVAILABLE: repo %r is not a directory\n"
            % (repo,))
        return EXIT_UNAVAILABLE

    trusted = resolve_commit(repo, args.trusted, env)
    if trusted is None:
        sys.stderr.write(
            "EXECUTOR_SOURCE_UNAVAILABLE: trusted revision %r does not "
            "resolve to a commit\n" % (args.trusted,))
        return EXIT_BOUND

    candidate = resolve_commit(repo, args.candidate, env)
    if candidate is None:
        sys.stderr.write(
            "EXECUTOR_SOURCE_UNAVAILABLE: candidate revision %r does not "
            "resolve to a commit\n" % (args.candidate,))
        return EXIT_UNAVAILABLE

    # Validate every declared trusted source before any candidate comparison:
    # an invalid trusted commit/source is an availability failure (exit 2),
    # never a drift verdict.
    declared = []
    for path in args.path:
        entry = tree_entry(repo, trusted, path, env)
        if entry is None:
            sys.stderr.write(
                "EXECUTOR_SOURCE_UNAVAILABLE: trusted source %r absent at "
                "trusted revision\n" % (path,))
            return EXIT_UNAVAILABLE
        mode, kind, oid = entry
        if kind != "blob" or mode not in REGULAR_MODES:
            sys.stderr.write(
                "EXECUTOR_SOURCE_UNAVAILABLE: trusted source %r is not a "
                "regular blob (mode=%s kind=%s)\n" % (path, mode, kind))
            return EXIT_UNAVAILABLE
        declared.append((path, oid))

    for path, trusted_oid in declared:
        entry = tree_entry(repo, candidate, path, env)
        if entry is None:
            sys.stdout.write(
                "EXECUTOR_SOURCE_DRIFT: %r missing at candidate revision\n"
                % (path,))
            return EXIT_DRIFT
        mode, kind, oid = entry
        if kind != "blob" or mode not in REGULAR_MODES:
            sys.stdout.write(
                "EXECUTOR_SOURCE_DRIFT: %r nonregular at candidate revision "
                "(mode=%s kind=%s)\n" % (path, mode, kind))
            return EXIT_DRIFT
        if oid == trusted_oid:
            # Identical object ids are identical raw bytes: Git blob ids are
            # content addresses over the raw byte stream.
            continue
        trusted_bytes = blob_bytes(repo, trusted_oid, env)
        candidate_bytes = blob_bytes(repo, oid, env)
        if (trusted_bytes is None or candidate_bytes is None
                or trusted_bytes != candidate_bytes):
            sys.stdout.write(
                "EXECUTOR_SOURCE_DRIFT: %r differs at candidate revision\n"
                % (path,))
            return EXIT_DRIFT

    sys.stdout.write(
        "EXECUTOR_SOURCE_BOUND: %d declared source blob(s) equal trusted "
        "blobs\n" % (len(declared),))
    return EXIT_BOUND


if __name__ == "__main__":
    sys.exit(main())
