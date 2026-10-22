# FixtureOracle: round-25 C1 multi-token fixtures (R23-ROUTED-1)

Reviewer: TameshiR25.FixtureOracle (UFO-FSD reviewer, leaf member, no dispatch). Judged on: calibration.
Scope: `.ufo/evidence/round-25/multitoken-cases.json`, `c1-suite.py`, `multitoken-mutants.spec`, against gate `tools/command-binding.py`.
Writes: none in the lane. Scratch only under `/tmp/fo-r25/`.

Labels: [OBS] = I ran it and read the output. [READ] = read from the file. [INF] = inference, not observed.

## Verdict

- Expected exits and finding IDs are derivable from the contract prose and agree with the gate: 11/11 on the working tree, 7/7 at HEAD. [OBS]
- Every spec mutant is killed by a named fixture, for the reason the spec states: 6/6 at HEAD, 10/10 on the working tree. [OBS]
- No fixture depends on execution order. [OBS]
- Blocking: the frozen pins are stale. The working-tree cases and spec do not match the sha256 values in `contract.json`, and the amendment record they cite does not exist on disk. The R1 sweep holds on HEAD bytes and on working-tree bytes, but fails on a mix of the two. [OBS]
- Not wrong-reason-proof. The R1 witness rule credits gate crashes as kills. The ruler also passes four unlisted stdout variants: W5, W6 and W9 weaken the literal match, and W8 is stricter than it. Only W6 is caught, by the gate's own selftest; none is caught by the ruler. [OBS for the runs; the literal reading is [INF] for W8, see F3.]

The lane changed during review. Uncommitted amendment-2 edits to two of my targets appeared mid-review. Both states are reported below.

## Findings by severity

### F1 HIGH: pins drift, and the amendment record is missing

Evidence:
- Pins in `contract.json`: fixtures `ea64fca9…` (line 8), measure `b18460c7…` (line 10), multitoken spec `2a496199…` (line 13), suite `ae33a04b…` (line 16). `frozen_before_wave: true` (line 33). [READ]
- HEAD blobs (`git show HEAD:<path> | sha256sum`): cases `ea64fca9…`, suite `ae33a04b…`, spec `2a496199…`, gate `9230c68e…` (equal to the base `1f73157` gate blob). `git diff --stat c9ff09f HEAD -- <4 targets>` is empty. [OBS]
- Working tree now: `multitoken-cases.json` is `f0a4ac80…` (216 lines), `multitoken-mutants.spec` is `8ec3f56b…` (43 lines). `git diff --stat HEAD` shows +217 and +17 lines. Suite `ae33a04b…` and measure `b18460c7…` are unchanged. [OBS]
- The cases file says cases 8–11 were "added by contract amendment 2 (before any after measurement)" (`multitoken-cases.json:215`). The spec says M7–M10 were "added by contract amendment 2" (`multitoken-mutants.spec:28`). [READ]
- `contract-amendment-2.json` does not exist in `round-25/`. `c1-pins.py:41` reads its `c1_input_sha256`, so that checker exits 2 (SETUP) today. [OBS, READ]

Runner sweeps, same argv as `c1-measure.py:53-57`, staged under `/tmp/fo-r25`:

| Bytes under test | Cases | Defects | Control | Outcome |
|---|---|---|---|---|
| HEAD (pinned) | 7 | 6 (M1–M6) | GREEN | `defects=6 killed=6 survived=0`, restore OK |
| Working tree | 11 | 10 (M1–M10) | GREEN | `defects=10 killed=10 survived=0`, restore OK |
| HEAD cases + working-tree spec (mix) | 7 | 10 | GREEN | `defects=10 killed=6 survived=4` (M7–M10 SURVIVED, exit 0) |

Smallest correction: commit the cases and spec together with a `contract-amendment-2.json` that carries their new sha256 values (the `c1_input_sha256` map `c1-pins.py` reads). Or revert both to HEAD. Never measure a mix. Owner: planner.

### F2 MEDIUM: the R1 witness rule credits non-semantic FAILs

Evidence: `c1-measure.py:63` and `:133` count any line matching `^FIXTURE \S+ FAIL` as a witness. `c1-suite.py:63-69` prints FAIL with `findings=None` whenever the gate's stdout is not JSON. Probes on `/tmp` copies, run through the real suite [OBS]:
- SyntaxError gate (`def evaluate(bundle)::`): `suite_exit=1 loose_FAIL_witnesses=7 strict_parsed_witnesses=0`. Lines read `FIXTURE mt-missing-first FAIL (exit=1 findings=None)`.
- Missing gate path: `suite_exit=1 loose=7 strict=0`. Lines read `(exit=2 findings=None)`.
- Hang gate (`time.sleep(120)`): `subprocess.TimeoutExpired` after 30.1 s, suite exit 1, no FIXTURE lines. The runner counts any non-zero exit as KILLED (`mutate-and-run.sh:34-35`, `:59-60`). The measure does not credit it, because there is no witness.
- Flat copy of the suite: `IndexError` at `c1-suite.py:27` (`REPO = HERE.parents[2]`), exit 1, no FIXTURE lines.

