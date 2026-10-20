# Registry — round-15 active gate registry and exit-class correction

Seat: `TameshiR15.Registry` (executor, leaf; SKILL.md owner for this wave).
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Read revision: `a9cf4da78f2514c7bedd91a850a88590009d7df0` plus the wave's
untracked round-15 working files. Status: **contract/registry only; nothing
executed.** No gate, selftest, probe, `--check`, build, lint or formatter was
run. Tool installs/updates: none.

## Axes named

- **calibration (C1, primary):** correct the routed classification and exit
  classes so the context instrument's verdict behavior is registered as a gate
  with a standalone self-invocation and explicit could-not-evaluate codes.
  This is a capability/conformance edit; no scalar change is claimed (6→6).
- **operability:** exact active entry command, expected-pin schema, self-test
  command, and four-class verdict map are now readable without reading code.
- **preservation:** archived round-14 script and every round-12–14 receipt stay
  byte-identical; the new active command is `tools/context-capture.py`.
- **not moved:** depth, coverage, freshness and adjacency. No successor sweep,
  no seventh mutation case, no sibling-gate execution, no new live-capture
  capability.

## Files changed by this seat

| Path | Change |
|---|---|
| `SKILL.md` | Appended the round-15 section at EOF (lines 1609–1691 at this write). No historical sentence deleted; `git diff --numstat -- SKILL.md` reports `86 1`, where the single removed line is the prior final line re-added byte-identically with the required trailing newline. |
| `.ufo/waves/round-15/w1/Registry.md` | This report. |

I did not edit `tools/context-capture.py`, `corpus/SOURCES.md`, `QUALITY.md`,
`LOG.md`, `SCORECARD.md`, `SHONEN.md`, or any historical evidence.

## Evidence chain

### Routed defect being corrected

- `corpus/lessons/round-14-verifier-spotcheck.md:160` (Routed defects item 5):
  `capture-context.py` compares runner/probe digests and mappings against
  persisted `expected.json`/`pin-manifest` values and `decide()` emits
  mismatch/exit1, so it is a gate; it lacks a standalone isolated
  self-invocation with exits and stable finding IDs; its exit64 is absent from
  the registry, and C1's disposition row labelled 64 only as "usage".
- `corpus/lessons/round-15.md:31-33` admit criteria: public CLI selftest over
  isolated fixtures asserting literal exit and stable finding pairs;
  digest-checked persisted snapshot bytes; every nonzero class named.
  `:45-46` records the two mistakes: gate-misclassification and
  exit-class-ambiguity, both repaired by the maintained tool plus registry.
- `PROTOCOL.md` §Gate standard: `0` clean, `1` failed fleet-wide; every other
  code is declared and mapped onto `clean|failed|could-not-evaluate`; a
  self-test asserts exit and a stable finding ID; an edited snapshot is
  `snapshot_tampered` (could-not-evaluate), not a compared verdict.

### Historical source (read-only; never executed by this seat)

- `.ufo/evidence/round-14/capture-context.py`, sha256
  `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`
  (measured with `sha256sum`; unchanged).
- Its contract: `:2-31` scope; `decide()` `:553-580` returns ok/0 or
  mismatch/1 over persisted expectations; `main()` `:605-643` maps invalid
  input to 2 and unexpected argv to 64. This is verdict behavior over
  persisted expectations, hence a gate under the standard.
