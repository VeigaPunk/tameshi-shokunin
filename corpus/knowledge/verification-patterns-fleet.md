<!-- corpus entry — tameshi-shokunin probation wave 1, lane TAMESHI-3 (cross-fleet
verification-pattern census), finished 2026-10-14. Assignment: read kaidoku-shokunin's
audit-lane pattern (corpus verify:-line re-runs, bit-exact evidence ids) and the game
lanes' verifier-AGREE loops (fleet root .ufo/waves/shokunin-train-20261014-w6..w8 closeout
artifacts); extract repeated vs lane-specific patterns. Writes: ONLY this file (assignment
named it). LOG.md append left to the parent — lane dispatch write scope overrides ambient
append rules, the documented known-gap precedent (kaidoku-shokunin/corpus/knowledge/
2026-10-14-r14-02-final-sweep.md:6-8). Substrates read read-only: kaidoku-shokunin/,
audio-shokunin/, game-dev-2d-shokunin/, game-dev-3d-shokunin/, .ufo/ (waves, reports),
fleet root docs (PROTOCOL.md, AXES.md), ~/Projects/prymeagnt/* (report dirs listed only).
Secrets: none read; no credential material or env contents touched. Baseline at lane
start: corpus/knowledge/ empty (`ls` returned no files, this lane). -->

# verification-patterns-fleet — census: the shared verifier shape (independent non-author replay on committed/retained state) vs two lane-specific encodings (kaidoku audit blocks; game AGREE tally)

Admission-bar use (corpus/QUALITY.md:3-8): every claim below carries a path:line anchor or a command output from this lane; observation/inference/unknown are labeled; a pattern is called **general** only with evidence from two independent lanes (PROVINCE.md:15-16: "a pattern is admitted from evidence in TWO independent lanes before it is claimed general").

Axes: **pattern-generality** (≥2-lane rule as the general/lane-specific divider) / **anchor-density** (each pattern cited to file:line or command) / **separation** (general vs lane-specific kept apart; observations vs inferences labeled).

Method (all read-only): kaidoku corpus entries 2026-10-14-r14-02 (full), 2026-10-14-r12-02, 2026-10-14-r9-02, 2026-10-13-r4u-05 + corpus/README.md + corpus/QUALITY.md + SCORECARD.md; .ufo/waves/kaidoku-r5/{01-audit-A,02-audit-B}.md; .ufo/waves/shokunin-train-20261014-w6..w8 (closeout.json, spec.json, tasks/*, xsentinel-report.md, xconnector-report.md); lane logs audio-shokunin/LOG.md, game-dev-2d-shokunin/LOG.md, game-dev-3d-shokunin/LOG.md; verifier report game-dev-2d-shokunin/reports/round-68/r68-verifier.md; .ufo/reports/round-68, round-69, round-77. All commands under "Verification (this lane)".

## 1. General patterns — repeated across ≥2 independent lanes (game lanes = audio/g2d/g3d; kaidoku = the audit lane)

### P1 — A declared falsifiable claim exists BEFORE the move (OBSERVATION)
- game: every seat brief opens with "Declared axis-move (verbatim): … Declared falsifiable claim: …" `.ufo/waves/shokunin-train-20261014-w6/tasks/g2d-reviewer.txt:8` (same template, e.g. `.ufo/waves/shokunin-train-20261014-w6/tasks/audio-scout.txt:8`); wave context binds "Falsified claims are useful rounds — report measured outcomes honestly" and "Evidence or it didn't happen" `.ufo/waves/shokunin-train-20261014-w6/spec.json:3`.
- kaidoku: candidate blocks pair a claim with its re-run recipe — `- verify: …` / `- verified-at: …` / `- suggested: admit` (kaidoku-shokunin/corpus/knowledge/2026-10-13-r4u-05-wakaru-oom.md:55-61; 2026-10-14-r12-02-queue-b-ledger.md:57-63).

### P2 — The verifier is a named NON-AUTHOR replaying the committed/retained state, not the author's prose (OBSERVATION)
- game: "Seat: verifier (named, independent, NON-AUTHOR). Verified the committed tree, not the author's claims." — game-dev-2d-shokunin/reports/round-68/r68-verifier.md:1-5; committed file hashes re-pinned before any run and matched to the author's declared post-diff hashes (r68-verifier.md:6-9).
- kaidoku: audit verdict logic "UNVERIFIABLE = cannot re-run or no evidence either way. Sha256 pins checked first" .ufo/waves/kaidoku-r5/01-audit-A.md:12; "Live re-runs could therefore be compared byte-for-byte against r4's retained outputs, not just re-executed" .ufo/waves/kaidoku-r5/02-audit-B.md:13-14.

### P3 — Byte-identity / exact-id equality is the top verdict class; volatile fields are scrubbed by an explicit list (OBSERVATION)
- game: "0 mismatches in all five comparisons" after scrubbing pids, elapsed/timing fields, run-dir paths, ASLR addresses, concat interleave order, a 4th-decimal wobble — and the one line-reference drift is recorded in a field named `provenance_only_line_diff` (game-dev-2d-shokunin/reports/round-68/r68-verifier.md:11-23).
- kaidoku: "Eight compare invocations reproduced byte-identical" including a 63 MB request (02-audit-B.md:41, :36); re-runs re-mint ids exactly (`ev_f4e02f93…` :78; `ev_294a449c…`, 79,955 B exactly :93); "r5 audits re-executed recipes, not just read them — 8/8 compare outputs byte-identical incl. a 63 MB request" kaidoku-shokunin/SCORECARD.md:37.
- INFERENCE: identity claim strength = the id's full domain `f(content, path, params)` (kaidoku-shokunin/corpus/QUALITY.md:24: same bytes at a different path are not the same id) — one r9-02 observation (renamed byte-copy minting the same id) is flagged unresolved, U4.

### P4 — Prior rows/ledgers must stay stable (regression fence) (OBSERVATION)
- game: "prior rows 0-mismatch ×5 comparisons" and "No axis harmed — flagless 88/88 unchanged" .ufo/reports/round-68/game-dev-2d.md:32-33; audio r67 verifier "112 rows + prior-102 byte-identical" audio-shokunin/LOG.md:1014.
- kaidoku: "all 102 prior ledger rows + receipts byte-stable" declared as the move's own invariant `.ufo/waves/shokunin-train-20261014-w6/spec.json:15` (audio r67 author prompt); corpus discipline "audited bit-exact or VERIFIED with errata appended, never rewritten" kaidoku-shokunin/corpus/knowledge/2026-10-14-r14-02-final-sweep.md:176-177.

### P5 — Verdict is tallied and attributed to a named non-author verifier (OBSERVATION)
- fleet protocol: "`[x]` only with a named non-author verifier" PROTOCOL.md:430-431 (tameshi SHONEN.md:14 pins this line); kaidoku reads the same mark spec for its four gate lines (r14-02:99-103).
- game: closeout.json records `"verifier": "AGREE 5/5"` per lane (.ufo/waves/shokunin-train-20261014-w6/closeout.json:10,19,28; w7 same lines; w8:10 and :28 "AGREE 6/6", :19 "AGREE 5/5"); naming lives in the LOG: "Non-author `reports/round-68/r68-verifier.md`: **AGREE 5/5**" game-dev-2d-shokunin/LOG.md:722; audio r69 "AGREE 6/6" audio-shokunin/LOG.md:1099; g3d r77 "AGREE 6/6 … prior-163 0-mismatch vs r76 verifier receipt" game-dev-3d-shokunin/LOG.md:891-894.
- kaidoku: every round carries "audit VERIFIED ×2" (two independent audit lanes) kaidoku-shokunin/SCORECARD.md:73-81; the audit lanes exist as literal reports 01-audit-A / 02-audit-B / 03-audit-C under .ufo/waves/kaidoku-r5/.

### P6 — Falsification is a first-class outcome, recorded as the finding, never softened (OBSERVATION)
- game: w7 audio closeout note "declared claim falsified-as-stated: post-table fork = named axis …" .ufo/waves/shokunin-train-20261014-w7/closeout.json:12; "Critic falsifications absorbed: declared bound is a write-position bound not a nominal-offset one" .ufo/reports/round-68/game-dev-2d.md:11; r64 verifier "claims 2,3,4a,4b AGREE; 1+5 DISAGREE-as-worded pre-fix → resolved by landing the verified bytes" game-dev-2d-shokunin/LOG.md:615.
- kaidoku: audits report defective recipes rather than hide them — "Defective/weak verify recipes (file 06) … re-ran it anyway (~3 min warm cache), all headline numbers reproduced" 01-audit-A.md:131-133; a new phantom-class id is "REPORTED, not fixed — PROVINCE.md is not this lane's file" r14-02:132-142; errata are append-only (r14-02:176-177).

### P7 — Anything changed after verification must carry its own proof (OBSERVATION)
- game: "simplifier flags applied post-verifier on both lanes … all byte-identical-proven, batteries re-run green" .ufo/waves/shokunin-train-20261014-w8/closeout.json:37; w7 "_check_tuple consolidation … applied as 8a67f71 with own 163/163 re-verification" w7/closeout.json:35; "post-verifier `e8d4fb7` is byte-identical-proven" .ufo/reports/round-68/game-dev-2d.md:32.
- kaidoku: rounds "audited bit-exact or VERIFIED with errata appended, never rewritten" r14-02:176-177; post-repair check re-run in one command with before-counts (r14-02:181-186).

### P8 — The verifier catches defects the author missed, against the record (OBSERVATION; mechanisms differ per lane)
- game (integration, not prose): "Integration defect: work commit `a32920b` omitted the runner diff (verifier-caught); fix commit `5265da6` landed the exact verified blob `66a18a00`" game-dev-2d-shokunin/LOG.md:614.
- kaidoku (record, not code): "Defective recipes were caught and patched: 2 in r2 (`LOG.md:17-18`), `grep -c`→`grep -o|wc -l` (`corpus/QUALITY.md:23`)" kaidoku-shokunin/SCORECARD.md:37.
- INFERENCE: the shared property is "replay against the artifact, not the claim"; the class of defect caught (integration blob vs written recipe) is lane-specific.

### P9 — Writers are scope-partitioned and receipts are retained so a replay is possible (OBSERVATION)
- game: "Write only your own report file and scratch inside your brief's write scope" .ufo/waves/shokunin-train-20261014-w6/tasks/g2d-reviewer.txt:16; verifier runs its own instrumented runs under disjoint scratch `corpus/live/r68-verifier/runs` (r68-verifier.md:3,11-13).
- kaidoku: entry header records assigned writes, namespaced scratch, and read-only substrates (r14-02:5-12); the lane ends with "`git status --porcelain` … shows exactly: `M corpus/README.md` + `?? corpus/knowledge/2026-10-14-r14-02-final-sweep.md` — the two assigned writes, nothing else" r14-02:186.

### P10 — A cross-lane adversarial layer audits hygiene/adjacency and reports findings, never fixes siblings (OBSERVATION)
- game: xsentinel census re-checks the prior wave's findings and files F1..F5 with evidence + smallest remediation + owner, e.g. the g3d r77 baseline violation (frozen tree, not archive) .ufo/waves/shokunin-train-20261014-w8/xsentinel-report.md:6-8, :31; closeout records "xsentinel findings handled: F4 …, F7 …" and "xconnector transfers recorded for wave 9" w8/closeout.json:38-39.
- kaidoku: mechanical checks 1/2/5/8 re-run against the current tree with PASS/FAIL per check r14-02:67-76; fleet-level residual reported up, not absorbed — "Two fleet-level residuals remain outside lane writ" r14-02:166-169; tameshi PROVINCE.md:20 states the same rule "Out of province → report, never absorb" (adjacency axis AXES.md:15).

## 2. Lane-specific encodings (single-lane evidence — NOT yet general per PROVINCE.md:15-16)

kaidoku — the audit-block encoding:
- Entry grammar: provenance HTML-comment header → Axes → "## Candidate:" blocks with `- claim:` (often labeled OBSERVATION) / `- verify:` (a runnable recipe) / `- verified-at:` (lane, shell/run ids) / `- suggested: admit` (r4u-05:55-61, r9-02:1-8 and :24-40, r12-02:57-63).
- corpus/README.md coverage-map row idiom `| knowledge/<name> | <gist> | <verify> |` (r14-02:50-53); map integrity via programmatic set-diff, tokens 56→70 (r14-02:63-65). Measured now: 72 knowledge files; 468 `verify:` vs 467 `verified-at:` occurrences, 4 files with unequal counts (U1).
- Audit lanes A/B/C with verdict vocabulary CONFIRMED / UNVERIFIABLE (01-audit-A.md:12), one round's "audit VERIFIED ×2" as the standing record (SCORECARD.md:73-81).
- Evidence-id identity domain `f(content, path, params)` (corpus/QUALITY.md:24); phantom-id class + cross-citation health chase (r14-02:121-142; SCORECARD.md:79 `ev_4898906e` corrected to `ev_5cb1856a`).
- 3-run content-address proof (SCORECARD.md:76; r9-02:1-8 header "byte-identical re-runs … all nine pinned digests byte-identical before/after").

game lanes — the AGREE-tally encoding:
- Seat set: 8 seats {scout, author, critic, reviewer, simplifier, scribe, baseline, boundary} + named non-author verifier + Sol adjudicator (game-dev-2d-shokunin/LOG.md:631, :636 "Per-axis verdicts (Sol `reports/round-66/r66-adjudicator.md`): **ADMIT**"; audio-shokunin/LOG.md:1010; game-dev-3d-shokunin/LOG.md:860).
- AGREE N/N = claim families / row-batteries replayed: r68 "AGREE 5/5 on `f754546` (prior rows 0-mismatch ×5 comparisons …)" .ufo/reports/round-68/game-dev-2d.md:32; r69 "AGREE 6/6 on `30bb86d` (119-row replay, verbatim member rebuilds, census independently reproduced)" .ufo/reports/round-69/audio.md:33; r77 "AGREE 6/6 on `35dfbe2` (own-geometry probe both directions; jitter reproduced 6/10-vs-4/10; 173×12 + prior-163×12 zero-mismatch)" .ufo/reports/round-77/game-dev-3d.md:33. INFERENCE: denominator = number of claim families; no w6-w8 artifact states the fraction's definition (U2).
- closeout.json schema: `wave` / `lanes{round, verdict, work, report_last, verifier, seats, note}` / `events` (w6/w7/w8 closeout.json).
- Metric unit = battery rows + discriminations, with additive-only rule: "flagless 88/88 unchanged; classifiers byte-identical since r65; upgrades opt-in flagged" .ufo/reports/round-68/game-dev-2d.md:33 and :25-27 (24 discriminations); g3d r77 "173/173 + 4 probes + Node 31/31; 163 prior rows byte-stable vs the r76 verifier's independent receipt" .ufo/reports/round-77/game-dev-3d.md:7.
- Nondeterministic edges carry measured distributions, e.g. "Nondeterministic edges now carry measured distributions" w8/closeout.json:34; jittered cell pinned/withdrawn accordingly (same line).
- Baseline freeze via `git archive HEAD`, tracked files only, no populated-tree re-archiving — brief mandate .ufo/waves/shokunin-train-20261014-w6/tasks/g2d-reviewer.txt:21; violation was this wave's xsentinel F1 (xsentinel-report.md:31 findings section).
- Sol adjudication renders per-axis verdicts in fleet vocabulary "improved locally / unchanged" (game-dev-2d-shokunin/LOG.md:636; axes table AXES.md:5-13).

## 3. Falsifiable predictions for tameshi's next rounds (INFERENCE)
- w9 (if/when it closes) should produce the same closeout schema with an `AGREE` field; a differing schema or missing field falsifies "schema is stable since w6".
- U1 (4 verify:/verified-at: count-mismatched files) is decidable by reading those 4 entries; predicts they are formatting variants, not missing evidence.
- U2 (AGREE denominator) is decidable by counting "### Claim" headings in any `reports/round-N/rN-verifier.md`; predicts the count equals N in the LOG tally.

## Verification (this lane)
- `ls kaidoku-shokunin/corpus/knowledge/*.md | wc -l` → 72.
- `grep -rn "verify:" kaidoku-shokunin/corpus/knowledge/*.md | wc -l` → 468; `grep -rn "verified-at:" …` → 467; per-file mismatches: 2026-10-13-r2-firmware-probe 7/6, 2026-10-13-r3-keyed-archive-carriers 3/4, 2026-10-13-r4u-05-wakaru-oom 3/4, 2026-10-13-r5-01-riscv-bypass 9/7.
- `grep -o '"verifier": "AGREE [0-9]/[0-9]"' .ufo/waves/shokunin-train-20261014-w{6,7,8}/closeout.json | sort | uniq -c` → w6 3×5/5; w7 3×5/5; w8 2×6/6 + 1×5/5 (w8 g2d = 5/5).
- `grep -n '"verdict"\|"verifier"\|"seats"' …/closeout.json` → w6 lines 7/10/11, 16/19/20, 25/28/29; w8 :10 "AGREE 6/6", :19 "AGREE 5/5", :28 "AGREE 6/6".
- Verifier semantics read verbatim: game-dev-2d-shokunin/reports/round-68/r68-verifier.md:1-9 (non-author statement + hash re-pin).
- Post-write state check (lane end): `git -C tameshi-shokunin status --porcelain` → `?? corpus/knowledge/` (directory untracked; it holds this file plus two sibling-lane files this lane did not write — gates-survey-kagi.md, gates-survey-kumitate.md). `wc -l` of this file → 105.

## Unknowns / not done
- U1 — four files with unequal `verify:` / `verified-at:` counts; not chased (may be wrapping/phrasing variants).
- U2 — the AGREE fraction's denominator: inferred as claim families; no w6-w8 artifact defines it.
- U3 — verifier identity: closeout.json records the verdict but not a verifier id; whether an id is mandatory was not checked.
- U4 — ev-id nuance: r9-02 header (renamed byte-copy, same id) vs QUALITY.md:24 path-sensitivity and 02-audit-B.md:78 path+content binding — unresolved this lane.
- U5 — w2-w5 waves have no closeout.json at all; the AGREE field first appears in w6 — earlier record forms not investigated.
- U6 — sampling: one verifier report read in full (g2d r68); other waves via LOG/report summaries; kaidoku audits A/B read, C/consistency only partially.
- U7 — Sol adjudicator reports and promotion gates skimmed only; outside this census's output.
- Errata: none yet (append-only; this is the file's first version).
<!-- corpus entry (extension) — tameshi-shokunin round 2, lane TAMESHI-R2-4, appended 2026-10-14. Assignment: read the game-dev-2d-shokunin verifier machinery (verifier scratch under corpus/live/rNN-*-verifier*/, SCORECARD.md / LOG.md AGREE loop, reports/round-NN/rNN-verifier.md) and document its mutation/verification discipline as the census's fourth pattern. Append-only: everything above this comment is byte-untouched; this lane wrote ONLY this file (LOG.md append left to the parent — same known-gap precedent as :5-8). Substrate read read-only: game-dev-2d-shokunin/ (LOG.md, SCORECARD.md, reports/, corpus/); secrets: none read. Commands under "Verification (extension)". -->

