# Round-35 w2 — ScoutTailRegion

Seat: `L1tameshi35.ScoutTailRegion` (leaf scout, godspeed). Dispatch tip `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.

Attacked: round-34 hold (d) — "the tail region (selftest/harness anchors) is inspected by neither head_of nor tally_block_of" (`corpus/lessons/round-34.md`, Holds routed to round 35). Question: what lies between the end of the tally block and the end of `run_regression`, what lies after `run_regression`, whether v3 inspects each region, and what a defect there can change.

Pins (blob `7da6e076`, not the dirty worktree):

- `tools/tally-audit-v3.py` sha256 `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` (scratch copy `work/tally-audit-v3-7da6e076.py`; every `TALLY_AUDIT` line below is this file)
- `tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (106218 bytes, 2080 lines)
- frozen counter `.ufo/evidence/round-35/c1/c1-measure.py` sha256 `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8`

The prescribed clone path already existed at ancestor `d16f9b5a` (tool still `da23d3a2…`); it was not checked out and not written. During the scout the fleet worktree HEAD moved to `68f25573` and `tools/tally-audit-v3.py` became dirty (`ec236de2…`, uncommitted last-match / brace-depth cutter). That drift was not scored. No packages installed.

Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/ScoutTailRegion/work/`.

v3 has no `head_of` / `tally_block_of`. The hold's cutters are `head_section` (`tally-audit-v3.py:240-244`) and `tally_block` (`:229-237`). The frozen counter's `tally_block` (`c1-measure.py:132-153`) is the same cut and returns a byte-identical pristine block (sha below).

## Map

Cuts from the pinned cutter on the pinned runner (0-based byte offsets, end exclusive):

| region | bytes | lines | bytes len | sha256 |
|---|---|---|---|---|
| `regression_body` | 68425:75302 | 1345-1471 | 6877 | (whole function) |
| `head_section` | 68425:73739 | 1345-1431 | 5314 | `8b293fbe1794ebe81ae104b1e37f3be238de334c17bb12ab65761fdcff310d41` |
| `tally_block` | 73739:75301 | 1432-1470 | 1562 | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |
| gap (end of block → end of function) | 75301:75302 | 1471 | 1 | the character `}` |
| after `run_regression` | 75302:106218 | 1472-2080 | 30916 | `f2f727403079d72de41b550b7cc217f61f0f68fc8d08a92e74681aeb84c8e330` |

`tally_block` is `body[start_of_local_nlegs : rfind('}')]` on the comment-blanked view (`:229-237`). On this file the last `}` in the body is the function closer, so the block **includes** the loop, the three verdict `if`s, the workdir `rm`, and `exit 0` (lines 1432-1470) and **excludes** only the closer. The runner's own selftest awk (`mutate-and-run.sh:1994`, stop at a line that is exactly `}`) prints those same 1562 bytes (sha `e163133c…`).

There is no statement between the end of the block and the end of the function. A line inserted before the `}` lands **inside** the block. A line inserted after the `}` lands in the tail.

After the function, four subregions:

1. **Banner** lines 1472-1474 (blank, `# --- selftest`, blank). Not code.
2. **`selftest` before the harness** lines 1475-1991. Fixture setup, eleven `<<'EOT'` heredocs (first at 1495; `banner`/`say_hello`/`add`/`chk` are heredoc text, not runner functions), leg-count checks. The only top-level function defined after `run_regression` is `selftest` itself. Every callee of `run_regression` (`usage_exit`, `die_setup`, `regression_specs`, `sha_of`, `table_*`, `regression_case_git`) is defined **before** line 1345.
3. **Harness window** lines 1992-2040, bytes 101921:104843, len 2922, sha `b7ac097dca167b7693c03978aad964cbd0749d6d566dec6466e8d37f3a81c311`. From `local tblock tgot tvec ti tj` through `tblock=$tblock_full` (`HARNESS_START`/`HARNESS_END`, `tally-audit-v3.py:619-635`). One `EXTRACT_RE` hit: the awk line at 1994.
4. **Post-harness `selftest`** lines 2041-2054 (`--help`, missing `--target`, `--regression` refuses `--target`, `VERDICT` printf) and **main** lines 2056-2080 (the `while`/`case` that sets `KEEP`, `WORKDIR`, `TIMEOUT_S`, `MODE` and calls `run_regression` at line 2078).