Consequence: a typo in a spec `@new` that makes the gate crash would be credited as a kill. Smallest correction: tighten the R1 witness at `c1-measure.py:133` to `r'^FIXTURE \S+ FAIL \(exit=\d+ findings=\['`. The strict form still matches every current log (M1 5, M2 3, M3 3, M4 1, M5 2, M6 1, M7–M10 1 each), and matches none of the three probes. Because `c1-measure.py` is pinned, this needs the same amendment as F1.

### F3 MEDIUM: the ruler passes stdout variants

I ran four unlisted variants, each as a one-line edit to a `/tmp` copy of the gate, against the 11 working-tree cases and against the gate's own selftest. [OBS]

| Variant | 11 cases | Gate selftest | Status by contract |
|---|---|---|---|
| W5: space-run-only collapse, `re.sub(' +',' ',stdout)` | SURVIVES | 44/44, survives | Weakens literal match. Contract-determined. |
| W6: stderr counted as stdout | SURVIVES | FAILS `CASE stderr-cannot-supply-token` (`command-binding.py:155`) | Contract-determined: `stdout_contains` checks stdout. No C1 spec models it. |
| W8: word-boundary match, `(?<!\S)tok(?!\S)` | SURVIVES | 44/44, survives | Stricter than literal match. Divergent under the fleet literal rule [INF]. |
| W9: `token.strip()` | SURVIVES | 44/44, survives | Weakens only tokens with edge whitespace. Not tested. |

The suite cannot express stderr: `c1-suite.py:37` hard-codes `'stderr': ''`. W6 therefore needs a suite amendment, and until then only the gate selftest catches it.

Candidate data-only fixtures (not applied; verified on `/tmp` copies of the suite with 14 cases). Pristine passes all 14. [OBS]
- C-a `mt-space-run-collapse`: requirement `a-gate`, tokens `["ALPHA BETA"]`, stdout `"ALPHA   BETA\n"`, expected exit 1 with `["STDOUT_MISMATCH"]`. Kills W5. Also gives M10 a second killer.
- C-c `mt-token-inside-word`: tokens `["ALPHA"]`, stdout `"ALPHABETA\n"`, expected exit 0 with `[]`. Kills W8. Needs an owner decision, because it rests on the fleet literal rule [INF].

### F4 LOW: attribution gaps and an overstated amendment note

- M4 and M6 each have exactly one killer (`mt-offending-sorted-second`, `mt-offending-sorted-first`). [OBS]
- Every multi-row fixture declares rows in name order, so sorted order is never isolated. A variant that iterates declared order is killed only by `mt-offending-sorted-second`, exactly as M4 is. [OBS]
- Candidate C-b `mt-declared-out-of-order`: rows `b-good` (`ALPHA BETA`) then `a-bad` (`ALPHA`), expected exit 1 with `["STDOUT_MISMATCH"]`. Pure data, no suite change. Gives the declared-order variant and M6 a second killer, and leaves M4 unchanged. [OBS]
- The amendment note calls M7–M10 "strictly weaker" (`multitoken-cases.json:215`). M7–M9 are monotone weakenings. M10 is not: token `ALPHA  BETA` (two spaces) with stdout `ALPHA  BETA\n` gives pristine `(0, [])` and M10 `(1, ['STDOUT_MISMATCH'])`. [OBS] Correct the wording to "three weakenings and one normalization".
- Case name `mt-newline-insensitive-token` tests newline-to-space collapse only. The M10 description says "whitespace-collapsed", which is broader. W5 is the gap this leaves. [READ]

### F5 LOW: suite error handling does not match its own exit contract

The suite's docstring says exit 3 is a setup error. Two paths bypass that contract. `c1-suite.py:61` (`timeout=30`) is not wrapped, so a hang becomes a traceback with exit 1, which the runner counts as KILLED. `c1-suite.py:27` runs at import, so a flat copy fails before any fixture runs. Both are caught by the witness requirement, so no false credit reaches the measure. Smallest correction: wrap the subprocess call in `try/except (subprocess.TimeoutExpired, OSError)`, print `FIXTURE <name> ERROR`, return 3, and move `REPO` into `selftest()`. Needs the same amendment as F1.

## Answers to the three questions

1. Derivable? Yes. I wrote a prose oracle from the contract text, not from `evaluate()`. Its rule is: each required token must be a literal, case-sensitive substring of that requirement's stdout; any miss adds `STDOUT_MISMATCH`; exit is 1 iff there is a finding. It matches all 11 working-tree expectations and all 7 HEAD expectations, and the pristine gate matches all 11. Confidence: high for the numbers. The literal and case-sensitive reading is inherited from `registry-check.py:35-37`, which defines the same key for the fleet. `command-binding.py` does not state it [INF]. Whether the expectations were written before any gate run cannot be checked from the tree. The `revision` value `1111…` is a placeholder, which suggests hand-authored fixtures, but that is not proof.

