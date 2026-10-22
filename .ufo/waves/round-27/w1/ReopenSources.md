# ReopenSources: round 27, wave 1 (frontier F8 source re-open)

Seat: TameshiR27.ReopenSources (reviewer, leaf, no dispatch).
Pin: content revision `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`; base `91edf9cd82ccc72e10f62f81d37181f549d593b8`.
Re-opened 2026-10-22 by ordinary HTTP GET. All four responses returned HTTP 200 on the first request. No challenge page was met.

## Verdict per row

| Row | Tier | Anchor | Teaches | Quotes |
|---|---|---|---|---|
| S012 (arXiv 2608.17214) | **Disagree.** The pin says B. The contract's B means secondary, and S012 is an original paper. | Agree | Agree, with three precision notes | Agree. Every quote is verbatim, located, and 25 words or fewer. |
| S090 (sysexits(3)) | Agree. A, scoped to the BSD convention. | Agree | Clause 1 agrees. **Clause 2 disagrees:** it is a use-note, not something the page says. | Agree. Every quote is verbatim, located, and 17 words or fewer. |
| S091 (gitrevisions) | Agree. A, scoped to Git object names. | Agree | Agree. "Not an interior-slice match" is an inference from "leading". | The anchors.json quote agrees. **The entry paraphrase disagrees:** it drops "unique within the repository". |

## Findings, by severity

Line numbers refer to the pinned files unless marked "worktree".

1. **High (worktree only, not in the pin).** The uncommitted entry (121 lines, sha256 `9144b525…f468`) says at lines 67–68 that the S_PIN_INCLUDES prefix direction "comes from S091 by analogy and from code lines `:1195` and `:1219`, which are the code under mutation." Its own stricter test at lines 28–32 says "no code line and no run of the mutated file supplies the value." Its §3 table still labels the row `anchored-hole` (line 50). Under the S012 definition quoted at pinned lines 13–18, an expectation that flows from the code under mutation is state-anchored. As written, this row cannot be an anchored hole. If this text lands, the C2 wording "composed outside that code" is false for one of the four survivors. Smallest fix: relabel the row as a differential hole with convention support, as the entry's own §4 recipe says, or remove the code-line support.

2. **Medium (pin).** The pinned S_PIN_INCLUDES row (line 47) says `anchored-hole`. §4 bullet 1 (lines 53–56) says "In each case the pristine agrees with an outside anchor and the mutant breaks it." §4 bullet 2 (lines 59–61) says the same row is "held by convention only": S091 applied to a content sha256 by analogy. The class label and bullet 1 overstate the anchor. Smallest fix: relabel the row as convention-supported, and change bullet 1 to say three of four, or drop "In each case".

3. **Medium (pin, registry).** S012 tier B does not fit the contract's tier text. As quoted in the pinned tree, A is "primary or authoritative for that scope (spec, official docs, **source code**, original paper, maintainer statement, the lane's own re-runnable gate output)" (`.ufo/waves/round-16/w2/ReopenS053.md:65`). B is "strong secondary (expert write-up with reproducible detail, survey, textbook)", and "A is reserved for primary/authoritative work and can never be a survey" (`.ufo/waves/round-16/w2/ReopenS057.md:75–78`). The row's only stated reason for B is "single-system preprint, one author" (line 23). That is an evidence limit, not a source-type limit. The registry already tiers original papers with narrow evidence at A: S007 (line 18), S008 (line 19), S019 (one company, line 30), S021 (line 32), S027 (line 38). The one original paper at B, S030 (line 41), is a rejected row, and its B is not argued from source type. Smallest fix: a supersedes row at A, scoped to the two definitions (abstract sentence 5), with the one-system numbers kept out of its teaches. Then pinned line 81 should read "tier A for the definitions; the one-system rates are not used." The tier cell is immutable in a prior-round row, so an in-place edit is not allowed.

4. **Medium (pin, registry).** The "Next unused id" pointer is stale. `corpus/SOURCES.md:338` reads `- Next unused id: S090.` Rows S090 (line 99) and S091 (line 100) exist. The base already had the pointer at S090 (base line 336), so this round did not advance it. The next writer could reuse S090 or S091. Smallest fix: append `- Next unused id: S092.` as the last line. Do not edit the earlier pointer lines (round-18 QUALITY 35).

