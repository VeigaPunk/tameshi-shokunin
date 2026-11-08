"""Blind-spot fixture: a wrapper whose parameter name collides with a measured name.

The audit resolves names lexically, so the wrapper's `rc` parameter is resolved to the
enclosing function's `rc = g.returncode` (a runner call). The site is classified
measured -- but every runtime call passes the literal 0, so no recorded code can fail.
"""

import subprocess


def sh(argv):
    return subprocess.run(argv, capture_output=True, text=True)


def main():
    g = sh(["/bin/true"])
    rc = g.returncode

    def add(name, code, body, want):
        return (name, code)

    def rec(name, rc, body, want):
        add(name, rc, body, want)

    rec("wrapped-literal-a", 0, "cannot fail", 0)
    rec("wrapped-literal-b", 0, "cannot fail", 0)


if __name__ == "__main__":
    main()
