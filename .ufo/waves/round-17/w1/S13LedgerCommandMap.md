# S13 — round-16 ledger: command → input map, and drift at `98bea7d`

Seat `TameshiR17.S13LedgerCommandMap`, round-17 wave 1. Read-only: no lane writes
outside this report, no git writes, no `jj`, no mutation, no tool installs or
upgrades. Scratch: `/tmp/tameshi-r17w1-S13LedgerCommandMap-FmQ7Xp`.

Question: for each crediting ledger entry, which class is it, what did it execute
(from the seat-report JSON `commands_executed`), which lane files did those
commands read, and which of those under `tools/` or `.ufo/evidence/` have changed
between the entry's read rev and `98bea7da5801f4bc58e4187690ee1687c8a5061f`.
O = observed, I = inference, U = unknown. Every function-level file inference is
marked `[I]`; commands and counts are O from the committed reports.

## Method (so the map can be re-run)

- Ledger: `.ufo/evidence/round-16/coldread/ledger.json`, schema
  `tameshi-coldread-ledger-v1`, 75 entries; every entry has
  `commands_executed_count > 0`.
- Reports: the 60 files named by `ledger.entries[].reports` (w1/w2/w3). Parsed the
  last fenced `json` block of each (61 blocks; `RX1.md` carries two, the second is
  the authoritative correction). All 60 parsed, 0 errors.
- Section match: recomputed the sectionizer on `SKILL.md` blobs at each report's
  `skill_sha256`, mapped each report section to its ledger entry by section
  sha256. All 75 entries assigned; the union of per-seat `commands_executed`
  equals `commands_executed_count` for **all 75 entries** (0 mismatches). This is
  the extraction's integrity check.
- Read revs (O):
  - wave 1 `CR*`: `28aeef498cc070c3183271b709bc79d344ff547a` — CR01 records
    "lane HEAD 28aeef4"; CR16 records `rev-parse HEAD -> 28aeef49`; page sha
    `97cf436b…`. `git diff 9f2c86f 28aeef4 -- tools .ufo/evidence` is empty, so
    using 9f2c86f (the commit that first carries the 97cf page) would not change
    any drift result.
  - wave 2 `RR*`: `c699c8c36d6e4eca4b796b81a8247904aa145ec8` (`3d8a1edb…`;
    RR01/RR14 state the pinned commit and hash `git show c699c8c:SKILL.md`).
  - wave 3 `RX1–RX8`: `05a224754db3c6fce18f5ec1816a6873bffe3d0e`
    (`e289acec…`; RX1 executes `rev-parse --verify 05a2247…`).
  - `RX9`: `34907080f6adda2b18ea13eff23822671cc6930e` (`906fb649…`).
- Lane files: inferred from `commands_executed` plus the report's `opened` list,
  both O. `[I]` marks the inference. Reads of a pinned object
  (`git show REV:path`, `git cat-file`) are recorded as `PATH@rev` and are **not**
  treated as live worktree opens; `/tmp` copies and sibling-repo paths are
  excluded (some report `opened` lines are absolute and were normalized to the
  lane root).
- Drift: `git -C <lane> diff --stat <entry read rev> 98bea7d -- <path>` for every
  inferred `tools/` or `.ufo/evidence/` input. `A` = added since the read rev,
  `M` = modified, `=` = byte-identical (empty diff). All exits 0; `A`/`M` facts
  are from `--name-status`.

Legend for the input column (all `[I]`):

