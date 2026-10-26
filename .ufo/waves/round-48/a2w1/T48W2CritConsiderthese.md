# T48W2CritConsiderthese — round-48 considerthese mining (attack report)

Seat: `T48W2CritConsiderthese` (critic, a2w1). Item: attack the round-48 considerthese mining —
section `### considerthese` in `corpus/lessons/round-48.md` at CONTENT `c7586b9a` against the operator
file `considerthese/2026-10-25.md`.

Read-only on the lane checkout: nothing under `corpus/`, `tools/`, `SCORECARD.md` was written; no git
add/commit/checkout/stash, no jj command; no counter was run against the lane (no `--selftest`, no
`--only`, no live C2/C1 invocation); no subagent dispatched; nothing installed or upgraded; no
`agent://all` message. Scratch `/fast/scratch/hyaku/tameshi-r48/T48W2CritConsiderthese` was created for
nine HTTP fetches (each ~109 KiB, total < 1.1 MiB) and removed before this report was written.
Disk guard checked first (`.ufo/evidence/round-48` pass): `/fast` 25 % used, 603 G free, `/tmp` 3 %.

Verdict framing: **the selection is grounded; the landed deliverable is not.** Idea 5 was genuinely
unmined before round 48, and the section lands in the right place with the right citation form — but the
section describes itself as "a table" and carries no table, its citation-count claim is contradicted by
the very file that carries it, its counter-mechanism sentence is contradicted by the frozen counter the
round is scored with, and two of its S108 observations are unbacked prose that nine fresh fetches do not
reproduce. Milestone `considerthese mining grounded?` → **PARTIAL**, not met.

No scored surface moves: the C2 counter reads only `^- C2-QUOTE …` lines of this lesson
(`.ufo/evidence/round-48/freshness/measure.py:105,289`) and the C1 counter reads
`.ufo/evidence/round-47/calibration/statements.json` (`calibration/measure.py:77-78`); neither reads
the considerthese prose. Every finding below is therefore a record-vs-tree defect, not a claim failure.

---

## What I verified as holding (so the findings below are scoped)

