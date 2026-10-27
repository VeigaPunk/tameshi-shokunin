# Round 44 non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25

## Conformance

- Report authorship: `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-44/tameshi.md` → `tameshi-shokunin 6fd519c4b670f433cdb3733491eb69a1dffc8fa0`; lane identity, landed report. Not a marker: claims, before/after measurements, evidence pointers, and lane commits present.
- `## SHONEN` heading present with one line per box (4 lines, all `[~]` with resolvable pointers).
- Cited lane commits exist and are ancestors of `master`: base `506e99c7b73c85711f066895984d501fcf7539cd`; freeze `ba01973c73ad7de60e5bd19ae08255a1b7ef917e`; landed `df000ab79a4c526bcb5cbf03a356c1a44fb32e27`; intermediates `05b3bd2`, `8bffd9b`, `315453b`, `83beaf9`, `ef990aa`, `2240848` — all `git cat-file -e` EXISTS and `git merge-base --is-ancestor <h> master` ANCESTOR.
- Lane state: `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state` → `local=remote=df000ab79a4c526bcb5cbf03a356c1a44fb32e27 ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `df000ab79a4c526bcb5cbf03a356c1a44fb32e27`. Pushed, no uncommitted round work.
- Prompt contract: dispatched `.ufo/prompts/tameshi-round-44.md` embeds the round contract and the five child-lane items (report path/filename, commit-before-report ordering, `SHONEN` heading requirement, commit-hash citation rule, write scope) against `templates/round-prompt.md` markers; L2 route via host route table, no `model` passed.
- Watchdog digest matches: `launch tameshi round=44 pgid=1996094 driver=hyaku-inline attempt=1` (09:56:14-03) and `complete tameshi round=44; hyaku-inline attempt=1` (10:22:16-03); no `lane-dead-no-report` line for round 44.

## Claims — re-check

### C1 (calibration, lowest non-retired axis)

Frozen contract `.ufo/evidence/round-44/contract.json` at `ba01973c…` (byte-identical at freeze; `amendments: []`); counter `.ufo/evidence/round-44/calibration/measure.py` sha256 at freeze and at HEAD = `c0c6199fd6172df69326834eaad4884a27427fdd84cf79404dd5b1f44bd9c0d6` = contract pin. Gate not executed (PROTOCOL §Gate standard — closure verifies committed evidence).

- Before (receipt `before/c2-old-at-base.stdout`): round-43 counter at base `506e99c…` → `C2_R43: … m7=1 … total=1 … C2_R43_PASS=false first=m7:SCORECARD.md#round-43_unknown_S256`. Round-44 counter at base → `m7=0 m12=1 total=1 C2_R44_PASS=false` (`before/c2-new-at-base.stdout`). Falsifies the reported before-states as written.
- After: receipt `after/c1-at-ef990aa.stdout` → `C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 … rev=ef990aaea3f6546db20feccbff89ac9ab78c5405 freeze=ba01973c… C2_R44_PASS=true`; the report's final-tip run at `df000ab79…` prints the same PASS string. Target sentence `C2_R44_PASS=true: self_pin=1 classes=7 m6=0 … total=0` is reproduced byte-exact in the receipt.
- Control (frozen `do_nothing_control`): `control/mask-removed.selftest.stdout` → `C2_R44_SELFTEST: cases=16 failed=2`, `FAIL T6_safe_floor_value_not_citation ['r unknown S256']`, `FAIL T6_assign_with_spaces_masked ['r unknown S256']`, `VERDICT: FAIL`, exit 1. Shows the assignment-mask is exactly what resolves the false `S256` citation.
- Selftest audit `w1/RevSelftestAudit.md`: baseline `cases=16 failed=0` PASS; every one of the 16 cases has a failing one-line mutation (zero vacuity), including `T6_genuine_unknown_still_flagged` and `T6_unmined_flagged` (deadening the unknown/unmined branches fails the suite) — the suite genuinely asserts genuine unknown and unmined citations still flag.
- **Ruling on the L1-flagged wording gap:** the frozen C1 *statement* is wider than the printed `C2_R44_PASS` label, but the frozen *target* sentence equals the counter predicate and the label exactly, and the statement's mechanism clause (assignment-bound S-id is a value, not a citation; genuine unknown/unmined still flag) is established by the frozen control receipt and the selftest audit as committed evidence. The measured counter, together with that committed side-evidence, satisfies the frozen claim as written; no predicate changed after data.
- Verdict: **calibration improved** (receipts verified; gate evidence-verified, not executed). The mis `m7` false alarm is removed (`m7=0`) and all seven classes are zero at the deciding revision.