`SNAP` = `.ufo/evidence/round-16/coldread/SKILL.snapshot.md`;
`RUN` = `tools/mutate-and-run.sh`; `BW` = `.ufo/evidence/round-12/BashWitness/pristine.sh`;
`RC` = `tools/repeat-control.py`; `BWST` = `tools/bash-witness-study.py`;
`PD` = `tools/pin-disposition.py`; `WM` = `tools/witness-metadata.py`;
`CC` = `tools/context-capture.py`; `ED` = `tools/evidence-disposition.py`;
`ASM` = `.ufo/evidence/round-16/coldread/assemble.py`;
`MEAS` = `.ufo/evidence/round-16/measure.py`;
`REAT` = `.ufo/evidence/round-16/attribution/reattribute.py`;
`LEDGER` = `.ufo/evidence/round-16/coldread/ledger.json`;
`RREG` = `.ufo/evidence/round-16/round-gate/runner-regression.txt`;
`RG` = `.ufo/evidence/round-16/round-gate/{suite.txt,round-gate.defects.spec,predictions.json,sweep/*}`;
`R12`/`R13`/`R14`/`R15` = the corresponding `.ufo/evidence/round-NN/` files named
by the commands. Corpus/`plans/` reads are not listed per row (not the asked
scope); they are counted in §Findings F5.

## Credit baseline

Using the v1 `entry_credit_reason` rule verbatim: **64/75 entries credit**.
The 11 non-crediting entries are `4, 7, 8, 12, 22, 23, 50, 59, 62, 64, 71`
(wrong-expectation or gap-blocking). Every non-crediting entry is outvoted at its
section sha by a crediting sibling, so the v1 count still yields
`coldread.sections_covered = 54/54`, `box3_full_page = true`,
`calibration_restraint_score = 8`, `depth_score = 7` at `98bea7d` (O:
`.ufo/evidence/round-16/measure.py --rev 98bea7d`, exit 0). Drift, not the v1
credit rule, is what the row-level map below exposes.

## Map — all 75 entries

`cmds` = `commands_executed_count`; the command column abbreviates the
tools/evidence-relevant commands verbatim from the JSON block (full lists stay in
the reports). `credit` is the v1 per-entry verdict, independent of drift.

