# ScoutC2Records — SCORECARD contract field sweep, rounds 38–42

Read-only sweep. No files edited outside this report; no tool installs; no scratch dirs used.

## Scope and presence rule

- Contract list: `/home/vgpnk/Projects/shokunin/AXES.md:75-83` — five fields:
  `axes`, `capabilities`, `planned`, `saturation`, `retired`. The heading is
  "SCORECARD.md contract (**per child repo**)"; AXES.md says nothing about per-round
  restatement. So the five fields are file-scoped by the contract; the per-round
  blocks are the lane's own rendering, and I graded per-block presence against that
  rendering (see §Caveat).
- Swept file: `SCORECARD.md` in the lane checkout. Round 38 begins at `SCORECARD.md:1821`;
  round 42 is the last block (`SCORECARD.md:1995`) and runs to EOF (`SCORECARD.md:2046`).
- Presence rules I applied (stated so a reviewer can re-grade):
  - **axes** = named axis(es) + 0–10 score + evidence/counting pointer.
  - **capabilities** = repertoire row, or an explicit "no new row" declaration
    (the lane's own convention at 1840/1866).
  - **planned** = a `Planned (round N+1)` line naming intended claims and their
    target axis/capability.
  - **saturation** = saturation-line value **and** stagnation window N. `partial` when
    only one of the two appears.
  - **retired** = retirement disposition (axes retired with justification, or an
    explicit "none retired").

## Matrix

| Block | lines | axes | capabilities | planned | saturation | retired |
|---|---|---|---|---|---|---|
| Round 38 | 1821–1852 | **carried** — claim table `Axis` column `SCORECARD.md:1828`; numeric restatement `SCORECARD.md:1833-1838` (depth 9→9, calibration 8→8, command D) | **carried (no row)** — `SCORECARD.md:1840` "Capabilities table: no new row this round" | **carried** — `SCORECARD.md:1847` `**Planned (round 39):**` | **absent** — only `SCORECARD.md:1823-1825` ("lowest non-retired axis", "inside the stagnation window"); no line value, no N | **absent** — only the adjective "non-retired" at `:1823`; no disposition |
| Round 39 | 1853–1869 | **carried** — `SCORECARD.md:1857` (claim table) + `:1864` (depth 9→9, calibration 8→8, command D) | **carried (no row)** — `SCORECARD.md:1866` "Capabilities table: no new row." | **carried** — `SCORECARD.md:1868` `**Planned (round 40):**` | **absent** — `SCORECARD.md:1855` "round 37 added a capability inside the window"; no line value, no N | **absent** — "non-retired" adjective only (`:1855`) |
| Round 40 | 1870–1894 | **carried** — `SCORECARD.md:1874` (claim table) + `:1891` (depth 9→9, calibration 8→8, command D) | **carried (row admitted)** — `SCORECARD.md:1885` + table `:1887-1889` (`write-path-census-v2`) | **carried** — `SCORECARD.md:1893` `**Planned (round 41):**` | **carried** — `SCORECARD.md:1872`: "at or above the saturation line 8 … (window N=2)" | **absent** — no retirement disposition |
| Round 41 | 1895–1994 | **carried** — `SCORECARD.md:1911` (claim table) + `:1922-1926` (depth 9→9, calibration 6→6, command D + round-21 monitor) | **carried (row admitted)** — `SCORECARD.md:1916` + table `:1918-1920` (write-path census destination resolution) | **ABSENT** — no `Planned (round 42)` line anywhere in 1895–1994; the last `**Planned` in the file is `:1893`. Round-42 mentions at `:1945`, `:1953`, `:1964` are "routed to round 42" defect routing, not declared claims with a target axis | **partial** — `SCORECARD.md:1902` gives "window N=2"; no saturation-line value | **absent** — "non-retired" adjective only (`:1901`) |
| Round 42 | 1995–2046 | **carried** — `SCORECARD.md:2003` (claim table `Axis` column) + `:2008-2012` (base: depth 9, calibration 6) + `:2043-2045` (unchanged at round commit) | **ABSENT** — no `Capabilities table` line, no row, no "no new row" declaration; the only trace is prose "C2's gain is a capability, not a ledger count" at `:2012` | **ABSENT** — no `Planned (round 43)` line anywhere in 1995–2046 (file ends at 2046) | **partial** — `SCORECARD.md:1998-1999` gives "window N=2"; no saturation-line value | **absent** — no retirement disposition |

Command basis: `grep -nE '^(##|###) |saturation|stagnation|retired|^Capabilities table|^Numeric axes|\*\*Planned|^\| Capability' SCORECARD.md` filtered to `>=1821`, plus `grep -n '^| Claim | Axis'` (`:1828,1857,1874,1911,2003`) and `grep -n 'Numeric axes'` (`:1833,1864,1891,1922,2008`); block extents from `grep -n '^## Round '`.

## Round 42's gap — verbatim

The round-42 block carries **no `planned` field** (and, separately, no `capabilities`
field). The block ends at EOF with no plan paragraph:

```
Numeric axes unchanged:
depth 9 → 9, calibration 6 → 6 (command D and the round-21 coldread monitor at the base
and at the round commit); no axis is harmed. The v4 tool's wider false-negative classes are
recorded in the lesson and the knowledge entry, outside the frozen claim.
```
(`SCORECARD.md:2043-2046`, byte-verbatim; `→` are U+2192)

Corroboration, verbatim from this round's counter docstring
(`.ufo/evidence/round-43/calibration/measure.py:13-16`):

```
        contract makes `planned` a required field and a round that omits it
        leaves its successor undeclared. At the base, the round-42 block has
        no such line (the last one is `Planned (round 41)`).
```

The last actual planned line in the file, and the shape round 42 should have carried:

```
**Planned (round 41):** `cmp` and `git diff --exit-code` lattices stay unmeasured; the v2 pattern still misses a variable destination on `os.replace`.
```
(`SCORECARD.md:1893`)

So round 42 declares no round-43 intended claims, no target axis/capability for
round 43, and therefore also no round-43 target for the lane's lowest non-retired axis.

## Does any other block have the same gap?

- **Same `planned` gap: yes — round 41 (`SCORECARD.md:1895-1994`).** No
  `Planned (round 42)` line exists; the file's last `**Planned` line is `:1893`
  (`grep -n '\*\*Planned' SCORECARD.md` ends there). Round 41's only forward
  statements are routing notes (`:1945`, `:1953`, `:1964`), which name successor
  counters, not claims-and-targets. Rounds 38, 39, 40 all carry the field
  (`:1847`, `:1868`, `:1893`), so the gap is a round-41/42 regression, not a
  long-standing shape.
- **Same `capabilities` gap: round 42 is unique.** Round 38 `:1840` and round 39
  `:1866` declare "no new row" explicitly; rounds 40 `:1885-1889` and 41 `:1916-1920`
  admit rows. Round 42 does neither. (Note: round 42's C2 capability target *failed*,
  so no row was admissible — but the field's explicit "no new row" form is still
  missing, unlike rounds 38/39 where the same situation was declared.)
- **`saturation`: only round 40 (`:1872`) states both the line value and N.** Rounds
  38 and 39 name the stagnation window but give neither N nor the line; rounds 41 and
  42 give N=2 only. Earlier blocks did carry both, e.g. round 21
  (`SCORECARD.md:861-863`: "declared saturation line (depth 8, calibration 8; `## Saturation`, line 8/10) … window N = 2") and round 12 (`:330`: "Saturation 8 and stagnation window 2 remain; no retirement."). The 38–42 blocks dropped that restatement.
- **`retired`: no block 38–42 states it.** Not unique to round 42 — but round 12
  folded saturation + non-retirement into one line (`:330`), so the omission is also
  a regression in rendering, not a per-lane policy change.

## Standing (file-level) sections — these carry the contract, and are stale

The five fields also live in the top-of-file sections, and there they are stale — which
is why the per-round blocks are the operative carrier for three of the five:

| Field | Standing carrier | State |
|---|---|---|
| axes | `## Current axes — fleet round-1 baseline`, `SCORECARD.md:58-84` (has a `Last-change round` column at `:64`) | stale: depth 6, calibration 0 (`:66-67`) vs depth 9 / calibration 6 in the round blocks |
| capabilities | `## Capabilities`, `SCORECARD.md:236-251` | stale: newest row is round 22 (`:249`); round 40/41 admissions live only inside round blocks (`:1889`, `:1919`) |
| planned | `## Planned`, `SCORECARD.md:264-279` | stale: newest entry is "Round 2 (declared fleet round 1, kaika)" (`:268`); no round-43 claims |
| saturation | `## Saturation`, `SCORECARD.md:253-262` | current: "**saturation line 8/10**" (`:257`), "**Stagnation window N = 2**" (`:259-260`) |
| retired | `## Retired`, `SCORECARD.md:281-283` | current: "- none retired; record with justification when an axis is retired." Also baseline `:83-84` "**Retired:** none." |

## Caveat on what "missing" means here

`AXES.md:75` scopes the five fields **per child repo**, not per round. Read strictly,
round 42's omission of `saturation`/`retired` is a rendering choice (the file-level
sections carry them), and the only *contract* miss is that the file's `planned` carrier
is stale — no section anywhere in `SCORECARD.md` declares round-43 claims. The lane's
own convention (rounds 38–40, plus the round-43 m12 class) makes `planned` the field
that must appear **in the newest round block**, so round 42 fails on that rule and on
the file-level carrier simultaneously. `capabilities` for round 42 is a gap only under
the lane's explicit "no new row" convention, not under the bare contract text.

