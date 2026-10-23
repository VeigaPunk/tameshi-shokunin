# Round-35 w2 — ConnectorConfigGuards (cross-lane env-keyed guard scan)

Seat: `tameshi-r35-w2-ConnectorConfigGuards` (leaf connector, godspeed). Judged on adjacency.
Dispatch pin: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.

Lane setup (scratch, read-only): the pre-existing clone at
`/fast/scratch/hyaku/tameshi-r35-seats/ConnectorConfigGuards/lane` sat at `d16f9b5a`
(pre-amendment bytes); I fetched origin and checked out the dispatch commit:

```
cd .../ConnectorConfigGuards/lane && git fetch -q origin && git checkout -q --detach 7da6e076...
echo $?  # -> 0 ; git rev-parse HEAD -> 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
sha256sum at the pin (all match contract.json frozen_artifacts):
  tools/tally-audit-v3.py          ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885
  .ufo/evidence/round-35/c1/c1-measure.py 515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8
  .ufo/evidence/round-35/c2/c2-measure.py 67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc
  tools/mutate-and-run.sh          a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
  tools/tally-audit-v2.py          7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10
```

No installs (nothing needed; pacman untouched per bounds). `/fast` was at 100%
(1.8G free) throughout; all writes are tiny.

## What I attacked

The class round 35 fixed in tameshi's audit — **environment-keyed guards**: a condition
on an env var or path whose value changes a verdict. tameshi's instance (wave-1
RevengerRootShape CRITICAL, closed by amendment A4) was fail-OPEN: the runner copy was
gated on the real auto-root value `/tmp/tameshi-r4-2-regression.*`, the auditor swept
only fabricated root literals, and the divergent copy was ACCEPTED. The cross-lane
question: do the sibling lanes' gates carry the same class, and does each site's own
selftest exercise **both sides** of the condition (key set vs unset / path matched vs
not) with asserted verdicts?

Method: read-only grep sweeps over
`/home/vgpnk/Projects/shokunin/{kumitate,kagi,tsukuroi,mado}-shokunin` for
`process\.env`, `os\.(environ|getenv)`, shell `[[ -n/-z "$VAR" ]]` guards and
path-prefix conditions; targeted reads of every hit that plausibly changes a verdict;
two measured live demonstrations; two executed sibling selftests. No file under any
sibling lane was written. No tameshi artifact was touched.

## Site inventory (path:line — key — verdict effect — direction — selftest both sides?)

### kumitate-shokunin (scripts/*.mjs) — 9 sites

1. `scripts/round-gate.mjs:173-176` (`resolveSrcDefault`) — `UFO_SRC` selects which
   origin tree the gate audits → changes the verdict. **Both sides: YES.**
   `ENV_KEYS` at `:740` strips `KUMITATE_REPORTS_DIR|KUMITATE_MAIN_REPO|KUMITATE_LANE|UFO_SRC`
   from every fixture child (`:741-745`, `:761-763`); the hermeticity case at
   `:1417-1441` runs the whole nested selftest under
   `UFO_SRC='/nonexistent/origin'` + bogus dir flags and requires `VERDICT: PASS`
   (exit 0). Unset side = every other child. Fail-closed default: no candidate →
   exit-2 refusal, never a scored zero (`:172-176`).
