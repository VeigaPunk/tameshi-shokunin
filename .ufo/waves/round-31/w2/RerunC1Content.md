# RerunC1Content — frozen C1 counter at content revision 2da841bd

seat: `RerunC1Content`
axis: calibration (measured C1 rerun, no judgment added)

## Verdict

C1 at `2da841bd9913a2037d2bf612793382e572c9d205` **does not pass**: 11 of 12 statements MATCH, one
MISMATCH is the `calibration` row (claimed 8, observed 6); unparsed 0, unobservable 0, append_only 1,
`C1_R31_PASS=false`, exit 1. This is exactly the shape the wave expected before the cold-read ledger
append. No regression FAIL: the six-leg regression ledger printed `REGRESSION: PASS (cases=9
passed=9; ledger legs exact: killed-delta<=0 flips<=0)` and exited 0.

The counter that ran is the contract's frozen counter: `sha256
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584` of
`.ufo/evidence/round-31/c1-measure.py` equals `contract.json:counter_sha256`. The measured revision
resolves in the lane and the run used an empty scratch work directory. No production file was
modified and no lane git write command was run.

## Exact run and full stdout

```
mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/RerunC1Content
timeout 2700 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/c1-measure.py \
  --rev 2da841bd9913a2037d2bf612793382e572c9d205 \
  --work /fast/scratch/hyaku/tameshi-r31-seats/RerunC1Content/w1
