seat: ExecStmt07
item: C1 re-observation of four frozen statements (write-path-census-v2, write-path census destination resolution, staged-id adoption guard, freshness) at freeze `745a5831` — both runs stable and content-agreeing, but all four standing claims are UNPARSABLE by the frozen counter (three cap rows carry no `→ value, exit N` triple; freshness has no `Axis | Score (0–10)` row at all).

Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin (read-only; nothing written except this report).
Freeze under test: `745a583181648cfc7f9c1b476cd1be7dc68f7433`. Base: `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`.
Contract read first: `.ufo/evidence/round-46/contract.json` (never edited). Counter, statements list and SCORECARD were not edited.
Scratch: `/tmp/tameshi-r46-ExecStmt07/` only.

## 1. Setup (exact commands)

```bash
W=/tmp/tameshi-r46-ExecStmt07; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```
Output: `git -C $W/clone rev-parse HEAD` → `745a583181648cfc7f9c1b476cd1be7dc68f7433`; `git -C $W/fleet/tameshi-shokunin rev-parse HEAD` → `745a583181648cfc7f9c1b476cd1be7dc68f7433`. `$W/fleet` holds 21 sibling symlinks + the lane clone (22 entries).

SCORECARD identity (so "current SCORECARD" == "base text at the freeze" is verified, not assumed):

```bash
for r in 683eedde… 745a5831…; do printf '%s ' $r; git show $r:SCORECARD.md | sha256sum; done; printf 'worktree '; sha256sum SCORECARD.md
```
Output: all three `4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1`. (The first `git rev-parse --verify A B` in my probe errored `fatal: Needed a single revision` — rev-parse takes one rev; I re-ran per-rev via `git show`, which is what produced the hashes above.)

## 2. Runs (twice each, sequential), cwd = `$W/clone`

```bash
export REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 PYTHONDONTWRITEBYTECODE=1
python3 tools/write-path-census-v2.py --selftest
python3 tools/write-path-census-v3.py --selftest
python3 tools/staged-id-guard.py --selftest
python3 .ufo/evidence/round-45/freshness/measure.py --lane /tmp/tameshi-r46-ExecStmt07/clone --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433
```
Each was run twice in a `date +%s.%N`-timed loop capturing stdout+stderr and `$?`; the freshness output of both runs is retained at `/tmp/tameshi-r46-ExecStmt07/fresh-{1,2}.out`.

