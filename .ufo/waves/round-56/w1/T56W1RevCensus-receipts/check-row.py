#!/usr/bin/env python3
"""Hand-check a candidate corpus/SOURCES.md row against SOURCES-CONTRACT-v1.

Reimplements the census validator's row rules (scripts/sources-census.sh row_pass,
usedby_findings) plus the two extra rules the seat item names: no literal or
escaped pipe in any cell, and duplicate-URL lookup against the whole registry.

Usage:
  check-row.py --lane LANE_DIR --sources BASE_SOURCES_MD --row ROW_FILE
               [--today YYYY-MM-DD] [--allow-missing-usedby PATH ...]
ROW_FILE holds the candidate table row(s), one per line (leading spaces allowed).
--allow-missing-usedby names used-by paths that will exist only at C0.
Exit: 0 all rows pass, 1 at least one row fails.
"""
import argparse
import datetime
import os
import re
import sys

KIND = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book",
        "community", "own-work"}
TIER = {"A", "B", "C"}
STATUS = {"queued", "mined", "rejected"}
HEADING = re.compile(r"^ {0,3}##[ \t]")
TOP = re.compile(r"^ {0,3}#[ \t]")
TABLE = re.compile(r"^ {0,3}\|")
ISO = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
CADENCE = re.compile(r"^[0-9]+d$")
SYMBOLIC = re.compile(r"^[A-Za-z][A-Za-z0-9 _-]*$")


def url_of(s):
    """Same normalisation as the census gawk url_of()."""
    m = re.search(r"https?://[^\s|]+", s)
    if not m:
        return ""
    u = m.group(0)
    u = re.sub(r"#[^ ]*$", "", u)
    u = re.sub(r"/$", "", u)
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    u = u[:n].lower() + u[n:] if n >= 0 else u.lower()
    return u


def registry_rows(path):
    """Yield (lineno, cells) for rows inside ## Registry, separator/header skipped."""
    section = None
    with open(path, encoding="utf-8") as fh:
        for no, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if HEADING.match(line):
                section = line.lstrip(" ")[2:].strip()
                continue
            if TOP.match(line):
                section = None
                continue
            if section != "Registry" or not TABLE.match(line):
                continue
            body = line.lstrip(" ")
            cells = body.split("|")
            if len(cells) < 3:
                continue
            inner = cells[1:-1]
            if inner and inner[0].strip() == "id":
                continue
            if all(re.fullmatch(r":?-+:?", c.strip()) for c in inner if c.strip()) and inner:
                continue
            yield no, [c.strip() for c in inner]


def epoch(s):
    if not ISO.match(s):
        return None
    try:
        return datetime.date(*map(int, s.split("-")))
    except ValueError:
        return None


