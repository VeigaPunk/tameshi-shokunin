# CapabilityEvidence — tameshi round 12, wave w2

Seat: `CapabilityEvidence` (scribe, leaf, read-only). Advisory, lane-internal draft. Not independent non-author admission, promotion, or verification. No score is awarded by this seat; values below are measured or marked UNKNOWN.

Owned write: this file only. Nothing under `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, `corpus/`, `.ufo/evidence/` was modified. No builds, tests, or lints run. Read-only counting commands and receipt reads only. Tool installs: none.

Snapshot read at 2026-10-20T03:45Z. HEAD `18ad5d050ef4bcd830fe513825baed878f025024`. The worktree is dirty (round-12 in-flight, see §6).

## 1. Axes named

| Axis / row | Rubric as written | Source |
|---|---|---|
| depth | 1 point per recorded mutation case in the runner's ledger, cap 10 | `SCORECARD.md:66`; command D `:72-73` |
| calibration | 2 points per restrained, durable-linked `[~]` box, cap 8; 2 remaining need independent review | `SCORECARD.md:67`; command C `:74-75` |
| capability rows (not an axis) | a row enters only through a round that demonstrates the capability running | `SCORECARD.md:244` |

Claim filing: C1 is calibration per the wave context and `claims.json:6`; the round-2 plan files the same work as "capability (frontier F3)" at `SCORECARD.md:268-270`. ReportScribe flagged this as unresolved (`.ufo/waves/round-12/w1/ReportScribe.md:97`). This draft files C1 as a **capability row** and C2 as a **depth reanalysis**, as in `claims.json:6-7`. L1 must confirm the filing.

## 2. Scalars: depth and calibration

| Axis | Pinned before | Measured now (worktree, read-only) | Draft after | Status |
|---|---|---|---|---|
| depth | 6 | command D at HEAD `recorded_cases=6 depth_score=6`; worktree `recorded_cases=6`; `unique_recorded_gates=6` (`measure.py` output) | **6 → 6** | scalar6→6 held. C2 adds no ledger case (`tools/mutate-and-run.sh:84-89`; `claims.json:8`). Post-run value: UNKNOWN until C2 run lands. |
| calibration | 6 | command C at HEAD `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`; `measure.py` `calibration_restraint_score=6` (boxes 1,2,4; box 3 excluded) | **6 → 6** | scalar6→6 held. Command C gives 8 unadjusted; the pinned 6 is an adjudicated value (`SCORECARD.md:216-219`; ClaimSkeleton `.ufo/waves/round-12/w1/ClaimSkeleton.md:28`). C1 touches no SHONEN box, so it adds 0. |

Runner-side constant check (observed now): `git -C kagi-shokunin cat-file -t fecee8743e52eb8fb5fbb40782934cb619a1a96e` → `commit`; `git -C kagi-shokunin show fecee874…:corpus/surface-census.sh | sha256sum` → `275d8294…53009f` = `PIN_BASH` (`tools/mutate-and-run.sh:544-545`). Pin holds.

## 3. Draft capability row (C1)

Proposed for the `## Capabilities` table (`SCORECARD.md:238-244`). **Status: CONDITIONAL — not entered.** The row cannot be earned at read time; the demonstration below is incomplete.

Draft row text (the 0 → 1 move, valid only after the demonstration lands):

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| repeated pristine-control gate | runs one exact argv N ≥ 3 times, compares raw exit/stdout/stderr bytes, names the finding (`controls_match` / `controls_mismatch` / `baseline_nonzero` / `command_unavailable`) | `python3 tools/repeat-control.py --selftest` → exit 0 (**receipt absent**); `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` (**`expected.json` absent**) | fleet round 12 (**pending**) |

Capability count: **before 0 → draft after 1 (conditional)**. Measured now: **0 demonstrations complete of the 3 required** (selftest transcript, digest-pinned snapshot, tamper run). Requirement source: `.ufo/waves/round-12/w1/AdmissionBounds.md:52` and `.ufo/evidence/round-12/EvidenceScribe`-inventory C1-1 (`.ufo/waves/round-12/w1/EvidenceScribe.md:44`).

