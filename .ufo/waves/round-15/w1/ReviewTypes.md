# ReviewTypes — round-15 C1 review: bool-versus-integer exits and container types

Seat: `TameshiR15.ReviewTypes` (reviewer, leaf). Lane: tameshi-shokunin. Report: `.ufo/waves/round-15/w1/ReviewTypes.md`.

## Read revision and scope

- Read revision: `tameshi-shokunin` HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0`. Working tree: `tools/` and `.ufo/evidence/round-14/` clean; only `?? .ufo/waves/round-15/` is untracked.
- `tools/context-capture.py` **does not exist** at this revision (`ls` → no such file). Nothing below describes implemented source. Every "tools/context-capture.py" reference is a requirement, not an observation.
- Historical source read in full: `.ufo/evidence/round-14/capture-context.py` (647 lines), git blob at commit `0c6e36d`, sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`. This equals `tool_sha256` in `.ufo/evidence/round-14/context-receipt.json:4` and the pins in `verification.json` / `expected-runtime*.json`, so these are the executed bytes.
- Stale digest, noted for provenance: `.ufo/waves/round-14/w1/ReceiptHarness.md` records `1ffda07b…` for a 644-line version. That is not the executed file. Do not cite `1ffda07b…` as the script's identity.
- Sibling precedent read: `tools/evidence-disposition.py` (r14, sha256 `1609a9df…`), used only as a reference pattern.
- Registry evidence: `SKILL.md:1602` (round-14 registry row for invocation context capture); round-14 `VerdictContract.md:17–19, 31–33` (protocol Gate standard as quoted there). The protocol file itself was not locatable in this tree, so protocol claims are taken from that quotation and marked as such.
- Executed: read-only file reads, `sha256sum`, and read-only `git log/show/diff/status`. No gate, selftest, probe, runner, build, test, or formatter was run. No tool was installed or updated. No file was written except this report. The historical script was not edited.

## Verdict

C1 cannot be accepted on exit classes as the round-14 registry currently states them. The historical source has five reachable defects in exit-class and type handling, which the promoted tool must correct (it must not edit the historical file). The fixes are bounded and listed below with literal acceptance cases. Do not admit a C1 claim that depends on type-strictness, exit-64 classification, or stable finding IDs until the criteria in §3 and §4 hold in the executed tool.

## 1. Evidence index (historical, line numbers from the read)

| Ref | What it shows |
|---|---|
| `capture-context.py:26–29`, `:123` | Docstring exit map: `0` ok; `1` mismatch "including injected run unusable"; `2` could-not-evaluate; `64` usage, no receipt. |
| `:196–208` (`run_bounded`) | Timeout, missing executable, exec failure, and non-UTF-8 output all raise `InvalidContext`. |
| `:340–347` (`parse_probe_document`) | Plain `json.loads`. Catches only `JSONDecodeError`. No duplicate-key rejection, no NaN/Infinity rejection. |
| `:352–357` (`comparison_block`) | Baseline check runs `row.get(...)` and `row.get("pinned", {}).get("status")` on every element of `base["legs"]` with no per-row `dict` check. |
| `:404–409` (`positive_control_block`) | `reflects = POISON in injected.stdout or POISON in injected.stderr or injected.exit != baseline.exit`; `effective = baseline_ok and injected.exit != 0 and reflects`. |
| `:539–540` | Baseline and injected `run_bounded` are called with no local guard. |
| `:553–580` (`decide`) | Strict `is not True` / `is not False` at `:560, :564, :566, :568, :570`. Truthiness `not …` at `:572, :574, :576`. Free-text reasons at `:561–577`. |
| `:605–628` (`main`) | Catches only `InvalidContext` (`:617`). No catch-all. Any other exception escapes; Python exits 1, which is the "mismatch" class. |
| `:618` | Invalid-input receipts use `status: "invalid_input"`, `exit: 2`, and carry no comparison or mapping. |
| `:637–642` | Console line is `print`-only; not a gate contract. |
| `context-receipt.json:80, 94, 132, 145` | Retained run exits are JSON integers (`0`, `128`). `:147` shows git's stderr containing the poison path. `:411` `all_match: true`. |
| `SKILL.md:1602` | Round-14 registry row for capture-context: verdict map `0`, `1`, `2` only; "no standalone selftest". **No row for 64.** |
| `VerdictContract.md:17–19` | Protocol Gate standard, as quoted: every nonzero code must be declared and mapped to clean/failed/could-not-evaluate; an undeclared code reads as could-not-evaluate; a selftest must assert both exit and a stable finding ID. |
| `VerdictContract.md:31–33` (H2, H3) | Uncaught exception → exit 1 (wrong class); argparse usage → exit 2 (wrong class for 64). |
| `evidence-disposition.py:147–148, 1930–1941` | Sibling precedent: `UsageError` → 64 without argparse. |
| `evidence-disposition.py:166–176` | Sibling precedent: duplicate-key rejection and `parse_constant` rejection. |
| `evidence-disposition.py:197–198` (`_is_int`) | Sibling precedent: `type(value) is int`. |
| `evidence-disposition.py:1506–1507` (`_status_for`) | `{0:…,1:…,2:…}.get(exit_code)`. **Hazard:** bool keys collide with int keys (see F3). |
| `evidence-disposition.py:1948–1952` | Sibling precedent: catch-all `except Exception` → could-not-evaluate exit 2. |

