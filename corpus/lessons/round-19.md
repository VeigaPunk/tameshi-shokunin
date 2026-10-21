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

Measured after at landed correction revision
`21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`:
`.ufo/evidence/round-19/after-21e7932.json`, corrected=5/open=0/total=5,
exit0. The same ruler at baseline7243e7f returned corrected0/open5/exit1.
Every row is revision- and input-digest-bound; gate labels remain narrower
than historical authenticity or arbitrary prose validation.

## No-harm repair — current evidence is not a historical score

The actual monitor at landed21e7932 returned **49/60, restraint6**:
`current-ledger-monitor-21e7932.json`. Required corpus appends changed
inputs of eleven buckets, including the registry section's new row.
The earlier historical-only score8 qualification was insufficient as a
current no-harm assertion (w1 AxisBound). This failed intermediate is
retained, not replaced by the4b7c682 historical60/60.

The repair preserves the round18 implementation and ledger byte-for-byte.
The small `coldread/measure.py` wrapper selects a new default round19
ledger and BOX3 evidence link, retaining the same strict trace/input/veto
algorithm without `--ledger-*` or overlay/legacy mode. Existing entries
are carried unchanged; affected buckets receive actual source re-reads
and committed trace receipts. These are explicitly **L1-author
input-keyed source re-anchoring**, not a new blind or independent cold-read,
and not required-command coverage. External observations remain outside
the credited-input predicate; they are never called re-verified by an
internal input hash. A source-read gap remains named rather than becoming
an invented command execution.

This is no-harm maintenance within C1, not another claim or capability.
QUALITY40 mines the failed intermediate. The current monitor's final
revision/count is recorded with its own receipt after the ledger lands.
The earlier “no current-page equivalence is claimed” statements remain
true: input-keyed credit is the narrower measurable predicate.

## Build-wave findings integrated

- NegativeControls showed five corruptions that the initial ruler missed:
  wrong effective receipt path, edited immutable S008 opened date, moving
  diff bound, fabricated runner hash, and a backdated timestamp. The
  hardened ruler pins the named receipt path, historical opened date,
  exact historical diff command, independently re-derived tool/runner
  hashes, and aware timestamps no earlier than frozen contract78b99dd.
  These checks are bounded, not producer authentication. Initial receipts
  remain measurements of the first ruler; final before/after measurements
  use the same strengthened ruler and say so.
- AxisBound's missing measurement instrument identity is supplied by a
  separate `round18-final-measure-instrument.json` companion binding the
  original receipt SHA and frozen instrument SHA. The original receipt is
  not rewritten. Its source blob is `7ca87a7c…26dd37` at4b7c682.
- MetadataDraft's second stale S008 mention (case8 line215) and the source
  installation phrases (guard note lines99/133) receive explicit sweep
  addenda. R18-1 supersedes only staged/PENDING markers, not technical
  analysis in their paragraphs.
- Captured-by correction (MistakesDraft): the failed usage invocation was
  already covered by QUALITY15/17; the missing exact-revision receipt by
  QUALITY2. QUALITY26/35 cover correction mechanics, not the original
  prevention duty. The count-command reference resolves to canonical
  `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md:34`.
  “not4b7c682” above means “not at4b7c682”. The scratch missing-runner row
  is a new round19 mistake, distinct from the five routed items.
- ReceiptLesson's nonzero registry row in old `final/checks.json` remains
  a failed raw attempt at921ef80. Its distinct successful branch-aligned
  reading is explicitly at5923d89; neither is reclassified at the other's
  revision. This old failure was already disclosed by the round18 report
  and verifier; it is not a sixth frozen defect.
- Historical audit outputs' printed “ancestor runs share instrument
  blobs” text is not established by their captured read commands
  (Audit965/Audit1212/Audit1925). It is not reused as ancestry evidence.
  Old traces need not authenticate stdout bytes; new refresh receipts
  separately persist output digests. Historical one-line range mismatches
  and external observations stay limitations, not newly earned credit.

Source-sweep addendum: S063/S077/S078 `used-by` gains
`corpus/knowledge/guard-kill-closure.md`; each status stays `mined` and
each recheck is unchanged. Old lists: S063 `corpus/lessons/round-17.md`,
S077/S078 `corpus/lessons/round-18.md`; new lists are exactly the old
list plus that knowledge path. No immutable cells, added rows or tiers.
These repair already-existing citations, not additional sourced C1 claims.
S063 and S078 were reopened by their named w1 scouts on2026-10-21; S077
was reopened by L1 on the same date:

| Row | URL | Located quote (≤25 words) |
|---|---|---|
| S063 | https://git-scm.com/docs/git | “it specifies a path to use instead of the default .git for the base of the repository.” — ENVIRONMENT VARIABLES, The Git Repository, GIT_DIR |
| S077 | https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html | “then that process will be reparented to the nearest still living ancestor subreaper.” — DESCRIPTION ¶2, man-pages6.19 |
| S078 | https://man7.org/linux/man-pages/man2/open.2.html | “These request opening the file read-only, write-only, or read/write, respectively.” — DESCRIPTION access modes |

Newly observed, **open outside C1**: `input-keyed-coldread-credit.md:1`
still uses S060's obsolete `%file`/General anchors (w1 SourceS075); mark
it stale pending a later metadata erratum, never claim metadata is repaired
across the whole lane. S064's live page digest changed in heading markup
only; its dated2026-10-20 row remains historical and its quoted prose
still matches. Neither source is added as support for the five-item count.
The lessons glob's teaching absence is path-scoped; the existing
`corpus/knowledge/operator-runbook.md` is not absent (w1 TeachingSweep).

Source range addendum (w1 SourceCorrection): the arithmetic mistake is
also a **range mismatch**, not only a row/cell mismatch. The full frozen
round18 range has five replacements and six changed cells (five used-by,
one status); four used-by-only changes belong to58e5d53→9ee1c80 alone.
Round18 lesson line48's “only in-place row change” is now explicitly
superseded alongside line79. Net zero deleted non-row lines does not
erase the intermediate footer deletion/restoration.

R18-3's ruler now compares two separately read, committed, SHA-pinned
historical source snapshots, reports exact row/cell deltas, and rejects
immutable changes, removed IDs, lost non-row lines, wrong history,
snapshot tampering and an extra claimed source ID. The old handwritten
numstat transcript remains historical corroboration, not its oracle.
Criterion38's range qualification records the lesson.

The current-monitor maintenance needed two further source entries after
the initial eleven: SHONEN's current ledger link invalidated bucket1499,
and migrating the active measurement recipe to the round19 selector
changed bucket1855. The resulting measured revision
`cecaefe73482504a814064dd7b2242c8c0b8ad50` returned strict input-keyed
60/60, restraint8, no overrides (`current-ledger-monitor-cecaefe.json`).
The intervening59/60 receipt atc5730cc is also retained. Later ruler and
lesson changes require their own current-input refresh before the final
no-harm measurement; the cited60/60 is not asserted for a later tip.

Route04/ReceiptIntent's stronger checks were incorporated: the effective
receipt's supersedes is an exact list (not substring containment), the
tool/runner hashes are independently pinned, and the new tally must be
byte-equal to the retained successful round18 tally even if someone
recomputes its local digest. Cross-revision tool identity and the
no-checkout scratch materialization are explicitly documented in the
round18 erratum. Earlier failed chronology fields confer no success.
The final source/receipt comparison is not a claim of producer
authentication or exhaustive adversarial coverage.
