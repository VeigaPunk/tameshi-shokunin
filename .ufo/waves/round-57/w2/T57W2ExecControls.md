# T57W2ExecControls — controls.sh + generators for the AMENDED C1 counter, run end to end

Staged under `.ufo/waves/round-57/w2/T57W2ExecControls/stage/.ufo/evidence/round-57/` (install at the same repo-relative paths; the generators must be in REV, `controls.sh` runs from the lane tree):
- `controls.sh` sha256 `9c7c10b1…7b6f`
- `control/gen_ledger.py` sha256 `60a9e2fc…ed0a`
- `control/gen_registry.py` sha256 `783322a6…d2` — UNCHANGED from wave 1 (copied so the stage is the whole control set); C2 controls are unchanged in intent.
Receipts: `T57W2ExecControls-receipts/` (`run2.stdout` + `run2/ctl-*.full` = full run; `run3-no-panel.stdout`; `RECIPE.txt`; `mk_pos_fixture.py`, `failing.json`; `stage.sha256`).

## Changes
1. ONE-GENERATION header statement kept verbatim (controls recomputed from lane git objects, no committed receipt read; `CTL_GENERATION_ERROR` guard unchanged).
2. `gen_ledger.py`: every new row carries `status_at_base`. New modes `bulkopen`, `quote-file` + `quote --commit SHA`. `skip` now writes `status_at_base=declined`. `fab`/`open`/`quote` copy the panel verdict when it is open/declined (a forger who copies the panel), else `open` (a fixed-at-base claim needs a BASE commit, which a forger lacks); the stats line prints `panel_agree`/`panel_present`.
3. Evidence search now uses the counter's whole-token key rule (the wave-1 generator used substring, so R52.2's key `bcba892` matched `bcba8924` and produced one `key_miss` in SKIP/OPEN/BULKOPEN; stats now read `unkeyed=0`). `blank_planned` now picks the newest `**Planned (round N)` paragraph by round number, ties later (the counter's rule; was: last in file).
4. `controls.sh`: new controls `CTL_BULKOPEN_c1`, `CTL_QUOTE_c1` (two commits in the clone: `chore: housekeeping notes` adds `corpus/ctl-quote-housekeeping.md` with `key: excerpt` lines and names no item id; the ledger commit then marks all 51 rows `fixed` with that commit and evidence in the new file). New arm check (not in wave 1): `phase_a NAME COUNTER DIR ARM_TERM` also requires the named term of `C1_R57_TERMS` to be > 0, else `CTL_ARM_MISMATCH` and the control counts as failed — a control that reaches `false` through the wrong arm no longer passes. Summary now `CONTROLS_A: m/10`, `CONTROLS_B: m/2`.

## Controls, pre-registered verdict, and what the dry run printed (run2, REV `47491e15`, BASE `5e356996`)
| CTL | construction | expected | printed (CTL / CTL_ARM) |
|---|---|---|---|
| CTL_0_c1 | BASE + instruments | false, arm `missing` | `rows=0/51 … panel=51/5 total=103 PASS=false`, `missing=51` |
| CTL_SKIP_c1 | 51 new rows `declined`, 45-char reason, `status_at_base=declined` | false, arm `panel_over` | `declined=51 panel=49/5 total=51 PASS=false`, `panel_over=44` (declined cap/fixed floor are non-binding: `declined_over=0`) |
| CTL_FAB_c1 | `fixed`, commit = HEAD, invented excerpt | false, arm `evidence_bad` | `fixed=51 agree=0/51 total=64 PASS=false`, `evidence_bad=51` |
| CTL_OPEN_c1 | `open`, newest Planned paragraph ids blanked (15 blanked) | false, arm `open_unplanned` | `open=51 agree=0/51 total=64 PASS=false`, `open_unplanned=51` |
| CTL_BULKOPEN_c1 | all `open`, `status_at_base=open`, new newest Planned paragraph names all 51 | false, arm `panel_over` | `rows=51/51 agree=51/51 panel=14/5 total=9 PASS=false`; `panel_over=9`, `open_unplanned=0`, nothing else fires |
| CTL_QUOTE_c1 | wave-1 forgery (unrelated message, quote file, all `fixed` with it) | false, arm `fixed_bad` | `fixed=51 agree=0/51 total=64 PASS=false`, `fixed_bad=51` |
| CTL_0_c2 | BASE + instruments | false | `gate_rows=0 held=0/0 total=11 PASS=false` |
| CTL_SKIP_c2 | rotated `expect.exit` | false | `held=0/3 total=7 PASS=false` |
| CTL_FAB_c2 | receipts never written | false | `held=1/3 mutants=1/3 total=4 PASS=false` |
| CTL_MUT_c2 | rows that never run the drift branch | false | `held=3/3 mutants=1/3 total=2 PASS=false` |
| CTL_POS_c1 | clone of REV | true | `rows=51/51 agree=51/51 panel=0/5 total=0 PASS=true` |
| CTL_POS_c2 | clone of REV | true | `gate_rows=3 held=3/3 mutants=3/3 total=0 PASS=true` |
Summary lines printed: `CONTROLS_A: 10/10 as pre-registered`, `CONTROLS_B: 2/2 as pre-registered`; 12 `CTL_MATCH`, 0 `CTL_MISMATCH`, 0 `CTL_ARM_MISMATCH`. Every `CTL` line of a scratch-clone revision prints `clone_rev=`; POS prints `rev=` (a lane revision). Full run ≈ 100–125 s.

## What is synthetic in the dry run (state it before relying on it)
- `panel.json` does not exist yet. The scratch assembly (lane at `06e9849` + working-tree `round-57/` instruments + working-tree ledger + a `**Planned (round 58)` paragraph naming the open ids, as `dry-c1.sh` does) carries a SYNTHETIC panel = each fixture row's `status_at_base`, and its sha256 is pinned in the CLONE's `c1/measure.py` `PANEL_SHA256` (the lane counter holds `PIN_PENDING…`; the lane file was not touched). CTL_SKIP/BULKOPEN panel numbers (44, 9) are therefore consequences of that synthetic panel (14 of 51 non-open; 2 of 51 declined), not of the real one.
- The passing ledger is NOT the L1's repaired one: the lane's working-tree ledger passes 31/51; the 20 rows the counter refuses (R51.1 R51.3 R51.6 R52.1 R52.2 R52.6 R53.6 R53.7 R53.9 R54.5–R54.10 R55.1 R55.3 R55.4 R55.6 R56.1) were replaced in the scratch copy by honest `declined` rows with keyed evidence (`mk_pos_fixture.py`). Counter relaxed in no way (only the pin constant in the clone). POS c1 therefore proves the plumbing and the arms, not the lane's content.
- C2 ran with the lane working-tree `c2/measure.py` (sha `7d49e3c4…`); no w2 stage of a C2 counter existed when I ran.

## Real-panel dependence the L1 must check
- CTL_SKIP and CTL_BULKOPEN fail only on the panel arm. With the real panel they fail the arm iff the panel has more than 5 ids whose verdict is not `declined` (SKIP) / not `open` (BULKOPEN). If the real panel is mostly `open` at base, BULKOPEN reads `panel_over<=0` and `CTL_ARM_MISMATCH` fires (the control would then need a different construction — it cannot be hidden: the arm check reports it).
- Negative sweep (`run3-no-panel.stdout`, the state in the lane today: no `panel.json`, `PANEL_SHA256` pending): `CTL_ARM_MISMATCH CTL_SKIP_c1 panel_over=0`, `CTL_ARM_MISMATCH CTL_BULKOPEN_c1 panel_over=0`, `CONTROLS_A: 8/10`, `CTL_MISMATCH CTL_POS_c1`, `CONTROLS_B: 1/2` — i.e. the controls cannot go green until the panel is committed AND pinned in the counter.
- The panel file must be committed in REV (controls clone REV; CTL_0 overlays `c1/` from REV so `panel.json` rides along).

## Findings
1. The lane's current `c1/measure.py --selftest` prints `C1_R57_SELFTEST: 11/45 pass` (run in a scratch copy of the working tree; first failures `good ledger passes`, `good verdict line fields`, … — the selftest fixtures predate the amendment: no `status_at_base`, no panel arg). Not my file; the counter's own gate fails until the L1 fixes it.
2. The `CTL_QUOTE_c1` forgery is refused only by the amended tie rule (`names_id` / item-text path): the commit is a real after-BASE ancestor of REV and the excerpt is absent at `routed_at` and at the commit's parent.
3. Wave-1's `unkeyed=1` finding is resolved by item 3 above (R52.2 hash keys), not by lane content.

Tools installed: none. Repo mutations: none (scratch clones only; scratch removed; nothing written under the lane except this seat's stage/receipts/report).
