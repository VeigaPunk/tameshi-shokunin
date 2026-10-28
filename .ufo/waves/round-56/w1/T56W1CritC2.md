# T56W1CritC2 — C2 falsification report (round 56, wave 1)

Seat: critic. Target: `C2_R56_PASS=true`. Instrument read: `.ufo/evidence/round-56/c2/measure.py` (sha `d17d36bd…` per freeze.json), gate `tools/receipt-revision-gate.py` (sha `1d80f8a6…`), surface `.ufo/evidence/round-56/control/frozen-surface.paths` (9 paths). All demonstrations ran in a `--shared` clone at `/fast/scratch/hyaku/tameshi-r56/T56W1CritC2/lane` (removed on exit); the lane repo and frozen instruments were never touched.

## Verdicts up front

1. **Content-identity exception is gameable — C2 can certify a revision whose contract, controls script, deciding script, and SCORECARD all differ from the revision the receipts name.** The declared surface omits every one of them. `C2_R56_PASS=true` is reachable on a tampered tree. **Defect (instrument-frozen, must route to a fix, not the wave's discretion).**
2. **The red-before receipt is genuinely the one the round-54 gate accepted** (slice == committed `controls-b.stdout` line 1, sha256 sidecar matches). The missing check was *any comparison of a receipt's `rev=` to the certified REV* — plus a **still-live second defect: `CONTROLS_B`/`CONTROLS_A` are shape-greps only; a failing fraction and `CTL_MISMATCH` lines pass gate-0 in round 54 *and* round 56.**
3. **Arm 5 genuinely depends on the gate.** Mutating `controls-b.stdout`'s `rev=` to a drifted commit fails `own=REFUSED` with `RECEIPT_REV_CONTENT_DRIFT` naming the drifted paths; an unresolvable rev fails `RECEIPT_REV_UNRESOLVABLE`; a rev-free file fails `RECEIPT_REV_ABSENT`. "Any two files" does not pass.
4. **Arm 6 accepts path-string mentions — and worse, its strongest cell is dead code.** `cells[8]=='mined'` reads the `opened` (date) column; `mined` is column 7. No SOURCES row can ever satisfy it, so `docs` caps at 3/4 and **`C2_R56_PASS=true` is unreachable regardless of content**. Kill-shot defect.

---

## Finding 0 (dominant): `C2_R56_PASS=true` is unreachable — arm-6 `mined` index bug

`measure.py` arm 6, note cell:

```python
for line in sources.splitlines():
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[8] == 'mined':
        mined.add(cells[0][1:])
```

SOURCES.md header (`corpus/SOURCES.md:10`): `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` — `status` (where `mined` lives) is **column 7**; column 8 is `opened`, always an ISO date. Evidence:

```
$ python3 - (scan, in scratch clone at freeze)
11-cell S rows: 140
mined at index: {7: 113}
cells[8]==mined (what arm6 reads): 0
```

So `mined` is always `∅`, `cited & mined` is always empty, the note cell never scores, `docs` ≤ 3/4, `total` ≥ 1 forever, and the counter can never print `C2_R56_PASS=true`. **Every other arm is moot until this is repaired.** Smallest safe correction: `cells[7] == 'mined'` (a one-character index fix in `measure.py`); the instrument is frozen, so this needs an amendment entry in `freeze.json`/contract, which is above my seat.

## Item 1 — the content-identity exception binds the declared surface, not the claim's inputs

Gate semantics (`check()`, positive/verdict role): if `rev != certified` and `--paths` given, accept iff `git diff --name-only rev certified -- <paths>` is empty. The exception is only as strong as the path list — and the frozen list omits the round's own claim-defining files.

Demonstration (scratch clone, real receipt shape):
- `c3e2ca9` = PIN-equivalent. Committed `controls-a.stdout` (role `control`, revs `{981c5e8b20a2, c3e2ca9f0207…}`) and `controls-b.stdout` (role `positive`, revs `{c3e2ca9…}`) at `R1=ee70141`.
- `R2=fc32858`: drifted **only** `SCORECARD.md` (standing row 8→4, the exact R55.3 falsification), `.ufo/evidence/round-56/contract.json` (gutted to `{"claims":{"C1":"gutted","C2":"gutted"}}`), `.ufo/evidence/round-56/controls.sh` (replaced by a stub printing `CONTROLS_A: 99/99`), `.ufo/evidence/round-56/deciding-run.sh` (tamper line appended).

Gate at `certified=R2`, the exact invocation `deciding-run.sh` gate-0b makes:

```
GATE OK .ufo/.../controls-a.stdout role=control revs=981c5e8b20a2,c3e2ca9f0207,c3e2ca9f020776b3d66c7af854fb82c834674fcf
GATE OK .ufo/.../controls-b.stdout role=positive revs=c3e2ca9f020776b3d66c7af854fb82c834674fcf
GATE: receipts=2 ok=2 refused=0 codes=none verdict=PASS   GATE_EXIT=0
```

The full counter at R2: `own=PASS`, `total=1` (only `docs` short). The binding was accepted for a revision whose **contract is gutted, whose receipt-producer is stubbed, whose deciding script is tampered, and whose SCORECARD row is falsified** — because none of those four is on `frozen-surface.paths`. A receipt naming a revision that differs from the certified one on an *unlisted* path is accepted even when that path is the claim itself.

Counter-proof (the mechanism works; the list is the hole): append each drifted path to `--paths` and every one flips the verdict —
`+SCORECARD.md → REFUSED RECEIPT_REV_CONTENT_DRIFT`; `+contract.json → REFUSED`; `+controls.sh → REFUSED`; `+deciding-run.sh → REFUSED`. Receipt: `T56W1CritC2-receipts/unlisted-path-exploit.txt`.

Also note what the list **does** include: `.ufo/evidence/round-56/c1|mmeasure.py` and `tools/receipt-revision-gate.py` — instruments — but not the contract that states the claim, the scripts that produce the receipts, the scorecard the claim writes, or `LOG.md`, `corpus/QUALITY.md`'s own consumers… (QUALITY/SOURCES/knowledge/registry *are* listed). The omission pattern is "claim products, not claim definitions." The contract's `cannot_see` covers a *copied* `rev=` token; it does not cover a certified revision whose claim-defining bytes differ from the receipt's named revision. **Fix direction:** add `contract.json`, `controls.sh`, `deciding-run.sh`, `SCORECARD.md`, `LOG.md`, `no-harm.sh`, `freeze.json`, `c2/red-before/*` to `frozen-surface.paths` — the file is frozen, so this is an amendment, not a wave edit.

## Item 2 — the red-before receipt is real; the missing check named exactly

Slice `red-before/round-54-ctl-pos-c1.stdout` is byte-identical to committed line 1 of `.ufo/evidence/round-54/control/controls-b.stdout` (`cmp` clean; sha256 sidecar `3310ff60…` matches). The whole `controls-b.stdout` (committed at `55649546`, re-stated at freeze `077d431e`) names `rev=077d431e6996` twice plus `rev=7df0e0426c98` — while the round certified `c2108100`. Verified: `077d431e` resolves and *is an ancestor* of `c2108100`; `7df0e0426c98` is **absent** from this repo (`Not a valid object name`) — the receipt cites a commit the lane never contained.

Round-54 `deciding-run.sh` (lines 49–58) checks each control receipt for: exists-as-blob at REV, non-empty, last-commit descends from FREEZE, and `CONTROLS_[AB]: N/M as pre-registered` shape. **Nothing in the file reads the `rev=` token inside the receipt or compares it to `REV`.** That is exactly the missing check the frozen gate now adds (gate-0b in round-56 `deciding-run.sh`).

Second, live defect: `grep -q '^CONTROLS_B: [0-9]*/[0-9]* as pre-registered'` accepts `CONTROLS_B: 2/3` — the file literally contains `CTL_MISMATCH CTL_POS_c1 expected=true actual=false` and `DECIDING_RUN_EXIT=0` was written anyway. **Round-56 `deciding-run.sh` still carries the same shape-only greps** (it greps the pattern, never the fraction, never `CTL_MISMATCH`). The new gate binds `rev=` but never validates the `CTL_*_PASS` verdicts the lines carry — a controls-b naming the right rev *and containing* `CTL_MISMATCH` would still pass gate-0. Refusal the gate reaches for the right reason (item per kill_rule), but the deciding-run admits a set that already announced its own mismatch. **Fix direction:** require the exact fraction `CONTROLS_B: 3/3` (or grep for `CTL_MISMATCH` and refuse) in `deciding-run.sh` — frozen file, amendment required.

## Item 3 — arm 5 (`own`) depends on the gate; mutations kill it

Arm 5 = `gate --certified REV --paths frozen-surface.paths --receipt controls-a:control --receipt controls-b:positive`, verdict must be `PASS`. At base it reads `own-receipts-missing` (files absent) — correct.

Mutations on the R1 receipt tree (each committed, counter re-run):

| Mutation to `controls-b.stdout` | arm5 result |
|---|---|
| `rev=c3e2ca9…` → `rev=981c5e8b20a2` (resolvable ancestor, drifts on listed paths) | `own=REFUSED`; gate names `RECEIPT_REV_CONTENT_DRIFT drift=c1/measure.py,c2/measure.py,receipt-revision-gate.py` — `C2_R56 total=2 PASS=false` |
| `rev=` → `rev=deadbeefdeadbeef` | `own=REFUSED`, code `RECEIPT_REV_UNRESOLVABLE` |
| file with no `rev=` at all | `RECEIPT_REV_ABSENT` |

"Any two files" fails: existence is not enough; the role semantics (`control` ⇒ all revs ancestors of certified; `positive` ⇒ exactly one rev, equal-or-content-identical) are load-bearing. **Liveness: good.** The companion weakness is Finding-item-1: a `controls-b` naming a rev that drifts *only off-surface* passes — the arm binds the list, not the claim.

## Item 4 — arm 6 (`docs`) accepts path strings; weakest 4/4 text; not enough

Cell-by-cell weakest text that still scores (demonstrated, `docs=3/4` printed — the 4th is the dead cell above):

- **QUALITY.md**: `<!-- tools/receipt-revision-gate.py RECEIPT_MISSING -->` — an HTML comment, a path and one code, no criterion text. Scores 1.
- **SKILL.md**: `<!-- receipt-revision-gate -->` appended at file tail, far outside `## Standing rules` (line 17). Scores 1 — the arm checks the whole file, not the section the contract names.
- **registry.json**: `{"name":"x","note":"tools/receipt-revision-gate.py RECEIPT_MISSING RECEIPT_EMPTY RECEIPT_REV_ABSENT"}` — a name-only row with 3 code strings, no argv, no expect. Scores 1.
- **knowledge note** (intended): header `source: S001\nverified-at: …\nrecheck: …` + `---` + empty body would score 1 — **but cannot**, because of the `cells[8]` bug. So the *only* cell demanding any semantic structure (a mined-source citation) is the unreachable one; the three scoring cells are pure substring checks.

Is it enough? **No, on two levels.** (a) Nothing checks that the QUALITY criterion's falsifier is a gate refusal code *on the real round-54 receipt*, or that SKILL's rule sits under `## Standing rules`, or that the registry row is a runnable gate row — the arm scores mention-density, not rule-stating. (b) Even the intended semantic cell is dead, so the arm cannot reach its denominator under any content. Fixable defects both: (i) `cells[7]`, (ii) scope the SKILL check to the `## Standing rules` section and require an actual criterion line (e.g. QUALITY row naming the gate + the real `RECEIPT_REV_CONTENT_DRIFT` on the round-54 receipt, per the contract target). Both need instrument amendment.

## Sweep summary (an attack that finds things still shows its sweep)

- Re-derived every "counter fact": precheck/monitor numbers from `before/c2.stdout`; `077d431e` resolves+ancestor; `7df0e0426c98` absent; `deciding-run.exit` = `DECIDING_RUN_EXIT=0`; slice==receipt (cmp + sidecar sha); CONTROLS_B fraction and CTL_MISMATCH lines read from the committed file.
- Full counter at `c3e2ca9`, `fc32858`, `5e248d5`, `ac1ad42`, `eedb8cd` — five distinct tree states, outputs cited.
- Gate invoked directly 7× (exploit PASS, 4× path-addition REFUSED, unresolvable REFUSED, absent REFUSED).
- `cells` column census over all 140 SOURCES rows.

## Impacted axes

Operability (the claim's own axis): the gate binds receipts to a declared surface that excludes the round's claim inputs — certified revision ≠ claim-relevant revision; deciding-run still admits partial/mismatched control sets. Calibration-adjacent: SCORECARD.md (the C1 restate surface) is off-surface, so receipt binding does not cover the row C1 certifies.

## Smallest safe corrections (all require instrument amendment; nothing a wave seat may edit)

1. `measure.py` arm 6: `cells[8]` → `cells[7]` — one index; without it the claim is unfalsifiable-by-success.
2. `frozen-surface.paths`: add `.ufo/evidence/round-56/contract.json`, `.ufo/evidence/round-56/controls.sh`, `.ufo/evidence/round-56/deciding-run.sh`, `.ufo/evidence/round-56/no-harm.sh`, `.ufo/evidence/round-56/freeze.json`, `SCORECARD.md`, `LOG.md` (the last two are claim products C1 writes; if deliberately excluded, the exclusion needs a stated reason, because the gate will then bind receipts across revisions where the scoreboard moved).
3. `deciding-run.sh`: grep the exact expected fractions (`CONTROLS_A: 7/7`, `CONTROLS_B: 2/2`) and refuse on `CTL_MISMATCH` anywhere in either receipt.
4. Arm-6 content checks (post-amendment): SKILL check scoped to `## Standing rules`; QUALITY check requiring the criterion row + `RECEIPT_REV_CONTENT_DRIFT` (the real red54 code), not any code.

## Tooling record

None installed. Stock `git`, `python3`, `bash`, `cmp`, `sha256sum` on the host; no installs needed or made.

## Receipts

- `T56W1CritC2-receipts/unlisted-path-exploit.txt` — exploit PASS + the four path-addition REFUSEDs.
- `T56W1CritC2-receipts/arm5-mutations.txt` — mutation runs (below).
- `T56W1CritC2-receipts/slice-identity.txt` — slice==receipt, sidecar, rev resolution.
- `T56W1CritC2-receipts/sources-cells.txt` — column census.
- Scratch clone `/fast/scratch/hyaku/tameshi-r56/T56W1CritC2` removed; commits `ee70141`, `fc32858`, `5e248d5`, `ac1ad42`, `eedb8cd` existed only there.
