# T47ScribeEntryStatic — report (C3 entry: flakiness is not static)

Seat: T47ScribeEntryStatic. Deliverable: `.ufo/waves/round-47/w1/T47ScribeEntryStatic.entry.md`
(1,354 words, 52 lines, sha256 `cf41a03679af02f7fc0b2f878137bc713f7355a91c5c27e803ec8e6919d62373`).
Intended landing path: `corpus/knowledge/r8-flakiness-not-static.md` (not landed by this seat; see Out of scope).

## Behavior

Drafted the re-grounded entry for snapshot `arxiv-2607.09345-abs.html` (S263), with the required header trio:

1. `source: S263 — https://arxiv.org/abs/2607.09345 — §Abstract — arXiv:2607.09345v1` (exact, as specified)
2. `verified-at: 2026-10-25`
3. `recheck: 365d — curl ... | grep -cF 'C-IDoFT is a controlled counterfactual, not a benchmark for reuse'` (ran 2026-10-25 → count 3)
4. `ground: F3 — ...`; F7 deliberately **not** claimed, with §3 stating why.

Section scheme follows the lane's house style (`corpus/knowledge/r6-flaky-failures-cluster.md`, `r8-gtest-order-and-seed.md`):
Snapshot paragraph (path, sha256, bytes, extraction tool sha, fetch dates, "under review", no venue), §1 what the
snapshot states (located quotes + token counts), §2 what it does and does not say about F3, §3 why it is not an F7
row, §4 fixture-craft meaning (lane's reading, `[INFERENCE]`), §5 boundary. The abstract is explicitly labelled as
not being the paper's evidence; the paper body was not fetched and no venue/peer-review outcome is asserted.

## Provenance and gates (commands actually run)

All read-only on the lane; scratch in `/tmp/tameshi-r47-T47ScribeEntryStatic/`.

- `sha256sum .ufo/evidence/round-47/coverage/sources/arxiv-2607.09345-abs.html`
  → `16ecdefca1f247d3acef2439576ca380bd0bacdd2fa1215e16c71006547a925d` (matches the pinned value; 44,459 bytes).
- `python3 .ufo/evidence/round-45/freshness/measure.py --extract <snapshot> > snap.txt`
  → exit 0, 5,492 bytes of extracted text (extraction tool sha256 `ba64041f…c6ed`).
- Live re-fetch for the recheck line: `curl -fsSL 'https://arxiv.org/abs/2607.09345' -o live.html` → exit 0;
  44,459 bytes; sha256 `16ecdefc…925d`; `cmp -s live.html <snapshot>` → **IDENTICAL**; the recheck grep count was 3.
- `grep -cF` of five candidate abstract sentences in the raw snapshot HTML → 3 each (meta description + abstract +
  citation block); every quote below was then located in the counter's own folded text, not just the raw HTML.
- Quote audit reusing the C3 counter's own `fold` / `norm_text` / `QUOTE_RE` / `entry_ok` (imported by path, not a
  counter run): 13 double-quoted passages; **13 located** in the snapshot text; **12 absent from the package copy**;
  all 13 within 6–25 folded tokens; `BAD: []`. The one package-present quote is the thesis sentence, marked as such
  in §1. So the "≥1 located quote absent from the package copy" rule is met with 12.
- `entry_ok('corpus/knowledge/r8-flakiness-not-static.md', entry, {'S263': ...}, package_bytes)`
  → `(True, 'ok', ['S263'])` using a synthetic row built from this snapshot. This validates header trio, citation of
  the row id, `verified-at ≥ 2026-10-25`, `recheck:` prefix, used-by membership and the fresh located quote.

Token counts printed beside quotes were corrected to the measured values after a first draft (several were off by
one); the file now carries the measured counts only.

## Touched surfaces

- `.ufo/waves/round-47/w1/T47ScribeEntryStatic.entry.md` (new; deliverable).
- `.ufo/waves/round-47/w1/T47ScribeEntryStatic.md` (this report).
- Scratch only: `/tmp/tameshi-r47-T47ScribeEntryStatic/{snap.txt,extract.err,live.html,verify.py}`.
- No lane file was edited; no `git add/commit/stash/checkout/reset/pull/push`; no `jj` command; contract, counters,
  pool, statements, controls, snapshots and package copies untouched.

## Findings (conflicts, verbatim)

