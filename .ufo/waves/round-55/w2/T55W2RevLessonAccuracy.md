# T55W2RevLessonAccuracy — attack on `corpus/lessons/round-55.md` at C0

seat: reviewer (wave 2, falsify). item: read `corpus/lessons/round-55.md` at
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` and check every number, path and claim —
(a) the Gate's word counts and locators against the committed snapshots, (b) the
`## Mistakes` entries as real mistakes with falsifiable fixes, and whether the second
one describes what the counter actually did, (c) the R54 dispositions against
`SCORECARD.md` `## Round 55 - round-54 record corrections`, (d) the `cannot_see` list
against the counter and gate code.

method: `git show <C0>:<path>` blobs only; every execution on a `git clone --shared`
fixture under `$HYAKU_SCRATCH/tameshi-r55/T55W2RevLessonAccuracy` (toplevel asserted
before any commit) or on a `git archive` copy of the lane's `corpus/`; no lane file,
frozen file or wave spec touched. No language server is mounted in this seat, so
caller/definition checks are git-blob and counter-code reads (recorded as a gap, not
as proof of absence). Nothing installed; pacman not used.

runnable receipt: `T55W2RevLessonAccuracy-receipts/commands.sh` (exit 0) with its
transcript `T55W2RevLessonAccuracy-receipts/commands.out` (160 lines, sections 01-15).
Each finding below cites its section.

**Verdict: the lesson does not read true at C0.** Twelve defects, three of them of the
class this very round is calibrating (a number/path that the tree contradicts, a
citation whose receipt does not carry the clause, and a "fix" with no arm behind it).
The routed-defect corrections themselves re-derive clean (ten of ten, section 09), and
the second Mistake reproduces exactly as described (section 07) — the failures are in
the document's own top matter, its Gate verdict, its forward commitments and one count
inside the table of corrections.

---

## F1 — HIGH · the freeze the lesson names is not the freeze that decides, and the amendment count is wrong

Lesson, line 3: "Base `0a2010ac`; counter freeze `631cd645` + amendments 1-4 (all in
`freeze.json`, all before any control score or deciding invocation)".

`receipts/commands.sh` §03:

```
amendments listed in freeze.json at C0: 7
manifest files listed: 7
631cd645 is an ancestor of the C0 freeze pointer e2979f2: yes
frozen paths differ between the named freeze and C0 (so FROZEN_UNCHANGED would read 0):
 .ufo/evidence/round-55/c1/measure.py | 41 +++++++++++++++++++---
 .ufo/evidence/round-55/c2/measure.py | 68 ++++++++++++++++++++++++------------
 .ufo/evidence/round-55/contract.json | 40 +++++++++++++++++++---
 .ufo/evidence/round-55/freeze.json   | 40 ++++++++++++++++++---
 4 files changed, 152 insertions(+), 37 deletions(-)
self-consistency of each freeze manifest (the gate re-hashes freeze.json at FREEZE):
  freeze rev=631cd6455e58 amendments=0 files=6 integrity=OK []
  freeze rev=e2979f277138 amendments=7 files=7 integrity=OK []
  freeze rev=9cf0146b94dd amendments=7 files=7 integrity=OK []
control receipts committed at C0 (0 = no control scored yet, so "all pre-control" holds): 0
```

Verdict: **wrong on both digits.** `631cd645` is the *pre-amendment* freeze: its own
`freeze.json` records **0** amendments and 6 manifest files. The freeze at C0 —
`e2979f277138da503af27b263b783f626f109be4` — records **7** amendments and 7 files
(`c1/staged-at-freeze.txt` joined); the freeze commit's own message reads "freeze
amendments 1-7", and `contract.json` at C0 lists the same seven. The JSON at
`631cd645` is internally consistent, so the gate's freeze-integrity check passes there;
but `deciding-run.sh:66` then compares that commit to `REV` over the seven frozen paths
and prints `FROZEN_UNCHANGED=0` → `rc=1` → the run is non-zero. A reader who anchors on
the lesson's pointer reproduces exactly the defect class R54.2 corrected (a freeze
pointer that is not the deciding freeze) *inside the document that fixes R54.2*.
The parenthetical "all before any control score or deciding invocation" is true
(0 committed control receipts, no `after/` at C0); only the hash and the count are wrong.

