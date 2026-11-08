# case_d — a class attribute named returncode on a non-runner value
class X:
    returncode = 0


def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    x = X()
    add("x", x.returncode, "b", 0)


main()
