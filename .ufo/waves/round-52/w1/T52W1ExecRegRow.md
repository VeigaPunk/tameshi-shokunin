# T52W1ExecRegRow — R51.1 registry re-pin (C1 operability, wave 1)

Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin (read-only for this seat; HEAD 1f72d7d8189042b434a2f3753c2c346aefd5ec0f, base ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4).
Scratch (deleted before yield): /fast/scratch/hyaku/tameshi-r52/T52W1ExecRegRow.
No tools installed or upgraded this seat. uv 0.13.0 (/home/vgpnk/.local/bin/uv), node present on PATH (fnm multishell shim).

## Deliverables

| Path (relative to lane) | Bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-52/w1/T52W1ExecRegRow.patch` | 849 | `6b72cc76b6d47216f86fa029b5395cd45a233d17d9783ea12b24db7403e0b525` |
| `.ufo/waves/round-52/w1/T52W1ExecRegRow-only.out` | 87 | `4292b7eeee1f9a399a6394674e41498c4bd7d28cc301c545a9278fc637b55195` |
| `.ufo/waves/round-52/w1/T52W1ExecRegRow-only-base.out` | 90 | `80abea57c428447843899bcff404a5b89903357fa730ef21e6bdd69c6605bd40` |
| `.ufo/waves/round-52/w1/T52W1ExecRegRow-only.json` | 3000 | `0ef9f309906de5654658c0b90d19f9e98c228804c50d5085bd9190e23da63869` |

## Findings

**F1 — R51.1 reproduced at base: the registered needle contradicts the tool's leg table.**
`tools/registry.json:1014` at base still declares `"stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]`, but `tools/mte-interop.py:74-78` `LEG_TABLE` has ten entries (`js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`, `js-round-gate`, `js-sources-check`, `js-cite-check`, `bash-drift-pins`) and `check()` prints `legs_conforming=%d/%d` with `len(legs)` as the denominator (`tools/mte-interop.py:343-344`), so the reachable terminal line is `10/10`.
Command: `git -C <lane> show ef19d8e1:tools/registry.json | sed -n '1014p'`; `git -C <lane> show ef19d8e1:tools/mte-interop.py | python3 -c "…ast LEG_TABLE…"` → `entries= 10`.

**F2 — Minimal edit produced; only the needle and `source` move.**
Patch old blob `3e852fd` (= `ef19d8e1:tools/registry.json`) → new blob `aaf37cb`; 2 insertions, 2 deletions, one hunk `@@ -1011,11 +1011,11 @@`. `name`, `kind`, `argv` (incl. `uv run --no-project --with jsonschema==4.25.1`), `expect.exit`, `timeout_s: 900`, `status: active` and `tags` are untouched; the row stays at `tools/registry.json:1011-1019`.
Commands: `git -C <lane> diff --no-color -- tools/registry.json` (lane worktree already carried this exact edit; `git -C <lane> hash-object tools/registry.json` → `aaf37cb347f0e1c9cdd7c8ba65860ab14589b3c4`, `git -C <lane> rev-parse HEAD:tools/registry.json` → `3e852fd…`, i.e. HEAD bytes = base bytes); `git -C <clone> apply --check <patch>` → clean.

**F3 — New `source` names a committed line that states ten legs.**
`corpus/lessons/round-51-verifier-spotcheck.md@ef19d8e1:126` reads: “**R51.1, registry gate made unsatisfiable.** Update the `mte-interop-check` row in `tools/registry.json` to the ten-leg panel … Show `registry-check --only mte-interop-check` green at the fix revision with a committed receipt.”
Command: `git -C <lane> show ef19d8e1:corpus/lessons/round-51-verifier-spotcheck.md | sed -n '126p'`.

**F4 — Base gate receipt (pre-fix) shows `differs`.**
Clone at `ef19d8e1` inside a scratch fleet mirror (`$S/fleet/tameshi-shokunin`, sibling `*-shokunin` symlinks beside it), `python3 <clone>/tools/registry-check.py --root <clone> --only mte-interop-check` with `TMPDIR=$S/tmp`:
`ROW mte-interop-check expect=0 got=0 differs` / `REGISTRY_CHECK: held=0/1 superseded=0` / `exit=1`; wall **522.750 s** (receipt `T52W1ExecRegRow-only-base.out`). The row ran to exit 0 but the 9/9 needle was absent — the stale-expectation class, not a tool failure.

