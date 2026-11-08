#!/usr/bin/env python3
"""R94S2 — premise audit of the round-94 note reader (QUALITY 154/155/157).

READ-ONLY. Imports the FROZEN counter bytes
  .ufo/evidence/round-94/c1/measure-v94.py
via importlib and uses ITS OWN functions (block_lines, split_cells, tables,
norm_cell, parse_note). Nothing here re-implements the parser.

Parts:
  (a) enumerate EVERY GFM table in the note and in corpus/README.md, using the
      reader's own `tables()`; print start line, header cells, data-row count
      and whether the header row carries a `verdict` cell.
  (b) print every block line OUTSIDE the single verdict table that carries a
      KILLED/SURVIVED token and at least two pipes (must be empty on the
      honest note).
  (c) name every presentation form in either file the reader does NOT key,
      and the declared limit that covers it.
  (d) prove the reader's classification on six hand-built variants built from
      the honest note; report the counter's `verdict_tables` and `badrows`.

Usage: python3 -I R94S2-premise-probe.py --lane LANE --rev REV --work SCRATCH
"""
import argparse, importlib.util, io, json, os, re, subprocess, sys

LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
COUNTER_REL = ".ufo/evidence/round-94/c1/measure-v94.py"
NOTE_REL = "corpus/knowledge/mutation-case-fleet-sources-census.md"
README_REL = "corpus/README.md"
SPEC_REL = ".ufo/evidence/round-94/c1/census-mutants.json"

OUT = io.StringIO()


def p(*a):
    print(*a)
    print(*a, file=OUT)


