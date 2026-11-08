import importlib.util, re
spec = importlib.util.spec_from_file_location("c1", "/fast/scratch/hyaku/tameshi-r92/T92R1/freeze25.py")
c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
ids = {f"C{i:02d}" for i in range(1,13)}
H = "| id | arm targeted | edit | verdict | witness |"
S = "|---|---|---|---|---|"
def t(rows): return rows
def mk(extra, tbl=None):
    tbl = tbl or [H, S] + [f"| {cid} | a | e | {'KILLED' if i%2 else 'SURVIVED'} | w |" for i,cid in enumerate(sorted(ids))]
    return "\n".join(tbl + extra)

# 1 baseline honest shape
nt = mk([]); rows,bad,h = c1.parse_note(nt, ids)
print("1 honest rows:", len(rows), "bad:", bad, "headers:", h)

# 2 fenced contradictory second table (all inverted verdicts)
inv = ["```", H, S] + [f"| {cid} | a | e | {'SURVIVED' if i%2 else 'KILLED'} | w |" for i,cid in enumerate(sorted(ids))] + ["```"]
nt2 = mk(inv); rows2,bad2,h2 = c1.parse_note(nt2, ids)
print("2 fenced-contradictory keys:", len(rows2), "bad:", bad2, "headers:", h2)

# 3 tilde fence (~) not recognized?
tilde = ["~~~", H, S] + [f"| {cid} | a | e | {'SURVIVED' if i%2 else 'KILLED'} | w |" for i,cid in enumerate(sorted(ids))] + ["~~~"]
nt3 = mk(tilde); rows3,bad3,h3 = c1.parse_note(nt3, ids)
print("3 tilde-fenced headers:", h3, "bad-count:", len(bad3), "bad0:", bad3[0] if bad3 else "")

# 4 S320-shaped row in a second table
nt4 = mk(["| S320 | src | mined |"])
r4,b4,h4 = c1.parse_note(nt4, ids); print("4 S320 row ->", b4, "headers:", h4)

# 5 header with two 'verdict' cells (one row), tokens only in col1
H2 = "| id | arm targeted | edit | verdict | verdict |"
tbl5 = [H2, S] + [f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
r5,b5,h5 = c1.parse_note("\n".join(tbl5), ids); print("5 two-verdict-col header rows:", len(r5), "bad:", b5, "headers:", h5)

# 6 data row whose witness cell is exactly 'verdict'
tbl6 = [H,S]+[f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
tbl6[2] = "| C01 | a | e | KILLED | verdict |"
r6,b6,h6 = c1.parse_note("\n".join(tbl6), ids); print("6 witness='verdict' row headers:", h6, "bad:", b6[:3])

# 7 escaped pipe inside witness cell (after verdict)
tbl7 = [H,S]+[f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
tbl7[3] = "| C02 | a | e | KILLED | a \\| b |"
r7,b7,h7 = c1.parse_note("\n".join(tbl7), ids); print("7 escaped pipe in witness bad:", b7, "c02row verdict:", r7.get("C02"))

# 8 escaped pipe inside verdict cell
tbl8 = [H,S]+[f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
tbl8[3] = "| C02 | a | e | KILLED \\| junk | w |"
r8,b8,h8 = c1.parse_note("\n".join(tbl8), ids); print("8 escaped pipe in verdict bad:", b8, "rows:", len(r8))

# 9 blockquote verdict table
tbl9 = ["> "+H, "> "+S]+["> | "+f"{cid} | a | e | KILLED | w |" for cid in sorted(ids)]
r9,b9,h9 = c1.parse_note("\n".join(tbl9), ids); print("9 blockquote rows:", len(r9), "bad:", b9, "headers:", h9)

# 10 header-count with tokens in second verdict column
tbl10 = [H2, S] + [f"| {cid} | a | e | KILLED | SURVIVED |" for cid in sorted(ids)]
r10,b10,h10 = c1.parse_note("\n".join(tbl10), ids); print("10 two verdict tokens bad:", b10[:2], "headers:", h10)

# 11 indented (4-space) code table - NOT fenced
tbl11 = [H,S]+[f"| {cid} | a | e | KILLED | w |" for cid in sorted(ids)]
tbl11 += ["    | C01 | a | e | SURVIVED | w |"]
r11,b11,h11 = c1.parse_note("\n".join(tbl11), ids); print("11 indented-contradictory-table bad:", b11, "rows:", len(r11))

# 12 measured regex vs fences: fenced measured line + real measured line
nt12 = "measured: 12/12 killed\n```\nmeasured: 6/12 killed\n```\n"
heads = re.findall(r"^measured: (\d+)/(\d+) killed\s*$", nt12, re.M)
print("12 measured heads (fence invisible?):", heads)
# 13 CRLF note lines
nt13 = mk([]).replace("\n","\r\n")
r13,b13,h13 = c1.parse_note(nt13, ids); print("13 CRLF rows:", len(r13), "bad:", b13)

# 14 verdict token in prose text (non-table line with pipes?)
nt14 = mk(["The verdict KILLED matters."])
r14,b14,h14 = c1.parse_note(nt14, ids); print("14 prose-line bad:", b14)

# 15 ID shape catalog
for s in ["C01","C001","X1","a1","S320","C-01","C_01","No12","C01A","1234","verdict"]:
    print("15 idshape", s, bool(c1.ID_SHAPE.match(s)))
