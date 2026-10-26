# T50RevengerRecur — the life of the 49 routed items (rounds 40–50)

Seat T50RevengerRecur (revenger), round 50 wave 1. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
base `e3729de862f73ae080d98fcf522a7081ce16e40a`, HEAD `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`.
Item: planning-data walk for the L1's planner seat — for each of the 49 items frozen in
`.ufo/evidence/round-50/c1/defects.json`, the round that first acknowledged it, how many rounds it was
carried, whether its class came back after a fix or a QUALITY criterion, and which items restate each
other; then a proposed QUALITY criterion only where a check that fails on a recurrence can be named.

I decided no claim, ran no claim counter (no `--selftest`, no `--explain`), read nothing under
`/home/vgpnk/.local/state/`, and quoted no mutant name or edit from `control/c2-*.stdout`. The lane is
read-only for this seat: no file written outside this report and
`.ufo/waves/round-50/w1/T50RevengerRecur.receipts/`; no git/jj mutation; no scratch left behind
(`/fast/scratch/hyaku/tameshi-r50/T50RevengerRecur`, removed). Tools installed: none.

Counting rule, stated once so the column can be checked:

* **first ack** = the earliest round *after* the routing round whose committed record names the item and
  its state — a SCORECARD `Planned` field, a `Disposition of …` line, or a lesson `## Mistakes` row. The
  closure files are cited only where the lane's own records are silent, and the cell says so.
* **rounds carried** = rounds strictly after the routing round up to and including the round the item was
  closed; for items still open at `4afb060`, up to and including round 50 (the round being planned).
* **closed** = the round whose tree carries what the item asked for, or the round that declined it with a
  reason (marked `declined`). `pre-routing` means the tree already satisfied it before the item was
  routed.
* "same class came back" is judged on the *class*, not the instance, and cites the later closure line.

---

## 1. The table — 49 rows

