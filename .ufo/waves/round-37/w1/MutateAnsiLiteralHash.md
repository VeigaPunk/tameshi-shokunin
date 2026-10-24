# MutateAnsiLiteralHash — blanking a literal `#` inside an ANSI-C quoted string (C2 depth)

Assignee: mutation-tester (leaf). Round 37, wave 1. Single assigned mutation probe:
one defect class, pristine / mutant / restored bytes, same bounded detector. No contract
change proposed; no sibling source touched.

## Detector under test

Frozen C2 counting command (`.ufo/evidence/round-37/contract.json`, counting_command):

```
python3 .ufo/evidence/round-37/code-view/measure.py --lane LANE --rev REV
```

`measure.py` loads `code_view` from `git show <rev>:tools/tally-audit-v3.py` and asserts the
two frozen fixtures at `.ufo/evidence/round-37/code-view/measure.py:48-58`:

| fixture | bytes | expectation |
|---|---|---|
| `ansi-c-escaped-quote-trailing-comment` | `": $'it\\'s' # inert st_tsu=0\nst_tsu=9\n"` | `#`-to-EOL blanked; `$'...'` stays open across `\'` |
| `ansi-c-literal-hash` | `": $'literal # data'\nst_tsu=9\n"` | byte-identical (quoted `#` is data) |

Per case: `got == want and len(got) == len(text) and got.count("\n") == text.count("\n")`
(`measure.py:58`). The same two cases are embedded in the tool's own selftest at
`tools/tally-audit-v3.py:889-903`. Contract axis: GNU Bash 5.3 §ANSI-C Quoting — a `#`
inside `$'...'` is literal, never a comment start.

Scanner under mutation: `code_view` at `tools/tally-audit-v3.py:152`; ANSI-C state branch at
`:172-180`; top-level word-boundary comment rule at `:199`.

## Isolation

Disposable clone of the lane (read-only on the lane; no worktree/index/jj/.ufo-state write):

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /tmp/r37-MutateAnsiLiteralHash/lane
git -C /tmp/r37-MutateAnsiLiteralHash/lane checkout --detach e6185d5f0b63a6963205110cb098f2f1eca27622
```

Observed base: `e6185d5f0b63a6963205110cb098f2f1eca27622`, clean checkout. Base tool sha256
`da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`, matching
`.ufo/evidence/round-37/counter-pin.json` `tool_sha256`. Frozen detector sha256
`1cb70e6bc366a89dd8f046f15645a69d1faa21cc3037990e0a4990b240452e6a`. No tool install or
update was needed; pacman was not run.

## Pristine baseline

```
$ python3 /tmp/r37-MutateAnsiLiteralHash/lane/.ufo/evidence/round-37/code-view/measure.py \
    --lane /tmp/r37-MutateAnsiLiteralHash/lane --rev e6185d5f0b63a6963205110cb098f2f1eca27622
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 \
  tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede \
  rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C2_R37_PASS=true          (exit 0)
```

Baseline is conclusive: both frozen arms pass on pristine bytes, so a mutant failure below
is a kill, not a pre-existing detector artefact.

## Mutant

Defect (single behavior-bearing insertion, 8 lines, inside the ANSI-C warning state): the
scanner applies the word-boundary comment-blanking rule while `quote == "ansi-c"`, so a `#`
that Bash treats as literal inside `$'...'` is erased to EOL. This is the "misplaced comment
rule / forgot that quoted `#` is data" defect class; the added guard is byte-identical to the
top-level comment-start condition at `:199`.

```
diff --git i/tools/tally-audit-v3.py w/tools/tally-audit-v3.py
index b0c7d48..5917cfa 100755
--- i/tools/tally-audit-v3.py
+++ w/tools/tally-audit-v3.py
@@ -173,6 +173,14 @@ def code_view(text):
             if c == '\\' and i + 1 < n:
                 i += 2
                 continue
+            if c == '#' and (i == 0 or text[i - 1] in ' \t\n;|&('):
+                j = text.find('\n', i)
+                if j < 0:
+                    j = n
+                for k in range(i, j):
+                    out[k] = ' '
+                i = j
+                continue
             if c == "'":
                 quote = None
             i += 1
```

