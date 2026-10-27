# T51W2ExecTool15 — C3 registry row audit: `tools/repeat-control.py`

Seat scope: independently audit the C3 registry row for `tools/repeat-control.py` at candidate
`6d8c11e378aa90b12650808e1b79270742935f15`, read-only on the lane. No source, row, or fixture was written
outside `$S=/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool15` (two `git clone --shared` fixtures, both at CAND,
`rev-parse --show-toplevel` asserted on each) and this report's directory. No git/jj mutation in the lane, fleet
or a sibling repo; the only commits would have been inside the clones and none were needed. No tool installed.

## Verdict

The row is **operable and truthful on every field the item asks me to check**, with two *meaning* gaps in the
Verdict-map cell (exit codes are all declared; two of their annotations are narrower than the tool) and one
stale **adjacent** row in the same file. No falsifying mismatch was found: kind, entry command, pinned values,
write scope and the self-test all reproduce. The known C3 blocker (the `tools/round21-measure.py` clone-context
failure, "row16") **does not apply to this row** — this tool is table row 15 and its self-test is green from two
independent fresh clones and from `cwd=/`.

Row identity: `SKILL.md:2156`, the 15th of 30 data rows under `#### Gate/probe registry — round 51`
(`SKILL.md:2138`, four hashes, so it is not a cold-read section boundary). Eight cells parse exactly as the
counter requires (`skill-row-2156.txt`).

## 1. Required runs

Clone: `git clone -q --shared LANE $S/cand && git -C $S/cand checkout -q --detach 6d8c11e3…`;
`rev-parse --show-toplevel` → `/fast/scratch/…/T51W2ExecTool15/cand`; `git status --porcelain` empty before and
after every run. The receipt line `tool-sha256=296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`
equals the sha256 of `git show CAND:tools/repeat-control.py`, so the clone ran the candidate bytes.

| run | exact command (cwd = clone, `TMPDIR=$S/tmp`, stdin `/dev/null`) | exit | last stdout line | wall |
|---|---|---|---|---|
| row self-test (verbatim backticks) | `python3 tools/repeat-control.py --selftest` | **0** | `SELFTEST: PASS (29 cases)` | 776 / 975 / 1107 ms (three timed runs, three fresh clones) |
| usage probe | `python3 tools/repeat-control.py --r51-no-such-flag` | **64** | `REPEAT_CONTROL: invalid_usage` | 30 ms |

Self-test stdout is 30 lines: 29 `SELFTEST_CASE … PASS (…)` + the tally; stderr empty. Byte-identical stdout
(sha256 `09f432706cf05e43c27bfa9c964d254225076ee71d87b113d1f51499b941916c`) in clone #1, in a **second**
`--shared` clone, and when run from `cwd=/` with an absolute path — deterministic and cwd-independent.
`SELFTEST: PASS (29 cases)` is the row's claim, and the 29 cases are really 29 `cli_case`/`snapshot_case`
invocations (`tools/repeat-control.py:698-850`); no case is unreachable.

The usage probe's 64 is a declared code: `invalid_usage` → `EXIT_BY_ID` (`tools/repeat-control.py:122-131`,
`194-197`), reached from `run_mode`'s "unexpected argument before `--`" branch (`:226-265`), with the
offending flag named on stderr.

## 2. Field-by-field audit

| Field | Row says | Observation at CAND | Verdict |
|---|---|---|---|
| Name | `repeated control agreement` | matches the gate's question (do N pristine controls agree) | ok |
| Kind | `gate` | returns 1 on disagreement (flaky command → `controls_mismatch`/1) and 0 on agreement; not a report-only probe | ok |
| Entry command | `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`, or `--snapshot DIR` | both forms executed: `--runs 3 --out … -- true` → 0 `controls_match`; `--snapshot <committed>` → 0 `controls_match`; `--snapshot <committed>/mismatch` → 1 `controls_mismatch` | ok |
| Verdict map | 0 clean; 1 failed; 2 (4 named causes); 64 invalid_usage | all 16 probes in `verdict-probes.txt` land on a declared code; each exit-2 cause reproduced independently: `baseline_nonzero` (child exit 7, **and** uniform signal death `-15`), `command_unavailable` (ENOENT), `snapshot_tampered` (one byte appended to `run-2.stdout`), `setup_error` (`--out /proc/…` unwritable, `:315-319`). Gaps → F1, F2 | ok on codes; two meaning gaps |
| Self-test cell | one backticked command → `SELFTEST: PASS (29 cases)` at exit 0 | one backticked command; argv is `python3 tools/repeat-control.py --selftest`; last line observed exactly as claimed; `SELFTEST:` is the first token of that line, so the counter's marker rule reads it | ok |
| Pinned values | `.ufo/evidence/round-12/ControlGate/expected.json`, `…/mismatch/expected.json` | both exist at CAND; both **load-bearing** (§3): corrupting one byte of a pinned observation flips `snapshot-committed-stable` to FAIL/exit 1; restoring restores PASS. The pins are also structural — the selftest's root is `dirname²(SELF)/.ufo/evidence/round-12/ControlGate` (`:112-121`, `:593`), so a copied tool outside the lane exits 2 `SELFTEST: COULD_NOT_EVALUATE` | ok |
| Write scope | `--out` created fresh, never deleted; `--snapshot` read-only; selftest scratch under `/tmp/tameshi-r12-repeat-control-selftest.*` removed on pass | strace: run mode's only writes are `mkdir --out` + 11 `O_WRONLY|O_CREAT|O_EXCL` files all inside `--out` (`run-mode-writes.txt`); `--out` still exists after the verdict; snapshot mode issues **zero** create/write syscalls (`snapshot-mode-writes.txt`, 0 lines); scratch path is hardcoded `tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir="/tmp")` (`:597`) so `TMPDIR` is ignored, removed on pass (`:859`) and kept on failure (`SELFTEST_SCRATCH …`, three 900 KB dirs observed, mine, deleted) | ok (accurate, including the failure case) |
| Owner | `tameshi` | lane is `tameshi-shokunin` | ok |

