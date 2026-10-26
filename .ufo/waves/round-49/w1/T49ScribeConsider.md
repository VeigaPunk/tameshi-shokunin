# T49ScribeConsider — `considerthese/2026-10-26.md` proposal 3, grounded on rounds 40–48

Seat: T49ScribeConsider (scribe/consideration, wave 1, round 49). Item: mine ONE still-unimplemented
proposal — proposal 3 of `considerthese/2026-10-26.md` (operator-authored, read-only, **not edited**):
the recurring-defect tracker for closures (`considerthese/2026-10-26.md:80`). This report grounds it on
the lane's own bar and proposes a QUALITY criterion only because a recurrence is shown (§5).

I decided no claim, ran no counter, and did not re-run any round's work. Everything below is read from
committed bytes at the lane checkout; the two places where I re-derived a closure's statement are
marked *re-derived* and carry the command.

## 0. Corpus opened and counting rule

All nine closure files were opened in full:

```
corpus/lessons/round-40-verifier-spotcheck.md … round-48-verifier-spotcheck.md   (9 files, 79–320 lines each)
```

Rule used for "status-neutral conformance defect and routed defect":

* **row** = one numbered item in a spot-check's `Step-1 conformance` / `Conformance defects` block, or one
  item in its `Routed defects` block, that names something wrong with the round's *form* (evidence,
  pointers, receipts, records, wave, order) rather than with the round's measured claim;
* **excluded**: `SHONEN` hand-off lines (operator-owned, `round-46:103`, `round-47:109`, `round-48:119`),
  observations a closure itself labels "not a defect" (`round-44:74`), and a warning a closure labels
  expected (`round-48:31`);
* where a conformance item is restated as a routed item in the same file (`round-43:12`→`:64`,
  `round-45:19a`→`:86`) the row is listed once, at the first place it appears;
* "routed-to" is the routing the spot-check itself records, or — where the spot-check records none —
  the criterion whose written text governs the class, marked **[I]** (inference from criterion text).
  Criterion line numbers are `corpus/QUALITY.md` headings (e.g. `Q88:1291`).

**Result: 44 defect rows, 26 classes, 10 recurring classes.** (Round 40: 5 · 41: 7 · 42: 3 · 43: 3 ·
44: 1 · 45: 5 · 46: 5 · 47: 8 · 48: 7 — counted from the table below by a script, not by eye.)

## 1. The table

