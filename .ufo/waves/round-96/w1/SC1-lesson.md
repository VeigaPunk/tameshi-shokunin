# SC1 — `corpus/lessons/round-96.md` draft (round 96)

**Seat:** R96SC1 (scribe). **Lane:** `tameshi`. **Mode:** read-only — nothing under
`corpus/` was written; this file is a draft for the L1 to integrate.

**Read first.** This draft is written against the lane at `ffb41c8f` (the records commit that
landed the round-96 lesson, QUALITY 173-174 and the LOG entry). Where it differs from the
landed lesson, the difference is stated in the note under each section and carries its
receipt. Two things drive the differences: **D1** (the round-95 verifier's routed defect —
Gate line numbers off by 3–4 under the Gate's own stated renderer) and a **convention
mismatch** the D1 fix introduced, measured below.

Every number below is a line a committed receipt printed, or is a measurement this seat made
and filed in this wave directory with its command. Numbers that are not yet measured are
written `TODO-not-measured`.

---

## Gate

Sources re-opened this round (all four fetched live by this round's scout, 2026-11-08; the
snapshots under `.ufo/evidence/round-96/sources/` are byte-identical to the round-95 bodies,
so the anchors below name the round-96 path). Each sid line carries its located quote on the
same line — the counter's `located_quotes` collects a quoted span only from a line naming
its sid. **Line numbers are in the canonical lane rendering**
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py`, `strip_tags`: script/style blocks and comments
removed, each tag replaced by one space, entities unescaped, lines right-trimmed); a quote
that wraps is located by its **span**. Word counts are `len(quote.split())`.

> **Note on the renderer convention (this is the correction D1 asked for, and it changes two
> things).** The landed lesson's preamble states the convention as *"each tag replaced by one
> space, entities unescaped, lines right-trimmed"* — which is **not** the convention that
> produces the lesson's own numbers. Under that stated convention the S321/S322/S323 quotes
> sit at 4512/4605/2723/2463, not at 4403/4496/2618/2358 (receipt:
> `.ufo/waves/round-96/w1/R96SC1-renderer-variants.txt`; canonical vs stated-convention spans
> for every quote below are in `.ufo/waves/round-96/w1/R96SC1-defect-check.txt`). The
> landed lesson therefore satisfies D1's *numbers* while still violating D1's *rule* — the
> stated convention still cannot produce the cited line. The preamble above names the
> canonical renderer, which does produce every number below, and quotes that carry a
> two-line span are located by the span rather than by a bare start line. The locator
> receipt for this seat's independent re-measurement is
> `.ufo/waves/round-96/w1/R96SC1-locate.txt`; the scout's independent locator receipt is
> `.ufo/waves/round-96/w1/R96S1-quotes.txt` and it agrees on every line.

- S320 sha256sum(1) `https://man.archlinux.org/man/sha256sum.1.en` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 12:21:54 GMT; `.ufo/evidence/round-96/sources/s320.html` sha256 `b968bc09…`), line 88: "Print or check SHA256 (256-bit) checksums." (6 words) — the digest the counter's `SELF_SHA256` pin computes and the audit compares is a sha256 of the counter bytes.
- S320 sha256sum(1), line 116: "don't output anything, status code shows success" (7 words) — why the checker reads the exit code, never prose, when it runs `git rev-parse --verify --quiet` for the revision identity (A2). These three sentences were paraphrased in the registry's `teaches` cell (D4); quoting them verbatim here closes that gap on the reading side.
- S321 GFM Tables `https://github.github.com/gfm/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 12:21:54 GMT; `.ufo/evidence/round-96/sources/s321.html` sha256 `b153d814…`), line 4403: "The delimiter row consists of cells whose only content are hyphens" (11 words) — one hyphen is a legal delimiter cell, the round-95 A5 rule the successor reader keeps.
- S321 GFM Tables, lines 4395-4396: "a single header row, a delimiter row separating the header from the data" (13 words) — the table shape the reader keys, which is why an indented row outside a table is not a verdict row.
- S321 GFM Tables, lines 4496-4497: "The table is broken at the first empty line, or beginning of another block-level structure" (15 words) — a following indented chunk ends a table, so it cannot extend an earlier verdict table.
- S322 CommonMark 0.31.2 Fenced code blocks `https://spec.commonmark.org/0.31.2/` fetched 2026-11-08 (HTTP date Sun, 08 Nov 2026 12:21:54 GMT; `.ufo/evidence/round-96/sources/s322.html` sha256 `c85f56cc…`), lines 2618-2619: "A fenced code block begins with a code fence, preceded by up to three spaces of indentation." (17 words) — a fence opens literal text, the declared limit the reader already held.
- S323 CommonMark 0.31.2 Indented code blocks `https://spec.commonmark.org/0.31.2/` (the same page bytes as S322; same fetch) lines 2358-2359: "An indented code block is composed of one or more indented chunks separated by blank lines." (16 words) — an indented chunk is literal text, so a verdict row presented inside one is not a keyed row.

Every quote above is ≤25 words, is present in the snapshot's `norm_text` (the counter's
`source` conjunct), and is located by a line or line span under the convention the preamble
names. This seat's re-measurement of all of them, with word counts and spans:
`.ufo/waves/round-96/w1/R96SC1-locate.txt`; the same facts independently from the scout:
`.ufo/waves/round-96/w1/R96S1-quotes.txt`.

