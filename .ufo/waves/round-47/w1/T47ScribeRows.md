# T47ScribeRows — four C3 registry rows (S261-S264) drafted, gate-quoted and predicate-checked

Seat: T47ScribeRows (leaf, round-47 wave w1). Contract read first:
`.ufo/evidence/round-47/contract.json` (frozen, never edited). Lane checkout read-only; the only
lane file written is this report and the one named deliverable.

## Deliverable

`.ufo/waves/round-47/w1/T47ScribeRows.rows.md` — four registry rows in the 11-column
`corpus/SOURCES.md` schema (one per line, no `|` in any cell) followed by the `## Gate quotes`
block (URL, access date 2026-10-25, ≤25-word quote, location, per row). Nothing was written into
`corpus/`; no git/jj command was run in the lane; no counter was run in any mode.

Rows, staged id → adopted id by document (never by arithmetic):

| row | staged | document | kind | tier |
|---|---|---|---|---|
| S261 | S155 | arxiv.org/abs/2302.09330 | paper | A |
| S262 | S158 | the Lam et al. camera-ready PDF | paper | A |
| S263 | S206 | arxiv.org/abs/2607.09345 | paper | A |
| S264 | S207 | Semantic Scholar graph record of DOI 10.1109/ICST60714.2024.00037 | docs | B |

Tier reasons, carried in the scope cell so the census still sees one `[ABC]` letter:
- S261, S263 — abstract-only carriers, but each row's scope is *the abstract's own claim*
  (prediction from recorded history / flakiness is not static), so A is the primary carrier for
  exactly what the row claims; nothing beyond the abstract is attributed to either paper.
- S262 — full camera-ready text read (guidelines box + §V-A), so A.
- S264 — **B**: the carrier is a third-party metadata index, not the publisher. The snapshot's own
  `venue` field reads `International Conference on Information Control Systems & Technologies`
  while its `externalIds.DBLP` is `conf/icst/LeinenEPSSJ24` and the abstract is about CI
  flaky-test cost; the record's venue field is demonstrably unreliable, so only its abstract string
  is used. `kind: docs` because the artifact is an API metadata record reproducing the publisher's
  abstract — it is not data to analyse (`dataset` would be false; S2 exposes no rows).

## Validation run (what was executed, and where)

Scratch dir `/tmp/tameshi-r47-T47ScribeRows/`. The C3 counter was **not** run (no `--selftest`,
no `--only`, no `--rev`); instead its own row predicate was imported read-only and driven against a
synthetic tree, so the rows are checked with the counter's exact code path without producing or
implying a verdict:

1. `importlib` load of `.ufo/evidence/round-47/coverage/measure.py`; `measure.flaky_rows()` over a
   fake `Tree` that returns the lane's `corpus/SOURCES.md` plus my four rows and the real snapshot
   bytes. Result: `rows recognized = ['S261','S263','S264']` — exactly the three frozen documents,
   each with `used` = its assigned entry path and `doc` equal to the frozen key. **S262 is absent by
   design**: the counter's `DOCS` tuple holds only the three frozen documents, matching the
   contract's `extra_row` ("the counter does not count it").
2. Same harness also verified, per row: 11 cells (12 pipes), no `|` inside any cell, the anchor's
   `SNAP_RE` path resolves, and the named 8-hex prefix is a real prefix of the snapshot's sha256
   (`2965343c`, `bf52c908`, `16ecdefc`, `6ab5b3f5`); S262 additionally names the PDF's full sha256
   `0b88045817f146db3eb26d305c864291010e5c083aa8d5cac480be3c5350895d`, which matches the committed
   PDF.
3. Frozen SOURCES census (the six `awk`/`grep` commands from `CORPUS.md`) on
   `/tmp/tameshi-r47-T47ScribeRows/audit2.md` = the lane file plus my four rows:
   `rows=124` (was 120), `malformed=0`, duplicate ids: none, enum/tier-violation output: empty.
   Tier histogram on the assembled copy: `A=111 B=10 C=3`.
4. Snapshot availability and identity at the freeze rev, `git cat-file -e` / `git show | sha256sum`
   against `9acfbe21435e1976636a276448dee1d5e7155915`: all five files under
   `.ufo/evidence/round-47/coverage/sources/` are present, and the freeze digests equal the working
   digests (`2965343c`, `16ecdefc`, `bf52c908`, `6ab5b3f5`), so the anchor prefixes hold at the rev
   the rows will be read at. At the freeze `corpus/SOURCES.md` holds 120 rows, last `S260` — the
   ids S261-S264 were unused.
5. Locating/freshness of every quote below: `measure.fold` + `measure.norm_text` (the counter's own
   folding) applied to the committed snapshots and to the three package copies under
   `.ufo/evidence/round-47/assimilation/package/`.

## Gate quotes (verbatim from the snapshot, folded with the counter's own normaliser)

- **S261** `https://arxiv.org/abs/2302.09330` — accessed 2026-10-25 — §Abstract, sentence 2, inside
  the visible `<blockquote class="abstract">` of `arxiv-2302.09330-abs.html`: "Detecting flaky tests
  is therefore a crucial task in maintaining code quality, as it builds the necessary foundation for
  any form of systematic response" (24 words). Located: yes. Absent from the package copy: yes.
- **S262** `https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf` —
  accessed 2026-10-25 — §V-A (RQ1), burst-length discussion, text lines 339-341 of
  `lam-2020-reruns.txt`: "require more reruns before a pass result can be observed and the test is
  marked as flaky" (17 words). Located: yes. Absent from the package copy: yes.
