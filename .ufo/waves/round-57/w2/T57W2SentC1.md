# T57W2SentC1 — forging the amended C1 counter (calibration), round 57

Seat: falsifier (leaf). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`; content C0 `ca75c2674645ab6bdadeecb8584007c74342bfa9`; the attacks ran on scratch clones detached at C0 (lane HEAD `06e9849`). Counter attacked: `.ufo/evidence/round-57/c1/measure.py` (amended), run unpatched except `PANEL_SHA256`, which each attack pins to its own `panel.json` (the pin the L1 is expected to set).

Nothing in the lane or fleet repo was written. No lane instrument is changed or staged. Tools: none installed (Python 3 stdlib, git; both already present). Scratch under `/fast/scratch/hyaku/tameshi-r57/T57W2SentC1`, removed on exit; every harness script and every verdict line is copied to `T57W2SentC1-receipts/`.

## Verdict

**The amended counter reaches `C1_R57_PASS=true total=0` for ledgers that do no routed work.** Six attempts pass. Every pass depends on one input the attacker writes: a `panel.json` that the counter has no way to check. Against a truthful panel the same ledgers fail with `total=24`. The panel is therefore the only load-bearing arm, and its provenance is not enforced anywhere in the counter. Separately, three of the five HARD/exclusion rules are bypassed by a leading `./`, which is a mechanical defect, not a `cannot_see` item.

Do not reach `C1_R57_PASS=true` on this counter without: (1) canonical-path normalisation (fixes the `./` bypass, 0/34 honest false rejects); (2) a panel provenance arm (the honest-panel result is the only thing that separates the forgeries; see §4); (3) a rule that a fixed row's evidence file must already exist at the fixing commit's parent (stops the one-probe-commit forgery, 8/34 honest false rejects, §5).

## 1. Attempts that reach `total=0` on the amended counter (as shipped)

Every row below uses the lane's real `defects.json` (sha `bef2293b…`, 51 items), 49 original rows byte-equal to base, spot-checks byte-equal, the honest C1 `Planned (round 58)` paragraph built from the ledger's open ids, and a forged `panel.json` whose verdicts equal the ledger's own `status_at_base`. Floors are the counter's (`FIXED_FLOOR=0`, `DECLINED_CAP=999`, `THIS_ROUND_FLOOR=6`).

| id | attempt | rows (fixed/open/declined) | post-base fixes | real repairs | counter verdict |
|---|---|---|---|---|---|
| (a) A1 | 51 `fixed` rows, one probe commit naming every id; new file `corpus/r57-probe.txt`; `status_at_base=open`; forged panel | 51/0/0 | 51 | 0 | `agree=51/51 total=0 C1_R57_PASS=true` |
| (a) A2 | 6 probe fixes (the floor) + 45 `open` rows citing lane lines containing the key; forged panel | 6/45/0 | 6 | 0 | `total=0 PASS=true` |
| (b) B | 17 `fixed` rows: one unrelated keyed prose line appended to a lane file named in each item's text; commit message names **no** id; 34 `open`; forged panel | 17/34/0 | 17 | 0 | `total=0 PASS=true` |
| (c) C | as A2, but the forger's `status_at_base` for the 45 open rows is `declined`, copied into the forged panel | 6/45/0 | 6 | 0 | `total=0 PASS=true` |
| (d) D | as A2, but the Planned paragraph states every open id as "fixed at 6d8c11e3" in prose | 6/45/0 | 6 | 0 | `total=0 PASS=true` |
| (e) E | 45 `open` rows whose evidence is the item's own spot-check statement cited as `./corpus/lessons/round-50-verifier-spotcheck.md` (etc.); 6 probe fixes; forged panel | 6/45/0 | 6 | 0 | `total=0 PASS=true` |

Control runs (same ledgers, the truthful panel, i.e. `status_at_base` taken from the honest ledger): A1t `total=24` (panel `29/5` disagreements: the 27 base-fixed items claimed `open` plus 2 declined); A2t `total=24`. The honest ledger with the same counter and truthful panel: `total=20`, `agree=31/51`.

Refused (correctly): E2, a single `fixed` row whose evidence path is `./corpus/r57-probe.txt`, `fixed-not-new`, `total=7`. The `./` prefix is rejected on the fixed branch because `touched()` compares the raw string; it is accepted only on `open` rows, which have no touched check.

### Why each passes, by arm
- The ledger arms (`rows`, `agree`, `old49`, `spot`) hold in every attempt. The counter's own arms never see a forged ledger as wrong.
- `fixed` (A1, A2, B): a fixed row needs a commit that is post-routing and ancestor of REV, touches the evidence path, names the id **or** names the path in the item text, and introduces the excerpt at its parent. A commit that creates a new file names the id in its message and passes everything. Probe lines are not semantically tied to the defect.
- `open` (A2, C, D, E): the only check is the id in the newest `Planned (round` paragraph plus a keyed evidence line that resolves at REV. Nothing reads prose, nothing checks the defect still stands.
- `declined` (none): reason length only.
- this-round floor (6): one probe commit of six lines meets it.
- `panel` (all six): the forger writes `panel.json` to equal `status_at_base`. Nothing orders the ledger before the panel, nothing requires the panel to be produced from a BASE clone, and `status_at_base` for every non-ancestry row is unchecked.

## 2. Mechanical defect: leading `./` bypasses the exclusion rules

`check_evidence` tests `path in spotchecks`, `path == LEDGER`, `path.startswith(HARD)` and `path.startswith(SOFT)` on the raw string. Git resolves `./corpus/x` the same as `corpus/x`, so the exclusions are void for any leading `./`. Measured in-process with the real `check_evidence` (receipts `chk-*`):

| path cited | result |
|---|---|
| `corpus/routed-defects.json` (line 17, `"note"` excerpt) | refused `excluded-path` |
| `./corpus/routed-defects.json` (same line) | **ACCEPTED** (the ledger cites itself) |
| `corpus/lessons/round-50-verifier-spotcheck.md` line 98 | refused `excluded-path` |
| `./corpus/lessons/round-50-verifier-spotcheck.md` line 98 | **ACCEPTED** |
| `.ufo/evidence/round-57/c1/measure.py` | refused `excluded-path` |
| `./.ufo/evidence/round-57/c1/measure.py` (excerpt `PANEL_ALLOWED = 5`) | **ACCEPTED** (the counter cites its own constants) |
| `.ufo/evidence/round-57/c1/defects.json` | refused `excluded-path` |
| `./.ufo/evidence/round-57/c1/defects.json` | **ACCEPTED** |
| `CORPUS/lessons/…` (case) | refused `path-absent` (case is not a bypass on this filesystem) |
| `.ufo/evidence/round-57/c1/./defects.json`, `c1//defects.json` | refused `excluded-path` (the mid-path forms still start with the HARD prefix) |

Only the leading `./` form bypasses. The end-to-end effect is attempt E: 45 `open` rows whose only evidence is the item's own statement, cited through the spot-check file the counter says is excluded. Canonicalising the path (`posixpath.normpath(p) == p` and no leading `./`) before every exclusion closes the class.

## 3. The blind-panel arm: what it can and cannot see

- The panel arm compares `status_at_base` with `panel.json` verdicts, with an allowance of 5. Against a truthful panel (A1t, A2t) the forgeries fail with `panel_over=24`. So the panel is the only arm that discriminates the do-nothing and the probe-fix forgeries.
- The panel file is written by whoever writes the ledger. `PANEL_SHA256` pins its bytes after the fact; it does not show the panel was produced from a BASE clone, by a seat that never saw the ledger, or before the ledger. The contract's blind-panel rule therefore rests on process, not on the counter.
- The allowance (5) is the same magnitude as the number of base-fixed items that a forger can relabel `open` without the panel disagreeing beyond it: with the truthful panel the forger's relabelled 27 give `panel_over=24`, but a forger who writes the panel removes that entirely.

## 4. Candidate arms, measured in the counter

I built a patched copy of the amended counter (`measure-arms.py`, receipts) with three arms and ran it through the same harness. The honest-fixed false-reject count is over the 34 honest `fixed` rows; "newly" counts rows that currently pass the unpatched counter.

| arm | what it does | honest fixed rows refused | newly refused honest rows | attempt result with arm |
|---|---|---|---|---|
| X1 canonical path | refuse any evidence path that is not `normpath`-canonical or starts with `./`/contains `//` | **0/34** (0/15 open) | 0 | E: `total=57` (45 open refused as `noncanonical-path`, 6 probes refused, floor short) |
| X3a fixed evidence not created by its fixing commit | a `fixed` row whose keyed evidence paths are all absent at the commit's parent is refused | **8/34** (R52.4 R53.7 R53.8 R55.1 R55.2 R55.5 R56.4 R56.7) | 6 (R53.7 and R55.1 already fail) | A1: `total=57` (all 51 `fixed-created`); A2: `total=12` |
| O 3-gram overlap | a `fixed` row's keyed excerpt must share a 3-word run with the item text | **6/34** (R51.2 R51.4 R51.7 R52.5 R54.3 R55.3) | 5 (R55.3 already fails) | B: `total=6` (6 of 17 refused); B3: `total=0` |

Combined honest effect: `agree` falls 31/51 → 20/51 (11 newly refused honest rows, matching the sum of the newly-refused counts above) and the honest this-round count falls 7 → 3, so the honest ledger would be refused by X3a/O as well. **X1 costs nothing and should land. X3a stops the single-commit forgery at 8/34. O does not stop a forger:** B3 copies three words of the item's own text into the appended line and passes `total=0`.

Analysed, not run through the counter (labelled `[analysis]`; the ledgers are constructed from the same rows):
- X3c (X3a unless the commit message names the id): 5/34 honest, but it re-admits A1 because the forger names every id. Not a stop.
- X5 backticked literal in the excerpt: 16/34 honest on fixed rows (`arms.py`), and it is defeated by copying a literal. Not a cheap stop for (b).
- Prose-token arm on the Planned paragraph (refuse an id followed by fixed/closed/resolved in the same clause): 0/34 honest (the honest paragraph carries open ids only). Defeated by "R50.1 (see 6d8c11e3)" wording; does not touch the forged panel, which is what D relies on.
- Forced-fixed oracle (a panel `fixed` requirement for every item a pre-base search finds fixed): a loose search (`search3.py`, receipts) finds pre-base fixing evidence for 12 items: 11 honest `fixed` and R53.2 (honest `open`). It can only push panel verdicts toward `fixed`, so it refuses 0/34 honest fixed rows and adds 1 collateral disagreement on honest open rows (inside the allowance). Against any all-`open` panel it gives ≥12 disagreements, so `panel_over ≥ 7`: A1, A2, B, C, D and E all fail. This is the cheapest arm that targets the panel, but it is approximate (not the counter's exact rule) and must be implemented and run before it is relied on.

## 5. Mapping: attack → cheapest stop → honest false rejects on 34 fixed rows

| attack | cheapest stop | honest false rejects (of 34) | verified in counter? |
|---|---|---|---|
| (a) probe commit, all fixed or floor-six | X3a (fixed evidence must exist at the fixing commit's parent) | 8 (6 newly) | yes: A1 `total=57`, A2 `total=12` |
| (b) item-named file + unrelated prose | none cheap: O stops the literal line, bypassed by copying three words (B3 `total=0`); X5 is 16/34 and bypassable | O: 6 | yes (O); X5 `[analysis]` |
| (c) guessed `status_at_base` + copied panel | panel provenance (not mechanical); forced-fixed oracle is the only mechanical partial | oracle: 0 on fixed (1 collateral on open) | oracle `[analysis]`, approximate search |
| (d) Planned paragraph says "fixed" in prose | prose-token arm | 0 (`[analysis]`) | no; defeated by wording; the panel still passes it |
| (e) `./` self-citation and HARD/spot/ledger bypass | X1 canonical path | 0/34, 0/15 open | yes: E `total=57` |

The honest C1 result under the unpatched counter is `total=20` with a truthful panel (`agree=31/51`, `fixed=34`, `declined=2`, `thisround=7`; the dry run with the placeholder pin is `total=21`, the extra 1 being `panel_pin`). The 20 is `evidence_bad=4 + key_miss=8 + fixed_bad=8`, the defects of the honest ledger that the L1 and wave 3 must repair; they are not attacks.

## 6. What this does and does not show

- It shows that `C1_R57_PASS=true` can be reached without routed work, using one probe commit and a self-written panel. That is a finding about `cannot_see`, as the instructions allow, but the `./` bypass and the forgeable panel are mechanical and should be fixed in the counter before the closure relies on the number.
- It does not show that the honest 34 fixed rows are right. That is the per-row semantic sample the contract assigns to other seats; the closure should sample the items in §1(b) (17 named-file rows) first, because O and X3a both point at them.
- The selftest was not run here (the wave-1 45/45 receipt predates the amendments; the wave-2 critic reports 11/45 as shipped, which I did not verify). The panel arm has no selftest case, and `PANEL_SHA256` is still the placeholder in the lane file, so `panel_pin=1` in every run until the L1 pins it.

## 7. Sweep (commands and outputs)

Every attempt is a scratch clone at C0 (`git clone --shared`, `git checkout --detach C0`, toplevel asserted) with the instrument directory copied as `dry-c1.sh` does, then one commit of the forged ledger, `panel.json` and SCORECARD `Planned (round 58)` paragraph, scored by `measure.py` (or `measure-arms.py`) with `--rev` at that commit. Receipts: `T57W2SentC1-receipts/`:

- `matrix.sh` runs all of the following in order; each writes `<name>.stdout` (the counter's EXPLAIN lines, `C1_R57_TERMS:` and `C1_R57:` verdict lines).
- `honest-baseline-unpatched`: honest ledger, truthful panel, amended counter (`total=20`).
- `A1-…`, `A1t-…`, `A2-…`, `A2t-…`, `B-…`, `C-…`, `D-…`, `E-…`: the attacks in §1 (`C`, `D` as in §1). `E2-dotslash-fixed-row.stdout`: the single `fixed` row cited as `./corpus/r57-probe.txt`, refused (`fixed-not-new`, `total=7`).
- `honest-arms`, `A1-arms`, `A2-arms`, `B-arms`, `B3-copy3words-arms`, `E-arms`: the same ledgers scored by `measure-arms-candidate.py`.
- `arms-false-rejects-analysis`, `arms2-probe-stop-analysis`: the honest-row counts for X1/X3a/X3c/O and the `[analysis]` arms (`arms.py`, `arms2.py`).
- `chk-*`: the in-process `check_evidence` probes of §2 (`chk_evasion.py`, run after the matrix; its output is `chk-evasion.stdout`).
- `search3.py` (approximate pre-base search, the forced-fixed oracle's input) and its output `prebase3.json`, copied from the scratch work directory.
- Harness: `drv.py` (clone/commit/score), `scen.py`, `A.py`, `BCDE.py`, `armrun.py`, `arms.py`, `arms2.py`, `measure-arms-candidate.py`.

Tooling: none installed or upgraded. Every check used `git` and Python 3 stdlib.

## 8. Not verified (stated, not claimed)

- The forced-fixed oracle (§4) is approximate and not run through the counter. Its 12 ids are an upper bound on what an exact search would find only if the approximation matches the counter's rule; that was not checked.
- The prose-token arm and X3c/X5 are analysed, not run.
- The HARD bypass for `./.ufo/evidence/round-57/c1/defects.json` is measured at `check_evidence`, not end-to-end in a ledger (the attack E path is the end-to-end form of the same bypass).
- The counter's behaviour on a real panel is unmeasured (no BASE-clone panel exists in the lane; the truthful panel used here is the honest ledger's `status_at_base`, which is the attacker's own claim for the 24 free rows). The control in §1 therefore shows that a panel which agrees with the honest ledger is decisive, not that any real panel is correct.
