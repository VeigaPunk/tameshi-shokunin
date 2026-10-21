# AppendOnlyScope — round 22 advisory

## Axes and observed disposition

Axes: calibration (terminal callback status, not artifact presence), provenance preservation (no rewritten historical authority), and operability/no-harm (existing registered commands retain their contracts). This is a read-only advisory audit, not an admission, deletion proposal, or production patch. No checks, tests, builds, formatters, installs, git/jj operations, or runtime dispatch were performed. Only this new report was written.

The frozen contract is `.ufo/evidence/round-22/contract.json:2-20`, base `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`. Its measured unit is eight malformed/mismatched CLI fixtures, not eight authenticated provider observations. Round 21 remains admitted; neither its C1 nor C2 claim is reopened here.

## Prior files that must remain immutable

For this accounting addition, keep these existing input/provenance files byte-preserved, rather than repairing counts, identities, or report classifications in place:

- `.ufo/waves/round-21/original-outcomes-final.json` — declared terminal outcomes and corrected totals.
- `.ufo/waves/round-21/original-outcomes1.json`.
- `.ufo/waves/round-21/original-outcomes2.json`.
- `.ufo/waves/round-21/original-outcomes2-corrected.json`.
- `.ufo/waves/round-21/w1/swarm-registry.json` and `.ufo/waves/round-21/w2/swarm-registry.json` — original exact seat identities and roles; no dead-seat replacement or identity rebinding.
- `.ufo/waves/round-21/spec1.json` and `.ufo/waves/round-21/spec2.json` — assignment declarations, not rewritten to match retrospective results.
- All existing retained files beneath `.ufo/waves/round-21/`, including dispatch/run/record/assignment/wait records and existing reports. Specifically preserve `.ufo/waves/round-21/w2/ProfileBashTsukuroiCensus.md` and `.ufo/waves/round-21/w2/V01WitnessTests.md`; partial reports are valuable historical artifacts, not completion authority.
- All existing files beneath `.ufo/evidence/round-21/` and all earlier filed evidence. Add new round-22 receipts instead of replacing historical observations, declarations, ledgers, or measurement programs.
- The already-frozen round-22 evidence inputs `.ufo/evidence/round-22/contract.json`, `measure.py`, `before.json`, and `census-start.txt`. In particular, do not alter the frozen eight-case ruler to fit the implementation.

Corpus/history has a different permission: existing content stays unchanged but a new dated section may be appended. This applies to `corpus/lessons/round-21.md` (including its existing Outcome-accounting erratum at lines 163–174), existing knowledge entries, `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md`, and historical `SCORECARD.md` entries. Add the new same-ground entry and its coverage/index row; do not rewrite old claims or remove superseded text. New conclusions should identify what they supersede and the relevant revisions. `QUALITY.md:262-278,310-317` makes the append-only corpus/LOG rule explicit; it does not impose that blanket numstat rule on `SKILL.md` or `SHONEN.md`. That exception is not a reason to change either for this bounded addition.

These are preservation obligations, not a claim that I established a whole-tree before/after byte-identity comparison. Such a verification was not run under this lane's no-check instruction. No production content was written by this seat.

## SOURCES: narrowly mutable cells, not mutable history

`corpus/SOURCES.md:10` has eleven columns. Existing rows may change only **status**, **recheck**, and **used-by**, with each affected ID and exact old→new cell transition logged. Existing **id, source, kind, tier, scope, anchor, teaches, opened** remain immutable. A reopening date belongs in the current lesson/search record; it does not replace the original opened date. A changed interpretation, anchor correction, or teaches correction needs an additional explicitly superseding row, not an in-place rewrite.

Evidence for the distinction: `corpus/lessons/round-19.md:277-281` explicitly records the Sources contract v1 status/recheck/used-by permission; `corpus/lessons/round-13.md:15-20` preserves original identity/date and adds S047 for an interpretation correction; `corpus/QUALITY.md:344-347,377-385` requires cell-level comparison and separates table-line replacements from forbidden immutable changes or lost non-row lines.

Therefore an allowed used-by edit may replace a Markdown table line and produce a deleted-line count without violating this exception. It must not be presented as a literal zero-deletion append, and zero deleted lines alone is not proof of immutable-cell compliance. Existing footer/search-log prose stays append-only. In particular retain `Next unused id: S082.` at `corpus/SOURCES.md:267`; when an actual new S082 row is admitted, append the new next-ID pointer rather than replacing this historical line (`QUALITY.md:265,310-317`).

