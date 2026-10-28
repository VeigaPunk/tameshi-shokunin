# tameshi — round 56 (hyaku run 11, attempt 1) — REPORT SKELETON

<!-- ============================================================================
DRAFT-ONLY BLOCK. This block is not part of the report: delete it (and this
comment) when the skeleton becomes `.ufo/reports/round-56/tameshi.md`.

Who fills it: the L1 (`TameshiR56`). Every `<fill: ...>` names the receipt, commit
or command that produces the value; no slot may be filled from prose, from a seat's
summary, or from this file. Fill discipline, checked mechanically before filing:

    grep -c 'fill:' <report>           # must print 0 (the same token; after this
                                       # draft-only block is deleted nothing else says it)
    grep -c '^## SHONEN' <report>      # must print 1  (marker rule, prompt §4)
    git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-remote origin refs/heads/master
                                       # must print the final lane hash the report cites
                                       # (pre-report gate, prompt §5.4)

Shape sources: prompt `.ufo/prompts/tameshi-round-56.md` §4 (required sections, in
this order), round-55 report (`.ufo/reports/round-55/tameshi.md`) for the register,
`corpus/lessons/round-55-verifier-spotcheck.md` for what the closure grades
(per-claim re-derivation, a verdict that names the revision it measured, a quoted
value that its own receipt contains, dispositions of R55.1–R55.7, no uncommitted
round work, no closure-seat contamination).

ONE BLOCKING FINDING AT DRAFTING (wave 1, two seats + this seat, receipted):
C2's `docs` arm cannot reach 4/4 as frozen. `.ufo/evidence/round-56/c2/measure.py:245`
builds the mined set with `cells[8] == 'mined'`, but `corpus/SOURCES.md`'s 11 cells are
`[id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by]` —
status is `cells[7]`, `cells[8]` is `opened`. Over the committed bytes at `c3e2ca9f`:
`rows=140 cells[8]==mined=0 cells[7]==mined=113`. With all four doc surfaces present
in a fixture the frozen counter prints `arm6-docs 3/4`; with the single index corrected
it prints `4/4` at the same revision. So `C2_R56_PASS=true` is unreachable until an
amendment is recorded in `.ufo/evidence/round-56/freeze.json` `amendments` — before any
control set is scored and before the single deciding invocation.
Receipts: `T56W1ScribeReport-receipts/docs-arm-mined-cell.txt`,
`…/docs-arm-amendment-demo.txt`, peer `T56W1ExecC2Counter-receipts/d-demo2-alldocs.stdout`,
peer `T56W1ScribeKnowledge-receipts/arm6-simulation.stdout`.
If the amendment does not land, the C2 row below must read its frozen verdict and the
report must say the claim was unreachable by instrument, not that it was measured false.

SEAT NOTES (T56W1ScribeReport, scribe, leaf — no subagent dispatch)
What this seat did: read the round-56 contract, both frozen counters (arm lists and the
exact predicates they enforce), `freeze.json`, the round-55 report and the round-55
non-author spotcheck, `SHONEN.md`, the standing axis table (`SCORECARD.md:2574-2580`),
`corpus/QUALITY.md` 105/106, `corpus/README.md` `## Frontier`, and the wave-1 peer
receipts; then wrote this skeleton and its slot manifest. Nothing in `SKILL.md`,
`SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**` or `.ufo/evidence/round-56/` was
touched; no git/jj mutation ran anywhere; no tool was installed (curl 8.23.0, python
3.14 and git were already on the host).
Receipts (this seat's): `T56W1ScribeReport-receipts/docs-arm-mined-cell.txt` (the
arm-6 index defect, replicated over committed bytes), `…/docs-arm-amendment-demo.txt`
(shared-clone fixture at `c3e2ca9f` + one commit carrying the four real doc surfaces:
frozen counter `arm6-docs 3/4`, one-index-corrected copy `4/4` at the same revision),
`…/skeleton-shape.txt` (section order, marker count, JSON block parses, slot inventory).
Slot manifest: `T56W1ScribeReport.json` (104 slots by section, the four filing gates,
and the two blocking findings) — the skeleton's own JSON block is the single source for
the report's machine-readable summary; the manifest is not that summary.
Out of scope, declared: no lane production edit, no frozen-instrument edit, no counter
run at the lane, no control/deciding/no-harm run, no census re-run beyond the round-start
validation, no SHONEN box change, no commit.
Integration checklist for the L1 (each is enforced by a frozen arm, not by taste):
  1. the re-key directory name is `rekey-r56-` + exactly 12 hex of C0; entries' `read_rev`
     is the full 40-hex C0; readers' `cand` is that same 40 hex;
  2. the restated calibration row must be the LAST 5-cell `| calibration |` row, or arm 6
     reads the round-54 row instead (it takes `rows[-1]`);
  3. arm 6's note surface is dead until the `cells[7]` amendment is recorded in `freeze.json`;
  4. `before/{c1,c2,c2-at-base}.stdout` must be committed at C0 — they are untracked at
     `c3e2ca9f` (peer receipt `T56W1ScribeLog-receipts/cited-paths.txt`), the R55.6 class;
  5. the deciding run refuses a dirty tree, so the control receipts and the `after/` outputs
     must be committed in the order the script expects (`clean-tree-before.txt`).