### C2 (freshness)

Re-measured by the integrator over committed bytes:

- `git show 506e99c7:corpus/SOURCES.md | grep -cE '^ {0,3}\| S160 '` → 0 (exit 1); `git show df000ab79a4c526bcb5cbf03a356c1a44fb32e27:corpus/SOURCES.md | grep -cE '^ {0,3}\| S160 '` → 1 (exit 0). Rows 114 → 115.
- S089 row byte-identical base vs after (status/recheck/anchor/used-by unchanged).
- S160 row (`corpus/SOURCES.md:130`): `mined`, opened 2026-10-25, recheck 180d, `used-by` `corpus/knowledge/r44-anchor-refresh-rule.md`; snapshot `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html` = 38687 bytes, sha256 `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`.
- Live re-open (2026-10-25, `curl -fsSL`): 38687 bytes, sha256 identical to the snapshot → the pinned snapshot is current; S089's old digest `bc572676…` is stale, so the supersession premise holds.
- Located quotes in snapshot: line 16 “There is no definitive way for Stryker to find and ignore them.” (12 words); line 17 “the only solution is by finding these by hand” (9 words); the `10 ** 0` example is at line 15 (split by inline tags; token count ~28/24 letter-digit words vs the lesson's stated 20 — see routed defect).
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, 115 rows, warnings exactly as reported (W04 ×9 incl. S160, W01 S101), no E-codes.
- Verdict: **freshness improved** (re-measured).

### No-harm

- `git diff 506e99c7 df000ab79 -- SCORECARD.md`: 28 insertions, 0 deletions (append-only round-44 section).
- Command D (depth) receipts: `recorded_cases=9 depth_score=9` at base and at `ef990aa`, exit 0 both.
- Coldread monitor receipts: `calibration_restraint_score=6`, `sections_covered=60/64` at base `506e99c…` and at `ef990aa…`; `depth_score=9` both. Depth and calibration numeric scores unchanged. Freshness axis newly tracked with a narrow document-scoped 0→1 unit (not a universal claim) — an addition, not harm.

## Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | improved | C1 frozen target reproduced in deciding receipt; false m7 removed; mask control + selftest audit evidence-verified |
| freshness | improved | C2 re-measured 0→1; S089 unchanged; snapshot live-verified; census exit 0 |
| depth | unchanged | command D 9→9 |
| operability | unchanged | no tool change claimed |
| coverage | unchanged | no new coverage-map ground |
| adjacency | unchanged | no contested scope reported |

The false `m7` alarm on the historical assignment is removed (`m7=0`) and all seven classes are zero at the deciding revision.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| Admit S160 (new row, Stryker equivalent mutants) | admit | live https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ (byte-identical to committed snapshot, sha256 `79f6501a…`) | agree | Snapshot is current; located quotes at lines 16–17 found verbatim; the row's grounding quote (12 words) is ≤25. Lesson's first quote word-count label (20) understates token count (~28/24) — cosmetic, not admission-relevant |
| Reject staged S160 (package) | reject | `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:14` — staged S160 is PIT FAQ (`pitest.org/faq/`) | agree | Staged S160 is the PIT FAQ already held as lane S156; refusing it as an adoption (collision) is correct. Lane S160 is a separate Stryker document, not a re-label |
| Re-open S089 (held, no in-place edit) | re-open | same live URL | agree | Live page equals the new snapshot digest, not S089's pinned `bc572676…`; append-only supersede via S160 is the correct repair |

## Trends

- **expansion: unchanged** — S160 is an anchor-refresh correction on already-held ground; no frontier row moved, no new coverage-map ground; assimilation none.
- **quality: improved** — the stale S089 anchor is superseded by a fresh, live-verified snapshot row, with no admitted entry failing its recheck; S089 preserved as history.
- **discernment: unchanged** — the lane made no self-assessed improvement claim; the outside spot-check agrees with the sample admit and reject, so no disagreement was left unlearned.

## Routed defects for round 45

- Cosmetic: `corpus/lessons/round-44.md` Gate's first located quote is labeled “20 words”; it tokenizes to ~28 (24 letter/digit words). The row's grounding quote (12 words) is compliant, so no bar is violated; correct the label in a future round (append-only).
- Observation (not a defect): wave shape was one v1 wave of 32 seats with 14 attack-role seats; no wave 2 or residual call because the distinct fresh attack inventory was below 32 and none remained unassigned, as reported in `w1/summary.md`.