Mutant blob lines 176-183 (base line 172 stays the `if quote == "ansi-c":` guard). Mutant
commit in the disposable clone only: `da6a65340eaf285fa9ffb39852293c7fffd7e3cb`, parent
`e6185d5f0b63a6963205110cb098f2f1eca27622`, `1 file changed, 8 insertions(+)`. Mutant tool
sha256 `8a179111bd89d99bc1c178a415680cd9e322af8f4a53fb03791eb5f1f891a8c2`.

## Mutant detection result

```
$ python3 /tmp/r37-MutateAnsiLiteralHash/lane/.ufo/evidence/round-37/code-view/measure.py \
    --lane /tmp/r37-MutateAnsiLiteralHash/lane --rev da6a65340eaf285fa9ffb39852293c7fffd7e3cb
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash FAIL
  expected=": $'literal # data'\nst_tsu=9\n"
  actual=": $'literal        \nst_tsu=9\n"
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=0/1 \
  tool_sha256=8a179111bd89d99bc1c178a415680cd9e322af8f4a53fb03791eb5f1f891a8c2 \
  rev=da6a65340eaf285fa9ffb39852293c7fffd7e3cb C2_R37_PASS=false            (exit 1)
```

Direct `code_view` repr probe on the mutant blob (same fixtures):

```
CASE escaped-quote-trailing-comment
  got = ": $'it\\'s'                 \nst_tsu=9\n"
  equal=True len_preserved=True newline_preserved=True
CASE literal-hash
  text = ": $'literal # data'\nst_tsu=9\n"
  got  = ": $'literal        \nst_tsu=9\n"
  equal=False len_preserved=True newline_preserved=True
```

**Verdict: KILLED** by the frozen two-case predicate (`C2_R37_PASS=false`, exit 1).
The killing power is entirely in the literal-hash arm: the escaped-quote arm still PASSes,
because its `#` sits outside the quoted string, so an ANSI-C-internal comment rule cannot
fire and the mutant's escaped-quote state machine is unchanged. All three numeric invariants
(equality, length, newline count) are preserved by the mutant; only byte equality of the
literal-hash fixture distinguishes it. That makes the literal-hash clause load-bearing for
this defect class — the escaped-quote fixture alone would let the mutant survive.

No adverse or anomalous detector behavior was observed. The mutant is a coverage fact, not a
contract finding: it confirms the frozen literal-hash assertion is necessary, and the
escaped-quote assertion is insufficient by itself, exactly as the two-case conjunction was
frozen.

## Restoration evidence

```
$ git -C /tmp/r37-MutateAnsiLiteralHash/lane checkout --detach e6185d5f0b63a6963205110cb098f2f1eca27622
$ git -C /tmp/r37-MutateAnsiLiteralHash/lane status --porcelain
                                                                      (empty)
$ sha256sum /tmp/r37-MutateAnsiLiteralHash/lane/tools/tally-audit-v3.py
da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede  tools/tally-audit-v3.py
$ python3 .../measure.py --lane /tmp/r37-MutateAnsiLiteralHash/lane --rev e6185d5f0b63a6963205110cb098f2f1eca27622
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 \
  tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede \
  rev=e6185d5f0b63a6963205110cb098f2f1eca27622 C2_R37_PASS=true          (exit 0)
```

Restored bytes are exact: sha256 equals the pristine/pin hash, clone worktree clean, detector
back to 2/2 PASS. Mutant commit is reachable there only via the disposable clone's reflog.

Live lane integrity (read-only; only this report was written to the lane):

```
lane HEAD                       = e6185d5f0b63a6963205110cb098f2f1eca27622  (unchanged)
lane tools/tally-audit-v3.py    = da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede
lane code-view/measure.py       = 1cb70e6bc366a89dd8f046f15645a69d1faa21cc3037990e0a4990b240452e6a
lane git status                 = only peer-authored untracked w1 reports + this report
```

Scratch clone `/tmp/r37-MutateAnsiLiteralHash/lane` is disposable and left restored; it holds
the mutant commit in reflog for inspection. This probe stops here.

Report: .ufo/waves/round-37/w1/MutateAnsiLiteralHash.md