5. **Medium-low (pin).** The S091 uniqueness qualifier is dropped. Pinned line 47 paraphrases S091 as "(a short name is a leading substring)". Lines 60–61 say "the prefix rule comes from Git's abbreviated-name convention (S091)". anchors.json line 53 says "that a short pin names a leading substring". All three drop "unique within the repository". That is the source's own condition, quoted at anchors.json line 51 and in the row's teaches (line 100). A one-digest pin has no analogue of uniqueness among repository objects. The entry should say that, not drop the clause silently. Smallest fix: restore the qualifier at line 47 and in anchor_strength, and add one sentence saying the probe does not test uniqueness.

6. **Low (pin).** S090 teaches clause 2, "an outside anchor for a usage exit of 64, fixed outside any gate's code", is the registry's use-note, not a claim of the page. The row also omits the page's BUGS disclaimers, "The choice of an appropriate exit value is often ambiguous." and "This interface is not portable.", which bound how strong the anchor is. Smallest fix: none needed in the entry. If the row is corrected, use a supersedes row.

7. **Low (pin).** S012 teaches drops three things. It drops the condition in abstract sentence 2, "If a fault moves measurement and expectation together the comparison cancels exactly". It drops "holding" and "on published procedure" from sentence 11. And it states the unit "mutants", which sentence 11 leaves implicit; sentence 12 says "the 12 recovered mutants". Smallest fix: fold into the supersedes row in item 3 if one is written.

8. **Low (pin, Gate record).** The 25-word Gate quotes for S012, S090 and S091 are in `corpus/lessons/round-27.md` at lines 28–30, 37–38 and 43–45. That file is absent at the pin (`git cat-file -e 2227d83:corpus/lessons/round-27.md` fails). It first appears at HEAD `2abb018`. The S012 Gate quotes only the definitional sentence. The row's "8 of 46" and "366 mutants" clauses have no located quote. The three Gates also give no revision or publication date, which `RV08SourcesContract.md` line 6 asks for. The rows carry those dates. Smallest fix: add a Gate quote for the numeric clauses, add the dates, and say in the lesson that the Gate lives at HEAD, not at the pin.

9. **Low (pin, notation).** Pinned line 47 says "content pin = digest chars 8–20". The probe slices `digest[8:20]` (`.ufo/evidence/round-27/f8/anchor-probe.py:60`), which is 12 hex characters. Smallest fix: write `digest[8:20] (12 hex)`. The worktree's "12-hex" at line 67 is correct.

10. **Low (pin, traceability).** The external anchors in anchors.json (lines 40 and 51) carry no location field. The location appears only in the entry header, line 1. Smallest fix: add a `location` field to each external anchor.

## 1. Evidence and commands

**Re-opened sources (ordinary GET, 2026-10-22).** The bodies are kept under `/tmp/tameshi-r27-reopen-w1/`.

- arXiv 2608.17214: `curl -sSL -o arxiv-abs.html https://arxiv.org/abs/2608.17214` returned `arxiv-abs http=200 bytes=42588`, sha256 `fb6f384d…a80`. The page shows "Submitted on 17 Aug 2026" and one submission-history entry, "[v1] Mon, 17 Aug 2026 23:56:16 UTC (47 KB)". The abstract has 15 sentences. `arxiv-v1-abs.html` (`http=200 bytes=42593`, sha256 `27a1f150…1635`) carries the identical abstract. Only v1 exists.
- FreeBSD sysexits(3): `freebsd http=200 bytes=59251`, sha256 `1fc793a2…2dbf`. The footer reads "FreeBSD 15.1 May 9, 2024". The ERRORS section holds the EX_USAGE entry. DESCRIPTION reads "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." BUGS reads "The choice of an appropriate exit value is often ambiguous." and "This interface is not portable."
- git-scm gitrevisions: `gitrevisions http=200 bytes=74658`, sha256 `ada50822…4326`. The version table reads "gitrevisions last updated in 2.56.0" with date 2026-09-28. The `<sha1>` entry under SPECIFYING REVISIONS reads "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository."

