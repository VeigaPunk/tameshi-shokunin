source: S001 — https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ — §§Mutant states, Metrics, page fetched 2026-10-19; S002 — https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json — MutantStatus and MutantResult, master fetched 2026-10-19; S004 — https://mutants.rs/using-results.html — §Mutant outcomes, fetched 2026-10-19; S005 — https://raw.githubusercontent.com/boxed/mutmut/main/HISTORY.rst — 3.8.0, main fetched 2026-10-19; S006 — https://raw.githubusercontent.com/BWBama85/shmutant/7eefc73010ad6342b80e3ed43915503e02c90618/README.md — §§The three verdicts, How a row is run, commit 7eefc73010ad6342b80e3ed43915503e02c90618
verified-at: 2026-10-19
recheck: 180d — `curl -fsSL 'https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/' | grep -c 'detected / valid'` (ran; 1)
ground: F1 — external mutation-score semantics + report interop (tameshi-art.md §4)

# Mutation-score semantics across tools

## Verdict vocabulary map

This maps outcome names, not interchangeable policies. Tameshi's rule is red **and** the full case count for Killed, green with the same count for Survived, and no definitive verdict for Inconclusive; only Killed and Survived enter its rate (`SKILL.md:191-213`).

| Tameshi | Stryker | cargo-mutants | mutmut (opened changelog only) | shmutant |
|---|---|---|---|---|
| **Killed** — red + full count (`SKILL.md:191-194`) | **Killed** — at least one test fails (`S001 §Mutant states`, S001.html:11-12) | **caught** — a test fails (`S004 §Mutant outcomes`, S004.html:192-194) | No general verdict mapping in this changelog; it records only a timeout misclassification fix (`S005 HISTORY.rst:23`). | **killed** only if the named witness fails; red elsewhere is **accidental**, not a kill (`S006 §The three verdicts`, README:21-39). Tameshi records failing labels but no per-mutant witness, so its Killed cannot be split into these two (`SKILL.md:195-197`; S006 README:23-31). |
| **Survived** — green + full count (`SKILL.md:205-206`) | **Survived** or **NoCoverage** are both undetected; Stryker distinguishes them by test coverage (`S001 §Mutant states`, S001.html:13-16; §Metrics, :41-46). | **missed** — no test failed; docs say this may be a gap or an indistinguishable mutant (`S004 §Mutant outcomes`, S004.html:197-200). | No general mapping documented by the opened history (`S005 HISTORY.rst:1-46`). | **survived** means green (`S006 §The three verdicts`, README:27-31). |
| **Inconclusive** — timeout, crash before summary, or missing count is not a kill and is excluded (`SKILL.md:208-212`) | **Timeout** is counted as detected; runtime/compile errors are not in the score (`S001 §Mutant states`, S001.html:17-31; §Metrics, :39-52). This intentionally differs from Tameshi. | **unviable** means it does not compile and is inconclusive about test coverage; **timeout** is a separate outcome (`S004 §Mutant outcomes`, S004.html:203-209). | A CPU-time-limited mutant had been reported as killed instead of timed out; 3.8.0 records fixing that (`S005 HISTORY.rst:4-5,23`). | **timeout**, **aborted**, **unsettled**, and **lost** are runs with no trusted answer (`S006 §The three verdicts`, README:41-46). |
| **Setup / not-run guard** — a red control has no denominator; a non-unique mutation is refused (`SKILL.md:145-149,341-344`). | **Pending** (generated but not run) / **Ignored** (not tested); neither enters `valid` (`S001 §Mutant states`, S001.html:9-10,32-34; §Metrics, :45-52). No direct Tameshi tally equivalent is recorded. | **unviable** means compile failure rather than caught/missed (`S004 §Mutant outcomes`, S004.html:203-205). | Not specified by the reopened changelog (`S005 HISTORY.rst:1-46`). | **unapplied** (old literal matched nothing) and **baseline** (selected tests were not initially green) are harness guards, not mutant outcomes (`S006 §The three verdicts`, README:33-39). |

Stryker's report schema enumerates eight statuses—`Killed`, `Survived`, `NoCoverage`, `CompileError`, `RuntimeError`, `Timeout`, `Ignored`, `Pending`—and requires each mutant's `id`, `mutatorName`, `location`, and `status` (`S002 mutation-testing-report-schema.json:41-46,88-100`). The exact source quotes, fetched URLs, access timestamps and SHA-256 values for all five reopened sources are retained in `.ufo/evidence/kaika-round-1/score-semantics/opened.tsv`; fetched bodies are retained there as `S001.html`, `S002.json`, `S004.html`, `S005.rst`, `S006.md`.

