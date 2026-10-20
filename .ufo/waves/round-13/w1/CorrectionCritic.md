# CorrectionCritic — round-12 verifier routed defects: ownership, follow-through, residuals

Seat: TameshiR13.CorrectionCritic (critic, leaf, read-only; this report is the only write). Advisory to L1. This is not an admission.
Source: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-12-verifier-spotcheck.md` §"Routed defects and residuals" (:140-147). Its author is the non-author closure: commit `546b371`, protocol-shokunin, 2026-10-20T01:11:30-03:00. The lane must never edit this file.
State inspected: lane HEAD `546b371`. The worktree had uncommitted L1 integration: LOG/QUALITY/README/SOURCES and new knowledge, `.ufo/evidence/round-13/{claims,before}.json` and `measure.py`. `tools/witness-metadata.py` and `tools/pin-disposition.py` had not landed yet.
Tool installs/updates: none.

## 1. Itemized routed defects

| # | Routed item (spotcheck line) | Owner | Round-13 carrier | Status at read |
|---|---|---|---|---|
| 1 | Hyaku renderer appends relative seat `Report:` destinations (:144) | **Operator** (renderer in ufo-fsd-alpha / hyaku) | none (not lane-fixable) | **Recurs, mitigated.** The `Report: write your scoped findings to .ufo/waves/round-13/w1/<Name>.md` line is relative in 32/32 `dispatch.json` task texts. All 32 items also name the absolute own-report path, and the context is absolute. No fleet-root misroot was observed: fleet `.ufo/waves/round-13/` holds only Oct-13 files, and no `w1/` exists. |
| 2 | Closure prompt's run-now wording vs the Gate standard's non-execution rule; the helper is not the full frozen step-1 checker (:145) | **Operator / orchestration** | none | Open, and not lane-owned. The lane may only refrain: no sibling-gate execution and no closure-gate claim. |
| 3a | Replace the brittle host-addendum line cite with the named planner-ruling section, append-only (:146) | **Lane (L1 integration)** | No seat owns the edit. EvidenceConnector is read-only. L1 drafted the correction at LOG.md:758-764. | **In progress.** See conditions C3a-1 to C3a-3. |
| 3b | Repair nested `declaration.kind=null` only through new evidence; no frozen rewrite (:146) | **Lane**: MetadataRepair executor, plus L1 QUALITY14 | `tools/witness-metadata.py`, `.ufo/evidence/round-13/witness-metadata.json` | Not landed. See conditions C3b-1 to C3b-4. |
| 4 | Carried debt, intentionally unchanged: full-page SKILL cold-read/box3, legacy provenance headers, F1 interop, stale-successor ledger, runbook ER-R3; no promotion (:147) | **Lane, carried** (provenance-header route marked "operator call", README:94-95) | Disclosure only | Named in the README round-13 block draft. See conditions C4-1 to C4-3. |

## 2. Historical immutable evidence (never rewritten; supersede only by append)

- `corpus/lessons/round-12-verifier-spotcheck.md`: non-author, all lines.
- `LOG.md:659` and `corpus/lessons/round-12.md:62` both cite `scripts/hyaku/lane-addendum.md:33-36`. Round-12 w2 seat reports carry further numeric cites:
  - `AdmissionCritic.md:37,43,76,130,132`
  - `LessonEvidence.md:13,45,47,49,51,53,79,80`
  - `PriorMistakes.md:133,156`
- Frozen BashWitness bytes; sha256 matched the git blobs at both `8742f5d` and HEAD:
  - `summary.json` `acc01268…47b9`
  - `declaration.json` `e8d2024a…0901`
  - `declared.tsv` `0def0d3b…41d3`
  - `declaration-before-run.txt` `d2343ddf…0042`
  - `manifest.json` `273ffc39…e1cf`
  - `rerun-20261020T035435Z/summary.json` `6726421f…`, which also carries `kind: null`
- Producer `tools/bash-witness-study.py`: `249d9dcd…3f1a`, equal to `summary.tool.sha256`. It is unchanged since `9df9212`.
- Round-12 receipts: `verification-final.json`, `oracle-repair.json` and `/tmp` argv. Closure explicitly declined to rewrite them (spotcheck :88, :149).
- `SCORECARD.md` round-12 rows :295-328, including the plan sentence :326-328. SOURCES immutable cells, including S041's teaches cell. The diff only flips the S041 status and used-by cells and appends S047; no immutable cell was overwritten.

## 3. Conditions and defects

### Item 3a (L1)

**C3a-1: the round-12 citation was stale when it was committed. "Lines moved later" is an incomplete account.**
- `git show 3eb7c58:scripts/hyaku/lane-addendum.md` has the ruling at :33-35. That revision is dated 2026-10-19T23:15, the headless attempt 1.
- At `cadb3e3` (00:41:50) the ruling sits at :41-43.
- At `1c57eb9` (00:52:53), which was live when `9df9212` (01:01:32) committed `round-12.md:62`, lines 33-36 are the `ufo-swarm-wave.mjs run` command and the reportDir sentence. That is not the ruling.
- The w2 cites `:41-44` and `:45-49` were right at `cadb3e3`/`1c57eb9`. They are off by one since `ad7ddd1`; the ruling is now :42-45 and routing :46-50.
- Smallest correction: L1's LOG append should state that the cite was valid only at `3eb7c58`. Pin the named section to a fleet revision: HEAD `168fcf6`, blob `1084093ec64fa57f4fdb1c9d734b8908c28771f8`. The blob is clean (`git status --porcelain` is empty for that path). The named section is "## 6. Campaign addendum — hyaku", item 2, **Planner seat (orchestrator ruling 2026-10-19, kama/tsukuroi r11–12 L0 lines)**.
- Also add one sentence that the numeric lane-addendum cites in the round-12 w2 seat reports are superseded the same way. Rewrite none of them.

**C3a-2: the draft promises a file that does not exist yet.** LOG.md:773 and the README round-13 block cite `corpus/lessons/round-13.md` and say the citation is "corrected in this round's … named-heading lesson". That file did not exist at read. Commit those sentences only together with the lesson's named-heading correction.

**C3a-3: identity.** Do not relabel the round-12 planner mapping. Round-12 w1 used ClaimSkeleton, a reviewer, as data-walk carrier; that is disclosed non-conforming under the ruling (`round-12/w2/AdmissionCritic.md:37-45`). Round-13 PlanningDataWalk is a revenger, which conforms. Keep both facts.

### Item 1 (operator, residual)

**C1-1: the LOG states more than the dispatch shows.** LOG.md:767-768 says "Explicit absolute seat destinations avoid round-12's fleet-root write mistake." The dispatched task text still ends with a relative `Report:` line in 32/32 seats. Each seat therefore receives two conflicting destinations.
- Smallest correction: append "renderer-appended relative `Report:` line persists (operator-owned, spotcheck item 1); absolute item paths mitigate it; no fleet-root misroot observed at <time>".
- Do not claim item 1 cured, and do not edit the fleet renderer: it is fleet `scripts/` or an external repo, outside lane write scope (lane-addendum :62-67).

### Item 3b (MetadataRepair; message sent)

**C3b-1: a second frozen null exists.** `rerun-20261020T035435Z/summary.json:15` has `kind: null` too. The companion must either anchor it as well, or state that it corrects only the canonical `summary.json` and that the rerun null stays uncorrected. MetadataSelftest.md:18 saw this; nothing in the assignment scopes it.

**C3b-2: location trap.** `cmd_check` walks the round-12 evidence directory with `rglob` and fails UNLISTED files (`bash-witness-study.py:811-814`, `:1182-1184`). Any file written under `round-12/BashWitness/` turns the registered probe's `check` from CLEAN into FAIL, which harms operability. The assigned path `.ufo/evidence/round-13/witness-metadata.json` is safe; keep to it.

**C3b-3: the producer defect stays live.** `bash-witness-study.py:787` reads `declaration["declared"]["kind"]`, but the writer puts `kind` at the top level (:875). Any future `run`/`rerun` will emit null again.
- No seat owns this file. Editing it is outside MetadataRepair's write set and would make the frozen `summary.tool.sha256` historical.
- Name it as lane debt with anchor `:787`, owner tameshi. The companion corrects observations, not the producer. Do not claim the defect "repaired" in general.

**C3b-4: kind semantics.** The normalized kind must equal `declaration.json:6` byte-for-byte: "declared-witness mapping (not a blind preregistration)". It must carry the disclosure. "Blind" by substring is a trap (MetadataSelftest.md:37). The QUALITY14 wording ("reject the old-null companion and accept the kind-only repair") holds only if the selftest has both arms with literal exits.

### Item 4 (carried debt)

**C4-1: plan divergence is undisclosed.** `SCORECARD.md:326-328` planned the next claim as "freshness — measure and disposition the existing stale-successor ledger debt". Round 13 instead claims C1 under depth for current-content pin dispositions, and the round-13 LOG entry does not mention the change.
- Append a sentence: the plan was superseded, pin readings are content freshness only, freshness stays unchanged, and stale-successor mutation re-sweeps remain open (README draft :+11-12 already says this; LOG/SCORECARD must agree).
- No row may be appended to `knowledge/fleet-kill-rate-ledger.md` as a successor from a pin reading.

**C4-2: F7 status.** README :120-121 says "A ground reads `held` only when its next move is measured." F7's next move is "per-leg reuse decisions classified". A constant `result_reuse=not_established` for all six legs is a uniform boundary, not a per-leg reuse decision.
- F7 should stay `open`, or at most become `partly held` with that reason. The README draft says "advances…not a full incremental result cache", which is acceptable only if no status cell flips to `held`.

**C4-3: SKILL edit trap.** README:99-103 says "the next `SKILL.md` edit re-runs" the cold-read. GateScribe will propose registry rows, which is a SKILL edit. Round 12 already appended to SKILL without re-running it and disclosed that (README:143-146).
- Round 13 must repeat the disclosure and must not read the registry append as a cold-read, box-3 credit or promotion.
- SHONEN stays `[~]`; scalars stay depth 6 and calibration 6.

### Minor

**M1: a superseded claim cell is cited as support.** S041 flips to `mined` with used-by pointing at the new knowledge, while S047 says S041's teaches cell is superseded. The knowledge entry must cite S047 (or the primary bytes) for every corrected claim, not S041's cell. Spot-read lines 187-188 cite S041 for "unproven" and "swap locations"; KnowledgeSupport should confirm those are within S041's still-valid scope.

**M2: dispositions file has no owner.** The README draft and `measure.py` read `.ufo/evidence/round-13/pin-dispositions.json`. PinProbe owns only `pin-manifest.json`. L1 must produce and commit the probe's output at that exact path. Otherwise `measure.py` reports `pin_dispositions: null` and C1's "after" is unmeasured.

## 4. Exact checks for L1 (not executed by this seat)

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --quiet 546b371 -- .ufo/evidence/round-12 tools/bash-witness-study.py corpus/lessons/round-12.md corpus/lessons/round-12-verifier-spotcheck.md`: expect exit 0.
2. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 546b371 -- LOG.md SCORECARD.md corpus/QUALITY.md corpus/README.md | grep -c '^-[^-]'`: expect 0. All changes must be appends.
3. In the same diff for `corpus/SOURCES.md`, every `-` line must be S003 or S041 differing only in the status/used-by cells, plus the "Next unused id" line.
4. Run `sha256sum` over the six frozen BashWitness files in §2 and compare each to the listed digest.
5. `python3 tools/bash-witness-study.py check`: expect `WITNESS_CHECK: CLEAN … 96 files covered, 95 manifest entries`, exit 0. The same counts as the round-12 baseline prove no file was added under the round-12 evidence directory.
6. `cd /home/vgpnk/Projects/shokunin && git status --porcelain .ufo/waves; ls .ufo/waves/round-13/w1 2>&1`: expect no output, then "No such file", meaning no misroot.
7. `git -C /home/vgpnk/Projects/shokunin show 326b4d2:scripts/hyaku/lane-addendum.md | grep -n 'Planner seat (orchestrator ruling'`: expect `42:`. Cite the heading text plus the revision, not a line number.
8. Grep the round-13 lesson, LOG and SCORECARD appends for `lane-addendum.md:[0-9]`: expect 0 new numeric cites.
9. Grep the round-13 appends for `held`, `seventh`, `6 → 7`, `re-sweep` and `successor`. Every hit must be negated or bounded (C4-1, C4-2).
10. Confirm that `corpus/lessons/round-13.md` and `.ufo/evidence/round-13/{witness-metadata,pin-dispositions}.json` exist in the same commit as the LOG/README sentences that cite them.
11. The companion selftest or check must show:
    - old-null red: exit 1 with an exact token;
    - kind-only repair green: exit 0;
    - tamper: exit 2 before any comparison;
    - missing companion: exit 2;
    - for every case, no `Traceback` on stderr.
    It must also state rerun-summary coverage explicitly (C3b-1).
