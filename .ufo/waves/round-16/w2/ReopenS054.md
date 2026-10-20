# ReopenS054 — re-opening S054 (Diátaxis: the compass)

Seat `TameshiR16.ReopenS054` (scout) · round 16, wave 2 · lane commit
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` · 2026-10-20 · scratch
`/tmp/tameshi-r16w2-ReopenS054-YoxeF3`.

Target: re-open <https://diataxis.fr/compass/>, compare against its row
`corpus/SOURCES.md:63` and its Gate quote `corpus/lessons/round-16.md:35`, and
rule each field holds/falls.

**Verdict line: holds on every field — quote exact and 17 words at §The compass
¶22, anchor reproducibly resolvable on byte-identical bytes, tier/kind/scope/
teaches grounded, used-by path present and citing S054; three non-blocking
precision notes (C1–C3).**

## Axes (godspeed)

- **A1 quote fidelity** — the Gate string must be the page's rendered text at
  the stated location, ≤25 words.
- **A2 anchor resolvability** — `§The compass ¶22` must land on that paragraph
  for a re-opener using the lane's counting convention, at the named revision.
- **A3 field justification** — kind/tier against the frozen contract, scope and
  teaches against page text.
- **A4 used-by substantiation** — the path must exist and cite the row.

## 1. Fetch (observed, 2026-10-20)

`curl -sS -D hdr.txt -o compass.html https://diataxis.fr/compass/` → exit 0.

| item | observed |
|---|---|
| status | `HTTP/2 200` |
| `date` | `Tue, 20 Oct 2026 13:51:43 GMT` |
| `last-modified` | `Thu, 06 Aug 2026 07:20:44 GMT` |
| `etag` | `W/"a801230224ee010cbbfc21e2019399f3"` |
| bytes | 20288 |
| sha256 | `8597a5b13f235ddff56b24b234745fd46ba9a115af2b165b1f4e59b82514e1a0` |

All four revision markers (bytes, sha256, ETag, Last-Modified) are identical to
the round's own wave-1 fetch of the same URL
(`.ufo/waves/round-16/w1/CRSource.md:22`). Today's re-open is therefore the
same revision the row names, not a new snapshot — the row's
`Last-Modified 2026-08-06` is confirmed by header.

## 2. Stated location: `§The compass ¶22`

HTML structure in the fetched bytes: `<section id="the-compass">` at
`compass.html:277`, `<h1>The compass<a class="headerlink" href="#the-compass">¶`
at `:278`, `<section id="using-the-compass">` at `:329`. The quote precedes the
H2, so it is inside §The compass under either reading of the section boundary
(to-next-heading or to-end-of-DOM-section).

Counting `<p>` elements from `<section id="the-compass">`:

- paragraph 22 is exactly
  `To use the compass, just two questions need to be asked: action or cognition? acquisition or application?`
  (`p22==quote` → `True`; the section contains 35 `<p>` elements and the quote
  occurs in exactly one of them);
- word count 17 (≤25).

Exactness is **text-exact**: in the raw bytes the same sentence is
`<p>To use the compass, just two questions need to be asked: <em>action or cognition?</em> <em>acquisition or application?</em></p>`
(`compass.html:327`), so a naive byte-substring check fails on the two `<em>`
tags — they are the page's emphasis, not words, and the rendered text equals the
Gate string character-for-character.

The convention is not S054's invention: the same wave-1 census's D1
(`§The compass ¶5`) resolves to the truth-table intro paragraph, and D3
(`§Using the compass ¶12`) resolves to the local 12th paragraph
("…close-up, at the level of sentences and words, or from a wider
perspective…"). Both reproduce exactly, so ¶ numbers in this round mean "index
of `<p>` elements inside the section".

**C1 (minor, non-blocking).** 15 of those 22 `<p>` elements are the compass
truth-table's cell paragraphs; counting prose paragraphs only puts the quote at
¶7 (10 prose paragraphs precede the H2). ¶22 is deterministic for a DOM
paragraph counter, but the row never states the counting rule, so a hand
counter can land elsewhere. Fix, if wanted: append the paragraph's opening
words to the anchor (e.g. `§The compass ¶22 “To use the compass…”`).

## 3. Field-by-field verdict

Row text quoted from `corpus/SOURCES.md:63`; Gate row from
`corpus/lessons/round-16.md:35`.

| field | row value | check performed | verdict |
|---|---|---|---|
| id | `S054` | no duplicate id (`uniq -d` filtered to S054 → 0); NF=13 | holds |
| source | `Diátaxis: the compass — https://diataxis.fr/compass/` | URL returns 200; H1 `The compass`; site is Diátaxis's own documentation (`<meta name="author" content="Daniele Procida">`; `Copyright © Daniele Procida`) | holds |
| kind | `docs` | contract enum includes `docs`; page is the framework's documentation | holds |
| tier | `A` | contract: A = "primary or authoritative for that scope (… official docs …)"; this is the framework author's own statement of the classification instrument, scoped exactly to that instrument | holds |
| scope | `separating instruction (how-to) content from record/reference content at section granularity` | compass table has the exact pair: how-to = `informs action` + `application of skill`; reference = `informs cognition` + `application of skill`; Q1 alone separates them (Q2 constant). "section": page says 0×; §Using the compass ¶12 licenses sentence/word-level through whole-document application, so section level is entailed a fortiori — [INFERENCE] at that one word | holds (with C3 note) |
| anchor | `§The compass ¶22 @ page fetched 2026-10-20, Last-Modified 2026-08-06` | section id present; ¶22 == quote; Last-Modified header `Thu, 06 Aug 2026 07:20:44 GMT`; bytes hash-identical to the wave-1 fetch | holds |
| teaches | `classify a page section by asking whether it informs action or cognition; action sections are executed by a cold reader, cognition sections are re-anchored` | first clause is the page's rule verbatim in substance ("just two questions…", table's `informs action`/`informs cognition`). `execut`, `cold reader`, `re-anchor` occur 0× on the page: clause 2 is the lane's operational gloss, consistent with the page but not quoted by it | holds (with C3 note) |
| status | `mined` | contract: "cited by ≥1 path in `used-by`" — satisfied literally; see C2 for the substantiation caveat | holds (formal) |
| opened | `2026-10-20` | fetch date header `Tue, 20 Oct 2026`; wave-1 fetch same date | holds |
| recheck | `180d` | docs page; Last-Modified stable since 2026-08-06; contract permits cadence; the "latest" alias (C4) makes periodic re-open appropriate | holds |
| used-by | `corpus/lessons/round-16.md` | `git cat-file -e c699c8c:corpus/lessons/round-16.md` → exit 0; line 35 cites S054 with the same URL and access date | holds |
| Gate: URL | `https://diataxis.fr/compass/` | identical to `source` | holds |
| Gate: accessed | `2026-10-20` | identical to `opened`; live fetch confirms | holds |
| Gate: quote | `"To use the compass, …application?"` | rendered-text equality `True`; 17 words; raw HTML splits the two questions with `<em>` (`compass.html:327`), so exactness is text-exact, not byte-substring | holds |
| Gate: location | `(§The compass ¶22)` | identical to the anchor's section+paragraph | holds |

