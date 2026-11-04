#!/usr/bin/env python3
"""Independent oracle for the R73-C1 reconciliation rule (seat T73W1S01).

This file is a from-scratch re-implementation of the rule stated in
`plans/round-73.plan.md` and the tool docstring.  It imports nothing from
`tools/wave-reconcile.py`; every record span, artifact listing, byte decode and
multiset comparison below is its own code over git objects.

What it does
------------
For every row of `tools/wave-reconcile.json`:

  * resolve the record's root (`lane` = this repo, `fleet` = --extra-root) and
    read the record blob at the record revision with `git cat-file blob`;
  * locate the declared record span as a BYTE substring and print its offset;
  * decode the artifact bytes as strict UTF-8, refusing a leading BOM;
  * re-derive the artifact side of the row with its own code:

      seats         printed == len(results) == results.seats
      seat_reports  printed == number of top-level *.md in the wave dir at rev
      roles         declared role multiset == `agent` multiset in results
      attack_share  |seats whose agent is in `named`| / |seats| >= floor_pct

  * measure `meet`/`drift` and compare with the row's `expect`.

Then it runs the lane's tool exactly once and diffs its `WAVE_ROW` lines with
the oracle's own rows on the tuple (id, kind, expect, measured, ok); the
`detail=` text is ignored.

Output lines:
  ORACLE_SPAN ...   record span location (record, rev, byte offset, length)
  ORACLE_ROW ...    one per manifest row, with the re-derived values
  TOOL ...          tool exit code / summary line / raw WAVE_ROW lines
  CMP ...           exactly one per manifest row: the differential result
  ORACLE rows=N met=N unexpected=N

Exit: 0 oracle rows all matched `expect` and (unless --no-tool) every
differential row agreed; 1 otherwise; 2 setup error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter

BOM = b"\xef\xbb\xbf"
WAVE_ROW_RE = re.compile(
    r"^WAVE_ROW\s+(\S+)\s+"
    r"kind=([A-Za-z_]+)\s+"
    r"expect=([A-Za-z_]+)\s+"
    r"measured=([A-Za-z_]+)\s+"
    r"(.*)$"
)


class SetupError(Exception):
    """A row could not be bound to its record or artifact (exit 2)."""


def git(repo: str, args: list[str]) -> bytes:
    proc = subprocess.run(
        ["git", "-C", repo, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip()
        raise SetupError(
            "git %s failed in %s (rc=%d): %s"
            % (" ".join(args), repo, proc.returncode, err)
        )
    return proc.stdout


def commit_sha(repo: str, rev: str) -> str:
    out = git(repo, ["rev-parse", "--verify", rev + "^{commit}"])
    return out.decode("ascii").strip()


def blob_at(repo: str, rev: str, path: str) -> bytes:
    sha = commit_sha(repo, rev)
    return git(repo, ["cat-file", "blob", sha + ":" + path])


def decode_utf8(raw: bytes, label: str) -> str:
    if raw.startswith(BOM):
        raise SetupError("UTF-8 BOM refused: %s" % label)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SetupError("undecodable UTF-8 artifact: %s (%s)" % (label, exc))


def load_json(raw: bytes, label: str):
    return json.loads(decode_utf8(raw, label))


def token_in(text: str, value: int) -> bool:
    """`value` occurs as a delimited token (no adjacent word characters)."""
    return re.search(r"(?<![0-9A-Za-z_])%d(?![0-9A-Za-z_])" % value, text) is not None


def role_pair_in(text: str, count: int, role: str) -> bool:
    """`<count> <role>` occurs as a delimited pair inside the record span."""
    pattern = r"(?<![0-9A-Za-z_-])%d %s(?![0-9A-Za-z_-])" % (
        count,
        re.escape(role),
    )
    return re.search(pattern, text) is not None


def resolve_root(roots: dict[str, str], spec: dict) -> str:
    name = spec.get("root", "lane")
    if name not in roots:
        raise SetupError("root %r has no --extra-root binding" % (name,))
    return roots[name]


def top_level_md_count(repo: str, rev: str, directory: str) -> tuple[int, list[str]]:
    sha = commit_sha(repo, rev)
    out = git(repo, ["ls-tree", "-r", "--name-only", sha, "--", directory])
    text = decode_utf8(out, "ls-tree %s:%s" % (sha, directory))
    prefix = directory.rstrip("/") + "/"
    names = []
    for line in text.splitlines():
        if not line.startswith(prefix):
            continue
        rest = line[len(prefix):]
        if "/" in rest:
            continue
        if rest.endswith(".md"):
            names.append(rest)
    return len(names), sorted(names)


def agents_of(results_obj: dict) -> tuple[list[dict], Counter]:
    seats = results_obj.get("results")
    if not isinstance(seats, list) or not seats:
        raise SetupError("wave results carry no non-empty results[]")
    agents = Counter()
    for index, seat in enumerate(seats):
        agent = seat.get("agent")
        if not isinstance(agent, str) or not agent:
            raise SetupError("results[%d] has no agent string" % index)
        agents[agent] += 1
    return seats, agents


def counter_delta(left: Counter, right: Counter) -> dict[str, list[int]]:
    delta = {}
    for key in sorted(set(left) | set(right)):
        if left[key] != right[key]:
            delta[key] = [left[key], right[key]]
    return delta


def evaluate_row(roots: dict[str, str], row: dict) -> dict:
    kind = row.get("kind")
    record = row.get("record")
    wave = row.get("wave")
    if not isinstance(record, dict) or not isinstance(wave, dict):
        raise SetupError("row %r lacks record/wave" % (row.get("id"),))

    rec_repo = resolve_root(roots, record)
    rec_label = "%s(%s):%s@%s" % (
        record.get("root", "lane"),
        rec_repo,
        record["path"],
        record["rev"],
    )
    rec_raw = blob_at(rec_repo, record["rev"], record["path"])
    rec_text = decode_utf8(rec_raw, rec_label)

    span = record["span"]
    if not isinstance(span, str) or not span:
        raise SetupError("row %r has no record span" % (row.get("id"),))
    span_bytes = span.encode("utf-8")
    offset = rec_raw.find(span_bytes)
    if offset < 0:
        raise SetupError(
            "record span is not a byte substring of %s: %r" % (rec_label, span)
        )
    occurrences = 0
    cursor = offset
    while cursor >= 0:
        occurrences += 1
        cursor = rec_raw.find(span_bytes, cursor + 1)

    wave_repo = resolve_root(roots, wave)
    wave_label = "%s@%s" % (wave["results"], wave["rev"])
    results_obj = load_json(
        blob_at(wave_repo, wave["rev"], wave["results"]), wave_label
    )
    seats, agents = agents_of(results_obj)

    printed = record.get("printed")
    if not isinstance(printed, int):
        raise SetupError("row %r has no integer printed" % (row.get("id"),))

    detail: dict[str, object] = {}
    measured = "drift"

    if kind == "seats":
        if not token_in(span, printed):
            raise SetupError(
                "printed %d is not a delimited token in the span for %r"
                % (printed, row["id"])
            )
        declared_seats = results_obj.get("seats")
        length = len(seats)
        detail["printed"] = printed
        detail["len_results"] = length
        detail["results_seats"] = declared_seats
        measured = "meet" if (printed == length == declared_seats) else "drift"

    elif kind == "seat_reports":
        if not token_in(span, printed):
            raise SetupError(
                "printed %d is not a delimited token in the span for %r"
                % (printed, row["id"])
            )
        count, names = top_level_md_count(wave_repo, wave["rev"], wave["dir"])
        detail["printed"] = printed
        detail["top_md"] = count
        detail["top_md_names"] = ",".join(names)
        measured = "meet" if printed == count else "drift"

    elif kind == "roles":
        declaration = row.get("declaration")
        if not isinstance(declaration, dict):
            raise SetupError("roles row %r has no declaration" % (row["id"],))
        form = declaration.get("form")
        if form == "spec-items":
            decl_repo = resolve_root(roots, declaration)
            decl_label = "%s(%s):%s@%s" % (
                declaration.get("root", "lane"),
                decl_repo,
                declaration["path"],
                declaration["rev"],
            )
            spec = load_json(
                blob_at(decl_repo, declaration["rev"], declaration["path"]),
                decl_label,
            )
            items = spec.get("items")
            if not isinstance(items, list) or not items:
                raise SetupError("spec %s carries no items[]" % decl_label)
            declared = Counter()
            for index, item in enumerate(items):
                role = item.get("role")
                if not isinstance(role, str) or not role:
                    raise SetupError("spec items[%d] has no role" % index)
                declared[role] += 1
        elif form == "text-tokens":
            declared_roles = declaration.get("roles")
            if not isinstance(declared_roles, dict) or not declared_roles:
                raise SetupError("text-tokens declaration has no roles map")
            declared = Counter()
            for role, count in declared_roles.items():
                if not isinstance(role, str) or not isinstance(count, int):
                    raise SetupError("text-tokens declaration is not string->int")
                if not role_pair_in(span, count, role):
                    raise SetupError(
                        "declared pair %d %s is absent from the span for %r"
                        % (count, role, row["id"])
                    )
                declared[role] += count
        else:
            raise SetupError("unknown role declaration form %r" % (form,))
        delta = counter_delta(declared, agents)
        detail["declaration_form"] = form
        detail["roles_declared"] = json.dumps(dict(sorted(declared.items())), sort_keys=True)
        detail["roles_artifacts"] = json.dumps(dict(sorted(agents.items())), sort_keys=True)
        detail["role_delta"] = json.dumps(delta, sort_keys=True)
        measured = "meet" if declared == agents else "drift"

    elif kind == "attack_share":
        if not token_in(span, printed):
            raise SetupError(
                "printed %d is not a delimited token in the span for %r"
                % (printed, row["id"])
            )
        named = row.get("named")
        floor_pct = row.get("floor_pct")
        if not isinstance(named, list) or not named:
            raise SetupError("attack_share row %r has no named roles" % (row["id"],))
        if not isinstance(floor_pct, int):
            raise SetupError("attack_share row %r has no integer floor_pct" % (row["id"],))
        total = len(seats)
        attack = sum(1 for seat in seats if seat.get("agent") in set(named))
        detail["attack"] = attack
        detail["total"] = total
        detail["floor_pct"] = floor_pct
        detail["share_pct_x100"] = (attack * 10000) // total if total else 0
        measured = "meet" if attack * 100 >= floor_pct * total else "drift"
    else:
        raise SetupError("unknown row kind %r" % (kind,))

    return {
        "id": row.get("id"),
        "kind": kind,
        "expect": row.get("expect"),
        "printed": printed,
        "measured": measured,
        "ok": measured == row.get("expect"),
        "offset": offset,
        "span_len": len(span_bytes),
        "span_occurrences": occurrences,
        "record": {
            "root": record.get("root", "lane"),
            "path": record["path"],
            "rev": record["rev"],
        },
        "detail": detail,
    }


def parse_tool_rows(stdout: str) -> tuple[dict[str, dict], list[str]]:
    rows: dict[str, dict] = {}
    raw = []
    for line in stdout.splitlines():
        if not line.startswith("WAVE_ROW"):
            continue
        raw.append(line)
        match = WAVE_ROW_RE.match(line)
        if not match:
            continue
        rid, kind, expect, measured, tail = match.groups()
        verdict = tail.split(None, 1)[0] if tail else ""
        rows[rid] = {
            "kind": kind,
            "expect": expect,
            "measured": measured,
            "ok": verdict == "ok",
            "raw": line,
        }
    return rows, raw


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--repo", default=".", help="lane repo worktree (default .)")
    parser.add_argument(
        "--extra-root",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help="root binding for record roots other than lane",
    )
    parser.add_argument(
        "--manifest", default="tools/wave-reconcile.json", help="manifest path"
    )
    parser.add_argument(
        "--no-tool", action="store_true", help="skip the differential tool run"
    )
    parser.add_argument("--tool-timeout", type=int, default=180)
    args = parser.parse_args(argv)

    lane_root = os.path.abspath(args.repo)
    roots = {"lane": lane_root}
    extras = list(args.extra_root)
    if not extras:
        extras = ["fleet=/home/vgpnk/Projects/shokunin"]
    for item in extras:
        if "=" not in item:
            raise SetupError("--extra-root expects NAME=PATH, got %r" % (item,))
        name, path = item.split("=", 1)
        if not name or not path:
            raise SetupError("--extra-root expects NAME=PATH, got %r" % (item,))
        roots[name] = os.path.abspath(path)

    toplevel = git(lane_root, ["rev-parse", "--show-toplevel"]).decode("utf-8").strip()
    if os.path.realpath(toplevel) != os.path.realpath(lane_root):
        raise SetupError(
            "lane root %s is not a git top level (got %s)" % (lane_root, toplevel)
        )

    manifest_path = args.manifest
    if not os.path.isabs(manifest_path):
        manifest_path = os.path.join(lane_root, manifest_path)
    with open(manifest_path, "rb") as handle:
        manifest_raw = handle.read()
    manifest = load_json(manifest_raw, "manifest " + manifest_path)
    if manifest.get("schema") != "tameshi-wave-reconcile-v1":
        raise SetupError("unexpected manifest schema %r" % (manifest.get("schema"),))
    rows = manifest.get("rows")
    if not isinstance(rows, list) or not rows:
        raise SetupError("zero-row manifest")

    oracle_rows = []
    for row in rows:
        result = evaluate_row(roots, row)
        oracle_rows.append(result)
        print(
            "ORACLE_SPAN id=%s record=%s:%s@%s span_bytes=%d offset=%d occurrences=%d"
            % (
                result["id"],
                result["record"]["root"],
                result["record"]["path"],
                result["record"]["rev"],
                result["span_len"],
                result["offset"],
                result["span_occurrences"],
            )
        )
        detail = " ".join(
            "%s=%s" % (key, detail_value)
            for key, detail_value in result["detail"].items()
        )
        print(
            "ORACLE_ROW id=%s kind=%s expect=%s measured=%s %s%s"
            % (
                result["id"],
                result["kind"],
                result["expect"],
                result["measured"],
                "ok" if result["ok"] else "MISMATCH",
                (" " + detail) if detail else "",
            )
        )

    met = sum(1 for result in oracle_rows if result["ok"])
    unexpected = len(oracle_rows) - met

    if args.no_tool:
        print("ORACLE_TOOL skipped=1 reason=--no-tool")
        print("ORACLE rows=%d met=%d unexpected=%d" % (len(oracle_rows), met, unexpected))
        return 0 if unexpected == 0 else 1

    tool_path = os.path.join(lane_root, "tools", "wave-reconcile.py")
    if not os.path.isfile(tool_path):
        raise SetupError("tool not found: %s" % tool_path)
    cmd = [
        "python3",
        "-I",
        "-X",
        "utf8",
        tool_path,
        "--repo",
        ".",
        "--extra-root",
        "fleet=" + roots["fleet"],
        "--manifest",
        "tools/wave-reconcile.json",
    ]
    proc = subprocess.run(
        cmd,
        cwd=lane_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=args.tool_timeout,
    )
    stdout = proc.stdout.decode("utf-8", "replace")
    stderr = proc.stderr.decode("utf-8", "replace")
    print("TOOL_EXIT rc=%d" % proc.returncode)
    summary = [
        line for line in stdout.splitlines() if line.startswith("WAVE_RECONCILE")
    ]
    for line in summary:
        print("TOOL_SUMMARY " + line)
    if stderr.strip():
        for line in stderr.strip().splitlines():
            print("TOOL_STDERR " + line)

    tool_rows, raw_rows = parse_tool_rows(stdout)
    for line in raw_rows:
        print("TOOL_RAW " + line)

    matched = 0
    missing = 0
    for result in oracle_rows:
        rid = result["id"]
        tool_row = tool_rows.get(rid)
        if tool_row is None:
            missing += 1
            print("CMP id=%s tool=MISSING oracle_measured=%s equal=0" % (rid, result["measured"]))
            continue
        flags = {
            "id_eq": 1,
            "kind_eq": int(tool_row["kind"] == result["kind"]),
            "expect_eq": int(tool_row["expect"] == result["expect"]),
            "measured_eq": int(tool_row["measured"] == result["measured"]),
            "ok_eq": int(tool_row["ok"] == result["ok"]),
        }
        equal = all(flags.values())
        if equal:
            matched += 1
        print(
            "CMP id=%s tool_kind=%s oracle_kind=%s tool_measured=%s oracle_measured=%s "
            "tool_ok=%d oracle_ok=%d %s equal=%d"
            % (
                rid,
                tool_row["kind"],
                result["kind"],
                tool_row["measured"],
                result["measured"],
                int(tool_row["ok"]),
                int(result["ok"]),
                " ".join("%s=%d" % (key, value) for key, value in flags.items()),
                int(equal),
            )
        )
        if not equal:
            print("CMP_DISAGREE id=%s tool_raw=%r oracle_row=%r" % (rid, tool_row["raw"], result))

    extra_ids = sorted(set(tool_rows) - {result["id"] for result in oracle_rows})
    print(
        "ORACLE_CMP rows=%d equal=%d missing=%d extra=%d"
        % (len(oracle_rows), matched, missing, len(extra_ids))
    )
    if extra_ids:
        print("ORACLE_EXTRA_IDS " + ",".join(extra_ids))

    print("ORACLE rows=%d met=%d unexpected=%d" % (len(oracle_rows), met, unexpected))
    if unexpected != 0 or missing or extra_ids or matched != len(oracle_rows):
        return 1
    if proc.returncode != 0:
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SetupError as exc:
        print("ORACLE_SETUP_ERROR " + str(exc))
        sys.exit(2)
