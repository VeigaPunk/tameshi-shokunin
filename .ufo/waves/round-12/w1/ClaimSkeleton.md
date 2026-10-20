# ClaimSkeleton — round 12 wave w1 (tameshi)

Seat: ClaimSkeleton. Role floor: the record validator forbids a planner role, so this
review was performed under the reviewer taxonomy. **This is an explicit role-floor
deviation; the exact planner seat is not claimed as met** (parent instruction, Main).
Read-only. Only files written: this report and
`.ufo/evidence/round-12/ClaimSkeleton/witness_recount.py`. No installs, no commits, no
repo edits, no production or runner edits, no build/test runs. Tool installs: none.

## Verdict on the score deltas (honest)

| Axis | Pinned before | Honest delta this round | Reason |
|---|---|---|---|
| depth | 6 | **0** (stays 6) | Command D counts ledger lines in `tools/mutate-and-run.sh`; the runner is frozen by contract, and the bash-surface-census leg is already one of the six. A witness split is reanalysis, never a seventh gate. |
| calibration | 6 (adjudicated, K1) | **0** (stays 6) | C1 touches no SHONEN box. Calibration moves only through box changes, and the repeat-control gate is a capability row, not a box. |

Measurable counts only: capability rows and evidence counts (below), no scalar increments.

## Evidence (commands and outputs, observed this session)

1. **Depth command D** (`SCORECARD.md:72-73`):
   - `git show 284ab0f:tools/mutate-and-run.sh | …` → `recorded_cases=6 depth_score=6`
   - worktree file → `recorded_cases=6 depth_score=6`
   - Ledger lines `tools/mutate-and-run.sh:84-89` are the six matches.
2. **Calibration command C** (`SCORECARD.md:75`):
   - `284ab0f:SHONEN.md` → `boxes=4 checked=4 asserted=0 … bound=0` (the baseline value of 0 is correct).
   - `121696b:SHONEN.md` and HEAD worktree → `boxes=4 checked=0 asserted=4 … asserted_mark_upper_bound=8`.
   - **Counting defect:** command C gives 8 at the measured commit, but the pinned value is 6 (`SCORECARD.md:216-219`). The 6 comes from a manual box-3 exclusion that command C cannot express. The pinned value is an adjudicated number, not the output of the stated command. Report it as "pinned 6, command C upper bound 8, delta −2 by adjudication," not as a mechanical 6.
3. **Witness split recount** (`ClaimSkeleton/witness_recount.py`, exact-string match on
   `witness/declared.tsv` vs `witness/case-labels.tsv`):
   - D1 failing 16, declared-exact-hits 2, undeclared 14 · D3 16 / 3 / 13
   - D4 3/3/0 · D5 1/1/0 · D6 2 / 1 / 1 · D7 2/2/0 · D8 3/3/0 · D9 2/2/0 · D2, D10 0 failing, NONE declared
   - Result: killed-on-witness 8, accidental 0, survived 2. **The split reproduces mechanically** under exact-string matching; the "partly contaminated" disclosure still stands.
   - Labels were checked for truncation: 0 truncated labels across the 16/16/3/1/2/2/3/2 fields.
4. **Volatile-output probe** (`grep` over witness and coldread `.out` files): mutant outputs contain mktemp paths (`/tmp/kumitate-kimi-census-selftest-<random>`, `witness/D1.out:16`, `D3.out:18`, `D8.out:4`) and `/tmp/tmp.<random>` (`coldread/appendixB/B7.out:24-26`). The pristine control outputs are clean (`witness/control.out` 2 lines; `appendixB/control.out` 19 lines, no paths or timings).

## Findings, by severity

### High
- **H1 (counting). Calibration command C does not reproduce the pinned 6.** Its output is 8 at `121696b` and at HEAD. Exclusion of box 3 is manual adjudication. Fix to the rubric: either the scorecard states "pinned = command C − adjudicated exclusions, listed by box", or command C gains an explicit exclusion list with a reason per entry. Until then, any score citing command C alone is wrong by 2.
- **H2 (planned depth move is inconsistent with the contract).** `SCORECARD.md:271-272` plans "witness-scoped split on a bash leg recorded as a ledger case. Before: command D 6 → after 7." The round-12 contract says "existing 6 recorded gate legs unchanged; never count reanalysis as a seventh independent gate," and the runner is frozen. The honest delta is **0**. The planned +1 is unattainable without editing the runner, and the regex in command D would also count any witness line written into the runner's ledger comment (`^#   (js|bash)-… \d+/\d+`). Guard: keep witness lines out of that comment block, or narrow command D.
- **H3 (generalization). The witness split is one leg.** `witness-scoped-kill-verdict.md` and `corpus/README.md` F2 are "partly held" (one JS leg). PROVINCE (`PROVINCE.md:13-15`) requires two independent lanes before a pattern is general. The bash-surface-census split is a second leg of the *same* gate family in the same lane, so it cannot promote the pattern to general. State it as "held on two gates in one lane", not "general".

