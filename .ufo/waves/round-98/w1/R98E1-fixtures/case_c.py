# case_c — returncode of subprocess.run
import subprocess


def add(name, code, body, want_code):
    print(name, code, body, want_code)


def main():
    p = subprocess.run(["/bin/true"])
    add("x", p.returncode, "b", 0)


main()
