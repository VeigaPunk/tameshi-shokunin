# T50ScribeConsider — considerthese proposal status at base + round-50 lesson draft

Seat: `T50ScribeConsider`. Item: list every proposal of the latest considerthese file with its implementation status in the
lane at `e3729de862f73ae080d98fcf522a7081ce16e40a`, then draft the round-50 lesson section `## considerthese` for
`considerthese/2026-10-26.md` proposal 3.

Read-only seat. No counter was run (no `measure.py` in any mode), no deciding run, no control scored. Every command below is
`git`-read-only against the lane checkout or a plain `grep`; nothing in the lane was written except this report and its probe
receipt. Lane HEAD at read time: `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2` (base + 4 pre-wave-1 commits: freeze, controls,
spec, SCORECARD pre-registration). Probe receipt:
`.ufo/waves/round-50/w1/T50ScribeConsider.probes.txt`.

## 1. The file

`considerthese/2026-10-26.md`, 89 lines, sha256 `376bddda8045f42d47c31ea256f0620d3b286d5c45e174312e34bb025902d26c`,
byte-identical at base and in the worktree
(`git -C LANE show e3729de:considerthese/2026-10-26.md | sha256sum` vs `sha256sum considerthese/2026-10-26.md`; added by
`41c1bc0 considerthese: 2026-10-26 daily reflection`, the only commit touching it). It is the **latest** file: the directory
holds `2026-10-19/20/22/23/24/25/26.md`, and 2026-10-26 is last
(`git ls-tree -r --name-only e3729de -- considerthese/`).

It carries five proposals (`## Self-improvement ideas (proposals only, not acted on)`, `:72`), one status block for the
2026-10-25 ideas (`## Status of earlier ideas`, `:64-70`), and the window note "Rounds 37–43 were covered in the 2026-10-25
file, so this one concentrates on what landed after it" (`:4-6`).

## 2. The five proposals at base `e3729de`

Status vocabulary as the item defines it: **implemented** = a tool/record in the tree does the thing; **mined only** = the
idea appears as a lesson/analysis but no artifact does the thing; **untouched** = nothing in the tree but the proposal text.

| # | Proposal (line span) | Ask | Status at base | Evidence |
|---|---|---|---|---|
| 1 | Crash-resume integrity check `:74-76` | after a crash, verify frozen contract/counter shas/amendments are byte-identical to the committing commit and flag re-freeze or amendment made after wave-1 data was visible | **untouched** | proposal only; `git grep -i 'crash-resume' e3729de -- corpus tools SCORECARD.md LOG.md SKILL.md` = 0 hits; no tool in `tools/` does it (`ls tools/`); the phrase occurs once elsewhere, as a candidate in a contract (`e3729de:.ufo/evidence/round-49/contract.json:78`) |
| 2 | Nondeterminism fix list `:77-79` | list every standing row that declares class `nondeterministic`, with root cause | **untouched** | the permitting rule exists — `corpus/QUALITY.md:1400` criterion 95 ("declared nondeterministic class") — but no list: `git grep -i 'nondeterminism fix'` = 0 hits; the only class tables are per-tool (`corpus/knowledge/hermetic-env-differential.md:74-79`, `js-round-gate` = nondeterministic) and the SCORECARD disclosure `SCORECARD.md:2328` (six-leg ledger "known to be nondeterministic under concurrency" while its row states `stable`) |
| 3 | Recurring-defect tracker for closures `:80-82` | tally each closure's status-neutral conformance defects; check whether a defect already routed to a criterion returns; a recurrence becomes a gate | **mined only** (round 49) | `corpus/lessons/round-49.md:130-140`: nine spot-checks (rounds 40-48), 44 status-neutral defects, 26 classes, 10 classes recur carrying 24 rows, four after a criterion (`:134-136`); no tracker artifact: `git -C LANE cat-file -e e3729de:corpus/routed-defects.json` → `fatal: path ... does not exist`, exit 128; `git log --all --oneline -- corpus/routed-defects.json` prints nothing (never committed in any ref) |
| 4 | Host and scratch budget readout `:83-85` | per round: scratch-space use, seats dispatched vs reported, host events from LOG/watchdog | **untouched** | `git grep -i 'budget readout\|scratch budget'` = 0 hits in `corpus tools SCORECARD.md LOG.md SKILL.md` (probe §2), and the phrase occurs once in a round-48 critic file (`.ufo/waves/round-48/a2w1/T48W2CritConsiderthese.md:226`); `git grep -n 'seats dispatched\|scratch-space\|scratch space'` = 206 lines tree-wide, but 189 are the same provenance sentence in `.ufo/evidence/round-21/coldread/ledger.json` and the rest are incidental prose — no readout table; the adjacent tool reconciles membership only (`tools/wave-accounting.py:1-10`: "Reconcile retained callback outcomes with exact wave membership", no scratch/host fields) and predates the idea |
| 5 | Carrier fallback register `:86-88` | list rate-limited/unstable carriers and the fallback each verification used | **untouched** | `git grep -i 'fallback register'` = 0 hits; the incident it cites is real and recorded — `corpus/lessons/round-47-verifier-spotcheck.md:88` ("live API: HTTP 429 on three attempts; fallback `api.crossref.org/works/10.1109/ICST60714.2024.00037`") and `corpus/lessons/round-47.md:55` ("the first fetch answered HTTP 429, a later one 200") — but no register; carrier defects are handled per entry instead (`corpus/knowledge/r8-flaky-cost-baseline.md:14`) |

