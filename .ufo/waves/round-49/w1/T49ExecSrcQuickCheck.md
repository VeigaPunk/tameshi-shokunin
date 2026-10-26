# T49ExecSrcQuickCheck — C2 source snapshot: QuickCheck (ICFP 2000, DOI 10.1145/351240.351266)

Seat: leaf source-snapshot executor, tameshi round 49, wave 1. Base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Item: open and snapshot the primary QuickCheck paper, pin its bytes, and locate the five named passages
verbatim (≤ 25 words) with page/section. No counter was run, no claim is decided, no lane file was edited.

Deliverables written (only these paths):

- `.ufo/waves/round-49/w1/T49ExecSrcQuickCheck.json` — the required `{url, carrier, sha256, quotes[]}` record (11 quotes, 5 topics).
- `.ufo/waves/round-49/w1/T49ExecSrcQuickCheck/` — `quickcheck-icfp00-icfp-2000-course-copy.pdf` (194315 B), `…​.pdftotext.txt`
  (83836 B), `fetch-receipt.json`, `crossref-10.1145-351240.351266.json`, `doi-resolution-headers.txt`,
  `excerpt-check.txt`, and three rendered page crops (`render-p1-abstract.png`,
  `render-p3-classify-ligature.png`, `render-p3-customgen-ligature.png`).

## 1. Carrier: published article text, third-party course mirror (not a preprint)

```
curl -sS -L -D doi-headers.txt -o doi-body.html -w '%{http_code} %{url_effective}\n' 'https://doi.org/10.1145/351240.351266'
   -> 302 https://dl.acm.org/doi/10.1145/351240.351266
   -> 403 https://dl.acm.org/doi/10.1145/351240.351266   (text/html, 5465 B)      # receipt: T49ExecSrcQuickCheck/doi-resolution-headers.txt
curl -sS -L -o tufts-quick.pdf -w '%{http_code} %{url_effective} %{size_download} %{content_type}\n' \
  'https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf'
   -> 200 https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf 194315 application/pdf
sha256sum quickcheck-icfp00-icfp-2000-course-copy.pdf
   -> bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172
pdfinfo -> 12 pages, 612x792, Creator dvipsk 5.58f, Producer GPL Ghostscript 9.04, CreationDate 2012-09-04
qpdf --check -> No syntax or stream encoding errors found
```

Evidence that these bytes are the **published article**, not a preprint:

- `quickcheck-icfp00-icfp-2000-course-copy.pdftotext.txt` page 1 ends with the ACM block
  `ICFP '00, Montreal, Canada.` / `Copyright 2000 ACM 1-58113-202-6/00/0009 .. 5.00` plus the
  "Permission to make digital or hard copies … for personal or classroom use" notice — i.e. the ACM
  camera-ready/VOR page furniture, and the copy is lawfully redistributable for classroom use.
- 12 pages, matching Crossref for this DOI: `https://api.crossref.org/works/10.1145/351240.351266`
  → `page: "268-279"`, `container-title: "Proceedings of the fifth ACM SIGPLAN international conference on
  Functional programming"`, `published-print: 2000-09`, `content-version: "vor"` (receipt:
  `T49ExecSrcQuickCheck/crossref-10.1145-351240.351266.json`).
- no preprint markers: `grep -in 'arxiv\|preprint\|submitted\|manuscript' <pdftotext>` → only a reference
  title (`[18] Philip Wadler. A prettier printer, March 1998. Draft`, line 711), no arXiv id, no TR number.
- abstract text matches the string S182 quotes (`Properties are described as Haskell functions …`), confirmed
  on the rendered page (`render-p1-abstract.png`).

**What that means for tier.** Tier A still holds for the *text*: the passages are the published article's
words (VOR per Crossref, ACM notice on the carrier), so §-level citation is sound. Two caveats the L1 should
carry into SOURCES:

1. **The carrier is a mirror, not the publisher.** `sha256 bfddcaa6…` pins *the Tufts CS257 copy*; the ACM DL
   bytes were not obtainable from this host (403, above). A pin on a third-party mirror is weaker than a pin
   on the DOI-served PDF, and the mirror was re-rendered in 2012 (dvipsk 5.58f / Ghostscript 9.04), so it is not
   the 2000 typesetting.
2. **The printed proceedings folios are not on the carrier.** `grep -c '268\|279' <pdftotext>` → `0`; only
   footnote markers `1` and `2` appear as page footers. Page numbers 268–279 come from the DOI/Crossref record,
   and the mapping used here is `PDF page n = printed 267+n` (n=3 → p. 270, n=7 → p. 274, n=10 → p. 277).

