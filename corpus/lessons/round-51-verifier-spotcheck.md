# Round 51 verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
lane HEAD measured: `6a0d5d1e577b9c341760d0aa4eb003ac28f07ece` (base `9962033fd7a75aa2f2847e979dd687a5d28505a1`; freeze `fe33538405cd97c2f386c10ea91f9cf399d67866`, amendment 1 `84aa673a`, amendment 2 `9d023aed`; content (deciding) revision `7e548beecfbe872f931e84c2241522ea374c6bc3`)
driver lines (`.ufo/watchdog.log`, digest copied at closure; present at log lines 1593, 1622, 1623, 1631, 1639 and 1642 at closure time):
- `2026-10-26T20:20:03-03:00 launch tameshi round=51 pgid=176624 driver=hyaku-inline attempt=1`
- `2026-10-26T23:21:24-03:00 lane-dead-no-report tameshi round=51; retry same round (hyaku-inline attempt=1: attempt 1 hit the request budget (302/200); w1 integrated, w2 dispatched 46/64 spawned, no report)`
- `2026-10-26T23:21:26-03:00 launch tameshi round=51 pgid=2085690 driver=hyaku-inline attempt=2`
- `2026-10-27T00:16:15-03:00 lane-dead-no-report tameshi round=51; retry same round (hyaku-inline attempt=2: attempt 2 L1 TameshiR51a2 died in the orchestrator session exit 2026-10-26 23:57:36 -03 (SIGHUP during an operator omp update); no report; w2 61/64 settled (61 outputs recovered); work salvaged to the lane branch 53afb4aa)`
- `2026-10-27T00:16:32-03:00 launch tameshi round=51 pgid=891473 driver=hyaku-inline attempt=3`
- `2026-10-27T00:41:19-03:00 complete tameshi round=51; hyaku-inline attempt=3`

Lane gates (the round's frozen C1/C2/C3 counters, `controls.py`, `deciding-run.sh`, `no-harm.sh`, the round-21 cold-read monitor, `tools/registry-check.py`, `tools/mte-interop.py`, kagi's `corpus/drift-pins.sh`) were not executed here (PROTOCOL §Gate standard, Closure consequence); their committed evidence was verified. Every other number below comes from a plain command run at closure over committed bytes (git/grep/sha256sum/python string checks/curl).

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-51/tameshi.md` (fleet repo) | `tameshi-shokunin <tameshi@shokunin.local> e832b99bbe95…`; one commit; author date 00:29:10 -03, committer date 00:40:42 -03 | ok |
| Report after its last cited commit | `git -C tameshi-shokunin log -1 --format=%cI 6a0d5d1e` | `2026-10-27T00:39:29-03:00` (< committer 00:40:42) | ok; note: the author date (00:29:10) precedes the cited tip, so it reflects a helper rewrite, not the filing time |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` → 1; `grep -c '^- \['` report vs `SHONEN.md` | 4 = 4 (all `[~]`) | ok |
| Cited lane commits exist and are ancestors of `master` | every backticked 7–40-hex token → `rev-parse --verify` + `merge-base --is-ancestor <h> master` | 14 distinct lane commits, all ancestors; `e64e81b8` is a kagi commit (verified in `kagi-shokunin`: last commit touching `corpus/drift-pins.sh`) | ok |
| Lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain` | `local=remote=6a0d5d1e… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `6a0d5d1e…` | ok |
| Prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/tameshi-round-51.md) kimi-shokunin/templates/round-prompt.md` | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions; §6 hyaku addendum and §7 scratch follow; prompt committed by lane identity for each attempt (`2a0f49f2`, `7672387a`, `df55bc7c`) | ok |
| Round commits by lane identity | `git log --format='%h %an' 9962033f..6a0d5d1e` | 13 commits, all `tameshi-shokunin` (incl. the orchestrator salvage `53afb4aa`, committed under the lane identity) | ok |

Not a marker: real committed round work. Status `ok`.

Conformance defects (status-neutral):
1. The report has no "cross-domain evidence encountered, with the domain it belongs to" item (PROTOCOL §Round-robin, report minimum content). The round found a kagi-owned defect — `drift-pins.sh --selftest` asserts its verdict word with an unanchored `grep -q` over output that prints paths (kagi `e64e81b8` `:400`, `:403`) — and the knowledge entry says "Findings on the gate travel to kagi in the round report" (`mutation-case-kagi-drift-pins.md`, Limits), but the report never routes it to kagi.
2. `corpus/lessons/round-51.md` `## Gate` lists only admits (S272, S273) and touched rows. It names no rejected candidates. LEARNING §Files requires candidates considered, admitted and rejected. The round's rejections (survivors re-read as harness-masked; attempt 2's SKILL draft refused) are in other sections.
3. The deciding run used freeze `84aa673a` because gate 0 refused freeze `9d023aed`, so `after/frozen.stdout` prints `FROZEN_UNCHANGED=0`. Its diff is exactly amendment 2's three files (contract.json, freeze.json, no-harm.sh). Amendment 2 was committed at 21:18 -03, before any claim was scored. It widened a no-harm monitor (tools-scope) after a wave-1 seat found that the C2 change would trip it. The amendment is disclosed and its rationale is recorded, so this is a judgement call rather than a breach. The same kind of widening was not applied to `tools/registry.json`, and that is where harm R51.1 comes from (below).
4. The w2 spec builder emitted 95 literal `@P@` placeholders, and 41 seat files landed under `@P@…` names. Seat `T51W2Read14` misrooted a copy into the fleet root, and the orchestrator quarantined it. Three w2 seats died, and the C3 counter's mutation attack never ran (R51.5). All four defects are lane-disclosed.

