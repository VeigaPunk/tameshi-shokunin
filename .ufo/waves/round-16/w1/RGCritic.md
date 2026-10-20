# RGCritic — falsifying C1 (depth 6→7, `js-round-gate`) before it runs

Seat: TameshiR16.RGCritic (critic, wave 1). This is read-only: I ran no mutants and edited no lane files. Scratch: `/tmp/tameshi-r16-RGCritic-AjWk/` (holds a materialized blob only). No tool installs.

**Verdict:** C1 survives the attack if L1 meets the conditions below. I found no blocker to independence or province. The defects I found are fixable, and none of them is a tradeoff the judge must reject. The pre-registration, attribution and ledger claims are still unproven, and they become false if any falsifier F3–F9 fires. F10 is a live wave-1 hazard; I already messaged agent://TameshiR16 about it.

## Observations (commands, exits, key lines)

| # | Command / read | Result |
|---|---|---|
| O1 | `git -C kumitate-shokunin log -- scripts/round-gate.mjs` | Last touched by `364f1d5…` (2026-10-13). `git show {364f1d5,175de6ba,HEAD}:scripts/round-gate.mjs \| sha256sum` gives `f890e277…a834d3e9` for all three revisions. kumitate HEAD is `1770305f…`. `merge-base --is-ancestor` exits 0. `status --porcelain -- scripts/` is empty. So the pin is **current** and matches the blob that §13 read (`arm-class-matrix.md:301`). |
| O2 | `tools/mutate-and-run.sh:84-89` | Six ledger legs: kimi-census, surface-census, tsukuroi-census, mado-verify, checklist-run, claims-check. **round-gate is absent.** |
| O3 | Command D (`SCORECARD.md:73`) at HEAD `28aeef49…` | `recorded_cases=6 depth_score=6`. The worktree count is also 6. Tool sha (worktree = HEAD) is `75ed934d…`. |
| O4 | `arm-class-matrix.md:300-306` | §13 is "Projection, not measurement … no mutant was cut, no gate mode was executed … a projection cell is a probe candidate for a future round, never an admission". It was credited to **calibration** in r4 (`SCORECARD.md:17,45`), not to depth. |
| O5 | `SCORECARD.md:286-289` | Round 12 rejected "6 → 7" because "reanalysis of the same bash target is depth within a case, not a new independent case". `measure.py:32,41` adds the `unique_recorded_gates` guardrail, which is "not automatic duplicate-proofing" (`SCORECARD.md:314-315`). |
| O6 | Blob imports (`rg.mjs:130-137`) | Only `node:` builtins. There are no `from './…'` or dynamic imports, so round-gate shares no code with the kimi-census or claims-check legs. |
| O7 | `rg.mjs:702,725,1392` | The selftest re-execs `SELF = fileURLToPath(import.meta.url)` through `process.execPath`, so the mutant tests itself. The harness keeps the basename `mutant-<id>.round-gate.mjs` (`mutate-and-run.sh:430,454`), so the `.mjs`/ESM semantics are preserved. The default timeout is 300 s (`:166`). |
| O8 | `rg.mjs:1498-1508` | `passed = results.filter(r => r.ok)`. A **SKIP is pushed with `ok: true`** (`:1382`, when `KUMITATE_ROUND_GATE_NESTED === '1'`). The exit code is `passed === results.length ? 0 : 1`. |
| O9 | RGRecon pristine runs (`/tmp/tameshi-r16-RGRecon-io6Btu/run{1,2,3}.out`), tallied by me | Each run: PASS=60 SKIP=0 FAIL=0. Stdout sha256 prefixes are `d0c70160…`, `ea84ce51…`, `5433547a…`. The verdict is stable, but the stdout bytes differ between runs. |
| O10 | `PROVINCE.md:7-11,14-17` | Owns "the method, documented from the fleet's existing gates as primary surfaces — `kumitate-shokunin/scripts/*` (six gates …)". The rule is "Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)". Core (`:28-38`) lists only the six measured legs' gates. |
| O11 | `service-optin-protocol.md:26-30`, `plans/round-7.plan.md:16-20`, `fleet-suite-census.md:283` | The queue "drains only under a fresh opt-in", and the rule is scoped "at round-7 dispatch". round-gate **is** a queue row. |
| O12 | `git -C kumitate-shokunin grep -nIc -i tameshi HEAD` | 0 matches, so kumitate has recorded no opt-in. Precedent: claims-check (queue row `fleet-suite-census.md:285`) was swept in r8 with no opt-in in `mutation-case-kumitate-claims.md:1-30`. checklist-run records its missing kagi opt-in as U4 (`mutation-case-kagi-checklist.md:10-12,354-355`). Both are counted in D. |
| O13 | `ls /tmp/tameshi-r16-RGSpec{A,B,C,D}*`, `/tmp/tameshi-r16-survivorprep`; `find /tmp -maxdepth 4 -newermt 2026-10-20 -name results.tsv -o -name spec.copy` | Each directory holds only the pristine `round-gate.mjs`. No `results.tsv` or `spec.copy` exists. `pgrep` shows only pristine `node ./round-gate.mjs --selftest` processes. **I found no evidence of an early mutant run as of about 10:26 -0300.** |
| O14 | `pgrep -af mutate-and-run` | pid 142708 has cwd = lane root and runs `bash tools/mutate-and-run.sh --regression … --keep` (CR22, started 10:25:57) **against the live lane tool**. RGLeg's dispatch (`dispatch1.json`, RGLeg task) has it editing that same file in wave 1. |
| O15 | RGLeg dispatch text | The header line is `#   js-round-gate … @@RG_KILLED@@/10 (@@RG_PCT@@ %)`. The heredoc body is `@@R16_ROUNDGATE_SPEC@@` ("L1 substitutes the **measured** spec"), and `TABLE_ROUNDGATE='@@R16_ROUNDGATE_TABLE@@'`. |