## 4. Fourth pattern (appended 2026-10-14, TAMESHI-R2-4) — game-dev-2d-shokunin verifier machinery: the mutation/verification discipline

The census holds three pattern blocks so far: the shared verifier shape P1–P10 (§1) and two lane-specific encodings (§2: kaidoku audit blocks; game-lanes AGREE tally). This is the fourth: the machinery-level discipline underneath game-dev-2d's AGREE tally — how its verifier replays, how mutations are run, and where falsification goes. It complements §2 (:76-83 records the tally's vocabulary/seat set/schema), not restates it. Single-lane evidence (game-dev-2d-shokunin only) — NOT general per PROVINCE.md:15-16; labels as §1 (OBSERVATION / INFERENCE / UNKNOWN); sub-ids D1–D10 avoid colliding with P1–P10.

### D0 — The loop, restated with the lane's own anchors (OBSERVATION)
- Wave form: 8-seat leaf wave (`reports/round-NN/rNN-{scout,author,critic,reviewer,simplifier,scribe,baseline,boundary}.md`, disjoint scratch, sole tracked writer = author) → wave-2 named non-author verifier → Sol per-axis adjudicator → ADMIT/HOLD → report-last commit. game-dev-2d-shokunin/LOG.md:611 (r64 wave), :631 (r66, "+ non-author verifier"), :722 (r68 "**AGREE 5/5** on `f754546`").
- Verdict language is per-claim AGREE / DISAGREE-as-worded: r62 "**AGREE on all checked claims**" LOG.md:595; r63 "**AGREE on all five claims**" LOG.md:605; r64 "claims 2,3,4a,4b AGREE; 1+5 DISAGREE-as-worded pre-fix → resolved by landing the verified bytes" LOG.md:615.
- Same shape through r68; r69's verifier seat died and the record says so (see D8). Lane-log counts (this lane's commands below): 9 `AGREE` / 1 `DISAGREE` lines in LOG.md.

