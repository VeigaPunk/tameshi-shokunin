import re, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-93/c1")
# import functions without running main (guard exists)
import importlib.util
spec = importlib.util.spec_from_file_location("m", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-93/c1/measure-v93.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

ids = set([f"C{i:02d}" for i in range(1,13)])
def verdict_table(rows):
    return "| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
def honest(verdicts=None):
    vs = verdicts or ["KILLED"]*12
    return verdict_table([f"| C{i+1:02d} | a | e | {vs[i]} | w |" for i in range(12)])

def test(name, note, expect):
    rows, bad, info = m.parse_note(note, ids)
    print(f"{name}: rows={len(rows)} bad={bad} info={info} expect={expect}")

# Probe 1: tilde fence content with inverted verdicts is skipped (declared S322) — but what about UNCLOSED fence swallowing real table?
test("unclosed fence swallowing verdict table", "```\n" + honest() + "\n", "rows=0 or swallowed")
test("unclosed tilde fence swallowing", "~~~\n" + honest(), "swallowed")
test("tilde fence with info string", "~~~json\n| C01 | a | e | SURVIVED | w |\n~~~\n" + honest(), "fenced ignored, honest parsed")
test("4-space indented fence (not fence per CommonMark?)", "    ```\n" + honest(), "fence NOT recognised -> stray verdict?")
test("3-space fence recognized", "   ```\n" + honest() + "\n   ```\n", "fenced")
test("fence close with info string (should NOT close)", "```\n| C01 | a | e | KILLED | w |\n``` extra\n| C01 | a | e | KILLED | w |\n", "close requires empty group2 - second ``` extra does not close")

# Probe 2: split_cells escaped
print("split escaped pipe:", m.split_cells("| a | b\\|c | d |"))
print("split backslash-pipe backslash:", m.split_cells("| a | b\\\\|c | d |"))
print("split trailing backslash:", m.split_cells("| a | b \\|"))
print("split no leading/trailing:", m.split_cells("a | b | c"))

# Probe 3: DELIM_RE - 2 dashes accepted? GFM requires 3
for d in ["|---|---|---|", "|--|--|--|", "|:-|-|-|", "--- | --- | ---"]:
    print(f"DELIM {d!r}: {bool(m.DELIM_RE.match(d))}")

# Probe 4: tables blank line break - data row with no pipe after delimiter?
note2 = "| id | verdict |\n|---|---|\n| C01 | KILLED |\n\n| C02 | KILLED |\n"
test("blank line breaks table, stray scan", note2, "C02 stray-verdict -> bad")

# Probe 5: verdict token case sensitivity
test("lowercase killed", verdict_table([f"| C{i+1:02d} | a | e | killed | w |" for i in range(12)]), "no-verdict")

# Probe 6: stray scan raw.count pipes <2 but split_cells tokens — pseudo-row with 1 pipe containing KILLED
test("prose 1 pipe", "Note: C01 | KILLED\n" + honest(), "prose not bad (count<2)")

# Probe 7: unicode / whitespace verdict with bold
test("bold verdict **KILLED**", verdict_table([f"| C{i+1:02d} | a | e | **KILLED** | w |" for i in range(12)]), "norm? split_cells token is '**KILLED**' not in VERDICTS -> no-verdict")

# Probe 8: header verdict with bold **verdict**
test("bold header", "| id | **verdict** |\n|---|---|\n| C01 | KILLED |\n", "norm_cell strips * -> verdict -> vtable")

# Probe 9: measured regex
for line in ["measured: 12/12 killed", "measured: 12/12 killed ", " measured: 12/12 killed", "measured: 5/12 KILLED"]:
    print(repr(line), bool(re.match(r"^measured: (\d+)/(\d+) killed\s*$", line, re.M)))

# Probe 10: located_quotes - quote must contain sid? Actually quote found on line with sid ANYWHERE
lesson = 'S322 says "the table is broken at the first empty line" here\n'
print("located_quotes:", m.located_quotes(lesson))

# Probe 11: selfpin - duplicate line
import hashlib
with open("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-93/c1/measure-v93.py","rb") as f:
    b=f.read()
norm = re.sub(m.SELF_PIN_RE, b"", b, flags=re.M)
print("selfpin norm sha:", hashlib.sha256(norm).hexdigest(), "match:", hashlib.sha256(norm).hexdigest()==m.SELF_SHA256)
# duplicate insertion: add same line at end, norm removes both -> same digest!
dup = b + b'SELF_SHA256 = "9a073d351dd23de2f61af95436e5cac1fa871193f7d52e0728553e9034cb99e2"\n'
norm_dup = re.sub(m.SELF_PIN_RE, b"", dup, flags=re.M)
print("dup-append same digest?", hashlib.sha256(norm_dup).hexdigest()==hashlib.sha256(norm).hexdigest())
print("dup lines in norm?", norm_dup.count(b'SELF_SHA256'))
# different hash line inserted
diff = b + b'SELF_SHA256 = "0000000000000000000000000000000000000000000000000000000000000000"\n'
norm_diff = re.sub(m.SELF_PIN_RE, b"", diff, flags=re.M)
print("diff-hash append same digest?", hashlib.sha256(norm_diff).hexdigest()==hashlib.sha256(norm).hexdigest())
# moved line
lines = b.split(b"\n")
idx = [i for i,l in enumerate(lines) if l.startswith(b"SELF_SHA256")]
print("self line idx:", idx)