| # | lines | heading (trimmed) | class/verdict | credit | cmds | commands touching tools/ or evidence (JSON) | inputs `[I]` | drift at 98bea |
|---|---|---|---|---|---|---|---|---|
| 0 | 1–5 | (preamble) | record/gap-minor | yes | 13 | sha256sum SNAP | SNAP | — |
| 1 | 6–16 | # tameshi-shokunin | record/gap-minor | yes | 6 | sha256sum SNAP; heading dump | SNAP | — |
| 2 | 17–29 | ## Standing rules | instruction/gap-minor | yes | 10 | read PROVINCE.md; grep mutation notes | — | — |
| 3 | 30–57 | ## Source notes | record/gap-minor | yes | 13 | git log per note; grep surveys | — | — |
| 4 | 58–93 | ## Gate-shape decision table | instruction/wrong-expectation | no | 16 | sha256sum SNAP; sibling gates | — | — (NC) |
| 5 | 94–130 | ## The mutation bar | instruction/gap-minor | yes | 14 | sha256sum SNAP | SNAP | — |
| 6 | 131–245 | ## Mutation-sweep recipe | instruction/gap-minor | yes | 18 | cp/sha256 SNAP; sibling gates | SNAP | — |
| 7 | 246–313 | ## Defect-taxonomy templates | instruction/wrong-expectation | no | 13 | sha256sum SNAP; mutation notes | — | — |
| 8 | 314–374 | ## Kill-rate bands | instruction/wrong-expectation | no | 18 | sha256sum SNAP; census replay | BW | — (NC) |
| 9 | 375–404 | ## Restore discipline | instruction/gap-minor | yes | 14 | sha256sum SNAP | BW, SNAP | — |
| 10 | 405–465 | ## Cross-language divergence | record/gap-minor | yes | 12 | sha256sum SNAP | SNAP | — |
| 11 | 466–496 | ## No-permissiveness audit recipe | instruction/gap-minor | yes | 14 | sha256sum SNAP; kagi gate | SNAP | — |
| 12 | 497–526 | ## Fail-closed arm taxonomy | instruction/wrong-expectation | no | 16 | sha256sum SNAP; sibling gates | — | — |
| 13 | 527–593 | ## Appendix A (JS case) | instruction/gap-minor | yes | 20 | cp/sha256 SNAP; kumitate blob | SNAP | — |
| 14 | 594–667 | ## Appendix B (bash case) | instruction/gap-minor | yes | 23 | cp/sha256 SNAP; kagi blob | SNAP | — |
| 15 | 668–793 | ## Third case (round 5) | record/gap-minor | yes | 10 | git show sibling tsukuroi census; corpus | — | — (corpus live) |
| 16 | 794–805 | ## The mutation service | record/verified-record | yes | 7 | sha256sum SNAP | SNAP | — |
| 17 | 806–826 | ### The opt-in contract | instruction/gap-minor | yes | 12 | git show RUN@b58b26fb; git show mado@eead56b | SNAP; RUN@b58b26fb | — |
| 18 | 827–857 | ### The protocol | instruction/gap-minor | yes | 17 | bash mado pinned --selftest; grep pinned gate | SNAP; RUN@b58b26fb | — |
| 19 | 858–882 | ### The boundaries | record/gap-minor | yes | 9 | git show RUN@rev across history; sha256 | SNAP; RUN@b58b26fb | — |
| 20 | 883–898 | ### The report shape | instruction/gap-minor | yes | 6 | sed/grep RUN (60-90, 425-505) | RUN | **DRIFT** |
| 21 | 899–920 | ### The mado run | record/gap-minor | yes | 9 | grep RUN (leg row); git show mado@eead56b | RUN | **DRIFT** |
| 22 | 921–932 | ## The leg ledger | record/wrong-expectation | no | 4 | sha256sum RUN; rev-parse HEAD | RUN | drift (NC) |
| 23 | 933–964 | ### Using the ledger | instruction/gap-minor | no | 3 | bash RUN --regression | RUN | drift (NC) |
| 24 | 965–1009 | ### Reading a receipt | instruction/gap-minor | yes | 12 | hash all RUN blobs; bash RUN --selftest/--regression (HEAD) | RUN, SNAP | **DRIFT** |
| 25 | 1010–1020 | ## The re-sweep cadence | instruction/gap-minor | yes | 7 | sibling HEAD hashes; RUN in opened | RUN, SNAP | **DRIFT** |
| 26 | 1021–1068 | ### The tick and the pin read | instruction/gap-minor | yes | 12 | sha256sum RUN; bash RUN --selftest | RUN | **DRIFT** |
| 27 | 1069–1091 | ### Triggers T1–T3 | instruction/gap-minor | yes | 6 | bash RUN --regression; git log RUN | RUN | **DRIFT** |
| 28 | 1092–1154 | ### Six-case confidence statement | record/gap-minor | yes | 18 | sha256sum RUN; blob search RUN | RUN, SNAP | **DRIFT** |
| 29 | 1155–1163 | ## The cadence's first tick | record/gap-minor | yes | 7 | git log/show RUN; sha256 SNAP | RUN, SNAP | **DRIFT** |
| 30 | 1164–1211 | ### The tick, executed | record/gap-minor | yes | 4 | sha256sum/line count RUN | RUN, SNAP | **DRIFT** |
| 31 | 1212–1229 | ### The receipt at this boundary | record/gap-minor | yes | 3 | bash /tmp RUN --selftest | SNAP | — |
| 32 | 1230–1245 | ### The re-pin semantics | record/verified-record | yes | 4 | git show pinned objects | SNAP | — |
| 33 | 1246–1271 | ### The service's limits | record/gap-minor | yes | 11 | cp/sha256 SNAP | SNAP | — |
| 34 | 1272–1280 | ## The operator's runbook | record/verified-record | yes | 2 | grep/sed RUN | RUN, SNAP | **DRIFT** |
| 35 | 1281–1301 | ### The operator's runbook body | record/gap-minor | yes | 2 | grep runbook | — | — |
| 36 | 1302–1364 | ### The six-leg regression | instruction/executed-ok | yes | 5 | bash RUN --selftest/--regression | RUN | **DRIFT** |
| 37 | 1365–1379 | ## Final pointers | record/gap-minor | yes | 15 | sha256sum SNAP; corpus/plans greps | SNAP | — |
| 38 | 1380–1395 | ### The map | record/gap-minor | yes | 7 | grep RUN (selftest/regression legs) | RUN | **DRIFT** |
| 39 | 1396–1435 | ### Boundary readings | record/gap-minor | yes | 5 | bash RUN --selftest/--regression | RUN | **DRIFT** |
| 40 | 1436–1448 | ### Where to enter | instruction/executed-ok | yes | 4 | operator run of RUN | — | — |
| 41 | 1449–1463 | ### What stays open | record/verified-record | yes | 6 | grep ledger | — | — |
| 42 | 1464–1478 | ## Promotion-evidence calibration | record/gap-minor | yes | 2 | read PROTOCOL | SNAP | — |
| 43 | 1479–1498 | ## Repeated controls and gate registry — round 12 | instruction/gap-minor | yes | 5 | sha256sum RUN,RC; repeat-control snapshots | RUN, RC | **DRIFT** |
| 44 | 1499–1516 | ### Gate/probe registry | record/gap-minor | yes | 15 | repeat-control selftest; bash-witness; find R12 | RC, BWST, R12 | — |
| 45 | 1517–1547 | ## Pin disposition — round 13 | instruction/gap-minor | yes | 3 | pin-disposition; witness-metadata | PD, WM, R13 | — |
| 46 | 1548–1562 | ### Round-13 gate/probe registry | instruction/gap-minor | yes | 10 | pin-disposition; witness-metadata; git-show exports | PD, WM, R12/R13 | — |
| 47 | 1563–1596 | ## Effective expectation reconciliation — round 14 | instruction/gap-minor | yes | 4 | evidence-disposition before (exit 1) and after (exit 0) | ED, R14, R13 | **DRIFT (round-14 bucket)** |
| 48 | 1597–1608 | ### Round-14 historical registry | record/verified-record | yes | 5 | evidence-disposition clean/selftest/exit2/usage | ED, R14, R13 | **DRIFT (round-14 family)** |
| 49 | 1609–1675 | ## Context gate classification — round 15 | record/gap-minor | yes | 15 | context-capture variants; evidence-disposition help | CC, ED, R14/R15 | — |
| 50 | 1676–1705 | ### Round-15 gate/probe registry | instruction/gap-blocking | no | 14 | context-capture; evidence-disposition (observed exit 2) | CC, ED, R14/R15 | drift observed (NC) |
| 51 | 6–16 | # tameshi-shokunin (RR01) | record/gap-minor | yes | 8 | git show SKILL; PyYAML | — | — (object-only) |
| 52 | 58–93 | ## Gate-shape decision table (RR02) | record/gap-minor | yes | 11 | git show SKILL; commit metadata | — | — |
| 53 | 131–245 | ## Mutation-sweep recipe (RR03) | instruction/gap-minor | yes | 7 | git show SKILL; pinned sibling gates | — | — |
| 54 | 246–313 | ## Defect-taxonomy templates (RR04) | instruction/gap-minor | yes | 7 | git show SKILL; sibling census replay | — | — |
| 55 | 314–374 | ## Kill-rate bands (RR05) | record/gap-minor | yes | 8 | SKILL range; git show sibling gates | — | — |
| 56 | 497–526 | ## Fail-closed arm taxonomy (RR06) | record/gap-minor | yes | 7 | SKILL range; sibling live gates | — | — |
| 57 | 921–932 | ## The leg ledger (RR07) | record/gap-minor | yes | 4 | git show mado@eead56b | RUN@c699c8c | — |
| 58 | 933–964 | ### Using the ledger (RR07) | instruction/gap-minor | yes | 1 | bash /tmp fleet RUN --regression | /tmp clone only | — (empty-input) |
| 59 | 1380–1395 | ### The map (RR08) | record/gap-minor | no | 9 | git cat-file RUN@c699c8c; grep | RUN@c699c8c | — (NC) |
| 60 | 1464–1478 | ## Promotion-evidence calibration (RR09/RR15) | record/gap-minor | yes | 29 | assemble selftest/run; git show anchors | ASM, MEAS | **DRIFT** |
| 61 | 1609–1675 | ## Context gate classification (RR10) | record/verified-record | yes | 2 | sha256sum CC,ED; git diff RUN | CC, ED, R13/R14/R15 | — |
| 62 | 1707–1739 | ## Errata (RR11) | record/gap-minor | no | 15 | git cat-file ledger absent; grep ASM | ASM (live), SNAP | drift (NC) |
| 63 | 1740–1788 | ## Seventh recorded case (RR12/RR12b) | instruction/executed-ok | yes | 21 | bash RUN --target; measure.py --rev | RUN, MEAS, RREG, RG | **DRIFT** |
| 64 | 1789–1796 | ### Round-16 gate/probe registry (RR13) | record/wrong-expectation | no | 9 | RUN selftest/regression; measure/assemble/reattribute selftests | RUN, MEAS, ASM, REAT | drift (NC) |
| 65 | 1–5 | (preamble) (RX1) | record/verified-record | yes | 5 | git show SKILL; PyYAML/Psych | — | — (object-only) |
| 66 | 6–16 | # tameshi-shokunin (RX1) | record/gap-minor | yes | 4 | git show SKILL; metadata | — | — (object-only) |
| 67 | 246–313 | ## Defect-taxonomy templates (RX2) | instruction/gap-minor | yes | 13 | SKILL range; sibling gates; corpus | — | — (corpus live) |
| 68 | 1302–1364 | ### The six-leg regression (RX3) | record/gap-minor | yes | 13 | git cat-file RUN@606716f/@9f1d3c3; staged copy | RUN@05a2247 | — |
| 69 | 1380–1395 | ### The map (RX4) | record/gap-minor | yes | 14 | git ls-tree; git show RUN@284ab0f/@05a2247 | RUN@05a2247 | — |
| 70 | 1676–1706 | ### Round-15 gate/probe registry (RX5) | instruction/executed-ok | yes | 19 | context-capture; evidence-disposition all modes | CC, ED, R14/R15 | — |
| 71 | 1707–1748 | ## Errata (RX6) | record/gap-blocking | no | 22 | evidence-disposition (exit 2); git archive 28aeef4 | ASM, ED, R14 | drift (NC) |
| 72 | 1749–1800 | ## Seventh recorded case (RX7) | instruction/gap-minor | yes | 22 | bash RUN --target; probes; measure.py; repeat-control | RUN@05a2247, MEAS, RG | — |
| 73 | 1801–1808 | ### Round-16 gate/probe registry (RX8) | instruction/gap-minor | yes | 20 | RUN selftest/regression; measure/assemble/reattribute | ASM, MEAS, REAT | **DRIFT** |
| 74 | 1707–1753 | ## Errata (RX9) | record/gap-minor | yes | 27 | git show SKILL; assemble; evidence-disposition lane+archive | LEDGER, ASM, RUN, ED | **DRIFT** |

