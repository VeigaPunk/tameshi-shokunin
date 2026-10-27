# T51W2ExecTool17 — C3 row audit: `tools/shrink-case.py`

Seat: T51W2ExecTool17 (leaf executor) · round 51, wave 2 (falsify) · judged axis: operability · milestone: C3 row
falsification.
Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`; content candidate `6d8c11e378aa90b12650808e1b79270742935f15`; lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Scope: audit only. No source file, row, counter, spec or fixture in the lane/fleet/sibling repos was written; no git/jj
mutation anywhere. Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool17/` (clone, fixtures, TMPDIR), deleted before
yield. No tool installed. Receipts: `.ufo/waves/round-51/w2/T51W2ExecTool17/`.

**Headline.** The row is operable: the exact self-test exits 0 from a fresh `git clone --shared` at CAND in 0.75 s with
the recorded terminal line, the usage probe exits a declared code, the kind is `probe` in the PROTOCOL sense, and every
exit code the run mode produced is `0` or `2` as declared. **One row field is false**: the Write-scope cell says
`lane read-only`, but every invocation of the tool — the row's self-test *and* the row's entry command — imports
`tools/pbt-staged-id.py` through `importlib` and writes `tools/__pycache__/pbt-staged-id.cpython-314.pyc` (77 535 B)
into the lane tree. The frozen C3 counter still credits the row, because the predicate only runs the self-test and reads
its terminal token; the false cell is invisible to it. PROTOCOL §Gate standard, *Self-test*, states the clause the write
violates: "over isolated fixtures (temp trees, no network, no live-tree write)".

## 1. The row under test

`SKILL.md:2138` `#### Gate/probe registry — round 51`; header `SKILL.md:2141`; row **`SKILL.md:2158`** (8 cells,
verbatim in `T51W2ExecTool17/row-2158.txt`):

| cell | content |
|---|---|
| Name | `shrink-case` |
| Kind | `probe` |
| Entry command | `` `python3 tools/shrink-case.py --pristine PRISTINE.py --mutant MUTANT.py --case CASE.json --out OUT.json` `` |
| Verdict map | `0 shrunk (report written); 1 selftest checks failed; 2 could-not-evaluate (usage, unreadable file, invalid case, case carries no kill)` |
| Self-test command | `` `python3 tools/shrink-case.py --selftest` `` → `SHRINK_SELFTEST: cases=21 failed=0` |
| Pinned values | `` `tools/pbt-staged-id.py` `` generator imported beside the tool; `` `tools/staged-id-guard.py` `` and `` `.ufo/evidence/round-49/c2/panel.json` `` for the M02 leg; expected edit literals in the tool source |
| Write scope | `caller-chosen --out FILE; tempfile.mkdtemp roots under TMPDIR for guard runs and selftest; lane read-only` |
| Owner | `tameshi` |

Tool at candidate: `tools/shrink-case.py`, 632 lines, sha256
`1ac31ae58d807df76d632d5eb18b06c2e62eae0428fc1fb3b2dc3f01ebb3526f` (retained copy
`T51W2ExecTool17/shrink-case.py.txt`).

## 2. Method

- `git clone -q --shared` of the lane in scratch, `checkout -q --detach <CAND>`;
  `git rev-parse --show-toplevel` printed the clone root (`/fast/scratch/…/work/tameshi-shokunin`) and
  `rev-parse HEAD` printed CAND before every run. All runs: `cwd` = clone, `stdin` = `/dev/null`,
  `TMPDIR` = `$S/tmp` (seat scratch), `pty` off.
- Ran the row's **exact backticked self-test** and the counter's usage probe form (`interpreter prefix + tool +
  --r51-no-such-flag`), then the entry command end to end on a real killing pair, then eight run-mode exit-code probes
  (twelve invocations in all, `exits.txt`).
- Row fields checked against the tool source (`git show <CAND>:tools/shrink-case.py`), the generator
  (`tools/pbt-staged-id.py`), the guard (`tools/staged-id-guard.py`), the pinned panel and PROTOCOL §Gate standard.
