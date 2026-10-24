# Residual review — C1 calibration counter (round 37, attempt 3, seat ResC1Counter)

Lane tip: `ba3c35fb6c9582fcf2351c59c61661dd7a8e7400`. Read-only audit; no lane,
`.ufo/state`, or git-write mutations performed (the one re-execution below writes
only under `/tmp`).

## Verdict

**Claim C1 survives.** The counter reproduces the claimed calibration endpoints
exactly, and no second unsuperseded r36 control-input mismatch exists. One
MINOR same-class finding outside C1's claim scope (r37 C2 mutation-falsifier
receipts citing unresolvable scratch revisions, unacknowledged by any erratum).

## 1. Calibration re-runs (executed)

| Rev | Output | Exit |
|---|---|---|
| `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` | `C1_R37: unresolved_control_inputs=1 old_mutant_resolves=0 correction=0 manifest_ok=0 receipts_ok=0 … C1_R37_PASS=false` | 1 |
| `32826f37eb40afa6b2497425eecc95e23dacc5ee` | `C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1 manifest_ok=1 receipts_ok=1 … C1_R37_PASS=true` | 0 |
| `ba3c35fb6c9582fcf2351c59c61661dd7a8e7400` | `C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1 manifest_ok=1 receipts_ok=1 … C1_R37_PASS=true` | 0 |

