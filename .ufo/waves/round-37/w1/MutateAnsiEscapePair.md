# MutateAnsiEscapePair — ANSI-C escape-pair probe (round 37, wave 1)

Seat: `L1-tameshi-r37-attempt2.MutateAnsiEscapePair` (leaf, mutation tester).
Claim under probe: **C2** (frozen at `.ufo/evidence/round-37/contract.json`).
Observed base: lane `e6185d5f0b63a6963205110cb098f2f1eca27622`;
`tools/tally-audit-v3.py` sha256 `da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`,
byte-identical to the pre-run pin `ae9b771ab795fb5b4a6302165d8abdc0a2c6b229` and to
`.ufo/evidence/round-37/code-view/after.stdout` (`tool_sha256=da8c1ef4…`).
Ground-truth lexer: **GNU bash 5.3.20(1)-release** (x86_64-pc-linux-gnu) — S104's 5.3 line.
Scratch: `/tmp/r37-ansi-probe` only. No tool installation was needed or performed.

## 1. Question and bound

Inside an ANSI-C string, does the lane `code_view` agree with bash about a single quote preceded by
**one** backslash (`\'`, escaped → string stays open) versus **two** (`\\'`, backslash pair consumed →
quote closes), and therefore about whether the following `#` starts a blanked comment and whether a
`#` inside the string stays literal? Declared bound unchanged: no nested substitutions, no unquoted
backslash-newline (docstring `tools/tally-audit-v3.py:160-161`).

## 2. Ground truth (lexical witnesses)

`bash --noprofile --norc -n` on a lone assignment; `rc=2` is bash's "unexpected EOF while looking for
matching `''" — i.e. the string is still open at EOF.

| witness | bash -n |
|---|---|
| `x=$'a\'` | rc=2 (open) |
| `x=$'a\\'` | rc=0 (closed) |
| `x=$'a\\\'` | rc=2 (open) |
| `x=$'a\\\\'` | rc=0 (closed) |

Odd backslash runs escape the quote, even runs leave it closing. Execution witnesses on the same
shapes (byte-exact files, `od -c` verified: one vs two backslashes at offset 0x20):

```
=== fx_1bs_comment.sh   ... $ ' i t \ ' s '   #   I N E R T
bash -n rc=0 ; bash run:  <it's>            rc=0
=== fx_2bs_comment.sh   ... $ ' a \ \ '       #   I N E R T
bash -n rc=0 ; bash run:  <a\>              rc=0
=== fx_1bs_hash.sh      ... $ ' i t \ ' s     #   K E E P '
bash -n rc=0 ; bash run:  <it's # KEEP>     rc=0
=== fx_2bs_hash.sh      ... $ ' a \ \         #   K E E P '
bash -n rc=0 ; bash run:  <a\ # KEEP>       rc=0
```

So in bash: `\'` keeps `#` inside the string (literal, not a comment); `\\'` closes the string and a
following blank-separated `#` is a comment. A raw newline inside `$'…'` is preserved (`<a'⏎b>`), which
the same-length view also preserves.

## 3. Pair table — bash vs the pinned scanner

`code_view` loaded by `exec` from the pinned bytes; "expected view" blanks `#`→newline only where bash's
lexer makes it a comment.

| fixture | bytes before `'` | bash world | bash stdout | pinned `code_view` |
|---|---|---|---|---|
| `frozen_1` (`: $'it\'s' # inert st_tsu=0`) | 1 bs | comment | (no output) | blanked, match |
| `frozen_1_analogue_2bs` (`: $'it\\' # inert st_tsu=0`) | 2 bs | comment | (no output) | blanked, match |
| `F1` (`printf … $'it\'s' # INERT`) | 1 bs | comment | `<it's>` + `TAIL` | blanked, match |
| `F2` (`printf … $'a\\' # INERT`) | 2 bs | comment | `<a\>` + `TAIL` | blanked, match |
| `F3` (`… $'it\'s # KEEP'`) | 1 bs | literal | `<it's # KEEP>` | unmodified, match |
| `F4` (`… $'a\\ # KEEP'`) | 2 bs | literal | `<a\ # KEEP>` | unmodified, match |
| `F5` (`… $'a\\\'b' # INERT`) | 3 bs | comment | `<a\'b>` | blanked, match |
| `F6` (`… $'a\\\\' # INERT`) | 4 bs | comment | `<a\\>` | blanked, match |
| `F7` (`… $'a\\'#INERT`, no space) | 2 bs | literal (word) | `<a\#INERT>` | unmodified, match |
| `F8` (`… $'a\'#'`) | 1 bs | literal (word) | `<a'#>` | unmodified, match |
| `F9` (`… $'a\'` ⏎ `b' # INERT`) | 1 bs, multi-line | comment | `<a'` ⏎ `b>` | blanked, match |
| `F10` (`… $'a\\'` ⏎ `# INERT`) | 2 bs, next line | comment | `<a\>` | blanked, match |
| `frozen_2` (`: $'literal # data'`) | 0 bs | literal | (no output) | unmodified, match |
| `frozen_2_analogue_2bs` (`: $'literal # data\\'`) | 2 bs | literal | (no output) | unmodified, match |

**Pinned tool: 14/14 match, 0 divergences inside the bound**, and every view is same-length with
newlines preserved. Command: `python3 probe.py pristine_pin.py` → `SUMMARY tool=pristine_pin.py
divergences=0 bash_ground_truth_failures=0 fixtures=14`, exit 0.

The pre-fix revision `d9c496b` (sha `6188db16…`, no `ansi-c` state at all — `grep -c ansi-c` = 0, so
every `'` closes) diverges on **5/14, all odd parity**, and agrees on every even-parity fixture:

