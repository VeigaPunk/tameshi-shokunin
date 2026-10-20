# ExitReview — round-12 w1 — repeat-control exit precedence (read-only)

Seat: ExitReview (reviewer, leaf). Advisory, lane-internal. Not an independent non-author promotion, admission, or pass.

## Status of the reviewed artifact

- `tools/repeat-control.py` does **not** exist in the tree (`ls tools/` → `mutate-and-run.sh` only; `git status` → only `.ufo/waves/round-12/` untracked). The review is therefore against the **contract text** (`.ufo/waves/round-12/spec.json` `context`, and the `taskCall/tasks/18` prompt in `dispatch.json`), not against code. No command was executed; no probe was run; no pass is claimed.
- Corpus precedent read: `tools/mutate-and-run.sh:57-64` (exit semantics; "a red control exits 2 (kills could not be attributed)"), `:77-78` (exit map 0/1/2/64), `:33` and `:57-58` (126/127 = not runnable → INCONCLUSIVE). `corpus/QUALITY.md` contains no exit-precedence rule.
- Tooling: no installs or updates performed; `/home/vgpnk/.omp/agent/RULES.md` not needed for this read-only pass and not read. Nothing recorded as installed.

## Contract facts the sequences are judged against (quoted from the spec)

- Gate interface: `python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...`; argv exact; stdin DEVNULL; numbered stdout/stderr/exit saved; bytes not normalized.
- "N>=3 runs, identical exit/stdout/stderr required; any nonzero baseline is could-not-evaluate, any output/exit disagreement fails."
- Stable IDs: `controls_match` exit 0; `controls_mismatch` exit 1; `baseline_nonzero` and `command_unavailable` exit 2 (could-not-evaluate); invalid usage exit 64 (could-not-evaluate); `snapshot_tampered` exit 2.
- **No precedence clause exists** between the rules "any nonzero baseline → could-not-evaluate" and "any output/exit disagreement → fails".

## Expected IDs/classes for the requested sequences

Recommended reading (A) is used in the "Expected" column; it is an [INFERENCE] from the fleet precedent, not a stated contract rule (see Ambiguity 1).

| Case | Expected ID (reading A) | Exit | Class | Unambiguous? |
|---|---|---|---|---|
| exits `[0,1,0]` (stdout/stderr identical) | `baseline_nonzero` | 2 | could-not-evaluate | **No** — also satisfies exit-disagreement → `controls_mismatch` (1). Precedence unstated. |
| exits `[1,1,1]` (identical out/err) | `baseline_nonzero` | 2 | could-not-evaluate | Yes under any-run reading and run-1 reading. Only collides with `controls_mismatch` if stdout/stderr also differ. |
| exits `[0,0,0]`, stderr differs | `controls_mismatch` | 1 | failed | Yes — stderr is named in "identical exit/stdout/stderr required"; no nonzero exit, so no could-not-evaluate path. |
| command unavailable (argv[0] missing / not executable / shebang interpreter missing) | `command_unavailable` | 2 | could-not-evaluate | ID and exit named; **trigger point and short-circuit unspecified** (Ambiguity 3). |
| invalid usage (e.g. `--runs 2`, missing `--`, empty COMMAND, unknown flag) | usage ID **not defined in contract** | 64 | could-not-evaluate | Exit yes; ID missing (Ambiguity 4). |

Reading comparison for the two multi-class sequences:

| Case | (A) any-run baseline, baseline dominates | (B) any-run baseline, mismatch dominates | (C) baseline = run 1 only |
|---|---|---|---|
| `[0,1,0]` | 2 `baseline_nonzero` | 1 `controls_mismatch` | 1 `controls_mismatch` |
| `[1,1,1]` | 2 `baseline_nonzero` | 2 `baseline_nonzero` | 2 `baseline_nonzero` |
| `[0,0,0]` stderr diff | 1 `controls_mismatch` | 1 `controls_mismatch` | 1 `controls_mismatch` |
| `[1,0,0]` | 2 `baseline_nonzero` | 1 `controls_mismatch` | 2 `baseline_nonzero` |

