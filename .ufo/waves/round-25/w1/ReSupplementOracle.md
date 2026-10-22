# R23-REATTACK SupplementOracle (round 25, wave 1)

**Verdict: AGREE.** The attacked binding holds. All 19 expected exits and exact finding sets in `.ufo/evidence/round-23/extra-cases.json` match the outcomes that the command-binding contract requires for their bundles. They hold at the frozen round-23 tool (commit 496d212, blob 23eab57) and at lane revision c9ff09f (blob 1b4bbb7). They still apply at c9ff09f: the fixture bytes are unchanged since 496d212, `evaluate()` is unchanged, and the active registry row `command-binding-selftest-r24` runs them (44/44 at c9ff09f).

Residual, not a counterexample: the 19 cases plus the round-24 fixtures do not pin stdout multi-token matching. A last-token-only check (M10) and a contiguous, in-order check (M12) both pass the whole active selftest at c9ff09f. The gap is already recorded and routed (R23-ROUTED-1). None of the 19 expectations is wrong because of it (section 5).

Scope: read-only attack, leaf member, no subagent dispatch, no repo writes except this file. Scratch work lives under /tmp only.

Runtime: Python 3.14.8 (`/usr/bin/python3`) for every run.

Device check: `read xd://lsp` returned "No such tool: xd://lsp. Mounted devices: ast_edit, debug." The `lsp` device is unavailable. Caller and definition checks below use literal text grep. Grep output is not semantic proof.

Confidence: high on the 19 expectations (hand derivation, docstring, and execution at two revisions). High on the mutant survivors (executed at c9ff09f). Medium on caller coverage (grep fallback only).

## 1. Seat status (R23-ROUTED-3)

- The round-23 SupplementOracle seat produced no output.
  - `TameshiR23.SupplementOracle.md` under `~/.omp/agent/sessions/-Projects-shokunin/2026-10-21T03-31-39-302Z_01a15c83-…/TameshiR23/` is 0 bytes (sha256 prefix e3b0c44298fc1c14, the empty-string hash).
  - The transcript named in `.ufo/waves/round-23/original-outcomes2.json` (`TameshiR23.SupplementOracle.jsonl`) does not exist (`wc -l` returned "No such file or directory").
  - The same row records `status: failed`, `final_output_chars: 0`, and `death_basis: no task-result callback retained`.
- This re-attack is the first evidence for the 19 cases in round 25.
- The item text is verbatim at `.ufo/waves/round-23/task-call2.json`, raw line 267.

## 2. Semantic check of the 19 expectations

Method: for each bundle I derived the exit and finding set from the bundle content and the contract text, then compared. Contract text: `tools/command-binding.py:2-17` (docstring: exact name; exact argv with no shell normalization; canonical absolute cwd; full revision; integer exit; required stdout tokens must match; nonzero expected exits are valid; held flags, source-read counts and filenames never establish execution; exit codes 0 clean, 1 failed, 2 could-not-evaluate, 64 usage). Outcome table: `corpus/knowledge/required-command-binding.md:23-27`.

| # | case (line in extra-cases.json) | expected | why, from the bundle |
|---|---|---|---|
| 0 | argv-order (:71) | 1 ARGV | receipt `one` has reordered argv tokens |
| 1 | argv-missing (:140) | 1 ARGV | `--selftest` dropped |
| 2 | argv-extra (:211) | 1 ARGV | extra token `--skip` |
| 3 | argv-joined-collision (:280) | 1 ARGV | one token `gate.py --selftest`; a join-based compare would wrongly pass |
| 4 | argv-normalized (:350) | 1 ARGV | `./gate.py` is not normalized to `gate.py` |
| 5 | argv-second-only (:419) | 1 ARGV | `two` argv is `[cat, gate.py]`, a source read |
| 6 | unknown-added (:502) | 1 MEMBERSHIP | extra receipt `extra`; name sets differ |
| 7 | all-stale (:572) | 1 REVISION | both receipts have a revision different from the bundle |
| 8 | second-cwd (:642) | 1 CWD | `two` cwd is `/elsewhere` |
| 9 | multiple-findings (:713) | 1 ARGV, CWD, EXIT | `one` has argv and cwd errors; `two` exits 0 where 1 is required |
| 10 | receipt-order-clean (:781) | 0 | receipts reversed; matching is by name; expected nonzero exit (`two` = 1) is valid |
| 11 | stderr-clean (:849) | 0 | stderr is `informational`; only stdout tokens are checked |
| 12 | stdout-surround-clean (:917) | 0 | `prefix\nPASS\nsuffix` contains the literal token |
| 13 | duplicate-before-malformed (:1004) | 2 INVALID_RECEIPT | duplicate `one` plus a malformed row; structural rejection comes first |
| 14 | unknown-expect-key (:1077) | 2 INVALID_REQUIREMENT | extra key `stdout_not_contains` |
| 15 | unknown-receipt-key (:1148) | 2 INVALID_RECEIPT | extra key `held: true` |
| 16 | unknown-bundle-key (:1219) | 2 INVALID_BUNDLE | extra key `commands_executed_count: 99` |
| 17 | argv-shell-string (:1285) | 2 INVALID_RECEIPT | argv is a string, not a list |
| 18 | all-of-tokens (:1356) | 1 STDOUT | required `[PASS, SECOND]`; stdout is `PASS\n` |

