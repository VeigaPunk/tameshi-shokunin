# FinalRevision — critique of measuring at a85f710 vs 4b7c682 vs 7243e7f

Seat: critic (advisory). Scope: ONLY the three-revision measurement attack for the
five routed round-18 defects. No production edits. Grounded in
`corpus/lessons/round-18-verifier-spotcheck.md` §5 and the named blobs.

## Verdict

The three-revision ladder is **unsound as designed**. Four of five defects are
byte-identical at all three revisions, and the fifth (R18-5) cannot be evaluated
by lane-blob existence at any of the three. The scheme adds a non-discriminating
column (a85f710) that can only inject `could-not-evaluate` noise into a count
that must end `corrected=5, failed=0`.

## Counterexample and evidence

All commands run read-only in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

1. **R18-1/R18-2/R18-3: identical blobs at all three revisions.**
   `git rev-parse <rev>:<path>` for `corpus/knowledge/guard-kill-closure.md`,
   `corpus/knowledge/mutation-case-kumitate-sources-check.md`,
   `corpus/lessons/round-18.md` → `9f9b60bf…`, `ea61d7fa…`, `b1991bb8…`
   respectively at a85f710, 4b7c682, AND 7243e7f. Line 2 still reads
   `Landed-tip results: PENDING (filled by L1 after landing)`; line 1 still calls
   S008 `queued`; line 79 still says `deletions = the four allowed used-by cells
   only`. There is no "before" state inside this ladder: every defect already
   exists at the earliest named revision. Measuring at a85f710 yields no
   gradient and invites an instrument to emit could-not-evaluate where a blob
   read still succeeds — contaminating the population count without evidence.

2. **R18-4: identical blob too.** `.ufo/evidence/round-18/final/checks.json` is
   blob `d8c98a92fd71cf0c…` at all three revisions; the `bash-witness-selftest`
   row records argv `[python3, tools/bash-witness-study.py, --selftest]`,
   revision `921ef80…`, `exit: 64`, stdout_sha256 `e3b0c44…` (empty) — the
   mis-invocation the verifier routed. First committed at `5923d89`, ancestor of
   all three. Same non-discrimination as (1).

3. **R18-5: the one column that differs is the wrong dimension.**
   `git show a85f710:.ufo/evidence/round-18/final/measure-final-60.json` →
   `fatal: path … exists on disk, but not in 'a85f710'`. The receipt first
   appears in `4b7c682` (diff a85f710..4b7c682 adds exactly
   `measure-final-60.json` +1978, `census-end.txt`, LOG, SCORECARD) and names
   `"revision": "a85f7107c4167cd9968248722256fcaf617fc30c"`. So at a85f710 the
   instrument sees ABSENT; at 4b7c682/7243e7f it sees a receipt bound to
   a85f710. An existence-based predicate would read a85f710 as
   `could-not-evaluate` (contract.json already records `2 could-not-evaluate`
   [INFERENCE: this is one of them]) — and worse, no committed file can ever
   "exist at" the revision it measures without rewriting history, so
   `exists-at-rev` is unsatisfiable as a fix criterion. The defective half of
   R18-5 lives outside the lane tree entirely: the report sentence
   "the same no-override count at final `4b7c682…` returned **60/60,8**, exit0"
   is `.ufo/reports/round-18/tameshi.md` line 53 in the **fleet** repo
   (`/home/vgpnk/Projects/shokunin`, report commit `a85e4d87`), unreachable by
   any lane-blob scan.

