# T55W1CritSourcedClaim — the round's sourced claim, attacked

Seat `T55W1CritSourcedClaim` (critic), tameshi round 55, wave 1.
Axis **coverage**; milestone **falsify the sourced-claim requirement**.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base
`0a2010acd1e92e4e332774050825e21bcfc7e079`; content commit audited
`9cf0146` (C0; `corpus/` is unchanged in the worktree at audit time);
access date **2026-10-28**.
All paths below are relative to the lane unless absolute.
Everything is in this file, `T55W1CritSourcedClaim.json`, and
`T55W1CritSourcedClaim-receipts/`. No counters were run; no lane production
file was edited. Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W1CritSourcedClaim`
(removed at seat end; the synthetic census receipts preserve the outputs).

---

## 0. Verdict, up front

**LOUD — the round has NO sourced claim under the frontier contract §2b.4.**
The only row opened this round is S280 (GNU Coding Standards §4.4). The knowledge
entry C2 lands, `corpus/knowledge/scratch-root-contract.md`, does **not** cite it,
and no file under `.ufo/evidence/round-55/` cites it either:

```
grep -c  'S280'  corpus/knowledge/scratch-root-contract.md   -> 0
grep -rl 'S280'  corpus/knowledge/ | wc -l                   -> 0
grep -rl 'S280'  .ufo/evidence/round-55/ | wc -l             -> 0
grep -c  'S280'  corpus/lessons/round-55.md                  -> 2   (the Gate, required by §2b.1)
grep -c  'S280'  corpus/SOURCES.md                           -> 3   (the row, the Search log, and the id-allocation line)
```

(`T55W1CritSourcedClaim-receipts/claim-map.txt`.) The lesson's Gate says the note
“cites it”; the note cites only S277, S278 and S279. The registry's Search log
repeats the same falsehood (“mined by `corpus/knowledge/scratch-root-contract.md`”).
The wave's own note draft **did** cite S280 (`T55W1ScribeNote-receipts/draft-section.md:25,76`);
the landing dropped the citation, and seat `T55W1ScribeNote` F4 said so before the
round landed it anyway. So the round as landed fails §2b.4 — and no counter can see it: the C2 note
arm checks the grammar and the mode names only
(`.ufo/evidence/round-55/c2/measure.py:257-259`).

Second loud point: **even with the citation restored, the source grounds only half
of C2.** GNU §4.4 supports the *line format*; it says nothing about exit codes
(`exit` occurs 0 times in the rendered page, and the standards' contents have no
exit-status node). The exit-2 half has no source among the documents opened this
round. `sysexits(3)` is not a candidate for it: it deprecates the scheme it would
be cited for, calls the choice of exit value “often ambiguous”, assigns 64–78 and
never 2. Rejecting it leaves the round with **no source for the exit-code half**;
if GNU is rejected as well, the round has no sourced claim at all. It cannot be
rejected on the line half (see §1.1), so the honest statement is: *C2's grammar
rests on S280 for its shape and on nothing external for its exit code.*

---

## 1. The two candidate sources

### 1.1 GNU Coding Standards §4.4, “Formatting Error Messages” — **ADMIT, line format only**

- URL `https://www.gnu.org/prep/standards/html_node/Errors.html`; opened
  2026-10-28; snapshot
  `.ufo/waves/round-55/w1/T55W1ScribeSources-receipts/sources/gnu-errors.html`,
  7147 B, sha256 `54c55cd4de53023b694f1195feb3e5a0a6198ed7f290c368442888356fda270c`
  (I re-hashed the committed bytes and re-rendered the page).
- Revision: the page's own stamp is **“last updated April 27, 2026”** (HTML
  comment, raw byte 204). Its chapter is **“Program Behavior for All Programs”**
  of *The GNU coding standards*.
- Located quotes (all present in the committed snapshot):

| # | quote | words | locator |
|---|---|---|---|
| 1 | “Error messages from other noninteractive programs should look like this:” | 10 | §4.4, rendered text |
| 2 | `program:sourcefile:lineno: message` | 1 whitespace token (4 colon-split) | §4.4, first form |
| 3 | `program: message` | 2 | §4.4, second form (“when there is no relevant source file”) |
| 4 | “The string message should not begin with a capital letter when it follows a program name and/or file name” | 19 | §4.4, casing rule |
| 5 | “Also, it should not end with a period.” | 8 | §4.4, final punctuation |

