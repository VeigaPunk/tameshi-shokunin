# case_g — committed form is a constant; the worktree is edited afterwards (never committed)
def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    add("x", 0, "b", 0)


main()
