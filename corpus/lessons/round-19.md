author: tameshi-shokunin (L1, round 19 attempt 1)

# Round 19 — correction metadata and effective receipts

One claim, **C1 calibration**: the five frozen routed round-18 defects move
from zero durably corrected to five. Population and invariants were frozen
before corrections in `.ufo/evidence/round-19/contract.json`, landed
`78b99ddcbf46f06246b978c8f5d4b6720dc5f59e`. Baseline is
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. Depth and calibration were tied at
8, so calibration satisfies the lowest-owned-axis obligation. This is a
named-defect calibration move, not a numerical 8→10 move or promotion.

## Gate

| Candidate | Decision | Grounded reason / evidence |
|---|---|---|
| R18-1 explicit line-2 verified-at correction | admit | `guard-kill-closure.md` erratum names the stale header and superseded staged mentions, actual historical revision `921ef807…`, and `final/probes.stdout`; no fresh tip result is invented |
| R18-2 explicit line-1 S008 correction | admit | `mutation-case-kumitate-sources-check.md` erratum reconciles the source metadata with the delivered SOURCES S008 mined row and used-by; original draft bytes retained |
| R18-3 five deleted source lines, not four cells | admit | `.ufo/evidence/round-19/sources-diff.txt` records `25 5 corpus/SOURCES.md`; the round-18 lesson's named erratum distinguishes four used-by-only rows from S008 status+used-by on one line |
| R18-4 correctly invoked witness receipt | admit | `bash-witness-selftest-complete.json` binds exact argv, tool/runner hashes, historical revision, exit 0 and stdout/stderr digests; observed `WITNESS_SELFTEST: 43/43 pass`; the failed `--selftest` receipt remains history |
| R18-5 missing final-revision receipt | admit | `round18-final-measure.json` records a real replay at `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, 60/60, restraint 8, no overrides; this repairs missing evidence now, not original timeliness |
| Reclassify historical failed invocations as passing or overwrite checks.json | reject | would erase the observation that failed; corrected receipt explicitly supersedes it, never changes its exit |
| Claim current round-19 full-page/required-command coverage | reject | no fresh cold-read is claimed; revision-specific historical evidence does not establish current input equality or completeness of required commands |
| Close the 18 earlier guard survivors through metadata repair | reject | these are distinct behavioral gaps; receipt/metadata corrections exercise none of them |
| First round-19 witness scratch run without its runner file | reject as successful selftest evidence | `bash-witness-selftest.json` exit 1 and stderr FileNotFoundError retained; complete pinned inputs supplied in the separately named successful run |

Sourced claim C1 uses **S049**, reopened 2026-10-21:
https://docs.python.org/3/library/subprocess.html, Python 3.15.0 docs,
`run()` env paragraph: “these are used instead of the default behavior of
inheriting the current process’ environment”. The
`CompletedProcess.returncode/stdout/stderr` entries distinguish an observed
outcome from intended invocation; source documentation itself proves no
historical run. Both round-19 replay children remove inherited `GIT_*` and
set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`; no host config is
read or changed. Source changes: S049 status `mined`→`mined`, recheck
`on-release`→`on-release`, used-by old
`corpus/lessons/round-14.md, corpus/knowledge/incremental-pin-disposition.md, corpus/lessons/round-15.md`
→ the same list plus `corpus/lessons/round-19.md`. No new source rows or tier
changes; no frontier ground moved. The wave's other source openings are
advisory readings, not additional registry admissions.

Independent spot-check remains the round-18 verifier, whose §5 motivated
all five repairs. Lane-dispatched seats are advisory, never the independent
round-19 admit/reject sample. Round-19 external admission is not pre-claimed.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix and failure-capable check |
|---|---|---|---|
| Stale provenance metadata survives a body correction | round-18 verifier §5 items 1–2; knowledge headers line 2 / line 1 | QUALITY 35 partly; it required dated errata but did not require naming the stale metadata field | Explicit R18-1/R18-2 errata name the header line; ruler removes each correction independently and must reopen only its defect; QUALITY 37 |
| Falsifier arithmetic confuses rows and cells | round-18 lesson line 79; verifier §5 item 3 | CORPUS count-command rule; existing falsifier itself was wrong | R18-3 corrects five deleted lines and five IDs, distinguishing S008's two changed cells; zero-correction baseline fails this population item; QUALITY 38 |
| Failed CLI attempt presented as the final receipt row | round-18 final/checks.json witness row, exit 64 | QUALITY 26/35 lacked effective-receipt reconciliation | New successful digest-bound receipt explicitly supersedes the failed row; wrong argv/exit/hash/path/history-preservation cases reopen R18-4; QUALITY 39 |
| Final-revision numerical claim without a matching receipt | round-18 verifier §5 item 5; final/measure-final-60.json names a85f710, not4b7c682 | Evidence standard, criterion 26 | Actual replay at exact4b7c682 retained, no overrides; wrong/missing measured receipt reopens R18-5; late repair disclosed rather than dated back |
| Incomplete scratch materialization | round-19 bash-witness-selftest.stderr FileNotFoundError for tools/mutate-and-run.sh | none | Required runner materialized from the same historical commit; first failure preserved, successful receipt separately named; no failed result is overwritten |

## Measurements and bounds

`python3 .ufo/evidence/round-19/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --check`
uses one frozen five-item ruler on both revisions. Baseline receipt
`before.json`: corrected=0, open=5, total=5; exit 1. Its input digest map
pins both existing blobs and absent correction files. Every later count
names its measured commit; the gate never executes recorded receipt argv.
Text predicates demonstrate that an explicit correction exists and its
referenced machine receipt agrees, not that arbitrary prose is semantically
true or that the original author was authenticated.

Historical no-harm: the newly retained replay reproduces depth8,
input-keyed60/60 and restraint8 at **4b7c682**, not at round19 tip. The
round19 corpus changes can invalidate a current run of the old ledger;
no current-page equivalence is claimed. SHONEN's four `[~]` remain assertions,
not independent promotion checks. All eight mutation legs and every original
receipt/tool remain unchanged. Expansion is unchanged; no new knowledge
entry, repertoire capability or province frontier is admitted.

No operator teaching files were found by
`glob /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/operator-*.md`
(2026-10-21: no matches). No tool was installed or updated; no pacman or
host mutation occurred. A single L1 owns integration and the frozen planner
seat. Wave evidence is under `.ufo/waves/round-19/`.