## Formula comparison

For the same valid mutant set, let `k` = killed, `s` = survived (including any NoCoverage mutants for the all-valid total), and `t` = timeouts. Tameshi uses `k/(k+s)` and excludes inconclusives (`SKILL.md:208-212`). Stryker defines detected as `k+t`, undetected as `s` (Survived + NoCoverage), valid as detected + undetected, and score as `detected/valid`; its compile/runtime errors are invalid and excluded (`S001 §Metrics`, S001.html:39-52; §Mutant states, :23-31). Thus, when the comparison contains only these valid outcomes, Stryker total score is `(k+t)/(k+s+t)`. Do not silently compare denominators if compile/runtime errors, ignored/pending mutants, or other unclassified cases are present: Stryker excludes them but Tameshi's formula does not define a corresponding bucket (`S001 §Metrics`, :45-52; `SKILL.md:208-212`).

For `k+s>0`:

`(k+t)/(k+s+t) - k/(k+s) = (t*s)/((k+s+t)(k+s)) >= 0`.

This is an inference from the cited formulas. The two total scores are equal exactly when `t=0` **or** `s=0` (with defined denominators); the `s=0` case matters even if timeouts occur. Stryker's separate covered-code score uses `covered = detected + survived`, so with `n` NoCoverage mutants among `s`, it is `(k+t)/(k+t+s-n)` (`S001 §Metrics`, S001.html:41-54). It is at least the overall score; a numeric covered-code score cannot be inferred without coverage-traced `n`.

## Six recorded cases, recomputed

Each note records no inconclusive runs, so `t=0` for this comparison and both overall formulas reduce to the same displayed arithmetic. Counts below are `(killed, survived, inconclusive)` from the case's verdict table/headline; survivor classes are included rather than discarded.

| Recorded case | Recorded `k/s/i` and survivors | Tameshi `k/(k+s)` | Stryker `(k+0)/(k+s+0)` |
|---|---|---|---|
| JS Kimi census | `8/2/0`; D2 truncation, D10 reported constant (`mutation-case-kimi-census.md:29-53,101-107`) | `8/(8+2)=8/10=80%` | `(8+0)/(8+2+0)=8/10=80%` |
| Bash Kagi surface census | `8/2/0`; B5 fixture-absent exec arm, B10 unasserted summary count (`mutation-case-kagi-census.md:50-76,107-127`) | `8/(8+2)=8/10=80%` | `(8+0)/(8+2+0)=8/10=80%` |
| Bash Tsukuroi census | `6/4/0`; B7 cap, B8 usage exit, B9 reported fields, B10 unreached PCI arm (`mutation-case-tsukuroi-census.md:64-103,132-168`) | `6/(6+4)=6/10=60%` | `(6+0)/(6+4+0)=6/10=60%` |
| Bash Mado verify | `4/6/0`; D3, D5, D7, D8, D9, R1 (`mutation-case-mado-verify.md:57-89,101-147`) | `4/(4+6)=4/10=40%` | `(4+0)/(4+6+0)=4/10=40%` |
| Bash Kagi checklist | `7/8/0`; A1, B1, B3, C1, D1, E2, F2, G1 (`mutation-case-kagi-checklist.md:107-132,173-195`) | `7/(7+8)=7/15=46.666…%` | `(7+0)/(7+8+0)=7/15=46.666…%` |
| JS Kumitate claims | `7/3/0`; D7 cap, D8 assert-blind threshold, D9 unreached arm (`mutation-case-kumitate-claims.md:62-99,137-173`) | `7/(7+3)=7/10=70%` | `(7+0)/(7+3+0)=7/10=70%` |

Recorded sweep commands for the six tallies (quoted from each case note; not rerun for this entry):

- Kimi `8/2/0`: `python3 /tmp/tameshi-r2-1-work/mutate_driver.py --run` (`mutation-case-kimi-census.md:174-175`).
- Kagi surface `8/2/0`: `python3 /tmp/tameshi-r3-1-work/mutate_driver.py --run` (`mutation-case-kagi-census.md:245-246`).
- Tsukuroi `6/4/0`: `python3 mutate_driver.py --run` from `/tmp/w5-tameshi-1-work/` (`mutation-case-tsukuroi-census.md:379-380`).
- Mado `4/6/0`: `bash tameshi-shokunin/tools/mutate-and-run.sh --target mado-shokunin/tools/mado-verify.sh --defects /tmp/w6-tameshi-mado-verify/spec/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/w6-tameshi-mado-verify/sweep --label mado-verify.sh --tail 14` (`mutation-case-mado-verify.md:284-288`).
- Kagi checklist `7/8/0`: `bash tool.sh --target /tmp/w8-tameshi-t81/pristine-checklist-run.sh --defects /tmp/w8-tameshi-t81/checklist.spec --suite 'bash "$MUTANT" --selftest' --label kagi-checklist --workdir /tmp/w8-tameshi-t81/sweep` (`mutation-case-kagi-checklist.md:282-285`).
- Claims `7/3/0`: `bash tameshi-shokunin/tools/mutate-and-run.sh --target /tmp/w8-t8-2-claims/claims-check.pinned.mjs --defects /tmp/w8-t8-2-claims/spec/claims-check.defects.spec --suite 'node "$MUTANT" --selftest' --workdir /tmp/w8-t8-2-claims/work --label claims-check.mjs --tail 14` (`mutation-case-kumitate-claims.md:369-373`).