### D1 — The verifier replays committed BYTES; if the commit lacks the change, that is the finding (OBSERVATION)
- r64: work commit `a32920b` "does NOT contain the proposed mutation" — it touches 858 files, all `corpus/live/`/`reports/` (`git show … | grep -vc …` → 0); `a32920b:corpus/fixtures/run_battery.py` sha256 byte-identical to parent `a7e0cb1`; the gate code existed only as uncommitted worktree state (sha `66a18a00…`) game-dev-2d-shokunin/reports/round-64/r64-verifier.md:11-19.
- The verifier materialized the committed tree into `corpus/live/r64-verifier/pretree/fixtures/` and ran the mandated battery against it → exit 0, PASS 96/96, NO `probe_while_live_signature_gate` row (receipt `pretree-runs/20261014T021648730172Z/verdicts.json`) r64-verifier.md:26-31; verdicts: claim 1 DISAGREE as worded (:35), claim 5 mutation scope DISAGREE (:102), "**Claims 2, 3, 4: AGREE. Claims 1 and 5: DISAGREE**" (:136).
- Routine rounds check provenance up front: "Executed runner == committed blob … The bytes I executed ARE the committed bytes" reports/round-65/r65-verifier.md:10-18; r68 "Committed file identity re-pinned before any run … byte-equal to the author's declared post-diff hashes" reports/round-68/r68-verifier.md:5-9.
- r68 also proves no tracked writes: `git status corpus/fixtures/` empty before AND after all replays; the battery copies fixtures into `runs/<stamp>/scratch` (corpus/fixtures/run_battery.py:124-142) and writes only there; `corpus/knowledge/seed.md` untouched r68-verifier.md:132-139.
- Closing record: fix commit `5265da6` "landed the exact verified blob `66a18a00`" LOG.md:614.

