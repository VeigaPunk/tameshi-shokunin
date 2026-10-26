# T50ScoutB5 — F6 frontier recon (round 50)

Seat T50ScoutB5, scout. Read-only on the lane; this file is the only write. Lane tip read: `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2` (`git rev-parse HEAD`). No counter was run. No tool was installed.

## 1. What "B5" is

- B5 is a **mutant (defect) of the kagi bash gate `surface-census.sh`**, not a fixture: "defect B5 | surface-census.sh:214-217" deletes the exec-bit arm (`if [[ "$kind" == "exec" && ! -x "$abs" ]] … SURFACE DIVERGED … (declared exec, no execute bit)`). Spec: `.ufo/evidence/kaika-round-1/coldread/spec-B.txt:18-20` (`grep -n 'defect B5' .ufo/evidence/kaika-round-1/coldread/spec-B.txt`).
- It **survived** the gate's own 16-case selftest: `SURVIVED (exit=0 …) surface-census.sh:214-217`, `.ufo/evidence/kaika-round-1/coldread/appendixB/results.tsv:6`; also `B-tool.txt:50`; declared reason `.ufo/evidence/round-12/BashWitness/declared.tsv:16` ("NONE: no selftest case creates a declared-exec path that is a regular file without the execute bit"). First sighting of the B5/B10 PASS: `.ufo/evidence/fleet-round-1/inherited-calibration.patch:77-83`.
- "B5 probe fixture" = the hand-built kaika-round-1 survivor probe: `.ufo/evidence/kaika-round-1/coldread/probe-fixtures/probe/` (`find … -type f | xargs ls -la`).

## 2. Its size, and whether it kills

- Size (measured now, `ls -la` of the directory): `census.tsv` 44 B = **1 row** (`$HOME/bin/tool	asset	exec	-	probe no-x exec`), `baseline.tsv` 0 B, `shapes.tsv` 0 B, `host/bin/tool` 1 B (non-executable, `-rw-r--r--`). So **1 census row + 1 host file = 2 units**, 4 files. It was never reduced by any tool; at 1 row it has nothing removable that keeps the kill, but no receipt says "1-minimal" for it.
- Kill: yes. Pristine prints `SURFACE DIVERGED $HOME/bin/tool (declared exec, no execute bit)` + `DRIFT (diverged=1 …)`; B5 mutant prints `SURFACE OK       $HOME/bin/tool (exec 644)` + `CLEAN` — `.ufo/evidence/kaika-round-1/coldread/B-probe-B5-pristine.txt`, `B-probe-B5-mutant.txt` (`cat` both). It is a kill of a survivor by a hand-built fixture, an `ADDITIVE-IMPROVISATION` per `reports/round-1-kaika-coldread.md:198` and `.ufo/waves/round-12/w1/SHONENReview.md:48`.
- The README row's "unmeasured" was therefore stale already at round 1 (size is 2 units; kill is observed); what no round had was a **tool-driven reduction with a stated cost** on a survivor fixture.

## 3. What round 29 already did to this move (F6 is not virgin)

- Pre-registered as "survivor B5 of the kagi surface-census leg … probe fixture reduced by delta debugging (S024) to a fixture that still kills B5 and is 1-minimal at line and file granularity", `corpus/README.md:440-447` ("this section claims no status change for F6").
- Outcome: honest stop. Pinned-declaration B5 fixture: 105 → 105 units, `kill_original=0` (B5 is masked by the exact-mode check; all 512 modes swept on three exec rows, no kill): `.ufo/evidence/round-29/c2-at-E.stdout:2`, `corpus/knowledge/survivor-fixture-minimization.md:45-47,57-77`, `corpus/lessons/round-29-verifier-spotcheck.md:110-121`, `SCORECARD.md:1454,1457-1458`.
- Only reduction ever shown: BuildF6A's non-anchored variant, 100 → 2 units with `kill=1 one_minimal=1 ddmin_match=1` but `anchored=0`, "not counted … the reachable starting point for the next F6 round": `corpus/lessons/round-29.md:162-167`, `.ufo/waves/round-29/w1/BuildF6A.md:205-236`.
- Stated next steps in the entry: a survivor "whose kill is reachable inside its own pinned declaration", or a stated declaration transformation: `corpus/knowledge/survivor-fixture-minimization.md:83-90`. Neither names B5 as the only admissible target.

## 4. Is this round's shrinker the same move?

Verdict: **a different instance of the same move; it does not discharge the README row's literal B5 text.**

