# T55W2RevSources2 — S280 re-opened, and the sysexits refusal

Seat `T55W2RevSources2` (reviewer, wave 2, L1 `TameshiR55`).
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; revision under attack
**C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`** (lane HEAD at read time
`133b2ce`, whose diff to C0 is only `.ufo/evidence/round-55/{c2/measure.py,
contract.json, freeze.json}` — so every corpus byte I cite is the C0 byte).
Access date **2026-10-28**. Nothing in the lane was written except this file
and `T55W2RevSources2-receipts/`; all fixtures are `mktemp -d` clones or
synthetic census roots under `/fast/scratch/hyaku/tameshi-r55/T55W2RevSources2`.

I re-opened both URLs myself and compared my own bytes to the committed
snapshots before checking a single cell.

```
gnu  https://www.gnu.org/prep/standards/html_node/Errors.html            http=200  7147 B  sha256 54c55cd4de53023b…  == committed snapshot
bsd  https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3        http=200 59251 B  sha256 1fc793a298a937d7…  == committed snapshot
```

Receipts `R1`/`R2` (`T55W2RevSources2-receipts/01-gnu-fetch.txt`,
`02-sysexits-fetch.txt`). GNU page revision stamp, read from my own copy:
`The GNU coding standards, last updated April 27, 2026` at raw offset **204**.

## Verdicts, one line each

| item | verdict |
|---|---|
| S280 quote, verbatim at its locator | **hold** — both forms and both rules are on §4.4 at the offsets below; nothing invented |
| S280 locator (anchor cell) | **overreach (low)** — names a *fetch* date where the contract asks for the *revision*, and locates the quote by prose, not by offset |
| S280 word count (`(17 words)`) | **wrong** — the C0 quote is **14** words (**15** with the ellipsis); 17 fits only the pre-rewrite longer quote |
| S280 `teaches` cell | **overreach** — its quoted spans hold, but the gloss (i) states `must not` where the page says `should not`, (ii) asserts an unmarked inference ("one program-prefixed line"), and (iii) carries a clause that is **not in the row's own named receipt** |
| the Gate's claim that the note cites S280 | **wrong at C0** — `corpus/knowledge/scratch-root-contract.md` cites S280 **0** times; the wave-1 draft cited it twice and the landed note dropped both |
| sysexits refusal, "duplicate of S090 (CORPUS.md rule 2, census W04)" | **wrong** — rule 2 is *append-only*, a same-lane duplicate is census **E04** (not W04), and E04 is cleared by rule 2's own `supersedes S0NN —` device |
| sysexits flip condition | **wrong** — both conjuncts are already true at C0, so the flip has already fired |
| sysexits quote + 15-word count | **hold** — verbatim in §DESCRIPTION; 15 words as stated |
| census | **hold** — exit 0, **140 rows**, **0 errors**, **16 warnings** (`W04=15`, `W01=1`), identical multiset to base (also exit 0, 139 rows) |

## Findings, by severity

### F1 (wrong) The sysexits refusal invokes a bar that does not exist, and misnames the code that does

`corpus/lessons/round-55.md` @ C0, Gate row 2:

> the document is already held as **S090**, so a new row would be a within-scope
> duplicate URL (CORPUS.md rule 2, census W04)

Three separate errors in one clause:

1. **CORPUS.md rule 2 is not a duplicate rule.** Read verbatim from
   `/home/vgpnk/Projects/shokunin/CORPUS.md` (`### Rules`, lines 110-129):
   rule 2 is *"**Append-only.** Only `status`, `recheck` and `used-by` change in
   place… A correction is a new row whose `teaches` opens `supersedes S0NN —`."*
   There is no duplicate-URL rule in rules 1-6 at all; the duplicate checks are
   census codes.
2. **`W04` is the wrong code and is a warning.** The census's own table
   (`scripts/sources-census.sh`, header lines 25-33): `E04 duplicate URL+scope
   (no supersedes)`; `W04 same URL across scopes (warnings do not affect clean
   lanes)`. "Within-scope duplicate" and "W04" cannot both be true. `W04` is
   also *permitted* in the live lane right now: the C0 registry carries 15 of
   them.
