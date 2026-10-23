# ResiduePerIndexRecord — round 34 wave 1: the SETUP embedded-CR fake-record class against frozen tally-audit-v2

Seat: `ResiduePerIndexRecord` (mutation tester, v2 wave, measurement-only probe).
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ResiduePerIndexRecord`. The lane clone was never
edited; all runs use byte copies in scratch.

## Verdict

**The class reproduces at the round-34 pin. A kill copy that makes the tool's driver emit one extra
record per vector is answered `TALLY_AUDIT: SETUP` (exit 2), which the frozen counter scores a
miss, not a kill.** The mutant **survives** the frozen audit pipeline (`score_tool` → `0/1`)
although it is a valid must-kill copy under the counter's own amendment-6 witness rule
(`ho_witness_ok` → `(True, 'vector')`) and the tool does notice the anomaly (it abandons the audit
rather than comparing anything).

Scope of the finding: **the landed measurement is not falsified.** The sealed held-out set at
`c17e593b` contains no record-boundary injector (14/14 JSON files scan clean for raw `\r` and for
every escaped form; §7), so the deciding run's `ho_kill=8/8` stands. The finding is a **coverage
gap** for future sealed sets: this shape cannot score as a kill under the frozen predicate, and a
future set that includes it would drive `ho_k < ho_kt` — a false negative against a tool that, at
worst, abstains. **No tool edit is proposed as landed work** (the pin is frozen; this rides to
round 35 as a Hold, per the tasking).

| copy | expected under the frozen predicate | actual (counter path) | verdict |
|---|---|---|---|
| `pristine` (pinned runner) | `ACCEPT`, rc 0 | `ACCEPT`, rc 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`; accept score `1/1` | baseline live |
| `m19-cr-fake-record` (**the mutant**) | `KILL`, rc 1 + `TALLY_AUDIT: FAIL` | `OTHER`, **rc 2**, `TALLY_AUDIT: SETUP (tally driver failed (exit 0, 15122/7561 results): )`; kill score **`0/1` (miss)** | **SURVIVED** |
| `m20-cr-bare-progress` (boundary control) | `KILL`, rc 1 + `FAIL` | `KILL`, rc 1, `TALLY_AUDIT: FAIL (… runtime=fail …)`; kill score `1/1` | killed |

## 1. Setup and pins (verified before and after every run)

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ResiduePerIndexRecord
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/ResiduePerIndexRecord/lane        # exit 0 (clone.exit)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                # exit 0 (checkout.exit)
git -C .../lane rev-parse HEAD                                            # 0b99d48e…7f68b7
git -C .../lane show 0b99d48…:tools/tally-audit-v2.py > tool.py           # exit 0 (show_tool.exit)
git -C .../lane show 0b99d48…:tools/mutate-and-run.sh  > pristine.sh      # exit 0 (show_sh.exit)
sha256sum tool.py pristine.sh                                             # exit 0 (pins.txt)
```

Observed, equal to the tasking pins:

```
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Counter (read-only import): `.ufo/evidence/round-33/c1/c1-measure.py` sha256
`f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` = pinned `f6b8868c…a07f28c`.
Lane files on disk at the detached tip re-hashed after all runs:
`lane/tools/tally-audit-v2.py 7b11ba25…8d10`, `lane/tools/mutate-and-run.sh a7d3f2dd…2eb9`.
Sandbox tools present, nothing installed this seat: `bubblewrap 0.13.1`, `Python 3.14.8`, `bash`.

## 2. Mutant construction (one insertion, byte-proven)

`gen.py` (scratch) replaces the tally-start line with itself plus one line, asserting the old string
occurs exactly once and the edit is not a no-op:

- old: `  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n` (occurs **1** time at `pristine.sh:1432`;
  the same text inside the two `awk` patterns at `pristine.sh:1994-1995` is not newline-terminated)
- new line, verbatim in the copy (`mutants/m19-cr-fake-record.sh:1433`):
  `  printf 'junk\rR\t0\tfake\n'` — the copy contains **no raw CR byte**; the CR is produced by
  `printf` at runner time, so a byte-grep of the copy cannot see it.
- control mutant: `  printf 'progress\r'` (`mutants/m20-cr-bare-progress.sh:1433`).

Proof of shape: `gen.py` rebuilds the mutant as `pristine[:off] + insertion + pristine[off:]` and
compares bytes — `rebuilt_identical=True`, `delta=30` bytes (22 for the control). `diff -u` shows
exactly one added line, nothing else.

```
python3 gen.py        # exit 0 (gen.exit)
m19-cr-fake-record sha256 6c4361bb24f7731e811bc811a26437904e540d3e4179851b5381da9139b8dd92 bytes=106568
m20-cr-bare-progress sha256 9cb22db4492aa862fc0bc2f587a99e474e247709068441978e82f62c339155d9 bytes=106560
```

## 3. Is it a legitimate must-kill copy? (counter's own gate, imported)

`probe.py` imports the frozen counter as a module and calls its functions on the scratch copies
(no counter `main`, no `--lane/--rev` run — the kill rule stays consumed):

