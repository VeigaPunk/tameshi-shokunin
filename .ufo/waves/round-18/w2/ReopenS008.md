# ReopenS008 — source row S008, independent re-open (wave 2, FALSIFY)

Seat: `TameshiR18.ReopenS008`. Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Clone: `/tmp/tameshi-r18w2-ReopenS008-s0ks1V/fleet/tameshi-shokunin` (detached at the read rev;
no writes to the lane or siblings). Report is the only lane write.

Scope: `corpus/SOURCES.md` row S008; its Gate quote in
`.ufo/waves/round-18/staged/lesson-round-18-gate.md`; tier/kind/anchor fit against
`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` / fleet `CORPUS.md`; and the `used-by` path.
The paper was opened on 2026-10-20 at `https://arxiv.org/abs/2102.11378` (`:raw` too),
`.../2102.11378v1`, `.../2102.11378v2`, and `https://ar5iv.labs.arxiv.org/html/2102.11378`
(full text, 531,867 bytes, curl exit 0).

Artifact hashes at the read rev (sha256):

| Path | sha256 |
|---|---|
| `corpus/SOURCES.md` | `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` |
| `.ufo/waves/round-18/staged/lesson-round-18-gate.md` | `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` |
| `corpus/knowledge/mutation-case-kumitate-sources-check.md` | `79f629b4b5b3790c480a2ce854513dded61642cd7731bb74a4e9d302a7eac0ce` |
| `corpus/README.md` | `cce903369bf96032debdf24ee5ab2609eb9b6a30c45a17bfe29038c18e71d3d3` |
| `corpus/lessons/round-1.md` | `568609fcd0071ec3eee6a73898fc62c7f28830f539a802537c183f793d7680fc` |

The staged `corpus/SOURCES.md` copy is byte-identical to the installed
`corpus/SOURCES.md` at the read rev (same sha256 `1d4b5910…`), so the staged Gate
describes the bytes actually in the lane.

## Row as read

`corpus/SOURCES.md:19`, NF=13:

```
S008 | Practical Mutation Testing at Scale (Petrović, Ivanković, Fraser, Just; arXiv 2102.11378)
     | paper | A | Google's diff-scoped mutation testing at code review
     | Abstract, arXiv:2102.11378v2 (v1 2021-02-22, last revised 2021-02-26)
     | diff-scoped mutation at code review; mutants filtered and capped per line and per review;
       operators chosen by historical productivity; 24,000+ developers on 1,000+ projects
     | mined | 2026-10-19 | 365d | corpus/knowledge/mutation-case-kumitate-sources-check.md
```

## 1. Quote — verbatim, 19 words, anchor holds

Staged quote (`.ufo/waves/round-18/staged/lesson-round-18-gate.md:16`):

> "Mutants are selected based on the historical performance of mutation operators,
> further eliminating irrelevant mutants and improving mutant quality."
> (Abstract, item (3); arXiv:2102.11378v2)

- Exact string present in the abstract of the live arXiv abs page (`:raw`), in v2,
  and in v1; the abstract text is identical across v1/v2:
  `(3) Mutants are selected based on the historical performance of mutation operators,
  further eliminating irrelevant mutants and improving mutant quality.`
- arXiv's own version line: `[Submitted on 22 Feb 2021 (v1), last revised 26 Feb 2021
  (this version, v2)]` — matches the row anchor's version and dates.
- Word count: `printf '%s\n' "$Q" | wc -w` → **19** (limit 25).
- The staged quote is present verbatim in the staged lesson and in the referenced entry
  (both grep `-F` returned the string; exit 0).
- Anchor "Abstract, item (3)" is exact: the abstract's numbered list item (3) is this
  sentence. The quote is also in v1, so v2 is a valid but not exclusive pin.

Verdict: **PASS**.

## 2. `teaches` cell — no overstatement

| Cell clause | Page evidence |
|---|---|
| diff-scoped mutation at code review | §II-A: "we implemented **diff-based** mutation testing: Mutants are only generated for lines that are changed"; changelists are sent "for code review". |
| mutants filtered and capped per line and per review | Abstract item (2): "Mutants are filtered, removing mutants that are likely to be irrelevant to developers, and limiting the number of mutants per line and per code review process". §II-C: "We limit the number of reported mutants to at most 7 times the number of total files in the changelist"; Fig. 7 discussion: "select one mutant per line". |
| operators chosen by historical productivity | Abstract item (3); §IV: "looks into historical performance of those mutants in two categories: developer feedback on **productivity** and mutant survivabiliy. **Mutation operators are ordered using this metric** rather than uniformly shuffled"; §IV-C: "historical information about mutation productivity". |
| 24,000+ developers on 1,000+ projects | Abstract: "used by more than 24,000 developers on more than 1,000 projects". |

"diff-scoped" is the row's shorthand for the page's "diff-based"; "historical
productivity" is the page's own §IV-C term and one of the two §IV categories. No clause
exceeds the page. The scope cell ("Google's diff-scoped mutation testing at code review")
is narrower than the paper, which is the honest direction.

Minor observation (not a defect): the Gate quote grounds clause 3 only; clauses 1, 2 and
4 are grounded in the same abstract/body but outside the quoted span. Contract rule 1's
quote requirement applies to new rows and S008 is an existing row being advanced.

Verdict: **PASS**.

## 3. Tier / kind / anchor fit

Contract (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`; mirrored at fleet `CORPUS.md:86-115`):

