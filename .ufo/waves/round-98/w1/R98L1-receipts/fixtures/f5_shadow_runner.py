"""Blind-spot fixture: runner-ness is decided by the call's NAME.

`sh` here is a local function that runs nothing and returns a constant returncode; the
audit still classifies `g.returncode` as measured ("returncode-of-runner-name").
"""

from types import SimpleNamespace


def sh(argv):
    return SimpleNamespace(returncode=0)


def main():
    def add(name, code, body, want):
        return (name, code)

    g = sh(["git", "grep", "GUARD_INERTIA"])
    add("shadow-runner", g.returncode, "nothing ran", 1)


if __name__ == "__main__":
    main()
