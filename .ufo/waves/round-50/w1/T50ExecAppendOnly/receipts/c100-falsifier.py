#!/usr/bin/env python3
"""Mutation proof for seat-report-append-only.py (C1 falsifier evidence).

Builds a throw-away git fixture, checks the pristine checker on four cases,
then stages three broken copies of the checker and shows each one loses the
discrimination the pristine copy has:

  prefix-to-length  `new.startswith(old)` -> `len(new) >= len(old)`:
                    misses an in-place rewrite that grows the file.
  drop-deleted      the `target is None` branch stops reporting:
                    misses a deletion.
  widen-scope       `.ufo/waves/round-*` -> `.ufo/waves/`:
                    reports a non-round wave file as in scope.

Each staged mutant prints a ``FAIL `` line (its behaviour is wrong), and the
entry point prints ``CRITERION-100-FALSIFIER-OK`` only when the pristine
checker passes every case and all three mutants are caught as wrong.

usage: c100-falsifier.py CHECKER SCRATCH MUTANT_RECEIPT_DIR
exit: 0 falsifier holds, 1 it does not, 2 setup error
"""

import os
import shutil
import subprocess
import sys


def run(cmd, stdin_data=None):
    return subprocess.run(
        cmd, input=stdin_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def git(repo, *args):
    proc = run(["git", "-C", repo] + list(args))
    if proc.returncode != 0:
        raise SystemExit(
            "ERROR: git %s failed: %s"
            % (" ".join(args), proc.stderr.decode("utf-8", "replace").strip())
        )
    return proc.stdout.decode("utf-8", "replace").strip()


def commit(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def main(argv):
    if len(argv) != 4:
        sys.stderr.write(
            "usage: c100-falsifier.py CHECKER SCRATCH MUTANT_RECEIPT_DIR\n"
        )
        return 2
    checker, scratch, receipt_dir = argv[1], argv[2], argv[3]
    checker = os.path.realpath(checker)
    os.makedirs(scratch, exist_ok=True)
    os.makedirs(receipt_dir, exist_ok=True)

    with open(checker, encoding="utf-8") as handle:
        source = handle.read()
    mutations = {
        "prefix-to-length": (
            "            if not new.startswith(old):",
            "            if not len(new) >= len(old):",
        ),
        "drop-deleted": (
            '            if target is None:\n'
            '                violations.append((path, "deleted"))\n'
            "                continue\n",
            "            if target is None:\n"
            "                continue\n",
        ),
        "widen-scope": (
            'ROUND_FILE = re.compile(r"^\\.ufo/waves/round-[^/]+/")',
            'ROUND_FILE = re.compile(r"^\\.ufo/waves/")',
        ),
    }
    for name, (needle, _replacement) in mutations.items():
        if needle not in source:
            sys.stderr.write(
                "ERROR: mutation %s does not match the checker source\n" % name
            )
            return 2

    mutant_paths = {}
    manifest = []
    for name, (needle, replacement) in mutations.items():
        path = os.path.join(scratch, "mutant-%s.py" % name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(source.replace(needle, replacement, 1))
        mutant_paths[name] = path
        manifest.append(
            "== %s\n--- original\n%s\n--- mutant\n%s\n"
            % (name, needle, replacement)
        )
    with open(os.path.join(receipt_dir, "mutations.txt"), "w") as handle:
        handle.write("".join(manifest))

    fixture = os.path.join(scratch, "fixture")
    shutil.rmtree(fixture, ignore_errors=True)
    os.makedirs(fixture)
    git(fixture, "init", "-q")
    toplevel = git(fixture, "rev-parse", "--show-toplevel")
    if os.path.realpath(toplevel) != os.path.realpath(fixture):
        sys.stderr.write("ERROR: fixture toplevel is not the fixture dir\n")
        return 2
    git(fixture, "config", "user.email", "fixture@example.invalid")
    git(fixture, "config", "user.name", "fixture")
    print("setup toplevel verified: fixture")

    os.makedirs(os.path.join(fixture, ".ufo/waves/round-01"))
    os.makedirs(os.path.join(fixture, ".ufo/waves/other"))
    with open(os.path.join(fixture, ".ufo/waves/round-01/A.md"), "w") as fh:
        fh.write("# Seat report A\nline 1\nline 2\n")
    with open(os.path.join(fixture, ".ufo/waves/round-01/B.md"), "w") as fh:
        fh.write("# Seat report B\nline 1\n")
    with open(os.path.join(fixture, ".ufo/waves/other/n.md"), "w") as fh:
        fh.write("not a round artifact\n")
    c1 = commit(fixture, "c1: base")

    with open(os.path.join(fixture, ".ufo/waves/round-01/A.md"), "a") as fh:
        fh.write("appended line\n")
    c2 = commit(fixture, "c2: append")

    # Longer than FROM and prefix-lost: the length-only mutant is fooled.
    with open(os.path.join(fixture, ".ufo/waves/round-01/A.md"), "w") as fh:
        fh.write("# Seat report A\nline 1 CHANGED\nline 2\nappended line\n")
    c3 = commit(fixture, "c3: rewrite A in place, longer")

    git(fixture, "rm", "-q", ".ufo/waves/round-01/B.md")
    c4 = commit(fixture, "c4: delete B")

    with open(os.path.join(fixture, ".ufo/waves/other/n.md"), "w") as fh:
        fh.write("changed\n")
    c5 = commit(fixture, "c5: rewrite non-round file")

    def check(program, from_rev, to_rev, label):
        proc = run([sys.executable, program, fixture, from_rev, to_rev])
        out = proc.stdout.decode("utf-8", "replace")
        err = proc.stderr.decode("utf-8", "replace")
        with open(os.path.join(receipt_dir, label + ".stdout"), "w") as fh:
            fh.write(out)
        with open(os.path.join(receipt_dir, label + ".stderr"), "w") as fh:
            fh.write(err)
        with open(os.path.join(receipt_dir, label + ".exit"), "w") as fh:
            fh.write("%d\n" % proc.returncode)
        return proc.returncode, out

    cases = [
        ("append-r0", c1, c2, 0),
        ("rewrite-r1", c2, c3, 1),
        ("delete-r1", c3, c4, 1),
        ("non-round-r0", c4, c5, 0),
    ]
    ok = True
    for label, from_rev, to_rev, want in cases:
        got, out = check(checker, from_rev, to_rev, "pristine-" + label)
        verdict = "PASS" if got == want else "FAIL"
        if got != want:
            ok = False
        print("%s pristine %s exit=%d (want %d)" % (verdict, label, got, want))

    mutant_expectations = [
        ("prefix-to-length", "rewrite-r1", c2, c3, 1),
        ("drop-deleted", "delete-r1", c3, c4, 1),
        ("widen-scope", "non-round-r0", c4, c5, 0),
    ]
    recognised = 0
    for name, label, from_rev, to_rev, pristine_exit in mutant_expectations:
        got, out = check(mutant_paths[name], from_rev, to_rev, "mutant-" + name)
        if got != pristine_exit:
            recognised += 1
            print(
                "FAIL mutant=%s case=%s mutant_exit=%d pristine_exit=%d"
                % (name, label, got, pristine_exit)
            )
        else:
            ok = False
            print(
                "FAIL-NOT-DETECTED mutant=%s case=%s mutant_exit=%d"
                % (name, label, got)
            )

    print("fixture commits: c1=%s c2=%s c3=%s c4=%s c5=%s"
          % (c1[:8], c2[:8], c3[:8], c4[:8], c5[:8]))
    print("mutants recognised as wrong: %d/%d" % (recognised, len(mutant_expectations)))
    if ok and recognised == len(mutant_expectations):
        print("CRITERION-100-FALSIFIER-OK")
        return 0
    print("CRITERION-100-FALSIFIER-FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
