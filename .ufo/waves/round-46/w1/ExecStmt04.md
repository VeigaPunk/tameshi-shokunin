seat: ExecStmt04
item: C1 statement re-observation of `effective expectation reconciliation`, `retained invocation-context gate`, `hermetic env-differential probe` (two runs each in a freeze clone, standing claim re-read with the counter's own `last_rows`/`claim_of`, plus an explicit environment-differential probe of the three frozen commands)

# ExecStmt04 — C1 re-observation + effective-expectation reconciliation + hermetic env-differential probe (round 46, wave 1)

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`
(base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`). Read-only: no lane file written except this report;
no `statements.json`, no counter, no `SCORECARD.md` edited; all scratch under `/tmp/tameshi-r46-ExecStmt04/`.
No tool installed, upgraded or removed (see §9).

## Result in one line

All three assigned statements **UNPARSED** at the freeze — their last standing `SCORECARD.md` rows
(lines 1520, 1521, 1522) carry a prose tally, not the counter's claim grammar — while both runs of each
frozen command are byte-identical, exit 0, and agree with `before/c1-at-freeze.stdout`; the reconciliation
text that turns each row into a MATCH is printed in §6. The three are **not equally hermetic**: the
reconciliation selftest collapses to `SELFTEST: FAIL (3/66 …)`, exit 1, when `jj` is not on `PATH` (§7),
and the env-diff selftest collapses to `ENVDIFF_SELFTEST: 1/9 pass`, exit 1, when `bwrap` is not on `PATH`.

## 1. Setup (exact commands)

```
W=/tmp/tameshi-r46-ExecStmt04; rm -rf $W; mkdir -p $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 745a583181648cfc7f9c1b476cd1be7dc68f7433
```

Verified: `git -C $W/clone rev-parse HEAD` → `745a583181648cfc7f9c1b476cd1be7dc68f7433`;
`git -C $W/fleet/tameshi-shokunin rev-parse HEAD` → same; `ls $W/fleet` → 21 sibling symlinks + the
`tameshi-shokunin` mirror. A second untouched clone `$W/clone2` at the same rev was used only to read the
committed state of `.ufo/evidence/round-15/` (§7.3).

Statements list pin re-derived by this seat, not trusted from the counter:

```
$ sha256sum .ufo/evidence/round-46/calibration/statements.json      # run in the lane (read-only)
a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9  .ufo/evidence/round-46/calibration/statements.json
```

(the digest equals `STATEMENTS_SHA256` in `measure.py` and `statements_sha256` in `contract.json`; the
harness re-printed it: `statements sha256: a15a8b45…46e9 (pin a15a8b45…46e9)`.)

## 2. Method

Harness `/tmp/tameshi-r46-ExecStmt04/run_obs.py` imports the counter
(`importlib` on `.ufo/evidence/round-46/calibration/measure.py`), reuses its `env()` (drop every `GIT_*`,
`PYTHONDONTWRITEBYTECODE=1`), its `pick_line()` (including the `census` and `monitor` specials) and its
`{work}`/`{clone}`/`{rev}` substitution verbatim, runs each statement's frozen `argv` **twice,
sequentially**, `cwd=clone` except `six-leg regression ledger` (`cwd=mirror`), with `REV=745a583…` in the
environment, and records stdout+stderr, exit code, wall seconds and the number of `obs` matches.

```
$ cd /tmp/tameshi-r46-ExecStmt04 && python3 run_obs.py > harness.log 2>&1; echo "EXIT=$?"
EXIT=0                                   # wall 1776.43 s for 22 statements x 2 runs
```

Raw transcripts: `/tmp/tameshi-r46-ExecStmt04/raw-<id>-run{1,2}.txt`; machine summary
`/tmp/tameshi-r46-ExecStmt04/results.json`. For the `sha_file` statements the seat re-derived the prefix
itself at the freeze (`git -C clone show HEAD:<file>` → sha256 → first 12 hex, plus a plain
`sha256sum <file> | cut -c1-12` in the checkout, identical because the clone is clean):