## 2. Findings (severity order)

Severity: **high** = misclassifies an outcome or passes a false claim, reachable by a retained-receipt check or a malformed input; **medium** = class or claim is ambiguous or overstated; **low** = provenance or hygiene. The live capture path produces only Python-constructed bools and ints, so some high findings are reachable only through the new retained-receipt check; each finding says which.

### F1 (high) — container-type errors escape as exit 1

- **Evidence:** `:352–356` indexes `row` and `row.get("pinned", {})` without a `dict` check; `:344` calls `json.loads` with no catch beyond `JSONDecodeError`, so deep nesting raises `RecursionError`; `:629` `decide` uses `receipt.get("comparison") or {}` (`:554–557`), so a non-dict truthy value raises `AttributeError`; `:615–628` has no catch-all. Result: `AttributeError` / `RecursionError` / `TypeError` exit 1 with a traceback, which reads as the "mismatch" class. [INFERENCE from static reading; not executed.]
- **Reachability:** baseline stdout from the probe (`tools/pin-disposition.py` output), and any retained-receipt input in the new CLI.
- **Acceptance criterion:** the promoted tool has a top-level catch-all that maps any uncaught exception to `setup_error`, exit 2, with no traceback on stderr (mirror `evidence-disposition.py:1948–1952`). Every container is type-checked before use: root object, `legs` list of exactly 6 with dict rows, `pinned` dict or absent, `comparison`/`mapping`/`sources`/`environment`/`runs` dict. Non-conforming shape is `probe_baseline_unusable` (baseline) or `receipt_malformed` (retained receipt), exit 2.

### F2 (high) — truthiness on boolean predicates accepts non-bool values

- **Evidence:** `decide` `:572`, `:574`, `:576` use `not (…).get(…)` truthiness while `:560–570` use `is True`/`is False`. Concrete false positive: a retained receipt with `"all_match": "false"` gives `not "false"` = `False`, so no reason is added and `decide` returns ok/0. The same holds for `"matches_declared": "no"`, `1`, or `[]`-free strings. A string `reasons` value would also be split character-by-character by `reasons.extend` (`:577`), which changes reasons but not the exit.
- **Reachability:** none in the live path (those values are constructed as bools at `:501–508` and `:316–335`). Reachable only through the retained-receipt check.
- **Acceptance criterion:** every boolean predicate in `decide` and in the receipt validator uses `is True` or `is False`. A retained predicate field that is not a JSON boolean is `receipt_malformed`, exit 2. A JSON `false` is a mismatch, exit 1, with its stable finding ID. `reasons` must be a list of strings, else `receipt_malformed`.

### F3 (high) — bool-as-integer exit codes

