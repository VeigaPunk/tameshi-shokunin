# T49ExecIdGuard — assimilation id-collision check and guard proof (round 49, wave 1)

Seat: leaf executor, read-only on the lane except this file and `.ufo/waves/round-49/w1/T49ExecIdGuard/`.
Scratch: `/fast/scratch/hyaku/tameshi-r49/T49ExecIdGuard` (created and deleted inside this wave; not citable).
I decide no claim. Every counter run below is `--selftest`, `--json` (analysis) or `--map` (admissibility probe), never a deciding run.

## 0. Base provenance of the bytes read

| artifact | sha256 | note |
|---|---|---|
| `corpus/SOURCES.md` | `7e99c6a068521cf3e3d581a52a74e8f58551309ecb2c3a284dda9b9c17235c7e` | identical to the base blob (`git -C <lane> cat-file -p 8ca67421…:corpus/SOURCES.md \| sha256sum`); lane HEAD is `455b2cd6…`, but `git -C <lane> status --porcelain corpus/SOURCES.md tools/staged-id-guard.py` is empty |
| `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` | `020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807` | the staged package, read-only |
| `tools/staged-id-guard.py` | `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` | equals the contract's `named_gate` sha256; never edited |

Receipt `w1/T49ExecIdGuard/source-hashes.txt`, `lane-head.txt`.

## 1. The id-collision check (item step 1)

```
S=/fast/scratch/hyaku/tameshi-r49/T49ExecIdGuard
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $S/reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > $S/staged-ids
comm -12 $S/reg-ids $S/staged-ids > $S/collisions
```

Observed (`wc -l`): registry **128**, staged **103**, collisions **8** — `S153 S154 S155 S156 S157 S158 S159 S160`.
The extraction agrees with the guard's own parser on both sides (`registry_rows` 128, `staged_rows` 103, `.ufo/waves/round-49/w1/T49ExecIdGuard/guard.json`), and the staged count matches the count already recorded at `corpus/SOURCES.md:269` ("103 staged rows").
Receipts `reg-ids`, `staged-ids`, `collisions`.

## 2. The guard proof (item step 2)

Two scratch copies of the registry, each with one appended S-id row carrying staged S182's document (the QuickCheck DOI):

| fixture | row indent | `^ {0,3}\|…` extractor | column-zero-only extractor | guard run |
|---|---|---|---|---|
| `reg-indented2.md` (row at file line 491) | 2 spaces | 129 ids, **9 collisions** (the 8 + **S182**) | 128 ids, 8 collisions, **S182 missed** | `registry_rows=129`, `collisions` 9 incl `S182` |
| `reg-indented4.md` | 4 spaces | 128 ids, 8 collisions (row invisible) | 128 ids, 8 collisions | `registry_rows=128`, `collisions` 8 |

Commands: the same three-step pipeline per fixture plus
`python3 -I <lane>/tools/staged-id-guard.py --registry $S/reg-indented{2,4}.md --staged <append> --json`.
Receipts `reg-indented{2,4}.md`, `reg-indented{2,4}-ids`, `reg-indented{2,4}-col0`, `reg-indented{2,4}-collisions`, `reg-indented{2,4}-col0collisions`, `reg-indented{2,4}.guard.json`.

Conclusion the proof supports: the collision file is nonempty for an indented row **only** because the pattern binds 0–3 leading spaces; a column-zero pattern would have false-greened it. The 4-space fixture shows the extractor's edge, and that edge is the census's own rule (`scripts/sources-census.sh:40` "Maintained parser accepts 0–3 leading ASCII spaces", `:541` `table_re='^ {0,3}\|'`, `:615`), so 0–3 is the correct bound, not a limb.

Two corrections to how the guard's own fields may be read (observed, not edited — the guard is a pinned capability):

