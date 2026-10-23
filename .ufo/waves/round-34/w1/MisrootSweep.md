# MisrootSweep — tameshi round-34 w1

Verdict: no fleet-root untracked file names a tameshi round-34 seat. `.ufo/state` and `.ufo/watchdog.log` are git-dirty, and the dirt is driver-shaped (baseline round integers; append-only watchdog lines). No round-34 seat id, scratch path, or seat report body is in that dirt. Nothing here was moved or deleted. Tool installs: none.

Scratch clone (read-only lane checkout, not the live worktree): `/fast/scratch/hyaku/tameshi-r34-seats/MisrootSweep/lane`, detached at `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Live lane HEAD during the sweep was already `a5b1936425d3533b2ce280b16208386dcb0dc4ee` (orchestrator; this seat did not commit). Parent ignore rule `.gitignore:1:*-shokunin/` hides the lane from fleet-root status (`git check-ignore -v`, exit 0).

## Pins (tip `0b99d48e`, scratch clone)

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/MisrootSweep/lane
```
exit 0.

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/tameshi-r34-seats/MisrootSweep/lane \
  checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C \
  /fast/scratch/hyaku/tameshi-r34-seats/MisrootSweep/lane rev-parse HEAD
```
checkout exit 0, rev-parse exit 0, stdout `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh
sha256sum tool.py pristine.sh lane/tools/tally-audit-v2.py lane/tools/mutate-and-run.sh
```
`git show` exit 0, 0. `sha256sum` exit 0. `cmp` of show-bytes vs checkout working tree exit 0, 0. Clone `git status --porcelain` empty, exit 0.

| file | sha256 | pin |
|---|---|---|
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | match |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | match |

Same two digests on the live tree at `a5b19364` (`sha256sum` of `tameshi-shokunin/tools/tally-audit-v2.py` and `tools/mutate-and-run.sh`, exit 0). Kill-rule counter was not run.

## Fleet-root status

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin status --porcelain
```
exit 0 both times. Fleet HEAD at the first snapshot: `34ea4ecb418f23d35b4734837dee3891626d3456` (`round-34: tameshi report`). By the closing snapshot (2026-10-23T16:44:33-03) HEAD was `9f966367582294f8037be224810a3935f58ff954` (`round-27: mado report`, commit time 16:43:36-03). That commit is another lane. This seat's fleet commands were status, diff, show, rev-parse, ls-files, check-ignore, and cat-file only.

Closing porcelain (33 lines; the only line present in the first snapshot and absent here is `?? .ufo/reports/round-27/mado.md`, which that commit absorbed):

```
 M .scratch/goal-20261023-hyaku-24h.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M .ufo/waves/hyaku/PHASE5.md
 M scripts/hyaku/hyaku.env
?? .omp/mcp.json
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
?? 0
?? AGENTS.md
?? bm.json
?? live.html
?? live_s228.html
?? nama.html
?? s395.txt
?? scripts/hyaku/__pycache__/
?? scripts/hyaku/append-closure.py.bak-20261023T040735Z
?? scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z
?? tf_bavelas.html
?? wb2.html
?? write
?? xc.xml
```

`-uall` expands `__pycache__/` to `append-closure.cpython-314.pyc` (10738 bytes) and `wave-live.cpython-314.pyc` (10708 bytes). No other untracked paths.

## Content scan (the misroot test)

Needles: the 64 `members` keys in `tameshi-shokunin/.ufo/waves/round-34/w1/swarm-registry.json` (`"wave": "round-34-w1"`, `createdAt` `2026-10-23T19:38:49.417Z`), the 64 `"name"` strings in `dispatch-w1.json`, plus `tameshi-r34`, `tameshi round-34`, `tameshi round 34`, `round-34-w1`, `MisrootSweep`, `tally-audit-v2`, `tameshi-r34-seats`, `/waves/round-34/`, `C1_R33`. Search was latin-1 over every byte, including the two `.pyc` files.

Result: 19 files, 0 needle hits. A second pass (`tameshi|round-34|round 34|Misroot|tally-audit`, case-insensitive) was also 0 hits on those 19 files.

`?? .ufo/reports/round-27/mado.md` was in the first porcelain only. After `9f966367` it is tracked (`git ls-files -v` → `H .ufo/reports/round-27/mado.md`, exit 0; path-limited `status --porcelain` empty, exit 0; `check-ignore` exit 1). Rescan of the working-tree bytes: 0 hits for the same needles, including bare `tameshi` and `round-34`. Other lane; not touched.