- **Evidence:** in Python `True == 1`, `False == 0`, and `hash(True) == hash(1)`. The live code compares exits with `== 0` / `!= 0` (`:403, :409, :406`) on values it constructed as ints, so it is safe. Any retained-receipt comparison of `exit`, `status`, or a top-level exit against an int literal is unsafe: `"exit": false` passes `== 0`; `"exit": true` passes `== 1`; `"exit": 0.0` passes `== 0`. The sibling `_status_for` (`evidence-disposition.py:1506–1507`) maps a bool key to a status silently. The sibling has `_is_int` (`:197–198`) but the historical file has no equivalent.
- **Acceptance criterion:** every exit value read from a retained record is validated with `type(x) is int` before any comparison or dict lookup. Failure is `receipt_malformed`, exit 2. Top-level `status` must agree with exit under the fixed map `ok↔0`, `mismatch↔1`, `invalid_input↔2`; disagreement is `receipt_malformed`, exit 2. Do not copy `_status_for` into the new tool without an `_is_int` guard.

### F4 (high) — exit 64 undeclared and unclassified

- **Evidence:** `:605–613` returns 64 for unexpected arguments and writes no receipt. The round-14 registry row (`SKILL.md:1602`) lists 0, 1, and 2 only. Per the quoted protocol, an undeclared nonzero code reads as could-not-evaluate, and the round-14 lesson (`corpus/lessons/round-14-verifier-spotcheck.md`, routed defect 5) explicitly requires an explicit could-not-evaluate class for 64. The historical 64 path also prints no stable finding ID. Argparse would exit 2, not 64 (`VerdictContract.md:33`); do not use argparse for the 64 path.
- **Acceptance criterion:** the new registry row maps `64` → could-not-evaluate (precedent: `repeat-control` "2 and 64 could-not-evaluate", round-12 registry). Usage errors print `usage_error` on stderr and exit 64, using a `UsageError` class (`evidence-disposition.py:147–148, 1930–1941`). Selftest pins `usage_error` with exit 64 for at least `--bogus` and for an extra argument to `--selftest`.

### F5 (medium) — exit-class contradiction between docstring and code for injected runs

- **Evidence:** the docstring and exit map (`:26–29`) say `1` covers "injected run unusable". The code does this only for non-zero exit or non-JSON stdout (`:371–375`, `comparison_block`). Timeout, non-UTF-8 output, missing executable, and exec failure on the **injected** run raise `InvalidContext` from `run_bounded` (`:196–208`), are not caught by the `comparison_block` path, and reach `main` at `:617`, which exits **2**. Baseline failures also exit 2, which is consistent. So the documented class for injected failures differs from the executed class depending on failure mode.
- **Acceptance criterion:** pick one rule, state it in the new docstring and registry row, and pin it. Recommended: an injected run that produces an observation with non-zero exit or non-JSON stdout is `injected_observation_differs`, exit 1; an injected run that produces no observation at all (`timeout`, `non_utf8_output`, `exec_failed`, `missing_executable`) is could-not-evaluate, exit 2. Timeouts and exec failures cannot be pinned by a fixture-only selftest; the registry must say so (see §6, gap G2).

### F6 (medium) — probe JSON accepts duplicate keys and non-finite constants

- **Evidence:** `parse_probe_document` (`:340–347`) uses plain `json.loads`. Its neighbour `parse_json` (`:158–181`) rejects duplicate keys, and the sibling rejects NaN/Infinity (`evidence-disposition.py:175–176`). Duplicate `status` or `observed_at` keys resolve last-wins, so a baseline can pass `status == "ok"` while its first occurrence says otherwise. Identical duplicates in both runs also yield `equal: true`.
- **Acceptance criterion:** probe stdout is parsed with the same duplicate-key and constant rejection as `parse_json`. Baseline failure → `probe_baseline_unusable`, exit 2. Injected failure → `injected_observation_differs`, exit 1.

### F7 (medium) — decide reasons are free text, not stable finding IDs

