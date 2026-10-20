# NoSiblingExec — read-only sibling / no-target-execution boundary audit (round 15, w1)

Seat: sentinel, leaf. Scope: historical `.ufo/evidence/round-14/capture-context.py` (sha not recomputed; bytes read only), its executed probe `tools/pin-disposition.py`, the text-only runner input `tools/mutate-and-run.sh`, the shared plan `.ufo/waves/round-15/spec1.json` (context + ContextGate/Registry/SpecHermetic items), `PROVINCE.md`, `.ufo/evidence/round-15/claims.json`, the routed defect at `corpus/lessons/round-14-verifier-spotcheck.md:154-162`, and the retained `.ufo/evidence/round-14/context-receipt.json` / `guardrails.json`.

**No command, gate, selftest, harness, git or interpreter was executed.** All findings are static source reads. `tools/context-capture.py` did not exist when I looked, so these are pre-implementation constraints on the planned gate, not a review of its code. Credentials were not touched. Tools installed or updated: none.

Axes: (a) no sibling code or gate execution; (b) sibling access stays read-only; (c) the selftest stays hermetic; (d) round-14 bytes are preserved; (e) process cleanup.

## Baseline: what the historical harness actually executes

| Process | Source | Target | Sibling exposure |
|---|---|---|---|
| `python3 tools/pin-disposition.py --manifest … --root FLEET_ROOT`, twice | `capture-context.py:538-540`, cwd `LANE_ROOT` | lane-owned probe | The probe runs `git -C <fleet>/<repo>` on 4 sibling repos (kumitate, kagi, tsukuroi, mado; `pin-disposition.py:128-135`). It uses only `rev-parse` and `cat-file -t/blob` (`:255, :278-296, :317-341`) and does O_NOFOLLOW regular-file hashing (`:353-403`). |
| `git -C LANE_ROOT rev-parse --git-dir`, twice | `capture-context.py:400-402` | own lane only | none |
| `tools/mutate-and-run.sh` | read as text only (`:477, :511-515`); the docstring at `:14` says "The runner is never run." | — | **none**. The runner is never spawned, sourced or imported. |

The retained receipt agrees: its argv shows `/usr/bin/python3` for the probe and `/usr/bin/git` for the control, and no runner argv (`context-receipt.json:53-60, 116-121`).

Conclusion: the historical harness does not execute sibling code or gates. Sibling access goes only through the probe's read-only plumbing, which preserves the PROVINCE.md:16-17 rule ("read-only probes"). That property is the boundary the promoted gate must keep. Executing the runner would break it. `--regression` materializes sibling gate bytes and runs `node "$MUTANT" --selftest` / `bash "$MUTANT" --selftest` for all six legs (`mutate-and-run.sh:1112-1140`), which is sibling-gate execution.

## Findings (supported risks only)

### F1 — Medium — Reusing the historical module can overwrite round-14 and read live sibling repos during selftest
- **Exploit path:** suppose `context-capture.py` imports the historical script (round 14 already did this through `runpy.run_path`, `guardrails.json:40`) and calls `main`, `write_receipt`, `evaluate`, `positive_control_block` or `base_receipt`.
  - `write_receipt` writes the hard-coded `OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"` (`:58, :583-602`). This replaces the retained round-14 receipt via `os.replace`.
  - `evaluate` and `positive_control_block` use module-global `LANE_ROOT`/`FLEET_ROOT`, derived from the historical file's own path (`:45-47, :400, :473, :538`). Inside a selftest they would therefore spawn the probe against the live fleet and run git against 4 live sibling repos and the live lane, whatever temp tree the selftest built.
  - `base_receipt` hashes the historical file as `tool_sha256` (`:414-416`), which misattributes the gate digest.
