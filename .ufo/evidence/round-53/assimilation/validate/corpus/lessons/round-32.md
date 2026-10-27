# Round 32 — lesson (tameshi)

Base `e24688b2ff6cca1c9ad20e112f02c629b8597ff8` (round-31 spot-check head). L1 TameshiR32, attempt 1
(`.ufo/watchdog.log`: `launch tameshi round=32 … attempt=1`, no `lane-dead-no-report` line; nothing
inherited; `jj-lane.sh state` at start: `tracked=0 untracked=0`).

One claim, **C1 — operability, capability acquisition** (stagnation nudge: depth 9 and calibration 8 at or
above the saturation line 8; no capability since round 25). Surface: a new versioned tool
`tools/tally-audit.py` that audits `tools/mutate-and-run.sh` without editing it. **Result: miss.**

Round order: freeze v1 `c3181497` → wave-1 record `e9f3b957` → v2 re-design `b50a18f0` (amendment 1) →
tool re-freeze and counter hardening `528f8dee` (amendment 2) → content revision `a4f71813` → wave-2 record
`21f7de32` → ledger append `4b529ee9` → sealed held-out set and measurement revision `24a5a5bb` → this record.

## Gate

Sources opened this round:

- **S097** (new; seat SrcBashExit, re-opened by ReviewSources with equal bytes):
  https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303,
  accessed 2026-10-23 UTC, 415804 bytes, sha256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`.
  Quote (§Exit Status, lines 3896–3897, 19 words): "Exit statuses fall between 0 and 255, though, as explained
  below, the shell may use values above 125 specially." Second quote (§Conditional Constructs `case`, lines
  1081–1082, 12 words, read by the L1 in the same pinned bytes): "The first pattern that matches determines
  the command-list that is executed." The rendered page https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
  timed out on every attempt (curl exit 28), so the row names the source file that was opened.
- **S099** (new; seat SrcMutationAdequacy, re-opened by ReviewSources): https://pitest.org/, accessed 2026-10-23 UTC,
  12023 bytes, sha256 `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc`. Quote (§What is mutation
  testing?, HTML line 114, 14 words): "The quality of your tests can be gauged from the percentage of mutations killed."
- **S094** (re-opened; seat ReopenS094): https://arxiv.org/pdf/1411.2664, PDF sha256 equal to the pin
  `6e9532a9…d697`. Quote (§1, printed page 2, 17 words): "Each submitted model is evaluated on a (fixed) test set
  that is available only to the organizers." Supports the sealed held-out design by analogy only.

Rejections:

- **S098 (Bash manual, Conditional Constructs page): not written.** Seat SrcBashCase could not open the URL (both
  addresses timed out); no bytes, no row. The `case` rule is cited through S097's pinned source instead.
- **Counter v1, before data.** Control seat CriticC1's 27-line allowlist met it (`kill=18/18 accept=8/8
  C1_R32_PASS=true`, two seeds) without running any tally, oracle or harness: every v1 copy family is public.
- **Tool `158202f8`, before any v2 run.** Seat DeterminismProbe found that its harness panel could not see a
  harness that skips singleton position 0 or 1 (16 of 72 gH05 pairs escaped). Re-frozen as `9639c458`.
- **"C1 closes the runner items" as the size of the gain.** CriticSize: the runner's own selftest still passes
  the eight MutateHead survivors; the tool is an outside audit, and the measurement shows it is incomplete.

Row changes, old → new (`corpus/SOURCES.md`, rows 94 → 96):

| ID | status | recheck | used-by |
|---|---|---|---|
| S094 | mined → mined | 730d → 730d | `corpus/knowledge/regression-tally-completeness.md` → that path plus `corpus/knowledge/runner-tally-audit.md` |
| S097 | (none) → mined | (none) → on-release | (none) → `tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md` |
| S099 | (none) → mined | (none) → 180d | (none) → `tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md` (`a4f71813`) → `corpus/knowledge/runner-tally-audit.md` (`24a5a5bb`; the frozen tool does not cite S099, lane census v2 flagged it, seat RerunCensus) |

## Controls before data (wave 1, 35 seats, none dead)

Scored with frozen counter v1 (`.ufo/waves/round-32/w1/`): do-nothing 0/18 0/8; always-pass 0/18 8/8;
always-fail 18/18 0/8; junk 4/18 4/8; sha pin 18/18 1/8; region diff 18/18 2/8 and 3/8; line count 6/18 6/8,
byte size 13/18 3/8; sha table 12/18 8/8; text-keyed 11/18 8/8; sibling consensus 18/18 3/8; static-only
2/18 8/8; runtime-only 6/18 8/8; harness-only 10/18 8/8; old selftest 2/18 8/8; combo shortcut 13/18 8/8 —
all false. CriticC1's counter-reading allowlist: true. v1 was re-designed before data as v2: the tool runs
under bwrap with only itself and one copy visible, its bytes are pinned, and a sealed held-out set written
after the freeze by seats who did not write the tool is added, each copy checked by the counter (a witness
for kills, observational equivalence for accepts). Amendment 2 re-pinned the tool after DeterminismProbe's
finding and closed a copy-order side channel (ReviewCounter F2) before any v2 run (ReviewAmend2Facts: no
`C1_R32V2:` line from real tool bytes before `528f8dee`). The L1 ran the working tool on the public v1
families (688 bodies over 200 seeds, 0 misses; `v2/dev/`) before the re-freeze, as disclosed in amendment 2.

## After measurement

First full v2 run at `24a5a5bb` (`.ufo/evidence/round-32/after/c1v2-at-measurement.stdout`, exit 1):

```
C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 rev=24a5a5bb598ae919546715267d76f814efaf8912 C1_R32V2_PASS=false
```

The held-out set (22 files from five completed author seats, committed unedited; byte-identical to the seats'
files by `cmp`) found what the public fixtures did not. Must-kill copies the tool passed: HeldOutGuard-1/-2
(majority-gated FAIL; divisibility guard), HeldOutLoop-1/-2 (status masked to seven bits; a leg status
overwritten), HeldOutTallyArms-01/-02 (conditional double count; grouped `126|127` arm as a flag),
HeldOutPrintf-1/-2 (count fields wrong for 3 failing or setup legs), HeldOutRefactor-k1 (status 5 at one
position). Must-accept copies the tool rejected: HeldOutLoop-3/-4 and HeldOutRefactor-a4 (an auxiliary leg
loop the stress rewrites instead of the tally loop), HeldOutRefactor-a3 (a second extraction line; exit 2).
C1 is a miss under its kill rule. No capability row enters the table.

No harm: runner sha256 unchanged; strict monitor `covered=64/64 restraint=8 box3_mismatch=0 depth_score=9` at
`24a5a5bb` (content revision 59/64 by design; 13 of 14 assembled cold-read entries kept by binding v5 and
appended, ledger 480 → 493; ColdA01's report was rejected by the assembler because its JSON did not parse);
command D `recorded_cases=9 depth_score=9`; fleet census exit 0 with the same eight W04 warnings; lane
census v2 CLEAN, 96 rows. `--then-regression` ran the full nine-leg replay after a passing audit:
`TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)` (ThenRegression).

## Mistakes

1. **class:** a fix to a widely read file deferred twice with no other route recorded. **evidence:**
   `corpus/lessons/round-30.md:207-212`, `round-31.md:176-179,188`. **captured-by:** the round-31 closure, routed
   item 3. **fix:** the versioned-tool route (a new tool reads the runner; the runner stays byte-identical);
   shown able to fail: the route landed a tool whose own measurement failed, while the monitor stayed 64/64.
2. **class:** a command reported with no exit receipt. **evidence:** `.ufo/evidence/round-31/after/commandD-at-final.stdout`
   with no `.exit`. **captured-by:** the round-31 closure. **fix:** `.ufo/evidence/round-32/receipt-check.py`;
   shown able to fail: on `.ufo/evidence/round-31` it exits 1, `missing_exit=5`, listing that file (the other
   four, `ctl/bind-v5-*.stdout`, are re-scoring captures that were never receipt pairs: a disclosed false
   positive class, ReviewReceiptCheck). On `.ufo/evidence/round-32` it exits 0.
3. **class:** a base reading stated without a receipt. **evidence:** round-31 report "base covered 64/64";
   `.ufo/evidence/round-31/before/` has no monitor receipt. **captured-by:** the round-31 closure. **fix:**
   `repair/c1monitor-at-r31-base-36c1d393.*` and `before/c1monitor-at-base.*` this round; shown able to fail:
   `ls .ufo/evidence/round-31/before/c1monitor-at-base.stdout` → absent.
4. **class:** a fixture set that is entirely public, so a tool author can memorize it. **evidence:**
   `.ufo/waves/round-32/w1/CriticC1.md` (v1 met, true). **captured-by:** the pre-data control wave. **fix:**
   counter v2's sealed held-out set; shown able to fail: the measurement receipt (`ho_kill=1/10`), where the
   same tool scored 18/18 and 8/8 on the public copies.
5. **class:** a selftest that only exercises the case nothing else covers, so it cannot see its own blind spot.
   **evidence:** DeterminismProbe (16 of 72 gH05 pairs escaped tool `158202f8`). **captured-by:** a seat outside
   its item. **fix:** nine position-only faults and selftest cases for positions 0 and 1 (`528f8dee`); shown able
   to fail: `--selftest` cases `harness position 0 skipped` and `harness position 1 skipped` exit 1 by design.
6. **class:** a tool tuned on visible fixtures. **evidence:** dev sweep 688 bodies, 0 misses
   (`v2/dev/devsweep-200.stdout`) against 13 of 22 sealed copies wrong. **captured-by:** the sealed held-out set.
   **fix:** none landed (the tool is frozen); routed below.
7. **class:** a declared pre-data step skipped. **evidence:** amendment 1 `controls_before_data` (v2 controls
   before the L1's first v2 run); the first run came first. **captured-by:** none (the L1 noticed after the run).
   **fix:** none shown able to fail; the controls ran afterwards as observations (`.ufo/waves/round-32/res/`).
   Next contract: the counter refuses to run unless a committed control receipt names its sha.
8. **class:** a count copied from an older revision. **evidence:** `contract.json` and LOG "270 of 480"; recount
   282 of 480 at `a4f71813` (ReviewEntry, ReviewScorecardLog). **captured-by:** wave-2 review. **fix:** errata in
   SCORECARD and the entry; shown able to fail: the recount command in `w2/ReviewEntry.md`.
9. **class:** a source row naming a user that does not cite it. **evidence:** lane census v2 at `a4f71813`:
   `no-id-or-path-cite: S099 tools/tally-audit.py`, VIOLATIONS. **captured-by:** the lane census v2 (the fleet
   census does not check it). **fix:** S099 `used-by` cell; shown able to fail: census v2 at `a4f71813` exit 1.

Misroot sweep: see the round report.

## Holds (dead seats)

Three wave-2 mutation-tester seats stopped on the provider safety filter with `Codex error event: This content
was flagged for possible cybersecurity risk … (code=cyber_policy)`: HeldOutFree (43 s), HeldOutHarnessVectors
(1 m), HeldOutHarnessCmp (5 m). Not retried or rerouted. HeldOutHarnessCmp left four files in its scratch
dir; they are not evidence and were not committed.

## Routed defects of round-31-verifier-spotcheck.md

1. Header test → `.ufo/evidence/round-32/repair/c1-r31-measure-v2.py` (`header[1] == 'Score (0–10)'`); the frozen
   round-31 counter is unchanged. Same verdicts as v1 at `36c1d393` (7) and `08125328` (0) (RunCounterV2).
2. Append-only by bytes → the same v2 (byte prefix from byte-mode `git show`). CtlHeaderV2: shape C (CRLF) and
   D (U+200B) rejected by v2; shapes A and B were confounded at a head that already passed.
3. Per-leg tally and the 8 MutateHead survivors → C1 (miss; the tool exists and catches every frozen survivor
   and the per-leg defect, but not the sealed copies).
4. Evidence gaps → round-31 base monitor receipt and command D receipts with exits (`repair/`); the round-31
   receipt without an exit stays as written.
5. Earlier queue (MutCounter M07/M08, dead-seat threshold, binding v5 FA-1..FA-3, QUALITY 69/71 errata,
   `mte-interop.py` SETUP): not worked this round; carried.
6. S055 digest drift: not re-opened this round; carried.

## Routed to round 33

- Tool v2 of `tally-audit.py` (new file; v1 stays as the measured object): runtime vectors over every count of
  failing and setup legs 0–9, all statuses at every position, the tally loop chosen as the loop that feeds the
  tally counters, tolerance of a second extraction line, stdout-only comparison (ReviewTool M1), a timeout on
  `--then-regression` (ReviewTool L1, SentinelTool). Re-measure on a new sealed set.
- Counter v2 defects (ReviewCounterV2): `witness.loop` names reach bash unquoted (validate names before use);
  a non-string block witness crashes; held-out discovery is not recursive.
- Held-out author prompts: avoid "defeat" wording that trips the provider filter (three dead seats).
