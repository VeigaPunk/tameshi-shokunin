# T47HardFreshLiveA — C2 selftest addition for `live()` (group `freshness`)

Seat: `T47HardFreshLiveA` (leaf). Group: `freshness`. Counter hardened: `.ufo/evidence/round-46/hardening/freshness-counter.py`.
Deliverable: `.ufo/waves/round-47/w1/T47HardFreshLiveA.addition.py` — one top-level `extra_T47HardFreshLiveA()`, helpers prefixed `_xT47HardFreshLiveA_`.
Scratch: `/tmp/tameshi-r47-T47HardFreshLiveA/`. No tool installed or upgraded.

## Result

All **7 assigned mutants killed**, plus **5 further `live()` mutants** killed by the same cases (recorded below, not claimed as my item).
Group sweep after assembly: **PRISTINE pass, 70 killed / 27 survived / 4 crashed of 101 real mutants, all 10 NEUTRAL `survived`, no regression** (baseline was 58/39/4 of the same 101; gained 12, lost 0). The sweep was re-run against the delivered addition bytes (assembled working copy `/tmp/tameshi-r47-T47HardFreshLiveA/h.py`, sha256 `0493bf9ff177c07978386103e778c228b0a34ba11470a773956f61492abf25fe`) and gave the same counts.

## Method (no network)

`live()` is the `--live` re-fetch mode and no case in the round-46 selftest reached it. Each case here:

1. builds a fixture git lane with `tempfile.mkdtemp()`: `corpus/SOURCES.md` (one `mined` row per ledger entry, the 13-cell pipe form `parse_rows()` requires) and the round-45 ledger at `LEDGER` (`.ufo/evidence/round-45/freshness/ledger.json`, shape `{"entries": [...]}`); `git init` runs first, `git -C <d> rev-parse --show-toplevel` is asserted to equal `os.path.realpath(d)` before the first commit, and the commit identity is passed only as `-c user.name=t -c user.email=t@t` on that fixture;
2. writes a stub `curl` into a second `TemporaryDirectory` and prepends it to `PATH` for the duration of the call (saved/restored `os.environ` in a `finally`), so `subprocess.run(['curl', ...])` inside `live()` resolves to the stub — **the network is never touched**. The stub parses the `-o` argument, copies `$X47LIVE_BODY` there when it is set, and exits `$X47LIVE_RC`;
3. calls `live(lane, 'HEAD')` under `contextlib.redirect_stdout(io.StringIO())` and asserts on the rule's observable output only: the `LIVE <id> present|absent` lines, the `C1_R45_LIVE: present=N absent=M` summary and the return code. No case reads the counter's source, pins a hash/length, or restates a mutated line.

So the separating inputs are: **the stub's exit code**, **whether the stub writes the target**, **whether the fetched bytes contain the quote**, and **the ledger's verdict for an id that is in the population**.

| case | ledger | stub |
|---|---|---|
| `L01_live_fetch_present` | one `holds` entry S001 (in population), quote `Flaky failure reports are retained only when the rerun reproduces them` | exits 0, body contains the quote |
| `L02_live_fetch_error_absent` | one `holds` entry S001 | exits 22, writes nothing |
| `L03_live_non_holds_skipped` | one `drifted` entry S001 (in population) | exits 0, body contains the quote |
| `L04_live_unreadable_target_absent` | one `holds` entry S001 | exits 0, writes no target |

Pristine expectations (all asserted, all pass): L01 `(1,0) rc=0 ['LIVE S001 present']`, L02 `(0,1) rc=0 ['LIVE S001 absent']`, L03 `(0,0) rc=0 []`, L04 `(0,1) rc=0 ['LIVE S001 absent']`.

## Assigned mutants

| pool id | mutant | case | separating input — original vs mutant | observed FAIL line |
|---|---|---|---|---|
| `live:int:0` | line 304 `ok = bad = 0` → `1` | L01 | one present fetch: original counts `present=1 absent=0`; mutant starts both counters at 1 → `2/1` | `FAIL L01_live_fetch_present summary=(2, 1) rc=0 live=['LIVE S001 present']` |
| `live:int:1` | line 322 `return 0` → `1` | L01 | original returns 0 after a complete run; mutant returns 1 | `FAIL L01_live_fetch_present summary=(1, 0) rc=1 ...` |
| `live:bool:0` | line 301 `(git(...) or '')` → `and` | L01 | registry text is non-empty, so `text or ''` = text (population non-empty, entry fetched, `1/0`); `text and ''` = `''` → empty population → the `id not in pop` gate skips the entry → `0/0`, no LIVE line | `FAIL L01_live_fetch_present summary=(0, 0) rc=0 live=[]` |
| `live:bool:1` | line 307 `verdict != 'holds' or id not in pop` → `and` | L03 | `drifted` entry whose id IS in the population: original `True or False` → skip (`0/0`, no LIVE line); mutant `True and False` → fetch → `1/0`, `LIVE S001 present` | `FAIL L03_live_non_holds_skipped summary=(1, 0) rc=0 live=['LIVE S001 present']` |
| `live:const:0` | line 312 `present = False` → `True` | L02 | curl exits 22, so the body branch is skipped and the initial value is reported: original `absent` (`0/1`); mutant `present` (`1/0`) | `FAIL L02_live_fetch_error_absent summary=(1, 0) rc=0 live=['LIVE S001 present']` |
| `live:cmp:0` | line 313 `res.returncode == 0` → `!= 0` | L01 | exit 0 + quote in body: original enters the body check → `present` (`1/0`); mutant `0 != 0` is False → check skipped → `absent` (`0/1`) | `FAIL L01_live_fetch_present summary=(0, 1) rc=0 live=['LIVE S001 absent']` |
| `live:not:0` | line 320 `bad += not present` → `bad += present` | L01 | one present fetch: original adds 0 to `bad` (`1/0`); mutant adds 1 (`1/1`) | `FAIL L01_live_fetch_present summary=(1, 1) rc=0 live=['LIVE S001 present']` |

