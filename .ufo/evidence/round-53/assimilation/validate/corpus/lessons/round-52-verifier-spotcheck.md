# Tameshi round 52 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
lane_round: 52
lane HEAD verified: tameshi-shokunin@f1a3246105f75bb9f678f20e25878c44db3a2caf (branch master, local=remote, ahead=0)
base: ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
report: .ufo/reports/round-52/tameshi.md (fleet commit 53fdd5559419b5dcd137aa9f444a8afd8b9dec01, author tameshi-shokunin)
verdict: rejected-harmed (claims re-verify on the frozen counters; the frozen no-harm coldread floor is RED at the lane tip and un-repaired)

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-52/tameshi.md` (fleet repo) | `tameshi-shokunin tameshi@shokunin.local 53fdd555… "round-52: hyaku honest-stop report (run wrap-up)"` | pass |
| cited commits exist + ancestor of branch | `git merge-base --is-ancestor ef19d8e… master` ; `… f1a3246… master` | both exit 0; master = origin/master = f1a3246 | pass |
| lane pushed, no ahead | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin` | `branch=master local=f1a3246 remote=f1a3246 ahead=0 behind=0` | pass |
| uncommitted round work | `git -C …/tameshi-shokunin status --porcelain` | 4 untracked: `.ufo/evidence/round-52/integrate/build-readers.py`, `.ufo/waves/round-52/w3.ready`, `w3.ready.dispatched`, `w3/` | defect (status-neutral) |
| prompt carries template contract | read `.ufo/prompts/tameshi-round-52.md` | report path (§4), commit-before-report + SHONEN heading + hash-citation + write scope (§4 items 3–4) all present | pass |
| SHONEN heading in report | `grep -c '^## SHONEN'` + read | heading present, but ONE `[~]` line covers all four boxes (contract: one line per box) | defect (status-neutral) |
| dispatch evidence | `grep -n 'tameshi round=52' .ufo/watchdog.log` | `2026-10-27T00:52:16-03:00 launch tameshi round=52 pgid=1080098 driver=hyaku-inline attempt=1` ; `2026-10-27T04:23:10-03:00 complete tameshi round=52; hyaku-inline attempt=1` (matches digest in closure notes) | pass |
| report is real, not a marker | read full report | names lane tip f1a3246, candidate 7ff81a5, evidence pointers, claims, trends, SHONEN | pass (real report) |

Report defects (status-neutral, all named in MANIFEST notes): (a) body claims "written but not committed/pushed to the fleet repository" — false, the report is committed (53fdd555) and pushed; (b) no "Landed changes" section and no "Before → after measurements" section (minimum-content defect per the marker rule); (c) SHONEN one-line-for-four-boxes; (d) trend verdict `discernment: unprovable` is outside the allowed vocabulary; (e) LOG.md carries no round-52 entry, so the round's landed changes are not tied to a LOG.md entry as the report contract requires; (f) start census "133 rows" is not printed in `census-start.stdout` (only exit 0 + `ok`; 133 is inferred from 134 now minus S274 — consistent but unprinted); (g) w3-internal inconsistency: `T52W3CritAdmission.md` says "16/19 readers delivered" while 18 reader JSONs are committed (the report's "18" matches the bytes).

## Per-claim re-check

### C1 — operability (registry homes)

Lane status: NOT claimed (no frozen deciding run; probe at candidate only). Closure re-measurement:

- before (base, committed): `.ufo/evidence/round-52/before/c1-base-prefreeze.stdout` — pre-freeze draft run at base: `held=48/49 not_held=2 mte_row=1 c3_total=1 total=4`; the frozen contract's `before` prose said total=2 and the lane filed an erratum (counter arithmetic gives 4; predicate/target unchanged). Controls: 11/11 as pre-registered (`.ufo/evidence/round-52/control/controls.stdout`, last line `CONTROLS: total=11 unexpected=0`; independent critic seat re-counted 11 CONTROL lines).
- after (tip, re-measured by closure): `python3 .ufo/evidence/round-52/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev f1a3246105f75bb9f678f20e25878c44db3a2caf --work <scratch> --explain` (10m4s, read-only over git objects) → `C1_R52: rev=f1a3246… held=49/49 not_held=0 dropped=0 mte_row=0 c3_covered=30 c3_total=0 r21_cases_missing=0 total=0 C1_R52_PASS=true`, exit 0.
- committed probe evidence verified (not executed by closure): `.ufo/waves/round-52/w3/T52W3ExecC1Probe.stdout` at rev 7ff81a5b0ab0 (ancestor of tip; `git diff 7ff81a5..f1a3246` touches only `.ufo/` wave-3 files — no predicate-relevant byte changes).
- landed bytes: `tools/registry.json` mte-interop-check `9/9`→`10/10` + source re-pointed (diff vs base); `tools/round21-measure.py` reads its subject's FLEET root; SKILL.md corrections.

