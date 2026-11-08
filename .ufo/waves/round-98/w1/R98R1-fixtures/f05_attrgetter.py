import operator
import subprocess


def add(name, code, body, want_code):
    pass


def main():
    p = subprocess.run(["true"])
    rc = operator.attrgetter("returncode")(p)
    add("attrgetter", rc, "body", 0)
