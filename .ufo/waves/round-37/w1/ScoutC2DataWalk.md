# Round-37 w1 — ScoutC2DataWalk (C2 syntax boundary)

Seat: `L1-tameshi-r37-attempt2.ScoutC2DataWalk` (leaf scout, godspeed). Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` read-only; nothing written outside this report.
No installs; `pacman` untouched. Lane tip `e6185d5` ; tool tip `ae9b771`,
`tools/tally-audit-v3.py` sha256 `da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`.

Slice: walk `code_view`, its selftest, and the r35 `AttackQuotedHash` note; separate the named
ANSI-C quote defect (closed by r37) from the still-open nested-substitution and line-continuation
cases (declared holds).

---

## 1. The state machine at HEAD — `tools/tally-audit-v3.py:152-208`

One `while` loop, one global `quote` register with **four** states after `ae9b771`
(`None`, `'`, `ansi-c`, `"`):

| branch | lines | semantics |
|---|---|---|
| `quote == "'"` | 167–171 | plain single quote; `\` NOT special; closes on `'` |
| `quote == "ansi-c"` | 172–179 | **new**: `\` skips 2 chars (`:173-175`), closes on `'` (`:176-177`) |
| `quote == '"'` | 180–187 | `\` skips 2, closes on `"` |
| top-level `\` | 188–190 | skip 2 chars; **leaves `\n` as previous char** |
| `$'` opener | 191–194 | **new**: `text[i+1] == "'"` → `quote="ansi-c"`, `i += 2` |
| `'`/`"` openers | 195–198 | enter plain quote states |
| `#` word-start | 199–206 | blank to EOL iff `i==0` or `text[i-1] in ' \t\n;|&('` (set unchanged) |

Docstring at `:160-161` is now explicit: *"This is bounded support, not a full Bash lexer:
nested command substitutions and unquoted backslash-newline continuations remain outside this
view."* Quote register still persists across newlines (no per-line reset).

## 2. Selftest — `tally-audit-v3.py:889-903`

Two `code_view` unit cases precede the 33 runner cases:

- `:889-893` fixture 1 `": $'it\\'s' # inert st_tsu=0\nst_tsu=9\n"` → expects `#`-to-EOL blanked;
- `:894` fixture 2 `": $'literal # data'\nst_tsu=9\n"` → expects byte-identical output.

Receipt `.ufo/evidence/round-37/tool-selftest-after.stdout`: `CASE code_view ANSI-C escaped
quote trailing comment PASS`, `CASE code_view ANSI-C literal hash PASS`,
`TALLY_AUDIT_V3_SELFTEST: 35/35 pass`. The same two fixtures are the frozen C2 predicate
(`.ufo/evidence/round-37/code-view/measure.py:48-54`) — verbatim identical bytes.

## 3. Named defect vs open holds — r35 specimens re-probed at HEAD

r35 `AttackQuotedHash` (`.ufo/waves/round-35/w2/AttackQuotedHash.md`) filed four mis-lexed
constructs: `$'…'` escape (A, over-blank) + `$'it\'s'` quote-leak (K2, under-blank), nested
`$( )` quotes (B), `\`+newline (C), `${X:-$'…'}` (D, fail-closed). Probe of HEAD `code_view`
(exec'd from committed bytes, `PYTHONDONTWRITEBYTECODE=1`):

```
A_ansiC        view="  : $'don\\'t reorder the legs # '; st_tsu=0\n"   ← # kept, mask VISIBLE
B_nesteddq     view='  : "note $(printf %s "n                  \n'     ← still blanked (HOLD)
C_linecont     view="  printf '%s' foo\\\n                         \n" ← still blanked (HOLD)
D_parambranch  view="  : ${X:-$'a\\'b # '}; st_tsu=0\n"               ← # kept, braces balance
K2_quoteleak   view="  : $'it\\'s'                                      \n" ← comment blanked
FIXTURE1/2     blanked / byte-identical                                ← frozen predicate
```

**Closed (the named ANSI-C quote defect):** both directions of the `$'…'` mis-lex —
A (literal `#` inside `$'…\'…'` was blanked, hiding `st_tsu=0` → false accept) and K2 (early
close re-opened a phantom quote, leaking a real comment → false kill). Receipts:
`code-view/before.stdout` `ansi_trailing_comment=0/1 … C2_R37_PASS=false` at `d9c496b`;
`code-view/after.stdout` `2/2 … C2_R37_PASS=true` at `ae9b771`. D's *specific input* also now
lexes correctly (the `#` stays inside the ANSI-C string, braces balance, `st_tsu=0` visible) —
its r35 fail-closed `unbalanced braces` exit-2 path is no longer triggered by this shape.