## 4. Caveats (none blocking)

**C2 — used-by is circular.** `corpus/lessons/round-16.md:35` is inside the
mandatory Gate provenance table ("Sources opened this round (rule 1 — URL,
access date, quote ≤25 words with location)"), i.e. the record that opens the
row. `git grep -l 'S054' c699c8c` returns three files: `corpus/SOURCES.md`,
`corpus/lessons/round-16.md`, and
`.ufo/waves/round-16/w1/RoutedDisposition.md` — the last mentions `S054` only
as an id-allocation pointer ("advance 'Next unused id' to `S054`"), no use of
the compass. No knowledge entry and no lesson body applies the compass rule
under S054's name. `mined` passes the contract's literal test but rests on the
opening record itself; the same shape holds for S055. If the wave wants used-by
to mean an independent use, this is the one field to revisit (route to L1, not
a row edit by this seat).

**C3 — scope/teaches interpolations.** Measured on the fetched page: `section`
0 occurrences, `execut` 0, `cold reader` 0, `re-anchor` 0; `sentence` 1
(§Using the compass ¶12). The grounded half of `teaches` (action vs cognition)
is directly on-page; "section granularity" and the cold-reader operational
clauses are the lane's authorised application, not page statements.

**C4 — mutable alias.** Headers show `x-rtd-version: latest` and
`x-rtd-path: /proxito/html/documentation-system/latest/compass/index.html`: the
URL is a moving alias. The row pins the revision only by Last-Modified, which is
sufficient for a 180d recheck as long as the re-opener compares the header or
hash (this seat did: identical to wave 1).

## 5. Reproduction (commands and exits)

```sh
# fetch
curl -sS -D hdr.txt -o compass.html https://diataxis.fr/compass/      # exit 0; HTTP/2 200
sha256sum compass.html                                                # 8597a5b1…14e1a0
wc -c compass.html                                                    # 20288
grep -i '^last-modified:' hdr.txt                                     # Thu, 06 Aug 2026 07:20:44 GMT
# location
python3 verify_s054.py                                                # exit 0
#   p22 'To use the compass, just two questions need to be asked: action or cognition? acquisition or application?'
#   p22==quote True
#   quote_words 17 <=25 True
#   occurrences_of_quote_in_section 1
#   total_p_in_section 35
# registry
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  show c699c8c:corpus/SOURCES.md | awk -F'|' '/^\|[[:space:]]*S054[[:space:]]*\|/{print "NF="NF; print "tier="$5; print "kind="$4; print "status="$9; print "usedby="$12}'
#   NF=13
#   tier= A
#   kind= docs
#   status= mined
#   usedby= corpus/lessons/round-16.md
git -C … cat-file -e c699c8c:corpus/lessons/round-16.md               # exit 0
git -C … grep -n '^| S054' c699c8c -- .                               # SOURCES.md:63, round-16.md:35
printf '%s' "To use the compass, just two questions need to be asked: action or cognition? acquisition or application?" | wc -w   # 17
```

No tool was installed or upgraded for this seat.

## 6. Remaining unknowns

- Whether this wave's standard treats the Gate-table self-citation as
  sufficient `used-by`; the frozen contract's literal text does, a stricter
  "independent use" reading would not.
- Whether the page changes before the 180d recheck; only Last-Modified and the
  body hash guard that, since the URL is a `latest` alias.

## 7. Verdict

**Holds** on every checked field of S054 (id, source, kind, tier, scope, anchor,
teaches, status, opened, recheck, used-by, and the Gate row's URL/date/quote/
location); the only defects found are the three precision notes C1–C3, none of
which falsifies a field.
