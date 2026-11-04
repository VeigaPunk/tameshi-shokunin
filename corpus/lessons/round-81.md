# tameshi round 81 — lesson (hyaku run 15)

Lane: tameshi-shokunin. Round: 81 (attempt 1), 2026-11-04. Base:
`56a0129fe9bfd0ce607290a36350e38ac4df9c72` (= `origin/master`, the round-80
closure and spot-check tip). Frozen plan: `plans/round-81.plan.md`
(declaration `1b115ba038e3d3bffc1432e62bbe5eb422c81266`). Three claims on
distinct axes: R81-C1 calibration (the round-80 closure's routed-defect
register is bound to repo state), R81-C2 freshness (every standing self-state
row pins settled instrument bytes), R81-C3 coverage (the suite's own assertion
text is pinned, so the two round-80 test-text survivors die).

## What was measured — R81-C1

- Before (base tip, instrument declared at `1b115ba0`):
  `DEFECT_BIND: rows=6 closed=0 open=6 unexpected=6` exit 1
  (`.ufo/evidence/round-81/controls/c1-before.txt`).
- Do-nothing control: the base tip itself — appending nothing leaves all six
  rows open, each naming its missing artifact.
- Landed: `tools/defect-bind.py` (five row kinds: `tree-paths`, `tree-bytes`,
  `receipt-tokens`, `sources-cell`, `doc-contains`; setup refusals before any
  row effect), `tools/defect-bind.json` (six rows over D1/D2/D4/D5/D6), and the
  six fixes: the two 7 MB round-80 receipts and the census-before receipt
  committed, the SCORECARD erratum with the receipt's true tokens, S289's
  `used-by` cell, the S289 fetch receipt, and the two Search-log notes.
- After: `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0` exit 0;
  `DEFECT_BIND_SELFTEST: 11/11 pass`.
- Sourced? No external row: a record-vs-repo-state count, per AXES.md
  calibration (a calibration claim counts mismatches, never asserts).

## What was measured — R81-C2

- Before (base tip): `SELFSTATE_PINS: rows=23 settled=20 stale=3` exit 1
  (`controls/c2-before.txt`), naming `receipt-exists-selftest` (pin
  `21ef81e9`, tool last changed at `4af6695f`), `receipt-bind-selftest` and
  `registry-bind-selftest` (both pin `ae591d5a`, both tools changed at
  `01ca77cd`).
- Landed: `--pin-audit` / `--pin-rev` in `tools/selfstate-freshness.py`
  (blob equality at pin vs tip; setup exit 2 on an unresolvable pin rev or a
  path absent at the pin) + arms 18–20; the three stale rows re-pinned at
  their instruments' last-modifying commits.
- After: `SELFSTATE_PINS: rows=23 settled=23 stale=0` exit 0; the standing
  sweep stays green (`SELFSTATE: rows=23 match=…`, exit 0);
  `SELFSTATE_SELFTEST: 21/21 pass`.
- Sourced on **S289** (git-cat-file, re-opened this round: the
  `blob <rev>:<path>` binding the audit rests on).

## What was measured — R81-C3

- Before (base tool bytes): `MUTATE: DONE (target=c3-base-ss defects=1
  killed=0 survived=1)` and the wave-reconcile twin, both `CONTROL: GREEN`,
  restore byte-identical (`controls/c3-base-ss.txt`, `c3-base-wr.txt`).
- Landed: `SELFTEST_TEXT_SHA256` + `ARM21_selftest_text_pin` (selfstate) and
  `arm25-selftest-text-pin` (wave-reconcile) — a digest of
  `inspect.getsource(selftest)` against a pinned constant; the two survivors
  appended to the standing specs (`ss-bom-only`, `wr-prefix`).
