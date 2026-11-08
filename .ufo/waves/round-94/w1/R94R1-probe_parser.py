#!/usr/bin/env python3
"""R94R1 parser probes against the committed measure-v94 reader (read-only import).

Imports split_cells, block_lines, tables, parse_note, located_quotes, norm_text,
norm_cell from the committed bytes and exercises each suspected false-green /
false-red path. Every probe prints: <name> => <result> plus a short note.
"""
import importlib.util
import json
import pathlib
import sys

MEASURE = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-94/c1/measure-v94.py"
)
spec = importlib.util.spec_from_file_location("measure_v94", MEASURE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SPEC_IDS = {f"C{i:02d}" for i in range(1, 13)}

HONEST = """# Case note

| id | arm targeted | edit | verdict | witness |
|---|---|---|---|---|
| C01 | a | e | KILLED | w |
| C02 | a | e | SURVIVED | w |
| C03 | a | e | KILLED | w |
| C04 | a | e | KILLED | w |
| C05 | a | e | SURVIVED | w |
| C06 | a | e | SURVIVED | w |
| C07 | a | e | KILLED | w |
| C08 | a | e | SURVIVED | w |
| C09 | a | e | SURVIVED | w |
| C10 | a | e | KILLED | w |
| C11 | a | e | SURVIVED | w |
| C12 | a | e | SURVIVED | w |
"""

results = []


def probe(name, fn):
    try:
        out = fn()
        results.append((name, out))
        print(f"{name} => {out}")
    except Exception as e:  # noqa: BLE001
        results.append((name, f"EXC {type(e).__name__}: {e}"))
        print(f"{name} => EXC {type(e).__name__}: {e}")


def note_with(extra):
    return HONEST + extra


def parse(text):
    rows, bad, info = mod.parse_note(text, SPEC_IDS)
    return bad, info, rows


def verdict(token_map):
    rows = {f"C{i:02d}": "KILLED" if i <= 5 else "SURVIVED" for i in range(1, 13)}
    rows.update(token_map)
    return rows


# --- Baseline -------------------------------------------------------------
def baseline():
    bad, info, rows = parse(HONEST)
    return f"bad={bad} info={info} rows12={len(rows)}"


probe("baseline", baseline)


def parse_honest_plus(extra):
    bad, info, rows = parse(note_with(extra))
    return f"bad={bad} vt={info['verdict_tables']} rows={len(rows)}"


# P1: tilde fence hiding inverted clone (fenced inverted table must be ignored — declared limit)
def p1():
    inv = "\n```\n| id | arm | edit | verdict | witness |\n|---|---|---|---|---|\n"
    inv += "".join(f"| C{i:02d} | a | e | {'SURVIVED' if i <= 5 else 'KILLED'} | w |\n" for i in range(1, 13))
    inv += "```\n"
    return parse_honest_plus(inv)


probe("P1-tilde-fence-inverted", p1)


# P2: unclosed fence swallowing verdict table -> note refused? (false red risk)
def p2():
    return parse("prose\n```\n" + HONEST)  # fence never closed; honest table inside


probe("P2-unclosed-fence-swallows-table", p2)


# P3: indented fence (4 spaces) before verdict table — CommonMark 4-space = code block, not fence
def p3():
    return parse("prose\n    ```\n" + HONEST)


probe("P3-indented-4sp-fence", p3)


# P4: tilde fence opened with ``` ``` ``` inside? closing requires same char & >=len
def p4():
    txt = "```\n| id | x |\n|---|---|\n| a | KILLED |\n~~~\n" + HONEST
    return parse(txt)


probe("P4-mixed-fence-chars", p4)


# P5: delimiter with only 1 dash -> DELIM_RE requires {3,} so table unrecognised
def p5():
    rows = ["| id | arm | edit | verdict | witness |", "|-|-|-|-|-|"]
    rows += [f"| C{i:02d} | a | e | {'KILLED' if i<=5 else 'SURVIVED'} | w |" for i in range(1, 13)]
    return parse("\n".join(rows) + "\n")


probe("P5-short-delim-dash", p5)


# P6: escaped pipe in a witness cell — must NOT shift columns
def p6():
    lines = HONEST.replace("| KILLED | w |", "| KILLED | a \\| b |", 1)
    return parse(lines)


probe("P6-escaped-pipe-witness", p6)


# P7: escaped backslash before pipe `\\|` — reader treats `\|` as literal pipe ANYWHERE
def p7():
    txt = HONEST.replace("| a | e |", "| a \\| e |", 1)  # single backslash before pipe
    return parse(txt)


probe("P7-backslash-pipe-in-edit", p7)


# P8: actually || in edit cell (double pipe) - reader splits
def p8():
    txt = HONEST.replace("| a | e |", "| a || e |", 1)
    return parse(txt)


probe("P8-double-pipe-edit-cell", p8)


# P9: leading/trailing pipe absent (GFM allows)
def p9():
    lines = []
    for ln in HONEST.split("\n"):
        if ln.startswith("|"):
            lines.append(ln.strip("| "))
    return parse("\n".join(lines))


probe("P9-no-outer-pipes", p9)


# P10: extra trailing pipe makes empty last cell
def p10():
    txt = HONEST.replace("| w |", "| w | |", 1)
    return parse(txt)


probe("P10-extra-trailing-pipe", p10)


# P11: header with two verdict columns (battery sharp-two-verdict-cols)
def p11():
    rows = ["| id | verdict | edit | verdict | witness |", "|---|---|---|---|---|"]
    rows += [f"| C{i:02d} | x | e | KILLED | w |" for i in range(1, 13)]
    return parse("\n".join(rows) + "\n")


probe("P11-two-verdict-cols", p11)


# P12: non-verdict table with data cell exactly "verdict" (pos-honest-verdict-cell class)
def p12():
    extra = "\n| kind | value |\n|---|---|\n| verdict | x |\n"
    return parse_honest_plus(extra)


probe("P12-data-cell-verdict", p12)


# P13: id-keyed table asserting no verdict (pos-honest-a13 class)
def p13():
    rows = ["| survivor | lanes | effect |", "|---|---|---|"]
    rows += [f"| C{i:02d} x | 1 | y |" for i in (2, 3, 12)]
    return parse_honest_plus("\n" + "\n".join(rows) + "\n")


probe("P13-idkeyed-no-verdict-table", p13)


# P14: stray verdict in prose with >=2 pipes outside table (pseudo-row)
def p14():
    return parse_honest_plus("blah | KILLED | blah\n")


probe("P14-stray-pseudo-row", p14)


# P15: stray verdict in prose with 1 pipe only (declared limit: not a row)
def p15():
    return parse_honest_plus("blah | KILLED blah\n")


probe("P15-stray-one-pipe-prose", p15)


# P16: stray verdict line INSIDE verdict table delimiter-miscount rows consumed?
# A verdict token in a non-verdict table's data row, 3+ cells
def p16():
    extra = "\n| a | b | c |\n|---|---|---|\n| x | SURVIVED | y |\n"
    return parse_honest_plus(extra)


probe("P16-verdict-in-other-table", p16)


# P17: verdict token echoed inside backticks in a consumed row? verdict table consumed set
# hides a second verdict token appended in witness cell OF THE VERDICT TABLE ITSELF
def p17():
    txt = HONEST.replace("| C01 | a | e | KILLED | w |", "| C01 | a | e | KILLED | w | SURVIVED |", 1)
    # width mismatch: 6 cells vs header 5 -> width rule?
    return parse(txt)


probe("P17-extra-verdict-token-in-witness", p17)


# P18: verdict token inside an edit cell of verdict table (two tokens, one in vcol)
def p18():
    txt = HONEST.replace("| C01 | a | e | KILLED | w |", "| C01 | a | KILLED | KILLED | w |", 1)
    return parse(txt)


probe("P18-verdict-token-in-edit-cell", p18)


# P19: narrower row (fewer cells) with verdict in column
def p19():
    txt = HONEST.replace("| C01 | a | e | KILLED | w |", "| C01 | a | KILLED |", 1)
    return parse(txt)


probe("P19-narrow-row-verdict-present", p19)


# P20: wider row with two verdict tokens (sharp-width-lastrow class)
def p20():
    txt = HONEST.replace("| C12 | a | e | SURVIVED | w |", "| C12 | a | e | SURVIVED | w | KILLED |", 1)
    return parse(txt)


probe("P20-wide-row-two-tokens", p20)


# P21: duplicate id row inside verdict table
def p21():
    txt = HONEST + "| C02 | a | e | KILLED | w |\n"
    return parse(txt)


probe("P21-dup-id-row", p21)


# P22: out-of-set id row appended inside table bounds (C001)
def p22():
    txt = HONEST + "| C001 | a | e | KILLED | w |\n"
    return parse(txt)


probe("P22-out-of-set-C001", p22)


# P23: verdict header is "Verdict" (capitalised) - norm_cell lowercases
def p23():
    return parse(HONEST.replace("| verdict |", "| Verdict |"))


probe("P23-capital-Verdict-header", p23)


# P24: verdict header with extra spaces / bold **verdict**
def p24():
    return parse(HONEST.replace("| verdict |", "| **verdict** |"))


probe("P24-bold-verdict-header", p24)


# P25: blank line inside verdict table (GFM breaks table; second half becomes orphan rows)
def p25():
    lines = HONEST.split("\n")
    # insert blank after C06 row (index ~8)
    lines.insert(8, "")
    return parse("\n".join(lines))


probe("P25-blank-line-inside-table", p25)


# P26: table header indented 4 spaces (CommonMark: indented code block, but tables() just regexes |)
def p26():
    rows = ["    | id | arm | edit | verdict | witness |", "    |---|---|---|---|---|"]
    rows += [f"    | C{i:02d} | a | e | {'KILLED' if i<=5 else 'SURVIVED'} | w |" for i in range(1, 13)]
    return parse("\n".join(rows) + "\n")


probe("P26-indented-table", p26)


# P27: quote matching — unrelated quote on a line naming S322 but not from snapshot
def p27():
    lesson = 'S322 ground: "the exact quote here is unrelated" and some prose\n'
    qs = mod.located_quotes(lesson)
    snap_text = "A fenced code block begins with a code fence"
    return f"quotes={qs} hit={any(mod.norm_text(q) in mod.norm_text(snap_text) for q in qs.get('S322', []))}"


probe("P27-located-quotes-unrelated", p27)


# P28: quote split across lines / 26-word quote rejected
def p28():
    words = " ".join(f"w{i}" for i in range(26))
    lesson = f'S320: "{words}"\n'
    qs = mod.located_quotes(lesson)
    return f"long-quote-accepted={bool(qs.get('S320'))}"


probe("P28-26-word-quote", p28)


# P29: coverage _names_note first-token rule (probe via re-implementation)
def p29():
    def names(cell):
        c = cell.strip().strip("`").strip()
        first = c.split()[0].strip("`") if c.split() else ""
        return first == "knowledge/mutation-case-fleet-sources-census.md"
    cases = {
        "`knowledge/mutation-case-fleet-sources-census.md` / Core": True,
        "`knowledge/mutation-case-fleet-sources-census.md-backup`": False,
        "`knowledge/mutation-case-fleet-sources-census.mdx`": False,
        "See `knowledge/mutation-case-fleet-sources-census.md` for details": False,
    }
    return {k: names(k) for k in cases}


probe("P29-coverage-names-note", p29)


# P30: self-pin regex — CRLF file? SELF_PIN_RE requires \n; norm leaves \r
def p30():
    import re as _re
    PAT = rb'^SELF_SHA256 = "[0-9a-f]{64}"\n'
    sample = b'SELF_SHA256 = "' + b"a" * 64 + b'"\r\nX'
    return f"crlf-stripped={_re.sub(PAT, b'', sample, flags=_re.M) != sample}"
probe("P30-selfpin-crlf", p30)


# P31: duplicated SELF_SHA256 line (second copy outside pin regex? both stripped by re.sub M)
def p31():
    import re as _re, hashlib
    PAT = rb'^SELF_SHA256 = "[0-9a-f]{64}"\n'
    b = b'SELF_SHA256 = "' + b"a" * 64 + b'"\ncode\nSELF_SHA256 = "' + b"b" * 64 + b'"\nmore'
    return f"both-stripped={_re.sub(PAT, b'', b, flags=_re.M)}"
probe("P31-selfpin-duplicated", p31)


# P32: fence with info string on closing fence ``` foo — reader requires empty info
def p32():
    txt = "```\n| id | x |\n|---|---|\n| a | KILLED |\n``` foo\n" + HONEST
    return parse(txt)


probe("P32-closing-fence-with-info", p32)


# P33: tilde fence inside backtick fence — inner tilde should not close backtick fence
def p33():
    txt = "```\n~~~\n| id | x |\n|---|---|\n| a | KILLED |\n```\n" + HONEST
    return parse(txt)


probe("P33-tilde-inside-backtick", p33)


# P34: measured regex over block_lines (fenced measured: ignored -> figure false)
def p34():
    import re as _re
    block = "\n".join(t for _, t in mod.block_lines("```\nmeasured: 5/12 killed\n```\n"))
    heads = _re.findall(r"^measured: (\d+)/(\d+) killed\s*$", block, re.M)
    return f"fenced-measured-heads={heads}"


probe("P34-fenced-measured", p34)


# P35: verdict token appears ONLY inside fenced block in a stray-line context -> block_lines hides it, honest
def p35():
    return parse_honest_plus("```\n| x | KILLED | y |\n```\n")


probe("P35-fenced-stray-verdict", p35)


# P36: delim row with alignment colons and 1 dash
def p36():
    rows = ["| id | arm | edit | verdict | witness |", "|:-|-|-|-|-|"]
    rows += [f"| C{i:02d} | a | e | KILLED | w |" for i in range(1, 13)]
    return parse("\n".join(rows) + "\n")


probe("P36-colon-1dash-delim", p36)


# P37: table without leading pipe on delimiter only
def p37():
    rows = ["id | arm | edit | verdict | witness", "|---|---|---|---|---|"]
    rows += [f"C{i:02d} | a | e | KILLED | w" for i in range(1, 13)]
    return parse("\n".join(rows) + "\n")


probe("P37-no-leading-pipe", p37)


print("\n---DONE---")