## F2 — HIGH · `QUALITY 106` does not exist at C0, and 105 carries no erratum

Lesson line 31: "QUALITY 106 states the rule and its falsifier is that same receipt";
line 55 (R54.1 evidence): "…`controls-b.stdout`; QUALITY 106"; lines 66-68: "Also
corrected in place: `corpus/QUALITY.md` 105's falsifier … carries an erratum rather
than a deletion; criterion 106 is appended."

§04:

```
last criterion heading in corpus/QUALITY.md at C0: ### Criterion 105 — a counter arm is proven on a positive control, not only on the do-nothing tree
Criterion 106 in corpus/QUALITY.md at C0: 0
files in the tree at C0 that carry a "### Criterion 106" heading (drafts, not the record):
  .ufo/waves/round-54/w1/T54W1ScribeQuality.md
  .ufo/waves/round-55/w1/T55W1ScribeQuality-receipts/criterion-106.md
  .ufo/waves/round-55/w1/T55W1ScribeQuality.md
any "erratum" heading attached to criterion 105: 0
the same false claim in LOG.md at C0:
2547:all ten routed values; QUALITY 106 (a control is scored at the revision it
```

Verdict: **criterion 106 is not appended.** `corpus/QUALITY.md` is 1590 lines and ends
at Criterion 105; C0's own contract calls line 1590 "QUALITY 1590's positive-control
claim". Three files carry a `### Criterion 106` heading — round 54's wave-1 draft (a
*different* rule: "a could-not-evaluate outcome prints no verdict token") and round 55's
two drafts — so the record now holds two competing 106s and the quality bar holds
neither. 105's falsifier *was* rewritten in place and now prints the corrected
`rekeyed=3/7` with `CTL_MISMATCH` and `[ER-R54-1]`, but nothing labels it an erratum,
so "carries an erratum" is unbacked. The same false claim ships in `LOG.md:2547`, and a
wave-1 seat had already reported it before C0 landed
(`.ufo/waves/round-55/w1/T55W1ScribeLog.md:225`: "**\"QUALITY 106 … with an erratum on
105\"** — 106 has not landed"). C1 cannot see this: no class reads QUALITY 106
(`c1/measure.py` R54.1 reads only `CTL_MISMATCH`/`2/3` in the corrections block).

## F3 — HIGH · the S280 "mined" verdict names a citation the cited document does not contain

Lesson line 11: "**admit, mined** — `corpus/knowledge/scratch-root-contract.md` cites it
for the \"one program-prefixed line\" shape".

§02:

```
grep -c S280 in corpus/knowledge/scratch-root-contract.md: 0
S-ids the note actually cites: S277 S278 S279
http/URL references in the note: 0
```

Verdict: **false.** The note cites S277, S278 and S279 and contains no URL; neither
"S280", "GNU", "coding standard" nor "program-prefixed" appears in it. The SOURCES row
S280 nevertheless declares `used-by` = `corpus/knowledge/scratch-root-contract.md,
corpus/lessons/round-55.md` — the note, plus the lesson that admits the row (a
self-reference to its own Gate cell, since no other lane document mentions S280 except
wave seat files). The census cannot catch that: E11 only checks that each used-by path
exists on disk (`scripts/sources-census.sh:567` prints `missing used-by` for an absent
file), and W03 only fires when the cell is `—`. So the
round ships a `mined` row whose declared user is a note that never mentions it, plus the
lesson's own Gate row — an admission ground the tree does not carry. (`tier A` and `status=mined` in the row are
otherwise consistent, and the sentence the note should be citing is in the snapshot the
lesson itself names — §01 lines 5-9.)

## F4 — MEDIUM · R54.2 says "the two stale ids"; the routed defect and the corrections section both name three

Lesson line 56: "R54.2 | FIXED — one freeze pointer (`077d431e`) for round 54; **the two
stale ids** moved into the corrections section".

§05:

