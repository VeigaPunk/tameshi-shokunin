# ReviewUsage — round-15 C1 planned calibration capability (64 usage class and stable finding IDs)

Seat: `TameshiR15.ReviewUsage` (reviewer, leaf). Lane: tameshi. Scope: review-only, no gate, selftest, build, test or formatter run.

## Read revision and state

- Lane HEAD read: `a9cf4da78f2514c7bedd91a850a88590009d7df0` (= claims.json `baseline`).
- Working tree at read time: untracked `.ufo/waves/round-15/` and `.ufo/evidence/round-15/` (contains `claims.json` only).
- `tools/context-capture.py` **does not exist** at this revision (`tools/` lists `bash-witness-study.py`, `evidence-disposition.py`, `witness-metadata.py`, `pin-disposition.py`, `repeat-control.py`, `mutate-and-run.sh`). This review is therefore spec- and source-level: it reviews the planned contract against the historical source and the protocol. Re-read the new file once it lands and re-check §Acceptance.
- Tool installs or updates by this seat: none.

## Verdict

C1 is admissible as a bounded capability only if the promoted tool (a) classifies exit 64 as `could-not-evaluate` under its own stable finding ID, (b) pins every exit/finding pair in a standalone selftest that asserts both values, and (c) fixes the root-derivation and uncaught-exception hazards below. Three hazards are implementation-critical; the historical source would reproduce them if copied as-is. The claim wording "both exit64 classes explicit" is not yet supported by the source and must be enumerated or dropped.

## Evidence (historical source, read-only)

File: `.ufo/evidence/round-14/capture-context.py` (647 lines, read in full).

| Observable | Location | Note |
|---|---|---|
| Only exit-64 path | `main()` 605–613 | unexpected argv → stderr + `return 64`, no receipt. `-h/--help` → 0 (606–609). |
| Exit map in docstring | 26–29 | 0 / 1 / 2 / 64; 64 has no finding ID. |
| Mismatch verdict | `decide()` 553–580 | returns `("mismatch", 1, reasons)`; this is the "verdict behaviour" routed defect 5 calls a gate. |
| Could-not-evaluate | `InvalidContext` kinds 127–130, raised at 150, 152, 171, 175, 197, 199, 201, 208, 220, 243–253, 358–361, 441–460, 471–474, 492–495, 520–522 | kinds are already stable strings (`missing_input`, `poison_path_exists`, `probe_baseline_unusable`, `runner_unparsed`, …). Reusable as finding IDs. |
| Free-text reasons | 561–563, 571–577 | `reasons` embed `comparison.error` (contains an exit number) and `mapping["reasons"]` (leg names). Not stable. |
| Receipt-write failure | 622–626, 631–636 | exit 2 with message on stderr only; no ID printed. |
| Receipt overwrite | `write_receipt()` 583–602, `os.replace` at 595 | silently replaces an existing path. |
| Root derivation | line 46: `LANE_ROOT = dirname ×4 (SELF)` | correct for `.ufo/evidence/round-14/capture-context.py` (4 levels → lane root). See hazard H1. |
| Uncaught region | `main()` 614: `receipt = base_receipt()` is outside the `try` at 615 | see hazard H2. |
| Probe-shape read | `comparison_block()` 354–356 | `row.get(...)` / `row.get("pinned", {}).get(...)` on unvalidated `legs` elements. See H2. |
| Dead guard | `safe_env()` 184–187 strips every `GIT_*`; `decide()` 568–569 checks `baseline_has_GIT_DIR is False` | `baseline_has_GIT_DIR` is always false by construction; the ID is unreachable. |
| Unreachable hermetically | `POISON_PATH` 60–61; `evaluate()` 469–472 | `/nonexistent/...` cannot be created inside a temp root; `poison_path_exists` cannot be pinned without writing outside temp roots. |
| Red control → exit 1 | `decide()` 570–571 | "git poison positive control is ineffective" → failed (1), including baseline-red control. |
| Injected run unusable → exit 1 | `comparison_block()` 371–375 → `decide()` 560–563 | historical semantics; must be pinned, not left implicit. |

Precedents already in the tree (read-only):

