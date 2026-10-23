# Round 30 — lesson (tameshi)

Base `9ed6db840dc97a0a5f4758b6b5f60cee83a61645` (round-29 spot-check head).
Three attempts: TameshiR30 (died with the orchestrator at 05:25:25Z; landed `dcdf2d08`, `e59728df`,
`8a8d2540`), TameshiR30A2 (died with the orchestrator, omp SIGSEGV, 06:19:06Z; landed `f09d3425`,
`713dee6a`, `bb681566`, `07ed440a`) and TameshiR30A3 (this record). Attempt 3 re-checked what it builds on:
the strict monitor at `bb681566` (`covered=33/64 restraint=6 box3_mismatch=1`, the same stdout as
`.ufo/evidence/round-30/head/c1monitor-at-bb681566.stdout`) and at base (`covered=64/64 restraint=8
box3_mismatch=0`); the v4 head receipt (re-run by seat RerunC1Head, byte-identical counter lines);
the census (exit 0); the authorship of the 23 uncommitted wave-A reports against their seats' host
transcripts (`.ufo/evidence/round-30/attempt3/inherited-wA-receipt.txt`: every file written by its own
seat; 18 equal to the seat's last `write`, 5 edited afterwards by the same seat).

One claim, **C1 — operability, EXPLORATORY**: the `--regression` case tally of
`tools/mutate-and-run.sh` (runtime completeness guard) and the runner's own `--selftest` as its
detector. Routed by `round-29-verifier-spotcheck.md` item 7 (MutateLegSum). Sourced on S087, S093
and S094. Contract chain: `contract.json` (v1) → amendments 1-3 (counters v2, v3, v4, each forced
before data by a control that met the previous one: the L1's own fixed-string self-attack, CtlK7Keyed,
CtlK8NoRun) → amendment 4 (`713dee6a`, before the content revision): C1 declared exploratory after
control CtlS2SymEval met v4 by modelling the tally block instead of running it. No counting command
and no numeric target; the v4 receipt is supporting evidence only.

Round order (QUALITY 56, 63): every widely read input edit (runner fix, SOURCES S092-S094 and S087
used-by, QUALITY 58-65, README Round-30 section, the knowledge entry) landed in `bb681566`; the cold
reads of wave C read `bb681566`.

## Gate

Sources re-opened this round (attempt 3, wave C seats; attempt-2 seat reports for S087):

- S092 (supersedes S059's anchor), seat ReopenS092: https://bazel.build/remote/caching.md fetched
  2026-10-23T07:14:23Z and 07:15:44Z, both sha256
  `266915c5d73f2cfe7d4ddcd9bb36a78e6037a710a71f2bab7d35b16d67768a5b` (16210 B), the row's pin. Located
  quote (line 345): "Bazel currently does not track tools outside a workspace." (9 words). Admit:
  the row stands as written (`queued`, used-by `—`).
- S093, seat ReopenS093S094: https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml
  fetched 2026-10-23, sha256 `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`
  (33289 B), `cmp` equal to `.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml`. Located quote
  (bwrap.xml:159): "Unshare all possible namespaces. Currently equivalent with: --unshare-user-try
  --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try" (15 words). Admit.
- S094, seat ReopenS093S094: https://arxiv.org/pdf/1411.2664v3 fetched 2026-10-23, sha256
  `6e9532a978ae5d498722eb95f1a13332f24d1eb09c1791f56fd9aa3eb310d697` (322643 B), `cmp` equal to the
  snapshot; the unversioned URL returns the same bytes. Located quote (§1, printed page 2): "Each
  submitted model is evaluated on a (fixed) test set that is available only to the organizers."
  (18 words). Admit the row.
- S087, attempt-2 seat ReopenS087 (`.ufo/waves/round-30/wA/ReopenS087.md`, authorship re-derived):
  tarball sha512 unchanged; used-by changed (below).

Change log (all in `bb681566`, attempt 2; re-read by seat RerunCensus, census exit 0 at base and
`bb681566`): S087 `used-by` `corpus/knowledge/mte-report-interop.md` → that path plus
`corpus/knowledge/regression-tally-completeness.md` (status, recheck unchanged); S092, S093, S094
added (rows 89 → 92; S092 `queued`, S093 and S094 `mined`). No status, recheck or used-by change in
attempt 3.

Rejects with reasons:

- **Knowledge-entry overreach** (seat ReopenS093S094): `corpus/knowledge/regression-tally-completeness.md:42`
  says the sandbox runs "with a cleared environment"; bwrap.xml:233-235 says `--clearenv` keeps PWD,
  and the argv then sets four variables. The S094 paragraph (`:60-62`) stretches §1 of the paper to
  every control round and to a hash seal defeating allowlists; §1 says neither. Erratum appended to the
  entry (see After measurement).
- **Amendment-4 receipt summary** (seat CriticC1Exploratory, re-checked by the L1 with `grep` on the
  committed receipts): `contract-amendment-4.json` gives CtlS1Normalize `sealed_killed=0/6` and
  CtlS4Sniff `sealed_equiv=5/6`; the receipts read CtlS1Normalize `sealed_killed=6/6 sealed_equiv=5/6`
  (`v4/ctl2/CtlS1Normalize-v4.stdout`, rev `e606538e`) and CtlS4Sniff `sealed_killed=0/6
  sealed_equiv=6/6` (rev `8357d0b9`). Both stay `PASS=false`; the decision does not change. Erratum
  here; the frozen amendment is not edited.
- **Cold-read binding v2 rejected** before wave-C data: a do-nothing transcript met it (below).
- **Binding v3 limit** (seat CtlBindV3): five hand-forged transcript shapes keep 31/32 round-29 pilot
  entries under v3 although no trace command ran (trace name only in another tool's arguments, an
  error result, the name only in a shell comment, a result placed before its call, a reused call id).
  v3 is not amended after data; the stricter conditions run as a separate post-data audit (below) and
  are routed to round 31 as binding v4.

## Controls and redesign before data

- C1 (attempts 1-2): v1-v4 and the exploratory declaration, receipts under
  `.ufo/evidence/round-30/ctl/`, `v4/`, `v4/ctl2/`. Seats CtlS3DenyList and CtlS8TokenBag (and five
  other attempt-2 seats) died with the attempt-2 orchestrator without a report; recorded dead with their
  last transcript events in `.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt`; none resent.
- Cold-read binding (attempt 3, L1-built controls on the round-29 pilot assembly, 32 entries;
  `.ufo/evidence/round-30/attempt3/bind-controls.txt`, builder `make-bind-controls.py`):

  | control | v2 kept | v3 kept |
  |---|---|---|
  | real round-29 transcripts | 32 | 31 (Read12B named its traces in lower case) |
  | do-nothing (prompt + one assistant `COLDREAD` line) | **32** | 0 |
  | prompt only | 0 | 0 |
  | trace names in assistant prose | 32 | 0 |
  | tool call naming the traces, no result | 32 | 0 |
  | hand-forged call + result | 32 | 30 |

  v2 was met by the do-nothing control, so attempt 3 froze v3 (`bind-select-v3.py`, landed `9207f226`
  with the receipts, before wave C was dispatched at 07:13Z): each seat's traces must be named in an
  assistant tool call that names `trace-inputs.py` and has a tool result. The hand-forged shape is the
  stated residual limit (it needs a forged host transcript).

## After measurement

- Wave C (attempt 3; 38 seats, policy v1, dispatched 07:13Z after slot grant, all returned by about
  07:52Z, none dead): 22 cold readers (31 drifted sections, two groupings A and B; group B's last seat
  wraps to sections 1-3), 16 attack, no-harm and frontier seats. 22 cold-read reports, 63 section
  entries assembled, no report rejected, no failing read (35 gap-minor, 22 verified-record, 6
  executed-ok).
- Binding v3 (frozen at `9207f226`): 63/63 kept (`coldread/bind-receipt-wC.json`). Post-data audit
  (`coldread/audit-bound-wC.py`, supporting only): 211/211 matched traces have a `bash` call naming
  `trace-inputs.py --out …<trace>` with a later non-error result, and every trace file's `rev` is
  `bb681566` (`coldread/audit-bound-wC.out`).
- Ledger 393 → 456 entries as an append (`coldread/append-receipt-wC.json`: prefix equal as data, other
  keys unchanged), landed `4df5107f`.
- Calibration no-harm monitor `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV`:
  base `9ed6db84` `covered=64/64 restraint=8 box3_mismatch=0` → content revision `bb681566` 33/64,
  restraint 6, box3_mismatch 1 → `4df5107f` `covered=64/64 restraint=8 box3_mismatch=0`, exit 0
  (`.ufo/evidence/round-30/head/c1monitor-at-4df5107f.stdout`); re-measured at the lane head at filing.
- C1 (exploratory): named non-author judge, seat JudgeC1 (reviewer, `.ufo/waves/round-30/wC/JudgeC1.md`):
  **`JUDGE C1: unprovable-but-better`**. Reasons on record: at `bb681566` the pristine selftest is
  106/106; dropping `"$st_citecheck"` from the tally loop now prints `REGRESSION: SETUP (case-tally
  mismatch: cases=9 counted=8)` exit 2, where base printed `PASS (cases=9 passed=8)` exit 0, and the
  mutant's selftest fails (98/106); the guard is unreachable on complete tallies; a sum-preserving
  miscount (duplicate one operand, drop another) still passes at run time and is caught only by the
  selftest. Supporting, not verdict: v4 receipt reproduced byte-identical by RerunC1Head
  (`C1_R30_PASS=true` at `bb681566`); CriticC1Exploratory: declaration predates the content revision,
  the five extra selftest cases were added before any judgment, CtlS2SymEval is an alternative semantic
  implementation the behavioral predicate cannot tell from execution. Limits: MutateHead, 18 mutants,
  7 killed, 3 equivalent survivors, 8 real survivors (routed below).
- No-harm, operability: full nine-leg `--regression` at `bb681566` `REGRESSION: PASS (cases=9 passed=9 …)`,
  exit 0 (RegressionReplayHead); every `tools/*.py` selftest has the same exit at base and `bb681566`
  (SelftestsNoHarmHead), and `evidence-disposition.py --selftest` (needs jj; run by the L1 in sandbox
  clones) is 66/66 at both (`attempt3/evidence-disposition-selftest.txt`); runner selftest 97/97 → 106/106.
- No-harm, depth: command D `recorded_cases=9 depth_score=9` at base and head. Census exit 0 at
  attempt-3 start (`attempt3/census-attempt3-start.stdout`) and at the head (report).
- Knowledge entry: errata E1-E4 appended to `corpus/knowledge/regression-tally-completeness.md`
  (ReopenS093S094, ReviewEntry, MutateHead). The entry is an input of no ledger entry (0 of 456), so the
  append drifts no credited section.
- Sibling overlap (ConnectorOverlap): no live sibling holds the tally shape or a read binding; mado's
  frozen round-13/14 harness copies are historical evidence only.

## Mistakes

1. **class:** counter met by a control that skips the claimed work, four times in one round.
   **evidence:** v1 → v2 by the L1's fixed-string self-attack (`contract-amendment-1.json`), v2 → v3 by
   CtlK7Keyed (`ctl/CtlK7Keyed.stdout`, `C1_R30_PASS=true`), v3 → v4 by CtlK8NoRun
   (`v4/K8-on-v3.stdout`), v4 → exploratory by CtlS2SymEval (`v4/ctl2/CtlS2SymEval-v4.stdout`).
   **captured-by:** the pre-freeze control rule (it fired each time, before data). **fix:** a counter for
   "the detector runs the code" must observe execution (a trace or a process record), not only
   verdicts; QUALITY 65 records the class. Shown able to fail: CtlS2SymEval's receipt is a verdict-only
   pass of a non-executing detector.
2. **class:** credit binding met by a do-nothing transcript. **evidence:**
   `attempt3/bind-controls.txt` (v2 keeps 32/32 for transcripts that only say `COLDREAD <seat>:`).
   **captured-by:** the leg lesson (control shapes before data); not applied to the binding in attempt 2.
   **fix:** binding v3 ties every credited trace to an executed tool call; the post-data audit adds tool
   name, `--out` argument, result order and error state. Shown able to fail: v3 keeps 0/32 on the
   do-nothing control and still keeps five forged shapes (CtlBindV3), so v4 is routed.
3. **class:** a summary copied into a frozen record without re-reading the receipts. **evidence:**
   `contract-amendment-4.json` misstates two control rows (Gate above). **captured-by:** none (QUALITY 62
   covers measured revisions, not summary values). **fix:** summaries of receipts are generated by a
   command over the committed receipts and pasted with the command. Shown able to fail: `grep -h
   '^C1_R30:' v4/ctl2/CtlS1Normalize-v4.stdout` prints `sealed_killed=6/6`, not 0/6.
4. **class:** a wave item overlapping a dead seat's task. **evidence:** wave C (attempt 3) carries
   ConnectorOverlap, RegressionReplayHead and SelftestsNoHarmHead, adapted from attempt 2's unspawned
   wave-B spec; attempt-2 wave-A seats ConnectorOverlap, RegressionReplay and SelftestsNoHarm died
   without reports (`attempt3/attempt2-dead-seats.txt`). The replays measure a different object (the
   landed `bb681566`, not `f09d3425` + `witness/fix.diff`), and the wave-C connector scan adds the
   binding surface, but the overlap was not checked before dispatch. **captured-by:** the orchestrator
   rule "never resend a dead seat's task" — not checked against the dead-seat list. **fix:** before
   dispatch, list every dead seat of the round and diff its item text against the new spec; an item
   that measures the same object is dropped. Shown able to fail: the dead list holds ConnectorOverlap,
   the wave-C spec holds an item of the same name.
5. **class:** seat containment breach and a self-repaired misroot, both with the clauses in context.
   **evidence:** seat ColdA01 (`.ufo/waves/round-30/wC/ColdA01.md`, Errata paragraph) killed two bash
   selftest processes of another seat's `/tmp/tameshi-r4-2-regression.*` workdir with a broad
   `pgrep`/kill, and its first report write landed at the fleet root
   (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-30/`); the seat moved the file to the lane and removed
   the fleet path (the L1's sweep at 07:33Z: path absent; `git -C /home/vgpnk/Projects/shokunin status
   --porcelain` shows no tameshi file). Readers sharing the scratch name pattern `tameshi-r4-2-regression.*`
   (the runner's default workdir) cannot tell their trees apart by name. **captured-by:** the wave context
   (`spec-wC.json` `context`: "Never kill a process you did not start: before any kill, check that
   /proc/<pid>/cwd is inside your own scratch dir"; absolute report path rule) — stated, not enforced.
   **fix:** the cold-read recipe passes `--workdir` under the seat's own scratch for every `--regression`
   run, so a seat's processes carry its name in their cwd; the operator-owned runtime kill-on-deadline
   stays routed (round-29 item 5(c)). Shown able to fail: ColdA01's disclosure names a sibling workdir
   under the shared default pattern.

## Routed defects of round-29-verifier-spotcheck.md

Per seat ReviewRoutedR29 (`.ufo/waves/round-30/wC/ReviewRoutedR29.md`), re-checked by the L1:

1. Unscored shortcut class / hold path → resolved: `contract.json` `hold_rule`, QUALITY 58; label- and
   key-shaped controls scored (CtlK5Labels, CtlK7Keyed, K9) before data.
2. Syntactic binding → resolved and strengthened: binding v3 + per-seat transcript path, size, sha256 and
   session id in the ledger `binding` field (QUALITY 60); its limit is Mistake 2.
3. Assembler/binding shape → resolved: verdicts not compared, labels normalised, pilot run before the
   freeze (`attempt3/bind-controls.txt`); the ten round-29 exclusions are not re-credited.
4. Control-before-data ordering → resolved for attempt 3: the binding controls landed in `9207f226`
   before the wave-C dispatch record `a2fa6c92`; the two attempt-2 controls without reports are recorded
   dead (`attempt2-dead-seats.txt`).
5. Containment → wave contexts carry the absolute-path and never-kill clauses (`spec-wC.json`
   `context`); 5(c) is operator-owned.
6. Receipt gaps → erratum in the round-30 report: the round-29 report's C2 `quote_located=1` is not in a
   committed receipt (`c2-at-E.stdout` reads `quote_located=0`), and its "measured commit" column should
   name `bc2058a4`, `7a45f7b9` and `9bb699ad`.
7. Carried items → S092 (`bb681566`), runner guard and selftest harness (`bb681566`),
   `r29-mistake1-ordering.txt` (`bb681566`).

## Routed to round 31

- Runner selftest gaps found by seat MutateHead (`.ufo/waves/round-30/wC/MutateHead.md`): a status-4
  arm counted as PASS survives (T08); `tally_line` survives an `&&`→`||` swap and a dropped first-line
  comparison (N03, H03, H04); the final leg's non-zero statuses are never exercised (H05); dropping the
  mixed vector or short-circuiting the guard stress survives (N01, N02). The runner is an input of
  222 ledger entries, so the fix opens round 31's content revision.
- Binding v4 (Mistake 2): the post-data audit's conditions become the binding.
- QUALITY imprecisions (seat ReviewQualityR30 F1-F4) and the stale `Next unused id: S092.` line in
  SOURCES (seat RerunCensus): input files, corrected in round 31's content revision.
