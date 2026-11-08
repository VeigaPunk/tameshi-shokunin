#!/usr/bin/env python3
"""T92S2 — audit the frozen counter's note-parser premise on the real note.

Read-only. Touches no repo file. Reads blobs out of the lane repo at a given
rev, imports the *committed* counter bytes at that rev, and reports:

  (a) a census of every row the parser considers a table row, in
      corpus/knowledge/mutation-case-fleet-sources-census.md and in
      corpus/README.md: first cell, id-shape, verdict-token presence;
  (b) the parser's own verdict on the honest note (rows / bad / headers);
  (c) which table FORMS in the note the parser does not key, with one
      concrete example of each form found;
  (d) the README line(s) that satisfy the counter's coverage conjunct.

Usage:
  python3 -I T92S2-parser-premise.py --lane <lane-repo> --rev <rev> [--out <file>]
"""
import argparse, json, os, re, subprocess, sys

SPEC_PATH = ".ufo/evidence/round-92/c1/census-mutants.json"
COUNTER_PATH = ".ufo/evidence/round-92/c1/measure-v92.py"
NOTE_PATH = "corpus/knowledge/mutation-case-fleet-sources-census.md"
README_PATH = "corpus/README.md"

ID_SHAPE = re.compile(r"^[A-Za-z]{1,4}[_-]?[0-9]{1,4}$")
VERDICTS = ("KILLED", "SURVIVED")


def git(repo, *a):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf-8", "replace"))
        raise SystemExit("git failed: " + " ".join(a))
    return p.stdout


