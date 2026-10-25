seat: T46CritEntryFalseRed
item: overreach attack on `corpus/knowledge/r9-false-red-rate.md` — inference-as-observation, numbers the S260 snapshot does not state, scope creep onto the lane's own verdicts, PROVINCE/QUALITY criteria, and the README round-46 "F3 stays open" claim

# Target and method

Attacked `corpus/knowledge/r9-false-red-rate.md` (40 lines) at content revision
`6f2168e028ce7ff6e82ac92093ac05dd1f147c32` against its own snapshot
`.ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json` and the governing docs.
I am not an author of this entry (author seat: `ScribeEntryFalseRed`, `w1/ScribeEntryFalseRed.md`).
Read before attacking: `.ufo/evidence/round-46/contract.json`, `PROVINCE.md`, `corpus/QUALITY.md`,
`corpus/README.md:570-580`, `corpus/lessons/round-46.md:45-65`, `corpus/SOURCES.md:135`,
`w1/ScribeEntryFalseRed.md`, the package copy, and the S026 snapshot/entry.

No finding is BLOCKING: the C3 predicate (`measure.py`) does not judge prose, and the entry's body carries
the material. The defects below are record defects a reader would take away as true.

All scratch under `/tmp/tameshi-r46-T46CritEntryFalseRed/` (`bodytext.txt`, `extract45.txt`, `live-feed.json`).

# Findings

## F1 — HIGH — the H1 asserts a polarity the snapshot never states, and the entry's own disclaimer retracts it

Attacks: `corpus/knowledge/r9-false-red-rate.md:6`

```
# Four red builds in five are not defects, by the publisher's own numbers
```

Command (word counts over the snapshot's body text; script in scratch, source
`d['entry']['content']['$t']`, tags stripped, whitespace folded):

```
$ python3 - <<'EOF' ... for pat in ['red build','build','defect','legitimate','false']: print(pat,'->',t.lower().count(pat.lower()))
red build -> 0
build -> 4
defect -> 0
legitimate -> 4
false -> 3
```

The word `defect` occurs **zero** times in the snapshot. What the snapshot states is:

```
POST: "about 84% of the transitions we observe from pass to fail involve a flaky test! This causes extra
repetitive work to determine whether a new failure is a flaky result or a legitimate failure."
POST: "In some cases, developers dismiss a failing result as flaky only to later realize that it was a
legitimate failure caused by the code."
```

Three changes are made by the title, none labelled: (a) *involve a flaky test* → *are not defects*
(association → polarity; the post explicitly says the determination is still outstanding);
(b) *transitions from pass to fail* (test-level) → *red builds* (build-level; `red build` count 0);
(c) 84% → "four in five" (0.84 is 4.2/5). The entry's own line 36 says "nothing here measures the lane's own
false-red rate" and line 28's inference says only that a single red is "weak evidence of a defect" — the H1
states the opposite, unconditionally. QUALITY criteria 3 (observation/inference separate) and 1 (every claim
falsifiable or marked opinion) are violated by the title.

Smallest safe correction: retitle to the snapshot's unit and polarity — e.g. `# Most observed pass-to-fail
transitions involve a flaky test, by the publisher's own numbers` — and move the "not a defect" reading into an
`Inference:` bullet carrying the post's own caveat ("This causes extra repetitive work to determine whether a
new failure is a flaky result or a legitimate failure").

Adjacency: the same overreach is in the registry row's claim cell, `corpus/SOURCES.md:135` cell 7 —
"… so legitimate failures get dismissed as false positives and a red build is more likely a flake than a
defect". Fixing only the entry leaves the row carrying the stronger version.

## F2 — HIGH — the quoted sentence is truncated exactly where the snapshot contradicts the inference drawn from it

Attacks: `corpus/knowledge/r9-false-red-rate.md:18` (quote boundary) and `:29` (inference premise).

