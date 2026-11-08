# case_j — attribute overwritten from a runner after construction (static chain stays non-runner)
import subprocess


class P:
    returncode = None


def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    p = P()
    p.returncode = subprocess.run(["/bin/true"]).returncode
    add("x", p.returncode, "b", 0)


main()
