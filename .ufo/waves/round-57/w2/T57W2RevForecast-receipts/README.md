# T57W2RevForecast receipts — cold-read forecast vs measured drift (round 57)

Seat `T57W2RevForecast` (wave 2, reviewer/forecast). Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base
`5e3569969b532310d2b8a3d130901757a3df356b`, C0
`ca75c2674645ab6bdadeecb8584007c74342bfa9`.

Every file here is a raw tool output. Commands are reproduced in
`.ufo/waves/round-57/w2/T57W2RevForecast.md`.

## Files

| file | what it is |
|---|---|
| `monitor-base.explain.json` | round-21 monitor at the BASE rev (`--explain`), full JSON |
| `monitor-c0.explain.json` | round-21 monitor at C0 (`--explain`), full JSON — the ground truth |
| `forecast-original-diffto.json` | the SHIPPED tool (`tools/cold-read-forecast.py`) `--diff-to C0` at base |
| `forecast-original-paths.json` | the SHIPPED tool `--paths <the 13 files C0 changed>` at base |
| `forecast-original-paths-skill-sections.json` | the SHIPPED tool `--paths … --skill-section` for the two SKILL sections C0 edited |
| `forecast-patched-diffto.json` | the STAGED (patched) tool `--diff-to C0` at base |
| `cold-read-forecast.patch` | `diff -u tools/cold-read-forecast.py <staged>` (the staged fix) |

## The two monitor runs (the ground truth)

```console
$ export HYAKU_SCRATCH=/fast/scratch/hyaku
$ S=$HYAKU_SCRATCH/tameshi-r57/T57W2RevForecast; mkdir -p "$S"
$ git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
$ git -C "$S/clone" checkout --detach 5e3569969b532310d2b8a3d130901757a3df356b
$ TMPDIR="$S" python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
      --repo "$S/clone" --rev 5e3569969b532310d2b8a3d130901757a3df356b --explain > "$S/measured-base.txt"
$ git -C "$S/clone" checkout --detach ca75c2674645ab6bdadeecb8584007c74342bfa9
$ TMPDIR="$S" python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
      --repo "$S/clone" --rev ca75c2674645ab6bdadeecb8584007c74342bfa9 --explain > "$S/measured-c0.txt"
```

Base: `sections_covered 64 / 64`, `calibration_restraint_score 8`, `uncovered_headings []`.
C0: `sections_covered 46 / 64`, `calibration_restraint_score 6`, `uncovered_headings` = 18.

## The three forecasts

```console
$ T=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/cold-read-forecast.py
$ python3 "$T" --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev 5e3569969b532310d2b8a3d130901757a3df356b \
      --diff-to ca75c2674645ab6bdadeecb8584007c74342bfa9 --json
$ python3 "$T" --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev 5e3569969b532310d2b8a3d130901757a3df356b \
      --paths .ufo/evidence/round-57/coldread-referent-r56.md SKILL.md corpus/QUALITY.md corpus/README.md \
               corpus/SOURCES.md corpus/knowledge/gate-row-exit-map.md corpus/knowledge/receipt-revision-binding.md \
               corpus/lessons/round-57.md tools/cold-read-forecast.py tools/fixtures/receipt-gate/accept.receipt \
               tools/fixtures/receipt-gate/drift.paths tools/fixtures/receipt-gate/drift.receipt tools/registry.json \
      --json
$ python3 "$T" --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev 5e3569969b532310d2b8a3d130901757a3df356b --paths <same 13 paths> \
      --skill-section '## Standing rules' --skill-section '### Gate/probe registry' --json
```

## The three defect fixtures (scratch clones of the lane, one fixture commit each)

Each fixture is a clone of the lane at base with ONE fixture commit
(`git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit`),
then the SHIPPED tool and the STAGED tool are run against it and the monitor
against it.

| fixture | what it changes | monitor (measured) | SHIPPED tool | STAGED tool |
|---|---|---|---|---|
| fx1 | a new `###` heading appended to SKILL.md | 64/65 covered, 1 uncovered | **0 lost** (miss) | 1 lost, `no-ledger-entry` |
| fx3 | the trailing `###` section removed from SKILL.md | 63/63 covered, 0 uncovered | **1 lost** (spurious) | 0 lost |
| fx4 | a mid-file `###` section removed from SKILL.md | 62/62 covered, 0 uncovered | **2 lost** (spurious) | 0 lost |
| fx2 | SKILL.md deleted | (cannot measure) | **exit 1, traceback** | exit 2, clean |

Fixture commands are in the report, section "The sweep".
