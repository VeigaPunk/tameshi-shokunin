# T49Read03 — C1 reader, `## Mutation-sweep recipe`, pointer ordinals 10-14

Seat: C1 reader (wave 1). Item: read the five rows of
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` whose heading starts with
`## Mutation-sweep recipe` and whose ordinal ∈ [10,14], at base
`8ca67421111fa354b47b803358391d0b07fc6db9`, against their targets at base, and record
verdict + verbatim located excerpt + proposed correction when not `holds`.

I decided no claim and ran no counter verdict. `measure.py` was used only as `--list` (allowed)
and its `list_pointers`/`check_reads`/`norm`/`pointed_text` functions were imported for a
static compatibility check of my own rows; no `measure.py` measure invocation was made.

## Behavior

For each pointer I opened `SKILL.md` at base at the row's `skill_line`, read the clause the
pointer supports, then opened the target at base (`git cat-file blob BASE:<file>`, pointed
lines only) and judged whether the pointed text really carries that clause.

- Base classes come from `git show 8ca67421…:SKILL.md` (blob `0b44815ce04ed07848a0245ebc41588d093021f3`,
  2136 lines); targets from `git cat-file blob BASE:corpus/knowledge/mutation-case-kagi-census.md`
  (274 lines, blob `945911eb350fcdea8b25ff2643efa5d2a6e8f6da`) and
  `…:corpus/knowledge/mutation-case-kimi-census.md` (237 lines, blob `622c5a5ac57e864d43f2aa9fbe6e0c05c6c30a88`).
- Pointer list reproduced from the frozen extractor:
  `python3 .ufo/evidence/round-49/c1/measure.py --list --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8ca67421111fa354b47b803358391d0b07fc6db9`
  → `missing_headings=[]`, 90 pointers, and exactly the five ordinals 10-14 this seat owns with
  the same `file`/`ranges`/`skill_line` as the control file (ord10 kagi 184-191 @skill 170;
  ord11 kimi 22-25 @174; ord12 kagi 44-47 @175; ord13 kimi 26-28 @186; ord14 kagi 48-49 @187).

Result: **5/5 `holds`, 0 stale, 0 unresolved, 0 absent.** Each pointed range is still the text
the clause describes; no line numbers drifted.

## Findings (one line of reasoning each)

1. **ordinal 10 — `mutation-case-kagi-census.md:184-191` — holds.** Clause
   `round 3's E1 kept miscalled case counts — mutation-case-kagi-census.md:184-191`
   (`SKILL.md:169-170`); the range opens on the §5 append-only errata heading
   (`corpus/knowledge/mutation-case-kagi-census.md:184`) and carries E1 at `:186-191`:
   "predicted the killed/survived verdict on **10/10** mutants but the failing-case *counts* on
   only 6/10" (B2 1→2, B3 2→3, B6 1→2), and the file dates itself round 3 (`:1` `TAMESHI-R3-1`,
   `:3` "round 3"). Show:
   `git -C LANE show 8ca67421…:corpus/knowledge/mutation-case-kagi-census.md | sed -n '1,3p;184,191p'`.
   The later round-21 erratum (`:261-274`) is an append that touches only the §7 reproduce
   commands and says nothing above it was edited, so it neither displaces nor contradicts the range.
2. **ordinal 11 — `mutation-case-kimi-census.md:22-25` — holds.** Same sentence's kimi pointer
   (`SKILL.md:173-175`); `:22-25` states the one-exact-string-replacement defect, "the driver
   asserts the old string occurs exactly once before writing", "`mutate_driver.py --check` →
   `all unique`, first-line match on all 10", no compounding. Boundary recorded for the L1 (not
   a staleness call): "print the count" is implied by the `--check` gate output, not stated
   verbatim in this range; the gate itself is documented. Show:
   `git -C LANE show 8ca67421…:corpus/knowledge/mutation-case-kimi-census.md | sed -n '20,28p'`.
3. **ordinal 12 — `mutation-case-kagi-census.md:44-47` — holds.** The kagi half of the same
   clause; `:44-47` records the `cp -p`/`cmp`-verified pristine copy, the
   "old string occurs exactly once before writing" assertion, "`mutate_driver.py --check` →
   `all unique`, all 10", no compounding, original never written, no live host surface read.
   Boundary recorded for the L1: "first matching line" is documented for Kimi at
   `mutation-case-kimi-census.md:24`, not restated here — which is why the sentence cites both
   lanes. Show: `…mutate-case-kagi-census.md | sed -n '40,56p'`.