```
$ cd /tmp/tameshi-r46-ExecStmt04/clone && for f in tools/mutate-and-run.sh tools/repeat-control.py tools/pin-disposition.py \
    tools/witness-metadata.py tools/evidence-disposition.py .ufo/evidence/round-15/verify.py tools/env-diff.py \
    tools/wave-accounting.py tools/command-binding.py tools/registry-replay.py tools/mte-interop.py \
    tools/tally-audit-v2.py tools/tally-audit-v3.py tools/write-path-census-v2.py tools/write-path-census-v3.py \
    tools/staged-id-guard.py; do printf '%-42s ' "$f"; sha256sum "$f" | cut -c1-12; done
tools/evidence-disposition.py   39ee5c5effd9
.ufo/evidence/round-15/verify.py 7e4519d9a0ea
tools/env-diff.py               e8b47ab7cf23
(... 13 more, all equal to the at-freeze receipt, §8)
```

Standing claims were read with the counter's own helpers, not by eye:

```
$ python3 - <<'E'
import importlib.util, json, subprocess
LANE='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
spec=importlib.util.spec_from_file_location('m',LANE+'/.ufo/evidence/round-46/calibration/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
REV='745a583181648cfc7f9c1b476cd1be7dc68f7433'
rev_sc=subprocess.run(['git','-C',LANE,'show',REV+':SCORECARD.md'],capture_output=True,text=True).stdout
wt_sc=open(LANE+'/SCORECARD.md').read()
print('worktree==rev SCORECARD:', wt_sc==rev_sc)
stmts=json.load(open(LANE+'/.ufo/evidence/round-46/calibration/statements.json'))['statements']
rows=m.last_rows(rev_sc)
for s in stmts: print(s['id'], m.claim_of(s, rows.get((s['kind'],s['id']))))
E
worktree==rev SCORECARD: True            # 206619 characters, the lane worktree file is the freeze text
```

`last_rows` yields 21 rows for 22 statements: the `freshness` axis has **no** standing axis row at all
(`ABSENT`), so its claim is unparsed by absence, not by wording.

## 3. Per-statement table — the three assigned statements (primary)

`claimed` = `claim_of(stmt, rows.get((kind,id)))` on the freeze `SCORECARD.md`; `observed` = the picked
line plus exit and, for `sha_file` statements, the tool sha256 prefix; `secs` = run1/run2 wall.

