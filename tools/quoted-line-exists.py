#!/usr/bin/env python3
r"""tools/quoted-line-exists.py — quoted counter lines must be byte-backed by
committed receipt bytes (round 65; considerthese 2026-10-28 proposal 1's
byte-for-byte quoted-line half — the half r64's receipt-existence sweep left
open; proposal text: "check that the path exists at the cited revision and
that the quoted counter line matches the committed stdout byte for byte" —
this tool is that second clause).

Modes (git objects only — no worktree, no index):

  # explicit: one quote against one receipt at a pinned revision
  python -I tools/quoted-line-exists.py --repo LANE \
      --receipt REV:path --quote "COUNTER_LINE value=1 ok"

  # document sweep: every verdict-shaped quoted span in a record must be
  # backed by at least one receipt the record itself cites
  python -I tools/quoted-line-exists.py --repo LANE --doc REV:path [--doc REV:path2 ...]

Extraction rules (deterministic, disclosed):

* path cites — backtick spans over the charset [A-Za-z0-9_./-] that start
  with `.ufo/` or `tools/` (full paths, `git cat-file -e`-style resolution
  against the ls-tree at REV: a listing hit is a blob, a directory prefix
  hit is a tree); or bare basenames (no slash, plausible file suffix) that
  resolve UNIQUELY among `.ufo/evidence/`+`tools/` paths in the tree at REV
  (0 or 2+ matches = skipped-ambiguous, counted); directory cites contribute
  every blob under them at REV (a record that names its receipts directory
  has cited all of them).
* verdict quotes — backtick spans, length >= 12, whose first whitespace-
  token (lead = token up to the first '=' with trailing ':;,;' stripped)
  matches ^[A-Za-z][A-Za-z0-9_\-]*$ and is not a command name (git/python/
  bash/grep/wc/ls/sed/awk/node/cat/sha256sum/diff/comm/sort/head/tail/curl/
  jq/echo/find/xargs/setsid/env/time), AND that are counter-shaped: they
  contain '=' anywhere, OR they contain ': ' with an ALL-UPPERCASE lead
  token (the lane's verdict-line shapes: `TOKEN: value` and `field=...`).
  Prose field descriptions (lowercase `field: value` spans, e.g. JSON key
  shorthand) and quoted stderr fragments are not counter lines and are not
  checked. Spans containing any of …<>|$ (ellipsis/abbreviation/placeholder
  shapes) are not byte-checkable — counted as skipped-shape.
* backing — quote bytes must appear as a substring of some cited receipt's
  committed bytes at REV (first backing receipt reported, paths sorted).

Output:
  RECEIPT  <resolved-blob|resolved-tree|ABSENT|ambiguous> <path>
  QUOTE    <backed|MISSING|skipped-shape> receipt=<path|-> "<span>"
  QUOTED_LINE_EXISTS: doc=<path> quotes=N backed=B missing=M skipped=K receipts=P absent=A ambiguous=G
  QUOTED_LINE_EXISTS TOTAL: docs=D quotes=N backed=B missing=M skipped=K

Exit map: 0 = every checkable quote backed and every cited path resolved;
1 = at least one MISSING quote or ABSENT cited path (the instrument's
finding); 2 = usage/setup, or a document with NOTHING checkable
(fail-closed: a vacuous pass is refused, so a checker that never looks has
no input — the do-nothing cheat scores 2, not 0). The red arms below are the
cheat-family discriminators (criterion 111 shape): an always-back cheat
fails arm 2/arm 3; an exit-0-always cheat fails arm 4.

Selftest: `--selftest` builds a throwaway fixture repository under TMPDIR
with git plumbing only and checks four arms:
  1. explicit green — quote present in receipt bytes, exit 0;
  2. explicit red — quote absent, exit 1;
  3. doc sweep — backed and unbacked quotes in one record: exactly one
     MISSING (named), exit 1;
  4. doc sweep on a record with nothing checkable exits 2 (vacuous guard),
     and missing flags exit 2 (usage).
"""

import argparse
import re
import subprocess
import sys
import tempfile
import os

PATH_PREFIXES = (".ufo/", "tools/")
PATH_CHARS = re.compile(r"^[A-Za-z0-9_./\-]+$")
BARE_SUFFIXES = (".txt", ".json", ".log", ".err", ".out", ".md", ".py",
                 ".sh", ".html", ".jsonl", ".stdout", ".stderr", ".tsv")
