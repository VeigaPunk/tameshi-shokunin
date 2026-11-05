#!/usr/bin/env python3
"""T86SC1 independent citation resolver — refined pass.

Refinements over parse_caps.py:
 * figure-shaped tokens (e.g. `107/107`, `4/4`) are excluded — they are
   counters, not paths;
 * a bare basename (e.g. `oracle-repair.json`) is resolved against every
   directory the SAME row cites (e.g. `.ufo/evidence/round-12/`), which is
   how the row itself means it;
 * a path token with a directory is resolved as repo-relative;
 * a token with an ellipsis is recorded as an elided cite (unresolvable
   by construction) and is reported separately.
"""
import json
import os
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
DOC = "SCORECARD.md"

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_NO_REPLACE_OBJECTS="1", GIT_CONFIG_GLOBAL="/dev/null",
           GIT_CONFIG_NOSYSTEM="1")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)


def blob(rev, path):
    p = git("cat-file", "blob", "%s:%s" % (rev, path))
    if p.returncode:
        raise SystemExit("cannot read %s:%s" % (rev, path))
    return p.stdout.decode("utf-8")


def parse_rows(text):
    lines = text.splitlines()
    idx = next(i for i, l in enumerate(lines) if l.strip() == "## Capabilities")
    rows = []
    cur = None
    for l in lines[idx + 1:]:
        if l.startswith("## "):
            break
        s = l.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not cells or set(cells[0]) <= set("-: ") or cells[0] == "Capability":
                cur = None
                continue
            if len(cells) < 3:
                cur = None
                continue
            cur = {"name": cells[0], "cells": cells}
            rows.append(cur)
        elif cur is not None and s:
            cur["cells"][1] += " " + s
            cur["cells"][2] += " " + s
    return rows


SUFFIXES = (".md", ".json", ".sh", ".py", ".txt", ".out", ".stdout", ".jsonl",
            ".tsv", ".csv", ".html", ".yaml", ".yml", ".log")
FIGURE = re.compile(r"^\d+/\d+$")
PATHY = re.compile(r"^[A-Za-z0-9_./\-~<>*]+$")


def raw_tokens(row):
    return re.findall(r"`([^`]+)`", " ".join(row["cells"]))


def pieces(row):
    """Every whitespace-separated piece of every backticked token, plus the
    full tokens (a token may itself be a path)."""
    out = []
    for tok in raw_tokens(row):
        out.append(("tok", tok))
        for part in re.split(r"\s+", tok):
            if part:
                out.append(("part", part))
    return out


def is_pathish(p):
    if not p or FIGURE.match(p):
        return False
    if p.startswith(("http://", "https://")):
        return False
    if not PATHY.match(p):
        return False
    if "/" in p:
        # a directory-like or file-like path; exclude bare flag words
        return bool(re.search(r"\.[A-Za-z0-9]{1,6}$", p)) or p.endswith("/")
    return p.endswith(SUFFIXES)


def row_cites(row):
    """Return (full_paths, bare_names, elided) cited by the row."""
    full, bare, elided = [], [], []
    for kind, p in pieces(row):
        if kind == "tok":
            if "…" in p or "..." in p:
                if any(is_pathish(x) for x in re.split(r"\s+", p)):
                    elided.append(p)
                continue
            if is_pathish(p):
                (full if "/" in p else bare).append(p)
            continue
        # part
        if "…" in p or "..." in p:
            if is_pathish(p.replace("…", "X")):
                elided.append(p)
            continue
        if not is_pathish(p):
            continue
        if "/" in p:
            full.append(p)
        else:
            bare.append(p)
    # dedup
    def dedup(xs):
        seen, out = set(), []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out
    return dedup(full), dedup(bare), dedup(elided)


def resolves(rev, path):
    p = git("cat-file", "-e", "%s:%s" % (rev, path))
    if p.returncode == 0:
        return True
    if "*" in path or "?" in path:
        # glob cite: resolve by listing the parent dir at rev
        d, _, pat = path.rpartition("/")
        d = d or "."
        ls = git("ls-tree", "-r", "--name-only", "%s:%s" % (rev, d))
        if ls.returncode:
            return False
        import fnmatch
        for ln in ls.stdout.decode().splitlines():
            rel = (d + "/" + ln.rsplit("/", 1)[-1]) if d != "." else ln
            if fnmatch.fnmatch(rel, path):
                return True
    return False


def dirs_of(full):
    """Directory prefixes cited by the row (a path ending '/' or the
    directory part of a cited file)."""
    ds = []
    for f in full:
        if f.endswith("/"):
            ds.append(f)
        else:
            d = os.path.dirname(f)
            if d:
                ds.append(d + "/")
    return ds


def main():
    rev = sys.argv[1] if len(sys.argv) > 1 else "d10a9c66d6181cddcad52cdbffd672beb886ff6c"
    text = blob(rev, DOC)
    rows = parse_rows(text)
    print("SCORECARD_CAPABILITY_ROWS: %d (rev=%s)" % (len(rows), rev))
    out_rows = []
    for row in rows:
        full, bare, elided = row_cites(row)
        ds = dirs_of(full)
        cites = []
        for f in full:
            hit = f if resolves(rev, f) else None
            tried = [f]
            if hit is None:
                for d in ds:
                    cand = d + f
                    tried.append(cand)
                    if resolves(rev, cand):
                        hit = cand
                        break
            cites.append({"cite": f, "form": "path", "resolved": hit is not None,
                          "resolved_as": hit, "tried": tried})
        for b in bare:
            hit = None
            tried = []
            for d in ds:
                cand = d + b
                tried.append(cand)
                if resolves(rev, cand):
                    hit = cand
                    break
            if hit is None:
                tried.append(b)
                if resolves(rev, b):
                    hit = b
            cites.append({"cite": b, "form": "basename",
                          "resolved": hit is not None,
                          "resolved_as": hit,
                          "tried": tried})
        out_rows.append({"name": row["name"], "cites": cites, "elided": elided})
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "cap_cites_%s.json" % rev[:8])
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out_rows, fh, indent=1, ensure_ascii=False)

    total = sum(len(r["cites"]) for r in out_rows)
    bad_rows = [r for r in out_rows if any(c["resolved"] is False for c in r["cites"])]
    el_rows = [r for r in out_rows if r["elided"]]
    print("CITATIONS_TOTAL: %d" % total)
    print("ROWS_ALL_CITES_RESOLVE: %d" % (len(out_rows) - len(bad_rows)))
    print("ROWS_WITH_UNRESOLVED_CITE: %d" % len(bad_rows))
    for r in bad_rows:
        print("ROW_UNRESOLVED: %s" % r["name"])
        for c in r["cites"]:
            if c["resolved"] is False:
                print("   MISS cite=%s form=%s tried=%s" %
                      (c["cite"], c["form"], c.get("tried")))
    print("ROWS_WITH_ELIDED_CITE: %d" % len(el_rows))
    for r in el_rows:
        print("ROW_ELIDED: %s :: %s" % (r["name"], r["elided"]))
    print("WROTE %s" % p)


if __name__ == "__main__":
    main()
