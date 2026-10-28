# T55W1RevSources — the round-55 source rows, reviewed

Seat `T55W1RevSources` (reviewer, L1 `TameshiR55`), tameshi round 55.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base
`0a2010acd1e92e4e332774050825e21bcfc7e079`; lane HEAD at review time
`631cd6455e58dce969310b4c0466c3383d9f5108`. Access date **2026-10-28**.

Item: open every source row the sources scribe proposes
(`.ufo/waves/round-55/w1/T55W1ScribeSources.md`/`.json`) and check the URL
resolves, the quote is verbatim at its locator, the quote is ≤25 words, the
tier is right under `corpus/SOURCES.md` contract v1, and the row parses as 11
columns with no pipe inside a cell. Say per row whether the row supports the
uniform-line claim.

**I opened both URLs myself and did not take the scribe's locators on faith.**
Both re-fetches are **byte-identical** to the snapshots the scribe committed,
so every offset below is reproducible from a fixed file:

```
gnu  https://www.gnu.org/prep/standards/html_node/Errors.html  http=200 bytes=7147  sha256 54c55cd4de53023b…  (identical to the snapshot)
bsd  https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 http=200 bytes=59251 sha256 1fc793a298a937d7… (identical to the snapshot)
```

Receipt `T55W1RevSources-receipts/fetch.stdout` (re-run at 14:01, 8 minutes
after the scribe's fetch). The GNU page's own revision stamp is
“last updated April 27, 2026” (HTML comment, raw byte 204); the FreeBSD page
footers **May 9, 2024**.

**The tree moved under the review.** At 13:56 the admitted row was kind `docs`
with a teaches ending “…the message text does not repeat the program's own
verdict vocabulary” (`corpus/SOURCES.md` sha256 `c78c0ab9…`). At 14:01 the same
row was kind `spec` with the clause gone (`corpus/SOURCES.md` sha256
`57ece0e5…`). Where a finding was true only of the earlier bytes I say so and
mark it closed; the remaining corrections are true of the current row.

---

## 1. Verdicts

### 1.1 S280 — GNU Coding Standards §4.4 — **ADMIT, with three corrections**

**URL resolves.** 200, 7147 B, `text/html`; identical bytes to the committed
snapshot. Not a bare homepage: the node is §4.4 of the standards.

**Quotes** (all ≤25 words; every one present in the section):

| quote | offset | words | verbatim at offset? |
|---|---|---|---|
| `Error messages from other noninteractive programs should look like this:` | 5020 | 10 | **raw** ✓ |
| `program:sourcefile:lineno: message` | 5154 | 2 | rendered only — raw bytes are `<var class="var">program</var>:<var…` |
| `program: message` | 5415 | 2 | rendered only — raw bytes begin `<var class="var">` |
| `The string message should not begin with a capital letter when it follows a program name and/or file name` | 6247 | 19 | rendered only — raw bytes are `<p>The string <var class="var">message` |
| `Also, it should not end with a period.` | 6501 | 8 | **raw** ✓ |

Receipt `locators.stdout`. The quotes exist and are faithful; the failure is
only in how the locator is labelled (F5).

**Tier.** `A` is right for **GNU's own convention**. It is **not** right for
“the line shape of a noninteractive program's error message” simpliciter: the
page is the GNU Coding Standards and it says “Error messages from other
noninteractive programs” inside a chapter addressed to GNU programs. Contract
v1: “`tier` — scoped to `scope`, never global.” → **correction C1** (F2).

**Columns.** pipes = 12 → 11 cells, no empty cell, no pipe inside a cell. The
live census passes (140 rows, `malformed=0`, `exit=0`; receipt
`census-live.stdout`).

**Does it support the uniform-line claim?** **Half of it, exactly.**
§4.4 grounds (a) the `program: message` line form, (b) the message “should not
begin with a capital letter when it follows a program name”, (c) “should not
end with a period”. It grounds **neither** the word “one” nor any exit code:

```
§4.4: exit=0 status=0 'one line'=False
§4.8 Standards for Command Line Interfaces (fetched 2026-10-28): exit=0 status=0
Contents (all 79 node titles, §4.4 and §4.8 among them): exit=0 status=0  (no exit/status node)
```

Receipts `gnu-absence-sweep.stdout`, `page-text/gnu-errors-4.4.txt`. So the
row may be cited for *the shape of the line* and for the two punctuation
rules; “one line per failure” and “exit 2” are the lane's own decisions. The
scribe's own audit says the same (`one_exit_code_per_class: false`), and the
round-55 Gate already states “it says nothing about the exit code, so the
round's exit-2 class is a lane declaration”. The remaining overreach is the
word **one**, which the row must mark as inference → **C2** (F3).

**Corrections.** C1 scope → GNU-qualified (tier then honest). C2 teaches →
say “the prescribed shape”, mark the one-line reading `[INFERENCE]`, and carry
the casing and no-period rules (the tree already added both at 14:01 — good).
C3 anchor → name the page's revision, and mark which offsets are rendered
rather than raw (F5, F8).

**The row as I would write it** (drop-in; 11 columns, pipes = 12, quote = 18
words):

```
| S280 | Formatting Error Messages, GNU Coding Standards §4.4 (page last updated April 27, 2026) — https://www.gnu.org/prep/standards/html_node/Errors.html | spec | A | GNU's own convention for a noninteractive program's error message: the `program: message` line form, the message's casing and final punctuation; it states nothing about exit codes | §4.4 "Formatting Error Messages": noninteractive sentence at raw byte 5020, first form at rendered 5154, second form at rendered 5415 (`<var>`-wrapped), casing rule at rendered 6247 (`<p>`/`<var>`), no-period rule at raw 6501, revision stamp at raw 204 (HTML comment); snapshot `.ufo/waves/round-55/w1/T55W1ScribeSources-receipts/sources/gnu-errors.html` 7147 B sha256 54c55cd4, refetched 2026-10-28 byte-identical | "Error messages from other noninteractive programs should look like this: program:sourcefile:lineno: message ... or like this: program: message" — the prescribed shape is a program-prefixed message line, `program: message`, the message not beginning with a capital letter and not ending with a period; the section mentions no exit status [INFERENCE: "one line" is not stated anywhere on the page — it follows from the template and from "The sentence conceptually starts at the beginning of the line"] | mined | 2026-10-28 | 730d | corpus/knowledge/scratch-root-contract.md, corpus/lessons/round-55.md |
```

Word count of the quoted span: 18 including the ellipsis, 17 excluding (the
scribe's audit says 17; the Gate now says 17). Both under the ceiling.

### 1.2 S281 — FreeBSD `sysexits(3)` — **REJECT** (agree with the verdict, not the reason)

**URL resolves.** 200, 59251 B, `text/html`; identical bytes to the committed
snapshot. Page: “FreeBSD 15.1-RELEASE and Ports.quarterly Manual Pages”, dated
May 9, 2024.

**Quotes** (all ≤25 words): deprecation sentence in §DESCRIPTION
(`This interface has been deprecated and is retained only for compatibility.
Its use is discouraged.`, 15 words); §BUGS `This interface is not portable.`
(5) and `The choice of an appropriate exit value is often ambiguous.` (10);
§ERRORS `Error numbers begin at EX__BASE …` (21) and `The meaning of the codes
is approximately as follows:` (9). All four are present; only the first three
are in the row's `teaches`/anchor, and §BUGS is the decisive one.

**Does it support the uniform-line claim?** **No — it argues against the
exit half.**

- It is about exit codes, not about line formatting at all.
- Its own text deprecates the scheme it would be cited for: “This interface
  has been deprecated and is retained only for compatibility. Its use is
  discouraged.”
- Its §BUGS says the mapping is not even well defined: “The choice of an
  appropriate exit value is often ambiguous.”
- The lane's class is exit **2**; `sysexits` assigns 64–78 and never names 2.
  Citing it for exit 2 would be citing a document for a value it contradicts.

**The reason recorded for the refusal is wrong.** The round-55 Gate says “a
new row would be a within-scope duplicate URL (CORPUS.md rule 2, census W04)”.
Neither supports that:

- `CORPUS.md`/contract rule 2 is “Append-only… A correction is a new row whose
  `teaches` opens `supersedes S0NN —`”. It does not forbid a second row on a
  held URL.
- `W04` is a **warning**, not a failure (`scripts/sources-census.sh:33`,
  `:645`), and the same-scope error `E04` (`:649`) requires *the same scope* —
  S090's scope (“BSD exit-status conventions…; legacy and deprecated by its
  own text”) and the draft's (“FreeBSD's own statement of the pre-defined
  per-failure-class exit-code scheme…”) are not the same.