## 4. Per-claim measurement rows

| Claim | Axis / type | Metric | Before | Draft after | Measured now | Status | Command / receipt |
|---|---|---|---|---|---|---|---|
| C1 | calibration · capability acquisition | capability rows entered | 0 | 1 (conditional) | 0 entered; demo 0/3 | **pending demonstration** | `claims.json:6` |
| C1 | calibration · capability | selftest IDs/exit | — | 8 cases, exit 0 | **UNKNOWN** — no `SELFTEST_CASE` receipt in `.ufo/evidence/round-12` (grep count 0) | UNKNOWN | `tools/repeat-control.py:545` (selftest) |
| C1 | calibration · capability | snapshot validation | — | `controls_match` verified | **UNKNOWN** — `ControlGate/` has `run-{1,2,3}.{stdout,stderr,exit}` only; no `expected.json`, `command.txt`, `finding.txt` | UNKNOWN | `tools/repeat-control.py:50-62`; `.ufo/waves/round-12/w1/FrontierState.md:212` |
| C1 | calibration · capability | snapshot tamper refusal | — | exit 2 `snapshot_tampered` | **UNKNOWN** — not run (no snapshot to tamper) | UNKNOWN | `tools/repeat-control.py:412-421` |
| C1 | calibration · capability | observed gate findings (CLI, lane-run) | 0 | ≥1 receipt | **21 finding receipts**: `controls_match` 7 (`BytesReview/cli` C01,C03,C05,C18,C19,C20; `FailureOracle/actual-pristine/gate-runs`), `controls_mismatch` 5 (C02,C04,C06,C07,C08), `baseline_nonzero` 5 (C09–C13), `command_unavailable` 4 (C14–C17) | observed (lane-run, not a demonstration by itself) | `.ufo/evidence/round-12/BytesReview/cli/*/finding.txt` |
| C1 | calibration · motivation | single-control blind spot | — | recorded | BaselineControl scenario A: flaky suite → D1 `KILLED` on a harmless change (false kill); scenario C: unstable stdout, exit 0 → control GREEN, D1 `SURVIVED`; B and D: control RED, cannot evaluate (exit 2) | observed | `.ufo/evidence/round-12/BaselineControl/scenario-{a,b,c,d}.{exit,stdout}` |
| C1 | calibration · box mark | SHONEN marks changed | 0 | 0 | 0 changed (`ClaimSkeleton.md:15`) | held | `SHONEN.md:5-34` |
| C2 | depth · axis move (reanalysis) | bash-leg defects with declared-witness classification | 0 | 10 (**if measured**) | **0 measured — UNKNOWN**: `declared.tsv` absent; `summary.json` absent (`measure.py` reports `bash_witness_summary: {}`) | UNKNOWN | `tools/bash-witness-study.py` `declare` / `run` |
| C2 | depth · tool self-test | classifier selftest | — | pass | `WITNESS_SELFTEST: 21/21 pass`, `VERDICT: PASS` (00:43:35Z) — **predates the regex fix below** | observed, stale | `.ufo/evidence/round-12/BashWitness/selftest.out` |
| C2 | depth · declaration | declaration run | — | `WITNESS_DECLARE: …` | `WITNESS_STUDY: CANNOT-EVALUATE (runner is missing pin constant(s): REV_BASH)` (00:44:05Z) | blocked at last receipt | `.ufo/evidence/round-12/BashWitness/declare.out` |
| C2 | depth · pin | target pin | — | match | `PIN_BASH` = `275d8294…53009f` = `git show fecee874:corpus/surface-census.sh` sha | observed (now) | `tools/mutate-and-run.sh:544-545` |
| C2 | depth · denominator | cases per defect | 16 declared | 16 (14 exercised + 2 skip-rows on this host, since `the-janitor` is absent) | **UNKNOWN per run**: host PATH observed (`the-janitor` absent, `/usr/bin/sqlite3` present); no run receipt | UNKNOWN | `.ufo/evidence/round-12/BashDenominator/cases.tsv:15-16`; `tools/bash-witness-study.py` docstring |
| C2 | depth · recorded legs | seventh gate | 6 | 6 | 6 (`unique_recorded_gates=6`) | held | `tools/mutate-and-run.sh:84-89` |

