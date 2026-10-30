# T58W1Panel06 — blind calibration panel

Axes: evidence accuracy, five-item completeness, blindness, reproducibility, zero lane mutation.

## Result

All five assigned items are fixed at base `2a32aa8228d5f86a85c81a923a3148bf792a9538`. These are independent recommendations, not admission decisions.

The scratch clone was created with `git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06 clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone`; root identity was asserted before detached checkout. Checkout output: `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`. The captured `rev-parse HEAD` matches the assigned base. Every resolving hash below was checked with `git merge-base --is-ancestor HASH BASE`: exit 0, empty stdout/stderr.

No candidate ledger or other panel was read. No round-57 wave content was read. A broad filename discovery glob incidentally returned round-57 staged filenames; those paths were not opened. The source registry and lesson files were inspected as primary content, not used as authority for their own status claims.

## Per-item evidence

### R53.8 — fixed

Resolving commit: `ca75c2674645ab6bdadeecb8584007c74342bfa9` (ancestor of base).

`corpus/SOURCES.md:150` now says `p. 3 (physical; printed footer 1787)`; `corpus/knowledge/change-aware-resweep-cadence.md:2` says `p. 3 (physical)`. The exact introducing patch is `99c3bc88d704566197783f66b211ee0a830e0330`. The Gate's historical 22/19 parentheticals are explicitly superseded by `corpus/lessons/round-57.md:12-18`, which gives 20/20. The latter patch, ca75c267, completes the compound item. Commands: `git blame -L 150,150 -- corpus/SOURCES.md`, `git blame -L 2,2 -- corpus/knowledge/change-aware-resweep-cadence.md`, `git blame -L 12,18 -- corpus/lessons/round-57.md`, and both introducing `git show` patches (absolute -C shown in the transcript below).

### R53.9 — fixed

Resolving commit: `d33053f7552db4bd290c99a36979760f544c41ad` (ancestor of base).

`git show --format=fuller --stat d33053f7552db4bd290c99a36979760f544c41ad` prints exactly the six named additions, `6 files changed, 1581 insertions(+)`. `git ls-tree -r HEAD --` restricted to those six paths prints six `100644 blob` entries (not filesystem-only artifacts). This resolves the tracking defect rather than merely changing its description.

### R54.1 — fixed

Resolving commit: `870d9b987f14a046964018429662a238f2fe9e20` (ancestor of base).

The original receipt remains honestly false: `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`, `CONTROLS_B: 2/3 as pre-registered`. `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` corrects SCORECARD and both lesson assertions; QUALITY has a superseding erratum. Do not mistake the round-55 deciding script for a complete fix: it still accepts arbitrary n/m. The current round-57 canonical script, introduced by 870d9b98, has `.ufo/evidence/round-57/deciding-run.sh:148-150`: equal numerator/denominator, CTL_MISMATCH refusal, committed exit exactly zero. Phase B is scored at REV (`.ufo/evidence/round-55/controls.sh:119-124`, and the round-57 controls implementation was independently read at its introducing commit). Thus the later cited commit completes the full item, including the failed-control admission path. Commands and exact guard text are captured below.

### R54.2 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (ancestor of base).

`git show 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- SCORECARD.md` shows both active freeze locations changed to `077d431e`. ER-R54-2 names the three old pointers and supersedes them with the one deciding pointer. `.ufo/evidence/round-54/after/frozen.stdout:1` prints `freeze=077d431e69965fa4673cd006ab64f6fc387f9e15`. Historical references inside the explicitly labeled erratum are not active competing pointers.

### R54.3 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (ancestor of base).

The same patch replaces the live claim's `total=14` with `total=13` and withdraws the misleading smoke/receipt delta. ER-R54-3 repeats `Old: total=14 ... Corrected: total=13`. The original before receipt line 8 prints `total=13 C2_R54_PASS=false`. The routed spot-check itself preserves the separate disclosure that the contract before-string expanded at 077d431e after 441c26be; no contrary 14-valued receipt was found or asserted. Commands: SCORECARD introducing patch and blame, receipt blame, and the scoped literal search of SCORECARD/contract/lesson performed during review.

## Residual risk and verification gaps

LSP discovery returned `No such tool: xd://lsp`; therefore references/definition/diagnostics were unavailable. Literal searches located excerpts only; Git history, patches, exact receipts and ancestry provide the evidence, not semantic LSP proof. These are documentary/control-flow status judgments; no full deciding runtime, census, cold-read monitor, resume path, rerouting or saturation workload was invoked or claimed to pass. Fleet-side archived reports were not modified or independently re-opened: lane errata explicitly supersede their incorrect historical assertions. Round-54/55 frozen scripts remain historical artifacts; the current round-57 gate supplies the completed guard.

No tools installed or updated. No implementation changes proposed or staged. Scratch was removed before submission (cleanup command recorded below).

## Command/output transcript

