# tameshi round 61 — lesson (hyaku run 14, 2026-11-01)

L1 `TameshiR61` (round 61; the r60 closure routed the genuine re-read remedy
here as the round's first obligation). Base
`8b0042bde0ca59aac9a23a8a707cf0902183d081` (= origin/master; the r60
verifier spot-check landing). Dispatch host: win32 (python 3.13.15, git
2.55.0.windows.3, `core.symlinks=false`). Plan carrier receipts:
`.ufo/evidence/round-61/win-host/`.

Fresh-start duty: the last three rejected closures (r58, r59, r60) and
`corpus/lessons/round-60-verifier-spotcheck.md` (read in full) were re-read
before anything was declared. Ruled out, with reasons: (a) re-attempting the
frozen precheck as-is — five completion attempts failed at ~112 min/rev
(r60 mistake 8); the remedy requires a host-feasible execution form first,
and the frozen decision code is kept unchanged; (b) claiming no-harm from
r60's lane-authored substitute — its 46-vs-50 comparison spans two revision
pairs with the attribution split unmeasured, so it cannot certify anything;
(c) extending the executor-source-pin counter family — its cross-host
demonstration is complete and admission is an operator ruling, not lane
work; (d) re-running r60 attempt-1's Linux counting commands — already
annotated host-scoped (criterion 118); the portable re-statements exist.

## Claims

- **C1 (operability, capability acquisition; sourced S293).** The frozen
  no-harm precheck gains a host-portable execution form:
  `tools/coldread-precheck-portable.py` runs the frozen round-18 decision
  code unchanged with ONLY its two per-input plumbing functions
  (`cat_file_blob`, `ls_tree_mode`) replaced by batched, cache-backed
  equivalents with spawn fallback, chunked and resumable on disk, and an
  equivalence probe that re-derives a deterministic sample through the
  original spawns (any mismatch, or an empty sample, fails the run). Before
  (base `8b0042bd`): the frozen precheck cannot produce a verdict on this
  host (75,889 ledger inputs x ~151,778 spawns/rev x 0.044 s/spawn ≈ 112
  min/rev; five failed runs — `.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`).
  After: a full measure of the base revision in 7.1 s
  (`measure-base.out`: `credited=46/64 … probe_sampled=20
  probe_mismatches=0`), and a synthetic differential in which the portable
  form and the frozen selector (spawning) produce byte-identical coldread
  section JSON at two revisions across discriminating cells — input-drift,
  exec-bit credit, symlink `input-not-blob`, `input-missing`,
  `no-ledger-entry` — `DIFFERENTIAL: PASS`
  (`.ufo/evidence/round-61/win-host/differential.stdout`).
- **C2 (calibration; the r60 remedy + closure-defect dispositions).** The
  genuine re-reads land: every one of the 18 sections that lost credit
  (46/64 at base; reasons all `input-drift:` on PROVINCE/QUALITY/SOURCES/
  README/tools edits from r60) was re-read in full by the L1 this round,
  every recorded input in its all-entry union was re-read at the pin
  revision through the batched reader, and fresh input-keyed ledger entries
  (schema `tameshi-coldread-ledger-v2`) pin the post-edit hashes with
  committed `tameshi-trace-inputs-v1` trace receipts
  (`.ufo/evidence/round-61/rekey/traces/`, ledger appended at the rekey
  commit). Then the monitor is re-run at the final revision toward lost=0.
  The closure defects land with it: D1 — the r60 first-family receipts
  (cited by the report, the lesson, criterion 119 and contract-a2-amend1,
  resolution marked `resolved: true` by pointer-sweep-a2) existed only in
  the worktree and are now committed
  (`.ufo/evidence/round-60/win-host/first-family/`, 21 files); D2 — the
  attempt-1 freeze re-run now carries its own win32-era receipt
  (`.ufo/evidence/round-61/win-host/freeze-a1-reverify.json`:
  `instrument=10/10`, 7 nonce-bearing receipts re-run, verdict
  `INSTRUMENT-OK (receipts re-run)`); D3 — the number-drift corrections are
  pinned in SCORECARD (erratum below the R60a2 rows).

## Gate

- Sourced row opened this round (URL, access date, located quote, what it
  grounds):
  - **S289 re-opened** — Git `git-cat-file` documentation,
    https://git-scm.com/docs/git-cat-file (held since r59 for its
    §DESCRIPTION/-t ground), re-fetched 2026-11-01 (HTTP date Sun,
    01 Nov 2026 09:03:03 GMT; 79,360 B; extract
    `.ufo/evidence/round-61/win-host/sources/s293-cat-file-batch.html`).
    Located quote for the re-open (§Output, `--batch` without a custom
    format, 12 words): "<oid> SP <type> SP <size> LF <contents> LF". It
    grounds the batched reader's parser: the portable precheck reads
    exactly this framing per `rev:path` spec, so the cache serves the same
    bytes the frozen per-input spawns would have returned. `used-by`
    old → new: `corpus/knowledge/executor-source-binding.md` →
    `corpus/knowledge/executor-source-binding.md, corpus/lessons/round-61.md`.
  - **S293 opened and REJECTED in the same round** — the same URL was
    first appended as a new row (only the id was checked for collisions,
    not the URL); the census flagged `W04 S293 duplicate url` and the row
    is kept as a REJECTED row per CORPUS.md rule 2 ("a rejection is
    evidence of taste"), with the S073/S103 precedent (r60 spot-check §6
    agreed with re-using a held URL instead of duplicating it) as the
    ruling. Consequence honestly carried: the day's FIRST rekey batch had
    pinned `corpus/SOURCES.md` at the pre-correction bytes, so its 18
    entries went stale when this correction landed; a SECOND batch at the
    corrected bytes supersedes them — both batches stay in the ledger
    (append-only), the superseded ones disclosed here and in the ledger
    bullet. The guard caught the lane's own record edit; that is the
    instrument working, and the correction is the round's craft.
