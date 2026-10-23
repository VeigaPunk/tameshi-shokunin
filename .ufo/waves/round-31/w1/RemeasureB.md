# RemeasureB — independent re-measurement of four C1 statements at base

Round 31 (Tameshi round), wave 1, seat RemeasureB. Scope: four of the twelve frozen C1
statements, re-measured at base `36c1d3933f680125aeefc447f07db0f03004901a` without invoking
the C1 counter. Judged on calibration.

## Verdict

- All four observed tuples in the frozen base receipt
  `.ufo/evidence/round-31/before/c1-at-base.stdout` are reproduced exactly by an independent
  run in a fresh clone at base. Every command exited 0.
- Two of the four base mismatches are genuine row-versus-tool drift, not a counter parsing
  artifact: `six-leg content-disposition probe` (row states 18/18, tool prints 19/19) and
  `effective expectation reconciliation` (row states 34/34, tool prints 66/66).
- Two of the four base matches are genuine: `repeated pristine-control gate` (29 cases,
  exit 0) and `exposed witness provenance correction` (39/39, exit 0).
- No UNPARSED or UNOBSERVABLE condition was seen for these four statements; each summary
  line matches the frozen observed regex at its first anchored match.

## Method

Fleet mirror and clone, exactly as assigned, under
`/fast/scratch/hyaku/tameshi-r31-seats/RemeasureB/`:

```
mkdir -p .../RemeasureB/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d);
  [ $b = tameshi-shokunin ] || ln -sfn $d .../RemeasureB/fleet/$b; done
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  .../RemeasureB/fleet/tameshi-shokunin
git -C .../RemeasureB/fleet/tameshi-shokunin checkout -q --detach 36c1d39
```