Note on `SNAP`: every wave-1 entry that names it shows status `A` (the file did
not exist at the read rev) but its bytes at `98bea7d` equal the measured page
sha, so it is not content drift; the read-rev provenance problem is F4. All
`DRIFT` marks are `M` (modified) paths whose read-rev bytes no longer match the
tip.

## Entries already drifted at `98bea7d`, besides the round-14 bucket (47)

All diffstat facts below are O (`git diff --stat <rev> 98bea7d -- <path>`); the
attribution of a path to an entry is `[I]` from the report's commands/`opened`.

### A. Round-14 family

| entry | heading | read rev | drifted input | diffstat |
|---|---|---|---|---|
| 47 | ## Effective expectation reconciliation — round 14 (the bucket named in the spot-check) | 28aeef4 | `tools/mutate-and-run.sh` (read transitively by `evidence-disposition.py`; pinned 75ed934d in `.ufo/evidence/round-13/expected.json`) | +121/−24 |
| 48 | ### Round-14 historical registry — superseded by round 15 | 28aeef4 | same gate, same transitive RUN | +121/−24 |

Entry 48 is a **second round-14-family bucket** with the same failing command.
The spot-check named only the §Effective-expectation-reconciliation bucket; this
one credits (record/verified-record) and would also lose input-keying. Its own
commands are `--root . --dispositions .ufo/evidence/round-14/dispositions.json`
(exit 0 at read rev) plus the selftest/exit-2/usage arms.