4. **ordinal 13 — `mutation-case-kimi-census.md:26-28` — holds.** `:26-28` is exactly the
   per-defect evidence bullet the clause names — full stdout → `evidence/<id>.selftest.txt`,
   exit code + mutant sha256 → `evidence/<id>.meta.json`, aggregate → `evidence/results.json`
   ("Historical Kimi records stdout, exit/SHA/results", `SKILL.md:185-186`); the file's total
   wall time is at `:30`, i.e. the clause correctly leaves duration to Kagi. Show:
   `…mutation-case-kimi-census.md | sed -n '26,31p'`.
5. **ordinal 14 — `mutation-case-kagi-census.md:48-49` — holds.** `:48-49` adds "wall time +
   case summary" to the same meta file, which is precisely the clause's "Kagi also records
   duration/summary" (`SKILL.md:186-187`); per-defect cost is corroborated at `:50-53`
   (~1.0 s each, 11.0 s wall over 11 runs). Show:
   `…mutation-case-kagi-census.md | sed -n '48,53p'`.

No row is `stale`/`unresolved`/`absent`, so per the item no `proposed_fix` is emitted: all five
rows carry `base_verdict: "holds"` and no correction is proposed. Pointer count for the section
is untouched by this seat (nothing deleted, nothing rewritten).

## Gates run (observed)

- Excerpt gate, self-tested before writing (the item's requirement): for every row the excerpt
  is a verbatim slice of the pointed lines, whitespace-collapsed to one space, length 191/269/366/195/197
  ∈ [24,400], and the collapsed excerpt occurs in the collapsed pointed text. Transcript:
  `.ufo/waves/round-49/w1/T49Read03.excerpt-check.txt` (also asserts each `claim` is a verbatim
  collapsed substring of base `SKILL.md`). Command that produced it: the inline `python3 - <<PYEOF`
  in this seat's session reading `git cat-file blob 8ca67421…:<file>`; the same script wrote the rows file.
- Claim verbatim check: all five `claim` strings collapse to substrings of collapsed base
  `SKILL.md` (`claim_in_base_SKILL=True`, lengths 78/109/109/85/71).
- Counter-compatibility check of my rows (static, no measure invocation): imported
  `list_pointers`/`check_reads` from `.ufo/evidence/round-49/c1/measure.py` and ran
  `check_reads(LANE, BASE, FLEET, pointers, {'rows': rows})`; my five ordinals report status
  `ok` (aggregate over all 90 base pointers: `unresolved=9, unverified=76, excerpt_miss=0,
  not_holds=0, absent=0` — the 76 unverified are the other sections' pointers, which this seat
  does not own, and the 9 unresolved are the base-state figure already recorded in
  `contract.json` `c1.before`).

## Touched surfaces

- Wrote `.ufo/waves/round-49/w1/T49Read03.rows.json` (5 rows, schema fields: heading, ordinal,
  raw, file, ranges, claim, base_verdict, verdict, excerpt, reader, note).
- Wrote `.ufo/waves/round-49/w1/T49Read03.excerpt-check.txt` (receipt for the excerpt/claim checks).
- Wrote this report `.ufo/waves/round-49/w1/T49Read03.md`.
- Lane checkout, jj state, Git index, fleet repo, shokuknow: unmodified. No fixture repo was
  needed, so no git mutation was issued anywhere.

## Out of scope / not done

- No verdict on C1 or C2; no deciding or measuring counter run (`measure.py` used only with
  `--list`, plus function imports).
- Did not read the hidden C2 panel, `~/.local/state/`, or
  `.ufo/evidence/round-49/control/c2-{WITNESS,CTL_FIX,CTL_ABSENT}.stdout`.
- Did not edit `SKILL.md` or the censuses; the section corrections in `SKILL.md` belong to the
  L1 integration (this seat reports zero required corrections for its five pointers).
- No tool install/upgrade was needed, so there is no channel entry to record.
- Scratch root `/fast/scratch/hyaku/tameshi-r49/T49Read03/` removed at exit; nothing cited here
  depends on a scratch path.

## Summary

Five recipe pointers (ordinals 10-14) read at base `8ca67421`, all target text located and quoted.
All five hold: kagi 184-191 (round-3 E1 miscalled counts), kimi 22-25 and kagi 44-47 (uniqueness
gate, `all unique`), kimi 26-28 (stdout/exit/SHA/results), kagi 48-49 (wall time + case summary).
No line drift, no stale pointer, no unresolved/absent target, therefore no proposed fixes.
Two boundary notes for the L1: "print the count" is implied by `--check` output, and "first
matching line" is recorded for Kimi only — both clause halves are covered by the cited pair.
Excerpts (24-400 collapsed chars) verified in-place; the counter's own `check_reads` marks my
five rows `ok`. Deliverable: `.ufo/waves/round-49/w1/T49Read03.rows.json`.
