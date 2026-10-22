# ReReplay16 — re-attack of round-23 Replay16 (row `context-capture-selftest`)

Verdict: the static exact binding of this row holds, both on the frozen round-23 artifacts and at lane
revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. I found no field-level false acceptance. The
required adversarial delta is a real weakness of the row's expectation (the `SELFTEST: PASS` token
carries no case count), but the binder enforces exactly what the row declares, so it is not a false
acceptance of this receipt.

## What was checked (round-23 frozen artifacts)

1. **Frozen requirement vs baseline source.** `.ufo/evidence/round-23/requirements.json` row
   `context-capture-selftest` = `argv ["python3","tools/context-capture.py","--selftest"]`,
   `expect {exit:0, stdout_contains:["SELFTEST: PASS"]}`. This is byte-for-byte the name/argv/expect
   projection of the `tools/registry.json` row at source_revision 28cae179 (registry blob 9315c7e,
   sha256 `ebd2e69a…` = `registry_sha256` in requirements.json and observations.json). The registry
   row's `source` is `SKILL.md@98bea7d:1680`; that SKILL.md table row names the self-test command
   `python3 tools/context-capture.py --selftest`. The argv matches. The token `SELFTEST: PASS` is not
   spelled out in that SKILL line; it comes from the registry row, not from the SKILL text.
2. **Bundle integrity.** `sha256(replay/bundle.json)` = `3d6c99b7…50b9` = `replay/expected.json`.
   I ran the binder in /tmp scratch on copies (not the registry command, not a suite):
   `python3 /tmp/rr16-scratch/cb-496d212.py --bundle bundle.json --expected expected.json --json`
   gave `{"exit": 0, "finding_ids": [], …}`, exit 0.
3. **Field-by-field, this row.** bundle requirement == frozen requirement == observations `requirement`.
   receipt argv == requirement argv == observations argv. receipt cwd == bundle cwd ==
   `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`. receipt revision == bundle revision ==
   `496d212b…`. receipt exit 0 == runner_result `got` 0 == expected exit 0. stderr is empty in both.
4. **Full output, not tails.** The receipt stdout is 5201 chars and 50 lines, and it equals
   observations `runner_result.stdout` exactly. `stdout_tail` (4096 chars) is a strict suffix of it.
   It contains no U+FFFD (the runner decodes with `errors="replace"`, registry-check.py:717,725, so
   no replacement happened). It has 49 `SELFTEST_CASE … OK` lines, 0 FAIL lines, and the final line
   is `SELFTEST: PASS (49/49)`, which is the only occurrence of the token.
5. **Source cross-check (496d212 `tools/context-capture.py`, blob 992d0a3, identical at 28cae179 and
   c9ff09fb).** `finish()` (lines 1779–1786) prints `SELFTEST: PASS (passed/total)` and returns 0
   only when `self.failed` is empty. Every other path prints `SELFTEST: FAIL` and returns 1 or 2
   (lines 1780–1784, 2200–2203). The only echo of child stdout is `SELFTEST_STDOUT` on failure
   (1741–1744), and it comes from `--check` children, which do not print the token. In the genuine
   program, the token plus exit 0 therefore implies a full pass. Statically there are 47
   `harness.check_case/usage_case` calls plus 2 hermetic records in `finish()`, which is 49 and
   matches `49/49`.

## Evidence present vs inferred

- **Present (observed):** exit code and complete decoded stdout/stderr, captured from
  `subprocess.Popen` in `registry-check.py:run_row` (676–726), plus the per-row measurement interval.
- **Inferred, not observed:** the receipt fields `argv`, `cwd` and `revision` are not read back from
  the child process. `replay.py:62,66–69` copies them from `row['argv']`, `str(clone)` and the
  `rev-parse` result. The ARGV, CWD and REVISION checks therefore agree by construction for any
  replay-produced bundle. They agree with the actual invocation only through code reading:
  `Popen(row["argv"], cwd=cwd)` at registry-check.py:676–683, and `git checkout --detach revision`
  with `check=True` at replay.py:50. Nothing reads the clone HEAD back after checkout. The concrete
  `python3` that PATH resolved (from `git_env()`) and its version are not recorded.
