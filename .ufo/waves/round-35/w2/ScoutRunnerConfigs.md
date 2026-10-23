# Round-35 w2 — ScoutRunnerConfigs

Seat: `L1tameshi35.ScoutRunnerConfigs` (leaf scout). Dispatch pin `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Attacked `run_regression` in the byte-pinned runner: every branch on `auto`, `KEEP`, `root`, `WORKDIR`, `TIMEOUT_S`, `TAIL_N`, and the printer that branch reaches. Also attacked A4's "real auto root" witness, because that witness is exactly this root construction.

No installs. pacman not run. No mutating git. The pre-existing scratch checkout at `/fast/scratch/hyaku/tameshi-r35-seats/ScoutRunnerConfigs/lane` was already `d16f9b5a` (ancestor of the pin) and was not checked out. Runner bytes were taken by read-only `git show` from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

## Pins

| object | sha256 | where |
|---|---|---|
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | git blob `2d81b929c765d52d6ff38837bb76901cd3358c8e` at `d16f9b5a`, at `7da6e076`, and the worktree file when hashed. 2080 lines. |
| `tools/tally-audit-v3.py` at `7da6e076` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | contract pin. Extracted to scratch `tally-audit-v3.pin.py`. |
| `c1-measure.py` at `7da6e076` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | contract pin. Extracted to scratch `c1-measure.pin.py`. |
| contract.json at `7da6e076` | `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0` | A4/A5 pins_new name the two hashes above. |

The worktree contract and counter have since moved (`tool ec236de2…`, `c1 b9ee1042…`). This report does not use them. Host: bash `5.3.20(1)-release`, CPython 3.14 (`/usr/lib/python3.14/tempfile.py`).

Scratch copy exercised: `/fast/scratch/hyaku/tameshi-r35-seats/ScoutRunnerConfigs/mutate-and-run.pin.sh` (same sha256, `chmod +x`). Its `FLEET_ROOT` is three `dirname`s of `SELF` = `/fast/scratch/hyaku`, so the nine legs die at repo-identity and never start a sweep. That is the safe executed path. A fleet-resident `SELF` (`…/tameshi-shokunin/tools/mutate-and-run.sh`) would set `FLEET_ROOT=/home/vgpnk/Projects/shokunin` and was not invoked.

## What was attacked

1. Control flow of `run_regression` (`mutate-and-run.sh:1345-1471`) plus the argv defaults (`:180-190`, `:2058-2079`) and the leg printer `regression_case` / `regression_case_git` (`:1150-1343`) that it calls.
2. Whether A4's auto-root witness (`tempfile.mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')` in the pinned tool `:365` and the pinned counter `:67`) is the same shape as the runner's `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` (`:1360`).

## Decision table

`auto` is local, set only at `:1357-1365`. `KEEP` is global, `0` unless `--keep` (`:190`, `:2067`). `root` is local. `WORKDIR` / `TIMEOUT_S` / `TAIL_N` are reset at `:184-187` before argv parse, so a caller export does not survive (observed). `BAND_KILLED` / `BAND_FLIPS` are not flags; the header always prints the fixture default `<=1/<=1` while every ledger leg passes `0 0`.

Stdout vs stderr: `usage_exit` (`:238-241`) and `die_setup` (`:244-246`) write stderr and print no `REGRESSION_*` line. Every `REGRESSION*` printer writes stdout. Child sweep stdout is captured to `$cwd/sweep.log` and does not join the regression stdout except the one `grep -m1 '^MUTATE: '` summary.