Named untracked bodies that are short enough to quote, none of which are seat ids:

| path | bytes | body |
|---|---|---|
| `0` | 31 | `NF=13 cells=11 double_quotes=0` |
| `write` | 25 | `agent://U100N079H334f935b` |
| `s395.txt` | 0 | empty |
| `.ufo/state/kotoba.report-baseline` | 68 | `61 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/state/kotodama.report-baseline` | 68 | `63 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/state/revenger.report-baseline` | 68 | `62 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `xc.xml` | 237 | Perseus "Too many requests" HTML |
| `wb2.html` | 620 | Wayback Machine bot-block HTML |
| `.omp/mcp.json` | 285 | `mcpServers.rea` disabled npx stanza |

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is SHA-256 of the empty string. The three untracked baselines are the same driver record as the tracked ones, for other lanes.

Larger untracked files scanned and not quoted (`AGENTS.md` 5921, `bm.json` 5563, `live.html` 57113, `live_s228.html` 5196, `nama.html` 68855, `tf_bavelas.html` 5583, both bak files, both pyc files): 0 hits. Left in place.

## Driver files — dirty, not seat-written

`git diff --stat -- .ufo/state .ufo/watchdog.log` exit 0:

```
 .ufo/state/chousa.report-baseline   |   2 +-
 .ufo/state/kagi.report-baseline     |   2 +-
 .ufo/state/kaidoku.report-baseline  |   2 +-
 .ufo/state/kake.report-baseline     |   2 +-
 .ufo/state/kama.report-baseline     |   2 +-
 .ufo/state/kengaku.report-baseline  |   2 +-
 .ufo/state/kumitate.report-baseline |   2 +-
 .ufo/state/mado.report-baseline     |   2 +-
 .ufo/state/mori.report-baseline     |   2 +-
 .ufo/state/tameshi.report-baseline  |   2 +-
 .ufo/state/tsukuroi.report-baseline |   2 +-
 .ufo/watchdog.log                   | 354 ++++++++++++++++++++++++++++++++++++
 12 files changed, 365 insertions(+), 11 deletions(-)
```

Each tracked baseline is one line, round integer only, hash unchanged. tameshi, from `git show HEAD:.ufo/state/tameshi.report-baseline` (exit 0) vs the worktree:

```
-23 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
+34 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Worktree mtime of `tameshi.report-baseline` is 2026-10-23 16:09:09-03. Watchdog append (`git diff -- .ufo/watchdog.log`, exit 0, 354 added lines) includes the matching driver line and no registry seat id:

```
2026-10-23T16:09:11-03:00 launch tameshi round=34 pgid=3367092 driver=hyaku-inline attempt=1
```

Added watchdog lines are `launch` / `complete` / `lane-dead-no-report` records (`driver=hyaku-inline`). They do not contain `tameshi-r34`, `MisrootSweep`, `tally-audit-v2`, `/fast/scratch/hyaku/tameshi`, or any of the 64 seat ids. `.ufo/watchdog.log` mtime 2026-10-23 16:38:14-03 is the last of those driver lines (`launch kumitate round=49`), not a seat write.

`git diff` of the other three tracked dirt paths (exit 0) is hyaku orchestrator text: `.scratch/goal-20261023-hyaku-24h.md`, `.ufo/waves/hyaku/PHASE5.md`, `scripts/hyaku/hyaku.env`. The only added line containing the string `MisrootSweep` is PHASE5 naming a kama seat's earlier look at the same stray paths (`0`, `write`, `s395.txt`, `bm.json`, the html files, `xc.xml`) as not kama r29. That line is not a tameshi seat file and was not edited here.

## Lane worktree (not fleet-root status)

`git -C tameshi-shokunin status --porcelain -uall` exit 0, during the sweep, listed only:

- `?? .ufo/waves/round-34/w1/swarm-registry.json` and sibling seat reports landing in that directory (authorized report dir, not this file).
- `?? .ufo/evidence/round-34/dev/c1-deciding-run.{stdout,exit,stderr}` — stdout 245 bytes and exit 2 bytes, byte-equal to the tracked `measure/c1-deciding-run.*` counterparts; stderr 0 bytes. mtimes 16:25:10 and 16:27:43-03, before registry `createdAt` 19:38:49Z. Pre-wave duplicates, not a round-34 seat stray at the fleet root. Not touched.

No misroot finding.
