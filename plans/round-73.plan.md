# tameshi round 73 — plan (frozen before any claim data)

Lane: tameshi-shokunin. Base: `a3dd35742eee608d1205843dacebc461b4242b9e`
(`= origin/master`, clean tree — the round-72 non-author verifier spot-check
commit). Round shape: **one v1 wave, 13 seats** (policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack seats by the policy's
named set = 2 reviewer + 1 critic + 1 mutation-tester = 4 = 30.8 %; `labrat` is
a frozen-topology seat the validator rejects, so no labrat item exists — the
round-72 defect this plan pays was a plan that declared one anyway).

Saturation state at round start (SCORECARD.md, round-60 correction; measured
this round by `tools/rekey-cost.py` and the axes table): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. A
capability entered the table at round 72 (`rekey-cost forecast`), so the
stagnation window (N = 2) is **not** exceeded and the nudge does not fire.
C1 still works the lowest scored numeric axis (calibration 8).

Two claims, distinct axes, causally separable: C1 lands only under `tools/`
and its manifest; C2 lands only inside `tools/rekey-cost.py`. Neither needs
the other's files, counters or commits.

## R73-C1 — calibration (lowest scored axis, 8; capability acquisition; sourced on the re-opened S066)

**Before.** The round-72 non-author closure (`corpus/lessons/round-72-verifier-spotcheck.md`)
routed two execution-claim defects that nothing in the lane measures: the
round report's shape line (`:56` at `3664a6d3`) prints "12 seats, 11 reports"
while 12 seat reports are committed, and the frozen plan
(`plans/round-72.plan.md:132-133` at `dfb534ca`) declares `1 labrat` while the
executed wave ran `revenger`. No instrument compares a round record's
execution claims with the committed wave artifacts:
`git ls-tree -r a3dd3574 tools/ | grep -c wave-reconcile` → **0**;
`git grep -c WAVE_RECONCILE a3dd3574` → 0.

**After.** `tools/wave-reconcile.py` + `tools/wave-reconcile.json` (schema
`tameshi-wave-reconcile-v1`) compares a record's execution claims with the
committed wave artifacts. Four row kinds:

| kind | the claim | the artifact re-derivation |
|---|---|---|
| `seats` | a record span prints the wave's seat count | `len(results[])`, `results.seats` |
| `seat_reports` | a record span prints the count of seat reports | the `*.md` files at the top of the wave dir at the artifact rev |
| `roles` | a record span declares a role multiset (spec items, or `N role` tokens in text) | the `agent` multiset in `results[]` |
| `attack_share` | — | named attack roles / total seats ≥ the declared floor |

Binding rules: the record span must be a byte substring of the record at the
record rev; the printed integer must occur in the span as a delimited token;
for `text-tokens` role declarations every `N role` pair must occur in the
span (an absent declaration is a setup error, never a silent pass); artifacts
are read from git objects at the artifact rev, never from a worktree; a
row-level `root` of `fleet` resolves against the `--extra-root` named path
(the fleet repo holds the round reports — the `receipt-exists.py`
`--extra-root` precedent). Artifact bytes decode as UTF-8; a UTF-8 BOM is
refused as setup exit 2 naming the artifact (S066 §8.1: a BOM is not part of
a JSON text and is never silently stripped). `expect: meet|drift`, so a
standing red arm MEASURES the drift on every sweep. Zero-row manifest,
unresolvable rev, undecodable bytes: setup exit 2 before any row effect.