Machine acceptance of the row by the frozen predicate was checked with the counter's own function, not by
re-reading prose: importing `.ufo/evidence/round-51/c3/measure.py` and calling `registry_rows` + `row_reason`
on `SKILL.md:2156` returns `reason=None`, `selftest argv = ['python3','tools/repeat-control.py','--selftest']`,
`usage argv = ['python3','tools/repeat-control.py','--r51-no-such-flag']`. So the row is not merely plausible —
it is the row shape the counter will execute, and both its argv were then run by hand above.

## 3. Falsification controls (the self-test is a gate, not a smoke test)

Two mutants in a **fixture** clone (`$S/pinprobe`, toplevel asserted), each restored with `git checkout --` and
`git status --porcelain` empty afterwards; the `cand` clone stayed pristine throughout.

| mutant | expected casualty | observed |
|---|---|---|
| M1: compare stdout/stderr with `.rstrip(b"\n")` inside `classify` (`:206-221`) | `mismatch-newline-only` | `SELFTEST_CASE mismatch-newline-only FAIL (expected=controls_mismatch/1 observed=controls_match/0)`, exit 1 |
| M2: decide `baseline_nonzero` before the mismatch loop (`:206-221`) | `mismatch-nonzero-exits` | `SELFTEST_CASE mismatch-nonzero-exits FAIL (expected=controls_mismatch/1 observed=baseline_nonzero/2)`, exit 1 |

Each mutant is killed by the case that names the property it broke, so the row's "29 cases" self-test really
grades this tool's verdict logic. Independent of their fixtures, the gate fails when it should: a command that
prints a nanosecond timestamp three times → `controls_mismatch`/1; uniform `exit 7` → `baseline_nonzero`/2.

## 4. Findings

**F1 (minor, operability; Verdict-map cell).** `0` is annotated only as `clean (controls_match)`, but
`dispatch` returns 0 for `-h`/`--help` after printing the three usage lines (`:882-886`). Measured: exit 0, and
the last stdout line is `       repeat-control.py --selftest` — **no `REPEAT_CONTROL:` finding at all**
(`help-probe.out`). A wrapper that keys on exit status (the row tells it 0 is clean) reads help as a clean
control; a wrapper that keys on the finding id gets nothing. The tool's own docstring has the same blind spot:
it lists three interfaces and never mentions `-h/--help`. Not code-undeclared, so C3's predicate is unaffected.

**F2 (minor; Verdict-map cell).** The map is a *run/snapshot-mode* verdict map. In `--selftest` mode the same
codes mean pass / fail / could-not-evaluate (`:854-864`): measured `SELFTEST: FAIL (1 of 29 cases failed: …)`
at exit 1 and `SELFTEST: COULD_NOT_EVALUATE (…)` at exit 2. So exit 2 has a fifth cause, and exit 1 a second
one, that the cell does not name — while neighbouring rows in the same table do say it (e.g.
`SKILL.md:2160` tally-audit-v2 "1 failed (audit FAIL **or a selftest case failure**)", `:2161`). The row's own
Self-test column states "at exit 0", so the passing direction is unambiguous; the failing meanings are not.
Codes are declared, so PROTOCOL §Gate standard's code rule and the frozen predicate still hold.

**F3 (adjacent row, not mine; disclosed by wave 1).** `SKILL.md:1503` still carries the round-12 row for the
same tool, and it **fails** the round-51 predicate: its second backticked pin is the bare fragment
`mismatch/expected.json`, which the counter reads repo-relative →
`pinned-path-missing:mismatch/expected.json`, reproduced here with the counter's own `row_reason`. The effect is
not a C3 failure (the round-51 row covers the tool) but the registry home now holds two rows for one tool with
different precision, one of them wrong; a reader who stops at the round-12 section gets the broken pin. Not
repaired: out of scope for this seat.

