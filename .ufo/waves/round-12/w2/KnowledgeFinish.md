# KnowledgeFinish — round 12, wave w2 (seat TameshiR12.KnowledgeFinish)

Advisory, lane-internal. Not an independent non-author admission or promotion.
No gate, test, build, lint or formatter was run by this seat; the only runtime
facts below are file reads and hashes.

Assigned write: `corpus/knowledge/repeated-control-precondition.md` only.
Report: this file. No other path was written.

## 1. Owned file

| path | state at write |
|---|---|
| `corpus/knowledge/repeated-control-precondition.md` | finalized in place; 80 lines / 12,124 B |

The source/provenance trio is present: `:1` `source:` (S004 + S026, each with
URL, section, fetch time, sha256 and byte count), `:2` `verified-at:`,
`:3` `recheck:` with two runnable commands and their healthy counts. The
`recheck:` line now also states S004's registry cadence (`on-release`) instead
of silently applying S026's 730d to both.

## 2. What was finalized, with anchors

| change | anchor in the note | grounding |
|---|---|---|
| Finite-run limitation promoted to its own bullet: N identical tuples back to back on one host, not a universal, cross-host, cold-start or statistical claim | `:29` | `tools/repeat-control.py:79-87` (no timeout/supervisor; "not a determinism proof and it cures no flakiness"); `.ufo/waves/round-12/w1/ControlThreats.md:45-56`; `.ufo/evidence/round-12/ControlThreats/probes.out` |
| Source-vs-lane distinction for N: S026's fail-3-in-a-row is a retry mitigation, not a control-repeat rule, so the floor of 3 is lane policy | `:29`, `:54` | same; S026 `S026.html:1136`; `tools/repeat-control.py:245-247` |
| `setup_error` added to the finding table and reading rules | `:43`, `:51` | `tools/repeat-control.py:115-123` (map), `:185-188` (emission) |
| Enforced `--runs >= 3` floor stated as a gate fact, separate from the source claim | `:35` | `tools/repeat-control.py:245-247`; snapshot floor `:349-350` |
| Snapshot rule corrected: digest validation, recomputation from stored bytes, recorded-ID exit, `controls_mismatch` 1 on unreproduced expectation, `snapshot_tampered` 2 on any defect, no execution of the recorded argv | `:52` | `tools/repeat-control.py:337-435` |
| `--out` placement rule (outside any tree the command inspects) | `:35` | `tools/repeat-control.py:24-29` |
| §3 split into contract (`:33-54`) and observed implementation/receipts (`:56-66`) instead of "contract, not measurement" | `:31`, `:56` | file read at 2026-10-20T03:45Z |
| Vague §5 evidence line replaced by four named arms and their exact closing commands | `:75-80` | see §4 below |
| Review F1: invented exact quotation removed; the admission clause is now unquoted contract paraphrase | `:72` | wave contract wording ("not independent non-author admission/promotion"); the old quoted string has no repo source |
| Review F4: `timeout` gloss replaced by the served sentence | `:18` | `S004.html:208` |
| Review F3: the standing summary now contains the required clause verbatim | `:71` | `SiblingOverlap.md:165` requirement |

## 3. Source verification retained in the note

Both bodies re-checked against the scratch copies the w1 seat pinned
(`/tmp/tameshi-r12-ck/fetch/`), digests identical to the header:

| source | sha256 | bytes | anchors used in the note |
|---|---|---|---|
| S004 | `5ec9ba95…f012334` | 29,579 | section `:184-187`, quote `:187`, `caught` `:193-194`, `unviable` `:203-205`, `timeout` `:208` |
| S026 | `ca1145fbe56de30b43b66baf7372206a38abe08a55b3db13f6c7a0114d7a6c8c` | 236,385 | quotes `:1130`, `:1132`, `:1136`, `:1137`; duplicate `text/template` copy `:1095-1102` |

