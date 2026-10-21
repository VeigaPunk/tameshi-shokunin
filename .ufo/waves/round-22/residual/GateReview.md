# GateReview — residual falsification of `tools/wave-accounting.py`

Candidate: `e4da41c3102f6f90b42257d4b8785335806ef954` (HEAD; `tools/wave-accounting.py` unchanged in the working tree versus the candidate).
Contract: `.ufo/evidence/round-22/contract.json` (C1, eight frozen public-CLI rejection predicates, bounded to declared retained inputs).
Method: static reading of `tools/wave-accounting.py`, `.ufo/evidence/round-22/measure.py`, the frozen fixtures and the registry and SKILL rows. Read-only data checks only. I did not run the gate, its selftest, measure.py, tests, builds or installs, and I made no git or jj mutations.

## Verdict

**No blocking defect against the C1 claim.** For each of the eight contract predicates I found no input that gets a clean exit (0) while that predicate is violated. A clean exit requires all of the following:
- every member has exactly one outcome, and the reverse (`seen != set(by_name)`, lines 105-106);
- outcome `id` and `role` exactly equal the member's (lines 91-93);
- agent IDs are unique within a wave's members, across all waves' members (`all_agents`), and within a wave's outcomes;
- status is exactly `completed` or `failed`;
- `replaced` is literally `false`;
- the claimed totals exactly equal the observed totals.

Reports never change `completed` or `dead` (lines 96-104).

I checked that the frozen bundle is a faithful projection. Every `derivation.json` input SHA-256 still matches its file. Bundle `members` exactly equal `.ufo/waves/round-21/w{1,2}/swarm-registry.json` name, agentId and role (71/71 and 75/75). `wrong-count-bundle.json` differs from `bundle.json` only in wave2 `claimed`.

There are seven nonblocking defects or tradeoffs below. Two of them give false-clean exit codes, but only on inputs outside the eight predicates. There is also one cross-lane provenance item that is **conditionally blocking**.

Axes impacted: correctness of exit classification, schema strictness, regression pinning (no-harm over future edits), provenance wording.

## Findings

### N1 — Deeply nested JSON escapes the exception map and exits 1, which means "failed invariant" (nonblocking, false-red with the wrong verdict class)
- Where: `run()` line 136 catches `(OSError, ValueError, TypeError, UnicodeError)`. `decode()` lines 29-31 call `json.loads`.
- Counterexample: a bundle `{"schema":"wave-accounting-v1","waves":[` + `[`×200000 + … whose expected digest matches. The same works for a deeply nested `expected.json`.
- Evidence: on this host (Python 3.14.8), `json.loads(b'['*200000+b']'*200000)` raises `RecursionError` (MRO `RecursionError → RuntimeError → Exception`), which is not in the tuple. The traceback is uncaught, so the interpreter exits 1. The module docstring and the SKILL.md table both say exit 1 means "failed invariant" and exit 2 means "could-not-evaluate". With `--json`, stdout is empty, with no `INVALID_INPUT`. `MemoryError` takes the same path.
- Never clean, so C1 is unaffected. But an exit-code consumer records an invariant failure for input that could not be evaluated.
- Smallest fix: add `RecursionError` (optionally `MemoryError`) to the `except` tuple at line 136.

### N2 — `--help` exits 0 even when combined with real arguments (nonblocking, false-clean exit code)
- Where: `main()` lines 161-164 map `SystemExit(0)` to return 0.
- Counterexample: `python3 tools/wave-accounting.py --bundle X --expected Y --help` exits 0 after printing only usage. Nothing is evaluated.
- The documented exit map says 0 means clean. Registry entries are safe because `stdout_contains` requires `"finding_ids": []`, but a consumer that only checks the exit code sees a pass.
- Smallest fix: treat help as usage (64) when `--bundle`, `--expected` or `--selftest` is also present, or return 64 for any non-evaluating exit.

### N3 — Unknown keys are silently ignored at every level (nonblocking, false-clean on schema)
- Where: `evaluate()` reads named keys with `.get` and never checks key sets. The same applies to the expected file in `run()` lines 125-130.
- Counterexamples that exit 0:
  - A member `{"name":"dead","id":"seat.dead","role":"critic","replaced":true}` with the matching outcome `"replaced": false`.
  - An outcome with `"status":"completed","status_detail":"failed (exit 1)"`.
  - A wave with `"claimed_total":{"seats":999}`.
  - A bundle with `"waves_superseded":[…]`.

  Contradictory or extra data is accepted without any finding.
- No false-red cost: the frozen bundle uses exactly bundle `{schema,waves}`, wave `{name,members,outcomes,reports,claimed}`, member `{name,id,role}`, outcome `{name,id,role,status,replaced}`, and expected `{schema,bundle_sha256}`. I checked this with a read-only key census.
- Smallest fix: require exact key sets for these five object kinds and raise `ValueError` (exit 2) on any other key.