Machine-readable exact argv, stdout, stderr and exit status are in `T58W1Panel06-receipts/git-evidence.json`. All commands below ran against the detached clone; all returned exit 0.

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone rev-parse HEAD
2a32aa8228d5f86a85c81a923a3148bf792a9538
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone merge-base --is-ancestor ca75c2674645ab6bdadeecb8584007c74342bfa9 2a32aa8228d5f86a85c81a923a3148bf792a9538
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone merge-base --is-ancestor d33053f7552db4bd290c99a36979760f544c41ad 2a32aa8228d5f86a85c81a923a3148bf792a9538
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone merge-base --is-ancestor 870d9b987f14a046964018429662a238f2fe9e20 2a32aa8228d5f86a85c81a923a3148bf792a9538
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone merge-base --is-ancestor 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb 2a32aa8228d5f86a85c81a923a3148bf792a9538
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 150,150 -- corpus/SOURCES.md
99c3bc88 (tameshi-shokunin 2026-10-28 11:38:37 -0300 150) | S275 | Change-Aware Mutation Testing for Evolving Systems (Ojdanić et al.; ESEC/FSE 2022, camera-ready) — https://doi.org/10.1145/3540250.3558911 | paper | A | the per-commit reuse decision — which mutants a changed commit still needs — for F7 | §3.2–3.3 (commit-relevant and subsuming mutants), p. 3 (physical; printed footer 1787) @ author camera-ready https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf, fetched 2026-10-27 (HTTP 200, 131622 B, sha256 4d755c4e…) | a re-sweep cadence is a reuse decision, not a re-run of everything: selecting only subsuming commit-relevant mutants cut the mutants requiring analysis by around 93% on average | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md |
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 2,2 -- corpus/knowledge/change-aware-resweep-cadence.md
99c3bc88 (tameshi-shokunin 2026-10-28 11:38:37 -0300 2) source: S275 — https://doi.org/10.1145/3540250.3558911 — §3.2 (commit-relevant mutants) and §3.3 (subsuming, high-order mutations), p. 3 (physical) — author camera-ready (ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf), fetched 2026-10-27 by L1 TameshiR53a2 (round-53 assimilation; staged as S161 by corpus-expansion-1, re-pointed by document)
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 12,18 -- corpus/lessons/round-57.md
ca75c267 (tameshi-shokunin 2026-10-28 20:34:28 -0300 12) - **R53.8 — the round-53 lesson's quote word counts are wrong.** `corpus/lessons/round-53.md` line 23 calls the
ca75c267 (tameshi-shokunin 2026-10-28 20:34:28 -0300 13)   S275 quote "22 words" and lines 31-32 call the S276 quote "19 words". Counted with `python3 -c 'print(len(q.split()))'`
ca75c267 (tameshi-shokunin 2026-10-28 20:34:28 -0300 14)   on the two quoted strings as they appear in that lesson, S275 "by selecting only subsuming commit relevant mutants,
ca75c267 (tameshi-shokunin 2026-10-28 20:34:28 -0300 15)   we reduce the number of mutants requiring analysis by around 93% on average" is 20 words and S276 "re-compute
ca75c267 (tameshi-shokunin 2026-10-28 20:34:28 -0300 16)   mutant suites per release. Sadly, this makes mutation results inconsistent; mutant scores from each release
adf87899 (tameshi-shokunin 2026-10-28 21:52:43 -0300 17)   cannot be directly compared" is 20 words. Both are within the 25-word bound of fleet-root `CORPUS.md` rule 1 (a ≤25-word quote); the
ca75c267 (tameshi-shokunin 2026-10-28 20:34:28 -0300 18)   parentheticals in the round-53 lesson are superseded by this line.
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone show --format=fuller --stat d33053f7552db4bd290c99a36979760f544c41ad
commit d33053f7552db4bd290c99a36979760f544c41ad
Author:     tameshi-shokunin <tameshi@shokunin.local>
AuthorDate: Tue Oct 27 11:43:51 2026 -0300
Commit:     tameshi-shokunin <tameshi@shokunin.local>
CommitDate: Wed Oct 28 10:43:53 2026 -0300

    round-53: land wave receipts that were never committed

 .ufo/waves/round-53/w1-results.json             | 272 ++++++++++++++++++
 .ufo/waves/round-53/w1/T53W1ExecR523.md         | 350 ++++++++++++++++++++++
 .ufo/waves/round-53/w2-results.json             | 248 ++++++++++++++++
 .ufo/waves/round-53/w2/T53W2CritClaims.md       | 267 +++++++++++++++++
 .ufo/waves/round-53/w2/T53W2ExecR523B.md        | 367 ++++++++++++++++++++++++
 .ufo/waves/round-53/w2/T53W2RevW1Specialists.md |  77 +++++
 6 files changed, 1581 insertions(+)
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone ls-tree -r HEAD -- .ufo/waves/round-53/w1-results.json .ufo/waves/round-53/w2-results.json .ufo/waves/round-53/w1/T53W1ExecR523.md .ufo/waves/round-53/w2/T53W2CritClaims.md .ufo/waves/round-53/w2/T53W2ExecR523B.md .ufo/waves/round-53/w2/T53W2RevW1Specialists.md
100644 blob f279ac448fe4fd1037e1f81e561047f42c25d5e5	.ufo/waves/round-53/w1-results.json
100644 blob 8acb5f9d8cba761da6b08da34ce10c5a877131b8	.ufo/waves/round-53/w1/T53W1ExecR523.md
100644 blob 548a0ec07cdfc81801370ff1749a8e5153bc5e27	.ufo/waves/round-53/w2-results.json
100644 blob 2b66b5f5db5e37831b7c3b76617206870fa3057b	.ufo/waves/round-53/w2/T53W2CritClaims.md
100644 blob c74927d0d50bd036a05450c1a7f2d5557413f8e7	.ufo/waves/round-53/w2/T53W2ExecR523B.md
100644 blob 3e54c4c5e854ac6f8c4910fb134dbf3b1ebca889	.ufo/waves/round-53/w2/T53W2RevW1Specialists.md
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 146,153 -- .ufo/evidence/round-57/deciding-run.sh
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 146) for ab in a b; do
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 147)   A=$(git -C "$CL" show "$REV:$E/control/controls-$ab.stdout")
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 148)   printf '%s\n' "$A" | grep -Eq "^CONTROLS_${ab^^}: ([0-9]+)/\1 as pre-registered" || refuse "controls-$ab-verdict-missing"
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 149)   printf '%s\n' "$A" | grep -q 'CTL_MISMATCH' && refuse "controls-$ab-mismatch-lines"
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 150)   [ "$(git -C "$CL" show "$REV:$E/control/controls-$ab.exit" | tr -d '[:space:]')" = 0 ] || refuse "controls-$ab-exit-nonzero"
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 151)   want=$(git -C "$CL" show "$REV:$E/control/controls-$ab.stdout.sha256" | awk '{print $1; exit}')
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 152)   got=$(git -C "$CL" show "$REV:$E/control/controls-$ab.stdout" | sha256sum | awk '{print $1}')
870d9b98 (tameshi-shokunin 2026-10-28 23:41:57 -0300 153)   [ "$want" = "$got" ] || refuse "controls-$ab-digest-mismatch"
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 1589,1613 -- corpus/QUALITY.md
99c3bc88 (tameshi-shokunin 2026-10-28 11:38:37 -0300 1589) 
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 1590) Falsifier that must fail: the round-53 C1 counter's rekey arm prints `rekeyed=0/30` at its own final content revision `88afa941` (the pathspec `git ls-tree --name-only REV .ufo/evidence/round-21/coldread` returns the directory itself), while the round-54 counter's arm prints `rekeyed=7/7` at its deciding revision and `rekeyed=3/7` with `CTL_MISMATCH` on the control cloned at the freeze commit (the control never fired; [ER-R54-1]); the two receipts are `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout` (the round-53 counter's bytes run at `88afa941`) and `.ufo/evidence/round-54/control/controls-b.stdout` (the round-54 positive control); both are committed.
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1591) 
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1592) ### Criterion 106 — a pre-registered control is scored at the revision it certifies
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1593) 
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1594) A control that certifies a repair must be scored at the revision the repair is in.
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1595) Cloning the FREEZE commit (the bytes frozen before the work) and calling the result a
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1596) positive control measures the tree the round started from: it cannot fire, and its
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1597) "pass" is an assumption, not a measurement. The receipt must name the revision it
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1598) cloned and that revision must be the candidate under test; a gate that opens on a
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1599) control receipt must compare the receipt's own `rev=` with the revision it decides.
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1600) 
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1601) Falsifier that must fail: `.ufo/evidence/round-54/control/controls-b.stdout` — its
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1602) `CTL_POS_c1` line prints `C1_R54_PASS=false` at `rev=077d431e6996` (the freeze) with
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1603) `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`, while four round-54 records
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1604) claimed the control passed. Round 55's `controls.sh` phase B re-scores every control at
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1605) the revision it certifies, and its `deciding-run.sh` gate refuses a control receipt that
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1606) does not descend from the freeze.
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1607) 
4c04c1d3 (tameshi-shokunin 2026-10-28 14:51:26 -0300 1608) Erratum on criterion 105: 105's own falsifier quoted the same round-54 control
4c04c1d3 (tameshi-shokunin 2026-10-28 14:51:26 -0300 1609) as printing 7 of 7. Its receipt prints 3 of 7 and `CTL_MISMATCH`; the 7-of-7
4c04c1d3 (tameshi-shokunin 2026-10-28 14:51:26 -0300 1610) reading belongs to a re-score at the deciding revision. 105 stands (an arm is
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1611) proven on a tree where it must fire) and its example is corrected here rather than
51d1f0eb (tameshi-shokunin 2026-10-28 14:39:49 -0300 1612) deleted.
c0137451 (tameshi-shokunin 2026-10-28 16:18:15 -0300 1613) 
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 2563,2569 -- SCORECARD.md
3146479c (tameshi-shokunin 2026-10-28 11:45:34 -0300 2563) monitors and the deciding script in `.ufo/evidence/round-54/contract.json`,
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2564) frozen at `441c26be` before any seat ran; **amendment 1** (one follow-up commit, landed before the
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2565) controls ran) fixes
3146479c (tameshi-shokunin 2026-10-28 11:45:34 -0300 2566) one mechanical discovery bug in the C1 counter's re-key arm, found by the binder
3146479c (tameshi-shokunin 2026-10-28 11:45:34 -0300 2567) dry run before any control was scored and before any deciding invocation —
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2568) predicate, target and arms unchanged. The round has **one freeze pointer,
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2569) `077d431e`** (5 amendments), which the deciding run uses [ER-R54-2]. Base `d33053f7`; content commit C0 `59c38109`; fix-pass
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 2584,2585 -- SCORECARD.md
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2584) | C1 the seven base-lost cold-read sections are re-read at the content commit and bound, and the precheck reads 64/64: `C1_R54_PASS=true` | calibration (8; surface: the cold-read floor) | `credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 total=4` false (`.ufo/evidence/round-54/before/c1.stdout`); at C0 the round's own edits drift it to `credited=41 lost=23` | `total=0` | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 / CTL_R53 / CTL_FAB / CTL_LOGINPUT false; CTL_POS_c1 `CTL_MISMATCH` `2/3` at the revision it cloned (the freeze) and true only when re-scored at the deciding revision [ER-R54-1] (`.ufo/evidence/round-54/control/`) |
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2585) | C2 seven tools share one scratch-root exit class and say so: `C2_R54_PASS=true` | operability (no numeric score; surface: the scratch-root exit class) | `unusable_exit2=3 docs=0 note=0 sources=0 total=13` false (`.ufo/evidence/round-54/before/c2.stdout`; the `14`/`13` 'delta' the round-54 parenthetical claimed inverted the two [ER-R54-3]) | `total=0` | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 false, CTL_EXIT0 false, CTL_POS_c2 true (`.ufo/evidence/round-54/control/`) |
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 2631,2652 -- SCORECARD.md
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2631) **ER-R54-1 - a positive control reported as passing while its receipt says it did not.**
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2632) Old: `CTL_POS_c1 true` (round-54 claim row); `corpus/QUALITY.md` 105's falsifier
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2633) (`the round-54 counter's arm prints rekeyed=7/7 on its positive control`);
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2634) `corpus/lessons/round-54.md` (`proven live by the positive control (CTL_POS_c1,
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2635) which prints rekeyed=7/7)`).
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2636) Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B:
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2637) 2/3` at the revision the control cloned. The cause is mechanical: phase B cloned
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2638) the FREEZE commit, which predates the re-key, so the control could not fire.
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2639) Receipt: `.ufo/evidence/round-54/control/controls-b.stdout`. Round 55 re-scores
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2640) its own positive control at the revision it certifies (`controls.sh` phase B).
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2641) 
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2642) **ER-R54-2 - three freeze pointers for one round.**
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2643) Old: `7883e0e5` called "the freeze pointer the deciding run uses"; `fe70474d`
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2644) in the measured-close line; `097985c1` in the fleet report.
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2645) Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2646) receipt prints. Receipt: `.ufo/evidence/round-54/after/frozen.stdout`
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2647) (`freeze=077d431e...`).
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2648) 
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2649) **ER-R54-3 - a quoted total no receipt contains.**
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2650) Old: `total=14` in the C2 claim row. Corrected: `total=13`.
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2651) Receipt: `.ufo/evidence/round-54/before/c2.stdout` (and the contract's own
9cf0146b (tameshi-shokunin 2026-10-28 14:16:25 -0300 2652) `before` text).
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone show ca75c2674645ab6bdadeecb8584007c74342bfa9 -- corpus/lessons/round-57.md
commit ca75c2674645ab6bdadeecb8584007c74342bfa9
Author: tameshi-shokunin <tameshi@shokunin.local>
Date:   Wed Oct 28 20:34:28 2026 -0300

    round-57: C0 content - receipt-gate registry rows and fixtures (R56.6), SKILL standing-rules/registry truth (R56.2), recheck errata and index (R56.3), cold-read referent record (R56.4), corrections R53.8 R55.2 R56.7, S283-S285, QUALITY, cold-read forecast tool

diff --git a/corpus/lessons/round-57.md b/corpus/lessons/round-57.md
new file mode 100644
index 00000000..9f377f7d
--- /dev/null
+++ b/corpus/lessons/round-57.md
@@ -0,0 +1,30 @@
+# tameshi round 57 — lesson (hyaku run 11, 2026-10-28)
+
+L1 `TameshiR57`, attempt 1. Base `5e3569969b532310d2b8a3d130901757a3df356b`; contract
+`.ufo/evidence/round-57/contract.json`. This file is written in sections as the round lands; the sections
+after `## Corrections to earlier records` are completed from committed receipts at the round's close.
+
+## Corrections to earlier records
+
+Append-only corrections (CORPUS.md: corrections are new entries, never rewrites). Each names the routed item it
+answers; the ledger rows `R53.8`, `R55.2` in `corpus/routed-defects.json` point here.
+
+- **R53.8 — the round-53 lesson's quote word counts are wrong.** `corpus/lessons/round-53.md` line 23 calls the
+  S275 quote "22 words" and lines 31-32 call the S276 quote "19 words". Counted with `python3 -c 'print(len(q.split()))'`
+  on the two quoted strings as they appear in that lesson, S275 "by selecting only subsuming commit relevant mutants,
+  we reduce the number of mutants requiring analysis by around 93% on average" is 20 words and S276 "re-compute
+  mutant suites per release. Sadly, this makes mutation results inconsistent; mutant scores from each release
+  cannot be directly compared" is 20 words. Both are within the 25-word bound of CORPUS.md SOURCES rule 1; the
+  parentheticals in the round-53 lesson are superseded by this line.
+- **R55.2 — a quoted C2 total the receipt contradicts.** The round-55 report quotes the C2 counter run on
+  `T55W1ScribeSkill` as `grammar=9/9 … note=9/9 skill=1/1 total=0`. The committed receipt
+  `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` line 44 reads
+  `C2_R55: rev=08d64e946006 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false`;
+  the quoted `total=0` is not a quote of that line. The correct statement of that run is `total=1`, verdict false, at
+  `rev=08d64e946006`. The report is fleet-side and is not edited by the lane; this line is the superseding record.
+- **R56.7 — "no byte changed after C0/PIN" is true of PIN→tip, not of C0→PIN.** `corpus/lessons/round-56.md`
+  lines 318-319 say no `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `tools/` or ledger
+  byte changed after C0/PIN. `git diff --stat c0137451f5b7 877eedee3ddb -- corpus SKILL.md tools` shows
+  `corpus/QUALITY.md` +31, `corpus/SOURCES.md` +2 and `corpus/knowledge/receipt-revision-binding.md` +39 between C0
+  and the bind input commit `877eedee`; the sentence holds for the interval from the pinned bind revision to the
+  round's final tip. This line supersedes the sentence; the round-56 lesson is not rewritten.
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone show 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- SCORECARD.md corpus/lessons/round-54.md
commit 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
Author: tameshi-shokunin <tameshi@shokunin.local>
Date:   Wed Oct 28 14:16:25 2026 -0300

    round-55: C0 — one scratch-root line in three tools (repeat-control, context-capture, registry-check now raise ScratchRootUnusable and print the frozen grammar on stderr), seven registry cells, the note's one-line section (nine allocating modes), SKILL.md scratch rule, the round-54 record corrections (ten routed defects, old->new, worktree-polluted values fixed), QUALITY 106 + 105 erratum, lessons round-55 (+ round-54 wording), LOG, S001 rows S280, wave-1 spec/dispatch

diff --git a/SCORECARD.md b/SCORECARD.md
index 6f5f95a3..54faed38 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -2561,11 +2561,12 @@ incomplete; the round reports the miss, not a narrowed target.
 L1 TameshiR54a2, hyaku run 11, attempt 2. Two claims on distinct axes,
 pre-registered with both counters, the controls harness, the 14 no-harm
 monitors and the deciding script in `.ufo/evidence/round-54/contract.json`,
-frozen at `441c26be` before any seat ran; **amendment 1** (`7883e0e5`) fixes
+frozen at `441c26be` before any seat ran; **amendment 1** (one follow-up commit, landed before the
+controls ran) fixes
 one mechanical discovery bug in the C1 counter's re-key arm, found by the binder
 dry run before any control was scored and before any deciding invocation —
-predicate, target and arms unchanged, and `7883e0e5` is the freeze pointer the
-deciding run uses. Base `d33053f7`; content commit C0 `59c38109`; fix-pass
+predicate, target and arms unchanged. The round has **one freeze pointer,
+`077d431e`** (5 amendments), which the deciding run uses [ER-R54-2]. Base `d33053f7`; content commit C0 `59c38109`; fix-pass
 commit C1 `99c3bc88`. Round shape: one v2 wave of 76 seats (band 64–128) plus
 one v1 wave of 47 seats (band 32–64) = 123 seats. Calibration (8) is the lowest
 non-retired axis and carries C1.
@@ -2580,8 +2581,8 @@ non-retired axis and carries C1.
 
 | Claim | Axis | Before (base `d33053f7`) | Target | Counting command | Controls (freeze bytes) |
 |---|---|---|---|---|---|
-| C1 the seven base-lost cold-read sections are re-read at the content commit and bound, and the precheck reads 64/64: `C1_R54_PASS=true` | calibration (8; surface: the cold-read floor) | `credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 total=4` false (`.ufo/evidence/round-54/before/c1.stdout`); at C0 the round's own edits drift it to `credited=41 lost=23` | `total=0` | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 / CTL_R53 / CTL_FAB / CTL_LOGINPUT false, CTL_POS_c1 true (`.ufo/evidence/round-54/control/`) |
-| C2 seven tools share one scratch-root exit class and say so: `C2_R54_PASS=true` | operability (no numeric score; surface: the scratch-root exit class) | `unusable_exit2=3 docs=0 note=0 sources=0 total=14` false (`.ufo/evidence/round-54/before/c2.stdout`; the contract's before text quotes the pre-freeze smoke run `total=13`, the recorded receipt is quoted here and the delta disclosed) | `total=0` | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 false, CTL_EXIT0 false, CTL_POS_c2 true (`.ufo/evidence/round-54/control/`) |
+| C1 the seven base-lost cold-read sections are re-read at the content commit and bound, and the precheck reads 64/64: `C1_R54_PASS=true` | calibration (8; surface: the cold-read floor) | `credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 total=4` false (`.ufo/evidence/round-54/before/c1.stdout`); at C0 the round's own edits drift it to `credited=41 lost=23` | `total=0` | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 / CTL_R53 / CTL_FAB / CTL_LOGINPUT false; CTL_POS_c1 `CTL_MISMATCH` `2/3` at the revision it cloned (the freeze) and true only when re-scored at the deciding revision [ER-R54-1] (`.ufo/evidence/round-54/control/`) |
+| C2 seven tools share one scratch-root exit class and say so: `C2_R54_PASS=true` | operability (no numeric score; surface: the scratch-root exit class) | `unusable_exit2=3 docs=0 note=0 sources=0 total=13` false (`.ufo/evidence/round-54/before/c2.stdout`; the `14`/`13` 'delta' the round-54 parenthetical claimed inverted the two [ER-R54-3]) | `total=0` | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 false, CTL_EXIT0 false, CTL_POS_c2 true (`.ufo/evidence/round-54/control/`) |
 
 The after values are read from the deciding receipts under
 `.ufo/evidence/round-54/after/`, never from this table (a deciding line that
@@ -2605,7 +2606,7 @@ only; carried from round 53: the service-limits §5 U1 heading re-read.
 ### Round 54 — measured close (appended after the deciding invocation)
 
 One deciding invocation at the post-re-key revision (`.ufo/evidence/round-54/after/`),
-freeze `fe70474d` (amendments 1-5), `FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c`, no-harm 14 ok / 0 RED,
+freeze `077d431e` (amendments 1-5) — one pointer for the round [ER-R54-2] — `FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c`, no-harm 14 ok / 0 RED,
 census exit 0.
 
 - **C1** `C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true` — **verifies**.
@@ -2616,3 +2617,86 @@ census exit 0.
 Numeric axes: calibration unchanged at 8 (the floor moved from 57/64 at base to the credited count in the C1 line above);
 depth 10 and freshness 9 unchanged. Capabilities: none claimed this round.
 
+
+## Round 55 - round-54 record corrections
+
+The round-54 non-author spot-check (`corpus/lessons/round-54-verifier-spotcheck.md`)
+routed ten record defects. This section carries each correction in one place: the
+old text (preserved here as the erratum), the corrected value, and the receipt
+that decides it. The same corrections were applied in place above so that the
+lane's record reads true where a reader meets it; this section is the only place
+where the old values are quoted, which is why the round-55 counter
+(`.ufo/evidence/round-55/c1/measure.py`) counts every stale token outside it.
+
+**ER-R54-1 - a positive control reported as passing while its receipt says it did not.**
+Old: `CTL_POS_c1 true` (round-54 claim row); `corpus/QUALITY.md` 105's falsifier
+(`the round-54 counter's arm prints rekeyed=7/7 on its positive control`);
+`corpus/lessons/round-54.md` (`proven live by the positive control (CTL_POS_c1,
+which prints rekeyed=7/7)`).
+Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B:
+2/3` at the revision the control cloned. The cause is mechanical: phase B cloned
+the FREEZE commit, which predates the re-key, so the control could not fire.
+Receipt: `.ufo/evidence/round-54/control/controls-b.stdout`. Round 55 re-scores
+its own positive control at the revision it certifies (`controls.sh` phase B).
+
+**ER-R54-2 - three freeze pointers for one round.**
+Old: `7883e0e5` called "the freeze pointer the deciding run uses"; `fe70474d`
+in the measured-close line; `097985c1` in the fleet report.
+Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding
+receipt prints. Receipt: `.ufo/evidence/round-54/after/frozen.stdout`
+(`freeze=077d431e...`).
+
+**ER-R54-3 - a quoted total no receipt contains.**
+Old: `total=14` in the C2 claim row. Corrected: `total=13`.
+Receipt: `.ufo/evidence/round-54/before/c2.stdout` (and the contract's own
+`before` text).
+
+**ER-R54-4 - a stale counter digest.**
+Old: `49280fe5` for `c2/measure.py`. Corrected: `8528ee85` - the amendment-4
+bytes that decided. Receipt: `.ufo/evidence/round-54/freeze.json`, key
+`c2/measure.py`.
+
+**ER-R54-5 - finding counts that do not match the committed readers.**
+Old: 25 wave-1 findings; 22 wave-2 findings in 9 sections. Corrected (re-derived
+over the committed reader files, `-receipts/` JSON excluded): `w1=28 w2=25 sections=12`
+- 28 findings across 23 wave-1 reader reports, 25 across 12 of the 23 wave-2
+reports. Command: `git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/w1`
+then a `findings` length sum per file (the round-55 c1 counter does exactly this
+at every revision).
+
+**ER-R54-6 - round work uncommitted at closure.**
+Old: three seat deliverables untracked when the round filed.
+Corrected: they are committed; the sweep that committed them is `ff2a821`.
+Receipts: `.ufo/waves/round-54/w2/T54W2Sent03.md` and
+`.ufo/waves/round-54/w2/T54W2Sent03-receipts/{c1committed-positive.stdout,rejection-attribution.txt}`.
+
+**ER-R54-7 - an imprecise forged-file disposition.**
+Old: "the deletion lands in 7fa9a5e0". Corrected: the file was **renamed** into
+`.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e`
+(`R100`); it still sits in the tree as the incident receipt. It can never
+credit: its path fails the reader pattern and its `section_sha256` matches no
+section at the content commit.
+
+**ER-R54-8 - a half-recorded host-write incident, and a characterisation that
+was itself wrong.**
+Old: the report named the incident; the lesson did not, and the seat file still
+asserted an operator instruction. Corrected in two steps. The incident is now
+recorded in `corpus/lessons/round-55.md` and
+`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` is marked superseded. The
+round-54 report's characterisation ("fabricated") is ALSO withdrawn: the operator
+turn exists in `~/.omp/agent/history.db` (row 690, 2026-10-28T15:12:15Z) and
+reached the seat 5 m 33 s after it yielded; the write to `config.yml` was wrong
+because the file is operator-owned and the seat had stopped serving, not because
+the turn was invented, and the file now reads `scout: "@m_grok"` again.
+
+**ER-R54-9 - wave-table numbers and the staged-package count.**
+Old: 4 reviewers (report), a 26.3 % attack share, "the other 84 staged entries".
+Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from
+`.ufo/waves/round-54/w1-registry.json`, and `staged=81` staged `.md` files under
+`merge/tameshi/knowledge` (read-only count of the source package).
+
+**ER-R54-10 - a quote under the wrong receipt.**
+Old: `CTL_R53 (58/64, rekeyed=0/30)` cited to `control/controls-a.stdout`.
+Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7`; the
+`rekeyed=0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`, the
+round-53 counter's own bytes run at the round-53 final revision.
diff --git a/corpus/lessons/round-54.md b/corpus/lessons/round-54.md
index 8aa2c029..0c435a42 100644
--- a/corpus/lessons/round-54.md
+++ b/corpus/lessons/round-54.md
@@ -48,7 +48,7 @@ Rejects (this round's set):
   round's centre of gravity is the C1 floor repair plus the C2 exit class. Flip:
   it is the next-ranked entry for round 55 (its subject, a stated minimality
   witness, matches the round-50 shrinker's `cannot_see` line).
-- **The other 84 staged `merge/tameshi` entries** — REFUSED for the same capacity
+- **The other 80 staged `merge/tameshi` entries** — REFUSED for the same capacity
   reason; they stay reserved by document.
 
 Assimilation verdict: one theme (the scratch-root contract) with three rows and
@@ -71,9 +71,11 @@ line rather than acted on; proposals 2–5 remain unmined (at most one per round
   counter had no arm-level self-test, and the round-53 control scored the
   do-nothing tree (which fails for other reasons), so a dead arm looked
   healthy. fix: this round's counter lists the re-key directory with
-  `git ls-tree -r` and proves the arm on the positive control CTL_POS_c1, which
-  requires `rekeyed=7/7`; the control receipts are committed before the deciding
-  run (`.ufo/evidence/round-54/control/`).
+  `git ls-tree -r` and the arm's own count is read at the deciding revision
+  (7 of 7); the control pre-registered in phase B was cloned at the freeze
+  commit, printed `CTL_MISMATCH` (3 of 7) and therefore never fired
+  [ER-R54-1, round-55 correction]; the control receipts are committed under
+  `.ufo/evidence/round-54/control/`.
 
 ## QUALITY criterion (drafted; lands with the round commit)
 
@@ -97,8 +99,10 @@ pin only artifacts those edits did not touch, and the deciding run re-derives
 
 - **R53.1** (the frozen round-53 C1 counter's rekey arm was dead) — FIXED: this
   round's counter lists the re-key directory with `git ls-tree -r` (a recursive
-  listing, so the directory's own name cannot shadow the match), and the arm is
-  proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`).
+  listing, so the directory's own name cannot shadow the match), and the arm
+  reads 7 of 7 at the deciding revision; the control
+  pre-registered in phase B was cloned at the freeze commit and printed
+  `CTL_MISMATCH` (3 of 7), so it never fired [ER-R54-1, round-55 correction].
   The dead arm's own receipt is kept:
   `.ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout`
   (`rekeyed=0/30` at the round-53 final revision). QUALITY 105 lands with it.
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone show 99c3bc88d704566197783f66b211ee0a830e0330 -- corpus/SOURCES.md corpus/knowledge/change-aware-resweep-cadence.md
commit 99c3bc88d704566197783f66b211ee0a830e0330
Author: tameshi-shokunin <tameshi@shokunin.local>
Date:   Wed Oct 28 11:38:37 2026 -0300

    round-54: C1 fix pass — 26 wave-1 reader findings adjudicated and fixed (stale SKILL anchors at C0, the C** placeholder, exit-arm drift after the scratch-root change, the runbook pin, S275 page locator, the env-diff run-path class), QUALITY 105

diff --git a/corpus/SOURCES.md b/corpus/SOURCES.md
index 66b5dfc5..2c3c86f3 100644
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -147,7 +147,7 @@ rows only, and a row is a claim opened in the round that writes it.
 | S272 | kagi `corpus/drift-pins.sh` (fleet gate, read-only) — kagi-shokunin/corpus/drift-pins.sh | code | A | the gate's own verdict vocabulary, exit map and hermetic scratch-tree selftest at the measured revision | :19 (exit map), :118-259 (verify), :374-446 (selftest), :400-405 (the exit-and-grep assertion) @ e64e81b8eb96f3682b00c1e7a291e84420b280fa (blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb, 451 lines, mode 100755; unchanged at kagi HEAD 69b61db46be4ed955994f6f1d1cba522bc5f4e97) | a host-drift gate anchors on committed baselines instead of live fingerprints and proves each verdict class in a scratch tree; its 13-case `--selftest` prints `DRIFT_SELFTEST: PASS (13 cases)` and asserts exit code plus an unanchored `grep -q` for the verdict word, not its position in the output | mined | 2026-10-26 | 180d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
 | S273 | GNU Bash Reference Manual, The Set Builtin (author copy of the manual, Edition 5.3, last updated 18 May 2025) — https://tiswww.case.edu/php/chet/bash/bashref.html (the gnu.org node page https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html was unreachable on 2026-10-27 UTC: eight attempts, HTTP 000, 0 bytes, connect timeouts — https and http, with and without www, IPv4-forced, and the single-page manual alike) | docs | A | Bash `errexit` (`-e`) and `pipefail`: which failing commands end a non-interactive shell, the listed non-exits, and a pipeline's return value | §The Set Builtin `-e` item (single-page copy lines 6547-6570) and `pipefail` item (lines 6706-6710); same text in the Savannah texi pinned by S097 at `@item -e` lines 5929-5948 and `@item pipefail` lines 6062-6066 (re-fetched 2026-10-27, sha256 f3d37d57, byte-identical to S097); a command of assignments only takes its status at §Simple Commands lines 3675-3677 (copy lines 4172-4173) @ author copy fetched 2026-10-27T00:22Z UTC, two fetches byte-identical (1040870 bytes; SHA-256 b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4), snapshot .ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html | Quotes (each at most 25 words), `-e`: "Exit immediately if a pipeline ... returns a non-zero status"; non-exits: "The shell does not exit if the command that fails is ... any command in a pipeline but the last"; the parenthetical tying that to pipefail: "any command in a pipeline but the last (subject to the state of the pipefail shell option)"; `pipefail`: "the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status"; assignments-only status: "the exit status of the last command substitution performed" | mined | 2026-10-26 | 365d | corpus/knowledge/mutation-case-kagi-drift-pins.md |
 | S274 | Hermeticity (Bazel Documentation) — https://bazel.build/basics/hermeticity | docs | A | what a hermetic build or test asserts: isolation from the host and identity of every declared input; used here as the contrast class for a fleet-bound self-test | §Overview and §Identifying non-hermeticity @ https://bazel.build/basics/hermeticity.md fetched 2026-10-27 (HTTP 200, 5878 B, sha256 2355150f…; re-fetched by a second seat, same sha) | a test is hermetic only when every input it reads is declared and independent of the host; a self-test that reads sibling repos at a fixed fleet root has an undeclared host input | mined | 2026-10-27 | 180d | corpus/lessons/round-52.md |
-| S275 | Change-Aware Mutation Testing for Evolving Systems (Ojdanić et al.; ESEC/FSE 2022, camera-ready) — https://doi.org/10.1145/3540250.3558911 | paper | A | the per-commit reuse decision — which mutants a changed commit still needs — for F7 | §3.2–3.3 (commit-relevant and subsuming mutants), p. 4 @ author camera-ready https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf, fetched 2026-10-27 (HTTP 200, 131622 B, sha256 4d755c4e…) | a re-sweep cadence is a reuse decision, not a re-run of everything: selecting only subsuming commit-relevant mutants cut the mutants requiring analysis by around 93% on average | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md |
+| S275 | Change-Aware Mutation Testing for Evolving Systems (Ojdanić et al.; ESEC/FSE 2022, camera-ready) — https://doi.org/10.1145/3540250.3558911 | paper | A | the per-commit reuse decision — which mutants a changed commit still needs — for F7 | §3.2–3.3 (commit-relevant and subsuming mutants), p. 3 (physical; printed footer 1787) @ author camera-ready https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf, fetched 2026-10-27 (HTTP 200, 131622 B, sha256 4d755c4e…) | a re-sweep cadence is a reuse decision, not a re-run of everything: selecting only subsuming commit-relevant mutants cut the mutants requiring analysis by around 93% on average | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md |
 | S276 | Keeping Mutation Test Suites Consistent and Relevant with Long-Standing Mutants (Ojdanić, Papadakis, Harman; arXiv 2212.11762) — https://arxiv.org/abs/2212.11762 | paper | A | whether a re-computed mutant suite can be compared with the previous one, for F7 | §Abstract @ arXiv:2212.11762v1 (submitted 2022-12-22), fetched 2026-10-27 (HTTP 200, 41423 B, sha256 d6dc4cf6…) | re-computing the mutant suite per release makes scores incomparable — 52% of 143,500 mutants degrade in relevance — so a pinned long-standing suite is the consistency device | mined | 2026-10-27 | 365d | corpus/knowledge/change-aware-resweep-cadence.md |
 | S277 | POSIX.1-2024, Base Definitions §8.1 Environment Variables (TMPDIR) — https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html | spec | A | TMPDIR's standard definition | §8.1 TMPDIR paragraph @ fetched 2026-10-28 (sha256 89294048...) | TMPDIR "shall represent a pathname of a directory made available for programs that need a place to create temporary files"; the standard fixes the variable's meaning, not its empty-string handling | mined | 2026-10-28 | 730d | corpus/knowledge/scratch-root-contract.md |
 | S278 | CPython 3.12.7 Lib/tempfile.py, `_candidate_tempdir_list` — https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py | code | A | the reference resolver's own TMPDIR search | `_candidate_tempdir_list` :163-165 @ v3.12.7 (sha256 fb44155f...) | `for envname in 'TMPDIR', 'TEMP', 'TMP': dirname = _os.getenv(envname); if dirname: dirlist.append(dirname)` — an empty value is skipped, so empty behaves as unset and the next candidate wins | mined | 2026-10-28 | on-release | corpus/knowledge/scratch-root-contract.md |
diff --git a/corpus/knowledge/change-aware-resweep-cadence.md b/corpus/knowledge/change-aware-resweep-cadence.md
index 7a4b628d..abdd66b5 100644
--- a/corpus/knowledge/change-aware-resweep-cadence.md
+++ b/corpus/knowledge/change-aware-resweep-cadence.md
@@ -1,5 +1,5 @@
 ---
-source: S275 — https://doi.org/10.1145/3540250.3558911 — §3.2 (commit-relevant mutants) and §3.3 (subsuming, high-order mutations), p. 4 — author camera-ready (ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf), fetched 2026-10-27 by L1 TameshiR53a2 (round-53 assimilation; staged as S161 by corpus-expansion-1, re-pointed by document)
+source: S275 — https://doi.org/10.1145/3540250.3558911 — §3.2 (commit-relevant mutants) and §3.3 (subsuming, high-order mutations), p. 3 (physical) — author camera-ready (ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf), fetched 2026-10-27 by L1 TameshiR53a2 (round-53 assimilation; staged as S161 by corpus-expansion-1, re-pointed by document)
 source: S276 — https://arxiv.org/abs/2212.11762 — §Abstract — arXiv:2212.11762v1 (submitted 2022-12-22), fetched 2026-10-27 by L1 TameshiR53a2
 verified-at: 2026-10-27 (both sources re-opened this round; snapshots under `.ufo/evidence/round-53/assimilation/`)
 recheck: 365d
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 1,7 -- .ufo/evidence/round-54/control/controls-b.stdout
7fa9a5e0 (tameshi-shokunin 2026-10-28 12:21:35 -0300 1) CTL CTL_POS_c1 C1_R54: rev=077d431e6996 c0=99c3bc88d704 credited=60 lost=4 rekeyed=3/7 readers=6/7 monitor=6/60 unstable=0 total=4 C1_R54_PASS=false
7fa9a5e0 (tameshi-shokunin 2026-10-28 12:21:35 -0300 2) CTL_MISMATCH CTL_POS_c1 expected=true actual=false
7fa9a5e0 (tameshi-shokunin 2026-10-28 12:21:35 -0300 3) CTL CTL_POS_c2 C2_R54: rev=077d431e6996 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
7fa9a5e0 (tameshi-shokunin 2026-10-28 12:21:35 -0300 4) CTL CTL_EXIT0 C2_R54: rev=7df0e0426c98 tools=7 unusable_exit2=6 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
7fa9a5e0 (tameshi-shokunin 2026-10-28 12:21:35 -0300 5) CONTROLS_B: 2/3 as pre-registered
55649546 (tameshi-shokunin 2026-10-28 12:22:02 -0300 6) 
55649546 (tameshi-shokunin 2026-10-28 12:22:02 -0300 7) # receipt re-stated at the round-54 freeze 077d431e (bytes unchanged; the verdict line above stands)
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 8,8 -- .ufo/evidence/round-54/before/c2.stdout
19c75588 (tameshi-shokunin 2026-10-28 11:51:50 -0300 8) C2_R54: rev=d33053f7552d tools=7 unusable_exit2=3 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=0 note=0 sources=0 total=13 C2_R54_PASS=false
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 1,1 -- .ufo/evidence/round-54/after/frozen.stdout
4fe57df5 (tameshi-shokunin 2026-10-28 12:25:49 -0300 1) FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c
[exit 0]
```

```text
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel06/clone blame -L 119,124 -- .ufo/evidence/round-55/controls.sh
631cd645 (tameshi-shokunin 2026-10-28 13:24:31 -0300 119) if [ "$PHASE" = b ]; then
631cd645 (tameshi-shokunin 2026-10-28 13:24:31 -0300 120)   # CTL_POS -- the real repair AT THE REVISION IT CERTIFIES must pass both counters.
631cd645 (tameshi-shokunin 2026-10-28 13:24:31 -0300 121)   d=$(clone_at "$LANE" "$REV" pos) || exit 2
631cd645 (tameshi-shokunin 2026-10-28 13:24:31 -0300 122)   mkwork wposa; score "$C1" "$d" cposa wposa >/dev/null; v=$(verdict "$SCR/cposa.out" C1_R55_PASS)
631cd645 (tameshi-shokunin 2026-10-28 13:24:31 -0300 123)   echo "CTL CTL_POS_c1 $(tail -1 "$SCR/cposa.out")"; check CTL_POS_c1 true "$v"
631cd645 (tameshi-shokunin 2026-10-28 13:24:31 -0300 124)   mkwork wposb; score "$C2" "$d" cposb wposb >/dev/null; v=$(verdict "$SCR/cposb.out" C2_R55_PASS)
[exit 0]
```

## Self-evaluation

Accuracy 4/5: exact patches and ancestor checks support each verdict; no live end-to-end gate run was made. Completeness 4/5: all five compound items addressed; fleet archived report correction relies on explicit lane supersession. Clarity 4/5: per-item reasons precede the long audit transcript. Actionability 5/5: exact machine verdicts and command receipts delivered. Conciseness 4/5: transcript duplication is retained for reproducibility. Overall 4.2/5. Improvements: independently replay the current gate if runtime assurance is requested; retain archived-report supersession as an explicit limitation. The user can distinguish observed content from unexercised behavior.