| id | first ack (round:file:line) | rounds carried | closed | recurred after fix / class evidence | class | duplicate of |
|---|---|---|---|---|---|---|
| R40.1 | r41 corpus/lessons/round-41.md:51 | 1 | r41 | class: record-drift (r47 spot-check:25; r48 spot-check:30) | record-drift | — |
| R40.2 | none in r41–r50 | 10 | **open** | class: pointer-unresolvable (r41 spot-check:70 = R41.2; r48 spot-check:30) | pointer-unresolvable | R41.2 |
| R40.3 | none in r41–r50 | 10 | **open** | — | prompt-item-unmet | — |
| R40.4 | r41 corpus/lessons/round-41.md:75 | 10 | **open** | class: label-count (r44 spot-check:73), then Q87 held (0 after r45) | label-count | R44.1 |
| R40.5 | pre-routing r39 SCORECARD.md:1859 | 0 | r39 (pre-routing) | — | guard-vacuous | — |
| R41.1 | r42 corpus/lessons/round-42.md:160 | 1 | r42 | class: instrument-defect (r43 lesson:132) | instrument-defect | — |
| R41.2 | r42 corpus/lessons/round-42.md:159 | 1 | r42 | class: pointer-unresolvable (r48 spot-check:29) | pointer-unresolvable | R40.2 |
| R41.3 | r42 SCORECARD.md:2028 | 1 | r42 | — | instrument-defect | — |
| R41.4 | r42 corpus/lessons/round-42.md:252 | 1 | r42 | — | instrument-defect | — |
| R41.5 | r42 corpus/lessons/round-42.md:247 | 1 | r42 | — | doc-overclaim | — |
| R41.6 | r42 corpus/lessons/round-42.md:118 | 1 | r42 | class: id-collision (r42 spot-check:114 → guard r43) | id-collision | R42.3 |
| R41.7 | r42 corpus/lessons/round-42.md:254 | 1 | r42 (declined) | — | format-cosmetic | — |
| R42.1 | r43 SCORECARD.md:2089 | 1 | r43 | — | instrument-defect | — |
| R42.2 | r43 corpus/lessons/round-43.md:171 | 8 | **open** | class: instrument-defect (r43 lesson:132; r49 lesson:94) | instrument-defect | — |
| R42.3 | r43 corpus/lessons/round-43.md:81 | 1 | r43 | — | id-collision | R41.6 |
| R42.4 | r43 corpus/lessons/round-43.md:181 | 8 | **open** | chain restated verbatim (R46.5/R47.7/R48.6/R49.6) | shonen-box-unpromotable | R46.5, R47.7, R48.6, R49.6 |
| R43.1 | r44 corpus/lessons/round-44.md:83 | 1 | r44 | — | record-citation-unknown | — |
| R43.2 | r44 corpus/lessons/round-44.md:85 | 1 | r44 | class: record-mutation (r47 spot-check:22) | record-mutation | — |
| R43.3 | r44 corpus/lessons/round-44.md:45 | 1 | r44 | class: stale-anchor (r45 spot-check:88; r46 spot-check:99) | stale-anchor | R45.4, R46.1 |
| R44.1 | r45 corpus/lessons/round-45.md:158 | 6 | **open** | class: label-count, no recurrence after Q87 | label-count | R40.4 |
| R44.2 | r45 (observation, not a defect) | 0 | r45 (declined) | class: wave-shape (r47 spot-check:21; r48 lesson:305) | wave-shape | R47.6 |
| R45.1 | r46 corpus/lessons/round-46.md:121 | 1 | r46 | class: monitor-false-red (r48 spot-check:29, after Q88) | monitor-false-red | — |
| R45.2 | r46 closure corpus/lessons/round-46-verifier-spotcheck.md:36 | 1 | r46 | **YES: r47 spot-check:23 and :24** | receipt-not-committed | R47.2 |
| R45.3 | r45 SCORECARD.md:2159 (same round) | 0 | r45 (declined) | — | measure-definition-change | — |
| R45.4 | r46 SCORECARD.md:2253 | 3 | r48 | class: stale-anchor | stale-anchor | R46.1, R47.5 |
| R46.1 | r47 SCORECARD.md:2312 | 2 | r48 | — | stale-anchor | R45.4, R47.5 |
| R46.2 | r47 SCORECARD.md:2309 | 1 | r47 | — | capability-not-operative | — |
| R46.3 | r47 SCORECARD.md:2264 | 1 | r47 | class: standing-row-unreproducible (r47 spot-check:103 → Q95) | standing-row-unreproducible | R47.1 |
| R46.4 | r47 corpus/lessons/round-47.md:105 | 1 | r47 | class: quote-fold, no recurrence after Q91 | quote-fold | — |
| R46.5 | chain restated (closure only) | 4 | **open** | — | shonen-box-unpromotable | R42.4 |
| R47.1 | r48 corpus/lessons/round-48.md:108 | 1 | r48 | class: standing-row-unreproducible, residual race re-routed r49 | standing-row-unreproducible | R46.3 |
| R47.2 | r48 corpus/lessons/round-48.md:306 | 3 | **open** | **YES (class): r45 → fixed r46 → r47** | receipt-not-committed | R45.2 |
| R47.3 | r48 corpus/lessons/round-48.md:108 | 1 | r48 | — | record-drift | — |
| R47.4 | r48 corpus/lessons/round-48.md:270 | 1 | r48 | — | weak-citation | — |
| R47.5 | r48 SCORECARD.md:2312 | 3 | **open** | carried-list class persists (R48.4/R49.5) | carried-open | R45.4, R46.1, R48.4, R49.5 |
| R47.6 | r48 corpus/lessons/round-48.md:305 | 2 | r49 | class: wave-shape (r48 spot-check:28) | wave-shape | R44.2 |
| R47.7 | chain restated (closure only) | 3 | **open** | — | shonen-box-unpromotable | R42.4 |
| R48.1 | r49 corpus/lessons/round-49.md:6 | 1 | r49 | — | coldread-credit-loss | — |
| R48.2 | r49 corpus/lessons/round-49.md:90 | 1 | r49 | — | order-of-scoring | — |
| R48.3 | r49 corpus/lessons/round-49.md:90 | 1 | r49 | — | order-of-scoring | R48.2 |
| R48.4 | r49 closure corpus/lessons/round-49-verifier-spotcheck.md:126 | 2 | **open** | carried-list class | carried-open | R47.5, R49.5 |
| R48.5 | r49 corpus/lessons/round-49.md:92 | 1 | r49 | — | record-drift | — |
| R48.6 | chain restated (closure only) | 2 | **open** | — | shonen-box-unpromotable | R42.4 |
| R49.1 | none: absent from `Planned (round 50)` | 1 | **open** | — | generator-error-path | — |
| R49.2 | r50 SCORECARD.md:2410 | 1 | **open** | — | instrument-defect | — |
| R49.3 | r50 SCORECARD.md:2410 | 1 | **open** | — | outside-section-stale | — |
| R49.4 | r50 SCORECARD.md:2416 | 1 | r50 | — | standing-axis-table-stale | — |
| R49.5 | r50 SCORECARD.md:2410 | 1 | **open** | carried-list class | carried-open | R47.5, R48.4 |
| R49.6 | chain restated (closure only) | 1 | **open** | — | shonen-box-unpromotable | R42.4 |