### D2 — Mutants and faults are scratch-only fixtures of the runner itself (OBSERVATION)
- `--probe-failing` = "also mutate scratch scene B and prove detection" corpus/fixtures/run_battery.py:110; implementation edits the scratch copy (`scratch/scene_b.tscn`, marker `"B"`→`"BROKEN"`) and executes `mutant_broken_scene_route` (expects exit 2 + `chain incomplete`) and `mutant_level_collision_removed` run_battery.py:2423-2429.
- r1: "targeted broken-scene mutation with exit 2 and `chain incomplete`" LOG.md:12; the named non-author "independently reran 15/15 PASS, confirmed targeted exit-2 mutant" LOG.md:14.
- Mutants are counted inside battery totals: "31 base CASES + 2 scratch mutations = 33 ordinary records" LOG.md:162; "50/50 PASS = 39 ordinary + 2 mutants + 9 opt-in" LOG.md:264.
- `--fault-injection` is a separate isolated probe family ("isolated executor fault probes (separate from seeded battery)") run_battery.py:111; its raw record keeps deliberate inner FAILs — r23: "inner hang and unrelated diagnostic remain deliberate FAIL; raw `r23-fault-verifier.json`" LOG.md:232.

### D3 — Suite sensitivity is proven by DISABLING the guard in a disposable copy: the intended assertion must FAIL (OBSERVATION)
- r9: "Verifier disabled shared unrelated-error filtering in disposable scratch runner: all four probe meta verdicts FAIL and battery exit 1" LOG.md:89.
- r11: "Two disposable `/tmp` sabotages (disable ERROR filter or suppress extra emission) each make meta FAIL/overall exit 1" LOG.md:109.
- r14: "Scratch disable-warning-check runner mutation makes meta and battery FAIL" LOG.md:141.
- r16: "Scratch-only expected-low-bound and receipt-list saboteurs each fail at clamp assertion" LOG.md:162; r23/r24: "Disposable scratch sabotage of authored limit similarly failed intended assertion" LOG.md:232, :242.
- A dedicated wave seat exists for this: `mutation-reviewer` — r20 "read-only mutation sensitivity plan, own scratch only" LOG.md:197; r23 "scratch-only authored-left sabotage" LOG.md:227; r24 (:237); r27 (:269).
- INFERENCE: the discipline is per-guard binary (disable the mechanism → the intended failure must surface), not a defect-corpus kill rate; no survived/killed tally was found (U8). Contrast: tameshi's round-2 plan measures a kill-rate on kumitate kimi-census (tameshi-shokunin/plans/round-2.plan.md:3-9), and the kumitate survey found "no kill-rate harness; no fault injection against the gate's own code" there (tameshi-shokunin/corpus/knowledge/gates-survey-kumitate.md:59-61, :278-281). D3 is the "binary guard-disable" tier a mutation bar can cite.