def blob(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def load_counter_module(repo, rev):
    """Import the committed counter bytes at <rev> as a module (main() is guarded)."""
    src = blob(repo, rev, COUNTER_PATH)
    if src is None:
        raise SystemExit("counter absent at rev " + rev)
    import types
    mod = types.ModuleType("frozen_counter")
    mod.__file__ = "%s@%s" % (COUNTER_PATH, rev)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod, src


def rows_of(text):
    """Mirror the frozen parser's own notion of a candidate row.

    The parser splits the RAW line on '|' (not the stripped line), keeps lines
    with >= 3 cells, skips fenced blocks, and takes cells[1] as the first cell
    (cells[0] is the empty string before the leading '|').
    Returns a list of dicts with the parser's per-row decisions.
    """
    out = []
    in_fence = False
    for lineno, raw in enumerate(text.split("\n"), 1):
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            out.append(dict(lineno=lineno, kind="fence-marker", text=line))
            continue
        if in_fence:
            out.append(dict(lineno=lineno, kind="fenced", text=line))
            continue
        cells = [c.strip() for c in raw.split("|")]
        if len(cells) < 3:
            out.append(dict(lineno=lineno, kind="not-a-row", ncells=len(cells), text=line))
            continue
        low = [c.lower() for c in cells]
        if "verdict" in low:
            out.append(dict(lineno=lineno, kind="header", ncells=len(cells),
                            first=cells[1], vcol=low.index("verdict"), text=line))
            continue
        first = cells[1]
        toks = [c for c in cells if c in VERDICTS]
        shaped = bool(ID_SHAPE.match(first))
        out.append(dict(lineno=lineno, kind="row", ncells=len(cells), first=first,
                        id_shaped=shaped, toks=toks, text=line))
    return out


def census(title, text, spec_ids, out):
    out.write("\n=== %s ===\n" % title)
    rows = rows_of(text)
    n_mark = sum(1 for r in rows if r["kind"] == "row")
    n_hdr = sum(1 for r in rows if r["kind"] == "header")
    n_fence = sum(1 for r in rows if r["kind"] in ("fence-marker", "fenced"))
    out.write("candidate rows=%d headers=%d fenced-lines=%d\n" % (n_mark, n_hdr, n_fence))
    out.write("%-6s %-9s %-6s %-5s %-9s %s\n" % ("line", "kind", "cells", "shape", "verdicts", "first cell / text"))
    for r in rows:
        if r["kind"] in ("not-a-row",):
            continue
        if r["kind"] == "row":
            out.write("%-6d %-9s %-6d %-5s %-9s %s\n" % (
                r["lineno"], r["kind"], r["ncells"], "yes" if r["id_shaped"] else "-",
                ",".join(r["toks"]) or "-", r["first"][:70]))
        else:
            out.write("%-6d %-9s %-6s %-5s %-9s %s\n" % (
                r["lineno"], r["kind"], "-", "-", "-", r["text"][:70]))
    # rows that would be REFUSED by the frozen rules
    bad = []
    for r in rows:
        if r["kind"] != "row":
            continue
        if not r["toks"] and not r["id_shaped"]:
            continue
        if not r["id_shaped"]:
            bad.append((r["lineno"], "unkeyed", r["first"]))
        elif r["first"] not in spec_ids:
            bad.append((r["lineno"], "out-of-set", r["first"]))
    return rows, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out", default="-")
    ap.add_argument("--worktree", action="store_true",
                    help="also census the WORKING-TREE note/README (the landing candidate) "
                         "in addition to the committed blobs at --rev")
    a = ap.parse_args()
    out = sys.stdout if a.out == "-" else open(a.out, "w")

    mod, csrc = load_counter_module(a.lane, a.rev)
    out.write("counter blob  %s@%s\n" % (COUNTER_PATH, a.rev))
    import hashlib
    out.write("counter sha256 %s\n" % hashlib.sha256(csrc).hexdigest())
    out.write("counter SELF_SHA256 %s\n" % mod.SELF_SHA256)
    out.write("counter ID_SHAPE %s   VERDICTS %s\n" % (mod.ID_SHAPE.pattern, mod.VERDICTS))

    spec_bytes = blob(a.lane, a.rev, SPEC_PATH)
    spec = json.loads(spec_bytes)
    spec_ids = set(m["id"] for m in spec["mutants"])
    out.write("spec ids %s\n" % ",".join(sorted(spec_ids)))
    out.write("note path %s\n" % mod.NOTE_PATH)
    out.write("readme path %s\n" % README_PATH)

    note_bytes = blob(a.lane, a.rev, NOTE_PATH)
    note_text = note_bytes.decode("utf-8", "replace")
    readme_bytes = blob(a.lane, a.rev, README_PATH)
    readme_text = readme_bytes.decode("utf-8", "replace")

    # ---- (b) the parser's own verdict on the honest note -------------------
    rows, bad, headers = mod.parse_note(note_text, spec_ids)
    out.write("\n=== (b) frozen parse_note on the honest note at %s ===\n" % a.rev)
    out.write("rows keyed   %s\n" % ",".join(sorted(rows)))
    out.write("row values   %s\n" % json.dumps({k: rows[k] for k in sorted(rows)}))
    out.write("bad          %s\n" % (bad if bad else "[] (no refusal)"))
    out.write("headers      %d\n" % headers)
    ids_ok = (not bad) and headers == 1 and sorted(rows) == sorted(spec_ids)
    out.write("ids_ok       %s   (== counter's ids conjunct)\n" % ids_ok)
    out.write("mismatched   %d\n" % sum(1 for k in spec_ids if rows.get(k) is None))
    heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", note_text, re.M)
    out.write("measured: lines %s\n" % heads)

    # ---- (a) census --------------------------------------------------------
    out.write("\n=== (a) row census ===\n")
    note_rows, note_bad = census("NOTE " + NOTE_PATH, note_text, spec_ids, out)
    readme_rows, readme_bad = census("README " + README_PATH, readme_text, spec_ids, out)
    out.write("\nnote rows the frozen rules would refuse: %s\n" % (note_bad if note_bad else "[] (none)"))
    out.write("README rows the frozen rules would refuse (if the parser ran on the README): %d\n"
              % len(readme_bad))
    for b in readme_bad[:40]:
        out.write("   %s\n" % (b,))

    # ---- (c) forms the parser does not key ---------------------------------
    out.write("\n=== (c) table FORMS in the note the parser does not key ===\n")
    forms = []

    # fenced code blocks
    fences = [r for r in note_rows if r["kind"] in ("fence-marker", "fenced")]
    fence_rows = [r for r in note_rows if r["kind"] == "row"]
    forms.append(("fenced code block", bool(fences),
                  "note lines %d-%d hold a fenced block; the parser toggles in_fence and "
                  "skips every line inside it" % (
                      fences[0]["lineno"], fences[-1]["lineno"]) if fences else ""))
    # html table
    html = [i + 1 for i, l in enumerate(note_text.split("\n"))
            if re.search(r"</?(table|tr|td|th)\b", l, re.I)]
    forms.append(("HTML table", bool(html),
                  "note lines %s carry <table>/<tr>/<td>; the parser never sees HTML" % html))
    # escaped pipe inside a cell
    esc = [(i + 1, l.strip()[:70]) for i, l in enumerate(note_text.split("\n"))
           if "\\|" in l]
    forms.append(("cell with an escaped pipe (\\|)", bool(esc),
                  "note lines %s contain a backslash-escaped pipe" % [e[0] for e in esc]))
    # tables: a table starts at a header row (kind=="header") or at a row that
    # is not contiguous with the previous candidate row; consecutive candidate
    # rows (header or row) belong to one table.
    tables = []
    cur = []
    prev = None
    for r in note_rows:
        if r["kind"] not in ("row", "header"):
            if cur:
                tables.append(cur)
                cur = []
            prev = None
            continue
        if prev is not None and r["lineno"] == prev + 1:
            cur.append(r)
        else:
            if cur:
                tables.append(cur)
            cur = [r]
        prev = r["lineno"]
    if cur:
        tables.append(cur)
    no_v_tables = []
    for t in tables:
        head = t[0]
        if not any(c.strip().lower() == "verdict" for c in head["text"].split("|")):
            no_v_tables.append(t)
    forms.append(("table whose header row has no cell named 'verdict' "
                  "(the parser never keys such a table)",
                  bool(no_v_tables),
                  "%d such table(s); first is note line %d: %s" % (
                      len(no_v_tables), no_v_tables[0][0]["lineno"],
                      no_v_tables[0][0]["text"][:80]) if no_v_tables else ""))
    idplus = [r for t in no_v_tables for r in t
              if not r["id_shaped"]
              and re.search(r"\b[A-Za-z]{1,4}[_-]?[0-9]{1,4}\b", r["first"])]
    forms.append(("row whose first cell carries an id token plus surrounding text "
                  "(id-shaped only if the WHOLE cell matches)",
                  bool(idplus),
                  "note line %d: first cell %r" % (idplus[0]["lineno"], idplus[0]["first"])
                  if idplus else ""))
    # LEADING text: a NON-EMPTY non-alphanumeric prefix before an id token.
    lead = [r for r in fence_rows
            if not r["id_shaped"]
            and re.match(r"^[^A-Za-z0-9]+[A-Za-z]{1,4}[_-]?[0-9]{1,4}\b", r["first"])]
    forms.append(("row whose first cell has LEADING text before an id token",
                  bool(lead),
                  "note line %d: first cell %r" % (lead[0]["lineno"], lead[0]["first"])
                  if lead else ""))
    # TRAILING text: an id token followed by anything else in the SAME cell.
    trail = [r for r in fence_rows
             if not r["id_shaped"]
             and re.match(r"^[A-Za-z]{1,4}[_-]?[0-9]{1,4}\b", r["first"])
             and not re.fullmatch(r"[A-Za-z]{1,4}[_-]?[0-9]{1,4}", r["first"])]
    forms.append(("row whose first cell is an id token FOLLOWED BY more text",
                  bool(trail),
                  "note line %d: first cell %r" % (trail[0]["lineno"], trail[0]["first"])
                  if trail else ""))
    # rows that carry a verdict token but are not id-shaped (would be refused)
    vt_unkeyed = [r for r in fence_rows if r["toks"] and not r["id_shaped"]]
    forms.append(("row carrying a verdict token but with a non-id first cell "
                  "(this is what the parser REFUSES)", bool(vt_unkeyed),
                  "note line %d: %r" % (vt_unkeyed[0]["lineno"], vt_unkeyed[0]["first"])
                  if vt_unkeyed else ""))
    # rows that are id-shaped but outside the spec set
    oos = [r for r in fence_rows if r["id_shaped"] and r["first"] not in spec_ids]
    forms.append(("row whose first cell is id-shaped but outside C01-C12", bool(oos),
                  "note line %d: %r" % (oos[0]["lineno"], oos[0]["first"]) if oos else ""))
    # prose verdict tokens (not a table row at all)
    prose = [(i + 1, l.strip()[:80]) for i, l in enumerate(note_text.split("\n"))
             if not l.strip().startswith("|")
             and re.search(r"\b(KILLED|SURVIVED)\b", l)]
    forms.append(("verdict token in prose (no table row)", bool(prose),
                  "note lines %s carry KILLED/SURVIVED outside a table row"
                  % [p[0] for p in prose]))
    for name, present, detail in forms:
        out.write("%-5s %-72s %s\n" % ("FOUND" if present else "absent", name, detail))
    out.write("\nexample of each FOUND form (line text):\n")
    for name, present, detail in forms:
        if present:
            out.write("  [%s] %s\n" % (name, detail))

    # ---- (f) parser PREMISE properties, measured on the real note ---------
    out.write("\n=== (f) parser premise properties, measured ===\n")
    vhdr = [r for r in note_rows if r["kind"] == "header" and r["vcol"] is not None]
    out.write("the verdict header is at note line %d, verdict column index %d\n"
              % (vhdr[0]["lineno"], vhdr[0]["vcol"]))
    out.write("=> the parser keys ONLY the table whose header names 'verdict'; "
              "every other table in the note is keyed by nothing.\n")
    # how many tables does the note carry, and how many does the parser key?
    out.write("tables in the note (contiguous candidate-row groups): %d\n" % len(tables))
    keyed = 0
    for t in tables:
        if any(c.strip().lower() == "verdict" for c in t[0]["text"].split("|")):
            keyed += 1
    out.write("tables keyed by the parser (header names 'verdict'): %d\n" % keyed)
    out.write("tables NOT keyed: %d\n" % (len(tables) - keyed))
    for t in tables:
        has = any(c.strip().lower() == "verdict" for c in t[0]["text"].split("|"))
        out.write("  table at note line %d (%d rows): %s\n"
                  % (t[0]["lineno"], len(t), "KEYED" if has else "not keyed"))
    # would the parser REFUSE the note's non-verdict tables if a row there
    # carried a verdict token?  (the r91 cheat class, replayed on THIS note)
    out.write("\nWould the parser refuse if a NON-VERDICT table's row carried a verdict "
              "token? (r91 cheat class on this note)\n")
    for t in tables:
        if any(c.strip().lower() == "verdict" for c in t[0]["text"].split("|")):
            continue
        # mutate the first DATA row of the table so one of its cells is a verdict token
        data_rows = [r for r in t[1:] if r["first"] != "---"]
        if not data_rows:
            continue
        sample = data_rows[0]
        mutated = list(sample["text"].split("|"))
        # put the verdict token in the LAST cell (the witness-ish column)
        mutated[-2] = " KILLED "
        mline = "|".join(mutated)
        nt2 = note_text.replace(sample["text"], mline, 1)
        r2, b2, h2 = mod.parse_note(nt2, spec_ids)
        out.write("  table at line %d, row %d (first cell %r) mutated to carry a verdict "
                  "token -> bad=%s headers=%d ids_ok=%s\n"
                  % (t[0]["lineno"], sample["lineno"], sample["first"], b2, h2,
                     (not b2) and h2 == 1 and sorted(r2) == sorted(spec_ids)))
    # what happens if the verdict table itself gains a 13th id-shaped row?
    extra = "| C13 | x | y | KILLED | z |"
    r3, b3, h3 = mod.parse_note(note_text.replace(
        "| C12 | used-by comma-list trimming", extra + "\n| C12 | used-by comma-list trimming", 1),
        spec_ids)
    out.write("\nadding an id-shaped row C13 (outside the spec set) to the verdict table -> "
              "bad=%s headers=%d\n" % (b3, h3))
    # what if the note gains a SECOND 'verdict' header?
    r4, b4, h4 = mod.parse_note(note_text + "\n| id | arm | edit | verdict | witness |\n", spec_ids)
    out.write("adding a second 'verdict' header -> bad=%s headers=%d\n" % (b4, h4))

    # BLIND-SPOT probes: can a CONTRADICTING second table be added without refusal?
    out.write("\nBLIND-SPOT probes: add a second table that contradicts the verdict table\n")
    probes = [
        ("second table, id-shaped first cell C02 (dup of the verdict table), UPPERCASE token",
         "| C02 | contradicting arm | edit | KILLED | witness |"),
        ("second table, id-shaped first cell C13 (outside the spec set), UPPERCASE token",
         "| C13 | contradicting arm | edit | KILLED | witness |"),
        ("second table, id-shaped first cell X1 (outside the spec set), UPPERCASE token",
         "| X1 | contradicting arm | edit | KILLED | witness |"),
        ("second table, the NOTE'S OWN survivor-row shape (id token + ' · ' + text, "
         "NOT id-shaped), UPPERCASE token",
         "| C02 · W02 thin-reject length | contradicting arm | edit | KILLED | witness |"),
        ("second table, the NOTE'S OWN survivor-row shape (NOT id-shaped), "
         "LOWERCASE verdict word 'killed'",
         "| C02 · W02 thin-reject length | contradicting arm | edit | killed | witness |"),
        ("second table, id-shaped first cell C02 but NO verdict token at all",
         "| C02 | contradicting arm | edit | (nothing) | witness |"),
    ]
    for name, row in probes:
        nt2 = note_text + "\n" + row + "\n"
        r2, b2, h2 = mod.parse_note(nt2, spec_ids)
        out.write("  %-88s -> bad=%s headers=%d ids_ok=%s\n"
                  % (name[:88], b2 if b2 else "[]", h2,
                     (not b2) and h2 == 1 and sorted(r2) == sorted(spec_ids)))
    # a row whose cells are shifted because the row lacks the leading pipe
    out.write("\nrow-shape probes (does the parser require a leading '|'?):\n")
    shapes = [
        ("row WITHOUT a leading pipe, id in the first position",
         "C02 | contradicting arm | edit | KILLED | witness |"),
        ("row WITHOUT a leading pipe, id in the second position",
         "x | C02 | edit | KILLED | witness |"),
    ]
    for name, row in shapes:
        nt2 = note_text + "\n" + row + "\n"
        r2, b2, h2 = mod.parse_note(nt2, spec_ids)
        out.write("  %-55s -> bad=%s headers=%d ids_ok=%s\n"
                  % (name, b2 if b2 else "[]", h2,
                     (not b2) and h2 == 1 and sorted(r2) == sorted(spec_ids)))

    # FENCED forms: a contradicting table inside a fenced code block.
    out.write("\nFENCED-FORM probes: a contradicting table inside a fenced code block\n")
    fenced_cases = [
        ("fenced table, id-shaped first cell C02, UPPERCASE verdict token",
         "```\n| C02 | contradicting arm | edit | KILLED | witness |\n```"),
        ("fenced table, id-shaped first cell C13 (outside the spec set), UPPERCASE token",
         "```\n| C13 | contradicting arm | edit | KILLED | witness |\n```"),
        ("fenced table with its own 'verdict' HEADER (would bump headers if keyed)",
         "```\n| id | arm | edit | verdict | witness |\n| C02 | x | y | KILLED | z |\n```"),
    ]
    for name, blk in fenced_cases:
        nt2 = note_text + "\n" + blk + "\n"
        r2, b2, h2 = mod.parse_note(nt2, spec_ids)
        out.write("  %-72s -> bad=%s headers=%d ids_ok=%s\n"
                  % (name[:72], b2 if b2 else "[]", h2,
                     (not b2) and h2 == 1 and sorted(r2) == sorted(spec_ids)))
    # IN-PLACE edit of the note's OWN survivor-table row (the most realistic edit)
    out.write("\nIN-PLACE probes: edit the note's own survivor-table row 120 cell 4\n")
    orig120 = [l for l in note_text.split("\n") if l.startswith("| C02 · W02 thin-reject length")][0]
    for label, repl in (("UPPERCASE 'KILLED' in the consequence column",
                         orig120.replace("| a 7-character rejection reason",
                                         "| KILLED | a 7-character rejection reason", 1)),
                        ("LOWERCASE 'killed' in the consequence column",
                         orig120.replace("| a 7-character rejection reason",
                                         "| killed | a 7-character rejection reason", 1))):
        nt2 = note_text.replace(orig120, repl, 1)
        r2, b2, h2 = mod.parse_note(nt2, spec_ids)
        out.write("  %-52s -> bad=%s headers=%d ids_ok=%s\n"
                  % (label, b2 if b2 else "[]", h2,
                     (not b2) and h2 == 1 and sorted(r2) == sorted(spec_ids)))

    # HTML-form and indented-code-block contradicting tables
    out.write("\nHTML / INDENTED-CODE-BLOCK probes:\n")
    more = [
        ("HTML table, C02 KILLED",
         "<table>\n<tr><td>C02</td><td>arm</td><td>edit</td><td>KILLED</td></tr>\n</table>"),
        ("4-space indented code block (Markdown code block), C02 KILLED",
         "    | C02 | arm | edit | KILLED | witness |"),
        ("HTML table with pipes inside the tags",
         "<table>\n| C02 | arm | edit | KILLED | witness |\n</table>"),
    ]
    for name, blk in more:
        nt2 = note_text + "\n" + blk + "\n"
        r2, b2, h2 = mod.parse_note(nt2, spec_ids)
        out.write("  %-62s -> bad=%s headers=%d ids_ok=%s\n"
                  % (name[:62], b2 if b2 else "[]", h2,
                     (not b2) and h2 == 1 and sorted(r2) == sorted(spec_ids)))

    # ---- (d) the README row that satisfies the coverage conjunct -----------
    out.write("\n=== (d) coverage conjunct: README lines that satisfy it ===\n")
    cov = [l for l in readme_text.split("\n")
           if l.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in l]
    out.write("counter's rule: l.lstrip().startswith('|') and the note path in l\n")
    out.write("matching lines: %d\n" % len(cov))
    for l in cov:
        out.write("  %s\n" % l)
    out.write("\ncoverage_ok = %s\n" % bool(cov))
    out.write("coverage conjunct shape: any( l.lstrip().startswith('|') and "
              "'knowledge/mutation-case-fleet-sources-census.md' in l )\n")
    out.write("=> a README row that NAMES the note in ANY column satisfies it, including "
              "a row that records the note as NOT admitted.\n")
    notadmitted = [l for l in readme_text.split("\n")
                   if l.lstrip().startswith("|")
                   and "knowledge/mutation-case-fleet-sources-census.md" in l
                   and "not admitted" in l]
    out.write("of the %d matching README lines, %d record the note as NOT admitted:\n"
              % (len(cov), len(notadmitted)))
    for l in notadmitted:
        out.write("  %s\n" % l[:220])
    # coverage redundancy: remove each matching line in turn; is coverage still true?
    out.write("\ncoverage redundancy (remove each matching README line in turn):\n")
    rlines = readme_text.split("\n")
    for i, l in enumerate(rlines):
        if l in cov:
            rest = [x for j, x in enumerate(rlines) if j != i]
            ok = any(x.lstrip().startswith("|")
                     and "knowledge/mutation-case-fleet-sources-census.md" in x for x in rest)
            out.write("  removing README line %d -> coverage_ok=%s  (%s)\n"
                      % (i + 1, ok, l[:70]))
    # is the note blob identical at the rev under test and at HEAD?
    out.write("\nnote blob identity across revs (the counter reads the note at --rev):\n")
    for r in (a.rev, "HEAD"):
        b = blob(a.lane, r, NOTE_PATH)
        out.write("  %s -> %s\n" % (r, hashlib.sha256(b).hexdigest() if b else "ABSENT"))
    wtn = open(os.path.join(a.lane, NOTE_PATH), "rb").read()
    out.write("  worktree -> %s\n" % hashlib.sha256(wtn).hexdigest())

    # ---- (e) the WORKING-TREE note/README (landing candidate) --------------
    if a.worktree:
        out.write("\n=== (e) WORKING-TREE census (landing candidate) ===\n")
        wt_note = open(os.path.join(a.lane, NOTE_PATH), encoding="utf-8").read()
        wt_readme = open(os.path.join(a.lane, README_PATH), encoding="utf-8").read()
        wt_rows, wt_bad, wt_headers = mod.parse_note(wt_note, spec_ids)
        out.write("worktree note: rows keyed %s\n" % ",".join(sorted(wt_rows)))
        out.write("worktree note: bad %s\n" % (wt_bad if wt_bad else "[] (no refusal)"))
        out.write("worktree note: headers %d\n" % wt_headers)
        out.write("worktree note: ids_ok %s\n" % ((not wt_bad) and wt_headers == 1
                                                  and sorted(wt_rows) == sorted(spec_ids)))
        wt_census, wt_cbad = census("WORKTREE NOTE", wt_note, spec_ids, out)
        out.write("worktree note rows the frozen rules would refuse: %s\n"
                  % (wt_cbad if wt_cbad else "[] (none)"))
        wt_wc = [l for l in wt_readme.split("\n")
                 if l.lstrip().startswith("|")
                 and "knowledge/mutation-case-fleet-sources-census.md" in l]
        out.write("worktree README rows naming the note: %d\n" % len(wt_wc))
        for l in wt_wc:
            out.write("  %s\n" % l[:160])
        out.write("worktree coverage_ok = %s\n" % bool(wt_wc))
        # what the appended block adds
        wt_h = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", wt_note, re.M)
        out.write("worktree measured: lines %s\n" % wt_h)

    if out is not sys.stdout:
        out.close()


if __name__ == "__main__":
    main()
