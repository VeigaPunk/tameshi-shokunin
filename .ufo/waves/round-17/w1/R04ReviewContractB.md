# R04 — Contract B: entry registry vs the lane's actual registered commands

Seat: R04ReviewContractB (reviewer). Round 17 wave 1.
Lane tip reviewed: `98bea7da5801f4bc58e4187690ee1687c8a5061f`.
Objects reviewed: `tools/registry.json` (live draft, sha256
`c434f3ea8a8a9745e68e18958bfd26850c1188a540d48b7a3bfc36995f856c6c`,
28 rows), `tools/registry-check.py` (sha256
`60b0f5032aade3d2d55f46e37a43ce0816c46a57ce992ee47d64a26e47237b51`,
`--selftest` 15 cases, rc 0, 1.37 s), SKILL.md registries at the tip
(`:1499`, `:1548`, `:1597`, `:1676`, `:1806`), SCORECARD capability rows
(`:240-247`), and the in-flight round-17 instruments (hashes in §6).
Method: every candidate command was run in a fleet-mirror clone at the tip
(`/tmp/tameshi-r17w1-R04ReviewContractB-aSsjlf/fleet/tameshi-shokunin`,
siblings symlinked as the contract prescribes), timed, and, for the
live-tree question, traced with `strace -f -qq -e trace=openat,execve`.
Round-17 instruments that are not in the tip commit were copied into the
clone and re-hashed at run time. No tool installs.

## 0. Incident disclosure (critical; reported to L1 at 12:32)

While proving the inherited-environment hazard I ran

```
GIT_DIR=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.git \
  bash tools/mutate-and-run.sh --selftest        # cwd = the /tmp clone
```

The runner's selftest fixture commits inherited `GIT_DIR` and landed in the
live lane. At 12:29:33 the live lane's detached HEAD moved to the fixture
commits `f8832ef`, `0559c60`, `e16adb7` (`git reflog`, `selftest-fixture*`)
and the index now contains only `exec.sh noexec.sh target.sh`; `master` and
`origin/master` remain `98bea7da…`. I edited no lane file. I verified the
worktree against `git archive master`: all 1296 tracked files are
byte-identical except the wave's intended changes (`.gitignore`, `.jj`,
`tools/__pycache__`, new `tools/registry-check.py`,
`.ufo/evidence/round-16/round-gate/runner-sha256.txt` R16-EV1 append).
Minimal repair (I did not run it; the contract forbids lane git writes):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  reset --mixed 98bea7da5801f4bc58e4187690ee1687c8a5061f
```

This is not just my accident; it is the contract-B hole in §1.1. The L1
repaired the lane at 12:36:43 (`git reflog`: “round-17 L1 repair: restore
HEAD after R04 seat fixture commits (GIT_DIR leak)”). Verified after the
repair: HEAD `98bea7da…` (detached, as before), index 1296 files, status
only the intended wave changes; the three fixture commits stay dangling.

## 1. Findings by severity

### 1.1 CRITICAL — registry-check inherits the caller's git environment

`run_row` (`tools/registry-check.py:196-231`) calls `subprocess.run` with no
`env=`, so every row inherits `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
`GIT_OBJECT_DIRECTORY`, … A monitor started from a jj/git wrapper that
exports these runs rows against the wrong repository. Demonstrated:

```
$ GIT_DIR=<live lane>/.git GIT_WORK_TREE=<live lane> \
    git -C <mirror>/kumitate-shokunin rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/tameshi-shokunin
```

Consequences on the current rows: every `mutate-and-run.sh --regression` leg
hits the r17 repo-identity guard (`repo_identity_mismatch`, staged runner
`:1000-1015`) → exit 2; `pin-disposition` reports `repo_foreign`; a
selftest that commits fixtures (runner, §0) can write the lane's object
store and move HEAD. **Contract B must require scrubbing at least**
`GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY
GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_NAMESPACE GIT_PREFIX`
for every row (and recommend `TMPDIR=/tmp`, `GIT_CONFIG_NOSYSTEM=1`). This
is also the root cause of §0.

