# RGControl — C1 pristine-control determinism (round-gate, pinned blob)

Seat: RGControl (leaf). No mutants run. All evidence under `/tmp/tameshi-r16-RGControl-3092/`.
Nothing written outside this report.

## Verdict (lead)

The repeated-control gate on the pinned blob **does not pass**: the tool's verbatim verdict is
`REPEAT_CONTROL: controls_mismatch` (exit 1) for both samples (N=3 and N=5).

The mismatch is **fully explained and bounded**: it is the selftest's own random temp-dir token,
`kumitate-round-gate-selftest-<6 chars>`, printed 9 times per run inside PASS detail text. It is
sourced at `round-gate.mjs:690` (`mkdtempSync(join(tmpdir(), 'kumitate-round-gate-selftest-'))`).
Everything else is invariant across 8 runs: exit `0`, stderr 0 bytes, stdout 9663 bytes, and after
substituting that one token the captures are byte-identical (one sha256). **No timing field exists
in the stdout at all.**

Consequence for C1's ledger leg: do **not** record `controls_match`. Record exit-status determinism
(8/8 zero, stderr empty) plus the named stdout token, and state that the sweep's kill oracle is
exit-only (below), so kill attribution is sound at exit granularity and not at text granularity.

## Commands and provenance

| Item | Observed |
|---|---|
| Blob materialized | `git -C kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > /tmp/tameshi-r16-RGControl-3092/round-gate.mjs` |
| Blob sha256 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` — matches the pin |
| Blob size / git blob oid | 80415 bytes; git object `1f7d623e7ba548b7181ad75ae93a2f0c0b8579f3` (`git rev-parse <rev>:scripts/round-gate.mjs`), file size equals `git cat-file -s` |
| Gate tool | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/repeat-control.py`, emitted `tool-sha256=296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`, `python=3.14.8` |
| Runtimes | `node v24.21.0`, `git 2.56.0` |
| Tool usage | `repeat-control.py --runs N --out DIR -- COMMAND [ARG...]` (help output, no other mode shown) |

Exact invocations (cwd `/home/vgpnk/Projects/shokunin/tameshi-shokunin`):

```
python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r16-RGControl-3092/ctrl3 -- node /tmp/tameshi-r16-RGControl-3092/round-gate.mjs --selftest
python3 tools/repeat-control.py --runs 5 --out /tmp/tameshi-r16-RGControl-3092/ctrl5 -- node /tmp/tameshi-r16-RGControl-3092/round-gate.mjs --selftest
```

Exit codes: 1 and 1. Wall time 9.9 s / 17.2 s. Both output dirs were absent beforehand (tool requires this).

## Verbatim verdict lines

N=3 (`ctrl3`):

```
REPEAT_CONTROL_TOOL repeat-control.py r12 (tameshi-shokunin, 2026-10-20) tool-sha256=296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25
REPEAT_RUN 1 exit=0 stdout-bytes=9663 stderr-bytes=0
REPEAT_RUN 2 exit=0 stdout-bytes=9663 stderr-bytes=0
REPEAT_RUN 3 exit=0 stdout-bytes=9663 stderr-bytes=0
REPEAT_COMPARE identical=no runs=3
REPEAT_OUT /tmp/tameshi-r16-RGControl-3092/ctrl3
REPEAT_CONTROL: controls_mismatch
```

N=5 (`ctrl5`): identical shape, `REPEAT_RUN 1..5` all `exit=0 stdout-bytes=9663 stderr-bytes=0`,
`REPEAT_COMPARE identical=no runs=5`, `REPEAT_CONTROL: controls_mismatch`, exit 1.

`ctrl3/finding.txt` verbatim:

```
REPEAT_CONTROL: controls_mismatch
REPEAT_EXIT: 1
```

Tool semantics confirmed from source: bytes are compared as bytes — "no decoding, stripping,
newline normalization or whitespace folding anywhere" (`tools/repeat-control.py:22-23`), mismatch
on any disagreement in `(exit, stdout, stderr)` (`:32`).

## Suite outcome (pristine)

`ctrl3/run-1.stdout` (63 lines, identical shape in all 8 captures):

- line 1: `kumitate round-gate --selftest (hermetic, node v24.21.0)`
- 60 lines beginning `PASS`, 0 lines beginning `FAIL`
- line 62: `ROUND_GATE_SELFTEST: 60/60 pass`
- line 63: `VERDICT: PASS`

Exit path is `round-gate.mjs:1511` `process.exitCode = main()`; `selfTest()` returns
`passed === results.length ? 0 : 1` (`:1506`) — i.e. the exit code is a faithful "all 60 checks
passed" oracle. It also removes its temp root in a `finally` (`:1498`); after all 8 runs,
`ls -d /tmp/kumitate-round-gate-selftest-*` returned 0 entries.

## Variance decomposition

- **exits**: `0` in 8/8 runs (3 + 5). No nonzero pristine exit observed.
- **stderr**: 0 bytes in 8/8 runs.
- **stdout length**: 9663 bytes in 8/8 runs (the random suffix is fixed-width, so even length is stable).
- **stdout bytes**: different every run. Raw sha256 values in `ctrl5`: 5 distinct hashes
  (`074fd7dc…`, `27f46890…`, `60da4bba…`, `e10f3a2d…`, `ed30f450…`).
