# FrozenPopulation — critic: five-item defect denominator vs §5, append-only, drift

**Review date:** 2026-10-21. **Scope attacked:** whether the five-item C1
denominator (frozen in `.ufo/evidence/round-19/contract.json`, ruler
`.ufo/evidence/round-19/measure.py`) faithfully covers exactly the five
routed defects in `corpus/lessons/round-18-verifier-spotcheck.md` §5
(:182–204), whether any denominator item can read `corrected` while its
defect remains, and whether the correction set stays append-only.
Read-only seat; no production edits; per lane bounds I did not run the ruler
— all predicate verdicts are traced from source plus committed receipts.
Delivery observed: baseline `7243e7f…`, freeze commit `78b99dd`, corrections
`21e7932`; worktree also holds **untracked** `after-21e7932.json` plus
uncommitted `SCORECARD.md`/`corpus/lessons/round-19.md` at read time.

## Axes

- **A1 denominator fidelity** — measured population ≡ verifier §5 items.
- **A2 failure-capability** — each predicate can still report `open`.
- **A3 receipt commitment** — claim evidence lives in committed blobs.
- **A4 append-only / durability** — original bytes kept; corrections named,
  appended, and stable against semantic (not just textual) regression.

## A1 — population layer: no drift observed

`contract.json` (frozen at `78b99dd`, one commit **before** corrections at
`21e7932` — pre-registration order holds) maps R18-1→§5.1 (guard-kill
PENDING), R18-2→§5.2 (S008 queued), R18-3→§5.3 (four-vs-five deletions),
R18-4→§5.4 (mis-invoked witness row), R18-5→§5.5 (unbacked 4b7c682
60/60). The ruler hardwires the same five identifiers
(`measure.py:137-139`); `before.json` reports all five `open` on the
frozen baseline with per-input SHA-256s. No sixth item, no renumbering, no
substitution. **The denominator itself is honest.** The risk concentrates
in *how* `corrected` is earned.

## Counterexamples

### Cx-1 (A3, live): claim-bearing after-receipt is not committed

`after-21e7932.json` is the only artifact reporting `corrected=5, open=0`
at the delivered revision — and at observation time it is untracked
(`git status` `?? .ufo/evidence/round-19/after-21e7932.json`), absent from
`git ls-tree -r 21e7932 .ufo/evidence/round-19/` (14 files listed). The
SCORECARD draft cites it already: "`21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`:
corrected=5, open=0, total=5, exit0". The verifier's own method was
"reconstructed from revision-pinned Git blobs, committed receipts"
(spotcheck :16-17); an uncommitted after-receipt fails that convention the
same way §5.5 failed the round-18 tip for lacking a committed receipt.
**Fixable defect, not a ruler flaw** — but any audit run before it lands
must reject, and the same check applies to the pending SCORECARD/LOG/
round-19.md claims that quote it.

### Cx-2 (A2): R18-3 arithmetic is verified against a lane-authored file, never recomputed

`arithmetic()` (`measure.py:105-111`) accepts the erratum plus a regex
`^25\s+5\s+corpus/SOURCES\.md$` over `sources-diff.txt` — a text file the
lane wrote (content: `git diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md`
→ `25 5`). It never recomputes the diff, and it checks only that the
erratum *contains* `S001 S008 S052 S056 S057`, not that those are the
rows actually deleted. Falsifier: an erratum naming S001–S057 that
includes one wrong row, or a `sources-diff.txt` fabricated outright, still
passes 5/5. Mitigating fact (independent, not ruler): the spotcheck
itself recorded "committed diff has **5** deleted lines (S001, S008,
S052, S056, S057)" (:194-195, §3 :151-153) and I independently reran the
numstat → `25 5`. So the delivered content is right; the *predicate* is
shallower than the defect requires.

### Cx-3 (A2/A4): semantic-drift gap — markers pass, named-line supersession untested

Every correction predicate is presence-of-markers on post-split text
(`measure.py:90-136`). None verify (a) the block is appended rather than
an in-place rewrite, (b) the superseded line still exists and is the one
named, or (c) that a *later* contradicting erratum hasn't reopened the
defect. Concrete falsifiers the ruler cannot see:

- **R18-1:** `guard()` wants `'line 2'`, `'Effective verified-at:'`,
  `TOOLS18`, `'18 mutation survivors'`. An erratum containing those
  strings *without* naming the `verified-at:` metadata line — the
  contract line §5.1 calls out — still passes. Delivered text does
  name "line 2's `Landed-tip results: PENDING…`" plus twelve further
  staged lines (diff at `guard-kill-closure.md` +169..+189), which
  satisfies the verifier's floor of "an appended correction naming that
  line" (:186); residual gap is ruler-vs-intent, not content.
- **R18-5 residual (structural, bounded):** the fleet report's sentence
  "the same no-override count at final `4b7c682…` returned **60/60,8**"
  (`.ufo/reports/round-18/tameshi.md:53`, fleet repo) is immutable
  history — append-only cannot delete it. The landed fix is the
  verifier's other horn: a committed receipt at `4b7c682`
  (`round18-final-measure.json`, revision field `4b7c682…`, exit 0,
  digest-bound stdout) plus an erratum that "does not claim the receipt
  existed in round 18". Acceptable; but the auditor must grade it as
  *evidence landed*, not *sentence dropped* — §5's own disjunction
  (:203-204). Any audit requiring literal removal must reject against the
  lane's append-only mandate; that is a tradeoff for the canonical judge,
  not a defect.

### Cx-4 (A2): receipt predicates bind the receipt, not the execution

`receipt()` (`measure.py:61-76`) enforces exact argv, `revision==REV18`,
`exit==0`, empty stderr, digest-bound stdout — all attested fields. For
R18-4, `tool_sha256`/`runner_sha256`/`recorded_at` on
`bash-witness-selftest-complete.json` are unchecked; the selftest's eight
receipt mutants never touch them (`measure.py:179-185`). Falsifier: a
hand-authored JSON claiming `WITNESS_SELFTEST: 43/43 pass` + `VERDICT:
PASS` stdout and the correct supersedes link scores `corrected` with no
execution. This is inherent to the evidence-verify (not re-execute)
convention the verifier itself set (:17-18) — so minimal acceptance is
attestation+commitment, but the audit should additionally verify
`tool_sha256` against `git show 4b7c682:tools/bash-witness-study.py |
sha256sum` since the field exists to be checked. Same gap on R18-5's
`round18-final-measure.json` (no tool pin at all on that receipt).

Secondary observation: the retained v1 scratch receipt
`bash-witness-selftest.json` uses `"supersedes": "<string>"` while the
complete receipt uses a list — shape drift across the supersession chain.
Cosmetic today (the ruler only reads the complete receipt), but any future
index over `supersedes` must handle both shapes.

### A4 — append-only: observed conformant, one caveat class

`git diff --numstat 7243e7f 21e7932` shows zero deletions on every
corrected file — guard-kill +21/−0, mutation-case +12/−0, round-18 lesson
+36/−0, LOG +35/−0, SCORECARD +31/−0 — except `corpus/SOURCES.md` +9/−1.
That single deletion is an in-place `used-by` cell edit on S049 (adds
`corpus/lessons/round-19.md` to the cell list). The spotcheck's own
accounting treats exactly this kind of cell update as permitted and
documented (round-18: "all five deletions are the documented cells"
:152-153), and the lane logged the S049 used-by gain in `sources-diff`-era
ledger prose. **Not a violation under established convention** — but it
is a second line-edit inside a round whose corrections are advertised as
append-only errata; the audit should confirm the S049 diff is *only* the
used-by cell, which I verified it is (teaches/status/tier cells identical
between baseline and delivered rows, line 58).

## Failure-capability matrix (traced, not executed)