============================================================================ -->

L1 `TameshiR56`. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`. Instrument set frozen at
`c3e2ca9f020776b3d66c7af854fb82c834674fcf` (`freeze.json`, amendments `<fill: .ufo/evidence/round-56/freeze.json amendments length>`).
Content commit C0 `<fill: commit hash carrying the round's content>`; measured revision
`<fill: revision the deciding run certified>`. Round shape: three waves (`w1` build/falsify,
`w2`/`w3` re-key readers and post-bind), seat counts `<fill: .ufo/waves/round-56/*/swarm-registry.json>`.

**Declared claims (2, frozen before data).**
- **C1, calibration** — the lowest non-retired axis. The round-55 edits cost the round-21
  cold-read monitor 18 of 64 credited sections and the 18-heading re-key never landed (R55.3);
  at base the monitor reads `6` while the standing calibration row still asserts `8`. C1's
  surface: the eighteen base-lost headings re-read at one content commit C0, bound under one
  `rekey-r56-<c0>` directory, with the precheck reading `lost=0` and the standing row stating
  the score the monitor actually reads at the commit it names. Counter
  `.ufo/evidence/round-56/c1/measure.py` (`C1_R56_PASS`).
- **C2, operability** — every receipt the lane certifies is bound to the revision it was
  measured against, by `tools/receipt-revision-gate.py`, and the gate refuses the real receipts
  the lane accepted in rounds 54 and 55. Counter `.ufo/evidence/round-56/c2/measure.py`
  (`C2_R56_PASS`).

## Work performed

Two claims, frozen before data: **C1 on calibration** (the cold-read floor — the eighteen
base-lost headings re-read at C0 and bound under one round-56 re-key, and the standing axis row
restated to the score the monitor reads) and **C2 on operability** (receipt↔revision binding —
`tools/receipt-revision-gate.py`, the rule it enforces, and the real receipts it refuses).

- **C1 — the eighteen base-lost headings are re-read at one content commit and bound under one
  round-56 re-key.** `<fill: what landed — rekey dir rekey-r56-C0-12HEX under .ufo/evidence/round-21/coldread/, 18 reader reports under .ufo/waves/round-56/w2|w3, the restated standing row>`;
  evidence `<fill: .ufo/evidence/round-56/after/c1.stdout>`, `<fill: commit hash of the bind>`.
  Integration constraints the frozen arm 3/4/6 enforce (verified in
  `.ufo/evidence/round-56/c1/measure.py:64,184-260`): the directory name matches
  `^rekey-r56-([0-9a-f]{12})$` and its 12 hex must resolve to C0; every bound entry's
  `read_rev` is C0's **full 40 hex**; every reader report's `cand` equals that same 40 hex and
  its `section_sha256` equals the section's sha256 at REV; no bound entry pins `LOG.md` or
  `SCORECARD.md`; the restated row must be the **last** 5-cell `| calibration |` row in
  `SCORECARD.md`, its score cell equal to the monitor's score at REV, its measured-commit cell
  resolving to a commit whose monitor score is that same value, its evidence cell naming
  `round-21`, its last-change cell naming `56`.
