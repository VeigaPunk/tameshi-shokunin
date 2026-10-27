# T51LabWitDUPUNIQ — C2 survivor witness for S_DUP_UNIQ

Seat: T51LabWitDUPUNIQ (C2 depth, mutation-case 9/10, survivor witness). Date: 2026-10-26.
Gate under test: `corpus/drift-pins.sh` @ `e64e81b8eb96f3682b00c1e7a291e84420b280fa`
(kagi-shokunin; blob content sha256 `c138d34c7f0d…`, 451 lines, mode 100755 — matches the
spec header). Spec: `.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec`.
Frozen sweep receipt: `.ufo/evidence/round-51/c2/sweep/results.tsv:10` —
`S_DUP_UNIQ  SURVIVED  exit=0  mutant-sha256 1dd090f8…`.

**Verdict: HOLE.** The mutant is not equivalent to the pristine gate. Off-suite witnesses
exist on the gate's *normal* operating path (default baseline); the pristine/mutant
divergence is in exit code and in verdict lines. The suite cannot see it because every
selftest case passes `--baseline`, which disables the block containing the mutation.

## 1. Mutant construction (smallest behavior-bearing point)

One line, per the spec's `@defect S_DUP_UNIQ` (`@old`/`@new` occur exactly once in the
pinned bytes — verified):

```diff
--- pristine.sh (blob sha256 c138d34c…)
+++ mutant.sh  (sha256 1dd090f8a3efaa16e85b8127334441d7dce7ba65379edc5b6137b0888ab02c76)
@@ -185,7 +185,7 @@
-    done < <(printf '%s\n' "$pinned" | sort | uniq -d)
+    done < <(printf '%s\n' "$pinned" | sort | uniq -u)
```

- Mutant sha256 `1dd090f8…` **equals the frozen sweep's mutant hash** (results.tsv:10) —
  byte-identical rebuild of the sweep's mutant. Evidence: receipts `mutant.diff`,
  `sha256.txt`.
- Line numbers below are valid for the pinned blob (my `pristine.sh` is byte-identical,
  sha verified before and after all runs).

## 2. Why the suite misses it (code reading)

- `drift-pins.sh:40` — `BASELINE="$SCRIPT_DIR/drift-baseline.tsv"`;
  `:42` — `DEFAULT_BASELINE="$BASELINE"` is frozen **before** arg parsing, so the default
  baseline always sits next to the script copy.
- `:168` — `if [[ "$BASELINE" == "$DEFAULT_BASELINE" ]]; then` gates the closed-membership
  block (UNPINNED / EXTRA / DUP); `:186-188` is the DUP loop ending in the mutated
  `uniq -d` pipe.
- `:45-61` — `FILES` hardcodes 15 `$HOME/…` paths, so a scratch `$HOME` gives full control
  of the member set; `:62-70` `NOHASH` pins the 6 secret-shaped rows (`sha` must be `-`).
- `:400` — the selftest harness always invokes
  `out=$("$0" --baseline "$base" --symbols "$sym" 2>&1)`, so `:168` is false in **every**
  suite case and `:188` is never executed by the suite → the frozen SURVIVED. (The
  unanchored `grep -q` at `:403` is not involved for this mutant.)

## 3. Witness design

Driver: receipts `witness.sh` (run as `bash witness.sh $S`, scratch-only). It

1. builds `$S/wit/home` and materializes all 15 `FILES` paths as regular files
   (modes/content fixed before pinning);
2. seeds one symbol row (`$HOME/.local/bin/the-janitor<TAB>1<TAB>^#!`) and lets the
   **gate's own `--pin`** write a truthful 15-row baseline
   (`DRIFT_PINS: PINNED (files=15 symbols=1 line_updates=0)`, receipts `pin.out`) — the
   baseline is exactly what the gate expects, so the only injected defect is duplication;
3. runs pristine and mutant on identical inputs via
   `env -i HOME=$S/wit/home TMPDIR=$S/tmp PATH=/usr/bin:/bin bash <gate>`, 3 reps each,
   capturing stdout/stderr/exit (all stderr empty: `stderr-sizes.txt`, 0 bytes total).

Three inputs (baselines in receipts):

| id | baseline | dup rows |
|----|----------|----------|
| C | `baseline.pinned.tsv` — gate-pinned truth (15 unique rows) | 0 (control) |
| A | `baseline.A-dup.tsv` — 16 rows, `$HOME/.agents/AGENTS.md` twice | 1 |
| B | `baseline.B-alldup.tsv` — 30 rows, every row twice | all |

## 4. Observed results (3/3 reps each, deterministic — receipts `ledger.txt`, `*.out`, `*.exit`)