| Row | Predicate must see | Realistic failure it still catches |
|---|---|---|
| R18-1 | `## Erratum R18-1` + 'line 2' + 'Effective verified-at:' + TOOLS18 + '18 mutation survivors'; checks.json probes row digest-bound to probes.stdout `open=0 closed=11` | missing/renamed erratum, tampered probes receipt, wrong tools rev |
| R18-2 | `## Erratum R18-2`; S008 row = 13 cells, `mined`, CASE in used-by; note names 'line 1' + REV18 | status regress to queued, used-by drop, absent note |
| R18-3 | `## Erratum R18-3` + 'five deleted table lines' + 5 IDs + numstat regex | missing erratum/ID/file — but **not** wrong-but-present facts (Cx-2) |
| R18-4 | strict-JSON receipt, argv `bash-witness-study.py selftest`, exit 0, empty stderr, digest-bound 43/43+VERDICT stdout, `historical_receipt_preserved`, supersedes old row, note 'failed raw invocation' | argv/exit/digest/supersedes tamper; duplicated keys; NaN (selftested) |
| R18-5 | receipt argv `measure.py --rev 4b7c682 --explain`, strict-JSON stdout 60/60 box3 restraint8 no-override ledger_committed; note disclaimer | wrong rev/score/digest; missing disclaimer |

Baseline runability is proven by `before.json`: same ruler_sha256
(`c538c33d…e18e`) as the after-receipt, all inputs digest-pinned,
`corrected=0/open=5` — the ruler genuinely fails on baseline rather than
being calibrated to pass.

## Impacted axes

- **calibration** (claimed): Cx-1 can block acceptance outright if the
  after-receipt isn't committed before audit; Cx-2/Cx-4 are ruler-depth
  gaps that a failure-capable audit should close by re-derivation.
- **operability** (not claimed, adjacent): Cx-3's supersession semantics
  are the load-bearing convention; grading R18-5 as "sentence must be
  deleted" would force an append-only violation — reject that reading.

## Minimal defensible acceptance

1. Commit `after-21e7932.json` (and the claiming SCORECARD/LOG/lesson
   edits) before audit; audit reads every input via `git show REV:path`,
   never worktree. Reject if the after-receipt is absent from the cited
   revision's tree or its `inputs` digests don't match the blobs.
2. `ruler_sha256` identical between before/after receipts; selftest line
   `SELFTEST: N/N` with zero failures recorded in committed output.
3. R18-3: auditor recomputes
   `git diff --numstat 183f87b… 4b7c682… -- corpus/SOURCES.md` on pinned
   revisions (expect `25 5`) **and** confirms the five deleted table lines
   are exactly S001/S008/S052/S056/S057 by reading the row diffs —
   `sources-diff.txt` corroborates, never substitutes.
4. R18-1/2: erratum block exists appended after all prior content, names
   the stale line(s) by number, and the stale line is still present and
   unchanged (append-only verified by numstat `0` deletions on both
   knowledge files).
5. R18-4/5: receipts exist as committed blobs at the delivered revision;
   strict-JSON, exact argv, `revision=4b7c682…`, exit 0, empty stderr,
   digest-bound stdout; R18-4 supersedes names
   `.ufo/evidence/round-18/final/checks.json#bash-witness-selftest` and
   the old failed row is byte-identical to baseline; R18-5 erratum keeps
   the "not in round 18" disclaimer. Additionally verify
   `tool_sha256`/`runner_sha256` against pinned blobs where present.
6. Whole-diff append-only: `git diff --numstat 7243e7f <delivered>` shows
   deletions only inside documented SOURCES used-by cells (currently:
   exactly S049 line 58).
7. Denominator stays five: `rows` length 5, ids R18-1..R18-5, `total=5`
   in both receipts; any added row, renamed id, or rescored item fails.

Falsifier for acceptance: any single committed-diff counterexample —
missing/uncommitted after-receipt; recomputed numstat ≠ `25 5` or a
deleted row ∉ the named five; an erratum absent or placed inline; a
receipt failing any bound in (5); a deletion outside documented cells —
and C1 reads `open≥1`, not `corrected=5`.

## Tools / installs

None installed or updated; no pacman transaction. Commands run:
`git log/status/diff/numstat/show/ls-tree/cat-file` (read-only) under
tameshi-shokunin, `grep`/`head` on lane files. All observations above are
from committed blobs and the stated files; the after-receipt's untracked
status and the two pending corpus edits are time-stamped observations
(2026-10-21) that may resolve when the lane lands its claim commit —
re-check Cx-1 first at audit time.
