# tameshi round 60 — lesson (hyaku run 13, 2026-10-30)

L1 `TameshiR60` (attempt 1; fresh-start round under run 13). Base
`9806562c7efc816bd979923e702ef39bc41cade7` (= origin/master, clean tree);
contract `.ufo/evidence/round-60/contract.json`; plan `plans/round-60.plan.md`;
counter `tools/executor-source-pin-measure.py` (installed); freeze
`.ufo/evidence/round-60/freeze.json`; tool commit (measured)
`da2ae6b361de2d6294c6324a02ae141ff6cb482f`.

Fresh-start duty: the last three rejected closures were read before the
claims were declared — round 57 (honest stop, operator wrap-up; no freeze, no
counter scored), round 58 (not admitted: an unpinned claimant executor forged
the C2 tallies; C3 measured), round 59 (honest stop: the frozen counter was
cheat-passable — a fingerprint cheat scored 24/24) — plus the outside
discernment check `corpus/lessons/round-59-verifier-spotcheck.md`, whose
§6 routed eight defects. Every claim below is aimed at one of those routed
defects and is sized so a do-nothing control cannot reach it.

## Claims

- **C1 (operability, capability re-certification; sourced S290).** The
  round-59 executor-source-pin capability is re-certified on an installed,
  discriminating counter: `tools/executor-source-pin-measure.py` — 8 shuffled
  class cells (`equal`, `unrelated`, `execbit`, `changed`, `missing`,
  `symlink`, `corrupt`, `unresolvable`) over 5 declared paths in ONE tool
  invocation per cell, per-run nonce fixtures, an empty-blob declared path,
  and a corrupt cell expecting exit 2. At the round's final lane revision the
  amended `tools/executor-source-pin.py` v2 scores `passed=8/8
  C1_R60_PASS=true`, and every control arm scores `C1_R60_PASS=false`:
  do-nothing tool-absent 0/8, the unfixed v1 tool 7/8 (only the `corrupt`
  cell failing — the red-before for the exit-2 reconciliation), always-accept
  3/8, fingerprint 3/8, sequence 3/8 (3–5/8 across runs, order-shuffled),
  hash-only 3/8, first-path-only 6/8, empty-blob-unsound 4/8. Closes round-59
  routed defects 1, 2, 4 and 7. The claim's before-state is the round-59
  verdict: the counter that certified the capability was cheat-passable, so
  the capability was **not admitted** (honest stop, closure round 59).
- **C2 (calibration).** The round-59 closure's routed defects and
  uncaptured mistakes become tree-checkable records: `corpus/routed-defects.json`
  carries rows `R59.1`–`R59.8` (7 `fixed` with in-tree receipts, `R59.4`
  `open` with its reason), `corpus/QUALITY.md` carries five new criteria
  (111–115), one per round-59 mistake whose `captured-by` was `none`, each
  citing this lesson; `SCORECARD.md` carries the annotation `not admitted
  (honest stop, closure round 59)` on the round-59 C1 capability row and a
  saturation premise restated on the scored axes; and the cold-read precheck
  run at (base `9806562c…` → the round's final revision) is recorded with
  `lost=0`.

## Gate

- Sourced rows opened this round (URL, access date, located quote, word
  count, what it grounds):
  - **S290** — Python, `secrets` module documentation,
    https://docs.python.org/3/library/secrets.html, accessed 2026-10-30
    (HTTP date Fri, 30 Oct 2026 18:38:28 GMT; 36,411 B; extract
    `.ufo/evidence/round-60/sources/s290-secrets.html`). Located quote
    (§module abstract, first paragraph, 25 words): "The secrets module is
    used for generating cryptographically strong random numbers suitable for
    managing data such as passwords, account authentication, security tokens,
    and related secrets." It grounds the per-run nonce fixture design: a
    counter whose fixtures change every run cannot be defeated by a
    content-recognition cheat. `used-by`:
    `corpus/knowledge/executor-source-binding.md`.
  - **S291** — Git, index-format documentation,
    https://git-scm.com/docs/index-format, accessed 2026-10-30 (HTTP date
    Fri, 30 Oct 2026 18:39:52 GMT; extract
    `.ufo/evidence/round-60/sources/s291-indexformat.html`). Located quote
    (§cache entry layout, 9-bit unix permission, 22 words): "9-bit unix
    permission. Only 0755 and 0644 are valid for regular files. Symbolic
    links and gitlinks have value 0 in this field." It grounds the exec-bit
    boundary decision: exactly two permission values for regular files
    (modes 100644/100755) and a symlink as a distinct type, so mode is not
    bound beyond regular-ness. `used-by`:
    `corpus/knowledge/executor-source-binding.md`.