## Falsifiers (numbered; each comes with the check that decides it)

**F1 — Independence (attack 1). Status: not falsified.** C1 would be a re-count, not a new case, if round-gate were already a ledger case, or shared code or a target with an existing leg, or if §13 had already earned depth.
- Evidence: O2 (absent from legs), O6 (no shared modules), O4 (§13 credited to calibration and explicitly "never an admission"). Same lane and same language as claims-check, which has precedent for counting as an independent case (O12).
- Decide at the measured REV with `python3 .ufo/evidence/round-12/measure.py --rev REV`. It must show `recorded_cases=7` **and** `unique_recorded_gates=7`. If `unique_recorded_gates` is less than `recorded_cases`, C1 is rejected.
- The case note must say the sweep *tests* §13 and does not re-credit it. The calibration axis must not count §13 a second time.

**F2 — Province (attack 2). Status: allowed, but the label is at risk.** The sweep is a read-only probe of a gate path that `PROVINCE.md:7-11` already names, under `:16-17`. It needs no opt-in **unless it is framed as a service or queue drain**. `service-optin-protocol.md:26-30` gates the *queue*, and round-gate is on that queue (O11).
- The claim is false-provenance if the note or the SCORECARD row calls the form "service", says the queue row was "drained", or implies owner consent. kumitate has 0 tameshi mentions (O12).
- Decide by `grep -nE 'service|opt-in|queue' <new case note>`. The engagement form must read **"tameshi-own read-only measurement (PROVINCE.md:7-11,16-17); no owner opt-in recorded (kumitate `git grep -c tameshi` = 0); owner intent U"**, and absorption must be recommendations-only.
- Also check that kumitate's `status --porcelain` is empty before and after the sweep, and that `git show HEAD:scripts/round-gate.mjs | sha256sum` still equals `f890e277…`.
- After the leg lands, PROVINCE Core (`:29-35`, "six recorded mutation legs") is inaccurate until an append-only Core line names round-gate (box 4; ProvinceBox4's lane).

**F3 — Predictions written after the run (attack 3).** Pre-registration is fake if no artifact with a fixed hash exists whose recorded time precedes the first `MUTATE_DATE`.
- Decide with: (a) the assembled 10-defect spec carries per-defect `# expect: K|S — reason (§13 line / target line)` comment lines, which spec v1 allows (`mutate-and-run.sh:306`). (b) Its sha256 appears in a message to agent://TameshiR16, or in a committed or `git hash-object -w` object, whose system timestamp is earlier than the sweep's `MUTATE_DATE`. (c) `sha256(spec.copy in the sweep workdir) == that sha`.
- File mtimes alone do not decide this; they are forgeable.

**F4 — Spec tuned to outcomes, or the predictions don't trace to §13.** This fires if any defect was swapped, re-worded or dropped after a mutant ran, or if a prediction labelled "from §13" has no §13 cell behind it.
- Decide with: (a) the defect IDs in `results.tsv` match the pre-registered ID set exactly, with the same `@old`/`@new` bytes. (b) The 15 RGSpec candidates and the 5 not selected are listed with their rejection reasons before the run. (c) Each prediction cites a §13 line, as RGMatrix's table does, or is labelled "seat inference, not §13". The ledger heredoc body must be **byte-identical to the pre-registered spec**, not a "measured spec": extract it at REV and compare sha256 with `spec.copy`.

**F5 — Low-information predictions inflate accuracy.** This fires if the hole-aimed mutants are chosen where survival is trivially certain while the §13 hypotheses stay untested. Example: `REPORT_MIN_BYTES` 1024→500 sits in the middle of the interval §13.4 projects, `[26, 1059]` (`arm-class-matrix.md:414-417`).
- Decide by checking the spec. A `REPORT_MIN_BYTES` defect must hit a **boundary**: 1059 (predict S) or 1060 (predict K). The composition (kill-aimed n / hole-aimed m) must be stated in the pre-registered spec, following the claims precedent (`mutation-case-kumitate-claims.md:72-79`).
- If F5 fires it is not grounds to reject depth, but the "15/15-style" accuracy claim must not be made.

**F6 — Survivors that are artifacts.** O8 shows that SKIP counts as a pass. A mutant that turns check 46 into a skip, or that removes checks, exits 0 with `N/N pass` and reads as SURVIVED. The suite's count is never asserted (§13.5.2).
- Decide by tallying `PASS/SKIP/FAIL` lines in every `evidence/<id>.out`. The pristine tally is 60/0/0 (O9). A survivor with SKIP>0 or a total below 60 is labelled "suite-shape survivor", not an assertion gap.
- Also record that `KUMITATE_ROUND_GATE_NESTED` is unset in the harness env, because a leaked `=1` silently skips check 46.
- Each survivor needs an off-suite non-equivalence witness: a run whose output differs from the pristine. Otherwise it is "possibly equivalent" and excluded from claims about assertion gaps.

**F7 — Attribution or hermeticity.** The case fails if kills come from the environment rather than the edit. Examples: the selftest reads the live `~/Projects/ufo-fsd-alpha` through `UFO_SRC`/`HOME` defaults (`rg.mjs:151-163`), or a timeout produces INCONCLUSIVE.
- Decide with: `CONTROL: GREEN`; inconclusive=0; `MUTATE_RESTORE: OK`; the pristine tally is 60/0/0; RGRecon/RGSentinel show no live-path reads (strace openat). The ledger expectation is exact (`mutate-and-run.sh:109-114`), so a single flaky timeout makes the leg FAIL later.
- O9 shows stdout bytes differ between runs. Repeat-control must therefore compare verdict and tally, not raw stdout. RGControl must say which.

**F8 — Command D counts a comment, not a leg.** Command D greps the header comment regex only (`SCORECARD.md:73`). A filled-in header line raises D to 7 even if the leg body, the `nlegs` count or the spec heredoc is broken or still has placeholders. If any `@@` placeholder survives, D stays 6 because `\d+/\d+` fails, so that case fails safe. A filled header over a broken leg is the real risk.
- Decide at the committed REV, never the worktree: `git show REV:tools/mutate-and-run.sh | grep -c '@@'` → 0. `tools/mutate-and-run.sh --selftest` → N/N PASS. `--regression` prints `REGRESSION: PASS (cases=7 passed=7 …)` with a `REGRESSION_PIN` for js-round-gate (git source `364f1d5…`, sha `f890e277…`), and the leg's measured row equals the recorded `TABLE_ROUNDGATE`.
- The recorded `@@RG_KILLED@@/10` must equal `killed=` in the sweep's `MUTATE: DONE` line.

**F9 — The swept tool differs from the recorded tool.** If the sweep runs on a half-edited worktree tool, `MUTATE_TOOL` pins neither HEAD (`75ed934d…`) nor the landed tool, so the run cannot be reproduced.
- Decide by recording the `MUTATE_TOOL` sha. It must equal `75ed934d…` (HEAD, which is unmodified) or the post-edit REV's blob. The `--regression` replay at REV then re-measures with the landed tool anyway.

**F10 — Wave-1 race (live hazard, messaged to L1).** O14: CR22 is running the live `tools/mutate-and-run.sh --regression` while RGLeg is assigned to edit that file.
- Cold-read seats that run the tool after the edit get a 7-leg tool with placeholders, which gives SETUP/FAIL. That would be misread as a SKILL wrong-expectation, which contaminates C2 calibration. [INFERENCE] An in-place rewrite during a running bash process can corrupt the run; an atomic rename cannot.
- Decide by comparing each CR seat's recorded tool sha with `75ed934d…`. Discard or re-run any cold-read verdict taken on a different tool sha.

## Evidence L1 must retain for the closure to admit depth 6→7 (attack 4)

1. Measured-REV and before-REV outputs of `measure.py`: `recorded_cases` 6→7 and `unique_recorded_gates` 6→7 (F1, F8).
2. The pre-registered spec: path, sha256, per-defect `expect` lines with §13 or "seat inference" citations, the composition line, and the list of rejected candidates. Its sha must appear in a timestamped record before `MUTATE_DATE` (F3, F4, F5).
3. The sweep workdir, kept: `MUTATE_TOOL`, `MUTATE_TARGET` (`f890e277…`), `CONTROL: GREEN`, 10 `DEFECT` lines, `MUTATE_RESTORE: OK`, `MUTATE: DONE … inconclusive=0`, `results.tsv`, and `spec.copy`, whose sha must equal item 2 (F3, F7, F9).
4. A per-defect PASS/SKIP/FAIL tally, and a non-equivalence witness for each survivor (F6).
5. A prediction-vs-measured table that keeps misses as errata and does not smooth them (precedent: `mutation-case-kumitate-claims.md:275-284`).
6. At REV: `grep -c '@@'` = 0; tool `--selftest` PASS; `--regression` `cases=7 passed=7` with the js-round-gate `REGRESSION_PIN`; the heredoc spec sha equals item 2 (F4, F8).
7. kumitate porcelain empty and HEAD blob still `f890e277…` before and after; the province label from F2; the SOURCES row(s) opened this round citing `364f1d5:scripts/round-gate.mjs` (F2).
8. The case note's independence sentence: a new gate path, and §13 tested, not re-credited (F1).

## Smallest safe corrections

- Change RGLeg's wording from "L1 substitutes the measured spec" to "the **pre-registered** spec, byte-identical, sha-checked against `spec.copy`" (F4).
- Freeze the assembled spec and post its sha256 to agent://TameshiR16 before the first mutant run (F3).
- Put a `REPORT_MIN_BYTES` boundary value in the spec and state the composition (F5).
- Add a tally column to the case table (F6).
- Label the form as tameshi-own read-only, with no opt-in, and do not describe it as a service-queue drain (F2).
- Keep cold-read seats on `git show HEAD:tools/mutate-and-run.sh` copies, or hold RGLeg's in-place edit until the cold-read runs finish (F10).

Impacted axes: depth (F1, F3–F9 gate the 6→7 claim), calibration (F10 contaminates C2; F4/F5 affect the honesty of prediction accuracy), adjacency/province (F2).