- **C2 — the rule, the gate and the refusals.** `tools/registry.json` carries the gate's cell
  naming its refusal codes; `corpus/knowledge/receipt-revision-binding.md` opens with the
  provenance trio (`source:` / `verified-at:` / `recheck:`) and cites a `mined` S-row;
  `corpus/QUALITY.md` criterion `<fill: 107>` states the rule with the gate's own refusal code on
  the real round-54 receipt as its falsifier; the `SKILL.md` `## Standing rules` bullet names
  `receipt-revision-gate`; `corpus/SOURCES.md` gains the round's one row. Evidence
  `<fill: .ufo/evidence/round-56/after/c2.stdout>`, `<fill: commit hash of C0>`,
  `<fill: T56W1ScribeReport-receipts/docs-arm-mined-cell.txt>` for the arm-6 index defect below.
- **Instrument falsification (frozen; defects reported, never edited).** Arm liveness for both
  counters `<fill: receipt>`; gate fuzz and mutants `<fill: receipt>`; the phase-A/phase-B control
  sets `<fill: .ufo/evidence/round-56/control/controls-a.stdout, controls-b.stdout>`; the single
  deciding invocation `<fill: .ufo/evidence/round-56/after/deciding-run.exit>`; the 15 no-harm
  monitors `<fill: .ufo/evidence/round-56/after/no-harm.stdout>`; freeze discipline
  (`FROZEN_UNCHANGED=1`, amendments before controls) `<fill: .ufo/evidence/round-56/after/frozen.stdout>`.
- **Dispositions of the seven routed defects R55.1–R55.7** — each is fixed, or reported with the
  reason it is not: `<fill: corpus/lessons/round-56.md §dispositions table>` (R55.3 by C1, R55.5 by
  C2, R55.1/R55.2/R55.4 as record corrections, R55.6 by committing the inherited evidence, R55.7
  by the closure-side rule).
- **What did NOT run, stated plainly.** `<fill: any instrument, wave or seat that did not execute,
  and what that costs the claim>`; the counters' own `cannot_see` sentences stand: C1 cannot tell
  a reader who computed `section_sha256` from the tree from one who read the section, and C2
  cannot tell a receipt produced by the run it claims from one that copied a `rev=` token.
- **Wave shape.** `<fill: seats per wave and attack share from .ufo/waves/round-56/*/swarm-registry.json>`.
- **Incidents.** `<fill: scratch, collision, or contamination incidents; or "none recorded">`.
- **Tool installs.** `<fill: tool, version, channel, reason — or "none this round">`.

## Landed changes

| Change | LOG entry | Commit |
|---|---|---|
| C1: 18-heading re-key `rekey-r56-C0-12HEX` + 18 reader reports; standing calibration row restated to the monitor's score at the commit it names | `LOG.md` `## <fill: date> — round 56` | `<fill: c0 / bind commit>` |
| C2: `tools/registry.json` gate cell; `corpus/knowledge/receipt-revision-binding.md`; `corpus/QUALITY.md` criterion `<fill: 107>`; `SKILL.md` `## Standing rules` bullet; `corpus/SOURCES.md` row `<fill: S281>` | same entry (C2 paragraph) | `<fill: c0>` |
| `SCORECARD.md` round-56 block (both claims, before/after, controls, restated standing row) | same entry | `<fill: c0>` |
| `corpus/lessons/round-56.md` (`## Gate`, `## Mistakes`, R55.1–R55.7 dispositions) | same entry | `<fill: c0>` |
| Instruments frozen before data: contract, both counters, `tools/receipt-revision-gate.py`, controls, no-harm, deciding run | same entry (freeze paragraph) | `c3e2ca9f` (+ `<fill: amendment commits, if any>`) |
| Wave specs, dispatches, registries and seat deliverables under `.ufo/waves/round-56/` | round-shape paragraph | `<fill: commits>` |
| The round's receipts: `before/`, `control/`, `after/` under `.ufo/evidence/round-56/` | same entry | `<fill: c0 / deciding commit>` |

## Before → after measurements

Counting command, both claims (run from the lane, `<empty dir>` fresh each time):
`python3 .ufo/evidence/round-56/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <rev> --work <empty dir> --explain`
and the same with `c2/measure.py`.

| Claim | Before | After | Measured commit |
|---|---|---|---|
| **C1** calibration | `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` (`.ufo/evidence/round-56/before/c1.stdout`); precheck `floor=0a2010acd1e9 floor_credited=64 cand=981c5e8b20a2 cand_credited=46 lost=18 RED` | `<fill: .ufo/evidence/round-56/after/c1.stdout — expected C1_R56_PASS=true, total=0, credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8-at-its-commit>` | `<fill: measured revision>` |
| **C2** operability | `C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` (`.ufo/evidence/round-56/before/c2.stdout`); at base before the freeze the same counter printed `error=gate-missing total=1` (`.ufo/evidence/round-56/before/c2-at-base.stdout`) | `<fill: .ufo/evidence/round-56/after/c2.stdout — the frozen arm 6 caps at 3/4 until the cells[7] amendment is recorded; see the draft-only block>` | `<fill: measured revision>` |