- Rejected this round, with reason and flip condition:
  - **git-ls-tree documentation as the mode ground** —
    https://git-scm.com/docs/git-ls-tree, opened 2026-10-30 (extract
    `.ufo/evidence/round-60/sources/s291-lstree.html`). REJECTED: the page
    documents `%(objectmode)` as a format placeholder but enumerates no
    octal mode values, so it cannot ground "regular modes 100644/100755,
    symlink 120000"; flip: a page that enumerates the mode values would
    carry the row instead. The row was re-targeted to `index-format` (S291),
    which does enumerate them.
- Id collision check before the append: `grep -c 'S290' corpus/SOURCES.md`
  → 0, `grep -c 'S291' corpus/SOURCES.md` → 0 (registry maximum was S289);
  `grep -c 'library/secrets\.html\|docs/git-ls-tree\|docs/git-hash-object'
  corpus/SOURCES.md` → 1 (S103, `git-hash-object` — an existing row, so the
  oid-equality ground was re-used, not duplicated).
- Status / recheck / used-by changes to existing rows, old → new: **S103**
  used-by `corpus/lessons/round-36.md` → `corpus/lessons/round-36.md,
  corpus/knowledge/executor-source-binding.md` (the content-addressed
  oid-equality ground now backs the binding entry too). No other row
  changed; no row was rewritten.
- Census before (round start): `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → exit 0, 149 rows, 16 W04
  duplicate-URL warnings and 1 W01 (S101) — all pre-existing. Census after
  the SOURCES append: exit 0, **151 rows**, malformed rows 0, warning set
  unchanged (no new W04/W01 from S290/S291).
- Assimilation: **none** — no `merge/tameshi/` package entry was adopted this
  round; the round's claims are counter-discrimination and routed-defect
  dispositions, and the staged package holds no entry on either ground (the
  package's own counter/mutation entries concern mutation-score semantics,
  not counter discrimination). No shokuknow registry row was appended.
- `considerthese/`: mined — proposal 4/5 of `considerthese/2026-10-28.md` were
  read; the one that fits this round's claims cheaply (a receipt-existence
  linter for records — the discipline criterion 108 already encodes) is
  carried into the ledger work as criterion 111–115 rather than as a new
  claim; the other was not applicable. Reflection is a pointer, not evidence.

## Mistakes

1. **A frozen counter publishes its fixtures, so a content-recognition
   cheat can meet the target (class: non-discriminating counter).** Evidence:
   `corpus/lessons/round-59.md` `## Mistakes` 1 and
   `.ufo/evidence/round-59/controls/cheat-cheat-fp.out`
   (`passed=24/24 C1_R59_PASS=true` for a cheat that never reads `--trusted`).
   Captured-by: **none** in round 59 (its freeze controls were tool-absent
   and do-nothing only). Fix: the round-60 counter derives every fixture
   byte and commit message from a per-run nonce (S290) and shuffles the class
   order, so the same cheat scores 3/8
   (`.ufo/evidence/round-60/controls/ctl-fingerprint.out`); criterion 111 now
   requires a cheat family before a counter certifies anything.
2. **A counter's invocation shape can under-cover the tool's declared
   interface (class: coverage hole in the predicate).** Evidence:
   `corpus/lessons/round-59.md` `## Mistakes` 2 — the round-59 counter
   invoked `--path` once per call, so a first-path-only strawman scored
   24/24. Captured-by: none. Fix: the round-60 counter declares all five
   paths in ONE invocation per cell, with the `symlink` cell on paths[1] and
   the `corrupt` cell on paths[3]; the first-path-only strawman now scores
   6/8 (`.ufo/evidence/round-60/controls/ctl-first-path-only.out`);
   criterion 112.
3. **A quote's word count drifts between the lesson and the source (class:
   reference-drift).** Evidence: `corpus/lessons/round-59.md` `## Gate`
   records the S289 quote as 17 words; the quote is 18 words (the round-59
   spot-check §6 item 8 names it). Captured-by: the QUALITY rule that a
   quote names its location — present, but it does not require the count.
   Fix: the round-59 lesson is left byte-unchanged (append-only) and the
   erratum is recorded here; every Gate quote in this lesson carries its
   word count (25 for S290, 22 for S291).
