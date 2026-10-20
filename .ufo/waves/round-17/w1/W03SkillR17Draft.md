# W03SkillR17Draft — SKILL.md section draft, round 17 (wave 1, leaf seat)

Scope: draft only. No lane file was edited, installed, or committed. The
section below is intended for the L1 integrator to append to SKILL.md after the
builders land. Tool names, flags, and exit codes are taken from the round-17
wave contract (interface contracts A, B, C) and from committed bytes at
`98bea7da5801f4bc58e4187690ee1687c8a5061f`. Nothing in the section was executed
by this seat. The v2/registry/measure/trace/assemble tools are not yet in the
tree (checked below), so every command for them is `[INFERENCE]` from the
contract until a builder's selftest and live run say otherwise.

## Evidence the seat read

| Fact | Command | Result |
|---|---|---|
| committed `tools/` at pin | `git ls-tree -r --name-only 98bea7da… \| grep tools` | `evidence-disposition.py`, `pin-disposition.py`, `mutate-and-run.sh`, `repeat-control.py`, `bash-witness-study.py`, `context-capture.py`, `witness-metadata.py`. No `registry.json`, `registry-check.py`, `trace-inputs.py`, `measure.py` v2, or `assemble.py`. |
| live tree state | `git --no-optional-locks status --porcelain` | `?? .ufo/evidence/round-17/`, `?? .ufo/waves/round-17/`, `?? .ufo/evidence/round-16/__pycache__/`. No round-17 tool yet at lane root. |
| v1 disposition exit contract | `sed -n 100,135p tools/evidence-disposition.py` at pin | `exit 0 clean`, `exit 1 failed semantic expectation`, `exit 2 could-not-evaluate bad/missing/tampered input`, `exit 64 usage error`; `status` values `clean`/`failed`/`could_not_evaluate`; schema `evidence-disposition-result-v1`. |
| v1 pin shape | `git show 98bea7da…:.ufo/evidence/round-14/dispositions.json` | `inputs` pins `.ufo/evidence/round-13/expected.json`, `verification.json`, `producer-oracle-repair.json` by sha256. The round-14 manifest does not pin any `tools/` path, so the R16-OP1 failure is a different manifest than the one shown here. |
| R16-OP1 red-before (live) | `.ufo/evidence/round-17/op1-redbefore-98bea7d.txt` | `exit=2`, `id: expected_input_digest_mismatch`, `tools/mutate-and-run.sh: observed 0673d2e5…8118aa expects 75ed934d…dc5`. A `tools/` pin moved on the live tree; the evidence did not change. This is the failure the v2 `historical_inputs` rule exists to fix. |
| registry shape | `git show 98bea7da…:.ufo/evidence/round-16/coldread/SKILL.snapshot.md` lines 1499–1510, 1676–1690 | Round-12 and round-15 registry tables are 8 columns. This section uses the 4-column shape the target asked for (Name, Kind, Command, Exits); the 8-column verdict/pin/write-scope/owner detail lives in the decision table and recipe below instead. |

## Section draft (paste into SKILL.md)

