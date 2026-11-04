#!/usr/bin/env python3
r"""tools/defect-bind.py — bind a closure's routed defect register to repo state.

A non-author closure routes defects for the lane's next round as prose. Without
a counter, "closed" is an assertion: the round-80 spot-check's six routed
defects (D1-D6) were prose, so nothing could re-derive whether the next round
actually closed them (the round-80 lesson mistake class: stale
self-description). This tool turns each routed defect into one declared row
whose state is MEASURED over committed bytes, and the lane's claim counter is
the mismatch count between the register's declared state and the observed
state.

Row kinds (all paths repo-relative; every input read from git objects, never a
worktree — S289: `git cat-file blob <rev>:<path>` binds committed bytes):

  tree-paths     every listed path must exist in the tree at `rev` AND be a
                 REGULAR BLOB (`git ls-tree -z` mode 100644 or 100755; S305's
                 listing form, S291's mode field). A directory (040000 tree)
                 or a symlink (120000 blob) is not the artifact a path row
                 means: round 81 measured `git cat-file -e` accepting both, so
                 a directory or a symlink target satisfied a row it never
                 represented. The row then measures `open`, detail
                 `not-regular-file:<path>=<mode>`.
  tree-bytes     every listed path is a regular blob at `rev` (same mode/type
                 boundary — a symlink's blob is its target string, so a
                 mode-blind `min_bytes` reads the link, not the artifact) and
                 its blob length is at least `min_bytes` (an empty committed
                 blob is not evidence: the round-80 D1 case committed a 0-byte
                 file for a 7.1 MB receipt).
  receipt-tokens one `span` must be a byte substring of the `doc` blob at
                 `rev`, and every token must be a byte substring of the
                 `receipt` blob at `rev` (the red arm: a token the record
                 claims as its receipt's figure must live in that receipt).
  sources-cell   the `corpus/SOURCES.md` row named by `id` (0-3 leading
                 spaces, the census parser's own tolerance) must carry every
                 token in its `used-by` cell (the last cell).
  doc-contains   every token must occur inside the named `## section` of the
                 `doc` blob at `rev` (a token in another section does not
                 count: the D6 search-log defect).

Rows carry `expect` (`closed` by default, `open` for a standing red arm). A
row's measured state is `closed` or `open`; a row whose state differs from its
expectation is `unexpected` and fails the sweep. An empty manifest is refused
exit 2 (a gate that measures nothing must not exit 0). Unresolvable inputs are
setup exit 2 *before* any row effect: a non-manifest JSON, an unknown kind, a
duplicate id, an absolute or `..` path, an empty token/span/path list, an
unresolvable revision. A row's own input that cannot be read at its declared
rev (a blob path that is a tree, a rev that resolves to no object) is a setup
refusal too, but it fires at that row's measurement, so earlier rows may
already have printed: the summary line is the verdict, never the row prefix.

The population is bound, not assumed: `--manifest-rev REV` requires the
manifest's bytes on disk to be byte-identical to the blob committed at
`REV:<manifest path>` (S103: the object id names the bytes; S289 reads them),
so a caller cannot delete a row or relax an `expect` and still measure every
remaining row green. A mismatch is `manifest-rev-mismatch`, exit 2, before any
row effect. Declared limit (S311): with `text`/`eol`/filter attributes on the
manifest path the worktree bytes may legitimately differ from the blob, so the
binding is exact only where no conversion attribute applies.

Usage:
  python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json
  python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json --manifest-rev REV
  python3 -I -X utf8 tools/defect-bind.py --selftest

Summary line: DEFECT_BIND: rows=N closed=C open=O unexpected=U manifest=<bound|unbound>
Row line:     DEFECT_BIND_ROW <id> kind=<kind> expect=<e> state=<s> detail=<d>
Exit: 0 every row matches its expectation; 1 any mismatch; 2 setup refusal.
"""

import argparse
import contextlib
import hashlib
import inspect
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCHEMA = "tameshi-defect-bind-v1"
KINDS = ("tree-paths", "tree-bytes", "receipt-tokens", "sources-cell",
         "doc-contains")
SOURCES_PATH = "corpus/SOURCES.md"
REGULAR_MODES = ("100644", "100755")
SELFTEST_ARMS = 14
# sha256 of inspect.getsource(selftest) at the landing commit. The pin covers
# the function's own text only: a module-level edit, a vacuous comment inside
# the function (over-kill) or a two-edit rewrite (weaken an arm and recompute
# this constant) stay outside the class, exactly the round-81 declared limits.
SELFTEST_TEXT_SHA256 = ("9d9dcf373be1f13795c6382d39e36551e04bf9ceadf3de375158beb23e78e8a7")


class SetupError(Exception):
    """A pre-effect refusal (exit 2), never a row verdict."""