Machine-readable copy of the same rows: `T50RevengerRecur.receipts/recurrence-walk.json`
(`schema: tameshi-r50-recurrence-walk-v1`, built by `build_table.py` in the receipts dir).

## 2. What the walk measures

```
rows 49   classes 27   classes with >=2 rows 12   closed 32   open 17
median rounds carried (closed) 1.0   mean 1.03   closed in exactly one round 26 of 32
open with carried >= 2: R40.2(10) R40.3(10) R40.4(10) R42.2(8) R42.4(8) R44.1(6)
                        R46.5(4) R47.2(3) R47.5(3) R47.7(3) R48.4(2) R48.6(2)
```

Two shapes, and they are almost disjoint:

* **Acknowledged in the next round and closed there** — 26 of 32 closed items, median 1 round. This is
  the healthy half: the item names a concrete object (a counter class, a receipt, a row, a pointer) and
  the next round changes that object.
* **The 17 open items** — 4 of them were never acknowledged at all or only by the closure
  (R40.2, R40.3, R45.2-class successor R47.2, R42.4-chain), and 6 were *acknowledged and then
  re-classified as disclosed or operator-owned* (R40.4, R44.1, R42.2, R42.4, R47.2, R47.5). Nothing in
  the window went from "acknowledged as a defect to fix" to open again by neglect — the long tail is made
  of items that were never given a fix, not of fixes that lapsed. The exceptions are the two *classes*
  that came back (§3).

Commands behind the counts (read-only):

```
python3 -c 'import json;d=json.load(open(".ufo/evidence/round-50/c1/defects.json"));print(d["count"])'   # 49
python3 /fast/scratch/.../build_table.py    # the receipt dir's copy reproduces the counts above
```

## 3. Classes that recurred **with a criterion behind them**

Every row below is a class whose first occurrence got a criterion (or was closed by a route) and whose
*next* occurrence is a later closure line. The last column is what the criterion's text could not reach —
that is the planning datum, not the recurrence itself.

