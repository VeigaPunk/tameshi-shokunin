seat: T46ReobsB
item: independently re-observed the two C1 statements `mutation sweep runner` and `six-leg regression ledger` at the CONTENT revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` (one run each, scratch clone/mirror) and re-read their standing rows with the counter's own `last_rows`/`claim_of`; attacked the restated rows' What/First cells for overstatement.

# T46ReobsB — C1 re-observation (wave 2, falsify)

I did not write the standing rows nor any wave-1 observation. Read-only on the lane: the only lane file I
wrote is this report. Scratch: `/tmp/tameshi-r46-T46ReobsB/`. No git/jj mutation in the lane, the fleet repo
or a sibling lane (only `git clone`, `git checkout --detach`, `git show` inside `/tmp`). No tool installed or
upgraded; no pacman transaction attempted.

## Verdict in one line

Both statements **MATCH** at the CONTENT revision: `mutation sweep runner` claimed = observed =
`MUTATE_SELFTEST: 106/106 pass` | exit 0 | `a7d3f2dd7d47`, and `six-leg regression ledger` claimed = observed =
`REGRESSION: PASS (cases=9 passed=9` | exit 0. Zero mismatch, zero unparsed, zero unobservable from this seat.
Two calibration findings below are cell-level (LOW/INFO), not value-level.

## Setup (exact command and output)

```
W=/tmp/tameshi-r46-T46ReobsB; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
```

```
git -C $W/clone rev-parse HEAD                  -> 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git -C $W/fleet/tameshi-shokunin rev-parse HEAD -> 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
ls $W/fleet | wc -l                             -> 21 entries (20 sibling-lane symlinks + tameshi-shokunin)
statements.json sha256 at REV = a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9   (== counter STATEMENTS_SHA256 == contract statements_sha256)
SCORECARD.md sha256 at REV    = 9a1770c6666956ac2bd2df381d41399f4605a45894af161ff199e8c01da582de
append_only(base prefix of REV) = 1
```

## Method

`/tmp/tameshi-r46-T46ReobsB/run.py` imports the frozen counter by path
(`importlib` on `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/measure.py`)
and reuses its own `env()`, `pick_line()`, `last_rows()` and `claim_of()`. Per statement it runs the frozen
argv **once** with `REV=6f2168e028ce7ff6e82ac92093ac05dd1f147c32` in the counter's scrubbed env,
`{work}`→`$W`, `{clone}`→`$W/clone`, `{rev}`→the CONTENT rev; cwd `$W/clone` for `cwd:"clone"` and
`$W/fleet/tamesh-shokunin` for `cwd:"mirror"`. The standing claims were read from
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6f2168e0…:SCORECARD.md` (the CONTENT blob, not the
worktree), then `last_rows()` → `claim_of(stmt, rows[(kind,id)])`. Stdout/stderr kept at
`$W/obs-<id>.stdout` / `.stderr`; the result JSON at `$W/summary.json`.

Launch: `cd /tmp/tameshi-r46-T46ReobsB && python3 run.py` (367 s wall for both statements).

## Per-statement result

| id | claimed (from the CONTENT SCORECARD.md row) | observed | verdict |
|---|---|---|---|
| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass` \| `0` \| `a7d3f2dd7d47` | `MUTATE_SELFTEST: 106/106 pass` \| `0` \| `a7d3f2dd7d47` | **MATCH** |
| six-leg regression ledger | `REGRESSION: PASS (cases=9 passed=9` \| `0` | `REGRESSION: PASS (cases=9 passed=9` \| `0` | **MATCH** |

Both standing rows are the ones appended by wave 1 at `SCORECARD.md:2177` and `:2178` (raw lines, CONTENT blob):

```
2177: | mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof; `--regression` refuses a miscounted tally (round 30) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47` | historical round 3; re-demonstrated round 31 |
2178: | six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0 | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
```

`grep` over the whole CONTENT blob finds exactly three rows per id — `241`, `1515`, `2177` for
`mutation sweep runner` and `242`, `1516`, `2178` for `six-leg regression ledger` — so `last_rows()`
(last row in file order) selects 2177/2178 and nothing after them re-sets either key. Cells parsed: 4 each
(`cells=[id, what, evidence, first]`), so no unescaped-pipe split on these two rows.

### `mutation sweep runner`

```
argv=['bash', 'tools/mutate-and-run.sh', '--selftest']  cwd=/tmp/tameshi-r46-T46ReobsB/clone  timeout=1800
picked='MUTATE_SELFTEST: 106/106 pass'  exit=0  seconds=6.2  stdout_bytes=5446  stderr_bytes=0
obs_regex_matches=1
sha_file=tools/mutate-and-run.sh  sha12=a7d3f2dd7d47
git -C clone show HEAD:tools/mutate-and-run.sh | sha256sum | cut -c1-12   -> a7d3f2dd7d47
grep -c '^PASS ' obs-mutation-sweep-runner.stdout                        -> 106
grep -c '^FAIL ' obs-mutation-sweep-runner.stdout                        -> 0
tail: 'MUTATE_SELFTEST: 106/106 pass' / 'VERDICT: PASS'
```

The stated count is the count of case lines: 106 `PASS` lines, 0 `FAIL`, and the summary states 106/106. The
12-hex tool prefix in the row equals both the counter's `git show HEAD:<file>` form and the plain
`sha256sum | cut -c1-12` form the item asks for, and it equals the prefix of the full 64-hex digest the
regression run itself prints (`REGRESSION_TOOL: … sha256=a7d3f2dd7d47511a…`).

### `six-leg regression ledger`

```
argv=['bash', 'tools/mutate-and-run.sh', '--regression', '--workdir', '/tmp/tameshi-r46-T46ReobsB/regression-wd']
cwd=/tmp/tameshi-r46-T46ReobsB/fleet/tameshi-shokunin  timeout=2700
picked='REGRESSION: PASS (cases=9 passed=9'  exit=0  seconds=360.8  stdout_bytes=7033  stderr_bytes=0
obs_regex_matches=1  sha_file=None
grep -c '^REGRESSION_CASE ' obs-six-leg-regression-ledger.stdout        -> 9
grep -c '^REGRESSION_CASE .*: PASS' …                                   -> 9
grep -cE '^REGRESSION_TABLE .*match=[0-9]+/[0-9]+ .*flips=0' …          -> 9
tail -1: 'REGRESSION_WORKDIR: /tmp/tameshi-r46-T46ReobsB/regression-wd (kept)'
```

Full printed line (output line 50):
`REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`.
Nine legs, every one `match=N/N … flips=0`, recorded defects 10+10+10+10+15+10+10+10+10 = 95, every leg
carrying a `REGRESSION_PIN … source=git repo=<sibling lane> rev=<40 hex> path=… mode=1006xx sha256=<64 hex>`:

```
js-kimi-census 8/10 · bash-surface-census 8/10 · bash-tsukuroi-census 6/10 · bash-mado-verify 4/10 ·
bash-checklist-run 7/15 · js-claims-check 7/10 · js-round-gate 5/10 · js-sources-check 5/10 · js-cite-check 5/10
```
`REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact)`.
`REGRESSION_DATE: 2026-10-25T22:22:48Z`. Both clones were clean and still at the CONTENT rev after the run
(`git status --porcelain` → 0 lines each; `rev-parse HEAD` → `6f2168e0…` each).

## Findings

**F1 — LOW — the `six-leg regression ledger` standing row quotes a truncated line, so its own evidence cannot
show the exactness its What cell claims.** Attacks `SCORECARD.md:2178` (What: "… at its pinned blob; exact
expectation"; evidence: `` `REGRESSION: PASS (cases=9 passed=9`, exit 0 ``). The frozen `obs` regex
`^(REGRESSION: \w+ \(cases=\d+ passed=\d+)` stops at `passed=9`, so the row necessarily quotes a fragment with
an unbalanced parenthesis and drops `; ledger legs exact: killed-delta<=0 flips<=0` — the very clause that
evidences "exact expectation". Reproduced: `python3 /tmp/tameshi-r46-T46ReobsB/run.py` → picked
`'REGRESSION: PASS (cases=9 passed=9'`; the full line 50 carries the band clause. Not an overstatement (the
What is corroborated by the full output, and by the nine `REGRESSION_TABLE … flips=0` lines), but a reader of
the row sees a truncated sentence and no exactness band. Severity LOW; no counter-visible effect (MATCH).

**F2 — LOW — the `mutation sweep runner` First cell dropped the evidence pointer the historical row carried.**
Attacks `SCORECARD.md:2177` cell 4, `historical round 3; re-demonstrated round 31`. The row it supersedes
(`SCORECARD.md:241`) states `historical round 3 (\`SCORECARD.md:16\`); re-demonstrated fleet round 1` — the
restatement keeps the "historical round 3" claim but loses its in-repo pointer and adds "re-demonstrated round
31" with no pointer. The frozen command cannot prove either provenance clause (it prints a selftest tally).
Severity LOW: provenance, not capability; the counter ignores cell 4, so no MATCH effect.

**F3 — INFO — the `six-leg regression ledger` First cell understates the recorded leg history.** Attacks
`SCORECARD.md:2178` cell 4, `historical round 7 (four legs) / round 10 (six) / round 26 (nine)`. The tool's own
ledger comment (`tools/mutate-and-run.sh:85`, CONTENT blob) reads
`# --regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine)` — r16 (seven) and r18
(eight) are omitted from the cell. Understatement, not overstatement; no counter effect.

**F4 — INFO — the `mutation sweep runner` What cell's second clause is proven only inside the aggregate
count.** Attacks `SCORECARD.md:2177` What: "… ; `--regression` refuses a miscounted tally (round 30)". The
quoted evidence is the aggregate `MUTATE_SELFTEST: 106/106 pass`, which cannot locate that clause; the clause
is nonetheless demonstrated by a named case in the same run —
`PASS tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2` — and by the sweep cases
`PASS sweep exits 0` / `PASS control green on pristine` / `PASS restore line OK` /
`PASS fixture target byte-identical after sweep`. I checked the implementations are real sweeps, not textual
assertions: `tools/mutate-and-run.sh:1578-1588` invokes `bash "$SELF" --target "$fx/target.sh" --defects … --suite
…`, hashes the fixture before and after, and compares (`[[ "$s_before" == "$s_after" ]]`). So the What cell
does **not** overstate what the command proves; only its single quoted line is coarser than the What.

**F5 — INFO — difference from wave 1: verdict flip, observation unchanged.** Attacking nothing (reporting the
required comparison with `.ufo/waves/round-46/w1/ExecStmt02.md`, which observed these two statements at the
freeze rev `745a5831…`). Wave 1 recorded `mutation sweep runner` **UNPARSED** (cell had the value and exit but
no `, tool sha256 \`12hex\``) and `six-leg regression ledger` **MISMATCH** (cell carried a literal `…` inside the
backticks); at the CONTENT revision both are **MATCH**. The observed tuples are identical to wave 1's, value for
value: `MUTATE_SELFTEST: 106/106 pass` | 0 | `a7d3f2dd7d47`, and `REGRESSION: PASS (cases=9 passed=9` | 0, with
the same nine leg tallies (`8/10 8/10 6/10 4/10 7/15 7/10 5/10 5/10 5/10`). The only other difference is wall
time (F6).

**F6 — INFO — the regression statement ran 2.1–2.3× slower than in wave 1, still far inside its timeout.**
`seconds=360.8` here vs `155.2 / 175.6` in `w1/ExecStmt02.md`, against `timeout=2700` (7.5× headroom). The run
overlapped a large wave-2 fleet and the nine legs read live sibling lanes through `$W/fleet/*-shokunin`
symlinks; the picked line, exit and all nine leg tallies were unaffected. Not a row defect; a load note for the
deciding run (a deciding run under heavier load still has ~7× margin).

## Not run (out of seat scope)

- `measure.py` in any mode — not `--selftest`, not the deciding run (`--lane … --rev … --base … --work …`),
  not `--emit`: the deciding run is the L1's. I ran only the two frozen statement argvs, once each, and the
  counter's parsing helpers.
- The other 20 statements (other seats' items), the C2/C3 counters, `no-harm.sh`, and any build/lint gate.
- A second run of each statement: the item asks for one run per statement, and run-to-run stability of these
  two was already measured at the freeze by wave 1 (`w1/ExecStmt02.md`: both runs of each identical on the
  picked line, `REGRESSION_DATE` the only differing line in the regression output).

## Retained evidence

`/tmp/tameshi-r46-T46ReobsB/`: `run.py` (runner), `summary.json`, `obs-mutation-sweep-runner.stdout` (5446 B),
`obs-six-leg-regression-ledger.stdout` (7033 B), the two empty `.stderr` files, `regression-wd/` (nine leg
workdirs, kept by the tool), `clone/` and `fleet/tameshi-shokunin` (both detached at `6f2168e0…`, clean),
`fleet/` (20 sibling-lane symlinks + the lane mirror).

## Risks / blockers

- None blocking. Both statements are observable at the CONTENT revision, exit 0, print exactly one matching
  line, and their standing rows parse to exactly the observed tuple.
- Residual risk for the deciding run: F6 (load-dependent regression wall time) and F1 (the regression row's
  truncated evidence cell is a permanent readability defect of the frozen grammar, not fixable without
  changing the statement).
