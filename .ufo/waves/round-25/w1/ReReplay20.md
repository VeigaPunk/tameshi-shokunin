# R23 re-attack — Replay20 (row `measure-round16-selftest`)

## Verdict

FINDING. The row's argv, cwd, revision and exit are bound exactly, but the stdout check is weak enough to accept a false result. The row expects `stdout_contains: ["MEASURE_SELFTEST:"]`. That token is printed by every selftest run that reaches its summary line, whatever the case count. The selftest exits 0 whenever `passed == len(checks)`, so a weakened `measure.py` with zero checks prints `MEASURE_SELFTEST: 0/0 pass` and exits 0. `tools/command-binding.py` accepts that receipt as CLEAN, so the row cannot tell the retained 38/38 run apart from an empty selftest. The cited baseline source does not contain the token either.

The finding still applies at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. The registry row is byte-identical, `evaluate()` in `command-binding.py` is unchanged, `measure.py` is unchanged, and the round-25 multi-token fixtures do not cover case-count pinning.

## What I checked, and what was present versus inferred

Lane checkout HEAD is 5b69fb23. c9ff09f is an ancestor of it, and `git diff --stat c9ff09f HEAD -- tools/command-binding.py tools/registry.json` is empty. `git status --porcelain` on the audited paths is empty.

Static binding across the frozen artifacts. I compared them in Python and observed the following:
- The `argv` and `expect` fields are identical in three places: `registry-baseline.json:507-527` (sha256 `ebd2e69a…`, which equals `requirements.json` `registry_sha256` and `git show 496d212:tools/registry.json`), `requirements.json:293-305`, and `replay/bundle.json:889-901`. Their value is `["python3", ".ufo/evidence/round-16/measure.py", "--selftest"]` with `{"exit": 0, "stdout_contains": ["MEASURE_SELFTEST:"]}`.
- The receipt at `replay/bundle.json:279-289` matches the observation at `replay/observations.json:891-932` on argv, cwd (`/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`) and revision (`496d212b…`). Exit is 0 and `runner_result.got` is 0. Stderr is `''`.
- The full stdout is 1065 bytes, with 38 `PASS` lines, 0 `FAIL` lines, and exactly one `MEASURE_SELFTEST: 38/38 pass (scratch /tmp/tameshi-r16-CRMeasure-2uj39g0g)`. `stdout`, `stdout_tail` and the bundle receipt stdout are byte-equal, because the output fits under the tail limit, so the full stream and the tail are the same here.
- Elapsed time was 0.783 s against `timeout_s` 120. The measurement interval is `14:44:34.780887` to `14:44:35.563760`.

The frozen bundle validates under both versions of the tool:
- `python3 /tmp/rereplay20-c18I/cb.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` returned `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": []}`. Here `cb.py` is the c9ff09f blob.
- Running the same command with `cb23.py` (the 496d212 blob) gave the identical result.

Evidence that is present in the retained artifacts:
- argv, cwd, revision, integer exit, complete stdout and stderr, and the per-row interval, all retained.
- Producer `replay.py:32-33,49-50` resolves the revision with `git rev-parse` and runs `checkout --detach` in a fresh clone.
- `runner_sha256` `cba16646…` equals `git show 496d212:tools/registry-check.py | sha256sum`.

Evidence that is inferred or not present:
- **Copied argv.** The receipt `argv` is not an independent observation of what ran. `replay.py:62` copies `list(row['argv'])` from the same source row the requirement came from, so ARGV equality holds by construction. It is consistent with execution only because `registry-check.py:676-677` passes `row["argv"]` to `Popen` unchanged. That is static code reading, not retained metadata.
- **Copied revision.** The per-receipt `revision` is the single resolved value copied into each row (`replay.py:63`). It was not re-read per command.
- **Not retained.** The interpreter that `python3` resolved to (path or version) and the child environment were not retained. Neither was a per-row blob digest of `measure.py`; its identity is inferred from the revision plus the checkout. The replay cwd no longer exists (`ls: cannot access '/tmp/tameshi-r23-replay-naxu6fzi'`).
- **Rejected inputs.** I treat nothing here as producer authentication, and I did not credit any metadata added to the round-23 artifacts after the fact.

## Counterexample: the stdout field accepts a false result

1. **Measure.py code.** `measure.py` (identical blob at 98bea7d, 496d212 and c9ff09f, checked with `git diff --quiet`) ends its selftest at lines 625-626:
   - `print('MEASURE_SELFTEST: %d/%d pass (scratch %s)' % (passed, len(checks), tmp))`
   - `return 0 if passed == len(checks) else 1`

   Checks are collected in `checks = []` (line 446). A mutant that drops checks prints `N/N` and exits 0. This includes an empty list, which gives `0/0`. This is from reading the code; I did not run a mutated `measure.py`, because the item forbids running the registry command.
