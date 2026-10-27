# Seat T51W2Read15 — cold-read re-key reader (round 51, wave 2, falsify)

Section: `## Seventh recorded case and full-page cold-read — round 16`
Lane: `tameshi-shokunin`; base `9962033fd7a75aa2f2847e979dd687a5d28505a1`; candidate `6d8c11e378aa90b12650808e1b79270742935f15`.
Section span at CAND: **lines 1754–1813** (next `##` heading `## Live-tree re-pin and entry-command monitor — round 17` at 1814); the nested `### Round-16 gate/probe registry` sits at 1806–1813 inside it. SKILL.md lines 1–2134 are byte-identical base→CAND (`git diff 9962033..6d8c11e -- SKILL.md` touches only the appended `#### Gate/probe registry — round 51` at :2137+), so every section-internal line anchor is unchanged.

Method: every pointer resolved against candidate bytes via `git show CAND:<path>`; the section's reproduce block was **executed** against candidate bytes (strongest falsifier). No repo was mutated; all scratch under `/fast/scratch/hyaku/tameshi-r51/T51W2Read15/`, deleted before yield.

## Verdict summary

- **One stale statement (the re-key edit this section needs):** the leg-count progression "(`tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26)" stops at nine. At CAND the runner embeds the tenth leg `bash-drift-pins` (r51): its own doc line `tools/mutate-and-run.sh:84` now reads "r26 nine; r51 ten", and `--regression` prints `cases=10` (wave-1 receipt `.ufo/waves/round-51/w1/T51ExecEmbed/regression.stdout`: `REGRESSION: PASS (cases=10 passed=10; …)`). Each dated clause as written is true; the progression must gain "`cases=10` since round 51".
- Everything else in the section holds against candidate bytes, including the executed reproduce block (below).
- **Four panel-tool updates (tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, mte-interop.py): no impact** — the section cites none of them (its pointers name only `tools/mutate-and-run.sh`, the round-16 evidence dir, the case note, `measure.py`, `assemble.py`, `reattribute.py`, the kumitate blob, and — one hop via the case note — `arm-class-matrix.md` §13 and `PROVINCE.md:7-11`).
- **Runner TMPDIR change: no impact** — the section's only `/tmp` statements are the reproduce scratch (`mktemp -d /tmp/tameshi-r16-rg.XXXXXX`, still valid; the recorded sweep itself ran under `/tmp`) and the historical "instructions were executed in `/tmp`". The block passes an explicit `--workdir`, so the runner's new `${TMPDIR:-/tmp}` auto-scratch defaults (`runner-cand.sh:491, :1432, :1555`) are not exercised, and the scrub rule is untouched (the suite's `TMPDIR` is sandboxed by `suite.txt` regardless of the operator's environment).

## Pointer-by-pointer verification (candidate bytes)

