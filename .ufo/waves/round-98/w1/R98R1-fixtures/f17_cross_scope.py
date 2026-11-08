import subprocess


def add(name, code, body, want_code):
    pass


def helper():
    p = subprocess.run(["true"])


def main():
    add("cross-scope", p.returncode, "body", 0)