```markdown
## Live-tree re-pin, entry-command monitor and input-keyed cold-read — round 17

Three repairs. Each one has one question it answers and one exit contract.
Read the decision table first; the recipe and registry follow it.

### Decision table

| Condition | Decision | Error pattern / limit |
|---|---|---|
| A round-14-style manifest fails with `expected_input_digest_mismatch` on a path under `tools/` (lane instruments move by design) | Do not edit the old manifest (round-14 files are immutable). Append a new `evidence-dispositions-v2` manifest that keeps the same `inputs` pins and adds `historical_inputs: {"tools/<path>": {"rev": "<40-hex>", "reason": "<text>"}}`. The tool reads that path from `git cat-file blob <rev>:<path>`. | Digest of the rev blob must still equal the pin, else exit 2 `expected_input_digest_mismatch`. |
| A `historical_inputs` key does not start with `tools/` (for example `.ufo/evidence/...`) | Refuse. Evidence never moves; a historical read of evidence is a bug in the manifest. | exit 2 `historical_input_forbidden` |
| A `historical_inputs` key is not in `expected.json` `inputs` | Refuse. The pin must already exist before it can be re-read at a rev. | exit 2 `historical_input_unknown` |
| The rev does not exist, the object is missing, git is unavailable, or `git -C <root> rev-parse --show-toplevel` (realpath) differs from the root (realpath) | Refuse. Do not fall back to the live file. | exit 2 `historical_input_unavailable` |
| Every pinned input verifies (live for non-`tools/`, rev blob for `tools/` historical keys), and every expected effective row holds | Clean. | exit 0, `status: clean`, payload `expected_inputs_historical: {path: rev}` |
| Any effective row's receipt check no longer satisfies its original expectation | Failed semantic expectation. Record the id; do not rewrite the expectation to match. | exit 1, `status: failed` |
| The before manifest (`.ufo/evidence/round-17/dispositions-before.json`) is run | It is supposed to fail: `producer_before` must stay unresolved. | exit 1 `failed`. Exit 0 here means the before-state is accidentally clean: a defect, not a pass. |
| An entry-registry row's observed exit differs from its `expect.exit` at the tested rev | Record `differs` and the row name. Do not edit `expect` to match without a written reason in the report. | `registry-check.py` exit 1 (`ROW <name> expect=<e> got=<g> differs`) |
| Registry unreadable, invalid, rev missing, or clone failed | Could not evaluate. | `registry-check.py` exit 2 |
| Cold-read ledger entry has `commands_executed_count > 0` and `inputs` is empty | Uncredited. | `measure.py` reason `inputs-unrecorded` |
| Cold-read entry input path missing at REV | Uncredited. | `measure.py` reason `input-missing:<path>` |
| Cold-read entry input blob at REV has a different sha256 than recorded | Uncredited. This is what makes a bucket input-keyed. | `measure.py` reason `input-drift:<path>` |
| `external_inputs` (absolute paths, `repo@rev:path`) appear in a ledger entry | Reported, never credited. | `measure.py` lists them; no credit |
| `strace` is absent or setup fails under `trace-inputs.py` | Could not trace. Do not write a partial receipt as evidence. | exit 2 |
| `trace-inputs.py` exits 0 | The wrapper ran. The wrapped command's own exit is only in the JSON `exit` field. | exit 0 does not mean the command passed |
| Bad argv or missing `--out`/`--root` for any round-17 tool | Usage error. | exit 64 |

### Recipe — re-pin a drifted disposition input (R16-OP1 pattern)

1. Run the live gate and read the error:
   `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
   Note `error.kind` and the path in `error.message`.
2. Find a rev whose blob matches the old pin (the pin is in `expected.json`
   `inputs` or in the manifest `inputs` map):
   `git -C . rev-parse <rev>:<path>` then `git -C . cat-file blob <rev>:<path> | sha256sum`.
   The sha must equal the pin. If no rev matches, stop: the pin cannot be
   re-established; report it.
3. Write a new file at a new path (for example
   `.ufo/evidence/round-17/dispositions.json`). Use schema
   `evidence-dispositions-v2`, `expected_file` and `inputs` copied from v1,
   `supersedes` = the v1 path (it must itself be pinned in `inputs`), and
   `historical_inputs` with the `tools/` path, the rev, and a reason.
   Do not touch the round-14 files.
4. Run the live command at the tip. Expect exit 0 with `status: clean`.
5. Run the before manifest:
   `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json`.
   Expect exit 1 with `producer_before` unresolved.
6. Entry-command monitor: run
   `python3 tools/registry-check.py --json` at the tip; read every `ROW` line.
   To grade an old rev against the new registry:
   `python3 tools/registry-check.py --rev <rev> --registry tools/registry.json --json`.