- Different gate and language: the round-50 target is the lane's own `tools/staged-id-guard.py` (497 lines; `wc -l`) driven by the round-49 generator `tools/pbt-staged-id.py`, shrinking `CASE = {registry, staged, map}` for 20 mutants; B5 is a bash census mutant with a host-tree fixture (`.ufo/evidence/round-50/contract.json` `.claims.C2.predicate`, `.claims.C2.shrinker_interface`). B5 is not in the round-50 panel; no round-50 artifact touches `surface-census.sh`.
- Same method: interestingness-driven reduction to a 1-minimal case, kill check preserved, cost stated — the S024 contract `corpus/knowledge/survivor-fixture-minimization.md:14-19` and the row's own "reduced size + kill check" (`corpus/README.md:83`). Contract `.claims.C2.cannot_see` admits a plain greedy-to-fixpoint loop meets the bar, so the claim is capability + method + cost.
- Survivor relation: the round-49 panel is not "survivors" in the mutation-sweep sense, but the guard's own 14 selftest fixtures kill only 6 of the 12 (`corpus/knowledge/pbt-generator-pilot.md:61-63`; `.ufo/evidence/round-49/control/c2-controls.stdout` CTL_FIX `confirmed=6`), so 6 panel mutants are survivors of the selftest fixtures killed only by generator cases — the shrinker's input for those is a survivor-killing case. The other 6 are fixture-killed, so "survivor" is true for half the panel only.
- Round-49 generator states "No shrinking: a counterexample is the first failing case, not a minimal one" (`corpus/knowledge/pbt-generator-pilot.md:69`) and F10's next move was "a second gate, or shrinking" (`corpus/README.md:599`): the shrinker also serves F10, not F6 alone.
- Source condition: the contract cites staged S167 (Zeller & Hildebrandt TSE 2002) as the row opened this round (`contract.json` `.claims.C2.sourced`); until now it was only a failed lead (`corpus/SOURCES.md:184`); S167 has no registry row at tip (`grep -n S167 corpus/SOURCES.md` empty) — the opening is another seat's job (T50ExecSrcZeller; wave dir `.ufo/waves/round-50/w1/T50ExecSrcZeller`).

## 5. Every F6 statement (tip), in order

| Where | Statement | Status it carries |
|---|---|---|
| `corpus/README.md:83` | Frontier row: F6, S022, S023, S024, `open`, "B5 probe fixture size: unmeasured → reduced size + kill check" | open |
| `corpus/README.md:431,440-447` | Round 29 pre-registration for B5, no status claim | open |
| `corpus/README.md:482` | Index row for `survivor-fixture-minimization.md`: "honest stop … no verdict changes" | open |
| `corpus/README.md:599` | F10 line (precedent wording; no F6 text) | — |
| `corpus/knowledge/survivor-fixture-minimization.md:7-10,83-90` | "frozen target was not reached … F6 stays open"; next moves | open |
| `corpus/knowledge/survivor-fixture-minimization.md:3-5` | verified-at 2026-10-23 "F6 honest-stop verdict is unchanged"; recheck drifts if F6 row changes status | stale on status change (touch header when F6 flips) |
| `SCORECARD.md:1024` | Round 22: "frontier F1/F4/F6/F7/F8/F9/F10 … unclosed" | open |
| `SCORECARD.md:1442-1459` | Round 29 row: C2 missed (honest stop), `units_original=105 units_minimized=105`, PASS false | open |
| `SCORECARD.md:2412,2429` | Round 50 pre-registration: C2 "F6 held (round 50) and an F6 entry citing a row opened 2026-10-26"; before = `corpus/README.md:83` open | pending |
| `corpus/lessons/round-29.md:13-15,71-73,83-84,153-167` | C2 sourced on S024; B5 masked; BuildF6A reduction 100→2 not counted | open |
| `corpus/lessons/round-29-verifier-spotcheck.md:110-121,165-168` | C2 missed confirmed; entry new ground, claims no kill | open |
| `corpus/lessons/round-34-verifier-spotcheck.md:147`, `round-35.md:83`, `round-35-verifier-spotcheck.md:40`, `round-36.md:16` | Entry's index/header-trio repairs only | no F6 verdict |
| `corpus/lessons/round-45.md:107,114`, `corpus/lessons/round-49.md:111` | contain "shrinking" / "F5-F6" but about F10 / cold-read cite-form (not frontier F6) | none |
| `corpus/SOURCES.md:33-35,151,179-188` | S022/S023/S024 rows; reading path; Zeller & Hildebrandt "stays a lead" | open |
| `corpus/QUALITY.md:696` | BuildF6B/A process incident, not frontier status | none |
| `.ufo/evidence/round-17/coldread/assemble.py:127`, `round-18/…:126` | "F6/F10" there is a trace-gate fixture id, unrelated to frontier F6 | none |

