# M01 — R16-C2b input-drift mutation probe

## Scope and axes

- **Calibration:** does a credited instruction lose credit when an executed lane input changes, without changing the instruction text?
- **Depth:** one concrete, behavior-bearing byte mutation, with an observed effect and exact restoration rather than a hypothetical counterexample.
- **Operability guard:** only the isolated clone was mutated. No live instrument, sibling source, historical evidence, or round contract was changed. This report does not judge the round.

Base: `98bea7da5801f4bc58e4187690ee1687c8a5061f`.
Scratch: `/tmp/tameshi-r17w1-M01ShaOnlyHole-fqeOS9`.
Clone: `/tmp/tameshi-r17w1-M01ShaOnlyHole-fqeOS9/fleet/tameshi-shokunin`.
The clone used the required fleet-mirror layout; other lane repositories were only symlinked beside it. Clone/checkout commands exited 0. All git writes below were confined to this clone. No tools were installed or updated.

## Mutant and credited instruction

**Exactly one character changed:** `tools/evidence-disposition.py:1081`, in `emit_could_not_evaluate`, changed `return 2` to `return 0`. The JSON payload still reports `could_not_evaluate` and `exit: 2`, but the process falsely succeeds. This is a plausible exit-map defect, not a comment-only edit.

The affected credited instruction is `SKILL.md:1563-1595`, **“Effective expectation reconciliation — round 14”**. Its recipe executes `tools/evidence-disposition.py`; its decision table classifies changed pinned inputs as could-not-evaluate (`SKILL.md:1574`). The retained reader report `.ufo/waves/round-16/w1/CR26.md:27-28` records executing the tool against both disposition manifests. The round-16 ledger at `.ufo/evidence/round-16/coldread/ledger.json:1735-1751` records this bucket as:

```text
class=instruction
verdict=gap-minor
blocking_gaps=0
wrong_expectations=0
commands_executed_count=4
seats=[CR26]
section_sha256=e8720037c0b1bd43db7b21fe2dd9a2669fe64db11f72649c754c85d1832e7cbd
```

The round-16 instrument grants credit from the section hash and verdict/count fields (`.ufo/evidence/round-16/measure.py:178-215,243-265`); it does not bind that entry to the tool bytes it executed.

## Expected detector and actual outputs

The same bounded detector was run on pristine, committed mutant, and committed restored bytes. Every subprocess had a 30-second timeout and completed without timeout.

1. **Assigned measurement:** run the unchanged round-16 `measure.py` at the phase commit. A detector enforcing input-keyed credit should remove the selected bucket after the input changes. The baseline measurement must first evaluate successfully.
2. **Behavior witness:** invoke the tool with a deliberately absent disposition file under this scratch root. Its correct process exit is **2** with finding `dispositions_missing`. This establishes that the one-character input mutation actually changes behavior. An expected exit 2 is not a failed baseline.

### Commands executed

These variable assignments abbreviate the absolute paths and exact commits used in the subprocess argv; each measurement and witness was invoked separately, with cwd equal to `C`:

```sh
C=/tmp/tameshi-r17w1-M01ShaOnlyHole-fqeOS9/fleet/tameshi-shokunin
W=/tmp/tameshi-r17w1-M01ShaOnlyHole-fqeOS9
BASE=98bea7da5801f4bc58e4187690ee1687c8a5061f
MUTANT=5d6b9d5566ca0c8577c97aa17fd2a48aa41ed7b1
RESTORED=15e46311eec82297a13db2d465d8c70733f8e242

python3 "$C/.ufo/evidence/round-16/measure.py" --repo "$C" --rev "$BASE"
python3 "$C/tools/evidence-disposition.py" --root "$C" --dispositions "$W/missing-dispositions.json" --json

# After the one-character edit, committed only in the clone:
git -C "$C" add -- tools/evidence-disposition.py
git -C "$C" -c user.name=TameshiR17.M01ShaOnlyHole -c user.email=tameshi-r17-m01@mutation.invalid -c commit.gpgsign=false commit -qm 'M01 probe: return success for could-not-evaluate'
python3 "$C/.ufo/evidence/round-16/measure.py" --repo "$C" --rev "$MUTANT"
python3 "$C/tools/evidence-disposition.py" --root "$C" --dispositions "$W/missing-dispositions.json" --json

# After restoring return 2, committed only in the clone:
git -C "$C" add -- tools/evidence-disposition.py
git -C "$C" -c user.name=TameshiR17.M01ShaOnlyHole -c user.email=tameshi-r17-m01@mutation.invalid -c commit.gpgsign=false commit -qm 'M01 probe: restore exact pristine disposition bytes'
python3 "$C/.ufo/evidence/round-16/measure.py" --repo "$C" --rev "$RESTORED"
python3 "$C/tools/evidence-disposition.py" --root "$C" --dispositions "$W/missing-dispositions.json" --json
```

