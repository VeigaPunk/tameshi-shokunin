# EnvironmentCritic — round14 w1 (critic, read-only)

Scope: attack the claim that the pin probe's GIT_* scrub makes its output equal across baseline and injected environments, and attack the planned `capture-context.py` receipt. **`.ufo/evidence/round-14/capture-context.py` does not exist yet** (glob at review time found only `before.json`, `sources-before.json`, `measure.py` and `claims.json`). So this is a review of the **retained contract only**. No harness behavior is claimed. I ran no checks, probe, runner, selftest or gate. I ran no targets. Only reads were done: file reads, `sha256sum`, `git rev-parse`/`status`/`log -1` on siblings, and ambient `GIT_*` **names** (no values). Tool installs: none.

## Facts observed (round13 evidence, unchanged bytes)

- `verification.json` `pin_live` and `pin_env_scrub` have **identical argv** (`python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`). They have the same key set `{argv, exit, exit_matches, expected_exit, name, started_at, stderr, stdout}`. Neither has a cwd or env field. Nothing in the receipt tells the two rows apart except `name` and `started_at` (26.903956 versus 26.952682, 49 ms apart).
- Parsed stdout is equal with `observed_at` removed **and also raw-equal**: both runs have `observed_at` `2026-10-20T04:59:26Z`, the same second. So round13 never actually tested the "exclude observed_at" rule.
- `verification-verdict.json:67 git_environment_scrub_equal: true` is an equality claim with no recorded injection. This matches routed item 2 of the r13 spot-check.
- Current digests match the round13 pins:
  - probe `2972539…f11`
  - runner `75ed934…dc5`
  - manifest `64eaa43…af6`
  - Lane HEAD is `d6809df`.
  - Only `.ufo/evidence/round-14/` and `.ufo/waves/round-14/` are untracked.
- Probe code:
  - `git_env()` (pin-disposition.py:197-211) removes every inherited `GIT_*` and passes `env=` to every run-mode git call (:217-223).
  - `run_mode` **always returns 0** (:565-589), even when all six rows are `unavailable`.
  - A repo-identity failure produces an `unavailable` row, not an error exit (:406-435).

## Counterexamples and corrections

### E1 — Injection that never reaches the probe (the round13 failure mode, reborn) — **blocker for the claim**
**Counterexample:** a harness writes the literal `injected_env={"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` into the receipt but passes a different object to `subprocess.run`, or none at all (`env=None`, `os.environ`, or a copy built before the update). Baseline and "injected" would be byte-equal, and the receipt would still show the injection. Equality cannot tell "scrub works" apart from "poison never delivered".

**Smallest safe correction (ReceiptHarness):**
- Build each env dict once and pass that same object.
- Derive the receipt fields from the dicts that were actually passed:
  - `env_delta_keys = sorted(k for k in injected.keys() ^ baseline.keys() | {k for k in baseline if baseline[k] != injected.get(k)})`, required to be `["GIT_DIR"]`
  - `injected_env = {k: injected[k] for k in env_delta_keys}`
- Assert that `GIT_DIR` is absent from the baseline dict.
- Optional, needs scope approval from Main/ReceiptHarness: add a **positive control**. Run read-only `git -C <lane> rev-parse --is-inside-work-tree` under the injected env **without** scrubbing (expected nonzero) and under the baseline env (expected 0). This shows the poison actually works. Without it, the receipt should say "delivery proven by construction (env= dict), not by an unscrubbed control".

**Axes:** calibration (false provenance), depth.

### E2 — Exit-code equality is not evidence
Even if the scrub failed, the probe would exit 0: `git -C repo` with `GIT_DIR=/nonexistent` → `repo_not_git` → all six rows `unavailable`, `status:"ok"`. `exit_matches` and `baseline_exit == injected_exit` carry **zero** discriminating weight.

**Correction:** the receipt must record exit codes, but the comparable predicate is the JSON. It should additionally record `injected.counts.unavailable == 0` and per-leg `content_status` equality. That makes the specific failure signature visible. A mismatch must not be summarized as an exit verdict.

**Axes:** calibration.

