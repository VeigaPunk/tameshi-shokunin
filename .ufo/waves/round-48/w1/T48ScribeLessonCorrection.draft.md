# Round-48 lesson — two append-only corrections (draft)

seat: `T48ScribeLessonCorrection` (w1, round 48, L1 TameshiR48)
date: 2026-10-26
base rev: `473336d9d789f6081195e7376d17836a24666bc3`
status: **draft, ready to append.** The destination is `corpus/lessons/round-48.md` (not yet written at this seat's run). Nothing here rewrites `corpus/lessons/round-47.md`: QUALITY criterion 4 — "Errata are append-only blocks" (`corpus/QUALITY.md:7`) — and routed defect 3 of `corpus/lessons/round-47-verifier-spotcheck.md:105` ask for a *named* correction, not an edit. Both blocks below are written to be pasted verbatim into the round-48 lesson, under a `## Corrections to earlier lessons (append-only)` heading.

Routed by: `corpus/lessons/round-47-verifier-spotcheck.md:25` (conformance defect 5) and `:105-106` (routed items 3 and 4).

---

## Correction C1-R48-1 — the round-47 dependence sets (unreceipted freeze-time observation)

Class: reference-drift + stale observation (a freeze-time observation restated as the round's dependence finding: the pointer it gives, `before/c1-at-freeze.stdout`, is offered for the `total=22` figure and not for the sets, no revision is named beside them, and they disagree with the rows that same round pinned — one of them, `hermetic`, also disagreeing with the deciding run).

### What was stated, and where

`corpus/lessons/round-47.md` (sha256 `50b47845be5609a6…`, 14348 B), lines 117-118, verbatim:

```
at the freeze `total=22` (every row lacked the clause; `before/c1-at-freeze.stdout`); observed dependence sets: `six-leg regression ledger` {fleet-root, node}, `effective expectation reconciliation` {jj},
`retained invocation-context gate` {fleet-root}, `hermetic env-differential probe` {env, node}, `mutation report interop` {node}; the other 17 observed `none`. C3: `python3 .ufo/evidence/round-47/coverage/measure.py --lane LANE --rev REV`; before `rows=0 entries=0`.
```

The two sets this correction is about are `six-leg regression ledger` {fleet-root, node} and `hermetic env-differential probe` {env, node}. The lesson calls them "observed dependence sets" in a paragraph that ends "The deciding values are in the report and SCORECARD.md" — i.e. they read as the round's dependence finding, which is what the round-47 standing rows restate. They are not.

### What the standing rows state

`SCORECARD.md:2270` (standing self-assessment re-stated at round 47, `### Standing self-assessment — re-stated at round 47`, which opens at `:2262`), verbatim:

```
| six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: FAIL (cases=9 passed=7`, exit 1, tool sha256 `a7d3f2dd7d47`, deps `env,fleet-root,node` | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
```

`SCORECARD.md:2276`, verbatim:

```
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23`, deps `bwrap,node` | round 21 |
```

So the rows declare {env, fleet-root, node} and {bwrap, node}.

### What was observed, and by which receipt

The deciding run at content revision `8b0e15d25ea598c0bf908d183fb410a085bf3a18`, `.ufo/evidence/round-47/after/c1.stdout` (sha256 `b56a8c2a861664046d6026a95dd452b00ec9331b00e5b523eeb9e0e0b6b37305`, 11099 B, `after/c1.exit` = 1), line 5 verbatim:

```
STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47 observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 (exit=0) MISMATCH declared_deps=env,fleet-root,node observed_deps=fleet-root,node DEPS-MISMATCH
```

line 17 verbatim:

```
STATEMENT cap/hermetic env-differential probe: claimed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 observed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 (exit=0) MATCH declared_deps=bwrap,node observed_deps=bwrap,node DEPS-OK
```

and the verdict line (`.` = `after/c1.stdout` last line):

```
C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=1 unparsed=0 unobservable=0 dep_mismatch=1 unpinned=0 append_only=1 total=2 rev=8b0e15d25ea598c0bf908d183fb410a085bf3a18 C1_R47_PASS=false
```

The deciding run therefore observed {fleet-root, node} for `six-leg regression ledger` (matching the lesson, disagreeing with that row's `deps` → `DEPS-MISMATCH`) and {bwrap, node} for `hermetic env-differential probe` (matching that row, disagreeing with the lesson).

The lesson's two sets are byte-identical to the **freeze-time** emission, not the content revision: `.ufo/evidence/round-47/before/c1-at-freeze.stdout` (sha256 `27ca1e91cc61f08c…`) lines 5 and 17, and `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` (sha256 `1d70c44ed2edbc82…`) lines 5 and 17:

```
STATEMENT cap/six-leg regression ledger: claimed=- observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 (exit=0) UNPARSED declared_deps=- observed_deps=fleet-root,node DEPS-OK
STATEMENT cap/hermetic env-differential probe: claimed=- observed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 (exit=0) UNPARSED declared_deps=- observed_deps=env,node DEPS-OK
```

The round-47 disclosure already said both sets are unstable (`SCORECARD.md:2314`, tail quoted): "its dependence set was {env, node} in one run and {bwrap, node} in another … a deciding run that observes a different set for either statement is a `dep_mismatch` and is reported as such, not re-run until it agrees." The declared `env,fleet-root,node` for `six-leg regression ledger` traces to a wave-1 probe under load, `.ufo/waves/round-47/w1/T47CritC1Control.md:253`: "six-leg regression ledger … quiet: P2=`REGRESSION: PASS (cases=9 passed=9`, exit 0   → deps env,fleet-root,node".

### Delta, stated narrowly

- As a description of the **freeze-time** emission the lesson is accurate, but it does not name that receipt, the revision or the round, inside a paragraph whose closing sentence points the reader at the deciding values.
- As a description of **what the round-47 standing rows restate**, the sentence is wrong for both statements: the rows carry {env, fleet-root, node} and {bwrap, node}.
- The deciding run reproduced the lesson's `six-leg` set but not its `hermetic` set; the `six-leg` row's declared set is the one the deciding run scored `DEPS-MISMATCH`.

### Correction block to append (round-48 lesson)

```
- **C1-R48-1 (corrects `corpus/lessons/round-47.md:117-118`; the file is never rewritten).**
  The round-47 lesson's "observed dependence sets" — `six-leg regression ledger` {fleet-root, node},
  `hermetic env-differential probe` {env, node} — are the **freeze-time** emission
  (`.ufo/evidence/round-47/before/c1-at-freeze.stdout:5,17` =
  `control/emit-observed-pre-freeze.out:5,17`), printed there without receipt, revision or round.
  The round-47 standing rows, which restate the content-revision emission, declare
  {env, fleet-root, node} (`SCORECARD.md:2270`) and {bwrap, node} (`SCORECARD.md:2276`); the
  deciding run at `8b0e15d2…` observed {fleet-root, node} and {bwrap, node} and scored the
  `six-leg` row `DEPS-MISMATCH` (`.ufo/evidence/round-47/after/c1.stdout:5,17`, verdict
  `total=2 … dep_mismatch=1 … C1_R47_PASS=false`). Both statements are the two the round-47
  disclosure names as unstable across runs under host load (`SCORECARD.md:2314`).
  **Rule for later rounds:** a dependence set is restated only from the deciding `--emit`, with
  that receipt's path and revision named beside it; a freeze-time set is labelled as the freeze
  state and never presented as the round's observed finding.
```

### Provenance

| artifact | sha256 (first 16) | bytes | lines cited |
|---|---|---|---|
| `corpus/lessons/round-47.md` | `50b47845be5609a6` | 14348 | 117-118 |
| `SCORECARD.md` (lane worktree) | `954e057f9395ff06` | 248883 | 2262, 2270, 2276, 2314 |
| `.ufo/evidence/round-47/after/c1.stdout` | `b56a8c2a86166404` | 11099 | 5, 17, last |
| `.ufo/evidence/round-47/before/c1-at-freeze.stdout` | `27ca1e91cc61f08c` | 10017 | 5, 17 |
| `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` | `1d70c44ed2edbc82` | 18790 | 5, 17 |
| `.ufo/waves/round-47/w1/T47CritC1Control.md` | `6db680af53bd341c` | 27649 | 253 |
| `corpus/lessons/round-47-verifier-spotcheck.md` | `1b245d7e8b96eba0` | 15711 | 25, 105 |

---

## Correction C1-R48-2 — the refusal of `r8-predictive-test-selection-cost.md` (wrong decisive cite)

Class: reference-drift (a criterion citation that does not say what it is cited for) + misattributed reason.

### What was stated, and where

Three places, all in the round-47 record:

1. `corpus/lessons/round-47.md:81`, verbatim:

```
| `r8-predictive-test-selection-cost.md` | refused | out of province (vendor-scale test selection; `PROVINCE.md:14-18`), unopened row; QUALITY 10, 2 | a row opened by the lane that ties selection to an own-leg re-sweep decision (F7) |
```

2. `.ufo/waves/round-47/w1/T47RevProvince.md:30`, verbatim:

```
| `r8-predictive-test-selection-cost.md` | **REFUSE** (out of province, unopened row) | `PROVINCE.md:14-18` | 10, 2 |
```

3. `.ufo/waves/round-47/w1/T47RevProvince.md` §6.5 (`:428` onward), the cite as written, verbatim:

```
infrastructure. **PROVINCE.md:14-18** (product domain) and **QUALITY 10** (its
document `S205` / arXiv 1810.05286 is not a lane row: `grep -c '1810.05286'
corpus/SOURCES.md` → 0) and **QUALITY 2** (the quote's magnitude cannot be
checked against any committed snapshot).
```

### What the cited lines actually say

`PROVINCE.md:14-18`, verbatim:

```
**Refuses:** product domains — every lane's gate remains its own; tameshi
owns only the reusable craft (a pattern is admitted from evidence in TWO
independent lanes before it is claimed general). Never edits a sibling's
gate code (read-only probes; recommendations travel in round reports).
Credential material (→ kagi), endpoint health (→ kama).
```

These lines refuse product domains, sibling gate code and credential/endpoint material. They say nothing about test selection, cost baselines or evidence admission; the refusal they support is about *whose gate it is*, not about *whether the claim is anchored*. The decisive defect of the entry is the anchor: its `source:` cites `S205` / arXiv 1810.05286, and the lane has no such row — `grep -c '1810.05286' corpus/SOURCES.md` → `0`, `S205` → `0` (`corpus/SOURCES.md` sha256 `bb8f0997b820b859…`) — so the quoted magnitude has neither an opened row (QUALITY 10) nor a committed snapshot behind it (QUALITY 2). The package copy's own head (sha256 `af5bef5fa75f6e1a…`, 2770 B) carries `source: S205 — https://arxiv.org/abs/1810.05286 …`, `verified-at: 2026-10-24`, `ground: F7`.

QUALITY 10, verbatim (`corpus/QUALITY.md:27-30`): "A new `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`; an external source enters through a `SOURCES.md` row opened in the round that writes it (tiers: `SOURCES.md`, contract v1); a tier-C row is never sole support. (MK-7)". QUALITY 2, verbatim (`corpus/QUALITY.md:4-5`): "Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge."

### What the closure ruled

`corpus/lessons/round-47-verifier-spotcheck.md:90`, verbatim (reason column of the discernment table):

```
the decisive reason is QUALITY 10/2: the entry cites a row the lane never opened. The `PROVINCE.md:14-18` cite is weak (those lines refuse product domains and sibling gates, not test selection); the flip condition (an opened row tied to an own-leg F7 re-sweep decision) is the right one
```

and its routed item, `:106`, verbatim:

```
4. **Reject citation**: when refusing `r8-predictive-test-selection-cost.md` again, cite the unopened-row reason (QUALITY 10) rather than `PROVINCE.md:14-18`.
```

### Correction block to append (round-48 lesson)

The corrected row, ready for the round-48 lesson's package table (reason cell carries the decisive criterion; the flip condition is kept and made checkable):

```
| `r8-predictive-test-selection-cost.md` | refused | unopened row: its `source:` cites `S205` / arXiv 1810.05286 and the lane has no such row (`grep -c '1810.05286' corpus/SOURCES.md` → 0, `S205` → 0), so the quoted factor-of-two magnitude has no row opened in the round that writes it and no committed snapshot behind it — **QUALITY 10** (decisive) and **QUALITY 2**. The round-47 `PROVINCE.md:14-18` cite is withdrawn as the decisive reason: those lines refuse product domains, sibling gate code and credential/endpoint material, not test selection (closure ruling, `round-47-verifier-spotcheck.md:90`, routed item 4 at `:106`) | **flip:** a `S205` row opened `mined` in the writing round, carrying a committed round snapshot whose anchor the entry pins, **and** a named own-leg move that consumes change-level selection (F7 re-sweep). With the row opened but no consuming move, the entry stays a report line (its province argument survives as prose in `T47RevProvince.md` §6.5, which is never rewritten) |
```

### Provenance

| artifact | sha256 (first 16) | bytes | lines cited |
|---|---|---|---|
| `corpus/lessons/round-47.md` | `50b47845be5609a6` | 14348 | 81 |
| `.ufo/waves/round-47/w1/T47RevProvince.md` | `8984dc3f530cea9c` | 35475 | 30, 428+ (§6.5) |
| `PROVINCE.md` | `b2875fe21f381d98` | 6334 | 14-18 |
| `corpus/QUALITY.md` | `8fba0f5523f7eca8` | 88755 | 7 (4), 4-5 (2), 27-30 (10) |
| `corpus/SOURCES.md` | `bb8f0997b820b859` | 112478 | absence of `S205` / `1810.05286` |
| `corpus/lessons/round-47-verifier-spotcheck.md` | `1b245d7e8b96eba0` | 15711 | 25, 90, 105-106 |
| package `r8-predictive-test-selection-cost.md` (`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/`) | `af5bef5fa75f6e1a` | 2770 | 1-5 (`source:`, `verified-at:`, `ground:`) |

---

## Not changed (bounds of this draft)

- `corpus/lessons/round-47.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `T47RevProvince.md` and the package copy are read-only to this seat; the corrections are appended ahead of them, per QUALITY 4.
- No counted surface is edited: the refusal row's verdict (`refused`) and the C1 numbers (`total=2`, `C1_R47_PASS=false`) stand as filed; only the *reason cited* and the *provenance of the stated sets* are corrected.
- The C1 counter, its rows and the round-48 predicates are the L1's; this draft neither re-runs nor rescopes them.
- `corpus/lessons/round-48.md` did not exist at this seat's run, so the destination is named, not written.
