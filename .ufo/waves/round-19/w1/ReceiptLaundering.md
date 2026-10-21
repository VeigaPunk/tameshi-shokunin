# ReceiptLaundering — critic: failed-row replacement vs append-only supersession

Scope: R18-4 only — the mis-invoked `bash-witness-selftest` row in
`.ufo/evidence/round-18/final/checks.json` (round-18 verifier §5 item 4,
`round-18-verifier-spotcheck.md:196-200`). Question attacked: may the failed
row be **replaced in place** inside `checks.json`, or must the correction be
an **append-only** successor receipt that supersedes it?

Verdict up front: **in-place replacement is receipt laundering and must be
rejected.** Append-only supersession is the only semantics consistent with
the verifier's own correction style, the pinned baseline inputs, and
QUALITY 26/35/39. The delivered round-19 repair already implements it
correctly; residual tradeoffs named below are acceptable, not defects.

## Grounded evidence (all paths absolute under tameshi-shokunin)

- The failed observation: `.ufo/evidence/round-18/final/checks.json`
  `"bash-witness-selftest"` records argv
  `["python3","tools/bash-witness-study.py","--selftest"]`, `exit: 64`,
  `stdout_sha256: e3b0c44…` (sha256 of empty bytes — verified; `e3b0c44` is
  the canonical empty-input digest). Its stderr
  (`final/bash-witness-selftest.stderr`) is an argparse usage error:
  `the following arguments are required: mode`. The tool's real interface
  takes `selftest` as a **positional subcommand**
  (`tools/bash-witness-study.py` usage line: `{declare,run,rerun,count,check,selftest}`);
  the recorded argv used a nonexistent `--selftest` flag. The failure is a
  *usage error*, not a selftest failure — the suite itself is green:
  `final/bash-witness.stdout` ends `WITNESS_SELFTEST: 43/43 pass`,
  `VERDICT: PASS`.
- The verifier's own correction style is append-only for every sibling
  defect: §5.1 "an appended correction naming that line is owed"
  (`round-18-verifier-spotcheck.md:186`), §5.2 "append a correction naming
  it" (:191), §5.3 "State five, or name S008's status+used-by line
  explicitly" (:195). Item 4's "Do not leave a failed invocation as the
  selftest row of the final receipt bundle" (:199-200) is the only
  imperative that *could* be misread as license to rewrite the row — and
  reading it that way contradicts the verifier's three adjacent
  prescriptions.
- The pinned baseline makes in-place edit mechanically self-defeating:
  `.ufo/evidence/round-19/before.json` pins
  `.ufo/evidence/round-18/final/checks.json` at sha256
  `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d` under
  `inputs`, measured at baseline `7243e7f1…` with `corrected: 0, open: 5`.
  Any byte change to `checks.json` — including deleting or flipping the one
  row — breaks the digest-bound baseline measurement the C1 claim is
  scored against.
- The round-19 ruler already adjudicates this:
  `.ufo/evidence/round-19/measure.py` `witness()` (:112-120) requires a
  *separate* receipt at
  `.ufo/evidence/round-19/bash-witness-selftest-complete.json` with exact
  argv `['python3','tools/bash-witness-study.py','selftest']`, `revision ==
  4b7c6823a462f5ea2eafcb262275300a545f3ed7` (the *measured* revision),
  int `exit == 0`, digest-bound existing stdout/stderr with empty stderr,
  `WITNESS_SELFTEST: 43/43 pass` + `VERDICT: PASS` in stdout,
  `historical_receipt_preserved is True`, and
  `'.ufo/evidence/round-18/final/checks.json#bash-witness-selftest'` in
  `supersedes`. The `receipt()` helper (:61-76) rejects bool exits,
  missing stream files, and digest mismatch.
- The canonical criterion landed this round: `corpus/QUALITY.md:352-355`
  (criterion 39): "A failed usage/setup attempt stays failed and
  byte-preserved; its successful successor explicitly names what it
  supersedes. Timeliness is not repaired retroactively." Criterion 35
  (`QUALITY.md:262-274`) extends append-only errata to corpus prose;
  criterion at `QUALITY.md:222-223`: "The pinned bytes are not edited, and
  the old pin is marked superseded, not deleted."
- The lane's own gate rejected the alternative:
  `corpus/lessons/round-19.md` gate row: "Reclassify historical failed
  invocations as passing or overwrite checks.json | **reject** | would
  erase the observation that failed; corrected receipt explicitly
  supersedes it, never changes its exit." Mistakes row 3 names the defect
  class "Failed CLI attempt presented as the final receipt row."
- The delivered repair conforms: `bash-witness-selftest-complete.json`
  binds argv, `tool_sha256`, `runner_sha256`, `revision: 4b7c682…`,
  `exit: 0`, stream paths + digests, `recorded_at:
  2026-10-21T05:28:57Z`, `supersedes` naming **both** the round-18 failed
  row and the round-19 scratch failure `bash-witness-selftest.json`
  (exit 1, FileNotFoundError — also byte-preserved per Mistakes row 5),
  `historical_receipt_preserved: true`. Lesson erratum
  `## Errata R18-4 / R18-5` in `corpus/lessons/round-18.md` carries the
  required "failed raw invocation" phrase.

## Why replacement fails (counterexamples, strongest first)

1. **It manufactures provenance.** Rewriting the row to exit 0 either keeps
   `stdout_sha256: e3b0c44…` — now asserting a *successful* run produced
   empty stdout, directly contradicted by the real 43/43 output — or
   invents a digest for output never produced by that argv at that
   revision. Both are false receipts; the second is a fabricated
   observation, the exact "receipt laundering" this seat exists to catch.
