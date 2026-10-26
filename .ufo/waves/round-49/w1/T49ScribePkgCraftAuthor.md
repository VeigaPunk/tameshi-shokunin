# T49ScribePkgCraftAuthor — assimilation triage of `pbt-generator-craft-author.md` (theme F10, round 49)

**Verdict: REFUSE as written.** Decisive ground is content, not standing: the entry's lead
inference rests on a sentence the source does not say, and its second inference asserts a
claim the lane's own held rows contradict. It is fixable only by re-scoping it into an entry
the lane already has a stronger carrier for (flip condition below).

## Item

- Candidate: `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/pbt-generator-craft-author.md`
  sha256 `f866c0c832a577c3c5bba0e05c7d2f8ba4fb0a126273afd44d1c1be75f733f28`, 42 lines
  (`sha256sum` / `wc -l`, 2026-10-26).
- Read-only source package: merge report says the package wrote nothing into the lane
  (`/home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md:3`).
- Theme F10 in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-49/contract.json`
  (`frontier_step.assimilation`): three package entries judged per entry, ≥1 admit and ≥1
  reject. This seat judges **only** `pbt-generator-craft-author.md`; the other two
  (`pbt-generator-as-fixture.md`, `r4-quickcheck-primary-correction.md`) are siblings' items.
  No claim is decided here and no counter was run.

## Gates

| gate | verdict | evidence |
|---|---|---|
| PROVINCE scope | **pass** | F10 is the lane's own frontier (`corpus/README.md:87`); a generator for a named fixture gate is the province's verification-fixture craft (`PROVINCE.md:1-6`). No product domain, no sibling gate code. |
| QUALITY bar | **fail** | criteria 1–3 (`corpus/QUALITY.md:3-6`) and criterion 10 clause 2 (`corpus/QUALITY.md:27-31`) — findings F1, F2, F3, F5, F6 below. |
| ground not already held | **pass formally, fails in substance** | No admitted entry carries `ground: F10` — `grep -rln '^ground: F10' corpus/knowledge/` prints nothing at base. But the round's C2 pilot is taking that ground (`contract.json` `claims.C2`), and the candidate's novel claim is contradicted by held rows F4. |
| CORPUS rule 1 (re-open every source it cites) | **done by this seat; the entry's own recheck cannot reproduce** | S170 re-opened 2026-10-26, PDF sha256 `35dddba5…`, 18 pages; all four quoted strings present (receipt `T49ScribePkgCraftAuthor.s170-reopen.txt`). The entry's line-4 recheck command returns `0` (F5). |
| CORPUS "a count carries its command" / quote location | **fail** | F2 (dangling `S116`), F5 (recheck count), F6 (undeclared line-break fold). |
| CORPUS rule 4 (expansion = admitted entries on *uncovered* ground) | **fail** | F7 (same thesis as the sibling F10 entry, which carries stronger sources). |

## Findings

Every command below was run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless a
path is absolute.

### F1 — decisive: the lead inference rests on a sentence S170 does not say

`pbt-generator-craft-author.md:23-27` states, as observation:

> "S170's subject is stateful code and large projects, not toy examples."

S170's abstract says the opposite: "This paper introduces Quviq QuickCheck, and in particular
the extensions made for testing stateful code, **via a toy example in C**."
(`pdftotext -layout` of the re-opened PDF, abstract lines 20-21; receipt line
`21: … via a toy example in C.`).

The entry then builds its headline recommendation on that premise — "the interesting generator
is one that reaches *stateful* fixture behaviour … not one that samples a flat input domain"
(`:25-28`). A misquoted premise under an `Inference:` label is still a false observation
(QUALITY 3: observation, inference and unknown stay separate; QUALITY 2: every claim carries
a measured anchor).

### F2 — the entry's only lane-internal example cites an id that exists nowhere

`pbt-generator-craft-author.md:28-30`: "The round-1 `S116` row's pattern — a spec property
converted into a Hypothesis property that kills a named mutant — is the same move at smaller
scale."

- `grep -nE '^\|[[:space:]]*S116[[:space:]]*\|' corpus/SOURCES.md` → no output. The lane registry
  holds 128 rows, ids `S001`–`S268` (`grep -oE '^\| S[0-9]{3,}' corpus/SOURCES.md | tr -d '| ' | sort -V | sed -n '1p;$p'`).
- The staged package cannot supply it: its ids are `S153`–`S255`
  (`grep -oE '^\| S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md | sort -V | sed -n '1p;$p'`).
- It never existed here: `git log --oneline -S'S116' -- corpus/SOURCES.md` and
  `git log --oneline -S'S116' -- corpus/` both print nothing.
