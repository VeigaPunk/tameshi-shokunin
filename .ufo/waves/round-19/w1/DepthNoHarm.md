# TameshiR19-2.DepthNoHarm — Report (round 19, w1)

Seat: scout, leaf member (no dispatch). Read-only audit; no production edits; no
lane gate/selftest/monitor/measurement tool executed; no builds, lints, tests or
formatters; no tool installs (none needed). All Git use was read-only
(`show`/`diff`/`grep`/`rev-parse`/`status`/`log`/`cat-file` with `GIT_*` env
stripped); no scratch, no writes outside this Report.

Assigned question: (1) rederive SCORECARD command D recorded case count at the
frozen baseline; (2) audit that the five C1 metadata/receipt corrections cannot
change the eight-leg tool ledger.

## 1. Command D rederived at baseline — OBSERVED

- Baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` =
  "round-18 verifier spot-check (integrator, hyaku): non-author admit/reject",
  protocol-shokunin, 2026-10-21T00:51:38-03:00; its diff touches exactly one
  file (`corpus/lessons/round-18-verifier-spotcheck.md`, +225/−0), so the
  round-18 tip content is contained in the baseline.
- Command D source verified in the baseline blob itself: `# D:` comment at
  `SCORECARD.md:72`, command at `:73` (matches the lesson's `SCORECARD.md:73`).
- Rederivation, exact command-D one-liner over the pinned blob:
  **`recorded_cases=8 depth_score=8`**
- The eight legs (`7243e7f:tools/mutate-and-run.sh:86-93`), every line matching
  command D's regex:

  | # | leg | recorded rate |
  |---|---|---|
  | 1 | js-kimi-census | 8/10 |
  | 2 | bash-surface-census | 8/10 |
  | 3 | bash-tsukuroi-census | 6/10 |
  | 4 | bash-mado-verify | 4/10 |
  | 5 | bash-checklist-run | 7/15 |
  | 6 | js-claims-check | 7/10 |
  | 7 | js-round-gate | 5/10 |
  | 8 | js-sources-check | 5/10 |

  Count 8 = depth 8, equal to round-18's declared value. Numeric stays 8; no
  promotion or new cold-read coverage is claimed or implied.

## 2. What "the eight-leg tool ledger" is — OBSERVED

Two surfaces, both present at baseline:

- **(a) The tool's pinned replay ledger**: the eight recorded case lines at
  `tools/mutate-and-run.sh:86-93`. This is command D's sole input (depth rule:
  "One point per recorded mutation case listed in the tool's pinned replay
  ledger", `SCORECARD.md:66`, baseline blob).
- **(b) The corpus eight-leg kill-rate row**:
  `corpus/knowledge/fleet-kill-rate-ledger.md:432` under
  `## Round 18 — eighth row appended` (`:424`); the section opens
  "Appended; nothing above is edited." (`:426`, blob `7243e7f`, dated
  2026-10-20). The row cites its own inputs: sweep 2026-10-20T19:41:29Z, runner
  `fb6d86d5…`, spec/predictions `93d22aa`, kumitate rev `0acb775`, sha256
  `6a293a72…258f`.

The baseline regression receipt binds (a) to executed evidence: eight
`REGRESSION_TABLE` lines with recorded-killed 8/8/6/4/7/7/5/5, each `flips=0`,
closing `REGRESSION: PASS (cases=8 passed=8; ledger legs exact:
killed-delta<=0 flips<=0)` (`.ufo/evidence/round-18/final/regression.stdout:45`,
blob `7243e7f`).

## 3. C1 correction touch-set audit — OBSERVED

Delivered corrections commit
`21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` ("round-19: correct routed metadata
and retain effective historical receipts", tameshi-shokunin identity,
2026-10-21T02:48:27-03:00). Full numstat `7243e7f`→`21e7932`: 30 files, all
pure additions except `corpus/SOURCES.md` (+9/−1).

Decisive absences (the audit core):

- `tools/mutate-and-run.sh` is **not** in the diff; its Git object id is
  identical at both revisions (`fd1a63a3493b5a2fb2723f2fb1baae9ee7480fba`);
  diff = 0 lines. Command D rederived at `21e7932`:
  **`recorded_cases=8 depth_score=8`** — invariant.
- `corpus/knowledge/fleet-kill-rate-ledger.md` is **not** in the diff;
  diff = 0 lines. The eight-leg row is byte-identical across the corrections.
- **Zero** files under `.ufo/evidence/round-18/`: every original receipt —
  including `final/checks.json`, which retains the mis-invoked
  `bash-witness-selftest` row (argv `tools/bash-witness-study.py --selftest`,
  revision `921ef807…`, exit 64, empty-stdout sha `e3b0c442…`) — is preserved
  byte-for-byte. The repair adds new superseding receipts; it does not rewrite
  history.

Per-defect mapping (round-18 verifier §5 → landed correction at `21e7932`):

| §5 defect | Landed correction | Append-only? |
|---|---|---|
| 1 header PENDING | `corpus/knowledge/guard-kill-closure.md` +21/−0: "Effective verified-at" block plus "R18-1 sweep addendum"; original line-2 PENDING text retained | yes |
| 2 S008 "queued" | `corpus/knowledge/mutation-case-kumitate-sources-check.md` +12/−0: erratum states "The effective source metadata is therefore S008, paper, tier A, mined" and supersedes the stale provenance line | yes |
| 3 four-vs-five cells | `corpus/lessons/round-18.md` +36/−0: `## Erratum R18-3 — falsifier arithmetic (2026-10-21, round 19)` at `:121` (ground truth re-verified: `git diff 183f87b 4b7c682 -- corpus/SOURCES.md` = 25 added, 5 deleted — S001, S008, S052, S056, S057) | yes |
| 4 exit-64 receipt row | new `.ufo/evidence/round-19/bash-witness-selftest-complete.{json,stdout,stderr}` (+22/+45/+0) plus a fresh full `bash-witness-selftest` receipt; `final/checks.json` untouched | yes (supersede, not rewrite) |
| 5 unbacked 4b7c682 claim | new `.ufo/evidence/round-19/round18-final-measure.json`: argv `.ufo/evidence/round-18/measure.py --rev 4b7c682… --explain`, `"revision": "4b7c682…"`, exit 0, stdout sha `55c530bb…`, recorded_at 2026-10-21T05:28:25Z; erratum R18-5 (`round-18.md:148`) states "The fleet report is not rewritten." | yes |

Causal isolation: command D's only input (the tool blob) and the eight-leg
row's cited inputs (sweep receipts, runner, spec `93d22aa`, kumitate
`0acb775`/`6a293a72…258f`) all lie outside the correction touch-set. No
corrected file is read by command D or cited by the ledger row, so no
correction can move either.

