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

- Before (base tip `56a0129f`, base manifest; the instrument was declared at
  `1b115ba0`):
  `DEFECT_BIND: rows=6 closed=0 open=6 unexpected=6` exit 1
  (`.ufo/evidence/round-81/controls/c1-before.txt`).
- Do-nothing control: the base tip itself — appending nothing leaves all six
  rows open, each naming its missing artifact.
- Landed: `tools/defect-bind.py` (five row kinds: `tree-paths`, `tree-bytes`,
  `receipt-tokens`, `sources-cell`, `doc-contains`; manifest-level refusals before any
  row effect, a row's own unreadable input a setup refusal at that row),
  `tools/defect-bind.json` (six rows over D1/D2/D4/D5/D6), and the
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
  sweep stays green (`SELFSTATE: rows=23 match=21 stale=2 unexpected=0`, exit
  0 — the two stale rows are the declared red arms, `unexpected=0`);
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
  an object." (10 words, raw page line 1193). Tier A, status `mined`, recheck
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
  byte-identical to the round-79 snapshot (`cmp` exit 0); the round-80 re-open
  left no committed bytes, and that absence is D5. Fetch receipt committed at
  `.ufo/evidence/round-81/sources/s289-cat-file.html` + `.headers` (round-80
  closure defect D5: the re-open was prose with no committed bytes).
  `used-by` old → new: `corpus/knowledge/executor-source-binding.md,
  corpus/lessons/round-61.md, corpus/lessons/round-64.md,
  corpus/lessons/round-79.md` → the same plus `corpus/lessons/round-80.md,
  corpus/lessons/round-81.md` (round-80 closure defect D4: the round-80 Gate
  logged this edit and it never landed).

Corrections of record (append-only, logged old → new; found by the wave's
source scout T81W1SC1):

- **S310 quote metadata** — old `(11 words, page line 1183)` → new `(10 words,
  page line 1193)`. The quote is 10 words and the page-line convention this
  registry uses is the 1-based RAW HTML line (verified against S308 220,
  S309 999, S304 4157); 1183 was the rendered-text line, the end of the
  `getsourcelines` paragraph.
- **S307 quote metadata** — old `(8 words, page lines 308-311)` → new
  `(7 words, page lines 308-311)`. Pre-existing (round-78) row, corrected here
  because it shows the word-count token was not a stable instrument: the count
  is a manual claim in the row, and nothing re-derives it.

- **Capability-row figure (wave scout T81W1SC2 B3)** — the live
  `## Capabilities` row `wave-record reconciliation` printed
  `WAVE_RECONCILE_SELFTEST: 23/23 pass`, one arm-count behind at the base and
  two behind after this round's arms; no standing monitor reads that cell
  (`registry-figure-bind`'s doc surface is SKILL.md). Old → new:
  `23/23 pass` → `25/25 pass`.
- **Spec headers (T81W1SC2 B5/B6)** — both mutant specs' header comments named
  their old populations (13 and 4 defects); the round-81 defect lines were
  appended but the header still described the older set. Each header now names
  its round-81 defect and the new population (14 and 5).

Census: `scripts/sources-census.sh validate --root … tameshi` verdict line
`tameshi	ok	…/corpus/SOURCES.md` and exit 0 before
(`.ufo/waves/round-81/assimilation/census-before.txt`) and after
(`.ufo/evidence/round-81/census-after.txt`).

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
2. **Three standing-sweep rows measured pre-settlement tool bytes.** Class: pin
   drift (a "settled bytes" claim whose pin names an older revision than the
   bytes it measures). Evidence pointer: round-80 closure defect D3 — two
   round-80 rows pinned the declaration commit `ae591d5a` while their
   instruments changed at `01ca77cd`, and the audit found a third
   (`receipt-exists-selftest`, pin `21ef81e9` vs last change `4af6695f`).
   Captured-by: none — the sweep compared *figures* (which happened to agree),
   never the instrument's bytes at the pin against the tip's. Fix:
   `--pin-audit` + arms 18–20 (criterion 79); shown able to fail — the base manifest reads
   `settled=20 stale=3` exit 1, arm18 measures a stale row and its settled
   twin, and arm20 refuses a single-row audit as evidence for the population.

## Wave findings

One v1 wave (`w1`), 13 seats. The findings below are the settled seat reports
under `.ufo/waves/round-81/w1/`; every claim was re-measured after the wave's
changes and the numbers in this lesson are the re-measured ones.

1. **Source scout (T81W1SC1) — two quote-metadata defects in the registry.**
   S310's quote is 10 words on the raw page line 1193, not 11 words on 1183
   (1183 was a rendered-text line, the end of the `getsourcelines` paragraph;
   four prior rows use the raw basis). The round's own row and the pre-existing
   S307 row (8 → 7 words) were corrected old → new above. It also verified
   S289's live bytes byte-identical to the committed snapshot and ran a full
   `used-by` resolution (137/137 mined rows resolve; 0 untracked). Instrument
   note worth keeping: a working-tree `grep` during a sibling write returned
   `0` and `4` on two consecutive runs — only committed blobs are a
   measurement while the wave writes.
2. **Surface scout (T81W1SC2) — the declaration commit turned four surfaces
   red.** `REGISTRY_BIND: rows=7 match=3 stale=4` exit 1 and `registry-check`
   `differs` on both selftest rows at `1b115ba0`, while the base tip read
   `match=7`: the arm moves were already in the declaration's instrument
   bytes, so the landing had to restore both surfaces. Its three census tables
   (live surfaces / coupled surfaces / must-not-change traps) named the
   SCORECARD capability figure (`WAVE_RECONCILE_SELFTEST: 23/23`, one behind
   even at base, bound by no monitor) and both spec headers; all three were
   corrected. Its trap register kept the C1 predicate's `24/24`/`17/17` tokens
   untouched. The landing was re-measured: `REGISTRY_BIND: rows=7 match=7`.
3. **Connector (T81W1CN1) — the nearest siblings and one unclosed hole.** The
   routed-defect binder's closest relative is souji's
   `souji-citation-reconcile.py` (same job, one row kind); no sibling lane has
   a standing sweep of *pins*, and no lane has the C3 device (a self-asserting
   arm that fails when the selftest's own text changes). Its D-CN3 is the
   real one: `defect-bind.py` reads its manifest from the path given, so the
   kill rule's "no row removed / `expect` relaxed / population narrowed"
   clause is enforced by the frozen commit and the round's manifest-binding
   receipt, not by the instrument — souji already filed `--register-rev` for
   this class. D-CN1 (a failed selftest returns 1, the same code as an open
   register), D-CN2 (two arm-naming families), D-CN4 (two pin doctrines under
   one word) and D-CN5 (the declaration carries C3's repair) are recorded as
   routed observations; the C3 fragility note (the digest is a hostage of the
   selftest function's layout) is disclosed.
4. **Reviewer (T81W1R1) — C1's independent base state and five weakness
   classes.** Its own six-probe script over the base tree reproduced
   `open=6`. It found the two narrow rows: D1a and D5 are `tree-paths` rows,
   and `git cat-file -e` accepts a tree or an empty blob, so a directory or a
   0-byte stand-in would measure `closed` (the `min_bytes` guard exists only
   on D1b); and D2's instrument is narrower than the plan's sentence (it
   checks the span in the doc and the tokens in the receipt, not the tokens in
   the span). Its other three classes passed (no exit-0-on-setup-error, no
   never-failing `expect` arm, byte-level receipt-token comparison), and it
   recorded that a manifest without a digest cannot prove its own population.
   Because the manifest is frozen at the declaration, these are routed to
   round 82 rather than edited mid-round.
5. **Executor (T81W1E2) — C2 reproduced and probed.** Its independent
   `cat-file` audit reproduced `rows=23 settled=20 stale=3` row-for-row with
   the same three stale rows, and its scratch re-pin reached `settled=23
   stale=0` at both the base and declaration tips while the standing sweep
   stayed byte-identical (`rows=23 match=21 stale=2 unexpected=0`). Edge
   probes: tag names are refused as pins (`instrument-rev-unresolvable`),
   tag object shas are accepted, directories at a pin or tip die as
   `blob-unreadable` (exit 2) rather than `pin-path-absent`, and a zero-row
   manifest is refused.
6. **Mutation-tester (T81W1M1) — seven instrument mutants, seven kills, and a
   class gap.** On `defect-bind.py`: state inversion (killed by A10 only),
   `expect` defaulting to the measured state (killed by six arms), the span
   check deleted (A4 only) and `min_bytes` ignored (A3 only); on
   `selfstate-freshness.py`: `settled = True`, tip-vs-tip comparison (both
   killed by ARM18 + ARM20) and the digest constant replaced (ARM21 only).
   Two of the mutants would have made the *frozen before-state* certify
   (`rows=6 ... unexpected=0` exit 0 and `rows=23 settled=23 stale=0` exit 0):
   the suite is the only thing standing between the counter and a false
   certification, which is why C3's class matters. Its hardening note: the
   `defect-bind.py` selftest text is not pinned, so the C3 class does not yet
   cover the round's newest instrument — round 82's move.
7. **Critic (T81W1C1) — a counterexample against the D2 row.** It built a
   committed candidate that deletes the erratum body, keeping only its heading,
   and the C1 counter still read `closed=6` exit 0: `check_receipt_tokens`
   tested the span's presence in the doc and the tokens' presence in the
   receipt, never the tokens inside the span, while the plan's own sentence
   requires the span to carry them. The reviewer (T81W1R1 §3 D2) found the same
   narrowness independently. The check was made faithful to the declared
   predicate (each token must occur in the span bytes AND in the receipt
   bytes; the detail names which side failed), and the manifest's span was
   extended to the sentence pair that actually carries `24/24` and `17/17`.
   The predicate, the six-row population and the kill rule are unchanged; the
   before-state was re-measured at the base tip with the corrected instrument
   (`controls/c1-before-instrument-v2.txt`, `open=6`, exit 1) and the
   after-state re-measured at the tip (`closed=6`, exit 0). This is a
   correction toward the declaration, not a rule change: the instrument now
   implements the sentence the plan froze.
8. **Executor (T81W1E1) — C1 rebuilt from the plan text, plus cheat
   vectors.** It rebuilt the six-row register from the plan alone and
   reproduced the base reading byte-identically (`open=6`, exit 1) at both
   `1b115ba0` and the round-80 tip, and reproduced the after-state `closed=6`
   exit 0 at `1415fb65` with both the committed and the declaration
   instrument, the manifest bytes unchanged. Its cheat register found one
   real vector worth naming: a `tree-bytes` row is satisfied by a **symlink
   entry whose target string is large enough** (the blob is the link target,
   so `min_bytes` reads the target length, never the artifact); the live D1b
   path is a real 7.1 MB blob today, so the row is honest, but a
   mode-blind `min_bytes` is not a content bind. Also routed: case/whitespace
   in row ids, the `sources-cell` empty-cell fallback, `id_ref`/`source_id`
   divergence, and the absent manifest pin. None falsifies C1 as declared; all
   are next-round counter axes.
9. **Executor (T81W1E3) — the C3 pin rebuilt independently, with its
   measured limits.** Its own domain-separated pin (different arm names,
   different digest construction) reproduces the class exactly: the unmodified
   base suites stay green, `ss-bom-only` fails only its own pin arm
   (`17/18`), `wr-prefix` fails only its own (`24/25`), and both survive the
   unpinned suites. Three limits were demonstrated by execution, not argued:
   (a) over-kill — a vacuous comment inside the selftest fails the pin;
   (b) single-edit misses live *outside* the digested region (a module-level
   constant or a `BOM` edit stays green: the pin covers the function's source,
   not the module); (c) the two-edit evasion (weaken an arm and recompute the
   constant) is real and reproducible — exactly the boundary the plan
   declares. This is the honest coverage boundary of any
   `getsource(selftest)` pin and is carried as a limit, not smoothed.
10. **Scribe (T81W1S1) — the record diffed against the receipts.** Its deltas
   were applied: the criterion number (78/79 now exist in `corpus/QUALITY.md`),
   "two" → "three" stale rows, the sweep's exact figure with its red-arm
   clause, the round-79-only snapshot wording, the census verdict line, the
   before-measurement revision, and the LOG's unverified cause sentence for
   the 0-byte blob (rewritten as a symptom, cause not established).

**Dead seats (reported, not hidden).** T81W1E4 never produced a report: its
result carries its last working text (mid-clone, extracting the spec diffs) and
no artifact; T81W1SN1 returned an empty output and no report. Both died in
flight; the wave's `w1-results.json` records 13 seats with 11 reports. No seat
was replaced and no seat's absence changes a claim: E4's battery rebuild is
covered by R2's independent 38-run matrix and by the L1's own landed batteries;
SN1's security surface is covered in part by E1's cheat register and R1's
source audit (the symlink-`min_bytes` vector), and the remainder is a named
next-round attack.
