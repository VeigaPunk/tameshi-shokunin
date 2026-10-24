# CriticC2Predicate — r37 C2 predicate attack (depth)

Seat: `L1-tameshi-r37-attempt2.CriticC2Predicate` (leaf; no dispatch).
Lane base observed: `e6185d5` (detached), tool `tools/tally-audit-v3.py` sha256 `da8c1ef4…93ede` == counter-pin.
Scope: discriminating power of the frozen two-case predicate, accidental-pass risk of the
literal-hash control, wording vs. supported quoting surface.

## Verdict

Predicate is discriminating for the named defect (old FAIL/new PASS replayed, digests match
frozen pins), but the implemented `$'…'` entry test is context-free and leaks two
under-blank classes in *valid* bash — `$$'…'` and a comment after operator `)`. The frozen
pair also admits a differently-wrong implementation (double-quote mode bound to `$'`). None
of these void the frozen claim — the predicate is honestly scoped to the two fixtures — but
each is unheld surface the wording "Bash ANSI-C `$'...'` strings are scanned as
single-quoted strings" does not cover.

## 1. Fixture discriminating — VERIFIED (replayed, not trusted)

```
python3 .ufo/evidence/round-37/code-view/measure.py --lane . --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d
→ CASE ansi-c-escaped-quote-trailing-comment FAIL
    expected=": $'it\\'s'                 \nst_tsu=9\n"
    actual=": $'it\\'s' # inert st_tsu=0\nst_tsu=9\n"
  CASE ansi-c-literal-hash PASS
  C2_R37: … tool_sha256=6188db16…d354 rev=d9c496b… C2_R37_PASS=false   (exit 1)

python3 .ufo/evidence/round-37/code-view/measure.py --lane . --rev ae9b771ab795fb5b4a6302165d8abdc0a2c6b229
→ both PASS, tool_sha256=da8c1ef4…93ede (== counter-pin.json) C2_R37_PASS=true   (exit 0)
```

Old tool mechanism: at `d9c496b` `'…'` has no escapes, so `$'it\'` closes at `\'`,
`s'` opens an unterminated plain quote, and `# inert st_tsu=0` is swallowed — comment leaks
into structural view. Exactly the frozen "before". MutateAnsiBranch confirms
necessity/sufficiency of the new branch; selftest receipt shows the two cases counted in
`35/35` (measure `selftest` line: `total = len(cases) + len(code_view_cases)`).

## 2. Literal-hash control — can pass accidentally, as designed-scoped

`$'literal # data'` contains no escape, so *any* quote-aware blanker passes it — including
the r36 tool with zero ANSI-C handling (observed PASS at `d9c496b` above). Its only
discriminating content is that a `#`-after-space blanker *without* quote state fails it.
It is an over-blanking control (MutateAnsiLiteralHash), not an ANSI-C detector: all
escape-semantics coverage rides on fixture 1 alone. Wording is accurate ("byte-identical"),
but the fixture must not be cited as evidence the tool "handles `$'…'`" — it cannot
distinguish ANSI-C from plain single-quote handling.

## 3. Counterexample F1 — `$'` entry is context-free; `$$'…'` under-blanks (valid bash)

`code_view` (`tally-audit-v3.py:191`) fires on the two bytes `$'` with no left-context
check. In bash, `$$` is the PID expansion and the following `'…'` is a *plain* single-quoted
string — not ANSI-C. Verified live:

```
bash -c "echo \$\$'a\\' # c'"   →  3600021a\            (comment honored, rc=0)
code_view(": $$'a\\' # c'\n")   →  ": $$'a\\' # c'\n"   (comment left live — under-blank)
```

Bash: `$$` + `'a\'` (plain quote ends at `'`) → ` # c'` is a comment. Tool: enters ansi-c
state at `$$'`, `\\'` consumed as escape, quote never closes → comment text survives into
the code view — the same defect class the r35 comment-blinding fixed, on input that is
*valid* bash (compare `bash t.sh` with `$$'it\'s'` → syntax error only because the plain
quote is unterminated *there*; with `$$'a\'` it is well-formed).

Smallest safe correction: suppress the ansi-c entry when `text[i-1] == '$'` (or more
precisely when the `$` is the second of a `$$` pair); one-character guard, then re-pin.

## 4. Counterexample F2 — `)` missing from comment-boundary set (valid bash)

`tally-audit-v3.py:199` delimiters: `' \t\n;|&('`. Bash treats `#` after a *word-closing
operator* `)` as a comment start:

```
bash -c '(true)#c'                 →  rc=0, no error   (#c is a comment)
bash -c 'arr=(a b)#c\necho done'   →  done              (#c is a comment)
code_view("(echo ok)#c\n")          →  "#c" left live   (under-blank)
```

So `(cmd)# } esac done` leaves forged structural tokens in the code view. The docstring's
own enumeration "after whitespace or one of `;|&(`" is thereby *wrong about the surface it
does claim* — not an overclaim, a mis-claim: `(` is listed, `)` is not. Note the asymmetry
is bash-real: `)` closing `$()` is inside the word (`echo $(x)#c` → `ok#c`, tool agrees
accidentally), but `)` closing `(…)`/array/case is an operator and bounds a comment.
`>`/`<` are also real boundaries (`echo x>#c` → dangling-redirect syntax error proves `#c`
was consumed as comment) but reachable only in invalid bash — flag, lower priority.

Smallest safe correction: add `)` (and optionally `><`) to the delimiter string and fix the
docstring enumeration to match.

## 5. Residual blind-spot — the frozen pair does not pin the mode identity

An implementation that binds `quote='"'` instead of the ansi-c branch on `$'` passes BOTH
fixtures: in `"` mode `\'` is skipped (fixture 1) and `#`/`'` are literal (fixture 2), yet
it is wrong for bash. Discriminator for w2: `$'it\'s "x"' # c` — true ANSI-C blanks the
comment; a `"`-mode impostor never closes the quote and leaks it. Fixable later; the frozen
contract does not promise more than the two fixtures, so this is a coverage note, not a
contract breach.

## No wording overclaim found in the named surfaces

- `contract.json:20-27` — "bounded", fixture-scoped "iff" — accurate.
- `code_view` docstring `:153-161` — explicit bound ("not a full Bash lexer", nested
  substitutions + unquoted continuations held). Accurate; but see F1/F2: the stated
  `$'…'` claim is itself over-broad by one missing left-context check, and the delimiter
  enumeration is incomplete (`)` — and `><` in invalid-input space — are bash boundaries).
- SCORECARD `:1803, :1809`, SOURCES S104 row (`corpus/SOURCES.md:113`) — all scoped
  ("nested substitutions and unquoted backslash-newline remain unsupported").
- `counter-pin.json` `control_mode` — transparent about bypassing the counter's
  historical tool digest while enforcing the new pin independently; no overstatement.
- Inherited r35 docstring overclaim (`:27-28`) already reported by CriticBoundedParser —
  not duplicated here.

## Impacted axes

- depth: F1 and F2 are unheld, valid-bash divergences inside the claimed `$'…'`/comment
  surface — fixable defects (one-char left-context guard; delimiter-set extension), not
  judge-blocking tradeoffs, since the frozen predicate is honestly two-fixture-scoped.
- Predicate soundness: before/after replay + digests + pin chain all clean; F3 is a
  coverage note for the falsification wave.

No installs performed; `python3`, `git`, `bash` only. No lane files edited other than this
report.