- **Impact:** round-14 raw evidence is mutated, contradicting "never overwrite round14". Selftest hermeticity fails, with live sibling reads that look like fixture results.
- **Smallest remediation:** reuse only the pure functions: `parse_json`, `validate_manifest`, `parse_runner_mapping`, `mapping_block`, `parse_probe_document`, `comparison_block`, `decide`. Write I/O, root derivation and receipt construction fresh in the new tool, with a round-15 output path. If the module is imported at runtime, the selftest copy layout must include the historical file. Otherwise the copied gate would import the live one (a live read). Copying the needed pure functions avoids both problems.

### F2 — Medium — A root-override flag would let the gate execute another tree's `tools/pin-disposition.py`
- **Exploit path:** the probe argv is the relative `[python3, "tools/pin-disposition.py", …]` with `cwd=LANE_ROOT` (`:538-540`). The historical script has no root flag; the root comes only from `realpath(__file__)` (`:45-46`). If the new gate adds `--lane-root/--root` so the selftest can point at fixtures, the same flag in capture mode would run any tree's `tools/pin-disposition.py` under the operator's identity. A sibling checkout passed as root is enough. That is sibling-code execution from a "read-only" gate.
- **Impact:** the no-sibling-execution boundary breaks. The receipt would still look like a lane observation.
- **Smallest remediation:** keep roots derived only from the gate's own realpath, with `FLEET_ROOT = dirname(LANE_ROOT)`. The selftest should copy the gate byte-for-byte (and assert the copy's sha256 equals its own) into `fleet=tempfile.mkdtemp()` / `lane=fleet/<lane-name>/tools/`. Synthetic probe, runner, manifest and expected fixtures go under that lane, and the copy runs as the public CLI. Do not use a fixed `/tmp/<name>` path: `FLEET_ROOT` would become `/tmp`, and the probe would resolve repos inside the shared `/tmp`.

### F3 — Medium — Retained-receipt `--check` must treat receipt contents as data
- **Exploit path:** a receipt is an untrusted record. It holds `runs.argv`, `runs.baseline.argv`, `positive_control.argv` (absolute `/usr/bin/git`, `-C <lane>`), `lane_root`, `fleet_root` and `invocation.cwd` (`context-receipt.json:6-12, 53-147`). A check mode that re-runs stored argv, or opens files under the receipt's `lane_root`/`fleet_root`, executes or reads whatever a forged receipt names.
- **Impact:** arbitrary command execution or reads outside the lane, and a "re-verified" claim that was never authorized.
- **Smallest remediation:** `--check` parses JSON (duplicate-key rejection as in `:158-181`), recomputes `decide()` over the stored blocks, and compares the pinned digest and exact expected `status`/`exit`/reasons. It never spawns subprocesses and never dereferences receipt-held paths. Any digest-bound snapshot verification reads only the gate's own constant REL paths under its own `LANE_ROOT`. This matches the S050 precedent ("It never executes receipt argv.", `round-14-verifier-spotcheck.md:130`). The registry should state that `--check` does not re-execute stored argv (`GateClassification.md:21`).

### F4 — Low — The probe is executed before its source digest is checked
- **Evidence:** the probe digest is computed at `:476, :481`, `matches_declared` at `:499-503`, and the probe is still spawned unconditionally at `:539-540`. `decide` flags the digest mismatch only afterwards (`:572-573`). Between hashing and exec there is also a read-then-exec window. The run-time `payload_tool_sha256_matches_disk` check (`:380-383`) only partly closes it, because the probe hashes its own file.
- **Impact:** a modified lane probe runs before the gate rejects it. The trust level is still the lane's own tree, so this does not extend to siblings.
- **Smallest remediation (optional, semantics-preserving):** in capture mode, if `sources.probe.matches_declared` is false, do not spawn the probe. Record `runs` as not executed and let `decide` return mismatch/exit 1 with its existing reason string. Otherwise keep the historical order. Do not claim a TOCTOU-free exec.