| # | Raw pointer text (section) | File / ranges | Verdict | Located excerpt / evidence |
|---|---|---|---|---|
| 1 | "kumitate `scripts/round-gate.mjs` at rev `364f1d5`" | kumitate-shokunin rev `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`, `scripts/round-gate.mjs` (1511 lines) | holds | `git -C kumitate-shokunin cat-file -t 364f1d5…` → `commit`; blob materializes |
| 2 | "blob sha256 `f890e277…a834d3e9`" | same blob | holds | recomputed `sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` |
| 3 | "60-case hermetic `--selftest`" | `.ufo/evidence/round-16/round-gate/sweep/sweep.log` (control block) | holds | `ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS`; my re-run control also green |
| 4 | "10 single-edit mutants → 5/10 killed (50 %)" | `.ufo/evidence/round-16/round-gate/sweep/results.tsv` (10 rows) + `sweep.log` | holds | `MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)`; KILLED: A1 A3 B1 E3 C1060; SURVIVED: C1059 A2 B2 CKIND E1 |
| 5 | "control green, 0 inconclusive" | `sweep.log` | holds | `CONTROL: GREEN (exit=0 …)`; `inconclusive=0` |
| 6 | "`MUTATE_RESTORE: OK`" | `sweep.log` | holds | `MUTATE_RESTORE: OK (target-sha256 before=…=after=f890e277…)` |
| 7 | "every one of the 10 predictions, committed in `e69b488` before the sweep, held" | lane commit `e69b488`; `.ufo/evidence/round-16/round-gate/predictions.json` | holds | `e69b488` adds predictions.json + spec + suite.txt; committer date `2026-10-20 10:39:59 -0300` (=13:39:59Z) < `MUTATE_DATE: 2026-10-20T13:40:15Z`; all 10 `predictions[].prediction` == `results.tsv` verdicts |
| 8 | "Detail of record: `corpus/knowledge/mutation-case-kumitate-round-gate.md`" | `corpus/knowledge/mutation-case-kumitate-round-gate.md` (unchanged base→CAND) | holds | §2 table matches results.tsv; §4 probe table matches survivor-probes logs; §6 records GuardAudit + bwrap |
| 9 | "The case is ledger leg `js-round-gate`" | `tools/mutate-and-run.sh:94` (ledger row), `:1489-1492` (leg call), `TABLE_ROUNDGATE` `:641` | holds | row `js-round-gate  kumitate-shokunin/scripts/round-gate.mjs  5/10 (50 %)`; still leg 7 of 10 |
| 10 | "`--regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26" | `tools/mutate-and-run.sh:84` (doc), `:1552+` (count) | **stale at CAND** | runner doc now "r26 nine; r51 ten"; `--regression` prints `cases=10` (T51ExecEmbed receipt). Re-key: append "`cases=10` since round 51" |
| 11 | reproduce block `W=$(mktemp -d /tmp/tameshi-r16-rg.XXXXXX)` … `--workdir "$W/work"` | executed | holds | see "Executed falsifier" — rc=0, exact expected lines |
| 12 | `git -C ~/Projects/shokunin/kumitate-shokunin show 364f1d5…:scripts/round-gate.mjs` | kumitate object store | holds | materializes the pinned blob (sha matches #2) |
| 13 | `sha256sum` expectation `f890e277…d3e9` | — | holds | recomputed, equal |
| 14 | `E=.ufo/evidence/round-16/round-gate`; `--defects "$E/round-gate.defects.spec"` | `.ufo/evidence/round-16/round-gate/` at CAND | holds | dir + spec exist; spec sha256 `e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4` == `sweep/spec.copy` == `predictions.json.spec_sha256` |
| 15 | `--suite "$(cat "$E/suite.txt")"`; "the ledger leg carries the same string" | `.ufo/evidence/round-16/round-gate/suite.txt` vs `tools/mutate-and-run.sh:1491` | holds | byte-identical strings (`h="$WORKDIR/sandbox-$DEFECT_ID"; … env -i … HOME="$h/home" TMPDIR="$h/tmp" … node "$MUTANT" --selftest`) |
| 16 | expected `CONTROL: GREEN ... MUTATE: DONE (... killed=5 survived=5 inconclusive=0 kill-rate=50%)` | runner output format | holds | executed at CAND bytes → exact match |
| 17 | scrub rule: "env -i with its own HOME and TMPDIR (the string in suite.txt)" | suite.txt; runner leg | holds | see #15 |
| 18 | "(GuardAudit, round 16)" / "use `bwrap` when mutants are untrusted" | `.ufo/waves/round-16/w2/GuardAudit.md` (exists at CAND); case note §6 | holds | case note: "GuardAudit showed a hostile mutant can still write outside its directory, overwrite a sibling mutant, or reach the network… `bwrap` confinement (tested by GuardAudit) is the next step" |
| 19 | "Grade by exit, not by stdout bytes… `tools/mutate-and-run.sh` grades on exit only" | `tools/mutate-and-run.sh:545-551` | holds | `case $RC in 0) SURVIVED ;; 124/126/127) INCONCLUSIVE ;; *) KILLED` — no stdout comparison in grading |
| 20 | "round-4 projection … `REPORT_MIN_BYTES` in [26, 1059] … 1059 survived … 1060 killed by the 1059-byte fixture" | `corpus/knowledge/arm-class-matrix.md` §13 (`:414-416`); results.tsv C1059/C1060; case note §3 | holds | matrix: "any integer in **[26, 1059]** changes no fixture verdict — the floor is *interval*-pinned"; C1059 SURVIVED, C1060 KILLED |
| 21 | "survivor-probe harness (`$E/survivor-probes/probes.mjs`, probe ids in the case note) … pristine (exit 0) … mutant (exit 1)" | `.ufo/evidence/round-16/round-gate/survivor-probes/` at CAND | holds | `probes.mjs` present; case note §4 lists P1, P1b (A2), P6 (B2), P9 (E1), `c1059-probe.sh` (C1059); logs: pristine `"ok": true` / mutant `"ok": false`; c1059 pristine `ROUND_GATE: CLEAN` vs mutant `ROUND_GATE: DRIFT` |
| 22 | "The errata section above lists what it found and repaired" | SKILL.md `## Errata — round 16 full-page cold-read` (1707–1753) | holds | repairs table present (snapshot sha `97cf436b…`, 51 buckets, CR01–CR27) |
| 23 | "repaired and new sections were re-read by fresh seats (wave 2, then a residual check)" | `.ufo/waves/round-16/w2/` (68 files incl. RR01–RR15, RR12b), `w3/RX1–RX8` | holds | both dirs populated at CAND |
| 24 | "counting command `python3 .ufo/evidence/round-16/measure.py --rev REV` (field `coldread.box3_full_page`)" | `.ufo/evidence/round-16/measure.py` (unchanged base→CAND) | holds | field `box3_full_page` at `:19/:221/:265/:287`; doc "Exits: 0 ok · 2 rev/blob missing … · 64 usage" |
| 25 | "earns the box-3 lane assertion (`[~]`), never an independent `[x]`" | `SHONEN.md` box 3; `.ufo/evidence/round-21/coldread/ledger.json` | holds | SHONEN.md third box is `[~] Instructions executable…` linking `.ufo/evidence/round-21/coldread/ledger.json`; measure.py `box3_marked = marks[2] == '~'` |
| 26 | registry row `tools/mutate-and-run.sh` — "selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage" | runner `:248-251` (usage 64), `die_setup` exit 2, regression FAIL exit 1 / SETUP exit 2 / PASS 0 (`:1519-1541`), selftest FAIL exit 1 / PASS 0 | holds at CAND | wave-1 receipts: `--selftest` 107/107 rc=0; `--regression` PASS cases=10 rc=0; SETUP arm `:1533-1541` intact |
| 27 | registry row `.ufo/evidence/round-16/measure.py` — "0 measured · 2 rev/blob missing · 64 usage" | measure.py `:35`, selftest checks `:612-622` | holds | `exit2-blob-missing`, `exit2-bad-rev`, `exit64-no-rev`, `exit64-unknown-arg` all asserted |
| 28 | registry row `.ufo/evidence/round-16/coldread/assemble.py` — "0 … · 1 a bucket uncovered · 2 usage (argparse), an invalid override or a heading mismatch (round 17)" | assemble.py selftest `:795-977` | holds | "incomplete coverage exits 1", "heading mismatch exits 2", relaxing/equal-rank override rejected exit 2; rejected reports listed in `reports_rejected`, not counted (`:339-352`) |
| 29 | registry row `.ufo/evidence/round-16/attribution/reattribute.py` — "0 corrected rule passes the oracle · 1 it fails" | reattribute.py `run_selftest` tail | holds | returns 0 on PASS / 1 on FAIL; `raise SystemExit(main())` |

## Executed falsifier (strongest check)

Ran the section's reproduce block against **candidate bytes**: runner = candidate blob (`sha256 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`, the bytes CAND embeds), spec = CAND `.ufo/evidence/round-16/round-gate/round-gate.defects.spec`, suite = CAND `suite.txt`, target = kumitate blob `364f1d5…:scripts/round-gate.mjs` (sha `f890e277…` verified before the run). Result (scratch workdir, deleted after):

```
rc=0
CONTROL: GREEN (exit=0 duration-ms=5632 pristine-sha256=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9)
MUTATE_RESTORE: OK (target-sha256 before=f890e277… after=f890e277… pristine-sha256=f890e277…)
MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
```

Byte-equal to the section's expected line. Falsification of the reproduce claim **failed** — the block holds at CAND, including under the tenth-leg runner and the TMPDIR-honouring defaults.

## Record-level observations (not section defects)

- The case note's §5 quotes dated receipts ("`REGRESSION: PASS (cases=7 passed=7…)`", "`MUTATE_SELFTEST: 83/83 pass`") pinned to the round-16/17 runner (`0673d2e5…`, per `runner-sha256.txt`'s round-17 correction note). Current runner is `977de470…` (cases=10, selftest 107/107). These are dated records and need no edit; the section's own parenthetical (#10) is the surface that must carry the current count.
- This section lost cold-read credit at CAND solely via its ledger entry's `input-drift:tools/mutate-and-run.sh` (the entry pins the old runner sha); the re-key re-anchors it to the CAND bytes this row was read against.

