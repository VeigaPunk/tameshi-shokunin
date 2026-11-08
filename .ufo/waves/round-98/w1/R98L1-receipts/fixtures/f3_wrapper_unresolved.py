"""Blind-spot fixture: the driver registers through a wrapper around `add`.

Two runtime states; the only static `add(...)` site is the wrapper's body, whose code
argument is the parameter `code` (no assignment anywhere before that line), so the
audit reports one unresolved site and exits 1 -- the recorded codes at the two call
sites are never classified.
"""


def run(argv):
    return 1, "out"


def main():
    def add(name, code, body, want):
        return (name, code)

    def rec(name, code, body, want):
        add(name, code, body, want)

    code, out = run(["true"])
    rec("wrapped-measured", code, out, 0)
    rec("wrapped-literal", 0, "cannot fail", 0)


if __name__ == "__main__":
    main()
