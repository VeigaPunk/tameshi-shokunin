# T55W2CritDoNothing — the do-nothing controls

Seat: T55W2CritDoNothing (critic, axis: calibration, milestone: the do-nothing controls).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Nothing here edits the lane; every score
below runs the frozen counter bytes against a `git clone --shared` at the revision named.

## 1. What I attacked

1. Both claims' do-nothing score: the lane at base `0a2010acd1e92e4e332774050825e21bcfc7e079`,
   scored with the frozen counter bytes taken from the freeze commit (see §2 on which freeze).
2. Every control receipt in `.ufo/evidence/round-55/control/` against its pre-registered verdict.
3. The three phase-A negative controls re-built independently in my own scratch, plus two
   controls of my own that the round does not pre-register:
   - values-carried-exactly-but-no-fixes (stronger than `CTL_SKIP_c1`),
   - fixes-carried-but-section-removed (the mirror: does the corrected arm bind at all?).

Axis named: **calibration** (the record must agree with the tree on ten routed defects) and the
control layer that decides whether either claim's target is reachable without doing the work.

## 2. Frozen bytes actually used

`freeze.json` is self-consistent at every revision I read (every `files` hash matches
`git show REV:<path> | sha256sum`). The *pointer* is not machine-readable (`freeze.json` has no
`frozen_at`, unlike round 53), and it moved during this wave:

