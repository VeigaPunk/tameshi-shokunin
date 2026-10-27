# T51ScribeFrontier — C1 draft: appended frontier status table

Seat: T51ScribeFrontier (scribe, leaf). Milestone: C1 frontier table. Round 51, wave 1.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Freeze commit `84aa673a1a476e48ccf239335696f0518d08bae7`; base `9962033fd7a75aa2f2847e979dd687a5d28505a1`.
I did not decide a claim, did not edit the lane checkout, did not commit/push anything outside a scratch clone.

## Behavior (what the appended text does)

`corpus/README.md` at the freeze commit is 608 lines and ends `...void as of round 50\n` (sha256 `f93748a131cf07fef19770c1414198bf57da23cc1801bcaa1fb54f45d8baa9e3`). The text below is appended after line 608, leaving every base byte a prefix (counter field `readme_prefix=1`). It appends one heading, one paragraph declaring `:76-87` superseded as a whole, one table whose header is exactly `| id | ground | candidate sources | status | next falsifiable move (before → after) |`, one row per F1..F10, and a two-line S022 note. The S022 status cell changes `queued` → `mined` (no other byte of that row moves).

Status cells: frozen status+round from `.ufo/evidence/round-51/c1/frontier-expected.json` verbatim, then ` — `, then a `README.md:A[-B]` pointer with `B-A <= 5`, then short qualifiers (`F1b open`; `for the nine frozen files`).

## The exact appended text (byte-identical to what the self-check ran)

```markdown

## Round 51 — frontier status table re-stated (calibration)

The status table at `corpus/README.md:76-87` is superseded as a whole: its status cells were never re-stated after the rounds that moved them (rounds 1, 21, 25, 27, 38, 49, 50), so seven of the ten cells no longer read what the lane later declared. Nothing above this line is rewritten — the coverage map is corrected by appending only — and each row below carries the latest wording with a pointer to the lines that declare its status.

| id | ground | candidate sources | status | next falsifiable move (before → after) |
|---|---|---|---|---|
| F1 | external mutation-score semantics + report interop | S001, S002, S086, S087 | held (round 25) — README.md:385-390; F1b open | before: emit one ledger leg as schema JSON and validate it (validator unavailable in round 1) → after: held for the eight recorded ledger legs (round 25, README.md:386-390); remaining: the emitted report names a target by basename with no lane or revision pin (round 26, README.md:412-413) and the 35 recorded survivors stay unclassified for NoCoverage (README.md:396) |
| F2 | witness-scoped kill verdicts / bash mutation tooling | S006, S257 | partly held (round 1) — README.md:115 | before: the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8 → after: still unmeasured; the existing bash leg's declared-witness study is retained separately (README.md:128) and round 45 adds GoogleTest's primer as an upstream instance of the split (README.md:563) |
| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040, S256, S258-S264 | open — README.md:589 | before: one control per sweep → after: N ≥ 3 byte-identical controls, or a named mismatch: still unmeasured; the rounds 45-47 entries add upstream statements and published measurements only (README.md:558-589) |
| F4 | golden / snapshot fixture discipline | S013, S014, S015, S016, S017, S045, S105-S108, S132, S152, S153, S154 | partly held (round 38) — README.md:492-495 | before: update paths that write expected values without an explicit flag: unmeasured → after: the write-path census counted 99 live write sites with 0 unflagged (round 39, README.md:503), and rounds 40-41 added two successor tools; remaining: the cmp and git diff --exit-code lattices, and the shutil.* and handle.write classes outside v2's pattern (README.md:511, README.md:521-523) |
| F5 | hermetic environment normalization | S015, S016, S028, S079 | Core (round 21) — README.md:330-335; for the nine frozen files | before: runner selftest host vs env -i LANG=C TZ=UTC identical (H3, round 1) → after: the nine frozen files measured the same way (nine clean controls, round 21); the three kumitate gates cite-check, surface-probe and proxy-check stay unmeasured (README.md:335-336) |
| F6 | fixture minimization for survivors | S022, S023, S024, S271 | held (round 50) — README.md:608 | before: B5 probe fixture size: unmeasured → after: held for the method on killing cases — one shrinker to a 1-minimal sub-case with a stated run cost (round 50); the round-29 B5 survivor is not discharged and stays masked → next: shrink on a second gate, or discharge B5 |
| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041, S047 | open — README.md:255-256 | before: pin-level cadence only → after: per-leg reuse decisions classified: not reached; round 13 acquired only the content-disposition prerequisite and round 17 moved no row (README.md:255-256) |
| F8 | oracle anchoring as a survivor class | S012, S090, S091 | partly held (round 27) — README.md:424-427 | before: 0 test-oracle lines → after: one survivor classified against an independently anchored expectation, one gate at one pin (round 27); bounded to 3 of 4 survivors anchored in the gate's header contract and 1 by convention only (round 29, README.md:433-437) → next: anchor the hole calls on the other eight recorded legs |
| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open — README.md:86 | before: no LLM-specific search run yet (U) → after: bounded pilot with an independent outcome check: untouched; round 43 states F9 is not touched (README.md:555-556) |
| F10 | PBT generators for gate fixtures | S018, S019, S020, S021, S269, S270 | held (round 49) — README.md:599 | before: no PBT fixture method → after: one generator against a named fixture gate, conditioned on the round-49 deciding receipt printing C2_R49_PASS=true; next: a second gate, or shrinking (README.md:599) |

S022 (`queued` → `mined`): the row's used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`, which cites it (round 50), so the status column is corrected to CORPUS.md's own reading — mined = cited by at least one path in used-by.
No other SOURCES row changes status here, and every used-by path of a mined row exists at this revision.
```

## Self-check (scratch clone at the freeze commit, then one commit)

Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"`, checked out at `84aa673a`, then `corpus/README.md` = freeze bytes + the fence above and the S022 cell flipped, committed as `6d236c76e4e96318e95d06eca394fed83d5e11e2` (2 files, +21/-1). Command and observed output:

```
$ python3 tameshi-shokunin/.ufo/evidence/round-51/c1/measure.py --lane <scratch clone> --rev 6d236c76e4e96318e95d06eca394fed83d5e11e2 --explain
FRONTIER F1: ok line 616
FRONTIER F2: ok line 617
FRONTIER F3: ok line 618
FRONTIER F4: ok line 619
FRONTIER F5: ok line 620
FRONTIER F6: ok line 621
FRONTIER F7: ok line 622
FRONTIER F8: ok line 623
FRONTIER F9: ok line 624
FRONTIER F10: ok line 625
C1_R51: rev=6d236c76e4e96318e95d06eca394fed83d5e11e2 frontier_rows=10 table_rows=10 frontier_bad=0 readme_prefix=1 sources_rows=131 status_conflicts=0 usedby_missing=0 total=0 C1_R51_PASS=true
EXIT=0

$ ... --rev 84aa673a1a476e48ccf239335696f0518d08bae7   # negative control, freeze commit without the append
C1_R51: rev=84aa673a1a476e48ccf239335696f0518d08bae7 frontier_rows=10 table_rows=10 frontier_bad=10 readme_prefix=1 sources_rows=131 status_conflicts=1 usedby_missing=0 total=11 C1_R51_PASS=false
EXIT=1

$ git -C <scratch clone> diff 84aa673a -- corpus/SOURCES.md
diff --git c/corpus/SOURCES.md w/corpus/SOURCES.md
index 368f65e..768be30 100644
--- c/corpus/SOURCES.md
+++ w/corpus/SOURCES.md
@@ -30,7 +30,7 @@ rows only, and a row is a claim opened in the round that writes it.
 | S019 | Property-Based Testing in Practice (Goldstein, Cutler, Dickstein, Pierce, Head; ICSE 2024) — https://harrisongoldste.in/papers/icse24-pbt-in-practice.pdf | paper | A | PBT practice at one company (Jane Street interviews) | Abstract, ICSE 2024 PDF p.1 (fetched 2026-10-19) | 30 interviews: PBT pays off on complex code; its weaknesses are generator effort (6/30 tedious, 7/30 high-effort) and no visible feedback on test effectiveness; shrinking interfaces and effectiveness evaluation are open problems | queued | 2026-10-19 | 730d | — |
 | S020 | Property-based testing in Python: empirical insights (de Oliveira, Corgozinho, Rocha, Valente; EMSE 2026) — https://doi.org/10.1007/s10664-026-10953-w | paper | A | PBT usage in 244 Python projects | Abstract; §6.2 and Table 2 (author copy https://homepages.dcc.ufmg.br/~mtov/pub/2027-esem-pbt-python.pdf, fetched 2026-10-19; Springer served an anti-bot challenge) | 367 PBTs from 244 projects in nine categories with Test Oracle at 29.97%; data generation is the main challenge (36.62% of SO questions); Ghostwriter fully automates only 18.23% | queued | 2026-10-19 | 365d | — |
 | S021 | Agentic Property-Based Testing (Maaz, DeVoe, Hatfield-Dodds, Carlini; arXiv 2510.09907) — https://arxiv.org/abs/2510.09907 | paper | A | agentic PBT bug validity on real packages | Abstract, arXiv:2510.09907v1 (submitted 2025-10-10) | an LLM agent infers properties from code and docs, writes Hypothesis tests and reflects before reporting: 56% of reports were valid bugs; ranking lifts the top-21 validity to 86% | queued | 2026-10-19 | 180d | — |
-| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | queued | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
+| S022 | Test-Case Reduction via Test-Case Generation (MacIver, Donaldson; ECOOP 2020) — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2020.13 | paper | A | internal test-case reduction and the validity problem | Abstract, LIPIcs ECOOP 2020 (DOI 10.4230/LIPIcs.ECOOP.2020.13; page fetched 2026-10-19) | internal reduction shrinks the sequence of random choices made during generation, so every reduced case is one the generator could have produced; compared with C-Reduce and delta debugging | mined | 2026-10-19 | 730d | corpus/knowledge/fixture-shrinking-pilot.md |
 | S023 | Shrink Ray README (DRMacIver/shrinkray) — https://github.com/DRMacIver/shrinkray | code | A | shrinkray's interestingness-driven reduction | README §Usage and §LLM mode @ page currentOid 5fe6ee135d732e4b7758b3dbe3d91428523018fb, fetched 2026-10-19 | a reducer driven by any executable interestingness test (exit 0 = interesting); parallel multi-format passes; local LLM proposals are accepted only when the interestingness test still passes | queued | 2026-10-19 | 90d | — |
 | S024 | Reducing Failure-Inducing Inputs (The Fuzzing Book, Zeller et al.) — https://www.fuzzingbook.org/html/Reducer.html | book | B | delta-debugging reducer practice | §Delta Debugging (fetched 2026-10-19) | a runnable delta-debugging reducer: a Runner returns FAIL only on the precise error, and the input is cut to the minimum that still reproduces it | mined | 2026-10-19 | 365d | corpus/knowledge/survivor-fixture-minimization.md, corpus/knowledge/fixture-shrinking-pilot.md, corpus/knowledge/delta-debugging-minimization-contract.md |
 | S025 | An Empirical Analysis of Flaky Tests (Luo, Hariri, Eloussi, Marinov; FSE 2014) — https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf | paper | A | flaky test root causes and fixes | §Findings F.2, FSE 2014 PDF p.2 (fetched 2026-10-19) | 201 flaky-fix commits: top causes are Async Wait, Concurrency and Test Order Dependency; 78% of flaky tests are flaky when first written; 74% of order-dependency fixes clean shared state | queued | 2026-10-19 | 730d | — |

scratch clone HEAD: 6d236c76e4e96318e95d06eca394fed83d5e11e2
scratch clone: /fast/scratch/hyaku/tameshi-r51/T51ScribeFrontier/lane (deleted before yield; not citable)
```