- **Runner digest:** `runner_sha256 cba16646…` is the hash of the live working-tree
  `tools/registry-check.py` (replay.py:78), not the clone copy that was executed (replay.py:54). The
  two coincide here, because `git show 496d212:tools/registry-check.py | sha256sum` gives `cba16646…`
  (the same value at 8f66b5d and c9ff09fb). So this is no false provenance for this run, but the
  field hashes the wrong file by design.
- No producer authentication is claimed or implied; the binder docstring disclaims it
  (command-binding.py:13–15). Nothing in observations.json fills historical metadata: the invocation
  fields sit beside a newly executed row with its own interval (14:42:29.71–14:42:31.06Z, inside the
  run interval).

## Concrete adversarial delta

The expectation is an unanchored substring with no count, so a selftest regression that deletes cases
still binds CLEAN. Genuine path: remove cases from `run_selftest_cases` (or have it return early). It
still reaches `finish()`, `self.failed` stays empty, and it prints `SELFTEST: PASS (2/2)` with exit 0.
`registry-check.run_row` then marks the row `held` (720), and the binder accepts it. I demonstrated the
binder side in /tmp scratch: I re-pinned copies of the bundle with only this row's stdout changed.

| receipt stdout / exit (only this row changed) | 496d212 binder | c9ff09fb binder |
|---|---|---|
| `…\nSELFTEST: PASS (2/2)\n`, exit 0 | exit 0, `[]` (accepted) | exit 0, `[]` (accepted) |
| `SELFTEST: FAIL (1/49 failed: clean)\nSELFTEST: PASS\n`, exit 0 | exit 0, `[]` (accepted) | exit 0, `[]` (accepted) |
| `SELFTEST: FAIL (1/49 failed: clean)\n`, exit 0 (control) | exit 1, `STDOUT_MISMATCH` | exit 1, `STDOUT_MISMATCH` |
| original stdout, exit 1 (control) | exit 1, `EXIT_MISMATCH` | exit 1, `EXIT_MISMATCH` |

The second row cannot come from the genuine program (see source item 5). It needs a fabricated
receipt, so it falls under the disclaimed producer-authenticity gap. The first row is reachable by a
real source mutation. Because the binder enforces the declared `stdout_contains` correctly, both rows
are weaknesses of the expectation, not field-level false acceptances by the binder. I did not run
`context-capture.py --selftest` or a mutated copy of it (the original item forbids running the
registry command), so whether a mutant really reaches the registry runner is `[INFERENCE]` from
source lines 1779–1786 and 720.

Impacted axes: calibration (the row's token strength). No identity change and no duplicate authority.

Smallest safe correction: pin the count as well. Either set `stdout_contains` to
`["SELFTEST: PASS (49/49)"]`, or keep `SELFTEST: PASS` and add `(49/49)` as a second required token.
This must be a new registry row revision or successor row, not an edit to the frozen round-23
requirements. It must be re-pinned whenever the case count legitimately changes.

## Status at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df

- In `tools/registry.json` (blob 60a6ff5, 54 rows), the `context-capture-selftest` row is unchanged:
  same argv, expect, timeout 60, source, `active`. It is not superseded.
- `tools/context-capture.py` is unchanged (blob 992d0a3).
- `tools/command-binding.py` changed only in `selftest()` (lines 164–169 now load the round-23 and
  round-24 `extra-cases.json`). `evaluate()` and `check()` are byte-identical in logic, and the table
  above shows identical results from both versions.
- The round-24 replay (`.ufo/evidence/round-24/replay/bundle.json`, revision d2eaecd) shows the same
  requirement, exit 0 and a final line of `SELFTEST: PASS (49/49)`.
- The binding still holds, and the count-free-token delta still applies unchanged. Neither
  `tools/registry.json` nor `.ufo/evidence/round-25/multitoken-cases.json` contains a count-pinned
  token for this row.

## Bounds and tooling

- The only writes are this report and scratch files under `/tmp/rr16-scratch` and `/tmp/rr16-*.py`.
  The only git commands were read-only (`GIT_OPTIONAL_LOCKS=0`: show, log, diff, rev-parse,
  cat-file). No gate, selftest, suite or registry command was run, and nothing was run in the lane.
- Tools installed or updated: none.

R23-REATTACK Replay16: AGREE
