seat: ExecStmt06
item: C1 statement re-observation — ran the frozen argv of `tally-audit-v2 runner audit`, `tally-audit-v3 runner audit` and `bounded ANSI-C code_view` twice each at the freeze rev and compared against their standing SCORECARD rows

Round 46, wave 1, C1 calibration seat. Read-only on the lane; all scratch under `/tmp/tameshi-r46-ExecStmt06/`. No lane file, no `SCORECARD.md`, no `statements.json` and no counter was edited. No tool installed or upgraded.

## Setup (exact commands)

```
W=/tmp/tameshi-r46-ExecStmt06; rm -rf $W; mkdir -p $W/fleet; for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

Verification:

```
git -C $W/clone rev-parse HEAD                   -> 745a583181648cfc7f9c1b476cd1be7dc68f7433
git -C $W/fleet/tameshi-shokunin rev-parse HEAD  -> 745a583181648cfc7f9c1b476cd1be7dc68f7433
ls $W/fleet | wc -l                              -> 21   (20 sibling-lane symlinks + the tameshi mirror)
sha256sum $W/clone/.ufo/evidence/round-46/calibration/statements.json
  -> a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9   (== contract statements_sha256 / stmts_pin)
sha256sum $W/clone/.ufo/evidence/round-46/calibration/measure.py
  -> ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a
```

`/usr/bin/time` is absent on this host (`error: command not found: /usr/bin/time`, exit 127 — first attempt discarded), so wall time was taken from `date +%s.%N` around each run. Every run exported `REV=745a583181648cfc7f9c1b476cd1be7dc68f7433`, ran with `cwd=$W/clone` (all three statements have `"cwd": "clone"`, so the sibling-lane mirror is not consulted), and captured stdout and stderr to separate files.

## Statement argv, run twice sequentially, cwd = `$W/clone`

1. `tally-audit-v2 runner audit` — kind `cap`, obs `^(TALLY_AUDIT_V2_SELFTEST: \d+/\d+ pass)`, `sha_file` `tools/tally-audit-v2.py`, timeout 900
```
cd $W/clone && t0=$(date +%s.%N); REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/tally-audit-v2.py --selftest > $W/v2-r1.out 2> $W/v2-r1.err; rc=$?; t1=$(date +%s.%N)
cd $W/clone && t0=$(date +%s.%N); REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/tally-audit-v2.py --selftest > $W/v2-r2.out 2> $W/v2-r2.err; rc=$?; t1=$(date +%s.%N)
```
2. `tally-audit-v3 runner audit` — kind `cap`, obs `^(TALLY_AUDIT_V3_SELFTEST: \d+/\d+ pass)`, `sha_file` `tools/tally-audit-v3.py`, timeout 1800
```
cd $W/clone && t0=$(date +%s.%N); REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/tally-audit-v3.py --selftest > $W/v3-r1.out 2> $W/v3-r1.err; rc=$?; t1=$(date +%s.%N)
cd $W/clone && t0=$(date +%s.%N); REV=745a583181648cfc7f9c1b476cd1be7dc68f7433 python3 tools/tally-audit-v3.py --selftest > $W/v3-r2.out 2> $W/v3-r2.err; rc=$?; t1=$(date +%s.%N)
```
3. `bounded ANSI-C code_view` — kind `cap`, **same argv, same `cwd`, same `obs`, same `sha_file` as statement 2**, timeout 1800. The counter keys its observation cache on `(argv, cwd, obs, sha_file, kind)` (`measure.py:204`), so at the deciding run these two statements share **one** execution of `python3 tools/tally-audit-v3.py --selftest`. My two extra runs above are that same command, so its run-1/run-2 rows below are the same bytes.

## sha256 prefix at the freeze (`sha_file` statements)

```
cd $W/clone && sha256sum tools/tally-audit-v2.py | cut -c1-12        -> 7b11ba25aead
cd $W/clone && sha256sum tools/tally-audit-v3.py | cut -c1-12        -> da8c1ef4b30c
cd $W/clone && git show HEAD:tools/tally-audit-v2.py | sha256sum | cut -c1-12  -> 7b11ba25aead   (== what measure.py:149-150 computes)
cd $W/clone && git show HEAD:tools/tally-audit-v3.py | sha256sum | cut -c1-12  -> da8c1ef4b30c
```

## Standing claim, read with the counter's own functions

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 - <<'E'
import importlib.util, json, sys
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('c1','/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
text=open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md').read()
rows=m.last_rows(text)
stmts=json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/statements.json'))['statements']
for s in stmts:
    if 'tally-audit' in s['id'] or 'ANSI-C' in s['id']:
        cells=rows.get((s['kind'],s['id']))
        print(s['id'], cells, m.claim_of(s,cells))
E
```
Output — `claim_of` is `None` for all three:

```
tally-audit-v2 runner audit  claim: None
tally-audit-v3 runner audit  claim: None
bounded ANSI-C code_view     claim: None
```

