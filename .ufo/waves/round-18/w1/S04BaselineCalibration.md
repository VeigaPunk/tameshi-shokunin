# S04 — round-17 baseline census and predicted wave-2 invalidation set

Seat: S04BaselineCalibration (leaf, no delegation). Base rev: `183f87b899e6cae46be98d251cbc87fb5118f6ca`.
Scratch: `/tmp/tameshi-r18w1-S04BaselineCalibration-JIiU5D` (fleet-mirror clone, all GIT_* scrubbed).
No tools installed or upgraded.

## 1. Baseline measurement (run, not read)

```
W=/tmp/tameshi-r18w1-S04BaselineCalibration-JIiU5D
mkdir $W/fleet; ln -s siblings; git clone -q <lane> $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q 183f87b899e6cae46be98d251cbc87fb5118f6ca   # exit 0, HEAD = 183f87b…
cd $W/fleet/tameshi-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  python3 .ufo/evidence/round-17/measure.py --rev 183f87b899e6cae46be98d251cbc87fb5118f6ca   # exit 0
python3 .ufo/evidence/round-17/measure.py --selftest
  -> MEASURE_SELFTEST: 94/94 pass (scratch /tmp/tameshi-r17-MeasureV2-ylx9n70s)   # exit 0
```

Measured at the base rev (JSON saved at `$W/measure.json`):

| field | value |
|---|---|
| `coldread.sections_covered` / `sections_total` | **58 / 58** (`reasons: {"credited": 58}`, `missing: []`) |
| `coldread.box3_full_page` | **true** (defined as covered == total, `measure.py:643`) |
| `calibration_restraint_score` | **8** (marks 1,2,4 `~`; box3 `~` + link + full page, `measure.py:661-668`) |
| `recorded_cases` / `depth_score` | **7 / 7**; legs `js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check, js-round-gate` |
| `ledger_guardrail` | header_legs 7, regression_calls 7, selftest_tuples 7, unique_recorded_gates 7, `lists_agree: true` |
| `sources` | rows **62**, malformed **0**, tiers `{A:54, B:6, C:2}`, status `{mined:35, queued:24, rejected:3}` |
| `shonen` | 4 boxes, marks `[~,~,~,~]`, asserted 4, checked 0, box3_marked/link/points true |
| `overrides_used` / `trace_gate` / `ledger_source` / `ledger_committed` | false / strict / rev / true |

Ledger facts (`.ufo/evidence/round-17/coldread/ledger.json`, 68 entries): 61 entries match a current
SKILL.md section sha; 3 sections carry two matching entries (`1155`, `1246`, `1517`, skill
`b1bd20ae…` and `de6c2b08…`, same section sha); 7 entries are older-skill versions whose sha no
longer matches any section (starts 497, 1021, 1069, 1676, 1806, 1855, 1897).
Three matched entries are **already stale at base**: `1155` (drift: `LOG.md`, `SCORECARD.md`,
`corpus/QUALITY.md`, `corpus/lessons/round-17.md`), `1246` (drift: `.ufo/evidence/round-17/measure.py`),
`1517` (drift: round-17 `assemble.py` + `measure.py`). Each is the `b1bd20ae…` entry; its twin
`de6c2b08…` entry credits, so coverage stays 58/58. The measured baseline is unchanged; the
ledger already carries stale entries that never credit.

## 2. Method of the edit simulation

Two independent passes, both against the clone only (lane repo untouched; no GIT_* pointed at the lane):

1. **Mechanical (input-keyed):** for every ledger entry whose `sha256` equals a current SKILL.md
   section sha, record the section `(start, heading)` when the planned-edited path is a key of
   `entry.inputs`. Strict rule: `inputs` must be non-empty and every recorded sha must still match
   (`measure.py:325-345`); the ledger and `SKILL.md` are the only ignored keys (`measure.py:129-132`).
2. **Empirical:** per file, `git reset --hard -q <base>`, append a marker, commit, then
   `measure.py --rev <newcommit>` (exit 0 every run). A drifted entry fails with
   `input-drift:<path>`; a section stays credited only if a second matching entry still verifies.
   Combined run: all 15 files edited in one commit. `SHONEN.md` was also tested in its planned
   shape (append the round-18 ledger link under box 3, `measure.py:129` link semantics).

The five ER-jj files are the knowledge notes carrying the ER-jj/ER-R3 text at the base rev:
`verification-patterns-fleet.md:309`, `fleet-kill-rate-ledger.md:420`, `service-limits.md:279`,
`operator-runbook.md:514`, `incremental-pin-disposition.md:386` (verified with `git grep` at REV).

## 3. Predicted invalidation set — 48 SKILL.md buckets (wave-2 re-read list)

