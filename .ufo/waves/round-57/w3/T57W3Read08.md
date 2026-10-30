# T57W3Read08 — cold-read report

Heading: `## Repeated controls and gate registry — round 12`  
Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`  
Frozen section: 1521–1540; SHA-256 `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831`  
Recommendation: **gap-minor** (advisory, not admission).

## Findings by severity

### Minor — incorrect source line pointer

`SKILL.md:1523` directs the reader to `corpus/SOURCES.md:503` for S265's supersession of S026. At C0b that line says `- Next unused id: S161.`; S265 is at line 140. The supersession claim itself is true. Defer pointer correction to round 58; no content edited.

Command:
```sh
python3 -c 'from pathlib import Path; p=Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/corpus/SOURCES.md'"'"'); lines=p.read_text().splitlines(); print('"'"'corpus/SOURCES.md:503: '"'"'+lines[502]); print('"'"'S265 row: '"'"'+str(next(i for i,l in enumerate(lines,1) if l.startswith('"'"'| S265 |'"'"')))); print('"'"'supersession: '"'"'+str(any(l.startswith('"'"'| S265 |'"'"') and '"'"'supersedes S026'"'"' in l for l in lines)))'
```
Output (exit 0):
```text
corpus/SOURCES.md:503: - Next unused id: S161.
S265 row: 140
supersession: True
```

## Executed sweep

Axes: calibration, executable recipe, pointer accuracy, honest finite-sample claims, zero lane mutation.

All execution used a shared scratch clone detached at C0b, with `HYAKU_SCRATCH=/fast/scratch/hyaku` and `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read08`. The documented recipe was instantiated with a non-secret Python fixture. Nine primary runs plus the existing-output refusal matched their expected exits. Negative fixture verdicts are expected, not section defects. Raw binary observations are retained losslessly as base64.

Full commands and stdout/stderr: `T57W3Read08-receipts/commands.json` and the adjacent report JSON. Raw observations: `T57W3Read08-receipts/raw-observations-base64.json`.

### frozen-sectionizer

```sh
python3 -c 'import importlib.util, subprocess; spec=importlib.util.spec_from_file_location('"'"'frozen'"'"','"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'"'"'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); raw=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"','"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"','"'"'show'"'"','"'"'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'"'"']); sec=next(s for s in m.sectionize(raw) if s['"'"'heading'"'"']=='"'"'## Repeated controls and gate registry — round 12'"'"'); print(sec['"'"'start'"'"'],sec['"'"'end'"'"'],sec['"'"'sha256'"'"'])'
```

Exit 0.

```text
1521 1540 3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831
```

### recipe-match

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/tameshi-r12-controls-UNIQUE -- python3 -c 'import sys; sys.stdout.buffer.write(b"ok\x00\n"); sys.stderr.write("notice\n")'
```

Exit 0.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_RUN 1 exit=0 stdout-bytes=4 stderr-bytes=7
REPEAT_RUN 2 exit=0 stdout-bytes=4 stderr-bytes=7
REPEAT_RUN 3 exit=0 stdout-bytes=4 stderr-bytes=7
REPEAT_COMPARE identical=yes runs=3
REPEAT_OUT /fast/scratch/hyaku/tameshi-r57/T57W3Read08/tameshi-r12-controls-UNIQUE
REPEAT_CONTROL: controls_match
```

### baseline-nonzero

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/nonzero -- python3 -c 'raise SystemExit(7)'
```

Exit 2.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_RUN 1 exit=7 stdout-bytes=0 stderr-bytes=0
REPEAT_RUN 2 exit=7 stdout-bytes=0 stderr-bytes=0
REPEAT_RUN 3 exit=7 stdout-bytes=0 stderr-bytes=0
REPEAT_COMPARE identical=yes runs=3
REPEAT_OUT /fast/scratch/hyaku/tameshi-r57/T57W3Read08/nonzero
REPEAT_CONTROL: baseline_nonzero
```

### command-unavailable

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/unavailable -- /fast/scratch/hyaku/tameshi-r57/T57W3Read08/not-a-command
```

Exit 2.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_RUN 1 exit=unavailable stdout-bytes=0 stderr-bytes=97
REPEAT_RUN 2 exit=unavailable stdout-bytes=0 stderr-bytes=97
REPEAT_RUN 3 exit=unavailable stdout-bytes=0 stderr-bytes=97
REPEAT_COMPARE identical=no runs=3
REPEAT_OUT /fast/scratch/hyaku/tameshi-r57/T57W3Read08/unavailable
REPEAT_CONTROL: command_unavailable
```

### selftest

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --selftest
```

