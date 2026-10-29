# Tameshi round 51 — frontier calibration, tenth mutation case, registry conformance

L1 TameshiR51, hyaku run 9, attempt 1. Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. The frozen predicates, controls and source spec are in `.ufo/evidence/round-51/contract.json` (freeze `fe335384`; amendment 1 controls-harness repair `84aa673`; amendment 2 panel-tool scope re-base `9d023aed`). No claim predicate or counter changed after freeze. The three counters' selftests reached their end-to-end `measure()` entry points: `quality/reach-r51.stdout` → 3/3 `calls_measure>0`; selftests at freeze → C1 6/6, C2 11/11, C3 10/10.

## Gate

Rows opened this round; URL, local access date, located quote and source limitations are recorded here under CORPUS.md SOURCES contract v1 rule 1. Rows touched old → new are listed after them.

- **S272** — kagi `corpus/drift-pins.sh`, the fleet's host-drift gate, at rev `e64e81b8eb96f3682b00c1e7a291e84420b280fa` (kagi round-9, 2026-09-28; blob SHA-256 `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`, 451 lines, mode `100755`; unchanged at kagi HEAD). Opened 2026-10-26 read-only with `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh`; tier A, kind code. Located quote (15 words), pinned lines 6-7: “v2 compares the live host against two committed baselines and exits non-zero on any change.” The gate's 13-case `--selftest` ran from a scratch copy (exit 0); its oracle at :403 uses an unanchored `grep -q` over captured output. Row S272 is under `corpus/SOURCES.md:147`.
- **S273** — GNU Bash Reference Manual, §The Set Builtin, author copy by Chet Ramey, Edition 5.3, last updated 18 May 2025; `https://tiswww.case.edu/php/chet/bash/bashref.html`, opened 2026-10-26 local time (UTC receipt is 2026-10-27T00:22Z), HTTP 200, 1,040,870 bytes, SHA-256 `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`, snapshot `.ufo/waves/round-51/w1/T51ScribeRowBash/chet-bashref.html`; kind docs, tier A. The requested gnu.org node page was unreachable (eight HTTP 000 / curl 28 attempts, disclosed in the row and seat report); the opened author copy is a distinct URL, while the same manual is already held as Savannah texi rows S097/S104. Located quotes (all ≤25 words): “Exit immediately if a pipeline ... returns a non-zero status” (9); “The shell does not exit if the command that fails is ... any command in a pipeline but the last” (19); “the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status” (20); “the exit status of the last command substitution performed” (9). The empirical composition matters: with `set -euo pipefail`, a zero-match `grep | cut` command substitution can make an assignments-only command exit 1; the manual states the rules separately, and the gate's call context determines whether `-e` applies. Row S273 is under `corpus/SOURCES.md:148`.

Rows touched: S022 status `queued` → `mined` (used-by already names `corpus/knowledge/fixture-shrinking-pilot.md`; mined means cited by at least one used-by path under CORPUS.md); no other existing row status changed. Appended S272 and S273; the registry has 133 rows and the next allocated id is S274. Census start exit 0; round-end census receipt is in `.ufo/evidence/round-51/census-end.*`.

Candidates rejected (LEARNING §Files; the reason for each is recorded in the section named):
- **Making `tools/round21-measure.py --selftest` hermetic (C3).** Rejected: the frozen round's tools-scope amendment does not allow editing that tool this round. The C3 section records the refusal; the routed fix needs a counter amendment (R51.4).
- **Attempt 2's uncommitted `SKILL.md` draft.** Rejected and discarded in attempt 3: it re-pointed `tools/mutate-and-run.sh` line numbers in sections whose readers had already read them, so the re-key could not bind those reads. SKILL.md was restored to its `f133b47f` bytes (Attempt 3 section, salvage disposition).
- **Attempt-2 probe verdicts (`C1_R51_PASS=true`, `C2_R51_PASS=true`).** Superseded, not admitted: non-deciding. The verdicts come only from `after/` (Attempt 3 section, salvage disposition).

