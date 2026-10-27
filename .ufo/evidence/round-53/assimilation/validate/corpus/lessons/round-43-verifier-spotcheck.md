# Round 43 non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25

## Conformance

- Report authorship: `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-43/tameshi.md` → `tameshi-shokunin d414598824c3f09040665b601cafde247467aca1`; lane identity and landed report.
- Report has `## SHONEN` and four `[~]` checklist lines. It is real work, not a marker: claims, measurements, evidence pointers, and lane commit are present.
- Lane cited commits exist and are ancestors of `master`: base `487b8f0da89fa0e2b8bea6930068accbf36e70a9`; measurement `3c4003f6e97e5c787e7538b2eb35d62f49783aaf`; freeze `6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`; landing `718a1e987febd32eb78ebc65adfe939f23b3de63`; and all intermediate hashes listed in report §Landed changes. Checked with `git cat-file -e <hash>^{commit}` and `git merge-base --is-ancestor <hash> master`.
- Prompt carries the round contract and report/SHONEN/write-scope contract (dispatched prompt §1–6). HEAD is detached but helper state resolves branch `master`, local/remote both `718a1e987febd32eb78ebc65adfe939f23b3de63`, `ahead=0`.
- **Conformance defect, status-neutral:** `git status --porcelain` shows a modified committed wave-1 reviewer note, `.ufo/waves/round-43/w1/RevC2Classes.md`, not round code. Its diff updates A13 pin/line references; it is not clean. Route to lane for round 44 to reconcile/remove the accidental worktree edit.
- Source census validation was run at closure: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → `tameshi ok`, with the same W04 duplicate-source warnings and W01 tier-C warning disclosed in round evidence; no E-code.

## C1 — depth; K/D/E/U pre-declaration check