- `kind` enum includes `paper` → fits.
- Tier **A**: "primary or authoritative for that scope (spec, official docs, source code,
  **original paper**, maintainer statement …)". The row is an original paper by Google
  engineers describing Google's own system; scope is explicitly limited to Google's
  system at code review. Fits A; no tier inflation.
- `anchor` requires an exact section/heading plus revision (version, commit, or
  publication date), never a bare homepage. The row gives heading (`Abstract`), version
  (`v2`) and dates (`v1 2021-02-22`, `last revised 2021-02-26`). Fits.
- `opened 2026-10-19`, `recheck 365d`: shapes valid.

Verdict: **PASS**.

## 4. `used-by` path — exists and cites S008, but the citation contradicts the row's status

Path: `corpus/knowledge/mutation-case-kumitate-sources-check.md`.

- Existence: `git cat-file -e 01d586d:corpus/knowledge/mutation-case-kumitate-sources-check.md`
  → 0; contract census (`mined` rows, used-by existence) printed `ok: …` for this path,
  exit 0.
- Citation: `git grep -n "S008"` at the rev finds the entry at:
  - `:1` — `source:` header: "S008 … (paper, tier A, **queued** — Q1 quote recorded in
    `.ufo/waves/round-18/sources/S066-B02SrcGoogleMutation.md`, not yet a mined row)".
  - `:76` — "Selection. S008's historical-performance selection (Q1, below) is not used."
    followed by the quote "cited here for contrast".
  - `:215-216` — "S008 is `queued` with `used-by —`; citing it here needs the L1 to mine
    it and set used-by."
- The cited draft record exists:
  `.ufo/waves/round-18/sources/S066-B02SrcGoogleMutation.md` = "S066 draft — DUPLICATE
  S008", with the same 19-word Q1 and arXiv URL; it was not installed as a row.

**Finding (minor, bookkeeping):** at the read rev the registry says `mined` +
`used-by corpus/knowledge/…sources-check.md`, while the entry it points to says S008 is
`queued`, `used-by —`, and "not yet a mined row". The same commit `58e5d53` both set
S008 to `mined` and added the entry that calls it `queued` (`git show 58e5d53:corpus/SOURCES.md`
line 19 = `mined`; `git show 58e5d53:corpus/knowledge/…` line 1 = `queued`). The entry
was not touched again before the read rev (`git log 183f87b..01d586d -- <entry>` → only
`58e5d53`). The contract's mechanical `mined` test ("cited by ≥1 path in used-by") is
met, so the row's status is contract-valid, but a reader who follows `used-by` is told
the opposite status, and the citation is contrast-only (the entry explicitly does not
use S008's selection). This does not affect the row's quote, teaches cell, tier, kind or
anchor; it is a stale entry, not a false row.

Other in-repo S008 citations, checked and not counted as `used-by`:
- `corpus/README.md:84` (frontier F7, "incremental re-sweep granularity") lists S008 —
  README is not a knowledge entry or lesson under the contract.
- `corpus/lessons/round-1.md:367` is the round-1 opening table (URL, timestamp, quote,
  anchor), not a use. Precedent: S007 is `queued` with `used-by —` while listed in the
  same table at `round-1.md:366`, so the lane does not count that table as used-by.

Recommendation: in the next L1 pass, update the entry's three status references
(`:1`, `:76`, `:215-216`) to `mined` or note that the row was mined after the entry was
written. No row edit is required.

## 5. Staged lesson claims and arithmetic

- Diff `183f87b..01d586d -- corpus/SOURCES.md`: hunks `19c19`, `73a74,85` (S065–S074 +
  blank + note), `195c207,208` (id footer). Matches staged §Registry changes; among
  pre-existing rows only line 19 changed, and only fields 8 and 11 (status, used-by).
- Counts: `183f87b` rows=62 mined=35 queued=24 rejected=3; `01d586d` rows=72 mined=44
  queued=23 rejected=5. Matches the staged "Totals" line exactly.
- Duplicate ids: 0. S008 row NF=13; tier/kind/status enums valid.
- Staged file installed: staged and live `corpus/SOURCES.md` sha256 both `1d4b5910…`.
- Staged statement "status queued → mined; used-by — → entry; other cells unchanged":
  verified against the two revs (base line 19 is `queued` / `—`).

Verdict: **PASS**.

## Findings summary

| # | Finding | Severity |
|---|---|---|
| F1 | Quote verbatim at Abstract item (3), arXiv:2102.11378v2; 19 words; version dates correct | none |
| F2 | `teaches` cell fully page-grounded; no overstatement | none |
| F3 | `kind=paper`, `tier=A`, anchor (heading+version+dates) fit the contract | none |
| F4 | `used-by` path exists and cites S008 at three lines | none |
| F5 | Cited entry still records S008 as `queued`/`used-by —` and says the selection is "not used"; same commit `58e5d53` introduced both the `mined` row and the stale entry | minor |
| F6 | Gate quote grounds only clause 3 of the four-clause `teaches` cell (other clauses verified directly on the page) | minor observation |

No blocking gap. No tool installs or upgrades were needed.

**Verdict: holds** — S008 is faithfully recorded at `01d586d` (19-word verbatim quote at
v2 Abstract item (3), teaches/tier/kind/anchor all fit, used-by path exists and cites),
with one minor bookkeeping gap: the only `used-by` entry still calls the row `queued`
and cites it for contrast only.
