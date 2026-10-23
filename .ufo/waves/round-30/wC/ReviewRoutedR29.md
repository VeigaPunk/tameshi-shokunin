# ReviewRoutedR29 — dispositions of round-29 routed defects 1-7 in committed lane bytes

seat: ReviewRoutedR29
rev: 9207f226e177c8a1a9a82de677df3cd9f8d1cda3
method: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 9207f226e177c8a1a9a82de677df3cd9f8d1cda3:<path>` (GIT_OPTIONAL_LOCKS=0), plus `git log`/`git diff --name-only` for ordering checks.

## Verdict

**4 resolved, 1 resolved for the lane share with an operator-owned remainder, 2 partial, 0 open.**
Defects 1, 2, 3 and 7 are resolved. Defect 5's lane share (seat-prompt clauses 5a/5b) is resolved; 5(c) is
operator-owned runtime enforcement and has no lane disposition to check. Defect 4 is partial: the
committed-order rule and falsifier receipt landed and were applied to every control that gated data, but
two registered attack controls (CtlS3DenyList, CtlS8TokenBag) never spawned and have neither a report file
nor a committed "recorded dead with its error text" receipt. Defect 6 is partial: the preventive criterion
landed and round-30 receipts exist for every revision a receipt names, but the required erratum to the
round-29 report belongs in the round-30 fleet report, which does not exist yet at this commit (pending by
design).

## Disposition table

| # | Defect | Disposition (path:line @ 9207f226) | Status | Reason |
|---|---|---|---|---|
| 1 | Unscored shortcut control class; no hold path in contract | `.ufo/evidence/round-30/contract.json:28-34` (required classes incl. K5 labels, K6 bytes), `contract.json:39` (hold_rule), `.ufo/evidence/round-30/ctl/CtlK5Labels.stdout` (PASS=false exit=1), `ctl/CtlK7Keyed.stdout` (PASS=true -> forced v3 re-design), `v4/ctl2/CtlK5Labels-v4.stdout` and `CtlK7Keyed-v4.stdout` (re-scored under v4, both false), `contract-amendment-4.json` (C1 declared exploratory before data after CtlS2SymEval met v4); captured by `corpus/QUALITY.md:653-663` (criterion 58) | resolved | Every "keyed on ids or labels / bytes" class was scored before data with committed receipts; the contract carries a hold rule naming this routed defect; when a control met the counter the kill rule executed (v3, v4 re-designs) or the claim went exploratory per criterion 58's stated escape. SealHeldout's death was handled by the hold rule's recorded L1-substitute path (amendment-3 reason: sealed set "written by this L1 (hold rule: 'by another seat or by the L1, recorded as such')"). |
| 2 | Binding is syntactic | `.ufo/evidence/round-30/coldread/bind-select-v3.py:157-159` (receipt records transcript path, byte size, sha256, session_id per seat), docstring lines 1-20 (registry membership + assistant-authored `COLDREAD <seat>:` in a host transcript), `.ufo/evidence/round-30/coldread/append-entries.py` docstring lines 11-13 (each appended entry gets `binding`: registry agent id, transcript path, byte size, sha256); captured by `corpus/QUALITY.md:677-689` (criterion 60) | resolved | Each appended entry binds to an outside artifact (host session transcript, hash and session id) that is recorded in the ledger receipt, so a closure checks it without a session search. Note: registry `agentId` is null for spawn-kind members (`wA/swarm-registry.json:28`), so the recorded agent id may be null; the transcript sha256+session id carry the check. |
| 3 | Assembler/binding shape mismatch (Mistake 5) | `bind-select-v3.py:22` ("verdicts are not compared: the assembler normalises them"), `norm()` retry/prefix stripping, `:103` `no-reports` (= the bool(reports) ask), `:150-154` trace-of-seat checks; pilot-before-freeze receipts `.ufo/evidence/round-30/attempt3/bind-controls.txt` (v3: real 31/32, donothing 0/32, promptonly 0/32, textmention 0/32, noresult 0/32, forged 30/32) | resolved | The new binding no longer compares assembler-normalized verdicts, normalizes seat labels itself, requires non-empty reports, and was tested on the round-29 pilot assembly before freezing (attempt-2 PilotBind D1-D7 plus the attempt-3 five-control battery). The 10 excluded round-29 reads were not retroactively credited; round-30 credit comes only through the new wave's frozen binding. |
| 4 | Control-before-data ordering (Mistake 1) | `.ufo/evidence/round-30/r29-mistake1-ordering.txt:1-4` (committed falsifier evidence: mtime lines + `first-commit bc2058a4` for both files); committed-order application: all v4 control receipts at lane commit `713dee6a` (03:08:50) before content revision `bb681566` (03:11:04) and before the wave-B/C specs; captured by `corpus/QUALITY.md:665-676` (criterion 59) | partial | The ordering rule and its evidence are committed and were applied to every control that gated data (all ctl2 receipts precede the content revision in lane commit order). Residual: wave-A attack controls CtlS3DenyList and CtlS8TokenBag are registered with `agentId: null` (`wA/swarm-registry.json:26-35, 62-70`) but never produced a report file, and no committed "recorded dead with its error text after a final check of that path" receipt exists for them. Amendment-4 records them only as "pending at writing … their outcome cannot change this decision". The criterion-59 closeout was therefore skipped for two formally moot seats. |
| 5 | Containment | 5(a): `spec-wA.json:4`, `spec-wB.json:4`, `make-spec-wC.py:54-56` — "Every `Report:` trailer path is relative to …/tameshi-shokunin — write it at …/tameshi-shokunin/<that path>, never at the fleet root"; pre-assembly presence sweep implemented by `.ufo/evidence/round-30/attempt3/verify-inherited-wA.py` + `inherited-removed.txt` (report files compared with registry members/transcripts; leftovers removed with receipt). 5(b): same contexts — "Never kill a process you did not start: before any kill, check that /proc/<pid>/cwd is inside your own scratch dir". 5(c): operator-owned. Captured by `corpus/QUALITY.md:690-700` (criterion 61) | resolved (lane share); 5(c) open by owner | Both seat-prompt clauses are verbatim in every committed wave context (wA, wB) and the committed wave-C generator; the attempt-3 verify script does the file-vs-registry presence comparison criterion 61 names. 5(c) — runtime killing a seat's process group at its deadline — was routed to the operator in the defect text itself; the lane's only share is the prompt-side mitigation ("kill any process tree you started before you return"), which is present. |
| 6 | Receipt gaps | `corpus/QUALITY.md:701-710` (criterion 62: a report names a revision as measured only if a counter receipt for that revision is committed; carried values labelled inferred) | partial | The preventive rule is committed and round 30 conforms so far: `v4/base.stdout` names rev `9ed6db84`, `v4/head.stdout:59` names rev `bb681566`, `v4/witness.stdout`, `head/c1monitor-at-bb681566.stdout` and `head/census-at-bb681566.stdout` each name the revision they measure. The corrective half — "correct the report's C2 `quote_located=1` / head-commit claims in the round-30 report" — is pending by design: no round-30 fleet report exists at this commit. |
| 7 | Carried items (S059 row; runner leg-sum; mistake-1 evidence) | 7(a) `corpus/SOURCES.md:101` — S092 "supersedes S059's anchor only", digest `266915c5…`, status `queued`; it is round 30's first SOURCES edit (see evidence). 7(b) `tools/mutate-and-run.sh:1453-1462` — tally completeness guard printing `REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)`; `:135-136`, `:1989-2039` selftest tally harness incl. the loop-missing-operand case at `:2033-2039`. Scored: `v4/base.stdout` `refused_drops=0/9 killed=0/13` -> `v4/head.stdout:59-61` `refused_drops=9/9 killed=13/13 … sealed_killed=6/6 sealed_equiv=6/6`, `PREDICATE: C1_R30_PASS=true`, `exit=0`. 7(c) `.ufo/evidence/round-30/r29-mistake1-ordering.txt:1-4` committed | resolved | All three carried items are landed. The leg-sum defect is closed functionally (drop mutants refused 9/9 at head vs 0/9 at base); the claim itself is declared exploratory by amendment-4, so the fix's claim-level verdict rides on the reviewer-seat rule, which is the contract, not a gap. |

## Evidence commands (observed output)

- `git show 9207f226:contract.json` -> `hold_rule` at line 39 names routed defects 1 and 4 verbatim;
  `controls_required_before_data` at lines 28-34 lists K5 (labels) and K6 (bytes).
- `git show 9207f226:.ufo/evidence/round-30/ctl/CtlK5Labels.stdout | tail -4` ->
  `PREDICATE: C1_R30_PASS=false`, `exit=1`; `ctl/CtlK7Keyed.stdout` -> `PASS=true`, `exit=0` (forced v3).
- `git show 9207f226:.ufo/evidence/round-30/v4/head.stdout | grep -n 'C1_R30:\|PREDICATE\|exit='` ->
  line 59 `rev=bb681566… refused_drops=9/9 killed=13/13 … sealed_killed=6/6 sealed_equiv=6/6`, line 60
  `PREDICATE: C1_R30_PASS=true`, line 61 `exit=0`; `v4/base.stdout` -> `refused_drops=0/9 killed=0/13`,
  `PASS=false`.
- `git show 9207f226:.ufo/evidence/round-30/r29-mistake1-ordering.txt` -> 4 lines: the two mtime lines
  and both files' `first-commit bc2058a4`.
- `git log --format='%h %s' 9ed6db84..bb681566 -- corpus/SOURCES.md` -> exactly one commit `bb68156`
  (content revision): S092 is round 30's first SOURCES edit.
- `git show 9207f226:.ufo/waves/round-30/wA/swarm-registry.json` -> `CtlS3DenyList` and `CtlS8TokenBag`
  entries with `"agentId": null` (lines 26-35, 62-70); neither appears in `wA/*.md` (ls-tree listing).
- `git show 9207f226:.ufo/evidence/round-30/attempt3/bind-controls.txt` -> v3 kept 31/32 real entries,
  0/32 on donothing / promptonly / textmention / noresult controls; 30/32 on forged.
- `git show 9207f226:.ufo/waves/round-30/spec-wA.json` and `spec-wB.json` -> the never-kill and
  fleet-root clauses both sit inside the single-line `context` field (line 4 of each file).
- `git log` on `9207f226` -> control receipts and specs precede the content revision:
  `713dee6a` 03:08:50 (ctl2 receipts + spec-wA) -> `bb681566` 03:11:04 (content revision) ->
  `07ed440a` 03:16:37 (head receipts + spec-wB) -> `9207f226` 03:48:53 (binding v3 + wave-C generator).

## Smallest safe corrections

- Defect 4 residual: at integration, append two lines to `attempt3/inherited-removed.txt` (or a sibling
  receipt) recording CtlS3DenyList and CtlS8TokenBag as dead/unspawned — `agentId: null`, empty report
  path check — so the criterion-59 file-presence closeout covers every registered control seat.
- Defect 6: carry the erratum into the round-30 fleet report at write time: name the round-29 report's
  C2 `quote_located=1` value and its three head-commit claims, with the correction `quote_located=0` and
  receipt `.ufo/evidence/round-29/c2-at-E.stdout` at `7a45f7b9`. No action needed before the report is
  drafted.

No tools installed or updated this item; no production files touched; all reads via read-only `git show`
with `GIT_OPTIONAL_LOCKS=0`.
