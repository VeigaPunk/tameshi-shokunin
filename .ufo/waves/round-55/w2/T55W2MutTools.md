# T55W2MutTools — falsify wave: is C2 per-mode attributable, and are the class-line mutations caught?

Seat: `T55W2MutTools` (mutation-tester). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit under test: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0). Base: `0a2010acd1e9…`.

## What I attacked

1. **Per-mode attribution of the C2 grammar arm.** Revert one tool's grammar line at a time
   (`repeat-control`, `context-capture`, `registry-check --rev`) and check that the counter loses
   exactly that one grammar mode and no other arm moves.
2. **The class line's own bytes.** Drop the value, drop the class token (both readings: the trailing
   `(could-not-evaluate)` and the leading `could-not-evaluate:` label), and move the line from
   stderr to stdout — for `repeat-control`, `context-capture` and `registry-check --rev`. Which arm
   catches each?
3. **A survivor probe (extra).** Print another tool's prefix on the line and see whether any arm
   notices.

Everything ran on commits in a scratch `git clone --shared` of the lane at C0. The lane was only
read; no lane file, no frozen file, no wave file was modified by this seat.

## Counter bytes I measured with

```
sha256sum .ufo/evidence/round-55/c2/measure.py
0458f632087f665fbafc07efc6920d32febf7551d9fc5964d0c87fa0e139476b  .ufo/evidence/round-55/c2/measure.py
git rev-parse HEAD:.ufo/evidence/round-55/c2/measure.py
6bc003725a5813264f4016b44d6fea90031145cb      # amendment 8, lane HEAD 4f7a7040
```
The worktree file is byte-identical to the HEAD blob (same sha256) and did not change during the
runs. The counter is invoked with `--lane <scratch-clone> --rev <mutant>` and clones the mutant
revision internally, so every arm measured the committed mutant tree, never a dirty worktree.

No tools were installed or upgraded for this seat (nothing was missing: `git`, `python3`, `strace`
were present; pacman was not touched).

## Control: pristine C0

```
python3 .ufo/evidence/round-55/c2/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb \
  --work /fast/scratch/hyaku/tameshi-r55/T55W2MutTools/w-base --explain
C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```
exit 0, 377 s. Receipt: `T55W2MutTools-receipts/base.out`.

## Experiment 1 — revert each tool's grammar line (one at a time)

Each mutant is one commit on C0 in the scratch clone. `git diff --stat C0 <mutant>` is the base→C0
delta in that single file (the whole base→C0 delta of each file is its grammar line):

| mutant (branch @ rev) | reverted | diff vs C0 |
|---|---|---|
| `m-rc-revert` @ `56efd4a83cfd` | `tools/repeat-control.py` | 1 file, +1 −21 |
| `m-cc-revert` @ `db6f5e0b89c3` | `tools/context-capture.py` | 1 file, +1 −10 |
| `m-reg-revert` @ `9b2eaaf2b038` | `tools/registry-check.py` | 1 file, +1 −13 |

Verdict lines (full strings in `receipts/runs/*/verdict.out`):

