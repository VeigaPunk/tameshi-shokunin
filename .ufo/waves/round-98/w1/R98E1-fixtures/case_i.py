# case_i — one add call site inside a loop
def run(argv):
    return 1, "o"


def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    for n in ("a", "b"):
        code, out = run(["x"])
        add(n, code, "b", 0)


main()
