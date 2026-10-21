# ResidualCurrentMonitor: round-20 residual falsification

Reviewer: TameshiR20-3.ResidualCurrentMonitor (read-only seat). Advisory only. This is not a non-author admission. L1 owns integration and runs final verification.

Scope: `.ufo/evidence/round-20/coldread/measure.py` (selector), the SHONEN box-3 ledger pointer, `.ufo/evidence/round-20/coldread/ledger.json`, and round-20 text that quotes the monitor.
Lane HEAD: `d0ec3c8`. Tracked tree clean; only untracked `.ufo/waves/round-20/*` present. Frozen contract `6fd220b`. Baseline `c144dcd`. Last recorded measured revision `32838a5` (score 8, sections 60/60, `overrides_used` false).

Execution boundary: no measure, selector or frozen selftest, registry row, build, lint or test was run. Evidence comes from file reads, read-only git (`status`, `log`, `show`, `cat-file`, `ls-files`, `diff`) and ad hoc read-only Python over JSON, blob hashes and a replica of the frozen section split and per-entry gates. The replica was calibrated on `32838a5`: its static upper bound is 60/60, matching the recorded measured 60/60. Items marked [INFERENCE] await L1's frozen run.

## 1. Answers

| Question | Answer |
|---|---|
| Selector preserves the frozen round-18 credit algorithm? | Yes. It loads `.ufo/evidence/round-18/measure.py` (sha256 7ca87a7c..., equal to contract historical `round18-measure`). It patches only four module globals (selector lines 89-92): `DEFAULT_LEDGER_PATH`, `LEDGER_PATH`, `BOX3_LINK`, and `IGNORED_INPUTS` union `{LEDGER}`. Diff against round-19 selector: four string lines. |
| No fallback to an old ledger? | Yes on the default path. Frozen `main` reads only `REV:DEFAULT_LEDGER_PATH` (frozen 1601-1603). Selector case `no-historical-ledger-fallback` (selector 72-78) checks absence gives 0 sections. |
| No override? | NO (F1). `--ledger-file`, `--ledger-rev` and `--inputs-overlay` pass straight through (selector line 93, frozen parser 1520-1534). The restraint score is not gated on `overrides_used` (frozen 679-683). |
| Relocation and default-package tests appropriate? | Partly (F4). Default, relocated-repo and no-fallback cases are sound. Override refusal, the real SHONEN layout and the score/override fields are untested. |
| SHONEN pointer valid? | Placement is valid. Line 9 (`- [~] Instructions executable...`) and line 10 (indented link) form one block in `shonen_boxes` (frozen 256-274, which keeps indented continuation lines), so `BOX3_LINK in boxes[2][1]` holds. The only change since `6fd220b` is the link target, round-19 to round-20 (SHONEN.md:10). |
| Docs free of blind, independent cold-read or command-coverage claims? | Largely yes (section 5). Three items must be fixed before re-anchoring. |
| "184 unchanged old entries"? | Not as stated. The ledger is byte-identical to the round-19 ledger (sha256 1ba190e5...). Of 184 entries, 159 match round-18 entries exactly. 25 are round-19 L1-author entries: all `gap-minor` (10 record, 15 instruction), 16 buckets, traces under `round-19/coldread/traces/L1`. SCORECARD round-19 records the same split (SCORECARD.md:758-759). |
| Does HEAD reproduce 8? | No, not without re-anchors (F2). [INFERENCE] Predicted restraint is 6 or less. |

## 2. Findings, ordered by severity

### F1 (High): "no override" is not enforced by the selector

- The wrapper forwards every override flag. A claim-bearing run can use `--ledger-rev REV:.ufo/evidence/round-19/coldread/ledger.json` (frozen 1587-1600) or `--inputs-overlay FILE` (frozen 1609-1642).
- Overlay items may replace `inputs` and `traces` for any entry keyed by (`skill_sha256`, `start`) (OVERLAY_FIELDS frozen 138-139; merge 584-601). A stale entry could be re-pinned to HEAD blobs without a new entry. The run then uses the legacy trace gate, and `overrides_used: true` is the only signal, because the restraint (679-683) does not read it. [INFERENCE] This could report 8 for a state no committed entry supports.
- Frozen docstring (67-71) says "A claim must never use overrides". The round-20 path does not enforce it. SKILL.md:1951 says "strict default, no overrides" for this same tool, so doc and tool disagree.
- Fix (section 7): refuse the three flags before delegating (exit 64), with selftest cases for each flag and for `--ledger-rev` aimed at round-18 or round-19 paths.