| call | result |
|---|---|
| `validate_ho(ho)` with `set=kill`, one edit, `witness.vector=[0]*9` | `ok` |
| `apply_edits(pristine, edits) == mutant bytes` | `true` |
| `block_run(tally_block_of(pristine), [0]*9)` | `(0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')` |
| `block_run(tally_block_of(mutant), [0]*9)` | `(0, 'junk')` |
| `ho_witness_ok(ho, pristine, mutant, work)` | `(True, 'vector')` |

So on the witness vector the copy's exit code is unchanged but its first stdout line differs — the
amendment-6 kill+vector rule (`c1-measure.py:214-219`) accepts it as a must-kill. An **accept** copy
cannot carry this injection: accept+vector requires `a == b` (`c1-measure.py:213`) and accept+head
requires an identical tally block (`c1-measure.py:192-193`). The class is kill-only.

## 4. Detector and exact outputs

Detector = the deciding run's own scoring path, `run_tool_sandboxed` + `score_tool`
(`c1-measure.py:234-283`), run on pristine, mutant and restored bytes.

### 4a. Raw tool (reproduces without the counter; `runs/*.rc` capture `$?`)

```
timeout 300 python3 tool.py --runner pristine.sh                    > runs/pristine.out 2> runs/pristine.err; echo $?  # 0
timeout 300 python3 tool.py --runner mutants/m19-cr-fake-record.sh  > runs/m19.out      2> runs/m19.err;      echo $?  # 2
timeout 300 python3 tool.py --runner mutants/m20-cr-bare-progress.sh> runs/m20.out      2> runs/m20.err;      echo $?  # 1
```

`runs/pristine.out` (stderr 0 bytes):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

`runs/m19.out` (stderr 0 bytes) — **one line, no CHECK lines at all** (the abort fires inside
`check_runtime` before any verdict line is printed):

```
TALLY_AUDIT: SETUP (tally driver failed (exit 0, 15122/7561 results): )
```

`runs/m20.out` last two lines (the control: same CR byte, no record boundary):

```
CHECK runtime FAIL vectors=15158 mismatched=15158; first: cfg(0,1) statuses 0 0 0 0 0 0 0 0 0: got (0, 'progress'), want (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)')
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
```

### 4b. Counter scoring path

```
python3 probe.py     # exit 0 (probe.exit); probe.out / probe.err (stderr empty)
pristine -> ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
m19      -> OTHER  rc=2 last='TALLY_AUDIT: SETUP (tally driver failed (exit 0, 15122/7561 results): )'
m20      -> KILL   rc=1 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'
```

`score_tool` on one-copy lists (a 4-tuple of kill_hit/kill_total/accept_hit/accept_total):

```
score_accept_pristine            = [0, 0, 1, 1]   # baseline: pristine is accepted
score_kill_m19                   = [0, 1, 0, 0]   # the mutant: 0 kills out of 1 must-kill -> MISS
score_kill_m20_discriminator     = [1, 1, 0, 0]   # same CR, no fake record -> killed
```

The detector is live in both directions (pristine accept `1/1`, sibling class kill `1/1`), so the
`0/1` on the mutant is a real survival, not a dead boundary.

## 5. Mechanism (line-pointed, pinned tool)

1. The audit driver emits one record per vector with `printf "R\t%s\t%s\n"` (`tool.py:283`), where
   the payload is the block's output up to the first **LF** (`${out%%$'\n'*}`).
2. The mutant's line `printf 'junk\rR\t0\tfake\n'` prepends `junk<CR>R<TAB>0<TAB>fake` to every
   vector's output. The payload therefore contains a CR.
3. `run_vectors` parses with `out.splitlines()` (`tool.py:284`). **`str.splitlines()` splits on CR
   as well as LF**, so each emitted record becomes two (`RC\t0\tjunk` and `R\t0\tfake`) and
   7561 vectors yield 15122 results.
4. `if rc != 0 or len(got) != len(vectors): raise CannotAudit(…)` (`tool.py:285-286`).
5. `main` catches `CannotAudit` and prints `TALLY_AUDIT: SETUP (…)`, **returning 2** (`tool.py:690-692`),
   before any `CHECK` or verdict line exists.
6. The counter maps `rc == 1 and last.startswith('TALLY_AUDIT: FAIL')` → `KILL`, `rc == 0 and
   …PASS` → `ACCEPT`, else `OTHER` (`c1-measure.py:255-260`), and counts a kill as
   `rc == 1 and last.startswith('TALLY_AUDIT: FAIL')` (`c1-measure.py:275,279`). `rc = 2` is
   neither, so `k_hit` stays 0 while `k_tot` increments — a **miss**.

The counter's block-level witness saw the same bytes correctly: `block_run` returns the last
`RC\t` record after the same `splitlines` split, giving `(0, 'junk')` vs pristine's PASS line. The
copy is behaviourally different; only the tool's whole-run record count check turns it into an
abstention.