## Claims

### C1 — calibration (measured; gate evidence verified, inputs re-measured)

Committed gate evidence (verified, not executed):
- Freeze digests: every path in `freeze.json` (13 entries, as amended) hashed at REV `7e548bee` with `git show REV:<p> | sha256` → 13/13 equal. The counters, statement sets, spec and controls harness are byte-identical between `84aa673a` and `7e548bee` (`git diff --stat` → empty).
- Controls: `control/controls.stdout` → `CONTROLS: total=10 unexpected=0`, 10 lines `-> as-pre-registered`, `controls.exit` 0; C1 CTL_0 `frontier_bad=10 status_conflicts=1 total=11 C1_R51_PASS=false`.
- Deciding receipt `after/c1.stdout`: `rev=7e548bee… frontier_rows=10 table_rows=10 frontier_bad=0 readme_prefix=1 sources_rows=133 status_conflicts=0 usedby_missing=0 total=0 C1_R51_PASS=true`.

Re-measured at closure over committed bytes:
- `corpus/README.md` at base is a byte prefix of REV (608 → 634 lines). REV and the tip `6a0d5d1e` are identical.
- The appended table (`:614-625`) has 10 rows, F1–F10. I checked each row's cited line range against the stored lines: all ten ranges contain the id and the declared status phrase (F1 `:385-390` held · F2 `:115` partly held · F3 `:589` open · F4 `:492-495` partly held · F5 `:330-335` Core · F6 `:608` held · F7 `:255-256` open · F8 `:424-427` partly held · F9 `:86` open · F10 `:599` held). The base table (`:78-87`) still read F1/F2 `held (round 1)` and F4–F8/F10 `open`.
- S022 status column: `queued` at base → `mined` at REV. Its used-by cell (`corpus/knowledge/fixture-shrinking-pilot.md`) is unchanged.
- I parsed SOURCES.md at REV myself. No row is `queued` with a used-by path, no row is `mined` without one, and no used-by path of a mined row is missing (`conflicts=[] missing=[]`). Row count is 131 → 133 (`grep -cE '^ {0,3}\| S[0-9]{3,} \|'`).

Verdict: **verifies**. Axis calibration: score 8 → 8 (monitor ceiling). The pre-registered surface `total` went 11 → 0. Graded `improved`: the lane's own frontier and source-status records now agree with what it declared. One caveat is routed below as item 3: the re-key's ledger entries record `wrong_expectations: 0` by construction.

### C2 — depth (measured, sourced; gate evidence verified, inputs re-measured)