### B. Other crediting entries already drifted (18)

Runner readers at wave 1 (`28aeef4`; runner was `75ed934d…`, tip `0673d2e5…`):

| entry | heading (short) | class/verdict | drifted input | diffstat |
|---|---|---|---|---|
| 20 | ### The report shape | instruction/gap-minor | RUN | +121/−24 |
| 21 | ### The mado run | record/gap-minor | RUN | +121/−24 |
| 24 | ### Reading a receipt | instruction/gap-minor | RUN (HEAD run + full-blob hash) | +121/−24 |
| 25 | ## The re-sweep cadence | instruction/gap-minor | RUN (`opened` live) | +121/−24 |
| 26 | ### The tick and the pin read | instruction/gap-minor | RUN | +121/−24 |
| 27 | ### Triggers T1–T3 | instruction/gap-minor | RUN | +121/−24 |
| 28 | ### Six-case confidence statement | record/gap-minor | RUN (sha256 only) | +121/−24 |
| 29 | ## The cadence's first tick | record/gap-minor | RUN (live HEAD) | +121/−24 |
| 30 | ### The tick, executed | record/gap-minor | RUN (sha256 + line count) | +121/−24 |
| 34 | ## The operator's runbook | record/verified-record | RUN | +121/−24 |
| 36 | ### The six-leg regression | instruction/executed-ok | RUN | +121/−24 |
| 38 | ### The map | record/gap-minor | RUN | +121/−24 |
| 39 | ### Boundary readings | record/gap-minor | RUN | +121/−24 |
| 43 | ## Repeated controls — round 12 | instruction/gap-minor | RUN (`sha256sum`) | +121/−24 |

