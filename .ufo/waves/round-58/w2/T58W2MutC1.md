# T58W2MutC1 — C1 counter mutations 2 (calibration)

Seat: mutation tester, wave 2 of round 58. Lane `tameshi-shokunin`, C0 = `8063d0a551fc5b3cb5a2d397da7353af53444534`.
Target: scratch copy of `.ufo/evidence/round-58/c1/measure.py` (pristine sha256 `9b7c01673912ec2a9313b98109a62216f0c5a8f9b64c1b459be141d118fb58d6`, byte-identical to the lane file). The lane repo was never written to; the counter was pointed at it read-only.

## Detectors and baseline

- Real: `python3 <copy> --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --explain` — exit 0 iff `total==0`.
- Selftest: `python3 <copy> --selftest --work $S/tmp`.

Pristine baseline: real run exit 0, `rows=51/51 agree=51/51 old49=ok panel=4/5 spot=ok total=0 C1_R58_PASS=true`; selftest exit 0, `C1_R58_SELFTEST: 110/110 pass`. Both green before mutating — no verdict below is inconclusive.

## Mutants (one single edit each)

| # | Site | Edit | Real lane | Selftest | Overall |
|---|------|------|-----------|----------|---------|
| M1 | L423 old49 comparison | `if len(seen) != 1 or seen[0] != was:` → `... and ...` | SURVIVED (`total=0`, `old49=ok`) | KILLED (exit 1: `rewritten old row counted (old49 arm) FAIL`, then `IndexError` on the deleted-row case) | killed |
| M2 | L121 Planned regex | `\bR5[0-6]\.\d+\b` → `\bR5[0-5]\.\d+\b` | KILLED (exit 1: `open-unplanned R56.1`, `open-unplanned R56.2`, `total=2`) | SURVIVED (`110/110 pass`) | killed |
| M3 | L115 disagreement budget | `PANEL_ALLOWED = 5` → `6` | SURVIVED (`panel=4/6`, `total=0`) | KILLED (exit 1, `107/110`: `good verdict line fields FAIL`, `panel agrees: panel=0/5, pass FAIL`, `cli good exits 0, verdict is last line FAIL`) | killed |
| M4 | L114 provenance digest pin | `PANEL_SHA256` first hex char `e`→`f` | KILLED (exit 1: `panel_pin=1` + `fixed_bad=11`, `total=12`, `C1_R58_PASS=false`) | SURVIVED (`110/110 pass`) | killed |

All four mutants are killed overall; no mutant survived both detectors. Raw outputs: `T58W2MutC1-receipts/m{1,2,3,4}-{real,selftest}.out`; diffs summarised in `T58W2MutC1-receipts/diffs.txt`; mutant file sha256s in the JSON.

## Findings (coverage, not contract changes)

1. **The two detectors are complementary, neither subsumes the other.** Killed-by matrices are disjoint: M1 and M3 are caught only by the selftest; M2 and M4 only by the real-lane run. The counter run alone against the clean installed ledger would admit the old49-weakening (M1) and the budget-widening (M3); the selftest alone would admit the planned-range narrowing (M2) and any constant-pin drift (M4). Keep running both.
2. **Pin constants are invisible to the selftest by construction.** The selftest asserts only the 64-hex shape of `PANEL_SHA256`/`DEFECTS_SHA256`, never their values; the real lane is the only detector for pin drift.
3. **M1's kill is partly a crash, not an assertion.** The deleted-old-row case reaches `seen[0]` on an empty list under `and` → uncaught `IndexError`, exit 1. Detection holds; the failure mode matters when reading selftest logs.
4. **A wrong panel pin costs more than the panel arm.** The pin miss empties `pcommits`, so 11 fixed rows relying on the A8 panel commit-tie fire `fixed-not-new` too (`total=12` at C0). The pin also protects fixed-row adjudication.

## Restoration and hygiene

- Working copy restored to pristine after every mutant; final sha256 `9b7c0167…` equals the lane file and the clone blob.
- Lane repo: only read-only `git show`/`rev-parse` against it; HEAD still C0; the 7 porcelain entries present at check time are orchestrator w2-dispatch artifacts (`build-spec-w2.py`, `w2-dispatch.json`, `w2.ready*`, `w2/`, `spec-w2.json`, `integrate/`), none written by this seat. Scratch clone clean.
- Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2MutC1` deleted before yield (see JSON `scratch_cleanup`). No `/tmp` use over 50 MB; selftest fixture lived under the scratch `tmp/`.
