#!/usr/bin/env python3
"""tools/receipt-commit-bind.py — bind receipt names in commit messages to the
commit bytes that carry them (round 65; the r64 non-author closure's routed
defect 1 class, made checkable).

Convention of record (stated in `corpus/lessons/round-65.md`): a commit whose
message names receipt content must carry those receipt bytes; an empty commit
carries no content, so it can never satisfy a receipt claim made in its own
message (git's own words, S296: "Usually recording a commit that has the exact
same tree as its sole parent commit is a mistake" — the r64 tail commit
6876d746 is the landed instance of the class: its subject names the
tip-confirmation receipt, the bytes landed only in its successor c7d28b19).

Check (range sweep, git objects only — no worktree, no index):

  python -I tools/receipt-commit-bind.py --repo LANE --base REV --tip REV

For every path ADDED in the range base..tip under `.ufo/evidence/` (the
lane's evidence surface, `git diff-tree -r --diff-filter=A --name-only`),
for every commit C in base..tip (oldest first): if C's raw message (%B)
names the file, the file must exist in C's tree (`git ls-tree -r C -- path`,
non-empty = carried).

Name rule (disclosed, deterministic): the message names the file if it
contains the basename WITH extension, or contains the basename WITHOUT
extension as a delimited token (the characters immediately before and after
are outside [A-Za-z0-9-]); the bare token must be at least 8 characters long,
so generic short words never match.

Output:
  BIND_OK   <commit-short> carries <path>            (per naming-and-carrying commit)
  BIND_DEFECT <commit-short> names <token> -> <path> not carried at that commit
  RECEIPT_COMMIT_BIND: commits=N evidence=M named=K carried=K2 findings=F

Exit map: 0 = sweep ran, zero defects; 1 = sweep ran, defects found;
2 = usage/setup error, INCLUDING a range that adds no evidence file at all
(fail-closed: a vacuous pass is refused, an always-pass cheat has no input).

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only (hash-object / mktree / commit-tree / update-ref;
the index is never touched) and checks four arms:
  1. red/discrimination — an empty commit whose message names a receipt that
     a LATER commit carries (the 6876d746 shape) yields exactly that one
     BIND_DEFECT and exit 1;
  2. green — a commit that carries the receipt it names yields BIND_OK,
     zero findings, exit 0;
  3. vacuous guard — a range adding no evidence file exits 2;
  4. usage — missing required flags exit 2.
Arms 1 is the cheat-family discriminator: the always-pass cheat (never flag)
fails arm 1, and the real-history sweep on the lane (the r64 round range) is
the second, non-synthetic red arm recorded in the round receipts.
"""

import argparse
import re
import subprocess
import sys
import tempfile
import os

EVIDENCE_PREFIX = ".ufo/evidence/"
MIN_TOKEN = 8


def run(repo, *args, binary=False, inp=None, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       input=inp.encode() if isinstance(inp, str) else inp)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (
            " ".join(args[:3]), r.stderr.decode(errors="replace").strip()[:300]))
    return r.stdout if binary else r.stdout.decode(errors="replace")


def added_evidence_paths(repo, base, tip):
    out = run(repo, "diff-tree", "-r", "--diff-filter=A", "--name-only",
               base, tip)
    return [l for l in out.splitlines()
            if l.startswith(EVIDENCE_PREFIX)]


def commits_in_range(repo, base, tip):
    out = run(repo, "rev-list", "--reverse", base + ".." + tip)
    return [l for l in out.splitlines() if l]


def name_tokens(path):
    base = path.rsplit("/", 1)[-1]
    stem = base.rsplit(".", 1)[0] if "." in base else base
    tokens = {base}
    if len(stem) >= MIN_TOKEN:
        tokens.add(stem)
    return tokens


def message_names(message, token):
    if token in message:
        return True
    if len(token) < MIN_TOKEN:
        return False
    return re.search(r"(?<![A-Za-z0-9-])" + re.escape(token) +
                     r"(?![A-Za-z0-9-])", message) is not None


def carried(repo, commit, path):
    out = run(repo, "ls-tree", "-r", "--name-only", commit, "--", path,
              check=False)
    if out.strip() == "":
        return False
    return any(line.strip() == path for line in out.splitlines())


