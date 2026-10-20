# NullCritic — round-13 w1 adversarial review (C2 companion metadata)

Seat: critic, read-only. I wrote only this report and sent two peer messages to `TameshiR13.MetadataRepair`. I ran no gate, selftest, test, build, lint or formatter. I used read-only reads, `sha256sum`, `git log`/`ls-files`, and one in-memory Python comparison: I imported the module and compared `build_companion()` with the landed JSON, without calling `run_check` or `--selftest`. I installed or updated no tools.

Reviewed state: `tools/witness-metadata.py` sha256 `48f162cc…2f4e` (994 lines) and `.ufo/evidence/round-13/witness-metadata.json` sha256 `5a8f7192…e32b`. The executor was still editing while I reviewed. L1 must review the final bytes again.

## Axes
- **A1 null authority:** the original nested null must not act as the authority for `kind`. It also must not disappear.
- **A2 no blind upgrade:** normalization must not make the prior-exposed declaration look blind.
- **A3 frozen integrity:** no round-12 bytes may be rewritten.
- **A4 gate honesty:** IDs, exits and selftest expectations must match what the gate can actually reach.

## Frozen facts (observed)
- **The null is a producer bug.** `tools/bash-witness-study.py:787` reads `declaration["declared"]["kind"]`. `:875` writes `kind` at the top level instead. The tool's current sha is `249d9dcd…`, which is the digest recorded in `summary.json#/tool`. The tool is unchanged since `9df9212`.
- **Authoritative value:** `declaration.json:6` is `declared-witness mapping (not a blind preregistration)`. Its digest `e8d2024a…` is the same digest frozen before the sweep in `declaration-before-run.txt:3`.
- **Three non-identical phrasings exist:**
  - top-level kind: parentheses form;
  - disclosure prefix: `declared-witness mapping, not a blind preregistration:` (comma form). `disclosure[:len(kind)] == kind` is False.
  - `declared.tsv:9`: `NOT a blind preregistration`.
  Only the top-level literal is a valid normalized value. The other two corroborate it but are not sources.
- **Substring trap:** `"blind preregistration" in EXPECTED_KIND` is True. Any keyword or substring test would accept the blind label.
- **Two frozen summaries hold the null, and both are in the manifest:**
  - `summary.json` `acc01268…`
  - `rerun-20261020T035435Z/summary.json` `6726421f…`
  Both have `declaration.sha256 == 0def…` and the same disclosure as the declaration, byte for byte. I verified this.
- **Measurement copies:** `after-committed.json:69` (`2fd2fd6e…`) and `after-worktree.json:69` (`7c74b23e…`) embed the null through `measure.py:26,36`. These are historical copies and must not be rewritten.
- **Round-13 measurement is clean:** round-13 `measure.py` does not embed the frozen summary. It records only `frozen_summary_sha256` and the companion, so it does not spread the null again.
- **Dangling reference:** `declared.tsv:9-10` points to an "evidence README" for the disclosure, but `BashWitness/` has no README. The companion correctly cites `declaration.json#/disclosure` instead.

## Allowed correction semantics (exact)
1. **New file only.** Nothing may be written under `.ufo/evidence/round-12/`. Do not regenerate `summary.json`. Do not edit `tools/bash-witness-study.py:787` this round: that would separate the live tool from the recorded producer digest `249d9dcd…`, which WitnessFinish §6 deliberately preserved.
2. **Normalized kind** is exactly equal to the pinned literal and to `declaration.json#/kind`, with no substring, case-folding or keyword matching. It must not be taken from the disclosure, from `declared.tsv`, or from `summary.json#/declaration/kind`.
3. **Disclosure** is byte-equal to `declaration.json#/disclosure` and to `summary.json#/declaration/disclosure`. The companion must carry it in full, plus `prior_exposure: true` and `blind: false`. Both flags are required; if either is missing or flipped, the gate goes red.
4. **The original null is kept as a fact.** The companion records `value: null` at `summary.json#/declaration/kind`, tied to the summary digest. If that record is omitted, or rewritten to a non-null value, the gate goes red.
5. **The companion adds metadata. It does not supersede anything.** The measured claim, kill counts and scalars stay unchanged (calibration stays at 6). No promotion credit is claimed.
6. **Every frozen null is either covered or named.** Here that means the rerun summary. The round-12 `after-*.json` copies need a name in the LOG/lesson, because Main owns that integration.

## Landed implementation versus the conditions

Met:
- exact `EXPECTED_KIND` equality;
- top-level kind checked against the literal;
- disclosure literal plus its sha;
- `prior_exposure is True` and `blind is False`, both with missing-key arms;
- original null with omitted and rewritten arms;
- digest pinning in the tool before any parse;
- strict JSON (no duplicate keys, no NaN);
- the old-null companion fails with `normalized_kind_null`/1;
- a `wrong-kind-blind` arm with `blind preregistration`;
- the rerun null is now named (`named-residual-uncorrected`);
- the landed JSON equals `build_companion()` (I observed True).

### Defects (owner: MetadataRepair; both messaged)