### F2 (High): HEAD cannot currently measure 61/61

- Static upper bound at HEAD `d0ec3c8`: 46 of 61 sections covered [INFERENCE]. The replica omits the trace gate and live-read binding, which only remove credit, so the real figure is at most 46.
- Fifteen sections are uncovered (listed in section 4):
  - 13 lose their only credit-passing entries because those entries pin metadata changed by `c51eb32` or `d0ec3c8`. Pins stale at HEAD: `corpus/SOURCES.md` 33/33, `tools/registry.json` 30/30, `corpus/README.md` 21/21, `corpus/QUALITY.md` 8/8, `SHONEN.md` 5/5, `LOG.md` 2/2, `SCORECARD.md` 2/2. Exempting exactly these paths restores 59/61.
  - Section 1938 (`### Round-20 gate/probe registry - frozen receipt instruments`) was appended by `c51eb32` with no ledger entry.
  - Sections 131 and 1380 are uncovered and also hold drift-silenced failing records (F3).
- Calibration: at `32838a5` the same replica gives 60 sections, 60 covered, matching the recorded measurement. At HEAD there are 61 sections; the new one is the only section whose text is absent at `32838a5`.
- Consequence [INFERENCE]: `box3_full_page` is false, box-3 points are 0, and `calibration_restraint_score` is at most 6 (boxes 1, 2 and 4 still `~`). SHONEN's `~` mark and link stay as a lane assertion, but the computed number falls below 8. QUALITY.md:364-366 requires a lower current score to be named before unchanged calibration is asserted. SCORECARD.md:776 (which asserts calibration stays at 8) and LOG.md:1351 assert 8 with no current measurement.
- Legacy stale pins from before round 20 (`tools/mutate-and-run.sh` 35/107, `PROVINCE.md` 9/17, `corpus/knowledge/fleet-kill-rate-ledger.md` 36/59, `tools/registry-check.py` 9/21, `tools/bash-witness-study.py` 12/42, others) did not block coverage at `32838a5`, and exempting the round-20 paths leaves them harmless. They are not the cause at HEAD.

### F3 (Medium): drift silences failing records

- Frozen aggregation (72-76): "an entry with drifted/missing inputs is stale and does not veto", and "a clean entry never launders a failing one".
- Two failing candidates are silenced only by drift today:
  - 0-based entry 73, section 131: `gap-minor` with `wrong_expectations=1`, pins `corpus/README.md`.
  - entry 98, section 1380: `wrong-expectation`, has a stale pin.
- If either pin becomes current (overlay re-pin, a README revert, or a re-anchor that re-pins it), its section becomes VETOED. Any re-anchor claiming 131 or 1380 must name these records. Otherwise "covered" would hide an open wrong expectation.

### F4 (Medium): selftest and registry gaps

- Registry row `round20-coldread-selector-selftest` (tools/registry.json 844-851) checks only `exit 0` and `SELECTOR_SELFTEST: 3/3 pass`.
- The relocation case (selector 68-71) asserts only `sections_covered == 4`. It does not assert `calibration_restraint_score`, `overrides_used` or `trace_gate`.
- No case uses the real SHONEN layout. The fixture writes the single-line `SHONEN_BOX3` (selector 44, frozen 739-747). The continuation form (`SHONEN_CONT_TEXT`, frozen 749-750) is not exercised by the selector.
- `__main__` (selector 87) matches only the exact argv `['--selftest']`. With extra arguments, the frozen `selftest()` runs with patched globals, which gives undefined results.
- No override-refusal case exists (F1).

### F5 (Medium): docs (see section 5 for the full audit)