| class | criterion written for it | later occurrence (spot-check line) | what the criterion did not reach |
|---|---|---|---|
| monitor-false-red | **Q88** (`corpus/QUALITY.md:1291`) for R45.1 | `round-48-verifier-spotcheck.md:29` — `FROZEN_UNCHANGED=0` false red | 88 requires the monitors green **at base before the freeze**; the r48 red came from the frozen path list containing the round's *own new receipts* — a self-referential input, not a base-run monitor. Round 50's `deciding-run.sh:36` now excludes `control/` and `after/` from `FROZEN`, so this half is fixed by list hygiene, not by 88 |
| standing-row-unreproducible | **Q92** (`:1363`) for R46.3 | `round-47-verifier-spotcheck.md:103` (one-observation row) and `:25` (lesson dependence sets) | 92 states *what* a statement depends on; it never counts observations. That gap became **Q95** (`:1400`, N≥3 or a declared nondeterministic class), written the next round |
| pointer-unresolvable | **Q72/Q73 → Q81 → Q97** for R40.2/R41.2 | `round-48-verifier-spotcheck.md:30` — the lesson cites `SOURCES.md:140/141` for rows at 142/143 | every criterion tests *resolution*: the path exists, the receipt postdates its writes, the pointer resolves at the landing revision. A pointer that resolves to the **neighbouring row** satisfies all three. Nothing in the set tests that the resolved line is the *intended* one |
| record-drift | **Q35** (`:262`, append-only correction form) for R40.1 | `round-47-verifier-spotcheck.md:25`; `round-48-verifier-spotcheck.md:30`; `round-49-verifier-spotcheck.md:45` (a correction count that does not add up) | 35 governs how a correction is *filed* — both revisions named, append-only — not whether the prose matches the table it summarises. A record can be perfectly filed and still wrong |
| receipt-not-committed | **none** — see §4 | `round-47-verifier-spotcheck.md:23` and `:24` | this is the operator's example: r46 committed the receipts (`selftest/c{1,2,3}-selftest.stdout`) and wrote no criterion, so nothing could fail when r47 dropped them |
| order-of-scoring | **Q99** (`:1446`, r49) for R48.2/R48.3 | no recurrence yet; r50's `deciding-run.sh:5-8,23-29` carries gate 0 | held so far — the only criterion in the window whose falsifier is a *refusal path in the deciding script* rather than prose |

Classes that recurred and were **closed by a check, with zero recurrence after it** (the other half of
the tracker, same window):

| class | gate | occurrences after the gate |
|---|---|---|
| label-count (R40.4, R44.1) | **Q87** (`:1223`, r45) | 0 — r45–r49 closures contain no count-label defect |
| quote-fold (R46.4) | **Q91** (`:1355`, r47) | 0 — r48 re-checks every Gate quote byte-exact |
| id-collision (R41.6, R42.3) | **tool** `tools/staged-id-guard.py` (r43 C3), not a criterion | 0 — r49's C2 gate is that same guard, sha-pinned |

## 4. Classes that recur with **no** criterion behind them

These are the rows a recurrence criterion has to reach, because nothing else can fail on them.

| class | rows | what recurs | why no gate fired |
|---|---|---|---|
| receipt-not-committed | R45.2, R47.2 | a round cites a `--selftest` tally (or a criterion falsifier) as evidence and commits no `.stdout` for it | no QUALITY criterion requires a committed receipt for a selftest tally. Q88 requires one for the **no-harm falsifier script only**; Q92/Q93 *name* a `--selftest` command as evidence and require no output. Measured: `selftest/*.stdout` under `.ufo/evidence/round-47/selftest/` at tip `03facb22` → **0 files**; round 45 → 0; round 46 → 6; round 48 → 4; rounds 49 and 50 → 4 each. And the criterion-93 falsifier receipt is still absent at base: `git ls-tree -r --name-only HEAD \| grep -c c93` → **0** |
| carried-open | R47.5, R48.4, R49.5 | a `Planned` list that names carried items and a next round that re-lists them instead of working them | the list is prose; nothing compares "named in Planned" with "landed". R47.5 has been carried three rounds and R48.4 two |
| wave-shape | R44.2 (observation), R47.6 | a wave built and not dispatched / below the floor | Q78 settles a *dispatched* wave whose parent exits early and says in terms "prepared specs are not dispatched seats"; Q90 is seat names. Per `corpus/lessons/round-48.md:305` no criterion refuses a round that closes with a declared wave unrun |
| shonen-box-unpromotable | R42.4, R46.5, R47.7, R48.6, R49.6 | the same sentence, five times | promotion is operator-owned; no lane check can close it. Note the lane's *lessons* stop naming it after round 43: `grep -c SHONEN corpus/lessons/round-4{4,5,6,7,8,9}.md` → 0 each. The item survives only in the closure files |

