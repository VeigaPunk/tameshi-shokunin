# T47ScribeSearchLog — round-47 F3 search-log note (scribe, leaf)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at base `0b5b7cd2`, freeze
`9acfbe21435e1976636a276448dee1d5e7155915`. Read first: `.ufo/evidence/round-47/contract.json`
(C3 surface, never edited), `CORPUS.md` rule 5, `corpus/SOURCES.md` `## Search log`
(lines 143–255) and `## Id allocation` (lines 279–303), `PROVINCE.md:1-16`. No counter ran, no
verdict was produced, no lane file other than this report and its note was written.

## Behavior — what was done

1. Read the frozen C3 surface and the pre-existing search-log entries to match their shape
   (question, where, date, identified/screened/included/excluded, exclusion reasons, stop).
2. Enumerated the package population with the item's own commands (below), then read every
   matched row in full (id, kind, tier, scope, anchor, teaches, status).
3. Resolved each row against the lane registry (`corpus/SOURCES.md`, 120 rows —
   `grep -cE '^[[:space:]]*\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`),
   the round-46 Gate (`corpus/lessons/round-46.md:6-70`), the tameshi quarantine slice
   (`.ufo/evidence/round-46/assimilation/quarantine-slice`) and the four rows this round
   adopts (`w1/T47ScribeRows.rows.md`: S261–S264).
4. Checked the two staged URLs whose exclusion would otherwise be unexplained (S171 DOI,
   S169 PDF) and the held PIT URL by live fetch, 2026-10-25, `curl -sS -o /dev/null -w
   '%{http_code} %{size_download}' --max-time 25 -L <url>`:
   - `https://www.juse.or.jp/sqip/workshop/report/attachs/2024/4_%E8%87%AA%E5%8B%95%E3%83%86%E3%82%B9%E3%83%88_%E6%9C%AC%E6%96%87.pdf` → `200 435007 application/pdf`
   - `https://doi.org/10.1109/TSE.2026.3685588` → `202 0 text/html; charset=UTF-8`
   - `https://pitest.org/faq/` → `200 20845 text/html; charset=utf-8`
5. Verified own-work anchors by path existence from the lane root and the fleet root
   (`os.path.exists` over every path token in the nine own-work anchors, scratch only).
6. Wrote the note and this report. Nothing was appended to `corpus/SOURCES.md`.

## Deliverable

`.ufo/waves/round-47/w1/T47ScribeSearchLog.note.md` — 5 physical lines, 0 pipe characters
(`grep -c '|' T47ScribeSearchLog.note.md` → 0). Text as written:

```
- 2026-10-25 — **round-47 bounded F3 search** (C3 assimilation). Question: which rows of
  theme F3 (flaky-aware verdicts, measurement half) can be opened and adopted this round?
  Where: the read-only package `shokuknow/merge/tameshi`, file `SOURCES.append.md`, run in
  that directory; F3-tagged rows plus the contract's fourth document (Lam et al.; staged
  S207, whose row is tagged F7). Counted 2026-10-25: `grep -cP '^ {0,3}\x7c S\d{3,}' SOURCES.append.md` gives 103 staged rows; `grep -cP '^ {0,3}\x7c S\d{3,}.*F3' SOURCES.append.md` gives 21 F3 rows; the pipe is written `\x7c` because this note carries no pipe character. Identified 21 · screened 22 · included 4 (S261, S262, S263, S264 by document) · excluded 18: 3 already adopted in round 46 (S190, S195, S216), 5 held duplicates (S160, S172, S202, S203, S225), 8 own-work rows whose lane and fleet receipt paths do not resolve (S180, S186, S193, S201, S208, S217, S219, S220), S171 unfetchable (DOI answers 202, 0 B), S169 outside the frozen document set (fetchable, 200, 435007 B). Quarantine 0 (the tameshi slice S105–S143 intersects none); province refusal 0. Stop: all 21 tagged rows screened; adoption frozen at four documents.
```

## Counts and the command that carries them