### D4 — A detected mutant must survive spoof attempts; engine errors never count as detection (OBSERVATION)
- `classify_mutant` requires the mutant's exact expected signature AND the positive PASS string absent run_battery.py:367-379; with `--probe-unrelated-error` the mutant is re-classified against injected-line, same-line-suffix and same-line-prefix spoofs, and the probe verdicts PASS only if `detected and not injected_detected and not suffix_detected and not prefix_detected` run_battery.py:381-390.
- "A script/parse error never counts as intended mutant detection" run_battery.py:451-453.
- Meta discrimination counts ride with the verdicts: r65 "29/29 discriminations" SCORECARD.md:34; r68 "discriminations 20→24 all True" SCORECARD.md:61 and "24/24 discriminations" SCORECARD.md:64.

### D5 — Flagged probes are opt-in and proven inert when unflagged (OBSERVATION)
- r68: flagless run dir contains NO `midlineforge-ladder-verdicts.json` and NO `probe_midlineforge_ladder` row; grep of flagless stdout finds zero `midline-offset` references; bare midlineforge arm unchanged r68-verifier.md:132-138.
- "opt-in flags only; flagless 88/88 unchanged; classifiers byte-identical since r65" SCORECARD.md:62; r67 "additive probe … prior 88 rows stable" SCORECARD.md:52.

### D6 — The verifier writes its OWN instruments and recomputes from spec, not from the author's mirrors (OBSERVATION)
- r68: own timing spike `corpus/live/r68-verifier/spike/proj/v_timing_probe.gd` + `run_timing.py`, "independent of the author's spike", 33 runs, own numbers (gap 200–201 ms; effective nominal bound ≈[0,~198)) r68-verifier.md:59-75.
- Clause map recomputed by `corpus/live/r68-verifier/recompute_clauses.py` — "my own reimplementation of both classifiers' clause logic …, not run_battery's mirrors" — 9/9 rows r68-verifier.md:84-93.
- Cross-run row comparison via `corpus/live/r68-verifier/compare_verdicts.py`; "0 mismatches in all five comparisons" after an explicit volatile scrub list (pids, elapsed/timing fields, run-dir paths, ASLR addresses, concat interleave order, a 4th-decimal wobble, one `provenance_only_line_diff`) r68-verifier.md:19-29.