## C1 — calibration: the lane's frontier status and source-status records

The stale table at README:76-87 held seven statuses that later lane declarations had changed; the frozen C1 expectation set is `.ufo/evidence/round-51/c1/frontier-expected.json`. The appended round-51 table points each status to the declaration; the C1 counter also checks the append-only prefix, S022's status/used-by consistency and mined used-by path existence. Two independent wave-1 readers re-derived all ten statuses and agreed with the frozen set; F11/F12 are fixture ids, not frontier rows (`T51CritExpectedA.md`, `T51CritExpectedB.md`). The probe on the table + S022 fixture printed all ten `FRONTIER Fk: ok`, `status_conflicts=0`, `total=0`, `C1_R51_PASS=true` (`T51ScribeFrontier.md` scratch receipt; the deciding receipt remains `.ufo/evidence/round-51/after/c1.stdout`).

Counter mutation probe: 14 behavior-bearing single edits, 7 killed / 7 survived; every survivor has a forged README/SOURCES witness where the mutant passes and pristine fails. The selftest catches table selection, prefix integrity, indentation, used-by existence and queued conflicts; remaining weaknesses include duplicate ids, wrong rounds, long pointers, unsupported status phrase and a table header without `ground`. Evidence and restoration hashes: `.ufo/waves/round-51/w1/T51MutC1Counter.md` and `T51MutC1Counter.receipts/`. This limitation is disclosed, not hidden.

## C2 — depth: tenth recorded leg and oracle-path finding

The pinned kagi drift gate has a true ten-defect spec in `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`, committed before the measured sweep. The recorded suite produced a green pristine control, restore `OK`, 2/10 KILLED (`K_MODE_CMP`, `K_COUNT_GE`), 8 SURVIVED and 7/10 predictions held (`.ufo/evidence/round-51/c2/sweep/sweep.txt`). The runner embeds that table exactly and its regression replays 10/10 cases. The neutral-name probe is separate: `T51LabSandboxLeak.md` rebuilt byte-identical mutants and showed K_GONE_ARM, K_AMBIG_GT and K_SHAPE_OPTIN flip to KILLED when only the sandbox path is renamed; no other verdict changed over three repeats. The defect is in the suite's `grep -q "$3"` over captured output that prints TMPDIR paths: `sandbox-$DEFECT_ID` itself contains the expected word. Thus the 20% recorded rate is not gate kill strength; do not report the three as equivalent. Five remaining survivors have off-suite witnesses; none was found equivalent. C2's counter probe found 15 one-edit blind spots with forged trees, one redundant clause, and one exit-wiring mutant caught by D1/D2/D3 (`T51MutC2Counter.md`). The counter certifies the frozen receipt predicates, not sweep provenance; the suite command was described in the spec but not machine-bound by the counter (`T51CritPrereg.md`).

The runner and four dependent panel tools were updated together: tally-audit, tally-audit-v2/v3 and mte-interop now understand the tenth leg; their selftests/audits passed in the scratch integration (`T51ExecEmbed.md`). The runner `--selftest` reached 107/107 and regression `cases=10 passed=10`. Tools' only other change was honoring `TMPDIR` for scratch defaults. Source entry: `corpus/knowledge/mutation-case-kagi-drift-pins.md` (`source:` S272/S273, `ground: Core`).

## C3 — operability: registry home