Findings:

- Every expectation matches the docstring and the knowledge table. Missing, unknown, mismatched or wrong-exit receipts give 1. Malformed shapes give 2. Clean bundles give 0.
- The expectations are not copied from the final tool's output. An earlier draft, `.ufo/evidence/round-23/pre-review-command-binding.py`, fails cases 13 to 16 (0-based). The draft-to-final changes include the behaviours those cases expect (structural validation before the duplicate check for case 13; key-set checks for cases 14 to 16), plus an expected-file key check and the round-24 loader.
- Exit and exact finding set are both compared, in the fixture runner and in the selftest (`tools/command-binding.py:132-194`). Neither check is output-only.
- The clean expectations are not vacuous. A mutant that over-rejects flips them (section 5, O1 and O2).

## 3. Execution at both revisions

- A Python driver in /tmp wrote each bundle and an expected digest to a temp directory and ran the tool's CLI in check mode (`--bundle … --expected … --json`).
- Results:
  - working tree: 19/19
  - blob at 496d212 (`23eab57`): 19/19
  - blob at c9ff09f (`1b4bbb7`): 19/19
  - round-24 fixtures (6 cases) at c9ff09f: 6/6
- The working-tree file equals the c9ff09f blob. `git status --porcelain -- tools/command-binding.py` is empty.

## 4. Does the finding still apply at c9ff09f?

Yes. Each point below was checked with a read-only git command (`GIT_OPTIONAL_LOCKS=0`).

- Fixture unchanged: `git diff --quiet 496d212 c9ff09f -- .ufo/evidence/round-23/extra-cases.json` exits 0. The content sha256 prefix is `87bffdc829ad705c` at both revisions.
- Tool changed only in the selftest loader: `git diff --stat 496d212 c9ff09f -- tools/command-binding.py` reports `1 file changed, 5 insertions(+), 4 deletions(-)`. Those lines add the round-24 fixture file to `selftest()`. `evaluate()` (`tools/command-binding.py:65-113`) and `check()` (`:115-130`) are unchanged.
- Registry, `tools/registry.json`:
  - `command-binding-selftest` (expects 38/38, source `SKILL.md@496d212:2019`) is `superseded`, with `superseded_by: command-binding-selftest-r24`.
  - `command-binding-selftest-r24` is `active`, with argv `python3 tools/command-binding.py --selftest` and expect `COMMAND_BINDING_SELFTEST: 44/44 pass`.
  - `SKILL.md:2081-2083` states that the 38/38 row is excluded from the active tally.
- Run of the active row's argv in a `git archive c9ff09f` export under /tmp: `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0. The 44 cases are 17 base, 19 round-23, 6 round-24, plus `tampered` and `duplicate-json-key`.
- Callers (grep fallback; the `lsp` device is unavailable):
  - the three active registry rows (`command-binding-selftest-r24`, `command-binding-frozen-clean-pinned`, `command-binding-source-read-red-pinned`);
  - `tools/registry-replay.py:111-124`, which builds bundles and expected files with the same schema strings;
  - round-25 staging, `.ufo/evidence/round-25/c1-measure.py:44-47`, and `c1-suite.py`;
  - round-24 `measure.py`, which runs the selftest under its mutants.

## 5. What the 19 do and do not pin (residual)

I made 20 one-at-a-time string mutants of the c9ff09f tool. Each anchor string occurs exactly once and each mutant compiles. Each mutant was run through the CLI on the 25 fixture cases (19 round-23 and 6 round-24). A case "kills" a mutant when its exit or exact finding set changes.

