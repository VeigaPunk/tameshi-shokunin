# T55W1ScribeSources — the sources C2's uniform-line claim rests on

Round 55, wave 1. Seat `T55W1ScribeSources`. Base
`0a2010acd1e92e4e332774050825e21bcfc7e079`. Access date **2026-10-28**.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Registry **read-only**.

Item: open the sources the C2 uniform-line claim rests on — GNU coding
standards "Errors" and FreeBSD `sysexits(3)` — and record, for each, the URL,
the access date, a ≤25-word located quote, the tier under the SOURCES contract
v1, and a proposed `S` row; reject whatever does not actually support *one
consistent line format / one exit code per class*.

Everything for this seat is in this file, `T55W1ScribeSources.json`, and
`T55W1ScribeSources-receipts/` — **nothing** under the name `T55W1Er10` (that
name is seat `T55W1Er10`'s; see F8).

## 0. What changed while this seat was reading

The item assumed two rows were still to be appended. They were not:

- **S280 already exists** — the L1 appended it at 13:52 on 2026-10-28 for the
  same GNU URL (`corpus/SOURCES.md:155`; the registry was clean at 13:49 and
  modified by 13:52).
- **`sysexits(3)` is already the registry's** — as **S090**
  (`corpus/SOURCES.md:99`), whose scope already reads "BSD exit-status
  conventions for command-line programs; legacy and deprecated by its own
  text". The L1 refused a second row before append and recorded the refusal in
  `corpus/lessons/round-55.md` `## Gate`.

So this seat **withdraws both drafted rows** (duplicates — `CORPUS.md` rule 2 /
census W04) and delivers what is still missing: byte-exact locators, the
independent verification of the refusal, and a **defect in the appended S280's
`teaches` cell** with a patch.

Registry state at audit: 140 rows, sha256
`c78c0ab988c2bfc893f7951218da11467341fdae33255b34eb2eb355ef7a793b`;
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → rc 0.

Method: both URLs opened at their canonical host (HTTP 200), the bytes
committed under `T55W1ScribeSources-receipts/sources/`, every quote re-located
from those committed bytes by `check-locators.py` (11/11 OK, rc 0). Offsets are
offsets into the **committed snapshot**, not into a live page.

## 1. GNU Coding Standards §4.4, "Formatting Error Messages" — S280

- **URL** — https://www.gnu.org/prep/standards/html_node/Errors.html
- **Access date** — 2026-10-28 (HTTP 200, 7147 B,
  sha256 `54c55cd4de53023b694f1195feb3e5a0a6198ed7f290c368442888356fda270c`)
- **Revision** — "The GNU coding standards, last updated April 27, 2026"
  (HTML comment, snapshot byte 204)
- **Tier** — **A**, kind `spec`: the GNU Coding Standards are the normative
  statement for GNU programs and this page is their primary carrier, read whole.
  The appended row says `docs`; the round's own Gate calls it "a normative
  standard (tier A)". `spec` is the consistent value (optional, in the patch).

Located quotes (all ≤25 words):

| # | quote | locator |
|---|---|---|
| 1 | "Error messages from other noninteractive programs should look like this:" | §4.4, snapshot byte 5020 (10 words) |
| 2 | "program:sourcefile:lineno: message" | §4.4, first literal form, snapshot byte 5154 |
| 3 | "program: message" | §4.4, second literal form — applies when there is no relevant source file, snapshot byte 5415 |
| 4 | "The string message should not begin with a capital letter when it follows a program name and/or file name" | §4.4, snapshot byte 6247, 19 words (`<var>` tags inside; the quote is the rendered text) |
| 5 | "Also, it should not end with a period." | §4.4, snapshot byte 6501, 8 words |

**What it supports.** Exactly one of C2's two halves: *one consistent line
format*. The page fixes the line as `program: message` for a noninteractive
program with no relevant source file, fixes the message's first character
(lower-case after the program name) and its last (no period). The frozen C2
line is that shape:

```
repeat-control.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<value>' (could-not-evaluate)
```

All seven tools' canonical lines pass the frozen regular expression *and* the
four GNU properties (one line, `program: message`, lower-case message, no final
period) — `grammar-vs-gnu.stdout`, 7/7 OK. The two negative controls (a
capitalised message, a trailing period) fail exactly the rule they violate, so
the check discriminates. The grammar is re-derived from the frozen counter
(`.ufo/evidence/round-55/c2/measure.py:46-50`), not from the assignment prose,
and the documented line in `corpus/knowledge/scratch-root-contract.md` matches
it once `<tool>` is substituted — the note and the counter state one grammar.

**What it does not support.** The word "exit" does not occur in the page
(`grep -c -i exit` → `0`), and the GNU Coding Standards' node index has no
exit-status node. The exit-2 half of C2 is a lane declaration carried by the
frozen contract and the note, never by this row.

### 1a. Defect in the appended S280, and the patch

Row as appended (`corpus/SOURCES.md:155`), tail of the `teaches` cell:

> "…one program-prefixed line is the standard's shape, **and the message text
> does not repeat the program's own verdict vocabulary**"

The bolded clause is **not in the source**. §4.4 says nothing about verdict
vocabulary; what it does say about the message text — no capital after the
program name (byte 6247), no trailing period (byte 6501) — the cell omits. The
round's own Gate does not claim it either: it admits S280 for the "one
program-prefixed line" shape and for the fact that the section "says nothing
about the exit code", so registry and lesson disagree about what the row
teaches.

Patch: `T55W1ScribeSources-receipts/S280-teaches-fix.patch` — replaces the
unsourced clause with the two grounded rules plus the no-exit-code limit, adds
the casing/period scope, widens the anchor with the page snapshot and byte
offsets, and sets `kind` to `spec`:

```
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -155,1 +155,1 @@
-| S280 | … | docs | A | the line shape of a noninteractive program's error message | §4.4 … | "…" — one program-prefixed line is the standard's shape, and the message text does not repeat the program's own verdict vocabulary | mined | 2026-10-28 | 730d | … |
+| S280 | … | spec | A | the line shape of a noninteractive program's error message, its casing and final punctuation, and nothing about exit codes | §4.4 … (page snapshot `…/sources/gnu-errors.html` 7147 B sha256 `54c55cd4`, sentence at byte 5020, forms at 5154 and 5415, casing rule at 6247, no-period rule at 6501; reader extraction … sha256 `edcaf94b`) | "…" — one program-prefixed line is the standard's shape; the message starts lower-case, ends without a period, and the section states no exit code | mined | 2026-10-28 | 730d | … |
```

The unabbreviated row is in the patch and in `T55W1ScribeSources.json`
(`corrections[0].proposed_row`). Demonstration (`patch-demo.stdout`): the lane
file copied to scratch, `patch -p1` applied — `verdict vocabulary` gone from
S280 (0 occurrences on that row), `NF=13`, 0 malformed rows, no duplicate ids,
no enum violations, both used-by paths resolve, `kind: spec`; the lane file's
sha256 is unchanged by the exercise, so the patch was never applied to the lane.

Disposition: apply **in place** while the row is uncommitted. If it is already
committed when this is read, the contract's correction form is a new row whose
`teaches` opens `supersedes S280 —` (the registry already carries same-URL
supersedes pairs: S047/S048, S160/S089, S268/S108).

## 2. FreeBSD `sysexits(3)` — already S090, no row

- **URL** — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3
- **Access date** — 2026-10-28 (HTTP 200, 59251 B,
  sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`)
- **Revision** — manpath `FreeBSD 15.1-RELEASE and Ports.quarterly` (the page's
  selector and `<title>`), footer `FreeBSD 15.1  May 9, 2024`

Located quotes:

| # | quote | locator |
|---|---|---|
| 1 | "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." | §DESCRIPTION, snapshot byte 49849, 15 words |
| 2 | "This interface is not portable." | §BUGS, snapshot byte 53809, 5 words |
| 3 | "The choice of an appropriate exit value is often ambiguous." | §BUGS, snapshot byte 53846, 10 words |
| 4 | "Error numbers begin at EX__BASE to reduce the possibility of clashing with other exit statuses that random programs may already return." | §ERRORS, snapshot byte 50084, 21 words |
| 5 | "The meaning of the codes is approximately as follows:" | §ERRORS, snapshot byte 50240, 9 words |

**Verdict: no row.** Two independent reasons, and the L1 gave the first:

1. **Duplicate.** S090 already holds this URL and its scope already says
   "legacy and deprecated by its own text" — the registry has absorbed the fact
   a new row would carry.
2. **It cannot support the claim anyway.** C2's second half is *one exit code
   per class*. The page deprecates the scheme, discourages its use, calls the
   interface non-portable and the choice of exit value ambiguous. Citing it
   would cite a page that argues the other way — the failure mode the
   contract's `teaches` field exists to prevent.

It also contradicts the lane's value: the class is exit **2**; `sysexits`
assigns 64–78 (`EX_OSERR` 71, `EX_CANTCREAT` 73, `EX_CONFIG` 78 are its nearest
candidates for an unusable scratch root) and its `EX__BASE` sentence exists to
keep those numbers clear of what other programs return. S090's own `teaches`
anchors "a usage exit of 64" — the registry's existing use of this document
points away from 2, not toward it.

## 3. Sweeps behind the negative claims

| question | command | result |
|---|---|---|
| does the GNU Errors page mention exit codes? | `grep -c -i exit sources/gnu-errors.html` | `0` |
| does the GNU Coding Standards have an exit-status node at all? | tag-strip `sources/gnu-node-index.html`, match `exit\|status` | no node (11825 B index, HTTP 200) |
| does `sysexits(3)` support one-exit-code-per-class? | read §DESCRIPTION, §ERRORS, §BUGS whole | no — deprecated, discouraged, non-portable, ambiguous |
| does either page name exit value 2 for this class? | read both class texts | no; `sysexits` assigns 64–78 |
| is either URL already in the registry? | `grep` the two URLs in `corpus/SOURCES.md` | GNU → S280; sysexits → S090 |

## 4. Findings

**F1 — the appended S280's `teaches` cell asserts a rule the source does not
contain** (§1a; patch + demonstration).

**F2 — `sysexits(3)` cannot support "one exit code per class"; it argues the
other way** (§2). No row; the byte offsets are offered so the Gate's refusal
quote is locatable in a committed snapshot.

**F3 — GNU §4.4 supports the line half and only the line half.** 0 occurrences
of "exit" in the page; no exit-status node in the standards. The exit-2 half is
a lane declaration.

**F4 — the frozen grammar is GNU-conformant and the note states the same
grammar.** `grammar-vs-gnu.py` re-derives the regex from `c2/measure.py`,
checks the regex and the four GNU properties per tool: 7/7 pass, with two
negative controls that fail exactly one rule each; the note's line matches the
frozen regex once `<tool>` is substituted.

**F5 — append hazard: the base `corpus/SOURCES.md` has no trailing newline.**
At base `tail -c 1` is `.`; appending without a leading newline glues the first
row onto the tail prose, so the row count falls to 140, the row is no longer a
row, and `validate` still exits 0 because a glued line does not begin with
`| S` — a row that disappears silently rather than a row that fails. Reproduced
in `append-check.stdout`. The L1's actual append carried the newline and the
current file ends `\n`, so nothing is broken today; the hazard is for the next
round appending to a file that ends mid-sentence.

**F6 — three numbers in the lesson's Gate do not match the tree.**
`corpus/lessons/round-55.md` says "Census at round end: exit 0, 141 rows" while
the registry holds **140** rows (`validate` rc 0) and S281 was refused; the
S280 quote cell says "(19 words)" where the quote is **17** words excluding the
ellipsis; the sysexits cell says "(14 words)" where it is **15**. Both quotes
sit under the 25-word ceiling, so the contract is not broken — the counts are
simply wrong and a later reader cannot check them.

**F7 — the base C2 receipt the assignment quotes was empty on disk while this
seat read.** `.ufo/evidence/round-55/before/c2.stdout` was **0 bytes**, mtime
`2026-10-28 13:50:09 -0300`; re-read 20 s later, still 0 bytes, beside a
2276-byte `c1.stdout` from 13:47:55. The assignment quotes
`grammar=6/8 … total=18 C2_R55_PASS=false` as this file's content. I did not
re-run the counter (frozen evidence, not this seat's work): the L1 must confirm
the base receipt carries the quoted line before the deciding run.

**F8 — name collision with seat `T55W1Er10`, and its repair.** This seat's item
named the deliverables `T55W1Er10.json` / `T55W1Er10.md` — seat `T55W1Er10`'s
own names. Those two files were written by this seat at 13:51 and 13:56 on
2026-10-28, **overwriting that seat's deliverables**; the fleet roster and the
65 KB `swarm-registry.json` both list `T55W1Er10` as a wave seat and its
`T55W1Er10-receipts/` (10 files, 13:50:03) was sitting beside them. Detected at
13:57 by a directory listing. Repair: the peer's exact `write`/`edit` payloads
were read from its session log (toolCall parts at lines 155, 161, 167, 170 of
`~/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f/T55W1Er10.jsonl`)
and replayed in order; the restored files are `T55W1Er10.json` 3640 B sha256
`2e15a640…` and `T55W1Er10.md` 11366 B sha256 `128c8e83…`, and the restored
JSON parses with `id: R54.10`, `derived: "controls-a rekeyed=0/7"`, matching
the peer's yielded `agent://T55W1Er10` output. Receipt:
`T55W1ScribeSources-receipts/peer-er10-restore.txt`. The peer and the L1 were
messaged. Seat `T55W1Er10` was then asked to verify, and did: both files match its originals
byte for byte (json 3640 B sha256 `2e15a640…`, md 11366 B sha256 `128c8e83…`, and both
post-write edits present at line 121 and line 169), so the replay reconstruction equals
what that seat wrote and no residual divergence remains. It asked that both files be left
as they are. This seat now writes only `T55W1ScribeSources.*`.

## 5. Touched surfaces

- **Wrote** (this seat's own paths only): `T55W1ScribeSources.md`,
  `T55W1ScribeSources.json`, and everything under
  `T55W1ScribeSources-receipts/`; plus the F8 restoration of `T55W1Er10.md`
  and `T55W1Er10.json` to their owner's bytes.
- **Read only**: `corpus/SOURCES.md`, `corpus/lessons/round-55.md`,
  `corpus/knowledge/scratch-root-contract.md`, `corpus/SOURCES-CONTRACT-v1.md`
  (fleet `.ufo/waves/kaika/`), `.ufo/evidence/round-55/c2/measure.py`,
  `.ufo/evidence/round-55/assimilation/*`, `.ufo/evidence/round-55/before/*`,
  the peer's session log and receipts. No frozen counter, contract, freeze
  manifest, no-harm or deciding-run script was modified; no lane production
  file was edited — the registry's sha256 is identical before and after the
  patch demo (`patch-demo.stdout`).
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku;
  S=$HYAKU_SCRATCH/tameshi-r55/T55W1ScribeSources` (snapshots, base copy,
  appended copies, patch demo). No git mutation anywhere; no clone needed.

## 6. Out of scope / not done

- No counter executed (C1 or C2): measurement is not this seat's item, so no
  `C2_R55_PASS` claim is made here and none of the receipts is a counter arm.
- The patch is a proposal, not an edit: `corpus/SOURCES.md` was never written.
- No tool installed or upgraded (none was needed).
- `corpus/lessons/round-55.md`, `QUALITY.md`, `LOG.md`, `SCORECARD.md`,
  `SKILL.md`, `tools/**` untouched — the L1 integrates.

## 7. Artifacts

| path (relative to the lane root) | what |
|---|---|
| `.ufo/waves/round-55/w1/T55W1ScribeSources.md` | this report: quotes, locators, audit, patch, collision |
| `.ufo/waves/round-55/w1/T55W1ScribeSources.json` | withdrawn drafts, audit, locators, sweeps, discrepancies, collision record |
| `…-receipts/sources/gnu-errors.html` | 7147 B, sha256 `54c55cd4…` |
| `…-receipts/sources/sysexits.html` | 59251 B, sha256 `1fc793a2…` |
| `…-receipts/sources/gnu-node-index.html` | 11825 B, sha256 `005dd3f4…` (exit-status sweep) |
| `…-receipts/{check-locators.py,locators.stdout}` | 11 locators re-derived from the snapshots, rc 0 |
| `…-receipts/{grammar-vs-gnu.py,grammar-vs-gnu.stdout}` | frozen grammar × GNU §4.4, 7/7 PASS |
| `…-receipts/{S280-teaches-fix.patch,patch-demo.stdout}` | the corrective diff and its demonstration |
| `…-receipts/{append-check.stdout,validate-rows.stdout}` | census rules on base + drafts; F5 reproduced |
| `…-receipts/peer-er10-restore.txt` | F8: the collision, the recovery source, the restored sizes and digests |
| `…-receipts/{fetch-headers.txt,census-start.stdout,proposed-rows.md}` | HEAD responses and digests; census rc 0; the withdrawn drafts |