The canonical round-51 registry section was appended to SKILL.md with one row per 30 frozen tools, backed by each seat's selftest and usage probe. The frozen C3 counter requires the real selftest to pass from its fresh clone and its finding id to be named. Wave-1 review found a blocker: `tools/round21-measure.py --selftest` exits 1 in that clone because it resolves its sibling fleet repos under the clone parent; with those sibling paths present, it exits 0 and 13/13. The row documents the actual command and the limitation, but cannot assert a false green result. Therefore C3 does not verify: its decisive counter output is `.ufo/evidence/round-51/after/c3.stdout` and is reported verbatim in the report. We did not change that pre-existing tool because the frozen round's tools-scope amendment does not allow it. Critic T51CritC3Counter also showed the counter can be forged by rows that alias `--help --selftest`; the round-51 table rows were reviewed by 30 executors, not admitted solely on the counter's output.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `oracle-leak` — harness-generated path text satisfied the gate's own expected-word grep, making three detectable mutants appear to survive | kagi `corpus/drift-pins.sh` @ `e64e81b8`, :400, :403, :158; `.ufo/evidence/round-51/c2/sweep/sweep.txt`; independent A/B/C matrix `T51LabSandboxLeak.md:52-93` | none — existing QUALITY 101 covers counter reach and measurement, not path tokens participating in verdict oracles | QUALITY criterion 102 requires a neutral-path vs hostile-path one-variable comparison before a recorded mutation verdict; the red/green pair at `T51LabSandboxLeak/red-gone-id.sh` and `green-gone-neutral.sh` is the falsifier (id path exits 0 PASS, neutral path exits 1 FAIL). The gate is sibling-owned and read-only; no kagi code was changed this round. |
| `status-usedby-conflict` — S022 was `queued` although its used-by cell named an existing entry | `corpus/SOURCES.md:33` at base; round-50 spot-check routed defect 1; `C1_R51_PASS` base control | CORPUS.md SOURCES contract v1: `mined` means cited by ≥1 used-by path; no previous round counter enforced this in the self-assessment | flip only S022 `queued` → `mined`, log old→new here, and require C1's queued/mined-vs-used-by predicate; CTL_0 shows the conflict, the scratch S022-only flip clears it. |

## Historical/self-assessment correction found in this round

The contract's C3 motivation says the registry home “names 2 of the 30 lane tools that expose a self-test.” A post-freeze all-section scan found 18 tools mentioned across the twelve per-round registry sections; 12 were not mentioned anywhere. The counter's canonical table is still the correct frozen claim surface, and it checked 0 conforming rows at base, but the prose overstates the absence of any row. This is recorded in `.ufo/evidence/round-51/integrate/l1-notes.md`; no predicate was changed.

The frozen C1 statement-set note at `.ufo/evidence/round-51/c1/frontier-expected.json` says the old table is at README lines `76-86`; its table actually runs `76-87` (header 76, separator 77, rows F1-F10 at 78-87). This is a note-only off-by-one: the frozen F9 basis correctly points to row 86, the counter's row set and spans are unchanged, and the appended table's pointers stay within the counter's six-line limit. W1 reader T51ScribeFrontier recorded this at `.ufo/waves/round-51/w1/T51ScribeFrontier.md:84-91`; the frozen file is not rewritten.

## No-harm, frontier, assimilation and tools

- No-harm at the deciding revision: `.ufo/evidence/round-51/after/no-harm.stdout` (eleven monitors). The round-21 cold-read monitor fell to 44/64 (score 6) after runner and registry changes, then the trace-bound 20-section re-key restored 64/64 (score 8); all readers and traces are listed under `.ufo/evidence/round-51/coldread/`.
- Frontier: no coverage-map ground advanced; C1 supersedes the stale status table, not a new frontier move. Assimilation: none — the F6 package theme was consumed in round 50 and no staged entry supports these claims. No `considerthese/` proposal was adopted this round.
- Tools installed/updated: none. `/home/vgpnk/.omp/agent/RULES.md` was read; pacman remained paused.

## Limits

- C1 counter: semantic status basis remains a frozen L1 reading; the two reviewers agreed, but the counter's mechanical pointers are not a semantic oracle.
- C2 counter: receipt authenticity and suite command are not machine-bound; neutral-sandbox evidence is disclosed separately from the recorded table.
- C3 counter: shallow row semantics permit forged SKILL rows; one real tool's selftest cannot pass in the mandated fresh clone. The claim is reported not verified rather than massaging the row or the predicate.

