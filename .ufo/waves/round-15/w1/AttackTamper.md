# AttackTamper: critic review of C1 `snapshot_tampered`/2

Seat: TameshiR15.AttackTamper (critic, leaf). I only read sources. I executed no gate, no selftest and no mutant. Tool installs/updates: none.

Read revision: HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0`. The worktree has only the untracked `.ufo/evidence/round-15/` and `.ufo/waves/round-15/` trees. **`tools/context-capture.py` did not exist when I read** (`ls tools/`), so this attacks the *planned* contract: the spec1.json Integration interface and claims.json C1 "frozen digest-bound retained run". It does not attack implemented code.

## Axes
A1 discrimination: the tamper arm fails when the digest check is removed. A2 actual CLI exit+ID, not a helper's return value. A3 precedence: integrity is checked before verdict. A4 hermetic, with no writes. A5 no false tamper on the valid round14 receipt. A6 honest anchoring claim.

## Grounding (observed, read-only)
- Historical `.ufo/evidence/round-14/capture-context.py` (sha256 `7313e9a2…7d89`) has **no snapshot mode and no `snapshot_tampered` token**. Every could-not-evaluate path is `InvalidContext(kind)` → exit 2 (`:612-628`). `decide()` (`:553-580`) reads only `comparison.equal`, `comparison.payload_tool_sha256_matches_disk`, `environment.env_delta_matches_declared`, `environment.baseline_has_GIT_DIR`, `positive_control.effective`, `sources.probe.matches_declared`, `sources.runner.matches_manifest_declaration` and `mapping.all_match/reasons`. It **never reads `observed_at`, `sources.*.sha256`, `tool_sha256` or the recorded `status`/`exit`**.
- The InvalidContext handler in `main()` **writes the receipt before returning 2** (`:618-622` → `write_receipt` → `OUTPUT_REL`). `LANE_ROOT` comes from `os.path.realpath(__file__)` (`:45-46`), so any child run of the real file resolves the real lane.
- Retained receipt `.ufo/evidence/round-14/context-receipt.json`: sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`, git blob `7ffec3c7…`, first byte `{` (od). Its `tool_sha256` is `7313e9a2…`, the historical script, **not** the new tool. It also carries absolute `lane_root`/`fleet_root`/`invocation.cwd`.
- The live sources still equal the receipt's recorded digests today: probe `297253…4f11`, runner `75ed93…adc5`, manifest `64eaa4…0af6`, expected_r13 `a01607…4336`. This is a point-in-time observation, not a stability claim.
- Lane precedent for a byte tamper:
  - `tools/repeat-control.py:790-791` flips `data[0] ^ 0x01`.
  - `tools/witness-metadata.py:1063-1082` appends `b" "` and hashes integrity first (`:388-391`).
  - `witness-metadata.py:710-714` pins tamper+semantic defect to `snapshot_tampered`/2.
- Gate standard (`kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:398-410`): the selftest asserts exit + a stable finding-id, "independent of the recomputation", and "a helper-only or model-only self-check does not satisfy this clause". The gate verifies digests "before comparing verdicts", and a baseline without digests is `unpinned (legacy)`.
- CPython `/usr/lib/python3.14/json/decoder.py:346-348`: `decode` skips trailing whitespace before its `Extra data` check, so a document with a trailing space still parses.

## Counterexample (primary): first-byte flip passes even with no digest check
Planned arm: copy repeat-control's recipe onto the JSON receipt, flipping byte 0. `{` (0x7B) becomes `z` (0x7A), so the receipt is invalid JSON. Then delete the digest comparison from the check mode (the mutant).

- Mutant path: the bytes go to the reused `parse_json` (`:167-181`), which raises `InvalidContext("invalid_json")`, so the run exits **2**.
- So an exit-only assertion passes on the mutant.
- The ID assertion also passes on the mutant if the check maps every snapshot-shape error to `snapshot_tampered`. repeat-control does exactly that ("a malformed record, or any shape error exits 2 `snapshot_tampered`", `repeat-control.py:59-62`), and an implementer reusing it would inherit that mapping.
- Net: the arm stays green whether or not the digest is verified. It is calibration theatre for A1.

A nominal helper-only test misses this too. `verify_digest(bytes, pin)` raising in-process says nothing about which layer the CLI actually hits first, or which ID and exit it prints.

### Discriminating replacement (required)
This is an isolated temp root, built by the selftest and run as a **subprocess of the public CLI**.

1. Write a synthetic receipt `R` that `decide()` accepts:
   - `comparison: {equal: true, payload_tool_sha256_matches_disk: true}`
   - `environment: {env_delta_matches_declared: true, baseline_has_GIT_DIR: false}`
   - `positive_control: {effective: true}`
   - `sources: {probe: {matches_declared: true}, runner: {matches_manifest_declaration: true}}`
   - `mapping: {all_match: true, reasons: []}`
   - `observed_at: "2026-10-20T06:35:01Z"`
   - Serialize with `json.dumps(R, indent=2) + "\n"`.
2. Write the expected record: raw-byte `sha256(R bytes)` plus the literal clean pair. ContextGate picks the clean ID token.
3. Tamper `R'`, with either of two edits:
   - **(a)** Append `b" "`. This is the witness-metadata precedent; it is valid JSON per decoder.py:346.
   - **(b)** Replace the single occurrence of `"observed_at": "2026-10-20T06:35:01Z"` with `…:02Z`. Assert exactly one occurrence before replacing.

   Neither edit changes any field `decide()` reads.