The lane's `SCORECARD.md` is byte-identical at base, at the freeze and in the working tree (so this is the base text the counter will read at REV):

```
git hash-object SCORECARD.md                        -> f3793c445b264e5f8c59defad8f23e1859e3976f
git rev-parse 745a583…:SCORECARD.md                 -> f3793c445b264e5f8c59defad8f23e1859e3976f
git rev-parse 683eedd…:SCORECARD.md                 -> f3793c445b264e5f8c59defad8f23e1859e3976f
grep -n 'tally-audit-v2 runner audit|tally-audit-v3 runner audit|bounded ANSI-C code_view' SCORECARD.md
  -> 1657, 1698, 1809   (one row each — no later row overrides them)
sed -n '1657p;1698p;1809p' SCORECARD.md | grep -o '→' | wc -l   -> 0
```

## Per-statement result

| id | kind | claimed (as `claim_of` parses it) | observed run 1 | observed run 2 | same? | exit 1/2 | seconds 1/2 | timeout | verdict |
|---|---|---|---|---|---|---|---|---|---|
| tally-audit-v2 runner audit | cap | `None` (row present at L1657, evidence cell has no `→` claim) | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | yes (stdout sha `4ac4b8f31397…`, byte-identical) | 0 / 0 | 124.75 / 153.64 | 900 | **UNPARSED** |
| tally-audit-v3 runner audit | cap | `None` (row present at L1698, evidence cell has no `→` claim) | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | yes (stdout sha `2f90807506be…`, byte-identical) | 0 / 0 | 375.22 / 317.92 | 1800 | **UNPARSED** |
| bounded ANSI-C code_view | cap | `None` (row present at L1809, evidence cell has no `→` claim) | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` | yes (same bytes as the row above; counter caches one execution) | 0 / 0 | 375.22 / 317.92 | 1800 | **UNPARSED** |

Full observed tuples as `measure.py:observe` builds them (line, exit, tool sha12):

```
tally-audit-v2 runner audit  -> ('TALLY_AUDIT_V2_SELFTEST: 22/22 pass', '0', '7b11ba25aead')
tally-audit-v3 runner audit  -> ('TALLY_AUDIT_V3_SELFTEST: 35/35 pass', '0', 'da8c1ef4b30c')
bounded ANSI-C code_view     -> ('TALLY_AUDIT_V3_SELFTEST: 35/35 pass', '0', 'da8c1ef4b30c')
```

Byte identity of the two runs (stderr empty, 0 bytes, in all four runs):

```
sha256sum $W/v2-r1.out $W/v2-r2.out -> 4ac4b8f31397b830fc86e8464c893deaa0c1035f05f2f90efef2b2fc4ab54697  (both)
sha256sum $W/v3-r1.out $W/v3-r2.out -> 2f90807506bec97846d11b092086357fbe276cb2f46439fc603e18b4520a198e  (both)
diff $W/v2-r1.out $W/v2-r2.out -> identical (exit 0)
diff $W/v3-r1.out $W/v3-r2.out -> identical (exit 0)
wc -c $W/v2-r1.err $W/v2-r2.err $W/v3-r1.err $W/v3-r2.err -> 0 0 0 0
```

Picked lines re-derived with the counter's own `pick_line` on the captured bytes (not by eye):

```
tally-audit-v2 runner audit  r1/r2 pick_line = 'TALLY_AUDIT_V2_SELFTEST: 22/22 pass'
tally-audit-v3 runner audit  r1/r2 pick_line = 'TALLY_AUDIT_V3_SELFTEST: 35/35 pass'
bounded ANSI-C code_view     r1/r2 pick_line = 'TALLY_AUDIT_V3_SELFTEST: 35/35 pass'
```

Case tallies (from stdout): `grep -c '^CASE '` = 22 on v2-r1 (23 lines incl. the final `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`) and = 35 on v3-r1 (36 lines incl. the final `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`); `grep -c '^CASE code_view'` = 2 on v3-r1, so the 35 `^CASE ` lines are 2 `CASE code_view …` + 33 `CASE …`.

## Flags required by the item

- **Runs differ:** none. Both statements produced byte-identical stdout on both runs (sha equal above); stderr empty in all four runs. The tally is stable, so it is usable as a standing value.
- **obs regex matches more than one line or none:** exactly one match in each combined `stdout + '\n' + stderr` (`re.findall(..., re.M)` count = 1 in v2-r1, v2-r2, v3-r1, v3-r2). No ambiguity, no zero-match.
- **Longer than its `timeout`:** none. v2 max 153.64 s vs 900 (17 %); v3 max 375.22 s vs 1800 (21 %). Both comfortably inside.
- **Concurrency caveat (not a difference, a risk):** the counter observes all 22 statements at once (`ThreadPoolExecutor(max_workers=len(statements))`, `measure.py:201`) and both selftests fork subprocesses (`grep -c subprocess` = 7 in each tool; 699 and 946 lines). My two runs of each statement were themselves overlapped 2-way (v2-r1∥v3-r1, then v2-r2∥v3-r2), so the observed 2-way wall times are a lower bound for the deciding run's load; headroom is ≥4.8× in both cases, so a timeout at the deciding run is unlikely but is not something I measured.
- **Clone untouched by the selftests:** `git -C $W/clone status --porcelain` empty after all four runs; `git -C $W/clone rev-parse HEAD` still `745a5831…`.

## Why all three are UNPARSED (evidence only, no verdict claimed)

The rows exist and are the last row for their id, but none carries the form the counter parses. `CLAIM_SHA = →\s*`([^`]+)`,\s*exit (\d+),\s*tool sha256 `([0-9a-f]{12})`` (applied because all three have `sha_file`). Observed cell contents:

- **L1657 (v2 runner audit)** evidence cell: ``deciding-run receipt `C1_R33: … v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true` at `c17e593b`, counter `.ufo/evidence/round-33/c1/c1-measure.py`, tool `tools/tally-audit-v2.py` @ `7b11ba25…8d10``. No `→`, no `exit N` → `claim_of` = `None`. Note the sha it does state, `7b11ba25…`, agrees with the observed `7b11ba25aead`.
- **L1698 (v3 runner audit)** evidence cell: ``deciding receipt `C1_R35: … pub_kill=6/6 … ho_kill=4/4 ho_accept=3/3 ho_invalid=0 … C1_R35_PASS=true` at `34fa5b0`, counter `.ufo/evidence/round-35/c1/c1-measure.py` @ `d360a159…`, tool `tools/tally-audit-v3.py` @ `6188db16…``. No `→`, no `exit N` → `None`. **Separately stale:** the tool prefix it states, `6188db16…`, is not the freeze tool — the observed prefix is `da8c1ef4b30c` (round-35 revision vs the round-37 revision). Reformatting this row into claim form without correcting the prefix would convert UNPARSED into MISMATCH.
- **L1809 (bounded ANSI-C code_view)** evidence cell: ``.ufo/evidence/round-37/code-view/after.stdout` (2/2), `.ufo/evidence/round-37/tool-selftest-after.stdout` (35/35), `.ufo/evidence/round-37/c2-repin-after.stdout` (frozen r36 predicate PASS), S104`. No `→`, no `exit N` → `None`. The `(35/35)` it states agrees with the observed `35/35`, and the round-37 receipt `.ufo/evidence/round-37/tool-selftest-after.stdout` ends with the same line `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`; `.ufo/evidence/round-37/code-view/after.stdout` pins `tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`, consistent with the freeze file.

Exact evidence cell that `claim_of` accepts, computed from my observations (synthetic cells, nothing written to the lane):

```
`python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead`
  claim_of(synthetic row) -> ('TALLY_AUDIT_V2_SELFTEST: 22/22 pass', '0', '7b11ba25aead')
`python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`
  claim_of(synthetic row) -> ('TALLY_AUDIT_V3_SELFTEST: 35/35 pass', '0', 'da8c1ef4b30c')
`python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`
  claim_of(synthetic row) -> ('TALLY_AUDIT_V3_SELFTEST: 35/35 pass', '0', 'da8c1ef4b30c')
```

No `|` appears inside any of those three cells, so `cells_of` splitting is not a hazard for these rows (unlike the `sources-registry` row).

## Cross-check against the committed freeze receipt

`.ufo/evidence/round-46/before/c1-at-freeze.stdout` states exactly what I re-observed, independently and before my runs:

```
STATEMENT cap/tally-audit-v2 runner audit: claimed=- observed=TALLY_AUDIT_V2_SELFTEST: 22/22 pass|0|7b11ba25aead (exit=0) UNPARSED
STATEMENT cap/tally-audit-v3 runner audit: claimed=- observed=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0|da8c1ef4b30c (exit=0) UNPARSED
STATEMENT cap/bounded ANSI-C code_view: claimed=- observed=TALLY_AUDIT_V3_SELFTEST: 35/35 pass|0|da8c1ef4b30c (exit=0) UNPARSED
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C1_R46_PASS=false
```

## Not run (deliberately, out of seat scope)

- The deciding run of the C1 counter (`measure.py --lane … --rev … --base … --work …`): the L1's, per the measurement bounds. I did not run `--emit` or `--selftest` of the counter either.
- The C2/C3 counters, the no-harm script, `six-leg regression ledger` and every other statement: not my item. No build/lint/format gate: the parent owns post-integration gates.
- No git or jj mutation in the lane or the fleet repo: only `git clone`/`checkout` inside `/tmp/tameshi-r46-ExecStmt06/`, plus read-only `git show`/`rev-parse`/`hash-object` against the lane.

## Tooling

None installed or upgraded. The absent `/usr/bin/time` was worked around with `date +%s.%N` rather than installed (pacman transactions are paused host-wide).
