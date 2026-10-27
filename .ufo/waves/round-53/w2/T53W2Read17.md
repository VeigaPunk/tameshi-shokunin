# T53W2Read17 — wave-2 re-read of `### The re-pin semantics, as executed`

- Candidate (content commit C\*\*): `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`
- Section extent at C\*\*: **lines 1237–1256** (19 lines); heading at 1237, next heading at 1257 (`### The service's limits — what tameshi refuses to mutation-test`). Trailing whitespace-only line stripped → **1101 body bytes, no trailing newline**.
- `section_sha256` = `c07692a2affebbc485651730a559a125010f091eb613b5317a3728851d9c2b24` (reproduced twice by two independent splits, checks 1–2; extent verified before hashing).
- Source: git objects only — `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C**:SKILL.md` (and `C**:corpus/knowledge/…`). The working tree was never read for any claim in this report.
- Wave-1 reader whose findings the L1 fixed: `.ufo/waves/round-53/w1/T53W1Read22.json` (F1 stale pointer, F2 narrowed source).

## Checks run (fix verification FIRST)

1. **Split at C\*\*** with the frozen monitor's own splitter — the packaged `sectionize()` of `.ufo/evidence/round-18/measure.py`, loaded and called on the C\*\* `SKILL.md` blob: one section whose heading is `### The re-pin semantics, as executed`, `start=1237`, `end=1256`, `sha256=c07692a2…1d9c2b24`; previous section `### The receipt at this boundary` (1219–1236), next heading at 1257. Fence-aware `^#{1,3}(\s|$)` scan, trailing whitespace-only lines popped, `\n`-join, sha256 over UTF-8/`surrogateescape`.
2. **Independent re-slice** (own fence-aware scan, not the module): heading occurrence at 1-based line 1237 only; block lines 1237–1256 → 19 lines, 1101 bytes, same `c07692a2…1d9c2b24`; next heading confirmed `### The service's limits — what tameshi refuses to mutation-test`. Extent checked before hashing.
3. **Fix F1 (stale pointer → heading name).** `grep -n "^### Triggers" SKILL.md` → single occurrence at **1075**; the pointer's inner text compared byte-for-byte to that heading line → **identical** (`### Triggers T1–T3 and the re-pin rule`, en dashes `\xe2\x80\x93` in both). The line inside the section, `  (`### Triggers T1–T3 and the re-pin rule`):`, does **not** register as a heading (line starts with spaces; the sectionizer and a manual `^#{1,3}(\s|$)` scan both agree — no phantom section created). The referenced section is under the round-8 boundary heading `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` (1015), so "the round-8 section's" is the correct parent; the rule text a reader lands on is `SKILL.md:1077-1078` (T1) and `:1089-1096` (the re-pin rule paragraph).
4. **Fix F2 (outcome = row or errata block).** The C\*\* bytes now read:

   > - **What a re-sweep produces lands appended.** The outcome lands as an appended
   >   row or errata block in
   >   `fleet-kill-rate-ledger.md` (append-only, per U9 and ER-3 — the errata-block
   >   branch is not hypothetical: ER-1…ER-4 and the round-16/18/52 appends take that
   >   form), the recorded tables byte-identical;

   Checked against the ledger at C\*\*: U9 at **:235-237** (line-joined) — "a new sweep appends a row (or an errata block)"; ER-3 at **:312** — "the outcome lands **as an appended row or errata block in this ledger** — never as an edit of §1–§4"; ER-1/ER-2/ER-3/ER-4 labels at **:244 / :272 / :285 / :318**, all inside `## Errata (append-only)` (**:239**); appended blocks `## Round 16 — seventh row appended` (**:403**), `## Round 18 — eighth row appended` (**:424**), `## Round 52 — §3 drift-pins cell superseded` (**:439**) — each appends, none edits §§1–§4.
