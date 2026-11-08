"""Control fixture: a loop whose recorded code is a literal still fails the audit.

Shows the loop handling is not blind: the loop variable only labels the site, the code
argument is classified and a constant is `literal` (one site, exit 1).
"""


def main():
    def add(name, code, body, want):
        return (name, code)

    for name in ("loop-a", "loop-b", "loop-c"):
        add(name, 0, "cannot fail", 0)


if __name__ == "__main__":
    main()