Run in `/home/vgpnk/Projects/shokuknow/merge/tameshi` on 2026-10-25, verbatim:

```
grep -cE '^ {0,3}\| S[0-9]{3,}' SOURCES.append.md                          # 103 staged rows
grep -E 'F3' SOURCES.append.md | grep -oE '^ {0,3}\| S[0-9]+'              # 21 ids, listed below
```

Output of the second command (21 lines, one id each):

```
S155 S158 S160 S169 S171 S172 S180 S186 S190 S193 S195 S201 S202 S203 S206
S208 S216 S217 S219 S220 S225
```

The note cannot carry that pipe, so it carries the equivalent pipe-free form, and both
were run:

- `grep -cP '^ {0,3}\x7c S\d{3,}' SOURCES.append.md` → 103
- `grep -cP '^ {0,3}\x7c S\d{3,}.*F3' SOURCES.append.md` → 21
- `grep -oP '^ {0,3}\x7c S\d+(?=.*F3)' SOURCES.append.md` → the same 21 ids.

Precision check (the broad `F3` grep cannot over-match): rows whose scope cell (field 6, the
tag column) contains `F3` = 21; rows whose body mentions `F3` only outside the scope cell =
none (`awk -F'|' '... if (s !~ /F3/ && $0 ~ /F3/) print $2'` → empty). So identified 21 is
both the command's output and the tag population.

Arithmetic: screened 22 = 21 tagged rows + the one contract-named document whose staged row
carries only an F7 tag (S207); included 4 = S155→S261, S158→S262, S206→S263, S207→S264;
excluded 18 = 3 + 5 + 8 + 1 + 1.

## Per-row dispositions — every F3-tagged staged row

Decision vocabulary: included (adopted this round), already adopted (round 46), held
duplicate, own-work anchor, fetchability, outside frozen set.

