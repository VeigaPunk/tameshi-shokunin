# T51CritPrereg — C2 pre-registration & measurement attack (round 51)

Seat bounds respected: read-only on the lane checkout; all sweep reproductions and counter runs executed in scratch
(`/fast/scratch/hyaku/tameshi-r51/T51CritPrereg/`, deleted before yield). No tools installed. Commands below are the
evidence commands; all lane paths are relative to the lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

## F1 — Frozen-artifact provenance: spec is a single, untouched commit; spec.copy identical; SHA matches the counter
- `git log --format='%H|%cI|%s' -- .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec` → exactly one commit
  `fe335384` (`2026-10-26T20:52:43-03:00`). The spec was added in the pre-registration commit and never touched after.
- `sha256sum .ufo/evidence/round-51/c2/bash-drift-pins.defects.spec .ufo/evidence/round-51/c2/sweep/spec.copy` →
  both `a98271f639bc520f7052e63efaaa0b560cda959d3122d9c6921dcd1b9b61a602`; `git show fe335384:…/bash-drift-pins.defects.spec | sha256sum` → same, i.e. spec.copy in the sweep dir is byte-identical and equals the counter's `SPEC_SHA` (`measure.py:38`).
- Amendment 1 scope: `git diff --stat fe335384 84aa673a` → only `contract.json`, `control/controls-attempt1.stderr`,
  `control/controls.py`, `freeze.json` (28 insertions/5 deletions). The spec, sweep receipts, counter and predicates are
  untouched by the amendment. Both pre-registration anchors hold.

## F2 — Pinned bytes: every @old occurs exactly once (apply is guaranteed non-no-op)
- Materialized the pin: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8…:corpus/drift-pins.sh`
  → 19088 bytes, sha256 `c138d34c…` (matches spec header, sweep `MUTATE_TARGET` and `CONTROL pristine-sha256`).
- Counted each `@old` string in those bytes: all 10 count == 1 (mode compare, GONE block, `-gt 1`, count-pin equality,
  shape opt-in, sha compare, nlink, POLICY, DUP, usage exit). The runner's `py_helper apply` asserts count==1 and refuses
  otherwise (`tools/mutate-and-run.sh:423-426`), and every mutant sha in `results.tsv` differs from pristine — the
  mutations were genuinely applied. No "old string absent → no-op mutant" explanation is available.

## F3 — Predictions vs measured: 7/10 held, exactly as advertised
- Parse: `# PREDICT (KILLED|SURVIVED)` before each `@defect` in the spec (5 KILLED: K_MODE_CMP, K_GONE_ARM,
  K_AMBIG_GT, K_COUNT_GE, K_SHAPE_OPTIN; 5 SURVIVED: S_SHA_CMP, S_HARDLINK, S_POLICY, S_DUP_UNIQ, S_USAGE_EXIT).
- Measured (`sweep.txt` `DEFECT` lines / `results.tsv`): held = K_MODE_CMP KILLED, K_COUNT_GE KILLED, 5 × S_* SURVIVED = 7/10.
  Misses = the three kill-aimed K_GONE_ARM / K_AMBIG_GT / K_SHAPE_OPTIN, all SURVIVED.

## F4 — The suite string is NOT pre-registered anywhere machine-readable
- The only suite mention is prose in the spec header: `bash-drift-pins.defects.spec:3` ("Suite: hermetic `env -i … bash "$MUTANT" --selftest` (13 cases at the pin, alternate-baseline harness); verdict oracle = exit status only.").
- Round-51 `c2/` contains only `bash-drift-pins.defects.spec`, `measure.py`, `sweep/` — no `suite.txt`, no `predictions.json`, no `suite_sha256`, no runner-sha pin file. Contrast: rounds 16/18/26 pre-registered the suite machine-readably
  (`.ufo/evidence/round-16/round-gate/suite.txt`, `predictions.json`; `round-26/contract.json` `suite` field).
- Consequence: the measured table is underdetermined by the committed artifacts. The verdict oracle, sandbox naming and the
  13-case selftest are not bound by anything machine-checked; the L1's prose is not a frozen datum.

