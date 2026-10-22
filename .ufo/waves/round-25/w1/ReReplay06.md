# ReReplay06: round-23 re-attack of the `pin-disposition-read` exact row binding

Lane revision: c9ff09fb41fb8aac5fc335faf10858ff606bd5df (base 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5). Worktree HEAD is 5b69fb2; `tools/registry.json`, `tools/command-binding.py`, `tools/pin-disposition.py` and `tools/registry-check.py` are byte-identical to c9ff09f in the worktree.

## Verdict

FINDING, calibration class. The frozen `expect` for `pin-disposition-read` is not the expect of its cited source. Its extra conjunct `stdout_contains: ["\"unavailable\": 0"]` rejects a state that the cited baseline (SKILL.md@98bea7d:1552) and the tool itself (pin-disposition.py:77-80) both classify as a successfully emitted observation. The frozen expect produces no false acceptance I could find. The one field-level false acceptance I could demonstrate (F2, receipt argv not coupled to output) was already disclosed by round 23.

## Scope and method

- Read: round-23 `requirements.json`, `replay/bundle.json`, `replay/observations.json`, `replay/expected.json`, `replay.py`, `command-binding.py`, `pin-disposition.py`, `registry-check.py` (`run_row`), SKILL.md:1552 (at 98bea7d and in the worktree), registry snapshots at 28cae179, 496d212 and c9ff09f, `registry-baseline.json`, and `source-refresh-final-receipts.json:86`.
- Ran, read-only, in `/tmp` scratch only:
  - `command-binding.py --bundle … --expected … --json` on the frozen bundle, with the 496d212 binder (in `/tmp/rer6-clone`) and the c9ff09f binder.
  - `pin-disposition.py --root /tmp/rer6-empty-fleet`. This is a counterfactual root, not the registry command.
  - The binder on four scratch bundles in `/tmp/rer6-cx`.
- Did not run: the original registry command against the live root, any `--selftest`, `replay.py`, `registry-check.py`, or any suite.
- Git was read-only (`show`, `log`, `diff`, `archive` into `/tmp`). No repo, index or ref writes.
- Installs or updates: none. `RULES.md` was not consulted because nothing was installed.

## 1. Static binding: what holds

| Link | Result | Evidence |
|---|---|---|
| Frozen requirement (name, argv, expect) equals the registry row projection at 28cae179 (registry sha ebd2e69), 496d212, c9ff09f, and `registry-baseline.json` | Exact, 4 of 4 | Computed equality. `replay.py:34-41` enforces the same equality at replay time. |
| Frozen argv equals the SKILL command | Exact | SKILL.md:1552 `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` |
| Frozen exit equals the SKILL verdict "0 observations" | Exact | SKILL.md:1552 |
| Frozen stdout token equals the SKILL verdict map | Not stated by source | SKILL.md:1552 says "0 observations, including changed/unavailable". The token was first added at 2a22ade (round 17), per `git log --reverse -S'\"unavailable\": 0' -- tools/registry.json`. |
| `bundle.requirements` equals `requirements.json` requirements | Exact | Computed. |
| Receipt argv, cwd, revision, exit, stdout and stderr equal the runner observation | Equal | `bundle.json:72-86`, `observations.json:249-293` (row for this name). |
| Receipt stdout is the full stream | Yes: 7452 bytes, equal to `runner_result.stdout`. `stdout_tail` (4096 bytes) is a suffix. stderr is empty. | Computed. |
| `expected.json` pins the bundle bytes | Yes: bundle sha256 3d6c99b7…; expected pins 3d6c99b7… | Binder exit 0 at 496d212 and at c9ff09f. |
| Tool identity | Stdout `tool_sha256` 331529ea… equals the file at 496d212 and in the worktree | sha256 |
| Runner identity | `runner_sha256` cba16646… equals `registry-check.py` in the clone, the worktree, 496d212 and c9ff09f | sha256 |
| Manifest identity | Clone manifest equals worktree manifest (sha256 64eaa43e…) | sha256 |

## 2. F1: frozen expect contradicts its cited source (calibration, latent false failure)

