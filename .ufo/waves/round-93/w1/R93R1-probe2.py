import importlib.util, re
spec = importlib.util.spec_from_file_location("m", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-93/c1/measure-v93.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ids=set([f"C{i:02d}" for i in range(1,13)])
def vt(rows): return "| id | arm targeted | edit | verdict | witness |\n|---|---|---|---|---|\n"+"\n".join(rows)+"\n"
def honest(vs=None):
    vs=vs or ["KILLED"]*12
    return vt([f"| C{i+1:02d} | a | e | {vs[i]} | w |" for i in range(12)])
def test(n,note,exp):
    rows,bad,info=m.parse_note(note,ids)
    print(f"{n}: rows={len(rows)} {rows} bad={bad} info={info} | {exp}")

# SELF-PIN followup: dup-append: both lines stripped -> YES same digest. But does Python execute second SELF_SHA256 assignment? It just overwrites variable, same file works. So an edited file CAN append a duplicate SELF_SHA256 line with ANY hash and still pass selfpin AND run modified code? No wait - norm strips both lines, so any additional code anywhere else changes digest. Appending duplicate line alone doesn't change code semantics (same value). But appending a line AND code? code changes digest. Hmm - the attack: append second SELF_SHA256 line is redundant. Real question: can an edit keep same normalized digest? Answer: ONLY if edit is (a) another SELF_SHA256 line (any hex), or (b) ... whitespace? No, whitespace changes digest since only the line is removed. So the only digest-preserving edits are extra self-pin lines. That's a real but narrow hole: attacker can append duplicate pin lines to obscure? Executing same code though. Two assignments same value = no behaviour change. BUT: typing: first line assigns, second reassigns before use - both same value so no effect. If second line has DIFFERENT hash, it overwrites SELF_SHA256 variable at runtime but verification compares normalized digest, not variable value. So attacker could have SELF_SHA256="dead..." second line, but self_pin_ok compares file digest to module constant SELF_SHA256 AT RUNTIME (second value!). E.g. file: line1 SELF_SHA256="X", line2 SELF_SHA256="Y" (Y != verified). norm strips both -> digest X-pinned. Runtime SELF_SHA256 = Y, digest != Y -> fails. In reverse: line1="Y"(wrong), line2="X"(correct pinned). Runtime sees X, norm strips both -> digest=X -> passes, but variable ends = X (second). Hmm so behaviour still pinned. Actually check: re.sub with flags=re.M, ^...$ per line - both stripped. So digest depends only on rest. Runtime SELF_SHA256 = LAST assignment. For self_pin_ok to pass, runtime value must equal digest of rest. Attacker can append SECOND line with the correct digest value (which they must compute after edit - requiring knowledge of correct SELF_SHA256; that IS the pinned value). So no bypass - duplicate line requires knowing correct digest, gives no extra freedom, but ALLOWS an edit to the line text itself? e.g. change line1's hash to arbitrary, add line2 with correct hash: norm strips both, digest ok, runtime = correct. So the VERIFIED hash displayed in source line1 is wrong but code correct. Not a behaviour change. Severity low - but it IS a way an "edited" file (different bytes) keeps same normalised digest, violating the plan's "any edit"? Plan kill rule (c): counter blob differs from stated sha256 - sha256 is of the FILE (189036...) not normalized. If file bytes differ, blob sha differs -> kill (c) triggers. So within frozen-claim, duplicate-line counter is caught by blob check, not selfpin. Real finding: selfpin normalisation allows byte-different counter to pass selfpin; reliance on external blob sha. Worth listing as low/design note.
# What about SELF_SHA256 line with trailing spaces / \r? RE requires \n exactly. \r\n file: line won't match -> norm keeps it -> digest mismatch -> die. Honest checkout on Windows / autocrlf could refuse. Lane is linux; plan pins sha256 so no CRLF. False-red only if someone checks out with eol conversion - but then blob sha also differs. Note it.

# Probe: width rule - header 5 cols, delimiter 5, data row with escaped pipe in edit cell
test("escaped pipe in edit cell", vt(["| C01 | a | x\\|y | KILLED | w |"]+[f"| C{i+1:02d} | a | e | KILLED | w |" for i in range(1,12)]), "one cell, OK")
# delim inside table as data: a data row that looks like delimiter is skipped (isdelim) - could hide an id row?
test("delim row as data", vt(["| C01 | a | e | KILLED | w |","|---|---|---|---|---|"]+[f"| C{i+1:02d} | a | e | KILLED | w |" for i in range(2,12)]), "C02 missing -> ids fail")
# header width vs delim mismatch: extra delim col
test("width mismatch header 5 delim 4", "| id | verdict | a | b | c |\n|---|---|---|---|\n| C01 | KILLED | 1 | 2 | 3 |\n", "width bad")
# verdict col but data token lower
# tables() consecutive: second table's header directly after first table's rows without blank? rows continue while pipe present, so merged
note = "| id | verdict |\n|---|---|\n| C01 | KILLED |\n| id2 | verdict2 |\n|---|---|\n| C02 | KILLED |\n"
test("two tables no blank", note, "second header becomes data row: width ok, first=C01? first cell id2 not in spec -> out-of-set")
# stray scan: consumed includes header+rows of vtable. If vtable header has verdict but data row width mismatch is skipped via continue, consumed still covers it - stray scan skips. Fine.
# Non-vtable with verdict token in SECOND cell only, 2 pipes: stray
test("non-vtable verdict token", "| id | note |\n|---|---|\n| C01 | KILLED |\n" + honest(), "stray-verdict bad")
# Header is "Verdict" capital -> norm lower -> verdict: accepts. Honest? fine.
# Header with trailing spaces
test("header 'verdict ' padded", "| id | verdict  |\n|---|---|\n| C01 | KILLED |\n", "norm strips")
# delimiter line BEFORE header? order matters
# pipe-in-prose: line "a|b|KILLED" with 2 pipes but no table: stray scan splits -> toks KILLED -> bad. Plan says "verdict word in prose with fewer than two pipes is not a table row" - implies 2+ pipes prose IS refused. Declared.
# What about verdict token in HEADING line with pipes? same.
# HTML comment with pipes + KILLED? block_lines doesn't strip HTML -> stray. False-red? note could contain <!-- | KILLED | --> prose. Worth noting.
test("html comment with verdict", honest() + "<!-- | KILLED | -->\n", "stray-verdict false-red?")
# Code inline backtick with pipes: `| KILLED |` in backticks -> raw.count| >=2, split_cells breaks on pipes inside backticks (no code-span handling) -> stray. False-red for legitimate inline code mention.
test("inline code mention", honest() + "see `| KILLED |` for details\n", "stray-verdict false-red?")
# Tilde fence close with trailing spaces / different length
note_t = "~~~\n| C01 | a | e | KILLED | w |\n~~~~\n" + honest()
test("tilde fence close longer", note_t, "closed, honest parsed")
note_t2 = "~~~~\n```\n~~~~\n" + honest()
test("fence char mismatch", note_t2, "backtick does not close tilde; tilde closes; honest ok")
# FENCE_RE: closing fence group(2) must be empty - trailing spaces ok (strip). Info on open ok.
# block_lines: fence inside indented list (4 spaces) not recognised -> content visible -> stray. False-red if note has indented fenced example.
test("indented fence 4sp content visible", "    ```\n| C01 | a | e | KILLED | w |\n    ```\n" + honest(), "stray-verdict")
# idset: spec_ids passed as spec_ids and spec_ids or set(ids) — if spec_ids empty set, falsy -> set(ids) which is also empty. fine.
# measured regex reads block = visible lines joined; line "measured: 12/12 killed" inside HTML? fine. Two measured lines (one fenced) -> len==1 ok. measured with leading spaces false-red? Plan note uses exact. Leading-space measured in honest note -> figure=false. False-red only if note format differs; note is fixed.
# source: located_quotes - sid anywhere in line, quote anywhere: line 'S321 "foo"' where foo is from S321 page but actually quote is generic? norm_text(q) in text: short common phrase could match by accident (e.g. "the table") -> false-green for source if lesson quotes a common phrase present in snapshot incidentally. Lesson is fixed committed though; claim is cov. Note as mechanism weakness.
# coverage: line.lstrip().startswith("|") and path substring. A row naming path in a CODE block of README counts (no fence handling) -> could be fenced denial or fenced assertion appended. False-green: append fenced row with path + "noted" counts as last_row? It starts with | -> last_row = fenced row. If fenced DENIAL appended, coverage false -> false-red; if fenced assertion after denial, coverage true -> false-green. Genuine fence gap in coverage.
print("block_lines fence:", m.block_lines("```\na\n```\nb"))
