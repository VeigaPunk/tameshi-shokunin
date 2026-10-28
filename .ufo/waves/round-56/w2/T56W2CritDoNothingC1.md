# C1 do-nothing control — T56W2CritDoNothingC1

Milestone: **C1 do-nothing control** (tameshi round 56, wave 2). Question: can any tree that skips
the claimed C1 work (fresh reader seats + honest re-key + honest restate) score
`C1_R56_PASS=true` on the frozen counter
`.ufo/evidence/round-56/c1/measure.py`? Answer: **no** — every do-nothing tree fails, and the
strongest fake bind is caught by three independent arms. The counter and the target are sound.

## Method

- Scratch clone of the lane at C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378`
  (basis tree `50652f57c5bc7d461424a701207628b12aa22a3e`, verified equal to the candidate tree),
  fixture `/fast/scratch/hyaku/tameshi-r56/T56W2CritDoNothingC1/c0.aX8pRO`; every commit asserted
  `git rev-parse --show-toplevel` == fixture dir; no lane production file touched.
- Each attempt is a **committed** mutation; the counter is scored at the mutated HEAD
  (`--rev <mutated HEAD>`). Two earlier passes were invalidated and discarded: the counter reads
  git objects at `--rev` only ("the live working tree is never read"), so uncommitted working-tree
  edits, and commits scored under `--rev C0`, are both invisible to it. The committed-HEAD runs
  below are the evidence.
- A sha/start/end pre-filtered re-enumeration of stale credit was discarded: that filter is
  stricter than the counter's condition and eliminated both stale-crediting headings; the frozen
  counter and the direct `entry_reason` enumeration agree at 2/18.

## Control — C0 itself

`C1_R56: rev=c0137451f5b7 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`

Five failing arms: precheck (lost=18), monitor (46/64, score 6, box3 false), no re-key, no readers,
standing row says 8 while the monitor reads 6 (row names round 53, measured commit `d33053f7552d`
scores 6 — the R55.3 routed defect, live at C0).

## Attempts (all committed; receipts in `T56W2CritDoNothingC1-receipts/`)

| # | Tree | Mutation | Verdict line (abbreviated) | PASS |
|---|------|----------|----------------------------|------|
| ctrl1 | `5c9476735807` | delete all 295 ledger entries of the eighteen headings | `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5` | false |
| ctrl2 | `c73c7c626944` | standing calibration row score cell 8 → 6, nothing else | `restate=6 total=5` (arm6 still fails: last-change cell names round 53, not 56) | false |
| ctrl3 | `072870bf5ebf` | one entry re-pinned `read_rev=C0`, traces moved under `rekey-r56-c0137451f5b7/`, no reader report | `c0=c0137451f5b7 rekeyed=0/18 readers=0/18 total=5` | false |
| ctrl4 | `896e0f514511` | committed `rekey-r56-c0137451f5b7/` dir with a trace file, nothing bound | `c0=c0137451f5b7 rekeyed=0/18 readers=0/18 total=5` | false |
| ctrl5 | `193896253c49` | **strongest fake**: all 295 entries of the eighteen rebound at `read_rev=C0` under one re-key dir, `wrong_expectations=0 blocking_gaps=0`, no reader reports | `rekeyed=2/18 readers=0/18 unstable=10 total=6` | false |

## Findings

1. **No do-nothing tree reaches the target.** The cheapest skips fail on the same five arms as the
   control; the maximal fake bind raises `total` to 6. The counter is not bypassable by ledger
   surgery, directory stubs, or a lone restate edit.
2. **Deletion cannot fake 64/64** (ctrl1): `credited`/`lost` are derived from sectionize coverage
   against entries that pass credit — the eighteen already fail credit at C0 (stale hashes), so
   removing their entries changes nothing (`cand_credited=46 lost=18` unchanged).
3. **A lone restate edit cannot pass arm 6** (ctrl2): even with the score cell matching the monitor
   (6), the last-change cell must name round 56; the round must actually do the work to claim it.
4. **2/18 headings credit from stale entries** (ctrl5 + direct enumeration with the frozen
   round-18 `entry_reason`): "Mutation-sweep recipe — numbered steps; bounded cold-read" (stale
   seat T51W2Read01) and "Standing rules" (stale seat Read02) pass `entry_reason` once rebound at
   `read_rev=C0`; the other sixteen fail it. **But arm 4 independently requires 18/18 committed
   reader reports naming each heading with `cand=C0` and the C0 section sha256 — so no reader seat
   is skippable.** All eighteen seats remain strictly necessary.
5. **Arm 5 (unstable inputs) fires on the historical tail**: 10 of the rebound entries list
   `LOG.md`/`SCORECARD.md` in `inputs` (`unstable=10`). The binder must bind only entries whose
   inputs exclude those two files — rebinding the whole append-only tail of these headings would
   lose credit the same way rounds 53/55 did.
6. Ledger structure (receipt `entry-structure.json`): append-only, 591 entries at C0, 295 across
   the eighteen headings, each pinning `sha256`/`start`/`end`/`read_rev`/`traces`/`inputs`.

## Tooling

No tools installed or upgraded (none needed); no pacman transactions touched.

## Receipts

`T56W2CritDoNothingC1-receipts/`: `control.out`, `delete-eighteen.out`, `restate-score-6.out`,
`repin-one.out`, `traces-no-readers.out`, `full-fake-bind.out` (counter stdout+EXPLAIN per tree),
`ctrl1.tree`–`ctrl5.tree` (mutated HEAD full hashes), `entry-structure.json` (ledger shape).
