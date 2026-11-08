import subprocess


class Result(subprocess.CompletedProcess):
    pass


def add(name, code, body, want_code):
    pass


def main():
    p = Result(["true"], 0)
    add("subclass", p.returncode, "body", 0)
