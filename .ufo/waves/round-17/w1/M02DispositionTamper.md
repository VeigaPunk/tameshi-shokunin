# M02 — disposition-gate one-byte tamper probes

## Scope and axes

Seat: `TameshiR17.M02DispositionTamper`. Axes: **depth** (independent tamper cases), **calibration** (baseline/restore-backed kill claims only), and the repaired **operability** boundary (historical tools versus live evidence). This is a scoped mutation result, not a round judgment.

Four independent one-byte substitutions were made only in my isolated scratch clone. Each changed a semantic field or a behavior-bearing runner pin; none introduced invalid JSON or changed file length. No sibling source, live lane instrument, original evidence, git index, or branch was changed. No tools were installed or updated.

Scratch root: `/tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf`.

## Detector and setup

Baseline clone root (`R1`):

```text
/tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin
```

Actual setup commands, all exit 0 (Python subprocess argv, no shell):

```text
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin
git -C /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin checkout -q 28aeef4
git -C /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin rev-parse HEAD
# stdout: 28aeef498cc070c3183271b709bc79d344ff547a
```

The fleet directories contain symlinks to existing sibling `*-shokunin` repos; the lane clone itself is not a symlink. No registered receipt argv was executed.

Identical detector argv for all nine v1 invocations, cwd `R1`, subprocess timeout **30 seconds**:

```text
python3 /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin/tools/evidence-disposition.py --root /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin --dispositions /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/fleet/tameshi-shokunin/.ufo/evidence/round-14/dispositions.json --json
```

Detector sha256: `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`.
Manifest sha256: `77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005`.

The first pristine invocation returned **0**, `status: clean`, `findings: []`, with `expected_checks=12`, `effective=11`, `passed=11`, `superseded=1`, `failed=0`. Every restored invocation returned the same exit, status, counts and empty findings. Every invocation had empty stderr. There were no timeouts.

One initial pristine run was shared across the four isolated cases; each mutation was followed by exact restoration and another detector run before the next mutation. Thus the restored run for one case also observes the pristine bytes before the next case.

## v1 kill table — 28aeef498cc070c3183271b709bc79d344ff547a

Paths below are relative to `R1`. Byte offsets are one-based, from `cmp -l` against `git show HEAD:<path>`; old/new byte values in parentheses are octal.

| Case | Mutation point | One-byte edit | Byte | Expected detector | Actual pristine → mutant → restored | Verdict |
|---|---|---|---:|---|---|---|
| Receipt | `.ufo/evidence/round-13/verification.json:27` | First `pin_selftest.exit`: `0` → `1` | 1767 (`060` → `061`) | 2 / `input_digest_mismatch` | 0 clean → **2 / `input_digest_mismatch`** → 0 clean | **killed** |
| Expected verdict | `.ufo/evidence/round-13/expected.json:21` | `expected_checks.pin_selftest.exit`: `0` → `1` | 1702 (`060` → `061`) | 2 / `input_digest_mismatch` | 0 clean → **2 / `input_digest_mismatch`** → 0 clean | **killed** |
| BashWitness evidence | `.ufo/evidence/round-12/BashWitness/summary.json:49` | `inputs.suite.declared_total`: `16` → `17` | 2182 (`066` → `067`) | 2 / `expected_input_digest_mismatch` | 0 clean → **2 / `expected_input_digest_mismatch`** → 0 clean | **killed** |
| Live runner | `tools/mutate-and-run.sh:542` | `PIN_JS=83016…` → `PIN_JS=93016…` | 25673 (`070` → `071`) | 2 / `expected_input_digest_mismatch` | 0 clean → **2 / `expected_input_digest_mismatch`** → 0 clean | **killed** |

Observed v1 result: **4 killed, 0 survived, 0 inconclusive**. A mutation is counted killed only because both its pristine and restored controls returned 0 clean.

### Actual mutant finding output

Each mutant emitted `status: could_not_evaluate`, `exit: 2`, the listed top-level `id`, and one finding with the same ID and the following detail:

```text
receipt:
  id=input_digest_mismatch
  .ufo/evidence/round-13/verification.json: observed cbb53a7f29fe8b9d40f8fc0a4d6c17a4035944e4dd764d886082ae754b74339a expects a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f
expected:
  id=input_digest_mismatch
  .ufo/evidence/round-13/expected.json: observed 14ba2ddbf7eb15b52c895c05d26b3ab52d55f0d277c34bb2bfd4c8676ce77718 expects a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336
witness:
  id=expected_input_digest_mismatch
  .ufo/evidence/round-12/BashWitness/summary.json: observed 5b3be1d66a3a319ab4ce353ef2a23e1cae0b5487485ffd967d7d551a983ac260 expects acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9
runner:
  id=expected_input_digest_mismatch
  tools/mutate-and-run.sh: observed 9016fa4245d1a1afe8a714e8fe931b45cba3f20663d34c88060037876377d51a expects 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
```