Count: **0 of 5 implemented, 1 mined only (proposal 3), 4 untouched** at `e3729de`.

### Post-base note on proposal 1 (context, not status)

The round-50 instrument added after base does one of the three things proposal 1 asks: the deciding script asserts the frozen
paths are unchanged between the counter-freeze commit and the content revision
(`.ufo/evidence/round-50/deciding-run.sh:36-37`, `FROZEN="… 15 paths …"` then `git diff --quiet "$FREEZE" "$REV" -- $FROZEN`
→ `FROZEN_UNCHANGED=`). It does **not** compare the contract's bytes to the blob of the commit that froze it, and it does not
scan for a re-freeze or a new amendment made after wave-1 data was visible (round-50's contract carries `amendments: []`,
`.ufo/evidence/round-50/contract.json`); `freeze.json` records sha256s but nothing in the tree verifies them against the
committing blob. So the crash-resume check remains unimplemented even in the post-base instrument.

## 3. Proposal 3 this round: what the C1 ledger is

Proposal 3 is implemented this round as C1's calibration surface, not as a new tool:

- instrument: `.ufo/evidence/round-50/c1/measure.py` (label `C1_R50_PASS`), statement set
  `.ufo/evidence/round-50/c1/defects.json` (49 items, sha256 pinned; built by `extract-defects.py` + `keys.json` at base);
  population per round 40→49: 5, 7, 4, 3, 2, 4, 5, 7, 6, 6 = 49
  (`python3` over `defects.json`; probe §3).
- ledger: `corpus/routed-defects.json`, schema `tameshi-routed-defects-v1`, row
  `{id, status, evidence[{path, lines, excerpt}], commit?, reason?, seat?, note?}`
  (`.ufo/evidence/round-50/contract.json:27`).
- floors: `fixed_min 20`, `declined_max 12`, `fixed_after_base_min 5` (`contract.json:30-34`;
  `measure.py:50-52` `FIXED_FLOOR=20`, `THIS_ROUND_FLOOR=5`, `DECLINED_CAP=12`).
- the tree-support rules: fixed = keyed excerpt absent at `routed_at`, in a path the post-routing commit touches, on lines
  with none of `ACK_WORDS`; open = id in the newest `**Planned (round` paragraph of `SCORECARD.md`; declined = reason ≥ 40
  chars (`measure.py:13-25`, `ACK_WORDS` at `:54-55`).
- at base the ledger does not exist and the counter's `before` is `missing=49`
  (`contract.json:28`; probe §1: `cat-file -e` exit 128, `git log --all` empty).

Tree state at my read: the ledger is still absent at HEAD `4afb060` (only the four pre-wave-1 commits exist above base:
`git log --oneline e3729de..HEAD`). It is a wave-1/wave-2 deliverable; this report's §2 base status is unaffected, and the
lesson draft below is written for the close, with one fact to confirm there (see §5).

What the ledger cannot do is stated by the contract itself: it cannot see semantic support (a new keyed excerpt that does not
actually resolve the item) and cannot see underclaim (an item marked open/declined that is in fact fixed)
(`.ufo/evidence/round-50/contract.json:35`). Control `CTL_FAB` reaches `fixed=38` from history alone and is stopped only by
the after-base floor (same line).

## 4. Earlier ideas block (`considerthese/2026-10-26.md:64-70`) — verified

The file's own claims hold at base:

| Filed under | Claim (`:66-70`) | Verified at |
|---|---|---|
| 2026-10-25 p1 | → QUALITY criterion 86 | `corpus/QUALITY.md:1156` "Criterion 86 — a deciding receipt binds the revision it measured…", lesson line cites `considerthese/2026-10-25.md:66-68` |
| 2026-10-25 p2 | → round-46 cumulative restatement | `corpus/lessons/round-46.md:101` "proposal 2 (cumulative mismatch-class regression run) is mined" |
| 2026-10-25 p3 | → round-47 dead-code scan, routed | `corpus/lessons/round-47.md:92` section + `:95` "unreferenced=2: `brace_depth_at` in `tools/tally-audit-v2.py:135` and …"; carried at `corpus/lessons/round-47-verifier-spotcheck.md:107` |
| 2026-10-25 p4 | not mined, more relevant now | no artifact; same gap as proposal 4 above (one object: tempo + capacity) |
| 2026-10-25 p5 | → round-48's unlanded drafts | `corpus/lessons/round-48.md:364` "### considerthese — `considerthese/2026-10-25.md` idea 5 (proposal uptake ledger)" — mined in a draft the round did not land |
| SHONEN | all four `[~]` | `SHONEN.md:5-12` — exactly four `- [~]` boxes, each with a lane-assertion bracket |

## 5. Draft — round-50 lesson section

To be appended to `corpus/lessons/round-50.md`. One fact is the L1's to confirm at close: this draft says the ledger exists
and carries the statuses; at my read (HEAD `4afb060`, wave 1 in flight) `corpus/routed-defects.json` is not in the tree. If
C1 lands, the draft stands as written; if it stops short, replace the second sentence's tense with the observed ledger state
and keep the "does not do" half, which is true of the instrument either way.

---

## considerthese

`considerthese/2026-10-26.md` (operator reflection, 2026-10-26), proposal 3, "Recurring-defect tracker for closures"
(`considerthese/2026-10-26.md:80-82`), was mined in round 49 as a one-round tally — the nine spot-checks of rounds 40-48
carry 44 status-neutral defects in 26 classes, 10 classes recur in a later round and carry 24 of the 44 rows, four of them
after a QUALITY criterion had been written for them (`corpus/lessons/round-49.md:130-140`) — and is implemented this round as
C1's ledger, `corpus/routed-defects.json` (`.ufo/evidence/round-50/contract.json:27`), scored by
`.ufo/evidence/round-50/c1/measure.py` (label `C1_R50_PASS`).

What the ledger does that the proposal asked for. It makes the lane's disposition of every routed defect a checkable record:
one row for each of the 49 items the ten spot-checks of rounds 40-49 routed (`.ufo/evidence/round-50/c1/defects.json`), with a
status the tree must support — `fixed` needs a full commit after the item's routing commit, a keyed excerpt absent from that
path at `routed_at`, and no acknowledgement word on the cited lines; `open` needs the id in the newest `**Planned (round`
paragraph of `SCORECARD.md`; `declined` needs a reason of at least 40 characters (`measure.py:13-25`) — and every evidence
excerpt must resolve at its cited 1-based lines, outside the spot-checks, the ledger and this round's C1 instrument, with the
ten spot-check files byte-unchanged. It also forces work in the round that opens it: `fixed >= 20`, `declined <= 12`, and at
least 5 fixes landed by commits after base (`contract.json:30-34`), which is what a ledger fabricated from history alone
cannot meet (`contract.json:35`, control `CTL_FAB`). So "a routed defect is not a closed defect" becomes a predicate instead
of a note, the half of the proposal that says the disposition must be visible.

What it does not do. It is per item, not per class: the row schema carries no class field (`contract.json:27`), so it neither
tallies a defect class nor counts a recurrence across rounds — the proposal's central question, "check whether a defect
already routed to a criterion shows up again", is not answered by the ledger. It carries no gate: the proposal's
"a recurrence means the fix did not stick and should become a gate, not another note" has no counterpart, because nothing in
the instrument reads two rounds at once. Its population also differs from the proposal's: 49 routed items, not the 44
status-neutral conformance defects the round-49 tally counted (`corpus/lessons/round-49.md:134`). And it cannot see semantic
support — a keyed excerpt that is new since routing but does not actually resolve the defect passes the counter
(`contract.json:35`); wave-2 seats attack that per row and the closure samples it. The recurrence half therefore stays open,
and the round-49 note already named what it needs: a criterion with a falsifier over the spot-checks
(`corpus/lessons/round-49.md:140`). The next step is a class field plus a recurrence clause whose falsifier is a class fixed
in round N that reappears in round N+k, not a second prose ledger.

---

## 6. Findings

1. **The latest file has five proposals; only one is implemented, and not at base.** Proposal 3 is the round-50 C1 surface;
   proposals 1, 2, 4 and 5 have no artifact at `e3729de` (`git grep` zero hits outside `considerthese/` for each name, probe
   §2). The file's own "Status of earlier ideas" block is accurate for the 2026-10-25 set (probe §5).