`audit` (`:683-697`) feeds `head_section`/`tally_block` only the `regression_body`. The full file is passed only to `check_harness`, which keeps only the harness window. `brace_depth_at` (`:215-223`) is defined and has no caller; it counts raw braces (comment-blind and quote-blind). HYGIENE, not on the verdict path.

## What v3 inspects

| region | `head_section` / head+static | `tally_block` / runtime | `check_harness` |
|---|---|---|---|
| lines 1432-1470 (the block, including post-`exit 0` if you insert there) | reassignment scan only | yes, full stdout × 4 configs × 30316 vectors | no |
| line 1471 `}` | end marker only | end marker only | no |
| 1475-1991 selftest prologue + heredocs | no | no | no |
| 1992-2040 harness window | no | no | yes, assertions only; awk **result** overwritten |
| 2041-2054 selftest epilogue | no | no | no |
| 2056-2080 parser and dispatch | no | no | no |

Hold (d) is still true of the two named cutters: neither reads a byte after `run_regression`. Round 35 did not add a tail scan. The harness check is a third reader of one slice, and it discards the extraction it exists to guard (`run_harness` splices `tblock=$AUDIT_INJECT` after the last awk line, `:638-640`).

The frozen C1 oracle uses the same cut (`c1-measure.py:132-153`, `behavior` at `:204`). A tail-only edit has `block` equal to pristine, so `diverge` is empty: an accept label passes, a kill label is invalid (`score_copies:305-310`). Tail edits are outside the claim's behavior. They are not a false C1.

## Findings

### BOUND-1 — the live tail can retarget `--regression` while v3 returns PASS

The parser/dispatch (lines 2058-2080) runs on every invocation, before `run_regression`, and is outside every inspected span. `run_regression` reads `TIMEOUT_S`, `KEEP`, `WORKDIR`, `TARGET` from those bindings. Three copies, each with `head`/`block`/harness-section byte-identical to pristine (block sha `e163133c…`), frozen counter `tally_block` equal to pristine:

- **dispatch** sha `c41738e23f7617279cdd5a031b32ccce8f6d7103307913706f596da49c9c30d2`. Line 2078 replaced with `printf 'HIJACK\n'; exit 99`.
  - `bash work/dispatch.sh --regression` → **rc 99**, stdout `HIJACK`.
  - `bash tools/mutate-and-run.sh --regression --target /no/such` → **rc 64**, stderr `--regression takes no --target/...` (the function is entered).
  - `python3 work/tally-audit-v3-7da6e076.py --runner work/dispatch.sh` → **rc 0**, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, `vectors=30316 mismatched=0`.
  - Six-vector oracle (all-zero, one-1, one-2, one-3, one-255, `[1,2,0…]` × the four `(auto,KEEP)` configs) matches pristine.
- **timeout0** sha `fd4c7cda2c14c623a51c49145c1b74e614313fd1ba8de718b06c1557106e5e3b`. The `--regression` arm also sets `TIMEOUT_S=0`.
  - `bash work/timeout0.sh --regression` → **rc 64**, stderr `--timeout must be a positive integer` (dies at `mutate-and-run.sh:1349`, before any leg).
  - `bash -x tools/mutate-and-run.sh --regression --workdir <scratch>` → trace shows `TIMEOUT_S=300`, `KEEP=0`, `run_regression`, still running at 3s (`rc TIMEOUT`). The mutant never gets that far.
  - Same v3 command → **rc 0**, all four checks PASS.
- **syntaxarm** sha `d0beb87efc6b36a1675828217cbbbf3d5a82a37dda20aba241a52205d36d8f9f`. The regression arm is `regression) ( ;;` (syntax error **inside** the `case`, which bash parses before the loop runs).
  - `bash -n work/syntaxarm.sh` → **rc 2**, `syntax error near unexpected token ;;` at line 2078.
  - `bash work/syntaxarm.sh --regression` → **rc 2**, same diagnostic. Pristine `bash -n` on the pinned runner → **rc 0**.
  - v3 → **rc 0**, all four checks PASS. Frozen counter block equal to pristine.

