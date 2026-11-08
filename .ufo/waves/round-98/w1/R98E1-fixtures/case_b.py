# case_b — constant bound through a name
def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    rc = 0
    add("x", rc, "b", 0)


main()