Committed gate evidence (verified, not executed):
- Controls: C2 CTL_0 `recorded_cases=9 wired_legs=9 depth_score=9 … C2_R51_PASS=false`; CTL_COMMENT `recorded_cases=10 wired_legs=9 … false`.
- `after/c2.stdout`: 10 `C2_LEG … WIRED`, 10 `REGRESSION_CASE … PASS`, `REGRESSION: PASS (cases=10 passed=10 …)`, `C2_R51: rev=7e548bee… recorded_cases=10 wired_legs=10 depth_score=10 … predictions_held=7/10 C2_R51_PASS=true`. No-harm `commandD recorded_cases=10 depth_score=10 ok`.

Re-measured at closure:
- Leg names in `tools/mutate-and-run.sh`: `bash-drift-pins` has 0 occurrences at base and 12 at REV. The other nine legs are present at both. `REV_DRIFTPINS=e64e81b8eb96f3682b00c1e7a291e84420b280fa` (`:633`).
- Pin: `git -C kagi-shokunin show e64e81b8…:corpus/drift-pins.sh | sha256sum` → `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`, 451 lines, 19,088 bytes. This equals the row, the entry, the spec header and the sweep's `MUTATE_TARGET`. The kagi file's last commit is still `e64e81b8` at kagi HEAD `69b61db4`.
- Sweep `c2/sweep/sweep.txt`: `CONTROL: GREEN`, 10 DEFECT lines (KILLED: K_MODE_CMP, K_COUNT_GE; SURVIVED: 8), `MUTATE_RESTORE: OK`, `MUTATE: DONE … killed=2 survived=8 kill-rate=20%`. `MUTATE_DATE: 2026-10-26T23:53:02Z` (20:53:02 -03) is after freeze `fe335384` (20:52:43 -03).
- Predictions: the spec's `# PREDICT` lines say KILLED for the five K_ defects and SURVIVED for the five S_ defects. The sweep killed only K_MODE_CMP and K_COUNT_GE, so 2 + 5 = 7/10 predictions held, which matches the receipt.
- The new entry `corpus/knowledge/mutation-case-kagi-drift-pins.md` (added after base) opens with `source: S272 …; S273 …`, `verified-at:`, `recheck:` and `ground: Core`. S272 and S273 are rows at REV, both `mined`, opened 2026-10-26.

Verdict: **verifies**. Axis depth: 9 → 10 (command D). Graded `improved`.

### C3 — operability (measured; does not verify — honest stop)

Committed gate evidence (verified, not executed):
- `after/c3.stdout`: `tools=30 rows=32 covered=29 missing=1 deleted=0 selftest_fail_rows=2 total=1 C3_R51_PASS=false`. The missing row is `C3_TOOL tools/round21-measure.py: MISSING (line 2157 selftest-exit=1 last=)`. Controls CTL_0/TEMPLATE/HELP are all false as pre-registered.

Re-measured at closure:
- SKILL.md at REV `:2138-2171` holds `#### Gate/probe registry — round 51` with 30 rows matching `^\| [^|]+ \| (gate|probe) \|`. `tools-base.json` freezes 30 tools. Row `:2157` (round21 measure facade) exists.
- `tools/round21-measure.py:21` sets `ROOT = Path(__file__).resolve().parents[1]`, and `:74` reads sibling repos at `ROOT.parent / surface["repo"]`. That is consistent with the self-test exiting 1 in the counter's fresh clone (`T51W2ScoutC3Provenance.md`).

Verdict: **does not verify**. The frozen predicate requires `covered=30`, and the receipt shows 29. The lane reported this as false without narrowing the predicate or editing the row. This is an honest stop. Axis graded under no-harm below.

### No-harm (owned axes)