**D1 (A4, high): the selftest will be red as written. This is a static derivation; I did not execute it.**
- `_fail` (`:243-247`) returns `snapshot_tampered` only when the reason ends with `_digest_mismatch`.
- Three cases expect `snapshot_tampered`, but their reasons do not end that way, so they get `input_unavailable`:
  - `extra-input-red` (`companion_inputs_mismatch`)
  - `missing-digest-red` (`companion_digest_invalid`)
  - `unpinned-digest-red` (`companion_digest_unpinned`)
- `path-escape-red` expects `path_rejected`. But the path-equality check at `:371-372` fails first with `companion_path_mismatch`, so `safe_input_path`'s `..` branch cannot be reached from the companion.
- **Fix:** use an explicit set of tamper reasons, and expect `companion_path_mismatch` for path-escape (or reorder the checks). Then require `SELFTEST: PASS N/N`.

**D2 (A1/A2, high): unknown keys and free text are accepted.**
- `run_check` only reads named keys.
- **Counterexample:** take the green companion and add `declaration.preregistration: "blind"`, or `original_nested.authoritative: true`, or rewrite `original_nested.note` / `purpose` to say "the null remains authoritative". Every named check still passes, so the result is exit 0 `metadata_consistent`. The companion would then assert blindness or null authority while the gate is green.
- **Smallest fix:** after the named checks, add `if companion != build_companion(): _fail("companion_noncanonical", 1)`. Add selftest arms `extra-blind-key-red` and `nested-null-authority-note-red`, each expecting `metadata_inconsistent`/`companion_noncanonical`/1.

**D3 (A1, medium): the rerun residual is asserted, never verified.**
- `scope.uncovered_null_observations` compares the companion only with the tool's literals (`:435-447`). The gate never hashes `rerun-…/summary.json` and never reads its `kind`.
- **Counterexample:** edit the rerun summary to say `kind: "blind preregistration"`. The gate stays green while the companion still states that the rerun's value is null.
- **Fix:** hash the rerun file against `6726421f…` (exit 2 `snapshot_tampered` on mismatch). Assert that its nested kind is null and that its disclosure and declared sha are equal to the declaration's.
- **Tradeoff:** the same declaration binds both summaries, so covering the rerun outright costs nothing. Keeping "uncorrected" is honest only if the gate verifies it.

### Lower-severity notes (no change required)
- The schema, `generated_for` and `expected` checks return exit 1 before the input digests are checked. So a tampered input plus a wrong schema gives 1, not 2. These checks cover companion structure, not comparison with frozen semantics, so the ordering is acceptable. Do not claim strict integrity-first ordering for them.
- These checks cannot be reached in either live or selftest runs, because pinned digests fail first: `top_level_kind_invalid`, `source_disclosure_*`, `summary_*`, `declared_*`. They are defensive only. L1 must not cite them as exercised arms.
- `manifest.json` (`273ffc39…`) and `declaration-before-run.txt` (`d2343ddf…`) are not pinned. The tool literal `e8d2…` already matches the pre-sweep freeze line. Pinning `declaration-before-run.txt` would let the gate prove that the kind was declared before the run, instead of relying on the literal. This is optional.

## Checks L1 should run (not executed here)
1. `sha256sum` on the frozen round-12 files must give exactly:

   | File | sha256 |
   |---|---|
   | `BashWitness/summary.json` | `acc01268…` |
   | `BashWitness/rerun-20261020T035435Z/summary.json` | `6726421f…` |
   | `BashWitness/declaration.json` | `e8d2024a…` |
   | `BashWitness/declared.tsv` | `0def0d3b…` |
   | `BashWitness/manifest.json` | `273ffc39…` |
   | `BashWitness/declaration-before-run.txt` | `d2343ddf…` |
   | `after-committed.json` | `2fd2fd6e…` |
   | `after-worktree.json` | `7c74b23e…` |

   Also `git diff --quiet 546b371 -- .ufo/evidence/round-12 tools/bash-witness-study.py` must exit 0.
2. `python3 tools/witness-metadata.py --selftest` must exit 0 with `SELFTEST: PASS N/N`. As of this review, D1 predicts 4 failing cases.
3. `python3 tools/witness-metadata.py --check --json` must give `metadata_consistent`/0 with `normalized_kind == "declared-witness mapping (not a blind preregistration)"`.
4. D2 negative check, in a temp copy of the lane: add `"preregistration":"blind"` to the companion's `declaration` and run `--check --lane-root <tmp>`. It must be exit 1, not 0. Repeat with `original_nested.note` rewritten.
5. D3 negative check, in a temp copy: change the rerun summary's `kind`. It must be exit 2 if the rerun is covered. If the gate stays green, the rerun disposition is unverified, and L1 must say so.
6. `python3 tools/witness-metadata.py --emit | diff - .ufo/evidence/round-13/witness-metadata.json` (allowing for the trailing newline) must show no semantic difference.
7. Grep the companion and the round-13 lesson/LOG text for `blind` and `preregistration`. Every hit must sit inside `not a blind preregistration` or `"blind": false`.