| id | predicate (line) | config that reaches it | exit | stdout | stderr | proof |
|---|---|---|---|---|---|---|
| E0 | any of `TARGET SPEC SUITE LABEL` non-empty (`:1346`) | `--regression` plus one of those flags, `--keep` irrelevant | 64 | empty | `mutate-and-run: --regression takes no --target/--defects/--suite/--label` then usage | observed, four flags, rc 64, stdout 0 |
| E1 | `--timeout`/`--tail` missing or `''` (`need_val:249`) | before `run_regression` | 64 | empty | `mutate-and-run: --timeout needs a value` (or `--tail`) | observed |
| E2 | `(( TIMEOUT_S > 0 ))` false, value is a number (`:1349`) | `0`, `-1`, `00` (octal 0) | 64 | empty | `mutate-and-run: --timeout must be a positive integer` then usage. No bash diagnostic | observed |
| E3 | same test, bash arithmetic error | `08`, `1.5`, `1e2` | 64 | empty | bash diagnostic on `:1349` first, then the same usage text | observed. `08`: `value too great for base` |
| E4 | same test, `set -u` unbound name | `abc`; also `--timeout --keep` (the flag is consumed as the value, name `keep`) | **1** | empty | `<script>: line 1349: <name>: unbound variable` only. Usage is not printed | observed. Not the documented usage exit 64 |
| E5 | `(( TAIL_N > 0 ))` (`:1350`) | timeout already passed | same split as E2–E4, message `--tail must be a positive integer`, diagnostic names `:1350` | | | observed `0`, `-3`, `abc` (exit 1), `08`, `1.5` |
| E6 | timeout checked before tail | both `0`, either order; later `--timeout 0` wins over an earlier `5` | 64 | empty | timeout message, not the tail message | observed |
| E7 | arithmetic check **passes** | `+1`, `0x10`, ` 1` (leading space) | falls through | (then the normal regression stdout) | empty on the identity path | observed: those three reached the same 2048-byte SETUP transcript as the default, exit 2 |
| E8 | `command -v` python3, sha256sum, mktemp, git, in that order (`:1351-1355`) | first missing wins. `timeout` is **not** in this list | 2 | empty | `MUTATE: SETUP (python3 missing)` / `(sha256sum missing)` / `(mktemp missing)` / `(git missing (--regression materializes each leg from its repo object store))` | observed, filtered PATH, rc 2 |
| E9 | `timeout` absent, the four above present | check E8 passes | 2 | full SETUP transcript (headers + 9 identity lines + tally) | empty | observed `miss-timeout-only`, stdout 2048 |
| R0 | `WORKDIR` empty (`:1359`) | no `--workdir`. `auto=1`. `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` | (continues) | root appears only in the final `REGRESSION_WORKDIR` line on the identity path | | observed `/tmp/tameshi-r4-2-regression.zaOsiD`. Suffix length 6. 40/40 further `mktemp -d` calls were length 6, 0 contained `_`, 38/40 contained an uppercase |
| R1 | `mktemp` fails (`:1360`) | auto path only | 2 | empty | `MUTATE: SETUP (mktemp -d failed)` | observed, fake `mktemp` exit 1. `auto` stays 0 because the assignment dies before `:1361` |
| R2 | `WORKDIR` non-empty (`:1362-1364`) | `--workdir DIR`. `auto=0`. `root` is the argument **verbatim** (relative stays relative). `mkdir -p` | (continues) | final line names that string | | observed absolute and `rel-wd` (printed `rel-wd`, created under the cwd) |
| R3 | `mkdir -p "$root"` fails | `--workdir` is an existing file | 2 | empty | mkdir `File exists`, then `MUTATE: SETUP (cannot create workdir: …)` | observed |
| R4 | `--workdir` set, `mktemp` broken | R1 does not run | 2 | SETUP transcript | empty | observed |
| R5 | `mkdir -p "$root/specs"` fails (`:1367`) | `specs` pre-created as a file | 2 | empty | mkdir `File exists`, then `MUTATE: SETUP (cannot create specs dir: …)` | observed. Root dir left in place (no rm on this path) |
| R6 | `regression_specs` returns non-zero (`:1368`) | specs dir mode `0555`. No `set -e`, so all nine `cat`s fail and the last status is returned | 2 | empty. Headers are **not** printed | nine `Permission denied` lines, then `MUTATE: SETUP (cannot write the embedded case specs)` | observed |
| H | specs written (`:1370-1383`) | every path that gets past R6 | (continues) | exactly four lines, then the legs: `REGRESSION_TOOL: <SELF> sha256=<sha>`, `REGRESSION_DATE: <UTC>`, `REGRESSION_BAND: ledger legs exact (…<=0 …<=0…); fixture-mode default killed-delta<=1 flips<=1`, `REGRESSION_EXPECT: … js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10 js-sources-check=5/10 js-cite-check=5/10` | | observed. EXPECT matches `table_count`/`table_total` of the nine `TABLE_*` literals. DATE is the only non-deterministic header. TOOL sha was `a7d3f2dd…`. Nine spec files written under `$root/specs` |
| L0 | `FLEET_ROOT=$(dirname^3 "$SELF")` (`:1358`), repo dir missing or not its own toplevel (`regression_case:1188-1193`) | scratch copy. Each `regression_case_git` (`:1332-1342`) builds `repo=$FLEET_ROOT/${rel%%/*}` | leg returns 2 | `REGRESSION_CASE <leg>: SETUP (repo_identity_mismatch: <FLEET_ROOT>/<repo> is not its own repository; toplevel=unresolved)` | empty | observed, 9/9, `FLEET_ROOT=/fast/scratch/hyaku`. No `REGRESSION_PIN`, no `REGRESSION_SWEEP`, no per-leg `REGRESSION_WORKDIR` |
| L1 | fleet-resident script, all nine materialization gates | `SELF` under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools` | not executed | next printer would be `REGRESSION_PIN` (`:1230`) then the sweep | | read-only: all 9 `ident`, `rev`, `path`, `pin_eq` true. Modes below. Sweep not run |
| T0 | tally: `nfail>0` (`:1441-1445`), wins over setup | any `(auto,KEEP)`, any root | 1 | `REGRESSION: FAIL (cases=9 passed=<p> failed=<f> setup=<s>)` then `REGRESSION_WORKDIR: <root> (kept)` | empty | observed on the extracted block. One `1`: `passed=8 failed=1 setup=0`. One `1` and one `2`: `passed=7 failed=1 setup=1`. Directory **not** removed even at `auto=1 KEEP=0` |
| T1 | `nsetup>0` (`:1447-1451`) | no status equal to `1` | 2 | `REGRESSION: SETUP (cases=9 passed=<p> cannot-verify=<s>)` then `(kept)` | empty | observed. One `2`: `passed=8 cannot-verify=1`. Status `3` and `255` take the `*` arm and the same printer. `00` is a string, not a number: also `*` → SETUP (not PASS) |
| T2 | `(( npass+nfail+nsetup != nlegs ))` (`:1456-1460`) | the pristine loop cannot reach it: `case $st` is exhaustive and each of the 9 statuses increments exactly one counter. Classified `0..255` in bash: each sums to 1, so nine of them sum to 9 | 2, only if the loop under-counts | `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=<sum>)` then `(kept)` | empty | observed by deleting the `"$st_citecheck"` operand: exit 2, `counted=8`. Not observed on the pristine bytes |
| T3 | PASS and `auto==1 && KEEP==0` (`:1464-1466`) | default `--regression` (no `--workdir`, no `--keep`) | 0 | `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` then `REGRESSION_WORKDIR: <root> (removed on PASS; --keep retains)` | empty if `rm` works | observed on the extracted block (bytes = lines 1432–1470; `awk` extraction identical). Directory removed (`exists` before true, after false) |
| T4 | PASS and not (auto=1 and KEEP=0) (`:1467-1468`) | `--keep` (`auto=1 KEEP=1`), or any `--workdir` (`auto=0`, `KEEP` 0 or 1) | 0 | same PASS line, then `REGRESSION_WORKDIR: <root> (kept)` | empty | observed all three. Directory remains |
| T5 | `rm -rf "$root"` fails after T3's printf | dir mode `0555` with a child. No `set -e` | **0** | still the "removed" line | `rm: cannot remove '…/canary': Permission denied` | observed. Directory still exists. The printer is not predicated on `rm`'s status |
| S | nine leg statuses all in `{2}` (the identity path), then T1 | all four `(auto,KEEP)`, and `--timeout 1 --tail 1` vs `--timeout 9 --tail 3` | 2 | 15 lines: 4 headers + 9 `REGRESSION_CASE … repo_identity_mismatch` + `REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)` + `REGRESSION_WORKDIR: <root> (kept)` | empty | observed. Date-normalized body **above** the final line is identical across all seven runs (`body_eq=True`). `KEEP` does not change a SETUP transcript. Root string appears **once**. Both auto dirs and both explicit dirs still existed afterward (not removed) |

`TIMEOUT_S` and `TAIL_N` do not select a printer inside `run_regression` after E2–E7. They are forwarded only into the child sweep (`regression_case:1248-1249`: `--timeout "$TIMEOUT_S" --tail "$TAIL_N"`). `run_one:456` runs `timeout "$TIMEOUT_S" bash -c "$SUITE"`. `print_tail:309` uses `tail -n "$TAIL_N"` and that output stays in `sweep.log`. On every executed pre-sweep path, changing them did not change stdout.

Env clobber, one command: `WORKDIR=/tmp/scout-should-not-appear TIMEOUT_S=0 TAIL_N=0 KEEP=1 <pin> --regression` → exit 2, sentinel absent, root `/tmp/tameshi-r4-2-regression.mgTcIg`. A leaked `TIMEOUT_S=0` would have died at E2.

### Leg printers not reached by the executed runs (source, `regression_case`)

Reached only when L0 does not fire. Read-only fleet check says a resident script would get past every gate below (so the next line is `REGRESSION_PIN`, then a real sweep). Sweep not run. This is the gap.

| order | predicate | return | stdout line |
|---|---|---|---|
| 1 | `mkdir -p "$cwd"` fails (`:1171`) | 2 | `REGRESSION_CASE <n>: SETUP (cannot create case workdir: …)` |
| 2 | `git` missing (`:1176`) | 2 | `SETUP (git missing; cannot materialize the pinned revision)` |
| 3 | repo identity (`:1190`) | 2 | the L0 line. **Observed.** |
| 4 | `rev^{commit}` missing (`:1195`) | 2 | `SETUP (revision not found: <repo>@<rev>)` |
| 5 | `cat-file -e rev:path` fails (`:1199`) | 2 | `SETUP (path not in revision: …)` |
| 6 | `git show` fails (`:1204`) | 2 | `SETUP (git show failed: …)` |
| 7 | `ls-tree` mode read fails / empty (`:1213`, `:1218`) | 2 | `SETUP (cannot read the blob mode: …)` / `(empty blob mode: …)` |
| 8 | mode `100755` and `chmod +x` fails (`:1223`) | 2 | `SETUP (cannot restore the exec bit on …)`. `100644` is left as written |
| 9 | mode known | (continues) | `REGRESSION_PIN <n>: source=git repo=<repo> rev=<rev> path=<path> mode=<mode> sha256=<recorded pin>` |
| 10 | sha256(materialized) != pin (`:1241`) | 2 | `REGRESSION_CASE <n>: SETUP (pin mismatch: recorded=… materialized=… source=…)` |
| 11 | child `bash "$SELF" --target … --workdir "$cwd" --label <n> --timeout --tail` (`:1248`) | child 0/1/2/other | `REGRESSION_SWEEP <n>: <first ^MUTATE: line, or "no MUTATE line (sweep exit=…)">` |
| 12 | child exit 2 (`:1254`) | 2 | `REGRESSION_CASE <n>: SETUP (sweep refused; log: …)` |
| 13 | child exit not in {0,1} (`:1258`) | 1 | `REGRESSION_CASE <n>: FAIL (sweep exit=…, expected 0 or 1; …)` |
| 14 | `results.tsv` missing (`:1264`) | 1 | `REGRESSION_CASE <n>: FAIL (no results table; …)` |
| 15 | table compare (`:1319-1329`) | 0 or 1 | zero or more `REGRESSION_DEFECT <n> <id>: measured=… recorded=…`, then `REGRESSION_TABLE <n>: match=<m>/<exp> recorded-killed=… measured-killed=… survived=… inconclusive=… flips=…`, then `REGRESSION_WORKDIR <n>: <cwd>`, then either `REGRESSION_CASE <n>: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=<exp>)` or `FAIL (out of band: <reasons>; log: …)`. Ledger call passes `ktol=0 ftol=0` (`:1341`) |

Child `run_sweep` printers (inside `sweep.log` only): `MUTATE_TOOL/DATE/TARGET/SPEC`, `CONTROL: GREEN|RED`, `DEFECT <id>: KILLED|SURVIVED|INCONCLUSIVE`, `MUTATE_RESTORE: OK|DRIFT`, `MUTATE: DONE` (exit 0) or `MUTATE: DEGRADED` (exit 1, any inconclusive). Suite exit `0` survived, `124/126/127` inconclusive, anything else killed (`:545-550`). A red control calls `die_setup` → child exit 2 → row 12.

Fleet-resident gates, read-only `git -C <repo> rev-parse --show-toplevel`, `rev-parse --verify <rev>^{commit}`, `cat-file -e <rev>:<path>`, `ls-tree`, `git show | sha256sum`, compared to the `PIN_*` literals. All nine `pin_eq=True`:

| leg | mode |
|---|---|
| js-kimi-census | 100644 |
| bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check, js-round-gate, js-sources-check, js-cite-check | 100755 |

So eight of nine ledger legs take the `chmod +x` arm. Not executed.

### The four `(auto,KEEP)` triples, pristine block

Second stdout line and the rm side effect. First line depends only on the nine statuses, not on the triple. Block bytes = `mutate-and-run.sh:1432-1470` (`awk` equality observed).

| auto | KEEP | how the CLI gets there | PASS second line | rm on PASS | non-PASS second line | rm on FAIL/SETUP |
|---|---|---|---|---|---|---|
| 1 | 0 | no `--workdir`, no `--keep` (the default) | `(removed on PASS; --keep retains)` | yes | `(kept)` | no |
| 1 | 1 | `--keep` | `(kept)` | no | `(kept)` | no |
| 0 | 0 | `--workdir DIR` | `(kept)` | no | `(kept)` | no |
| 0 | 1 | `--workdir DIR --keep` | `(kept)` | no | `(kept)` | no |

`root` on auto is the mktemp path; on explicit it is the `--workdir` string unchanged. v3/counter `CONFIGS` (both files, lines 349–350 and 52–53) are `(None,'1','0')`, `(None,'1','1')`, `('tally-audit','0','1')`, `('tally-audit-explicit','0','0')`. `None` is replaced by `mkdtemp`, not by `mktemp`. The two explicit roots are relative and are not created.

## Findings

### CRITICAL — the witnessed "real auto root" is not the runner's mktemp shape

A4 closed the wave-1 glob `/tmp/tameshi-r4-2-regression.*`. That glob matches **both** generators (observed: `mktemp` path `…j9zV0j` and `mkdtemp` path `…8wzbak3y` both `GLOB_MATCH`). It does not close a gate on the template the runner actually uses.

- Runner, `:1360`: `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`. Suffix is exactly six characters. 8 samples plus 40/40 more: length `{6: 40}`, underscore 0, uppercase 38/40. Executed default root `…zaOsiD` (length 6).
- Pinned tool `:365` and pinned counter `:67`: `tempfile.mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')`. CPython 3.14 `tempfile._RandomNameSequence`: `characters = "abcdefghijklmnopqrstuvwxyz0123456789_"`, ``k=8``. 40/40 length 8, uppercase 0, underscore 12/40. Counter's own auto root during the proof: `…2dgru2pk` (length 8, contains `_`).
- `[[ $root == /tmp/tameshi-r4-2-regression.?????? ]]` is a full-string match of exactly six characters. Observed `SIX_MATCH` on the mktemp path, `SIX_NO` on the mkdtemp path (including one that contains `_`).

