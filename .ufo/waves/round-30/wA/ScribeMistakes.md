# Round 30 — candidate Mistakes rows (wave A)

**Verdict:** Three pre-data counter false-greens are demonstrated (v2/K7, v3/K8, and draft-v4/K9); the frozen v4 receipts show these controls rejected. The routed runner defect also has a falsifying old-state execution and a witness for the fix. I do not promote amendment 1's unscored v1 self-attack, or the current dirty-tree status, into execution claims. No `corpus/lessons/round-30.md` was present when read; these are report-only drafts.

**Axes:** calibration (does a counter distinguish the claimed behavior from a cheap non-behavioral program?), evidence provenance (does a receipt actually support the stated revision/result?), and containment (does orchestration isolate and account for its work?).

## Mistakes

1. **class:** v2 accepted a text-keyed selftest that never executed the tally. **evidence:** `.ufo/evidence/round-30/contract-amendment-2.json:7,13-17`; `.ufo/waves/round-30/ctl/CtlK7Keyed.md:19-32,51`; `.ufo/evidence/round-30/ctl/CtlK7Keyed.stdout:35-37`. The control reads `$SELF` for public arm/threshold spellings and has the runtime guard, but no behavioral tally test. **captured-by:** pre-data control CtlK7Keyed; it forced amendment 2. **fix:** v3 adds inserted arithmetic mutants and equivalent rewrites, so static recognition of public arm text no longer suffices. This fix is shown able to fail this control: `.ufo/evidence/round-30/ctl/CtlK7Keyed-v3-rescore-by-L1.stdout:47-49` reports `insert_killed=0/8`, `C1_R30_PASS=false`, `exit=1` (the receipt does not retain its argv). **Old-state command/output:**
   ```sh
   timeout --kill-after=5 900 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r30/ctl/CtlK7Keyed/clone --rev 16a9ad36b8c6c923b75116406c9b1191f43ce924
   ```
   `.ufo/waves/round-30/ctl/CtlK7Keyed.md:26-32` records exit 0 and `.ufo/evidence/round-30/ctl/CtlK7Keyed.stdout:35-37` gives `killed=13/13 heldout_killed=12/12`, `C1_R30_PASS=true`, `exit=0` despite the no-run detector.

2. **class:** v3 accepted a static allowlist for the generators' finite text language without running the tally. **evidence:** `.ufo/evidence/round-30/contract-amendment-3.json:9,25-31`; `.ufo/waves/round-30/ctl/CtlK8NoRun.md:9,17-19,46-52`; `.ufo/evidence/round-30/v4/K8-on-v3.stdout:47-49`. The attempt-1 control's report says its selftest uses string normalization and allowlists, not tally execution; L1 independently re-derived a v3 PASS. **captured-by:** pre-data control CtlK8NoRun, rescored by L1; it forced amendment 3. **fix:** v4 binds the tally block to a committed digest and adds six sealed mutants plus six equivalent rewrites. This correction rejects K8 on the frozen v4 receipt: `v4/K8.stdout:47-48` has `sealed_block_match=0`, `sealed_killed=0/6`, `C1_R30_PASS=false`. **Old-state command/output:** the control report records the invocation template and two concrete revisions:
   ```sh
   timeout --kill-after=5s 900 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30/ctl/CtlK8NoRun/clone --rev 8ad9db7e4def4bf352ee4e12e55b1616bf8d83db
   timeout --kill-after=5s 900 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30/ctl/CtlK8NoRun/clone --rev 545f3575a463735fbc7c8fb25cdafb0029a7fb93
   ```
   `.ufo/waves/round-30/ctl/CtlK8NoRun.md:21-37` records `C1_R30_PASS=true`, `exit=0` on both, and `false`, `exit=1` after exact restoration.

