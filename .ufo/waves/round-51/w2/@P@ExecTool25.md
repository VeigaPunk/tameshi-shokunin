# T51W2ExecTool25 — falsify the C3 registry row for `tools/wave-route-mix.py`

Seat: `T51W2ExecTool25` (executor, leaf). Axes: operability. Milestone: C3 row falsification.
Candidate: `6d8c11e378aa90b12650808e1b79270742935f15`. Base: `9962033fd7a75aa2f2847e979dd687a5d28505a1`.
Row under audit: `SKILL.md:2166` (candidate), the `wave-route-mix` row of
`#### Gate/probe registry — round 51` (section opens `SKILL.md:2138`).

Raw receipts: `./@P@ExecTool25/` (row text, tool bytes at candidate, counter stdout, selftest/usage
receipts and exits, timings, behaviour matrix, mutation receipts, write-scope receipt). A copy of the
receipt directory sits at `./T51W2ExecTool25/`.

## Verdict

**No predicate falsifier for the C3 claim from this row.** The row satisfies every clause of the
frozen C3 predicate as applied to it, the self-test is real, hermetic and reproducible from a fresh
`git clone --shared` at CAND, and the frozen counter covers the row.

**Four row-fidelity defects were found (M1–M4).** None is visible to the frozen predicate; two of
them are the class wave 2 exists to find — a verdict map that does not name every path that can
produce its exit code (M1) and a pinned-values cell that lost a real pin the base row recorded (M2).
M3 and M4 are measurement-strength observations about this row's claim and the counter's check of it.

