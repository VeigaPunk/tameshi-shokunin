# ReportDraft — tameshi round 16, wave 2 (falsify)

Seat: `TameshiR16.ReportDraft` (leaf, no delegation). Draft body of the round-16 report sections (`.ufo/prompts/tameshi-round-16.md` §4, lines 99-129), built only from lane commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8` and wave-1 reports. Unknowns are marked **PENDING**. Items the working tree adds after `c699c8c` are named as uncommitted and are not counted.

## Verdict on what was attacked

**partial.** C1 (depth 6→7) holds at `c699c8c`. C2 (calibration 6→8) falls at `c699c8c`: the ledger it depends on is not in the commit, and the committed counter scores calibration at 6. The round-15 attribution repair holds. The SHONEN box-3 link checker and its selftest are vacuous for the committed page (repaired only in the uncommitted working tree). `SCORECARD.md` and `LOG.md` carry no round-16 entry at `c699c8c`.

## Method and scratch

- Lane HEAD read: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD` → `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (exit 0). Commit time 2026-10-20T10:49:37-03:00; pre-registration `e69b488` 10:39:59-03:00.
- Counting command copied from committed bytes to scratch: `/tmp/tameshi-r16w2-ReportDraft-sM395a/measure.py` (sha256 `dc3483609d14a8efb768e25fb5d8a72ac6cf37dca512536269e42afe14abfd5e`, identical to `git show c699c8c:.ufo/evidence/round-16/measure.py`).
- Assembler and attribution tool copied from committed bytes to scratch (`assemble.py`, `reattribute.py`). `reattribute.py` derives its lane root from its own location (`reattribute.py:45`), so it was also run from a layout mirror (`/tmp/tameshi-r16w2-ReportDraft-mirror-iPytS4`, built with `git archive c699c8c` of `.ufo/evidence/round-16/attribution` and `.ufo/evidence/round-15`).
- Not re-run: the round-gate regression leg (`tools/mutate-and-run.sh --regression`). I cite its retained output only.
- Tool installs or updates by this seat: none.

## Work performed

Declared claims (lesson `corpus/lessons/round-16.md`, header block): **C1 depth 6→7** (seventh recorded mutation case, kumitate `round-gate.mjs`, leg `js-round-gate`); **C2 calibration 6→8** (full-page cold-read of `SKILL.md` earns the box-3 lane assertion). Both target axes sit at 6, the lowest non-retired numeric scores (`SCORECARD.md` baseline table, and the round-15 row). Routed defects 1 (sibling-overlap scan) and 2 (usage attribution) from `corpus/lessons/round-15-verifier-spotcheck.md:157-160` are claimed as done this round.

- **C1 pre-registration before sweep.** `git show --stat e69b488` lists `.ufo/evidence/round-16/round-gate/predictions.json` (+74). Pre-registration committed 10:39:59-03:00. Sweep at 10:40:15-03:00 (`corpus/knowledge/mutation-case-kumitate-round-gate.md:2`, "sweep 13:40:15Z"). Evidence: `.ufo/evidence/round-16/round-gate/sweep/results.tsv`.
- **C1 sweep result.** 10 single-edit mutants, 5 KILLED (A1, A3, B1, E3, C1060) and 5 SURVIVED (C1059, A2, B2, CKIND, E1). Read directly from the table, every verdict matches the `(predict …)` text in its row: 10/10. This is a reading of the retained table, not a re-run.
- **C1 case 7 landed.** `corpus/knowledge/mutation-case-kumitate-round-gate.md` (+135 lines at `c699c8c`). Its header line 1 cites S053, S052, S056 and S057; the body cites S052 (line 41), S056 (line 42) and S057 (line 109). The runner edit is `tools/mutate-and-run.sh` (+108/−24). Retained regression output `.ufo/evidence/round-16/round-gate/runner-regression.txt` tail: `REGRESSION_TABLE js-round-gate: match=10/10 … flips=0`, `REGRESSION: PASS (cases=7 passed=7 …)`, `rc=0`. I did not re-run it.
- **C2 cold-read ledger assembler.** `.ufo/evidence/round-16/coldread/assemble.py` (committed; 39982 B). Its selftest passes: `SELFTEST: all checks passed`, exit 0 (my run from a scratch copy). The page it sections by default is `SKILL.snapshot.md` (sha256 `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`, 51 buckets), not the committed `SKILL.md` (sha256 `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4`, see §Before → after).
- **C2 seat cold-read reports.** 38 `CR*.md` files in `.ufo/waves/round-16/w1/` (`ls .ufo/waves/round-16/w1/CR*.md | wc -l` → 38): 30 cold-read section reports (CR01–CR27 with CR04, CR11, CR12 split a/b) and 8 others (CRCritic1/2, CRSentinel, CRRevenger, CRSource/CRSource2, CRLedger, CRMeasure).
- **C2 ledger artifact.** `.ufo/evidence/round-16/coldread/ledger.json` is absent: `git ls-tree -r --name-only c699c8c .ufo/evidence/round-16/coldread/` lists only `SKILL.snapshot.md` and `assemble.py`; `find` over the lane returns nothing; `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` → non-zero (ABSENT).
- **Attribution repair (QUALITY 18).** `.ufo/evidence/round-16/attribution/correction.json` (committed). `reattribute.py --selftest` run in the layout mirror: `SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)`, exit 0. The round-15 receipt it reads hashes `3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` (45164 B), matching the lesson's claim that `verification-3.json` is unchanged.
- **Attribution tool portability.** `reattribute.py:45` sets `LANE_ROOT = Path(__file__).resolve().parents[4]`. Run from a bare `/tmp` copy it exits 1 (`IndexError` on `parents[4]`); with the layout mirror but without `.ufo/evidence/round-15` it exits 1 with `FileNotFoundError`. It passes only at the real layout depth with the round-15 receipt present.
- **Sources (C1/C2 frontier step).** Six rows opened this round: S052 (Stryker supported mutators, A), S053 (kumitate `round-gate.mjs` @ `364f1d5`, A), S054 (Diátaxis compass, A), S055 (Python doctest, A), S056 (PIT mutators, A), S057 (Papadakis et al. survey preprint, B). The per-row quotes live in the lesson's `## Gate` table; this seat did not re-open the URLs.
- **Mistake frontier step (committed lesson `## Mistakes`, four rows):** attribution (`round-15-verifier-spotcheck.md` routed defect 2; captured-by none; fix QUALITY 18); attribution in AttrFix's own brief (captured-by AttrCritic); landing (`.ufo/waves/hyaku/misroots/TameshiR15`; captured-by none; fix QUALITY 19); scope (RGLeg editing a live instrument; captured-by RGCritic; fix QUALITY 20).
- **Sibling-overlap scan (round-15 routed defect 1).** Wave-1 connector `Overlap1` (`.ufo/waves/round-16/w1/Overlap1.md`) is committed at `c699c8c`. In the working tree it has a +2-line erratum appended at its end (`git diff -- .ufo/waves/round-16/w1/Overlap1.md`, uncommitted; the erratum corrects the game-dev-3d SKILL.md claim at its §2 sweep comment).
- **Wave 1.** `.ufo/waves/round-16/w1/swarm-registry.json` → `wave: tameshi-r16-w1`, 68 members: executor 25, scout 14, reviewer 10, scribe 5, revenger 4, critic 4, connector 4, sentinel 2. No mutation-tester seat in wave 1. The registry has no per-seat status field; 68 `.md` report files are present, so per-seat completion is **PENDING** beyond the file count.
- **Wave 2 (in flight at read time).** `.ufo/waves/round-16/w2/swarm-registry.json` → `wave: tameshi-r16-w2`, 67 members: executor 22, reviewer 18, scout 8, critic 5, scribe 5, mutation-tester 4, sentinel 3, connector 2. Round seat total 68 + 67 = 135 (cap 200). Wave-2 reports were still landing at 10:54 (for example `MisrootSweep.md`, `RR01.md`, `WaveCounts.md`); completion is **PENDING**.
- **Role mapping.** Wave 1 has no planner seat (the validator rejects `planner`; the L1 holds the §3 planner function, with a bounded walk riding scout/connector/revenger items). `PlannerWalk.md` exists in w1; this seat did not audit that mapping.