- Id collision check before the append: `grep -c 'S293' corpus/SOURCES.md`
  → 0 at write time (registry maximum was S292) — an insufficient check:
  mistake 6 below records the class. The row carries no literal pipe (the
  census E01 lesson of r60).
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (152 rows, 16 W04 + 1 W01, all
  pre-existing) and exit 0 at round end (153 rows; receipt in the round
  report).
- Rejected this round, with reason and flip: **git `cat-file --batch-check`
  as the prefetch primitive** — opened in the same page (same extract);
  REJECTED for the receipt design because `--batch-check` returns only
  `<oid> SP <type> SP <size> LF` (no contents), and the frozen decision
  code consumes blob BYTES (`sha256` over content; trace receipts parsed
  from bytes), so a check-only prefetch would still need one spawn per
  input; flip: a design that only needs object existence/metadata would
  take `--batch-check`.

## Mistakes

1. **A cache-backed instrument can run green on broken plumbing when its
   probe cannot fail empty (class: probe-cannot-fail-empty).** Evidence:
   the first working-tree run of the batched precheck reported
   `credited=46/64` — agreeing with r60's substitute — while its ls-tree
   field parser produced an EMPTY mode map (`len(fields) < 4` against a
   3-field format) and a `'100644'` hardcode served every mode from the
   byte cache; the run's own probe line read `probe_sampled=0`, which the
   first revision treated as a vacuous pass. Captured-by: none — nothing
   required an equivalence sample to be non-empty, or forbade answering
   modes from a byte cache. Fix: the probe contract now treats
   `sampled=0` as a failure (exit 2 `equivalence` guard requires
   sampled ≥ 1 and mismatches = 0), and the mode cache serves ONLY
   real ls-tree values (any other path falls back to the frozen spawn);
   the fixed run still measures 46/64 with `probe_sampled=20
   probe_mismatches=0`, so the number survives its instrument repair.