**Row-level observation for S182 (report only, not an edit).** S182
(`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:36`) says "the article text was retrieved by
DOI resolution on 2026-10-23" and locates the row at "§Abstract and §1 Introduction". Two mismatches with what
this host can reproduce today: (a) a bare DOI resolution returns **403**, so that retrieval route is not
reproducible here without a browser/session (softened by the fact that the abstract string is verbatim in this
carrier); (b) the F10-bearing statements are **not** in §Abstract/§1 — they are in §2.1, §2.4, §3.2, §5.1.4 and
§6.3 (quotes below), so the row's location field understates the citation.

## 2. Extraction artifact (ligatures) and how quotes were verified

`pdftotext -layout` on this Type1-encoded PDF loses ligatures: `fi`/`fl` extract as *nothing* (`de ne` = define,
`classi es` = classifies, `speci cation` = specification), and `ffi` arrives as control byte `0x0e`
(`ine\x0ecient` = inefficient, `di\x0eculty` = difficulty; 13 occurrences). Rendering the page and reading the
glyph was used as authority for every quote containing such a word:

```
pdftoppm -r 200 -f 3 -l 3 -png -x 880 -y 400 -W 860 -H 500 tufts-quick.pdf p3-customgen   # "define his or her own test data generators"
pdftoppm -r 200 -f 3 -l 3 -png -x 0   -y 800 -W 860 -H 620 tufts-quick.pdf p3-classify    # "…but it classifies some of the test cases"
pdftoppm -r 200 -f 1 -l 1 -png -x 60  -y 600 -W 820 -H 420 tufts-quick.pdf p1-abs2        # abstract sentence
```
→ copies kept as `render-p3-customgen-ligature.png`, `render-p3-classify-ligature.png`, `render-p1-abstract.png`.

Automated location check (`T49ExecSrcQuickCheck/excerpt-check.txt`, produced by the script in that file's header;
column-cropped with `pdftotext -f P -l P -x {0|306} -W 306 -H 792 -layout`, `0x0e`→`ffi`, hyphens joined,
whitespace removed, `fi`/`fl` tolerated as absent):

```
RESULT: 11/11 quotes located in the pinned bytes; sha256(pdf)=bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172
word-limit: max 23 words (limit 25); topics = controlling_size, custom_test_data_generators,
            generator_choice_pitfalls, observing_test_data_distribution, properties_as_testable_functions
```

## 3. The five requested passages (verbatim, location, words)

Column-cropped text is at `<pdftotext>.txt` page P; the column crops used for each check are reproducible with
the `pdftotext -x/-W` command above.

| # | Topic | Quote (≤ 25 words) | Location | w |
|---|---|---|---|---|
| 1a | properties as testable functions on random input | "Properties are described as Haskell functions, and can be automatically tested on random input" | §Abstract, p. 268 (PDF p1), left col, sentence 2 | 14 |
| 1b | same | "The function quickCheck takes a law as a parameter and applies it to a large number of randomly generated arguments" | §2.1 A Simple Example, p. 269 (PDF p2), left col, after `OK: passed 100 tests.` | 20 |
| 2a | custom test data generators | "The best solution, though, is to replace the condition with a custom test data generator for ordered lists." | §2.4 Monitoring Test Data, p. 270 (PDF p3), right col, opening sentence | 18 |
| 2b | same | "QuickCheck provides support for the programmer to define his or her own test data generators, with control over the distribution of test data" | §2.4, p. 270 (PDF p3), right col, penultimate paragraph (after the `forAll orderedList` example) | 23 |
| 3a | observing the test-data distribution | "The combinator collect will gather all values that are passed to it, and print out a histogram of these values." | §2.4, p. 270 (PDF p3), left col, after the `classify` example | 20 |
| 3b | same | "The classify combinator does not change the meaning of a law, but it classifies some of the test cases" | §2.4, p. 270 (PDF p3), left col, under `OK, passed 100 tests (43% trivial).` | 19 |
| 4a | controlling size (`sized`) | "sized generates an a by passing the current size bound to its parameter" | §3.2 Generators for User-Defined Types, p. 271 (PDF p4), right col, under the `sized :: (Int -> Gen a) -> Gen a` declaration | 13 |
| 4b | same | "It is then up to the programmer to interpret the size bound in some reasonable way during test data generation." | §3.2, p. 271 (PDF p4), right col, next sentence | 20 |
| 5a | pitfalls of generator choice | "it seems to be very hard to construct a generator for a type, without knowing something about the desired distribution of test cases" | §3.2, p. 271 (PDF p4), left col (why `Arbitrary` instances are not auto-derived) | 23 |
| 5b | same | "the false sense of security that can be engendered when one's program passes a large number of tests in trivial cases" | §5.1.4 A False Sense of Security, p. 274 (PDF p7), left col, first sentence | 21 |
| 5c | same | "Our experience is that this results in far too high a proportion of trivial test cases, and therefore inefficient testing" | §6.3 Test Data Generation, p. 277 (PDF p10), left col (verdict on grammar leaf-probability generators) | 20 |