Exit 0.

```text
SELFTEST_CASE stable PASS (expected=controls_match/0 observed=controls_match/0 saved-bytes-ok)
SELFTEST_CASE mismatch-stdout PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE mismatch-run3-only PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE mismatch-newline-only PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE mismatch-stderr PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE mismatch-exit PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE mismatch-nonzero-exits PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE nonzero-baseline PASS (expected=baseline_nonzero/2 observed=baseline_nonzero/2)
SELFTEST_CASE child127-baseline PASS (expected=baseline_nonzero/2 observed=baseline_nonzero/2)
SELFTEST_CASE command-unavailable-enoent PASS (expected=command_unavailable/2 observed=command_unavailable/2)
SELFTEST_CASE command-unavailable-eacces PASS (expected=command_unavailable/2 observed=command_unavailable/2)
SELFTEST_CASE command-unavailable-enoexec PASS (expected=command_unavailable/2 observed=command_unavailable/2)
SELFTEST_CASE invalid-runs-2 PASS (expected=invalid_usage/64 observed=invalid_usage/64)
SELFTEST_CASE invalid-runs-1 PASS (expected=invalid_usage/64 observed=invalid_usage/64)
SELFTEST_CASE invalid-runs-0 PASS (expected=invalid_usage/64 observed=invalid_usage/64)
SELFTEST_CASE invalid-runs-abc PASS (expected=invalid_usage/64 observed=invalid_usage/64)
SELFTEST_CASE invalid-missing-separator PASS (expected=invalid_usage/64 observed=invalid_usage/64)
SELFTEST_CASE invalid-existing-out PASS (expected=invalid_usage/64 observed=invalid_usage/64 refused-out-untouched)
SELFTEST_CASE stdin-devnull PASS (expected=controls_match/0 observed=controls_match/0 stdin-devnull-ok)
SELFTEST_CASE snapshot-pass PASS (expected=controls_match/0 observed=controls_match/0)
SELFTEST_CASE snapshot-mismatch-pass PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST_CASE snapshot-tamper-byte PASS (expected=snapshot_tampered/2 observed=snapshot_tampered/2)
SELFTEST_CASE snapshot-tamper-missing PASS (expected=snapshot_tampered/2 observed=snapshot_tampered/2)
SELFTEST_CASE snapshot-tamper-unlisted PASS (expected=snapshot_tampered/2 observed=snapshot_tampered/2)
SELFTEST_CASE snapshot-tamper-duplicate-key PASS (expected=snapshot_tampered/2 observed=snapshot_tampered/2)
SELFTEST_CASE snapshot-tamper-manifest-symlink PASS (expected=snapshot_tampered/2 observed=snapshot_tampered/2)
SELFTEST_CASE snapshot-tamper-observation-symlink PASS (expected=snapshot_tampered/2 observed=snapshot_tampered/2)
SELFTEST_CASE snapshot-committed-stable PASS (expected=controls_match/0 observed=controls_match/0)
SELFTEST_CASE snapshot-committed-mismatch PASS (expected=controls_mismatch/1 observed=controls_mismatch/1)
SELFTEST: PASS (29 cases)
```

### frozen-match

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --snapshot /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/.ufo/evidence/round-12/ControlGate
```

Exit 0.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
SNAPSHOT_INPUTS 9 verified
SNAPSHOT_EXPECTED id=controls_match exit=0
SNAPSHOT_OBSERVED id=controls_match exit=0
REPEAT_CONTROL: controls_match
```

### frozen-mismatch

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --snapshot /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/.ufo/evidence/round-12/ControlGate/mismatch
```

Exit 1.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
SNAPSHOT_INPUTS 9 verified
SNAPSHOT_EXPECTED id=controls_mismatch exit=1
SNAPSHOT_OBSERVED id=controls_mismatch exit=1
REPEAT_CONTROL: controls_mismatch
```

### mismatch-stdout

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/mismatch-stdout -- python3 -c 'from pathlib import Path; import sys; p=Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read08/state-stdout'"'"'); n=int(p.read_text())+1 if p.exists() else 1; p.write_text(str(n)); print(n)'
```

Exit 1.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_RUN 1 exit=0 stdout-bytes=2 stderr-bytes=0
REPEAT_RUN 2 exit=0 stdout-bytes=2 stderr-bytes=0
REPEAT_RUN 3 exit=0 stdout-bytes=2 stderr-bytes=0
REPEAT_COMPARE identical=no runs=3
REPEAT_OUT /fast/scratch/hyaku/tameshi-r57/T57W3Read08/mismatch-stdout
REPEAT_CONTROL: controls_mismatch
```

