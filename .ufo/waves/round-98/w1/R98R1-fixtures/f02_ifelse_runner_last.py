import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main(c):
    if c:
        rc = 7
    else:
        p = subprocess.run(["true"])
        rc = p.returncode
    add("ifelse", rc, "body", 0)


if __name__ == "__main__":
    import sys
    main(len(sys.argv) > 1)
    print(RECORDED)
