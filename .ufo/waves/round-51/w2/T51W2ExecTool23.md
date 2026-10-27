# T51W2ExecTool23 — independent audit of the C3 registry row for `tools/wave-accounting.py`

Candidate `6d8c11e378aa90b12650808e1b79270742935f15` (base `9962033fd7a75aa2f2847e979dd687a5d28505a1`).
Row audited: **SKILL.md:2164**, the `wave accounting` row of the canonical section
`#### Gate/probe registry — round 51` (heading SKILL.md:2138, 8-cell header SKILL.md:2140, section runs
2138-2171 to EOF at CAND; the row bytes are byte-identical in the worktree at audit time, md5
`e4ccec492dfec03f6965effe85794bc6` for SKILL.md:2164 in both). Read-only on the lane; three `git clone --shared --no-checkout` trees at CAND in
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool23/` (`cand`, `pinprobe`, `c3work/tameshi-shokunin`),
each with `git rev-parse --show-toplevel` asserted before use. Raw receipts:
`.ufo/waves/round-51/w2/@P@ExecTool23/receipts.txt`.

## Verdict

**The row is operably true at CAND.** Every field the C3 predicate grades reproduces: the backticked
self-test exits 0 from a fresh `--shared` clone under the counter's exact environment, its last stdout
line is `FINDING: SELFTEST_PASS` (the id the row records), the usage probe exits 64 (declared), both
named pinned paths exist at CAND and are load-bearing, and the write-scope claim holds over twelve
in-clone invocations (no lane write, no `__pycache__`, TMPDIR empty afterwards). Nothing in this row produces a
clone-context failure: this row is **not** `round21-measure`, and it does not reproduce that blocker.

Two **disclosure** gaps (F1, F2) and one **semantic approximation** (F3) are reported below. None of them
makes a declared cell false, so none of them adds a `missing` tool to C3, and none of them is a reason to
repair the row mid-wave. F4 is a counter-side weakness in how the row's marker is matched; F5 records
the properties that make this row *more* operable than the section average.

## What was run

Counter-exact replication (`.ufo/evidence/round-51/c3/measure.py:47-50, 173-183`): `env` = ambient minus
`GIT_*` plus `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`; `TMPDIR=<work>/tmp`; `cwd` = clone
root at CAND; `stdin=DEVNULL`; `python3 tools/wave-accounting.py …` resolved from the clone.

| Invocation | Exit | Wall | Last stdout line |
|---|---|---|---|
| `python3 tools/wave-accounting.py --selftest` | **0** | 1.01 s | `FINDING: SELFTEST_PASS` |
| `python3 tools/wave-accounting.py --r51-no-such-flag` | **64** | 0.04 s | (empty; stderr `error: unrecognized arguments: --r51-no-such-flag`) |
| same self-test, ambient env, `TMPDIR=$S/tmp` | 0 | 0.88 s | `FINDING: SELFTEST_PASS` |

Marker extraction as the counter does it (first whitespace token of the last non-empty line) is
`FINDING:`; that token appears in the row's Self-test cell (SKILL.md:2164, `→ FINDING: SELFTEST_PASS`) and
`64` appears as a token in the row's Verdict map cell. Both graded checks pass.

Self-test tally reproduced verbatim: `ACCOUNTING_SELFTEST: 8/8 pass`, `ACCOUNTING_EXTRA_SELFTEST: 16/16
pass`, 24 `ACCOUNTING_*_CASE … ok` lines, stderr empty. `8` matches `CASES` in
`.ufo/evidence/round-22/measure.py:12-21`; `16` matches `len(cases)` in
`.ufo/evidence/round-22/accounting-extra-cases.json` (names listed in the receipts). The row's "8/8 frozen
plus 16/16 supplemental" is exact, and both tallies are computed from the fixtures, not hardcoded.

## Field-by-field against source

| Cell | Row text (abridged) | Evidence at CAND |
|---|---|---|
| Kind | `gate` | Exit 1 is reachable on a real invariant failure, measured: `--bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected …wrong-count-expected.json` → **exit 1**, `WAVE_ACCOUNTING: failed`, `FINDINGS: TOTAL_MISMATCH`. Verdict is `1 if findings else 0` (`tools/wave-accounting.py:122`) over caller-supplied declared data, so the tool can fail → PROTOCOL.md:377-379 ("A tool that cannot fail is a probe") keeps this a gate, not a probe. |
| Entry command | `python3 tools/wave-accounting.py --bundle BUNDLE.json --expected EXPECTED.json` | Matches the interface: `--bundle/--expected/--json/--selftest` (`:199-206`), both inputs required, missing → `print_usage` + 64 (`:213-215`). Measured `--bundle` alone → 64 (`bundle-only`), no arguments → 64 (`noargs`). |
| Verdict map | `0 clean; 1 failed invariant; 2 could-not-evaluate (invalid, unavailable or tampered input); 64 could-not-evaluate (usage)` | All four observed and correctly classed: **0** on the committed pair (`total {"completed":66,"dead":80,"seats":146}`); **1** `TOTAL_MISMATCH`; **2** `INVALID_INPUT` for a missing path and for a directory as `--bundle`, `SNAPSHOT_TAMPERED` for a file whose digest differs from `expected.json` (`:134-135`, `:139-140`); **64** for the unknown flag, for no arguments, and for `--selftest --json` (`:209-211`, `:213-215`, `:207`). Source enumeration of every exit path yields exactly {0,1,2,64} — no undeclared code. |
| Self-test command | ``python3 tools/wave-accounting.py --selftest`` → `FINDING: SELFTEST_PASS`, 8/8 + 16/16 | Measured exit 0 and that exact last line. Command has no shell metacharacters; argv is `python3 tools/T --selftest`, satisfying the predicate's `python3 [-I]` form. |
| Pinned values | `.ufo/evidence/round-22/measure.py`, `.ufo/evidence/round-22/accounting-extra-cases.json` | Both `git cat-file -e CAND:<path>` → EXISTS. Both are read at run time from `root = Path(__file__).resolve().parent.parent` (`:146`) and both are **load-bearing**, see P1-P3 below. |
| Write scope | `stdout only; caller-chosen --bundle/--expected read-only, selftest fixtures under isolated TMPDIR` | Verified: after twelve in-clone invocations (plus one run of an isolated copy) `git status --porcelain` in the clone is empty, `find . -name __pycache__ -o -name '*.pyc'` is empty (bytecode suppressed at `:21` although the selftest `exec_module`s the oracle via `:149`), `TMPDIR` is empty after the selftest's `TemporaryDirectory(prefix='tameshi-r22-accounting-')` (`:156`), and every verdict run emitted nothing on stderr. |
| Owner | `tameshi` | `tools/wave-accounting.py` is a lane tool under the lane's `tools/`. |
| Name | `wave accounting` | Unique in the file (SKILL.md:2164 is the only row whose Entry cell names this tool inside a `^#{2,4} Gate/probe registry` section; the older occurrence at SKILL.md:1997 sits under `### Round-21 gate/probe registry — finite environment differential`, which does not match the counter's `HEAD_RE` and is therefore not graded). |