1. **Package author list is wrong.** Package line 1 says:
   `source: S206 — https://arxiv.org/abs/2607.09345 — "How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection" (Baltes, McKim, Zaidman, Wagner), arXiv 2607.09345, v1 posted 2026-07-10, marked "15 pages, 7 figures, under review"`
   The committed snapshot names five authors: `Ömer Oktay Gültekin , Alexander Berndt , Jonathan Bell , Thomas Bach , Sebastian Baltes`.
   The entry follows the snapshot and records the discrepancy in §5. Title, posting date (v1 `Fri, 10 Jul 2026
   12:24:25 UTC`), sizes and the `Comments: 15 pages, 7 figures, under review` line agree with the package.
2. **Package grounds F7; this snapshot does not support F7.** Package line 4: `ground: F7 (the counter-case to a
   code-based re-sweep predictor) and F3 (the determinism precondition)`. The abstract contains no statement about
   re-sweeping, cadence or reuse of prior leg results; its 42%/58% split is about recovering a *cause*, not reusing a
   result. The assignment conditions F7 on a claim about incremental re-sweeps, so the entry claims F3 only and §3
   states the adjacency (a reused verdict is a static record) as `[INFERENCE]`, not grounding.
3. **Package recheck command remains valid but is weaker.** Package line 3 greps `Flakiness is not a static property
   of test code` (the thesis), which is still present (count 3 here). The entry's recheck greps a phrase the package
   never quoted (`C-IDoFT is a controlled counterfactual, not a benchmark for reuse`), so a future drift in the
   counterfactual-dataset wording is detected as well.
4. **"under review" is the whole status.** The snapshot has no journal-reference field; `Comments: 15 pages, 7
   figures, under review` plus `arXiv:2607.09345v1 [cs.SE]` are all it says. The entry states no venue and no
   peer-review outcome, and its title says "posted", not "published".
5. **What only the abstract shows.** The abstract reports authors' claims about three detectors, two curated datasets
   (C-IDoFT: 54,468 unit tests / 57 projects; 86 mined end-to-end tests), the 42%/58% cause-recoverability split, and
   a reframing toward environment-conditioned failure probability. It gives no per-detector F1, no project-level
   breakdown, no environment-differential result, and no statement that any lane gate is flaky. §2 and §5 say so;
   §2's transfer to the lane is marked `[INFERENCE]`.
6. **Craft consequence (the lane's reading, §4).** Every F3 control verdict should carry an `evidence_class`
   (`execution` only when N ≥ 3 byte-identical controls decided it; otherwise `static-only`, which may not print a
   pass), and a per-case record should state whether the deciding evidence was a repeated execution or a static read —
   the abstract's own 42%/58% split is the published shape of that distinction for its dataset. Labelled inference;
   the entry does not claim the abstract says anything about this lane.

## Out of scope (left for the landing/row seats)

- Adding the `S263` row to `corpus/SOURCES.md` is not this seat's deliverable. For the counter to accept the entry,
  that row must satisfy `measure.py`'s reader: 13 pipe cells, cell 8 exactly `mined`, cell 2 holding
  `https://arxiv.org/abs/2607.09345`, cell 6 holding `.ufo/evidence/round-47/coverage/sources/arxiv-2607.09345-abs.html`
  with an 8–64 hex char sha256 prefix (`16ecdefc…`), and cell 11 (used-by) listing `corpus/knowledge/r8-flakiness-not-static.md`.
- Indexing: `corpus/README.md` must contain the backticked path `` `corpus/knowledge/r8-flakiness-not-static.md` ``
  or its `corpus/`-stripped form, else the counter counts the entry but not its index.
- No counter verdict was produced (the deciding run is the L1's): `measure.py` was never run with `--rev` here, and
  its `--selftest` was not run (not needed for a drafting seat). The `entry_ok` call above is an import-level reuse of
  the counter's own functions against the unlanded draft, not a counter run.
- `assemble.py`, `pool.py`, `no-harm.sh` and the C1/C2 surfaces were not touched.
- No tool was installed or upgraded (nothing was needed); no model was passed anywhere.

## Known limits

- The entry rests on the abstract page alone; body claims (datasets, shortcut list, reimplementations) are reported as
  the authors' claims, not verified.
- The snapshot is v1 and marked under review: a revision could reword the quotes; the recheck line (365d, `grep -cF`
  on a package-absent phrase) is the drift detector, and a zero count means re-locate every quote before reuse.
- The live re-fetch on 2026-10-25 was byte-identical, so the "fetched" provenance is observed once on that date, not a
  standing guarantee.
- The entry file is written at the wave path, not at `corpus/knowledge/`; the final counter reading is the landing
  seat's to take.