Notes on the passages, as read (no interpretation beyond the sentence):

- §2.4's whole argument is that a *large* pass count hides a degenerate input distribution: `classify` (3b) then
  `collect` (3a) expose it, and the section ends by recommending a custom generator (2a/2b) over an implication.
- §3.2 makes generator quality the programmer's responsibility (5a) *because* distribution knowledge is
  type-specific, and gives `sized` (4a/4b) as the only size control, with the size bound deliberately global
  ("every use of sized sees the same bound", §3.2 p. 271) so parts do not correlate.
- §5.1.4 and §6.3 are the pitfall statements (5b: >95% of pre-condition-satisfying unification cases were the
  trivial "one term is a variable" shape; 5c: grammar tuning toward leaves yields trivial cases and inefficient
  testing).

## 4. Relevance to C2 (the generator item; this seat decides nothing)

The claim's predicate asks for a real class floor (each of 12 frozen classes ≥ 10 cases of 400) and an
independent oracle. The paper supplies exactly that vocabulary: properties are functions over generated input
(1a/1b), a *custom* generator per type (2a/2b), and distribution must be *observed*, not assumed (3a/3b) —
with the failure mode of a passing suite that only exercised trivial cases named outright (5b/5c). The `sized`
material (4a/4b) is the paper's answer to the run-time cost of unbounded generation, which is the shape the
`--cases 400` budget has to live in. These are the quotes `corpus/knowledge/pbt-generator-pilot.md` can cite as
an SOURCES row opened 2026-10-26 for F10; the row itself (S182) and its tier are the L1's to re-score.

No claim, control or counter verdict is offered here. No `--selftest`/`--list` invocation of any round-49 counter
was made (no counter is in scope for this item).

## 5. Blockers, risks, non-actions

- **ACM DL 403.** Publisher bytes unobtainable from this host (`doi-resolution-headers.txt`); the snapshot is a
  classroom-permitted mirror. If the L1 wants a publisher-served pin, that needs a browser/campus session — not
  reachable from this seat.
- **Page folios absent on the carrier** (§1 caveat 2), so all printed page numbers in the table are Crossref-derived.
- **`aaron` CLI not used.** `skill://aaron` was read; `aaron papers fetch <doi>` would write into `~/aaron-library`
  (outside this seat's allowed write paths) and its fallback retrievers are not appropriate here, while the course
  copy returned the full article in one request. No tool was installed or upgraded (host pacman transactions are
  paused anyway; nothing was needed).
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49ExecSrcQuickCheck` was used for the fetch and the column crops and is
  deleted before yielding; every cited receipt is a copy inside `.ufo/waves/round-49/w1/`.

## Summary

1. QuickCheck ICFP 2000 snapshotted: 194315 B, 12 pp., `sha256 bfddcaa648f836e50804910fc0956cc037c1a8b3e3d6716fb12e4e1ffdcb5172`, HTTP 200 from the Tufts CS257 course archive.
2. Carrier is the **published article's text** (ACM copyright block, ICFP '00 line, Crossref `vor`, 268–279, no preprint markers), served by a third-party mirror — tier A for content, mirror-level pin.
3. ACM DL refused the DOI landing page (302 → 403), so the publisher's own bytes are not what was pinned; carrier caveat recorded for S182.
4. Carrier prints no proceedings folios (`grep -c '268\|279'` = 0); page numbers are inherited from Crossref, mapping `PDF page n = printed 267+n`.
5. All five requested topics located verbatim, 11 quotes, max 23 words, each with section + page + column; `excerpt-check.txt` reports 11/11 located in the pinned bytes.
6. Ligature extraction artifact documented and defeated: `fi`/`fl` vanish, `ffi` = byte `0x0e`; three rendered page crops are the authority for `define`, `classifies`, `inefficient`.
7. S182's location field ("§Abstract and §1") misses where the F10 material actually sits (§2.4, §3.2, §5.1.4, §6.3) — flagged for the L1, not edited.
8. No counter run, no claim decided, no lane file touched; deliverables are `T49ExecSrcQuickCheck.json` plus seven receipt files (pdf, pdftotext, fetch receipt, Crossref JSON, DOI headers, excerpt check, three page renders) under `T49ExecSrcQuickCheck/`.
