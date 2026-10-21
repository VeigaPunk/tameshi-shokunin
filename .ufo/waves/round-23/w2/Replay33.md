I did not write `.ufo/waves/round-23/w2/Replay33.md`, because this wave's rules forbid all file writes, report included. L1 should persist the findings below.

**Bottom line:** argv and expect for `round19-coldread-selector-selftest` are bound exactly, and the full output is present. One field-level false acceptance is real: the stdout token doesn't bind the pass count. Three metadata fields are copied by the producer rather than observed, and the replay ran at an intermediate revision, not the frozen delivered one.

## Static binding: confirmed exact

- **Same argv and expect everywhere.** argv is `["python3", ".ufo/evidence/round-19/coldread/measure.py", "--selftest"]` and expect is `{"exit": 0, "stdout_contains": ["SELECTOR_SELFTEST: "]}`. These are byte-identical across:
  - `registry-baseline.json` (sha `ebd2e69a…`, which matches `requirements.json.registry_sha256`)
  - `requirements.json` (row 32 of 43)
  - the bundle's requirement and receipt
  - the `observations.json` requirement
  - HEAD's `tools/registry.json`
- **Baseline source.** The row's source is `SKILL.md@55e1d312:1936`. That line documents `--selftest` but not the token, so the token is defined only by the registry row and the format at `measure.py:82`.
- **Registry drift.** Between baseline and HEAD, `tools/registry.json` only added the three `command-binding-*` rows. No existing row changed.

## Evidence: present versus inferred

**Present:**
- The receipt's exit is 0.
- stdout is complete: 145 bytes, 3 CASE PASS lines plus `SELECTOR_SELFTEST: 3/3 pass`. The bundle's `stdout` equals `runner_result.stdout`. stderr is empty.
- The interval is 14:44:54.43–14:44:54.68Z (elapsed 0.244s).
- `registry-C.json`, run at `336565fc`, shows the same text in `stdout_tail`.

**Caveat on completeness:** the output is under the 4096-byte tail limit, so complete and tail capture are identical here. This row doesn't show that complete capture works.

**Inferred, not observed:**
- **Copied fields.** `replay.py:62` sets the receipt's `argv=list(row['argv'])`, `cwd=str(clone)` and `revision=revision` from producer variables. So for the replay bundle, the gate's `ARGV_MISMATCH`, `CWD_MISMATCH` and `REVISION_MISMATCH` checks compare the producer's values with themselves. Nothing re-checks the clone's HEAD after checkout, and the `/tmp` cwd no longer exists.
- **Revision.** The bundle revision is `496d212b`, committed 14:41:18Z, two commits before the frozen `336565fc` (14:47:40Z). The gate only checks receipt revision against bundle revision, and nothing pins the bundle revision to the contract base or the delivered commit.
  - `336565fc` evidence for this row exists only as a tail in `registry-C.json`, outside any binding bundle.
  - That this row's source is the same at both commits rests on file mtimes: `measure.py` 07:10Z, round-18 `measure.py` the day before. That is an inference.
- **Runner digest.** `observations.runner_sha256` hashes the live tree's `tools/registry-check.py`, not the clone copy that actually ran.
- **Base registry.** Whether `registry-baseline.json` equals `tools/registry.json@28cae179` is not verified; I made no git object reads. Its `source_revision` field is self-declared.

**Rejected claims:**
- **Producer authentication.** `replay/expected.json` was written by `replay.py` in the same run. The docstring calls it a "trusted caller-owned commitment", but it is producer-owned. A matching digest shows the file is unchanged since that run, not who produced it.
- **Historical retrofill.** None found. The new invocation fields exist only on newly executed rows. R17-CMD-BIND is not closed by this row.

## False acceptance and adversarial delta

**False acceptance (stdout field).** `"SELECTOR_SELFTEST: "` is a bare prefix. `command-binding.py:109-112` only checks exit equality and a substring, so a receipt with `stdout="SELECTOR_SELFTEST: 0/3 pass\n"` and `exit=0` comes back CLEAN. Only the exit value carries success.

The contrast with the same round's `command-binding-selftest` row, which pins `"38/38 pass"`, shows the prefix is an authoring gap, not a design choice. This is derived from reading the source; I did not execute it.

**Adversarial delta (vacuous pass).** At `measure.py:79-83`, the script returns 0 whenever `passed == len(outcomes)`. If a change drops the three `outcomes.append` calls, it prints `SELECTOR_SELFTEST: 0/0 pass` and exits 0. The registry row, the replay and the gate would all report it held or clean. No field binds the executed script's digest or the case count.

**Impacted axes:** calibration (false acceptance), provenance (revision identity) and identity (runner digest).

## Smallest safe corrections

1. Pin the requirement token to `SELECTOR_SELFTEST: 3/3 pass`. This changes the frozen requirements, so it belongs in the next round, not a retrofit.
2. Have the gate's expected file also pin the revision, and require the bundle revision to match it.
3. In `replay.py`, record the clone's HEAD after checkout and hash the runner from the clone path.
4. Fix the docstring so `expected.json` is described as producer-owned.

Commands used: only read-only file and ref reads, `sha256sum`/`stat`, and in-memory JSON parsing in Python. No registry command, suite, git process or write. No tools installed.
