# C1 cheap controls — round 29
## Result
All four controls were rejected by the unchanged frozen round-29 counter. No control reached `C1_R29_PASS=true`. K4 nevertheless increased the older monitor from **52/64 to 53/64 without a new reader**: section start 1814 was credited. Eleven other re-anchored entries were stopped by existing trace receipts.
Axes: false acceptance; avoiding the claimed work; cheap isolated controls; exact restoration. This is a pre-freeze control probe, not an integration or shipping decision.
Baseline A already fails. Therefore these are rejected negative controls, **not killed mutants**; a conventional pristine/mutated/restored kill verdict is inconclusive.
## Isolation and frozen detector
- A: `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`.
- Private clone: `/fast/scratch/hyaku/tameshi-r29-CtlC1Cheap`.
- Independent private worktrees: `/fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2`, `-K3`, `-K4`.
- Only this report was written in the lane. No lane Git write command, `jj` command, runtime, seat spawn, or model invocation was used.
- Operator rules were read. No tools were installed or updated.
- Every launched program was bounded by `timeout 300`; all launched process groups exited. No service or outstanding process tree remains.
Counters were copied from A before any ledger edit. Before and after SHA-256 values are identical:

| Frozen file | Before and after SHA-256 |
| --- | --- |
| `/tmp/CtlC1Cheap-c1-r29.py` | `adaadfc6f34bd102fe0cf77f5ab5114d715e50491bddcb7a8e2f7b4f56e4c1d8` |
| `/tmp/CtlC1Cheap-c1-r27.py` | `6f95ef1d0624e4da2130168e56be65f678a203fcefe7afca9cfad592b47670a8` |
The embedded round-27 counter and cold-read implementation were not edited. Every counter below used `--repo <private clone or worktree> --rev HEAD`.
### Setup commands exercised

```sh
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
timeout 300 mkdir -p /fast/scratch/hyaku
timeout 300 git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
timeout 300 cp /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap/.ufo/evidence/round-29/c1-measure.py /tmp/CtlC1Cheap-c1-r29.py
timeout 300 cp /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap/.ufo/evidence/round-27/c1-measure.py /tmp/CtlC1Cheap-c1-r27.py
timeout 300 cp /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap/.ufo/evidence/round-21/coldread/ledger.json /tmp/CtlC1Cheap-ledger-A.json
```
### Common append recipe
Actual mutations were surgical hashline edits: change the last existing entry closer at line 24520 from `}` to `},`, then append 12 compact JSON entries before the entries array closes. The following equivalent standalone builder reproduces those ledger bytes. Save it as `/tmp/CtlC1Cheap-build.py`; it is a reproduction recipe, not an additional executed detector. All original entries and every other top-level key are retained.

```python
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
repo, kind = sys.argv[1:]
env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
def git(*args):
    return subprocess.run(['timeout', '300', 'git', '-C', repo, *args],
                          env=env, capture_output=True, check=True).stdout
rel = '.ufo/evidence/round-21/coldread/ledger.json'
p = Path(repo) / rel
raw = p.read_text()
data = json.loads(raw)
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '9f3084bc60ad56aac01e4556ef4c7653df2f65e5'
assert len(data['entries']) == 371
indices = [354, 308, 325, 359, 362, 364, 366, 367, 368, 337, 369, 370]
entries = []
if kind == 'K2':
    for n in range(1, 13):
        e = copy.deepcopy(data['entries'][0])
        e.update(start=90000+n, end=90000+n,
                 heading=f'### Junk control C1-K2-{n}',
                 sha256=hashlib.sha256(f'junk-{n}'.encode()).hexdigest(),
                 read_rev=head, seats=['Ghost'],
                 reports=['.ufo/waves/round-29/w1/Ghost.md'])
        entries.append(e)
else:
    assert kind in ('K3', 'K4')
    for i in indices:
        e = copy.deepcopy(data['entries'][i])
        e.update(read_rev=head,
                 inputs={path: hashlib.sha256(git('show', head+':'+path)).hexdigest()
                         for path in e['inputs']},
                 seats=['Ghost'], reports=['.ufo/waves/round-29/w1/Ghost.md'])
        if kind == 'K3':
            e['verdict'] = 'gap-blocking'
        entries.append(e)
# Same compact append bytes as the exercised hashline edit at line 24520.
marker = '\n  ],\n  "carried_from"'
assert raw.count(marker) == 1
before, after = raw.split(marker)
addition = ',\n'.join('    '+json.dumps(e, ensure_ascii=True, separators=(',', ':'))
                      for e in entries)
p.write_text(before+',\n'+addition+marker+after)
```
### The 12 uncovered sections and copied entries
The initial bounded command was `python3 .ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap --rev HEAD --explain` (wrapped in `timeout 300`, exit 0). Its `coldread.missing` list selected these exact sections. Indices are zero-based. Each copied entry is the latest successful-shaped record for that heading at A; its strict entry gate was also exercised at the historical commit below and returned no failure. A read revision can predate the receipt commit, so historical credit was checked at a landed ledger revision, not the earlier `read_rev`.

