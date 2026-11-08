#!/usr/bin/env python3
"""R100RV1 reproduction: which rendering of the committed round-95/96 snapshots yields the
round-95 Gate numbers (84/4399/4393/4493/2615/2355) and the round-96 re-pins?
Reads: canonical strip_tags/locate from the R93S1 renderer blob (argv[1]); snapshots from the
lane worktree .ufo/evidence (sha256 recorded by the caller). Usage: python3 -I repro.py <R93S1.py>"""
import html, re, sys
ns = {}
exec(compile(open(sys.argv[1], encoding="utf-8").read(), "R93S1", "exec"), ns)
strip_tags, locate = ns["strip_tags"], ns["locate"]
E = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence"
def snap(rnd, s): return open("%s/round-%s/sources/%s.html" % (E, rnd, s), encoding="utf-8").read()
R95 = [("S320","s320","Print or check SHA256 (256-bit) checksums.",84),
       ("S321","s321","The delimiter row consists of cells whose only content are hyphens",4399),
       ("S321","s321","a single header row, a delimiter row separating the header from the data, and zero or more data rows",4393),
       ("S321","s321","The table is broken at the first empty line, or beginning of another block-level structure",4493),
       ("S322","s322","A fenced code block begins with a code fence, preceded by up to three spaces of indentation.",2615),
       ("S323","s323","An indented code block is composed of one or more indented chunks separated by blank lines.",2355)]
R96 = [("S320","s320","Print or check SHA256 (256-bit) checksums.",88),
       ("S321","s321","The delimiter row consists of cells whose only content are hyphens",4403),
       ("S321","s321","The table is broken at the first empty line, or beginning of another block-level structure",4496),
       ("S322","s322","A fenced code block begins with a code fence, preceded by up to three spaces of indentation.",2618),
       ("S323","s323","An indented code block is composed of one or more indented chunks separated by blank lines.",2358)]
def stated(raw):
    return [l.rstrip() for l in html.unescape(re.sub(r"<[^>]+>", " ", raw)).split("\n")]
def tagempty(raw):
    x = re.sub(r"<script\b[^>]*>.*?</script\s*>", " ", raw, flags=re.S | re.I)
    x = re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", x, flags=re.S | re.I)
    x = re.sub(r"<!--.*?-->", " ", x, flags=re.S)
    x = html.unescape(re.sub(r"<[^>]+>", "", x)).replace("\u00a0", " ")
    return [l.rstrip() for l in x.split("\n")]
def perline(raw):
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", l)).replace("\u00a0", " ")).strip()
            for l in raw.split("\n")]
def fmt(spans): return ",".join("%d-%d" % s for s in spans) if spans else "-"
print("== A. round-95 Gate pointers (cited) under each renderer; hit = span starts on cited line ==")
renderers = [("canonical", lambda r: strip_tags(r)), ("stated-preamble", stated),
             ("tags-to-empty", tagempty)]
for name, fn in renderers:
    hits = 0; row = []
    for sid, s, q, c in R95:
        sp = locate(fn(snap(95, s)), q)
        h = any(a == c for a, _ in sp); hits += h
        row.append("%s:cited=%d->%s%s" % (sid, c, fmt(sp), "" if h else "(miss)"))
    print("[%s] hit=%d/6  %s" % (name, hits, "  ".join(row)))
print("== B. per-raw-line tag strip (no line joining), first-4-word line search ==")
for sid, s, q, c in R95:
    L = perline(snap(95, s)); key = " ".join(q.split()[:4])
    print("%s cited=%d perline_hits=%s" % (sid, c, [i + 1 for i, l in enumerate(L) if key in l][:4]))
print("== C. round-96 re-pins under canonical renderer (round-96 snapshots) ==")
for sid, s, q, c in R96:
    sp = locate(strip_tags(snap(96, s)), q)
    print("%s cited=%d canonical=%s %s" % (sid, c, fmt(sp), "hit" if any(a == c for a, _ in sp) else "miss"))
print("== D. canonical neighbourhood of each round-95 quote start (line:text) ==")
for sid, s, q, c in R95:
    t = strip_tags(snap(95, s)); sp = locate(t, q)
    if sp:
        st = sp[0][0]
        for i in range(max(1, st - 2), st + 1):
            print("%s start=%d %6d| %r" % (sid, st, i, t[i - 1][:90]))
