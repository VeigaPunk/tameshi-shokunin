# T56W2RevSources — independent re-open of round 56's new source rows (wave 2)

Seat: `T56W2RevSources` (wave 2, tameshi round 56, hyaku run 11).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
C0 (content commit under review): `c0137451f5b7f22d65f748fc69f1b181f55e1378`.
Base: `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`.
Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W2RevSources` (removed on exit).

## Target

The round added **two** registry rows to `corpus/SOURCES.md` (not one):

| id | source | status | used-by |
|---|---|---|---|
| S281 | Statement layer specification (in-toto Attestation Framework, Statement v1) | `mined` | `corpus/knowledge/receipt-revision-binding.md` |
| S282 | Build: Provenance (SLSA specification, predicate type `slsa.dev/provenance/v1`) | `rejected` | `—` |

The highest S-number is **S282**; the row the claim's `used-by` names is **S281**.
Both are re-opened below, because the item's checks (anchor resolves, `teaches`
grounded by the passage, `used-by` naming the knowledge entry) split across the
two, and the round's `## Gate` table carries a separate quoted passage for each.

## Verdict

**`gap-minor` — 3 findings**, all in lane files committed at C0. No lane file was
edited by this seat. Nothing found in `corpus/SOURCES.md` itself is false: both
rows' anchors resolve, both `teaches` cells are grounded by the real page text,
both rows are enum-clean, and the census passes.

The three findings are in the round's *evidence* for the rows, not in the rows:
the lesson's quote for S282 is not in the source, the knowledge entry's first
quote for S281 is a splice, and the knowledge entry's recheck line names a
selftest count the tree no longer produces.

---

## F1 — the lesson's quoted passage for S282 is not in the source (major)

**File:** `corpus/lessons/round-56.md:21` (the round-56 `## Gate` table).
**Claim:** the table quotes the S282 anchor's `§Model, first paragraph` as

> "Provenance is a predicate that describes how a software build was executed."

labelled *"(reader extraction, 11 words)"*.

The source does not contain that sentence at any revision I could reach. The
actual `§Model` first paragraph is:

```
Provenance is an attestation that a particular build platform produced a set of
software artifacts through execution of the `buildDefinition`.
```

### Commands and outputs

```
$ grep -n "Provenance is a predicate that describes how a software build was executed" \
      /fast/scratch/hyaku/tameshi-r56/T56W2RevSources/build-provenance.md
grep_exit=1                       # no match

$ awk 'NR>=40 && NR<=43 {printf "%d\t%s\n", NR, $0}' build-provenance.md
40	## Model
41	
42	Provenance is an attestation that a particular build platform produced a set of
43	software artifacts through execution of the `buildDefinition`.
```

The same absence holds against the lane's **own** wave-1 extraction receipt,
which is byte-identical to the live page (`sha256 efece57a…76fc`, receipt
`.ufo/waves/round-56/w1/T56W1ScribeSources-receipts/slsa-build-provenance.md`):

```
$ grep -c "Provenance is a predicate that describes how a software build was executed" \
      .ufo/waves/round-56/w1/T56W1ScribeSources-receipts/slsa-build-provenance.md
0
$ grep -n -A3 "^## Model" .ufo/waves/round-56/w1/T56W1ScribeSources-receipts/slsa-build-provenance.md
40:## Model
41-
42-Provenance is an attestation that a particular build platform produced a set of
43-software artifacts through execution of the `buildDefinition`.
```

So the receipt the lesson calls a "reader extraction" was fetched correctly and
holds the true text; the sentence the lesson quotes is in neither.

### The sweep (this is the whole reach, not a spot check)

The phrase was searched in the upstream repository at every revision I could
enumerate, not just at the row's anchor:

| where | command | result |
|---|---|---|
| `slsa-framework/slsa` @ main, full clone (310 files) | `grep -rn -i "describes how a software build was executed" .` | no hit |
| same clone | `grep -rn -i "predicate that describes" .` | no hit |
| `spec/build-provenance.md` @ prior touching commit `bc8d1b82` (2026-03-05) | `grep -n -i "describes how a software build was executed" bp-old.md` | no hit — `§Model` first para there is also "Provenance is an attestation that a particular build platform produced…" |
| `docs/provenance/v0.1.md` @ tag `v0.1` | `grep -c -i "describes how a software build was executed"` | 0 — `§Model` there reads "Provenance is a claim that some entity (`builder`) produced one or more software artifacts…" |
| `docs/provenance/{index,v0.2,v1-rc1,v1-rc2,v1.0,v1}.md` @ tag `v1.0.0` | `grep -c -i "describes how a software build was executed"` | 0 for each |
| rendered `slsa.dev/spec/v1.0/provenance`, `/spec/v1.1/provenance`, `/spec/v0.2/provenance`, `/spec/v0.1/provenance`, `/provenance`, `/spec/v1.0/verifying-artifacts` | `grep -c -i "describes how a software build was executed"` | 0 for each |
| lane tree at C0 | `grep -rn "Provenance is a predicate that describes" .` | 1 hit — `corpus/lessons/round-56.md:21` only |

The sentence appears in the lane only in the lesson row that quotes it.

### Why this matters

`corpus/CORPUS.md` (fleet root) rule 1: *"The round lesson's `## Gate` records,
for every new row, the URL, the access date, and a ≤25-word quote with its
location grounding `teaches`."* The quote is the row's evidence. Here the
evidence for S282 is a sentence that is not in the cited document, so the row's
rejection reason is recorded against a passage that does not exist. The
**conclusion** is nonetheless correct — S282's `teaches` cell in `SOURCES.md`
is properly grounded in the real `§Model` paragraph ("a build platform produced
artifacts through execution of a buildDefinition"), and the `REJECTED:` reason
and `flip:` are correct — so this is an evidence defect, not a wrong verdict.

Two smaller details in the same cell, for the L1's adjudication:

* the word count is wrong: `printf '%s\n' "Provenance is a predicate that describes how a software build was executed." | wc -w` → **12**, not the "11 words" the table claims;
* the cell claims "reader extraction", but **no** SLSA extraction artifact is
  committed at C0 — `git ls-tree -r c013745… --name-only | grep -iE 'slsa|build-prov'`
  returns nothing. The only SLSA bytes in the tree are the untracked wave-1
  receipt above.

**Suggested repair (deferred to round 57 by the L1):** replace the quoted cell
with the true sentence, e.g. *"Provenance is an attestation that a particular
build platform produced a set of software artifacts…"* (11 words to `§Model`'s
first paragraph), or commit the SLSA extraction receipt under
`.ufo/evidence/round-56/assimilation/` and cite its sha256 as the S281 receipt
is cited.

---

## F2 — the knowledge entry's first S281 quote is a splice, not verbatim (minor)

**File:** `corpus/knowledge/receipt-revision-binding.md:7-10` — the file named by
S281's `used-by` cell.

The note opens:

> An attestation is about a subject it identifies by digest: "Set of software
> artifacts that the attestation applies to. Each element MUST have `digest` set",
> and "Subject artifacts are matched purely by digest, regardless of content type"

The first quoted string is not a contiguous substring of the source. The source
(`spec/v1/statement.md` @ `v1.2.0`, lines 36-37) reads:

```
> Set of software artifacts that the attestation applies to. Each element
> represents a single software artifact. Each element MUST have `digest` set.
```

The note drops *"represents a single software artifact."* and joins the two
remaining halves into one quoted sentence.

```
$ git show c013745…:.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md \
    | grep -c "Set of software artifacts that the attestation applies to. Each element MUST have"
0                                   # the note's quoted string is not in the source

$ git show c013745…:.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md | sed -n '36,37p'
> Set of software artifacts that the attestation applies to. Each element
> represents a single software artifact. Each element MUST have `digest` set.
```

The lane's own extraction receipt has the **full, correct** sentence:

