#!/usr/bin/env python3
"""Round-99 C2 fixture (never executed): a control driver that registers two of its
four states through a renamed recorder. One aliased state is literal-coded, the
round-97 D-2 defect class moved behind an alias. The round-98 audit counts only the
two bare `add(...)` sites; the round-99 audit counts all four."""
import subprocess

STATES = []


def add(name, code, body, want):
    STATES.append((name, code, body, want))


record = add


def sh(argv):
    return subprocess.run(argv, capture_output=True)


def main():
    p = sh(["git", "grep", "-c", "TOKEN"])
    add("bare-measured", p.returncode, p.stdout, 1)
    q = sh(["true"])
    add("bare-measured-2", q.returncode, q.stdout, 0)
    r = sh(["git", "grep", "-c", "OTHER"])
    record("alias-measured", r.returncode, r.stdout, 1)
    record("alias-literal", 0, b"", 0)


if __name__ == "__main__":
    main()
