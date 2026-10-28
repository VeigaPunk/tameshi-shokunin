# T56W3MutCounterArms — frozen C1 counter, arm liveness at PIN

Counter: `.ufo/evidence/round-56/c1/measure.py` (frozen, not edited). PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd`. C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.

## Result in one paragraph

The frozen counter does **not** print `C1_R56_PASS=true` at PIN. The single failing arm is arm 6, and it fails on case: `'round-21' in cells[2]` is case-sensitive, while the last calibration row at `SCORECARD.md:2718` says `Round-21 cold-read monitor ...`. The other five arms pass at PIN (precheck `lost=0 ok`, monitor `64/64 score=8 box3=true`, one `rekey-r56-c0137451f5b7` with 18/18 bound, readers 18/18, `unstable=0`). Because the baseline is red, the eight PIN scores below are INCONCLUSIVE, not KILLED. On a green control that differs from PIN only by lowercasing that one word, the counter prints PASS and every mutant stays true (SURVIVED), as expected for relaxations. Four arms are witnessed by a real state; two arms (arm 1 precheck literal, arm 2 thresholds) and arm 5 have no witness in the states I could build.

## Baseline (no mutant)

Canonical lane and the pristine scratch clone give the same line (`--explain`, exit 1):

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=2f5512a8ab07 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor covered=64 score=8 box3=True
EXPLAIN arm3-rekey dirs=['rekey-r56-c0137451f5b7'] c0=c0137451f5b7f22d65f748fc69f1b181f55e1378
EXPLAIN arm4-readers 18/18
EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='Round-21 cold-read monitor `calibration_restraint_score`; tw' round='56'
C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false
```

Arm 6 evidence (checked by a direct read of the file at PIN): `'round-21' in cell2 = False`, `'Round-21' in cell2 = True`, `\b56\b in cell4 = True`. The row is the last `calibration` row with five cells (`SCORECARD.md:2718`, round 56, measured commit `c1dd23b3f83f`).

Control (scratch fixture `bd65b7c011d6d56e4c7d04b348f639e850184c20` = PIN + one commit changing only SCORECARD.md line 2718, `Round-21` → `round-21`):

```
C1_R56: rev=bd65b7c011d6 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true   (exit 0)
```

This is the only change needed to make the frozen counter green at a content revision. It is a lane production-file change, so it is for L1 to integrate. I did not edit the lane.

## Mutant set (eight single edits, all in fresh `git clone --shared` clones detached at PIN; old string asserted unique in code)

Note on the set: all eight are **relaxations** (a condition replaced by a weaker or `True` expression). A relaxation can only turn a false verdict into true, never a true verdict into false. So "KILLED = verdict goes false" cannot happen for any of them at any green state. The live test for each is therefore whether a real state exists where the original refuses for that arm and the mutant admits it. I report that as the witness.

Old-string uniqueness: `covered == 64`, `score == 8`, `'round-21'`-style strings occur in the docstring too, so M2/M3 were anchored to code (`monitor_ok = covered == 64 and score == 8`).

| id | arm | edit (line in frozen file) | PIN baseline (before → after) | PIN status | Green control FIX (before → after) | Status | Witness state (original → mutant) | Verdict |
|---|---|---|---|---|---|---|---|---|
| M1 | 1 precheck | L154 `'lost=0 ok' in last` → `True` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0, PASS=true | SURVIVED | base 981c5e8: precheck exit 1 (RED) → unchanged, total=5 → total=5. No witness built. | arm 1 literal is only reachable with exit 0 and `lost>=1` (see below) |
| M2 | 2 monitor coverage | L169 `covered == 64` → `covered >= 46` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | base: covered=46 score=6 → still fails on score, total=5 → 5. No state with covered in 46..63 and score 8 observed. Unwitnessed. | arm 2 coverage threshold not discriminated by any observed state |
| M3 | 2 monitor score | L169 `score == 8` → `score >= 6` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | base: covered=46 → still fails on coverage. Needs covered 64 with score 6–7; not observed. Unwitnessed. | arm 2 score threshold not discriminated by any observed state |
| M4 | 3 rekey count | L220 `rekeyed != len(frozen)` → `rekeyed < 0` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | base 981c5e8 (rekey absent, rekeyed=0/18): **total=5 → total=4** (the 18-count failure disappears; verdict still false) | **arm 3 count check is live** (witnessed at base; verdict stays false there) |
| M5 | 4 readers sha | L247 `section_sha256 == sec['sha256']` → `True` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | fixture W5 (`d2444be0648bfb9dc4b47d1887bccd639530ee07`; one committed reader `T56W2Read01.json` section_sha256 set to 64 zeros): **original total=1, readers=17/18, PASS=false → mutant total=0, readers=18/18, PASS=true** | **arm 4 sha check is live (witnessed)** |
| M6 | 5 stable inputs | L65 `UNSTABLE_INPUTS = ('LOG.md','SCORECARD.md')` → `()` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | no bound rekey entry at PIN pins `LOG.md` or `SCORECARD.md` (18 bound, 0 such pins; `unstable=0`). Base has no rekey dir. No witness built: the fixture needs a LOG.md pin in a 13.3 MB ledger whose line the read tool would not tag for me. | **arm 5 is dead at PIN and at FIX: nothing it could fire on exists** |
| M7 | 6 restate row score | L273 `row_score == score` → `True` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | fixture W7 (`50516e43232c07cf10f967b557d9edf624bed468`; row score 6, measured at base `981c5e8b`, where monitor=6): **original total=1, restate=6 vs monitor 8, PASS=false → mutant total=0, PASS=true** | **arm 6 score-equality check is live (witnessed; this is the R55.3 stale-row class)** |
| M8 | 6 restate ancestry | L271 `is_ancestor(lane, row_commit, rev)` → `True` | total=1 → total=1 | INCONCLUSIVE | total=0 → total=0 | SURVIVED | fixture W8 (`005e4ab9dc3e296ee995e2bf307ca023a42bd592`; row cites sibling commit `c34fcffd`, which is not an ancestor of W8, monitor there = 8): **original total=1, score_at_row=None → mutant total=0, score_at_row=8, PASS=true** | **arm 6 ancestry check is live (witnessed)** |