The known C3 blocker (the truthful `tools/round21-measure.py --selftest` exiting 1 from the
counter's fresh clone) is **not** this row's tool: `wave-route-mix`'s selftest is hermetic — it
builds its config from an inline literal and reads no repo, fleet or home file — so it exits 0 from
the clone (M5, below, is about its pinned-value disclosure, not about the clone-context failure).

## What was run

Clone and environment (lane read-only; no git/jj mutation in the lane, fleet or sibling repos):

```
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r51/T51W2ExecTool25/work/tameshi-shokunin
git -C .../tameshi-shokunin checkout -q --detach 6d8c11e378aa90b12650808e1b79270742935f15
# rev-parse --show-toplevel printed the clone dir (asserted before any write in the clone)
TMPDIR=<scratch>/work/tmp   stdin=/dev/null   cwd=clone root
```

Row's exact backticked self-test and the usage probe, as the counter runs them:

```
python3 tools/wave-route-mix.py --selftest            exit 0   wall 37 ms
   stdout last line: ROUTEMIX_SELFTEST: 8/8 pass     stderr: (empty)
python3 tools/wave-route-mix.py --r51-no-such-flag    exit 64  wall 36 ms
   stdout: (empty)   stderr last line: wave-route-mix.py: error: unrecognized arguments: --r51-no-such-flag
```

`python3 -I tools/wave-route-mix.py --selftest` (isolate mode) → exit 0, same last line; the same
command from a foreign cwd with an absolute path → exit 0, same last line. The selftest reads stdin
never (291 stdout bytes with `stdin=PIPE` closed) and writes no file: a pristine `TMPDIR` is empty
after both a selftest and an entry run, and `git status --porcelain` in the clone is empty after all
probes (`@P@ExecTool25/write-scope.txt`).

### Frozen counter, full run at CAND

`python3 .ufo/evidence/round-51/c3/measure.py --lane . --rev 6d8c11e… --work <empty scratch dir> --explain`
(658 s, exit 1 — the exit 1 is the known round21-measure row, not this one):

```
C3_TOOL tools/wave-route-mix.py: covered line 2166 selftest exit=0 last=ROUTEMIX_SELFTEST: 8/8 pass
C3_R51: rev=6d8c11e378aa90b12650808e1b79270742935f15 tools=30 rows=32 covered=29 missing=1 deleted=0
        selftest_fail_rows=2 total=1 C3_R51_PASS=false
C3_TOOL tools/round21-measure.py: MISSING (line 2157 selftest-exit=1 last=)
```

Full stdout: `@P@ExecTool25/c3-counter-explain.stdout`. This row is **covered**; `missing=1` is the
round-21-measure row, which the contract already discloses.

Applying the counter's own `row_reason` and `run_row` to the candidate row gives
`row_reason -> None` and `run_row verdict: PASS` (`@P@ExecTool25/mutation-counter-row.txt`).

## Row fields against the source

Row text (`SKILL.md:2166`, in `@P@ExecTool25/row-2166.txt`):

> | wave-route-mix | gate | `python3 tools/wave-route-mix.py --spec SPEC.json --config CONFIG.yml --max-share 0.40` | 0 clean (no provider above the bound, every role routed, at least one seat); 1 failed (a provider above --max-share, an unrouted role, or an empty seat list); 2 could-not-evaluate (unreadable spec or config); 64 could-not-evaluate (usage: unknown flag, missing --spec, --max-share outside (0,1]) | `python3 tools/wave-route-mix.py --selftest` → ROUTEMIX_SELFTEST: 8/8 pass | none — the expected case verdicts are literals in the selftest; no repo file is read | nothing — read-only: JSON on stdout under --json plus one ROUTEMIX summary line on stderr; selftest writes no files | tameshi |

Tool bytes at candidate: `tools/wave-route-mix.py`, 128 lines, sha256
`1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` — **byte-identical to base**
(`git diff --stat base…cand -- tools/wave-route-mix.py` is empty; last commit touching it is
`33d03b7`, round 21). So every defect below is a defect of the *row*, not of the tool.

**Kind `gate` — correct.** PROTOCOL §Gate standard: "A tool that cannot fail is a probe." The tool
genuinely fails: a concentrated spec exits 1 (`ROUTEMIX: REFUSE … over=['prov-a']`), an unrouted
role exits 1, an empty seat list exits 1. `gate` is the honest label, not a probe.

**Verdict map semantics — checked against the source, all four codes reproduced** (`@P@ExecTool25/behaviour-matrix.txt`):

| Row claim | Source | Observed |
|---|---|---|
| 0 clean: no provider above the bound, every role routed, at least one seat | `tools/wave-route-mix.py:67-70` (`over` uses strict `>`, `ok = not over and not unrouted and n > 0`) | 3 providers × ≤40 % → exit 0, `ROUTEMIX: OK seats=10 max_share=0.4 prov-a=4/10 prov-b=3/10 prov-c=3/10` |
| 1 failed: provider above `--max-share` | `:67` strict `>` | 5/10 → exit 1, `over=['prov-a']` |
| 1 failed: unrouted role | `:62-64` | `unrouted=['ghost']` → exit 1 |
| 1 failed: empty seat list | `:70` `n > 0` | `{"items":[]}` → exit 1, `ROUTEMIX: REFUSE seats=0` |
| 2 could-not-evaluate: unreadable spec or config | `:109-114` (`OSError`, `ValueError`) | missing spec → 2; missing config → 2; non-JSON spec → 2 |
| 64 usage: unknown flag, missing `--spec`, `--max-share` outside (0,1] | `:100-108` | `--r51-no-such-flag` → 64; no `--spec` → 64; `--max-share 0` → 64; `--max-share 1.5` → 64; `--max-share nan` → 64; `--max-share abc` → 64 |

**Pinned values — the cell's "no repo file is read" is true of the self-test**, which builds its
config from an inline literal string (`tools/wave-route-mix.py:74`) and never opens a file. But see
M2: the base row pinned a value that materially affects expected behaviour and the candidate row
records "none".

**Write scope — accurate.** The tool opens no file for writing anywhere (grep for
`open(`/`write`/`mkstemp`/`mkdtemp`/`TemporaryDirectory` in the tool returns only the two
`Path(...).read_text()` reads at `:110-111`). Observed: `--json` → 17 stdout lines (the JSON object)
+ exactly 1 stderr line (`ROUTEMIX: …`); without `--json` → 0 stdout lines + exactly 1 stderr line.
Pristine-TMPDIR runs write nothing; the clone tree stays clean.

**Last-line marker — a real diagnostic, and the row quotes it exactly.** The last stdout line is
`ROUTEMIX_SELFTEST: 8/8 pass`, computed at `:89` as `len(cases)-len(bad)` / `len(cases)` over the
eight case literals at `:76-85` — not a hardcoded string and not help text. The counter's marker
rule (`measure.py:178-180`: first whitespace token of the last stdout line must appear in the row's
Self-test cell) is satisfied: the token `ROUTEMIX_SELFTEST:` is in the cell. The row's `8/8`
matches the observed `8/8` and the eight `ROUTEMIX_CASE … ok` lines.

## Findings

### M1 — the verdict map does not name every path that can produce exit 1 (material)

The row declares `1 failed (a provider above --max-share, an unrouted role, or an empty seat list)`.
The tool can also exit **1 with an unhandled Python exception**: `roles = [it.get("role") for it in
spec.get("items", [])]` (`tools/wave-route-mix.py:115`) is unguarded, so a spec that is valid JSON
but not an object, or whose `items` are not objects, raises `AttributeError` and the process dies
with an uncaught traceback and exit 1:

```
$ python3 tools/wave-route-mix.py --spec <json list> --config <cfg>
Traceback (most recent call last):
  … File "tools/wave-route-mix.py", line 115, in main
    roles = [it.get("role") for it in spec.get("items", [])]
AttributeError: 'list' object has no attribute 'get'
exit=1
```

So exit 1 conflates three *refusals* with one *internal error*. The lane's own convention in this
same table discloses it where it applies — the `frozen registry replay` row in the round-51 table
says "an uncaught traceback also exits 1". The `wave-route-mix` row does not, so a reader of this
row alone reads a crashed run as "the wave was refused for concentration". PROTOCOL §Gate standard
allows an undeclared *code* to read as could-not-evaluate; here the code (1) is declared, but its
declared *meaning* is incomplete. Evidence: `@P@ExecTool25/behaviour-matrix.txt`
(`baditems` exit 1, `notdict` exit 1 — both with tracebacks).

### M2 — the pinned-values cell records "none" for a value the base row pinned and the selftest does not assert (material)

The base row (`SKILL.md:1976`, quoted in `@P@ExecTool25/row-and-base.txt`) pinned
"max-share0.40 and literal synthetic expectations; round20 refused spec/round21 accepted spec
retained". The candidate row replaces that with "none — the expected case verdicts are literals in
the selftest; no repo file is read". Two consequences, both measured:

1. **`--max-share 0.40` is now unpinned and unasserted.** The selftest always calls `evaluate(...)`
   with an explicit `0.40`, so it never touches the argparse default at `:97`. Two mutants —
   `default=0.40 → 0.99` and `default=0.40 → 0.10` — both keep the self-test green
   (`ROUTEMIX_SELFTEST: 8/8 pass`, exit 0) while changing the tool's documented default. The base
   row's "max-share0.40" pin was the only place that value was recorded; the candidate row drops it.
2. **The gate's real verdict input is not pinned at all.** The entry verdict depends on the
   operator's live route table `~/.omp/agent/config.yml` (default `--config`, `:21`/`:96`) — a
   mutable artifact outside the repo. Replaying the lane's own committed round-21 spec
   (`.ufo/waves/round-21/spec1.json`) at CAND against today's live config gives
   `anthropic 12, kimi-code 4, minimax-code 20, opencode-go 19, zai 16`, while the retained receipt
   `.ufo/waves/round-21/routemix-spec1.json` records
   `anthropic 11, google-antigravity 1, openai-codex 28, xai-oauth 4, zai 27`. Both `ok: true`, but
   the frozen runs the base row cited ("round20 refused spec/round21 accepted spec retained") are
   not reproducible from committed inputs, and the candidate row no longer points at them.

The row's "no repo file is read" is true and is a genuine strength of the self-test; the defect is
that "none" is offered as the whole pinned-values answer for a gate whose verdict depends on a
mutable external artifact and whose default bound is unasserted.

### M3 — the counter's finding-id check does not verify the row's `8/8` tally (counter weakness, row-relevant)

The row's Self-test cell asserts `→ ROUTEMIX_SELFTEST: 8/8 pass`. The counter only compares the
*first whitespace token* of the last stdout line against the cell (`measure.py:178-180`). A tool
that prints a wrong tally still passes the row check — measured with the counter's own `run_row`:

```
tally-wrong-3/8             counter_row_verdict=PASS   last='ROUTEMIX_SELFTEST: 3/8 pass'
forged-tally-0/8            counter_row_verdict=PASS   last='ROUTEMIX_SELFTEST: 0/8 pass'
all-cases-fail-but-exit-0   counter_row_verdict=PASS   last='ROUTEMIX_SELFTEST: 8/8 pass'
```

The row's own claim is currently **true** (verified 8/8 with eight `ROUTEMIX_CASE … ok` lines, and
the eight case literals at `:77-84` are exactly the eight cases), so this is not a false row — it is
a note that the counter's check of this row's finding id is weaker than the row's assertion, and
that the assertion currently rests on the tool, not on the counter.

