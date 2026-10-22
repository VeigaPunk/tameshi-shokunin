# R23-REATTACK Replay02: exact row `repeat-control-snapshot-mismatch`

**Verdict: FINDING.** The static binding of the row is exact, and the frozen instance really reproduces. The pin is not a sufficient witness. The row binds only `expect.exit = 1`, and `repeat-control.py --snapshot` returns 1 both when the snapshot reproduces its recorded `controls_mismatch` and when it fails to reproduce any recorded expectation. I built a self-consistent snapshot whose three control runs are identical and whose record says `controls_mismatch`. The tool exits 1 and `command-binding.py` returns CLEAN at both the c9ff09f copy and the round-23 copy. The finding still applies at c9ff09f and at HEAD (5b69fb2).

Confidence: high on the mechanics (executed on /tmp copies). Moderate on practical exposure: it needs a later tree that rewrites that fixture, and I assert nothing about who would write one.

Tags: **[EXEC]** = run by me on a /tmp copy. **[READ]** = read with line numbers. **[INF]** = inference, not tested.

## Scope and bounds
- Frozen inputs read: `.ufo/evidence/round-23/requirements.json`, `replay/bundle.json`, `replay/observations.json`, `replay/expected.json`, `replay.py`, `registry-baseline.json`, `tools/command-binding.py`.
- Executed: the row's tool in snapshot mode on a `git archive` replica of revision 496d212 (scratch under `/tmp/r25-rereplay02/`); two adversarial /tmp variants; `command-binding.py` (copies taken from the 496d212 and c9ff09f blobs) on /tmp bundles; one read-only `command-binding.py` run on the frozen bundle in place, which wrote nothing.
- Not run: `replay.py`, `registry-check.py`, any `--selftest`, any suite, any registry command in the lane. No lane writes, no production edits.
- Deviation: one early `git status --porcelain` ran without `GIT_OPTIONAL_LOCKS=0`, so it may have refreshed `.git/index` stat data. It showed only untracked entries and changed no tracked content. Every later git call used `GIT_OPTIONAL_LOCKS=0` or was read-only (`show`, `diff`, `rev-parse`, `archive`).
- Tools installed or updated: none. Python 3 standard library only.
- lsp device: not available. `read xd://lsp` returned "No such tool: xd://lsp. Mounted devices: ast_edit, debug." So there was no semantic caller or reference search. Caller and reference checks were done by reading with line numbers and by execution.

## 1. Static binding (confirmed)
- Baseline source: `SKILL.md@98bea7d:1503`, row "repeated pristine controls": `--snapshot DIR`, pinned `mismatch/expected.json`, verdict map "1 failed" [READ: `git show 98bea7d:SKILL.md | sed -n 1495,1512p`].
- The row JSON is identical at 28cae17 and 496d212 (`tools/registry.json` file sha256 `ebd2e69a…`, equal to the frozen `registry_sha256`), and at c9ff09f and 5b69fb2 (file sha256 `a8f255f1…`). Row: argv `["python3","tools/repeat-control.py","--snapshot",".ufo/evidence/round-12/ControlGate/mismatch"]`, expect `{"exit":1}`, status `active`, timeout 60, tags `baseline`.
- Frozen `registry-baseline.json` has sha256 `ebd2e69a…`. Its active row projects exactly onto the `requirements.json` row (checked: `requirement == baseline projection: True`). The name occurs once each in requirements (43 rows), bundle receipts (43) and observations (43).
- Observation argv == receipt argv == requirement argv (True). Receipt stdout, stderr and exit equal the observation `runner_result` (True).
- `command-binding.py` `evaluate()`: exact equality on argv (c9ff09f:103-104), cwd (105-106), revision (107-108), and exit as an exact int (109-110; `bool` rejected at line 90).
- Limit: all of these compare the bundle with itself. The bundle's requirements are written by the harness. The tie to the registry is `replay.py`'s own check, which I re-ran by hand above, not `command-binding.py`.

## 2. Evidence present vs inferred
Present (bytes retained and checked):
- Full output, not tails. The observation stdout is five lines and equals `stdout_tail`. stderr is empty and equals `stderr_tail`. The runner kept full streams (`retain_streams=True`, registry-check.py:724-726). The tail window is 4096 bytes (line 110), which this output fits inside.
- `got=1`, `expect=1`, `held=true`. `elapsed_s` 0.073 against a measurement interval of 0.073036 s (internal consistency only).
- [EXEC] Replica at 496d212, same argv, cwd = replica root: rc 1. Stdout and stderr are byte-identical to the frozen receipt.
- [EXEC] All nine input digests of the round-12 snapshot verify.