### 1.2 HIGH — three registered rows are not reproduced by a `--rev` clone

- `pin-disposition-read` passes the absolute live root
  `--root /home/vgpnk/Projects/shokunin`. Under `--rev` it therefore reads
  the live fleet, not the clone (its `manifest` is resolved in the clone,
  its six sibling observations in the live tree). If the row is changed to
  the mirror-relative `--root ..`, `pin-disposition.py:248-249` refuses each
  symlinked sibling with `repo_symlink`: measured `unchanged 0 / changed 0 /
  unavailable 6`, **exit 0**. Its verdict map (`0 observations, including
  changed/unavailable`) makes both forms green without saying the same
  thing. Registered as-is it also has no `stdout_contains`, so an
  all-unavailable result holds.
- `measure-round16-rev` and the two `measure` instruments default `--repo`
  to the hard-coded live lane (`round-16/measure.py:53`,
  `round-17/measure.py:78`). In a `--rev` clone the registered command (no
  `--repo`) reads the *live* lane. Proof: a clone-only commit `9e31698`
  gives `rc=2 "error": "rev-missing"` without `--repo`, `rc=0` with
  `--repo .`; `strace` shows 140 opens under
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. At the same rev the two
  outputs are identical, so the row passes by coincidence today and will
  diverge as soon as the clone is not the live lane.
  Recommendation: register `--rev HEAD --repo .` (also fixes the frozen-rev
  weakness below), or change both instruments' default to the lane
  containing the script.
- `trace-inputs-round17-selftest` is location-dependent. Its `home-external`
  case opens its *own script path* and asserts it lands in `external`
  (`trace-inputs.py:556-559`), where `external` is “regular files under
  `/home` outside root”. In a `/tmp` `--rev` clone the script is outside
  `/home`, so the case fails: measured 15/16, rc 1, row `differs` at
  unchanged bytes (`c587d35…`); the same bytes pass 16/16 in the live lane.
  The fixture must open a path explicitly under `/home` (e.g. a file in
  `$HOME`) or the row can never hold under `--rev`.

### 1.3 HIGH — timeout does not kill the row's process tree

`subprocess.run(..., timeout=…)` kills only the direct child. A timed-out
`bash tools/mutate-and-run.sh --regression` leaves its `node`/`bash` suites
running (the runner's own per-suite timeout is 300 s,
`mutate-and-run.sh:173`, × up to 11 runs per leg) and they keep writing
`/tmp` and reading siblings after the `ROW … got=timeout` line. Use
`start_new_session=True` + `killpg(SIGTERM)`, grace, then `SIGKILL`, and
record the kill in the report. Also cap captured stdout/stderr (the current
`PIPE`s are unbounded; a noisy row can exhaust memory); markers should be
searched on the capped text.

### 1.4 MEDIUM — markers that will drift, and rows that assert nothing

Verified volatile output tokens (run in the clone, `/tmp` and UTC clock):
`REGRESSION_DATE`, `REGRESSION_WORKDIR` (mkdtemp), `MUTATE_DATE`,
`MEASURE_SELFTEST … (scratch /tmp/<mkdtemp>)`, pin `observed_at` and
absolute `root`/`manifest`, witness `companion=<abs>`, bash-witness
`declared<TAB><abs path>`. Any marker containing these differs between the
live lane and the clone even when the semantics match. Current registry
status (sha `c434f3ea…`):

- `mutate-and-run-selftest` expects `MUTATE_SELFTEST: 83/83 pass`.
  The **staged** r17 runner (X05, sha `…` staged file, mtime 12:30) prints
  `MUTATE_SELFTEST: 88/88 pass` (measured rc 0, 5.25 s). After installation
  this row will report `differs` although the tool is green. Drop the count
  (`MUTATE_SELFTEST: `) or update to 88 after the install.