Only the `[0,1,0]` / `[1,0,0]` rows change between readings. Exit code differs (2 vs 1) for them, so an exit-only consumer will see a different verdict.

## Findings (ordered by severity)

### HIGH — H1. Unstated precedence between `baseline_nonzero` and `controls_mismatch`
`[0,1,0]` triggers two unconditional rules (contract: "any nonzero baseline" and "any output/exit disagreement"). The contract does not rank them. Under the implicit reading, the answer is exit 2 vs exit 1 for the same observation.
- Support for (A) baseline dominates [INFERENCE]: the word "any" is unconditional on both rules; `mutate-and-run.sh:63-64` ranks a red control above any attribution verdict ("a red control exits 2 (kills could not be attributed)"); a disagreement verdict about a control whose runs are not all pristine-green is not a well-defined claim.
- Support for (B) mismatch dominates: disagreement is positive evidence of nondeterminism, which is the gate's reason to exist.
- Risk if unresolved: implementer picks one silently; SKILL registry row and L1 verdict will encode whichever. **Requires an L1 ruling written into the contract before the selftest is authored.**

### HIGH — H2. Selftest and snapshot fixtures can pin the wrong precedence without anyone noticing
Any fixture for `[0,1,0]` will assert whichever ID the implementer chose; the selftest then "passes" by construction. The ruling in H1 must be pinned as a named selftest arm, and the `--snapshot` expected-ID file must be generated from the ruling, not from observed gate output (otherwise snapshot validation is circular).

### MEDIUM — M1. `command_unavailable` trigger is unspecified
Questions the contract does not answer:
1. Is it a pre-flight `which`-style check, or a `FileNotFoundError`/`PermissionError`/`IsADirectoryError` at `Popen` on run 1?
2. On run 1 failure, are runs 2–3 skipped? The contract requires "numbered stdout/stderr and exit" saved; for a run that never executed, what files are written?
3. Exec failure on run 2 or 3 only (after a 0 on run 1), e.g. `[0,UNAVAIL,0]`: ID is `command_unavailable` by name, but does it dominate `controls_mismatch` if run 2 and 3 disagree? Recommendation [INFERENCE]: yes — exec failure is infrastructure, not control evidence.
4. Shebang interpreter absent: `execve` returns ENOENT, Python raises `FileNotFoundError` identically to a missing binary. Should be `command_unavailable`, but the message will name the script, not the interpreter. Document.
Exit code 2 is shared with `baseline_nonzero`, so an exit-only consumer cannot tell these apart; the ID is the only discriminator.

### MEDIUM — M2. Child exit 126/127 mapping divergence from fleet precedent
`mutate-and-run.sh:33,57-58` maps 124/126/127 to INCONCLUSIVE because it runs suites via `bash -c` (126/127 = "not runnable" from the shell). The new contract is argv-exec with no shell. A child that itself returns 127 is a nonzero child exit → `baseline_nonzero` under the contract. If an implementer copies the fleet mapping, a script that exits 127 becomes `command_unavailable`, which conflates a real child exit with an exec failure. Both are exit 2, but the ID lies. **Contract should state: command_unavailable is determined by the exec failure only, never by child exit code.**

### MEDIUM — M3. Usage-error ID undefined; `--out` behavior unspecified
- Only the exit code 64 is given for invalid usage. A stable ID (e.g. `invalid_usage`) is needed for parity with the other IDs; the contract lists five named IDs, not six.
- `--out DIR` already existing and non-empty: contract silent. Overwrite would clobber evidence; refusal is usage (64) or setup (2)? Pick one; the fleet tool uses 2 for setup/refusal and 64 for usage.
- `--runs` values 0, 1, 2 (contract says N>=3) and non-integer values: contract says invalid usage implicitly; should be stated.

### MEDIUM — M4. Child signal termination
A child killed by a signal yields a negative `returncode` in Python. Under the contract that is nonzero → `baseline_nonzero`. Acceptable, but must be stated, and the implementation must never propagate the child's raw code as the gate's exit (a child exit of 1 or 2 would otherwise collide with `controls_mismatch` / `baseline_nonzero`). Exit codes must come only from the gate's own map.

