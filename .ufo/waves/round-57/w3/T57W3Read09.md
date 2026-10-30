# T57W3Read09 — ### Gate/probe registry

Recommendation: **verified-record**; no new actionable false statement or unexpected command failure found in this section. This is not an admission decision.

- Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`; frozen round-18 sectionize: lines 1541–1558.
- Section SHA-256: `1dcb4f7f561650a558fc7218316725ececa9af65955338ba78f96e1820564fa9`.
- Axes: factual calibration, command operability, pointer integrity, scope restraint.
- Read the complete section and reviewed its base-to-C0b diff. Commands ran from a shared scratch clone detached at C0b, with TMPDIR confined to this seat's scratch. No lane content or frozen evidence edited; no tools installed/upgraded.

## Executed sweep

Every entry mode and selftest ran; literal placeholders were instantiated with non-secret fixtures. Receipt positive/verdict/control roles and JSON output were exercised. Each command and its complete stdout/stderr/exit are in the adjacent JSON and individual receipt files.

| Sweep | Observed result |
|---|---|
| repeat-control selftest | exit 0, SELFTEST: PASS (29 cases) |
| repeat-control three runs | exit 0, controls_match |
| clean / mismatch snapshots | exits 0 / 1, expected finding IDs |
| bash witness selftest | exit 0, VERDICT: PASS |
| bash witness count | exit 0, unresolved none; retained sample only |
| witness check / run / rerun | exits 1 / 2 / 2, documented runner drift |
| receipt gate selftest | exit 0, GATE_SELFTEST: 19/19 pass |
| receipt registry accept / content-drift / unresolvable-certified | exits 0 / 3 / 2 with expected codes |
| receipt verdict JSON / ancestor control / usage | exits 0 / 0 / 1 |
| witness invalid subcommand | exit 64, usage |
| pointer and historical integrity sweep | exit 0; all 14 named files resolve; 95 manifest-listed files hash-match; manifest itself unpinned; round-12 scope verified |

## Findings by severity

None. Expected negative-control exits and disclosed stale pins are not failures of the documented contract.

## Residual risk and verification gaps

- Canonical count logic (`tools/bash-witness-study.py:1070–1144`) recomputes retained artifacts and does not call runner preflight. Canonical run preflight (`:947–953`, `:551–589`) checks the frozen runner digest and refuses on drift. This supports only the documented retained-study claim, not a fresh mutation sweep.
- Receipt gate roles and exits follow its one `run` path (`tools/receipt-revision-gate.py:163–220`); the 19-case selftest includes content-identical older-positive acceptance and strict mismatch refusal. No alternative runtime or authority was introduced.
- Git history anchors the witness manifest; the section honestly states that manifest.json itself is not pinned. No full-page or global monitor claim follows from this report.
- LSP device unavailable (`No such tool: xd://lsp`); direct source and literal search are fallback evidence, not semantic reference proof.
- Kind/owner are declared registry metadata. The scope sentence is not an assertion of a seventh independent historical measurement.
- Optional clarity: use controls_match/controls_mismatch instead of clean/failed; qualify the stale runner pin as still stale at C0b. Both are notes, not false claims.

## Commands and receipts

### repeat-selftest

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/repeat-control.py --selftest
```

Exit 0; full output: `T57W3Read09-receipts/repeat-selftest.json`.

### witness-selftest

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/bash-witness-study.py selftest
```

Exit 0; full output: `T57W3Read09-receipts/witness-selftest.json`.

### witness-count

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/bash-witness-study.py count
```

Exit 0; full output: `T57W3Read09-receipts/witness-count.json`.

### witness-check

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/bash-witness-study.py check
```

Exit 1; full output: `T57W3Read09-receipts/witness-check.json`.

### witness-run

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/bash-witness-study.py run
```

Exit 2; full output: `T57W3Read09-receipts/witness-run.json`.

### witness-rerun

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/bash-witness-study.py rerun
```

Exit 2; full output: `T57W3Read09-receipts/witness-rerun.json`.

### repeat-run

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read09/repeat-out -- python3 -c 'print("pristine-control")'
```

Exit 0; full output: `T57W3Read09-receipts/repeat-run.json`.

### repeat-clean

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
```

Exit 0; full output: `T57W3Read09-receipts/repeat-clean.json`.

### repeat-mismatch

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
```

Exit 1; full output: `T57W3Read09-receipts/repeat-mismatch.json`.

### gate-selftest

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py --selftest
```

Exit 0; full output: `T57W3Read09-receipts/gate-selftest.json`.

### receipt-gate-accept

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py --lane . --certified 5e3569969b532310d2b8a3d130901757a3df356b --receipt tools/fixtures/receipt-gate/accept.receipt:positive
```

Exit 0; full output: `T57W3Read09-receipts/receipt-gate-accept.json`.

### receipt-gate-content-drift

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py --lane . --certified 5e3569969b532310d2b8a3d130901757a3df356b --paths tools/fixtures/receipt-gate/drift.paths --receipt tools/fixtures/receipt-gate/drift.receipt:positive
```

Exit 3; full output: `T57W3Read09-receipts/receipt-gate-content-drift.json`.