| # | round | defect (file:line) | class | routed-to | recurred-in |
|---|---|---|---|---|---|
| 1 | 40 | lesson quarantine summary contradicts its own table (`round-40:293`) | record-drift | round-41 lesson §Correction (`round-41:28`); Q35:262 | 47:25; 48:30b |
| 2 | 40 | wave-grant ledger line not closure-resolvable (`round-40:303`) | pointer-unresolvable | Q72:846; Q73:860 | 41:70; 48:30a |
| 3 | 40 | both assimilation id lists not pasted into the report (`round-40:308`) | prompt-item-unmet | — (report-text form only) | — |
| 4 | 40 | S152 quote labelled "11 words", 13 tokens (`round-40:312`) | label-count | Q87:1223 (written r45) | 44:73 |
| 5 | 40 | round-38 `^\s*leg` guard still matches 0 lines (`round-40:314`) | guard-vacuous | carried, no criterion | — |
| 6 | 41 | m8 `BACKTICK_RE` spans newlines, skips cited paths (`round-41:69`) | instrument-defect | fixed in r42 (line-scoped m8) | — |
| 7 | 41 | residual receipt asserts `present:false` for a later-written file (`round-41:70`) | pointer-unresolvable | Q81:1001 (presence receipt after its writes) | 48:30a (class) |
| 8 | 41 | carried: C1 counter has no self-pin; m7/m8 vacuous without records (`round-41:71`) | instrument-defect | r42 successor counter | — |
| 9 | 41 | carried: three v3 `unflagged` false positives (`round-41:72`) | instrument-defect | r42 v4 | — |
| 10 | 41 | carried: v3 docstring "NOT resolved" overstates scope (`round-41:73`) | doc-overclaim | r42 docstring correction | — |
| 11 | 41 | staged ids S153/S154 collide with the round's own rows (`round-41:74`) | id-collision | renumber-by-document-in-scratch rule | 42:114 |
| 12 | 41 | SOURCES bullet list split by a blank line (`round-41:75`) | format-cosmetic | — | — |
| 13 | 42 | two declared mutants survive unclassified (`round-42:104`) | survivor-open | Q83:1049 | — |
| 14 | 42 | m10 content-blind; m8 scope limit (`round-42:109`) | instrument-limit | none (disclosed, no action) | — |
| 15 | 42 | staged set collides with six lane rows (`round-42:114`) | id-collision | `tools/staged-id-guard.py` (r43 C3) | — |
| 16 | 43 | committed wave-1 note dirty in the worktree at closure (`round-43:12`, disposition `:64`) | record-mutation | reconcile in r44 | 47:22 |
| 17 | 43 | SCORECARD `unknown S256` citation at the landing revision (`round-43:63`) | record-citation-unknown | r44 assignment-mask control | — |
| 18 | 43 | S089 anchor digest stale against live bytes (`round-43:65`) | stale-anchor | append-only supersede row | 45:88; 46:99 |
| 19 | 44 | Stryker quote labelled "20 words", 28 tokens (`round-44:73`) | label-count | Q87:1223 | — |
| 20 | 45 | no committed `--selftest` stdout for either counter (`round-45:19a`, routed `:86`) | receipt-not-committed | round fix: receipts committed in r46 (`round-46:36`) — no criterion | 47:23 |
| 21 | 45 | dead wave-2 seat + duplicate Mut seats (`round-45:19b`) | wave-shape | Q90:1335 | — |
| 22 | 45 | no-harm monitor prints false red (`round-45:85`) | monitor-false-red | Q88:1291 (lesson at 1303 names this defect) | 48:29 |
| 23 | 45 | freshness score 1→9 under a changed formula (`round-45:87`) | measure-definition-change | cite the 0→71 count as the comparable measure | — |
| 24 | 45 | five anchor-refresh candidates stay open (`round-45:88`) | stale-anchor | `round-46:99` | 46:99 |
| 25 | 46 | S259 lesson quote prints hyphen for en dash (`round-46:20b`) | quote-fold | Q91:1355 | — |
| 26 | 46 | anchor refresh not worked; stays open (`round-46:99`) | stale-anchor | r48 C2 (four rows re-anchored) | — |
| 27 | 46 | hardened counters not adopted as operative (`round-46:100`) | capability-not-operative | Q93:1371 | — |
| 28 | 46 | three standing statements depend on host, undeclared (`round-46:101`) | standing-row-unreproducible | Q92:1363 | 47:103 |
| 29 | 46 | lesson quote fidelity: print the fold or the dash (`round-46:102`) | quote-fold | Q91:1355 | — |
| 30 | 47 | wave 2 (32 seats) built, never dispatched; below floor (`round-47:21`, `:108`) | wave-shape | protocol floor only; Q90 does not reach it | — |
| 31 | 47 | seat report rewritten after the report landed (`round-47:22`) | record-mutation | carried: `round-48:117` append-only rule | — |
| 32 | 47 | counter selftest tallies not committed as L1 receipts (`round-47:23`) | receipt-not-committed | `round-47:104` | — |
| 33 | 47 | criterion 93 falsifier output uncommitted (`round-47:24`) | receipt-not-committed | `round-47:104` | — |
| 34 | 47 | lesson dependence sets disagree with the standing rows (`round-47:25`) | record-drift | `round-47:105`; Q92:1363 | — |
| 35 | 47 | standing value restated from one observation (`round-47:103`) | standing-row-unreproducible | Q95:1400 | — |
| 36 | 47 | refusal cites a weaker adjacent line (`round-47:106`) | weak-citation | Q94:1382 | — |
| 37 | 47 | carried items still open (`round-47:107`) | carried-open | `round-48:117` | 48:117 |
| 38 | 48 | two orchestrator salvages under the lane identity (`round-48:26`) | attribution-salvage | disclosed, no action | — |
| 39 | 48 | C1 controls scored after the deciding run (`round-48:27`) | order-of-scoring | `round-48:116`; round-49 contract gate 0 | — |
| 40 | 48 | five `--only` previews at C, undisclosed (`round-48:28`) | order-of-scoring | `round-48:116` | — |
| 41 | 48 | `FROZEN_UNCHANGED=0` false red (`round-48:29`) | monitor-false-red | `round-48:115` (drop receipt dirs) | — |
| 42 | 48 | lesson cites `SOURCES.md:140/141` for S267/S268; rows at 142/143 (`round-48:30`) | pointer-unresolvable | `round-48:118`; Q97:1428 | — |
| 43 | 48 | SCORECARD "pasted byte-exact" false for the three axis rows (`round-48:30`) | record-drift | `round-48:118` | — |
| 44 | 48 | cold-read credit 60→57 on the content revision (`round-48:114`) | coldread-credit-loss | Q98:1436 | — |