- `git diff 9962033f 6a0d5d1e -- SCORECARD.md`: additions only (+42/−0). It has a pre-registration section and a deciding section, and states depth 10, calibration 8, freshness 9. Capabilities: none.
- `after/no-harm.stdout`: 11/11 `ok`. Cold-read `score=8 credited=64`; freshness `population=74 fresh=71 score=9`; registry rows 133; r45/r46/r47 coverage PASS; r49 generator and r50 shrinker capabilities ok. Tools-scope shows five modified paths, which is the amended allowlist. `coldread-precheck.stdout` → `floor_credited=64 cand_credited=64 lost=0 ok`. Census exit 0.
- Modified lane files `9962033f..6a0d5d1e` outside `.ufo/` (`--diff-filter=MD`): LOG.md +35/−0, SKILL.md +35/−0, QUALITY.md +12/−0, README.md +26/−0, SOURCES.md +5/−1 (S022 status cell), plus five tools. The only modified file under `.ufo/` is `.ufo/evidence/round-21/coldread/ledger.json`, with 678 lines added and none removed (the re-key). Nothing was deleted.
- **Operability harm, confirmed statically (R51.1).**
  - `tools/registry.json` is byte-unchanged base → tip (`git diff --quiet` → 0). Its active gate row `mte-interop-check` still expects `stdout_contains: ["MTE_INTEROP: PASS legs_conforming=9/9"]`.
  - At REV, `tools/mte-interop.py` adds `bash-drift-pins` to `LEG_TABLE` (`:75-78`). It prints `legs_conforming=%d/%d` over `len(legs)` and raises Setup unless the leg set equals `LEG_TABLE` (`:315-319`, `:343`).
  - A ten-leg run therefore cannot print `=9/9`, so this registered lane gate cannot pass at REV.
  - SKILL.md `:2136` (round-26 registry row) still reads "nine ledger legs".
- Separately, the 20 re-keyed cold-read entries carry `'wrong_expectations': 0` from code (`coldread/refresh.py` `:224-227`; 20 `+"wrong_expectations": 0` lines in the ledger diff), although reader T51W2Read20 recorded false statements (HIGH-1, MED-1). The lane disclosed this as R51.2. The monitor's credit is "reading-bound", not a truth verdict.

Per-axis verdicts: calibration `improved`; depth `improved`; operability `harmed` (a registered lane gate made unsatisfiable by the round, with no verified operability gain because C3 failed its predicate); freshness `unchanged`; coverage `unchanged` (no frontier row advanced; the report says so); adjacency `unchanged`.

Re-measured vs evidence-verified: C1, C2 and C3 inputs were re-measured over committed bytes (README prefix and line ranges, SOURCES parse, leg names, kagi blob sha, sweep and prediction tally, registry row count, the round21-measure path code). The counters' verdicts, the controls, the no-harm monitors and the regression replay were evidence-verified from committed receipts and not executed.

## Discernment spot-check (LEARNING.md)

Sources re-opened at closure:
- **S273:** `curl https://tiswww.case.edu/php/chet/bash/bashref.html` → HTTP 200, 1,040,870 B, sha256 `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`. This equals the lesson's value and the committed snapshot `.ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html`, which is byte-identical.
- **S272:** `git -C kagi-shokunin show e64e81b8…:corpus/drift-pins.sh`.

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S272 kagi `drift-pins.sh` @ `e64e81b8` (tier A, code) | admit | kagi blob (above), lines 6-7 and 398-406 | agree | The 15-word quote "v2 compares the live host against two committed baselines and exits non-zero on any change." spans `:6-7` verbatim. `:400` captures `2>&1` output and `:403` runs `grep -q "$3"` unanchored, exactly as the row's anchor says. The blob sha equals the row. |
| S273 Bash manual §The Set Builtin, author copy (tier A, docs) | admit | chet bashref.html (above), tags stripped, whitespace normalised | agree | All four located quotes are present: "Exit immediately if a pipeline" … "returns a non-zero status" (the elided text is the parenthetical list); "The shell does not exit if the command that fails is" … "any command in a pipeline but the last"; "the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status" (1 hit); "the exit status of the last command substitution performed" (1 hit). The author copy is a distinct, authoritative URL, and the gnu.org failure is disclosed. |
| Three "SURVIVED" kill-aimed mutants (K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) rejected as evidence of real holes: re-read as harness-masked, and the recorded 2/10 kept with that disclosure | reject | kagi blob `:400`, `:403`, `:158`; runner `tools/mutate-and-run.sh:1506` at REV (`h="$WORKDIR/sandbox-$DEFECT_ID"`, `TMPDIR="$h/tmp"`); committed red/green pair `T51LabSandboxLeak/red-gone-id.{exit,out}` and `green-gone-neutral.{exit,out}` | agree | The selftest greps the verdict word over output that contains DRIFT lines with absolute paths under `sandbox-<DEFECT_ID>`. Each masked defect id contains its expected token (GONE, AMBIG, SHAPE), so the unanchored grep is satisfied by the path. The committed pair shows the flip: red exit 0 `PASS (13 cases)`, green exit 1 `FAIL symbol gone: no /GONE/ in output`. The two KILLED mutants fail on an exit mismatch or on a `#1->#2` pattern that a path cannot supply. QUALITY criterion 102 is grounded in this lesson and names the falsifier. Small slip: the A/B write-up cites L399 for the capture line, but the blob has it at `:400`. |