- `tools/bash-witness-study.py` 1574–1579: `UsageParser.error()` overrides argparse to exit `EXIT_USAGE = 64` (argparse default is 2); selftest 1372–1376 asserts the exact code. This is the pattern to copy if argparse is used.
- `tools/repeat-control.py` 870–894: `dispatch()` returns `usage_failure(...)` for bad shapes; `main()` wraps everything in `except Exception` → `setup_failure` (exit 2), with a comment: "never let a traceback exit 1". `usage_failure` maps to `invalid_usage` (64).
- `.ufo/evidence/round-12/oracle-repair/single-control-mutant.py` 42–48, 127–129, 201–203, 861–864: `setup_error` (2) exists "so that no uncaught Python exception can exit 1 and be read as `controls_mismatch`"; `invalid_usage` is 64 could-not-evaluate.
- `.ufo/evidence/round-12/GateSecurity/probes.py` 29–31 (P1): default argparse usage exit collides with the gate map (2 = could-not-evaluate). Round-12 MinimalityReview P3 records the same for Python 3.14.7.
- `tools/evidence-disposition.py` 1828–1835: usage case asserts `returncode == 64` only (exit-only); do not copy for C1.
- `SKILL.md` 1503: repeat-control registry maps "2 and 64 could-not-evaluate" as one class; the finding ID is the only discriminator. C1 must keep 64 separate from 2 by ID.
- `SKILL.md` 1601: evidence-disposition registry row declares `64 usage`. `SKILL.md` 1602: the context row omits 64 entirely (routed defect 5).
- `SKILL.md` 148: "A red control has no denominator — stop and record it as setup failure."
- `SKILL.md` 489: "Zero-work is a defect, not a green."
- Protocol (`kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md`, read-only) §Gate standard 388–410: verdict codes map to `clean|failed|could-not-evaluate`; an undeclared nonzero code reads as could-not-evaluate; self-test must assert exit code **and** a stable finding-id with expected values committed in the owning repo; a helper-only self-check does not satisfy; a gate whose verdict depends on a mutable fleet artifact **ships a snapshot run** with committed expected verdict and pinned input digests.

## Hazards (implementation-critical)

**H1 — LANE_ROOT depth.** If the promoted `tools/context-capture.py` keeps the historical four-level `dirname` chain, `LANE_ROOT` resolves to `/home/vgpnk/Projects` (SELF → tools → tameshi-shokunin → shokunin → Projects), not the lane root. Reads for `tools/pin-disposition.py` then fail with `missing_input` (exit 2), and `main()` still calls `write_receipt()` on that path, so the receipt would be written to `/home/vgpnk/Projects/.ufo/evidence/round-15/`, outside the lane. Derived by source reading; not executed. Required: two levels (`SELF` → `tools` → lane root), or explicit lane-root derivation covered by a selftest that proves it.

**H2 — exit 1 leak by traceback.** Python's uncaught exception exits 1, which the protocol reads as `failed` (mismatch). Two concrete paths: (a) `base_receipt()` at 614 is outside the `try`; `os.getcwd()` / `open(SELF)` failures are uncaught; (b) `comparison_block()` 354–356 raises `AttributeError` when a baseline `legs` element is not an object or `pinned` is not an object, because the probe document is validated only by `schema/status/len`. Required: move everything under the `try`, add a top-level `except Exception` → exit 2 with a stable ID (`setup_error`), and add a selftest case with malformed legs expecting `2 / probe_baseline_unusable`.

**H3 — output overwrite.** `write_receipt()` uses `os.replace`. Once the path is a constant round-15 path, a refusal to overwrite is still required: an existing `.ufo/evidence/round-15/context-receipt.json` must cause exit 2 with an ID (proposal: `output_exists`), and the round-14 receipt path must never be a legal target.

## Acceptance criterion (exact, for the promoted tool)

A. **Usage class.** `python3 tools/context-capture.py <one or more unexpected args>` and `python3 tools/context-capture.py --selftest <extra>` (if `--selftest` exists) each exit **64**, print the literal ID `usage_error` on stdout or stderr, and create no file under the lane's `.ufo/evidence/round-15/`. The registry row lists `64 → could-not-evaluate`. Exit 64 and exit 2 never share an ID.

B. **Exit-and-ID pairs.** `--selftest` runs each case as a public CLI subprocess (`python3 <tempcopy>/tools/context-capture.py …`), compares `(exit, finding_id)` against a literal table in the file, prints `SELFTEST_CASE <name> PASS|FAIL`, and exits 1 on any mismatch, 0 only when all pass. A case that checks exit alone, or checks `exit != 0`, fails this criterion.