*Re-derived, row 42* — the closure says the lesson "cites `corpus/SOURCES.md:140-141`"; the lesson
actually carries two single-line cites, both off by two rows, pointing at S265/S266:

```
$ git -C "$L" show c7586b9a:corpus/lessons/round-48.md | grep -nE 'SOURCES\.md:1[0-9]{2}'
62:- Row change: `corpus/SOURCES.md:140` appends S267 as `docs`/`A`/`mined`, opened 2026-10-26, recheck
84:- Row change: `corpus/SOURCES.md:141` appends S268 as `docs`/`B`/`mined`, opened 2026-10-26, recheck `180d`,
$ git -C "$L" show c7586b9a:corpus/SOURCES.md | grep -nE '^ {0,3}\| S26[5-8] '
140:| S265 | … 141:| S266 | … 142:| S267 | … 143:| S268 | …
```

The defect stands and is sharper than reported: each cite lands on the *previous* row.

## 2. Recurrence count

* **10 of 26 classes recur in a later round**: record-drift (40,47,48), pointer-unresolvable (40,41,48),
  stale-anchor (43,45,46), label-count (40,44), id-collision (41,42), receipt-not-committed (45,47),
  monitor-false-red (45,48), wave-shape (45,47), record-mutation (43,47), standing-row-unreproducible
  (46,47).
* Those 10 classes carry **24 of the 44 rows** (54.5 %). The other 16 classes occur once each (20 rows).
* Three classes recur **twice or more**: record-drift ×3, pointer-unresolvable ×3, stale-anchor ×3.
* The class the operator's reflection names as the example — "selftest tallies cited but not committed
  as receipts (round 45, fixed in 46, back in 47)" (`considerthese/2026-10-26.md:56`) — is confirmed
  and is the one recurrence that has **no criterion** behind it (§4).

## 3. Recurrences that came *after* a QUALITY criterion was written for the class

| class | criterion written for it | later occurrence (spot-check line) | what the criterion did not reach |
|---|---|---|---|
| pointer-unresolvable | Q72 (`QUALITY.md:846`, "a pointer must name a file that exists at write time") + Q73 (`:860`, "closure-resolvable control") | `round-41:70`; then Q81 (`:1001`) written for the receipt form; `round-48:30` again | 72 is a write-time existence test; 81 binds a presence receipt to its writes; neither covers a *line span that lands on the neighbouring row* (34 covers line anchors only into files the lane does not own) |
| record-drift | Q35 (`:262`, append-only correction names false text and both revisions) | `round-47:25`; `round-48:30` | 35 fixes how a correction is *filed*, not whether the prose matches the table it summarizes |
| monitor-false-red | Q88 (`:1291`; its lesson at `:1303` names `round-45:85` as the case) | `round-48:29` | 88 requires monitors green **at base before the freeze**; the r48 red came from the *frozen-path list including the round's own new receipts* — a self-referential input, not a base-run monitor |
| standing-row-unreproducible | Q92 (`:1363`, `deps` clause + tool sha) | `round-47:103` (one-observation row) | 92 states what a statement depends on; it does not count observations — that gap became Q95 (`:1400`) |
| receipt-not-committed | **none** — closed in r46 by committing the receipts (`round-46:36`, `round-46:95` records it as "defect 2 … → `selftest/c{1,2,3}-selftest.stdout` committed") | `round-47:23` and `round-47:24` | no criterion ever required the receipt, so nothing could fail when round 47 dropped them |