## 5. Items that restate each other (duplicate chains)

Four chains, 18 of the 49 rows. A ledger that scores them as 18 independent dispositions overstates the
surface; a planner should treat each chain as one item plus its carriers.

1. **Anchor refresh / fetch receipt** — R43.3 → R45.4 → R46.1 → R47.5 → R48.4 → R49.5. Closed at r48
   for the four documents (S265–S268 supersede S026/S048/S093/S108); the *carrier* survives because
   R47.5's list also held the dead `brace_depth_at` helpers, the round-47 counter survivors, the
   located-name check and the append-only rule, which r49 and r50 re-list.
2. **SHONEN boxes** — R42.4, R46.5, R47.7, R48.6, R49.6. Verbatim.
3. **Receipt-not-committed** — R45.2, R47.2. Same class, different counters; not a duplicate of object,
   a duplicate of *rule*.
4. **Order-of-scoring** — R48.2, R48.3. The two halves of the round-48 conformance pair (start/exit
   receipts; control order). One gate (Q99) closes both.

Weaker relations worth naming: R40.2 ≈ R41.2 (pointer/receipt resolution, one class); R40.4 ≈ R44.1
(label instances, one class, both still uncorrected — see §6); R41.6 ≈ R42.3 (collision hazard before and
after the guard); R46.3 ≈ R47.1 (dependence declared, then repeatability); R48.2 ≈ R48.3.

## 6. Divergences the planner must decide around

These are tree facts, not judgments; the C1 counter's rules make each of them a disposition problem.

1. **Two items are stale routings — the tree already answered them before they were routed.**
   * **R40.5** (`^\s*leg` vacuous): round 39 replaced the vacuous guard and measured it —
     `SCORECARD.md:1859` `C1_R39: … live_agree=1 stripped_agree=1 r38_regex_hits=0 … C1_R39_PASS=true`,
     "one vacuous guard replaced by a successor that agrees on both probes; the r38 file is unchanged".
     The round-40 closure nonetheless routed it (`round-40-verifier-spotcheck.md:152`,
     `grep -cE '^\s*leg' tools/mutate-and-run.sh` → 0 — which is *the round-39 evidence*, quoted as a
     live defect). A `fixed` row cannot cite a post-routing commit here; the honest statuses are
     `declined` (pre-routing fix) or `open`, and `open` needs the id in `Planned (round 50)`, where it is
     absent.
   * **R45.3** (freshness score jump): the routing round's own block already states the fix —
     `SCORECARD.md:2159` "The round-44 unit stays a monitor". Same disposition problem.
2. **Two items are acknowledged, class-gated, and still uncorrected at the instance.**
   * **R40.4**: `corpus/lessons/round-40.md:14` still reads "Quote (11 words)" for a 13-token quote;
     r41 named the class (`round-41.md:75`), r45 gated it (Q87), no round appended a correction to the
     round-40 label.
   * **R44.1**: `corpus/lessons/round-44.md:26` still reads "line 15, 20 words" (28 tokens); r45 named it
     and Q87 governs it; no correction was appended.
   The class is closed (0 recurrences after Q87); the instances are open at the tree. `fixed` would need a
   keyed excerpt new since routing that *resolves* the label, and there is none.
