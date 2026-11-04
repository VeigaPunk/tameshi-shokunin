# tameshi round 77 — plan (frozen before any claim data)

Lane: tameshi-shokunin. Base: `ac6baf7a46df613b171b4c1ab834c888cd6321b9`
(branch `master` = `origin/master`, clean tree — the round-76 non-author closure
verdict commit, `corpus/lessons/round-76-verifier-spotcheck.md`).

Round shape: **one v1 wave, 12 seats** (policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; attack seats by the policy's
named set = reviewer 2 + critic 1 + mutation-tester 1 = 4 = 33.3 %). `labrat`
is a frozen-topology seat the validator rejects, so no labrat item exists; the
planner seat stays with the L1 per the orchestrator ruling.

Saturation state at round start (SCORECARD.md): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. A
capability entered at round 74 (`round-range additivity sweep`); rounds 75 and
76 entered none, so two capability-less rounds sit at the window boundary
(N = 2) and **a capability-less round 77 fires the nudge for round 78**. That
is declared, not waived: C2 works the lowest scored numeric axis (calibration
8) regardless, and no nudge waiver is claimed here.

Two claims, distinct axes, causally separable: C1 lands only inside
`tools/wave-reconcile.py`, `tools/wave-reconcile-mutants.spec` and their
battery receipts; C2 lands only inside `.ufo/evidence/round-21/coldread/ledger.json`
plus the round's rekey evidence and the record paragraphs that correct the
mislabelled claim. C2's before-state is measured at base; its after-state needs
only a rekey over whatever set the monitor reports at the pre-rekey tip — it
does not need C1's bytes, and a C1-less round would rekey a different (smaller)
section set to the same 65/65 predicate. C1's counter never reads the ledger.

