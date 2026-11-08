import importlib.util
spec = importlib.util.spec_from_file_location("m", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-93/c1/measure-v93.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ids=set([f"C{i:02d}" for i in range(1,13)])
# 5-col header, 3-col delimiter, 5-col data rows -> is bad flagged?
note = "| id | a | b | verdict | w |\n|---|---|---|\n| C01 | x | y | KILLED | z |\n"
rows,bad,info = m.parse_note(note, ids)
print("3col-delim under 5col-header:", rows, bad, info)
# 5-col header, 5-col delim, data rows 5 -> fine
note2 = "| id | a | b | verdict | w |\n|---|---|---|---|---|\n| C01 | x | y | KILLED | z |\n"
print("5col delim:", m.parse_note(note2, ids))
# delimiter row that is valid 2-col under 5-col header is still accepted as "table", data rows keyed.
# What does tables() say delim is?
print("tables():", m.tables(note))
# So line 269: delim = drows[0][1] -> first DATA row. Width check compares header vs first data row (duplicated by the per-row check anyway on same row). The real delimiter width is validated only by DELIM_RE (>=2 cols, >=3 dashes) not by column count. False-green limited: GFM-invalid table still keyed; verdict cells still true to header. Does it ACCEPT a table whose header/delim mismatch would render differently in a GFM renderer? For verdict extraction, marginal. But it's a genuine docstring-vs-code hole AND a hostile case: delimiter with MORE columns than header? drows[0] still data.
# Additional check: can NOT-yet-created table (header+delim, zero data rows) cause issues? verdict_tables=1, rows={}, ids fails safe.
# Coverage fence probe (manual logic replicate):
readme = "header\n| knowledge/mutation-case-fleet-sources-census.md | noted |\n| knowledge/mutation-case-fleet-sources-census.md | withdrawn |\n```\n| knowledge/mutation-case-fleet-sources-census.md | noted |\n```\n"
last=None
for line in readme.split("\n"):
    if line.lstrip().startswith("|") and "knowledge/mutation-case-fleet-sources-census.md" in line:
        last=line
print("coverage last_row (fenced):", repr(last), "denial?", any(t in last.lower() for t in m.DENIAL_TOKENS))
# Fenced denial AFTER true row: coverage turns false (false-red). Fenced assertion AFTER denial: true (false-green). Both real since coverage does not use block_lines.
# Also: blockquote line "> | path |" does NOT start with | after lstrip (starts with >) -> missed. A README row in blockquote naming the note as last row is ignored -> coverage graded by earlier row. Minor.
# README line without leading pipe: "a | b | knowledge/..." -> lstrip starts with 'a' not '|' -> missed. GFM table rows without leading pipe ignored. Minor false-red/green.
# Note path substring: a row naming "knowledge/mutation-case-fleet-sources-census.md.bak"? substring matches -> counts! Appended "path.bak" row with denial would consume last_row. Actually substring 'in line' matches superstring. An innocent row mentioning longer filename could be graded. Check: line "| x/knowledge/mutation-case-fleet-sources-census.mdx | withdrawn |" -> last_row. False-red possible. Low.
print("superstring match:", "| knowledge/mutation-case-fleet-sources-census.mdx | withdrawn |".count("knowledge/mutation-case-fleet-sources-census.md"))
# split_cells on escaped backslash before pipe: '\\\\|' -> first \\ consumed? Code: ch=='\\' and next=='|' -> literal |. For 'a\\|b' (double backslash then pipe): i at first \\, next is \\ not | -> append '\\'; second \\, next is | -> append '|' consume. Result 'a\\|b'? Actually yields a + \\ + | + b => 'a\|b' single backslash + pipe, NOT split. Correct GFM: \\\\ is escaped backslash, then | IS separator. Reader treats as literal pipe -> merges cells -> width/cells shift. False-red possible on cells containing literal backslash before pipe (e.g. regex C:\\|). Note the note has no such cells (edit column could). Mechanism-level.
print("backslash-pipe:", m.split_cells("| a | C:\\\\|x | KILLED |"))
