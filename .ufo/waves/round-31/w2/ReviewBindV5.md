# ReviewBindV5 — review of binding v5 (cold-read bound) and its control receipts

Seat `ReviewBindV5`, round-31 wave 2. Read-only review; no files outside this report and the seat
scratch `/fast/scratch/hyaku/tameshi-r31-seats/ReviewBindV5` were written. No tools installed
(tooling directive: nothing needed; system `python3` used).

Scope: `…/.ufo/evidence/round-31/coldread/bind-select-v5.py` (sha256
`8760ddc9014af73a20dc95627528b845af75c9539c780fa509fba2c9b2e61338` — recomputed, matches
`ctl/README-bind-v5.txt` line 7), diff vs `bind-select-v4.py`, control receipts under
`…/.ufo/evidence/round-31/ctl/` (README-bind-v5.txt, bind-v5-*.stdout, harness probes), pilot
`…/coldread/pilot/v5-on-r30-real-receipt.json` (assembled 63 / kept 63 / excluded 0).

Verdict first: **v5 is a strict improvement over v4 on the observed shapes — all nine new-shape
controls and all seven old shapes are killed — but two forged-shape families survive under trivial
syntactic variants (double heredoc; function definition with `f ()` spacing), and the command reader
is roughly-parse only, so several genuine launch shapes (backslash continuations, `if` blocks,
`false || trace`, variable `--out`, `sudo`/`bash -c`) are rejected.** Findings below by severity.

## How it was verified
- Parser behavior exercised directly in the seat scratch by importing the frozen v5 module and
  feeding `traced_commands` / `assistant_has` 60+ crafted command strings (test scripts
  `t1..t4_traced.py`, `t3_assistant.py` in scratch). Every claim below shows the exact command and
  observed output.
- End-to-end binding of the wave recipe ran in scratch: `cd $R && python3 tools/trace-inputs.py
  --root $R --out traces/ColdA03-x.json -- --rev abc` with a synthetic registry/report/receipt/
  transcript binds 1/1 (exit 0).
- Real-bash ground truth for heredoc semantics run with the system bash (scripts `hd1..hd3.sh`,
  `bashcheck.sh` in scratch).
- Control receipts read; harness copies under `ctl/harness/` were not re-run (they need the seats'
  scratch fixtures; the frozen stdout files are the record).
- `diff -u` v4→v5 confirms the code change set matches the v5 docstring bullets one-for-one.

## False-accept findings (v5 credits a command that does not execute)

**FA-1 (HIGH) — double here-document on one line: only the first opener is tracked; the second
heredoc's body is parsed as commands.** `_drop_heredoc_bodies` (bind-select-v5.py:95-106) stores a
single `delim` from the first `HEREDOC_RE` match on a line (line 103) and drops lines only up to
that delimiter. For `cat <<A <<B`, lines between A's delimiter line and B's delimiter line are real
heredoc data but remain visible to the lexer. Verified: `cat <<A <<B\nA-body\nA\npython3
tools/trace-inputs.py --root $R --out traces/ColdA03-x.json -- --rev abc\nB` →
`[('ColdA03-x.json', ['--rev', 'abc'])]`; real bash (`hd3.sh`) feeds that line to `cat` as stdin
data — it never executes. This re-opens the exact control shape `literal_heredoc` (killed only in
its single-heredoc form) in a variant an attacker controls.

**FA-2 (HIGH) — shell function defined with `f () {` (space before parens) is not detected; body
credits.** The check at bind-select-v5.py:129 matches token `function` or `FUNC_TOKEN_RE`
(`^[A-Za-z_][\w.-]*\(\)$`, line 91), i.e. only the no-space form. Bash's classic POSIX form
`f () {` (verified valid: `bash -c 'f () { echo in-f; }; f'` prints `in-f`) produces tokens
`f`, `()`, `{` — no match. Verified: `f () {\npython3 tools/trace-inputs.py --root $R --out
traces/ColdA03-x.json -- --rev abc\n}` → `[('ColdA03-x.json', ['--rev', 'abc'])]`. The control
shape `uncalled_function` used `r31_never_called() {` and was killed; this variant survives.

**FA-3 (LOW) — a call with two later toolResults, first non-error and second error, is still
credited.** assistant_has (bind-select-v5.py:314-317) checks only `later[0][1]`
(not `isError`) once `len(later) == len(res)`; verified `fx_twoafter` fixture → traced kept.

## False-reject findings (v5 rejects a command that genuinely runs)

