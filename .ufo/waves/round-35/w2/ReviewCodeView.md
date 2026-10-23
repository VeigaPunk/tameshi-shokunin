# Round-35 w2 — ReviewCodeView

Seat: `tameshi-r35-w2-ReviewCodeView` (leaf reviewer, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (clone-verified). Frozen bytes verified at pin:
tool `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`,
runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`,
counter `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`.

Slice: audit `code_view` (`tools/tally-audit-v3.py:150-194`) plus every scan that consumes it
(`regression_body`, `tally_block`, `head_section`, `counting_case`, `tally_loop`) against the
POSIX/bash lexical rules (S102 snapshot `.ufo/evidence/round-35/src/s102-posix-chap02.html`;
§2.2 quoting, §2.2.4 dollar-single-quotes, §2.3 token recognition rule 10, §2.7.4 here-documents).
Axes named: quote state transitions, backslash handling, heredocs, `$'...'`, command
substitution, `#` after an operator, CRLF. For each divergence I built a runner copy where it
matters and recorded (label → verdict). Ground truth for labels is **behavior**: the block bash
executes, driven by the counter's own `run_block` under all four (auto,KEEP) triples.

No installs (python3 + bash only; pacman untouched). Lane checkout read-only; all work under
`/fast/scratch/hyaku/tameshi-r35-seats/ReviewCodeView/` (mutants + audit receipts in `work/`).
A dead prior attempt of this seat left a stale `d16f9b5` checkout + partial mutants; all
evidence below was re-produced fresh at `7da6e076` with the `ef98fc53` tool bytes.

No LSP server answers these files (no `pylsp`, no `lsp` CLI on host); the reviewer LSP device
is unavailable here, recorded per protocol. Semantic checks were done by importing both frozen
files and executing their extraction/behavior functions — stronger than reference lookup.

## The one-line summary of the bug class

`code_view` models only three states (unquoted / `'` / `"`) plus one escape, and blanks `#`
only after `[ \t\n;|&(]` or at offset 0. It has **no `$'...'` state, no heredoc state, no
`\r` handling, no string-awareness in the brace scanner, and an incomplete comment-start set**.
Every divergence below is a case where `code_view`'s token stream ≠ bash's, and I show the
verdict consequence in a real copy.

## Verdict matrix (all at pin `7da6e076`, tool `ef98fc53`)

Command shape for every row: `python3 tools/tally-audit-v3.py --runner work/<name>.sh`
(executed as `python3 ../lane/tools/tally-audit-v3.py --runner <name>.sh` from `work/`).
Counter label = `behavior()`/`diverge()` of the frozen `c1-measure.py` on the copy's text.
Receipts: `work/audits/<name>.out`, `work/counter-labels.txt`, `work/k6-proof.txt`,
`work/j1-raw-proof.txt`; sha256s in `work/sha256s.txt`.

| copy (sha256 head) | bash truth | counter label | tool verdict | counter-valid? |
|---|---|---|---|---|
| pristine `a7d3f2dd` | identical | ACCEPT-valid | **PASS** rc=0 | yes |
| a1 `36bdc8bc` `( : )# esac` before block | identical | ACCEPT-valid | PASS rc=0 | yes (benign instance) |
| a2 `82c3bdde` `( : )# st_js` before block | identical | ACCEPT-valid | **FAIL head** rc=1 | no → CRITICAL-1 |
| a3 `cdbb7d1f` `v=$'\''` + `# st_js` | identical | ACCEPT-valid | **FAIL head** rc=1 | no → CRITICAL-1 |
| a4 `d507f60d` heredoc `st_js=$?` in head | identical | **KILL-valid (div=4)** | **FAIL all-4** rc=1 | kill, uncountable → CRITICAL-2 |
| a5 `2eb566a2` `x='}'` before block | identical | **SystemExit, run aborts** | SETUP rc=2 | aborts → BOUND-1 |
| a6 `85b8dca6` heredoc `esac` in unreachable arm | identical | ACCEPT-valid | **SETUP** rc=2 | no → CRITICAL-1 |
| a7 `182545a5` heredoc `}` before block | identical | **SystemExit, run aborts** | SETUP rc=2 | aborts → BOUND-1 |
| a8 `00900973` `x=$(echo ok)# st_js` | identical | ACCEPT-valid | **FAIL head** rc=1 | no → CRITICAL-1 |
| a9 `d2c504e7` heredoc `local nlegs=9` shadow | identical | ACCEPT-valid | PASS rc=0 | yes (mechanism demo for k6) |
| a10 `3439eb0d` `( : )# esac` inside arm 0 | identical | ACCEPT-valid | **SETUP** rc=2 | no → CRITICAL-1 |
| j1 `8c3afb83` whole file CRLF | unrunnable | **SystemExit, run aborts** | FAIL harness rc=1 | aborts → BOUND-1 |
| k1 `2b34b9d3` `st_js=$?\<nl># st_js=0` | **mask runs** | KILL-valid (div=4) | FAIL all-4 rc=1 | kill, uncountable → CRITICAL-2 |
| k2 `0aec4276` `cat <#f` (unrunnable) | parse error | ACCEPT-valid (div=0) | **PASS** rc=0 | pass — semantic hole → BOUND-2 |
| k6 `7310711e` heredoc shadows real block | **diverges** | ACCEPT-valid (div=0) | **PASS** rc=0 | pass — false-accept → CRITICAL-3 |

## CRITICAL-3 — heredoc extraction hijack: the audit blesses a decoy tally, bash runs the real one (the claim's guarantee is false)

`code_view` has no heredoc state. `tally_block` cuts `body[s.start() : last '}' ]` where
`s` is the FIRST line matching `^[ \t]*local nlegs=` **in the code view** — and a heredoc body
line `  local nlegs=9 …` is data to bash but code to the view.

Copy `k6-heredoc-shadow.sh` (sha256 `7310711eac1ef4352eb56bc03da109d615cca87bcb2b79a154b10fc999b1e716`):
inside `run_regression`, between `st_citecheck=$?` and the real tally, I inserted

```bash
  cat >/dev/null <<'EOT'
  <the pristine tally block verbatim, all 40 lines>
EOT
```

then mutated the REAL (executed) block's arm `1) nfail=$((nfail + 1)) ;;` →
`1) npass=$((npass + 1)) ;;`. `bash -n` parses it (rc 0); under the runner the `cat` consumes
the heredoc as inert data and the mutated tally runs.

**What the tool audited:** `tv3.tally_block(tv3.regression_body(k6_text))` returns a slice
that is byte-different from pristine (it trails into `EOT\n` + the mutated block) but
*behaviorally identical* — every path in the fake block exits before the dead tail. Proof:
`work/k6-proof.txt` — the counter's own `run_block` driven over the tool-extracted block vs
the block bash executes (the mutated slice, sha256 `f4474377…`) under all four configs:

```
vec=[1,0,…] tool-extracted=(1,'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)…')
            real-executed=(0,'REGRESSION: PASS (cases=9 passed=9 …)')   <-- DIVERGES
```

in **all four** (auto,KEEP) triples. The failing-leg-into-PASS flip is invisible to the
audit because it never runs the bytes bash runs.

**Verdicts:** tool `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`
rc=0 (`work/audits/k6-heredoc-shadow.out`). Counter `behavior()` (which shares the
identical `code_view` + `tally_block`, `c1-measure.py:90-143`) returns div=0 → the copy is
counter-certified `ACCEPT-valid` while the copy's executed behavior diverges from pristine.

**Why CRITICAL:** C1's guarantee is that the audit observes the copy's tally behavior. Here
the audited bytes are a heredoc-carried decoy; the audit is certifying the *decoy's*
behavior. This is RevengerRootShape's CRITICAL shape (shim vs real) one level deeper: not
the witness env but the *extracted object itself* is fakeable, and the counter's ground
truth shares the parser so the fraud is undetectable inside the apparatus — a labeled
specimen lands as `valid=True, pass=True` while the copy under test kills. It also
retro-degrades `a9-heredoc-nlegs` (PASS, extraction silently hijacked to a `local nlegs=9`
decoy — harmless only because the decoy happened to be behavior-equivalent).

## CRITICAL-2 — divergent copies the frozen kill rule cannot count

The predicate requires a kill specimen to fail **exactly `runtime`**. Two copies diverge
under the apparatus's own ground truth (counter `div=4`, both are KILL-valid) yet fail
non-runtime checks, so in the deciding run they land as kill *misses*:

- **a4 `heredoc st_js=$?` (d507f60d):** the counter's `code_view` treats the heredoc data
  line as a second `st_js` assignment → `names` has 10 entries → extracted behavior diverges
  on every vector (mismatch demo in `audits/a4-heredoc-leg-assign.out`: the oracle expects
  `cases=10`, the block counts 9). But to bash the line is inert data — the executed copy
  is **identical**. The counter calls it a kill and the tool kills it (head+static+runtime+
  harness all FAIL) — yet under the frozen rule (`failed == ['runtime']`) it does not count,
  and semantically it is an accept copy murdered by parser disagreement. Both readings lose.
- **k1 `st_js=$?\<newline># st_js=0` (2b34b9d3):** backslash-newline is removed *before*
  tokenization (S102 §2.1), so bash joins the lines → `#` is mid-word → the comment text
  executes: the live head fragment prints `pristine st_js=7 ; k1 st_js=0`
  (`/tmp/k1frag.sh` output, rc 0) — a real mask of a captured leg status; the counter's
  extracted behavior diverges under all four configs (KILL-valid). `code_view` correctly
  blanks the comment but leaves the `\` as a phantom trailing byte, so `ASSIGN_RE` no
  longer matches `st_js=$?\` → the copy fails at `head` (non-bare + missing assignment),
  not `runtime`. Killed, but not countable.

Either specimen in the sealed set produces `ho_kill < ho_kill_total` → `C1_R35_PASS=false`
while the divergence is real (k1) or fabricated by the counter itself (a4).

## CRITICAL-1 — the accept clause is falsified: behaviorally identical copies are failed/refused

Counter-certified `ACCEPT-valid` (div=0) copies that the tool FAILS or REFUSES — each one is
a `pass=False` under the frozen scoring (`not div and rc == 0`):

- **`#` after `)` unblanked** (cv start-set lacks `)`): `x=$(echo ok)# st_js` (a8) and
  `( : )# st_js` (a2) — bash comments (verified), visible to the view → `leg st_js appears
  3 times` → head FAIL rc=1. Inside the block, `( : )# esac` in arm 0 (a10) → `counting
  case` tail truncated → **SETUP rc=2** (`counting case $VAR in not found`).
- **`$'...'` quote desync** (S102 §2.2.4: `\'` does not terminate `$'…'`): `v=$'\''` opens a
  phantom `'` in the view → the next line's `# st_js` comment survives → head FAIL rc=1
  (a3). Verified: `code_view("v=$'\\''\n  # st_js\n")` keeps `# st_js`; a real `'x'` blank it.
- **heredoc data seized as code**: `esac` in an unreachable-arm heredoc (a6) → SETUP rc=2
  (the `esac` truncates `counting_case`'s 400-char tail — same refuse class as the
  round-34 `esac`-in-comment bug the fix claimed to close, now via heredoc instead of `#`).

## BOUND-1 — a lawful specimen can abort the entire deciding run

`tally_block` raises `SystemExit` (not `CannotAudit`) inside the counter's `behavior()` —
it propagates out of `score_copies`, killing the run mid-panel:

- **a5 `x='}'` in head / a7 heredoc `}` line** (`SystemExit: SETUP: tally start not found`,
  `work/counter-labels.txt`): `regression_body`'s brace counter is **string- and
  heredoc-blind** — `}` inside `'…'` or heredoc data closes `run_regression` early in the
  view, `local nlegs=` falls outside → abort. The tool's own verdict is SETUP rc=2 — but the
  counter never reaches a verdict because the run dies.
- **j1 whole-file CRLF** (8c3afb83): the counter's `apply_edits` output text keeps `\r\n`;
  `run_regression() {` no longer matches `\{[ \t]*\n` → `SystemExit: SETUP: run_regression
  not found` → run aborts (`work/j1-raw-proof.txt`). Asymmetrically, the tool reads its
  `--runner` file in text mode (universal newlines) so head/static/runtime pass the
  LF-normalized image and only `harness` fails on the raw bytes (`audits/j1-crlf.out`,
  rc=1) — the audited bytes are not the scored bytes (HYGIENE).

BOUND because these never mint a wrong PASS — they deny the measurement outright.

## BOUND-2 — apparatus-certifiable but semantically absurd

`cat <#f` inside `if false; then` (k2): `#` after `<` IS a comment in bash (verified), so
`<` loses its word → `bash -n` exits 2 and `bash k2 … --regression` exits 2 with a syntax
error — the copy cannot run at all. Counter `behavior()` extracts the surrounding block
(div=0, ACCEPT-valid) and the tool returns **TALLY_AUDIT: PASS rc=0**. The apparatus
certifies an unparseable file as behaviorally identical. Under the frozen literal rule it
is a `pass=True`; under any sane semantics it is a kill. Shared-parser blindspot.

## HYGIENE

- **H1 — phantom `\` residue:** `code_view` skips `\X` (2 chars) but leaves `\` visible, so
  `st_x=$?\<newline>` renders as non-bare. Direction: always fail-closed (never hides a
  comment that is code — comment text can't be code anyway unless joined by `\<newline>`,
  which is exactly what the residue flags). Net: `\<newline>#` can never smuggle a mask past
  `head` (k1 proves it dies for the wrong reason but dies).
- **H2 — `i==0` in the comment-start set:** `#` at position 0 of any `code_view` argument
  blanks — consistent with bash (`#!` shebang class); unreachable on the real slices.
- **H3 — consistent cases verified inert:** `#` after `{`, `!`, `;; `, mid-word (`foo#`),
  inside `'…'`/`"…"`/`$'…'`/`${…}`, in heredoc bodies that carry no scanner-token
  (`local nlegs`, `st_x=`, `esac`, `}`, `done`, `run_regression() {` are the lethal set).
- **H4 — `harness_section` regexes run on RAW text** (`HARNESS_START`/`HARNESS_END`/
  `EXTRACT_RE`, no `code_view`): a heredoc/comment carrying `local tblock` or a
  `tblock=$(awk …)` line could spoof the harness slice boundary — same class as
  CRITICAL-3, unexercised (the harness anchors live in `selftest`, a different function);
  flagged, not demoed.

## What I could NOT break (with proof)

- A false-accept where `code_view` blanks *executed code* as if it were a comment: no such
  direction exists — bash's `#` is only ever mid-word (data) or token-start (comment); the
  cv start-set is a subset of bash's token-start contexts *plus* the `i==0` edge, so
  "blanked-but-executed" is impossible in the unquoted state, and in the desynced state the
  blanked text is inside a bash string (still not code). The only "comment that executes"
  construction (`\<newline>#`) leaves the `\` residue and is killed at `head` (k1).
- Whole-file verdict stability on pristine: rc=0 PASS at the pin (baseline).
- Benign-instance controls: `( : )# esac` *outside* token-reach of `counting_case`'s tail
  (a1) and a `local nlegs=9` heredoc decoy with no payload (a9) both PASS — the mechanism
  fires only when the unblanked/data text hits a live scanner anchor.
- `{#`, `!#`, `;;#`, `foo#`, `x='#'`, `x=$'\''#…'` all behave consistently with bash
  (probes in `work/`).

## Residual risk / verification gaps

- Backquote substitutions containing unbalanced quotes, and `$()` containing heredocs, were
  not exercised (same class as the demonstrated ones; POSIX leaves some of it unspecified).
- `run_regression` is the only `re.M` line-anchored function-name scan; a heredoc or comment
  carrying `run_regression() {` earlier in the file could spoof `regression_body`'s entry —
  plausible by symmetry with CRITICAL-3, not demoed.
- The `>`/`<`-adjacent `#` family yields only parse errors (unrunnable copies), never a
  runnable divergent one — mapped, BOUND-2 covers the reachable shape.
- The deciding run's `ho_invalid`/`ho_distinct` interplay with a CRITICAL-2 specimen
  (a4-style: counter-valid kill that is semantically accept) was reasoned, not run — the
  run-abort bound (BOUND-1) may fire first for some shapes.

## Fix direction (for the record)

The view needs two more states: heredoc-body (enter on `<<`/`<<-` delimiter, exit at the
terminator line, blank or preserve the body consistently) and `$'…'` (with `\'` non-
terminating per §2.2.4); the comment-start set needs `)` (and `<`/`>` for completeness —
bash treats all of them as comment-introducing when `#` directly follows a completed
token); `\<newline>` should be erased rather than skipped-visible; `regression_body`'s brace
scan needs the quote/heredoc view too, not just comment-blanking; and the tool should read
the runner file in binary with an explicit decode so the audited bytes equal the scored
bytes. Until then, every structural check inherits these divergences, and the counter —
which shares `code_view` verbatim — inherits the same blindspots into ground truth.
