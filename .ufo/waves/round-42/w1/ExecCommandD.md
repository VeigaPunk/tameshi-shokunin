# ExecCommandD — no-harm baselines at round-42 base (wave 1)

Executed at `REV=c77c2b7e64d2e356381441ecf94abac03e984606` (round-42 base) from a scratch
clone `/tmp/tameshi-r42-ExecCommandD-1` (`git clone --shared` of the lane; HEAD
`322b5cd` freeze commit). Both commands are read-only — they resolve blobs at REV via
`git show` / `git rev-parse` and print JSON; the scratch clone was byte-clean after both
runs (`git status --porcelain` empty) and was deleted before this report. No tool installs
performed (none needed). No lane-checkout edits.

## Finding 1 — SCORECARD command D (depth): `recorded_cases=9 depth_score=9`

Exact command (as printed in `SCORECARD.md:73`, run from the repo):

```sh
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Output (exact):

```
recorded_cases=9 depth_score=9
```

Matches the expected no-harm baseline (depth_score=9; the runner's ledger comment holds nine
recorded cases at the base). This equals the round-41 measurement (`SCORECARD.md:1922-1923`,
`recorded_cases=9 depth_score=9`).

## Finding 2 — round-21 coldread monitor (calibration): `calibration_restraint_score=6`

Exact command (round-41 block, `SCORECARD.md:1704`, `:1924`):

```sh
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV
```

Run in the scratch clone with `REV=c77c2b7…`. Exit 0; stdout (key fields):

```json
{
 "calibration_restraint_score": 6,
 "coldread": {
  "box3_full_page": false,
  ...
 }
}
```

Full JSON printed to stdout; stderr empty. `calibration_restraint_score=6` is the expected
no-harm calibration baseline (round-41: "the round-21 coldread monitor prints
`calibration_restraint_score: 6` at both revisions", `SCORECARD.md:1924-1927`; box 3 stays
uncredited — `box3_full_page=false`, consistent with the `[~]` SHONEN box-3 lane assertion
that earns no points). The monitor wrote nothing: the scratch clone's working tree was clean
after the run (`git status --porcelain` empty). The monitor does read external input digests
(e.g. fleet-repo files under `/home/vgpnk/Projects/shokunin/`) read-only as part of its
input-keyed ledger bookkeeping; none were modified.

## Could not check

- Nothing beyond the two baseline commands was asked; no counter was run against any tip
  (the deciding C1/C2 runs belong to the L1). Both baselines are the live no-harm reference
  for the round.