- SCORECARD.md:796 says all 184 original entries are carried unchanged. Inaccurate: 159 carried plus 25 round-19 L1-author entries.
- SCORECARD.md:776 asserts calibration stays at 8 before any current measurement exists.
- SKILL.md:1951 says "strict default, no overrides" (not enforced, F1) and "2 usage/could-not-evaluate". Usage errors exit 64 (frozen 95-97 docstring; `UsageParser.error` 147-151).

### F6 (Low): pins, digests and live reads

- Malformed pin: entry 97 (start 1302, `gap-minor` record) has key `tools/mutate-and-run.sh@75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`. It can never resolve (`input-missing`). HEAD `tools/mutate-and-run.sh` sha256 is d22c4025..., which `contract.json` lists as historical `witness-runner`. The 75ed934... digest appears in LOG.md and in this key, and is not HEAD's runner. Cite digests by `git show REV:path`, not from prose.
- Live reads: 14 traces record live-lane reads. Non-`.git` reads need digest binding at REV (frozen 432-456). `.git/` reads are accepted without digest binding by design (frozen 448-449). That is 2,515 accepted reads in those traces.
- Four traces record a live `corpus/SOURCES.md` digest that no longer equals HEAD: `04-step3-registry-land.json`, `05-step3-oldrev-current-registry.json`, `10-only-verify-round15.json`, `4.json`. Entries using them would fail `live-lane-read`.
- `carried_from` is an absolute `/home/vgpnk/...` path on 68 entries. The algorithm never reads it (informational only).

### F7 (Info): contract scope and a possible invariant conflict

- `contract.json` freezes only the receipt-window and round20-measure instruments. The selector (sha256 4d78a823...), the ledger (1ba190e5...), the SHONEN pointer, SKILL section 1938, the registry rows and the SOURCES edit all landed after `6fd220b`, outside the frozen population. They should be recorded as unfrozen.
- `contract.json` invariant (line 56): "S049 opened-date basis made explicit without changing the row". `c51eb32` changed S049's used-by cell (SOURCES diff). The lesson calls this a mutable-cell change. The integrator should reconcile the wording. Note that this edit also contributes to the 33 stale `corpus/SOURCES.md` pins.

## 3. Self-reference and dependency traps (order matters)

- T1 Pin fixed point. Existing entries pin SCORECARD.md, LOG.md, SHONEN.md, corpus/README.md, corpus/QUALITY.md, corpus/SOURCES.md and tools/registry.json. A commit that records a monitor number in any of them invalidates the pins that produced it. The number is then valid only at the revision where those pins are current. QUALITY.md:370-375 requires the cited delivered revision to reproduce the count with `overrides_used=false`. Remedy: record numbers only in unpinned files (for example this file or `final/`), measure at the final commit, and never add recording docs to new pins.
- T2 Ordering. Metadata has already landed (`c51eb32`, `d0ec3c8`), so the ledger is stale against HEAD. "Re-anchor after metadata lands" is correct only if these land first: wrapper override refusal and its tests; the registry row expectation; SKILL section 1938 wording (a measured section); SCORECARD and LOG wording. Then re-anchor, commit the ledger, and measure. Any later edit to a pinned path re-stales every entry that pins it (T1).
- T3 SKILL sections are measured content. SKILL.md is an ignored input, but each section is keyed by its text sha256. Correcting section 1938 (exit map or override wording) changes its sha and orphans any entry written against the old text. Fix first, then re-anchor.
- T4 Registry coupling. `tools/registry.json` is pinned by 30 entries and was changed by `d0ec3c8`. Any new monitor row, or any change to the selector row's tally, re-stales those pins. Land registry edits before re-anchoring.
- T5 Selector coupling. No entry pins the selector, so editing it does not stale credit. But the monitor cites its sha, and its registry expectation (`3/3`) must match the new tally.
- T6 Overlay as silent re-anchor (F1). An overlay re-pin looks like a re-anchor in `sections_covered`. Only `overrides_used` and `trace_gate` differ.
- T7 Historical replay. SHONEN now names the round-20 ledger. Replaying the round-19 measure at HEAD reports `box3_ledger_link: false` and restraint 6. Historical replays must pin `32838a5`.
- T8 Rename. Box-3 credit is a substring test for `.ufo/evidence/round-20/coldread/ledger.json` in the box-3 block (frozen 680). Moving the ledger silently drops box-3 points.
- T9 Self-declared evidence. Traces and `commands_executed_count` are author-declared. Validation is not producer authentication, and command coverage is not claimed (QUALITY.md:405-406). Re-anchors are L1-author input-keyed evidence only.
- T10 Drift silences vetoes (F3). Stale failing records stop vetoing. Metadata churn can therefore unmask earlier failures without any entry changing.