def load_counter(path):
    spec = importlib.util.spec_from_file_location("measure_v94", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def blob(lane, rev, rel):
    r = subprocess.run(["git", "-C", lane, "cat-file", "blob", "%s:%s" % (rev, rel)],
                       capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def hdr(t):
    p("")
    p("=" * 78)
    p(t)
    p("=" * 78)


def part_a(M, name, text):
    hdr("(a) GFM tables in %s — reader's own tables()" % name)
    tbls = M.tables(text)
    p("tables found: %d" % len(tbls))
    for oi, header, delim, drows in tbls:
        low = [M.norm_cell(c) for c in header]
        vcols = [k for k, c in enumerate(low) if c == "verdict"]
        # data rows = rows of the table excluding any delimiter-looking row
        data = [(ln, c) for ln, c, isd in drows if not isd]
        p("  start_line=%d  header=%s  delim_cells=%d  data_rows=%d  verdict_header=%s"
          % (oi + 1, json.dumps(header), len(delim), len(data),
             ("yes (cols=%s)" % vcols) if vcols else "NO"))
        for ln, c in data:
            p("      row %4d: %s" % (ln + 1, json.dumps(c)))
    return tbls


def part_b(M, name, text):
    """Every block line outside the verdict table with a verdict token and >=2 pipes."""
    hdr("(b) stray verdict tokens outside the verdict table — %s" % name)
    consumed = set()
    vtables = []
    for oi, header, delim, drows in M.tables(text):
        low = [M.norm_cell(c) for c in header]
        if any(c == "verdict" for c in low):
            consumed.add(oi)
            consumed.update(ln for ln, _, _ in drows)
            vtables.append(oi)
    hits = []
    for oi, raw in M.block_lines(text):
        if oi in consumed or raw.count("|") < 2:
            continue
        toks = [c for c in M.split_cells(raw) if c in M.VERDICTS]
        if toks:
            hits.append((oi, raw, toks))
    p("verdict tables (header carries a `verdict` cell): %d at lines %s"
      % (len(vtables), [o + 1 for o in vtables]))
    p("stray verdict-token rows (>=2 pipes): %d" % len(hits))
    for oi, raw, toks in hits:
        p("  L%d tokens=%s :: %s" % (oi + 1, toks, raw.strip()[:160]))
    if not hits:
        p("  (empty — the honest note/README state the item demands)")
    # informational: verdict tokens anywhere at all (incl. prose, single pipe)
    prose = []
    for oi, raw in M.block_lines(text):
        if any(t in raw for t in M.VERDICTS):
            prose.append((oi, raw))
    p("  (info) block lines mentioning KILLED/SURVIVED in any form: %d" % len(prose))
    for oi, raw in prose[:12]:
        p("      L%d: %s" % (oi + 1, raw.strip()[:120]))
    return hits


def part_e(M, note_text, readme_text):
    """Adjunct: the reader's own coverage scan and figure scan on the real files.

    QUALITY 157/164: coverage grades the LAST corpus/README.md row (outside a
    fenced block) whose own cells name the note; figure reads the block-level
    `measured: N/M killed` line.
    """
    hdr("(e) adjunct — coverage (QUALITY 157/164) and figure scans on the real files")
    DENIAL = M.DENIAL_TOKENS
    rows = []
    for oi, raw in M.block_lines(readme_text):
        cells = M.split_cells(raw)

        def _names_note(cell):
            c = cell.strip().strip("`").strip()
            first = c.split()[0].strip("`") if c.split() else ""
            return first == "knowledge/mutation-case-fleet-sources-census.md"

        if cells and any(_names_note(c) for c in cells):
            if raw.count("|") >= 2:
                rows.append((oi, raw))
    p("README rows (block lines, own cell naming the note, >=2 pipes): %d" % len(rows))
    for oi, raw in rows:
        p("  L%d: %s" % (oi + 1, raw.strip()[:200]))
    last = rows[-1] if rows else None
    if last:
        denial = [t for t in DENIAL if t in last[1].lower()]
        p("LAST row = L%d; denial tokens in it: %s -> coverage_ok=%s"
          % (last[0] + 1, denial or "none", not denial))
    else:
        p("LAST row = none -> coverage_ok=False")
    block = "\n".join(t for _, t in M.block_lines(note_text))
    heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", block, re.M)
    p("note `measured: N/M killed` lines (block-level, fenced excluded): %d -> %s"
      % (len(heads), heads))
    allheads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", note_text, re.M)
    p("note `measured:` lines INCLUDING fenced content: %d -> %s" % (len(allheads), allheads))
    p("")
    p("Note: the reader's coverage scan requires the note path to be the FIRST")
    p("whitespace token of a cell, with the cell stripped of backticks. The")
    p("README's own § 'Round 90 — coverage map' row and the round-94 row both")
    p("use a backtick-quoted path cell, so both satisfy the cell rule; the LAST")
    p("one wins (QUALITY 157).")


def part_g(M, spec_ids):
    """(d-cont) the reader's TABLE DEFINITION against S321's actual rules.

    S321 (GFM 0.29-gfm, 4.10 Tables) says, from the committed snapshot:
      * "The delimiter row consists of cells whose only content are hyphens
         ( - ), and optionally, a leading or trailing colon" -> ONE hyphen is
         legal; the reader's DELIM_RE demands three or more.
      * "The header row must match the delimiter row in the number of cells.
         If not, a table will not be recognized" -> a mismatched delimiter is
         NOT a table in GFM; the reader recognises it and adds a `delim:` row.
      * "The remainder of the table's rows may vary in the number of cells...
         empty cells are inserted... the excess is ignored."
      * "The table is broken at the first empty line, or beginning of another
         block-level structure."
      * a table may not sit inside an indented code block (S321 4.4 / S322
         4.4): four leading spaces make the block literal code, but the
         reader's DELIM_RE accepts ANY leading whitespace.
    """
    hdr("(g) the reader's TABLE DEFINITION against S321 (GFM) — recognition probes")
    probes = [
        ("G1 delimiter of ONE hyphen per cell (GFM-legal)",
         "| id | arm | verdict |\n|-|-|-|\n| X1 | a | KILLED |\n"),
        ("G2 delimiter of TWO hyphens per cell (GFM-legal)",
         "| id | arm | verdict |\n|--|--|--|\n| X1 | a | KILLED |\n"),
        ("G3 delimiter of THREE hyphens per cell (the note's own shape)",
         "| id | arm | verdict |\n|---|---|---|\n| X1 | a | KILLED |\n"),
        ("G4 header/delimiter cell-count mismatch (GFM: NOT a table)",
         "| id | arm | verdict |\n|---|---|\n| X1 | a | KILLED |\n"),
        ("G5 table indented 4 spaces (an indented CODE block in GFM)",
         "    | id | arm | verdict |\n    |---|---|---|\n    | X1 | a | KILLED |\n"),
        ("G6 table indented 2 spaces (GFM-legal, <=3 spaces)",
         "  | id | arm | verdict |\n  |---|---|---|\n  | X1 | a | KILLED |\n"),
        ("G7 table inside a blockquote (GFM-legal)",
         "> | id | arm | verdict |\n> |---|---|---|\n> | X1 | a | KILLED |\n"),
        ("G8 table without leading/trailing pipes (GFM-legal)",
         "id | arm | verdict\n--- | --- | ---\nX1 | a | KILLED\n"),
        ("G9 table broken by a heading (GFM: broken at a block-level structure)",
         "| id | arm | verdict |\n|---|---|---|\n| X1 | a | KILLED |\n# heading\n"),
        ("G10 remainder row with MORE cells than the header (GFM: excess ignored)",
         "| id | arm | verdict |\n|---|---|---|\n| X1 | a | KILLED | extra |\n"),
        ("G11 remainder row with FEWER cells (GFM: empty cells inserted)",
         "| id | arm | verdict |\n|---|---|---|\n| X1 |\n"),
        ("G12 header cell `VERDICT` (upper case)",
         "| id | arm | VERDICT |\n|---|---|---|\n| X1 | a | KILLED |\n"),
        ("G13 header cell `verdicts` (plural — not the token)",
         "| id | arm | verdicts |\n|---|---|---|\n| X1 | a | KILLED |\n"),
        ("G14 header cell `Verdict` (mixed case)",
         "| id | arm | Verdict |\n|---|---|---|\n| X1 | a | KILLED |\n"),
        ("G15 header cell `verdict` (the token, control)",
         "| id | arm | verdict |\n|---|---|---|\n| X1 | a | KILLED |\n"),
    ]
    for name, txt in probes:
        tbls = M.tables(txt)
        rows, bad, info = M.parse_note(txt, spec_ids)
        p("%-62s tables=%d verdict_tables=%d badrows=%d  %s"
          % (name, len(tbls), info["verdict_tables"], info["badrows"],
             (info["bad"][:2] if info["bad"] else "")))
    p("")
    p("Reading: G1/G2 -> the reader's DELIM_RE (-{3,}) is STRICTER than S321's")
    p("'cells whose only content are hyphens': a GFM-legal one- or two-hyphen")
    p("delimiter is NOT a table to this reader, so its rows fall through to the")
    p("stray-verdict rule instead of the table rule.")
    p("G4 -> the reader RECOGNISES a table GFM says is not a table, and adds a")
    p("`delim:` finding (the plan's QUALITY 165 declares this rule).")
    p("G5 -> the reader's DELIM_RE accepts any leading whitespace, so a table")
    p("inside a 4-space INDENTED CODE block is keyed. S322 grounds only FENCED")
    p("blocks (4.5); S321 4.4 makes an indented block literal code too. This is")
    p("a class the plan's declared limits do not name.")
    p("G7 -> a blockquoted table is not keyed (the reader sees '>' in the cell).")
    p("G8/G9/G10/G11 -> the reader's remainder and break rules match S321.")
    p("G12/G13/G14/G15 -> norm_cell() lowercases and strips `*`/backticks, so the")
    p("header cell is matched case-insensitively (VERDICT, Verdict, `verdict`")
    p("all key) but only as the exact word `verdict` (`verdicts` does not).")


def part_h(M, base_note, spec_ids):
    """(d-cont) HOSTILE-side robustness where the TABLE rule does not fire.

    G1/G2/G7 showed that a table the reader does not recognise (one-hyphen
    delimiter, blockquoted) still has its rows scanned by the stray-verdict
    rule. These probes ask whether a hidden second verdict table survives
    that backstop, and how the exact-string token match behaves.
    """
    hdr("(h) hostile-side backstop — the stray-verdict rule where tables() misses")
    HDR = "| id | arm | edit | verdict | witness |"
    probes = [
        ("H1 hidden 2nd verdict table, THREE-hyphen delimiter",
         base_note + "\n\n" + HDR + "\n|---|---|---|---|---|\n"
         + "".join("| C%03d | a | b | KILLED | d |\n" % i for i in range(1, 13))),
        ("H2 hidden 2nd verdict table, ONE-hyphen delimiter (GFM-legal)",
         base_note + "\n\n" + HDR + "\n|-|-|-|-|-|\n"
         + "".join("| C%03d | a | b | KILLED | d |\n" % i for i in range(1, 13))),
        ("H3 hidden 2nd verdict table inside a blockquote",
         base_note + "\n\n> " + HDR + "\n> |---|---|---|---|---|\n"
         + "".join("> | C%03d | a | b | KILLED | d |\n" % i for i in range(1, 13))),
        ("H4 hidden 2nd verdict table indented 4 spaces (indented code block)",
         base_note + "\n\n    " + HDR + "\n    |---|---|---|---|---|\n"
         + "".join("    | C%03d | a | b | KILLED | d |\n" % i for i in range(1, 13))),
        ("H5 stray pseudo-table row, token as a CODE SPAN",
         base_note + "\n\n| C001 | a | b | `KILLED` | d |\n"),
        ("H6 stray pseudo-table row, token in BOLD",
         base_note + "\n\n| C001 | a | b | **KILLED** | d |\n"),
        ("H7 stray pseudo-table row, token in lower case",
         base_note + "\n\n| C001 | a | b | killed | d |\n"),
    ]
    for name, txt in probes:
        rows, bad, info = M.parse_note(txt, spec_ids)
        p("%-64s verdict_tables=%d badrows=%d %s"
          % (name, info["verdict_tables"], info["badrows"],
             (info["bad"][:2] if info["bad"] else "")))
    p("")
    p("Reading: the stray-verdict rule is the backstop for every class where")
    p("tables() declines the table (H2/H3/H4/H5/H6/H7 all yield badrows>0, so")
    p("the `ids` conjunct is false and the state is refused). The exact-string")
    p("token match is the same in the table rule and the stray rule, so a")
    p("backticked/bolded/lower-case token is invisible to BOTH (H5/H6/H7).")


def part_i(M, base_note, spec_ids):
    """(d-cont) the DRIVER's own fixture strings, run through the reader.

    Read from the committed driver (.ufo/evidence/round-94/c1/controls-v94.py)
    so the shapes are the battery's, not mine. Read-only: the driver is
    imported for its constants only; it is never executed.
    """
    hdr("(i) the DRIVER's own fixture strings through the reader's parse_note()")
    import importlib.util as _ilu
    dpath = os.path.join(M.__file__.rsplit("/.ufo/", 1)[0],
                         ".ufo/evidence/round-94/c1/controls-v94.py")
    try:
        ds = _ilu.spec_from_file_location("controls_v94", dpath)
        dm = _ilu.module_from_spec(ds)
        ds.loader.exec_module(dm)
    except Exception as e:
        p("could not import the driver: %s" % e)
        return []
    HIDDEN3 = ("\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
        "| C%03d | fixture arm | fixture edit | %s | differs |\n"
        % (i, "SURVIVED" if dm.DERIVED["C%02d" % i] == "KILLED" else "KILLED") for i in range(1, 13)))
    HIDDENX = ("\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n" + "".join(
        "| X%d | fixture arm | fixture edit | KILLED | differs |\n" % i for i in range(1, 13)))
    RENAMED = ("\n| id | arm | result | witness |\n|---|---|---|---|\n"
               "| C01 | fixture arm | SURVIVED | differs |\n| C02 | fixture arm | KILLED | differs |\n")
    vcell = base_note + ("\n| survivor | witness | note |\n|---|---|---|\n"
                         "| C02 | differs | verdict |\n| **C03** | differs | bold id |\n")
    a13 = base_note.replace(
        "| survivor | lanes hit | effect on live registries |\n|---|---|---|\n| C12 used-by trim |",
        "| id | survivor | lanes hit | effect on live registries |\n|---|---|---|---|\n"
        "| C12 |  used-by trim |")
    for old, new in (("| C03 supersedes width |", "| C03 | supersedes width |"),
                     ("| C09 fragment strip |", "| C09 | fragment strip |"),
                     ("| C10 spaced cadence |", "| C10 | spaced cadence |"),
                     ("| C02, C06, C08 |", "| C02 | C06, C08 |")):
        a13 = a13.replace(old, new, 1)
    fixtures = [
        ("pos-real (the committed note)", base_note),
        ("pos-honest-a13 (§2b ids become their own cells)", a13),
        ("pos-honest-verdict-cell (a data cell exactly `verdict`)", vcell),
        ("hidden-c001 (second verdict table C001-C012)", base_note + HIDDEN3),
        ("hidden-x (second verdict table X1-X12)", base_note + HIDDENX),
        ("renamed-result (header `result`, two verdict tokens)", base_note + RENAMED),
        ("pseudo-row (bare pipe line, no delimiter row)",
         base_note + "| C02 | fixture arm | KILLED | differs |\n"),
        ("pos-fenced-hidden (fenced inverted table)",
         base_note + "\n```\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n"
         "| C01 | a | b | SURVIVED | differs |\n```\n"),
    ]
    out = []
    for name, txt in fixtures:
        rows, bad, info = M.parse_note(txt, spec_ids)
        p("%-58s verdict_tables=%d badrows=%d %s"
          % (name, info["verdict_tables"], info["badrows"],
             (info["bad"][:2] if info["bad"] else "")))
        out.append((name, info["verdict_tables"], info["badrows"]))
    p("")
    p("The battery's expectations line up: pos-* -> verdict_tables=1 badrows=0;")
    p("hidden-* -> verdict_tables=2; renamed-result / pseudo-row -> badrows>0")
    p("(the stray-verdict rule, so `ids` is false).")
    return out


def part_j(M, base_note, spec_ids):
    """(d-cont) the honest note with the SAME verdicts in other markup.

    The reader matches the HEADER cell through norm_cell (strips `*` and
    backticks, lowercases) but matches the DATA token by EXACT string. This
    asks whether an honest note whose twelve verdict cells are written as
    code spans or in bold is refused.
    """
    hdr("(j) the honest note with the same twelve verdicts in other markup")
    variants = []
    for style, wrap in (("code span", "`%s`"), ("bold", "**%s**")):
        t = base_note
        for v in ("KILLED", "SURVIVED"):
            t = t.replace("| %s |" % v, "| %s |" % wrap % v)
        variants.append(("honest note, verdict cells as %s" % style, t))
    variants.append(("honest note, verdict cells lower case",
                     base_note.replace("| KILLED |", "| killed |").replace("| SURVIVED |", "| survived |")))
    for name, txt in variants:
        rows, bad, info = M.parse_note(txt, spec_ids)
        p("%-52s verdict_tables=%d badrows=%d %s"
          % (name, info["verdict_tables"], info["badrows"],
             (info["bad"][:2] if info["bad"] else "")))
    p("")
    p("Reading: the token set is matched by EXACT string in the data cell, so a")
    p("verdict written `KILLED` or **KILLED** or `killed` is not a verdict to")
    p("this reader: the row is refused with `no-verdict`. The HEADER cell, by")
    p("contrast, goes through norm_cell() and is matched case-insensitively")
    p("and formatting-insensitively. The asymmetry is undeclared in the plan.")


def part_c(M, note_text, readme_text, note_tbls, readme_tbls):
    hdr("(c) presentation forms the reader does NOT key (declared limits)")
    p("Declared limits of the plan (plans/round-94.plan.md, R94-C1 'Declared limits'):")
    p("  L1 a fenced block is literal text (S322): a fenced inverted table or a")
    p("     fenced `measured:` line is not keyed and does not refuse the note;")
    p("  L2 a table with no `verdict` cell in its header row is not a verdict table")
    p("     (S321): an id-keyed table that asserts no verdict is never refused;")
    p("  L3 a `verdict` cell outside the header row is a data cell (QUALITY 155);")
    p("  L4 a verdict word in prose with fewer than two pipes on the line is not a")
    p("     table row;")
    p("  L5 a cell containing an escaped `\\|` is one cell (S321), so it does not")
    p("     shift the columns;")
    p("  L6 the counter certifies the twelve cells, not how they were obtained;")
    p("  L7 canary/unstable0 are declarations where C2 says so;")
    p("  L8 a fully-correct fence table plus a second fenced table that ALSO passes")
    p("     is not a refusal: the fence limit is a limit.")
    p("")
    # which tables in each file are NOT keyed, and why
    for name, tbls, text in (("note", note_tbls, note_text), ("corpus/README.md", readme_tbls, readme_text)):
        p("%s: per-table keying decision" % name)
        for oi, header, delim, drows in tbls:
            low = [M.norm_cell(c) for c in header]
            vcols = [k for k, c in enumerate(low) if c == "verdict"]
            ndata = sum(1 for _, _, isd in drows if not isd)
            if vcols:
                p("  L%-4d KEYED  verdict_cols=%s header=%s" % (oi + 1, vcols, json.dumps(header)))
            else:
                p("  L%-4d not keyed (no `verdict` cell in header) header=%s rows=%d"
                  % (oi + 1, json.dumps(header), ndata))
                p("        -> limit L2 (S321): a table whose header row carries no `verdict`")
                p("           cell is not a verdict table; its rows are not keyed.")
        p("")
    # fenced blocks in each file
    for name, text in (("note", note_text), ("corpus/README.md", readme_text)):
        fenced = []
        in_fence = False
        start = None
        for i, raw in enumerate(text.split("\n")):
            m = M.FENCE_RE.match(raw)
            if not in_fence:
                if m:
                    in_fence = True
                    start = i + 1
            else:
                if m and m.group(2).strip() == "":
                    in_fence = False
                    fenced.append((start, i + 1))
        p("%s: %d fenced block(s) at lines %s -> limit L1 (S322): fenced content is"
          % (name, len(fenced), [f[0] for f in fenced]))
        p("     literal text; block_lines() drops it, so a fenced table (even an")
        p("     inverted one) is never a verdict table and never refuses.")
    # escaped pipes
    for name, text in (("note", note_text), ("corpus/README.md", readme_text)):
        esc = [(i + 1, raw) for i, raw in enumerate(text.split("\n")) if "\\|" in raw]
        p("%s: %d line(s) with an escaped `\\|` -> limit L5 (S321): split_cells()")
        p("     treats `\\|` as a literal pipe inside one cell, so it does not shift")
        p("     the columns." % name if False else
          "%s: %d line(s) with an escaped `\\|` -> limit L5 (S321): split_cells() treats"
          % (name, len(esc)))
        p("     `\\|` as a literal pipe inside one cell, so it does not shift columns.")
        for ln, raw in esc[:8]:
            p("       L%d: %s" % (ln, raw.strip()[:120]))
    # prose tokens with < 2 pipes
    for name, text in (("note", note_text), ("corpus/README.md", readme_text)):
        prose_tok = []
        for oi, raw in M.block_lines(text):
            if raw.count("|") >= 2:
                continue
            if any(t in raw for t in M.VERDICTS):
                prose_tok.append((oi, raw))
        p("%s: %d prose line(s) with a verdict token and <2 pipes -> limit L4:" % (name, len(prose_tok)))
        for oi, raw in prose_tok[:10]:
            p("       L%d: %s" % (oi + 1, raw.strip()[:120]))
    # scope fact: the reader scans the NOTE only for stray tokens
    p("")
    p("Scope fact (reader premise): the stray-verdict scan and the verdict-table")
    p("keying run over the NOTE only. corpus/README.md is read by the reader only")
    p("for the `coverage` conjunct (last row naming the note), never for verdict")
    p("content. README pipe rows carrying KILLED/SURVIVED are therefore never")
    p("keyed — a scope boundary, not a declared limit of the plan.")


def part_d(M, base_note, spec_ids):
    hdr("(d) six hand-built variants — the reader's own parse_note()")
    p("base note = committed note at the instrument revision (honest state)")
    p("spec ids  = %s" % ",".join(sorted(spec_ids)))
    p("")
    HDR = "| id | arm targeted | edit | verdict | witness |"
    DELIM = "|---|---|---|---|---|"

    def row(i, v):
        return "| C%02d | arm | edit | %s | wit |" % (i, v)

    honest = "| C%02d | arm | edit | %s | wit |"
    variants = []

    # V1 second verdict table (ids X1..X12)
    t = base_note + "\n\n## extra\n\n" + HDR + "\n" + DELIM + "\n" + \
        "".join("| X%d | arm | edit | KILLED | wit |\n" % i for i in range(1, 13))
    variants.append(("V1 second verdict table (X1-X12)", t))

    # V2 renamed header carrying tokens (header `result`, two verdict tokens)
    t = base_note + "\n\n## extra\n\n" + \
        "| id | arm | edit | result | witness |\n|---|---|---|---|---|\n" + \
        "| C02 | arm | edit | KILLED | wit |\n| C03 | arm | edit | SURVIVED | wit |\n"
    variants.append(("V2 renamed header `result` + two verdict tokens", t))

    # V3 bare pipe line with a token, no delimiter row
    t = base_note + "\n\n## extra\n\n| C02 | arm | edit | KILLED | wit |\n"
    variants.append(("V3 bare pipe line with a token (no delimiter row)", t))

    # V4 id-keyed non-verdict table (ids are their own cells, asserts no verdict)
    t = base_note + "\n\n## impact\n\n" + \
        "| survivor | lanes hit | effect |\n|---|---|---|\n" + \
        "| C12 | 20 | many findings |\n| C03 | 20 | 97 rows |\n"
    variants.append(("V4 id-keyed non-verdict table (no verdict asserted)", t))

    # V5 a data cell whose text is exactly `verdict`, in a table whose HEADER
    # carries no `verdict` cell (the driver's own `pos-honest-verdict-cell`
    # shape: QUALITY 155 — a `verdict` cell outside the header row is a data
    # cell), plus a bolded id.
    t = base_note + "\n\n| survivor | witness | note |\n|---|---|---|\n" + \
        "| C02 | differs | verdict |\n| **C03** | differs | bold id |\n"
    variants.append(("V5 a data cell whose text is exactly `verdict` (non-verdict header)", t))

    # V5b the driver's own `pos-honest-a13` reformat: the §2b impact table's
    # ids become cells of their own (the round-92 kill).
    a13 = base_note.replace(
        "| survivor | lanes hit | effect on live registries |\n|---|---|---|\n| C12 used-by trim |",
        "| id | survivor | lanes hit | effect on live registries |\n|---|---|---|---|\n"
        "| C12 |  used-by trim |")
    for old, new in (("| C03 supersedes width |", "| C03 | supersedes width |"),
                     ("| C09 fragment strip |", "| C09 | fragment strip |"),
                     ("| C10 spaced cadence |", "| C10 | spaced cadence |"),
                     ("| C02, C06, C08 |", "| C02 | C06, C08 |")):
        a13 = a13.replace(old, new, 1)
    variants.append(("V5b driver pos-honest-a13: §2b ids become their own cells", a13))

    # V7 (extra) a table inside a 4-space INDENTED code block: GFM renders it
    # as literal code, but the reader's FENCE_RE only knows ``` and ~~~.
    t = base_note + "\n\n## extra\n\n    | id | arm | edit | verdict | witness |\n" + \
        "    |---|---|---|---|---|\n" + \
        "".join("    | X%d | arm | edit | KILLED | wit |\n" % i for i in range(1, 13))
    variants.append(("V7 extra: table inside a 4-space indented code block", t))

    # V8 (extra) header cell written `**verdict**`: norm_cell() strips `*` and
    # lowercases, so the header IS keyed.
    t = base_note + "\n\n## extra\n\n" + \
        "| id | arm | edit | **verdict** | witness |\n|---|---|---|---|---|\n" + \
        "| X1 | arm | edit | KILLED | wit |\n"
    variants.append(("V8 extra: header cell `**verdict**` (norm_cell strips `*`)", t))

    # V9 (extra) a verdict token written as a code span in the DATA cell:
    # the reader matches the data token by EXACT string, so it is not a token.
    t = base_note + "\n\n## extra\n\n" + HDR + "\n" + DELIM + "\n" + \
        "| X1 | arm | edit | `KILLED` | wit |\n"
    variants.append(("V9 extra: verdict token written as a code span in the data cell", t))

    # V10 (extra) a verdict token written in bold in the DATA cell.
    t = base_note + "\n\n## extra\n\n" + HDR + "\n" + DELIM + "\n" + \
        "| X1 | arm | edit | **KILLED** | wit |\n"
    variants.append(("V10 extra: verdict token written in bold in the data cell", t))

    # V11 (extra) a verdict token in lower case in the DATA cell.
    t = base_note + "\n\n## extra\n\n" + HDR + "\n" + DELIM + "\n" + \
        "| X1 | arm | edit | killed | wit |\n"
    variants.append(("V11 extra: verdict token in lower case in the data cell", t))

    # V12 (extra) an escaped pipe inside a data cell: one cell (S321).
    t = base_note + "\n\n## extra\n\n" + HDR + "\n" + DELIM + "\n" + \
        "| X1 | arm | edit \\| more | KILLED | wit |\n"
    variants.append(("V12 extra: escaped pipe in a data cell (one cell, S321)", t))

    # V6 fenced inverted table
    t = base_note + "\n\n## extra\n\n```\n" + HDR + "\n" + DELIM + "\n" + \
        "".join("| C%02d | arm | edit | SURVIVED | wit |\n" % i for i in range(1, 13)) + "```\n"
    variants.append(("V6 fenced inverted table (12 rows inverted)", t))

    results = []
    for name, text in variants:
        rows, bad, info = M.parse_note(text, spec_ids)
        p("%-52s verdict_tables=%d badrows=%d" % (name, info["verdict_tables"], info["badrows"]))
        if bad:
            for b in bad[:6]:
                p("        bad: %s" % b)
            if len(bad) > 6:
                p("        ... %d more" % (len(bad) - 6))
        results.append((name, info["verdict_tables"], info["badrows"], bad))
        p("")
    # baseline
    rows, bad, info = M.parse_note(base_note, spec_ids)
    p("%-52s verdict_tables=%d badrows=%d" % ("BASELINE honest note", info["verdict_tables"], info["badrows"]))
    if bad:
        for b in bad:
            p("        bad: %s" % b)
    p("")
    p("expectations (plan's declared limits / kill rule (a)):")
    p("  V1 -> verdict_tables=2 (not 1)  -> ids/verdict_tables false")
    p("  V2 -> NOT a verdict table; the two token rows are stray -> badrows=2")
    p("  V3 -> stray row -> badrows=1")
    p("  V4 -> not a verdict table, no token -> badrows=0, verdict_tables=1 (honest)")
    p("  V5 -> data cell, not a header -> badrows=0, verdict_tables=1 (honest)")
    p("  V6 -> fenced -> badrows=0, verdict_tables=1 (honest, limit L1)")
    p("  V7 -> a 4-space INDENTED block is NOT a fence to this reader: keyed ->")
    p("        verdict_tables=2, badrows>0 (an UNDECLARED class: the plan's limit")
    p("        L1 names fenced blocks only; GFM/CommonMark also make a 4-space")
    p("        indented block literal code).")
    p("  V8 -> norm_cell() strips `*` and lowercases, so `**verdict**` IS a header")
    p("  V9/V10/V11 -> the DATA token is matched by EXACT string; a code span, a")
    p("        bold span or a lower-case spelling is NOT a verdict token")
    p("  V12 -> an escaped `\\|` stays inside one cell (S321)")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE_DEFAULT)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    lane = os.path.realpath(a.lane)
    counter = os.path.join(lane, COUNTER_REL)
    M = load_counter(counter)
    note = blob(lane, a.rev, NOTE_REL)
    readme = blob(lane, a.rev, README_REL)
    specb = blob(lane, a.rev, SPEC_REL)
    spec_ids = set()
    if specb:
        try:
            spec_ids = {m["id"] for m in json.loads(specb).get("mutants", [])}
        except Exception as e:
            p("spec parse failed: %s" % e)

    p("R94S2 premise probe")
    p("lane      = %s" % lane)
    p("rev       = %s" % a.rev)
    p("counter   = %s" % counter)
    p("note      = %s" % NOTE_REL)
    p("spec ids  = %d (%s)" % (len(spec_ids), ",".join(sorted(spec_ids))))
    p("VERDICTS  = %s" % (M.VERDICTS,))
    p("FENCE_RE  = %s" % M.FENCE_RE.pattern)
    p("DELIM_RE  = %s" % M.DELIM_RE.pattern)

    nt = note if note is not None else ""
    rm = readme if readme is not None else ""

    nt_tbls = part_a(M, NOTE_REL, nt)
    rm_tbls = part_a(M, README_REL, rm)
    part_b(M, NOTE_REL, nt)
    part_b(M, README_REL, rm)
    part_e(M, nt, rm)
    part_c(M, nt, rm, nt_tbls, rm_tbls)
    part_d(M, nt, spec_ids)
    part_i(M, nt, spec_ids)
    part_j(M, nt, spec_ids)
    part_h(M, nt, spec_ids)
    part_g(M, spec_ids)

    hdr("END")
    with open(os.path.join(a.work, "R94S2-premise-probe.out"), "w", encoding="utf-8") as f:
        f.write(OUT.getvalue())
    print(OUT.getvalue())


if __name__ == "__main__":
    main()
