# T57W1RevInherited — round-57 inherited-state audit (tameshi, wave 1)

Scope: read-only audit of the state the round starts from. No file was edited; the only writes are this report, its JSON, and the receipts directory `T57W1RevInherited-receipts/` (09 files, cited below as `R/NN`, path `.ufo/waves/round-57/w1/T57W1RevInherited-receipts/`). Capture time ≈ 2026-10-28 21:07–21:09 local.

Lane base: `5e3569969b532310d2b8a3d130901757a3df356b`. Tools installed or upgraded: none.

## Verdict

The lane starts clean at base. Its only dirt is this round's own two untracked directories. The fleet root holds no untracked file naming tameshi round 57. Three things need the L1's attention before any counter scores: the contract's `before/` receipts do not exist, a staged `__pycache__` would be installed by `stage-collect.py --install`, and a sibling's receipts sit outside `w1/`.

## Findings (by severity)

### F1 — medium: contract's "before" receipts are absent; counters not installed
- Contract (`.ufo/evidence/round-57/contract.json`) cites `.ufo/evidence/round-57/before/c1.stdout` and `before/c2.stdout` as the base readings (`C1_R57 … rows=0/N … C1_R57_PASS=false`, `C2_R57 … gate_rows=0 … C2_R57_PASS=false`).
- In the lane: `before/`, `after/`, `integrate/`, `c1/`, `c2/`, `control/` exist but have 0 entries; `c1/measure.py` and `c2/measure.py` are absent (they exist only as staged files under `w1/T57W1ExecC1Counter/stage/` and `w1/T57W1ExecC2Counter/stage/`). Command and output: `R/05`.
- Facts I could check against base: the ledger has 49 rows (fixed 31 / open 7 / declined 11, schema `tameshi-routed-defects-v1`), none with an `R5x` id (prefix counts R40–R49 only); the seven spot-check files `round-50..56-verifier-spotcheck.md` are present; `sources-census` validate at base exits 0 (`census-before.exit` = `CENSUS_BEFORE_EXIT=0`). `R/09`.
- Not verified: the `rows=0/N` and `gate_rows=0` readings. They are only reproducible once the counters are installed and run at base. Until then they are contract assertions, not receipts.
- Action for L1: produce the two `before/` receipts from the installed counters before any post-state claim cites them.

### F2 — medium: staged bytecode would be installed by `stage-collect.py --install`
- `w1/T57W1ExecC1Counter/stage/.ufo/evidence/round-57/c1/__pycache__/measure.cpython-314.pyc` is staged. It is git-ignored (`!!` in `git status --ignored`, `R/05`).
- `stage-collect.py` has no pycache or `.pyc` exclusion: `grep -n "pycache\|pyc" stage-collect.py` returns no match (`R/07`). `--install` would copy the bytecode into the lane's `c1/`.
- Action for L1: delete `__pycache__` under every `stage/` tree before install (only one such tree exists right now), or add an exclusion.

### F3 — low: a sibling's receipts are outside the spec'd `w1/` directory
- `T57W1RevCensus-receipts/` sits at `.ufo/waves/round-57/T57W1RevCensus-receipts/`, one level above `w1/`. The spec requires `.ufo/waves/round-57/w1/<seat>-receipts/`. Its contents (`census-before.*`, `census-rerun.stdout`, `gap-classification.tsv`, `missing-ids-S001-S282.txt`, `registry-table-ids-raw.txt`) are still being written (mtime 21:08). `R/07`.
- This is a sibling seat's output; I did not touch it. The owner (T57W1RevCensus) or the L1 should move it into `w1/` when the seat finishes.

### F4 — info: L1 liveness is not visible as its own process
- Watchdog: `1915:2026-10-28T20:35:21-03:00 launch tameshi round=57 pgid=3886721 driver=hyaku-inline attempt=1`. No `lane-dead-no-report tameshi round=57` line exists (grep exit 1, `R/03`). No `complete` line yet.
- `ps` shows no member of pgid 3886721 (`R/08`).
- Dispatcher log: `2026-10-28T21:06:13 spawned tameshi 57 w1 47`; `21:07:09 drive … 'tameshi/w1: live 43/47'`. The 47 seats are children of `omp` pid 923625 (cwd = fleet root, started 11:01:34). That is the inline driver's process, not a tameshi-owned one. `R/08`.
- So the L1 is evidenced as alive by dispatcher log and by w1 artefact mtimes (21:06–21:08), not by a process of its own. No lane-dead condition is present. Recording only; no action beyond noting that the watchdog's pgid is stale for an inline driver.

