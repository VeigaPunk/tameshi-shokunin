# MutFixtures — round-24 private mutation probe

**Verdict: three survived, three were killed, none were inconclusive.** The surviving single-line mutants are per-token argv prefix matching, absolute-value exit comparison, and exit truthiness comparison. Each retained `COMMAND_BINDING_SELFTEST: 44/44 pass` / process exit 0 while accepting a concrete mismatch that pristine and restored bytes rejected. These are additional selftest coverage findings, not defects observed in the delivered exact comparisons and not a rejection of the eleven frozen predicates.

## Axes and bounds

- **Calibration (assigned axis):** distinguish the named predicate guarantee from broader mutation adequacy, with observed outputs rather than inferred coverage.
- **Probe coverage:** exercise stripping, ordered de-duplication, both whole-vector and per-token prefix matching, absolute-value exits, and truthiness exits independently.
- **Isolation/restoration:** one behavior-bearing line per private child clone; byte-exact restoration and the same bounded public detector before, during, and after each mutation.

Measured revision: `c8c5b88c8e961a929cdc351b95a7074c76958909` (observed `git rev-parse HEAD` in the private root clone). All repository source anchors below refer to that revision. No production code, fixture, registry, index, or lane state was modified. The only production-tree write is this report. No subagents or other runtime were invoked. No tools were installed or updated.

The frozen contract explicitly says K1–K4 count four specific mutants, not general mutation adequacy: `.ufo/evidence/round-24/contract.json:60-64`. No producer-authentication, promotion, historical closure, or numerical score-uplift claim is made.

## Setup and bounded detector

Executed setup:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/TameshiR24-2-MutFixtures-r24 && git -C /tmp/TameshiR24-2-MutFixtures-r24 checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909
```

Both setup commands completed with no stdout/stderr. From that private root, six independent child clones were created using `git clone -q --no-hardlinks . probe-NAME && git -C probe-NAME checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909`, with NAME equal to each of `strip`, `dedupe`, `prefix`, `token-prefix`, `abs`, `truthy`. Child clone setup also completed with no stdout/stderr. Independent detectors ran concurrently; a clone's source was never edited while its detector was running.

For every child, cwd was `/tmp/TameshiR24-2-MutFixtures-r24/probe-NAME`. The identical detector was run on pristine, mutated, and restored bytes:

```sh
env TMPDIR=/tmp/TameshiR24-2-MutFixtures-r24/probe-NAME PYTHONDONTWRITEBYTECODE=1 python3 tools/command-binding.py --selftest
```

The mutation/restoration runs used equivalent subprocess environment variables and argv directly (no shell). Each invocation had a 120-second outer deadline; the public selftest also bounds each fixture subprocess at 15 seconds (`tools/command-binding.py:174-194`). The root clone had a separate initial pristine `44/44 pass` run before creating children. No registry battery, replay, gate, or selftest was run in production.

The CLI selftest's literal expectations and loaded fixture files were not changed (`tools/command-binding.py:132-194`, especially `164-169`). Exact production comparison anchors are `tools/command-binding.py:103-110`; the documented exact argv/integer-exit contract is `tools/command-binding.py:7-9`.

## Results and exact mutants

Every child baseline and every restored run emitted `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, empty stderr. Mutation output is retained verbatim below. A nonzero selftest means the deliberately defective implementation was detected, not a baseline failure.

| Child | Replaced line | Mutated selftest | Process exit | Verdict | Failing selftest cases |
|---|---:|---|---:|---|---|
| `strip` | 103 | `COMMAND_BINDING_SELFTEST: 43/44 pass` | 1 | **killed** | `argv-padded-token` |
| `dedupe` | 103 | `COMMAND_BINDING_SELFTEST: 43/44 pass` | 1 | **killed** | `argv-repeated-flag` |
| `prefix` | 103 | `COMMAND_BINDING_SELFTEST: 42/44 pass` | 1 | **killed** | `argv-extra`, `argv-repeated-flag` |
| `token-prefix` | 103 | `COMMAND_BINDING_SELFTEST: 44/44 pass` | 0 | **survived** | none |
| `abs` | 109 | `COMMAND_BINDING_SELFTEST: 44/44 pass` | 0 | **survived** | none |
| `truthy` | 109 | `COMMAND_BINDING_SELFTEST: 44/44 pass` | 0 | **survived** | none |

### Observed common pristine/restored output

All six pristine child runs and all six restored child runs emitted this passing stdout; stderr was empty and process exit was 0 in every run:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra PASS
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token PASS
CASE argv-repeated-flag PASS
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 44/44 pass
```

### Mutant `strip`

Expected detector: `argv-padded-token` must fail the selftest under stripping.

Exact replacement text at `tools/command-binding.py:103` in this child clone only:

```python
        if [token.strip() for token in receipt['argv']] != [token.strip() for token in required['argv']]:
