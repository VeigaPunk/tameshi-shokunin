# SourceReview — round22 residual falsification (S082 and corpus entries)

Seat: `TameshiR22.SourceReview` (critic, read-only). Candidate
`e4da41c3102f6f90b42257d4b8785335806ef954`; base
`51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`; contract
`.ufo/evidence/round-22/contract.json`.

Exercised: `git show`/`git diff`/`git log`/`git cat-file` reads, JSON reads,
sha256 of two bundle files, `awk` field count of SOURCES.md:91. No tests,
gates, selftests, builds, installs, or git/jj writes. Tool installs/updates:
none.

Axes: provenance (cited evidence exists and is quoted exactly), calibration
(tier/scope/claim size), append-only integrity, and authority boundary
(advisory reports versus outside authority).

## Verdict

**One blocking defect (B1)**, six nonblocking findings. The S082 source and
located quote reopen exactly. Append-only obligations hold.

## B1 — BLOCKING: the knowledge entry and lesson cite evidence that does not exist

- Counterexample: `corpus/knowledge/callback-authoritative-accounting.md:2`
  says "final committed-revision execution **is retained** in
  `.ufo/evidence/round-22/final/verification.json`". `corpus/lessons/round-22.md:46`
  says "Actual streams are retained in round22 final/verification.json".
- Evidence:
  - `git cat-file -e e4da41c:.ufo/evidence/round-22/final/verification.json`
    fails, and the worktree has no `.ufo/evidence/round-22/final/` directory.
  - `git log -S'final/verification.json' -- corpus/` shows that `66a25ab` introduced
    the citation, so it has been a false present-tense claim at both `66a25ab`
    and `e4da41c`.
  - Knowledge lines 46-48 make the same claim again: "The final verification
    receipt records observed exits…".
- Rules violated:
  - `corpus/QUALITY.md:21-26` criterion 8: an unreported verification is never
    cited as a pass.
  - Criterion 9: evidence must be in the repo before the commit that cites it.
  - Admission bar 2 (`QUALITY.md:3-4`).
- Impacted axes: provenance, calibration. This is false provenance: a future
  receipt is described as retained.
- Smallest safe correction (L1, at integration):
  - Land `.ufo/evidence/round-22/final/verification.json` with the actually
    observed exits, streams, instrument hashes and measured commit.
  - The citing text predates the file. So append a dated erratum to
    `corpus/lessons/round-22.md`, not an in-place rewrite (QUALITY35,
    `QUALITY.md:265-280`). The erratum should name the forward reference at
    `66a25ab`..`e4da41c` and the revision that first contains the file.
  - If no final receipt is produced, the erratum must replace "is retained"
    with named debt under criterion 8.

## Reopened S082 source: passes

- Source file: `.ufo/waves/round-21/original-outcomes-final.json`.
- At `51d49d5`, `git show … | grep -n rehabilitate` finds only line 1369:
  `"partial_report_files_do_not_rehabilitate_failed_jobs": true,`.
  The lesson quote (`corpus/lessons/round-22.md:28`) matches exactly, minus the
  JSON trailing comma.
- The blob is `2a3f0daa7a4e886415184e691420dd2e302042c2` at both base and
  candidate, so the source is unchanged. The file was introduced in `678a67f`.
- The QUALITY34 line-anchor check (`QUALITY.md:255-260`) passes: name, line
  and revision agree.
- Adjacent totals are at lines 1364-1368: seats 146, completed 66, dead 80.
  The two failed-with-report rows are `wave2.rows[52]`
  `ProfileBashTsukuroiCensus` and `wave2.rows[69]` `V01WitnessTests`. Both are
  `status: failed`, have a report path, `replaced: false`, and role reviewer.
- Second anchor: `corpus/lessons/round-21.md:163-174` `## Outcome-accounting
  erratum (round21)` exists. It is unchanged from base to candidate: the diff
  for that path is empty. It preserves the superseded "forty returned;35"
  statement and the 38/37 and 66/80 corrections.
