# T47RevC3Predicate — C3 claim vs predicate vs label

Round 47, wave 1, seat T47RevC3Predicate. Read-only on the lane except this file.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`,
freeze `9acfbe21435e1976636a276448dee1d5e7155915`. Scratch: `/tmp/tameshi-r47-T47RevC3Predicate/`.
No verdict is emitted: every counter call below is a probe or a `--selftest`, never a deciding run.
No tool was installed or upgraded (nothing was needed).

## 1. Side by side

**A. Contract `claims.C3.statement`, verbatim** (`.ufo/evidence/round-47/contract.json`):

> Three registry rows for the frozen documents (arxiv.org/abs/2302.09330; arxiv.org/abs/2607.09345;
> the api.semanticscholar.org graph record of DOI 10.1109/ICST60714.2024.00037 with the
> %2C-encoded fields query), opened this round with committed snapshots in
> .ufo/evidence/round-47/coverage/sources/ and 8-hex sha256 prefixes in their anchors, adopted at
> guard-admitted ids, are each cited by a re-grounded knowledge entry (verified-at >= 2026-10-25,
> listed in the row's used-by, carrying a located 6-25-token quote and at least one located quote
> absent from the package copy of the same entry), and every such entry is indexed in
> corpus/README.md.

**B. Contract `claims.C3.target`, verbatim:**

> C3_R47_PASS=true: self_pin=1 rows>=3 entries>=3 indexed==entries covered==rows

**C. Counter docstring predicate, verbatim** (`coverage/measure.py:4-27`, introduced as
"the same sentence in the contract, here and in the receipt label"):

> C3_R47_PASS=true iff self_pin=1 and rows >= 3 and entries >= 3 and indexed == entries
> and covered == rows, where
> * rows = census-valid registry rows at REV (0-3 leading spaces, 13 cells) with status `mined`
>   whose source cell's first URL is one of the three frozen documents (... the Semantic Scholar
>   graph record of DOI 10.1109/ICST60714.2024.00037 with the %2C-encoded fields query; compared
>   without scheme, `www.`, trailing slash or case), whose anchor cell names a snapshot path under
>   .ufo/evidence/round-47/coverage/sources/ that is present at REV together with an 8+-hex sha256
>   prefix of that snapshot's bytes;
> * entries = corpus/knowledge/*.md files at REV whose line 1 is `source:` citing at least one such
>   row id, line 2 `verified-at:` with an ISO date >= 2026-10-25, line 3 `recheck:`, that are listed
>   in a cited row's used-by cell, and that carry at least one double-quoted quote of 6..25
>   whitespace tokens found in the folded text of a cited row's snapshot AND, when the committed
>   package copy exists, at least one such located quote that does not occur in that package copy;
> * indexed = entries whose repo path appears backticked in corpus/README.md at REV;
> * covered = rows cited on line 1 of at least one admitted entry.

**D. The `C3_R47_PASS` label**, verbatim (`coverage/measure.py:177`):

> `C3_R47: self_pin=%d rows=%d entries=%d indexed=%d covered=%d row_ids=%s rev=%s C3_R47_PASS=%s`

Live instance at the freeze (probe, §4): `C3_R47: self_pin=1 rows=0 entries=0 indexed=0
covered=0 row_ids=- rev=9acfbe21435e1976636a276448dee1d5e7155915 C3_R47_PASS=false`.

## 2. Is it the same statement?

**Target = code predicate = label: yes.** `measure():175-179` evaluates exactly
`self_pin==1 and len(rows)>=MIN_ROWS(3) and len(entries)>=MIN_ENTRIES(3) and len(indexed)==len(entries)
and len(covered)==len(rows)`; the label prints those five names and the verdict token; the target
carries the same five names with the same thresholds. `indexed` and `covered` are constructed as
subsets (`indexed` ⊆ `entries`, `covered` ⊆ `rows`), so the equality is a sound spelling of the
universal ("every entry indexed", "every row covered"). The `--selftest` exercises all five legs
(T17 entries=2 → false; T18 rows=2 → false; T19 unindexed → false; T20 self_pin=0 → false;
T23/T24 coverage mismatch → false), 24 cases, 0 failed (§6).

**Statement ≠ code predicate, in both directions.** The statement is *narrower* than the code on
five operational points and *wider* on one clause the code does not measure at all:

| # | element | contract `statement` | code predicate | drift | severity |
|---|---|---|---|---|---|
| 1 | row identity | "Three registry rows for the frozen documents" | status must be `mined`, exactly 13 cells, 0-3-space indent, **first** URL in the source cell, snapshot present under the round-47 sources prefix, 8+-hex prefix of its bytes | predicate ⊃ statement; `mined` is CORPUS-entailed by "listed in used-by", 13 cells/indent are the census schema, but the **first-URL rule** is stated only in the docstring | medium (see F2) |
| 2 | adoption ids | "adopted at **guard-admitted ids**" | any `S\d{3,}`; id never read | predicate ⊄ statement — the clause is dropped and **unmeasured** | high (F1) |
| 3 | rows count | "Three registry rows" | `rows >= 3`, uncapped; two rows for one document count twice | universal "Three" not enforced | low (F5) |
| 4 | entry count | "are each cited by a re-grounded knowledge entry" (one entry may satisfy all three) | `entries >= 3` — three **distinct** admitted entries | stricter than the statement | low (F4) |
| 5 | entry provenance | "(verified-at >= 2026-10-25, listed in the row's used-by, carrying a located 6-25-token quote and at least one located quote absent from the package copy)" | additionally line-1 `source:`, line-2 `verified-at:`, line-3 `recheck:`; quote located in a **cited** row's folded snapshot | line order + `recheck:` come from CORPUS.md ("opens with …"), so grounded, but not in the contract sentence | low |
| 6 | indexed form | "indexed in corpus/README.md" | backticked `corpus/knowledge/x.md` **or** `knowledge/x.md` | form not stated; matches the lane's README convention | low |
| 7 | self-pin | absent | `self_pin == 1` | target/label carry it, statement does not | info |

Consequence for the milestone: **C3 target = predicate = label holds**; **C3 statement = predicate
does not**. The docstring's claim to be "the same sentence in the contract" is inaccurate — the
sentence it matches is `target`, not `statement` (F3).

## 3. Universal words

`each` (rows) and `every such entry` are the only universals in the statement.

- "are each cited by …" — the full set is the three frozen documents, enumerated by `DOCS`
  (`measure.py:42-46`) and by the `surface` field ("0 rows and 0 entries citing …"). `covered==rows`
  enumerates it. **Sound.**
- "every such entry is indexed" — "such" bounds the set to admitted entries; `entries` is
  enumerated by `tree.ls('corpus/knowledge/')` + `entry_ok`, and `indexed` is a subset of it, so
  `indexed==entries` enumerates the full set. **Sound.**
- Not a universal, but an unbounded existential: "adopted at guard-admitted ids" — no counting
  command enumerates it (§9 rule 2 is met only for the two universals, not for this clause). F1.
- The `surface` field's negative ("0 rows and 0 entries … at base") carries its command
  (`unmoved_command`), and I re-ran it: §4. **Sound.**

## 4. Surface unmoved at the freeze / at base (probe)

```
python3 .ufo/evidence/round-47/coverage/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9acfbe21435e1976636a276448dee1d5e7155915
C3_R47: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=9acfbe… C3_R47_PASS=false   (exit 1)
```
Byte-for-byte identical (1745 bytes, `out.stdout == receipt` in Python) to the committed
`.ufo/evidence/round-47/before/c3-at-freeze.stdout`, i.e. the surface is unmoved **and** the
before-receipt is reproducible from the freeze. The only stdout besides the verdict is 23
`REFUSED … no provenance trio` lines (see F7).

```
… --rev 0b5b7cd2b2c15d23086e811a0f0348d84261277b
C3_R47: self_pin=0 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=0b5b7cd… C3_R47_PASS=false   (exit 1)
```
At base `self_pin=0` because the counter does not exist at `0b5b7cd` (expected, not a failure);
`rows=0 entries=0` is the claim's "unmoved" state. `corpus/knowledge/` already holds 55 files at
the freeze (28 with a three-line provenance trio), none of which cites one of the three documents —
`grep -rl '2302.09330|2607.09345|ICST60714' corpus/` → nothing.

## 5. Are the three documents frozen in `DOCS` and in the contract?

**In `DOCS`** (`measure.py:42-46`), exact tuple:

```
arxiv.org/abs/2302.09330
arxiv.org/abs/2607.09345
api.semanticscholar.org/graph/v1/paper/doi:10.1109/icst60714.2024.00037?fields=title%2cabstract%2cyear%2cvenue%2cauthors%2cexternalids
```
`self_pin` pins the whole file, so `DOCS` is frozen at REV. The third key is fully `%2c`-encoded —
required, because `URL_RE = https?://[^\s;,)]+` (`:48`) stops at a literal comma. Probed:

| row URL form | `URL_RE` capture | matches `DOCS[2]` |
|---|---|---|
| literal commas (the package row S207's own form, `SOURCES.append.md:61`) | `…/doi:10.1109/icst60714.2024.00037?fields=title` | **no** |
| `%2C`-encoded six fields | full string | **yes** |
| `%2C`-encoded, reordered / subset / one extra field | full string | **no** (three variants, all false) |

**In the contract:** by document, yes — the two arXiv URLs are exact; the Semantic Scholar record is
identified by DOI plus "with the %2C-encoded fields query" but **not** by the exact query string
that `DOCS[2]` requires (F2). Snapshots and package copies are named but not digest-pinned (F6).

End-to-end fixture probe (scratch `git init` repo at `/tmp/tameshi-r47-T47RevC3Predicate/fixture1`,
real snapshot bytes, 11-column rows, counter invoked with `--lane D --rev HEAD`):

| fixture | row form | verdict line |
|---|---|---|
| m1 | both arXiv rows + `%2C` S2 row, first URL = the record | `rows=3 row_ids=S261,S263,S264` |
| m2 | same, S2 URL with literal commas (package form) | `rows=2 row_ids=S261,S263` |
| m3 | S2 row whose first URL is `https://doi.org/…`, record second | `rows=2 row_ids=S261,S263` |
| m4 | ids `S206`,`S207`,`S999` | `rows=3 row_ids=S206,S207,S999` |
| m5 | second row for a document already counted (`S265` = same URL as `S261`) | `rows=4 row_ids=S261,S263,S264,S265` |
| m6 | one entry citing all three rows (`entries=1 covered=3`) | `C3_R47_PASS=false` |

## 6. AXES coverage, CORPUS rule 4, prompt §9

- **AXES coverage** (`/home/vgpnk/Projects/shokunin/AXES.md:12`): "Fraction of the domain's real
  surfaces the skill governs … PROVINCE.md lists every surface". `PROVINCE.md:40` delegates the
  frontier surfaces: "**Frontier** — F1–F10 in `corpus/README.md` `## Frontier`", and
  `corpus/README.md:80` lists **F3 | determinism precondition, flaky-aware verdicts | S004, S011,
  S025, S026, S027, S040 | open**. The claim's `surface`/`type` name F3 and its "measurement half"
  in those words, and F3 stays `open` (same posture as the round-45/46 appends at
  `corpus/README.md:565,577`). Named surface ✓, not a rename of a number.
- **CORPUS rule 4** ("Expansion is knowledge, not rows … There is no row quota"): consistent in the
  part that matters — rows alone cannot pass (CTL_C rows=3 entries=0 → false; m1 rows=3 entries=0 →
  false), and the uncounted Lam row earns nothing. The target's `rows>=3` reads as a row floor, but
  it is the citation precondition: `covered==rows` couples every counted row to an admitted entry,
  and the fourth row is explicitly excluded from counting, so extra rows buy nothing.
- **Prompt §9** (`/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-47.md:417-432`):
  - one command over committed bytes: ✓ `counting_command` (`--lane --rev`), label prints counts;
  - no universal without full enumeration: ✓ for the two universals (§3);
  - judgement on the frozen counter/kill rule/predicate: ✓ (`amendments: []`; contract.json and
    measure.py in the worktree are byte-identical to `9acfbe`, sha256
    `3a88c2fc…346e1` and `c8fb89e6…94260` respectively);
  - the "same sentence in plan, code and label": ✗ across `statement`↔code (F3);
  - "a coverage claim names the surface it moves … and the command that would show it unmoved":
    surface ✓; `unmoved_command` is prose ("the same counter: rows=0 entries=0 shows the surface
    unmoved"), not a pasteable command (F8).
- **Do-nothing controls** (`.ufo/evidence/round-47/control/controls-at-freeze.stdout`): CTL_A
  package byte-exact → `rows=3 entries=0`; CTL_B relabel → `entries=0`; CTL_C rows only →
  `entries=0`; CTL_D wrong digest → `rows=0`. All false at freeze ✓ (a package copy cannot pass).
- **Package copies**: the three lane copies are byte-identical to
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/` (`3a962fe5…`,
  `4fab9714…`, `9f778247…`), and byte-identical between freeze and worktree.

## 7. Findings

### F1 — HIGH: "guard-admitted ids" is in the claim, absent from the predicate, and the dispatched ids contradict the only committed admitted map

- The statement's clause "adopted at guard-admitted ids" has no representation in `target`, in the
  docstring, or in the code: `flaky_rows` accepts any `S\d{3,}` (`measure.py:43,103-118`). Fixture
  m4 counts `S206,S207,S999` as three rows. The label already prints `row_ids=…`, so the ids are
  visible but never asserted.
- The committed guard artifacts disagree with the dispatched ids. The only admitted map committed at
  the freeze is `.ufo/evidence/round-46/assimilation/adoption-map.json`:
  `{"S153":"S105","S154":"S106","S159":"S155","S160":"S156","S155":"S261","S156":"S262","S157":"S263","S158":"S264","S195":"S258","S190":"S259","S216":"S260"}`.
  With staged documents `SOURCES.append.md:9-12` (S155 = arXiv 2302.09330, S156 = arXiv 2406.09843,
  S157 = JOSS Hypothesis, S158 = Lam camera-ready), that map reserves **S264 for the Lam document**
  and S262/S263 for two documents not adopted this round.
- `corpus/SOURCES.md:471` and `:474` state the same reservation in the registry itself ("moves
  staged S155–S158 to S261–S264 in the map only, so those four ids are reserved by the map and
  unused in the registry"; "Next unused id: S265 (S261–S264 are map-only reserved)").
- The round-47 dispatch (`.ufo/waves/round-47/spec-w1.json` row-scribe item) and the brief assign
  S261/2302.09330, **S262/Lam**, **S263/2607.09345**, **S264/S2 record** — S262–S264 reassigned away
  from their reservations. The id-guard seat has already recorded this exact conflict
  (`w1/T47ExecIdGuard.receipts.md` §5) and also recorded that the four-entry contract map alone is
  **refused** by the lane's guard (`verdict="inadmissible"`, `map_uncovered=S153,S154,S156,S157,S159,S160`,
  exit 1); only a 10-entry map (`S156→S265`, `S157→S266` map-only) is admitted (§6b).
- Net: the claim's "guard-admitted ids" is satisfied by nothing committed at the freeze, the
  predicate cannot see it, and the registry prose would name two documents for S262–S264 unless
  lines 471/474 are superseded in this round's registry note. Not mine to decide; the counter is
  frozen and must not be edited after the freeze.

*Recommendation for the L1 record:* land the 10-entry admissible map as the round's adoption map,
append the supersession note for `SOURCES.md:471,474`, and state in the report that the id clause
is frozen-unmeasured (row counts unaffected). For a future round, pin the ids in the predicate — the
label already prints `row_ids`, so an exact `row_ids==S261,S263,S264` leg costs one line.

### F2 — MEDIUM: `DOCS[2]`'s exact query string is not in the contract, and two plausible row forms silently drop the row

- `DOCS[2]` requires exactly `?fields=title%2cabstract%2cyear%2cvenue%2cauthors%2cexternalids`.
  The contract says only "the … graph record of DOI … with the %2C-encoded fields query". Three
  equally valid encodings (reordered, subset, extra field) fail; probed all false.
- Copying the package row verbatim fails: `SOURCES.append.md:61` writes literal commas, `URL_RE`
  truncates at the first comma, fixture m2 → `rows=2`. The contract and the dispatch item do warn
  about `%2C`, so an informed seat survives; an uninformed one sees `rows=2` and cannot tell which
  row was dropped (no per-row diagnostic).
- Placing the DOI URL first in the source cell also drops the row (fixture m3 → `rows=2`); the
  first-URL rule exists only in the docstring (`:104-108`), not in the contract sentence.

*Recommendation:* add a one-line `REFUSED <id> <reason>` diagnostic per near-miss row (the entry
path already has one), and carry the exact `DOCS` tuple in the round's evidence note. Predicate
change is not available this round (frozen).

### F3 — LOW: the docstring's "the same sentence in the contract" is false for `statement`

`measure.py:4` claims sameness with the contract; the contract's `statement` is a prose sentence that
(a) carries "guard-admitted ids" the code ignores, (b) omits `mined`/13-cell/first-URL/line-order/
`recheck:`/`entries>=3`, and (c) does not mention `self_pin`. The `target` and the printed label do
match the code. Milestone reading: **claim (target) = predicate = label ✓; statement = predicate ✗**.

### F4 — LOW: `entries>=3` (distinct) is stricter than the statement

Fixture m6: one entry that cites S261, S263 and S264 satisfies the statement's "each cited by a
re-grounded knowledge entry" (`covered=3=rows`) but yields `entries=1` → `C3_R47_PASS=false`. The
intent is clear from `entry_basenames` (three files), and T17 shows the counter is deliberate; the
gap is statement wording only. A seat that writes one omnibus entry would produce an honest miss.

### F5 — LOW: `rows` is a floor, not "three"

Fixture m5: a second row for an already-counted document (`S265`, same URL as `S261`) raises the
rendered `rows` to 4; the target `rows>=3` and `covered==rows` still accept it (with the extra row
cited). The statement's "Three registry rows" is not enforced; a duplicate document row is caught
only by the CORPUS census duplicate-URL check (`sources-census.sh validate`, exit 0 required before
append), not by this counter.

### F6 — MEDIUM: no digest pin on the C3 inputs, unlike C1 and C2

C1 carries `statements_sha256` and C2 `pool_sha256`; C3 carries no sha256 field at all. The counter
verifies the row's anchor prefix against **whatever bytes sit at REV**, so replacing a snapshot and
updating the row's prefix still counts (the package-copy freshness leg only compares the entry to the
package copy, not the snapshot to the freeze). Today the bytes are intact — all five round-47
snapshots and the three package copies are byte-identical between `9acfbe` and the worktree
(`2965343c…`, `16ecdefc…`, `6ab5b3f5…`, `0b880458…`, `bf52c908…`) — but nothing in the predicate
keeps it so. A reviewer must diff the sources directory against the freeze commit by hand.

### F7 — LOW (diagnostics): 23 `REFUSED … no provenance trio` lines are noise

`entry_ok` checks the trio before it checks the citation, so every pre-existing entry without a trio
is printed even though it cites none of the flaky rows. The freeze receipt shows the same 23 lines,
so the receipt is reproducible, but the noise hides the one line a seat would need if it added a
malformed entry.

### F8 — LOW: `unmoved_command` is prose

`claims.C3.unmoved_command` is "the same counter: rows=0 entries=0 shows the surface unmoved", not a
command (§9 asks for "the command that would show it unmoved"). `counting_command` covers the need;
the field reads as a note.

### Non-findings verified (no defect)

- `--selftest`: 24 cases, `failed=0`, `VERDICT: PASS`, exit 0. All five target legs exercised
  (T17–T20, T23–T24); package-relabel refusal exercised (T21) and fresh-quote acceptance (T22).
- Freeze integrity: `contract.json` and `coverage/measure.py` worktree sha256 equal their blobs at
  `9acfbe`; `amendments: []`.
- Entry gates match the lane conventions: `source:`/`verified-at:`/`recheck:` at lines 1-3 (CORPUS
  "opens with"); used-by must be the bare repo path `corpus/knowledge/<name>.md` (my m6 fixture
  matched with bare paths); README index accepts `` `knowledge/x.md` `` (the lane's own table style,
  `corpus/README.md:7-15`) or the full path (T16).
- Snapshot ↔ document: the S2 JSON carries `externalIds.DOI = 10.1109/ICST60714.2024.00037`, the
  requested fields (`title, venue, year, authors, abstract`) and no `\uXXXX`/escaped quotes, so a
  quote taken from the decoded abstract also locates in the counter's folded raw text (checked at 8,
  12 and 20 tokens and mid-abstract). arXiv titles match the staged documents.
- `extra_row` (Lam PDF) is correctly outside the counted set; its row cannot disturb
  `covered==rows`.

## 8. Residual risk

- A snapshot swapped after the freeze is invisible to the predicate (F6); only an out-of-band diff
  finds it. The deciding run's receipt should be accompanied by a sources-vs-freeze digest table.
- The `%2C`/first-URL traps are silent (F2): a seat that loses a row sees `rows=2` and no reason.
- Ids: the pass condition cannot distinguish the contract's ids from any other ids (F1); the
  registry note is the only place the by-document mapping is checked, and it currently disagrees.

## 9. Verification gaps

- I did not run the deciding measure over the post-landing tree (it does not exist yet); every
  verdict above is a freeze/base probe.
- Network reads were not repeated: snapshot authenticity rests on the content checks in §7
  (titles, DOI, abstract) plus the freeze digests, not on a fresh fetch (read-only package, no
  campaign tools).
- The used-by backtick failure mode is code-derived (`measure.py:118`) and not fixture-exercised;
  the bare-path success is fixture-exercised (m6).

## 10. Commands run (scratch root `/tmp/tameshi-r47-T47RevC3Predicate/`)

| # | command | exit |
|---|---|---|
| 1 | `measure.py --lane <lane> --rev 9acfbe…` | 1 (`rows=0 entries=0 self_pin=1`; stdout identical to `before/c3-at-freeze.stdout`) |
| 2 | `measure.py --lane <lane> --rev 0b5b7cd…` | 1 (`rows=0 entries=0 self_pin=0`) |
| 3 | `measure.py --selftest` | 0 (`cases=24 failed=0`, `VERDICT: PASS`) |
| 4 | fixture m1–m6 (`git init` in `/tmp/…/fixture1`, `-C` on every call, toplevel checked; counter `--lane D --rev HEAD`) | 1 each (expected `PASS=false`) |
| 5 | python probe of `URL_RE`/`doc_key` over literal/`%2C`/variant URLs and arXiv variants | 0 |
| 6 | `git show 9acfbe:<file> \| sha256sum` vs worktree for contract, counter, 5 snapshots, 3 package copies | 0 (8 SAME) |
| 7 | `sha256sum` package copies vs `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/` | 0 (3 SAME) |

Read-only reads: `contract.json`, `coverage/measure.py` (all 335 lines), `before/c3-at-freeze.stdout`,
`control/controls-at-freeze.stdout`, `corpus/SOURCES.md` (rows + round-46/47 notes), `corpus/README.md`
(Frontier table, index style), `PROVINCE.md`, `tools`-free checks of `adoption-map.json` /
`guard-map.json`, `w1/T47ExecIdGuard.receipts.md`, `w1/spec-w1.json`, `CORPUS.md`, `AXES.md`,
`.ufo/prompts/tameshi-round-47.md` §9/§10.