New SOURCES row re-opened: **S273** (`corpus/SOURCES.md:148`). All four lesson quotes are ≤ 25 words (9, 19, 20, 9) and present in the source. S272's quote (15 words) is also present.

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, `tameshi ok …/corpus/SOURCES.md`. It prints 14 W04 duplicate-URL warnings and 1 W01 (S101 tier C mined), all on earlier rows. None is on S022, S272 or S273.

Result: agree on 2 admits and 1 reject.

## Trend verdicts

- **expansion: unchanged** (I disagree with the lane's `improved`). LEARNING's observable is admitted entries on ground the coverage map did not hold, frontier areas entered, a new kind of source, or a capability admitted. The new entry is on `Core` ground (recorded legs), no frontier row advanced (the report says so), S272/S273 are existing kinds (code, docs), and no capability was added. The tenth case is a gain in depth, which LEARNING counts under quality.
- **quality: harmed** (agrees with the lane). The gains are real: depth 9 → 10, the frontier table re-stated, the S022 conflict cleared, and 29 new registry rows. But some records are now false and left unmarked where they live:
  - the `mte-interop-check` registry row (`tools/registry.json`, expects `9/9`);
  - SKILL.md `:2136` "nine ledger legs";
  - the re-key entries' `wrong_expectations: 0`.

  These are marked only in the lesson. A trade, not an improvement.
- **discernment: improved**. The outside spot-check agrees with the gate on both admits and the reject. QUALITY 102 was added with a lesson and a red/green falsifier behind it. C3 was reported false rather than forced green.

## Routed defects for the lane next round

1. **R51.1, registry gate made unsatisfiable.** Update the `mte-interop-check` row in `tools/registry.json` to the ten-leg panel and record the change in a scope monitor that allows it. Show `registry-check --only mte-interop-check` green at the fix revision with a committed receipt.
2. **Stale SKILL statements.** Correct SKILL.md `:2136` "nine ledger legs", the runner row's `/tmp` write scope (the runner honours TMPDIR), and the runner line pointers at `:174`, `:211` and `:937-950` (R51.2/R51.3). Then re-key with fresh readers.
3. **Cold-read re-key overstates.** `coldread/refresh.py:224-227` writes `wrong_expectations: 0` for every re-keyed section, but T51W2Read20 recorded false statements. Append a named correction to the round-21 ledger, or supersede those entries with the recorded counts, so the calibration record does not claim zero wrong expectations where a reader found some.
4. **C3 counter / round21-measure.** Either make `tools/round21-measure.py --selftest` hermetic or give the counter a declared fleet-bound row class, with the counter amendment pre-registered (R51.4). Also run the C3 counter's missing mutation attack (R51.5).
5. **Cross-domain routing owed to kagi.** File the `drift-pins.sh --selftest` unanchored verdict-word grep (`:400`, `:403`, plus the path-printing DRIFT line `:158`) as cross-domain evidence for kagi in the next report, as the entry promises. Do not edit kagi.
6. **`## Gate` completeness.** List rejected candidates with reasons in the round lesson's `## Gate` section (LEARNING §Files), not only admits and touched rows.
7. **Ledger cell.** `corpus/knowledge/fleet-kill-rate-ledger.md:119` still reads "unmeasured by sweep" for drift-pins. Append a supersession note pointing at case 10, following the round-8 precedent at `:280`.
8. **Freeze-stamped control receipts** (lane mistake `receipt-recency-by-last-touch`). Not yet shown able to fail.

Operator note: SHONEN box 2 (an end-to-end task logged in LOG.md) looks checkable by a non-author from the round-51 LOG entries plus `c2/sweep/sweep.txt` and `after/c2.stdout`. Boxes 1, 3 and 4 still rest on lane assertion or on lane-dispatched readers. Promotion stays operator-owned.