### mismatch-stderr

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/mismatch-stderr -- python3 -c 'from pathlib import Path; import sys; p=Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read08/state-stderr'"'"'); n=int(p.read_text())+1 if p.exists() else 1; p.write_text(str(n)); print(n,file=sys.stderr)'
```

Exit 1.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_RUN 1 exit=0 stdout-bytes=0 stderr-bytes=2
REPEAT_RUN 2 exit=0 stdout-bytes=0 stderr-bytes=2
REPEAT_RUN 3 exit=0 stdout-bytes=0 stderr-bytes=2
REPEAT_COMPARE identical=no runs=3
REPEAT_OUT /fast/scratch/hyaku/tameshi-r57/T57W3Read08/mismatch-stderr
REPEAT_CONTROL: controls_mismatch
```

### mismatch-exit

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/mismatch-exit -- python3 -c 'from pathlib import Path; import sys; p=Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read08/state-exit'"'"'); n=int(p.read_text())+1 if p.exists() else 1; p.write_text(str(n)); sys.exit(n)'
```

Exit 1.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_RUN 1 exit=1 stdout-bytes=0 stderr-bytes=0
REPEAT_RUN 2 exit=2 stdout-bytes=0 stderr-bytes=0
REPEAT_RUN 3 exit=3 stdout-bytes=0 stderr-bytes=0
REPEAT_COMPARE identical=no runs=3
REPEAT_OUT /fast/scratch/hyaku/tameshi-r57/T57W3Read08/mismatch-exit
REPEAT_CONTROL: controls_mismatch
```

### source-pointer

```sh
python3 -c 'from pathlib import Path; p=Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/corpus/SOURCES.md'"'"'); lines=p.read_text().splitlines(); print('"'"'corpus/SOURCES.md:503: '"'"'+lines[502]); print('"'"'S265 row: '"'"'+str(next(i for i,l in enumerate(lines,1) if l.startswith('"'"'| S265 |'"'"')))); print('"'"'supersession: '"'"'+str(any(l.startswith('"'"'| S265 |'"'"') and '"'"'supersedes S026'"'"' in l for l in lines)))'
```

Exit 0.

```text
corpus/SOURCES.md:503: - Next unused id: S161.
S265 row: 140
supersession: True
```

### existing-output-refusal

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read08/clone/tools/repeat-control.py --runs 3 --out /fast/scratch/hyaku/tameshi-r57/T57W3Read08/tameshi-r12-controls-UNIQUE -- python3 -c 'import sys; sys.stdout.buffer.write(b"ok\x00\n"); sys.stderr.write("notice\n")'
```

Exit 64.

```text
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=a8fad68fcbb87d03fb7e5e22fb1f70bd94d36c857a1c4b58171d91b042df80fd
REPEAT_CONTROL: invalid_usage
repeat-control: --out already exists (refused, never overwritten): /fast/scratch/hyaku/tameshi-r57/T57W3Read08/tameshi-r12-controls-UNIQUE
usage: repeat-control.py --runs N --out DIR -- COMMAND [ARG...]
       repeat-control.py --snapshot DIR
       repeat-control.py --selftest
```

## Pointers, bounds and verification gaps

Read the entire frozen section, the source rows, the cited knowledge note and round-12 runtime evidence. All named files resolve. The standalone precondition and exact-byte decision table agree with the current implementation and observed fixtures. Other SKILL sections retain the historical six-leg context and identify later ten-leg expansion, so the round-12 statement is not a present-tense saturation claim.

LSP unavailable (`read xd://lsp`: `No such tool`); literal grep/source inspection used as fallback, not semantic proof. No indefinite hanging process was launched; caller-owned timeout is explicitly stated and implementation documentation confirms no supervisor. Finite controls cannot establish determinism or cross-host reliability. No whole-monitor 64/64 claim made.

No tool installation, staged patch, tracked content mutation, runtime admission or shipping action. Scratch removed after retaining receipts.

## Self-evaluation

Accuracy 4/5: outputs retained, but absence of indefinite-hang behavior was established by reading rather than a hang experiment. Completeness 4/5: all section commands and pointers checked; external websites were not re-fetched because the cited contract is pinned tree truth. Clarity 4/5: exact commands are lengthy but preserved for reproducibility. Actionability 5/5: one specific line-pointer fix identified and deferred as required. Conciseness 4/5: full sweep transcripts add length but satisfy evidence discipline. Overall 4.2/5. Improvements: update the source pointer in round 58; retain the separate machine-readable receipts when binding monitor credit. User agreement expected: the minor pointer gap is clearly separated from successful runtime behavior.
