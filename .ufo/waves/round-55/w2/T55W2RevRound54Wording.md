# T55W2RevRound54Wording — `corpus/lessons/round-54.md` at C0, against its own receipts

Seat T55W2RevRound54Wording (reviewer, wave 2 / falsify). Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; content commit
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0); C0's parent and the round's freeze
`e2979f277138da503af27b263b783f626f109be4`; wave base `0a2010acd1e92e4e332774050825e21bcfc7e079`.
All reads are `git show`/`ls-tree`/`log` at those revisions — the lane worktree is dirty
with peers' in-flight wave-2 files, so nothing here is read from the worktree except the
read-only census (recorded as such).

The target file did not change between the wave base and the freeze, so "base" below is
exact:

```
$ git rev-parse 0a2010ac:corpus/lessons/round-54.md e2979f27:corpus/lessons/round-54.md 9cf0146b:corpus/lessons/round-54.md
8aa2c029089ceae630a7c84e8182c783d9bc6dbf
8aa2c029089ceae630a7c84e8182c783d9bc6dbf
0c435a42f3c5a31495fbd8b83ce31a0412a87726
```

Receipts: `T55W2RevRound54Wording-receipts/` (`sweep.stdout` is the whole driver run,
`sweep.stderr` empty except one fixed heredoc bug I corrected in `staged-count.sh`;
`staged-count.stdout` is the package reconciliation; `census-validate.*`,
`sources-row-count.stdout`, both driver scripts copied in below). Driver:
`T55W2RevRound54Wording-receipts/driver.sh`, `T55W2RevRound54Wording-receipts/staged-count.sh`
(read-only: `git show`, `git log`, `ls-tree`, `os.walk` on the read-only package).

Artifacts opened at C0: `corpus/lessons/round-54.md`; `corpus/lessons/round-53.md`;
`corpus/lessons/round-53-verifier-spotcheck.md`; `corpus/lessons/round-55.md`;
`SCORECARD.md` (round-54 block, measured close, `## Round 55 - round-54 record corrections`);
`corpus/QUALITY.md` (105 at C0 and at `99c3bc88`); `corpus/SOURCES.md`;
`corpus/knowledge/scratch-root-contract.md`; `corpus/knowledge/change-aware-resweep-cadence.md`;
`considerthese/2026-10-28.md`, `considerthese/2026-10-19.md`;
`.ufo/evidence/round-54/{after/{c1.stdout,c1.start,c2.stdout,frozen.stdout,deciding-run.exit},before/c2.stdout,control/{controls-a.stdout,controls-b.stdout,controls-b.exit,r53-counter-at-88afa941.stdout,controls.sh},c1/measure.py path only,freeze.json,deciding-run.sh,assimilation/{S277-posix-env.html,S278-tempfile.py,S279-tempfile-docs.html}}`;
`.ufo/waves/round-54/w1/T54W1ExecCensus-receipts/08-lesson-quote-wordcounts.txt`;
read-only package `/home/vgpnk/Projects/shokuknow/merge/tameshi/{MERGE-REPORT.json,MERGE-REPORT.md,knowledge/**,amendments/**}`.

## The three edits C0 made to this file (exact hunks)