4. **A counter's control family can be strong while its positive arm is
   untested against the tool's own plumbing failures (class: coverage hole
   in the predicate).** Evidence: the round-59 counter had no cell in which
   the tool's blob read fails at plumbing level, so the tool mapped that
   arm to DRIFT (exit 1) while its own decision table said exit 2 — the
   mismatch the round-59 spot-check §6 item 7 named. Captured-by: none. Fix:
   the round-60 counter's `corrupt` cell deletes the candidate's loose blob
   object and expects exit 2; the unfixed tool scores 7/8 with only that
   cell failing (`.ufo/evidence/round-60/controls/v1-tool-red.out`), and the
   v2 tool maps the arm to `EXECUTOR_SOURCE_UNAVAILABLE`
   (`tools/executor-source-pin.py:249-266`).
5. **A freeze that digests nonce-bearing receipts can never re-verify against
   the tree (class: reference-drift).** Evidence: `.ufo/evidence/round-60/freeze.json`
   digests 16 files, 7 of which are counter receipts whose bytes carry a
   per-run nonce and a shuffled class order. After the control family was
   re-run at the certified revision, a naive re-verification of the freeze
   reports 7 mismatches and cannot distinguish a re-run receipt from a
   tampered instrument. Captured-by: none — the freeze has no instrument/receipt
   distinction to test. Fix: `.ufo/evidence/round-60/freeze-verify.py`
   classifies the comparison and reports `FREEZE_VERIFY instrument=10/10
   receipt=9/16 verdict=INSTRUMENT-OK (receipts re-run)`
   (`.ufo/evidence/round-60/freeze-verify.json`): every frozen INSTRUMENT
   digest still matches, and the pre-data receipt bytes remain recoverable
   from the freeze commit (`git show da2ae6b361de2d6294c6324a02ae141ff6cb482f:.ufo/evidence/round-60/controls/ctl-fingerprint.out`).
   Criterion 117 now requires the distinction.

## Verdicts

- **C1, measured.** Before (the round-59 verdict): the counter that
  certified the capability admitted a fingerprint cheat at 24/24, so the
  capability was **not admitted** (honest stop, closure round 59). After, at
  `da2ae6b361de2d6294c6324a02ae141ff6cb482f`: `passed=8/8
  C1_R60_PASS=true`, exit 0 (`.ufo/evidence/round-60/after/cert.out`), and a
  second run at the same revision with a different nonce and class order also
  scores 8/8 (`.ufo/evidence/round-60/after/cert-repeat.out`). Controls:
  do-nothing tool-absent 0/8, v1 tool 7/8 (corrupt only), always-accept
  3/8, fingerprint 3/8, sequence 3/8, hash-only 3/8, first-path-only 6/8,
  empty-blob-unsound 4/8 — every arm `C1_R60_PASS=false`
  (`.ufo/evidence/round-60/controls/`). The counter's digest is frozen
  (`.ufo/evidence/round-60/freeze.json`, sha256 `c136561d…`) and matches the
  committed bytes. **Admission remains an operator ruling**: the capability
  row is annotated `not admitted (honest stop, closure round 59)` and the
  round-60 row is written as "lane demonstrated; admission pending".
- **C2, measured.** Before (base `9806562c…`): R59.* ledger rows 0, QUALITY
  criteria citing the round-59 lesson 0, the SCORECARD annotation 0 — the
  do-nothing control receipt. After: 8 rows (7 `fixed`, 1 `open` with its
  reason), 6 QUALITY citations of `corpus/lessons/round-59.md` (criteria
  111–115 plus the section preamble), 2 matches for the annotation string,
  and the cold-read precheck recorded at the round's final revision with
  `lost=0`.

## Next-round carry

- Author-independent trust for the binding itself stays outside the lane's
  claims (F11's remaining ground); the lane does not claim it.
- `R59.4` stays open: the seat-result completeness check belongs to the
  wave validator in the ufo-fsd-alpha checkout, outside this lane's write
  scope; the lane-side criterion 114 is the mitigation.
- The counter's remaining honest limits: one fixture repo per run, one
  declared path spelling set, and no packed-object or promisor-partial
  failure modes (the `corrupt` cell deletes a loose object only).