- Cited source (SKILL.md@98bea7d:1552, the `source` field at `registry-baseline.json:123`): verdict map "0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed".
- Tool (pin-disposition.py:77-80): "0 observations emitted, including drift and unavailable legs (this is a probe, not a gate)".
- Frozen expect (`registry-baseline.json:116-121`, `requirements.json:79-85`): `{"exit": 0, "stdout_contains": ["\"unavailable\": 0"]}`. The row is `kind: probe`.

Counterexample, reproduced in `/tmp`:

```
cd /tmp/rer6-clone && python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/rer6-empty-fleet
-> exit 0; "status": "ok"; "counts": {"legs": 6, "unchanged": 0, "changed": 0, "unavailable": 6}; stderr 0 bytes
```

The frozen binder on that output, with only argv re-pointed in both requirement and receipt so that argv matches:

```
python3 command-binding.py --bundle A/bundle.json --expected A/expected.json --json
-> {"exit": 1, "finding_ids": ["STDOUT_MISMATCH"], ...}   (496d212 binder)
-> identical result with the c9ff09f binder (bundle_sha256 484f22ab…)
```

So a baseline-valid observation is a frozen-row failure. The row's current pass (observed at 2026-10-21T14:42:24Z) depends on live sibling state: the row is `external: true` and five of six legs read `changed`. A sibling outage would turn this row red while the probe still exits 0 and the cited source still calls the run an observation.

- Not a false acceptance. The conjunct narrows the pass set: the frozen pass set is a subset of the baseline pass set. No output that passes the frozen expect fails the baseline verdict map.
- Origin. The defect is in the registry authoring at round 17 (2a22ade). Round 23 froze it faithfully, since `replay.py:34-41` requires equality with `registry-baseline.json`.
- Smallest safe correction (not applied; no production edits). Remove the `stdout_contains` conjunct from the `pin-disposition-read` row so that `expect` equals the SKILL.md@98bea7d:1552 verdict map. Re-freeze `requirements.json` and re-run the evidence-only replay through its own pre-check. If a readable-pins gate is wanted, add it as a separate gate row with its own source line.

## 3. F2: receipt argv is a copy, and the binder accepts argv that disagrees with the output (disclosed; confirmed)

- The receipt argv is copied from the row: `replay.py:62` `'argv': list(row['argv'])`, and `replay.py:68` `'argv': o['argv']`.
- The runner executes that same list: `registry-check.py:676-677` `subprocess.Popen(row["argv"], cwd=cwd, …)`. The file is byte-identical at 496d212 and c9ff09f. But `runner_result` carries no argv echo. Its keys are `elapsed_s, expect, got, held, kind, name, non_hermetic_argv, status, stderr, stderr_tail, stdout, stdout_tail, tags`.
- The binder checks receipt argv only against the requirement (`command-binding.py:103-104`). No output field is checked against argv.
- Adversarial delta (control B). Re-point argv in the requirement and in the receipt to `--root /tmp/rer6-empty-fleet`, keep the live stdout (whose `root` field says `/home/vgpnk/Projects/shokunin`), and commit a new expected. Result: exit 0, `finding_ids: []`, at both the 496d212 and c9ff09f binders (bundle_sha256 242991c0…).
- This is the field-level false acceptance I could demonstrate. The disclosure in `source-refresh-final-receipts.json:86` is accurate: "The instrument supplies receipt argv, cwd and revision, so the replay verdict tests only exit and stdout. Argv discrimination rests on the source-read pair and the synthetic cases." The delta needs a caller-committed bundle, and the binder's design checks copy consistency only. This is not a producer-authentication claim.

## 4. Field checks I attempted to break and could not

- Exit: integer only. Bool and float are rejected (`command-binding.py:79, :90`). Frozen exit is 0. Pin-disposition returns 0 only on the success path (`pin-disposition.py:691`) and 2 on invalid input (`:201`).
- Token: the captured stdout is indent-2 JSON. The only key named `unavailable` is `counts.unavailable` (payload keys at `pin-disposition.py:679-689`; leg keys observed in the stdout). A JSON string cannot embed an unescaped `"unavailable": 0` [INFERENCE from JSON escaping rules], so the substring cannot match inside a string value.
- Zero-leg or pinless pass: impossible. The manifest must list exactly the six canonical legs (`pin-disposition.py:620-628, :656-661`). Counts come from `content_status` (`:676-678`). Any unverified pin forces `content_status` to unavailable (`:543-547`). So `unavailable: 0` implies six verified pins and readable worktrees.
- Binder structure: duplicate JSON keys, non-finite constants, extra keys, duplicate requirements or receipts, membership mismatches, and cwd and revision shape are all rejected (`command-binding.py:50-52, :67-68, :76, :89-101`). Stderr cannot supply the token (stdout only, `:111`; selftest case at `:155`).

