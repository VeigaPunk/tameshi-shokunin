# ReReplay27 — re-attack of round-23 wave-2 Replay27 (`assemble-round17-selftest`)

## Verdict

FINDING. The round-23 receipt does match the frozen requirement exactly on argv, cwd,
revision, exit and the stdout token. That part holds. Two things in this row still accept
something false, and both apply unchanged at lane revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`.

1. **The `source` provenance is false (field-level false acceptance).** The registry row cites
   `source: "SKILL.md@98bea7d:1806"`. At `98bea7d`, `.ufo/evidence/round-17/coldread/assemble.py`
   does not exist yet: `git ls-tree -r --name-only 98bea7d -- .ufo/evidence/round-17/coldread/assemble.py`
   prints nothing. At that revision `SKILL.md` never mentions `round-17/coldread/assemble` or the
   needle `SELFTEST: all checks passed`. Line 1806 is the heading `### Round-16 gate/probe registry`.
   The nearest table row (line 1812) documents `round-16/coldread/assemble.py` with exit semantics
   only and no stdout token. `tools/registry-check.py` accepts this field because it only checks the
   shape against `SOURCE_RE` (`registry-check.py@c9ff09f:257-262`) and never resolves the anchor.
2. **Adversarial delta: a failing-selftest stdout binds CLEAN.** `stdout_contains` only tests that the
   substring is present (`command-binding.py:111`). A receipt that keeps exit 0 and the banner but
   carries `[FAIL]` check lines is accepted by both the round-23 and the lane versions of the gate.

## Scope checked

- Frozen requirement (`.ufo/evidence/round-23/requirements.json`, 43 rows):
  `argv ["python3", ".ufo/evidence/round-17/coldread/assemble.py", "--selftest"]`,
  `expect {"exit": 0, "stdout_contains": ["SELFTEST: all checks passed"]}`. This is identical in
  `replay/bundle.json` `requirements`.
- Baseline source: `requirements.json.registry_sha256 = ebd2e69a…c92a`. This equals
  `sha256(git show 28cae17:tools/registry.json)` and `sha256(git show 496d212:tools/registry.json)`,
  and `replay.py:35-41` refuses to run unless the projection equals the frozen list. The registry
  row at `28cae17` has the same argv and expect, plus `timeout_s 120`, `kind selftest`,
  `source SKILL.md@98bea7d:1806` and `tags ["new-r17"]`.
- Receipt in `replay/bundle.json`: argv equal; `cwd /tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`
  equals the bundle cwd; `revision 496d212b…4182963` equals the bundle revision; `exit 0`;
  `stderr ""`; `stdout` is 7,280 B.
- Full stdout, not the tail: the bundle stdout is byte-equal to `observations.json` `runner_result.stdout`
  (the tail is retained separately as `stdout_tail`, 4,094 B). It has 77 `[ok]` lines, 0 `[FAIL]` lines,
  and its last line is `SELFTEST: all checks passed`. The banner prints only when `failures` is
  empty (`assemble.py:1792-1796`), and `check()` appends every false condition before the banner
  (`assemble.py:1010-1013`).
- Digest: `sha256(replay/bundle.json) = 3d6c99b7…0b9`, which equals `replay/expected.json`.

## Evidence present versus inferred

- **Present (retained bytes):** the complete stdout and stderr, the exit (`got 0`), the
  `measurement_interval` (14:44:47.858 to 14:44:48.028 UTC) and `elapsed_s 0.17`.
- **Declared, not observed:**
  - The receipt `argv` is `list(row['argv'])` (`replay.py:62`), not the process's recorded args.
    `run_row` passes `row["argv"]` straight to `Popen` (`registry-check.py@496d212:676-677`), so the
    two are equal by reading the code, not by observation.
  - The receipt `cwd` and `revision` are copied from the same variables as the bundle-level fields
    (`replay.py:62,66`). In this bundle, `ARGV_MISMATCH`, `CWD_MISMATCH` and `REVISION_MISMATCH` are
    therefore true by construction. They are not independent checks.
  - The revision comes from `rev-parse` on the source repo (`replay.py:32`), followed by
    `checkout --detach` with `check=True` (`replay.py:50`). The clone's HEAD is never re-read.
  - The clone `/tmp/tameshi-r23-replay-naxu6fzi` no longer exists, so none of this can be re-observed.
  - `observations.runner_sha256` hashes the live `args.repo/tools/registry-check.py` (`replay.py:78`),
    not the clone copy that actually ran. Its value `cba16646…44ad` does equal the `496d212` blob, so
    the provenance holds, but only by coincidence. Round 24 renamed this field to
    `runner_sha256_clone_copy`.