Matches the claim (false at `d9c496b`, true at `32826f3` and tip). The committed
receipts `.ufo/evidence/round-37/calibration/{before-final-control,after-control-final}.stdout`
are byte-identical to these re-runs (same fields, same flags). Ancestry is fair:
`d9c496b` is an ancestor of `32826f3` (`git merge-base --is-ancestor` → yes), so
the before/after pair is a genuine progression of the same counter
(`.ufo/evidence/round-37/calibration/measure.py`, unchanged between the two
revs' freeze commit `c2b08d70`).

Counter internals verified against the contract kill_rule:

- `correction` = SCORECARD.md at rev contains `### Round 36 control-input erratum (round 37)`.
- `manifest_ok` = committed `.ufo/evidence/round-37/control/empty-panel/manifest.json`
  parses; `source_revision` (`d9c496b`) resolves; `rev-parse source_rev:.ufo/evidence/round-35/c1/panel`
  equals `source_panel_tree` (`4f3d8af5…`); specimen counts 9/0; the empty-panel
  dir contains exactly `[manifest.json]`.
- `receipts_ok` = replay receipt contains `C1_R35_CONTROL_PASS=true` + `pub_kill=0/0`
  and `C1_R36V2_CONTROL_PASS=false` + `pub_slots=0`, `mode=control`,
  `EMPTY_PANEL_REPLAY_PASS=true`, `counter_rev ==` manifest `source_revision`,
  both `panel_rev`/`counter_rev` resolve as commits, `panel_rev` ancestor of rev.
  Committed receipt: `counter_rev=d9c496b…` `panel_rev=c2b08d70…` — `c2b08d70`
  is the freeze commit "round-37: freeze claims and empty-panel input", ancestor
  of tip (verified).
- `mismatches = 0 iff` old mutant `91373d55…` unresolvable AND all three above.

Replay re-runnability: `.ufo/evidence/round-37/control/replay-empty-panel.py`
(140 lines, committed in the same freeze commit `c2b08d70` as manifest,
contract, and both counters) writes only under `--work-root`. Re-executed at the
recorded revs with a `/tmp` work root; see §4 for the diff result.

## 2. Second-mismatch hunt (executed, exhaustive over committed trees)

Method: `git grep -hoE '\b[0-9a-f]{40}\b'` over `.ufo/evidence/round-36` and
`.ufo/evidence/round-37` at the tip → 104 unique revisions; each tested with
`git cat-file -e <rev>^{commit}`/`^{tree}`/bare in the lane → **49 unresolvable**.
The counter structurally cannot see any of them (it hardcodes exactly one rev,
`OLD_MUTANT = 91373d55…`, and only re-validates the r37 replay receipt).
Classification of all 49:

1. **46 unresolvable revs — cross-repo coldread provenance keys, not control
   inputs.** Every occurrence sits inside the three r36 monitor receipts
   (`control/monitor-at-e423c41b.stdout`, `after/monitor-at-796e08b.stdout`,
   `after/monitor-at-b455001e.stdout`) in the shape
   `/home/vgpnk/Projects/<project>@<rev>:<path>` → sha256 (`shokunin@`,
   `kagi-shokunin@`, `kumitate-shokunin@`; verified by prefix-extracting every
   match, only these three shapes occur). These are content-address records of
   external-input files read during coldread; they were never lane objects. The
   monitor control receipt's own input rev (`e423c41b`) resolves. Not control-input
   mismatches.
2. **`b8c60bc9…` — not a git citation.** It is the `id=` query parameter of a
   cgit URL (`cgit.git.savannah.gnu.gov/.../bashref.texi?id=b8c60bc9…`) in
   `round-37/census/{end,end-attempt3}.stdout`. Coincidental 40-hex string.
3. **3 unresolvable revs — genuine same-class citations, but outside C1's
   claim scope (MINOR finding, below).**

Upstream check: `.ufo/evidence/round-35` cites 6 unique revisions, **0
unresolvable** — the source-panel chain the manifest points at is fully
resolvable.

**No second unsuperseded r36 control-input mismatch exists.** The r36 control
directory contains exactly three receipts; the two empty-panel receipts cite
only `rev=91373d55…` (the one mismatch, superseded), and the monitor control's
input rev resolves. The C1 claim's "one" is accurate within its scope.

## 3. Finding — MINOR: unsuperseded unresolvable `rev=` inputs in r37 C2 mutation falsifier receipts

- `.ufo/evidence/round-37/mutation/parity-frozen-predicate.stdout:3` — `rev=36a8c475dcd29ac4e91f9fd3ec9ebc775af71c90` (unresolvable)
- `.ufo/evidence/round-37/mutation/branch-removal.stdout:7` — `rev=871153829dda96950226d83ec41f6b88d3ae614d` (unresolvable)
- `.ufo/evidence/round-37/mutation/pristine-frozen-predicate.stdout:3` — `rev=a0a6bfd20f840d97c5bc456f726ff2a05262670c` (unresolvable)
- `.ufo/evidence/round-37/mutation/scratch-revs.txt` — labels all three `pristine=`/`mutant=`/`parity_mutant=`

Same defect class the round itself treated as a live mismatch at r36 (receipt
claims a run at a revision absent from the lane object database → run
unverifiable): C2's anti-vacuity falsifiers (parity run, branch-removal kill)
rest on runs that cannot be re-verified. Unsuperseded: `git grep` for the three
revs across SCORECARD.md / LOG.md / QUALITY.md / lessons / .ufo/reports at the
tip → zero hits; no erratum covers them.

Why MINOR, not MAJOR: the C1 contract scopes the claim to "the round-36
empty-panel control's unreachable scratch revision" and its before-expected
enumerates exactly that one mismatch; the C2 contract (`kill_rule`) freezes
fixture bytes and tool pin but does not require resolvable falsifier revisions,
and `scratch-revs.txt` discloses the scratch nature in the committed evidence.
Neither claim's stated contract is violated, and the C1 counter's count of one
is correct within its declared scope. The gap is consistency with the round's
own erratum discipline.

Smallest fix: add a short "Round 37 mutation-falsifier scratch-revision erratum"
alongside the three existing r36 errata, stating the three receipts remain
historical outputs of scratch worktree commits (mirroring the r36 treatment) —
or, if the falsifiers must stay load-bearing, re-run them at a committed
revision and commit the replacement receipts.

## 4. Replay re-execution result

Command (no lane writes; scratch under `/tmp`):
`python3 .ufo/evidence/round-37/control/replay-empty-panel.py --lane . --rev d9c496b… --panel-rev c2b08d70… --work-root /tmp/r37-replay-check/work`.

Result (executed 2026-10-24): **exit 0; output byte-identical to the committed
receipt** — `diff` of the re-run against
`.ufo/evidence/round-37/control/replay-at-final-control.stdout` is empty
(`REPLAY_RERUN_MATCHES_COMMITTED_RECEIPT`), including `COUNTER_SOURCE v1/v2`
sha256s (`d360a159…`, `9eb8944c…`), both control summary lines
(`C1_R35_CONTROL_PASS=true`, `C1_R36V2_CONTROL_PASS=false`), and the final
`EMPTY_PANEL_REPLAY: … counter_rev=d9c496b… panel_rev=c2b08d70… v1_pass=1
v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true` line. The replay is genuinely
re-runnable from committed bytes at the recorded revisions. (Operational note:
the runner needs stdin closed — `< /dev/null` — and ~125 s; the first attempt
stalled inheriting an open stdin in a background shell, not a lane defect.)

## Residual risk and verification gaps

- The counter binds the replay receipt's `counter_rev` to the manifest and
  checks `panel_rev` ancestry, but cannot cryptographically prove the replay ran
  against the committed empty-panel directory bytes; mitigated by the runner
  being committed and re-executed here with matching output (§4).
- I did not independently re-run the r36-era frozen counters on the r35 source
  panel (out of C1 scope; r35 chain fully resolvable per §2).
- Text grep was the only available semantic tool for citation classification;
  every classified occurrence was prefix-extracted and shape-checked, not
  sampled.
