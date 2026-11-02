#!/usr/bin/env python3
r"""tools/receipt-commit-bind.py — bind receipt names in commit messages to the
commit bytes that carry them (round 65; the r64 non-author closure's routed
defect 1 class, made checkable. Round 66: the candidates-scope arm — r65
lesson mistake 5, routed to this round by the r65 non-author closure — the
checker blob changes only in this round).

Convention of record (stated in `corpus/lessons/round-65.md`): a commit whose
message names receipt content must carry those receipt bytes; an empty commit
carries no content, so it can never satisfy a receipt claim made in its own
message (git's own words, S296: "Usually recording a commit that has the exact
same tree as its sole parent commit is a mistake" — the r64 tail commit
6876d746 is the landed instance of the class: its subject names the
tip-confirmation receipt, the bytes landed only in its successor c7d28b19;
the r65 tip commit 87e95597 is the second instance, empty while naming four
receipts).

Check (range sweep, git objects only — no worktree, no index):

  python -I tools/receipt-commit-bind.py --repo LANE --base REV --tip REV

Three arms, all over every commit C in base..tip (oldest first):

  Arm 1 (frozen, r65 — range-added candidates): for every path ADDED in the
  range under `.ufo/evidence/` (`git diff-tree -r --diff-filter=A
  --name-only`), if C's raw message (%B) names the file, the file must exist
  in C's tree (`git ls-tree -r C -- path`, non-empty exact = carried).
  Blind spot (r65 lesson mistake 5): a message naming an evidence path that
  is added NOWHERE in the range never becomes a candidate, so the sweep can
  read `named=0 findings=0` exit 0 on a genuinely defective range — the
  vacuous pass receipted at `.ufo/evidence/round-65/win-host/
  live-bind-erratum-sweep.txt` for `7d7f9ca8..87e95597`.

  Arm 2 (round 66 — message spans): every full path span in C's message that
  starts with `.ufo/evidence/` or `tools/` (disclosed rule below) must
  resolve at C via `git cat-file -e C:<path>` (exit 0 = the blob or tree
  exists at C — held registry row S289's `-e` semantics; the `<commit>:<path>`
  object spelling is gitrevisions, held row S091). Naming a path that is
  absent at the naming commit is itself a BIND_DEFECT.

  Arm 3 (round 66 — the candidates-scope fix proper): every file-like token
  in C's message (basename with a known receipt/tool extension — disclosed
  extension list below) must resolve to at least one path anywhere in C's
  tree (`git ls-tree -r --name-only C`, basename match). A token that
  resolves nowhere is a BIND_DEFECT: the commit names content its tree does
  not carry, whether or not the range ever adds it — this is the arm that
  catches the 87e95597 shape on the live history (its message names
  live-tip-guard.txt etc. by bare basename, and those files were added only
  by the LATER commit ced05ce1, so arm 1 alone still reads findings=0 there).

Name rule arm 1 (disclosed, deterministic, frozen r65): the message names the
file if it contains the basename WITH extension, or contains the basename
WITHOUT extension as a delimited token (the characters immediately before and
after are outside [A-Za-z0-9-]); the bare token must be at least 8 characters
long, so generic short words never match.

Span rule arm 2 (disclosed, deterministic): a span is the longest match of
`(?:\.ufo/evidence|tools)/[A-Za-z0-9_./-]+` in the message not preceded by
[A-Za-z0-9_./-]; trailing characters in `.,;:!?"'` + backtick + `)` are
stripped, and a span whose last segment is empty or ends in `...` is skipped
(an ellipsis shape, not a path).

Token rule arm 3 (disclosed, deterministic): a token is any match of
`[A-Za-z0-9][A-Za-z0-9_-]*\.(txt|json|out|md|py|sh|log|err|diff|html|htm|
csv|tsv|exit|stderr|stdout|yaml|yml|pdf|bin)` in the message; tokens inside
arm-2 spans are the same arm-3 tokens (the span is checked exactly by arm 2,
the basename must additionally resolve somewhere by arm 3).

Output:
  BIND_OK   <commit-short> carries <path>            (arm 1, named+carried)
  BIND_OK   <commit-short> carries-span <path>       (arm 2, resolves)
  BIND_OK   <commit-short> resolves <token>          (arm 3, resolves)
  BIND_DEFECT <commit-short> names <token> -> <path> not carried at that commit   (arm 1)
  BIND_DEFECT <commit-short> names-span <path> -> absent at that commit           (arm 2)
  BIND_DEFECT <commit-short> names-unknown <token> -> no tree path with that name at that commit (arm 3)
  RECEIPT_COMMIT_BIND: commits=N evidence=M named=K carried=K2 spans=P bare=B findings=F

Exit map: 0 = sweep ran, zero defects; 1 = sweep ran, defects found;
2 = usage/setup error, INCLUDING a range with nothing to check at all —
no evidence file added AND no message span AND no message token (fail-closed:
a vacuous pass is refused, an always-pass cheat has no input).

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only (hash-object / mktree / commit-tree / update-ref;
the index is never touched) and checks seven arms:
  1. red/discrimination — an empty commit whose message names a receipt that
     a LATER commit carries (the 6876d746 shape) yields exactly that one
     BIND_DEFECT and exit 1 (arm 1);
  2. green — a commit that carries the receipt it names — by basename, token
     and full span — yields BIND_OK lines, zero findings, exit 0;
  3. vacuous guard — a range with no evidence file, no span and no token
     exits 2;
  4. usage — missing required flags exit 2;
  5. red/nowhere-named — an empty commit whose message names `tip-guard.txt`
     where no path of that name exists anywhere in the tree and the range
     never adds it (the 87e95597 shape) yields the names-unknown BIND_DEFECT
     and exit 1 (arm 3; arm 1 alone reads findings=0 on this fixture — the
     blind spot, now closed);
  6. red/span-absent — an empty commit whose message names the full span
     `.ufo/evidence/win-host/tip-guard.txt` while nothing exists there yields
     the names-span BIND_DEFECT and exit 1 (arm 2);
  7. green/suffix-collision — a commit carrying `reh-bar-receipt.txt` and
     naming it is NOT flagged for the distinct `bar-receipt.txt` (the
     delimited-only name rule, mistake 5's class).
Arms 1, 5 and 6 are the cheat-family discriminators: an always-pass cheat
fails them, and the real-history sweeps recorded in the round receipts
(r64 range, r65 pre-correction range) are the non-synthetic red arms.
"""

