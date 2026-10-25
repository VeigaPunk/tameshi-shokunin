seat: ExecJudge08

# Round-45 w2 — C1 falsify verdicts: S008, S056, S104

Independent re-judgment. I am not the author of any of these entries (authors: ExecRows03, ExecRows07, ExecRows20). Every fetch below is mine, run 2026-10-25 from `/tmp/tameshi-r45-ExecJudge08/`, against the row's own URL.

S008 agree — reviewer ExecJudge08 — live sha256 `aaf66df0…` equals the entry `raw_sha256` and the committed snapshot's gunzip sha256, and the 23-token quote sits in the arXiv 2102.11378**v2** abstract body (between `Abstract:` at extract offset 546 and `Comments:` at 2458, quote at 1698) stating per-line/per-review mutant filtering and historical-operator selection, which is what the row's teaches cell claims.
S056 agree — reviewer ExecJudge08 — live sha256 `a31331da…` equals the entry `raw_sha256`, the committed snapshot's gunzip sha256 and the row's own recorded prefix `a31331da…`, and the 21-token quote is the opening body sentence of the `CONDITIONALS_BOUNDARY` section immediately before its Original/Mutated table, stating that relational operators are replaced by their boundary counterpart — exactly the teaches claim.
S104 agree — reviewer ExecJudge08 — live sha256 `f3d37d57…` equals the entry `raw_sha256` and the committed snapshot's gunzip sha256, and the 15-token quote sits at snapshot lines **494-495**, exactly the row's `#L494-L495` anchor inside `@node ANSI-C Quoting`, with lines 496-498 stating that backslash-escaped characters are replaced as specified by the ANSI C standard — supporting the "single-quoted region while honoring backslash escapes" teaches claim.

## Inputs and integrity

- Ledger at the assigned commit is the ledger at HEAD: `git diff --stat ad5942c… 1f9266a… -- .ufo/evidence/round-45/freshness/ledger.json .ufo/evidence/round-45/freshness/sources/ corpus/SOURCES.md` printed nothing (exit 0); `git show ad5942c:./.ufo/evidence/round-45/freshness/ledger.json | sha256sum` = `433a624bf8cdd42ccf2ea2a818aa0bdc40dd2c77cd636e1121d0aa51eb5a9913` = `sha256sum .ufo/evidence/round-45/freshness/ledger.json`.
- Registry rows (`grep -nE '^ {0,3}\| S(008|056|104) ' corpus/SOURCES.md`): line 19 S008 (mined, A, scope "Google's diff-scoped mutation testing at code review", anchor "Abstract, arXiv:2102.11378v2"), line 65 S056 (mined, A, scope "PIT's own operator definitions for Java bytecode mutation…", anchor "§CONDITIONALS_BOUNDARY @ page fetched 2026-10-20 … sha256 a31331da…"), line 113 S104 (mined, A, scope "Bash ANSI-C `$'...'` quoting and backslash-escaped single quotes…", anchor "§ANSI-C Quoting, `@node ANSI-C Quoting`, lines 494-495 @ Bash 5.3 commit `b8c60bc9…`"). All three: id <= S160, status `mined`, http(s) URL present. Population-valid.
- Ledger URLs are byte-identical to the rows' first http(s) URLs, including S104's `#L494-L495` fragment.

## Provenance (sha256 comparison lines)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S###.live '<row url>'   # exit 0 for all three
$ sha256sum S008.live S056.live S104.live
aaf66df07f514232c0eb1cdf010c9db99a1a9e886c9a6a3f933c54fb32eceeed  S008.live   (45029 bytes)
a31331daf89f246f3e02c0da92578d4ad2163c53741c3700437e75b9a1602da2  S056.live   (67033 bytes)
f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5  S104.live  (415804 bytes)
```

| row | live sha256 | entry raw_sha256 | `gunzip -c <entry.snapshot> \| sha256sum` | verdict |
|---|---|---|---|---|
| S008 | `aaf66df07f514232c0eb1cdf010c9db99a1a9e886c9a6a3f933c54fb32eceeed` | same | same | equal — provenance confirmed |
| S056 | `a31331daf89f246f3e02c0da92578d4ad2163c53741c3700437e75b9a1602da2` | same | same | equal — provenance confirmed |
| S104 | `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` | same | same | equal — provenance confirmed |

No dynamic-page drift for any of the three, so the "different chrome → require the quote in today's live text" branch did not need to fire; as a belt-and-braces check I still confirmed the quote survives extraction of my own live fetch for S008 (`quote in S008.live == True`; for S056/S104 the raw bytes are HTML/texi with intervening tags and line wraps, so presence is only meaningful post-extraction — see context below).

## Context (quote located in `--extract` output)

Extraction: `python3 …/freshness/measure.py --extract /tmp/tameshi-r45-ExecJudge08/S###.snap` — exit 0 for all three; normalized text is a single line (5486 / 18403 / 413378 chars).