## Proposed re-key wording (the one edit)

`…(`tools/mutate-and-run.sh --regression` → `cases=7` at round 16; `cases=8` since round 18; `cases=9` since round 26; `cases=10` since round 51).`

## reads.json row

```json
{
  "seat": "T51W2Read15",
  "heading": "## Seventh recorded case and full-page cold-read — round 16",
  "cand": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "section_lines_cand": "1754-1813",
  "nested_heading": "### Round-16 gate/probe registry",
  "nested_lines_cand": "1806-1813",
  "next_heading": "## Live-tree re-pin and entry-command monitor — round 17 (1814)",
  "skill_unchanged_base_to_cand": "SKILL.md 1-2134 byte-identical; C3 registry append at 2137+",
  "pointers": [
    {"raw": "kumitate scripts/round-gate.mjs at rev 364f1d5", "file": "kumitate-shokunin:scripts/round-gate.mjs", "ranges": "rev 364f1d5954158ef8844bca4a5fef57b05d2f2ca5, whole blob (1511 lines)", "verdict": "holds", "excerpt": "cat-file -t -> commit; blob materializes"},
    {"raw": "blob sha256 f890e277…a834d3e9", "file": "kumitate-shokunin:scripts/round-gate.mjs", "ranges": "whole blob", "verdict": "holds", "excerpt": "sha256sum -> f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9"},
    {"raw": "60-case hermetic --selftest", "file": ".ufo/evidence/round-16/round-gate/sweep/sweep.log", "ranges": "control block", "verdict": "holds", "excerpt": "ROUND_GATE_SELFTEST: 60/60 pass / VERDICT: PASS"},
    {"raw": "10 single-edit mutants -> 5/10 killed (50 %)", "file": ".ufo/evidence/round-16/round-gate/sweep/results.tsv", "ranges": "10 rows", "verdict": "holds", "excerpt": "KILLED A1 A3 B1 E3 C1060; SURVIVED C1059 A2 B2 CKIND E1"},
    {"raw": "control green, 0 inconclusive, MUTATE_RESTORE: OK", "file": ".ufo/evidence/round-16/round-gate/sweep/sweep.log", "ranges": "header/restore lines", "verdict": "holds", "excerpt": "CONTROL: GREEN (exit=0 …); MUTATE_RESTORE: OK"},
    {"raw": "predictions committed in e69b488 before the sweep; all 10 held", "file": "lane commit e69b488; .ufo/evidence/round-16/round-gate/predictions.json", "ranges": "predictions (10)", "verdict": "holds", "excerpt": "commit 2026-10-20 10:39:59 -0300 < MUTATE_DATE 2026-10-20T13:40:15Z; 10/10 predicted == measured"},
    {"raw": "Detail of record: corpus/knowledge/mutation-case-kumitate-round-gate.md", "file": "corpus/knowledge/mutation-case-kumitate-round-gate.md", "ranges": "whole file (unchanged base->CAND)", "verdict": "holds", "excerpt": "§2/§4/§6 match results.tsv, survivor-probes logs, GuardAudit/bwrap"},
    {"raw": "ledger leg js-round-gate", "file": "tools/mutate-and-run.sh", "ranges": ":94 ledger row; :1489-1492 leg call; :641 TABLE_ROUNDGATE", "verdict": "holds", "excerpt": "js-round-gate kumitate-shokunin/scripts/round-gate.mjs 5/10 (50 %); leg 7 of 10"},
    {"raw": "--regression -> cases=7 at round 16; cases=8 since round 18; cases=9 since round 26", "file": "tools/mutate-and-run.sh", "ranges": ":84 doc; :1552+ count", "verdict": "stale-at-cand", "excerpt": "runner doc now 'r26 nine; r51 ten'; --regression prints cases=10 (T51ExecEmbed/regression.stdout); re-key: append 'cases=10 since round 51'"},
    {"raw": "reproduce block (mktemp /tmp; git show kumitate blob; sha256sum; E=round-16/round-gate; --defects/--suite/--label/--workdir; expected CONTROL/DONE lines)", "file": "tools/mutate-and-run.sh + .ufo/evidence/round-16/round-gate/{round-gate.defects.spec,suite.txt} + kumitate blob", "ranges": "executed end to end at CAND bytes", "verdict": "holds", "excerpt": "rc=0; CONTROL: GREEN; MUTATE_RESTORE: OK; MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%) — byte-equal to the section's expected line"},
    {"raw": "spec sha (implicit via predictions/spec.copy)", "file": ".ufo/evidence/round-16/round-gate/round-gate.defects.spec", "ranges": "whole file", "verdict": "holds", "excerpt": "sha256 e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4 == sweep/spec.copy == predictions.spec_sha256"},
    {"raw": "suite.txt string; ledger leg carries the same string", "file": ".ufo/evidence/round-16/round-gate/suite.txt vs tools/mutate-and-run.sh:1491", "ranges": "1 line", "verdict": "holds", "excerpt": "byte-identical env -i … HOME/TMPDIR sandbox string"},
    {"raw": "(GuardAudit, round 16); use bwrap when mutants are untrusted", "file": ".ufo/waves/round-16/w2/GuardAudit.md; case note §6", "ranges": "seat report exists at CAND", "verdict": "holds", "excerpt": "scrub-does-not-confine finding recorded; bwrap recommended"},
    {"raw": "tools/mutate-and-run.sh grades on exit only", "file": "tools/mutate-and-run.sh", "ranges": ":545-551", "verdict": "holds", "excerpt": "case $RC: 0 SURVIVED / 124,126,127 INCONCLUSIVE / * KILLED"},
    {"raw": "round-4 projection REPORT_MIN_BYTES [26, 1059]; 1059 survived, 1060 killed by the 1059-byte fixture", "file": "corpus/knowledge/arm-class-matrix.md §13 (:414-416); sweep results C1059/C1060", "ranges": "§13.4", "verdict": "holds", "excerpt": "'any integer in [26, 1059] changes no fixture verdict — interval-pinned'"},
    {"raw": "survivor-probe harness $E/survivor-probes/probes.mjs; probe ids in the case note; pristine exit 0 / mutant exit 1", "file": ".ufo/evidence/round-16/round-gate/survivor-probes/", "ranges": "probes.mjs + 10 logs + c1059-probe.sh", "verdict": "holds", "excerpt": "P1/P1b/P6/P9/c1059 in case note §4; pristine ok:true vs mutant ok:false; CLEAN vs DRIFT"},
    {"raw": "The errata section above lists what it found and repaired", "file": "SKILL.md", "ranges": "1707-1753", "verdict": "holds", "excerpt": "## Errata — round 16 full-page cold-read with repairs table"},
    {"raw": "repaired and new sections re-read by fresh seats (wave 2, then a residual check)", "file": ".ufo/waves/round-16/w2/, w3/", "ranges": "68 w2 files incl. RR01-RR15b; RX1-RX8", "verdict": "holds", "excerpt": "both dirs populated at CAND"},
    {"raw": "counting command python3 .ufo/evidence/round-16/measure.py --rev REV (field coldread.box3_full_page)", "file": ".ufo/evidence/round-16/measure.py", "ranges": ":19,:221,:265,:287; exits :35", "verdict": "holds", "excerpt": "field present; exits 0/2/64"},
    {"raw": "earns the box-3 lane assertion ([~]), never an independent [x]", "file": "SHONEN.md; .ufo/evidence/round-21/coldread/ledger.json", "ranges": "SHONEN box 3", "verdict": "holds", "excerpt": "box 3 is [~] linking the round-21 coldread ledger; measure.py marks[2]=='~'"},
    {"raw": "registry row tools/mutate-and-run.sh: selftest 0/1; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage", "file": "tools/mutate-and-run.sh", "ranges": ":248-251 usage 64; :1519-1541 regression exits; selftest FAIL exit 1", "verdict": "holds", "excerpt": "wave-1 receipts: selftest 107/107 rc=0; regression PASS cases=10 rc=0"},
    {"raw": "registry row .ufo/evidence/round-16/measure.py: 0 measured · 2 rev/blob missing · 64 usage", "file": ".ufo/evidence/round-16/measure.py", "ranges": ":35; selftest :612-622", "verdict": "holds", "excerpt": "exit2-blob-missing / exit2-bad-rev / exit64 asserted"},
    {"raw": "registry row .ufo/evidence/round-16/coldread/assemble.py: 0 covered · 1 uncovered · 2 usage/override/heading", "file": ".ufo/evidence/round-16/coldread/assemble.py", "ranges": "selftest :795-977", "verdict": "holds", "excerpt": "incomplete->1; heading mismatch->2; overrides->2; rejected reports listed not counted"},
    {"raw": "registry row .ufo/evidence/round-16/attribution/reattribute.py: 0 oracle pass · 1 fail", "file": ".ufo/evidence/round-16/attribution/reattribute.py", "ranges": "run_selftest tail", "verdict": "holds", "excerpt": "returns 0/1; SystemExit(main())"}
  ],
  "panel_tool_updates_impact": "none — section cites none of tally-audit.py / tally-audit-v2.py / tally-audit-v3.py / mte-interop.py",
  "runner_tmpdir_change_impact": "none — block passes explicit --workdir; suite TMPDIR sandboxed by suite.txt; runner's new ${TMPDIR:-/tmp} defaults (:491,:1432,:1555) not exercised by this section's claims",
  "falsifier": "Executed the section's reproduce block against candidate bytes (runner blob 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda, spec e99b87eb…11c4, suite.txt, kumitate blob f890e277…d3e9): rc=0, CONTROL: GREEN, MUTATE_RESTORE: OK, MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%) — byte-equal to the section's expected line; falsification failed. The one candidate-made staleness found is pointer #10 (leg-count progression 9 -> 10 since round 51).",
  "rekey_edit": "append '; `cases=10` since round 51' to the leg-count progression",
  "scratch": "/fast/scratch/hyaku/tameshi-r51/T51W2Read15 (deleted before yield)"
}
```
