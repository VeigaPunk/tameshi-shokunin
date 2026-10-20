# ReceiptHarness — round14 w1 (executor)

Status: implementation complete after the parent-directed simplification; the
harness was **not executed** by this seat (no probe, runner, suite, gate,
selftest or target run). Only a Python syntax parse (`ast.parse`) of my own new
file was performed; no behavior check was run. No tool installs or updates. This
report does not call the work independently verified.

## File changed (only)

- `.ufo/evidence/round-14/capture-context.py` — new, 644 lines, 27,577 bytes,
  mode 755, sha256
  `1ffda07bb53a31b34221f5721d5f1ec2853d6cad354115790ade8a7d4c403c93`.
- No shared file, historical evidence, sibling repo, fleet file or registry was
  written. `context-receipt.json` does not exist yet; the harness creates it on
  the L1 run.

## Behavior (bounded core)

Inputs are fixed lane-relative paths; no CLI arguments (any argument except
`-h/--help` is exit 64 and writes nothing):

```text
tools/pin-disposition.py                 probe (read-only)
tools/mutate-and-run.sh                  runner (parsed as text, never executed)
.ufo/evidence/round-13/pin-manifest.json configured pin authority
.ufo/evidence/round-13/expected.json     r13 input digest pin
output: .ufo/evidence/round-14/context-receipt.json (atomic, 0644)
```

Environment leg — exactly two probe runs, baseline then injected, **no retry,
no A-B-A**, identical resolved argv (`which("python3")` recorded), cwd = realpath
lane root, `stdin=DEVNULL`, 120 s timeout each:

- baseline env: ambient with every `GIT_*` key removed, plus `LC_ALL=C`; removed
  key NAMES recorded, never values;
- injected env: a fresh copy of that dict plus exactly
  `{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}`;
- `env_delta_keys`, `injected_env`, `env_delta_matches_declared` and
  `baseline_has_GIT_DIR` are derived from the two dicts actually passed, not
  from the literal; the full environment dict is never serialized
  (`ambient_env_dumped=false`);
- the poison path must be absent (`os.path.lexists`) before any run, else exit 2;
- positive control: `git -C <lane> rev-parse --git-dir` under both envs (30 s),
  full argv/exit/stdout/stderr recorded; `effective` requires baseline exit 0 +
  non-empty stdout and the injected run reflecting the poison (nonzero exit or
  poison path in output), so probe equality is not vacuous.

Comparison — only the **top-level** `observed_at` is removed:

- both documents must parse; the baseline must be a six-leg `pin-disposition-v1`
  `status=ok` document, else exit 2;
- canonical JSON (sorted keys, compact separators) equality; any inequality is
  recorded mismatch (exit 1), including an injected run that exits nonzero or
  emits no JSON;
- `exclusions=["observed_at"]`, both `observed_at` values and
  `raw_stdout_equal` are recorded separately; normalized digests make the
  comparison auditable;
- `payload_tool_sha256_matches_disk` requires both payload `tool_sha256` values
  to equal the pre-run on-disk probe digest. There is no post-run re-hash loop.

Mapping leg — values and variable names, not presence:

- calls are scoped to the `run_regression` body; the six selftest fixture calls
  are outside that body and are not parsed;
- exactly six header rows, six `PIN_*`, six `REV_*` and six calls, with six
  unique and identical leg name sets;
- per leg, five booleans: header repo/path == manifest; `PIN_<X>` name equals
  the declared suffix AND value == `expected_sha256`; `REV_<X>` name equals the
  declared suffix AND value == `pinned_commit`; call leg/repo/path == manifest;
  `PIN_`/`REV_`/`TABLE_` suffixes agree and equal the declared suffix. The name
  check is required because `REV_BASH == REV_CHECKLIST` and
  `REV_JS == REV_CLAIMS`, so a value-only comparison cannot see a swap.

