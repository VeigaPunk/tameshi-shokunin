# K06Calibration8: can calibration legitimately go 6 → 8 in round 17?

Seat: critic (leaf, read-only). Lane tip read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`.
Scratch: `/tmp/tameshi-r17w1-K06Calibration8-zhoi9c` (held committed copies of `SKILL.md`, the r16 `measure.py` and the r16 `ledger.json`; removed after the review).
No lane file was edited and no tool was installed.

## Short answer

The lane cap of 8 is still valid. The round-16 overclaim falsified the
**claim**, not the **rubric**. The rubric (SCORECARD.md:67) is "two points per
correctly restrained, durable-evidence-linked promotion assertion (`[~]`),
capped at 8; the remaining 2 require independent promotion review of all
boxes". Boxes 1, 2 and 4 already earn 6. Their links resolve to
`reports/round-1-calibration.md` `## box-1` :71, `## box-2` :105 and `## box-4` :167.
The +2 is box 3 only.

Round 17 can legitimately reach 8 only if the conditions below hold **at one
measured commit and at the branch tip**. Even then, the 8 is a lane
measurement and the non-author closure decides it (SCORECARD.md:573-576;
spot-check §3). AXES.md:34-36 adds a hard coupling: if any axis is harmed,
the round is not admitted. So 8 is unreachable unless C2 operability also
holds. The C2 repairs edit `tools/evidence-disposition.py`,
`tools/mutate-and-run.sh` and `tools/pin-disposition.py`, and those edits are
what make most of the existing cold-read credit go stale (see F3).

## Evidence

| Fact | Command | Observed |
|---|---|---|
| Page at tip | `git show 98bea7d:SKILL.md \| sha256sum` | `906fb649…1397`. 54 buckets under the r16 sectionizer: 24 instruction, 30 record by the credited entry's class. |
| Closure sectionizer agrees today | grep for `^#{4,6} ` and for `~~~` / indented fences in SKILL.md@98bea7d | 0 / 0 / 0. The lane's `#{1,3}` + backtick sectionizer and the closure's `#–######` + `~~~` sectionizer give the same buckets. This holds only while these counts stay 0. |
| r16 credit is page-agnostic | ledger@98bea7d, entries whose `skill_sha256 == 906fb649` | **1 of 75**. The other 53 credited buckets are credited by reads taken on older page versions (`97cf436b`, `3d8a1edb`, `e289acec`) because the section sha matches. |
| Aggregation is any-credit | r16 `measure.py` `coldread()`, synthetic run in scratch | `[executed-ok, wrong-expectation]` gives covered 1/1, `full=True`. `[wrong-expectation, executed-ok]` gives 1/1, `True`. `[wrong-expectation]` alone gives 0/1. A later failing re-read does **not** uncover a bucket that has one credited entry (`measure.py:244-256`, `break` on the first credit). |
| Bucket cites into tools that round 17 edits | regex over SKILL.md@98bea7d | `tools/mutate-and-run.sh:72-109` (buckets :921 record and :933 instruction), `:511-518` (:1164 record), `:733-791` (:1212 record), `:85-89` and `:115-119` (:1302 record). Round 17 adds a repo-identity guard to this file (C2). |
| Round-14 recipe still states the pre-r16 outcomes | `git show 98bea7d:SKILL.md \| sed -n 1563,1600p` | Steps 2-3 still run `--root . --dispositions .ufo/evidence/round-14/dispositions{-before,}.json` with the outcomes "must fail producer_before" and "only repair is that row's supersession". |
| The round-14 gate's live red | `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt` | `exit=2 expected_input_digest_mismatch tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…`. Contract A keeps v1 byte-identical, so the round-14 manifests return 2 at `--root .` **permanently**. |
| strace path form | `cd sub; strace -f -qq -y -e trace=openat cat ../link/f` (strace 7.2) | The argument is `"../link/f"`, which is relative and goes through a symlink. `-y` adds the resolved fd path `3</tmp/…/real/f>`. |
| Box-3 block parse | r16 `measure.py:137-155` `shonen_boxes` | The block is the box line plus contiguous **indented, non-blank** continuation lines. `box3_link` is a plain substring test on that block (`measure.py:286`). |
| Draft recipe uses an override | `.ufo/waves/round-17/w1/W03SkillR17Draft.md`, recipe step 7 | `measure.py --rev <tip> --ledger-file .ufo/evidence/round-17/coldread/ledger.json` |

## Conditions that must all hold for a legitimate 8

1. **One page, fully re-read after the last surface change.** Fix the final
   SKILL.md sha before the re-read. That sha must already include the R16-C2a
   repair and every new round-17 section (W03 adds about 4 headings). Every
   bucket at that sha needs a **v2** entry with `skill_sha256` equal to it.
   Credit carried from round-16 v1 entries keyed only by section sha must not
   count. This is the same as `inputs-unrecorded` for every executed v1
   entry, so it also holds for record entries with commands; all 54 r16
   credited entries have `commands_executed_count > 0`.