2. **It destroys the defect's evidence.** The exit-64 + usage-error stderr
   is the only committed proof of *why* the row failed (wrong argv shape).
   Replacement erases the distinction between "selftest red" and "selftest
   never actually invoked" — the distinction Mistakes row 3 was created to
   preserve.
3. **It breaks the frozen baseline.** `before.json` pins the file's digest;
   the C1 measurement (0/5 → 5/5 on baseline `7243e7f1`) becomes
   unreproducible if the pinned input mutates.
4. **Even same-file *append* fails.** Adding a sibling
   `bash-witness-selftest-v2` key inside `checks.json` still mutates the
   pinned blob (violates QUALITY "pinned bytes are not edited") and the
   baseline input digest. Append-only here means **new artifact +
   `supersedes` pointer**, not append-inside-JSON.
5. **It reclassifies history.** The gate row states it: overwriting turns a
   recorded failed observation into a pass the run never earned.

### Strongest argument *for* replacement — and why it still loses

A literalist reading of §5.4 ("do not leave a failed invocation as the
selftest row of the final receipt bundle") could claim the bundle must not
*contain* a failed row, hence replacement or deletion. Rebuttal: the
verifier's own items 1–3 prescribe appended corrections for defects of the
same class; the fleet contract ("prior reports/evidence preserved;
corrections append dated named errata") and QUALITY 39 codify it; and the
sentence's *effect* — that no effective receipt may rest on a usage-error
invocation — is fully satisfied when the effective row is the superseding
43/43 receipt. No legitimate goal of replacement is unreachable via
supersession; replacement adds only evidence destruction.

## Falsifier (failure-capable, all mechanical)

- `git show 4b7c682:.ufo/evidence/round-18/final/checks.json | sha256sum`
  must equal `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d`.
  Any in-place edit or deletion fails this.
- The failed row must still decode with `exit == 64` and its original
  `--selftest` argv at that revision.
- The successor receipt must satisfy every clause of `measure.py`'s
  `receipt()` + `witness()`: wrong argv, bool/non-int exit, missing stream
  file, digest mismatch, non-empty stderr, missing `43/43`/`VERDICT: PASS`,
  `historical_receipt_preserved` absent/false, or a `supersedes` list
  lacking `checks.json#bash-witness-selftest` each independently reopens
  R18-4 → `status: open`. Ruler selftest (:176-206) already exercises
  bool-exit, usage-exit-64, tampered-stderr, and malformed-JSON mutants.
- A replacement-edited `checks.json` (green row, fabricated digest) does
  **not** satisfy the ruler — the successor path is still required — while
  additionally breaking the pinned baseline digest. Replacement is thus
  both insufficient and independently harmful: it cannot score and it
  destroys evidence.

## Minimal defensible acceptance for R18-4

1. `checks.json` byte-identical at the measured revision; failed row
   preserved verbatim (argv, exit 64, empty-stdout digest, usage-error
   stderr).
2. One new, separately named receipt under `.ufo/evidence/round-19/`
   binding: correct argv (positional `selftest`), `revision` = measured
   historical tip `4b7c682`, int `exit` 0, existing digest-verified
   stdout/stderr, empty stderr, stdout attesting `WITNESS_SELFTEST:
   43/43 pass` + `VERDICT: PASS`, `tool_sha256` and `runner_sha256`.
3. `supersedes` naming the failed row by `path#key`;
   `historical_receipt_preserved: true`; `recorded_at` dating the replay —
   late repair disclosed, never presented as a round-18 artifact
   (QUALITY 39's timeliness clause; ruler requires the erratum phrase
   "does not claim the receipt existed in round 18" for the sibling item).
4. A dated erratum in `corpus/lessons/round-18.md` naming the failed raw
   invocation.

All four are already met by the delivered artifacts; acceptance requires
nothing beyond what exists.

## Residual tradeoffs (report, not defects — for the canonical judge)

- **One-directional pointer.** Byte-preservation forbids a
  `superseded_by` back-pointer inside `checks.json`; a consumer reading
  only that file still sees exit 64 as the last word. Discoverability
  rests entirely on the successor's `supersedes` plus the lesson erratum.
  Inherent cost of byte-preservation; strengthening it would require an
  index/manifest convention, not in-place edit.
- **`revision` field ambiguity.** The successor's `revision: 4b7c682` is
  the *measured* revision; `recorded_at` + erratum disclose the replay's
  lateness. A field named `measured_revision` would be clearer; current
  naming is honest but demands the reader pair it with `recorded_at`.
- **Combined erratum.** `## Errata R18-4 / R18-5` covers two routed
  defects in one block; the ruler keys required phrases per defect, so
  independent reopening still works.

## Impacted axes

- **quality**: receipt integrity — replacement fabricates/erases
  observations; append-only preserves and supersedes.
- **discernment**: the honest-failure record is what separates a corrected
  defect from a laundered one; the gate row rejecting overwrite is the
  discernment move.
- **calibration (the owned axis)**: C1 measures *defects durably
  corrected*, not score cosmetics — a rewritten row would fake correction
  by erasure and could never fail an audit that re-opens the historical
  blob.

## Method / no-harm

Read-only seat. Commands used: `cat`, `grep -n`, `sed -n`, `find`, `ls` on
the named files; `read` tool on `measure.py`, QUALITY, lesson files. No
production edits, no git/jj writes, no selftests/builds/lints, no
subagents, no installs (none needed). Observations are quoted from
committed bytes; the "laundering" characterization of replacement is
inference from the digest-binding argument above, not from any
tool-observed misbehavior.