### N4 — A replacement seat in a later wave under the same name is clean (nonblocking tradeoff; the honest wording is already "declared")
- Where: `all_agents` deduplicates agent IDs across waves, but nothing deduplicates seat names across waves. Replacement detection is only `outcome.get('replaced') is not False` (line 94).
- Counterexample: wave `w1` has seat `X` with id `X-3`, status `failed`. Wave `w2` has seat `X` with id `X-4`, status `completed`, `replaced:false`. Per-wave claims are honest. The result is clean, while `total.seats` counts seat X twice and `total.completed` absorbs the replacement. This is how a replacement wave re-dispatches a dead seat, and it does not depend on trusting the flag.
- No false-red cost on frozen data: wave1 and wave2 share 0 seat names and 0 IDs.
- `corpus/knowledge/callback-authoritative-accounting.md:21` says "no declared replacement", which is accurate. A claim of replacement detection beyond the self-declared flag would be an overclaim.
- Smallest fix: a `CROSS_WAVE_SEAT` finding for any seat name repeated across waves.

### N5 — Selftest pins only part of the enforced invariants (nonblocking, regression pinning)
`measure.py` changes one thing per predicate on a single two-seat wave. Each of these code changes would still give `ACCOUNTING_SELFTEST: 8/8 pass`:
- deleting the member-side `DUPLICATE_AGENT` check (lines 72-73), **or** the outcome-side one (lines 88-89). The `duplicate-agent` case sets both `members[1].id` and `outcomes[1].id`, so either check alone still fires;
- deleting cross-wave `all_agents` deduplication (the fixture has one wave);
- deleting the `outcome['role'] != member['role']` comparison (only the id is changed);
- narrowing `seen != set(by_name)` to `set(by_name) - seen`, which makes extra outcome seats clean;
- weakening `replaced is not False` to `is True`. A missing `replaced` would then be clean. This is the exact field that `derivation.json` normalized for the 28 rows that omitted it (raw outcome census: `replaced=False` on 118 of 146);
- deleting `DUPLICATE_WAVE`, `DUPLICATE_MEMBER`, `DUPLICATE_OUTCOME` or `UNKNOWN_REPORT`;
- deleting the duplicate-key and nonfinite-JSON rejection in `decode()`, or the `claimed` shape and type checks.

The C1 unit is the eight predicates, so this is not a claim defect. It does undercut `residual-attack-inventory.json`'s "12 additional schema/accounting invariants": none of them has executable registry coverage. In addition, the persisted wrong-count pair has no `tools/registry.json` row; it is only a command in the knowledge doc.

Smallest correction: either state that these invariants are unpinned, or add literal fixtures in a new frozen counter. Do not edit the frozen round-22 `measure.py`.

### N6 — The gate's status vocabulary is the normalized projection, not raw callbacks (nonblocking, false-red if raw callbacks are fed in)
- Evidence: `.ufo/evidence/round-22/round21-callbacks.json` rows carry `status` values `failed (exit 1)` (80) and `completed` (66). The gate only accepts `failed`. A bundle built directly from retained callback rows would report `UNKNOWN_STATUS` on all 80 dead seats.
- The tool's real authority is the normalized `original-outcomes-final.json` projection. `derivation.json` records this, but neither the tool docstring nor the SKILL table names the `failed (exit N)` → `failed` mapping.
- Smallest fix: one line in the SKILL row or docstring naming the accepted projection vocabulary.

### N7 — Exit classes and wording are inconsistent (nonblocking)
- A duplicate report name is a `ValueError` (exit 2, line 62-63), while a duplicate member, outcome or agent is a finding (exit 1). All are data-level accounting defects in an otherwise valid shape.
- The output field `report_artifacts` (line 115) is a declared basename count, not observed files. The tool never touches report paths, which keeps reports independent but makes the field name stronger than what is measured.
- The predicate name `registry-id-mismatch` (`measure.py:18`, contract) tests outcome id against the bundle's own `members`, not `swarm-registry.json`. SKILL.md:1993 says "bind exact registered name/agent/role". This only holds because derivation-time projection made `members` equal the registry, which I verified. The gate re-checks nothing against the registry.
- `selftest()` loads `.ufo/evidence/round-22/measure.py` without a digest check. A modified oracle returning `{'discriminated': 8, 'cases': []}` would print `8/8 pass`. Only git protects it, and SKILL claims digest pinning only for bundle and expected, so this is accurate but worth knowing.

## Cross-lane item (outside the tool; route to the integrator)

### X1 — Forward provenance reference (conditionally blocking)
`corpus/knowledge/callback-authoritative-accounting.md:2` cites `.ufo/evidence/round-22/final/verification.json` as the retained final execution. That path does not exist at the candidate: `ls` reports no `final/` directory. It is blocking if admitted before L1 lands that receipt from the integrated, verified revision. Otherwise it is nonblocking.

## Not defects (attacks that held)
- Whitespace or invisible-character ID aliases (`"seat.a"` vs `"seat.a\u200b"`) are treated as distinct. That is correct under the exact-identity doctrine (`w1/RegistryBinding.md:56`, `w1/MinimalDesign.md:38`). `string()` rejects only all-whitespace values and never normalizes the compared values.
- Swapped IDs between two seats produce `IDENTITY_MISMATCH` on both. A duplicate member name with one outcome produces `DUPLICATE_MEMBER`.
- TOCTOU: the bundle bytes are read once, and both the digest and the decode use the same buffer.
- `claimed` rejects bools (`type is not int`), floats and negatives. Oversized integers hit Python's int-string limit and return `ValueError` (exit 2). Duplicate JSON keys and NaN/Infinity give exit 2.
- Tamper ordering: a digest mismatch returns `SNAPSHOT_TAMPERED` (exit 2) before decoding, which matches the documented exit map.

## Installs
None.
