# T48W2SentinelScratch — operability: `/tmp` writes, leftover clones, network (round 48, a2w1)

Seat: sentinel (operability). Item: audit the two frozen round-48 counters
(`.ufo/evidence/round-48/calibration/measure.py`, `.ufo/evidence/round-48/freshness/measure.py`)
and `.ufo/evidence/round-48/control/run-controls.py` for (a) writes under `/tmp` regardless of
`TMPDIR`/`--work`, (b) leftover clones after a run, (c) network use outside the C2 live check;
report path:line findings; inspect `/fast/scratch/hyaku/tameshi-r48/` for finished wave-1 seat
dirs (names + sizes, never delete others').

Lane `tameshi-shokunin` at base `473336d9d789f6081195e7376d17836a24666bc3`; counters frozen at
`755298415f8c`. Read-only on the lane: the only lane write is this file. Nothing under `corpus/`,
`tools/`, `SCORECARD.md` was touched. No tool installed.

Context that makes the `/tmp` axis load-bearing: contract **amendment 10** declines the
V-relative dependence rule *because* "the round-48 counter refuses `--work` under `/tmp`, so P1 is
stable there". A `/tmp` escape in either counter is therefore not cosmetic — it can change a
`dep_mismatch` reading. §7.4 of the seat bounds is the lane rule being audited.

## Verdict

| # | severity | path:line | defect (one line) |
|---|---|---|---|
| F1 | medium | `freshness/measure.py:382`, `:662` | `mkdtemp()` with no `dir=` and no guard: a `TMPDIR` that is unset or unusable silently falls back to `/tmp`; 43 `/tmp` trees in one `--selftest` (measured). C2 has no `--work` and no refusal, so nothing in the program prevents it. |
| F2 | medium | `calibration/measure.py:106-117` + `:591`, `:842` | `scratch_root()` falls back to the **shared** `/fast/scratch` and creates `c1-r48-<rand>` there; no `rmtree` of that root exists, so a seat probe without `TMPDIR` leaves an unattributable tree outside every seat subtree (observed, 3.0 MB). |
| F3 | medium | `calibration/measure.py:450-451`, `:461-462`, `:466-468`; `deciding-run.sh:20,37` | clone cleanup is not exception-safe: `return 2` on clone failure and any raise from `fut.result()` skip the per-round `rmtree`; `deciding-run.sh` has no `trap`, so an interrupted run (attempt 1 died in a host crash) leaves the whole round tree (~1.8 GB). |
| F4 | low-med | `control/run-controls.py:307-310` vs docstring `:34` | the "outside `/fast/scratch`" guard is a printed **note**, then `os.makedirs(work)` and five `git clone`s proceed: `--work /tmp/x` clones the lane under `/tmp` while the docstring claims it "never touches … /tmp". |
| F5 | low | `control/run-controls.py:187`, `:247`, `:402` | five `--shared` clones and the counter run dirs are never removed; it prints `work=<dir>` per tree but has no cleanup and no `--keep`. |
| F6 | low | `freshness/measure.py:184-194` (called `:344`) | the only network path (allowed: this *is* the C2 live check), but `resp.read()` is unbounded, redirects are followed by default, and the URL comes from a committed receipt with no host allowlist. |
| F7 | info (decisive) | `statements.json` → `tools/{repeat-control,pin-disposition,evidence-disposition,env-diff,tally-audit-v3,mutate-and-run}` | the C1 counter's own code is `/tmp`-clean, but **7 of its 22 statements run tools that hardcode `/tmp`** (`dir="/tmp"`, `mktemp -d /tmp/…`): 7 × 6 profiles × 3 rounds = **126 `/tmp` writes per deciding C1 run**, immune to the profile `TMPDIR`. Live leaks on this host right now (12 × 6.7 MB). Carried from w1 §6, now with frozen line numbers and live evidence. |

Clean, and safe for the L1 to rely on (evidence below): C1's `--work`-under-`/tmp` refusal
(`:396-397`, before any write, control `T63`); C1's per-round clone deletion including the last
round (`:466-468`); C1's selftest writing **zero** `/tmp` paths with `TMPDIR` unset; C2's
`finally` removals (`:393`, `:845`); C2 with `TMPDIR` set writing **zero** `/tmp` entries over 43
cases; `run-controls` giving every counter child `TMPDIR` under `--work` (`:250-253`); and network:
**only** `live_fetch`.

## Probes (command → observed)

All probes ran with `S=/fast/scratch/hyaku/tameshi-r48/T48W2SentinelScratch`; `--selftest` only,
scratch trees only, never against the lane worktree, no counter judged.

| # | command | observed |
|---|---|---|
| P1 | `strace -f -e trace=mkdir,openat,… python3 .ufo/evidence/round-48/freshness/measure.py --selftest` with `TMPDIR` **unset** | `C2_R48_SELFTEST: cases=43 failed=0`; trace shows **43** distinct `/tmp/c2-r48-census-*` trees (each materialising `corpus/SOURCES.md` + every used-by blob) and `/tmp/c2-r48-selftest-*` (4025 file ops). |
| P2 | same, `TMPDIR=$S/ok` (existing, writable) | `0` occurrences of `/tmp/c2-r48`; all 43 census trees under `$S/ok/`. |
| P3 | `TMPDIR=$S/does-not-exist python3 -c 'import tempfile;print(tempfile.gettempdir())'` | `gettempdir: /tmp` → `mkdtemp` created `/tmp/c2-r48-selftest-q3kj6ovz`. Python's silent fallback is the mechanism of F1. |
| P4 | `TMPDIR` **unset**, `strace … calibration/measure.py --selftest` | root chosen `/fast/scratch/c1-r48-2irlnhtd`; **zero** `/tmp` paths in a 20 MB trace (C1 is `/tmp`-clean); interrupted by the job cap at 300 s. |
| P5 | `TMPDIR=$S/ok python3 .ufo/evidence/round-48/calibration/measure.py --selftest` | `C1_R48_SELFTEST: cases=76 failed=0` / `VERDICT: PASS` in 256 s; `$S/ok` **empty** afterwards (per-case dirs removed, `:847`). |
| P6 | `/fast/scratch/c1-r48-2irlnhtd` after P4 | 3.0 MB, created 10:33:46; still present at 10:36 (no `rmtree` of that root exists); gone by 10:40 — removed by another actor, **not** by the counter. A second tree `/fast/scratch/c1-r48-xkbewgrm` (1.7 MB, contains `lane/` + `work/`) exists now and is **not mine**. |

## F1 — C2 falls back to `/tmp` silently (medium)

*Attacks:* the lane's `/tmp` rule at the only place C2 can be run without a caller-supplied work
dir; and the harness's ability to *claim* a scratch-clean probe.

```
382:    work = tempfile.mkdtemp(prefix='c2-r48-census-')
393:        shutil.rmtree(work, ignore_errors=True)
662:    root = tempfile.mkdtemp(prefix='c2-r48-selftest-')
845:        shutil.rmtree(root, ignore_errors=True)
```

No `dir=`, no `under_tmp`-style refusal, and the CLI (`:852-861`) has **no `--work`**: the only
control is ambient `TMPDIR`. Python's `tempfile.gettempdir()` silently substitutes `/tmp` when
`TMPDIR` is unset, relative, non-existent or unwritable (P3), so `mkdtemp` writes `/tmp` and says
nothing. Reproduced: 43 census trees in `/tmp` from one `--selftest` (P1).

*Impact.* (1) A seat that follows the documented probe (`--selftest`, no `TMPDIR`) writes the host
`/tmp` — the exact thing the lane rule forbids — 43 times per invocation. (2) The dirs are removed
in `finally`, so the residue appears only on SIGKILL/timeout: up to a full materialised registry +
blobs per case. (3) Collision surface: many concurrent seats use one fixed prefix in the shared
`/tmp`; today `/tmp` carries 292 entries / 499 MB (363 MB of it an appimage mount, the rest other
seats' trees), so this is not hypothetical cross-talk. (4) Unlike C1 (`:396`), C2 cannot detect that its scratch was `/tmp`, so a
receipt cannot show the difference.

*Smallest remediation.* Resolve the root once at startup, C1-style: `TMPDIR` if set, `realpath`
outside `/tmp`, and writable, else exit 2 with a message; then `mkdtemp(..., dir=root)` at both
sites. ~6 lines, no behaviour change when `TMPDIR` is valid.

## F2 — C1's fallback root lands at the shared `/fast/scratch` and is never removed (medium)

```
106: def scratch_root():
108:     for cand in (os.environ.get('TMPDIR'), '/fast/scratch'):
...
591:     root = scratch_root()
842:         d = tempfile.mkdtemp(prefix='c1-r48-', dir=root)
847:             shutil.rmtree(d, ignore_errors=True)      # per case only
```

When `TMPDIR` is valid, `root` *is* `TMPDIR` and nothing new is created (P5: clean). When it is
unset or unusable, `root` becomes `/fast/scratch` and the counter creates
`/fast/scratch/c1-r48-<rand>` there — **outside** the mandated per-seat subtree
`/fast/scratch/hyaku/tameshi-r48/<SeatName>/` — and no code path removes that directory
(`grep -n rmtree` finds only `:468`, `:490`, `:847`, all sub-dirs of `--work`/`root`). Observed:
`/fast/scratch/c1-r48-2irlnhtd`, 3.0 MB, from my `TMPDIR`-unset probe (P4/P6); a second
`/fast/scratch/c1-r48-xkbewgrm` (1.7 MB) is present now from another seat.

*Impact.* Stray trees at a shared root with **no seat attribution**: nobody can tell whose tree it
is, so cleanup is unsafe (the seat rule forbids deleting others' dirs), and the fault is invisible
in the seat's own directory. Two concurrent `TMPDIR`-unset probes also share one parent, which is
the definition of cross-seat interference the rule exists to prevent.

*Smallest remediation.* Drop the `/fast/scratch` fallback (exit 2 with the existing message at
`:115`) or make it seat-scoped (`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r48/<seat>`); and
`rmtree(root)` in a `finally` only when the counter created it (i.e. `root != TMPDIR`).

## F3 — C1 clone cleanup is not exception-safe; the deciding run has no trap (medium)

```
449-451:  if made is None:
              print('C1_R48: clone/checkout failed', file=sys.stderr)
              return 2                    # ← before the cleanup loop
461-462:       for key, f in futs.items():
                   results[key] = f.result()      # ← can raise (OSError etc.)
466-468:       for prof in PROFILES:              # cleanup starts only here
```

The per-round clone removal runs **after** results are collected, with no `try/finally` around the
round body. Any failure inside the round — clone/checkout failure (`:451`), a `subprocess` raise
surfacing through `fut.result()` (`:462`), or SIGTERM/SIGKILL — leaves that round's clones. Scale:
the lane is 229 MB and `setup_profile` makes **12** `--no-hardlinks` clones per round (6 profiles ×
`clone` + `fleet/<lane>`), i.e. ~1.8 GB/round (w1 measured 1,864,620 KB; consistent with the live
`L1/ctl/run-CTL_B` = 1.9 GB).

`deciding-run.sh` is the only thing that removes the work tree, and it does so on the **last
line** (`:37 rm -rf "$SCR"`) with `set -u` and no `trap`: an interrupted deciding run — the actual
failure mode of attempt 1 — leaves `$SCR` with a round's clones behind. (Currently
`/fast/scratch/hyaku/tameshi-r48/deciding` does not exist, so nothing is leaking from this
invocation.)

*Smallest remediation.* wrap the round body in `try: … finally: <per-profile rmtree>`, and add
`trap 'rm -rf "$SCR"' EXIT INT TERM` immediately after `mkdir -p "$SCR"` (`:20`).

## F4 — `run-controls.py`'s `/tmp` guard is inert (low-medium)

```
34:  never touches the lane checkout, the fleet repo, /tmp, the lane's jj state or its Git index.
...
307:      print('run-controls: note: --work %s is outside /fast/scratch' % work, file=sys.stderr)
310:  os.makedirs(work, exist_ok=True)
```

The docstring asserts a `/tmp` prohibition; the code prints a **note** and proceeds to
`os.makedirs` + five `git clone -q --shared` (`:187`) into `--work`. `--work /tmp/x` therefore
clones the lane 5× under `/tmp`, writes `CTL_*.stdout`/`.stderr`/`run-*/` there, and exits 0.
`os.path.abspath` at `:306` correctly neutralises `/fast/scratch/../tmp/...`, and the child
`TMPDIR` is always under `--work` (`:250-253`) — so the escape is limited to the caller's own
`--work`, but the claimed invariant is false. Compare the frozen C1 counter, which hard-refuses
(`:396-397`) before creating anything. I did **not** run it with `--work /tmp/...`: doing so would
create the very tree this finding describes.

*Smallest remediation.* make it `raise HarnessError('--work must be under /fast/scratch')`, i.e.
the same refusal the counter uses.

## F5 — `run-controls.py` leaves its clones (low)

`:247` removes only the counter's own run dir before a run; nothing removes the five committed
trees it made at `:187`. Observed live in `L1/ctl`: `CTL_A..CTL_E` 152 MB each (760 MB) plus the
counter run dirs (`run-CTL_A` 109 MB, `run-CTL_B` 1.9 GB) and `tmp` 5.2 MB — 2.7 GB under one
`--work`. The script prints `work=<dir>` per tree (`:402`), so the footprint is visible but never
reclaimed; there is no `--keep`.

*Smallest remediation.* add `--keep` (default off) and `rmtree` the five trees at exit; or state in
the header that `--work` is the seat's to delete (it already is, by lane rule).

## F6 — the allowed network path (low, bounded)

```
184: def live_fetch(url, timeout=60):
185-187:  req = urllib.request.Request(url, headers={'User-Agent': 'tameshi-c2-r48/1.0 …'})
188:     with urllib.request.urlopen(req, timeout=timeout) as resp:
193:         raw = resp.read()
344:         cache[url] = ('raw', fetch(url))          # one fetch per distinct receipt URL
```

This is the C2 live check and is in scope by contract. Observations, not a routed defect: `read()`
has no size cap (a large or hostile body is read into memory before `extract`); `urllib` follows
redirects, so the host actually contacted need not be the receipt's host (the URL-set test at
`:134` validates the *declared* string only); `check_live` maps every exception to `unreachable`, so
a failure degrades rather than crashes (good). Cheap hardening: `resp.read(MAX_BYTES)` and a
redirect handler that rejects a non-`https` scheme or a host outside the receipt's host.

**Network audit result outside this path: none.** `grep -nE 'urllib|requests\.|socket\.|curl |wget '`
over `calibration/measure.py`, `control/run-controls.py`, `control/c2-controls.py`,
`deciding-run.sh`, `no-harm.sh` → no matches; the 19 tools the 22 statements invoke → no network
calls (their `https://` hits are fixture registry text, e.g. `tools/staged-id-guard.py:275-284`);
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (the census both counters run) has no
`curl`/`wget`/`git fetch`/`remote`; every `git` call in the three files is a local-path operation
(`clone --shared`, `show`, `cat-file`, `rev-parse`). The C1 `calibration` axis statement runs
`.ufo/evidence/round-45/freshness/measure.py --lane --rev` **without** `--live`, so its network
mode is not on this path.

## F7 — the deciding C1 run does write `/tmp`, through its statements (info, decisive)

The counter's own code is `/tmp`-clean (P4), but 7 of the 22 statements execute tools that hardcode
`/tmp` and therefore ignore the profile `TMPDIR` that `profile_env` (`:288-302`) carefully sets:

| statement | tool:line | literal |
|---|---|---|
| mutation sweep runner | `tools/mutate-and-run.sh:1477` (+ `:482`, `:1360` auto roots) | `mktemp -d /tmp/tameshi-r4-2-selftest.XXXXXX` |
| repeated pristine-control gate | `tools/repeat-control.py:597` | `mkdtemp(..., dir="/tmp")` |
| six-leg content-disposition probe | `tools/pin-disposition.py:706` | `mkdtemp(..., dir="/tmp")` |
| effective expectation reconciliation | `tools/evidence-disposition.py:2351` | `mkdtemp(..., dir="/tmp")` |
| hermetic env-differential probe | `tools/env-diff.py:61` (and `--tmpfs /tmp` at `:69`) | `TemporaryDirectory(..., dir="/tmp")` |
| tally-audit-v3 runner audit | `tools/tally-audit-v3.py:422` | creates `/tmp/tameshi-r4-2-regression.<6>` |
| bounded ANSI-C code_view | same tool, same site | same |

7 statements × 6 profiles × 3 rounds = **126 invocations** of a `/tmp`-writing tool per deciding
C1 run, none of which the counter can redirect, and none of which can ever exhibit a `TMPDIR`
dependence — so for those statements P0 vs P1–P5 is structurally blind to the `env` axis (w1 §6).
This is live, not theoretical: 12 `/tmp/tameshi-r14-evidence-disposition-selftest.*` dirs
(**80 MB**, timestamps 09:41–10:32 today) plus 3 zero-byte `/tmp/tameshi-r4-2-regression.*`; the
writer is `evidence-disposition.py:2351`, and the prefix is produced by no other file in the lane.

*Impact.* The deciding run's own receipt cannot claim a `/tmp`-free C1, the `env` dependence of
those seven statements is unmeasured, and the leaks (80 MB now) are unattributable to a seat.
Not fixable inside the frozen counters without touching `tools/` (outside this seat's bounds and
inside the round's frozen pathspec) — it belongs to the round that re-freezes `tools/`.

## Scratch hygiene — `/fast/scratch/hyaku/tameshi-r48/` inventory

At 10:41, du of the whole tree = 8.1 G of `/fast/scratch/hyaku` (26% of `/fast`, 602 G free;
`disk-guard.sh status` run before the heavy pass: `/tmp` 3% / 125 G free).

* **No wave-1 seat directory remains.** Wave-1 report/seat names (`T48ConnCorpus`,
  `T48CritC1Design`, `T48ExecC1Counter`, `T48SentinelTmp`, …) have no directory under
  `tameshi-r48/`; everything present is a live a2w1/orchestrator seat.
* Live trees, name + size + mtime: `L1` 3.0 G (ctl 2.7 G, c2ctl 153 M, emit 109 M, out 260 K),
  `T48W2CritC1Controls` 4.8 G, `T48W2RevSelftestReceipts` 4.3 G, `T48W2ExecC1ProbeB` 2.4 G,
  `T48A2ExecC1SerialA/B/D` 2.4 G each, `T48W2RevC1Separability` 2.0 G, `T48W2ExecC1ProbeD` 201 M,
  `T48W2ExecNoHarm` 155 M, `T48A2CritC1Emit` 308 M, `T48W2SentinelScratch` 58 M (mine, removed at
  the end), remaining seats < 20 M. None of these is mine to delete.
* Orphans at the shared root (F2): `/fast/scratch/c1-r48-xkbewgrm` 1.7 M (not mine; left in
  place).
* Ambient `/tmp` (other seats' tools, not these three files; left untouched): 292 entries, 499 MB
  total — 12 × 6.7 MB `tameshi-r14-evidence-disposition-selftest.*` (F7), 3 zero-byte
  `tameshi-r4-2-regression.*`, 7 `tsukuroi-r3-2-selftest.*`, plus six
  `context-capture-selftest-*` that appeared inside a 5 s window while this seat probed.

## Not established

* Whether a *completed* C1 `--selftest` with `TMPDIR` unset leaves the empty `c1-r48-<rand>`
  directory: statically no `rmtree` targets it (`:842` creates it, only `:847` removes the per-case
  child), and the interrupted probe left 3.0 MB (P6); my completed run (P5) used a `TMPDIR`, where
  `root` is `TMPDIR` itself, so it left nothing to observe.
* `run-controls.py --work /tmp/...` was not executed (F4) — the probe would itself create the
  `/tmp` tree the finding describes.
* Attribution of `/tmp/tameshi-r14-*` to the C1 counter run rather than a seat invoking the tool
  directly rests on (i) the tool being the only producer of that prefix in the lane and (ii) the
  timestamps coinciding with wave-2 C1 probes; the invocation itself was not traced.
* Peak RSS of a 12-clone round was not measured (disk only).

## Tooling / scratch record

* No tool installed or upgraded (nothing needed; `strace` and `du` present).
* Scratch `$S=/fast/scratch/hyaku/tameshi-r48/T48W2SentinelScratch` (58 M: four strace logs, probe
  outputs) is deleted at the end of this seat; `TMPDIR` pointed inside `$S` for every probe except
  P1/P3/P4, which deliberately unset or invalidated it to reproduce F1/F2 — the resulting `/tmp`
  and `/fast/scratch` trees from those probes are reported above (P6), not hidden.