Inferred (declared by the harness, not observed from the process):
- argv: `list(row['argv'])` (replay.py:62-63). By code this is the list passed to `Popen` (registry-check.py:676-677). No pid, cmdline, or resolved executable was retained.
- `python3`: PATH-resolved. `git_env()` removes `GIT_*` keys and adds git and locale settings (registry-check.py:149-166); PATH is inherited. The interpreter binary is not recorded. [INF: a different interpreter would go undetected; not tested.]
- cwd: `str(clone)` (replay.py:62), the same value given to `Popen` (registry-check.py:678).
- revision: the requested revision after `rev-parse` (replay.py:32-33). replay.py:50 checks out with `check=True` but does not re-read HEAD. The materialize path in registry-check.py (lines 809-818) does.
- Tool identity: `tool-sha256=296fe566…` is the tool's own self-report. It equals `git show 496d212:tools/repeat-control.py | sha256sum`, so git corroborates the content, not the run.
- `measurement_interval`: harness wall clock around `run_row` (replay.py:59-61).

Rejected, as the item requires:
- Producer authentication: nothing in the chain is signed or attested. `expected.json`, the bundle and the observations come from one run and carry plain sha256 digests. I do not treat them as proof of origin. The finding below does not depend on origin.
- Historical retrofill: no evidence of it. The round-12 `mismatch/expected.json` has only `schema, runs, expected_id, expected_exit, inputs`. Invocation fields (argv, cwd, revision, measurement_interval) appear only in the round-23 observation rows, which `replay.py` writes fresh.

## 3. Field-level false acceptance (the finding)

Field: the row's `expect` carries only `exit`.
- `evaluate()` reads stdout only through `stdout_contains` (c9ff09f:111-112). This row has none. stderr is type-checked (line 91) and never compared. So at exit 1 the binding accepts any stdout and any stderr.
- The tool returns 1 on two different branches of `snapshot_mode` (repeat-control-496d212.py):
  - Reproduced: `return finish(record["expected_id"])` (462-463). stderr is empty.
  - Not reproduced: `return finish("controls_mismatch", message=…)` (464-473). The message goes to stderr (188-189).
  - In both branches the last stdout line is `REPEAT_CONTROL: controls_mismatch` (190). Only the `SNAPSHOT_EXPECTED` and `SNAPSHOT_OBSERVED` lines (460-461) and stderr tell the branches apart. The binding reads neither for this row.

Concrete adversarial delta, ADV-A [EXEC]:
1. `git archive` of 496d212 (tools and round-12 ControlGate) into `/tmp/r25-rereplay02/rev496`. Copy that to `adv-identical-claims-mismatch`.
2. Overwrite `run-2.*` and `run-3.*` with `run-1.*`: stdout `mismatch-out\n`, stderr `mismatch-err\n`, exit `0\n`.
3. Keep `expected_id=controls_mismatch`, `expected_exit=1`. Recompute the nine digests so the record is self-consistent.
4. Run `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch`. Observed: rc 1.
   - stdout: `SNAPSHOT_INPUTS 9 verified` / `SNAPSHOT_EXPECTED id=controls_mismatch exit=1` / `SNAPSHOT_OBSERVED id=controls_match exit=0` / `REPEAT_CONTROL: controls_mismatch`
   - stderr: `repeat-control: snapshot expectation not reproduced: expected=controls_mismatch/1 observed=controls_match/0`
5. Single-row bundle: the row's argv and `expect {"exit":1}`, receipt with exit 1 and that stdout and stderr, cwd and revision as in the replica. `command-binding.py --json`: rc 0, `finding_ids: []`. Same result at the c9ff09f copy (sha256 `9230c68e…`) and the 496d212 copy (sha256 `d533dc1e…`).

Other variants [EXEC], identical results at both binding copies:

| Variant | Tool rc | Current pin `{exit:1}` | Proposed pin (section 5) |
|---|---|---|---|
| ADV-A: identical runs, record claims controls_mismatch/1 | 1 | CLEAN | STDOUT_MISMATCH |
| ADV-B: frozen mismatching runs, record claims controls_match/0 (`SNAPSHOT_EXPECTED id=controls_match exit=0`, `SNAPSHOT_OBSERVED id=controls_mismatch exit=1`) | 1 | CLEAN | STDOUT_MISMATCH |
| Exit 1 with empty stdout and stderr | n/a (synthetic receipt) | CLEAN | STDOUT_MISMATCH |
| Frozen replica output, receipt exit forced to 0 | n/a (synthetic receipt) | EXIT_MISMATCH | EXIT_MISMATCH |
| Frozen replica output, exit 1 | 1 | CLEAN | CLEAN |

