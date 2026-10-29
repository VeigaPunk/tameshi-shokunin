# T57W1ExecDeciding — round-57 deciding-run.sh (staged)

Staged: `.ufo/waves/round-57/w1/T57W1ExecDeciding/stage/.ufo/evidence/round-57/deciding-run.sh` (sha256 `4103f33ef9eaa3a87d4204a0ddb4e6692c3797bfed062bd365dd112f85fc97a9`, executable, `bash -n` ok).
Usage: `deciding-run.sh LANE BASE REV OUTDIR` (all absolute). Derived from `.ufo/evidence/round-56/deciding-run.sh` (167 lines). No lane file edited; no tool installed.

## Design changes from round 56
1. **No FREEZE argument**: freeze = last commit touching `freeze.json` at REV (found in the clone), must descend from BASE.
2. **Fresh clone**: `git clone --shared LANE $SCR/clone`; REV must equal that clone's HEAD. All counters / no-harm / precheck / gate run with `--lane <clone>` (committed bytes only). The lane's own working tree must also be clean (only untracked files under OUTDIR allowed), before and after.
3. **Receipt gate is NOT a precondition of the controls** (the R56 circularity). Controls need: blob, non-empty, committed after the freeze, `CONTROLS_A|B: N/N as pre-registered`, no `CTL_MISMATCH`, `.exit` = 0, `.stdout.sha256` equals the stdout digest. The gate runs LAST (`receipt-gate-verdicts.*`) and certifies only `c1.stdout` / `c2.stdout` this run produced (`verdict:C1_R57_PASS=`, `verdict:C2_R57_PASS=`).
4. **Freeze manifest** (`tameshi-freeze-v1`): schema, round 57, base == BASE arg == contract.base; manifest keys == contract `frozen_paths` mapped (relative to `.ufo/evidence/round-57/`, `tools/…` own key, `freeze.json` skipped); every digest re-derived at the freeze commit AND at REV (post-freeze edit of a frozen file is a refusal); amendments shape/count == freeze-commit count and mirrored in contract (a missing `amendments` key reads as `[]`).
5. Script bytes must equal the committed `.ufo/evidence/round-57/deciding-run.sh` at REV.
6. **Cold-read precheck first**: `.ufo/evidence/round-48/quality/coldread-precheck.sh LANE BASE REV` (from REV bytes) before any counter; RED, non-zero exit or a last line not `COLDREAD_PRECHECK … ok` refuses.
7. Order after gate 0: C1 counter, C2 counter (each `.start/.stdout/.exit/.end`, `--work` inside scratch, `--explain`), no-harm.sh (`LANE BASE REV`, per the staged T57W1ExecNoHarm signature), census, final gate. Pass rule: counter exit 0, `C?_R57_PASS=true` present and no `…=false` line; no-harm: exit 0, no `RED`, every `^NOHARM` line `ok`, and ≥ `NOHARM_MIN=18` (the staged no-harm.sh prints 18 monitors; edit the constant if that file changes before freeze). Census uses `$DECIDING_FLEET` (default the real fleet root; echoed into `census.stdout`).
8. Everything printed is also in `OUTDIR/deciding-run.stdout`; ends with `DECIDING_RUN_EXIT=<n>` (also `deciding-run.exit`).

Gate-0 refusals exit 3, print `DECIDING_REFUSED <reason>`, write nothing to OUTDIR (retry possible). Once counter c1 starts, a second invocation is refused (`second-invocation c1`). Usage/relative path exit 2; a run that completes with a failed arm exits 1.