- After: selfstate `defects=5 killed=5 survived=0`, wave
  `defects=14 killed=14 survived=0`, both `CONTROL: GREEN`, restore
  byte-identical; `SELFSTATE_SELFTEST: 21/21`, `WAVE_RECONCILE_SELFTEST:
  25/25`. Frozen FAIL sets: `ss-bom-only` → `ARM21` only; `wr-prefix` →
  `arm25` only. Disclosed matrix change: `arm20-cleanup-removed` (an existing
  defect that edits arm20's fixture cleanup inside the selftest function) now
  also fails `arm25` beside its own arm20 — still killed.
- Sourced on **S310** (Python `inspect` docs, `inspect.getsource`).

## Gate

New row this round (opened 2026-11-04):

- **S310 — Python 3.15, inspect (https://docs.python.org/3.15/library/inspect.html)**,
  fetched 2026-11-04 (HTTP date `Wed, 04 Nov 2026 08:40:02 GMT`, 221,837 B,
  sha256 `7570b79d9d6211df9b796e0e19d454fce2b44c0de471f99b9bb9b106735dfdcc`,
  snapshot `.ufo/evidence/round-81/sources/inspect315.html`, headers
  `inspect315.headers`). Located quote: "Return the text of the source code for
  an object." (11 words, page line 1183). Tier A, status `mined`, recheck
  365d, `used-by corpus/lessons/round-81.md`. The page's `getsourcelines`
  sibling returns `(lines, lineno)` — a shape the pin does not need, and the
  two are different documents of the same page.
- Admit/reject pair for the closure to spot-check: **admit** S310 (above);
  **reject** none this round — the round's second source question was S289
  re-opened, which is a re-open, not a new row (CORPUS.md rule 2: the same
  document already held).

Re-opened row (same round, old → new logged):

- **S289 — Git, git-cat-file documentation**, re-opened 2026-11-04
  (08:40:02 GMT): `https://git-scm.com/docs/git-cat-file`, 79,488 B, sha256
  `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910`,
  byte-identical to the round-79/80 snapshot. Fetch receipt committed at
  `.ufo/evidence/round-81/sources/s289-cat-file.html` + `.headers` (round-80
  closure defect D5: the re-open was prose with no committed bytes).
  `used-by` old → new: `corpus/knowledge/executor-source-binding.md,
  corpus/lessons/round-61.md, corpus/lessons/round-64.md,
  corpus/lessons/round-79.md` → the same plus `corpus/lessons/round-80.md,
  corpus/lessons/round-81.md` (round-80 closure defect D4: the round-80 Gate
  logged this edit and it never landed).

Census: `scripts/sources-census.sh validate --root … tameshi` exit 0 before
(`assimilation/census-before.txt`) and after.

## Mistakes

1. **A record described a state the repository did not carry — six times in
   one round.** Class: stale self-description (the lane's record asserting an
   artifact, token or edit that the committed bytes do not hold). Evidence
   pointer: the round-80 non-author closure's §6 register
   (`corpus/lessons/round-80-verifier-spotcheck.md` §6.1–6.6): two 7 MB
   receipts cited but untracked, one committed as a 0-byte blob, a
   before-state token pair that is not the cited receipt's, an S289 `used-by`
   edit claimed and not landed, a re-open with no fetch receipt, and a missing
   Search-log note. Captured-by: none — every standing instrument measured a
   *tool's* figure (`selfstate-freshness`, `registry-figure-bind`,
   `quoted-line-exists`, `receipt-exists`), and no counter read a closure's
   routed-defect prose as a population. Fix: `tools/defect-bind.py` +
   `tools/defect-bind.json` (criterion 78); shown able to fail — the base tip
   reads `rows=6 closed=0 open=6` exit 1, each row naming its missing artifact,
   and the selftest refuses an empty manifest, a duplicate id, a `../` path and
   an unresolvable rev before any row effect.
2. **Two standing-sweep rows measured pre-settlement tool bytes.** Class: pin
   drift (a "settled bytes" claim whose pin names an older revision than the
   bytes it measures). Evidence pointer: round-80 closure defect D3 — two
   round-80 rows pinned the declaration commit `ae591d5a` while their
   instruments changed at `01ca77cd`, and the audit found a third
   (`receipt-exists-selftest`, pin `21ef81e9` vs last change `4af6695f`).
   Captured-by: none — the sweep compared *figures* (which happened to agree),
   never the instrument's bytes at the pin against the tip's. Fix:
   `--pin-audit` + arms 18–20; shown able to fail — the base manifest reads
   `settled=20 stale=3` exit 1, arm18 measures a stale row and its settled
   twin, and arm20 refuses a single-row audit as evidence for the population.

## Wave findings

(to be filled from the wave's settled seat reports)