Mutant `mutant-len6.sh` sha256 `634b144cdc41b27161c0a65be6e2d5dc9db06b37f6e90434445cb574c3ec6a27`, one insertion after the tally `esac`/`done` (the site occurs once):

```bash
if [[ $auto -eq 1 && $root == /tmp/tameshi-r4-2-regression.?????? ]]; then nfail=0; npass=$((npass + 1)); fi
```

Pinned tool, executed:

```
python3 …/tally-audit-v3.pin.py --runner …/mutant-len6.sh
```

exit 0. Stdout:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Pinned counter (`515b0b1b…`, imported, `behavior` + `diverge` over its `CONFIGS`): `PINNED_COUNTER_DIVERGE_LEN6 []`. Same blocks driven with the counter's `run_block` under a real `mktemp -d` root `/tmp/tameshi-r4-2-regression.Ox1fru` (`auto=1 KEEP=0`):

| vector | pristine | mutant |
|---|---|---|
| nine zeros | exit 0 PASS, workdir line `(removed …)` | exit 2 `SETUP (case-tally mismatch: cases=9 counted=10)`, `(kept)` |
| one `1` | exit 1 `FAIL (… passed=8 failed=1 setup=0)`, `(kept)` | exit 0 PASS `(removed …)` — a failing leg is masked into a PASS **and** the workdir is deleted |