3. **class:** the v4 draft leaked the selftest job label through its working-directory name. **evidence:** `.ufo/evidence/round-30/contract-amendment-3.json:9`; `.ufo/evidence/round-30/v4/K9-on-draft.stdout:59-61`; `.ufo/evidence/round-30/v4/ctl/K9-vs-witness.diff:42-50`. K9 checks `${PWD##*/}` and never runs the tally; on the draft, the counter reports `sealed_block_match=1`, `sealed_killed=6/6`, `sealed_equiv=6/6`, `C1_R30_PASS=true`, `exit=0`. **captured-by:** L1 self-attack before the v4 freeze. **fix:** the frozen v4 runs each selftest in a bubblewrap sandbox that hides job labels and counter context; K9 is rejected by the frozen receipt (`v4/K9.stdout:59-60`: `killed=0/13`, `sealed_killed=0/6`, `C1_R30_PASS=false`). **Old-state command/output:** the K9 stdout preserves the revision and result, but not the exact draft-counter argv. Amendment 3 gives the frozen-counter invocation form (`python3 .ufo/evidence/round-30/c1-measure-v4.py --repo CLONE --rev REV --sealed SEALED_JSON`); do not present that as the observed draft invocation.

4. **class:** regression tally could report PASS after one of nine statuses was omitted, while `--selftest` stayed green. **evidence:** `.ufo/waves/round-29/w1/MutateLegSum.md:103-114,135-156`; `.ufo/evidence/round-30/c1-measure.py:7-10`; `.ufo/evidence/round-30/witness/fix.diff`; `.ufo/evidence/round-30/v4/witness.stdout:1-14,59-61`. **captured-by:** no old detector; MutateLegSum's behavioral harness exposed it. **fix:** the frozen witness adds a runtime tally-completeness guard and a behavioral selftest over extracted tally code. It is shown able to fail the dropped-leg and arm mutants: the witness receipt gives `killed=13/13`, `insert_killed=8/8`, `sealed_killed=6/6`, with all 19 status vectors correct. **Old-state commands/output:**
   ```sh
   timeout 5 bash /tmp/tameshi-r29-MutateLegSum.Anwjjq/tally-mutant.sh 1
   timeout 900 bash tools/mutate-and-run.sh --selftest
   ```
   The first prints `REGRESSION: PASS (cases=9 passed=8 ...)`, exit 0; the second reports `MUTATE_SELFTEST: 97/97 pass` / `VERDICT: PASS`, exit 0 on the mutant. The harness was extracted and fixed-status; the archived report explicitly says no full `--regression` replay was run.

5. **class:** data was dispatched before the final required control report landed. **evidence:** `corpus/lessons/round-29-verifier-spotcheck.md:201-203`; `.ufo/evidence/round-30/r29-mistake1-ordering.txt:1-4`; `corpus/lessons/round-29.md:80-91`. The saved times put `CriticC2v2.md` at 22:33:57.922 after `task-adapter-w1.json` at 22:27:45.552; the report concluded the control call's target was unreachable. **captured-by:** not by the original dispatch gate; the post-hoc timing review caught it. **fix:** round-30 `contract.json:39` records the file-presence hold rule and requires a final path check before treating a seat as dead. This rule is recorded, but the supplied evidence does not demonstrate its enforcement under a failed control. **Old-state check:** round-29.md:90-91 names `stat -c %Y` as the comparison; the historical timestamp output is preserved in `r29-mistake1-ordering.txt`, but that artifact does not preserve the complete original shell argv. Do not upgrade the reconstructed `stat` invocation to an observed command transcript.

6. **class:** the frozen binding did not match the assembler's report shape, excluding ten passing reads; the binding also was not tied to an outside transcript artifact. **evidence:** `corpus/lessons/round-29-verifier-spotcheck.md:194-200`; `.ufo/evidence/round-29/coldread/select-receipt-w1.json:1-6`; `.ufo/evidence/round-29/coldread/c1-dry-all32.txt:1-8`; `.ufo/waves/round-29/res/CriticSelectBound.md:41-52,74-81`. **captured-by:** the post-wave selector receipt and closure's independent binding review, not a pre-freeze pilot. **fix:** the routed proposal is to bind on canonical seat names and effective verdicts (or preserve report labels in assembly), test a real assembled entry before freeze, and bind to an external artifact. No supplied result shows that correction able to fail, so it is not credited as a completed fix. **Old-state command/output:**
   ```sh
   timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 .ufo/evidence/round-29/coldread/select-bound.py --assembled .ufo/evidence/round-29/coldread/assembled-w1.json --out /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-bound.json --receipt /fast/scratch/hyaku/tameshi-r29-critic-select-bound-review-receipt.json
   ```
   `CriticSelectBound.md:49-52` records `assembled=32, kept=22, excluded=10`; `c1-dry-all32.txt` records `appended=32 bound=22`, `C1_R29_V2_PASS=false`. The closure's claim that registry-member reports could be forged is analysis at spot-check line 95, not an executed falsifier; no command/output for that exploit was found.