These failures match the two integrity layers in the committed detector: `tools/evidence-disposition.py:1164-1177` verifies disposition-level input pins before parsing; `:1182-1192` verifies every original expected input before evaluating predicates. This is tamper detection, not evidence that retained receipt commands were re-executed.

## Restoration evidence — exact hashes

`sha256sum` was run over all four files immediately before every detector invocation. In the table, the before and after columns are independently observed hashes, not inferred from the edit operation. All non-target files retained their original hashes during each case. `cmp -l` produced exactly one changed-byte row for each mutation and no rows after restoration.

| File | Before sha256 | Mutated sha256 | Restored sha256 |
|---|---|---|---|
| `.ufo/evidence/round-13/verification.json` | `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f` | `cbb53a7f29fe8b9d40f8fc0a4d6c17a4035944e4dd764d886082ae754b74339a` | `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f` |
| `.ufo/evidence/round-13/expected.json` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` | `14ba2ddbf7eb15b52c895c05d26b3ab52d55f0d277c34bb2bfd4c8676ce77718` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` |
| `.ufo/evidence/round-12/BashWitness/summary.json` | `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` | `5b3be1d66a3a319ab4ce353ef2a23e1cae0b5487485ffd967d7d551a983ac260` | `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` |
| `tools/mutate-and-run.sh` | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` | `9016fa4245d1a1afe8a714e8fe931b45cba3f20663d34c88060037876377d51a` | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |

Comparison-tool caveat: the host's `cmp --version` printed `cmp cmp (pi-shell) 17.2.11`. For receipt/witness/runner mutations, its differing-byte output was accompanied by status 0; the expected.json mutation returned 1. This discrepancy was reported to `xd://report_issue`. No identity or kill claim relies on `cmp`'s exit status: differing-byte rows and the independent sha256 values are recorded above; restored byte-list output was empty.

## Conditional v2 table — prerequisites unavailable

A second independent fleet-mirror clone was successfully prepared at:

```text
/tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/v2/fleet/tameshi-shokunin
```

Actual setup commands, all exit 0:

```text
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/v2/fleet/tameshi-shokunin
git -C /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/v2/fleet/tameshi-shokunin checkout -q 98bea7da5801f4bc58e4187690ee1687c8a5061f
git -C /tmp/tameshi-r17w1-M02DispositionTamper-3hwvz4nf/v2/fleet/tameshi-shokunin rev-parse HEAD
# stdout: 98bea7da5801f4bc58e4187690ee1687c8a5061f
```

The initial `glob` checks (`hidden=true`, `gitignore=false`) found neither required copy-in artifact. The blocker was sent only to `agent://TameshiR17`. Before closing this report, the manifest appeared but the staged detector still did not:

- **Missing:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-17/staged/tools/evidence-disposition.py`. The staging tools listing contained only `mutate-and-run.sh`.
- **Available:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-17/dispositions.json`, sha256 `2e7f26d86db60e5818e57ea9261960f7bb660aceaa96220a46bb949aa5a56958` (observed with `sha256sum`, exit 0). Its `historical_inputs` maps all four tools to `4acc607dfd79f19d508bd50cdd06b77269fccd1d` (`:11-27`).

The target's conjunction (“if the staged v2 tool and manifest exist”) was not met. No alternate implementation or synthetic manifest was substituted, and the second clone was not mutated.

| Case | Required v2 mutant result | Actual detector output | Verdict |
|---|---|---|---|
| Round-13 receipt | 2, integrity finding | Not run: required staged v2 detector absent | **inconclusive / unavailable** |
| expected.json | 2, integrity finding | Not run: same missing detector | **inconclusive / unavailable** |
| Round-12 BashWitness file | 2, integrity finding | Not run: same missing detector | **inconclusive / unavailable** |
| Live `tools/mutate-and-run.sh` | Not 2; a clean-capable v2 baseline should remain 0 | Not run: same missing detector | **inconclusive / unavailable** |

The v2 evidence/live-tool boundary is **unobserved**, not credited as passing or counted as a killed mutant. No v2 pristine-control failure is being misreported as a kill.

Verdict: partial — v1 tamper invariant holds for all four restored one-byte probes; conditional v2 comparison is unavailable because the assigned staged detector is absent.
