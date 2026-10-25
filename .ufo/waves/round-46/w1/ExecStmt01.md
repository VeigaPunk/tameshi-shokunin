seat: ExecStmt01
item: C1 statement re-observation — ran the frozen argv of `sources-registry`, `depth`, `calibration` twice each at the freeze rev and compared against their standing SCORECARD rows

Round 46, wave 1, C1 calibration seat. Read-only on the lane; all scratch under `/tmp/tameshi-r46-ExecStmt01/`. No lane file, no SCORECARD.md, no statements.json, no counter was edited. No tool installed.

## Setup (exact commands)

```
W=/tmp/tameshi-r46-ExecStmt01; rm -rf $W; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433; git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

Verification:
```
git -C $W/clone rev-parse HEAD                      -> 745a583181648cfc7f9c1b476cd1be7dc68f7433
git -C $W/fleet/tameshi-shokunin rev-parse HEAD     -> 745a583181648cfc7f9c1b476cd1be7dc68f7433
ls $W/fleet | wc -l                                 -> 21   (20 sibling-lane symlinks + the tameshi mirror)
sha256sum $W/clone/.ufo/evidence/round-46/calibration/statements.json
  -> a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9   (== the contract's statements_sha256 / stmts_pin)
```

Runner used for every observation (writes stdout/stderr/exit/wall to `$W/<label>.{out,err,meta}`, exports `REV`):

```
#!/bin/bash
label=$1; cwd=$2; shift 2
export REV=745a583181648cfc7f9c1b476cd1be7dc68f7433
W=/tmp/tameshi-r46-ExecStmt01
start=$(date +%s%N)
( cd "$cwd" && "$@" ) > "$W/$label.out" 2> "$W/$label.err"
code=$?
end=$(date +%s%N)
ms=$(( (end - start) / 1000000 ))
printf 'exit=%d wall_ms=%d wall_s=%d.%03d\n' "$code" "$ms" "$((ms/1000))" "$((ms%1000))" > "$W/$label.meta"
cat "$W/$label.meta"
```
(`/usr/bin/time` and `bc` are absent on this host; first attempt with `/usr/bin/time` returned `error: command not found: /usr/bin/time` and exit 127, discarded, and the wall clock was moved to `date +%s%N` nanoseconds in the runner above.)

## Statement argv, run twice sequentially, cwd = `$W/clone`

All three statements have `"cwd": "clone"`, `"sha_file": null` — so no `sha256sum <file>` line applies to any of them (nothing to print; stated rather than skipped silently). `REV=745a583181648cfc7f9c1b476cd1be7dc68f7433` in the env for all runs.

1. `sources-registry` (kind `cap`, obs `census`, timeout 300)
```
$W/run.sh sr1 $W/clone bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
$W/run.sh sr2 $W/clone bash .ufo/evidence/kaika-round-1/sources-census-v2.sh
```
2. `depth` (kind `axis`, obs `depth_score=(\d+)`, timeout 300)
```
$W/run.sh d1 $W/clone bash -c 'git show "$REV:tools/mutate-and-run.sh" | python3 -c '"'"'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'"'"''
$W/run.sh d2 $W/clone bash -c '... same argv ...'
```
3. `calibration` (kind `axis`, obs `monitor`, timeout 900)
```
$W/run.sh c1 $W/clone python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433
$W/run.sh c2 $W/clone python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

## Standing claim, read with the counter's own functions

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 - <<'E'
import importlib.util, json
spec = importlib.util.spec_from_file_location('c1', '.ufo/evidence/round-46/calibration/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
text = open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md').read()
rows = m.last_rows(text)
stmts = {s['id']: s for s in json.load(open('.ufo/evidence/round-46/calibration/statements.json'))['statements']}
for sid in ('sources-registry', 'depth', 'calibration'):
    s = stmts[sid]; cells = rows.get((s['kind'], sid))
    print('ID=%s kind=%s' % (sid, s['kind'])); print('  cells=%r' % (cells,)); print('  claim=%r' % (m.claim_of(s, cells),))
print('n_rows_cap=%d n_rows_axis=%d' % (sum(1 for k in rows if k[0]=='cap'), sum(1 for k in rows if k[0]=='axis')))
E
```
Output (cells truncated here, full text quoted per statement below):
```
ID=sources-registry kind=cap
  claim=None
ID=depth kind=axis
  claim=('9',)
ID=calibration kind=axis
  claim=('8',)
n_rows_cap=19 n_rows_axis=2
```
The lane's `SCORECARD.md` is the base text at the freeze, confirmed:
```
git show 683eedd:SCORECARD.md | sha256sum -> 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1
git show 745a583:SCORECARD.md | sha256sum -> 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1
sha256sum SCORECARD.md              -> 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1
cur==freeze=True  base_bytes=206619  cur_bytes=206619  cur.startswith(base)=True
```

## Per-statement result

| id | kind | claimed (as `claim_of` parses it) | observed run 1 | observed run 2 | same? | exit 1/2 | seconds 1/2 | timeout | verdict |
|---|---|---|---|---|---|---|---|---|---|
| sources-registry | cap | `None` (row present, evidence cell unparseable) | `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | yes (stdout sha `ce02de309cb0…`) | 0 / 0 | 0.170 / 0.178 | 300 | **UNPARSED** |
| depth | axis | `9` | `9` | `9` | yes (stdout sha `d3143a682709…`) | 0 / 0 | 0.013 / 0.012 | 300 | **MATCH** |
| calibration | axis | `8` | `6` | `6` | yes (stdout sha `5d352f12cc1e…`) | 0 / 0 | 29.731 / 29.422 | 900 | **MISMATCH** |

Byte identity of the two runs (all stderr empty, 0 bytes, in both runs of all three statements):
```
sha256sum sr1.out sr2.out -> ce02de309cb0c58b323ef1152fa6ca5428f32b4cd198ecdcd94b7d890cfcc659  (both)
sha256sum d1.out  d2.out  -> d3143a6827097dbce390a8292c82022b1b2c10104c968d98593e0e900d7ed2eb  (both)
sha256sum c1.out  c2.out  -> 5d352f12cc1ef42118ecd4b420dab92e5cff6aabd2f0857a3f2e32b90bd51154  (both)
diff sr1.out sr2.out -> identical (exit 0); diff d1.out d2.out -> identical; diff c1.out c2.out -> identical
```

Picked lines re-derived with the counter's own `pick_line` on the captured bytes (not by eye):
```
sources-registry sr1/sr2 pick='rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)'
depth            d1/d2  pick='9'      (obs regex matches: 1)
calibration      c1/c2  pick='6'      (obs 'monitor': json.loads(stdout)['calibration_restraint_score'])
```

## Flags required by the item

- **Runs differ:** none. All three statements produced byte-identical stdout on both runs; stderr empty.
- **obs regex matches more than one line or none:** none. `depth`'s regex `depth_score=(\d+)` matches exactly one line (`grep -c` = 1). The two `census` anchors each occur exactly once in the 41-line census output (`grep -c '^== A rows$'` = 1; `grep -c '^SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)$'` = 1, at output lines 1, 2 and 41). `calibration`'s `monitor` pick reads a single JSON scalar (`"calibration_restraint_score"` occurs once); the JSON body is 1855 lines (`wc -l c1.out`) and parses cleanly (exit 0).
- **Longer than its `timeout`:** none. 0.170/0.178 s vs 300; 0.013/0.012 s vs 300; 29.731/29.422 s vs 900 (3.3 % of budget). The calibration monitor is the only slow one and it is well inside.
- **External-input dependence (stability caveat, not a difference):** the `calibration` statement's stdout embeds `external_inputs` hashes of **live fleet** paths (`/home/vgpnk/Projects/shokunin/SCORECARD.md`, sibling `*-shokunin/...`, `.omp/agent/config.yml`) because the round-21 wrapper delegates to `.ufo/evidence/round-18/measure.py`, which hashes them for `input-drift` vetoes. The two runs were byte-identical, but that identity is a function of concurrent fleet writes, not of the clone; the picked scalar was `6` in both. `sources-registry`'s script has zero references to `/home/vgpnk` (`grep -c` = 0) and `depth` reads only `git show "$REV:…"` in the clone, so those two are clone-local.

## What the observations mean for the standing rows (evidence only, no verdict claimed)

**sources-registry — UNPARSED for two independent reasons.** Standing row is SCORECARD.md line 1609, inside the `| Capability | What it can now do | Evidence pointer | First-working round |` table at line 1607 (last `cap`-kind row for this id; the later `sources-registry` rows at lines 2020/2081/2146/2164 sit in one-column tables whose header cell 0 is not exactly `Capability`, so `last_rows` correctly skips them).
 1. Arrow order. The evidence cell reads `` `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; … `` — the printed line comes *after* `exit 0`, while `CLAIM_BASE = →\s*`([^`]+)`,\s*exit (\d+)` requires line-then-exit. `re.search(CLAIM_BASE, cell)` → `None`, hence `claim_of` → `None`.
 2. Unescaped pipes inside the evidence cell. The cell embeds `` `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` `` with two literal `|`; the row has 7 pipes and `cells_of` yields 6 cells, so `cells[2]` is cut mid-code-span and `cells[3]` is the fragment `S[0-9]{3} \`. Even with the arrow order fixed, the row is structurally misaligned.
 3. Stale count in the same cell: it states `→ 99 rows at round 35` while the frozen command prints `rows=117` (output lines 1–2: `== A rows` / `117`).
 4. What the counter would emit for this statement, computed with `emit_row` on my observation (not appended by me):
    ```
    EMIT_CAP | sources-registry | curate where the lane learns: … census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0 | S[0-9]{3} \ |
    ```
    The 4th cell comes from `old[3]`, i.e. the pipe-split fragment — the true first-working cell is `old[5]` = `fleet round 1 (kaika)`. Appending this line verbatim would produce a malformed row that nevertheless satisfies `claim_of` (it compares only printed-line/exit/sha), so the pipe layout and the 4th cell must be corrected by hand when the row is restated.

**depth — MATCH.** Line 1536, `| depth | 9 | … command D above prints \`recorded_cases=9 depth_score=9\` | … |`. Observed `recorded_cases=9 depth_score=9` twice; claim `9` == observed `9`. Emitted form for reference: `EMIT_AXIS | depth | 9 | <same evidence cell> |`.