| staged | kind/tier | document (short) | decision | reason and evidence |
|---|---|---|---|---|
| S155 | paper/A | arXiv 2302.09330, flaky prediction from history | **included** | frozen document 1; adopted as S261 (`w1/T47ScribeRows.rows.md`, snapshot `arxiv-2302.09330-abs.html` sha256 `2965343c`); staged id collides with lane S155 (PIT basic concepts) and was re-pointed by document |
| S158 | paper/A | Lam et al. camera-ready PDF, rerun budget | **included** | contract's extra row; adopted as S262; staged id collides with lane S158 (PIT `DetectionStatus.java`); the quarantine register's S110 row is the same URL, payload-absent on the register's ASCII apostrophe, and the committed fresh snapshot `lam-2020-reruns.pdf` (sha256 `0b880458`) resolves it |
| S160 | docs/A | PIT FAQ `pitest.org/faq` | excluded — held duplicate | lane S156 is the same document (`§Is it random?`, `§Timeouts`, snapshot `.ufo/evidence/round-42/sources/pit-faq.html`, 20845 B, live URL re-fetched 200/20845 B today); lane S160 is a different document (Stryker equivalent mutants), so the staged id cannot be reused. The entry `flaky-aware-verdict-evidence.md` cites it; `w1/T47ScribeEntryPredict.md:46` already drops that quotation |
| S169 | talk/B | JUSE SQIP 2024 Japanese flaky-test talk | excluded — outside frozen set | not one of the four documents C3 freezes; the PDF is fetchable today (200, 435007 B), so this is a bounded-search exclusion, not a fetchability death; it stays a package lead |
| S171 | paper/B | IEEE TSE 2026 cross-project flakiness | excluded — fetchability | `https://doi.org/10.1109/TSE.2026.3685588` answers `202` with 0 bytes today; no abstract text is obtainable at the lane, so no located quote can be produced this round |
| S172 | own-work/A | repeat-control instrument + round-12 control snapshot | excluded — held duplicate | both anchors resolve in the lane: `tools/repeat-control.py`, `.ufo/evidence/round-12/ControlGate`; the lane already holds this material and the row adds no opened external source |
| S180 | own-work/A | repeat-control on the fleet regression leg | excluded — own-work anchor | instrument resolves, but the measured run lives at `/tmp/r3-rc` (absent) at revision `31687496`; nothing persisted to quote |
| S186 | own-work/A | repeat-control verdict + normalised re-diff | excluded — own-work anchor | anchor is a verdict string and a re-diff at revision `31687496` with no receipt path; no document exists to open |
| S190 | paper/A | IEEE TSE 2026 detected/undetected flaky failures | excluded — already adopted | round-46 Gate: admitted as lane S259 via the TUM portal record |
| S193 | own-work/A | env-diff receipt, round 6 | excluded — own-work anchor | `lanes/tameshi/round6/evidence/env-diff-norm-receipt.json` and `/tmp/r6/env-diff-norm.py` are absent at the lane root and at the fleet root (the lane has no round-6 evidence directory) |
| S195 | paper/A | arXiv 2504.16777 systemic flakiness | excluded — already adopted | round-46 Gate: admitted as lane S258 |
| S201 | own-work/A | env-diff run-id receipt, round 7 | excluded — own-work anchor | `lanes/tameshi/round7/evidence/env-diff-runid-receipt.json`, `.../env-diff-runid.py` and the round-6 contract are all absent; the lane has no round-7 evidence directory |
| S202 | docs/A | GoogleTest `docs/advanced.md` @ `cd8e73f0` | excluded — held duplicate | lane S256 is the same pinned document (round 45) |
| S203 | docs/A | GoogleTest `docs/primer.md` @ `cd8e73f0` | excluded — held duplicate | lane S257 is the same pinned document (round 45) |
| S206 | paper/A | arXiv 2607.09345 code-based detection limits | **included** | frozen document 2; adopted as S263 (snapshot `arxiv-2607.09345-abs.html` sha256 `16ecdefc`) |
| S208 | own-work/A | env-diff width sweep, round 8 | excluded — own-work anchor | contract path `lanes/tameshi/round6/evidence/env-diff-contract.json` absent; the lane has no round-8 evidence directory |
| S216 | docs/A | Google Testing Blog per-post JSON record | excluded — already adopted | round-46 Gate: admitted as lane S260, with the honest note that the rendered post is already lane S026 |
| S217 | own-work/A | repeat-control on a constant-assertion control | excluded — own-work anchor | the anchor's `lanes/tameshi/round10/evidence/q4/` receipts do not exist (no round-10 evidence directory); only `tools/repeat-control.py` resolves |
| S219 | own-work/A | six-surface receipts re-measured, round 10 | excluded — own-work anchor | the round-10 receipt set does not exist at the lane or the fleet root; only the instrument resolves |
| S220 | own-work/A | F1 interop chain run under two PATH conditions | excluded — own-work anchor | the round-10 `evidence/f1/` receipts do not exist at the lane or the fleet root |
| S225 | docs/A | same per-post feed record, re-opened | excluded — held duplicate | round-46 Gate names S216/S225/S229/S235 as one document and adopted S260; the lane also holds the rendered post as S026 |
| S207 | paper/B | Semantic Scholar record of DOI 10.1109/ICST60714.2024.00037 | **included** (outside the tag set) | not matched by the F3 grep — its scope cell reads "F7's cost baseline in money and time"; the contract assigns the document to F3's cost half, so it is screened and adopted as S264 (snapshot `s2-icst24-cost-of-flaky.json`); recorded so the counts stay reproducible from the command |

