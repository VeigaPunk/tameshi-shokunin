#!/usr/bin/env python3
"""Two-edit diagnostic (not a matrix row): GIT bare + PATH pin removed.

Shows whether the hostile shim is reachable once the sealed PATH pin is also
removed, i.e. that the pin is the measured mechanism behind R97L1-6's
identical result.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import independent as I  # noqa: E402


def main():
    I.ensure_checker()
    src = open(I.CHECKER, "rb").read()
    base = os.path.join(I.HERE, "work", "diag-two-edit")
    import shutil
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    spec = I.state_hostile(base)
    repo, rev = I.build_fixture(base, spec["rows"], spec["receipts"],
                                spec.get("claims_sha"), spec.get("worktree"))
    one = src.replace(b'GIT = "/usr/bin/git"', b'GIT = "git"', 1)
    two = one.replace(b'"PATH": "/usr/local/bin:/usr/bin:/bin"',
                      b'"PATH": os.environ["PATH"]', 1)
    assert two != one, "PATH anchor not found"
    p1 = os.path.join(base, "checker-one-edit.py")
    p2 = os.path.join(base, "checker-two-edit.py")
    open(p1, "wb").write(one)
    open(p2, "wb").write(two)
    env = I.env_base(spec["env_override"])
    for tag, path in (("pristine", I.CHECKER), ("one-edit", p1), ("two-edit", p2)):
        rc, out = I.run_checker(path, repo, rev, [], env)
        print("DIAG %s exit=%d" % (tag, rc))
        print("".join("  " + ln + "\n" for ln in out.strip().splitlines()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
