seat: T46ReobsE
item: C1 independent re-observation at CONTENT `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` of four cap statements — callback-authoritative wave accounting, required-command-receipt-binding, refusing-registry-replay, mutation report interop — including their restated What / First-working-round cells and the digest pin's coverage of the case set that prints the claimed tally.

I am not the author of the standing rows (wave-1 ScribeStanding / L1) nor of the wave-1 observation (ExecStmt05). Read-only on the lane; all scratch under `/tmp/tameshi-r46-T46ReobsE/`. No tool installed or upgraded. Nothing written outside this report.

## Setup (as the counter builds it)

```
W=/tmp/tameshi-r46-T46ReobsE; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
```
→ `CLONES_DONE`, both `rev-parse HEAD` = `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`. The four statements have `cwd: clone`, so they ran in `$W/clone`; `$W/fleet/tameshi-shokunin` was not needed.

Frozen-surface checks (all read at the CONTENT revision, not the worktree):
```
git -C $W/clone show 6f2168e…:.ufo/evidence/round-46/calibration/statements.json | sha256sum
→ a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9   (= the contract's statements_sha256)
sha256sum $W/measure_at_rev.py  .ufo/evidence/round-46/calibration/measure.py   (worktree)
→ ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a  (both; self_pin would be 1)
append_only: base SCORECARD 207916 bytes, REV 225496 bytes, rev.startswith(base) → True, 64 appended lines
```
Counter `measure.py` imported with `importlib` from the CONTENT blob (`$W/measure_at_rev.py`); `last_rows(<SCORECARD at REV>)` then `claim_of(stmt, rows[(kind,id)])` per the item, plus `pick_line` for the observation. Each statement's argv ran **once** (my own `subprocess` call, env `REV` = CONTENT, `PYTHONDONTWRITEBYTECODE=1`); the sha is `git -C $W/clone show HEAD:<sha_file>` → sha256[:12].

## Row per statement

`/tmp/tameshi-r46-T46ReobsE/obs.py` (imports the CONTENT counter, runs each argv once, picks the `obs` line, reads the last row):

| id | claimed (last SCORECARD row at REV) | observed | verdict | wall / timeout | stdout lines | obs-regex matches |
|---|---|---|---|---|---|---|
| callback-authoritative wave accounting | `ACCOUNTING_SELFTEST: 8/8 pass` \| `0` \| `96b3038a77f8` | `ACCOUNTING_SELFTEST: 8/8 pass` \| `0` \| `96b3038a77f8` (exit 0) | **MATCH** | 1.06 s / 900 | 27 | 1 |
| required-command-receipt-binding | `COMMAND_BINDING_SELFTEST: 44/44 pass` \| `0` \| `9230c68e53a5` | `COMMAND_BINDING_SELFTEST: 44/44 pass` \| `0` \| `9230c68e53a5` (exit 0) | **MATCH** | 1.77 s / 900 | 45 | 1 |
| refusing-registry-replay | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` \| `0` \| `9fcd2dbba737` | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` \| `0` \| `9fcd2dbba737` (exit 0) | **MATCH** | 0.39 s / 900 | 11 | 1 |
| mutation report interop | `MTE_SELFTEST: 17/17 pass` \| `0` \| `193ea6e32f89` | `MTE_SELFTEST: 17/17 pass` \| `0` \| `193ea6e32f89` (exit 0) | **MATCH** | 0.16 s / 900 | 18 | 1 |

Full digests observed (sha256 of the `sha_file` blob at HEAD): `96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e` (`tools/wave-accounting.py`), `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` (`tools/command-binding.py`), `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` (`tools/registry-replay.py`), `193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4` (`tools/mte-interop.py`).

