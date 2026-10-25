# Scribe — lesson `## Gate` draft (round 43, wave 1)

Seat: `L1Tameshi43.ScribeLessonGate` (leaf, no dispatch) · Round 43 · Access date **2026-10-25**
Milestone: lesson Gate draft · `Assimilation: none` (package read, never written, no campaign tool)

Axes named for this item: **rule-exactness** (CORPUS.md §SOURCES.md rule 1 fields, one block per
row), **locatability** (line number + contiguous quote + bytes + digest, criterion 79), and
**reconciliation** (registry vs. the round-43 entry vs. the item's premise). Each was walked
independently; nothing was written to the lane.

Read first, as instructed: `.ufo/evidence/round-43/contract.json` (whole file),
`corpus/lessons/round-42.md` `## Gate` (lines 1–121), fleet `CORPUS.md` §SOURCES.md rules
(lines 64–135), `corpus/QUALITY.md` criterion 79 (line 944).

---

## 1. What was opened and measured (observed)

Both sources were fetched by this seat into `/tmp/tameshi-r43-ScribeLessonGate-src/` with
`curl -fsSL`, and compared byte-for-byte with the snapshots the lane already pinned this round.

| source | bytes | sha256 | `cmp` vs lane snapshot |
|---|---|---|---|
| `https://en.wikipedia.org/wiki/Mutation_testing` | 170793 | `6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43` | identical |
| `https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/` | 38687 | `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce` | identical |

Pinned snapshots: `.ufo/evidence/round-43/sources/{wikipedia-mutation-testing.html,
stryker-equivalent-mutants.html}`, manifest `sha256.txt` (both digests above, verbatim). They are
in the lane worktree but **untracked** at this writing (`git status` →
`?? .ufo/evidence/round-43/sources/`), so criterion 79 binds only when the round commit lands them.
Second fetch of the Wikipedia URL an hour apart: same digest (`cmp` → `wiki-stable`). Three fetches
of the Stryker URL today (default UA, `Mozilla/5.0`, `curl/8`): all `38687 B` / `79f6501a…`, so the
digest is not a user-agent artefact. Independent reproduction: `.ufo/waves/round-43/w1/
ScoutStrykerEquiv.md` §1 (`38687` / `79f6501a…4079ce`) and `ScoutWikiEquiv.md` §1 (`170793` /
`6e4a06c0…cc43`, revid `1373580212`).

Quote word counts were executed, not estimated (`wc -w` over each string): 12, 13, 20, 9, 16, 15,
19, 7. Every quoted span was also tested for contiguity in the raw bytes — `str.count(q) → 1` for
each base fragment; the two spans that cross `<i>` / `<code>` markup are identified as such below
and quoted as rendered.

---

## 2. The draft `## Gate` block (paste-ready — do not write the lesson from this seat)

```markdown
## Gate

Theme (survivor-resolution rule, depth + calibration; `Assimilation: none`): one new row
(S159, Wikipedia) and one held row re-opened (S089, Stryker) ground the rule that a survivor is
classified, never relabelled. The staged package's equivalent-mutant material is deferred with the
package untouched (§Defer). Every source below was opened by this lane on 2026-10-25 and pinned
under `.ufo/evidence/round-43/sources/`; this seat's own fetches reproduced both snapshots
byte-for-byte (`cmp` exit 0) and match the digests recorded by `ScoutStrykerEquiv.md` §1 and
`ScoutWikiEquiv.md` §1.

### Admit — `corpus/knowledge/r43-survivor-resolution-rule.md` (S159 new; S089, S155, S158 held)

- S159 — https://en.wikipedia.org/wiki/Mutation_testing — title "Mutation testing - Wikipedia",
  170793 B, sha256 `6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43`, revision
  1373580212 (`wgCurRevisionId`, line 6; footer "last edited on 6 September 2026", line 1026),
  snapshot `.ufo/evidence/round-43/sources/wikipedia-mutation-testing.html`. Located quotes, all
  inside the `Mutation testing overview` h2 (line 762) — this revision has **no** "Equivalent
  mutants" section (`grep -c 'Equivalent_mutants'` → 0):
  (a) line 794, `<p id="mw-Q">`: "The resulting program is behaviorally equivalent to the original
  one. Such mutants are called equivalent mutants." (16 words; `<i id="mw-g">` wraps the two-word
  phrase "equivalent mutants", quoted as rendered); (b) line 796, `<p id="mw-w">`:
  "Equivalent mutants detection is one of the biggest obstacles to practical usage of mutation
  testing." (15 words, contiguous);
  (c) line 794: "However, there are cases where it is not possible to find a test case that could
  kill this mutant." (19 words, contiguous). Reachability is a separate RIP condition, line 786:
  "A test must reach the mutated statement." (7 words) — and the page carries no `surviv`,
  `unreach`, `unkilled` or `undetected` text (`grep -ci` → 0 each; `ScoutWikiEquiv.md` §4), so it
  never separates a dead-code survivor from an equivalent mutant. That separation is the lane's
  rule, not the page's.
- S089 (held, re-opened) — https://stryker-mutator.io/docs/mutation-testing-elements/
  equivalent-mutants/ — title "Equivalent mutants | Stryker Mutator", 38687 B, sha256
  `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`, snapshot
  `.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html`. Not a new row: the URL is
  already `corpus/SOURCES.md:98`, and a second row for one document would need
  `supersedes S089 — ` (rule 2). Located quotes: line 16, "There is no definitive way for Stryker
  to find and ignore them." (12 words, contiguous); line 16, "There is currently also no way yet to
  mark them to be ignored." (13 words, contiguous); line 17, "the only solution is by finding these
  by hand" (9 words) — the page's own remedy, i.e. classification is authored, not queried; line 15,
  "even if we change `>=` to `<=` and even `<` or `>` we will get the same output each time!"
  (20 words rendered; `<code>` splits the four operators), the `10 ** 0` example.
- S089 digest moved, and the Gate records it because the anchor cell may not. The anchor cell
  (`corpus/SOURCES.md:98`) pins `html sha256 bc572676…e04d`, fetched 2026-10-22 and reproducible
  across the repeated fetches then (`.ufo/waves/round-26/w1/DraftSourcesRows.md:100-118`). Today's bytes
  hash `79f6501a…79ce`. Cause, from the source's own headers: `last-modified: Sat, 24 Oct 2026
  15:08:38 GMT`, `cf-cache-status: DYNAMIC` (`ScoutStrykerEquiv.md` §1) — the page was rebuilt
  between the two reads. The prose did not move: the document is the same 38687 B, and
  `10 ** 0 = 1` and "no definitive way for Stryker" land at the same character offsets r26 recorded
  (30613 / 30826) and are each contiguous once. The 2026-10-22 copy was not retained, so the
  changed bytes cannot be named; the page's upstream markdown is a smaller pin if the L1 wants one
  (2057 B, sha256 `39aba4bc…22328`, `ScoutStrykerEquiv.md` §5). Consequence for the entry:
  `corpus/knowledge/r43-survivor-resolution-rule.md:20` says "byte-identical to S089's 2026-10-22
  anchor" — that sentence is false and must read "same prose, new digest".
- PROVINCE: survivor-classification semantics for the lane's own kill verdicts is Core F1/F8
  ground, where S159 and S089 are the tool vendors' own statements. QUALITY: every quote is ≤25
  words and located; both documents are pinned under `.ufo/evidence/round-43/sources/` with a
  manifest and satisfy criterion 79 once the round commit lands them (they were still untracked
  when this Gate was drafted — `git status` → `?? .ufo/evidence/round-43/sources/`); the S089
  re-open is recorded here rather than by editing its anchor, per rule 2.
- Held rows cited by the same entry, all re-opened this round and unchanged: S155 (PIT basic
  concepts; its `used-by` cell gains the entry), S158 (PIT `DetectionStatus`; its `EQUIVALENT(true)`
  at line 75 and the comment at lines 71–72 are present verbatim in the committed round-42
  snapshot, verified this seat). S156 (PIT FAQ) is *not* cited: `ScoutPitEquiv.md` §2 shows a
  case-insensitive count of 0 for `equivalent`, `unkillable` and "cannot be killed" on the live
  page, which is byte-identical to the committed snapshot (`ccf6ac49…`).

### Defer — the staged package's equivalent-mutant material (`staged:S156`, `staged:S163`–`staged:S166`, `staged:S168`)

`Assimilation: none`. `/home/vgpnk/Projects/shokuknow/merge/tameshi/` was read only; its four
equivalent-mutant entries are unchanged since 2026-10-24 23:33 (`stat`), so round-42's verdicts
still describe these bytes:

| staged entry (package path) | sha256 | what it argues | disposition |
|---|---|---|---|
| `knowledge/corpus/knowledge/survivor-classification.md` | `dc9a7dbb…` | a survivor is a candidate hole, classified into behaviourally-equivalent vs. behaviourally-different (lines 31–33) | REFUSED — round-42 reasons stand |
| `knowledge/corpus/knowledge/mutation-score-semantics-cjk.md` | `44a0f083…` | the score's denominator excludes equivalent mutants (lines 9, 15–17, 45–48) | DEFERRED |
| `knowledge/corpus/knowledge/llm-mutant-equivalence-cost.md` | `08f50720…` | LLM mutants carry a worse equivalent-mutant rate, so a survivor needs an equivalence witness (lines 16, 27–32) | DEFERRED |
| `knowledge/corpus/knowledge/cjk-mutation-metric-and-tool-comparison.md` | `90c85c6a…` | §2.1 states the killed ÷ non-equivalent metric (line 11) | DEFERRED |

1. Rule 1: none of their sources was opened in round 43. The round opened S089 and S159 only; a
   package row opened 2026-10-23 cannot be appended on that opening.
2. `survivor-classification.md` was refused in round 42 and the defects are unrepaired in these
   bytes: the drifted quote is still at lines 13–14 ("…テストの穴とは当たり／ません" where the page
   reads 「…とは限りません」), and the recheck cell (line 5) still expects one hit of `168 killed`.
3. `mutation-score-semantics-cjk.md:56` still points at `CANNOT-ANSWER.md` §3.7, which does not
   exist in the landing repo: `find /home/vgpnk/Projects/shokunin -maxdepth 4 -name
   'CANNOT-ANSWER*'` → 0 hits, and none is inside `merge/tameshi/`. The only copy that resolves is
   the assimilation source lane, `/home/vgpnk/Projects/shokuknow/lanes/tameshi/CANNOT-ANSWER.md`
   (sha256 `b501b218…c8ea`, one of 16 per-lane copies), whose item 7 at line 41 reads "No Chinese
   *peer-reviewed journal* paper on mutation testing was found." That gap is stale in the package's
   own terms: `cjk-mutation-metric-and-tool-comparison.md:2,20` cites a refereed 《软件学报》 2024
   article (S168). The round-42 flip condition is therefore unmet — the pointer is unresolvable
   where the entry would land and obsolete where it does resolve.
4. Duplication. The survivor-classification thesis is now stated by the lane's own K/D/E/U rule
   (this round's entry), and F8 is already partly supported by
   `corpus/knowledge/oracle-anchored-survivors.md` (`corpus/README.md:422-437`; line 85 still reads
   "open" and line 427 corrects it, so the r42 citation "README.md:85" pointed at the stale cell).
   The denominator thesis of the cjk entry is held F1 (`corpus/knowledge/mutation-score-semantics.md`).
5. Id: `staged:S156` is arXiv 2406.09843, while the lane's S156 is the PIT FAQ
   (`corpus/SOURCES.md:126`); `llm-mutant-equivalence-cost.md:2` cites `S156`, so an as-is adoption
   would repoint that citation at a different document. The lane's next unused id is S160
   (`corpus/SOURCES.md:456`) and the guard's safe floor for a partial adoption is S256
   (`corpus/SOURCES.md:454`).

Flip for a later assimilation round: re-open each source in the adopting round and snapshot it
there (rule 1), repair 2 and 3, renumber by document, and say what each entry adds beyond the
lane's K/D/E/U rule.

### Ids, used-by, census

- Rows: 113 (S001–S158) at the freeze → 114 now —
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `114` (2026-10-25).
  New row: S159. `- Next unused id: S160.` (`corpus/SOURCES.md:456`).
- Used-by changes (rule 2, old→new, no other cell edited):
  - S089 `corpus/knowledge/mutation-case-kumitate-cite-check.md` → the same plus
    `corpus/knowledge/r43-survivor-resolution-rule.md`.
  - S155 `corpus/knowledge/pit-outcome-vocabulary.md` → the same plus
    `corpus/knowledge/r43-survivor-resolution-rule.md`.
  - S158 `corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r42-attribute-and-outflag-destinations.md`
    → the same plus `corpus/knowledge/r43-survivor-resolution-rule.md`.
- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` printed `ok`
  over `corpus/SOURCES.md` at round start and after the append, with the same 9 × W04 + 1 × W01
  warning set and no E code (`.ufo/evidence/round-43/census-sources/{start,after}.stdout`).
  Neither receipt stores the exit status or a row count; the exit-0 claim rests on the `ok` verdict
  line, and the 113/114 counts rest on the `grep -cE` command above.
- No duplicate-URL warning names `en.wikipedia.org/wiki/Mutation_testing`, so S159 is the only row
  holding that URL.
```

---

## 3. Findings the Gate depends on (numbered, checkable)

1. **The item's premise "Stryker = new source row" does not hold on the lane's bytes.** The URL is
   already a mined row: `corpus/SOURCES.md:98` (S089, `mined`, opened 2026-10-22, recheck 180d).
   CORPUS.md rule 2 allows only `status`, `recheck` and `used-by` to change in place; any second
   row for the same document must open `supersedes S089 — `. The registry therefore assigns the
   only new id to Wikipedia (**S159**) and leaves S160 unused
   (`corpus/SOURCES.md:453-456`). My Gate carries an **admit block for S159** and a **re-open block
   for S089**; both carry every field the item demands (URL, access date, bytes, sha256, ≤25-word
   located quotes with line numbers). Drafting a second Stryker row would have violated rule 2 and
   contradicted the already-appended registry.

2. **The entry was corrected mid-wave and now agrees with the registry.** First read of
   `corpus/knowledge/r43-survivor-resolution-rule.md` (5997 B) had `source: S159, S160; S155
   (held), S158 (held)`; the current bytes (7554 B, sha256
   `7b26c0a7ad462ab3532b756f680c0143b10811e6a9c53169241eafe8c8f266e3`, mtime 07:54:27) read
   `source: S089 (held, re-opened), S159 (new); S155 (held), S158 (held)` (line 3) and anchor the
   Wikipedia quotes to the `Mutation testing overview` section with the same line numbers this Gate
   uses (lines 24–32). No further id correction is owed.

3. **`corpus/knowledge/r43-survivor-resolution-rule.md:20` is false and must be fixed.**
   It claims the Stryker snapshot is "byte-identical to S089's 2026-10-22 anchor". S089's anchor
   pins `bc572676…e04d`; today's bytes are `79f6501a…79ce`, and the HTTP `last-modified` is
   2026-10-24T15:08:38Z, after the pinned fetch. The **prose** is unchanged (same 38687 B, same
   character offsets 30613/30826 for the two markers as r26 recorded at
   `.ufo/waves/round-26/w1/DraftSourcesRows.md:127-131`, each span contiguous once). The honest
   sentence is "same prose, new digest".

4. **"Equivalent mutants section" is the wrong anchor for the Wikipedia row.** `grep -c
   'Equivalent_mutants'` → 0; the heading inventory has no equivalent-mutant heading. The two
   paragraphs are `<p id="mw-Q">` (line 794) and `<p id="mw-w">` (line 796) inside the
   `Mutation testing overview` h2 at line 762. The appended row already says
   `§Mutation testing overview, p ids mw-Q and mw-w` (`corpus/SOURCES.md:129`) — correct. Only
   prose elsewhere needs the same phrasing.

5. **The page does not carry the equivalent/dead-code distinction, which is load-bearing for C1.**
   `surviv`/`unreach`/`unkilled`/`undetected` each count 0 in the snapshot; equivalence is defined
   behaviourally (line 794) and reachability appears only as RIP condition 1 (line 786). So the
   page cannot be cited for "a dead-code survivor is not an equivalent mutant" — that ruling is the
   lane's `D` class. My Gate says this explicitly so the entry cannot be read as borrowing vendor
   authority for the `D` verdict.

6. **PIT FAQ says nothing about equivalence**, so it is rightly excluded from the entry's citations:
   `ScoutPitEquiv.md` §2 counts `equivalent` 0, `unkillable` 0, `cannot be killed` 0; the live page
   is byte-identical to the committed snapshot (`ccf6ac49…`). S156's `used-by` did not change this
   round (verified in the diff).

7. **Census receipts do not carry the numbers the registry note attributes to them.** Both
   `census-sources/*.stdout` print only the 10 warnings and `ok <path>`; neither prints a row count
   and no `.exit` file is retained (`ls` → only `start.stdout`, `after.stdout`, `start.exit`).
   The `113`/`114` counts and "exit 0" in `corpus/SOURCES.md:455` are correct in substance but
   rest on a `grep -cE` count and on the `ok` line, not on the receipt. The Gate states that
   provenance rather than repeating the note's phrasing.

8. **The pre-append dedupe receipt the registry note cites was not retained.** `corpus/SOURCES.md:453`
   says "the census W04 warning showed S089 already holds that URL", but
   `.ufo/evidence/round-43/census-sources/` holds only the start and after runs (neither mentions
   Stryker), and `ExecCensus.md` contains no dedupe run (`grep -i 'stryker|S089|dedupe'` → 0).
   The dedupe itself is directly verifiable and is recorded instead: `corpus/SOURCES.md:98` holds
   the URL. Not a blocker; it is a receipt gap the L1 may route.

9. **The staged package is byte-stable and untouched by this round.** All four equivalent-mutant
   entries and `SOURCES.append.md` share mtime 2026-10-24 23:33:20; none is cited by any lane
   knowledge file (`grep` over `corpus/README.md` and `corpus/SOURCES.md` → 0 hits for all four
   names), and the r42 refusal/deferral blocks
   (`corpus/lessons/round-42.md:82-108`) still describe them. This is why a deferral block, not an
   adoption, is the gate outcome.

10. **`corpus/README.md:85` (the r42 citation for F8) is stale by its own correction.** Line 85
    reads "open"; lines 424–437 record F8 as "partly held" and line 427 names the line-85 cell as
    superseded. Any repetition of the r42 duplication argument should cite 422–437 instead.

11. **`CANNOT-ANSWER.md §3.7` resolves, but only in the assimilation source lane, and its content
    is obsolete.** `mutation-score-semantics-cjk.md:56` cites it. No such file exists under
    `/home/vgpnk/Projects/shokunin` (`find -maxdepth 4` → 0) or in `merge/tameshi/`; the resolving
    copy is `/home/vgpnk/Projects/shokuknow/lanes/tameshi/CANNOT-ANSWER.md` (sha256
    `b501b218976f3dc3faa17325a5b6e86b9046df4f67eadcb082a8d46d7053c8ea`), where §3 item 7 (line 41)
    says "No Chinese *peer-reviewed journal* paper on mutation testing was found". The package's
    own `cjk-mutation-metric-and-tool-comparison.md:2,20` (row S168, 《软件学报》 2024) closes that
    gap, so the cjk entry points at a file the landing repo does not carry and at a paragraph its
    own package has superseded. This sharpens the r42 flip condition rather than repeating it.

---

## 4. Touched surfaces

- **Written:** this report only (`.ufo/waves/round-43/w1/ScribeLessonGate.md`) and scratch under
  `/tmp/tameshi-r43-ScribeLessonGate-src/` (fetches only; removed before return).
- **Read:** `.ufo/evidence/round-43/contract.json`; `.ufo/evidence/round-43/sources/*`;
  `.ufo/evidence/round-43/census-sources/*`; `.ufo/waves/round-43/w1/{ScoutStrykerEquiv,
  ScoutWikiEquiv, ScoutPitEquiv, ExecCensus}.md`; `corpus/SOURCES.md`, `corpus/README.md`,
  `corpus/QUALITY.md:944-1002`, `corpus/lessons/round-42.md`,
  `corpus/knowledge/r43-survivor-resolution-rule.md`, `corpus/knowledge/oracle-anchored-survivors.md`;
  fleet `CORPUS.md:22-135`; read-only package under
  `/home/vgpnk/Projects/shokuknow/merge/tameshi/` and `.ufo/waves/round-26/w1/DraftSourcesRows.md`.
- **Out of scope, not attempted:** no edit to any lesson, entry, registry or counter; no git/jj
  mutation; no counter run (C1/C2/C3 are other seats'); no campaign tool; nothing installed
  (no pacman, uv, npm or cargo transaction — none needed).

---

## 5. Known limits of this draft

- The Gate is drafted against the **worktree** registry (114 rows, S159 appended, S089/S155/S158
  used-by extended). If the L1 renumbers or appends a superseding S160 for the Stryker digest, the
  re-open block's first sentence and the `Next unused id` line must be rewritten to match; the
  quotes, bytes and digests do not change.
- The Guarantee of "byte-identical" prose for S089 is bounded: same size, same line layout, same
  marker offsets, same upstream markdown text — but the 2026-10-22 file is gone, so the changed
  bytes are unnamed by construction.
- Wikipedia is editable; the pin is the sha256 + revid, and every line number here is valid only
  for revision 1373580212.
- I did not run `sources-census.sh` (it is not in the lane's `tools/`); the census paragraph
  reports the retained receipts and the one row-count command this seat executed.
