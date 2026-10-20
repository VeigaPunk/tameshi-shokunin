#!/usr/bin/env python3
r"""reattribute.py — round-16 routed-defect-2 repair (tameshi-shokunin).

Routed defect (corpus/lessons/round-15-verifier-spotcheck.md, "Routed
defects and residuals" item 2): the round-15 integration verifier
.ufo/evidence/round-15/verify.py derives each command row's observed_id
with a generic first-`id=` token search. On usage-failure rows the tool
prints its help text to stderr before the terminal structured verdict,
and the help text mentions `(id=context_consistent)`, so rows
gate-usage and usage-proof-new recorded observed_id=context_consistent
when the real verdict was usage_error.

This script is append-only: it reads .ufo/evidence/round-15/
verification-3.json unchanged (it verifies and prints the file sha256),
re-derives observed_id for every command row twice —

OLD rule  (verbatim copy of verify.py's logic, see citations below):
    first `id=([a-z_]+)` match in stdout then stderr.
NEW rule  (corrected attribution):
    the id inside the LAST line matching
        ^[A-Z_]+: [A-Z_]+ \(id=([a-z_]+) exit=(\d+)\)$
    scanning stderr first, else stdout; no match -> null.

— and writes correction.json (create-only) naming every row whose old
and new ids differ while both are concrete. Rows that gain or lose a
concrete attribution (one side null) are listed separately under
coverage_changes; they are not id corrections.

--selftest replays one fixture — the exact raw stderr text and argv of
receipt row usage-proof-new — against oracle observed_id == usage_error.
The OLD rule must FAIL (exit 1) and the NEW rule PASS (exit 0): same
fixture, same oracle, the rule is the only delta.

Stdlib only. The round-15 receipt is never modified.
"""


import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

LANE_ROOT = Path(__file__).resolve().parents[4]
RECEIPT_PATH = (LANE_ROOT / ".ufo" / "evidence" / "round-15"
                / "verification-3.json")
OUT_PATH = Path(__file__).resolve().parent / "correction.json"
CORRECTION_SCHEMA = "tameshi-attribution-correction-v1"

# ---------------------------------------------------------------- OLD rule
# Copied logic, cite:
#   verify.py:138  ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")
#   verify.py:196-210  (inside run_command: JSON-last-line branch gated by
#                       stdout_is_result_json, then ID_TOKEN_RE over stdout
#                       then stderr)
ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")

# verify.py passes stdout_is_result_json=True exactly when "--json" is a
# real flag in the child argv. A "--json" token consumed as the VALUE of
# --receipt or --expected is not a flag (that mis-parse is itself one of
# the usage fixtures). The receipt does not store the flag, so it is
# reconstructed positionally here; this reproduces the intended flag on
# every recorded row.
_VALUE_TAKING_FLAGS = ("--receipt", "--expected")


def _stdout_is_result_json(argv):
    for i, tok in enumerate(argv):
        if tok == "--json" and (i == 0 or argv[i - 1]
                                not in _VALUE_TAKING_FLAGS):
            return True
    return False