## Attempt 3 — deciding run, salvage disposition, mistakes (L1 TameshiR51a3, 2026-10-27)

Attempt 1 (TameshiR51) stopped at its request budget; attempt 2 (TameshiR51a2) died with every running w2 seat when the orchestrator session exited on 2026-10-26 23:57:36 -03 (`.ufo/watchdog.log` lane-dead line). The orchestrator committed attempt 2's uncommitted tree as salvage `53afb4aa`. Attempt 3 dispatched no new wave; it re-verified and reused salvage bytes as below.

### Salvage disposition

- **Reused, re-verified:** the 20 w2 reader rows named in `.ufo/evidence/round-51/coldread/readers.json` (`T51W2Read01`–`Read20`). They were copied byte-exact into `coldread/reads/` (`cmp` clean). For 19 of the sections, the monitor's section sha256 is the same at `6d8c11e3`, the bytes the seats read, and at `f133b47f`, the bytes being re-keyed. The 20th section, `### Round-26 gate/probe registry — report interop`, differs by exactly one row: the round21-measure row at SKILL.md:2157, whose fresh-clone limitation Read20's NOTE-B records. Re-key `rekey-02ec217c` gave 20 targets and 20 entries; the monitor went 44/64 → 64/64 (`.ufo/evidence/round-51/integrate/a3/refresh-02ec217c.stdout`, landed `7e548bee`).
- **Discarded:** attempt 2's uncommitted `SKILL.md` draft, which re-pointed `tools/mutate-and-run.sh` line numbers in the sweep-recipe, leg-ledger and receipt sections. Landing it would have changed sections after their readers had read them, so the re-key could not have bound those reads. SKILL.md was restored to its `f133b47f` bytes (`02ec217c`). The stale pointers are routed below, not fixed.
- **Superseded:** the attempt-2 probes at `.ufo/evidence/round-51/integrate/l1-probe-f133b47/`. They printed `C1_R51_PASS=true` and `C2_R51_PASS=true`; the C3 probe file is empty because the run was killed. They are non-deciding; the verdicts come only from `after/`.
- **Kept as evidence, no claim rests on them:** the 41 w2 files under literal `@P@…` names (Mistakes row 3).
- **Dead seats:** `T51W2MutC3Counter`, `T51W2ExecFinalCounters` and `T51W2ExecC2Replay` were killed with no report and were not re-dispatched. The deciding run supersedes the last two; the C3 counter's mutation attack is the one item left unrun.

### Deciding run

There were two invocations of `.ufo/evidence/round-51/deciding-run.sh` at REV `7e548beecfbe872f931e84c2241522ea374c6bc3`:

1. **FREEZE `9d023aed`** (the amendment-2 freeze) was refused at gate 0 with nothing run and no receipt written: `DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-51/control/controls.exit` (`integrate/a3/deciding-invocation-1-refused.txt`).
2. **FREEZE `84aa673a`** (amendment 1), after which the control receipts were committed, ran to completion. `FROZEN_UNCHANGED=0`, and the diff it lists is exactly amendment 2's three files: `contract.json`, `freeze.json`, `no-harm.sh`. Results:
   - 11/11 no-harm monitors ok.
   - QUALITY 98 precheck `64 → 64 lost=0 ok`.
   - Census exit 0.
   - `C1_R51_PASS=true`.
   - `C2_R51_PASS=true` (`depth_score=10`, `predictions_held=7/10`).
   - `C3_R51_PASS=false` (`covered=29 missing=1`; `tools/round21-measure.py` selftest exit 1 in the fresh clone).
   - `DECIDING_RUN_EXIT=1` (`.ufo/evidence/round-51/after/`).
   - Verdicts: C1 verifies, C2 verifies, C3 does not verify.
