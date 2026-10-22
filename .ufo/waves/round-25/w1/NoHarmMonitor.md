# NoHarmMonitor — round-25 wave 1 (calibration)

Seat: `NoHarmMonitor` (executor, calibration axis). Report written by a leaf seat; no
production file was edited, no git/jj write was issued in the lane, no gate was run inside
the live lane checkout.

## Verdict

**PASS — every lane no-harm monitor holds at the frozen revision `c9ff09f`, and the same
monitors hold at the wave base `1f73157`. Nothing in the wave's frozen revision regresses
a registered gate, and the frozen round-21 counters are numerically identical at base and
at REV (calibration 8, depth 8).**

One calibration hazard was found and it is a *false-alarm* hazard, not a lane defect:
two registry rows (`round21-measure-selftest`, `mutate-and-run-regression`) fail when the
lane is checked out **outside a fleet root**, and pass unchanged when it sits in one. A
no-harm reviewer who clones the lane into a bare directory will read `held=45/47` and
report two false regressions. Details and the smallest safe correction are in
[Finding F2](#f2-false-alarm-hazard-clone-layout-not-a-lane-defect).

The wave's own C1 counter is at `0/3` at REV and the gap is **record-only**, not
execution: the two sweeps already hold (green control, restore OK, every defect killed
with its `FAIL` witness) — what is missing is the SCORECARD rows and one disposition file
([Finding F5](#f5-the-c1-gap-at-rev-is-record-only-not-execution)).

## Setup

Private clone, per the item:

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/noharmmonitor-r25
git -C /tmp/noharmmonitor-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
```

Two clones were used, one per revision, and both were then placed in a **fleet layout**
(a directory whose children are the lane plus one entry per `*-shokunin` sibling lane):

```
/tmp/noharm-fleet-rev/tameshi-shokunin   # clone at c9ff09fb41fb8aac5fc335faf10858ff606bd5df
/tmp/noharm-fleet-base/tameshi-shokunin  # clone at 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5
```

Sibling lanes are **symlinks** to the read-only live siblings
(`/home/vgpnk/Projects/shokunin/{kumitate,kagi,tsukuroi,mado}-shokunin`, …); no sibling
lane was written (see [Writes](#writes-and-non-effects)).

The fleet layout is not cosmetic — see F2. The first attempt ran the monitors in a bare
`/tmp/noharmmonitor-r25` clone and produced two spurious `differs` rows; every number
below was re-measured in the fleet layout.

## Monitor results at REV (`c9ff09fb41fb8aac5fc335faf10858ff606bd5df`)

| # | Command (cwd = lane clone) | Exit | Summary line |
|---|---|---|---|
| 1 | `bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 96/96 pass` · `VERDICT: PASS` |
| 2 | `python3 tools/command-binding.py --selftest` | 0 | `COMMAND_BINDING_SELFTEST: 44/44 pass` |
| 3 | `python3 tools/registry-check.py --help` | 0 | usage block; documents `python3 tools/registry-check.py [--root DIR] [--rev REV] …`, trailer `REGISTRY_CHECK: held=<N>/<M> superseded=<K>`, and "prefer `--rev`" |
| 4 | `python3 tools/registry-check.py --root /tmp/noharm-fleet-rev/tameshi-shokunin` (documented live check) | 0 | `REGISTRY_CHECK: held=47/47 superseded=7` (54 `ROW` lines) |
| 5 | `python3 tools/registry-check.py --root /tmp/noharm-fleet-rev/tameshi-shokunin --rev c9ff09fb41fb8aac5fc335faf10858ff606bd5df` (documented hermetic check) | 0 | `REGISTRY_CHECK: held=47/47 superseded=7` |
| 6 | round-21 strict monitor, command taken from `.ufo/evidence/round-24/landing-verification.json` → `checks.monitor.argv`: `python3 .ufo/evidence/round-21/coldread/measure.py --repo /tmp/noharm-fleet-rev/tameshi-shokunin --rev c9ff09fb41fb8aac5fc335faf10858ff606bd5df --explain` | 0 | `calibration_restraint_score: 8`, `depth_score: 8`, `trace_gate: "strict"` |

Round-21 strict monitor, full summary at REV (`.ufo/evidence/round-21/coldread/measure.py`):

```
calibration_restraint_score = 8      depth_score = 8
recorded_cases = 8                   ledger_committed = true      ledger_source = "rev"
overrides_used = false                trace_gate = "strict"
ledger_legs = 8 (js-kimi-census, bash-surface-census, bash-tsukuroi-census,
                  bash-mado-verify, bash-checklist-run, js-claims-check,
                  js-round-gate, js-sources-check)
ledger_guardrail = {header_legs 8, lists_agree true, regression_calls 8,
                    selftest_tuples 8, unique_recorded_gates 8}
coldread = {sections_covered 62, sections_total 62, missing 0, uncovered_headings 0,
            ledger_present true, box3_full_page true, inputs_overlay_merged 0}
shonen  = {asserted 4, boxes 4, marks ["~","~","~","~"], untouched 0}
sources = {rows 83, malformed 0, status {mined 54, queued 23, rejected 6},
           tiers {A 74, B 7, C 2}}
```

**Base comparison (`1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`)** — same monitors, same
fleet layout:

* `python3 tools/registry-check.py --root /tmp/noharm-fleet-base/tameshi-shokunin --rev 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5` → exit 0, `REGISTRY_CHECK: held=47/47 superseded=7`.
* round-21 strict monitor at base → exit 0, `calibration_restraint_score: 8`, `depth_score: 8`, `recorded_cases: 8`, `ledger_guardrail` identical, `coldread.sections_covered 62/62`, `sources.rows 83`, `trace_gate: "strict"`.

So: **REV introduces no monitor regression and no numeric drift** (calibration 8 → 8, depth
8 → 8). This matches round 24's own landing verification, which recorded
`REGISTRY_CHECK: held=47/47 superseded=7` and the same 11/11 discriminating hardening
checks.

## Wave counters, measured read-only at REV

**C1 (calibration axis, the wave's own counter)**

```
python3 .ufo/evidence/round-25/c1-measure.py --repo /tmp/noharm-fleet-rev/tameshi-shokunin
→ exit 1
→ C1_ROUTED: dispositioned=0/3
```

Per-item detail from the same run:

| Item | `holds` | executed evidence | `scorecard_row` | reason |
|---|---|---|---|---|
| R23-ROUTED-1 | **true** | `MUTATE: DONE (target=r25-multitoken defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)`, `control_green: true`, `restore_ok: true`, witnessed kills M1–M6 | false | — |
| R23-ROUTED-2 | **true** | `MUTATE: DONE (target=r25-selftest defects=8 killed=8 survived=0 inconclusive=0 kill-rate=100%)`, `control_green: true`, `restore_ok: true`, witnessed kills G1–G8 | false | — |
| R23-ROUTED-3 | false | `dead: 34` | false | `disposition file absent` |

The recorded "before" receipt is reproducible: running the **REV** counter against the
**base** clone (`--repo /tmp/noharm-fleet-base/tameshi-shokunin`) gives exit 1,
`C1_ROUTED: dispositioned=0/3`, with reasons byte-identical to
`.ufo/evidence/round-25/c1-before.json` (`absent: .ufo/evidence/round-25/c1-suite.py,
…multitoken-cases.json, …multitoken-mutants.spec, …guard-mutants.spec` /
`disposition file absent`).

**C2 (coverage axis, cross-check only — not this seat's item)**

```
uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /tmp/noharm-fleet-rev
→ exit 0
→ MTE_INTEROP: PASS legs_conforming=8/8
```

All eight legs report `CONFORMS (schema=ok official_score=<x> tameshi_score=<x>
official_killed=<k> recorded_killed=<k> official_valid=<v> recorded_defects=<v>)` with the
official and tameshi scores equal on every leg. Run read-only against the `/tmp` fleet
layout; the live fleet root was not used as `--fleet-root`.

## Findings

### F1 — no-harm: clean

Every registered gate in `tools/registry.json` (47 active rows + 7 superseded) holds at
REV, in both the live and the hermetic (`--rev`) invocation of the documented check, and
the same registry holds at base. The two selftests report full passes
(`96/96`, `44/44`). The frozen round-21 counters are identical at base and REV. Nothing
in the frozen revision harms any axis.

### F2 — false-alarm hazard: clone layout, not a lane defect

In a bare clone (`/tmp/noharmmonitor-r25`, no sibling lanes present) the documented
registry check reports two rows that differ:

```
ROW mutate-and-run-regression expect=0 got=2 differs
ROW round21-measure-selftest expect=0 got=1 differs
REGISTRY_CHECK: held=45/47 superseded=7          (exit 1)
```

Observed causes:

* `bash tools/mutate-and-run.sh --regression` → exit 2, `REGRESSION: SETUP (cases=8
  passed=0 cannot-verify=8)`, with every leg reporting
  `REGRESSION_CASE <leg>: SETUP (repo_identity_mismatch: /tmp/kumitate-shokunin is not its
  own repository; toplevel=unresolved)`.
* `python3 tools/round21-measure.py --selftest` → exit 1,
  `CalledProcessError: Command '['git', '-C', '/tmp/tameshi-shokunin', 'show',
  '08175c62d661fddf052ed10abc91313dec8eb77d:tools/mutate-and-run.sh']' returned non-zero
  exit status 128` (raised at `tools/round21-measure.py:74`).

Both tools resolve sibling lanes as **`<lane-parent>/<repo-name>`**: the regression legs
come from `.ufo/evidence/round-21/c2-contract.json`, whose surfaces are `tameshi-shokunin`,
`kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`, and
`tools/round21-measure.py` reads `ROOT.parent / surface["repo"]` (`tools/round21-measure.py:74`).
A lane checkout named `tameshi-shokunin` inside a directory that holds the other lanes
satisfies that; a bare `…-r25` clone does not. In the fleet layout both rows hold
(`held=47/47`), which is also what round 24 recorded.

**Smallest safe correction (for reviewers and for any future clone-based re-run):** run
lane monitors from a fleet-layout clone — the lane directory named `tameshi-shokunin`
inside a parent that contains one entry per `*-shokunin` sibling lane — and treat
`repo_identity_mismatch` / `git show … returned non-zero exit status 128` as a
**setup** failure of the sandbox, never as a lane defect. No lane file needs changing to
fix this; a lane change here would be a false repair of a non-defect.

### F3 — record accuracy: the C1 "before" is a working-tree counter measured at base

The contract's C1 "before" is quoted as *dispositioned=0/3, exit 1 at 1f73157*. At the base
revision the counter does not exist at all — `.ufo/evidence/round-25/` is absent from the
base tree (the base's newest evidence directory is `.ufo/evidence/round-24`) — so running
the counter *as committed at base* is exit 2 (`can't open file
'/…/.ufo/evidence/round-25/c1-measure.py': [Errno 2] No such file or directory`). The
recorded before value is reproducible only in the way the receipt states it: the REV-era
counter run against a base clone, which I reproduced exactly (exit 1, `0/3`, same
reasons). The claim's wording stays accurate about the *state* (nothing recorded at base,
`SCORECARD` carries no `R23-ROUTED` rows); it is the *tool* that is newer than the base
revision it grades.

### F4 — pin drift, already amended: no action

The contract pins the C2 tool as `tool_sha256 58a5ae92…`; that is the freeze commit
`2a97ec1`'s copy. The contract's own named lane revision `c9ff09f` carries
`tools/mte-interop.py` at `sha256 311448d92c10891e2fd9513586c203d4d245f94559ab7843de48bef4de1db422`
(commit message: *mte-interop --fleet-root stages sibling lanes so clones can run the C2
counter*). This drift is already recorded in
`.ufo/evidence/round-25/contract-amendment-1.json` (`tool_sha256_frozen` /
`tool_sha256_now`, `at_revision c9ff09f…`), and the amended tool passes 8/8 (measured
above). The vendor pins are exact at REV:
`mutation-testing-metrics-3.9.0.tgz = ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548`,
`mutation-testing-report-schema-3.9.0.tgz = adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280`
— identical to `contract.json`. **Do not re-pin**; the amendment already covers it.

### F5 — the C1 gap at REV is record-only, not execution

At REV the two executed sweeps already hold (F-table above): green control, restore OK,
every defect killed with an explicit `FIXTURE … FAIL` / `CASE … FAIL` witness. The counter
still reads `0/3` because the *record* is missing:

* `SCORECARD.md` carries no row whose first cell is `R23-ROUTED-1` / `-2` / `-3`
  (`scorecard_row: false` for all three; the counter matches `^\|\s*<label>\b`,
  `.ufo/evidence/round-25/c1-measure.py:145`).
* `.ufo/evidence/round-25/dead-falsifier-disposition.json` does not exist
  (`reason: "disposition file absent"`), and the round-23 wave-2 input
  `.ufo/waves/round-23/original-outcomes2.json` lists **34** seats whose status is not
  `completed`.

Smallest safe correction, for whichever seat owns the C1 record (not this seat — I wrote
nothing but this report):

1. Add three `SCORECARD.md` rows whose leading cell is exactly the label
   (`| R23-ROUTED-1 …`, `| R23-ROUTED-2 …`, `| R23-ROUTED-3 …`); the label is what the
   counter matches, and the row must sit in the lane's own scorecard, not in a wave note.
2. Add `.ufo/evidence/round-25/dead-falsifier-disposition.json` with `{"rows": [...]}` whose
   row set equals exactly the 34 dead seats from
   `.ufo/waves/round-23/original-outcomes2.json`; each row needs `name`, a `status` in
   `{reattacked-agree, reattacked-finding, reattack-seat-died}`, and either a `report`
   path (existing file) whose text contains exactly one line
   `R23-REATTACK <name>: AGREE|FINDING` matching the status, or — for a dead re-attack
   seat — non-empty `error` text
   (`.ufo/evidence/round-25/c1-measure.py:90-118`).
3. Re-run the counter; both negative controls must fail as required (dropping one row and
   flipping one status each have to break the check), otherwise the item does not count.

I did not create these records: they are the C1 record seat's deliverable, and the
counter's own vacuity is under attack by another wave seat (`MeasureVacuity`).

## Writes and non-effects

* Live lane checkout: **nothing written** except this report file
  (`.ufo/waves/round-25/w1/NoHarmMonitor.md`). No `git`/`jj` write command, no checkout,
  no reset; `git -C <lane> rev-parse HEAD` = `09dc114da9002525d31985c14093d32c6712bff4`
  (read-only).
* Sibling lanes: **nothing written**. Post-run `git status --porcelain` on
  `kumitate-shokunin` (clean), `kagi-shokunin` (3 modified files under
  `.ufo/waves/round-28/build/`, mtime 2026-10-21 14:54 −0300), `tsukuroi-shokunin`
  (untracked round-24 wave files, mtime 2026-10-22 05:25 −0300) — all predate or belong
  to other live seats' work; the registry rows only read siblings (the single absolute
  path in `tools/registry.json` is `pin-disposition-read`, `--root /home/vgpnk/Projects/shokunin`,
  a read).
* My clone only: the live-mode registry check wrote two untracked paths into the **clone**
  (`.ufo/evidence/round-15/attempt-4/`, `.ufo/evidence/round-15/verification-4.json`) —
  documented behaviour of live mode ("rows may write into the root; prefer `--rev`"). No
  tracked file in the clone differs from `c9ff09f`.
* Scratch: `/tmp/noharm-fleet-rev`, `/tmp/noharm-fleet-base`, and the C2 run's own
  staging copies under the tool's temp dir.

## Tooling record

* `uv 0.13.0` (already present at `/home/vgpnk/.local/bin/uv`) used for
  `uv run --no-project --with jsonschema==4.25.1 …` — resolved `jsonschema==4.25.1`
  from PyPI into the uv cache for the C2 cross-check. No system package was installed,
  updated or removed; no host service was restarted; no pacman transaction was issued.

## Risks / blockers

* None blocking. The single live risk is F2 (false "differs" rows in a bare clone),
  which any reviewer of this wave can hit; the correction is a sandbox-layout rule, not
  a code change.
* `measure.py` reads absolute live-fleet paths for its external-input ledger
  (`/home/vgpnk/Projects/shokunin/…`), so the round-21 strict monitor is not fully
  hermetic; that is pre-existing at base and unchanged at REV (identical numbers on both
  sides), so it is recorded, not repaired here.
* The wave's live lane has advanced past `c9ff09f` (HEAD `09dc114`); every number in
  this report is measured at the frozen revision the contract names, per the item.
