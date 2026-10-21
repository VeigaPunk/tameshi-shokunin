**Scope / non-actions.** Read-only. I wrote no file (the target `Report:` path was not written: this wave's read-only rule and the ticket's "no repo writes" override it; L1 persists this text). I ran no registry command, gate, suite, build, formatter, git, or subagent — only read-only file/JSON/hash/stat inspection. `R17-CMD-BIND` is **not** claimed closed.

## Row audit — `sources-census`

**Frozen declaration vs baseline source: identical.**
- `requirements.json:337-346` → argv `["bash",".ufo/evidence/kaika-round-1/sources-census-v2.sh"]`, expect `{exit:0, stdout_contains:["SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)"]}`.
- `registry-baseline.json:570-585` → same argv/expect; only extras dropped (`kind=gate`, `source=SCORECARD.md@98bea7d:240`, `status=active`, `tags=[baseline]`, `timeout_s=60`). `requirements.json` pins the baseline by digest: `ebd2e6…` **equals** computed sha256 of `registry-baseline.json` (verified).
- Bundle requirement is byte-equal to the frozen row; exactly one requirement and one receipt with that name in 43/43.

**Receipt fields (declared binding): exact.**
- `replay/bundle.json:318-342`: argv byte-equal, `cwd` == bundle cwd `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`, `revision` == bundle revision `496d212…`, `exit=0` == expect, `stderr=""`.
- Full stdout **actually present, not a tail**: 1863 bytes / 41 lines; `stdout_tail` == full stdout for this row (12 of 43 rows have 4096-byte tails; this one does not). `observations.json` `runner_result.stdout` is byte-identical, and all 43 bundle receipts equal their observation streams.
- Token occurs **once**, at offset 1811 (line 40, final verdict line). Timing is coherent: interval delta 0.130973 s vs `elapsed_s=0.131`, nested in the replay window; `replay-gate-A.json` (exit 0, findings `[]`) ran 23 s later and its `bundle_sha256=3d6c99…` equals `expected.json` and the computed bundle digest.

**Cross-run corroboration.** `registry-C.json` (independent 336565f run, `held=46/46`, 4 superseded) retains a `sources-census` `stdout_tail` of 1863 bytes that is **byte-identical** to the replay receipt (cwd/argv/revision differ). `monitor-current-C.json` (round-21/coldread `measure.py`, 336565f, exit 0) independently reports `rows=81, malformed=0, A=72 B=7 C=2, mined=52 queued=23 rejected=6`, matching the receipt's Part A exactly. Static read of the script confirms CLEAN is emitted only under `bad=0` and exit is `$bad`, so token+exit 0 are coupled to the script's checks.

## One field-level false acceptance (F1)

`expect.stdout_contains` is containment over a producer-supplied string, and this row's witness token is a **source literal**: it appears verbatim in the executed script (`sources-census-v2.sh:20`) and in a committed prior output (`kaika-round-1/sources-census-v2.txt:41`). The gate separates source-read *argv*, never source-read *content*.

First-party demonstration already in the round: in `source-read-bundle.json` the requirement is `python3 tools/receipt-measure.py --selftest` with token `RECEIPT_MEASURE_SELFTEST: 10/10 pass`; the receipt is `cat tools/registry.json`, whose stdout **contains that token** (registry.json declares its own expected token). Exit/cwd/revision all matched; `source-read-gate-A.json` reports **only `ARGV_MISMATCH`** — the stdout axis was satisfied by a pure source read. So `missing-stdout-token` is not an execution witness; `argv-mismatch` is the sole discriminator, and argv is itself a declared string.

## Concrete adversarial delta (D1)

Substitute `.ufo/evidence/kaika-round-1/sources-census-v2.txt` (sha256 `b97f509a…`, 1863 bytes, 41 lines, **44-row** census) into the receipt's `stdout`, keep argv/cwd/revision/exit 0. Static trace of `evaluate()`: argv equal, cwd equal, revision equal, exit 0==0, token present once → no finding → exit 0. Diff against the real 81-row output is only three numeric lines (`44→81`; `A=37 B=5→A=72 B=7`; `mined=12 queued=29 rejected=3→mined=52 queued=23 rejected=6`), and total byte length is **identical (1863)**, so even a length check would not catch it. This is exactly historical metadata retrofill; not executed here, static trace only.