Rejected this round: **one**. `https://docs.github.com/en/rest/commits/commits#get-a-commit`
(GitHub REST API "Get a commit", opened 2026-11-08, HTTP date Sun, 08 Nov 2026 12:24:50 GMT,
547 847 B, sha256 `fc8e1251…`, located line 733: "Returns the commit's SHA-1 hash. You can use
this endpoint to check if a remote reference's SHA-1 hash is the same as your local
reference's SHA-1 hash") is **refused** for the revision-identity ground: it is a hosted-API
statement about an `ETag` comparison, not the `<rev>` grammar or the `^{commit}`
dereference the seal needs; those grounds are already held at tier A (`S091`, `S062`).
Flip condition: a future claim specifically about GitHub's REST API (the
`application/vnd.github.sha` media type as an ETag) admits it as a tier-B vendor row
anchored at §Get a commit. The refusal and its three measured reasons are in the scout's
receipt `.ufo/waves/round-96/w1/R96S1.md` §4 and its sweep table (line 318). Rows re-opened:
S320, S321, S322, S323 — status unchanged (`mined`), `used-by` gains
`corpus/lessons/round-96.md`. Row added: none. Registry rows 183, mined 149, queued 23,
rejected 11 — unchanged; census exit 0 before and after
(`.ufo/waves/round-96/census-before.txt`, `.ufo/waves/round-96/census-after.txt`).

> **Note on the S323 registry anchor.** The registry row's own `anchor` cell still prints
> `line 2355` for the sentence this lesson locates at 2358-2359 — the D1 drift, still live in
> `corpus/SOURCES.md` at `ffb41c8f`. `2355` is blank under the canonical renderer, and under
> the anchor cell's own stated convention the sentence is at 2463-2464, so the printed number
> is wrong under both readings (receipt: `.ufo/waves/round-96/w1/R96SC1-defect-check.txt`,
> §DEFECT 3). The exact 11-column old→new for that one cell is in `SC1-sources.append.md`.
> Until the L1 lands it, this lesson and the registry disagree about S323's line by 3, and
> that disagreement is named here rather than left silent.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M4 | **number-drift**: the Gate's cited line numbers did not follow from the renderer the Gate itself named. The landed lesson's preamble says the line numbers come from a rendering where *each tag is replaced by one space*, but under that rendering the S321/S322/S323 quotes are at 4512/4605/2723/2463 — the lesson prints 4403/4496/2618/2358, which are the numbers the *canonical* lane renderer (script/style and comments removed as well) produces. A reader who followed the lesson's own stated convention landed 109–105 lines off, on every quote that has a `<script>`/`<style>` block before it. | `corpus/lessons/round-96.md:12` (the preamble) against the cited lines at `corpus/lessons/round-96.md:16-21`; the two conventions measured over the same committed bytes in `.ufo/waves/round-96/w1/R96SC1-renderer-variants.txt` (canonical vs stated) and `.ufo/waves/round-96/w1/R96SC1-defect-check.txt` §DEFECT 1 (per-quote `vA_carries` / `vB_carries`); the routed defect is `corpus/lessons/round-95-verifier-spotcheck.md:172-183` (D1) and its row table at line 122. | QUALITY 172 — *"a cited line is a line the record's named snapshot rendering shows carrying the sentence"* — which round 95 wrote **against this exact defect** and which the round-96 Gate still violates: D1 fixed the numbers and left the convention that contradicts them. | the Gate preamble now names the canonical renderer (`.ufo/waves/round-93/w1/R93S1-tagstrip.py` `strip_tags`) and every quote that wraps is located by its span. The fix counts because it can fail: the two renderers disagree on these quotes by 105-109 lines (`.ufo/waves/round-96/w1/R96SC1-renderer-variants.txt`), so a preamble that names the wrong one is now visibly inconsistent with its own numbers. QUALITY 173-174 do not cover it; the rule that would is *a record that cites a line names the renderer that produced it, and a quote that wraps is located by its span*. |