```
**R54.2 — three different freeze pointers.** SCORECARD.md:2564-2567 calls `7883e0e5` …;
`SCORECARD.md` "measured close" says "freeze `fe70474d` (amendments 1-5)" …;
report `:157` says the freeze pointer is `097985c1` …
the corrections section quotes all three:
23:Old: `7883e0e5` called "the freeze pointer the deciding run uses"; `fe70474d`
24:in the measured-close line; `097985c1` in the fleet report.
the C1 counter stale scan watches only two (c1/measure.py, R54.2 class):
    stale = scan(lane, rev, ("SCORECARD.md",), r"7883e0e5|fe70474d")
```

Verdict: **"two" is wrong — there were three pointers**, and the section the row cites
lists three. The counter scans two, so a third stale instance could stand anywhere in the
record set and still score `total=0`; at C0 no third instance survives in the four record
files (only inside the corrections block), so the round does not lose the fact — it
miscounts it, which is the number-drift class it is calibrating.

## F5 — MEDIUM · the Mistake-1 fix describes an invocation convention as if it were an arm, and its "captured-by" claim is refuted by round 54's own freeze

Lesson lines 29-33: "fix: round 55's `controls.sh` phase B clones the revision it
certifies and its `deciding-run.sh` gate refuses any control receipt not descending
from the freeze; QUALITY 106 states the rule and its falsifier is that same receipt.
… The counter for this class is C1's `R54.1` row".

Code at C0: `controls.sh:119-125` is

```
d=$(clone_at "$LANE" "$REV" pos) || exit 2
```

