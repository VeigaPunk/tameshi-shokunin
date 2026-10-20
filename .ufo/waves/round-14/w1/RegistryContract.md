# RegistryContract — round 14 gate/probe registry row proposal

Lane: tameshi-shokunin. Baseline: `d6809df7775338f000e44c8a916067b8866867fb`.
Status: **contract-only.** `tools/evidence-disposition.py` does not exist yet
(`tools/` holds only the five retained tools). `.ufo/evidence/round-14/`
holds only `claims.json`. `capture-context.py` does not exist. No code was read
for these; every field below is a proposal against the retained contract in
`.ufo/waves/round-14/spec.json` and the retained round-13 receipts.

Scope of this seat: read-only. No shared file edited (SKILL.md, LOG.md,
corpus/README.md, SCORECARD.md, SOURCES.md, QUALITY.md untouched). No gate,
selftest, sibling repo command, or verification was run. The only commands were
file reads, JSON parses of retained receipts, and `sha256sum` of three files.
Tool installs/updates by this seat: none.

## 1. Existing registry pattern (observed)

- `SKILL.md:1499-1501`: `### Gate/probe registry` (round 12), 8 columns:
  `Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner`.
- `SKILL.md:1548-1553`: `### Round-13 gate/probe registry` under
  `## Pin disposition and provenance correction — round 13` (`SKILL.md:1517`).
  Verdict maps use the exit lattice `0 clean / 1 failed / 2 could-not-evaluate`,
  with `64` usage where the tool has it. Selftest is `python3 tools/<tool>.py --selftest`.
  Write scope names the isolated `/tmp/tameshi-r1N-*` or temp-tree selftest.
  Owner is `tameshi`.
- Round-13 rows say "No registry row changes rank, SHONEN authority, or the six
  recorded cases" (`SKILL.md:1555`). Keep that sentence for round 14.

## 2. Proposed row — evidence-disposition gate (exact fields)

Proposed heading (L1 appends, append-only, after `SKILL.md:1561`):

```
## Effective expectation reconciliation — round 14

### Round-14 gate/probe registry
```

Table header is identical to `SKILL.md:1501` / `:1550`.

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| evidence disposition ledger | gate | `python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions.json --json` | 0 clean: all 12 expectation rows effective or superseded and semantically satisfied; 1 failed semantic expectation (finding IDs in stdout JSON); 2 could-not-evaluate: missing, unreadable, schema-invalid, digest-mismatched or tampered input, unsafe path/symlink; 64 usage | `python3 tools/evidence-disposition.py --selftest` | `.ufo/evidence/round-14/dispositions.json` (schema `evidence-dispositions-v1`) pins: `.ufo/evidence/round-13/expected.json` sha256 `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336`; `.ufo/evidence/round-13/verification.json` sha256 `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f`; `.ufo/evidence/round-13/producer-oracle-repair.json` sha256 `df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d`; the 13 `expected.inputs` digests are verified by the gate from `expected.json` before any predicate; literal finding IDs and expected-check names in the tool | normal mode: read-only over lane files; never executes receipt `argv`; writes nothing (stdout JSON only). Selftest: isolated `tempfile.mkdtemp()` fixtures only (`/tmp/tameshi-r14-*`), removed in `finally`; invokes own CLI via subprocess | tameshi |

Notes on the row:
- Expected-file and receipt digests above are current committed bytes observed by
  this seat via `sha256sum` (no gate run). They match the round-13 closure's
  "13 inputs; mismatches=[]" statement only for the three files named here; the
  other ten `expected.inputs` digests were not re-hashed by this seat.
- The gate's own digest is not yet knowable. L1 records `sha256sum tools/evidence-disposition.py`
  in the round-14 receipt at integration, as round 13 did for the runner
  (`expected.json` input `tools/mutate-and-run.sh` = `75ed934d…`).

### Optional second row (contingent, not required for the gate)

Only if L1 wants the context-capture harness registered, and only after
`capture-context.py` exists and its verdict map is specified by ReceiptHarness:

| six-leg context receipt | probe | `python3 .ufo/evidence/round-14/capture-context.py` | [UNSPECIFIED — ReceiptHarness to define; no harness code exists yet] | none (harness self-checks inside the script; not a gate) | `tools/mutate-and-run.sh` sha256 `75ed934d…`; `tools/pin-disposition.py` sha256 `297253971…`; `.ufo/evidence/round-13/pin-manifest.json` sha256 `64eaa43e…` | writes only `.ufo/evidence/round-14/context-receipt.json`; no sibling execution unless L1 runs it; env injected explicitly (`GIT_DIR=/nonexistent/tameshi-round14-poison`) | tameshi |

Do not register this row until the file exists. A row with an undefined verdict map is a hidden-gate risk.

## 3. Findings and risks against the retained contract

1. **Row-count mismatch — fix before implementation.** The spec says "All13
   expected rows" (`spec.json` Interfaces). `.ufo/evidence/round-13/expected.json`
   has **12** `expected_checks` keys: pin_selftest, metadata_selftest,
   metadata_old_null, metadata_corrected, producer_before, producer_before_oracle,
   producer_after_oracle, producer_after, witness_check, witness_count, pin_live,
   source_census. The "13" matches `expected.inputs` (13 entries) or the 13 checks
   in `verification.json`, not expected rows. Required dispositions: 12 rows, 11
   effective plus `producer_before` superseded in the after file. The gate must
   reject any row count other than 12 as an unexplained/missing row. L1 should
   correct the "All13" phrase in the round-14 record, not in historical files.

2. **Extra receipt checks are not expectation rows.** `verification.json` has 13
   checks; 3 are not in `expected_checks`: `frozen_and_guardrail_unchanged`,
   `pin_env_scrub`, `metadata_emit`. `verification-verdict.json` adds
   `baseline_final_count`. The disposition schema should list only the 12 expected
   names. Extra receipt checks are not rows, and the gate should not error on them.

3. **Superseded `producer_before` needs an explicit raw-observation rule.** The
   retained raw check (`verification.json` index 4) has `exit=1`, `expected_exit=1`,
   and `exit_matches=true`. Its stdout does not contain
   `summary preserves top-level exposed declaration kind`; stderr is
   `FileNotFoundError … .ufo/evidence/tools/mutate-and-run.sh` (path-layout crash).
   Its `contains` predicate fails on the raw receipt by design. Schema
   `superseded` rows carry only `name/state/reason/superseded_by`, so the gate must
   locate the raw `producer_before` check by name, verify the observed exit and its
   stderr/stdout fingerprint, and report it as informational (a finding ID, not
   a pass). `producer-oracle-repair.json` `supersedes` names exactly this
   path-layout crash. **Decision needed:** whether the raw observation must be
   matched to the literal stderr `FileNotFoundError` string, or only to the existence
   and exit of the named raw check. Recommendation: both, with stable IDs.

4. **Replacement rows.** `producer_before_oracle` and `producer_after_oracle` are
   in `producer-oracle-repair.json` (`checks[0..1]`), not `verification.json`. Their
   `contains` predicates hold on stdout (`…kind FAIL` and `WITNESS_SELFTEST: 41/41 pass`).
   The gate must select them from the file named by the disposition, not by global
   name search, because the two files do not share names (verified: no name overlap).

5. **Structured `pin_live` predicate.** `expected.json` requires `rows:6`,
   `statuses:{unchanged:3,changed:3,unavailable:0}`, and `result_reuse:not_established`.
   Observed in `verification.json` index 8: 6 legs, counts `{legs:6,unchanged:3,changed:3,unavailable:0}`,
   and every leg's `result_reuse` = `not_established`. The gate should count
   `legs[].content_status` and check every leg's `result_reuse`, not just the
   top-level `counts`, so a count can't mask a per-leg mismatch.