**FR-1 (MEDIUM-HIGH) — backslash-newline continuations split the command, so a wrapped trace call
is never found.** The lexer (bind-select-v5.py:122) runs on the raw text; a real `\`+newline is
not treated as continuation (newline is a separator). Verified:
`cd $R && python3 tools/trace-inputs.py \` + real newline + `    --root $R --out … -- --rev abc`
→ `[]`. (A literal `\n` pair, not a real newline, passes — only the real continuation fails.)

**FR-2 (MEDIUM-HIGH) — a single `function` keyword or `name()` token anywhere in the whole bash
call kills every trace in it, including sibling commands that do run.** The early return at
bind-select-v5.py:129 applies to the whole raw token list. Verified: `f() { echo hi; }\n<trace>` →
`[]` (function + genuine sibling trace in one call); `echo function; <trace>` → `[]`; and a
legitimate argv token `a()` (`… --out x.json -- a() b`) kills its own call → `[]`. Over-broad for
the docstring claim "a command that *defines* a shell function … credits nothing".

**FR-3 (MEDIUM) — trace commands inside `if`/`then` (and `{ … }` group) are invisible.**
`_program` (bind-select-v5.py:168-203) breaks on unknown head words: `if [ -f x ]; then <trace>;
fi` → `[]`; `{ cd $R && <trace>; }` → `[]`. Not documented; plausible if a reader guards the trace.

**FR-4 (MEDIUM) — a trace after `||` is always blocked, including unconditional idioms where it
does run.** bind-select-v5.py:158-159 sets `blocked` for any `||`; `false || <trace>` and
`! true || <trace>` → `[]`, although both always execute the right-hand side (`false` fails).
`<trace> || echo failed` and `cd $R && <trace> || echo failed` are fine (trace is on the left).
The docstring calls post-`||` traces "unreachable", which is an overstatement for these idioms.

**FR-5 (MEDIUM) — variable `--out` values can never bind.** `--out "$O"` yields out basename
`$O` (unexpanded), which cannot equal a real receipt filename → the entry is rejected despite a
genuine run (verified → `[('$O', …)]`). `$TRACE_DIR/foo.json` works (basename `foo.json`). Only
`$(`, backtick, `)` values are filtered by design (line 239); `$VAR` indirection is an additional
invisible shape.

**FR-6 (LOW-MEDIUM) — a comment mentioning heredoc syntax swallows the rest of the command.**
`HEREDOC_RE` searches every line including comments (line 103): `# example: cat <<EOF` + newline +
`<trace>` → `[]` (verified). A reader who writes an explanatory `<<EOF` comment in the same bash
call as the trace loses the trace.

**FR-7 (LOW) — `timeout 5 -s KILL <trace>` (GNU allows options after the duration) is rejected;**
`_program` consumes options only before the duration (lines 183-188), then the trailing `-s` breaks
the outer loop → `[]` (verified). `timeout -s KILL 5 <trace>` works.

**FR-8 (LOW) — `nice -n 5 python3 …` is rejected while bare `nice` works:** the `-n` value is not
skipped (line 177-180 skips only `-u`/`--unset` values) → `[]` (verified).

**FR-9 (LOW) — launch paths outside the wrapper list: `sudo <trace>`, `bash -c '<trace>'` → `[]`**
(verified). This matches the README's "not covered" list (README-bind-v5.txt lines 17-18).

**FR-10 (LOW) — heredoc delimiter with trailing whitespace (`EOF   `) is not honored** (exact
equality, line 99), so any genuine trace after such a terminator is dropped. (Bash's own delimiter
matching is whitespace-tolerant; not re-verified here.)

**FR-11 (LOW) — `--out` paths containing `)` (e.g. `/tmp/(x)/…`) are filtered by design** (line
239); legitimate parenthesized directories reject. Documented rule; listed for calibration.

## Docstring / code consistency
All ten v5 bullets in the docstring match the implemented code (verified one-by-one above): quote
keeping + unquoting, single-heredoc removal, `name() {`/`function name` definition kill, `-c`/
`-m` no-script (with `-W`/`-X` option-arg skipping), `||` block and `&&`-after-never-succeeds,
`command -v/-V`, `timeout` without duration, `--out` substitution filtering, and result-before-call
rejection (verified via `fx_before` fixture: `[]`, while v4 credited). The two gaps (FA-1, FA-2)
are variants the docstring does not cover, not doc/code mismatches. README sha256 claim verified by
recomputation.

## Residual risk and verification gaps
- A hand-forged call+result pair stays beyond any transcript binding (README-bind-v5.txt lines
  19-20); FA-1 and FA-2 are the two *syntactic* bypasses found that would let such a pair be
  formatted in a shape v5 parses as executed. Both are cheap for an adversary to exploit and are
  the top items to close in a next binding revision.
- General reachability/execution is not decidable from text — acknowledged by v4 (line 14) and the
  controls cannot falsify a fake but *executed-looking* call.
- I did not re-run the ctl harnesses (they need the seats' scratch fixtures); I verified the same
  claims at the parser level and end-to-end on the wave recipe. The frozen control stdout files are
  consistent with the docstring and with my parser-level results for their shapes.
- Wave-recipe exposure: the canonical `cd $R && python3 tools/trace-inputs.py --root $R --out
  <path> -- <argv>` binds cleanly (e2e kept 1/1). The false-reject list above matters only where a
  reader diverges from that recipe (wrapped lines, guards, variables, launchers); none of the
  failing shapes is part of the recipe itself.
