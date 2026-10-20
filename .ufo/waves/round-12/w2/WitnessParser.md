# WitnessParser — parser and denominator completeness review (round 12, wave 2)

**Seat:** `TameshiR12.WitnessParser` (read-only reviewer, advisory; not an admission)
**Scope:** `tools/bash-witness-study.py` (1163 lines) and the denominator/label grammar it depends on: `.ufo/evidence/round-12/BashWitness/pristine.sh` (sha256 `275d8294…53009f`, matches PIN_BASH), `tools/mutate-and-run.sh` runner contract, and the wave-1 `BashDenominator.md` claims.
**Method:** static reading only. No parser, runner, selftest, or sweep was executed. One `sha256sum` on the evidence copy of `pristine.sh` (read-only hash).
**Tool installs/updates:** none.

Severity: H = can produce a wrong or unsupported classification, or destroys committed evidence; M = fail-open or silent acceptance on a reachable input; L = latent or hardening.

---

## High

**H1. `rerun` overwrites committed evidence, then always fails its own comparison.**
`cmd_rerun` (`tools/bash-witness-study.py:858-877`) calls `_execute_sweep` at :864. That helper writes the new summary to `evidence/summary.json` (:838) and the manifest (:839) before returning. The code then reads `committed = evidence/summary.json` (:865), which is now the fresh summary, and `fresh = rundir/summary.json` (:868). Nothing writes `rundir/summary.json`, so `read_text` raises `Cannot` (:200-204). Result: the committed `summary.json` is replaced, and `rerun` prints `CANNOT-EVALUATE` (:1157-1159). The agreement and deviation lines at :871-876 are unreachable. The docstring promise "compare with the committed summary" (:21-22) does not hold.
Fix: read the committed summary into memory before `_execute_sweep`, and write rerun output under the rerun directory instead of the committed path.

**H2. The sweep result is not gated on the runner's exit status or restore proof.**
`_execute_sweep` (:822-847) gates only on `sweep["control_green"]` (:825). It never checks `sweep["exit"]`, `sweep["restore_ok"]` (:547), or `sweep["done_line"]` (:548-549). Runner paths that end with `MUTATE: SETUP` and exit 2 after all rows are written are not caught. The clearest case is the byte-identity refusal, `MUTATE_RESTORE: DRIFT` followed by `die_setup` (`tools/mutate-and-run.sh` ~:500-503). Here `results.tsv` is complete, so `collect_results` (:553-597) succeeds, the summary gets `status: complete` (:835), and the study returns EXIT_OK (:847). The target changed during the sweep, and the study still reports a clean result.
Fix: require `exit in {0,1}`, `restore_ok`, and a `MUTATE: DONE|DEGRADED` line before classifying. Otherwise return `could-not-evaluate`.

**H3. `classify` has an unguarded fall-through to KILLED.**
`classify` (:411-429) treats any verdict that is not `SURVIVED` or `INCONCLUSIVE` as KILLED. The comment at :421 says `verdict == KILLED`, but the code never tests it. The runner emits only three verdicts (`tools/mutate-and-run.sh:32-33`, :485-489), so this is latent today. An unknown verdict string with a failing witness label would be counted `killed-on-witness`.
Fix: `if verdict != "KILLED": return "inconclusive", ["unknown-verdict:" + verdict]`.

**H4. No cross-check between the verdict, exit code, and log content.**
In the KILLED path, `classify` uses only `runinfo["bad"]`. It does not compare `runinfo["failures"]` (from the `SELFTEST` line, :380) with `len(runinfo["bad"])`. It also does not compare the runner's recorded `exit` (`results.tsv` field 3, read at :575, never used by `classify`) with the log's SELFTEST outcome. Pristine guarantees `failures == count(bad-case lines)` and exit 1 only on FAIL (`pristine.sh:754`, :846-847). A log with `SELFTEST: PASS` plus `bad-case` lines, or a mismatched count, is accepted as `killed-on-witness` when a declared label appears. The SURVIVED path does check `bad` (:416-417), so the two branches are asymmetric.
Fix: in `run_problems`, add `failures == len(bad)` and `(failures > 0) == (exit != 0)`.

---

## Medium

**M1. `collect_results` accepts duplicate and unknown defect ids.**
- Duplicates are not rejected. `seen` (:557, :593) is only used for the missing check (:594-596).
- `witnesses = declared.get(ident)` (:569) conflates "absent from declared.tsv" with "declared NONE" (`parse_declared_tsv` maps NONE to `None`, :344-345). An unknown id is therefore classified as `accidental` with reason `declared-NONE` (:425) and `declared_witness_none: true` (:579). No error is raised.
- `counts()` (:643-653) never compares `total` to the 10 declared rows.
Fix: reject duplicates and unknown ids, and assert `len(rows) == len(DECLARED_WITNESSES)`.