| id | claimed | observed run 1 | observed run 2 | same? | exit | seconds | verdict |
|---|---|---|---|---|---|---|---|
| effective expectation reconciliation | — (row line 1520: `` `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 ``) | `SELFTEST: PASS (66/66)` \| 0 \| `39ee5c5effd9` | `SELFTEST: PASS (66/66)` \| 0 \| `39ee5c5effd9` | yes | 0/0 | 3.24 / 3.26 | **UNPARSED** |
| retained invocation-context gate | — (row line 1521: `` `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…` → exit0, copied-source CLI selftest49/49 ``) | `SELFTEST: PASS (49/49)` \| 0 \| `7e4519d9a0ea` | `SELFTEST: PASS (49/49)` \| 0 \| `7e4519d9a0ea` | yes | 0/0 | 2.18 / 2.07 | **UNPARSED** |
| hermetic env-differential probe | — (row line 1522: `` `python3 tools/env-diff.py --selftest` actual9/9 (`ENVDIFF_SELFTEST: 9/9 pass`) ``) | `ENVDIFF_SELFTEST: 9/9 pass` \| 0 \| `e8b47ab7cf23` | `ENVDIFF_SELFTEST: 9/9 pass` \| 0 \| `e8b47ab7cf23` | yes | 0/0 | 0.23 / 0.23 | **UNPARSED** |

Each of the three rows asserts the right number in prose (66/66, 49/49, 9/9) but in a form the counter
cannot read: no `` `value` `` directly after `→`, no `, exit N`, and (all three declare `sha_file`) no
`, tool sha256 \`12hex\``. That is the whole defect — the printed values themselves have not drifted.

## 4. Per-statement table — the other 19 statements (corroboration only; owned by sibling seats)

Run for completeness so the wave has one uniform measurement; the seat makes no claim on them.

| id | kind | claimed | observed (identical both runs) | exit | seconds r1/r2 | verdict |
|---|---|---|---|---|---|---|
| sources-registry | cap | — | `rows=117 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` \| 0 | 0 | 0.17/0.16 | UNPARSED |
| mutation sweep runner | cap | — | `MUTATE_SELFTEST: 106/106 pass` \| 0 \| `a7d3f2dd7d47` | 0 | 5.68/5.67 | UNPARSED |
| six-leg regression ledger | cap | `REGRESSION: PASS (cases=9 passed=9 …)` \| 0 | `REGRESSION: PASS (cases=9 passed=9` \| 0 | 0 | 156.14/178.79 | **MISMATCH** |
| repeated pristine-control gate | cap | — | `SELFTEST: PASS (29 cases)` \| 0 \| `296fe566dc59` | 0 | 0.83/0.81 | UNPARSED |
| six-leg content-disposition probe | cap | — | `SELFTEST: PASS (19/19)` \| 0 \| `331529eadafe` | 0 | 1.03/1.02 | UNPARSED |
| exposed witness provenance correction | cap | — | `SELFTEST: PASS 39/39` \| 0 \| `df3390682a04` | 0 | 1.50/1.49 | UNPARSED |
| callback-authoritative wave accounting | cap | — | `ACCOUNTING_SELFTEST: 8/8 pass` \| 0 \| `96b3038a77f8` | 0 | 0.88/1.12 | UNPARSED |
| required-command-receipt-binding | cap | — | `COMMAND_BINDING_SELFTEST: 44/44 pass` \| 0 \| `9230c68e53a5` | 0 | 1.50/1.51 | UNPARSED |
| refusing-registry-replay | cap | — | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` \| 0 \| `9fcd2dbba737` | 0 | 0.38/0.39 | UNPARSED |
| mutation report interop | cap | — | `MTE_SELFTEST: 17/17 pass` \| 0 \| `193ea6e32f89` | 0 | 0.15/0.16 | UNPARSED |
| tally-audit-v2 runner audit | cap | — | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` \| 0 \| `7b11ba25aead` | 0 | 125.68/115.29 | UNPARSED |
| tally-audit-v3 runner audit | cap | — | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| 0 \| `da8c1ef4b30c` | 0 | 267.54/260.36 | UNPARSED |
| bounded ANSI-C code_view | cap | — | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| 0 \| `da8c1ef4b30c` | 0 | 266.26/305.86 | UNPARSED |
| write-path-census-v2 | cap | — | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` \| 0 \| `402285329588` | 0 | 0.05/0.05 | UNPARSED |
| write-path census destination resolution | cap | — | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` \| 0 \| `095924a7a165` | 0 | 0.06/0.06 | UNPARSED |
| staged-id adoption guard | cap | — | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` \| 0 \| `03a796c5726c` | 0 | 0.05/0.06 | UNPARSED |
| depth | axis | `9` | `9` | 0 | 0.03/0.03 | **MATCH** |
| calibration | axis | `8` | `6` | 0 | 32.59/30.16 | **MISMATCH** |
| freshness | axis | — (no axis row) | `9` | 0 | 0.76/0.75 | UNPARSED |

`|` inside an observed value separates the observed tuple (`line | exit | sha`), not table columns.

## 5. Flags the item asked for

1. **Two runs differing (unstable tally): none.** All 22 statements returned identical observed tuples and
   identical exit codes in run 1 and run 2, including the two heavy ones (regression 156 s vs 179 s wall,
   tally-audit-v3 268 s vs 260 s) — wall time varies, the printed tally does not.
2. **`obs` regex matching more than one line: none.** `matches=regex:1` for all 19 regex statements;
   `census:rows=1 clean=1` for `sources-registry`; `monitor:1` (valid JSON, key present) for `calibration`.
3. **No `obs` match / unobservable: none.** Every statement produced its picked line on both runs.
4. **Command exceeding its `timeout`: none.** Worst ratio is `bounded ANSI-C code_view` 305.86 s / 1800 s
   = 0.170; then tally-audit-v3 0.149, tally-audit-v2 0.140, six-leg regression ledger 178.79 s / 2700 s
   = 0.066.
5. **Claim-surface defect worth the L1's attention (not mine to fix):** `six-leg regression ledger`'s
   `obs` regex `^(REGRESSION: \w+ \(cases=\d+ passed=\d+)` truncates the real summary
   `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, so the only string
   that can match is the syntactically unbalanced prefix `REGRESSION: PASS (cases=9 passed=9`. The standing
   row currently states `REGRESSION: PASS (cases=9 passed=9 …)` and therefore MISMATCHes on one literal
   `…`. A reconciled row must state the truncated prefix verbatim.
6. **`calibration` axis drift:** the standing axis row states `8`; the monitor prints `6`
   (`coldread/measure.py --repo {clone} --rev {rev}` → `calibration_restraint_score` = 6, twice, 32.6 s /
   30.2 s). This is the one genuine value drift in the 22 and it belongs to the axis seat, not to me; it is
   reported because the contract's `scores_at_base` says calibration 6, i.e. the *row* is stale, not the
   monitor.
7. **Two statements share one argv** (`tally-audit-v3 runner audit`, `bounded ANSI-C code_view` →
   `python3 tools/tally-audit-v3.py --selftest`). The counter dedupes them by key, so both rows must state
   the same observed tuple; the seat ran them as two independent double-runs and got the same tuple four
   times out of four.

## 6. Effective expectation reconciliation — exact text that makes each row a MATCH

Produced with the counter's own `emit_row(stmt, observed, old_cells)` (so `what` and `first` are the
standing cells, unchanged), and round-tripped back through `last_rows`/`claim_of`:

```
$ python3 - <<'E'   # emit rows for the three assigned statements
... m.emit_row(s, tuple(results[s['id']][0]['observed']), rows.get((s['kind'], s['id']))) ...
```

```
EMIT_CAP | effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`, exit 0, tool sha256 `39ee5c5effd9` | round 14 |
EMIT_CAP | retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → `SELFTEST: PASS (49/49)`, exit 0, tool sha256 `7e4519d9a0ea` | round 15 |
EMIT_CAP | hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23` | round 21 |
```

Round-trip proof (same helpers, synthetic table built from all 19 emitted cap rows):

```
$ python3 - <<'E'
... build '| Capability | What | Evidence | First |' table from emit_row() output ...
... m.last_rows(text) ; m.claim_of(s, rows[(s['kind'], s['id'])]) == observed ...
E
emitted cap rows: 19 roundtrip mismatches: []
```

So the entire 19-row capability surface reconciles mechanically; a wave that appends such a block leaves
`mismatches+unparsed+unobservable` at 2 (the two axis defects of §5.5–5.6) until the axis rows are fixed.
Because `append_only` is measured against **base** `683eedd`, appending a fresh round-46 capability table is
sufficient — the round-31 rows (lines 1515–1526) may stay untouched, and `last_rows` takes the last
standing row.

## 7. Hermetic env-differential probe of the three frozen commands (seat-added, beyond the item's two runs)

`/tmp/tameshi-r46-ExecStmt04/probe.py` runs each frozen `argv` (cwd = clone) under four explicit profiles
and then under two targeted dependency strips:

- **P0_counter** — the counter's `env()` (inherited minus `GIT_*`, `PYTHONDONTWRITEBYTECODE=1`, `REV` set).
- **P1_minimal** — `env -i PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME=/nonexistent TMPDIR=$W/probe-tmp LANG=C LC_ALL=C TZ=UTC`.
- **P2_minimal_hostile** — P1 plus `LANG/LC_ALL=en_US.UTF-8 TZ=Pacific/Chatham COLUMNS=20 LINES=5 TERM=dumb PYTHONPATH=/nonexistent GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent`.
- **P3_counter_hostile** — P0 plus the same hostile additions.

```
$ cd /tmp/tameshi-r46-ExecStmt04 && python3 probe.py /tmp/tameshi-r46-ExecStmt04/clone
```

| statement | P0 | P1 | P2 | P3 | `jj` off PATH only | `jj` added to P1 | `bwrap` off PATH |
|---|---|---|---|---|---|---|---|
| effective expectation reconciliation | `PASS (66/66)` exit 0 | **`FAIL (3/66 …)` exit 1** | **`FAIL (3/66 …)` exit 1** | `PASS (66/66)` exit 0 | **`FAIL (3/66 …)` exit 1** | `PASS (66/66)` exit 0 | not required |
| retained invocation-context gate | `PASS (49/49)` exit 0 | `PASS (49/49)` exit 0 | `PASS (49/49)` exit 0 | `PASS (49/49)` exit 0 | `PASS (49/49)` exit 0 | n/a | not required |
| hermetic env-differential probe | `9/9 pass` exit 0 | `9/9 pass` exit 0 | `9/9 pass` exit 0 | `9/9 pass` exit 0 | `9/9 pass` exit 0 | n/a | **`1/9 pass` exit 1** |

### 7.1 Finding — `effective expectation reconciliation` is `PATH`-sensitive through `jj`

Under P1/P2 the selftest fails exactly three of its 66 cases, all of them the jj ones:

```
SELFTEST: FAIL (3/66 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.<x>)
```

Exit code 1 (`env -i … python3 tools/evidence-disposition.py --selftest > f 2>&1; echo $?` → `EXIT=1`).
The differentiator is `jj` alone, not `HOME`, not locale, not `GIT_DIR`:

- `jj` resolves to `/home/vgpnk/.local/bin/jj`; the counter's `env()` inherits the host `PATH`, which is why
  the deciding command passes today.
- Strip only `/home/vgpnk/.local/bin` from the inherited `PATH` → still `FAIL (3/66)`, `EXIT=1`.
- Add **only** `jj` to the minimal `PATH` (`ln -sf /home/vgpnk/.local/bin/jj $W/nobwrap/jj`, `HOME=/nonexistent`)
  → `SELFTEST: PASS (66/66)`, `EXIT=0`.

The tool documents the dependency in its own docstring (`tools/evidence-disposition.py:121`,
"Selftest also requires `jj` for its isolated colocated-repository cases"), but the printed PASS line and the
standing SCORECARD row do not. Consequence for C1: on a host without `jj`, the picked line becomes
`SELFTEST: FAIL (3/66 failed: …)`, which the `obs` regex `^(SELFTEST: PASS \(\d+/\d+\))` cannot match, so
the statement flips from UNPARSED to **UNOBSERVABLE** (and `total` grows by one) rather than to MISMATCH.
This is a precondition of the standing value, and a reconciled row that states the value without the
precondition would be stating something weaker than what it observed.

### 7.2 Finding — `hermetic env-differential probe` is `PATH`-sensitive through `bwrap`, and it lies about it

With `bwrap` absent from `PATH` (shim dir of symlinks to the ordinary coreutils, python3, git, jq — no
`bwrap`):

```
$ cd /tmp/tameshi-r46-ExecStmt04/clone && env -i PATH=/tmp/tameshi-r46-ExecStmt04/nobwrap HOME=/nonexistent \
    TMPDIR=/tmp/tameshi-r46-ExecStmt04/probe-tmp LANG=C LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
    python3 tools/env-diff.py --selftest
ENVDIFF_CASE missing-bwrap PASS
ENVDIFF_CASE timeout FAIL
ENVDIFF_CASE pin-mismatch-public-cli FAIL
ENVDIFF_SELFTEST: 1/9 pass
EXIT=1
```

Eight of nine cases fail; the printed line still matches the `obs` regex, so the counter would record a
**MISMATCH** (`ENVDIFF_SELFTEST: 1/9 pass` ≠ the row's `9/9`) — a louder failure mode than 7.1, but the same
class: a host dependency (`bwrap`, `/usr/bin/bwrap`, bubblewrap 0.13.1) that neither the value nor the row
declares. `execute()` returns `{"error": "BWRAP_UNAVAILABLE"}` when `shutil.which("bwrap")` is empty, and
only the `missing-bwrap` case is designed to pass in that state.

### 7.3 The retained invocation-context gate is the hermetic one, and it retains its own invocation context

- Invariant across P0–P3 and across the `jj` strip: `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)`
  (line 21 of a 49-line transcript under P0; 44 lines under the minimal-`PATH` run, same picked line, exit 0).
  It scrubs `GIT_*` itself (`verify.py:148,282`) so `GIT_DIR=/nonexistent` cannot poison it.
- It **does** write into the tree it runs from, once per invocation, never overwriting: the clean freeze
  clone `$W/clone2` carries `attempt-2/`, `attempt-3/`, `verification-2.json`, `verification-3.json`
  committed; after this seat's 7 invocations in `$W/clone` the tree holds `attempt-4…attempt-10` and
  `verification-4…verification-10.json` (`git -C $W/clone status --porcelain` lists exactly those 14
  untracked paths, nothing else). `write_exclusive()` (`verify.py:250-259`) raises
  `verify.py: refusing to overwrite existing receipt …` on a collision, but the attempt counter means a
  second run **succeeds** with the same printed value — confirmed by run 1/run 2 both exiting 0 in the same
  clone. So the "two runs differ" hazard does not fire, and a deciding run in a fresh `--work` clone starts
  at `attempt-4` with an unchanged value.
- The argv carries a **fixed** rev `7650fe4db89f3a706aed63d048ac47e02289cc72`, not `{rev}`: the statement
  is pinned to the round-15 context-gate revision and is invariant to `REV` by construction. `{rev}` only
  reaches it through the environment variable, which the tool does not read for this argv.

## 8. Agreement with the L1's at-freeze receipt

Compared programmatically against `.ufo/evidence/round-46/before/c1-at-freeze.stdout`
(parsed `STATEMENT kind/id: claimed=… observed=… (exit=…) VERDICT`):

```
$ python3 - <<'E'  # compare results.json observed tuples to the before receipt
...
disagreements: 0
```

22/22 observed tuples agree, including all three of mine (`SELFTEST: PASS (66/66)|0|39ee5c5effd9`,
`SELFTEST: PASS (49/49)|0|7e4519d9a0ea`, `ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23`) and the 16 tool sha256
prefixes. The receipt's verdict column (`mismatches=2 unparsed=19 unobservable=0 append_only=1 total=21`,
`C1_R46_PASS=false`) is reproduced exactly by this seat's own claim reads; the seat's own tally from the
three assigned statements is 3 UNPARSED, 0 MISMATCH, 0 UNOBSERVABLE.

## 9. Tooling record

Nothing installed, upgraded or removed; `pacman` untouched. Pre-existing and used:
Python 3.14.8, git 2.56.0, jj 0.45.1 (`/home/vgpnk/.local/bin/jj`), bubblewrap 0.13.1 (`/usr/bin/bwrap`).

## 10. Lane state / bounds

- Lane worktree `git status --porcelain` before this report: only the pre-existing
  `?? .ufo/waves/round-46/w1.ready`; nothing written by this seat inside the lane except this report.
- No `git add/commit/stash/checkout/switch/reset/pull/push` and no `jj` command ran in the lane; the only
  git mutations were `git clone`/`git checkout --detach` inside `/tmp/tameshi-r46-ExecStmt04/`.
- `git -C $W/fleet/tameshi-shokunin status --porcelain` → empty after the two `--regression` runs, i.e. the
  mirror tree is clean; the nine legs materialized their pinned blobs into `$W/regression-wd` (7.0 MB, nine
  case dirs + `specs/`) and only read the sibling lanes' object stores (`REGRESSION_PIN … repo=/tmp/…/fleet/<sibling>`
  for each of the nine legs).
