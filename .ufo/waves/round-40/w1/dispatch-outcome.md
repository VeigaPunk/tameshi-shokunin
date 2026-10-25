# Round-40 wave 1 — dispatch outcome

date: 2026-10-24 · wave: round-40-w1 · policy v2 (band 64-128) · L1: Kimi fresh L1 (attempt 1; the first L1 died on a provider-route failure after the freeze commit and during the wave, and this L1 resumed the same round)

## Grant and dispatch

```
$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/wave-slot.sh acquire tameshi round-40-w1 64 120
granted lane=tameshi wave=round-40-w1 seats=64
```

The grant is recorded in the seat ledger as `1792889233 64 tameshi round-40-w1`
(`~/.local/state/shokunin-hyaku/wave-slots`), taken at 2026-10-24T21:47:13-03:00,
immediately before the wave was dispatched. It was released only after the
settlement classification below (`released lane=tameshi wave=round-40-w1`,
exit 0).

`ufo-swarm-wave.mjs plan` and `run` exit 0 under
`scripts/hyaku/ufo-wave-policy-v2.json` (`waveMinLanes` 64, `waveMaxLanes` 128,
`maxLanes` 256). `run` wrote `.ufo/waves/round-40/dispatch-w1.json`: one
`taskCall` carrying `context` + 64 tasks, `counts.spawn=64`, `resume=0`.

The Kimi L1 has no AgentSwarm tool on this surface, so the batched call was the
one `taskCall` in `dispatch-w1.json`, issued by a single headless `omp -p`
dispatcher session
(`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-25T00-47-28-539Z_01a17086-db1b-7336-9e26-0aa8c7ded5d1.jsonl`).
The wave was not split, no seat was replaced, and no prepared spec was counted
as a seat. The 64 landed reports are the count.

## Settlement

Parent start `1792889248` (2026-10-24T21:47:28-03:00). Parent exit
`1792890156` (2026-10-24T22:02:36.574-03:00). Last seat terminal `1792890156`
(`ReviewQ123`, 2026-10-24T22:02:36.564-03:00). Delta +10 ms; 0 s at
unix-second resolution.

```
$ python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-40/settlement-receipt.json
WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal
exit 0
```

```
$ python3 tools/wave-parent-settle.py --selftest
WAVE_PARENT_SELFTEST: 3/3 pass
exit 0
```

The dispatcher's own final line was
`DISPATCH_RESULT terminal=64 elapsed_s=760 holding=1` — the hold loop polled
every 20 s and saw `active` fall 64 → 0 over 760 s, then the parent stayed up
until the last seat disposed.

Independent of the receipt, the OMP log
`/home/vgpnk/.omp/logs/omp.2026-10-24.3225220.log` records 65 `Session exit
recorded` lines: 64 seats plus the parent, every one `kind=normal`,
`reason=dispose`, `pendingToolCalls=0`, no duplicate seat name, and every
registry member present in both the exit list and the report directory.

## Seats

- Dispatched: 64. Reports landed: 64 (all non-empty). Dead seats: 0. Aborted
  transcripts: 0.
- Roles: connector 1, scout 8, executor 6, scribe 3, sentinel 1, revenger 1,
  simplifier 1, reviewer 20, critic 12, mutation-tester 11.
- Attack roles (reviewer, critic, mutation-tester): 43/64 (67.2%).
- The L1 holds the planner seat. The validator rejects `planner`.

## What the attack seats changed

No attack falsified a frozen predicate. Two findings are disclosed rather than
repaired, because the rule was frozen before data:

- `CriticHardcode` — a tool that hardcodes the five fixture strings can pass
  `live_json_v2` but cannot reach `C1_R40_PASS=true` without the pinned
  sha256. The pin is what closes it.
- `CriticUniversal` — `os.symlink`, `os.link`, `Path.symlink_to`,
  `Path.rename`, `shutil.*`, `os.remove/unlink` and `handle.write` are outside
  v2's `WRITE_RE`; `tools/repeat-control.py:807-823` writes `expected.json`
  through a variable path and through `os.symlink`. The frozen predicate claims
  no universality, so the pass bit stands and the gap is recorded in the round
  lesson's Holds.
