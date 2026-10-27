# T53W1Read22 — cold read of `### The re-pin semantics, as executed`

- Candidate (content commit C\*): `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Section extent at C\*: **lines 1232–1247**; heading at 1232, next heading at 1248 (`### The service's limits — what tameshi refuses to mutation-test`). Body after stripping the trailing whitespace-only line (1247): **15 lines, 917 bytes, no trailing newline**.
- `section_sha256` = `0767d32fa85ab5591b3c170d27be7cb69a40e04be5859c52a992fa88a7bf73f5` (reproduced twice, by two independent splits — see checks 2 and 3).
- Reads were taken from git objects only (`git -C .../tameshi-shokunin show C*:<path>`); the working tree was never consulted. Read-only; no repo state changed. Scratch used: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read22/` (deleted before yield).

## Checks run (all commands executed, output read)

1. `git cat-file -p C*:SKILL.md | grep -n '^### The re-pin semantics, as executed'` → `1232` (single occurrence; heading is unique in the file).
2. Fence-aware split (`^#{1,3}(\s|$)`, headings outside ``` fences) over `git cat-file -p C*:SKILL.md` → heading index 31, range **1232–1247**, next heading `(1248, "### The service's limits — what tameshi refuses to mutation-test")`, body 15 lines / 917 bytes, sha256 `0767d32f…73f5`.
3. Independent re-slice: 1-based lines 1232–1247 of the same blob, trailing whitespace-only lines popped, `\n`-joined, sha256 over UTF-8/surrogateescape → same `0767d32f…73f5`, same 917 bytes; line 1248 confirmed to be the next heading. Extent verified before hashing.
4. Round-8 section located by line: `awk 'NR>=1060 && NR<=1096'` over `C*:SKILL.md` → `### Triggers T1–T3 and the re-pin rule` at **1071**, next heading `### Six-case confidence statement (round 8, measured)` at **1094**; the preceding section `### The tick and the pin read` (heading at 1023) therefore ends at **1069**.
5. `corpus/knowledge/service-optin-protocol.md` at C\* → the quoted sentence is at **lines 61–62**, inside the cited `:59-62`; §8 Errata (lines 276–286, E1/E2) does not touch item 1, so "present, not errata" survives.
6. `corpus/knowledge/fleet-kill-rate-ledger.md` at C\* (441 lines) → `## Errata (append-only)` at 239; ER-4 at 318 (tick receipt, pin read 324–333, `[U]` re-sweep at 339, "land as their own rows" at 352); ER-4 addendum at 356 with `stale + drift` readings at 358–359; ER-3's outcome clause at 312; U9 at 235–237; successor debt at 398.

## Holds

- **"T1 fired for two cases."** T1 (`C*:SKILL.md:1073-1076`) names the two live instances, tsukuroi and mado; ER-4's pin read (`fleet-kill-rate-ledger.md:328-329, 333`) reads exactly `stale=2, drift=0`.
- **The re-pin rule content itself** is at `C*:SKILL.md:1073-1076` and is a faithful summary (the only difference is punctuation — the source reads `…its reason; **never an edit…**`, the section reads `…its reason — never an edit…`; not in quotation marks, so a paraphrase, not a misquote).
- **Intake precondition quoted from the protocol.** `corpus/knowledge/service-optin-protocol.md:59-62` reads "…A moved substrate needs a / re-pin, never a re-interpretation of the old table." — the section's quotation is the line-joined bytes; `:59-62` does bound it.
- **"ER-4 and its addendum name the re-sweeps of the two moved cases as follow-on rows — open at this write".** ER-4 `:339` keeps the moved revisions `[U]` and calls the re-sweep "this round's re-sweep work (its own appended rows)"; `:352` says "the re-sweeps of the two `stale` cases land as their own rows". Still open at C\*: no later block lands them (`:398` "successor sweep joins the existing tsukuroi/mado successor debt"; the round-16/18/52 blocks append new cases, never those two sweeps).
- **"the addendum reads them `stale + drift`".** Verbatim at `:358` and `:359`.
- **"the recorded tables byte-identical".** ER-4 `:318` "No §1–§4 cell is edited", `:352` "no rate is re-cut"; the file's own practice is supersession-outside-the-table (`:439`, round 52).
- **(append-only)** — `:239` section header, and the append-only convention restated at `:405`, `:426`, `:439`.
- **"a rate never travels to a later revision".** ER-3 `:312` "a rate never travels (per-revision, per-host; §0)".
- **"an unlanded leg is named debt, never assumed".** Practised at `:398` ("existing tsukuroi/mado successor debt").
- **Scratch directive:** the section names no scratch path, no `/tmp`, no `/fast/scratch` — nothing to fail here.

## Findings

### F1 — stale pointer: the round-8 section is not `:1069-1090`

> The rule is the round-8 section's (`:1069-1090`)

At C\* the round-8 re-pin section is `### Triggers T1–T3 and the re-pin rule`, spanning **1071–1092** (next heading at 1094). The cited range is wrong at both ends, by two lines:

- `1069` is the **last line of the preceding section** `### The tick and the pin read` — mid-bullet text: `  porcelain lines after); an untouched case reads `current`.` So the range opens inside a different section's falsifiers bullet.
- `1090` cuts the section's closing receipt **mid-sentence**: `  \`REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0` — it drops `flips<=0)`, the `every leg match=10/10 … flips=0` clause, and the concluding claim "the recorded tables hold at their own pinned blobs regardless of the live drift above."

A reader following the pointer lands half in the previous section and leaves the re-pin rule's own receipt truncated; a reader checking the range against the heading sees it is not the named section at all. The rule text a reader needs is at `:1073-1076`; the section is `:1071-1092`.

### F2 — narrowed source: the outcome is a row **or an errata block**, not "an appended row"

> The outcome is an appended row in

(the quoted line continues on the next source line: `` `fleet-kill-rate-ledger.md` (append-only), the recorded tables byte-identical; ``)

The ledger this sentence cites keeps a disjunction that the section closes:

- U9 (`fleet-kill-rate-ledger.md:235-237`): "a new sweep appends a row **(or an errata block)**";
- ER-3 (`:312`, the cadence policy the section's rule rests on): "the outcome lands **as an appended row or errata block in this ledger** — never as an edit of §1–§4".

The errata-block branch is not hypothetical: ER-1…ER-4 are errata blocks, and the appended round-16 / round-18 / round-52 outcomes are appended *sections*, not table rows. Stated as "an appended row", the section misdescribes the mechanism it points at — a lane that lands a re-sweep as an errata block would read itself as non-compliant with the section, and a reader would miss the form most of this ledger's outcomes actually take.

## Non-findings considered and rejected

- **`(`:1069-1090`)` as a deliberate widening to include the drift falsifiers.** Rejected as a charitable reading: the sentence says "the round-8 section's", and the range starts mid-sentence in a differently-titled section and ends mid-receipt; no reading makes 1069 a section start.
- **T1 paraphrase punctuation (`—` vs `;`).** Paraphrase, unquoted; content identical. Not a finding.
- **"open at this write" after 15 later rounds of errata.** Checked against the whole ledger as of C\*: no later block lands the two re-sweeps (`:398` still calls them debt). Holds.
- **"The intake precondition round 8 named is present, not errata."** Checked the protocol's own errata (§8, `:276-286`); neither E1 nor E2 touches §1 item 1. Holds.

## Files

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w1/T53W1Read22.json`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w1/T53W1Read22.md`
