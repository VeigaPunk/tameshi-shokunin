# T53W2ScoutMisroot — Misroot sweep (wave 2, tameshi round 53)

Seat: T53W2ScoutMisroot · sweep time 2026-10-27 ~13:54 UTC (local ls times below are UTC−3)
Scope: read-only sweep. No files created or deleted by this seat; no fixture needed, so no scratch tree was created (nothing to clean).

## 1. Fleet-root untracked files naming tameshi round 53

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain`

Full output (3 untracked files):

```
?? .scratch/closure-mado-r50.json
?? .ufo/reports/round-53/tameshi.md
?? .ufo/reports/round-63/kake.md
```

In scope (names tameshi round 53):

- `.ufo/reports/round-53/tameshi.md` — 3,593 bytes, mtime Oct 27 10:31 local (13:31 UTC). L1 round-53
  report ("# Tameshi round 53 — cold-read floor repair (calibration) + tools scratch hygiene").
  Per the item's note, the L1 copies+deletes these; this seat reports only.

Out of scope but recorded for completeness:

- `.scratch/closure-mado-r50.json` — names mado round 50, not tameshi r53; also under read-only fleet `.scratch/`.
- `.ufo/reports/round-63/kake.md` — names round 63 (kake), not tameshi r53.

Lane repo (`tameshi-shokunin`) status, supplementary check: only expected wave-2 artifacts
untracked (`.ufo/waves/round-53/w2.ready.dispatched`, `T53W2ConnSources.md`, `T53W2RevContract.md`).
No stray lane files.

## 2. `/fast/scratch/hyaku/tameshi-r53` — seat trees older than this wave

Tree total: 1.5 GB. Wave-2 seat dirs under `w2/` (28 present) are current-wave. Older material:

### 2a. Wave-1 seat trees — all four still on disk (NOT yet deleted)

| path | mtime (local) | contents (sample) |
|---|---|---|
| `w1/T53W1ExecR523` | Oct 27 10:39 | `ctx.pkl` (96 KB), `table.pkl` (33 KB), `repo/` clone |
| `w1/T53W1ExecRegCheck` | Oct 27 10:51 | `SKILL_Cstar.md`, `c1work/`, `c2base/`, `c2work/`, base output |
| `w1/T53W1LabLint` | Oct 27 10:52 | `base_to_c.diff`, `c2base/` clone, `__pycache__/` |
| `w1/T53W1MutCounter` | Oct 27 10:53 | `SKILL.orig.md`, `build_and_mutate.py`, two `c*.measure.orig.py`, `__pycache__/` |

Caveat: these are older than wave 2 but NOT confirmed abandoned. Wave-1 executors T53W1ExecR523,
T53W1ExecRegCheck and T53W1LabLint still show as running in the live roster, and the mtimes above
(10:39–10:53 local = 13:39–13:53 UTC, i.e. minutes before this sweep) show active writes. Deletion
is due at each seat's yield; recommend the L1 re-check this list after wave-1 peers land.

### 2b. Non-seat-named top-level working dirs/files (leftovers by name; owners not identifiable from dir names)

| path | mtime (local) | notes |
|---|---|---|
| `controls-A/` | 10:08–10:09 | `c1-measure.py`, `c2-measure.py`, `base-c1/`, `base-c2/`, `lost-headings.json` |
| `dbg/` | 10:08 | `m.py`, `lh.json`, `w/precheck.sh` |
| `drvtest/` | 10:48 | `r18.py`, `r18b.py`, `__pycache__/` |
| `p2check/` | 10:48 | `tmp/`, `missing/`, seven `*.out` disposition checks |
| `probe-c0/` | 10:16 | `c2/` |
| `probe-c2pp/` | 10:49 | `tmp/`, `registry-check.py`, `env-diff.py` |
| `selftest-check/` | 10:31 | six `*.out` checks (env-diff, repeat-control, pin-disposition, …) |
| `__pycache__/` (top level) | 10:15 | `r18measure.cpython-314.pyc` |
| `lost-at-c0.txt` | 10:17 | 1,675 bytes |
| `r18measure.py` | 10:52 | 76,144 bytes, modified 1–2 min before this sweep — actively used |

Same caveat: mtimes 10:48–10:52 local on `drvtest`, `p2check`, `probe-c2pp`, `r18measure.py` show
live use, consistent with the still-running wave-1 executor peers. Older ones (`dbg`, `controls-A`,
`probe-c0`, `selftest-check`, top `__pycache__`, `lost-at-c0.txt`, 40+ min stale) cannot be tied to
a live seat by name from this sweep — flagged for L1 disposition.

## 3. `/tmp` — tameshi-r53 files over 50 MB

Command: `find /tmp -maxdepth 5 -iname '*tameshi*' -size +50M` → **no matches** (exit 1).
No oversized tameshi-r53 files in `/tmp`.

Informational: 8 r53-named entries exist in `/tmp`, all far under the 50 MB cap (max 208 KB):

| path | size | mtime (local) |
|---|---|---|
| `/tmp/r53w1res.json` | 208 KB | Oct 27 10:04 |
| `/tmp/r53w1d.json` | 176 KB | Oct 27 10:04 |
| `/tmp/r53w2d.json` | 112 KB | Oct 27 10:04 |
| `/tmp/r53c2-sources.md` | 112 KB | Oct 27 10:04 |
| `/tmp/r53c2-lesson.md` | 29 KB | Oct 27 10:05 |
| `/tmp/r53c2-spans.tsv` | 17 KB | Oct 27 10:04 |
| `/tmp/r53-closure.json` | 4 KB | Oct 26 22:13 |
| `/tmp/r53dbg/` | 12 KB (dir) | Oct 27 10:07 (`lh.json`, `m.py`) |

Size rule (`/tmp` only for files under 50 MB) is not violated by any of these; note they live
directly in `/tmp` rather than under a seat scratch tree, and the two oldest are ~13 h old —
reported by name for L1/owner disposition.

## Verdict

- One fleet-root untracked file names tameshi round 53: `.ufo/reports/round-53/tameshi.md` (L1-owned; report-only).
- Four wave-1 seat trees plus nine non-seat-named top-level entries remain under
  `/fast/scratch/hyaku/tameshi-r53` (1.5 GB total); evidence shows most are still being written by
  live wave-1 peers — none confirmed abandoned at sweep time.
- No `/tmp` file over 50 MB; eight small r53-named `/tmp` entries reported as informational leftovers.
- No deletions performed (scout is report-only); no scratch tree created by this seat.
