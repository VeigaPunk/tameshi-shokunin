# FCensusNoHarm — round 19 w2 falsifier (CensusNoHarm)

## Strongest material assertion attacked
The census table: 76 registry rows; tier A/B/C = 67/7/2; status
mined/queued/rejected = 48/23/5; 0 malformed rows; 0 duplicate IDs; S038–S039
intentionally retired; S079 next unused — with the derived no-harm decision
"no new row warranted; S049 already exists and only gained the round-19
used-by".

## Verdict: AGREE
Every count reproduced independently by plain awk over
`corpus/SOURCES.md` (read-only; no validator rerun, per bounds):
rows=76; tier A=67 B=7 C=2; status mined=48 queued=23 rejected=5;
duplicate IDs=0; max ID=S078 → next unused S079 (SOURCES.md:223).

## Evidence
- Staleness ruled out: `git diff 55e1d312 master -- corpus/SOURCES.md` is
  empty and the working tree is clean for that file, so the census applies
  byte-identically to the frozen build revision 55e1d31 (observation 2026-10-21).
- Structure check under the true 13-field layout (tier=$5, status=$9,
  opened=$10, recheck=$11, used-by=$12): all 76 rows pass Sddd ID format,
  tier enum, status enum, YYYY-MM-DD opened, `Nd`/`on-release` recheck,
  nonempty used-by; no mined row has `—`. 0 violations.
- S038–S039 retirement quote confirmed at SOURCES.md:207-209 ("S038–S039
  allocated, never written, retired").
- Cited evidence verified: `.ufo/evidence/round-19/census-start.txt:1-10`
  records `sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  tameshi`, Exit: 0, and exactly six W04 duplicate-URL warnings
  (S047, S048, S075–S078), matching the report's characterization.
- No-harm grounded: `corpus/lessons/round-19.md:27-40` states S049
  "reopened 2026-10-21", used-by = old list + `corpus/lessons/round-19.md`,
  and the exact words "No new source rows or tier changes; no frontier
  ground moved." Registry matches: S049 row exists, mined, on-release,
  used-by ends with round-19.md. No row added (76 rows; S079 next unused).
- C1 comparison: `.ufo/evidence/round-19/measure.py:1-38` measures only the
  five frozen round-18 corrections via revision-pinned blobs (4b7c682 /
  921ef807, numstat DIFF_COMMAND on historical snapshots); it does not
  measure the current registry, so the census claims are independent and
  uncontradicted by the C1 ruler.
- Post-census delivered changes (S049 used-by append; lesson source-sweep
  addendum appending `corpus/knowledge/guard-kill-closure.md` to S063/S077/
  S078 used-by) alter only used-by cells of existing mined rows; statuses
  stay mined, rechecks unchanged (S063 on-release, S077/S078 180d). None of
  the report's tallies move. This is a completeness note, not a defect: the
  report does not mention the S063/S077/S078 append, but its scoped
  assertions remain true at 55e1d31.

## Concrete falsifier
Recount `git show 55e1d312c4e8ac67aefad80099bd27581ff805c9:corpus/SOURCES.md`
for `^\| S[0-9]{3} ` rows: if tier tally ≠ 67/7/2, status tally ≠ 48/23/5,
row count ≠ 76, or any two rows share an ID, the census assertion fails.
Recomputation yields exact agreement; the falsifier does not fire.

## Residual unknowns
- The report names its awk predicates but not the field positions it used
  for opened/recheck; its tally fields ($5/$9) match the real layout, and
  its described structural checks pass under the true $10/$11/$12 mapping.
  I reproduced the semantics, not its literal command.
- I did not rerun `sources-census.sh validate` (bounds); the W04 warning set
  rests on census-start.txt, which the report itself also treated as
  retained evidence.
- Row prose accuracy (titles/teaches columns) is outside the census claim
  and was not audited.

No production edits, no installs, no git writes; read-only awk/sed/git-diff
over the frozen build surface only.
