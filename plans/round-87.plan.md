# Round 87 — successor counters, frozen before the after-state

Base: `master` at `4a079f6ab57ab2f47b9e502a35eca75ec180cda7` (round-86 tip).
Pre-freeze instruments (committed before this declaration): `a3b4f75d…` (counter,
census v2, controls, receipts) and `38c83698…` (v2-schema overreach manifest).
This declaration is the round-87 freeze; its hash is recorded in `LOG.md`.
L1: TameshiR87. Attempt 1.

## Declaration

Two claims on distinct axes. Round-86's counter and census are NOT amended; both
remain committed and their verdicts stand. Both successors are NEW freezes.

### R87-C1 — operability, capability acquisition

A successor certification counter for `tools/design-blob-audit.py`, closing the
four round-86 routed classes: opaque per-run labels (no class substring in any
root or receipt name), a fixture worktree forced off the candidate tree, exact
stdout and stderr comparison (no `rstrip` tolerance), and git pinned to
`/usr/bin:/bin` for the counter and for every child tool call.

- Before (round-86 counter, its own counterfeits): `T86E2-att3b-cheat.py` 8/8 and
  `T86CN1-oracle-worktree.py` 8/8 (kill, lesson `round-86.md` M3).
- After (this counter, measured at `a3b4f75d` in `.ufo/evidence/round-87/pre-freeze/c1/`):
  real instrument `passed=8/8`; controls `ctl-att3b-label-worktree` 0/8,
  `ctl-cn1-oracle-worktree` 1/8, `ctl-fingerprint` 0/8, `ctl-sequence` 0/8,
  `ctl-pinned-hash` 0/8, `ctl-always-accept` 0/8, `ctl-r85-forgery` 0/8.
- Frozen predicate, the same sentence in this plan, in the counter's PASS label
  and in the receipt: `C1_R87 rev=<rev> passed=8/8 C1_R87_PASS=true`, exit 0, from
  `python3 -I .ufo/evidence/round-87/measure.py --repo LANE --rev REV --work EMPTY_DIR`.
- Controls: each run as `--tool CONTROL --work EMPTY_DIR` and must print
  `C1_R87_PASS=false`. Control bytes are committed at `a3b4f75d` (`controls/`,
  sha256 in `pre-freeze/sha256s.txt`).
- Do-nothing control: tool absent at REV prints `passed=0/8 C1_R87_PASS=false`,
  exit 1.
- Kill rule: any control printing `passed=8/8`, or the real instrument printing
  `passed<8/8` at REV, kills the claim. A miss is an honest stop.
- Capability-table rule (AXES §Capabilities): the row enters `SCORECARD.md`
  `## Capabilities` only if the predicate verifies at the landing revision.
- Sourced: `S299` (Python `shutil` documentation: `shutil.which` for trusted git
  resolution) and `S289` (git `cat-file`: blob contents for expected rows).

### R87-C2 — calibration (lowest scored axis: calibration 8 of depth 10 / calibration 8 / freshness 9)

The capability census must catch overreach: a receipt pin that resolves to a
tree, a symlink, a path with a line suffix, or an uncited path must not bind a
capability row. Census v2 reads manifest and self-state FROM GIT at `--rev`,
refuses non-repo-relative paths, requires a pin to be a regular blob entry
(mode 100644 or 100755) named by its own row, and matches citations exactly.

- Before (census v1, identical overreach rows, filesystem manifest):
  `CAP_CENSUS: rows=30 bound=30 unbound=0 mismatches=0`, exit 0
  (`pre-freeze/c2/v1-overreach-before.txt`). Real population under v1:
  `rows=30 bound=30 unbound=0 mismatches=0` (`v1-real-before.txt`).
- After (census v2 at `38c83698`): overreach `CAP_CENSUS_V2: rows=30 bound=0 unbound=30
  mismatches=0`, exit 1 (`pre-freeze/c2/v2-overreach.txt`); real
  `CAP_CENSUS_V2: rows=30 bound=30 unbound=0 mismatches=0`, exit 0
  (`pre-freeze/c2/v2-real.txt`).
- Frozen predicate (landing revision REV):
  (a) real: `CAP_CENSUS_V2: rows=N bound=N unbound=0 mismatches=0`, exit 0, where N is
  the number of `## Capabilities` table rows at REV, from
  `python3 -I -X utf8 tools/capability-census-v2.py --repo . --rev REV --manifest tools/capability-census-v2.json --selfstate tools/selfstate-freshness.json`;
  (b) overreach: the same command with
  `--manifest .ufo/evidence/round-87/overreach/r86-cited-tree-manifest-v2schema.json`
  prints `bound=0` and exits 1.
