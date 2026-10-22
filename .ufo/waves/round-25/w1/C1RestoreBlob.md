# C1RestoreBlob — R25 W1 (C1 calibration, repair-first)

Lane revision under test: `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` (base `1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5`).
Private clone: `/tmp/C1RestoreBlob-r25`, detached at the pinned revision, clean tree throughout.
Scratch (sweep logs + evidence): `/tmp/C1RestoreBlob-scratch/`. No tool installs were needed (no pacman/uv/npm activity). LSP: no language server answered for these bash/python files in this environment, so definition-level checks were made by reading the script sources directly; nothing below rests on grep-as-semantic-proof.

## Verdict

**Yes, both.**

1. The pristine sha256 printed by `MUTATE_TARGET` and `MUTATE_RESTORE` in **both** C1 sweeps equals the committed blob:
   `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` (11,799 bytes)
   = `git show c9ff09fb41fb8aac5fc335faf10858ff606bd5df:tools/command-binding.py | sha256sum`
   = the base revision's blob too, so the gate bytes are unchanged base→REV.
2. The gate under test is the committed one. Every byte the sweeps touched — target, runner (`tools/mutate-and-run.sh` sha `d22c4025e8ce38b8…`, == `git show REV:tools/mutate-and-run.sh`), suite (`.ufo/evidence/round-25/c1-suite.py`), both specs, and the ruler-owned fixtures — was staged from the clean pinned clone; the clone itself was never written (`git status --porcelain` empty before and after all runs).

Counter observation at this revision: `C1_ROUTED: dispositioned=0/3`. R23-ROUTED-1 and R23-ROUTED-2 **hold** (control green, restore OK, 6/6 and 8/8 defects KILLED with explicit witnesses) but are not dispositioned because `SCORECARD.md` at `c9ff09f` carries neither label. R23-ROUTED-3 does not hold: `dead-falsifier-disposition.json` is absent while 34 round-23 wave-2 seats are dead — exactly the repair work this wave owes. The executed-check substance of R1/R2 is already green at REV; the gap to 3/3 is record-keeping, not gate quality.

## Evidence

Setup (all commands run inside the clone or `/tmp` scratch only):

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/C1RestoreBlob-r25
git -C /tmp/C1RestoreBlob-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
# → HEAD: c9ff09fb41fb8aac5fc335faf10858ff606bd5df ; status --porcelain: empty
```

Blob identity, three ways (working tree / pinned REV / base):

```
sha256sum /tmp/C1RestoreBlob-r25/tools/command-binding.py                        → 9230c68e…1061d0d
git -C /tmp/C1RestoreBlob-r25 show c9ff09fb…:tools/command-binding.py | sha256sum → 9230c68e…1061d0d
git -C /tmp/C1RestoreBlob-r25 show 1f731573…:tools/command-binding.py | sha256sum → 9230c68e…1061d0d
```

Canonical counter, both sweeps through `c1-measure.py` (the lane's copy is byte-identical to the REV blob, sha `b18460c7ca559c18…`, verified before executing it):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-25/c1-measure.py \
  --repo /tmp/C1RestoreBlob-r25
# → C1_ROUTED: dispositioned=0/3
#   R23-ROUTED-1: holds=true control_green=true restore_ok=true witnessed_kills=M1..M6, scorecard_row=false
#   R23-ROUTED-2: holds=true control_green=true restore_ok=true witnessed_kills=G1..G8, scorecard_row=false
#   R23-ROUTED-3: holds=false reason="disposition file absent" dead=34
```

