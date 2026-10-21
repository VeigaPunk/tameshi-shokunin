# ScribeLimits — round24 C1 calibration: what the eleven predicates do NOT show

Lane: TameshiR24-2.ScribeLimits (leaf, no dispatch). Read-only. No commands were run and no production file was touched. Files were read from the working tree in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; I did not pin them to a revision.

Sources (abbreviations used below):
- **C** = `.ufo/evidence/round-24/contract.json`
- **K** = `corpus/knowledge/replay-projection-hardening.md`
- **L** = `corpus/lessons/round-24.md`
- **M** = `.ufo/evidence/round-24/measure.py`
- **B** = `.ufo/evidence/round-24/before.json`

## Verdict

The eleven predicates show that eleven named checks can each fail on a synthetic fixture at the time the ruler runs. They do not show that the hardening is complete, that the bundles are authentic, that the realpath logic isolates writes, or that the calibration score should move. The baseline is 1/11 at base 6a1821a, and the 11/11 target is only a target. No after-measurement is recorded in the sources I read.

## Plain-language list of what the predicates do NOT show

### A. Status of the measurement

1. **No after-state is shown.** The 11/11 figure is the target, not an observation (C:10-13). The lesson says the after measurement "is recorded below once executed" (L:53), and the knowledge entry says executed results go in the lesson and SCORECARD "only after execution" (K:2-3). Nothing in the sources I read records that execution.
2. **The 1/11 baseline is one row, and K4 is a control.** K4 was already killed at base, so it is not a repair (L:10-12; B:14). Only K1-K3 and K5-K11 are candidate repairs.
3. **The numeric score does not move.** Calibration stays at 8 and nothing is promoted (C:64; L:12-13). The predicates are "capability checks, not historical defects" (L:12-13; K:38-40). They are not an expertise score (M:11).

### B. Predicates K1-K4 (selftest mutants)

4. **Four mutants, not mutation adequacy.** K1-K4 count kills of four specific one-line guard weakenings (C:61; K:38; L:24; M:4-6). Other weakenings are not measured.
5. **A kill can come from any CASE line.** A mutant counts as discriminated when its selftest exits 1 and prints at least one `CASE ... FAIL` line (M:80-82). The rule does not check that the failing case is the one aimed at the mutated guard. An unrelated failure would also count.
6. **The anchor must match exactly once.** If the guard text in `command-binding.py` changes, the row becomes `inconclusive` and is not discriminated (M:73). A refactor can therefore lower the score without any change in behaviour.
7. **Strength depends on the selftest cases.** The kills come from whatever cases the pristine public selftest contains (M:69-70, 78). The ruler adds no cases of its own. The knowledge entry's example "a declared -15 that matches stays clean" (K:14) is not one of the ruler's own fixtures (M:24-37).

### C. Predicates K5-K6 (frozen bundle substitution)

8. **Substitution is self-consistent by construction.** The ruler writes a new bundle and a new expected file whose `bundle_sha256` matches the new bytes (M:107-116). The pin check therefore passes on what the ruler itself wrote. The predicate shows that a literal-digest pin is enforced, not that the original bundle is correct.
9. **The pin is not producer authentication.** "Neither the pin nor the gate authenticates the producer" (K:33-34). The same is said in L:25-26 and C:3.
10. **Row plus bundle changed together selects a new contract.** A later commit that changes both chooses a new contract (C:62; K:32-33). The predicates do not guard against that.
11. **Only active rows count.** The ruler only looks at rows with `status == active` (M:94). Superseded rows are still executed but do not count toward `held` (K:23-26), and the predicate does not measure them.
12. **K6 mutates stdout by appending a newline.** The change is `stdout + '\n'` (M:112). The predicate does not test any other kind of substituted content.

### D. Predicates K7-K11 (replay projection CLI on synthetic fixtures)

13. **Synthetic fixtures only.** K7-K11 test the CLI on fixtures the ruler writes itself (M:9-10; C:63). "An actual replay run is separate evidence" (C:63). Nothing in these predicates shows a real replay run.
14. **K7/K8 test only `held: false`.** The knowledge row says refusal happens when `held` is "not `true`" (K:17). The fixtures use only `held=False` (M:172-173). Other non-true values, or a missing field, are not tested.
15. **K8 uses a single cleanup string.** The fixture sets `cleanup_error` to one string (M:173). Other values, including a null or empty value, are not tested.
16. **K9 tests one size only.** The fixture sets `--max-stream-bytes 16` and sends 67 bytes (M:175). The default of 1 MiB named in K:18 is not exercised.
17. **K10 tests one row shape.** The fixture is one row with `external=True` and `non_hermetic_argv` (M:181). The row kind named "runner `non_hermetic_argv` rows" in K:19 is covered only for this one case.
18. **K11 uses only existing directories.** The fixtures create both sibling directories before the test (M:185-189). The non-strict realpath gap for missing components is not exercised (K:37; L:33-36, citing S084).

### E. Cross-cutting limits in the knowledge entry and lesson

19. **Realpath identity is not write isolation.** K11 shows identity normalisation only (K:35-37; L:22-24, 33-36). The rows run in a clone whose fleet mirror symlinks the live sibling repos (K:35-36), so symlinks are not a write barrier.
20. **The runner digest is not a predicate.** The row "runner digest from the live tree" is marked "recorded per run, not a ruler predicate" (K:21). None of the eleven measures it.
21. **Receipt metadata is not observed.** Receipt argv, cwd and revision are the invocation parameters that the instrument passes to the runner, not observed process metadata (K:30-31).
22. **Historical closure is not shown.** The predicates do not show that R17-CMD-BIND is closed, and they do not reopen or close any historical finding (L:22-23 gate rejects "fixed" before predicate fails at base and holds after).
23. **Two source items underlie the rules.** S084 is official Python documentation quoted in K:1 and L:31-36. S085 is the team's own round-23 adjudication (K:1; L:38-41). S085 is not independent evidence.
24. **Bounded lookup is minimal.** Identified 2, screened 2, included 2, excluded 0 (L:47). This is a source-count note, not a coverage claim.

## Smallest safe correction for the L1 report

Quote items 1, 4, 8-9, 13, 19-20 and 22 verbatim in the report's limits section, cite their lines above, and do not describe the after-state until an execution record exists.

## Tooling

No tool was installed, upgraded or executed. Reading was done with the `read` tool only.