**M2. Case labels are not validated against the pinned catalog.**
- `CASE_RE` (:172) accepts any `\S+` name.
- `run_problems` (:388-408) checks only the total, numbering, and skip set. It does not check that names are the 16 catalog names or that each name appears once.
- The only catalog is the hand-typed tuple in `cmd_selftest` (:1000-1004). It is never compared with the target's selftest.
- The declared witnesses are not checked against the target at declare time. `cmd_declare` (:724-734) checks defect ids only.
- Duplicate names with different numbers pass the numbering check (:402). Example: `ok-case 01 clean` and `bad-case 03 clean`. That would falsely satisfy a `clean` witness.
Current status, verified by reading: all nine witness labels exist in pristine (`clean` :767, `asset-gone` :769, `runtime-absent` :770, `undeclared-file` :771, `crosscheck-disagree` :772, `symlink-swap` :773, `sqlite-unavailable` :783/:786, `malformed-row` :791, `fused-shape-row` :808). The spec's @old lines (`bad-case` spec at `tools/mutate-and-run.sh:631-669`) edit census code, not the selftest label text at `pristine.sh:694-847`. So the current mapping is consistent. The gap is structural: a mutant or a changed pin could rename or duplicate labels without detection.
Fix: at declare time, extract the case-name list from the target and assert that every declared witness is in it and that names are unique. At run time, assert the observed name set equals that list.

**M3. `check` fails open when `manifest.json` is missing.**
`cmd_check` (:938-951) prints a note when the manifest is absent and continues. It then prints `CLEAN` and returns EXIT_OK (:957-959). Deleting `manifest.json` makes `summary.json`, `sweep/`, and `sweep.cli.*` unverified while `check` still passes. The manifest is also unanchored: `declaration.json` (:752-786) does not pin its digest, so a rewritten summary plus a rewritten manifest also passes.
Fix: make a missing manifest a `Cannot` or `Fail`. Pin the manifest digest in `declaration.json` or in a committed file outside the evidence directory.

**M4. The manifest does not cover rerun outputs.**
`write_manifest` (:698-713) covers `sweep/` and only the literal names `sweep.cli.log` and `sweep.cli.exit` (:700). A `rerun-<stamp>/` directory and `rerun-<stamp>.cli.{log,exit}` (written by `run_sweep` at :538-539) are not covered, and `check` does not verify them.

**M5. `count` does not re-evaluate, despite its docstring.**
The docstring says `count` "re-evaluate[s] the retained sweep against the static declared TSV" (:18-19). `cmd_count` (:880-913) only verifies the declared digest and the declaration linkage (:889), then prints rows and counts from `summary.json`. It never re-runs `classify` and never compares each row's `declared_witness` with the current `declared.tsv` mapping. A summary whose rows were edited, with the manifest not re-checked, prints as authoritative.
Fix: either re-classify from the raw `.out` files and the declared mapping, or correct the docstring and state that `count` only reports `summary.json`.

**M6. Non-UTF-8 mutant output crashes the run and wedges the evidence directory.**
`read_text` (:200-204) catches only `OSError`. `UnicodeDecodeError` from `collect_results` (:568) propagates past `main` (:1152-1159), which catches only `Fail` and `Cannot`. The sweep directory already exists (:523), so later `run` refuses (:853-854) and `rerun` needs a new stamp. `run_sweep` decodes its own log with `replace` (:537), so the inconsistency is local to the per-defect read.
Fix: decode the per-defect logs with `errors="replace"`, or catch `UnicodeDecodeError` and classify the row as inconclusive.

**M7. An unparsed FAIL summary line crashes instead of being inconclusive.**
`parse_case_lines` line 380 does `int(m.group(3))`. `FINAL_RE` (:173) allows the denominator to be absent. In that case `group(3)` is `None` and `int(None)` raises `TypeError`, which `main` does not catch. Pristine always prints `FAIL (%s/%s cases)` (`pristine.sh:847`), so this is unreachable today. The synthetic tests (:1006-1026) never generate a FAIL line without a denominator.

---

## Low

**L1. `control_record` hard-codes `"exit": 0`** (:606). It is recorded as a fact, not read from the runner.

**L2. Unanchored gate substrings.** `control_green` (:546) and `restore_ok` (:547) use `in` over the full runner log. The runner's own gate is anchored (`grep -q '^CONTROL: GREEN '`, `tools/mutate-and-run.sh:1036-1037`). `print_tail` (`tools/mutate-and-run.sh:241-248`) writes suite output into the same stdout as `  | <line>`, so the substring can match suite output. Use `re.search(r"^CONTROL: GREEN ", log, re.M)`.

**L3. Every runner SETUP before the control line is reported as "control not green"** (:825-828). The runner's own reason (`MUTATE: SETUP (...)`) is lost from the summary and recoverable only from `sweep.cli.log`.