- **(a) one consistent line format — yes.** The page gives the message form as a single template line,
  `program: message` when there is no source file, with the message starting
  lower-case after the program name and not ending in a period.
  The frozen C2 line has that shape (`repeat-control.py: could-not-evaluate: …`
  — lower-case message, no final period, one line).
- **(b) one exit code per class — no.** `exit` appears 0 times in the rendered
  page; the standards' contents have no exit-status node. The page is silent, not
  supportive. The word **“one”** in “one line” is also not in the source (0 hits
  for “one line”); the page gives *a form*, not a line count. That reading is an
  inference, and the row/Gate should mark it.
- **Decoration test:** if S280 were deleted, no C2 arm would change — the counter
  derives the grammar from the frozen contract, not from the source. The row is
  *justificatory* (it grounds the design choice), not *operative* (it
  discriminates no arm). That is acceptable for §2b.4, which asks only that the
  claim rest on a row; it is not a claim that the source measures anything.

### 1.2 FreeBSD `sysexits(3)` — **REJECT (decoration for the line half, contradiction for the exit half)**

- URL `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3`; opened
  2026-10-28; snapshot
  `.ufo/waves/round-55/w1/T55W1ScribeSources-receipts/sources/sysexits.html`,
  59251 B, sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`.
  Page: FreeBSD 15.1-RELEASE and Ports.quarterly, dated **May 9, 2024**.
- Located quotes (all present after whitespace normalisation):

| # | quote | words | locator |
|---|---|---|---|
| 1 | “This interface has been deprecated and is retained only for compatibility. Its use is discouraged.” | 15 | §DESCRIPTION |
| 2 | “This interface is not portable.” | 5 | §BUGS |
| 3 | “The choice of an appropriate exit value is often ambiguous.” | 10 | §BUGS |
| 4 | “Error numbers begin at EX__BASE to reduce the possibility of clashing with other exit statuses that random programs may already return.” | 21 | §ERRORS |

- **(a) one consistent line format — no.** The page is about exit values; it
  prescribes no message format. It is decoration for C2's line half.
- **(b) one exit code per class — nominally yes, actually the opposite.** It is
  the classic per-failure-class scheme, but it deprecates itself (“deprecated …
  discouraged”), calls the mapping ambiguous, and calls the interface
  non-portable. The lane's class is exit **2**; the page's codes begin at 64
  (`EX_USAGE` 64, `EX_OSERR` 71, `EX_CANTCREAT` 73, `EX_CONFIG` 78) and the page
  never names 2. Citing it for exit 2 would cite a document that contradicts the
  value. The registry already holds it as **S090** and already records the
  deprecation in S090's scope, so there is nothing to add and nothing to
  supersede.
- **Verdict: reject.** Refusal is right; the *reason* the round recorded is wrong
  (§4, F2).

---

## 2. §2b.4 as landed — the falsification

§2b.4 (`.ufo/prompts/tameshi-round-55.md:69-71`):

> **At least one sourced claim** — one of the round's claims rests on a
> `SOURCES.md` row opened this round: the knowledge entry or evidence it lands
> cites that `S###`.

The claim is C2 (operability). What it lands:

| landing | cites S280? | evidence |
|---|---|---|
| `corpus/knowledge/scratch-root-contract.md` (the “One line, every mode (round 55)” section, lines 71–102) | **no** (0 tokens; only S277, S278, S279 appear, lines 14, 19, 22, 28) | `claim-map.txt` |
| `.ufo/evidence/round-55/**` (all files) | **no** (0 files) | `grep -rl 'S280' .ufo/evidence/round-55/ \| wc -l` → 0 |
| `corpus/lessons/round-55.md` | yes (2 hits: the Gate row and the extraction pointer) — but the lesson is the §2b.1 record, not “the knowledge entry or evidence it lands” | `claim-map.txt` |

