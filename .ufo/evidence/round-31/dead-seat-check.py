#!/usr/bin/env python3
"""dead-seat-check.py — flag a new wave spec that re-dispatches a dead seat (round 31, wave 1).

Routed defect 3 of the round-30 closure (lesson round-30, Mistake 4): a seat
whose engine died before it wrote a report was re-entered in the next wave
under the same name, and nothing looked. This check reads the round's dead-seat
list plus the proposed wave spec and prints one line per new item that reuses a
dead seat's name or repeats its target work.

Usage:
    python3 dead-seat-check.py --dead DEAD --spec SPEC.json [--min-jaccard 0.6]
    python3 dead-seat-check.py --selftest

DEAD accepts three shapes, detected from the first non-blank byte:
  * a wave spec — JSON object with "items": [{"name": ..., "prompt": ...}, ...];
    each item's target text comes from its prompt (or an explicit "target" key).
    This is the intended way to pass a dead round: the prior spec carries the
    targets.
  * a JSON list of dead seats — ["Name", ...] or [{"name": ..., "target": ...}, ...];
    a JSON object with "dead" or "seats" instead of a bare list is also accepted.
  * a text list, one seat per line — "NAME<tab>k=v..."; blank lines and lines
    whose first non-blank character is "#" are skipped; a "target=" field, when
    present, supplies the target text (the attempt-2 dead-seats.txt shape parses
    as name-only). Other fields are ignored.

Similarity rule (stated in full): for each side take the "# Target" part of the
prompt — the text after a line matching ^#\\s*Target\\b up to (not including)
the next line matching ^#\\s+\\S, i.e. the next level-1 heading such as
"# Acceptance"; a target given by an explicit "target" key is used verbatim.
Lowercase that text, take the set of word tokens matching [a-z0-9_]+, and
compare with Jaccard: |A&B| / |A|B|. A pair is near-identical when its Jaccard
is >= --min-jaccard (default 0.6). A pair is compared only when both sides have
a non-empty target; the name check is exact after normalisation (lowercase,
drop every character outside [a-z0-9]), so Ctl-S3 and Ctls3 collide by design.
At most one line is printed per new item; a name match outranks a target match.

Known property, measured on round-30 spec-wC (38 items): the Cold*/ColdB*
targets are 0.90-0.97 Jaccard similar to each other because most of their text
is shared boilerplate, so on a cold-read wave the default threshold flags every
new cold read against any dead one. Raise --min-jaccard (>= 0.98) for such
waves, or judge the flagged pair by reading it; the flag is a pointer, not a
verdict.

Output (stdout, one line per flagged item, sorted by item name):
    FLAG item=<name> dead=<dead name> reason=name-reuse|target-similar|name-reuse+target-similar jaccard=<0.xx|->
One trailer line on stderr:
    DEAD_SEAT_CHECK: dead=<D> items=<N> flagged=<K> threshold=<x.xx>

Exits: 0 no flagged item · 1 any flagged item · 2 bad input (unreadable,
unparseable, empty dead list, spec without items, item without a name, bad
threshold, missing argument). Empty inputs are errors, not passes: a truncated
or absent file must never look like a clean wave.
"""
import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
from pathlib import Path

MIN_JACCARD = 0.6
TARGET_HEADING = re.compile(r"(?m)^#\s*Target\b")
NEXT_HEADING = re.compile(r"(?m)^#\s+\S")
TOKEN = re.compile(r"[a-z0-9_]+")
NON_NAME = re.compile(r"[^a-z0-9]")
FIELD_TARGET = re.compile(r"(?:^|\t)target=(.*?)(?=\t[a-z_]+=|$)")
JSON_LEAD = ("{", "[")


class BadInput(Exception):
    """Operator error: unreadable, unparseable or empty input."""


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise BadInput(f"{path}: cannot read ({exc.strerror or exc})") from None
    except UnicodeDecodeError as exc:
        raise BadInput(f"{path}: not UTF-8 text ({exc.reason} at byte {exc.start})") from None


def parse_json(text, path):
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise BadInput(f"{path}: invalid JSON ({exc.msg} at line {exc.lineno} column {exc.colno})") from None


