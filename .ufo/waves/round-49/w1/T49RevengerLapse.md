# T49RevengerLapse — lapse archaeology: why each of the seven cold-read sections lost credit

Seat T49RevengerLapse (revenger). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`8ca67421111fa354b47b803358391d0b07fc6db9` (round-48 verifier spot-check, 2026-10-26). Read-only on
the lane: no file written outside this report and the receipt dir
`.ufo/waves/round-49/w1/T49RevengerLapse/`; no git/jj mutation; no scratch dir left behind
(`/fast/scratch/hyaku/tameshi-r49/T49RevengerLapse`, removed).

No claim is decided here. The C1 counter was not run — not even `--selftest`. The one measurement run
is the round-21 cold-read monitor with `--explain` (no `--ledger-file`/`--ledger-rev`/`--inputs-overlay`,
`overrides_used=false`), read as a probe of the base tree, not as a verdict.

This is the planning-data walk for the L1's planner seat: for each of the seven sections it names
the ledger inputs that no longer verify at base, the commit that first moved each input off the
digest the ledger recorded, what that commit did, and whether that kind of change recurs every round.

---

## 1. Method, and why the attribution is sound

The monitor credits a section only from ledger entries whose `inputs` map still verifies
(`.ufo/evidence/round-18/measure.py:47-58`, implementation `:330-351`). At base, `sha256(blob at
REV:<p>)` is compared with the digest each entry recorded; a mismatch is `input-drift:<p>`
(`.ufo/evidence/round-18/measure.py:330-351`). The round-21 selector adds the round-21 ledger path
itself to the ignored set, so the ledger never counts as its own input
(`.ufo/evidence/round-21/coldread/measure.py:22,112`). `ledger_source=rev`, `ledger_committed=true`,
`trace_gate=strict` (receipt `verify.txt` §1).

I recomputed the input gate with the frozen implementation's own helpers (same module import the
selector uses) rather than re-implementing it: for every ledger entry that matches one of the seven
sections' `sha256`, `input_failures(repo, REV, inputs_view(entry))`. The union over each section's
entries reproduces the monitor's `input-drift:` sets exactly — 12, 2, 3, 1, 4, 7, 7 paths
(`verify.txt` §2, `ALL SEVEN MATCH`).