def sweep(repo, base, tip, out=sys.stdout):
    paths = added_evidence_paths(repo, base, tip)
    if not paths:
        out.write("RECEIPT_COMMIT_BIND error=empty-range "
                  "no evidence files added in %s..%s\n" % (base[:9], tip[:9]))
        return 2
    commits = commits_in_range(repo, base, tip)
    findings = 0
    named = 0
    carried_count = 0
    per_commit_msgs = {}
    for c in commits:
        per_commit_msgs[c] = run(repo, "show", "-s", "--format=%B", c)
    # pre-compute each path's carriers once (ls-tree per commit per path is
    # fine for round-sized ranges; dedupe by (commit, path) result cache)
    carry_cache = {}
    for c in commits:
        for p in paths:
            carry_cache[(c, p)] = carried(repo, c, p)
    for c in commits:
        short = c[:9]
        msg = per_commit_msgs[c]
        for p in paths:
            hit = None
            for tok in name_tokens(p):
                if message_names(msg, tok):
                    hit = tok
                    break
            if hit is None:
                continue
            named += 1
            if carry_cache[(c, p)]:
                carried_count += 1
                out.write("BIND_OK %s carries %s\n" % (short, p))
            else:
                findings += 1
                out.write("BIND_DEFECT %s names %s -> %s not carried at "
                          "that commit\n" % (short, hit, p))
    out.write("RECEIPT_COMMIT_BIND: commits=%d evidence=%d named=%d "
              "carried=%d findings=%d\n" %
              (len(commits), len(paths), named, carried_count, findings))
    return 1 if findings else 0


def _env():
    e = dict(os.environ)
    e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
    e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
    return e


def build_fixture(d):
    """Fixture repo: base -> C1 (empty, names foo-receipt) -> C2 (carries
    .ufo/evidence/win-host/foo-receipt.txt, names it). Returns
    (repo, base, tip)."""
    fx = os.path.join(d, "fx")
    os.makedirs(fx)
    run(fx, "init", "-q", ".")
    run(fx, "config", "user.email", "fx@fx")
    run(fx, "config", "user.name", "fx")

    def commit(tree, parents, msg):
        args = ["commit-tree", tree]
        for p in parents:
            args += ["-p", p]
        r = subprocess.run(["git", "-C", fx, *args, "-m", msg],
                           capture_output=True, env=_env(),
                           input=msg.encode())
        if r.returncode != 0:
            raise RuntimeError("commit-tree: %s" % r.stderr.decode()[:200])
        return r.stdout.decode().strip()

    empty_tree = run(fx, "mktree", inp="").strip()
    b1 = run(fx, "hash-object", "-w", "--stdin", inp="seed file\n",
             binary=False).strip()
    t1 = run(fx, "mktree", inp="100644 blob %s\tseed.txt\n" % b1).strip()
    base = commit(t1, [], "base")
    # C1: EMPTY commit (same tree as parent) naming a receipt it does not
    # carry — the 6876d746 shape.
    c1 = commit(t1, [base], "post-landing foo-receipt receipt (guard run)")
    # C2: carries the receipt under .ufo/evidence/win-host/ and names it.
    b2 = run(fx, "hash-object", "-w", "--stdin",
             inp="RECEIPT_EXISTS_SELFTEST: 4/4 pass\n", binary=False).strip()
    leaf = run(fx, "mktree", inp="100644 blob %s\tfoo-receipt.txt\n" % b2).strip()
    ev = run(fx, "mktree", inp="040000 tree %s\twin-host\n" % leaf).strip()
    evr = run(fx, "mktree", inp="040000 tree %s\tevidence\n" % ev).strip()
    t2 = run(fx, "mktree",
             inp="100644 blob %s\tseed.txt\n040000 tree %s\t.ufo\n" % (b1, evr)).strip()
    c2 = commit(t2, [c1], "foo-receipt receipt completed — bytes appended")
    run(fx, "update-ref", "refs/heads/master", c2)
    return fx, base, c2