## Addendum: re-read after executor fixes (tool sha256 `176503af…bf13`, 1088 lines; companion `46328227…bd8d`)
All three fixes were checked statically against the current bytes. I did not execute anything.
- **D1 closed.** `SNAPSHOT_TAMPER_REASONS` (`:244-251`) now maps `companion_inputs_mismatch`, `companion_path_mismatch`, `companion_digest_invalid` and `companion_digest_unpinned` to `snapshot_tampered`. `validate_relative_path` (`:308-317`) runs at `:393`, before the path-equality check, so `path-escape-red` now reaches `path_rejected`.
- **D2 closed.** The canonical-equality check `companion != build_companion()` now runs last and returns `companion_noncanonical`/1 (`:588-589`). The `extra-blind-key-red` arm adds `declaration.preregistration="blind"` and expects exactly that result. A rewritten `note` or `purpose` is also rejected by the same equality check. No dedicated selftest arm covers a rewritten note; adding one would be optional hardening.
- **D3 closed.** The rerun summary is now read through `safe_input_path` and hashed against `6726421f…`; a mismatch gives `rerun_summary_digest_mismatch`/2, `snapshot_tampered`. The gate asserts that the rerun's nested null is still null and that its disclosure and declared sha equal the declaration's (`:473-491`). Two arms cover this: `tamper-rerun-red` and `rerun-scope-omitted-red`. Its disposition is still `named-residual-uncorrected`, which is honest now that the gate verifies the facts behind it.
- **Still open, for L1:** checks 1–3, 6 and 7 above still apply to the final bytes, with check 2 expecting `SELFTEST: PASS N/N` at the new N. Checks 4 and 5 are now encoded as selftest arms: `extra-blind-key-red` and `tamper-rerun-red`. Re-hash the tool and companion; if either differs from the digests above, re-read before admitting.

## Scope update: Main adopted the producer root fix (appended; earlier text above is kept)
Main decided, on CorrectionCritic's root-cause concern, to fix the mutable producer source. I accept this as valid. The round-13 prompt asks for the null repair through NEW evidence without rewriting the frozen declaration. It does not forbid fixing mutable producer code. This supersedes two earlier lines: "do not edit `tools/bash-witness-study.py:787` this round" (Allowed correction §1), and the `tools/bash-witness-study.py` operand in check 1's `git diff --quiet`. L1 should not expect a zero producer diff.

Observed against the working tree (static only; nothing executed):
- `git diff --stat -- tools/bash-witness-study.py` shows 6 additions and 2 deletions. The live sha256 is `49e9e5e2…ad80`; the historical one is `249d9dcd…` (index blob `874d10e`, commit `9df9212`).
- `build_summary` now reads `"kind": declaration.get("kind")` (`:787`). This is the top-level field that `cmd_declare` writes at `:875`.
- New regression in `cmd_selftest` (about `:1538-1544`): the fixture declaration carries the exact literal `declared-witness mapping (not a blind preregistration)`, and `check("summary preserves top-level exposed declaration kind", qsummary["declaration"]["kind"] == <literal>)` asserts it. If the line is reverted to `declaration.get("declared", {}).get("kind")`, `kind` becomes `None` and the assertion fails, so the regression kills that revert. Exact equality also rejects a blind relabel and a disclosure-derived value. One mutant survives: a hard-coded literal. That mutant still produces the correct value, so this is acceptable.
- `"tool": sha256_file(__file__)` (`:781-782`) is written only into new summaries. Round-12 `cmd_check`/`cmd_count` never compare `summary.tool.sha256` with the live tool, and no live script consumes `selftest.sha256.txt` (grep shows only `manifest.json:70`). Changing the producer therefore does not turn any round-12 check red.
- The companion stays independent of the live producer. `witness-metadata.py` pins the historical `PRODUCER_TOOL_SHA256 = 249d9dcd…` against `summary.json#/tool` with `checked_live: false`, and never hashes `tools/bash-witness-study.py`. A fixed producer leaves C2 unchanged. Both claims also remain true: the companion note says the frozen null came from reading `declared.kind`, and the frozen evidence keeps that historical fact.

Conditions that remain:
1. The frozen round-12 bytes stay unchanged. Check 1's digest table still applies, and `git diff --quiet 546b371 -- .ufo/evidence/round-12` must exit 0.
2. Do not run `bash-witness-study.py run` or `rerun` against `.ufo/evidence/round-12/BashWitness`. The fixed tool would write a non-null `kind` and a new `tool.sha256` into, or beside, frozen evidence.
3. Historical replay of the round-12 selftest or sweep must use `git show 9df9212:tools/bash-witness-study.py` (`249d9dcd…`), not the live file. `selftest.sha256.txt:1` is a historical pin and is now expected to differ from the live tool.
4. Main's LOG and lesson integration should name the producer fix as a mutable-code correction, separate from the companion, and claim no kill-rate change, no new witness and no scalar change.

Additional check for L1, not executed here: `python3 tools/bash-witness-study.py selftest` must stay green and include the new `summary preserves top-level exposed declaration kind` assertion. Optionally, revert line 787 in a temp copy of the tool and confirm that this assertion goes red.
