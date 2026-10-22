# DraftLesson26 — draft of `corpus/lessons/round-26.md`

Seat: `TameshiR26.DraftLesson26` (scribe; axes calibration, depth). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Date: 2026-10-22. Lane base `d4140796f4e48e8ec81b793facba73fbd03b4443`; contract frozen at `622d31d90b1fbc55c56e91a2b012bc18d6f1421a`; integration at `a08e85c5d7f899e8a5992e20517edb1a380d79eb`.

## Verdict

One fenced draft of `corpus/lessons/round-26.md` is below, in the shape of `corpus/lessons/round-25.md`
(sections `## Claims`, `## Gate`, `## Mistakes`, `## Wave findings routed forward`, `## Routed items 4–5
disposition`, `## After measurement`). Every number in it is taken from a file or a receipt I opened
this session; the after-measurement numbers are left as placeholders because the after state does not
exist yet. I edited no lane file except this report; I ran no gate, selftest or sweep inside the lane
repo; I ran no `jj` command; I ran no git write command.

## What I read (provenance)

- `.ufo/evidence/round-26/contract.json` (frozen claims C1/C2, bounds, counters).
- `.ufo/evidence/round-26/c1-measure.py`, `c2-measure.py` (frozen counter code; the C2 item checks are
  at `:38-52` item1, `:54-70` item2, `:73-95` item3, `:97-113` main).
- `.ufo/evidence/round-26/c1-before.stdout` (8 legs, exit 1), `c2-before.stdout` (3/3 mismatches,
  exit 1), `census-start.stdout`/`.exit`, `before-rev.txt`.
- `.ufo/evidence/round-26/cite-check/cite-check.defects.spec` (10 defects, 5 kill-aimed / 5
  hole-aimed), `predictions.json` (5 KILLED / 5 SURVIVED predicted, control 62/62), `sweep/sweep.txt`
  (MUTATE_TOOL sha `d22c4025…`, control GREEN, 5 killed / 5 survived, kill-rate 50 %, `MUTATE_RESTORE: OK`),
  `sweep/results.tsv`, `sweep/evidence/*.out`, `regression-worktree.stdout`.
- `.ufo/evidence/round-26/after/mte-check-a08e85c.stdout` (`MTE_INTEROP: PASS legs_conforming=9/9`,
  exit 0), `after/mte-selftest-a08e85c.stdout` (`MTE_SELFTEST: 17/17 pass`, exit 0).
- `tools/mutate-and-run.sh:87-95,629,1082,1145,1372-1381,1424-1427,1955`;
  `tools/mte-interop.py:78,318`; `tools/registry.json:1001-1020`; `SKILL.md:2086-2101`.
- `corpus/lessons/round-25.md` (shape), `corpus/lessons/round-25-verifier-spotcheck.md:189-206`
  (routed items 1–5), `corpus/QUALITY.md` (criteria 1–50), `corpus/SOURCES.md` (table shape, rows
  S086/S087, "Next unused id: S088"), `corpus/knowledge/mte-report-interop.md` (base and current
  `verified-at` line).
- Read-only sibling: `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show
  1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs` → sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines, 126 735 bytes
  (matches the contract pin).
- One external page, ordinary fetch, no challenge: `https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/`,
  opened 2026-10-22. Located quote (24 words): "All Stryker versions support a variety of different
  mutators. We've aligned on a standard naming scheme so it is easy to switch and compare
  implementations." Located at the page's `## Support` heading lead paragraph. The row itself
  (S089) is opened and written by seat `DraftSourcesRows`; my opening is a cross-check, not a second
  admission.

## The fenced draft