- Kill rule: any overreach row bound (`bound>=1`), any real row unbound, or v2
  selftest below 15/15 at REV, kills the claim.
- Stated limit, fixed before data: the lane's real population holds no
  overreach, so the measured move is overreach detection (0 → 30 of 30 overreach
  rows refused) with the real population held at 30/30. It does not claim that
  the lane's real self-assessment was miscalibrated; round-86's closure found no
  such error.
- Sourced: `S305` (git ls-tree: "The type of the object (commit, blob or tree).",
  snapshot line 1812 — tree entries carry mode and type) and `S289`.

## Frontier step

- `S289` (git cat-file) and `S299` (Python shutil) re-opened 2026-11-05 for the
  R87-C1 ground: fetch headers `date: Thu, 05 Nov 2026 07:38:31 GMT` for both;
  snapshots `.ufo/evidence/round-87/sources/s289-cat-file.html` (79360 B) and
  `s299-shutil.html` (120949 B). Located quotes and access dates are recorded in
  `corpus/lessons/round-87.md` `## Gate`. No new row planned; `used-by` old → new
  logged there.
- Mistakes to mine this round are recorded in the lesson at landing.

## Routed round-86 defects

| # | defect (round-86 closure) | round-87 handling |
|---|---|---|
| 1 | C2 before-state input not committed | v1 real and overreach before-state bytes committed at `a3b4f75d`/`38c83698` |
| 2 | final-tip figures without committed receipt | not in this round's claims; named as open |
| 3 | S305 fetch timestamp contradicts header | corrected in `corpus/SOURCES.md` round-87 note (new correction line, row unchanged) |
| 4 | attack-share figure disagrees between records | counting rule stated once in the round report (see report) |
| 5 | no QUALITY criterion for M3/M4 | criteria added at landing, citing `lessons/round-86.md` M3/M4 |
| 6 | retained instruments unregistered | open; named |
| 7 | successor C1/C2 work | this round's R87-C1 and R87-C2 |

Limits left open, named: the v1 census stays frozen; caller revision authority is
narrowed (v2 reads its manifest only from `--rev`) but the caller still chooses
`--rev`; receipt race and parent aliases; conversion attributes; malformed
kind/source-id.

## Assimilation

`Assimilation: none.` `merge/tameshi/MERGE-REPORT.md` (103 staged rows, 86 knowledge
entries) covers mutation-score semantics, flaky verdicts and PBT generators. None
serves R87-C1 or R87-C2, and nothing was appended. The quarantine-first duty is
not triggered (no append). `considerthese/2026-10-28.md` ideas 1, 2, 3 and 5 are
already implemented by committed tools (`quoted-line-exists.py`,
`arm-liveness.py`, `rekey-cost.py`, `pointer-recheck.py`); idea 4 (assimilation
backlog burn-down) does not serve these claims, so none was taken.

## coldread_forecast

Planned monitored edits: `corpus/SOURCES.md` (round-87 correction and `used-by`
entries) and `corpus/QUALITY.md` (criteria for M3/M4). Measured at base with
`python3 -I -X utf8 tools/rekey-cost.py --edit corpus/SOURCES.md --edit corpus/QUALITY.md`:
`REKEY_COST sections=71 planned=2 at_risk=13 predicted_lost=13`. The rekey is owed
after the edits land; the floor must read `lost=0` at the landing tip before any
admission is reported.

## No harm

No existing tool is modified. Round-85's counter, round-86's counter, the v1
census and their verdicts are untouched. Standing sweeps are run at the landing
revision and their receipts committed.

## Wave

One validated v1 wave, 10 seats: executor 3 (T87E1 counterfeit hunt on R87-C1;
T87E2 determinism and near-miss arm liveness on R87-C1; T87E3 overreach hunt on
R87-C2), scout 1 (T87SC1 pin inventory), connector 1 (T87CN1 read-only sibling
counter scan), scribe 1 (T87S1 located-quote check for the Gate), reviewer 1
(T87R1), critic 1 (T87C1), mutation-tester 1 (T87M1), sentinel 1 (T87SN1). L1 holds
the planner seat. Attack roles counted as reviewer, critic and mutation-tester:
3 of 10 = 30 %; sentinel is counted as robustness, not as attack. Sole integration
owner: L1. Seats use scratch under `/fast/scratch/hyaku/tameshi-r87/<seat>/` and
deliver findings and files only; they never commit, push or run a mutating git/jj
command.
