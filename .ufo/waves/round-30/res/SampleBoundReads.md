**Verdict: qualified support for the sampled bindings, not for completed execution of every credited instruction.** The six sampled entries have real matching command calls and observations in their bound host transcripts. ColdA01/375 and ColdB02/933 nevertheless receive instruction credit after interrupted regression runs. Their disclosed `gap-minor` verdicts are supportable as bounded reads; treating them as completed end-to-end replays is not supported. ColdA04's historical record has separate completed read/selftest receipts and must not be described as a completed regression. The timing explanation also needs narrowing: a 240- or 300-second cutoff does not establish that completion requires more than six minutes.

Seat: SampleBoundReads. Review only; no claim admission or canonical judgment.

Axes: **calibration** (credit and conclusions match the observations), **operability** (invocation versus completion), and **freshness** (the stated revision and input identities).

## Scope and evidence identity

Entry numbers below are one-based positions in `.ufo/evidence/round-30/coldread/assembled-wC-bound.json`, not section numbers. I opened each listed seat report, every receipt listed for the sampled entry, and its actual host transcript from `bind-receipt-wC.json`.

All lane-relative paths below are rooted at `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Let `H` denote this exact read-only host directory:

`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7/TameshiR30A3`

Thus `H/TameshiR30A3.ColdA01.jsonl:155` is a host transcript line, not a receipt or a report assertion. Let `T` denote `.ufo/evidence/round-30/coldread/traces` in the lane.

The following read-only command, run in the lane, returned exit 0 with no output, establishing that the reviewed evidence bytes agree with the requested revision:

```sh
env GIT_OPTIONAL_LOCKS=0 git diff --exit-code 957c5ddb2af61063c8993e8aed1321cb0d54b66a -- .ufo/evidence/round-30/coldread/bind-receipt-wC.json .ufo/evidence/round-30/coldread/assembled-wC-bound.json .ufo/evidence/round-30/coldread/traces .ufo/waves/round-30/wC
```

`sha256sum` over the six absolute host transcript paths returned the following hashes, each identical to its binding receipt's `transcript_sha256`:

| Seat | Observed transcript SHA-256 |
|---|---|
| ColdA01 | `d4645d63c31c936be9f66da290650c31372bca006a8cc2d3756e6425918fcdd5` |
| ColdA02 | `448f312b046da17fc482f3bf60863355f505ce748a8b5b917c5a7ee9f9fcadf0` |
| ColdA04 | `7236da82b98894bf2c2997b2bf129038b15e2834ebc7b1804270f862770f8050` |
| ColdA06 | `af53ef9718fac5b80482be065e001840a39755404442131158daab1b86f26cf7` |
| ColdB02 | `f63241688f8af16d71deff3032d97d008b81a343d6e389e717e4a1c2ceaba582` |
| ColdB07 | `dd6cb1401093d50f537e63a9b71480816feac7c112d59617d4d9aafcd4e731de` |

Every sampled receipt records read revision `bb681566b18211adf8ae9c28df91e17678e3f545`. This is a targeted sample, not an audit of the remaining entries.

## Sample table

“Supported” evaluates the recorded, qualified verdict. It does not turn a timeout into a passing regression.

| Entry | Seat | Bound verdict | Supported / not supported | Reason |
|---|---|---|---|---|
| 2: SKILL 375–404, Restore discipline | ColdA01 | instruction / `gap-minor` | Supported as a partial read; not supported as a completed replay | All four receipt commands occur in the host transcript. The retained regression receipt has child exit 124; its run completed four legs and stopped during the fifth. The report discloses both interrupted attempts. Its broader “operates as stated” and “exceeded the 6-minute bound” wording goes beyond the retained run's observation. |
| 6: SKILL 933–964, Using the ledger | ColdA02 | instruction / `executed-ok` | Supported | After an initial job-limit refusal, a different, real invocation completed all nine legs, emitted the closing PASS receipt and removal message, and has receipt exit 0. The refusal is not being mistaken for the successful invocation. |
| 12: SKILL 1272–1280, Round-10 runbook and embedding record | ColdA04 | record / `gap-minor` | Supported as a historical record; not supported as a completed current replay | Both retained receipts match completed commands: a record read and `--selftest`. A separately attempted regression was killed at 300 seconds and wrote no receipt. The report explicitly distinguishes that missing receipt from the selftest later written under the same intended filename. |
| 16: SKILL 1479–1498, Repeated controls | ColdA06 | instruction / `executed-ok` | Supported | The exact repeat-control invocation ran three identical zero-exit children, the cited-file read completed, and the separate selftest completed. All three receipt commands and matching results occur in the transcript. |
| 36: SKILL 933–964, Using the ledger | ColdB02 | instruction / `gap-minor` | Supported as a partial read; not supported as a completed replay | Its sole receipt is the actual regression invocation, with child exit 124. The host output ends after six PASS legs and the seventh pin; no closing regression receipt or automatic PASS cleanup was observed. The report says exactly that. ColdA02's success cannot supply ColdB02's missing observation. |
| 52: SKILL 1754–1805, Seventh recorded case | ColdB07 | instruction / `executed-ok` | Supported for the reproduced case and named ancillary commands | The case sweep completed with the predicted five kills/five survivors and restore proof. All six listed commands have matching transcript calls/results and receipt exit 0. The report separately discloses that the full nine-leg regression was skipped; the measurement command's inventory is not a substitute regression receipt. |

Bound-entry coordinates: `assembled-wC-bound.json:49-59,187-197,382-392,541-551,1571-1581,2245-2255`.

## Exact command and observation checks

Commands in this section are the exact child commands after the collector's `--`; collector wrappers, literal receipt filenames, and corresponding result records are in the cited host lines. These are historical observations I inspected, not commands I reran.

### Entry 2 — ColdA01

Report: `.ufo/waves/round-30/wC/ColdA01.md:40-64,96`. Receipts: `T/ColdA01-2-1.json:3-16`, `-2.json:3-12`, `-3.json:3-15`, `-4.json:3-12`.

```sh
python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/README.md tools/mutate-and-run.sh
bash -c 'git -C /tmp/ColdA01-4BEV/fleet/tameshi-shokunin status --porcelain -- tools/mutate-and-run.sh; sha256sum tools/mutate-and-run.sh; stat -c "%s %y" tools/mutate-and-run.sh'
timeout 240 bash tools/mutate-and-run.sh --regression --keep
bash -c 'git -C /tmp/ColdA01-4BEV/fleet/tameshi-shokunin show bb681566b18211adf8ae9c28df91e17678e3f545:SCORECARD.md | sed -n 13p'
```

Host call/result pairs: `H/TameshiR30A3.ColdA01.jsonl:60-64,75-78,153-158,159-162`. The file-read command returned `exit=0`. The fingerprint result prints tool SHA `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`, size `106538`, and no dirty-path row. The final pointer read prints the quoted retained-scratch sensitivity text.

Most importantly, host line 155 prints wrapper `exit=0` but only a partial regression tail; host line 158 explicitly prints:

```text
rev bb681566b18211adf8ae9c28df91e17678e3f545 child_exit 124 inputs 1
4
REGRESSION_CASE js-kimi-census: PASS ...
REGRESSION_CASE bash-surface-census: PASS ...
REGRESSION_CASE bash-tsukuroi-census: PASS ...
REGRESSION_CASE bash-mado-verify: PASS ...
```

The ellipses above omit only the repeated band text, not further completed cases. Receipt `ColdA01-2-3.json:15` also says `124`. The wrapper's zero status is not child success. Host line 155 measures `260.39 seconds`, below six minutes; the 240-second child deadline prevented observing completion. The report's disclosure of incompletion is supported; the unconditional completion/time conclusion is not.

### Entry 6 — ColdA02

Report: `.ufo/waves/round-30/wC/ColdA02.md:24-30,64-78`. Receipt: `T/ColdA02-6-1.json:3-12`.

```sh
bash tools/mutate-and-run.sh --regression
```

The first attempted wrapper receives `Background job limit reached (100)` at `H/TameshiR30A3.ColdA02.jsonl:48-50`. The replacement wrapper at host lines 52–54 uses outer `timeout 350` around the collector and actually runs the child above. Host line 54 contains all nine per-leg PASS rows, followed by:

```text
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.PbbIwa (removed on PASS; --keep retains)
Wall time: 339.22 seconds
```

The receipt records child exit 0. This is a real completed-run counterexample to an unconditional assertion that this revision's regression cannot finish within six minutes. It does not establish identical timing under another seat's later load.

### Entry 12 — ColdA04

Report: `.ufo/waves/round-30/wC/ColdA04.md:24-29,50-68`. Receipts: `T/ColdA04-12-1.json:3-15`, `T/ColdA04-12-2.json:3-12`.

```sh
python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" corpus/knowledge/operator-runbook.md tools/mutate-and-run.sh corpus/knowledge/fleet-kill-rate-ledger.md
bash tools/mutate-and-run.sh --selftest
```

Host call/result pairs: `H/TameshiR30A3.ColdA04.jsonl:64-66,90-92`. The read returns `rc=0`, the expected revision, and the three input paths. The selftest result ends:

```text
MUTATE_SELFTEST: 106/106 pass
VERDICT: PASS
Wall time: 17.18 seconds
```

The separate regression child was also really launched:

```sh
bash tools/mutate-and-run.sh --regression
```

Its wrapper at host lines 67–69 puts `timeout 330` outside the collector, but the host tool imposes a 300-second deadline. Host line 80 reports `Command timed out after 300 seconds`, six completed PASS legs and the seventh pin, with `Wall time: 300.16 seconds`. Host line 83 then shows `FileNotFoundError` for the intended `ColdA04-12-2.json`. Only afterward, at host lines 90–92, does the selftest create that receipt. The retained receipt's argv correctly says `--selftest`, not `--regression`; this is not a hidden completed-regression receipt. The 300-second cutoff cannot by itself establish that the full run needs more than 360 seconds.

The actual section is a historical account of the runbook landing and cases 5–6 being embedded (`SKILL.md:1272-1280`), so this interruption does not invalidate its historical-record classification.

### Entry 16 — ColdA06

Report: `.ufo/waves/round-30/wC/ColdA06.md:11-22,56-60,258`. Receipts: `T/ColdA06-16-1.json:3-19`, `-2.json:3-15`, `-3.json:3-12`.

```sh
python3 tools/repeat-control.py --runs 3 --out /tmp/ColdA06-r12-controls-a -- bash -c 'printf pristine'
python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" corpus/knowledge/repeated-control-precondition.md .ufo/evidence/round-12/verification-final.json corpus/SOURCES.md
python3 tools/repeat-control.py --selftest
```

Host call/result pairs: `H/TameshiR30A3.ColdA06.jsonl:55-63`. Host line 57 shows `REPEAT_RUN 1/2/3 exit=0` individually, `REPEAT_COMPARE identical=yes runs=3`, and `REPEAT_CONTROL: controls_match`. Host line 60 shows the cited-file read completed (`TRACE_EXIT=0`), and line 63 ends `SELFTEST: PASS (29 cases)`. All three receipts have child exit 0. The report's finite demonstration follows from these observations; it does not claim all possible suite behavior was exercised.

### Entry 36 — ColdB02

Report: `.ufo/waves/round-30/wC/ColdB02.md:15-21,35`. Receipt: `T/ColdB02-6-1.json:3-14`.

```sh
timeout 320 bash tools/mutate-and-run.sh --regression
```

The literal collector invocation is at `H/TameshiR30A3.ColdB02.jsonl:70-73`. The subsequent log/receipt read at host lines 95–97 shows six completed PASS cases, then `REGRESSION_PIN js-round-gate`, and:

```text
rev: bb681566b18211adf8ae9c28df91e17678e3f545 exit: 124
inputs: ['tools/mutate-and-run.sh']
```

Host line 100 independently displays the same final completed case (`js-claims-check`) and seventh pin. The report explicitly says the closing `REGRESSION:` line and removal-on-PASS path were unobserved. This supports a candid partial-read verdict, not successful completion of the “one command replays every leg” instruction (`SKILL.md:935-950`).

### Entry 52 — ColdB07

Report: `.ufo/waves/round-30/wC/ColdB07.md:76-104,113`. Receipts: all six `T/ColdB07-22-{1,2,3,4,5,6}.json`; argv/revision/exit are at lines 3–16 or earlier in each.

```sh
bash -c 'bash tools/mutate-and-run.sh --target /tmp/ColdB07-R7Sf/round-gate.mjs --defects .ufo/evidence/round-16/round-gate/round-gate.defects.spec --suite "$(cat .ufo/evidence/round-16/round-gate/suite.txt)" --label js-round-gate --workdir /tmp/ColdB07-R7Sf/rgwork'
python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest
python3 .ufo/evidence/round-16/coldread/assemble.py --selftest
python3 .ufo/evidence/round-16/measure.py --selftest
python3 -c "import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]" corpus/knowledge/mutation-case-kumitate-round-gate.md tools/mutate-and-run.sh .ufo/evidence/round-16/round-gate/predictions.json .ufo/evidence/round-16/round-gate/sweep/results.tsv
python3 .ufo/evidence/round-16/measure.py --rev bb681566b18211adf8ae9c28df91e17678e3f545
```

Host call/result pairs are `H/TameshiR30A3.ColdB07.jsonl:92-104,114-117`. The sweep's complete output is also present in the host's process-read result at line 113, not merely in the seat's prose. It includes all ten defect outcomes, identical before/after target hashes, and:

```text
MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
```

Receipt 22-1 records child exit 0. Host lines 98–99 show `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` and `SELFTEST: all checks passed`; line 103 contains the measure selftest's passing cases; line 104 shows the cited-file reader's result. Host line 116 prints `regression_calls: 9`, `recorded_cases: 9`, and `T6=0`. Those inventory fields are not an executed nine-leg regression. The report explicitly makes that distinction. Receipt 22-6 records live-lane Git metadata/object reads at lines 31–48; these are disclosed, not concealed live working-tree content reads.

## Counterexample, limits, and smallest safe correction

**Strongest counterexample:** the same section, `Using the ledger`, has ColdA02's completed nine-leg receipt and ColdB02's interrupted six-leg receipt. Both entries are bound and receive instruction credit. Therefore “bound/credited” cannot mean “this reader completed the replay,” and a second reader's success must not be substituted for the interrupted reader's missing observation.

This is not evidence that the trace commands were invented. It is a limitation of what the credit means. The existing credit predicate accepts instruction `gap-minor` with a positive command count and no blocking/wrong-expectation entries (`.ufo/evidence/round-16/measure.py:178-210`); it does not inspect a trace's child exit. The supplemental audit checks a matching wrapper result and receipt revision, not child success (`.ufo/evidence/round-30/coldread/audit-bound-wC.py:49-67`). Thus a successful collector wrapping exit 124 is consistent with both instruments. I did not run or replace either instrument.

The original seat task, preserved as data in `H/TameshiR30A3.ColdA01.jsonl:8`, also expressly allowed skipping commands needing more than six minutes and required at least one named instruction command. I have not silently replaced that bounded-read assignment with a requirement to run every command. The qualified `gap-minor` records should remain honest records; whether they satisfy the round's no-harm duty belongs to the canonical judge, not this review.

Smallest safe correction:

1. In the integrator's summary, explicitly identify ColdA01/375 and ColdB02/933 as **partial instruction reads, regression completion unobserved**. Identify ColdA04/1272 as a **historical record checked by read/selftest, regression attempt interrupted without a receipt**. Do not summarize the bound tally as completed recipes or completed independent replays.
2. Append a narrow clarification to the timing explanation rather than rewriting historical reports: ColdA01's retained child was stopped at 240 seconds and ColdA04's collector at 300 seconds. Say “stopped at the configured deadline,” not “proved to require more than six minutes.” ColdA02 observed completion in 339.22 seconds at the same content revision; differing load remains a limitation, not a measured cause.
3. Narrow ColdA01's “the command operates as stated” to “the completed prefix agrees with the documented per-leg behavior; this seat did not observe the whole-command result.” Preserve the timeout receipt and the actual gap classification. No post-data alteration of the frozen binding or credit rule is warranted by this sample.

No gate, selftest, sweep, or other runtime was invoked for this review. No production files or historical evidence were edited. No tools were installed or updated, and no background processes were started. The only file written is this report.