2. **A cited evidence pointer can be marked resolved before the bytes are
   committed (class: pointer-premature-resolution; r60 closure defect D1).**
   Evidence: `pointer-sweep-a2.json` marked `A2-first-family-seq`
   `resolved: true` ("lands with the receipts commit"), but no
   `first-family/` path existed at `a205f00b` or at the r60 tip — the
   sweep's "none drifted" was false in that one case. Captured-by: the r60
   verifier spot-check (§7 D1). Fix: the 21 first-family receipt bytes
   found intact in the worktree (mtime 2026-10-31 19:41, the first scored
   family's run) are committed this round, and a fresh sweep run at the
   landing revision re-derives every pointer from committed bytes
   (`pointer-sweep-r61.json`). Rule already on file (criterion 116),
   now with its worked instance.
3. **A re-run claim can rest on another host's receipt (class:
   host-scoped-receipt; r60 closure defect D2).** Evidence: the r60
   attempt-2 lesson cited "attempt-1's freeze still `instrument=10/10
   INSTRUMENT-OK (receipts re-run)` at this tree" from attempt-1's Linux
   receipt; no win32-era re-run receipt existed. Captured-by: the r60
   verifier spot-check (§7 D2), which re-derived the claim manually
   (19/19 instrument files byte-identical). Fix: the frozen
   `freeze-verify.py` (pure python, host-portable) was executed on this
   host and its receipt committed (see C2 above) — the claim now carries
   its own receipt.
4. **Prose numbers drift when a control family changes size after the
   sentence was written (class: number-drift; r60 closure defect D3).**
   Evidence: "ten-arm red family" (r60 report; SCORECARD R60a2-C1 row)
   against EIGHT control arms declared in both contracts and landed in
   `amend1/`; the r60 report's decomposition of the C2 grep count 4 named
   a fourth item ("the no-harm note") that does not contain the phrase.
   Captured-by: the r60 verifier spot-check (§7 D3). Fix: the SCORECARD
   erratum below the R60a2 rows pins the corrected family size and the
   exact decomposition (`grep -n 'counting command host-scoped (linux)'
   SCORECARD.md` at `49ddecf1` → lines 2921 (R60-C1 row), 2922 (R60-C2
   row), 2978 (attempt-2 "What landed" sentence), 2994 (the R60a2-C2 row
   quoting the pattern itself)); the raw count 4 was correct throughout.
5. **A row's URL, not just its id, must be checked against held rows
   before appending (class: incomplete-collision-check).** Evidence: S293
   was appended this round after `grep -c 'S293'` → 0, and the census
   immediately flagged `W04 S293 duplicate url git-scm.com/docs/git-cat-file
   across scopes` — the page was held as S289 (r59). Captured-by: the
   census gate itself (the same round). Fix: S293 re-stated `rejected`
   (kept as the rejection record), S289 re-opened with `used-by` extended
   old → new (logged above), and the sourcery rule this lesson carries:
   the pre-append check is `grep -c '<url-path>'` over the registry, not
   the id. The rekey cost: the SOURCES correction staled batch 1's pins
   and forced the superseding batch (Gate and Verdicts above) — the guard
   pricing a one-line registry fix at an 18-entry rekey is the system
   working as designed.
6. **A full-page re-read can still find untouched prose drift years later
   (class: prose-spacing-drift).** Evidence: this round's genuine re-read
   of SKILL.md found two pre-existing spacing defects in the round-21
   registry section — "unchanged from33d03b7" and "retain the199-entry
   prefix" (both read past three prior full-page cold-reads). Captured-by:
   this round's re-read (entry minor_gaps=2,
   `.ufo/evidence/round-61/rekey/traces/section-18.json`). Fix: recorded
   here; the page is append-only, so the text stands as written and this
   erratum is the correction of record.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the question is routed at `.ufo/l0-questions.md` (tameshi | round-60,
  routing with option (b)) and stands unanswered — this was again an
  L1-only round, disclosed here. The falsification surface is the
  committed instruments: the differential receipt (frozen selector vs
  portable form, byte-for-byte), the spawn-equivalence probes inside every
  precheck receipt, and the receipts themselves — every one re-runnable by
  the closure judge from the repo alone.
- The re-read receipts name their reader honestly: L1-author source
  re-reads at a pinned revision, input-keyed credit only — the same
  population the round-53..58 rekeys produced; they are not blind
  re-verification and are not cited as such anywhere.

## Verdicts

- **C1, measured.** Before: no precheck verdict possible on this host
  (~112 min/rev; five failed runs). After, at the round's tool commit:
  `python -I tools/coldread-precheck-portable.py --repo . --rev <rev>
  --work <scratch dir>` → `COLDREAD_PORTABLE rev=<rev> credited=46/64
  elapsed=7.1s probe_sampled=20 probe_mismatches=0`, exit 0, plus
  `DIFFERENTIAL: PASS` (frozen selector == portable form at two revisions
  over discriminating cells). The batched form runs the frozen decision
  code unchanged; only `cat_file_blob`/`ls_tree_mode` are cache-backed
  with spawn fallback.
- **C2, measured at the rekey commits (receipts land in the following
  commit — receipt-after-subject ordering, the r60 precedent).** Before:
  46/64 credited at base; the 18 uncredited sections all fail on
  `input-drift:` of r60-edited record files
  (`.ufo/evidence/round-61/win-host/rekey-plan.json`,
  `union-plan.json`). After: TWO batches, both landed (append-only):
  batch 1 at `72d36ae1…` (18 entries, 11,004 input pins at the records
  commit `19d7e996…`) measured
  `COLDREAD_PRECHECK floor=8b0042bde0ca floor_credited=46
  cand=72d36ae1aff7 cand_credited=64 lost=0 ok` + `box3_full_page=true`
  + `EQUIVALENCE … mismatches=0` (receipt `precheck-final.{out,json}`);
  batch 1 was then superseded by the S293/S289 SOURCES correction
  (Gate above) — its SOURCES pins went stale by the correction landing,
  exactly the drift the guard exists to catch — and batch 2 at the
  corrected bytes (18 entries, same unions, new trace receipts
  `traces-2/`) re-established credit at the corrected tip; the batch-2
  guard receipt lands with the receipts commit. The superseded batch-1
  entries stay in the ledger as landed history, disclosed here; at the
  final tip they read `input-drift:corpus/SOURCES.md` — non-crediting,
  non-vetoing, and true.

## Next-round carry

- The portable precheck is an EXECUTION FORM of the frozen instrument, not
  a replacement: wherever the frozen precheck can run (the Linux host), it
  remains the decider; the portable form's probe + differential receipts
  are what license its use here.
- The rekey entries pin `corpus/SOURCES.md` at this round's bytes; any
  later round that edits SOURCES/PROVINCE/QUALITY/README/tools re-stales
  the 18 sections and owes its own rekey — that is the instrument working,
  not a defect.
- r60's routed L0 question (win32 wave surface) stands; the round-59
  capability row stays "lane demonstrated; admission pending".

## Erratum — appended round 62 (2026-11-01; r61 verifier spot-check routed defects RD1–RD4)

Appended only; the text above stands as written (lessons are append-only).
All sites re-verified against committed bytes in round 62 before this
append.

- **RD1:** line 32 ("any mismatch, or an empty sample, fails the run") and
  the mistake-1 fix (lines 123–124: "exit 2 `equivalence` guard requires
  sampled ≥ 1 and mismatches = 0") described a gate absent from the shipped
  bytes at this round's base (`git show ed3a66c2:tools/coldread-precheck-portable.py
  | grep -c "probe_failed\|sampled.*< 1"` → 0; `main()` gated only on
  `mismatches`). Fixed in round 62 (`probe_failed` gate on both measure
  modes + fail-closed arms; `corpus/lessons/round-62.md`).
- **RD2:** line 58 ("21 files") and line 134 ("the 21 first-family receipt
  bytes") — the committed tree holds **20**
  (`git ls-tree -r 19d7e996 | grep -c first-family/` → 20; also 20 at the
  r62 base and tip). LOG, SCORECARD and the `19d7e996` commit subject carry
  no count (re-verified; the spot-check's site list over-stated those).
- **RD3:** the "2,215-line SKILL.md" figure (fleet r61 report) is 2,214
  (`git show ed3a66c2:SKILL.md | wc -l` → 2214; same at base and pin).
- **RD4:** line 75 labels the S289 re-open quote "12 words"; the quoted
  framing "<oid> SP <type> SP <size> LF <contents> LF" is 8
  whitespace-separated tokens. The same wrong label sits in the
  `corpus/SOURCES.md` round-61 registry note (line 539), left unedited — a
  registry byte change would re-stale the batch-2 rekey pins and owe an
  18-section re-read rekey; the SCORECARD erratum and this append are the
  corrections of record there.