Baseline C1 ruler receipt (committed `before.json` at `21e7932`): revision
`7243e7f…`, `corrected: 0`, `open: 5`, rows R18-1…R18-5 all `"open"`, with
input digests (`checks.json` `fed3c8e6…`, `probes.stdout` `d37c99e3…`, and the
three corpus correction files) — consistent with the claimed 0/5 start.
Evidence-verified from the committed JSON; I did not execute the ruler.

Single non-append edit, disclosed: the `corpus/SOURCES.md` −1/+1 replacement is
the S049 row's used-by cell gaining `corpus/lessons/round-19.md`
("S049 stays mined"), disclosed in the appended SOURCES journal entry dated
2026-10-21. SOURCES.md is not an input to command D or to the eight-leg ledger
row, so this edit cannot move either.

## 4. Verdict

- **Baseline recorded case count: 8 (depth 8)** — rederived independently via
  command D on the pinned blob at `7243e7f`.
- **No-harm: HOLDS on observed evidence.** The five C1 metadata corrections,
  as landed at `21e7932`, cannot change the eight-leg tool ledger on either
  surface: the tool blob is byte-identical across the corrections (command D's
  output is therefore invariant at 8), and the eight-leg corpus ledger row is
  untouched (0-line diff). The in-flight SCORECARD round-19 sentence "tool
  bytes and eight-leg mutation ledger are unchanged" is consistent with this
  independent diff evidence.

## 5. Unknowns / boundary

- L1 work is still in flight: `LOG.md` (+40), `SCORECARD.md` (+39) and
  `corpus/lessons/round-19.md` (+86) are modified-uncommitted vs
  HEAD=`21e7932`, and several `.ufo/evidence/round-19/` files
  (`after-21e7932.json`, `contract.json`, `frozen-runs.json`, `coldread/`,
  `current-ledger-monitor-21e7932.json`, `source-count-before.json`) are
  untracked. My invariance statement is pinned to `7243e7f`→`21e7932`; a later
  commit could in principle touch `tools/` or the ledger, and this audit does
  not cover commits after `21e7932`.
- `before.json` open=5 and `after-21e7932.json` corrected=5 are L1's ruler
  outputs; I verified the committed `before.json` content but did not execute
  the ruler (lane-tool execution out of my scope). The `after` receipt's
  content was not audited by this seat.
- The 18 guard survivors and P08/P11 breadth canaries remain open (restated in
  the appended `guard-kill-closure.md` correction text); nothing here closes
  them, and no claim beyond C1's defect-count unit is made.

Tool installs: none.