A syntax error **after** the `esac` (copy sha `a4ebe4d8a4702c2a688c5704592a1abfc176edb0ab72d0df1bf6e894d0c694a3`, line 2082 `this is not valid shell (`) is weaker: `bash -n` is rc 2, but `bash copy --regression --target /no/such` is still rc 64, because `usage_exit` leaves the shell before the parser reads past the `case`. v3 still returns rc 0. v3 never runs `bash -n`.

**keep1** sha `096a764af63ec7b753332a215624aaa9de2f9c373d7457dcfa75ab0dff5683e4` sets `KEEP=1` on the `--regression` arm. `bash -x work/keep1.sh --regression --workdir <scratch>` trace: `KEEP=0` then `KEEP=1` then `run_regression`, process rc 2 (the copy's `FLEET_ROOT` is `dirname`³ of the scratch path, so legs SETUP). The PASS-only branch `if [[ $auto -eq 1 && $KEEP -eq 0 ]]` (`mutate-and-run.sh:1464`) was **not** observed to flip the workdir line on this host. The binding change is observed; the rm-on-PASS effect is source-level, not executed here. v3 → rc 0.

What this region can change: which function `--regression` calls, whether the script parses, and the `KEEP` / `TIMEOUT_S` / `WORKDIR` / `TARGET` values `run_regression` sees. What it cannot change: the extracted block's `(exit, full stdout)` under the four configs. Under the frozen predicate that is an accept, and v3 correctly PASSes. Under `bash <file> --regression` it is a different program. That is the hold, still open, fail-closed only relative to the block oracle.

### BOUND-2 — selftest outside the harness window is invisible; inside it, the awk result is discarded

- **selfprologue** sha `76f6d1ba0b7b2ae0adce09fd6dd8b7bb318783d3574b3d29b5bcac757b4be8a4`. Inserts `printf 'TAILSELF\n'` as the first line of `selftest` (line 1476, before the harness). `timeout 4 bash work/selfprologue.sh --selftest` → **rc 124**, stdout begins `TAILSELF | PASS sweep exits 0 | ...`. Block/harness bytes unchanged. v3 → **rc 0**.
- **verdict** sha `504168a1bc651bad375f473fbf6ddfc478e5674344fa27f3d227f3d7995c32f2`. Line 2048 `VERDICT: PASS` → `VERDICT: PASS-TAIL` (after `tblock=$tblock_full`, still inside `selftest`). Outside the harness section (section ends at the start of line 2041). v3 → **rc 0**. The new string was not executed to the end of `--selftest` (that path is the whole selftest); the byte is outside every span `audit` reads.
- **cmp** sha `2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c`. Inside the window, `tally_line`'s comparison dropped to `[[ $rc -eq $want_rc ]]` only (the pinned tool's own `harness exit-only` seed). v3 → **rc 1**, `CHECK harness FAIL reference cases=9; faults rejected=28/34; accepted: label fail-wording setup-wording verdict-word pass-wording printf-counts-swapped`. The assertion bytes **are** inspected.
- **awk** sha `b3cce6503f9b140724500db8fd373bf21d7feb46a06ad7b053e9d1489b9d0e2f`. The extract line still matches `EXTRACT_RE`, program replaced with `BEGIN{print "printf x"}`.
  - `awk 'BEGIN{print "printf x"}' work/awk.sh` → **rc 0**, stdout `printf x\n`.
  - Pinned awk on the pinned runner → **rc 0**, 1562 bytes, sha `e163133c…` (the tally block).
  - v3 → **rc 0**, harness `faults rejected=34/34`. The awk runs and its stdout is thrown away (`:640`).
  - Frozen counter block still equal to pristine (v3 does not use that awk). The runner's own `--selftest` would score `printf x` as the tally; v3 will not notice.

### BOUND-3 — the one-byte gap is a quote-blind fence (false SETUP, not a false accept)

`regression_body` (`:196-212`) counts `{`/`}` on `code_view`. Comments are blanked; quotes are not. A `}` inside quotes drops the depth to 0 and ends the body **before** the real closer. `tally_block` then `rfind`s that same `}`, so the block loses the closing quote.