2. **The re-read runs after the L1 installs the staged instruments.** Run it
   at a rev at or after the install commit for `tools/evidence-disposition.py`
   v2, `tools/mutate-and-run.sh` (guard), `tools/pin-disposition.py`,
   `tools/registry*.{py,json}` and the SHONEN box-3 append. After the re-read,
   no lane file listed in any entry's `inputs` may change, up to and including
   the commit that records the claim (see F5).
3. **The R16-C2a repair is in the bucket itself.** The SKILL.md :1563-1596
   text must stop saying that the round-14 manifests produce
   producer_before / clean at `--root .`. Mark steps 2-3 historical, scope them
   to the archived root, and name the working round-17 v2 invocation. That
   invocation must return exit 0 clean (11 effective + 1 superseded), and the
   before manifest must return exit 1 failed. An appended corrective section
   alone does not fix it: the old bucket would still carry a wrong expectation.
   The re-read of this bucket must trace inputs that include
   `tools/evidence-disposition.py`, both round-17 manifests,
   `.ufo/evidence/round-13/expected.json` and its pinned inputs.
4. **Every input is verified at REV and the inputs are complete.** For every
   executed entry, `inputs` is a superset of the union of its committed trace
   receipts, and the shas are equal. Each receipt path in `traces` must exist
   at REV. "Non-empty" alone is not enough (F1).
5. **Current failures veto.** If an entry at the bucket's current sha has
   every input still verifying at REV and records `wrong_expectations > 0`,
   `blocking_gaps > 0` or a FAIL verdict, the bucket is uncovered. The
   any-credit rule must not survive into v2 (F2).
6. **The red-before is shown on the round-14 bucket.** Run v2 `measure.py`
   with `--ledger-file` set to the r16 ledger and `--inputs-overlay` recording
   CR26's runner `75ed934d`. The result must report
   `input-drift:tools/mutate-and-run.sh` on `## Effective expectation
   reconciliation — round 14`, with box3 false and restraint 6. This is
   R16-C2b's stated acceptance.
7. **The claimed number uses no overrides.** The 8 comes from
   `python3 .ufo/evidence/round-17/measure.py --rev REV` with the ledger
   committed at REV (no `--ledger-file`, `--ledger-rev` or `--inputs-overlay`),
   and the same command at the final branch tip also gives 8. W03's recipe
   step 7 must drop `--ledger-file` from the counting form.
8. **The box-3 text is corrected by an append and is itself restrained.**
   - The new line is an **indented, non-blank** continuation directly under
     the box-3 line, so `shonen_boxes` includes it.
   - It says that the round-16 full-page assertion failed on the round-14
     bucket and cites `corpus/lessons/round-16-verifier-spotcheck.md` §2.
   - It names `.ufo/evidence/round-17/coldread/ledger.json` and the v2
     `measure.py`.
   - It scopes the claim to lane inputs verified at the measured rev.
     External/sibling inputs and git-ref-dependent outcomes are reported, not
     keyed.
   - It keeps "lane-dispatched seats, no independent promotion verifier".
   - Command C still reads `boxes=4 checked=0 asserted=4 untouched=0`.
9. **Operability holds.** `registry-check.py --rev REV` reports held M/M.
   Every registry row whose `source` is a SKILL.md heading also appears in
   that bucket's v2 entry, as an executed command with the same exit. A row
   must not "hold" by registering a failure that the bucket text describes as
   a success (for example a round-14 `--root .` row with `expect.exit: 2`
   while the bucket says clean).
10. **The sectionizers still agree.** SKILL.md at REV has no `####`+ headings
    and no `~~~` fences. Otherwise the closure's independent sectionizer gives
    a different bucket count, and the claim cannot be re-derived from the
    closure side.

## Failure modes (how it fails again)

- **F1. Self-pinning inputs (strongest counterexample).** Contract C credits
  an executed entry if `inputs` is non-empty and every listed blob matches at
  REV. Nothing checks that the list is *complete*. An entry with
  `inputs: {"SHONEN.md": <sha>}`, or any file that does not drift, credits
  forever while the tool it actually ran changes. This is the r16 hole again,
  just one level up.
  *Smallest correction:* the measure loads each `traces` receipt from the
  blob at REV and requires `receipt.inputs ⊆ entry.inputs` with equal shas,
  and `len(traces) ≥ 1` (ideally `== commands_executed_count`). A missing
  receipt gives the reason `trace-missing:<path>`.
- **F2. Disagreement resolves to credit.** This is demonstrated above with r16
  code: one credited entry hides any number of failing entries at the same
  sha. The closure's line "a re-read at 09ee1d0 would leave it uncovered" is
  therefore **false under the lane's own measure**: CR26's credit would still
  have covered it. If v2 keeps "v1 output" aggregation, a wave-2 seat that
  finds a wrong expectation cannot flip the number.
  *Correction:* condition 5 (veto by input-current failures; failures whose
  inputs drifted are treated as stale).
