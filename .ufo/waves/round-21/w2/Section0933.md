done — Section 933 audit complete; verdict: blocking.

# Section 933 — “Using the ledger”

**Scope:** `SKILL.md:933-964` at `790abd2129f153c13b471e381d454186edbde65e` (the revision is also the `refs/heads/master` tip). Static source/evidence review only; no mutation recipe or regression replay was run.

## Findings

1. **Blocking: six cited source ranges are stale or incomplete.** I materialized the pinned `tools/mutate-and-run.sh` blob and compared each citation to its actual contents:
   - Section `:939` cites `tools/mutate-and-run.sh:72-109` and `:891-975` for the command, scratch lifecycle, and exit map. At this revision the former is prologue/case inventory material, while the latter is embedded defect specs, not the regression implementation. Current anchors are `:126-136`, `:189-210`, `:1273-1294`, and `:1364-1384`.
   - Section `:943` cites `:733-791` for Git-object materialization and pin validation; those lines are embedded tsukuroi/mado specs. The actual `git show`, mode restoration, and SHA-256 check are at `:1104-1175` (the printed `REGRESSION_PIN` is `:1159-1160`).
   - Section `:961` cites `:511-522` for pins/revisions/tables; that range is sweep code. Current declarations are `:597-620`.
   - Section `:962` cites `:550-728` for specs. It includes only part of the original four specs (and the preceding pin/table declarations); it does not cover all four. The first-four spec bodies are at `:648-829`.
   - Section `:962` cites `:927-944` for the leg registry; those lines are claims-check defects. The current registry is `:82-100`, with its actual eight dispatches at `:1314-1353` and `nlegs=8` at `:1355-1356`.

   `REGRESSION_TOOL` and receipt emission are at `tools/mutate-and-run.sh:1299-1311`; per-leg table/pass evidence is at `:1240-1255` and the closing status/cleanup at `:1364-1384`. These support the receipt procedure, but the section’s citations do not point there. The six stale/incomplete ranges are counted as six blocking citation gaps.

2. **Wrong expectation — the contribution contract overstates suite hermeticity and executed counts.** The first two current regression legs are not both hermetic in the stated sense. The pinned `../kagi-shokunin/corpus/surface-census.sh:817-847` checks whether the real `JANITOR` handler is on `PATH`; absent it records two `skip-case`s, and present it runs the real handler. The pinned historical measurement explicitly records the suite as “16 cases (14 hermetic + 2 substrate-gated `skip-case`)” (`corpus/knowledge/fleet-kill-rate-ledger.md:46`). Its `SELFTEST: PASS (N cases)` summary counts the skips as cases, not as executed tests. Replace the universal “hermetic suite”/“executed count” contract with the actual substrate-gated qualification.

3. **Wrong expectation — scratch retention has a pre-allocation exception.** `run_regression` checks `python3`, `sha256sum`, `mktemp`, and `git` at `tools/mutate-and-run.sh:1280-1284`; only afterward does it allocate the default root at `:1287-1293`. `die_setup` exits 2 at `:236-238`. Thus a missing prerequisite is a SETUP refusal with no root to retain. The retention statement is accurate for failures after allocation, but needs that boundary.

4. **Wrong expectation — one leg’s SETUP does not stop all suites.** Repo/revision/blob/pin checks return SETUP before the *affected leg’s* suite (`tools/mutate-and-run.sh:1104-1175`). `run_regression` then continues to invoke later legs (`:1314-1353`) and aggregates their statuses (`:1355-1374`). Narrow “before any suite runs” to “before that leg’s suite runs”; the current wording implies a global short-circuit that does not exist.

## Accurate and historical claims

- The command is current, not obsolete: the usage at `tools/mutate-and-run.sh:190` exposes `--regression [--workdir DIR] [--keep]`; it assumes the command is run from the repository root. The valid-run outcome map 0/1/2 is correct. Invalid CLI usage can separately return 64.
- `git show <rev>:<path>` materialization, the recorded target hash check, and the per-leg pin receipt are implemented as described. I verified SHA-256 for all eight materialized target blobs against `PIN_*` at `:597-611`; both sibling ancestry claims also hold at review time: tsukuroi `165307fe` is an ancestor of HEAD `c05af5c` (rc 0), and mado `eead56b` is an ancestor of HEAD `741122d` (rc 0). This is a static check, not a replay.
- The numbers 4 at r7-1, 7 at round 16, and 8 at round 18 are dated historical counts in `tools/mutate-and-run.sh:82-100`, not a claim that the current ledger has only four legs. The current runner has eight legs (`:1314-1356`). The first four recorded rates remain 8/10, 8/10, 6/10, and 4/10 (`:613-616`).
- The `(U)` statement that no fleet-contributed leg has been exercised is supported at this revision by `corpus/knowledge/operator-runbook.md:427-431` and `corpus/knowledge/closeout-r11.md:335-339`; the current runner embeds its eight specs and hard-codes their calls (`tools/mutate-and-run.sh:648-1072`, `:1314-1353`). Do not treat `corpus/knowledge/fleet-kill-rate-ledger.md:85-88` as current embedding status: that T7-2 snapshot says only cases 1 and 2 are embedded and is stale at this revision.

## Verification and gaps

- Commands and exits: `git rev-parse HEAD` and `git rev-parse refs/heads/master` each returned `790abd2129f153c13b471e381d454186edbde65e` (rc 0); `git merge-base --is-ancestor 790abd2129f153c13b471e381d454186edbde65e refs/heads/master` returned 0. `git show 790abd2129f153c13b471e381d454186edbde65e:SKILL.md > /tmp/tameshi-r21-Section0933/SKILL.md` and the same command for `tools/mutate-and-run.sh` both succeeded (rc 0); their `git hash-object --stdin` IDs were respectively `71cbd6cff4bbea7d52e89b3f74da76d461584a4d` and `fd1a63a3493b5a2fb2723f2fb1baae9ee7480fba`.
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin merge-base --is-ancestor 165307fe4746a8807b02ec4a7d7ecac0368454a6 HEAD` and the corresponding mado command for `eead56b20ad2b28299ae4fa623d52a99b44c743c` each returned 0; observed HEADs were `c05af5c07a639252795317abcb98bcfe7e19dba4` and `741122d177ae8ff68a73768777f20484d5bdcbe4`. The `sha256sum` command on the eight target blobs materialized from their pinned revisions exited 0, and all eight hashes matched their `PIN_*` declarations.
- `git show 790abd2129f153c13b471e381d454186edbde65e:tools/operator-runbook.md` returned 128 because that path does not exist; the corrected path `corpus/knowledge/operator-runbook.md` materialized successfully (rc 0). No build, test, mutation, or replay was run.
- LSP is unavailable: `read xd://lsp` returned “No such tool” and the mounted-device list does not include `lsp`; therefore no LSP status, references, definition, or diagnostics could be queried. Text searches were locators only; findings are based on direct reads of the pinned source and evidence.
- No runtime change, rerouting, or saturation claim is made by this section. The regression path uses one canonical `$SELF` script and its nested sweeps use that same script; rerouting/saturation checks are not applicable to the section.