The second block is the negative control: the same counter on the freeze commit without the append prints `frontier_bad=10 status_conflicts=1 total=11 C1_R51_PASS=false`, exactly the contract's `before` line, so the PASS is produced by the append and not by an empty table check.

## Findings

**N1 — the frozen statement's own prose is off by one on the table's last line; the table is 76-87, not 76-86.**
`grep -n '^\| \(id \| ground\|F[0-9]\+ \|\)' corpus/README.md` prints header `76`, separator `77`, rows `F1`=78 … `F10`=87. `.ufo/evidence/round-51/c1/frontier-expected.json:4` says "The status table at corpus/README.md:76-86". The contract and this seat item say 76-87; my paragraph uses 76-87. Row-level data in the frozen file is unaffected (`F9` basis `:86` is the F9 row). Not amended — the contract is never edited; recorded here for the L1.

**N2 — exactly seven of the ten base status cells are superseded, which is what the paragraph claims.**
`sed -n '76,87p' corpus/README.md` vs the frozen rows: F1 `held (round 1)` → `held (round 25)`; F2 `held` → `partly held`; F4 `open` → `partly held (round 38)`; F5 `open` → `Core (round 21)`; F6 `open` → `held (round 50)`; F8 `open` → `partly held (round 27)`; F10 `open` → `held (round 49)`; F3, F7, F9 stay `open`. Seven changed, three unchanged.

