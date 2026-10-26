# T49W2RevRows — SOURCES rows re-open (round 49, wave 2, falsify)

Seat: T49W2RevRows. Item: re-open each SOURCES row the round appended (S269, S270; diff
`git -C <lane> diff 8ca674211111fa354b47b803358391d0b07fc6db9 f181a961ae44061af486f600e5ea257d2baf78f8 -- corpus/SOURCES.md`
= 5 insertions, 0 deletions: rows S269/S270 at corpus/SOURCES.md:144-145 + three appended note lines at :492-494).
Base `8ca67421`, candidate `f181a961`. Live bytes == candidate bytes:
`git -C <lane> diff --stat f181a961 HEAD -- corpus` → empty; `git status --porcelain -- corpus | wc -l` → 0;
`cmp` live vs candidate round-49.md → IDENTICAL; live vs candidate SOURCES.md → SOURCES-IDENTICAL.
Read-only seat: no counter runs, no verdicts; scratch `/fast/scratch/hyaku/tameshi-r49/T49W2RevRows/` (deleted before yield).
No tools installed or upgraded (used host pdftotext/pdfinfo 26.08.0, curl, python3, gawk via the fleet census script).

## Re-open result: both rows verified against today's bytes; 3 low findings, 3 informational

### 1. Fresh fetch today vs committed snapshot and receipts — PASS
```
curl -sSL 'https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf'   → 200, application/pdf
curl -sSL 'https://smallbone.se/papers/lic.pdf'                               → 200, application/pdf
sha256sum → bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172  quick-today.pdf (194315 B)
             eaee48f930ba20a06824fe238cc6a42427e9fb45d1d70b852bf091ad6e44ac08 smallbone-today.pdf (1269821 B)
```
Identical to the committed snapshots (blob `4431a878`/`43c5a98c` at f181a961, sha256 equal to working copies) and to all
three wave-1 receipts (w1/T49ScribeRows.src/fetch-receipts.json; w1/T49ExecSrcQuickCheck/fetch-receipt.json 20:32:41Z;
w1/T49ExecSrcSmallbone/receipt.json 20:32:43Z — the Gate's "independent fetches, identical sha256" holds).

### 2. Gate quotes located in live bytes and snapshot — PASS (contract rule 1)
Lesson `corpus/lessons/round-49.md` `## Gate` (lines 18-27), quote word counts verified 20/14/19 ≤ 25:

| row | quote (words) | claimed location | located at (today's fetch == snapshot, sha256-equal) |
|---|---|---|---|
| S269 | "The combinator collect will gather all values that are passed to it, and print out a histogram of these values" (20) | §2.4 Monitoring Test Data, p. 270 | PDF p. 3, verbatim ✓ |
| S269 | "Properties are described as Haskell functions, and can be automatically tested on random input" (14) | Abstract, p. 268 | PDF p. 1, verbatim ✓ |
| S270 | "As always with random testing tools, the quality of the test data determines the quality of the generated equations" (19) | §2.10, printed p. 34 (PDF p. 39) | PDF p. 39 (folio line "34"), verbatim ✓ |

Page mapping proven: `pdftotext` full split → PDF p. 39 first line is folio "34" and holds "2.10 Generating Test Data";
PDF p. 34 is folio "29" (different content) — the lesson's "(PDF p. 39)" parenthetical is exact.
Pilot entry `corpus/knowledge/pbt-generator-pilot.md` quotes also all located: §2.4 collect + "QuickCheck provides
support … distribution of test data" (PDF p. 3), §3.2 `sized` "generates an a by passing the current size bound to its
parameter" + "It is then up to the programmer to interpret the size bound…" (PDF p. 4), §5.1.4 heading "A False Sense of
Security" + "the false sense of security that can be engendered…" (PDF p. 7), S270's three §2.10 spans (PDF p. 39).
DOI/citation apparatus: committed crossref.json sha256 e1ba3955… (as cited in fetch-receipts.json) → DOI 10.1145/351240.351266,
"QuickCheck", ICFP00, pages 268-279; 12 PDF pages ↔ pp. 268-279 consistent. Pilot recheck commands reproduce:
`pdftotext …smallbone.pdf - | tr -s ' \n' ' ' | grep -c 'that fit the program at hand'` → 1; same over quick.pdf for
`print out a histogram of these values` → 1.

### 3. Cells and schema — PASS
11-column schema (contract v1); census full-tree validate exit 0 → 0 malformed rows, enums ok, no `|` in cells.
kind=paper (enum ✓); tier A (original paper, S269) and B (author's own report, S270) within contract definitions —
B is conservative, no inflation; status=mined backed by used-by `corpus/knowledge/pbt-generator-pilot.md`, which exists,
cites both rows (pilot.md:1-2), and no other knowledge entry cites them (tree grep at f181a961); opened=2026-10-26 in both
cells (contract C2 "sourced" requirement ✓; fetch receipts 20:32-20:33Z same day); recheck=365d, valid cadence;
append-only respected (0 deleted lines; lesson's "Rows touched old → new: none" true).
Id ceiling: max registry id at candidate = S270 → note line "Next unused id: S271" correct. Collision receipts match the
Gate and the :493 note line: `wc -l reg-ids` = 128 (128 unique), `wc -l staged-ids` = 103, `collisions` = exactly
S153-S160 (8), none on S182/S183; collision-probe.out = "0-3-space extractor collision set: S153-S160 plus S182" (9) and
"column-0 extractor collision count: 8" — the Gate's guard proof verbatim.
S270 anchor-correction note (":145, not the package's §4.1 p. 44") true: PDF p. 49 (folio 44) is §3.4 "Problems with
Partiality", `grep -ci generator` → 0 (only regex hit is the subsection number "3.4.1"); headings-4.1.out shows the only
'4.1' §-headings are elsewhere (A Parallel Correctness Criterion / Automatic Ranking of Solutions).

### 4. Census — no new finding from the round
Prescribed invocation (corpus-only mirror):
`git archive f181a961 corpus | tar -x -C $S/v && scripts/sources-census.sh validate --file $S/v/corpus/SOURCES.md`
→ exit 1, 18 findings. Same-shape base mirror → exit 1, identical 18 findings (diff empty; the earlier 15-line base run
differed only because that base mirror accidentally had tools/). Full-tree mirrors: exit 0 at f181a961 and at base,
outputs identical except the path line. So every W04/W01/E11 is pre-existing (rounds ≤48 rows); S269/S270 add none, and
the contract's no_harm census claim (full-tree exit 0) stands. The corpus-only exit 1 is mirror-shape (E11 = used-by path
absent because tools/ is not in a corpus-only archive) — recorded so the exit code is not misread.

## Findings

**F1 (low, row wording) — S269 anchor mislabels the carrier "author-served PDF".**
corpus/SOURCES.md:144 (anchor cell): "author-served PDF fetched 2026-10-26". The pinned URL
`https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf` is a third-party university course mirror
(`~nr` = Norman Ramsey's CS257 archive), and the round's own Gate says so:
corpus/lessons/round-49.md:21 — "on a course mirror; the ACM DL answered 302 → 403, so the publisher's own bytes are not
the pin." The row contradicts the lesson and inflates provenance. (S270's "author-served" is correct — smallbone.se.)
Contract rule 2 bars in-place anchor edits; proportionate fix is an appended note (or a superseding row if the closure
wants it mechanical). Shows: `sed -n '144p' corpus/SOURCES.md | grep -o 'author-served PDF'` vs
`sed -n '21p' corpus/lessons/round-49.md`.

**F2 (low, factual) — S270 anchor says "117 pp"; the committed PDF has 116 pages.**
corpus/SOURCES.md:145: "author-served PDF 117 pp fetched 2026-10-26". Commands on the committed snapshot
`.ufo/waves/round-49/w1/T49ScribeRows.src/smallbone.pdf`: `pdfinfo … | grep -i '^pages'` → "Pages: 116";
`pdftotext -f 116 -l 116 … - | grep -m1 -E '^[0-9]{2,3}$'` → folio "111" (last printed number);
`pdftotext … - | grep -c 117` → 0 ("117" appears nowhere in the document). Wave-1's own committed receipt records
`pdfinfo.pages: 116` (w1/T49ExecSrcSmallbone/receipt.json). Likely a pdftotext form-feed chunk miscount (117 splits).

**F3 (low, lesson wording) — Gate overstates S269's anchor.**
corpus/lessons/round-49.md:44-45: "…so S269's anchor names §2.4 and §3.2 as well". The row's anchor
(corpus/SOURCES.md:144) names "Abstract, first paragraph (p. 268) and §2.4 Monitoring Test Data (p. 270)" — no §3.2;
§3.2 is cited by the pilot entry's source line (corpus/knowledge/pbt-generator-pilot.md:1), not the row anchor.
Shows: `sed -n '144p' corpus/SOURCES.md | grep -c '§3.2'` → 0.

**F4 (informational) — used-by completeness is convention-dependent.**
used-by lists only the pilot entry, but corpus/lessons/round-49.md:8-9,18-27 (Gate) and the README note table
(corpus/README.md:597, Sources cell "S269, S270") also cite the rows. Contract text (SOURCES-CONTRACT-v1.md): used-by =
"knowledge entries or lessons citing the row". Same-round-Gate exclusion follows the round-48 precedent (round-48.md
cites S265-S268 at base; their used-by omit the lesson), and the census validator checks only that used-by paths exist,
not completeness — but README citing rows in a note-table Sources cell is new in round 49. Closure may want one sentence
settling whether README/lesson citations belong in used-by. No correctness impact on the rows' claims.

**F5 (informational, provenance) — an intermediate Sci-Hub-resolved fetch is disclosed only in a w1 receipt.**
w1/T49ScribeEntryDraft.quickcheck-receipt.txt:4-8 (committed at f181a961) records `aaron papers fetch 10.1145/351240.351266`
resolving tier=scihub (mirror sci-hub.ee, pdfBytes 313371) with an explicit "PROVENANCE CAVEAT … recorded not smoothed".
The row/Gate pin the Tufts course-mirror bytes, and this seat re-located every quote on the pinned bytes today, so no
claim rests on the shadow-library copy; the lesson's provenance narrative (ACM 302→403 → course mirror) just never
mentions the probe. Awareness only.

**F6 (informational, tooling) — prescribed census invocation exits 1; not caused by the round.**
See §4: identical finding sets base vs candidate under same-shape mirrors; full-tree validate exit 0 at both revisions.
Every finding names pre-existing rows (S047/S048/S075-S092/S101/S104/S160/S265-S268); S269/S270 appear in none.

## Residual risk and verification gaps
- Journal pages 268/270/271/274 for S269 rest on Crossref pagination + a 12-page author copy that prints no journal
  folios; the offset-0 mapping (PDF p.1 = p.268) is consistent with Crossref pages 268-279 but not independently
  folio-verifiable. §-heading and quote locations were verified directly.
- Tier B vs A for S270 is curation judgment (an author's licentiate thesis could argue A as "maintainer statement"); the
  census does not police it and the row's scope sentence discloses the reading.
- F4 is a policy reading, not a mechanical violation; the validator cannot arbitrate it.
- C2's deciding run, hidden panel, and generator quality are other seats' scope; nothing here ran a counter or is a verdict.

## Summary
- Re-opened S269/S270 (the round's only appended rows): both URLs fetched today return bytes sha256-identical to the
  committed snapshots and all three wave-1 receipts.
- All three lesson-Gate quotes (20/14/19 words, ≤25) and every pilot-entry quote locate verbatim at their claimed
  pages/sections in live bytes (== candidate) and snapshot; S270's "printed p. 34 (PDF p. 39)" mapping proven exact.
- Cells pass: 11-column schema, kind/tier/status/opened/recheck valid, used-by path exists and is the sole knowledge
  entry citing the rows, append-only intact, id ceiling S271 correct, collision receipts (128/103/8) match the Gate.
- Census: zero new findings from the round (full-tree exit 0; corpus-only exit 1 is pre-existing rows + mirror shape).
- Findings: F1 SOURCES.md:144 "author-served" is a course mirror (row contradicts lesson:21); F2 SOURCES.md:145 "117 pp"
  is 116 pages (receipt itself says 116, folios end 111); F3 round-49.md:45 claims an anchor that names no §3.2.
- Informational: used-by convention vs lesson/README citations (F4); committed Sci-Hub-probe disclosure lives only in a
  w1 receipt (F5); prescribed census exit code explained (F6).
- No finding voids a row, the Gate, or claim C2's sourced predicate; fixes are two-word/one-line note-grade corrections
  for the L1 to route.
