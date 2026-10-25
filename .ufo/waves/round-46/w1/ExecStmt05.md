seat: ExecStmt05
item: C1 statement re-observation of callback-authoritative wave accounting, required-command-receipt-binding, refusing-registry-replay, mutation report interop (cap rows, tool-sha claims) at freeze 745a583181648cfc7f9c1b476cd1be7dc68f7433

Verdict summary: all four statements are stable and observable (exit 0, one obs-regex match, 0.14–1.53 s against 900 s timeouts), and all four are **UNPARSED** — the standing SCORECARD row of each lacks the counter's claim grammar because every one of these four statements declares `sha_file`, so `claim_of` demands the `, tool sha256 \`<12 hex>\`` clause that none of the rows carries. No printed tally drifted: the numbers the rows assert in prose (`8/8`, `44/44`, `10/10`, `17/17`, exit 0) are exactly what the frozen commands print, and the frozen tool sha256 prefixes are `96b3038a77f8`, `9230c68e53a5`, `9fcd2dbba737`, `193ea6e32f89`.

## Setup (exact commands)

```
W=/tmp/tameshi-r46-ExecStmt05; rm -rf $W; mkdir -p $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

- `git -C $W/clone rev-parse HEAD` → `745a583181648cfc7f9c1b476cd1be7dc68f7433`
- `git -C $W/fleet/tameshi-shokunin rev-parse HEAD` → `745a583181648cfc7f9c1b476cd1be7dc68f7433`
- `ls $W/fleet` → 22 sibling symlinks + the `tameshi-shokunin` clone (not needed by these four statements, all `cwd: clone`).

Harness `/tmp/tameshi-r46-ExecStmt05/run.py` reproduces the counter's `env()` (drops `GIT_*`, sets `PYTHONDONTWRITEBYTECODE=1`, sets `REV`) and `pick_line()` (`re.search(pat, out, re.M)`, `group(1)`), runs each argv twice sequentially with `timeout=stmt['timeout']`, and records wall time, exit code, and the number of regex matches. Invocation:

```
cd /tmp/tameshi-r46-ExecStmt05 && python3 run.py 'callback-authoritative wave accounting' 'required-command-receipt-binding' 'refusing-registry-replay' 'mutation report interop'
```

The four frozen argvs (all `cwd=/tmp/tameshi-r46-ExecStmt05/clone`, all `timeout: 900`):

```
python3 tools/wave-accounting.py --selftest     obs ^(ACCOUNTING_SELFTEST: \d+/\d+ pass)
python3 tools/command-binding.py --selftest     obs ^(COMMAND_BINDING_SELFTEST: \d+/\d+ pass)
python3 tools/registry-replay.py --selftest     obs ^(REGISTRY_REPLAY_SELFTEST: \d+/\d+ pass)
python3 tools/mte-interop.py --selftest         obs ^(MTE_SELFTEST: \d+/\d+ pass)
```

Tool sha256 at the freeze (`cd /tmp/tameshi-r46-ExecStmt05/clone && for f in ...; do printf '%s %s\n' "$(sha256sum $f | cut -c1-12)" "$f"; done`):

```
96b3038a77f8 tools/wave-accounting.py
9230c68e53a5 tools/command-binding.py
9fcd2dbba737 tools/registry-replay.py
193ea6e32f89 tools/mte-interop.py
```

These equal the counter's own `git show HEAD:<sha_file>` prefixes (see the COUNTER-OBSERVE section), so worktree bytes and blob bytes agree at the freeze.

## Per-statement table

Standing claim read with the counter's own code (`importlib` of `.ufo/evidence/round-46/calibration/measure.py`, `last_rows(open('SCORECARD.md').read())`, `claim_of(stmt, rows.get((kind,id)))`) on the lane's current `SCORECARD.md`, which is byte-unchanged from HEAD (`git diff --stat HEAD -- SCORECARD.md` empty; `git status --porcelain -- SCORECARD.md` empty; HEAD `10a05fdf56d210988a30cf1a0a9dcd349441ba1a`).

| id | claimed (`claim_of`) | observed run 1 | observed run 2 | same? | exit | seconds | verdict |
|---|---|---|---|---|---|---|---|
| callback-authoritative wave accounting | `None` (row text: `→ frozen counter8/8 (\`ACCOUNTING_SELFTEST: 8/8 pass\`; extra cases \`ACCOUNTING_EXTRA_SELFTEST: 16/16 pass\`)`) | `ACCOUNTING_SELFTEST: 8/8 pass` + `0` + `96b3038a77f8` | same | yes | 0/0 | 0.90 / 0.92 | UNPARSED |
| required-command-receipt-binding | `None` (row text: `` `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0 (not a C1 statement) ``) | `COMMAND_BINDING_SELFTEST: 44/44 pass` + `0` + `9230c68e53a5` | same | yes | 0/0 | 1.53 / 1.49 | UNPARSED |
| refusing-registry-replay | `None` (row text: `` `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 (not a C1 statement) ``) | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` + `0` + `9fcd2dbba737` | same | yes | 0/0 | 0.37 / 0.36 | UNPARSED |
| mutation report interop | `None` (row text: `` `MTE_SELFTEST: 17/17 pass`, exit 0 at round 33 ... ``) | `MTE_SELFTEST: 17/17 pass` + `0` + `193ea6e32f89` | same | yes | 0/0 | 0.15 / 0.14 | UNPARSED |

Observed tuple order is the counter's: `(printed line, str(exit), sha256[:12] of sha_file at REV)`.

Counter-equivalent confirmation (the counter's own `observe()`/`claim_of()`/`emit_row()` called through `importlib`, not a hand re-implementation):

```
COUNTER-OBSERVE callback-authoritative wave accounting: claimed=- observed=ACCOUNTING_SELFTEST: 8/8 pass|0|96b3038a77f8 (exit=0) UNPARSED
COUNTER-OBSERVE required-command-receipt-binding: claimed=- observed=COMMAND_BINDING_SELFTEST: 44/44 pass|0|9230c68e53a5 (exit=0) UNPARSED
COUNTER-OBSERVE refusing-registry-replay: claimed=- observed=REGISTRY_REPLAY_SELFTEST: 10/10 pass|0|9fcd2dbba737 (exit=0) UNPARSED
COUNTER-OBSERVE mutation report interop: claimed=- observed=MTE_SELFTEST: 17/17 pass|0|193ea6e32f89 (exit=0) UNPARSED
```

These four lines are byte-identical to the frozen before-receipt `.ufo/evidence/round-46/before/c1-at-freeze.stdout:10-13`, which reports `C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21 rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C1_R46_PASS=false`. So these four are four of the 19 `unparsed`, none of the 2 `mismatches`, none of the `unobservable`.

## Why each row is UNPARSED (exact diagnosis)

All four statements declare `sha_file`, so `claim_of` uses `CLAIM_SHA = →\s*\`([^\`]+)\`,\s*exit (\d+),\s*tool sha256 \`([0-9a-f]{12})\``, not `CLAIM_BASE`. Probe output:

