import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    rc = 7
    if False:
        p = subprocess.run(["true"])
        rc = p.returncode
    add("dead-branch", rc, "body", 1)


if __name__ == "__main__":
    main()
    print(RECORDED)
