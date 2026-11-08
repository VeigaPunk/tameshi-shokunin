import importlib.util, hashlib, os, sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
W = LANE + "/.ufo/waves/round-98/w1"
REND = sys.argv[1] if len(sys.argv) > 1 else LANE + "/.ufo/waves/round-93/w1/R93S1-tagstrip.py"
BLOB_SHA = "2d431606904915a1113b5041dfb87f4665a6aa3f5acd22a1afb2f2ef73f2a1bf"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()

def hdr(path, name):
    last_status = ""
    last_date = ""
    for line in open(path, encoding="utf-8", errors="replace"):
        low = line.lower()
        if low.startswith("http/"):
            last_status = line.strip()
        elif low.startswith("date:"):
            last_date = line.split(":", 1)[1].strip()
    return last_status, last_date

print("== R98SC1 receipt: snapshots ==")
for fn in ("SC1-s012.html", "SC1-s009.html", "R98SC1-s009-default-ua.html"):
    p = os.path.join(W, fn)
    print("%-30s bytes=%-6d sha256=%s" % (fn, os.path.getsize(p), sha(p)))
for fn in ("SC1-s012.headers", "SC1-s009.headers", "R98SC1-s009-default-ua.headers"):
    st, dt = hdr(os.path.join(W, fn), fn)
    print("%-30s last_status=%r last_date=%r" % (fn, st, dt))

print()
print("== renderer ==")
print("path: %s" % REND)
print("run: python3 -I R98SC1-receipts.py [RENDERER]  (default: the lane worktree file, byte-identical to the blob)")
print("expected blob 764aca97e513d650949999362cd4b0f5f0e566a5 sha256: %s" % BLOB_SHA)
have = sha(REND)
print("loaded renderer sha256: %s%s" % (have, "" if have == BLOB_SHA else "  WARNING: not the pinned blob"))
spec = importlib.util.spec_from_file_location("r93s1_tagstrip", REND)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
print("strip_tags defined: R93S1-tagstrip.py:68 (worktree byte-identical to the blob)")
print("renderer op: script/style removed, comments removed, each tag -> one space, entities unescaped, nbsp folded, lines rstrip")
print()

DOCS = {
    "SC1-s012.html": [
        ("S012-state-anchored-def",
         "An expectation is specification-anchored when composed from values fixed outside the code under mutation, and state-anchored when it flows, directly or transitively, from that code."),
        ("S012-cannot-fail",
         "A test oracle that obtains its expected value from the system it is judging cannot fail."),
        ("S012-reanchor-8of46",
         "Re-anchoring one holding oracle on published procedure, changing no production code, recovers 8 of 46"),
    ],
    "SC1-s009.html": [
        ("S009-impediment",
         "Identifying equivalent mutants remains the largest impediment to the widespread uptake of mutation testing."),
        ("S009-7pct21pct-clause",
         "TCE can discard more than 7% and 21% of all the mutants as being equivalent and duplicated mutants respectively."),
        ("S009-30pct-rendered",
         "A human- based equivalence verification reveals that TCE has the ability to detect approximately 30% of all the existing equivalent mutants."),
        ("S009-30pct-hyphenated-control",
         "A human-based equivalence verification reveals that TCE has the ability to detect approximately 30% of all the existing equivalent mutants."),
    ],
}
for fn, quotes in DOCS.items():
    p = os.path.join(W, fn)
    raw = open(p, encoding="utf-8", errors="replace").read()
    lines = m.strip_tags(raw)
    digits = sha(p)
    print("== %s (%d stripped lines, sha256 %s) ==" % (fn, len(lines), digits))
    for name, q in quotes:
        hits = m.locate(lines, q)
        in_norm = m.norm_quote(q) in m.norm_text(raw)
        print("%-32s words=%2d <=25=%s spans=%s in_normalised_text=%s" %
              (name, len(q.split()), len(q.split()) <= 25, hits, in_norm))
    # the abstract line and its length
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith("Abstract:") or s == "Abstract":
            print("%-32s line=%d chars=%d head=%r" % ("abstract-marker", i, len(ln), s[:60]))
    print()