**Pinned registry and entry.** `git --no-pager show 2227d83:corpus/SOURCES.md` has sha256 `0a66531d…58e5`, with the S012 row at line 23, S090 at 99, S091 at 100, and the pointer at 338. `git --no-pager show 2227d83:corpus/knowledge/oracle-anchored-survivors.md` has sha256 `994f5324…356ad` and 82 lines. `git --no-pager show 2227d83:.ufo/evidence/round-27/f8/anchors.json` has sha256 `780e1009…5eea`, which matches the receipt's anchors digest.

**Base-to-pin registry diff.** `git --no-pager diff --stat 91edf9cd 2227d83 -- corpus/SOURCES.md` printed `corpus/SOURCES.md | 4 +++-`. A cell-by-cell comparison of S012 shows status `queued` to `mined`, used-by `—` to `corpus/knowledge/oracle-anchored-survivors.md`, and the other nine cells unchanged. The lesson's Gate records the same change. S090 and S091 were absent at base.

**Worktree state.** `git --no-pager status --short -- corpus/knowledge/oracle-anchored-survivors.md` printed ` M corpus/knowledge/oracle-anchored-survivors.md`. The worktree copy has sha256 `9144b525…f468` and 121 lines. HEAD `2abb018` holds the pinned entry, sha256 `994f5324…`. anchors.json is unchanged in the worktree and at HEAD.

**Tier wording.** The contract file `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` is not at the pin and not in the worktree. Its wording is taken from `.ufo/waves/round-16/w2/ReopenS053.md:65` and `.ufo/waves/round-16/w2/ReopenS057.md:75–78`, both read from the pinned tree.

**Quote rule.** `.ufo/waves/round-21/w1/RV08SourcesContract.md` line 5 (next ID), line 6 (an exact located quote of at most 25 words grounding `teaches`), and line 7 (tier scoped to the stated scope; community cannot be A).

**Word-count convention.** Whitespace split. `corpus/lessons/round-12-verifier-spotcheck.md:123` counts "cargo-mutants" as one word, giving "20 words".

## 2. Row S012 (pinned line 23)

- **Tier: disagree (item 3).** The contract's A list includes "original paper". S012 is the paper that defines state-anchored and specification-anchored expectations (abstract sentences 4 and 5). Its measured numbers are one-system results (sentences 9, 11 and 15), and the row says so. But the row's stated reason for B is an evidence limit. Tier, under the contract, is about source type. The limit belongs in the scope or teaches cell, as S019 (one company, A) and S021 (A) show.
- **Anchor: agree.** "Abstract, arXiv:2608.17214v1 (submitted 2026-08-17)" matches the arXiv page. Only v1 exists, and the submission date is 17 Aug 2026.
- **Teaches: agree, with notes (item 7).** "Names state-anchored oracles, whose expectation flows from the code under mutation" matches sentence 5. The cancellation is conditional, as sentence 2 shows. "Measured on one system (366 mutants)" matches sentences 9 and 15.
- **Quotes: agree** (ledger rows 1 to 4).

## 3. Row S090 (pinned line 99)

- **Tier: agree (A).** FreeBSD's own manual page is official documentation, which the contract lists under A. The scope cell records that the page is "legacy and deprecated by its own text", and the deprecation sentence is verbatim. The page is authoritative for what the convention labels 64. It is not authority for what a gate must return. The entry uses it that way: "a fixed convention, not a recommendation" (lesson lines 39–41).
- **Anchor: agree.** The anchor names §ERRORS, EX_USAGE entry. The footer reads "FreeBSD 15.1 May 9, 2024". The fetch date is 2026-10-22.
- **Teaches: clause 1 agrees; clause 2 disagrees (item 6).** Clause 1 is verbatim, 17 words. The scope cell says "command-line programs", but the page's NAME says "system programs" and DESCRIPTION says "commands". That is a minor wording gap.
- **Quotes: agree** (ledger rows 5, 6, 8, 11, 13).

## 4. Row S091 (pinned line 100)