### F5 — info: fleet root has no round-57 tameshi misroot
- `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all | grep -i "tameshi\|round-57\|round 57\|r57"` → no match (exit 1). `R/04`.
- Tracked: `.ufo/prompts/tameshi-round-57.md` (the L1 prompt, committed at fleet). `.ufo/reports/round-57/` holds chousa, kake, kama, kotoba, kotodama, kumitate, mori — no `tameshi.md`. Expected: `.ufo/state/tameshi.report-baseline` = `57 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (sha256 of the empty string), i.e. the report was absent at launch. `R/04`.
- Fleet index state, outside tameshi round 57, recorded for the orchestrator (not acted on): 0 staged entries; 40 intent-to-add entries (` A`, empty blob `e69de29`, e.g. `o.bin`, `oldrep1.out`, `oldrep2.out`, `.scratch/source-routing-queue.md`, `.scratch/closure-r54/*`, `.scratch/kasegi-r44/*`); 1 modified tracked file `.scratch/goal-20261028-hyaku-run11.md`; 4 untracked (`lane3/`, `.scratch/closure-r54/lane/`, `.scratch/closure-r54/work-c2/clone/`, `.scratch/closure-r54/work-c2-base/clone/`). `R/04`.

### F6 — info: lane tree is clean at base
- `git -C …/tameshi-shokunin status --porcelain` → `?? .ufo/evidence/round-57/` and `?? .ufo/waves/round-57/` only. No tracked modification. HEAD = base (detached). `jj-lane.sh state` → `local=…356df… remote=…356df… ahead=0 behind=0 head=detached tracked=0 untracked=2`. No stash; the only worktree is the lane. `R/01`, `R/02`.
- The lane's `refs/heads/hyaku/*` and `refs/jj/keep/*` predate this round and were not touched.
- Ignored `__pycache__` under older frozen evidence dirs (`.ufo/evidence/round-50/c1/`, `round-52/…`, `round-55/…`, `round-56/c2/`) is bytecode left by earlier runs, not a frozen-path edit. `R/05`.

### F7 — info: authorship of round-57 untracked files
- All files are owned by `vgpnk` (one OS user), so ownership does not identify seats. Authorship here is by filename prefix, the seat roster, and content headers. `R/06`, `R/07`.
- L1 (`TameshiR57`) artefacts, by content: `contract.json` (`"l1": "TameshiR57"`), `w1.ready` (`"l1":"TameshiR57"`), `w1.ready.dispatched` (dispatch roster), `build-spec-w1.py`, `spec-w1.json`, `w1-dispatch.json`, `stage-collect.py`, `census-before.stdout`/`.exit`, `swarm-registry.json` (`"wave": "round-57-w1"`).
- The 22 seat directories under `w1/` each map to a roster seat in `w1.ready.dispatched` (47 roster entries). None is unattributed. Five roster entries have a retry spawn id differing from the directory name (`T57W1ExecControls-2`, `T57W1ExecNoHarm-2`, `T57W1ExecDeciding-2`, `T57W1ExecForecast-3`, `T57W1ExecRegistryRows-2`). `R/07`.
- `w1-validate.stderr` is 0 bytes (`R/06`).

### F8 — caveat, not a finding: raw spot-check counts vs contract
- A crude pattern (`^[0-9]+\. |^- \*\*R`) over the spot-check files gives r50 4, r51 12, r52 6, r53 9, r54 0, r55 7, r56 7. Contract expects r50 4, r51 8, r52 6, r53 9, r54 10, r55 7, r56 7. The pattern does not match round 54's heading format, and it counts non-routed numbered lists. Two rows (r51, r54) do not reconcile under this pattern. That is the extractor's job (`T57W1ExecExtract`); I did not run the extractor. Recorded so the extractor's count is checked against the contract's 51 total, not against mine.

### Observed, not interpreted
- `.ufo/state/tameshi.round` contains `1` while the round is 57; `kotoba.round` contains `16` and `kumitate.round` `18`. The meaning of `.round` was not found in `scripts/hyaku`, so no conclusion is drawn.

## Commands run (all read-only; receipts in `T57W1RevInherited-receipts/`)
- `git -C <lane> status --porcelain`; `jj-lane.sh state <lane>`; `git rev-parse HEAD`, `stash list`, `worktree list`, `for-each-ref` → `R/01`, `R/02`.
- `grep lane-dead-no-report|tameshi|round=57 .ufo/watchdog.log` → `R/03`.
- `git -C <fleet> status --porcelain [--untracked-files=all]`, `diff --cached --name-only`, `ls-files -s`, `ls-files` for round-57 paths → `R/04`.
- `git status --porcelain --ignored -- .ufo/waves/round-57 .ufo/evidence/round-57`, `find`/`ls` of `before/ c1/ …`, `git ls-tree` at base → `R/05`.
- `stat` owner/mtime, `head` of authorship files, `cat w1.ready`, `census-before.exit`, `wc -c w1-validate.stderr` → `R/06`.
- Python roster-vs-artefact check; `grep pycache stage-collect.py`; `find … __pycache__` in stage trees → `R/07`.
- `ps -o … -p 923625,923390`; `/proc/*/stat` pgid scan for 3886721; `ps` of tameshi-r57 processes; dispatcher-log grep; state-file reads → `R/08`.
- Python ledger shape check; `git cat-file -e` for the seven spot-check files; `git show … | grep -c` counts → `R/09`.

## Verification gaps
- Counters (`c1/measure.py`, `c2/measure.py`) were not run; their before-readings are unverified (F1).
- `contract.json` was not re-derived against the frozen set; only its base facts (49 rows, census exit 0) were checked.
- The L1's own liveness was inferred from logs and artefact timestamps; no direct probe of the L1 session was made (F4).
- Nothing was built, linted, or tested; this seat's assignment did not call for it.
