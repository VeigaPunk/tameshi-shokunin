# ScorecardReview — tameshi round 12, wave w1

Seat: `ScorecardReview` (reviewer, leaf, read-only). Advisory, lane-internal.
This is NOT independent non-author promotion review and not an admission.
No score is awarded here. Tooling installed: none (used git, python3, grep, cmp
already present).

Owned write: this file only. Nothing under `SCORECARD.md`, `SHONEN.md`, `LOG.md`,
`tools/`, `corpus/`, or `reports/` was modified.

## 1. Axes named

| Axis | Rubric (as written) | Counting command | What the command actually measures |
|---|---|---|---|
| depth | 1 point per recorded mutation case in the pinned replay ledger, cap 10 (`SCORECARD.md:66`, command D `:72-73`) | regex over header comment rows of `tools/mutate-and-run.sh` | count of documentation rows in a comment block, not executed legs |
| calibration | 2 points per correctly restrained, durable-evidence-linked `[~]` box, cap 8; remaining 2 need independent review (`SCORECARD.md:67`, command C `:74-75`) | regex over `SHONEN.md` checkbox marks | count of marks only; cannot see "restrained", "durable", or link resolution |
| capability rows (not an axis) | a row enters only through a round that demonstrates the capability running (`SCORECARD.md:244`) | none | — |

Frontier touched: F2 (witness-scoped kills, bash leg) and F3 (determinism precondition), `corpus/README.md:79-80`; F4–F10 (`corpus/README.md:81-87`) not touched.

## 2. Evidence (commands run, read-only)

Measured against the pinned commits and HEAD `18ad5d0`.

```
# depth, pinned commit 284ab0f (SCORECARD command D)
recorded_cases=6 depth_score=6
# depth, HEAD
HEAD recorded_cases=6
# calibration, pinned commit 284ab0f (SCORECARD command C)
boxes=4 checked=4 asserted=0 untouched=0 asserted_mark_upper_bound=0
# calibration, HEAD SHONEN.md
HEAD boxes=4 checked=0 asserted=4 untouched=0 upper=8
# calibration, 121696b (the commit SCORECARD says the scored pin 6 was measured on)
- [~] x4 at lines 5,7,9,11   -> command C yields asserted=4, upper bound 8
```

Structural checks of the depth rubric (probe, in memory only):

- `tools/mutate-and-run.sh` at HEAD has 6 header rows (`:84-89`), 6 `REV_*`
  assignments, and 6 leg invocations (`:1113-1138`). The six rows have six
  distinct gate paths.
- Probe: appending one extra row
  `#   bash-surface-census  kagi-shokunin/corpus/surface-census.sh  8/10 (80 %)`
  to a copy of the text makes command D print **7**; counting unique gate paths
  prints **6**.

Structural checks of the calibration rubric:

- `reports/round-1-calibration.md:208` lists box 3 as `[ ]` ("assertion rejected").
  `SHONEN.md` box 3 (line 9) is `[~]` and links to
  `reports/round-1-kaika-coldread.md`, not to a box-3 anchor.
- `reports/round-1-calibration.md` has anchors `## box-1` … `## box-4` at
  lines 71, 105, 132, 167. Links for boxes 1, 2, 4 resolve to those headings.
- `SCORECARD.md:67` says the pinned 6 is "rubric of command C, box 3 excluded".
  Command C does not exclude box 3. It returns 8 at 121696b and at HEAD.

Determinism probes (saved evidence, not re-run):

- `.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout` and
  `h3-selftest-envi.stdout` are byte-identical (82 lines, 0 `/tmp/` strings),
  stderr identical. Exit files differ only because they record
  `duration-s`; the gate must compare exit codes, not raw wrapper bytes.
- `h1b-regression.stdout` contains per-run mktemp paths
  (`/tmp/tameshi-r4-2-regression.VGA0wT/…`, lines 8, 13, 18 and 4 more).
  Byte-identical repeat-control on `--regression` would mismatch on every run.

Repo state: `tools/` contains only `mutate-and-run.sh`. `tools/repeat-control.py`
does not exist at HEAD. No C1 capability is landed.

## 3. Findings (by severity)

### HIGH-1 — Calibration pinned 6 is not the output of the stated rubric command

- `SCORECARD.md:67` says pinned `6` = "rubric of command C, box 3 excluded".
- Command C at 121696b and HEAD prints `asserted=4 … upper_bound=8`. It does
  not exclude box 3. The 6 comes from a manual, non-counting adjudication
  (`LOG.md` fleet round 1 post-review entry; `SCORECARD.md:208-220`).
- `SHONEN.md:9-10` keeps box 3 as `[~]` ("lane assertion, scope-bounded").
  `reports/round-1-calibration.md:208` says `[ ]` ("assertion rejected").
  The two records disagree on the same box at HEAD.
- Consequence: the reproducible command output (8) and the scored value (6)
  differ. Anyone re-running command C gets 8. The 6 is not reproducible from
  the rubric.
- Recommendation (no edit here; owner: L1 / SHONEN owner): choose one of
  (a) set SHONEN box 3 back to `[ ]` so command C reproduces 6 at HEAD, or
  (b) add an explicit scored-exclusion field to the rubric and a command that
  reads it. Do not raise the score to 8 and do not treat box 3 as earned.
  Either choice needs a LOG entry naming the change.

### HIGH-2 — Depth command counts documentation rows, so a witness split is a trap

- Command D counts regex matches in the tool's header comment
  (`tools/mutate-and-run.sh:84-89`). It does not count executed legs and does
  not check that the pin resolves. A new comment row raises the score with no
  new gate (probe above: 6 → 7).
- The C2 brief says the bash-surface-census witness split must NOT count as a
  seventh gate. Under the current command, adding a witness-split row to the
  header is exactly the failure that would count.