### D7 — The regression fence is a field-tuple row diff against prior receipts (OBSERVATION)
- 7-field criterion (script, flags, expected_exit, actual_exit, signature, verdict, error) r68-verifier.md:19-21.
- r65 "97 prior rows 0-mismatch on 7-field tuples, own `/proc` corroboration" SCORECARD.md:34; r67 "prior 88 rows stable" SCORECARD.md:52; r68 "prior 0-mismatch ×5" SCORECARD.md:64.

### D8 — Falsification and failed verification are first-class, kept in the record (OBSERVATION)
- r64 DISAGREE-as-worded → "resolved by landing the verified bytes" LOG.md:615; SCORECARD.md:24 ("1+5 DISAGREE-as-worded on pre-fix commit `a32920b` … resolved by follow-up commit landing the verified blob").
- r68: declared grid "falsified as written (~80× resolution overstated — critic) and recorded honestly; the measured bound … is what landed" SCORECARD.md:64.
- r69: verifier seat "never survived rate limits" (5 respawns) — operator adjudicator replay recorded instead LOG.md:744-746, :771-773; SCORECARD.md:74.
- r27: a critic scratch mutation false-passed — recorded as "an adverse limit on arbitrary mutated-fixture provenance, not present in tracked source" LOG.md:270; "Do not claim arbitrary mutation resistance or signal provenance under malicious fixture edits" LOG.md:273; the later verifier confirms the tracked fixture "contains neither direct receiver invocation nor manual `pressed.emit`" LOG.md:274.
- INFERENCE: mutation evidence is scoped to the tracked source's real code path; a mutation that only works by rewriting the fixture is not admitted as evidence about the source.

### D9 — Receipts: where a replay can find them (OBSERVATION; one INFERENCE)
- Latest form is retained in-tree verifier scratch: at read time `corpus/live/r68-verifier/` holds 3 timestamped run dirs, per-flag battery stdout/stderr, `compare_verdicts.py`, `recompute_clauses.py`, `spike/`, `fixtures-status-before/mid.txt`; r64's scratch holds `pretree/fixtures/` + `pretree-runs/` (this lane's `find`, below).
- `corpus/lessons/` carries per-round receipts `rN-…-verifier.json` (early era) then `rN-…-non-author.json`; the listing shows 107 such files, spanning r2–r61 (last: `r61-crash-non-author.json`; none r62+ there) — commands below.
- INFERENCE: the receipt form migrated from lessons-JSON to in-tree scratch + report tables somewhere r62–r68; the exact migration commit was not chased (U9).
- Path caveat for other census lanes: older LOG entries write paths as `.shokunin/game-dev-2d/corpus/fixtures/run_battery.py`; the current repo root has no `.shokunin/` dir and the file is `corpus/fixtures/run_battery.py`; the lane worktree was reached via symlink `~/Projects/prymeagnt/game-dev-2d/.shokunin/game-dev-2d` → `/home/vgpnk/Projects/shokunin/game-dev-2d-shokunin` (r64-verifier.md:4-6). Drop the `.shokunin/game-dev-2d/` prefix for repo-root anchors.
- Report-form note: `reports/` mixes flat `rN-*` files (max flat round = r59) with 11 `round-NN/` dirs (round-60…round-70); the r70 dir was empty at read (`ls`, below).

### D10 — The verifier declares its own bounds and non-writes (OBSERVATION)
- r68: "No commits, no tracked-file writes, no subagents. Scratch only under `corpus/live/r68-verifier/`." r68-verifier.md:151-152; "Bounds of this verification" block at :141-150.
- r64: "No commits/push/merge/stash/checkout; wrote only this report + `corpus/live/r64-verifier/`" r64-verifier.md:5-8.

### Predictions from this block (INFERENCE)
- The next admitted round should carry `reports/round-NN/rNN-verifier.md` with per-claim AGREE/DISAGREE on a named commit; a round admitted without one falsifies D0/D1 as stated. (At append time `reports/round-70/` exists but is empty; r70 scratch dirs are untracked — observation.)
- If a future verifier report omits the "executed bytes == committed bytes" provenance check or the prior-row 0-mismatch statement, the loop has drifted.

### Verification (extension)
- `wc -l` LOG.md → 778; `grep -c 'AGREE'` → 9; `grep -c 'DISAGREE'` → 1; `grep -n "AGREE" … | tail` → :667, :722.
- `grep -n "HEADLINE\|DISAGREE\|materialized"` reports/round-64/r64-verifier.md → :11, :27, :35, :102, :136.
- `find corpus/live/r68-verifier -maxdepth 2` → 3 run dirs + `compare_verdicts.py` + `recompute_clauses.py` + `spike/` (`run_timing.py`, `timing-results.json`) + `battery*/fixtures-status*.txt`; `find corpus/live -maxdepth 1 -name '*verifier*' | wc -l` → 51.
- `ls corpus/lessons | grep -icE 'verifier|non-author'` → 107 (r2…r61; last `r61-crash-non-author.json`).
- `ls reports | grep -cE '^r[0-9]+-'` → 428; `ls reports | grep -cE '^round-'` → 11; max flat round r59 (ls pipeline).
- `git -C game-dev-2d-shokunin rev-parse HEAD` → `9fb50aa992cca6cb0bb1ce51ed2f891c09d85abb` ("r69 report-last: ADMIT — gap-relative referent pinned by crossed cells"); `git status --porcelain` → 15 lines: 13 untracked `corpus/live/{r69,r70}-*/` scratch dirs + 2 untracked reports (`reports/round-68/r68-boundary.md`, `reports/round-68/r68-verifier.md`).
- Post-write state check (lane end): recorded in the appended lane-end note below.