Wave 2 (`c699c8c`; runner was `89722ddb…`):

| entry | heading (short) | class/verdict | drifted input | diffstat |
|---|---|---|---|---|
| 60 | ## Promotion-evidence calibration (RR09/RR15) | record/gap-minor | `assemble.py`, `measure.py` | ASM +25/−2; MEAS +71/−2 |
| 63 | ## Seventh recorded case (RR12) | instruction/executed-ok | RUN; `measure.py`; `runner-regression.txt` | RUN +19/−6; MEAS +71/−2; RREG +11/−10 |

Wave 3:

| entry | heading (short) | class/verdict | drifted input | diffstat |
|---|---|---|---|---|
| 73 | ### Round-16 gate/probe registry (RX8) | instruction/gap-minor | `assemble.py` (05a2247) | +4/−2 |
| 74 | ## Errata (RX9) | record/gap-minor | `ledger.json` (34907080) | +29/−20 |

### C. Non-crediting entries that also drift (reported, not coverage-relevant)

`22`, `23` (RUN, wrong-expectation); `50` (gate observed exit 2 at c699c8c);
`62` (`assemble.py` live), `64` (RUN/MEAS/ASM/REAT), `71` (`assemble.py` at
05a2247). They already fail v1 credit, so the repair need not rescue them, but
their commands corroborate the same drift.