Consequence: the row does not establish what a red control has to establish, namely that the mismatch fixture's controls diverge and the gate detects it. It establishes only that the snapshot verdict was non-zero. The runner's `held` is also exit-only for this row: `held = got == expected_exit and not missing and cleanup_ok` (registry-check.py:720), with no needles [READ, not executed].

Scope of the attack: ADV-A and ADV-B need a later tree that rewrites that fixture. They were constructed, not observed in the lane. At 496d212 the fixture tree reproduces (executed). The fixture tree (`1c7ddff5…`) and the tool and binding blobs are identical at c9ff09f and 5b69fb2 [READ], so the frozen instance holds at the lane revision too.

The tool's own selftest was not run. Statically it does not cover this gap: the mismatch case is `snapshot-mismatch-pass` (repeat-control-496d212.py:785). `snapshot_case` compares only the last `REPEAT_CONTROL:` line (636-643, via `last_finding_id` at 559-567), which is identical in both branches. No selftest case reaches the not-reproduced branch [READ].

## 4. Still applies at c9ff09f?
Yes [READ + EXEC].
- Row: unchanged. The same JSON at 496d212, c9ff09f and 5b69fb2. Status `active`, so not superseded.
- `command-binding.py`: 496d212 to c9ff09f changes only lines 161-172 (the selftest now also loads round-24 extra cases). `evaluate()` (65-113) is unchanged. c9ff09f and 5b69fb2 are identical.
- `repeat-control.py` (sha256 `296fe566…`) and `registry-check.py` (sha256 `cba16646…`) are identical at 496d212, c9ff09f and 5b69fb2.
- Frozen 43-row bundle (sha256 `3d6c99b7…`, matching `expected.json`) at both binding copies: rc 0, `finding_ids []`. The lane-side run printed `COMMAND_BINDING: CLEAN none`, rc 0.

## 5. Smallest safe correction (not applied)
In `tools/registry.json`, row `repeat-control-snapshot-mismatch`, change `expect` from `{"exit": 1}` to:

```
{"exit": 1, "stdout_contains": ["SNAPSHOT_EXPECTED id=controls_mismatch exit=1", "SNAPSHOT_OBSERVED id=controls_mismatch exit=1"]}
```

- [EXEC] Frozen replica: CLEAN. ADV-A, ADV-B and empty-output: STDOUT_MISMATCH, at both binding copies.
- Why these two lines: `snapshot_mode` prints each SNAPSHOT line exactly once per run. With both present and exit 1, expected = observed = controls_mismatch/1 is forced. Pinning `REPEAT_CONTROL: controls_mismatch` alone would not work, because ADV-A prints that line.
- The runner's needle check is literal and case-sensitive. The code checks complete stdout (registry-check.py:717-718), though the docstring (lines 36-37) says "over the retained tail". The frozen stdout satisfies the pin.
- Consequence: the registry file changes, so the round-23 freeze (`registry_sha256` `ebd2e69a…`) stops matching. Applying this needs a new freeze and a replay of this row. That is the integrator's call. I did not edit anything.
- Optional, larger: make the not-reproduced branch emit a distinct verdict id. That changes `repeat-control.py`'s content and therefore the frozen tool identity. Out of scope for this row.

## 6. Residual risks and verification gaps
- Binding exactness is internal to one harness run. Nothing outside the run anchors requirements, receipts, cwd, revision or the expected digest.
- The `python3` executable identity is not recorded and was not tested [INF].
- Clone HEAD is not re-read after checkout in `replay.py` (line 50) [INF: low risk, because a failed checkout raises].
- Doc drift: the `registry-check.py` docstring (lines 36-37) says `stdout_contains` is checked "over the retained tail"; the code (717-718) checks complete stdout. No effect on this row, which has no needles. It matters for any row that relies on tails.
- The row alone is one-sided: a tool that always exits 1 passes it. The clean row (expect 0) would reject that. I did not run the clean row [INF].
- The other 42 rows were not checked.

## Reproduce
- `GIT_OPTIONAL_LOCKS=0 git archive --format=tar 496d212bc46789cdf8cafab72978bdb7f4182963 tools .ufo/evidence/round-12/ControlGate | tar -x -C /tmp/r25-rereplay02/rev496`
- In `/tmp/r25-rereplay02/rev496`: `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch` gives rc 1, five stdout lines, empty stderr, equal to the frozen receipt.
- Adversarial trees and bundles: `/tmp/r25-rereplay02/adv-*` and `/tmp/r25-rereplay02/bundles/*`. Binding copies: `/tmp/r25-rereplay02/src/command-binding-{496d212,c9ff09f}.py`. Scratch lives outside the lane and can be removed.
- Lane-side read-only check: `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json` gives `COMMAND_BINDING: CLEAN none`, rc 0.

R23-REATTACK Replay02: FINDING