(`c1-measure.py` deletes its internal sweep workdirs with its tempdir, so the printed hash lines do not survive it; I therefore reproduced both sweeps with the identical argv its `sweep()` uses — same staged inputs, same suite command, `--label r25-multitoken` / `r25-selftest` — into persistent workdirs. The counter's own run independently asserts the same booleans in its JSON, so the two runs corroborate.)

Replica sweep 1 — multitoken ruler sweep (`multitoken-mutants.spec`, 6 defects, 7 fixtures):

```
MUTATE_TARGET: …/stage/tools/command-binding.py sha256=9230c68e…1061d0d bytes=11799
CONTROL: GREEN (exit=0 duration-ms=271 pristine-sha256=9230c68e…1061d0d)
  | MULTITOKEN_SUITE: 7/7 pass
MUTATE_RESTORE: OK (target-sha256 before=9230c68e… after=9230c68e… pristine-sha256=9230c68e…)
MUTATE: DONE (target=r25-multitoken defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)
```

Replica sweep 2 — guard-sweep rerun (`guard-mutants.spec`, 8 defects, 44-case selftest):

```
MUTATE_TARGET: …/stage/tools/command-binding.py sha256=9230c68e…1061d0d bytes=11799
CONTROL: GREEN (exit=0 duration-ms=1606 pristine-sha256=9230c68e…1061d0d)
  | COMMAND_BINDING_SELFTEST: 44/44 pass
MUTATE_RESTORE: OK (target-sha256 before=9230c68e… after=9230c68e… pristine-sha256=9230c68e…)
MUTATE: DONE (target=r25-selftest defects=8 killed=8 survived=0 inconclusive=0 kill-rate=100%)
```

Witness integrity (kill credit requires an explicit FAIL line in the per-defect log, never exit-code alone): all 14 evidence logs carry them — `sweep-multitoken/evidence/M{1..6}.out` hold `FIXTURE … FAIL` lines (e.g. M1: `FIXTURE mt-missing-first FAIL (exit=0 findings=[])`), `sweep-selftest/evidence/G{1..8}.out` hold `CASE … FAIL` lines (e.g. G4: `CASE negative-exit-mismatch FAIL` at its line 41). Each mutant dies of a distinct symptom (M1 any-of→5 fixtures fail; M2 first-token-only→middle/last unguarded; M5 over-strict→clean reordered cases fail), so the kills are independently attributable, not one shared failure.

Mechanism behind the hashes (`tools/mutate-and-run.sh`): `TARGET_SHA0` is pinned from the target before any suite run and the pristine copy is hash-checked against it (read-race refusal, :487-491); every suite run executes a fresh copy of the pristine or a mutant, never the target (`run_one`, `run_sweep` :506-541); after the last run the target and pristine are re-hashed and any change is a `MUTATE_RESTORE: DRIFT` SETUP refusal (:552-558). Full suite output goes to `evidence/<id>.out` (:421-431), which is what the counter's witness regex reads.

## Findings by severity

- **LOW (design reliance, not a defect):** `c1-measure.py` stages the sweep inputs from the `--repo` **working tree** (`shutil.copy2(repo / p, stage / p)` in its `main()`) with no internal revision pin. The runner's own `--regression` legs deliberately materialize via `git show <rev>:<path>` to be "immune to working-tree drift" (`tools/mutate-and-run.sh`, r7-1 block); the counter does not. The guarantee my item asks about therefore holds **because the operator supplied a clean clone pinned at the contract revision** — verified here — not because the counter enforces it. Pointed at a drifted working tree it would sweep drifted bytes silently, with no SETUP refusal. Smallest safe correction (recommendation only, for the integrator): record `git -C repo rev-parse HEAD` + dirty-state in the counter's JSON, or refuse a dirty tree — no behavioral change for a pinned clone.
- **INFO (expected pre-repair state, corroborates the C1 framing):** at `c9ff09f`, `dead-falsifier-disposition.json` is absent (`dead=34` matches the contract's 34 dead round-23 wave-2 seats) and `SCORECARD.md` has no `R23-ROUTED-1/2` rows, so 0/3 is the honest reading even though both sweeps' executed checks hold. R3's doctored-copy negative controls were not exercisable at this revision (no rows to doctor) — the counter's `disposition_failures` logic was read (:80-99) and its controls fire only once rows exist; re-check when the disposition file lands.

## Residual risk and verification gaps

- My first counter invocation was lost to my own staging race (I pointed it at the scratch directory the staging job was still rebuilding) and was re-run clean; the reported counter output is from the clean run `measure2.out`. The replica sweeps were single runs each; I did not repeat them for timing variance (durations varied 264–1664 ms per suite run, all well under timeouts, zero INCONCLUSIVE).
- The counter's temp workdirs are unrecoverable by design; hash-line evidence comes from my argv-identical replicas, and the counter's JSON booleans agree with them. The permanent artifacts for re-inspection live in `/tmp/C1RestoreBlob-scratch/` (outside the lane, per bounds).
- I verified the two C1 sweeps and blob identity only; the runner's `--selftest` and `--regression` ledger modes were not re-run (out of this item's scope). No lane file was written except this report; no git write command touched the lane, the fleet, or sibling repos; no installs were performed.