LEAD_TOKEN = re.compile(r"^[A-Za-z][A-Za-z0-9_\-]*$")
DENY_LEAD = {
    "git", "python", "python3", "bash", "sh", "grep", "egrep", "wc", "ls",
    "sed", "awk", "node", "cat", "sha256sum", "diff", "comm", "sort", "head",
    "tail", "curl", "jq", "echo", "find", "xargs", "env", "time", "make",
    "cd", "printf", "setsid", "tr", "cut", "stat",
}
BAD_IN_QUOTE = ("…", "<", ">", "|", "$")
MIN_QUOTE = 12


def run(repo, *args, binary=False, inp=None, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       input=inp.encode() if isinstance(inp, str) else inp)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (
            " ".join(args[:3]), r.stderr.decode(errors="replace").strip()[:300]))
    return r.stdout if binary else r.stdout.decode(errors="replace")


def show(repo, rev, path):
    r = subprocess.run(["git", "-C", str(repo), "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def backtick_spans(text):
    return re.findall(r"`([^`\n]+)`", text)


def classify_paths(spans, tree_paths, tree_set):
    """Return (resolved, absent, ambiguous, skipped) where resolved is a list
    of (cited_text, path_or_DIR, kind) and DIR expands later. A directory
    cite expands only when it has >= 2 path segments: the bare prose spans
    `.ufo/` and `tools/` name a surface convention, not a receipt set, and
    are counted as skipped-shape."""
    resolved = []
    absent = []
    ambiguous = []
    skipped = 0
    evidence_paths = [p for p in tree_paths
                      if p.startswith(".ufo/evidence/") or p.startswith("tools/")]
    by_base = {}
    for p in evidence_paths:
        by_base.setdefault(p.rsplit("/", 1)[-1], []).append(p)
    for s in spans:
        t = s.strip()
        if not t or not PATH_CHARS.match(t):
            continue
        if t.startswith(PATH_PREFIXES):
            segs = [x for x in t.split("/") if x]
            if len(segs) < 2:
                skipped += 1
                continue
            is_dir = any(p.startswith(t.rstrip("/") + "/") for p in tree_paths)
            if is_dir:
                resolved.append((t, t, "tree"))
            elif t in tree_set:
                resolved.append((t, t, "blob"))
            else:
                absent.append(t)
            continue
        if "/" in t:
            continue  # relative or foreign path shapes: not resolvable, ignored
        if not t.endswith(BARE_SUFFIXES):
            continue
        hits = by_base.get(t, [])
        if len(hits) == 1:
            resolved.append((t, hits[0], "blob"))
        elif len(hits) == 0:
            continue  # a bare word that names no evidence file: not a cite
        else:
            ambiguous.append(t)
    return resolved, absent, ambiguous


def cat_file_batch(repo, rev, paths):
    """One `git cat-file --batch` process for every <rev>:<path> spec —
    the lane's batched-read pattern (coldread-precheck-portable.py). Returns
    dict path -> bytes for blobs that resolved."""
    out = {}
    if not paths:
        return out
    specs = ["%s:%s" % (rev, p) for p in paths]
    inp = "\n".join(specs).encode() + b"\n"
    p = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch"],
                       capture_output=True, input=inp)
    if p.returncode != 0:
        raise RuntimeError("cat-file --batch failed: %s" %
                           p.stderr.decode(errors="replace")[:300])
    buf = p.stdout
    pos = 0
    for spec in specs:
        nl = buf.index(b"\n", pos)
        header = buf[pos:nl].decode(errors="replace")
        parts = header.split(" ")
        if len(parts) >= 3 and parts[1] == "blob":
            size = int(parts[2])
            data = buf[nl + 1:nl + 1 + size]
            out[spec.split(":", 1)[1]] = data
            pos = nl + 1 + size + 1  # trailing newline after the blob
        else:
            # "<spec> missing" or a non-blob — no bytes follow
            pos = nl + 1
    return out


def expand_receipts(repo, rev, resolved, tree_paths):
    """resolved -> ordered dict path->bytes for blobs (dirs expanded);
    one batched cat-file pass for every blob (cited or directory member)."""
    wanted = []
    for _, p, kind in resolved:
        if kind == "tree":
            pref = p.rstrip("/") + "/"
            wanted.extend(tp for tp in tree_paths if tp.startswith(pref))
        else:
            wanted.append(p)
    blobs = cat_file_batch(repo, rev, sorted(set(wanted)))
    receipts = {}
    for p in wanted:
        if p in blobs:
            receipts.setdefault(p, blobs[p])
    return receipts


def quote_spans(spans):
    quotes = []
    skipped = 0
    for s in spans:
        t = s.strip()
        if len(t) < MIN_QUOTE:
            continue
        if any(ch in t for ch in BAD_IN_QUOTE):
            skipped += 1
            continue
        lead = t.split(None, 1)[0].split("=", 1)[0].rstrip(":;,")
        if not LEAD_TOKEN.match(lead) or lead.lower() in DENY_LEAD:
            continue
        upper_colon = ": " in t and re.match(r"^[A-Z][A-Z0-9_]*$", lead)
        if "=" not in t and not upper_colon:
            continue
        quotes.append(t)
    return quotes, skipped


def sweep_doc(repo, rev, docpath, extra_root=None, out=sys.stdout):
    raw = show(repo, rev, docpath)
    if raw is None:
        out.write("QUOTED_LINE_EXISTS error=doc-unreadable %s\n" % docpath)
        return 2, None
    text = raw.decode("utf-8", "surrogateescape")
    tree_out = run(repo, "ls-tree", "-r", "--name-only", rev)
    tree_paths = [l for l in tree_out.splitlines() if l]
    tree_set = set(tree_paths)
    spans = backtick_spans(text)
    resolved, absent, ambiguous = classify_paths(spans, tree_paths, tree_set)
    # fleet-root surface cites (the r64 cross-surface class): a path absent
    # in-tree is checked, as a NAMED filesystem check, against --extra-root
    # before it counts as a finding.
    fs_resolved = []
    still_absent = []
    for a in absent:
        hit = extra_root and os.path.isfile(os.path.join(extra_root, a))
        if hit:
            fs_resolved.append(a)
        else:
            still_absent.append(a)
    absent = still_absent
    receipts = expand_receipts(repo, rev, resolved, tree_paths)
    quotes, skipped = quote_spans(spans)
    if not quotes and not resolved and not absent and not ambiguous \
            and not fs_resolved:
        out.write("QUOTED_LINE_EXISTS error=empty-doc %s\n" % docpath)
        return 2, None
    backed = 0
    missing = 0
    seen = set()
    for q in quotes:
        if q in seen:
            continue
        seen.add(q)
        qb = q.encode("utf-8")
        hit = None
        for p in sorted(receipts):
            if qb in receipts[p]:
                hit = p
                break
        if hit:
            backed += 1
            out.write('QUOTE backed receipt=%s "%s"\n' % (hit, q[:72]))
        else:
            missing += 1
            out.write('QUOTE MISSING receipt=- "%s"\n' % q[:72])
    seen_lines = set()
    for line in (["RECEIPT ABSENT %s\n" % a for a in absent]
                 + ["RECEIPT ambiguous %s\n" % a for a in ambiguous]
                 + ["RECEIPT resolved-fs %s (extra-root) %s\n" % (a, extra_root)
                    for a in fs_resolved]
                 + ["RECEIPT resolved-%s %s\n" % (k, p)
                    for _, p, k in resolved]):
        if line not in seen_lines:
            seen_lines.add(line)
            out.write(line)
    stats = {"quotes": len(seen), "backed": backed, "missing": missing,
             "skipped": skipped, "receipts": len(receipts),
             "absent": len(absent), "ambiguous": len(ambiguous)}
    out.write("QUOTED_LINE_EXISTS: doc=%s quotes=%(quotes)d backed=%(backed)d "
              "missing=%(missing)d skipped=%(skipped)d receipts=%(receipts)d "
              "absent=%(absent)d ambiguous=%(ambiguous)d\n" %
              dict(stats, doc=docpath))
    rc = 1 if (missing or absent) else 0
    return rc, stats


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--receipt", action="append", default=[])
    ap.add_argument("--quote", action="append", default=[])
    ap.add_argument("--doc", action="append", default=[])
    ap.add_argument("--extra-root", dest="extra_root")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.repo:
        ap.print_usage(sys.stderr)
        sys.stderr.write("QUOTED_LINE_EXISTS error=usage\n")
        return 2
    try:
        if a.doc:
            total = {"docs": 0, "quotes": 0, "backed": 0, "missing": 0,
                     "skipped": 0}
            rc = 0
            for d in a.doc:
                rev, _, path = d.partition(":")
                if not path:
                    sys.stderr.write("QUOTED_LINE_EXISTS error=usage "
                                     "--doc REV:path\n")
                    return 2
                rc_d, st = sweep_doc(a.repo, rev, path, a.extra_root)
                if st:
                    total["docs"] += 1
                    for k in ("quotes", "backed", "missing", "skipped"):
                        total[k] += st[k]
                rc = max(rc, rc_d)
            sys.stdout.write("QUOTED_LINE_EXISTS TOTAL: docs=%(docs)d "
                             "quotes=%(quotes)d backed=%(backed)d "
                             "missing=%(missing)d skipped=%(skipped)d\n" % total)
            return rc
        if a.receipt and a.quote:
            if len(a.receipt) != 1 or len(a.quote) != 1:
                sys.stderr.write("QUOTED_LINE_EXISTS error=usage one "
                                 "--receipt and one --quote\n")
                return 2
            spec = a.receipt[0]
            rev, _, path = spec.partition(":")
            if not path:
                sys.stderr.write("QUOTED_LINE_EXISTS error=usage "
                                 "--receipt REV:path\n")
                return 2
            raw = show(a.repo, rev, path)
            if raw is None:
                sys.stdout.write("QUOTE MISSING receipt=%s (unreadable)\n"
                                 % path)
                return 1
            if a.quote[0].encode("utf-8") in raw:
                sys.stdout.write('QUOTE backed receipt=%s "%s"\n'
                                 % (path, a.quote[0][:72]))
                return 0
            sys.stdout.write('QUOTE MISSING receipt=%s "%s"\n'
                             % (path, a.quote[0][:72]))
            return 1
        ap.print_usage(sys.stderr)
        sys.stderr.write("QUOTED_LINE_EXISTS error=usage --doc or "
                         "--receipt/--quote required (or --selftest)\n")
        return 2
    except (RuntimeError, subprocess.CalledProcessError) as e:
        sys.stderr.write("QUOTED_LINE_EXISTS error=setup %s\n" % e)
        return 2


def _fixture(d):
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
                           capture_output=True, env=_env(), input=msg.encode())
        if r.returncode != 0:
            raise RuntimeError("commit-tree: %s" % r.stderr.decode()[:200])
        return r.stdout.decode().strip()

    def _env():
        e = dict(os.environ)
        e["GIT_AUTHOR_NAME"] = e["GIT_COMMITTER_NAME"] = "fx"
        e["GIT_AUTHOR_EMAIL"] = e["GIT_COMMITTER_EMAIL"] = "fx@fx"
        return e

    blob = lambda s: run(fx, "hash-object", "-w", "--stdin", inp=s).strip()
    rec = blob("RECEIPT_LINE_A value=1 ok\nRECEIPT_LINE_B value=2 ok\n")
    doc_body = (
        "Record: the run passed — `RECEIPT_LINE_A value=1 ok` per "
        "`selftest-receipt.txt`; the other arm printed "
        "`RECEIPT_LINE_C value=9 no`; full path cite "
        "`.ufo/evidence/fix/selftest-receipt.txt`.\n"
    )
    doc = blob(doc_body)
    rec_leaf = run(fx, "mktree",
                   inp="100644 blob %s\tselftest-receipt.txt\n"
                       "100644 blob %s\tselftest-doc.md\n" % (rec, doc)).strip()
    ev = run(fx, "mktree", inp="040000 tree %s\tfix\n" % rec_leaf).strip()
    evr = run(fx, "mktree", inp="040000 tree %s\tevidence\n" % ev).strip()
    top = run(fx, "mktree",
              inp="040000 tree %s\t.ufo\n100644 blob %s\tREADME.md\n"
                  % (evr, blob("seed\n"))).strip()
    r1 = commit(top, [], "fixture base")
    run(fx, "update-ref", "refs/heads/master", r1)
    return fx, r1


