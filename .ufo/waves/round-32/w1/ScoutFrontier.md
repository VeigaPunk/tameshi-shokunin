# ScoutFrontier — round 32 wave 1

Verdict: a runner tally audit does not move any frontier row F1–F10 toward Core. The surface is lane ground already held: the lane's own runner. The three planned checks (per-leg presence, an oracle sweep of the tally block, a meta-test of the selftest harness) close a hole the lane already recorded on that same Core surface. They are not an F-row's next move.

No tools installed.

## Frontier rows

`corpus/README.md` `## Frontier` (lines 68–87) is the F-table. Later sections supersede status cells; they do not add a row for the runner tally.

The only row whose wording can be confused with this audit is F8, because the audit's second check is an independent oracle. The row is not that oracle.

```
corpus/README.md:85
| F8 | oracle anchoring as a survivor class | S012 | open | 0 test-oracle lines → one survivor classified against an independently anchored expectation |
```

Round 27 supersedes the status cell, not the ground:

```
corpus/README.md:424-429
F8 moves from open to **partly held**: its next move (one survivor
classified against an independently anchored expectation) is measured, on
one gate at one pin. Hole calls on the other eight recorded legs stay
pristine-differential until anchored. Line 85's F8 row reads "open"; this
section supersedes its status cell, and lines 234-238 above (round 16,
pristine-derived expectations only) describe the state before this round.
```

Round 29 narrows that hold and does not widen it to the runner:

```
corpus/README.md:433-438
F8 correction (round-27 spot-check routed item 4): the round-27 section
above says the F8 next move "is measured" against "an independently
anchored expectation". The entry `knowledge/oracle-anchored-survivors.md`
bounds that to 3 of the 4 survivors anchored in the gate's own header
contract and 1 held by convention only. F8 stays partly held on that
bound.
```

F8's measured object is cite-check hole survivors at one pin. The tally audit does not classify a survivor of a recorded gate. It does not discharge the remaining eight legs. It does not move F8.

Round 30 already placed the tally itself off the frontier:

```
corpus/README.md:449-456
## Round 30 — regression tally completeness (exploratory), S092–S094
| `knowledge/regression-tally-completeness.md` | Core ground (the lane's own runner, `tools/mutate-and-run.sh --regression`), not a frontier move. The tally refuses as SETUP when the counted leg statuses do not add up to the case count; `--selftest` runs the extracted tally block under 23 fixed status vectors and a guard stress case (97 → 106 cases). ...
No frontier row changes status this round (F1–F10 as above).
```

Round 31 repeats the same close (`corpus/README.md:464`): no frontier row changes status.

`PROVINCE.md` agrees, and it has no later append that reopens this surface. The file ends at the round-26 Core append (line 118).

```
PROVINCE.md:36-42
the mutation service and its opt-in protocol
(`corpus/knowledge/service-optin-protocol.md`); this lane's runner,
corpus and source registry (`corpus/SOURCES.md`).

**Frontier** — F1–F10 in `corpus/README.md` `## Frontier`; ground moves
to Core only through an admitted, source-headed `knowledge/` entry
whose `source:` cites a `mined` `SOURCES.md` row.
```

The other rows, as their later sections leave them, are not this audit: F1 report interop is held and F1b NoCoverage stays frontier (`PROVINCE.md:99-105`); F2 and F3 stay partial or open (`corpus/README.md:105-140`); F4 stays open (line 81); F5's finite method is Core for nine named surfaces only (`PROVINCE.md:85-95`, `corpus/README.md:324-338`); F6 was pre-registered with no status change (`corpus/README.md:440-447`); F7 reuse decisions stay open (`corpus/README.md:148-161`, `:255-256`); F9 and F10 stay open (lines 86–87). Rounds 26, 30 and 31 each say no F-row changes (`corpus/README.md:413`, `:456`, `:464`).

What is not already held is the detector's completeness, and that gap is written on the Core entry, not as a new frontier:

```
corpus/knowledge/regression-tally-completeness.md:74
E4 (seat MutateHead, `.ufo/waves/round-30/wC/MutateHead.md`): at `bb681566` eight non-equivalent mutants of the tally and its selftest harness survive the 106-case selftest ... The detector is better than at base, not complete. Routed to round 31.
```

The runner's own harness already checks that the nine `st_*=$?` names are the extraction source, and it drops one operand (`tools/mutate-and-run.sh:1989-1991`, `:2033-2039`). It does not sweep statuses 0–255, and it does not reject a faulty copy of its own harness. Those two checks are new instrumentation on Core ground. They are not an F-row move.

## Where the tally and the harness are described

Root `README.md` does not describe either. Its body is the lane blurb (`README.md:1-14`). No line names `--regression`, the tally, or `--selftest`.

`corpus/README.md:449-456`, quoted above, is the README description: the tally's SETUP refusal, and `--selftest` running the extracted block under fixed vectors (97 cases to 106).

`SKILL.md` does not describe the tally block or the harness. Its three uses of the word "tally" are unrelated (`SKILL.md:232`, `:705`, `:2083`). The closest ledger prose cites the runner header, which is where the tally sentence actually sits:

```
SKILL.md:935-940
- **One command replays every leg.** `bash tools/mutate-and-run.sh
  --regression [--workdir DIR] [--keep]` ...
  Exits0/1/2:
  PASS/FAIL/SETUP (`tools/mutate-and-run.sh:126-136,1273-1294,1364-1384`).