Both `git add` and both commits exited **0**. `git rev-parse HEAD` returned the mutant and restored hashes above, respectively, each with exit 0.

### Measurement results

| Phase | `measure.py` process exit | Covered/total | `missing` | `box3_full_page` | Calibration restraint | Selected bucket credited |
|---|---:|---:|---|---|---:|---|
| pristine | 0 | 54/54 | `[]` | `true` | 8 | yes |
| mutant | 0 | 54/54 | `[]` | `true` | 8 | yes |
| restored | 0 | 54/54 | `[]` | `true` | 8 | yes |

All three actual measurement outputs contained these unchanged key lines:

```json
{
  "calibration_restraint_score": 8,
  "coldread": {
    "box3_full_page": true,
    "ledger_present": true,
    "missing": [],
    "sections_covered": 54,
    "sections_total": 54,
    "uncovered_headings": []
  }
}
```

This is a key-field excerpt, not the complete output. All three also reported `depth_score: 7`, `recorded_cases: 7`, and `shonen.box3_points: true`. Their `revision` fields were the respective exact commits above. With no missing bucket anywhere, the selected unchanged instruction remained credited.

### Behavior-witness results

| Phase | Expected process exit | Actual process exit | Payload `status` | Payload `exit` | Payload `id` |
|---|---:|---:|---|---:|---|
| pristine | 2 | 2 | `could_not_evaluate` | 2 | `dispositions_missing` |
| mutant | 2 | **0** | `could_not_evaluate` | 2 | `dispositions_missing` |
| restored | 2 | 2 | `could_not_evaluate` | 2 | `dispositions_missing` |

All three named the same absent path, `/tmp/tameshi-r17w1-M01ShaOnlyHole-fqeOS9/missing-dispositions.json`, and produced no stderr. Thus the independent exit-map witness kills the mutant while the assigned round-16 credit measurement does not.

## Hashes and exact restoration

SHA-256 values were computed from `git -C "$C" show REV:PATH` bytes for all three phase commits. Each `git show` exited 0.

| Path | Pristine SHA-256 | Mutant SHA-256 | Restored SHA-256 |
|---|---|---|---|
| `tools/evidence-disposition.py` | `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95` | `209ca3ecdfa27cb4373e9e02f297192f8c95d502fd64130207fcd2bd328254b6` | `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95` |
| `SKILL.md` | `906fb64961fd8f41bb673a0919ef0b77bcca46ad005215ae96e4b3df97011397` | same | same |
| `.ufo/evidence/round-16/measure.py` | `03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb` | same | same |
| `.ufo/evidence/round-16/coldread/ledger.json` | `b84151a35f0cefa0716f3dd200a183dee5badc7be09ba1bac11d61283f70623c` | same | same |

The byte comparison printed `EXACT_TOOL_BYTES_RESTORED=true`. The following command also exited 0:

```sh
git -C /tmp/tameshi-r17w1-M01ShaOnlyHole-fqeOS9/fleet/tameshi-shokunin rev-parse '98bea7da5801f4bc58e4187690ee1687c8a5061f^{tree}' '5d6b9d5566ca0c8577c97aa17fd2a48aa41ed7b1^{tree}' '15e46311eec82297a13db2d465d8c70733f8e242^{tree}'
```

Actual output, pristine / mutant / restored:

```text
4e9f7450d96fc12bc615e1a6fb87a9e7e90616b2
1673246bc341bb0bfde04842a4c2c6a33a8bdc8d
4e9f7450d96fc12bc615e1a6fb87a9e7e90616b2
EXACT_TRACKED_TREE_RESTORED=true
```

The scratch clone is retained at the restored commit so the mutant commit remains inspectable. No live lane source was modified.

## Optional round-17 measure v2

At the final availability check, `glob` with `hidden=true`, `gitignore=false`, path `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-17/*` returned only `op1-redbefore-98bea7d.txt`, `census-start.txt`, and the `redbefore/` directory. **`measure.py` did not exist there.** No v2 command was run, and no v2 result is claimed. This does not grade X07's pending implementation.

## Probe verdict

The mutant **SURVIVED the round-16 credit detector**: baseline and restored runs evaluated successfully, and the mutant retained 54/54 coverage and restraint 8 despite a behavior-changing dependency edit. The separate exit-map witness **KILLED** it (2 → 0 → 2). This is the requested R16-C2b coverage finding, not permission to relax the contract.

falls — round-16 input-drift invalidation is absent; the selected bucket stays credited after its executed tool changes; exact bytes and the entire tracked tree were restored.