- Demonstrated: live tree + the S281 draft → `W04` only
  (`W04 S281 duplicate url man.freebsd.org/… across scopes`), no `E04`
  (`census-synthetic.stdout`).

And S090 already carries the deprecation in its `scope` cell, so there is
nothing to `supersedes`. **Correct wording:** “S090 already holds this
document and already records the deprecation; the contract's only re-append
route is a `supersedes S090 —` row, and there is nothing to supersede. The
substantive reason is that the page cannot ground the claim.” The L1's choice
to record the refusal in the lesson rather than as a row is then legitimate
(rejected rows are optional; the registry is “a short registry of opened,
honestly tiered rows”, contract rule 4).

**What would support the exit half** (what the row's `flip` should say):
a normative or maintainer source that (a) assigns one non-zero status to a
*cannot-evaluate / unusable-environment* class and (b) is not deprecated — or,
honestly, the lane's own frozen counter and `tools/registry.json` declaring
exit 2 for the class, cited as `own-work` (tier A is allowed for “the lane's
own re-runnable gate output”). No external standard is required if the round
says “lane declaration” — which the Gate already does.

**The row as I would write it, if the L1 wants the rejection on the record:**

```
| S281 | sysexits(3), FreeBSD 15.1-RELEASE and Ports.quarterly manual page — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | docs | A | FreeBSD's own statement that its pre-defined exit-code interface is deprecated, and why its BUGS section calls the choice of exit value ambiguous; not a ground for the lane's class code | §DESCRIPTION deprecation sentence at rendered byte 49849, §BUGS at 53809 and 53846, §ERRORS EX__BASE at 50084; page footered May 9, 2024; snapshot `.ufo/waves/round-55/w1/T55W1ScribeSources-receipts/sources/sysexits.html` 59251 B sha256 1fc793a2, refetched 2026-10-28 byte-identical | REJECTED: the page deprecates the per-class scheme it would be cited for and calls the choice of exit value often ambiguous, so it cannot ground one exit code per class, and it never names the lane's 2; the URL is already held as S090, which already records the deprecation; flip: a non-deprecated normative source assigning a specific non-zero status to a cannot-evaluate class, or the lane's own counter and registry declaring 2 as own-work | rejected | 2026-10-28 | 365d | — |
```

### 1.3 The withdrawn S280 draft — withdrawal right, stated reason wrong

The scribe withdrew its S280 draft because the L1 had already appended the
same URL. Right call. But the same mis-citation appears in the withdrawal
reason (`rows_withdrawn[0].reason`: “a second row would be a within-scope
duplicate (CORPUS.md rule 2 / census W04)”) — see §1.2. The accurate reason is
“the row is already admitted at this URL; the draft's substance belongs in a
correction of the admitted row, not in a second row.”

Note also that correcting an uncommitted row **in place** is not what rule 2
permits either: “Only `status`, `recheck` and `used-by` change in place, and
each change is logged old→new in the round lesson.” The tree's in-place change
of `kind`, `scope`, `teaches` therefore needs an old→new entry in
`corpus/lessons/round-55.md` `## Gate`, or a `supersedes S280 —` row if the
append is already committed. (F1)

---

## 2. Findings

### F1 (high) — the admitted row's `teaches` carried an unsourced clause; the in-place fix needs a logged old→new
At 13:56 the row taught “…and the message text does not repeat the program's
own verdict vocabulary”. §4.4 has **no** such rule:

```
§4.4 hits for 'verdict': 0   'repeat': 0   'verdict vocabulary': 0
§4.4 hits for 'capital letter': 2   'period': 2   'exit': 0
```

(`unsourced-clause.stdout`; the phrase also exists in S272, about a different
tool, which is presumably where it came from.) At 14:01 the row was rewritten
(kind `spec`, clause gone, casing + no-period rules added; `corpus/SOURCES.md`
sha256 `c78c0ab9…` → `57ece0e5…`). **Closed for the bytes now on disk, open for
the record:** contract rule 2 requires the change be logged old→new in the
round lesson, and the final commit must carry the corrected text, not the
13:56 text.

### F2 (medium) — tier A over a scope that is not the source's
`scope` = “the line shape of a noninteractive program's error message”. The
source is authoritative for GNU's programs, not for noninteractive programs.
Under contract v1 (“tier — scoped to `scope`, never global”) this is tier
inflation. Fix: C1 above. Evidence: the page's own subject line and the 79-node
contents, both GNU-scoped.

### F3 (medium) — “one line” is an inference, and the C2 note uses S280 for it
The note draft (`T55W1Er10.md`, seat `T55W1ScribeNote`) says “The shape itself
is the standard's: a noninteractive program's message is one program-prefixed
line … which is why the class is one line”. The page never says “one line”
(0 hits) and has no line-count rule; the nearest ground is the parenthetical
“The sentence conceptually starts at the beginning of the line”. The claim is
fine as a *reading*, but a citation must mark it. Fix: C2's `[INFERENCE]`, or
have the note attribute the one-line count to the counter (which does enforce
it) rather than to §4.4.

### F4 (medium) — `mined` + `used-by` name a note that does not cite S280
`used-by` = `corpus/knowledge/scratch-root-contract.md, corpus/lessons/round-55.md`.
The lesson cites it (Gate, 2 hits). The note does **not**:
`grep -c S280 corpus/knowledge/scratch-root-contract.md` → **0**, and its
round-55 section (`## One line, every mode (round 55)`, now landed at line 71)
cites no source id at all — the draft's closing paragraph (“Sources: S277-S279
… and S280 is the authority for the one-line shape”) did not survive the
landing. So the section states “The class is one stderr line, byte-shaped” and
“The line is the contract” with **no authority named**, which is exactly the
gap this row was opened to close. `mined` is satisfied by the lesson, so the
census passes, but the first path is a forward reference — the class
`CORPUS.md` names as “An index row is a claim. Write the row when the file
exists, not before.” Cite S280 there (with F3's `[INFERENCE]` marking), or drop
that path. Receipt `note-citation.stdout`.

### F5 (low) — locator labels: “raw” where the bytes are markup
`check-locators.py` verifies a *raw prefix* that is a tag (`b'<var class="var">program</var>:<var…'`,
`b'<p>The string'`) and then a *rendered* match, and prints `raw=True` for
both. Reproduced independently (`locators.stdout`): offsets 5154, 5415, 6247
are not raw-verbatim; 49849, 50084, 50240 in sysexits are not either (double
spaces from the `<pre>` layout, `<b>EX__BASE</b>`, a line break). No quote is
fabricated — only the column's label overstates. Fix: call those “rendered”
in the anchor, as the row above does.

### F6 (low) — the Gate's duplicate citation is not in the record it cites
See §1.2. `W04` is a warning; `E04` needs a shared scope. Synthetic census:
`E11=170 W04=16 W01=1`, no `E04` (`census-synthetic.stdout`; `E11` is a
`--file`-mode artifact — used-by resolves against the file's directory,
`scripts/sources-census.sh:567`).

### F7 (high, governance — reported, not fixed) — the freeze manifest no longer pins the files it names
```
freeze.json amendments  at HEAD: []        in worktree: [1,2,3]
contract.json amendments in worktree: [1,2,3,4,5]
round-55.md header: "counter freeze 631cd645 + amendments 1-4 (all in freeze.json)"

contract.json      worktree 5de4f37b…  manifest ed6871e1…  DIFFERS
c1/measure.py      worktree 711507e7…  manifest 77abe1e9…  DIFFERS
c2/measure.py      worktree d6ca1d85…  manifest ab3ae751…  DIFFERS
no-harm.sh / deciding-run.sh / controls.sh                      MATCH
```
(`freeze-vs-tree.stdout`.) At the freeze commit the manifest matches all six
blobs exactly; in the working tree it matches three. Three records disagree on
how many amendments exist (3 / 5 / “1-4”). Also: `.ufo/evidence/round-55/before/c2.stdout`
was **0 bytes at 13:53** and held **43 lines** at the freeze commit; at 14:03
it holds the single summary line the assignment quotes, so the per-arm
`EXPLAIN` lines of the base receipt are gone from disk (the frozen blob keeps
them). **The frozen GRAMMAR regex itself is unchanged** (no `GRAMMAR` or
`could-not-evaluate` lines in the c2 diff), so the source claim reviewed here
is unaffected — but a manifest that matches neither HEAD nor the tree pins
nothing, and C1's own philosophy is that records must agree with the tree.

### F8 (low) — the anchor carries no revision
Contract v1: “`anchor` — exact section / heading / page / line plus revision
(version, commit, or publication date).” The row's `@ fetched 2026-10-28` is
the access date, not the page's revision. The page states its own: “last
updated April 27, 2026” (raw byte 204, HTML comment). Add it (C3).

### F9 (low) — artifact collision on `T55W1Er10.md`
The sources scribe says its quotes and verbatim rows “live in `T55W1Er10.md`”,
but that path now holds seat `T55W1ScribeNote`'s draft section (it was
rewritten at 13:56, same minute as its `.json`). The scribe's row text survives
only in `T55W1ScribeSources.json`. Nothing is lost, but one filename was
written by two seats; the report's pointer is stale.