- **Tier: agree (A).** This is official Git documentation for object-name syntax. The scope cell limits the use: "applies to Git object names, used here only as a convention for short hex pins". The step to content digests is the entry's analogy, and the entry labels it "by analogy" (pinned lines 60–61; anchors.json line 53).
- **Anchor: agree.** The anchor names §SPECIFYING REVISIONS, the `<sha1>` entry. The page says "last updated in 2.56.0" with date 2026-09-28. The fetch date is 2026-10-22.
- **Teaches: agree, with two wording notes.** "A short object name is the full name" does not fit, because the full 40-byte name is not short. A safer wording is "an object name is either the full name or a leading substring that is unique within the repository". "A prefix convention, not an interior-slice match" is the registry's inference from "leading substring", and should be labelled as one. The page's example confirms that uniqueness concerns other objects: "if there is no other object in your repository whose object name starts with dae86e".
- **Quotes: the anchors.json quote agrees** (ledger row 7). **The entry paraphrase disagrees** (item 5).

## 5. Quote ledger

Every quote attributed to S012, S090 or S091 by the entry, anchors.json, or the round-27 Gate. Verbatim means exact after whitespace collapse. Words are counted by whitespace split.

| # | Row | Attributed at | Quoted text | Verbatim | Location in source | Words | 25 or fewer |
|---|---|---|---|---|---|---|---|
| 1 | S012 | entry line 1 | Oracles That Cannot Fail | Yes, title prefix | arXiv abstract page title | 4 | Yes |
| 2 | S012 | entry lines 13–14 | flows, directly or transitively, from | Yes | abstract sentence 5 of 15 | 5 | Yes |
| 3 | S012 | entry lines 17–18 | composed from values fixed outside the code under mutation | Yes | abstract sentence 5 of 15 | 9 | Yes |
| 4 | S012 | anchors.json line 3 (note) | composed from values fixed outside the code under mutation | Yes | abstract sentence 5 of 15 | 9 | Yes |
| 5 | S090 | entry line 46 | EX_USAGE (64) and a bad flag, joined by an ellipsis as in the entry | Yes, both fragments, in order | §ERRORS, EX_USAGE entry | 2 and 3 | Yes |
| 6 | S090 | anchors.json line 40 | EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag | Yes, after whitespace collapse (the page wraps the line) | §ERRORS, EX_USAGE entry | 17 | Yes |
| 7 | S091 | anchors.json line 51 | or a leading substring that is unique within the repository | Yes, after whitespace collapse | §SPECIFYING REVISIONS, `<sha1>` entry, first sentence | 10 | Yes |
| 8 | S090 | SOURCES line 99, teaches clause 1 | EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag | Yes | as row 6 | 17 | Yes |
| 9 | S091 | SOURCES line 100, teaches | a leading substring that is unique within the repository | Yes | as row 7 | 9 | Yes |
| 10 | S012 | lesson lines 28–30 (HEAD only) | An expectation is specification-anchored when composed from values fixed outside the code under mutation, and state-anchored when it flows, directly or transitively, from that code. | Yes | abstract sentence 5 | 25 | Yes, at the limit |
| 11 | S090 | lesson lines 37–38 (HEAD only) | as row 6 | Yes | as row 6 | 17 | Yes |
| 12 | S091 | lesson lines 43–45 (HEAD only) | The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository. | Yes, after whitespace collapse | §SPECIFYING REVISIONS, `<sha1>` entry | 18 | Yes |
| 13 | S090 | SOURCES line 99, scope (supporting page text) | This interface has been deprecated and is retained only for compatibility. Its use is discouraged. | Yes | DESCRIPTION | 15 | Not an attributed quote |

Unquoted paraphrases, checked but not graded as quotes:

- Pinned line 47: "(a short name is a leading substring)". It drops the uniqueness clause (item 5).
- Pinned lines 60–61: "the prefix rule comes from Git's abbreviated-name convention (S091)". Acceptable, because line 61 says "by analogy".
- anchors.json line 53 (anchor_strength): drops the uniqueness clause (item 5).
- Pinned lines 13–14: "state-anchored" is S012's own term. No quote is involved.

## 6. Registry state

- **URL duplicates: none.** Each of the three URLs appears once, at SOURCES lines 23, 99 and 100.
- **Pointer: stale** (item 4).
- **Opened dates: consistent.** S012 keeps its opened date of 2026-10-19, as the append-only rule requires. The 2026-10-22 re-open appears in the entry header and the Gate.
- **Cell counts: 11 per row for all three rows,** with no `|` inside any cell.