### receipt-gate-unresolvable-certified

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py --lane . --certified deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --receipt tools/fixtures/receipt-gate/accept.receipt:positive
```

Exit 2; full output: `T57W3Read09-receipts/receipt-gate-unresolvable-certified.json`.

### pointers-history-integrity

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 -c 'import pathlib,json,hashlib,subprocess,importlib.util
root=pathlib.Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone'"'"')
paths=['"'"'tools/repeat-control.py'"'"','"'"'tools/bash-witness-study.py'"'"','"'"'tools/receipt-revision-gate.py'"'"','"'"'.ufo/evidence/round-12/ControlGate/expected.json'"'"','"'"'.ufo/evidence/round-12/ControlGate/mismatch/expected.json'"'"','"'"'.ufo/evidence/round-12/BashWitness/declaration.json'"'"','"'"'.ufo/evidence/round-12/BashWitness/declared.tsv'"'"','"'"'.ufo/evidence/round-12/BashWitness/manifest.json'"'"','"'"'.ufo/waves/round-27/w1/Read25.md'"'"','"'"'.ufo/waves/round-27/residual/ReRead08.md'"'"','"'"'corpus/lessons/round-1-verifier-spotcheck.md'"'"','"'"'tools/fixtures/receipt-gate/accept.receipt'"'"','"'"'tools/fixtures/receipt-gate/drift.receipt'"'"','"'"'tools/fixtures/receipt-gate/drift.paths'"'"']
for p in paths:
 q=root/p; assert q.is_file(),p; print('"'"'POINTER_OK'"'"',p,hashlib.sha256(q.read_bytes()).hexdigest())
e=root/'"'"'.ufo/evidence/round-12/BashWitness'"'"'; manifest=json.loads((e/'"'"'manifest.json'"'"').read_text())['"'"'files'"'"']
assert '"'"'manifest.json'"'"' not in manifest
for p,want in manifest.items(): assert hashlib.sha256((e/p).read_bytes()).hexdigest()==want,p
print('"'"'MANIFEST_OK'"'"',len(manifest),'"'"'files; manifest itself not pinned'"'"')
d=json.loads((e/'"'"'declaration.json'"'"').read_text()); print('"'"'DISCLOSURE'"'"',d['"'"'disclosure'"'"'])
for p in ['"'"'.ufo/evidence/round-12/ControlGate/expected.json'"'"','"'"'.ufo/evidence/round-12/ControlGate/mismatch/expected.json'"'"']: print('"'"'EXPECTED'"'"',p,(root/p).read_text())
historical=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',str(root),'"'"'show'"'"','"'"'9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md'"'"']).decode()
print('"'"'ROUND12_BOXES'"'"'); print('"'"'\n'"'"'.join(l for l in historical.splitlines() if l.startswith('"'"'- ['"'"')))
lesson=(root/'"'"'corpus/lessons/round-1-verifier-spotcheck.md'"'"').read_text(); assert '"'"'box-3 increment is not credited'"'"' in lesson; print('"'"'LESSON excludes box-3 increment'"'"')
s=importlib.util.spec_from_file_location('"'"'w'"'"',root/'"'"'tools/bash-witness-study.py'"'"'); w=importlib.util.module_from_spec(s); s.loader.exec_module(w)
assert hashlib.sha256(w.extract_spec((root/'"'"'tools/mutate-and-run.sh'"'"').read_text()).encode()).hexdigest()==d['"'"'inputs'"'"']['"'"'spec'"'"']['"'"'sha256'"'"']; print('"'"'RUNNER_SPEC matches frozen declaration'"'"')
'
```

Exit 0; full output: `T57W3Read09-receipts/pointers-history-integrity.json`.

### receipt-json

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py --lane /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone --certified 5e3569969b532310d2b8a3d130901757a3df356b --receipt tools/fixtures/receipt-gate/accept.receipt:verdict:rev= --json
```

Exit 0; full output: `T57W3Read09-receipts/receipt-json.json`.

### receipt-control

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py --lane /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone --certified adf87899c70d616140a81185a8f9acbbdfb30392 --receipt tools/fixtures/receipt-gate/accept.receipt:control
```

Exit 0; full output: `T57W3Read09-receipts/receipt-control.json`.

### receipt-usage

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/receipt-revision-gate.py
```

Exit 1; full output: `T57W3Read09-receipts/receipt-usage.json`.

### witness-usage

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 tools/bash-witness-study.py not-a-command
```

Exit 64; full output: `T57W3Read09-receipts/witness-usage.json`.

### frozen-sectionize

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 python3 -c 'import importlib.util,subprocess; p='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"'; s=importlib.util.spec_from_file_location('"'"'frozen'"'"',p+'"'"'/.ufo/evidence/round-18/measure.py'"'"'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); raw=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',p,'"'"'show'"'"','"'"'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'"'"']); sec=next(s for s in m.sectionize(raw) if s['"'"'heading'"'"']=='"'"'### Gate/probe registry'"'"'); print(sec['"'"'start'"'"'],sec['"'"'end'"'"'],sec['"'"'sha256'"'"']); print('"'"'\n'"'"'.join(raw.decode().splitlines()[sec['"'"'start'"'"']-1:sec['"'"'end'"'"']]))'
```

Exit 0; full output: `T57W3Read09-receipts/frozen-sectionize.json`.

### round12-checklist

```sh
cd /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone && TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read09 git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read09/clone show 9df9212d33dc2dbda133e88f28ad47bb08839a5b:SHONEN.md
```

Exit 0; full output: `T57W3Read09-receipts/round12-checklist.json`.

## Self-evaluation

Accuracy 4/5 (source fallback, no LSP); completeness 4/5 (section only, no fresh sweep by design); clarity 4/5 (full command snippets are long); actionability 5/5 (machine-readable identity and receipts); conciseness 4/5 (complete evidence retained). Overall 4.2/5. Improvement: preserve a mounted LSP path for future semantic review.
