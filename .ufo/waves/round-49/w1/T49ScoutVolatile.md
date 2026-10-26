# T49ScoutVolatile — C1 durability recon (record-file append probe)

Question: which currently credited SKILL.md sections would lapse if one line were appended to each of LOG.md, SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md?
Base: `8ca67421111fa354b47b803358391d0b07fc6db9`. Monitor: `.ufo/evidence/round-21/coldread/measure.py` (wraps the round-18 credit algorithm, ledger `.ufo/evidence/round-21/coldread/ledger.json`).

## Answer

**None.** All 57 sections credited at base stay credited under every append variant. The monitor score stays 6 (57/64 covered) in every variant, and the per-section credited vector is identical to base's. The 7 lapsed sections stay lapsed.

- No credited section has a crediting entry that lists a record file in `inputs`. Count of crediting entries listing any of the five record files: 0.
- Sections whose only crediting entry lists a record file: **none** (0 of 57).
- Crediting entries per credited section: 36 sections have 1, 21 have 2 (`.ufo/waves/round-49/w1/T49ScoutVolatile.receipts/durability-recompute.json`, field `credited_entries`).
- The 7 uncovered sections are exactly the C1 targets, starts 131, 375, 1380, 1464, 1479, 1517, 1563 (recipe, restore, map, promotion, r12, r13, r14). Each has matching entries (13, 16, 13, 1, 17, 20, 14), and none of them credits at base.
- The lapsed sections' entries list record files. The monitor's base reason strings name `input-drift:LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md` and `corpus/SOURCES.md` for the recipe. For restore and map, `corpus/README.md` is the drifted record file. Promotion's drift is `reports/round-1-calibration.md` only (not a record file). Source: `.ufo/evidence/round-49/control/monitor-at-base-8ca67421.json`, `coldread.sections[]` `reason`.
- Appending can only turn more entries stale; it cannot create a veto. Aggregation is `covered = credited > 0 and not vetoes` (round-18 measure.py:638). A failing entry vetoes only if `not entry_is_stale` (measure.py:528, :632-636). A record-file append drifts an entry's inputs, so it becomes stale and stops vetoing. Not-credited sections gain nothing from this either.

Context: 231 of 497 ledger entries list a record file. All of them are older/superseded entries or sit on the 7 lapsed sections. None are the crediting entry of a currently covered section. This is why the exposure is already zero at base. C1 must keep it that way: its re-key entries for the 7 sections must list only non-record files (the contract's `work_plan` already says this).

## Method

1. Read the credit rule from the round-18 measure.py docstring: input gate at :47, aggregation at :72, `IGNORED_INPUTS` at :135 (SKILL.md plus the round-17/18 ledgers; the round-21 selector adds its own ledger path). The rule is per-entry: every recorded `inputs` key must be a git blob at REV whose sha256 matches. A single drifted key makes that entry `input-drift`.
2. Static recompute. `receipts/durability-recompute.py` imports the round-18 module read-only, takes `SKILL.md` and the round-21 ledger from `git show 8ca67421…`, sectionizes, matches entries by section `sha256`, and calls `entry_reason` / `entry_is_stale` / `entry_failure` at base. For each section it reports the crediting entries and which of the five record files appear in their `inputs`. Output: `receipts/durability-recompute.json`. Result: covered 57 of 64; crediting entries with a record input 0; sections with no volatile-free crediting entry none.
3. Empirical probe (not a verdict). A `git clone --shared` in scratch (`/fast/scratch/hyaku/tameshi-r49/T49ScoutVolatile`), detached at base, one commit appending `\nprobe line\n`. Variants: each of the five files alone (one1 LOG.md, one2 SCORECARD.md, one3 corpus/SOURCES.md, one4 corpus/QUALITY.md, one5 corpus/README.md) and all five together (`all`). Each was run as `python3 .ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <commit>` with `TMPDIR` in scratch. Every run exited 0 with score 6, 57/64 covered, and a credited vector identical to base. A second base run (`base2`) matched too. Receipts: `receipts/append-probe-runs.jsonl`.
4. The first attempt timed out after one4 (about 300 s). one5, `all` and base2 were rerun in a second command. The clone's resulting revisions are listed in the jsonl. The scratch clone is deleted.

Files in `.ufo/waves/round-49/w1/T49ScoutVolatile.receipts/`: `durability-recompute.py`, `durability-recompute.json`, `append-probe-runs.jsonl`.

## Limits

- The probe appended to the five record files only. It does not cover a rename or deletion of a record file, nor appends to other cited files (corpus/knowledge/*, tools/*). Those are separate drift sources and are not in scope here.
- The probe read blobs at a commit (the monitor reads no worktree). A worktree-only append without a commit would not change the monitor at all.
- No install or tool change was made.

## Summary
- Answer: no currently credited section lapses after a one-line append to LOG.md, SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md or corpus/README.md. All 57 stay credited.
- 0 of 57 credited sections have a crediting entry that lists a record file, so none is record-only. 36 sections have one crediting entry and 21 have two.
- Monitor probes in a scratch clone at base (each file alone and all five together): score 6, 57/64 covered, credited vector identical to base in every run.
- The 7 lapsed sections stay lapsed. Their entries carry the record-file drift (recipe, restore, map, r12, r13, r14); promotion drifts only on reports/round-1-calibration.md.
- 231 of 497 ledger entries list a record file, all non-crediting for covered sections. C1's re-keyed entries for the 7 sections must list non-record inputs only.
- Receipts are in `.ufo/waves/round-49/w1/T49ScoutVolatile.receipts/`. The scratch clone was removed. No lane or fleet writes beyond those.
