# W05ReadmeRows — corpus/README.md draft rows, round 17

Baseline: committed `corpus/README.md` at `98bea7da5801f4bc58e4187690ee1687c8a5061f` (237 lines). Read with `git show`; no lane file was edited, no git write, no `jj`.

## Evidence gathered

| Check | Command | Result |
|---|---|---|
| Knowledge files without a coverage row | `git ls-tree -r --name-only 98bea7d corpus/knowledge`, then `grep -qF "knowledge/$b"` on the committed README | 0 missing (25 files, all have a row) |
| Fleet round lessons table rows | `grep -n` on the committed README | 1 row only: `lessons/round-1.md` (README:26). Rounds 12–16 have no row in that table; each has its own `## Round N —` block (README:123, 148, 180, 195, 219) |
| Round-block shape | README:219–237 (round 16) | Appended `## Round N — title` block, one intro sentence, `Note / Holds / Sources` table, dated superseded-readings paragraph |
| Entry provenance trio | `git show 98bea7d:corpus/knowledge/incremental-pin-disposition.md \| head -8` | `source:` / `verified-at:` / `recheck:` lines, then `ground:` / `source-correction:` |
| Peer drafts (read-only, `history://`) | W02KnowledgeDraft, W01LessonDraft, W04QualityDraft | W02 drafts `corpus/knowledge/input-keyed-coldread-credit.md`; W01 drafts `corpus/lessons/round-17.md` (`## Mistakes`); W04 drafts QUALITY criteria 23–26. None of these files exist in the lane yet (`ls corpus/knowledge`, `corpus/lessons`: no round-17 files) |

Consequence: the "new entry" is `corpus/knowledge/input-keyed-coldread-credit.md` (W02, not yet written). Its coverage row is drafted from W02's assigned content, not from its bytes. Its `S0xx` source ids are markers for the L1 to mint; I did not invent ids.

## Neighbouring rows (verbatim, for shape)

Coverage map, last round-16 row (README:219–237 block):

```
| Note | Holds | Sources |
|---|---|---|
| `knowledge/mutation-case-kumitate-round-gate.md` | case 7: kumitate `round-gate.mjs` 5/10 (50 %), 10/10 pre-registered predictions held; projected floor interval [26,1059] confirmed at its edge (1059 survives, 1060 killed); guarded `env -i` suite; ledger leg `js-round-gate` (`--regression` cases=7) | S053, S052, S056, S057; `arm-class-matrix.md` §13 |
```

Fleet round lessons, only row (README:26):

```
| Entry | Admitted / rejected | Evidence |
|---|---|---|
| `lessons/round-1.md` — fleet round-1, distinct from the historical training arc | Admitted: canonical, durable lane assertions; rejected: same-lane promotion authority and broad current cold-read credit from one historical JS mutant. Outside admit/reject review remains open. | `../reports/round-1-calibration.md`; `../LOG.md` fleet round-1 entries |
```

Frontier table header (README:68–73): `| id | ground | candidate sources | status | next falsifiable move (before → after) |`; rows F1–F10 are all `open` or `held/partly held` and none is touched by round 17.

## Placement decision

Rounds 12–16 appended their rows in a `## Round N` block rather than inserting into the top table, so earlier line numbers stay valid (README:123–237 say so explicitly). Round 17 follows that shape: one new `## Round 17` block at end of file. The Fleet round lessons table is the one place where round 17 **does** get a row, because the Target asks for it, but the table has not been kept current since round 1 (see Findings).

## Draft A — coverage-map row for the new entry (goes in `## Round 17` block)

Conditional on W02's file landing as `corpus/knowledge/input-keyed-coldread-credit.md`. If it lands under another name, the row name changes and nothing else.