These recomputations agree with the lane's recorded six-leg ledger: `8/10, 8/10, 6/10, 4/10, 7/15, 7/10` (`tools/mutate-and-run.sh:84-92`). The recipe's band readings remain report conventions, not pass/fail gates (`SKILL.md:314-340`). No covered-code score is claimed for these cases: their notes do not retain Stryker-style per-mutant coverage classifications.

### Possible Stryker NoCoverage candidates (U, not verdict conversions)

Stryker calls a mutant NoCoverage only when no test covers it; the state is distinct from Survived (`S001 §Mutant states`, S001.html:13-16). The case notes do not include coverage traces, so these are candidates only, not measured Stryker statuses:

| Case-note survivor(s) | Why it is a candidate | Evidence |
|---|---|---|
| Kagi surface census B5 | Fixture-absent exec x-bit arm | `mutation-case-kagi-census.md:107-116` |
| Tsukuroi B8, B10 | No CLI usage-refusal case; PCI-unreadable arm unreachable in fixtures | `mutation-case-tsukuroi-census.md:96-99,144-164` |
| Mado D5, R1 | No failing-selftest exit case; no TOML-unavailable scenario | `mutation-case-mado-verify.md:84-89,121-143` |
| Kagi checklist F2, G1 | No broken `--only` case; no unknown-argument case | `mutation-case-kagi-checklist.md:125-128,188-190` |
| Kumitate claims D9 | Unresolved-note arm is not entered by any fixture | `mutation-case-kumitate-claims.md:94-99,160-169` |

Kimi D2's high-findings boundary is fixture-unreached, but its note's erratum says D2 itself is assert-caused rather than an unreached-arm survivor; do not infer NoCoverage from that boundary alone (`mutation-case-kimi-census.md:82-92,223-230`). More generally, absent coverage traces, even an apparent code-path gap is not enough to relabel a recorded Tameshi Survived as Stryker NoCoverage. NoCoverage would remain in Stryker's **overall valid** denominator but is excluded from its covered-code denominator (`S001 §Metrics`, S001.html:41-54).

## Rejected rule: “count Timeout as a kill”

Rejected for Tameshi's recorded score: a kill requires red **and** an enumerated full count (`SKILL.md:191-193`), while a timeout or run without a definitive summary is Inconclusive, not a kill (`SKILL.md:208-209`). A timed-out run therefore supplies no Tameshi kill/survivor denominator evidence; do not turn it into `k` or `s`. Stryker's Timeout-as-Detected policy is real but different (`S001 §Mutant states`, S001.html:17-22; §Metrics, :39-52). Flip only if the local scoring contract explicitly adopts that timeout-as-detected policy and records timeouts as a declared valid denominator category; merely observing a timeout is insufficient.

## Report interop and O / I / U

- **O:** S002 was reopened and retained. Its schema requires thresholds and files at the report root, and each file carries language, source and mutants (`S002 mutation-testing-report-schema.json:6-8,19-27,41-46,152-172`). Rechecks for S001, S002, S004, S005 and S006 each returned `1`; commands and outputs are in `opened.tsv`.
- **I:** A Tameshi-to-Stryker report adapter can map only a measured `Killed`/`Survived` result directly; `NoCoverage`, `Timeout`, invalid, ignored and pending need explicit coverage/status evidence and policy. The six arithmetic comparisons do not establish those additional statuses.
- **U:** `python3 -c 'import jsonschema; print(jsonschema.__version__)'` failed with `ModuleNotFoundError: No module named 'jsonschema'`. No report JSON was emitted or schema validation claimed; the exact availability check is retained in `.ufo/evidence/kaika-round-1/score-semantics/schema-validation.txt`. Coverage-traced NoCoverage counts and all six covered-code scores are also unknown.

## Errata (append-only)

none