Under the counter's own mkdtemp auto root `…2dgru2pk`, the same two vectors were identical (`len6-auditauto same True`). The default `--regression` config is the one that diverges; the witness does not generate a string that config can produce.

### BOUND — explicit `--workdir` is not an absolute path in the four triples

Comment in both pinned files ("relative and absolute") is false: the two `auto=0` roots are the relative strings `tally-audit` and `tally-audit-explicit`, and nothing `mkdir`s them. The runner's `auto=0` root is the caller's string verbatim after `mkdir -p` (`R2`, observed, including a relative `rel-wd` and an absolute scratch dir).

Mutant `mutant-abs.sh` sha256 `14d03d22c1cd0e508b3424908cd9c5e2f5c7b0ddf0b0e1ead36f64b0879ca027`:

```bash
if [[ $auto -eq 0 && $root == /* ]]; then nfail=0; npass=$((npass + 1)); fi
```

Same pinned tool: exit 0, `TALLY_AUDIT: PASS`, `runtime PASS vectors=30316 mismatched=0`. Pinned counter `diverge` over `CONFIGS`: `[]`. Under root `/tmp/scout-abs-wd-pin`, `auto=0 KEEP=0` (a real `--workdir /tmp/scout-abs-wd-pin`): nine zeros go PASS→`SETUP counted=10`; one `1` goes FAIL→PASS. Under `tally-audit` the blocks matched.