- Ten rows have no `stdout_contains` at all: `bash-witness-count`,
  `pin-disposition-read`, `evidence-disposition-round17`,
  `evidence-disposition-round17-before`, `measure-round16-rev`,
  `verify-round15`, `registry-check-selftest`, `measure-round17-selftest`,
  `trace-inputs-round17-selftest`, `assemble-round17-selftest`. Exit-only
  is the round-16 G4 lesson in reverse: use the stable verdict token
  (examples in §4). For the two count-bearing selftests that are stable at
  the tip (`repeat-control-selftest` 29, `bash-witness-selftest` 41/41,
  `witness-metadata-selftest` 39/39, `pin-selftest` 18/18,
  `context-selftest` 49/49, `evidence-disposition-selftest` 34/34,
  `measure-round16-selftest` 38/38) counts are acceptable but will churn
  when cases are added; count-free prefixes are safer.

### 1.5 MEDIUM — clone construction is under-specified and not verified

`clone_lane_at_rev` (`registry-check.py:242-290`) does `git clone -q …`
then `git checkout -q REV` and returns. It should:
resolve `<rev>^{commit}` with `rev-parse --verify --end-of-options`, then
`checkout --detach <sha>`, then assert `rev-parse HEAD` equals that sha.
Otherwise a branch name can attach (not a defect by itself) and a path-like
or ambiguous rev is accepted by checkout. Also pin *full* clone semantics
(no `--depth`/`--single-branch`): v2 disposition `historical_inputs` and
measure `--ledger-rev` read old commits, and a shallow clone would turn
those into exit 2. Finally, `--rev` without `--registry` reads
`<clone>/tools/registry.json`, which does not exist at any rev before this
round lands → exit 2; the counting command's `--registry` is mandatory for
old-rev grading and should be documented as such.

### 1.6 LOW — CLI/report edges

- A nonexistent `--root` makes every row `got=unavailable` and exits 1;
  recommend exit 2 `root_unavailable` (and for `--rev`, require a git
  worktree before cloning).
- `--only <non-active row>` yields `held=0/0`, exit 0; ambiguous. Return 2,
  or report the skip explicitly and exit 0 only for an explicit
  `--allow-skipped`.
- `got` vocabulary: contract says `got=<exit>`; the implementation emits
  `timeout` and `unavailable`. That is the right behavior; add the words to
  the contract and define `stdout_contains` as literal, case-sensitive,
  ANDed substrings of stdout decoded with `errors=replace`.
- `--json` schema is not in contract B; the implementation's
  `tameshi-registry-check-report-v1` is reasonable. Pin it, and include a
  bounded stderr tail + the resolved commit sha (not only the rev string)
  so a `differs` row is reproducible.
- `status` has no enumerated vocabulary; a typo silently skips a row
  (`run_row` skips any non-`active`). Validate `active|historical|parked`.
- Rows are not checked for write scope. All current rows are read-only in
  the lane (clone `git status --porcelain` stayed clean after the batch),
  but the monitor should report post-run dirt (or refuse `--root .` writes)
  rather than rely on the convention.
- Sequential execution is correct for determinism; do not parallelize by
  default (the 2-minute regression leg would contend with node/bash
  selftests and make wall-clock timeouts flaky).

## 2. Per-command notes (measured in the mirror clone at 98bea7da)

`F` = needs fleet root; `N` = network; `T` = writes /tmp; `C` = wall
clock/mkdtemp in output; `L` = reads live tree outside the clone;
`clone` = faithful under `--rev` as written.

