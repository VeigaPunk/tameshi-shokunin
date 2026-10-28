# T54W1ScoutNextEntry — next assimilation candidate

Survey only. Nothing in the lane or in `/home/vgpnk/Projects/shokuknow` was edited. No campaign tool was run.

The path named in the seat item, `merge/tameshi/knowledge/delta-debugging-minimization-contract.md`, is not on disk. The staged file is `merge/tameshi/knowledge/corpus/knowledge/delta-debugging-minimization-contract.md` (47 lines, opened read-only). The package index is `merge/tameshi/MERGE-REPORT.md:35`.

## Verdict

Not a next candidate. Round 50 already admitted this entry, edited, at the target path below, and refused the staged row and the 139-run cost sentence (`corpus/lessons/round-50.md:57-67`). Copying the staged bytes in now would overwrite that landing.

## Target path

`corpus/knowledge/delta-debugging-minimization-contract.md`

MERGE-REPORT classifies it `new-file`, round2, title "A reduced fixture has a stated minimality witness and a stated cost in test runs". The lane already holds that path. The landed file is the round-50 edit (header re-pointed to S271 + S024, `verified-at: 2026-10-26`), not the staged bytes.

## `source:` staged ids

One id, on line 2 of the staged file:

- **S167** — `https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf` — locator "§I Introduction (ddmin definition and the 896-line HTML case study), p. 183-184" — IEEE TSE vol. 28 no. 2, February 2002, "opened from a university course mirror 2026-10-23".

No second `source:` line. The body cites only S167. The boundary paragraph points at `CANNOT-ANSWER.md` §2, which is not a `source:` id and is not a file in the package or the lane.

## Rows it would need appended

The package's own append row is one row, staged **S167**, same URL (`merge/tameshi/SOURCES.append.md:21`, 11 cells). Its claim cell says the reduction cost is "139 automated test runs, 35 minutes on a 500 MHz PC". Its `used-by` cell names two paths: this entry and `corpus/knowledge/repeat-control-measured-n3.md`.

Do not append it.

- The same URL is already lane row **S271** (`corpus/SOURCES.md:146`), opened 2026-10-26, mined, used by this entry and by `corpus/knowledge/fixture-shrinking-pilot.md`. Round 50 recorded that staged S167 collides with no lane id and is not reused (`corpus/SOURCES.md:506`; `corpus/lessons/round-50.md:48-52`).
- Staged ids S161–S255 stay reserved (`corpus/SOURCES.md:514`). Next unused lane id is **S280**. Minting S167, or a second row for this URL, is not an append this entry needs.
- MERGE-REPORT's "rows whose source the lane already holds" table (`MERGE-REPORT.md:114-124`) does not list S167. That table was staged when the lane held 107 rows and the first staged id was S153 (`MERGE-REPORT.md:9`). It is stale against S271.

## Fit against the round-50 shrinker's stated blind spots

Does not fit. The shrinker's own list is `corpus/knowledge/fixture-shrinking-pilot.md:104-128` ("What this does not establish"), for `tools/shrink-case.py`. The counter's matching limit is `.ufo/evidence/round-50/contract.json` `claims.C2.cannot_see` (search beyond logged cost; generality past the 20 cases).

