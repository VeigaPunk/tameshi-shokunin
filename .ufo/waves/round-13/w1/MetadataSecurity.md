# MetadataSecurity: round-13 read-only security boundary review

Scope: `tools/witness-metadata.py` and `.ufo/evidence/round-13/witness-metadata.json`. Covered: untrusted paths, malformed JSON, missing-digest bypass and honest could-not-evaluate states.

I ran no checks, gates, selftests or tool invocations, and edited nothing in the implementation. Reads, `sha256sum`, `jq`, `stat` and `git ls-files -s`/`hash-object` were the only commands. I installed or updated no tools.

Reviewed snapshot (still landing concurrently; line numbers refer to this snapshot):
- `tools/witness-metadata.py`: sha256 `176503afd1abdcd9cdf1ab927e62debfc467604e0faf43d711fed8933493bf13`, 1088 lines
- companion: sha256 `463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d`

The defects were sent to `TameshiR13.MetadataRepair`, together with an earlier contract message sent before the implementation landed.

## Frozen inputs (unchanged at review time)
| file | sha256 | git blob (index) |
|---|---|---|
| round-12/BashWitness/summary.json | acc01268…47b9 | ac4e227b…5dad (matches `hash-object`) |
| round-12/BashWitness/declaration.json | e8d2024a…0901 | 7fb79463…5819 (matches) |
| round-12/BashWitness/rerun-20261020T035435Z/summary.json | 6726421f…f5f0 | 045370ef… |

No symlinks exist under `.ufo/evidence/round-12/BashWitness` or `.ufo/evidence/round-13`. The rerun summary's `declaration.kind` is `null`, which matches the companion's scope claim.

## Boundaries that hold (no green bypass found)
- **Companion paths are never opened.** A companion `path` must equal the pinned literal (`:392-395`). Reads use the tool's `PINNED_INPUTS` rel (`:68-84`), never the companion's value. Absolute paths and `..` are rejected first (`:308-317`).
- **Inputs are walked safely.** Every component is checked with `lstat`; symlinks and non-regular files are rejected, and the resolved path must stay inside the lane (`:320-345`).
- **Missing-digest bypass is closed.** A missing or non-hex digest gives exit 2 `companion_digest_invalid` (`:396-398`). A digest that differs from the tool's literal gives exit 2 `companion_digest_unpinned` (`:399-400`). An extra or missing input entry gives exit 2 `companion_inputs_mismatch` (`:380-385`). The authority is the tool's literals, not the companion, so the companion cannot certify itself.
- **Malformed JSON is classified.** Invalid UTF-8, malformed JSON, duplicate keys (`object_pairs_hook`), NaN/Infinity (`parse_constant`) and a non-object top level all give exit 2 `input_unavailable` (`:283-305`).
- **Unexpected exceptions fail closed.** The catch-all at `:1074-1081` maps them, including RecursionError, to exit 2 `unexpected_exception`. Exit 0 is never reachable by accident.
- **Smuggled extras are rejected.** `companion != build_companion()` (`:588`) catches extra keys such as `preregistration: "blind"`. The bool/int aliasing that dict equality would allow (`1 == True`) is closed earlier by the `is True` / `is False` / `type(...) is int` checks (`:373, :424, :440, :561-566, :580-583`).
- **Selftest isolation holds.** Fixtures live under `tempfile.mkdtemp` and are removed in a `finally` block (`:932-984`). Frozen bytes are re-hashed before and after (`:909-930, :987-1003`).