### Unknowns (extension)
- U8 — no survived/killed defect corpus or kill-rate metric found in this lane; its sabotage evidence is binary per guard. Whether any earlier round ran one was not exhaustively searched (grep scope: `mutation|mutant|sabotage`).
- U9 — the receipt-form migration point (lessons-JSON → in-tree scratch) between r61 and r64; not chased.
- U10 — the report-form switch from flat `rN-*` (through r59) to `round-NN/` (from round-60); the commit/decision that made the switch not chased.
- U11 — the sabotage instruments ("disposable" `/tmp` scratch runner) are not retained by design; whether any sabotaged copy survives for re-execution was not checked.
- U12 — r69 has no `r69-verifier.md`; the operator replay is recorded only in LOG/SCORECARD/adjudicator; whether raw artifacts for it exist was not checked.
- U13 — verifier seat routing (`openai-codex/gpt-6-luna`, "free-model rate limits", 5 respawns) is as the LOG says; the routing machinery was not inspected.
- Errata (extension): none at append time (append new errata blocks below; never rewrite).
<!-- lane-end note (TAMESHI-R2-4) — appended 2026-10-14 after the checks below -->

Lane-end checks (TAMESHI-R2-4): the section's first write lacked a leading newline, so its header comment rendered glued to the pre-existing final line (:106 `Errata: none yet …`); repaired same day by inserting one newline before the comment. Proof the original is untouched: `head -c 16536 corpus/knowledge/verification-patterns-fleet.md | sha256sum` → `df4ab192509fafc02bdd2450f54fe864730f29429298f9f93a5bc361ef06ba3e`, byte-identical to the pre-write file. Post-write `git -C tameshi-shokunin status --porcelain` → ` M corpus/knowledge/verification-patterns-fleet.md` + pre-existing `?? plans/`. File at this check: 194 lines (`wc -l`), 105 pre-write; this note appends after the check (the lane handoff carries the final count). Substrate: `git -C game-dev-2d-shokunin status --porcelain` unchanged (15 untracked entries before and after this lane; no tracked file modified). No scratch written (none needed; the /tmp namespace was unused).

## Errata (round 2)

Applied 2026-10-14 by TAMESHI-R2-2 from the wave-1 review trail (wave record
LOG.md:42-48 and the carried round-2 items LOG.md:66-67; per
plans/round-2.plan.md:10). Appended below the TAMESHI-R2-4 extension above —
nothing above this block is edited. Round-2 re-measurements were run by this
lane 2026-10-14 (scratch `/tmp/tameshi-r2-2-work/`).

**V-R2-1 (measured — held).** The kaidoku census numbers re-measured on the
current corpus (unmoved since the census; newest entry mtime 05:11): 72
knowledge files; 468 `verify:` vs 467 `verified-at:`; the same four
count-mismatched files (2026-10-13-r2-firmware-probe 7/6,
2026-10-13-r3-keyed-archive-carriers 3/4, 2026-10-13-r4u-05-wakaru-oom 3/4,
2026-10-13-r5-01-riscv-bypass 9/7). Commands: `ls
kaidoku-shokunin/corpus/knowledge/*.md | wc -l`; `grep -rn "verify:" … |
wc -l`; `grep -rn "verified-at:" … | wc -l`; per-file loop.

**V-R2-2 (measured — held).** The w6/w7/w8 closeout AGREE tallies re-grepped
identically: w6 3×5/5; w7 3×5/5; w8 2×6/6 + 1×5/5 (w8 g2d = 5/5). Command:
`grep -o '"verifier": "AGREE [0-9]/[0-9]"'
.ufo/waves/shokunin-train-20261014-w{6,7,8}/closeout.json | sort | uniq -c`.

**V-R2-3 (judgment — wave-record position, §3).** U1/U2 remain the recorded
decidable round-2 audit predictions (LOG.md:66-67). The round-2 fleet-note
lane (TAMESHI-R2-4, extension above) added the game-dev-2d pattern block
D1-D10 with its own U8-U13 and did not discharge U1/U2 — they stay open.

**V-R2-4 (measured — U1 first reading).** The four count-mismatches read as
grep-shape artifacts, not missing evidence (first reading only, not the full
chase): `2026-10-13-r2-firmware-probe.md:113` is a "Corrected verify:" line
inside its own errata block; `2026-10-13-r5-01-riscv-bypass.md:62` matches on
"re-verify:" inside a heading; `2026-10-13-r3-keyed-archive-carriers.md:112`
and `2026-10-13-r4u-05-wakaru-oom.md:152` are `verified-at:` stamps on
`source:`-based candidates. U1 is partially explained, still open.

## Errata (round 4)

Applied 2026-10-14 by ERR-T — the round-4 tameshi errata sweep (read every
corpus note's headers/pins; re-resolved each against live state; append-only;
nothing above this block is edited). Sweep scratch `/tmp/w4-errt-sweep/`.
Re-measured held before the findings below, so no errata was needed for them:
the kaidoku census counts (72 knowledge files; `verify:` 468 vs `verified-at:`
467; same four mismatched files), the w6/w7/w8 closeout tallies (3×5/5,
3×5/5, 2×6/6 + 1×5/5), PROTOCOL.md:430-431, the `.ufo/waves/kaidoku-r5/01–03`
audit files, and the audio/g3d/`.ufo/reports` line refs (spot-checked
unchanged). Sibling-note pins also re-resolved held (no appends made there):
kumitate 62/42/60/102/39/43 all exit 0 with unchanged sha256s; kagi 250
selftest cases + `--falsify` `caught=16/18 failed=2` + stamps recompute
`ok=56` + `tcase` counts 1/1/0/0/0/1; kimi-census `83016d45…` (mtime
2026-10-13 18:53:12.694); surface-census `275d8294…`; SKILL.md `dd2f4dee…`
(still the live revision, `/tmp` snapshot matches); kumitate `175de6ba` / kagi
`fecee87`; the executor scratch and both mutation-case scratch trees intact.