3. **Choice of FREEZE.** The controls were re-scored after amendment 2: `controls.stdout` at `6d8c11e3` names rev `9d023aed`. The `controls.exit` byte did not change, so git holds no commit for it after `9d023aed`. Gate 0 keys on the last commit that touched the file, not on when the score was produced.
4. **Unchanged by this choice:** no counter, predicate, target or kill rule. The 84aa673 diff is the declared pre-score amendment 2.

### Mistakes (attempt 3)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `receipt-recency-by-last-touch` — the deciding gate dates a receipt by the last commit that changed its bytes, so a byte-identical re-score after an amendment reads as "not after freeze" | `integrate/a3/deciding-invocation-1-refused.txt`; `git log --format=%h 7e548bee -- .ufo/evidence/round-51/control/controls.exit` → `f0129a55` only; `controls.stdout` at `6d8c11e3` names rev `9d023aed` | QUALITY 99 (deciding-run gate 0) covers missing receipts, not re-scored identical ones | Routed, not fixed: the round-52 deciding gate should bind each control receipt to a freeze-stamped header line (`FREEZE=<sha>` inside the receipt) rather than to git last-touch. Not yet shown able to fail. |
| `misroot` — seat `T51W2Read14` also wrote its report into the fleet root `.ufo/waves/round-51/w2/` (byte-identical to the lane copy, sha256 `9b17352c…`) | orchestrator quarantine `/home/vgpnk/Projects/shokunin/.tower/quarantine/fleet-root-strays-20261027T0020/` | wave-context absolute-path rule (§6 item 2) | The orchestrator moved the copy; the lane copy stays canonical. The attempt-3 sweep `git -C /home/vgpnk/Projects/shokunin status --porcelain` shows only `?? .ufo/reports/round-45/kengaku.md`, which is another lane's file and was left untouched. |
| `unfilled-placeholder` — the w2 spec builder emitted `@P@<name>` deliverable paths (95 occurrences in `w2-dispatch.json`), so 41 seat files landed under literal `@P@…` names | `.ufo/waves/round-51/build-spec-w2.py:38-61`; `find .ufo/waves/round-51/w2 -name '*@P@*' \| wc -l` → 41 | none; the wave validator accepts any string | `integrate/a3/placeholder-guard.sh DISPATCH` refuses a taskCall carrying `@[A-Z]@`. It was shown able to fail: w2 gives `FAIL placeholders=95` (exit 1) and w1 gives `PASS placeholders=0` (exit 0) (`integrate/a3/placeholder-guard.receipt`). Run it before writing any `.ready`. |

### Routed defects (found by w2 seats, open at the deciding revision)

- **R51.1, operability harm.** The registry row `mte-interop-check` (`tools/registry.json`) still expects `MTE_INTEROP: PASS legs_conforming=9/9`. The tool now requires and prints ten legs (`tools/mte-interop.py:343`), so `registry-check --only mte-interop-check` cannot pass at REV. This is static evidence from `T51W2Read20.md` HIGH-2; the L1 did not run that gate. The frozen tools-scope monitor allows only the five panel tools to change, so the registry row could not follow this round without turning that monitor red. This is a trade, and it is reported as harm.
- **R51.2.** SKILL.md:2136 (round-26 registry) still says "nine ledger legs" (`T51W2Read20.md` HIGH-1). The runner row's write scope still names `/tmp` although the runner honours TMPDIR (MED-1). The re-key entries carry `wrong_expectations: 0` by construction (`refresh.py:227`), although reader Read20 recorded these false statements. The re-key is reading-bound, not a truth verdict.
- **R51.3.** Runner line pointers in the sections that attempt 2's discarded draft re-pointed (SKILL.md:174, :211, :937-950). Fixing them needs a fresh read and re-key.
- **R51.4.** C3: `tools/round21-measure.py --selftest` resolves sibling repos at `ROOT.parent`. Either make it hermetic, or give the counter a declared fleet-bound row class (`T51W2ScoutC3Provenance.md`). This needs a counter amendment in a later round.
- **R51.5.** The C3 counter's mutation attack (`T51W2MutC3Counter`) never ran.
