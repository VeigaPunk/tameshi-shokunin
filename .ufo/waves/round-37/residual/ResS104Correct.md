# ResS104Correct — residual falsification of the S104 located-quote line-range correction (round 37, attempt 3)

Lane tip `ba3c35fb6c9582fcf2351c59c61661dd7a8e7400` (branch master). Target claim: S104 located-quote
range corrected old 489–493 → new 494–495 in `corpus/SOURCES.md` (row S104), `corpus/lessons/round-37.md`
(Gate correction bullet), and `LOG.md` (round-37 correction line). Attack: fetch the pinned URL and
re-derive every number from the wire, then compare against the committed bytes and the actual diff.

## Verdict

**The claim survives.** Fresh fetch of the pinned URL reproduces sha256
`f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` exactly; in those bytes
`@node ANSI-C Quoting` is at L489 and the located quote occupies L494–495; all three files carry the
correction and agree on old→new; the lesson's old→new log matches the actual `git` diff byte for byte,
with nothing else changed. No BLOCKER, no MAJOR. Two cosmetic MINOR phrasing notes, no fix required.

## Attack 1 — pinned fetch fidelity

Executed: `curl -sL 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303' -o /tmp/bashref.texi`

```
sha256sum → f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5  /tmp/bashref.texi
wc -l     → 11553 /tmp/bashref.texi        wc -c → 415804
file      → TeX document, ASCII text
```

- sha256 matches the hash claimed in the lesson bullet (`f3d37d57…2be32d5`,
  `corpus/lessons/round-37.md:12`), the LOG correction (`LOG.md:1999`), and my assignment, byte-exact.
- 11,553 lines matches the lesson bullet's "11,553 lines"; 415,804 bytes matches
  `.ufo/waves/round-37/w1/ReviewFrontierStatus.md:23` (independent same-day fetch).

## Attack 2 — line truth in the fetched bytes

Executed: `awk 'NR==489||NR==493||NR==494||NR==495{printf "%d:%s\n",NR,$0}' /tmp/bashref.texi`

```
489:@node ANSI-C Quoting
493:
494:Character sequences of the form @code{$'@var{string}'} are treated as
495:a special kind of single quotes.
```

Full block (read of :488–498): L490 `@subsubsection ANSI-C Quoting`, L491–492 the two `@cindex` lines,
L493 blank, L494–495 the quoted sentence. So:

- old range 489–493 = node header/`@cindex`/blank block — the recorded range before correction was
  indeed describing the header, not the quote;
- new range 494–495 = exactly the located quote — correct;
- "off by five" (`LOG.md:1998`) is arithmetically right (489→494 start shift +5);
- quote is verbatim after Texinfo rendering (`@code{$'@var{string}'}` → `$'string'`), matching the
  "quote itself is verbatim" claim in `LOG.md:2000`.

Word count re-derived: `printf '%s\n' "Character sequences of the form \$'string' are treated as a special kind of single quotes." | wc -w` → `15` — matches the row/lesson/LOG claim of 15 words, unchanged by the correction.

## Attack 3 — three-file agreement at HEAD `ba3c35fb`

- `corpus/SOURCES.md:113` — S104 row: URL fragment `#L494-L495`, anchor "§ANSI-C Quoting,
  `@node ANSI-C Quoting`, lines 494–495"; tier A / mined / 2026-10-24 / 365d / used-by unchanged.
- `corpus/lessons/round-37.md:12` — Gate correction bullet: old `lines 489–493` / `#L489-L493` →
  new `lines 494–495` / `#L494-L495`, sha256 `f3d37d57…2be32d5`, 11,553 lines, word count (15)
  unchanged, "the original admit bullet above stays as written" (the :7 bullet indeed still reads
  489–493 — disclosed, not a silent contradiction).
- `LOG.md:1996–2000` — append-only correction naming the old range, the new range 494–495, the
  sha256, and attribution ("Wave-1 seat ReviewSourceScope found it" — accurate:
  `.ufo/waves/round-37/w1/ReviewSourceScope.md:65-73`, independently `ScoutBashSource.md:44`).

All three name the same old value, the same new value, and the same pin. Frozen
`.ufo/evidence/round-37/contract.json` contains no line-number claim (grep `489|494` → no hits; C2
block matches on "ANSI-C" only), so the correction cannot contradict the frozen contract.

## Attack 4 — old→new log vs the actual diff

`git show 583909a -- corpus/SOURCES.md` (commit "S104 citation correction…", ancestor of HEAD —
verified `git merge-base --is-ancestor 583909a HEAD`):

- exactly 1 insertion / 1 deletion, the S104 row: `#L489-L493` → `#L494-L495` and
  `lines 489–493` → `lines 494–495`; every other row field and every other row byte-identical.
- same commit: `LOG.md` +5 (the correction bullet), `corpus/lessons/round-37.md` +1 (the Gate
  correction bullet). Nothing else in the three files changed.
- later tip commit `ba3c35f` ("end census receipt at final tip") leaves the three files untouched:
  `git diff 583909a HEAD -- LOG.md corpus/SOURCES.md corpus/lessons/round-37.md` → empty.

So the lesson's old→new log is exactly what the diff did — no silent field drift, no stale range
left in a live record. Remaining `489–493`/`#L489-L493` occurrences in the tree are only (a) the
two intentionally preserved originals (lesson:7, LOG:1984) each explicitly corrected by an
append-only bullet, and (b) frozen wave-1 seat reports describing the pre-correction state —
correctly not edited. No undisclosed live citation remains.

## Findings

- **BLOCKER: none.**
- **MAJOR: none.**
- **MINOR (cosmetic, no fix required):**
  1. `corpus/SOURCES.md:113` compressed row format reads "…`@node ANSI-C Quoting`, lines 494–495",
     which a naive parse attaches to the `@node` (actually at 489). The row convention locates the
     *quote* in that field (cf. S102/S103 rows), and the lesson bullet disambiguates
     ("`@node ANSI-C Quoting` at L489–493 and the located quote at **L494–495**");
     `.ufo/waves/round-37/w1/ReviewFrontierStatus.md:40` already suggested "node at 489, body
     494–495" phrasing. Same looseness in the lesson bullet's "@node … at L489–493" (the directive
     is only at L489; 489–493 is the header block). Informational only; changing the row again for
     phrasing would cost more than it buys.

## Residual risk / verification gaps

- Single-source fetch: my hash reproduction is one network pull from the canonical
  `cgit.git.savannah.gnu.org` host; S104 (like S097) still records no committed snapshot or digest
  in the row itself — a pre-existing, documented convention gap
  (`ReviewSourceScope.md:77-78`, `ReviewFrontierStatus.md:103-107`), not introduced by this
  correction. If the convention tightens, both rows want a committed `.texi` snapshot.
- The `#L494-L495` fragment remains GitHub-style and inert for cgit `plain/` URLs (documented,
  `ReviewFrontierStatus.md:45-47`); the prose anchor is the load-bearing locator and is now correct.
- Wave-1 frozen reports (e.g. `ConnectorSiblingOverlap.md:70,76,82`) still cite the old window as
  of their write time; they are historical evidence and were correctly left byte-identical, but a
  future reader must use the correction bullets, not the w1 reports, for the current range.
- I did not re-run the sources-census validator; the census is fragment-insensitive
  (`url_of` strips `#…`), so the correction cannot change its W04 outcome, and the final-tip
  census receipt at `ba3c35f` (exit 0, 101 rows) postdates the corrected row.

Tooling directive record: no tools installed or updated; all checks used preinstalled curl, git,
sha256sum, awk, wc, printf (read-only git only; no lane or `.ufo/state` writes except this report).