## 4. Re-anchor scope for L1 (not executed here)

Minimum 15 new credit-passing entries, one per section below. Each needs non-empty non-ignored pins that match the delivered-revision blobs, `commands_executed_count > 0`, and committed traces whose `inputs` are a subset of the entry inputs with equal digests. Entries are immutable, so these are appended. Head start lines are from HEAD `SKILL.md`.

| HEAD start | Heading (abridged) | Status at HEAD |
|---|---|---|
| 6 | `# tameshi-shokunin` (preamble) | no credit; stale pins |
| 131 | `## Mutation-sweep recipe - numbered steps; bounded cold-read evidence` | stale pins; drift-silenced failing entry 73 (wrong_expectations 1) |
| 375 | `## Restore discipline - proof the substrate never moved` | stale pins |
| 1272 | `## The operator's runbook and the six-leg regression (round ...` | stale pins |
| 1380 | `### The map - where a reader enters, artifact by artifact` | stale pins; drift-silenced failing entry 98 (wrong-expectation) |
| 1479 | `## Repeated controls and gate registry - round 12` | stale pins |
| 1499 | `### Gate/probe registry` | stale pins |
| 1517 | `## Pin disposition and provenance correction - round 13` | stale pins |
| 1548 | `### Round-13 gate/probe registry` | stale pins |
| 1563 | `## Effective expectation reconciliation - round 14` | stale pins |
| 1609 | `## Context gate classification and explicit exit classes - r...` | stale pins |
| 1814 | `## Live-tree re-pin and entry-command monitor - round 17` | stale pins |
| 1846 | `### Round-17 gate/probe registry - re-pin and monitor` | stale pins |
| 1925 | `### Round-18 gate/probe registry - routed-defect closure` | stale pins |
| 1938 | `### Round-20 gate/probe registry - frozen receipt instruments` | no entry at all |

## 5. Docs audit

| Location | Statement (abridged) | Assessment |
|---|---|---|
| SHONEN.md:10 | "lane assertion, input-keyed monitor only; no independent promotion verifier" | Compliant. |
| ledger `provenance` field | "Original entries unchanged; refreshed entries are L1-author source re-reads only, not independent/blind cold-read or required-command coverage" | Compliant. Labelled Round19; update when re-anchored. |
| SCORECARD.md:797-798 | "labeled L1-author input-keyed re-anchoring, never blind or independent cold-read, recipe re-execution or required-command coverage" | Compliant. |
| corpus/lessons/round-20.md:7 | "No promotion, independent cold-read, required-command coverage ... is claimed." | Compliant. |
| LOG.md:1324-1327 | No promotion, numeric increase or survivor closure claimed | Compliant. |
| SKILL.md:1951 | "strict default, no overrides"; "2 usage/could-not-evaluate" | FIX. Overrides are not enforced (F1). Usage exits 64 (frozen 95-97, 151). |
| SCORECARD.md:776 | Calibration stays at 8, asserted before any current measurement | FIX. State as pending; QUALITY.md:364-366 applies. |
| SCORECARD.md:796 | All 184 original entries carried unchanged | FIX. Use 159 carried plus 25 round-19 L1-author entries. |
| Selector help text (frozen 1518) | "input-keyed cold-read ledger coverage" | Acceptable. Frozen text, so keep disclaimers adjacent. |

## 6. Required final monitor fields

Fields follow the round-19 precedent (`.ufo/evidence/round-19/final/monitor-final.stdout`) and QUALITY.md:364-375. Values marked HEAD are current predictions, not measurements.