```
callback-authoritative wave accounting
  CLAIM_BASE -> None            tool sha256 clause present: False
required-command-receipt-binding
  CLAIM_BASE -> '→ `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0'    CLAIM_SHA -> None   tool sha256 clause present: False
refusing-registry-replay
  CLAIM_BASE -> '→ `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0'     CLAIM_SHA -> None   tool sha256 clause present: False
mutation report interop
  CLAIM_BASE -> '→ `MTE_SELFTEST: 17/17 pass`, exit 0'                 CLAIM_SHA -> None   tool sha256 clause present: False
```

- Three rows (command-binding, registry-replay, mte-interop) already carry a well-formed `→ \`LINE\`, exit N` claim and fail only on the missing `, tool sha256 \`<12 hex>\`` clause. Their substantive claim is correct; only the digest field is absent.
- `callback-authoritative wave accounting` (SCORECARD.md:1523) fails one step earlier: after the arrow it carries prose (`frozen counter8/8 (...)`), so even `CLAIM_BASE` does not match.
- Neither `→` character nor line content is the problem: the arrow is U+2192 and the quoted lines are exact.

Standing-row location: each of these ids appears twice in `SCORECARD.md` (older narrative rows at lines 249 / 1057 / 1150 / 1234, the standing rows at lines 1523 / 1524 / 1525 / 1526 inside the table headed `| Capability | What it can now do | Evidence pointer | First-working round |`). `last_rows` overwrites by `(kind,id)` in file order, so the 1523-1526 rows are the ones compared — confirmed by `claim_of` consuming exactly those evidence cells. `callback-authoritative wave accounting` is the only one of the four present in two `Capability` tables; last-row-wins resolves it to line 1523.