- **No producer authentication** is claimed or available (`command-binding.py` docstring).
- **No historical metadata retrofill:** the invocation fields are attached only to rows that this
  run executed (`replay.py:5-6,62`). The bundle landed in `8f66b5d`, 5 minutes after `496d212`.

## Counterexample commands and observed output (scratch `/tmp/rr27`, read-only toward the lane)

The gate was taken from `git show 496d212:tools/command-binding.py` and
`git show c9ff09f:tools/command-binding.py`. Only the target receipt was edited, and each case got
its own digest-pinned expected file.

```
frozen-as-is                 cb-496d212 rc=0 finding_ids []   | cb-c9ff rc=0 finding_ids []
A token-only (0 checks)      cb-496d212 rc=0 finding_ids []   | cb-c9ff rc=0 finding_ids []
B 2x "[FAIL] …" + banner     cb-496d212 rc=0 finding_ids []   | cb-c9ff rc=0 finding_ids []
C "SELFTEST: FAIL (2 checks)\nSELFTEST: all checks passed"
                             cb-496d212 rc=0 finding_ids []   | cb-c9ff rc=0 finding_ids []
D "not SELFTEST: all checks passed"
                             cb-496d212 rc=0 finding_ids []   | cb-c9ff rc=0 finding_ids []
control token on stderr      rc=1 ["STDOUT_MISMATCH"] (both)
control exit 1               rc=1 ["EXIT_MISMATCH"]   (both)
```

Case B is the stdout that a one-edit mutant of `assemble.py` would produce if it deleted the
`if failures:` block at lines 1792-1794: the failing checks still print `[FAIL]`, and then the banner
prints with exit 0. [INFERENCE] I did not run the mutant, because the item forbids running the suite.

Provenance commands:

```
$ git show 98bea7d:SKILL.md | sed -n 1806p
### Round-16 gate/probe registry
$ git show 98bea7d:SKILL.md | rg -n 'round-17/coldread/assemble|all checks passed'
(no output)
$ git log --reverse --format=%h -S'"assemble-round17-selftest"' -- tools/registry.json | head -1
2a22ade          # row introduced here, with source SKILL.md@98bea7d:1806
$ git show 2a22ade:SKILL.md | rg -n 'round-17/coldread/assemble.py'
1888, 1903       # 1903 = the "Round-17 gate/probe registry — input-keyed credit" table row
$ git show 2a22ade:.ufo/evidence/round-17/coldread/assemble.py | rg -n 'all checks passed'
1499
```

The same `98bea7d:1806` anchor is also used by four sibling rows introduced in `2a22ade`:
`evidence-disposition-round17-before`, `registry-check-selftest`, `measure-round17-selftest` and
`trace-inputs-round17-selftest`. I did not audit those rows.

## Status at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df

- `tools/registry.json` changed (`a8f255f1…`, 54 rows), but this row is byte-identical in content:
  same argv, expect and `source SKILL.md@98bea7d:1806`, `status active`, not superseded.
- `assemble.py` blob is unchanged (`8bcce2ea…` at `28cae17`, `496d212` and `c9ff09f`).
- `tools/command-binding.py` changed (`d533dc1e…` → `9230c68e…`), but the diff only touches selftest
  fixture loading (it adds `round-24/extra-cases.json`). `evaluate()` is unchanged, and the run
  above shows identical results.
- The source check in `registry-check.py@c9ff09f` is still regex-only (lines 257-262).

Both findings still apply.

## Impacted axes

- **Calibration:** the `source` field asserts provenance that the cited bytes do not contain.
- **Acceptance soundness:** a stdout that contains failures can bind CLEAN. The exit code is the
  only guard, and it fails exactly when the failure branch is removed.
- **Identity:** the receipt's cwd, revision and argv are declared, not independently observed.

## Smallest safe correction

1. Re-anchor this row's `source` to `SKILL.md@2a22ade:1903` through a new registry or contract
   revision. Do not edit the frozen round-23 artifacts. Then make `registry-check.py` resolve the
   anchor (`git show <rev>:<file>` succeeds and the line number is in range) instead of only
   checking its shape. This is a fixable defect.
2. The token weakness is a tradeoff in the `command-binding-v1` schema, which has no negative
   needles. No positive-only `stdout_contains` set closes it. The smallest safe closure is to add
   an optional `stdout_absent` list (for this row: `["[FAIL]", "SELFTEST: FAIL"]`) to both
   `registry-check` and `command-binding`. Alternatively, require the banner to be the final line.
   Either needs a new contract revision, and it belongs with the R23-ROUTED-1 multi-token fixture
   line of work.

## Tooling

No tools were installed or upgraded. Scratch files exist only under `/tmp/rr27`.

R23-REATTACK Replay27: FINDING