## Findings

**F1 — the drifted set is much larger than one bucket.** Besides entry 47 (the
named bucket), 19 crediting entries lose an input under R16-C2b: the 18
runner/evidence readers in §B plus entry 48 in §A (the second round-14-family
bucket). The 14 crediting wave-1 runner readers (plus non-crediting 22/23)
account for most of it. If the L1 backfills `inputs` honestly at each entry's read
rev, `measure.py --rev 98bea7d` would report `input-drift:tools/mutate-and-run.sh`
for all of them; they must be re-read at the measured rev (the declared full-page
wave-2 re-read covers this) or the overlay must leave them uncovered.

**F2 — the round-14 family has two buckets, not one.** The spot-check named only
`## Effective expectation reconciliation — round 14` (entry 47). Entry 48
(`### Round-14 historical registry — superseded by round 15`) embeds the same
`--root . --dispositions .ufo/evidence/round-14/dispositions.json` command and
credits as `verified-record`; at tip it returns 2 `expected_input_digest_mismatch`
for the same reason (runner moved from `75ed934d` to `0673d2e5`, while
`.ufo/evidence/round-13/expected.json` still pins `75ed934d`). The round-15 row
(entry 70) already documents the moved runner and predicts exit 2, so it is
consistent; entry 48 does not. [I] for entry 48's exit-2 at tip is inferred from
the same code path the spot-check exercised; I did not execute the gate.

**F3 — historical-pin reads cannot be expressed by the v2 `inputs` map.**
Entries 17, 18, 19, 24, 27, 29, 30, 39, 57, 58, 59, 62, 68, 69, 71, 72 read
`tools/…` through `git show REV:path` / `git cat-file` (or a `/tmp` copy of a
pinned blob). Under the stated schema, `inputs` is lane-relative worktree paths
whose blob at the measured rev must carry the recorded sha. A pinned object read
is not a worktree open; if recorded as `tools/mutate-and-run.sh` with the pinned
sha (e.g. `89722ddb` at c699c8c), it fails `input-drift` because the tip blob is
`0673d2e5`. If omitted, an entry whose commands are object/sibling-only has an
empty `inputs` map and fails `inputs-unrecorded`. The L1 needs an explicit ruling
for this class (e.g. object reads go to `external_inputs`, or an
`inputs`-key syntax `path@rev` is admitted); otherwise entries 51, 57, 58, 59,
65, 66, 68, 69 cannot be honestly credited.

**F4 — the page snapshot did not exist at the wave-1 read rev.** 49 entries name
`.ufo/evidence/round-16/coldread/SKILL.snapshot.md` in commands/`opened`. O:
`git diff --name-status 28aeef4 98bea7d -- …/SKILL.snapshot.md` → `A`; the file
first lands at `e69b488` ("pre-register … retain wave-1 seat reports"), after the
wave-1 seats read at `28aeef4`. At the measured rev its sha is
`97cf436b…3580` (the assigned page), so the v2 input check at REV would pass, but
`read_rev` provenance is inconsistent (a seat cannot have opened a path that did
not exist at its read rev). The assembler should either record this as an
external input, or flag it; recording it silently as a clean lane input at the
read rev overstates provenance. [I] on how the seats obtained it (the lane was
being written during the wave; the /tmp copies carry the same sha).

**F5 — corpus drift is outside the asked tool/evidence scope but will bite the
same rule.** [I] from `git diff --name-status <rev> 98bea7d -- corpus plans`:
`corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/arm-class-matrix.md`,
`corpus/QUALITY.md` changed since every read rev; `corpus/README.md` and
`corpus/SOURCES.md` changed since 28aeef4. 20 entries read
`fleet-kill-rate-ledger.md` — 22, 24, 25, 27–34, 36, 37, 38, 40, 41, 57, 59,
68, 69 — of which 18 credit (all but 22 and 59); entries 15 and 19 read
`arm-class-matrix.md`. If those reads are recorded in
`inputs` (the schema says every lane-tracked file opened), they drift too. This
is not a defect in the asked map; it is a scoping decision the L1 must make
before claiming full-page input-keyed credit.

