# LabratControlGenuine — is the C1 do-nothing control genuine?

Seat: Labrat-style read-only probe (bounded hypothesis test), round 36 wave w1, policy v1.
Attacked: C1's do-nothing control — "monitor at the content commit prints 6" is a genuine
do-nothing only if the content commit `e423c41` actually contains ALL round-36 record edits
(LOG/SCORECARD/lesson/SOURCES/v2/contract) and no record edit landed in a later commit.

## Revisions under test

- `796e08b` — round-35 tip (C1 before base, score 6 / 60-64)
- `e423c41` — round-36 content commit (the control measurement commit)
- `b455001` — round-36 cold-read refresh commit
- `d9c496b` — round-36 receipts commit = lane tip (`git rev-parse HEAD`)

## Commands run (all at lane root /home/vgpnk/Projects/shokunin/tameshi-shokunin)

```
git log --oneline -20                                          # commit topology
git diff --stat 796e08b e423c41                                # control vs r35 tip
git diff --stat e423c41 b455001                                # refresh delta
git diff --stat b455001 d9c496b                                # receipts delta
git log --oneline e423c41..HEAD                                # what landed after control
git diff --name-only e423c41 HEAD -- LOG.md SCORECARD.md corpus/ \
    .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-36/contract.json
git diff --name-only 796e08b e423c41 -- .ufo/evidence/round-21/coldread/
git status --porcelain -- LOG.md SCORECARD.md corpus/ .ufo/evidence/round-36/ \
    .ufo/evidence/round-21/coldread/
git show e423c41 -- LOG.md | SCORECARD.md | corpus/SOURCES.md | corpus/QUALITY.md
git diff -w --stat e423c41 b455001 -- .ufo/evidence/round-21/coldread/ledger.json
git diff -w e423c41 b455001 -- .ufo/evidence/round-21/coldread/ledger.json | grep …
python3 - <<…                                                  # ledger entry count at e423c41 vs b455001
grep -nE 'calibration_restraint_score|sections_covered' monitor receipts
grep -nE "--rev|git.*show|blob" .ufo/evidence/round-{21,18}/…/measure.py
git log --oneline -3 -- .ufo/evidence/round-21/coldread/measure.py
git diff --name-only 796e08b HEAD -- .ufo/evidence/round-21/coldread/measure.py
```

## Findings (observed)

1. **All six record-edit classes are inside the content commit.** `git diff --stat 796e08b
   e423c41` (16 files, +5506/−1):
   - `LOG.md` +46 — dead-pointer correction for the r35 `ResidualSentinelClosure.md`
     citation (append-only, names the five real residual reports) + round-36 entry.
   - `SCORECARD.md` +47 — round-36 block, C1/C2 table rows, numeric axes 6→8 / 9→9.
   - `corpus/lessons/round-36.md` +85 (new lesson).
   - `corpus/SOURCES.md` +3/−1 — S103 row + Next-unused-id S103→S104.
   - `corpus/QUALITY.md` +12 — criterion 72 (dead-pointer falsifier).
   - `.ufo/evidence/round-36/c1/c1-measure-v2.py` +559 (frozen v2 counter),
     `.ufo/evidence/round-36/contract.json` +43 (frozen contract).
   - Non-record companions confined to the same commit: S103 snapshot
     (`src/s103-git-hash-object.html`, +1709) and wave w1/w2
     dispatch/spec/validate files (+2091) — wave-prep artifacts, not record edits.
   - `.ufo/evidence/round-21/coldread/` (ledger + monitor) **not touched** in e423c41 —
     the refresh is absent from the control tree, exactly as the contract requires.

2. **Zero record edits after the control commit.** `git log e423c41..HEAD` =
   b455001 + d9c496b only, and `git diff --name-only e423c41 HEAD` restricted to
   LOG/SCORECARD/corpus/v2/contract returns **empty**. `d9c496b` is HEAD, so no
   further commits exist. `git status --porcelain` on all record/evidence paths is
   clean — the checked-out worktree matches the tip.
   - e423c41→b455001: only `ledger.json` (4 appended entries, see below) + the
     round-36 `coldread/` refresh artifacts (specs, receipts, 4 trace files).
   - b455001→d9c496b: only `after/` + `control/` measurement receipts (22 files,
     insertions-only).

3. **The control is a real do-nothing measurement of the content-commit tree.**
   The round-18 implementation (`measure.py` docstring + `blob()`/`git show REV:path`,
   `rev-parse --verify --end-of-options`) reads every input — ledger, SKILL/SHONEN,
   SOURCES, input files — **at the explicit `--rev` commit**, never the live worktree.
   So `monitor-at-e423c41b.stdout` = 6 / 60-64 reflects the content commit's tree,
   which contains every record edit and no refresh. Receipt scores:
   before `796e08b`=6/60-64, control `e423c41`=6/60-64, after `b455001`=8/64-64;
   all three exit 0. `measure.py` itself last changed at `370f2df` (round 21) —
   untouched in round 36 (kill-rule consistent).

4. **Refresh delta is clean** (supports the control's interpretation):
   `git diff -w e423c41 b455001` on `ledger.json` = **118 insertions, 0 deletions**
   — the huge raw stat (+40709/−40186) is wholesale re-indentation; `-w` suppresses
   every whitespace-only pair, and no content line was removed or altered. Parsed
   JSON: 493 → 497 entries; the 4 new entries name the four r35-drifted headings
   (Mutation-sweep recipe, Restore discipline, ### The map, ### Where to enter)
   and all carry `read_rev = e423c41ba253357ab8c8513f0376dad9d38ab248` — the reads
   are anchored at the very commit the control measures.

## Minor observation (does not invalidate the control)

- LOG.md's round-36 entry cites the control receipt as
  `.ufo/evidence/round-36/control/monitor-at-content-commit.*` while the committed
  file is `monitor-at-e423c41b.*` — a name-level slip inside the record edit
  (criterion-72-adjacent: the glob resolves to nothing literally). The receipt
  itself exists under the rev-pinned name and matches the claim.

## Verdict

**CONTROL GENUINE — no record edit escaped the content commit.** Every enumerated
record file changed in `796e08b→e423c41` and none changed in `e423c41..HEAD`; the
monitor's printed 6 at `e423c41` is measured against a tree holding all records and
no ledger refresh. The do-nothing control for C1 stands.
