# R98S1 — SCORECARD round-98 section skeleton

> Draft by seat R98S1 (scribe). Placeholders marked `<TO FILL AT RECORDS>` are the
> records-revision values; the pre-freeze controls named below were read from blobs committed
> at `764aca97e513d650949999362cd4b0f5f0e566a5`. The two capability rows are appended to the
> existing `## Capabilities` table; the round-98 section follows the round-97 section's shape.

## Round 98 — two claims: the recorded control code is a measurement (calibration) and every guard refusal class the matrix declared runs (operability)

Base `034240a591575167f0747ad7372a1f4b9cd33a58`; instruments
`d32043ec836ca097e93ae0b095faa7cae4125697` (control-assertion audit, repaired `controls98.py`,
guard refusal battery, registry cell audit); freeze
`764aca97e513d650949999362cd4b0f5f0e566a5` (plan, claims, 12 pre-freeze controls, S012/S009
snapshots); records `<TO FILL AT RECORDS>`.
One v1 wave `w1`, 13 seats (executor 4, reviewer 2, critic 1, connector 1, revenger 1,
mutation-tester 1, scribe 1, scout 1, sentinel 1; attack 4/13 = 31 % by the §6 named set
(reviewer×2, critic, mutation-tester), 7/13 = 54 % including sentinel, connector and revenger).

| Claim | Axis | Before | After (predicate) | Verdict | Counting command | Measured commits |
|---|---|---|---|---|---|---|
| R98-C1 | calibration | at base `034240a5` no committed tool prints a `CONTROL_ASSERT` line (`git grep -c 'CONTROL_ASSERT' 034240a5 -- .` no output, rc 1; `.ufo/evidence/round-98/pre-freeze/c1c2-before-tokens.out`), the base carries neither the audit nor the repaired driver (`git cat-file -e` rc 128), and the round-97 driver's `c2-nowork-absent` is `add("c2-nowork-absent", 0, …)` at line 156 whose receipt carries outer `rc=0` while the wrapped `git grep` returns 1 (spot-check D-2) | pre-freeze at `d32043ec`: `CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0`, exit 0; the round-97 driver `measured=14 literal=1 unmeasured=1`, exit 1, line 156 named; selftest `12/12`; `CONTROLS98 states=18 matched=18 mismatched=0`; at `<RECORDS_REV>`: `<TO FILL AT RECORDS>` | `<TO FILL AT RECORDS>` | `python3 -I tools/control-assertion-audit.py --repo . --rev <RECORDS_REV> --driver .ufo/evidence/round-98/controls98.py`; red arm with `--driver .ufo/evidence/round-97/controls97.py` | `<TO FILL AT RECORDS>` |
| R98-C2 | operability | at base `034240a5` no committed tool prints a `GUARD_REFUSALS` line (`git grep -c 'GUARD_REFUSALS' 034240a5 -- .` no output, rc 1; `c1c2-before-tokens.out`); neither of the two code-only class tokens appears in committed evidence (`git grep -c … -- .ufo/evidence` rc 1 each); the round-97 record receipted four of the six classes the matrix declared and left `state-unbuildable` and `limit-mechanism-missing` code-only (spot-check D-6) | pre-freeze at `d32043ec`: `GUARD_REFUSALS classes=6 refused=6 wrong=0 positive=ok`, exit 0; `--red state-unbuildable` → `classes=6 refused=5 wrong=1 positive=ok red=state-unbuildable`, exit 1; selftest `9/9`; at `<RECORDS_REV>`: `<TO FILL AT RECORDS>` | `<TO FILL AT RECORDS>` | `python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --lane . --rev <RECORDS_REV> --tool .ufo/evidence/round-97/c2/guard-inertia.py --tool-sha 634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8 --work <empty>`; red arm `--red state-unbuildable` | `<TO FILL AT RECORDS>` |

Scores: `<TO FILL AT RECORDS>` (calibration is the claim's axis — lowest non-retired, pinned
8; promotion past the cap needs independent review and is not pre-approved here). **Retired:**
`<TO FILL AT RECORDS>`. **Saturation:** `<TO FILL AT RECORDS>`.

**Wave.** `w1`, 13 seats. `<TO FILL AT RECORDS>` (each seat's finding and its disposition).
Findings the record must state rather than smooth: (a) the frozen tool emits 13
`GUARD_SETUP` tokens and the battery covers the six the round-97 matrix declared, so the
record says "the six classes the matrix declared", never "every class the tool declares"
(`.ufo/waves/round-98/w1/R98C1-c2-classes.txt`); (b) the audit's name resolution is linear and
scope-blind, and a constant at the site's scope can be reported measured when a nested-scope
runner assignment is later in source order
(`.ufo/waves/round-98/w1/R98C1-c1-kill-a-shadow.txt`); (c) the battery does not pin the tool
it drives — any blob whose digest the caller supplies is accepted, so a stub with the class
tokens scores `classes=6 refused=6 wrong=0 positive=ok`, and the C2 DoD measures the interface,
not the frozen bytes (R98R2 F1); (d) the red summary line and its exit 1 are identical for
"red class missed" and "red class refused", so the discriminating evidence is the named
`GUARD_REFUSALS_RED <class> missed-as-declared rc=0` line (R98R2 F2); (e) neither the battery
nor the freeze emits a per-class success line or the ten `GUARD_ROW` lines, so the After
clause's "six per-class runs" is carried, if at all, by a wave harness receipt (R98R2 F3;
`R98E2-transcript-probe.out`: positive 1 line, red 2 lines, 0 `GUARD_SETUP` lines); (f)
`--rev` is validated for 40-hex form and resolvability only, so "at R" is a caller obligation
(R98R2 F5).