- **Substituted captures**: replacing `kumitate-round-gate-selftest-[A-Za-z0-9]{6}` with
  `kumitate-round-gate-selftest-SUFFIX` yields sha256
  `2bc8a186bf9d7008cbbc0e61650d87a1c218f41cf909553188cce172a9ff086f` for **all five** ctrl5 runs
  and all three ctrl3 runs; `diff` exit 0 pairwise.
- **Lines affected**: exactly 9 of 63, selftest cases 30, 32, 33, 35, 36, 37, 53, 54, 56. One
  distinct token per run, occurring 9 times (e.g. ctrl3: `…-kpXtMc`, `…-kSS3AC`, `…-FDpe2U`;
  ctrl5: `…-6Nfcpm`, `…-DNZYTx`, `…-P4pFvz`, `…-V9o3Tj`, `…-XlSc6T`).
- **Timings**: none. No elapsed/duration/ms token appears in stdout. The only match for
  `durationMs` is the frozen-JSON-key fixture detail at stdout line 44, where it is a key *name*
  inside `keys=checks,citations,contract,durationMs,…`, not a measured value (and it is identical
  in every run). So there is no timing field to vary.
- Node version is printed in the header line and was constant (`v24.21.0`).

The suite's own nested hermeticity check (`round-gate.mjs:1393-1400`) compares only the last two
lines by regex (`/^ROUND_GATE_SELFTEST: \d+\/\d+ pass$/` and `VERDICT: PASS`), i.e. the upstream
authors already treat the temp token as noise and never compare it.

## Implications for C1's ledger leg (`js-round-gate`)

1. **Control wording.** Raw gate verdict is `controls_mismatch` (exit 1) with a named cause, not
   `controls_match`. Per the registry (`SKILL.md:1487-1488`), a mismatch forbids attributing a later
   red suite *solely* to the mutant — so the sweep needs a stated basis, not silence.
2. **The basis that holds.** `tools/mutate-and-run.sh` gates the pristine run on exit only
   (`:470-476`: `ctl_rc -ne 0` → CONTROL RED → setup abort) and classifies `KILLED` as any exit
   outside `{0,124,126,127}` (`:32`, `:486-492`), with `SURVIVED` = exit 0. Since pristine exit is
   deterministically 0 (8/8) and stderr is empty, kill attribution is sound **at exit granularity**:
   a red mutant suite cannot be caused by the pristine command's stdout nondeterminism.
3. **What is not attributable.** Text-level expectations. A mutant that changes a PASS message
   without changing exit status is graded SURVIVED; a pre-registered prediction that expects a
   specific line to change must therefore be scored by exit, not by stdout diff. Stdout equality
   must never be used as the sweep's expected value on this target.
4. **Prediction consequence.** Because the oracle is exit-only and `selfTest()` returns 1 on *any*
   failed check (`round-gate.mjs:1506`), a mutant that breaks an asserted behavior anywhere in the
   60 checks is detectable; a mutant that only relaxes printed text is not. Predictions stating
   "killed" should name the check whose assertion the edit breaks, not a message diff.

## Bounded recommendations (in priority order)

- **R1 — Record the truth in the ledger leg.** Write `js-round-gate` control as: `repeat-control.py`
  `controls_mismatch` (exit 1) caused by `kumitate-round-gate-selftest-[A-Za-z0-9]{6}` ×9/run
  (`round-gate.mjs:690`); exit 0 and empty stderr 8/8; token-substituted captures byte-identical
  sha256 `2bc8a186…`. Do not claim `controls_match`.
- **R2 — Do not normalize to reach green.** `SKILL.md:1495` says not to "normalize output" for this
  gate. The token substitution above is analysis of an observed mismatch, not a gate pass; if L1
  wants a normalized textual oracle, it must be **pre-registered as the command itself** (a
  projection command named in the spec) before mutants run, and labelled as a projection.
- **R3 — Score the sweep by exit.** Ensure the 10 pre-registered predictions for the mutants are
  phrased against exit codes / the 60/60 summary, and that the harness does not compare mutant
  stdout to pristine stdout.
- **R4 — Do not change kumitate this round.** The only way to get a literal `controls_match` on
  `--selftest` is to stop printing the temp root in PASS details — a sibling-repo (kumitate) change
  outside this lane's write scope. Note it as a follow-up, not an action.
- **R5 — Alternative surface is not available.** `node round-gate.mjs --help` exits 64 (usage) and
  prints usage, so it cannot serve as a zero-exit stable pristine control. `--selftest` is the only
  green, hermetic pristine surface for this blob.

## Evidence paths (/tmp)

- `/tmp/tameshi-r16-RGControl-3092/round-gate.mjs` — pinned blob, sha256 above.
- `/tmp/tameshi-r16-RGControl-3092/ctrl3/` — `command.txt`, `finding.txt`, `run-{1..3}.{stdout,stderr,exit}`, `norm-{1..3}.stdout`.
- `/tmp/tameshi-r16-RGControl-3092/ctrl5/` — `command.txt`, `run-{1..5}.{stdout,stderr,exit}`.
- No tool installs or upgrades were performed. No mutants were run; only the unmodified copy was executed.

## Remaining unknowns

- Whether L1's pre-registered mutation predictions are exit-phrased or text-phrased — that is the
  condition under which this control finding does or does not weaken C1's kill-rate claim.
- `[INFERENCE]` The temp-token nondeterminism is intrinsic to `mkdtempSync` and cannot be removed
  by any environment variable; not tested, since `mkdtempSync` does not accept a fixed-name mode.