## 5. Unknown runtime values (explicit)

These are **UNKNOWN** and must not be filled by this draft:

1. C1 `--selftest` exit code and per-case IDs (no transcript on disk).
2. C1 `--snapshot` verdict and `expected.json` digests (directory incomplete).
3. C1 tamper-run exit (not executed).
4. C1 finding ID the gate itself assigns to `ControlGate/run-{1,2,3}` (stable tuple) and to `ControlGate/mismatch/` (no `finding.txt`). The by-construction reading is `controls_match` and `controls_mismatch` respectively ([INFERENCE] from the saved bytes via `tools/repeat-control.py:191-205`; mismatch run-3 stdout is `mismatch-out-changed`).
5. C2 per-defect witness classification for all 10 defects (no `declared.tsv`, no `summary.json`, no `sweep` output).
6. C2 post-run depth value (only if a ledger case were recorded; none is planned — stays 6).
7. C2 host skip state: observed `the-janitor` absent from PATH and `/usr/bin/sqlite3` present (§6 F-6). The per-run skip set remains UNKNOWN until a run lands.
8. Current `bash-witness-study.py` selftest after the regex fix (see §6 F-3): no rerun receipt.

## 6. Findings (path:line)

**F-1 — ControlGate snapshot is incomplete.** `tools/repeat-control.py:61-62` names `.ufo/evidence/round-12/ControlGate/` as the committed snapshot location, and `.ufo/waves/round-12/w1/FrontierState.md:212` cites `ControlGate/expected.json` as the capability evidence pointer. The directory holds only `run-{1,2,3}.{stdout,stderr,exit}` (23:24:19Z) and `mismatch/`. `expected.json`, `command.txt`, `finding.txt` are absent (`find .ufo/evidence/round-12 -name expected.json` → none). Effect: `--snapshot` cannot pass, and the FrontierState capability pointer is dangling at read time. Owner: ControlSnapshot / ControlGate seats (w2 roster). Not fixed here.

**F-2 — No repeat-control selftest receipt.** `tools/repeat-control.py:545` defines `selftest()`; `grep -rl SELFTEST_CASE .ufo/evidence/round-12` → 0 files. The inventory's C1-1 transcript requirement (`.ufo/waves/round-12/w1/EvidenceScribe.md:44`; `EvidenceScribe/inventory.md:62`) is unmet. Calling C1 demonstrated without it violates `SCORECARD.md:244`.

**F-3 — C2 declaration blocker: regex bug, patched after the blocked receipt, not re-run.** `declare.out` (00:44:05Z) reports `runner is missing pin constant(s): REV_BASH`. Cause: `REV_BASH` in the runner is a 40-hex git SHA (`tools/mutate-and-run.sh:545`), while the pre-fix `PIN_RE`/pin read required 64 hex on both (the earlier read of `tools/bash-witness-study.py:174` showed `^(PIN_BASH|REV_BASH)=([0-9a-f]{64})$`). The selftest fixture used `"b" * 64` for `REV_BASH`, which masked the mismatch. Current file (mtime 00:44:58Z, after the receipt): `:174` `PIN_RE` = PIN_BASH 64-hex; `:175` `REV_RE` = `{7,64}`; fixture `:983` uses `"b" * 40`; a short-pin case is at `:999`. `selftest.out` (00:43:35Z) predates the patch. Status: patch present, **not verified by receipt**; `declared.tsv` not produced. Recommendation for L1/WitnessFinish: rerun `declare` into a fresh evidence dir and retain the output; do not re-declare into the existing directory (the tool refuses that, `tools/bash-witness-study.py:724-726`).