| Start | Heading | Source index | Historical revision where its strict entry gate credits |
| --- | --- | --- | --- |
| 131 | ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | 354 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 375 | ## Restore discipline — before/after identity, not continuous non-write proof | 308 | `af7b70daf7754f1d9363669cf9bc97ec01f61f9c` |
| 1380 | ### The map — where a reader enters, artifact by artifact | 325 | `af7b70daf7754f1d9363669cf9bc97ec01f61f9c` |
| 1479 | ## Repeated controls and gate registry — round 12 | 359 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1517 | ## Pin disposition and provenance correction — round 13 | 362 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1548 | ### Round-13 gate/probe registry | 364 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1563 | ## Effective expectation reconciliation — round 14 | 366 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1609 | ## Context gate classification and explicit exit classes — round 15 | 367 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1814 | ## Live-tree re-pin and entry-command monitor — round 17 | 368 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1925 | ### Round-18 gate/probe registry — routed-defect closure | 337 | `af7b70daf7754f1d9363669cf9bc97ec01f61f9c` |
| 1938 | ### Round-20 gate/probe registry — frozen receipt instruments | 369 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |
| 1964 | ### Round-21 gate/probe registry — finite environment differential | 370 | `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6` |

## C1-K1 — do nothing

Mutant/control: none. A was scored unchanged. Expected detector: false, because the existing ledger covers only 52 of 64 sections.

Build and run:

```sh
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap --rev HEAD
```

Full stdout:

```text
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=52/64 restraint=6 box3_mismatch=1 appended=0 bound=0 prefix_equal=1 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C1_R29_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL C1-K1: meets=no

Mutation verdict: baseline failure; inconclusive as a kill test. No bytes were changed.

## C1-K2 — junk

Appended 12 copies of the first recorded entry, with made-up starts 90001–90012, made-up headings and section hashes, and `verified-record` verdicts. No real section was read or repaired.

Expected detector: `C1_R29_PASS=false`; junk or false findings cannot repair coverage, and a nonexistent report cannot bind a new entry.

Worktree and commit commands exercised, with the equivalent builder invocation between them:

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap worktree add --quiet --detach /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
# Equivalent reproduction of the exercised hashline append:
timeout 300 python3 /tmp/CtlC1Cheap-build.py /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 K2
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 add -- .ufo/evidence/round-21/coldread/ledger.json
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 -c user.name=ctl -c user.email=ctl@x commit -q -m "C1-K2 isolated cheap control"
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 update-ref refs/heads/ctl-C1-K2 HEAD
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 --rev HEAD
```

Observed commit: `f501ee3ef63f691d9e818d70d67ca76c6b435a5d`; retained as `ctl-C1-K2` in the private clone.

Full stdout:

```text
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=f501ee3ef63f691d9e818d70d67ca76c6b435a5d
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=52/64 restraint=6 box3_mismatch=1 appended=12 bound=0 prefix_equal=1 rev=f501ee3ef63f691d9e818d70d67ca76c6b435a5d
PREDICATE: C1_R29_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL C1-K2: meets=no

Mutation verdict: rejected negative control; conventional kill test inconclusive because pristine A also fails.

### Restoration evidence

The exact original ledger bytes were restored by returning this worktree to A; equality with the saved original bytes was checked. All 371 original entries and all other top-level data keys were preserved in the control.

| Ledger state | SHA-256 |
| --- | --- |
| Before | `c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f` |
| Control | `fd32e372617ad7e89cd61a610a5e7f439e84f921eeeba7de108677f8c142ebb4` |
| Restored | `c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f` |

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K2 --rev HEAD
```

