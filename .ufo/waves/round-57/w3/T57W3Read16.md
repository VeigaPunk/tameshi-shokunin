# T57W3Read16 — verified-record

Heading: `### Round-18 gate/probe registry — routed-defect closure`

C0b: `adf87899c70d616140a81185a8f9acbbdfb30392`; frozen sectionizer bounds 1968–1980; SHA-256 `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e`.

## Findings

None. All eight registry rows read end to end; cited files and anchors resolve.

## Executed sweep

Commands execute with cwd `/fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone`, TMPDIR `/fast/scratch/hyaku/tameshi-r57/T57W3Read16`, and scrubbed inherited GIT_* variables. Full stdout/stderr and exit status are retained in the corresponding absolute receipt path below.

### defect-probes-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-18/defect-probes.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/defect-probes-selftest.json`.

### r19-check

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-19/measure.py --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392 --check
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/r19-check.json`.

### witness-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/tools/bash-witness-study.py selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/witness-selftest.json`.

### assemble-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-18/coldread/assemble.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/assemble-selftest.json`.

### r19-coldread-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-19/coldread/measure.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/r19-coldread-selftest.json`.

### r19-coldread

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-19/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/r19-coldread.json`.

### trace-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/tools/trace-inputs.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/trace-selftest.json`.

### r19-measure-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-19/measure.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/r19-measure-selftest.json`.

### evidence-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/tools/evidence-disposition.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/evidence-selftest.json`.

### r18-measure-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-18/measure.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/r18-measure-selftest.json`.

### registry-selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/tools/registry-check.py --selftest
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/registry-selftest.json`.

### defect-probes

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-18/defect-probes.py --rev adf87899c70d616140a81185a8f9acbbdfb30392
```

Exit: `2`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/defect-probes.json`.

### witness-count

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/tools/bash-witness-study.py count
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/witness-count.json`.

### trace-example

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/tools/trace-inputs.py --root /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone --out /fast/scratch/hyaku/tameshi-r57/T57W3Read16/example-trace.json -- python3 -c 'from pathlib import Path; print(len(Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/SKILL.md'"'"').read_bytes()))'
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/trace-example.json`.

### defect-probes-fleet-layout

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-18/defect-probes.py --rev adf87899c70d616140a81185a8f9acbbdfb30392
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/defect-probes-fleet-layout.json`.

### section-audit

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/section-audit.py
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/section-audit.json`.

### r18-measure-explain

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone/.ufo/evidence/round-18/measure.py --repo /fast/scratch/hyaku/tameshi-r57/T57W3Read16/clone --rev adf87899c70d616140a81185a8f9acbbdfb30392 --explain
```

Exit: `0`. Receipt: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read16-receipts/r18-measure-explain.json`.

## Results and limits

- Registry 51 cases; evidence disposition 66/66; witness 51/51; trace 30/30; round-18 measure 98/98; assembler 80/80; round-19 correction ruler 43/43; round-19 selector 3/3: all successful.
- Fleet-aware defect probe: `DEFECT_PROBES: open=0 closed=11 total=11`.
- Round-19 `--check`: corrected=5, open=0, total=5.
- Identity/pointer audit: `1968 1980 661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e`; `ALL POINTER AND IDENTITY CHECKS PASS`.
- Collector example exited 0 and retained `example-trace.json`; witness count reports unresolved none.

- Axes: calibration (false statements versus setup limitations), command operability, pointer integrity, and bounded evidence provenance.
- LSP device is unavailable: read xd://lsp returned No such tool. Source inspection and literal search are fallback evidence, not semantic references/definition/diagnostics proof.
- Initial defect-probes execution exited 2 because the isolated clone lacked a sibling kagi-shokunin source. Added a scratch-only sibling symlink to the existing fleet source; the tool mounts source read-only. Re-execution exited 0 with open=0 closed=11 total=11. This was a scratch-layout issue, not a false section claim.
- Both explicit --repo examples used the detached scratch clone rather than the live lane, retaining the exact C0b revision. All reviewed section text was read end to end (1968–1980, with the long round-19 row opened raw).
- Section claims are consistent with pointer and pin checks, public selftests, and guard probes. The round-18 and round-19 cold-read measurements are input-keyed observations, not required-command coverage; their uncovered historical entries were not misclassified as section defects.
- Residual risk: selftests and bounded probes do not establish universal process cleanup; the section expressly retains UID, PID-reuse, and adopted-orphan limits. No new live kernel race or UID-transition experiment was run.
- No tools installed or upgraded; no monitored content or frozen evidence edited. No staged source correction required.

## Self-evaluation

Accuracy 4/5: concrete receipts support every result, but cleanup race limits remain intentionally untested. Completeness 4/5: every row and pointer covered through CLI and source checks, not every possible environmental state. Clarity 4/5: separate receipts preserve full output but require opening linked files. Actionability 5/5: exact C0b/hash and machine-readable report supplied. Conciseness 4/5: command inventory is necessarily repetitive. Overall 4.2/5. Highest-value improvement would be semantic navigation once LSP is mounted; expanding kernel-race testing is outside this bounded reader certification. The user can distinguish observed results from residual risk.
