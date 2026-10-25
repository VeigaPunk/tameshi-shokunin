# ScoutQ110 — Quarantine S110 hand-check (tameshi)

## Verdict: PRESENT — the quarantined quote is verbatim in the cited source

The register's `payload-absent` verdict is a **false positive** caused by
two-column PDF extraction, not a fabrication.

## The row

Campaign absent-defect register:
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:217`

```
| `tameshi` | round1 | S110 | `payload-absent` |
https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf |
`one can use ≤ 5 reruns (50% less than Google's default ten reruns [6]) and still
check correctly ≥ 82% of the time.` |
```

(Lint finding: `quote-lint-full-v5.json`, `findings` with `lane=tameshi,
round=round1, id=S110, verdict=ABSENT, binding=id`. Staged lane row renumbered
to S114 in `lanes/tameshi/SOURCES-PROPOSED.md`; never adopted into
`corpus/SOURCES.md`.)

## Hand-check

- Fetch (2026-10-24): `curl -fsSL -o /tmp/tameshi-r40-ScoutQ110/lam.pdf
  https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf`
  → HTTP 200, 565,435 bytes, sha256
  `0b88045817f146db3eb26d305c864291010e5c083aa8d5cac480be3c5350895d`.
- `pdftotext -raw lam.pdf -` (and default mode): whitespace-folded text
  contains the quote **byte-exact**, including the typographic `’` and the
  `≤`/`≥` glyphs:
  `one can use ≤ 5 reruns (50% less than Google’s default ten reruns [6]) and
  still check correctly ≥ 82% of the time.`
- Page anchor holds: `pdftotext -raw -f 2 -l 2` matches; the string appears
  only on PDF page 2, under the `RQ1 & RQ3:` guideline — exactly the cited
  anchor "§Guidelines, RQ1 & RQ3, p. 2". Quote is 23 words (within 25).

## Why the checker missed it

Under `pdftotext -layout` the sentence is split across the two-column break
(`...default ten <RIGHT-COLUMN-TEXT> reruns [6]) and still check...`), so a
contiguous-string match fails. The lint's eleven folds evidently included only
the column-interleaved extraction (or an equivalent split-line fetch), hence
`payload-absent`. Reading-order extraction resolves it.

## Disposition

- **Present.** Quote verbatim, anchor correct, source reachable, tier A
  (author-hosted camera-ready of the Lam et al. flaky-reruns study).
- The staged row's second `teaches` clause also verifies: same page,
  `RQ2 & RQ3:` guideline — "run tests in different orders with fewer times
  each, rather than fewer orders with more times each" (lam-raw.txt:161).
- Register left untouched per task bounds; this finding names the false
  positive without rewriting the register's class.