def _git_env():
    """Strip every inherited GIT_* variable: a fixture repo must not inherit
    the caller's repository (the lane's standing fixture discipline)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.setdefault("LC_ALL", "C")
    return env


def run_git(repo, *args, check=True):
    proc = subprocess.run(["git", "-C", repo] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=_git_env())
    if check and proc.returncode != 0:
        raise SetupError("git-%s-failed:%s" % (
            args[0], proc.stderr.decode("utf-8", "replace").strip()[:200]))
    return proc


def blob_bytes(repo, rev, path):
    """The committed bytes of a REGULAR file at `rev`.

    Every kind reads through here, so the type/mode boundary is one gate: a
    doc or receipt that is a directory or a symlink is a setup refusal, never
    silently the tree or the link target (round-82 reviewer D1: three kinds
    called `cat-file blob` directly and were mode-blind).
    """
    entry = tree_entry(repo, rev, path)
    if entry is None:
        raise SetupError("blob-unresolvable:%s:%s" % (rev, path))
    mode, kind = entry
    if kind != "blob" or mode not in REGULAR_MODES:
        raise SetupError("not-regular-file:%s:%s=%s" % (rev, path, mode))
    proc = run_git(repo, "cat-file", "blob", "%s:%s" % (rev, path),
                   check=False)
    if proc.returncode != 0:
        raise SetupError("blob-unresolvable:%s:%s" % (rev, path))
    return proc.stdout


def resolve_rev(repo, rev):
    proc = run_git(repo, "rev-parse", "--verify", "%s^{commit}" % rev,
                   check=False)
    if proc.returncode != 0:
        raise SetupError("rev-unresolvable:%s" % rev)
    return proc.stdout.decode("ascii").strip()


def repo_relative(value, field):
    """Refuse an absolute, drive-qualified or parent-escaping path."""
    if not isinstance(value, str) or not value:
        raise SetupError("invalid-path:%s" % field)
    if "\\" in value:
        raise SetupError("invalid-path:%s:backslash" % field)
    if re.match(r"^[A-Za-z]:", value):
        raise SetupError("invalid-path:%s:drive-qualified" % field)
    if value.startswith("/"):
        raise SetupError("invalid-path:%s:absolute" % field)
    parts = value.split("/")
    if any(p in ("..", "") for p in parts):
        raise SetupError("invalid-path:%s:escape" % field)
    return value


def row_paths(row, field="paths"):
    paths = row.get(field)
    if not isinstance(paths, list) or not paths:
        raise SetupError("empty-%s:%s" % (field, row.get("id")))
    return [repo_relative(p, field) for p in paths]


def row_tokens(row):
    tokens = row.get("tokens")
    if not isinstance(tokens, list) or not tokens:
        raise SetupError("empty-tokens:%s" % row.get("id"))
    if any(not isinstance(t, str) or not t for t in tokens):
        raise SetupError("invalid-token:%s" % row.get("id"))
    return tokens


def tree_entry(repo, rev, path):
    """Return (mode, type) for `path` at `rev`, or None when absent.

    Presence alone is not identity: `git cat-file -e REV:PATH` accepts a tree
    and a symlink as readily as a file (round-81 reviewer), so the row kinds
    that mean "a regular file is committed here" read the entry's mode and
    type from `git ls-tree -z` (S305's listing form; S291's mode field, where
    only 0755/0644 are regular files and symlinks are a distinct type).
    """
    proc = run_git(repo, "ls-tree", "-z", rev, "--", path, check=False)
    if proc.returncode != 0:
        raise SetupError("ls-tree-failed:%s:%s" % (rev, path))
    for record in proc.stdout.split(b"\x00"):
        if not record:
            continue
        meta, _, name = record.partition(b"\t")
        fields = meta.split(b" ")
        if len(fields) < 3:
            continue
        if name.decode("utf-8", "replace") == path:
            return fields[0].decode("ascii"), fields[1].decode("ascii")
    return None


def regular_file_state(repo, rev, path):
    """None when `path` is a regular blob at `rev`; else a state token."""
    entry = tree_entry(repo, rev, path)
    if entry is None:
        return "missing"
    mode, kind = entry
    if kind != "blob" or mode not in REGULAR_MODES:
        return "not-regular-file:%s=%s" % (path, mode)
    return None


def check_tree_paths(repo, rev, row):
    missing, not_regular = [], []
    for path in row_paths(row):
        state = regular_file_state(repo, rev, path)
        if state == "missing":
            missing.append(path)
        elif state is not None:
            not_regular.append(state)
    detail = []
    if missing:
        detail.append("missing:" + ",".join(missing))
    if not_regular:
        detail.append(",".join(not_regular))
    if detail:
        return "open", ";".join(detail)
    return "closed", "paths-present"


def check_tree_bytes(repo, rev, row):
    minimum = row.get("min_bytes")
    if not isinstance(minimum, int) or minimum < 0:
        raise SetupError("invalid-min-bytes:%s" % row.get("id"))
    short, wrong_kind = [], []
    for path in row_paths(row):
        state = regular_file_state(repo, rev, path)
        if state == "missing":
            # the round-81 contract: an unresolvable blob is a setup refusal,
            # never a verdict
            raise SetupError("blob-unresolvable:%s:%s" % (rev, path))
        if state is not None:
            wrong_kind.append(state)
            continue
        size = len(blob_bytes(repo, rev, path))
        if size < minimum:
            short.append("%s=%d<%d" % (path, size, minimum))
    if wrong_kind:
        return "open", ",".join(wrong_kind)
    if short:
        return "open", "short:" + ",".join(short)
    return "closed", "min-bytes-met"


def check_receipt_tokens(repo, rev, row):
    span = row.get("span")
    if not isinstance(span, str) or not span:
        raise SetupError("empty-span:%s" % row.get("id"))
    doc = repo_relative(row.get("doc"), "doc")
    receipt = repo_relative(row.get("receipt"), "receipt")
    doc_bytes = blob_bytes(repo, rev, doc)
    receipt_bytes = blob_bytes(repo, rev, receipt)
    span_bytes = span.encode("utf-8")
    if span_bytes not in doc_bytes:
        return "open", "span-absent:%s" % doc
    missing_span = [t for t in row_tokens(row)
                    if t.encode("utf-8") not in span_bytes]
    if missing_span:
        return "open", "token-absent-in-span:" + ",".join(missing_span)
    missing = [t for t in row_tokens(row)
               if t.encode("utf-8") not in receipt_bytes]
    if missing:
        return "open", "token-absent-in-receipt:" + ",".join(missing)
    return "closed", "tokens-in-span-and-receipt"


def _sources_cell(text, source_id):
    pattern = re.compile(r"^ {0,3}\|[ \t]*%s[ \t]*\|" % re.escape(source_id),
                         re.M)
    match = pattern.search(text)
    if not match:
        return None
    line_end = text.find("\n", match.start())
    if line_end < 0:
        line_end = len(text)
    line = text[match.start():line_end]
    cells = [c.strip() for c in line.split("|")]
    # leading empty cell from the leading pipe; last non-empty is used-by
    while cells and cells[-1] == "":
        cells.pop()
    if len(cells) < 3:
        return None
    return cells[-1]


def check_sources_cell(repo, rev, row):
    source_id = row.get("id_ref") or row.get("source_id")
    if not isinstance(source_id, str) or not re.match(r"^S[0-9]{3,}$",
                                                      source_id):
        raise SetupError("invalid-source-id:%s" % row.get("id"))
    text = blob_bytes(repo, rev, SOURCES_PATH).decode("utf-8")
    cell = _sources_cell(text, source_id)
    if cell is None:
        return "open", "row-absent:%s" % source_id
    missing = [t for t in row_tokens(row) if t not in cell]
    if missing:
        return "open", "cell-absent:" + ",".join(missing)
    return "closed", "cell-carries"


def _section(text, heading):
    lines = text.split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading.strip():
            start = i + 1
            break
    if start is None:
        return None
    out = []
    for line in lines[start:]:
        stripped = line.lstrip("#")
        if line.startswith("#") and len(line) - len(stripped) <= level:
            break
        out.append(line)
    return "\n".join(out)


def check_doc_contains(repo, rev, row):
    doc = repo_relative(row.get("doc"), "doc")
    section = row.get("section")
    if not isinstance(section, str) or not section.startswith("## "):
        raise SetupError("invalid-section:%s" % row.get("id"))
    text = blob_bytes(repo, rev, doc).decode("utf-8")
    body = _section(text, section)
    if body is None:
        return "open", "section-absent:%s" % section
    missing = [t for t in row_tokens(row) if t not in body]
    if missing:
        return "open", "section-token-absent:" + ",".join(missing)
    return "closed", "section-carries"


CHECKERS = {
    "tree-paths": check_tree_paths,
    "tree-bytes": check_tree_bytes,
    "receipt-tokens": check_receipt_tokens,
    "sources-cell": check_sources_cell,
    "doc-contains": check_doc_contains,
}

REQUIRED = ("id", "kind")


def load_manifest(path):
    try:
        raw = open(path, "rb").read()
        man = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        raise SetupError("manifest-unreadable:%s" % exc)
    if not isinstance(man, dict) or man.get("schema") != SCHEMA:
        raise SetupError("manifest-schema:%r" % (man.get("schema")
                                                 if isinstance(man, dict)
                                                 else type(man).__name__))
    rows = man.get("rows")
    if not isinstance(rows, list) or not rows:
        raise SetupError("manifest-empty")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise SetupError("row-not-object")
        for key in REQUIRED:
            if key not in row:
                raise SetupError("row-missing-%s" % key)
        if row["kind"] not in CHECKERS:
            raise SetupError("unknown-kind:%s" % row["kind"])
        if row["id"] in seen:
            raise SetupError("duplicate-id:%s" % row["id"])
        seen.add(row["id"])
        expect = row.get("expect", "closed")
        if expect not in ("closed", "open"):
            raise SetupError("invalid-expect:%s" % row["id"])
        if not isinstance(row.get("rev"), str) or not row["rev"]:
            raise SetupError("row-missing-rev:%s" % row["id"])
        _validate_payload(row)
    return rows


def _validate_payload(row):
    """Refuse a malformed row payload BEFORE any row effect (a refusal is
    setup exit 2, never a row verdict)."""
    kind = row["kind"]
    if kind in ("tree-paths", "tree-bytes"):
        row_paths(row)
        if kind == "tree-bytes":
            minimum = row.get("min_bytes")
            if not isinstance(minimum, int) or minimum < 0:
                raise SetupError("invalid-min-bytes:%s" % row["id"])
        return
    if kind == "receipt-tokens":
        repo_relative(row.get("doc"), "doc")
        repo_relative(row.get("receipt"), "receipt")
        span = row.get("span")
        if not isinstance(span, str) or not span:
            raise SetupError("empty-span:%s" % row["id"])
        row_tokens(row)
        return
    if kind == "sources-cell":
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not re.match(r"^S[0-9]{3,}$",
                                                          source_id):
            raise SetupError("invalid-source-id:%s" % row["id"])
        row_tokens(row)
        return
    if kind == "doc-contains":
        repo_relative(row.get("doc"), "doc")
        section = row.get("section")
        if not isinstance(section, str) or not section.startswith("## "):
            raise SetupError("invalid-section:%s" % row["id"])
        row_tokens(row)
        return
    raise SetupError("unknown-kind:%s" % kind)


def bind_manifest(repo, manifest_path, rev):
    """Refuse a manifest whose bytes are not the blob committed at `rev`.

    A sweep's denominator is its manifest; read from a path, a caller can
    delete a row or relax an `expect` and every remaining row still measures
    green (the round-81 carried defect D-CN3). S103: the object id names the
    bytes, not the path; S289 reads them. The declared limit is S311: on a
    path carrying `text`/`eol`/filter attributes the worktree bytes may
    legitimately differ from the blob.
    """
    path = manifest_path
    if os.path.isabs(path):
        try:
            path = os.path.relpath(os.path.realpath(path),
                                   os.path.realpath(repo))
        except ValueError as exc:
            raise SetupError("invalid-path:manifest:%s" % exc)
        if path == ".." or path.startswith(".." + os.sep):
            raise SetupError("invalid-path:manifest:escaping-repo")
        path = path.replace(os.sep, "/")
    path = repo_relative(path, "manifest")
    resolved = resolve_rev(repo, rev)
    proc = run_git(repo, "cat-file", "blob", "%s:%s" % (resolved, path),
                   check=False)
    if proc.returncode != 0:
        raise SetupError("manifest-rev-unreadable:%s:%s" % (rev, path))
    try:
        with open(manifest_path, "rb") as fh:
            disk = fh.read()
    except OSError as exc:
        raise SetupError("manifest-unreadable:%s" % exc)
    if disk != proc.stdout:
        raise SetupError("manifest-rev-mismatch:%s:%s" % (rev, path))
    return resolved


def sweep(repo, manifest_path, out=sys.stdout, manifest_rev=None):
    """Measure every declared row; each row reads its own `rev` (never a
    caller-supplied default, so a caller cannot silently re-point the whole
    population at a different revision than the one it declared)."""
    bound = None
    if manifest_rev:
        bound = bind_manifest(repo, manifest_path, manifest_rev)
    rows = load_manifest(manifest_path)
    resolved = {}
    for row in rows:
        key = row["rev"]
        if key not in resolved:
            resolved[key] = resolve_rev(repo, key)
    counts = {"closed": 0, "open": 0, "unexpected": 0}
    for row in rows:
        state, detail = CHECKERS[row["kind"]](repo, resolved[row["rev"]], row)
        expect = row.get("expect", "closed")
        counts[state] += 1
        mismatch = state != expect
        if mismatch:
            counts["unexpected"] += 1
        out.write("DEFECT_BIND_ROW %s kind=%s expect=%s state=%s detail=%s\n"
                  % (row["id"], row["kind"], expect, state,
                     detail.replace(" ", "_")))
    out.write("DEFECT_BIND: rows=%d closed=%d open=%d unexpected=%d "
              "manifest=%s\n"
              % (len(rows), counts["closed"], counts["open"],
                 counts["unexpected"], "bound" if bound else "unbound"))
    return 0 if counts["unexpected"] == 0 else 1


# --------------------------------------------------------------- selftest

DOC = (
    "# record\n"
    "\n"
    "The before row reads ALPHA 24/24 and BETA 17/17.\n"
    "\n"
    "## Search log\n"
    "\n"
    "- Round 80: the source work is recorded here.\n"
    "\n"
    "## Other\n"
    "\n"
    "- Round 81: a token that lives in a different section.\n"
)
RECEIPT = (
    "REGISTRY_BIND: live 24/24\n"
    "SELFSTATE: live 17/17\n"
)
SOURCES = (
    "| id | source | kind | tier | scope | anchor | teaches | status | "
    "opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
    "| S289 | toy | docs | A | scope | anchor | teaches | mined | "
    "2026-10-30 | 180d | corpus/lessons/round-61.md |\n"
)


def _fixture_env():
    return _git_env()


class Fixture:
    def __init__(self, root):
        self.root = root
        self.rev1 = None
        self.rev2 = None

    def git(self, *args):
        subprocess.run(["git", "-C", self.root] + list(args), check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=_fixture_env())

    def put(self, rel, text):
        path = os.path.join(self.root, rel)
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", newline="\n") as fh:
            fh.write(text)

    def build(self):
        self.git("init", "-q")
        top = subprocess.run(["git", "-C", self.root, "rev-parse",
                              "--show-toplevel"], check=True,
                             stdout=subprocess.PIPE,
                             env=_fixture_env()).stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(self.root):
            raise SetupError("git-fixture-misroot:%s" % top)
        self.put("doc.md", DOC)
        self.put("receipt.txt", RECEIPT)
        self.put(SOURCES_PATH, SOURCES)
        self.put("tools/toy.py", "print('rev1')\n")
        self.put("big.txt", "x" * 64 + "\n")
        self.put("sub/inner.txt", "inner\n")
        link = os.path.join(self.root, "link.txt")
        if not os.path.lexists(link):
            os.symlink("doc.md", link)
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit",
                 "-qm", "rev1")
        self.rev1 = self._head()
        self.put("tools/toy.py", "print('rev2')\n")
        self.put("late.txt", "only at rev2\n")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit",
                 "-qm", "rev2")
        self.rev2 = self._head()

    def _head(self):
        return subprocess.run(["git", "-C", self.root, "rev-parse", "HEAD"],
                              check=True, stdout=subprocess.PIPE,
                              env=_fixture_env()).stdout.decode().strip()

    def manifest(self, rows, name="m.json"):
        path = os.path.join(self.root, name)
        with open(path, "w", newline="\n") as fh:
            json.dump({"schema": SCHEMA, "rows": rows}, fh)
        return path

    def run(self, rows):
        path = self.manifest(rows)
        import io
        buf = io.StringIO()
        code = sweep(self.root, path, out=buf)
        return code, buf.getvalue()


def _expect_setup(fn, prefix):
    try:
        fn()
    except SetupError as exc:
        return str(exc).startswith(prefix) or prefix in str(exc)
    return False


def selftest(out=sys.stdout):
    passed = 0
    total = 0

    def arm(name, ok, detail=""):
        nonlocal passed, total
        total += 1
        if ok:
            passed += 1
        out.write("ARM %s %s%s\n" % ("PASS" if ok else "FAIL", name,
                                     (" [" + detail + "]") if detail else ""))

    fx = tempfile.mkdtemp(prefix="defect-bind-",
                          dir=os.environ.get("TMPDIR") or None)
    try:
        f = Fixture(fx)
        f.build()
        base = f.rev1

        # arm 1: tree-paths closed when every path is in the tree.
        code, text = f.run([{"id": "t1", "kind": "tree-paths", "rev": base,
                             "paths": ["doc.md", "tools/toy.py"]}])
        arm("A1_tree_paths_closed", code == 0
            and "DEFECT_BIND: rows=1 closed=1 open=0 unexpected=0" in text,
            text.strip().splitlines()[-1])

        # arm 2: tree-paths open when a path exists only at a later rev.
        code, text = f.run([{"id": "t2", "kind": "tree-paths", "rev": base,
                             "paths": ["late.txt"]}])
        arm("A2_tree_paths_open", code == 1
            and "state=open" in text and "missing:late.txt" in text, "")

        # arm 3: tree-bytes measures an empty committed blob as open.
        f.put("empty.txt", "")
        f.git("-c", "user.name=t", "-c", "user.email=t@t", "add", "empty.txt")
        f.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm",
              "empty")
        rev3 = f._head()
        code, text = f.run([{"id": "t3", "kind": "tree-bytes", "rev": rev3,
                             "paths": ["empty.txt"], "min_bytes": 1}])
        ok_empty = code == 1 and "short:empty.txt=0<1" in text
        code2, text2 = f.run([{"id": "t3b", "kind": "tree-bytes", "rev": rev3,
                               "paths": ["big.txt"], "min_bytes": 1}])
        arm("A3_tree_bytes_min", ok_empty and code2 == 0, text.strip())

        # arm 4: receipt-tokens closed, then open on a token the receipt
        # does not carry (the red arm the instrument exists for).
        row = {"id": "t4", "kind": "receipt-tokens", "rev": rev3,
               "doc": "doc.md",
               "span": "The before row reads ALPHA 24/24 and BETA 17/17.",
               "receipt": "receipt.txt", "tokens": ["24/24", "17/17"]}
        code_ok, _ = f.run([row])
        # the receipt half is exercised with a token the span carries and the
        # receipt does not; the span half with a span that carries neither.
        row_bad = dict(row, id="t4b", tokens=["ALPHA"])
        code_bad, text_bad = f.run([row_bad])
        row_span = dict(row, id="t4c", span="a span the doc does not carry")
        code_span, text_span = f.run([row_span])
        row_nospan = dict(row, id="t4d",
                          span="The before row reads")
        code_nospan, text_nospan = f.run([row_nospan])
        arm("A4_receipt_tokens", code_ok == 0 and code_bad == 1
            and "token-absent-in-receipt:ALPHA" in text_bad
            and code_span == 1 and "span-absent" in text_span
            and code_nospan == 1
            and "token-absent-in-span:24/24,17/17" in text_nospan, "")

        # arm 5: sources-cell reads the used-by cell of the named row.
        row = {"id": "t5", "kind": "sources-cell", "rev": rev3,
               "source_id": "S289", "tokens": ["round-61.md"]}
        code_ok, _ = f.run([row])
        row_bad = dict(row, id="t5b", tokens=["round-80.md"])
        code_bad, text_bad = f.run([row_bad])
        row_absent = dict(row, id="t5c", source_id="S999")
        code_absent, text_absent = f.run([row_absent])
        arm("A5_sources_cell", code_ok == 0 and code_bad == 1
            and "cell-absent:round-80.md" in text_bad and code_absent == 1
            and "row-absent:S999" in text_absent, "")

        # arm 6: doc-contains is section-scoped: a token in another section
        # does not count.
        row = {"id": "t6", "kind": "doc-contains", "rev": rev3,
               "doc": "doc.md", "section": "## Search log",
               "tokens": ["Round 80"]}
        code_ok, _ = f.run([row])
        row_bad = dict(row, id="t6b", tokens=["Round 81"])
        code_bad, text_bad = f.run([row_bad])
        res = f.run([dict(row, id="t6c", section="## Missing")])
        arm("A6_doc_contains_section", code_ok == 0 and code_bad == 1
            and "section-token-absent:Round_81" in text_bad and res[0] == 1
            and "section-absent" in res[1], "")

        # arm 7: expect=open is a standing red arm: it MEETS when open and
        # fails when closed.
        row = {"id": "t7", "kind": "tree-paths", "rev": base,
               "paths": ["late.txt"], "expect": "open"}
        code_meet, text_meet = f.run([row])
        row_closed = dict(row, id="t7b", paths=["doc.md"])
        code_fail, text_fail = f.run([row_closed])
        arm("A7_expect_open_standing_arm", code_meet == 0 and code_fail == 1
            and "unexpected=1" in text_fail, text_meet.strip().splitlines()[-1])

        # arm 8: refusals are setup exit 2, never a row verdict.
        arm("A8_refusals", all([
            _expect_setup(lambda: load_manifest(
                os.path.join(f.root, "nope.json")), "manifest-unreadable"),
            _expect_setup(lambda: f.run([]), "manifest-empty"),
            _expect_setup(lambda: f.run([
                {"id": "x", "kind": "nope", "rev": base}]), "unknown-kind"),
            _expect_setup(lambda: f.run([
                {"id": "d", "kind": "tree-paths", "rev": base,
                 "paths": ["doc.md"]},
                {"id": "d", "kind": "tree-paths", "rev": base,
                 "paths": ["doc.md"]}]), "duplicate-id"),
            _expect_setup(lambda: f.run([
                {"id": "p", "kind": "tree-paths", "rev": base,
                 "paths": ["../escape"]}]), "invalid-path"),
            _expect_setup(lambda: f.run([
                {"id": "p", "kind": "tree-paths", "rev": base,
                 "paths": ["/abs"]}]), "invalid-path"),
            _expect_setup(lambda: f.run([
                {"id": "p", "kind": "tree-paths", "rev": base,
                 "paths": ["C:/abs"]}]), "invalid-path"),
            _expect_setup(lambda: f.run([
                {"id": "r", "kind": "tree-paths", "rev": "deadbeef",
                 "paths": ["doc.md"]}]), "rev-unresolvable"),
            _expect_setup(lambda: f.run([
                {"id": "e", "kind": "receipt-tokens", "rev": base,
                 "doc": "doc.md", "span": "x", "receipt": "receipt.txt",
                 "tokens": []}]), "empty-tokens"),
            _expect_setup(lambda: f.run([
                {"id": "e", "kind": "receipt-tokens", "rev": base,
                 "doc": "doc.md", "span": "", "receipt": "receipt.txt",
                 "tokens": ["x"]}]), "empty-span"),
            _expect_setup(lambda: f.run([
                {"id": "s", "kind": "sources-cell", "rev": base,
                 "source_id": "bad", "tokens": ["x"]}]), "invalid-source-id"),
            _expect_setup(lambda: load_manifest(_bad_schema(f)), "schema"),
            _expect_setup(lambda: load_manifest(_bad_json(f)),
                          "manifest-unreadable"),
        ]) and _cli_guards(f, base), "")

        # arm 9: a row missing its required key is refused.
        arm("A9_missing_rev_refused",
            _expect_setup(lambda: f.run([{"id": "m", "kind": "tree-paths",
                                          "paths": ["doc.md"]}]),
                          "row-missing-rev"), "")

        # arm 10: the summary counts every row, and a multi-row sweep with
        # one expected-open row is exit 0 (no vacuous pass on an empty set
        # is A8's manifest-empty).
        code, text = f.run([
            {"id": "a", "kind": "tree-paths", "rev": base,
             "paths": ["doc.md"]},
            {"id": "b", "kind": "tree-paths", "rev": base,
             "paths": ["late.txt"], "expect": "open"},
        ])
        arm("A10_multi_row_summary", code == 0
            and "DEFECT_BIND: rows=2 closed=1 open=1 unexpected=0" in text, "")

        # arm 11: a blob path that exists only at another rev is a SETUP
        # refusal for tree-bytes (an unresolvable input is not a verdict).
        arm("A11_tree_bytes_unresolvable",
            _expect_setup(lambda: f.run([
                {"id": "u", "kind": "tree-bytes", "rev": base,
                 "paths": ["late.txt"], "min_bytes": 1}]), "blob-unresolvable"),
            "")

        # arm 12: a path row reads the object's TYPE and MODE. A directory and
        # a symlink are not the regular file a row means (round-81 reviewer
        # D1a/D5 + executor cheat register: `cat-file -e` accepts both; a
        # symlink's target string satisfies a mode-blind min_bytes).
        code_dir, text_dir = f.run([{"id": "r1", "kind": "tree-paths",
                                     "rev": rev3, "paths": ["sub"]}])
        code_link, text_link = f.run([{"id": "r2", "kind": "tree-paths",
                                       "rev": rev3, "paths": ["link.txt"]}])
        code_link_bytes, text_link_bytes = f.run([
            {"id": "r3", "kind": "tree-bytes", "rev": rev3,
             "paths": ["link.txt"], "min_bytes": 1}])
        code_regular, _ = f.run([{"id": "r4", "kind": "tree-bytes",
                                  "rev": rev3, "paths": ["doc.md"],
                                  "min_bytes": 1}])
        link_doc_refused = _expect_setup(
            lambda: f.run([{"id": "r5", "kind": "receipt-tokens", "rev": rev3,
                            "doc": "link.txt", "span": "x",
                            "receipt": "receipt.txt", "tokens": ["x"]}]),
            "not-regular-file")
        code_symlink_bytes, text_symlink_bytes = f.run([
            {"id": "r6", "kind": "tree-bytes", "rev": rev3,
             "paths": ["link.txt"], "min_bytes": 1}])
        arm("A12_regular_file_boundary",
            code_dir == 1 and "not-regular-file:sub=040000" in text_dir
            and code_link == 1
            and "not-regular-file:link.txt=120000" in text_link
            and code_link_bytes == 1
            and "not-regular-file:link.txt=120000" in text_link_bytes
            and code_regular == 0 and link_doc_refused
            and code_symlink_bytes == 1
            and "not-regular-file:link.txt=120000" in text_symlink_bytes,
            text_dir.strip().splitlines()[-1])

        # arm 13: the manifest is bound to the bytes committed at a declared
        # revision. A narrowed manifest measures green UNBOUND, and is
        # refused BOUND — that is the whole difference the flag buys.
        import io as _io
        wide = [{"id": "b1", "kind": "tree-paths", "rev": rev3,
                 "paths": ["doc.md"]},
                {"id": "b2", "kind": "tree-paths", "rev": rev3,
                 "paths": ["absent-here.txt"], "expect": "open"}]
        mpath = f.manifest(wide, name="bound.json")
        f.git("-c", "user.name=t", "-c", "user.email=t@t", "add", "bound.json")
        f.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm",
              "bound manifest")
        rev4 = f._head()
        probe = _io.StringIO()
        code_before = sweep(f.root, mpath, out=probe)
        bound_text = probe.getvalue()
        probe = _io.StringIO()
        code_bound = sweep(f.root, mpath, out=probe, manifest_rev=rev4)
        bound_tokens = "manifest=bound" in probe.getvalue()
        # the cheat: delete one row from the same path, keep the declared rev
        f.manifest([wide[0]], name="bound.json")
        narrowed_refused = _expect_setup(
            lambda: sweep(f.root, mpath, out=_io.StringIO(),
                          manifest_rev=rev4), "manifest-rev-mismatch")
        probe = _io.StringIO()
        code_narrowed = sweep(f.root, mpath, out=probe)
        narrowed_unbound = "manifest=unbound" in probe.getvalue()
        outside_refused = _expect_setup(
            lambda: sweep(f.root, os.path.join(f.root, "..", "outside.json"),
                          out=_io.StringIO(), manifest_rev=rev4),
            "escaping-repo")
        absent_refused = _expect_setup(
            lambda: sweep(f.root, "no-such-manifest.json",
                          out=_io.StringIO(), manifest_rev=rev4),
            "manifest-rev-unreadable")
        unresolvable_refused = _expect_setup(
            lambda: sweep(f.root, mpath, out=_io.StringIO(),
                          manifest_rev="deadbeef"), "rev-unresolvable")
        noncommit_refused = _expect_setup(
            lambda: sweep(f.root, mpath, out=_io.StringIO(),
                          manifest_rev=rev4 + "^{tree}"), "rev-unresolvable")
        arm("A13_manifest_rev_binding",
            code_before == 0 and bound_tokens and code_bound == 0
            and narrowed_refused and narrowed_unbound and outside_refused
            and absent_refused and unresolvable_refused and noncommit_refused,
            bound_text.strip().splitlines()[-1])

        # arm 14: the selftest's own assertion text is pinned, so an edit that
        # weakens an arm (keeping its name and fixtures) fails THIS arm
        # instead of passing vacuously (round-81 mutation-tester's named gap:
        # the round's newest instrument carried no text pin).
        try:
            self_text = inspect.getsource(selftest)
            measured = hashlib.sha256(self_text.encode("utf-8")).hexdigest()
            arm("A14_selftest_text_pin", measured == SELFTEST_TEXT_SHA256,
                "measured=%s pinned=%s" % (measured[:12],
                                           SELFTEST_TEXT_SHA256[:12]))
        except OSError as exc:
            arm("A14_selftest_text_pin", False, "source-unreadable:%s" % exc)
    finally:
        shutil.rmtree(fx, ignore_errors=True)

    out.write("DEFECT_BIND_SELFTEST: %d/%d pass\n" % (passed, total))
    return 0 if (passed == total == SELFTEST_ARMS) else 1


def _cli_guards(fixture, rev):
    """Drive main() itself: every arm above calls sweep()/load_manifest()
    directly, so the CLI guards were outside the suite's reach (round-82
    mutation-tester survivors r2/r3)."""
    err = io.StringIO()
    out = io.StringIO()
    path = fixture.manifest([{"id": "g1", "kind": "tree-paths", "rev": rev,
                              "paths": ["doc.md"]}], name="guard.json")
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        empty_rev = main(["--repo", fixture.root, "--manifest", path,
                          "--manifest-rev", ""])
        no_manifest = main(["--repo", fixture.root])
    return (empty_rev == 2 and "needs a revision" in err.getvalue()
            and no_manifest == 2)


def _bad_schema(f):
    path = os.path.join(f.root, "bad-schema.json")
    with open(path, "w", newline="\n") as fh:
        json.dump({"schema": "other", "rows": [
            {"id": "x", "kind": "tree-paths", "rev": f.rev1,
             "paths": ["doc.md"]}]}, fh)
    return path


def _bad_json(f):
    path = os.path.join(f.root, "bad.json")
    with open(path, "w", newline="\n") as fh:
        fh.write("{not json")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--manifest")
    ap.add_argument("--manifest-rev")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.selftest:
            return selftest()
        if not args.manifest:
            sys.stderr.write("defect-bind: --manifest is required\n")
            return 2
        if args.manifest_rev is not None and not args.manifest_rev:
            sys.stderr.write("defect-bind: --manifest-rev needs a revision\n")
            return 2
        return sweep(args.repo, args.manifest, manifest_rev=args.manifest_rev)
    except SetupError as exc:
        sys.stderr.write("defect-bind: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