4. **4b7c682 vs 7243e7f differ by exactly one file.** `git diff --stat
   4b7c682 7243e7f` → only `corpus/lessons/round-18-verifier-spotcheck.md`
   (+225). For defect predicates the two revisions are interchangeable; the only
   correct roles are baseline=7243e7f (frozen, per contract) and
   4b7c682-as-cited-revision (the rev R18-5's sentence cites).

## Hidden regression risk (beyond the attack itself)

Re-running `measure.py` at a *new* revision is not guaranteed to reproduce
60/60: 7243e7f and any delivered revision D add corpus files (the verifier
lesson, round-19 corrections) that can shift `sections_total`/coverage. The
verifier's remedy "land one at the cited revision" is satisfiable precisely
because the tool pins blobs by `--rev`: a receipt with `.revision` ==
`4b7c6823a462f5ea2eafcb262275300a545f3ed7` measures the frozen inputs and can
be committed at D. A predicate requiring the receipt file inside the 4b7c682
tree is impossible; a predicate re-measuring at D is measurement-surface drift
disguised as a fix.

## Falsifier (failure-capable audit must expose)

- Run the audit against frozen baseline `7243e7f`: it MUST report all 5 items
  defective / corrected=0. If baseline reads corrected>0 for any item, the
  predicate is measuring labels, not defects.
- Doctored-fix negative: an in-place edit that deletes `PENDING` from
  guard-kill-closure.md:2 or rewrites round-18.md:79 MUST FAIL acceptance —
  invariant `historical bytes retained` plus verifier remedies are
  "appended correction naming that line" (§5.1) and "State five, or name S008"
  (§5.3). A predicate that only checks the defective string is gone both
  false-passes on byte removal and false-fails the append-only remedy.
- R18-5 negative: a receipt whose `.revision` field ≠ the cited revision, or a
  receipt path present in the tree but bound to a different rev, MUST FAIL.
  (Current committed state already demonstrates this: `measure-final-60.json`
  exists at 7243e7f but binds a85f710 — baseline must not count it as a fix.)

## Minimal defensible acceptance

Two endpoints only: frozen baseline `7243e7f` (expected: 5 defective) and
delivered lane revision `D` (expected: corrected=5, failed=0). a85f710 enters
only as the *bound revision inside* the R18-5 receipt — a data field, never a
measurement endpoint.

- **R18-1**: at D, `guard-kill-closure.md` line 2 bytes unchanged AND a dated
  appended erratum/correction naming the `verified-at`/`Landed-tip results`
  line with the landed-tip numbers (per verifier §5.1 wording).
- **R18-2**: at D, EITHER the S008-`queued` mention swept to `mined` OR an
  appended correction naming it (verifier allows both); `corpus/SOURCES.md`
  S008 row still `mined` with this entry as used-by.
- **R18-3**: at D, line-79 arithmetic corrected to five OR an appended erratum
  stating five and naming S008's status+used-by line; `git diff --numstat
  183f87b D -- corpus/SOURCES.md` deletions still = 5.
- **R18-4**: at D, the exit-64 row bytes retained (not deleted) AND a new final
  receipt artifact/row carries the real `WITNESS_SELFTEST: 43/43` tally bound to
  an exact revision; the failed invocation labeled mis-invocation.
- **R18-5**: at D, a committed receipt JSON with `.revision` (and `rev_input`)
  == `4b7c6823a462f5ea2eafcb262275300a545f3ed7` (or the exact revision the
  claim is re-scoped to) PLUS a lane-side erratum naming the fleet report
  sentence (`.ufo/reports/round-18/tameshi.md` @ `a85e4d87`), since the lane
  cannot write the fleet tree.
- Acceptance wrapper: fails on any item unreadable (`could-not-evaluate` →
  failed), requires corrected=5 AND failed=0, and prints per-item
  baseline/delivered verdicts so a silent skip cannot masquerade as a pass.

## Impacted axes

- calibration (C1): the claim fails if the count is contaminated by
  could-not-evaluate at a non-baseline revision.
- discernment: three-revision grading asserts a before/after gradient that does
  not exist; keeping it would be a provenance defect of the same class being
  repaired.
- quality: exists-at-rev predicates encode the same
  "receipt-bound-to-wrong-revision" error as R18-5 itself.

## Smallest safe correction to the attack

Drop a85f710 as an endpoint; keep exactly two measurement points
(7243e7f baseline, delivered D). Express R18-5 as a two-part predicate:
(receipt `.revision` field == cited rev AND erratum names the fleet sentence).
For R18-1..R18-4 require defective-bytes-retained + named-correction-present at
D. That is fixable inside the round; anything stricter (receipt inside the
measured tree) is unsatisfiable and the canonical judge must reject it.

No installs; no lane selftests/gates run; evidence above is `git show`/`rev-parse`/
`diff`/`cat-file`/`rev-list` read-only output quoted at stated revisions.
