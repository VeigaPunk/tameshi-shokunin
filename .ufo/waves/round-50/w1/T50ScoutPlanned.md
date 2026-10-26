# T50ScoutPlanned — planned-row inventory, rounds 40-49 (read at e3729de862f73ae080d98fcf522a7081ce16e40a)

Seat T50ScoutPlanned (scout; read-only). Every path:line below is at `e3729de` (read from a `git archive` of that
revision, not the HEAD worktree: HEAD `4afb060` adds the round-50 pre-registration section and restates the standing
axis table, which changes the status of R49.4 only — see the last section). Nothing here is a verdict; a ledger row's
status is the L1's judgment against the counter's rules.

Commands used (all re-runnable):
- `git -C LANE show e3729de:SCORECARD.md | grep -n 'Planned (round'` -> the 17 Planned lines below (1666 ... 2410).
- `git -C LANE show e3729de:corpus/lessons/round-NN.md | grep -n -i 'routed\|carried\|Holds'` for rounds 40-49.
- `python3 -c "import json;..."` over `.ufo/evidence/round-50/c1/defects.json` for the 49 ids and keys.
- file/line spot reads with `sed -n A,Bp` on the archive.

`Planned (round 42)` and `Planned (round 43)` paragraphs do not exist (SCORECARD.md:2102 says so for 43; the round-42
block has none); rounds 42-43 declared their next-round work only in lesson `## Holds` (round-42.md:172-260,
round-43.md:184-214). Rounds 46 and 47 carry a second block each (`:2253-2255` disposition + additions).

## 1. Table: planned item -> later round -> id

Status column = what the tree at `e3729de` shows: DONE (thing exists; file:line), PART (some asks met), OPEN, DROPPED
(stopped being listed in any Planned paragraph without being done; tree unchanged).

