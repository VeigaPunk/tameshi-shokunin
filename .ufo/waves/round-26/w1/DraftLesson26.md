# DraftLesson26 — draft of `corpus/lessons/round-26.md` (corrected against the landed corpus)

Seat: `TameshiR26.DraftLesson26` (scribe; axes calibration, depth). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Date: 2026-10-22. Lane base `d4140796f4e48e8ec81b793facba73fbd03b4443`; contract frozen at `622d31d90b1fbc55c56e91a2b012bc18d6f1421a`; integration at `a08e85c5d7f899e8a5992e20517edb1a380d79eb`.

## Verdict

The fenced draft of `corpus/lessons/round-26.md` is below, in the shape of `corpus/lessons/round-25.md`
(`## Claims`, `## Gate`, `## Mistakes`, `## Wave findings routed forward`, `## Routed items 4–5
disposition`, `## After measurement`). It is **corrected** against what the L1 has since landed, so
that it no longer contradicts the corpus: the two SOURCES rows now match the landed rows
`corpus/SOURCES.md:97-98`, and the after-measurement values now come from the landed receipts rather
than placeholders. I edited no lane file except this report; I ran no gate, selftest or sweep inside
the lane repo; I ran no `jj` command; I ran no git write command.

## Correction notice (why this file was rewritten)

My first version of this draft followed the wave brief for S089 and named
`https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/` with a
`<<QUOTE PENDING>>` marker. Seat `DraftSourcesRows` told me the L1 had already landed both rows
(`40a12bf`) and that the brief's URL is wrong for two independent reasons:

- the supported-mutators page is **already row S052** (`corpus/SOURCES.md:61`), so a second row on
  it is census error **E04 within S052's scope** (validation exit 1) or a W04 duplicate-URL warning
  across scopes. Seat `DraftSourcesRows` measured the three shapes on `/tmp` copies: same scope
  without a `supersedes` marker → **E04, exit 1**; different scope → **W04 only, exit 0**; same
  scope with `teaches` opening `supersedes S052` → **exit 0**. The L1 landed a different Stryker
  page instead — *equivalent mutants*.
- the brief's `used-by` path `knowledge/mutation-case-kumitate-cite-check.md` is census **E11**,
  because `used-by` resolves from the lane root and must be
  `corpus/knowledge/mutation-case-kumitate-cite-check.md`.

Both defects were mine: I copied the brief's URL into the draft without checking the census. The
draft below now carries the landed rows. Read-only census check by seat `DraftSourcesRows` against
the real root, `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` →
exit 0, lane `ok`, only the seven pre-existing W04s (S047, S048, S075–S078, S081); none from
S088/S089.

## Landed state and supersession (read-only)

The L1 has already landed the lesson, so this draft is now an audit artifact rather than pending
work:

- `40a12bf` — content landing: the ninth-case entry, S088/S089, the SKILL survivor table, the
  registry source fix, QUALITY 51–52, PROVINCE/README appends, the round-25 amendment-3
  corrections, the refreshed `verified-at`, SCORECARD/LOG/**lesson**, and the wave-1 evidence.
- `d2206cd` — SCORECARD measured results for C1 and C2 at `40a12bf`, with after receipts.
- `2b064cf` — the `mte-interop-check` registry row now uses the clone's own fleet mirror
  (`registry-check` flagged the live fleet root as non-hermetic), plus the harmed monitor receipts.
- `corpus/lessons/round-26.md` is landed; its `## After measurement` section currently reads
  "Filled after wave 2".

The landed lesson is **not** a copy of this draft: it carries wave-2 material this seat never saw
(the equivalent-mutant finding from seat `CriticEquivalence`, the `K_FENCE_TILDE` witness
correction from `ReviewPredictions`, the mutator-family mapping from `OpenStrykerMutators`, the
counter weakenings from `MutateC1Counter` and `CriticC1`/`CriticC2`, the registry-row landing
defect from `RegistryCheck`, and the runner/interop weakenings from `MutateInteropLegSet`,
`MutateRunnerSelftest` and `ReviewMteLeg9`). The delta list is below.

## What I read (provenance)

- `.ufo/evidence/round-26/contract.json` (frozen claims C1/C2, bounds, counters).
- `.ufo/evidence/round-26/c1-measure.py`, `c2-measure.py` (frozen counter code; C2 item checks at
  `:38-52` item1, `:54-70` item2, `:73-95` item3, `:97-113` main).
- `.ufo/evidence/round-26/c1-before.stdout` (8 legs, exit 1), `c2-before.stdout` (3/3 mismatches,
  exit 1), `census-start.stdout`/`.exit`, `before-rev.txt`.
- `.ufo/evidence/round-26/cite-check/cite-check.defects.spec` (10 defects, 5 kill-aimed / 5
  hole-aimed), `predictions.json` (5 KILLED / 5 SURVIVED predicted, control 62/62), `sweep/sweep.txt`
  (MUTATE_TOOL sha `d22c4025…`, control GREEN, 5 killed / 5 survived, kill-rate 50 %, `MUTATE_RESTORE: OK`),
  `sweep/results.tsv`, `sweep/evidence/*.out`, `regression-worktree.stdout`.
- `.ufo/evidence/round-26/after/c1-measure-40a12bf.stdout` (`C1_DEPTH: recorded_cases=9
  wired_legs=9 depth_score=9`, exit 0), `after/commandD-40a12bf.stdout` (`recorded_cases=9
  depth_score=9`), `after/c2-measure-40a12bf.stdout` (three `RESOLVED` lines, `C2_RECORD:
  mismatches=0/3`, exit 0), `after/mte-check-a08e85c.stdout` (`MTE_INTEROP: PASS
  legs_conforming=9/9`), `after/mte-selftest-a08e85c.stdout` (`MTE_SELFTEST: 17/17 pass`),
  `after/monitor-harmed-{a08e85c,d2206cd,2b064cf}.json` (each `calibration_restraint_score = 6`,
  `box3_full_page = false`).
- `tools/mutate-and-run.sh:87-95,629,1082,1145,1372-1381,1424-1427,1955`;
  `tools/mte-interop.py:78,318`; `tools/registry.json:1001-1020`; `SKILL.md:2086-2101`;
  `corpus/SOURCES.md:61,97-98` and the round-26 lookup footer; `SCORECARD.md:72-73,1273-1317`.
- `corpus/lessons/round-25.md` (shape), `corpus/lessons/round-25-verifier-spotcheck.md:189-206`
  (routed items 1–5), `corpus/QUALITY.md` (criteria 1–50, plus the landed 51–52), the landed
  `corpus/lessons/round-26.md`, `corpus/knowledge/mte-report-interop.md` (base `d414079` and
  current `verified-at` line).
- Read-only sibling: `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show
  1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs` → sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines, 126 735 bytes
  (equal to the contract pin and to the landed S088 anchor).

## The fenced draft (corrected)

```markdown
# Round 26 — ninth recorded case and round-25 record repair

author: TameshiR26 (L1, attempt 1)
Date: 2026-10-22. Base `d4140796f4e48e8ec81b793facba73fbd03b4443`. Contract frozen at
`622d31d90b1fbc55c56e91a2b012bc18d6f1421a` (before any mutant ran and before any edit to the files
the C2 counter reads); integration at `a08e85c5d7f899e8a5992e20517edb1a380d79eb`.

## Claims

- **C1 depth (learning).** The ninth recorded mutation-ledger leg `js-cite-check`:
  kumitate `scripts/cite-check.mjs` at kumitate rev
  `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` (blob sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines, 126 735 bytes,
  mode 100755; unchanged at kumitate master). The spec (10 defects: 5 kill-aimed, 5 hole-aimed) and
  the predictions (5 KILLED, 5 SURVIVED) were committed at `622d31d` before any mutant ran; the
  control was GREEN, exit 0, 62/62 hermetic cases, `VERDICT: PASS`. The measured sweep is 5/10
  killed, kill-rate 50 %, 10/10 verdict predictions held (`sweep/results.tsv`, `sweep/sweep.txt`).
  Counter `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV`: before
  `C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8`, exit 1
  (`.ufo/evidence/round-26/c1-before.stdout`); target
  `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0. The counter reads the runner's
  ledger comment lines (`tools/mutate-and-run.sh:87-95`; the ninth is `:95`) and requires each
  recorded leg to be wired: spec heredoc, regression replay call, leg-check entry, and a table line
  whose defect and killed counts match the recorded table. Scorecard command D
  (`SCORECARD.md:72-73`) reads `recorded_cases=9 depth_score=9` at the measured commit.
  Bound (contract, `claims.C1.bound`): the counter checks that the leg is *recorded and wired*, not
  that the recorded table equals a real sweep. That claim rests on the regression companion, not on
  the counter: `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9)`
  and, for the leg, `REGRESSION_CASE js-cite-check: PASS` and
  `REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5
  inconclusive=0 flips=0` (`.ufo/evidence/round-26/cite-check/regression-worktree.stdout`).
- **C2 calibration (record repair).** Mismatches between the lane's own record and the repo bytes
  for the three fixed labels routed by the round-25 outside spot-check
  (`corpus/lessons/round-25-verifier-spotcheck.md:189-199`, R25-SPOT-1..3). Counter
  `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV`: before
  `C2_RECORD: mismatches=3/3`, exit 1 (`.ufo/evidence/round-26/c2-before.stdout`); target
  `C2_RECORD: mismatches=0/3`, exit 0. Item 1 is resolved at `a08e85c`: `tools/registry.json:1001`
  and `:1011` hold the active rows `mte-interop-selftest` and `mte-interop-check`, and
  `SKILL.md:2101` holds the table row that starts ``| `tools/mte-interop.py` |``. Items 2 and 3 are
  prose repairs of the lane's own record (the round-25 SCORECARD block and the round-25 lesson
  `## Claims`; the `verified-at` line of `corpus/knowledge/mte-report-interop.md`).
  Numeric calibration stays 8 (lane cap): this is a record repair, not a numeric move.
  Bound (contract, `claims.C2.bound`): the population is three fixed labels; items 4 and 5 of the
  same routing are dispositioned below, not counted.

No-harm companions named by the contract: `bash tools/mutate-and-run.sh --regression` →
`REGRESSION: PASS (cases=9 passed=9)`;
`uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root
/home/vgpnk/Projects/shokunin` → `MTE_INTEROP: PASS legs_conforming=9/9`, exit 0
(`.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`); the same tool's `--selftest` →
`MTE_SELFTEST: 17/17 pass`, exit 0 (`.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout`);
`python3 tools/registry-check.py --rev REV` and `scripts/sources-census.sh validate` are recorded
under `## After measurement`.

## Gate

Admit candidates:

1. `corpus/knowledge/mutation-case-kumitate-cite-check.md` — the ninth knowledge entry. Admit: the
   pin, the pre-registered spec and predictions, the measured sweep and its per-defect evidence are
   committed under `.ufo/evidence/round-26/cite-check/`; the entry opens with `source:`,
   `verified-at:`, `recheck:` and `ground:` (QUALITY 10) and states the survivors as
   unproven-equivalent pending off-suite witnesses, not as equivalents.
2. The ninth leg `js-cite-check` in the runner and the interop. Admit: the ledger comment line
   (`tools/mutate-and-run.sh:95`), the recorded table `TABLE_CITECHECK` (`:629`, 10 ids, 5 KILLED),
   the embedded spec heredoc (`:1082`), the leg's own check (`:1145`), the regression replay call
   and its suite string (`:1424-1427`), the leg-check entry
   `'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5'` (`:1955`), the interop's table map
   (`tools/mte-interop.py:78`) and its nine-leg SETUP message (`:318`), the two active registry rows
   (`tools/registry.json:1001`, `:1011`) and the SKILL table row (`SKILL.md:2101`).
3. The two counters `.ufo/evidence/round-26/c1-measure.py` and `c2-measure.py`. Admit: both were
   frozen at `622d31d`, before any mutant ran and before any edit to the files the C2 counter reads,
   and each states its population, its exit map and its bound in its own docstring.

Reject:

- Reading `C1_DEPTH: depth_score=9` as evidence that the recorded table equals a real sweep. The
  counter checks recording and wiring only (contract `claims.C1.bound`); the table-versus-sweep
  claim rests on the regression companion's `match=10/10 … flips=0` line.
- Reading `MTE_INTEROP: PASS legs_conforming=9/9` as nine independent measurements, as a Stryker
  run, as Stryker mutators, or as producer authentication. With the 1:1 status mapping the official
  score equals the runner's integer kill rate by construction (round-25 seat C2Tautology); the
  load-bearing checks are `ledger` and `per_mutant`, and on all nine legs they read
  `per_mutant=ok failed=none`.
- Reading `C2_RECORD: mismatches=0/3` as closure of the round-25 spot-check, or of the class. The
  counter's population is three fixed labels (`c2-measure.py:38-95`); items 4 and 5 are
  dispositioned below and are not counted (QUALITY 50: counts never stand in for items).
- Reading the 62/62 control as a determinism proof. It is one control run in the sweep
  (`sweep/sweep.txt`, `CONTROL: GREEN`), not a repeated-control sample with a finite sample size
  (QUALITY 11); the round-18 case 8 entry had eight pristine runs, this case has one.
- Reading the five survivors as equivalent mutants. Equivalence is undecided for all five here; a
  survivor needs an off-suite witness or an explicit equivalence argument (S089's vendor statement:
  there is no definitive way to find and ignore equivalent mutants). The probes are open below.
- Reading "10/10 verdict predictions held" as "the predicted case killed each mutant". A verdict
  prediction is KILLED/SURVIVED; the witness case is a separate reading. It differs for at least
  one mutant: `K_FENCE_TILDE` was predicted to die on the marker-symmetric case (a `~~~` fence
  scoring like a backtick fence), and it died instead on "fence content is never tokenized (by
  design, kept)" and "R16 regression: fence content is never tokenized under line-local pairing"
  (`sweep/evidence/K_FENCE_TILDE.out:27,39`).

Flip condition: an independently retained, applicable execution or authority record.

S088 opened 2026-10-22 by the L1 (`git -C kumitate-shokunin show
1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`; blob sha256 equal to the pin,
unchanged at kumitate master; re-opened by seats OpenCiteCheckPin and the five probe seats).
Located quote, `:75-76`: "Never reads --src or --self; MUST PASS in any repo state. This is the
whole of --selftest." Landed row `corpus/SOURCES.md:97` — kind code, tier A, status mined, opened
2026-10-22, recheck 180d, used-by `corpus/knowledge/mutation-case-kumitate-cite-check.md`.

S089 opened 2026-10-22 by the L1 with an ordinary fetch
(`https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/`, html sha256
`bc572676…e04d`; also opened by seat OpenEquivalentSource). Located quote, the paragraph
immediately after the `10 ** 0` example: "There is no definitive way for Stryker to find and ignore
them. There is currently also no way yet to mark them to be ignored." Landed row
`corpus/SOURCES.md:98` — kind docs, tier A, status mined, opened 2026-10-22, recheck 180d, used-by
`corpus/knowledge/mutation-case-kumitate-cite-check.md`.

Both new rows start mined, tier A, recheck 180d. No existing row's status, recheck or used-by
changes: S052 (Stryker supported mutators) was re-opened by seat OpenStrykerMutators and left
unchanged; the Madeyski et al. 2014 preprint (tier B) was screened and not added. Bounded lookup:
identified 4, screened 4, included 2, excluded 2. Next unused id: S090.

Open item for the L1, from seat `DraftSourcesRows`: S052's anchor carries a stale build stamp
(records 2026-10-19; the page is served with a 2026-10-21 build stamp, site-wide, since S089's page
carries the identical stamp). The content still supports S052's `teaches` — all six mutator families
and their support values were re-extracted from the served `## Support` table and each is unchanged
— so this is anchor drift, not a wrong row, and it is fixable only as a new correction row. If the
L1 prefers the brief's original URL instead of the landed one, the shape that satisfies the census is
a row on that URL whose `teaches` opens `supersedes S052` (same scope with that marker: exit 0;
same scope without it: E04, exit 1; different scope: W04 only).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| A landed knowledge entry's `verified-at` line names an earlier run of the instrument than the one measured at the recorded revision: provenance drift, the record asserting a result of bytes that are not the bytes that produced it | The line at base `d414079` (and unchanged at `77302fa`) reads `verified-at: 2026-10-22; C2 counter executed at 09dc114 (tool sha256 8c24255c…): PASS 8/8, exit 0; selftest 16/16, exit 0; official metrics per leg observed (lines in .ufo/waves/round-25/w1/DraftKnowledge.md)` (`corpus/knowledge/mte-report-interop.md`, line 2), while the tool measured in round 25 at `77302fa` was sha256 `8269b82f…` with selftest 17/17 (`.ufo/evidence/round-25/after/c2-selftest.stdout`); the two digests are of the same file `tools/mte-interop.py` at two revisions, and the header names neither the revision of the tool it ran nor a receipt that exists at the revision | **None of the landed criteria caught it.** QUALITY 10 requires a `verified-at:` field, not that its digest is the measured bytes; QUALITY 26 governs receipts, and the round-25 receipts were current — the header was the stale part; QUALITY 24 is the closest rule (an outcome that changes is re-pinned in the same round and "every mention of the old outcome is swept in that round") and it did not catch this, because the sweep is a manual step and nothing compares the header's digest with the file at the revision. New QUALITY 51 (drafted this round from this mistake) makes it checkable | Fix = the C2 counter's third item, `R25-SPOT-3` (`.ufo/evidence/round-26/c2-measure.py:73-95`): the `verified-at` line must name `tool sha256 <hex>` with `<hex>` a prefix of `sha256(tools/mte-interop.py)` at the measured revision, must name `selftest N/N`, and must name a backticked `.stdout` receipt that exists at that revision and carries `MTE_SELFTEST: N/N pass`. Shown able to fail: at base `d414079` the counter prints `C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=8269b82f213e; no named .stdout receipt at the revision carries the verified-at selftest count)` and `C2_RECORD: mismatches=3/3`, exit 1 (`.ufo/evidence/round-26/c2-before.stdout`, lines 4–5). The repair names the current tool's digest and committed receipts of the run that produced it; the false line and both digests stay in the record (QUALITY 26, QUALITY 35). |

## Wave findings routed forward (not claimed this round)

- The five survivors of the ninth leg are open work, not equivalents: `S_OOR_EDGE` (line-range check
  accepts one line past the end of file), `S_STRICT` (strict mode promotes warnings only at two or
  more), `S_EMPTY_GUARD` (the verdict drops only the scanned-files guard), `S_USAGE` (usage exit 64
  becomes 65), `S_PIN_INCLUDES` (a content pin is accepted anywhere inside the digest). Each needs
  an off-suite witness or an explicit equivalence argument; probe seats are open in wave 2.
- `K_FENCE_TILDE` was killed by a case other than the predicted one (see `## Gate`). The
  prediction-versus-witness reading for all ten mutants belongs to the knowledge entry.
- The `verified-at` repair and the counter's shape constrain each other: item `R25-SPOT-3` accepts
  exactly one line beginning `verified-at:` and reads the digest from that line, so the repair
  cannot be an appended erratum alone — the single header line has to carry the measured digest,
  and the false text, both digests and both revisions are preserved in an appended erratum
  (QUALITY 26, QUALITY 35). The L1 owns that wording; the counter stays frozen.

## Routed items 4–5 disposition

- **Item 4** (`corpus/lessons/round-25-verifier-spotcheck.md:200-203`): still open from the lane's
  own routing — MtGuardGaps' 17 surviving weakenings of `tools/command-binding.py`, the 14
  re-attack FINDING rows, round-24 spot-check items 2–4, and emitted reports that name targets
  without a lane/revision pin (SiblingOverlap). Disposition: <<PENDING — wave 2: owner, check and
  evidence pointer per item>>. Not counted by the C2 counter (three fixed labels only).
- **Item 5** (`corpus/lessons/round-25-verifier-spotcheck.md:204-206`): seat bounds — ReReplay14 ran
  `jj log` at the fleet root and ReOutputComplete ran `jj st` in the lane; wave contexts must name
  `jj` beside git. Disposition: this round's wave context names it explicitly ("Never run ANY `jj`
  command anywhere"), and the rule is captured by new QUALITY 52 (drafted this round).
  <<PENDING — L1 to confirm the context text is carried into wave 2>>.

## After measurement

At `40a12bf34f34977a5789e81b930303b97c4038d1`, over a clone:

- C1: `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0 — all nine legs `WIRED`
  (`.ufo/evidence/round-26/after/c1-measure-40a12bf.stdout`). Command D gives the same score:
  `recorded_cases=9 depth_score=9` (`.ufo/evidence/round-26/after/commandD-40a12bf.stdout`).
  Companion: `REGRESSION: PASS (cases=9 passed=9)` with
  `REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5
  inconclusive=0 flips=0` (`.ufo/evidence/round-26/cite-check/regression-worktree.stdout`).
- C2: `C2_ITEM R25-SPOT-1: RESOLVED`, `C2_ITEM R25-SPOT-2: RESOLVED`, `C2_ITEM R25-SPOT-3:
  RESOLVED`, `C2_RECORD: mismatches=0/3`, exit 0
  (`.ufo/evidence/round-26/after/c2-measure-40a12bf.stdout`).
- Interop: `MTE_INTEROP: PASS legs_conforming=9/9`, exit 0, every leg `per_mutant=ok failed=none`;
  selftest `MTE_SELFTEST: 17/17 pass`, exit 0.
- Negative control retained: the counter over a clone at base `d414079` still prints
  `C2_RECORD: mismatches=3/3`, exit 1 (`.ufo/evidence/round-26/c2-before.stdout`) — the fix can
  fail.
- No-harm: the strict cold-read monitor is harmed at three landed revisions and the harmed
  intermediates are retained — `monitor-harmed-a08e85c.json`, `monitor-harmed-d2206cd.json`,
  `monitor-harmed-2b064cf.json`, each reading `calibration_restraint_score = 6` and
  `box3_full_page = false`. <<PLACEHOLDER — the L1's final restored monitor, registry-check and
  census receipts at the closing revision; this seat observed only the three harmed receipts and
  claims no restored value.>>
```

## Delta: the landed lesson vs this draft (for the L1; no lane file was edited by me)

The landed `corpus/lessons/round-26.md` (at `40a12bf`) already contains this draft's substance and
more. Where it differs, the landed text wins and this draft is the superseded artifact:

| Section | Landed text | This draft |
|---|---|---|
| `## Claims` | Shorter; names the two counters and the before/target values | Longer; adds the contract bounds, the runner/table/replay anchors, the no-harm companions |
| `## Gate` admits | Entry, ninth leg, interop mapping, two counters, QUALITY 51–52 | Entry, ninth leg, two counters (QUALITY 51–52 named in the landed text only) |
| `## Gate` rejects | Equivalent mutant (`S_EMPTY_GUARD`), the risky-prediction reading (`K_FENCE_TILDE`), the ten edits vs Stryker mutators, `depth_score=9` vs table truth, C2 0/3 vs class closure | Score-equals-kill-rate by construction, the counter's fixed population, the single control vs determinism, survivors vs equivalence, verdict-vs-witness |
| `## Gate` sources | S088 and S089 with the landed quotes, both rows `corpus/SOURCES.md:97-98`, lookup 4/4/2/2, S052 re-opened and unchanged | Same rows and quotes after this correction; the lookup counts and the S052 note now match |
| `## Mistakes` | Two rows: the stale `verified-at` (captured-by "none at the time"; QUALITY 51) and the registry row landed in a shape the registry gate refuses (caught by `registry-check.py` `SOURCE_RE`) | One row: the stale `verified-at`, with the same captured-by reasoning; the registry-row defect is a wave-2 finding this seat did not see |
| `## Wave findings routed forward` | Five bullets (kumitate holes, interop leg-set guard, C1/C2 counter gaming, runner summary-loop defect, drift sentinel) | Two bullets (the five survivors, the `K_FENCE_TILDE` witness); the rest arrived in wave 2 |
| `## Routed items 4–5` | Item 4 open and explained with seat evidence; item 5 closed in the wave contexts | Item 4 and item 5 with placeholders for the owner/check/pointer text |
| `## After measurement` | "Filled after wave 2" | Filled from the landed receipts at `40a12bf` for C1, C2, the interop and the negative control, with the monitor paragraph left as a placeholder |

## Findings for the judge (conflicts, stated verbatim)

1. **The wave brief's S089 was unusable, and my first draft copied it.** The brief named
   `https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/`, which is
   already row S052 (`corpus/SOURCES.md:61`): a second row on it is census error E04 within S052's
   scope (validation exit 1) or a W04 duplicate-URL warning. The L1 landed *equivalent mutants*
   instead (S089). The brief's `used-by` path `knowledge/mutation-case-kumitate-cite-check.md` is
   census E11, because `used-by` resolves from the lane root and must be
   `corpus/knowledge/mutation-case-kumitate-cite-check.md`. A seat that opens a source must read
   the census's rules before it drafts a row; the brief is not a substitute for the census.
2. **QUALITY 35 versus the frozen C2 counter.** QUALITY 35 (`corpus/QUALITY.md:262-279`) says a
   correction to a landed entry "is an appended, dated erratum … The original bytes are never
   rewritten in place". The frozen counter's item `R25-SPOT-3`
   (`.ufo/evidence/round-26/c2-measure.py:73-95`) reads: `lines = [l for l in kn.splitlines() if
   l.startswith("verified-at:")]` … `if len(lines) != 1: return ["expected one verified-at line,
   found %d" % len(lines)]`, and it takes the digest from that one line. A repair that only appends
   an erratum leaves the stale digest in the only `verified-at:` line and the counter still reports
   MISMATCH; a repair that appends a second `verified-at:` line is refused by the counter. The
   smallest safe correction is therefore both: the single header line carries the measured digest,
   and the appended erratum preserves the false text and both digests. The counter stays frozen.
3. **No criterion caught the mistake.** The `## Mistakes` row records that QUALITY 10, 24 and 26
   each come close and none fires, so the capture is the new QUALITY 51, not a landed criterion. The
   landed lesson says the same ("none at the time"); my seat's independent reading reached it from
   the counter code rather than from the landed text.
4. **The control is a single run.** The ninth leg's control is one GREEN run of 62/62 cases
   (`sweep/sweep.txt`), against case 8's eight pristine runs. Reading it as determinism is rejected
   (QUALITY 11). The landed lesson does not make this reading; the draft keeps it.
5. **One prediction held on the verdict but not on the witness case.** `K_FENCE_TILDE` died on
   "fence content is never tokenized (by design, kept)" and "R16 regression: fence content is never
   tokenized under line-local pairing" (`sweep/evidence/K_FENCE_TILDE.out:27,39`), not on the
   predicted marker-symmetric case. The landed lesson carries this from seat `ReviewPredictions`;
   the draft reached it from the sweep evidence.
6. **The after-measurement paragraph of the landed lesson is still unfilled** ("Filled after wave
   2") while the receipts exist for C1 and C2 at `40a12bf` and three harmed monitor receipts are
   retained. This seat did not fill it (the lesson is the L1's file), and claims no restored
   monitor value.
7. **S052's anchor stamp is stale, and the landed lesson does not mention it.** S052 records the
   supported-mutators page as fetched 2026-10-19; the page is now served with a 2026-10-21 build
   stamp, and S089's page carries the identical stamp, so the rebuild is site-wide (seat
   `DraftSourcesRows`, re-extracting all six families and their support values from the served
   `## Support` table: each unchanged, so S052's `teaches` still holds). The landed lesson says
   S052 was "re-opened … and left unchanged"; that is true of the row's content and status, but the
   anchor's build stamp is now stale. Anchor drift is fixable only as a new correction row, and it
   is the L1's call whether to spend a row on it this round.

## Out of scope (not touched by this seat)

- No lane file was edited except this report. `corpus/lessons/round-26.md` is the L1's file and is
  already landed; this draft does not modify it.
- No product file was edited: `tools/mutate-and-run.sh`, `tools/mte-interop.py`,
  `tools/registry.json`, `SKILL.md`, `corpus/SOURCES.md`, `SCORECARD.md` and
  `corpus/QUALITY.md` are unchanged by me.
- No gate, selftest or sweep was run inside the lane repo. The kumitate sibling was read with
  `git show` only; no `jj` command was run anywhere; no git write command was run in the lane.
- The C2 items 2 and 3, the entry text, the S088/S089 rows and QUALITY 51–52 belong to seats
  `DraftScorecard`, `DraftLesson25Correction`, `DraftEntry`, `DraftSourcesRows` and
  `DraftQuality`, and to the L1's landing commit; this seat drafted the lesson shape and the
  corrections above.

## Tools

None installed or upgraded this session. No pacman, uv, npm, cargo or binary install was needed; the
work used files already in the lane and one ordinary web fetch (Stryker's supported-mutators page),
whose URL the landed corpus does not use.