### F5 — Low — Ambient interpreter and PATH pass through to the probe
- **Evidence:** `safe_env` removes only `GIT_*` (`:184-187`), so `PYTHONPATH`/`PYTHONHOME` reach `python3 tools/pin-disposition.py`. A `PYTHONPATH` that points into a sibling tree puts modules there ahead of the stdlib. `python3`/`git` come from ambient `PATH` via `shutil.which` (`:517-518`). In Python 3.14 an empty `PATH` entry yields the relative name `git`/`python3`, checked against the invoker's cwd (`/usr/lib/python3.14/shutil.py:1591-1601, 1633-1640`), while the child resolves it against `cwd=LANE_ROOT`. The probe's own git is also a bare PATH lookup (`pin-disposition.py:218`), separate from the control's `git_path`. The retained r14 run resolved to `/usr/bin/python3` and `/usr/bin/git`, so this was not exercised historically.
- **Smallest remediation:**
  - **Selftest (required for hermeticity):** spawn the copied CLI with `[sys.executable, "-I", copied_gate, …]`.
  - **Capture mode:** keep the declared baseline policy unchanged (no new environment claim). Add an exit-2 `InvalidContext("missing_executable", …)` refusal when `which()` returns a non-absolute path, and record only the *names* of ambient `PYTHON*` keys present, never values (`ambient_env_dumped` stays false).

### F6 — Low — Timeout cleanup does not reach grandchildren
- **Evidence:** in Python 3.14, `subprocess.run` on timeout calls `process.kill()` and then `process.wait()` for the direct child only (`/usr/lib/python3.14/subprocess.py:558-571`). The probe's `git` grandchildren lose their parent's 30 s bound and may outlive it.
- **Impact:** orphan read-only git processes on sibling repos after a probe timeout, which surfaces as `InvalidContext("timeout")`/exit 2. They hold no locks (`GIT_OPTIONAL_LOCKS=0`).
- **Smallest remediation:** `start_new_session=True` in `run_bounded`, plus `os.killpg(proc.pid, SIGKILL)` on timeout. Selftest temp roots go in `try/finally: shutil.rmtree`.

### Not a finding (bounded)
- **Sibling git plumbing.**
  - The probe bypasses system and global config, disables locks and prompts, and sets `GIT_NO_LAZY_FETCH=1` (`pin-disposition.py:197-211`). The installed git is 2.55.0, per the pacman local db entry name `git-2.55.0-1`.
  - The probe never uses `status`/`diff`/`hash-object`, so it never touches the index, hooks, fsmonitor or filters (`:73-75`).
  - Repo-local `.git/config` of siblings is still parsed; no environment knob disables it. My claim that `rev-parse`/`cat-file -t|blob` trigger no configured command is **[INFERENCE]** from git's command semantics; I did not audit git's source.
  - Remediation: keep `git_env()` byte-identical and add no new sibling git subcommands (e.g. `log`/`diff` with textconv) to the gate.
- **Positive control.** It lacks `GIT_NO_LAZY_FETCH`, but it targets only the lane (`:400`), so it has no sibling impact.

## Exact bounded recommendations for ContextGate / Registry / L1

1. Only the pure historical functions are reused (F1). The output constant is `.ufo/evidence/round-15/…`. Round-14 files are never opened for write.
2. There is no root or path override in capture mode. The selftest runs a digest-asserted copy of the gate in a `mkdtemp` fleet/lane layout, with `sys.executable -I` (F2, F5).
3. `--check` makes no subprocess calls and does not dereference receipt paths. The registry states "does not re-execute stored argv" (F3).
4. `tools/mutate-and-run.sh` is never spawned, sourced or imported in any mode. The selftest uses a synthetic runner text fixture.
5. Optional hardening that changes no claim: digest-gate the probe before execution (F4), refuse non-absolute executables (F5), and use process-group kill on timeout (F6).
6. L1's single post-seat check pass can confirm items 1–4 statically. Grep the new tool for `mutate-and-run`, `subprocess`/`run_bounded` call sites inside the check path, `round-14/context-receipt`, and any argparse root option. Then confirm the round-14 receipt and harness bytes are unchanged against the baseline `a9cf4da78f2514c7bedd91a850a88590009d7df0` (`claims.json:3`).

These are advisory source findings. They are not an admission vote, and none of them was observed at runtime.