### F10 (low) — the note's class inventory understates the tree
The landed note says the tools “keep their own exception classes
(`ScratchRootUnusable` in the two round-55 edits, a local class in `env-diff`)”.
The tree has **six** local `class ScratchRootUnusable(RuntimeError)` —
`bash-witness-study.py:205`, `context-capture.py:300`, `env-diff.py:32`,
`evidence-disposition.py:191`, `pin-disposition.py:161`,
`repeat-control.py:148` — and `registry-check.py` declares none (it raises the
builtin `RuntimeError`, `:782`). Naming `env-diff` as a *different* “local
class” is the misleading part: it is the same class name, declared locally,
like five others. The draft stated this exactly (“six of the seven … and
registry-check declares no class at all”); the landed text lost that
precision. Receipt `type-claim.stdout`.

---

## 3. Sweeps run (so “nothing found” is checkable)

| # | command | outcome |
|---|---|---|
| 1 | `curl -sS -o gnu2.html -w 'http=%{http_code} bytes=%{size_download}' -L https://www.gnu.org/prep/standards/html_node/Errors.html` | 200 / 7147 |
| 2 | `curl -sS -o bsd2.html -w … -L 'https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3'` | 200 / 59251 |
| 3 | `sha256sum gnu2.html bsd2.html <committed snapshots>` + `cmp -s` | both byte-identical |
| 4 | 11-quote offset check (raw vs rendered vs word count) | 11 present; 6 raw-verbatim, 5 rendered-only |
| 5 | word recount of the two Gate quotes | 18/17 and 15 — Gate now says 17 and 15 ✓ |
| 6 | `grep -c 'verdict\|repeat'` on the rendered §4.4 | 0 / 0 |
| 7 | absence sweep: `exit`, `status`, `one line` in §4.4, §4.8 (fresh fetch, 6187 B) and the 79-node contents | 0 / 0 / absent in all three |
| 8 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | **exit 0**, 140 rows |
| 9 | contract census commands (rows / NF!=13 / duplicate ids / `\|` in cells) | 140 / 0 / empty / empty |
| 10 | synthetic A2 (base + corrected row inside Registry) | parses, no E-code from the row (only `--file` `E11` artifacts) |
| 11 | synthetic B2 (live tree + S281 draft inside Registry) | +1 `W04` only, no `E04` |
| 12 | `python3 grammar-vs-gnu.py` (scribe's, re-run) | `RESULT: PASS`, 7/7, grammar re-derived from `c2/measure.py` |
| 13 | `grep -n 'class ScratchRootUnusable(RuntimeError)' tools/*.py` + `sed -n 765,785p tools/registry-check.py` | 6 classes; registry-check raises builtin `RuntimeError` — the note's “six of the seven” is accurate |
| 14 | freeze manifest digest replay at HEAD and in the worktree | 6/6 at HEAD, 3/6 in the tree (F7) |
| 15 | both rows **as written in §1** inserted into a Registry copy and run through `validate --file` | S280: 12 pipes, 11 cells, 18-word quote, no code of its own; S281: exactly one `W04`, no `E04` (`reviewer-rows-parse.stdout`) |

## 4. Residual risk and verification gaps

- **No counter was run by this seat.** I make no `C1_R55_PASS`/`C2_R55_PASS`
  claim. My grammar receipt re-runs the scribe's checker against the frozen
  regex re-derived from `c2/measure.py`; it does **not** measure the seven
  tools' live stderr (that is C2's arms).