- **S008** at offset 1698, inside the abstract (`Abstract:` 546 < 1698 < `Comments:` 2458; `Submission history` 2786, `References` 3247 — the quote is well before all navigation/reference chrome). Version marker `2102.11378v2` present, matching the row's anchor. Context:
  `…(2) Mutants are filtered, «removing mutants that are likely to be irrelevant to developers, and limiting the number of mutants per line and per code review process»; (3) Mutants are selected based on the historical performance of mutation operators, further eliminating irrelevant mutants and improving mutant quality. Evaluation in a code-review-based setting with more than 24,000 developers on more than 1,000 projects shows…`
  All four teaches sub-claims are covered by the surrounding abstract sentence (diff-scoped/incremental at code review in item (1), per-line and per-review capping in the quote, historical-operator selection in item (3), 24,000 developers / 1,000 projects in the closing sentence). Not a title, nav, footer or bare fragment.
- **S056** at offset 2283, body of the operator documentation: `…Conditionals Boundary Mutator (CONDITIONALS_BOUNDARY) Active by default «The conditionals boundary mutator replaces the relational operators <, <=, >, >= with their boundary counterpart as per the table below.» Original conditional Mutated conditional < <= …` The quote is the section's opening statement and is followed by the real Original/Mutated table, so it is body content near the row's `§CONDITIONALS_BOUNDARY` anchor, not a table fragment. The "as per the table below" tail does not truncate the claim — the claim (relational operator → boundary counterpart) is stated in full before it.
- **S104** at `S104.snap` lines 494-495 (`grep -n 'are treated as' S104.snap` → `494:Character sequences of the form @code{$'@var{string}'} are treated as`), i.e. exactly the row's `#L494-L495` anchor. Context:
  `@node ANSI-C Quoting @subsubsection ANSI-C Quoting @cindex quoting, ANSI @cindex dollar-single quote quoting «Character sequences of the form @code{$'@var{string}'} are treated as a special kind of single quotes.» The sequence expands to @var{string}, with backslash-escaped characters in @var{string} replaced as specified by the ANSI C standard. Backslash escape sequences, if present, are decoded as follows: …`
  The quote states the "single-quoted region" half of teaches and the immediately following lines (496-498) state the "honoring backslash escapes" half, so the entry does not rest on vocabulary overlap alone.

## Independent predicate cross-checks

- Token counts (whitespace tokens): S008 23, S056 21, S104 15 — all inside the 6-25 bound.
- Not copied from the row: for each row, `quote in <each SOURCES.md cell>` is False for every cell (checked by splitting the row on `|`), so none of the three quotes was lifted from the row's own scope/anchor/teaches text.
- Shared content words with scope+anchor+teaches (stop-worded): S008 `code, developers, line, mutants, review` (5); S056 `boundary, conditionals, counterpart, relational` (4); S104 `quotes, single` (2 — meets the >= 2 threshold at the minimum, which is acceptable but worth noting).
- Counter machinery corroboration (allowed `--check` form, not the deciding run):
  ```
  $ python3 .ufo/evidence/round-45/freshness/measure.py --lane <lane> --rev 3310e7be803516ca5934b4e949d91bcec824b179 \
      --check S###.json --snapdir /tmp/tameshi-r45-ExecJudge08/raw
  CHECK S008 verified ok   (exit 0)
  CHECK S056 verified ok   (exit 0)
  CHECK S104 verified ok   (exit 0)
  ```
  (Fragments are copies of the ledger entries; snapshots are `gunzip -c <committed .raw.gz>` byte-for-byte, named `S###.raw` in the snapdir. First attempt used `S###.snap` names and the counter returned `CHECK S### invalid snapshot absent` — a naming artifact of my scratch dir, not a data defect.)

## Verdict artifact

`/tmp/tameshi-r45-ExecJudge08/reviews.json` — three reviews, all `verdict: "agree"`, `reviewer: "ExecJudge08"`, `report: ".ufo/waves/round-45/w2/ExecJudge08.md"`. All three rows count toward C1 from this seat's side; no dispute raised.

## Bounds / tooling

- Read-only on the lane except this report file; no git add/commit/stash/checkout/switch/reset/pull/push, no jj command, nothing written under /home/vgpnk/Projects/shokuknow or the fleet repo. All scratch under `/tmp/tameshi-r45-ExecJudge08/`.
- No tool installs or updates this seat. No subagent dispatch.

## Risks

- S104 meets the shared-content-word threshold at exactly 2 (`single`, `quotes`); the substance is carried by the adjacent lines 496-498 rather than by the 15-token quote alone. I still agree, but a stricter reader could call the quote thin — the claim is fully supported by the node, not by the quote's word overlap.
- S056's quote ends "as per the table below", a pointer to the table that follows; the sentence states the replacement fully before the pointer, so I do not treat it as truncated.