- SOURCES contract rule 1 (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:45-47`) is
  satisfied. Lesson Gate lines 25-35 give the path, the access date
  2026-10-21 UTC, and a quote of 25 words or fewer with its location.
- Row shape:
  - `SOURCES.md:91` has 11 columns (`NF=13`), kind `own-work`, status `mined`.
  - Both used-by paths exist at the candidate.
  - The scope cell excludes provider authenticity, consistent with contract
    bound 1.

## Knowledge, lesson, QUALITY45, README and SKILL entries against obligations

- Append-only:
  - `git diff --numstat 51d49d5 e4da41c` reports zero deleted lines in every
    file.
  - The `Next unused id: S082.` footer is retained at `SOURCES.md:268`, and
    `S083` is appended at `:291`, satisfying the QUALITY35 footer rule.
  - No existing SOURCES row cell changed.
  - `QUALITY.md` criterion 45 (`:443-453`) continues from 44 under its own dated
    heading.
- QUALITY45 falsifier against data:
  - `sha256(bundle.json)=dfb1027f…45c18e` and
    `sha256(wrong-count-bundle.json)=d984c49c…a7a17e` each equal the
    `bundle_sha256` in their expected file, so the red run is digest-matching
    rather than a tamper.
  - `TOTAL_MISMATCH` exists at `tools/wave-accounting.py:114`.
  - Both failed-with-report identities stay failed in the source.
  - These are data observations only; neither exit was exercised.
- Scope and contract bounds:
  - Numeric depth and calibration stay 8 (`SCORECARD.md` round22, lesson:71).
  - r21 stays admitted (lesson:54-55; `LOG.md` round22 "Round21 admission is not
    redone").
  - The eight synthetic predicates are kept separate from the 146 seats and the
    two historical false positives (knowledge:50-54, README round22, SCORECARD).
  - Callback integrity is stated as not authentication (knowledge:23-25, 60;
    `SKILL.md:1992-1993`).
- README: the round22 entry's "same-ground calibration repair, not a new
  frontier crossing" matches the README:285 precedent. The knowledge file has
  its coverage/index row in the same round (QUALITY7, `QUALITY.md:18-20`).
- Knowledge header: opens with `source:`, `verified-at:` and `recheck:`, as
  required by QUALITY10 (`QUALITY.md:27-30`). The `verified-at:` content is the
  B1 defect.
- Retained corroboration: `.ufo/evidence/round-22/round21-callback-corroboration.json`
  reports `count 146, headers_retained 146, agree 146`, consistent with
  knowledge:59-60 and lesson:97-98.
- Route-mix data cited at lesson:47 checks out:
  - `.ufo/waves/round-22/route-mix.json`: exit 1, `over_bound.zai=38`.
  - `route-mix-final.json`: exit 0, `zai=24`.

## Advisory reports versus outside authority: passes

- Lesson:22-23 reserves outside non-author admission and admit/reject sampling
  for fleet closure.
- Lesson:36-40 labels SourceScope advisory and rejects its RFC 9110 analogy
  with a flip condition, so the rejection is kept (admission bar 5).
- Seat findings are framed as observations, not admission:
  - PartialEvidence (lesson:59-64), and Audit26/Audit29 (lesson:88-92).
  - "Read-only seats corroborated" (lesson:81).
  - Both rejected seat recommendations (`report=null`, in-place edits) are
    recorded with reasons (lesson:82-85).
- Both advisory files label themselves advisory and wrote no production
  content:
  - `.ufo/waves/round-22/w1/SourceScope.md:16`.
  - `.ufo/waves/round-22/w1/AppendOnlyScope.md:5`.
- No own-seat output is claimed as independent review credit, matching
  contract bound 2.

## Nonblocking findings

- **N1 — the tier A justification is a tradeoff, not a defect.**
  - The contract's own-work tier A example is "the lane's own re-runnable gate
    output" (`SOURCES-CONTRACT-v1.md:26-27`). The S082 source is a
    hand-corrected declaration snapshot introduced with the erratum in
    `678a67f`, not gate output.
  - Sibling metadata in the same file is admitted unreliable: provider labels on
    three rows, and Section0827 text drift (lesson:59-64, 88-92).
  - The scope cell confines tier A to declared statuses and membership, and the
    146/146 corroboration supports that scope. So tier A as "primary for what
    the lane declared" is defensible.
  - Optional fix: an appended lesson note that grounds the scoped tier in the
    corroboration, not in gate output. Do not edit the immutable tier or scope
    cells.
- **N2 — anchor versus teaches.**
  - The quote at :1369 grounds only the "cannot rehabilitate failed jobs" half
    of `teaches`.
  - "Against exact registry identities" and scope "original membership" rest on
    other evidence: rows :1123-1128 and :1297-1302, totals :1364-1368, the
    round21 `w1`/`w2` `swarm-registry.json`, and `tools/wave-accounting.py`.
  - This does not break contract rule 1. Optional fix: an appended note citing
    range :1364-1369.
- **N3 — `on-change` recheck token.**
  - `grep -c on-change corpus/SOURCES.md` returns 1: S082 is the only use.
  - The contract lists `90d`, `180d`, `on-release` or an ISO date
    (`SOURCES-CONTRACT-v1.md:38-39`). The existing `365d` (S079/S080) shows the
    list is not treated as closed, and the census enum check does not test
    recheck.
  - The token is coherent for a revision-pinned blob. No correction is
    required.
- **N4 — search log scope.**
  - `SOURCES.md:284-289` counts identified2/screened2/included2/excluded0. That
    is correct for L1's own-work lookup.
  - The advisory seat separately opened RFC 9110 §15 and a `wait(2)` alternate
    (`SourceScope.md:50-84`). L1 did not open them, so writing no row is right
    under rule 1.
  - Optional fix: append one search-log sentence noting the advisory-only
    external candidate and why it is not a row.
- **N5 — path shorthand.** "round22 route-mix.json" (lesson:47) means
  `.ufo/waves/round-22/`, while "round22 final/verification.json" means
  `.ufo/evidence/round-22/`. This is resolvable but inconsistent.
- **N6 — freeze-before-spawn ordering.**
  - Lesson:12-13 says `contract.json` and `before.json` landed in `81106f9`
    (2026-10-21T10:36:06-03:00) "before any seat spawned". `81106f9` does
    contain both.
  - `run1.json` and `dispatch1-attempt2.json` carry no timestamps and landed in
    `66a25ab`, so the retained files do not independently timestamp the
    spawn-after-freeze ordering. [INFERENCE: not falsified, not independently
    shown.]

## Checks for L1 after integration

- `.ufo/evidence/round-22/final/verification.json` exists at the final
  revision with actual observed tuples, plus the B1 lesson erratum.
- `git diff --numstat 51d49d5 <final> -- corpus LOG.md` still shows zero
  deletions.
- The SOURCES contract census (`SOURCES-CONTRACT-v1.md:66-81`).
- The registered `wave-accounting-frozen-entry` and `wave-accounting-selftest`
  rows, and the frozen `measure.py`, at the final revision.
