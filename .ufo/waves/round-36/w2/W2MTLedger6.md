# W2MTLedger6 — cold-read ledger aggregation probe (C1 calibration)

Seat: mutation-tester, wave 2, round 36. Leaf seat (no subagents). All scratch work under
`/fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger6/`; the only lane path created is this report.

## What was attacked

C1 (calibration): "cold-read monitor refresh restores credit 6 -> 8". The probe targets the
monitor's **per-section aggregation** — the place where a second (bad) entry for an already
credited heading could either (a) veto the section or (b) leave it credited.

Target section: `### Where to enter — four readers`, `start 1436`, section-content
`sha256 441858d2ff55a2dc1bbf36edc3844dcab9b7bba6ddad373df7cc9a6d13aae094` — one of the four
round-35-drifted headings re-anchored at `b455001`.

Ledger state at the measured rev (pristine `fbb01cf`, 497 entries; ledger blob
`b0522d3ca6e1ee6e06935a0265e3cd0c392c4d69`, worktree sha256
`29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`):

| index | class | verdict | read_rev | role at rev |
|---|---|---|---|---|
| 148 | instruction | gap-minor | a9c94c5c | stale input (`input-drift:corpus/knowledge/closeout-r11.md`), does **not** credit |
| 496 | record | gap-minor | e423c41b | the round-36 refresh entry; **carries the section** |

Mutant: append a 498th entry that is a byte-shape copy of entry 496 (`start 1436`, same section
sha, record/gap-minor, `commands_executed_count 1`, `blocking_gaps 0`, `wrong_expectations 0`,
same round-36 trace receipt) with one **deliberately wrong input sha**:
`corpus/README.md -> 765b322483436ddab135285020832267e6813ca3ddc3e2e6405c05fa6aa90628`
(true bytes `7c0fe513ac1999d1c489d0c0e6b0aa57c648c8b2855d0e4a28fd617dcbc2619f`). The path is not
in the trace receipt, so the input gate is the only gate it can trip.

## Detector (unchanged, frozen bytes)

`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo <SCRATCH_LANE> --rev <REV> --explain`

* selector `measure.py` sha256 `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`
* delegated implementation `round-18/measure.py` sha256
  `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`
* contract pins re-verified this seat: v2 counter `9eb8944c...`, `tools/tally-audit-v3.py`
  `6188db16...`, `tools/mutate-and-run.sh` `a7d3f2dd...` — all match.

No `--ledger-file` / `--ledger-rev` / `--inputs-overlay` used (selector rejects them; runs report
`overrides_used: false`, `trace_gate: strict`, `ledger_committed: true`).

Scratch lane: `git clone /home/vgpnk/Projects/shokunin/tameshi-shokunin
/fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger6/lane` (58M, HEAD `fbb01cf`). All commits are in
this disposable clone only.

## Runs (exact commands and revisions)

Baseline — pristine tip:

```
python3 .../round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r36-seats/W2MTLedger6/lane \
  --rev fbb01cf46f8437fd1264c1a3acc053c882fa2164 --explain > baseline.json
```

Arm A — fifth entry, wrong sha (ledger worktree sha256 `4591d4ac...`, blob `601f43a1...`):

```
git commit -m "scratch mutant A: fifth round-36-style entry for section 1436 with wrong corpus/README.md sha"  # 3baaec96
python3 .../measure.py --repo .../lane --rev 3baaec96ec32901553bc4c8e46dc9f099d682af0 --explain > mutantA.json
```

Arm B — bad entry alone (good entries 148+496 removed; ledger sha256 `27b35362...`, blob `9a205c40...`):

```
git commit -m "scratch mutant B: bad entry alone for section 1436 (good twins removed)"  # b49461d7
python3 .../measure.py --repo .../lane --rev b49461d74f483963c3b5be59474365e3a9360a29 --explain > mutantB.json
```

Arm C — attribution control: same fifth entry with the **correct** README sha (ledger sha256
`fe0bad3a...`):

```
git commit -m "scratch mutant C: same fifth entry with the correct corpus/README.md sha"  # deb3f19e
python3 .../measure.py --repo .../lane --rev deb3f19ecd186839666a4368cfcd607d83289f7d --explain > mutantC.json
```

All four exits `0`, stderr empty.

## Actual outputs

| run | rev | score | covered | section 1436 `credited` / `vetoed` / `reason` | section `reasons` (explain) | reasons histogram |
|---|---|---|---|---|---|---|
| baseline | fbb01cf | **8** | 64/64 | true / false / `credited` | `credited`, `input-drift:corpus/knowledge/closeout-r11.md` | `{credited: 64}` |
| A (bad fifth, wrong sha) | 3baaec96 | **8** | 64/64 | true / false / `credited` | `credited`, `input-drift:corpus/README.md`, `input-drift:corpus/knowledge/closeout-r11.md` | `{credited: 64}` |
| B (bad alone) | b49461d7 | **6** | 63/64 | false / **false** / `input-drift:corpus/README.md` | `input-drift:corpus/README.md` | `{credited: 63, input-drift:corpus/README.md: 1}` |
| C (same fifth, correct sha) | deb3f19e | **8** | 64/64 | true / false / `credited` | `credited`, `input-drift:corpus/knowledge/closeout-r11.md` | `{credited: 64}` |

A vs C differ only in one input digest; A gains exactly `input-drift:corpus/README.md`, so the
appended entry **was parsed and evaluated**, and the wrong sha is its sole defect (it credits in C,
so class/commands/trace gates are all satisfied).

Aggregation semantics confirmed in source (`round-18/measure.py`): `covered = credited > 0 and not
vetoes`; a veto needs `entry_failure(entry) is not None` **and** `not entry_is_stale(...)`. An
input-drift entry is neither failing (verdict/gaps shape is clean) nor non-stale, so it is excluded
twice. Section 1436's pre-existing stale twin (148) already demonstrated the first half at baseline.

## Verdict line

**Mutant SURVIVED (no behavioral delta to the invariant) — expected semantics CONFIRMED: the
appended fifth entry with a deliberately wrong input sha cannot veto and cannot strip credit; the
section stays credited via the good round-36 entry, monitor section reason `credited`,
`vetoed: false`, score stays 8 and coverage stays 64/64. Bad-entry-alone control: section
uncovered with reason `input-drift:corpus/README.md` and `vetoed: false` — loss of credit, never a
veto. C1's before/control/after calibration numbers are not disturbed by a bad fifth entry.**

Not a coverage finding against the contract: the observed non-credit-without-veto is the documented
fail-closed design, not a defect; no contract or counter change is implied.

## Restoration evidence

Lane was never written: ledger sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`
identical before and after all runs; lane HEAD `fbb01cf46f8437fd1264c1a3acc053c882fa2164`
unchanged; lane `git status --porcelain` shows only the pre-existing untracked
`.ufo/waves/round-36/w1/` and `.ufo/waves/round-36/w2/` (identical before and after). All mutations
live in three commits of the disposable clone (`3baaec96`, `b49461d7`, `deb3f19e`); no frozen
artifact was edited (hashes above). No tools installed; no `pacman`; runs used system `git` and
`python3`.
