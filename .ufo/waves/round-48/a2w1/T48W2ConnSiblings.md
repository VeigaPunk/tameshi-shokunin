# T48W2ConnSiblings — sibling-lane overlap of the round-48 re-anchored documents

Seat: T48W2ConnSiblings (connector, adjacency). Round 48 attempt 2, wave 1.
Item: check whether the four documents re-anchored in round 48 (C2 targets S026, S048,
S093, S108 superseded by S265–S268) are also held by sibling lanes, and with what
scope/tier/anchor; report overlaps and conflicts. Never absorb — adjacency only.

## Method

- Live registry of each of the 21 sibling lanes read at `<lane>/corpus/SOURCES.md`
  (all 21 exist; sizes 51–936 lines).
- Scoped grep per document URL/host over the live registry, then a corpus-wide sweep
  over each sibling's entire `corpus/` for the exact URLs and host variants.
- Sibling wave artifacts under `.ufo/waves/` were excluded (stale copies of the same
  registry); only live `corpus/SOURCES.md` rows count as holdings.

Commands (run from `/home/vgpnk/Projects/shokunin`):

    for d in *-shokunin; do [ "$d" = tameshi-shokunin ] && continue
      grep -in -E "<pattern>" "$d/corpus/SOURCES.md"; done
    for d in *-shokunin; do ... grep -rl -E "googleblog|tensorflow\.org|incremental_analysis" "$d/corpus"; done

## The four re-anchored documents (tameshi standing, for comparison)

| T | Document | tameshi row | tier | anchor |
|---|----------|-------------|------|--------|
| S026→S265 | Google Testing Blog, "Flaky Tests at Google and How We Mitigate Them" (Micco, 2016-05-27) — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html | `tameshi-shokunin/corpus/SOURCES.md:37` (S026, opened 2026-10-19) → `:140` (S265, 2026-10-26, sha256 `a4c5c46b4af9`, 236387 B) | A | Post body; S265 locates articleBody ¶ at raw line 1132 |
| S048→S266 | PIT docs, Incremental analysis — https://pitest.org/quickstart/incremental_analysis/ | `:57` (S048, opened 2026-10-20) → `:141` (S266, 2026-10-26, sha256 `e9cbc3e1ab7c`, 8892 B, Last-Modified 2026-06-03) | A | §Incremental analysis item 4, raw line 86 |
| S093→S267 | bwrap(1), bubblewrap 0.13.1 — blob page + raw XML https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml | `:102` (S093, opened 2026-10-23) → `:142` (S267, 2026-10-26, sha256 `2cb77df2f4be`, 33289 B) | A | tag v0.13.1 = commit `362936ae`; S267 quote at raw lines 153–160 (bytes 5909–6400) |
| S108→S268 | 黄金测试 zh-cn (TensorFlow Federated) — https://www.tensorflow.org/federated/golden_tests?hl=zh-cn | `:120` (S108, opened 2026-10-24) → `:143` (S268, 2026-10-26, sha256 `04e4c091715a`, 111409 B) | B | §如何更新 .expected 文件？, page raw line 3611 |

## Finding 1 — bwrap.xml v0.13.1 IS held by a sibling: kumitate-shokunin (overlap)

`kumitate-shokunin/corpus/SOURCES.md` holds the identical bytes twice:

- **S069** (`:82`) — same raw URL `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml`;
  docs, **tier A**, mined, opened **2026-10-23**, recheck `on-release`; same tag/commit `362936ae`
  and same body sha256 `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`.
  Scope: bwrap environment options, PID-namespace reaper, `--die-with-parent`.
  Anchor: `bwrap.xml:62-67, 138-140, 217-235, 587-599`.
  Used-by: `corpus/knowledge/agent-isolation-substrates.md`, `corpus/lessons/round-45.md`.
- **S095** (`:108`) — same raw URL, same tag/sha256; docs, **tier A**, mined, opened
  **2026-10-23**, `on-release`. Scope: filesystem action semantics (`--bind`/`--ro-bind`/`--tmpfs`,
  argument order). Anchor: `bwrap.xml:253-255, 295-312, 410-416`.
  Used-by: `scripts/cap-run.mjs`, `scripts/cap-spawn.mjs`, `corpus/lessons/round-47.md`,
  `corpus/knowledge/counter-amendment-discipline.md`, `corpus/knowledge/mount-order-and-bind-scope.md`.
- Adjacent, not the same document: S070 (`:83`) holds bubblewrap **source** `bubblewrap.c`
  at the same commit (code, tier A).