| Registered command | rc | ms | F | N | T | C | L | clone | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `bash tools/mutate-and-run.sh --selftest` | 0 | 5202 | – | – | ✓ | – | – | ✓ | 83/83 at tip; staged 88/88 |
| `bash tools/mutate-and-run.sh --regression` | 0 | 121047 | ✓ | – | ✓ | ✓ | sibling object stores | ✓* | needs 7 sibling repos at FLEET_ROOT, pinned revs present; `REGRESSION: PASS (cases=7 passed=7 …)`; timeout 121 s |
| `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` | 0 | 22 | – | – | – | – | – | ✓ | `REPEAT_CONTROL: controls_match`; committed snapshot |
| `… --snapshot …/ControlGate/mismatch` | 1 | 23 | – | – | – | – | – | ✓ | `controls_mismatch` |
| `python3 tools/repeat-control.py --selftest` | 0 | 727 | – | – | ✓ | – | – | ✓ | 29 cases |
| `python3 tools/bash-witness-study.py count` | 0 | 38 | – | – | – | C path | – | ✓ | `counts<TAB>killed_on_witness=8…`, `unresolved<TAB>none` |
| `python3 tools/bash-witness-study.py selftest` | 0 | 48 | – | – | ✓ | – | – | ✓ | 41/41 |
| `python3 tools/pin-disposition.py --manifest … --root /home/vgpnk/Projects/shokunin` | 0 | 57 | ✓ | – | – | C | ✓ | **✗** | live counts unchanged 3/changed 3/unavailable 0; mirror-relative `--root ..` → 6 `repo_symlink`, exit 0 |
| `python3 tools/pin-disposition.py --selftest` | 0 | 719 | – | – | ✓ | – | – | ✓ | 18/18 |
| `python3 tools/witness-metadata.py --check --companion …` | 0 | 33 | – | – | – | C path | – | ✓ | `WITNESS_METADATA: metadata_consistent` |
| `python3 tools/witness-metadata.py --selftest` | 0 | 1325 | – | – | ✓ | – | – | ✓ | 39/39 |
| `python3 tools/context-capture.py --check --json` | 0 | 28 | – | – | – | – | – | ✓ | `context_consistent`; `DEFAULT_LANE_ROOT` from script (`:138`) |
| `… --check --receipt round-15/frozen/context-missing-env/…` | 1 | 27 | – | – | – | – | – | ✓ | `missing_injected_environment` |
| `… --check --receipt round-15/frozen/mapping-suffix/…` | 1 | 27 | – | – | – | – | – | ✓ | `mapping_mismatch` |
| `python3 tools/context-capture.py --selftest` | 0 | 1281 | – | – | ✓ | – | – | ✓ | 49/49 |
| `python3 tools/evidence-disposition.py --root . --dispositions round-17/dispositions.json --json` | 0 | 40 | – | – | – | – | – | ✓ | staged v2 `fab4cf73…`, `"status": "clean"`; needs full clone for historical revs |
| `… dispositions-before.json --json` | 1 | 31 | – | – | – | – | – | ✓ | `producer_before` finding; same v2 sha |
| `python3 tools/evidence-disposition.py --selftest` | 0 | 898 | – | – | ✓ | – | – | ✓ | 34/34 |
| `python3 .ufo/evidence/round-16/measure.py --rev <frozen>` | 0 | 45 | – | – | – | – | ✓ w/o `--repo` | **✗** | see §1.2; frozen rev never tracks the tip |
| `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | 789 | – | – | ✓ | C scratch | – | ✓ | 38/38 |
| `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | 34 | – | – | ✓ | – | – | ✓ | `SELFTEST: all checks passed` |
| `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | 27 | – | – | ✓ | – | – | ✓ | `SELFTEST: PASS`; source now SKILL.md:1813 (live) |
| `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | 0 | 61 | – | – | – | – | – | ✓ | `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` |
| `python3 .ufo/evidence/round-15/verify.py --rev <frozen>` | 0 | 1745 | – | – | – | – | – | ✓ | frozen rev; output has no stable verdict line registered |
| `python3 tools/registry-check.py --selftest` | 0 | 1367 | – | – | ✓ | – | – | ✓ | 15 cases |
| `python3 .ufo/evidence/round-17/measure.py --selftest` | 0 | 1392 | – | – | ✓ | C scratch | – | ✓ | 58/58 (draft `f654d5b…`) |
| `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest` | 0 live / 1 clone | 686 (clone) | – | – | ✓ | – | – | **✗** | 16/16 live; 15/16 in a `/tmp` clone because `home-external` opens the script's own path (`c587d35…`) |
| `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` | 0 | 42 | – | – | ✓ | – | – | ✓ | `SELFTEST: all checks passed` (`5996bc2…`) |

