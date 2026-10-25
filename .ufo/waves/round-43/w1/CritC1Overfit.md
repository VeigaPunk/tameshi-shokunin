# CritC1Overfit — kill-oracle overfit (C1, depth)

Seat: `L1Tameshi43.CritC1Overfit`. Read-only on the lane; work under
`/tmp/tameshi-r43-CritC1Overfit-/`. No installs (system `python3 3.14.8`).

## Verdict

**The literal route in my item does not pass, and it does not print a field: it
crashes before the receipt.** The tool pin is not what stops it — `self_pin` is
(`.ufo/evidence/round-43/mutants/measure.py:486-492`), and the substitution is
green in every other measured field. Three demonstrated paths make an 8 KB
lookup-table tool print `C1_R43_PASS=true`: a spoofed `__file__`, a fabricated
`--lane`, and a fabricated lane against the **pending** counter edit. The K
reachability gate is **fixture-granular, not site-granular**.

Counterexample (one line): a table keyed by the twelve fixture basenames plus
`context-capture`/`registry-replay`, `sites: []` for anything else, no `ast`
import, yields `C1_R43_PASS=true` — with the executed counter bytes
(`4339186a…`, `b56a34d7…`) never equal to the attested bytes (`0d0f81bd…` /
the fabricator's own pin).

## Anchors — the freeze moved five times during this seat

| item | value |
|---|---|
| item's cited freeze | `17f6ef0…`, C1 counter pin `ad7ecf8c…` |
| freeze chain observed | `17f6ef0` → `5cd2154` (A4/A5) → `114ffac` (A6/A7) → `273c047`/`3aee2c0` (A9/A10) → `e20cf89` |
| **receipts below run at** | rev = freeze = `3aee2c078f8976499b587086af3577fc94dc8cf1` |
| C1 counter bytes there | `0d0f81bdbe09bb53997ade30911fc178a38de072f84aacf23c6c9c0a710e57f1` |
| contract bytes there | `9e24154a093c781ecdd42e8ae0bcaf2c61215736c4065112ff037547a2433e94` |
| census tool pin (`frozen_tools`) | `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5` |
| lane working tree, at write time | counter **dirty** `3d1ff3dc6b75658dfbb5ada11a310ff3067144ae11bd30c8cc4147ad40eed8c0`, contract still pinning `0d0f81bd…` |

A5 fixed the two defects my first probe hit at `17f6ef0` (`tool_sha_ok` read the
guard's hash; the K reachability sentence was not implemented → `killed=6`). A9
fixed live-site reachability and the `--probe-mutant` verdict. **None of A5/A9/A10
touched `self_pin`'s `__file__` input, `--lane`, `stage()`-then-run, or the
absence of a contract/mutant-set pin** — so the three bypasses below survive all
of them.

Genuine baseline at `3aee2c0` (read-only; not the deciding run):

```
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12
run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6
mutants_killed=5 dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0
apply_error=0 unresolved=0 … dead_code_cases=F12_method_two_returns
dead_code_arg_ok=1 kill_fixture_reachable=1 … C1_R43_PASS=true
```

## The substitute

`/tmp/tameshi-r43-CritC1Overfit-/gen/overfit-census.py`,
sha256 `2b3d17445617bb995e26171845c756d261aca2bd6f835596437322bedc1a4e21`
(8 085 B): `TABLE` = the pristine v4 output per fixture/live file (fingerprints
match exactly), `classify()` = `TABLE.get(basename-without-.py, [])`. Imports
`argparse, json, os, sys` only. Scored with the counter's own functions on
`3aee2c0`:

```
text_mode=False fixtures_pass=12/12 fails=0 errors=0 live_ok=3/3
lane_unflagged=0 tool_errors=0 over 27 tools
```

(Text mode fails F04/registry-replay only because the counter's text parser cannot
express `explicit_out`, `:280-310`; every measurement `battery()` call is JSON —
`:527`, `:566`.)

## E1 / E2 — literal substitution (`TOOL_REL` re-pointed, clone in /tmp)

```
E1  TOOL_REL = '/tmp/…/gen/overfit-census.py'   exit=1, no C1_R43 line
E2  TOOL_REL = 'tools/overfit-census.py'        exit=1, no C1_R43 line
    Traceback … line 559, in main
      body, count = apply_once(tool_raw.decode(), mut['find'], mut['replace'])
    AttributeError: 'NoneType' object has no attribute 'decode'
```

`tool_raw = show(lane, rev, TOOL_REL)` (`:495`) is `None` for an absolute `/tmp`
path and for a relative path absent at REV; `tool_absent=1`, `tool_sha_ok=0` are
computed but **the run dies at `:559` before any field is printed** (also `:534`
in `--control`). Exact values, probed through the counter's own functions:

| variant | self_pin | tool_absent | tool_sha_ok | selftest_exit | fixtures | run_errors | live_ok |
|---|---|---|---|---|---|---|---|
| E1 absolute | 0 (running `affad992…` ≠ pin) | 1 | 0 | 0 | 12/12 | 0 | 3/3 |
| E2 relative | 0 (running `f1a5113c…` ≠ pin) | 1 | 0 | 1 | 0/12 | 15 | 0/3 |

E1 is the sharper one: an absolute `TOOL_REL` makes `os.path.join(work,'live',TOOL_REL)`
return the `/tmp` path (`:504`), so selftest + battery + `lane_unflagged` all run
the substitute **green**; only the missing `tool_raw` guard and `self_pin` stand in
the way. A missing `None` guard is also a robustness defect: a seat gets a
traceback instead of a refusal.

## E3 — one statement after `stage()`, no pin line touched

`counter3/measure-stage.py` (sha `4339186a…`), insertion at clone `:503-506`
writing the substitute over `work/live/tools/write-path-census-v4.py`:

```
C1_R43: self_pin=0 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12
run_errors=0 live_ok=3/3 live_unflagged_v4=0 … mutants_killed=5 dead_code_only=1
dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1
… C1_R43_PASS=false
```

**The only failing field is `self_pin`.** `tool_sha_ok` stays 1 because it hashes
the git blob (`:495`, `:499`) while the executed bytes are the staged copy
(`:504`); the bytes that run are never hashed anywhere.

## E4 — bypass #1: `self_pin` attests a path, not the code

`:490` opens `os.path.abspath(__file__)`; `__file__` is caller-controlled, so
`exec(compile(<modified source>, <pristine path>, 'exec'), {'__file__': <pristine path>, …})`
(`/tmp/…/run-spoofed.py`; the executed clone is `counter3/measure-stage.py`,
sha `4339186a…`):

```
self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12
run_errors=0 live_ok=3/3 live_unflagged_v4=0 … mutants_killed=5 dead_code_only=1
dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_fixture_reachable=1
C1_R43_PASS=true       (exit 0)
```

executed counter `4339186a…` ≠ attested `0d0f81bd…`; tool `2b3d1744…`. No field is
forged — only the tool bytes are substituted and `self_pin`'s input redirected.
`self_pin` authenticates a filename variable; any receipt field is therefore
forgeable by a modified counter that the pin cannot see.

## E5 — bypass #2: `--lane` is caller-chosen; the contract pins itself

`lane = os.path.abspath(args.lane)` (`:475`); the contract read from that lane
(`:481`) supplies the counter pin (`:485`) *and* the tool pins (`:498`), and
`mutants.json` comes from the same lane (`:530`, `:551`). The contract has **no
self-hash** (all sha-like fields: three `claims.*.counter_sha256`, `tool_sha256`,
two `frozen_tools`), and `mutants.json` has **no pin** (`contract.json:33` is
prose: "at REV, unchanged"). Fabricated repo `/tmp/…/fakelane3`, commit
`76d5f2c5…`: pristine counter bytes, census pin = toggle-table tool
`2bc2c02f…`, six-entry `mutants.json` authored over that tool. **Unmodified**
frozen counter:

```
self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12
run_errors=0 live_ok=3/3 live_unflagged_v4=0 … mutants_killed=5 dead_code_only=1
killed_names=attr_bind_several_assignments,attr_never_resolve_self,
method_fold_disabled,outflag_dests_never_recorded,outflag_no_parse_args_check
dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns
dead_code_arg_ok=1 kill_fixture_reachable=1 C1_R43_PASS=true      (exit 0)
```

The receipt is indistinguishable in kind from the genuine one — same names, same
cases, only `rev`/`freeze` differ. The counter cannot distinguish a lookup table
from a parser, a fabricated lane from the real one, or a bespoke mutant set from
the declared one.

## E6 — the K gate is per fixture, not per failing site

`:570-571` (`reachable_fails = [case for case in mdetail if not mdetail[case]]`)
derives one boolean per fixture from `unreachable_statements(fixture_source)`. In
`fakelane3` the `method_fold_several_returns` mutant corrupts F12's **reachable**
write at line 11 (`{"expected": true, "kind": "open", "lineno": 11,
"resolved": "self.destination()"}`; only line 10, `return os.path.join('golden'…)`,
is dead) and is still reported as `dead_code_names=method_fold_several_returns
dead_code_cases=F12_method_two_returns`. Any fixture containing one dead statement
becomes an immunity certificate for any mutant that fails only there. `check_site`
(`:314`) already knows the failing `lineno`; the rule's unit should be the site.

Related surface on the same axis: the twelve fixtures are fixed sources written to
predictable names in a `mkdtemp` dir (`FIXTURES` `:66`, `stage()` `:423-426`),
`check_site` (`:314`) accepts on `(lineno, four booleans, needle substring)`, and
`lane_unflagged` (`:441-448`) sums `site['unflagged']` **over the tool's own
report** — a tool returning `sites: []` is arithmetically clean (that is how the
substitute yields `live_unflagged_v4=0` over 27 staged tools).

## E7 — the pending repair is fabricable too

While this seat ran, the lane re-froze and then left `.ufo/evidence/round-43/
mutants/measure.py` **dirty** at HEAD `e20cf89`: the snapshot I tested is
`b56a34d7…` (contract still pinning `0d0f81bd…`); the worktree has since moved on
again to `3d1ff3dc…`, still dirty. The pending edit adds
`claims.C1.mutants_sha256`, `kill_binding` (kill must be bound to
`F11_outflag_namespace`) and `kill_cases`, and drops `kill_fixture_reachable`.
Given a fabricated contract that pins the fake `mutants.json` and the fake
counter, the pending counter prints:

```
self_pin=1 … mutants_killed=5 dead_code_only=1 … kill_binding=1
kill_cases=…outflag_no_parse_args_check:F11_outflag_namespace mutants_sha_ok=1
C1_R43_PASS=true      (fakelane3 commit 21d653ae…)
```

**Pinning `mutants_sha256` inside the contract read from `--lane` does not close
E5**: the fabricator writes the hash of their own mutant file into their own
contract. Only a pin held outside the measured lane does.

Live hazard for the L1: with the working tree dirty the counter no longer matches
the contract pin, so **every parallel seat running the working-tree counter right
now gets `self_pin=0`**; and if the edit is committed without adding
`claims.C1.mutants_sha256`, `mutants_sha_ok` is 0 by construction. Re-freeze must
move counter bytes, contract pin, and `mutants_sha256` in one commit before the
deciding run.

## Smallest safe correction (priority order)

1. **`self_pin` must attest the code that runs, not `__file__`.** Minimum: refuse
   unless `os.path.realpath(sys.argv[0]) == os.path.realpath(__file__)` and the
   opened file's `os.stat` is the one the loader read; that kills the
   `-c`/`exec` redirect (argv[0] is `-c`). Better: hash the module source the
   interpreter actually loaded (`__loader__.get_source`/a `runpy` entry point) and
   compare with the pin, or have the harness pass the expected sha from outside
   the lane.
2. **Hash the bytes that execute.** After `stage()`, `sha256` the file at
   `tool_path` (`:504`) and print it as `tool_exec_sha`, comparing it to the pin;
   today `tool_sha_ok` certifies the git blob while `:504` runs a possibly
   different file. Also guard `tool_raw is None` before `:534/:559` so a
   substitution attempt yields a refusal, not a traceback.
3. **Pin the contract, the mutant set and the census tool out of band** — constants
   in the L1's receipt, verified via `--contract-sha/--mutants-sha`. This removes
   E5 and E7 in one move; a field inside the measured lane cannot do it.
4. **Apply reachability at the failing site** (`check_site` returns `lineno`):
   mark a case dead only when that line is dominated by an unconditional
   return/raise in its block. Removes E6.
5. **Make `lane_unflagged` independent of the tool's report**: count write calls
   with a separate AST scan of the staged files and require agreement; a
   `sites: []` tool then fails instead of passing.

## Impacted axes

- **depth** (C1): the kill oracle's case layer is overfittable
  (12/12 + 3/3 + 0 unflagged with zero parsing), its provenance chain is not
  anchored (`self_pin` on `__file__`, contract/lane relativism), and the K gate's
  unit is the fixture, not the failing site.
- **calibration**: receipt fields agree while referents differ — a lookup table
  reads as a parser and a fabricated lane reads as the real one.
- **operability**: fixture-name coupling plus lane-relative pins are reusable by
  any later counter with the same shape; the missing `None` guard turns any
  substitution attempt into a traceback.

## Reproduction / retained artifacts

```
# E4: one statement after stage() + spoofed __file__  -> C1_R43_PASS=true
python3 /tmp/tameshi-r43-CritC1Overfit-/run-spoofed.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 \
  --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1

# E5/E6: unmodified committed A10 counter, fabricated lane -> C1_R43_PASS=true
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  3aee2c0:.ufo/evidence/round-43/mutants/measure.py > /tmp/tameshi-r43-CritC1Overfit-/counter-a10.py
python3 /tmp/tameshi-r43-CritC1Overfit-/counter-a10.py \
  --lane /tmp/tameshi-r43-CritC1Overfit-/fakelane3 \
  --rev 76d5f2c5a19c40a0682d85edff1170d7058ab04e \
  --freeze 76d5f2c5a19c40a0682d85edff1170d7058ab04e

# E7: pending counter (b56a34d7…) in the same lane, commit 21d653ae…
python3 /tmp/tameshi-r43-CritC1Overfit-/counter3/measure-pending.py \
  --lane /tmp/tameshi-r43-CritC1Overfit-/fakelane3 \
  --rev 21d653aed6b3a6233bec64fbfc93bbc010bd8fc2 \
  --freeze 21d653aed6b3a6233bec64fbfc93bbc010bd8fc2
```

Run the counter from the committed blob (`counter-a10.py`), never from the lane's
working tree: the worktree file is dirty and unpinnable.

Retained under `/tmp/tameshi-r43-CritC1Overfit-/` for verification:
`gen/overfit-census.py`, `counter3/measure-stage.py`, `counter3/measure-pending.py`,
`run-spoofed.py`, `B0/E3p/E4p/E6p/E7p.stdout`, `fakelane3/`. The lane was not
modified by this seat (`git status` shows only other seats' files and the L1's own
counter edit). Nothing here is a measurement of the claim: the baseline is
read-only context; the deciding run remains the L1's.