The precondition anchor was corrected in form only (`§Tests fail…` now cited as
`:184-187`, the section header through the quote line; the quote itself stays
`:187`). S026 quote fidelity (tags/entities, duplicate body copy) is unchanged
from `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`.

## 4. Retained receipts the note now cites

| receipt | path | observed value |
|---|---|---|
| pristine control run | `.ufo/evidence/round-12/FailureOracle/actual-pristine/gate-runs/`, `gate.stdout`, `manifest.json` | `REPEAT_CONTROL: controls_match`, `REPEAT_EXIT: 0`, `REPEAT_COMPARE identical=yes runs=3`, tool-sha `29d80254…`; `expected_finding_observed: true` |
| byte-boundary matrix | `.ufo/evidence/round-12/BytesReview/cli/C01–C20` | 20 cases at tool-sha `d45d8e39…`: 6 `controls_match`, 5 `controls_mismatch`, 5 `baseline_nonzero`, 4 `command_unavailable`; each `finding.txt` matched its expected class (`BytesReview.md` "TOTAL 20 UNEXPECTED 0") |
| implementation identity | `tools/repeat-control.py` | 30,557 B, sha256 `29d8025490f349c106bc8132da7bfecc2ae4f8fb00720b43636e52335d27467a`, `VERSION` r12 |

Not claimed anywhere in the note: a snapshot verdict (no `expected.json` exists
under `.ufo/evidence/round-12/` — `find . -name expected.json` → no hits), a
selftest transcript, or any run of the six recorded gates through this gate.
The exact commands that would close each are in the note's §5 (`:75-80`).

## 5. Disposition of the w2 review findings

- **F1 (invented quote at old `:55`) — fixed.** The quoted string is gone; `:72`
  paraphrases the contract without quotation marks.
- **F2 (missing `setup_error`, floor not stated) — fixed.** Table `:43`, rule
  `:51`, floor `:35`; the floor stays labelled lane policy, with S026's
  fail-3-in-a-row explicitly distinguished from a control-repeat rule (`:29`).
- **F3 (required clause absent) — satisfied.** `:71` carries "no flakiness
  cured or determinism proven".
- **F4 (paraphrase in quote form) — fixed.** `:18` quotes `S004.html:208`
  verbatim.
- **F5 / F6 — not touched: outside the owned path and historical.** F5's
  word-count notes live in `.ufo/evidence/round-12/ControlKnowledge/quotes.tsv`
  (evidence), and the `[I]` labels there were not rewritten. F6's access-date
  reconciliation is in `corpus/lessons/round-12.md:13` and
  `corpus/SOURCES.md:15,37`; per L1, the lesson gets an appended current-source
  access note, and this seat did not edit either file.

## 6. Observations outside the owned path (reported, not edited)

- `corpus/README.md:127` now carries the coverage-map row for this note, so
  QUALITY criterion 7 is satisfied for the file (earlier w1 debt is closed).
  That row cites `.ufo/evidence/round-12/verification.json`, which does not
  exist at this write (`ls` → no such file; `BashWitness/summary.json` also
  absent, its seat is in flight). The row's citation dangles until the
  integration owner writes that file.
- The instrumented gate may still change under this wave; the note pins its
  identity with "read … at 2026-10-20T03:45Z" (`:60`) rather than asserting a
  permanent pin.
- `corpus/README.md:80` still lists F3 as `open`; the round-12 resolution block
  at `:127` and `.ufo/waves/round-12/w1/FrontierState.md:84-87,195` record
  "partly held". The note itself claims no F3 status, so no conflict is
  introduced here.

## 7. Tooling

No install or upgrade was performed; no package-manager call was made. Only
repo file reads, `sha256sum`, `find`, `wc`, `grep`/`sed` reads were used.

## 8. Blockers

None. The assigned note is finalized and self-consistent with the retained
receipts; the remaining gaps are named in the note with their exact evidence
commands, not smoothed over.
