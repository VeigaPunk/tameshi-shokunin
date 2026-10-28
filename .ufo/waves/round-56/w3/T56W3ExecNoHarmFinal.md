# T56W3ExecNoHarmFinal — no-harm at PIN 2f5512a8ab0771fb2eee463ec16db359174f5edd

## Command
`HYAKU_SCRATCH=/fast/scratch/hyaku /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 2f5512a8ab0771fb2eee463ec16db359174f5edd` (wall 54 s)

## Output (every line)
```
NOHARM commandD recorded_cases=10 depth_score=10 ok
NOHARM coldread-floor score=8 credited=64 ok
NOHARM r45-freshness population=74 fresh=71 score=9 ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-140 142 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
NOHARM r47-coverage rows=3 entries=3 C3_R47_PASS=true ok
NOHARM tools-scope [A:tools/receipt-revision-gate.py M:tools/registry.json ] ok
NOHARM registry-rows-not-shrunk base=56 rev=57 ok
NOHARM r49-generator-capability [PBT_STAGED_ID: cases=400 violations=0 counterexample=none classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31] ok
NOHARM r50-shrinker-selftest [SHRINK_SELFTEST: cases=14 failed=0] ok
NOHARM r53-scratch-hygiene tmp_hits=0 ok
NOHARM ledger-not-shrunk base=591 rev=609 ok
NOHARM sources-not-shrunk base=140 rev=142 ok
```
**ok = 15, RED = 0** (deciding run requires 15). No RED, so nothing to attribute to the round. (My trailing `grep -c RED` returned exit 1 because the count was 0; the script itself printed all 15 lines.)

## Monitors still fire at PIN (scratch `git clone --shared` of the lane, `checkout --detach PIN`, toplevel asserted equal to the clone dir before each commit, committed with `-c user.name/email`; the lane repo was never touched; each mutant run through the same no-harm.sh with LANE=<clone> REV=<mutant commit>)

| mutation (on PIN) | mutant rev | monitor line | result |
|---|---|---|---|
| delete one recorded case line (`#   bash-drift-pins ... 2/10`, line 97 of `tools/mutate-and-run.sh`) + pop one ledger entry | 9e9f9611b957c1dd687148f2508d3fc6a87793ab | `NOHARM commandD recorded_cases=9 depth_score=9 RED` | FIRES |
| same | same | `NOHARM ledger-not-shrunk base=591 rev=608 ok` | does NOT fire (floor is base 591, PIN has 18 spare) |
| delete the S282 row of `corpus/SOURCES.md` | 3ecf0de9548044e7a5def76731890023c49196ae | `NOHARM coldread-floor score=6 credited=51 RED` | FIRES (indirectly; the cold-read credit depends on a SOURCES row) |
| same | same | `NOHARM sources-not-shrunk base=140 rev=141 ok`, `registry-rows-not-below-140 141 ok` | does NOT fire (floor is 140, PIN has 2 spare) |
| delete last 3 SOURCES rows + last 19 ledger entries | fc771a3ecdfe0ec6b9f043a274e8363313555fc0 | `NOHARM registry-rows-not-below-140 139 RED`, `NOHARM sources-not-shrunk base=140 rev=139 RED`, `NOHARM ledger-not-shrunk base=591 rev=590 RED`, `NOHARM coldread-floor score=6 credited=45 RED` | ALL FIRE |

## Reading
- The commandD monitor (recorded cases) fires on a one-case drop (10 -> 9).
- The SOURCES shrink-by-one is caught by `coldread-floor` (RED), not by the row-count monitors: `sources-not-shrunk` / `registry-rows-not-below-140` have slack of 2 rows (floor = base 140, PIN = 142), and `ledger-not-shrunk` has slack of 18 (floor = base 591, PIN = 609). They fire once the count crosses below base (shown by the 3-row / 19-entry mutant). This is by design of the carried round-55 floors, not a defect of the round; noted so nobody claims the count monitors are a one-row tripwire.
- Scratch clones removed on exit (trap); no lane files, no mutating git outside the scratch clones.
- No tools installed.
