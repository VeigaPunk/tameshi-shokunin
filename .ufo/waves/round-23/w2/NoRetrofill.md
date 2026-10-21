The no-retrofill axis holds. Old receipts with missing argv or truncated tails are byte-for-byte unchanged, and the full streams exist only in the new replay. I found no blocking counterexample. There are three smaller calibration findings. No report file was written, because this wave forbids report writes, so these findings are for L1 to persist. I ran only read-only `git show`, `git diff` and `git log` plus local JSON parsing, nothing else. No tools were installed.

**How the axis was checked**
- **Old files unchanged:** across `28cae179..336565f`, every file outside `round-23/` only gained lines. The one exception is `tools/registry-check.py`, which changed 2 lines to add an opt-in `retain_streams=False` parameter. With that default, ordinary output still carries only the tails (`stdout_tail` and `stderr_tail`, no full streams); `registry-C.json` confirms this for the current battery.
- **Ledger prefix intact:** `round-21/coldread/ledger.json` grew from 249 to 264 entries. The first 249 entries and every other top-level key are equal to the `8f66b5d` version when parsed as data.
- **Registry rows intact:** `tools/registry.json` only appends three `new-r23` rows. The frozen argv and expect values are not changed.
- **Uncommitted files:** the uncommitted `LOG.md` and `SCORECARD.md` changes are also append-only.
- **Replay data is consistent:** the bundle digest matches `expected.json` (`3d6c99b7…`). The bundle's requirements match `requirements.json`, and `registry-baseline.json` has the same SHA-256 (`ebd2e69a…`) as the real `28cae179:tools/registry.json`.
- **Full streams:** for all 43 rows, the bundle's stdout and stderr equal the runner's full streams. Every truncated tail (4096 bytes) is a suffix of its full stream; 12 rows were actually truncated. No stream was empty, and no row came near its timeout (the slowest used 13% of its limit). No stream contained the Unicode replacement character, so the "complete decoded" label is accurate here.
- **Instrument hashes and ordering:** `replay.py`, `registry-check.py`, `receipt-measure.py` and `command-binding.py` each hash identically at `496d212`, `8f66b5d` and `336565f`. `requirements.json` was committed at 14:41:18 UTC, before the replay started at 14:42:22.
- **Source-read substitution receipt:** the receipt for `cat tools/registry.json` copies the actual source-read run exactly. Its real argv is kept, not replaced with the required argv, so `ARGV_MISMATCH` is genuine.
- **Wording:** the docs scope the claim to "not retrofilled historical fields", and nothing claims to close historical R17-CMD-BIND.

**Finding 1: the replay's argv, membership, cwd and revision checks cannot fail** (calibration tradeoff, not a defect)
- **Counterexample:** in `replay.py`, each receipt's `argv` is copied from `row['argv']`, its name from the requirement, and its cwd and revision from the same variables as the bundle's. So `ARGV_MISMATCH`, `MEMBERSHIP_MISMATCH`, `CWD_MISMATCH` and `REVISION_MISMATCH` are impossible by construction. The clean result in `replay-gate-A.json` only adds evidence on exit codes and stdout tokens beyond what `REPLAY: 43/43` already shows.
- **Why it isn't false provenance:** `Popen` runs exactly `row["argv"]`, so the recorded argv is the real invocation, not the process's observed command line.
- **Correction:** describe the replay result as an exit/token binding with argv equal to the declaration by construction. Keep the source-read and correct-command pair as the only real argv discriminator.

**Finding 2: the bundle drops the "external" marker** (minor provenance loss)
- **Counterexample:** the `pin-disposition-read` row carries `non_hermetic_argv: ['/home/vgpnk/Projects/shokunin']` in `observations.json`, meaning it reads live parent-directory state. Its bundle receipt has no such marker and looks the same as the 42 hermetic rows under revision `496d212`. That revision string does not cover what this row read.
- **Correction:** state in the claim that one of the 43 rows is a declared external, live-state row whose revision binding is partial. Do not change the frozen bundle.

**Finding 3: missing streams would silently become empty strings** (latent; currently harmless)
- **Counterexample:** `replay.py` uses `.get('stdout', '')`, so a row that timed out or was unavailable would get an empty stream filled in. Its exit would be a string, so the gate would reject it with exit 2 (`INVALID_RECEIPT`). A second case is not covered by that: if the main process exits but a stray child keeps the pipe open, the runner may record a cut-off stream as complete.
- **Correction:** have future replays fail when `stdout` is absent instead of defaulting to an empty string. No rerun is needed for the present evidence.

**Smaller notes**
- `census-start.json` and `census-after-curation.json` are new receipts that record no cwd, revision or timing. They aren't used as required-command receipts, but they are weaker than the other round-23 receipts.
- The 15 appended ledger entries each have `commands_executed_count: 1`. That counts the `python3 -c` reader command and is literally true. No `.py` file reads that field, and both the ledger provenance and the knowledge doc disclaim command coverage, so no credit leaks.

**Axes affected:** calibration (findings 1 and 2), provenance (findings 2 and 3), and maintainability (finding 3). Correctness and no-retrofill are not harmed.