**F-4 — `SKILL.md` is modified in the worktree; calibration binding at risk.** `git diff --stat` → `SKILL.md | 40 +++++++++-` (uncommitted). sha256 of worktree `SKILL.md` = `593dfe58…`; HEAD = `33e3009c…`, the pin the box-3 cold-read binds to (`LOG.md` K1; `SHONENReview.md:33`). `SHONENReview.md:34` recommended no SKILL.md edit this round. Not an authority decision here. L1 must reconcile before any box-1/box-3 mark is cited.

**F-5 — Source-status flips are uncommitted and one row conflicts with the lesson.** `measure.py` (worktree) → `source_status` mined 15 / queued 26 / rejected 3; HEAD baseline `before.json:8-12` → mined 12 / queued 29 / rejected 3. The uncommitted flips include S004 and S026 (`.ufo/waves/round-12/w1/` lesson table `corpus/lessons/round-12.md` Gate). That lesson says the S026 reader "omitted the article body. No article quotation is credited from that partial view." `corpus/knowledge/repeated-control-precondition.md:16-21` nonetheless quotes the S026 post body with line numbers (`S026.html:1130-1137`), and its header cites `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`. I did not confirm that file exists or that its excerpts match the sha256 (`ca1145fb…`) recorded at `repeated-control-precondition.md:1`. Status: **unresolved conflict**, to be settled by L1 before the knowledge note is cited as Core support (`PROVINCE.md:40-42`).

**F-6 — C2 denominator rule is unsettled.** `.ufo/evidence/round-12/BashDenominator/cases.tsv:15-16` marks `verbs-sandboxed` and `verbs-break-injection` as `skip-case`. The tool's classifier treats only the two expected verb skips as acceptable (`tools/bash-witness-study.py` docstring ~:40-61). A host lacking `the-janitor` gives 14 exercised + 2 skipped. The claim's "full denominator" wording (`claims.json:7`) must say whether a skip counts; AdmissionBounds raised the same point (`.ufo/waves/round-12/w1/AdmissionBounds.md:95`). Unresolved.

**F-5 late addendum.** `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv` exists (header: verbatim served-byte excerpts with location lines). I did not verify its excerpts or the S026 sha256 against the served bytes. The conflict with the lesson's "no article quotation is credited" statement is unresolved.

**F-7 — C1 score field vs capability field.** `claims.json:6` records C1 as `score_before 6 / score_after 6`. The requested capability move is 0 → 1 in the capabilities table. Both are drafted here: the scalar stays 6; the capability count is the only field that moves, and only conditionally (§3). `claims.json:9` ("both worked") overstates C1 under `SCORECARD.md:244`; AdmissionBounds `:32` flagged the same.

## 7. Out of scope / not done

- No commits, no edits to `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`, or `corpus/`.
- No run of `repeat-control.py`, `bash-witness-study.py`, or the mutation runner (assignment is read-only; WitnessFinish owns the C2 experiment).
- No installs or upgrades.
- The `the-janitor`/`sqlite3` PATH check completed late (bg_114): `the-janitor` absent from PATH; `/usr/bin/sqlite3` present. Recorded in §5 item 7 and §6 F-6.

## 8. Checks L1 should run once after all seats land

1. `python3 tools/repeat-control.py --selftest; echo exit=$?` → retain transcript (F-2).
2. Create `ControlGate/expected.json` via the snapshot protocol, then `--snapshot` and a tamper run (F-1).
3. `python3 tools/bash-witness-study.py declare` into a fresh evidence dir, then `run`, `count`, `check` (F-3, F-6).
4. Reconcile `SKILL.md` sha (F-4) and the S026 conflict (F-5) before any SHONEN or knowledge claim.
5. Then fill the §4 UNKNOWN cells from receipts only; keep scalars at 6 unless a box or ledger case changes.

## 9. Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/CapabilityEvidence.md`
- Receipts read: `.ufo/evidence/round-12/{ControlGate,BaselineControl,BashWitness,BytesReview/cli,FailureOracle,claims.json,before.json,measure.py}`, `tools/{repeat-control.py,bash-witness-study.py,mutate-and-run.sh}`, `SCORECARD.md`, `LOG.md:529-663`.