2. **Synthetic bundles.** I built single-row bundles from the frozen row in `/tmp/rereplay20-c18I`, re-pinned each one with `expected.json`, and ran both binding versions on them. They gave identical results:
   - The unchanged row returned exit 0 with no findings.
   - Stdout `MEASURE_SELFTEST: 0/0 pass (scratch /tmp/x)\n` with exit 0 returned **exit 0 with no findings (false acceptance)**.
   - Stdout `FAIL exit2-no-repo\nMEASURE_SELFTEST: 37/38 pass …` with exit 0 returned **exit 0 with no findings**. This receipt contradicts itself under `measure.py`'s semantics. The binding's documented scope is checking retained declarations, so this is a tradeoff rather than a defect. The `0/0` case is the one that matters, because an unmodified producer running a weakened program can produce it.
   - Stdout `not MEASURE_SELFTEST: run\n` with exit 0 returned **exit 0 with no findings**. The token is matched anywhere in stdout, not anchored to a line.
   - As controls, exit 1 returned `EXIT_MISMATCH` and empty stdout returned `STDOUT_MISMATCH`. Both fired correctly.
3. **Source provenance.** The row cites `source: SKILL.md@98bea7d:1811`. That line reads ``| `.ufo/evidence/round-16/measure.py` | probe | `python3 … --rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage |``. It does not contain `MEASURE_SELFTEST`, and it does not document the selftest's exit 1 on failure. `git show 98bea7d:SKILL.md | grep MEASURE_SELFTEST` has no match. The token was taken from the code; the cited source does not support it.
4. **Sibling rows.** In the same registry at c9ff09f, sibling selftest rows pin the case count:
   - `tools/registry.json:838` expects `RECEIPT_MEASURE_SELFTEST: 10/10 pass`.
   - `:878` expects `ROUND21_MEASURE_SELFTEST: 13/13 pass`.
   - `:931` expects `COMMAND_BINDING_SELFTEST: 38/38 pass`.

   This row at `:512-518` does not pin the count. Rows at `:645` and `:730` also use count-free tokens; I did not audit them.

## Still applies at c9ff09fb41fb8aac5fc335faf10858ff606bd5df

- The row is not superseded. Its JSON at c9ff09f is the same as at round 23 (`"stdout_contains": ["MEASURE_SELFTEST:"]`, `status: active`, same source).
- `git diff 496d212 c9ff09f -- tools/command-binding.py` touches only `selftest()`, which now also loads `round-24/extra-cases.json`. The `evaluate()` stdout check is unchanged at line 111: `any(token not in receipt['stdout'] …)`.
- The round-24 replay receipt for this row (`.ufo/evidence/round-24/replay/bundle.json`, revision d2eaecd4) again shows `MEASURE_SELFTEST: 38/38 pass` under the same count-free expectation.
- The round-25 R23-ROUTED-1 fixtures (`.ufo/evidence/round-25/multitoken-cases.json`: `mt-missing-*`, `mt-offending-*`, `mt-clean-*`; `multitoken-mutants.spec` M1-M6) test all-of versus any-of token logic and iteration across rows. None of them tests whether a single token pins a case count, so they do not close this gap.

## Impacted axes

- **Calibration.** The C1 replay credits this row as a held 38-case selftest, but the binding only proves "summary line reached and exit 0".
- **Provenance.** The `stdout_contains` token is attributed to a source line that does not contain it.

## Smallest safe correction

Change only this registry row's expectation to match the sibling convention, and record the token's real origin:
- Set `stdout_contains` to `["MEASURE_SELFTEST: 38/38 pass"]`.
- Change `source` to cite `.ufo/evidence/round-16/measure.py@98bea7d:625-626` alongside the SKILL line, or correct SKILL.md:1811 to document `--selftest` as 0 all pass, 1 any fail.

Then add a supplemental `command-binding` fixture with stdout `MEASURE_SELFTEST: 0/0 pass` and exit 0 under that expectation, expecting `STDOUT_MISMATCH`. No change to `evaluate()` is needed. This is a registry or ruler edit for the L1 integrator; I made no production edits.

## Bounds and tooling

- **Writes.** This report only. Scratch was limited to `/tmp/rereplay20-c18I`, which holds blob copies and synthetic bundles.
- **Commands not run.** No registry command, suite, gate or selftest was run. Git use was read-only, with `GIT_OPTIONAL_LOCKS=0`.
- **Tooling.** No tools were installed or updated.

R23-REATTACK Replay20: FINDING