The record boundary is not CR-specific: Python `str.splitlines()` also splits on `\v`, `\f`,
`\x1c`-`\x1e`, `\x85`, `\u2028`, `\u2029` (measured: each yields 2 lines for `"a<sep>b"`), so any
output byte that is a splitlines boundary in a must-kill copy takes the same exit-2 path. This is
the "per-index record parsing" Hold: the driver has no per-index identity, so a boundary forging or
deleting records is only visible as a count mismatch — and a count mismatch is routed to SETUP, not
FAIL.

## 6. Scoring direction (why the landed PASS still stands)

A SETUP is scored as *not killed*, which is **stricter against the tool** than treating SETUP as a
kill. Therefore this class can never turn a false measurement into `C1_R33_PASS=true`; it can only
understate kill coverage (a false negative that would fail an honest tool if such a copy were
sealed). The deciding run at `c17e593b` used a fixed set with no such copy (§7), so
`ho_kill=8/8` and `C1_R33_PASS=true` are unaffected by this find.

## 7. Sealed-set and pin hygiene checks

```
python3 -c "import glob; fs=sorted(glob.glob('lane/.ufo/evidence/round-33/heldout/*.json')); \
  hits=[p for p in fs if b'\r' in open(p,'rb').read()]; print(len(fs), len(hits), hits)"   # exit 0
heldout files=14 cr_hits=0 []
```

A second scan for the escaped forms (`\\r`, `\\x0d`, `\\v`, `\\x0b`, `\\f`, `\\x0c`, `\\x1c`,
`\\x1d`, `\\x1e`, `\\u2028`, `\\u2029`) and for `printf` in the same 14 JSON files found **0**
files. The sealed set cannot express this class, and a raw-byte CR scan alone is insufficient
hygiene because the injected CR here lives in a `printf` escape, not in the copy bytes.

## 8. Prior-round line (same class, earlier pin)

Round 33's `DevStderr` seat measured the same shape against tool sha `9dbbce62…33a4` at rev
`f6d8a891…` as `M19-cr-fake-record` (`.ufo/waves/round-33/w1/DevStderr.md`), with
`4754/2377 results`; the round-33 lesson routed it as "one escape into SETUP via an embedded-CR fake
record … routed: per-index record parsing" (`corpus/lessons/round-33.md:62-64`). At the round-34 pin
the vector universe grew (7561 per config; `15122/7561`), the escape is unchanged, and this seat
re-measures it through the counter's actual scoring functions rather than the raw tool alone.

## 9. Restoration and hygiene

- The pinned tool and runner were never mutated in place. `sha256sum tool.py pristine.sh` **after**
  all runs: `7b11ba25…8d10` / `a7d3f2dd…2eb9`, identical to the pre-run values and the tasking pins
  (`probe.py` re-prints both pins at the end of its run; `tool` hash in `PROBE_PINS` equals the
  start-of-run value).
- Lane bytes untouched: on-disk `lane/tools/tally-audit-v2.py` and `lane/tools/mutate-and-run.sh`
  re-hash to the pins; `git -C lane rev-parse HEAD` = `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`;
  every lane access was `show`/read; no git or jj write command was run anywhere.
- The mutants are separate files in `mutants/`; scratch contains `tool.py`, `pristine.sh`,
  `gen.py`, `probe.py`, `runs/`, `work/` only. No sibling repo, `MANIFEST.json`, `templates/`,
  `scripts/`, `.ufo/state/`, watchdog log, or lane jj/Git index was touched.
- Nothing installed or upgraded (no pacman/uv/npx/binary): `bwrap`, `python3`, `bash` were already
  present.
- Commands run and exit codes, all captured: `clone.exit 0`, `checkout.exit 0`, `show_tool.exit 0`,
  `show_sh.exit 0`, `gen.exit 0`, `probe.exit 0`, `runs/pristine.rc 0`, `runs/m19.rc 2`,
  `runs/m20.rc 1`, both scans exit 0.

## 10. Hold wording (measurement-only, ride to round 35)

**Hold — per-index record parsing (reproduced at `7b11ba25…8d10`, rev `0b99d48e…`):** a must-kill
copy whose block writes any `splitlines()` boundary (e.g. `printf 'junk\rR\t0\tfake\n'`) inflates
the audit driver's record count, raising `CannotAudit` (`tool.py:285-286`) and exiting 2 with
`TALLY_AUDIT: SETUP` (`tool.py:690-692`); the counter's kill predicate requires rc 1 + `FAIL`
(`c1-measure.py:275-279`), so the copy scores a miss (`score_tool` → `0/1`, measured). The copy is
valid under the amendment-6 witness rule (`ho_witness_ok` → `(True,'vector')`). Under the frozen
contract this is a coverage gap, not a contract defect: a future v3 should give each driver record
an index and treat duplicate/extra/out-of-range records as **mismatch (FAIL)**, reserving SETUP for
a driver that produced no record at all — that correction was already routed in round 33
(`.ufo/waves/round-33/w1/DevStderr.md` §"Smallest safe correction") and is **not** re-proposed as
landed work here. The landed measurement is unaffected: 14/14 sealed JSONs carry no boundary
injector.