```
$ git -C LANE diff e2979f27 9cf0146b -- corpus/lessons/round-54.md
@@ -48,7 +48,7 @@  ... Rejects (this round's set)
-- **The other 84 staged `merge/tameshi` entries** — REFUSED for the same capacity
+- **The other 80 staged `merge/tameshi` entries** — REFUSED for the same capacity
@@ -71,9 +71,11 @@ ... Mistakes
-  `git ls-tree -r` and proves the arm on the positive control CTL_POS_c1, which
-  requires `rekeyed=7/7`; the control receipts are committed before the deciding
-  run (`.ufo/evidence/round-54/control/`).
+  `git ls-tree -r` and the arm's own count is read at the deciding revision
+  (7 of 7); the control pre-registered in phase B was cloned at the freeze
+  commit, printed `CTL_MISMATCH` (3 of 7) and therefore never fired
+  [ER-R54-1, round-55 correction]; the control receipts are committed under
+  `.ufo/evidence/round-54/control/`.
@@ -97,8 +99,10 @@ ... Round-53 routed defects — dispositions
-  listing, so the directory's own name cannot shadow the match), and the arm is
-  proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`).
+  listing, so the directory's own name cannot shadow the match), and the arm
+  reads 7 of 7 at the deciding revision; the control
+  pre-registered in phase B was cloned at the freeze commit and printed
+  `CTL_MISMATCH` (3 of 7), so it never fired [ER-R54-1, round-55 correction].
```

Line numbers at C0: edit 1 = L51; edit 2 = L72–78 (the new sentence L74–77);
edit 3 = L100–105 (the new sentence L102–105).

**Correction to the item's own framing:** the third hunk is the **R53.1 disposition
bullet**, not "the R53.9 area" — the R53.9 bullet (L133–135) is byte-identical to base.
The file's three edits are: staged count, the R53.1 fix paragraph in `## Mistakes`,
and the R53.1 disposition bullet. I reviewed each.

## Edit 2 and edit 3 (the R53.1 rewrites): new sentences agree with the receipts

Receipts, verbatim:

```
$ git -C LANE show 9cf0146b:.ufo/evidence/round-54/control/controls-b.stdout
CTL CTL_POS_c1 C1_R54: rev=077d431e6996 c0=99c3bc88d704 credited=60 lost=4 rekeyed=3/7 readers=6/7 monitor=6/60 unstable=0 total=4 C1_R54_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false
...
CONTROLS_B: 2/3 as pre-registered

$ git -C LANE show 9cf0146b:.ufo/evidence/round-54/after/c1.stdout
C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true

$ git -C LANE show 9cf0146b:.ufo/evidence/round-54/after/frozen.stdout
FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c
```

- "the arm's own count is read at the deciding revision (7 of 7)" — **true**:
  `rekeyed=7/7` is on the deciding line at `rev=c21081008adb`, which is the revision
  `after/frozen.stdout` names. `EXPLAIN arm3-rekey dirs=['rekey-r54-99c3bc88d704']
  c0=99c3bc88d704…` shows the arm reading the re-key directory itself.
- "the control … was cloned at the freeze commit" — **true**: the control's `rev=` is
  `077d431e6996`, the freeze pointer in `frozen.stdout`, and `controls.sh` phase B
  clones exactly the REV it is given.
- "printed `CTL_MISMATCH` (3 of 7)" — **true**, with a one-line bookkeeping note: the
  `3 of 7` is on the `CTL CTL_POS_c1` line immediately above `CTL_MISMATCH`; the
  mismatch line itself prints only `expected=true actual=false`. SCORECARD's claim row
  quotes the *other* receipt number for the same event (`CTL_MISMATCH` `2/3` = the
  CONTROLS_B tally), so the lesson's `(3 of 7)` and SCORECARD's `2/3` are two different
  quantities, both receipt-backed. Not a contradiction, but they read as one.
- "never fired" — supported in the only sense the receipt can support: the control was
  pre-registered `expected=true` (`controls.sh`: `check CTL_POS_c1 true "$v"`) and
  printed `actual=false`, so it never produced its pre-registered verdict.

**Verdict: both rewrites are factually right and both name their receipt
(`[ER-R54-1, round-55 correction]`, `.ufo/evidence/round-54/control/`).**

### Did dropping `rekeyed=7/7` / "positive control" lose information a reader needs?

Token census, base vs C0:

```
$ git -C LANE show e2979f27:corpus/lessons/round-54.md | grep -nE "positive control|rekeyed=7/7|CTL_POS_c1"
74:  `git ls-tree -r` and proves the arm on the positive control CTL_POS_c1, which
75:  requires `rekeyed=7/7`; the control receipts are committed before the deciding
81:  where the arm must fire (the positive control), not only on the do-nothing
101:  proven live by the positive control (`CTL_POS_c1`, which prints `rekeyed=7/7`).
$ git -C LANE show 9cf0146b:corpus/lessons/round-54.md | grep -nE "positive control|rekeyed=7/7|CTL_POS_c1|7 of 7"
75:  (7 of 7); the control pre-registered in phase B was cloned at the freeze
83:  where the arm must fire (the positive control), not only on the do-nothing
103:  reads 7 of 7 at the deciding revision; the control
```

What went and what a reader still gets:

- `rekeyed=7/7` → **no loss**: the same number is stated twice in prose ("7 of 7" at
  L74–75 and L103). The literal `rekeyed=` prefix survives in the same file at L67 and
  L108 (`rekeyed=0/30`).
- "positive control" → **no loss inside the file**: the phrase survives at L83 in the
  same file's QUALITY 105 block ("proven on a tree where the arm must fire (the
  positive control)"). What the *paragraph* lost is the control's role sentence —
  "proves the arm on the positive control … requires `rekeyed=7/7`" — so a reader of
  only this bullet must infer that the control's expectation was 7/7. It is one hop
  away: `controls.sh` (`check CTL_POS_c1 true "$v"`) and ER-R54-1.
- `CTL_POS_c1` → **the only real loss**: the control's identifier is gone from the file.
  `controls-b.stdout` carries three `CTL` lines, so a reader verifying "the control
  pre-registered in phase B" must match the sentence to the `CTL_POS_c1` line by
  content rather than by name. Recoverable in one hop from the receipt the sentence
  cites.
- **Residual wording hazard (worth one edit):** "…and therefore never fired" (L76–77)
  and "…so it never fired" (L105) leave the pronoun's subject unstated, and the arm
  *did* fire — 3 of 7. A reader who takes "it" for the arm reads the opposite of what
  happened. The disambiguating clause ("the control … was cloned at the freeze commit")
  is two clauses earlier, and the *cause* of the mismatch (the clone predates the
  completed re-key) lives only in ER-R54-1. Suggested repair: "the pre-registered
  positive control (`CTL_POS_c1`, expected true) printed `CTL_MISMATCH`: the arm read
  3 of 7 on the pre-re-key freeze clone it ran against, so the control never proved the
  arm live; the deciding run's own reading is 7 of 7."

## Edit 1 (the staged count, 84 → 80): FALSE — the edit introduced the error it meant to fix

Both the package manifest and the lane's own two neighbours count **entries**, and they
disagree with 80:

```
$ bash staged-count.sh          # T55W2RevRound54Wording-receipts/staged-count.stdout
MERGE-REPORT.json: entries = 86 | accepted(rows) = 103 | refused(rows) = [] | first_id = S153
entry kinds = {'new-file': 81, 'amendment': 4, 'folded-into-canonical': 1}
*.md under merge/tameshi/knowledge (recursive) = 81
*.md under merge/tameshi (recursive, all) = 87
round-53 adopted entry on disk (change-aware-resweep-cadence.md): True
round-54 named-rejected entry on disk (delta-debugging-minimization-contract.md): True
amendment entries = 4 | any amendment target present among knowledge/ files? False
folded-into-canonical entries = 1
```