Verdict: **improved** — the falsifiable before→after re-derives on the frozen counter at the lane tip (closure re-measurement). Grading rests on the closure's own measurement because the lane's frozen deciding run never occurred (run wrap-up); the frozen counter, controls and kill rule are intact and were not narrowed after seats scored.

### C2 — calibration (closure-found false records)

Lane status: NOT claimed (probe at candidate only; wave-2 review reported over-counted records; deciding run never occurred). Closure re-measurement:

- before (base, committed): `.ufo/evidence/round-52/before/c2-at-base.stdout` — `m1=2 m2=1 m3=3 m4=20 m5=1 m6=0 total=27 C2_R52_PASS=false`; exit file `c2-at-base.exit` = 1.
- after (tip, re-measured by closure): `python3 .ufo/evidence/round-52/c2/measure.py --lane … --rev f1a3246… --explain` → all six checks ok, `total=0 C2_R52_PASS=true`, exit 0.
- committed probe evidence verified: `.ufo/waves/round-52/w3/T52W3ExecNoHarm-c2.out` at rev 7ff81a5, same result.
- caveat: the wave-2 review's over-count finding is itself overstated for its worked example. Independent closure seat re-derived Corr12 (`.ufo/waves/round-52/w2/T52W2RevCorr0912.md` vs `.ufo/evidence/round-51/coldread/reads/T51W2Read12.md`): the reviewer claimed "0 of 14" findings are reader-marked failures; observed ≥2 (strict `**drift**` rows) to 6 (reader's confirmed-drift/stale/false/incomplete marks) of 14, with selectively truncated line citations. The frozen counter's m4 (`wrong_expectations == len(findings)`, verbatim quotes) still holds — 14/14 quotes are substrings. See routed defect R52.4.

Verdict: axis **harmed** — not by the C2 record-set (which re-verifies) but by the frozen no-harm monitor below: the round's own edits dropped 19 cold-read sections at the tip and the re-key that would restore them never landed. The calibration axis is the one the round-21 cold-read monitor scores (8 at base, 64/64 credited).

### No-harm (frozen) — re-measured by closure

- Command: `bash .ufo/evidence/round-48/quality/coldread-precheck.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 f1a3246105f75bb9f678f20e25878c44db3a2caf` (read-only; reads git objects, scratch under HYAKU_SCRATCH).
- Observed: `COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=f1a3246105f75bb9f678f20e25878c44db3a2caf cand_credited=45 lost=19 RED`.
- Corroboration: committed receipts `precheck-cand0.stdout` (cand bcba892, 46 credited, lost 18 RED), `precheck-cand1.stdout` (cand 7ff81a5, 45 credited, lost 19 RED), and the w3 no-harm probe `.ufo/waves/round-52/w3/T52W3ExecNoHarm-noharm.out` (`coldread-floor score=6 credited=45 RED` at rev 7ff81a5). The other 10 no-harm monitors are ok (commandD 10, freshness 71/74, coverage monitors pass, tools-scope ok, registry rows 134).
- Re-key state: 18 reader JSONs committed (T52W3Read01–17, 19; Read18 absent) for 19 lost sections; no ledger entries carry T52 reader findings (C2 m6 reports `t52_entries=0`); `.ufo/evidence/round-52/after/` does not exist — the frozen deciding run never happened.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability (C1) | improved | closure re-measurement of the frozen counter at the tip: total 4 (base) → 0 (tip), 49/49 rows held; controls 11/11 as pre-registered; deciding run absent (run wrap-up) so the grade rests on the closure's measurement |
| calibration (C2) | harmed | the axis's own monitor (round-21 cold-read floor) is RED at the tip: 64 → 45 credited, 19 sections lost by the round's edits, re-key never landed; the C2 record-set itself re-verifies (total 27 → 0) |
| depth / coverage / freshness / adjacency | unchanged | no committed change to those axis surfaces this round (SCORECARD diff is a pre-registration entry only; freshness monitor ok at candidate) |

