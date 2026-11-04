# tameshi round 72 — plan (frozen before any claim data)

Lane: tameshi-shokunin. Base: `f20ba482c7441d4c75818e7cd8a3165fee7821a1`
(`= origin/master`, clean tree). Round shape: **one v1 wave, 12 seats**
(policy `scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack roles
reviewer/critic/mutation-tester/labrat = 4 = 33 %).

Saturation state at round start (SCORECARD.md, round-60 correction): scored
axes depth 10, calibration 8, freshness 9 — all at or above the saturation
line 8, window N = 2 exceeded (no capability admitted since round 50).
The stagnation nudge fires: this round is a capability/frontier move, and
C2 still works the lowest scored axis (calibration 8).

Two claims, distinct axes, causally separable.

## R72-C1 — capability: planning-time rekey-cost forecast (axis: operability, verdict-only)

**Before.** No instrument prices a planned monitored-file edit against the
cold-read ledger. The cost is discovered only after the edit, by the guard:
`git ls-tree -r f20ba48 tools/ | grep -c rekey-cost` → **0**; `REKEY_COST`
occurs 0 times in the tree at base. Round 52 lost admission to exactly this
debt (`.ufo/evidence/round-52`; `considerthese/2026-10-28.md` proposal 3).

**After.** `tools/rekey-cost.py` prints, from the committed ledger's own
input-keyed pins, the sections a planned edit set would drop and the re-read
debt they owe.

**Counter (frozen).**
```
python3 -I tools/rekey-cost.py --selftest
python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md --edit PROVINCE.md
```
Frozen outputs: selftest `REKEY_COST_SELFTEST: 8/8 pass` exit 0; the round's
plan `REKEY_COST sections=64 planned=2 at_risk=17 predicted_lost=17` exit 0.

**Frozen arms** — each is a counterfactual the guard itself was re-driven on
at base, in scratch clones, before this plan was written
(`.ufo/evidence/round-72/reh/`, five receipts; guard output pasted in
`reh/README.txt`):

| planned edit | forecast (frozen) | guard-measured counterfactual |
|---|---|---|
| `corpus/SOURCES.md` | 13 | `lost=13 RED` (`reh-sources-only.out`) |
| `PROVINCE.md` | 6 | `lost=6 RED` (`reh-province-only.out`) |
| `corpus/QUALITY.md` | 6 | `lost=6 RED` (`reh-quality-only.out`) |
| `SCORECARD.md` | 0 | `lost=0 ok` (`reh-scorecard-only.out`) |
| `tools/pointer-recheck.json` | 0 | structural: no section pins it |
| `PROVINCE.md` + `corpus/SOURCES.md` | 17 | `lost=17 RED` (`reh-province-sources.out`) |
| no planned path | `REKEY_COST error=no-planned-path`, exit 2 | — |

**Live check.** The forecast 17 must equal the guard's measured `lost=17` at
the C2 edit commit (`COLDREAD_PRECHECK … lost=17 RED`).

**Kill rule.** C1 fails if the selftest is not 8/8, if any arm above differs,
or if the forecast for the round's edit set differs from the guard's measured
loss at the C2 edit commit.

**Control that skips the claimed work.** An always-13 forecast fails the
2/0 arms; an always-0 forecast fails the 13/17 arms; a forecast that sums
per-arm losses instead of taking the union reports 19 for the round's edit
set and fails. The base tree cannot produce the forecast at all.

**Predicate (one sentence).** The tool exists in the tree, its selftest
passes 8/8, each of the seven arms above prints its frozen value, and the
forecast for this round's edit set equals the guard's measured loss at the
edit commit.

## R72-C2 — calibration (lowest scored axis, 8): the two routed defects paid, monitor restored

**Before.** (a) `corpus/SOURCES.md:177` (S302) cites "§4.3's numeric-address
form" for the sentence "Specifying a line number will match only that line in
the input" — the committed snapshot's heading is **§4.2 Selecting lines by
numbers** (`s302-sed.html` heading line 2246; sentence line 2255; the r71
non-author closure's routed defect 1). (b) `PROVINCE.md:57` says "the
seven-leg list now sits at `:85-91`" — at base, `tools/mutate-and-run.sh`
lines 85–91 carry the ledger header plus legs 1–4; the ten-leg ledger runs
**88–97** (leg 7 `js-round-gate` at 94, leg 10 `bash-drift-pins` at 97); the
lane's own red arm `province-r16-sevenleg-85-91` measures that drift on every
sweep. Paying both re-owes the cold-read rekey (forecast C1 = 17).

**After.** (a) S303 supersedes S302 with the §4.2 anchor (CORPUS.md rule 2;
the census exempts a same-URL/same-scope row whose `teaches` opens
`supersedes S302`); (b) a PROVINCE append corrects the span to `:88-94`
(seven-leg cut, leg 7 at 94) and `:88-97` (ten-leg ledger, leg 10 at 97); the
three new pointer rows measure `hit` at the tip; the guard's RED at the edit
commit is paid by the rekey so the monitor is green at both floors and in rev
mode.

**Counter (frozen).**
```
python3 -I tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json
python3 -I tools/pointer-recheck.py --repo . --manifest .ufo/evidence/round-72/control-manifest.json
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
python3 -I tools/coldread-precheck-portable.py --repo . --floor <BASE> --cand <tip>
```
Frozen outputs: `POINTER_RECHECK: rows=11 met=11 unexpected=0` exit 0 with the
three new rows `hit ok` (`province-r72-tenleg-88-97`,
`province-r72-sevenleg-cut-88-94`, `sources-s303-sed-4-2`); the **control
manifest** (same three rows, record/target revs = base) reads three `miss ok`
under `rows=3 met=3`; census exit 0; the guard red at the edit commit
(`lost=17 RED`) → `lost=0 ok` at both floors (round floor `4ed9ce1c` 64 → 64;
historic `8b0042bd` 46 → 64) and `--rev` `credited=64/64`.

**Kill rule.** C2 fails if any new row reads `miss` at the tip, if the control
manifest reads `hit`, if the census exits non-zero, if SOURCES row count does
not move 162 → 163, or if the monitor is RED at the tip.

**Control that skips the claimed work.** The same three rows scored at the
base revs: without the corrections the needles do not exist, so a
do-nothing round cannot reach the tip result (`rows=3 met=3` all `miss`).

**Predicate (one sentence).** At the tip, S303 carries the §4.2 label,
PROVINCE carries the corrected spans, the three new pointer rows read `hit`
while the same rows at base read `miss`, the census exits 0, and the
cold-read monitor reads 64/64 at both floors and in rev mode.

**Sourced claim.** S303 is a `SOURCES.md` row opened this round (live re-fetch
of the GNU sed manual on 2026-11-03, Gate quote in `corpus/lessons/round-72.md`).

## Shared no-harm

Monitored bytes base → tip: `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`,
`tools/registry.json`, `SHONEN.md`, `tools/mutate-and-run.sh` and the guarded
probe `tools/coldread-precheck-portable.py` must be blob-identical (diff-tree
check). `corpus/SOURCES.md` + `PROVINCE.md` are the only monitored edits and
both are rekeyed; `LOG.md`/`SCORECARD.md` appends are free (forecast 0, guard
`lost=0`). Additivity: `SOURCES.md` and the ledger are checked old-bytes-only
(insertions disclosed); the round's new files are in no section's input union.

## Round shape, seats, controls committed pre-data

- Wave `w1`: 12 seats — 3 executor, 2 scribe, 1 scout, 1 connector,
  1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 labrat.
- Planner seat: held by the L1 (validator rejects `planner`); the bounded
  planning data-walk rides the scout item.
- Residual call: none planned (≤4 allowed if a wave-2 attack item appears).
