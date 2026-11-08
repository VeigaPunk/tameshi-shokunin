#!/usr/bin/env python3
"""gate-line-recheck — every Gate line pointer must name the line its quote starts on.

Round 100 (tameshi). Mines `considerthese/2026-11-08.md` idea 2 (gate line-pointer checker):
"Re-render each committed source snapshot with the Gate's stated renderer, then confirm that
each cited `line N` holds the start of its quote." The class is routed history: the round-95
non-author closure (D1, `corpus/lessons/round-95-verifier-spotcheck.md:172-183`) found six Gate
line numbers off by 3-4 under the lane renderer while every quote was verbatim, so the lane's
quote-presence checks (`C1_SOURCE ... quote:1`) stayed green. Quote presence is not pointer
correctness; this tool counts the second.

Renderer: the lane's canonical renderer named by the round-96..99 Gates,
`.ufo/waves/round-93/w1/R93S1-tagstrip.py` (`strip_tags` + `locate`), read as a blob at --rev.
Only the four definitions `strip_tags`, `norm_text`, `_bare` and `locate` are compiled from that
blob (via `ast`, nothing else in it runs); its sha256 is printed. --renderer names another blob.

Grammar (declared, not inferred):

  Gate section   from the line `## Gate` to the next line starting `## `.
  block          a bullet (a line starting `- `) with its continuation lines, or a
                 blank-line-separated paragraph.
  sid            the first `S` + 3 digits in the block, else none.
  pointer        `line N` or `lines N-M` (`-` or an en dash) in the block.
  quote          in the text after the pointer and before the next pointer of the block:
                 (a) the first `"..."` span with no inner `"` when ` (K word[s])` follows it;
                 (b) else the first span closed by `" (K word[s])` whose inner quotes each wrap
                 one whitespace-free token (`"spellchecker"`); (c) else the first `"..."` span
                 with no inner `"`. None -> unbound `no-quote`.
  snapshot       (1) explicit: the last backticked token before the pointer in the block that
                 ends `.html`/`.htm`/`.json`, else the first such token after it; a token with
                 `/` must be a blob at --rev, a bare name resolves to
                 `.ufo/evidence/round-NN/sources/<name>` (NN from the record's file name);
                 (2) sha: a 64-hex token in the block (nearest before the pointer, then after)
                 equal to the sha256 of an `.html`/`.htm` blob at --rev (first by path);
                 (3) inherited: the last snapshot bound earlier in the same Gate for the same
                 sid; (4) convention: `.ufo/evidence/round-NN/sources/s<digits>.html` for the
                 block's sid. Otherwise unbound `snapshot-unresolved`. A `.json` snapshot is
                 unbound `snapshot-not-html` (no line rendering is declared for JSON).

Verdict of one pointer (rendered lines = `strip_tags(blob)`, spans = `locate(lines, quote)`):

  hit     `line N`: some located span starts at N; `lines N-M`: some located span is (N, M).
  miss    the quote is located, but not at the cited line(s); the observed spans are printed.
  absent  the quote is not located anywhere in the rendered snapshot.
  unbound no quote, no snapshot, a JSON snapshot, or a snapshot that is not UTF-8.

Usage:
  python3 -I tools/gate-line-recheck.py --repo LANE --rev <40 hex> --record PATH [--record PATH ...]
        [--renderer PATH]
  python3 -I tools/gate-line-recheck.py --selftest [--repo LANE --rev <40 hex>]

Output: one `GATE_LINE <verdict> <record>:<line> sid=<S###|-> cited=<N|N-M> observed=<a-b,...|->
snapshot=<path|-> bind=<explicit|inherited|convention|-> detail=<d>` line per pointer, then
`GATE_LINE_RECHECK records=R pointers=P hit=H miss=M absent=A unbound=U renderer_sha256=<hex>`.

Exit: 0 every pointer hit (and at least one pointer); 1 any miss, absent or unbound pointer, or
no pointer at all; 2 setup (repo not a git top level, rev not 40 hex or not a commit, record or
renderer absent at rev, renderer lacks a required definition); 64 usage (including a run
without `python3 -I`).
"""
import argparse
import ast
import hashlib
import html as htmlmod
import os
import re
import shutil
import subprocess
import sys
import tempfile