```markdown
# Round 26 — ninth recorded mutation leg and round-25 record repair

author: TameshiR26 (L1, attempt 1)
Date: 2026-10-22. Base `d4140796f4e48e8ec81b793facba73fbd03b4443`. Contract frozen at
`622d31d90b1fbc55c56e91a2b012bc18d6f1421a` (before any mutant ran and before any edit to the files
the C2 counter reads); integration at `a08e85c5d7f899e8a5992e20517edb1a380d79eb`.

## Claims

- **C1 depth (learning).** The ninth recorded mutation-ledger leg `js-cite-check`:
  kumitate `scripts/cite-check.mjs` at kumitate rev
  `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` (blob sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines, 126 735 bytes,
  mode 100755). The spec (10 defects: 5 kill-aimed, 5 hole-aimed) and the predictions (5 KILLED,
  5 SURVIVED) were committed at `622d31d` before any mutant ran; the control was GREEN, exit 0,
  62/62 hermetic cases, `VERDICT: PASS`. The measured sweep is 5/10 killed, kill-rate 50 %,
  10/10 verdict predictions held (`sweep/results.tsv`, `sweep/sweep.txt`).
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

No-harm companions named by the contract and their status at `a08e85c`:
`bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9)`;
`uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root
/home/vgpnk/Projects/shokunin` → `MTE_INTEROP: PASS legs_conforming=9/9`, exit 0
(`.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`); the same tool's `--selftest` →
`MTE_SELFTEST: 17/17 pass`, exit 0 (`.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout`);
`python3 tools/registry-check.py --rev REV` and `scripts/sources-census.sh validate` are re-run at the
after revision and recorded under `## After measurement`.

## Gate

Admit candidates:

1. `corpus/knowledge/mutation-case-kumitate-cite-check.md` — the ninth knowledge entry. Admit: the
   pin, the pre-registered spec and predictions, the measured sweep and its per-defect evidence are
   committed under `.ufo/evidence/round-26/cite-check/`; the entry opens with `source:`,
   `verified-at:`, `recheck:` and `ground:` (QUALITY 10) and states the five survivors as
   unproven-equivalent pending off-suite probes, not as equivalents.
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
- Reading `C2_RECORD: mismatches=0/3` as closure of the round-25 spot-check. The counter's
  population is three fixed labels (`c2-measure.py:38-95`), not the routing list; items 4 and 5 are
  dispositioned below and are not counted (QUALITY 50: counts never stand in for items).
- Reading the 62/62 control as a determinism proof. It is one control run in the sweep
  (`sweep/sweep.txt`, `CONTROL: GREEN`), not a repeated-control sample with a finite sample size
  (QUALITY 11); the round-18 case 8 entry had eight pristine runs, this case has one.
- Reading the five survivors as equivalent mutants. Equivalence is undecided for all five here; a
  survivor needs an off-suite witness or an explicit equivalence argument (S057 §5.3.1). The probes
  are open below.
- Reading "10/10 verdict predictions held" as "the predicted case killed each mutant". A verdict
  prediction is KILLED/SURVIVED; the witness case is a separate reading. It differs for at least
  one mutant: `K_FENCE_TILDE` was predicted to die on the marker-symmetric case (a `~~~` fence
  scoring like a backtick fence), and it died instead on "fence content is never tokenized (by design, kept)"
  and "R16 regression: fence content is never tokenized under line-local pairing"
  (`sweep/evidence/K_FENCE_TILDE.out:27,39`).

Flip condition: an independently retained, applicable execution or authority record.

S088 opened 2026-10-22 by seat `DraftSourcesRows`: kumitate `scripts/cite-check.mjs` at rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, read with
`git -C kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`.
Locator and located quote (≤ 25 words) are recorded by the seat that opened it; this lesson cites
the row and no claim here rests on its content. Cross-checked independently by this seat, read-only,
on 2026-10-22: the blob hashes to
`40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f` and is 2537 lines, so the row's
pin and the contract's pin are the same bytes.

S089 opened 2026-10-22 by seat `DraftSourcesRows`:
`https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/` — the official
mutator taxonomy the entry uses to name the operator families of the ten defects. Access date
2026-10-22. Located quote (≤ 25 words), recorded by the opening seat: <<QUOTE PENDING — seat
DraftSourcesRows>>. Independently opened by this seat on 2026-10-22 with an ordinary fetch (no
challenge, no headless browser): the page's lead paragraph under `## Support` reads "All Stryker
versions support a variety of different mutators. We've aligned on a standard naming scheme so it
is easy to switch and compare implementations." (24 words). If the two openings disagree, the
row's own text wins and this sentence is corrected by an appended erratum.

