# X04 — tools/registry.json (contract B entry registry)

Lane tip measured: `98bea7da5801f4bc58e4187690ee1687c8a5061f` (branch master, = live HEAD at run time).
Method: every pre-existing row was executed in a fleet-mirror clone of the tip
(`/tmp/tameshi-r17w1-X04RegistryRows-EkLHZD/fleet/tameshi-shokunin`, siblings symlinked,
`git checkout -q 98bea7d`) so writes stay off the live tree; the five round-17 rows were run
in the live lane (the manifests/tools are still untracked wave output). Elapsed = wall seconds.

## Row-by-row evidence

| row name | source | argv (after interpreter) | expect | observed | elapsed | held? |
|---|---|---|---|---|---|---|
| repeat-control-snapshot-clean | SKILL.md r12 `### Gate/probe registry` (~:1499) | `--snapshot .ufo/evidence/round-12/ControlGate` | 0 | 0 | 0.02 | yes (`controls_match`) |
| repeat-control-snapshot-mismatch | same | `--snapshot .ufo/evidence/round-12/ControlGate/mismatch` | 1 | 1 | 0.02 | yes (`controls_mismatch`) |
| repeat-control-selftest | same + SCORECARD caps | `--selftest` | 0 | 0 | 0.72 | yes (`SELFTEST: PASS (29 cases)`) |
| bash-witness-count | SKILL.md r12 (bash declared-witness study) | `count` | 0 | 0 | 0.04 | yes |
| bash-witness-selftest | same | `selftest` | 0 | 0 | 0.05 | yes (`WITNESS_SELFTEST: 41/41 pass`) |
| pin-disposition-read | SKILL.md r13 `### Round-13 gate/probe registry` (~:1548) | `--manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 | 0 | 0.06 | yes (changed/unchanged/unavailable observations emitted) |
| pin-disposition-selftest | same + SCORECARD caps | `--selftest` | 0 | 0 | 0.73 | yes (`SELFTEST: PASS (18/18)`) |
| witness-metadata-check | SKILL.md r13 | `--check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 | 0 | 0.04 | yes (`metadata_consistent`) |
| witness-metadata-selftest | same + SCORECARD caps | `--selftest` | 0 | 0 | 1.31 | yes (`SELFTEST: PASS 39/39`) |
| evidence-disposition-round17 | r15 registry disposition row, re-pinned to round-17 v2 manifest per target | `--root . --dispositions .ufo/evidence/round-17/dispositions.json --json` | 0 | **2 `schema_mismatch`** | 0.03 | **differs** — live `tools/evidence-disposition.py` is still v1 (`r14` banner); v2 support is being staged this wave |
| evidence-disposition-round17-before | same, before-manifest | `--root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json` | 1 | **2 `schema_mismatch`** | 0.02 | **differs** — same cause |
| evidence-disposition-selftest | r15 registry + SCORECARD caps | `--selftest` | 0 | 0 | 0.92 | yes (`SELFTEST: PASS (34/34)`) |
| context-capture-frozen | SKILL.md r15 `### Round-15 gate/probe registry` (~:1676) | `--check --json` | 0 | 0 | 0.03 | yes (`context_consistent`) |
| context-capture-missing-env | same (`--receipt/--expected` form) | `--check --receipt .ufo/evidence/round-15/frozen/context-missing-env/receipt.json --expected …/expected.json` | 1 | 1 | 0.03 | yes (`missing_injected_environment`) |
| context-capture-mapping-suffix | same | `--check --receipt .ufo/evidence/round-15/frozen/mapping-suffix/receipt.json --expected …/expected.json` | 1 | 1 | 0.03 | yes (`mapping_mismatch`) |
| context-capture-selftest | same | `--selftest` | 0 | 0 | 1.27 | yes (`SELFTEST: PASS (49/49)`) |
| mutate-and-run-selftest | SKILL.md r16 `### Round-16 gate/probe registry` (~:1806) + SCORECARD caps | `bash tools/mutate-and-run.sh --selftest` | 0 | 0 | 5.15 | yes — **but observed marker is `MUTATE_SELFTEST: 83/83 pass`; the SCORECARD's named literal `80/80` is stale** (registered stdout_contains uses the observed literal) |
| mutate-and-run-regression | same + SCORECARD caps | `bash tools/mutate-and-run.sh --regression` | 0 | 0 | 114.53 | yes (`REGRESSION: PASS (cases=7 passed=7 …)`) |
| measure-round16-rev | SKILL.md r16 | `--rev 98bea7da5801f4bc58e4187690ee1687c8a5061f` | 0 | 0 | 0.04 | yes |
| measure-round16-selftest | SKILL.md r16 | `--selftest` | 0 | 0 | 0.78 | yes (`MEASURE_SELFTEST: 38/38 pass`) |
| assemble-round16-selftest | SKILL.md r16 | `--selftest` | 0 | 0 | 0.03 | yes (`SELFTEST: all checks passed`) |
| reattribute-round16-selftest | SKILL.md r16 | `--selftest` | 0 | 0 | 0.03 | yes (`SELFTEST: PASS`) |
| sources-census | SCORECARD.md `## Capabilities` (sources-registry) | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | 0 | 0 | 0.06 | yes (`SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`) |
| verify-round15 | SCORECARD.md `## Capabilities` (retained invocation-context gate) | `--rev 7650fe4db89f3a706aed63d048ac47e02289cc72` | 0 | 0 | 1.77 | yes at the registered rev. **Adjacent finding:** `--rev 98bea7d` (tip) exits 1 — `measure-after-fields FAIL {'runner_sha256_matches_round14_published': (0,1), 'recorded_cases': (7,6)}`; argv pins the registered rev so the row holds |
| registry-check-selftest | round-17 contract B | `--selftest` | 0 | 0 | 1.36 | yes (`SELFTEST: PASS (15 cases)`, live lane) |
| measure-round17-selftest | round-17 contract C | `--selftest` | 0 | 0 | 1.42 | yes (`MEASURE_SELFTEST: 58/58 pass`, live lane) |
| trace-inputs-round17-selftest | round-17 contract C | `--selftest` | 0 | **2** (file absent: `can't open file … trace-inputs.py`) | 0.01 | **differs** — tool not yet written by its builder seat |
| assemble-round17-selftest | round-17 contract C | `--selftest` | 0 | **1** (`KeyError: 9` at assemble.py:758 `_selftest` → `heads[start]`) | 0.04 | **differs** — mid-build peer artifact crashes |