### LOW — L1. Stderr counts as "output" only by the explicit enumeration
"any output/exit disagreement" alone could be read as stdout-only. The explicit "identical exit/stdout/stderr required" resolves it to include stderr. The `[0,0,0]` stderr case therefore depends on that enumeration; the contract should say "output (stdout and stderr)" in one place.

### LOW — L2. Reference-run choice is immaterial
Equality is an equivalence relation, so comparing each run to run 1 is equivalent to pairwise all-equal. No ambiguity in the verdict; mention only so the implementer does not invent a "reference = last run" rule.

### LOW — L3. Overclaim surface
`controls_match` must not be recorded in SKILL/LOG as determinism or flakiness-cured. Three identical runs is a sample of three. Contract already says "no flakiness cured or determinism proven"; the registry row should carry that wording next to the ID.

### OUT OF SCOPE (noted, not reviewed)
- Timeouts/hangs: contract has no timeout. A hanging child hangs the gate; no ID covers it. Route to the design-boundary review seat, not this one.

## Ambiguity report (consolidated)

1. **(H1)** `baseline_nonzero` vs `controls_mismatch` precedence — unresolved; blocks `[0,1,0]` and `[1,0,0]`.
2. **(M1)** command_unavailable trigger point, short-circuit, and per-run artifact contents — unresolved.
3. **(M3)** usage-error ID and `--out`-exists behavior — unresolved.
4. **(M2)** 126/127 mapping — contract should forbid shell-style mapping explicitly.
5. "Baseline" = any run vs run 1 — the `[0,1,0]`/`[1,0,0]` rows depend on this; contract says "any nonzero baseline", which supports any-run; confirm in ruling.

## Exact owned paths

- Written: `.ufo/waves/round-12/w1/ExitReview.md` (this file only).
- Not written: no evidence directory created (`.ufo/evidence/round-12/ExitReview/` not needed; no probes executed). No edits to `tools/`, `corpus/`, `LOG.md`, `SKILL.md`, or any sibling seat.

## Verification gaps

- Implementation absent: no code path, selftest, or snapshot was inspected. Every ID/exit above is a contract-derived expectation, not an observed result.
- No gate execution, no fixture run, no determinism claim.
- L1 requested checks after the implementation lands: (a) the `[0,1,0]` ruling pinned as a named selftest arm; (b) `[1,1,1]`, `[0,0,0]`-stderr, and command-unavailable arms; (c) a grep-level check that no path maps child exit 126/127 to `command_unavailable`; (d) usage ID defined.

## Residual risk

- Highest: H1. If L1 does not rule it, two independent implementers will produce different exits for the same observation, and both will pass their own selftests.
## Addendum — L1 ruling (disagreement first) and ControlThreats counterexample

- Ruling adopted (Main, L1): compare exit/stdout/stderr tuples before the baseline check. This supersedes the reading-A row for `[1,0,0]` in the table above: it is `controls_mismatch`/1, not `baseline_nonzero`/2. `[0,1,0]` stays `controls_mismatch`/1; identical `[1,1,1]` stays `baseline_nonzero`/2.
- Why nonzero-first makes exit disagreement unreachable: two distinct integers cannot both be 0, so any exit disagreement already contains a nonzero exit. Under nonzero-first, `controls_mismatch` could then fire only from output differences with exits `[0,0,0]`. Disagreement-first is the only reading in which "any output/exit disagreement fails" has its own reachable path.
- Measured fixture (`.ufo/evidence/round-12/ControlThreats/probes.out:14-15`): cold-first-run exits `[1,0,0]`, stdout `cold/warm/warm`. Disagreement-first → `controls_mismatch`/1. Run-1-only baseline → `baseline_nonzero`/2.
- New limitation: the same child, invoked again after its state is warm, gives identical `[0,0,0]` triples and therefore `controls_match`/0 (`probes.out:16`). A pass is conditional on the child's prior state. It is not evidence of statelessness or determinism. The contract should say so beside the `controls_match` ID.
- Verification gap unchanged: the gate is still absent from the tree; no observed IDs exist yet.