## F5 — Exact reproduction of the measured 2/10 with the canonical (historical) suite; evidence outputs byte-identical
- Reproduced the sweep from the committed spec + pinned target + base runner (sha `a7d3f2dd…`, same as `MUTATE_TOOL`),
  with the suite shape historically recorded for this harness (round-16/18/26 style, bash variant):
  `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C bash "$MUTANT" --selftest`
- Command: `bash tools/mutate-and-run.sh --target …/drift-pins.sh --defects …/bash-drift-pins.defects.spec --suite '<above>' --workdir … --label drift-pins --timeout 120`
- Observed: CONTROL GREEN, 2/10 KILLED (K_MODE_CMP, K_COUNT_GE), 8 SURVIVED, kill-rate 20% — exactly the committed table.
  All 11 `evidence/*.out` files are byte-identical to the committed receipts (`cmp -s` passes; `results.tsv` differs only in `duration-ms`).
- So the committed sweep is consistent with having been produced by this pipeline. But note this cuts both ways: the
  receipt bytes are deterministic (up to timings), so byte-identity does not prove the run happened in the window — a
  re-run today produces indistinguishable bytes (see F8).

## F6 — The three misses are an artifact of the *unrecorded* suite string; single-variable neutral-name probe kills all three
- Same sweep, same spec, same target, only `sandbox-$DEFECT_ID` → `sandbox` (neutral):
  `h="$WORKDIR/sandbox"; …`
- Observed: CONTROL GREEN, 5/10 KILLED — K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN all flip to KILLED; predictions 10/10.
- Mechanism (verified in the pinned `drift-pins.sh`): the selftest checks verdict words with an unanchored
  `grep -q "$3" <<< "$out"` (`drift-pins.sh:403`) over the gate's output. The gate prints scratch paths verbatim,
  e.g. the file-level drift line `printf 'DRIFT   %s %s\n' "$p" "${diffs[*]}"` (`:170`), `MOVED` (`:242`), `GONE`
  (`:232`), `AMBIG` (`:236`), `SHAPE` (`:220`). Under the canonical suite the selftest's `mktemp -d` root lives at
  `TMPDIR=$WORKDIR/sandbox-$DEFECT_ID/tmp` (runner `run_one` exports `WORKDIR`/`DEFECT_ID`: `tools/mutate-and-run.sh:452-460`),
  so every printed path contains the defect id; the substring (GONE/AMBIG/SHAPE) satisfies the `grep -q` even though the
  mutated assertion never fires. With a neutral sandbox name the substrings disappear and the same mutants red.
- The three "survivors" and the 2/10 kill-rate are therefore properties of the unrecorded suite string, not of the
  pre-registered spec or of the gate's semantics alone. The L1's announced probe (neutral names kill all three) is
  confirmed independently.

## F7 — The frozen counter checks nothing about the suite (nor results.tsv, nor evidence files, nor predictions)
- `.ufo/evidence/round-51/c2/measure.py` `sweep_check()` (`:134-159`) parses only `sweep.txt`: CONTROL GREEN with
  pristine-sha256 == PIN, one DEFECT line per spec id (no INCONCLUSIVE), MUTATE_RESTORE OK, MUTATE DONE, MUTATE_DATE >
  first-commit time. It never reads `results.tsv`, `evidence/*.out`, `MUTATE_SPEC`, `MUTATE_TOOL`, the suite, or the
  sandbox naming. Predictions are counted and printed but excluded from the predicate (`:22`, `:264-265`).
- `regression()` (`:162-187`) replays the runner at REV using whatever suite the leg embeds — a suite chosen later, not
  the one the sweep used.

## F8 — Pre-registration ordering: real but thin (19 s), and entirely self-stamped
- `MUTATE_DATE: 2026-10-26T23:53:02Z` vs spec-commit committer time 23:52:43Z (`git log --format=%ct`; the counter uses
  `%ct`): margin = 19 s. (Author time margin: 34 min.) The sweep ran before amendment 1 (23:55Z) and before the receipt
  commit `f0129a5` (00:05:09Z).
- `MUTATE_DATE` is written by the runner itself from the local clock (`tools/mutate-and-run.sh:498` — `date -u`). No
  external witness, journal entry or receipt-side timestamp binds the run to that instant; the receipts are self-authored.
  Nothing in the committed record proves the sweep ran exactly once, or that it ran on that host at that moment.