Design-phase disclosure (pre-data, this plan's own commit): the L1 built the C1
candidate and ran the 8-defect battery in scratch before this plan was frozen;
the candidate bytes, the extended spec, every battery stream and the base
survivor control are committed under `.ufo/evidence/round-77/design/` in the
same commit as this plan. The predicates below are frozen against those
measurements; the wave's seats re-derive and attack them.

## R77-C1 — operability (sourced on S305, opened this round): the round-76 recursion survivor becomes arm20

**Named survivor (round-76 carry, `T76W1M1.md`).**
`git-listing-recursion-removed` — `GitReader.listing` drops `-r`, so
`git ls-tree --name-only <rev> -- <dir>` returns the tree entry instead of the
directory's descendants; the round-76 wave measured it surviving the 19-arm
suite 19/19 while a production-backed discriminator read `printed=127 files=0`
against pristine `files=127`. Re-measured at base this round on base bytes:
the mutant is `WAVE_RECONCILE_SELFTEST: 19/19 pass`
(`.ufo/evidence/round-77/base-survivor-r77.txt`, second block; the pristine
base reads the same line, first block).

**Sourced ground (S305).** Git's own `git-ls-tree` page: `-r` —
"Recurse into sub-trees." (page line 1664) — and "directory name (without -r)
will behave differently" (page lines 1631-1632). A path-limited listing is
recursive only when `-r` is passed, so the protected rule is a documented
contract, not a recall.

**Before (measured at base `ac6baf7a`).**
`git show ac6baf7a:tools/wave-reconcile.py | sha256sum` →
`ca05ec154454d57902313dcddd3c1e6980628bb352f57344afdcd820db5767e3`;
`python3 -I -X utf8 tools/wave-reconcile.py --selftest` →
`WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0
(`.ufo/evidence/round-77/base-selftest-wr.txt`);
`tools/wave-reconcile-mutants.spec` carries 7 defects
(sha256 `6ffb4a3a15155fe511a6…` at base) and the recursion mutant survives
19/19.

**After.**
`tools/wave-reconcile.py` gains `arm20-nested-listing-recursion`: a REAL git
fixture (`tempfile.mkdtemp` + `git init -q`, toplevel verified equal to the
fixture root per the lane's git-fixture rule, removed in `finally`) holding
`wave/one.md` and `wave/nested/two.md`, a record blob whose span is
`1 seat report` with `printed: 1`, measured through the production `GitReader`.
Recursion returns both paths (the nested one excluded by the top-level rule) →
`files=1` → `meet`; a reader without `-r` returns the `wave` tree entry →
`files=0` → `drift`. `SELFTEST_ARMS` 19 → 20.
`tools/wave-reconcile-mutants.spec` gains the eighth defect
`git-listing-recursion-removed` (the exact single edit; the first seven blocks
byte-identical to base).

Counting commands (pasteable; after-state at the landing rev):

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r77/l1/battery" --label wave-reconcile-arms-r77
```

Expected after-state: `WAVE_RECONCILE_SELFTEST: 20/20 pass` exit 0; the battery
prints `CONTROL: GREEN`, `MUTATE: DONE (target=wave-reconcile-arms-r77
defects=8 killed=8 survived=0 inconclusive=0 kill-rate=100%)` and
`MUTATE_RESTORE: OK` byte-identical.

**Kill matrix (frozen; measured on the design-phase candidate
`.ufo/evidence/round-77/design/battery-results.tsv` and the per-defect streams,
pristine 20/20):**

| mutant | dies on |
|---|---|
| `m2-delimited-tautology` | arm13 + arm16 (r75 collateral, unchanged) |
| `span-rule-removed` | arm14 + arm17 + arm18 (r75 collateral, unchanged) |
| `seat-reports-any-depth` | arm15 + **arm20** (new intrinsic collateral: any-depth counting also fails the real recursive-listing fixture — disclosed, not a defect) |
| `mc-record-bound` | arm16 |
| `roles-bypass` | arm17 |
| `attack-bypass` | arm18 |
| `adv-seatreports-require-printed-bypass` | arm19 only |
| `git-listing-recursion-removed` | **arm20 only** |

**Kill rule (frozen, satisfiable by construction from the table above).** C1
fails if (i) the pristine selftest is not green at the stated count (20/20);
(ii) the battery control is not GREEN or the restore is not byte-identical;
(iii) the battery is not `defects=8 killed=8 survived=0`; (iv) the new defect
dies on any arm other than arm20, `m2`/`span-rule-removed`/`mc`/`roles`/
`attack`/`adv` change their kill set from the table above, or
`seat-reports-any-depth` fails any arm other than the disclosed arm15 + arm20;
(v) any base arm 1–19 changes its outcome between base bytes and landed bytes
(arms 1–19 selftest lines byte-identical); or (vi) the landed bytes change any
counter other than the selftest arm count/spec defect count (the standing
six-row wave sweep and the 20-row selfstate sweep stay out of scope).

## R77-C2 — calibration (the lowest scored axis at 8): the cold-read credit the record claims is the monitor's reading at the true tip

**Before (measured at base `ac6baf7a`).**
`python3 -I -X utf8 tools/coldread-precheck-portable.py --repo . --rev ac6baf7a --work <scratch> --out .ufo/evidence/round-77/coldread-base-r77.json`
→ `COLDREAD_PORTABLE rev=ac6baf7a46df credited=63/65 elapsed=2.7s
probe_sampled=20 probe_mismatches=0`; the `--out` JSON's `measure` block reads
`sections_covered=63 sections_total=65 box3_full_page=false`, with exactly two
uncredited sections (**`## Standing rules`**, **`## Mutation-sweep recipe —
numbered steps; bounded cold-read evidence`**) whose reasons are
`input-drift` on `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `tools/registry.json`, `PROVINCE.md`.
The round-76 record claims `credited=65/65` "at the landing tip (`b2b0f82a`)";
`b2b0f82a` is the last rekey batch, not the tip (`ac6baf7a` is), and the tip
reading is 63/65 — the mismatch this claim counts.

**After.** One rekey batch at the pre-rekey tip, covering EXACTLY the monitor's
uncredited set at that revision (no section added by hand, no section dropped);
the landed tip reads `credited=65/65` with `box3_full_page=true`, i.e. the
record's claim and the monitor agree at the revision the record names.

Counting commands (pasteable; after-state at the landing rev):

```sh
python3 -I -X utf8 tools/coldread-precheck-portable.py --repo . --rev <LANDING_REV> \
  --work <scratch> --out .ufo/evidence/round-77/coldread-after-r77.json | tail -1
python3 -c "import json;d=json.load(open('.ufo/evidence/round-77/coldread-after-r77.json'))['measure'];print('covered=%d/%d box3_full_page=%s'%(d['sections_covered'],d['sections_total'],d['box3_full_page']))"
```

Expected after-state: `COLDREAD_PORTABLE rev=<LANDING_REV> credited=65/65 …`
and `covered=65/65 box3_full_page=True`; exit 0.

**Kill rule (frozen).** C2 fails if (i) the base reading is not `63/65` with
`box3_full_page=false` (the do-nothing control reaches the after-state);
(ii) the landing-tip reading is not `65/65` / `box3_full_page=true`;
(iii) the rekey plan's section set differs from the monitor's uncredited set at
the pre-rekey tip; (iv) any lane content commit lands after the rekey commit
(the rekey is the landing tip); or (v) any rekey entry's inputs are not
byte-identical at the pin (the rebind's own exit 0 plus `REBIND OK`).

## No-harm and separability monitors

- Scored axes at base: depth 10, calibration 8, freshness 9. No axis score
  row is edited by either claim; the SCORECARD gains records only.
- The standing six-row wave sweep (`tools/wave-reconcile.py --manifest
  tools/wave-reconcile.json --extra-root fleet=…`) must keep reading
  `WAVE_RECONCILE: rows=6 met=6 unexpected=0` at the landing tip.
- The selfstate sweep (`tools/selfstate-freshness.py --manifest
  tools/selfstate-freshness.json`) must keep reading `SELFSTATE: rows=20
  match=18 stale=2 unexpected=0` at the landing tip; its instrument and
  manifest are untouched this round.
- `corpus/SOURCES.md` census (`scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi`) must exit 0 before and after.
- C1 edits exactly two files; C2 edits only the ledger plus round-77 evidence.
  Neither claim's counter reads the other's files.

## coldread_forecast (criterion 110/115)

Planned monitored edits: `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `tools/wave-reconcile.py`,
`tools/wave-reconcile-mutants.spec`. Measured pre-data with the lane's own
forecast instrument:

```
python3 -I -X utf8 tools/rekey-cost.py --edit SCORECARD.md --edit LOG.md \
  --edit corpus/QUALITY.md --edit corpus/SOURCES.md \
  --edit tools/wave-reconcile.py --edit tools/wave-reconcile-mutants.spec
→ REKEY_COST sections=65 planned=6 at_risk=14 predicted_lost=14
```

Receipt `.ufo/evidence/round-77/rekey-cost-full-r77.txt`. The forecast's
`predicted_lost=14` is priced into this round: the single end-of-round rekey
batch covers the monitor's measured uncredited set at the pre-rekey tip (the
base reading already carries 2 of them: `## Standing rules` and
`## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`).

## Routed defects this round pays (round-76 closure §6; not claims)

1. **§6.1 cold-read receipt scope** — paid by C2 (tip re-run + rekey) plus an
   append-only correction of the mislabelled "at the landing tip
   (`b2b0f82a`)" sentence.
2. **§6.2 selftest receipts name no revision** — every selftest receipt this
   round carries the measured tool sha256 and rev; the C1 tallies name the
   tool sha.
3. **§6.3 lesson sweep sentence carries no pointer** — the round-77 lesson
   cites one combined tip receipt for each standing sweep.
4. **§6.4 range notation** — the round-77 report writes the base revision and
   an explicit inclusive range, never a bare count from a non-base revision.
5. **§6.5 carried items** — the two bash-instrument gaps
   (`MUTATE_SELFTEST: 107/107`, `REGRESSION: PASS (cases=10 …)`) stay carried
   with a written reason (widening the selfstate runner past `python3 -I` is a
   tool change that needs its own before/after and a frozen tuple table; it
   does not fit this round's claim cap), and the 17-of-44 registry gap stays
   carried with the same reason; both are named in the report and the lesson.