| Stated blind spot | What the staged entry does |
|---|---|
| Units are lines and map entries, not cells (`fixture-shrinking-pilot.md:106-108`) | Talks about a generic "input entity". Does not name the shrinker's unit and does not close the cell cut. |
| Starting cases are the generator's tiny cases; a directory, a long log, or a compiled input is not measured (`:109-111`) | The worked example is an 896-line HTML reduction — the class the shrinker says it did not measure. |
| A greedy-to-fixpoint loop meets the same bar; ddmin is not claimed to beat greedy (`:112-113`) | Presents ddmin as the specification of "reduced". Does not contradict the non-claim, and does not close it. |
| These are killing cases, not survivors; B5 stays masked (`:114-117`) | Says "the lane's own B5 probe has not been reduced" (staged lines 35-36). Round 29 did reduce it: 171 oracle tests, kept nothing, B5 masked (`corpus/knowledge/survivor-fixture-minimization.md:53,57`). The sentence denies the blind spot instead of matching it. |
| One gate, 20 mutants, one seed (`:118-119`); counter cannot see generality past those 20 | Silent. Does not close it. |
| A kill is oracle agreement, including a setup refusal; the counter cannot tell a readable 1-minimal case from one that is merely small (`:120-122`) | The inference on staged lines 26-28 asks the lane to publish "the entity whose removal restores the failure". The source, and the shrinker's check, say the opposite: removing any single unit makes the failure disappear (`.ufo/evidence/round-50/c2/measure.py` docstring "minimal"). |
| The counter sees the search only through logged cost and the resulting case (`:123-124`) | The cost half matches a property the shrinker already publishes (`runs`). It does not see chunk order or cache reuse, so that blind spot stays. |
| Under the counter's layout the real-guard selftest leg is skipped (`:125-128`) | Silent. |

The only overlap is the cost unit (test runs). That property is already in the landed entry and in the shrinker. Nothing in the staged file closes a listed blind spot.

The staged F6 next-move quote, "B5 probe fixture size: unmeasured → reduced size + kill check", is the old frontier cell at `corpus/README.md:83`. The round-50 restatement is `corpus/README.md:621`: F6 held for the method on killing cases; B5 not discharged; next move is a second gate or discharging B5.

## First QUALITY-bar failure

**QUALITY 10, second clause** (`corpus/QUALITY.md:27-30`): an external source enters through a `SOURCES.md` row opened in the round that writes it. The staged file's first content line is `source: S167`, and S167 is not a lane row.

That is the decisive gate the round-50 triage recorded (`.ufo/waves/round-50/w1/T50ScribePkgDD.md:230`). It fails before any body sentence.

If a row were opened from the staged line anyway, the first claim-level failure is **QUALITY 2** (`corpus/QUALITY.md:4-5`), which is the refusal the round-50 lesson actually numbered (`corpus/lessons/round-50.md:62-67`):

- The row and the entry attribute "139 automated test runs, or 35 minutes" to the 896-line reduction (staged lines 15-17; append-row claim cell). The abstract states 139 as the case study's total. §I and §IV-B Fig. 12 state 57 for that reduction. 82 + 57 = 139 is an inference the paper does not state.
- The anchor `p. 183-184` does not resolve on the carrier the lane opened: 17 pages, paginated 1–17, no journal folios (same lesson; landed `verified-at` line).
- The `recheck:` command, `curl -fsSL <url> | grep -c 'minimal test case'`, counts a compressed PDF and returns 0. The round-50 re-open recorded that (`.ufo/waves/round-50/w1/T50ScribePkgDD.md:96-99`).

Also failing as written, not first: QUALITY 9 (no snapshot in the package), 34 (page anchor on a file the lane does not own), and a dangling `CANNOT-ANSWER.md` §2 (QUALITY 97 as cited by the same triage at line 231). The witness-direction sentence (D5 in that triage) is the misfit against the shrinker, not the first bar failure.

## What was opened

- `/home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md` (the knowledge-file row at line 35; the already-held table at lines 114-124; adopt checklist).
- `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/delta-debugging-minimization-contract.md` (whole file).
- `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:21` (the S167 row, read verbatim).
- Lane: `corpus/knowledge/delta-debugging-minimization-contract.md` (landed edit), `corpus/knowledge/fixture-shrinking-pilot.md:104-128`, `corpus/README.md:83` and `:621`, `corpus/SOURCES.md:146` and `:505-514`, `corpus/QUALITY.md:3-5` and `:27-30`, `corpus/lessons/round-50.md:46-67`, `.ufo/waves/round-50/w1/T50ScribePkgDD.md:84-160` and `:227-233`, `.ufo/evidence/round-50/contract.json` C2 `cannot_see`.

No tools installed.
