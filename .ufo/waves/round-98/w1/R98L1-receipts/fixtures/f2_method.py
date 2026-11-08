"""Blind-spot fixture: the recorder is a method (`rec.add(...)`), not a bare name.

The audit's site selector requires `ast.Name` with id "add", so an attribute call is
invisible even though the method is literally named `add`.
"""


class Recorder:
    def __init__(self):
        self.items = []

    def add(self, name, code, body, want):
        self.items.append((name, code, body, want))


def main():
    rec = Recorder()
    rec.add("method-literal", 0, "nothing measured", 0)
    rec.add("method-measured", 1, "nothing measured either", 1)


if __name__ == "__main__":
    main()