```
control          C2_R55: rev=9cf0146b94dd grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
m-rc-revert      C2_R55: rev=56efd4a83cfd grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
m-cc-revert      C2_R55: rev=db6f5e0b89c3 grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
m-reg-revert     C2_R55: rev=9b2eaaf2b038 grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

`bad` map of each (from `receipts/runs/*/c2-receipts.json`) names exactly one mode:

```
m-rc-revert  {"repeat-control --selftest":   "grammar rc=2 stderr=[\"repeat-control: setup: RuntimeError: cannot create clone scratch … (could-not-evaluate)\"]"}
m-cc-revert  {"context-capture --selftest":  "grammar rc=2 stderr=[]"}
m-reg-revert {"registry-check --rev":        "grammar rc=2 stderr=[]"}
```

The bytes each reverted tool actually emits (direct probe, `TMPDIR` = a nonexistent path,
`receipts/direct/*.err|.out`, `receipts/direct-rev/*`):

```
m-rc-revert  stderr: repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '…/no-such-tmpdir' (could-not-evaluate)
             stdout: REPEAT_CONTROL: setup_error
m-cc-revert  stdout: SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: … )
             stderr: (empty)
m-reg-revert stdout: REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: … )
             stderr: (empty)
```

**Verdict (experiment 1): all three mutants killed, each by exactly one mode, and nothing else
moves.** `lazy`, `empty`, `usable`, `tmp_mkdirs`, `docs`, `note`, `skill` read bit-identical to the
control in all three runs; `total` moves 0 → 1. The grammar arm is mode-attributable: the `bad` key
is the mode as invoked, so a regression names the tool+mode that causes it, not just "grammar
broke". Restoring the tool bytes restores the control verdict exactly (the control run is that
restoration: same counter bytes, `total=0`, `PASS=true`).

## Experiment 2 — mutate the message (which arm catches it?)

All on `repeat-control` except where noted; each is a one-line diff versus C0.

| mutant @ rev | mutation | emitted class line | caught by | modes lost |
|---|---|---|---|---|
| `m-rc-drop-value` @ `46919de656b6` | drop the quoted value (`: %r` removed) | `repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory (could-not-evaluate)` | grammar | 1 |
| `m-rc-drop-class` @ `6edf771bb26e` | drop the trailing class token `(could-not-evaluate)` | `… TMPDIR is not a usable directory: '…/no-such-tmpdir'` | grammar | 1 |
| `m-rc-drop-label` @ `b6c5b6893f7b` | drop the leading class label `could-not-evaluate:` | `repeat-control: cannot create clone scratch under the scratch root: … (could-not-evaluate)` | grammar | 1 |
| `m-rc-stdout` @ `7aeb829acc9c` | line to stdout | correct line, on **stdout**; stderr empty | grammar | 1 |
| `m-cc-stdout` @ `56ad1289efa5` | line to stdout | `context-capture.py: could-not-evaluate: …` on **stdout**; stderr empty | grammar | 1 |
| `m-reg-stdout` @ `7530d5ba9fd3` | `--rev` path line to stdout (`--selftest` left on stderr) | correct line on **stdout**; stderr empty | grammar | 1 (`registry-check --rev`) |

Verdict lines:

```
m-rc-drop-value   C2_R55: rev=46919de656b6 grammar=8/9 … total=1 C2_R55_PASS=false
m-rc-drop-class   C2_R55: rev=6edf771bb26e grammar=8/9 … total=1 C2_R55_PASS=false
m-rc-drop-label   C2_R55: rev=b6c5b6893f7b grammar=8/9 … total=1 C2_R55_PASS=false
m-rc-stdout       C2_R55: rev=7aeb829acc9c grammar=8/9 … total=1 C2_R55_PASS=false
m-cc-stdout       C2_R55: rev=56ad1289efa5 grammar=8/9 … total=1 C2_R55_PASS=false
m-reg-stdout      C2_R55: rev=7530d5ba9fd3 grammar=8/9 … total=1 C2_R55_PASS=false
```
(full strings in `receipts/runs/*/verdict.out`; every `bad` map is the single mode named in the
table, always `grammar rc=2 stderr=…` — for the stdout mutants `stderr=[]`.)

Arm-level corroboration with the counter's *own* predicate (import of the frozen
`GRAMMAR` regex against the captured streams, `receipts/armcheck.py`, output `armcheck.json`):

```
m-base            grammar=True   RuntimeError=False  stderr=[correct one line]
m-rc-revert       grammar=False  RuntimeError=True   stderr=[repeat-control: setup: RuntimeError: …]
m-rc-drop-value   grammar=False  RuntimeError=False  stderr=[… usable directory (could-not-evaluate)]
m-rc-drop-class   grammar=False  RuntimeError=False  stderr=[… usable directory: '…/no-such-tmpdir']
m-rc-drop-label   grammar=False  RuntimeError=False  stderr=[repeat-control: cannot create …]
m-rc-stdout       grammar=False  RuntimeError=False  stderr=[]
m-cc-revert       grammar=False  RuntimeError=True   stderr=[]
m-cc-stdout       grammar=False  RuntimeError=False  stderr=[]
m-rc-wrong-prefix grammar=True   RuntimeError=False  stderr=[env-diff: could-not-evaluate: …]
```

**Verdict (experiment 2): every message mutation is killed, all by the grammar arm and only by it.**
That is structural, not an accident of these three mutations: `docs` (7 registry cells), `note`
(`corpus/knowledge/scratch-root-contract.md`) and `skill` (`SKILL.md`) are *static-text* arms — they
read the documents at the mutant revision, so they stayed 7/7, 9/9, 1/1 in every run, including the
runs where the tool emitted a line missing the value or the class token. The grammar arm is the only
arm that reads the tools' bytes, so message drift has exactly one detector (one per affected mode).
The `RuntimeError`/`Traceback` clause is a second, independent detector in the revert case; in the
message mutants it is silent, and the grammar regex alone carries them.

## Experiment 3 — survivor probe: the line names the wrong tool

```
m-rc-wrong-prefix @ 913cdfca57a3
diff: emit_err(f"repeat-control: could-not-evaluate: {message}")  →  emit_err(f"env-diff: could-not-evaluate: {message}")
C2_R55: rev=913cdfca57a3 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
bad map: {}
exit 0
```

**SURVIVOR — PASS=true, `total=0`, empty `bad` map.** `repeat-control --selftest` prints
`env-diff: could-not-evaluate: …` and the counter accepts it: `GRAMMAR`'s prefix is
`^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?:` — any name. The note's grammar states `<tool>: …`, and this
mutant's line names a different tool while the run's `--lane/--rev` is the mutant's; no arm binds the
prefix to the tool being executed (the docs/note/skill arms only compare static text).

Impact: a caller that keys on the prefix (the counter's own `cannot_see` says the contract does not
pin whether callers parse by prefix or whole line) can now attribute the refusal to the wrong tool —
and the round's "one grammar, nine modes" verdict is silent on per-tool attribution. Severity is
limited: the line still has one shape, one stream, and exit 2. **Coverage finding, not a contract
change** — I did not alter the counter; the fix would be to bind the prefix per mode inside the
grammar arm (the arm already knows which tool each mode invokes).

## Findings

- **F1 (positive, operability).** Per-mode attribution holds: three grammar-line reverts each lose
  exactly their one mode (`grammar 9/9 → 8/9`, `total 0 → 1`), with every other arm unchanged, and the
  `bad` map names the mode as invoked. A regression therefore names its tool, not just "grammar".
- **F2 (coverage, by design).** Message drift — missing value, missing class token in either
  position, line on stdout — is caught by the grammar arm only, once per emitting mode. The three
  document arms are static-text arms and cannot see the bytes a tool emits; the multi-arm structure
  is not independent verification of the tool output.
- **F3 (survivor, real gap).** The grammar's tool prefix is unbound: a tool printing another tool's
  name passes every arm (`total=0 C2_R55_PASS=true`). Command and output above.
- **F4 (record defect in the frozen counter, no scoring effect).** `c2/measure.py`'s docstring still
  advertises **8** allocating modes and `note=N/8` (`measure.py:17,28,32`), while the arms measure
  **9** (`c2-receipts.json` → `allocating` has 9 entries, including `registry-check --rev` added by
  amendment 6; amendment 8 fixed the code's denominators, not the docstring). A reader of the
  counter's own contract understates the arm by one mode. Frozen file — reported, not edited here.

## Lane integrity / restoration

All mutations live in commits inside `/fast/scratch/hyaku/tameshi-r55/T55W2MutTools/mut`; nothing
was written into the lane. Evidence from the lane (read-only commands):

```
git -C <lane> rev-parse HEAD                      → 4f7a7040a57e (moved during this seat by other seats)
git -C <lane> diff --stat 9cf0146 HEAD -- tools/  → (empty: the lane's committed tools/ still equal C0)
sha256 worktree vs C0 blob:
  tools/repeat-control.py   worktree=a8fad68fcbb8 c0=a8fad68fcbb8 SAME
  tools/context-capture.py  worktree=831b781054d7 c0=f1043425085a DIFF
  tools/registry-check.py   worktree=7984540cd3cb c0=639eda19af44 DIFF
```

The two DIFF lines are **not this seat's work**: another seat has uncommitted edits in the lane
worktree for exactly those two files (`git diff --stat HEAD -- tools/context-capture.py
tools/registry-check.py` → +28 −10, mtime 14:30:24, between my control run's clone at 14:25:30 and
my mutant runs). Their sha256 was identical at both of my checks (14:44 and 14:49), and this seat
issued no write to the lane — its only lane writes are this report and `T55W2MutTools-receipts/`.
Every measurement is anchored to committed bytes (`clone --shared` + `checkout -B r55-rev <mutant>`
on the *commit* of each mutant, and the control at the lane's C0 commit), so a dirty worktree could
not enter a verdict.

Scratch was removed with `rm -rf` of this seat's own directory only, after the receipts below were
copied out.

## Receipts (`T55W2MutTools-receipts/`)

| file | content |
|---|---|
| `base.out`, `base.err` | control run at C0 (`total=0 PASS=true`), `--explain` |
| `mutants.json`, `mutants.err` | every mutant branch, rev, `git diff --stat`/full diff vs C0 |
| `runs/<mutant>/verdict.out`, `verdict.err` | the counter's `--explain` output and stderr per run |
| `runs/<mutant>/c2-receipts.json` | the counter's own receipt (arms, `bad` map, allocating list) |
| `runs/<mutant>/summary.txt` | branch/rev/rc/elapsed + verdict line + `bad` map |
| `direct/<branch>.{out,err}`, `direct.txt` | single-mode direct probes under unusable `TMPDIR` |
| `direct-rev/<branch>.{out,err}` | `registry-check --rev` refusal bytes (base / revert / stdout) |
| `armcheck.py`, `armcheck.json` | frozen `GRAMMAR` applied to the captured streams |
| `setup_mutants.py`, `run_counter.sh`, `direct_probe.sh` | the exact drivers (anchors asserted; toplevel checked before every commit) |