def check(row, no, lane, base_urls, base_scopes, today, allow_missing, max_id):
    fails = []
    if "\\|" in row:
        fails.append("ESCPIPE: escaped '|' in the row inflates NF (contract forbids it)")
    cells = row.split("|")
    # A well-formed row is "| c1 | ... | c11 |" -> split yields 13 fields.
    if len(cells) != 13:
        fails.append(f"E01: NF={len(cells)} (need 13 => 11 columns + 2 empty); "
                     f"a literal '|' inside a cell is the usual cause")
    inner = [c.strip() for c in cells[1:-1]]
    if len(inner) < 11:
        return fails or ["E01: fewer than 11 cells; cannot continue"]
    rid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby = inner[:11]
    if not re.fullmatch(r"S[0-9]{3,}", rid):
        fails.append(f"E02: id={rid!r} is not S[0-9]{{3,}}")
    else:
        n = int(rid[1:])
        if n <= max_id:
            fails.append(f"E02/E03: id={rid} <= registry max S{max_id:03d} (next unused is S{max_id+1:03d})")
        if rid in base_urls["ids"]:
            fails.append(f"E03: id={rid} already present in the registry")
    if kind not in KIND:
        fails.append(f"E05: kind={kind!r} not in {sorted(KIND)}")
    if tier not in TIER:
        fails.append(f"E06: tier={tier!r} not in A|B|C")
    if status not in STATUS:
        fails.append(f"E07: status={status!r} not in queued|mined|rejected")
    if tier == "A" and kind == "community":
        fails.append("E10: community source tiered A")
    o = epoch(opened)
    if o is None:
        fails.append(f"E08: opened={opened!r} is not a valid ISO date")
    elif o > today:
        fails.append(f"E08: opened={opened} is in the future (today {today})")
    if ISO.match(recheck):
        if epoch(recheck) is None:
            fails.append(f"E09: recheck={recheck!r} is not a valid ISO date")
    elif not CADENCE.match(recheck) and not SYMBOLIC.match(recheck):
        fails.append(f"E09: recheck={recheck!r} is neither an ISO date, NNd, nor a symbolic cadence")
    u = url_of(source)
    if not u:
        fails.append("CONTRACT: source cell carries no http(s) URL")
    else:
        for prior_id, prior_url in base_urls["urls"]:
            if prior_url == u:
                scope_key = (u, scope)
                if prior_id and (prior_id, scope) in base_urls["scopes"]:
                    if status != "rejected" and not re.search(r"supersedes S[0-9]{3}", teaches):
                        fails.append(f"E04: url {u} already in scope {scope!r} as {prior_id}; "
                                     f"teaches must say 'supersedes S###' or the row is a duplicate")
                else:
                    fails.append(f"W04: url {u} already present as {prior_id} (cross-scope duplicate; "
                                 f"reuse the existing row instead of adding one)")
    if status == "rejected" and len(teaches) < 8:
        fails.append("W02: rejected row with a thin reason (<8 chars)")
    if status == "rejected" and "REJECTED:" not in teaches:
        fails.append("CONTRACT: rejected row must read 'REJECTED: <reason>; flip: <what would change the verdict>'")
    if status == "mined" and usedby == "—":
        fails.append("W03: mined row with used-by = —")
    if tier == "C" and status == "mined" and usedby != "—":
        fails.append(f"W01: tier-C mined row with a used-by ({usedby})")
    if not anchor.strip() or anchor == "—":
        fails.append("CONTRACT: anchor cell empty")
    if usedby != "—":
        for p in [x.strip() for x in usedby.split(",") if x.strip()]:
            if p in allow_missing:
                continue
            if not os.path.exists(os.path.join(lane, p)):
                fails.append(f"E11: used-by path {p} does not exist in the lane")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--sources", required=True, help="registry to compare against (base SOURCES.md)")
    ap.add_argument("--row", required=True)
    ap.add_argument("--today", default=datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    ap.add_argument("--allow-missing-usedby", nargs="*", default=[])
    a = ap.parse_args()
    today = datetime.date(*map(int, a.today.split("-")))
    urls, scopes, ids = [], set(), set()
    max_id = 0
    for _no, cells in registry_rows(a.sources):
        if len(cells) < 11:
            continue
        rid, source, _k, _t, scope = cells[0], cells[1], cells[2], cells[3], cells[4]
        ids.add(rid)
        if re.fullmatch(r"S[0-9]{3,}", rid):
            max_id = max(max_id, int(rid[1:]))
        u = url_of(source)
        if u:
            urls.append((rid, u))
            scopes.add((rid, scope))
    base = {"urls": urls, "scopes": scopes, "ids": ids}
    rc = 0
    rows = [l.rstrip("\n") for l in open(a.row, encoding="utf-8") if l.strip()]
    if not rows:
        print("FAIL: row file holds no candidate row")
        return 1
    for i, row in enumerate(rows, 1):
        fails = check(row, i, a.lane, base, None, today, set(a.allow_missing_usedby), max_id)
        label = row.strip()[:60]
        if fails:
            rc = 1
            print(f"FAIL row {i}: {label}...")
            for f in fails:
                print(f"  - {f}")
        else:
            print(f"PASS row {i}: {label}...")
    return rc


if __name__ == "__main__":
    sys.exit(main())