- MERGE-REPORT.md line 7: `- proposed knowledge entries: **86**`.
- Round-53's lesson, L54: `- **The other 85 staged `merge/tameshi` entries** —
  REJECTED this round` — i.e. 86 entries, round 53 adopted **one**
  (`change-aware-resweep-cadence.md`, which cites S275/S276), leaving 85.
- SCORECARD, `**Planned (round 54):**` (L2534–2536): `the 85 unadopted
  `merge/tameshi` entries (next: `r8-predictive-test-selection-cost.md`,
  `delta-debugging-minimization-contract.md`)`.

Round 54 adopted **none** of the package and named exactly one as the next-ranked
refusal (`delta-debugging-minimization-contract.md`). 85 unadopted − 1 named = **84** —
the pre-edit text. The post-edit **80** is `81 − 1`: it counts `.md` files under
`merge/tameshi/knowledge`, which (a) includes the entry round 53 already adopted, and
(b) excludes the 4 `amendment` entries (their payloads sit under `amendments/`, not
`knowledge/`) and the 1 `folded-into-canonical` entry. `80` is a real file count of the
wrong set (it is 81 files minus the named one, not the "other staged entries"). Even on
the file convention the sentence does not close: the 81 files include the entry round 53
adopted, so "the other 80 … REFUSED" counts an already-adopted entry as a round-54
refusal, and the unadopted new-file subset would be 79, not 80.

ER-R54-9, which moved the number, states the file count correctly — "`staged=81`
staged `.md` files under `merge/tameshi/knowledge` (read-only count of the source
package)" — but the lesson turned that file count into an *entry* count and subtracted
the named entry, so the correction propagated a category error into the sentence.

**Verdict: edit 1 is false as written. Correct value: 84** ("the other 84 staged
`merge/tameshi` entries"), or the sentence may be restated in the file-count unit:
"81 staged `.md` payload files plus 4 amendments (86 entries), all refused this round".
The number is load-bearing only as a record claim, but it is exactly the class of claim
this wave exists to falsify.

## Remaining falsehoods the round did not touch

### F2 (medium) — R53.5 says "no amendment is recorded"; the round recorded five

```
$ git -C LANE show 9cf0146b:corpus/lessons/round-54.md | sed -n '/R53.5/,+3p'
- **R53.5** (stale freeze receipts) — FIXED: `freeze.json` is regenerated at
  freeze time and the deciding run prints `FROZEN_UNCHANGED=1` against it; no
  amendment is recorded.

$ for r in 441c26b 077d431; do printf '%s amendments=' "$r"; git -C LANE show $r:.ufo/evidence/round-54/freeze.json | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["amendments"]))'; done
441c26b amendments=0
077d431 amendments=5