**Drift attribution.** For each entry and each failing input, the recorded digest `d` is compared
against the path's blob history (`git rev-list --reverse BASE -- <path>`, one `git cat-file blob
<c>:<path> | sha256sum` per commit). The *first drifting commit* is the successor of the last commit
whose blob equals `d`. Two checks make this trustworthy:

- **0 of 94** attributed drift commits are outside the entry's own read line: each is a descendant of
  that entry's `read_rev` (`lapse.json`, `pre_read_drift` empty for every entry). No entry is blamed
  on a commit that predates its read.
- **93 of 94** entries have every recorded input digest equal to the blob at the entry's own
  `read_rev`; the one exception carries a fabricated digest, reported in §6 (`digestcheck.json`).

**The sections' own text never changed.** All 94 entries were found by matching the section `sha256`,
so every entry was keyed against the same section bytes that are at base. The lapse is entirely an
input gate failure, not a section-content edit.

Base state observed (`verify.txt` §1):

```
calibration_restraint_score 6
sections_covered 57 sections_total 64
UNCOVERED 131-245   ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
UNCOVERED 375-404   ## Restore discipline — before/after identity, not continuous non-write proof
UNCOVERED 1380-1395 ### The map — where a reader enters, artifact by artifact
UNCOVERED 1464-1478 ## Promotion-evidence calibration — fleet round-1
UNCOVERED 1479-1498 ## Repeated controls and gate registry — round 12
UNCOVERED 1517-1547 ## Pin disposition and provenance correction — round 13
UNCOVERED 1563-1596 ## Effective expectation reconciliation — round 14
```

`python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --explain`

The seven sections carry **94 ledger entries** (13, 16, 13, 1, 17, 20, 14) out of 497 in the base
ledger (3,489,570 bytes, `ledger.json` at base; `verify.txt` §4). Every one of the 94 entries fails
the input gate at base — that is why no entry credits and the section-level reason is the union.

---

## 2. The table — section × lapsed input × first drifting commit × class × recurrence

`first drifting commit` = earliest drift among the section's entries for that path (per-entry first
drifts differ; the `distinct drifts` column counts them, the full per-entry map is `table.json` /
`lapse.json`). `recurs?` is the measured touch history of that path over the 48 rounds
(`hist.json`: rounds are read from `round-NN` commit subjects).

| Section | input | class | first drifting commit | recurs? | entries recording | distinct drifts |
|---|---|---|---|---|---|---|
| recipe `SKILL.md:131` | `LOG.md` | record append | `67c0e01` 2026-10-23 | yes — 38/48 rounds, 104 commits | 2 | 2 |
| recipe `SKILL.md:131` | `SCORECARD.md` | record append | `67c0e01` 2026-10-23 | yes — 38/48 rounds, 95 commits | 2 | 2 |
| recipe `SKILL.md:131` | `corpus/QUALITY.md` | record append | `9f3084b` 2026-10-22 | yes — 32/48 rounds, 47 commits | 4 | 4 |
| recipe `SKILL.md:131` | `corpus/README.md` | record append | `9f3084b` 2026-10-22 | yes — 31/48 rounds, 44 commits | 13 | 6 |
| recipe `SKILL.md:131` | `corpus/SOURCES.md` | record append | `b05d2ee` 2026-10-22 | yes — 38/48 rounds, 52 commits | 4 | 4 |
| recipe `SKILL.md:131` | `corpus/knowledge/closeout-r11.md` | content edit of cited note | `d16f9b5` 2026-10-23 | no — round 35 only (2 commits) | 2 | 1 |
| recipe `SKILL.md:131` | `corpus/knowledge/incremental-pin-disposition.md` | content edit of cited note | `5054532` 2026-10-26 | no — rounds 13,14,17,18,48 (6 commits) | 2 | 1 |
| recipe `SKILL.md:131` | `corpus/knowledge/regression-tally-completeness.md` | content edit of cited note | `5054532` 2026-10-26 | no — rounds 30,48 (3 commits) | 1 | 1 |
| recipe `SKILL.md:131` | `corpus/knowledge/repeated-control-precondition.md` | content edit of cited note | `5054532` 2026-10-26 | no — rounds 12,16,48 (3 commits) | 2 | 1 |
| recipe `SKILL.md:131` | `corpus/knowledge/survivor-fixture-minimization.md` | content edit of cited note | `d16f9b5` 2026-10-23 | no — rounds 29,35 (3 commits) | 1 | 1 |
| recipe `SKILL.md:131` | `reports/round-1-calibration.md` | content edit of cited note | `583909a` 2026-10-24 | no — round 37 only (2 commits) | 1 | 1 |
| recipe `SKILL.md:131` | `tools/mutate-and-run.sh` | tool change | `bb68156` 2026-10-23 | no — rounds 16,17,18,26,30 (11 commits) | 3 | 1 |
| restore `SKILL.md:375` | `corpus/README.md` | record append | `66a25ab` 2026-10-21 | yes — 31/48 rounds, 44 commits | 16 | 11 |
| restore `SKILL.md:375` | `tools/mutate-and-run.sh` | tool change | `bb68156` 2026-10-23 | no — rounds 16,17,18,26,30 (11 commits) | 2 | 1 |
| map `SKILL.md:1380` | `corpus/README.md` | record append | `9f3084b` 2026-10-22 | yes — 31/48 rounds, 44 commits | 13 | 6 |
| map `SKILL.md:1380` | `corpus/knowledge/closeout-r11.md` | content edit of cited note | `d16f9b5` 2026-10-23 | no — round 35 only (2 commits) | 9 | 1 |
| map `SKILL.md:1380` | `tools/mutate-and-run.sh` | tool change | `bb68156` 2026-10-23 | no — rounds 16,17,18,26,30 (11 commits) | 4 | 1 |
| promotion `SKILL.md:1464` | `reports/round-1-calibration.md` | content edit of cited note | `583909a` 2026-10-24 | no — round 37 only (2 commits) | 1 | 1 |
| r12 `SKILL.md:1479` | `corpus/SOURCES.md` | record append | `9ee1c80` 2026-10-20 | yes — 38/48 rounds, 52 commits | 15 | 13 |
| r12 `SKILL.md:1479` | `corpus/knowledge/repeated-control-precondition.md` | content edit of cited note | `5054532` 2026-10-26 | no — rounds 12,16,48 (3 commits) | 17 | 1 |
| r12 `SKILL.md:1479` | `tools/mutate-and-run.sh` | tool change | `58e5d53` 2026-10-20 | no — rounds 16,17,18,26,30 (11 commits) | 7 | 3 |
| r12 `SKILL.md:1479` | `tools/trace-inputs.py` | tool change | `370f2df` 2026-10-21 | no — rounds 18,21 (2 commits) | 1 | 1 |
| r13 `SKILL.md:1517` | `.ufo/evidence/round-17/coldread/assemble.py` | tool change | `fad9e95` 2026-10-20 | no — round 17 only (3 commits) | 1 | 1 |
| r13 `SKILL.md:1517` | `.ufo/evidence/round-17/measure.py` | tool change | `fad9e95` 2026-10-20 | no — round 17 only (3 commits) | 1 | 1 |
| r13 `SKILL.md:1517` | `corpus/SOURCES.md` | record append | `58e5d53` 2026-10-20 | yes — 38/48 rounds, 52 commits | 18 | 15 |
| r13 `SKILL.md:1517` | `corpus/knowledge/incremental-pin-disposition.md` | content edit of cited note | `58e5d53` 2026-10-20 | no — rounds 13,14,17,18,48 (6 commits) | 20 | 2 |
| r13 `SKILL.md:1517` | `tools/bash-witness-study.py` | tool change | `58e5d53` 2026-10-20 | no — rounds 12,13,18,21 (4 commits) | 6 | 2 |
| r13 `SKILL.md:1517` | `tools/mutate-and-run.sh` | tool change | `58e5d53` 2026-10-20 | no — rounds 16,17,18,26,30 (11 commits) | 13 | 3 |
| r13 `SKILL.md:1517` | `tools/trace-inputs.py` | tool change | `370f2df` 2026-10-21 | no — rounds 18,21 (2 commits) | 4 | 1 |
| r14 `SKILL.md:1563` | `.ufo/evidence/round-14/context-missing-env.json` | tool change | **none — digest never matched** (§6) | no — round 14 only (1 commit) | 1 | — |
| r14 `SKILL.md:1563` | `corpus/SOURCES.md` | record append | `21e7932` 2026-10-21 | yes — 38/48 rounds, 52 commits | 13 | 12 |
| r14 `SKILL.md:1563` | `corpus/knowledge/incremental-pin-disposition.md` | content edit of cited note | `5054532` 2026-10-26 | no — rounds 13,14,17,18,48 (6 commits) | 14 | 1 |
| r14 `SKILL.md:1563` | `tools/bash-witness-study.py` | tool change | `370f2df` 2026-10-21 | no — rounds 12,13,18,21 (4 commits) | 3 | 1 |
| r14 `SKILL.md:1563` | `tools/evidence-disposition.py` | tool change | `370f2df` 2026-10-21 | no — rounds 14,17,18,21 (6 commits) | 3 | 1 |
| r14 `SKILL.md:1563` | `tools/mutate-and-run.sh` | tool change | `a08e85c` 2026-10-22 | no — rounds 16,17,18,26,30 (11 commits) | 11 | 2 |
| r14 `SKILL.md:1563` | `tools/trace-inputs.py` | tool change | `370f2df` 2026-10-21 | no — rounds 18,21 (2 commits) | 3 | 1 |

Rows per class: 10 record-file, 11 cited-note, 15 tool (36 section×input pairs; 12/2/3/1/4/7/7 rows
per section). Every row's commit is reproducible with
`git -C LANE show --stat <commit> -- <path>` (`diffs.txt` holds all 25 commit×path excerpts).

---

## 3. When each section actually fell off, and what killed its last clean entry

A section stays credited while **one** entry verifies (`coldread()` aggregation,
`.ufo/evidence/round-18/measure.py:620-645`). Its lapse commit is therefore the *latest* per-entry
first failure — when the last clean entry went stale (`lapse.json`, `verify.txt` §6).

| Section | pointers | entries | entry read rounds | first input drift | **lapse commit (round)** | rounds uncredited at base | first-lapse cause, by entry |
|---|---|---|---|---|---|---|---|
| recipe `SKILL.md:131` | 34 | 13 | 27–36 | `b05d2ee` (28) | `7500239` (37) | 11 | 13/13 record file (2 also tool) |
| restore `SKILL.md:375` | 10 | 16 | 21–36 | `66a25ab` (22) | `e118024` (38) | 10 | 16/16 record file (1 also tool) |
| map `SKILL.md:1380` | 17 | 13 | 27–36 | `9f3084b` (29) | `e118024` (38) | 10 | 13/13 record file (3 also tool, 1 also note) |
| promotion `SKILL.md:1464` | 5 | 1 | 17 | `583909a` (37) | `583909a` (37) | 11 | 1/1 cited note (no record input at all) |
| r12 `SKILL.md:1479` | 5 | 17 | 17–30 | `9ee1c80` (18) | `5054532` (48) | 0 | 15 record file, 4 tool, 1 note |
| r13 `SKILL.md:1517` | 9 | 20 | 17–31 | `fad9e95` (17) | `5054532` (48) | 0 | 17 record file, 5 tool, 2 note |
| r14 `SKILL.md:1563` | 10 | 14 | 18–30 | `21e7932` (19) | `5054532` (48) | 0 | 12 record file, 3 tool, 1 note |

Pointer counts are the frozen extractor's per-heading counts
(`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`; 90 total, matching the contract
floors 34/10/17/5/5/9/10). "rounds uncredited at base" counts the rounds after the lapse commit up
to base (round 48). The class counts in the last column can exceed the entry count: an entry whose
first-failure commit drifted several inputs at once is counted once per class (e.g. `58e5d53` moved
both a note and two tools, so r12's 17 entries yield 20 class counts).

Two different failure shapes are visible, and they matter to the planner:

- **recipe / restore / map** lapsed in rounds 37–38 and stayed lapsed for 10–11 rounds. Their late
  entries (read rounds 30–36) were re-keyed and still died 0–3 rounds after their read (median 1),
  because every one of them records `corpus/README.md` and/or `corpus/SOURCES.md`.
- **r12 / r13 / r14** were credited at the revision just before the base round's note edit and lost it
  there. Probed directly: at `5054532^` = `755298415f8c4eef3bed0c0d7625e2aacb03d6c2` the monitor
  reports `sections_covered 60/64`, with recipe, restore, map and promotion UNCOVERED and r12, r13,
  r14 **credited** (`explain-prev.json`; `python3 .ufo/evidence/round-21/coldread/measure.py --repo
  LANE --rev 755298415f8c4eef3bed0c0d7625e2aacb03d6c2 --explain`). Base is 57/64 — the round-48
  commit `5054532` cost exactly those three sections and nothing else.
  Their last clean entries are the six *record-free* ones (§4), and they were killed by `5054532`
  ("round-48: C2 records — … re-pointed entries"), which rewrote the `source:`/`verified-at:` header
  lines of `corpus/knowledge/incremental-pin-disposition.md`,
  `repeated-control-precondition.md` and `regression-tally-completeness.md` (2 insertions / 2
  deletions each, `diffs.txt`). The last clean entry of r12 is `ledger.json:29057` (read round 30),
  of r13 `ledger.json:30426` (read round 31), of r14 `ledger.json:29344` (read round 30) — all three
  are record-free, and all three died on that note rewrite.

---

## 4. The measured invariant: record-carrying entries survive ~1 round

Counting each entry's `inputs` against the five record files named in the contract
(`LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`):

- **88 of 94** entries carry at least one record file. Median survival
  (round of first failure − round of read) = **1 round**, min 0, max 3 (`survival.txt`).
- **6 of 94** entries carry none. Their survival: 20, 18, 18, 17 rounds, plus two round-17/18
  originals that died in their own round (0 and 1) on tool/note edits. The six, with ledger lines:

| section | entry | ledger line | read round | first failure |
|---|---|---|---|---|
| promotion | 0 | `ledger.json:2159` | 17 | round 37, `reports/round-1-calibration.md` (erratum appended) |
| r12 | 0 | `ledger.json:2202` | 17 | round 18, note + `tools/mutate-and-run.sh` |
| r12 | 16 | `ledger.json:29057` | 30 | round 48, `repeated-control-precondition.md` |
| r13 | 0 | `ledger.json:2411` | 17 | round 17, two `.ufo` scripts + note + tool |
| r13 | 17 | `ledger.json:30426` | 31 | round 48, `incremental-pin-disposition.md` |
| r14 | 13 | `ledger.json:29344` | 30 | round 48, `incremental-pin-disposition.md` |

So: an entry that records a record file has a half-life of one round (88/88 observations, max 3);
an entry that does not can survive 17–20 rounds. This is the quantitative form of "record appends
would recur on every round".

---

## 5. What the first-drift commits actually changed

Grouped by commit (`commits.json`, `diffs.txt`; each verifiable with `git show --stat <c> -- <path>`):

| commit (round) | paths in the table | what the commit did |
|---|---|---|
| `fad9e95` (17) | r13: `.ufo/evidence/round-17/coldread/assemble.py`, `measure.py` | **tool change**: 288+/31− and 84+/26−; adds `live_lane_reads`, `read_rev` validation, trace hardening to the round-17 cold-read tooling |
| `9ee1c80` (18) | r12: `corpus/SOURCES.md` | record edit: 11+/4−; rewrites the S001 row's `used-by` cell (adds `mutation-case-kumitate-sources-check.md`) |
| `58e5d53` (18) | r12/r13: `corpus/SOURCES.md`, `incremental-pin-disposition.md`, `bash-witness-study.py`, `mutate-and-run.sh` | mixed: record edit (S008 row rewrite, 15+/2−), note append (ER-jj2 block, 2+/0−) and tool changes (eighth leg `js-sources-check` in the runner, 102+/28−; `GIT_*` scrub + hostile-env selftest in the witness study, 122+/12−) |
| `21e7932` (19) | r14: `corpus/SOURCES.md` | record edit: 9+/1−; rewrites S049's `used-by` cell |
| `370f2df` (21) | r12/r14: `trace-inputs.py`, `bash-witness-study.py`, `evidence-disposition.py` | **tool change**: selftest additions (5+/1−, 41+/6−, 23+/0−) |
| `66a25ab` (22) | restore: `corpus/README.md` | record append: 11+/0−, new `## Round22 — callback-authoritative accounting` section |
| `a08e85c` (26) | r14: `tools/mutate-and-run.sh` | **tool change**: 96+/20−, ninth leg `js-cite-check` |
| `b05d2ee` (28) | recipe: `corpus/SOURCES.md` | record edit: 15+/1−, S059 re-open + S104 correction |
| `9f3084b` (29) | recipe/map: `corpus/QUALITY.md`, `corpus/README.md` | record appends: 34+/0− (criteria 55, 56) and 18+/0− (`## Round 29`) |
| `bb68156` (30) | recipe/restore/map: `tools/mutate-and-run.sh` | **tool change**: 65+/1−, r30 tally guard (`SETUP (case-tally mismatch)`) + behavioural selftest |
| `67c0e01` (31) | recipe: `LOG.md`, `SCORECARD.md` | record append: 18+/0− and 14+/0−, round-31 measured result |
| `d16f9b5` (35) | recipe/map: `closeout-r11.md`, `survivor-fixture-minimization.md` | **note edit**: 4+/0− and 2+/0−, new `source:`/`verified-at:`/`recheck:` header blocks |
| `583909a` (37) | recipe/promotion: `reports/round-1-calibration.md` | **note edit**: 9+/0−, box-3 erratum appended |
| `5054532` (48) | recipe/r12/r13/r14: three knowledge notes | **note edit**: 2+/2− per note — header re-point to superseding sources S265/S267 |