| Field | Required content |
|---|---|
| `revision`, `rev_input` | 40-hex delivered commit; equal to the commit measured. No later commit may change a pinned path (T1). |
| `calibration_restraint_score` | The current measured value, named even if below 8. HEAD [INFERENCE] at most 6. Prior historical value 8 at `32838a5`, with the delta. |
| `coldread.sections_total`, `sections_covered` | 61 and 61 required for box-3 points. HEAD at most 46. |
| `coldread.box3_full_page` | Required true for restraint 8. HEAD false [INFERENCE]. |
| `coldread.reasons`, `missing`, `uncovered_headings` | Full lists. Include every failing or stale candidate for covered sections, not only uncovered ones (F3). |
| `coldread.inputs_overlay_merged` | Required 0. |
| `overrides_used` | Required false. |
| `trace_gate` | Required `strict`. |
| `ledger_source`, `ledger_committed` | Required `rev` and true. |
| `ledger.path`, `ledger.blob_sha256` | `.ufo/evidence/round-20/coldread/ledger.json`; HEAD 1ba190e5... |
| `ledger.entries`, `ledger.carried_unchanged`, `ledger.l1_author_r19`, `ledger.l1_author_new`, `ledger.buckets` | Recomputed at the measured revision. HEAD 184, 159, 25, 0, 16. |
| `selector.path`, `selector.sha256` | HEAD 4d78a823... (post-fix value must be recorded). |
| `algorithm.path`, `algorithm.sha256` | `.ufo/evidence/round-18/measure.py`; 7ca87a7c... |
| `shonen.blob_sha256` | HEAD f400d74a6452069281f3e91538b6908f558412e48329a7aecf01b2c142ce5a8e. Must equal the pins of every credited SHONEN-pinning entry. |
| `shonen.marks`, `box3_marked`, `box3_ledger_link`, `box3_points` | Four boxes `~`; link true; points as computed. |
| `stale_pin_audit` | At the measured revision: number of stale non-ignored pins among credited entries (must be 0), and the full list for uncredited entries. HEAD 275 stale pairs of 5,316 across 124 of 184 entries. |
| `drift_silenced_failures` | Section, entry index, verdict, `wrong_expectations`, `blocking_gaps`. HEAD: 131/73 and 1380/98. |
| `live_lane_reads` | Bound and unbound counts; `.git/` count reported separately. HEAD: 4 unbound SOURCES digests; 2,515 `.git/` reads. |
| `sources` | Rows, tiers, status, malformed. Round-19: 76 rows, A67/B7/C2, mined 48, queued 23, rejected 5, malformed 0. Re-verify at the delivered revision and note the S049 used-by change. |
| `skill.blob_sha256`, `skill.sections` | HEAD 33d7918601e3df37e9d38be9e023f196555a80cdde20c19621c8e1e33c989a71; 61 sections. |
| `contract` | Commit `6fd220b`; scope note that selector and ledger are unfrozen (F7). |
| `runner_sha256` | HEAD `tools/mutate-and-run.sh` d22c4025...; do not cite 75ed934... |
| `external_inputs` | Informational only. Not credited (ledger provenance). |
| `non_claims` | "lane assertion; input-keyed only; not blind or independent cold-read; not required-command coverage; no survivors closed; no independent promotion." |
| `falsifier` | The strict default command at the delivered revision reproduces the count with `overrides_used=false` (QUALITY.md:372-375). |
| `docs_after_measure` | Name any commit after the measured one. None may touch a pinned path, or the measurement must be repeated. |
| C1 receipts (separate) | Cite `tools/receipt-measure.py --repo ... --rev REV --json` and stage ruler sha f34dc233... (SCORECARD.md:782). They are not the calibration number. |

## 7. Changes to make before any re-anchor (not applied; read-only seat)

1. Wrapper: refuse `--ledger-file`, `--ledger-rev` and `--inputs-overlay` before calling `module.main()` (exit 64, JSON `override-refused`). Refuse `--selftest` combined with other arguments. Add selftest cases for each flag and for `--ledger-rev HEAD:.ufo/evidence/round-19/coldread/ledger.json`. Add a continuation-layout SHONEN case. Update the registry expectation in the same commit.
2. SKILL.md:1951: change "2 usage/could-not-evaluate" to "2 could-not-evaluate; 64 usage". Keep "no overrides" only after item 1 lands. Do this before re-anchoring because section 1938 is measured.
3. SCORECARD.md:776: state calibration as a pending current measurement, with the historical 8 named separately. SCORECARD.md:796: change to 159 original carried unchanged plus 25 round-19 L1-author entries.
4. Ledger `provenance`: update the round label when re-anchored. Keep the non-independence wording.
5. Leave entry 97 as is (original entries are unchanged). Document it as a permanent `input-missing`.
6. New entries should pin only sources actually re-read. Do not pin SCORECARD, LOG, SHONEN, corpus/README, corpus/QUALITY, corpus/SOURCES or tools/registry.json unless they are the sources read.
7. Order: all metadata and registry edits, then re-anchor, then commit the ledger, then measure at that commit with no override flags.

