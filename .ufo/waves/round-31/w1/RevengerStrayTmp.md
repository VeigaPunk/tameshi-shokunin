# RevengerStrayTmp — owner of `/tmp/tameshi-r4-2-regression.j0FKnk` and clone `tameshi-registry-check-i272er4j`

Seat: `TameshiR31.RevengerStrayTmp` (round 31, wave 1). Scope: round-30 closure routed defect 6.
Verdict first, then evidence. Read-only; nothing deleted or modified. All times UTC (host
local time is UTC-3, so `04:22 -0300` below = `07:22Z`).

## Verdict

**Owner: `TameshiR30A3.ColdA08`** — a round-30 wave-C reviewer seat in session
`2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7` (project dir
`-Projects-shokunin`).

- The clone `/tmp/tameshi-registry-check-i272er4j` was created by `tools/registry-check.py`
  via `tempfile.mkdtemp(prefix="tameshi-registry-check-", dir="/tmp")`
  (`tameshi-shokunin/tools/registry-check.py:766`), invoked by ColdA08's own tool call:
  `bash` call `bash:0#2086ce8dd9614be2a7a817f318591f69` (entry id `88ac577c`, started
  `2026-10-23T07:20:56.156Z`) — the command
  `cd /tmp/ColdA08-Uc3O/fleet/tameshi-shokunin && timeout 500 python3 tools/trace-inputs.py
  --root /tmp/ColdA08-Uc3O/fleet/tameshi-shokunin --out
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-24-3.json
  -- timeout 330 python3 tools/registry-check.py --rev bb681566b18211adf8ae9c28df91e17678e3f545`
  (`.../TameshiR30A3/TameshiR30A3.ColdA08.jsonl:61`).
- The workdir `/tmp/tameshi-r4-2-regression.j0FKnk` was created inside that clone's
  registry-replay by the registry's `mutate-regression` row, via `mutate-and-run.sh`'s
  `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` (`tools/mutate-and-run.sh:1360`;
  template contract at `tools/mutate-and-run.sh:142` and
  `.ufo/evidence/round-16/coldread/SKILL.snapshot.md:936-939`: scratch removed on PASS,
  kept on FAIL/SETUP — a killed run keeps the workdir).
- Cause of death: the seat's own `timeout 330` inner bound. registry-check was still live
  at `07:26:11Z` (process 3608014, mid `bash-checklist-run` leg) and hit its ~07:26:26Z
  deadline; `timeout` SIGTERM killed it mid-replay. ColdA08 honestly recorded the gap in
  its report (`wC/ColdA08.md:103`, `:185`) and receipt `ColdA08-24-3.json` (exit 124).
- The clone `i272er4j` is already removed (registry-check's `--rev` SIGTERM/`finally`
  cleanup; `stat` → "No such file or directory"). The workdir survives because
  mutate-and-run keeps its scratch on non-zero exit.

## Evidence chain

1. **Both paths stated/listed (bounded).**
   `stat /tmp/tameshi-r4-2-regression.j0FKnk` → dir, Birth `2026-10-23 04:22:05 -0300`
   (07:22:05Z), Modify/Change `04:25:37 -0300` (07:25:37Z). `ls` (bounded): leg dirs
   `bash-checklist-run`, `bash-mado-verify`, `bash-surface-census`, `bash-tsukuroi-census`,
   `js-kimi-census` (04:22–04:25) plus `specs` — exactly the mutate-and-run leg layout.
   `stat /tmp/tameshi-registry-check-i272er4j` → ENOENT; `ls -d /tmp/tameshi-registry-check-*`
   shows 7 other registry-check clone dirs, not this one. Of 35 sibling
   `/tmp/tameshi-r4-2-regression.*` dirs, j0FKnk is the only Oct-23 one (all others Oct-22).