7. **class:** named-revision receipt and report claims diverged. **evidence:** `corpus/lessons/round-29-verifier-spotcheck.md:33-39,214-216`; `.ufo/evidence/round-29/c2-at-E.stdout:1-4`; `.ufo/waves/round-29/res/RerunC2Head.md:38-55`. **captured-by:** the post-hoc receipt comparison. **fix:** commit a receipt for each revision named as measured and correct the `quote_located=1`/head claims; no round-30 report was available to establish that correction. **Old-state command/output:**
   ```sh
   timeout 900 python3 .ufo/evidence/round-29/c2-measure-v2.py --repo /fast/scratch/hyaku/tameshi-r29-rerunc2head --rev 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef
   ```
   `RerunC2Head.md:47-52` records `quote_located=0`, `C2_F6_V2_PASS=false`, `EXIT=1`; the report's `quote_located=1` did not match that receipt.

8. **class:** orphaned/uncommitted scratch after an interrupted orchestrator — attribution not established. **evidence:** the required read-only command below returned a non-empty status, but includes live round-30 edits and reports; status alone cannot prove these bytes belong to attempt 1 or were left by an orchestrator death. **captured-by:** a clean-tree predicate would fail on this output; it does not capture provenance. **fix:** none demonstrated; do not credit a proposed cleanup or commit as a fix from this snapshot. **Old-state command/output:**
   ```sh
   GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain
   ```
   ```text
    M corpus/QUALITY.md
    M corpus/README.md
    M corpus/SOURCES.md
    M tools/mutate-and-run.sh
   ?? .ufo/evidence/round-30/coldread/
   ?? .ufo/evidence/round-30/r29-mistake1-ordering.txt
   ?? .ufo/evidence/round-30/sources/
   ?? .ufo/evidence/round-30/wA/
   ?? .ufo/waves/round-30/dispatch-wA.json
   ?? .ufo/waves/round-30/dispatch-wA.stderr
   ?? .ufo/waves/round-30/make-spec-w1.py
   ?? .ufo/waves/round-30/make-spec-wA.py
   ?? .ufo/waves/round-30/spec-wA.json
   ?? .ufo/waves/round-30/wA/
   ?? corpus/knowledge/regression-tally-completeness.md
   ```

## Evidence limits and routed-item crosswalk

- Amendment 1 calls the v1 fixed-public-fixture-string shortcut an L1 self-attack, but explicitly says no control, fix, or data seat had run (`contract-amendment-1.json:7,14-19`). The v1 base receipt (`c1-at-base.stdout:19-20`) is a baseline miss (`killed=0/13`, `C1_R30_PASS=false`), not a scored shortcut. Thus no v1 exploit command/result is claimed. The K5 label control later fails v2 (`ctl/CtlK5Labels.stdout:35-37`), but does not retroactively prove a v1 run.
- Round-29 routed item 1 is covered by row 1; item 4 by row 5; item 7's runner leg-sum defect by row 4. Items 2/3 and 6 are represented by rows 6/7 with the limitations above.
- Routed containment item 5(a) misroot and 5(b) foreign-process kill are described at `round-29-verifier-spotcheck.md:204-210`, but the supplied sources do not retain an exact failing command/output for either; they are not promoted as tested fixes here. For 5(c), the spot-check cites `git diff --stat 1a1e8b22 3c16b3a6` → `BuildF6A.md | 12+ 11-` (`:211-213`), but runtime process-group termination was only proposed, not demonstrated able to fail.
- Routed item 7's S059 supersedes row remains a separate source-row task. The current `wA/ReopenS059.md:63-75` is a draft/review and records an uncommitted competing S092 row; it is not evidence of a landed correction or a census pass.

## Scope and hand-off

- **Gates:** none run by this scribe. All counter/selftest outputs above are existing receipts or archived reports; only the read-only `git status --porcelain` command is newly executed here.
- **Touched surface:** this report only: `.ufo/waves/round-30/wA/ScribeMistakes.md`.
- **Out of scope:** no lesson, product code, counter, contract, source row, lane index, or sibling file changed. No `jj` command, subagent dispatch, or tool installation/update.
- **Artifact:** `.ufo/waves/round-30/wA/ScribeMistakes.md`.