The record files are *not* append-only in diff shape even though they are read-only records in the
contract's sense: `corpus/SOURCES.md` accumulates 540 insertions but also 50 deletions over 52
commits (row re-writes, e.g. `9ee1c80`, `58e5d53`, `21e7932`), and `corpus/README.md`/`QUALITY.md`
get new sections appended (601/10 and 1443/1). The class in the table therefore means "this is one
of the five record files the contract exempts", not "this diff is an append".

---

## 6. Divergences and anomalies found

1. **A ledger entry records a digest that never existed.** `.ufo/evidence/round-21/coldread/ledger.json:24170`
   (section r14, entry 9, `read_rev` `b05d2ee8`) records
   `.ufo/evidence/round-14/context-missing-env.json` =
   `9a3a3f9b5a62c1e5a0cf4a0a4b4f7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b` — a patterned placeholder,
   not the blob (`1ee9d09b…` at both its read_rev and base; the path has exactly one commit, round
   14, `4d409d7`). The monitor reports this as `input-drift:`, which is the wrong name: it never
   matched, so no commit "drifted" it. It does not change the r14 verdict (that entry also fails on
   real drifts), but a re-key that copied this entry's `inputs` verbatim would carry a permanently
   failing input. `digestcheck.json`.
2. **The `--explain` per-section `reason` is a union, not a per-entry attribution.** Recipe shows 12
   paths, but entry 1 (`ledger.json` read `b05d2ee8`) drifts only `corpus/README.md` while entry 12
   (read `e423c41b`, `ledger.json:40181`) drifts five record files at once. A planner who reads only
   the union cannot tell which re-keying round each path belongs to — the per-entry map is in
   `table.json`/`lapse.json`.