| input | pristine | mutant |
|---|---|---|
| C (clean baseline) | exit **0**, `DRIFT_PINS: CLEAN (files=15 symbols=1)` | exit **1**, 15 bogus `DUP` lines + `DRIFT_PINS: DRIFT (files_ok=15 files_bad=15 symbols_ok=1 symbols_bad=0)` |
| A (one dup row) | exit **1**, `DUP      $HOME/.agents/AGENTS.md (baseline has more than one row)` + DRIFT `files_bad=1` | exit **1**, 14 `DUP` lines naming exactly the **non**-duplicated paths (never AGENTS.md) + DRIFT `files_bad=14` |
| B (all rows dup) | exit **1**, 15 `DUP` lines + DRIFT | exit **0**, `DRIFT_PINS: CLEAN (files=30 symbols=1)` |

Differing lines on identical input (full diffs: receipts `A.diff`, `B.diff`):

- C: pristine's last line is `DRIFT_PINS: CLEAN (files=15 symbols=1)`; mutant's is
  `DRIFT_PINS: DRIFT (files_ok=15 files_bad=15 symbols_ok=1 symbols_bad=0)`.
- A: pristine prints `DUP      $HOME/.agents/AGENTS.md (baseline has more than one row)`;
  the mutant never names the true duplicate and instead flags the 14 correct rows.
- B: exit-code flip — pristine 1, mutant 0; the mutant blesses a fully-duplicated baseline.

The control C was expected to be a no-witness sanity check; it turned out to be the
simplest witness: on the gate's everyday default-baseline run the mutant already inverts
DUP semantics (`uniq -u` flags exactly the unique rows).

## 5. Equivalence-class argument (from the code)

The programs differ only at `:188`. On the sorted `pinned` list, `uniq -d` emits rows
occurring >1× and `uniq -u` rows occurring exactly 1×; these agree only when the list is
empty — a default baseline with no non-comment rows. The divergence is additionally gated
by `:168`, so it is invisible exactly on the alternate-baseline path (`--baseline`), which
is the only path the selftest exercises. Every real default-baseline invocation over the
15-row FILES set therefore distinguishes pristine from mutant. No input makes the mutant
behave like the pristine gate while printing DUP verdicts; and the mutant's exit 0 on
input B is unreachable for pristine.

This is a coverage finding for C2's survivor ledger (the suite's DUP assertion never runs
on the default-baseline path), not a verdict: I decide nothing; a probe is not a kill.

## 6. Controls and integrity

- Pristine bytes verified `c138d34c…` before and after all runs; gate copies that executed
  the 18 runs re-hash identically post-run (`sha256.txt`) — no self-modification
  (verify/pin write only baselines; no `--pin` in any witness run).
- kagi-shokunin untouched: `git -C …/kagi-shokunin status --porcelain=v1 -- corpus/drift-pins.sh`
  empty; rev `e64e81b8…` resolves; blob `8a2903dc` at that rev (`lane-untouched.txt`).
  Mutant bytes lived only under the scratch root, deleted after receipt copy.
- Lane writes: only `.ufo/waves/round-51/w1/T51LabWitDUPUNIQ.md` and
  `.ufo/waves/round-51/w1/T51LabWitDUPUNIQ/` (50 files). No git/jj mutations anywhere;
  no `/tmp` writes (TMPDIR pointed at scratch); no sibling-lane or fleet-repo writes.
- Tooling: none installed or upgraded (bash + coreutils only). No pacman use.

## Reproduce

```bash
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show \
  e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh > pristine.sh
cp pristine.sh mutant.sh   # then edit L188: uniq -d -> uniq -u
bash witness.sh <scratch>  # driver in T51LabWitDUPUNIQ/witness.sh
cat <scratch>/out/ledger.txt
```

## Summary
- Verdict HOLE: rebuilt S_DUP_UNIQ (sha256 1dd090f8… == frozen sweep receipt, one-line `uniq -d`→`uniq -u`) is not equivalent to the pristine gate.
- Witness on the gate's normal path: default baseline next to the script copy, scratch HOME materializing all 15 hardcoded FILES paths, gate's own `--pin` writes the truthful baseline.
- Clean baseline (control became witness): pristine exit 0 CLEAN vs mutant exit 1 DRIFT with 15 bogus `DUP` lines — 3/3 reps.
- One duplicated row: pristine names `$HOME/.agents/AGENTS.md`; mutant names exactly the 14 non-duplicates, never the duplicate — verdict-line divergence, 3/3 reps.
- All rows duplicated: pristine exit 1 vs mutant exit 0 `CLEAN` — exit-code flip; mutant blesses a defective baseline.
- Root cause of the frozen SURVIVED: selftest always passes `--baseline` (drift-pins.sh:400), and the DUP block is gated to the default baseline (`:168`), so `:188` is never suite-executed.
- Mutant ≡ pristine only for an empty pinned list; every real default-baseline run diverges.
- Lane and kagi repo untouched (status empty, hashes before/after equal); receipts: 50 files in `.ufo/waves/round-51/w1/T51LabWitDUPUNIQ/`; scratch deleted.
