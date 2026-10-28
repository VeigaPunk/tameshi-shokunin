# T56W1ExecC1Counter — C1 counter liveness

## Evidence

- Ran the frozen counter at base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` with an initially empty work directory and `--explain`. The observed result exactly matches `.ufo/evidence/round-56/before/c1.stdout`:
  - `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`
  - Explanation arms: precheck `lost=18 RED`; monitor `46/6/false`; rekey dirs `[]`; readers `0/18`; restate `row_score=8`, row commit `d33053f7552d`, score at row `6`.
- Cloned the lane with `git clone --shared` into `/fast/scratch/hyaku/tameshi-r56/T56W1ExecC1Counter/clone`, checked out frozen revision `c3e2ca9f020776b3d66c7af854fb82c834674fcf`, and asserted the clone's toplevel was the clone directory before committing the fixture. No lane or frozen instrument files were edited.
- In the clone, appended a synthetic ledger entry whose trace is under `rekey-r56-c3e2ca9f0207` and whose `inputs` pins `SCORECARD.md`; added the matching trace file and committed the fixture. Counter output at fixture revision `cbb82f9fa93c`:
  - `EXPLAIN arm3-rekey dirs=['rekey-r56-c3e2ca9f0207'] c0=c3e2ca9f0207`
  - `C1_R56: rev=cbb82f9fa93c c0=c3e2ca9f0207 credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=1 restate=8 total=6 C1_R56_PASS=false`

## Arm assessment

| Arm | Mutation / observed before → after | Verdict field change | Finding |
|---|---|---|---|
| 1 precheck | Base run only; `lost=18` | `credited=46 lost=18` | Confirmed base behavior against the supplied before receipt. No isolated passing-to-failing mutation attempted. |
| 2 monitor | Base run only: `monitor=6/46` | unchanged in fixture | Confirmed base behavior; no passing-to-failing mutation attempted. |
| 3 rekey | The synthetic fixture created a rekey directory and one non-qualifying bound ledger record, not a valid 18-entry baseline. `rekeyed=0/18` before/after remains 0. | No tally decrement demonstrated. | **Liveness not demonstrated.** A meaningful arm-3 drop requires first building all 18 qualifying entries; base/freeze have none. |
| 4 readers | No committed complete reader set existed; `readers=0/18`. | No isolated change demonstrated. | **Liveness not demonstrated.** A wrong-SHA report can only be shown to drop a reader from a valid passing set; that set is absent from base/freeze. |
| 5 stable | Added a bound entry with `inputs.SCORECARD.md` in a committed scratch clone. Base `unstable=0 total=5`; after synthetic trigger `unstable=1 total=6`. | `unstable=0` → `unstable=1`; `total=5` → `total=6`. | **Confirmed live** once a rekey directory resolves. The trigger entry need not qualify for rekey credit: the stability scan examines every bound entry. |
| 6 restate | Base/freeze row already asserts 8 while its measured commit reads 6. | `restate=8`; `total=5` | **No isolated mutation demonstrated.** A wrong-score mutation atop an already-wrong baseline cannot demonstrate the arm's independent liveness. |

## Limitation / risk

Only arm 5 was actively triggered beyond the supplied base run. The requested independent arm-3, arm-4, and arm-6 mutation deltas need a passing C1 fixture (64 credited sections, 18 valid re-key bindings, 18 correctly bound reader reports, and a valid standing row) as their starting point. Constructing such a tree entails the same full 18-heading re-key/reader work that the later content wave is intended to create; the frozen counter does not provide a fixture builder. Accordingly, I do not claim those arms were proven live. The current `rekeyed=0/18` outcome in the synthetic fixture is not evidence of an arm-3 mutation delta.

No tools were installed or updated. No build, test, lint, formatter, or validation command was run.