| revision | amendments | c1/measure.py | c2/measure.py |
|---|---|---|---|
| `e2979f2` (the pointer this seat's brief names) | 7 | `5e8f50d1…` | `36ca47d3…` |
| `133b2ce` | 8 | `5e8f50d1…` | `0458f632…` |
| `c31cdd9` | 8 | `5e8f50d1…` | `0458f632…` |
| `4f7a704` (lane HEAD while I worked) | 9 | `83dfbbb0…` | `0458f632…` |

I scored with **both** C1 byte-sets (`5e8f50d1` and `83dfbbb0`) and with the single C2 byte-set
in force since `133b2ce` (`0458f632`). The verdicts are invariant across them (§3, §4).

## 3. Do-nothing score — C1 (calibration)

Command (frozen bytes extracted from the freeze commit, clone at base):

```
git clone --shared --quiet LANE $S/clone-base
git -C $S/clone-base checkout 0a2010acd1e92e4e332774050825e21bcfc7e079
python3 $S/code-f5/c1/measure.py --lane $S/clone-base \
  --rev $(git -C $S/clone-base rev-parse HEAD) --work $S/work-f5-base --explain
```

Output (`T55W2CritDoNothing-receipts/f5-c1-base.explain`; full 28-line explain kept there):

```
EXPLAIN R54.1 FAIL premise=ok corrected=miss stale=6 derived=CTL_MISMATCH + 2/3
EXPLAIN R54.2 FAIL premise=ok corrected=miss stale=3 derived=freeze pointer=077d431e
EXPLAIN R54.3 FAIL premise=ok corrected=miss stale=1 derived=total=13
EXPLAIN R54.4 FAIL premise=ok corrected=miss stale=0 derived=c2 digest=8528ee85
EXPLAIN R54.5 FAIL premise=ok corrected=miss stale=0 derived=w1=28 w2=25 sections=12
EXPLAIN R54.6 FAIL premise=ok corrected=miss stale=0 derived=sweep commit=ff2a821
EXPLAIN R54.7 FAIL premise=ok corrected=miss stale=0 derived=rename commit=7fa9a5e
EXPLAIN R54.8 FAIL premise=ok corrected=miss stale=0 derived=config.yml + fabricated + seat marked
EXPLAIN R54.9 FAIL premise=miss corrected=miss stale=1 derived=reviewers=5 attack=21/76 seats=76 staged=0
EXPLAIN R54.10 FAIL premise=ok corrected=miss stale=0 derived=controls-a rekeyed=0/7
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
```

Exit 1. The earlier C1 bytes (`5e8f50d1`) print the same line byte-for-byte
(`T55W2CritDoNothing-receipts/c1-donothing.explain`). This also reproduces the committed
`.ufo/evidence/round-55/before/c1.stdout` verdict line at `4f7a704` exactly — the base receipt is
honest for the bytes it now claims.

**Verdict: CTL_0 for C1 is false, and not vacuously so.** Only R54.9 has `premise=miss` (its
staged-count receipt is introduced by this round); the other nine rows hold their premises and
still fail on `stale` (4 rows) and `corrected` (0/10). Excluding R54.9 entirely would leave total=9.

## 4. Do-nothing score — C2 (operability)

Command:

```
python3 $S/code-f5/c2/measure.py --lane $S/clone-base \
  --rev $(git -C $S/clone-base rev-parse HEAD) --work $S/w0-c2 --explain
```

Output (`T55W2CritDoNothing-receipts/c2-donothing.explain`, 44 explain lines):

```
EXPLAIN grammar repeat-control --selftest          rc=2  FAIL
EXPLAIN grammar registry-check --selftest          rc=2  ok
EXPLAIN grammar bash-witness-study selftest        rc=2  ok
EXPLAIN grammar pin-disposition --selftest         rc=2  ok
EXPLAIN grammar evidence-disposition --selftest    rc=2  ok
EXPLAIN grammar context-capture --selftest         rc=2  FAIL
EXPLAIN grammar env-diff --selftest                rc=2  ok
EXPLAIN grammar env-diff --contract                rc=2  ok
EXPLAIN grammar registry-check --rev               rc=2  FAIL
EXPLAIN lazy … (5/5 ok)   EXPLAIN empty … (13/13 ok)   EXPLAIN usable … (13/13 ok)
EXPLAIN docs                                      0/7 FAIL
EXPLAIN note                                      0/9 FAIL
EXPLAIN skill                                     0/1 FAIL
C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false
```

Exit 1. Failure decomposition: grammar 3 + docs 7 + note 9 + skill 1 = 20. The behavioural arm
carries 3 of the 20; documentation carries 17 — the claim's target is a conjunction, so this is
not a defect, but it means the do-nothing margin on *behaviour* is only three modes, and
phase B's `CTL_BREAK_c2` (not yet run) is the arm that certifies those three.

**Verdict: CTL_0 for C2 is false.** Note the committed `.ufo/evidence/round-55/before/c2.stdout`
prints `total=20`; the `total=21` in this seat's brief is the pre-amendment-8 arithmetic and is
still present in the committed receipt at `e2979f2`/`133b2ce` — same verdict, different
bookkeeping. Do not cite 21 for the current bytes.

## 5. Control receipts, pre-registered vs observed

Receipt under test: `.ufo/evidence/round-55/control/controls-a.stdout`.
While I worked it was **rewritten twice**: at 14:38 it held four CTL lines (516 bytes, snapshot
`T55W2CritDoNothing-receipts/controls-a.snapshot-1438.txt`); at 14:40:00 a restarted phase-A run
(`controls.sh a LANE 4f7a7040… 0a2010ac…`, pid started 14:39:56) truncated it to `CTL_0_c1`; by
14:46 it had rewritten four lines (snapshot `controls-a.snapshot-1446.txt`, `CTL_SKIP_c2` still in
flight). Every line I read — before and after the restart — matches my independent run in the same
row; the rows below are therefore re-derived, not merely quoted.

| control | pre-registered | receipt (observed 14:38 and 14:46) | my independent run | agree |
|---|---|---|---|---|
| CTL_0_c1 | false | `total=10 … C1_R55_PASS=false` | `total=10 premise=9/10 stale=4 corrected=0/10` (`f5-c1-base.explain`, `c1-donothing.explain`) | yes |
| CTL_0_c2 | false | `grammar=6/9 … total=20 … C2_R55_PASS=false` | `grammar=6/9 … total=20` (`c2-donothing.explain`) | yes |
| CTL_SKIP_c1 | false | `stale=4 classes_corrected=7/10 total=6 … false` | `stale=4 classes_corrected=7/10 total=6 … false` (`skip1.explain`) | yes |
| CTL_FAB_c1 | false | `stale=4 classes_corrected=0/10 total=10 … false` | `stale=4 classes_corrected=0/10 total=10 … false` (`fab1.explain`) | yes |
| CTL_SKIP_c2 | false | (in flight when I closed; expected `total=4 false` from the arm values) | docs 7/7, note 8/9, skill 1/1, tools untouched → grammar stays 6/9 → total=4, false (§6) | yes |

My fixtures are rebuilt by `T55W2CritDoNothing-receipts/run-c1-controls.sh` (C1) and
`T55W2CritDoNothing-receipts/doc-arms.sh` (C2 docs-only), each on a `git clone --shared` at base
whose `rev-parse --show-toplevel` is asserted equal to the fixture dir before any commit.

**No control prints true.** So neither the counter nor the target is inverted in phase A — but
"false as pre-registered" is necessary, not sufficient: §8.1 shows the phase-A C1 set cannot tell
the frozen counter from one whose stale arm is dead.

## 6. CTL_SKIP_c2, arm-level proof (and one fixture defect)

`doc-arms.sh` output (`T55W2CritDoNothing-receipts/doc-arms.txt`):

```
--- files changed vs BASE (the mutant must not touch tools/*.py) ---
SKILL.md
corpus/knowledge/scratch-root-contract.md
tools/registry.json
docs cells=7 docs=7/7
note names=8/9 missing=['registry-check --rev']
skill=1/1
```

Reading: the docs-only mutant satisfies `docs` (7/7) and `skill` (1/1) outright, and fails the
`note` arm only because its pasted mode list is the **pre-amendment-6 list of eight** — the ninth
allocating mode `registry-check --rev` is missing. With no `tools/*.py` touched, the nine grammar
arms are exactly the base arms already measured (6/9). Total would be 3 (grammar) + 1 (note) = 4,
`C2_R55_PASS=false`. The pre-registered verdict holds, twice over.

Finding (minor, fixable, does not change the verdict): **`CTL_SKIP_c2` is over-determined.** It
cannot show that the note arm refuses documentation-only work, because its own fixture leaves the
note short of 9/9. Smallest safe correction: append `registry-check --rev` to the `modes` list in
`controls.sh` phase A, so the docs-only control fails on the grammar arm alone.

## 7. My own controls: each C1 arm is necessary

Both were run on clones at the revisions named, with the frozen C1 bytes (`83dfbbb0`).

| control | rev | line | reading |
|---|---|---|---|
| values carried exactly, no stale fix (`correct1.explain`) | base+block | `stale=4 classes_corrected=8/10 total=6 … false` | correct values alone do not pass |
| fixes carried, corrections section removed (`fixonly.explain`) | C0 minus section | `premise=10/10 stale=0 classes_corrected=0/10 total=10 … false` | in-place fixes alone do not pass |

With the do-nothing line (total=10) and C0's line (`total=0 PASS=true`,
`f5-c1-c0.explain`) this is a four-point frontier: neither half passes, both together pass, nothing
passes.

