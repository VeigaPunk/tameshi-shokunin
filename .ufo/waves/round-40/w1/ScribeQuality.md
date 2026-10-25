# ScribeQuality — QUALITY criterion 79 draft (mined quote needs committed snapshot)

## Task

Draft QUALITY criterion 79: a mined quote is not citable support unless a
committed snapshot contains it. Cite `considerthese/2026-10-24.md` proposal 3
(date 2026-10-24) and the S108 snapshot. The reflection is a pointer, not
evidence. Do not edit `considerthese/` or `QUALITY.md`; do not edit the live
lane checkout.

## Headline finding

A complete, correctly-cited `### Criterion 79` draft **already exists in the
working tree** at `corpus/QUALITY.md:944-960`. It is **uncommitted**: HEAD is
`5641ed84c8dc148c34c8dd83f062279ddf06b4af` (the contract-freeze commit), and the
working-tree delta vs `HEAD:corpus/QUALITY.md` is exactly +18 lines at end of
file (942 → 960 lines), the draft and nothing else; file mtime 2026-10-24
21:48:03 -0300, after the 21:33 freeze commit. `git log -S'Criterion 79' --
corpus/QUALITY.md` returns no commits — it has never been committed. I did not
create or modify it; recorded as found pre-existing work (author unknown to me).

## Draft text (verbatim, `corpus/QUALITY.md:944-960`)

    ### Criterion 79 — a located quote needs a committed snapshot

    A mined row that presents a located quote as support is not citable until a
    committed snapshot contains that quote. A live fetch that cannot be repeated,
    or a page whose quote is split by markup, is not a substitute for the bytes.
    Unreachable is not fabrication: the quote is unverifiable until the snapshot
    lands. A status edit does not replace the snapshot.
    Lesson: `corpus/lessons/round-40.md`, and `considerthese/2026-10-24.md`
    proposal 3, mined 2026-10-24, not edited. The reflection pointed at repeatedly
    unreachable sources; the evidence is the round-39 closure's redirect-loop on
    S108 and the snapshot pinned this round.
    Falsifier that must fail: `python3 .ufo/evidence/round-40/s108/measure.py
    --lane LANE --rev 304e3355705640af2879c772fc9a5c2902c61763` prints
    `snapshot_absent=1 C2_R40_PASS=false` and exits 1. The same command at
    `5641ed84c8dc148c34c8dd83f062279ddf06b4af` prints `quote_in_snapshot=1
    stripped_quote_fails=1 C2_R40_PASS=true`. Removing the prefix
    `可以通过使用参数` from a copy of the snapshot must make the quote check fail.

Wording vs. mandate: task said "a mined quote is not citable support unless a
committed snapshot contains it"; the draft's "not citable until a committed
snapshot contains that quote" is equivalent and stronger (names the mined row
and the located quote).

## Citation chain verified (all observed, nothing inferred)