## Discernment spot-check (LEARNING.md — from outside)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S274 admit (Bazel Hermeticity) | admit, tier A, mined | live re-fetch `https://bazel.build/basics/hermeticity.md` (HTTP 200, 5878 B) sha256 `2355150f…bbc6` — byte-identical to the committed snapshot `.ufo/waves/round-52/w1/T52W1ScribeSource-snapshot.txt`; quote at snapshot lines 12-14 present verbatim ("a hermetic build system always returns the same output by isolating the build from changes to the host system", 18 words ≤ 25); second quote lines 28-29 present; second seat re-fetch recorded in the row | agree | source supports exactly the scoped claim (fleet-bound self-test has an undeclared host input; applied by analogy, which the lesson discloses) |
| Wave-1 kill-note supersession variant | reject (duplicate of the landed line) | `corpus/knowledge/fleet-kill-rate-ledger.md:439-441` landed supersession line (names drift-pins, "unmeasured by sweep", "supersed", "case 10"); frozen m5 rule text in `.ufo/evidence/round-52/c2/measure.py` | agree | the landed line already satisfies the frozen m5 rule with the same pointers; my C2 re-run at the tip shows `m5 ok row=1 note=True`; landing a second variant would be a duplicate |
| SOURCES row S274 (new row quote check) | row written | `corpus/SOURCES.md:149` | agree | row well-formed (11 columns), teaches-cell claim grounded in the snapshot; census validate exit 0 |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0 (warnings only, no E-code findings).

## Trend verdicts

- expansion: **unchanged** — one tier-A row (S274) opened and mined by the round lesson, but no new admitted `knowledge/` entry on uncovered coverage-map ground and no capability admitted; the sourced C1 claim it supports is not admitted this round.
- quality: **harmed** — the frozen no-harm coldread floor is RED at the lane tip (64 → 45 credited, 19 lost) and the re-key that would repair it never landed; the lane's own report grades this harmed and the closure's independent re-run confirms it at the tip.
- discernment: **improved** — the non-author spot-check agrees with the gate on the sampled admit (S274) and reject (supersession duplicate); QUALITY criterion 103 entered with the `## Mistakes` row and a falsifier that fails at base behind it; the wave-2 over-count review's own inaccuracy (Corr12) was caught by the closure's independent seat and is routed below, so the disagreement is learned, not left standing.

## Routed defects (lane must fix next round)

1. **R52.1 coldread re-key debt.** 19 sections lost credit at the tip; 18/19 reader JSONs committed (Read18 missing), no T52 ledger entries, no frozen deciding receipts. Re-run the frozen re-key/deciding pipeline per `.ufo/evidence/round-52/deciding-run.sh` and the contract kill rule, or record an honest stop again.
2. **R52.2 LOG.md round-52 entry missing.** The round's landed changes are not tied to a LOG.md entry (report contract). Append (never rewrite) the round-52 entry naming the commits bcba892 → f1a3246 and the wrap-up disposition.
3. **R52.3 over-count review overstated (this closure's finding).** `T52W2RevCorr0912.md` claims "0 of 14" reader-marked failures for Corr12; independent re-derivation found ≥2–6 with selectively truncated citations. Re-derive the "8 over-count" verdict for records 01, 02, 06, 09–13 under one written counting rule (reader-marked drift at CAND; exclude `holds-hist` rows per the record's own §3) and correct the lesson row if warranted; consider a QUALITY criterion for reviewer-seat quote truncation.
4. **R52.4 uncommitted round work.** 4 untracked files (`.ufo/evidence/round-52/integrate/build-readers.py`, `.ufo/waves/round-52/w3.ready`, `w3.ready.dispatched`, `w3/`): commit under the round-53 entry or revert; a lane repo must not carry uncommitted round work into the next round.
5. **R52.5 hard-coded `/tmp` in `tools/registry-check.py:766`** (lesson self-routed, scratch directive §7.4): honour TMPDIR/a scratch argument next round.
6. **R52.6 report-contract repairs.** Add per-box SHONEN lines; add Landed changes and Before → after sections (or their accepted equivalents); fix the false "not committed/pushed" sentence in future reports; keep trend verdicts inside the allowed vocabulary.

## Closure disposition

Rejected-harmed, not admitted: both declared claims re-verify on the frozen counters at the lane tip (closure-measured), but the calibration axis is harmed (coldread floor RED at tip, un-repaired), and admission requires no axis harmed. The honest-stop report is real and accurate in its core claims; its defects are conformance-level and routed. The next steered round should carry R52.1–R52.6.