## 8. Findings

1. **The C1 `stale` arm has no control coverage — the phase-A set cannot distinguish the frozen
   counter from one whose stale scan is dead.** This is the one finding that can let a falsehood
   survive a green C1. A dead scan is not hypothetical: amendments 5 and 9 both rewrote `scan()`
   (collapsed pass added, then applied to every row), and an early `return` / a dropped `hits`
   accumulation silently guts the arm.
   Witness (`T55W2CritDoNothing-receipts/dead-stale-witness.sh`, output in
   `dead-stale-witness.txt`): at C0 with **one** stale assertion reintroduced outside the
   corrections section,

   ```
   fixture rev=40488caacfbf
   frozen counter      : … stale=1 classes_corrected=10/10 total=1 C1_R55_PASS=false
   dead-scan counter   : … stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
   ```

   and the three pre-registered phase-A C1 controls, re-scored with the dead-scan counter:

   ```
   CTL_0_c1 (base)     : … stale=0 classes_corrected=0/10  total=10 C1_R55_PASS=false
   CTL_SKIP_c1 (skip1) : … stale=0 classes_corrected=7/10  total=3  C1_R55_PASS=false
   CTL_FAB_c1  (fab1)  : … stale=0 classes_corrected=0/10  total=10 C1_R55_PASS=false
   ```

   Every control still prints exactly its pre-registered verdict, so `CONTROLS_A: 5/5` would be
   earned by a C1 counter whose stale arm is dead. (Phase B's `CTL_POS_c1` cannot catch it either:
   at the certified revision `stale=0` with the honest counter, so the mutation is invisible there.)
   **Smallest safe correction:** pre-register one more C1 control — `CTL_STALE`, the C0 clone with a
   single stale assertion reintroduced outside the corrections section — expecting `total=1 false`.
   It costs one C1 run (seconds; measured above), and it is the only fixture in the set whose sole
   failing arm is `stale`. Strengthening `CTL_SKIP_c1` to carry all ten derived values (finding 2)
   achieves the same isolation but needs the seat marking and the staged receipt in the fixture.
2. **No control printed true.** CTL_0 (both claims), CTL_SKIP_c1, CTL_FAB_c1 are false with the
   frozen bytes, matching the pre-registered verdicts and the receipt. CTL_SKIP_c2 cannot pass:
   its behavioural arms are untouched and 6/9. There is no counter/target inversion to report —
   but per finding 1, "false as pre-registered" is weaker than it reads.
3. **Harness defect — `CTL_SKIP_c1` loses one of the values it claims to carry (minor, and it is
   what makes finding 1 possible).** `controls.sh` derives the rename commit with
   `git log --diff-filter=R "$REV" -- .ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json`.
   Pathspec-limited to the new path, git reports no rename there at base:

   ```
   $ git -C LANE log --format=%H --diff-filter=R 0a2010ac -- .ufo/…/T54W2Sent01-receipts/forged-reader.json | wc -l
   0
   $ git -C LANE log --format=%H 0a2010ac -- .ufo/…/T54W2Sent01-receipts/forged-reader.json | head -1
   7fa9a5e0104bc181872401547987d6744f3b570d          # what the C1 counter derives
   ```

   So the values-only block carries `renamed  config.yml` with an empty commit and R54.7's
   corrected arm misses for a fixture reason, not for the control's stated property (the block
   also cannot satisfy R54.8/R54.9 without the seat marking and the staged receipt). Result:
   `classes_corrected=7/10`, so the control is false on two arms and never isolates `stale`.
   Correction: drop `--diff-filter=R` (or use `--diff-filter=A`) for the new path.