- Scratch left in `/tmp/tameshi-r46-ExecStmt04/` (`clone`, `clone2`, `fleet/`, `regression-wd/`,
  `raw-*.txt`, `results.json`, `claims.json`, `harness.log`, `probe*.txt`, `run_obs.py`, `probe.py`,
  `nobwrap/`, `home-ok/`). The failed-selftest fixture dirs the tool leaves in `/tmp`
  (`/tmp/tameshi-r14-evidence-disposition-selftest.*`, created by the P1/P2 strips) were removed.

## 11. Risks and blockers for the deciding run

1. **`jj` on `PATH` is a precondition of C1 statement 7** (§7.1). The L1's deciding run must inherit a
   `PATH` that resolves `jj`, or that statement becomes UNOBSERVABLE and `C1_R46_PASS=false` for a reason
   unrelated to any SCORECARD value. Cheapest hardening, if the L1 wants it: none is available to this seat
   (the tool is a frozen statement target; editing it is out of scope and would break the `sha_file` claim).
   The safe operational rule is: deciding run with the host environment, never `env -i`.
2. **`bwrap` on `PATH` is a precondition of C1 statement 9** (§7.2), same class, but it degrades to a
   readable MISMATCH instead of an UNOBSERVABLE.
3. **`six-leg regression ledger` cannot match any natural sentence** (§5.5): its expected string is an
   unbalanced prefix. Whoever appends that row must paste `REGRESSION: PASS (cases=9 passed=9` exactly,
   closing nothing.
4. **Two axis defects remain outside this seat** (§5.6–5.7): `calibration` row states 8 vs observed 6, and
   `freshness` has no standing axis row at all. With the 19 capability rows reconciled as in §6, `total`
   would still be 2.
5. No blocker for the seat's own scope: all three assigned statements are observable, stable, in-timeout
   and agree with the L1's at-freeze receipt.
