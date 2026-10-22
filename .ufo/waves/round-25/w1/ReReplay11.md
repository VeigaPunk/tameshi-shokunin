# ReReplay11: R23 re-attack of row `evidence-disposition-round18-before`

## Verdict

AGREE. The static binding for this row holds on every frozen byte and still holds at lane revision c9ff09fb.

- The row's binding fields (argv, expect, cwd, revision, exit, full stdout) show no field-level false acceptance.
- Two deltas the standalone gate accepts (D8 reason-only change, D9 consistent argv swap) are closed at registry level by the active digest-pinned row `registry.json:971`. That closure is by code reading and row content; I did not execute it.
- One gap sits outside the row's binding. The retained invocation metadata in `replay/observations.json` is pinned by nothing (D10). Its values match today, but nothing would detect an edit. I treat this as a traceability residual, not a counterexample to the row binding.
- Producer authenticity is not claimed. `expected.json` is written by the same replay run as the bundle.

## Scope and method

- Read-only. No registry command, selftest, or suite was run. No lane files were written. No git write commands were run.
- Scratch files are in `/tmp/r23-reattack-replay11/` (blobs from `git show`, read-only git with `GIT_OPTIONAL_LOCKS=0`). Mutation copies are in `/tmp/r23-reattack-replay11/mut/`.
- The lane HEAD is `5b69fb2`, a descendant of c9ff09fb. I assessed the c9ff09fb blobs explicitly and did not assess HEAD.
- Tools installed or updated: none. `python3` was already present.

## 1. Frozen row against baseline (exact)

Frozen row (`round-23/requirements.json:168` is the name line):
- argv: `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json`
- expect: exit 1, `stdout_contains` = [`"expectation": "producer_before"`, `"status": "failed"`]

Observed on the frozen files (Python equality checks, all True):
- Frozen row equals the active baseline row (`round-23/registry-baseline.json:280`).
- `requirements.json` `registry_sha256` `ebd2e69a…` equals sha256 of `registry-baseline.json`.
- `actual-source-read.json` holds `cat tools/registry.json` at 496d212; its stdout hashes to `ebd2e69a…`, so the registry is byte-identical to the baseline. The row in it equals the frozen row.
- `replay/bundle.json` requirement row (`:764`) equals the frozen row. The bundle's full requirements list equals the frozen list.
- `tools/registry.json` at c9ff09fb: row at line 280 is `active`, has no `superseded_by`, and its argv and expect equal the frozen row. The file has 54 rows and no duplicate names.

## 2. Retained invocation metadata and full output

- Receipt (`bundle.json:157`, stdout line `:160`) versus observation (`observations.json:504` requirement, `:513` runner_result): argv, cwd, revision, exit (1), stdout, and stderr are all equal.
- Full stdout is 6307 characters. `stdout_tail` is the last 4096 characters, starting at offset 2211.
- The `"expectation": "producer_before"` token is at offset 1357, outside that tail. The `"status": "failed"` token is at offset 6029, inside it. A tails-only capture would false-reject this row (see D6).
- The stdout parses as JSON. Top-level `status` is `failed`, `exit` is 1, and there is one finding: `{"id": "expected_contains_missing", "expectation": "producer_before"}`. Each token occurs exactly once.
- Runner record: `held` true, no `cleanup_error`, no `non_hermetic_argv`, no `stdout_missing`. `elapsed_s` 0.106 matches `measurement_interval` 14:42:26.655775 to 14:42:26.762256.
- The runner passes the row's argv unchanged: `registry-check.py:676-684` calls `Popen(row["argv"], cwd=cwd, …, env=row_env())`. Token checks run on the full decoded stdout (`:717-720`).

## 3. Gate field exactness (`tools/command-binding.py`)

Field checks in the c9ff09fb blob: argv `:103-104`, cwd `:105-106`, revision `:107-108`, exit `:109-110`, stdout tokens `:111-112`. Pin check `:125-126`. The r23 and c9ff09fb blobs have identical `evaluate`/`check` code; `git diff` touches only selftest lines `161-172`.

Frozen bundle, run from `/tmp` copies:
- `python3 command-binding.r23.py --bundle bundle.json --expected expected.json --json` gives `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": [], …}` with exit 0.
- The c9ff09fb blob gives identical output.

Mutation results. Each mutated bundle had its `expected.json` regenerated as the caller pin. Both tool blobs gave identical results.

| case | delta | result |
|---|---|---|
| D0 | none | exit 0, `[]` |
| D1 | receipt argv `dispositions-before.json` to `dispositions.json` | exit 1, ARGV_MISMATCH |
| D2 | receipt exit 1 to 0 | exit 1, EXIT_MISMATCH |
| D3 | receipt cwd to `/tmp/other-clone` | exit 1, CWD_MISMATCH |
| D4 | receipt revision to `d`×40 | exit 1, REVISION_MISMATCH |
| D5 | drop `"status": "failed"` from receipt stdout | exit 1, STDOUT_MISMATCH |
| D6 | receipt stdout = last 4096 chars only | exit 1, STDOUT_MISMATCH |
| D7 | stdout empty, full text moved to stderr | exit 1, STDOUT_MISMATCH |
| D8 | finding id and detail changed to another failure; both tokens kept | exit 0, `[]`. Accepted |
| D9 | argv swapped consistently in requirement and receipt | exit 0, `[]`. Accepted |
| D10 | `observations.json` row argv and `held` edited; bundle and expected untouched | exit 0, `[]` on both tools. Accepted (gate never reads the file) |

