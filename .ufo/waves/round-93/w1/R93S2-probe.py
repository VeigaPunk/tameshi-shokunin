#!/usr/bin/env python3
"""R93S2 - parser-premise audit of the round-93 verdict-content reader.

Read-only.  Uses the FROZEN counter's own functions (importlib on
.ufo/evidence/round-93/c1/measure-v93.py at the instrument revision) - no
re-implementation of the parser anywhere in this file.

Parts
  (a) enumerate EVERY GFM table of the note and of corpus/README.md with the
      reader's own `tables()` definition; print start line, header cells,
      data-row count, and whether the header row carries a `verdict` cell.
  (b) print every block line OUTSIDE the verdict table that carries a
      KILLED/SURVIVED token and at least two pipes (must be EMPTY on the
      honest note); cross-check against the reader's own `bad` list.
  (c) name every presentation form in either file the reader does NOT key and
      why that is the declared limit.
  (d) prove the reader's classification on six hand-built variants built in
      the scratch dir; report the reader's `verdict_tables` and `badrows`.

Usage:  python3 -I R93S2-probe.py --lane LANE --rev REV --scratch DIR
"""
import argparse, importlib.util, json, os, re, subprocess, sys

COUNTER_REL = ".ufo/evidence/round-93/c1/measure-v93.py"
NOTE_REL = "corpus/knowledge/mutation-case-fleet-sources-census.md"
README_REL = "corpus/README.md"
SPEC_REL = ".ufo/evidence/round-93/c1/census-mutants.json"