This does not move the default (`auto=1`) run. It is the explicit-workdir axis the comment claims to represent and the tuples do not.

### BOUND — "removed" is printed even when `rm` fails

T3 prints the removed line, then `rm -rf "$root"`, then `exit 0`. No `set -e`. Observed: root mode `0555` with a canary, exit 0, stdout says `(removed on PASS; --keep retains)`, stderr `rm: cannot remove '…/canary': Permission denied`, directory still present. Early exits (E8, R1, R3, R5, R6, T0, T1) never rm, so a failed `mktemp`/`mkdir`/`specs` path also leaves the directory. Only T3 removes it, and only when `rm` happens to succeed.

### BOUND — the positive-integer check is bash arithmetic, and one failure mode is exit 1

Documented usage exit is 64 (`:80-81`, `:241`). E4 is exit 1 with no usage text (`set -u` on an unbound name inside `(( ))`). E7 accepts `+1`, `0x10`, and ` 1`. GNU `timeout 0x10 true` then exits 125 (`timeout: invalid time interval '0x10'`). `run_regression` would forward that string into every child (`:1248`, `:456`); a 125 is not 124/126/127, so `run_sweep` counts it KILLED, the control goes red, the leg returns SETUP (row 12). Not reached: the identity path never calls `timeout`. Default `300` is unaffected.

