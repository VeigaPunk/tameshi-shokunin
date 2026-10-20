# SectionHashes — wave-2 falsification of cold-read section bucketing

**Verdict: HOLDS.** An independent reimplementation of the sectioning rule reproduces
`assemble.py`'s per-bucket sha256 exactly on both files (105 positions, 65 unique
buckets, 0 disagreements). Between `e69b488:SKILL.snapshot.md` and
`c699c8c3:SKILL.md`, 11 buckets changed sha and 3 new buckets were appended;
the bucket-shas themselves are computed correctly by the shipped script.

## What was attacked

`.ufo/evidence/round-16/coldread/assemble.py::sectionize` — the claim that sections
= heading-to-heading (preamble = start 1, heading ""), text = lines joined by `\n`
after stripping trailing whitespace-only lines, sha256 per bucket, and that buckets
are correctly keyed/compared across the two SKILL files.

## Method (independent code)

`$SCRATCH=/tmp/tameshi-r16w2-SectionHashes-1792504312`. Own sectioner written from
the contract text (`my_sections.py`, ~45 lines): headings = `^#{1,3}` followed by
whitespace/EOL, skipped inside fenced blocks; section = heading line through line
before next heading; trailing whitespace-only lines stripped; sha256 over
`"\n".join(body)`.

File acquisition (committed bytes only):

```
git -C tameshi-shokunin show e69b488:.ufo/evidence/round-16/coldread/SKILL.snapshot.md > snapshot.md
git -C tameshi-shokunin show c699c8c3:SKILL.md > skill.md
git -C tameshi-shokunin show c699c8c3:.ufo/evidence/round-16/coldread/assemble.py > assemble.py
```

sha256 evidence: snapshot.md `97cf436b…580`, skill.md
`3d8a1edb…b7a4` — matches the pinned skill sha `3d8a1edb…` from the wave spec.
snapshot has 1704 lines / 51 sections; post SKILL.md 1795 lines / 54 sections.

## Differential vs assemble.py

Ran the committed script on a /tmp worktree (`wt/` with the two skill files placed
at their repo-relative paths):

```
cd wt && python3 .ufo/evidence/round-16/coldread/assemble.py \
  --skill .ufo/evidence/round-16/coldread/SKILL.snapshot.md --skill SKILL.md \
  --out $SCRATCH/ledger.json   # exit=1 (no reports globbed → all sections "missing")
```

`ledger.json` `_meta.missing` carries every bucket's sha/start/end/heading from
assemble.py's own sectionize. Cross-check vs my sectioner:

- positions checked: 105 (51 snapshot + 54 SKILL.md)
- disagreements (sha, end, heading): **0**
- unique bucket sha sets: equal (65 buckets)

Edge-case survey of inputs: no `~~~` fences, no `####` headings, no indented
fences, no `#nonspace` heading lines — so the rule differences that *do* exist
between the implementations (assemble.py anchors fences at column 0 and accepts
`~~~`; mine allows leading whitespace; heading regexes equivalent) are
inert on these two files. [INFERENCE: on other inputs with column-0 vs indented
`~~~` fences the two could diverge; not triggered here.]

## Buckets whose sha changed (snapshot e69b488 → SKILL.md c699c8c3)

My sectioner, compared by `start` line (11 changed):

| start | heading | pre sha | post sha |
|------:|---------|---------|----------|
| 6 | `# tameshi-shokunin` | c3344d0c2391c0cb | 8200ed3851a7462e |
| 58 | `## Gate-shape decision table — hermetic vs live vs audit-lane` | 93f142621f18f2a0 | 79cd9cde2069ca9d |
| 131 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 9441176ef6f469f2 | c7247157d06ec252 |
| 246 | `## Defect-taxonomy templates and exact-string guidance` | b593581a4f4770a0 | a4f86492f72883d4 |
| 314 | `## Kill-rate bands — admission readings (rounds 2–3, measured)` | 0f18a08fe755c0b1 | 455545e97decab6e |
| 497 | `## Fail-closed arm taxonomy` | cce85bd4513ca8e3 | e6b977739cd34935 |
| 921 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | b861ccb67f5e91c2 | 8e92a785d3a4bb11 |
| 933 | `### Using the ledger` | 6a692e9404de3850 | 80ce092dba57c1c3 |
| 1380 | `### The map — where a reader enters, artifact by artifact` | 6bacad37cae530c5 | 45441353347fe77a |
| 1464 | `## Promotion-evidence calibration — fleet round-1` | a450fe34dd57e7e5 | 76c6929815b2b84e |
| 1609 | `## Context gate classification and explicit exit classes — round 15` | 16a693dac842c976 | 132cfb9ef1aa0711 |

New buckets in c699c8c3 (starts not present in snapshot — appended at tail):

| start | end | heading | sha |
|------:|----:|---------|-----|
| 1707 | 1739 | `## Errata — round 16 full-page cold-read (append-only)` | 798a280ce2f9… |
| 1740 | 1788 | `## Seventh recorded case and full-page cold-read — round 16` | 0cd4e2c9a715… |
| 1789 | 1796 | `### Round-16 gate/probe registry` | 2a36432225c5… |

No bucket was removed or reordered: every snapshot start exists in SKILL.md, and
all post-file headings ≥1707 are new. All 39 pre-sha buckets not listed above are
sha-identical across the two files (assemble.py's sha-keyed merge correctly pools
them — its own output shows single missing entries with two positions).

Consistency check: `diff snapshot.md skill.md` has 15 hunks
(`15c15 63c63 134,135c134,135 271,272c271,272 278,280c278,280 361c361 505c505
514,515c514,515 925c925 950c950 1390c1390 1393c1393 1472c1472 1614c1614
1705c1705,1796`), each falling inside exactly the changed/new sections listed.

## Observation worth flagging (not a disagreement)

Section `start=1676` (`### Round-15 gate/probe registry`) has `end=1705` in
snapshot vs `end=1706` in SKILL.md but **identical sha** `7544ca694055…`: the
SKILL.md edit added a whitespace-only line at 1706 inside that section, which the
strip-trailing-blank rule absorbs into the same bucket. This means a seat's
`end` differs across pins while its sha does not — correct per the rule, but a
w1 report pinned to end=1705 and a w2 report pinned to end=1706 describe the same
ledger entry. Both implementations agree on this, so it is a rule property, not
a bug.

## Disagreements

None. Sha256 of sections, section boundaries, bucket identity, and the
changed/new-bucket partition all match between the independent implementation
and the committed `assemble.py` output.

## Commands executed (key lines above)

- `git show e69b488:…/SKILL.snapshot.md`, `git show c699c8c3:SKILL.md`, `git show c699c8c3:…/assemble.py` (all exit 0)
- `sha256sum` → skill.md `3d8a1edb…` (pin verified)
- `python3 my_sections.py snapshot.md skill.md` (exit 0; 51 + 54 sections)
- `python3 wt/.ufo/evidence/round-16/coldread/assemble.py --skill … --skill … --out ledger.json` (exit 1 — expected: no seat reports in the /tmp worktree; ledger.json written with all 105 positions in `_meta.missing`)
- position-by-position comparison script: `disagreements: 0`, `unique buckets mine: 65 ledger: 65 equal: True`

No tool installs needed (stdlib python3, git). Scratch: `/tmp/tameshi-r16w2-SectionHashes-1792504312` (contains my_sections.py, both skill files, my_out.jsonl, ledger.json, wt/ worktree).
