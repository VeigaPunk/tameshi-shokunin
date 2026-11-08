# case_k2 — same as k1 but the nested function (and its `p` assignment) appears
# after the add call, so the last assignment before the call is `p = Result(0)`.
import subprocess


class Result:
    def __init__(self, rc):
        self.returncode = rc


def add(name, code, body, want_code):
    print("RECORD name=%s code=%r want=%r" % (name, code, want_code))


def main():
    p = Result(0)
    add("scope-shadowed-constant", p.returncode, "body", 1)
    def helper():
        p = subprocess.run(["/usr/bin/true"])
        return p


main()