- **Evidence:** `decide` `:561–577` produces sentences. The spec requires literal expected finding IDs. The historical `InvalidContext.kind` values (`missing_input`, `unreadable_input`, `invalid_utf8`, `invalid_json`, `invalid_manifest`, `invalid_expected`, `invalid_fleet_root`, `poison_path_exists`, `missing_executable`, `timeout`, `exec_failed`, `non_utf8_output`, `runner_unparsed`, `probe_baseline_unusable`) are already stable and should be reused.
- **Acceptance criterion:** each `decide` reason gets one stable ID. Proposed IDs for exit 1: `injected_observation_differs`, `probe_payload_digest_mismatch`, `env_delta_not_declared`, `baseline_has_git_dir`, `positive_control_ineffective`, `probe_source_digest_mismatch`, `runner_source_digest_mismatch`, `runner_mapping_mismatch` (with per-check sub-IDs such as `runner_leg_set_differs`, `runner_leg_order_differs`, `runner_leg_<leg>_<check>`). New exit-2 IDs: `receipt_malformed`, `setup_error`, `usage_error` (64), and `snapshot_tampered` if a snapshot mode is added.

### F8 (medium) — positive-control `reflects` is weaker than its name

- **Evidence:** `:404–406` sets `reflects` true when the injected exit differs from the baseline exit, even if neither stream contains the poison path. The env delta is exactly `GIT_DIR` (`:527–530`, `:533–534`), so an exit difference is attributable to the injection, but it does not show that git read the path. The retained stderr does show that (`context-receipt.json:147`).
- **Acceptance criterion:** either (a) require the poison path in injected stdout or stderr and name the field `poison_path_observed`, or (b) keep exit-difference semantics and rename the field to `injected_exit_differs`. The claim must not say that the poison path was reflected under (b). Recommended: (a), since it is tighter and matches the retained evidence. Record which option was chosen in the registry row.

## 3. Likely false positives (reject these readings)

- **FP1.** A selftest case that expects exit 1 and passes because the code raised an uncaught exception. Protect against this by pinning the stable finding ID and by failing any case whose stderr contains `Traceback`.
- **FP2.** Round-14 retained receipts show the type is correct. They do not. Every value they contain is produced by the tool and is a JSON integer or boolean. They cannot exercise F1–F3, so their passing is no evidence about type handling.
- **FP3.** `status: "invalid_input"` (`:618`) disagrees with the registry's "could-not-evaluate". This is a naming difference, not an exit-class error. Accept it only with an explicit `invalid_input` → could-not-evaluate line in the new registry row.
- **FP4.** `baseline_has_GIT_DIR is not False` (`:568`) rejects `0` and `None` as well as `True`. This is conservative and correct. Do not report it as a bug.
- **FP5.** `payload_tool_sha256_matches_disk` (`:564`) and `env_delta_matches_declared` (`:566`) are already strict. Do not report them as F2 findings.

## 4. Unearned claims to reject

- **U1.** "C1 decide is type-strict." Reject until F2 is fixed: three predicates use truthiness.
- **U2.** "Exit 64 is could-not-evaluate." Reject unless the registry row says so. The round-14 row lists no 64.
- **U3.** "Uncaught errors are could-not-evaluate." Reject for the historical script, which exits 1 on them. Accept for the new tool only after the catch-all and a fixture that triggers it.
- **U4.** "The positive control proves the poison path is reflected." Reject as written; it proves only that the injected exit differs (F8).
- **U5.** "The retained-receipt check handles malformed receipts." Reject unless fixtures for F1–F3 exist and pass.
- **U6.** "Selftest verifies exit codes." Reject if it checks only exit. The protocol requires exit and stable ID together.
- **U7.** "Decide reasons are stable finding IDs." Reject until F7's table is implemented.
- **U8.** "`1ffda07b…` identifies the executed capture-context.py." Reject. The executed digest is `7313e9a2…`.
- **U9.** "argparse gives usage exit 64." Reject. argparse gives 2 (`VerdictContract.md:33`).
- **U10.** "Injected-run failures are exit 1, as documented." Reject: the code gives exit 2 for timeout, non-UTF-8, and exec failure (F5).

## 5. Exact acceptance criteria and proposed selftest cases

These are a recommendation for the owner of `tools/context-capture.py`. Each case is an isolated `mkdtemp` snapshot fixture (see G1), invoked via a subprocess of the public CLI, asserting **literal exit and stable ID together**, and failing on any `Traceback` in stderr.