- **F3. Round 17 makes its own credit stale, as round 16 did.** The C2 edits
  touch `mutate-and-run.sh`, which is cited by line range in 5 buckets (4 of
  them record class), and `evidence-disposition.py`, which runs in the
  round-14 and round-15 buckets. The guard insertion very likely shifts
  `:72-109`, `:85-89`, `:115-119`, `:511-518` and `:733-791` [INFERENCE: the
  staged diff was not read]. If those record buckets are credited with an
  entry that did not list the runner in `inputs`, they stay credited while
  wrong. Seats must put every lane file they opened *by hand* to check a
  record into `inputs`, not only traced files.
- **F4. Trace under-capture.**
  - (a) strace prints the *argument* path (relative and through symlinks).
    In the fleet-mirror layout, siblings are reached through
    `/tmp/…/fleet/<sibling>` symlinks. A helper that filters on "under
    /home" without `-y` or realpath drops every sibling read, and
    mis-resolves relative opens after `chdir`. Use `strace -y` (verified
    above) or track per-pid cwd.
  - (b) Reads through git objects (`git show REV:…`, `cat-file`) are excluded
    with `.git/`. Fixed 40-hex revs are safe. Outcomes that depend on
    `HEAD`/branch refs (pin-disposition branch-tip resolution,
    `registry-check --rev master`) are not keyed. Flag these opens
    (`.git/HEAD`, `refs/`, `packed-refs`) and require `read_rev == REV` for
    such entries.
  - (c) A command's outcome can change when a directory gains or loses an
    entry (globs, censuses over `.ufo/evidence/round-*`) while no input sha
    changes.
- **F5. The record commit drifts its own inputs.** SCORECARD.md, LOG.md and
  PROVINCE.md are appended at the record commit. Buckets cite `LOG.md:303`,
  `LOG.md:316` and `PROVINCE.md:14-16`. If those files are in `inputs`, the
  append gives `input-drift`, and the score is 8 at the measured rev but 6 at
  the tip. That is the same "holds at measured, stale at landing" split the
  closure rejected. Either measure at the tip (condition 7), or keep
  append-only files out of the post-read commits. Silently re-pinning shas is
  not a fix.
- **F6. Inputs-overlay / ledger override leaking into the claim.** If the
  counted 8 used `--ledger-file`/`--inputs-overlay`, the measured commit does
  not carry its own evidence (condition 7). W03 already drafts that form.
- **F7. False uncredit, a blocker but not a lie.** The helper keeps
  "successful opens of regular files under root", while contract C defines
  `inputs` as lane-*tracked* files. Two cases fall between them:
  - `__pycache__/*.pyc` reads: an untracked
    `.ufo/evidence/round-16/__pycache__/` already exists in the live tree.
  - Opens of files the command itself creates.

  Both go into `inputs`, and at REV they become `input-missing`. Filter to
  `git ls-files` at the trace rev with read-only flags, and report the rest as
  `untracked_opened`.
- **F8. Box-3 append that does not parse or still overclaims.** A blank line
  or an unindented append falls outside the block, so `box3_link` is false.
  The fail is honest, but 8 is lost. An append that adds the r17 ledger path
  while leaving "every bucket … wrong expectations repaired" unqualified still
  passes the substring test and still overclaims (condition 8).
- **F9. Page changes after wave 2.** L1 typo fixes, the pasted W03 section, or
  the r17 SCORECARD/SKILL registry rows each produce new section shas. They
  leave buckets uncovered (fail-closed), or they force an unplanned wave-3
  re-read.
- **F10. External drift is not credited.** Sibling inputs are reported only.
  An instruction bucket whose stated outcome depends on a live sibling tree
  (not a pinned rev) can go wrong with no `input-drift`. The tick buckets
  (:1038-1059, :1164-1197) already scope themselves as "*at the tick*". Every
  other instruction bucket that reads siblings must be scoped the same way, or
  must pin a rev.
- **F11. Operability coupling.** Any registry row that `differs` at REV
  (AXES.md:34-36) blocks admission, whatever the box-3 count.

## Impacted axes

- **calibration:** conditions 1-8 and 10; F1, F2, F3, F5, F6 and F8 can each
  produce a false 8.
- **operability:** conditions 2 and 9; F11.
- **quality:** F3 (record cites made stale by the round's own tool edits) and
  condition 3.

Verdict: **partial.** The lane cap of 8 holds and is reachable. Contract C as
written still lets a false 8 through (F1 inputs completeness, F2 any-credit
aggregation), and the round-17 C2 edits will stale existing credit (F3, F5)
unless conditions 1-10 hold at the measured commit and at the tip.