```

Actual mutated stdout:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra PASS
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token FAIL
CASE argv-repeated-flag PASS
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 43/44 pass
```

Observed selftest process exit: `1`; stderr: `''`.

### Mutant `dedupe`

Expected detector: `argv-repeated-flag` must fail the selftest under ordered de-duplication. This mutant de-duplicates all argv tokens, not only flags.

Exact replacement text at `tools/command-binding.py:103` in this child clone only:

```python
        if list(dict.fromkeys(receipt['argv'])) != list(dict.fromkeys(required['argv'])):
```

Actual mutated stdout:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra PASS
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token PASS
CASE argv-repeated-flag FAIL
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 43/44 pass
```

Observed selftest process exit: `1`; stderr: `''`.

### Mutant `prefix`

Expected detector: `argv-extra` and `argv-repeated-flag` must fail the selftest when an entire receipt argv suffix is ignored.

Exact replacement text at `tools/command-binding.py:103` in this child clone only:

```python
        if receipt['argv'][:len(required['argv'])] != required['argv']:
```

Actual mutated stdout:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra FAIL
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token PASS
CASE argv-repeated-flag FAIL
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 42/44 pass
```

Observed selftest process exit: `1`; stderr: `''`.

### Mutant `token-prefix`

Expected detector: A same-argc token-extension mismatch should kill per-token prefix comparison; this probe checks whether the 44 cases provide such discrimination.

Exact replacement text at `tools/command-binding.py:103` in this child clone only:

```python
        if len(receipt['argv']) != len(required['argv']) or any(not actual.startswith(expected) for actual, expected in zip(receipt['argv'], required['argv'])):
```

Actual mutated stdout:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra PASS
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token PASS
CASE argv-repeated-flag PASS
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 44/44 pass
```

Observed selftest process exit: `0`; stderr: `''`.

### Mutant `abs`

Expected detector: An equal-magnitude, opposite-sign exit mismatch should kill absolute-value comparison; `-9` versus `0` alone cannot do that.

Exact replacement text at `tools/command-binding.py:109` in this child clone only:

```python
        if abs(receipt['exit']) != abs(required['expect']['exit']):
```

Actual mutated stdout:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra PASS
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token PASS
CASE argv-repeated-flag PASS
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 44/44 pass
```

Observed selftest process exit: `0`; stderr: `''`.

### Mutant `truthy`

Expected detector: Two distinct nonzero exit integers should kill truthiness comparison; zero/nonzero mismatches alone cannot do that.

Exact replacement text at `tools/command-binding.py:109` in this child clone only:

```python
        if bool(receipt['exit']) != bool(required['expect']['exit']):
```

Actual mutated stdout:

```text
CASE clean-with-expected-red PASS
CASE source-read-not-command PASS
CASE wrong-cwd PASS
CASE stale-revision PASS
CASE missing PASS
CASE duplicate PASS
CASE unknown PASS
CASE wrong-exit PASS
CASE stderr-cannot-supply-token PASS
CASE bool-exit PASS
CASE empty-requirements PASS
CASE duplicate-requirement PASS
CASE noncanonical-cwd PASS
CASE short-revision PASS
CASE string-exit PASS
CASE bool-expected-exit PASS
CASE blank-argv PASS
CASE argv-order PASS
CASE argv-missing PASS
CASE argv-extra PASS
CASE argv-joined-collision PASS
CASE argv-normalized PASS
CASE argv-second-only PASS
CASE unknown-added PASS
CASE all-stale PASS
CASE second-cwd PASS
CASE multiple-findings PASS
CASE receipt-order-clean PASS
CASE stderr-clean PASS
CASE stdout-surround-clean PASS
CASE duplicate-before-malformed PASS
CASE unknown-expect-key PASS
CASE unknown-receipt-key PASS
CASE unknown-bundle-key PASS
CASE argv-shell-string PASS
CASE all-of-tokens PASS
CASE argv-swapped-between-names PASS
CASE argv-case-only PASS
CASE argv-padded-token PASS
CASE argv-repeated-flag PASS
CASE negative-exit-mismatch PASS
CASE negative-exit-declared-match PASS
CASE tampered PASS
CASE duplicate-json-key PASS
COMMAND_BINDING_SELFTEST: 44/44 pass
```

Observed selftest process exit: `0`; stderr: `''`.

## Concrete counterexamples, observed on all three phases

These supplemental probes call the real `evaluate()` loaded by the same `python3` via `runpy.run_path('tools/command-binding.py')`. They are not substitutions for, additions to, or a modification of the 44-case detector. They confirm that a surviving mutant changes actual comparison behavior. The executed command argv was `python3 -c EXAMPLE_CODE NAME`, with the same child cwd/environment and a 120-second deadline. Exact EXAMPLE_CODE:

```python
import copy, json, runpy, sys
m = runpy.run_path('tools/command-binding.py')
kind = sys.argv[1]
required_argv = ['gate', '--check']
receipt_argv = list(required_argv)
expected_exit = actual_exit = 0
if kind == 'strip': receipt_argv[1] = ' --check'
elif kind == 'dedupe': receipt_argv.append('--check')
elif kind == 'prefix': receipt_argv.append('--skip')
elif kind == 'token-prefix': receipt_argv[1] = '--check-extra'
elif kind == 'abs': expected_exit, actual_exit = 1, -1
elif kind == 'truthy': expected_exit, actual_exit = 1, 2
bundle = {'schema': 'command-binding-v1', 'revision': '1' * 40, 'cwd': '/fixture/repo', 'requirements': [{'name': 'one', 'argv': required_argv, 'expect': {'exit': expected_exit, 'stdout_contains': ['CLEAN']}}], 'receipts': [{'name': 'one', 'argv': receipt_argv, 'cwd': '/fixture/repo', 'revision': '1' * 40, 'exit': actual_exit, 'stdout': 'CLEAN\n', 'stderr': ''}]}
code, findings = m['evaluate'](bundle)
print(json.dumps({'probe': kind, 'required_argv': required_argv, 'receipt_argv': receipt_argv, 'expected_exit': expected_exit, 'actual_exit': actual_exit, 'evaluate_exit': code, 'finding_ids': findings}, sort_keys=True))
```

Every supplemental probe process exited 0 with empty stderr; the JSON `evaluate_exit` field is the validator result, not the probe process status. Every mutation accepted its designated mismatch; every pristine/restored implementation rejected it. Actual stdout, by phase:

### `strip`

```text
pristine: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "strip", "receipt_argv": ["gate", " --check"], "required_argv": ["gate", "--check"]}
mutated: {"actual_exit": 0, "evaluate_exit": 0, "expected_exit": 0, "finding_ids": [], "probe": "strip", "receipt_argv": ["gate", " --check"], "required_argv": ["gate", "--check"]}
restored: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "strip", "receipt_argv": ["gate", " --check"], "required_argv": ["gate", "--check"]}
```

### `dedupe`

```text
pristine: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "dedupe", "receipt_argv": ["gate", "--check", "--check"], "required_argv": ["gate", "--check"]}
mutated: {"actual_exit": 0, "evaluate_exit": 0, "expected_exit": 0, "finding_ids": [], "probe": "dedupe", "receipt_argv": ["gate", "--check", "--check"], "required_argv": ["gate", "--check"]}
restored: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "dedupe", "receipt_argv": ["gate", "--check", "--check"], "required_argv": ["gate", "--check"]}
```

### `prefix`

```text
pristine: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "prefix", "receipt_argv": ["gate", "--check", "--skip"], "required_argv": ["gate", "--check"]}
mutated: {"actual_exit": 0, "evaluate_exit": 0, "expected_exit": 0, "finding_ids": [], "probe": "prefix", "receipt_argv": ["gate", "--check", "--skip"], "required_argv": ["gate", "--check"]}
restored: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "prefix", "receipt_argv": ["gate", "--check", "--skip"], "required_argv": ["gate", "--check"]}
```

### `token-prefix`

```text
pristine: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "token-prefix", "receipt_argv": ["gate", "--check-extra"], "required_argv": ["gate", "--check"]}
mutated: {"actual_exit": 0, "evaluate_exit": 0, "expected_exit": 0, "finding_ids": [], "probe": "token-prefix", "receipt_argv": ["gate", "--check-extra"], "required_argv": ["gate", "--check"]}
restored: {"actual_exit": 0, "evaluate_exit": 1, "expected_exit": 0, "finding_ids": ["ARGV_MISMATCH"], "probe": "token-prefix", "receipt_argv": ["gate", "--check-extra"], "required_argv": ["gate", "--check"]}
```

### `abs`

```text
pristine: {"actual_exit": -1, "evaluate_exit": 1, "expected_exit": 1, "finding_ids": ["EXIT_MISMATCH"], "probe": "abs", "receipt_argv": ["gate", "--check"], "required_argv": ["gate", "--check"]}
mutated: {"actual_exit": -1, "evaluate_exit": 0, "expected_exit": 1, "finding_ids": [], "probe": "abs", "receipt_argv": ["gate", "--check"], "required_argv": ["gate", "--check"]}
restored: {"actual_exit": -1, "evaluate_exit": 1, "expected_exit": 1, "finding_ids": ["EXIT_MISMATCH"], "probe": "abs", "receipt_argv": ["gate", "--check"], "required_argv": ["gate", "--check"]}
```

### `truthy`