$ git -C LANE log --format='%h %ad %s' --date=iso -- .ufo/evidence/round-54/freeze.json
077d431 2026-10-28 12:05:19 -0300 round-54: amendment 5 — …
fe70474 2026-10-28 12:05:19 -0300 round-54: amendment 4 — …
4e2de73 2026-10-28 12:00:39 -0300 round-54: amendment 3 — …
097985c 2026-10-28 11:52:14 -0300 round-54: freeze-digest gate …
19c7558 2026-10-28 11:51:50 -0300 round-54: re-freeze (amendment 2, …)
7883e0e 2026-10-28 11:44:51 -0300 round-54: amendment 1 — C1 arm 3 …
441c26b 2026-10-28 11:19:07 -0300 round-54: claim contract, both counters, …
```

`after/frozen.stdout` prints `freeze=077d431e…`, i.e. the amendment-5 commit, and the
same round's corrected SCORECARD block says it in one sentence: "The round has **one
freeze pointer, `077d431e`** (5 amendments), which the deciding run uses [ER-R54-2]"
(SCORECARD L2568–2570, and again at L2645). The lesson's R53.5 bullet is therefore the
one surviving statement in the round's record that the freeze was never amended.
Related, same bullet: the lesson's Gate (L5–6) still says "Claims frozen at `441c26be`
(`.ufo/evidence/round-54/contract.json`, `freeze.json`), before any seat ran"; at
`441c26be` both files hold the pre-amendment bytes (0 amendments; amendment 2 re-hashed
all 11 contract paths), so the pointer a reader takes from the lesson is not the one the
deciding run verified. ER-R54-2 corrected three other pointers and left this one; it is
the same defect class it claims to have closed.

### F3 (medium) — the Gate's word counts contradict the round's own committed census receipt, and the routed count clause was marked FIXED without a fix

```
$ git -C LANE show 9cf0146b:.ufo/waves/round-54/w1/T54W1ExecCensus-receipts/08-lesson-quote-wordcounts.txt
== lesson Gate word counts (contract rule 1 requires <=25) ==
S277: quote='TMPDIR This variable shall represent a pathname of a directory made available for programs that need a place to create temporary files' tokens=22 lesson_claims=21 match=False within_25=True
S278: quote='if dirname: dirlist.append(dirname)' tokens=3 lesson_claims=5 match=False within_25=True
S279: quote='The directory named by the TMPDIR environment variable' tokens=8 lesson_claims=11 match=False within_25=True
```

Lesson at C0: L20 `(21 words, §8.1 TMPDIR paragraph)`, L27 `(5 words, :163-165)`,
L34 `(11 words, §tempfile.gettempdir)`. Each number is reproducible only under its own
convention: 21 = 22 whitespace tokens minus the `TMPDIR` label; 5 = the code line split
on punctuation (`if dirname dirlist append dirname`); 11 = the *containing* sentence
`'The list is: The directory named by the TMPDIR environment variable.'` (my count: 11
whitespace tokens), not the 8-token fragment printed in the lesson. No single convention
yields all three, and the round's own receipt recorded `match=False` on all three. This
is also the clause round 53 routed and round 54 marked FIXED:
`corpus/lessons/round-53-verifier-spotcheck.md` defect 8 — "Gate word-count
parentheticals are off by 1–2 words. Correct the page cell in SOURCES.md and the
knowledge entry." The disposition (lesson L127–132) addresses only the page cell.

### F4 (medium) — the Gate's considerthese attribution names the wrong file and the wrong proposal

```
$ git -C LANE show 9cf0146b:corpus/lessons/round-54.md | sed -n '57,60p'
considerthese mining: `considerthese/2026-10-28.md` proposal 1 (the contract-debt
table: which SCORECARD contract sections are placeholders and for how long) is
mined into this round's SCORECARD `planned` line and the report's stale-lane
line rather than acted on; proposals 2–5 remain unmined (at most one per round).

$ git -C LANE show 9cf0146b:considerthese/2026-10-28.md | sed -n '/## Self-improvement ideas/,$p' | head -6
1. **Receipt-existence linter for records.** For every SCORECARD, LOG and lesson sentence that cites an evidence path in the
   past tense, check that the path exists at the cited revision and that the quoted counter line matches the committed
   stdout byte for byte. …

