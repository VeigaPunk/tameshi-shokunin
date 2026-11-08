# Round 96 — the sealed audit and the hardened pins tool

Lane `tameshi`, round 96 (2026-11-08). Base `c8de77f3de0fd4bf619ebe78fa0b28adaf320d3e`.
Claims: C1 calibration (the sealed audit: rev identity and hostile-PATH refusal) and C2 operability (the hardened pins tool: atomic write, symlink and empty-lane refusal). Frozen
before data in `plans/round-96.plan.md` and `.ufo/waves/round-96/claims.json`.

## Gate

Sources re-opened this round (all four fetched live by this round's scout, 2026-11-08; the
snapshots under `.ufo/evidence/round-96/sources/` are byte-identical to the round-95 bodies,
so the anchors below name the round-96 path). Each sid line carries its located quote on the
same line — the counter's `located_quotes` collects a quoted span only from a line naming
its sid. Line numbers are in the canonical lane rendering
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py` `strip_tags`: script/style blocks and comments
removed, each tag replaced by one space, entities unescaped, lines right-trimmed); a quote
that wraps is located by its **span**. Word counts are `len(quote.split())`.

- S320 sha256sum(1) `https://man.archlinux.org/man/sha256sum.1.en` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 12:21:54 GMT; `.ufo/evidence/round-96/sources/s320.html` sha256 `b968bc09…`), line 88: "Print or check SHA256 (256-bit) checksums." (6 words) — the digest the counter's `SELF_SHA256` pin computes and the audit compares is a sha256 of the counter bytes.
- S320 sha256sum(1), line 116: "don't output anything, status code shows success" (7 words) — why the checker reads the exit code, never prose, when it runs `git rev-parse --verify --quiet` for the revision identity (A2). These three sentences were paraphrased in the registry's `teaches` cell (round-95 spot-check D4); quoting them verbatim here closes the gap on the reading side.
- S321 GFM Tables `https://github.github.com/gfm/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 12:21:54 GMT; `.ufo/evidence/round-96/sources/s321.html` sha256 `b153d814…`), line 4403: "The delimiter row consists of cells whose only content are hyphens" (11 words) — one hyphen is a legal delimiter cell, the round-95 A5 rule the successor reader keeps.
- S321 GFM Tables, lines 4496-4497: "The table is broken at the first empty line, or beginning of another block-level structure" (15 words) — a following indented chunk ends a table, so it cannot extend an earlier verdict table.
- S322 CommonMark 0.31.2 Fenced code blocks `https://spec.commonmark.org/0.31.2/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 12:21:54 GMT; `.ufo/evidence/round-96/sources/s322.html` sha256 `c85f56cc…`), lines 2618-2619: "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." (17 words) — a fence opens literal text, the declared limit the reader already held.
- S323 CommonMark 0.31.2 Indented code blocks `https://spec.commonmark.org/0.31.2/` (the same page bytes as S322; same fetch) lines 2358-2359: "An indented code block is composed of one or more indented chunks separated by blank lines." (16 words) — an indented chunk is literal text, so a verdict row presented inside one is not a keyed row.

Rejected this round: **one**. `https://docs.github.com/en/rest/commits/commits#get-a-commit`
(GitHub REST API "Get a commit", opened 2026-11-08, HTTP date Sun, 08 Nov 2026 12:24:50 GMT,
547 847 B, sha256 `fc8e1251…`, located line 733: "Returns the commit's SHA-1 hash. You can use
this endpoint to check if a remote reference's SHA-1 hash is the same as your local
reference's SHA-1 hash") is **refused** for the revision-identity ground: it is a hosted-API
statement about an `ETag` comparison, not the `<rev>` grammar or the `^{commit}`
dereference the seal needs; those grounds are already held at tier A (`S091`, `S062`).
Flip condition: a future claim specifically about GitHub's REST API (the
`application/vnd.github.sha` media type as an ETag) admits it as a tier-B vendor row
anchored at §Get a commit. Rows re-opened: S320, S321, S322, S323 — status unchanged
(`mined`), `used-by` gains `corpus/lessons/round-96.md`. Row added: none. Registry rows
183, mined 149, queued 23, rejected 11 — unchanged; census exit 0 before and after.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **wrong-path default**: the successor checker's `COUNTER` constant still named round 95's `measure-v95.py`, which does not exist in round 96, so every run of the documented command died `counter-absent-at-rev` — kill rule (d)-class, found by the round's own reviewer before any positive existed. | `w1/R96R1.md` FALSIFIES-WORDING #1 (`R96R1-probe1-positive-default.out`: `DISPOSITION_SETUP counter-absent-at-rev`, exit 2); the constant was at `conjunct-disposition-v96.py:53`. | the plan's own counter command (`plans/round-96.plan.md` §C1) was never executed at the freeze — no pre-freeze run of the documented command existed. | A1 repaired the constant; QUALITY 173 now requires the printed instrument line to name the revision and the digest the verdict was read at, so a wrong default is visible in the receipt. |
| M2 | **inherited label**: the round-95 to round-96 copy carried `C1_R95_`, `round-95/` paths and a `--rev` string into the new instruments; the path rewrites were mechanical and left `measure-v95.py` and a `v95` name in prose and code. | `git show 10d8fa5d:.ufo/evidence/round-96/conjunct-disposition-v96.py` line 53; `w1/R96C1.md` C1.1. | none — the copy step had no post-copy assertion that every `round-95`/`v95` token had been replaced or deliberately kept. | A1; the round-96 instruments now carry a `ROUND = 96` constant and the receipts prove the run (`counter_sha=` on every graded body, validated by the driver since A9). |
| M3 | **no-op selftest cases**: the two print statements added for the new cases asserted nothing that could fail, so kill rule (c) was tripped by the shipped selftest itself. | `w1/R96C1.md` C1.8 (`selftest.txt` 13/13 while a reverted seal would still pass); the block was `selftest()` cases 12-13. | the plan's kill rule (c) was written but not read against the new cases before the freeze. | A5 rewrote them to run the real main path — `hostile-path-cheat` under a poisoned `PATH`, `branch-revspec-cheat` with `--rev master` — and both now fail if the seal or the guard is removed. |
| M4 | **renderer drift**: the Gate's cited line numbers did not follow from the rendering the Gate itself named. The first landed preamble said the numbers come from a rendering where each tag is replaced by one space; under *that* rendering the S321/S322/S323 quotes sit at 4512/4605/2723/2463, while the lesson printed 4403/4496/2618/2358 — the numbers the canonical lane renderer (script/style and comments removed as well) produces. A reader following the lesson's own stated convention landed 109 lines off on every quote with a script block before it. | `w1/SC1-lesson.md` and `w1/SC1-sources.append.md` (renderer-variants and locate receipts); the round-95 spot-check's D1. | the round-95 D1 rule existed but was checked against the numbers, not against the preamble that claimed to produce them. | the preamble now names the canonical renderer (`.ufo/waves/round-93/w1/R93S1-tagstrip.py`), wrapped quotes are located by span, and the registry's S323 `anchor` cell moves `2355` -> `2358` (QUALITY 172: a cited line is one the named rendering shows carrying the sentence). |