`sha_file` digests at the freeze (`sha256sum <file> | cut -c1-12` in the checkout, and the counter's own method `git show HEAD:<file> | sha256sum | cut -c1-12`; both agree):

| tool | sha256 prefix (12) |
|---|---|
| `tools/write-path-census-v2.py` | `402285329588` |
| `tools/write-path-census-v3.py` | `095924a7a165` |
| `tools/staged-id-guard.py` | `03a796c5726c` |

## 3. Standing claims, read with the counter's own parser

```bash
python3 - <<'E'
import importlib.util, json
spec = importlib.util.spec_from_file_location('c1m','.ufo/evidence/round-46/calibration/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = m.last_rows(open('SCORECARD.md').read())
stmts = json.load(open('.ufo/evidence/round-46/calibration/statements.json'))['statements']
… m.claim_of(s, rows.get((s['kind'], s['id']))) …
E
```
Output: `claim_of` → `None` for all four; `last_rows` has 21 keys (22 statements), and `('axis','freshness')` is not among them. `depth` → `('9',)`, `calibration` → `('8',)` (parser works; freshness is the axis-level absence).

Counter parser sanity, run in the freeze checkout: `python3 .ufo/evidence/round-46/calibration/measure.py --selftest` → `C1_R46_SELFTEST: cases=18 failed=0`, `VERDICT: PASS` (so `claim_of`=None ⇒ `unparsed` per its own T6/T7 cases). Counter sha256 `ad5f85df21b1` both in the worktree and at the freeze; `statements.json` sha256 `a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9` (matches the contract pin).

## 4. Per-statement result

| id | kind | claimed | observed run 1 | observed run 2 | same? | exit | seconds (r1/r2) | verdict |
|---|---|---|---|---|---|---|---|---|
| `write-path-census-v2` | cap | **None** (row states tool `4022853295882c5a…78b` only — no printed value, no exit) | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` + sha `402285329588` | identical | yes | 0 / 0 | 0.04 / 0.03 | **UNPARSED** |
| `write-path census destination resolution` | cap | **None** (row states tool `095924a7…0279` only — no printed value, no exit) | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` + sha `095924a7a165` | identical | yes | 0 / 0 | 0.03 / 0.03 | **UNPARSED** |
| `staged-id adoption guard` | cap | **None** (row states tool `03a796c5…dca8` only — no printed value, no exit) | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` + sha `03a796c5726c` | identical | yes | 0 / 0 | 0.04 / 0.03 | **UNPARSED** |
| `freshness` | axis | **None** (no `Axis \| Score (0–10)` row exists for the axis) | `9` (from `C1_R45: self_pin=1 … fresh=71 score=9 target=50 rev=745a5831… C1_R45_PASS=true`) | `9`, byte-identical stream | yes | 0 / 0 | 0.71 / 0.69 | **UNPARSED** |

Why "UNPARSED" and not "MISMATCH": the frozen counter compares `claim_of(...)` against `(obs, exit[, sha12])`; `CLAIM_SHA = '→ `([^`]+)`, exit (\d+), tool sha256 `([0-9a-f]{12})`'`. Reproduced per row:

| id | `CLAIM_BASE` match | `CLAIM_SHA` match |
|---|---|---|
| write-path-census-v2 | False | False |
| write-path census destination resolution | False | False |
| staged-id adoption guard | False | False |
| freshness | (no row) | (no row) |

So these four alone contribute `unparsed=4` to the counter's `total` at the freeze. Content-wise nothing observed contradicts the SCORECARD: all three stated tool digests equal the observed 12-hex prefixes, every command exits 0, and freshness's stated `score=9` (round-45 claim table, SCORECARD.md:2154: `` `verified=73 disputed=2 fresh=71 score=9 C1_R45_PASS=true` ``) equals the observed `score=9`. The defect is form/placement, not arithmetic.

The standing rows (verbatim evidence cells, SCORECARD.md lines 1889 / 1920 / 2074):

- `write-path-census-v2`: "deciding receipt `C1_R40: ... C1_R40_PASS=true` at `5641ed84`, counter `.ufo/evidence/round-40/census/measure.py`, tool `tools/write-path-census-v2.py` @ `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b`"
- `write-path census destination resolution`: "deciding receipt `C2_R41: … C2_R41_PASS=true` at the round-41 measured commit, counter `.ufo/evidence/round-41/census/measure.py`, tool `tools/write-path-census-v3.py` @ `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279`"
- `staged-id adoption guard`: "deciding receipt `C3_R43: … C3_R43_PASS=true` at the round-43 measured commit, counter `.ufo/evidence/round-43/guard/measure.py`, tool `tools/staged-id-guard.py` @ `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`"
- `freshness`: no row. `grep -cE '^\| *freshness *\| *[0-9]+' SCORECARD.md` → `0`; every `| freshness …` line (111, 187, 325, 388, 445, 540, 591, 629, 680) is an "unchanged" verdict in a `Axis | … verdict | Bound` table, which `last_rows` ignores (it accepts only header[0]=='Capability' or header[1].startswith('Score')).

## 5. Flags requested by the item

- Two runs differ: **none**. All four produced byte-identical streams across both runs; `fresh-1.out == fresh-2.out` → `True`.
- `obs` regex matches more than one line: **none**. Match counts (python `re.M` over the full stdout+stderr stream): v2 = 1, v3 = 1, guard = 1, freshness = 1. Note `staged-id-guard` prints a second line `VERDICT: PASS`, which the `^(STAGED_ID_GUARD_SELFTEST: …)` regex correctly does not match; `freshness`'s `\bscore=(\d+)\b` matches only the `C1_R45:` summary line (no `…_score=` token can match because `_` is a word character).
- `obs` regex matches nothing: **none**.
- Slower than `timeout`: **none**. Max observed 0.71 s against declared timeouts of 900/900/900/300 s.

## 6. Appendable rows the counter itself emits for these observations

Generated read-only by calling `emit_row(stmt, observed, rows.get(...))` from the frozen counter (not written to SCORECARD.md):

```
EMIT_CAP | write-path-census-v2 | … | `python3 tools/write-path-census-v2.py --selftest` → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`, exit 0, tool sha256 `402285329588` | round 40 |
EMIT_CAP | write-path census destination resolution | … | `python3 tools/write-path-census-v3.py --selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`, exit 0, tool sha256 `095924a7a165` | round 41 |
EMIT_CAP | staged-id adoption guard | … | `python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`, exit 0, tool sha256 `03a796c5726c` | round 43 |
EMIT_AXIS | freshness | 9 | see the evidence pointer in the round-46 SCORECARD block |
```
Each of these parses under `claim_of` (the cap form is exactly `CLAIM_SHA`; the axis form is a bare integer in column 2). `EMIT_AXIS` inherits its evidence column from the last `('axis','freshness')` row — which does not exist, so the freshness append must also carry a real evidence/rule cell (the counter only needs column 2 to parse).

## 7. Adjacent observation (outside this seat's four statements, flagged not owned)

`claim_of` for the other two axis rows: `depth` → `('9',)`, `calibration` → `('8',)`. The contract's `axes.scores_at_base` records calibration 6 ("lowest non-retired axis"), and SCORECARD.md:2008/2063 say "Numeric axes at the base: depth 9 …, calibration 6", while the last `Axis | Score (0–10)` row (SCORECARD.md:1536 block, second score table) states calibration 8. Whoever owns the `calibration` statement should confirm which value the coldread monitor prints at REV; I did not run it (not my statement).

## 8. Bounds honoured

- No writes to the lane except this file; no writes to `/home/vgpnk/Projects/shokunin` (fleet), no sibling lane, no jj/Git mutation anywhere (all lane git calls were `show`/`rev-parse`).
- No counter run as a verdict; the only counter invocation was `--selftest` (in the scratch clone) plus module-level `last_rows`/`claim_of`/`emit_row` calls on the read-only SCORECARD.
- No subagent dispatch, no background jobs, no commits, no network fetch (the round-45 freshness counter reads its committed ledger, ran in 0.7 s).
- Tooling: nothing installed or upgraded; no pacman (guard respected).

## 9. Residual risk

- `freshness`'s observed `score=9` depends on the round-45 counter's own committed ledger and its 73 held rows; it re-derives from committed bytes here, not from live fetches, so a REV that changes the ledger changes the value. Two runs agree at this freeze only.
- The three cap `--selftest` commands are pure local and deterministic in the observed window; both runs exit 0 in <0.05 s, so an unstable tally is unlikely but is only evidenced for these two runs.