**F4 (caveat, not a mismatch).** The selftest's scratch is hardcoded to `/tmp` (`:597`), so the counter's
`TMPDIR=WORK/tmp` isolation does not sandbox this row's 29 cases: every graded run writes ~900 KB into the host
`/tmp` and removes it on pass, and **keeps** it on any case failure (`SELFTEST_SCRATCH`). The row states this
truthfully (that is why I rate it a caveat); it matters only under a hardened `/tmp` or when a run fails.

**F5 (negative result the brief asked for).** This is **not** row16: `tools-base.json` index 14 is
`tools/repeat-control.py` (table row 15), index 15 / row 16 is `tools/round21-measure.py`, the known
clone-context blocker. This row's self-test needs only `bash`, `cat`, the stdlib and the lane tree at CAND, and
exited 0 in two independent fresh `--shared` clones.

## 5. Residual risk / what I did not see

- I audited this row, not the deciding run: I did not execute the full C3 counter over all 30 tools (L1's job).
  The counter's row predicate returned `reason=None` for this row and I ran both argv by hand; whether the other
  29 rows cover their tools is outside this seat.
- I did not test a *hanging* gate command (the tool documents no timeout/supervisor); that limitation is
  disclosed in its docstring and is irrelevant to the row's own 1 s self-test, but it does mean a row consumer
  can block, and the counter's 900 s limit is the only backstop.
- Interrupt-derived exits (130 on SIGINT, `KeyboardInterrupt` is not caught by `main`'s `except Exception`,
  `:890-893`) are undeclared by every row in the table, not just this one; I did not count that as a row defect.
- I could not judge whether a *duplicate* row (F3) is acceptable to the round's integration; only that the
  round-51 row itself is conformant and executable.

## 6. Receipts (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-51/w2/T51W2ExecTool15/`)

`skill-row-2156.txt` (heading, header, row, 8 parsed cells) · `verdict-probes.txt` (16 probes: tool sha256, rev,
rc, last line, wall) · `selftest-row-command.out` / `.err` (the required run) · `selftest-rerun.out` ·
`selftest-fresh-clone2.out` · `selftest-cwd-root.out` (same stdout sha in three contexts) · `usage-probe.out` /
`.err` · `help-probe.out` (F1) · `noargs-probe.out` · `selftest-pinned-snapshot-corrupted.out` (pin is
load-bearing) · `selftest-mut-M1-newline.out`, `selftest-mut-M2-precedence.out` (§3) ·
`strace-run-all-syscalls.txt`, `run-mode-writes.txt`, `strace-snapshot-all-syscalls.txt`,
`snapshot-mode-writes.txt` (write scope).

Reproduce (scratch clone; no lane write):

```
S=$(mktemp -d -p /fast/scratch/hyaku/tameshi-r51)
git clone -q --shared LANE $S/c2 && git -C $S/c2 checkout -q --detach 6d8c11e378aa90b12650808e1b79270742935f15
cd $S/c2 && TMPDIR=$S/tmp python3 tools/repeat-control.py --selftest </dev/null; echo rc=$?
TMPDIR=$S/tmp python3 tools/repeat-control.py --r51-no-such-flag </dev/null; echo rc=$?
```

## 7. Scratch

`$S` (two clones, probe `--out` dirs, receipts source) is deleted before yield; the three
`/tmp/tameshi-r12-repeat-control-selftest.*` dirs my failure-path runs kept (900 KB each) were deleted after
attributing them via their `SELFTEST_SCRATCH` lines; no other `/tmp` residue from this seat.

## Summary

`skills` row at `SKILL.md:2156` (`tools/repeat-control.py`, gate, table row 15/30) passes the frozen C3 row
predicate (`row_reason → None`) and its declared behaviour reproduces: self-test exit 0 with last line
`SELFTEST: PASS (29 cases)` in 0.78–1.11 s, byte-identical across two fresh `--shared` clones at CAND and from
`cwd=/`; usage probe exit 64 `REPEAT_CONTROL: invalid_usage`. Every Verdict-map code is reachable and matched by
an independent probe (0/1/2×4/64); pinned snapshots are genuinely load-bearing (one-byte corruption → FAIL/1)
and the self-test kills two mutants of the tool's own verdict logic. No falsifying mismatch on kind, entry,
pins, write scope or marker. Two minor meaning gaps in the Verdict-map cell: `0` also means `--help` with no
finding id (F1), and selftest mode uses 0/1/2 with pass/fail/could-not-evaluate meanings the cell does not name
(F2). Adjacent defect: the older row at `SKILL.md:1503` for the same tool remains and fails the predicate
(`pinned-path-missing:mismatch/expected.json`), leaving two rows of different precision (F3). This is not
row16's clone-context blocker. No lane, fleet or sibling file was written; C3's predicate may still fail
elsewhere (the `round21-measure.py` row), but not on this row.
