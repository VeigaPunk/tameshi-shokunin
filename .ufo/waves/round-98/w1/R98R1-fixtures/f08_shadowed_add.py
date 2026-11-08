import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def add(name, code, body, want_code):
    RECORDED.append((name, 0, body, want_code))


def main():
    p = subprocess.run(["true"])
    add("shadowed", p.returncode, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