Standing manifest: **6 rows** over the committed round-72 wave — 4 green
(`results` seats 12; the report's "12 seats"; the spec's roles = the results'
roles; attack share 3/12 = 25 % ≥ floor 25 %) and **2 red arms** (the
report's "11 reports" vs 12 committed seat reports; the plan's role set incl.
`labrat` vs the results' incl. `revenger`).

**Counter (frozen).**
```
python3 -I -X utf8 tools/wave-reconcile.py --selftest
python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
```
Frozen outputs: selftest `WAVE_RECONCILE_SELFTEST: 12/12 pass` exit 0; the
standing sweep `WAVE_RECONCILE: rows=6 met=6 unexpected=0` exit 0 with both
red arms reading `expect=drift measured=drift ok`.

**Frozen selftest arms** (12; hermetic, fixture bytes through the same decode
and row engine, TMPDIR-honouring, deleted in `finally`): seats-meet,
seats-mismatch-caught, seat_reports-drift-measured, roles-spec-meet,
roles-text-drift-measured, attack-below-floor-caught, attack-at-floor-meet,
bom-refused, invalid-utf8-refused, zero-rows-refused,
unresolvable-rev-refused, declaration-absent-refused.

**Kill rule.** C1 fails if the selftest is not 12/12, if any standing row
reads other than its expected status, or if any control below reaches
`unexpected=0`.

**Control that skips the claimed work** (built and scored before this freeze,
receipts `.ufo/evidence/round-73/reh/`): (i) an always-`meet` reconciler —
over a manifest carrying a declared red arm it measures `unexpected=1`, exit
1; (ii) `measured := printed` — identical failure; (iii) a population read
from the manifest's own declared count — identical failure. The base tree
cannot print the sweep line at all (`--manifest` is usage exit 2).

**Predicate (one sentence).** The tool exists in the tree, its hermetic
selftest passes 12/12, and the committed six-row manifest reads
`rows=6 met=6 unexpected=0` exit 0 with both r72-closure red arms measured as
drift on every sweep.

## R73-C2 — operability (verdict-only): the rekey-cost arm battery becomes executable, with the ignored-path arm

**Before.** `tools/rekey-cost.py` records its live arms as **static receipts**
only (`.ufo/evidence/round-72/cost-live-arm-*.txt`); nothing re-runs them.
The round-72 wave's coverage finding (seat T72W1S09) is the consequence: the
`IGNORED`-filter mutant M3 survives every recorded arm and is killed only by
the selftest. Before-state counter:
`git grep -c REKEY_ARMS a3dd3574 -- tools/rekey-cost.py` → **0**; M3 over the
six recorded arms → `KILLING_ARMS=0/6` (the mutant's six outputs are
byte-identical to the pristine six).

**After.** `tools/rekey-cost.py --arms` runs a **7-arm battery in-process**
against the committed ledger — `sources` 13, `province` 6, `quality` 6,
`scorecard` 0, `pointer` 0, `union(sources,province)` 17, `ignored(skill)` 0 —
and reports `REKEY_ARMS: arms=7 meet=7 unexpected=0` exit 0; `--arms` under
M3 reads `unexpected=1` naming `ignored-skill`, exit 1. The 8th arm, the
no-planned-path case, stays the frozen selftest's (exit 2), so the battery
line counts 7.

**Counter (frozen).**
```
python3 -I tools/rekey-cost.py --arms
python3 -I tools/rekey-cost.py --selftest
```
Frozen outputs: `REKEY_ARMS: arms=7 meet=7 unexpected=0` exit 0;
`REKEY_COST_SELFTEST: 8/8 pass` exit 0 (unchanged — the battery is not a
selftest arm).

**Kill rule.** C2 fails if `--arms` is not `arms=7 meet=7 unexpected=0` exit
0 at both the C2 commit and the round tip, if the selftest is not 8/8, or if
M3 is not killed by the battery.

**Control that skips the claimed work.** The base tool has no `--arms`
(usage exit 2). A battery that prints `meet` for every arm without comparing
the forecast measures `unexpected=0` under M3 as well — it is refuted by the
recorded M3 receipt (`REKEY_ARMS: arms=7 meet=6 unexpected=1`, exit 1) which
the same bytes must produce under the mutant. A battery that omits the
ignored-path arm measures `arms=6`, not `arms=7`.

**Predicate (one sentence).** `--arms` prints `arms=7 meet=7 unexpected=0`
exit 0 on the committed ledger at the C2 commit and at the round tip, the
selftest still reads 8/8, and the same battery under M3 prints
`unexpected=1` naming `ignored-skill`.

## Causal separability

C1 touches `tools/wave-reconcile.py`, `tools/wave-reconcile.json`,
`corpus/QUALITY.md` (criteria 121–123), `corpus/SOURCES.md` (S066 re-open +
tail note). C2 touches `tools/rekey-cost.py` only. Each claim's counter reads
only its own files; neither commit carries the other's bytes.

## Shared no-harm forecast

The round's monitored edit set is `{corpus/SOURCES.md, corpus/QUALITY.md}` —
both rekeyed. Forecast at base:
`python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md --edit corpus/QUALITY.md`
→ `REKEY_COST sections=64 planned=2 at_risk=13 predicted_lost=13` (13, not
19: every QUALITY-pinned section is also SOURCES-pinned). The live RED at the
edit commit must equal 13, and the rekey must restore `lost=0 ok` at both
floors and `credited=64/64` in rev mode. `tools/*`, `plans/*`, `LOG.md` and
`SCORECARD.md` forecast 0 (no section pins them); `corpus/README.md`,
`PROVINCE.md`, `SKILL.md`, `tools/mutate-and-run.sh`, `SHENON`/`SHONEN.md`,
`tools/registry.json` and `tools/coldread-precheck-portable.py` are not
edited.

## Round-72 spot-check routed items — dispositions declared before data

1. Frozen plan vs executed wave → the plan erratum is appended to
   `plans/round-72.plan.md` (frozen text, append-only) and the class becomes
   C1's `roles` red arm.
2. Report count "12 seats, 11 reports" → corrected in this round's report
   erratum and the class becomes C1's `seat_reports` red arm.
3. Census sentence precision → restated in `corpus/lessons/round-73.md`
   `## Gate` (E04 only for a same-scope fixture; the real row prints W04).
4. `tools/pointer-recheck.json` note count → the note is not append-only by
   contract; its count is corrected to the four green arms present.
5. LOG binding for receipt-only commits → this round's LOG entry names
   `93cae77b`, `ebad004b`, `d8e7f337` as inheriting the "Round 72 — appended
   after the wave" entry.
6. Carry — arm coverage → **C2**.
7. Carry — inherited record misses (SCORECARD 6 absent cited paths, LOG 5
   missing quotes) → re-measured at the tip and reported as inherited, not
   this round's claim.

## Wave (13 seats, one v1 wave)

3 executor · 2 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 sentinel · 1 revenger · 1 connector. Planner seat held by the L1 and no
labrat item exists — both are frozen-topology seats the validator rejects
(`ufo-swarm-wave.mjs:263`); the bounded planning data-walk rides the scout
item. Every seat is read-only on tracked files: it writes only under
`.ufo/waves/round-73/w1/<name>/` and its own `$HYAKU_SCRATCH` tree.