## Flags

- Two-run divergence: **none**. `cmp -s obs-<id>-run1.stdout obs-<id>-run2.stdout` → `IDENTICAL` for all four (full stdout, not just the picked line).
- obs regex matching more than one line: **none** (`obs_matches=1` on both runs, all four). Matching none: **none**.
- Exceeds `timeout`: **none** (max 1.53 s vs 900 s).
- **Contradiction to flag:** `SCORECARD.md:1524` and `:1525` end their evidence cell with `(not a C1 statement)`, yet `statements.json` lists `required-command-receipt-binding` and `refusing-registry-replay` as C1 statements (ids 10 and 11 of 22). The counter does not read that prose, so it costs nothing mechanically, but the standing text and the frozen statements list disagree. Any appended row built by `emit_row` replaces cells[2], so that phrase disappears automatically.
- Side effect of running: none. After all 8 selftest runs, `git -C $W/clone status --porcelain | wc -l` → `0`; the selftests write nothing into the clone.

## Substantive sub-claims inside the standing rows (checked, all hold)

- `callback-authoritative wave accounting`: row asserts the frozen counter prints `ACCOUNTING_SELFTEST: 8/8 pass` **and** `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`. Run-1 stdout contains both lines (27 lines total, 8 `ACCOUNTING_CASE ... ok`, 16 `ACCOUNTING_EXTRA_CASE ... ok`, then `FINDING: SELFTEST_PASS`). The `obs` regex only picks the first, so the extra tally is invisible to C1 — it is nevertheless accurate.
- `mutation report interop`: row states `jsonschema 4.25.1 installed via uv`. `python3 -c "import jsonschema; print(jsonschema.__version__)"` → `4.25.1` at `/usr/bin/python3`, and the selftest's 17 cases including the official schema/metrics paths all `PASS`. Sub-claim holds; note the row's provenance says "installed via uv" while the interpreter that resolved it here is the system python — the version is right either way and this is outside the C1 comparison.
- `required-command-receipt-binding` / `refusing-registry-replay`: the printed tallies (`44/44`, `10/10`) equal the row text exactly; both exit 0.

## Emit-form lines the counter derives for these four (evidence, from the counter's own `emit_row`)

Not a proposal and not written anywhere; these are the rows `--emit` would print, and each one re-parses through `claim_of` to the observed tuple (`claim_of -> (...) equals observed -> True` for all four):

```
EMIT_CAP | callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | `python3 tools/wave-accounting.py --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0, tool sha256 `96b3038a77f8` | round 22 |
EMIT_CAP | required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, tool sha256 `9230c68e53a5` | round 23 |
EMIT_CAP | refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0, tool sha256 `9fcd2dbba737` | round 24 |
EMIT_CAP | mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0, tool sha256 `193ea6e32f89` | round 25 |
```

## Bounds respected, and what was not run

- Edited files: this report only. Nothing written to `statements.json`, `measure.py`, `SCORECARD.md`, the lane's git index or jj state, `/home/vgpnk/Projects/shokuknow`, the fleet repo or any sibling lane. Scratch confined to `/tmp/tameshi-r46-ExecStmt05/`.
- The full 22-statement counter was **not** run by this seat (the deciding run is the L1's). Instead the counter module's `observe`/`claim_of`/`emit_row` were invoked for the four assigned statements only, into `/tmp/tameshi-r46-ExecStmt05/xwork`. `--selftest` of the counter was also not run (it exercises synthetic fixtures, not these statements, and the freeze already ships its result).
- No build, lint, test or formatter was run; no git mutating command and no jj command was run in the lane; no package manager was invoked (pacman paused host-wide) and no tool was installed.
