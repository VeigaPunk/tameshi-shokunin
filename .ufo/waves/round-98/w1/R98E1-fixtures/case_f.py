# case_f — two add definitions; the second shadows the first and ignores `code`
def run(argv):
    return 1, "o"


def add(name, code, body, want_code):
    print("FIRST", name, code, body, want_code)


def add(name, code, body, want_code):
    print("SECOND", name, body, want_code)


def main():
    code, out = run(["x"])
    add("x", code, "b", 0)


main()