## Registry changes

No row added this round (no uncovered ground was opened). One cell changed: the S323 row's
`anchor` column, `line 2355` -> `line 2358`, with the convention parenthetical corrected to
the renderer that produces it (M4; one cell of one row, 11 columns preserved, census exit 0
after). S320-S323 carry `used-by` for this lesson, appended in `corpus/SOURCES.md` before the freeze (`scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin tameshi` exit 0; rows 183, mined 149, queued
23, rejected 11, unchanged before -> after).

## Measurements

Every number below is a line a committed receipt printed at the revision named.

- **C1 positive at the records revision `8ed9c526`.**
  `.ufo/evidence/round-96/landing/c1-positive.out` reads
  `DISPOSITION_INSTRUMENT rev=8ed9c5262bd2f36f3cc8a64550897f4d1adb3a3b
  sha256=69ee68b6… conjuncts=19` and
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`, exit 0.
- **C1 rev refusals.** `c1-rev-branch.out` (`--rev master`) and `c1-rev-empty.out`
  (`--rev ''`) each print `DISPOSITION_SETUP rev-not-a-commit-id` exit 2;
  `c1-rev-unresolvable.out` (`--rev deadbeef…`) prints `DISPOSITION_SETUP rev-unresolvable`
  exit 2.
- **C1 hostile PATH.** `c1-hostile-path.out`: a `git` shim at the head of `PATH` that exits
  99; the checker prints `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=17`
  exit 1 (17 `receipt-absent-at-rev` findings on a lane with no committed receipts) — never
  green, and the shim is never the binary that answered (`GIT=/usr/bin/git`).
- **C1 forge matrix.** `landing/forge-matrix.txt` prints `summary: 8 checks, 0 failed`:
  `forge-handwritten` exit 1 `receipt-absent-at-rev figure` (round-95 checker exit 0),
  `forge-counter-sha` exit 1 `receipt-counter-sha-mismatch mismatched0` (round-95 exit 0),
  `forge-replace-ref` exit 2 `DISPOSITION_SETUP replace-refs-present` (round-95 executes the
  substituted blob).
- **C1 nowork + selftest.** `c2-nowork-base.out` at base `c8de77f3` prints
  `DISPOSITION_SETUP counter-absent-at-rev` exit 2; `c1-nowork-base.out` prints
  `C1_SETUP spec-absent-at-rev` exit 2; `c2-selftest.out` prints
  `DISPOSITION_SELFTEST: 13/13 pass` exit 0, including
  `SELFTEST hostile-path-cheat PASS exit=2 (identical to honest PATH)` and
  `SELFTEST branch-revspec-cheat PASS exit=2 (rev-not-a-commit-id)`.
- **C2 pins tool.** `c2-pins-positive.out`: `PINS_WRITTEN …/pins.json`, `PINS_CHECK OK`;
  `c2-pins-empty-lane.out`: `PINS_SETUP lane-empty` exit 2; `c2-pins-symlink.out`:
  `PINS_SETUP pins-symlink-refused` exit 2 with `target_before == target_after ==
  9660b330…`.
- **C2 driver.** `c2-rerun-plant.out` prints `pos-real MATCH exit=0` and
  `C1_CONTROLS states=1 matched=1 mismatches=0 missing=0`, exit 0: the planted receipt
  (`w1/R96R2-out-rerun9-planted.out`, `counter_sha=000000…0`, `exit=1`,
  `pass=false verdict_tables=false`) sat beside the driver's own write and was not graded.
  `c2-receipt-symlink.out`: the same, with `pos-real.out` a symlink to an outside file
  (`FORGED` untouched). `c2-outdir-symlink.out`: `outdir-symlink-refused`, exit 1.
- **C2 battery.** The full run at the records revision prints
  `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`, exit 0
  (`.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt`); every one of the fifty
  receipts carries a `counter_sha=` line equal to the counter blob
  (`69ee68b6…`, or the mutant's own digest for `D01`-`D05`).
- **Census.** `census-before.txt` and `census-after.txt` both exit 0; rows 183, mined 149,
  queued 23, rejected 11, unchanged.