**L4. Spec-parser parity with the runner (latent).**
- `parse_spec` (:252-276) splits on `splitlines()`, and `extract_spec` (:237-249) uses the same. The runner splits on `\n` only (`tools/mutate-and-run.sh:303`). The target spec currently contains no CR or form-feed characters (checked by grep, zero hits), so this is latent.
- Comments: the parser skips only lines that start with `#` (:255). The runner skips lines where `line.lstrip().startswith('#')` (`tools/mutate-and-run.sh:306`). An indented comment is accepted by the runner and refused by the parser (fail-closed, but different).
- Empty `@old` and `@new == @old` are refused by the runner (`tools/mutate-and-run.sh:340-342`) but not by the parser. `spec_precheck` (:279-291) is non-blocking, so `declare` writes `declared.tsv` even when a literal is non-unique.

**L5. `collect_results` skips line 1 without checking it is the header** (:559). `int()` on `exit` and `duration` (:575-576) raises an uncaught `ValueError` on malformed input. Both are fail-closed (crash, not a pass), but not classified.

**L6. Environment scrub is incomplete.** `SCRUB_ENV` (:94) covers `THE_JANITOR_BIN`, `SQLITE3_BIN`, and `CENSUS_BREAK`. Cases 10 and 16 set their own variables explicitly (`pristine.sh:780`, :836). A grep of environment reads in `pristine.sh` (read-only, evidence copy) also finds variables that the sweep does not scrub: `DEEP` (`pristine.sh:584`, `${DEEP:-}` selects whether the verbs path skips or runs `op` probes; this is in the verbs path exercised by cases 15–16), `ONEPASSWORD_BROWSER_SUPPORT` (`pristine.sh:497`, sets the expected path for a verbs-path check), `FAKE_REF` (`pristine.sh:612`, inside a `sh -c` probe), and `TMPDIR` (`pristine.sh:274`, scratch location only, harmless). An operator who exports `DEEP` or `ONEPASSWORD_BROWSER_SUPPORT` changes case 15/16 behavior outside the pinned environment, and the skip-set guard (:404-407) would not catch a changed outcome on a host where both cases run. Fix: add these names to `SCRUB_ENV` and record them in `env_facts`.

---

## Verified as not contaminated (checked, no finding)

- **Diagnostic and tail lines do not leak into labels.** Pristine indents failure diagnostics with `    | ` (`pristine.sh:756`, :787, :812, :830), and `CASE_RE` is anchored at column 0 with no leading whitespace (:172). Runner tails (`  | `) are never parsed: labels come from per-defect `evidence/<id>.out` (:568).
- **Denominator is complete on every path.** I traced `pristine.sh:694-847`: nine `run_case` calls (cases 1–9), case 10 (:778), cases 11–12 (:789-790), case 13 (:791), case 14 (:803), and cases 15–16 on both the skip branch (:816, :822) and the run branch (:816, :834). Total 16, matching `DECLARED_TOTAL` (:92).
- **Skip contamination is guarded.** Skipped labels must equal `EXPECTED_SKIP_LABELS` (:93, :404-405) and the control's skip set (:406-407). Skipped cases do not increment `failures` in pristine (`pristine.sh:821-823`), and the parser never counts skips as bad.
- **Duplicate case numbers are caught** by `sorted(numbers) == range(1, total+1)` (:402).
- **Declared mapping ids** match the spec ids (`cmd_declare` :732-734; spec defects `tools/mutate-and-run.sh:631-669`, ids B1–B10).
- **Runner-to-parser file contract.** `results.tsv` (`tools/mutate-and-run.sh:478`, :493) and `evidence/<id>.out` and `control.out` (:425, :466, :470) match what the parser reads (:546, :565, :601).

---

## Gaps in the parser's own selftest (`cmd_selftest` :962-1109)

It does not cover: FAIL without a denominator (M7), duplicate or unknown labels (M1, M2), duplicate or unknown result ids (M1), a KILLED row with a PASS log (H4), a runner exit or DRIFT (H2), a missing manifest (M3), rerun (H1, M4), non-UTF-8 logs (M6), or `count` re-evaluation (M5). All 21 synthetic checks pass by construction against the parser's own fixtures (`.ufo/evidence/round-12/BashWitness/selftest.out`); that output is not evidence for any of the gaps above.

---

## Checks requested of the main agent (not run by this seat)

1. Reproduce H1 with a committed `summary.json` present and a `rerun` invocation; confirm the summary is replaced and the exit is `CANNOT-EVALUATE`.
2. Reproduce H2 with a runner `DRIFT` injection on a fixture target.
3. Add H3/H4/M1/M2/M7 cases to `cmd_selftest` before any study is declared on this leg.

## Residual risk

- The study has not been run in this round. `BashWitness/` contains only `pristine.sh` and `selftest.out`; `declared.tsv`, `declaration.json`, `summary.json`, and `manifest.json` do not exist yet. Any classification produced by the current parser should be treated as unvalidated until H1–H4 are fixed.
- Reviewer findings here are advisory. This is not an independent admission or promotion.