```
$ git show c013745…:.ufo/evidence/round-56/assimilation/in-toto-statement-v1.extract.txt \
    | grep "Set of software artifacts"
  "Set of software artifacts that the attestation applies to. Each element represents a single software artifact. Each element MUST have `digest` set."
```

The second quote in the note ("Subject artifacts are matched purely by digest,
regardless of content type") **is** verbatim — it is the located quote at lines
54-55, and the note says so. The defect is only the first quotation mark pair.

**Severity:** minor, and mitigated by the note's own parenthetical *(S281
§Fields, `subject`; the second sentence is the located quote, lines 54-55)*,
which flags the second as the located quote. But it still presents a spliced
string in quotation marks as the source's words, and the lane treats exactly
this class as a named mistake (round-48 lesson: *"Line-pointer and byte-exact
wording errors"*). The repair is to paste the receipt's full sentence, or to
drop the quotation marks around the first string and paraphrase it.

---

## F3 — the knowledge entry's recheck line names a selftest count the tree no longer prints (minor)

**File:** `corpus/knowledge/receipt-revision-binding.md:3` (the `recheck:` header)
and `:155` (the §Re-derive failure criterion).

Line 3 states the recheck must print `GATE_SELFTEST: 14/14 pass`; line 155
makes a report of anything else a failure. At C0 the committed gate prints
**19/19**:

```
$ git show c013745…:tools/receipt-revision-gate.py > gate-c0.py
$ python3 gate-c0.py --selftest | tail -1
GATE_SELFTEST: 19/19 pass
note expects: GATE_SELFTEST: 14/14 pass
```

The note's own `verified-at:` header is honest that it was written at the
freeze, and at the freeze the gate really did print 14/14:

```
$ git show c3e2ca9f…:tools/receipt-revision-gate.py | sha256sum
1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2   # the sha the note pins
$ git show c013745…:tools/receipt-revision-gate.py | sha256sum
c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9   # the tree at C0
```

`git log c3e2ca9f..c013745 -- tools/receipt-revision-gate.py` shows the single
amendment commit `21eb3c6` ("…19-case suite") that took the suite from 14 to 19
cases. The knowledge note was committed at C0 **after** that amendment and was
not updated with it.

**Why it matters:** the note's `recheck:` line is the standing instruction for a
future reader to re-open this source. A reader who runs it at C0 sees `19/19`
against an expected `14/14`, and the §Re-derive criterion would declare the
source drifted when only the *lane's own gate* grew — the source-side half of
the same line (the `sha256sum` must print `cbe684a1…ebea`) still holds, which I
re-verified today (§ below). A recheck that mis-fires on its own lane's
amendment is the round-56 failure mode this round exists to prevent.

**Suggested repair:** update the count to `19/19` (and the §Re-derive comment
and criterion), or restate the criterion as "the suite passes and `codes-closed`
holds" rather than pinning a case count.

---

## Per-check results — the item's checks, one by one

### S281 — in-toto Statement v1, `https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md`

| check | result | evidence |
|---|---|---|
| `anchor` names a section that exists at that URL | **AGREE** | `## Fields` is present (line 24 of the fetched file); the `subject` field block is lines 34-56; the anchor's cited lines 36-37 and 54-55 are exactly those. Fetched body `sha256 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` = the anchor's `cbe684a1…ebea` |
| anchor's revision pin holds | **AGREE** | `git/ref/tags/v1.2.0` → `df02077bf97218a8860a5c534eff1f1381f56984` (anchor says `df02077b`); `main` HEAD → `50bf01716982189898823e90586075f37cd9bb7d` (anchor says `50bf0171`), and the bytes at `main` are identical to the tag (`cmp` clean, same sha256) |
| `teaches` grounded by the passage | **AGREE** | "an attestation applies to a subject identified by digest" ← lines 36-37 *"Set of software artifacts that the attestation applies to… Each element MUST have `digest` set"*; "subjects are matched purely by digest" ← lines 54-55 *"Subject artifacts are matched purely by digest, regardless of content type"* |
| lesson's S281 quote located | **AGREE** | `corpus/lessons/round-56.md:19` quotes *"Subject artifacts are matched purely by digest, regardless of content type."* — verbatim at lines 54-55 with `> ` stripped and the newline folded, as the extraction receipt documents |
| `tier`/`kind`/`scope` follow the contract's definitions | **AGREE** | `kind=spec` (enum), `tier=A` scoped to *"what an in-toto Statement v1 applies to: a subject identified by digest, not git receipt encoding and not DSSE verification"* — the spec is primary for its own shape (contract tier A); `community` n/a; `status=mined` and `used-by` cites ≥1 path, as the contract requires |
| `opened` is today's date | **AGREE** | `2026-10-28`; today is 2026-10-28 |
| `used-by` names the knowledge entry, which exists at C0 and cites the row | **AGREE** | `corpus/knowledge/receipt-revision-binding.md` exists at C0 (blob `38862d71…`); `grep -c 'S281'` → 2 (the `source:` header and the body) |
| URL is not a within-scope duplicate | **AGREE** | `grep -n "in-toto/attestation" corpus/SOURCES.md` → 1 hit (S281's own row); census validate reports no `E04` for it |
| *(extra)* the knowledge entry it points at | **DISAGREE** | F2, F3 above |

### S282 — SLSA Build Provenance, `https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md`

| check | result | evidence |
|---|---|---|
| `anchor` names a section that exists at that URL | **AGREE** | `## Model` present (line 40 of the fetched file); fetched blob `sha256 efece57ac1dd6e18c54a2b78e6ff18923a2590c3799c40c87b03572897ca76fc` = the anchor's `efece57a…76fc`; HTTP 200 |
| anchor's revision pin holds | **AGREE** | commits touching `spec/build-provenance.md`: `ba7d291a1521a8f3fc68db80990f2ba1562ccb12` 2026-10-19 (the anchor's "path last changed ba7d291a, 2026-10-19"), prior `bc8d1b82…` 2026-03-05 |
| `teaches` grounded by the passage | **AGREE** | the `§Model` first paragraph says *"a particular build platform produced a set of software artifacts through execution of the `buildDefinition`"* — the row's *"the predicate records that a build platform produced artifacts through execution of a buildDefinition"* is grounded |
| `REJECTED:`/`flip:` shape | **AGREE** | `teaches` reads `REJECTED: … ; flip: …` as the contract requires; `used-by=—` and `status=rejected` are consistent (no `W03`) |
| `tier`/`kind`/`scope` follow the contract's definitions | **AGREE** | `kind=spec`, `tier=A` scoped to *"SLSA's build-provenance predicate, not a statement-level subject binding"* — primary for its own predicate; tier-A rejected rows already exist in this registry (S067, S071, S080), so no new convention |
| `opened` is today's date | **AGREE** | `2026-10-28` |
| URL is not a within-scope duplicate | **AGREE** | `grep -n "slsa-framework" corpus/SOURCES.md` → 1 hit (S282's own row); no `E04` |
| *(extra)* the round's quoted passage for it | **DISAGREE** | **F1** — the lesson's quote is not in the source |

### Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
      --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
… (17 pre-existing warnings, all at base) …
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
exit=0
```

**exit 0.** No `E`-code, and no new warning: the `W04`/`W01` lines are identical
at base and at C0, and `S281`/`S282` appear in none of them.

**Rows: 142, not the 141 the brief expects.** This is a brief/tree mismatch, not
a lane defect — the round added **two** rows, and the lane's own tail note
says so (`corpus/SOURCES.md:521`: *"one row added for the sourced C2 claim, S281
… A second candidate (SLSA Build Provenance) was opened and added as the REFUSED
row S282"*):

```
base 981c5e8 rows: 140
C0   c013745 rows: 142
```

`140 + 2 = 142`. The census requirement (exit 0) holds; the parenthetical row
count in the assignment is off by one because it counted only the mined row.
The round's own `no-harm.sh` guard (`R >= 140`) is satisfied with margin.
`Next unused id: S283` in the tail note is correct — no `S283` row exists and
there are no duplicate ids.

## Residual risk and verification gaps

* **The S282 anchor is unpinned to a commit.** It cites `main` plus a blob
  sha256, and the row records the path's last-touch commit. That is adequate
  to detect drift on re-fetch, but not a commit pin like S281's `v1.2.0`/`df02077b`.
  I verified the blob sha256 and the last-touch commit both still hold today;
  a future reader who re-fetches `main` gets the same bytes only until `main`
  moves. Worth naming in the lesson.
* **Cross-lane overlap, not a duplicate.** `mori-shokunin` already holds the
  same upstream page in row `S060` (`https://slsa.dev/spec/v1.0/provenance`,
  whose cell also names the in-toto `statement.md`), with the same digest-binding
  teaching and explicitly *"no commit pin for in-toto main-branch files"*. The
  census `shared` mode does not report it because `url_of()` takes only the first
  URL in a cell and mori's cell starts with `slsa.dev/…`. S281 is not a
  within-lane duplicate and is not required to be, but the fleet already holds
  this ground in a weaker form — S281's commit-pinned `v1.2.0` anchor is the
  stronger artifact, and the round could have said so in the lesson.
* **The SLSA page is not the same document as SLSA Provenance v1.0.** The row's
  `main` blob carries a `Draft (v1.3)` change-history entry, so the row's
  "predicate type `slsa.dev/provenance/v1`" is the spec's stated current major
  version while the file also tracks an unreleased draft. Not false, but the
  row's scope cell does not say which minor it read.
* **I did not re-open every URL in the registry** — the item scopes me to the
  row(s) this round added, and I swept those rows' URLs exhaustively (including
  every upstream revision I could enumerate) rather than spot-checking the
  other 141 rows.