## F9 — Ways the case could be dressed up after the data, and what the record does / does not prevent
1. **Re-sweeping with neutral sandbox names** (or any suite that kills the three) — *prevented after commit*: the
   receipts are immutable in git since `f0129a5`; replacing them is a new, visible commit. *Not prevented before commit*:
   nothing attests how many sweeps happened in the ~12-min window between `fe335384` and `f0129a5`, or that the committed
   run was the only/first one; any pre-commit run could have been selected.
2. **Editing predictions** — *prevented*: the spec exists in exactly one commit (`F1`); any edit is a visible new commit.
   In any case predictions are outside the PASS predicate (`F7`), so they bind nothing.
3. **Doctoring sweep.txt fields** (CONTROL/verdict lines/date) before `f0129a5` — *not prevented*: the counter trusts the
   self-authored lines; nothing verifies them against the evidence files or an external clock.
4. **Choosing the suite after the data** — *not prevented* (F4/F7): the suite is unfrozen, so e.g. the neutral-name suite
   (5/10, predictions 10/10) or the defect-id suite (2/10) are both compatible with the same frozen spec; the recorded
   table can only be re-derived if the suite is guessed (F5 reproduced it exactly with the historical shape).
5. **Target/pin substitution** — *prevented at REV*: the counter requires pristine-sha256 in CONTROL == the leg's PIN and
   the PIN == sha256 of the owner-repo blob at the leg's rev (`measure.py:245-246`).

## F10 — At freeze and at HEAD, the "recorded case" does not exist in git yet; the sweep predates the ledger entry
- `git rev-parse HEAD:tools/mutate-and-run.sh` == `9962033:tools/mutate-and-run.sh` == `bb68156:tools/mutate-and-run.sh`
  == `2d81b929…`; `tools/mutate-and-run.sh` is byte-identical to base (round-30, 9 legs), and `MUTATE_TOOL` sha
  `a7d3f2dd…` in the receipt equals this HEAD blob (verified `sha256sum`).
- Counter at HEAD: `python3 .ufo/evidence/round-51/c2/measure.py --lane <clone> --rev HEAD --work <empty> --explain` →
  `recorded_cases=9 wired_legs=9 depth_score=9 new_legs=0 … C2_R51_PASS=false` (plus `REGRESSION: PASS (cases=9 passed=9)`).
- No `corpus/knowledge/mutation-case-kagi-drift-pins.md`, no drift-pins row in `corpus/SOURCES.md` at HEAD.
- So at freeze the only pre-registered C2 artifacts were the spec (defects+predictions) and the separate; the tenth ledger
  leg, its wiring and the sourced entry exist nowhere yet — they must be added before REV. The measured table therefore
  predates the ledger entry that must reproduce it; the table-replay consistency check will only bind a suite chosen later
  (F7). "Pre-registered in this freeze commit" is true only of the spec, not of the recorded case.

## Summary
- Frozen artifacts are consistent: spec added once in `fe335384`, sha = counter's SPEC_SHA, spec.copy identical, all 10
  @old occur once, amendment 1 touched only the controls harness; predictions 7/10 held as stated.
- The suite string is nowhere pre-registered (only prose in the spec header); the counter checks no suite, no results.tsv,
  no evidence files, no predictions.
- Independent reproduction: canonical historical suite → exactly the committed 2/10 with byte-identical evidence outputs;
  neutral-name single-variable probe → 5/10 (all three misses kill). The three survivors are an artifact of the unrecorded
  `sandbox-$DEFECT_ID` naming satisfying unanchored `grep -q` over printed scratch paths (`drift-pins.sh:403`).
- Ordering: MUTATE_DATE is 19 s after the spec commit, but is self-stamped (`mutate-and-run.sh:498`); no external witness;
  uniqueness of the sweep is asserted, not evidenced.
- Dressing-up: predictions and receipts are immutable post-commit; but the suite choice, sweep count/selection and receipt
  fields are unbound by the frozen record, and the runner/leg do not exist in git at freeze or HEAD (C2_R51_PASS=false today).
