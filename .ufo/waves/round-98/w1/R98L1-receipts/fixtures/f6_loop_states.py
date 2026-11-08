"""Scale fixture: three runtime states registered from ONE static `add(...)` site.

Every recorded code is a genuine runner measurement, but the audit's site count (1) is a
lower bound on the state set (3), and the site label is lost ("?").
"""


def run(argv):
    return 1, "out"


def main():
    def add(name, code, body, want):
        return (name, code)

    for name in ("loop-a", "loop-b", "loop-c"):
        code, out = run([name])
        add(name, code, out, 0)


if __name__ == "__main__":
    main()