2. `scripts/claims-check.mjs:110-114` — same `UFO_SRC` default. **Both sides:
   PARTIAL.** `''`-override children exercised (`:1068`); the file's own comment
   (`:1244-1246`) says the poisoned-env acceptance is proven "from outside" — but the
   outer harness (see #7) poisons only GIT_*/NODE_*/INJECT names, not UFO_SRC. The
   non-empty-bogus side for claims-check is covered only by sibling tools (#1, #5).
   HYGIENE gap (lane-wide coverage holds; per-tool coverage does not).
3. `scripts/cite-check.mjs:116-120` — same default. **Both sides: PARTIAL** —
   `UFO_SRC: ''` children at `:2330`, `:2357`; no non-empty-bogus UFO_SRC child found
   (its hermeticity budget went to the GIT_* canary at `:2515-2528` and the INJECT41
   recursion at `:2446-2500`). Same HYGIENE class as #2.
4. `scripts/surface-probe.mjs:167-171` — same default. **Both sides: YES** —
   `--selftest` never resolves src (`:164-166`); `''`-fallback to the fail-closed arm
   asserted at `:1672-1675`; ambient passthrough child env explicit at `:1616`.
5. `scripts/proxy-check.mjs:327` (`UFO_SRC`) and `:438`
   (`DEFAULT_KIMI_ROOT = process.env.KIMI_ROOT || ~/.kimi-code`) — env selects the
   substrate the K terms count. **Both sides: YES** — nested hermeticity
   `:2870-2890` runs selftest under `UFO_SRC='/nonexistent/origin'` +
   `KIMI_ROOT='/nonexistent/kimi'` requiring PASS; fail-closed arm
   `KIMI_ROOT_NOT_A_DIR` at `:1270-1276` probed at `:2604-2605` and `:2310-2317`.
   **Residual BOUND:** on a live run with no `--kimi-root`/`--src` flag, an ambient
   `KIMI_ROOT`/`UFO_SRC` pointing at a *real but wrong* tree silently changes the
   scored substrate; there is no provenance token in the verdict naming the resolved
   substrate source (the docstring at `:275-281` documents the default deliberately,
   and `--src`/`--kimi-root` flags pin it — the pinned counting commands bypass env).
6. `scripts/wave-census.mjs:276` + `:585-589` —
   `KUMITATE_WAVE_CENSUS_SELFTEST_INJECT_FAIL` inject key. **Both sides: YES, and
   measured this seat:** parent run `node scripts/wave-census.mjs --selftest` →
   exit 0, `VERDICT: PASS`; the suite internally spawns a child with the inject var
   set and requires exit 1 + `FAIL  WC00` (`:586-589`).
7. `scripts/cite-check.mjs:2446-2500` + `:2697-2703` — selftest-depth/inject/primary-only
   env keys gating an injected failing case. **Both sides: YES, and
   mutation-verified:** `scripts/gate-mutants.mjs:169-171` carries live mutants of the
   guard itself (`process.env[INJECT41] !== undefined` → `!== '1'` and
   `=== undefined`), i.e. kumitate mutation-tests its own env guard's both directions.
8. `scripts/gate-mutants.mjs:854-866` + `:1117-1138` — fixture child asserts its env
   is EXACTLY `HOME|LANG|PATH|TMPDIR|TZ` with pinned values (`TMPDIR === root`,
   `cwd === root/work`); `if (process.env.GIT_DIR)` in the child performs an unsafe
   sentinel commit (`:863-866`). The harness plants
   `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE` (+ `NODE_OPTIONS`, `NODE_PATH`) at
   `:1123-1128`, runs the control, restores, and asserts HEAD unchanged. **Both
   sides: YES** — the env-keyed branch is the alarm, and both its arms are driven.
9. `scripts/cap-run.mjs:106,156,295,393-414`, `scripts/cap-spawn.mjs:40-46` — the
   sandbox that makes #1-#8 meaningful: child env is an explicit allowlist
   (`PATH`/`XDG_RUNTIME_DIR`), with hostile-env leak probes (marker keys, fake
   `GIT_DIR`, `P1ENV` parse). Not verdict guards themselves; the enforcement layer.

### tsukuroi-shokunin (tools/) — 5 sites

10. `tools/tsukuroi-census.sh:393-430` — the override surface: every probe command and
    host path is env-selectable (`TSUKUROI_PACMAN`, `_PACMAN_CONF`, `_PACMAN_DB`,
    `_ROOT_DIR`, `_SYSTEMCTL`, `_DMESG`, `_JOURNALCTL`, `_NVIDIA_SMI`, `_LSMOD`,
    `_PCI_SYSFS`, `_DEV_DIR`, `_HOSTNAME_FILE`, `_DMESG_RESTRICT_FILE`,
    `_BOOT_TARGET`, `_CGROUP_ROOT`, `_MEM_SLICE`, `_PRESSURE_FILE`, `_MEMINFO_FILE`,
    `_VMSTAT_FILE`, `_PACMAN_LOG`, `_ETC_DIR`, `_OFFLINE_DB`, `_EXPAC`, `_VERCMP`,
    `_FOREIGN_BASELINE`, `_OOM_BASELINE`, `_SAMPLE_N`, `_TIMER_SCAN_MAX`). All six
    plane verdicts (packages/systemd/drivers/journal/update-safety/oom) are computed
    through these. **Both sides: YES per arm** — hermetic `--selftest` builds a
    fixture tree with a dispatcher stub and re-invokes the script via the overrides;
    measured this seat: `bash tools/tsukuroi-census.sh --selftest` → exit 0,
    `TSUKUROI_CENSUS_SELFTEST: PASS (105 cases, 105 passed, 0 failed)`. Dangerous
    values fail closed: empty/relative/unsafe `TSUKUROI_ROOT_DIR` → BLOCKED before
    any stat with the raw caller path never echoed (`:772-808`, cases at `:2696-2706`).
11. **Provenance asymmetry (the live A4-sibling channel).** Only the root arm records
    the channel: `root_src=default|override` (`:403`, `:874`). **Measured live this
    seat** (host is genuinely DEGRADED; both runs exit 1, top verdict identical):
    - clean: `PLANE packages: DEGRADED (... root_src=default root_dir=/ ...)`
    - `TSUKUROI_ROOT_DIR=/tmp`: `PLANE packages: DEGRADED (... root_src=override root_dir=/tmp ...)`
    For the other 20+ overrides there is **no provenance token** (no `journal_src=`,
    `pacman_src=`, … anywhere in the file): a live census run under ambient
    `TSUKUROI_JOURNALCTL=<wrapper>` changes the journal evidence bytes with nothing in
    the output recording the substitution. Direction: **fail-open potential** —
    verdict computed over an attacker-selectable substrate. The benign arm is
    recorded; the dangerous arms are not. **BOUND.**
12. `tools/score-census-handoff-r32.py:786-800` — the lane's own harness treats the
    channel as untrusted: it strips `TSUKUROI_*` from the "plain" live view, then runs
    a "filtered" view with `TSUKUROI_JOURNALCTL` pointed at a seeded wrapper that
    drops K coredump entries (K∈2..4), and requires the two views to agree. This is a
    two-sided sweep of the env channel in harness form — the structural sibling of
    tameshi's A4 fix (real substrate value vs fabricated one).
13. `tools/probe-git-env-leak.py`, `probe-git-env-residual-r30.py`,
    `probe-child-env-allowlist-r31.py/r32/r33/r34.py` — a five-round probe series
    measuring whether ambient env reaches children **by NAME** (12 injected names per
    run), because copy-minus-denylist env handling passes while leaking (r32
    docstring `:6-12`; r34 docstring enumerates 13 surviving `GIT_*` names). Evidence
    the class is tracked lane-wide on purpose, not incidentally.
14. `clean_env()` GIT_* strips: `tools/check-revision-binding.py:103-107`,
    `check-report-receipts.py:311`, `check-btrfs-space-r30.py:104`,
    `run-receipt.py:39`, `mutants-btrfs-space-r30.py:362` — hygiene guards that
    REMOVE env-keyed variance (ambient `GIT_DIR` must not redirect git children).
    Not verdict guards themselves.

### mado-shokunin — 5 sites

15. `tools/mado-verify.sh:3394-3408` — `HYPRLAND_INSTANCE_SIGNATURE` (env) and
    hyprctl-on-PATH gate the entire hypr-live plane: unset/unreachable →
    `live.plane UNKNOWN "... verdict cannot be CLEAN"` (`:3405-3407`). **Env-keyed
    verdict change; direction fail-closed. Selftest both sides: NO** — the variable
    appears only at `:3397-3398`; the selftest (`:416+`) is file-plane hermetic
    (`LIVE=0` → SKIP row at `:3185-3186`). The in-repo fix pattern already exists —
    the walker rows were split out of live_plane precisely "so the selftest can drive
    both pin arms against a stub walker / systemctl" (`:3360-3362`) — but it was not
    applied to the hyprctl/env guard. **BOUND** (coverage gap on a fail-closed guard).
16. `tools/mado-verify.sh:3551-3568` — the live env probes (`printenv GDK_SCALE`,
    `printenv NVD_BACKEND`) are themselves env-keyed live verdicts (FAIL if
    `NVD_BACKEND` is set). Same no-live-selftest situation; acceptable for a live
    plane, but the stub shape used for the regression engine's D3 defect (`:2078-2084`)
    would cover the branch shape.
17. `tools/mado-wsrules.py:358-359` — `ConfigReader` seeds hyprlang's variable table
    with `dict(os.environ)`, and `$VAR` expansion in workspace rules reads it
    (`:370-386`). The tool's output is therefore a function of the caller's ambient
    env. **Measured this seat**, identical `--home`, exit 0 on all three runs
    (fixture: one workspace rule `defaultName:$CCG_WSNAME`):
    - `env -u CCG_WSNAME … --home H` → `"defaultName": "$CCG_WSNAME"` (unexpanded), sha256 `2ef676a73a5ece2d9a0e467611940524fcec0c8999ea1f4bafe9a6feac86fa2`
    - `CCG_WSNAME=alpha …` → `"defaultName": "alpha"`, sha256 `77a6b09c7ee35e6ed53d70b247b002ac462c0b1cee91f18f4cc6dd19a0a1fa95`
    - `CCG_WSNAME=beta …` → `"defaultName": "beta"`, sha256 `bb5e809742657a6bfe6f120a99720e200e3a74b04b3b2f4b1b49c10e34873a4b`
    `cmp`: unset≠alpha, alpha≠beta — three divergent byte hashes under one fixed
    substrate. This is fidelity-faithful (real hyprlang inherits the environment), so
    it is not a tool bug; it is the **object-under-test env-sensitivity class** —
    the measurement must pin the env, and nothing in the file (no selftest) does.
    **BOUND** (measurement fragility).
18. `tools/mado-verify.sh:474-501, 510-594` — the selftest's stub runner is env-keyed
    (`STUB_ROWS`/`STUB_CONTROL`/`STUB_RESTORE`/`STUB_EXIT`) and drives the regression
    engine through green/doctored/extra-id/missing-id/control-red/inconclusive
    scenarios. **Both sides by construction** — positive-control reference for how an
    env-keyed harness should look.
19. `quality/counter-selftest.py:475-476`, `quality/check-control-receipts.py:61-63` —
    GIT_* scrub for children; hygiene (same class as tsukuroi #14).

### kagi-shokunin — 0 sites

20. `corpus/revision-audit.py:39-43` — `git_env()` strips `GIT_*` only (hygiene).
    `corpus/release-clock.py` (93.9KB) contains **zero** `os.environ`/`os.getenv`
    reads (grep miss). No `tools/` or `scripts/` directory exists (glob empty); no
    env-keyed verdict guard found anywhere in the lane. **Lane-specific absence.**

## Generality verdict

**GENERAL** (≥2 independent lanes): kumitate, tsukuroi and mado all carry
env/path-keyed conditions that change verdicts; kagi currently does not. Within the
class:
- **Fail-open shapes still live:** tsukuroi #11 (non-root override arms without
  provenance, live-demonstrated channel) and mado #17 (ambient-env parse dependence,
  measured divergence). kumitate #5's unflagged-live substrate selection is the same
  shape, mitigated by documented flag defaults.
- **Everything else observed is fail-closed** (`UNKNOWN — verdict cannot be CLEAN`,
  `BLOCKED`, exit-2 refusal) **or harnessed two-sided with asserted verdicts**
  (kumitate #1/#4/#5/#6/#7/#8, tsukuroi #10/#12, mado #18).
- **No sibling instance matches tameshi pre-A4's exact false-accept** (a divergent
  copy accepted because the auditor swept fabricated key values): the sibling gates'
  dangerous sides are fail-closed or env-stripped, and kumitate additionally
  mutation-tests its own env guards (#7).

## What I could NOT break (with proof)

- **The tameshi apparatus.** Read-only by construction; the dispatch-pin checkout
  reproduces all five frozen sha256s byte-for-byte (list in the header). This seat
  makes no tameshi claim and breaks none; the six wave-1 reports under `w1/` were not
  touched.
- **kumitate selftest hermeticity.** Could not make a selftest verdict
  env-sensitive: the nested-poisoned-env acceptance runs (round-gate `:1417-1441`,
  proxy-check `:2870-2890`) are code-read, and the parent side is measured green
  (`wave-census --selftest` → exit 0). The `''`-override side is asserted in
  claims-check `:1068`, cite-check `:2330/:2357`, surface-probe `:1647/:1672`.
- **tsukuroi dangerous override classes.** Empty/relative/unsafe `TSUKUROI_ROOT_DIR`
  → BLOCKED before any stat, raw caller path never echoed (`:772-808`; selftest cases
  `:2696-2706` inside the measured 105/105 PASS). Live benign arm measured: only the
  provenance token changes (`root_src=default root_dir=/` → `root_src=override
  root_dir=/tmp`), exit 1 both runs, top verdict identical.
- **mado live-plane guard direction.** Every failure arm of the env guard lands on
  UNKNOWN with "verdict cannot be CLEAN" (`:3405-3407`) or SKIP (`:3185-3186`); no
  fail-open arm exists for it in the file.
- **kagi.** No env-keyed verdict surface exists to attack (grep over `corpus/` for
  `os.environ|os.getenv|process.env` returns only `revision-audit.py:40` and a
  knowledge-doc example).

## Proposed move (one bounded adjacency move, two instances)

Adopt patterns each repo already contains; no axis harmed (runtime: one output token
/ one selftest case; contract: unchanged):

1. **tsukuroi-census.sh live mode — generalize the `root_src` provenance token to
   every override arm** (`journal_src=`, `pacman_src=`, `db_src=`, … at `:394-430`),
   **or** preflight-refuse any `TSUKUROI_*` override in live (non-`--selftest`) mode
   unless an explicit `TSUKUROI_ALLOW_OVERRIDES=1` is also set. Evidence: the live
   demo above shows the channel is live and, outside the root arm, unrecorded; the
   lane's own `score-census-handoff-r32.py:786` already treats ambient `TSUKUROI_*`
   as untrusted when comparing views. Verification: rerun
   `bash tools/tsukuroi-census.sh --selftest` (must stay 105/105 PASS, exit 0) and the
   two live commands above (polluted run must then print the refusal or a
   `*_src=override` token per arm).
2. **mado-verify.sh — split the `HYPRLAND_INSTANCE_SIGNATURE`/hyprctl-presence guard
   the way `walker_live_rows` was split** (`:3360-3362`) so the selftest drives both
   arms against a stub `hyprctl` (unset → UNKNOWN row asserted; set + answering →
   version-pin arm asserted), plus a stub-`printenv` arm for the
   GDK_SCALE/NVD_BACKEND probes. This closes the only env-keyed verdict branch in the
   sibling set with zero selftest coverage. Verification: `bash tools/mado-verify.sh
   --selftest` (must exit 0 with the two new cases green).

## Verification summary (exercised only)

| command | exit | evidence |
|---|---|---|
| lane fetch + checkout `7da6e076` | 0 | HEAD = dispatch pin; 5 sha256s match contract |
| wsrules demo ×3 (`env -u CCG_WSNAME` / `=alpha` / `=beta`, same `--home`) | 0 / 0 / 0 | sha256 `2ef676a7…`, `77a6b09c…`, `bb5e8097…`; `cmp` diverged both ways |
| `bash tsukuroi-census.sh` (clean) and `env TSUKUROI_ROOT_DIR=/tmp bash …` | 1 / 1 | `root_src=default root_dir=/` vs `root_src=override root_dir=/tmp`; verdict line identical otherwise |
| `bash tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (105 cases, 105 passed, 0 failed)` |
| `node scripts/wave-census.mjs --selftest` (kumitate) | 0 | `VERDICT: PASS` (node v24.21.0) |

Tooling: no installs, no upgrades, no pacman. Scratch:
`/fast/scratch/hyaku/tameshi-r35-seats/ConnectorConfigGuards/{lane,wsrules-demo,tsukuroi-live}`.
Only file written under the fleet tree: this report.