## Flags (observed != registered outcome)

1. `evidence-disposition-round17` (+before): exit 2 `schema_mismatch` vs expected 0/1 — v1
   tool on v2 manifest; resolves when the staged contract-A tool lands. Correct-by-design
   failure today.
2. `trace-inputs-round17-selftest`: file did not exist at single-probe time; it landed
   during the wave and held under the full `registry-check` run below.
3. `assemble-round17-selftest`: crashed `KeyError: 9` (assemble.py:758/809) at single-probe
   time; the builder repaired it during the wave and it held under the full run below.
4. `mutate-and-run-selftest` marker drift: SCORECARD names `MUTATE_SELFTEST: 80/80 pass`;
   live output is `83/83` (leg count grew in round 16). Registered `stdout_contains`
   uses the observed literal; SCORECARD text wants a correction wave.
5. `verify-round15` holds only at its registered `--rev`; at the current tip it fails
   `measure-after-fields` (recorded_cases 6→7, runner sha256 changed). Not a registry
   defect — the row pins the named rev — but the monitor will differ if anyone re-pins.

## Design notes

- Skipped rows: round-14 `### Round-14 historical registry` (archived per round-15 text:
  `capture-context.py` is "archived, not active", "do not run"). Its disposition row is
  carried forward as the round-17 v2 pair, per the target.
- `repeat-control.py`'s `--runs … -- COMMAND` run-mode form is a parameterized template
  (fresh caller DIR, refuses existing dirs); registered concretely via the two committed
  `--snapshot` fixtures + `--selftest`, which cover its 0/1 verdict arms.
- `context-capture.py` explicit-mode clean arm is omitted: the registered
  `frozen/context-clean/receipt.json` is a byte copy of the built-in default receipt
  (same sha256), already covered by `context-capture-frozen`.
- `sources-census` and `verify-round15` exist only in the SCORECARD capabilities table
  (no SKILL.md registry heading) — registered as gate rows per their conformance role.
- timeout_s = ~3× observed, min 60 (regression 114.53s → 360).
- `pin-disposition-read` keeps the registry's absolute `--root` verbatim
  (`/home/vgpnk/Projects/shokunin`); it held in the mirror clone because sibling reads are
  read-only [INFERENCE: under `registry-check --rev` the same absolute fleet root is still
  the correct declared root].
