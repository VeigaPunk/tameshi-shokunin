#!/usr/bin/env python3
"""Flag landed seat reports that were rewritten instead of appended to.

Every file under ``.ufo/waves/round-*/`` that exists at FROM is a landed
wave artifact (seat report, spec, registry, receipt).  The carried rule is
append-only: a later revision may add bytes after the old end, but the
bytes at FROM must remain a prefix.  This checker reports every violation.

    usage: seat-report-append-only.py LANE FROM TO

LANE  repository path (git work tree; any subdirectory is resolved to its
      top level)
FROM  revision whose tree is the baseline
TO    revision whose tree is checked

For each file under ``.ufo/waves/round-*/`` present at FROM the file is
reported REWRITTEN when

  * it is absent at TO (deleted), or
  * its bytes at TO do not begin with its bytes at FROM (in-place edit,
    truncation, or a replacement that moves earlier bytes), or
  * one side is not a git blob and a prefix cannot be established.

Output is one line per violation, then a summary line::

    REWRITTEN\t<path>\t<reason>
    SUMMARY\tchecked=<n>\trewritten=<m>

Exit status: 0 when no file was rewritten, 1 when at least one was,
2 on a setup error (bad arguments, not a repository, unresolvable
revision, git failure).  Only read-only git plumbing is used
(``rev-parse``, ``ls-tree``, ``cat-file``); the work tree, index and
refs are never touched.
"""

import os
import re
import subprocess
import sys

ROUND_FILE = re.compile(r"^\.ufo/waves/round-[^/]+/")


class SetupError(Exception):
    """Raised when the checker cannot establish the comparison."""


def git(lane, *args, stdin_data=None):
    try:
        proc = subprocess.run(
            ["git", "-C", lane] + list(args),
            input=stdin_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:  # git itself is missing
        raise SetupError("git executable not found: %s" % exc)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise SetupError(
            "git %s failed (rc=%d): %s" % (" ".join(args), proc.returncode, detail)
        )
    return proc.stdout


def resolve_rev(lane, spec):
    """Resolve *spec* to a full commit id, or raise SetupError."""
    try:
        out = git(
            lane, "rev-parse", "--verify", "--quiet", "--end-of-options",
            spec + "^{commit}",
        )
    except SetupError:
        raise SetupError("cannot resolve revision %r to a commit in %s" % (spec, lane))
    rev = out.decode("ascii", "replace").strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", rev):
        raise SetupError("revision %r did not resolve to a commit" % spec)
    return rev


def tree_files(lane, rev):
    """Map path -> (mode, type, sha) for .ufo/waves/round-*/ files at *rev*."""
    out = git(lane, "ls-tree", "-r", "-z", "--full-tree", rev, "--", ".ufo/waves")
    files = {}
    for record in out.split(b"\0"):
        if not record:
            continue
        try:
            meta, path_b = record.split(b"\t", 1)
        except ValueError:
            raise SetupError("unparseable ls-tree record: %r" % record[:80])
        path = path_b.decode("utf-8", "surrogateescape")
        if not ROUND_FILE.match(path):
            continue
        fields = meta.split(b" ")
        if len(fields) != 3:
            raise SetupError("unparseable ls-tree metadata for %s" % path)
        mode, kind, sha = (f.decode("ascii", "replace") for f in fields)
        files[path] = (mode, kind, sha)
    return files


class BlobReader:
    """Read blobs from one persistent ``git cat-file --batch`` process."""

    def __init__(self, lane):
        try:
            self.proc = subprocess.Popen(
                ["git", "-C", lane, "cat-file", "--batch"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        except OSError as exc:
            raise SetupError("cannot start git cat-file: %s" % exc)

    def read(self, sha):
        try:
            self.proc.stdin.write(sha.encode("ascii") + b"\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise SetupError("git cat-file stream closed: %s" % exc)
        header = self.proc.stdout.readline()
        if not header:
            raise SetupError("git cat-file produced no header for %s" % sha)
        fields = header.split()
        if len(fields) != 3 or fields[1] != b"blob":
            raise SetupError(
                "git cat-file cannot read blob %s: %s"
                % (sha, header.decode("utf-8", "replace").strip())
            )
        try:
            size = int(fields[2])
        except ValueError:
            raise SetupError("git cat-file size field is not numeric: %r" % header)
        try:
            data = self.proc.stdout.read(size)
        except OSError as exc:
            raise SetupError("reading blob %s failed: %s" % (sha, exc))
        if len(data) != size:
            raise SetupError(
                "short read for blob %s: %d of %d bytes" % (sha, len(data), size)
            )
        self.proc.stdout.read(1)  # the record's trailing newline
        return data

    def close(self):
        for stream in (self.proc.stdin, self.proc.stdout):
            try:
                stream.close()
            except OSError:
                pass
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()


def check(lane, from_rev, to_rev):
    """Return (checked_count, [(path, reason)]) for every rewritten file."""
    before = tree_files(lane, from_rev)
    after = tree_files(lane, to_rev)

    violations = []
    from_reader = to_reader = None
    try:
        for path in sorted(before):
            mode, kind, sha = before[path]
            if kind != "blob":
                violations.append((path, "source-not-a-blob"))
                continue
            target = after.get(path)
            if target is None:
                violations.append((path, "deleted"))
                continue
            t_mode, t_kind, t_sha = target
            if t_kind != "blob":
                violations.append((path, "target-not-a-blob"))
                continue
            if t_sha == sha:
                continue
            if from_reader is None:
                from_reader = BlobReader(lane)
                to_reader = BlobReader(lane)
            old = from_reader.read(sha)
            new = to_reader.read(t_sha)
            if not new.startswith(old):
                violations.append((path, "prefix-lost"))
    finally:
        for reader in (from_reader, to_reader):
            if reader is not None:
                reader.close()
    return len(before), violations


def main(argv):
    if len(argv) != 4:
        sys.stderr.write("usage: seat-report-append-only.py LANE FROM TO\n")
        return 2
    lane_arg, from_spec, to_spec = argv[1], argv[2], argv[3]

    try:
        if not os.path.isdir(lane_arg):
            raise SetupError("LANE is not a directory: %s" % lane_arg)
        top = git(lane_arg, "rev-parse", "--show-toplevel").decode(
            "utf-8", "surrogateescape"
        ).strip()
        if not top:
            raise SetupError("LANE is not inside a git work tree: %s" % lane_arg)
        lane = os.path.realpath(top)
        from_rev = resolve_rev(lane, from_spec)
        to_rev = resolve_rev(lane, to_spec)
        checked, violations = check(lane, from_rev, to_rev)
    except SetupError as exc:
        sys.stderr.write("ERROR: %s\n" % exc)
        return 2

    for path, reason in violations:
        sys.stdout.write("REWRITTEN\t%s\t%s\n" % (path, reason))
    sys.stdout.write(
        "SUMMARY\tchecked=%d\trewritten=%d\n" % (checked, len(violations))
    )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
