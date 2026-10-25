seat: ExecStmt03
item: C1 statement re-observation — repeated pristine-control gate, six-leg content-disposition probe, exposed witness provenance correction (twice each in a freeze clone, standing-row claim re-parsed with the counter's own helpers)

# ExecStmt03 — C1 re-observation of three frozen statements (round 46, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`
(base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`). Read-only: no lane file was written except this report;
all scratch under `/tmp/tameshi-r46-ExecStmt03/`.

## Result in one line

All three statements **UNPARSED** at the freeze: their last standing `SCORECARD.md` rows (lines 1517–1519) do
not carry the counter's claim grammar (`CMD` → `` `PRINTED LINE` ``, exit N[, tool sha256 `12hex`]), while both
runs of each frozen command are byte-identical, exit 0, well inside `timeout`, and agree with
`before/c1-at-freeze.stdout` line for line. 0 mismatches, 0 unobservables, 3 unparsed from this seat.

## Setup (exact command)

```
W=/tmp/tameshi-r46-ExecStmt03; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

Output:
```
clone_head=745a583181648cfc7f9c1b476cd1be7dc68f7433
mirror_head=745a583181648cfc7f9c1b476cd1be7dc68f7433
a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/statements.json
```
The `statements.json` sha256 equals the pinned `a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9`
in `measure.py:STATEMENTS_SHA256` and in the contract (`stmts_pin` would be 1). All three statements have
`"cwd": "clone"`, so every run used `cwd=/tmp/tameshi-r46-ExecStmt03/clone` with `REV` in the env and the
counter's own `env()` (all `GIT_*` dropped, `PYTHONDONTWRITEBYTECODE=1`).

## Exact commands run

Runner (imports the counter module by path, so `pick_line`, `env`, `last_rows`, `claim_of` are the counter's own
code, not a re-implementation): `cd /tmp/tameshi-r46-ExecStmt03 && python3 run.py`. It executed each argv from
`statements.json` twice, sequentially, exactly as `observe()` would:

```
cd /tmp/tameshi-r46-ExecStmt03/clone && REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/repeat-control.py --selftest
cd /tmp/tameshi-r46-ExecStmt03/clone && REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/pin-disposition.py --selftest
cd /tmp/tameshi-r46-ExecStmt03/clone && REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/witness-metadata.py --selftest
```

Literal shell replay with the bash `time` keyword (third invocation, confirmation only, not the tally):

```
cd /tmp/tameshi-r46-ExecStmt03/clone && export REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 PYTHONDONTWRITEBYTECODE=1 TIMEFORMAT='wall=%3R'; for t in "python3 tools/repeat-control.py --selftest" "python3 tools/pin-disposition.py --selftest" "python3 tools/witness-metadata.py --selftest"; do echo "== literal: $t"; time $t > /tmp/tameshi-r46-ExecStmt03/lit.out 2>/tmp/tameshi-r46-ExecStmt03/lit.err; echo "exit=$?"; grep -nE "^(SELFTEST: PASS \(([0-9]+) cases\)|SELFTEST: PASS \([0-9]+/[0-9]+\)|SELFTEST: PASS [0-9]+/[0-9]+)$" /tmp/tameshi-r46-ExecStmt03/lit.out; echo "stderr_bytes=$(wc -c < /tmp/tameshi-r46-ExecStmt03/lit.err)"; done
```

Claim read (counter helpers on the lane's `SCORECARD.md`; also re-read from the REV blob):

```
python3 - <<E
import importlib.util, json, subprocess, sys
sys.dont_write_bytecode=True
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec=importlib.util.spec_from_file_location('c1m',L+'/.ufo/evidence/round-46/calibration/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sc=subprocess.run(['git','-C',L,'show','745a583181648cfc7f9c1b476cd1be7dc68f7433:SCORECARD.md'],capture_output=True,text=True).stdout
rows=m.last_rows(sc); print(rows[('cap','repeated pristine-control gate')]); ...
E
```

## Per-statement table

| id | claimed | observed run 1 | observed run 2 | same? | exit | seconds | verdict |
|---|---|---|---|---|---|---|---|
| repeated pristine-control gate | `-` (claim_of → None) | `SELFTEST: PASS (29 cases)` \| 0 \| `296fe566dc59` | `SELFTEST: PASS (29 cases)` \| 0 \| `296fe566dc59` | yes (byte-identical stdout) | 0 / 0 | 0.708 / 0.717 | **UNPARSED** |
| six-leg content-disposition probe | `-` (claim_of → None) | `SELFTEST: PASS (19/19)` \| 0 \| `331529eadafe` | `SELFTEST: PASS (19/19)` \| 0 \| `331529eadafe` | yes (byte-identical stdout) | 0 / 0 | 0.930 / 0.931 | **UNPARSED** |
| exposed witness provenance correction | `-` (claim_of → None) | `SELFTEST: PASS 39/39` \| 0 \| `df3390682a04` | `SELFTEST: PASS 39/39` \| 0 \| `df3390682a04` | yes (byte-identical stdout) | 0 / 0 | 1.362 / 1.399 | **UNPARSED** |

`sha_file` prefixes at the freeze (item step 2), counter form vs filesystem form, all equal:

```
git -C clone show HEAD:tools/repeat-control.py        | sha256 → 296fe566dc59   (sha256sum tools/repeat-control.py | cut -c1-12 → 296fe566dc59)
git -C clone show HEAD:tools/pin-disposition.py       | sha256 → 331529eadafe   (sha256sum tools/pin-disposition.py | cut -c1-12 → 331529eadafe)
git -C clone show HEAD:tools/witness-metadata.py      | sha256 → df3390682a04   (sha256sum tools/witness-metadata.py | cut -c1-12 → df3390682a04)
```

Observed stdout/stderr sizes per run: 2936/2936, 1409/1409, 6002/6002 bytes stdout, 0 bytes stderr for all three
statements; run1 vs run2 stdout sha256 `09f432706cf0`, `1f39911c34eb`, `c4f371609f34` (`cmp -s` → identical).
The `clone` worktree stayed clean (`git status --porcelain` → 0 lines) and `HEAD` stayed at the freeze after all runs.

## Why UNPARSED — the standing rows, verbatim

Deciding (last, file order) rows of the `| Capability | What it can now do | Evidence pointer | First-working round |` table:

- line 1517 `repeated pristine-control gate`, evidence cell:
  `` `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 ``
  → printed line not backticked, no `, tool sha256 \`…\``; `CLAIM_SHA` cannot match → `claim_of` None.
- line 1518 `six-leg content-disposition probe`, evidence cell:
  `` `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 ``
  → no backticked printed line, no `, exit N`, no tool sha256 → None.
- line 1519 `exposed witness provenance correction`, evidence cell:
  `` `python3 tools/witness-metadata.py --selftest`: metadata selftest39/39 PASS0 ``
  → colon form, no `→`, no `exit N`, no tool sha256 → None.

Each id has exactly 2 data rows in recognised tables (lines 243–245 and 1517–1519); last-row-wins selects
1517–1519, and the earlier rows (243: `→ PASS (29 cases), exit 0; …`; 244: `→ 18/18 PASS0; …`;
245: `metadata selftest39/39 PASS0; …`) do not parse either.

## Flags the item asked for

- Two runs differ: **none** (all three byte-identical, same exit).
- `obs` regex matches >1 line: **none** (exactly 1 match each: `obs_regex_matches=1`).
- `obs` regex matches none: **none** (picked line non-empty each run).
- Command slower than `timeout` (900 s each): **none** (max 1.399 s; no `timeout` outcome, no `UNOBSERVABLE`).

## Calibration findings the L1 needs before appending rows

1. **The exact emit form works.** Feeding the observed tuples through the counter's own `emit_row`, then
   re-parsing the emitted evidence cell with `claim_of`, reproduces the observed tuple exactly for all three:
   ```
   EMIT_CAP | repeated pristine-control gate | … | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0, tool sha256 `296fe566dc59` | round 12 |
   EMIT_CAP | six-leg content-disposition probe | … | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, tool sha256 `331529eadafe` | round 13 |
   EMIT_CAP | exposed witness provenance correction | … | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0, tool sha256 `df3390682a04` | round 13 |
   ```
   `claim_of(emitted) == observed` → True for all three.
2. **Shortening the printed line is a silent MISMATCH, not an error.** Dropping the `SELFTEST: ` prefix (the
   shape the current rows use) still parses: `claim_of` returns `('PASS (29 cases)','0','296fe566dc59')`
   (and `('PASS (19/19)',…)`, `('PASS 39/39',…)`) which is **not** the observed tuple → MISMATCH. The row must
   quote the picked line whole, `SELFTEST: ` included.
3. **Omitting the tool sha256 for these `sha_file` statements is UNPARSED.** Verified: the same evidence cell
   without `, tool sha256 \`…\`` gives `claim_of` → None (the counter switches to `CLAIM_SHA` whenever
   `sha_file` is set).
4. **Stale-value drift is present in the older rows**: line 244 states `18/18`, the tool now prints `19/19`
   (line 1518 already says 19/19). Copying the round-13 text instead of the observed line would mismatch.
5. **The tallies are load- and environment-stable**, so they can be standing values: 4 concurrent instances of
   each selftest (12 processes, matching the counter's 22-worker concurrency) all printed the same line with
   exit 0, and each selftest also passed under `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 HOME=<empty>`
   with no ambient git identity (`SELFTEST: PASS (29 cases)` / `(19/19)` / `39/39`, rc=0) — they supply their
   own fixture identity. Clone stayed clean afterwards.
6. **`append_only` context**: `SCORECARD.md` working tree, `745a…:SCORECARD.md` and `683ee…:SCORECARD.md` all
   hash to `4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1` (no sibling has touched it yet),
   so the base is still a byte prefix at the freeze.

## Cross-check against the frozen before-receipt

`.ufo/evidence/round-46/before/c1-at-freeze.stdout` lines for these three are identical to mine, value for value:
```
STATEMENT cap/repeated pristine-control gate: claimed=- observed=SELFTEST: PASS (29 cases)|0|296fe566dc59 (exit=0) UNPARSED
STATEMENT cap/six-leg content-disposition probe: claimed=- observed=SELFTEST: PASS (19/19)|0|331529eadafe (exit=0) UNPARSED
STATEMENT cap/exposed witness provenance correction: claimed=- observed=SELFTEST: PASS 39/39|0|df3390682a04 (exit=0) UNPARSED
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C1_R46_PASS=false
```
These three are 3 of the 19 `unparsed`; neither `mismatches=2` (`six-leg regression ledger`, `calibration`) nor
the rest is this seat's item.

## Retained evidence

`/tmp/tameshi-r46-ExecStmt03/`: `run.py` (runner), `obs-repeated-pristine-control-gate-run{1,2}.stdout`,
`obs-six-leg-content-disposition-probe-run{1,2}.stdout`,
`obs-exposed-witness-provenance-correction-run{1,2}.stdout`, `lit.out`/`lit.err`, `nohome/`, `clone/` (detached
at the freeze, clean), `fleet/` (sibling-lane symlinks + lane mirror, unused by these three statements).

## Risks / blockers

- None blocking. The three statements cannot match at the freeze without appended rows (that is the intended
  before state, `total=21`); the exact strings to append are in finding 1, and finding 2 is the trap that turns a
  reformat into a MISMATCH rather than an error.
- Unrun by me, by design: the full 22-statement counter (L1's deciding run), the counter `--selftest`, the other
  19 statements, `no-harm.sh`.
- No tool installed or upgraded; no pacman transaction attempted.