```
| Note | Holds | Sources |
|---|---|---|
| `knowledge/input-keyed-coldread-credit.md` | why sha-only cold-read credit goes stale (a section's executed commands read lane files that move while the SKILL.md sha stays fixed); the input-keyed rule (contract C / R16-C2b): an entry with executed commands credits its bucket only if every recorded input still has its sha256 at the measured rev; strace-based input capture (`trace-inputs.py`); undeclared-input limits; re-measure with `measure.py --rev REV`; lane assertion, not promotion | S0xx (strace(1) — L1 mints); S0xx (round-16 spot-check, `lessons/round-16-verifier-spotcheck.md` §2–§6); `.ufo/evidence/round-17/coldread/` (wave-2 ledger) |
```

## Draft B — Fleet round lessons row for round 17

Goes in the `## Fleet round lessons` table, directly under the round-1 row. Conditional on W01's file landing as `corpus/lessons/round-17.md`.

```
| `lessons/round-17.md` — fleet round-17, calibration and entry-command operability (repair round after round-16 rejected-harmed) | Admitted: none adjudicated here — round-17 claims are lane-asserted (input-keyed cold-read credit, entry-command registry); rejected: none recorded. Round-16's rejected-harmed verdict stands as history and is not reversed. Outside admit/reject review remains open. | `../.ufo/evidence/round-17/`; `lessons/round-16-verifier-spotcheck.md` §2–§6; `../tools/registry.json` and `../tools/registry-check.py` (after the L1 install) |
```

Matching status sentence (same style as the round-1 status paragraph under the table), to follow Draft B:

```
Fleet round-17 status: **lane-asserted repair; formal admission open**, not a
completed round. Wave 1 builds the instruments and falsifiers; the full-page
cold-read re-read and the registry counts (`REGISTRY_CHECK: held=N/M`) are wave-2
work and are not claimed here.
```

## Draft C — Frontier annotation (appended paragraph at end of `## Round 17` block)

```
## Round 17 — input-keyed cold-read credit and entry-command operability

[Coverage-map row(s) and fleet-lesson row above.]

Frontier F1–F10 are unchanged: no ground moves to `held` in this round. The
input-keyed entry documents a calibration method for the box-3 cold-read ledger;
it is not a new ground in the frontier table, and its `S0xx` source ids are not
yet mined `SOURCES.md` rows, so under QUALITY 10 it cannot move F3 or F7. F7
(incremental re-sweep granularity) is related in mechanism to the input-keyed
rule but its next move (per-leg reuse decisions) is not measured here.

The round-16 block's cold-read credit reading stands as recorded history. A
round-17 credit reading is only the output of `measure.py --rev REV` with the v2
ledger; until that is run at the round's rev, no bucket is re-credited and the
round-16 full-page ledger keeps its v1 reading. Full-page box-3 re-read and any
promotion remain open.
```

## Findings for the L1

1. **Fleet round lessons table is stale.** It has one row (round-1). Rounds 12–16 each have a `## Round N` block but no table row, so `lessons/round-12.md`…`round-16.md` are not indexed in that table. The round-17 row is drafted as asked; the L1 decides whether to backfill 12–16 (out of this target).
2. **Known gaps sentence is stale.** Known gaps says "New entries carry the header (2 of 21 now)". With the new entry and any round-16 entry, that count is wrong; the L1 should recount (`for f in corpus/knowledge/*.md; do head -5 "$f" | grep -c '^source:'; done | sort | uniq -c`) and update in the same round. I did not draft that edit.
3. **Round-17 knowledge row is conditional.** W02's entry does not exist yet. The `S0xx` markers must be replaced by minted ids before landing; each id must have a `SOURCES.md` row opened this round (QUALITY 10).
4. **Placement.** Use the appended `## Round 17` block, not an edit in the top coverage table, to keep prior line numbers stable (README:123–237 convention; QUALITY 7).
5. **No edits to `corpus/README.md` were made.** Rows above are drafts for the L1 to integrate.

## Tools

No tools installed or updated. Scratch: `/tmp/tameshi-r17w1-W05ReadmeRows-rd.md` and `/tmp/tameshi-r17w1-W05ReadmeRows-scratch` (removed after writing this report).

## Verdict

built — README row drafts (coverage row, fleet-lesson row, round-17 status and frontier annotation) written to this report; conditional on W01/W02 file names; no corpus file edited.
