#!/usr/bin/env python3
"""X1 crosswalk arm: gate-line-recheck (rendered-line walker, prose grammar) vs
pointer-recheck (raw-blob walker, manifest grammar) on the same pointer population.

Steps
  1. read the record blobs at --rev and the renderer blob at --rev
  2. take gate-line-recheck's own extracted pointers/quotes (its grammar), run its
     locate() to obtain observed start lines
  3. write a fixture repo: record.md = the Gate sections verbatim (so every pointer
     token is bound in the record bytes); rendered/<snap> = the renderer's output
  4. emit a pointer-recheck manifest: expect=miss at the cited line, expect=hit at
     the observed start line, needle = the longest quote prefix present on the
     observed start line (asserted on the rendered bytes)
  5. run pointer-recheck over it; predicate rows=N met=N unexpected=0 exit 0
  6. trap arms: forged expectations must MISMATCH (exit 1)

Not covered (declared): the range end (`lines N-M` equality) is gate-line-only;
this arm checks the start line, and it reuses the renderer's line space, so it
cross-checks the pointer->coordinate mapping, not the rendering.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

GIT = "/usr/bin/git"
RENDERER = ".ufo/waves/round-93/w1/R93S1-tagstrip.py"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(repo, *args, env=None):
    p = subprocess.run([GIT, "-C", repo] + list(args), capture_output=True, env=env)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args[:2]),
                                                p.stderr.decode(errors="replace")[:400]))
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--tool", required=True, help="gate-line-recheck.py bytes")
    ap.add_argument("--precheck", required=True, help="pointer-recheck.py bytes")
    ap.add_argument("--work", required=True)
    ap.add_argument("--record", action="append", required=True)
    a = ap.parse_args()

    sys.dont_write_bytecode = True
    gl = load_module(os.path.abspath(a.tool), "gate_line_recheck")
    tree = gl.Tree(os.path.abspath(a.lane), a.rev)
    ns, rsha = gl.load_renderer(tree, RENDERER)

    rows, rendered, gate_text = [], {}, []
    for rec in a.record:
        text = tree.read_text(rec)
        m = gl.ROUND_RE.search(os.path.basename(rec))
        rnd = m.group(1) if m else None
        sid_snap = {}
        # keep the Gate section verbatim in the fixture record
        lines = text.split("\n")
        gs = next((i for i, ln in enumerate(lines) if ln.rstrip() == "## Gate"), None)
        if gs is not None:
            ge = next((j for j in range(gs + 1, len(lines)) if lines[j].startswith("## ")),
                      len(lines))
            gate_text.extend(lines[gs:ge])
            gate_text.append("")
        for bstart, raw in gl.gate_blocks(text):
            sm = gl.SID_RE.search(raw)
            sid = "S" + sm.group(1) if sm else None
            ptrs = list(gl.POINTER_RE.finditer(raw))
            snaps = [(s.start(), s.group(1)) for s in gl.SNAP_RE.finditer(raw)]
            shas = [(s.start(), s.group(1)) for s in gl.SHA_RE.finditer(raw)]
            for i, p in enumerate(ptrs):
                seg_end = ptrs[i + 1].start() if i + 1 < len(ptrs) else len(raw)
                q = gl.find_quote(raw[p.end():seg_end])
                mdline = bstart + raw[:p.start()].count("\n")
                n1 = int(p.group(1))
                n2 = int(p.group(2)) if p.group(2) else None
                before = [t for pos, t in snaps if pos < p.start()]
                after = [t for pos, t in snaps if pos > p.start()]
                tok = before[-1] if before else (after[0] if after else None)
                snap = gl.resolve_snapshot(tree, tok, rnd) if tok else None
                if snap is None:
                    for h in list(reversed([h for pos, h in shas if pos < p.start()])) + \
                            [h for pos, h in shas if pos > p.start()]:
                        hit = tree.html_by_sha(h)
                        if hit:
                            snap = hit
                            break
                if snap is None and sid and sid in sid_snap:
                    snap = sid_snap[sid]
                if snap is None and sid and rnd is not None:
                    cand = ".ufo/evidence/round-%s/sources/s%s.html" % (rnd, sid[1:])
                    if cand in tree.blobs:
                        snap = cand
                if snap is not None and sid:
                    sid_snap[sid] = snap
                if q is None or snap is None or not snap.endswith((".html", ".htm")):
                    continue  # unbound in gate-line too; not crosswalk material
                if snap not in rendered:
                    rendered[snap] = ns["strip_tags"](tree.read_text(snap))
                vlines = rendered[snap]
                quote = " ".join(q.split())
                spans = ns["locate"](vlines, quote)
                if not spans:
                    continue  # absent: a third verdict class, out of scope here
                start = spans[0][0]
                span_end = spans[0][1]
                rows.append(dict(record=rec, mdline=mdline, sid=sid or "-",
                                 cited=n1, range=n2, snap=snap, start=start,
                                 quote=quote, needle=None, ptok=p.group(0),
                                 span_end=span_end))
    if not rows:
        raise SystemExit("X1: no crosswalk rows")

    # needle: the exact rendered-page bytes of the located quote (page spacing and
    # inter-line newlines kept), sliced by word offsets so a tag-injected double
    # space never breaks the match. Declared narrowing: the needle is the quote's
    # own span bytes; the hit arm therefore asserts "present in span [a,b]", and
    # the miss arm asserts "absent from the cited line" -- the start-line identity
    # comes from locate(), not from the sub-string test.
    def locate_offsets(vlines, quote):
        text = "\n".join(vlines)
        words, offs = [], []
        pos = 0
        for ln in vlines:
            for m in re.finditer(r"\S+", ln):
                words.append(_bare(m.group(0)))
                offs.append(pos + m.start())
            pos += len(ln) + 1
        qw = [_bare(w) for w in quote.split()]
        n = len(qw)
        for j in range(len(words) - n + 1):
            if words[j:j + n] == qw:
                return text, offs[j], offs[j + n - 1] + len(
                    re.search(r"\S+", text[offs[j + n - 1]:]).group(0))
        return text, None, None

    def _bare(tok):
        return tok.strip(".,;:!?\"'()[]")

    by_snap = {}
    for r in rows:
        by_snap.setdefault(r["snap"], rendered[r["snap"]])
    for r in rows:
        vlines = by_snap[r["snap"]]
        text, o1, o2 = locate_offsets(vlines, r["quote"])
        if o1 is None:
            raise SystemExit("X1: offset locate failed for %s" % r["snap"])
        needle = text[o1:o2]
        cited_line = vlines[r["cited"] - 1] if r["cited"] - 1 < len(vlines) else ""
        if r["cited"] != r["start"] and needle in cited_line:
            raise SystemExit("X1: needle present on cited line %d (%s)"
                             % (r["cited"], r["snap"]))
        r["needle"] = needle

    fx = os.path.join(a.work, "fx")
    shutil.rmtree(fx, ignore_errors=True)
    os.makedirs(fx)
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
           "GIT_AUTHOR_NAME": "fx", "GIT_AUTHOR_EMAIL": "fx@fixture.invalid",
           "GIT_COMMITTER_NAME": "fx", "GIT_COMMITTER_EMAIL": "fx@fixture.invalid",
           "HOME": a.work, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
    subprocess.run([GIT, "-C", fx, "init", "-q"], check=True, env=env)
    top = subprocess.run([GIT, "-C", fx, "rev-parse", "--show-toplevel"],
                         capture_output=True, env=env).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(fx), (top, fx)
    with open(os.path.join(fx, "record.md"), "w") as fh:
        fh.write("\n".join(gate_text) + "\n")
    os.makedirs(os.path.join(fx, "rendered"))
    for snap, vlines in rendered.items():
        name = snap.replace("/", "_")
        with open(os.path.join(fx, "rendered", name), "w") as fh:
            fh.write("\n".join(vlines) + "\n")
        for r in rows:
            if r["snap"] == snap:
                r["target"] = "rendered/" + name
    subprocess.run([GIT, "-C", fx, "add", "-A"], check=True, env=env)
    subprocess.run([GIT, "-C", fx, "commit", "-q", "-m",
                    "x1 crosswalk: gate Gate sections + renderer output"], check=True, env=env)
    frev = subprocess.run([GIT, "-C", fx, "rev-parse", "HEAD"],
                          capture_output=True, env=env).stdout.decode().strip()
    assert len(frev) == 40

    def manifest(name, rs):
        rows_out = []
        for i, (r, expect, at, en) in enumerate(rs):
            rows_out.append({
                "id": "%s-%s-%d" % (os.path.basename(r["record"]).replace(".md", ""),
                                    expect, at),
                "record": "record.md", "record_rev": frev,
                "pointer": r["ptok"],
                "target": r["target"], "target_rev": frev,
                "start": at, "end": en, "needle": r["needle"],
                "expect": expect,
                "note": "x1 crosswalk row from %s:%d" % (r["record"], r["mdline"]),
            })
        p = os.path.join(a.work, name)
        with open(p, "w") as fh:
            json.dump({"schema": "tameshi-pointer-recheck-v1", "rows": rows_out}, fh, indent=1)
        return p, rows_out

    print("X1_RENDERER_SHA256=%s" % rsha)
    print("X1_FIXTURE=%s" % frev)
    print("X1_ROWS=%d" % len(rows))
    for r in rows:
        print("X1_ROW %s:%d sid=%s cited=%d observed_start=%d needle=%r"
              % (r["record"], r["mdline"], r["sid"], r["cited"], r["start"], r["needle"]))

    # main arm: cited line = miss, observed start = hit
    pairs, dropped = [], 0
    for r in rows:
        pairs.append((r, "hit", r["start"], r["span_end"]))
        if r["cited"] != r["start"]:
            pairs.append((r, "miss", r["cited"], r["cited"]))
        else:
            dropped += 1
    print("X1_MISS_ARMS=%d X1_HIT_ARMS=%d X1_NO_MISS_ARM=%d"
          % (len(pairs) - len(rows), len(rows), dropped))
    p, mrows = manifest("x1-manifest.json", pairs)
    print("X1_MANIFEST=%s rows=%d" % (p, len(mrows)))
    out = subprocess.run([sys.executable, "-I", os.path.abspath(a.precheck),
                          "--repo", fx, "--manifest", p], capture_output=True)
    sys.stdout.write(out.stdout.decode())
    print("X1_MAIN_RC=%d" % out.returncode)
    if out.stderr:
        sys.stdout.write("X1_MAIN_STDERR=" + out.stderr.decode()[:500] + "\n")

    # trap 1: a cited line forged as expect=hit must MISMATCH
    t1 = [(rows[0], "hit", rows[0]["cited"], rows[0]["cited"])]
    p1, _ = manifest("x1-trap-cited-as-hit.json", t1)
    o1 = subprocess.run([sys.executable, "-I", os.path.abspath(a.precheck),
                         "--repo", fx, "--manifest", p1], capture_output=True)
    sys.stdout.write(o1.stdout.decode())
    print("X1_TRAP1_RC=%d" % o1.returncode)
    # trap 2: an observed line forged as expect=miss must MISMATCH
    t2 = [(rows[0], "miss", rows[0]["start"], rows[0]["span_end"])]
    p2, _ = manifest("x1-trap-observed-as-miss.json", t2)
    o2 = subprocess.run([sys.executable, "-I", os.path.abspath(a.precheck),
                         "--repo", fx, "--manifest", p2], capture_output=True)
    sys.stdout.write(o2.stdout.decode())
    print("X1_TRAP2_RC=%d" % o2.returncode)

    ok = (out.returncode == 0 and o1.returncode == 1 and o2.returncode == 1)
    print("X1_VERDICT %s" % ("agree" if ok else "DISAGREE"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