Codes: M=`tools/mutate-and-run.sh`, RC=`tools/registry-check.py`, ED=`tools/evidence-disposition.py`,
BW=`tools/bash-witness-study.py`, IK=`corpus/knowledge/input-keyed-coldread-credit.md`,
VP/FK/SL/OR/IP = the five ER-jj files in the order named in §2, SH=`SHONEN.md`,
SO=`corpus/SOURCES.md`, PR=`PROVINCE.md`, RD=`corpus/README.md`, QL=`corpus/QUALITY.md`.
Every listed code records that bucket as an input in the ledger (mechanical union; identical if the
7 non-matching entries are included — they add no bucket).

| start | heading | files |
|---:|---|---|
| 1 | `` (preamble) | PR |
| 6 | `# tameshi-shokunin` | RD |
| 17 | `## Standing rules` | PR |
| 30 | `## Source notes` | VP |
| 58 | `## Gate-shape decision table — hermetic vs live vs audit-lane` | VP |
| 131 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | RD |
| 314 | `## Kill-rate bands — admission readings (rounds 2–3, measured)` | PR |
| 375 | `## Restore discipline — proof the substrate never moved` | RD |
| 405 | `## Cross-language divergence — bash vs JS (round 3, measured)` | PR |
| 466 | `## No-permissiveness audit recipe` | VP |
| 668 | `## Third case — cross-author confirmation (round 5, measured)` | PR |
| 794 | `## The mutation service — running a sweep for an opting-in lane (round 6, measured)` | PR |
| 827 | `### The protocol — ordered, fail-closed` | M |
| 858 | `### The boundaries — what a service run is not` | FK |
| 883 | `### The report shape — what the opting-in lane receives` | M |
| 921 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | M, FK |
| 933 | `### Using the ledger` | M |
| 965 | `### Reading a receipt — the discipline` | M, FK |
| 1010 | `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` | FK |
| 1021 | `### The tick and the pin read` | M, FK, OR |
| 1069 | `### Triggers T1–T3 and the re-pin rule` | M, FK, OR |
| 1092 | `### Six-case confidence statement (round 8, measured)` | M, IK, VP, FK, SL, OR, IP |
| 1155 | `## The cadence's first scheduled tick, and the service's limits (round 9, measured)` | M, RC, ED, BW, IK, VP, FK, SL, OR, IP, SH, SO, PR, RD, QL |
| 1164 | `### The tick, executed` | M, FK |
| 1212 | `### The receipt at this boundary` | M, FK |
| 1230 | `### The re-pin semantics, as executed` | FK |
| 1246 | `### The service's limits — what tameshi refuses to mutation-test` | FK, SL, OR, PR |
| 1272 | `## The operator's runbook and the six-leg regression (round 10, measured)` | M, FK, OR |
| 1281 | ``### The operator's runbook — `corpus/knowledge/operator-runbook.md` `` | OR |
| 1302 | `### The six-leg regression — usage and this round's receipt` | M, FK |
| 1380 | `### The map — where a reader enters, artifact by artifact` | M, FK, SL, OR, RD |
| 1396 | `### Boundary readings, executed by this lane` | M |
| 1436 | `### Where to enter — four readers` | M, FK, OR |
| 1449 | `### What stays open — named, never closed by prose` | FK, SL, OR |
| 1479 | `## Repeated controls and gate registry — round 12` | M |
| 1499 | `### Gate/probe registry` | M, BW |
| 1517 | `## Pin disposition and provenance correction — round 13` | M, BW, IP, SO |
| 1548 | `### Round-13 gate/probe registry` | M, BW, SO |
| 1563 | `## Effective expectation reconciliation — round 14` | M, ED, BW, IP, SO |
| 1597 | `### Round-14 historical registry — superseded by round 15` | M, ED, BW |
| 1609 | `## Context gate classification and explicit exit classes — round 15` | ED, SO |
| 1676 | `### Round-15 gate/probe registry` | M, ED, BW |
| 1707 | `## Errata — round 16 full-page cold-read` | M, ED, BW |
| 1754 | `## Seventh recorded case and full-page cold-read — round 16` | M |
| 1806 | `### Round-16 gate/probe registry` | M |
| 1814 | `## Live-tree re-pin and entry-command monitor — round 17` | M, RC, ED, BW |
| 1846 | `### Round-17 gate/probe registry — re-pin and monitor` | M, RC, ED, BW, SO |
| 1855 | `## Input-keyed cold-read credit — round 17` | IK, SO |

Per-file bucket counts (mechanical): M 28, RC 3, ED 8, BW 10, IK 3, VP 5, FK 17, SL 5, OR 10,
IP 4, SH 1, SO 7, PR 8, RD 5, QL 1. Union **48**; complement **10** (carryable unchanged):
`94` mutation bar, `246` defect taxonomy, `497` fail-closed taxonomy, `527` Appendix A, `594`
Appendix B, `806` opt-in contract, `899` mado run, `1365` final pointers, `1464` promotion
calibration, `1897` round-17 input-keyed registry.

