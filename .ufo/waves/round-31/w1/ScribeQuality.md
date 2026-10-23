# ScribeQuality — round 31, wave 1

Verdict: Draft only. Paste-ready text below appends criteria 66–70 and append-only errata for F1–F4. No production file was edited.

Axes: source fidelity, scope precision, falsifiability, append-only correction.

## Provenance and observed evidence

The requested baseline was read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:corpus/QUALITY.md`; it ends at criterion 65. The first attempt was rejected before execution because the requested scratch working directory did not yet exist. The successful shell command was `mkdir -p /fast/scratch/hyaku/tameshi-r31-seats/ScribeQuality && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:corpus/QUALITY.md`; it returned the committed text through criterion 65.

Relevant committed evidence:

- `corpus/lessons/round-30-verifier-spotcheck.md:40-45` records the dispatched-seat/non-author conflict and the bad `:60-62` paragraph cite; it quotes LEARNING.md §Discernment and AXES.md.
- `SCORECARD.md:1473` calls JudgeC1 a “named non-author seat”; `.ufo/waves/round-30/wC/JudgeC1.md:3` calls the review “Non-author” despite the dispatch noted by the spot-check.
- `corpus/lessons/round-30.md:159-182` records the missing pre-dispatch dead-seat comparison and the workdir/kill breach. `.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt:7-10` lists dead seats; `.ufo/waves/round-30/spec-wC.json:279-284` includes ConnectorOverlap. `.ufo/waves/round-30/wC/ColdA01.md:45,100` records a regression invocation without `--workdir` and a broad kill of a sibling's processes.
- `corpus/lessons/round-30.md:69-73,213` routes binding v4. `.ufo/evidence/round-30/coldread/bind-select-v3.py:2-10` describes the pre-data selector; `.ufo/evidence/round-30/coldread/audit-bound-wC.py:2-9` identifies stricter checks as a separate post-data audit.
- `corpus/lessons/round-30.md:59` cites the S094 paragraph as `:60-62`; the spot-check at `corpus/lessons/round-30-verifier-spotcheck.md:44-45` says the paragraph is line 60 only.
- F1–F4 findings and smallest corrections are in `.ufo/waves/round-30/wC/ReviewQualityR30.md:16-71`.

## Paste-ready text to append to `corpus/QUALITY.md`

```text
## Criteria appended — round 31 (2026-10-23)

Routed by `lessons/round-30-verifier-spotcheck.md` (Conformance defects and routed defects 1–5) and `lessons/round-30.md` Mistakes 2, 4 and 5. Criteria 1–65 remain unchanged.

66. Round 31. A seat dispatched by this lane remains part of the lane and is
    not described as a non-author or independent reviewer of that lane's work.
    A different seat name or report does not change dispatch provenance; its
    report may support the lane's ruling but cannot supply the non-author
    ruling. Captured by: `lessons/round-30-verifier-spotcheck.md:40-43`
    (LEARNING.md §Discernment and AXES.md quotes). Falsifier:
    `.ufo/waves/round-30/wC/JudgeC1.md:3` calls JudgeC1's review
    "Non-author"; `SCORECARD.md:1473` calls it a "named non-author seat"
    although the spot-check records that the L1 dispatched JudgeC1.

67. Round 31. Every seat invocation of `--regression` passes `--workdir`
    with a directory beneath that seat's own scratch directory. Before any
    process is killed, the seat checks `/proc/<pid>/cwd` and verifies that it
    resolves beneath that seat's own scratch; a process the seat did not start
    is never killed. Captured by: `lessons/round-30.md:169-182` (Mistake 5).
    Falsifier: `.ufo/waves/round-30/wC/ColdA01.md:45` records
    `timeout 240 bash tools/mutate-and-run.sh --regression --keep` without a
    `--workdir`; `ColdA01.md:100` discloses killing sibling processes with a
    broad `pgrep`/kill.

68. Round 31. Before any re-dispatch after a seat is dead or has no report,
    a committed check lists every dead seat for the round and compares each
    dead seat's task text with each proposed item. The check records the
    comparison and disposition; an item measuring the same object is not
    dispatched again. A name match triggers comparison but does not replace
    the task-text comparison. Captured by: `lessons/round-30.md:159-168`
    (Mistake 4). Falsifier: `.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt:7-10`
    lists ConnectorOverlap among the dead seats, while
    `.ufo/waves/round-30/spec-wC.json:279-284` includes an item of that name;
    `lessons/round-30.md:164-168` records that no overlap check ran before
    dispatch.

