# T56W2ExecC0Receipts — C0 calibration receipts

## Precheck
Command:
```sh
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 0a2010acd1e92e4e332774050825e21bcfc7e079 c0137451f5b7f22d65f748fc69f1b181f55e1378
```
Output: exit 1 (expected RED), `floor_credited=64`, `cand_credited=46`, `lost=18`. The loss set is **exactly** the eighteen frozen headings in the C1 list; no additional heading was lost.

Each listed heading's reason is the command output's `drifted=` set:

- `## Context gate classification and explicit exit classes — round 15`: `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/context-capture.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, `tools/registry.json`, `tools/trace-inputs.py`
- `## Effective expectation reconciliation — round 14`: `corpus/SOURCES.md`, `tools/context-capture.py`
- `## Live-tree re-pin and entry-command monitor — round 17`: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py`
- `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py`
- `## Pin disposition and provenance correction — round 13`: `corpus/SOURCES.md`
- `## Repeated controls and gate registry — round 12`: `corpus/SOURCES.md`, `tools/repeat-control.py`
- `## Standing rules`: no input-drift path (`drifted=` empty)
- `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`: `corpus/SOURCES.md`
- `## The operator's runbook and the six-leg regression (round 10, measured)`: `tools/registry.json`
- `### Gate/probe registry`: `tools/bash-witness-study.py`, `tools/repeat-control.py`
- `### Round-13 gate/probe registry`: `corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/pin-disposition.py`
- `### Round-15 gate/probe registry`: `tools/context-capture.py`
- `### Round-17 gate/probe registry — re-pin and monitor`: `corpus/SOURCES.md`, `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py`
- `### Round-18 gate/probe registry — routed-defect closure`: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/registry-check.py`, `tools/registry.json`
- `### Round-21 gate/probe registry — finite environment differential`: `.ufo/evidence/round-15/verify.py`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/env-diff.py`, `tools/registry-check.py`, `tools/registry.json`
- `### Round-26 gate/probe registry — report interop`: `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py`
- `### The service's limits — what tameshi refuses to mutation-test`: `tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py`
- `### Triggers T1–T3 and the re-pin rule`: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/service-limits.md`, `tools/bash-witness-study.py`, `tools/context-capture.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry-check.py`, `tools/registry.json`, `tools/repeat-control.py`

## C0 monitor
Command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c0137451f5b7f22d65f748fc69f1b181f55e1378`
Extracted output: `covered=46`, `score=6`, `box3=false`.

## Drift-set JSON list
Extracted from monitor output's uncredited-section input-drift reasons (unique sorted values):
```json
["input-drift:.ufo/evidence/round-15/verify.py", "input-drift:corpus/QUALITY.md", "input-drift:corpus/SOURCES.md", "input-drift:corpus/knowledge/service-limits.md", "input-drift:tools/bash-witness-study.py", "input-drift:tools/context-capture.py", "input-drift:tools/env-diff.py", "input-drift:tools/evidence-disposition.py", "input-drift:tools/mutate-and-run.sh", "input-drift:tools/pin-disposition.py", "input-drift:tools/registry-check.py", "input-drift:tools/registry.json", "input-drift:tools/repeat-control.py", "input-drift:tools/trace-inputs.py"]
```

Executed commands: precheck above; round-21 monitor above; `python3 -c` loading the C0 monitor JSON and printing the exact summary and unique sorted input-drift list. No files other than this scoped report were written by this seat.
