# ReviewJSON — round-15 C1 review against malformed JSON and duplicate keys

Seat: `TameshiR15.ReviewJSON` (reviewer, leaf). Scope: read-only review of the planned C1 JSON handling. No gate, selftest, capture, Python snippet, or verification command was executed. Claims below are source-read or `[INFERENCE]` (unexecuted).

## Read revision and state

- Lane HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (`round-14 verifier spot-check`).
- `tools/context-capture.py`: **ABSENT** at the read revision. Nothing below is a claim about implemented code; it is a criterion for the planned source.
- Round-15 untracked state read: `.ufo/waves/round-15/` (wave spec and seat reports) and `.ufo/evidence/round-15/claims.json` only.
- Historical script read: `.ufo/evidence/round-14/capture-context.py`, sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` (matches the retained receipt's `tool_sha256`; last commit `0c6e36d0bd2fd98077de4cff4c90c6f467c2e1fb`).
- Retained evidence read: `.ufo/evidence/round-14/context-receipt.json` (sources, runs, comparison), `guardrails.json`, `context-missing-env.json`.
- Contract read: `corpus/lessons/round-14-verifier-spotcheck.md` line 160 (routed defect 5), `SKILL.md` lines 1592–1602 (round-14 registry row: `0/1/2`, no `64`, no standalone selftest).
- Lane pattern read: `tools/pin-disposition.py` lines 464–495 (probe-side duplicate-key hook with `InvalidInput`).
- Host: `python3` 3.14.7 (read-only `--version`).

Tools installed or updated: none.

## Axes

- **calibration**: how strongly the gate's JSON claims are stated (a claim the code does not earn is a calibration defect).
- **operability**: exit-class correctness (`0/1/2/64`) on malformed input.
- **depth**: JSON edge cases reached (duplicates, nesting, digit limits, shape).
- **coverage**: which JSON inputs are parsed and by which path (manifest, expected, probe baseline, probe injected, retained receipt).

## Historical JSON surface (exact)

| Site | Lines | Parse | Duplicate-key hook | Caught | Behaviour on failure |
|---|---|---|---|---|---|
| `_no_duplicate_keys` | 158–164 | raises `InvalidContext("invalid_json", "duplicate JSON key ...")` | — | — | — |
| `parse_json` (manifest, expected) | 167–181, called 487–488 | `json.loads(text, object_pairs_hook=_no_duplicate_keys)` line 173 | **yes** | `JSONDecodeError` only (174) | `invalid_json` exit 2; non-object root `invalid_json` (179–180); bad UTF-8 `invalid_utf8` (170–171) |
| `parse_probe_document` (probe stdout, both runs) | 340–347, called 351, 362 | `json.loads(run["stdout"])` line 344 | **no** | `JSONDecodeError` only (345) | returns `None` |
| `comparison_block` baseline gate | 351–361 | `row.get(...)` on every element of `legs` (354–356) | — | none | non-dict `legs` element raises `AttributeError` |
| `run_bounded` | 190–210 | decodes stdout as UTF-8 (205–208) | — | `FileNotFoundError`, `TimeoutExpired`, `OSError` | `non_utf8_output`, `timeout`, `exec_failed` → exit 2 |
| `main` | 605–643 | — | — | `InvalidContext` only (617) | any other exception escapes → Python exit **1** |

Exit map as documented (docstring 26–29): `0` ok; `1` mismatch "(including injected run unusable)"; `2` could-not-evaluate; `64` usage. Decide reasons (559–577) are free text; only `InvalidContext.kind` values are identifiers.

Read order in `evaluate()` (476–479, 487–489, 515, 539–540): probe file, runner file, manifest, expected, then runner-mapping parse, then the two probe runs. A malformed manifest or expected therefore fails **before** the probe runs and needs only the four files to exist.

## Acceptance criterion (exact)

Each row is a CLI case for the planned `tools/context-capture.py` (`--selftest` subprocess, isolated temp root). "Pinned" means the selftest asserts **both** the exit and the stable identifier (`kind=` in the stdout line, or `receipt.error.kind`). Exit-only assertions are rejected (see P1).

| ID | Input (synthetic, temp root) | Required exit | Required stable ID | Status at read revision |
|---|---|---|---|---|
| J1 | manifest truncated `{` | 2 | `invalid_json` | supported (174–178) |
| J2 | manifest zero bytes | 2 | `invalid_json` | supported (JSONDecodeError path) |
| J3 | manifest root `[]` | 2 | `invalid_json` | supported (179–180) |
| J4 | manifest `{} {}` (trailing data) | 2 | `invalid_json` | supported (JSONDecodeError path) |
| J5 | manifest invalid UTF-8 bytes | 2 | `invalid_utf8` | supported (170–171) |
| J6 | manifest with duplicate `"schema"` | 2 | `invalid_json` | supported (hook, 162/173) |
| J7 | manifest nested 100000 deep `[` | 2 | `invalid_json` | **NOT supported**: uncaught `RecursionError` → exit 1 `[INFERENCE]` |
| J8 | manifest integer with 5000 digits | 2 | `invalid_json` | **NOT supported**: uncaught `ValueError` (int digit limit) → exit 1 `[INFERENCE]` |
| J9 | expected.json duplicate `"inputs"` (valid manifest) | 2 | `invalid_json` | supported (488 with hook) |
| J10 | expected.json duplicate key nested under `inputs` | 2 | `invalid_json` | supported (hook applies at every depth) |
| J11 | manifest with repeated leg | 2 | `invalid_manifest` | supported (453); **not** a JSON-scope case, keep separate |
| J12 | retained receipt with duplicate `"status"` in `--check` mode | 2 | `invalid_json` | **NOT supported**: no check mode exists; required if `--check` ships (F8) |
| P1 | baseline probe stdout not JSON | 2 | `probe_baseline_unusable` | supported (352–361) |
| P2 | baseline probe stdout with duplicate key | 2 | `probe_baseline_unusable` | **NOT supported**: accepted silently (344) (F2) |
| P3 | baseline probe `legs` = six non-object entries | 2 | `probe_baseline_unusable` | **NOT supported**: `AttributeError` → exit 1 (354–356) (F3b) |
| P4 | injected probe stdout UTF-8, not JSON, exit 0 | 1 | reason prefix `injected observation differs from baseline` | supported (371–375, 560–563) |
| P5 | injected probe stdout invalid UTF-8 | **2** | `non_utf8_output` | supported (208) but **contradicts** docstring "1 ... injected run unusable"; pin 2 (F5) |
| P6 | injected probe stdout duplicate key, canonical-equal to baseline | 1 | reason prefix `injected observation differs from baseline` | **NOT supported**: currently exit 0 possible (F2) |
| P7 | injected probe exit nonzero with valid JSON | 1 | reason prefix as P4 | supported (341–342 → `None`) |
| P8 | injected probe timeout | **2** | `timeout` | supported (199); contradicts docstring "1 ... injected run unusable"; pin 2 (F5) |

## Findings (ordered by severity)

**F1 — required, implementation-critical: wrong `LANE_ROOT` depth.**
Historical line 46 derives `LANE_ROOT` with four `dirname` calls, correct only for `.ufo/evidence/round-14/capture-context.py`. For `tools/context-capture.py` four calls resolve to `/home/vgpnk/Projects`, so `PROBE_REL` (`tools/pin-disposition.py`) resolves outside the lane. Every run then fails at the first read with `missing_input`, exit 2. A selftest that asserts only exit 2 would pass for the wrong reason (P1). Required: `LANE_ROOT = dirname(dirname(SELF))` and `FLEET_ROOT = dirname(LANE_ROOT)`. Selftest must run a copy of the tool at `<tmp>/tools/context-capture.py`, so that every write (including `OUTPUT_REL` on invalid input, historically written in `main` 617–628 and `write_receipt` 583–602) stays inside the temp root.

**F2 — required for any "duplicate keys are rejected" claim: the probe-stdout parse is unhooked, and canonical equality is last-wins.**
`parse_probe_document` (344) uses plain `json.loads`. `comparison_block` builds `base_cmp`/`inj_cmp` and compares canonical `json.dumps(sort_keys=True)` (384–391). With duplicate keys, Python keeps the last value, so the comparison is not injective over the raw bytes. `raw_stdout_equal` (367) is recorded but never used in `decide` (559–580).
Concrete counterexample (parser differential, not a fabricated run): baseline top-level `"status":"ok"` once; injected stdout contains `"status":"mismatch", ..., "status":"ok"` with the same `tool_sha256` and `observed_at`. Canonical equal, `equal=true`, `decide` → `ok`, exit 0, while the first occurrence in the injected bytes reports `mismatch`. Note `comparison_block` never checks the injected `status`.
Required fix (minimal, preserves historical exit classes): route `parse_probe_document` through the same hook as `parse_json`, **and catch `InvalidContext` inside it and return `None`**. Without the catch, injected duplicates would become exit 2 `invalid_json` while injected non-JSON stays exit 1 (P4), an inconsistent split. With the catch: baseline duplicate → `probe_baseline_unusable` (2); injected duplicate → `None` → comparison error → exit 1 (P6).

**F3 — required for "malformed JSON → 2" claims: uncaught exceptions exit 1.**
Only `JSONDecodeError` is caught at 174 and 345, and only `InvalidContext` at 617. `RecursionError` (deep nesting) and `ValueError` (integer digit limit, CPython 3.11+; host is 3.14.7) escape `main`, and Python's uncaught-exception status is 1 — the same status as `mismatch`, with no receipt and no stable ID. `[INFERENCE]` from CPython `json` behaviour; unexecuted. Required: catch `(ValueError, RecursionError)` in both parse sites and convert to `InvalidContext("invalid_json", ...)`. Note `ValueError` covers `JSONDecodeError`; `InvalidContext` is not a `ValueError`, so hook errors are not swallowed.

**F3b — required for the documented exit-2 claim "baseline is not a six-leg ok document": `AttributeError` on non-dict rows.**
`comparison_block` 354–356 calls `row.get` on each `legs` element and `row.get("pinned", {}).get(...)`. A valid-JSON baseline with `"legs": [1,2,3,4,5,6]` (or `pinned` as a string) raises `AttributeError` → exit 1. Required: `isinstance(row, dict)` and `isinstance(row.get("pinned"), dict)` guards that route to `probe_baseline_unusable`. This is the only way the docstring claim at line 28–29 holds.

**F5 — required doc correction: the exit-1 claim for "injected run unusable" is false for timeouts and non-UTF-8.**
Docstring 26–29 says exit 1 includes "injected run unusable". In code, injected non-UTF-8 → `non_utf8_output` (208, exit 2), injected timeout → `timeout` (199, exit 2), injected exec failure → exit 2. Exit 1 applies only to UTF-8 text that is not a JSON object, or to a nonzero exit (P4, P7). The new tool's docstring must state this exact split and must not copy the "including" sentence. Keep the historical semantics (reuse, per the wave spec) and pin P5/P8 at 2.

**F4 — required for any "stable finding ID" claim: exit-1 reasons are free text.**
`decide` (559–577) emits interpolated strings (`"... after excluding observed_at: {error}"`, `"(exit={})"`). Only `InvalidContext.kind` is a stable identifier. The round-14 defect asks for "stable expected finding IDs". Required: either map each exit-1 reason to a fixed ID in the new tool, or pin the exact reason prefix and state that it is a prefix, not an ID. Do not claim stable mismatch IDs otherwise.

**F8 — required if `--check` ships: retained receipts are a tamper vector for duplicate keys.**
`json.dump` cannot emit duplicates, so duplicates in a retained receipt indicate hand editing or tampering. A last-wins read lets a later `"status":"ok"` override an earlier `"status":"mismatch"`. Required: the receipt parse uses the same hook and exits 2 `invalid_json` (consistent with the spec's `snapshot_tampered` class at 2, per the wave spec's AttackJSON/ContextGate expectations).

**F6 — optional hardening, not required by the claim set.**
`json.loads` accepts `NaN`, `Infinity`, `-Infinity` by default (no `parse_constant`). Not strict RFC 8259. Adding `parse_constant` raising `invalid_json` is cheap; do not claim strict conformance either way. A UTF-8 BOM is rejected as `invalid_json` (JSON BOM error), which is conservative and acceptable; pin it or do not claim BOM support.

**F7 — adjacent, out of C1 scope: the probe's own manifest read has the same unhooked-exception gap.** `tools/pin-disposition.py` 488–493 catches only `JSONDecodeError`. Deep nesting there would exit the probe with status 1 and no JSON, which C1 classifies as baseline-unusable (2) or injected-mismatch (1) via `parse_probe_document`. Do not edit the probe for C1; note it for the probe's owner.

## Unearned claims to reject

- **U1** "Any inequality is a mismatch" / "canonical JSON comparison is faithful" (docstring 4–9). False for duplicate keys (F2). Reject unless F2 is fixed and P6 is pinned.
- **U2** "Malformed JSON always exits 2." False until F3 (J7, J8). Reject unless J7/J8 are pinned at 2.
- **U3** "Injected run unusable → exit 1." False for timeout and non-UTF-8 (F5). Reject the unqualified sentence.
- **U4** "Stable finding IDs" for mismatch reasons. Reasons are free text (F4). Reject unless mapped.
- **U5** "Duplicate-key handling verified by the probe path." Reject unless a CLI case reaches the probe comparison (P2, P6), which requires a synthetic runner fixture (see recipe). Otherwise the claim covers manifest/expected/receipt only.
- **U6** "Strict RFC 8259 validation." Not earned (F6).
- **U7** "Round-14 retained receipts were duplicate-checked." Not earned: the historical tool has no check mode and its probe parse is unhooked (F2). Any such claim requires a future executed check, not this review.
- **U8** "The `guardrails.json` helper controls cover duplicate keys." Not earned: their `json.load` calls (lines 10, 25, 40 of `guardrails.json`) use last-wins with no hook. They remain helper evidence only.

## Likely false positives (test-design hazards)

- **P1 — exit-only assertions pass for the wrong reason.** J-cases can exit 2 through `missing_input` (F1), `invalid_manifest`, or `runner_unparsed`. Exit 1 can come from an uncaught traceback (F3, P-cases). Reject any selftest that asserts exit alone; pin `kind=` (or `error.kind`) and the stdout prefix.
- **P2 — helper-only unit call counts as the gate clause.** Calling `_no_duplicate_keys` or `parse_json` directly does not satisfy the defect-5 requirement "standalone isolated self-invocation testing exits and stable expected finding IDs". Reject.
- **P3 — BOM flagged as "malformed valid JSON".** It is `invalid_json` by design (F6); state it, do not treat it as a defect.
- **P4 — injected non-JSON mapped to exit 2 "could-not-evaluate".** By historical design it is exit 1 (mismatch). Changing it is a semantics change, not a fix. Pin 1 unless TameshiR15 explicitly decides otherwise.
- **P5 — duplicate-key receipt reported as `snapshot_tampered`.** The kind is `invalid_json`; pin the kind, do not conflate with a digest mismatch.
- **P6 — selftest passes when the probe is never reached.** Manifest/expected cases (J-rows) never run the probe; a selftest that claims probe-path coverage must include a P-row that does.

## Fixture recipe pointers (for ContextGate and SpecJSON; no source authored here)

- J1–J11: the temp root needs `tools/pin-disposition.py` and `tools/mutate-and-run.sh` present (stub content is enough: their hashes are recorded at 477–478, not parsed before the manifest/expected parse), plus the manifest/expected under test. Use synthetic files only; do not copy the real runner or manifest (no live reads).
- J10 requires a **valid** manifest (`validate_manifest` 439–462: six legs, 40-hex `pinned_commit`, 64-hex `expected_sha256`, unique legs).
- P-rows reach the probe only after `parse_runner_mapping` (213–256) succeeds: six header rows, six unique `PIN_` and `REV_` constants, six `run_regression` calls, six unique legs equal to the set in the header rows. A synthetic runner satisfying these is required. `mapping_block.all_match` may be false (adds reasons to `decide`) without raising.
- The stub probe's stdout is fully controlled by the fixture, so P2/P3/P5/P6/P8 are reachable without executing the real probe. Expected exits per table above.
- Do not reuse the real `context-receipt.json` as a fixture; it is retained evidence.

## Recommendations (exact, bounded)

1. Set `LANE_ROOT = os.path.dirname(os.path.dirname(SELF))` for `tools/context-capture.py` (F1). Selftest runs a copy under a temp `tools/`.
2. Introduce a single `_parse_json_strict(raw_text, label)` used by manifest, expected, probe baseline, probe injected, and receipt-check parses. It sets `object_pairs_hook=_no_duplicate_keys`, catches `(ValueError, RecursionError)` → `InvalidContext("invalid_json")` (F2, F3, F8). Reuse the historical helper names where possible.
3. In `parse_probe_document`, catch `InvalidContext` from that helper and return `None` (F2). Preserve the baseline check and the injected path exactly.
4. Add `isinstance` guards in `comparison_block` for `legs` elements and `pinned` (F3b).
5. Docstring of the new tool: state the exact exit split from F5; do not copy "including injected run unusable".
6. Selftest: pin each row J1–J12, P1–P8 with exit **and** `kind=`/`error.kind` (or the reason prefix for exit 1). Include P6 and P2 only if the fixture recipe above is implemented; otherwise state explicitly that duplicate-key handling of probe output is not covered.
7. Optional (F6): `parse_constant` raising `invalid_json`. Not required; do not claim strict RFC 8259.
8. Do not edit the historical `capture-context.py`, round-14 receipts, or `tools/pin-disposition.py` (F7). Keep historical bytes identical.

## Residual risk and verification gaps

- No execution: every behaviour marked `[INFERENCE]` (J7, J8, F3 exception escapes) depends on CPython 3.14 `json` and exception behaviour and must be confirmed by the L1 selftest, not by this report.
- The P-row fixtures are not yet proven to exercise the probe comparison; coverage of duplicate keys in probe output stays unclaimed until they run.
- Receipt-check mode does not exist; J12 and F8 are conditional on it shipping.
- The round-14 retained receipt's probe stdout was produced by a probe with no duplicate keys [INFERENCE from its `json.dumps` producer]; this was not parsed in this review.