- Retained clean receipt `.ufo/evidence/round-14/context-receipt.json`,
  sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`.
- Retained negative fixture `.ufo/evidence/round-14/context-missing-env.json`,
  sha256 `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`;
  it lacks `environment.injected_env` while stored flags still say ok/0, which
  is exactly why the maintained check re-derives facts instead of trusting
  summary booleans. Round-14 `guardrails.json` already pins the literal
  `missing_injected_environment`/exit1 pair for this fixture.

### Maintained tool contract (source read, not run)

`tools/context-capture.py` (owner: ContextGate). Latest observed read:
sha256 `0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc`,
85,159 B, mtime 2026-10-20 05:16:51 -03:00. The owner edited it repeatedly
during this wave (`533b826f…` → `7fa11363…` → `e2b6d07e…` → `a15b9585…` →
`90151305…` → `0ed784e0…`); the registered flags, expected-pin schema, frozen
digest and stable IDs were identical across those reads. The file is owned by
another live seat and may still change; L1 should re-hash and re-read `--help`
before running.

- USAGE (`:249-275`): `--check [--receipt FILE --expected FILE] [--json]` and
  `--selftest`.
- Frozen default: `--check` alone replays
  `.ufo/evidence/round-14/context-receipt.json` against the built-in pin
  sha256 `05cb55b8…9c1a`, id `context_consistent`, exit0
  (`:133-141`, `:1278-1290`).
- Explicit mode: `--receipt` and `--expected` are required together
  (`:2018-2020`); the expected file is schema `tameshi-context-expected-v1`
  with exactly `receipt_sha256`, `id`, `exit` (`:31-35`, `:123-125`).
- Stable IDs in the module docstring (`:57-85`) include
  `context_consistent` (0), `missing_injected_environment`,
  `comparison_mismatch`, `mapping_mismatch`, `receipt_verdict_mismatch`,
  `expected_verdict_mismatch` (1), `receipt_json_invalid`,
  `receipt_structure_invalid`, `snapshot_tampered`, `expected_invalid` (2),
  `usage_error` (64).
- Selftest dispatches the real CLI through subprocesses under
  `tempfile.mkdtemp()`, pins literal ids/exits (`:1584`, `:1700-1930`), and
  prints `SELFTEST: PASS (n/n)` / exit0 or `SELFTEST: FAIL` / exit1
  (`:1694-1698`). Its fixtures are synthetic; it reads no live lane path.
- The owner (ContextGate) confirmed this same contract by message during the
  wave: `--check` frozen pin `context_consistent`/0; `--check --receipt FILE
  --expected FILE` with both flags or neither (one alone is `usage_error`/64);
  `--selftest` runs real CLI subprocesses on `mkdtemp` fixtures with 38
  declared checks (31 receipt fixtures, 5 usage, 2 hermetic meta); no capture
  mode; noarg and unknown args are `usage_error`/64 with no files written.
  These are declarations, not results executed by this seat.
- The tool never captures, never opens a recorded root, never executes
  retained argv and writes nothing in check mode (docstring `:11-24`,
  USAGE). The archived script is not imported.

## Registry rows as written (SKILL.md §Round-15 gate/probe registry)

Context row (active path, kind `gate`):

- entry: `python3 tools/context-capture.py --check` (frozen clean receipt);
  `--check --receipt FILE --expected FILE` for a caller-pinned retained receipt.
- verdict: `0` clean (`context_consistent`); `1` failed stable finding ID
  (e.g. `missing_injected_environment`); `2` and `64` could-not-evaluate
  (missing/malformed/tampered receipt or expected pin, e.g.
  `snapshot_tampered`; `64 usage_error`).
- self-test: `python3 tools/context-capture.py --selftest`.
- pinned: frozen clean receipt path/digest and built-in id/exit in tool;
  expected-pin schema `tameshi-context-expected-v1` for other retained
  receipts; negative fixture digest; literal selftest pairs in tool.
- write scope: check reads receipt bytes only and writes nothing; selftest is
  isolated temp fixtures; round-14 script/receipts byte-retained.

Disposition row (restated so 64 is explicit):

- entry: `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`.
- verdict: `0` clean; `1` failed semantic expectations; `2` and `64`
  could-not-evaluate (invalid/missing/tampered inputs; `64` usage).
- self-test: `python3 tools/evidence-disposition.py --selftest`.

The round-14 registry rows remain unedited. The old
`invocation context capture | probe` row and recipe step 5 (`SKILL.md:1592-1595`,
`:1602`) are explicitly superseded by the new section as archived guidance;
they are not deleted or rewritten. The historical `capture-context.py` row is
therefore still discoverable as a probe archive, while the active path has
`gate` and zero active `probe` rows — `measure.py` counts those separately.

## Before → after (structural, not runtime)

| Observable in SKILL.md | Before | After |
|---|---|---|
| Active context instrument kind | `probe` | `gate` |
| Active context entry | archived round-14 noarg capture | `tools/context-capture.py --check` (+ explicit pin form) |
| Standalone context self-test | `no standalone selftest` | `--selftest` entry recorded |
| Context 64 class | absent | `2 and 64 could-not-evaluate` (64 usage) |
| Disposition 64 class | `64 usage` only | `2 and 64 could-not-evaluate` (64 usage) |
| Round-14 archive status | active-looking recipe step 5 / probe row | retained as archive, explicitly superseded |

No runtime result is claimed. Selftest green, check exits, and the tool's
current bytes are capability declarations owned by L1's single post-wave run.

## Limits and non-claims

- A clean `--check` proves the retained receipt's recorded and re-derived facts
  under its pinned digest; it does **not** re-execute stored argv, prove
  author authenticity, or establish general environment independence, suite
  identity, result reuse or concurrent sibling stability.
- The single `GIT_DIR` injection and six static runner mappings remain the
  whole historical scope; round-13's undocumented setup is not retroactively
  repaired.
- Selftest green is capability, not a measurement, and this seat did not run
  it. Same-wave reviews are advisory, not outside admission.
- No new live capture is implemented or claimed: the active command is a
  retained-receipt gate. The historical noarg capture remains archived only.
- `corpus/SOURCES.md` had no `S051` row at this write (last "Next unused id:
  S051"). The section cites `corpus/lessons/round-15.md` and states that the
  own-work row is opened only after the maintained tool exists; it does not
  cite a nonexistent row. If L1 opens that row before commit, the lesson's
  own text is the citation anchor; no runtime result is implied.

## Bounded recommendations for L1 (not executed here)

1. After ContextGate finishes, re-read `--help` and confirm it still matches
   the registered flags; re-hash the tool (latest observed at this report:
   `0ed784e0…61edc`).
2. Run once: `python3 tools/context-capture.py --selftest`; expect exit0 and
   the tool's own `SELFTEST: PASS (n/n)` line. Record the observed n; do not
   take it from this report.
3. Run once: `python3 tools/context-capture.py --check`; expect exit0 and
   `context_consistent`.
4. Optional committed discriminating replay (recommended by the frozen-evidence
   advice): write an expected pin (a path is L1's choice, e.g.
   `.ufo/evidence/round-15/context-missing-env.expected.json`) with exactly

   ```json
   {"schema": "tameshi-context-expected-v1",
    "receipt_sha256": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
    "id": "missing_injected_environment",
    "exit": 1}
   ```

   then run
   `python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected <that pin>`;
   expect exit1 with `missing_injected_environment`. Do not rewrite the round-14
   fixture; the expected file is new round-15 input.
5. Preserve round-12–14 bytes; do not run sibling gates; keep the historical
   rows as archive.

## Risks / open items

- **Concurrent owner edit:** the tool changed several times while I read
  (`533b826f…` → `7fa11363…` → `e2b6d07e…`). The registered flags/IDs match the
  `e2b6d07e…` read; if a later edit changes `usage:` or a registered ID, the row
  must be corrected before gate execution. This is the one implementation-
  critical dependency.
- **Negative replay needs the expected pin:** `--receipt` without `--expected`
  is a usage/64 path by design, not a negative verdict. Item 4 above supplies
  the pin; without it, the negative fixture is not a committed gate run.
- **`--help` exits 0** and is not a clean verdict; only `--check`/`--selftest`
  are verdict modes.
- **No S051 row yet:** bounded to citation wording above; not a claim that the
  source acquisition did not happen.