## 7. Worktree drift (uncommitted)

The worktree entry (sha256 `9144b525…f468`, 121 lines) has new text that touches the three rows.

- Lines 28–32 add a test: "no code line and no run of the mutated file supplies the value."
- Lines 62–69 say the S_PIN_INCLUDES direction comes partly from code lines `:1195` and `:1219`. The worktree's own test at lines 28–32 rules that out (item 1).
- Line 50 still labels the row `anchored-hole`.
- Line 67 says "12-hex", which matches the probe (item 9).
- Lines 98–104 add a statement from a kumitate file about exit 64. This is not an S-row attribution, and I did not check it.
- Line 120 repeats the pinned S012 tier B sentence (item 3).

The worktree adds no new quotes attributed to S012, S090 or S091. The quotes in the ledger are unchanged. I did not verify `:1195` or `:1219` in kumitate, which is outside this item.

## 8. Smallest safe corrections (for the L1 to apply; I did not edit)

1. Relabel the S_PIN_INCLUDES class at pinned line 47 and soften "In each case" at line 54. If the worktree text lands, remove its code-line support or relabel the row (item 1).
2. Append `- Next unused id: S092.` to `corpus/SOURCES.md` (item 4).
3. Restore "unique within the repository" at pinned line 47 and at anchors.json line 53. Say the uniqueness condition is untested for one-digest pins (item 5).
4. S012 tier: write a supersedes row at A, scoped to the definitions. Update pinned line 81 to match. If the L1 keeps B, the Gate should say why, and the reason cannot be the contract's B (item 3).
5. Optional: supersedes rows for the S090 teaches clause 2 and the S012 teaches details (items 6 and 7). No entry change is needed for these.
6. Gate: add a located quote for the S012 numeric clauses, add revision or publication dates for all three rows, and note that the lesson lives at HEAD (item 8).
7. Notation: change "digest chars 8–20" to "digest[8:20] (12 hex)" at pinned line 47 (item 9).
8. anchors.json: add a `location` field to each external anchor (item 10).

## 9. Residual risk and verification gaps

- The tier wording comes from quotations in two pinned wave files. The contract is not at the pin, not in the worktree, and I did not open the fleet-root CORPUS.md, because the bounds forbid touching the fleet repo. If the contract text differs, recheck item 3.
- The fleet validator, `scripts/sources-census.sh` in the fleet root, was not run, for the same reason. Item 4 comes from reading the file.
- S012 was read from its abstract only. The full text was not opened.
- Not checked, because they are outside this item: the kumitate header quotes (cite-check.mjs lines 35, 38, 61, 69 and 71), kumitate round-close-gate.mjs lines 204–206, and the probe's behavior beyond the slice on line 60. These are contract-attributed, not S-row-attributed.
- The worktree findings apply to sha256 `9144b525…f468` as read at review time. They may already be stale.
- The gate's behavior on an ambiguous pin prefix is untested. S091's uniqueness condition is the thing that would test it.
- Quote checks are whitespace-normalised substring matches against the fetched bodies. No PDF or OCR step was involved.

## 10. Tooling and writes

- No tool was installed, upgraded, or removed. `RULES.md` was not needed.
- Fetches used curl with the user agent `Mozilla/5.0 (tameshi-r27 source re-open; ordinary HTTP client)`. The string starts with a browser-style prefix. No challenge was met, and I record the exact string for transparency.
- Repository access was read-only: `git show`, `cat-file`, `diff`, `grep`, `log` and `status`, each with `GIT_OPTIONAL_LOCKS=0`, with one exception. One `git --no-pager status --short` call omitted that variable, to check whether `.ufo/waves/round-27/w1/` was tracked. Git may have refreshed the lane index stat cache on that call. No tracked content changed. I disclose it here rather than leave it out. No git write command and no jj command ran.
- Scratch files are under `/tmp/tameshi-r27-reopen-w1/`: fetched bodies, revision exports, and a copy of the SOURCES diff. Nothing else was written except this report.
