# case_k1 — the site's `p` is Result(0); a nested function defined earlier in the
# file also binds `p` from subprocess.run. That binding never reaches the site's scope.
import subprocess


class Result:
    def __init__(self, rc):
        self.returncode = rc


def add(name, code, body, want_code):
    print("RECORD name=%s code=%r want=%r" % (name, code, want_code))


def main():
    p = Result(0)
    def helper():
        p = subprocess.run(["/usr/bin/true"])
        return p
    add("scope-shadowed-constant", p.returncode, "body", 1)


main()