def target_of(prompt):
    """The '# Target' part of a prompt, or '' when the prompt has no such heading."""
    if not isinstance(prompt, str):
        return ""
    head = TARGET_HEADING.search(prompt)
    if head is None:
        return ""
    rest = prompt[head.end():]
    end = NEXT_HEADING.search(rest)
    return rest[:end.start()] if end else rest


def entry(name, target, where):
    if not isinstance(name, str) or not name.strip():
        raise BadInput(f"{where}: seat entry has no usable name")
    if target is None:
        target = ""
    if not isinstance(target, str):
        raise BadInput(f"{where}: seat {name.strip()!r} has a non-string target")
    return {"name": name.strip(), "target": target}


def entries_from_spec_item(item, where):
    if not isinstance(item, dict):
        raise BadInput(f"{where}: item is not a JSON object")
    name = item.get("name")
    if not isinstance(name, str) or not name.strip():
        raise BadInput(f"{where}: item has no usable \"name\"")
    if "target" in item:
        return entry(name, item["target"], where)
    return entry(name, target_of(item.get("prompt", "")), where)


def entries_from_list(data, path):
    out = []
    for index, item in enumerate(data):
        where = f"{path}: [{index}]"
        if isinstance(item, str):
            out.append(entry(item, "", where))
        elif isinstance(item, dict):
            out.append(entries_from_spec_item(item, where))
        else:
            raise BadInput(f"{where}: entry is neither a name nor an object")
    return out


def load_dead(path):
    text = read_text(path)
    stripped = text.lstrip()
    if stripped.startswith(JSON_LEAD):
        data = parse_json(text, path)
        if isinstance(data, list):
            dead = entries_from_list(data, path)
        elif isinstance(data, dict) and isinstance(data.get("items"), list):
            dead = entries_from_list(data["items"], path)
        elif isinstance(data, dict) and isinstance(data.get("dead", data.get("seats")), list):
            dead = entries_from_list(data.get("dead", data.get("seats")), path)
        else:
            raise BadInput(f"{path}: JSON has no \"items\", \"dead\" or \"seats\" list")
    else:
        dead = []
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            where = f"{path}:{number}"
            name = line.split("\t", 1)[0].strip()
            if re.search(r"\s", name):
                raise BadInput(f"{where}: seat name {name!r} contains whitespace; "
                               f"use NAME<tab>field=value text lines, or a JSON list")
            found = FIELD_TARGET.search(line)
            dead.append(entry(name, found.group(1).strip() if found else "", where))
    if not dead:
        raise BadInput(f"{path}: dead-seat list is empty")
    return dead


def load_spec(path):
    data = parse_json(read_text(path), path)
    if not isinstance(data, dict):
        raise BadInput(f"{path}: top level is not a JSON object")
    items = data.get("items")
    if not isinstance(items, list):
        raise BadInput(f"{path}: no \"items\" list")
    if not items:
        raise BadInput(f"{path}: \"items\" list is empty")
    return [entries_from_spec_item(item, f"{path}: items[{index}]")
            for index, item in enumerate(items)]


def norm_name(name):
    return NON_NAME.sub("", name.lower())


def tokens_of(target):
    return set(TOKEN.findall(target.lower())) if target.strip() else set()


def jaccard(left, right):
    if not left or not right:
        return None
    return len(left & right) / len(left | right)


def variant(score):
    return "-" if score is None else f"{score:.2f}"


def evaluate(dead, items, threshold):
    """One flag line per item that reuses a dead name or repeats a dead target."""
    by_name = {}
    for seat in dead:
        by_name.setdefault(norm_name(seat["name"]), seat)
    dead_tokens = [(seat, tokens_of(seat["target"])) for seat in dead]
    lines = []
    for item in sorted(items, key=lambda it: it["name"]):
        pool = tokens_of(item["target"])
        named = by_name.get(norm_name(item["name"]))
        named_score = jaccard(pool, tokens_of(named["target"])) if named else None
        best_score, best_seat = None, None
        for seat, seat_tokens in dead_tokens:
            score = jaccard(pool, seat_tokens)
            if score is not None and score >= threshold and (best_score is None or score > best_score):
                best_score, best_seat = score, seat
        if named is not None:
            similar = named_score is not None and named_score >= threshold
            reason = "name-reuse+target-similar" if similar else "name-reuse"
            lines.append(f"FLAG item={item['name']} dead={named['name']} reason={reason} "
                         f"jaccard={variant(named_score)}")
        elif best_seat is not None:
            lines.append(f"FLAG item={item['name']} dead={best_seat['name']} reason=target-similar "
                         f"jaccard={variant(best_score)}")
    return lines


