# ReReplay25 — re-attack of round-23 Replay25 (row `registry-check-selftest`)

Seat: TameshiR25.ReReplay25 (critic, leaf; no subagents). Judged on: calibration.
I wrote only this report. Mutant runs happened only in `/tmp/rr25-replay25`, a fresh clone checked out at the lane revision, which I removed afterward. No tools were installed or upgraded.

## Verdict

**FINDING.** For the round-23 row, the static binding is exact: argv, expect, receipt argv, cwd, revision and exit all match, and the digest pin holds. But the frozen `expect` makes a false acceptance possible at the field level. `stdout_contains: ["SELFTEST: PASS"]` does not pin the case count. In a run, a `registry-check.py --selftest` that executes **zero cases** got `held=true` from the registry runner and **CLEAN** (exit 0, no findings) from `tools/command-binding.py`. The row's baseline `source` anchor is also false provenance. Round 17 already recorded that defect, and it is still unfixed. Both findings still apply at lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`.

## Static binding of the frozen row (round-23 artifacts)

| field | value | sources compared | result |
|---|---|---|---|
| argv | `["python3","tools/registry-check.py","--selftest"]` | `requirements.json`, `registry-baseline.json`, bundle requirement, bundle receipt, observation `argv`, observation `requirement.argv` | identical in all 6 |
| expect | `{"exit":0,"stdout_contains":["SELFTEST: PASS"]}` | `requirements.json`, `registry-baseline.json`, bundle requirement | identical |
| registry | `registry-baseline.json` = `git show 28cae17:tools/registry.json` (`cmp` equal), sha256 `ebd2e69a…ec92a` = `requirements.json.registry_sha256` | also equal to `496d212:tools/registry.json` | exact |
| bundle requirements | all 43 equal to `requirements.json.requirements` | Python `==` | exact |
| receipt exit | `0` = `runner_result.got` = `expect.exit` | bundle vs observations | exact |
| receipt cwd / revision | `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`, `496d212b…4182963` | receipt = observation = bundle top level | exact |
| stdout | 2700 bytes, stderr 0 bytes; receipt stdout == `runner_result.stdout` == `runner_result.stdout_tail` | 51 `SELFTEST_CASE … PASS` lines, then `SELFTEST: PASS (51 cases)`; token appears once; no `FAIL` | present |
| digest pin | `expected.json.bundle_sha256` = sha256(bundle.json) = `3d6c99b7…a50b9` | recomputed | exact |

I re-ran the binder at the lane revision on the frozen bundle, in the `/tmp` clone:

```
$ python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json
{"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
exit=0
```

## Evidence actually present vs inferred

- **Present:** the complete decoded stdout and stderr, the integer exit (`proc.returncode`, `registry-check.py:711-719`), and a digest-pinned bundle.
  - The stdout is 2700 bytes, which is under `TAIL_BYTES = 4096` (`registry-check.py:110`, `_tail` at `:386-388`). So for this row the "full output" is byte-identical to the tail and adds nothing beyond it.
- **Copied, not observed:** the receipt `argv`, `cwd` and `revision` were not captured from the process. They are the same Python values used to build the requirement and the bundle header:
  - argv: `replay.py:39`, `:62`, `:68`
  - cwd and revision: `replay.py:62`, `:66-68`
  - So `ARGV_MISMATCH`, `CWD_MISMATCH` and `REVISION_MISMATCH` cannot fire for this producer.
  - From reading the code (not observed), `Popen(row["argv"], cwd=cwd)` (`registry-check.py:676-683`) receives exactly these values. The declaration is therefore truthful, but nothing independent such as `/proc/<pid>/cmdline` or `cwd` was retained.
  - The interpreter `python3` resolves through `PATH` (`row_env`, `registry-check.py:170-174`), and its identity is not recorded.
- **Provenance of `runner_sha256`:** `observations.json.runner_sha256` hashes the **live lane** file `args.repo/tools/registry-check.py` (`replay.py:78`). The code actually executed was loaded from the clone (`replay.py:54-56`), and the row subprocess ran the clone's file.
  - The value happens to be correct: `cba16646…44ad` equals `git show 496d212:tools/registry-check.py | sha256sum`, and the same holds at `c9ff09f`.
  - The field's provenance is still the live tree, not the executed bytes.
- **Not authenticated:** `measurement_interval`, `elapsed_s` and the per-case timings are self-reported by the producer. The temporary cwd no longer exists. I make no claim about producer authenticity or historical metadata, and I did not retrofill either.

## Finding 1: false acceptance at the field level (concrete, executed)

`registry-check.py` prints `SELFTEST: PASS ({passed} cases)` (`:1816`). The frozen token `SELFTEST: PASS` is a substring check (`command-binding.py:111`, runner `registry-check.py:718`), so any case count, including 0, satisfies it. At `496d212` the selftest had 51 cases, and round-24 `RowAudit01.md:72` read that count but did not treat it as part of the binding.