2. **Bounded transcript searches (as assigned).**
   `timeout 120 grep -rl --include=*.jsonl -e j0FKnk /home/vgpnk/.omp/agent/sessions/` →
   16 files, all in session `2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7`
   (round-30 `TameshiR30A3` Cold* seats, closer `HyakuCloseTameshi30`, plus round-31 routing
   echoes including this seat's own transcript).
   Same search for `i272er4j` → 9 files; repeated without `--include` → +1 file
   (`.../HyakuCloseTameshi30/HyakuCloseTameshi30.CloseBreaches-2.md`), same sessions only.
   **No transcript contains `i272er4j` as an invocation** — expected, since the mkdtemp
   suffix is generated inside registry-check.py and never appears on the invoker's command
   line.

3. **Decisive capture — `TameshiR30A3/TameshiR30A3.ColdA01.jsonl:143`** (tool-result,
   timestamp `"2026-10-23T07:26:11.229Z"`, produced by the seat's `pgrep -af
   'mutate-and-run|trace-inputs'` at `ColdA01.jsonl:141`). It shows:
   - `3608014 bash /tmp/tameshi-registry-check-i272er4j/fleet/tameshi-shokunin/tools/mutate-and-run.sh
     --target /tmp/tameshi-r4-2-regression.j0FKnk/bash-checklist-run/target.checklist-run.sh
     --defects /tmp/tameshi-r4-2-regression.j0FKnk/specs/bash-checklist-run.spec --suite bash
     "$MUTANT" --selftest --workdir /tmp/tameshi-r4-2-regression.j0FKnk/bash-checklist-run
     --label bash-checklist-run …` — linking clone ↔ workdir in one live process;
   - `1784804 python3 tools/trace-inputs.py --root /tmp/ColdA08-Uc3O/fleet/tameshi-shokunin
     --out …/traces/ColdA08-24-3.json -- timeout 330 python3 tools/registry-check.py --rev
     bb681566b18211adf8ae9c28df91e17678e3f545` and `1785396 /usr/bin/strace -f …
     --kill-on-exit …` — the only `registry-check` invocation running anywhere at 07:26Z
     (all other pgrep entries are other seats' mutate-and-run/trace-inputs). ColdA08's
     `registry-check.py` is the only process that can create a `tameshi-registry-check-`
     clone (the sole `mkdtemp` site, `registry-check.py:766`).

4. **Owner's own tool call — `ColdA08.jsonl:61`** (id `88ac577c`, ts `07:20:56.156Z`):
   the `trace-inputs … -- timeout 330 registry-check.py --rev bb681566…` command quoted in
   the Verdict. Workdir birth 07:22:05Z lands inside this run's replay. A second attempt,
   `timeout 75` instead of 330, is at `ColdA08.jsonl:100` (id `e77c5a9d`, ts `07:27:59.316Z`);
   it rewrote receipt `ColdA08-24-3.json` (mtime 04:29 -0300), which records
   `argv: timeout 75 … registry-check.py --rev bb681566…`, `exit: 124`, cwd/root
   `/tmp/ColdA08-Uc3O/fleet/tameshi-shokunin` (`traces/ColdA08-24-3.json:3-15`). The stray
   workdir is from the 330 s attempt — the 75 s attempt started after j0FKnk's mtime and
   died on an earlier row.

5. **Corroboration.** Round-30 L1 `TameshiR30A3.jsonl:280` (07:21:34Z) shows the wave-C
   assignment instructing a `timeout 1200 python3 tools/registry-check.py` base-vs-target
   compare; ColdA08 was assigned recipe step 3 (cold-read §24). Sibling rosters at
   07:26:3x–07:27:02Z show `TameshiR30A3.ColdA08 — reviewer (running): Waiting for
   registry-check trace to finish` (e.g., `ChousaR32A2.NoHarmAfter32.jsonl:11`,
   `TameshiR30A3.jsonl:366`'s own receipt line `ColdA08-24-3`). Report
   `wC/ColdA08.md:103`/`:185` records "it did not finish inside 75 s … or 330 s … exit 124
   under timeout, receipt ColdA08-24-3". Strace leftovers persist:
   `/tmp/trace-inputs-run-xzle19pz/trace.log` (368 MB, mtime 04:26 -0300 — the 330 s run's
   kill point).

6. **Ruled out.** The earlier owner hypothesis space (wave-C seats collectively, the L1,
   `ColdA01`'s pgrep kill): `ColdA01`'s kills targeted `pgrep -f 'ColdA01'` matches only;
   the i272er4j/j0FKnk command lines contain no `ColdA01` string, and its errata name a
   different workdir (`1e5R9E`, `ColdA01.jsonl:150,173,188,197,199`). Closer
   `HyakuCloseTameshi30` investigated and reached "owner unidentified" (`HyakuCloseTameshi30.jsonl:152`,
   `CloseBreaches-2.jsonl:103–116`) — this report supersedes it: the missing link was that
   the invoker's command line never names the mkdtemp suffix, so a suffix-grep over the
   store finds only observers, not the creator.

## Confidence

High. The 07:26:11Z live-process capture binds clone `i272er4j` to workdir `j0FKnk` inside
ColdA08's only-concurrent `registry-check --rev` run; the seat's own call (`ColdA08.jsonl:61`,
07:20:56Z) brackets the workdir birth (07:22:05Z); tool templates are the unique
mkdtemp sources (`registry-check.py:766`, `mutate-and-run.sh:1360`); receipt and report
self-document the timeout kill. Residual uncertainty: the ~6 s between `timeout 330`'s
deadline (~07:26:26Z) and workdir mtime (07:25:37Z) — explained by writes stopping before
the term, not by an external killer; nothing contradicts it.

## Searched (negative space)

`grep -rl` (with and without `--include=*.jsonl`) over all of
`/home/vgpnk/.omp/agent/sessions/` for `j0FKnk`, `i272er4j`; a scan of all 10,083 `.jsonl`
files for lines containing `registry-check` with timestamps in 06:50–07:59Z (no other
invocation found); `registry-check` greps over `-Projects-shokunin-tameshi-shokunin`,
`-tmp*`, and today's other `-Projects-shokunin` session dirs (06-51 session empty; 06-20
contains only `eval.log`); `/tmp` listing for both names and for entries created in the
incident window; `stat`/`ls` on both paths.

No tooling installed or updated (grep/stat/find/Python only); no pacman transactions.