| # | Planned in (SCORECARD line) | Item | Later round did it? (file:line of the thing) | Spot-check id | Status @e3729de |
|---|---|---|---|---|---|
| 1 | r35 (:1666) | v3 residue classes in round-34 Holds: Guard-2 divisibility, TallyArms-02 coexistence, quoted case subject, helper-function refactors, per-index record parsing, preamble seeding, nonzero-leg stress, all-pairs nlegs recompute | Never. Listed again only as "open recall classes in the lesson Holds" r36 (:1726), r37 (:1773); no later Planned names them. `tools/tally-audit-v3.py` was last edited at r37 (`git log` -> `ae9b771`); `grep -n -i 'divisib\|coexist\|preamble\|per-index\|all-pairs\|nonzero-leg' tools/tally-audit-v3.py` -> 0 lines. Source list: `corpus/lessons/round-34.md:54-64`; also round-35.md:144-157 (stderr outside tuple, removed-workdir effect) | none | DROPPED (open in tree) |
| 2 | r36 (:1726) | cold-read refresh for the four drifted headings | r36 C1 (SCORECARD.md:1743), score 6->8 | none | DONE (r36) |
| 3 | r36 (:1726) | public-slot cardinality/distinctness asserts in a successor counter | r36 C2 `c1-measure-v2.py` (SCORECARD.md:1744) | none | DONE (r36) |
| 4 | r36 (:1726), r37 (:1773) | `code_view` ANSI-C `$'…'` quote class | r37 C2 (SCORECARD.md:1803), capability row :1809; `tools/tally-audit-v3.py:157-161` | none | DONE (r37) |
| 5 | r38 (:1817) | nested command-substitution quoting + unquoted backslash-newline holds | Not lifted. `tools/tally-audit-v3.py:160-161` still says "nested command substitutions and unquoted backslash-newline continuations remain outside this view"; same text at SCORECARD.md:1809/2191/2283/2347; `corpus/lessons/round-37.md:24`. Never in a Planned paragraph after r38 | none | DROPPED (open in tree) |
| 6 | r39 (:1847) | F4 write-path census over the surveyed gates | r39 C2 (SCORECARD.md:1860; `tools/write-path-census.py`) | none | DONE (r39) |
| 7 | r39 (:1847), r40 (:1868), r41 (:1893), r44 (:2076), r45 (:2145) | comparator lattices beyond POSIX `diff`: `cmp`, `git diff --exit-code` | Never measured. `corpus/knowledge/golden-comparison-verdict.md:50-51` still says they are not covered; the word `cmp` as an item last appears in :2145 (r45 Planned) and in no later Planned paragraph | none | DROPPED after r45 (open in tree) |
| 8 | r39 (:1847) | "the two named holds in the round-38 lesson" | round-38.md:111-119: hold 1 = F4 write census (row 6, done), hold 2 = comparators (row 7, open), hold 3 = rule generalised to own fixtures (never done; no later Planned) | none | PART |
| 9 | r40 (:1868) | write forms the frozen pattern misses: `.write_bytes`, `os.replace` | r40 C1: `tools/write-path-census-v2.py:1`, SCORECARD.md:1876 (row), :1889 (capability) | none | DONE (r40) |
| 10 | r41 (:1893) | v2 misses a variable destination on `os.replace` | r41 C: `tools/write-path-census-v3.py:1`, capability row SCORECARD.md:1920; v3 tests `v3_variable_replace` at `tools/write-path-census-v4.py:619-634`; r41 knowledge `corpus/knowledge/r41-variable-destination-writes.md:67` | maps to R41.4, R41.5 (v3 false positives, v3 docstring) — resolved by v4 not by editing v3: `corpus/lessons/round-42.md:247-252` | DONE (r41/r42) |
| 11 | r42 lesson Holds (no Planned) | v4 limits: 23 constructed false negatives; `explicit_out` default; C2 survivors `outflag_no_parse_args_check`, `method_fold_several_returns` | survivors resolved r43 (SCORECARD.md:2104; `corpus/knowledge/r43-survivor-resolution-rule.md`) | R42.1 | DONE (r43) for survivors; v4's 23 false negatives are "disclosed, not repaired" (round-42.md:207-228) and never planned |
| 12 | r43 lesson Holds :199 | staged file's own digest not printed (sentinel F4; "routed to round 44") | guard prints `staged_sha256`: `tools/staged-id-guard.py:52-53`; observed in round-45.md:67 | none | DONE (r44/r45) |
| 13 | r43 lesson Holds :203-208 + r44 Planned (:2076) + r45 Planned (:2145) | whole-set staged adoption: a map over all 103 staged rows, injective and disjoint from the registry | Never built. Rows were adopted piecemeal by document (S256-S257 r45, S258-S260 r46, S261-S264 r47, S265-S268 r48: `corpus/SOURCES.md:136-143`); `corpus/SOURCES.md:490-492` still reserves staged S161-S255 "by document for the package". Not in the r46+ Planned paragraphs | none (R41.6/R42.3 are the *collision* hazard, answered r43-r47; not the whole-set map) | DROPPED after r45 (open) |
| 14 | r43 lesson Holds :209-214 + r44 (:2076) + r45 (:2145) | two guard refusal classes: (a) prose-document row refused as `unmapped` without saying which cause fired; (b) a registry row itself indented four spaces invisible to both patterns | Not touched: `tools/staged-id-guard.py` last commit `6b83a11` (r43); `:143-147` still appends to one `unmapped` list with no cause; no 4-space handling | none | DROPPED after r45 (open) |
| 15 | r44 (:2076), r45 lesson | S089 anchor supersession | S160 (`corpus/SOURCES.md:130`, :479) | R43.3 | DONE (r44; before the spot-check was written? R43.3 routed_at `506e99c`, fix commit in r44) |
| 16 | r46 (:2163) | kill the round-45 C1/C2 counter selftest survivors | answered by r46 C2 (SCORECARD.md:2253, first clause); receipts `.ufo/evidence/round-46/selftest/c{1,2,3}-selftest.{stdout,exit}`; r47 pool 183/183 `SCORECARD.md:2318` | R45.2 | DONE (r46/r47) |
| 17 | r46 (:2163; "stay open" :2253; carried r47 :2255, r48 :2312) | per-snapshot fetch receipt in the freshness ledger | r48 C2: S265-S268 rows with receipts, `corpus/SOURCES.md:140-143`, `corpus/lessons/round-48.md:49,76`, `SCORECARD.md:2363` | R46.1 (also R45.4 in part) | DONE (r48) for S026/S093/S108 (+S048) |
| 18 | r46 (:2163) | re-pin the five anchor-refresh candidates of `.ufo/waves/round-45/w2/ConnDriftAnchors.md` | **Only part.** The file names five open candidates S153, S154, S157, S159, S100 (`ConnDriftAnchors.md:22,36-40,43-45`: "open one supersede row per drifted document"). r48 superseded S026/S048/S093/S108 (not on that list). `grep -n 'supersede' corpus/SOURCES.md` shows no supersede row for S153/S154/S157/S159/S100 | R45.4 (its text counts "five anchor-refresh candidates" and S026/S093/S108) | OPEN for the five; **R45.4 is a compound item and its five-candidate ask is unmet** |
| 19 | r47 (:2228) | route MutC3Counter / MutDriver selftest gaps (round-46 w1) into a successor hardening claim | r47 C2 hardened the *v2 freshness/coverage counters* (`contract.json:38`), not the round-46 C3 counter or the driver; `w1/MutC3Counter.md`'s 4 survivors and `MutDriver.md`'s 8-case gap have no later receipt | none (R47.5 names the *round-47* counters' survivors, a different set) | OPEN |
| 20 | r47 (:2228) | F3 next package rows S155, S169, S206; S158 PDF needs a text snapshot | S155 -> S261, S158 -> S262, S206 -> S263, (+S207 -> S264): `corpus/SOURCES.md:136-139`, `corpus/lessons/round-47.md:68`. `grep -n S169` over lessons/SOURCES/SCORECARD (excluding the Planned line) -> 0 | none | PART (S169 not adopted; never relisted) |
| 21 | r47 (:2228) | pin five tool-less statements by sha256 | r47 C1: all 22 rows carry a tool sha256 (`SCORECARD.md:2264`, `contract.json:24`) | R46.3 (second half) | DONE (r47) |
| 22 | r47 additions (:2255) | hermetic observation of frozen statements (pin `jj`/`bwrap`/census inputs) | r47-r48 replaced hermeticity with a declared `deps` clause + `runs 3` value class (`SCORECARD.md:2264-2276`, `:2334`); the observation itself is still host-dependent (`SCORECARD.md:2328`). Spot-check ask R46.3 is "make the frozen observation hermetic" | R46.3 | PART: judge R46.3 as compound (sha256 done; hermetic not) |
| 23 | r47 additions (:2255) | absorb wave-2 killing cases; sealed held-out set; AST-pin control; "killed only when a named rule case fails" | r47 C2 `killed=183 applicable=183 neutral_killed=0` (`SCORECARD.md:2318`); `.ufo/evidence/round-47/hardening/pool.py:251-261`, `contract.json:8,18,48` (CTL_E ast pin) | R46.2 | DONE (r47) |
| 24 | r47 closure routing -> r48 (:2312) | selftest receipts for the three r47 counters, `addition-lint.py`, criterion-93 falsifier | **Not done.** `.ufo/evidence/round-47/selftest/` does not exist; `.ufo/evidence/round-47/quality/` holds `c91-92-falsifiers.stdout` only (no c93 block receipt); r48 committed receipts for its own counters (`.ufo/evidence/round-48/selftest/`), r49 for its own (`corpus/lessons/round-49.md:140`). Routed text: `corpus/lessons/round-48.md:306-307` | R47.2 | OPEN |
| 25 | r48 (:2312), r49 (:2367) | delete or re-pin the dead `brace_depth_at` helpers | still present: `tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:234` (`grep -n 'def brace_depth_at' tools/*.py`) | R47.5, R48.4, R49.5 | OPEN |
| 26 | r48 (:2312), r49 (:2367) | selftest cases for the C1 counter's 8 and the C3 counter's 10 round-47 survivors (`w1/T47MutC1Counter.md`, `T47MutC3Counter.md`) | No new selftest cases landed; r49 only restates (:2367). Plus later survivor sets: `T49MutC1Counter.md` (14 of 28), `T49MutC2Counter.md` (9 of 15) in `corpus/lessons/round-49.md:101,115` | R47.5, R48.4, R49.2 (partly) | OPEN |
| 27 | r48 (:2312) | located-name (entry-author) check; r49 amended (:2380) restates | no tool/QUALITY text: `grep -rn -i 'located.name\|entry-author' tools corpus/QUALITY.md` -> 0 | R47.5, R48.4 | OPEN |
| 28 | r48 closure -> r49 amended (:2380) | append-only rule for landed seat reports (round-47 conformance defect 2) | no QUALITY text added: `grep -n -i 'seat report' corpus/QUALITY.md` -> 0 lines carrying the rule | R48.4 | OPEN |
| 29 | r48 (:2312), r49 (:2367) | continue F3/F7 from the package: S161/S162/S205 | none adopted: `grep -c '1810.05286\|S205' corpus/SOURCES.md` -> 0; r48 lesson refused the one S205-citing entry (`round-48.md:270`); S161/S162 appear only in Planned | R48.4, R49.5 (key `S205`; S161/S162 unkeyed) | OPEN |
| 30 | r49 (:2367) | decide: pinned-leg successor for `six-leg regression ledger`, or declared nondeterministic | no decision recorded in the r49 section (:2386-2410); the standing row still reads `runs 3 stable` (:2334) while :2328 discloses the race | R48.4 (key `six-leg regression ledger`) | OPEN (decision) |
| 31 | r49 amended (:2380) | decision on re-pinning the lapsed cold-read sections (rounds 12/13/14) | r49 C1: `sections=64 covered=64 ... total=0 C1_R49_PASS=true` (SCORECARD.md:2397-2400 region) | R48.1 | DONE (r49) |
| 32 | r49 amended (:2380) | deciding script writes start+exit before output is read; drops receipt dirs from the frozen path list | `.ufo/evidence/round-49/deciding-run.sh:6-10` | R48.2 | DONE (r49) |
| 33 | (no Planned; spot-check) | pre-registered control order; `--only` previews declared | `deciding-run.sh:6,23-27` gate 0 (controls committed after freeze); r49 report text | R48.3 | DONE (r49), judge on evidence rule |
| 34 | r50 (:2410) | successor C1 counter capping `absent` and requiring evidence for it | not at base. (This round's C1 counter is the routed-ledger counter, not the cold-read counter.) `corpus/lessons/round-49.md:108-114` | R49.2 | OPEN (declared r50) |
| 35 | r50 (:2410) | C2 counter's differential-generator blind spot | not at base; `corpus/lessons/round-49.md:96-100` | R49.2 | OPEN (declared r50) |
| 36 | r50 (:2410) | generator reach: 5-cell rows, duplicate map keys, numeric order past the digit boundary | not at base. Receipts: `.ufo/waves/round-49/w2/T49W2MutGenerator.md:72,127-129` (M16 5-cell, M04 numeric sort, M21), `T49W2MutGuardOwn.md:112,152` (m11 5-cell, m12 duplicate keys), `T49W2ExecC2Probe.md:151` | none (R49.1 is error paths, not reach) | OPEN, no id |
| 37 | r50 (:2410) | SKILL.md:1503/1509/1555 outside-section corrections | at `e3729de` those lines are unchanged (`git show e3729de:SKILL.md | sed -n '1503p;1509p;1555p'`); HEAD same | R49.3 | OPEN |
| 38 | r50 (:2410) | "carried items from round 48's list" | = rows 25-30 above | R48.4, R47.5 | OPEN |
| 39 | r49 lesson routed (not in any Planned) | generator error paths: unreadable guard exits 1 where the docstring says 2 (`tools/pbt-staged-id.py:41` vs `main()` `:982`, only `os.path.isfile`) | not fixed at base | R49.1 | OPEN |

Spot-check ids with **no planned counterpart** (the ledger needs no Planned entry unless open): R40.1-R40.4 (typos/
labels; R40.1 and R40.4 were noted as corrected by `corpus/lessons/round-41.md:53` and :75), R40.5 (depth guard:
SCORECARD.md:1859 is the r39 guard-agreement C1, but R40.5's routed_at is `a3d6c69`, after it, so the keyed excerpt
must be new since routing), R41.1-R41.3 (R41.3 successor pair = r42 C1: `corpus/lessons/round-42.md:172-215`), R41.7
(left as is on purpose: `round-42.md:254-256` -> a `declined` reason candidate), R42.2, R42.4, R43.1 (S256/m7:
`round-44.md:88`), R43.2 (`round-44.md:85`), R44.1 (r45 lesson `:158` names the 28-token count; no edit to
`round-44.md`), R44.2, R45.1 (`round-46.md:121`), R45.3 (`round-46.md:129`), R46.4 (`.ufo/evidence/round-47/quality/
round46-lesson-dash-restored.md`), R47.1 (r48 `runs 3` rows, SCORECARD.md:2334), R47.3 (`round-48.md:121`), R47.4
(`round-48.md:270`), R47.6, R48.5 (`SCORECARD.md:2382`), R49.4, R49.6, and the SHONEN ids (R42.4, R46.5, R47.7, R48.6,
R49.6): none ever carries a Planned entry; SHONEN promotion is operator-owned.

## 2. Planned items still open at e3729de with NO spot-check id

These must be carried by the L1's new `Planned (round 50...)` paragraph in addition to the ids; none can be reached by
an id-keyed ledger row.

1. `cmp` / `git diff --exit-code` comparator lattices (rows 7-8; planned r39, r40, r41, r44, r45; dropped after r45).
   Evidence: `corpus/knowledge/golden-comparison-verdict.md:50-51`; `corpus/lessons/round-38.md:116-119`.
2. Whole-set staged adoption map over the 103 staged rows (row 13; planned r44, r45; dropped after r45).
   Evidence: `corpus/SOURCES.md:490-492`, `corpus/lessons/round-43.md:203-208`.
3. Guard refusal classes (row 14): prose-document `unmapped` without a cause message; four-space-indented registry row
   invisible to both patterns. Evidence: `corpus/lessons/round-43.md:209-214`, `tools/staged-id-guard.py:143-147`.
4. Round-46 survivors not closed by r47: `.ufo/waves/round-46/w1/MutC3Counter.md` (4 of 22), `MutDriver.md`
   (predicate assembly untested), `CritC3Control.md` (18 of 22 cheat variants pass) (row 19; planned r47, never resolved).
5. S169 (r47 F3 rank) and S161/S162 (r48 candidates) never adopted (rows 20, 29). S205/F7 has an id (R48.4/R49.5).
6. Round-35/36 residue: v3 residue classes (row 1), `stderr` outside the compared tuple and removed-workdir effect
   (`round-35.md:152-157`), nested command-substitution and unquoted backslash-newline (row 5; hold from r38, dropped).
   These were last named in the r37/r38 Planned paragraphs.
7. Generator reach: 5-cell rows, duplicate map keys, numeric ordering (row 36; named in the r50 Planned line only).
8. Round-49 lesson routed items with no id and no Planned line: C1 selftest never calls `measure()` (`round-49.md:101`),
   C2 counter gaps F4-F7 (`:115`), `deciding-run.sh` runs working-tree code (`:104`, T49RevDeciding F1-F2),
   generator oracle is a transcription of the guard's rules (`:123`), guard docstring names exit 1 only for an
   inadmissible map (`:127`; the lesson says the guard "is not edited" -> a `declined` candidate, but no one filed it),
   the round-21 ledger entry whose digest never matched (`:106`, "left as written" -> `declined`-shaped).
9. Round-42/43 "disclosed, not repaired" instrument limits (`round-42.md:172-228`, `round-43.md:142-200`): never
   planned; listed only so the L1 does not mistake them for planned work.

## 3. Findings the L1 should weigh for the ledger (judgment is the L1's)

- **R45.4 is a compound item and not fixed:** it asks for the five anchor-refresh candidates in `ConnDriftAnchors.md`
  and a pin-by-quote for S026/S093/S108. r48 did the second (S265/S267/S268 rows, `corpus/SOURCES.md:140-143`) but
  there is no supersede row for S153, S154, S157, S159 or S100 (row 18). Marking R45.4 `fixed` on the r48 commit
  would credit the wrong half; `open` needs the id in the Planned paragraph.
- **R47.2 is open, not fixed:** round-47 selftest receipts and the criterion-93 falsifier receipt are not in the tree
  (row 24). r48/r49 committed receipts for their own counters only.
- **R47.5 and R48.4 are compound and open** (brace_depth_at at `tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:
  234`; 8+10 survivors; located-name; append-only rule; S205; six-leg decision). R49.5 restates R48.4.
- **R46.3 is compound:** the sha256 half is done (r47, SCORECARD.md:2264); the hermetic-observation half became a
  declared `deps` clause (SCORECARD.md:2276, :2328 still discloses host dependence). A `fixed` row must carry text for
  both asks; otherwise `open`.
- **R46.1 is fixable as `fixed`** on the r48 commit (receipts + S026/S093/S108 re-pinned by quote; `SOURCES.md:140-143`,
  `round-48.md:49,76`), subject to the counter's keyed-excerpt-new-since-routing rule (routed_at `0b5b7cd`).
- **R49.4 changed after the base:** at `e3729de` the standing axis table still reads `calibration | 6`; HEAD `4afb060`
  ("standing axis table restated with round-49 values (routed R49.4)") is post-routing and touches SCORECARD.md, so
  the L1 can cite it as the fix commit for R49.4 (verify the keyed excerpt is absent at `e3729de`: key `calibration | 8`).
- **R49.1 and R49.3** stay open at both `e3729de` and HEAD (`tools/pbt-staged-id.py:982`; SKILL.md:1503/1509/1555).
- Candidates for `fixed` by evidence found above: R40.1 (round-41.md:53 acknowledges, but it is a spot-check/lesson
  correction whose keyed text must be new in a non-spot-check file at a post-routing commit), R41.3 (r42 C1), R41.4/
  R41.5 (v4, `round-42.md:247-252`), R42.1 (r43), R43.2/R43.3 (r44), R45.1-R45.3 (r46), R46.2 (r47), R47.1/R47.3/R47.4
  (r48), R48.1-R48.3, R48.5 (r49). Whether each excerpt is absent at `routed_at` is for the counter's `--explain`; I did
  not run any counter.
- Candidates for `declined` (the lane's own text already states the reason): R41.7 (`round-42.md:254-256`), R44.2 and
  R47.6/R42.2 are observations (status-neutral), R49.6/R48.6/R47.7/R46.5/R42.4 SHONEN (operator-owned).

Tools installed/updated: none. Scratch `/fast/scratch/hyaku/tameshi-r50/T50ScoutPlanned/` (git archive of e3729de) removed before yield.

## Summary
- 39 planned/routed work items inventoried from Planned (round 35, 36-41, 44-50) + lessons 40-49; r42/r43 have no Planned paragraph (Holds only).
- Done later: rows 2-4, 6, 9-12, 15-17, 21, 23, 31-33 (file:line in table).
- Still open at e3729de AND mapped to ids: brace_depth_at (R47.5/R48.4/R49.5), r47 survivors, located-name, append-only rule, S205, six-leg decision, SKILL.md 1503/1509/1555 (R49.3), generator error paths (R49.1), C1 `absent` + C2 differential (R49.2), selftest receipts (R47.2), five anchor-refresh candidates (R45.4).
- Open with NO id (L1's Planned paragraph must add): cmp/git-diff lattices; whole-set staged adoption; guard refusal classes; r46 C3/driver survivors; S169 and S161/S162; r35 residue + nested-substitution/backslash-newline holds; generator reach; r49 lesson items without id.
- R45.4, R46.3, R47.5, R48.4 are compound items: not `fixed` unless every ask is met; R47.2 is open (no r47 selftest receipts).
- R49.4's fix commit is post-base (HEAD 4afb060); R49.1/R49.3 remain open at HEAD.
- No counter was run; no lane file other than this report was touched.
