# InheritanceCritic — round 12, wave 2

This review is advisory, lane-internal and read-only. It is not admission, promotion or independent verification. I edited no files other than this report. No tools were installed or updated. I read `/home/vgpnk/.omp/agent/RULES.md`.

Axes: calibration (honest provenance and restraint) and identity/provenance (which attempt authored, ran or verified what). Depth is touched only through evidence reuse.

## Verdict

The "clean at round start" and "no inherited work" statements are **true for the headless attempt that wrote them**. They are **false for the in-session attempt that is now running**. The text has no attempt qualifier, so a reader of the committed round would take them as describing the whole round. That is false provenance by omission. Fix it with an append, not a rewrite.

## 1. Timeline (observed)

- Headless attempt: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:405` `launch tameshi round=12 pgid=13129 driver=hyaku slot=3 attempt=1` at 2026-10-19T23:10:59-03:00.
- That attempt ended at `watchdog.log:408` `lane-dead-no-report tameshi round=12 … headless attempt ended by operator directive` at 23:24:27-03:00.
- In-session attempt: `watchdog.log:411` `launch tameshi round=12 pgid=288438 driver=hyaku-inline attempt=1` at 2026-10-20T00:41:11-03:00.
- `ps -g 13129` → no processes. The headless writer is gone.
- `find … -newermt 23:24:27 ! -newermt 00:41:11` → **empty**. Nothing was written between the kill and the resume.
- Every file written after 00:41:11 belongs to w2 or the resumed L1:
  - `spec-w2/dispatch-w2/spawn-w2/assignments-w2/record-w2.json` and `w2/swarm-registry.json`
  - `BashWitness/{selftest.out,declare.out,declaration-hash.txt}`
  - `resumed-before.json` and `resumed-sources-before.txt`
  - `SKILL.md` (00:44:13), `corpus/QUALITY.md` (00:44:21), `corpus/README.md` (00:44:48)
- `git reflog` shows no reset, checkout or stash after `18ad5d0` at 2026-10-19 22:04:36. `git stash list` is empty. No earlier dirt was discarded.
- `.jj` op log contains only workspace-add and git-import operations (20:39), with no working-copy snapshots. It adds no evidence.

## 2. Inherited statements audited

| # | Statement (path:line) | Written by (mtime, window) | True at headless start? | True at resumed start? |
|---|---|---|---|---|
| S1 | `LOG.md:658` "No inherited uncommitted lane or operator work." | headless (LOG 23:20:52) | **Yes** | **No** |
| S2 | `corpus/lessons/round-12.md:3` "`18ad5d0…`, clean at round start." | headless (23:19:13) | **Yes** | **No**, if "round" means the current attempt |
| S3 | `corpus/lessons/round-12.md:38` "complete starting lesson-directory listing (… round-1-verifier-spotcheck.md, round-1.md, round-10.md). No inherited uncommitted work was present." | headless | **Yes**. `git ls-tree 18ad5d0 corpus/lessons/` gives exactly those 3 files | **No**. `round-12.md` itself was already present, uncommitted, and the worktree had 9 dirty paths |
| S4 | `.ufo/evidence/round-12/claims.json:4` `"baseline_clean": true` | headless (23:14:33) | **Yes** | **No** |

Evidence that the headless baseline was clean (all at-write testimony from w1 seats; none of it is a fresh replay):
- `w1/ExitReview.md:7` reports `git status` showing only `.ufo/waves/round-12/` as untracked. That is before `.ufo/evidence/round-12/` existed (dir created 23:14:02), so it is near dispatch at 23:13:51.
- `w1/ReportScribe.md:50` says only the two round-12 directories were untracked, at probe 02:14Z.
- `w1/RegistryReview.md:15` says "HEAD = working tree … no uncommitted drift at check time".
- The reflog has no destructive operation. Both untracked directories were the attempt's own outputs, not inherited work. **Keep S1–S4 byte-preserved as the truthful earlier-attempt baseline.**

## 3. Counterexamples against reading them as round-wide truth

**C-1. At 00:41:11 the resumed attempt inherited 9 dirty top-level paths.** All of them predate the kill, and the gap is empty, so they are attributed to the headless attempt. Mtime shows only the last write, but the empty gap plus the dead pgid makes this strong [INFERENCE].
- Modified tracked files:
  - `LOG.md` (+10, the `:655-663` entry)
  - `corpus/SOURCES.md` (+7/−5: S004/S006/S011/S026/S028 cells)
  - `corpus/knowledge/witness-scoped-kill-verdict.md` (+3, E2/E3)
- Untracked files:
  - `corpus/knowledge/repeated-control-precondition.md`
  - `corpus/lessons/round-12.md`
  - `tools/repeat-control.py` (23:24:06)
  - `tools/bash-witness-study.py` (23:24:22)
  - `.ufo/waves/round-12/` (spec/dispatch/assignments/record-result plus w1: 30 reports and the registry)
  - `.ufo/evidence/round-12/`: 448 inherited files in waves+evidence, versus 24 written after the resume.

**C-2. The headless attempt was killed mid-wave, and some inherited artifacts are truncated work, not finished outputs.**
- The w1 registry has 32 members (`record-result.json`), but `w1/` holds 30 reports. **ControlGate and BashWitness, the two production executors, never reported.**
- `ControlGate/run-{1,2,3}.*` and `mismatch/` were written at 23:24:19, 8 s before the kill. There is no `expected.json`.
- Before w2, `BashWitness/` held only `pristine.sh` (23:14:43), as `spec-w2.json` WitnessFinish states.
- `BytesReview.md` (23:24:21) and `FailureOracle.md` (23:23:33) landed in the last minute, so they may reflect interrupted probes. `BytesReview.md:50` itself says "probe2 … did not complete cleanly".
- So "inherited" must not be read as "completed and verified".

**C-3. Runtime results in the inherited LOG were run by the headless attempt only.**
- `LOG.md:660`: "Guardrails actually run … 80/80 … six pinned legs PASS". Source files are `runner-selftest.txt` (23:15:38) and `runner-regression.txt` (23:17:28).
- `LOG.md:658`: census exit 0, from `sources-before.txt` (23:14:09).
- These are headless observations. The resumed attempt re-ran the census only (`resumed-sources-before.txt`: `tameshi ok …`, `exit=0`). I found no resumed runner selftest or regression receipt.
- Under the round prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-12.md:157-160`), reused outputs must be re-verified or named as discarded. Until then, `LOG.md:660` is earlier-attempt testimony.

