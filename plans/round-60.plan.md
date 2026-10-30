# tameshi round 60 — plan (frozen before data)

Fresh-start round (run-13): reads the last three rejected closures
(r57 honest-stop, r58 not-admitted forgery, r59 honest-stop cheat-passable
counter + spot-check `corpus/lessons/round-59-verifier-spotcheck.md`) and
declares only claims a do-nothing control cannot reach. Base
`9806562c7efc816bd979923e702ef39bc41cade7` (= origin/master, clean tree).

## Stagnation nudge premise

Scored axes sit at or above the saturation line 8 (depth 10, calibration 8,
freshness 9, per the round-58/59 standing rows); no capability has entered
the SCORECARD table with a verified admission since round 50. The
lowest-axis obligation is waived (`AXES.md` §The stagnation nudge); the round
is a capability + calibration move. Premise stated on the SCORED axes only
(round-59 spot-check defect 5); coverage/adjacency/operability are
verdict-only axes this round.

## Claim C1 — operability, capability re-certification (sourced: S290)

**Predicate (one sentence, same in contract.json and the counter's PASS
label):** at the round's final lane revision, the installed counter
`tools/executor-source-pin-measure.py` (8 shuffled class cells × 5 declared
paths in ONE invocation per cell, per-run nonces, shuffled order, corrupt
cell expecting exit 2) run on the amended `tools/executor-source-pin.py` v2
scores `passed=8/8 C1_R60_PASS=true`, while the control family scores
`C1_R60_PASS=false` on every arm: do-nothing tool-absent 0/8, unfixed v1
tool 7/8 (only the corrupt cell failing — the red-before for the exit-2
reconciliation), always-accept, fingerprint, sequence, hash-only,
first-path-only, and empty-blob-unsound controls each fail.

**Counting command:** `python3 -I tools/executor-source-pin-measure.py --lane <lane> --rev <rev> --work <empty scratch dir>`

**Kill rule:** any change to the counter's cells, class set, expected exits
or PASS condition after the first scored run voids the claim (re-freeze +
re-declare required); any control scoring 8/8 kills the counter and the
claim honest-stops.

**Red receipts (frozen before data, committed this round):**
`.ufo/evidence/round-60/controls/*.out` — do-nothing-tool-absent
`passed=0/8 … reason=tool-absent`; v1-tool-red `passed=7/8` (corrupt cell
expected 2 observed 1); ctl-always-accept 3/8; ctl-fingerprint 3/8;
ctl-sequence 3/8; ctl-hashonly 3/8; ctl-first-path-only 6/8;
ctl-empty-unsound 4/8 — every arm `C1_R60_PASS=false`.

**Source:** S290 (Python `secrets` documentation, opened this round) grounds
the per-run nonce fixture design.

## Claim C2 — calibration (routed-defect and mistake dispositions)

**Predicate (one sentence):** the round's final tree records the round-59
closure's routed defects and uncaptured mistakes where the tree can check
them: `corpus/routed-defects.json` carries rows `R59.1`–`R59.8` (one per
round-59 spot-check §6 item; `fixed` rows carry in-tree receipts, non-fixed
rows carry status `open` with reason), `corpus/QUALITY.md` carries ≥5 new
numbered criteria each citing `corpus/lessons/round-59.md` (one per
`captured-by: none` mistake), `SCORECARD.md` carries the annotation
`not admitted (honest stop, closure round 59)` on the round-59 C1 capability
row and a saturation premise restated on the scored axes, and the cold-read
precheck run at (base `9806562c…` → final revision) is recorded with
`lost=0` (no heading covered at base loses credit from this round's edits).

**Counting commands:**
- `python3 -c "import json;d=json.load(open('corpus/routed-defects.json'));rows=[x for x in d['defects'] if x['id'].startswith('R59.')];print(len(rows), sum(1 for x in rows if x['status']=='fixed'))"`
- `grep -c 'corpus/lessons/round-59\.md' corpus/QUALITY.md`
- `grep -c 'not admitted (honest stop, closure round 59)' SCORECARD.md`
- `bash .ufo/evidence/round-48/quality/coldread-precheck.sh <lane> 9806562c7efc816bd979923e702ef39bc41cade7 <final-rev>` (recorded receipt)

**Kill rule:** any counting command ambiguous at adjudication (two
reasonable readings) kills the claim honest-stop; receipts that do not
resolve at the final revision defeat the claim.

**Do-nothing control (§9, committed before data):** every C2 counting
command run at base `9806562c…` scores zero — R59.* rows 0, QUALITY
criteria citing round-59 lesson 0, SCORECARD annotation 0. A do-nothing
round cannot reach a nonzero target; receipt `T60W1S19/receipt.json`
(wave seat re-derivation) plus L1 re-run recorded in the report.

## No-harm guards

- No SKILL.md or PROVINCE.md edits (round-21 cold-read monitor input bytes
  unchanged; forecast prices all planned edits at 0 headings —
  `tools/cold-read-forecast.py` run 2026-10-30, `headings=0 readers=0 of 64`,
  14 headings already uncovered at base, not counted).
- Contract carries `coldread_forecast` (round-59 mistake 5 / criterion 110).
- Sibling lanes, fleet repo, `.ufo/state/`, `templates/`, `scripts/`:
  read-only. Seats never commit. All scratch under
  `/fast/scratch/hyaku/tameshi-r60/`, deleted on exit.
