## Replay29 — `measure-round18-selftest` (R23 C1 falsification, read-only)

**Axes:** A1 frozen-contract fidelity/provenance · A2 retained-evidence presence & freshness · A3 C1 binding discrimination (false-accept surface) · A4 source-read vs command execution separation.

### Verdict
- **Static exact binding: confirmed** for argv/expect against the base revision's tracked registry and against the receipt.
- **Actual evidence present, not inferred:** full 3467-byte stdout, not a tail; receipt == observation; fresh run, not a historical retrofill (proved below).
- **One field-level acceptance boundary:** the gate accepts `stdout` as a declaration with no run-identity or content binding; a demonstrably different historical stdout passes. Concrete adversarial delta supplied.
- **No false acceptance in the delivered row evidence itself.** Producer authentication and historical metadata retrofill are rejected; source-read is not execution.

### Frozen row (base `28cae179`)
```
argv  ["python3", ".ufo/evidence/round-18/measure.py", "--selftest"]
expect {"exit": 0, "stdout_contains": ["MEASURE_SELFTEST: "]}
```
- Read-only zlib parse of git objects (no `git` process spawned): base commit `28cae179…` tree → `tools/registry.json` blob `9315c7e8…`; its bytes are **byte-identical** to `.ufo/evidence/round-23/registry-baseline.json`, and sha256 = `ebd2e69a…` = frozen `registry_sha256`. Active-row projection equals `requirements.json` exactly (43 rows). The digest is therefore a real base-revision anchor, not a self-declared copy.
- Row `source` `SKILL.md@58e5d53:1923-1932` verified from that commit's own blob: line 1932 is this row ("as round 17"), and the round-17 row (line 1901) is the explicit `--selftest` command. The source itself says this probe "binds credit to recorded inputs, not to the commands a bucket requires — **never cite it as command coverage**."

### Actual retained invocation
- Receipt (bundle sha256 `3d6c99b7…`): argv exact, cwd `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` = bundle cwd, revision `496d212…` = bundle rev, exit 0, stderr `""`, stdout 3467 B.
- Complete, not a tail: `stdout == stdout_tail` (3467 B) and both < `TAIL_BYTES` 4096; 123 lines, **98 `PASS ` lines**, one token occurrence, final line `MEASURE_SELFTEST: 98/98 pass (scratch /tmp/tameshi-r17-MeasureV2-kwa2esv8)`.
- Interval 14:44:49.365302→52.728204 (3.3629 s) matches `elapsed_s` 3.363; latest row action 14:44:52.7, before the 14:44:58 replay end.
- Bundle stdout is byte-identical to the observations stdout; embedded requirement equals the frozen row.
- Revision provenance is benign here: `496d212` is an ancestor of the frozen delivered `336565f` (depth 2: `336565f → 8f66b5d → 496d212`); blobs for `measure.py` (`9643f70…`), `command-binding.py` (`23eab57…`), `registry-check.py` (`08ac9cd…`), `replay.py` (`b14e13c…`) are identical at both, and the live worktree (HEAD `336565f`) recomputes to the same blob ids.

### Freshness (rejecting retrofill) — proven out-of-band
The selftest emits two per-run nondeterministic values: the `mkdtemp(prefix='tameshi-r17-MeasureV2-')` suffix (measure.py:886) and a synthetic fixture commit in `PASS revision-40hex <sha>` (measure.py:1433-1437).
- Fresh values `kwa2esv8` / `69335f67…` occur in **no** earlier artifact; scanning all `.ufo/evidence` files containing `MEASURE_SELFTEST: 98/98` (19 artifacts) found 19 distinct scratch suffixes and distinct fixture SHAs, none equal, and the fresh 3467-byte stream is not a contained substring of any.
- The later 336565f monitor run (`registry-C`, 14:48-14:50) produced a normalized-equal 3467-byte stream differing only in those two fields (`o7xhzjvm` / `3003d44f…`), i.e. independent reruns, not copies.
- Do **not** read `revision-40hex 69335f…` as the repo/bundle revision; it is a fixture SHA and attests nothing about `496d212`/`336565f`.

### Field-level false acceptance (A3)
`command-binding.evaluate` (lines 109-112) only requires `expect.exit` equality and literal substring containment in the producer-supplied `stdout`; it never binds completeness, run identity, case integrity, stderr, or command-target content. For this row, replacing the receipt `stdout` with the **already-retained round-18 historical stream** `.ufo/evidence/round-18/final/measure-selftest.stdout` (3566 B, 121 lines, nested scratch `.../round-18-L1-final-a2vitd82/tmp/tameshi-r17-MeasureV2-kofgxugi`, fixture `4b03e7f…`) leaves argv/cwd/revision/exit unchanged, still contains `MEASURE_SELFTEST: `, and yields `(0, [])` after regenerating `expected.json`. A 17-byte stub `"MEASURE_SELFTEST: "` with exit 0 does the same. So "full output, not tails" is an auditor criterion, not a gate predicate; freshness was established only by the out-of-band nondeterminism diff above.

**Concrete adversarial delta:** receipt `stdout` ← `round-18/final/measure-selftest.stdout` bytes (or token-only stub), `exit:0`, argv/cwd/revision untouched, `expected.json` recomputed → gate exit 0 / `finding_ids: []`. Static trace of `evaluate`; I did not execute the gate on the mutant (wave restriction). Not present in the delivered replay.

### Contradictions / rejected claims
- `observations.runner_sha256` (`cba166…`) is hashed from `args.repo/tools/registry-check.py` (live `336565f`), not the executed clone; here the blob is identical at both revisions, so the value is accidentally accurate but not execution-derived.
- `revision` is compiler-stamped; no output field attests it for this row. The clone checkout plus identical blob ids is the real link.
- `replay-gate-A` exit 0 / `[]` proves declaration consistency on the producer-supplied digest; it is **not** producer authentication.
- `source-read-gate-A` (exit 1, `ARGV_MISMATCH`) correctly refuses source-read credit. This row gives no command-coverage/credit closure (per its own source note); do not claim R17-CMD-BIND or bucket coverage from it.

### Proposed move (one, bounded — A2, composes with sibling token-integrity proposals)
In the **replay compiler** (not the frozen gate), extract per-row run-witness tokens from stdout — here the `tameshi-r17-MeasureV2-<suffix>` and `revision-40hex <sha>` — record `stdout_sha256` + witnesses in the observation, and fail the replay if those witnesses equal the previous retained run of the same row (optionally: appear in prior evidence). This makes freshness a recorded, checkable fact instead of an auditor's diff, adds no gate-schema change, and remains honestly non-authenticating (it detects copy/retrofill, not a determined forger).
**Risks:** forgeable by a producer who fabricates unique tokens; deterministic rows need an allowlist; previous-run comparison requires retaining the prior observation; no help for rows whose output has no unique token.
**Verification:** predicate holds for this row (fresh `kwa2esv8`/`69335f…` absent corpus-wide; prior run `o7xhzjvm`/`3003d44f…`), and the stale round-18 stream would be flagged.

**Report-write conflict:** the seat target says write `.ufo/waves/round-23/w2/Replay29.md`, but the authoritative wave context says read-only, "DO NOT WRITE ANY FILE", and "this wave forbids report writes" (L1 persists). I wrote nothing; this message is the report payload.

**Tooling:** none installed or upgraded. No registry command, suite, build, test, or formatter was run; checks were file reads, JSON diffs, sha256, and read-only zlib parsing of loose git objects.
