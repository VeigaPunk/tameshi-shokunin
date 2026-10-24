# W2MTLedger5 — round-36 C1 trace-receipt deletion probe

Seat: mutation-tester (leaf). Lane tip observed: `fbb01cf46f8437fd1264c1a3acc053c882fa2164`
(`round-36 verifier spot-check (integrator, hyaku)`). Measured claim: **C1** (calibration;
cold-read monitor refresh restores credit 6 -> 8 per the round-36 contract).
Scratch lane clone (isolated, disposable): `/fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger5/lane`.
Nothing was written in the lane repo or any other checkout; no tool installs.

## Attack

One-behavior mutation: delete **one of the four** round-36 cold-read trace receipts that the
refresh commit `b455001` added, at a scratch commit, leaving the ledger and SKILL.md untouched.

- Target file: `.ufo/evidence/round-36/coldread/traces/L1/source-2.json`
  (owning ledger entry: section start **375**, `## Restore discipline — before/after identity,
  not continuous non-write proof`, class `record`, one trace).
- File sha256 before mutation: `1e23a1ad6892cf2c5369aca1079d76b752520271c318a56fd8a61cda82482797`
  (blob `4d9a476367edac1ca6a7338d317eb98c16d63bb2` at `b455001`).
- Rationale for this receipt: each of the four refreshed sections is credited **solely** by its
  fresh round-36 record entry; all 13–15 older same-sha ledger entries are `input-drift` stale at
  `b455001` and therefore cannot mask the loss (verified per entry before mutating).

## Commands (all absolute; run from the scratch clone)

Baseline (pristine bytes at the refresh commit):

```
python3 /fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger5/lane/.ufo/evidence/round-21/coldread/measure.py \
  --repo /fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger5/lane \
  --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c
```

Mutation (`git rm` + scratch commit; mutant rev `698491868ea757a8086d0c1c5c4536137d8c75d3`,
1 file, 39 deletions — only that trace removed):

```
git rm .ufo/evidence/round-36/coldread/traces/L1/source-2.json
git commit -m "mutant: delete round-36 trace receipt source-2 (restore-discipline entry)"
python3 .../measure.py --repo .../lane --rev 698491868ea757a8086d0c1c5c4536137d8c75d3
python3 .../measure.py --repo .../lane --rev 698491868ea757a8086d0c1c5c4536137d8c75d3 --explain
```

Restoration:

```
git checkout b455001e2589b3f4f471d94a3de7e5e549b9f54c -- .ufo/evidence/round-36/coldread/traces/L1/source-2.json
git commit -m "restore: exact source-2 bytes from b455001"     # restored rev 5a76bb43dfae31b811822490d3523eba76bc9907
python3 .../measure.py --repo .../lane --rev 5a76bb43dfae31b811822490d3523eba76bc9907
```

All three runs used `trace_gate: strict`, `overrides_used: false`, exit code 0
(a trace loss is scored, not raised — the monitor stays a measurement, not a gate).

## Expected vs observed

| run | rev | expected | observed |
|---|---|---|---|
| baseline | `b455001e` | 8, 64/64 | `calibration_restraint_score: 8`, `sections_covered: 64/64`, `box3_points: true` |
| mutant (source-2 deleted) | `698491868e` | owning entry `trace-missing:<path>`; section loses credit; score drops | **yes**: score **6**, covered **63/64**, box3_points **false** |
| restored | `5a76bb43df` | back to 8, 64/64 | `8`, `64/64`, `box3_points: true` |

Mutant section record (`--explain`, only uncovered section):

```
start 375, credited false, vetoed false, end 404
reason: input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh;trace-missing:.ufo/evidence/round-36/coldread/traces/L1/source-2.json
reasons: [input-drift:corpus/README.md, input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh,
          trace-missing:.ufo/evidence/round-36/coldread/traces/L1/source-2.json]
```

Per-entry attribution at the mutant rev (round-18 `entry_reason`, strict):

| section | owner trace | entry_reason |
|---|---|---|
| 131 | source-1.json | `None` (credits) |
| **375** | **source-2.json (deleted)** | **`trace-missing:.ufo/evidence/round-36/coldread/traces/L1/source-2.json`** |
| 1380 | source-3.json | `None` |
| 1436 | source-4.json | `None` |

So the loss is attributed to the owning entry only; the three sibling receipts still credit.

Credit-loss mechanism: the deleted receipt makes the fresh 375 entry fail the trace gate, so
`sections_covered` drops 64 -> 63; `box3_full_page` requires full coverage
(`sections_covered == sections_total`), so `box3_points` flips true -> false, and the
`calibration_restraint_score` component `2 * box3_points` drops 2 points: **8 -> 6**.
(Observed, not merely inferred: both fields flipped in the same run.)

## Restoration evidence

- Restored file sha256: `1e23a1ad6892cf2c5369aca1079d76b752520271c318a56fd8a61cda82482797` —
  identical to the pre-mutation hash above; `cmp` against `b455001:<path>` byte-identical.
- Restored commit tree `ced3aa52cc0fb6dd6b5da9a0e71922201f005d0c` == `b455001` tree
  (`git diff --stat b455001 5a76bb43` empty after restore).
- Monitor output at restored rev equals baseline in every field except `revision`/`rev_input`.
- Scratch clone retained for inspection at `/fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger5/`
  (`out/baseline.json`, `out/mutant.json`, `out/mutant-explain.json`, `out/restored.json`,
  `out/traces-before.sha256`, `out/mutant-rev.txt`, `out/restored-rev.txt`).

## Verdict

**KILLED.** C1's trace gate is behavior-bearing: deleting one of the four round-36 trace
receipts at the refresh commit makes exactly the owning entry fail `trace-missing`, removes
credit from its section, and drops the C1 score from 8 to 6 (64/64 -> 63/64). Baseline passed,
so the result is a genuine kill, and the mutation was restored byte-exactly (tree identical,
monitor output identical apart from the revision field).
