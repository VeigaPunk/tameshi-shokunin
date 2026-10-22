# C2Rounding: ledger percentages vs official float scores

Lane: TameshiR25.C2Rounding (leaf reviewer, no dispatch). Item: compare the integer percentages at `tools/mutate-and-run.sh:84-96` with the official float scores, and list any ledger line or SKILL.md / knowledge statement that is wrong under exact arithmetic.

## Verdict

- No ledger integer at `tools/mutate-and-run.sh:86-93` is wrong under nearest-integer rounding. Seven of the eight are exact. The eighth, `7/15 → 47 %`, is the nearest integer to the exact 46.67 %.
- The runner's integer formula is exactly round-half-up of 100·k/n. Exhaustive check over 1 ≤ n ≤ 1000 and 0 ≤ k ≤ n: 0 mismatches.
- Under exact arithmetic, six statements write 7/15 as "= 47 %", which is false as an equality (46.67 %). Further rounded labels, in parentheses or prose, are listed in F3.
- One real defect: the DEGRADED headline `kill-rate=` (`tools/mutate-and-run.sh:562`) uses all defects as the denominator. SKILL.md:210 defines the rate as killed/(killed+survived). Reproduced: the tool prints 33 % where the documented rate is 50 % (F1). No ledger line is affected today because all eight legs have inconclusive=0.
- Two latent rounding issues do not touch the eight current legs: an informational float half-up in the interop tool (F4) and band edges read from printed integers (F5).

Snapshot tags used: `tools/mutate-and-run.sh` #5E81 (unchanged during review), `SKILL.md` #07B4, `tools/mte-interop.py` #EF9A. The interop file changed during the review (#7570 → #EF9A, a four-check judge plus a `runner_pct` / `official_rounded_half_up` line). Findings cite #EF9A. Re-read before the final check.

## 1. Ledger lines vs exact and official values

Official float = `mutationScore` from the vendored `mutation-testing-metrics` 3.9.0 (`package/src/calculateMetrics.ts:253`: `(totalDetected / totalValid) * 100`, unrounded). I ran `calculateMetrics` on synthetic K/S reports with the same packages and call that `NODE_RUNNER` uses (`tools/mte-interop.py:79-90`), in `/tmp/c2rounding-scratch/run` (node v24.21.0). Command: `node legs.mjs`.

| Line | Leg | Ledger k/n → printed | Exact | Official float | Half-up | Reading |
|---|---|---|---|---|---|---|
| 86 | js-kimi-census | 8/10 → 80 | 80 | 80 | 80 | exact |
| 87 | bash-surface-census | 8/10 → 80 | 80 | 80 | 80 | exact |
| 88 | bash-tsukuroi-census | 6/10 → 60 | 60 | 60 | 60 | exact |
| 89 | bash-mado-verify | 4/10 → 40 | 40 | 40 | 40 | exact |
| 90 | bash-checklist-run | 7/15 → 47 | 46.6667 | 46.666666666666664 | 47 | nearest integer; printed value is 0.33 pp above exact |
| 91 | js-claims-check | 7/10 → 70 | 70 | 70 | 70 | exact |
| 92 | js-round-gate | 5/10 → 50 | 50 | 50 | 50 | exact |
| 93 | js-sources-check | 5/10 → 50 | 50 | 50 | 50 | exact |

Other checks on the same lines:
- The embedded `TABLE_*` verdict tables (`tools/mutate-and-run.sh:613-620`) parse to the same numerator and denominator for all eight legs. Example: `TABLE_CHECKLIST` has 15 entries, 7 KILLED, 8 SURVIVED.
- The vendored tarballs match their pins at `tools/mte-interop.py:63-66`. Both sha512 integrity strings match.
- The official float is not 46.67. The tool never prints 46.67. The interop judge prints the raw value (`official_score=46.666666666666664`, `tools/mte-interop.py:252-257`). The 2-decimal figure appears only in the docstring example at `tools/mte-interop.py:32`.
- The regression gate compares counts, not percentages. `tools/mutate-and-run.sh:1235-1257` uses `exp_killed` and the measured kill count. `tools/mte-interop.py:243-247` uses the `REGRESSION_TABLE` counts. Integer rounding cannot flip a leg.

## 2. Findings (severity order)

### F1 — medium — DEGRADED headline kill-rate contradicts the documented denominator

Evidence:
- `tools/mutate-and-run.sh:498-499`: `total` is the number of defect rows, including inconclusive ones.
- `tools/mutate-and-run.sh:562`: `pct=$(( (200 * killed + total) / (2 * total) ))`.
- `tools/mutate-and-run.sh:564-565`: the DEGRADED line prints that `pct`.
- SKILL.md:210-211: "Kill rate = killed / (killed + survived) — inconclusive runs are excluded from the denominator".
- `corpus/knowledge/mutation-score-semantics.md:10` and `:23`: Tameshi's rate uses only Killed and Survived.
- `tools/mte-interop.py:235` and `:240-241` use killed/(killed+survived), so the interop side agrees with SKILL and the runner's DEGRADED line does not.