Removed in the simplification (per parent): runner table kill-rate parsing and
counts, probe `CANONICAL_LEGS` third authority, the recursive diff/volatile
taxonomy, the TOCTOU before/after re-hash loop, the duplicated assertions list,
and verbose source/provenance prose.

Exit map (unchanged): **0** equal observation + effective control + exact env
delta + matching source pins + all six mappings; **1** mismatch; **2**
could-not-evaluate; **64** usage error, no receipt.

## Retained evidence at handoff (static only)

Input digests observed before writing (unchanged from the r13 pins):

| Input | sha256 |
|---|---|
| `tools/pin-disposition.py` | `297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11` |
| `tools/mutate-and-run.sh` | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |
| `.ufo/evidence/round-13/pin-manifest.json` | `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` |
| `.ufo/evidence/round-13/expected.json` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` |

Design observation, disclosed: one read-only
`git -C <lane> rev-parse --git-dir` pair was run before the simplification to
choose the control shape — baseline (GIT_* unset) printed `.git` exit 0;
injected `GIT_DIR` exited 128 with
`fatal: not a git repository: '/nonexistent/tameshi-round14-poison'`; the poison
path did not exist (`test -e` exit 1). This is not a harness run and is not a
receipt.

## Risks / limits

- Any inequality, including a sibling commit or worktree change landing between
  the two probe runs, now exits 1 by design (no volatile classification, no
  retry). Inspect `comparison` and the two runs; L1 may re-run manually.
- The poison tests the fail-closed nonexistent-`GIT_DIR` path only; a poison
  pointing at a different valid repo is not tested.
- The declared variable-name table is a static expectation tied to the recorded
  runner; a legitimate re-cut fails closed (runner digest also fails first).
- The runner parser fails closed (exit 2) if the runner text shape changes.
- No runner/leg execution, so no result-reuse claim; `result_reuse` remains
  `not_established`.

## Checks L1 should run (after integration, once)

1. `python3 .ufo/evidence/round-14/capture-context.py` — expect exit 0. Inspect
   `.ufo/evidence/round-14/context-receipt.json`:
   `environment.env_delta_keys==["GIT_DIR"]`,
   `environment.injected_env=={"GIT_DIR":"/nonexistent/tameshi-round14-poison"}`,
   `baseline_has_GIT_DIR==false`, `ambient_env_dumped==false`;
   `runs.argv_equal`/`cwd_equal` true and both run exits 0;
   `comparison.exclusions==["observed_at"]`, `equal==true`,
   `raw_stdout_equal` recorded, `payload_tool_sha256_matches_disk==true`;
   `positive_control.effective==true`; `sources.probe.matches_declared==true`
   and `sources.runner.matches_manifest_declaration==true` with the digests
   above; `mapping.all_match==true`, `mapping.parsed` counts all 6,
   `call_scope.call_count==6`, and every leg's five checks true.
2. Grep the receipt: environment values are only the poison `GIT_DIR` plus the
   four fixed non-secret control constants (`GIT_CONFIG_NOSYSTEM`,
   `GIT_CONFIG_GLOBAL`, `GIT_OPTIONAL_LOCKS`, `GIT_TERMINAL_PROMPT`); no
   `"PATH":`, `"HOME":`, tokens or other ambient values; `ambient_git_keys_removed`
   carries names only.
3. Optional negative control for the REV collision (scratch text only, never
   edit the runner): import the module, call `parse_runner_mapping` on the
   runner text with `"$REV_BASH"` replaced by `"$REV_CHECKLIST"`, then
   `mapping_block(parsed, manifest)`; expect `all_match=false` and
   `bash-surface-census.checks.constant_names_match_leg=false`.
4. Historical identity:
   `git diff --quiet d6809df -- .ufo/evidence/round-13 .ufo/evidence/round-12 tools/pin-disposition.py tools/mutate-and-run.sh`
   (expect 0).
5. No selftest is defined; do not look for one.