### M4 — the usage-probe check is nearly vacuous for this row (counter weakness, row-relevant)

The counter checks that the usage probe's exit code appears as a token in the row's verdict map
(`measure.py:182-183`). This row's map declares 0, 1, 2 and 64, so *any* of those satisfies it.
Measured with the counter's own `run_row` against mutants of the tool:

```
exit-1-becomes-0         counter_row_verdict=PASS
exit-2-becomes-0         counter_row_verdict=PASS
usage-64-becomes-1       counter_row_verdict=PASS
usage-64-becomes-2       counter_row_verdict=PASS
```

So for this row the counter does not bind the usage exit code to 64, and does not bind the entry's
failure exit to 1. (Renaming the finding id *is* caught: `marker-renamed` →
`finding-id-not-in-row (ROUTEMIX_DONE:)`. Making the selftest always exit 1 is caught:
`selftest-exit=1`.)

### M5 — the row's selftest is hermetic, so the known clone-context blocker does not apply here (negative finding, recorded because the seat brief asks)

The contract's disclosed C3 blocker is that the truthful `tools/round21-measure.py --selftest` exits
1 from the counter's fresh clone because its fixtures expect sibling fleet repos. `wave-route-mix`
has no such dependency: its selftest parses an inline YAML literal (`:74`) and asserts against
literal expectations. It exits 0 from the clone with a scratch `TMPDIR` and `stdin=/dev/null`, and
the counter reports the row covered (`C3_TOOL tools/wave-route-mix.py: covered line 2166`). M2 above
is about this row's pinned-value disclosure, not about a clone-context failure.

