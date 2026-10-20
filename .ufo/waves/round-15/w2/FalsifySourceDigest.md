# FalsifySourceDigest — round 15 wave 2 (critic, static)

Seat: `TameshiR15.FalsifySourceDigest`. This was a static review only. I did not run the gate or its selftest, and I made no build/test/format calls. No tools were installed or updated. I only read files, plus one `sha256sum` call to hash the inputs.

## Source read (exact)

- `tools/context-capture.py` (read tag 472A, sha256 `0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc`) — lines 1–283, 459–663, 755–1353, 1387–1443, 1579–2017.
- Historical producer `.ufo/evidence/round-14/capture-context.py` (sha256 `7313e9a2…7d89`) — lines 465–515 and 540–647, focused on `sources` derivation and `decide`.
- `.ufo/evidence/round-14/context-receipt.json` (sha256 `05cb55b8…9c1a`), projected to `tool_sha256`, `sources`, and the comparison flags. `.ufo/evidence/round-14/context-missing-env.json`, projected to `tool_sha256` and `sources.probe`.

## Axes

A1 = matches_declared versus the raw digest relation. A2 = producer hash stays historical (not the active tool). A3 = selftest pins a literal id/exit pair for each documented predicate.

## Assigned attack: `matches_declared` contradicted by a raw digest mismatch — DEFENDED

`recompute_sources` (L1017–1035) compares the strings `probe.sha256` and `probe.declared_sha256` directly. It never relies on the stored flag. So if a receipt keeps `matches_declared: true` while its raw digests differ, the gate emits `probe_source_digest_mismatch` with exit 1. The runner check (L1028) works the same way.

The selftest pins both lies:
- `probe-source-lie` (L1840–1847): `declared_sha256 = "1"*64`, flag left `true` → `probe_source_digest_mismatch`/1.
- `runner-source-lie` (L1849–1856): the same for the runner → `runner_source_digest_mismatch`/1.

A second kind of digest lie is also covered. In it, `sources.probe.sha256` and `declared_sha256` agree with each other but not with the `tool_sha256` inside the raw stdout documents. `recompute_comparison` (L920–944) recomputes `payload_tool_sha256_matches_disk` from the raw stdout. The `payload-digest-lie` case (L1773–1782) pins this as `comparison_tool_digest_mismatch`/1. Wrong-type flags are also handled: `matches_declared: 1` → `receipt_structure_invalid`/2 (L1858–1863).

## A2 producer hash — DEFENDED (with one redundancy, not a defect)

- `FROZEN_TOOL_SHA256` (L140) = `7313e9a2…7d89`. This equals `sha256(.ufo/evidence/round-14/capture-context.py)`, and it equals the `tool_sha256` field inside both retained round-14 receipts. The active tool hashes to `0ed784e0…1edc`, which is different.
- The result's `tool_sha256` (L1227) is the gate's own digest. It sits beside `receipt.sha256` and is never written back as the receipt's producer. Check mode writes nothing (L1298–1344), so the receipt's producer hash cannot be replaced with the active tool's.
- Redundancy: `tool_declaration_mismatch` (L1175) only runs in frozen mode. Frozen mode first requires the receipt bytes to hash to `05cb…`, and those bytes contain `tool_sha256 = 7313…`. So this ID can never be emitted without a SHA-256 second preimage, and no selftest case can pin it. This is a tradeoff, not a wrong verdict. In explicit mode the receipt's producer hash is not bound (the docstring at L99–100 explains this). Requiring that binding would go beyond bounded retained replay, so I am not raising it.

## The one falsifiable hole (A3): the converse contradiction is not pinned in the selftest

**Counterexample (mutant):** delete the literal-flag checks in `recompute_sources`: L1023–1026 (`matches_declared is not True`) and/or L1032–1035 (`matches_manifest_declaration is not True`). The docstring rule at L50–52 ("match flags must be literal True") would then be enforced by no code.

**Why the full selftest would still pass:**
- The fixture sets both flags to `true`, with equal raw digests (L1462–1471).
- The only other flag mutation is `matches_declared: 1`, which `require_bool` rejects first with exit 2 (L635, L1858).
- `probe-source-lie` and `runner-source-lie` both keep the flag `true`, so they still fail on the raw-string check (L1019/L1028).
- No case sets `matches_declared: false` or `matches_manifest_declaration: false` while the raw digests are equal. A grep of every `matches_declared` / `matches_manifest_declaration` write in the selftest found only L1465, L1471 and L1860.
- So both mutants survive. The documented recorded-flag-versus-raw contradiction, in the direction "flag false, digests equal", has no literal expected id/exit pair.

**Impacted axes:** A3 (calibration of the selftest's literal pairs) and A1 (the converse direction is unpinned). Gate verdicts on retained receipts are unaffected. Statically, the current code does return `probe_source_digest_mismatch`/1 for this input, so this is a selftest gap, not a wrong verdict.

**Smallest safe correction:** add one or two `check_case` entries. Each sets `sources.probe.matches_declared = False` (and, separately, `sources.runner.matches_manifest_declaration = False`) while leaving the raw digests equal. Set `status="mismatch"`, `exit=1`, and non-empty `reasons`. Pin `probe_source_digest_mismatch`/1 and `runner_source_digest_mismatch`/1. Without the L1023/L1032 checks, the gate would return `receipt_verdict_mismatch`, so these cases kill both mutants.

## Tradeoff noted (not counted as the hole)

The historical producer can write `declared_sha256: null` with `matches_declared: false`. It does this when r13 `expected.json` has no entry for the probe (L496–503 there), and `decide` (L572–579) then records status `mismatch`, exit 1. The active gate's `require_hex` (L633) instead classifies such a receipt as `receipt_structure_invalid`/2. Neither retained receipt has this shape: both declare `297253…4f11`. So this is a strict-schema choice, outside bounded retained replay. It is not a C1 defect.

## Bounded claim

What I checked statically: the requested contradiction is detected and pinned, and the producer hash stays bound to the historical script. The one hole I found is that the selftest does not pin the converse contradiction. I have not run anything, so nothing here claims any check passes. Execution belongs to L1.
