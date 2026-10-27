# T51CritEquiv — C2 equivalence attack: the eight round-51 survivors

Seat: T51CritEquiv (critic). Item: for each of the eight surviving mutants in
`.ufo/evidence/round-51/c2/sweep/sweep.txt`, argue from the pinned code whether it is
an equivalent mutant, a selftest hole, or an environment-satisfied assertion, using the
lane's own survivor rule (corpus/knowledge/r43-survivor-resolution-rule.md, K/D/E/U).

## Method (what I ran)

1. Pinned bytes: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show
   e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh` → sha256
   `c138d34c…`, 451 lines, mode 100755 — matches the spec's pin and the sweep's
   MUTATE_TARGET (`sweep.txt:3`).
2. Spec: `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec` — each `@old`
   occurs exactly once; I applied the ten edits with the runner's own escape decoder
   (`tools/mutate-and-run.sh:314-340` `py_helper::unescape`). The byte-identical
   mutant + pristine copies were taken from the L1 sweep workdir
   `/fast/scratch/hyaku/tameshi-r51/L1/sweep/w/` (`pristine.drift-pins.sh`,
   `mutant-<ID>.drift-pins.sh`; their sha256s equal `results.tsv`), so every probe
   below runs the *sweep's own artifacts*.
3. Reproduction: each mutant run under the sweep's exact suite shape
   (`h="$WORKDIR/sandbox-$DEFECT_ID"; … TMPDIR="$h/tmp" … bash "$MUTANT"
   --selftest`) → CONTROL GREEN, K_MODE_CMP + K_COUNT_GE KILLED, the other eight
   SURVIVED — identical to `sweep.txt`.
4. Single-variable probe: the same ten mutants with the sandbox dir renamed to a
   fixed name carrying **no defect-id substring** (TMPDIR under `…/hbx/tmp`). The
   three kill-aimed misses flip to KILLED on their own declared selftest cases; the
   five S_* survivors stay green.
5. Distinguishing-input witnesses: for each S_* survivor, a minimal verify run
   (pristine vs mutant) showing a real input on which they differ.

## Result: the eight survivors

| # | Mutant (sweep) | Pinned lines (edit) | Class (r43 K/D/E/U) | What distinguishes it |
|---|---|---|---|---|
| 1 | K_GONE_ARM | `drift-pins.sh:231` `if [[ "$n" -eq 0 ]]` → `-eq -1` (GONE printf at 232) | **U / not_killed — environment-satisfied assertion** (not a hole: the input exists and kills when the harness stops leaking) | The selftest case "symbol gone" *is* the discriminating input (value pin, n=0). Pristine prints `GONE …`; the mutant falls through to the else branch (`actual=$(grep -nE -m1 …)` fails under `set -euo pipefail`, exit 1, no GONE verdict). The case only passes because the same fixture also changes b.txt's sha, so the file loop prints `DRIFT … b.txt sha …` whose path contains the sandbox dir name `sandbox-K_GONE_ARM` ⊇ "GONE"; the run() oracle is `grep -q 'GONE'` (line 403), unanchored. Neutral sandbox → `drift-selftest: FAIL symbol gone: no /GONE/ in output` → exit 1. |
| 2 | K_AMBIG_GT | `drift-pins.sh:234` `elif [[ "$n" -gt 1 ]]` → `-gt 2` | **U / not_killed — environment-satisfied assertion** | The case "symbol ambiguous" (two matching lines, value pin) is the distinguishing input: pristine prints `AMBIG`; the mutant accepts it as a single match. The case passes because the same fixture changes b.txt lines 1→2, so the file loop prints `DRIFT … b.txt lines …` with `sandbox-K_AMBIG_GT` ⊇ "AMBIG" satisfying `grep -q 'AMBIG'`. Neutral sandbox → `FAIL symbol ambiguous: no /AMBIG/ in output` → exit 1. |
| 3 | K_SHAPE_OPTIN | `drift-pins.sh:220` `if [[ "$shape" == "shape" ]]` → `"shaped"` | **U / not_killed — environment-satisfied assertion** | The case "shape drift" (env.txt gets a non-assignment line) is the distinguishing input: pristine prints `SHAPE`; the mutant never runs the shape assertion. The case passes because the same fixture changes env.txt lines 2→3, so the file loop prints `DRIFT … env.txt lines …` with `sandbox-K_SHAPE_OPTIN` ⊇ "SHAPE" satisfying `grep -q 'SHAPE'`. Neutral sandbox → `FAIL shape drift: no /SHAPE/ in output` → exit 1. |
| 4 | S_SHA_CMP | `drift-pins.sh:156` `[[ "$cs" != "$sha" ]]` → `[[ "$cs" != "$cs" ]]` | **U / not_killed — selftest hole** (reachable-input survivor) | No selftest case changes content without also changing lines/mode or a symbol pin, so the sha compare never fires. A same-length, same-mode content edit distinguishes it: witness `alpha\nbeta\n` → `alpha\nbata\n` (same lines, same mode, new sha) → pristine exit 1 `DRIFT … sha …`, mutant exit 0 `CLEAN`. |
| 5 | S_HARDLINK | `drift-pins.sh:135` `if [[ "$nlink" -gt 1 ]]` → `-gt 2` | **U / not_killed — selftest hole** | No selftest case creates a hardlink (the only link case is a symlink, caught by `-L` at line 130 first). A regular file with nlink=2 distinguishes: witness `ln a.txt hard.txt` → pristine exit 1 `LINK … (hardlink count 2 …)`, mutant exit 0 `CLEAN`. |
| 6 | S_POLICY | `drift-pins.sh:145` `if [[ "$sha" != "-" ]]` → `if [[ "$sha" == "-x" ]]` | **U / not_killed — selftest hole** | The selftest's only no-hash row (env.txt) always carries sha `-`, so the POLICY refusal is never reached. A no-hash baseline row that asks for a real hash distinguishes: witness `DRIFT_EXTRA_NOHASH=env.txt` + baseline row sha=`0123456789ab…` → pristine exit 1 `POLICY … baseline sha must be `-` …`; mutant skips the refusal and prints `DRIFT … sha 0123456789ab->-` — i.e. it *leaks the first 12 hex chars of the secret-derived hash* the guard exists to withhold. |
| 7 | S_DUP_UNIQ | `drift-pins.sh:188` `uniq -d` → `uniq -u` | **U / not_killed — selftest hole** | The membership/DUP block (lines 168-189) runs only for the default baseline; every selftest case passes `--baseline`, so it is skipped. A default-baseline verify distinguishes in both directions: (a) clean 15-row baseline → pristine exit 0 `CLEAN`, mutant exit 1 with a false `DUP` per row; (b) one duplicated row → pristine exit 1 with exactly the true DUP, mutant suppresses the true duplicate (and floods false DUPs). |
| 8 | S_USAGE_EXIT | `drift-pins.sh:88` `exit 2` → `exit 0` | **U / not_killed — selftest hole** | The selftest re-invokes the gate with known flags only; no case passes an unknown argument. Witness `bash drift-pins.sh --r51-no-such-flag` → pristine exit 2, mutant exit 0 (same message). |

None of the eight is an equivalent mutant (E): every row above names a real input on
which the mutant's observable behavior differs from the pristine tool, and none is a
dead-code-only survivor (D): the edited constructs are on reachable paths (the
selftest's own cases reach them — the three K_* cases kill when the harness stops
masking). All eight are therefore `U` (not_killed) under the r43 rule, with two
mechanisms: the three K_* are **environment-satisfied assertions** (the input exists
inside the selftest; the sweep verdict oracle — exit status + unanchored `grep -q`
over path-printing output — is satisfied by the sandbox directory name, which embeds
the defect id), and the five S_* are **holes** (the discriminating input class is
absent from the 13-case suite).

## Evidence commands (all run from scratch; lane read-only)

- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8…:corpus/drift-pins.sh` — pinned bytes (sha `c138d34c…`).
- `ls /fast/scratch/hyaku/tameshi-r51/L1/sweep/w` — sweep artifacts: `pristine.drift-pins.sh`, `mutant-<ID>.drift-pins.sh`, `sandbox-<DEFECT_ID>/` dirs (confirms the suite names its sandbox per defect id).
- `sha256sum` of copied `mutant-<ID>` files equals `.ufo/evidence/round-51/c2/sweep/results.tsv` mutant-sha256 column.
- Selftest runs (per mutant, `env -i PATH=… HOME=… TMPDIR=… bash <mutant> --selftest`): defect-id sandbox → 2 KILLED / 8 SURVIVED (matches `sweep.txt`); neutral sandbox → K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN KILLED, five S_* unchanged.
- Witness runs: `bash drift-pins.sh --baseline B --symbols S …` (S_SHA_CMP, S_HARDLINK, S_POLICY), default-baseline verify under scratch `$HOME` (S_DUP_UNIQ), `--r51-no-such-flag` (S_USAGE_EXIT) — pristine vs mutant exit/verdict differences as tabulated.