**Open (unchanged at HEAD, declared holds):**
- **B — nested `$( )` quoting.** No `$(` tracking; `"n` inside `$(…)` still closes the outer
  `"` state and `# ` blanks to EOL. `st_tsu=0` remains hidden in the view — the r35 false-accept
  shape survives the fix (as designed; outside the frozen predicate).
- **C — unquoted `\`+newline.** Branch `:188-190` skips both chars but leaves `\n` as
  `text[i-1]`, so `#` still reads as word-start; `#bar >/dev/null; st_tsu=0` still blanked.
- **Parameter-branch quoting (broader class).** `${…}` state is not modelled; only its ANSI-C
  interior (D) improved. Unquoted `${x: #lit}` still blanks `#lit}` including `}` →
  `unbalanced braces` fail-closed (r35 `AttackArithHash` CRITICAL-3 class, `.ufo/waves/round-35/w2/AttackArithHash.md:150-166`).
- Holds are *declared*, not silently promoted: docstring `:160-161` and
  `LOG.md:1979-1981` ("nested `$(…)`, unquoted backslash-newline, parameter-branch quoting
  stay unsupported").

## 4. Secondary observations

- **Counter copy NOT mirrored.** Frozen r36 counter `.ufo/evidence/round-36/c1/c1-measure-v2.py:128`
  still carries the pre-`ae9b771` lexer (no `ansi-c` state; grep `ansi` → 0 hits) — r35
  HYGIENE-2 (AttackQuotedHash `:228-230`, AttackNameAssembly `:216,281-282`) persists: tool and
  counter disagree on `$'…'` bytes. Benign today (counter ground truth is behavioural +
  committed panel carries no `$'…'`); re-attested `C2_R37_REPIN_PASS=true`
  (`.ufo/evidence/round-37/c2-repin-after.stdout`, frozen counter sha `9eb8944c…` in
  `counter-pin.json`).
- **Word-start set unchanged** (` \t\n;|&(`); r35 §7's bounds (`)`,`>`,`<`,`=` positions) are
  untouched by `ae9b771` — the diff adds states, no delimiter changes.
- **Edge parity check (inference, probed):** `\$'…'`, `$'a\\'` escaped-backslash, and `$'…\'…\'…'`
  chains lex identically to bash; an unterminated `$'…'` swallows following comments fail-closed,
  same as an unterminated plain `'…'` did before the fix.
- **Selftest blind spot partially closed:** r35 §6 HYGIENE noted no `$'…'` seed; r37 added the
  two unit fixtures but still no *runner-level* seed for B/C/D shapes — consistent with their
  hold status.

## 5. Confidence and remaining unknowns

- Confident (observed): fixture and specimen `code_view` outputs above; both receipts; the diff
  of `ae9b771`; counter-copy divergence; hold declarations in docstring + LOG.
- Inference: bash-side truth for B/C/D is taken from r35's verbatim transcript
  (`AttackQuotedHash.md:357-365`), not re-executed against the full tool CLI at HEAD (probe was
  `code_view`-level only — sufficient for the syntax boundary, but a full `--runner` verdict on
  rebuilt B/C specimens is untested this round).
- Unknown: whether any *committed* panel specimen contains `$'…'` (none observed; repin PASS is
  consistent). If one is ever added, the tool/counter lexer skew of §4 becomes verdict-bearing.