- `column0_collisions` / `column0_miss` are computed over the **staged** text only (`tools/staged-id-guard.py:136-138`), yet the docstring calls them "the indented-row proof" (`:52`) without naming the side. For a registry-side indented row (this item's fixture) the fields stay `[]` and prove nothing; the standalone column-zero pipeline above is what proves it.
- On the 2-space fixture the guard reports `held: {"S182": "S182"}` (self-dedupe: the fixture registry row carries the same DOI). Adoption probes on that fixture are refused for the right reason: `mapE-fixture-selfmap` → `map leaves a colliding id on itself: S182`; `mapF-fixture-held-moved` → `map moves a held document off its registry id: S182 -> S290 (registry S182)`. So the fixture proves extraction only, never an adoption.

Selftest on the real tool: `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS` (receipt `selftest.out`).

## 3. Guard output on the real registry/staged pair (item step 3)

```
python3 -I <lane>/tools/staged-id-guard.py --registry <lane>/corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
```
exit 0, receipt `guard.json`:

| field | value |
|---|---|
| `collisions` | `S153 S154 S155 S156 S157 S158 S159 S160` (8) |
| `held` | `S153→S105, S154→S106, S155→S261, S158→S262, S159→S155, S160→S156` (6) |
| `unmapped` / `cascade` | `[]` / `[]` |
| `refused` / `verdict` | `false` / `answered` |
| `next_free` / `safe_floor` | `S269` / `S269` (from `registry_max` S268 and `staged_max` S255) |
| `registry_rows` / `staged_rows` / `registry_docs` | 128 / 103 / 109 |

The six `held` dedupes are document-verified against the registry rows they name: POSIX `diff` at `corpus/SOURCES.md:117` (staged `SOURCES.append.md:7`), `golden.go` at `:118` (`:8`), arXiv 2302.09330 at `:136` (`:9`), the Lam et al. camera-ready at `:137` (`:12`), PIT basic concepts at `:125` (`:13`), PIT FAQ at `:126` (`:14`). Two collision rows are **not** held and need fresh ids: staged S156 (arXiv 2406.09843 , `SOURCES.append.md:10`) and staged S157 (doi 10.21105/joss.01891, `:11`). Both documents exist in the lane only as unopened leads (`corpus/SOURCES.md:278` JOSS 01891, `:279` arXiv 2406.09843), never as rows, which is why the guard cannot dedupe them.

## 4. The quarantine slice (item step 4)

The item's awk returns **17** rows (`quarantine-tameshi-slice.txt`), from two tables of `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`:

- 14 `payload-absent` rows, lines 215–228;
- 3 never-checked rows, lines 363–365 (`S113`, `S123`, `S134`), whose id cell carries a stray backtick (`S134\``) and which the register's own "By lane" count (line 240: `| \`tameshi\` | 14 |`) does not include.

Distinct slice ids: `S105 S109 S110 S113 S118 S119 S123 S124 S126 S129 S131 S132 S134 S137 S140 S141 S143`.

**S182 and S183 are not in the slice, and appear zero times anywhere in the register** (`grep -c 'S182'` = 0, `grep -c 'S183'` = 0; receipts `quarantine-S182-hits.txt`, `quarantine-S183-hits.txt`). By **document**:
- staged S182's document `doi.org/10.1145/351240.351266` **does** appear — register line 365, id `S134`, class "the cited source could not be fetched, so no quote was checked" (the never-checked table, not the fabrication class). The lane already reconciled it: `corpus/lessons/round-40.md:67` records S134 as *present* — "the DOI opens through the campaign's own `aaron` channel and the quote is locatable".
- staged S183's document `smallbone.se/papers/lic.pdf` appears **nowhere** in the register (`grep -c -i smallbone` = 0, `grep -c -i 'lic\.pdf'` = 0).

How the slice must be joined (receipt `quarantine-doc-crosscheck.txt`): of the 17 register ids only **`S105` and `S132`** exist in the lane registry; the other **15** do not (`S109 S110 S113 S118 S119 S123 S124 S126 S129 S131 S134 S137 S140 S141 S143`). An id-keyed quarantine lookup is therefore not a quarantine check at all — the same reason the guard decides by document. Joined **by document**, **53 of the 103** staged rows cite a document that also carries a flagged quote, while **0** staged anchors contain one of the quarantined quote spans; each of those 53 still owes a per-quote check, and `corpus/SOURCES.md:269`'s recorded "Quarantine 0 (the tameshi slice S105–S143 intersects none)" is an id-range statement that cannot see any of them.

## 5. Recommended renumber map for the two rows — by document

Rules the map is judged by are the guard's own (`tools/staged-id-guard.py:29-37`, `:180-270`): a target that is a registry id is admissible only as the dedupe of that id's document; any other target must be a fresh id at or above the safe floor `S269`, must not be an id another staged row still holds, and the map must cover every collision.

Probes run against the real pair (receipts in `w1/T49ExecIdGuard/`):

| map | entries | guard verdict | reason |
|---|---|---|---|
| `mapA` (the eight collisions decided) | 8 | **admitted** | six dedupe + `S156→S269`, `S157→S270` |
| `mapB` (mapA + `S182→S271`, `S183→S272`) | 10 | **admitted** | recommended |
| `mapC` (only `S182→S269`, `S183→S270`) | 2 | refused | `map does not cover every collision: S153…S160` |
| `mapD` (`S182→S182`, `S183→S183`) | 10 | refused | `map targets are still staged ids: S182,S183` |
| `mapG` (identity over the whole package) | 103 | refused | `still staged ids` (95) + own-id + held-moved reasons |
| `mapH` (collisions decided, 95 reserved ids kept) | 103 | refused | `map targets are still staged ids: S161…` (95) |

**Recommendation (by document, never arithmetic):**

| staged row | document | decision | target |
|---|---|---|---|
| `SOURCES.append.md:36` S182 | QuickCheck, Claessen & Hughes, ICFP 2000, `doi.org/10.1145/351240.351266` (tier A) | registry holds no row with this document → fresh id | **S271** |
| `SOURCES.append.md:37` S183 | Smallbone, Chalmers TR 76L 2011, `smallbone.se/papers/lic.pdf` (tier B) | registry holds no row with this document → fresh id | **S272** |
| `:10` S156 | arXiv 2406.09843 | not held → fresh id | S269 |
| `:11` S157 | `doi.org/10.21105/joss.01891` | not held → fresh id | S270 |
| `:7,8,9,12,13,14` S153/S154/S155/S158/S159/S160 | POSIX diff / golden.go / 2302.09330 / Lam / PIT basic / PIT FAQ | held → **adopt nothing** | cite S105 / S106 / S261 / S262 / S155 / S156 |

Why S271/S272 and not S269/S270: a map must cover all eight collisions, and two of them (S156, S157) cannot dedupe, so two fresh ids necessarily exist below the two package rows. Fresh ids are then issued in the package's own row order (lines 10, 11, 36, 37), which is a document ordering, not `max+index` — the naive arithmetic map (`guard.json` `naive_map`, `S153→S269 … S160→S276`) is refused precisely because it counts. If the L1 prefers a different but still admissible assignment (any injective set of ids ≥ S269 disjoint from the staged ids), the two rows' ids change with it; what is not optional is that they are **fresh ids ≥ S269 taken from their documents**, because a map may not leave a row on its staged id (mapD/mapG/mapH).

Consequences the integration and the C2 pilot must carry:

1. the pilot entry cites **S271/S272**, and the ids follow the documents, so the citation is correct only if the map above (or one that keeps those two targets) is the one adopted;
2. the admitted copy of `knowledge/corpus/knowledge/r4-quickcheck-primary-correction.md` cites `S182`/`S183` at lines 2, 3, 20, 33, 39, 48, 54-55, 64, 66 (source file is read-only); every one of those citations must be re-pointed by document to the adopted ids, which is the guard's own rule (`tools/staged-id-guard.py:8`);
3. the lane's allocation ledger says the opposite of what a map can do — `corpus/SOURCES.md:484,488,490`: "staged ids S161–S255 stay reserved by document for the package". Any map-based adoption refuses exactly that (mapH: 95 `still staged ids`), so the ledger line needs a correction or the adoption must splice rows at reserved ids without a map (then S182/S183 stand and no renumber happens). That is the L1's call; the contract's `frontier_step` ("staged S182/S183 … re-numbered") points at the map path;
4. the same ledger's latest `Next unused id: S265` (`corpus/SOURCES.md:490`) is stale: S265–S268 are written rows (`:140-143`), and the guard's `next_free`/`safe_floor` are `S269`.

## 6. Findings with locations

| # | finding | evidence |
|---|---|---|
| 1 | 8 id collisions, six of them document-held dedupes, two needing fresh ids | `guard.json`; `corpus/SOURCES.md:117,118,125,126,136,137` |
| 2 | the collision sets agree between the item's extractor and the guard's parser | 128/103/8 vs `registry_rows`/`staged_rows`/`collision_count` |
| 3 | an indented (2-space) row is caught by 0–3 and missed at column zero — the guard's pattern is load-bearing | `reg-indented2-collisions` (9) vs `reg-indented2-col0collisions` (8) |
| 4 | 4-space indentation is blind to both patterns, matching the census's 0–3 rule | `reg-indented4-collisions`; `scripts/sources-census.sh:40,541,615` |
| 5 | guard's `column0_*` fields measure the staged side only, docstring doesn't say | `tools/staged-id-guard.py:52,136-138` |
| 6 | S182/S183 are absent from the quarantine register by id; S182's document is there as never-checked `S134`, S183's is absent | register lines 365, 240; `quarantine-*-hits.txt` |
| 7 | the slice cannot be joined by id: 15 of its 17 ids are not lane-registry ids | `quarantine-doc-crosscheck.txt` |
| 8 | 53 staged rows cite a document with a flagged quote; 0 staged anchors match a quarantined span — per-quote checks are owed | `quarantine-doc-crosscheck.txt` |
| 9 | `corpus/SOURCES.md:269`'s recorded "Quarantine 0" is an id-range check and cannot see finding 8 | `corpus/SOURCES.md:269` |
| 10 | the reserved-block ledger line and the guard's map rule conflict | mapG/mapH refusals vs `corpus/SOURCES.md:484,488,490` |
| 11 | the ledger's "next unused id" is 4 behind the registry | `corpus/SOURCES.md:490` vs `:140-143`, `guard.json` `next_free=S269` |

## 7. Receipts

`w1/T49ExecIdGuard/`: `reg-ids`, `staged-ids`, `collisions`, `guard.json`, `guard.err`, `selftest.out`,
`reg-indented2.md`, `reg-indented4.md`, `reg-indented{2,4}-ids`, `reg-indented{2,4}-col0`,
`reg-indented{2,4}-collisions`, `reg-indented{2,4}-col0collisions`, `reg-indented{2,4}.guard.json`,
`mapA|B|C|D-keep-staged-id|G-identity-whole-set|H-reserved-identities|E-fixture-selfmap|F-fixture-held-moved.json` and `.out.json`,
`quarantine-tameshi-slice.txt`, `quarantine-tameshi-count.txt`, `quarantine-S182-hits.txt`, `quarantine-S183-hits.txt`,
`quarantine-doc-crosscheck.txt`, `source-hashes.txt`, `lane-head.txt`.

## 8. Tooling

No install or upgrade: everything above ran on `python3 -V` = 3.14.8 (stdlib only) and coreutils/gawk. No pacman, uv, npm or binary install was attempted; no `~/.local/bin` change.

## Summary

Eight ids collide (S153–S160); six are document-held dedupes to S105/S106/S261/S262/S155/S156, two (S156 arXiv 2406.09843, S157 JOSS 01891) need fresh ids at the safe floor S269.
The guard admits a map only if it covers all eight collisions and never leaves a row on its staged id; identity and reserved-block maps are refused (95 `still staged ids`).
Recommended by document: staged S182 → **S271** and staged S183 → **S272** (both documents unheld), with S156→S269, S157→S270 in package row order — this map (mapB) is admitted by the guard.
The pilot entry must therefore cite S271/S272, and the admitted r4-quickcheck entry's S182/S183 citations must be re-pointed by document.
The guard proof holds: a 2-space-indented `| S182 |` registry row yields 9 collisions under `^ {0,3}`, 8 at column zero; 4-space rows are blind, matching the census's 0–3 rule.
Quarantine: S182/S183 are absent by id; S182's DOI is register line 365 (never-checked `S134`, reconciled at `round-40.md:67`), S183's document is absent entirely.
The slice must be joined by document, not id — 15 of its 17 ids are not lane-registry ids, and 53 staged rows cite a document with a flagged quote (0 anchor matches).
`corpus/SOURCES.md:484-490`'s reserved-block and `next unused S265` lines conflict with the guard and with the registry's actual max S268.