```

Work directory was empty at start (`[]`). Wall time 157.9 s. stderr empty (0 bytes). Exit **1**
(the counter returns 1 when `mismatches>0`; `timeout` propagates it).

```
STATEMENT sources-registry: claimed=0,94 observed=0,94 (exit=0) MATCH
STATEMENT mutation sweep runner: claimed=106,106,0 observed=106,106,0 (exit=0) MATCH
STATEMENT six-leg regression ledger: claimed=PASS,9,9,0 observed=PASS,9,9,0 (exit=0) MATCH
STATEMENT repeated pristine-control gate: claimed=PASS,29,0 observed=PASS,29,0 (exit=0) MATCH
STATEMENT six-leg content-disposition probe: claimed=19,19,0 observed=19,19,0 (exit=0) MATCH
STATEMENT exposed witness provenance correction: claimed=39,39,0 observed=39,39,0 (exit=0) MATCH
STATEMENT effective expectation reconciliation: claimed=66,66,0 observed=66,66,0 (exit=0) MATCH
STATEMENT retained invocation-context gate: claimed=0,49,49 observed=0,49,49 (exit=0) MATCH
STATEMENT hermetic env-differential probe: claimed=9,9 observed=9,9 (exit=0) MATCH
STATEMENT callback-authoritative wave accounting: claimed=8,8 observed=8,8 (exit=0) MATCH
STATEMENT depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT calibration: claimed=8 observed=6 (exit=0) MISMATCH
C1_R31: statements=12 mismatches=1 unparsed=0 unobservable=0 append_only=1 rev=2da841bd9913a2037d2bf612793382e572c9d205 C1_R31_PASS=false
```

## Every statement vs the base receipt

Base lines are `.ufo/evidence/round-31/before/c1-at-base.stdout` (13 lines, receipt `c1-at-base.exit`
= `1`). "Claimed" rows at base: `SCORECARD.md` at base, capability rows `:240-249`, axis rows
`:66-67`. At the content revision every claimed value comes from the appended block, capability rows
`SCORECARD.md:1514-1523`, axis rows `:1536-1537`.

| statement | base claimed | base observed | base | content claimed | content observed | content | what changed |
|---|---|---|---|---|---|---|---|
| sources-registry | 0,44 | 0,92 | MISMATCH | 0,94 | 0,94 | MATCH | claim 44→94 (row `:1514`); observation 92→94 (SOURCES rows added) |
| mutation sweep runner | 80,80,0 | 106,106,0 | MISMATCH | 106,106,0 | 106,106,0 | MATCH | claim 80→106 (`:1515`); command output identical |
| six-leg regression ledger | PASS,6,6,0 | PASS,9,9,0 | MISMATCH | PASS,9,9,0 | PASS,9,9,0 | MATCH | claim 6,6→9,9 (`:1516`); command output identical |
| repeated pristine-control gate | PASS,29,0 | PASS,29,0 | MATCH | PASS,29,0 | PASS,29,0 | MATCH | none |
| six-leg content-disposition probe | 18,18,0 | 19,19,0 | MISMATCH | 19,19,0 | 19,19,0 | MATCH | claim 18→19 (`:1518`); command output identical |
| exposed witness provenance correction | 39,39,0 | 39,39,0 | MATCH | 39,39,0 | 39,39,0 | MATCH | none |
| effective expectation reconciliation | 34,34,0 | 66,66,0 | MISMATCH | 66,66,0 | 66,66,0 | MATCH | claim 34→66 (`:1520`); command output identical |
| retained invocation-context gate | 0,49,49 | 0,49,49 | MATCH | 0,49,49 | 0,49,49 | MATCH | none |
| hermetic env-differential probe | 9,9 | 9,9 | MATCH | 9,9 | 9,9 | MATCH | none |
| callback-authoritative wave accounting | 8,8 | 8,8 | MATCH | 8,8 | 8,8 | MATCH | none |
| depth | 6 | 9 | MISMATCH | 9 | 9 | MATCH | claim 6→9 (`:1536`); command D prints 9 at both revs |
| calibration | 0 | 8 | MISMATCH | 8 | 6 | MISMATCH | claim 0→8 (`:1537`); observation 8→6 (below) |

Only two observations moved between the two runs: `sources-registry` (92→94) and `calibration`
(8→6). All ten other commands printed the same values at both revisions, so their base mismatches
were claim staleness that the appended rows corrected, not tool changes.

### Why `sources-registry` observed 92→94

`corpus/SOURCES.md` gains two tier-A, status `mined` rows, `S095` (`:104`) and `S096` (`:105`); the
round-31 note records "New rows S095 (Go testable examples) and S096 (rustdoc documentation tests),
both mined by that entry. Rows 92 → 94" (`corpus/SOURCES.md:373-374`) and moves the next-free id to
`S097` (`:377`). `S055` is re-opened by editing that row in place (`corpus/SOURCES.md:64`; one line
replaced, row count unchanged). Running `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` in a scratch clone at
each revision:

- base `36c1d393`: `== A rows` `92`, tiers `A=83 B=7 C=2`, status `mined=64 queued=22 rejected=6`,
  `SOURCES_CENSUS: CLEAN`, exit 0.
- content `2da841bd`: `== A rows` `94`, tiers `A=85 B=7 C=2`, status `mined=66 queued=22
  rejected=6`, `SOURCES_CENSUS: CLEAN`, exit 0.

The monitor independently reports `sources.rows=94` at the content revision. (The wave brief's
"S095-S097" names the id space; this revision adds S095 and S096 only.)

### Why `calibration` observed 8→6

Statement command: `python3 .ufo/evidence/round-21/coldread/measure.py --repo {clone} --rev {rev}`,
read through the round-27 wrapper `.ufo/evidence/round-27/c1-measure.py`; the counter parses
`calibration_restraint_score`. Running the round-27 wrapper at each revision:

- base `36c1d393`: `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9` exit 0.
- content `2da841bd`: `C1_MONITOR: covered=55/64 restraint=6 box3_mismatch=1 depth_score=9` exit 1,
  with nine `uncovered:` lines (listed below).

The drop is repo state, not counter nondeterminism: the same frozen monitor reads 64/64 at base.
The cold-read ledger credits a SKILL.md section only when an entry's section `sha256` matches and
every recorded input blob still hashes as recorded. Nine of 64 sections lost credit at this
revision:

1. `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` (`SKILL.md:131`) — the two
   entries that credited it at base recorded `corpus/QUALITY.md`, `corpus/README.md`,
   `corpus/SOURCES.md`; all three changed.
2. `## Restore discipline — before/after identity, not continuous non-write proof` (`:375`) —
   `corpus/README.md`.
3. `### The map — where a reader enters, artifact by artifact` (`:1380`) — `corpus/README.md`.
4. `## Pin disposition and provenance correction — round 13` (`:1517`) — `corpus/SOURCES.md`.
5. `### Round-13 gate/probe registry` (`:1548`) — `corpus/SOURCES.md`.
6. `## Live-tree re-pin and entry-command monitor — round 17` (`:1814`) — `corpus/SOURCES.md`.
7. `## Input-keyed cold-read credit — round 17` (`:1855`) — section hash change, see below.
8. `### Round-20 gate/probe registry — frozen receipt instruments` (`:1938`) —
   `corpus/QUALITY.md`, `corpus/SOURCES.md`.
9. `## Ninth recorded case — round 26` (`:2104`) — `corpus/QUALITY.md`, `corpus/README.md`,
   `corpus/SOURCES.md`.

