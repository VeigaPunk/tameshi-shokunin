# T52W3RevQuality — QUALITY criterion 103 + round-52 `## Mistakes` (wave 3, cold-read)

Scope: `corpus/QUALITY.md` criterion 103 (round-52 block) and `corpus/lessons/round-52.md` `## Mistakes` (:41-47). For each of the 3 rows: class, evidence pointer, captured-by, fix-shown-able-to-fail; every cited receipt opened at CAND1 `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135` and every quoted red/green value re-checked. Read-only seat: no counter was executed (a probe is never a verdict); all confirmations are receipt-level. No installs or upgrades were needed; pacman untouched.

Provenance note: lane HEAD is `f1a3246105…` (wave 3 moved past CAND1), but every file cited here is blob-identical between CAND1 and the working tree (`git -C <lane> rev-parse CAND1:<f>` == `git -C <lane> hash-object <lane>/<f>` for contract.json, round-52.md, QUALITY.md, controls.stdout, a0/controls.stdout, T52W1ScoutRecurrence.md, T52W2ExecC1Probe.md). Commands below use `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b:<path>`; all cited receipts are lane-resident, so no copies were made into w3.

## Row-by-row verification (round-52.md:45-47)

Row 1 `tool-change-without-registry-row` (:45) — COMPLETE, fix is a check.
- Class/evidence: `corpus/lessons/round-51-verifier-spotcheck.md:84-88` carries the static R51.1 confirmation exactly as quoted (registry row still expects `9/9`; `mte-interop.py` adds `bash-drift-pins` → ten legs; SKILL.md `:2136` "nine ledger legs"); `:126` is routed defect 1 (update the row, record in a scope monitor, committed green receipt). `git show 7ff81a5b:corpus/lessons/round-51-verifier-spotcheck.md | sed -n '84,88p;126p'`.
- Recurrence pointer: `.ufo/waves/round-52/w1/T52W1ScoutRecurrence.md:15-19,36` classifies R51.1 as the R47.1-analogous tool/registered-gate drift and names the missing gate (operational registry replay at the candidate), explicitly "a note … would not enforce agreement" (:19).
- Captured-by "none at round 51" ✓ consistent with the routed remedy being new.
- Quoted values, all confirmed in `.ufo/evidence/round-52/control/controls.stdout` (11 lines, `CONTROLS: total=11 unexpected=0` :12): `C1_CTL_0` false with `held=48/49` (:1), `C1_CTL_STALE` false (:2), `C1_CTL_SUPERSEDE` false (:3), `C1_CTL_NEEDLE` false (:4), `C1_CTL_POSITIVE` true with `held=49/49 total=0` (:6). Per-control receipts exist for all 11 names under `.ufo/evidence/round-52/control/`; `C1_CTL_0.stdout:2` reads `summary=48/49 not_held=['mte-interop-check']` and `:4` `C1_MTE_ROW BAD … needles=[…9/9]` — the falsifier's "mte-interop-check differing" is receipt-backed, not inferred.

Row 2 `fleet-bound-run-outside-fleet` (:46) — COMPLETE, fix is a check (red/green pair on the standing positive control).
- Quoted value confirmed: `.ufo/evidence/round-52/control/a0/controls.stdout:6` = `C1_CTL_POSITIVE expect=true got=false -> UNEXPECTED … total=5 C1_R52_PASS=false`; `:12` `unexpected=1`. Exact match for "POSITIVE `total=5`".
- Amendment 1 present at CAND1 (`contract.json:80-85`), harness-only (fleet-mirror clone, branch per control), and the final re-run is 11/11 as pre-registered (`controls.stdout:12`).
- The standing detector is the pre-registered positive control itself: a0 shows it firing; after the amendment it passes. That satisfies "shown able to fail".

Row 3 `own-edit-breaks-frozen-row-rule` (:47) — COMPLETE, fix landed and is re-checked by a standing rule.
- Quoted values confirmed in `.ufo/waves/round-52/w2/T52W2ExecC1Probe.md`: probe `total=1 C1_R52_PASS=false` with `c3_total=1` (:7, :40), cause `selftest-cell-commands=3` at `SKILL.md:2157` (:84, :169).
- Fix landed before CAND1: `git show 7ff81a5b:SKILL.md | sed -n '2157p'` — the Self-test cell now contains exactly one backticked span (`` `python3 tools/round21-measure.py --selftest` ``); `c2-count.py`/`FLEET` are backtick-free there. Corroborated by `control/C1_CTL_POSITIVE.stdout:21` (`tools/round21-measure.py: covered line 2157 selftest exit=0 last=ROUND21_MEASURE_SELFTEST: 13/13 pass`).
- The frozen round-51 C3 row rule re-runs inside the C1 counter at every deciding run, so any future backticked prose in that cell re-blocks credit: a standing check, not a one-off cleanup.