2. Mutant to fixture: observed by running the real suite on real mutant copies. Killers listed are forward-order results. Reverse order gave identical sets.

| Mutant (stated reason) | Killing fixtures, observed `exit findings` | For the stated reason? |
|---|---|---|
| M1 any-of, not all-of | mt-missing-first, mt-missing-middle, mt-missing-last, mt-offending-sorted-first, mt-offending-sorted-second: each `0 []` | Yes. Each case has some but not all tokens present. |
| M2 first token only | mt-missing-middle, mt-missing-last, mt-offending-sorted-first: `0 []` | Yes. The missing token is not first. |
| M3 last token only | mt-missing-first, mt-missing-middle, mt-offending-sorted-second: `0 []` | Yes. The missing token is not last. |
| M4 first sorted row only | mt-offending-sorted-second: `0 []` | Yes. Single killer. |
| M5 contiguous and declared order | mt-clean-reordered, mt-clean-two-requirements: `1 ['STDOUT_MISMATCH']` on clean cases | Yes. Over-strict on reordered clean output. |
| M6 last-wins reset | mt-offending-sorted-first: `0 []` | Yes. Single killer. |
| M7 case-folded | mt-case-folded-token (`alpha` against `ALPHA`): `0 []` | Yes. |
| M8 space-stripped | mt-space-insensitive-token (`ALPHABETA` against `ALPHA BETA`): `0 []` | Yes. |
| M9 punctuation-stripped | mt-punctuation-insensitive-token (`ALPHA,` against `ALPHA`): `0 []` | Yes. |
| M10 whitespace-collapsed | mt-newline-insensitive-token (`ALPHA BETA` against `ALPHA\nBETA\n`): `0 []` | Yes for newline. Broader wording, see F4. |

Predicted kill sets from the spec's stated behaviour matched the observed sets for all 10 mutants, on both the working-tree cases and the HEAD cases.

3. Order dependence and wrong-reason passes. No execution-order dependence: forward and reversed case order gave identical killer sets for all 10 mutants and identical 11/11 for pristine. Each case runs in a fresh gate process (`c1-suite.py:59-61`) with freshly written bundle and expected files (`:56-58`). Wrong-reason passes and kills are in F2 and F3.

## Smallest safe corrections (none applied)

- C-1 (F1, blocking, planner): commit cases and spec together with `contract-amendment-2.json`, or revert both to HEAD.
- C-2 (F2): tighten `c1-measure.py:133` to the strict witness regex.
- C-3 (F3, data only): add C-a `mt-space-run-collapse` and C-b `mt-declared-out-of-order`. Add C-c `mt-token-inside-word` only after an owner decision on word semantics. Each addition changes the fixtures pin, so it belongs in C-1.
- C-4 (F3, needs suite amendment): let `bundle_for` take stderr, then add an stderr-only fixture (W6).
- C-5 (F5): wrap the subprocess call and move `REPO` into `selftest()`.
- C-6 (F4): change "four strictly weaker" to "three weakenings and one normalization".

## Residual risk and verification gaps

- I replicated the R1 runner sweep exactly, same argv and spec. I did not run the full `c1-measure.py`, because it needs R2 and R3 inputs and a full staged tree. R2 and R3 are not reviewed here.
- The lsp device is unavailable. `read xd://lsp` returned "No such tool: xd://lsp. Mounted devices: ast_edit, debug", and the in-kernel `tool.lsp` call returned "Unknown tool from js runtime: lsp". Caller checks are therefore the literal text-grep fallback, not semantic proof. Callers found by grep: `c1-measure.py:51-70` (stages and runs the spec), `registry-replay.py:111` (builds `command-binding-v1` bundles in the same gate format), and unrelated gates in `registry.json`.
- The lane changed during review. Uncommitted edits to two of my targets, and to `guard-mutants.spec` and `tools/mte-interop.py`, appeared mid-review. None of those edits was mine. All hashes above are as observed at the time and may have moved.
- Not verified: whether cases 8–11 were authored before any after-measurement (no record exists), and whether `c1-pins.py` passes once amendment 2 lands.
- The W8 expectation (C-c) and the literal reading generally rest on [INF] cross-tool inheritance of the key semantics.

## Tools

- Installed or updated: none. I used the system `python3` (3.14), `bash`, and `git` with `GIT_OPTIONAL_LOCKS=0`, read-only.
- Scratch under `/tmp/fo-r25/` (`amend-runner`, `amend-eval`, `probe`, `probe2`, `cand2`, `st-*`) is outside the lane and can be removed.
- No lane writes, no git write commands, no subagents.