**V-R4-1 (measured — the D-block's substrate moved; state pins refreshed).**
`game-dev-2d-shokunin` is no longer at the extension's read revision: HEAD
`9fb50aa9…` → **`1275746cedfa314246755a81b4ab60e57075df98`** ("r73 report-last
+ simplifier-fold …", 2026-10-14 12:51:17 −0300), **10 commits** since;
`git status --porcelain` **15 → 30** lines. Re-measured against the current
tree: `find corpus/live -maxdepth 1 -name '*verifier*' | wc -l` **51 → 56**;
`ls reports | grep -cE '^round-'` **11 → 15** (round-60…round-74; the
read-empty `round-70/` now holds reports); flat `rN-*` = 428 held (max flat
round r59 held); `ls corpus/lessons | grep -icE 'verifier|non-author'` = 107
held; `wc -l LOG.md` **778 → 863** (additions-only), `grep -c 'AGREE'`
**9 → 12**, `grep -n 'AGREE' … | tail` was `:667, :722` → now `:840, :860`.
The D9 line's two then-untracked reports are committed (r68-verifier /
r68-boundary, landed in r70 `16d003c`), and the r69/r70 scratch it listed as
untracked is now tracked (2,620 `corpus/live` files match `r69-|r70-`). New
porcelain carries r73/r74 seat scratch ×18, `reports/round-74/`, three
`reports/round-71/r71-*.md`, r72-simplifier snapshot entries and one
`__pycache__`. All D-block cited lines still resolve: LOG.md
:611/:614-615/:631/:636/:722/:744-746/:771-773 and SCORECARD.md
:24/:34/:52/:61-64/:74 re-read to the quoted content — both files' diffs since
`9fb50aa9` are additions-only (`85/0`, `37/0`); `corpus/fixtures/run_battery.py`
is not in the diff, so its cited lines hold; the r68-verifier scratch still
carries three run dirs + both recompute instruments. The extension's
prediction was not falsified: r70–r73 all carry `rNN-verifier.md`. The same
stale revision text also sits in this repo's `corpus/README.md:12` (round-3
coverage-map row) — flagged, not edited (outside this sweep's write scope).
Commands: `git -C game-dev-2d-shokunin rev-parse HEAD`; `status --porcelain`;
`diff --numstat 9fb50aa9..HEAD -- LOG.md SCORECARD.md`; the find/ls/grep
counts above.

**V-R4-2 (measured — tameshi SHONEN.md moved under the P5 citation).** §1 P5's
parenthetical "(tameshi SHONEN.md:14 pins this line)" no longer resolves. At
`3da686c` (round-1 commit, the census's own wave) `SHONEN.md:14` was "Header
pins: PROTOCOL.md lines 419-428 (seed), lines 430 (mark spec)."; the round-2 /
round-3 rewrites (last commit `53e74a8`, 2026-10-14 13:01:03) moved the pin to
the last line — current `SHONEN.md:36` carries it verbatim, and `:14` is now
inside the end-to-end box ("`cmp`-verified pristine byte copy…").
PROTOCOL.md:419-428 and :430-431 re-read held. Command: `sed -n '14p;36p'
tameshi-shokunin/SHONEN.md`; `git -C tameshi-shokunin show 3da686c:SHONEN.md`.

**V-R4-3 (measured — two cited anchors re-resolved on frozen files;
corrections recorded).** Neither target file moved, so these are citation
corrections rather than drift — kept because a re-resolving reader lands wrong:
(a) P10's "(adjacency axis AXES.md:15)" and §2's "axes table AXES.md:5-13" do
not resolve — on the file (unchanged since `e867f78`, 2026-10-13 16:47:03;
worktree clean) the six-axis table is **`AXES.md:9-16`** (depth :11, coverage
:12, operability :13, freshness :14, calibration :15, **adjacency :16**), and
`:5` is the intro's last line ("fleet-level axes."). Correct ranges: adjacency
= `:16`, table = `:9-16`. (b) P4's `spec.json:15` seat label "(audio r67
author prompt)" — `:15` is the **audio-scout** prompt (Brief:
`tasks/audio-scout.txt`); audio-author is `:21`. The quoted invariant ("all
102 prior ledger rows + receipts byte-stable") does sit at `:15`, and in all 8
audio-seat prompts (:15/:21/:27/:33/:39/:45/:51/:57); the quote resolves, the
seat label is corrected. Command: `sed -n '9,16p' AXES.md` + `git show
e867f78:AXES.md`; `grep -n '"prompt"' spec.json` + per-prompt Brief grep;
`grep -c '102 prior' spec.json` → 8.

**ER-jj — jj-era reading of "HEAD" (round 17, 2026-10-20; append-only).** Lane and owner repos are jj-colocated, so git HEAD is detached at the working-copy commit's parent and may differ from the branch tip (S061). Every active instruction above that reads `HEAD` (`show HEAD:<path>`, ancestor of HEAD, worktree vs HEAD, `git archive HEAD`) now reads the branch tip `refs/heads/<branch>` (`detect_branch`, `../scripts/hyaku/jj-lane.sh:53-65`) or an explicit 40-hex revision; dated records above are not re-interpreted. Canonical rule: `SKILL.md:1027-1035`, `operator-runbook.md` ER-R3.