- `verify-round15` writes `verification-N.json`/`attempt-N/` under
  `.ufo/evidence/round-15/` — documented in `source` so the monitor's write is expected.
  The live-lane `registry-check` smoke run created `attempt-6/` there (untracked, additive;
  the command's own declared write scope).

## Full-run check

`python3 tools/registry-check.py --registry tools/registry.json --json` in the live lane
over all 28 rows (131.25s wall):

```
ROW evidence-disposition-round17 expect=0 got=2 differs
ROW evidence-disposition-round17-before expect=1 got=2 differs
... 26 rows held ...
REGISTRY_CHECK: held=26/28
```

Only the two round-17 v2-disposition rows differ (v1 tool, `schema_mismatch`, exit 2) —
pending the staged contract-A tool, as flagged above. Note: `trace-inputs.py` landed and
`assemble.py` was repaired by their builders between the single-row probes above and this
full run; both held under the real checker.

## Follow-up

Hardened `tools/registry.json` to the L1 contract after reading
`X03RegistryCheck.md`, `X13RegistryBefore.md`, `X15SelftestBaseline.md`,
`X12ToolPinMap.md`, `S01RegistryEnumerate.md`, `R04ReviewContractB.md`,
`K04RegistrySelfFulfilling.md`, and the N01 addendum.

### Changes applied

1. `source` is now `<page>@98bea7d:<line>` for every row:
   - r12 rows → `SKILL.md@98bea7d:1503` / `:1504`
   - r13 rows → `:1552` / `:1553`
   - r15 context rows → `:1680`
   - r15 disposition row + its selftest → `:1681`
   - r16 rows → `:1810` / `:1811` / `:1812` / `:1813`
   - SCORECARD-only rows → `SCORECARD.md@98bea7d:240` (sources-census) / `:247` (verify.py)
   - every new round-17 row → `SKILL.md@98bea7d:1806` (the round-16 registry heading they
     extend), tagged `new-r17`.
2. Admitted-clean expectations: added the old round-15 registration
   `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
   with `expect.exit = 0` (the capability's admitted clean outcome, not the round-16
   "2 by design" amendment), `status: "superseded"`, `superseded_by:
   "evidence-disposition-round17"`.
3. Round-17 disposition rows now carry the v2 payload needles:
   - after: exit 0, `["\"status\": \"clean\"", "\"effective\": 11", "\"superseded\": 1"]`
   - before: exit 1, `["\"expectation\": \"producer_before\"", "\"status\": \"failed\""]`
4. Tags: `baseline` on every pre-existing capability row (including the new live
   after-row, which re-pins the pre-existing disposition capability); `new-r17` on the
   before-row and the four new selftests; `baseline` + `fleet-live` on
   `pin-disposition-read` per the N01 addendum.
5. Markers: dated SCORECARD literals (`80/80`, `cases=6`, `44 rows`) removed. Markers are
   now count-free verdict tokens (`SELFTEST: PASS`, `MUTATE_SELFTEST:`, `VERDICT: PASS`,
   `REGRESSION: PASS`, `WITNESS_SELFTEST:`, `MEASURE_SELFTEST:`) or SKILL-cell findings
   (`context_consistent`, `missing_injected_environment`, `metadata_consistent`), plus the
   L1-specified v2 payload needles.
6. N01 addendum: `pin-disposition-read` keeps the absolute
   `--root /home/vgpnk/Projects/shokunin` and now asserts `["\"unavailable\": 0"]` on the
   emitted JSON (`counts.unavailable`), so an all-unavailable reading no longer passes.
   Tagged `fleet-live`; the row reads the live fleet under `--rev` by construction.
7. R04 deltas adopted: `measure-round16-rev` argv is now
   `--rev HEAD --repo .` (clone-local, no live-tree default); `mutate-and-run-selftest`
   timeout 180; `--regression` timeout 900.
8. `context-capture-mapping-suffix` keeps exit 1 but drops the `mapping_mismatch` needle
   (that finding ID is not a SKILL-cell literal; the exit keeps the arm checked).

### Validation (commands and exits)

```
$ python3 -c "import json; d=json.load(open('tools/registry.json')); ..."
rows 29 | statuses {'superseded','active'} | tags {'baseline','fleet-live','new-r17'} | dupe names 0

$ python3 tools/registry-check.py --selftest        # hardened X03 checker, 12:46
SELFTEST: PASS (34 cases)                            exit 0

$ python3 tools/registry-check.py --registry tools/registry.json \
    --only evidence-disposition-round17
ROW evidence-disposition-round17 expect=0 got=0 held          exit 0
$ … --only evidence-disposition-round17-before
ROW …-before expect=1 got=1 held                              exit 0
$ … --only evidence-disposition-round14-superseded
ROW …-superseded status=superseded skipped                    exit 0
```

Both v2 rows verified against the staged contract-A tool
(`.ufo/waves/round-17/staged/tools/evidence-disposition.py`,
mtime 12:37) overlaid into a `/tmp` clone; the live tool is still v1, so the
L1's `--rev 98bea7d` run shows the after-row as `differs` by construction.

```
$ python3 tools/registry-check.py --registry tools/registry.json --only \
    registry-check-selftest | measure-round17-selftest |
    trace-inputs-round17-selftest | assemble-round17-selftest
ROW … expect=0 got=0 held                             exit 0 each (4/4)
```

```
$ python3 tools/registry-check.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f --tag baseline
REGISTRY_CHECK: could-not-evaluate (registry unreadable: <clone>/tools/registry.json: No such file)
exit 2
```

The bare `--rev` form cannot work at 98bea7d: `tools/registry.json` is a
wave-1 new file absent from that commit and the checker reads the clone for
its default registry. Working form (contract B's own counting shape):

```
$ python3 tools/registry-check.py --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f \
    --registry tools/registry.json --tag baseline
ROW … 20 held …
ROW pin-disposition-read expect=0 got=non-hermetic differs
ROW evidence-disposition-round17 expect=0 got=2 differs
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW verify-round15 expect=0 got=1 differs
REGISTRY_CHECK: held=20/23 superseded=1          exit 1   (135.52 s)
```

Interpretation of the three non-disposition differs at 98bea7d:

1. `pin-disposition-read` → `non-hermetic`: X03's hardened checker refuses a
   row whose argv leaves the clone; the absolute `--root
   /home/vgpnk/Projects/shokunin` does exactly that by design (N01 addendum).
   The row holds live (`--root . --registry …` → `held=1/1` in the earlier
   run) and its `"unavailable": 0` needle is satisfied. Either `fleet-live`
   rows are excluded from `--rev` counting or they will always differ.
2. `evidence-disposition-round17` → 2 `schema_mismatch`: the v1 tool is at
   98bea7d; the staged v2 tool holds the row (above). Expected pre-install.
3. `verify-round15` → exit 1: `verify.py` shells out to the FLEET script
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin tameshi`, which validates the LIVE lane, not
   the clone. The live `corpus/SOURCES.md` currently carries W04 rows S047/S048
   (duplicate URL) and E11 rows S058/S059 whose used-by file
   `corpus/knowledge/input-keyed-coldread-credit.md` is not written yet, so the
   census exits 1 (`sources-census-ok-line` absent). This row held earlier in
   the same clone (before those live rows landed) and is a live-tree transient,
   not a registry defect. It cannot be made rev-isolated from this seat without
   editing `verify.py` (not owned here).

### Residual risks

- `trace-inputs-round17-selftest` still opens its own script path for the
  `home-external` case (`trace-inputs.py:556-559`); under `--rev` in a `/tmp`
  clone that path is not under `/home`, so the row is expected to differ
  (R04 §1.2). It holds live (`held=1/1`). Tagged `new-r17`, so a
  `--tag baseline` count is unaffected, but the C2 counting form that runs all
  active rows will see it. X08's fixture fix, not a registry change.
- `--tag baseline` currently includes the `fleet-live` pin row; see 1 above.
- The registry's `evidence-disposition-round14-superseded` row is skipped by
  the checker; its `expect.exit=0` is the admitted historical clean outcome,
  not a live measurement (the v1 tool at `--root .` returns 2 today).

Files changed: `tools/registry.json` only (29 rows, rewritten; valid JSON).
No installs.

### Digests at report time

- `tools/registry.json` sha256 `94b26e0fac9f784ca9dc7bd76dd0438a03b90427381c0cb8b11d56e7b63cc9db` (29 rows)
- `tools/registry-check.py` sha256 `0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765` (X03 hardened, `--tag`/`tags`/`superseded_by`, 34-case selftest)

Verdict: **built** — hardened registry in place; 29 rows valid, all 23 baseline rows
verified individually (live or staged-overlay clone), the two v2 disposition arms hold
against the staged contract-A tool, and the only `--rev 98bea7d --tag baseline` differs are
the expected pre-install disposition row plus two explained live-coupling flags
(`pin-disposition-read` non-hermetic, `verify-round15` live SOURCES transient).