| mutant | kills among round-23 19 | kills among round-24 6 |
|---|---|---|
| M01 argv guard removed | 7 | 4 |
| M02 argv name-insensitive (receipt argv in any requirement's argv) | 0 | 1 (`argv-swapped-between-names`) |
| M03 argv space-joined compare | 1 | 0 |
| M04 argv first token only | 5 | 4 |
| M05 cwd guard removed | 2 | 0 |
| M06 revision guard removed | 1 | 0 |
| M07 exit guard removed | 1 | 1 |
| M08 membership guard removed | 1 | 0 |
| M09 stdout `any(...)` replaced by `all(...)` | 1 | 0 |
| **M10 stdout last token only** | **0** | **0** |
| M11 stdout first token only | 1 | 0 |
| **M12 stdout contiguous, in declared order** | **0** | **0** |
| M13 stdout may count stderr | 0 | 0 |
| M14 findings truncated to one | 1 | 0 |
| M15 first requirement only | 3 | 0 |
| M16 unknown expect key accepted | 1 | 0 |
| M17 unknown receipt key accepted | 1 | 0 |
| M18 unknown bundle key accepted | 1 | 0 |
| M19 bool exit accepted | 0 | 0 |
| M20 string argv accepted | 1 | 0 |
| O1 over-rejection control: stderr non-empty fails | 1 (`stderr-clean`) | – |
| O2 over-rejection control: stdout must equal joined tokens | 13 (includes the three clean cases 10, 11, 12) | – |
| earlier draft (not a mutant) | 4 of 19 fail (cases 13 to 16) | – |

Active selftest at c9ff09f (44 cases; exit and findings both checked), run from the /tmp export with each mutant substituted in the copy:

- unmodified: `44/44`, exit 0.
- M02: `43/44`, FAIL `argv-swapped-between-names`. Killed; the round-24 fixture closes the ArgvExact item from round 23 (`.ufo/waves/round-23/fresh-adjudication.json:53`).
- M10: `44/44`, exit 0. **Survives.**
- M12: `44/44`, exit 0. **Survives.**
- M13: `43/44`, FAIL `stderr-cannot-supply-token`. Killed by a base case, not by the 19.
- M19: `43/44`, FAIL `bool-exit`. Killed by a base case, not by the 19.

What this means:

- The 19 expectations are correct for the correct tool. Under M10 and M12 they still pass, so they do not pin every stdout multi-token rule. The docstring requires all required tokens to match. A receipt with stdout `SECOND\n` for required `[PASS, SECOND]` must exit 1; under M10 it exits 0. Case 18 checks only that one missing token gives STDOUT. It does not separate all-of from last-only or contiguous matching.
- The gap is already recorded. `corpus/knowledge/replay-projection-hardening.md:53-54` says last-token-only matching survives (PredK4). `corpus/lessons/round-24.md:97-98` lists K4 last-token-only as "nothing". The routed fix is R23-ROUTED-1 (`.ufo/evidence/round-25/c1-measure.py:11-14`, `multitoken-mutants.spec` M3 and M5).
- At c9ff09f no registry row runs `multitoken-cases.json`. `git grep -n multitoken c9ff09f -- tools` returns no matches, and no registry row argv mentions multitoken, mutants, round-25 or c1-suite.
- Case 12 pins literal substring matching as clean. That is the accepted semantics: `corpus/knowledge/required-command-binding.md:17` says "optional literal stdout tokens", and the loose-token tightening was rejected in `fresh-adjudication.json:118`.

## 6. Smallest safe correction (verified in /tmp, not applied)

Both candidates use one requirement named `two-token`, argv `[gate, --check]`, exit 0, expect `stdout_contains [PASS, SECOND]`, bundle revision `a`×40, cwd `/fixture/repo`, and a receipt with the same argv, cwd, revision and exit 0.

- candA: receipt stdout `SECOND\n`; expected `(1, [STDOUT_MISMATCH])`. The lane tool matches. M09 and M10 mismatch, so both are killed.
- candB: receipt stdout `PASS\nNOISE\nSECOND\n`; expected `(0, [])`. The lane tool matches. M12 mismatches, so it is killed. M11 is not killed by either candidate, but case 18 already kills it.

Smallest safe change: add candA and candB as a new append-only round-25 fixture file; load it in `selftest()`; register a successor row expecting `46/46`; mark the 44/44 row superseded. Do not edit the frozen round-23 `extra-cases.json`. This belongs to C1 (R23-ROUTED-1). I made no repo writes.

[INFERENCE, not executed] C1's own `multitoken-cases.json` rows `mt-missing-first` and `mt-clean-reordered` appear to kill M10 and M12 by the same mechanism. I did not run C1's suite, which is outside this item.

## 7. Residual risk and verification gaps

- `lsp` is unavailable. Caller and definition checks are literal grep only.
- The expected outcomes were checked against the docstring and the knowledge table, which I read. I did not check them against any external specification.
- I did not run the registry gates, the C1 suite, `mutate-and-run.sh`, the replay, or the pinned gates. Those are outside this item. The active selftest was run only in a `git archive` export under /tmp.
- Mutants are string-level substitutions. They do not cover the whole mutation space.
- This report makes no producer-identity, promotion, or score claim.

## 8. Tooling record

No tool was installed or updated. Used: Python 3.14.8, jq, and read-only git (`GIT_OPTIONAL_LOCKS=0`, plus `git archive` into /tmp). Repo writes: this report only.

R23-REATTACK SupplementOracle: AGREE