Note the asymmetry: a file may be listed only by the already-stale `b1bd20ae…` twin at `1155`,
`1246` or `1517`. It is still a recorded input (it is in the table above), but its drift alone no
longer removes measured credit there because the `de6c2b08…` twin verifies. `SHONEN.md` and
`corpus/QUALITY.md` exist only on that stale twin, so their edits cost no coverage.

## 4. Empirical credit loss per planned edit (one file per commit)

`measure.py --rev <commit>` exit 0 in all 15 runs; values are `sections_covered/58` and
`calibration_restraint_score`.

| edit | uncovered buckets | covered | calib |
|---|---:|---:|---:|
| `tools/mutate-and-run.sh` | 28 | 30/58 | 6 |
| `tools/registry-check.py` | 2 (`1814`, `1846`; `1155` survives on the twin) | 56/58 | 6 |
| `tools/evidence-disposition.py` | 7 (all but `1155` of its 8) | 51/58 | 6 |
| `tools/bash-witness-study.py` | 9 (all but `1155` of its 10) | 49/58 | 6 |
| `input-keyed-coldread-credit.md` | 2 (`1092`, `1855`) | 56/58 | 6 |
| `verification-patterns-fleet.md` | 4 (`30`, `58`, `466`, `1092`) | 54/58 | 6 |
| `fleet-kill-rate-ledger.md` | 16 (all but `1155` of its 17) | 42/58 | 6 |
| `service-limits.md` | 4 (`1092`, `1246`, `1380`, `1449`) | 54/58 | 6 |
| `operator-runbook.md` | 8 (all but `1155`, `1246` of its 10) | 50/58 | 6 |
| `incremental-pin-disposition.md` | 3 (`1092`, `1517`, `1563`) | 55/58 | 6 |
| `SHONEN.md` (marker) | 0 | 58/58 | 8 |
| `SHONEN.md` (planned round-18 link append) | 0 | 58/58 | 8 |
| `corpus/SOURCES.md` | 7 (`1517`, `1548`, `1563`, `1609`, **`1814`**, `1846`, `1855`) | 51/58 | 6 |
| `PROVINCE.md` | 7 (`1`, `17`, `314`, `405`, `668`, `794`, `1246`) | 51/58 | 6 |
| `corpus/README.md` | 4 (`6`, `131`, `375`, `1380`) | 54/58 | 6 |
| `corpus/QUALITY.md` | 0 | 58/58 | 8 |
| **all 15 together** | **48 = the §3 union exactly** (verified set equality) | **10/58** | **6** |

Why `calib` falls even when only one section is lost: `box3_full_page` is coverage == total
(`measure.py:643`), and `box3_points` requires it (`measure.py:667`); three `~` marks still give
`2*3 = 6`. `SHONEN.md`/`QUALITY.md` edits are the only singles that leave 8.

`corpus/SOURCES.md` has a second mechanism: bucket `1814` records it in `external_inputs` as a
live-lane read bound to the recorded digest; the edited live bytes yield
`live-lane-read:/home/…/corpus/SOURCES.md` (`measure.py:417-423`), independent of `inputs` drift.
The other 14 files are invalidated purely through `input-drift`.

`recorded_cases` stayed 7 in every marker run (markers are comments). The C1 leg-8 edit is the one
that must move `recorded_cases 7 -> 8`, `depth 7 -> 8`, and the guardrail 7/7/7 -> 8/8/8; all 28
`M` buckets in §3 are the depth-claim re-read set.

## 5. Consequences for the round's claims

- The `calibration 8` claim survives **only after** wave 2 re-reads the 48 buckets and records the
  new input digests in the round-18 ledger. Measured at the combined-edit rev with the round-17
  ledger, the state is 10/58, `box3_full_page=false`, calibration 6. The 10 complement buckets can
  be carried verbatim (`assemble.py --carry`), so 58/58 is reachable at 48 re-reads, not 58.
- The round-18 measure (contract F) is required for the 8: its box-3 link is the round-18 ledger
  path and its ignored inputs are SKILL.md plus both ledgers. The round-17 measure keeps reading 8
  for the planned SHONEN append only because the round-17 link remains in the box.
- `corpus/SOURCES.md` edits move the census itself (rows/tiers/status), not just the 7 input keys;
  the recorded census must be re-taken at the round-18 rev. Same for `SHONEN.md` marks, and for
  `tools/mutate-and-run.sh` leg/guardrail counts.
- Base stale entries (`1155`, `1246`, `1517` twin `b1bd20ae…`) are dead credit at base and should
  not be carried as if live; only the `de6c2b08…` twins currently credit those sections.

Verdict: **built** — baseline is 58/58 covered, box3 full page true, calibration 8, recorded_cases 7, sources 62 rows (0 malformed); the planned edits invalidate 48 of 58 SKILL.md buckets (union verified empirically: combined rev measures 10/58, calibration 6 until wave-2 re-reads land).
