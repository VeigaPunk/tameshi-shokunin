# RunSourcesCount — round24 W1 SOURCES.md census

Seat: TameshiR24-2.RunSourcesCount · 2026-10-21 · lane: tameshi-shokunin

## Verdict

Census clean. Delivered c8c5b88 `corpus/SOURCES.md` has **83 S-rows, 0 malformed rows (every row exactly 11 cells), tier A74/B7/C2, status mined54/queued23/rejected6**. Versus base 6a1821a: **+2 rows, added ids S084 and S085, 0 removed, +2 tier A, +2 mined**; all other tier/status/kind buckets unchanged. No defects found; no correction required.

## Commands (exact argv, cwd, exit)

Setup (per assignment, in /tmp only):

```
argv: rm -rf /tmp/RunSourcesCount-r24 && git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/RunSourcesCount-r24 && git -C /tmp/RunSourcesCount-r24 checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909 && git -C /tmp/RunSourcesCount-r24 rev-parse HEAD
cwd:  /home/vgpnk/Projects/shokunin
exit: 0   → HEAD = c8c5b88c8e961a929cdc351b95a7074c76958909, CLONE_OK
```

Assigned Run command (delivered):

```
argv: GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c8c5b88c8e961a929cdc351b95a7074c76958909:corpus/SOURCES.md
cwd:  /home/vgpnk/Projects/shokunin/tameshi-shokunin
exit: 0
```

Base comparison (same form):

```
argv: GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6a1821a8897eea6e7d9669292160ec9593669409:corpus/SOURCES.md
cwd:  /home/vgpnk/Projects/shokunin/tameshi-shokunin
exit: 0
```

Analysis pass: Python (eval kernel) parsing both blob texts in memory via `git show` + `git rev-parse <rev>:corpus/SOURCES.md`; independent cross-checks with `wc -l`, `grep -c '^| S[0-9][0-9][0-9] '`, `awk -F'|'`, and `git diff --numstat` — all read-only, all with `GIT_OPTIONAL_LOCKS=0`.

## Exact counts

| metric | delivered c8c5b88 (blob `d93709c43f6f713946748e0b33b6f0ef197b5287`) | base 6a1821a (blob `2ad7e2d1998cf69e6018ae4d31d87562dcedf866`) | Δ |
|---|---|---|---|
| file lines (`wc -l`) | 307 | 298 | +9 |
| pipe-rows | 85 (= header + delimiter + 83 S-rows) | 83 (= header + delimiter + 81 S-rows) | +2 |
| S-rows | **83** | **81** | **+2** |
| malformed rows (≠11 cells) | **0** | **0** | 0 |
| tier A / B / C | 74 / 7 / 2 | 72 / 7 / 2 | +2 A |
| status mined / queued / rejected | 54 / 23 / 6 | 52 / 23 / 6 | +2 mined |
| kind docs / own-work / paper / code / spec / book / community / tool | 38 / 6 / 19 / 11 / 4 / 2 / 2 / 1 | 37 / 5 / 19 / 11 / 4 / 2 / 2 / 1 | +1 docs, +1 own-work |
| duplicate ids | none | none | — |

Id set: S001..S085 monotonic; gaps exactly S038, S039 — documented as "allocated, never written, retired" in the file's own §Id allocation, present in both revisions. Removed ids: none.

## Added ids (decisive lines)

Both added rows sit contiguously at the end of the registry table (delivered lines 93–94, 11 cells each, opened 2026-10-21):

- **S084** @line 93 — kind `docs`, tier `A`, status `mined` — "os.path — Common pathname manipulations (Python docs) — https://docs.python.org/3/library/os.path.html" (realpath canonical-path semantics; used-by replay-projection-hardening.md, round-24.md).
- **S085** @line 94 — kind `own-work`, tier `A`, status `mined` — "Round23 routed critic defects — .ufo/waves/round-23/fresh-adjudication.json" (routed_not_executed lines53–104 @ revision 6a1821a…; used-by replay-projection-hardening.md, round-24.md).

Tail of delivered output (exit line `EXIT=0`): the round24 search-log block "Round24 bounded lookup: opened the routed round23 adjudication (own-work) and the Python os.path reference for realpath; identified2/screened2/included2/excluded0. New tierA/mined rows S084 and S085; no existing row changes." then `- Next unused id: S086.`

Diff corroboration: `git diff --numstat 6a1821a..c8c5b88 -- corpus/SOURCES.md` → `9  0  corpus/SOURCES.md` (2 row lines + 7 appended log lines, nothing deleted).

## Falsification (what I attacked; no defect found)

- Recounted S-rows two extra ways: `grep -c '^| S[0-9][0-9][0-9] '` → 83 / 81 (matches parser); `awk -F'|'` over rows matching `/^\| S[0-9]/` → NF=13 (leading pipe + 11 cells + trailing pipe) for **all** rows in both revisions, i.e. zero malformed under a delimiter-based method that does not share code with the regex parser.
- Tier/status re-derived by awk column position ($5 tier, $9 status) → identical distributions (A74/B7/C2; mined54/queued23/rejected6 delivered; A72/B7/C2; mined52/queued23/rejected6 base).
- Checked for escaped-pipe / wrapped-row hazards: cell splitter handles `\|`; every pipe-row is a single physical line; pipe-row total (85/83) is exactly header+delimiter+S-rows, so no stray pipe rows outside the registry table.
- Checked id hygiene: no duplicate ids; monotonic order; only gaps are the two documented-retired ids (present in both revs, so not introduced by this round).
- Line-count conflict resolved: the interactive reader displayed "of 309/300"; two content-pinned measures agree (`wc -l` = 307/298; Python `splitlines()` on the exact blob = 307/298) — reader display accounting, not a file property. Blob oids above pin the compared content.

## Bounds compliance

No tool installs or upgrades performed (none needed — nothing to record). Only read-only git (`show`, `rev-parse`, `diff --numstat`) against the main repo with `GIT_OPTIONAL_LOCKS=0`, plus the assignment-specified /tmp clone; writes limited to this report file. No producer-authentication, promotion, R17-CMD-BIND-closure or score-uplift claim is made; counts above are observations only.
