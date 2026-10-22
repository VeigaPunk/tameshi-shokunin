# ScoutNextFrontier — planning data walk, routed items 2–8

Scope: items 2–8 of `corpus/lessons/round-27-verifier-spotcheck.md` ("## Routed
defects"). For each: is it still open at
`b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a` (lane HEAD), which lane files the
fix must edit, and how many cold-read ledger entries record those files as
inputs. Ledger =
`.ufo/evidence/round-21/coldread/ledger.json@b05d2ee`, 354 entries; counts
are keys in `entries[].inputs` (lane-relative paths only; `external_inputs`
excluded). Counting command:

```
git show b05d2ee…:.ufo/evidence/round-21/coldread/ledger.json | python3 -c \
 'import json,sys; [len(...)]' # per-key Counter over entries[].inputs
```

## Table

| # | Routed item | Open at b05d2ee? | Lane files the fix must edit | Ledger entries recording each file |
|---|---|---|---|---|
| 2 | Full `registry-check.py` run at the landed head from a fleet mirror | **Open** | None existing: new receipt file under `.ufo/evidence/round-28/` (evidence files are never ledger inputs). `tools/registry.json` (86 entries) only *if* the run flags a stale row | 0 unconditional; 86 conditional |
| 3 | `corpus/SOURCES.md:338` "Next unused id: S090" stale; no r27 bounded-lookup note for S090/S091 | **Partly met, still open** | `corpus/SOURCES.md` | 99 |
| 4 | `corpus/README.md` F8 row "independently anchored" overstates (3 of 4) | **Open** | `corpus/README.md` | 54 |
| 5 | QUALITY 53/54 amendments; possible S012 supersedes row | **Open** | `corpus/QUALITY.md`; `corpus/SOURCES.md` only if the S012 tier is revised | 31; +99 conditional |
| 6 | `--regression` leg-sum check `npass+nfail+nsetup == nlegs` | **Open** | `tools/mutate-and-run.sh` | 199 |
| 7 | Wording: SCORECARD "51 wave seats cold-read", LOG/lesson "15 real defects"; ledger rewrites re-indent whole file | **Open** | `SCORECARD.md` (2), `LOG.md` (2), `corpus/lessons/round-27.md` (0); ledger-writer fix lands in a new `round-28/coldread/append-entries.py` (0) — or edits `round-27`'s copy (0, evidence path) | 4 total |
| 8 | Cross-lane: r26 cite-check-hole routing dropped by kumitate R39-5 | **Open; tameshi cannot close it** | None in this lane — kumitate files only (`scripts/cite-check.mjs` sits in `external_inputs`, so kumitate edits drift zero tameshi credit) | 0 |

## Per-item evidence

**Item 2 — open.** Only receipt is `.ufo/evidence/round-27/after/registry-2227d83.json`,
predating the SKILL registry-row edits in `b1cc95e`/`af7b70d`. `git ls-tree
b05d2ee .ufo/evidence/round-27/ .ufo/evidence/round-28/` shows no
`registry-*` file at `35a01b3` or `b05d2ee` (round-28 holds only
`append-probe.txt`, `census-start.{exit,stdout}`). The fix creates a new
receipt; it edits an existing ledger-tracked file only if the run flags
`tools/registry.json`.

**Item 3 — partly met.** `git show b05d2ee:corpus/SOURCES.md`: line 338 still
reads `- Next unused id: S090.` and line 352 `- Next unused id: S092.`; the
b05d2ee diff appends a "Round28 bounded lookup" note stating "The stale
`Next unused id: S090` line above stays append-only; S090 and S091 were used
in round 27." That is the append-only-correct repair pattern for the stale
pointer. Still open: no identified/screened/included record for the round-27
S090/S091 mining exists anywhere (the appended note documents S059's
re-open, not the r27 lookups); fix is another `corpus/SOURCES.md` append.

**Item 4 — open.** `corpus/README.md@b05d2ee:85` F8 row still reads "one
survivor classified against an independently anchored expectation" with no
3-of-4 bound; the round-27 section (:422–427) names the bound but the row is
not amended. b05d2ee did not touch README.

**Item 5 — open.** `corpus/QUALITY.md@b05d2ee:591–614` items 53/54 are the
un-amended text ReviewQuality flagged: 53 keys on edits to "a file traced as
an input" (the counter cannot check "independent"), 54 requires receipt
sha256-binding ("a named digest is not provenance" per the routed item).
S012 stays `mined`, tier B, `corpus/SOURCES.md:60`-region row unchanged by
b05d2ee — a supersedes row is needed only if the tier-B call is revised.

**Item 6 — open.** `tools/mutate-and-run.sh@b05d2ee:1430` `local nlegs=9
npass=0 nfail=0 nsetup=0`; the loop :1431–1437 classifies each leg status;
verdict prints at :1439–1452 use `nlegs` without asserting
`npass+nfail+nsetup == nlegs`. A *static* selftest check exists
(:1938–1945, "leg-count agreement: calls=9 specs=9 nlegs=9") but the runtime
leg-sum check round-26 item 5 asked for is absent — still open exactly as
routed. Runner carries the heaviest cold-read footprint in the lane.

**Item 7 — open.** `SCORECARD.md@b05d2ee:1374` "C1 detail: 51 wave seats
cold-read the 39 uncovered sections at `2227d83`;" — 39 of 51 did reads.
`LOG.md` round-27 block: "51 + 8 seats; 15 page defects found by cold reads
and corrected in SKILL.md." `corpus/lessons/round-27.md:164` "They found 15
real defects in SKILL.md text" — corrected count is 13 pre-existing + 2
self-introduced (the spot-check's own arithmetic). For the ledger-format
sub-item: `.ufo/evidence/round-27/coldread/append-entries.py:48` writes
`json.dumps(ledger, indent=2)` — whole-file re-indent; the round-26 copy is
a different script (sha256 `02fb82fe…` vs `65b28b62…`). Smallest safe fix is
a round-28 append script that preserves prior bytes (append tail only);
editing the committed round-27 script is pointless (it is a historical
receipt).

**Item 8 — open here.** Routed to kumitate via the integrator. Kumitate lane
is at `dfabe92` (round-41 closure); `scripts/cite-check.mjs` bytes now
`896f0720…` ≠ the r26 pin `40573448…`. Later rounds added 11 hermetic cases
(round-41 `68db341`, "75/75") and the zero-resolved `VERDICT: FAIL` fixture
(round-40 `1530a75`) — the *companion* r26 item 7 request — plus cases
adjacent to the holes (`LINE_OOR` selftest :1883, `--strict` warn→DRIFT
:2404). But no kumitate commit names the R39-5-dropped routing or all four
tameshi-named holes (line n+1, `--strict` + one warning, unknown-flag exit
64, interior-slice content pin); the planner should treat it as still open
and re-route, not as silently absorbed. Zero tameshi ledger cost: kumitate
paths appear only in `external_inputs`.

## Credit-drift cost ranking (descending)

Under QUALITY 53 / the round-28 lesson mechanism, editing a file named in
`entries[].inputs` un-matches every section that recorded the old hash. Cost
= entries recording the file:

1. **Item 6 — `tools/mutate-and-run.sh`: 199** (most-read file in the ledger)
2. **Item 3 — `corpus/SOURCES.md`: 99** (b05d2ee's append already dropped 10
   credited sections; a second edit re-drifts the same population)
3. **Item 5 — `corpus/QUALITY.md`: 31** (+`corpus/SOURCES.md` 99 *only if* the
   S012 supersedes row is written — prefer amending QUALITY text alone)
4. **Item 4 — `corpus/README.md`: 54**
5. **Item 7 — `SCORECARD.md` 2 + `LOG.md` 2** (lesson and writer files cost 0)
6. **Item 2 — 0** unless the run flags a registry row (then 86)
7. **Item 8 — 0** in this lane

Ranking strictly by unconditional key count: 6 (199) > 3 (99) > 4 (54) >
5 (31) > 7 (4) > 2, 8 (0).

## Planner note

Items 3, 4, 5 all touch high-drift prose files; batching them into one
content commit does not reduce per-file drift (each edited file un-matches
its own recorded hashes) but does collapse the re-read wave to one revision.
Item 6 alone nearly doubles item 3's cost; the LOG note in round 27
explicitly left it open for this reason.

Tools: none installed or updated this task. Read-only git on the lane and on
the kumitate sibling (`GIT_OPTIONAL_LOCKS=0`); no writes outside this report.

Report: `.ufo/waves/round-28/w1/ScoutNextFrontier.md`