Before classification, the K/D/E/U definitions were already in the frozen contract at `697d2f17568d900fb0bfbe063c6292090781cbfe` (the contract's `claims.C1.rule`), including K's reachable-failure requirement and D's unreachable-after-return/raise criterion. Its amendment list at that frozen commit was empty. Later A1–A14 each state `rule_changed: false`; the deciding run is recorded after freeze. Thus the rule was frozen before classification, not authored to fit the result.

- Before receipt: `.ufo/evidence/round-43/before/c1-round42-at-base.stdout` at base `487b8f0…` says six declared, four killed, both named survivors; both direct probes in `control/c1-probe-survivors.stdout` say `survived`. Round-42 mutant JSON is unchanged and contains both exact edits (`git show 718a1e9:.ufo/evidence/round-42/census/mutants.json`).
- After receipt at measured commit `3c4003f6…`: `.ufo/evidence/round-43/after/c1-at-3c4003f6.stdout` records 6 declared, 5 killed, 1 `dead_code_only`, 0 equivalent/unresolved, 12/12 fixtures, `kill_binding=1`, `dead_code_arg_ok=1`, and PASS. Independently re-measured landing bytes using `python3 .ufo/evidence/round-43/mutants/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 718a1e987febd32eb78ebc65adfe939f23b3de63 --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` → same C1 verdict and counts (exit 0; output line begins `C1_R43: self_pin=1 ... mutants_declared=6 mutants_killed=5 dead_code_only=1 ... kill_binding=1 ... dead_code_arg_ok=1 ... C1_R43_PASS=true`).
- Spot read of counter confirms F11 uses `SimpleNamespace` and its failure is bound specifically to `F11_outflag_namespace`; reachability code is applied to the failing fixture, not a constant/source-only assertion. F12 has two top-level returns; `method_return`'s second return is after the first unconditional return. The differential probe reports its difference on F12 and the classification requires every differing case to be unreachable. Therefore `dead_code_only` is earned under the frozen rule, not a relabel, and it is explicitly not a kill or equivalence.
- Control: `control/c1-round42-battery-A10.stdout` gives the 10-fixture battery, 4 kills, control false; the original two survivors were genuinely killed in neither old battery nor direct probes.
- Verdict: **depth improved** (measured and evidence-verified).

## C2 — calibration

- Base receipt `.ufo/evidence/round-43/before/c2-at-base-A10.stdout`: `m12=2 m13=1 total=3`, false, at base `487b8f0…`; this is more mismatches than the summary's nominal two because the final counter also grades its own round-43 claim block. The earliest-recorded before-state remains m12=1/m13=1. Do-nothing counter receipt states old counter cannot emit m12/m13/classes.
- At `3c4003f6…`, after receipt reports seven classes all zero, total zero, 114 registry rows, PASS. Independently re-measured at landing with `python3 .ufo/evidence/round-43/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 718a1e987febd32eb78ebc65adfe939f23b3de63 --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` → `m7=1`, `total=1`, `first=m7:SCORECARD.md#round-43_unknown_S256`, `C2_R43_PASS=false` (exit 1). The landing SCORECARD contains an unknown S256 citation in the round-43 block; the frozen measurement commit predates this later claim-block edit. This means the claim's final predicate does not hold at the cited landing commit.
- Verdict: **calibration harmed** (the report's improved claim cannot be admitted: its own record currently fails m7). This is not a rerun of any sibling gate; the counter is lane-owned and its committed receipt was examined, then the specified count was re-derived over landing bytes.

## C3 — operability capability

- Base receipt at `487b8f0…`: `tool_absent=1`, selftest failure, C3 false. Control receipt has constant-empty stub disagreement and `C3_R43_CONTROL_PASS=false`.
- At `3c4003f6…`, committed frozen receipt reports selftest 24/24, 103 staged rows, 7 live collisions, 3 held docs, cascade/naive map refused, safe map admitted, `substitute=0`, C3 PASS. Independently re-measured landing bytes with `python3 .ufo/evidence/round-43/guard/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 718a1e987febd32eb78ebc65adfe939f23b3de63 --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` → same fields and `C3_R43_PASS=true` (exit 0). The receipt names revision and frozen snapshot digest; the protocol gate standard's committed self-test/frozen-run evidence is present. No axis harmed by the scorecard diff for this claim.
- Verdict: **operability improved** (capability acquisition verified).

## Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 remeasurement plus committed counter receipts and survivor-fixture spot-check |
| calibration | harmed | C2 landing remeasurement finds one false m7 source citation and failed predicate |
| operability | improved | C3 landing remeasurement and frozen/self-test receipt |

Admission is **false** because C2 fails at landing and calibration is harmed. This does not change lane status: the report represents committed round work and is not a marker.

## Discernment spot-check

| Item | Decision | Re-opened source | Result | Reason |
|---|---|---|---|---|
| Admit S159, Wikipedia mutation-testing definition/obstacle | admit | committed snapshot `.ufo/evidence/round-43/sources/wikipedia-mutation-testing.html`, lines 794–796; URL https://en.wikipedia.org/wiki/Mutation_testing | agree | Located text defines equivalent mutants behaviorally and says detection is a major obstacle. The lesson limits the citation to those points and does not attribute survivor/dead-code taxonomy to Wikipedia. Quote at line 796 is 15 words, within 25. |
| Re-open S089, Stryker equivalent mutants | re-open/held, no new row | committed snapshot `.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html`, lines 15–17; URL https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | agree | Line 16 says no definitive automatic way to find/ignore equivalent mutants; line 15 illustrates same output under operator changes. The lesson correctly records the changed digest and says text survives at the same offsets, rather than asserting byte identity. |
| Quote check for new registry row S159 | admitted, mined | `corpus/SOURCES.md` S159; snapshot lines 794–796 | agree | Registry teaches the equivalent-mutant behavioral definition and detection obstacle; both source statements support that bounded description. Lesson records two located quotes of 16 and 15 words. |

## Trends

- **expansion: improved** — new knowledge entry `corpus/knowledge/r43-survivor-resolution-rule.md` cites mined S159 and re-opened S089; it adds survivor-side K/D/E/U distinctions. Guard is a demonstrated new capability. Admit-quality review agrees with the bounded source use.
- **quality: unchanged** — C1's survivor classifications are grounded and C3's capability evidence holds, but C2's landed record currently fails its own m7 predicate. The report's quality-improved claim is therefore not fully sustained; no evidence here establishes an admitted knowledge entry false/stale or a stronger replacement that would meet LEARNING's quality-improved condition.
- **discernment: improved** — independent admit and reject/re-open decisions agree with lesson gates, with a located reason for each, and the new row's bounded quote is confirmed.

## Routed defects for round 44

- Reconcile the round-43 SCORECARD `m7` unknown `S256` citation and re-run the C2 measurement at the final intended revision; preserve correction as an append-only record, do not rewrite the filed report/lesson.
- Restore or explicitly disposition the modified tracked file `.ufo/waves/round-43/w1/RevC2Classes.md`; it is an unrelated dirty worktree change at closure.
- The lesson records the S089 anchor digest as stale after source drift; update its `anchor` to the re-opened snapshot in a future append-only registry change and log old→new in that round's lesson.