### Pinned values really affect expected behaviour (probes in `pinprobe`, restored after each)

- **P1 — frozen oracle mutated.** Flipping one `CASES` expectation in `.ufo/evidence/round-22/measure.py`
  (`('unknown-status','UNKNOWN_STATUS')` → `…_PROBE`) gives `ACCOUNTING_CASE unknown-status FAIL`,
  `ACCOUNTING_SELFTEST: 7/8 pass`, last line `FINDING: SELFTEST_FAIL`, **exit 1**.
- **P2 — supplemental fixture mutated.** Setting `cases[0].expected_exit=0` in
  `accounting-extra-cases.json` gives `ACCOUNTING_EXTRA_CASE role-mismatch FAIL`,
  `ACCOUNTING_EXTRA_SELFTEST: 15/16 pass`, `FINDING: SELFTEST_FAIL`, **exit 1**.
- **P3 — pinned file removed.** `measure.py` moved away → `FINDING: SELFTEST_UNAVAILABLE [Errno 2] No such
  file or directory: …/round-22/measure.py`, **exit 2**.
- **P4 — the gate itself weakened (non-vacuity).** Disabling `if outcome.get('replaced') is not False:`
  in `tools/wave-accounting.py` gives `ACCOUNTING_CASE replacement-seat FAIL`, `7/8`, plus
  `missing-replacement FAIL` and `zero-is-not-false-replacement FAIL` (`14/16`), `FINDING: SELFTEST_FAIL`,
  **exit 1**. The self-test is discriminating on the tool's own guards, not just on its data plumbing.