| Citation element | Check | Result |
|---|---|---|
| Proposal 3 exists | `considerthese/2026-10-24.md:68-69` | "**Persistently unreachable sources.** The gnu.org Bash manual pages timed out in rounds 32, 34, 35 and 36. I could keep a list of sources that have failed repeatedly… and suggest pinned alternatives" |
| Pointer, not evidence | `considerthese/2026-10-24.md:61` | Heading: `## Self-improvement ideas (proposals only, not acted on)` — proposal 3 is a suggestion; the draft correctly cites it as Lesson provenance, not as the falsifier |
| Date 2026-10-24 | `considerthese/2026-10-24.md` filename + line 1; file window 2026-10-21→24 | Matches "mined 2026-10-24" |
| S108 snapshot | `.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` | 111405 bytes; `sha256sum` = `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0` = `contract.json` claims.C2.snapshot_sha256 |
| Quote present | raw `golden_tests.zh-cn.html:3611` carries it split by `<code>` tags; tag-stripped text contains the contiguous quote (scratch strip; ScoutS108 independently reports stripped byte offset 4819 via `measure.py`'s exact `stripped_text()`) | `quote_in_snapshot=1` |
| Round-39 redirect loop | `corpus/lessons/round-40.md:31` (round-39 closure could not re-open the URL, redirect loop, no snapshot); `corpus/lessons/round-39.md:16-17` (S108 mined with quote, no snapshot) | Confirms draft's evidence sentence |
| "Row stays mined; status edit ≠ snapshot" | `corpus/lessons/round-40.md:31` ("The row stays mined. No status,…"); `:51` quote-split row names "criterion 79" | Confirms draft's final two rule sentences |
| Style conformance | `### Criterion N — title` blocks at `QUALITY.md:903` (76), `:916` (77), `:931` (78); draft at `:944` follows identically | Consistent |

## Falsifier lines verified against committed receipts

The draft's falsifier names `python3 .ufo/evidence/round-40/s108/measure.py
--lane LANE --rev REV` at the base and frozen revs. The frozen contract
(`contract.json`, pinned at `5641ed84`) fixes both revs and the predicate. I did
**not** run the counter in default mode (that deciding run is reserved for the
L1); the committed receipts say exactly what the draft claims:

- `.ufo/evidence/round-40/before/c2-at-base.stdout`:
  `C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 stripped_quote_fails=0 rev=304e3355705640af2879c772fc9a5c2902c61763 C2_R40_PASS=false`
  and `.ufo/evidence/round-40/before/c2-at-base.exit` = `1`. Matches falsifier line 1.
- `.ufo/evidence/round-40/after/c2-at-5641ed84.stdout`:
  `C2_R40: snapshot_absent=0 quote_in_snapshot=1 sha_ok=1 stripped_quote_fails=1 rev=5641ed84c8dc148c34c8dd83f062279ddf06b4af C2_R40_PASS=true`
  and `.ufo/evidence/round-40/after/c2-at-5641ed84.exit` = `0`. Matches falsifier line 2.
- Prefix-removal clause: on a scratch copy I deleted `可以通过使用参数` (occurs
  exactly once in raw bytes, line 3611) → the tag-stripped text no longer
  contains the quote. Corroborates `stripped_quote_fails`; the counter itself
  implements this via a `QUOTE_REMOVED` marker at `measure.py:77-79`.

## Commands run (auditable)

- `sha256sum .ufo/evidence/round-40/s108/golden_tests.zh-cn.html` → `f27cf2…782bf0`
- `wc -c` same file → `111405` (matches `corpus/lessons/round-40.md:31`)
- `git -C <lane> log -1 --format='%H %ad %s'` → `5641ed84… 2026-10-24 21:33 round-40: freeze C1 write-form census and C2 S108 snapshot pin before data`
- `git show HEAD:corpus/QUALITY.md` → `/tmp/tameshi-r40-ScribeQuality/QUALITY-HEAD.md`; `diff -q` vs worktree → differ; `diff -u` → single +18-line EOF hunk (the draft)
- `git log -S'Criterion 79' -- corpus/QUALITY.md` → empty (never committed)
- Python scratch: tag-strip of the snapshot (quote found) and of the
  prefix-removed copy (quote absent) — read-only repro, not the counter
- `grep` for proposal/quote/lesson anchors listed in the table above

## Bounds honored

No edits to `considerthese/`, `corpus/QUALITY.md`, `contract.json`, `.ufo/state`,
the Git index/`.git`, or any lane file. Scratch confined to
`/tmp/tameshi-r40-ScribeQuality/`. Counters not run in default mode; only
committed receipts were read. No tools installed (none needed).

## Out-of-scope / handoff

- Whether the uncommitted draft lands (gets committed) is the L1's call; it is
  staged-in-place but outside the freeze commit, so `git show
  5641ed84:corpus/QUALITY.md` does not contain it — citation "QUALITY.md:944" is
  a working-tree address until then.
- No defect found in the draft; no rewrite proposed. Calibration read: the
  draft is complete, correctly cited (pointer labeled pointer), and its
  falsifier is byte-exact against committed receipts.

Confidence: high.