No row is missing a field; no fix is a note. Every fix chains to a mechanism that re-fires (C1 counter at deciding; pre-registered positive control; frozen C3 row rule).

## QUALITY criterion 103 (QUALITY.md:1562-1570)

- Structure is check-shaped, not exhortation: "Check that can fail" (registry-check `held=N/N` over every active row + counted-panel comparison of `len(LEG_TABLE)` against every "<count> ledger legs"/`(K/K)` SKILL statement), "Lesson" pointer (round-52.md `## Mistakes` row 1 — correct, :45), "Falsifier that must fail".
- Falsifier values verified: base `held=48/49` with `mte-interop-check` differing = `control/C1_CTL_0.stdout:2,36` (`total=4`); `C1_CTL_STALE/SUPERSEDE/NEEDLE` all false = `controls.stdout:2-4`; positive `63b12e8c` `held=49/49` = `controls.stdout:6`. Cited receipt path exists at CAND1.
- Operative form exists: `.ufo/evidence/round-52/c1/measure.py` present at CAND1 (and c2/measure.py).
- The criterion is already operative at CAND1: zero `nine ledger legs` hits in CAND1 SKILL.md; `tools/registry.json:1014` expects `legs_conforming=10/10`; criterion numbering sequential (100 at :1469, 101 :1526, 102 :1550, 103 :1562).

## Findings

1. LOW (adjacent scope, re-key bookkeeping) — `corpus/lessons/round-52.md:34` records the cold-read drop as "18 sections … (64 → 46)", explicitly measured at CAND0; at CAND1 the same precheck prints `lost=19`, `cand_credited=45` (`.ufo/evidence/round-52/integrate/precheck-cand1.stdout:20`), the extra lost section being `### The tick and the pin read` (:16, absent from `precheck-cand0.stdout`, whose summary at :19 reads `lost=18`). The sentence is CAND0-anchored so it is not false, but the lesson nowhere states the CAND1 number, so a lesson-only reader under-counts the re-key surface by one section. Show: `git -C <lane> show 7ff81a5b:.ufo/evidence/round-52/integrate/precheck-cand0.stdout | grep -c '^LOST'` (18) vs `grep -c '^LOST' .ufo/evidence/round-52/integrate/precheck-cand1.stdout` (19). Suggested remedy belongs to the round record, not the frozen contract: one clause in the lesson's Re-key bullet stating the CAND1 count.

No other defect found in scope. Both observations below are non-defects recorded for the integrator:
- Contract C1 `before` prose still says `total=2` while the base arithmetic is `total=4`; this is self-disclosed in amendment 1's erratum (`contract.json:85`), and neither the lesson rows nor QUALITY 103 quotes the stale total (they quote `held=48/49` only). No action.
- Row 2's "evidence-disposition rows refused control commits on no branch" rests on amendment 1 prose (`contract.json:80-84`), not on a line of `a0/controls.stdout` (whose only UNEXPECTED line is the positive control). The row's primary red value (`total=5`) is receipt-backed.

## Residual risk and verification gaps

- Receipt-level only: I ran no counter, control, or precheck (seat bounds); the deciding-run outcome at CAND1 is the L1's to produce.
- Base vs CAND0 failure modes differ for the same C3 unit: `C1_CTL_0.stdout:21` shows behavioral red at base (`selftest-exit=1`), the probe shows grammar red at CAND0 (`selftest-cell-commands=3`). Consistent, but falsifier readers should not conflate them.
- I did not audit the 19 CAND1 re-key entries' contents (m6/C2 readers' scope), nor the correction records' counts (explicitly `cannot_see` in the contract).
- C1_CTL_0's `not_held=2` includes the summary-clause unit per the erratum arithmetic (`contract.json:85`); `total=4` for base is the erratum-corrected figure.

## Summary
- All 3 `## Mistakes` rows (round-52.md:45-47) have class, evidence pointer, captured-by, and a fix shown able to fail; none is a note.
- Every quoted red/green value verified at CAND1: controls 11/11 (`controls.stdout:12`), C1_CTL_0 `held=48/49` (:1), POSITIVE true `49/49` (:6), a0 POSITIVE red `total=5` (:6), probe `c3_total=1`/`selftest-cell-commands=3` (:40/:84).
- Row 3's fix verified landed: CAND1 `SKILL.md:2157` self-test cell has exactly one backticked span; `nine ledger legs` = 0 hits; `registry.json:1014` expects `10/10`.
- QUALITY 103 (:1562-1570) is check-shaped with receipt-backed falsifiers and a correct lesson pointer; numbering sequential.
- 1 LOW finding: lesson states the CAND0 drop count (18) but not the CAND1 count (19, extra section `The tick and the pin read`); CAND0-anchored, not false.
- No installs/upgrades; read-only seat; no counters run; all cited receipts lane-resident and blob-identical CAND1↔working tree; scratch deleted before yield.