Both rows start mined, tier A, recheck 180d, used by
`corpus/knowledge/mutation-case-kumitate-cite-check.md`. No existing row's status, recheck or
used-by changes. Bounded lookup: identified 2, screened 2, included 2, excluded 0.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| A landed knowledge entry's `verified-at` line names an earlier run of the instrument than the one measured at the recorded revision: provenance drift, the record asserting a result of bytes that are not the bytes that produced it | The line at base `d414079` (and unchanged at `77302fa`) reads `verified-at: 2026-10-22; C2 counter executed at 09dc114 (tool sha256 8c24255c…): PASS 8/8, exit 0; selftest 16/16, exit 0; official metrics per leg observed (lines in .ufo/waves/round-25/w1/DraftKnowledge.md)` (`corpus/knowledge/mte-report-interop.md`, line 2), while the tool measured in round 25 at `77302fa` was sha256 `8269b82f…` with selftest 17/17 (`.ufo/evidence/round-25/after/c2-selftest.stdout`); the two digests are of the same file `tools/mte-interop.py` at two revisions, and the header names neither the revision of the tool it ran nor a receipt that exists at the revision | **None of the landed criteria caught it.** QUALITY 10 requires a `verified-at:` field, not that its digest is the measured bytes; QUALITY 26 governs receipts, and the round-25 receipts were current — the header was the stale part; QUALITY 24 is the closest rule (an outcome that changes is re-pinned in the same round and "every mention of the old outcome is swept in that round") and it did not catch this, because the sweep is a manual step and nothing compares the header's digest with the file at the revision. New QUALITY 51 (drafted this round from this mistake) makes it checkable | Fix = the C2 counter's third item, `R25-SPOT-3` (`.ufo/evidence/round-26/c2-measure.py:73-95`): the `verified-at` line must name `tool sha256 <hex>` with `<hex>` a prefix of `sha256(tools/mte-interop.py)` at the measured revision, must name `selftest N/N`, and must name a backticked `.stdout` receipt that exists at that revision and carries `MTE_SELFTEST: N/N pass`. Shown able to fail: at base `d414079` the counter prints `C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=8269b82f213e; no named .stdout receipt at the revision carries the verified-at selftest count)` and `C2_RECORD: mismatches=3/3`, exit 1 (`.ufo/evidence/round-26/c2-before.stdout`, lines 4–5). The repair names the current tool's digest and a committed receipt of the run that produced it; the false line and both digests stay in the record (QUALITY 26, QUALITY 35). |

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

<<PLACEHOLDER — to be filled by the L1 from receipts at the after revision; do not fill from this
draft.>>

- C1: `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0, at REV, over a clone;
  companion `REGRESSION: PASS (cases=9 passed=9)` with
  `REGRESSION_TABLE js-cite-check: match=10/10 … flips=0`.
- C2: `C2_RECORD: mismatches=0/3`, exit 0, at REV, over a clone, with the three item lines
  `C2_ITEM R25-SPOT-1: RESOLVED` / `-2: RESOLVED` / `-3: RESOLVED`.
- No-harm: strict cold-read monitor, `python3 tools/registry-check.py --rev REV`, and
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` at the after
  revision.
- Negative control: the C2 counter over a clone at base `d414079` must still print
  `C2_RECORD: mismatches=3/3`, exit 1, and one repair reverted in a scratch clone must move the
  count to at least 1 — the fix can fail.
```

## Placeholders the L1 must fill (numbered)

1. `## After measurement` — all five placeholders, from receipts at the after revision, in a clone.
   No number in this section may be copied from this draft.
2. `## Routed items 4–5 disposition` — item 4's per-item disposition (owner, check, evidence
   pointer) and item 5's confirmation that the wave-2 context carries the `jj` prohibition.
