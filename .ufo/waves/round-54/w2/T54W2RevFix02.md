# T54W2RevFix02 — C1 fix-pass verify (cats 7–12)

Axes: calibration, depth.
Scope: anchor fixes in `### The operator's runbook`, `## Repeated controls and gate registry — round 12`, `## Pin disposition and provenance correction — round 13`, `## Effective expectation reconciliation — round 14` (cited SKILL.md:`:1023-1169`, `:1276-1277`, `:1506`, `:1551`, `:1606`, `:1608`).
Diff: `59c38109bf119d0e9d4f878644a82babc937bc1e` → `99c3bc88d704566197783f66b211ee0a830e0330` on `SKILL.md` (tools/ hunks out of this seat).

## Verdict

One actionable finding (medium): the `:1606` fix correctly binds the 12/13 counts to `.ufo/evidence/round-13/expected.json`, then overstates that "the commands below name" that file. Every other in-scope hunk re-pins cleanly under `sed -n` at C1.

## Findings (by severity)

### M1 — medium — SKILL.md:1606 overstates what the recipe commands name

**Quote (byte-exact at C1):**
`distinguish twelve expected rows from thirteen pinned inputs (both counts belong to `.ufo/evidence/round-13/expected.json`, which the commands below name: twelve expected checks, thirteen inputs).`

**Why:** The counts do belong to `.ufo/evidence/round-13/expected.json` (`expected_checks` len 12, `inputs` len 13 at C1). The relative clause "which the commands below name" does not: the only command argv texts in steps 2–3 are
`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json`
and `.ufo/evidence/round-14/dispositions.json`. Neither argv names `expected.json`. That path appears only as an `inputs` key *inside* those disposition manifests. The fix repaired the missing file bind, then overstated how the recipe commands surface it.

**Command / output:**
```
sed -n '1604,1612p'  # at C1 SKILL.md
# … expected.json only in the parenthetical; commands name dispositions-*.json only
git show 99c3bc88…:.ufo/evidence/round-13/expected.json
# → expected_checks: 12, inputs: 13
git show 99c3bc88…:.ufo/evidence/round-14/dispositions-before.json | inputs keys
# → [expected.json, verification.json, producer-oracle-repair.json]
```
Receipts: `T54W2RevFix02-receipts/overstatement-checks.txt`, `expected-stale-check.txt`.

## Hunk-by-hunk (file:line, severity)

### H1 — SKILL.md:1269 — `:1010-1154` → `:1023-1169` — clean

Negation cite for "no cadence … names [service-limits]". At C1, `## The re-sweep cadence…` opens at 1023; next `##` is 1170; `sed -n '1023,1169p'` contains no `service-limits`. Ledger mates `:285` / `:318` remain ER-3 / ER-4 heads; `sed` on `fleet-kill-rate-ledger.md` 285–360 likewise names no `service-limits`. Severity: none.

### H2 — SKILL.md:1319 — `:1250-1254` → `:1276-1277` — clean

Operator-runbook pointer to the service-limits rendering/divergence rule. C1 `sed -n '1276,1277p'`:
`and the intake-precondition check; this page is the compact rendering, and a divergence between the two is the finding, never smoothed.`
Matches the claim. (C0 `:1250-1254` was the opt-in re-pin paragraph — the bug the fix removes.) Severity: none.

### H3 — SKILL.md:1306–1307 — runbook pin cell — clean

`8b2e185f…` / 516 L / 33 515 B, `committed at 59c38109`. At C1 (and C0):
`sha256sum` = `8b2e185ff011…`, `wc` = 516 lines / 33515 bytes; `git cat-file -e 59c38109:corpus/knowledge/operator-runbook.md` succeeds. Replaces the non-object `e1e349b6…` / 511 L / 31 416 B "uncommitted worktree" pin. Severity: none.

### H4 — SKILL.md:1506 — `corpus/SOURCES.md:500` → `:503` — clean

C1 `sed -n '503p' corpus/SOURCES.md`:
`Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; …)`.
C0 `:500` was "Next unused id: S265…" with no supersession. Severity: none.

### H5 — SKILL.md:1551 — `unchanged` row gains pin-verify conjunct — clean

Observation now requires worktree equality **and** pin verify against the manifest digest, citing `tools/pin-disposition.py:67-71`, `:563-567` (same-file continuation convention, cf. `drift-pins.sh:142-148`, `:252-258`).
- `:67-71` docstring: `unchanged` needs readable regular file + verified pin + byte equality with `expected_sha256`.
- `:563-567` code: `pinned["status"] != "verified"` → `content_status = "unavailable"` / `pin_not_verified`.
No overstatement; no duplicate parenthetical. Severity: none.

### H6 — SKILL.md:1606 — bind 12/13 to `expected.json` — **M1** (see Findings)

Counts calibrate; "which the commands below name" overstates. Severity: medium.

### H7 — SKILL.md:1608 — "moved pins are the round-13 expected manifest's" — clean

Replaces "their pinned inputs moved after round 14". At C1, exactly three of thirteen `expected.json` inputs are digest-stale vs live blobs: `tools/mutate-and-run.sh`, `tools/bash-witness-study.py`, `tools/pin-disposition.py` — the three the sentence names. Both round-14 disposition manifests still list only three inputs and those three digests still match; live `--root` runs of both manifests exit 2 `expected_input_digest_mismatch` (clone receipt). Severity: none.

## Out-of-scope adjacent hunks (noted, not judged)

Refusal-table re-pins at SKILL.md:1282–1286 (`:824-828`, `:851-855`, `:834-836`, `:890-892`) sit in `### The service's limits` and are cats 1–6 (`T54W2RevFix01`). Spot-checked resolving; not counted here.

## Residual risk / verification gaps

- Did not re-run the `git archive 28aeef4` replay that steps 2–3 claim exits 1 then 0; only the live-tree exit-2 half of step 2 was executed. Pre-existing recipe, not introduced by the C1 hunk under test.
- Bare `:563-567` after `tools/pin-disposition.py:67-71` follows the lane's same-file continuation pattern; a reader applying the service-limits "bare `:…` = this page" rule out of section would mis-resolve to unrelated SKILL mutant-probe lines. Convention risk only; intended tool lines hold.

## Artifacts opened / commands run

- `git diff 59c38109… 99c3bc88… -- SKILL.md tools/` → `T54W2RevFix02-receipts/c0-c1.diff`
- `git show 99c3bc88…:SKILL.md` (+ C0 twin); `sed -n` on cited ranges → `anchor-sed-skill.txt`, `sections-full.txt`, `refusal-and-negation.txt`
- `git show …:corpus/SOURCES.md`, `tools/pin-disposition.py`, `corpus/knowledge/operator-runbook.md`, `fleet-kill-rate-ledger.md`, `service-limits.md`, `.ufo/evidence/round-13/expected.json`, round-14 dispositions → `external-anchors.txt`, `pin-disposition-semantics.txt`
- Shared clone at C1: `evidence-disposition.py` on both round-14 manifests → `disp-run.txt`, `disp-before.json`, `disp-after.json`
- Stale-input census → `expected-stale-check.txt`, `r14-inputs-check.txt`
- Overstatement / hunk checklist → `overstatement-checks.txt`, `hunk-checklist.txt`

No lane production files edited. No tooling installs. Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2RevFix02/`.
