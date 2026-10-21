# Round22 NoHarmBoundary — advisory source audit

## Axes and scope

Axes: calibration (terminal callback status, not report presence), operability (registered entry outcomes), source-credit integrity (current committed inputs), and preservation (historical provenance/no production edits). Only this new report was written. No dispatch, install, Git/jj mutation, build, test, formatter, or measurement command was run. This is advisory, not admission or independent review credit. No deletion proposed: removing historical observations or a monitor would harm preservation/calibration. No semantic no-caller assertion is made; no deletion candidate required LSP proof.

Contract read first: `.ufo/evidence/round-22/contract.json`, base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`, eight predicates, before0/target8, declared callback inputs rather than authenticated provider telemetry. Round21 remains admitted; its two claims are not reopened.

## Observed current interfaces

- `tools/registry-check.py:9-80,1824-1863`: `python3 tools/registry-check.py [--root DIR] [--rev REV] [--registry PATH] [--only NAME] [--tag TAG]... [--json]`, or `--selftest` alone. Exit0 all active rows held;1 differing row;2 cannot evaluate;64 usage. Rows execute directly, not through a shell. Superseded rows still execute but do not enter the active denominator. `--rev` uses an isolated fleet-mirror clone; live mode may write receipts into its root and is expressly discouraged by `SKILL.md:1839-1842`.
- Registry entry fields: unique lower-case/hyphenated `name`, `kind` gate/probe/selftest, string-list `argv`, `expect.exit` with optional literal ANDed `stdout_contains`, finite positive `timeout_s` at most86400, pinned `source` of form `file@7-40hex:line[-line]`, `status` active/superseded; superseded needs an active `superseded_by`; optional tags. Adding a SKILL table row is not itself executable registry coverage; adding a `tools/registry.json` row is a separate operation.
- Strict source monitor SKILL row: `SKILL.md:1978`, `.ufo/evidence/round-21/coldread/measure.py`, `--repo REPO --rev REV --explain`, selftest `--selftest`; exit0 means observed, not full-page acceptance. Its executable registry row is **`round21-coldread-selector-selftest`**, `tools/registry.json:884-892`: active, tag `new-r21`, timeout300, argv `python3 .ufo/evidence/round-21/coldread/measure.py --selftest`, expect0 plus `SELECTOR_SELFTEST: 12/12 pass`, source `SKILL.md@370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb:1978`. This selftest row does NOT measure current source credit.
- Selector source `.ufo/evidence/round-21/coldread/measure.py:17-30,102-113`: unchanged round18 algorithm, round21 default ledger; rejects ledger-file/ledger-rev/inputs-overlay overrides including abbreviations and equals forms. No fallback to historical ledger. Numeric no-harm must use this selector without overrides, not old round19/20 numbers.

## Retained status and exact evidence boundary

`.ufo/evidence/round-21/final/monitor-current.json` records actual revision `326b3b14aff3a2b17d5a92329499ae948fd6f7bf`, exit0, interval `2026-10-21T13:14:38.229076+00:00`–`13:14:44.803782+00:00`, instrument SHA256 `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`, sections62/62, box3 true, restraint8, depth8, overrides false. This is a retained observation, not a run by this auditor and not proof for a later revision.

`SCORECARD.md:951-963` explicitly supersedes the earlier wave2 report-count inference: wave2 **38 completed/37 dead**; total146 seats **66 completed/80 dead**, no replacement. It separately records battery40/40 active plus4 superseded at `40508a120ee13e6088a594decc66d2da759bd0cc`, then directs final-source credit to its actual measured revision. These revision-specific records must not be conflated. `SCORECARD.md:965-980` declares round22 one calibration claim plus capability, not a second axis, promotion, fixture-count expertise score, or authenticity claim.

No current no-harm result was observed. No contradiction requiring reopening admitted round21 claims was found in these scoped interfaces. The important non-equivalence is selector-selftest success versus actual current full-page source credit. Retained outcome source `.ufo/waves/round-21/original-outcomes-final.json` explicitly contains failed callback rows with `replaced:false`; existence of a report cannot override their status.

## Inputs affected by one SKILL registry row

The frozen algorithm `.ufo/evidence/round-18/measure.py:18-22,124,132-136,209-252,604-610` keys coverage by section SHA, not by whole-page SHA or line number. Sections are preamble plus every #/##/### heading outside fences, ending before the next heading, trailing blank lines stripped. `SKILL.md` is ignored as a generic input because section hashes cover its bytes.

- **One table row inside an existing section** changes that section's hash, not automatically all62 buckets and not automatically the denominator. If inserted at the end of the current registry, the affected section is `### Round-21 gate/probe registry — finite environment differential` (start1964 through1987 in the inspected page). Its existing ledger read cannot cover the changed bytes. A separate new #/##/### section would add a bucket (conditionally63, if no other headings change); do not invent that denominator from the row count.
- **Adding an executable registry row** changes `tools/registry.json`'s digest and can stale reads of unchanged SKILL sections that recorded that file. Historical ledger entries mentioning it span starts17,1069,1155,1246,1272,1436,1609,1814,1846,1923/1925 (same heading across historical layouts),1938,1964. These are a dependency exposure set, NOT a measured count of newly uncovered sections: another verified entry may still cover a section.
- **Appending SCORECARD observations** can stale entries at starts17 and1155 that record `SCORECARD.md`. `LOG.md`, corpus/source metadata, owning tool bytes, receipts, and selector changes similarly affect only entries recording those inputs; freeze production metadata before final source re-anchors rather than repeatedly invalidating them.
- The latest ledger entry for start1964 (read revision `678a67f25346f1e3d91b2ca53ab816cbe7dcbaa9`) records `tools/registry.json`, `tools/{env-diff,round21-measure,wave-route-mix}.py`, `.ufo/evidence/round-21/{c1-mutants.json,c1-survivors.py,c2-contract.json,c2-count.py,coldread/measure.py,f5/receipt-final-production.json}`, `.ufo/evidence/round-20/coldread/ledger.json`, `corpus/SOURCES.md`, `corpus/knowledge/hermetic-env-differential.md`, `corpus/lessons/round-21.md`, and SKILL. Its trace is `.ufo/evidence/round-21/coldread/traces/L1-final/source-1964.json`; provenance explicitly labels L1-author source re-anchor and preservation of prior233 entries. Preserve it; append accurate new reads rather than editing old provenance.