| check | command | observed |
|---|---|---|
| idea 5 was unmined before round 48 | `git grep -n "uptake" -- .` | 4 hits: `considerthese/2026-10-25.md:78`, `considerthese/2026-10-26.md:67`, `.ufo/waves/round-48/w1/T48ScoutConsiderthese.md:13,17`, `corpus/lessons/round-48.md:364`. No lesson 1-47 mentions an uptake ledger. |
| lessons 44-47 mined only ideas 1-3 | `grep -n "considerthese" corpus/lessons/round-4[4-7].md` | r44 10-24 p2 (pointer); r45 10-25 p1 (criterion 86) + p2 as data; r46 10-25 p2; r47 10-25 p3. Idea 4 and 5 untouched. |
| no earlier per-proposal accounting under another name | `grep -n "proposal" corpus/lessons/round-4[4-7].md` | 9 hits, each a single-proposal mining note (r44:70,76; r45:130,132; r46:101,105; r47:7) plus one mistakes-table row; none tabulates multiple proposals. |
| the mapping "ideas 1-3 were mined in rounds 45-47" | `corpus/lessons/round-45.md:130`, `round-46.md:101`, `round-47.md:92`; `corpus/QUALITY.md:1174` | holds. |
| landing form cites path + date | `corpus/lessons/round-48.md:364` heading `considerthese/2026-10-25.md` idea 5 (date in the filename, precedent rounds 45-47); `:366` "Operator-authored, read-only"; `:375-376` declares no criterion and no SOURCES row with a reason | conforms to precedent (r46 p2 also landed as a lesson table, no criterion). |
| the operator file was not edited by the lane | `git log --oneline -- considerthese/2026-10-25.md` | one commit, `8ac3174` (operator's own reflection). |
| S108 raw bytes really are fetch-unstable | 9 live `curl` fetches today (table under F3) | 9 distinct sha256 at two byte lengths. The premise the section needs is true; only its two *variant classes* are unsupported. |
| the C2 live check is phrase-based, not byte-based (`:375` second clause "no round-48 check treats a second live fetch as byte-identical") | `measure.py:336-354` | true: `check_live` returns `ok` iff the quote is in `extract(live_bytes)`. |
| idea-4's timestamp argument itself | `git log --format='%h a=%ai c=%ci'` | the four cited pairs share the **author** second (`473336d`/`e73389c` 01:11:52; `0b5b7cd`/`9acfbe2` 20:26:58; `683eedd`/`745a583` 17:45:21; `5891bdb`/`3310e7b` 10:28:28) and differ in committer time. Default `git log` prints the author date, so `round-48.md:367` reproduces as written. Not a finding — recorded because I tested it. |

---

## F1 (material, coverage) — the section says "mined as a table" and lands no table; 3 of 8 absorptions are silently dropped

**Attacked:** `round-48.md:368` "Idea 5 is mined as a table, not a tool" and `:369` "of the eight
absorbed proposals (10-24 p1-p5, 10-25 p1-p3), criteria 79 and 86 were cited … and criteria 76, 78 and
80 were not".

**Evidence.**

```
$ sed -n '362,376p' corpus/lessons/round-48.md | grep -c '^|'
0
$ awk '/^\| proposal \| absorbed/,/^$/' .ufo/waves/round-48/w1/T48ScoutConsiderthese.md | grep -c '^| 10-'
8
```

The 8-row ledger (proposal → absorbed as (round) → later citations → fired on real data) exists only in
`w1/T48ScoutConsiderthese.md` (sha256 `8c28342a67492039…`), which the lesson cites **only** for the
idea-4 sentence (`:368`). The landed section names five criteria for eight proposals and never lands the
three non-criterion absorptions:

| dropped absorption | where it is recorded | command |
|---|---|---|
| 10-24 p5 SHONEN readiness → round-42 lesson table | `corpus/lessons/round-42.md:140-142` | `sed -n '140,150p' corpus/lessons/round-42.md` |
| 10-25 p2 cumulative regression run → round-46 lesson table **and** the round-46 standing-statement counter | `corpus/lessons/round-46.md:101-106` | as cited |
| 10-25 p3 dead-code debt list → round-47 `T47ExecDeadCode.scan.py` scan | `corpus/lessons/round-47.md:92-100` | as cited |

Idea 5's own ask is per proposal: "track each of my proposals with the round and criterion that absorbed
it and whether it later fired on real data" (`considerthese/2026-10-25.md:78-80`). A five-criterion
citation sentence answers one third of that. The section even inherits the scout's own disclaimer
("waves and evidence are not searched, so this is a lower bound") without the table the disclaimer was
written for.

**Impacted axes:** coverage (the mined proposal is not delivered), calibration (a record describes
itself falsely — the same class as the round-48 mistake row 6, `reference-drift`).

**Smallest safe correction:** land the scout's 8-row table verbatim at `:368-371`, with one provenance
line: the report path, the grep command with the per-criterion round lists, and the note that
waves/evidence are unsearched. If the L1 does not want a table, the words "as a table" must go and the
section must name the three non-criterion absorptions in prose.

---

## F2 (material, calibration) — "76, 78 and 80 were not cited after the round that wrote them" is false for 78 in the file that carries it

**Attacked:** `round-48.md:369-370`.

**Evidence** (the section's own command, run at CONTENT):

```
$ grep -lE "(criterion|QUALITY) 78\b" corpus/lessons/*.md
corpus/lessons/round-39.md
corpus/lessons/round-39-verifier-spotcheck.md
corpus/lessons/round-48.md
$ grep -noE "QUALITY (76|77|78|80|86)" corpus/lessons/round-48.md
305:QUALITY 78
309:QUALITY 77
310:QUALITY 86
310:QUALITY 77
```

`round-48.md:305` is the `scope` mistake row: "QUALITY 78 (`corpus/QUALITY.md:931-943`) settles a
*dispatched* wave whose parent exits before seat terminals". That is a later-round lesson citation of the
criterion by the section's own metric, so 78 belongs in the "cited" column — it was also *consulted* and
found insufficient, which is closer to "fired" than anything 79 did in round 47. The same grep also shows
criterion 77 (landed beside 76 by 10-24 p2, `round-38-verifier-spotcheck.md:58`) cited twice in
round 48, invisible to a one-criterion-per-proposal cell.

76 and 80 hold: `grep -lE "(criterion|QUALITY) 76\b"` → `round-38.md`, `round-38-verifier-spotcheck.md`
only; `80` → `round-41-verifier-spotcheck.md` only (same round as its writing).

**Impacted axes:** calibration. This is the class the round-48 mistake row 6 ships a fix for ("every
number a lesson restates from a counter names the receipt line it came from, and the comparison runs"):
the sentence names a command but not its result, and the command contradicts it.

**Smallest safe correction:** either move 78 to the cited column (and say where), or scope the sentence
to "before this round". Cheapest honest form: `criteria 79 and 86 were cited in later rounds, 76 and 80
were not, and 78 was cited once as the rule that did not cover a round-47 defect (§Mistakes row 2)`.

---

## F3 (material, unbacked evidence) — the S108 seven-fetch probe has no receipt, and two of its stated observations do not reproduce

**Attacked:** `round-48.md:372-373` "seven live fetches of the zh-cn page returned HTTP 200 with seven
distinct raw sha256 values (104924, 111405 or 111409 bytes) and, after the amendment-2 extraction of six
of them, two text variants (3496 and 3148 characters)".

**Evidence.**

```
$ git grep -c "dede6ebd\|735ce737\|e0e67e9f" -- .
.ufo/waves/round-48/w1/T48ScoutConsiderthese.md:1
$ cat .ufo/evidence/round-48/freshness/sources/S108.receipt.json
{"url":"…golden_tests?hl=zh-cn","fetched_at":"2026-10-26T08:41:18Z","http_status":200,
 "bytes":111409,"sha256":"04e4c091715a9ee2…"}
```

The seven per-fetch digests exist only as prose in the scout's item (§"Why 5 fits", line 23); no
committed receipt records a per-fetch timestamp/bytes/sha256, and the only committed S108 receipt is the
C2 snapshot's own single fetch. I re-ran the probe (9 fetches, `curl -sS -L`, same URL, scratch dir):

| fetch | bytes | sha256 (first 8) | extract len | quote at | `--update_goldens` |
|---|---|---|---|---|---|
| f1 | 111405 | `b24a7d77` | 3496 | 2513 | yes |
| f2 | 111405 | `5cbb4b57` | 3496 | 2513 | yes |
| f3 | 111409 | `8cf71f56` | 3496 | 2513 | yes |
| f4 | 111409 | `efb62b84` | 3496 | 2513 | yes |
| f5 | 111405 | `4af2a937` | 3496 | 2513 | yes |
| f6 | 111409 | `c2c34999` | 3496 | 2513 | yes |
| f7 | 111409 | `cb7994ed` | 3496 | 2513 | yes |
| f8 | 111409 | `c73dca0f` | 3496 | 2513 | yes |
| f9 | 111409 | `fcb0e468` | 3496 | 2513 | yes |

`count=1` for the S268 quote in every extraction. So the byte-instability premise is confirmed and
stronger than stated (9/9 distinct), but **no 104 924-byte fetch and no 3 148-character variant appeared
in 9 fetches**; if the scout's two-variant split were a 1/3 process (it reports 2 of 6), 9 misses is
~2.6 % likely — possible as a transient devsite variant, but nothing in the repo lets a reader check it.
The sentence's load-bearing conclusion ("the receipt must be bound to the snapshot's own fetch") survives
on the byte-instability fact alone.

**Impacted axes:** freshness (no score movement — the C2 predicate does not read this paragraph),
calibration/QUALITY 2 (a stated measurement with no anchor a reader can re-open).

**Smallest safe correction:** drop `(104924, 111405 or 111409 bytes)` and "two text variants (3496 and
3148)", leaving "the fetches return distinct raw sha256 at 111 405/111 409 bytes, and every
amendment-2 extraction is 3 496 characters carrying `--update_goldens`", **or** commit a seven-line per-fetch receipt
(`fetched_at http bytes sha256 extracted_len`) under `.ufo/evidence/round-48/freshness/` and cite it.
Either way the paragraph needs a receipt pointer; today it has none.

---

## F4 (reference-drift, adjacent to the mining but in the same seat's claim surface) — the S108 quote offset `2 533` is unreproducible

**Attacked:** `round-48.md:78` — "Located quote (amendment-2 extraction; found once, at offset 2 533 of
3 496 characters; **6 tokens**)". This line is in the C2 `S268` supersede block, not in
`### considerthese`, but it is the same S108 observation the considerthese paragraph repeats, so it is in
scope for "is the evidence opened".

**Evidence** (the counter's own extractor, `.ufo/evidence/round-48/freshness/measure.py:166-177`, copied
verbatim and applied):

```
$ python3 - # extract() verbatim from measure.py:170-177
S108.html (round 48 snapshot)          bytes=111409 textlen=3496 quote_at=2513 count=1
round-40/s108/golden_tests.zh-cn.html  bytes=111405 textlen=3496 quote_at=2513 count=1
round-45/freshness/sources/S108.raw.gz bytes=111409 textlen=3496 quote_at=2513 count=1
nine live fetches                      textlen=3496 quote_at=2513 count=1   (all)
```

`2513` is the 0-based index (`t.find`, as the counter uses for substring tests); 1-based it is `2514`.
No extraction variant I tried yields `2533`: spec order (`tags→' '`, unescape, collapse) = 3496/2513;
`tags→''` = 3492/2513; unescape omitted = 3514/2531. "Found once" and "of 3 496 characters" are both
correct; the offset is not.

**Impacted axes:** calibration (a cited number that a reader's re-run contradicts). No scored surface:
the frozen counter tests substring containment and never computes an offset.

**Smallest safe correction:** `at offset 2 513 (0-based) of 3 496 characters`, or delete the offset and
keep "found once".

---

## F5 (scope overreach) — idea 4 is rejected on one of its three declared readouts

**Attacked:** `round-48.md:366-368` "idea 4 (tempo and capacity readout) is not mined and is not
buildable from the repo: [author timestamps rewritten], so no per-round elapsed time can be derived".

**Evidence.** Idea 4 declares three readouts (`considerthese/2026-10-25.md:70-72`): "elapsed time, seats
dispatched versus reported, and commits per claim". Only the first needs timestamps.

```
$ jq '.items|length' .ufo/waves/round-46/spec-w1.json .ufo/waves/round-47/spec-w1.json .ufo/waves/round-47/spec-w2.json
37
40
32
$ ls .ufo/waves/round-46/w1/*.md | wc -l   # reported seats (upper bound; registry has exact members)
40
```

`seats dispatched` is the spec item count (exact); `seats reported` is the registry's terminal or the
report files (the scout itself did this crudely: `ls .ufo/waves/round-N/w1 w2 | grep -c '\.md$'`). `commits
per claim` is a count of `round-N:` commits between the round's claim commits — no timestamps involved.
The operator's next-day file makes exactly this move and reaches a buildable variant:
`considerthese/2026-10-26.md` idea 4 "Host and scratch budget readout … folds in the unmined tempo idea
from 2026-10-25" (scratch use, seats dispatched vs reported, host events from LOG/watchdog lines). The
blanket "not buildable from the repo" is therefore false as stated; only "per-round elapsed time cannot
be derived from commit timestamps" is supported by the evidence given.

**Impacted axes:** coverage (a buildable proposal is pre-refused on a reason that does not cover it),
calibration (overreaching claim).

**Smallest safe correction:** narrow to `idea 4 is not mined; its elapsed-time readout is not derivable
from commit timestamps (…), while seats-dispatched-vs-reported and commits-per-claim would be — the
round mines only idea 5`.

---

## F6 (overgeneralisation) — the "recurring fired / one-off did not" rule is contradicted by two rows of the dropped table

**Attacked:** `round-48.md:371` "Proposals about a thing that recurs every round (a quote, a landing
commit) fired; proposals about a one-off past incident did not."

**Evidence.** Two counterexamples in the scout's own 8-row table (and therefore in the data the section
summarises):