Reproduction (copy of the tool in `/tmp/c2rounding-scratch/degraded/`, three defects: one killed, one survived, one suite exit 127). Observed:

```
MUTATE: DEGRADED (target=degraded-fixture defects=3 killed=1 survived=1 inconclusive=1 kill-rate=33%)
```

The documented rate is 1/(1+1) = 50 %. By the same printed formula, killed=1 survived=0 inconclusive=1 gives 50 % where the documented rate is 100 %, and killed=0 survived=0 inconclusive=2 gives `kill-rate=0%` where the documented rate is undefined. Those two cases were checked by hand, not run.

Selftest gap: `tools/mutate-and-run.sh:1538` expects `killed=0 survived=1 inconclusive=1 kill-rate=0%`. Under either denominator that is 0, so the arm cannot distinguish them.

Ledger impact: none. All eight legs have inconclusive=0, and the DONE path (`:568-569`) has total = killed+survived, which matches SKILL.

Smallest safe correction (sketch; not applied): in the sweep summary, set `valid=$((killed + survived))`. If `valid` is 0, print `kill-rate=n/a`; otherwise `pct=$(( (200 * killed + valid) / (2 * valid) ))`. Add a selftest arm `killed=1 survived=0 inconclusive=1` expecting `kill-rate=100%`. The DONE values and the `:1538` arm are unchanged by this. Alternatively, if the defects denominator is intended, amend SKILL.md:210-211 and `mutation-score-semantics.md:10,23`. Both readings cannot stand.

### F2 — low — "7/15 = 47 %" is false as an equality (exact 46.67 %)

Equality form:
- `tools/mutate-and-run.sh:586`: "7/15 = 47 % at :130-131" (comment).
- SKILL.md:1103: "| 5 | kagi `corpus/checklist-run.sh` (T8-1) | … | 7/15 = 47 % · 7 kill + 8 hole |".
- SKILL.md:1316: "| 5 | `bash-checklist-run` | … | 7/15 = 47 % |".
- `corpus/knowledge/closeout-r11.md:108`: "7/15 = 47 % · 7 kill + 8 hole".
- `corpus/knowledge/operator-runbook.md:153`: "7/15 = 47 % · 7 kill + 8 hole".
- `corpus/knowledge/mutation-case-kagi-checklist.md:211`: "47 % = 7 kill-aimed (7/7) + 8 hole-aimed (0/8)".

Correct forms already in the corpus: `corpus/knowledge/mutation-case-kagi-checklist.md:131` ("7/15 = 46.7 %, printed 47 %") and `corpus/knowledge/mutation-score-semantics.md:41` ("7/15=46.666…%").

Smallest correction: write "≈ 47 %" or "46.67 % (printed 47 %)". The corpus is append-only for receipts (`corpus/QUALITY.md:150-152`, criterion 26: "the original line is never rewritten"), so the knowledge-file fixes should be dated appended errata. The comment at `tools/mutate-and-run.sh:586` may be edited by the tool owner.

### F3 — low — parenthetical "(47 %)" labels are rounded labels

Correct under the nearest-integer convention, not exact:
- `tools/mutate-and-run.sh:90`: "7/15 (47 %)" (ledger line itself).
- `corpus/README.md:51`: "7/15 (47 %)".
- `corpus/knowledge/fleet-kill-rate-ledger.md:276`: "7/15 (47 %)"; `:279`: "47 % (kagi checklist r8)".
- `corpus/knowledge/incremental-pin-disposition.md:162`: "7/15 (47 %)".
- `corpus/knowledge/mutation-case-kagi-checklist.md:225`: "7/15 (47%)".
- SKILL.md:1145: "40 / 47 / 60 / 70 / 80 / 80".
- `LOG.md:307`, `SCORECARD.md:21` ("47%"), `SCORECARD.md:49` and `corpus/knowledge/closeout-r11.md:52` ("47 % · 70 %").

Smallest correction: state the convention once. It already appears in `tools/mte-interop.py:31-32`. No per-line edit is needed.

### F4 — low, latent — informational half-up in the interop tool uses a float

`tools/mte-interop.py:320-322`: `int(score + 0.5)`, where score = `(totalDetected / totalValid) * 100`. Exhaustive check, 1 ≤ n ≤ 1000: 40 (k, n) pairs disagree with the runner's exact half-up. All 40 are exact .5 ties, and all have n a multiple of 40. Example: 23/40. Exact 57.5, runner prints 58, float 57.49999999999999, interop prints `official_rounded_half_up=57`.