3. **Two items are absent from `Planned (round 50)` and so cannot be `open` under the C1 counter.**
   * **R49.1** (generator error paths, F1–F3): `Planned (round 50)` names "generator reach (5-cell rows,
     duplicate map keys, numeric order past the digit boundary)" — that is the *reach* finding
     (`T49W2RevGenCode.md` F4/F5/F6), not the error paths at `:16-46` (unreadable guard exits 1 where the
     docstring says 2). No round-50 record mentions the error paths: `grep -o "R49\.[0-9]"
     .ufo/evidence/round-50/contract.json` → no matches; `grep -n "unreadable\|error path"` over the
     round-50 scripts → only `exit 2` argument guards.
   * **R49.6** (SHONEN) and the four earlier SHONEN rows: `Planned (round 50)` does not name them either.
   Both need either a Planned sentence or a `declined` reason ≥ 40 characters.
4. **R47.2's asks are only half met at the tree.** The receipts that exist are for the *successor*
   counters (`.ufo/evidence/round-48/selftest/c1-r48-selftest.stdout`, `c2-r48-selftest.stdout`;
   `.ufo/evidence/round-49/control/c{1,2}-selftest.stdout`), not for the three round-47 counters, and
   `quality/addition-lint.py` has no committed selftest receipt (`find .ufo/evidence/round-48 -name
   '*addition*' -o -name '*lint*'` → empty) and no criterion-93 falsifier receipt exists anywhere
   (`grep -c c93` over the tree → 0). R47.2 is also absent from `Planned (round 50)` except through
   "carried items from round 48's list", which does not name it.
5. **The lane's own records were silent for the one fix that regressed.** R45.2's fix is acknowledged
   only in the closure (`round-46-verifier-spotcheck.md:36`); `grep -n selftest
   corpus/lessons/round-46.md` returns lines 11, 115 and 125 — none about receipts. That silence is the
   mechanism of the r47 regression, and it is why §7's criterion keys on the *class*, not on the round.

## 7. Proposed criterion — only because §4 names a check that fails on a recurrence

**QUALITY criterion 100 — a routed-defect class with a second occurrence is closed by a check, and the
check's falsifier receipt postdates the later occurrence.**

(a) Each `fixed` row of `corpus/routed-defects.json` carries a `class`. (b) A committed class map
`corpus/routed-classes.json` gives, per class with ≥ 2 rows in the round-40..50 window, the gate that
closes it (a criterion number or a tool path) and the committed receipt its falsifier prints. (c) The
class is closed only when the gate exists, the receipt resolves at the revision, and the receipt's commit
is **not older** than the class's last occurrence. A class whose second occurrence postdates its gate's
last green receipt is a miss, not a closed class. (d) The class map is the ledger's companion, not a
second ledger: no row is duplicated, and a class may be closed by a tool (as `id-collision` was).

Cost: two git calls per multi-occurrence class — 12 classes at base, ~24 calls, no network, no clone.

**Falsifier fixture (built and run; receipts in `T50RevengerRecur.receipts/`).** The check is
`recurrence-check.py` (stdlib only). Two fixture repos, each `mktemp -d` + `git init -q`, toplevel
asserted before the first commit:

* **red fixture** — a ledger with R45.2 and R47.2 in class `receipt-not-committed`, and a class map whose
  entry is `{"gate": null}`. This is the *real* lane shape: both items were routed, r46 committed the
  receipts, r47 dropped them, and no criterion names the class.
* **green fixture** — the same ledger with `{"gate": "Q100", "falsifier_receipt":
  ".ufo/evidence/round-50/quality/c100-falsifier.stdout"}` and that receipt committed after the ledger.

Observed (2026-10-26, scratch only):

```
RED   RECURRENCE FAIL receipt-not-committed rows=2 no-gate
      RECURRENCE_CHECK classes=1 multi=1 fails=1          RED_EXIT=1
GREEN RECURRENCE_CHECK classes=1 multi=1 fails=0          GREEN_EXIT=0
```