C. **Coverage of the map.** The literal table has at least one case per exit code that the tool can reach hermetically: 0 (`context_match`), 1 (each reachable mismatch ID), 2 (each reachable setup ID, including H2's `probe_baseline_unusable` and `output_exists`), 64 (`usage_error`). Every ID in the tool's FINDINGS table is either pinned by a case or named in the registry as unreached by design. `baseline_has_GIT_DIR` and `poison_path_exists` are listed as unreached (see §Likely false positives F8); they are not claimed covered.

D. **Hermetic layout.** The selftest copies the tool into a temp tree shaped `<tmp>/tameshi-shokunin/tools/` with a `git init` repository and fixtures for every input the probe reads, so `LANE_ROOT` and `FLEET_ROOT` derive to temp. No case reads the real `/home/vgpnk/Projects` tree, writes outside `<tmp>`, or creates `/nonexistent/...`. A positive clean case (`0 / context_match`) must exist, so a root mis-derivation cannot pass as a green-by-absence.

E. **Snapshot run (required, not optional).** Because the verdict reads mutable `tools/pin-disposition.py` and `tools/mutate-and-run.sh`, PROTOCOL §Gate standard "Two evidences" requires a snapshot mode `--snapshot DIR` that pins digests of the four inputs plus the expected exit and finding ID; a tampered snapshot yields exit 2 `snapshot_tampered`. The integrator's reading "digest-bound snapshot mode if needed" resolves to **needed**.

F. **Registry row.** Kind `gate`; entry command; verdict map `0 clean; 1 failed (listed IDs); 2 could-not-evaluate (listed IDs); 64 could-not-evaluate (usage_error)`; self-test command `python3 tools/context-capture.py --selftest`; pinned values path; write scope (normal run writes only the round-15 receipt; selftest only temp); owner `tameshi`.

G. **Help.** `-h/--help` exits 0 and prints the literal ID `help_printed`; the registry states that this 0 is not a verdict and that consumers key on the ID, not the exit alone.

## Likely false positives to reject

- **F1 argparse exit 2.** Default argparse usage errors exit 2 (round-12 probe P1; MinimalityReview P3). A "usage" case that accepts any non-zero or accepts 2 passes while the contract says 64. Reject unless the parser class overrides `error()` to 64 (pattern: `bash-witness-study.py:1574–1579`), and the case asserts 64 exactly.
- **F2 exit-only usage check.** `evidence-disposition.py:1835` asserts `returncode == 64` without an ID. Any path that returns 64 would pass. Reject per criterion B.
- **F3 traceback reads as mismatch.** A selftest case "mismatch exit 1" passes if an uncaught exception produces exit 1. Reject per H2; the case must assert the ID, and the ID must be produced by a deliberate `decide()` path, not an exception.
- **F4 reason-text matching.** Matching on `reasons` substrings or the free stdout `CONTEXT:` line passes accidentally (the reasons include dynamic exit numbers and leg names). Reject; pin only the ID token.
- **F5 wrong-class pass.** With the H1 root bug, a "missing input" case expecting `2 / missing_input` passes for the wrong reason. Reject unless the clean positive case (D) also passes in the same run.
- **F6 helper-only green.** A selftest that calls `decide()` or `evaluate()` in-process instead of the CLI passes without exercising exit mapping. Protocol §Gate standard rejects helper-only self-checks.
- **F7 existing-receipt overwrite.** A selftest that only checks the file exists after the run cannot see an overwrite. Require the pre-existing file's bytes and sha256 to be unchanged (criterion H3).
- **F8 dead or unreachable IDs.** `baseline_has_GIT_DIR` is unreachable (`safe_env` strips all `GIT_*`). `poison_path_exists` cannot be reached hermetically without writing to `/nonexistent`. A coverage statement that claims all IDs are pinned would be false.
- **F9 round-14 pins read as current.** `decide()` checks live sibling digests; a clean run on the current tree says nothing about the round-14 revision. The round-15 receipt must record the revision and the digests it read.

## Unearned claims to reject

- **U1 "both exit64 classes explicit."** The historical source has one 64 path (`main()` 605–613: unexpected argv). No second 64 class exists in the tree. Accept only if the executor enumerates two literal 64 IDs with two distinct parse surfaces (for example a second subcommand that has its own usage error) and pins both. Otherwise drop the phrase.
- **U2 "context gate correctly registered."** Accepted only once the registry row (F above) exists in `SKILL.md` with kind `gate`, 64 declared, selftest command, pinned values, and write scope. The current row (`SKILL.md:1602`) is a "probe" with "no standalone selftest" and no 64.
- **U3 "frozen digest-bound retained run" over the round-14 receipt.** The round-14 receipt is not replayable by the new tool: it contains `observed_at`, absolute `lane_root`/`fleet_root`, `invocation.argv/cwd`, ambient env policy, and `tool_sha256` of the historical bytes. The new tool must produce its own round-15 receipt and its own snapshot expectation. Reject any claim that round-14 was replayed.
- **U4 "standalone isolated exit+finding selftest."** Accept only if it meets criteria B–D. A selftest that prints lines without comparing them to committed literals, or that asserts exit only, is not standalone evidence under the protocol.
- **U5 score movement.** claims.json says 6→6, "no promotion points." Reject any statement that calibration or scalar moved.
- **U6 "hermetic, no writes outside temp roots."** Reject if the selftest needs the real fleet root, writes `/nonexistent`, or uses the real `.ufo/evidence/round-15/` path.
- **U7 "help is green."** Reject treating `help_printed` as clean evidence (criterion G).
- **U8 "no new broad environment claims."** Acceptable only if the tool adds no environment reads beyond those already present (`PATH` lookup for `python3` and `git`, the explicit `GIT_DIR` injection, and the `LC_ALL=C` policy). Any new `--root` flag or env override is a new claim and must be declared in the registry's environment column.

## Recommendations (bounded)

1. Promote the historical file by copy-then-edit into `tools/context-capture.py`; leave `.ufo/evidence/round-14/capture-context.py` bytes unchanged. Fix H1 (two-level root derivation) and add the clean positive case (D) that proves it.
2. Move `base_receipt()` inside the `try`; add a top-level `except Exception` → exit 2 `setup_error`; add the malformed-legs case → `probe_baseline_unusable` (H2).
3. Define a single FINDINGS table in the tool (ID → exit class) and emit it as the last stdout line, e.g. `CONTEXT_CAPTURE: finding=<id> exit=<n>`. Reuse `InvalidContext.kind` strings as setup IDs. Map each decide() branch to one literal ID: `injected_observation_differs`, `payload_tool_sha256_mismatch`, `env_delta_mismatch`, `baseline_has_GIT_DIR` (unreached by design), `positive_control_ineffective`, `probe_source_digest_mismatch`, `runner_source_digest_mismatch`, `runner_mapping_mismatch`, plus sub-IDs for the six mapping checks (`header_matches_manifest`, `pin_name_and_value_match_manifest`, `rev_name_and_value_match_manifest`, `leg_call_matches_manifest`, `constant_names_match_leg`, `leg_set_mismatch`, `leg_order_mismatch`). These names are proposals.
4. Argparse-free dispatch (matching repeat-control's `dispatch()`), or a `UsageParser` that exits 64. Usage → `usage_error` (64). `-h/--help` → 0 with `help_printed`, stated as non-verdict.
5. Red-control decision (integrator call, not silently changed): `SKILL.md:148` says a red control is a setup failure. Historical `decide()` 570–571 maps a red or ineffective positive control to 1. Either (a) keep historical semantics and pin the ID as `failed` in the registry, or (b) split baseline-red (`2 / positive_control_baseline_unusable`) from ineffective-with-working-baseline (`1 / positive_control_ineffective`). Recommend (b) because it matches the stated standard; the reuse instruction in the spec permits either only if the registry says which.
6. Injected-run unusable (`comparison_block` 371–375) maps to 1 in historical semantics. Keep it (reuse instruction), but pin it as `injected_observation_differs` with a literal case, and list it in the registry's exit-1 row.
7. Add `--snapshot DIR` and `--check RECEIPT` (receipt consistency: schema, decision equals recorded exit, recorded digests equal recomputed digests) with their own literal IDs and usage handling. `--check` exits 2 on unreadable input, 1 on an inconsistent receipt, 0 on consistent.
8. Overwrite refusal (H3): exclusive create (`os.open` with `O_EXCL`) or a pre-existence check that returns exit 2 `output_exists`, with a selftest case that asserts the pre-existing bytes are unchanged.
9. Registry (`SKILL.md`): replace the "probe" row with a gate row carrying every column in criterion F, and list the 64 class explicitly. Do not edit the historical round-14 row; add a round-15 row.

## Verification gaps (not executed; per assignment)

- Nothing above was run. Hazards H1 and H2 are derived from source reading and should be confirmed by the main agent's single post-integration run (for example: `python3 tools/context-capture.py extra` expects 64; a copied tool at a temp root expects the temp lane root).
- The new file does not exist at revision `a9cf4da`; criteria A–G must be re-checked against the file once it lands.
- The two-64-class wording (U1) cannot be checked until the executor enumerates them.
- Whether the poison path can ever be exercised without writing outside temp roots is unresolved (F8); this review does not claim it can.
- Exact `argparse` behaviour under the repo's Python is recorded only by round-12 probes (3.14.7); the current interpreter was not re-measured.

## Residual risk

- Stable IDs are only as stable as the literal table; a future decide() branch added without a table entry would silently become `could-not-evaluate` through the protocol default. A static check that every `decide()` reason maps to a FINDINGS key would close this, but that is a further gate claim and is not recommended for round 15.
- Exit 2 remains ambiguous at the exit level (historical G-6 pattern). Consumers must key on the finding ID.
- The C1 capability remains a finite-control claim: it does not establish environment independence, result reuse, or a mutation rate.