Entry line 18 quotes `"build monitors typically wait for additional CI cycles to run this test again" (13 words)`
and `"adding to the delay of identifying real problems and increasing the pool of changes that could contribute"`
(17 words). Entry line 29 then states:

```
- **Inference — same-job rerun blindness.** The publisher's default mitigation reruns in later CI cycles, and
  the post reports the wait as a delay, not as identification.
```

Command and output (the snapshot's one sentence, verbatim):

```
$ python3 -c "... t.find('At the very least') ..."
At the very least, build monitors typically wait for additional CI cycles to run this test again to determine
whether or not the test has been broken by a submission adding to the delay of identifying real problems and
increasing the pool of changes that could contribute.
```

The 13-token quote stops one word before `to determine whether or not the test has been broken by a submission`,
which is the post naming the rerun as *the identification step*. "the post reports the wait as a delay, not as
identification" is therefore false against the snapshot: the post reports both, and the delay is the price of
that identification. The quote is legitimately located and fresh (the C3 counter cannot see a truncation), so
this survives every automated check and only a reader catches it.

Smallest safe correction: extend the located quote to `to determine whether or not the test has been broken by a
submission` (or quote the whole sentence) and restate the inference as: the post's rerun *is* the identification
step, and the blindness is that identification is deferred to later CI cycles, not that it is absent.

## F3 — MEDIUM — the entry offers the attempt count as the separating condition; the snapshot's next sentence says the count leaves the determination open

Attacks: `corpus/knowledge/r9-false-red-rate.md:29`, second sentence:

```
A gate that reruns inside one job without a declared attempt count cannot separate "flaked three times in a row"
from "broken" — the post's own declared-flaky mechanism needs exactly three consecutive failures before it will say so.
```

Command and output:

```
$ python3 -c "... t.find('Imagine a 15 minute') ..."
Imagine a 15 minute integration test marked as flaky that is broken by my code submission. The breakage will not
be discovered until 3 executions of the test complete, or 45 minutes, after which it will need to be determined
if the test is broken (and needs to be fixed) or if the test just flaked three times in a row.
```

The post's own mechanism at three consecutive failures still leaves "broken or flaked three times" to be
determined. The entry's sentence is not false (a count is necessary) but it presents the count as the separator
when the snapshot says the count is not sufficient — the omission is the one fact that would change a reader's
verdict rule. Correction: add the post's "after which it will need to be determined … or if the test just flaked
three times in a row" and say the count bounds the wait, not the determination.

## F4 — MEDIUM — a CI-corpus prior is transferred onto the lane's own single-run ledger as a verdict rule

Attacks: `corpus/knowledge/r9-false-red-rate.md:28`, last sentence:

```
The lane's own verdicts are where this bites: a leg that flips a declared class on one run is not yet a kill,
and a gate that fails once is not yet a broken gate.
```

This is inside an `Inference:` bullet (so labelled), but it asserts a lane-wide verdict rule with no measurement,
and the lane's own record contradicts it:

- `corpus/QUALITY.md` criterion 82: "a mutant counts as killed only when the run finishes with parseable output
  and at least one declared check fails" — a completed failing run *is* a kill; no repeat is required.
- `SCORECARD.md` depth axis: "One point per recorded mutation case listed in the tool's pinned replay ledger"
  (`SCORECARD.md:66`, command D) — the nine legs are single-run probes; under the entry's sentence none of them
  would be evidence, and the depth axis would fall to 0.
- The lane's own F3 entry states the opposite precondition: `corpus/knowledge/repeated-control-precondition.md:29`
  — "Neither source prescribes a repeat count for a control — S026's fail-3-in-a-row is a retry-mitigation rule,
  not a control-repeat rule".

Scope creep is the mechanism: Google's post-submit corpus (84% of transitions involve a flake) is applied to a
hermetic fixture counter whose legs are deterministic by construction. Correction: state the precondition
("a gate whose own runs vary"), or drop the sentence; the transfer to this lane's counters is not measured.

## F5 — MEDIUM — "a false-red share of that order" contradicts the entry's own not-claimed line

Attacks: `corpus/knowledge/r9-false-red-rate.md:28` vs `:36`.

`:28` "A verdict rule that reads a single red as a defect carries a false-red share of that order unless it
states an attempt budget or an independent witness." — `:36` "The denominator is not this lane's gate fleet, and
nothing here measures the lane's own false-red rate."

A rule's false-red share is a property of the population it runs on; the entry asserts a share "of that order"
for a verdict rule and then says no such rate is measured here. The `unless` clause does not repair it — it
attaches a Google-scale prior to any rule. Correction: make it conditional ("if a rule ran on a corpus with that
transition rate, …") or drop "of that order".

## F6 — LOW — a relationship attributed to the publisher that the snapshot does not state

Attacks: `corpus/knowledge/r9-false-red-rate.md:37`:

```
- The relationship between the 84% transition rate and the 1.5% result rate is the publisher's; it is not derived here.
```

The snapshot states the 1.5% result rate and the 84% transition rate in different paragraphs and never relates
them (verified by reading the full body text; no sentence carries both figures). "is the publisher's" asserts a
stated relationship that is not there. Correction: "the snapshot states both rates and states no relationship
between them; none is derived here."

## F7 — LOW — a normative rule sits in the observation section

Attacks: `corpus/knowledge/r9-false-red-rate.md:10`: "… so the feed is a second carrier of the same document, not
a second document: the two rows' figures must agree, and opening the feed adds no claim the page does not carry."

"must agree" is a rule, not a state of the snapshot (QUALITY 3). The substantive claim is true and I verified it:
the S026 row (`corpus/SOURCES.md:37`) and the S260 row (`:135`) both state "about 84%", and the feed body adds
nothing (see V3). Correction: "the two rows state the same figure" — or move the "must" into the Inference
section.

## F8 — LOW — interpretation inside "What the snapshot states"

Attacks: `corpus/knowledge/r9-false-red-rate.md:12`: "The rate is a steady state, not a backlog being worked
off". The snapshot says "we see a continual rate of about 1.5%" and "the insertion rate is about the same as the
fix rate, meaning we are stuck with a certain rate" — "steady state" is a fair reading, "not a backlog being
worked off" is the entry's gloss. Correction: quote "we are stuck with a certain rate" or move the gloss to
`Inference:`.

## F9 — LOW — "the post's own gate" reframes a mitigation option as a gate

Attacks: `corpus/knowledge/r9-false-red-rate.md:20`: "The post's own gate is \"causing it to report a failure only
if it fails 3 times in a row\"". The snapshot: "We have several mitigation strategies … We even have a way to
denote a test as flaky - causing it to report a failure only if it fails 3 times in a row." It is a per-test flag
among several presubmit mitigations, not a gate the post owns. Correction: "The post's declared-flaky option is".

## F10 — LOW — paraphrase outside the quotes narrows the post's clause

Attacks: `corpus/knowledge/r9-false-red-rate.md:14`: "… occasionally fail (15 words) in a way the code change did
not cause." Snapshot: "more than 1 in 7 of the tests written by our world-class engineers occasionally fail in a
way not caused by changes to the code or tests." The paraphrase drops "or tests", narrowing the exclusion to code
changes only. Correction: "in a way not caused by changes to the code or tests".

## F11 — INFO — the second ground axis is unrecorded in the round's frontier note

Attacks: `corpus/knowledge/r9-false-red-rate.md:4` (`ground: … F7 (incremental re-sweep granularity) — what a
rerun attempt costs in discovery latency`) versus `corpus/README.md:577` and `PROVINCE.md` round-46 append, both
of which name F3 only. `corpus/README.md:84` still records F7 `open`. No false claim is made (the entry claims no
F7 movement); the asymmetry is that the entry grounds two frontier axes and the round's frontier note records one.
No correction required if the intent is a reading; otherwise name F7 in the round note.

## F12 — HIGH (adjacency) — the README and lesson carrier rationale for S260 is false, and the entry says so

Attacks: `corpus/README.md:577` — "S260 is the publisher's per-post feed record of the same post, adopted because
the rendered page's body sits in a script template that the lane's HTML extraction discards." — and
`corpus/lessons/round-46.md:59-61` — "The new row is the publisher's per-post record, whose body the lane's HTML
extraction can read (the rendered page keeps it in a script template), so the claim becomes re-checkable by the
counter."

Commands and outputs:

```
$ python3 - <<'EOF'  # feed body text vs S026.raw.gz page text, tags stripped
page bytes: 236374 84% count: 2 hardly a perfect solution count: 2
body text inside page text: True
body sentences: 38 missing from page: 0

$ python3 .ufo/evidence/round-45/freshness/measure.py --extract .../S026.raw.gz > extract45.txt
exit=0
26626 extract45.txt
$ grep -c "84% of the transitions" extract45.txt
1
$ grep -o "hardly a perfect solution" extract45.txt | wc -l
1

$ python3 -c "import measure; print('has84 =', '84% of the transitions we observe from pass to fail' in m.norm_text(page_bytes))"
counter norm_text(page): has84 = True
counter norm_text(page): has hardly = True
```

`corpus/knowledge/repeated-control-precondition.md:3` (the S026 header) already documents the shape: the page
"serves its post body twice — a `text/template` copy and a `<noscript>` copy". The lane's extractor reads it; the
round-46 counter's own `norm_text` reads it. So the rationale is false on both carriers, and it is the *reason*
given for opening row S260.

The entry is the correct record here: `r9-false-red-rate.md:10` says "opening the feed adds no claim the page does
not carry" — verified true (all 38 body sentences present in the page text). The entry and the README/lesson
therefore contradict each other, and the entry is right.

This was already reported by the authoring seat (`w1/ScribeEntryFalseRed.md`, finding 1: the page "holds the body
twice — `84%` occurs 2 times, of which 1 occurrence sits inside a `<script>` block", extractor output contains
"84% of the transitions") and landed anyway. Severity HIGH because the README/lesson sentence is the round's
stated justification for a registry row and it is refuted by the lane's own extractor output.

Smallest safe correction: replace the rationale with the true one — S260 is a second, machine-checkable carrier
of a document the lane already holds as S026, adopted for a per-post record with a pinned digest, and it adds no
claim S026 does not carry; delete "sits in a script template that the lane's HTML extraction discards" from both
files (append-only errata in the lesson).

## F13 — LOW (adjacency) — "gains three published measurements" overstates r9's contribution

Attacks: `corpus/README.md:577` first sentence ("gains three published measurements") versus
`corpus/lessons/round-46.md:61-62` ("Two of the three entries are on unheld ground (clustering, the
same-job-rerun blind spot); this one is not, and the round does not claim it as expansion"). For r9 the 84% figure
was already held at S026 (`corpus/SOURCES.md:37` cell 7: "about 84% of pass-to-fail transitions involve a flaky
test"). The lesson is honest; the README aggregate is not, for one of the three. Correction: "gains two new
measurements and one carrier repair".

# What I attacked and found clean (no defect)

- **V1 quote inventory.** Imported the counter's `QUOTE_RE`/`fold`/`norm_text` from
  `.ufo/evidence/round-46/coverage/measure.py` (functions only, no counter run): `quotes 20`, all 20 located in
  the folded snapshot, `located 20 fresh 16`, `located outside 6..25: []`. The 18 `(N words)` labels equal the
  measured whitespace-token counts in order (`15 14 11 13 15 15 13 17 12 9 15 14 16 18 19 20 16 17`) — QUALITY
  criterion 87 satisfied; the letter-and-digit counts differ on four quotes (14/15, 15/16, 12/13, 18/19), which
  criterion 87 explicitly allows.
- **V2 snapshot facts on line 1.** `wc -c` → `8353`; `wc -l` → `0`; `sha256sum` →
  `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929`. `entry.content.$t` exists and holds the
  body. `entry.link` carries `{"rel":"alternate","href":"https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html"}`
  — the entry's locator at line 10 is exact. `published` `2016-05-27T17:31:00.000-07:00`; body opens "by John
  Micco"; the source line's "(Micco, 2016-05-27)" is supported.
- **V3 carrier claim at line 10.** Verified true (F12 commands): all 38 body sentences occur in the page text.
- **V4 recheck line.** `grep -c '84% of the transitions we observe from pass to fail' <snapshot>` → `1`;
  `grep -c 'Almost 16% of our tests have some level of flakiness' <snapshot>` → `1`; live re-fetch
  `curl -fsSL 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' | sha256sum` →
  `434d8658…9929  -`, byte-identical to the committed snapshot.
- **V5 "S026-ground" attribution at line 16.** `grep -n "84%\|transitions we observe" corpus/knowledge/repeated-control-precondition.md`
  → `20:- transitions (`:1132`): "about 84% of the transitions we observe from pass to fail involve a flaky test"`;
  that entry's header line 1 cites S026. Accurate.
- **V6 dropped package arithmetic at line 39.** Package copy lines 21-25 carry "0.02 cents", "$5.67" and
  "over 95 %"; `grep -rn "0\.02\|5\.67\|95 %\|over 95" corpus/` → only `corpus/lessons/round-46.md:82,109`
  (prose naming them as rejected), no registry row. "the lane holds no row carrying those prices" is true.
- **V7 QUALITY criteria satisfied.** 7 (entry lands with its row and README index): `corpus/README.md:575`
  backticks `knowledge/r9-false-red-rate.md`, row `corpus/SOURCES.md:135` carries `used-by`. 79 (located quote
  needs a committed snapshot): snapshot committed, 20 quotes located. 87: see V1.
- **V8 PROVINCE.** No sibling lane is named (`grep -nE 'kumitate|kagi|tsukuroi|mado|kaidoku|kama|sibling'` → no
  hits), so no sibling-gate claim can be false. Nothing is absorbed: no tool, no rule, no sibling surface is
  adopted, and flaky-test engineering stays reported. Bullets 3-4 (`:30-31`) discuss a rerun budget and a
  detection floor, which is the adjacent territory `PROVINCE.md` round-46 append names — they are labelled
  `Inference:` and adopt nothing, so no absorption violation; the residual defect is F5's transfer and, at
  `:31`, the unbacked lane-wide rule "it belongs in the claim, not in the report" (no QUALITY criterion or
  measurement is cited for it) — INFO, in-province craft but unsourced.
- **V9 "F3 stays open" honesty.** `corpus/README.md:80` records F3 `open`; the entry at `:40` claims no
  measurement of the lane's controls and no status change. The status claim is honest. What it delivers is a
  reading of a publisher's rate, not a lane measurement — consistent with the frontier note. The dishonest part
  of the round-46 section is not the F3 status but the carrier rationale (F12) and the "three published
  measurements" aggregate (F13).

# Unreproduced

None. Every finding above was reproduced with the command shown; none is reported on inference alone.

# Bounds and tooling

- Read-only on the lane; wrote only this report file. No `git`/`jj` mutation in the lane, no fixture repo
  created, no counter run as a verdict (only `measure.py` functions imported for tokenization and one
  `--extract` run of the round-45 freshness tool, which is a read-only extraction, not a score).
- One network read: `curl -fsSL` of the frozen feed URL to re-verify the recheck digest (V4).
- No install, no upgrade, no pacman transaction. Scratch: `/tmp/tameshi-r46-T46CritEntryFalseRed/`.