4. **`CTL_SKIP_c2` does not isolate the note arm** — see §6; add the ninth mode to the fixture's
   list. By the same argument the C2 documentation arms have no sensitivity control either: a
   counter whose `docs`/`note`/`skill` arms were dead would read 7/7, 9/9, 1/1 and the docs-only
   mutant would still be false on grammar 6/9. [INFERENCE from the measured arm values; I did not
   build a dead-docs counter. Phase B's `CTL_BREAK_c2` covers the grammar arm only.]
5. **Provenance: the phase-A receipt does not name the freeze it certified, and it was rewritten
   mid-wave.** `controls.sh` prints neither the freeze commit nor a counter digest into
   `controls-a.stdout`, and the file lost the first run's four lines when the run restarted against
   `4f7a704` (9 amendments) at 14:40. `deciding-run.sh` does pin the freeze
   (`FROZEN_UNCHANGED=… freeze=… rev=…`) and refuses receipts whose commits do not descend from
   it, so the gate holds — but a reader of `controls-a.stdout` alone cannot tell which counter
   bytes produced it. Correction: `echo "FREEZE=$(git rev-parse "$FREEZE")"` plus the two
   `sha256sum`s as the first lines of the receipt. (Round 54's phase-A receipt has the same gap,
   so this is a carried weakness, not a round-55 regression.)
6. **Round-55 base receipts are honest for the bytes they now claim.** My independent run
   reproduces `before/c1.stdout` byte-for-byte at `4f7a704`; the C2 line differs from the
   `e2979f2`/`133b2ce` receipt by the amendment-8 bookkeeping only (21 → 20). The brief's `21`
   should be dropped from any record written from now on.

## 9. Is each claim's target beyond a do-nothing control?

- **C1 (calibration): yes.** Do-nothing is `total=10 premise=9/10 stale=4`; the target is `total=0`.
  Nine of the ten rows fail with their premises intact, so the gap is the record work itself, not a
  missing prerequisite. Values alone reach `classes_corrected=8/10` and stop (total=6); fixes alone
  reach `stale=0` and stop (total=10); together they reach total=0 at C0. The target needs both,
  and neither is reachable by inaction.
- **C2 (operability): yes.** Do-nothing is `total=20` (`grammar=6/9`, `docs=0/7`, `note=0/9`,
  `skill=0/1`). Documentation-only work reaches `docs=7/7`, `skill=1/1`, `note=8/9` and stops at
  `grammar=6/9` — the three defective modes are behavioural and can only be fixed in the tools.
  The behavioural margin (3 of 20) is thin, so the phase-B `CTL_BREAK_c2` receipt is the one that
  must actually certify it; it is not in phase A and was not run by me.

## 10. Commands and artifacts

Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W2CritDoNothing` (removed on exit; nothing written
outside my wave dir and that scratch). No mutating git/jj command ran in the lane; every fixture
commit happened on a `git clone --shared` whose toplevel was asserted first.

Artifacts opened: `.ufo/evidence/round-55/{contract.json,freeze.json,controls.sh,deciding-run.sh,
before/c1.stdout,before/c2.stdout,c1/measure.py,c2/measure.py,c1/staged-at-freeze.txt}`,
`.ufo/evidence/round-55/control/controls-a.stdout`, `.ufo/evidence/round-54/control/{controls-a,
controls-b}.stdout`, `.ufo/waves/round-55/spec-w2.json`, `.ufo/waves/round-55/w2/swarm-registry.json`;
commits `e2979f2`, `133b2ce`, `c31cdd9`, `4f7a704`, `9cf0146`.

Commands (all exit codes recorded in the receipt files):

```
python3 code-f5/c1/measure.py --lane clone-base --rev 0a2010ac… --work work-f5-base --explain
python3 code-f5/c1/measure.py --lane clone-c0   --rev 9cf0146b… --work work-f5-c0   --explain
python3 code-f5/c2/measure.py --lane clone-base --rev 0a2010ac… --work w0-c2       --explain
bash T55W2CritDoNothing-receipts/run-c1-controls.sh
bash T55W2CritDoNothing-receipts/doc-arms.sh $S
bash T55W2CritDoNothing-receipts/dead-stale-witness.sh $S
python3 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi   # exit 0, 140 rows
sha256sum <each frozen file>  vs freeze.json at e2979f2 / 133b2ce / c31cdd9 / 4f7a704
```

No tool installed or upgraded for this seat.