Two objections do not rescue it. (1) The lesson's Gate cites S280, and contract
v1 lets a lesson appear in `used-by` — but §2b.4 names “the knowledge entry or
evidence it lands”, and the Gate is separately mandated by §2b.1 for *every* new
row; if the Gate counted, §2b.4 would be satisfied for every round by §2b.1 and
would mean nothing. (2) `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`
*is* the source's extraction and its filename carries the id, but it is evidence
*of the source*, not the C2 claim's landing evidence (the counter is), and its
content names no `S`-id. Neither is the knowledge entry or the claim's evidence.

The Gate asserts the opposite: “`corpus/knowledge/scratch-root-contract.md` cites
it for the ‘one program-prefixed line’ shape”. That sentence is false against the
committed bytes. The Search log at `corpus/SOURCES.md:517` repeats it (“mined by
`corpus/knowledge/scratch-root-contract.md`”), and the row's `used-by` cell names
the same path first.

Why it happened is visible in the wave: the note scribe wrote the citation into
its draft —

```
draft-section.md:25  … when it follows the program name (S280) — which is why the class is one line
draft-section.md:76  and S280 is the authority for the one-line shape. The nine-mode and
```

— and the landing kept neither sentence (the landed section instead says “The
line is the contract; the Python type is not” with no authority named). Seat
`T55W1ScribeNote` F4 reported exactly this before the landing. The landed note is
therefore the document §2b.4 names, and it fails.

**Consequence, stated plainly:** as of `9cf0146`, the round's frontier step is
missing its one sourced claim. C2 can still score `C2_R55_PASS=true`, because the
C2 counter's note arm matches only the grammar and the nine mode labels. The
requirement is asserted in the lesson and checked by nobody.

And with the citation restored, the source still covers only the line half; the
exit-2 half remains a lane declaration. That is not a defect *if it is said* —
the Gate does say it — but the round must not claim “C2 rests on the sources
opened this round” without that qualifier.

---