Standing-row location at REV (row lines from `ID … SCORECARD row lines at REV` in `obs.py`): `callback-authoritative wave accounting` 249 / 1523 / **2185**; `required-command-receipt-binding` 1057 / 1524 / **2186**; `refusing-registry-replay` 1150 / 1525 / **2187**; `mutation report interop` 1234 / 1526 / **2188**. `last_rows` overwrites by `(kind,id)` in file order, so 2185-2188 are compared; the `claim_sha` group I printed consumes exactly those cells.

Cross-check, not a verdict (the L1's run decides): the counter itself, run once into a scratch work dir at the CONTENT revision
```
python3 $W/measure_at_rev.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work $W/c1work
→ STATEMENT cap/callback-authoritative wave accounting: claimed=ACCOUNTING_SELFTEST: 8/8 pass|0|96b3038a77f8 observed=… MATCH
→ STATEMENT cap/required-command-receipt-binding: … MATCH
→ STATEMENT cap/refusing-registry-replay: … MATCH
→ STATEMENT cap/mutation report interop: … MATCH
→ C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R46_PASS=true   (EXIT=0, 730.09 s)
```
These four lines are byte-identical to my independent observations. The other 18 statements were not independently re-observed by me; the counter's lines are the only evidence I have for them.

## What / First-working-round cells

| id | What (cell 2) | does it still describe the capability? | First (cell 4) |
|---|---|---|---|
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | **yes, proven.** `python3 tools/wave-accounting.py --selftest` prints 8 discriminated cases whose names map 1:1 to the clauses (`registry-id-mismatch`, `duplicate-agent`, `missing-outcome`, `unknown-status` → identities/terminal states; `failed-with-report-counted-completed` → partial artifacts of a failed seat, `report_artifacts`/`failed_with_report` in `tools/wave-accounting.py:105,118`; `false-completion-count` → mismatched totals; `snapshot-tampering` → digest tampering; `replacement-seat` → REPLACEMENT_FORBIDDEN) | `round 22` — confirmed: `git log --diff-filter=A --format='%h %ad %s' -- tools/wave-accounting.py` → `66a25ab 2026-10-21 round-22: add callback-status accounting gate and sourced lesson` |
| required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | **yes, proven.** The 44 printed cases cover name (`duplicate`, `unknown`), argv (`argv-order`, `argv-extra`, `argv-missing`, `argv-normalized`, `argv-case-only`, `argv-padded-token`), cwd (`wrong-cwd`, `noncanonical-cwd`), revision (`stale-revision`, `short-revision`) and outcome (`wrong-exit`, `stderr-cannot-supply-token`, `bool-exit`). The tool's own bound ("validates retained declarations, not their producer authenticity", `tools/command-binding.py:13-14`) is narrower than the cell, so no overstatement | `round 23` — `496d212 2026-10-21 round-23: implement explicit command receipt binding and full replay streams` |
| refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | **second clause proven, first clause not exercised — see F2 (LOW).** The 10 printed cases all drive `--project` (9) and `--plan` (1); `'--run'` appears 0 times inside `selftest()` | `round 24` — `d2eaecd 2026-10-21 round-24: add refusing registry replay, fixture kills, pinned registry successors and sourced entry` |
| mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | **schema/metrics half proven on fixtures, "each recorded leg" not exercised — see F3 (LOW).** The selftest calls the real `leg_report()` on one synthetic leg dir and `judge()` on 16 hand-seeded reports; `check(`/`mutate-and-run` appear 0 times inside `selftest()`. The official library is real: `official_metrics()` extracts the vendored `mutation-testing-report-schema 3.9.0` and `mutation-testing-metrics 3.9.0` tarballs after `sha512` verification (`tools/mte-interop.py:176-181`) and runs `calculateMetrics` under node | `round 25` — `2a97ec1 2026-10-21 round-25: freeze C1/C2 contract, rulers, fixtures, interop tool and before receipts` |

All four First-round cells are therefore accurate. The four rows are byte-exact `emit_row` output for the observed tuples (`EMIT_CAP` split; evidence, What and First cells all identical to the standing cells) — the author did not hand-edit the emitted evidence.

## Findings

**F1 — LOW (calibration; digest pin does not cover the case set that prints the claimed tally).** Attacks the `tool sha256` field of `callback-authoritative wave accounting` and `required-command-receipt-binding`, and `statements.json`'s `sha_file`. Both selftests load their supplemental expectations from files that neither the row nor `statements.json` pins: `tools/wave-accounting.py:148-153` loads `.ufo/evidence/round-22/measure.py` (blob `b29573dbea55884eb6f6372d55ed58f6bb111d99`) and `.ufo/evidence/round-22/accounting-extra-cases.json` (blob `08961235326ec50aadfe6a7130f244330592add3`); `tools/command-binding.py:164-167` loads `.ufo/evidence/round-23/extra-cases.json` (19 cases) and `.ufo/evidence/round-24/extra-cases.json` (6 cases). For wave accounting the claimed line itself is printed by the unpinned oracle (`result, code = module.measure(root)` → `ACCOUNTING_SELFTEST: 8/8 pass`). Reproduced on a scratch copy of the clone:
```
cp -a $W/clone $W/clone-mut2; patch .ufo/evidence/round-22/measure.py: "'discriminated': ok}" → "'discriminated': True}"
python3 tools/wave-accounting.py --selftest → ACCOUNTING_SELFTEST: 8/8 pass / ACCOUNTING_EXTRA_SELFTEST: 16/16 pass / FINDING: SELFTEST_PASS, exit 0
sha256sum tools/wave-accounting.py → 96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e  (unchanged)
```
```
cp -a $W/clone $W/clone-mut; set case "argv-order" in .ufo/evidence/round-23/extra-cases.json to the "receipt-order-clean" bundle/expected (0, [])
python3 tools/command-binding.py --selftest → COMMAND_BINDING_SELFTEST: 44/44 pass, exit 0
sha256sum tools/command-binding.py → 9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d  (unchanged)
```
In both cases the standing row would still be MATCH: a case can be neutralized with the tally and the pinned digest unchanged. The bound is asymmetric and loud on the other side — deleting the fixtures fails closed: `python3 tools/command-binding.py --selftest` with a missing fixture prints `COMMAND_BINDING_SELFTEST: fixture-unavailable` (exit 1), wave accounting prints `FINDING: SELFTEST_UNAVAILABLE` (exit 2), and the `obs` regex matches neither, so the statement becomes UNOBSERVABLE rather than silently green. `mutation report interop` is not exposed to this class: its vendored tarballs are `sha512`-verified inside the pinned tool. Not drift: `git -C $W/clone diff --stat 745a583… 6f2168e… -- .ufo/evidence/round-22 .ufo/evidence/round-23 .ufo/evidence/round-24` → empty.

**F2 — LOW (What-cell overstatement).** Attacks the `What` cell of `refusing-registry-replay` (SCORECARD.md:2187). "replay frozen registry requirements" is not exercised by the frozen command: `python3 tools/registry-replay.py --selftest` prints exactly `CASE clean|not-held|cleanup|held-missing|stream|stream-at-limit|external|non-hermetic|invalid|plan-realpath PASS`, and the selftest's subprocess calls use `'--project'` (×1) and `'--plan'` (×1), `'--run'` (×0) — the replay mode declared at `tools/registry-replay.py:251`. The refusal half is proven (the rejected-row cases assert `(out/'bundle.json').exists() == False`). What the command proves is the projection refusal and the realpath plan, not the replay.

**F3 — LOW (What-cell overstatement).** Attacks the `What` cell of `mutation report interop` (SCORECARD.md:2188). "emit each recorded leg" is not exercised: `python3 tools/mte-interop.py --selftest` emits **one** synthetic leg (`emit_tmp/pristine.target.t.py` + `spec.copy` + `results.tsv`, 3 defects) through `leg_report()` and judges 16 hand-seeded reports; the path that emits the ledger's recorded legs (`--check`, which runs `tools/mutate-and-run.sh --regression --keep`) is never called inside `selftest()` (grep count 0). The schema and official-metrics clauses are proven (17/17 including `emitter-locations`). Suggested honest narrowing: "emit a leg directory as an MTE report and judge reports with the official schema and metrics library".

**F4 — LOW (stale superseded text; inherited from wave 1).** Attacks the supersession claim in the round-46 block ("This section supersedes, for every value it states, the standing rows … above", SCORECARD.md round-46 section) against SCORECARD.md:1524 and :1525, which still read `… exit 0 (not a C1 statement)` for `required-command-receipt-binding` and `refusing-registry-replay`. Those two **are** C1 statements — `python3 -c "import json;d=json.load(open('/tmp/tameshi-r46-T46ReobsE/statements_at_rev.json'))['statements'];[print(i,'of',len(d),s['id']) for i,s in enumerate(d,1) if s['id'] in ('required-command-receipt-binding','refusing-registry-replay')]"` → `11 of 22 required-command-receipt-binding`, `12 of 22 refusing-registry-replay`. The supersession sentence covers *values*, and a membership assertion is not a value, so the false phrase survives in the file a reader meets first. Wave-1 `ExecStmt05.md:95` flagged the same contradiction; it is unchanged at CONTENT. Costs the counter nothing (the counter reads the 2186/2187 cells).

**F5 — INFO (difference from wave 1; the intended closure).** Same four statements, two revisions, same commands:
```
wave-1 ExecStmt05 (freeze 745a583…): claimed=- for wave accounting; claimed lacking the sha clause for the other three; all four UNPARSED
T46ReobsE  (CONTENT 6f2168e…):       all four claimed=<line>|0|<sha12>, all four MATCH
```
The observed tuples did not move between the two revisions, and the four tool blobs are identical at freeze and at CONTENT (`git rev-parse 745a583…:<f>` == `git rev-parse 6f2168e…:<f>` for all four; `git diff --stat` over the four tools + counter + statements.json empty). So the MATCH was achieved by appending rows, not by editing tools — the honest reading of C1's move.

**F6 — INFO (wave-1 report inaccuracy, not an artifact defect).** `ExecStmt05.md:95` says the two ids are "ids 10 and 11 of 22"; they are 11 and 12 (0-based index 10/11). Command above. No consequence for C1.

**F7 — INFO (understatement, already noted by wave 1).** `callback-authoritative wave accounting`'s Evidence cell states only `ACCOUNTING_SELFTEST: 8/8 pass`; the command also prints `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`, which `pick_line` does not read. Not a defect: a failing extra case still changes the exit code (`code = code if code else (0 if good == len(cases) else 1)`, `tools/wave-accounting.py:193`), so the row's `exit 0` catches it.

**F8 — INFO (fail-closed on a missing dependency; measured for one of the four).** `mutation report interop` needs `jsonschema` and node. Blocking the import:
```
PYTHONPATH=/tmp/tameshi-r46-T46ReobsE/block (jsonschema.py: raise ImportError) python3 tools/mte-interop.py --selftest
→ MTE_SELFTEST: SETUP (blocked for probe), exit 2; obs regex `^(MTE_SELFTEST: \d+/\d+ pass)` match: False
```
so the statement turns UNOBSERVABLE, never silently green. The node-absent path (`official_metrics` → `Setup('node not found')`, same SETUP exit 2) was read, not run.

## Not run / limits

- The C1 counter's `--selftest` (18 cases) was not run by me.
- The other 18 statements were not independently re-observed; only the counter's scratch lines cover them.
- The `node`-absent SETUP path was read from `tools/mte-interop.py:190-196`, not executed.
- I did not edit, commit or run any mutating git/jj command in the lane; the two mutants live in `/tmp/tameshi-r46-T46ReobsE/clone-mut{,2}`.
- Deciding runs remain the L1's; everything above is a seat observation.
