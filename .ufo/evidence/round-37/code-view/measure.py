#!/usr/bin/env python3
"""Measure the frozen round-37 ANSI-C code-view predicate at committed bytes."""
import argparse
import hashlib
import os
import subprocess
import sys

EXPECTED = "C2_R37_PASS=true iff the ANSI-C escaped-quote trailing-comment fixture is fully blanked and the literal-hash fixture is byte-identical."


def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
    return env


def git(lane, *args):
    return subprocess.run(["git", "-C", lane, *args], env=git_env(), capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    resolved = git(lane, "rev-parse", "--verify", a.rev)
    if resolved.returncode:
        print("C2_R37: SETUP rev_unresolved=%s" % a.rev)
        return 2
    rev = resolved.stdout.decode().strip()
    source = git(lane, "show", "%s:tools/tally-audit-v3.py" % rev)
    if source.returncode:
        print("C2_R37: SETUP tool_missing_at_rev")
        return 2
    namespace = {"__name__": "tameshi_round37_code_view", "__file__": "tools/tally-audit-v3.py"}
    try:
        exec(compile(source.stdout, "tools/tally-audit-v3.py@" + rev, "exec"), namespace)
    except Exception as exc:
        print("C2_R37: SETUP tool_load_error=%s" % type(exc).__name__)
        return 2
    code_view = namespace.get("code_view")
    if not callable(code_view):
        print("C2_R37: SETUP code_view_missing")
        return 2

    text1 = ": $'it\\'s' # inert st_tsu=0\nst_tsu=9\n"
    hash1 = text1.index("#")
    line_end1 = text1.index("\n")
    want1 = text1[:hash1] + (" " * (line_end1 - hash1)) + text1[line_end1:]
    text2 = ": $'literal # data'\nst_tsu=9\n"
    cases = (("ansi-c-escaped-quote-trailing-comment", text1, want1),
             ("ansi-c-literal-hash", text2, text2))
    passed = 0
    for name, text, want in cases:
        got = code_view(text)
        ok = got == want and len(got) == len(text) and got.count("\n") == text.count("\n")
        passed += bool(ok)
        print("CASE %s %s" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            print("  expected=%r" % want)
            print("  actual=%r" % got)
    tool_sha = hashlib.sha256(source.stdout).hexdigest()
    ok = passed == len(cases)
    print("C2_R37: ansi_trailing_comment=%d/1 ansi_literal_hash=%d/1 tool_sha256=%s rev=%s C2_R37_PASS=%s"
          % (int(code_view(text1) == want1), int(code_view(text2) == text2), tool_sha, rev,
             "true" if ok else "false"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