Adversarial change: `/tmp` clone at `c9ff09f`, with these two lines inserted at the top of `selftest()` in `tools/registry-check.py`:

```python
print("SELFTEST: PASS (0 cases)")
return 0
```

I ran the frozen round-23 requirement through the unchanged `run_row`, built the receipt exactly as `replay.py:66-71` does, labelled it with revision `c9ff09f…`, pinned it, and ran the lane binder:

```
$ sha256sum fleet/tameshi-shokunin/tools/registry-check.py
e327d7443082b99b1169efe07d5f01d76c04f51ff3757051fe99fe3e89c92c1a   (pristine: cba16646…44ad)
runner_result {"got": 0, "held": true, "stdout": "SELFTEST: PASS (0 cases)\n", "stderr": ""}
$ python3 fleet/tameshi-shokunin/tools/command-binding.py --bundle mutant-bundle.json --expected mutant-expected.json --json
{"bundle_sha256": "f8b8925bc88a4fb0de2e0042bafa1482cceea85823f0a79dbb6d7258c0c7993c", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
binding_exit=0
```

A selftest with every case deleted is accepted by both the registry runner and the binder.

The same run also accepted a receipt labelled `c9ff09f` whose executed bytes differ from that revision (`git status` shows ` M tools/registry-check.py`). The binder's docstring disclaims "continuous checkout identity" (`command-binding.py:10-13`). So this second point is a stated tradeoff, not a binder defect.

## Finding 2: the baseline source does not establish argv or expect (already known, still open)

- The row cites `source: "SKILL.md@98bea7d:1806"`. At `98bea7d`, line 1806 is the heading `### Round-16 gate/probe registry`. That table (`:1808-1813`) does not list `registry-check.py`.
  - `git ls-tree 98bea7d tools/` contains no registry file at all.
  - `tools/registry-check.py` was first added at `2a22ade` (round 17).
- The command is actually defined at `SKILL.md@c9ff09f:1851`, with `--selftest` and exit 0 meaning "every active row held". No stdout token is specified there, so the token comes from the tool, not from the documentation.
- `SOURCE_RE` validates only the shape of the field and never opens the cited file (`registry-check.py:257-261`).
- Round 17 reported this as `.ufo/waves/round-17/w2/RegistryCompleteness.md:122-139` (F4, rows 10 and 25-28). It is still uncorrected in `tools/registry.json` at `c9ff09f` and at `HEAD` (`5b69fb2`). Five rows still carry this anchor.

## Latent gap (inference only, not exercised)

- The receipt projection (`replay.py:68-71`) drops the runner's `held`, `cleanup_error` and `stdout_missing` fields, and the receipt schema has no field for them (`command-binding.py:87-88`).
- `run_row` sets `held = got == expected_exit and not missing and cleanup_ok` (`registry-check.py:720`). A row whose descendants survive bounded cleanup would therefore be `held=false` in the registry, yet still bind CLEAN.
- For this row, `cleanup_ok` was true: `held: true` with no `cleanup_error` key.

## Still applies at the lane revision `c9ff09f`

- **Row:** byte-identical JSON content in `c9ff09f:tools/registry.json` and in `HEAD`. The whole file changed (sha `ebd2e69…` became `a8f255f1…`), but this row did not. It is not superseded.
- **`tools/registry-check.py`:** unchanged; sha `cba16646…` at `496d212`, `1f73157`, `c9ff09f` and `HEAD`.
- **`tools/command-binding.py`:** sha `d533dc1e…` became `9230c68e…`. The only change between `496d212` and `c9ff09f` is that selftest now also loads `round-24/extra-cases.json`. `evaluate()` is unchanged, so the token check is the same. I executed Finding 1 against the `c9ff09f` binder.

## Impacted axes

Calibration: a token-only `expect` gives a vacuous acceptance of a coverage-bearing selftest. Provenance: the `source` anchor and the `runner_sha256` origin.

## Smallest safe correction

1. **Registry, not the binder.** Add a pinned successor row for `registry-check-selftest`, using the existing `superseded_by` mechanism, with:
   - `stdout_contains: ["SELFTEST: PASS (51 cases)"]`, using the count current at the successor's revision;
   - `source` re-anchored to the `SKILL.md` line that names `registry-check.py … --selftest` at that revision (today `:1851`).

   The tradeoff: every added selftest case then forces a new registry successor. That is the round-24 pinned-successor discipline, and the gate's judge has to accept it.
2. **Optional, for the replay instrument only.** Hash the clone's executed `tools/registry-check.py` for `runner_sha256` instead of the live lane copy. Carry `held` and `cleanup_error` beside each receipt in `observations.json` so the lost cleanup state stays visible.

R23-REATTACK Replay25: FINDING