Assessment: true document overlap — two lanes independently pinned the same tag's raw
bytes three days before round 48 (both 2026-10-23 vs tameshi S093 also 2026-10-23) and
both re-verified later. Kumitate re-fetched in its round-50 spotcheck
(`corpus/lessons/round-50-verifier-spotcheck.md:46`: `REOPEN50: HOLD`, fresh curl
sha256 = `2cb77df2…`, exact match) — i.e. kumitate actively maintains freshness of the
same snapshot tameshi re-anchored at S267. **Anchors are disjoint** (kumitate quotes
`:62-67`/`:138-140`/`:217-235`/`:253-255`/`:587-599`; tameshi S267 quotes `:153-160`)
and **no value conflict**: kumitate's quotes (`--clearenv`, PID-1 reaper,
`--die-with-parent`, bind/tmpfs ordering) do not intersect or contradict tameshi's
`--unshare-all` six-flag expansion + `--unshare-cgroup-try` try-else-skip quote. The
`--unshare-*` lines (153–160) are cited by no kumitate row. The blob-page URL form
(`github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml`, tameshi S093/S267 source
cell) is held by no sibling; only the raw form is shared.

## Finding 2 — Google flaky-tests blog 2016: held by NO sibling (tameshi sole holder)

No sibling `corpus/SOURCES.md` (nor any sibling corpus file) contains
`testing.googleblog.com`, "Flaky Tests at Google", or "Micco". Topic adjacency only:
- `kumitate-shokunin/corpus/SOURCES.md:59` S046 — Shi/Bell/Marinov ISSTA 2019
  "Mitigating the Effects of Flaky Tests on Mutation Testing" (paper, tier A, opened
  2026-10-22); `:62` S049 — Alshammari et al. Mutation 2024 flaky de-duplication
  (tier B, rejected). Same subject (flake rates/rerun semantics), different documents,
  no shared URL, no conflicting values.
- `tabi-shokunin/corpus/SOURCES.md:27,32,33,36` — S013/S018/S019/S022 web-flaky
  sources (Playwright retries, ICST 2025 DOM-event paper, KNU record, IEEE abstract).
  Different document set entirely.

Unrelated string matches (not holdings): `kasegi-shokunin/corpus/source-snapshots/round-35/S052.txt`
is a Chrome stable-channel release page enumerating `googleblog.com/2022-2023` URLs;
`revenger-shokunin/corpus/snapshots/dex-format.html` contains a bare `googleblog.com`
string. Neither is a registry row nor cites the flaky-tests post.

## Finding 3 — PIT incremental-analysis page: held by NO sibling (same-host adjacency only)

No sibling registry row carries `https://pitest.org/quickstart/incremental_analysis/`
(nor does any sibling corpus file). Siblings hold other pitest.org pages:
- `kama-shokunin/corpus/SOURCES.md:57` S045 — `pitest.org/quickstart/basic_concepts/`
  (docs, **tier A**, opened 2026-10-20, anchor §Running the tests + commandline
  §`--mutationThreshold`, gh-pages `614bec6`); `:75` S063 — PIT `DetectionStatus.java`
  source at `f7fe5adf` (code, tier A, REJECTED status).
- `kumitate-shokunin/corpus/SOURCES.md:52` S039 — `pitest.org/` + `pitest.org/faq/`
  (docs, **tier A**, opened 2026-10-22); `:65`/`:99` S052/S086 — a Stack Overflow PIT
  question (community, tier C, rejected/superseded).
- `tsukuroi-shokunin/corpus/SOURCES.md:153` S147 — `pitest.org/quickstart/basic_concepts/`
  (docs, **tier B**, REJECTED; snapshot held in-lane, sha256 `c51d8423…`); its teaches
  cell explicitly states "mutation-testing method is tameshi ground (PROVINCE.md
  OUT-010)" — a sibling formally deferring the method province to this lane.

No conflict: no sibling states anything about incremental-analysis item 4/5 or the
"should therefore be prioritised" wording tameshi re-anchored; scopes are disjoint pages.

## Finding 4 — TFF golden_tests zh-cn: held by NO sibling (tameshi sole holder)

No sibling registry row (nor corpus file) contains `tensorflow.org`, `golden_tests`,
`federated`, `黄金测试`, or `update_goldens`. No adjacency whatsoever observed.

## Summary

- Overlap: **1 of 4** documents shared with a sibling — bubblewrap bwrap.xml v0.13.1,
  held by kumitate-shokunin as S069 + S095 (tier A, mined 2026-10-23, on-release,
  same commit + sha256, disjoint anchors, no value conflict, kumitate re-verified the
  bytes in its round-50 spotcheck).
- The other three (Google flaky-tests blog 2016, PIT incremental analysis, TFF zh-cn
  golden tests) are held by no sibling; tameshi is sole holder in each case.
- Conflicts: **none observed**. No sibling states a different value or anchor for any
  of the four documents; where anchors differ (kumitate S069/S095 vs tameshi S093/S267)
  they cite different line ranges of identical bytes with non-intersecting claims.
- Adjacency notes for the record: kumitate/tabi hold flaky-test literature (S046, S049,
  S013–S022); kama/kumitate/tsukuroi hold other PIT pages with tsukuroi S147 explicitly
  deferring mutation-testing method to tameshi ground; kumitate S070 holds bubblewrap.c
  source at the same commit.

## Hygiene

- Read-only on all lane checkouts; the only write is this report file.
- No fixture repos, no counters run, no scratch dirs created (pure grep/read pass) —
  nothing to clean up. No tools installed.