## 5. Evidence present versus inferred

| Claim | Status |
|---|---|
| Frozen argv and expect exact to registry snapshots (4 of 4) | Present (computed) |
| Frozen expect exact to the SKILL verdict map | Absent. The token contradicts "including unavailable". |
| Full stdout (7452 bytes) retained and equal to runner stdout; tail is a suffix | Present |
| Exit 0 retained | Present (runner `got` 0; bundle `exit` 0) |
| Tool and runner identities | Present (sha256 match) |
| Manifest read from the clone | Present (stdout `manifest` field is the clone path) |
| Probe root is the live fleet | Present (stdout `root`; `non_hermetic_argv`; `replay.py:51-53` symlinks live siblings) |
| Revision 496d212 is the clone checkout | Present by construction (`replay.py:32-33, :50`) |
| Revision 496d212 is the revision the content was read at | Not established. The root is live, the row is `external: true`, and five of six legs are `changed`. |
| Receipt argv is the argv that was executed | Inferred (copy at `replay.py:62, :68`; `Popen(row["argv"])` at `registry-check.py:676-677`; no echo in `runner_result`) |
| `observed_at` 2026-10-21T14:42:24Z falls inside the window | Present (tool-stamped; row window 14:42:24.157–14:42:24.279 UTC) |
| The six pins are verified | Present as recorded in stdout. Not recomputed here. |
| `observations.json` metadata (`measurement_interval`, `registry_sha256`, `runner_sha256`) | Unsigned. Not pinned by `expected.json` or the binder. |
| Producer authenticity | Not claimed and not established |

## 6. Retrofill check (historical metadata)

- Committer times are -0300. Commit 496d212 is at 11:41:18 (14:41:18 UTC) and contains no bundle, expected or observations file (empty-file sha). The run window is 14:42:22.6–14:44:58.8 UTC.
- The bundle, expected and observations files first appear in 8f66b5d and 54c14ea, both at 11:46:12 (14:46:12 UTC), after the window closed. The bundle sha256 3d6c99b7… is identical in both commits and in the worktree. No commit after those touches these paths.
- This establishes ordering only. It does not establish who wrote the observation rows. `replay.py:4-6` says it never fills fields into historical observations. I did not audit that claim beyond these paths.

## 7. Lane revision c9ff09f

- The row is identical at c9ff09f: same argv, expect, source and tags; `status: active`; no successor row. The only `pin-` rows are `pin-disposition-read` and `pin-disposition-selftest`.
- `command-binding.py` changes from 496d212 to c9ff09f only in selftest hunks (`@@ -164`, `@@ -166`). `evaluate` and `check` are unchanged.
- `pin-disposition.py` and `registry-check.py` are byte-identical across 496d212, c9ff09f and the worktree.
- SKILL.md:1552 is unchanged in the worktree.
- F1 and F2 reproduce at c9ff09f (results above).

## 8. Residual risk and verification gaps

- Current live fleet state was not measured. The pass at 14:42 is a historical observation only.
- Not run: the original registry command, all selftests, `replay.py`, `registry-check.py`, the 42 other rows, and `verify-round15`.
- Pinned blobs in sibling repos were not recomputed.
- The requirement projection drops `external`. `replay.py:39` keeps only name, argv and expect, and `command-binding.py:76` forbids extra keys, so the binder cannot distinguish live rows from hermetic ones. The round-23 correction discloses the two live rows.
- `observations.json` is outside both the binder and `expected.json`.
- No producer-authentication assessment was made. The `command-binding.py` docstring disclaims it.

R23-REATTACK Replay06: FINDING
