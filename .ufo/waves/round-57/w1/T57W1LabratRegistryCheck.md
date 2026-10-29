# T57W1LabratRegistryCheck — registry-check runs a gate row at a pinned revision

Verdict: **CONFIRMED** for the milestone "registry-check runs fixtures at a pinned revision". Two constraints the row author must design around: absolute fleet-root argv is refused as non-hermetic (`differs`), and the gate's usage errors exit 1, which registry-check counts as `differs` (F2).

Lane base: `5e3569969b532310d2b8a3d130901757a3df356b`. Fixture commit (throwaway, scratch clone, identity `fixture`): `b9e08c13badb22179c2eb986b798f9b2b5ce78fb`, parent = base.

## Probe (raw outputs under `.ufo/waves/round-57/w1/T57W1LabratRegistryCheck-receipts/`)

Invocation: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry-check.py --root <clone at fleet/tameshi-shokunin> --rev b9e08c13badb22179c2eb986b798f9b2b5ce78fb --only <row>` (driver is the lane's copy; rows come from the fixture commit's `tools/registry.json`).

| row | expect | got | verdict | wall (s) |
|---|---|---|---|---|
| r57-probe-gate-held | 0 | 0 | held | 2.494 |
| r57-probe-gate-exit3 | 3 | 3 | held | 3.046 |
| r57-probe-gate-exit2 | 2 | 2 | held | 2.857 |
| r57-probe-absolute-argv | 0 | non-hermetic | differs | 2.015 |
| r57-probe-base-in-clone | 0 | 0 | held | 2.994 |
| r57-probe-shallow | 0 | 0 | held | 4.623 |
| r57-probe-history-count | 0 | 0 | held | 2.333 |

Raw ROW lines and trailers (from `*.human.stdout`):

```
ROW r57-probe-gate-held expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
ROW r57-probe-gate-exit3 expect=3 got=3 held
REGISTRY_CHECK: held=1/1 superseded=0
ROW r57-probe-gate-exit2 expect=2 got=2 held
REGISTRY_CHECK: held=1/1 superseded=0
ROW r57-probe-absolute-argv expect=0 got=non-hermetic differs
REGISTRY_CHECK: held=0/1 superseded=0
ROW r57-probe-base-in-clone expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
ROW r57-probe-shallow expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
ROW r57-probe-history-count expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
```

Control (existing row at base, `--rev 5e3569969b532310d2b8a3d130901757a3df356b`): `receipt-revision-gate-selftest` -> `ROW receipt-revision-gate-selftest expect=0 got=0 held`, `REGISTRY_CHECK: held=1/1 superseded=0`.

JSON detail of the exit-3 row (`--json`): `stdout_tail` = `GATE REFUSED fixtures/r57-probe/stale.txt role=positive revs=c34e2b14... code=RECEIPT_REV_MISMATCH ...` and `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_MISMATCH verdict=REFUSED`; report `rev_resolved` = `b9e08c13badb22179c2eb986b798f9b2b5ce78fb`, `root` = clone path under the fleet mirror.

## Answers to the item's questions

1. **Does a `gate` row run under `--rev`?** Yes. `r57-probe-gate-held` (exit 0, `--certified 5e3569969b532310d2b8a3d130901757a3df356b`, positive receipt with `rev=5e3569969b532310d2b8a3d130901757a3df356b`) -> `held`. The `--certified` SHA resolves inside the registry-check clone: the gate's own `git rev-parse` ran in the transient clone and printed `GATE: ... verdict=PASS`.
2. **Shared clone or depth?** Neither. `clone_lane_at_rev` runs `git clone --no-hardlinks -c core.hooksPath=/dev/null <root>` (no `--shared`, no `--depth`). Observed in the clone: `git rev-parse --is-shallow-repository` = `false` (row `r57-probe-shallow`, held); `git rev-list --count HEAD` = `490` = base count 489 + fixture commit (row `r57-probe-history-count`, held); `git cat-file -t 5e3569969b532310d2b8a3d130901757a3df356b` = `commit` (row `r57-probe-base-in-clone`, held). The fixture repo itself has `objects/info/alternates` (it was `--shared`); the transient clone still received the full closure.
3. **Row expecting exit 3.** `r57-probe-gate-exit3` (stale receipt `rev=5e3569969b532310d2b8a3d130901757a3df356b`, expect 3) -> `ROW ... expect=3 got=3 held`. registry-check does not special-case 3: `held` iff `got == expect.exit` and every needle present and cleanup ok. Overall `REGISTRY_CHECK` exit is 0 when all held.
4. **Exit-2 named row.** `r57-probe-gate-exit2` (unresolvable `--certified 0123…`) -> `expect=2 got=2 held`, needle `error=unresolvable-certified`.
5. **Hermeticity.** `r57-probe-absolute-argv` (argv names `<clone>/tools/receipt-revision-gate.py`, absolute, under the fleet root that is the parent of `--root`) -> `ROW r57-probe-absolute-argv expect=0 got=non-hermetic differs` (rc 1). The workaround is relative argv with `--lane .` (cwd = clone root), which all other rows use. Note `fleet_root` is `dirname(realpath(--root))`, so in production (lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`) any absolute `/home/vgpnk/Projects/shokunin/...` token in a row argv is refused.
6. **Wall time.** Per `--only` run 2.0–4.6 s (median ~2.9 s); `--json` run 3.1 s; TMPDIR-scoped run 3.9 s; a plain `git clone --no-hardlinks` of the lane alone measured 13.6 s (cold, 173 MB `.git`). Clone cost dominates.

## Findings (operability)

- **F1 (scratch placement, applies to every seat):** with `TMPDIR` unset, `clone_lane_at_rev` mkdtemps under `tempfile.gettempdir()` = `/tmp`. The lane's `.git` is 173 MB, which breaks the "`/tmp` only for files under 50 MB" rule. Measured: the `--root` clone path printed in the JSON report is `/tmp/tameshi-registry-check-*` when TMPDIR is unset and `/fast/scratch/hyaku/tameshi-r57/.../tmpdir/tameshi-registry-check-*` when `TMPDIR` is set; both are removed in `finally`. Workaround: export `TMPDIR` to the seat scratch before `registry-check.py --rev`. (My own runs left no `/tmp` residue; two other `/tmp/tameshi-registry-check-*` directories were present during my runs and belong to peer seats — not mine, not attributed.)
- **F2 (exit-class collision):** `receipt-revision-gate.py` usage errors call `raise SystemExit('usage: ...')` which exits **1**. Measured: `python3 tools/receipt-revision-gate.py --lane . --certified 5e3569969b532310d2b8a3d130901757a3df356b` (no `--receipt`) -> rc=1, stderr = usage line. In registry-check exit 1 is the `differs` class, while the documented could-not-evaluate class is 2. A gate row that intends to pin usage refusal as 2 cannot do so; the gate's own named refusals (0/2/3) are fine. Not edited (lane file; L1 decides).
- **F3 (unrun check):** I did not run a case where `--certified BASE` is reachable only through an unreferenced object in the root (the transient `git clone` copies refs only). Not run; the probe shows only the ancestor-of-HEAD case.

## Tools
No installs. Used `git 2.56.0`, `python3 3.14.8` (already on host). No pacman, no uv, no npm.

## Scratch hygiene
Fixture clone, fleet mirror and TMPDIR under `$HYAKU_SCRATCH/tameshi-r57/T57W1LabratRegistryCheck` removed after the run. The lane and fleet were not written; no git mutation outside the scratch clone. The only lane-tree writes are this report, the JSON, and the receipts dir.
