# T48W2CritAxis — axis routing and do-nothing reachability (round 48, a2)

Seat: critic, axis/controls. Read-only on the lane; one `--no-live` probe of the frozen C2
counter into scratch; no counter verdict is claimed here.
Observed against CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17`; lane HEAD `17cc5ce`
(wave-spec commit). `git diff --stat c7586b9..HEAD -- SCORECARD.md corpus/QUALITY.md
corpus/lessons/round-48.md corpus/SOURCES.md` is empty, so line citations hold at both.
Scratch: `/fast/scratch/hyaku/tameshi-r48/T48W2CritAxis` (removed before yield). No tool
installs.

Rules referenced: `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-48.md` §6 item 9
(claim sizing: calibration = counted mismatches; universal clauses only when enumerated;
a do-nothing-reachable target is a broken target; one predicate sentence in plan, code and
receipt), `/home/vgpnk/Projects/shokunin/AXES.md` (axis table), contract
`.ufo/evidence/round-48/contract.json` (amendments 1–10), freeze
`.ufo/evidence/round-48/freeze-2.json`.

---

## Q1 — Is C1 a calibration move, not quality work re-scoring a held rule?

**Verdict: yes, calibration.** The surface the round changes is the self-assessment (the
`### Standing self-assessment — re-stated at round 48` block, `SCORECARD.md:2324-2336`), and the
metric is a mismatch count, exactly what item 9 requires ("A calibration claim must count
mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state. It
cannot be an assertion."). It is not a coverage/depth move: no new input class, tool or edge
class is scored; the 22 statements of `.ufo/evidence/round-47/calibration/statements.json` are
reused unchanged and sha-pinned (`924102df…`, `calibration/measure.py:77`).

Evidence that the move is real and not relabelling: the round-47 row for `six-leg regression
ledger` states the one-shot `REGRESSION: FAIL (cases=9 passed=7`, exit 1 (`SCORECARD.md:2270`),
and the round-48 row states `PASS (cases=9 passed=9`, exit 0, `runs 3 stable`
(`SCORECARD.md:2334`) — a value corrected by observation, the round-47 routed defect 1. The
counter counts it as `mismatch`/`unattested`, never as assertion: verdict order and label at
`calibration/measure.py:517-560, 574-581`.

### Counterexample tested — the narrow class the counter's own rule forces

`six-leg regression ledger` declares `runs 3 stable` while the same section, 6 lines earlier,
calls it "known to be nondeterministic under concurrency" (`SCORECARD.md:2328`), on peer
evidence of a one-sided PASS→FAIL race (`.ufo/waves/round-48/w1/T48RevenRegression.md`, ~10% at
6-way concurrency). The declaration is forced: amendment 4 makes `unattested` fire for any
member V the counter did not itself observe, so the FAIL member cannot be declared unless a
deciding-run observation produces it — and rows are frozen before the deciding run. So the
honest row is the narrowest attested class, and the cost is paid at the kill rule: with p≈0.1,
P(all three P0 rounds PASS) ≈ 0.73, i.e. roughly a one-in-four chance the deciding run is an
automatic miss on that statement, precisely as the contract's kill rule says it must be
("a flaky deciding observation outside V is a mismatch, not a rerun").

Judgment: this is a tradeoff amendment 4 already discloses (attestation rate
1-(1-p)^12, contract `amendments[3]`) and QUALITY 95 already states ("A `stable` class from
three agreeing observations stays a finite sample and proves no determinism"). It is **not** an
axis mislabel and **not** a counter defect. It *is* an honesty limit the round report must state
numerically rather than as "known nondeterministic" prose beside a machine-readable `stable`.

Non-blocking defects found while judging the axis:

- **D1 (predicate identity, docstring vs frozen rule).** `calibration/measure.py:11-12` and
  `:47-50` still say a member is attested when it is "recorded as a P0 tuple … in a committed
  file under `.ufo/evidence/round-48/calibration/observations/` at REV (read with `git show` at
  REV)". Amendment 4 says the opposite ("Committed files under …/observations/ are evidence for
  the report only, never attestation") and the code matches the amendment:
  `grep -n OBSERVATIONS_DIR .ufo/evidence/round-48/calibration/measure.py` → only `:79`
  (constant) and `:746` (a selftest fixture); `freeze-2.json` records "load_attestations/
  attest_token removed". The frozen counter's own header therefore documents the rule the
  contract forbids. Not exercised by the current 22 rows (all members come from the P0 emit),
  so no verdict changes — but item 9's "same sentence in the plan, the same condition in the
  counter's code" fails on the sentence.
- **D2 (latent, same root).** The contract's `claims.C1.statement` retains the pre-amendment
  attestation parenthetical ("observed in this run's P0 tuples or recorded as a P0 tuple in a
  committed observation receipt"), while amendment 4 admits P1 tuples plus up to six extra P0
  observations. A member seen only at P1 would be attested by code and forbidden by the claim
  sentence. No round-48 row does this (emit V is P0-derived), so it is latent.
- **D3 (provenance disclosure gap).** The rows were seeded from
  `.ufo/evidence/round-48/calibration/emit-15b1521.stdout`, whose own FLEET lines record
  `lane_clean=0` at points 2–4 (`emit-15b1521.stdout:2-4`) and whose verdict line reads
  `fleet_drift=1 … rev=15b1521…` (last line). The emit is not a pass (it printed
  `total=22 unparsed=22`), and amendment 4 forbids using it as attestation, so no rule breaks;
  but the SCORECARD paragraph that cites the emit (`SCORECARD.md:2326`) does not say the
  worktree was dirty against `corpus/`, `tools/` or `SCORECARD.md` for three of four points.
  A reader cannot tell that the row values are a seeded draft, not an observation of committed
  bytes. The deciding run re-observes at CONTENT (`deciding-run.sh:36`), so the claim is
  unaffected; a mismatch is still possible and correctly becomes a miss.

**Impacted axis:** calibration.

**Smallest safe corrections:** (D1) change `measure.py:11-12, 47-50` to amendment 4's rule and
note in the round report that amendment 4 supersedes the `claims.C1.statement` attestation
parenthetical (D2); no counter change — the code already conforms. (D3) one sentence in the
round-48 SCORECARD block citing `lane_clean=0`/`fleet_drift=1` in the emit receipt. For the
narrow class, state the miss probability; do not touch the row after data.

---

## Q2 — Is C2 freshness, and is it sourced?

**Verdict: yes, freshness and sourced.** The surface changed is four held registry rows and the
knowledge entries that consume them (drift detection against live pages), not a new rule or a
new input class. §2b item 4 is met: the claim rests on `SOURCES.md` rows opened this round
(S265–S268, `opened 2026-10-26`, `status mined`, `corpus/SOURCES.md:140-143`) and the entries it
re-points cite them.

Probe (not a verdict), frozen counter, `--no-live`, CONTENT, scratch `$TMPDIR`:

```
python3 .ufo/evidence/round-48/freshness/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 --no-live
TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S048 row=S266 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S093 row=S267 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
TARGET S108 row=S268 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped REFRESHED
C2_R48: self_pin=1 targets=4 refreshed=4 census_exit=0 live=off rev=c7586b9… C2_R48_PARTIAL=true
```

Sourcing chain checked statically as well: snapshot set is exactly four files plus four
receipts (`git ls-tree -r --name-only c7586b9 -- .ufo/evidence/round-48/freshness/sources`),
e.g. `S026.receipt.json` carries `url` = S265's source URL, `fetched_at 2026-10-26T08:40:51Z`,
`http_status 200`, `sha256 a4c5c46b4af9…` matching the snapshot and the `sha256 a4c5c46b4af9`
in S265's anchor cell; Gate lines are
`corpus/lessons/round-48.md:21-24`; each entry names both T and R
(`repeated-control-precondition` S026×6/S265×1, `incremental-pin-disposition` S048×2/S266×1,
`regression-tally-completeness` S093×6/S267×2, `r8-golden-update-flag` S108×1/S268×1) and
carries `verified-at: 2026-10-26`.

Two limits, neither a predicate breach:

- **Live leg unproven until the deciding run.** `live=skipped` here; the counter counts
  `live='skipped'` as ok (`freshness/measure.py:432-435`), so only the live invocation can earn
  `C2_R48_PASS`. The contract says this (`kill_rule`: "unreachable is reported, never credited"),
  but a `--no-live` receipt must never be read as the target.
- **Supersession is one-directional (freshness limit).** The held rows S026/S048/S093/S108 stay
  `mined` with their old anchors and no pointer to S265–S268; only the new row's `teaches` cell
  and the entries carry the flag. AXES' freshness signal is "stale items flagged or fixed", and
  a registry reader who opens S026 alone sees nothing. The entries also still cite T (above), so
  T is not orphaned. This is the pre-registered mechanism, not an overreach — but the round
  report should name it rather than imply the held rows were edited.

**Impacted axis:** freshness. **Smallest safe correction:** none to the counter or target; in the
round report, state that the four held rows are flagged from the superseding side only.

---

## Q3 — Could a do-nothing control reach either target?

**C2: no. Proven by a committed receipt.** `control/c2-controls.stdout`:
`CTL_F refreshed=0` with all four targets `row=none … NOT` (base tree, `rev=473336d9…`),
`CTL_G refreshed=0` (rows-only), `CTL_H refreshed=2` (quote-without-phrase, the contract's
`<=2` boundary), final line `CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true`; exit 0
(`control/c2-controls.exit`), scored-at recorded in `control/c2-controls.meta`
(`scored_at_freeze_bytes=7552984`, harness sha `46b8c039`, counter sha `faefe9b4`). CTL_F is
exactly the contract's `do_nothing_control`, and the counter's `ok` requires
`live == 'ok'` in live mode, so a fabricated-snapshot do-nothing cannot pass the deciding
invocation either (`freshness/measure.py:432-435`).

**C1: unproven — no C1 control receipt exists, and the record says one does.**

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only HEAD \
    -- .ufo/evidence/round-48/control
.ufo/evidence/round-48/control/c2-controls.exit
.ufo/evidence/round-48/control/c2-controls.meta
.ufo/evidence/round-48/control/c2-controls.py
.ufo/evidence/round-48/control/c2-controls.stderr
.ufo/evidence/round-48/control/c2-controls.stdout
.ufo/evidence/round-48/control/run-controls.py
$ grep -E '^CTL_B ' .ufo/evidence/round-48/control/c1-controls.stdout
grep: …/control/c1-controls.stdout: No such file or directory (os error 2)   # rc=2
$ git log --all --diff-filter=A --name-only -- .ufo/evidence/round-48/control
… only c2-controls.{exit,meta,stderr,stdout} at c7586b9 and
  c2-controls.py + run-controls.py at 7552984; no c1-controls.* ever added
```

Yet four records assert the receipt:

1. `contract.json` `freeze_plan` step 2: "the controls are scored and committed".
2. `contract.json` `amendments[9]` (n=9): "the C1 controls are scored at the counter-freeze
   commit"; `freeze-2.json` lists `control/run-controls.py` sha `f5732f18…` and
   `pending_w1_seats_at_freeze` still contains `T48ExecC1Controls`.
3. `corpus/QUALITY.md:1418` (criterion 95): "control CTL_B
   (`.ufo/evidence/round-48/control/c1-controls.stdout`) prints `total>0`, and the positive
   control CTL_E prints `total=0`".
4. `.ufo/evidence/round-48/quality/falsifiers.sh:33`: `R=$E/control/c1-controls.stdout`.

Consequence, observed: block 95 of the falsifier script cannot reach its OK branch at CONTENT —
it greps a missing file (`rc=2`), so it prints `CRITERION-95-FALSIFIER-VACUOUS`, and the
round's own lesson records exactly this mistake class ("`landing` — a record written ahead of the
work cites receipts that do not exist at the revision that carries it",
`corpus/lessons/round-48.md:360`) for the attempt-1 salvage — the pattern is still live in the
content revision, because QUALITY 94–96 were carried in at `15b1521` and the pointed-to receipt
was never produced.

Why this is material, not bookkeeping: the two controls that matter for target reachability are
missing. **CTL_B** is the cheapest control that *skips the claimed work* — the 22 round-47 rows
re-appended with `runs 3 stable` and no re-observation; item 9 requires that receipt before
freeze ("if it meets the target, the counter or target is wrong"). Without it, "the rows could
not have been relabelled from last round" is asserted, not shown. **CTL_E** ("rows emitted by
the counter's own `--emit` from the same observation run → must print total=0") is the only
committed demonstration that the frozen counter can pass on the *real* 22 statements at all;
the selftest's `total=0` cases (T30/T33a, `measure.py:739-756`) run on synthetic statements and
cannot show satisfiability of the real population. `emit-15b1521` shows only the opposite
(`total=22 unparsed=22`), which is the CTL_A-side datum, not CTL_E.

**Impacted axis:** calibration (do-nothing reachability is a calibration property; item 9 names
kaidoku r29 C1 and kake r34 as the precedents this rule exists for).

**Smallest safe correction (in order of preference):**
1. Before the deciding run, run the frozen harness with the frozen counter
   (`python3 .ufo/evidence/round-48/control/run-controls.py …` — sha `f5732f18…`, counter sha
   `572a5670…`) and commit `control/c1-controls.{stdout,exit,meta}`; require A `unparsed`,
   B/C/D to fail for the named reason and E `total=0`. If CTL_E cannot reach `total=0`, the
   target is unreachable: record an honest stop, do not admit C1.
2. If (1) cannot be done before the deciding run, correct the records instead of leaving them
   false: `corpus/QUALITY.md:1418` must not name a receipt that does not exist, and the round
   report must state "C1 do-nothing reachability unproven" and cite the lesson's own `landing`
   row. Do not amend the contract after the deciding run.

---

## Q4 — Are there universal words whose set the counter does not enumerate?

**Verdict: every universal clause is backed by a closed, pinned set; two identity gaps, no
unenumerated set.** Item 9 bans "all/complete/every/no harm anywhere" unless the counting
command enumerates the full set. The enumerations:

| Clause | Set actually enumerated | Where |
|---|---|---|
| C1 "for each of the 22 frozen statements" | `statements.json` at REV, pinned `924102df…`, `len == 22` required for pass | `measure.py:20, 77-78, 574-581` |
| C1 "every observed P0 tuple ∈ V" | 3 rounds × P0 + ≤6 extra fresh P0 observations (`MAX_EXTRA=6`); an extra outside V is `mismatch` | `measure.py:82, 494-557`; selftest T33b/T60 |
| C1 "every member of V is attested" | V enumerated by `parse_row`; attested by this invocation's P0/P1 tuples or extras only | `measure.py:529-556`; `OBSERVATIONS_DIR` unused outside selftest |
| C1 "D contains every dependence observed in all 3 rounds / none observed in none" | `DEP_NAMES` = 5 names; per-round variant diffs; `required = ∩`, `never = DEP_NAMES − ∪` | `measure.py:87, 498-512` |
| C1 "base SCORECARD.md stays a byte prefix" | whole-file prefix `rev_sc.startswith(base_sc)` | `measure.py:429` |
| C2 "for each T in {S026,S048,S093,S108}" | `TARGETS` fixed 4; `exactly one row` else `none`/`ambiguous` | `freshness/measure.py:85, 213-233` |
| C2 "every knowledge entry in T's base used-by cell" | base row at BASE (`S026…` cells), split on commas | `freshness/measure.py:200-209, 318-336` |
| C2 "R's used-by cell lists exactly those entries" | set equality with the base list | `:334-336` |
| C2 "at most 25 words", required phrases | `MAX_WORDS=25`; `REQUIRED` identical to the contract's `required_phrases` | `:100, 86-91, 303-316` |

Boundary checks I made on the actual Gate lines (`corpus/lessons/round-48.md:21-24`): S026 quote
15 words, S048 21, S093 exactly 25 (passes `words > 25`), S108 6 whitespace tokens under
amendment 2's CJK-biased count; each contains its required phrase(s).

The two identity gaps, both already covered under Q1 as D1/D2, are not missing sets but
*different* sets in different texts: (i) attestation (contract `statement` + counter docstring
say P0 + committed observation receipts; amendment 4 + code say P0/P1/extras, no files);
(ii) C2's "whose source cell carries T's URL" is implemented as amendment 1's
source+anchor URL-set inclusion (`freshness/measure.py:215-219, 132-160`), which is the pre-data
amendment and is enumerated by `urls_of`, not the plain wording. Neither is exercised by a
round-48 value: all 22 row members are P0-derived, and every target's receipt URL is in R's
source or anchor cell (receipts = ok above).

**Impacted axes:** calibration (D1/D2 identity). Freshness: no universal gap.

---

## Verdict summary

| Question | Verdict | Class |
|---|---|---|
| 1. C1 = calibration, not quality re-scoring | Yes | calibration; six-leg `stable` is a disclosed finite sample (miss risk ≈0.27), not a counter defect |
| 2. C2 = freshness and sourced | Yes | freshness; live leg pending by design; held rows flagged one-directionally (limit) |
| 3. Do-nothing can reach a target | C2: **no** (CTL_F/G/H committed). C1: **unproven** — no `control/c1-controls.*` exists; amendment 9, freeze step 2, QUALITY 95 and `falsifiers.sh:33` name it; block 95 is VACUOUS at CONTENT | fixable defect (calibration) |
| 4. Unenumerated universal words | None; closed sets, two text-level identity gaps (D1/D2) | fixable documentation/provenance defects |

Nothing here attacks the C1/C2 predicates or targets themselves: no target was narrowed, no
rule was changed after data, and the axis routing for both claims is correct. The blocking item
for milestone "axis naming and do-nothing reachability" is C1's missing control receipt; the
smallest safe correction is to score and commit it with the frozen harness before the deciding
run (or record it as unscored and report C1's reachability as unproven).

## Sources & frontier
C2 re-anchors S026/S048/S093/S108 through S265–S268 (opened 2026-10-26, cited by the four
entries with `verified-at: 2026-10-26`); census at CONTENT exit 0. This seat added no source
row and no fixture.
