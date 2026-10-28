#!/usr/bin/env python3
"""Sweep 3 (column-aware, final): does the round-54 SCORECARD block quote a value its
cited receipt does not print?

Counting rule, fixed before this run:
 * POPULATION: every `total=N`, `CX_R54_PASS=true|false`, `CTL_POS_cN`, `rekeyed=N/N`,
   `credited=N` token in a table cell of the `## Round 54 — ...` section at REV.
 * EXCLUDED CELLS: the claim-text cell (col 1), the axis cell (col 2) and the Target cell
   (col 4) — a target/claim is a prediction, not a quoted measurement. Everything outside
   a table row (prose) is scored.
 * ATTRIBUTION: the LAST `.ufo/...` reference inside the token's own CELL, else on its line,
   else in its paragraph. A reference ending in `/` names a directory (all receipts under it).
 * BACKING SCOPE: every receipt under .ufo/evidence/round-54, .ufo/evidence/round-53 and
   .ufo/waves/round-54 (*.stdout/.txt/.exit/.json/.out/.md).
 * VERDICTS: NAMED_PRINTS_IT | NAMED_SILENT | NO_RECEIPT_NAMED | NO_SUCH_RECEIPT.
 * 8-hex tokens resolving via `git cat-file -e <tok>^{commit}` are commit pointers,
   out of scope (RESOLVES_AS_COMMIT).
"""
import re, subprocess, sys, json
LANE, REV, OUT, LABEL = sys.argv[1:5]

def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True, text=True)

def show(p):
    r = git("show", f"{REV}:{p}")
    return r.stdout if r.returncode == 0 else None

sec = re.search(r"\n## Round 54 — cold-read floor.*?(?=\n## Round 55|\Z)", show("SCORECARD.md"), re.S).group(0)
lines = sec.splitlines()
paths = git("ls-tree", "-r", "--name-only", REV, "--",
            ".ufo/evidence/round-54", ".ufo/evidence/round-53", ".ufo/waves/round-54").stdout.split()
receipts = {}
for p in paths:
    if p.endswith((".stdout", ".txt", ".exit", ".json", ".out", ".md")):
        t = show(p)
        if t is not None: receipts[p] = t

VAL = re.compile(r"total=\d+|C[12]_R54_PASS=(?:true|false)|CTL_POS_c\d|rekeyed=\d+/\d+|credited=\d+")
HEX = re.compile(r"\b[0-9a-f]{8}\b")
PTR = re.compile(r"\.ufo/(?:evidence|waves)/round-5[0-9]/[A-Za-z0-9_./-]*")
SKIP_CELLS = {1, 2, 4}

paras, cur, start = [], [], 0
for i, l in enumerate(lines):
    if not l.strip():
        if cur: paras.append((start, i - 1)); cur = []
    else:
        if not cur: start = i
        cur.append(l)
if cur: paras.append((start, len(lines) - 1))

def resolve(ref):
    if ref.endswith("/"): return [p for p in receipts if p.startswith(ref)]
    return [ref] if ref in receipts else []

rows, skipped = [], 0
for i, l in enumerate(lines):
    is_row = l.lstrip().startswith("|")
    cells = l.split("|") if is_row else [l]
    for ci, cell in enumerate(cells):
        if is_row and ci in SKIP_CELLS:
            if VAL.search(cell) or HEX.search(cell):
                skipped += len(VAL.findall(cell)) + len(HEX.findall(cell))
            continue
        toks = [m.group(0) for m in VAL.finditer(cell)] + [m.group(0) for m in HEX.finditer(cell)]
        if not toks: continue
        a, b = next(((a, b) for a, b in paras if a <= i <= b), (i, i))
        refs_cell = [m.group(0) for m in PTR.finditer(cell)]
        refs_line = [m.group(0) for m in PTR.finditer(l)]
        refs_para = [m.group(0) for m in PTR.finditer("\n".join(lines[a:b + 1]))]
        for tok in toks:
            if HEX.fullmatch(tok) and git("cat-file", "-e", f"{tok}^{{commit}}").returncode == 0:
                rows.append({"line": i + 1, "col": ci, "token": tok, "verdict": "RESOLVES_AS_COMMIT",
                             "ref": None, "targets": [], "backing": []}); continue
            ref = (refs_cell or refs_line or refs_para or [None])[-1]
            targets = resolve(ref) if ref else []
            backing = sorted(p for p, t in receipts.items() if tok in t)
            if ref is None: v = "NO_RECEIPT_NAMED"
            elif not targets: v = "NO_SUCH_RECEIPT"
            elif any(tok in receipts[t] for t in targets): v = "NAMED_PRINTS_IT"
            else: v = "NAMED_SILENT"
            rows.append({"line": i + 1, "col": ci, "token": tok, "verdict": v, "ref": ref,
                         "targets": targets, "backing": backing})

print(f"LABEL={LABEL} REV={REV} SECTION_LINES={len(lines)} RECEIPTS={len(receipts)}")
print(f"SCORED_TOKENS={len(rows)} EXCLUDED_TARGET_OR_CLAIM_TOKENS={skipped}")
print()
print(f"{'line':>5s} {'col':>3s} {'token':21s} {'verdict':18s} cited ref")
print("-" * 104)
for r in rows:
    print(f"{r['line']:>5d} {r['col']:>3d} {r['token']:21s} {r['verdict']:18s} {r['ref'] or '-'}")
    if r["verdict"] in ("NAMED_SILENT", "NO_SUCH_RECEIPT"):
        print(f"        receipts that DO print it: {r['backing'] or 'NOWHERE'}")
agg = {}
for r in rows: agg[r["verdict"]] = agg.get(r["verdict"], 0) + 1
print()
print("SUMMARY " + " ".join(f"{k}={v}" for k, v in sorted(agg.items())))
bad = [r for r in rows if r["verdict"] in ("NAMED_SILENT", "NO_SUCH_RECEIPT")]
print(f"DEFECTS={len(bad)}")
for r in bad:
    print(f"  L{r['line']}c{r['col']} {r['token']}  ref={r['ref']}  ->  {r['backing'] or 'NOWHERE'}")
json.dump({"label": LABEL, "rev": REV, "rows": rows, "summary": agg, "excluded": skipped},
          open(OUT, "w"), indent=1)
