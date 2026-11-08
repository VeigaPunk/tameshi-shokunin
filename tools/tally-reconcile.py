#!/usr/bin/env python3
"""tally-reconcile — reconcile every recorded selftest tally with the receipt its line cites.

Round 99 (tameshi). Mines `considerthese/2026-11-08.md` idea 1 (frozen-tally reconciler).
Two non-author closures found the same class by eye: round 94's frozen
`DISPOSITION_SELFTEST: 8/8 pass` beside a receipt printing `9/9`
(`corpus/lessons/round-94.md:66`), and round 98's report "Selftest `18/18`
(`pre-freeze/c1-audit-selftest.out` at the freeze ...)" whose receipt prints `12/12`
(round-98 spot-check D2). QUALITY 169 states the rule (a frozen tally cites its receipt);
this tool makes it a count.

Grammar (declared, not inferred):

  token tally     `TOKEN: N/M pass`, TOKEN = `[A-Z][A-Z0-9_]{2,}`.
  selftest tally  the word `selftest` (any case) followed within 12 non-digit characters
                  by `N/M`, on a span no token tally covers.
  citation        a path on the same line ending `.out`, `.txt`, `.log` or `.json`
                  (`[A-Za-z0-9_./-]+`) where the suffix ends the path (`a.out.bak` is not a
                  citation; a sentence-ending `.` is allowed), not within 12 characters
                  after a `://` or anywhere after an `http(s)://` on the line, and not the
                  record itself. A scheme-less host path (`www.h.example/a.out`) IS cited
                  as a path and grades `unbound unresolved` (round-99 A4, declared).

Resolution of a citation, against the tree at --rev only (never the worktree): the path
itself if it is a blob in the tree; otherwise `<root>/<path>` for each receipt root — the
explicit `--receipt-root` values plus, when the record's file name carries `round-NN`,
`.ufo/evidence/round-NN` and `.ufo/waves/round-NN`. No match -> unbound `unresolved`;
more than one -> unbound `ambiguous-path`.

Grading of one (tally, citation) pair, reading the receipt blob at --rev:

  token tally     the receipt's lines `TOKEN: n/m` with the same TOKEN, whatever follows
                  (`pass`, `fail`, nothing; round-99 A2); none -> unbound `token-absent`;
                  every observed n/m equal to the claim -> matched; otherwise mismatched.
  selftest tally  the receipt's `*_SELFTEST: n/m` lines (any suffix); none -> unbound
                  `no-selftest-line`; more than one distinct token -> unbound
                  `ambiguous-selftest`; else as above.

A tally on a line with no citation is `uncited` (counted, never graded).

Usage:
  python3 -I tools/tally-reconcile.py --repo LANE --rev <40 hex> --record PATH [--record PATH ...]
        [--receipt-root DIR ...]
  python3 -I tools/tally-reconcile.py --selftest

Output: one `TALLY <verdict> <record>:<line> <form> <token> claimed=N/M receipt=<path|-> observed=<n/m|-> detail=<d>`
line per pair, then
`TALLY_RECONCILE records=R tallies=T pairs=P matched=M mismatched=X unbound=U uncited=C`.

Exit: 0 no mismatched and no unbound pair; 1 otherwise; 2 setup (repo not a git top level,
rev not 40 hex or not a commit, record absent at rev, receipt root not a tree at rev);
64 usage.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

GIT = "/usr/bin/git"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
TOKEN_RE = re.compile(r"\b([A-Z][A-Z0-9_]{2,}):\s+(\d+)/(\d+)\s+pass\b")
SELFTEST_RE = re.compile(r"(?i)\bselftest\b[^0-9\n]{0,12}?(\d+)/(\d+)\b")
# Round-99 A3 (R99R1 F3): the suffix must end the path — `a.out.bak` is not a citation of
# `a.out`; a sentence-ending period after the suffix is allowed.
CITE_RE = re.compile(r"[A-Za-z0-9_./-]+\.(?:out|txt|log|json)(?!\.?[A-Za-z0-9_/-])")
# Round-99 A2 (R99R1 F1): a receipt line carrying the token is graded whatever follows N/M
# (`pass`, `fail`, nothing), so a contradicting `TOKEN: 9/9 fail` line is not invisible.
RECEIPT_TOKEN_RE = re.compile(r"\b([A-Z][A-Z0-9_]{2,}):\s+(\d+)/(\d+)")
RECEIPT_SELFTEST_RE = re.compile(r"\b([A-Z][A-Z0-9_]*_SELFTEST):\s+(\d+)/(\d+)")
ROUND_RE = re.compile(r"round-(\d+)")


class Setup(Exception):
    pass


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(repo, *args):
    try:
        p = subprocess.run([GIT, "-C", repo] + list(args), capture_output=True, env=sealed_env(),
                           timeout=120)
    except subprocess.TimeoutExpired:
        raise Setup("git-timeout")
    return p.returncode, p.stdout


class Tree:
    def __init__(self, repo, rev):
        if not repo or not os.path.isdir(repo):
            raise Setup("repo-absent")
        rc, out = git(repo, "rev-parse", "--show-toplevel")
        if rc != 0 or os.path.realpath(out.decode().strip()) != os.path.realpath(repo):
            raise Setup("repo-not-toplevel")
        if not HEX40.match(rev or ""):
            raise Setup("rev-not-40-hex")
        rc, out = git(repo, "cat-file", "-t", rev)
        if rc != 0 or out.decode().strip() != "commit":
            raise Setup("rev-not-commit")
        rc, out = git(repo, "ls-tree", "-r", "-z", "--name-only", rev)
        if rc != 0:
            raise Setup("ls-tree-failed")
        self.repo, self.rev = repo, rev
        self._cache = {}
        self.blobs = set(x for x in out.decode("utf-8", "surrogateescape").split("\0") if x)
        self.dirs = set()
        for b in self.blobs:
            parts = b.split("/")
            for i in range(1, len(parts)):
                self.dirs.add("/".join(parts[:i]))

    def read(self, path):
        # Round-99 A9 (R99SN1 F3/F4): a blob that is not UTF-8 is refused (a byte inside the
        # N/M digits must not hide a contradicting line); each blob is read once.
        if path in self._cache:
            return self._cache[path]
        rc, out = git(self.repo, "cat-file", "blob", "%s:%s" % (self.rev, path))
        if rc != 0:
            raise Setup("blob-unreadable:%s" % path)
        try:
            text = out.decode("utf-8")
        except UnicodeDecodeError:
            raise Setup("blob-not-utf8:%s" % path)
        self._cache[path] = text
        return text


def norm(p):
    p = p.strip("/")
    while p.startswith("./"):
        p = p[2:]
    return p


def find_tallies(line):
    out = []
    spans = []
    for m in TOKEN_RE.finditer(line):
        out.append(("token", m.group(1), int(m.group(2)), int(m.group(3))))
        spans.append(m.span())
    for m in SELFTEST_RE.finditer(line):
        s, e = m.span(1)[0], m.span(2)[1]
        if any(a <= s < b or a < e <= b for a, b in spans):
            continue
        out.append(("selftest", "-", int(m.group(1)), int(m.group(2))))
    return out


def find_citations(line, record):
    cites = []
    for m in CITE_RE.finditer(line):
        start = m.start()
        if "://" in line[max(0, start - 12):start + 3] or line[max(0, start - 3):start].endswith("://"):
            continue
        prefix = line[:start]
        if re.search(r"https?://\S*$", prefix):
            continue
        p = m.group(0)
        if p.startswith("/"):
            cites.append(p)
            continue
        p2 = norm(p)
        if p2 and p2 != record and p2 not in cites:
            cites.append(p2)
    return cites


def resolve(tree, cite, roots):
    if cite.startswith("/"):
        return None, "unresolved"
    if cite in tree.blobs:
        return cite, None
    hits = [r + "/" + cite for r in roots if (r + "/" + cite) in tree.blobs]
    if not hits:
        return None, "unresolved"
    if len(set(hits)) > 1:
        return None, "ambiguous-path"
    return hits[0], None


def grade(form, token, n, m, receipt_text):
    if form == "token":
        obs = [(int(a), int(b)) for t, a, b in RECEIPT_TOKEN_RE.findall(receipt_text) if t == token]
        if not obs:
            return "unbound", "-", "token-absent"
    else:
        rows = RECEIPT_SELFTEST_RE.findall(receipt_text)
        if not rows:
            return "unbound", "-", "no-selftest-line"
        if len(set(t for t, _, _ in rows)) > 1:
            return "unbound", "-", "ambiguous-selftest"
        obs = [(int(a), int(b)) for _, a, b in rows]
    shown = ",".join(sorted(set("%d/%d" % o for o in obs)))
    if all(o == (n, m) for o in obs):
        return "matched", shown, "equal"
    return "mismatched", shown, "differs"


def reconcile(tree, records, extra_roots):
    for r in extra_roots:
        if norm(r) not in tree.dirs:
            raise Setup("receipt-root-not-tree:%s" % r)
    for rec in records:
        if norm(rec) not in tree.blobs:
            raise Setup("record-absent:%s" % rec)
    lines = []
    tallies = pairs = matched = mismatched = unbound = uncited = 0
    for rec in records:
        rec = norm(rec)
        roots = [norm(r) for r in extra_roots]
        mr = ROUND_RE.search(os.path.basename(rec))
        if mr:
            for auto in (".ufo/evidence/round-%s" % mr.group(1), ".ufo/waves/round-%s" % mr.group(1)):
                if auto in tree.dirs and auto not in roots:
                    roots.append(auto)
        for lineno, text in enumerate(tree.read(rec).split("\n"), 1):
            found = find_tallies(text)
            if not found:
                continue
            cites = find_citations(text, rec)
            for form, token, n, m in found:
                tallies += 1
                if not cites:
                    uncited += 1
                    lines.append("TALLY uncited %s:%d %s %s claimed=%d/%d receipt=- observed=- detail=no-citation"
                                 % (rec, lineno, form, token, n, m))
                    continue
                for c in cites:
                    pairs += 1
                    path, why = resolve(tree, c, roots)
                    if path is None:
                        unbound += 1
                        lines.append("TALLY unbound %s:%d %s %s claimed=%d/%d receipt=%s observed=- detail=%s"
                                     % (rec, lineno, form, token, n, m, c, why))
                        continue
                    verdict, obs, det = grade(form, token, n, m, tree.read(path))
                    if verdict == "matched":
                        matched += 1
                    elif verdict == "mismatched":
                        mismatched += 1
                    else:
                        unbound += 1
                    lines.append("TALLY %s %s:%d %s %s claimed=%d/%d receipt=%s observed=%s detail=%s"
                                 % (verdict, rec, lineno, form, token, n, m, path, obs, det))
    lines.append("TALLY_RECONCILE records=%d tallies=%d pairs=%d matched=%d mismatched=%d unbound=%d uncited=%d"
                 % (len(records), tallies, pairs, matched, mismatched, unbound, uncited))
    return lines, (0 if mismatched == 0 and unbound == 0 else 1)


# --- selftest: each case is a fixture repo built under a scratch dir -----------------------

SELFTEST_CASES = [
    # (name, files, records, roots, expected summary fields, expected exit)
    ("token-matched",
     {"plans/round-5.plan.md": "A `X_SELFTEST: 3/3 pass` (`pre/a.out`)\n",
      ".ufo/evidence/round-5/pre/a.out": "X_SELFTEST: 3/3 pass\n"},
     ["plans/round-5.plan.md"], [], {"pairs": 1, "matched": 1}, 0),
    ("token-mismatched-r94-shape",
     {"corpus/lessons/round-7.md": "    -> D_SELFTEST: 8/8 pass, exit 0   (.ufo/evidence/round-7/pre/c.out)\n",
      ".ufo/evidence/round-7/pre/c.out": "D_SELFTEST: 9/9 pass\n"},
     ["corpus/lessons/round-7.md"], [], {"mismatched": 1}, 1),
    ("selftest-word-r98-d2-shape",
     {"r/round-9.md": "Selftest `18/18` (`pre/s.out` at the freeze; `rec/s.out` at R)\n",
      ".ufo/evidence/round-9/pre/s.out": "C_SELFTEST: 12/12 pass\n",
      ".ufo/evidence/round-9/rec/s.out": "C_SELFTEST: 18/18 pass\n"},
     ["r/round-9.md"], [], {"pairs": 2, "matched": 1, "mismatched": 1}, 1),
    ("token-absent",
     {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` (`a.out`)\n", ".ufo/evidence/round-3/a.out": "nothing\n"},
     ["p/round-3.md"], [], {"unbound": 1}, 1),
    ("unresolved-path",
     {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` (`missing.out`)\n", ".ufo/evidence/round-3/a.out": "x\n"},
     ["p/round-3.md"], [], {"unbound": 1}, 1),
    ("ambiguous-path",
     {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` (`a.out`)\n",
      ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 2/2 pass\n", ".ufo/waves/round-3/a.out": "Y_SELFTEST: 2/2 pass\n"},
     ["p/round-3.md"], [], {"unbound": 1}, 1),
    ("uncited-not-graded",
     {"p/round-3.md": "the battery prints `Y_SELFTEST: 2/2 pass`\n", ".ufo/evidence/round-3/a.out": "x\n"},
     ["p/round-3.md"], [], {"tallies": 1, "pairs": 0, "uncited": 1}, 0),
    ("mixed-observed-is-mismatch",
     {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` (`a.out`)\n",
      ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 2/2 pass\nY_SELFTEST: 1/2 pass\n"},
     ["p/round-3.md"], [], {"mismatched": 1}, 1),
    ("ambiguous-selftest",
     {"p/round-3.md": "selftest 2/2 (`a.out`)\n",
      ".ufo/evidence/round-3/a.out": "A_SELFTEST: 2/2 pass\nB_SELFTEST: 2/2 pass\n"},
     ["p/round-3.md"], [], {"unbound": 1}, 1),
    ("url-not-a-citation",
     {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` see https://h.example/x/a.json\n", ".ufo/evidence/round-3/a.json": "x\n"},
     ["p/round-3.md"], [], {"pairs": 0, "uncited": 1}, 0),
    ("explicit-root",
     {"p/notes.md": "`Y_SELFTEST: 2/2 pass` (`a.out`)\n", "ev/a.out": "Y_SELFTEST: 1/2 pass\n"},
     ["p/notes.md"], ["ev"], {"mismatched": 1}, 1),
    ("two-tallies-one-line",
     {"p/round-3.md": "`A_SELFTEST: 2/2 pass` and `B_SELFTEST: 4/4 pass` (`a.out`)\n",
      ".ufo/evidence/round-3/a.out": "A_SELFTEST: 2/2 pass\nB_SELFTEST: 3/4 pass\n"},
     ["p/round-3.md"], [], {"tallies": 2, "pairs": 2, "matched": 1, "mismatched": 1}, 1),
    # round-99 amendment arms (R99R1 F1/F3, R99M1 t4/t9 survivors)
    ("receipt-fail-suffix-is-graded",
     {"p/round-3.md": "`D_SELFTEST: 8/8 pass` (`a.out`)\n",
      ".ufo/evidence/round-3/a.out": "D_SELFTEST: 8/8 pass\nD_SELFTEST: 9/9 fail\n"},
     ["p/round-3.md"], [], {"pairs": 1, "mismatched": 1}, 1),
    ("receipt-no-suffix-is-graded",
     {"p/round-3.md": "selftest 8/8 (`a.out`)\n", ".ufo/evidence/round-3/a.out": "C_SELFTEST: 9/9\n"},
     ["p/round-3.md"], [], {"pairs": 1, "mismatched": 1}, 1),
    ("suffix-must-end-path",
     {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` (`a.out.bak`)\n",
      ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 2/2 pass\n"},
     ["p/round-3.md"], [], {"pairs": 0, "uncited": 1}, 0),
    ("sentence-end-period-cited",
     {"p/round-3.md": "Y_SELFTEST: 2/2 pass, see a.out.\n", ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 1/2 pass\n"},
     ["p/round-3.md"], [], {"pairs": 1, "mismatched": 1}, 1),
    ("selftest-window-13-not-a-tally",
     {"p/round-3.md": "selftest:abcdefghijk 2/2 (`a.out`)\n", ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 1/2 pass\n"},
     ["p/round-3.md"], [], {"tallies": 0, "pairs": 0}, 0),
    ("selftest-window-12-is-a-tally",
     {"p/round-3.md": "selftest:abcdefghij 2/2 (`a.out`)\n", ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 1/2 pass\n"},
     ["p/round-3.md"], [], {"tallies": 1, "mismatched": 1}, 1),
    ("two-char-token-not-a-tally",
     {"p/round-3.md": "`AB: 2/2 pass` (`a.out`)\n", ".ufo/evidence/round-3/a.out": "AB: 1/2 pass\n"},
     ["p/round-3.md"], [], {"tallies": 0}, 0),
]


def build_fixture(base, files):
    d = tempfile.mkdtemp(dir=base)
    env = sealed_env()
    env.update({"GIT_AUTHOR_NAME": "fx", "GIT_AUTHOR_EMAIL": "fx@fixture.invalid",
                "GIT_COMMITTER_NAME": "fx", "GIT_COMMITTER_EMAIL": "fx@fixture.invalid"})
    subprocess.run([GIT, "-C", d, "init", "-q"], check=True, env=env)
    top = subprocess.run([GIT, "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, env=env)
    if os.path.realpath(top.stdout.decode().strip()) != os.path.realpath(d):
        raise SystemExit("fixture toplevel mismatch")
    for p, body in files.items():
        fp = os.path.join(d, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "wb" if isinstance(body, bytes) else "w") as fh:
            fh.write(body)
    subprocess.run([GIT, "-C", d, "add", "-A"], check=True, env=env)
    subprocess.run([GIT, "-C", d, "commit", "-q", "-m", "fx"], check=True, env=env)
    rev = subprocess.run([GIT, "-C", d, "rev-parse", "HEAD"], capture_output=True, env=env).stdout.decode().strip()
    return d, rev


def summary_fields(line):
    return dict((k, int(v)) for k, v in re.findall(r"(\w+)=(\d+)", line))


def selftest():
    base = tempfile.mkdtemp(prefix="tally-reconcile-selftest-")
    passed = 0
    total = 0
    try:
        for name, files, records, roots, want, want_rc in SELFTEST_CASES:
            total += 1
            d, rev = build_fixture(base, files)
            lines, rc = reconcile(Tree(d, rev), records, roots)
            got = summary_fields(lines[-1])
            ok = rc == want_rc and all(got.get(k) == v for k, v in want.items())
            passed += ok
            print("SELFTEST %s %s rc=%d %s" % ("PASS" if ok else "FAIL", name, rc, lines[-1]))
        # setup arms
        d, rev = build_fixture(base, {"a.md": "x\n"})
        d3, rev3 = build_fixture(base, {"p/round-3.md": "`X_SELFTEST: 9/9 pass` (`dig.out`)\n",
                                        ".ufo/evidence/round-3/dig.out":
                                        b"X_SELFTEST: 9/9 pass\nX_SELFTEST: 8\xff/8 pass\n"})
        for name, fn in (
            ("setup-rev-short", lambda: Tree(d, rev[:12])),
            ("setup-record-absent", lambda: reconcile(Tree(d, rev), ["nope.md"], [])),
            ("setup-root-not-tree", lambda: reconcile(Tree(d, rev), ["a.md"], ["nope"])),
            ("setup-subdir-not-toplevel", lambda: Tree(os.path.join(d, ".git"), rev)),
            # round-99 A9 (R99SN1 F3): a non-UTF-8 byte inside N/M must not hide a contradiction
            ("setup-receipt-not-utf8", lambda: reconcile(Tree(d3, rev3), ["p/round-3.md"], [])),
        ):
            total += 1
            try:
                fn()
                ok = False
            except Setup:
                ok = True
            passed += ok
            print("SELFTEST %s %s" % ("PASS" if ok else "FAIL", name))
        # worktree edit must not change the verdict (blob read at rev)
        total += 1
        d2, rev2 = build_fixture(base, {"p/round-3.md": "`Y_SELFTEST: 2/2 pass` (`a.out`)\n",
                                        ".ufo/evidence/round-3/a.out": "Y_SELFTEST: 1/2 pass\n"})
        with open(os.path.join(d2, ".ufo/evidence/round-3/a.out"), "w") as fh:
            fh.write("Y_SELFTEST: 2/2 pass\n")
        lines, rc = reconcile(Tree(d2, rev2), ["p/round-3.md"], [])
        ok = rc == 1 and summary_fields(lines[-1]).get("mismatched") == 1
        passed += ok
        print("SELFTEST %s worktree-edit-ignored rc=%d" % ("PASS" if ok else "FAIL", rc))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print("TALLY_RECONCILE_SELFTEST: %d/%d pass" % (passed, total))
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--record", action="append", default=[])
    ap.add_argument("--receipt-root", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args()
    except SystemExit:
        return 64
    # Round-99 A10 (R99SN1 F2): without -I a hostile PYTHONPATH can replace subprocess/re.
    if not sys.flags.isolated:
        print("TALLY_USAGE run as python3 -I (isolated mode is required)")
        return 64
    if a.selftest:
        return selftest()
    if not a.repo or not a.rev or not a.record:
        print("TALLY_USAGE --repo, --rev and at least one --record are required")
        return 64
    try:
        lines, rc = reconcile(Tree(os.path.abspath(a.repo), a.rev), a.record, a.receipt_root)
    except Setup as exc:
        print("TALLY_SETUP %s" % exc)
        return 2
    for ln in lines:
        print(ln)
    return rc


if __name__ == "__main__":
    sys.exit(main())
