\
RECORDED = []


def run(cmd):
    return 0, ""


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    code, out = run(["git", "grep", "-c", "TOKEN-1"])
    add("fake-01", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-2"])
    add("fake-02", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-3"])
    add("fake-03", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-4"])
    add("fake-04", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-5"])
    add("fake-05", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-6"])
    add("fake-06", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-7"])
    add("fake-07", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-8"])
    add("fake-08", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-9"])
    add("fake-09", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-10"])
    add("fake-10", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-11"])
    add("fake-11", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-12"])
    add("fake-12", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-13"])
    add("fake-13", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-14"])
    add("fake-14", code, "body", 1)
    code, out = run(["git", "grep", "-c", "TOKEN-15"])
    add("fake-15", code, "body", 1)


if __name__ == "__main__":
    main()
    print(len(RECORDED), set(r[1] for r in RECORDED))
