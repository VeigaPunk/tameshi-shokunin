import subprocess


def add(name, code, body, want_code):
    pass


def main():
    for n in ("a", "b"):
        p = subprocess.run(["true"])
        add(n, p.returncode, "body", 0)
        add(n + "-2", p.returncode, "body", 0)