Closure for D8 and D9 at registry level (by code reading; not executed):
- `registry.json:971` (`command-binding-frozen-clean-pinned`, active at c9ff09fb) requires `"bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9"` in stdout.
- Any byte change to the bundle changes that digest.
- `registry-check.py:718-720` sets `held = False` when a needle is missing.
- The superseded rows at `registry.json:939` and `:950` lack the digest token and close nothing.

Baseline equality is not enforced by the gate. The gate checks receipts against the bundle's own requirements. Baseline equality is enforced at generation time by `replay.py:37` and `:41`, and was verified by hand in section 1.

## 4. Present versus inferred

| item | status | basis |
|---|---|---|
| Frozen argv and expect | present, exact | section 1 |
| Receipt argv, exit, stdout, stderr | present, pinned | `bundle.json` hashes to the pin `3d6c…` in `expected.json`. `expected.json` (`0831c9c8…`) is cited in `final-verification.json` and `RunReplayGate.md:38` |
| Receipt cwd | string only; not observed | the clone `/tmp/tameshi-r23-replay-naxu6fzi` is gone; `replay.py:49` |
| Receipt revision | checkout succeeded (`replay.py:50`, `check=True`); not re-observable | clone gone |
| Executed argv | declared; passed verbatim to `Popen`; no OS exec record (pid, exe) | inferred from code (`registry-check.py:676-684`) |
| Interpreter (`python3`) and env | not recorded. Env is the `git_env` scrub plus `PYTHONDONTWRITEBYTECODE` (`registry-check.py:149-173`) | inferred |
| Disposition tool identity | observed. The tool hashes its own file at run time (`evidence-disposition.py:136`, `:211-216`, emitted at `:1438`). Value `39ee5c5e…` at both revisions | observed |
| `observations.json` metadata (argv copy, cwd, revision, `measurement_interval`, `held`, `runner_sha256`, `registry_sha256`) | present and consistent today. Pinned by nothing: sha `a83d8a0b…` appears in 0 files under `.ufo` and 0 registry rows | inferred from an unpinned file |
| `runner_sha256` | value `cba16646…` equals the live tree file and the clone blob at 496d212. But `replay.py:78` hashes `args.repo`, not the executed clone copy | value matches; provenance differs |
| `expected.json` authenticity | not established. `replay.py:73-75` writes bundle and expected in the same run (self-pin) | rejected as authenticity evidence |

## 5. Status at lane revision c9ff09fb

- The row is active at `registry.json:280`. Its argv and expect are unchanged, and it is not superseded.
- `command-binding.py` changed only in selftest fixture loading (lines `161-172`). The round-24 fixture list is present at c9ff09fb. The field checks in section 3 apply unchanged.
- These blobs are identical at c9ff09fb and in the lane tree: the eight audited round-23 artifacts (`requirements.json`, `registry-baseline.json`, `replay/bundle.json`, `replay/expected.json`, `replay/observations.json`, `actual-source-read.json`, `replay.py`, `final-verification.json`). Also identical: `registry-check.py` (sha256 `cba16646…`), `evidence-disposition.py` (sha256 `39ee5c5e…`), and `dispositions-before.json` (git blob `495ee072…`, sha256 `dc948a5e…`), plus the round-13 and round-14 inputs.
- The per-row held state at c9ff09fb is inferred from identical blobs. I did not observe it, because that would run the registry command.
- The round-23 finding that "the registry does not enforce frozen" (`RevisionDeclared.md:11-13`) still applies to the superseded row at `:939`. It is closed for the active row by `:971`.
- D10 applies unchanged at c9ff09fb.

## 6. Historical retrofill

None found for this row.
- `measurement_interval` appears 0 times in `registry-baseline.json` and `requirements.json`.
- Its appearances are all in round-23 capture artifacts.
- `replay.py:62` adds invocation fields only to newly executed rows.
- The round-18 input `dispositions-before.json` has the same git blob (`495ee072…`) at 496d212 and c9ff09fb.

## Smallest safe correction (not applied; audit only)

1. Close D10. Pin the sha256 of `observations.json` (`a83d8a0b…`) in a registry row, as `registry.json:971` does for the bundle. Alternatively, have `command-binding` cross-check each observations row's argv, cwd, revision, got, and stdout against the receipt with the same name.
2. Record interpreter identity (`sys.executable` and version) and an env digest in each observations row.
3. At `replay.py:78`, hash the executed clone file rather than `args.repo`.
4. Optional, outside audit scope: add a finding-level token (for example `"id": "expected_contains_missing"`) to this row's needles. That changes the frozen requirement set and needs re-freezing.

## Residual risk and verification gaps

- No fresh execution at c9ff09fb. Per-row held state there is inferred from identical blobs.
- The closure of D8 and D9 at `registry.json:971` is by code reading, not execution.
- The selftests for `command-binding` and `evidence-disposition` were not run, per the bounds.
- The replay clone is deleted, so cwd and revision cannot be re-observed from the bundle alone.
- Producer authenticity is neither claimed nor tested.

R23-REATTACK Replay11: AGREE