## Summary
- All eight survivors are U (not_killed) under r43; none is E (equivalent) and none is D (dead-code-only): every survivor has a concrete distinguishing input.
- Three kill-aimed misses (K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN) are environment-satisfied: their own selftest cases contain the discriminating input, and kill when the sandbox path stops leaking the verdict word.
- Mechanism of masking: suite names sandbox `sandbox-$DEFECT_ID` (confirmed in `w/`); path-printing verdict lines (DRIFT etc.) then contain the defect id; selftest `run()` uses unanchored `grep -q "$3"` (`drift-pins.sh:403`) on that output.
- Independent confirmation of the L1 probe: with a fixed neutral sandbox name, all three flip to KILLED on their declared cases (`FAIL symbol gone/ambiguous/shape drift: no /GONE|AMBIG|SHAPE/ in output`).
- Five S_* survivors are genuine selftest holes: no same-length-content case (S_SHA_CMP), no hardlink case (S_HARDLINK), no no-hash-with-hash case (S_POLICY), no default-baseline run (S_DUP_UNIQ), no unknown-arg case (S_USAGE_EXIT).
- S_POLICY's hole is the most serious: the mutant would leak 12 hex chars of a secret-derived hash where the pristine gate prints a refusal.
- S_DUP_UNIQ's mutant not only misses duplicates but false-positives every unique row on a clean default baseline.
- No killing witness requires touching the lane: all probes used scratch copies of the sweep's own pinned artifacts.