Controls: `<fill: .ufo/evidence/round-56/control/controls-a.stdout — CTL_0_c1/c2, CTL_SKIP_c1/c2, CTL_FAB_c1/c2, CTL_RESTATE_c1 all false as pre-registered>`
and `<fill: .ufo/evidence/round-56/control/controls-b.stdout — CTL_POS_c1/c2 true at the revision they certify, CONTROLS_B: 2/2>`.
A control that cannot fire is not a pass: quote the receipt's own line, including any
`CTL_MISMATCH` (R55.4).

## Sources & frontier

- Census, round start: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit `0`,
  `140` rows (`grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md`); receipt `<fill: .ufo/waves/round-56/w1/T56W1ExecCensus-receipts/census-validate-base.stdout>`.
  Round end: exit `<fill: 0>`, `<fill: row count>` rows; receipt `<fill: .ufo/evidence/round-56/after/census.stdout>`.
- Rows added by tier: `<fill: S281 — tier A, kind spec, status mined>` — *Statement layer
  specification (in-toto Attestation Framework v1)*, `https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md`,
  pin `df02077b…` (tag `v1.2.0`), sha256 `cbe684a1…ebea`, opened 2026-10-28; located quote
  (11 words, `## Fields`, `subject`, lines 54-55): *"Subject artifacts are matched purely by
  digest, regardless of content type."* It grounds the rule that a receipt is evidence only for
  the content it was measured against; it is **not** sourced for the lane's `rev=` encoding or for
  DSSE verification (proposal: `.ufo/waves/round-56/w1/T56W1ScoutSource.md`; duplicate sweep
  there exited 1 on seven fragments).
  Rows refused before append: `<fill: DSSE protocol, https://github.com/secure-systems-lab/dsse/blob/master/protocol.md — reason>`
  `<fill: or "none refused">`.
- Rows touched old→new: `<fill: S…: used-by …→…, or none>`.
- Frontier rows advanced: `<fill: none | the F-id that moved, with its before→after>` — the ten statuses are unchanged
  (`F1 held r25, F2 partly r1, F3 open, F4 partly r38, F5 Core r21, F6 held r50, F7 open,
  F8 partly r27, F9 open, F10 held r49`; `awk -F'|' '/^\| F[0-9]+ \|/{…}' corpus/README.md` and
  `git diff 981c5e8b..<rev> -- corpus/README.md` empty for the frontier regions). C2's ground is
  the lane's own deciding gate, not a frontier row.
- Assimilation: `<fill: shokuknow merge/tameshi entries adopted or "none — reason">`.

## Trend verdicts

- **expansion — `<fill: unchanged|improved|harmed|unprovable-but-better>`.** `<fill: evidence: no
  frontier row advanced and no capability claimed; the one new source row is knowledge on an
  operability surface the lane already owns>`.
- **quality — `<fill: improved|harmed|unchanged|unprovable-but-better>`.** `<fill: evidence: the four doc surfaces now state the receipt-binding
  rule and the gate refuses the real accepted receipts; counter-signal: the frozen docs arm could
  not count the note until the index amendment, and C2's own-receipts arm depends on the round's
  control set>`.
- **discernment — `<fill: improved|harmed|unchanged|unprovable-but-better>`.** `<fill: evidence: the round's own instruments were falsified before
  the deciding run, one frozen-instrument defect was found by measurement and reported rather
  than edited, and R55.1–R55.7 were dispositioned with receipts>`.

No scalar: each verdict names what moved and what did not.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources —
  `<fill: evidence pointer at the measured revision>` (`SHONEN.md:5-6`)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `<fill: LOG.md entry +
  receipts>`; no independent promotion verifier (`SHONEN.md:7-8`)
- [~] Instructions executable by an agent without oral context — `<fill: the monitor's reading at
  the measured revision: 64/64 score=8 box3=true, or the honest shortfall>` (`.ufo/evidence/round-21/coldread/ledger.json`)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `<fill: evidence that only lane files
  were written and siblings read read-only>` (`SHONEN.md:11-12`)