import argparse
import re
import subprocess
import sys
import tempfile
import os

EVIDENCE_PREFIX = ".ufo/evidence/"
MIN_TOKEN = 8
SPAN_RE = re.compile(r"(?<![A-Za-z0-9_./-])((?:\.ufo/evidence|tools)/"
                     r"[A-Za-z0-9_./-]+)")
TOKEN_RE = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9_-]*\.(?:txt|json|out|md|py|sh|log|err|diff|"
    r"html|htm|csv|tsv|exit|stderr|stdout|yaml|yml|pdf|bin)\b")
SPAN_STRIP = ".,;:!?)\"'`"


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
    # round 66 name rule v2: the token must appear DELIMITED (the characters
    # immediately before and after are outside [A-Za-z0-9-]); a bare
    # substring match is refused - "reh-rekey-manifest.json" in a message
    # does not name the distinct range-added "rekey-manifest.json" (the
    # suffix-collision class, mined as this round's mistake 5).
    return re.search(r"(?<![A-Za-z0-9-])" + re.escape(token) +
                     r"(?![A-Za-z0-9-])", message) is not None


def message_spans(message):
    spans = set()
    for m in SPAN_RE.finditer(message):
        s = m.group(1)
        while s and s[-1] in SPAN_STRIP:
            s = s[:-1]
        if not s or s.endswith("/") or s.endswith("..."):
            continue
        if s.split("/")[-1] == "":
            continue
        spans.add(s)
    return sorted(spans)


