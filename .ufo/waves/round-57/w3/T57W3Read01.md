# T57W3Read01 — ## Standing rules

- Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392` (detached scratch clone).
- Frozen round-18 sectionizer: lines **17–57**, sha256 `d7042aa08484f1a8c72c7228dd668c0cb89baa83533b12b8b8f9839f0ef5093c`.
- Verdict: **verified-record**. Findings: none.
- Axes: factual calibration, command operability, pointer integrity, substrate safety.

## Executed evidence

The section was read end to end. `pointers.py` imports the frozen sectionizer, reads the C0b blob with `git -C ... show`, and prints its boundary/hash. Pointer sweep confirmed PROVINCE, both mutation census notes, scratch-root knowledge note, registry, gate, round-55/56 counters, S278/S279 rows, and the errata disclosure. The cited census lines support read-only copied mutants and no secret content reads; PROVINCE retains sibling ownership.

- Nine documented allocating modes: unusable TMPDIR → exit 2, correct single stderr line, no traceback.
- Five non-allocating modes: same unusable TMPDIR → expected exit 0.
- Seven helpers × unset/empty/usable: **21/21** correct root selections.
- Receipt gate: **GATE_SELFTEST: 19/19 pass**, exit 0; exercises identity, content-equivalent rerouting, drift, strict mismatch, absent/unresolvable revisions, control ancestry, and unresolvable certified exit 2. Table codes agree with canonical check logic at tools/receipt-revision-gate.py:125-159 and selftest observations.
- Seven historical helper registry cells present. Literal tracked round-48–52 w1/w2 census: **3202 files; dash=0, slash=7354**.

## Commands and outputs

Full commands, cwd, TMPDIR, exits, stdout and stderr are in the sibling JSON and individual `T57W3Read01-receipts/*.json` files. Each command actually ran; expected refusal exits are not failures of the documented behavior.

### repeat-control-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/repeat-control.py --selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/repeat-control-selftest.json`.

### registry-check-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/registry-check.py --selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/registry-check-selftest.json`.

### bash-witness-study-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/bash-witness-study.py selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/bash-witness-study-selftest.json`.

### pin-disposition-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/pin-disposition.py --selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/pin-disposition-selftest.json`.

### evidence-disposition-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/evidence-disposition.py --selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/evidence-disposition-selftest.json`.

### context-capture-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/context-capture.py --selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/context-capture-selftest.json`.

### env-diff-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/env-diff.py --selftest
```
Exit: 2. Receipt: `T57W3Read01-receipts/env-diff-selftest.json`.

### env-diff-contract

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/env-diff.py --contract .ufo/evidence/round-55/c2/fixture-contract.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read01/envdiff-out.json --fleet-root /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone
```
Exit: 2. Receipt: `T57W3Read01-receipts/env-diff-contract.json`.

### registry-check-rev

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/registry-check.py --rev HEAD
```
Exit: 2. Receipt: `T57W3Read01-receipts/registry-check-rev.json`.

### repeat-control-snapshot

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/repeat-control.py --snapshot /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/.ufo/evidence/round-12/ControlGate
```
Exit: 0. Receipt: `T57W3Read01-receipts/repeat-control-snapshot.json`.

### bash-witness-study-count

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/bash-witness-study.py count
```
Exit: 0. Receipt: `T57W3Read01-receipts/bash-witness-study-count.json`.

### pin-disposition-read

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/pin-disposition.py --manifest /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
```
Exit: 0. Receipt: `T57W3Read01-receipts/pin-disposition-read.json`.

### evidence-disposition-json

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone --dispositions /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/.ufo/evidence/round-18/dispositions.json --json
```
Exit: 0. Receipt: `T57W3Read01-receipts/evidence-disposition-json.json`.

### context-capture-check

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/context-capture.py --check --json
```
Exit: 0. Receipt: `T57W3Read01-receipts/context-capture-check.json`.

### receipt-gate-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/receipt-revision-gate.py --selftest
```
Exit: 0. Receipt: `T57W3Read01-receipts/receipt-gate-selftest.json`.

### env-diff-contract-prepared

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools/env-diff.py --contract /fast/scratch/hyaku/tameshi-r57/T57W3Read01/env-contract.json --out /fast/scratch/hyaku/tameshi-r57/T57W3Read01/envdiff.json --fleet-root /fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone
```
Exit: 2. Receipt: `T57W3Read01-receipts/env-diff-contract-prepared.json`.

### pointers

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read01-receipts/pointers.py
```
Exit: 0. Receipt: `T57W3Read01-receipts/pointers.json`.

### scratch-helper-arms

```sh
python3 -c 'import importlib.util, os, pathlib, tempfile
root=pathlib.Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools'"'"')
for name in ('"'"'env-diff'"'"','"'"'repeat-control'"'"','"'"'registry-check'"'"','"'"'bash-witness-study'"'"','"'"'pin-disposition'"'"','"'"'evidence-disposition'"'"','"'"'context-capture'"'"'):
 s=importlib.util.spec_from_file_location('"'"'probe_'"'"'+name.replace('"'"'-'"'"','"'"'_'"'"'), root/(name+'"'"'.py'"'"'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 for arm,value in [('"'"'unset'"'"',None),('"'"'empty'"'"','"'"''"'"'),('"'"'usable'"'"','"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read01'"'"')]:
  if value is None: os.environ.pop('"'"'TMPDIR'"'"',None)
  else: os.environ['"'"'TMPDIR'"'"']=value
  tempfile.tempdir=None
  got=m.strict_scratch_root(); expected=value if value else None
  assert got==expected,(name,arm,got,expected)
  print(name,arm,repr(got),'"'"'PASS'"'"')
'
```
Exit: 1. Receipt: `T57W3Read01-receipts/scratch-helper-arms.json`.

### scratch-helper-arms-corrected

```sh
python3 -c 'import importlib.util, os, pathlib, tempfile
root=pathlib.Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read01/clone/tools'"'"')
for name in ('"'"'env-diff'"'"','"'"'repeat-control'"'"','"'"'registry-check'"'"','"'"'bash-witness-study'"'"','"'"'pin-disposition'"'"','"'"'evidence-disposition'"'"','"'"'context-capture'"'"'):
 s=importlib.util.spec_from_file_location('"'"'probe_'"'"'+name.replace('"'"'-'"'"','"'"'_'"'"'), root/(name+'"'"'.py'"'"'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
 for arm,value in [('"'"'unset'"'"',None),('"'"'empty'"'"','"'"''"'"'),('"'"'usable'"'"','"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read01'"'"')]:
  if value is None: os.environ.pop('"'"'TMPDIR'"'"',None)
  else: os.environ['"'"'TMPDIR'"'"']=value
  tempfile.tempdir=None
  got=m.strict_scratch_root(); expected=value if value else tempfile.gettempdir()
  assert got==expected,(name,arm,got,expected)
  print(name,arm,repr(got),'"'"'PASS'"'"')
'
```
Exit: 0. Receipt: `T57W3Read01-receipts/scratch-helper-arms-corrected.json`.

## Notes and verification limits

- LSP unavailable: read xd://lsp returned No such tool; pointer checks are literal/runtime evidence, not semantic reference proof.
- The section is a standing policy plus documented behavior, not an executable shell block. Its gate invocation is an argument template; exercised the shipped 19-case selftest rather than running literal LANE/REV placeholders.
- Round-55 env-diff fixture-contract.json is generated by measure.py lines 184-189, not a committed input. The first exploratory invocation lacked that fixture and exited 2; the prepared scratch contract reproduced the documented scratch-root refusal. This is not a false section statement.
- An initial helper probe incorrectly expected None for an unset root and failed its own assertion. After reading strict_scratch_root, the corrected probe checked tempfile.gettempdir(); all 21 helper arm checks passed.
- The receipt gate is an eighth scratch_root registry cell but explicitly does not use strict_scratch_root; the section correctly scopes the seven-helper contract. No claim that the gate implements that contract is certified.
- Unusable-TMPDIR sweep: nine allocating modes returned exit 2 with one matching stderr line; repeat-control additionally prints REPEAT_CONTROL: setup_error on stdout, already disclosed by scratch-root-contract.md lines 97-104. Five lazy modes returned exit 0.
- Empty/unset/usable checks exercised the seven helpers directly, not all full command success paths; no full usable/empty thirteen-mode replay or strace allocation census is claimed.
- Historical scratch census: 3202 tracked round-48..52 w1/w2 files, 0 dash-form and 7354 slash-form tameshi seat-root occurrences. This is a literal convention census, not proof every historical operator obeyed the policy.
- S278 and S279 URLs resolved via read; the CPython source skips empty environment candidates and the Python gettempdir docs retain the documented order. External pages are live references, not frozen C0b input blobs.
- No tools installed or updated. No lane content, frozen evidence, or SKILL.md edited.

## Self-evaluation

Accuracy 4/5: output distinguishes runtime passes from limited helper probes. Completeness 4/5: full usable/empty command replays were not claimed. Clarity 4/5: verbose commands retained for reproduction. Actionability 5/5: exact revision, hash and receipts supplied. Conciseness 4/5: full command inventory intentionally retained. Overall 4.2/5. Improvement: consume the JSON receipts for concise downstream binding rather than reproducing this report.