```
frozen_1_escaped_quote_trailing_comment  scan=DIVERGES   (comment leaks)
F1_odd_1bs_quote_comment                 scan=DIVERGES
F3_odd_1bs_literal_hash                  scan=DIVERGES   (blanks real string text: got
                                                          "…$'it\'s        \nprintf…")
F5_odd_3bs_quote_comment                 scan=DIVERGES
F9_odd_1bs_multiline_comment             scan=DIVERGES
SUMMARY tool=before_d9c496b.py divergences=5 … exit=1
```

The old defect is parity-*blind* closing, which is accidentally correct at even parity — so an
even-parity fixture alone would not have caught it either. The pair (odd + even) is what pins behaviour.

## 4. Mutation: parity-blind lookbehind (smallest behaviour-bearing change)

Replaced the ansi-c pair-skip with single-character lookbehind — the plausible misreading "a quote is
escaped iff the immediately preceding byte is a backslash" (`tools/tally-audit-v3.py:172-179` in
pristine form):

```diff
         if quote == "ansi-c":
-            if c == '\\' and i + 1 < n:
-                i += 2
-                continue
-            if c == "'":
+            if c == "'" and (i == 0 or text[i - 1] != '\\'):
                 quote = None
             i += 1
             continue
```

Mutant bytes: sha256 `1e6e7c98b79201809db6272f88a61dde4514653d4b6aa5f51d2ec83e3bef7be8`
(retired copy kept at `/tmp/r37-ansi-probe/mutant_lookbehind.py.frozen`).

**Frozen detector, run verbatim in a scratch git lane with the mutant committed** — SURVIVED:

```
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 tool_sha256=1e6e7c98… C2_R37_PASS=true
```

**Extended probe — KILLED on 4/14, every one even parity** (pristine baseline on the same fixtures
was 0/14, so the kill is attributable to the mutation):

```
frozen_1_analogue_2bs      want ": $'it\\\\'                 \nst_tsu=9\n"
                           got  ": $'it\\\\' # inert st_tsu=0\nst_tsu=9\n"
F2_even_2bs_quote_comment  want "printf … $'a\\\\'        \nprintf 'TAIL\\n'\n"
                           got  "printf … $'a\\\\' # INERT\nprintf 'TAIL\\n'\n"
F6_even_4bs_quote_comment  (same leak with `$'a\\\\\\\\'`)
F10_even_2bs_nextline_comment (next-line `# INERT` never blanked; it also swallows `printf 'TAIL'`)
```

Behavioural consequence, measured with the tool's own twice-only head rule
(`tools/tally-audit-v3.py:529-537`, `head_code.count(nm)` at :535): a head with the correct two
`st_tsu` occurrences plus one trailing comment mention counts **2** under the pinned tool and **3**
under the mutant (`# inert st_tsu=0` counted as a second write) → `check_head` false-fails, the same
false-kill class as the r36 leak but mirrored to even parity. Pre-fix revision shows the same count 3
on the one-backslash fixture. So a parity-blind defect in either direction is verdict-bearing.

**Verdict on the mutant: survived the frozen predicate, killed by the extended probe.** This is a
coverage finding only: the frozen two-case predicate attests odd-parity escaping plus literal-hash
preservation and does not discriminate even-parity handling, but the committed tool *is* parity-correct
(§3 and inspection of :172-179). C2 at the pin therefore still re-attests `C2_R37_PASS=true`
(`measure.py --lane <lane> --rev ae9b771…` → `tool_sha256=da8c1ef4… C2_R37_PASS=true`). No contract
change is claimed or implied.

## 5. Out-of-bound observation (not counted in any verdict)

The comment-start set at `tools/tally-audit-v3.py:199` is `' \t\n;|&('` — it omits `)`, `<`, `>`. Bash
starts a comment after a redirection operator, so a line that closes an ANSI-C string and then
redirects trips the view:

```
redir2.sh bytes: : $'a\\' >#INERT
bash -n:  redir2.sh: line 1: syntax error near unexpected token `newline'   (rc=2)
```

bash consumed `#INERT` as a comment (leaving `>` without a target); the view leaves `#INERT` as code.
Same bytes at both `d9c496b` and `ae9b771` — this is the word-start delimiter set, **independent of
ANSI-C escape handling**, outside this seat's bound, and deliberately not repaired here.

## 6. Restoration evidence

```
1e6e7c98…  mutant_lookbehind.py.frozen   (observed defect, retired)
da8c1ef4…  mutant_lookbehind.py          (restored: copied from pristine_pin.py)
da8c1ef4…  pristine_pin.py               (pin bytes)
cmp mutant_lookbehind.py pristine_pin.py → IDENTICAL
python3 probe.py mutant_lookbehind.py     → divergences=0 … exit=0   (post-restore)
measure.py (restored scratch lane)        → tool_sha256=da8c1ef4… C2_R37_PASS=true
```

Lane untouched: `git diff` empty, HEAD `e6185d5…`; `git status` lists only sibling untracked
`.ufo/waves/round-37/w1/*.md` reports. The only lane write from this seat is this file.

## 7. Limits

- 5+ backslash runs are not executed; parity is classified by the same pair rule, but unprobed.
- ANSI-C octal/hex/unicode escapes consume digits, never `'`, so they cannot move close-parity; not
  probed, no divergence implied.
- Nested `$()` and unquoted backslash-newline remain the declared holds (docstring :160-161); the
  probe does not reach them.
- The naive even-parity analogue `: $'it\\'s' # inert …` is **not** valid: bash closes at the quote
  after `\\`, so `s'` opens a fresh single-quoted string and `bash -n` returns rc=2. The analogue used
  above (`$'it\\' # inert …`) keeps the shape valid for both parities; this trap is why the parity
  fixture has to be written deliberately.