- The row supports the **shape**, and my “one line” correction is a reading of
  a template plus one parenthetical. A future round could find a stronger
  source for a one-line diagnostic rule (none exists in the GNU standards:
  the contents list has no such node, and §4.8 is silent too).
- `spec` vs `docs` is curation, not a rule: both are enum-valid. I recommend
  `spec` because the row's tier rests on the document being normative — the
  tree now says `spec`, the Gate calls it “a normative standard”, so the two
  agree.
- The note's round-55 section landed at 14:05 while I reviewed (F4, F10). The
  wording I quote is the landed text; the earlier draft in `T55W1Er10.md` had
  the source paragraph the landing dropped. If the section is edited again,
  F4 and F10 must be re-checked against it.
- F7 is a records-against-tree observation made at 14:03; the working tree was
  being edited while I read it, so the digests will differ again if the L1
  re-freezes. The *structure* of the finding (manifest lags contract, lesson
  count stale, base receipt lossy) will not change.

## 5. Touched surfaces

- **Wrote** (this seat's own paths only):
  `.ufo/waves/round-55/w1/T55W1RevSources.md`,
  `.ufo/waves/round-55/w1/T55W1RevSources.json`, and
  `.ufo/waves/round-55/w1/T55W1RevSources-receipts/` (`fetch.stdout`,
  `locators.stdout`, `word-counts.stdout`, `row-parse.stdout`,
  `tree-S280-cells.txt`, `unsourced-clause.stdout`, `gnu-absence-sweep.stdout`,
  `census-live.stdout`, `census-synthetic.stdout`, `type-claim.stdout`,
  `grammar-vs-gnu-rerun.stdout`, `freeze-vs-tree.stdout`,
  `reviewer-rows-parse.stdout`, `note-citation.stdout`,
  `page-text/gnu-errors-4.4.txt`, `page-text/gnu-errors-2026-10-28.html`,
  `sysexits-region.txt`).
- **Read only**: `corpus/SOURCES.md`, `corpus/lessons/round-55.md`,
  `corpus/knowledge/scratch-root-contract.md`, `corpus/CORPUS.md` (fleet),
  `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, `scripts/sources-census.sh`,
  `tools/*.py`, `.ufo/evidence/round-55/**`, the scribe's receipts.
- **No git/jj mutation anywhere**; no lane production file edited; no counter,
  contract, freeze manifest, no-harm or deciding-run script touched.
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku;
  S=$HYAKU_SCRATCH/tameshi-r55/T55W1RevSources` (fresh fetches, synthetic
  roots), removed at the end of the seat.
- No tool installed or upgraded: nothing was needed, so there is no
  tool/version/channel entry.