No box is `[x]`: `[x]` requires a named non-author verifier, and none ran this round.
`<fill: or name the verifier and the box it checked>`

**Stale-lane:** respawn-per-round driver; no other mission of this lane is open.
**Round end state:** lane `master` at `<fill: lane HEAD>` = remote (`<fill: ls-remote origin
refs/heads/master output>`), `<fill: ahead=0>`; report filed last on the fleet repo via
`fleet-commit.sh --as tameshi`; round verdict `<fill: admitted-candidate | partial | harmed>`.

```json
{
  "lane": "tameshi",
  "round": 56,
  "attempt": 1,
  "l1": "TameshiR56",
  "base": "981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1",
  "freeze": "c3e2ca9f020776b3d66c7af854fb82c834674fcf",
  "amendments": "<fill: .ufo/evidence/round-56/freeze.json amendments length>",
  "c0": "<fill: content commit>",
  "measured_rev": "<fill: measured revision>",
  "lane_head": "<fill: lane branch tip at filing>",
  "lane_remote_head": "<fill: ls-remote origin refs/heads/master output>",
  "claims": {
    "C1": {
      "axis": "calibration",
      "counter": "python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev REV --work EMPTY --explain",
      "before": "C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false",
      "before_receipt": ".ufo/evidence/round-56/before/c1.stdout",
      "after": "<fill: after/c1.stdout verdict line>",
      "after_receipt": "<fill: .ufo/evidence/round-56/after/c1.stdout>",
      "pass": "<fill: true|false>",
      "rekey_dir": "<fill: .ufo/evidence/round-21/coldread/rekey-r56-C0-12HEX>",
      "headings_bound": "<fill: K>/18",
      "readers": "<fill: R>/18",
      "monitor": "<fill: score>/<fill: credited>",
      "restate": "<fill: score@commit>"
    },
    "C2": {
      "axis": "operability",
      "counter": "python3 .ufo/evidence/round-56/c2/measure.py --lane LANE --rev REV --work EMPTY --explain",
      "before": "C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false",
      "before_receipt": ".ufo/evidence/round-56/before/c2.stdout",
      "after": "<fill: after/c2.stdout verdict line>",
      "after_receipt": "<fill: .ufo/evidence/round-56/after/c2.stdout>",
      "pass": "<fill: true|false>",
      "docs": "<fill: k>/4",
      "own": "<fill: PASS|REFUSED|own-receipts-missing>",
      "instrument_defect": "docs arm reads cells[8] (opened) for the mined status; status is cells[7]; receipt T56W1ScribeReport-receipts/docs-arm-mined-cell.txt",
      "amendment": "<fill: recorded in freeze.json before controls? yes|no>"
    }
  },
  "controls": {
    "phase_a": "<fill: .ufo/evidence/round-56/control/controls-a.stdout — n/m as pre-registered>",
    "phase_b": "<fill: .ufo/evidence/round-56/control/controls-b.stdout — n/m as pre-registered>",
    "no_harm": "<fill: ok count>/15 — .ufo/evidence/round-56/after/no-harm.stdout>",
    "frozen_unchanged": "<fill: .ufo/evidence/round-56/after/frozen.stdout>",
    "deciding_run_exit": "<fill: .ufo/evidence/round-56/after/deciding-run.exit>"
  },
  "sources": {
    "rows_before": 140,
    "rows_after": "<fill: row count>",
    "rows_added": "<fill: [S281]>",
    "rows_touched": "<fill: []>",
    "frontier_advanced": "<fill: []>",
    "census_exit": "<fill: 0>",
    "census_receipt": "<fill: .ufo/evidence/round-56/after/census.stdout>"
  },
  "trends": {
    "expansion": "<fill: unchanged|improved|harmed|unprovable-but-better>",
    "quality": "<fill>",
    "discernment": "<fill>"
  },
  "shonen": {
    "boxes": 4,
    "checked": "<fill: count of [x]>",
    "partial": "<fill: count of [~]>",
    "untouched": "<fill: count of [ ]>",
    "named_non_author_verifier": "<fill: none>"
  },
  "stale_lane": "respawn-per-round driver; no other mission of this lane is open",
  "tool_installs": "<fill: []>",
  "gates": {
    "marker_shonen_count": "<fill: marker count, must be 1>",
    "fill_slots_remaining": "<fill: 0>",
    "pre_report_gate": "<fill: lane hash printed by ls-remote origin refs/heads/master>"
  }
}
```