```text
pristine: {"actual_exit": 2, "evaluate_exit": 1, "expected_exit": 1, "finding_ids": ["EXIT_MISMATCH"], "probe": "truthy", "receipt_argv": ["gate", "--check"], "required_argv": ["gate", "--check"]}
mutated: {"actual_exit": 2, "evaluate_exit": 0, "expected_exit": 1, "finding_ids": [], "probe": "truthy", "receipt_argv": ["gate", "--check"], "required_argv": ["gate", "--check"]}
restored: {"actual_exit": 2, "evaluate_exit": 1, "expected_exit": 1, "finding_ids": ["EXIT_MISMATCH"], "probe": "truthy", "receipt_argv": ["gate", "--check"], "required_argv": ["gate", "--check"]}
```

### Why the three survivors matter

- **Per-token prefix:** required `['gate', '--check']`, receipt `['gate', '--check-extra']`, identical argc. The surviving line accepts a different flag because `actual.startswith(expected)` replaces exact token equality. Whole-vector-prefix matching was separately killed, so that killed mutant does not cover this variant.
- **Absolute-value exit:** expected `1`, receipt `-1` is accepted although the integers differ. The existing `negative-exit-mismatch` uses expected `0` / receipt `-9` (`.ufo/evidence/round-24/extra-cases.json:276-340`), still unequal after `abs()`. The declared-match fixture uses `-15` on both sides (`343-405`), still equal after `abs()`.
- **Exit truthiness:** expected `1`, receipt `2` is accepted because both are truthy. The existing `wrong-exit` base changes 0 to 1 (`tools/command-binding.py:134-154`); the negative mismatch changes 0 to -9, also crossing zero/nonzero. Both remain detectable while distinct nonzero values collapse.

Positive control anchors: stripping was killed by `argv-padded-token` (`.ufo/evidence/round-24/extra-cases.json:141-205`); ordered de-duplication was killed by `argv-repeated-flag` (`208-273`); vector-prefix acceptance was killed by `argv-extra` (`.ufo/evidence/round-23/extra-cases.json:142-211`) and the repeated-flag case.

## Hashes and exact restoration evidence

All hashes are SHA-256. Define **B0** as the observed pristine script digest:

```text
9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d  tools/command-binding.py
```

For each child, `sha256sum tools/command-binding.py` was observed before mutation and while mutated. After restoring its original one-line comparison, the script and both fixture hashes were recorded, and `cmp -s tools/command-binding.py ../tools/command-binding.py` compared it directly with the untouched private root. Each comparison exited 0 with no stdout/stderr. The original script bytes were therefore restored, not merely a behaviorally equivalent implementation.

| Child | Before script hash | Mutated script hash | Restored script hash | `cmp` exit |
|---|---|---|---|---:|
| `strip` | B0 | `fed7d6d18920cc120179324eebbff116b9ab95b5fac1efe0e185a38d3a540c19` | B0 | 0 |
| `dedupe` | B0 | `1adfd4c17952e8949bf2e5e56d11308e484f41a389c613d47b91ec945b5dfad3` | B0 | 0 |
| `prefix` | B0 | `61fbc540bbd1fa1d90c7daaed7f50f38d729e4643405139e2e84f23579cfea66` | B0 | 0 |
| `token-prefix` | B0 | `827c34999635995b90b1c34a554b804846a2d4180cf87e04fbeb52da92d04d7e` | B0 | 0 |
| `abs` | B0 | `e0ab7ecbdbf2b65a4c7fa21a1b61ed9bda75c1b2ab06f4b3552e9ef9cbc83988` | B0 | 0 |
| `truthy` | B0 | `aafb9bfa745031905e62a06ad1505f926b64ff6d4548d845aec66330cd328a5f` | B0 | 0 |

The fixture hashes observed in the pristine root were unchanged in every restored child:

```text
87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00  .ufo/evidence/round-23/extra-cases.json
6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35  .ufo/evidence/round-24/extra-cases.json
```

All six restored detector runs passed 44/44, exit 0, empty stderr; all six restored counterexamples again returned the appropriate `ARGV_MISMATCH` or `EXIT_MISMATCH`. No mutant was kept. The private clones remain restored for inspection; no production integration was attempted.

## Smallest safe correction

Keep `evaluate()`'s delivered exact argv and exact integer-exit comparisons unchanged. Add three literal negative fixtures to the existing supplemental selftest file, with all unrelated fields matching:

1. Required argv `['gate', '--check']` versus receipt `['gate', '--check-extra']`: expected validator exit 1 and `['ARGV_MISMATCH']`.
2. Expected exit `1` versus observed exit `-1`: expected validator exit 1 and `['EXIT_MISMATCH']`.
3. Expected exit `1` versus observed exit `2`: expected validator exit 1 and `['EXIT_MISMATCH']`.

These are recommendations only; no fixture/contract/production changes were made. A surviving mutant is a coverage finding, not permission to widen the frozen contract. No additional checks or broad batteries were exercised.
