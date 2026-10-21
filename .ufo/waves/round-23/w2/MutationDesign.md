## Static findings

**Axes:** anchor precision, behavioral discrimination, pristine/restored controls, evidence calibration.

No files written, commands executed, tools installed, or subagents dispatched. Findings returned here under the wave’s no-write restriction.

### Ten exact guard anchors

`mutate.py:13–22` declares ten distinct replacements. Each matches a behavior-bearing guard in `tools/command-binding.py`; `mutations-A.json` records **one occurrence per anchor**.

All ten recorded mutants exited **1**, with empty stderr and explicit `CASE … FAIL` output—not merely unexplained process failures.

| Mutant | Exact original anchor | Representative failing detector | Recorded summary |
|---|---|---|---|
| argv | `if receipt['argv'] != required['argv']:` | `source-read-not-command` | 30/38 pass |
| cwd | `if receipt['cwd'] != bundle['cwd']:` | `wrong-cwd` | 35/38 pass |
| revision | `if receipt['revision'] != bundle['revision']:` | `stale-revision` | 36/38 pass |
| membership | `if set(receipts) != set(requirements):` | `missing`, `unknown` | 35/38 pass |
| duplicate-command | `if row['name'] in receipts:` | `duplicate` | 37/38 pass |
| exit | `if receipt['exit'] != required['expect']['exit']:` | `wrong-exit` | 36/38 pass |
| stdout | `if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):` | `stderr-cannot-supply-token` | 36/38 pass |
| bool-exit | `or not revision(row.get('revision')) or type(row.get('exit')) is not int` | `bool-exit`, `string-exit` | 36/38 pass |
| snapshot-pin | `if digest != expected['bundle_sha256']:` | `tampered` | 37/38 pass |
| empty-requirements | `or not isinstance(bundle.get('requirements'), list) or not bundle['requirements']` | `empty-requirements` | 37/38 pass |

Seven comparison guards and the snapshot guard become `if False:`. The bool-exit mutant removes the integer-type check; empty-requirements removes only the nonempty requirement.

### Controls, verdict semantics, and restoration

The recorded detector is the same private-copy invocation throughout:

```text
python3 <scratch>/tools/command-binding.py --selftest
```

It has a 90-second outer timeout.

**Actual recorded outputs:** pristine and restored controls both exited **0**, printed `COMMAND_BINDING_SELFTEST: 38/38 pass`, and had empty stderr. Aggregate receipt: **10 killed, 0 survived, 0 inconclusive**, `source_unchanged: true`.

The implementation correctly marks a mutant **inconclusive** when the initial control fails or its anchor count is not exactly one (`mutate.py:49–52`). Each mutation derives from pristine `text`, so replacements are not cumulative.

**Calibration limitations:**

- Classification otherwise uses only `result['exit'] != 0`. A returned fixture-unavailable error or crash would also become “killed.” The actual receipt’s explicit behavioral failures support these ten kills; the classifier alone does not establish that distinction.
- Restoration happens once after all mutants, not after each. A failed restored control makes the overall command fail but does not revise earlier row statuses to inconclusive.
- The harness rewrites retained raw bytes before the restored control and never writes the original tool. However, the receipt lacks mutated-copy and restored-copy hashes.

Recorded original tool SHA-256:

```text
d533dc1ef114234a8ca1d6a8155f052c9b8f5001f2f4918b3eb6a3f3f59af954
```

**After-hash:** not recorded. Restoration evidence is the raw-byte rewrite, successful restored control, and original-source equality check—not an independently recorded after-digest.

### One fresh static mutation candidate

**Mutant:** weaken the exit guard at `tools/command-binding.py:109` to ignore negative receipt exits:

```python
if receipt['exit'] >= 0 and receipt['exit'] != required['expect']['exit']:
```

**Expected detector:** the existing `--selftest`.

**[INFERENCE] Expected outcome:** this mutant would survive the existing detector. Built-in fixtures contain no negative integer exits; the nineteen supplemental cases likewise contain only receipt exits `false`, `0`, and `1`, with required exits `0` and `1`. Their rejection paths and comparisons remain unchanged.

Yet a structurally valid receipt with exit `-9`, expected exit `0`, and otherwise matching fields would lose `EXIT_MISMATCH`. The implemented contract accepts integer exits without a nonnegative restriction.

**Actual output:** none; this candidate was not applied or executed.  
**Verdict:** **unexecuted / inconclusive**, with a statically supported coverage gap—not an observed survivor.  
**Restoration:** no bytes changed.

### Provenance boundary

`mutations-A.json` names revision `496d212bc46789cdf8cafab72978bdb7f4182963`. `registry-C.json` separately records the delivered revision `336565fc2e70e034307ef267aaa2018572c200d3`, including a passing 38/38 selftest and source-read rejection. That is not a new execution of the mutation suite.

The evidence supports the **finite ten-mutant kill claim**, not exhaustive mutation coverage or closure of historical R17-CMD-BIND.