## 8. Checks for L1 after integration (not run here)

1. `python3 .ufo/evidence/round-20/coldread/measure.py --selftest` after item 7.1 (registry row tally updated), and `python3 .ufo/evidence/round-18/measure.py --selftest` (registry rows around tools/registry.json 723-727).
2. `python3 .ufo/evidence/round-20/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <delivered> --explain`, with no override flags. Record every section 6 field.
3. A static pin audit at the same revision: stale credited pins must be 0, and the drift-silenced list must be stated.
4. Confirm the measured revision is the final commit and that no later commit touches a pinned path.
5. `tools/registry-check.py` at the delivered revision.
6. Record SHA-256 of selector, round-18 measure, ledger, SHONEN, SKILL, registry and runner at that revision.

## 9. Passed checks (positive evidence)

- Round-18 measure sha256 equals contract historical `round18-measure` (7ca87a7c...). Stage measure (f34dc233...) and receipt-window (f03ae7e9...) equal their contract frozen values.
- Round-20 ledger bytes equal round-19 ledger bytes (1ba190e5...).
- All 159 round-18 entries appear verbatim in the round-20 ledger; the 25 extra entries are L1-author round-19 entries.
- All 1,832 unique trace paths exist at HEAD and parse as `tameshi-trace-inputs-v1`.
- Replica of the frozen gates at `32838a5` gives 60/60 static upper bound, matching the recorded measurement.
- Selector diff against round-19: four string lines.
- SHONEN diff since `6fd220b`: one line (link target).

## 10. Verification gaps and limits

- Not executed: measure, selector selftest, frozen selftest, registry rows, build, lint and tests.
- The 46/61 figure is a static upper bound from a hand replica, not a measurement. Trace gating and live-read binding are not replicated (they only remove credit).
- Not checked: whether a round-20 "observed-outcome addendum" exists. SCORECARD.md:782 refers to one, and none is present yet. It is an expected final record.
- Traces and declared command counts are not authenticated. This is input-keyed evidence only.
- Four SKILL sections and fifteen ledger buckets were examined by content hash only. No author's reading was re-performed.

## 11. Identities at HEAD `d0ec3c8`

- `.ufo/evidence/round-20/coldread/measure.py`: 4d78a823ebf6e154bf413b6d513891ec7aeb6f93f99dc45dd7d78a74aef9313b
- `.ufo/evidence/round-19/coldread/measure.py`: 4c9c74ca3bb0d85121d6bd3e4deeafe4474374d0a67becf9a9c9fe4c0d42f2f7
- `.ufo/evidence/round-18/measure.py`: 7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37
- `.ufo/evidence/round-20/coldread/ledger.json` (equal to round-19 ledger): 1ba190e5f34dcaf8a38540b48cb2d80835f2f7a656b175f08996077a2b105c02
- `SHONEN.md`: f400d74a6452069281f3e91538b6908f558412e48329a7aecf01b2c142ce5a8e
- `SKILL.md`: 33d7918601e3df37e9d38be9e023f196555a80cdde20c19621c8e1e33c989a71
- `tools/registry.json`: 4b71353dd5afb5f92fe08ef36f19947227d1beec2eee0710b122adefcd2a4468
- `tools/mutate-and-run.sh`: d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b
- Commits: contract `6fd220b`; `c51eb32` (SHONEN pointer, selector and ledger landed, SKILL section 1938, SOURCES, README, QUALITY, LOG); `d0ec3c8` (HEAD; registry rows, SCORECARD, LOG); baseline `c144dcd`; measured `32838a5`.
