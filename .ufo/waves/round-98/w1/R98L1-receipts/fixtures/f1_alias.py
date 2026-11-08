"""Blind-spot fixture: the recorder is aliased, so no call is named `add`.

One runtime state, recorded code is the literal 0 (cannot fail whatever it wraps).
The audit should report WHO this is; it reports zero sites and exits 0.
"""


def main():
    def add(name, code, body, want):
        return (name, code)

    record = add
    record("alias-literal", 0, "nothing measured", 0)


if __name__ == "__main__":
    main()