## Additional measured facts (not defects)

- The selftest is not vacuous: 13 of 20 single-line mutants are killed by it. Inverting any one of
  the eight case literals (`:77-84`) drops the tally to `7/8 pass` and the exit to 1; weakening the
  bound comparison (`:67`, `>` → `>=` or → never) and dropping the `over` check likewise fail the
  selftest (`6/8` or `7/8`). The seven survivors are the three exit-code rewrites
  (`:113`, `:124`, `:108`), the `--max-share` argparse default (M2), the provider split
  (`rsplit` vs `split` — the fixtures use single-slash aliases only), and a hardcoded tally.
  Full table: `@P@ExecTool25/mutation-selftest.txt`.
- `--help` prints argparse's help to stdout and exits **64** (`:100-103` catches argparse's
  `SystemExit`), i.e. help is classed as usage. Consistent with the map's "usage" family; noted for
  completeness.
- The row appears in only one registry section (the counter's `registry_rows` finds exactly one row
  naming `tools/wave-route-mix.py`, at line 2166); the round-21 table's older row at `:1976` sits
  under a heading that does not match the counter's `^#{2,4} Gate/probe registry` pattern, so it is
  not a candidate row.
- The lane's own `tools/registry.json:865-877` registers `wave-route-mix-selftest` with
  `expect.exit 0` and `stdout_contains ["ROUTEMIX_SELFTEST: 8/8 pass"]` — consistent with the
  observed behaviour.

## Report to the L1

- C3 is not falsified by this row; the row is covered by the frozen counter and its self-test is
  real, hermetic, reproducible and fast (37 ms), with no clone-context blocker.
- Two row-text defects are worth fixing at the L1's discretion: **M1** (name the traceback path
  under exit 1, as the `frozen registry replay` row does) and **M2** (restore a pinned value for
  `--max-share 0.40` and/or re-point at the retained round-21 frozen runs, instead of "none").
- Two counter-strength notes, consistent with the already-disclosed mutation work but specific to
  this row: **M3** (the finding-id check ignores the `8/8` tally the row asserts) and **M4** (the
  usage-probe check is satisfied by any of the four codes this row's map declares).

## Blockers

None. Everything above was measured directly against candidate bytes; no report-only inference is
presented as measurement. No source file and no registry row was modified.