For 1-6 and 8-9 the section text is unchanged; their previously-crediting ledger entries name one or
more of the three corpus files edited by this revision as inputs, and `input_failures()` in
`.ufo/evidence/round-18/measure.py:330-350` marks such an entry `input-drift`, leaving no crediting
entry. Other input paths that appear in the union reason strings (`tools/mutate-and-run.sh`,
`tools/bash-witness-study.py`, `tools/trace-inputs.py`, `.ufo/evidence/round-17/*`,
`corpus/knowledge/incremental-pin-disposition.md`, `tools/registry.json`) are byte-identical between
base and content (e.g. `tools/mutate-and-run.sh` blob `2d81b929...` at both revs), so they cannot be
the cause.

Section 7 is the one `no-ledger-entry`: the content revision also edits `SKILL.md:1886` (one line,
the `--regression --workdir` rule: `git diff -U0 36c1d393 2da841bd -- SKILL.md`), which lies inside
the section that starts at `SKILL.md:1855` and ends before the heading at `:1897`. The section body
hash changes from `43a041e71156...` to `4869ae55bc8e...`; two ledger entries match the base hash and
zero match the revision hash, so the section is uncovered. `SKILL.md` is in the monitor's
`IGNORED_INPUTS` as an input gate, but the section text itself is the measured surface, so the edit
invalidates the entry regardless.

The new knowledge entry `corpus/knowledge/executable-self-assessment.md` is not recorded as an input
of any ledger entry, so it causes no credit drift. `box3_mismatch=1` follows: `SHONEN` box 3 is
marked `[~]` with the ledger link, and the monitor does not credit the full page (55/64).

## Append-only check

`SCORECARD.md` at base is a byte prefix of the file at `2da841bd`: base 118152 bytes, rev 125590
bytes, appended 7438 bytes, `append_only=1` from the counter. The appended bytes begin after base
line 1480; the block heading is `SCORECARD.md:1482` (`## Round 31 — standing self-assessment
re-stated ...`). No base byte was changed.

## What C1 still needs, and risks

- The one mismatch is the row this revision itself appended: `SCORECARD.md:1537` states
  `calibration | 8` with the note "Last-change round 29 (restored 6 → 8); held 30", while the monitor
  at this revision returns restraint 6. C1 passes only if the cold-read ledger append restores
  full-page credit (all nine headings above) at the measured revision, or the claim is measured at a
  later revision that carries that append. An append that covers only part of the nine leaves the
  row false and leaves the round-27 monitor non-zero.
- The contract's `no_harm.drift_plan` enumerates the SOURCES/QUALITY/README/knowledge-entry edits but
  not the `SKILL.md:1886` one-line edit. That edit is not an input-gate change (SKILL.md is ignored
  as an input) but it silently dropped one of the 64 cold-read sections. The fresh cold-read list for
  this wave should include `## Input-keyed cold-read credit — round 17` (`SKILL.md:1855`) as a drifted
  section, alongside the eight corpus drift sections.
- `S055` was rewritten in place in `corpus/SOURCES.md` (`:64` at the content revision; one line
  replaced, row count unchanged, only its `used-by` field extended). This does not affect the census
  row count but is an in-place edit to a source row; noted for the integrator, not judged here.
- No test, gate, formatter or lint was run in the lane repository; all execution was inside
  `/fast/scratch/hyaku/tameshi-r31-seats/RerunC1Content/`. No tool was installed or upgraded. No
  process survives this item (checked `/proc/<pid>/cwd`; none owned by this seat).

## Retained evidence

- Full stdout/stderr of the run: `/fast/scratch/hyaku/tameshi-r31-seats/RerunC1Content/c1-at-content.stdout`
  (13 lines, pasted above) and `c1-at-content.stderr` (0 bytes); per-statement command output:
  `.../w1/obs-*.stdout`.
- Monitor JSON at the content revision: `.../monitor-at-content.json` (`sections_covered=55`,
  `sections_total=64`, `calibration_restraint_score=6`, `box3_full_page=false`, `revision=2da841bd...`,
  `trace_gate=strict`, `overrides_used=false`).
- Base/monitor comparison: `clone-base` at `36c1d393` and `w1/clone` at `2da841bd`, both in the same
  scratch root. Round-27 wrapper receipts saved as `round27-at-base.stdout` (`C1_MONITOR:
  covered=64/64 restraint=8 box3_mismatch=0`, exit 0) and `round27-at-content.stdout` (`C1_MONITOR:
  covered=55/64 restraint=6 box3_mismatch=1`, exit 1, plus the nine `uncovered:` lines quoted above).
- Census at both revisions run in scratch clones: 92 → 94 rows, `SOURCES_CENSUS: CLEAN`, exit 0 both.
- Counter identity: `sha256sum .ufo/evidence/round-31/c1-measure.py` =
  `657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584`, equal to
  `.ufo/evidence/round-31/contract.json:claims[0].counter_sha256`.