\* with sibling symlinks and pinned objects; not hermetic against sibling
deletion/history rewrite.

Strace evidence for “reads live tree outside the clone”: 0 live-fleet opens
for `measure --rev --repo .`, context check/selftest, witness check/selftest,
bash-witness count/selftest, repeat selftest, disposition selftest, assemble
selftest, runner selftest; 140 for `measure --rev` without `--repo`.
`pin-disposition --root /home/...` opens the live fleet by construction.

## 3. Does `--rev` reproduce `--root .`?

Yes for lane-local byte readers, with these conditions:

1. **Lane bytes**: identical (clone checkout at REV; all current rows read
   tracked files). Untracked files differ by design: a pre-commit live run
   sees round-17's untracked instruments/evidence; a `--rev` run at the same
   commit does not. The counting command runs post-commit, so this is not a
   defect, but `--rev` must not be used to grade an uncommitted worktree.
2. **Siblings**: the mirror symlinks live sibling repos; the clone is not a
   fleet snapshot. Regression is stable because its legs pin revs and read
   content by commit id; pin-disposition is not, because it reads sibling
   HEAD/worktree and refuses symlinked repos.
3. **Absolute paths in argv** defeat the clone (`pin-disposition-read`).
   Relative `--root .`/`--repo .` forms follow the clone; keep them
   relative.
4. **Git environment** must be scrubbed, or “reproduction” is against
   whatever repo the caller's `GIT_*` points at (§1.1).
5. **Full history** must be present for v2 `historical_inputs` and
   `--ledger-rev`; a shallow clone silently turns those into exit 2.

## 4. Recommended rows (deltas to the current registry)

- `mutate-and-run-selftest`: `stdout_contains ["MUTATE_SELFTEST: ",
  "VERDICT: PASS"]` (drop 83/83), `timeout_s 180`.
- `mutate-and-run-regression`: keep `REGRESSION: PASS`, `timeout_s 900`
  (measured 121 s; 360 s is only 3× and the internal per-suite timeout is
  300 s).
- `pin-disposition-read`: keep the live absolute root; add `["\"legs\": 6",
  "\"unavailable\": 0"]`; document live-only (or mark it `historical` for
  `--rev` runs). If a mirror-relative row is added, it must expect the
  `repo_symlink` outcome explicitly, never silence.
- `measure-round16-rev` / `measure-round17-*`: use `--rev HEAD --repo .`;
  add `["\"calibration_restraint_score\":", "\"coldread\":"]` (do not
  assert 8: older revs score 6). `measure-round16-selftest` timeout 120.
- `evidence-disposition-round17(-before)`: add `["\"status\": \"clean\""]`
  and `["\"status\": \"failed\"", "producer_before"]` respectively.
- `bash-witness-count`: add `["unresolved\tnone"]` (and optionally the
  frozen `counts\tkilled_on_witness=8`).
- `verify-round15`: add `["measure-historical-preserved: PASS"]`; keep the
  frozen rev (it is a historical replay, not a live probe).
- `registry-check-selftest`: add `["SELFTEST: PASS"]`, timeout 180.
- `trace-inputs-round17-selftest`: first fix the `home-external` fixture to
  open a file under `$HOME` rather than the script's own path; today the row
  differs in any `/tmp` clone (15/16, §1.2). Then add
  `["SELFTEST: 16/16"]` (or `["SELFTEST: "]`), timeout 120.
- `assemble-round17-selftest`: add `["SELFTEST: all checks passed"]`,
  timeout 120.
- Keep `repeat-control` snapshot rows (they are the only static form of the
  parameterized round-12 entry; `--runs 3 --out DIR -- COMMAND` cannot be a
  registry argv without a placeholder and a fresh output directory).
