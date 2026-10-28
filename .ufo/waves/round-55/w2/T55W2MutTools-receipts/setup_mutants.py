#!/usr/bin/env python3
"""Build one commit per mutant on top of C0 in the scratch clone; print hashes+diffs."""
import json
import os
import subprocess

S = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(S, "mut")
BASE = "0a2010acd1e92e4e332774050825e21bcfc7e079"
C0 = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
RC = "tools/repeat-control.py"
CC = "tools/context-capture.py"
REG = "tools/registry-check.py"


def git(*args, check=True):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
    if check and p.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr))
    return p


def assert_toplevel():
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(REPO):
        raise SystemExit("toplevel is %r, expected %r" % (top, REPO))


def fresh(branch, rev=C0):
    assert_toplevel()
    git("checkout", "-q", "-B", branch, rev)
    assert_toplevel()


def edit(path, old, new, count=1):
    full = os.path.join(REPO, path)
    text = open(full, encoding="utf-8").read()
    n = text.count(old)
    if n != count:
        raise SystemExit("mutation anchor found %d time(s), want %d: %r" % (n, count, old[:80]))
    open(full, "w", encoding="utf-8").write(text.replace(old, new))


def commit(branch, msg, target_mode):
    assert_toplevel()
    git("add", "-A")
    assert_toplevel()
    git("commit", "-q", "-m", msg)
    sha = git("rev-parse", "HEAD").stdout.strip()
    return {"branch": branch, "rev": sha, "target_mode": target_mode,
            "stat": git("diff", "--stat", C0, sha).stdout.strip(),
            "diff": git("diff", C0, sha).stdout}


def main():
    git("config", "user.email", "wave2@localhost")
    git("config", "user.name", "T55W2MutTools")
    out = []

    # ---- 1-3: revert one tool's grammar line (the whole-file base revert is the
    # only base..C0 delta in each of these files).
    for branch, path, target in (("m-rc-revert", RC, "repeat-control --selftest"),
                                 ("m-cc-revert", CC, "context-capture --selftest"),
                                 ("m-reg-revert", REG, "registry-check --rev")):
        fresh(branch)
        assert_toplevel()
        git("checkout", BASE, "--", path)
        out.append(commit(branch, "mutant %s: revert %s to its base grammar line"
                          % (branch, path), target))

    # ---- 4: drop the value (the quoted TMPDIR) from the message.
    fresh("m-rc-drop-value")
    edit(RC,
         '"cannot create clone scratch under the scratch root: TMPDIR is not a usable '
         'directory: %r (could-not-evaluate)" % t)',
         '"cannot create clone scratch under the scratch root: TMPDIR is not a usable '
         'directory (could-not-evaluate)")')
    out.append(commit("m-rc-drop-value", "mutant: message drops the TMPDIR value",
                      "repeat-control --selftest"))

    # ---- 5: drop the trailing class token "(could-not-evaluate)".
    fresh("m-rc-drop-class")
    edit(RC, ': %r (could-not-evaluate)" % t)', ': %r" % t)')
    out.append(commit("m-rc-drop-class",
                      "mutant: message drops the (could-not-evaluate) class token",
                      "repeat-control --selftest"))

    # ---- 5b: drop the leading class label on the operator line.
    fresh("m-rc-drop-label")
    edit(RC, 'emit_err(f"repeat-control: could-not-evaluate: {message}")',
         'emit_err(f"repeat-control: {message}")')
    out.append(commit("m-rc-drop-label",
                      "mutant: operator line drops the could-not-evaluate label",
                      "repeat-control --selftest"))

    # ---- 6: the class line on stdout instead of stderr.
    fresh("m-rc-stdout")
    edit(RC, 'emit_err(f"repeat-control: could-not-evaluate: {message}")',
         'emit(f"repeat-control: could-not-evaluate: {message}")')
    out.append(commit("m-rc-stdout", "mutant: repeat-control class line on stdout",
                      "repeat-control --selftest"))

    fresh("m-cc-stdout")
    edit(CC, 'sys.stderr.write("context-capture.py: could-not-evaluate: {}\\n".format(exc))',
         'sys.stdout.write("context-capture.py: could-not-evaluate: {}\\n".format(exc))')
    out.append(commit("m-cc-stdout", "mutant: context-capture class line on stdout",
                      "context-capture --selftest"))

    fresh("m-reg-stdout")
    # Only the --rev path (inside the clone_lane_at_rev except block); the
    # --selftest print above it stays on stderr.
    edit(REG, '''        except ScratchRootUnusable as exc:
            # The class, not a verdict: one stderr line with the frozen grammar,
            # exit 2, and stdout carries no could-not-evaluate verdict (round 55).
            print(f"registry-check: could-not-evaluate: {exc}", file=sys.stderr)''',
         '''        except ScratchRootUnusable as exc:
            print(f"registry-check: could-not-evaluate: {exc}", file=sys.stdout)''')
    out.append(commit("m-reg-stdout",
                      "mutant: registry-check --rev class line on stdout",
                      "registry-check --rev"))

    # ---- 7: survivor probe: another tool's prefix on the class line.
    fresh("m-rc-wrong-prefix")
    edit(RC, 'emit_err(f"repeat-control: could-not-evaluate: {message}")',
         'emit_err(f"env-diff: could-not-evaluate: {message}")')
    out.append(commit("m-rc-wrong-prefix",
                      "mutant: repeat-control prints another tool's prefix",
                      "repeat-control --selftest"))

    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