## Commands for L1 only, after integration/source freeze

Run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. `REV` below must be assigned the actual final40-hex committed lane revision; do not substitute the frozen base or a historical green revision. These are deferred commands, not exercised verification.

```sh
python3 tools/wave-accounting.py --selftest
python3 .ufo/evidence/round-22/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 tools/registry-check.py --selftest
python3 .ufo/evidence/round-21/coldread/measure.py --selftest
python3 tools/registry-check.py --rev "$REV" --json
python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev "$REV" --explain
```

First two commands are grounded in `tools/wave-accounting.py:137-178` and frozen `.ufo/evidence/round-22/measure.py:83-89`; require actual8/8 discrimination and the clean control, not just tool presence. The counter has **no `--rev` option** and evaluates the supplied working repo, so L1 should run it against its final committed isolated tree when attributing a revision. Registry runs should not use `--tag`/`--only` for the final complete battery. If the checker is deliberately grading a different committed revision against the integrated registry, explicitly add `--registry /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry.json` and preserve that registry digest; otherwise its default is the measured clone's registry.

For real retained population replay, the public interface is exactly `python3 tools/wave-accounting.py --bundle BUNDLE --expected EXPECTED --json`. BUNDLE/EXPECTED require the integrator's actual persisted paths; none is invented here. Bind BUNDLE to all146 exact original registry identities/roles and declared terminal outcomes from `.ufo/waves/round-21/{w1,w2}/swarm-registry.json` and `original-outcomes-final.json`; EXPECTED must independently persist its digest. The digest authenticates byte membership, not callback provenance. Require corrected totals66/80, exact status enum, replacement=false, and preserve partial reports as artifacts only.

Final monitor acceptance must inspect fields, not exit0 alone: `coldread.sections_covered == coldread.sections_total`, `coldread.box3_full_page == true`, restraint8, depth8, `overrides_used == false`, `trace_gate == strict`; persist actual revision, instrument digest, interval, and complete output. Source re-anchors stay L1-author input-keyed evidence, not blind/independent cold reads or required-command coverage.

## Tradeoff and stop boundary

Minimal recommendation: add the new callable entry using existing table/schema conventions, preserve old evidence, then perform only actual affected source re-reads and one final full battery/current-source observation. Avoid creating a second monitor or treating the selector-selftest as no-harm. Appending a new section improves discoverability but adds a real coverage obligation; inserting one row avoids that extra denominator but still requires a truthful section re-read. No deletion is safe or necessary for this assignment. No tools installed. Production/evidence bytes were not written by this lane; a global byte-identical-tree check was not run or claimed because concurrent integration may change the shared tree and this lane is forbidden to run checks.
