# MTMonitorInput — monitor input-drift mutation probe

Seat: mutation-tester (leaf). Round 36, wave 1. Claim under attack: C1
(calibration) — the cold-read monitor's input-drift gate.

## Attack

Took the refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c`
(score 8, 64/64) into an isolated clone, changed exactly ONE byte of
`corpus/QUALITY.md` there, committed it, and re-ran the same default-mode
monitor (`trace_gate: strict`, no overrides). Expected detector: the
re-anchored section(s) whose ledger entry cites `corpus/QUALITY.md` lose
credit and `calibration_restraint_score` drops from 8.

Scratch (only writes outside this report):
`/fast/scratch/hyaku/tameshi-r36-seats/MTMonitorInput/`
(`repo/` = `git clone --no-hardlinks` of the lane, checked out at
`b455001e`; the lane itself was never written).

Frozen monitor bytes exercised (hashes of the scratch checkout at
`b455001e`, identical to the lane's):
- `.ufo/evidence/round-21/coldread/measure.py` sha256
  `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`
- `.ufo/evidence/round-18/measure.py` sha256
  `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`
- `.ufo/evidence/round-21/coldread/ledger.json` sha256
  `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`
  (git blob `b0522d3c`; unchanged by the mutation commit)

## Commands (all revs explicit)

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r36-seats/MTMonitorInput/repo
git -C .../repo checkout b455001e2589b3f4f471d94a3de7e5e549b9f54c

# 1) pristine baseline at the refresh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /fast/scratch/hyaku/tameshi-r36-seats/MTMonitorInput/repo \
  --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c
# 2) do-nothing control at the content commit (reference only)
... --rev e423c41ba253357ab8c8513f0376dad9d38ab248
# 3) one-byte mutation, committed only in the scratch clone
#    corpus/QUALITY.md position 53418 (0-based): 0x65 'e' -> 0x66 'f'
#    ("entry that names a file" -> "entry that namfs a file", criterion 72)
git -C .../repo show --numstat 9e748c59a6e8892af8207e59422e6ebc4eae7734
#    1  1  corpus/QUALITY.md   (single-file, +1/-1, same 54133 bytes)
python3 .../measure.py --repo .../repo \
  --rev 9e748c59a6e8892af8207e59422e6ebc4eae7734 --explain
# 4) restore exact pristine bytes, re-run same detector
git -C .../repo checkout b455001e -- corpus/QUALITY.md
python3 .../measure.py --repo .../repo --rev b455001e2589b3f4f471d94a3de7e5e549b9f54c
```

Mutant commit `9e748c59a6e8892af8207e59422e6ebc4eae7734`, parent
`b455001e`; `--numstat` shows only `corpus/QUALITY.md`. The mutant rev's
ledger blob is byte-identical to `b455001e`'s (`b0522d3c`), so the commit
is exactly the one-byte input drift.

## Actual score lines (JSON fields, unmodified monitor output)

```
before  b455001e: "calibration_restraint_score": 8
                 "sections_covered": 64, "sections_total": 64
                 "box3_full_page": true | trace_gate strict | overrides_used false | ledger_committed true
control e423c41: "calibration_restraint_score": 6
                 "sections_covered": 60, "sections_total": 64
                 uncovered: 131, 375, 1380, 1436 (the four round-35-drifted sections)
mutant  9e748c59: "calibration_restraint_score": 6
                 "sections_covered": 63, "sections_total": 64
                 "box3_full_page": false
                 uncovered: 131 reason input-drift:corpus/QUALITY.md (round-36 entry)
                 box 1/2/4 marks still '~' (6 points); box-3 full-page point lost
restored b455001e: "calibration_restraint_score": 8
                 "sections_covered": 64, "sections_total": 64 (same detector on restored bytes)
```

`before-refresh.json` and `restored.json` are byte-identical
(sha256 `6b287d9e793aaa116528d91596f4f35ab94f29feb65626f75c99ee5241cab46d`).

## Entry-level attribution (round-36 re-anchored entries only)

| section | heading | trace | QUALITY.md input | input failures at b455001e | at mutant |
|---|---|---|---|---|---|
| 131 | Mutation-sweep recipe | `round-36/coldread/traces/L1/source-1.json` | yes (`f7382e20…`) | `[]` (credits) | `input-drift:corpus/QUALITY.md` |
| 375 | Restore discipline | `.../source-2.json` | no | `[]` (credits) | `[]` (credits) |
| 1380 | The map | `.../source-3.json` | no | `[]` (credits) | `[]` (credits) |
| 1436 | Where to enter | `.../source-4.json` | no | `[]` (credits) | `[]` (credits) |

## Verdict

KILLED — the input-drift detector fired: the monitor went from
`calibration_restraint_score 8, 64/64` to `6, 63/64` on a single drifted
byte, with the round-36 entry for section 131 failing exactly
`input-drift:corpus/QUALITY.md` and the box-3 full-page point flipping
false. The mutant cannot survive the assigned detector.

Coverage finding on the tasking premise: only ONE of the four
re-anchored sections cites `corpus/QUALITY.md`. The round-36
`refresh-specs.json` and trace receipts `source-1..4` show section 131
lists QUALITY.md while 375/1380/1436 list only
`corpus/README.md`/`tools/mutate-and-run.sh`/`corpus/knowledge/closeout-r11.md`.
The score still drops because calibration credit requires all 64
sections (box 3), so one uncovered section costs the 2 box-3 points; but
the four-section blast radius in the task text is not what the committed
ledger entries encode.

## Hashes / restoration evidence

- `corpus/QUALITY.md` before (b455001e): sha256
  `f7382e201ba34f2786f18eae114ff5d896356f083e9fd10d09a9c93f8af58782`,
  54133 bytes (blob `ca7ed9b`).
- after one-byte mutation: sha256
  `792360da4dddfe115ce6d79b5e449b7c87c2959b62095ccf3f81ad656ac4d961`,
  54133 bytes (blob `f70b2b1`); changed position 53418, `e`->`f`.
- after restore: sha256 back to
  `f7382e201ba34f2786f18eae114ff5d896356f083e9fd10d09a9c93f8af58782`,
  equal to `git show b455001e:corpus/QUALITY.md`; `git diff b455001e --
  corpus/QUALITY.md` empty. (Scratch worktree vs the mutant HEAD shows
  `M corpus/QUALITY.md`, the expected restored state; no lane bytes
  touched.)
- Scratch run artifacts: `before-refresh.json`, `control-content.json`,
  `after-mutant-explain.json`, `restored.json`, `mutrev.txt` under
  `/fast/scratch/hyaku/tameshi-r36-seats/MTMonitorInput/`.

Tooling: no installs, no upgrades, no pacman; Python 3 stdlib + git
read-only plumbing only. No other runtime invoked.