*Adjacent field gap (D2):* the bundle requirement may be weakened to `expect={"exit":0}` — schema-legal (`{'exit'} ⊆ expect ⊆ {'exit','stdout_contains'}`) — and an empty stdout passes, because `command-binding.py` reads only `--bundle` and `--expected` (verified: no reference to `requirements.json`, `registry-baseline`, `registry_sha256`, or `source_revision`; the only file reads are lines 117-118). The bundle's exact key set `{schema,revision,cwd,requirements,receipts}` cannot carry the contract digest or `source_revision=28cae179…`; report revision is `496d212…` ≠ contract source revision ≠ delivered `336565f…`.

## Trust anchor and evidence status

- `bundle.json` and `expected.json` were written **157 µs apart by the same `replay.py` process** (mtime 11:44:58.826544 / .826701), so as delivered `SNAPSHOT_TAMPERED` defends post-hoc edits relative to a self-generated pin, not producer-side fabrication. If a caller pre-pinned `expected.json` before the run, D1 is blocked; no such pre-commitment is evidenced in-repo.
- **Present:** full streams (43/43), this row's bytes, second-run byte equality, cross-instrument corpus counts, gate receipt.
- **Inferred/unverified:** that this receipt's bytes came from executing at `496d212` (producer-declared revision; ephemeral clone deleted); the executed script's blob digest (no digest retained; worktree `b9b754…` is not proven to be the `496d212` blob); the runner module identity — `observations.runner_sha256=cba166…` is hashed from `<live repo>/tools/registry-check.py` (worktree), while the module was imported from the clone, a cross-tree digest; receipt contemporaneity (only mtimes).
- **Rejected as evidence:** producer authentication (no independent signature; self-generated expected) and historical retrofill as proof — and the gate cannot detect retrofill (D1). No retrofill detected *in this row's own fields*.

## Axes (contract population) and effect

- `argv-mismatch`: exact and exercised, but is the only source-read separator → **weakened by F1**.
- `missing-stdout-token`: exact predicate, non-discriminating for source/retrofill → **claim harmed if read as execution evidence**.
- `cwd-mismatch`, `revision-mismatch`, `membership`, `duplicate-command`, `exit-mismatch`, `bool-exit`: exact, no new defect.
- `tampered-bundle`: correct vs `expected.json`, anchor self-generated as delivered.
- **Missing population member:** "correct declared argv + non-execution stdout" has no finding ID, so the measured 10/10 discrimination is closed over the gate's own vocabulary and cannot express this row's central failure. That is the calibration defect, not the 10 case results.

## Proposed move (one, bounded)

**Per-run nonce challenge in the verdict line, argv untouched.** Caller generates a fresh hex nonce *before* the run and holds it in a caller-owned pin; the runner passes it via `row_env()` (no argv change, preserving exact-argv binding); each required command echoes `nonce=<hex>` in its verdict line (for this row: `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path) nonce=<hex>`); the gate requires that exact token. Second-order effects: retrofilled prior `.txt` or script source cannot carry the current nonce → `STDOUT_MISMATCH`; `requirements_sha256` (sha256 of frozen `requirements.json`, required in the bundle) closes D2; cwd/revision/exit semantics unchanged.

**Risks:** touches all 43 frozen scripts (contract churn, re-baseline of requirement digests), so stage echo-lines for all rows before enabling or every non-echoing row fails; the nonce is not a secret and will be logged; if the nonce pin is written by the same process it degenerates into another self-pin; any command that scrubs env loses it.

**Verification (proposed for L1, not run):** replay D1 fixture (prior `.txt`) → expect `STDOUT_MISMATCH`; D2 fixture (exit-only expect) → expect a contract-digest finding or `INVALID_REQUIREMENT`; fresh nonce run → pass; previous-run nonce → fail; confirm argv/cwd/revision/exit case results unchanged.