All eight PIN "after" lines are byte-identical to the baseline line above. All eight FIX "after" lines are byte-identical to the FIX control line. The witness output lines are in the table and quoted in full below.

Exact witness lines:

```
W5 original: C1_R56: rev=d2444be0648b c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=17/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false   (exit 1)
W5 M5:       C1_R56: rev=d2444be0648b c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true    (exit 0)
W7 original: C1_R56: rev=50516e43232c c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=6 total=1 C1_R56_PASS=false   (exit 1)
W7 M7:       C1_R56: rev=50516e43232c c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=6 total=0 C1_R56_PASS=true    (exit 0)
W8 original: C1_R56: rev=005e4ab9dc3e c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false   (exit 1)
W8 M8:       C1_R56: rev=005e4ab9dc3e c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true    (exit 0)
base 981c5e8 original: C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false   (exit 1)
base 981c5e8 M4:       C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=4 C1_R56_PASS=false   (exit 1)
```

M1 and M4 detail. M1: the frozen precheck (`coldread-precheck.sh`, lines 27–30) exits 1 when `len(cc) < len(fc)` and exits 0 otherwise. In the exit-0 case it prints `lost=N ok`, where N counts floor-credited headings lost even though the candidate gained at least as many credited headings. So the arm's `'lost=0 ok'` literal is the only thing that refuses "exit 0, lost≥1". At PIN, FIX, and base, that state does not occur, so M1 is SURVIVED everywhere I could score it. The arm is effectively gated by exit code; the literal covers only one corner. I did not build a fixture that produces that corner.

## Findings about the counter (for L1)

1. **Red at PIN (blocker for the deciding run as written).** `C1_R56_PASS=true` cannot be obtained at PIN with the frozen counter; it prints `total=1 C1_R56_PASS=false` (arm 6, case). Repair under the frozen-counter rule is a lane content change, not a counter change: SCORECARD.md line 2718 `Round-21` → `round-21`. The control FIX differs from PIN by exactly that and is green. Diff for L1 to integrate:

   ```
   -| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |
   +| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |
   ```

   The change touches no entry input (`SCORECARD.md` is not in any bound entry's inputs, `unstable=0`), no reader report, and no `C0`. The PIN moves; the rekey bindings do not. L1 must confirm this on the new content commit by rerunning the counter; I have only demonstrated it on the scratch fixture.

2. **Arm 5 is dead.** No bound entry pins `LOG.md` or `SCORECARD.md` at PIN, so the stable check cannot fire. M6 is SURVIVED everywhere I could score, and it is not witnessed.

3. **Arm 1 and arm 2 thresholds are not independently discriminated.** M1, M2, M3 never change a verdict in any state I could observe (PIN, FIX, base). They are either redundant with the exit code (M1) or only reachable in states the monitor does not produce (M2, M3).

4. **Arm 6 is the only arm exercised by the actual R55.3 failure mode, and it is live.** M7 and M8 are each witnessed by a stale row and a non-ancestor row commit. The arm is live, but its case-sensitive `'round-21'` literal is what reds PIN, which is a separate check the mutant set did not cover.

5. **Arm 3 and arm 4 are live.** M4 is witnessed at base (total 5 → 4, the 18-count failure removed), and M5 is witnessed by a corrupted reader sha.

## Limits

- The baseline is red at PIN, so the PIN scores are INCONCLUSIVE by the attack rule. The green control and the witnesses are scratch fixtures; the deciding run must reproduce them on the L1's committed PIN, not on my scratch revs.
- W5, W7, W8 are scratch-only commits. They are reproducible from the recipe above, not from the lane.
- M6 witness was not built (ledger tagging); M1, M2, M3 have no witness state in the three revs and the fixtures I built.
- Tools installed: none. Stdlib `python3`, `git`, `sha256sum` only. No pacman.
- Scratch clones and fixtures were under `/fast/scratch/hyaku/tameshi-r56/T56W3MutCounterArms` and are removed after this report. Lane tracked files were not modified; this report is the only file written in the lane.

## Reproduction commands

```
python3 <clone>/.ufo/evidence/round-56/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 2f5512a8ab0771fb2eee463ec16db359174f5edd --work <empty dir> --explain
# → C1_R56: rev=2f5512a8ab07 ... total=1 C1_R56_PASS=false   (exit 1)

python3 <clone>/.ufo/evidence/round-56/c1/measure.py --lane <fixture-with-SCORECARD-line-2718-lowercased> --rev <that commit> --work <empty dir> --explain
# → ... total=0 C1_R56_PASS=true   (exit 0)
```

Mutants: one-line edit to a clone's copy of `measure.py`, then the same command. The clone at PIN has the same objects as the lane, so `--lane <clone>` and `--lane <lane>` read identical bytes.