`git rev-parse HEAD` printed `36c1d3933f680125aeefc447f07db0f03004901a`. Commands were run
with cwd = the clone (the same working directory the counter uses for `clone`-cwd
statements), environment stripped of every `GIT_*` variable and with
`PYTHONDONTWRITEBYTECODE=1` (the counter's `env()`), each under `timeout 900`:

```
timeout 900 python3 tools/repeat-control.py --selftest
timeout 900 python3 tools/pin-disposition.py --selftest
timeout 900 python3 tools/witness-metadata.py --selftest
timeout 900 python3 tools/evidence-disposition.py --selftest
```

The counter file `.ufo/evidence/round-31/c1-measure.py` was never executed. It was read only
after the measurements to map each statement id to its frozen command; that mapping was
independently confirmed against the base SCORECARD rows quoted below. Row extraction was also
done independently: each of the four ids occurs exactly once in the base SCORECARD (fence-aware
scan; no occurrence inside a fenced block or HTML comment), all four in the single
`| Capability |` table whose header sits at `SCORECARD.md:238` at base:

```
243:| repeated pristine-control gate | ...
244:| six-leg content-disposition probe | ...
245:| exposed witness provenance correction | ...
246:| effective expectation reconciliation | ...
```

Tool file hashes at base (sha256):

```
296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25  tools/repeat-control.py
331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c  tools/pin-disposition.py
df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4  tools/witness-metadata.py
39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8  tools/evidence-disposition.py
```

## Table (statement, summary line, exit, counter observed, equal?)

Counter observed values are quoted from `.ufo/evidence/round-31/before/c1-at-base.stdout`.
"Equal?" compares my observed tuple with the counter's observed tuple. "Row agrees?" compares
the base SCORECARD row with my observed tuple (that is the C1 mismatch property itself).

| # | Statement | Base SCORECARD row (line) | Observed summary line (scratch file:line) | Exit | Counter observed | Equal? | Row agrees? |
|---|---|---|---|---|---|---|---|
| 1 | repeated pristine-control gate | `SCORECARD.md:243`: `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 | `SELFTEST: PASS (29 cases)` (`repeat-control.out:30`) | 0 | PASS,29,0 | yes | yes |
| 2 | six-leg content-disposition probe | `SCORECARD.md:244`: `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0 | `SELFTEST: PASS (19/19)` (`pin-disposition.out:20`) | 0 | 19,19,0 | yes | no (19,19,0 ≠ 18,18,0) |
| 3 | exposed witness provenance correction | `SCORECARD.md:245`: metadata selftest39/39 PASS0 | `SELFTEST: PASS 39/39` (`witness-metadata.out:40`) | 0 | 39,39,0 | yes | yes |
| 4 | effective expectation reconciliation | `SCORECARD.md:246`: `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0 | `SELFTEST: PASS (66/66)` (`evidence-disposition.out:67`) | 0 | 66,66,0 | yes | no (66,66,0 ≠ 34,34,0) |

Case counts confirm the summary numerators: 29 `SELFTEST_CASE` lines in `repeat-control.out`,
19 in `pin-disposition.out`, 39 in `witness-metadata.out` (these print `... OK` rather than the
word PASS), 66 in `evidence-disposition.out`. Every case line records a passing outcome.

## Determinism

Three passes: two concurrent (all four tools started together) and one serial pass in the same
clone. Per tool, the three summary lines are identical:

```
repeat-control.out:30 / repeat-control.run2.out:30 / repeat-control.serial.out:30:
  SELFTEST: PASS (29 cases)
pin-disposition.out:20 / pin-disposition.run2.out:20 / pin-disposition.serial.out:20:
  SELFTEST: PASS (19/19)
witness-metadata.out:40 / witness-metadata.run2.out:40 / witness-metadata.serial.out:40:
  SELFTEST: PASS 39/39
evidence-disposition.out:67 / evidence-disposition.run2.out:67 / evidence-disposition.serial.out:67:
  SELFTEST: PASS (66/66)
```

`cmp` between pass 1 and pass 2 stdout is identical (`same=yes`) for all four tools. Run-1
stdout sha256: `09f43270…` (repeat-control), `1f39911c…` (pin-disposition), `c4f37160…`
(witness-metadata), `cf74b01b…` (evidence-disposition). Python 3.14.8. Clone worktree stayed
clean (`git status --porcelain` = 0 lines) after every pass, so the selftests wrote no tracked
state.

## Drift provenance (bounded probe, not a claim about the fix)

A second clone under my scratch (`fleet-hist`, same sibling-symlink layout) was detached at the
two commits that touched these tools after their capability rows landed, and the two tools were
run there under the same environment:

| Rev | pin-disposition | evidence-disposition | Row text at that rev |
|---|---|---|---|
| `4acc607` (round 13) | `SELFTEST: PASS (18/18)` | file `tools/evidence-disposition.py` absent (exit 2, `No such file`) | pin row: 18/18; no evidence-disposition row |
| `2a22ade` (round 17) | `SELFTEST: PASS (19/19)` | `SELFTEST: PASS (56/56)` | both rows unchanged: 18/18 and 34/34 |
| `370f2df` (round 21) | `SELFTEST: PASS (19/19)` | `SELFTEST: PASS (66/66)` | both rows unchanged: 18/18 and 34/34 |
| `36c1d39` (base) | `SELFTEST: PASS (19/19)` | `SELFTEST: PASS (66/66)` | 18/18 and 34/34 |

So both standing rows were already stale at round 17: the pin row matched at round 13 and
diverged by `2a22ade`; the evidence row states a round-14 value while the tool already printed
56/56 at round 17. The exact commit that added case 19 (pin) and cases 35–56 (evidence) was not
bisected; the evidenced interval for pin is `(4acc607, 2a22ade]`.

## Smallest safe correction (record only; not applied by this seat)

The frozen predicate requires the base SCORECARD to be a byte prefix of the revision's
SCORECARD, so neither stale row can be edited in place. The minimal move that satisfies both
the append-only property and the last-row-of-its-table-type rule is to append a restated
`| Capability |` table after the current last table (line 246), outside any code fence or HTML
comment, keeping each id string exact and each row in the claim syntax the frozen patterns read.
For this seat's two rows the corrected values are:

- `| six-leg content-disposition probe | … `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 … |`
- `| effective expectation reconciliation | … `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 … |`

The other eight capability ids must be restated in that appended table only with independently
measured values (do not copy the old claims); three further capability statements
(sources-registry, mutation sweep runner, six-leg regression ledger) and the two axis rows are
outside this seat and remain with their owning seats. The appended table becomes the last row
source for every capability id it restates; ids it omits keep their earlier row. Because all
four tools print deterministically at base, re-running the four commands after the append should
reproduce the same observed tuples above.

## Risks and limits

- Four of twelve statements measured; the remaining eight were not run by this seat.
- The counter was not invoked, so equality is with the frozen receipt text, not a re-derivation
  of the counter's own claimed-row extraction. Claimed values were instead read directly from
  the unique base rows at lines 243–246 and parsed with the documented claim syntax.
- `pin-disposition`'s selftest builds fixture repositories; its summary is self-contained, and
  the same 19/19 appeared in two distinct clones at two revisions, so no evident dependence on
  sibling lanes affects the count. No sibling repo was written.
- The exact introducing commit for each stale value was bounded, not bisected to a single
  revision.
- No tool was installed or upgraded; no model, scoring, or promotion claim is made here.

## Evidence index (scratch, ephemeral)

`/fast/scratch/hyaku/tameshi-r31-seats/RemeasureB/`: `repeat-control.out`, `pin-disposition.out`,
`witness-metadata.out`, `evidence-disposition.out` (pass 1), `*.run2.out` (pass 2),
`*.serial.out` (serial pass), `hist-<rev>-<tool>.out` (provenance probes), and
`SCORECARD.at-base.md` (sha256 `518286e0…`, the base SCORECARD read via `git show`). Clones:
`fleet/tameshi-shokunin` at base, `fleet-hist/fleet/tameshi-shokunin` at the probed revisions.
No process was left running; every command ran under a timeout.