### Medium
- **M1 (C1 contract vs. evidence reality). Byte-identical stdout over-rejects volatile output.** The contract forbids normalization, so any suite that prints mktemp paths, durations, or dates fails `controls_mismatch` on a healthy suite. Fleet pattern P3 (`verification-patterns-fleet.md`) already requires an explicit volatile-scrub list. The C1 gate as specified cannot express one. Pristine JS and bash controls in the current evidence are clean, so this does not break C1 on those legs, but it will break on any future leg whose green output prints a temp path. Propose: C1 reports the mismatching byte ranges and classifies, rather than normalizing.
- **M2 (C1 statistical power). N=3 identical samples is weak.** Under an independent per-run pass/fail flake probability p, the probability that three runs show a mismatch is `1 − (1−p)^3 − p^3`:
  - p=0.50 → 0.75
  - p=0.25 → 0.56
  - p=0.10 → 0.27
  - p=0.05 → 0.14
  - p=0.01 → 0.03

  So "identical in 3 runs" is evidence of no observed mismatch, not determinism. The gate's wording must say so. The contract's "no flakiness cured or determinism proven" clause is the right claim; keep it.
- **M3 (one-case / overfit, witness).** Killed-on-witness is an *any-of* test. For D1 and D3, a generic label `green fixture → CLEAN exit 0, members=49 checked=49 chain=3 info=4` is declared and fails on almost any count-changing mutant. 14/16 (D1) and 13/16 (D3) failing labels are undeclared. The 8/0 split therefore shows presence of one declared witness, not that the declared assertion is the one that discriminates. Report the undeclared-failing count next to every split.
- **M4 (bash denominator).** The kagi surface-census count of 16 includes 2 `skip-case` rows that execute nothing on this host (`mutation-case-kagi-census.md` §0; U2). A "full-count" check (`SKILL.md:189-194`) passes on a skip-inflated count. Any bash witness split must state the executed (non-skip) denominator (14), not 16.
- **M5 (contamination, BashWitness).** `mutation-case-kagi-census.md` §1 already lists per-defect failing labels (B1–B10) and survivor analysis. BashWitness must declare witnesses from the pinned kagi source/selftest only, and must not open that note or `coldread/appendixB/*.out` before its declarations are hashed. Same contamination the js leg suffered (`witness-scoped-kill-verdict.md` E1).

### Low
- **L1.** Calibration pin 6 is box-level: box 3 is scope-bounded. Keep that bound in every citation.
- **L2.** F3 (`corpus/README.md`) still says "open"; a C1 tool that runs would move it to "partly held" only after a demonstrated run, per the capabilities rule (`SCORECARD.md:244`).

## Proposed independent counting commands (no score awarded by these)

- Depth (unchanged, must read 6): `git show 284ab0f:tools/mutate-and-run.sh | python3 -c 'import re,sys; print(len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)))'` → 6.
- Calibration, mechanical (upper bound, not the pin): command C at `121696b` → asserted_mark_upper_bound=8. Pin remains 6 by the K1 adjudication, which must be cited by box.
- Witness split (exact-string, reproducible): `python3 .ufo/evidence/round-12/ClaimSkeleton/witness_recount.py` → `TOTAL killed-on-witness=8 accidental=0 survived=2`.

## Exact owned paths
- `.ufo/waves/round-12/w1/ClaimSkeleton.md` (this report)
- `.ufo/evidence/round-12/ClaimSkeleton/witness_recount.py` (read-only recount, uses kaika evidence inputs)

## Residual risks / verification gaps
- The planner seat is not met; this is a reviewer-taxonomy review (role-floor deviation, reported to Main).
- The repeat-control gate (`tools/repeat-control.py`) did not exist when I read the tree; I did not exercise it. M1/M2 are from the contract and the evidence, not from a run.
- Non-author independence: nothing here is an independent promotion or admission. Any outside spot-check remains a separate debt.
- The volatile probe was a grep on saved outputs, not a repeated-run measurement of any suite.
- `grep` for `repeat` in the runner (from the kaika capability demo) was not re-run this session.