- **10-24 p4, attempt/dispatch health → QUALITY 78.** Wave dispatch and settlement recur every round;
  the criterion has no lesson citation between round 39 and round 48. Under the section's own metric it
  therefore *did not* fire, while its object recurs every round. (Under F2's correction it was
  consulted once in round 48 and found insufficient — which is still not "fired".)
- **10-24 p5, SHONEN promotion readiness → round-42 lesson table.** A standing, every-closure item
  (`considerthese/2026-10-26.md`: "still all four `[~]` through round 47") with no later citation:
  `grep -rn "SHONEN" corpus/lessons/round-4[3-8].md` → only `round-43.md:181` ("C2 measures record
  agreement, not the SHONEN"), not a citation of the table. It is neither a recurring object that fired
  nor a one-off incident, so the dichotomy has no cell for it.

**Impacted axes:** coverage — the sentence exists to serve idea 5's purpose ("so I learn which kinds of
proposals are useful"), and an unfalsifiable rule serves nothing.

**Smallest safe correction:** replace with the measured reading: `criteria whose object a standing
counter re-checks were cited in later rounds (79, 86); criteria written for a single past incident were
not (76, 80); two absorptions (round-42 SHONEN table, round-46 regression table) are unmeasured by this
grep` — and keep the lower-bound disclaimer attached to it.

---

## F7 (material, calibration — strongest single counterexample) — "the snapshot is the only carrier a quote can be located in" contradicts the frozen counter that scores the round

**Attacked:** `round-48.md:374-375` "The snapshot is therefore the only carrier a quote can be located
in".

**Evidence.** The C2 counter locates the quote in the live fetch, and the live result is **required** for
`REFRESHED`:

```
.ufo/evidence/round-48/freshness/measure.py:336-354  check_live(): returns 'ok' iff quote in extract(live bytes)
.ufo/evidence/round-48/freshness/measure.py:432-435  ok = (… and fields['live'] in ('ok','skipped'))
.ufo/evidence/round-48/deciding-run.sh:9,19           "2 C2 (live) once"; measure.py invoked with no --no-live
```

My nine fetches each contained the S268 quote in their amendment-2 extraction (table in F3), i.e. the
live page is a carrier the counter locates the quote in — it is only not a *pinned, byte-stable* carrier.
The second clause of the same sentence ("no round-48 check treats a second live fetch as byte-identical")
is true and is the point; the first clause overstates it and would let a later reader argue that live
checks are useless, which the round's own predicate contradicts.

**Impacted axes:** calibration (a record contradicting the frozen counter it describes; the same class as
round-47's `reference-drift` row, now about the scored mechanism rather than a header line).

**Smallest safe correction:** insert one word — "the only **pinnable** carrier a quote can be located in"
— or rewrite as "the snapshot is the only carrier whose bytes the row's receipt can pin; the live check
locates the same phrase in a fresh fetch but no check treats two fetches as byte-identical".

---

## Impacted axes and what does not move

| axis | effect |
|---|---|
| coverage | F1 and F6: the mined proposal's deliverable (per-proposal ledger) is not landed; its reading rule is unfalsifiable. |
| calibration | F2, F4, F7: three checkable statements fail at the content revision; F3 adds an unanchored measurement; F5 an overreach. All six are record-vs-tree, none is a claim row. |
| freshness | no movement. C2's predicate (`self_pin=1 targets=4 refreshed=4 census_exit=0`) is unaffected; the S108 instability premise is true and is used correctly (phrase-based live check). |
| C1 / census / no-harm | unaffected — the section is not read by `calibration/measure.py` or `no_harm.sh`. |

## Flips (what would make me withdraw a finding)

- F1: a table at `:368-371` in a revision I did not read — I checked `c7586b9a` and the worktree, both
  `grep -c '^|'` → 0, and the section text is byte-identical at `15b1521`.
- F2: a reading of "after the round that wrote them" that excludes the carrying round — then the sentence
  needs that qualifier to be checkable; as printed, its own command returns `round-48.md`.
- F3: a committed per-fetch receipt for the seven probe fetches (none exists: `git grep dede6ebd` hits
  only the report prose).
- F7: a reading of "carrier" restricted to "byte-pinnable carrier" — again a wording fix, not a data fix.

## Provenance

| artifact | sha256 (first 16) | lines cited |
|---|---|---|
| `corpus/lessons/round-48.md` (= `c7586b9a:corpus/lessons/round-48.md`) | `a6d5fd94e0933610` | 78, 305, 309-310, 362-376 |
| `considerthese/2026-10-25.md` | `a062eee9a707350e` | 70-72, 78-80 |
| `considerthese/2026-10-26.md` | `376bddda8045f42d` | status of earlier ideas, idea 4 |
| `.ufo/waves/round-48/w1/T48ScoutConsiderthese.md` | `8c28342a67492039` | 13, 17, 23, 28-35 |
| `.ufo/evidence/round-48/freshness/measure.py` | `faefe9b442741bcd` | 105, 170-177, 289, 336-354, 432-435 |
| `.ufo/evidence/round-48/freshness/sources/S108.html` | `04e4c091715a9ee2` | 111409 B snapshot |
| `.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` | `f27cf274b5dd7c28` | 111405 B snapshot |
| `.ufo/evidence/round-48/deciding-run.sh` | (read) | 9, 19 |
| lane HEAD when read | `17cc5ce` | content `c7586b9a`, one commit after it (spec/dispatch only) |

Limits: nine live fetches today are a sample, not the scout's seven; the 104 924-byte / 3 148-character
variant may be a transient devsite response I did not hit. I did not run the C1 or C2 counters, by
assignment. No counter output is used as a verdict anywhere above. Scratch dir removed; nothing under
`/tmp` written by me (all probe files were under `/fast/scratch/hyaku/tameshi-r48/T48W2CritConsiderthese`).
