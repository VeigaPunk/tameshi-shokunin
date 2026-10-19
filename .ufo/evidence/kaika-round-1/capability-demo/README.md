# Capability demo — `tools/mutate-and-run.sh` (kaika round 1)

Bounded probes of the lane's existing instrument; the tool was **not edited** and the repository
was not written to (only this evidence directory and `/tmp/tameshi-r1-lab-*` scratch).

- Lane: `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tameshi-shokunin`
- git HEAD: `4eb4cf319c0eddd4ef0c6d1d4d11e51e0d4ee307` (branch `kaika/round`; pre-existing
  uncommitted `corpus/QUALITY.md`, `corpus/lessons/round-1.md` are L1's, not touched here)
- Tool sha256: `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`
  (`sha256sum tools/mutate-and-run.sh`; also echoed by the tool's own `MUTATE_TOOL:` line)
- Probe time: 2026-10-19 18:43–18:45 UTC; host loadavg 7.18 (other fleet seats running)

Environment fingerprint: `env-fingerprint.txt` (bash 5.3.15, node v24.21.0, python 3.14.7,
git 2.55.0, host `LANG=en_US.UTF-8`, `LC_ALL` unset, `TZ` unset).

## Verdicts

| Hypothesis | Verdict | Evidence |
|---|---|---|
| H1 — `--selftest` = 80/80 + `VERDICT: PASS` exit 0; `--regression` = `REGRESSION: PASS` exit 0 | **CONFIRMED** | `h1a-*`, `h1b-*` |
| H2 — exactly one control run per sweep, no repeat-control option | **CONFIRMED** | `h2-sweep.*` + source cites below |
| H3 — selftest insensitive to a scrubbed environment (`env -i`, `LANG=C`, `TZ=UTC`, fresh HOME) | **CONFIRMED** | `h3-*` vs `h1a-*` |

### H1 — CONFIRMED

Command (cwd = lane):

```
bash tools/mutate-and-run.sh --selftest
```

- `h1a-selftest-host.stdout:81` → `MUTATE_SELFTEST: 80/80 pass`
- `h1a-selftest-host.stdout:82` → `VERDICT: PASS`
- `h1a-selftest-host.exit` → `exit=0 duration-s=5`; stderr empty.

```
bash tools/mutate-and-run.sh --regression
```

- `h1b-regression.stdout:35` → `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`
- 6 × `REGRESSION_PIN` and 6 × `REGRESSION_CASE …: PASS`; 0 `REGRESSION_DEFECT` lines.
- `h1b-regression.exit` → `exit=0 duration-s=79`; stderr empty.
- Six legs materialized read-only from sibling git object stores, per `REGRESSION_PIN` lines:
  kimi-census 8/10, kagi surface-census 8/10, tsukuroi-census 6/10, mado-verify 4/10,
  kagi checklist-run 7/15, kumitate claims-check 7/10 — each measured `match=N/N`, `flips=0`,
  `inconclusive=0`. Fleet trees were not written (tool design: `git show`, header:79-108).

### H2 — CONFIRMED

Reading (source cites):
- Header order-of-operations, `tools/mutate-and-run.sh:63-64`: "(4) control run on the pristine —
  a red control exits 2 …; (5) mutant runs" — one control, then mutants.
- `tools/mutate-and-run.sh:465-475`: `run_sweep` calls `run_one "$PRISTINE" … CONTROL` exactly
  once (line 466); it emits `CONTROL: GREEN|RED` once; a red control aborts with exit 2.
- Usage options `tools/mutate-and-run.sh:188-196` list `--workdir --label --timeout --tail --keep`
  only; option parser (`:1621-1630`) has no repeat/control option.
- Sweep of the whole file for the string `repeat`: no match
  (`grep -n "repeat" tools/mutate-and-run.sh` → empty). No `--control-repeat`, no `N` option.

Observation: a 2-defect sweep over a `/tmp` fixture target (cwd = lane):

```
D=$(mktemp -d /tmp/tameshi-r1-lab-sweep.XXXXXX)
printf '#!/usr/bin/env bash\necho ok\n' > "$D/target.sh"
printf '@defect D1 | flip ok to bad\n@old ok\n@new bad\n@defect D2 | flip ok to worse\n@old ok\n@new worse\n' > "$D/spec.txt"
mkdir -p "$D/wd"
bash tools/mutate-and-run.sh --target "$D/target.sh" --defects "$D/spec.txt" \
  --suite 'bash "$MUTANT"' --workdir "$D/wd"
```

`CONTROL: GREEN` appears **1** time, followed by 2 `DEFECT` lines, `MUTATE: DONE`, exit 0
(`grep -c '^CONTROL: ' h2-sweep.stdout` → `1`). So the control count is 1 per sweep regardless of
defect count — measured.

Consequence for F3 (determinism precondition, ART C3 'U'): a sweep gives a single control
observation; there is no built-in repeat/flake probe. Whether that suffices for a "determinism
precondition" is a rubric judgment, not measured here. [INFERENCE] A flaky suite can therefore be
recorded as `CONTROL: GREEN` on one sample; the tool does not itself establish determinism.

### H3 — CONFIRMED

Command (cwd = lane; `HOMED=$(mktemp -d /tmp/tameshi-r1-lab-home.XXXXXX)`):

```
env -i PATH="$PATH" LANG=C LC_ALL=C TZ=UTC HOME="$HOMED" bash tools/mutate-and-run.sh --selftest
```

- `h3-selftest-envi.stdout:81` → `MUTATE_SELFTEST: 80/80 pass`; `:82` → `VERDICT: PASS`
- `h3-selftest-envi.exit` → `exit=0 duration-s=5`; stderr empty.
- Summary/verdict lines are byte-identical to the host-env run (`diff` → no output); the **entire
  stdout** is line-identical (`diff … | grep -c '^[<>]'` → `0`), including all 80 `PASS` lines.
  That is the tool's hermetic claim (header:132-136) holding under a scrubbed environment.

## File list

| File | Contents |
|---|---|
| `h1a-selftest-host.stdout/.stderr/.exit` | `--selftest`, host env; 80/80 PASS, exit 0, 5 s |
| `h1b-regression.stdout/.stderr/.exit` | `--regression`, six legs; PASS, exit 0, 79 s |
| `h2-sweep.stdout/.stderr/.exit` | one 2-defect sweep on a `/tmp` fixture; 1 `CONTROL:` line, exit 0 |
| `h3-selftest-envi.stdout/.stderr/.exit` | `--selftest` under `env -i …`; identical stdout, exit 0 |
| `env-fingerprint.txt` | HEAD, branch, tool sha256, toolchain versions, LANG/TZ, loadavg |

## Cleanup

- H2 scratch `/tmp/tameshi-r1-lab-sweep.Hznrhc` removed after the probe (`rm -rf`); its workdir
  and mutant copies are therefore not retained — the full stdout is the record.
- H3 HOME `/tmp/tameshi-r1-lab-home.dV7lAW` removed after the comparison.
- `--regression` scratch root `/tmp/tameshi-r4-2-regression.VGA0wT` was removed by the tool on
  PASS (it prints "removed on PASS"); `--selftest` roots `/tmp/tameshi-r4-2-selftest.*` were
  likewise removed by the tool. Post-check: no `/tmp/tameshi-r1-lab-*` or
  `/tmp/tameshi-r4-2-{selftest,regression}.*` remain.
- No writes outside the lane and `/tmp/tameshi-r1-lab-*`.