def run(argv):
    parser = argparse.ArgumentParser(
        prog="dead-seat-check.py",
        description="Flag new wave items that reuse a dead seat's name or repeat its target work.")
    parser.add_argument("--dead", metavar="PATH", help="dead-seat list: prior wave spec, JSON list or text list")
    parser.add_argument("--spec", metavar="PATH", help="new wave spec JSON with an \"items\" list")
    parser.add_argument("--min-jaccard", type=float, default=MIN_JACCARD, metavar="F",
                        help=f"target token-Jaccard threshold (default {MIN_JACCARD})")
    parser.add_argument("--selftest", action="store_true", help="run the built-in rule checks and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.dead is None or args.spec is None:
        print("DEAD_SEAT_CHECK_ERROR: --dead and --spec are required", file=sys.stderr)
        return 2
    if not 0.0 < args.min_jaccard <= 1.0:
        print(f"DEAD_SEAT_CHECK_ERROR: --min-jaccard {args.min_jaccard} outside (0, 1]", file=sys.stderr)
        return 2
    try:
        dead = load_dead(args.dead)
        items = load_spec(args.spec)
    except BadInput as exc:
        print(f"DEAD_SEAT_CHECK_ERROR: {exc}", file=sys.stderr)
        return 2

    lines = evaluate(dead, items, args.min_jaccard)
    for line in lines:
        print(line)
    print(f"DEAD_SEAT_CHECK: dead={len(dead)} items={len(items)} flagged={len(lines)} "
          f"threshold={args.min_jaccard:.2f}", file=sys.stderr)
    return 1 if lines else 0


def selftest():
    """Exercise every rule and exit path on temporary real files; no network, no repo."""
    failures = []
    ran = 0

    def record(name, ok, detail=""):
        if not ok:
            failures.append(f"{name}: {detail}")

    def check(name, argv, want_exit, want_lines):
        nonlocal ran
        ran += 1
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            got = run(argv)
        record(name, got == want_exit, f"exit {got} != {want_exit}")
        record(name + "/stdout", out.getvalue().splitlines() == want_lines,
               f"stdout {out.getvalue().splitlines()!r} != {want_lines!r}")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        def write(name, text):
            path = root / name
            path.write_text(text, encoding="utf-8")
            return str(path)

        def score(left, right):
            return variant(jaccard(tokens_of(left), tokens_of(right)))

        def line(item, dead_name, reason, value):
            return f"FLAG item={item} dead={dead_name} reason={reason} jaccard={value}"

        copy_a = ("# Target\nCount every row of the tally, print one line per leg, and report at x.md.\n"
                  "# Acceptance\nlisted\n")
        copy_b = ("# Target\nCount every row of the tally, print one line per leg, and report at y.md.\n"
                  "# Acceptance\nlisted\n")
        far = "# Target\nRead docs/quality.md and quote the third paragraph verbatim.\n# Acceptance\nquoted\n"
        spec_two = write("spec-two.json", json.dumps({"items": [
            {"name": "SeatCopy", "prompt": copy_b},
            {"name": "SeatFar", "prompt": far},
        ]}))
        spec_clean = write("spec-clean.json", json.dumps({"items": [
            {"name": "FreshName", "prompt": far},
        ]}))

        dead_same_name = write("dead-same-name.json",
                               json.dumps([{"name": "seat_copy", "target": target_of(copy_a)}]))
        check("name-reuse+target", ["--dead", dead_same_name, "--spec", spec_two], 1,
              [line("SeatCopy", "seat_copy", "name-reuse+target-similar",
                    score(target_of(copy_a), target_of(copy_b)))])

        dead_json = write("dead.json", json.dumps([{"name": "seata", "target": target_of(copy_a)}]))
        check("clean", ["--dead", dead_json, "--spec", spec_clean], 0, [])

        dead_copy = write("dead-copy.json", json.dumps([{"name": "SeatA", "target": target_of(copy_a)}]))
        check("target-copy", ["--dead", dead_copy, "--spec", spec_two], 1,
              [line("SeatCopy", "SeatA", "target-similar",
                    score(target_of(copy_a), target_of(copy_b)))])

        boundary = write("dead-boundary.json", json.dumps([{"name": "Low", "target": "alpha beta gamma"}]))
        spec_five = write("spec-five.json", json.dumps({"items": [
            {"name": "Elsewhere", "prompt": "# Target\nalpha beta gamma delta epsilon"},
        ]}))
        spec_seven = write("spec-seven.json", json.dumps({"items": [
            {"name": "Elsewhere", "prompt": "# Target\nalpha beta gamma delta epsilon zeta eta"},
        ]}))
        check("boundary-inclusive", ["--dead", boundary, "--spec", spec_five], 1,
              [line("Elsewhere", "Low", "target-similar", "0.60")])
        check("below-threshold", ["--dead", boundary, "--spec", spec_seven], 0, [])
        check("above-threshold", ["--dead", boundary, "--spec", spec_seven, "--min-jaccard", "0.4"], 1,
              [line("Elsewhere", "Low", "target-similar",
                    score("alpha beta gamma", "alpha beta gamma delta epsilon zeta eta"))])

        dead_spec = write("dead-spec.json", json.dumps({"items": [{"name": "SeatA", "prompt": copy_a}]}))
        check("dead-from-spec", ["--dead", dead_spec, "--spec", spec_two], 1,
              [line("SeatCopy", "SeatA", "target-similar",
                    score(target_of(copy_a), target_of(copy_b)))])

        dead_text = write("dead.txt", "# round dead seats\n\nSeatA\ttranscript=x\tbytes=1\treport_file=absent\n"
                                      "SeatB\ttarget=alpha beta gamma delta\treport_file=absent\n")
        check("dead-text", ["--dead", dead_text, "--spec", spec_two], 0, [])
        check("dead-text=target", ["--dead", dead_text, "--spec", spec_five, "--min-jaccard", "0.5"], 1,
              [line("Elsewhere", "SeatB", "target-similar", score("alpha beta gamma delta",
                                                                 "alpha beta gamma delta epsilon"))])

        bad_spec = write("bad-spec.json", json.dumps({"items": []}))
        bad_json = write("bad.json", "{not json")
        nameless = write("nameless.json", json.dumps({"items": [{"prompt": far}]}))
        empty_dead = write("empty-dead.txt", "# only a comment\n")
        bad_text = write("bad-text.txt", "SeatOne target text without a tab separator\n")
        bad_bytes = root / "bad-bytes.json"
        bad_bytes.write_bytes(b'{"items": [\xff\xfe]}')
        for name, argv in [
            ("non-utf8", ["--dead", dead_json, "--spec", str(bad_bytes)]),
            ("space-in-name", ["--dead", bad_text, "--spec", spec_clean]),
            ("empty-items", ["--dead", dead_json, "--spec", bad_spec]),
            ("bad-json", ["--dead", bad_json, "--spec", spec_clean]),
            ("nameless-item", ["--dead", dead_json, "--spec", nameless]),
            ("empty-dead", ["--dead", empty_dead, "--spec", spec_clean]),
            ("missing-file", ["--dead", str(root / "nope.txt"), "--spec", spec_clean]),
            ("bad-threshold", ["--dead", dead_json, "--spec", spec_clean, "--min-jaccard", "0"]),
        ]:
            check(name, argv, 2, [])

    if failures:
        for failure in failures:
            print(f"SELFTEST FAIL {failure}", file=sys.stderr)
        print(f"DEAD_SEAT_CHECK_SELFTEST: fail={len(failures)}", file=sys.stderr)
        return 1
    print(f"DEAD_SEAT_CHECK_SELFTEST: ok={ran}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