3. **The round-48 note re-point is the base-round trigger, not a record append.** For r12/r13/r14 the
   last clean entries were record-free since rounds 30–31; `5054532` rewrote the three knowledge
   notes' header lines and lapsed all three sections in the same round. The section-level reason
   strings still list `corpus/SOURCES.md` (also changed in `5054532`), which obscures that the
   *decisive* input was a note.
4. **Record files are exempt in the contract but are also the only per-round churn.** Five files are
   touched in 31–38 of 48 rounds; the notes in 1–5 rounds; the tools in 1–5 rounds. Nothing else in
   the table recurs at round cadence.

---

## 7. Planning data for the C1 planner

- **Re-keying without dropping records cannot hold.** 88/94 entries that carry a record file lapsed
  within ≤3 rounds (median 1). The three sections that lapsed in rounds 37–38 were re-keyed
  repeatedly across their read rounds (21–36) and still fell off; the re-key itself is not the fix,
  dropping record inputs is.
- **Dropping records is necessary and, measured, sufficient for ~17–20 rounds.** The six record-free
  entries survived 17–20 rounds; the only shorter ones are the round-17 originals that included
  `.ufo` scripts or tools as inputs.
- **Residual risk after the C1 re-key is note/tool rewrites, and it is already realized.** Three
  notes were rewritten in the base round: `incremental-pin-disposition.md` (rounds 13,14,17,18,48),
  `repeated-control-precondition.md` (12,16,48), `regression-tally-completeness.md` (30,48). A
  section re-keyed now will lapse again the next time one of its cited notes gets a `source:` header
  re-point — which is what a source supersession does (S026→S265, S093→S267 this round).
  Tools last edited: `mutate-and-run.sh` r30, `trace-inputs.py` r21, `bash-witness-study.py` r21,
  `evidence-disposition.py` r21 — lower but non-zero risk.