## Consequences for round-43 C2 (m12), from the counter's code

- `m12_planned` is a bare substring test on the newest block only:
  `wanted = 'Planned (round %d)' % (round_no + 1)`; hit iff `wanted in block_text`
  (`.ufo/evidence/round-43/calibration/measure.py:118-121`), called once for the newest
  block (`:403`), where `newest_round_block` takes the **last** `## Round N` match and
  returns text through EOF (`:110-116`). At base/freeze the newest block is round 42, so
  `m12=1` for the absent `Planned (round 43)`.
- Two limits a reviewer should record: (1) the test is shape-blind — any occurrence of
  the literal string inside the block, including a prose sentence like "no `Planned
  (round 43)` line exists", would satisfy it; (2) it audits only the newest block, so
  round 41's identical omission was counted only while round 41 was newest and is
  invisible at every later revision. This round's sweep finds it only because the sweep
  is not the counter.
- Forward hazard, not a finding about round 42: at the round-43 measured commit the
  newest block becomes round 43, so `m12` will demand the literal `Planned (round 44)`
  inside the round-43 block; absent that line, `m12=1` and `C2_R43_PASS=false` by the
  predicate at `measure.py:33-34`. The round-42 gap will have been superseded, not
  repaired — no revision will ever count it again.

## Adjacent structural drift (not one of the five fields)

Round 42's claim table header omits the `Delta` column that rounds 38–41 carry
(`SCORECARD.md:2003` vs `:1828`, `:1857`, `:1874`, `:1911`). Not a contract field;
noted so a later reader does not mistake the column shift for a missing `Delta` field
under the contract.

## Confidence

- High: every line cite above was read directly (`sed`/`grep` over
  `SCORECARD.md:1821-2046`); the round-42 block ends at EOF (2046 lines total), so
  "no plan paragraph follows" is exhaustive within the file.
- High: rounds 38/39/40 have `planned`; none exists after `:1893` — verified by a
  file-wide `grep -n '\*\*Planned'`, whose last hit is `:1893`.
- Judgment (stated rule above): round 42 `capabilities` = absent though prose at `:2012`
  uses the word "capability"; round 41 `planned` = absent though routing notes name
  round 42. A lenient grader could count both as implicit; neither has a field shape.
- Unresolved: whether the L1/adjudicator treats the stale top-of-file sections
  (`:58-65`, `:236-251`, `:264-279`) as satisfying the per-repo contract for axes,
  capabilities and planned. Under that reading, the contract miss is the stale `planned`
  carrier, and the per-block gaps are a rendering regression that m12 happens to police
  for the newest block only. No AXES.md text settles this; `AXES.md:75` says only
  "per child repo".