**calibration — MISMATCH.** Line 1537, `| calibration | 8 | … | 29 (restored 6 → 8); held 30 |`. Observed `calibration_restraint_score = 6` twice; claim `8` != observed `6`. This matches the contract's `scores_at_base`: "calibration 6 (round-21 coldread monitor restraint)". Emitted form for reference: `EMIT_AXIS | calibration | 6 | <same evidence cell> |`.

## Cross-check against the committed freeze receipt

`.ufo/evidence/round-46/before/c1-at-freeze.stdout` states exactly what I re-observed, independently:
```
STATEMENT cap/sources-registry: claimed=- observed=rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 (exit=0) UNPARSED
STATEMENT axis/depth: claimed=9 observed=9 (exit=0) MATCH
STATEMENT axis/calibration: claimed=8 observed=6 (exit=0) MISMATCH
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583… C1_R46_PASS=false
```

## Not run (deliberately, out of seat scope)

- The deciding run of the C1 counter (`measure.py --lane … --rev … --base … --work …`): the L1's, per the measurement bounds. I also did not run `measure.py --emit` or `--selftest` (not part of this item).
- The C2 and C3 counters, the no-harm script, and any build/lint/format gate: not my item; the parent owns post-integration gates.
- No git/jj mutation of any kind in the lane or the fleet repo: only `git clone`/`checkout` inside `/tmp/tameshi-r46-ExecStmt01/`, plus read-only `git show`/`rev-parse` against the lane.

## Tooling

None installed or upgraded (the two missing host binaries, `/usr/bin/time` and `bc`, were worked around in shell rather than installed, per the paused-pacman guard).