- `S116` does exist in *other* lanes' registries, where it names unrelated objects
  (`grep -hE '^\|[[:space:]]*S116[[:space:]]*\|' */corpus/SOURCES.md` from
  `/home/vgpnk/Projects/shokunin` prints kumitate's Temporal Visibility, kaidoku's unblob
  formats, mado's CPython `functools` reference; `… | grep -icE 'property|hypothesis|quickcheck|generator'` → `0`).

So the sentence anchors to a foreign id space and resolves to no object in this lane. The
worked instance it supplies is the entry's only concrete tie to the lane's own method; without
it the recommendation has no lane instance at all.

### F3 — an internal warning is attributed to the QUALITY bar that is not in it

`pbt-generator-craft-author.md:33-36`: "claiming the library is the contribution would repeat
the mistake the lane's own QUALITY bar warns about."

`grep -niE 'property|generator|pbt|hypothesis' corpus/QUALITY.md` returns exactly two lines,
both the criterion-88 text "a claim whose property is 'runs the code'" (`corpus/QUALITY.md:739,741`)
— nothing about generators, libraries, or what counts as a contribution. `grep -niE 'library|contribution|interchangeab' corpus/QUALITY.md`
prints nothing. The cited warning does not exist (QUALITY 2).

### F4 — the second inference contradicts ground the lane already holds

`pbt-generator-craft-author.md:31-36` concludes "the generator library is interchangeable".
Three rows on the same ground say generation is where the cost is:

- `corpus/SOURCES.md:29` (S019, tier A, ICSE 2024, 30 interviews): "its weaknesses are
  generator effort (6/30 tedious, 7/30 high-effort) and no visible feedback on test effectiveness".
- `corpus/SOURCES.md:30` (S020, tier A, 244 Python projects): "data generation is the main
  challenge (36.62% of SO questions)".
- The F10 primary-source row the round is re-opening (staged S183,
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:37`): "it is important to
  provide good test data generators, that fit the program at hand" — the sibling entry quotes
  the same sentence at `pbt-generator-as-fixture.md` §"means for the lane's F10 move".

Commands: `awk -F'|' '/^\|[[:space:]]*S0(18|19|20|21)[[:space:]]*\|/ {print $2" :: "$8}' corpus/SOURCES.md`;
`grep -nE '^\|[[:space:]]*S183[[:space:]]*\|' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`.
An admitted entry that calls the generator interchangeable would land against held tier-A rows.

### F5 — the recheck recipe returns zero on the live bytes

`pbt-generator-craft-author.md:4`: `curl -fsSL '…quviq-testing.pdf' | grep -c 'QuickCheck'`
"(expect a non-zero count)".

Run verbatim 2026-10-26: **`0`**, grep exit 1 — the PDF's content streams are compressed, so
the string is not greppable in the byte stream. Through the extractor the lane's staged S183
row already uses (`pdftotext -layout … | grep -c 'QuickCheck'`) the same bytes give **`36`**.
The documented recheck therefore cannot confirm the source it is attached to; a 365-day recheck
under QUALITY 10 would fail on correct bytes (receipt `.s170-reopen.txt`).

### F6 — a line-break fold is printed as the source's text

`pbt-generator-craft-author.md:13` prints "…testing tool of choice in the Haskell community".
The source prints "Haskell com-" / "munity" across a line break (`s170.txt:16-17`). The fold is
not declared at the quote (QUALITY 91's rule for quotes, applied as corpus hygiene; the words
are otherwise correct).

### F7 — same ground as the sibling F10 entry, with weaker carriers

`pbt-generator-as-fixture.md:24-40` already states the same two conclusions — "the generator's
output is the fixture", "the deliverable is a named property plus the mutant it kills" — on
S157 (tier A paper) and S166 (a worked instance with recorded mutant counts). The candidate's
only content beyond that is the stateful recommendation (F1) and the interchangeability claim
(F4). Under CORPUS rule 4 a second entry on the same ground adds no expansion.

### F8 — standing: the `source:` row is staged, not opened in this lane

`pbt-generator-craft-author.md:2` cites `S170`, which is a row of the unappended package
(`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:24`), not a lane row
(`grep -nE '^\|[[:space:]]*S170[[:space:]]*\|' corpus/SOURCES.md` → no output). This is the
round-48 refusal ground (QUALITY 10 clause 2; `corpus/QUALITY.md:1394`), and it is the one
ground here that routine integration repairs — rounds 45–47 admitted package documents by
appending new rows (`corpus/README.md:565`, `:577`, `:589`). It is listed for completeness, not
as the decision.

## Verdict and flip condition

**Refuse.** Decisive criterion: **QUALITY 3** (an observation presented as the source's
statement must be the source's statement) together with **QUALITY 2** (every claim carries a
measured anchor) — F1 for the premise, F2 for the only lane-resolvable example, F3 for the
invented internal citation. F4 is a second, independent content ground: the claim contradicts
held rows S019/S020. F5–F8 are each independently blocking as written but are ordinary
integration repairs.

**Flip (would admit):** all of —

1. replace `:24-25` with S170's actual sentence ("…extensions made for testing stateful code,
   via a toy example in C", abstract) and demote the stateful preference to a labelled opinion
   about *one* possible pilot shape, not a "should";
2. delete `:28-30` or re-anchor it to a lane row that exists at the landing tip;
3. delete `:33-36`'s QUALITY-bar sentence or anchor it to a criterion that exists;
4. drop "the generator library is interchangeable" (`:34`) or restate it against S019/S020/S183
   as a contested question with the lane's own pilot as the discriminator;
5. append S170 as a new tameshi row opened 2026-10-26 (tier B, ≥6-token located quotes: abstract
   lines 15-17 and page 17 lines 12-13 / 23) with a `pdftotext`-based recheck; and
6. state what it adds beyond `pbt-generator-as-fixture.md` — at which point the honest landing is
   a fold into that entry or into the round's F10 lesson, not a second F10 entry.

If the aim is only to preserve S170's best sentence, it is page 17: "The need for a specification
is the real weakness of property-based testing" (line 23), reinforced at lines 12-13 ("formulating
specifications is hard"). The entry never quotes either — a fix that would strengthen the thesis
it claims in its title (`:7`) but does not carry.

## Adjacency (what the refused material routes to)

- Property craft vs generator craft: S170 page 17 is a statement about *specifications*, adjacent
  to the round's generator move, not a second F10 measurement. It belongs beside the pilot's
  property discussion (`contract.json` `claims.C2`), or in `corpus/lessons/round-49.md`'s Gate.
- The stateful-fixture idea is a candidate *next move* for F10 after the round's flat-domain
  pilot reports; it needs its own measured move, not an entry.
- Overlap map for the theme's ≥1-admit/≥1-reject requirement: `pbt-generator-as-fixture.md`
  (S157 tier A + S166 instance) and `r4-quickcheck-primary-correction.md` (S182 tier A, S183
  tier B, and it closes the lane's long-standing wrong-DOI lead) are the stronger carriers;
  this entry is the weakest of the three and duplicates their thesis.

## Out of scope / not claimed

- No claim decision, no counter invocation (`c1/measure.py`, `c2/measure.py` untouched); no
  `--selftest`, `--list` or scratch-tree run was needed for a read-only triage.
- Nothing read under `/home/vgpnk/.local/state/`; no `c2-*` control stdout opened.
- No model passed; no `agent://all` message.
- The guard, the panel, the contract, and the lane checkout are unmodified. Sibling entries and
  other seats' verdicts are not reviewed here.

## Touched surfaces

- Written (only these):
  - `.ufo/waves/round-49/w1/T49ScribePkgCraftAuthor.md` (this report)
  - `.ufo/waves/round-49/w1/T49ScribePkgCraftAuthor.s170-reopen.txt` (re-open receipt, PDF sha256 + quote locations + recheck counts)
- Read-only: `contract.json`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md`,
  `corpus/SOURCES.md`, `CORPUS.md` (fleet root), the candidate and its two sibling package
  entries, `corpus/lessons/round-45.md` `## Gate`, the package's `SOURCES.append.md`.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49ScribePkgCraftAuthor` removed after the receipt
  was copied (PDF, extracted text, second fetch all deleted).
- Tooling: none installed or upgraded (host pacman paused; nothing was needed — `curl`,
  `pdftotext`, `pdfinfo`, `grep`, `awk` were already present).

## Summary

- REFUSE `pbt-generator-craft-author.md` as written; decisive ground is content (QUALITY 3 + 2), not standing.
- F1: line 24-25 says S170 is "not toy examples"; S170's abstract says "via a toy example in C".
- F2: line 28's `S116` resolves to no tameshi row now or in history; other lanes' S116 are unrelated objects.
- F3: line 35 cites a QUALITY-bar warning about libraries/contributions that does not exist.
- F4: line 34's "generator library is interchangeable" contradicts held tier-A S019/S020 and staged S183.
- F5: the line-4 recheck prints `0` on live bytes; `pdftotext | grep -c` prints `36`.
- F7/F8: same thesis as `pbt-generator-as-fixture.md`; `source: S170` is a staged, unappended row (flippable).
- Flip needs a corrected premise, a resolvable anchor, a real criterion, and a reason to exist beside the sibling entry.