- Do **not** register the round-14 historical `evidence-disposition`
  command expecting 2: that would enshrine the R16-OP1 harm. The v2 rows
  above are its replacement; the round-14 manifests stay immutable.
- Add the SKILL.md round-17 registry heading before landing: five row
  `source` strings currently point at “SKILL.md round-17 registry pending”,
  which is not a resolvable source under contract B.

## 5. Residual risk / verification gaps

- The registry and its instruments were being written during this review
  (registry-check.py went through an IndentationError and a fixed
  `--json` tail; disposition/assemble/trace were still moving). Rates and
  line references are pinned to the hashes in §6; re-run the full registry
  after installation.
- Not executed: `mutate-and-run --regression` against the *staged* runner
  (2 min; the tip runner passed 7/7 in the clone), and a real `--rev` clone
  of the whole 28-row registry at an older rev (the clone here is at the
  review tip). The full run at the tip was in progress when this report was
  written; the row-by-row results above are from the same commands run
  individually.
- Network: none of the rows reach the network in these runs; suites that
  shell out to node/git do so locally. Hostile-mutant network access is out
  of scope (round-16 GuardAudit caveat stands).
- Wall-clock: no row's *exit* depends on the clock; only printed timestamps.
  The pin row's *content* depends on live sibling tips (that is its job).
- Full registry run in the same clone: `python3 tools/registry-check.py
  --root . --registry tools/registry.json --json` → rc 1, 133 s,
  `REGISTRY_CHECK: held=26/28`; the JSON report parsed and the human ROW
  lines went to stderr. Both differs were stale copies of instruments still
  being written: `assemble-round17-selftest` holds on the current bytes
  (`5996bc2…`, 80 ms, held=1/1); `trace-inputs-round17-selftest` still
  differs in the clone for the §1.2 location reason. Effective at the
  reviewed bytes: 27/28.
- The §0 incident was repaired at 12:36:43; any lane read of HEAD between
  12:29:33 and the repair is invalid, but the counting command can run now.

## 6. State hashes at review close (all under the lane)

| Object | sha256 |
|---|---|
| `tools/registry.json` | `c434f3ea8a8a9745e68e18958bfd26850c1188a540d48b7a3bfc36995f856c6c` |
| `tools/registry-check.py` | `60b0f5032aade3d2d55f46e37a43ce0816c46a57ce992ee47d64a26e47237b51` |
| staged `tools/evidence-disposition.py` | `fab4cf7392fe75ba74d811b5a0722ebc6f9ed3923146495284019e71c2c7941f` |
| staged `tools/mutate-and-run.sh` | `aea83422ebb098016cfaefa0b52eb06a5728b6dc00d38c6b63e76007588e3063` (88/88, 5.25 s) |
| staged `tools/pin-disposition.py` | `331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c` |
| `.ufo/evidence/round-17/measure.py` | `f654d5b660c27632e121d8959c58d0d23b2d2f5ce29db0e5e0eda45dda829997` |
| `.ufo/evidence/round-17/coldread/assemble.py` | `5996bc2a77da2cfe72834577c1869fcf890f12da966cccc84bcef650043ab0dd` |
| `.ufo/evidence/round-17/coldread/trace-inputs.py` | `c587d35bf7e169e29b6797f47fd7132a6c3c15b6a730be2b2160ff86d5ab620e` |
| `.ufo/evidence/round-17/dispositions.json` | `d9d6b82da26fb51cef453899f5271bebbbad01f0ea9d04abfacffa70062d2535` |

Verdict: **partial** — contract B holds for the lane-local rows and the
registry-check selftest, but it falls on inherited git environment, on three
rows that leave the clone (pin-disposition absolute root, measure default
`--repo`, trace-inputs `/home`-anchored selftest), and on the
timeout/process-tree and marker drift above; fix §1.1–§1.3 and the §4
deltas before the registry counts as the C2 monitor.