Full restored stdout:

```text
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=52/64 restraint=6 box3_mismatch=1 appended=0 bound=0 prefix_equal=1 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C1_R29_PASS=false
```

Restored exit: `1`. Stderr: empty. The restored detector result matches the original baseline.

## C1-K3 — all false

Appended one entry for each of the 12 actual missing headings, using the historical source entries above but setting every verdict to `gap-blocking`. Inputs were recomputed at A, so these are current failing findings rather than stale failures. No successful read was supplied.

Expected detector: `C1_R29_PASS=false`; junk or false findings cannot repair coverage, and a nonexistent report cannot bind a new entry.

Worktree and commit commands exercised, with the equivalent builder invocation between them:

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap worktree add --quiet --detach /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
# Equivalent reproduction of the exercised hashline append:
timeout 300 python3 /tmp/CtlC1Cheap-build.py /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 K3
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 add -- .ufo/evidence/round-21/coldread/ledger.json
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 -c user.name=ctl -c user.email=ctl@x commit -q -m "C1-K3 isolated cheap control"
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 update-ref refs/heads/ctl-C1-K3 HEAD
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 --rev HEAD
```

Observed commit: `2958619fe6133e346b3fbdc37e6304262e4c5b4c`; retained as `ctl-C1-K3` in the private clone.

Full stdout:

```text
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2958619fe6133e346b3fbdc37e6304262e4c5b4c
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=52/64 restraint=6 box3_mismatch=1 appended=12 bound=0 prefix_equal=1 rev=2958619fe6133e346b3fbdc37e6304262e4c5b4c
PREDICATE: C1_R29_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL C1-K3: meets=no

Mutation verdict: rejected negative control; conventional kill test inconclusive because pristine A also fails.

### Restoration evidence

The exact original ledger bytes were restored by returning this worktree to A; equality with the saved original bytes was checked. All 371 original entries and all other top-level data keys were preserved in the control.

| Ledger state | SHA-256 |
| --- | --- |
| Before | `c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f` |
| Control | `75e8db2197a91446304b221c7c608019d080f6952853332582bf8e626581a12f` |
| Restored | `c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f` |

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K3 --rev HEAD
```

Full restored stdout:

```text
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=52/64 restraint=6 box3_mismatch=1 appended=0 bound=0 prefix_equal=1 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C1_R29_PASS=false
```

Restored exit: `1`. Stderr: empty. The restored detector result matches the original baseline.

## C1-K4 — no reader

Appended the most recent historically credited entry for each of the 12 uncovered headings. Only `read_rev`, `inputs`, `reports`, and `seats` were replaced: `read_rev` is the pre-commit HEAD A; every recorded input digest was recomputed from that HEAD; reports point to the absent `.ufo/waves/round-29/w1/Ghost.md`; seats are `["Ghost"]`. Original commands, findings, provenance, and trace references were otherwise copied. No reader or new trace receipt was produced.

Expected detector: `C1_R29_PASS=false`; junk or false findings cannot repair coverage, and a nonexistent report cannot bind a new entry.

Worktree and commit commands exercised, with the equivalent builder invocation between them:

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap worktree add --quiet --detach /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
# Equivalent reproduction of the exercised hashline append:
timeout 300 python3 /tmp/CtlC1Cheap-build.py /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 K4
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 add -- .ufo/evidence/round-21/coldread/ledger.json
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 -c user.name=ctl -c user.email=ctl@x commit -q -m "C1-K4 isolated cheap control"
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 update-ref refs/heads/ctl-C1-K4 HEAD
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 --rev HEAD
```

Observed commit: `2070ed212257af642e89e7a9c4d74b85f3298793`; retained as `ctl-C1-K4` in the private clone.

Full stdout:

```text
C1_MONITOR: covered=53/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2070ed212257af642e89e7a9c4d74b85f3298793
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=53/64 restraint=6 box3_mismatch=1 appended=12 bound=0 prefix_equal=1 rev=2070ed212257af642e89e7a9c4d74b85f3298793
PREDICATE: C1_R29_PASS=false
```