## Landed changes

| Change | Commit | LOG.md entry | Notes |
|---|---|---|---|
| Pre-registration of js-round-gate predictions; wave-1 seat reports retained | `e69b488` (10:39:59-03:00) | **none at `c699c8c`** | `git show c699c8c:LOG.md \| grep -c -i "round 16"` → 0; `round-16` → 0 |
| Round-16 landing: case 7, cold-read repairs, sources S052–S057, attribution repair | `c699c8c` (10:49:37-03:00) | **none at `c699c8c`** | 46 files, +5333/−116 (`git show --stat`) |
| SCORECARD round-16 row | **none** | — | `git show c699c8c:SCORECARD.md \| grep -c -i "round 16"` → 0 |

Conformance gap, per §2.5 and §4: the round-16 move record (LOG.md entry, SCORECARD row with score delta, evidence pointer, counting command and measured commit) is absent at `c699c8c`. **PENDING** for the L1 landing commit.

Working-tree items after `c699c8c` (uncommitted, not counted): `M .ufo/evidence/round-16/measure.py` (repair), `M .ufo/waves/round-16/w1/Overlap1.md` (+2), `M corpus/lessons/round-16.md` (+1 "vacuous" mistake row), untracked `.ufo/evidence/round-16/Overlap1/`, `.ufo/evidence/round-16/measure-repair/`, `.ufo/waves/round-16/{assignments2,dispatch2,record2,spawn2,spec2}.json`, `.ufo/waves/round-16/w2/`.