- **Per-section stability of the non-record inputs the re-key would pin:**
  - recipe: `closeout-r11.md` (last r35), `survivor-fixture-minimization.md` (r35),
    `reports/round-1-calibration.md` (r37), `incremental-pin-disposition.md` (**r48**),
    `repeated-control-precondition.md` (**r48**), `regression-tally-completeness.md` (**r48**),
    `mutate-and-run.sh` (r30).
  - restore: only `corpus/README.md` (record, must go) and `mutate-and-run.sh` (r30).
  - map: `README.md` (record), `closeout-r11.md` (r35), `mutate-and-run.sh` (r30).
  - promotion: its single entry has **no** record input; its only input is
    `reports/round-1-calibration.md` (r37). A record-drop re-key changes nothing here — the section's
    credit depends on never re-editing that report.
  - r12/r13/r14: their surviving entries already pin the notes that were rewritten in round 48, so
    the re-key must record the **post-`5054532`** note bytes, and must not copy `ledger.json:24170`'s
    entry.
- **Do not treat the 12/2/3/1/4/7/7 path counts as pointer counts.** They are ledger-input counts;
  the section pointer floors are 34/10/17/5/5/9/10 (`c1-pointers-at-base-8ca67421.json`), which the
  C1 predicate requires to be preserved. Nothing in this archaeology bears on pointer resolution.