7. Cold-read: each seat writes a `tameshi-coldread-report-v2` block with
   `read_rev`, per-section `inputs` (from `trace-inputs.py`), and
   `external_inputs`. Then assemble the ledger and measure it at the tip:
   `python3 .ufo/evidence/round-17/measure.py --rev <tip> --ledger-file .ufo/evidence/round-17/coldread/ledger.json`.
   Check `box3_link` and the per-bucket reasons.
8. Selftests are capability only. Each tool's `--selftest` uses synthetic
   fixtures and proves the tool's own branches, not the lane's evidence. Frozen
   replays and live runs are the evidence.

### Round-17 gate/probe registry

| Name | Kind | Command | Exits |
|---|---|---|---|
| effective expectation disposition, v2 (live tree) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json` | 0 clean; 1 failed semantic expectation; 2 could-not-evaluate (`historical_input_forbidden`, `historical_input_unknown`, `historical_input_unavailable`, `expected_input_digest_mismatch`, identity mismatch); 64 usage |
| entry-command monitor | gate | `python3 tools/registry-check.py --root . --json` (or `--rev REV --registry PATH --json`) | 0 all rows held; 1 any row `differs`; 2 could-not-evaluate (registry unreadable or invalid, rev missing, clone failed); 64 usage |
| input-keyed cold-read measure, v2 | gate | `python3 .ufo/evidence/round-17/measure.py --rev REV [--ledger-file PATH \| --ledger-rev REV:PATH] [--inputs-overlay FILE]` | 0 measured; 2 rev or blob missing; 64 usage |
| input trace helper | probe | `python3 .ufo/evidence/round-17/coldread/trace-inputs.py --root DIR [--cwd DIR] --out FILE -- ARGV...` | 0 traced (wrapped command's exit is in the JSON `exit` field); 2 strace unavailable or setup failure; 64 usage |
| cold-read ledger assembler, v2 | probe | `python3 .ufo/evidence/round-17/coldread/assemble.py` (main-mode flags `[UNSPECIFIED]` in the wave contract; `--selftest` is specified) | exit codes `[UNSPECIFIED]` in the wave contract |

Selftest commands (capability only): `--selftest` on `evidence-disposition.py`,
`registry-check.py`, `measure.py`, `trace-inputs.py`, `assemble.py`. The
registry-check and measure selftests exercise synthetic fixtures; a red-before
case (input drift uncredits an otherwise credited bucket) is required in
measure's selftest.

Limit: the round-17 registry rows describe instruments; they are not an
outside-admission sample, do not change rank, SHONEN authority, or the six
recorded cases, and do not register sibling-repo gates. Round-14 and round-16
historical bytes stay as written.
```

## Limits of this draft

- None of the round-17 tools is in the tree at the lane root (`ls tools`
  shows only the seven pre-round-17 instruments). Every command for
  `registry-check.py`, `measure.py` v2, `trace-inputs.py`, `assemble.py`, and
  the v2 disposition path is from the wave contract. Exit codes are as
  specified there; they were not observed.
- `assemble.py` main-mode arguments and its exit codes are not specified in
  the wave contract; the draft marks them `[UNSPECIFIED]` instead of inventing
  them.
- `--root .` on the v2 command follows the contract's abbreviated form
  (`expected --root . --json`). The draft adds `--dispositions` because the
  v1 tool requires it (`tools/evidence-disposition.py:120-121` USAGE at pin `98bea7da`). Builder
  to confirm; [INFERENCE].
- The 4-column registry shape follows the target. Round-12 and round-15
  registries are 8 columns; the extra columns (verdict map, self-test
  command, pinned values, write scope, owner) are either folded into the
  decision table or left for the integrator to restore if the lane wants the
  wider shape.
- No command was run by this seat. No install, no tool version change, no
  pacman activity.

## Verdict

built — draft section and registry table written; commands and exit codes are contract-sourced and await the builders' selftests and live runs.