Today's eight legs have n = 10 or 15 and no exact ties, so the printed lines agree. The line is information only. `judge()` (`:230-258`) does not use it. Smallest correction: compute from integer counts, `(200*killed + valid) // (2*valid)`, or with `fractions.Fraction`.

### F5 — low, latent — band reading from the printed integer

The runner prints integers (`:562`). The bands (SKILL.md:329-331) are >80 %, 50-80 %, <50 %. The printed integer can cross an edge:
- 80 edge: exact in (80, 80.5) prints 80. 33/41 = 80.49 % prints 80. For n ≤ 200 there are 80 such pairs; the smallest n is 41.
- 50 edge: exact in [49.5, 50) prints 50. 50/101 = 49.50 % prints 50. For n ≤ 200 there are 51 such pairs; the smallest n is 101.

No ledger leg is affected (n = 10, 15). Smallest correction: an appended note at SKILL.md:314-340 that bands are read from the exact k/n, not the printed integer.

### F6 — nit — stale pointers

- `tools/mutate-and-run.sh:582`: "kill-rate 60 % at :69-70". The 60 % sits at `corpus/knowledge/mutation-case-tsukuroi-census.md:68`.
- `tools/mutate-and-run.sh:584`: "kill-rate 40 % at :61-62". The 40 % sits at `corpus/knowledge/mutation-case-mado-verify.md:60`; the tool line quoting `kill-rate=40%` is at `:62`.
- `corpus/knowledge/mutation-score-semantics.md:53`: "recorded six-leg ledger … (tools/mutate-and-run.sh:84-92)". The ledger now lists eight legs at `:86-93`.

## 3. Verified correct (coverage record)

- Tool formula: `(200k+n)//(2n)` equals `floor(100k/n + 1/2)` for all 1 ≤ n ≤ 1000, 0 ≤ k ≤ n. Zero mismatches.
- Identity at `corpus/knowledge/mutation-score-semantics.md:25-27`: (k+t)/(k+s+t) − k/(k+s) = ts / ((k+s+t)(k+s)). Checked algebraically. The equality cases at `:29` (t=0 or s=0) follow from it.
- Percent sweep: 128 k/n-then-percent pairs in 85 files (SKILL.md, LOG.md, SCORECARD.md, README.md, corpus/**, tools/mutate-and-run.sh, tools/mte-interop.py). 18 were flagged at |exact − printed| ≥ 0.005, and each was triaged:
  - Regex artefacts, correct on reading: LOG.md:126 (band text); SKILL.md:588; `corpus/knowledge/mutation-case-kumitate-sources-check.md:189`; `corpus/knowledge/self-hardening-r6.md:51,173`; `corpus/lessons/round-18-verifier-spotcheck.md:77`.
  - Correct at one decimal: `corpus/knowledge/mutation-case-kagi-checklist.md:131` (46.7); `corpus/knowledge/service-optin-protocol.md:157` (13/23 = 56.5 %, printed 57 % by the tool formula).
  - Rounded equality: F2 list minus `:211`.
  - Rounded label: F3 items at `corpus/README.md:51`, `fleet-kill-rate-ledger.md:276`, `incremental-pin-disposition.md:162`, `mutation-case-kagi-checklist.md:225`, `tools/mutate-and-run.sh:90`.
- All other k/n-percent statements match their exact values. Examples: 80, 60, 40, 70, 50, 100 %; 13/23 printed 57; 10/10 mado hardened = 100 %; `8/15` at `corpus/knowledge/fleet-suite-census.md:498,601` (owner's 15-defect run, killed 8 / survived 7 at `:489-490`) with the 40 % at `:602` read as "first below the 50–80 % band", which is correct.

## 4. Verification run, gaps, tooling

Ran (all in `/tmp/c2rounding-scratch`, nothing written in the repo):
- `node legs.mjs` (official float for eight legs).
- Python exhaustive checks (formula identity, float-vs-integer, band edges, TABLE_* counts, pin sha512).
- Copy of `mutate-and-run.sh` in `/tmp/c2rounding-scratch/degraded/` with a three-defect fixture (produced the DEGRADED line in F1).

Not run:
- `tools/mte-interop.py --check`. It runs the regression sweep, so the main agent should run it once after edits settle. Expected rounding lines: `runner_pct=N official_rounded_half_up=N` with N equal to 80, 80, 60, 40, 47, 70, 50, 50.
- `tools/mte-interop.py --selftest`. It needs python `jsonschema`, which is not installed here.

Tooling: none installed or upgraded by this lane. Host node v24.21.0 and python3 standard library were used as present.