4. Expected literal: `("snapshot_tampered", 2)`.

Mutant argument, from source reading only: with the digest check removed, `R'` parses and `decide(R')` returns `ok`/0. The case then observes the clean pair, not `snapshot_tampered`/2, and fails. This arm discriminates. **Edit (b) also catches a normalized or "observed_at-excluded" digest.** That implementation is wrong for a byte-retention snapshot, because the observed_at exclusion belongs to the baseline/injected comparison (`:384-391`), not to evidence integrity.

## Further counterexamples

1. **Verdict-before-integrity (A3).** Take `R'` with the digest changed **and** `comparison.equal: false`. If the check runs `decide()` first, it exits 1 `mismatch`, a compared verdict on tampered evidence. The Gate standard says "before comparing verdicts", and the lane precedent is witness-metadata tamper-plus-defect → `snapshot_tampered`/2. **Required ordering:** hash the raw bytes → verify → parse those exact bytes, with no re-read → `decide()`. A test arm for this is optional but cheap: expect literal `snapshot_tampered`/2.
2. **Unpinned live re-derivation (A3/A6).** Suppose the check re-hashes the live `tools/pin-disposition.py`, or re-parses the live `tools/mutate-and-run.sh` through `parse_runner_mapping`/`mapping_block`, but pins only the receipt. A later live edit of `"$REV_BASH"`→`"$REV_CHECKLIST"` then flips the verdict to 1, or drift becomes mislabelled tamper. A frozen run also cannot read live files ("Two evidences"). **Required:** the check reads only the files in its expected record, all digest-pinned. Otherwise it reads the receipt plus its record only.
3. **Write on the tamper path (A4).** Reusing the `main()` InvalidContext handler writes an `invalid_input` receipt to `OUTPUT_REL` on every exit 2 (`:618-622`). Because `LANE_ROOT` follows `__file__`, a selftest child of the real file writes into the real lane: a round15 receipt is clobbered during a read-only check. That breaks the "no live-tree write" clause, and a helper test cannot observe it. **Required:** the check/snapshot mode never calls `write_receipt`. It takes explicit `--receipt`/`--expected` paths or a snapshot DIR, so the child touches only the temp root.
4. **False tamper on the valid historical receipt (A5).** Requiring `receipt.tool_sha256 == sha256(SELF)`, or `lane_root == LANE_ROOT`, makes the committed round14 receipt (`tool_sha256 7313e9a2…`) read `snapshot_tampered`. The claimed "frozen digest-bound retained run" would then contradict itself. **Required if checked at all:** pin the producing-tool digest and receipt schema literally in the expected record. Do not compare them to the running tool or the current root.
5. **Missing pin reads clean (A6).** If no expected record exists, or its digest is absent or empty, the run must never fall through to `decide()` → 0. The Gate standard says `unpinned (legacy)`; the lane precedent is witness-metadata `missing-digest-red` → `snapshot_tampered`/2. **Required:** a non-clean exit 2 with a pinned ID.
6. **Traceback exit 1 (A2).** Tamper the record's digest to a non-string (`123`/`null`) and run unguarded `DIGEST_RE.fullmatch(123)`. That raises TypeError, Python exits 1, and the run reads as `failed`. **Required behaviour:** fail closed to 2, as evidence-disposition maps `internal_error`→2 (`evidence-disposition.py:1948-1951`). The specific test arm is optional.

## Required routed fix vs optional hardening

Required (routed defect 5 plus Gate standard clauses):
- **R1:** at least one tamper arm per the discriminating recipe (a or b). The first-byte flip must not be the sole tamper arm.
- **R2:** literal expected `("snapshot_tampered", 2)` committed in the tool, not computed by calling `decide()`. Assert it from the child's exact final verdict token and returncode, not by substring search.
- **R3:** raw-byte digest verified before parse and before `decide()`.
- **R4:** no write and no live read in check/snapshot mode; explicit paths.
- **R5:** no `SELF`/root equality against retained receipt metadata.
- **R6:** a missing or unpinned digest is never clean.
- **R7:** an unexpected exception exits 2, never 1.

Optional hardening (not routed; do not overclaim):
- **O1:** an external anchor for the expected record digest. Options are a literal in the tool source (witness-metadata pattern) or reliance on committed git history. Without one, a coordinated receipt+record rewrite inside the snapshot passes. This is round12 SnapshotReview case E (`probe-output.txt:9`). Disclose the limit, as `repeat-control.py:89-92` does. Never claim "tamper-proof".
- **O2:** further arms for missing, unlisted, symlinked and duplicate-key inputs (repeat-control precedent).
- **O3:** a tamper+mismatch precedence arm.
- **O4:** internal-consistency recomputation of the receipt booleans (for example `sources.probe.sha256 == declared_sha256` vs `matches_declared`). This belongs to SpecSourcePins/Types, not to tamper.

Non-claims to reject: the selftest passing is capability, not a measurement. One discriminating arm is not a tamper-detection rate. Self-contained digests do not prove the producer's provenance. A green L1 run does not make this seat independent admission authority.

## For L1 (post-integration, one pass)
1. Confirm by reading that the tamper arm's edit leaves every `decide()`-read key unchanged and keeps the JSON valid.
2. Optionally run one throwaway mutant: comment out the digest comparison, then run `--selftest`. The tamper case must fail with the clean pair observed, and the scratch must not be committed.
3. `sha256sum .ufo/evidence/round-14/{capture-context.py,context-receipt.json}` must still equal `7313e9a2…7d89` and `05cb55b8…9c1a`.