**F6 — empty-input entries.** Commands/`opened` for 51, 57, 58, 65, 66 contain no
lane worktree file (SKILL read through `git show`, sibling repo, or `/tmp`
clone). Under a strict "inputs non-empty" clause they would fail
`inputs-unrecorded` even with zero drift. 15 and 67 do read corpus files live, so
they are not empty (but see F5).

**F7 — read-rev choice does not affect drift.** CR01/CR16 fix the wave-1 read rev
at `28aeef4`; using `9f2c86f` (first commit with the 97cf page) gives identical
`tools/`+`.ufo/evidence/` diffs. The v2 `read_rev` should still be `28aeef4`
(that is the lane HEAD the seats observed), not the page-creation commit.

## Concurrent lane-state observation (not caused by this seat)

At 12:32:47 the live lane worktree was on a **detached HEAD `e16adb7`**, with
three commits created at 12:29:33 on top of the measured tip:
`f8832ef selftest-fixture`, `0559c60 selftest-fixture-exec`,
`e16adb7 selftest-fixture-noexec`; `98bea7d` remains their parent. `git status`
showed 18 entries (`D exec.sh`, `D noexec.sh`, `D target.sh`, plus untracked
lane files) — i.e. another wave-1 session committed a selftest fixture in the
lane root while this seat was analysing. This seat made no git write. All
evidence above is rev-pinned (`git show 98bea7d:…`, `git diff <rev> 98bea7d`), so
it still reproduces; `git cat-file -t 98bea7d` → `commit`. The L1 should restore
the branch before landing anything, and this report is currently untracked.

## Commands run (all exits 0 unless noted)

- `python3 <scratch>/parse.py`, `map.py`, `infer.py`, `final2.py` — parsed 60
  reports/61 JSON blocks, assigned 75/75 entries, commands-union mismatch count 0.
- `python3 .ufo/evidence/round-16/measure.py --rev 98bea7d…` — exit 0;
  `sections 54/54 box3 True restraint 8 depth 7`.
- `git diff --stat 28aeef4 98bea7d -- tools/mutate-and-run.sh` → 121+/24−.
- `git diff --stat c699c8c 98bea7d -- tools/mutate-and-run.sh` → 19+/6−.
- `git diff --stat 05a2247 98bea7d -- tools/mutate-and-run.sh` → empty.
- `git diff --stat c699c8c 98bea7d -- .ufo/evidence/round-16/measure.py` → 71+/2−.
- `git diff --stat c699c8c 98bea7d -- …/coldread/assemble.py` → 25+/2−;
  `05a2247` → 4+/2−; `34907080` → empty.
- `git diff --stat c699c8c 98bea7d -- …/attribution/reattribute.py` → 70+/31−.
- `git diff --stat c699c8c 98bea7d -- …/round-gate/runner-regression.txt` → 11+/10−.
- `git diff --stat 34907080 98bea7d -- …/coldread/ledger.json` → 29+/20−.
- `git show 98bea7d:…/SKILL.snapshot.md | sha256sum` → `97cf436b…3580`.
- Runner shas: `28aeef4` `75ed934d…`, `c699c8c` `89722ddb…`, tip `0673d2e5…`.

No tool was installed or upgraded. No lane file other than this report was
written; no git/jj write was performed.

**Verdict: built** — per-entry map (75 entries, 64 crediting). Drifted at
`98bea7d`: the named round-14 bucket (47), a second round-14-family bucket (48),
and 18 other crediting runner/evidence readers; plus the historical-pin and
empty-input classes the v2 rule must adjudicate before backfilling any entry.
