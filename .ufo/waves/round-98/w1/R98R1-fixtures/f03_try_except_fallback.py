import subprocess

RECORDED = []


def add(name, code, body, want_code):
    RECORDED.append((name, code, body, want_code))


def main():
    try:
        p = subprocess.run(["true"])
        rc = p.returncode
    except Exception:
        rc = 7
    add("try-fallback", rc, "body", 0)


if __name__ == "__main__":
    main()
    print(RECORDED)
