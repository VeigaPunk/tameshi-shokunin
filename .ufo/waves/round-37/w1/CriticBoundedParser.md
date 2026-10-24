# CriticBoundedParser — r37 scope-overclaim sweep (depth)

Axes checked: depth (claim honesty of the code_view surface), calibration (does prose exceed evidence).

Verdict: **one overstating sentence found** — inherited r35-era wording in the module docstring, not in any r37-authored artifact. Every r37 addition (frozen contract, `code_view` docstring, SCORECARD r37 rows, LOG r37 entry, lesson, wave specs, QUALITY 73–75, SOURCES S104) carries an explicit bound.

## The overstating sentence, verbatim

`tools/tally-audit-v3.py:27-28` (module docstring, unchanged since round 35; measured rev `ae9b771ab795fb5b4a6302165d8abdc0a2c6b229`):

> "All structural scans now run on a quote-aware code view in which shell comment text is blanked (same length, newlines kept), so offsets and slices are unchanged."

The sentence is categorical: no "supported forms" qualifier, no enumeration — it reads as a universal comment-blanking guarantee, the exact shape of a lexer claim.

## Counterexample (executed at the pinned rev)

`git show ae9b771:tools/tally-audit-v3.py | exec` then `code_view(...)`:

1. **Under-blank — a real comment survives unblanked:**
   `': "$(x \'y"\') tail" # real comment\n'` → output byte-identical. Bash treats `'y"'` as single-quoted inside `$(...)`, so the trailing `# real comment` is a genuine comment; `code_view`'s flat quote register closes `"` at the literal `"` inside `'y"'`, desyncs, and swallows the comment into quote state. `bash -c` on the same text runs the comment as a comment (verified live).
2. **Over-blank — word continuation blanked as comment:**
   `'foo bar\\\n#baz\n'` → `foo bar\\\n    \n`. After an unquoted backslash-newline, bash continues the word (`#baz` is not a comment); `code_view` skips the `\`+newline pair, sees `#` at a "start of word" position, and blanks real code.
3. (`echo $(true)#abc` accidentally matches bash — `)` is not in the comment-start set, so `#abc` survives; luck, not modeling.)

## Why the bound elsewhere does not rescue the sentence

- `code_view`'s own docstring (`:153-161`) is correctly bounded: "only outside supported quote forms… This is bounded support, not a full Bash lexer." ✓
- Contract `contract.json:20-27` is bounded ("bounded Bash ANSI-C `$'...'` quote handling"; axis line names it a capability, not a lexer). ✓
- SCORECARD `:1803,:1809,:1817-1819` ("nested substitutions and unquoted backslash-newline remain unsupported"; "do not generalize the bounded ANSI-C capability to a full Bash lexer"), LOG `:1979-1981` (explicit holds), lesson `round-37.md:7,23`, w1/w2 spec contexts ("not a full shell lexer"), QUALITY 74, SOURCES S104 row — all bounded. ✓
- But a reader of the module docstring alone (the tool's own `__doc__`, printed by `--help`-adjacent surfaces) gets the universal claim. The r35 scorecard already conceded the non-universality (`SCORECARD.md:1722-1724`: "is not universal… no universal lexical claim is made or admitted") — yet the docstring sentence making that claim was never scoped, and QUALITY 74 ("a Bash `code_view` claim names each supported quoting form") now makes the omission a lane-criterion violation: the sentence names zero supported forms.

## Impacted axes

- depth: claim-surface wording exceeds the two measured fixtures; the C2 predicate itself is unaffected (both frozen fixtures still pass).
- calibration: minor — prose says more than the code does; mitigated but not cured by the bounded statements in the record.

## Smallest safe correction

Reword `tally-audit-v3.py:27-28` to the enumerated form, e.g. "All structural scans now run on a quote-aware code view in which shell comment text under the supported quote forms (single, double, ANSI-C `$'…'`) is blanked — see `code_view`'s docstring for the held-out classes." One-line change; no predicate, fixture, or receipt is touched. Fixable defect, not a judge-blocking tradeoff.

## Residual check — no other offender

- `code_view` docstring first line ("with shell comment text replaced by spaces") is immediately qualified by "outside supported quote forms" + the explicit not-a-lexer bound in the same paragraph — scoped, not overclaiming.
- No round-37 report file exists (`reports/` and `.ufo/reports/` hold nothing past round 1); the round record is LOG + lesson + SCORECARD, all bounded as cited.
- Module docstring also never mentions the r37 ANSI-C addition at all — stale by omission, but an omission is not an overclaim; the :27-28 sentence is the finding.

No installs performed; no tools required beyond `git`, `python3`, `bash` (all present).