- **Recurrence answer, stated once:** record-file append (and in-place row edit) recurs **every
  round** — 31–38 of 48 rounds, 44–104 commits per file; cited-note edits and tool changes are
  **episodic** — 1–5 rounds each, and in this lane they cluster in tool-building rounds (17–21, 26,
  30) and in source-supersession rounds (35, 37, 48).

---

## 8. Artifacts and commands

All under `.ufo/waves/round-49/w1/T49RevengerLapse/`:

| file | content |
|---|---|
| `verify.txt` | the six verification blocks quoted above (monitor summary, union match, attribution checks, ledger size/placeholder, survival, lapse commits) |
| `explain.txt` | full `--explain` JSON at base (2245 lines), the probe this analysis starts from |
| `explain-prev.json`, `prev-probe.txt` | the same probe at `5054532^` (60/64; r12/r13/r14 credited), the round-48 trigger measurement |
| `drift.json` | per entry: read_rev, verdict, commands, `inputs`, `fails` |
| `table.json` | the section×input rows behind the table, with per-entry drift commits |
| `lapse.json` | per entry first-failure commit; per section lapse commit |
| `hist.json` | per path: every distinct blob, its commit and subject history |
| `commits.json` | the 14 first-drift commits: full sha, date, subject, name-status, shortstat |
| `diffs.txt` | the 25 commit×path diff excerpts classified in §5 |
| `survival.json`, `survival.txt` | the 94-entry survival table and the record/no-record split |
| `entrylines.json` | each of the 94 entries' `ledger.json` line number, read_rev, inputs_dropped |
| `ledgerlines.json` | all 497 base-ledger entries with their line numbers |
| `digestcheck.json` | the one digest that does not match its own read_rev |
| `ledger-at-base.json` | `git show 8ca67421:.ufo/evidence/round-21/coldread/ledger.json` (unmodified copy) |
| `entries2.out` | per entry: input count, record inputs, failing inputs (the per-section detail behind §3–§4) |