- Required rule for recording the split (no edit here):
  1. Depth denominator = number of **unique gate paths** among the recorded
     legs, each with a `--regression` PASS at HEAD and a pin that resolves via
     `git cat-file -e <rev>:<path>`. Current value 6 under this rule.
  2. The witness split is a classification of the **same** 8 measured kills on
     `kagi-shokunin/corpus/surface-census.sh`. It is recorded as a
     sub-measurement (`killed-on-witness` / `accidental`) on the existing leg.
     Depth stays 6. It moves F2 only when a bash leg is measured
     (`corpus/README.md:79` next move; `corpus/README.md:115-118` partly held).
  3. Do not add a seventh header row for it.

### HIGH-3 — C1 gate: the control must be path-free, and the tool does not exist yet

- `tools/repeat-control.py` is absent at HEAD. Any capability row for C1 is
  premature until the tool runs. Its `--selftest` (exact IDs/exits) and
  `--snapshot` (tamper → `snapshot_tampered`, exit 2) must be executed and saved
  in `.ufo/evidence/round-12/<seat>/`.
- Byte-identity is a poor control choice for `mutate-and-run.sh --regression`
  (mktemp paths in every run; see §2). The selftest stdout is path-free and is
  the candidate control. Mismatch on a volatile control is a false
  `controls_mismatch`, not a flake finding.
- The gate must compare **exit codes parsed from the exit file** (the raw
  `exit=… duration-s=…` line differs run to run).
- Recommendation: the C1 selftest must include (a) a deliberately path-bearing
  control that reports `controls_mismatch` exit 1, and (b) a control with
  nonzero baseline that reports `baseline_nonzero` exit 2, so the mismatch class
  is proven to fire, not assumed.

### MEDIUM-1 — N = 3 identical runs is weak evidence of determinism

- Under an independent per-run binary-outcome model with per-run flake
  probability p, the chance that 3 runs are all identical is
  `(1-p)^3 + p^3`: p=0.05 → 0.857; p=0.1 → 0.730; p=0.2 → 0.520; p=0.5 → 0.250.
  [INFERENCE: binomial model; unmeasured on any gate.]
- Therefore `controls_match` means "3 observed identical runs of the control",
  never "deterministic" and never "flakiness cured". The capability row must use
  that wording. The contract already says this; the SCORECARD row must too.

### MEDIUM-2 — No independence in this wave

- Every seat in `round-12/w1` is a tameshi-dispatched same-lane seat (`spec.json`
  context: "Any reports are advisory lane-internal"). None of them is
  non-author promotion review. Calibration's last 2 points stay unearned, and
  no calibration move can be recorded from this wave.

### LOW-1 — Records not yet written

- `LOG.md` has no round-12 entry at HEAD (last entry: fleet round 1 phase-2).
  Every change needs one (contract). L1 owns it.

## 4. How to record capability improvements (no fraudulent scalar increments)

Apply per capability; each step is a precondition for the next.

1. **Land the artifact** at a committed path (C1: `tools/repeat-control.py`;
   C2: witness declaration file and its SHA-256, committed before the sweep).
2. **Demonstrate it running**, in the same round. Save stdout, stderr, and exit
   under `.ufo/evidence/round-12/<seat>/`. Record exact finding IDs and exit
   codes, not prose.
3. **Add a Capabilities row** (`SCORECARD.md` Capabilities table) with the
   command, the exit, and the evidence pointer. This is the only write C1 or C2
   earns on its own.
4. **Recompute the axis counting command** at the new commit. A scalar changes
   only if the command output changes under the rubric. Expected: C1 → calibration
   unchanged (command C counts `[~]` marks only); C2 → depth unchanged at 6 under
   HIGH-2's unique-path rule.
5. **Record the verdict as the command's output**, not as "improved". Use the
   verdict words the records already use (`axis moved`, `unchanged`,
   `unprovable-but-better`). "Improved" needs a measured before/after on the
   rubric.
6. **State independence explicitly**: "lane-dispatched; no independent promotion
   verifier". Do not cite this wave as independent review.
7. **Errata append-only.** Any miss or contradiction becomes an errata row
   naming the discriminator (`QUALITY.md` criterion 6).
8. **Leave the frontier honest.** Move a `corpus/README.md` ground only when its
   next move in the table is measured (`corpus/README.md:120-121`).

## 5. Exact owned paths

- Owned write: `.ufo/waves/round-12/w1/ScorecardReview.md` (this file).
- Read-only inputs used: `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`,
  `corpus/QUALITY.md`, `corpus/README.md`, `corpus/knowledge/witness-scoped-kill-verdict.md`,
  `reports/round-1-calibration.md`, `tools/mutate-and-run.sh`,
  `.ufo/evidence/kaika-round-1/capability-demo/*`,
  `.ufo/evidence/fleet-round-1/calibration-acceptance.json`, `LOG.md`,
  `.ufo/waves/round-12/spec.json`, `.ufo/waves/round-12/w1/swarm-registry.json`.

## 6. Residual risk and verification gaps

- No command was re-executed by this seat (none was assigned). All numbers are
  from saved evidence or from read-only `git show` / in-memory probes.
- The 80 % bash kill-rate, the 8/10 witness split, and the N = 3 probabilities
  are not measured on any bash leg here. [UNK]
- `git status` shows sibling edits to `corpus/SOURCES.md` and
  `corpus/knowledge/witness-scoped-kill-verdict.md`, and new
  `.ufo/evidence/round-12/`. Not mine; not read for content; not modified.
- L1 integrated checks still owed: run command D and C at HEAD; run the
  C1 selftest and `--snapshot` once `tools/repeat-control.py` lands; re-check the
  SHONEN box 3 disagreement (HIGH-1) before any calibration figure is cited.
