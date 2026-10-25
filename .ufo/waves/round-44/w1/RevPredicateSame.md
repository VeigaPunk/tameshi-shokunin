# Claim/predicate sentence review

## Axes
- C1: calibration.
- C2: freshness.
- This review concerns whether the written claim and counter predicate agree; no deciding measurement was run.

## C1
| Contract sentence | Counter predicate sentence | Printed label |
|---|---|---|
| `.ufo/evidence/round-44/contract.json:21`: “The lane's self-assessment records agree with the observed repo state across seven classes with total=0: classes m6 m7 m8 m10 m11 m12 m13 carried from round 43, and the round-43 false m7 alarm on the SCORECARD C3 receipt field safe_floor=S256 is resolved because an S-id bound to an assignment (key=S###) is a field value, not a citation, while genuine unknown and unmined citations still flag.” | `measure.py:37-39`: “Predicate C2_R44_PASS is true iff: self_pin=1, classes=7 (all seven declared classes ran — a counter that omits m12/m13 cannot pass), and m6=m7=m8=m10=m11=m12=m13=0.” | `measure.py:545`: `C2_R44_PASS=true` (emitted from `passed`; component output at :530-544 includes self_pin, classes, individual m-fields and total). |

**Same statement? No.** The contract sentence makes an additional behavioral claim: assignment-bound S-ids are values, and genuine unknown/unmined citations still flag. The predicate/label only assert the pinned seven-class zero-hit condition. The zero-hit condition is consistent with those behaviors but does not itself establish them; the contract is wider. The label also does not identify C1: it is named `C2_R44_PASS` despite the contract's C1 claim, and is explicitly the counter's predicate name.

Universal quantifiers: predicate uses “all seven declared classes ran”; `classes=7` is a constant rather than an independently enumerated class-run proof, and the docstring says evidence is each m-field (`:48-50`); implementation defines seven entries at `:527` and emits all seven at `:531-532`. This enumerates class fields but does not independently prove each routine ran beyond the code path. Contract “genuine unknown and unmined citations still flag” is universal in effect; m7 enumerates cited S-ids in the fixed `RECORDS`/newest SCORECARD+LOG records, not every possible repo citation (`:45-50`, `:506-507`), so scope is limited to those inputs.

## C2
| Contract sentence | Counter predicate sentence | Printed label |
|---|---|---|
| `.ufo/evidence/round-44/contract.json:41`: “S089's stale html-digest anchor in corpus/SOURCES.md is superseded by a new row S160 opened this round from the live Stryker equivalent-mutants page (sha256 79f6501a..., snapshot committed under .ufo/evidence/round-44/sources/stryker-equivalent-mutants.html), status mined, cited by a knowledge entry, with the old->new change logged in the round-44 lesson.” | `measure.py:37-39`: the `C2_R44_PASS` predicate is `self_pin=1`, `classes=7` and all seven m-fields zero. | `measure.py:545`: `C2_R44_PASS=true`. |

**Same statement? No.** C2 is a freshness/source-provenance claim; the label is solely the C1 record-agreement counter result. It does not test S160, S089, source digest/status, knowledge-entry use, or lesson logging. `contract.json:42` target specifies both a count of one S160 row and census validation exit 0; neither is in the C2_R44 predicate. This is a disjoint measurement, not a small paraphrase.

Universal quantifiers: C2 statement has no explicit all/every/no quantifier. Counter's universal “all seven” is as above and limited to its declared seven classes.

## Target wording check
The C2 target at `contract.json:42` is `grep -cE '^ {0,3}\\| S160 ' corpus/SOURCES.md -> 1 at the landing commit; sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi exit 0 at round end`. This review's available report-plan text (`SCORECARD.md:2076-2079`) is the planned-round-44 prose about staged adoption and guard refusal classes; it is **not equal** to the C2 target and does not mention S160 or the C2 census-validation command. No separate report-plan wording for C2 was located in the inspected round-44 evidence/wave paths; therefore equality with a distinct plan sentence is not established.

## Evidence / commands
- Read contract and counter source; no counter measurement or tests executed.
- `grep -n 'C2_R44_PASS'` in round-44 evidence found the label in counter source and base receipt only; base receipt is the old counter's false result, not a C2 result.
- `grep -n 'S160'` across lane located the round-44 contract target, but no landed round-44 S160 registry/knowledge/lesson row in the inspected tree. This is not a finding about final landing behavior; the current checkout's inspected paths do not show it.
- No tools installed.