> **Note on the landed M1-M3.** The landed lesson's three mistakes (wrong-path default,
> inherited label, no-op selftest cases) are sound and stay as M1-M3. This seat's row is
> **M4** — additional, not a replacement: it is the defect class D1 named in round 95 and
> that the round-96 landing did not close, found by re-measuring the landed Gate against
> both conventions rather than by accepting its numbers. It is reported here because the L1
> integrates, and an extra mistake row in the same table is a row the L1 may merge or drop —
> that call is the L1's. If the L1 keeps only one of the four, keep M4: it is the only one
> whose fix is still open in the landed bytes.

## Registry changes

No row added this round (no uncovered ground was opened). S320-S323 carry `used-by` for
this lesson, appended in `corpus/SOURCES.md` before the freeze (`scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin tameshi` exit 0; rows 183, mined 149, queued
23, rejected 11, unchanged before -> after).

One **cell** changes: the S323 row's `anchor` column, `line 2355` → `line 2358`, with the
convention parenthetical corrected to the renderer that produces it. The exact 11-column
old→new is in `SC1-sources.append.md`. S320, S321 and S322 need no change: S321's anchor
(`line 4496`) and S322's anchor (`line 2613`, the §4.5 heading its anchor cell names) are
correct as landed, and S320's anchor cites no line at all.

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
- **C2 driver.** The driver grades **its own write**: `c2-rerun-plant.out` prints
  `pos-real MATCH exit=0` and `C1_CONTROLS states=1 matched=1 mismatches=0 missing=0`,
  exit 0, while the planted receipt it did **not** grade is carried by
  `w1/R96R2-out-rerun9-planted.out` (`counter_sha=000000…0`, `exit=1`,
  `C1_CONJUNCTS pass=false verdict_tables=false`); a symlinked receipt is refused —
  `w1/R96R2-out-symlink-summary.txt` prints `pos-real SYMLINK-REFUSED`, and
  `c2-receipt-symlink.out` records the same run with the outside file's sha256
  (`outside_sha=8dfa71ca…`). `c2-outdir-symlink.out`: `outdir-symlink-refused`, exit 1.
- **C2 battery.** The full run at the records revision prints
  `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`, exit 0 — **re-derived by this
  seat** by re-grading all fifty committed receipts with the driver's own `grade()` and its
  own expectations table (`.ufo/waves/round-96/w1/R96SC1-regrade.txt`); every one of the
  fifty receipts carries a `counter_sha=` line equal to the counter blob
  (`69ee68b6…`, or the mutant's own digest for `D01`-`D05`).
- **Census.** `census-before.txt` and `census-after.txt` both exit 0; rows 183, mined 149,
  queued 23, rejected 11, unchanged.

> **Note on the battery receipt pointer.** The landed lesson names
> `.ufo/evidence/round-96/pre-freeze/controls/C1-summary.txt` for the
> `states=50 matched=50` line. That path is **not** in the tree
> (`git ls-files .ufo/evidence/round-96/pre-freeze/controls/` lists the fifty
> `<state>.out` receipts and no summary file — the driver writes its summary into a scratch
> outdir), so the pointer as landed does not resolve. This seat therefore **re-derived the
> number**: re-grading all fifty committed receipts with the driver's own `grade()` and its
> own expectations table, at a clone of the records revision, prints
> `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`
> (`.ufo/waves/round-96/w1/R96SC1-regrade.txt`) — the number is sound, its pointer is not.
> For contrast, the wave replay `.ufo/waves/round-96/w1/R96E4-battery-replay.out` prints
> `independent_match=44/50 mismatches=6` for the **pre-A6** driver and names the six
> mismatches (`D01`-`D05`, `replace-honest`) — the defect A6 repaired. The L1 should land
> the summary file or point at a receipt that exists.

## Wave

13 seats (executor 4, scribe 1, scout 1, reviewer 2, critic 1, mutation-tester 1, sentinel
1, connector 1, revenger 1), read from
`.ufo/waves/round-96/w1-dispatch.json` `taskCall.tasks`; attack share 4/13 (reviewer×2,
critic, mutation-tester) = 31 % by the addendum §6 named set.