**N3 — the counter's pointer span (6 lines) is narrower than three of the frozen `basis` ranges, so those bases cannot be used verbatim.**
`.ufo/evidence/round-51/c1/measure.py:133` rejects a pointer when `b - a > 5`; `PTR_RE` at `:34`. The frozen bases F1 `:385-397` (13 lines), F4 `:491-497` (7) and F5 `:330-338` (9) exceed it. I trimmed to `385-390`, `492-495`, `330-335`, each still containing the id token and the status phrase (counter printed `FRONTIER Fk: ok` for all ten rows). Anyone reusing the frozen `basis` strings as pointers would score `no-supporting-pointer`.

**N4 — F9 has no pointer outside the superseded table, so its status cell must point into it.**
`sed -n '555,556p' corpus/README.md` names F9 but says "is not touched", not `open`; the only base lines pairing `F9` with `open` are the superseded row at `:86` (the frozen basis names `:86` for that reason). The F9 cell therefore cites `README.md:86`. The counter accepts it; read it as "the round-43 directive never moved F9", not as a self-supporting claim.

**N5 — S022 is the only SOURCES conflict at the freeze commit, and the flip clears it.**
Base run: `sources_rows=131 status_conflicts=1`; the flip yields `status_conflicts=0 usedby_missing=0`, `sources_rows` unchanged at 131. The row's used-by cell already reads `corpus/knowledge/fixture-shrinking-pilot.md` (`corpus/SOURCES.md:33`), which exists and cites S022 (round-50 row, `corpus/README.md:605`).

**N6 — this deliverable is cold-read neutral, measured (not inferred).**
`.ufo/evidence/round-48/quality/coldread-precheck.sh <clone> 9962033f 6d236c7` prints `COLDREAD_PRECHECK floor=9962033fd7a7 floor_credited=64 cand=6d236c76e4e9 cand_credited=64 lost=0 ok` (exit 0). So the append adds no re-key debt of its own, unlike the two drops the contract already names (runner bytes → 20 sections; SKILL.md registry section → 1). This is a draft-commit measurement on a scratch clone; the L1 re-measures at the content revision.

**N7 — no cell contains a `|`, and every row has exactly five cells.**
`measure.py` slices cells on `|` (`cells()`), so a stray pipe would silently shift the status column. Checked on the draft clone: every appended table line has 6 pipes (5 cells), same as the base table rows.

