# T51W2CritQualityMistake — QUALITY 102 / mistake-row falsifier review

Axes: calibration (scope and evidential restraint), depth (whether verdicts are actually falsifiable), operability (whether the check can be run and interpreted).

## Findings

### F1 — The evidence contains a real, one-variable red/green falsifier, but the draft check is not yet a runnable checker

The pair's actual commands are directly inspectable in `.ufo/waves/round-51/w1/T51LabSandboxLeak/red-gone-id.sh` and `green-gone-neutral.sh`; the receipt documents the reproduced suite command (`README.md:3`) and exact pair outcomes (`:39-42`). The former uses `sandbox-K_GONE_ARM`, prints `DRIFT_SELFTEST: PASS (13 cases)`, rc 0; the latter uses `sandbox-n2`, prints `FAIL symbol gone: no /GONE/ in output`, rc 1. The target and mutant are held constant, and path is the manipulated variable. Thus this is a valid discriminating fixture pair for a checker, not merely a verbal assertion. It is NOT evidence that the checker itself exists or has been run: QUALITY 102 currently specifies desired output `ORACLE_NAME ...` but gives no implementation/command, and the lesson explicitly says `none` under captured-by (`corpus/lessons/round-51.md:34`). `QUALITY.md:1558` says what must happen, but does not implement the paired check. Do not claim criterion 102 has been operationally satisfied based on the artifact scripts alone.

Exact manual invocations, from a disposable working directory with their documented environment:
```
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/red-gone-id.sh
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/green-gone-neutral.sh
```
Expected rc 0 then 1, respectively; captured output files are `.ufo/waves/round-51/w1/T51LabSandboxLeak/red-gone-id.out` and `green-gone-neutral.out` (exit receipts `.exit`). Evidence pointers: report §3-5, receipt README `:39-47`, raw `raw/K_GONE_ARM-A-r1.out` and `raw/K_GONE_ARM-B-r1.out`.

### F2 — Three named path-masked mutants are exact in the reported experiment; they are not a general count of all masked cases

A/B differs only in sandbox naming, with all ten rebuilt mutant SHA-256 values matching the sweep (`README.md:3`; `mutants-sha.csv`). Across three repeat runs each, exactly K_GONE_ARM, K_AMBIG_GT, and K_SHAPE_OPTIN change A=survived/rc0 to B=killed/rc1; K_MODE_CMP and K_COUNT_GE remain killed; five hole-aimed survivors and pristine control remain unchanged (`README.md:5-37`; `T51LabSandboxLeak.md:52-63,97-107`). The counterexample for accidental overstatement is scope: only named cases in this ten-mutant suite were tested, and some C-form entries are intentionally absent (C path-word tests the two previously killed mutants and K_GONE_ARM). So “exactly three” is supported for this dataset/design, not every drift-pins selftest case or every conceivable path spelling.

Reproduce the stored raw evidence without changing anything:
```
cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/README.md
cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/raw/K_GONE_ARM-A-r1.out
cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/raw/K_GONE_ARM-B-r1.out
cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/raw/K_AMBIG_GT-B-r1.out
cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w1/T51LabSandboxLeak/raw/K_SHAPE_OPTIN-B-r1.out
```
The fixed-target mechanism is also grounded in the pinned source facts: output captures stdout+stderr (line 399), expected token is an unanchored `grep -q` (403), and DRIFT prints absolute path (158); report `:67-87`. This is stronger than merely correlating names and outcomes.

### F3 — Negative controls stayed unchanged in A/B/C for the two already-killed mutants; the mistake row's additional three exit-only controls are supported only by separate reports

K_MODE_CMP and K_COUNT_GE stay KILLED in all tested forms, including deliberate verdict-word paths (`T51LabSandboxLeak.md:54,57,89-93`; receipt README `:11-23`). The five hole-aimed survivors and pristine control stay as recorded across A/B (`:59-60`). The lesson additionally calls `js-round-gate`, `js-sources-check`, and `js-cite-check` unchanged under naming changes (`corpus/lessons/round-51.md:72-75`), but those are separate path-variation studies, not rows in this A/B/C matrix. Their references (`T51LabLeakRoundgate.md` §4, `T51LabLeakSourcesCheck.md` results, `T51LabLeakCiteCheck.md` findings 1-2) must remain distinct evidence; do not cite this matrix as proving those controls. A broad “any check flags one” rule could falsely reject a legitimate exit-status-only oracle that never consumes path text. Criterion 102 currently limits itself to self-tests searching captured stdout/stderr for expected tokens, which avoids that false positive.

### F4 — Criterion 102 is directionally right, but its quantifier and execution contract need tightening

The criterion's scope is the right one-variable class: mutation cases with output-token oracles over output that may contain harness-generated paths (`QUALITY.md:1552-1554`). It should not require *all* self-tests or all fixtures to be renamed; those are not exposed to this specific oracle-input channel. Conversely, “for every mutation-suite case that asserts a verdict word in captured output” is underspecified: it does not define how to discover such assertions, whether token matching is anchored/structured, which paths count (TMPDIR, cwd, HOME, mutant name), how to handle multiple output tokens, nor how neutral/hostile paths are proven to be the only changed input. Without an executable inventory, one operator can omit the vulnerable case and still produce an apparently complete check. “Their verdicts must agree” is also too strong as a universal correctness condition if a target deliberately branches on its configured path; the relevant criterion is whether the *oracle's observed expected token* can be supplied by path text, not arbitrary path sensitivity.

Smallest safe refinement: require an enumerated case list of output-token oracle sites and the captured streams/paths each oracle consumes; for each, construct paired otherwise-identical executions where the hostile token occurs only in harness-controlled path text, then assert the same case-level verdict and report both raw outputs/exit codes. Make the check's discovery/review boundary explicit (source scan plus declared cases; no claim of automatic completeness unless tested). Preserve independent exit-code-only controls as controls, not in-scope cases. This catches the demonstrated bug while avoiding universalizing the 3-of-10 result.

## Evidence and limits

Primary: `.ufo/waves/round-51/w1/T51LabSandboxLeak.md` §§2-5; `.ufo/waves/round-51/w1/T51LabSandboxLeak/README.md` and its `raw/` files; `corpus/QUALITY.md:1550-1558`; `corpus/lessons/round-51.md:30-35,64-75`. This review reads the committed evidence and scripts; it did not rerun the mutation suite or invoke the counter. No claim is made that the still-draft criterion checker has been implemented or that every possible path-sensitive oracle is enumerated.
