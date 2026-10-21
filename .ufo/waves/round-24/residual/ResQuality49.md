# ResQuality49 — round24 residual critic: QUALITY48 execution note and criterion 49

Seat: TameshiR24-2.ResQuality49-5 (critic). Mode: read-only inspection; this item has no "Run" clause, so no tool, selftest, ruler or mutant was executed. Outcomes I derived but did not execute are marked [INFERENCE]. Inspected tree: lane worktree at HEAD 4903959687d16623adeeeae059bc010dcfc9d23f (untracked: `final-verification.json`, `residual-dispatch.json`; neither is cited here). No tools were installed or updated.

## Verdict

**49 is partly falsifiable. Its falsifier rests on one retained executed seat report. Its rule has three defects, and the lesson row that cites it is not "shown able to fail" by the repo's own standard.**

1. **Falsifier: holds.** It is backed by retained executed evidence, from one source only. MutProject M05 shows the selftest `external` case failing at 9/10, while the frozen K10 stays discriminated (exit 0, T/T/T/T). The tool and ruler bytes are identical at c8c5b88 and 4903959, so the claim can still be re-executed and could still come out false.
2. **Falsifiability: partial.** The falsifier tests the motivating defect, not whether a body of work applies the rule. Two parts have no stated consequence and no check: the "counts once, for the conjunction only" tally and the "record each predicate's expected failing case" duty.
3. **Defect A: the mandated row order is the blind order.** "Offending row comes after a clean row" kills first-row-only mutants. It does not kill last-wins or last-row-only mutants. PredK4 shows this exact blindness for the per-token loop: the only multi-token case put the missing token last.
4. **Defect B: the falsifier's own exemplar does not conform.** The selftest `external` fixture it relies on is a single-row per-row fixture. Under 49's own row-order clause, the `external` disjunct therefore has no conforming fixture at 4903959. Erratum F still credits it as "the selftest only".
5. **Defect C: the rule misses most of its cited evidence.** 49 cites MutFixtures and the K2/K3/K4 weakenings, but its closed list of trigger kinds does not reach them: per-token loops, sign-blind or truthiness exit comparison, case-folding.
6. **Duplication and contradiction.** 49 does not contradict 15, 25, 29 or 47. Its last sentence duplicates 15 (and 48's "named mutant"). It reuses QUALITY29's term "covered" without citing 29. The unnumbered QUALITY48 execution note narrows 48's literal rule (K7–K11 "not a repair") without saying so.
7. **Mined-mistake row: not shown able to fail.** The repo standard is one oracle failing on the defect and passing on the fix. The row's MutProject half shows a pre-existing selftest doing that, not any check built under QUALITY49. Its MutPlan half shows only survival, a check that cannot fail.

## Evidence

### Q1: does the falsifier rest on retained executed evidence?

- The falsifier text is at `corpus/QUALITY.md:520-523`.
- MutProject (`.ufo/waves/round-24/w1/MutProject.md`) is committed at 4903959 (blob `f1028ecf…`). Its seat callback is listed as completed in `.ufo/waves/round-24/outcomes1.json`.
- Clone and identities, `MutProject.md:18-35`: c8c5b88, `tools/registry-replay.py` sha256 `9fcd2dbb…`, `measure.py` sha256 `0a7f6daa…`.
- M05 diff, `MutProject.md:697-701`: `if row.get('external') is True or result.get('non_hermetic_argv'):` → `if result.get('non_hermetic_argv'):`.
- Captured selftest stdout, `MutProject.md:704-717`: `CASE external FAIL`, `9/10 pass`, exit 1. The K7–K10 wrapper exited 0 with T/T/T/T (`MutProject.md:115, 720ff`).
- Restore hash: M05 is restored to P before M06 (`MutProject.md:141-142`).
- Frozen bytes are unchanged, checked with read-only `git show <rev>:<path> | sha256sum`:

  ```
  c8c5b88  tools/registry-replay.py  9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714
  4903959  tools/registry-replay.py  9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714
  c8c5b88  measure.py                0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64
  4903959  measure.py                0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64
  ```

**Limits.**

- It is a single executed source. `grep -l "CASE external FAIL\|CASE non-hermetic FAIL" w1/*.md` returns only `MutProject.md`. PredK10's W1/W5 K10 outcomes are explicitly `[INFERENCE]` (`PredK10.md:4,52,56`).
- K10 was observed through a wrapper that imports `measure.replay_rows()` (`MutProject.md:43,66`), not through the ruler's `main()`. That is faithful to the frozen predicate, but it is not a full ruler run.
- The mutant and raw streams are retained only as transcripts embedded in the report. The /tmp clone is gone. Round-12's standard is "Raw records and the mutant are retained; no temp-only pointer carries this claim" (`corpus/lessons/round-12.md:159-164`); this is met only in transcript form.
- The falsifier names one mutant, "remove-external", but concludes "not coverage of **either** disjunct". The other disjunct needs M06 (`MutProject.md:116`), which the falsifier does not cite. The mutant label also differs from the report's ID (`M05 external-disjunct-deleted`), and the lesson uses a third name ("remove-external-classification", `lessons/round-24.md:55`).

### Q2: is 49 falsifiable as written?

- **Falsifiable part.** The falsifier is a reproducible empirical claim about frozen bytes. If re-running M05 at 4903959 made K10 discriminate=false, or made the selftest pass, the claim would be refuted.
- **Untestable part 1.** No procedure says what 49 does to the round24 tally. It never states which K-predicates count for which trigger or conjunction, or whether 48's 10-moved count changes. So no observation can show a work product violating 49.
- **Untestable part 2.** "Record each predicate's expected failing case or finding" (`QUALITY.md:517-518`) has no sanction. K5/K6 record no failure reason (lesson Erratum F, `round-24.md:110-112`), yet nothing in 49 or the execution note says whether they still count.
- **Unclear term.** "Byte-versus-character choice" is listed as a trigger, but it is a representation choice. The fixture it implies (bytes > limit ≥ characters, as in MutProject's `"é"*5`, `max_bytes=8` witness at `MutProject.md:123`) is never named.

### Defect A: the mandated row order is the blind order

- **Rule.** `QUALITY.md:515`: "In a per-row fixture, the offending row comes after a clean row."
- **Retained evidence of the blind spot.** `PredK4.md:45,56,70` shows the per-token version. The "last-wins loop overwrite" survives because "the only multi-token case puts the missing token last". The seat's killing fix puts the missing token **first**. PredK4 was in-memory over JSON, with no tool executed (`PredK4.md:38`).
- **Counterexample on this tool [INFERENCE, derived from `tools/registry-replay.py:78-80`, not executed].** Move `findings, refused, live = set(), [], []` (line 78) inside the `for row in observations['rows']` loop (line 80); this is a one-location mutant.
  - A 49-conforming fixture `[clean, offending]` leaves the offending row's findings and live entry in place, so the mutant survives.
  - `[offending, clean]` resets them on the clean row, so the mutant is killed.
- **Same blindness for last-row-only and skip-first-row.**
  - `rows[-1:]` sees the offending last row and survives.
  - `rows[1:]` also sees the offending row (position 1) and survives.
- **Net effect.** 49's order is necessary against first-row-only mutants (PredK7:67, PredK9:55) but is exactly the order that hides last-wins mutants.

### Defect B: the falsifier's exemplar fails 49's own row-order clause

- The selftest builds every case with one row: `'rows': [row]` (`tools/registry-replay.py:198`). The `external` and `non-hermetic` cases are at `:204-205`.
- The guard sits inside the per-row loop (`:80, :99`).
- So under `QUALITY.md:515`, the selftest `external` case is a non-conforming per-row fixture. PredK10 W4 (`PredK10.md:55`) confirms the selftest "is also single-row; not caught".
- The falsifier offers that case as the coverage K10 lacks. Erratum F (`round-24.md:107-108`) credits "K10: dropping either live-dependent disjunct — the selftest only".
- Read strictly, 49 leaves both live-dependent disjuncts **uncovered** at 4903959, and the lesson does not say so.

### Defect C: the closed trigger list misses the cited evidence

- **The list.** `QUALITY.md:513-515` defines "several triggers" as a disjunction, a per-row loop, a byte-versus-character choice, or an alias-resolution step.
- **What it cites.** "Captured by" includes MutFixtures, and Erratum F covers K2/K3/K4. Their surviving weakenings fall outside every listed kind:
  - per-token argv prefix (`MutFixtures.md:44`);
  - `abs()` and truthiness exit comparison (`MutFixtures.md:45-46`; K3, `round-24.md:95-96`);
  - `argv[0]`-only case-folding (K2);
  - last-token-only and case-insensitive stdout matching (K4).
- **Consequence.** 49 grants these predicates full credit while citing their survivors as captured evidence.

### Q3: duplicate or contradict QUALITY15/25/29/47/48?

| Criterion | Relation to 49 |
|---|---|
| 15 (`QUALITY.md:61-67`) | Duplicate. 15's "A setup error with the expected exit code is not proof of the intended assertion" is the substance of 49's "expected failing case or finding, not just 'some failure'". 48 (`:491`, "selftest kill of a named mutant") and 46 (`:459`, "typed expected outcomes") repeat it too. No contradiction. |
| 25 (`:143-149`) | No overlap with 49. (48's append-only supersession bullet at `:497-498` restates 25's `superseded`/`superseded_by` rule. That duplication is pre-existing in 48, not 49.) |
| 29 (`:176-189`) | Compatible, since both are "only when" necessary conditions. 29 requires a selftest kill per one-defect removal. 49 adds trigger independence, which K8 shows is needed: K8 kills M02 (`MutProject.md:112`) yet misses "cleanup only when not held" (Erratum F, PredK8). But 49's unscoped "A guard … is covered only when" reuses 29's defined term without citing 29 and while saying it "Narrows 48", so "covered" now has two authorities. |
| 47 (`:472-484`) | Compatible. 47's "substituted-command pair" is a single-trigger, single-field fixture. 49 generalizes it without citing it. |
| 48 (`:489-501`) | 49 is consistent with 48's count (K10 still counts once). But the **execution note** (`:506-510`) contradicts 48's literal rule: 48 counts a gap repaired when its predicate "fails at the base revision and holds after the change". K7–K11 do exactly that (before.json `tool-absent` → after 11/11), yet the note says they are "not a repair". That narrowing is real and justified (CorpusQuality48 Counterexample, `w1/CorpusQuality48.md:62`), but it lives in an unnumbered note, not in 48 or 49. |

### Q4: is the lesson's mined-mistake row "shown able to fail"?

- **The standard.** The repo uses the phrase for one oracle that fails on the defective state and passes on the fixed state, with retained records:
  - `lessons/round-12.md:159-164`: exit 1, then exit 0 after restoring;
  - `QUALITY.md:132-134`: credited at `e69b488`, uncredited at `09ee1d0`;
  - `lessons/round-16-verifier-spotcheck.md:63,164`: 81/82 rc 1 against 83/83 rc 0;
  - this lesson's own after.json row (`round-24.md:54`): `git cat-file -e` 128, then 0.
- **The row** (`round-24.md:55`) claims its "Fix" is QUALITY49, which is prose. No QUALITY49-conforming check exists: the split single-trigger fixtures are "Routed to round25 (unexecuted)" (`round-24.md:150-151`).
- **MutProject half.** It shows the *pre-existing* selftest `external` case failing on M05 and passing on pristine. That is a red/green pair, but for a detector that predates 49 and, by Defect B, does not conform to it. Its K10 half shows a check that **cannot** fail. This is defect evidence, which belongs in the "Evidence pointer" column, not the "shown able to fail" column.
- **MutPlan half.** "M2 drop-sibling-realpath survives both selftest and K11" (`MutPlan.md:8,83,97`) shows that no detector fails. MutPlan does hold a genuine red/green single-trigger pair: its supplemental symlink-sibling probe exits 0 on pristine and restored, and 1 on M2 (`MutPlan.md:97,104-160`). The row does not cite it. That probe is also seat /tmp code, not a retained lane fixture.
- **Conclusion.** The row is not shown able to fail. It shows the defect is real (accurate) and that a single-trigger fixture can discriminate in two seat probes. It does not show the fix discriminating.

## Impacted axes

- Calibration: K10/K11 and the selftest coverage credit (Defects A, B).
- Provenance: the column semantics of the "shown able to fail" row.
- Duplicate authority: "covered" in 29 vs 49; 15 vs 49's last sentence; the unnumbered narrowing in the 48 note.
- Premature saturation: 49's closed trigger list (Defect C).
- No identity change or regression: frozen bytes are unchanged (hashes above).

## Smallest safe correction (append-only; no tool, fixture, ruler or registry change)

1. **Append a dated correction to 49 in round25** (do not edit 49):
   - "a per-row or per-token fixture places the offending element both first and after a clean element (or between clean elements)";
   - "this criterion's 'covered' adds independence to QUALITY29's kill requirement, which still applies";
   - "at 4903959 neither live-dependent disjunct has a conforming fixture: the selftest cases are single-row";
   - state that K2/K3/K4-class weakenings (per-token, sign or truthiness, case) are outside 49 and remain open under 29.
2. **Make the 48 execution note's narrowing explicit**, by numbering it or adding a 48 correction: "a base failure caused by tool absence demonstrates new capability, not repair".
3. **Lesson errata row for `round-24.md:55`:**
   - move the K10/M2 survival evidence to the "Evidence pointer" column;
   - set the "shown able to fail" cell to "not yet: no QUALITY49-conforming fixture exists (routed round25)";
   - cite the red/green pairs that do exist (MutProject M05/M06 selftest `external`/`non-hermetic` 9/10 against 10/10, `MutProject.md:115-116,141-142`; MutPlan symlink-sibling probe 1 against 0, `MutPlan.md:97`) as seat-probe evidence that single-trigger fixtures discriminate;
   - use the mutant IDs M05/M06, not prose labels.
4. **Optionally, have a "Run" seat re-execute M05 and M06 at 4903959.** This would give the falsifier an independent second executed source.