- Replayed the row through the frozen counter's own functions (`row_reason`, `run_row` from
  `.ufo/evidence/round-51/c3/measure.py` at CAND, imported read-only) — see §6.
- Repo reads via `git -C … show <rev>:<path>` only.

## 3. Direct measurements (receipts in `T51W2ExecTool17/`)

| # | command (from the clone, `TMPDIR` = scratch, stdin `/dev/null`) | exit | last stdout line | wall |
|---|---|---|---|---|
| 1 | `python3 tools/shrink-case.py --selftest` — **the row's exact self-test** | **0** | `SHRINK_SELFTEST: cases=21 failed=0` | **0.75 s** |
| 2 | same, second run (determinism) | 0 | identical, stdout sha256 identical (`8be8fe37…921576`) | 1.10 s |
| 3 | `python3 -I tools/shrink-case.py --selftest` (the tool's documented form) | 0 | `SHRINK_SELFTEST: cases=21 failed=0`, same stdout sha256 | 1.10 s |
| 4 | `python3 tools/shrink-case.py --r51-no-such-flag` — **usage probe** | **2** | (stdout empty) stderr ends `error: unrecognized arguments: --r51-no-such-flag` | 0.03 s |
| 5 | entry command on the M02 pair (`--pristine/--mutant/--case/--out`) | **0** | `shrink-case: units 7 -> 1, runs 7`; `out.json` written | 0.23 s |

- `selftest.stdout` (21 lines `SELFTEST … ok`, then the terminal line), `selftest.stderr` (empty),
  `selftest-again.stdout`, `selftest-I.stdout`, `usage.stdout`/`usage.stderr`, `entry.stdout`/`entry.stderr`,
  `entry-out.json`, `entry-case.json`, `exits.txt`.
- The 21 checks are 7 `core:` ddmin checks, 7 `cli:` stub checks and 7 `M02:` checks — the M02 group is the three-way
  agreement the `cases=21` value reports (`shrink-case.py:605`).
- First token of the terminal line is `SHRINK_SELFTEST:`, which the row's Self-test cell contains ⇒ the counter's
  finding-id test passes. The marker is a real diagnostic (case count **and** failure count, computed from
  `checks`/`failed`, `shrink-case.py:601-605`), not help text; a forced failure prints
  `SHRINK_SELFTEST: cases=21 failed=1` and exits 1 (`failpanel-selftest.stdout`, scratch copy — the lane was not
  touched).
- `usage` exit **2** is a token in the Verdict map ⇒ declared.
- **Clone-context:** this row is *not* the known row16 failure. The self-test needs no sibling fleet repo; it is
  clone-safe at CAND (measurement 1).

### 3.1 Exit-code audit (`exits.txt`, 12 probes; source `shrink-case.py:611-629`)

| code | row says | measured |
|---|---|---|
| 0 | `shrunk (report written)` | entry command on a killing pair: `units 7 -> 1, runs 7`, `out.json` = `{case, runs:7, units_before:7, units_after:1}` (`entry-out.json`) |
| 1 | `selftest checks failed` | only from `--selftest`: failing-panel control → `SHRINK_SELFTEST: cases=21 failed=1`, exit 1. **No run-mode invocation produced 1.** |
| 2 | `could-not-evaluate (usage, unreadable file, invalid case, case carries no kill)` | identical guards (no kill) → 2; absent `--case` → 2; `{"registry":5}` → 2; no arguments → 2 (`missing --pristine, --mutant, --case, --out`); `--out` an existing directory → 2 (`Is a directory`); odd `map` shapes → 2 |

No undeclared code appeared; run mode returns only `0` or `2` (`run_from_arguments` returns 0 or raises `Unusable`,
caught at `shrink-case.py:626`). `--pristine`/`--mutant` given as a directory, `--case` as a directory and `--out`
inside a missing parent all land on the declared 2 path (source-checked at `:231-247`).

## 4. Row-field audit against source

| cell | verdict |
|---|---|
| Kind `probe` | **Upheld.** PROTOCOL §Gate standard: "A tool that cannot fail is a probe." Run mode has no failure verdict — exit 0 always means "report written", exit 1 exists only as its own self-test failure — and the row's own Verdict map says so. 12 run-mode probes returned only 0/2. |
| Entry command | **Upheld.** The four flags match `argparse` (`shrink-case.py:611-618`) and the entry command ran end to end (measurement 5). It does not advertise `-I`, unlike the tool's docstring (`:12-14`); both forms run identically (§5 F4). |
| Verdict map | **Upheld** as a code set and as meanings (3.1). |
| Self-test command | **Upheld.** Exact, one backticked command, no shell metacharacters; exits 0 at CAND from a clone; terminal line reproduced byte-for-byte; 21 checks all `ok`. |
| Pinned values | **Upheld, and load-bearing.** `load_generator(os.path.dirname(os.path.abspath(__file__)))` (`:217-230, :258`) imports `tools/pbt-staged-id.py` beside the tool; the M02 leg reads `tools/staged-id-guard.py` and `.ufo/evidence/round-49/c2/panel.json` (`:516-530`); `M02_EDIT` is a literal (`:44-45`). Verified independently: the panel's M02 `old`/`new` equal `M02_EDIT` exactly. Control: the same tool without the panel prints `M02: the embedded edit is the panel M02 edit  skip (panel not reachable)` and `cases=20` (`nopanel-selftest.stdout`) — so the pinned panel really decides the `cases=21` value. |
| Write scope | **FALSE** on `lane read-only` (§5 F1). The other two clauses hold: `--out` is the only report path (measurement 5), and both `tempfile.mkdtemp` roots (run `:260`, selftest `:452`/`:540`) honour `TMPDIR` (verified: `TMPDIR=<scratch>` → `mkdtemp` returned `<scratch>/probe-…`; no TMPDIR leftovers after any run). |
| Owner `tameshi` | Correct. |

## 5. Findings

**F1 (medium — the row's Write-scope cell is false; the frozen counter cannot see it).**
The row says `lane read-only`. Measured, in a cleaned clone at CAND, with a full-tree before/after snapshot
(`footprint.txt`): the only change the self-test makes to the lane is

```
204a205,206
> tools/__pycache__
> tools/__pycache__/pbt-staged-id.cpython-314.pyc     (77 535 B, sha256 c1238840780f0cda9d936aa66efdede10f3e416595623460d72de16cceaf9e0b)
```

plus the `tools/` directory mtime. The **entry command writes the same file**: after `rm -rf tools/__pycache__`,
measurement 5 left `tools/__pycache__/pbt-staged-id.cpython-314.pyc` again; the usage probe does not (argparse exits
before any import). Cause isolated (`minimal-import.txt`): `load_generator()` loads the lane sibling with
`importlib.util.spec_from_file_location` + `spec.loader.exec_module` (`shrink-case.py:217-230`), and CPython caches the
bytecode beside the source — the same call site feeds run mode (`:258`) and the M02 leg (`:573`). No `-B`, and unlike
the C3 counter (`measure.py:40` sets `sys.dont_write_bytecode = True`) the tool never disables it; with `-B` no file is
written (control). The write is gitignored (`.gitignore:4` `__pycache__/`), so `git status --porcelain` stays at 0
lines and the tree is not dirtied — but it *is* a live-tree write, which is the exact thing PROTOCOL §Gate standard,
*Self-test*, forbids ("isolated fixtures (temp trees, no network, no live-tree write)"). Corroboration that this is the
tool's live behaviour, not a clone artefact: the real lane worktree currently holds
`tools/__pycache__/pbt-staged-id.cpython-314.pyc` (read-only `ls`).
Consequence for the claim: the row's write-scope cell is a false statement of fact, and a truthful cell would say
"writes `tools/__pycache__/<generator>.pyc` beside the imported generator (gitignored) unless `PYTHONDONTWRITEBYTECODE`
is set". Not repaired (seat bounds).

**F2 (low — bounded exit-1 gap, not induced from the frozen tree).** `run_from_arguments` catches only `Unusable`
(`shrink-case.py:625-627`), while the pinned generator's `run_guard` can raise `SetupProblem` (`pbt-staged-id.py:782-790`,
on an OSError writing the case files or spawning the guard). That path would leave the process with an uncaught
traceback and exit **1**, which this row maps to `failed`, where a corrupted work directory is `could-not-evaluate`.
Not counted as a mismatch: from the frozen tree the generator is committed and `load_generator` folds import failures
into the declared 2, and no caller-controlled input reached exit 1 in eight run-mode probes. Recorded because the contract's
C3 *cannot_see* names exactly this surface ("the verdict map names every code the tool can exit with beyond 0, 1 and
the usage code") and this is its nearest neighbour.

**F3 (low — the `cases=21` marker degrades silently without the pin).** With `panel.json` absent the same tool prints
`cases=20` and exits 0; a whole check becomes a `skip` line (`shrink-case.py:524-531`). The row's Pinned-values cell
does name the panel, so the row is truthful; the counter would not notice the degradation, because it only requires the
first token `SHRINK_SELFTEST:` (`measure.py:172-180`) — `cases=20` would be accepted just as `cases=21` is. This is a
counter-side weakness, disclosed here rather than attributed to the row.

**F4 (observation — no mismatch).** The row runs `python3 tools/shrink-case.py --selftest` while the tool's docstring
advertises `python3 -I tools/shrink-case.py …` (`:12-14`). Both forms exit 0 with byte-identical stdout
(`selftest.stdout` vs `selftest-I.stdout`), and both write the same pyc, so the missing `-I` changes nothing here; the
only theoretical difference is `sys.path[0]` (`tools/`) being consulted before the interpreter's own modules.

## 6. Counter replay: the frozen predicate credits the row

Read-only import of `.ufo/evidence/round-51/c3/measure.py` at CAND, row parsed from `SKILL.md` at CAND
(`counter-replay.out`):

```
row line 2158 cells 8
row_reason -> None argv ['python3', 'tools/shrink-case.py', '--selftest'] usage ['python3', 'tools/shrink-case.py', '--r51-no-such-flag']
run_row -> (None, 'SHRINK_SELFTEST: cases=21 failed=0')
```

So this row contributes `covered` to C3_R51_PASS while its Write-scope cell is false (F1). That is the precise gap
between the frozen predicate (exit + terminal token) and the claim it stands for (a truthful row).

## 7. Limits of this audit

- F1 is measured on a `--shared` clone at CAND on this host (CPython 3.14.8). The mechanism is version-independent
  (`SourceFileLoader` caching), but the file name carries the interpreter tag, so a different interpreter yields
  `…cpython-3XX.pyc` with the same effect. The live-lane listing corroborates one such file at `cpython-314`.
- "Lane read-only" was judged by filesystem effect (name/size/mtime census of the whole tree except `.git`), not by a
  syscall trace; a read-only-open violation without a filesystem change would not be caught by this method.
- Exit 1 in run mode (F2) was not induced; the reasoning is source-level.
- No claim is made about the quality of the shrunk cases the tool produces beyond the tool's own three verification
  arms (`sub-case`, `kills`, `1-minimal`) reproduced green in the self-test.
- The `.ufo/evidence/round-51/c3/__pycache__/` entry that appeared in the clone afterwards is from my own read-only
  import of the counter (`replay.py`), not from the tool.

## 8. Disposition

The row is **operable and truthful in the seven fields C3 exercises**: kind `probe` correct per PROTOCOL, entry
command real, verdict map accurate for 0/1/2, self-test exact and green from a clone at CAND with the recorded terminal
line, pinned values real and behaviour-bearing, owner correct. **The Write-scope cell is false**: the tool writes
`tools/__pycache__/pbt-staged-id.cpython-314.pyc` into the lane in both the self-test and the entry command, which
contradicts `lane read-only` and PROTOCOL §Gate standard's "no live-tree write" clause for self-tests; the frozen
counter credits the row regardless (§6). Two bounded notes (F2 exit-1 mapping, F3 silent `cases=20`) are recorded for
the L1's disclosure decision. No repair was made — seat bounds forbid editing the row or the tool.