— it clones whatever `REV` the caller passed, with no comparison, no base check and no
freeze-ancestry check; round 54's failure was precisely the caller passing the freeze as
`REV`. The second clause is real but narrower than the class: `deciding-run.sh:46-55`
checks existence, blob-ness, size, `git log -1 -- "$f"` and `merge-base --is-ancestor
"$FREEZE" "$c"` — commit order only. The lesson itself concedes the missing fact in its
`cannot_see` list ("never compares the `rev=` a `CTL` line names with the revision under
test"). Composed: `controls.sh b LANE FREEZE FREEZE OUT` — round 54's exact mistake —
still yields receipts the round-55 gate accepts. §15 makes that concrete: phase B is
`d=$(clone_at "$LANE" "$REV" pos)` (no comparison of `REV` to anything), and the gate's
control verdict check is `grep -q '^CONTROLS_B: [0-9]*/[0-9]* as pre-registered'` — a
regex that accepts `CONTROLS_B: 2/3 as pre-registered`, which is exactly what round 54's
failing receipt printed. So the class is caught by nothing at C0: not by the harness
(comment only), not by commit order (round 54's receipts descend from the freeze), not
by the verdict line (2/3 passes the regex). The surviving guard is the documentation
clause, and that clause points at F2 (a criterion that is not in `corpus/QUALITY.md`).

Mistake 2's `captured-by` is likewise refuted (§06):

```
round-54 freeze.json amendment 1:
  … Mechanical discovery bug, found by the binder dry run before any deciding
  invocation and before any control score; predicate, target and arms unchanged.
```

Verdict: "no prior round had a dry run *before* the controls" is **false** — round 54's
own freeze manifest records a dry run before any control score (amendment 1; round 54's amendment 2 likewise names "wave-1 attack seats … before the deciding run"). The
mechanism the lesson attributes to the dry run is real (see the "gets
right" table, mistake-2 rows), the novelty claim is not.

## F6 — MEDIUM · the S280 quote is 14 words, not 17

§01:

```
wc -w fragment1: 12
wc -w fragment2: 2
wc -w both quoted spans: 14
wc -w with the 3-word section-title quote added: 17
```

Verdict: the row's quote cell holds two fragments (12 + 2 = **14** words by `wc -w`).
17 is reproducible only by adding the section-title quote ("Formatting Error Messages",
3 words) or the verdict cell's quoted phrase — which the row does not say it counts. This
is the identical class and identical numbers as the round-33 routed defect the lane
already carries ("the S100 Gate quote is 14 words, not 17", `corpus/lessons/round-33.md:149`)
and round 34's "labeled 15, wc -w counts 16". The ≤25-word budget is met either way, so
the round is not harmed — the number is simply not the quote's.

## F7 — MEDIUM · the sysexits rejection cites rule 2 of CORPUS.md and census W04; neither is the duplicate rule

Lesson line 12: "…so a new row would be a within-scope duplicate URL (CORPUS.md rule 2,
census W04)".

§10:

```
CORPUS.md rule 2 (the lesson cites it for a duplicate URL):
2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, …
census code table: inside scope = E04, across scopes = W04:
25:#             E03 duplicate id                   E04 duplicate URL+scope (no supersedes)
33:#             W04 same URL across scopes (warnings do not affect clean lanes)
-- inserting a duplicate of S090's URL in the same scope, inside the registry:
tameshi-shokunin	E04	S281 duplicate url man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 within scope BSD exit-status conventions for command-line programs; legacy and deprecated by its own text
```

Verdict: **both references miss.** `CORPUS.md` rule 2 is *Append-only* (it governs
in-place mutation of `status`/`recheck`/`used-by`); the census's within-scope duplicate
is **E04**, while **W04 is the cross-scope warning** and would not fire for this
candidate. The rejection's substance stands — a same-scope duplicate row is E04 — but the
citation a reader must re-open is wrong twice, which is R54.10's class (a quote under the
wrong receipt) recurring in the Gate. Note also that a duplicate row marked `rejected` is
exempt from E04 by the awk condition `status!="rejected"`.

## F8 — LOW · "wrapped at 78 columns" is 76

§07:

```
SKILL.md at C0, correct edit present (whitespace-normalised): True
SKILL.md at C0, raw match (the pre-amendment arm's comparison): False -> skill arm = 0 /1
the marker is split here: line 39 width 76 -> line 40 width 79
```

Verdict: the mechanism is exactly as the lesson says (raw `MARKER in text` cannot see a
split marker; normalising recovers it), and "78" is only the wrap target — the actual
split is after `scratch` at column 76. Substance holds; the number is approximate.

## F9 — LOW · `S281-sysexits.txt` names a rejected snapshot with an id no row carries

The Gate table's own row is "(no row)", and `corpus/SOURCES.md` at C0 has no S281. The
lane's precedent for a rejected candidate's snapshot is an id-less name (round 53 keeps
`assimilation/ojda-home.html`, `ojda-portfolio.html` and the `collisions/` dir). A file
named `S281-…` will read as the snapshot of the next admitted row, which also takes S281.
The digest in the lesson (`0bf02057…`) is correct (§01), so this is a naming
defect only.

## F10 — LOW · the S280 extraction stops one sentence before the clause the Gate cell cites

Lesson line 11: "the page's next paragraph adds the lower-case/no-period rule". §14
(curl of the page) shows it there — "…because that isn't the beginning of a sentence. (The sentence
conceptually starts at the beginning of the line.) **Also, it should not end with a
period.**" — but the committed snapshot
(`assimilation/S280-gnu-errors.txt`, lines 10-11) ends at "because that isn't the
beginning of a sentence." So the receipt carries the capital-letter rule and not the
no-period half. Per the lane's own QUALITY 104/91 shape (a citation must resolve to a
receipt establishing its clause), either extend the extraction or drop the clause; the
locator itself ("the next paragraph") is correct.

## F11 — LOW · the lazy-arm compensation is not scheduled by any wave-2 item

Lesson line 88: "The lazy arm also cannot distinguish \"allocates nothing\" from
\"allocates only after its preconditions fail\" — the wave's probes push two lazy modes
with failing inputs."

§12: `spec-w2.json` has 34 items; `items containing 'failing input': 0`; four items
mention laziness, and the closest (`T55W2RevDocsArms`) asks "are the five lazy modes
really lazy?" — a laziness check with valid invocations, not a failing-input probe. The
spec is also not committed at C0 (`git ls-tree` of `.ufo/waves/round-55/` lists only the
wave-1 files). The blind spot is stated honestly; the compensation it promises does not
exist in the dispatch that exists.

## F12 — LOW · "content commit C0 (this commit's parent chain)"