69. Round 31. The binding conditions for a data wave are frozen as executable
    code before data dispatch, and the frozen code is scored against the
    required controls before data. A post-data audit may add findings but
    cannot supply, change or retroactively satisfy a binding condition.
    Captured by: `lessons/round-30.md:69-73,213` (Mistake 2 and routed
    binding v4). Falsifier: `.ufo/evidence/round-30/coldread/bind-select-v3.py:2-10`
    freezes a selector that lacks the stricter conditions implemented by the
    separate post-data audit `.ufo/evidence/round-30/coldread/audit-bound-wC.py:2-9`.

70. Round 31. A line-range citation to a paragraph names all and only the
    lines containing that paragraph; it excludes adjacent blank lines and a
    following heading. A one-line paragraph is cited as one line. Captured by:
    `lessons/round-30-verifier-spotcheck.md:44-45`. Falsifier:
    `lessons/round-30.md:59` cites the S094 paragraph as `:60-62`, although
    the paragraph is line 60, line 61 is blank, and line 62 is `## Limits`.

## Errata — round 30 QUALITY imprecisions (append-only; 2026-10-23)

These errata qualify the prior text; they do not rewrite it.

- **F1 — criterion 60 (`corpus/QUALITY.md:683-688`).** The Falsifier's
  normalization example is incomplete. Read “report `executed-ok` vs entry
  `gap-minor`” as “reports `executed-ok` and `verified-record` normalized to
  entry `gap-minor`.” The second observed pair is `verified-record` to
  `gap-minor` (`.ufo/waves/round-30/wC/ReviewQualityR30.md:22-29`); the
  claim that the excluded entry verdicts are passing classes is unchanged.
- **F2 — round-30 routing preamble (`corpus/QUALITY.md:649-651`).** Its
  mistake list is incomplete. Read “Mistakes 1, 4 and 5” as “Mistakes 1, 3,
  4 and 5”; criterion 61 itself routes Mistakes 3 and 4
  (`ReviewQualityR30.md:35-43`).
- **F3 — criterion 62 Falsifier (`corpus/QUALITY.md:705-709`).** “The only
  C2 head receipt” overstates the revision measured by
  `c2-at-E.stdout` (`7a45f7b9`, committed at `9bb699ad`). Read it as “the
  only committed C2 counter receipt”; the receipt is not a head receipt, and
  no receipt is committed for the three named head commits
  (`ReviewQualityR30.md:45-56`).
- **F4 — criterion 63 Falsifier (`corpus/QUALITY.md:716-721`).** The
  committed `drift-sim-union4.txt` reports `covered=33/64` at
  `rev=daa11583`; `contract.json:45` records the four-file comment-line
  sandbox recipe. The sandbox revision is not an object in the lane
  repository, so the receipt establishes its printed output, not an
  independently re-checkable construction. The 64/64 base and 52/64 earlier
  readings are separately recorded by `monitor-at-base.stdout` and
  `.ufo/evidence/round-29/c1-at-A.stdout`. Retain the recipe only as
  contract-reported context, not as verified construction evidence
  (`ReviewQualityR30.md:58-71`).
```

## Gates, scope, and limits

- Gates, counter, selftests, and regression runs: not executed; this was a drafting/scribe assignment.
- Actual touched surface: only `.ufo/waves/round-31/w1/ScribeQuality.md`; created the seat's own empty scratch directory. Proposed `corpus/QUALITY.md` additions and errata above were not applied.
- Out of scope: product edits, edits to the prior lesson/review, commits, promotion, producer-authentication, and numeric-score claims. No tools installed or updated.
- Bounds disclosure: the successful `git show` shell call was inadvertently launched with process cwd `/home/vgpnk/Projects/shokunin`, not the required seat scratch cwd. Its command only created this seat's scratch directory and performed the requested read-only `git -C ... show`; it did not write in the lane or fleet repository. The initial call failed before running because the scratch cwd did not exist. Subsequent source inspection used read-only file tools; no other seat scratch was opened.

Artifact: `.ufo/waves/round-31/w1/ScribeQuality.md`.
