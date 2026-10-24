# ReviewFrontierStatus — S104 row, search log, and source-census review

Scoped item: S104 row (`corpus/SOURCES.md`), the round-37 search log (LOG.md Frontier
entry + `corpus/lessons/round-37.md` Gate + seat search log
`.ufo/waves/round-37/w1/ScoutBashSource.md`), and the start/end `sources-census.sh
validate` outputs. Reviewed the diff `e423c41..e6185d5` for registry field flips.
Live lane checkout untouched; fetched the pinned source read-only to /tmp.

## Verdict

**PASS with one low-severity observation.** ID allocation, tier, status, access
date, quote content, used-by, and the census receipts are all correct and
internally consistent; the only documented old→new flip (S103 `used-by`) is real,
justified, and logged in three places. One cosmetic anchor-window off-by-one.

## Findings

### LOW — anchor line window cites the node header, not the quote body

The row's anchor and the lesson's Gate cite "lines 489–493" (and URL fragment
`#L489-L493`), but the located quote occupies lines 494–495.

Observed on a fresh fetch of the pinned URL (2026-10-24, 415,804 bytes,
sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` —
byte-identical size+digest to S097's recorded pin):

```
$ grep -n "@node ANSI-C Quoting\|Character sequences of the form" /tmp/bashref_sav2.texi
489:@node ANSI-C Quoting
494:Character sequences of the form @code{$'@var{string}'} are treated as
```

`corpus/SOURCES.md:113` ("lines 489–493") names the `@node` header/`@cindex` block
(489–493); the quoted sentence "…are treated as a special kind of single quotes."
is at 494–495; `corpus/lessons/round-37.md:7` reads "Located quote, `@node ANSI-C
Quoting`, lines 489–493: …". Section name and node anchor are exact; the numeric
window describing where the quote sits is off by the 5-line header. Same
observation, independently reached, in `ScoutBashSource.md` ("Nuance found").
Cosmetic: the anchor's section/node identity is correct and the quote is verbatim
modulo Texinfo markup; a repair would write the window as 489–495 (or "node at
489, body 494–495"), not 489–493 alone.

### Informational — cosmetic URL fragment

`#L489-L493` is GitHub-style line syntax; cgit serves raw text for `plain/` and
uses `#nNNN` anchors for `tree/` views, so the fragment is inert data. Harmless;
the prose anchor carries the real location.

## Checks that pass (evidence)

- **ID allocation.** `grep -c '^| S' corpus/SOURCES.md` → 101 rows; `git show
  e423c41:corpus/SOURCES.md | grep -c '^| S'` → 100. Pointer `- Next unused id:
  S104.` at `SOURCES.md:423` was live before the row landed (pre-existing
  duplicate at `:425`-area is append-only convention; line `:426` now reads
  `- Next unused id: S105.`). No collision; gaps S038/S039/S098 are pre-existing
  (absent at e423c41 too), consistent with the registry's documented pointer
  convention.
- **Tier/status.** Row fields `docs | A | … | mined` at `SOURCES.md:113` are
  schema-valid per `.ufo/evidence/kaika-round-1/sources-census.sh` enum check;
  tier A matches sibling row S097 (same official GNU Bash 5.3 manual, same
  commit). `mined` is satisfied: every used-by path exists and cites "S104"
  (H4 rule).
- **Access date.** `opened 2026-10-24` and `recheck 365d` (same cadence as S097);
  r37 commit `e6185d5` dated 2026-10-24; my own re-fetch of the pinned URL
  succeeded the same date (canonical host `cgit.git.savannah.gnu.org`;
  `git.savannah.gnu.org` returns a bare 301 — scout log documents the same).
- **Quote grounding.** Located quote verbatim modulo markup: texi
  `@code{$'@var{string}'}` → "`$'string'`"; 15 words ≤ 25. Grounding for the
  teaches claim verified: `\'` → `single quote` at lines 520–521 and "The
  expanded result is single-quoted, as if the dollar sign had not been present"
  at 543 — exactly the escaped-`'` semantics the C2 tool implements; scope text
  ("bounded comment-blinding", nested substitutions/continuations out) matches
  the section's actual coverage.
- **Used-by.** `tools/tally-audit-v3.py` cites S104 at `:158` (code_view
  docstring); `corpus/lessons/round-37.md` cites it (Gate, Mistakes). QUALITY.md
  (`:875`, criterion 74) and SCORECARD.md (`:1803,:1809`) also name S104 but are
  not in the cell — consistent with convention (QUALITY/scorecard never appear
  in used-by; tools do, cf. S102).
- **Old→new flip.** `git diff e423c41 e6185d5 -- corpus/SOURCES.md` shows exactly
  two changes: the S104 append (row + Round-37 notes + S105 pointer) and S103
  `used-by` `.ufo/evidence/round-36/coldread/refresh-receipts.json,
  corpus/lessons/round-36.md` → `corpus/lessons/round-36.md`. No status/recheck/
  tier/anchor fields changed on S103 or any other row; the flip is logged in the
  registry notes (`SOURCES.md:425`), the lesson (`round-37.md:8`), and LOG.md.
  Justification holds: the receipts file does still contain `cited_source` S103
  strings (5 hits), but the r36 review found that field is not consumed by the
  monitor, and the flipped convention matches how the S102 precedent treats
  evidence JSON vs. tools/lessons.
- **Census output.** `census/start.stdout` (tip d9c496b): 9 pre-existing warnings,
  `ok`, exit 0. `census/end.stdout`: same warnings plus `W04 S104 duplicate url
  cgit.git.savannah.gnu.org/…id=b8c60bc9… across scopes`, `ok`, exit 0. The new
  W04 is real (S104 shares S097's pinned URL; the validator normalizes the
  fragment) but consistent with convention — seven prior W04s (S047/S048, S092,
  …) are tolerated when scopes differ; disclosure confirmed
  (`CriticSHONENRestraint.md:44`). No E-class errors, no exit-code change.
- **Search log.** `ScoutBashSource.md` records the fetch protocol, 415,804-byte /
  `f3d37d57…` pin, commit identity (`bash-5.3` tag), and the 301/502 transient —
  all reproduced above. Its "nuance" is adopted as the LOW finding. LOG.md
  Frontier entry (`:1981-1988`) and lesson Gate are consistent with the receipts.

## Residual risk / gaps

- Offline-verifiability gap (by precedent, not new): S104 has no committed
  snapshot and no byte count/digest in its anchor — weaker than S103's pin but
  identical to S097's; the commit-pinned URL plus scout receipt is the load-
  bearing record. If the convention tightens, S097 and S104 would both want a
  committed `.texi` snapshot.
- The 301 from `git.savannah.gnu.org` means S097/S104 fetches must use the
  `cgit.git.savannah.gnu.org` canonical host going forward; the row URL already
  does.

No installs. No edits to lane content.