## Refusal strings (all observed, see `T57W1ExecDeciding-receipts/proof-harness.stdout`, per-case output in `…-receipts/cases/`)
| case | exit | first line |
|---|---|---|
| happy path (stub counters, real gate, stub fleet) | 0 | `DECIDING_RUN_EXIT=0` (final `GATE: receipts=2 ok=2 refused=0 codes=none verdict=PASS`) |
| second invocation | 3 | `DECIDING_REFUSED second-invocation c1` |
| REV = ancestor / lane HEAD moved | 3 | `DECIDING_REFUSED rev-is-not-head-of-fresh-clone rev=<sha> head=<sha>` |
| REV unresolvable | 3 | `DECIDING_REFUSED rev-unresolvable` |
| BASE == REV | 3 | `DECIDING_REFUSED base-not-proper-ancestor-of-rev` |
| tampered digest in freeze.json | 3 | `DECIDING_REFUSED freeze-integrity` + `FREEZE_MISMATCH c1/measure.py e59e9ff9eb27 != 000000000000 at freeze` + `FREEZE_MISMATCH amendments=0 inconsistent with 2 manifest commits…` |
| frozen counter edited after freeze | 3 | `DECIDING_REFUSED freeze-integrity` + `FREEZE_MISMATCH c1/measure.py 8efa8a4aaa81 != e59e9ff9eb27 at rev` |
| script differs from committed bytes | 3 | `DECIDING_REFUSED script-not-committed-bytes .ufo/evidence/round-57/deciding-run.sh` |
| missing counter / no-harm | 3 | `DECIDING_REFUSED counter-missing .ufo/evidence/round-57/c2/measure.py` (and `…/no-harm.sh`) |
| CTL_MISMATCH in controls-a | 3 | `DECIDING_REFUSED controls-a-mismatch-lines` |
| controls-b `1/2` | 3 | `DECIDING_REFUSED controls-b-verdict-missing` |
| controls receipt absent | 3 | `DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-57/control/controls-b.stdout` |
| cold-read precheck RED | 3 | `DECIDING_REFUSED coldread-precheck-red exit=1` (OUTDIR left empty) |
| dirty lane tree | 3 | `DECIDING_REFUSED dirty-tree` |
| OUTDIR non-empty / missing / outside lane | 3 | `outdir-not-empty` / `outdir-missing` / `outdir-not-in-lane <path>` |
| relative LANE | 2 | `LANE must be absolute` |
| counter prints `PASS=false` | 1 | `COUNTER_NOT_PASS c2`, `COUNTER_PASS_FALSE_LINE c2`, `DECIDING_RUN_EXIT=1` |
| counter exits 4 | 1 | `COUNTER_EXIT_NONZERO c2` |
| no-harm RED line | 1 | `NOHARM_RED`, `NOHARM_OK_COUNT ok=18 total=19 min=18` |
| no-harm only 9 monitors | 1 | `NOHARM_OK_COUNT ok=9 total=9 min=18` |
| verdict names unresolvable rev (final gate LAST) | 1 | `GATE: receipts=2 ok=1 refused=1 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED`, `DECIDING_RUN_EXIT=1` |

25 cases in total; harness `…-receipts/proof-harness.sh SCRIPT` builds synthetic lanes in scratch (real `tools/receipt-revision-gate.py` copied in; stub counters, stub fleet census, stub precheck) and drives the script.

## Not proven / L1 must note
- Only run on synthetic stubs; never run against the real lane (counters/no-harm for round 57 do not exist yet). Real precheck/no-harm/census wiring is by signature only: no-harm `LANE BASE REV` was read from the staged file, precheck `LANE FLOOR CAND` from the round-48 script.
- The real round-57 `contract.json` currently has `frozen_paths: []` and no `amendments`; the L1's freeze commit must list the frozen instruments (including `.ufo/evidence/round-57/deciding-run.sh`, `no-harm.sh`, counters, `tools/receipt-revision-gate.py`) there and write a matching `freeze.json` (else the manifest is trivially empty — the script checks keys == contract surface, not that the surface is non-empty).
- The final gate requires each verdict receipt to contain exactly one distinct `rev=` token equal to REV (a counter `--explain` that prints other `rev=` tokens makes `RECEIPT_REV_AMBIGUOUS`); counters' `--explain` output must respect that.
- `NOHARM_MIN=18` is a constant in the frozen script.
- Controls receipts needed in `control/`: `controls-{a,b}.{stdout,exit,stdout.sha256}` (sha256 file first token = sha256 of the stdout); `controls-*.exit` must read 0.
- `DECIDING_FLEET` env override exists for stub proofs.