The lesson is committed *in* C0 (only commit touching the file:
`git log --format=%h -- corpus/lessons/round-55.md` → `9cf0146`), so C0 is this commit,
not an ancestor of it. Cosmetic, but it is the pointer a reader uses to find C0.

---

## What the lesson gets right (checked, not assumed)

Everything below was re-derived; each line cites its receipt section.

| claim | where | result |
|---|---|---|
| base `0a2010ac` | line 3 | ✓ (`0a2010acd1e9…`) |
| S281 quote "15 words", located §DESCRIPTION, BUGS "ambiguous" | line 12 | ✓ `wc -w` = 15; both sentences present in the snapshot (§01) |
| snapshot digests `edcaf94b…`, `0bf02057…` | lines 14-16 | ✓ `sha256sum` of both committed blobs reproduces the quoted prefixes (§01) |
| census "exit 0, 140 rows" by the lesson's own grep | line 16 | ✓ 140 rows, `validate` exit 0 (§10) |
| §4.4 locator for the GNU quote | line 11 | ✓ snapshot title carries "4.4 Formatting Error Messages" |
| mistake 1: phase-B control cloned `077d431e`; it predates `7fa9a5e` | lines 21-23 | ✓ receipt line `rev=077d431e6996…`; ancestor relation holds (§03/§09) |
| mistake 1: receipt prints `CTL_MISMATCH CTL_POS_c1 expected=true actual=false` / `CONTROLS_B: 2/3` | lines 22-24 | ✓ verbatim (§09) |
| mistake 1: four files asserted the pass, including a criterion written in round 54 | line 25 | ✓ (`SCORECARD:2583`, `QUALITY:1590`, `lessons/round-54:101`, fleet report `:162`; the criterion was 105) |
| mistake 2: arm 7 (skill) matched the raw marker and read `0/1` on a correct edit | lines 36-38 | ✓ reproduced: raw `False`, normalised `True` (§07) |
| mistake 2: note arm used the counter's `--selftest` spelling for a mode invoked as `selftest` | lines 38-40 | ✓ pre-amendment bytes label all seven `--selftest`; with those labels the note reads 7/8, with the labels as invoked 8/8 (§07) |
| R54.1 receipt + `2/3` in the corrections section | line 55 | ✓ (the QUALITY 106 half fails — F2) |
| R54.3 `total=13` | line 57 | ✓ `before/c2.stdout` last line `total=13` (§09) |
| R54.4 `8528ee85` | line 58 | ✓ `round-54/freeze.json` `files["c2/measure.py"]` (§09) |
| R54.5 `w1=28 w2=25 sections=12` | line 59 | ✓ re-derived: 23 w1 readers / 15 with findings / 28; 23 w2 / 12 with findings / 25 (§08) — and ER-R54-5's "12 of the 23 wave-2 reports" is exact |
| R54.6 swept files added at `ff2a821` | line 60 | ✓ `--diff-filter=A` on `T54W2Sent03.md` (§09) |
| R54.7 renamed (R100) at `7fa9a5e` | line 61 | ✓ `R100 old → receipts/forged-reader.json` (§09) |
| R54.8 seat file marked superseded; operator turn in `history.db` row 690 | line 62 | ✓ `**SUPERSEDED (round 55, ER-R54-8).**` at `:332`; row 690 = `use m_glm53 instead of m_grok`, epoch 1793200335 = 2026-10-28T15:12:15Z (§09) |
| R54.9 `reviewers=5 attack=21/76 seats=76` and `staged=81` | line 63 | ✓ registry (`5 21 76`) and the committed receipt `output=81` (§09) |
| R54.10 `rekeyed=0/7` in `controls-a.stdout`; `0/30` in `r53-counter-at-88afa941.stdout` | line 64 | ✓ both (§09) |
| `cannot_see`: ten wave reviewers re-derived the ten values | line 74 | ✓ `T55W1Rev01`–`Rev10`, each item mapped to two of R54.1–R54.10 |
| `cannot_see`: a paraphrased false claim scores `total=0` | lines 76-79 | ✓ executed: fixture with "Round 54's phase-B positive control passed as pre-registered" outside the corrections block → `stale=0 total=0 C1_R55_PASS=true` (§11) |
| `cannot_see`: an unrelated wrong assertion inside the corrections section is exempt | lines 78-79 | ✓ same fixture, `CTL_POS_c1 true` planted inside the block → still `total=0 PASS=true` (§11) |
| `cannot_see`: LOG.md joined the record set and a whitespace-collapsed span scan exists (amendment 5) | lines 80-81 | ✓ `RECORD` includes `LOG.md`; `scan_span()` collapses whitespace (`c1/measure.py:34-39,99-118`) |
| `cannot_see`: the deciding gate never compares a `CTL` line's `rev=` | lines 89-91 | ✓ `deciding-run.sh:46-55` checks existence/blob/size/commit-order + verdict regex only |
| C2 `cannot_see`: a wave item inventories undocumented modes | lines 84-86 | ✓ `T55W2RevNoteNine` ("look for a tenth documented mode … sweep hard") |