```

That cited header is the tally sentence:

```
tools/mutate-and-run.sh:134-136
# repo/rev/blob, pin mismatch, sweep setup refusal — with no FAIL, or (r30) the
# counted pass/fail/setup statuses do not add up to the case count (SETUP
# "case-tally mismatch"; --selftest runs the tally block under fixed statuses).
```

The guard itself is `tools/mutate-and-run.sh:1453-1460`. The harness is `tools/mutate-and-run.sh:1989-2040` (`tally_line` at 1998, the 9+9 position loops at 2008–2021, the extra vectors at 2022–2031, the missing-operand stress at 2033–2039). `SKILL.md:1002-1008` still records `MUTATE_SELFTEST: 67/67` at `cf41efaa…`. Later pulses in the same file say 80/80 (`SKILL.md:1336`, `:1424`). Neither is the 106-case harness.

The knowledge entry describes the harness's limits at `corpus/knowledge/regression-tally-completeness.md:13-23` and `:64-66`. That file is a live credit input (below). Cite it; do not edit it to document the new tool.

## Cold-read inputs — what not to edit

Credit is the round-18 algorithm, selected unchanged by `.ufo/evidence/round-21/coldread/measure.py:1-22`. An entry matches a SKILL section by the section's own sha256 (`measure.py:609-612`), not by the whole-file `skill_sha256`. `SKILL.md` and the round-17 and round-18 ledger paths are ignored as inputs (`measure.py:132-136`, `inputs_view` at 321–327). Every other `inputs` key is checked: if the blob at the measured rev is not that sha, the entry is `input-drift` and does not credit (`measure.py:348-349`). A section is covered only when at least one matching entry credits and no non-stale failure vetoes it (`measure.py:635-638`). `box3_full_page` is true only when every section is covered (`measure.py:655`).

Observed at `git rev-parse --short HEAD` → `e9f3b95`, comparing each recorded sha to `sha256(git cat-file blob HEAD:path)`. "Eligible" means the class/verdict/count gate would pass (`gap-minor` or `executed-ok` for instruction; `gap-minor` or `verified-record` for record; commands > 0; not a fail verdict). The trace gate was not re-run, so eligible-and-matching is an upper bound on entries an edit would turn into `input-drift`, not a proof those sections credit today.

| Path | Entries listing it | Eligible | Eligible and sha still HEAD | Edit? |
|---|---:|---:|---:|---|
| `SKILL.md` | 50 | 50 | 0 | Ignored as an input. Do not rewrite an existing section: that changes the section sha and unbinds its entries. A new trailing `##` does not rehash earlier sections, but the new section is uncovered until a ledger entry exists, and full-page credit requires every section. |
| `README.md` | 4 | 3 | 3 | Do not edit. All 4 recorded shas are the current blob. |
| `corpus/README.md` | 80 | 75 | 9 | Do not edit. This is where the frontier table and the round-30 tally paragraph live. |
| `PROVINCE.md` | 37 | 33 | 8 | Do not edit. |
| `corpus/knowledge/regression-tally-completeness.md` | 1 | 1 | 1 | Do not edit. The one eligible entry still matches, on SKILL section start 131 (`## Mutation-sweep recipe`). |
| `corpus/knowledge/operator-runbook.md` | 62 | 54 | 44 | Do not edit. |
| `LOG.md`, `SCORECARD.md` | 3 each | 3 | 0 | Already drifted against this ledger. Still listed; not a safe place to sneak a note. |
| `tools/mutate-and-run.sh` | 282 | 250 | 60 | Do not edit. HEAD blob prefix `a7d3f2dd7d47` is the frozen runner pin. C1 also requires that pin. |

Sections that still name a matching doc blob include, among others: `## Standing rules` (start 17), `## Mutation-sweep recipe` (start 131), `## Kill-rate bands` (start 314), `## Restore discipline` (start 375), `## Cross-language divergence` (start 405), `## Third case` (start 668), `## The cadence's first scheduled tick` (start 1155), `### The service's limits` (start 1246), `### The map` (start 1380). One start-131 entry lists `corpus/knowledge/regression-tally-completeness.md` together with `PROVINCE.md`, `README.md` and `corpus/README.md`.

`affected-sections.json` in the same directory is a snapshot at `790abd21` (31 sections, zero `credited: true`). It is not the HEAD credit state. The round-21 ledger is the latest `coldread/ledger.json` on this tree (rounds 16–21 only).

## Smallest safe correction

Do not add a round-32 frontier sentence to `corpus/README.md`, `PROVINCE.md`, `README.md`, or `corpus/knowledge/regression-tally-completeness.md`. Do not edit the runner.

Document the new tool in a new file that no `inputs` key of `.ufo/evidence/round-21/coldread/ledger.json` names. A new `corpus/knowledge/` note qualifies only because it does not exist in that ledger yet; opening it in a later cold-read makes it an input from then on. Do not claim an F1–F10 status change in that note. The honest sentence is the round-30 one: Core ground, the lane's own runner, not a frontier move, with the detector's remaining hole (E4, and the sum-preserving miscount the sum guard does not see) as the reason the external audit exists.