def selftest(out=sys.stdout):
    ok = 0
    total = 4
    import io
    d = tempfile.mkdtemp(prefix="rcbind-selftest-")
    try:
        fx, base, tip = build_fixture(d)
        # arm 1: red — exactly one defect (the empty naming commit), exit 1
        buf = io.StringIO()
        rc = sweep(fx, base, tip, out=buf)
        text = buf.getvalue()
        defects = [l for l in text.splitlines() if l.startswith("BIND_DEFECT")]
        if rc == 1 and len(defects) == 1 and "foo-receipt" in defects[0]:
            ok += 1
            out.write("SELFTEST_ARM1 red-discrimination: PASS\n")
        else:
            out.write("SELFTEST_ARM1 red-discrimination: FAIL rc=%r\n%s\n"
                      % (rc, text))
        # arm 2: green — a commit on top of c2 that adds AND names another
        # receipt it carries; the range tip..c3 names nothing not carried.
        buf = io.StringIO()
        fx2 = fx
        b3 = run(fx2, "hash-object", "-w", "--stdin",
                 inp="second receipt\n", binary=False).strip()
        foo_blob = run(fx2, "rev-parse",
                       "master:.ufo/evidence/win-host/foo-receipt.txt").strip()
        ev_leaf2 = run(fx2, "mktree",
                       inp="100644 blob %s\tfoo-receipt.txt\n"
                           "100644 blob %s\tbar-receipt.txt\n"
                           % (foo_blob, b3)).strip()
        ev = run(fx2, "mktree", inp="040000 tree %s\twin-host\n" % ev_leaf2).strip()
        evr = run(fx2, "mktree", inp="040000 tree %s\tevidence\n" % ev).strip()
        seed = run(fx2, "rev-parse", "master:seed.txt").strip()
        t3 = run(fx2, "mktree",
                 inp="100644 blob %s\tseed.txt\n040000 tree %s\t.ufo\n" % (seed, evr)).strip()
        r = subprocess.run(["git", "-C", fx2, "commit-tree", t3, "-p", tip,
                            "-m", "bar-receipt receipt appended and carried"],
                           capture_output=True, env=_env(),
                           input=b"x")
        c3 = r.stdout.decode().strip()
        run(fx2, "update-ref", "refs/heads/master", c3)
        rc = sweep(fx2, tip, c3, out=buf)
        t2_ = buf.getvalue()
        if rc == 0 and "findings=0" in t2_ and "BIND_OK" in t2_:
            ok += 1
            out.write("SELFTEST_ARM2 green-carrying: PASS\n")
        else:
            out.write("SELFTEST_ARM2 green-carrying: FAIL rc=%r\n%s\n"
                      % (rc, t2_))
        # arm 3: vacuous guard — a range adding no evidence file exits 2
        b4 = run(fx2, "hash-object", "-w", "--stdin", inp="plain\n",
                 binary=False).strip()
        t4 = run(fx2, "mktree",
                 inp="100644 blob %s\tseed.txt\n100644 blob %s\tplain.txt\n"
                     % (seed, b4)).strip()
        r = subprocess.run(["git", "-C", fx2, "commit-tree", t4, "-p", c3,
                            "-m", "no evidence here"],
                           capture_output=True, env=_env(), input=b"x")
        c4 = r.stdout.decode().strip()
        buf = io.StringIO()
        rc = sweep(fx2, c3, c4, out=buf)
        if rc == 2 and "error=empty-range" in buf.getvalue():
            ok += 1
            out.write("SELFTEST_ARM3 vacuous-guard: PASS\n")
        else:
            out.write("SELFTEST_ARM3 vacuous-guard: FAIL rc=%r\n%s\n"
                      % (rc, buf.getvalue()))
        # arm 4: usage — missing flags exit 2
        r = subprocess.run([sys.executable, os.path.abspath(__file__),
                            "--repo", fx2], capture_output=True)
        if r.returncode == 2:
            ok += 1
            out.write("SELFTEST_ARM4 usage: PASS\n")
        else:
            out.write("SELFTEST_ARM4 usage: FAIL rc=%r\n" % r.returncode)
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    out.write("RECEIPT_COMMIT_BIND_SELFTEST: %d/%d pass\n" % (ok, total))
    return 0 if ok == total else 1


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--base")
    ap.add_argument("--tip")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.repo and a.base and a.tip):
        ap.print_usage(sys.stderr)
        sys.stderr.write("RECEIPT_COMMIT_BIND error=usage "
                         "--repo --base --tip required (or --selftest)\n")
        return 2
    try:
        return sweep(a.repo, a.base, a.tip)
    except (RuntimeError, subprocess.CalledProcessError) as e:
        sys.stderr.write("RECEIPT_COMMIT_BIND error=setup %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
