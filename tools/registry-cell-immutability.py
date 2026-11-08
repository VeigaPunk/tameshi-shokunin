#!/usr/bin/env python3
"""registry-cell-immutability — audit CORPUS SOURCES registry rows between two
commits for in-place edits of immutable cells.

`CORPUS.md` §SOURCES.md rule 2 is append-only: only `status`, `recheck` and
`used-by` may change in place, and each change is logged old→new in the round
lesson; every other cell (source, kind, tier, scope, anchor, teaches, opened)
is frozen, and a correction is a new superseding row. Round 97 edited the
`anchor` cells of S159 and S006 in place; the round's census passed and only
the non-author spot-check (D-1) caught it. This tool measures the class.

Both revisions are read as blobs through `git cat-file` (never a worktree).
Rows are parsed with the maintained 0-3 leading-space rule; a row that is not
11 columns is setup, not a verdict (a malformed registry has no cell identity).

Usage:
  python3 -I tools/registry-cell-immutability.py --repo LANE \
      --from <40 hex> --to <40 hex> [--path corpus/SOURCES.md] [--selftest]

Exit: 0 no immutable cell changed and no row removed; 1 findings (each printed
as `REGISTRY_CELL <id>:<column> changed` or `REGISTRY_ROW removed <id>`);
2 setup (bad rev, blob absent, zero rows, malformed row); 64 usage.
"""
import argparse
import os
import re
import subprocess
import sys

GIT = "/usr/bin/git"
PATH = "corpus/SOURCES.md"
ROW = re.compile(r"^ {0,3}\|[ \t]*S([0-9]{3,})[ \t]*\|")
COLUMNS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
           "status", "opened", "recheck", "used-by"]
IMMUTABLE = {1: "source", 2: "kind", 3: "tier", 4: "scope", 5: "anchor",
             6: "teaches", 8: "opened"}


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def parse_registry(text):
    """Returns id -> 11-cell tuple, or raises ValueError with the first defect."""
    rows = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        if not ROW.match(line):
            continue
        parts = line.split("|")
        if len(parts) != 13:
            raise ValueError("malformed row at line %d: %d columns" % (lineno, len(parts) - 2))
        cells = [c.strip() for c in parts[1:12]]
        rid = cells[0]
        if rid in rows:
            raise ValueError("duplicate id %s at line %d" % (rid, lineno))
        rows[rid] = cells
    if not rows:
        raise ValueError("no registry rows")
    return rows


def compare(old, new):
    findings = []
    changed = removed = added = 0
    for rid in old:
        if rid not in new:
            findings.append("REGISTRY_ROW removed %s" % rid)
            removed += 1
    for rid in new:
        if rid not in old:
            added += 1
            continue
        for idx, name in IMMUTABLE.items():
            if old[rid][idx] != new[rid][idx]:
                findings.append("REGISTRY_CELL %s:%s changed" % (rid, name))
                changed += 1
    return findings, changed, removed, added