**C-4. Unfulfilled forward promises were inherited.**
- `LOG.md:663`: "New claim commands and the final measured revision are recorded below after runtime verification."
- `corpus/lessons/round-12.md:30`: "Runtime receipts appended below."
- Neither has been fulfilled. The resumed attempt must fulfil both, or append that the headless attempt did not.

**C-5. Attempt identity collides.**
- Both launches are recorded as `attempt=1` (`watchdog.log:405` and `:411`). The L1 task text also says "attempt 1 in-session".
- If the report refers to "attempt 1", it is ambiguous. It must name driver plus launch time or pgid: `hyaku` pgid 13129 at 23:10:59 versus `hyaku-inline` pgid 288438 at 00:41:11.
- Separately, w1 member `agentId`s equal the bare names (`"agentId": "ControlGate"`, `record-result.json`). w2 uses `TameshiR12.*`. w1 seat IDs therefore cannot be resolved through `history://`. Cite w1 reports as files, not as live agents.

**C-6. The resumed baseline measures the committed revision, not the inherited worktree.**
- `resumed-before.json` gives `"revision": "18ad5d0…"`, the same value as the headless `before.json` plus the `calibration_*`/`unique_recorded_gates` fields.
- That is correct as a committed baseline. But it was produced by the **inherited** `measure.py` (headless, 23:16:56), and it does not describe the 9 inherited dirty paths.
- The report must say both things: (a) the baseline is the committed rev; (b) the inherited delta is listed separately with reuse/discard decisions.

**C-7. Resumed-session forward references (not inherited, but the same risk).**
- New `SKILL.md`/`corpus/README.md` text cites the following paths, which **do not exist** at review time (`ls` → "No such file or directory"):
  - `.ufo/evidence/round-12/verification.json`
  - `ControlGate/expected.json`
  - `BashWitness/{summary,declaration,manifest}.json`