### E3 — Exclusion broader or narrower than `observed_at`
**Counterexamples:**
- **Recursive strip:** a recursive `observed_at` strip, or a strip of every `*_at`/timestamp field, would hide a future nested field. Today there is exactly one `observed_at`, at top level (key census: `observed_at: 1`).
- **Parse failure:** if either stdout fails to parse, a harness that reports `equal=false` instead of could-not-evaluate turns a tooling error into a scrub verdict.

**Correction:**
- Drop only the top-level `observed_at`.
- Compute `differing_paths` over the full parsed trees and require `differing_paths ⊆ {"/observed_at"}`.
- Record both `observed_at` values and `raw_stdout_equal` separately.
- A parse failure or a missing top-level `observed_at` means could-not-evaluate, not a mismatch.
- Compare the parsed objects. Also keep the raw bytes or their sha256 so the receipt can be audited without re-running.

**Axes:** calibration.

### E4 — Moving siblings between the two runs (live hazard **now**)
**Current state versus the round13 recorded HEADs:**

| Sibling | Recorded HEAD | Current HEAD | Notes |
|---|---|---|---|
| kumitate | `1770305` | `1770305` | clean |
| kagi | `c2cab35` | `c2cab35` | clean |
| tsukuroi | `9574a18` | **`8606bad`** | worktree **dirty: 11 modified + 5 untracked**; `tools/tsukuroi-census.sh` itself is not dirty |
| mado | `59cfbdc` | **`97c3583`** | clean; index mtime ≈ 06:10Z |

TsukuroiR14 and MadoR14 are running concurrently. A sibling commit, or an edit to a leg target, between the baseline and injected runs makes `head.commit`, `head.blob_sha256` or `worktree.sha256` differ. That would be a **false scrub failure**. A change that lands mid-run inside one of the two runs could also yield a mixed snapshot.

The round13 bracket hashed only the sibling **index files** (`sibling_indexes_before/after`). That misses ref-only moves, such as `reset --soft` or `update-ref`, and worktree edits that never touch the index.

**Correction:**
- Run **A-B-A**: baseline, injected, baseline.
- Bracket every run with a per-leg `(HEAD commit, worktree sha256)` snapshot.
- Classify the result:
  - `A1==A2` and `B==A1` (minus `observed_at`) → equal.
  - `A1!=A2` → could-not-evaluate (drift), never a scrub failure.
- Also keep the index bracket for parity with round13.

**Do not** compare the new receipt's head commits or counts with round13's `pin_live` (changed 3/unchanged 3). Sibling HEADs have legitimately moved. The new receipt asserts only baseline≡injected plus the mapping, not 3/3/0.

**Axes:** freshness (not preclaimed), calibration, adjacency (read-only siblings).

### E5 — The ambient environment is not GIT-clean and must not be dumped
The ambient environment in this session already contains `GIT_EDITOR`, `GIT_PAGER` and `GIT_TERMINAL_PROMPT` (names only, values not read). If L1 runs from a hook, worktree or a similar context, ambient `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` could already be set. In that case "baseline" would itself be poisoned, or would equal injected.

**Correction:**
- Record `ambient_git_names` (sorted **names only**) and the booleans `baseline_has_GIT_DIR=false` and `baseline_has_GIT_WORK_TREE`.
- Never serialize `os.environ`, PATH or HOME values. PATH-like dumps appear in round12 `after-committed.json` and `BashWitness/*environment.path`, so that precedent exists and should not be repeated.
- If the harness cannot get a GIT_DIR-free baseline, it should strip `GIT_DIR` from the baseline and record that name in `baseline_removed_names`. It should not silently proceed.

**Axes:** operability, no-ambient-dump contract.

### E6 — "Same argv/cwd" must be proven, not asserted
`python3` in argv resolves through PATH, and the probe writes `os.path.abspath(manifest_path)`, which depends on cwd.

**Correction:**
- Record `argv` and absolute `cwd` once per run, and record `argv_equal`/`cwd_equal` computed from the values actually passed.
- Record `shutil.which("python3")` (a path, not env) for both runs.
- Use a bounded `timeout` and `stdin=DEVNULL`.
- Pin the probe and manifest sha256 **before and after** all runs, and cross-check that `tool_sha256` in each payload equals the on-disk digest (TOCTOU).
- Never execute the receipt argv from round13. The gate must not do so either.

