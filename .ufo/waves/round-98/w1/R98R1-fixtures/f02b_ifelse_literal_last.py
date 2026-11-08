import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main(c):
    if c:
        p = subprocess.run(["true"])
        rc = p.returncode
    else:
        rc = 7
    add("ifelse-swapped", rc, "body", 0)


if __name__ == "__main__":
    main(True)
    print(RECORDED)