def blob(repo, rev, path):
    r = subprocess.run([GIT, "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True, env=sealed_env())
    return None if r.returncode != 0 else r.stdout


def resolve(repo, rev):
    if not re.fullmatch(r"[0-9a-f]{40}", rev or ""):
        return None
    r = subprocess.run([GIT, "-C", repo, "rev-parse", "--verify", "--quiet",
                        "--end-of-options", rev + "^{commit}"],
                       capture_output=True, env=sealed_env())
    return r.stdout.decode().strip() if r.returncode == 0 else None


def selftest():
    head = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    def row(rid, anchor="A1", status="mined", recheck="90d", used="—", teaches="t",
            indent=""):
        return "%s| %s | src-%s | docs | A | s | %s | %s | %s | 2026-01-01 | %s | %s |" % (
            indent, rid, rid, anchor, teaches, status, recheck, used)
    def run(old, new):
        try:
            return compare(parse_registry(old), parse_registry(new)), None
        except ValueError as exc:
            return None, str(exc)
    cases = []
    # 1 anchor changed -> finding
    r, err = run(head + row("S001"), head + row("S001", anchor="A2"))
    cases.append(("anchor-change", err is None and r[1] == 1 and r[2] == 0 and len(r[0]) == 1,
                  "changed=1"))
    # 2 status only -> clean
    r, err = run(head + row("S001"), head + row("S001", status="queued"))
    cases.append(("status-only", err is None and r[1] == 0 and len(r[0]) == 0, "clean"))
    # 3 recheck+used-by -> clean
    r, err = run(head + row("S001"), head + row("S001", recheck="2026-02-02", used="corpus/x.md"))
    cases.append(("recheck-usedby", err is None and r[1] == 0 and len(r[0]) == 0, "clean"))
    # 4 row added -> clean, added counted
    r, err = run(head + row("S001"), head + row("S001") + "\n" + row("S002"))
    cases.append(("row-added", err is None and r[1] == 0 and r[3] == 1, "clean added=1"))
    # 5 row removed -> finding
    r, err = run(head + row("S001") + "\n" + row("S002"), head + row("S001"))
    cases.append(("row-removed", err is None and r[2] == 1 and len(r[0]) == 1, "removed=1"))
    # 6 teaches changed -> finding
    r, err = run(head + row("S001"), head + row("S001", teaches="other"))
    cases.append(("teaches-change", err is None and r[1] == 1, "changed=1"))
    # 7 two-space-indented row is parsed, not ignored
    r, err = run(head + row("S001", indent="  "), head + row("S001", indent="  ", anchor="A2"))
    cases.append(("indented-parsed", err is None and r[1] == 1, "changed=1"))
    # 8 malformed row -> setup
    bad = head + row("S001")[:60]
    r, err = run(head + row("S001"), bad)
    cases.append(("malformed-setup", r is None and err is not None, "setup"))
    # 9 no rows -> setup (no vacuous pass)
    r, err = run(head, head + row("S001"))
    cases.append(("empty-setup", r is None and err is not None, "setup"))
    # 10 column-zero row parsed
    r, err = run(head + row("S001", indent="") , head + row("S001", indent="", anchor="A9"))
    cases.append(("column-zero-parsed", err is None and r[1] == 1, "changed=1"))
    passed = 0
    for name, ok, want in cases:
        passed += bool(ok)
        print("SELFTEST %s %s want=%s" % (name, "PASS" if ok else "FAIL", want))
    total = len(cases)
    print("REGISTRY_IMMUTABLE_SELFTEST: %d/%d pass" % (passed, total))
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None)
    ap.add_argument("--from", dest="rev_from", default=None)
    ap.add_argument("--to", dest="rev_to", default=None)
    ap.add_argument("--path", default=PATH)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.repo or not a.rev_from or not a.rev_to:
        print(__doc__)
        sys.exit(64)
    repo = os.path.realpath(a.repo)
    lo = resolve(repo, a.rev_from)
    hi = resolve(repo, a.rev_to)
    if not lo or not hi:
        print("REGISTRY_SETUP rev-unresolvable")
        sys.exit(2)
    ob = blob(repo, lo, a.path)
    nb = blob(repo, hi, a.path)
    if ob is None or nb is None:
        print("REGISTRY_SETUP blob-absent-at-rev:%s" % a.path)
        sys.exit(2)
    try:
        old = parse_registry(ob.decode("utf-8"))
        new = parse_registry(nb.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        print("REGISTRY_SETUP unparsable:%s" % exc)
        sys.exit(2)
    findings, changed, removed, added = compare(old, new)
    for line in findings:
        print(line)
    print("REGISTRY_IMMUTABLE from=%s to=%s shared=%d changed=%d removed=%d added=%d"
          % (lo[:12], hi[:12], len(set(old) & set(new)), changed, removed, added))
    sys.exit(0 if changed == 0 and removed == 0 else 1)


if __name__ == "__main__":
    main()