The proposed S082 is same-ground **own-work** support scoped to the retained declared callback outcomes, not an external source or new frontier coverage. Its source header can cite the retained outcome file and lesson erratum, with precise anchors and the original data's limits. Do not invent an external opening to satisfy the external-source rule. `QUALITY.md:27-30` requires the new knowledge entry to open with `source:`, `verified-at:`, and `recheck:`; `QUALITY.md:18-20` requires the coverage-map row in the same round or explicitly owned debt. `corpus/knowledge/hermetic-env-differential.md:1-4` illustrates existing source-headed structure, not authority to claim its separate F5 ground for accounting.

## Registry obligations for the proposed tool

Distinguish the two registries:

1. The **wave registries** above are frozen identity inputs. Compare each outcome's name/id/role with the original registry member and corresponding spec; report presence cannot alter status. Do not repurpose or rewrite them as a tool registry.
2. `tools/registry.json` is the maintained command registry. Append new rows for the public accounting gate and its selftest; preserve existing names, argv, expected exits/assertions, source pins, tags, and admitted capabilities. If a genuine replacement is needed, retain the old row as `superseded` with an existing active `superseded_by` target; it still runs. For this additive feature no existing-row supersession is needed.

Use existing schema `tameshi-entry-registry-v1`. `tools/registry-check.py:18-27,200-298` defines a unique lowercase-hyphen row name, kind `gate|probe|selftest`, nonempty direct argv, integer `expect.exit`, optional literal `stdout_contains`, finite positive bounded `timeout_s`, `source` shaped `<file>@<7-40 hex rev>:<line>[-<line>]`, and `status: active`. A placeholder source revision is not an acceptable final pin. New gate argv should name retained round-22 bundle and persisted expected-input files by lane-relative paths; do not use live fleet-root absolute paths or a writer mode. Register the actual public gate, not only selftest coverage.

No-harm obligations are `QUALITY.md:136-147`: changes to pinned instruments require the affected registered commands and re-pin/supersession if outcomes change; the final monitor covers all active registered entry commands at the delivered revision in a clone, not just new selftests. Those are L1/integrator verification obligations, not checks exercised by this seat. Existing `tools/registry.json:875-892` includes round21-measure and coldread-selector rows, which this addition must not remove or rewrite. The inspected command registry contains no wave-accounting row; this is an integration obligation, not a claim that current in-flight work is complete or deficient.

The inspected `tools/wave-accounting.py:137-144` selftest imports `.ufo/evidence/round-22/measure.py`. Keep that explicit frozen dependency available and immutable; do not delete it as an obsolete duplicate after the tool lands. Instrument edits during a reading wave must follow staged-install/receipt identity requirements (`QUALITY.md:102-113,390-400`), not mutate the instrument readers are executing.

## Concrete contradiction and preserved contract

Observed retained data, not a fresh recount:

- `original-outcomes-final.json:3-5`: wave1 71 seats / 28 completed / 43 dead.
- `:636-638`: wave2 75 / 38 / 37.
- `:1364-1369`: total 146 / 66 / 80; partial reports do not rehabilitate failed jobs.
- `:1123-1128`: `TameshiR21.ProfileBashTsukuroiCensus`, reviewer, **failed**, report path present, replaced=false.
- `:1297-1302`: `TameshiR21.V01WitnessTests`, reviewer, **failed**, report path present, replaced=false.

The retained lesson's historical “forty returned;35 provider-dead” is explicitly superseded by its existing erratum (`corpus/lessons/round-21.md:163-174`). Preserve both; do not silently turn 40 report artifacts into 40 completed callbacks or delete the partial reports. Current inspected tool logic distinguishes `completed` and `failed`, records failed-with-report separately, rejects other status strings and mismatched totals, and requires replaced exactly false (`tools/wave-accounting.py:88-116`). Its input-digest guard is at `:119-132`. These are source observations, not exercised success claims or proof that source registry snapshots themselves are authenticated.

## Narrow recommendation and tradeoff

Keep the additive design: one new gate, new immutable round-22 retained inputs/receipts, source-headed same-ground knowledge, appended command-registry rows, and append-only dated/index/source bookkeeping with the explicit three-cell exception above. Do not add a second accounting authority, erase stale prose, retrofit historical evidence, or infer provider authenticity from a digest of caller-declared input.

No deletions made or recommended. Historical redundancy is intentional provenance; deleting the failed reports, prior incorrect outcome snapshot, existing erratum, or frozen ruler would harm calibration/provenance. LSP absence proof is not applicable because no semantic deletion candidate was advanced. Tradeoff: this preserves historical contradictions and adds a maintained registry entry, while keeping the authority split inspectable. A passing gate would establish consistency of persisted declared inputs and eight bounded rejection predicates—not callback authentication, independent review credit, expertise points, or new-ground coverage.