**Axes:** calibration, identity.

### E7 — Mapping receipt: value-only matching cannot detect variable swaps
The runner has REV value collisions: `REV_BASH == REV_CHECKLIST == fecee87…` and `REV_JS == REV_CLAIMS == 175de6b…`.

**Counterexample:** swap `"$REV_BASH"`→`"$REV_CHECKLIST"` in the bash-surface call (mutate-and-run.sh:1118). A check that compares resolved values to the manifest still passes.

**Other extraction traps:**
- The six leg calls are `regression_case_git`, **not `run_leg`**. The wording in the assignment would match zero lines.
- `regression_case_git` also appears in five selftest fixture calls (:1455, 1465, 1472, 1480, 1520, 1547). A naive "all calls" grep returns 12, not 6.
- Lines 84-89 are a **comment** table.
- The manifest's `source` line ranges are line-number claims that must be checked by content.
- The probe's own `CANONICAL_LEGS` (pin-disposition.py:~125-136) is a third leg→repo/path authority.

**Correction (per leg booleans):**
- `table_path == call_path == manifest repo/path`
- The call uses `PIN_<X>`/`REV_<X>` variable **names** that are expected for that leg.
- `PIN_<X>` value `== manifest.expected_sha256`
- `REV_<X>` value `== manifest.pinned_commit`
- Calls are scoped to `run_regression`, lines 1111-1141 (`local st_js …` through `st_claims=$?`), with an exact count of 6 and unique leg names. A count other than 6 is a failure.
- Optionally record agreement with `CANONICAL_LEGS`.

**Axes:** depth, calibration (duplicate authorities).

### E8 — Scope and provenance boundary
The new context receipt is prospective evidence for round14. It must not be wired into `evidence-disposition.py` as a replacement receipt for round13 `pin_env_scrub`, and it must not be described as the missing round13 setup. The round13 row stays "equality retained, injection unrecorded". DispositionSpec and Gate should keep the `pin_env_scrub` row exactly as observed. The round14 receipt only shows that the same unchanged probe bytes behave equivalently under a recorded injection **now**.

**Axes:** calibration (false provenance), historical integrity.

## Tradeoffs the canonical judge must decide (not fixable defects)
- **Positive control:** the unscrubbed git call in E1 adds a subprocess beyond "pin probe only". Without it, injection delivery is proven by construction only.
- **The `/nonexistent` poison tests only the fail-closed path.** A poison pointing at a different *valid* repo is stronger: with `-C repo`, git would treat cwd as the worktree, `--show-toplevel` would still equal the repo path, and HEAD/blob would come from the wrong repo. That would make the probe's identity check the only defense other than the scrub. It is out of scope for this contract; record it as a known gap rather than add it silently.

## Checks L1 should run (after all seats finish, once)
1. `python3 .ufo/evidence/round-14/capture-context.py` (whatever CLI ReceiptHarness defines), then inspect `context-receipt.json` for:
   - `env_delta_keys==["GIT_DIR"]`
   - `injected_env` equal to the exact poison
   - no env values other than the poison
   - `ambient_git_names` names only
   - `argv_equal`/`cwd_equal` true
   - the A-B-A drift classification
   - `differing_paths ⊆ ["/observed_at"]`
   - `injected.counts.unavailable==0`
   - probe and manifest sha before and after equal to `2972539…`/`64eaa43…`, and equal to the payload `tool_sha256`
   - six mapping rows all true, with `call_count==6`
2. A grep on the receipt for the poison's absence elsewhere, and for the absence of `PATH=`/`HOME=`/token-shaped values.
3. Hand-mutate a scratch copy of the runner with the REV_BASH→REV_CHECKLIST swap, and confirm the mapping booleans go false. Use a temp copy only: never edit `tools/mutate-and-run.sh`.
4. Confirm that historical files are byte-identical: `git diff --quiet d6809df -- .ufo/evidence/round-13 .ufo/evidence/round-12 tools/pin-disposition.py tools/mutate-and-run.sh`.
5. Record sibling HEADs and the tsukuroi/mado dirty state at harness time in the round14 report. Do not treat any difference from round13's recorded HEADs as a regression.