Exclusion reasons present: already adopted in round 46 (3), held duplicate (5), own-work
anchor (8), fetchability (1), outside frozen set (1). Quarantine 0: the tameshi slice is 17
rows (S105–S143, `wc -l` on `.ufo/evidence/round-46/assimilation/quarantine-slice` = 17) and
`comm -12` against the 21 ids prints nothing; its S110 row is the Lam document and is
resolved by the fresh snapshot, not a live quarantine. Province refusal 0: every tagged row
is verdict/method scope, which `PROVINCE.md:1-16` ("verification-fixture craft … verdict-line
discipline") owns; none is a product domain, credential material or endpoint health.

## Gates and bounds observed

- Read-only on the lane: the only files written are `.ufo/waves/round-47/w1/T47ScribeSearchLog.md`
  (this report) and `T47ScribeSearchLog.note.md`. `corpus/SOURCES.md` was read, never edited.
- No git or jj command ran in the lane; no mutating command of any kind; the read-only package
  `/home/vgpnk/Projects/shokuknow` was only read (grep/read; three `curl` fetches of public URLs).
- No counter ran (no `--selftest`, no `--only`, no verdict); no score or pass line is claimed.
- Scratch: `/tmp/tameshi-r47-T47ScribeSearchLog/` (`f3rows.txt`, `f3.ids`, `slice.ids`).
- Tools: nothing installed or upgraded; `pacman` untouched; `grep`, `awk`, `curl`, `python3`
  were already present; no model was passed anywhere.
- No subagent was spawned (leaf member); no `agent://all` message.

## Findings

1. **The item's four documents are not four F3-tagged rows.** The tag command returns 21 rows
   and S207 is not among them; its scope cell tags F7 only. Counting "identified" as the
   command's 21 and "screened" as 22 (the four documents plus the rest) keeps both the
   count reproducible and the population complete; a future log that writes "identified 22"
   from this command would be unreproducible.
2. **The suggested command and the no-pipe rule collide.** The note therefore carries the
   `grep -P` form with `\x7c` for the pipe; the two forms were run here and print identical
   numbers (103 and 21). The verbatim pipe form is preserved in this report.
3. **Lane id collision risk is broader than S155/S158.** Staged S160 also collides with a
   held lane id (PIT FAQ in the package vs Stryker equivalent mutants in the lane), and the
   package's own S160 is a fifth document the contract does not adopt. Entry authors already
   drop it (`w1/T47ScribeEntryPredict.md:46`); the re-point S160→S156 is the only honest
   option if any later entry wants that paragraph.
4. **The own-work rows are not openable sources.** Eight of the nine name receipts under
   `lanes/tameshi/round{6,7,8,10}/…` or `/tmp/…` that exist nowhere on this host (the lane's
   evidence directories start at `round-12`); they can ground nothing this round, and they
   were not counted as fetchability failures because their subject (the lane's own
   instruments) is lane-local and already partly held.
5. **Quarantine carries no live refusal for this theme.** The only document-level overlap
   (S110 = Lam PDF) was a lossy-fold artifact cured by the fresh snapshot; the search log
   should say "quarantine 0" rather than inherit the register's payload-absent status.

## Conflicts reported verbatim (for the canonical judge)

- Package row S207 scope cell: `F7's cost baseline in money and time — the quantity a re-sweep cadence`
  — against the assignment's framing that this document is an F3 row.
- Quarantine register row S110: `payload-absent`, URL
  `https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf`, quote
  `one can use ≤ 5 reruns (50% less than Google's default ten reruns [6]) and still check correctly ≥ 82% of the time.`
  — against the fresh PDF snapshot (sha256 `0b880458…`) in which the same sentence is contiguous
  under the PDF's curly apostrophe `Google’s`.
- Lane registry line 303: `Next unused id: S265 (S261–S264 are map-only reserved; staged ids S161–S255 stay reserved by document for the package).`
  — the four ids adopted this round are exactly those reserved ones, so no new reservation is needed.

## Out of scope (not done)

- No registry append, no id allocation decision beyond recording S261–S264, no entry rewrite,
  no re-grade of any tier, no counter run, no verdict, no commit.
- S169 was not adopted or rejected as false: it is a bounded-search exclusion only.
- The other 82 staged rows (103 − 21) were not screened; the query was bounded to the F3 tag
  and the one contract-named document.

## Artifact paths

- `.ufo/waves/round-47/w1/T47ScribeSearchLog.note.md` (deliverable note)
- `.ufo/waves/round-47/w1/T47ScribeSearchLog.md` (this report)
- `/tmp/tameshi-r47-T47ScribeSearchLog/f3rows.txt`, `f3.ids`, `slice.ids` (scratch)