2. **Proposal 3's tracker is only half built, and the ledger's schema proves it.** No `class` key in
   `tameshi-routed-defects-v1` (`contract.json:27`), no cross-round read in the counter (`measure.py:13-25` covers one REV
   only). The proposal asked for a recurrence check that becomes a gate; the ledger gives per-item disposition and floors.
3. **The population the ledger checks is not the population round 49 counted.** 49 routed items vs 44 status-neutral
   conformance defects in 26 classes (`corpus/lessons/round-49.md:134`); a routed item can bundle several asks, and the
   contract's rule that a compound item is fixed only when every ask is met lives in the assignment, not in the counter.
4. **Base absence is exact.** `git -C LANE cat-file -e e3729de:corpus/routed-defects.json` → exit 128 with
   `fatal: path 'corpus/routed-defects.json' does not exist`; `git log --all --oneline -- corpus/routed-defects.json` → no
   lines. The contract's `before` says the same (`missing=49`).
5. **Proposal 1 stays unimplemented even after base.** The only freeze-integrity check in the tree is
   `deciding-run.sh:36-37`'s `git diff --quiet "$FREEZE" "$REV" -- $FROZEN` over 15 paths; nothing compares
   `freeze.json`'s sha256 map to the committing blob, and nothing flags a post-wave-1 amendment (round-50: `amendments: []`).
6. **Proposal 2's rule is real but the list is not.** Criterion 95 (`corpus/QUALITY.md:1400-1417`) exists; the only
   class assignments are one per-tool table (`corpus/knowledge/hermetic-env-differential.md:78`) and one SCORECARD
   disclosure (`SCORECARD.md:2328`, which states `stable` while disclosing a known race), so "every row that declares
   `nondeterministic`, with its root cause" has no home.
7. **Proposal 4's readout is still absent and already known to be buildable.** The round-48 critic corrected the
   "not buildable" claim (`/…/T48W2CritConsiderthese.md:226`, quoting the operator's own next-day narrowing), yet nothing
   measures scratch use, seats dispatched vs reported, or host events per round; `tools/wave-accounting.py:1-10` is the
   nearest capability and answers wave membership only.
8. **Proposal 5's incident is documented, its register is not.** `corpus/lessons/round-47-verifier-spotcheck.md:88` records
   the three 429s and the Crossref fallback; carrier defects are disclosed per entry
   (`corpus/knowledge/r8-flaky-cost-baseline.md:14`). No list exists to re-check a tier-B admission that rests on a fallback.

## 7. Limits of this report

- No counter was invoked, so nothing here reports `C1_R50_PASS` or any other claim outcome; the ledger's actual contents,
  its row statuses, and the counter's deciding line are unobserved by me.
- The "post-base note" on proposal 1 reads bytes at HEAD `4afb060`; if a later wave-1 commit changes `deciding-run.sh` the
  note's line numbers move (`contract.json` freezes that file, so a change would itself be a re-freeze event).
- I did not open `.ufo/evidence/round-50/control/c2-*.stdout` beyond listing names, did not touch the hidden panel path, and
  did not quote mutant names.
- The lesson draft's first sentence of paragraph 2 asserts the ledger "is implemented this round"; that is the round's
  pre-registered instrument, not an observed file — confirm at close (§5).

## Summary

- Latest file: `considerthese/2026-10-26.md` (89 lines, sha256 `376bddda…`), five proposals at `:74`, `:77`, `:80`, `:83`, `:86`.
- At base `e3729de`: proposal 3 **mined only** (`corpus/lessons/round-49.md:130-140`); proposals 1, 2, 4, 5 **untouched**
  (zero keyword hits outside `considerthese/`); 0 of 5 implemented.
- `corpus/routed-defects.json` is absent at base and in all refs (exit 128; `git log --all` empty), matching the contract's
  `missing=49`.
- Proposal 3 this round: C1's ledger (49 items, per-item status, evidence-resolution rules, floors 20/12/5), schema at
  `.ufo/evidence/round-50/contract.json:27`.
- The ledger does not do the proposal's recurrence half: no class field, no cross-round read, no gate; population is 49 routed
  items, not 44 conformance defects in 26 classes.
- Earlier-ideas block verified accurate; SHONEN still four `[~]` (`SHONEN.md:5-12`).
- Deliverable + probe receipt: `.ufo/waves/round-50/w1/T50ScribeConsider.md`, `T50ScribeConsider.probes.txt`.