## Findings
| sev | defect | exploit path | evidence | smallest remediation |
|---|---|---|---|---|
| **M1** | A tamper can be masked by exit 1, so the honest state is lost. | Tamper the rerun summary and also set `producer.checked_live=true` in the companion. Result: exit 1 `producer_checked_live_invalid`; `snapshot_tampered` is never reported. The same masking happens when the `schema` or `expected` checks fail while summary or declaration bytes are tampered. | The rerun summary is hashed at `:475-481`, after the exit-1 companion checks at `:416-471`. The schema and expected checks (`:363-374`) run before the frozen hash loop (`:403-409`). The docstring at `:23-25` claims integrity before comparison. | Hash all four pinned files (fold `:475-481` into the `:403` loop) before any exit-1 comparison. Add a selftest arm: tamper plus companion defect → exit 2. |
| L1 | The bytes that are hashed are not the bytes that are parsed (TOCTOU). | A concurrent writer swaps a frozen file between the hash and the parse. The result is a green verdict with `inputs_verified` listing bytes that were never compared. | `:405` hashes `read_bytes()`, then `:412-413` and `:482` re-read from disk inside `load_json_object`. | Parse the exact hashed `raw` bytes, e.g. with a `load_json_bytes(raw, label)` helper. |
| L2 | The companion path is unconstrained and the lane root is not reported. | Run `--lane-root /tmp/pristine-copy --companion <lane>/.ufo/evidence/round-13/witness-metadata.json`. It prints green naming the lane's companion while the frozen bytes of another tree were verified. | `:358` uses `is_file()`, which follows symlinks. An absolute `--companion` is accepted (`:1060`). The result omits the lane root (`:591-598`). | Pass the companion through `safe_input_path` under the lane, and emit the resolved `lane_root` in the result line and JSON. |
| L3 | Usage errors exit 2, colliding with `input_unavailable`. | A misspelled flag or a missing mode returns argparse's exit 2, which a caller would read as could-not-evaluate or tamper. | `:1018-1048`. The lane convention is exit 64 for usage errors (`tools/bash-witness-study.py:74,118`). | Override `parser.error` to exit 64. |
| L4 | The selftest leaves security arms unproven. | Symlink-component rejection, a declaration.json tamper, NaN, invalid UTF-8 and non-object JSON have no fixture. The subprocess inherits `PYTHONPATH`, and `tools/` is first on `sys.path`. An uncaught `TimeoutExpired` at `:940-952` produces a traceback instead of a named failure. | `SELFTEST_CASES` at `:625-800` has no `symlink`, NaN or UTF-8 case. | Add those arms, run the subprocess with `[sys.executable, "-I", …]`, and catch `TimeoutExpired` as a named FAIL. |

## Exact checks for L1 (not executed here)
1. `sha256sum tools/witness-metadata.py .ufo/evidence/round-13/witness-metadata.json`: confirm whether the code moved past the reviewed snapshot; if it did, re-anchor the line numbers above.
2. `sha256sum .ufo/evidence/round-12/BashWitness/{summary.json,declaration.json,declared.tsv} .ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json`: expect `acc01268…`, `e8d2024a…`, `0def0d3b…`, `6726421f…`.
3. `git diff --exit-code -- .ufo/evidence/round-12`: expect no diff.
4. `python3 tools/witness-metadata.py --check --json`: expect `{"id":"metadata_consistent","exit":0}` and process exit 0.
5. `python3 tools/witness-metadata.py --selftest`: expect `SELFTEST: PASS N/N` with every literal expected ID and exit matched, and no `FROZEN_MUTATED` line.
6. M1 probe (only in a temp copy of the lane, never in place):
   - Copy the four pinned files and the companion into a tempdir.
   - Append one byte to the rerun summary.
   - Set `producer.checked_live` to `true` in the companion.
   - Run `--check --lane-root <tmp> --json`.
   - Expected after the fix: exit 2 `snapshot_tampered rerun_summary_digest_mismatch`. The current code gives exit 1.
7. L3 probe: `python3 tools/witness-metadata.py --chek; echo $?`. Expected after the fix: 64. The current code gives 2.
8. `find .ufo/evidence/round-12 .ufo/evidence/round-13 -type l`: expect no output.

## Residuals
- No green bypass was found. All findings concern honest exit-2 classification, reporting and selftest coverage.
- `checked_live: false` for the producer and runner is disclosed honestly. Those identities come from frozen JSON fields, not from hashing the live tools, which is intended.
- The implementation was still landing during review, so the owner may close M1 and L1–L4 after this snapshot.