No statement anywhere in README/SCORECARD/lessons marks F6 held, closed or discharged before round 50.

## 6. Recommended `## Round 50` F6 line

Constraint from the counter (`.ufo/evidence/round-50/c2/measure.py:329-330`): one physical README line containing `\bF6\b` and the literal `held (round 50)`; keep the F10 precedent form (conditioned on the deciding receipt, void-if-not-true, frontier row left as written — `corpus/README.md:599`). Placeholders in braces are the L1's to fill from the deciding receipt; do not state counts before it prints.

> F6 (fixture minimization for survivors): open → **held (round 50)** for the generic move "reduced size + kill check by a stated-cost 1-minimal reduction", not for the B5 text of its row, conditioned on the round-50 deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; if that receipt prints anything else, this line is void as of round 50 (the round report states it and the next round appends the erratum here). What the move is: `tools/shrink-case.py` reduces the round-49 generator's killing case for a mutant of `tools/staged-id-guard.py` to a sub-case no single registry line, staged line or map entry can be removed from without losing the kill, and prints its guard-run count (`corpus/knowledge/{NEW_ENTRY}.md`; source S167, opened 2026-10-26). What it is not: survivor B5 (kagi `surface-census.sh:214-217`) is a different gate; its hand-built probe fixture (1 census row + 1 host file, `.ufo/evidence/kaika-round-1/coldread/probe-fixtures/probe/`) still kills it and has no tool reduction, and its pinned-declaration form stays the round-29 honest stop (`corpus/knowledge/survivor-fixture-minimization.md:57-77`), so B5 is not discharged. Limits: one gate, and half the round-49 panel mutants are not selftest survivors (`corpus/knowledge/pbt-generator-pilot.md:61-63`). The frontier table row above stays as written (append-only); F6's next move is a survivor of a second gate (B5 under a stated declaration transformation, `corpus/knowledge/survivor-fixture-minimization.md:89-90`).

Sentence pointers: (1) row `corpus/README.md:83`; (2) condition clause mirrors `corpus/README.md:599`; the receipt directory is `.ufo/evidence/round-50/after/` (`SCORECARD.md:2431`) and the file name `c2.stdout` follows round 49's `after/c2.stdout` (`corpus/README.md:599`) — [INFERENCE] for round 50, the L1 confirms the name; (3) mechanism = `contract.json` `.claims.C2.predicate`; (4) B5 non-discharge = §1–§3 above; (5) limits = §4 pointers.

If the L1 prefers the status bare ("open → held (round 50)" with no narrowing), that overstates: the row's literal move names B5 and the shrinker never touches it. The narrowed wording above still satisfies the counter's regex. Also required when F6 flips: refresh `corpus/knowledge/survivor-fixture-minimization.md` header (lines 4-5 say the F6 verdict is unchanged and the recheck drifts on an F6 status change) — a new entry is needed by the counter anyway (`measure.py:345-353`: new since BASE, names F6, `source:` cites a `mined` S-id opened 2026-10-26); either add the round-50 pointer to the old entry or write a distinct new entry and cite it from the README line; do not reuse the old entry as the "new" one.

## Summary
- B5 = kagi `surface-census.sh:214-217` exec-bit-arm mutant; survived the 16-case selftest (`kaika-round-1/coldread/appendixB/results.tsv:6`).
- B5 probe fixture = `kaika-round-1/coldread/probe-fixtures/probe/`: 1 census row + 1 host file (44 B + 1 B); it kills B5 (`B-probe-B5-*.txt`); README "unmeasured" was stale, no tool reduction exists.
- Round 29 tried the B5 reduction and stopped honestly (105 → 105, masked; `knowledge/survivor-fixture-minimization.md:45-77`); the only reduction was a non-anchored 100 → 2 variant, uncounted.
- Round-50 shrinker targets `staged-id-guard.py` mutants: same method, different gate; it does not discharge B5 and does not mention it.
- No source marks F6 held before round 50; all F6 statements are open (table §5).
- Recommended line §6: "open → held (round 50)" narrowed to the generic move, conditioned on `after/c2.stdout`, B5 explicitly not discharged; one physical line (counter `measure.py:329-330`); refresh the old entry's header or cite a new one.