Reproduce:

```
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=8ca67421111fa354b47b803358391d0b07fc6db9
python3 "$LANE/.ufo/evidence/round-21/coldread/measure.py" --repo "$LANE" --rev "$BASE" --explain
git -C "$LANE" rev-list --reverse "$BASE" -- <path>          # blob history of one input
git -C "$LANE" cat-file blob <commit>:<path> | sha256sum     # digest per commit
git -C "$LANE" show --stat <commit> -- <path>                # what the drift commit changed
```

Per-entry input recomputation (frozen helpers, no scoring) is spelled out in `verify.txt` §2.

Tooling: no install or upgrade was made (pacman is paused host-wide; nothing was needed — Python 3.14
stdlib and git only).

## Summary

- All 7 uncovered sections fail only the ledger input gate; their section bytes are unchanged, so the lapse is 100% input drift.
- 36 section×input pairs: 10 record-file, 11 cited-note, 15 tool. Record files recur every round (31–38 of 48 rounds); notes/tools are episodic (1–5 rounds).
- 88 of 94 entries carry a record file and lapsed in a median of 1 round (max 3); the 6 record-free entries survived 17–20 rounds.
- recipe/restore/map lapsed at rounds 37–38 (7500239, e118024) and lost 10–11 rounds of credit; promotion at round 37 (583909a, a note edit).
- r12/r13/r14 are credited at 5054532^ (probe: 60/64, those three credited) and uncredited at base (57/64); the base-round commit 5054532 rewrote three knowledge-note headers and killed their last, record-free entries.
- One ledger entry (ledger.json:24170) records a fabricated digest for .ufo/evidence/round-14/context-missing-env.json — never matched, so "input-drift" mislabels it; a re-key must not copy it.
- Re-keying without dropping the five record files reproduces the lapse; dropping them leaves note/tool rewrites as the residual trigger (already realized in round 48).
- The C1 re-key must record the post-5054532 note bytes; promotion's single entry has no record input and depends only on reports/round-1-calibration.md staying unedited.