### HYGIENE — mismatch arm is dead on these bytes

T2's printer exists and was observed only after deleting one loop operand. The pristine `case` (`:1434-1438`) sends every status, including `2..255`, into exactly one counter. Nine `regression_case` returns therefore always sum to 9. `regression_case` itself only `return`s 0, 1, or 2.

### HYGIENE — pinned counter's tool constant is the pre-A4 hash

`c1-measure.pin.py:46` `TOOL_SHA256 = da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f`. Confirmed by importing that file (`TOOL_SHA_CONST`). The tool blob at the same commit, and contract.json `frozen_artifacts.tool_sha256` / A4 `pins_new`, are `ef98fc53…`. Deciding mode (`:374`) sets `tool_sha_ok` only when `tool_sha == TOOL_SHA256` (`a.tool is None`). Those two hashes differ, so `tool_sha_ok` cannot be 1. `c1-measure.py` main was not executed (it wants a lane and a sealed set); the consequence is the source predicate applied to the two observed hashes. Fail-closed, not a false accept.

## What I could not break

- Wave-1 prefix glob. Both generators match `/tmp/tameshi-r4-2-regression.*` (command and both paths above). A4 does close that specimen.
- Pristine tally printers. Extracted block, all four triples, PASS / one-fail / one-setup / fail+setup: first line, second line, exit, and rm-vs-keep match the table above. `awk` extraction equals lines 1432–1470.
- Pre-sweep stdout is invariant in `(auto,KEEP)`, `TIMEOUT_S`, and `TAIL_N` except the final root string and the date line (`body_eq=True` on seven runs).
- Environment cannot select a workdir or a timeout. The sentinel export was ignored.
- Conflicting `--regression` flags, missing tools, a failing `mktemp`, a non-directory workdir, and an unwritable specs dir all fail closed (64 or 2) with no `REGRESSION:` line.
- Placing the script outside the fleet fail-closes every leg at repo-identity (exit 2, workdir kept) and does not read the sibling repos. The resident repos' pins do match, so that fail-closed is a property of `SELF`'s path, not of the pins.
- Status `0..255` cannot skip the tally counters, so the mismatch printer is not a pristine behavior.

## Not executed (gap)

A green or red nine-leg `--regression` from the fleet-resident path. That is the only way to observe rows 9–15 (`REGRESSION_PIN`, `REGRESSION_SWEEP`, `REGRESSION_TABLE`, per-leg `REGRESSION_WORKDIR`, `REGRESSION_CASE PASS|FAIL`) as live stdout. The read-only gate check says all nine legs would get there; the printers are cited from `:1171-1329` and were not run. PASS/rm behavior of the tally tail was run as the extracted bytes, not as the tail of a live nine-leg process.

Receipts: `/fast/scratch/hyaku/tameshi-r35-seats/ScoutRunnerConfigs/probe-out/` (`cfg-*.out`, `drive-*.out`, `v3-mutant-len6.out`, `v3-mutant-abs.out`). Default identity transcript sha256 `555a507ee636e27fd59378d90c9bb1cdf9c3f95505b2b67880806db496d5a9bd` (includes `REGRESSION_DATE: 2026-10-23T21:37:20Z`).