6. **Predicate reads.** Confirmed by this seat's JSON parse: `pin_selftest` contains
   `SELFTEST: PASS (18/18)`; `metadata_selftest` contains `SELFTEST: PASS 39/39`;
   `witness_check` contains `WITNESS_CHECK: CLEAN`; `witness_count` contains
   `witness_classified=10`; `producer_after` contains `WITNESS_SELFTEST: 41/41 pass`;
   all exit fields equal the expected exits. `metadata_old_null`/`metadata_corrected`
   and `source_census` need JSON-field or exit predicates, not `contains`, per the
   spec ("structured predicates via parsed check.stdout").

7. **Path safety (fail-closed).** Reject absolute paths and `..` in `inputs` keys
   and in the `expected_file` value. Read receipts with `O_NOFOLLOW` and require
   regular files inside the lane root, following the `pin-disposition.py` pattern
   (`tools/pin-disposition.py:73-82`). Tampered or symlinked inputs → exit 2, not 1.

8. **Exit lattice and finding IDs.** Map: bad/missing/tampered input → 2; semantic
   expectation mismatch → 1; usage → 64; clean → 0. Stable finding IDs should be
   prefixed `EDS-` (e.g. `EDS-ROW-COUNT`, `EDS-DIGEST-MISMATCH`, `EDS-SUPERSEDED-RAW`).
   Keep the IDs in the registry row's "Verdict map" cell or the tool docstring, not
   the spec alone, so an auditor can match them without reading the code.

9. **Write scope and shared files.** Gate owns `tools/evidence-disposition.py` only.
   DispositionSpec owns `.ufo/evidence/round-14/dispositions-before.json` and
   `dispositions.json` only. ReceiptHarness owns `.ufo/evidence/round-14/capture-context.py`
   only. SKILL.md's registry section, LOG.md, corpus/README.md, SCORECARD.md and
   QUALITY.md are L1 integration edits. AGENTS.md requires a LOG.md entry per change.

10. **Freshness boundary.** The row registers no sibling gate execution. The
    committed round-13 receipts were produced by the runner and pin probe, and this
    gate only evaluates their recorded output. Freshness successor sweeps stay
    unopted-in and unregistered (`SKILL.md:806-858` opt-in contract). No row added.

## 4. Checks for L1 (after all seats finish; none run by this seat)

1. `python3 tools/evidence-disposition.py --selftest` → expect exit 0, stable
   finding-ID outcomes per fixture (gate's own isolated fixtures).
2. `python3 tools/evidence-disposition.py --root /home/vgpnk/Projects/shokunin/tameshi-shokunin --dispositions .ufo/evidence/round-14/dispositions-before.json --json`
   → expect exit 1 with the `producer_before` finding (proves the old unresolved row is
   rejected).
3. Same command with `.ufo/evidence/round-14/dispositions.json` → expect exit 0 with 12
   per-expectation dispositions (11 effective, 1 superseded).
4. `diff` the two dispositions files: only the `producer_before` row's `state`
   (effective→superseded) and its reason/replacement fields may differ.
5. Confirm no historical bytes changed: `git status --porcelain` against
   `d6809df…` shows no edits under `.ufo/evidence/round-12/`, `.ufo/evidence/round-13/`,
   `tools/mutate-and-run.sh`, `SHONEN.md`, or any round-13 receipt. Also check
   `sha256sum` of `expected.json`, `verification.json`, `producer-oracle-repair.json`
   against the digests in §2 (they must be unchanged).
6. Confirm the gate's `expected.inputs` digest verification by parsing the
   `expected.json` `inputs` map and comparing the 13 digests (do not trust the closure
   count alone).
7. Record `sha256sum tools/evidence-disposition.py` and the gate's `--selftest`
   output in the round-14 receipt.
8. After SKILL.md append, verify the new registry row has exactly 8 cells, and that
   the existing round-12/round-13 rows are byte-identical to `d6809df`.

## 5. Ownership summary

- Gate: `tools/evidence-disposition.py` (new). Row owner: tameshi.
- DispositionSpec: two disposition JSON files (new).
- ReceiptHarness: `capture-context.py` (new), optional probe row only after it exists.
- L1: SKILL.md registry section, LOG.md entry, README/SCORECARD/QUALITY edits, and integrated checks above.
- No row or edit touches sibling repos, fleet files, or `.ufo/evidence/round-12/` or `round-13/`.
