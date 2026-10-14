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