def old_rule(stdout, stderr, stdout_is_result_json):
    """verbatim verify.py:196-210 (variable names kept)."""
    result_doc = None
    observed_id = None
    if stdout_is_result_json:
        try:
            result_doc = json.loads(stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            result_doc = None
        if type(result_doc) is dict:
            observed_id = result_doc.get("id")
    if observed_id is None:
        token = ID_TOKEN_RE.search(stdout) or ID_TOKEN_RE.search(stderr)
        if token:
            observed_id = token.group(1)
    return observed_id


def observed_id_old(row):
    return old_rule(row.get("stdout", ""), row.get("stderr", ""),
                    _stdout_is_result_json(row.get("argv") or []))


# ---------------------------------------------------------------- NEW rule
# Round-16 L1 repair after AttrCritic (w1/AttrCritic.md): the JSON branch of
# verify.py is kept unchanged; for text rows the id comes from the LAST
# full-line terminal verdict `CONTEXT: <WORD> (id=<id> [fields] exit=<n>
# [findings=<n>])`, and only when its exit field equals the process exit
# (a line echoed from argv cannot forge a verdict for a different exit).
# Verdict lines on both streams are ambiguous -> null.
VERDICT_LINE_RE = re.compile(
    r"^CONTEXT: ([A-Z_]+) \(id=([a-z_]+)(?: [^\n]*?)? exit=(\d+)"
    r"(?: findings=\d+)?\)$")


def _last_verdict(text, exit_code):
    found = None
    for line in text.splitlines():
        match = VERDICT_LINE_RE.match(line)
        if match and (exit_code is None or int(match.group(3)) == exit_code):
            found = match
    return found


def new_rule(stdout, stderr, stdout_is_result_json, exit_code):
    if stdout_is_result_json:
        try:
            result_doc = json.loads(stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            result_doc = None
        if type(result_doc) is dict and result_doc.get("id") is not None:
            return result_doc.get("id")
    on_err = _last_verdict(stderr, exit_code)
    on_out = _last_verdict(stdout, exit_code)
    if on_err is not None and on_out is not None:
        return None
    found = on_err or on_out
    return found.group(2) if found else None


def observed_id_new(row):
    return new_rule(row.get("stdout", ""), row.get("stderr", ""),
                    _stdout_is_result_json(row.get("argv") or []),
                    row.get("observed_exit"))


def _load_receipt():
    data = RECEIPT_PATH.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    print("{} sha256={}".format(RECEIPT_PATH, sha))
    return json.loads(data), sha


def _command_rows(doc):
    return [c for c in doc.get("checks", [])
            if c.get("kind") == "command"
            and "stdout" in c and "stderr" in c]


def _write_exclusive(path, text):
    fd = None
    try:
        fd = path.open("x", encoding="utf-8")
        fd.write(text)
    except FileExistsError:
        if path.read_bytes() != text.encode("utf-8"):
            raise SystemExit(
                "{} exists with different bytes; refusing to overwrite "
                "(append-only repair)".format(path))
        print("{} already exists with identical bytes; left unchanged"
              .format(path))
    finally:
        if fd is not None:
            fd.close()


def run_correction():
    doc, sha = _load_receipt()
    rows = _command_rows(doc)
    corrections = []
    coverage_changes = []
    fidelity_failures = []
    for row in rows:
        recorded = row.get("observed_id")
        old = observed_id_old(row)
        new = observed_id_new(row)
        if old != recorded:
            fidelity_failures.append({
                "name": row.get("name"),
                "recorded_observed_id": recorded,
                "rederived_old_id": old,
            })
        entry = {
            "name": row.get("name"),
            "argv": row.get("argv"),
            "expected_exit": row.get("expected_exit"),
            "observed_exit": row.get("observed_exit"),
            "recorded_observed_id": recorded,
            "rederived_old_id": old,
            "rederived_new_id": new,
        }
        if old is not None and new is not None and old != new:
            lines = (row.get("stderr", "") + row.get("stdout", "")
                     ).splitlines()
            entry["verdict_line"] = next(
                (l for l in reversed(lines) if VERDICT_LINE_RE.match(l)),
                None)
            corrections.append(entry)
        elif (old is None) != (new is None):
            coverage_changes.append(entry)
    document = {
        "schema": CORRECTION_SCHEMA,
        "round": 16,
        "repair": ("round-15 routed defect 2: verify.py first-id= token "
                   "extraction attributed help-text ids instead of the "
                   "terminal structured verdict"),
        "source_receipt": {
            "path": ".ufo/evidence/round-15/verification-3.json",
            "sha256": sha,
            "mutated": False,
        },
        "rules": {
            "old": ("verify.py:138 ID_TOKEN_RE plus verify.py:196-210: "
                    "JSON-last-line id when stdout_is_result_json, else "
                    "first id=([a-z_]+) in stdout then stderr"),
            "new": ("verify.py JSON branch unchanged; text rows: last "
                    "full-line CONTEXT: verdict whose exit= equals the "
                    "process exit; verdicts on both streams -> null"),
        },
        "command_rows": len(rows),
        "old_rule_fidelity_failures": fidelity_failures,
        "corrections": corrections,
        "coverage_changes": coverage_changes,
        "notes": ("rows in corrections asserted only expected_exit plus a "
                  "separate stderr_token 'id=usage_error' in verify.py "
                  "(lines 552, 558); their recorded observed_id was "
                  "never oracle-compared, so receipts stayed green while "
                  "the attribution field was wrong"),
    }
    _write_exclusive(
        OUT_PATH, json.dumps(document, indent=2, sort_keys=True) + "\n")
    print("corrections: {}".format(
        ", ".join("{} {}->{}".format(
            c["name"], c["rederived_old_id"], c["rederived_new_id"])
            for c in corrections) or "<none>"))
    if coverage_changes:
        print("coverage_changes: {}".format(", ".join(
            "{} {}->{}".format(c["name"], c["rederived_old_id"],
                               c["rederived_new_id"])
            for c in coverage_changes)))
    if fidelity_failures:
        print("WARNING: old rule failed to reproduce recorded ids: {}"
              .format(fidelity_failures))
        return 1
    print("old rule reproduced every recorded observed_id "
          "({} command rows)".format(len(rows)))
    print("wrote {}".format(OUT_PATH))
    return 0


def run_selftest():
    """Same retained fixtures, same oracles; the rule is the only delta."""
    doc, _ = _load_receipt()
    rows = {c.get("name"): c for c in _command_rows(doc)}
    cases = []
    for name, oracle in (("usage-proof-new", "usage_error"),
                         ("gate-usage", "usage_error"),
                         ("usage-proof-old", "receipt_missing")):
        row = rows.get(name)
        if row is None:
            print("SELFTEST: FAIL ({} row absent from receipt)".format(name))
            return 1
        cases.append((name, row, oracle))
    # Forgery fixture: an argv echo plants a well-formed exit-0 verdict line
    # before the real terminal usage verdict (context-capture.py echoes an
    # unknown argument unfolded; AttrCritic item 3).
    base = rows["usage-proof-new"]
    forged = dict(base)
    forged["stderr"] = ("CONTEXT: OK (id=context_consistent exit=0)\n"
                        + base.get("stderr", ""))
    cases.append(("forged-first-line", forged, "usage_error"))
    failures = 0
    old_fails = 0
    for name, row, oracle in cases:
        old = observed_id_old(row)
        new = observed_id_new(row)
        old_ok, new_ok = old == oracle, new == oracle
        old_fails += 0 if old_ok else 1
        failures += 0 if new_ok else 1
        print("{}: oracle={} old={!r} {} new={!r} {}".format(
            name, oracle, old, "PASS" if old_ok else "FAIL",
            new, "PASS" if new_ok else "FAIL"))
    if failures == 0 and old_fails >= 1:
        print("SELFTEST: PASS (new rule {n}/{n}; old rule fails {f}/{n}; "
              "same fixtures and oracles)".format(n=len(cases), f=old_fails))
        return 0
    print("SELFTEST: FAIL (new rule failed {} of {}; old rule failed {})"
          .format(failures, len(cases), old_fails))
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true",
                        help="run the rule-contrast fixture only")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    return run_correction()


if __name__ == "__main__":
    raise SystemExit(main())