## Residual risk and verification gaps

- **R1 — the corrections are closed only where the counter reads.** The routed defects
  R54.2/R54.4 also name the round-54 *report*, which lives at the fleet root
  (`.ufo/reports/round-54/tameshi.md`, outside the lane). At C0 it still prints
  `49280fe5` (§13: 1 hit) and `097985c1` (§13: 1 hit). The lane's record files are clean;
  a reader of the fleet report still meets the stale digest and the third freeze pointer.
  Since the report is outside the lane and outside C1's `RECORD`, the round should either
  declare the residue or the fleet should correct it.
- **R2 — S280's used-by is enforced by nothing.** Census E11 checks path existence only
  (`sources-census.sh:538-567`). Any future round can satisfy a `mined` row with a
  used-by file that never mentions the id; the round's own E11 pass is therefore not
  evidence that S280 is used.
- **R3 — no arm binds a phase-B clone to the revision it certifies** (F5). I did not run
  `controls.sh` phase B end to end: it executes both counters plus 13 traced modes, and a
  full run in this seat's scratch would have produced a second, non-deciding receipt for
  the round rather than evidence about the harness. The static proof is the script text
  (`clone_at "$LANE" "$REV"`) plus the gate's four checks; a positive demonstration —
  `controls.sh b LANE FREEZE FREEZE OUT` then `deciding-run.sh` — remains for the L1 if
  it wants the execution receipt.
- **R4 — no language server in this seat.** Markdown has no server here, so the
  caller/definition checks above are `git show`/`git grep`/code reads; absence claims are
  backed by the exact pattern and the exact path list (corrections block, record set,
  spec items), never by a cold empty result.
- **R5 — scope.** I did not attack the C2 gate's own arithmetic (the counter's docstring
  still says "8 allocating modes / note=8" while the verdict prints `note=%d/9`); it is a
  frozen-instrument documentation mismatch, adjacent to but not part of the lesson, and
  another wave-2 seat owns the docs surfaces (`T55W2RevDocsArms`).

## Fix list for the L1 (smallest set that makes the lesson read true)

1. Line 3 → `counter freeze e2979f2 … (7 amendments)`; keep the "all pre-control" clause.
2. Lines 31, 55, 66-68 → either land `### Criterion 106 — a pre-registered control is
   scored at the revision it certifies` (with a falsifier that can fail) and label 105's
   in-place rewrite as an erratum, or drop all three references. Land the same fix in
   `LOG.md:2547`.
3. Line 11 → name where S280 is actually used (or add the citation to the note), and
   correct the count to 14 words.
4. Line 12 → `census E04` (and drop the CORPUS.md rule-2 clause).
5. Line 56 → "the three stale ids".
6. Lines 29-33 → state the fix as "phase B is invoked at the content revision and the
   gate checks commit order"; and either add an arm to `controls.sh` that refuses a
   phase-B `REV` that is not the certified revision, or name the class as still caught by
   nothing.
7. Line 42 → drop or replace "no prior round had a dry run before the controls" (round
   54's amendment 1 is the counter-example).
8. Line 37 → 76 columns; line 4 → "C0 (this commit)".
9. Line 88 → schedule the two lazy failing-input probes in the wave spec, or say the
   blind spot is uncompensated.