**F5 — Fixed gate receipt shows `held` (the closure receipt).**
Same clone, fixture commit `8d0a770cb9d1d58596ea21685174f9a5f9916e81` (`tools/registry.json | 4 ++--`, 1 file) made with a clone-local identity `t52-fixture <t52-fixture@example.invalid>`; `git -C <clone> status --porcelain` empty and `git -C <clone> rev-parse --show-toplevel` = the clone path before the commit. Re-run of the same command:
`ROW mte-interop-check expect=0 got=0 held` / `REGISTRY_CHECK: held=1/1 superseded=0` / `exit=0`; wall **216.388 s** (receipt `T52W1ExecRegRow-only.out`).
Supplementary `--json` run (same clone, same argv + `--json`): `exit 0`, row `held: true`, `elapsed_s: 180.076` (stderr holds the live-mode warning plus the same human `ROW`/`REGISTRY_CHECK` lines, which `--json` moves there by design), and `stdout_tail` carries all ten `MTE_LEG … CONFORMS` lines ending in `MTE_INTEROP: PASS legs_conforming=10/10` (receipt `T52W1ExecRegRow-only.json`). Running workdir was `$S/tmp/tameshi-mte-regression-…` (TMPDIR honoured), removed on PASS.

**F6 — The frozen C1 predicate (`mte_row_ok`) accepts the edited row and rejects the base row.**
Probe (not a verdict) importing `.ufo/evidence/round-52/c1/measure.py` without running `main`: `leg_count(base mte) = 10`; `mte_row_ok(lane worktree registry, base mte) = True ("legs=10 want='MTE_INTEROP: PASS legs_conforming=10/10' status=active needles=[…10/10]")`; `mte_row_ok(base registry, base mte) = False (needles=['…9/9'])`.
Command: `python3 - <<'EOF' … importlib load c1/measure.py; git show ef19d8e1:tools/mte-interop.py … EOF` from the lane root.

**F7 — uv resolved `jsonschema==4.25.1` offline.**
`uv run --offline --no-project --with jsonschema==4.25.1 python3 -c 'import jsonschema; print("jsonschema", jsonschema.__version__)'` → `jsonschema 4.25.1`, `rc=0`, `Installed 5 packages in 155ms`, 1.727 s; `uv cache dir` = `/home/vgpnk/.cache/uv`. `--offline` forbids network, so the pin is satisfied from the local cache for the row's exact argv prefix. (Both receipt runs above therefore resolved without network; their wall time is regression execution, not resolution.)

**F8 — Lane bounds held.**
This seat wrote only `.ufo/waves/round-52/w1/T52W1ExecRegRow.{patch,md}`, `-only.out`, `-only-base.out`, `-only.json`; it did not touch `tools/registry.json` (the `M` there and the other four `M` paths predate this seat: lane `git status --porcelain` still lists `SCORECARD.md`, `SKILL.md`, `corpus/knowledge/fleet-kill-rate-ledger.md`, `tools/registry.json`, `tools/round21-measure.py`), any git/jj state, or the fleet repo. Scratch dir removed at end (no live clone left).

## Residual risk / out-of-scope notes

- Only `--root` live-mode in a fleet-mirror clone was exercised (as the item specifies). `registry-check --rev` from the lane root builds its own mirror and is the C1 counter's job at the deciding run; this seat's receipts are probes.
- `mte-interop-check` is a 900 s-timeout gate; observed 216–523 s here, so no margin risk in this environment.
- The row's meaning (“the ten recorded legs conform”) is now aligned with the tool's `LEG_TABLE` at base; the C1 counter's `cannot_see` (a needle weakened to whatever the tool prints) does not apply to this row because the needle is the tool's own `K/K` denominator, not a constant typed by the editor.

## Summary

- R51.1 reproduced: base `tools/registry.json:1014` expects `legs_conforming=9/9`; `tools/mte-interop.py:74-78` has ten legs and prints `K/K` (`:343-344`).
- Deliverable patch re-pins the needle to `10/10` and points `source` at `corpus/lessons/round-51-verifier-spotcheck.md@ef19d8e1:126` (the “ten-leg panel” routed defect); nothing else in the row changes.
- Receipt at base (scratch fleet-mirror clone): `ROW … differs`, `held=0/1`, `exit=1`, 522.750 s.
- Receipt at fixture commit `8d0a770` (clone-local identity): `ROW … held`, `held=1/1`, `exit=0`, 216.388 s; `--json` tail shows `MTE_INTEROP: PASS legs_conforming=10/10`.
- `uv run --offline … jsonschema==4.25.1` resolves from `/home/vgpnk/.cache/uv` (155 ms), so no network is needed by the row.
- Lane untouched apart from the five declared wave paths; scratch deleted.