- **S263** `https://arxiv.org/abs/2607.09345` — accessed 2026-10-25 — §Abstract, the C-IDoFT
  sentences, inside the visible `<blockquote class="abstract">` of `arxiv-2607.09345-abs.html`:
  "C-IDoFT is a controlled counterfactual, not a benchmark for reuse" (10 words). Located: yes.
  Absent from the package copy: yes.
- **S264** `https://api.semanticscholar.org/graph/v1/paper/doi:10.1109/icst60714.2024.00037?fields=title%2Cabstract%2Cyear%2Cvenue%2Cauthors%2CexternalIds`
  — accessed 2026-10-25 — the record's `abstract` string, penultimate sentence, in
  `s2-icst24-cost-of-flaky.json`: "The insights gained from our case study have led to the decision
  to shift effort from investigation and repair to automatically rerunning tests" (23 words).
  Located: yes. Absent from the package copy: yes.

All four are also usable as the **fresh located quote** the C3 entry predicate demands (a located
quote that does not occur in the package copy of the same basename).

## Findings the entry seat and the L1 need

1. **The Lam text snapshot is a two-column PDF extraction, and that breaks one quote.** The
   guideline the round-46 package copy quotes — "one can use ≤ 5 reruns … and still check correctly
   ≥ 82% of the time" (`package/flaky-aware-verdict-evidence.md`, S158 bullet) — is **not a
   substring of the snapshot's folded text**: lines 113-114 interleave the left column with the
   right column ("… Google's default ten | conducted surveys of developers … | reruns [6]) and still
   check correctly ≥ 82% of the time."). An entry re-grounded on S262 that reuses that sentence
   fails `entry_ok`'s `located` test and would print `REFUSED … no located quote`. The located
   fragment is only "one can use ≤ 5 reruns (50% less than Google's default ten" (12 words, line
   113) — and it *is* in the package copy, so it cannot serve as the fresh quote either. The row's
   anchor says this explicitly; the entry should quote a single-column, line-contiguous fragment
   (my S262 gate quote is one) and note the interleave where it relies on the 82% figure.
2. **S264's tier is B for a reason visible in the record itself** (venue/DBLP contradiction above).
   The package copy's B is therefore re-derived, not inherited: the carrier is secondary even
   though the abstract text is the publisher's.
3. **The S263 abstract carries more than the truncation suggests.** `og:description` and
   `citation_abstract` cut off, but the visible abstract blockquote is complete (1,929 folded
   chars), including "C-IDoFT is a controlled counterfactual, not a benchmark for reuse" and the
   project-separated re-scoring sentence. Quote from the blockquote, not from the meta fields.
4. Quote candidates that are **located but in the package copy** (so not fresh): S262 "one can use ≤
   5 reruns (50% less than Google's default ten" (12 w); S263 "Flakiness is not a static property of
   test code" (9 w) and "widely used benchmarks contain shortcuts that inflate reported F1 scores"
   (10 w); S264 "Automatically rerunning a test costs 0.02 cents" (7 w). Candidates that are
   **fresh but not located** in the txt: S262 "we label tests as flaky if our runs have both pass
   and fail outcomes across these reruns" (17 w) — the abstract region is column-interleaved.
5. The rows' `used-by` names the three entry paths (`corpus/knowledge/flaky-aware-verdict-evidence.md`
   for S261+S262, `r8-flakiness-not-static.md` for S263, `r8-flaky-cost-baseline.md` for S264).
   Until those files exist, the census's "mined rows whose used-by paths do not exist" check prints
   exactly those three paths — a precondition of the entry seat, not a defect of the rows.
6. Registering S261-S264 takes the registry 120 → 124 rows, so the no-harm monitor "registry rows
   not below 120" stays ok; S160 is untouched.

## Limits of this seat

- Abstract-level only for S261, S263, S264 (the S2 record carries an abstract, not the paper); no
  claim beyond the abstract is made in those rows, and the S264 venue contradiction is reported, not
  resolved (the publisher's page was out of scope).
- S262 is the uncounted fourth row; the counter will not see it, and I did not add it to any
  document list (the frozen `contract.json` is untouchable).
- No entry file, no `corpus/README.md` index row, no status/`recheck`/`used-by` edit elsewhere was
  made; no registry row was appended to `corpus/SOURCES.md` (the row text lives only in the
  deliverable, for the owning seat to append).
- No counter was run as a verdict; no `git add/commit/stash/checkout/switch/reset/pull/push`, no
  mutating `jj`, nothing written under `/home/vgpnk/Projects/shokuknow` or the fleet repo.

## Tooling

None installed or upgraded; `pacman` untouched. Only the system `python3`, `awk`, `grep` and
read-only `git show`/`git cat-file` were used.

## Artifacts

- Deliverable: `.ufo/waves/round-47/w1/T47ScribeRows.rows.md`
- Scratch: `/tmp/tameshi-r47-T47ScribeRows/rows.md` (draft), `audit2.md` (census copy), `abs.txt`
  (abstract extraction notes)
- Read-only inputs: `.ufo/evidence/round-47/contract.json`, `corpus/SOURCES.md:10-11,131-135`,
  `.ufo/evidence/round-47/coverage/measure.py`, `.ufo/evidence/round-47/coverage/sources/*`,
  `.ufo/evidence/round-47/assimilation/package/*.md`, `/home/vgpnk/Projects/shokunin/CORPUS.md`