Exit: `1`. Stderr: empty.

CONTROL C1-K4: meets=no

Mutation verdict: rejected negative control; conventional kill test inconclusive because pristine A also fails.

### Frozen round-27 monitor check

```sh
timeout 300 python3 /tmp/CtlC1Cheap-c1-r27.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 --rev HEAD
```

Full stdout:

```text
C1_MONITOR: covered=53/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2070ed212257af642e89e7a9c4d74b85f3298793
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
```

Exit: `1`. Stderr: empty.

The monitor alone credits one re-anchored entry, start **1814**, despite no new reader. Existing trace receipts stop the other 11. The complete round-29 counter still rejects the control (`53/64`, `bound=0/12`). The Ghost report is absent at A: `git cat-file -e A:.ufo/waves/round-29/w1/Ghost.md` exited 128.

First strict gate result for each appended entry, using the unchanged credit implementation:

| Start | Result |
| --- | --- |
| 131 | `trace-input-drift:corpus/README.md` |
| 375 | `trace-input-drift:corpus/README.md` |
| 1380 | `trace-input-drift:corpus/README.md` |
| 1479 | `trace-input-drift:corpus/SOURCES.md` |
| 1517 | `trace-input-drift:corpus/SOURCES.md` |
| 1548 | `trace-input-drift:corpus/SOURCES.md` |
| 1563 | `trace-input-drift:corpus/SOURCES.md` |
| 1609 | `trace-input-drift:corpus/SOURCES.md` |
| 1814 | `credited` |
| 1925 | `trace-input-drift:corpus/SOURCES.md` |
| 1938 | `trace-input-drift:corpus/QUALITY.md` |
| 1964 | `trace-input-drift:corpus/SOURCES.md` |

### Restoration evidence

The exact original ledger bytes were restored by returning this worktree to A; equality with the saved original bytes was checked. All 371 original entries and all other top-level data keys were preserved in the control.

| Ledger state | SHA-256 |
| --- | --- |
| Before | `c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f` |
| Control | `676b5fe6b93950a9602613f18f2f48b0eef1c9a0f3e8c8e2c2c7d298ad7e55c2` |
| Restored | `c5b3a3496d6799d163e5902931a24fd857dbb04454e6f9b7b483e71dd6cf385f` |

```sh
timeout 300 git -C /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 checkout -q --detach 9f3084bc60ad56aac01e4556ef4c7653df2f65e5
timeout 300 python3 /tmp/CtlC1Cheap-c1-r29.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC1Cheap-K4 --rev HEAD
```

Full restored stdout:

```text
C1_MONITOR: covered=52/64 restraint=6 box3_mismatch=1 depth_score=9 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
  uncovered: ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
  uncovered: ## Restore discipline — before/after identity, not continuous non-write proof
  uncovered: ### The map — where a reader enters, artifact by artifact
  uncovered: ## Repeated controls and gate registry — round 12
  uncovered: ## Pin disposition and provenance correction — round 13
  uncovered: ### Round-13 gate/probe registry
  uncovered: ## Effective expectation reconciliation — round 14
  uncovered: ## Context gate classification and explicit exit classes — round 15
  uncovered: ## Live-tree re-pin and entry-command monitor — round 17
  uncovered: ### Round-18 gate/probe registry — routed-defect closure
  uncovered: ### Round-20 gate/probe registry — frozen receipt instruments
  uncovered: ### Round-21 gate/probe registry — finite environment differential
C1_R29: monitor_exit=1 covered=52/64 restraint=6 box3_mismatch=1 appended=0 bound=0 prefix_equal=1 rev=9f3084bc60ad56aac01e4556ef4c7653df2f65e5
PREDICATE: C1_R29_PASS=false
```

Restored exit: `1`. Stderr: empty. The restored detector result matches the original baseline.

## Final status

No false pass was found among the four assigned controls. K4 exposes limited monitor-only credit without a fresh reader, but not acceptance by the frozen full counter. The baseline clone and all three control worktrees are at A with their original ledger bytes; mutated commits remain available only on private control branches. No additional probe or integration was performed.

Report: `.ufo/waves/round-29/ctl/CtlC1Cheap.md`