GIT = "/usr/bin/git"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_RENDERER = ".ufo/waves/round-93/w1/R93S1-tagstrip.py"
RENDERER_DEFS = ("strip_tags", "norm_text", "_bare", "locate")
POINTER_RE = re.compile(r"\blines? (\d+)(?:\s*[-\u2013]\s*(\d+))?\b")
QUOTE_COUNTED_RE = re.compile(r'"(.+?)"\s*\(\d+ words?\)', re.S)
QUOTE_PLAIN_RE = re.compile(r'"([^"]+)"', re.S)
WORD_COUNT_RE = re.compile(r'\s*\(\d+ words?\)')
INNER_TOKEN_RE = re.compile(r'"[^"\s]+"')
SHA_RE = re.compile(r"\b([0-9a-f]{64})\b")
SNAP_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:html|htm|json))`")
SID_RE = re.compile(r"\bS(\d{3})\b")
ROUND_RE = re.compile(r"round-(\d+)")


class Setup(Exception):
    pass


def sealed_env():
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null"}


def git(repo, *args):
    try:
        p = subprocess.run([GIT, "-C", repo] + list(args), capture_output=True, env=sealed_env(),
                           timeout=120)
    except subprocess.TimeoutExpired:
        raise Setup("git-timeout")
    return p.returncode, p.stdout


class Tree:
    def __init__(self, repo, rev):
        if not repo or not os.path.isdir(repo):
            raise Setup("repo-absent")
        rc, out = git(repo, "rev-parse", "--show-toplevel")
        if rc != 0 or os.path.realpath(out.decode().strip()) != os.path.realpath(repo):
            raise Setup("repo-not-toplevel")
        if not HEX40.match(rev or ""):
            raise Setup("rev-not-40-hex")
        rc, out = git(repo, "cat-file", "-t", rev)
        if rc != 0 or out.decode().strip() != "commit":
            raise Setup("rev-not-commit")
        rc, out = git(repo, "ls-tree", "-r", "-z", "--name-only", rev)
        if rc != 0:
            raise Setup("ls-tree-failed")
        self.repo, self.rev = repo, rev
        self._cache = {}
        self.blobs = set(x for x in out.decode("utf-8", "surrogateescape").split("\0") if x)
        self._sha_index = None

    def html_by_sha(self, sha):
        """Path of an .html/.htm blob at rev whose sha256 is `sha` (first by name), else None."""
        if self._sha_index is None:
            self._sha_index = {}
            for b in sorted(self.blobs):
                if b.endswith((".html", ".htm")):
                    h = hashlib.sha256(self.read_bytes(b)).hexdigest()
                    self._sha_index.setdefault(h, b)
        return self._sha_index.get(sha)

    def read_bytes(self, path):
        if path in self._cache:
            return self._cache[path]
        if path not in self.blobs:
            raise Setup("blob-absent:%s" % path)
        rc, out = git(self.repo, "cat-file", "blob", "%s:%s" % (self.rev, path))
        if rc != 0:
            raise Setup("blob-unreadable:%s" % path)
        self._cache[path] = out
        return out

    def read_text(self, path):
        try:
            return self.read_bytes(path).decode("utf-8")
        except UnicodeDecodeError:
            raise Setup("blob-not-utf8:%s" % path)


def find_quote(seg):
    """The quote a pointer cites, per the declared grammar (round-100 pre-freeze rule):
    (a) the first plain span `"..."` (no inner quote) when ` (K words)` follows it;
    (b) else the first span closed by `" (K words)` when every inner quote wraps one token;
    (c) else the first plain span. Returns the quote text or None."""
    plain = QUOTE_PLAIN_RE.search(seg)
    if plain and WORD_COUNT_RE.match(seg, plain.end()):
        return plain.group(1)
    counted = QUOTE_COUNTED_RE.search(seg)
    if counted:
        inner = counted.group(1)
        if INNER_TOKEN_RE.sub("", inner).count('"') == 0:
            return inner
    return plain.group(1) if plain else None


def load_renderer(tree, path):
    """Compile only the declared definitions of the renderer blob; return (namespace, sha256)."""
    raw = tree.read_bytes(path)
    sha = hashlib.sha256(raw).hexdigest()
    try:
        mod = ast.parse(raw.decode("utf-8"), filename=path)
    except (UnicodeDecodeError, SyntaxError):
        raise Setup("renderer-unparseable:%s" % path)
    defs = [n for n in mod.body if isinstance(n, ast.FunctionDef) and n.name in RENDERER_DEFS]
    names = set(n.name for n in defs)
    missing = [d for d in RENDERER_DEFS if d not in names]
    if missing:
        raise Setup("renderer-missing:%s" % ",".join(missing))
    ns = {"re": re, "htmlmod": htmlmod, "__builtins__": __builtins__}
    exec(compile(ast.Module(body=defs, type_ignores=[]), path, "exec"), ns)
    return ns, sha


def gate_blocks(text):
    """Yield (start_line, raw_block_text) for each block of the `## Gate` section."""
    lines = text.split("\n")
    start = None
    for i, ln in enumerate(lines):
        if ln.rstrip() == "## Gate":
            start = i + 1
            break
    if start is None:
        return []
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    blocks, cur, cur_start = [], [], None
    for k in range(start, end):
        ln = lines[k]
        if not ln.strip():
            if cur:
                blocks.append((cur_start, "\n".join(cur)))
            cur, cur_start = [], None
            continue
        if ln.startswith("- ") and cur:
            blocks.append((cur_start, "\n".join(cur)))
            cur, cur_start = [], None
        if not cur:
            cur_start = k + 1
        cur.append(ln)
    if cur:
        blocks.append((cur_start, "\n".join(cur)))
    return blocks


def resolve_snapshot(tree, token, rnd):
    if "/" in token:
        return token if token in tree.blobs else None
    if rnd is None:
        return None
    cand = ".ufo/evidence/round-%s/sources/%s" % (rnd, token)
    return cand if cand in tree.blobs else None


def recheck(tree, records, renderer_path):
    ns, rsha = load_renderer(tree, renderer_path)
    out, counts = [], {"hit": 0, "miss": 0, "absent": 0, "unbound": 0}
    rendered = {}
    for rec in records:
        text = tree.read_text(rec)
        m = ROUND_RE.search(os.path.basename(rec))
        rnd = m.group(1) if m else None
        sid_snap = {}
        for bstart, raw in gate_blocks(text):
            sm = SID_RE.search(raw)
            sid = "S" + sm.group(1) if sm else None
            ptrs = list(POINTER_RE.finditer(raw))
            snaps = [(s.start(), s.group(1)) for s in SNAP_RE.finditer(raw)]
            shas = [(s.start(), s.group(1)) for s in SHA_RE.finditer(raw)]
            for i, p in enumerate(ptrs):
                seg_end = ptrs[i + 1].start() if i + 1 < len(ptrs) else len(raw)
                seg = raw[p.end():seg_end]
                q = find_quote(seg)
                mdline = bstart + raw[:p.start()].count("\n")
                n1 = int(p.group(1))
                n2 = int(p.group(2)) if p.group(2) else None
                cited = "%d-%d" % (n1, n2) if n2 is not None else "%d" % n1
                # snapshot binding
                before = [t for pos, t in snaps if pos < p.start()]
                after = [t for pos, t in snaps if pos > p.start()]
                snap, bind = None, "-"
                tok = before[-1] if before else (after[0] if after else None)
                if tok is not None:
                    snap = resolve_snapshot(tree, tok, rnd)
                    bind = "explicit" if snap else "-"
                if snap is None:
                    sb = [h for pos, h in shas if pos < p.start()]
                    sa = [h for pos, h in shas if pos > p.start()]
                    for h in list(reversed(sb)) + sa:
                        hit_path = tree.html_by_sha(h)
                        if hit_path:
                            snap, bind = hit_path, "sha"
                            break
                if snap is None and sid and sid in sid_snap:
                    snap, bind = sid_snap[sid], "inherited"
                if snap is None and sid and rnd is not None:
                    cand = ".ufo/evidence/round-%s/sources/s%s.html" % (rnd, sid[1:])
                    if cand in tree.blobs:
                        snap, bind = cand, "convention"
                if snap is not None and sid:
                    sid_snap[sid] = snap
                verdict, observed, detail = None, "-", "-"
                if q is None:
                    verdict, detail = "unbound", "no-quote"
                elif snap is None:
                    verdict, detail = "unbound", "snapshot-unresolved"
                elif not snap.endswith((".html", ".htm")):
                    verdict, detail = "unbound", "snapshot-not-html"
                else:
                    if snap not in rendered:
                        try:
                            rendered[snap] = ns["strip_tags"](tree.read_text(snap))
                        except Setup:
                            rendered[snap] = None
                    lines = rendered[snap]
                    if lines is None:
                        verdict, detail = "unbound", "snapshot-not-utf8"
                    else:
                        quote = " ".join(q.split())
                        spans = ns["locate"](lines, quote)
                        observed = ",".join("%d-%d" % s for s in spans) if spans else "-"
                        if not spans:
                            verdict = "absent"
                        elif n2 is None and any(a == n1 for a, _ in spans):
                            verdict = "hit"
                        elif n2 is not None and (n1, n2) in spans:
                            verdict = "hit"
                        else:
                            verdict = "miss"
                        detail = "words=%d" % len(quote.split())
                counts[verdict] += 1
                out.append("GATE_LINE %s %s:%d sid=%s cited=%s observed=%s snapshot=%s bind=%s detail=%s"
                           % (verdict, rec, mdline, sid or "-", cited, observed, snap or "-", bind, detail))
    total = sum(counts.values())
    out.append("GATE_LINE_RECHECK records=%d pointers=%d hit=%d miss=%d absent=%d unbound=%d "
               "renderer_sha256=%s" % (len(records), total, counts["hit"], counts["miss"],
                                       counts["absent"], counts["unbound"], rsha))
    rc = 0 if total > 0 and counts["hit"] == total else 1
    return out, rc


# ---------------------------------------------------------------- selftest

PAGE = ("<html><head><style>p{}\n.a{}\n</style></head><body>\n"
        "<p>Alpha line here.</p>\n"
        "<p>The quick brown fox jumps over\n"
        "the lazy dog.</p>\n"
        "<p>Gamma &amp; delta \"inner\" words end.</p>\n"
        "</body></html>\n")
# strip_tags lines: 1 '<style> removed' head, ... measured in the selftest itself


def gate(body):
    return "# lesson\n\n## Gate\n\n" + body + "\n\n## Mistakes\n\nnone\n"


def build_fixture(base, files):
    d = tempfile.mkdtemp(dir=base)
    env = sealed_env()
    env.update({"GIT_AUTHOR_NAME": "fx", "GIT_AUTHOR_EMAIL": "fx@fixture.invalid",
                "GIT_COMMITTER_NAME": "fx", "GIT_COMMITTER_EMAIL": "fx@fixture.invalid"})
    subprocess.run([GIT, "-C", d, "init", "-q"], check=True, env=env)
    top = subprocess.run([GIT, "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, env=env)
    if os.path.realpath(top.stdout.decode().strip()) != os.path.realpath(d):
        raise SystemExit("fixture toplevel mismatch")
    for p, body in files.items():
        fp = os.path.join(d, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "wb" if isinstance(body, bytes) else "w") as fh:
            fh.write(body)
    subprocess.run([GIT, "-C", d, "add", "-A"], check=True, env=env)
    subprocess.run([GIT, "-C", d, "commit", "-q", "-m", "fx"], check=True, env=env)
    rev = subprocess.run([GIT, "-C", d, "rev-parse", "HEAD"], capture_output=True, env=env).stdout.decode().strip()
    return d, rev


def summary_fields(line):
    return dict((k, int(v)) for k, v in re.findall(r"(\w+)=(\d+)\b", line) if k != "renderer_sha256")


def selftest(repo=None, rev=None):
    """With --repo/--rev the renderer fixture is the renderer blob at rev (so the selftest runs
    from a `git show` copy of this tool); otherwise the file beside this tool's lane root."""
    if repo or rev:
        try:
            renderer = Tree(os.path.abspath(repo or ""), rev).read_bytes(DEFAULT_RENDERER)
        except Setup as exc:
            print("GATE_LINE_SELFTEST: setup %s" % exc)
            return 2
    else:
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rpath = os.path.join(here, DEFAULT_RENDERER)
        try:
            with open(rpath, "rb") as fh:
                renderer = fh.read()
        except OSError:
            print("GATE_LINE_SELFTEST: setup renderer-unreadable %s" % rpath)
            return 2
    scratch = os.environ.get("TMPDIR") or None
    base = tempfile.mkdtemp(prefix="gate-line-recheck-selftest-", dir=scratch)
    passed = total = 0
    snap = ".ufo/evidence/round-7/sources/s001.html"
    common = {DEFAULT_RENDERER: renderer, snap: PAGE}
    # rendered lines of PAGE under strip_tags: 'Alpha line here.' is line 2; the fox sentence
    # starts on 3 and ends on 4; 'Gamma & delta "inner" words end.' is line 5.
    S = "- S001 page `s001.html` sha `x`, "
    cases = [
        ("hit-single", S + 'line 2: "Alpha line here." (3 words)', 0, dict(pointers=1, hit=1)),
        ("hit-range", S + 'lines 3-4: "The quick brown fox jumps over the lazy dog." (9 words)', 0,
         dict(hit=1)),
        ("hit-single-wrapped-start", S + 'line 3: "The quick brown fox jumps over the lazy dog." (9 words)',
         0, dict(hit=1)),
        ("miss-off-by-one", S + 'line 3: "Alpha line here." (3 words)', 1, dict(miss=1, hit=0)),
        ("miss-range-end", S + 'lines 3-5: "The quick brown fox jumps over the lazy dog." (9 words)', 1,
         dict(miss=1)),
        ("miss-range-start-only", S + 'lines 2-4: "The quick brown fox jumps over the lazy dog." (9 words)', 1,
         dict(miss=1)),
        ("absent", S + 'line 2: "Alpha line there." (3 words)', 1, dict(absent=1)),
        ("inner-quotes", S + 'line 5: "Gamma & delta "inner" words end." (6 words)', 0, dict(hit=1)),
        ("no-quote", S + "line 2 carries the alpha sentence", 1, dict(unbound=1)),
        ("inherited-sid", S + 'line 2: "Alpha line here." (3 words)\n- S001 again, line 5: '
         '"Gamma & delta "inner" words end." (6 words)', 0, dict(pointers=2, hit=2)),
        ("convention-sid", '- S001 page, no snapshot named, line 2: "Alpha line here." (3 words)', 0,
         dict(hit=1)),
        ("unbound-no-snapshot", '- S999 page, line 2: "Alpha line here." (3 words)', 1, dict(unbound=1)),
        ("unbound-json", '- S001 `s001.json`, line 2: "Alpha line here." (3 words)', 1, dict(unbound=1)),
        ("two-pointers-one-block", S + 'line 2: "Alpha line here." (3 words), and line 4: '
         '"Gamma & delta "inner" words end." (6 words)', 1, dict(pointers=2, hit=1, miss=1)),
        ("no-pointer", "- S001 nothing cited here", 1, dict(pointers=0)),
        ("outside-gate-ignored", S + 'line 2: "Alpha line here." (3 words)', 0, dict(pointers=1)),
        ("sha-binding-beats-convention", "- S001 two fetches: sha256 `" + "0" * 64 + "` then sha256 `"
         + hashlib.sha256(PAGE.encode()).hexdigest() + '`, line 2: "Alpha line here." (3 words)', 0,
         dict(hit=1)),
        ("counted-closer-not-greedy", S + 'lines 3-4: "The quick brown fox jumps over the lazy dog." '
         'The Gate quotes "The quick brown fox" (4 words)', 0, dict(hit=1)),
    ]
    try:
        for name, body, want_rc, want in cases:
            total += 1
            files = dict(common)
            if name == "unbound-json":
                files[".ufo/evidence/round-7/sources/s001.json"] = "{}\n"
            if name == "sha-binding-beats-convention":
                files[snap] = "<p>decoy</p>\n<p>other</p>\n"
                files[".ufo/waves/round-7/w1/real.html"] = PAGE
            text = gate(body)
            if name == "outside-gate-ignored":
                text += '\n- S001 `s001.html` line 3: "Alpha line here." (3 words)\n'
            files["corpus/lessons/round-7.md"] = text
            d, rev = build_fixture(base, files)
            lines, rc = recheck(Tree(d, rev), ["corpus/lessons/round-7.md"], DEFAULT_RENDERER)
            got = summary_fields(lines[-1])
            ok = rc == want_rc and all(got.get(k) == v for k, v in want.items())
            passed += ok
            print("SELFTEST %s %s rc=%d %s" % ("PASS" if ok else "FAIL", name, rc, lines[-1]))
        # setup arms
        d, rev = build_fixture(base, dict(common, **{"corpus/lessons/round-7.md": gate("- x")}))
        dn, revn = build_fixture(base, {"corpus/lessons/round-7.md": gate("- x"),
                                        DEFAULT_RENDERER: "def strip_tags(raw):\n    return []\n"})
        for name, fn in (
            ("setup-rev-short", lambda: Tree(d, rev[:12])),
            ("setup-record-absent", lambda: recheck(Tree(d, rev), ["nope.md"], DEFAULT_RENDERER)),
            ("setup-renderer-absent", lambda: recheck(Tree(d, rev), ["corpus/lessons/round-7.md"], "nope.py")),
            ("setup-renderer-missing-defs", lambda: recheck(Tree(dn, revn), ["corpus/lessons/round-7.md"],
                                                            DEFAULT_RENDERER)),
            ("setup-subdir-not-toplevel", lambda: Tree(os.path.join(d, ".git"), rev)),
        ):
            total += 1
            try:
                fn()
                ok = False
            except Setup:
                ok = True
            passed += ok
            print("SELFTEST %s %s" % ("PASS" if ok else "FAIL", name))
        # a worktree edit must not change the verdict (blobs read at rev)
        total += 1
        d2, rev2 = build_fixture(base, dict(common, **{"corpus/lessons/round-7.md":
                                                       gate(S + 'line 3: "Alpha line here." (3 words)')}))
        with open(os.path.join(d2, "corpus/lessons/round-7.md"), "w") as fh:
            fh.write(gate(S + 'line 2: "Alpha line here." (3 words)'))
        lines, rc = recheck(Tree(d2, rev2), ["corpus/lessons/round-7.md"], DEFAULT_RENDERER)
        ok = rc == 1 and summary_fields(lines[-1]).get("miss") == 1
        passed += ok
        print("SELFTEST %s worktree-edit-ignored rc=%d" % ("PASS" if ok else "FAIL", rc))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print("GATE_LINE_SELFTEST: %d/%d pass" % (passed, total))
    return 0 if passed == total else 1


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--record", action="append", default=[])
    ap.add_argument("--renderer", default=DEFAULT_RENDERER)
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args()
    except SystemExit:
        return 64
    if not sys.flags.isolated:
        print("GATE_LINE_USAGE run as python3 -I (isolated mode is required)")
        return 64
    if a.selftest:
        return selftest(a.repo, a.rev)
    if not a.repo or not a.rev or not a.record:
        print("GATE_LINE_USAGE --repo, --rev and at least one --record are required")
        return 64
    try:
        lines, rc = recheck(Tree(os.path.abspath(a.repo), a.rev), a.record, a.renderer)
    except Setup as exc:
        print("GATE_LINE_SETUP %s" % exc)
        return 2
    for ln in lines:
        print(ln)
    return rc


if __name__ == "__main__":
    sys.exit(main())
