# R23 Re-attack Replay08 — exact row `witness-metadata-check`

Verdict up front: **AGREE** — the attacked binding holds. Static exact binding is
confirmed for every field the frozen contract declares; the retained invocation
metadata and full output are actually present, not inferred; the row is NOT
superseded at lane revision c9ff09f. One concrete adversarial delta exists at the
contract boundary (cross-field receipt consistency is unbound) and is demonstrated
below; it does not make the retained round-23 evidence wrong.

## 1. Row identity and baseline-source comparison

Frozen requirement (`.ufo/evidence/round-23/requirements.json:96-116`, schema
`command-binding-requirements-v1`, `source_revision` 28cae179):

- argv: `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json`
- expect: `{exit: 0, stdout_contains: ["metadata_consistent"]}`

Baseline source: `.ufo/evidence/round-23/registry-baseline.json:152-165` carries the
same argv/expect with `kind: gate`, `status: active`, `tags: [baseline]`,
`timeout_s: 60`, `source: SKILL.md@98bea7d:1553`. The file's sha256 equals the
`registry_sha256` pinned in requirements.json (verified: `ebd2e69a…fec92a`), so the
frozen projection is digest-anchored to the baseline source, and the projection
dropping `kind/timeout_s/source/tags` is the declared `command-binding-requirements-v1`
shape (exactly `{name, argv, expect}`), not drift. `.ufo/evidence/round-23/replay.py:36-39`
additionally asserts frozen requirements == active source rows at run time.

## 2. Retained invocation metadata and full output — present, not inferred

For the `witness-metadata-check` row only:

- `replay/bundle.json:96-114` receipt: argv equal to frozen; `cwd`
  `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`; `revision`
  `496d212bc46789cdf8cafab72978bdb7f4182963`; `exit` 0; `stderr` `""`; `stdout`
  `WITNESS_METADATA: metadata_consistent reason=ok exit=0
  companion=/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json
  inputs=summary,declaration,declared,rerun_summary\n` — a complete single-line
  stream ending in `\n`, not a tail.
- `replay/observations.json:318-376`: same row with `measurement_interval`
  14:42:25.112708→14:42:25.211548 UTC (2026-10-21), `elapsed_s` 0.099 (interval and
  elapsed agree), embedded `requirement` byte-equal to the frozen row, and
  `runner_result` retaining both `stdout` and `stdout_tail` — verified identical
  strings (`stdout == stdout_tail`, `bundle stdout == observations stdout`,
  `stderr` empty in all three places).
- Cross-field consistency in the actual evidence: receipt `cwd` == bundle `cwd`;
  receipt `revision` == bundle `revision`; the `companion=` path in stdout is
  exactly `cwd + argv's relative companion`.
- `observations.json` `runner_sha256` `cba1664…44ad` == sha256 of
  `tools/registry-check.py` blob at revision 496d212 (recomputed), so the retained
  runner identity matches the replayed revision.
- I re-ran the read-only validator from /tmp scratch on the frozen pair:
  `python3 tools/command-binding.py --bundle bundle.json --expected expected.json
  --json` → `{"exit": 0, "finding_ids": []}`, `bundle_sha256 3d6c99b7…50b9`; the
  on-disk `expected.json` digest-pins those exact bytes (no tamper).

## 3. Static exact binding — confirmed

`tools/command-binding.py` `evaluate()` (unchanged 496d212→c9ff09f; the only
inter-revision diff is selftest fixture paths, verified by `git diff`):

- name membership exact both directions (`MEMBERSHIP_MISMATCH`), duplicates
  rejected (`DUPLICATE_COMMAND`, `DUPLICATE_REQUIREMENT`);
- argv: exact list equality, no shell normalization (`ARGV_MISMATCH`);
- cwd: canonical-absolute, per-receipt equality with bundle cwd (`CWD_MISMATCH`);
- revision: full 40-hex, per-receipt equality with bundle revision
  (`REVISION_MISMATCH`);