**quotebrace** sha `332ace0efbbccb31133ff547bb5efab461f17b30619c51a81d1b2989c928c19a`. Inserts `  : '}'` immediately before line 1471. Body length 6882 (pinned 6877): the scan stops on the quoted `}`. Block length 1567 (pinned 1562), sha `97e5da53b9fc05e3e14defa13ea2b816caf971c2fc707559a9146df4bfb8621e`, ends in an open `'`.

- `bash -n work/quotebrace.sh` → **rc 0**.
- `bash work/quotebrace.sh --regression --target /no/such` → **rc 64**, same `--target` refusal as pristine (the quoted brace sits after `exit 0`; the early-exit path does not need it).
- Runner awk (line-anchored `^}$`, which `  : '}'` is not) → **rc 0**, 1570 bytes, tail `exit 0\n  : '}'\n`. Running that extract as a tally with all-zero legs → **rc 0**, stdout the normal PASS + `REGRESSION_WORKDIR: Z (kept)`. The runner's own extractor does not truncate.
- v3 → **rc 2** in 0.09s, `TALLY_AUDIT: SETUP (tally driver failed (exit 2, 0/7561 results): ... unexpected EOF while looking for matching '`)`.
- Frozen counter `tally_block` length 1567, not equal to pristine. `behavior` → `run_block` raises `SystemExit` (`c1-measure.py:200-203`) and `score_copies` (`:296`) does not catch it, so one such specimen aborts the deciding run instead of being marked invalid.

This is the round-34 comment-brace class, closed for comments and open for quotes, sitting on the tail boundary. It refuses a file bash accepts. It does not accept a divergent block.

## What I could not break

- **commentbrace** sha `d5b7b58334540c587a449183d8808784247059cc1ac4adee5b9915733b72bf1f`. Inserts `  # }` before the closer. `code_view` blanks it; the body still ends at the real `}`. The comment is inside the block (len 1568) but the six-vector oracle matches pristine on all four configs, and v3 → **rc 0**, `vectors=30316 mismatched=0`. A comment `}` does not reopen hold-(d)'s brace truncation.
- **deadghost** sha `1ac06b0f009e10484f8b3adbb153fdb20fc3082147003ec4583167ed4933ec49`. `printf 'GHOST\n'` between `exit 0` and `}`. That byte range is **inside** the block (len 1581), not in the gap. Six-vector oracle matches (the `exit` runs first). v3 → **rc 0**, 30316 matched. Unreachable epilogue is inspected and correctly accepted.
- **liveghost** sha `c289482888bf32b81c22517d8d2df3bc8fe2658898d59f0ef41af010084435fb`. Same printf with `exit 0` removed, so the epilogue is reachable. Six-vector oracle diverges on the all-zero vector under every config: stdout gains a `GHOST` line, exit stays 0. v3 → **rc 1**, `CHECK runtime FAIL vectors=30316 mismatched=40` (first mismatch is that PASS line). Head and harness still pass. A reachable in-function epilogue cannot hide.
- No copy whose edit was strictly after line 1471 changed block sha `e163133c…`. None of those can flip the frozen four-config oracle, so none is a C1 false accept or a missed kill under the predicate as written. Pristine v3 on the pinned runner → **rc 0**, `vectors=30316 mismatched=0`, `faults rejected=34/34`.

## Rank

- **CRITICAL:** none against C1 as frozen. The tail does not make a kill look like an accept under `behavior()`, and it does not make v3 PASS a block the oracle says diverges.
- **BOUND-1:** lines 2056-2080 (and any syntax error inside that `case`) are unread; they can stop `--regression` from calling `run_regression` or change `KEEP`/`TIMEOUT_S` before it does. v3 rc 0. Hold (d) stands for the two cutters.
- **BOUND-2:** lines 1475-1991 and 2041-2054 are unread (`--selftest` only). Lines 1992-2040 are executed, but the awk extract they anchor is overwritten, so a sabotaged extractor still PASSes.
- **BOUND-3:** the gap byte is quote-blind. A quoted `}` there is a false SETUP (v3 rc 2, counter `SystemExit`), while `bash -n` is clean and the runner's own awk still extracts a working block.
- **HYGIENE:** `brace_depth_at` is dead and comment-blind.

Not broken: comment-brace truncation at this boundary; unreachable post-`exit` bytes inside the block; a reachable post-`exit` byte (killed, `runtime` only).