## 3. Contract v1 on the proposed rows

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md:64-130` (fleet), carried
verbatim from `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`.

### 3.1 S280 (appended at C0)

| field | value at `9cf0146` | contract v1 | verdict |
|---|---|---|---|
| `id` | S280 | next unused; no reuse | **PASS** (S279 was the last; census E03 silent) |
| `source` | “Formatting Error Messages (GNU Coding Standards §4.4) — URL” | title — canonical URL | **PASS** |
| `kind` | `spec` | enum | **PASS** |
| `tier` | `A` | A = primary/authoritative **for that scope** | **FAIL (scoped)** — `scope` is the generic “the line shape of a noninteractive program's error message”; the document is the GNU standards' chapter “Program Behavior for All Programs”. A is honest only if the scope names GNU's convention. |
| `scope` | generic line shape | the claim the tier applies to | **CONCERN** — see tier |
| `anchor` | “§4.4 … @ fetched 2026-10-28 (… extraction sha256 `edcaf94b`; the quote sits at the section's … rule)” | exact section/heading/page/line **plus revision** (version, commit, or publication date) | **FAIL** — “fetched 2026-10-28” is the access date (already in `opened`), not the page's revision. The page states “last updated April 27, 2026”; `grep -c 'April 27, 2026' corpus/SOURCES.md` → 0. |
| `teaches` | line shape + “the message **must not** begin with a capital letter or end with a period”; “**one** program-prefixed line is the standard's shape” | one grounded learner benefit | **PASS with an unmarked inference** — casing and no-period are in the page (as “should not”); “one” and the modal “must” are not. Mark `[INFERENCE]` or attribute the count to the counter. |
| `status` | `mined` | “cited by ≥1 path in `used-by`” | **PASS only via the lesson** — the note path does not cite the row |
| `opened` | 2026-10-28 | past/present ISO date | **PASS** |
| `recheck` | `730d` | ISO date or cadence (`90d`, `180d`, `on-release`) | **PASS** — `NNd` form, accepted by census E09; same cadence as S277 for a stable spec |
| `used-by` | `corpus/knowledge/scratch-root-contract.md, corpus/lessons/round-55.md` | paths of the knowledge entries **or lessons citing the row** | **FAIL for the first path** — the note cites S280 zero times. The census cannot see this: E11 checks only that the path exists (it does). |
| Gate quote | §4.4, `program:sourcefile:lineno: message` … `program: message` | ≤25 words, located | **PASS** — 14 whitespace tokens (the lesson says 17; still far under the ceiling) |

### 3.2 S281 (the withdrawn sysexits row)

The round opened sysexits this round and refused it **before append**, recording
the refusal in the lesson and the Search log “not as a row”. §2b.1 says
“**Rejections stay as rows with reason and flip**”, and contract v1 defines the
rejected-row form (`REJECTED: <reason>; flip: <what would change the verdict>`)
and the `rejected` status (“kept — a rejection is evidence of taste”). The
round's stated reason — “within-scope duplicate URL (CORPUS.md rule 2, census
W04)” — is wrong on both citations:

- contract rule 2 is *Append-only* (it forbids editing history, not a second row);
- `W04` is a **warning** that does not change a lane's clean status
  (`scripts/sources-census.sh:33`), and `E04` fires only for the **same scope**
  **and** `status != rejected` (`:648-650`).

I demonstrated all three cases on a scratch copy of the lane registry (the full
lane corpus/tools copied so E11 resolves):

| scratch case | census output for S281 | rc |
|---|---|---|
| `status=rejected`, different scope | `W04 … across scopes` + `ok` | **0** |
| `status=queued`, different scope (the draft's scope) | `W04 … across scopes` + `ok` | **0** |
| `status=queued`, S090's exact scope | `E04 … within scope …` | **1** |

(`census-synthetic-rejected.txt`, `census-synthetic-cross-scope.txt`,
`census-synthetic-same-scope.txt`.) The draft's scope (“FreeBSD's own statement
that its pre-defined exit-code interface is deprecated …”) is not S090's scope
(“BSD exit-status conventions for command-line programs; legacy and deprecated by
its own text”), so the draft would never have triggered E04. **The rejection
could and, under §2b.1, should have been landed as a `rejected` row** — the
census accepts it, and the row is the only durable evidence of the refusal.

With the row as drafted (reason/flip rewritten to the substantive reason), every
cell passes: `id` S281 next unused; `kind docs`; `tier A` over the page's own
statement about itself; `anchor` §DESCRIPTION/§BUGS with the page date May 9,
2024 (**revision present**); `teaches` `REJECTED: …; flip: …`; `status rejected`;
`opened 2026-10-28`; `recheck 365d`; `used-by —`.

---

## 4. Findings

**F1 (high) — §2b.4 is not met, and the record says it is.** The note does not
cite S280; the Gate and the Search log assert that it does; the C2 counter does
not check citations, so the claim can score while the frontier step is missing.
Receipts: `claim-map.txt`, `sourced-claim-audit.txt`.

**F2 (high) — the sysexits rejection was not kept, and the recorded reason is
wrong.** §2b.1 and contract v1 keep rejections as rows; the census demonstrably
accepts a `rejected` S281 row on the held URL (rc 0, W04 only). The cited
“within-scope duplicate” is neither a rule-2 violation nor an E04 hit.
Receipts: `census-synthetic-*.txt`.

**F3 (medium) — S280's `used-by` first path is false.** The note cites S280 zero
times; `mined` is satisfied only by the lesson path. The census's E11 checks
existence, not citation, so this is invisible to conformance.

**F4 (medium) — S280's `anchor` omits the source's revision.** Contract v1
requires “section/heading/page/line **plus revision (version, commit, or
publication date)**”. The anchor carries the access date only; the page's own
stamp “last updated April 27, 2026” is absent from the registry (`grep -c` → 0).

**F5 (medium) — tier A is asserted over a scope wider than the source's
subject.** The page is the GNU standards' “Program Behavior for All Programs”;
the scope is generic. Tier is scoped to the scope, never global (contract v1).
Fix: qualify the scope to GNU's convention, keep A.

**F6 (low) — “one line” and “must not” overreach the source.** The page says
“should look like this” and “should not begin/end”; it never says “one line”
(0 hits). The row should mark the one-line reading `[INFERENCE]` or attribute it
to the counter, and use the page's modal.

**F7 (low) — the Gate quote's stated word count is not reproducible.** The quoted
span is 14 whitespace tokens (12 + 2); the Gate says 17. Both are under the
25-word ceiling, so this is a record accuracy nit, not a contract breach.

**Not a finding (checked):** the S280 row has 11 cells, one pipe-free cell each,
no duplicate id, a valid `kind`/`status`/`opened`/`recheck`; the live census exits
0 on 140 rows (`census-live.txt`); the base had 139 rows, so S280 is the round's
only new row.

---

## 5. Smallest safe corrections

`corpus/**` and `tools/**` are production files: these are proposals. The L1
integrates. All are one-cell / one-paragraph edits; none touches the frozen
counter set.

### 5.1 Restore the citation in the note (turns §2b.4 from false to true)

In `corpus/knowledge/scratch-root-contract.md`, after the grammar block in
`## One line, every mode (round 55)`, add the sentence the draft carried:

```
+The shape is the standard's, not an invention: §4.4 of the GNU Coding Standards
+prescribes `program: message` for a noninteractive program, the message starting
+lower-case after the program name and not ending with a period (S280). The *one
+line per failure* reading is [INFERENCE]: the page gives the form, not a count;
+the counter is what enforces one line.
```

and end the section with the draft's sources paragraph:

```
+Sources: S277-S279 remain the authority for the `TMPDIR` arms above (S277 the
+definition, S278 the resolver's skip-empty rule, S279 the documented order), and
+S280 is the authority for the line's shape. The nine-mode and five-mode
+inventories are the round-55 counter's own table
+(`.ufo/evidence/round-55/c2/measure.py`) — a lane measurement, not a sourced claim.
```

This makes S280's first `used-by` path true and gives §2b.4 its citation. (The
landed note's round-55 section cites nothing at all today.)

### 5.2 S280 row: add the revision and qualify the scope

```
-| S280 | … | spec | A | the line shape of a noninteractive program's error message | §4.4 Formatting Error Messages @ fetched 2026-10-28 (reader extraction `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`, sha256 `edcaf94b`; the quote sits at the section's noninteractive-program rule) | …
+| S280 | … | spec | A | GNU's convention for a noninteractive program's error message: the `program: message` form, the message's casing and final punctuation; it states nothing about exit codes | §4.4 Formatting Error Messages @ page "last updated April 27, 2026" (HTML comment, raw byte 204), fetched 2026-10-28 (reader extraction `.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt`, sha256 `edcaf94b`; sentence at raw byte 5020, forms at 5154 and 5415, casing rule at 6247, no-period rule at 6501) | …
```

If C0 is already final, contract rule 2 makes the route a `supersedes S280 —`
row; if the content commit is still open, fold both cells into it.

### 5.3 Keep the rejection as a `rejected` row

```
| S281 | sysexits(3), FreeBSD 15.1-RELEASE and Ports.quarterly manual page — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | docs | A | FreeBSD's own statement that its pre-defined exit-code interface is deprecated, and why its BUGS section calls the choice of exit value ambiguous; not a ground for the lane's class code | §DESCRIPTION deprecation sentence at byte 49849, §BUGS at 53809 and 53846, §ERRORS EX__BASE at 50084; page dated May 9, 2024 | REJECTED: the page deprecates the per-class scheme it would be cited for and calls the choice of exit value often ambiguous, so it cannot ground one exit code per class; flip: an authoritative, non-deprecated source assigning one exit status to a cannot-evaluate class | rejected | 2026-10-28 | 365d | — |
```

Census-verified: rc 0, one `W04` warning, no `E04` (`census-synthetic-rejected.txt`).

### 5.4 Correct the two false sentences

- Lesson Gate: replace “`corpus/knowledge/scratch-root-contract.md` cites it” with
  “cites it only after the note edit in this round lands; at C0 it does not”, and
  mark “one program-prefixed line” as an inference.
- `corpus/SOURCES.md:517` Search log: replace “mined by
  `corpus/knowledge/scratch-root-contract.md`” with the same conditional, and
  replace the duplicate justification with the substantive one (the page cannot
  ground the claim; the held URL is S090).

### 5.5 If the exit half must be sourced at all

Do not use sysexits. The honest row is `own-work`, tier A (allowed for “the
lane's own re-runnable gate output”), citing
`.ufo/evidence/round-55/c2/measure.py` + `tools/registry.json` for exit 2, cited
from the note. Otherwise keep the Gate's current wording (“lane declaration”) and
do not present the exit code as sourced.

---

## 6. Sweeps run (so “nothing found” is checkable)

| # | command | outcome |
|---|---|---|
| 1 | `sha256sum` of both committed snapshots | match the scribe's digests (`54c55cd4…`, `1fc793a2…`) |
| 2 | render `gnu-errors.html`, count `exit`, `status`, `one line`, `EX_` | 0, 0, 0, 0 |
| 3 | render, locate the §4.4 rule and the casing/no-period sentences | present; chapter title “Program Behavior for All Programs” |
| 4 | render, locate the 4 sysexits quotes | all present after whitespace normalisation |
| 5 | sysexits code sweep `EX_USAGE/EX_OSERR/EX_CANTCREAT/EX_CONFIG`, `64/71/73/78` | present; no `exit 2`, no `could-not-evaluate` |
| 6 | `grep -c S280` on the note, `grep -rl S280 corpus/knowledge/`, `.ufo/evidence/round-55/` | 0, 0, 0 |
| 7 | `grep -c S280` on the lesson and on SOURCES | 2, 3 |
| 8 | draft-vs-landed citation comparison | draft cites S280 twice; landing kept neither |
| 9 | S280 row cell split | 11 cells, no pipe inside a cell, `spec`/`A`/`mined`/`730d` |
| 10 | `grep -c 'April 27, 2026'` in the registry | 0 (anchor has no revision) |
| 11 | word count of the Gate's quoted span | 14 tokens (Gate says 17, still ≤25) |
| 12 | live census validate | rc 0, 140 rows |
| 13 | synthetic census: rejected S281, different scope | W04 + ok, rc 0 |
| 14 | synthetic census: queued S281, different scope | W04 + ok, rc 0 |
| 15 | synthetic census: queued S281, S090's scope | E04, rc 1 |
| 16 | base row count (`git show 0a2010ac:corpus/SOURCES.md`) | 139 → S280 is the only new row |

## 7. Boundaries

- **No counter run.** I make no `C1_R55_PASS`/`C2_R55_PASS` claim. My audit is of
  the records and the served bytes, not of the tools' behaviour.
- **No production edit.** `corpus/**`, `tools/**`, `SKILL.md`, `SCORECARD.md`,
  `LOG.md` untouched; only my seat's `.md`/`.json`/`-receipts/` were written.
- **No mutating git/jj.** Scratch synthetic registries were plain file copies;
  no commit was made anywhere.
- No tool installed or upgraded (none needed).
- Observed but out of scope: the assignment's base figures (`premise=10/10`,
  `grammar=6/8`, `total=18`) are the pre-amendment values; the frozen contract on
  disk declares amendments 1–7 and the base receipts now read
  `premise=9/10 … total=10` and `grammar=6/9 … total=21`. The frozen set is not
  mine to change; the L1 owns which figure the report quotes.
- Overlap: seats `T55W1ScribeSources`, `T55W1ScribeNote` and `T55W1RevSources`
  found adjacent items (the scribe's F6 counts, the note's F4 citation gap, the
  reviewer's F2/F4/F8). This seat re-derived every claim above from the bytes;
  where the conclusions coincide they are independent confirmations, not
  quotations.

## 8. Artifacts (relative to the lane root)

| path | what |
|---|---|
| `.ufo/waves/round-55/w1/T55W1CritSourcedClaim.md` | this report |
| `.ufo/waves/round-55/w1/T55W1CritSourcedClaim.json` | machine-readable verdicts, checks, findings, corrections |
| `…-receipts/source-audit.txt` | snapshot digests, revision stamp, §4.4 rendered rule, absence sweep, sysexits quotes and code range |
| `…-receipts/claim-map.txt` | every S280 citation in the lane, the note's S-id list, the dropped draft lines |
| `…-receipts/contract-checks.txt` | the S280 row's 11 cells and the contract-v1 field-by-field verdicts |
| `…-receipts/sourced-claim-audit.txt` | §2b.4 inputs: note/lesson/evidence citations, row cells, quote counts, anchor revision |
| `…-receipts/census-live.txt` | live validate rc 0, 140 rows |
| `…-receipts/census-synthetic-rejected.txt` | rejected S281 row: W04 only, rc 0 |
| `…-receipts/census-synthetic-cross-scope.txt` | queued S281, different scope: W04 only, rc 0 |
| `…-receipts/census-synthetic-same-scope.txt` | queued S281, S090's scope: E04, rc 1 |
