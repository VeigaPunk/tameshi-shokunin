seat: CritRowSelection

# C1 population definition — cherry-pick attack (round 45, w1)

Method: parsed `corpus/SOURCES.md` with the counter's exact predicate
(`.ufo/evidence/round-45/freshness/measure.py:78-97` — ROW_RE, 13-cell split,
URL_RE on the source cell, `status=='mined' and id<=S160 and url`). The file is
identical at base and freeze (blob `a3bb6a2e2e275bea51b4500fdad885ef062fecdc`,
462 lines at both `5891bdb…` and `3310e7b…`); 115 rows parsed, 0 parse
problems. S160 monitor count = 1.

## 1. Population and exclusions (all rows)

Population (mined, id<=S160, http(s) URL): **73 rows**.

| excluded class | count | rows |
|---|---|---|
| mined, no URL (own-work/path) | 14 | S031 S032 S033 S034 S035 S036 S037 S050 S051 S053 S082 S083 S085 S088 |
| queued | 22 | S007 S009 S010 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S025 S027 S040 S042 S043 S044 S045 S092 |
| rejected | 6 | S029 S030 S046 S067 S071 S080 |
| id > S160 | 0 | — |

Total excluded 42; no row is excluded by id (max id in file = S160).

## 2. Are the 14 mined no-URL exclusions defensible? — YES

All 14 are internal path references, not external documents:
- lane own-work: S031 `tools/mutate-and-run.sh`, S050 `tools/evidence-disposition.py`,
  S051 `tools/context-capture.py`, S082 `.ufo/waves/round-21/original-outcomes-final.json`,
  S083 `tools/registry.json`, S085 `.ufo/waves/round-23/fresh-adjudication.json`;
- sibling-lane read-only gate files: S032/S037/S053/S088 (kumitate scripts),
  S033/S036 (kagi), S034 (tsukuroi), S035 (mado).

Verified: the substring `http` appears nowhere in any of the 14 source cells.
They name in-repo paths pinned at blob revisions; there is no URL to re-fetch,
so they cannot participate in a live-bytes sweep. The exclusion is coherent
with the claim surface ("held external sources … with an http(s) URL", contract
`contract.json:20`) and is not a hole in the sweep: these rows' drift is already
governed by git blob pinning, not by byte drift. No fix needed here.

## 3. Does id <= S160 exclude anything? — NO (at freeze)

No row with id > S160 exists in SOURCES.md at either frozen rev (max = S160).
The bound is dormant at freeze; it is instead *protective*: C2's adopted
S256/S257 (id > 160) can never leak into the C1 population and dilute or drag
the freshness count.

## 4. Duplicate-URL rows: double counting is real, bounded to 15 rows

7 distinct URLs are held by 15 population rows (exact matches, canonical
normalization — trailing slash, http/https, www, arXiv abs/pdf — confirms the
same 65 distinct URLs):

| URL | rows |
|---|---|
| https://bazel.build/reference/test-encyclopedia | S028 S081 |
| https://pitest.org/quickstart/incremental_analysis/ | S041 S047 S048 |
| https://man7.org/linux/man-pages/man1/strace.1.html | S060 S075 |
| https://docs.jj-vcs.dev/latest/git-compatibility/ | S061 S076 |
| https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html | S068 S077 |
| https://man7.org/linux/man-pages/man2/open.2.html | S072 S078 |
| https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ | S089 S160 |

Distinct documents in population: **65** (73 rows − 15 dup rows + 7 dup URLs).

The counter counts rows, so one committed snapshot blob can serve several
entries, and (more sharply) the same quote can verify sibling rows: `grade()`
(`measure.py:132-165`) only rejects a quote copied from the *row's own* cells
(`measure.py:159-161`) — not a quote reused across two rows of the same URL, and
the ≥2-shared-word test is evaluated per row. E.g. one strace man-page sentence
can plausibly satisfy both S060 and S075; one PIT §Incremental analysis passage
can serve S041/S047/S048.

Consequences (target math):
- Row target 50/73 = 68.5% of rows.
- Minimum distinct documents needed to reach fresh=50, using all dup credit:
  35 singletons + 7 URLs feeding 15 dup rows = **42 distinct documents** (64.6%
  of the 65-document universe). So a pass can hide as few as 42/65 documents
  refreshed.
- Proportion-preserving equivalent on distinct documents: 0.6849 × 65 ≈ **45**
  (45/65 = 69.2%) — i.e. the passing threshold measured per-document would be
  ~45, not 50.
- Absolute parity (50 distinct documents) is strictly harder than the frozen
  row metric.
- Score rule `floor(10*fresh/73)` (`measure.py:255`) is fixed to the 73-row
  denominator: at fresh=50, score 6; under a 65-document population the same
  work would score floor(500/65)=7, and the proportional 45-doc target also
  scores 6.

Verdict meaning: the literal claim ("at least 50 of … 73 held registry rows",
`contract.json:21`) is what the counter measures, and it is not violated by
duplicate URLs — but the *freshness* meaning is diluted: a pass can be reached
while fewer than half of the distinct external documents are re-verified
(42/65). This is a genuine, bounded inflation vector (15 of 73 rows / 7 of 65
documents), not a threshold-flip by itself: the deciding run would need to land
fresh in [42..50] rows with ≤42 distinct docs for the verdict to differ between
the two framings.

## Smallest safe correction (tie to the claim)

Keep the frozen 73-row count as the pass gate, but require the L1's deciding
run to report both `fresh` and `distinct_docs` (fresh rows that hit a distinct
URL), and publish the max per-URL row count; if the intent is per-document
freshness, the population should be the 65 distinct URLs with target 45
(proportional) or 50 (absolute parity) — with the score_rule updated to the
65-document denominator. No change to the 14 no-URL exclusions (defensible) or
to `id <= S160` (excludes nothing at freeze; keeps C2 rows out).

Commands run (read-only): `git show <rev>:corpus/SOURCES.md | wc -l` at both
frozen revs (462/462); `git rev-parse <rev>:corpus/SOURCES.md` → both
`a3bb6a2e2e275bea51b4500fdad885ef062fecdc`; scratch analysis scripts under
`/tmp/tameshi-r45-CritRowSelection/` (`analyze.py`, `analyze2.py`,
`analyze3.py`; outputs above).
