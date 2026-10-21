# RowAudit07 — five-row replay audit (round24 C1)

**Verdict: no false acceptance found for the five assigned rows.** Requirement snapshots,
receipts, observations `runner_result` (exit, full stdout, held) and stdout tokens all
agree exactly, and `held` recomputes true from the committed requirement+receipt pair.
Two rows carry under-pinned expectation tokens (FA-1) and one carries an exit-only pin
(FA-2); those are binding-sufficiency gaps a future regression could exploit, not
defects of this replay. One structural limit (FA-N) is unavoidable in this evidence set.

Rows: `pin-disposition-selftest`, `context-capture-mapping-suffix`, `sources-census`,
`defect-probes-selftest`, `round21-measure-selftest`.
Replayed revision `d2eaecd443bf5f4e387e7e5331282e3d11dea047`; delivered revision `c8c5b88c8e961a929cdc351b95a7074c76958909` (d2eaecd is an ancestor; the five tools/inputs
are byte-identical across the gap — see Evidence 4).

## Row table (observed)

| row | req == round23 requirements.json | live registry row == round23 baseline | receipt exit / obs got | receipt stdout == obs stdout | needles found | recomputed held == reported |
|---|---|---|---|---|---|---|
| pin-disposition-selftest | yes | yes | 0 / 0 | identical, 1409 B | `SELFTEST: PASS` ×1 | true / true |
| context-capture-mapping-suffix | yes | yes | 1 / 1 | identical, 924 B | none (exit-only) | true / true |
| sources-census | yes | yes | 0 / 0 | identical, 1863 B | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` ×1 | true / true |
| defect-probes-selftest | yes | yes | 0 / 0 | identical, 516 B | `SELFTEST: PASS` ×1 | true / true |
| round21-measure-selftest | yes | yes | 0 / 0 | identical, 461 B | `ROUND21_MEASURE_SELFTEST: 13/13 pass` ×1 | true / true |

All five: `stderr == ""` on both sides; `stdout == stdout_tail` (streams ≤ 4096 B, so the
retained stream is the full stream, no `TAIL_BYTES` truncation); `kind`, `status`, `tags`
match the registry row; `elapsed_s < timeout_s`; per-row `revision` equals
`observations.revision`; every row interval is inside the global measurement interval.

## Evidence

1. **Requirement identity.** `observations.json` row `requirement` objects are deep-equal
   to the corresponding `requirements.json` entries (all 43 rows; 43 unique names, no
   duplicates, no omissions). `requirements.json` is exactly the active-row projection of
   `registry-baseline.json` whose sha256 is `ebd2e69a…fec92a`, the value recorded in both
   `requirements.json` and `observations.registry_sha256`. Live `tools/registry.json` rows
   for the five are identical to the baseline in `kind/argv/expect/timeout_s/status/tags`
   (no drift, no supersession; the five appear at `tools/registry.json:132,397,571,762,875`).
   Requirement source anchors resolve to the right entries (`SKILL.md@98bea7d:1552`,
   `SKILL.md@98bea7d:1680`, `SCORECARD.md@98bea7d:240`, `SKILL.md@58e5d53:1923-1932`,
   `SKILL.md@370f2df…:1977`).

2. **Receipt vs observations.** `bundle.json` receipts are byte-identical to
   `observations.runner_result` for exit/stdout/stderr on all five
   (`observations.json:334-379, 724-768, 1084-1127, 1437-1480, 1789-1832`;
   `bundle.json:95,218,324,429,…`). Recomputing the runner predicate
   `got == expect.exit and all(needle in stdout) and cleanup_ok`
   (`tools/registry-check.py:719-720`) reproduces `held: true` for all five, with
   `cleanup_error`/`non_hermetic_argv`/`stdout_missing` absent.

3. **Tokens are verdict-backed, not opportunistic.** Each producing tool prints its needle
   only on the all-pass branch: `tools/pin-disposition.py:1323-1329` (FAIL branch returns 1),
   `.ufo/evidence/round-18/defect-probes.py:1013-1018`, `tools/round21-measure.py:132-134`
   (`passed == len(checks)` else exit 1), and `sources-census-v2.sh:20` (`CLEAN` only when
   `bad=0`). Internal counts agree with the verdicts: 19 `SELFTEST_CASE` lines vs
   `PASS (19/19)`; 6 case lines vs `PASS (6 cases)`; 13 `MEASURE_CASE` lines vs
   `13/13 pass`; 2 `FINDING` lines vs `findings=2`; 25 `no-id-cite` lines vs `count=25`.

4. **Receipts transfer to the delivered revision.** At `d2eaecd` and `c8c5b88` the five
   executables and their inputs hash identically: `pin-disposition.py 331529ea…`,
   `context-capture.py c4a1d165…`, `sources-census-v2.sh b9b75471…`,
   `defect-probes.py 99297d96…`, `round21-measure.py eda5490a…`, `registry-check.py cba16646…`
   (= `observations.runner_sha256_clone_copy`), `registry-replay.py 9fcd2dbb…`
   (= replay-command `instrument_sha256`), `command-binding.py 9230c68e…`
   (= replay-gate `tool_sha256`). `git diff --name-only d2eaecd…HEAD` is 26 files:
   25 under `.ufo/evidence/round-24/` plus `.ufo/evidence/round-21/coldread/ledger.json`;
   `corpus/` and `SOURCES.md` are untouched, and none of the five rows reads the round-21
   coldread ledger (`round21-measure.py:22-23` reads only `c1-survivors.py`, `c2-count.py`
   and `c2-contract.json` from `.ufo/evidence/round-21`). In particular, all
   40 unique used-by paths of the 54 `mined` SOURCES rows exist at HEAD and none changed
   after the replay revision, and recomputing HEAD census counts matches the receipt exactly:
   `rows=83`, `tiers A=74 B=7 C=2`, `status mined=54 queued=23 rejected=6`, `malformed=0`.

5. **Gate and replay records.** `replay-command.json` exit 0; its progress stream has 43
   `name got held` lines (plus the final JSON report) and includes
   `pin-disposition-selftest 0 True`, `context-capture-mapping-suffix 1 True`,
   `sources-census 0 True`, `defect-probes-selftest 0 True`, `round21-measure-selftest 0 True`.
   `replay-gate.json` exit 0 with
   `{"bundle_sha256":"4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6","exit":0,"finding_ids":[]}`;
   `sha256sum bundle.json` = `4f424023…a9c6`, so the committed expected pin matches.
   `live-dependent.json` does not list any of the five (`revision_pinned: 41`).

6. **Negative-control authenticity.** The mapping-suffix fixture really encodes the defect:
   `receipt.json` leg `js-kimi-census` carries `declared_variable_suffix: "BASH"` while the
   tool's canonical map says `"js-kimi-census": "JS"` (`tools/context-capture.py:171`); the
   receipt's stored checks/`match`/`all_match` are `true` and stored verdict is `ok/0`, so
   the recomputed mismatch is genuine. `sha256(receipt.json)` at HEAD =
   `02204ef81bd63268eda1c00d98b68a6e5ad9795399c266e57b18f4f8cc58fe5e`, exactly the sha the
   run printed, and `expected.json` pins `id=mapping_mismatch, exit=1` for that sha. The
   observed findings are exactly `mapping_mismatch` + `receipt_verdict_mismatch`; no
   `expected_verdict_mismatch` finding appears, i.e. the primary id matched its pin.

## False acceptance flags

- **None in this replay.** No row is `held` on a missing/extra token, wrong exit, truncated
  stream, cleanup error, non-hermetic argv, duplicate name, or stale requirement.
- **FA-1 (medium, under-pinned token) — `pin-disposition-selftest`, `defect-probes-selftest`.**
  Both requirements pin only the literal `SELFTEST: PASS`. Both tools emit that token from a
  computed total, so a gutted suite still satisfies the row. Concrete counterexample
  [INFERENCE from `tools/pin-disposition.py:1323-1329` and
  `.ufo/evidence/round-18/defect-probes.py:1013-1018`]: delete every `case(...)`/`record(...)`
  call; the tools then print `SELFTEST: PASS (0/0)` / `SELFTEST: PASS (0 cases)` and exit 0,
  and the registry row still holds. `round21-measure-selftest` already demonstrates the
  stricter form: its `13/13` needle rejects `0/0`, and a dropped case makes it `12/12`, which
  also fails the needle.
- **FA-2 (medium, exit-only pin) — `context-capture-mapping-suffix`.** The requirement pins
  `exit: 1` with no stdout token. Any exit-1 finding set is accepted; only exit 2 is
  could-not-evaluate (`tools/context-capture.py:93-100`). Concrete counterexample [INFERENCE]:
  a checker regression that reports a different exit-1 finding on this same fixture — the
  sibling row's `missing_injected_environment` shape at `observations.json:701` is an
  observed example of that finding class — would still hold while suffix detection is gone.
  The fixture's `expected.json` pin would add a secondary `expected_verdict_mismatch`, but the
  registry requirement does not look at stdout, so `held` stays true.
- **FA-3 (low, no row-count floor) — `sources-census`.** The token proves internal
  consistency, not that the registry still has its rows; a single still-consistent mined row
  would print `CLEAN` and exit 0 [INFERENCE from `sources-census-v2.sh:10-20`]. Not trivially
  vacuous: with zero mined rows `pairs` is
  empty and the B2 loop emits a bogus `no-id-or-path-cite` line, forcing `bad=1` →
  `VIOLATIONS` (fail-closed), and with a missing `SOURCES.md` the empty `m` also forces
  `bad=1`. The present receipt is non-vacuous: `A rows 83`, and the HEAD recount matches it.
- **FA-N (structural, not a row defect).** `bundle.json` receipts are derived from
  `observations.json` by `project()` (`tools/registry-replay.py:96-104`), so “receipt vs
  observations” is a consistency check, not an independent observation; the tool docstring
  already says it authenticates no producer. The executing clone
  `/tmp/tameshi-registry-replay-dzo3ypiq` no longer exists, so independent re-execution is
  impossible from this evidence set. The replay revision is also an ancestor of, not equal
  to, the delivered revision; transfer is argued from byte-identical tools/inputs plus
  unchanged corpus (Evidence 4), not from a re-run.

## Smallest safe correction

1. Tighten the two selftest rows in `tools/registry.json` (and regenerate the frozen
   requirements for the next replay) to the full verdict line:
   `"SELFTEST: PASS (19/19)"` for `pin-disposition-selftest`, `"SELFTEST: PASS (6 cases)"`
   for `defect-probes-selftest`. Accept the intended churn: adding a case requires updating
   the pin, exactly as `round21-measure-selftest` already behaves.
2. Add a finding needle to `context-capture-mapping-suffix`:
   `"declared_variable_suffix 'BASH' is not the canonical 'JS'"` (present in the observed
   line), so the row proves *which* defect was detected rather than only that exit 1 occurred.
3. Optional: give `sources-census-v2.sh` a row-count floor (fail when `A rows` falls below the
   contract baseline), since the registry token cannot express completeness; otherwise record
   the row as a consistency gate, not a completeness gate.

## Confidence and unknowns

- High confidence on the three assigned axes: the equality checks are mechanical and the
  provenance chain (registry-baseline sha → requirements → runner copy sha → gate tool sha →
  bundle sha) is complete.
- FA-1/FA-2/FA-3 are labelled [INFERENCE] because they were derived from the committed
  branch logic; I did not execute the battery, gates, or selftests in the lane per lane bounds.
- Unknown/unreachable: independent execution proof (clone deleted); behaviour of the rows at
  the delivered revision beyond the byte-identity argument above.
- No tools were installed or updated during this audit.