5. **Protocol quote and anchor** (`corpus/knowledge/service-optin-protocol.md:59-62` at C\*\*): the quoted sentence is the line-joined bytes of lines **61–62** — "…A moved substrate needs a / re-pin, never a re-interpretation of the old table." — inside the cited range. §8 Errata `E1` (:278) and `E2` (:283) do not touch §1 item 1, so "present, not errata" survives.
6. **Round-8 section's rule against the paraphrase.** `:1077-1078` (line-joined, bold markers dropped): "T1 — a case reads `stale` → re-measure at the live revision, or record the STALE cell with its reason; **never an edit of the recorded table**". Section's paraphrase matches (no quotation marks; punctuation `—` vs `;` only).
7. **"T1 fired for two cases".** Round-8 T1 names exactly two live instances (tsukuroi `084951be…`, mado `d7edaab4…`, `:1079-1080`); ER-4's headline/table read `current=4 stale=2 drift=0` (:333) with rows 3/4 the two `stale` cases (:328-329).
8. **ER-4 + addendum → follow-on rows, still open.** ER-4 `:352` — "the re-sweeps of the two `stale` cases land as their own rows, no rate is re-cut"; `:339` keeps them `[U]` as "this round's re-sweep work (its own appended rows)". Addendum (**:356**) reads both gates **`stale + drift`** (:358 tsukuroi, :359 mado). No block after the addendum lands either re-sweep: ER-5 (:366-401) adds no sweep ("closes no mutation re-sweep", ":398 `successor sweep joins the existing tsukuroi/mado successor debt`"); round 16/18 append kumitate cases; round 52 supersedes only the §3 `drift-pins` cell. "Open at this write" holds.
9. **"a rate never travels to a later revision"** — ER-3 `:312` "a rate never travels (per-revision, per-host; §0); `moved=0` is recorded, never manufactured".
10. **"an unlanded leg is named debt, never assumed"** — practised at ER-5 `:398` and at ER-4 `:339` (`[U]` kept, not assumed).
11. **Scratch directive** — `grep -n "tmp\|scratch"` over the section bytes: no match (exit 1). The section names no scratch path, no `/tmp`, no `$HYAKU_SCRATCH` value; nothing here can violate the 50 MB `/tmp` rule.
12. **C\*→C\*\* diff of the section** (`diff -u` of the C\* extent 1232–1247 vs the C\*\* extent 1237–1256): exactly the two fixes described, nothing else changed; the ER-4/addendum sentence was already present at C\*.

## Holds

- Both wave-1 findings are fixed in the C\*\* bytes, and the fixes are internally consistent: the heading pointer resolves uniquely to the round-8 section that carries the rule; the outcome sentence now carries the same disjunction as U9 `:235-237` and ER-3 `:312`.
- Every remaining claim in the section is source-backed (checks 5–10): the protocol quote and anchor, the two-case T1 firing, the appended/append-only mechanism, the byte-identical tables, the no-travel rate rule, the ER-4 + addendum follow-on rows still open, and the named-debt practice.
- No `:NNN-NNN` anchor inside this section is stale: the only line-anchored citation is `service-optin-protocol.md:59-62`, whose quoted content resolves at lines 61–62 inside the range.
- The section's dated statements are dated correctly and read as history, not as live state: "T1 fired for two cases" (round 8/9 boundary), "the addendum reads them `stale + drift`" (2026-10-14T20:02Z), "open at this write". No dead receipt is presented as live.

## Findings

**None.** No statement in `### The re-pin semantics, as executed` at C\*\* fails against its cited source, the ledger's current text, or the page's own conventions.

## Non-findings considered and rejected

- **"the round-16/18/52 appends take that form"** — read as: those three appended blocks take the appended (row-or-block) form the sentence just named. Round 16/18 say "seventh/eighth row appended" (row form of the disjunction); round 52 is an appended block superseding one §3 cell without editing it. All three append and none edits §§1–§4, which is the property being argued. Read as "all three are labelled ER-*n* errata blocks" it would be imprecise, but that is not what the sentence says.
- **"ER-4 and its addendum name the re-sweeps … as follow-on rows"** — the row form is ER-4's (`:352`, `:339`); the addendum (**:356-362**) names the re-sweeps on both legs without repeating "rows". The compound subject names them collectively, and the parenthetical assigns the addendum its own fact (it "reads them `stale + drift`"). Not a misstatement.
- **Quote drops the source's terminal period** (`…old table"`). Quoted fragment verbatim; the period sits outside the quoted span. Typographic, not a content drift.
- **Heading-pointer form vs the page's "measured anchor (path:line, …)" standing rule** (`SKILL.md:22`) — a unique, byte-identical heading is a deterministic locator on this page, and it is the robust form here: the C\*→C\*\* fix pass itself shifted the round-8 section from 1071–1092 to 1075–1096, so a line range would already be stale again. Not a violation worth a finding; the fix is an improvement over the rejected range.
- **"`the recorded tables byte-identical`"** — supported: ER-4 `:318` "No §1–§4 cell is edited; … old tables stand at their revisions".
- **"`(append-only, per U9 and ER-3 …)`"** — U9 says the cadence is a convention and that a new sweep appends a row (or errata block); ER-3 states the appended-row-or-errata-block outcome and "never as an edit of §1–§4"; the ledger states append-only itself at `:241` ("never edits above per `corpus/QUALITY.md` item 4"). Holds.

## Out-of-section observation (explicitly NOT a finding of this seat)

`SKILL.md:1431`, in a different section, still carries the same range the wave-1 reader rejected here — `so T1 fired (`:1069-1090`)`. At C\*\* the round-8 section is 1075–1096, so that pointer is stale in the same way F1 was. It lies outside this section's byte range; reported only so the owning re-read seat/wave can confirm rather than rediscover it.

## Tools installed

None.

## Scratch

`/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read17/` (blobs extracted from git objects, all files far under 50 MB); deleted before yield — no leftovers. No git/jj mutation, no writes outside the two wave-2 report paths.