Byte-level confirmation of the last row, re-derived (read-only `git ls-tree`, no counter run):

```
round-45 @ ea25e022  selftest_stdout=0   falsifier_stdout=quality/c86-falsifier.stdout quality/c87-falsifier.stdout
round-46 @ 3ae8b048  selftest_stdout=3   falsifier_stdout=quality/c88-90-falsifiers.stdout
                     (selftest/c1-selftest.{stdout,exit}, c2-*, c3-*)
round-47 @ 8b0e15d2  selftest_stdout=0   falsifier_stdout=quality/c91-92-falsifiers.stdout      ← c93 absent
round-47 @ 03facb22  no .ufo/evidence/round-47/selftest/ directory at all (tip, not only C)
round-48 @ c7586b9a  selftest_stdout=3 ; @ 98e63044 also quality/c94-96-falsifiers + coldread-precheck receipts
```

Round 47's closure head `03facb22` still carries neither the counter tallies nor the criterion-93
falsifier, so the recurrence is not an artefact of measuring at the content revision.

## 4. Criteria that held (the tracker discriminates)

| class | criterion | occurrences after it | evidence |
|---|---|---|---|
| label-count | Q87 (`QUALITY.md:1223`) | **0** | no count-label defect in `round-45:19–88`, `round-46`, `round-47`, `round-48`; the r48 quotes are counted ("at 15, 21, 25 and 6 tokens", "25 tokens, at the limit and not over") |
| quote-fold | Q91 (`:1355`) | **0** | `round-48` re-checks every Gate quote byte-exact with amendment 2's procedure; no fold defect reported |
| id-collision | tool, not criterion (`tools/staged-id-guard.py`, r43 C3) | **0** | the round-49 contract's C2 gate is that same guard, sha-pinned |
| capability-not-operative | Q93 (`:1371`) | 0 | r47 C2 `killed=183 applicable=183` |

This is the tracker's useful half: two criteria (87, 91) closed their class with zero recurrence on a
4-round and a 2-round observation window, and one class (id-collision) was closed by a **tool** rather
than by prose. Small N — stated as sample size, not as effect size.

## 5. Proposed criterion (only because §2 shows recurrences)

**Criterion 99 — a tally is evidence only as a committed receipt, and a recurring class is closed by a
check, not by another route.**

(a) Every count a round's records cite as its own evidence — a counter's `--selftest` tally, a
criterion's falsifier output — is carried by a `.stdout` receipt inside that round's evidence tree at
the revision the record names, and the record names the receipt. A tally that exists only in prose or
only in a seat report is not evidence: it is a claim about a run nobody can re-read. The round's
deciding script refuses a record whose tally has no committed receipt. (b) When a routed defect class
recurs in a later round, the repair is a check with a falsifier — the recurrence is not closed by a
second route, a note, or a carried item.

Falsifier that must fail (the round-45 and round-47 shapes fail; round 46 and round 48 pass; shown able
to fail on real bytes by the §3 transcript):

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
probe(){ rev=$1; d=$2
  n=$(git -C "$L" ls-tree -r --name-only "$rev" -- ".ufo/evidence/$d" | grep -cE 'selftest[^/]*\.stdout$')
  f=$(git -C "$L" ls-tree -r --name-only "$rev" -- ".ufo/evidence/$d" | grep -cE 'falsifier[^/]*\.stdout$')
  printf '%s %s selftest_stdout=%s falsifier_stdout=%s\n' "$d" "$rev" "$n" "$f"; }