So the check fails on a recurrence and passes on a closed class — it is able to fail, which is the bar
the lane's criteria 87/91/97/98 set. It would also refuse the two real long-tail classes of §4
(`carried-open`, `wave-shape`) at base for want of a gate, and would pass `label-count`, `quote-fold` and
`id-collision` on the evidence already committed (Q87/Q91 falsifier receipts, the guard's sha-pinned
selftest). It does **not** reach R40.4/R44.1's uncorrected instances or R40.5/R45.3's stale routings —
those are ledger-status problems (§6), which is the right split: criterion 100 governs closure of a
*class*, the C1 ledger governs the disposition of an *item*.

## 8. Artifacts and commands

`T50RevengerRecur.receipts/`:

| file | content |
|---|---|
| `recurrence-walk.json` | the 49 rows of §1 (`schema: tameshi-r50-recurrence-walk-v1`), 27 classes, duplicate lists |
| `build_table.py` | the table builder, so the counts in §2 reproduce from the JSON |
| `recurrence-check.py` | the criterion-100 check used by the falsifier |
| `run-red.txt`, `run-green.txt` | the two observed runs quoted in §7, with exit codes |
| `commands.txt` | every read-only command quoted in this report, in order |

Verification commands used for the divergences (all read-only, all against the lane checkout):

```
git -C LANE ls-tree -r --name-only 03facb22 -- .ufo/evidence/round-47/selftest | wc -l     # 0
git -C LANE ls-tree -r --name-only 3ae8b048 -- .ufo/evidence/round-46/selftest | wc -l     # 6
git -C LANE ls-tree -r --name-only c7586b9a -- .ufo/evidence/round-48/selftest | wc -l     # 4
git -C LANE ls-tree -r --name-only HEAD | grep -c c93                                      # 0
grep -c SHONEN corpus/lessons/round-4{4,5,6,7,8,9}.md                                      # 0 each
grep -o 'R49\.[0-9]' .ufo/evidence/round-50/contract.json | sort -u                         # no matches
grep -n '^\*\*Planned (round 50)' SCORECARD.md                                             # :2410
```

Limits: the class map is my reading of 49 item texts; a different classing would move rows between
classes (the 12 multi-occurrence classes are the ones where the item text names the same object or the
same rule). "Closed" is judged on the tree, not on the prose — which is why four items the lane's prose
calls answered appear as open or stale in §6. I did not re-run any round's counter, so every closed
verdict above rests on a committed receipt line, cited in the table.

## Summary

49 items, 27 classes, 12 with a second occurrence; 32 closed (3 declined), 17 open; median carry for closed items 1 round (26 of 32 closed in one round).
The long tail is not lapsed fixes but items never given one: never acknowledged (R40.2, R40.3), re-classified as disclosed or operator-owned (R40.4, R44.1, R42.2, R42.4-chain), or absent from `Planned (round 50)` (R49.1, R49.6).
Three classes recurred *after* a criterion: monitor-false-red after Q88 (`r48 spot-check:29`), standing rows after Q92 → Q95 (`r47 spot-check:103`), pointers after Q72/73/81/97 (`r48 spot-check:30`).
One class recurs with no criterion at all: receipt-not-committed, r45 → fixed r46 → r47 (`r47 spot-check:23,24`), and R47.2's criterion-93 falsifier receipt is still absent (`grep -c c93` → 0).
Label-count, quote-fold and id-collision held after their gates (Q87, Q91, the staged-id guard): measured rules and a tool stopped their classes; filing rules and routes did not.
Four duplicate chains carry 18 of the 49 rows (SHONEN alone is 5); two routings are stale (R40.5 fixed at r39, R45.3 satisfied at routing) and two instances remain uncorrected while their class is gated (R40.4, R44.1).
Proposed criterion 100: a class with a second occurrence is closed only by a check whose falsifier receipt postdates that occurrence, keyed by a committed class map beside the ledger.
Falsifier observed on two scratch fixture repos: RED (`gate: null`, the real receipt-not-committed shape) exits 1 naming the class; GREEN (gate receipt after the occurrence) exits 0.