## Findings

### F1 (low, operability/disclosure) — the Entry cell is a template, and the lane's own earlier row already had a runnable one

`BUNDLE.json` / `EXPECTED.json` in SKILL.md:2164 are placeholders: neither file exists, so the row's
entry command cannot be run by a reader without inventing inputs. The same tool already has a row at
**SKILL.md:1997** (round-21 registry) whose Entry cell is the runnable invocation
`python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected
.ufo/evidence/round-22/expected.json --json`, and that invocation still works at CAND: **exit 0**,
`{"completed": 66, "dead": 80, "seats": 146}`. The round-51 row therefore regresses the disclosure it
replaces. Precedent inside the same round-51 table exists (`evidence disposition accounting` carries a
"lane run:" clause), so this is a row-quality gap, not a house style. The C3 predicate only requires the
Entry cell to name `tools/T` (`c3/measure.py:121`), so this does not falsify the row.

### F2 (low, disclosure) — the Pinned values cell omits the digest-pinned snapshot pair that makes "tampered input" real

The gate implements PROTOCOL's "Two evidences" clause: `expected.json` must pin `bundle_sha256` and a
mismatch is `SNAPSHOT_TAMPERED` → could-not-evaluate (`tools/wave-accounting.py:128-135`). The committed
pair is digests-matching — `sha256(.ufo/evidence/round-22/bundle.json)` =
`dfb1027f80be935fe781ccb8c47d89639a88a9eff6e05d1b45b2a7a61845c18e` = `expected.json:bundle_sha256`;
`wrong-count-bundle.json`/`wrong-count-expected.json` likewise match and are what prove exit 1 — yet the
round-51 row names neither pair, while SKILL.md:1997 names both ("digest-pinned round22 bundle/expected.json,
wrong-count bundle/expected pair"). The two paths the row does name are correct and load-bearing (P1-P3),
so the cell is true but incomplete; the predicate only requires the named paths to exist (`c3/measure.py:148-151`).

### F3 (very low, semantics) — two declared codes carry approximate meanings

- `--help` **exits 0** (`:207` maps `SystemExit(0)` to 0) after printing usage; the map's `0` means
  "clean", so a reader who writes `wave-accounting.py --help && echo ok` sees a clean verdict for a run
  that evaluated nothing. Measured: exit 0, 618 bytes of help on stdout.
- A closed stdout raises `BrokenPipeError` from `print('WAVE_ACCOUNTING: …')` (`:220`), i.e. outside the
  `run()` guard, so the interpreter exits **1** with a traceback — the code the map classes as "failed
  invariant". Measured with `… | head -0`: tool status 1, traceback in stderr. `python3 … >/dev/null`
  still exits 0, so this only bites on a closed pipe.

Both codes are declared, and both behaviours are stock Python; recorded as a meaning gap, not a
falsification.

### F4 (counter-side, not a row defect) — the marker check is satisfied by the generic family prefix

The row's last-line id is `FINDING: SELFTEST_PASS`, but the counter compares the **first whitespace
token** (`c3/measure.py:178-180`), i.e. `FINDING:`, which `FINDING: SELFTEST_FAIL` and
`FINDING: SELFTEST_UNAVAILABLE` also start with. For this row the pass is actually carried by
`rc == 0` (`:175-177`): the tool prints PASS only when `measure()` returned 0 and every supplemental case
passed (`tools/wave-accounting.py:193-194`), which P1/P2/P4 confirmed by flipping the tallies. Disclosed
because it belongs in the C3 `cannot_see` set, not because this row is false.

### F5 (positive) — properties that make this row auditable

- The self-test resolves its pinned inputs from the tool's own location, not the CWD: it passed from
  `cwd=clone` and from `cwd=clone/tools`, and an isolated copy of the file (no sibling tree) fails
  **loudly** — exit 2, `FINDING: SELFTEST_UNAVAILABLE` naming the missing `measure.py`. No silent pass
  when the lane tree is absent.
- The oracle is independent of the recomputation: `.ufo/evidence/round-22/measure.py` drives the tool as
  a subprocess (`:49`) and compares against literal finding ids and literal exit codes (`:76-79`), and the
  supplemental expectations are committed JSON data — PROTOCOL.md:385-389's "expected values committed in
  the owning repo and independent of the recomputation".
- No `GIT_*` leakage: the self-test builds its own scrubbed child env (`:155`) and passed under the
  counter's `GIT_CONFIG_GLOBAL=/dev/null`.

## Reader

Read against candidate bytes, not rephrased. The section this row lives in is
`#### Gate/probe registry — round 51` (SKILL.md:2138); note that the wave-2 re-key list
(`.ufo/waves/round-51/w1/T51ExecRekey.md` §3) names **`### Gate/probe registry` (1499-1517)** as its
registry heading, not this one — so this `## Reader` block is offered as row-level verification evidence
for the heading at 2138, and the L1 should credit it only if it recomputes 2138 as a lost-credit heading.

Claims carrying credit in SKILL.md:2164, each checked against bytes/execution rather than restated:

| Row claim | Candidate-side check |
|---|---|
| kind = gate | SKILL.md:2164 cell 2 vs measured exit 1 on `wrong-count` pair; not a probe |
| entry names `tools/wave-accounting.py --bundle … --expected …` | `tools/wave-accounting.py:199-215`; measured 0/1/2/64 behaviour |
| verdict map `0/1/2/64` | all four codes observed; source enumeration shows no fifth code |
| self-test `python3 tools/wave-accounting.py --selftest` | executed: exit 0, `FINDING: SELFTEST_PASS` |
| "8/8 frozen plus 16/16 supplemental" | `measure.py:12-21` (8 `CASES`) and `accounting-extra-cases.json` (16 cases); tallies printed 8/8 and 16/16 |
| pinned `.ufo/evidence/round-22/measure.py`, `…/accounting-extra-cases.json` | both `cat-file -e` EXISTS at CAND; load-bearing under P1/P2/P3 |
| write scope "stdout only … isolated TMPDIR" | twelve runs: clean `git status`, no `__pycache__`, empty TMPDIR, empty stderr |
| owner `tameshi` | lane-owned tool under `tools/` |

## Scope, limits, housekeeping

- Not audited (outside this seat): whether the *set* of 30 tools is right, the other 29 rows,
  `round21-measure.py`'s clone-context blocker, and the cold-read ledger. This seat supplies evidence that
  the `wave accounting` row is **not** a source of the round's honest C3 failure.
- No source, row, counter or fixture was edited in the lane, fleet or sibling repos. `pinprobe` working-tree
  mutations were reverted with `git checkout -- <path>` and the clone verified clean; no commits were made
  anywhere.
- No tool was installed or updated (no pacman, `uv`, `npm`, `cargo` or `~/.local/bin` write). No PATH
  directory was touched.
- Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool23/` (clones, TMPDIR, receipts source) is deleted
  before yield; the consolidated receipts live only in
  `.ufo/waves/round-51/w2/@P@ExecTool23/receipts.txt` (14 KB). One 4.4 KB file momentarily landed in
  `/tmp` during a probe (`measure.py.bak.<pid>`) and was removed; nothing else was written outside the
  seat's scratch and deliverables.
