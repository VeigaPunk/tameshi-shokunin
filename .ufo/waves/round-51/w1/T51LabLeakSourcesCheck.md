# T51LabLeakSourcesCheck — sandbox-id leak audit of recorded leg `js-sources-check`

- Seat: T51LabLeakSourcesCheck (leaf; no subagents)
- Round: 51 (hyaku 9), lane tameshi-shokunin
- Context: C2 (depth 9 → 10) leak mechanism — "suite names its sandbox `sandbox-$DEFECT_ID`; the gate's selftest checks verdict words with an unanchored grep over output that prints scratch paths; the defect id inside the path satisfies the grep"
- Item: audit recorded leg `js-sources-check` (tools/mutate-and-run.sh `regression_case_git js-sources-check`, line 1421-1424) for the same leak. Hypothesis to falsify: none of its recorded verdicts (TABLE_SOURCESCHECK, runner line 630) depends on the defect id appearing in the sandbox path.

## Method

1. **Pin materialization** (receipt: `T51LabLeakSourcesCheck/pin-materialization.txt`):
   - `git -C kumitate-shokunin show 0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs` (REV_SOURCESCHECK)
   - sha256 = `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` = PIN_SOURCESCHECK ✓
   - blob mode 100755 → `chmod +x` ✓
2. **Embedded spec**: extracted the heredoc `cat >"$d/js-sources-check.spec"` from the runner (lines 1026-1083) — 10 defects, ids K_KIND S_KIND K_EXIT S_VERDICT K_STRICT K_CLOSED K_ROWS S_DUP_LINE S_ENTRY_COUNT S_FILE_READ. All 10 `@old` strings verified count==1 against the pinned bytes (runner's `py_helper apply` and an independent parse).
3. **Sweeps**: ran the recorded runner itself (`tools/mutate-and-run.sh --target --defects --suite --workdir --label --timeout 300 --tail 60`) twice, same target/spec, single variable = sandbox directory name:
   - **variant A** (recorded suite, verbatim from runner line 1423): `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest`
   - **variant B** (neutral sandbox name): identical suite with `sandbox-$DEFECT_ID` → `sandbox-n$ORDINAL` (case-map K_KIND→1 S_KIND→2 K_EXIT→3 S_VERDICT→4 K_STRICT→5 K_CLOSED→6 K_ROWS→7 S_DUP_LINE→8 S_ENTRY_COUNT→9 S_FILE_READ→10; CONTROL→0).
   - Sandbox dirs observed on disk: A had `sandbox-CONTROL`, `sandbox-K_KIND`, … `sandbox-S_FILE_READ`; B had `sandbox-n0` … `sandbox-n10` — the variable was exercised as intended.

## Results

Control (pristine) green in both variants: exit 0, `SOURCES_SELFTEST: 46/46 pass`, restore OK (`MUTATE_RESTORE: OK`, target sha256 unchanged `6a293a…`).

Per-defect exit / verdict, variant A vs B (identical in every row):

| defect | A sandbox | A exit | B sandbox | B exit | verdict |
|---|---|---|---|---|---|---|
| K_KIND | sandbox-K_KIND | 1 | sandbox-n1 | 1 | KILLED |
| S_KIND | sandbox-S_KIND | 0 | sandbox-n2 | 0 | SURVIVED |
| K_EXIT | sandbox-K_EXIT | 1 | sandbox-n3 | 1 | KILLED |
| S_VERDICT | sandbox-S_VERDICT | 0 | sandbox-n4 | 0 | SURVIVED |
| K_STRICT | sandbox-K_STRICT | 1 | sandbox-n5 | 1 | KILLED |
| K_CLOSED | sandbox-K_CLOSED | 1 | sandbox-n6 | 1 | KILLED |
| K_ROWS | sandbox-K_ROWS | 1 | sandbox-n7 | 1 | KILLED |
| S_DUP_LINE | sandbox-S_DUP_LINE | 0 | sandbox-n8 | 0 | SURVIVED |
| S_ENTRY_COUNT | sandbox-S_ENTRY_COUNT | 0 | sandbox-n9 | 0 | SURVIVED |
| S_FILE_READ | sandbox-S_FILE_READ | 0 | sandbox-n10 | 0 | SURVIVED |

- Variant A reproduces TABLE_SOURCESCHECK exactly (5 KILLED / 5 SURVIVED, 0 flips, killed-delta 0) — the harness is the recorded sweep.
- Variant B verdicts and exits identical for all 10 defects; 0 differing defects.
- Every mutant sha256 matched precomputed expected hashes (independent apply).

## Finding

**Hypothesis not falsified: none of the recorded `js-sources-check` verdicts depends on the defect id appearing in the sandbox path.** No defect's verdict differs between `sandbox-$DEFECT_ID` and `sandbox-n<ordinal>` (one variable), so there is no defect to list per the item's "for each, the selftest assertion that matched the id" clause — no assertion matched an id.

Why the C2 mechanism does not bite here: the `js-sources-check` selftest (`sources-check.mjs` `selfTest()`, lines 571-898) is a verdict oracle of typed assertions on child exit statuses, parsed `SOURCES` lines (anchored `^SOURCES\s+(error|warn)\s+([A-Z_]+)\s`), counts, and `finalLine` verdict prefixes. No assertion does an unanchored grep over raw output that prints scratch paths, and the suite's stdout carries no scratch path (evidence files contain no `/tmp`/sandbox strings). There is no path-printing surface for a defect id to satisfy.

## Evidence

- `T51LabLeakSourcesCheck/pin-materialization.txt` — pin sha256, rev, mode, spec extraction source/line range
- `T51LabLeakSourcesCheck/variant-A/{sweep.log,results.tsv,defects.tsv,evidence/*.out}` — recorded-suite sweep (sandbox-$DEFECT_ID)
- `T51LabLeakSourcesCheck/variant-B/{sweep.log,results.tsv,defects.tsv,evidence/*.out}` — neutral-sandbox sweep (sandbox-n$ORDINAL)

Tools: no installs made (node v24.21.0, python3 3.14.8 present; official runner used as-is). No lane/fleet files touched outside the report and receipts above.

## Summary

1. Pinned `sources-check.mjs` @ 0acb7752 materialized; sha256 = PIN_SOURCESCHECK; mode 100755 preserved.
2. Embedded js-sources-check spec extracted (10 defects); every @old count==1 in pinned bytes.
3. Two sweeps via the recorded runner, single variable: sandbox `sandbox-$DEFECT_ID` vs `sandbox-n$ORDINAL` (dirs verified on disk).
4. Control green, restore OK in both; variant A reproduces TABLE_SOURCESCHECK exactly (5/5, 0 flips).
5. All 10 exits/verdicts identical across A and B — no defect's verdict differs.
6. No selftest assertion matched an id; the selftest oracle has no unanchored grep over path-printing output.
7. Hypothesis not falsified: recorded leg `js-sources-check` shows no sandbox-id leak (contrast with C2's drift-pins misses).
8. Receipts copied to w1/T51LabLeakSourcesCheck/; scratch cleaned.
