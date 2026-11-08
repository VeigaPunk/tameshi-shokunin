import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    p = subprocess.run(["true"])
    rc = p.returncode
    rc += 7
    add("augassign", rc, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