## Before → after measurements

Counting command (both revisions, exit 0): `python3 measure.py --rev REV` (scratch copy of `c699c8c`'s `.ufo/evidence/round-16/measure.py`).

| Measure | Before `7650fe4` (round-15 measured commit) | After `c699c8c` | Claim | Verdict |
|---|---|---|---|---|
| `recorded_cases` / `depth_score` | 6 / 6 | **7** / 7 | C1 depth 6→7 | **holds** |
| ledger legs | js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check | + `js-round-gate` | C1 | holds |
| `calibration_restraint_score` | 6 | **6** | C2 calibration 6→8 | **falls** |
| `coldread.ledger_present` | false | **false** | C2 | falls |
| `coldread.sections_covered / sections_total` | — / 51 | **0 / 54** | C2 | falls |
| `shonen.box3_ledger_link` | false | **false** | C2 | falls (see finding 2) |
| `shonen.marks` | ~,~,~,~ | ~,~,~,~ | — | [~] on all four, no [x] |
| `sources.rows` | 49 | **55** | frontier | holds |
| `sources.tiers` (A/B/C) | 42 / 5 / 2 | **47 / 6 / 2** | frontier | holds |
| `sources.status` (mined/queued/rejected) | 22 / 24 / 3 | **28 / 24 / 3** | frontier | holds |
| `sources.malformed` | 0 | 0 | — | holds |

Selftest of the counting command at `c699c8c`: `python3 measure.py --selftest` → `MEASURE_SELFTEST: 33/33 pass`, exit 0.

Page-level evidence for C2 (not in the JSON counter, from committed bytes):
- `git show c699c8c:SKILL.md | sha256sum` → `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (matches the prompt's SHA), 1795 lines.
- `git show c699c8c:.ufo/evidence/round-16/coldread/SKILL.snapshot.md | sha256sum` → `97cf436b…623580` (the assembler's default input, 51 buckets). `diff` of snapshot vs committed page: 131 changed lines. The ledger therefore cannot cover the committed page unless `assemble.py` is re-run over the committed `SKILL.md` as a `--skill`; no such ledger is committed.
- Measured buckets on the committed page: 54 (preamble + 53 headings). The committed SKILL adds `## Errata — round 16 full-page cold-read (append-only)`, `## Seventh recorded case and full-page cold-read — round 16`, and `### Round-16 gate/probe registry`.

Finding 2 (verifier falls): `measure.py` `shonen_boxes` returns only each box's first physical line (`BOX_RE`, line 62; function at line ~137), and `box3_link = … BOX3_LINK in boxes[2][1]` is computed in `measure()`. `SHONEN.md` at `c699c8c` carries the ledger path on the indented continuation line: `git show c699c8c:SHONEN.md | sed -n 10p` → `  [lane assertion, full page: … ledger .ufo/evidence/round-16/coldread/ledger.json …](.ufo/evidence/round-16/coldread/ledger.json)`. The 33-case selftest's fixture (`SHONEN_BOX3`, measure.py:310) places the link on the box line, so the selftest passes against a shape the committed file never uses. Repair exists only in the working tree (`.ufo/evidence/round-16/measure-repair/`, measure.py modified); it is not in `c699c8c`.

Frontier census: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (fleet root) → exit 0; output lines `tameshi W04 S047 …`, `tameshi W04 S048 …` (disclosed duplicate-URL warnings, unchanged), `tameshi ok …/corpus/SOURCES.md`.

## Sources & frontier

- Registry before → after: **49 → 55 rows** (`measure.py` above; committed `corpus/SOURCES.md`). Malformed 0 → 0.
- Rows added by tier: **A +5** (S052, S053, S054, S055, S056), **B +1** (S057), C +0.
- Rows touched old → new: **none.** `git diff --numstat 7650fe4 c699c8c -- corpus/SOURCES.md` → 16 insertions, 1 deletion; the one deletion is the footer `-- Next unused id: S052.` (becomes `S058`). The diff shows no other removed row.
- Frontier rows advanced: **none recorded.** `git diff 7650fe4 c699c8c -- corpus/README.md | grep '^[-+]| F[0-9]'` → no output. The README diff appends a round-16 section (+28 lines) and no F-row status changes. [INFERENCE] S052–S057 support C1/C2 scope, not any F1–F10 status change.
- Sourced claim (§2b step 4): the case-7 knowledge file cites S052, S053, S056, S057 in its `source:` header (`corpus/knowledge/mutation-case-kumitate-round-gate.md:1`). Satisfied.
- Census before/after: start artifact `.ufo/evidence/round-16/census-start.txt` (3 lines: two W04 warnings, `ok`). Start exit code is not recorded in that file (**minor gap**); end census exit 0 (above).
- Registry id space: 55 rows present; S038 and S039 are absent by the id-allocation footer (reserved, retired).

## Trend verdicts (proposed; L1 decides; LEARNING.md trend definitions not re-read by this seat)

- **expansion — proposed `improved`.** Evidence: six new rows (five A, one B), one new admitted knowledge note (`mutation-case-kumitate-round-gate.md`, +135 lines), depth case 7 measured. Caveat: the new note is one case; no new frontier ground held.
- **quality — proposed `unchanged`.** Evidence against an improvement: the lesson's C2 claim (`calibration 6→8`) is not supported by any committed artifact at `c699c8c` (findings 1-2 below). The round's own selftest passed a shape the page does not use. Four mistakes are recorded with captured-by named. No non-author check exists for round 16.
- **discernment — proposed `unchanged`.** No non-author admit/reject sample for round 16 (`corpus/lessons/round-15-verifier-spotcheck.md` is the round-15 check; round-16 has none yet). `unprovable-but-better` requires a named non-author reviewer on record: **PENDING**.

## SHONEN

Checklist at `c699c8c` (`SHONEN.md`, 12 lines). Pointer resolvability checked against `c699c8c`:

- `[~]` box 1 (`SHONEN.md:5-6`) — pointer `reports/round-1-calibration.md#box-1` resolves (PRESENT; anchor `## box-1` at `reports/round-1-calibration.md:71`). No named non-author verifier → stays `[~]`.
- `[~]` box 2 (`SHONEN.md:7-8`) — pointer `reports/round-1-calibration.md#box-2` resolves (anchor `:105`). `[~]`, no non-author verifier.
- `[~]` box 3 (`SHONEN.md:9-10`) — pointer `.ufo/evidence/round-16/coldread/ledger.json` **does not resolve** at `c699c8c` (ABSENT). Under §4 (`[~]` requires a resolvable evidence pointer) it cannot be `[~]` at this commit. **PENDING** L1: land the ledger and re-measure, or revise the line. Not `[x]` (no independent verifier).
- `[~]` box 4 (`SHONEN.md:11-12`) — pointer `reports/round-1-calibration.md#box-4` resolves (anchor `:167`). `[~]`, no non-author verifier.
- `[x]`: none.

## Stale-lane

Stale-lane: respawn-per-round driver; no other mission of this lane is open. (Per prompt §6 extras; the L1 confirms.)

## Misroot sweep (partial, read-only)

`git --no-optional-locks -C /home/vgpnk/Projects/shokunin status --porcelain` at read time: `M .ufo/watchdog.log`; untracked `.ufo/state/{kaidoku,kake,kama,mado,mori,souji,tabi,tameshi,tsukuroi}.report-baseline`; `scripts/hyaku/jj-lane.sh`; `scripts/hyaku/jj-lane-selftest.sh`. `grep -l -i tameshi` over `scripts/hyaku/jj-lane.sh`, `scripts/hyaku/jj-lane-selftest.sh` and `.ufo/state/tameshi.report-baseline` → no match (exit 1). No fleet-root seat note naming this lane was seen. Not exhaustive: wave-2 seats still writing. `.ufo/state/*` not touched.

## L0 questions

No round-16 tameshi line in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (`grep -n "^tameshi |"` → only the round-1 line). Open host-level questions belong to other lanes (tsukuroi, hyaku-orchestrator, kaidoku) and are out of this seat's scope.

## Dead seats

Wave 1: none recorded in the registry; 68 report files present; per-seat completion **PENDING** (registry has no status field). Wave 2: **PENDING**.

## Findings (for L1 — defects and falsifications, with pointers)

1. **Falls — C2 unsupported at `c699c8c`.** `ledger.json` absent (`git cat-file -e` → non-zero); `measure.py --rev c699c8c` → `calibration_restraint_score: 6`, `box3_full_page: false`, `sections_covered: 0/54`. The lesson header's C2 claim is not measured.
2. **Falls — verifier link check vacuous on the committed page.** `measure.py` `shonen_boxes` / `box3_link` (single-line match) vs `SHONEN.md:10`; selftest fixture `measure.py:310`. Repair uncommitted.
3. **Falls — conformance.** No LOG.md round-16 entry and no SCORECARD round-16 row at `c699c8c` (§2.5, §4). Landed changes not tied to LOG.
4. **Holds — C1.** `recorded_cases 7` (`measure.py --rev c699c8c`); retained regression output `REGRESSION: PASS (cases=7 passed=7)`; sweep 10/10 predictions match the table; pre-registration `e69b488` precedes the sweep by 16 s.
5. **Holds — attribution repair.** `reattribute.py --selftest` in layout mirror → exit 0, new rule 4/4 vs old 3/4. Portability defect: `reattribute.py:45` (exit 1 from a bare copy).
6. **Holds — sources census.** Exit 0; rows 49→55; no existing row touched (footer only).
7. **Minor.** Round-start census artifact lacks an exit-code line (`census-start.txt`). The ledger is absent; `assemble.py` defaults to the snapshot (51 buckets), not the committed page (54 buckets). The lesson's "68 completed, 0 dead" is not recorded in the registry.
8. **Inherited/uncommitted (name in report):** `M .ufo/evidence/round-16/measure.py`, `M .ufo/waves/round-16/w1/Overlap1.md`, `M corpus/lessons/round-16.md`, untracked `Overlap1/`, `measure-repair/`, `*2.json`, `w2/`. Working-tree repairs are not measured at HEAD.

## Evidence index (commands and exits)

| Command (scratch copies unless noted) | Exit | Key output |
|---|---|---|
| `git show c699c8c:SKILL.md \| sha256sum` | 0 | `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` |
| `python3 measure.py --rev c699c8c…` | 0 | `recorded_cases 7`, `calibration_restraint_score 6`, `ledger_present false`, `sources.rows 55` |
| `python3 measure.py --rev 7650fe4…` | 0 | `recorded_cases 6`, `sources.rows 49` |
| `python3 measure.py --selftest` | 0 | `MEASURE_SELFTEST: 33/33 pass` |
| `python3 assemble.py --selftest` | 0 | `SELFTEST: all checks passed` |
| `python3 reattribute.py --selftest` (bare copy) | 1 | `IndexError` on `parents[4]` |
| `python3 reattribute.py --selftest` (layout mirror, no round-15 evidence) | 1 | `FileNotFoundError` on `verification-3.json` |
| `python3 reattribute.py --selftest` (layout mirror, with round-15 evidence) | 0 | `SELFTEST: PASS (new rule 4/4; old rule fails 3/4 …)` |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | 0 | `tameshi ok …/corpus/SOURCES.md`; W04 S047/S048 |
| `git cat-file -e c699c8c:.ufo/evidence/round-16/coldread/ledger.json` | non-zero | ABSENT |
| `git show c699c8c:SHONEN.md` | 0 | 12 lines; box 3 link at `:10` |
| `git show c699c8c:LOG.md \| grep -c -i "round 16"` | count | 0 |
| `git show c699c8c:SCORECARD.md \| grep -c -i "round 16"` | count | 0 |
| `git show --stat e69b488` | 0 | `predictions.json +74` |
| read of `round-gate/sweep/results.tsv` | — | 10/10 match by direct reading (no command) |
| `git --no-optional-locks -C /home/vgpnk/Projects/shokunin status --porcelain` | 0 | 11 entries (listed above) |

Verdict repeated: **partial** (C1 holds; C2 falls at `c699c8c`; attribution repair holds; SHONEN link checker vacuous; LOG/SCORECARD missing).
