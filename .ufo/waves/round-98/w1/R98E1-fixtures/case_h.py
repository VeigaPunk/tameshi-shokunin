# case_h — constant bound through a two-name chain
def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    zero = 0
    rc = zero
    add("x", rc, "b", 0)


main()