probe ea25e022 round-45   # red shape: 0 selftest receipts
probe 3ae8b048 round-46   # green shape
probe 8b0e15d2 round-47   # red shape again: 0, and no c93 falsifier
probe c7586b9a round-48   # selftest green at C; c94-96 lands on the receipts tail (98e63044)
[ "$(probe 8b0e15d2 round-47 | sed 's/.*selftest_stdout=//;s/ .*//')" -eq 0 ] || { echo "CRITERION-99-FALSIFIER-VACUOUS"; exit 1; }
echo "CRITERION-99-FALSIFIER-OK"
```

Observed when I ran it (2026-10-26, lane checkout, read-only):

```
round-45 ea25e022 selftest_stdout=0 falsifier_stdout=2
round-46 3ae8b048 selftest_stdout=3 falsifier_stdout=1
round-47 8b0e15d2 selftest_stdout=0 falsifier_stdout=1
round-48 c7586b9a selftest_stdout=3 falsifier_stdout=0
CRITERION-99-FALSIFIER-OK
```

The judge is taken at the revision a record names, so round 48's falsifier receipt is counted at its
tip `98e63044` (`quality/c94-96-falsifiers.stdout`, plus both coldread-precheck receipts), which is the
receipts-only tail criterion 86 permits; at C the selftest receipts alone are already present.

**Amendment to Q88 (not a new number):** a freeze/self-identity check's input list excludes the
artifacts the round itself writes; a red whose cause is the check's own input set prints that input
list and is reported as self-referential, never as drift. Lesson: `round-48:29` with the routed fix at
`round-48:115`; this is the one shape criterion 88's base-run clause cannot reach.

## 6. Lesson

The lane's own closure ledger, read as a series rather than one round at a time, shows that **a routed
defect is not a closed defect**. Twenty-four of forty-four status-neutral defects in rounds 40–48 fall
into ten classes that return in a later round, and four of those classes returned *after* a QUALITY
criterion had been written for them — pointer-unresolvable three times under three different criteria
(72, 81, 97), record-drift after 35, monitor-false-red after 88, standing-row-unreproducible after 92 —
while a fifth, receipt-not-committed, returned although no criterion had ever been written for it.
The two criteria written as *measured* rules rather than as filing rules (87 for quote counts, 91 for
byte-exact quotes) show no recurrence; the classes that kept returning were the ones closed by a
route, a note, or a carried item. The operator's own example, proposal 3 of
`considerthese/2026-10-26.md` (2026-10-26, line 80) — "uncommitted selftest receipts: round 45, fixed
in 46, back in 47" — is exactly this shape: round 46 fixed it by committing the receipts and no
criterion was written, so nothing could fail when round 47 dropped them (verified at
`.ufo/evidence/round-47/` at `03facb22`: no `selftest/` directory, no criterion-93 falsifier stdout).
"A recurrence means the fix did not stick and should become a gate, not another note" is therefore not
a preference but the observed difference between the classes that stopped and the classes that did not.
The tracker itself needs no new data source: every input above is already committed, and the two
commands that produce the count are a `grep` over nine files and a `git ls-tree` per round.

## 7. Limits

* Sample: 9 closures (rounds 40–48), 44 rows. No statistical claim; the recurrence counts are counts of
  listed items, not rates over a population.
* Conformance defects are the closures' findings. I re-derived only rows 42 (§1) and the receipt
  inventory (§3); the rest are quoted with file:line and not re-investigated.
* "routed-to" cells marked **[I]** infer a criterion from its text where the spot-check records no
  routing (rows 7, 34, 42). Rows with no criterion say so.
* Rounds 40–44 predate criteria 86–98, so an early row cannot have been criterion-routed; the
  recurrence column, not the routed-to column, is what carries the finding.
* I ran no counter, decided no claim, and did not read the hidden C2 panel, the `c2-*.stdout` control
  receipts, or anything under `/home/vgpnk/.local/state/`. Scratch: none created; no files written
  except this one. Tools installed: none.
* `considerthese/2026-10-26.md` was read, not edited.

## Summary

9 closures (rounds 40–48) yield 44 status-neutral defects in 26 classes; 10 classes recur, carrying 24 rows.
Measured-rule criteria held (Q87 label-count, Q91 quote-fold: 0 recurrences); filing-rule criteria did not
(pointer-unresolvable under Q72/73→Q81→Q97; record-drift after Q35; monitor-false-red after Q88; standing rows after Q92).
The operator's example — uncommitted selftest/falsifier receipts, r45 → fixed r46 → back r47 — is confirmed at byte
level (round 47 @ `03facb22`: no `selftest/` directory, no c93 falsifier receipt) and is the one recurrence with **no** criterion.
Proposed: **QUALITY criterion 99** (a tally is evidence only as a committed receipt; a recurrent class is closed by a check
with a falsifier), plus an input-set clause amending Q88; its falsifier fails on the r45/r47 trees and passes on r46/r48 as observed.