def message_file_tokens(message):
    return sorted(set(TOKEN_RE.findall(message)))


def carried(repo, commit, path):
    out = run(repo, "ls-tree", "-r", "--name-only", commit, "--", path,
              check=False)
    if out.strip() == "":
        return False
    return any(line.strip() == path for line in out.splitlines())


def object_exists(repo, commit, path):
    r = subprocess.run(["git", "-C", str(repo), "cat-file", "-e",
                        "%s:%s" % (commit, path)], capture_output=True)
    return r.returncode == 0


def tree_basenames(repo, commit):
    out = run(repo, "ls-tree", "-r", "--name-only", commit)
    names = set()
    for line in out.splitlines():
        line = line.strip()
        if line:
            names.add(line.rsplit("/", 1)[-1])
    return names


def sweep(repo, base, tip, out=sys.stdout):
    paths = added_evidence_paths(repo, base, tip)
    commits = commits_in_range(repo, base, tip)
    msgs = {c: run(repo, "show", "-s", "--format=%B", c) for c in commits}
    spans_all = {c: message_spans(msgs[c]) for c in commits}
    tokens_all = {c: message_file_tokens(msgs[c]) for c in commits}
    if not paths and not any(spans_all.values()) and not any(tokens_all.values()):
        out.write("RECEIPT_COMMIT_BIND error=empty-range "
                  "no evidence files added and no message spans or tokens "
                  "in %s..%s\n" % (base[:9], tip[:9]))
        return 2
    findings = 0
    named = 0
    carried_count = 0
    span_checks = 0
    bare_checks = 0
    carry_cache = {}
    for c in commits:
        for p in paths:
            carry_cache[(c, p)] = carried(repo, c, p)
    tree_names = {}
    for c in commits:
        tree_names[c] = tree_basenames(repo, c)
    for c in commits:
        short = c[:9]
        msg = msgs[c]
        # arm 1 (frozen): range-added candidates named by basename/stem
        # (frozen counting convention: one line per named path, the first
        # matching token of that path names it)
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
        # arm 2 (r66): full message spans resolve at the naming commit
        for s in spans_all[c]:
            span_checks += 1
            if object_exists(repo, c, s):
                out.write("BIND_OK %s carries-span %s\n" % (short, s))
            else:
                findings += 1
                out.write("BIND_DEFECT %s names-span %s -> absent at that "
                          "commit\n" % (short, s))
        # arm 3 (r66): file-like tokens resolve somewhere in the tree
        for t in tokens_all[c]:
            bare_checks += 1
            if t in tree_names[c]:
                out.write("BIND_OK %s resolves %s\n" % (short, t))
            else:
                findings += 1
                out.write("BIND_DEFECT %s names-unknown %s -> no tree path "
                          "with that name at that commit\n" % (short, t))
    out.write("RECEIPT_COMMIT_BIND: commits=%d evidence=%d named=%d "
              "carried=%d spans=%d bare=%d findings=%d\n" %
              (len(commits), len(paths), named, carried_count,
               span_checks, bare_checks, findings))
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
    total = 7
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
        # receipt it carries — by basename, token and full span; the range
        # tip..c3 names nothing not carried.
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
                            "-m", "bar-receipt.txt appended and carried at "
                                  ".ufo/evidence/win-host/bar-receipt.txt"],
                           capture_output=True, env=_env(),
                           input=b"x")
        c3 = r.stdout.decode().strip()
        run(fx2, "update-ref", "refs/heads/master", c3)
        rc = sweep(fx2, tip, c3, out=buf)
        t2_ = buf.getvalue()
        if (rc == 0 and "findings=0" in t2_ and "BIND_OK" in t2_
                and "resolves bar-receipt.txt" in t2_
                and "carries-span .ufo/evidence/win-host/bar-receipt.txt" in t2_):
            ok += 1
            out.write("SELFTEST_ARM2 green-carrying: PASS\n")
        else:
            out.write("SELFTEST_ARM2 green-carrying: FAIL rc=%r\n%s\n"
                      % (rc, t2_))
        # arm 3: vacuous guard — nothing to check exits 2
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
        # arm 5: red/nowhere-named — the 87e95597 shape: an empty commit
        # naming a file no path of which exists anywhere and the range never
        # adds; arm 1 alone reads findings=0 here (the blind spot).
        r = subprocess.run(["git", "-C", fx2, "commit-tree", t4, "-p", c4,
                            "-m", "tip-guard receipt saved: tip-guard.txt "
                                  "written"],
                           capture_output=True, env=_env(), input=b"x")
        c5 = r.stdout.decode().strip()
        buf = io.StringIO()
        rc = sweep(fx2, c4, c5, out=buf)
        t5_ = buf.getvalue()
        defects5 = [l for l in t5_.splitlines() if l.startswith("BIND_DEFECT")]
        if (rc == 1 and len(defects5) == 1
                and "names-unknown tip-guard.txt" in defects5[0]):
            ok += 1
            out.write("SELFTEST_ARM5 nowhere-named-red: PASS\n")
        else:
            out.write("SELFTEST_ARM5 nowhere-named-red: FAIL rc=%r\n%s\n"
                      % (rc, t5_))
        # arm 6: red/span-absent — an empty commit naming the full span of a
        # path that exists nowhere (the span form of the 87e95597 shape).
        r = subprocess.run(["git", "-C", fx2, "commit-tree", t4, "-p", c5,
                            "-m", "receipt landed at "
                                  "`.ufo/evidence/win-host/tip-guard.txt` "
                                  "per the run"],
                           capture_output=True, env=_env(), input=b"x")
        c6 = r.stdout.decode().strip()
        buf = io.StringIO()
        rc = sweep(fx2, c5, c6, out=buf)
        t6_ = buf.getvalue()
        has_span_defect = any("names-span .ufo/evidence/win-host/"
                              "tip-guard.txt" in l
                              for l in t6_.splitlines()
                              if l.startswith("BIND_DEFECT"))
        if rc == 1 and has_span_defect:
            ok += 1
            out.write("SELFTEST_ARM6 span-absent-red: PASS\n")
        else:
            out.write("SELFTEST_ARM6 span-absent-red: FAIL rc=%r\n%s\n"
                      % (rc, t6_))
        # arm 7: green/suffix-collision - a commit carrying
        # .ufo/evidence/win-host/reh-bar-receipt.txt and naming it must NOT
        # be flagged for the distinct bar-receipt.txt whose basename is a
        # suffix of the carried one (mistake 5's class).
        b5 = run(fx2, "hash-object", "-w", "--stdin",
                 inp="prefixed receipt\n", binary=False).strip()
        leaf5 = run(fx2, "mktree",
                    inp="100644 blob %s\treh-bar-receipt.txt\n" % b5).strip()
        ev5 = run(fx2, "mktree",
                  inp="040000 tree %s\twin-host\n" % leaf5).strip()
        evr5 = run(fx2, "mktree", inp="040000 tree %s\tevidence\n" % ev5).strip()
        t5t = run(fx2, "mktree",
                  inp="100644 blob %s\tseed.txt\n040000 tree %s\t.ufo\n"
                      % (seed, evr5)).strip()
        r = subprocess.run(["git", "-C", fx2, "commit-tree", t5t, "-p", c6,
                            "-m", "reh-bar-receipt.txt appended and carried"],
                           capture_output=True, env=_env(), input=b"x")
        c7 = r.stdout.decode().strip()
        buf = io.StringIO()
        rc = sweep(fx2, c6, c7, out=buf)
        t7_ = buf.getvalue()
        if rc == 0 and "findings=0" in t7_ and "carries" in t7_:
            ok += 1
            out.write("SELFTEST_ARM7 suffix-collision-green: PASS\n")
        else:
            out.write("SELFTEST_ARM7 suffix-collision-green: FAIL rc=%r\n%s\n"
                      % (rc, t7_))
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