- exit: exact int equality, bool rejected (`EXIT_MISMATCH` / `INVALID_RECEIPT`);
- stdout: token check scans the FULL `stdout` string, never `stdout_tail`, and
  stderr can never supply a token (selftest case `stderr-cannot-supply-token`);
- fail-closed shapes: strict key sets (no extra fields), duplicate JSON keys and
  nonfinite constants rejected, whole-file sha256 pinned by `expected.json`
  (`SNAPSHOT_TAMPERED`).

No declared field is compared loosely, so there is no field-level false acceptance
in the frozen row.

## 4. One concrete adversarial delta

`stdout_contains` is token-membership in an otherwise-unbound free-text field, and
nothing cross-binds receipt fields against each other. Demonstration (my /tmp
scratch, validator run read-only): I took the frozen bundle and changed only the
receipt's stdout `companion=` path to `/tmp/forged/witness-metadata.json` while the
receipt argv still declared
`.ufo/evidence/round-13/witness-metadata.json` (token `metadata_consistent` kept).
Re-pinned `expected.json` to the mutated bytes; `command-binding.py` returned
`exit 0, finding_ids []`. So the binding accepts a receipt whose own stdout
testifies a different companion was read than the argv declares; stderr is likewise
validated as a string but never compared (the expect schema permits only
`exit`/`stdout_contains`), and the baseline row's `timeout_s: 60` is dropped by the
projection, so timeout compliance is inferred from runner code, never retained.
This is the adversarial surface the original item asked to name. It sits at the
tool's declared boundary ("validates retained declarations, not their producer
authenticity" — command-binding.py docstring), and the actual round-23 receipt does
not exploit it: every cross-field relation in section 2 checks out.

## 5. Producer authentication and retrofill — rejected

My verdict rests on retained bytes, digest cross-checks and code reading only; no
author claim or producer identity is trusted, and the tool itself disclaims
producer authenticity. Retrofill is excluded for the audited horizon: the companion
`.ufo/evidence/round-13/witness-metadata.json` is blob-identical (`c03a6133…26581`)
at 496d212 and at c9ff09f; the three replay evidence files at HEAD are
blob-identical to 54c14ea, the first commit touching them (authored 2026-10-21
11:46 -03, one minute after the recorded run end 14:44:58 UTC; only 54c14ea and
8f66b5d ever touched them). The gate itself anchors source bytes via constants in
`tools/witness-metadata.py` (`PINNED_BY_NAME`, `RERUN_SUMMARY_SHA256`,
`HISTORICAL_RUNNER_SHA256`), so companion digests must equal constant-pinned actual
files; the stdout `inputs=` list matches the tool's `ALL_PINNED` construction
(witness-metadata.py:363-365, 631, 640-647).

## 6. Currency at lane revision c9ff09f

- Registry row: byte-identical at 496d212, c9ff09f, and the working tree — NOT
  superseded (`tools/registry.json`, `status: active`).
- `tools/witness-metadata.py`: sha256 `df33906…0bed4` at both revisions (unchanged).
- `tools/command-binding.py`: `evaluate()` unchanged; only selftest fixture loading
  gained round-24 cases.
- c9ff09f is an ancestor of current HEAD 5b69fb2; the three audited files are
  identical between c9ff09f and HEAD.

The finding therefore still applies at c9ff09f in the same form.

## 7. Residual risk and verification gaps

- I did not execute the gate row itself (original item forbids running the registry
  command), so the green state is evidenced by retained streams plus validator
  re-run, not by an independent fresh execution; that residual is inherent to the
  retained-declaration contract.
- Producer authenticity of the 2026-10-21 run remains unprovable from artifacts
  (declared out of scope by the tool); only contemporaneity (commit minutes after
  the measured interval) and internal consistency are established.
- The mutated-bundle demonstration edits evidence bytes by construction; it shows a
  binding-schema gap, not anything that happened historically.

R23-REATTACK Replay08: AGREE