3. **`E04` is exactly the code rule 2's device clears.** Its predicate is
   `teaches !~ /supersedes S[0-9]{3}/`.

Fixture, synthetic roots, runnable (`R3`):

```
scripts/sources-census.sh validate --root $ROOT $ROOT/a-shokunin   # same URL, SAME scope, no supersedes
a-shokunin  E04  S281 duplicate url man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 within scope BSD exit-status conventions for command-line programs
exit=1

scripts/sources-census.sh validate --root $ROOT $ROOT/b-shokunin   # same URL, SAME scope, teaches opens "supersedes S090 — …"
b-shokunin  ok   …/b-shokunin/corpus/SOURCES.md
exit=0

scripts/sources-census.sh validate --root $ROOT $ROOT/c-shokunin   # same URL, DIFFERENT scope (the natural shape)
c-shokunin  W04  S281 duplicate url man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 across scopes
c-shokunin  ok   …/c-shokunin/corpus/SOURCES.md
exit=0
```

So: with the scope cell the candidate would actually carry (S090 keeps
`EX_USAGE`; the candidate teaches the deprecation), the census is **clean with
one warning** — there is no bar to invoke. With S090's exact scope string it is
`E04`, and `supersedes S090 —` clears it, which is the corpus's own documented
device and, at C0, the registry's **commonest** pattern for an already-held URL:
**14 rows** carry `supersedes S0NN —` in `teaches` — `S047 S048 S075 S076 S077
S078 S081 S092 S100 S160 S265 S266 S267 S268` (`R7`). One URL is held **four
times**: `pitest.org/quickstart/incremental_analysis` at S041, S047, S048 and
S266, and the lane still validates `exit 0` — those rows produce `W04`
warnings, nothing more (`R4`). The Gate refuses a row for exactly the
construction this registry uses fourteen times.

