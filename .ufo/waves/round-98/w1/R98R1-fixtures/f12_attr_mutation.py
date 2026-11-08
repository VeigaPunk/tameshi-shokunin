import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    p = subprocess.run(["true"])
    p.returncode = 0
    add("mutated-attr", p.returncode, "body", 1)


if __name__ == "__main__":
    main()
    print(RECORDED)