- They must exist before commit (QUALITY criterion 9). Owners: ControlFinish, WitnessFinish, CapabilityEvidence, L1.

**Non-defect, recorded to prevent a false alarm.** `git diff SKILL.md` shows one `-` line. It is the old no-newline-at-EOF marker. `cmp -n <committed size>` confirms that the committed bytes are a strict prefix in `SKILL.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/README.md` and `witness-scoped-kill-verdict.md` (all `PREFIX_OK`). AdmissionBounds' `git diff -U0 … has no '-' lines` check (`w1/AdmissionBounds.md:68`) would wrongly fail on this. Use a byte-prefix check instead.

## 4. Smallest safe corrections (append-only; L1 owns the writes)

Do **not** edit `LOG.md:658`, `lessons/round-12.md:3,38` or `claims.json:4`. They are a truthful record of the headless attempt.

1. **LOG.md**: append a bullet to the round-12 entry, after `:663`:
   > - Attempt provenance (append-only correction to `:658`): the entry above was written by the headless attempt (hyaku, pgid 13129, launched 2026-10-19T23:10:59-03:00, ended `lane-dead-no-report` 23:24:27, `watchdog.log:405,408`); "no inherited uncommitted work" is true of that attempt's start at clean `18ad5d0`. The in-session attempt (hyaku-inline, pgid 288438, 2026-10-20T00:41:11-03:00, `watchdog.log:411`) inherited that attempt's uncommitted outputs — `LOG.md`, `corpus/SOURCES.md`, `corpus/knowledge/witness-scoped-kill-verdict.md`, `corpus/knowledge/repeated-control-precondition.md`, `corpus/lessons/round-12.md`, `tools/repeat-control.py`, `tools/bash-witness-study.py`, `.ufo/waves/round-12/` (w1; ControlGate and BashWitness unreported), `.ufo/evidence/round-12/` — and resolved them per the round prompt: reused-and-reverified {…}, discarded {…}. The `:660` runner results are headless-attempt observations unless a resumed receipt is cited.

2. **corpus/lessons/round-12.md**: append under "## Authority and dispatch":
   > ### Inherited work (resumed attempt)
   > Lines 3 and 38 describe the headless attempt's start and remain true for it. The in-session attempt did not start clean: it inherited the nine paths named in `LOG.md` round 12 attempt-provenance bullet, including this file. "Attempt 1" is ambiguous (`watchdog.log:405,411`); attempts are identified by driver and launch time.

3. **Evidence**: leave `claims.json` and `before.json` byte-preserved. Add a new `.ufo/evidence/round-12/inherited.json` that records:
   - each inherited path, its sha256 at resume and its pre-kill mtime;
   - a decision per path: `reused-reverified` (with receipt path), `reused-testimony` or `discarded`;
   - `baseline_clean_headless: true` and `baseline_clean_resumed: false`.

   Report and LOG should cite this file instead of mutating S4.

4. **Fulfil or retract** the forward promises at `LOG.md:663` and `lessons/round-12.md:30` with resumed-attempt receipts. If they cannot be fulfilled, append that the headless attempt did not produce them.

5. **Runner guardrails**: either re-run `--selftest`/`--regression` in the resumed attempt and cite those receipts, or label `LOG.md:660` as earlier-attempt testimony. Do not present the old output as resumed verification.

6. **Report wording**: list w1 as "32 dispatched, 30 reported; both production executors interrupted". Do not write "one validated 32-seat batch" without the w2 addition (`LOG.md:659`, `lessons/round-12.md:36` are true only for w1).

## 5. Impacted axes and judgment class

- **Calibration.** If S1–S4 are committed unqualified, an overreach goes uncorrected. This is a fixable defect, because append-only corrections restore truth. It is not a tradeoff.
- **Identity/provenance.** The attempt=1 collision (C-5) and the w1 agentId shape are fixable through report wording.
- **Depth.** Not moved by this review. C-2 and C-3 bound how much inherited evidence C1/C2 can cite without a fresh replay. The canonical judge should refuse any C1/C2 acceptance that rests only on headless ControlGate/BashWitness partial outputs.

## Owned paths

- `.ufo/waves/round-12/w2/InheritanceCritic.md`: this file, the only write.
