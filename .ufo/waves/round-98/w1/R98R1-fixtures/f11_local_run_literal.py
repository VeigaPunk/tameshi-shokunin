RECORDED = []


def run(cmd):
    return 0, ""


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    code, out = run(["git", "grep", "-c", "GUARD_INERTIA"])
    add("literal-via-local-run", code, "body", 1)


if __name__ == "__main__":
    main()
    print(RECORDED)