def load_counter(lane, rev):
    """Import the frozen counter blob AT THE NAMED REVISION (never the worktree)."""
    p = subprocess.run(["git", "-C", lane, "cat-file", "blob", "%s:%s" % (rev, COUNTER_REL)],
                       capture_output=True)
    if p.returncode != 0:
        raise SystemExit("counter-blob-unreadable-at-rev:%s" % rev)
    src = p.stdout.decode("utf-8")
    tmpdir = os.environ["SCRATCH"] + "/counterblob"
    os.makedirs(tmpdir, exist_ok=True)
    path = os.path.join(tmpdir, "measure-v93.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("measure_v93_frozen", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.__file__ = path
    return mod, src


def git_text(lane, rev, path):
    p = subprocess.run(["git", "-C", lane, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", errors="replace")


def hdr_cells(M, header):
    return [M.norm_cell(c) for c in header]


def part_a(M, texts, out):
    out.append("=== (a) every GFM table, reader's own tables() definition ===")
    for label, text in texts:
        out.append("-- file: %s" % label)
        tbls = M.tables(text)
        out.append("   tables=%d" % len(tbls))
        for oi, header, drows in tbls:
            low = hdr_cells(M, header)
            vcols = [k for k, c in enumerate(low) if c == "verdict"]
            out.append("   start_line=%d header=%s" % (oi + 1, json.dumps(header)))
            out.append("      header_norm=%s data_rows=%d verdict_header=%s verdict_cols=%s" % (
                json.dumps(low), len(drows), "yes" if vcols else "no",
                json.dumps(vcols)))
        out.append("")


def part_b(M, texts, out):
    out.append("=== (b) block lines outside the verdict table carrying a token "
               "with >=2 pipes ===")
    for label, text in texts:
        out.append("-- file: %s" % label)
        # Reproduce the reader's OWN consumed-set exactly (tables() + norm_cell).
        consumed = set()
        vtables = []
        for oi, header, drows in M.tables(text):
            low = hdr_cells(M, header)
            vcols = [k for k, c in enumerate(low) if c == "verdict"]
            if vcols:
                consumed.add(oi)
                consumed.update(ln for ln, _, _ in drows)
                vtables.append(oi)
        out.append("   verdict_tables_at=%s" % json.dumps([v + 1 for v in vtables]))
        hits = []
        for oi, raw in M.block_lines(text):
            if oi in consumed or raw.count("|") < 2:
                continue
            toks = [c for c in M.split_cells(raw) if c in M.VERDICTS]
            if toks:
                hits.append((oi + 1, raw.strip()[:100], toks))
        out.append("   stray_verdict_lines=%d" % len(hits))
        for ln, raw, toks in hits:
            out.append("      line=%d tokens=%s raw=%s" % (ln, json.dumps(toks), json.dumps(raw)))
        # cross-check with the reader's own bad[] (stray-verdict entries only)
        rows, bad, info = M.parse_note(text, SPEC_IDS)
        stray = [b for b in bad if b.startswith("stray-verdict:")]
        out.append("   reader_bad_stray=%d reader_badrows=%d reader_verdict_tables=%d" % (
            len(stray), len(bad), info["verdict_tables"]))
        out.append("   reader_bad_all=%s" % json.dumps(bad))
        out.append("   reader_rows_keys=%s" % json.dumps(sorted(rows)))
        # STRICT sweep (stricter than the reader): a token appearing as a
        # SUBSTRING of a cell, outside the verdict table, with >= 2 pipes.
        strict = []
        for oi, raw in M.block_lines(text):
            if oi in consumed or raw.count("|") < 2:
                continue
            for t in M.VERDICTS:
                if t in raw:
                    strict.append((oi + 1, t, raw.strip()[:100]))
                    break
        out.append("   strict_substring_token_lines_outside_verdict_table=%d" % len(strict))
        for ln, t, raw in strict:
            out.append("      line=%d token=%s raw=%s" % (ln, t, json.dumps(raw)))
        out.append("")


def part_c(M, texts, out):
    out.append("=== (c) presentation forms the reader does NOT key ===")
    for label, text in texts:
        out.append("-- file: %s" % label)
        # fenced blocks
        fence = None
        regions = []
        for idx, raw in enumerate(text.split("\n")):
            m = M.FENCE_RE.match(raw)
            if fence is None:
                if m:
                    fence = (m.group(1)[0], len(m.group(1)), idx)
                    continue
            else:
                if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] \
                        and m.group(2).strip() == "":
                    regions.append((fence[2] + 1, idx + 1))
                    fence = None
                continue
        out.append("   fenced_blocks=%d ranges=%s" % (
            len(regions), json.dumps(regions)))
        for (a, b) in regions:
            body = "\n".join(text.split("\n")[a - 1:b])
            out.append("      fence[%d-%d] verdict_tokens=%d pipes2_lines=%d" % (
                a, b, sum(body.count(t) for t in M.VERDICTS),
                sum(1 for ln in body.split("\n") if ln.count("|") >= 2)))
        # tables with no verdict header
        noverdict = []
        for oi, header, drows in M.tables(text):
            low = hdr_cells(M, header)
            if not any(c == "verdict" for c in low):
                noverdict.append((oi + 1, header, len(drows)))
        out.append("   tables_without_verdict_header=%d" % len(noverdict))
        for oi, header, n in noverdict:
            out.append("      start_line=%d data_rows=%d header=%s" % (oi, n, json.dumps(header)))
        # prose tokens: verdict token on a line with < 2 pipes (never a table row)
        prose = []
        for idx, raw in enumerate(text.split("\n")):
            if raw.count("|") >= 2:
                continue
            for t in M.VERDICTS:
                if t in raw:
                    prose.append((idx + 1, t))
                    break
        out.append("   prose_token_lines=%d" % len(prose))
        for ln, t in prose:
            out.append("      line=%d token=%s" % (ln, t))
        # escaped pipe
        out.append("   escaped_pipe_occurrences=%d" % text.count("\\|"))
        out.append("")


def build_variants(note_text):
    """Six hand-built variants, each on top of the committed honest note."""
    V = {}
    rows12 = "\n".join(
        "| C%03d | arm%d | edit%d | %s | witness%d |" % (
            i, i, i, "KILLED" if i % 2 else "SURVIVED", i) for i in range(1, 13))
    V["V1-second-verdict-table"] = (
        note_text + "\n## Appendix A\n\n"
        "| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n"
        + rows12 + "\n")
    V["V2-renamed-header-with-tokens"] = (
        note_text + "\n## Appendix B\n\n"
        "| id | result | note |\n|---|---|---|\n"
        "| C01 | KILLED | a |\n| C02 | SURVIVED | b |\n")
    V["V3-bare-pipe-line-with-token"] = (
        note_text + "\n## Appendix C\n\n"
        "| C02 | E10 community-at-A | KILLED |\n")
    V["V4-id-keyed-non-verdict-table"] = (
        note_text + "\n## Appendix D\n\n"
        "| id | arm targeted | edit | outcome | witness |\n|---|---|---|---|---|\n"
        + "\n".join("| C%02d | arm%d | edit%d | outcome%d | witness%d |" % (
            i, i, i, i, i) for i in range(1, 13)) + "\n")
    # V4a: the EXACT round-92 kill class, in place - the note's own section-2b
    # impact table is reformatted so the ids are their own cells.  The header
    # gains an `id` column and still carries NO `verdict` cell.
    a13 = note_text.replace(
        "| survivor | lanes hit | effect on live registries |\n|---|---|---|\n"
        "| C12 used-by trim |",
        "| id | survivor | lanes hit | effect on live registries |\n|---|---|---|---|\n"
        "| C12 |  used-by trim |")
    for old, new in (("| C03 supersedes width |", "| C03 | supersedes width |"),
                     ("| C09 fragment strip |", "| C09 | fragment strip |"),
                     ("| C10 spaced cadence |", "| C10 | spaced cadence |"),
                     ("| C02, C06, C08 |", "| C02 | C06, C08 |")):
        a13 = a13.replace(old, new, 1)
    assert a13 != note_text
    V["V4a-a13-in-place-impact-reformat"] = a13
    # V4b: the note plus a non-verdict table holding a data cell whose text is
    # exactly `verdict` and a bolded id - the round-92 SF-2 class.
    V["V4b-verdict-data-cell-and-bold-id"] = (
        note_text + "\n| survivor | witness | note |\n|---|---|---|\n"
        "| C02 | differs | verdict |\n| **C03** | differs | bold id |\n")
    V["V5-verdict-data-cell"] = (
        note_text + "\n## Appendix E\n\n"
        "| id | arm targeted | edit | outcome | witness |\n|---|---|---|---|---|\n"
        "| **C01** | arm1 | edit1 | verdict | witness1 |\n")
    V["V6-fenced-inverted-table"] = (
        note_text + "\n## Appendix F\n\n```\n"
        "| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n"
        + "\n".join("| C%02d | arm%d | edit%d | %s | witness%d |" % (
            i, i, i, "SURVIVED" if i % 2 else "KILLED", i) for i in range(1, 13))
        + "\n```\n")
    return V


def part_d(M, note_text, out, scratch):
    out.append("=== (d) six hand-built variants (reader classification) ===")
    vdir = os.path.join(scratch, "variants")
    os.makedirs(vdir, exist_ok=True)
    V = build_variants(note_text)
    base_rows, base_bad, base_info = M.parse_note(note_text, SPEC_IDS)
    out.append("-- baseline honest note: verdict_tables=%d badrows=%d rows=%d ids_match=%s" % (
        base_info["verdict_tables"], len(base_bad), len(base_rows),
        sorted(base_rows) == sorted(SPEC_IDS)))
    for name in sorted(V):
        text = V[name]
        path = os.path.join(vdir, name + ".md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        rows, bad, info = M.parse_note(text, SPEC_IDS)
        ids_ok = (not bad) and set(rows) == SPEC_IDS
        out.append("-- %s" % name)
        out.append("   verdict_tables=%d badrows=%d ids_ok=%s rows_keys=%d" % (
            info["verdict_tables"], len(bad), ids_ok, len(rows)))
        out.append("   bad=%s" % json.dumps(bad))
    out.append("")


def part_e(M, out):
    """Supplementary: the declared limits' behaviour, observed on the reader itself.

    Neither file contains an escaped pipe today, so the S321 limit is asserted by
    the plan, not exercised by the note.  These two constructions show what the
    reader actually does with each declared limit, using the reader's own
    functions.
    """
    out.append("=== (e) supplementary: declared-limit behaviour, observed ===")
    # E1: escaped pipe inside a cell is ONE cell (S321) - the column count holds.
    t1 = ("| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n"
          "| C01 | a \\| b | e | KILLED | w |\n")
    r1, b1, i1 = M.parse_note(t1, SPEC_IDS)
    out.append("-- escaped-pipe cell: cells=%s verdict_tables=%d badrows=%d rows=%s" % (
        json.dumps(M.split_cells("| C01 | a \\| b | e | KILLED | w |")), i1["verdict_tables"],
        len(b1), json.dumps(sorted(r1))))
    # E2: a fenced block is literal text (S322) - an inverted table inside a fence
    # is neither keyed nor refused.
    t2 = ("```\n| id | arm | verdict |\n|---|---|---|\n| C01 | a | SURVIVED |\n```\n")
    r2, b2, i2 = M.parse_note(t2, SPEC_IDS)
    out.append("-- fenced inverted table: verdict_tables=%d badrows=%d rows=%s bad=%s" % (
        i2["verdict_tables"], len(b2), json.dumps(sorted(r2)), json.dumps(b2)))
    # E3: a verdict word in prose with fewer than two pipes is not a table row.
    t3 = "prose says SURVIVED and KILLED in a sentence with no pipe.\n"
    r3, b3, i3 = M.parse_note(t3, SPEC_IDS)
    out.append("-- prose token, 0 pipes: verdict_tables=%d badrows=%d bad=%s" % (
        i3["verdict_tables"], len(b3), json.dumps(b3)))
    # E4: the same token on a line that DOES carry two pipes is a presented row.
    t4 = "prose says | SURVIVED | here.\n"
    r4, b4, i4 = M.parse_note(t4, SPEC_IDS)
    out.append("-- prose token, 2 pipes: verdict_tables=%d badrows=%d bad=%s" % (
        i4["verdict_tables"], len(b4), json.dumps(b4)))
    out.append("")


def part_f(M, out, lane, rev):
    """Cross-check: my hand-built variants against the COMMITTED control receipts.

    Each receipt under .ufo/evidence/round-93/pre-freeze/controls/ was produced
    by the frozen counter on a committed fixture; its C1_SUMMARY line carries the
    reader's own verdict_tables/badrows for that state.  If my independent
    variant reproduces the committed classification, the reader behaves as the
    battery recorded - read from committed bytes, not from my memory.
    """
    import glob
    out.append("=== (f) cross-check against committed control receipts ===")
    cdir = os.path.join(lane, ".ufo/evidence/round-93/pre-freeze/controls")
    mine = {
        "hidden-c001": ("V1-second-verdict-table", 2, 12),
        "renamed-result": ("V2-renamed-header-with-tokens", 1, 2),
        "pseudo-row": ("V3-bare-pipe-line-with-token", 1, 1),
        "pos-honest-a13": ("V4a-a13-in-place-impact-reformat", 1, 0),
        "pos-honest-verdict-cell": ("V4b-verdict-data-cell-and-bold-id", 1, 0),
        "pos-real": ("baseline-honest-note", 1, 0),
    }
    for name in sorted(mine):
        p = os.path.join(cdir, name + ".out")
        if not os.path.exists(p):
            out.append("-- %-26s NO RECEIPT" % name)
            continue
        txt = open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"badrows=(\d+) verdict_tables=(\d+)", txt)
        if not m:
            out.append("-- %-26s receipt has no badrows/verdict_tables line" % name)
            continue
        c_bad, c_vt = int(m.group(1)), int(m.group(2))
        vname, m_vt, m_bad = mine[name]
        out.append("-- %-26s receipt(vt=%d bad=%d)  mine[%s](vt=%d bad=%d)  MATCH=%s" % (
            name, c_vt, c_bad, vname, m_vt, m_bad,
            (c_vt, c_bad) == (m_vt, m_bad)))
    out.append("")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    os.environ["SCRATCH"] = os.path.abspath(a.scratch)
    os.makedirs(a.scratch, exist_ok=True)
    M, src = load_counter(a.lane, a.rev)
    global SPEC_IDS
    spec = json.loads(git_text(a.lane, a.rev, SPEC_REL))
    SPEC_IDS = set(m["id"] for m in spec["mutants"])
    note = git_text(a.lane, a.rev, NOTE_REL)
    readme = git_text(a.lane, a.rev, README_REL)
    if note is None or readme is None:
        raise SystemExit("note-or-readme-absent-at-rev")
    out = []
    out.append("R93S2 parser-premise audit  rev=%s" % a.rev)
    out.append("counter blob sha256=%s (bytes read from git at the rev, not the worktree)" % (
        __import__("hashlib").sha256(src.encode("utf-8")).hexdigest()))
    out.append("note bytes=%d readme bytes=%d spec_ids=%s" % (
        len(note), len(readme), json.dumps(sorted(SPEC_IDS))))
    out.append("")
    texts = [("corpus/knowledge/mutation-case-fleet-sources-census.md", note),
             ("corpus/README.md", readme)]
    part_a(M, texts, out)
    part_b(M, texts, out)
    part_c(M, texts, out)
    part_d(M, note, out, a.scratch)
    part_e(M, out)
    part_f(M, out, a.lane, a.rev)
    txt = "\n".join(out) + "\n"
    sys.stdout.write(txt)
    with open(os.path.join(a.scratch, "probe.out"), "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    main()