**N8 — candidate-source cells were extended past the base lists with the carriers later sections name; each extension is named in a cited section.**
F1 `+S086, S087` (`README.md:383`), F2 `+S257` (`:563`), F3 `+S256, S258-S264` (`:558-589`, rounds 45-47), F4 `+S105-S108, S132, S152-S154` (`:495`, `:503`, `:511`, `:521-523`, rounds 38-41), F5 `+S079` (`:328`), F6 `+S271` (`:605`), F7 `+S047` (`:152`, round 13), F8 `+S090, S091` (`:422`, round 27), F10 `+S269, S270` (`:597`). The ground text is the base wording unchanged; only the next-move cells were rewritten to the later move with its section cited. If the L1 prefers the base candidate lists verbatim, drop the added ids — the counter reads only the status cell, so that edit does not change the measurement.

**N9 — the paragraph says the cells "were never re-stated after the rounds that moved them"; the round-25 F1 correction and the round-27 F8 correction each re-stated one cell in prose before this table.**
`corpus/README.md:385-397` and `:424-431` do restate those two statuses (as `held`/`partly held`) without rewriting the table. To keep the sentence exact I enumerated the rounds that moved cells (1, 21, 25, 27, 38, 49, 50), so the claim is "the table's cells never changed; the later rounds stated the move elsewhere". Disclosed because a critic could read the shorter phrasing as denying those two prose corrections.

## Gates

| gate | state | evidence |
|---|---|---|
| C1 counter `C1_R51_PASS` | `true`, `total=0` on the draft commit | receipt below, `EXIT=0` |
| README append-only (base bytes prefix) | `readme_prefix=1` | counter field |
| Cold-read credited sections | 64 → 64, `lost=0` | `coldread-precheck.sh`, N6 |
| Lane checkout untouched | no write outside `.ufo/waves/round-51/w1` | only `write`/`edit` targets were scratch + this dir |
| Contract untouched | not edited | `.ufo/evidence/round-51/contract.json` read only |

## Touched surfaces

- Wrote: `.ufo/waves/round-51/w1/T51ScribeFrontier.md` (this file), `.ufo/waves/round-51/w1/T51ScribeFrontier.c1-receipt.txt`.
- Wrote (scratch, deleted before yield): `/fast/scratch/hyaku/tameshi-r51/T51ScribeFrontier/{section.md,lane/}`.
- Draft deliverable text targets `corpus/README.md` (append after line 608) and `corpus/SOURCES.md:33` (one status cell). Neither lane file was edited by me — the L1 applies the text.

## Out of scope / not done

- C2 and C3 deliverables; the runner edit; the SKILL.md registry rows; the SOURCES row for C2 (S272/S273); the round-49 style re-key (see N6: not needed for this file, needed for the runner/registry).
- No deciding-run invocation, no control run, no `--selftest` of the counter (I ran it only against scratch clones, per bounds).
- No tool installs; nothing installed, nothing upgraded.

## Artifact paths

- `.ufo/waves/round-51/w1/T51ScribeFrontier.md` — this report (contains the exact text).
- `.ufo/waves/round-51/w1/T51ScribeFrontier.c1-receipt.txt` — counter PASS at `6d236c7`, negative control at `84aa673a`, the S022 diff.

## Summary

- Appended text drafted: heading + one paragraph + the exact 5-column table with F1..F10 + the two-line S022 note; nothing above line 608 changes.
- Self-check on a scratch clone at `84aa673a` plus one commit (`6d236c7`): `frontier_bad=0 readme_prefix=1 status_conflicts=0 usedby_missing=0 total=0 C1_R51_PASS=true`.
- Negative control at the freeze commit prints `frontier_bad=10 status_conflicts=1 total=11 C1_R51_PASS=false`, so the PASS is not vacuous.
- Frozen prose says the table is `:76-86`; it is `:76-87` (N1). Frozen F1/F4/F5 bases exceed the counter's 6-line pointer span (N3).
- F9's only `F9`+`open` pointer is the superseded table row `:86` (N4).
- Seven of ten status cells were superseded (N2); S022 is the only SOURCES conflict (N5).
- Cold-read credit measured 64 → 64, `lost=0`: this file adds no re-key debt (N6).
- Every cell is pipe-free, five cells per row (N7); candidate-source extensions are listed with their sections (N8).