3. The S089 located quote, and S088's locator and located quote, from seat `DraftSourcesRows`. The
   two openings must agree; if they do not, the row's text wins and this lesson is corrected by an
   appended erratum.
4. The `verified-at` repair wording (item `R25-SPOT-3`): the single `verified-at:` line carrying the
   measured digest and a committed receipt, plus the appended erratum naming the false text, both
   digests and both revisions.
5. The knowledge entry path `corpus/knowledge/mutation-case-kumitate-cite-check.md` is referenced by
   the runner header comment (`:95`, `:100-105`), `SKILL.md:2092` and the SOURCES rows; if the L1
   renames it, every anchor in this draft moves with it.

## Findings for the judge (conflicts, stated verbatim)

1. **QUALITY 35 versus the frozen C2 counter.** QUALITY 35 (`corpus/QUALITY.md:262-279`) says a
   correction to a landed entry "is an appended, dated erratum … The original bytes are never
   rewritten in place". The frozen counter's item `R25-SPOT-3`
   (`.ufo/evidence/round-26/c2-measure.py:73-95`) reads: `lines = [l for l in kn.splitlines() if
   l.startswith("verified-at:")]` … `if len(lines) != 1: return ["expected one verified-at line,
   found %d" % len(lines)]`, and it takes the digest from that one line. A repair that only appends
   an erratum leaves the stale digest in the only `verified-at:` line and the counter still reports
   MISMATCH; a repair that appends a second `verified-at:` line is refused by the counter. The
   smallest safe correction is therefore both: the single header line carries the measured digest,
   and the appended erratum preserves the false text and both digests. The draft says so; the L1
   must land that wording. The counter itself stays frozen.
2. **No criterion caught the mistake.** The `## Mistakes` row records that QUALITY 10, 24 and 26
   each come close and none fires, so the capture is the new QUALITY 51 (drafted by seat
   `DraftQuality`, `w1/DraftQuality.md`), not a landed criterion. The draft cites QUALITY 51 by
   number as a proposal, not as a landed rule; if the L1 does not land it, the sentence changes.
3. **The control is a single run.** The ninth leg's control is one GREEN run of 62/62 cases
   (`sweep/sweep.txt`), against case 8's eight pristine runs. The draft rejects reading it as
   determinism (QUALITY 11). If wave 2 adds repeated controls, that sentence is superseded by an
   appended erratum.
4. **One prediction held on the verdict but not on the witness case.** `K_FENCE_TILDE` died on
   "fence content is never tokenized (by design, kept)" and "R16 regression: fence content is never
   tokenized under line-local pairing" (`sweep/evidence/K_FENCE_TILDE.out:27,39`), not on the
   predicted marker-symmetric case. The draft says so in `## Gate`; the entry owns the full
   per-mutant table.
5. **Item 5 of the routing is a context rule, not a lane artifact.** `jj` cannot be undone from the
   lane; the disposition is that the context names it, and the rule is captured by QUALITY 52. The
   draft leaves the confirmation open rather than claiming the item closed.

## Out of scope (not touched by this seat)

- No lane file was edited except this report. `corpus/lessons/round-26.md` does not exist yet; the
  L1 creates it from this draft.
- No product file was edited: `tools/mutate-and-run.sh`, `tools/mte-interop.py`,
  `tools/registry.json`, `SKILL.md` and `corpus/SOURCES.md` are unchanged by me.
- No gate, selftest or sweep was run inside the lane repo. The kumitate sibling was read with
  `git show` only; no `jj` command was run anywhere; no git write command was run in the lane.
- The C2 items 2 and 3 (SCORECARD block, round-25 lesson correction, entry `verified-at`) belong to
  seats `DraftScorecard`, `DraftLesson25Correction` and `DraftEntry`; this draft names them and
  does not write them.
- QUALITY 51 and 52 belong to seat `DraftQuality`; S088/S089 to seat `DraftSourcesRows`; the entry
  to seat `DraftEntry`.

## Tools

None installed or upgraded this session. No pacman, uv, npm, cargo or binary install was needed; the
drafting used the files already in the lane and one ordinary web fetch of the S089 page.