* **Untracked wave-1 bytes.** `.ufo/waves/round-56/` is untracked at C0
  (`git status --porcelain` → `?? .ufo/waves/round-56/`). The wave-1
  extraction receipt I cite in F1 lives there and is therefore not part of the
  committed tree; the same receipt's *content* is reproduced by the committed
  `.ufo/evidence/round-56/assimilation/` snapshot for S281, but no SLSA
  equivalent is committed.
* **No tool installs were needed.** No `pacman`/`uv`/`npm` action was taken;
  `curl`, `git`, `gawk`, `python3` and `jq`-free shell were sufficient. Nothing
  to record on the tooling-authorization channel.

## Commands run (all receipts under `.ufo/waves/round-56/w2/T56W2RevSources-receipts/`)

| receipt | content |
|---|---|
| `01-lesson-s282-quote-vs-source.txt` | F1: the lesson cell, the failed grep, the true `§Model` paragraph |
| `02-knowledge-quote-fidelity.txt` | F2: the note's splice vs source lines 36-37 and the extraction receipt |
| `03-recheck-line-stale.txt` | F3: the `recheck:` line, the `14/14` criterion, `19/19` at C0, both gate shas |
| `04-census.txt` | census at the C0 clone (`census` + `validate`, exit 0) |
| `05-s281-anchor-reopen.txt` | S281 raw fetch, sha256, HTTP 200, headings, lines 34-37/54-56, tag→commit, main HEAD, byte-identity |
| `06-s282-anchor-reopen.txt` | S282 raw fetch, sha256, `§Model` + first paragraph, last-touch commits, HTTP 200 |
| `07-row-delta-and-dup.txt` | base vs C0 row counts, the round's tail note, within-lane duplicate greps, cross-lane check |

Fixture discipline: a `git clone --shared` clone at
`/fast/scratch/hyaku/tameshi-r56/T56W2RevSources/clone` was checked out
`--detach c013745…` and `git rev-parse --show-toplevel` was asserted to equal
that directory before use. No mutating git command was run anywhere. No lane
production file and no frozen instrument under `.ufo/evidence/round-56/` was
edited.