### Capability rows (append to `## Capabilities`)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| control-assertion audit | classify every static `add(...)` site of a control driver by the provenance of its recorded code (measured / literal / unresolved) from committed bytes, refusing a bad revision or an absent/unparsable driver at setup | `python3 -I tools/control-assertion-audit.py --repo . --rev <RECORDS_REV> --driver .ufo/evidence/round-98/controls98.py` → `CONTROL_ASSERT sites=15 measured=15 literal=0 unmeasured=0`, exit 0; the round-97 driver → `measured=14 literal=1 unmeasured=1`, exit 1, line 156 named; `--selftest` → `CONTROL_ASSERT_SELFTEST: 12/12 pass` (`.ufo/evidence/round-98/pre-freeze/c1-audit-*.out` at `d32043ec`; records lines `<TO FILL AT RECORDS>`) | round 98 |
| guard refusal battery | drive the six `GUARD_SETUP` refusal classes the round-97 matrix declared through the public CLI of the tool blob whose digest the caller pins (`--tool-sha`), one manifest fixture per class, with the positive run and a red arm that must miss; the battery does not pin the tool path or digest itself — a stub with the same interface and tokens scores the same, so the frozen tool's identity is the caller's obligation (R98R2 F1) | `python3 -I .ufo/evidence/round-98/refusals/guard-refusals.py --lane . --rev <RECORDS_REV> --tool .ufo/evidence/round-97/c2/guard-inertia.py --tool-sha 634997d0… --work <empty>` → `GUARD_REFUSALS classes=6 refused=6 wrong=0 positive=ok`, exit 0; `--red state-unbuildable` → `refused=5 wrong=1`, exit 1; a non-64-hex and a mismatched pin → `GUARD_REFUSALS_SETUP tool-sha-invalid` / `tool-sha-mismatch`, exit 2 (wave receipts `R98E2-pin-short.out`, `R98E2-pin-zero.out`); `--selftest` → `GUARD_REFUSALS_SELFTEST: 9/9 pass` (`.ufo/evidence/round-98/pre-freeze/c2-refusals-*.out`; records lines `<TO FILL AT RECORDS>`) | round 98 |

### Routed-defect closures (round-97 spot-check, not claims)

- **D-1** — the round-97 in-place `anchor` additions on S006/S159 are logged old → new in
  `corpus/lessons/round-98.md` §Registry changes (append-only remedy B; no cell rewritten) and
  measured by `tools/registry-cell-immutability.py`: red pair `0b19af5f..29734beb` prints
  `REGISTRY_CELL S006:anchor changed`, `REGISTRY_CELL S159:anchor changed`,
  `changed=2 removed=0 added=0`, rc 1; green pair `29734beb..d32043ec` prints `changed=0
  removed=0 added=0`, rc 0; selftest `10/10` (`.ufo/evidence/round-98/pre-freeze/registry-*.out`).
- **D-3** — the three pre-A15 fragments (`pre-freeze/c1-forge-conjunct.out`,
  `w1/SC1-quote-backability.txt`, `w1/SC1-receipt-catalog.txt`) are marked superseded by
  appended notes beside them with both digests, never rewritten; the notes land with this
  records revision (`.ufo/evidence/round-97/pre-freeze/NOTE-superseded-r98.txt`,
  `.ufo/waves/round-97/w1/NOTE-superseded-r98.txt`; digests re-derived from the blobs at
  `29734beb`: `1c9754f3…`, `e7cdb4f9…`, `f600b2ea…`, `e2c1cb77…`, `a1add17f…`).
- **D-4** — `committed-battery binder` (round 97; `BATTERY states=50 matched=50 mismatched=0
  missing=0`, `--selftest 7/7`, `.ufo/evidence/round-97/landing/c1-positive-{1,2,3}.out`,
  sha256 `54c6f667…`) and `guard-inertia matrix` (round 97; `GUARD_INERTIA rows=10 killed=8
  limits=2 survived=0 unmet=0`, `--selftest 7/7`, `.ufo/evidence/round-97/landing/
  c2-positive-{1,2,3}.out`, sha256 `254536aa…`) enter the `## Capabilities` table in this
  round's append, with the correction sentence beside the table.
- **D-5** — the round-97 report erratum is in `corpus/lessons/round-98.md` §Errata (S159
  quote 15 words and snapshot `4b5a8374…`; S006 renderer span 490-491 inside the paragraph
  490-492) and `CONTROLS97 states=18 matched=18 mismatched=0` lands with this records
  revision as `.ufo/evidence/round-97/pre-freeze/CONTROLS97-summary.txt`, labelled a
  restatement, not a re-execution.
- **D-7** — the stale-lane line is graded `progressing` with commit counts in the round
  report (`git rev-list --count 034240a5..HEAD` → 4 at this scribe's write: `6b1428c8`,
  `d32043ec`, `764aca97`, `cdaecece`); final report line `<TO FILL AT RECORDS>`.