## Additional `live()` kills from the same cases (not my item, reported for the ledger)

`live:cmp:1` and `live:cmp:2` (line 307, L01: a `holds` entry in the population makes the mutated gate `==`/`in` true, so the entry is skipped → `0/0`) — `FAIL L01_live_fetch_present summary=(0, 0) rc=0 live=[]`.
`live:int:2` (line 313 `== 0` → `== 1`, L01, `(0,1)`) and `live:cmp:3` (line 315 `in` → `not in`, L01, `(0,1)`) — both `FAIL L01_live_fetch_present summary=(0, 1) ...`.
`live:const:2` (line 317 `present = False` inside the `except` arm → `True`): L04 makes the target unreadable while curl exits 0, so the `except` arm runs — original `absent` (`0/1`), mutant `present` (`1/0`) — `FAIL L04_live_unreadable_target_absent summary=(1, 0) rc=0 live=['LIVE S001 present']`.

## Remaining `live()` survivor, with the argument (not fakeable)

`live:const:1` (line 311 `capture_output=True` → `False`) still survives the sweep. `capture_output` only controls whether the child's fds are piped; `live()` reads `res.returncode` and nothing else from `res`, so **no input gives the original and the mutated rule different values** — the mutant is value-equivalent for this rule. The only observable is the child's output leaking to fd 1, which is a harness-level side effect, not a rule value; asserting on it would not be "an input on which the rule returns a different value". Not mine by item either; reported so the sweep result is not silently left undiscussed. Full-sweep evidence: `NEUTRAL ... survived` for all 10 commute mutants and `MUT live:const:1 survived` in the run below.

## Commands (exit codes)

1. `python3 .ufo/evidence/round-47/hardening/assemble.py --group freshness --add /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-47/w1/T47HardFreshLiveA.addition.py --out /tmp/tameshi-r47-T47HardFreshLiveA/h.py` → **0** (`wrote ... (1 additions)`); my cases print `L01..L04` PASS and the assembled pristine run ends `C1_R45_SELFTEST: cases=38 failed=0` / `VERDICT: PASS`.
2. `python3 /tmp/tameshi-r47-T47HardFreshLiveA/h.py --selftest` (from the scratch dir) → **0**, `VERDICT: PASS`.
3. `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshLiveA/h.py --group freshness --ids live:int:0,live:int:1,live:bool:0,live:bool:1,live:const:0,live:cmp:0,live:not:0` → **0**; `PRISTINE pass` and all seven lines `MUT live:*:N killed`.
4. `python3 .ufo/evidence/round-47/hardening/pool.py --try /tmp/tameshi-r47-T47HardFreshLiveA/h.py --group freshness` (whole group, no `--ids`) → **0**; `PRISTINE pass`; 70 `MUT ... killed`, 27 `survived`, 4 `crashed`, 10/10 `NEUTRAL ... survived`. The 4 `crashed` are exactly the baseline's (`parse_rows:int:1`, `parse_rows:int:8`, `review_sets:bool:1`, `review_sets:not:2`) and unchanged by my file.
5. Read-only comparison of `/tmp/tameshi-r47-T47HardFreshLiveA/full-final.txt` with `.ufo/evidence/round-47/before/base-freshness.txt`: 111 ids on both sides, regressions `[]`, neutral killed `[]`, gained 12 (`live:int:0`, `live:int:1`, `live:int:2`, `live:bool:0`, `live:bool:1`, `live:cmp:0`, `live:cmp:1`, `live:cmp:2`, `live:cmp:3`, `live:const:0`, `live:const:2`, `live:not:0`).

All runs used absolute paths; nothing was written in the lane except this report and the addition file; no git/jj mutation, no lane commit, no campaign tool in `/home/vgpnk/Projects/shokuknow`.

## Risks

- The cases depend on `git` and `/bin/sh` being present in the selftest environment (both are; the round-46 `extra_HardMeasure` cases already build fixture git repos).
- `os.environ` is mutated in-process for the stub and restored in a `finally`; a hard kill inside `live()` would leak the modified environment only within that already-failing run.
- The stub `curl` is prepended to `PATH` only inside `_xT47HardFreshLiveA_run`; if a future case runs concurrently in threads it would race, but the counter's selftest is single-threaded.