| Case | Input (synthetic fixture) | Expected exit | Expected stable ID |
|---|---|---|---|
| C01 | `--bogus` | 64 | `usage_error` |
| C02 | `--selftest extra` | 64 | `usage_error` |
| C03 | `--help` | 0 | (usage text on stdout) |
| C04 | baseline run `exit: false` | 2 | `receipt_malformed` |
| C05 | baseline run `exit: 0.0` | 2 | `receipt_malformed` |
| C06 | retained receipt `mapping.all_match: "false"` | 2 | `receipt_malformed` (not 0) |
| C07 | retained receipt `mapping.all_match: false`, reasons `["leg x: …"]` | 1 | `runner_mapping_mismatch` |
| C08 | retained receipt `sources.probe.matches_declared: 0` | 2 | `receipt_malformed` |
| C09 | top-level `exit: true`, `status: "mismatch"` | 2 | `receipt_malformed` |
| C10 | `status: "ok"`, `exit: 1` | 2 | `receipt_malformed` |
| C11 | baseline probe `legs` contains a string element | 2 | `probe_baseline_unusable` |
| C12 | baseline probe row with `pinned: null` | 2 | `probe_baseline_unusable` |
| C13 | baseline probe stdout with duplicate `status` key | 2 | `probe_baseline_unusable` |
| C14 | injected probe stdout with duplicate `status` key | 1 | `injected_observation_differs` |
| C15 | baseline probe stdout deeply nested (RecursionError trigger) | 2 | `setup_error` or `invalid_json` (pick one, pin it) |
| C16 | injected run `exit: 128`, no poison path in streams | 1 | `positive_control_ineffective` or `injected_observation_differs` (per F8 option pinned) |
| C17 | `reasons` is a string, not a list | 2 | `receipt_malformed` |
| C18 | `environment.baseline_has_GIT_DIR: 0` | 2 | `receipt_malformed` |

Acceptance also requires: no case exits 1 with `Traceback` in stderr; all exit comparisons use integers validated with `type(x) is int`; the 64 mapping appears in the registry row; the historical file is byte-identical to `7313e9a2…` after the round.

## 6. Recommendations (bounded)

1. Promote `capture-context.py` to `tools/context-capture.py`. Do not edit the historical file.
2. Add the catch-all (F1) and the type-validation layer (F1–F3) before any `decide` reuse.
3. Use `UsageError` for 64 (F4) and a registry row that maps 64 to could-not-evaluate.
4. Pick one injected-run exit rule and state it in the docstring and registry (F5). Recommended rule in §2.
5. Parse probe JSON with duplicate-key and constant rejection (F6).
6. Map every `decide` reason to a stable ID (F7). Reuse the existing `InvalidContext.kind` IDs.
7. Choose F8 option (a) or (b) and record it in the registry row.
8. Add a snapshot mode that accepts retained run records and digest-pins its inputs; drift is `snapshot_tampered`, exit 2. The selftest drives this mode, because the live probe cannot be steered to produce malformed shapes.
9. Keep the historical file's registry row unchanged; record the new tool as a separate row.

## 7. Verification gaps and handoff

- **G1.** Nothing was executed. All findings are static, from reading source and retained JSON. F1, F3, and F5 are [INFERENCE] until L1 runs the selftest cases in §5.
- **G2.** Timeouts, exec failures, and non-UTF-8 output on the injected run cannot be fixture-tested without a real process. The registry must say this is untested, not claim coverage.
- **G3.** The reachability of F1 from the live pin probe depends on `tools/pin-disposition.py` output shapes, which were not read in this pass. Treat F1's live reachability as unknown.
- **G4.** The protocol Gate standard is taken from its quotation in `VerdictContract.md:17–23`. The source file was not located in this tree.
- **L1 checks to run once after seats return:** `python3 tools/context-capture.py --selftest` (expect exit 0 and the case count); the §5 cases via the selftest; `sha256sum .ufo/evidence/round-14/capture-context.py` (expect `7313e9a2…`); and a check that `SKILL.md` round-15 row contains `64`.

## 8. Tool and install record

- Installs or updates: none.
- Reads outside the lane: `kimi-shokunin` path was attempted and not found; no content read from it.
- No credential, auth, or agent database file was read.