**The outcome — no new row — is still defensible**, but on grounds the Gate does
not state: CORPUS rule 4 (*"Expansion is knowledge, not rows… a short registry
of opened, honestly tiered rows beats a long one"*), and S090's own cadence
(opened 2026-10-22, `recheck 365d`, not due six days later). What is wrong is
the reason written down: it cites a rule that says the opposite (rule 2 supplies
the admission mechanism) and a census code that is a warning for a different
case.

### F2 (wrong) The flip condition has already fired, so it cannot be a rejection's flip

The Gate's flip: *"a lane rule that actually adopts an EX_\* code and records the
deprecation as an accepted trade"*. Both conjuncts are recorded at C0:

- **adopts an EX_\* code**: the lane's uniform usage exit is 64 —
  `tools/bash-witness-study.py:75` "Usage errors exit 64 (the probe contract)";
  `tools/context-capture.py:89`, `tools/evidence-disposition.py:178`,
  `tools/mutate-and-run.sh:250`; and the code is *asserted*, not incidental:
  `tools/mutate-and-run.sh:2123  bash "$SELF" --regression --target "$fx/target.sh" …; st '--regression refuses --target (exit 64)' $?`,
  with mutation defects `K_EXIT`/`S_USAGE` ("usage error exit 64 becomes 65").
  S090 exists for precisely this: its `teaches` reads *"an outside anchor for a
  usage exit of 64, fixed outside any gate's code"*, and
  `corpus/knowledge/oracle-anchored-survivors.md:49` anchors the `S_USAGE` row
  to `S090 (EX_USAGE (64) … "a bad flag")`.
- **records the deprecation as an accepted trade**: S090's `scope` cell already
  says *"legacy and deprecated by its own text"*, and
  `corpus/lessons/round-27.md` records the trade in words: *"The page calls the
  interface legacy and deprecated; the entry uses it only as a fixed
  convention, not as a recommendation."*

A flip names what would change the verdict. This one describes the state the
corpus is already in, so it cannot distinguish this candidate's fate — and read
straight, it says the row *should* be admitted. Worse, the flip is not tied to
what the candidate would add: the only thing the deprecation sentence buys is an
**anchor** for a claim already made in prose, which is the S265-S268
`supersedes … anchor and quote only` shape, not a new document.

### F3 (wrong) S280's word count is stale by three

Gate cell: `(17 words; the page's next paragraph adds the lower-case/no-period rule)`.

Recount of the two quoted spans at C0 (`R5` §5.1):

```
quoted spans: ['Error messages from other noninteractive programs should look like this: program:sourcefile:lineno: message', 'program: message']
wc -w of the two quoted spans         : 14
wc -w with the "..." counted as a word: 15
wc -w if colons also split words      : 16
```

No method yields 17. The number is a leftover: the pre-rewrite quote carried
`... or like this: program: message`, and **that** string counts 18 with the
ellipsis and **17** without (`R5` §5.2). The rewrite dropped `or like this:`
and kept the old count. Wave 1 had already measured 18/17 against the longer
form (`T55W1RevSources-receipts/word-counts.stdout`); C0 kept the 17 and lost the
words. The ≤25 ceiling is not breached either way, so this is a count that
carries no command and does not reproduce — CORPUS's *"A count carries its
command"* is the rule it breaks.

### F4 (overreach) The Gate asserts a citation the note does not contain

Gate verdict cell: *"`corpus/knowledge/scratch-root-contract.md` cites it for the
'one program-prefixed line' shape"*.

```
$ git show 9cf0146:corpus/knowledge/scratch-root-contract.md | grep -c S280          -> 0
$ git show 9cf0146:corpus/knowledge/scratch-root-contract.md | grep -n "GNU\|4\.4\|Standards"  -> no output (0 matches)
$ ... S277=1  S278=2  S279=1  S280=0      # the three older neighbours are cited, S280 is not
```

The note's `## One line, every mode (round 55)` section was **added this round**
(base `0a2010ac`: no such section, `S280` count 0) and states the one-line shape
with no source. The wave-1 draft that became this section **did** cite it twice
(`T55W1ExecNote-receipts/note.patch:48` "…when it follows the program name
(S280)", `:100` "and S280 is the authority for the one-line shape"); both lines
are absent from the committed note. So the landed edit dropped the citations the
draft carried, and the Gate then asserted them.

Consequence for the row: `used-by` cell 11 = `corpus/knowledge/scratch-root-contract.md,
corpus/lessons/round-55.md`. The contract defines `mined` as *"cited by ≥1 path
in `used-by`"*, and `used-by` as *"paths of the knowledge entries or lessons
citing the row"*. The **first** path does not cite it; the second is the Gate
that admits the row. So `mined` survives only through self-citation by the
admitting lesson — technically inside the letter, substantively hollow, and the
prose claim about the note is simply false.

The census cannot see this (fixture `D`, `R3`): `E11` checks only that the
`used-by` path **exists**.

```
d-shokunin  W03  S090 mined but unused        # note.md exists, cites S090 zero times
d-shokunin  ok   …/d-shokunin/corpus/SOURCES.md
exit=0
```

### F5 (overreach) Half the `teaches` cell is unsupported by the row's own receipt

`teaches` (cell 7, C0) ends: *"…and the message must not begin with a capital
letter or end with a period after that prefix"*. Both rules are genuinely on the
page — `The string message should not begin with a capital letter…` (raw
`The string ` at byte 6250) and `Also, it should not end with a period.` (raw
byte 6501) — but the anchor names
`.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt` as its receipt, and
that file does not contain the second rule:

```
$ git show 9cf0146:.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt | grep -c -e period -e "end with"   -> 0
$ ... | grep -c 'should not begin with a capital letter'                                                      -> 1
```

11 lines, 663 B, sha256 `edcaf94bb897158f…` (first16 `edcaf94b` matches the
anchor). The extraction is honest about what it is ("reader extraction"), and
its two quoted sentences are verbatim — the only deviation I found is the
apostrophe (`isn't` in the extraction vs `isn&rsquo;t` in the page). The defect
is that the row's named artifact verifies half of its `teaches`; wave 1's C3
asked for exactly this and it is still open at C0. This is the residue of the
wave-1 repair: the earlier clause ("the message text does not repeat the
program's own verdict vocabulary") was **correctly** removed as unsourced, and
its replacement is sourced *on the page* but not *in the receipt*.

### F6 (overreach) `must not` where the standard says `should not`; `one` is the lane's inference

```
"must"   occurrences in §4.4 flat text : 0
"should" occurrences                   : 9
"one line"                             : False
```

The page says *"should not begin with a capital letter"* and *"it should not end
with a period"*. The row upgrades both to `must not` and, in the same gloss,
states *"one program-prefixed line is the standard's shape"* — the word `one` is
nowhere in §4.4 (the page shows one line per message, it never says so). Wave
1 filed this as C2/F3; C0 still carries it unmarked. The `[INFERENCE]` marker
the corpus uses elsewhere would cost four characters.

### F7 (overreach, low) The anchor gives a fetch date where the contract asks for a revision

`anchor` (cell 6): `§4.4 Formatting Error Messages @ fetched 2026-10-28 (reader
extraction …; the quote sits at the section's noninteractive-program rule)`.
CORPUS's `anchor` definition: *"exact section / heading / page / line plus
revision (version, commit, or publication date). Never a bare homepage."* The
heading is exact and the section is right; the "revision" slot is filled with
the **fetch** date, and the page's own revision — `last updated April 27, 2026`,
raw offset 204 — is in my copy and absent from the row. "The section's
noninteractive-program rule" is prose where the sibling rows use `:163-165`
style offsets. Everything is locatable (I re-found every span from the URL
alone), so this is labelling, not fabrication.

### F8 (overreach, low) Tier A is scoped to an un-GNU-qualified scope

`scope` (cell 5) = *"the line shape of a noninteractive program's error
message"*; `tier` = A. CORPUS: *"`tier` — scoped to `scope`, never global… **A**:
primary or authoritative for that scope"*. The GNU Coding Standards are
authoritative for **GNU** programs' behaviour; for non-GNU lanes they are a
respected house convention. Wave 1's C1 asked for a GNU-qualified scope and C0
did not take it. Honest counter-argument, recorded because it limits the
severity: §4.4 sits under the page breadcrumb *"Up: Program Behavior for All
Programs"*, so inside the document the rule is general — but "general inside the
GNU standards" is not "authoritative for every program", and `A` is the
authority claim. Nothing in the row's *use* depends on it (the note cites nothing).

## Holds (checked, no defect)

- **Quote verbatim.** All four spans present at §4.4: sentence at raw 5020, the
  conditional at 5298, `program: message` rendered-only (`<var>`-wrapped, so raw
  `find` returns −1 — as wave 1 recorded), `The string ` at 6250, no-period at
  6501. The inline join with `... or` elides only "when there is an appropriate
  source file", which the second form does not need.
- **Row shape.** 11 cells, 12 pipes, no pipe inside a cell, inside `## Registry`
  (line 155, before `## Paths`), `kind=spec` / `tier=A` / `status=mined` /
  `opened=2026-10-28` / `recheck=730d` all inside the enums; both `used-by`
  paths exist on disk.
- **`teaches` quoted spans** = 12 + 2 = 14 words, ceiling honoured.
- **sysexits quote.** `This interface has been deprecated and is retained only
  for compatibility. Its use is discouraged.` — 15 words as the Gate says,
  present in §DESCRIPTION (`R2`), with §BUGS' *"The choice of an appropriate
  exit value is often ambiguous."* (10 words) also present, so the second
  refusal reason is honest. Extraction `S281-sysexits.txt` sha256
  `0bf02057a605ef52…` matches the lesson's `0bf02057…`.
- **Census.** Exit 0; **140 rows**; **0 errors**; **16 warnings** —
  `W04=15` (the pre-existing across-scope duplicate set) and `W01=1`
  (S101, tier C mined) — byte-identical multiset to a base clone (139 rows,
  same 16). S280 adds no code, and the sysexits URL appears once in the
  registry. `malformed=0`. The lesson's *"exit 0, 140 rows"* reproduces; it is
  silent on the 16 warnings, which is accurate but under-reported.

## Receipts (all runnable; fixtures under scratch, never the lane)

| file | what it shows |
|---|---|
| `T55W2RevSources2-receipts/01-gnu-fetch.txt` | my fetch, byte-identity with the committed snapshot, rendered §4.4 text |
| `T55W2RevSources2-receipts/02-sysexits-fetch.txt` | my fetch, the three sentences and their word counts |
| `T55W2RevSources2-receipts/03-census-duplicate-fixtures.txt` | the `E04` / `supersedes` / `W04` / `E11`-blind fixtures |
| `T55W2RevSources2-receipts/04-census-live.txt` | live census at C0's bytes, row count, warning histogram |
| `T55W2RevSources2-receipts/05-wordcount-and-citation.txt` | the 14/15/16 recount, the teaches cell, the 0-citation fact, the dropped patch lines |
| `T55W2RevSources2-receipts/06-base-census-delta.txt` | base clone at `0a2010ac`: 139 rows, same 16 warnings, exit 0 |
| `T55W2RevSources2-receipts/07-supersedes-precedent.txt` | the 14 `supersedes S0NN —` rows at C0, and one URL held four times |

Artifacts opened: `CORPUS.md` (fleet root, rules + census code table);
`scripts/sources-census.sh` (duplicate logic and overridable code table);
`corpus/SOURCES.md` @C0 lines 99, 155, 515-517; `corpus/lessons/round-55.md`
@C0 (Gate, Mistakes, dispositions); `corpus/knowledge/scratch-root-contract.md`
@C0 (all 102 lines) and @base `0a2010ac`;
`.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt` and
`S281-sysexits.txt`; `.ufo/waves/round-55/w1/T55W1RevSources.md` and its
receipts (`note-citation`, `word-counts`, `locators`, `unsourced-clause`,
`page-text/gnu-errors-2026-10-28.html`); `.ufo/waves/round-55/w1/
T55W1ExecNote-receipts/note.patch`; `.ufo/waves/round-55/w1/T55W1ExecCensus.md`
/ `.json`; `corpus/QUALITY.md` @C0 (criterion 39 context);
`corpus/lessons/round-27.md`; `corpus/knowledge/oracle-anchored-survivors.md`;
the two live URLs.

## Residual risk and verification gaps

- **What I did not judge:** whether the round *should* hold the deprecation
  sentence at all. My finding is about the reason written down, not a demand
  that a row be added; on rule 4's arithmetic the corpus is better without one.
- **`W04` vs `E04` depends on the scope cell the author would have typed.** My
  fixture `C` assumes the natural shape (different scope). If an author had
  copy-pasted S090's scope verbatim the code would be `E04` — which
  `supersedes S090 —` still clears (fixture `B`). Both branches end without a
  bar, so the finding does not rest on which scope was intended.
- **`mined` may be intended to include the admitting lesson.** `used-by`'s
  definition admits lessons, so the status is inside the letter; I flag the
  prose claim (F4) as false and the substance (self-mining) as hollow, not the
  enum as violated. No census code covers "the named path does not cite the
  row" (proved by fixture `D`).
- **The note has no `source:` / `verified-at:` / `recheck:` frontmatter** (it
  starts at an H1, and did so at base too), so CORPUS's *"Each `knowledge/`
  entry opens with `source:`…"* is unmet lane-wide. Pre-existing, outside this
  round's diff, reported as context for why the dropped inline citation left no
  other channel.
- **Not re-derived here:** the T55W1RevSources locator table (I re-found every
  span from my own copy and agree on all five offsets, including the
  rendered-only ones), the C1/C2 counters, and anything outside the two source
  rows and the census.

No tools were installed for this seat (system `curl`, `git`, `awk`, `grep`,
`python3` sufficed); no pacman/uv/npm transaction ran.

Report: .ufo/waves/round-55/w2/T55W2RevSources2.md
