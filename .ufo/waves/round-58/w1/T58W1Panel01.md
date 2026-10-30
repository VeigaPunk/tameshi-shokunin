# T58W1Panel01 — blind panel

Axes: calibration accuracy, evidence provenance, blindness, no lane mutation.

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.

## Findings, ordered by unresolved status

### R50.4 — open

The item is compound carried work, not merely a request to acknowledge it. Base SCORECARD.md:2433 explicitly includes removing/re-pinning dead `brace_depth_at` helpers among the seven carried open items. At base, tools/tally-audit-v2.py:135-143 and tools/tally-audit-v3.py:234-242 still define them. A Python AST scan of each committed blob finds zero direct `Call(Name("brace_depth_at"))` nodes. This is a concrete uncompleted member, sufficient to leave the compound item open; it does not assert that every other carried member remains unresolved.

Commands: `git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel01/clone show 2a32aa8228d5f86a85c81a923a3148bf792a9538:SCORECARD.md` (selected line 2433); same command for `tools/tally-audit-v2.py` (135-143) and `tools/tally-audit-v3.py` (234-242). Outputs include `def brace_depth_at(text, offset):`; AST outputs are `direct_calls: []` for both. Full exact commands, selection ranges and outputs are in the receipts below.

### R50.1 — fixed

Resolution completed at `f133b47f27ec60e6527e7436c8a6df8c4fdf996c` (the required old→new lesson log; cell correction previously landed in `6d8c11e378aa90b12650808e1b79270742935f15`). Base SOURCES.md:33 reads `| mined |` and names `corpus/knowledge/fixture-shrinking-pilot.md`. Round-51 no-harm.sh:5-7 explicitly replaces population 73 with a score floor for population 74. Lesson round-51.md:12 logs `S022 status queued → mined`. Thus all three requested parts exist, rather than merely a status flip.

Commands: `git -C CLONE show BASE:corpus/SOURCES.md`, `git -C CLONE show BASE:.ufo/evidence/round-51/no-harm.sh`, `git -C CLONE show BASE:corpus/lessons/round-51.md`; selected outputs in tree-evidence.json. `git ... show f133b47f... -- corpus/lessons/round-51.md` proves introduction of the log; full diff in history-evidence.json.

### R50.2 — fixed

Introducing commit `6d8c11e378aa90b12650808e1b79270742935f15`. SKILL.md:2181-2201 carries a round-51 gate/probe registry with both requested rows. At 2193, `pbt staged-id generator` includes `2 could-not-evaluate (usage or setup)` and its selftest; at 2201, `shrink-case` includes `2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill)` and its selftest. Both rows include pins and write scope. The historical round-12 scope sentence applies to its historical table, not the new round-51 table.

Commands: `git -C CLONE show BASE:SKILL.md` selected lines 2181,2183,2193,2201; `git -C CLONE show 6d8c11e... -- SKILL.md`. Outputs and full introducing diff are saved.

### R50.3 — fixed

Introducing commit `6d8c11e378aa90b12650808e1b79270742935f15`. README.md:612 says the original table is `superseded as a whole`; :621 says F6 `held (round 50)` and :625 says F10 `held (round 49)`. Original append-only historical cells need not be rewritten.

Commands: `git -C CLONE show BASE:corpus/README.md` selected lines 610,612,621,625; `git -C CLONE show 6d8c11e... -- corpus/README.md`. Outputs and introducing diff are saved.

### R51.1 — fixed

Introducing commit `bcba8924894216268afc4171f06eb8c28e912b46`. Its registry diff changes `legs_conforming=9/9` to `legs_conforming=10/10`. The base registry retains the active ten-leg expectation. Round-52 no-harm.sh explicitly allows `M:tools/registry.json`; contract.json also names that permitted edit. The committed round-52 w2 probe binds CAND0 to this exact commit; its isolated receipt reads:

```
ROW mte-interop-check expect=0 got=0 held
REGISTRY_CHECK: held=1/1 superseded=0
EXIT=0
```

Commands: `git -C CLONE show bcba8924... -- tools/registry.json`; `git -C CLONE show BASE:tools/registry.json` parsed by row name (not historical line number); `git -C CLONE show BASE:.ufo/evidence/round-52/no-harm.sh`; `git -C CLONE show BASE:.ufo/waves/round-52/w2/T52W2ExecC1Probe/registry-check-only-mte.stdout`; `git -C CLONE show BASE:.ufo/waves/round-52/w2/T52W2ExecC1Probe.md` selected provenance lines. These commands inspect committed execution evidence; I did not rerun the gate. The unrelated C3 failure in that probe does not invalidate the observed mte gate success.

## Commands, receipts, and provenance

Here CLONE expands to `/fast/scratch/hyaku/tameshi-r58/T58W1Panel01/clone`; BASE expands to the full base above. Exact argv arrays, stdout, stderr, return codes, and any selected line numbers are preserved in:

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel01-receipts/tree-evidence.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel01-receipts/history-evidence.json`

The first receipt set includes an accidentally historical line selection of registry.json:1011-1020 (now another row); this is not used as evidence. The second receipt set corrects this by parsing the row named mte-interop-check and records its complete object.

Setup executed `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r58/T58W1Panel01/clone`, asserted clone toplevel, detached checkout at BASE. `rev-parse HEAD` printed BASE. Each nominated resolving commit passed `merge-base --is-ancestor COMMIT BASE` (exit 0, empty stdout), recorded in tree-evidence.json. Introducing diffs and full hashes are preserved in history-evidence.json.

## Residual risk and verification gaps

LSP device unavailable: `read xd://lsp` returned `No such tool`; no semantic LSP claims are made. Text locations and AST direct-call scans are the fallback. No runtime checks were executed; R51.1 execution is grounded in the committed receipt, not a new run. No new counter pass, saturation, admission, or resume-continuity claim is made. No declined verdict is used.

Read baseline routed-defect rows only for the seven explicitly carried ids; their status labels were not accepted as truth. The open result was independently re-derived from SCORECARD obligations and live base tool definitions. No round-57 waves/panel or other round-58 seat files were opened. All examined corpus/tool/evidence content came from the detached base clone (except the assignment's working-tree defect set).

No tools installed or updated. No lane implementation changes or staged patches. Scratch cleanup executed `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel01 && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W1Panel01`; exit 0, output `SCRATCH_REMOVED=/fast/scratch/hyaku/tameshi-r58/T58W1Panel01`. Scratch was deleted before this report was written.
