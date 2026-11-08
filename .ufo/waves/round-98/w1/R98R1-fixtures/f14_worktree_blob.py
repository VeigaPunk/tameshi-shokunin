import subprocess


def add(name, code, body, want_code):
    pass


def main():
    p = subprocess.run(["true"])
    add("worktree-blob", p.returncode, "body", 0)