$ grep -rn -i "contract-debt|placeholders" LANE/considerthese/
considerthese/2026-10-19.md:34:1. **Contract-debt tracker.** Each run, read `SCORECARD.md` and flag contract sections still left as placeholders
```

The 2026-10-28 file's proposal 1 is the receipt-existence linter; the contract-debt
tracker is proposal 1 of `considerthese/2026-10-19.md`. A reader following the pointer
lands on a different proposal, and the record no longer says which idea was actually
carried into the Planned line (SCORECARD's `Planned (round 54)` does leave
"considerthese proposals 2–5", consistent with "proposal 1 mined", so the *counting*
holds while the *content* and the *file* do not).

### F5 (low) — the QUALITY 105 block in the lesson is narrower than the criterion that landed

Lesson L82–86 (drafted): "A counter arm that reads a directory **by pathspec** …
Falsifier: a control receipt in which the arm's own counter **reads zero** (the arm
never fired) …". The criterion that actually landed at `99c3bc88` reads (QUALITY.md
L1586): "A counter arm that reads a directory, **a revision or a manifest** … The check
that can fail: a positive-control receipt in which the arm's own counter reads zero,
**or a control run that pre-registers the arm's value without a tree that carries it**."

```
$ git -C LANE log --oneline -S "pre-registers the arm's value without a tree that carries it" -- corpus/QUALITY.md
99c3bc8 round-54: C1 fix pass — … QUALITY 105
```

The missing clause is exactly ER-R54-1's shape: the round-54 control pre-registered the
arm's value on a tree that did not carry it and read 3 of 7 — non-zero, so the lesson's
drafted falsifier ("reads zero") would not have fired on the round's own evidence. The
block is honest about being a draft ("drafted; lands with the round commit"), but it is
the only statement of 105 in the lesson, and a reader of the lesson alone gets the
weaker check.

### F7 (verification gap, not a finding) — the Gate's "text-extracted" byte counts have no committed artifact

Lesson: S277 "33758 B text-extracted", S279 "20462 B text-extracted". The committed
snapshots are 52350 B and 75190 B; a plain tag-strip of them yields 33756 and
19349–19412 depending on `<style>`/`<script>` handling — so the S277 figure is
plausibly the same recipe (±2 B of whitespace normalisation) and the S279 figure is
only reachable with the L1's own extractor, which is not committed. Not falsified, not
checkable: a gap, recorded rather than counted.

## The sweep that found nothing (the same file, checked against receipts)

- **Edit 2/3 numbers**: `rekeyed=7/7` at `rev=c21081008adb` (`after/c1.stdout`),
  `CTL_MISMATCH … expected=true actual=false` with `rekeyed=3/7` at `rev=077d431e6996`
  (`control/controls-b.stdout`), control receipts committed
  (`5564954 … control receipts re-stated at the freeze commit`), deciding run opened
  `2026-10-28T15:23:33Z` (`after/c1.start`) after that commit. Both citations hold.
- **R53.1 dead-arm receipt**: `control/r53-counter-at-88afa941.stdout` prints
  `rekeyed=0/30` at `rev=88afa9415454` and `PROBLEM rekey-dir-count=0` — the lesson's
  `(rekeyed=0/30 at the round-53 final revision)` is exact.
- **R53.2/R53.3**: `after/` is fully populated (8 files) and `deciding-run.sh` L49–58
  refuses a deciding run unless all four control receipts are non-empty blobs at REV
  and both `CONTROLS_A/B … as pre-registered` verdict lines are present. Holds.
- **R53.6**: `before/c2.stdout` shows the four tools at `rc=1` with a `RuntimeError`
  traceback (`env-diff`, `bash-witness-study`, `evidence-disposition`,
  `pin-disposition`) and `unusable_exit2=3`; `after/c2.stdout` shows those four at
  `rc=2` with a `could-not-evaluate` naming line and `unusable_exit2=7`. "four of
  seven" and "7/7" both hold.
- **R53.7**: `integrate/binder.py:166` writes a `rev_reason` naming read rev and PIN;
  `rekey-r54-99c3bc88d704/refresh-receipts.json` exists in the tree. Holds.
- **R53.8 (page half)**: `corpus/SOURCES.md` S275 anchor cell is `p. 3 (physical;
  printed footer 1787)` and
  `corpus/knowledge/change-aware-resweep-cadence.md` carries `p. 3 (physical)`.
- **R53.9**: all six round-53 wave files are tracked at base —
  `w1-results.json`, `w2-results.json`, `T53W1ExecR523.md`, `T53W2CritClaims.md`,
  `T53W2ExecR523B.md`, `T53W2RevW1Specialists.md` all `TRACKED-at-base`.
- **Gate snapshot identity**: the lesson's sha prefixes resolve —
  `89294048…`, `fb44155f…`, `6b0edccf…` are the sha256 of the three committed
  snapshots; S278's `:163-165` window contains `if dirname: dirlist.append(dirname)`
  on line 165; both long quotes are present in the committed HTML snapshots.
- **Note claim (L37–42)**: `corpus/knowledge/scratch-root-contract.md` L9 (three arms),
  L26–29 ("the standard fixes only the variable's meaning… The empty arm is therefore a
  lane declaration that follows the resolver the lane actually calls"). Holds.
- **The method line (L93–96)**: deciding line reads `credited=64 lost=0` from the
  committed tree. Holds.

## Not checked (named, so the sweep is bounded)

- L3–4 ("attempt 1 left nothing behind … nothing inherited"): no attempt-1 artifact
  exists to test; unfalsifiable from the tree.
- L17–18 / L31–32 (HTTP 200 and fetch provenance of S277–S279): the snapshots are
  committed, the HTTP status was not re-fetched (no network use in this seat).
- L100–132 dispositions R53.2–R53.7 beyond the receipt-level checks above (e.g.
  whether *every* revision a receipt names resolves — I spot-checked the four the
  receipts print: `d33053f7552d`, `c21081008adb`, `077d431e6996`, `88afa9415454`).

## Environment

No tool installs were needed (nothing newer than the stock `git`, `python3`, `gawk`
was required; pacman is paused host-wide and was not used). Scratch
`/fast/scratch/hyaku/tameshi-r55/T55W2RevRound54Wording` held only the two driver
scripts (copied into `-receipts/`) and was removed. No lane production file, no frozen
file and no wave spec was written; the only writes are this file and
`T55W2RevRound54Wording-receipts/`. Census at C0: `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tameshi` → `rc=0`, last line `tameshi ok …/corpus/SOURCES.md`,
`corpus/SOURCES.md` at C0 carries 140 `| Sxxx` rows.

## Findings, by severity

1. **HIGH — `corpus/lessons/round-54.md:51` (edit 1) is false.** "The other 80 staged
   `merge/tameshi` entries" should be **84**: the package declares 86 entries
   (`MERGE-REPORT.json`; 81 `new-file` + 4 `amendment` + 1 `folded-into-canonical`),
   round 53 adopted one, round 54 adopted none and named one, so 85 − 1 = 84. The
   correction used `staged=81`, a count of `.md` files under `merge/tameshi/knowledge`,
   and that set includes the round-53 adopted entry and excludes the 4 amendments and
   the folded entry. Receipt: `-receipts/staged-count.stdout`. The pre-edit text was
   right; the C0 edit is the regression.
2. **MEDIUM — `round-54.md:118–120`**: "no amendment is recorded" is contradicted by
   the round's own `freeze.json` (5 amendments at `077d431e`, 0 at `441c26be`), by the
   six commits that touch it, and by SCORECARD's "(5 amendments) — one pointer for the
   round". Same defect class as ER-R54-2, which left this pointer uncorrected (the Gate
   line still names `441c26be` for `freeze.json`).
3. **MEDIUM — `round-54.md:20,27,34`**: the Gate word counts (21/5/11) do not match the
   round's committed census receipt (`tokens=22/3/8`, `match=False` three times); each
   number needs a different counting convention, and the routed clause (R53.8) is
   marked FIXED without a correction.
4. **MEDIUM — `round-54.md:57–60`**: the mined proposal is attributed to
   `considerthese/2026-10-28.md` proposal 1, but that proposal is the receipt-existence
   linter; the contract-debt tracker is `considerthese/2026-10-19.md` proposal 1.
5. **LOW — `round-54.md:74–77,102–105`**: the rewrites are true against the receipts and
   lose no unrecoverable fact, but they drop `CTL_POS_c1` and the word "positive", and
   "never fired" has no stated subject while the arm did fire (3 of 7); the cause now
   lives only in ER-R54-1. One-clause repair suggested above.
6. **LOW — `round-54.md:82–86`**: the lesson's QUALITY 105 draft states a narrower
   falsifier than the criterion that landed at `99c3bc88`; the omitted clause is the
   one that catches ER-R54-1's shape.
7. **GAP — `round-54.md:17,31`**: the "text-extracted" byte counts have no committed
   extraction artifact; not falsified, not checkable.