def selftest(out=sys.stdout):
    ok = 0
    total = 4
    d = tempfile.mkdtemp(prefix="qle-selftest-")
    try:
        fx, rev = _fixture(d)
        here = os.path.dirname(os.path.abspath(__file__))
        # arm 1: explicit green
        r = subprocess.run([sys.executable, os.path.join(here, "quoted-line-exists.py"),
                            "--repo", fx, "--receipt",
                            "%s:.ufo/evidence/fix/selftest-receipt.txt" % rev,
                            "--quote", "RECEIPT_LINE_A value=1 ok"],
                           capture_output=True)
        if r.returncode == 0 and b"QUOTE backed" in r.stdout:
            ok += 1
            out.write("SELFTEST_ARM1 explicit-green: PASS\n")
        else:
            out.write("SELFTEST_ARM1 explicit-green: FAIL rc=%r %r %r\n"
                      % (r.returncode, r.stdout[:200], r.stderr[:200]))
        # arm 2: explicit red (the always-back cheat fails here)
        r = subprocess.run([sys.executable, os.path.join(here, "quoted-line-exists.py"),
                            "--repo", fx, "--receipt",
                            "%s:.ufo/evidence/fix/selftest-receipt.txt" % rev,
                            "--quote", "RECEIPT_LINE_Z value=99 no"],
                           capture_output=True)
        if r.returncode == 1 and b"QUOTE MISSING" in r.stdout:
            ok += 1
            out.write("SELFTEST_ARM2 explicit-red: PASS\n")
        else:
            out.write("SELFTEST_ARM2 explicit-red: FAIL rc=%r %r\n"
                      % (r.returncode, r.stdout[:200]))
        # arm 3: doc sweep — exactly one MISSING (RECEIPT_LINE_C), exit 1
        r = subprocess.run([sys.executable, os.path.join(here, "quoted-line-exists.py"),
                            "--repo", fx, "--doc",
                            "%s:.ufo/evidence/fix/../fix/selftest-doc.md" % rev],
                           capture_output=True)
        # note: '..' path is unusual; use the clean path instead
        r = subprocess.run([sys.executable, os.path.join(here, "quoted-line-exists.py"),
                            "--repo", fx, "--doc",
                            "%s:.ufo/evidence/fix/selftest-doc.md" % rev],
                           capture_output=True)
        txt = r.stdout.decode(errors="replace")
        if (r.returncode == 1 and txt.count("QUOTE MISSING") == 1
                and "RECEIPT_LINE_C" in txt and "backed=1" in txt):
            ok += 1
            out.write("SELFTEST_ARM3 doc-sweep-red: PASS\n")
        else:
            out.write("SELFTEST_ARM3 doc-sweep-red: FAIL rc=%r\n%s\n"
                      % (r.returncode, txt))
        # arm 4: vacuous guard + usage
        empty_blob = run(fx, "hash-object", "-w", "--stdin",
                         inp="nothing checkable\n").strip()
        fix_leaf = run(fx, "rev-parse", "master:.ufo/evidence/fix").strip()
        empty_leaf = run(fx, "mktree",
                         inp="100644 blob %s\tempty.md\n" % empty_blob).strip()
        evr2 = run(fx, "mktree",
                   inp="040000 tree %s\tfix\n040000 tree %s\tfix2\n"
                       % (fix_leaf, empty_leaf)).strip()
        ufo2 = run(fx, "mktree", inp="040000 tree %s\tevidence\n" % evr2).strip()
        top2 = run(fx, "mktree", inp="040000 tree %s\t.ufo\n" % ufo2).strip()
        envx = dict(os.environ)
        envx["GIT_AUTHOR_NAME"] = envx["GIT_COMMITTER_NAME"] = "fx"
        envx["GIT_AUTHOR_EMAIL"] = envx["GIT_COMMITTER_EMAIL"] = "fx@fx"
        r = subprocess.run(["git", "-C", fx, "commit-tree", top2, "-p", rev,
                            "-m", "empty doc fixture"], capture_output=True,
                           env=envx, input=b"x")
        rev2 = r.stdout.decode().strip()
        r = subprocess.run([sys.executable, os.path.join(here, "quoted-line-exists.py"),
                            "--repo", fx, "--doc", "%s:.ufo/evidence/fix2/empty.md" % rev2],
                           capture_output=True)
        arm4a = (r.returncode == 2 and b"error=empty-doc" in r.stdout)
        r2 = subprocess.run([sys.executable, os.path.join(here, "quoted-line-exists.py"),
                             "--repo", fx], capture_output=True)
        arm4b = (r2.returncode == 2)
        if arm4a and arm4b:
            ok += 1
            out.write("SELFTEST_ARM4 vacuous-usage: PASS\n")
        else:
            out.write("SELFTEST_ARM4 vacuous-usage: FAIL arm4a=%r rc=%r %r arm4b_rc=%r\n"
                      % (arm4a, r.returncode, r.stdout[:200], r2.returncode))
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)
    out.write("QUOTED_LINE_EXISTS_SELFTEST: %d/%d pass\n" % (ok, total))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
