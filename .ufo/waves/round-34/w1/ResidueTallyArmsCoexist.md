# ResidueTallyArmsCoexist — round-34 w1 mutation seat

Claim under attack: C1 (operability, `tools/tally-audit-v2.py`) measured TRUE at
`c17e593b51802dd4ed568da3265f21c6d00c4273`. This seat attacks one routed v3 residue class,
measurement-only: **TallyArms-02 coexistence** — a block edit that makes statuses 126 and 127
coexist in the tally count. The deciding run stands; no contract change is proposed; the tool
stays frozen.

## Verdict first

**KILLED at the pin.** Mutant `a3ae612e…321e9` (byte-identical to replaying the committed
round-32 sealed copy `HeldOutTallyArms-02.json` against the pinned runner) is rejected by the
frozen tool: `CHECK runtime FAIL vectors=15158 mismatched=1584`, `TALLY_AUDIT: FAIL`, exit 1.
Pristine and restored bytes audit `PASS`, exit 0. The kill rides entirely on the co-occurrence
sweep (`tool.py:403-414`); the pre-amendment bytes recorded by round-33 ReviewTool survived this
class, the current pin does not. There is no false positive on the equivalent twin (explicit
`126)`/`127)` `+1` arms), which audits PASS.

## Frozen bytes, verified before any run

Extracted from a detached clone of the lane at the dispatch tip (writes only in seat scratch):

| object | sha256 | source |
|---|---|---|
| `tool.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | `git show 0b99d48:tools/tally-audit-v2.py`; equals the brief pin |
| `pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `git show 0b99d48:tools/mutate-and-run.sh`; equals the brief pin |
| counter `c1-measure.py` (not run) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | live lane; matches brief `f6b8868c…a07f28c` (rev `6aaad5b3`) |
| controls receipt (not run) | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` | live lane `.ufo/evidence/round-33/c1/controls-receipt.json` |

The same two blobs hash identically at the measurement revision and at the live lane HEAD, which
advanced after dispatch — the frozen pins still describe live bytes:

```
$ for rev in 0b99d48… c17e593b… a5b19364…; do git -C lane show $rev:tools/tally-audit-v2.py | sha256sum; done
7b11ba25…8d10   (x3, exit 0; git cat-file -e <rev>^{commit} exit 0 each)
$ for rev in 0b99d48… c17e593b… a5b19364…; do git -C lane show $rev:tools/mutate-and-run.sh | sha256sum; done
a7d3f2dd…2eb9   (x3)
```

Lane HEAD at probe time was `a5b1936425d3533b2ce280b16208386dcb0dc4ee`; the clone is detached at
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (`git rev-parse HEAD` exit 0). `c17e593b` is an
ancestor of the tip (`git merge-base --is-ancestor`, exit 0), and the committed receipt
`.ufo/evidence/round-34/measure/c1-deciding-run.stdout` still reads
`C1_R33: … ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 … C1_R33_PASS=true`,
with `.exit` = `0`.

## The mutant

One insertion in `run_regression`'s tally block (`pristine.sh:1432-1439`, arms `1435-1437`):

```diff
     case $st in
       0) npass=$((npass + 1)) ;;
       1) nfail=$((nfail + 1)) ;;
+      126|127) nsetup=1 ;;
       *) nsetup=$((nsetup + 1)) ;;
     esac
   done
```

`diff -u pristine.sh mutated.sh` exit 1 (one hunk, above); mutant sha256
`a3ae612ea62941706f9dbc6dff63bba75fcc2fd940ac9d0b9bd2e549123321e9`.

Provenance to the routed class: applying `edits[0]` of the committed round-32 sealed copy
(`.ufo/evidence/round-32/heldout/HeldOutTallyArms-02.json`, tree blob `618c59e1…`, file sha256
`1ab0f6446daa913481e07945f7073fb598971981b760ef4aec25cb599fe815f8`) to the pinned runner yields
exactly that sha — `old_occurrences 1`, `json_mutant_sha256 a3ae612e…`, script exit 0. The
mutant bytes are preserved as `mutant-from-json.sh` after restoration.

### Non-equivalence witness (independent of the tool)

`witness.sh` extracts the block the way the runner's own harness does (from `local nlegs=9` to the
line before the closing `}`) and drives it under the tool's hermetic config (`root=tally-audit`,
`auto=0`, `KEEP=1`), stderr discarded, first stdout line + exit compared:

| vector | pristine | mutant |
|---|---|---|
| `126 127 0 0 0 0 0 0 0` | `RC=2` `SETUP (cases=9 passed=7 cannot-verify=2)` | `RC=2` `SETUP (cases=9 passed=7 cannot-verify=1)` |
| `127 126 0 0 0 0 0 0 0` | `RC=2` `… cannot-verify=2` | `RC=2` `… cannot-verify=1` |
| `126 127 1 0 0 0 0 0 0` | `RC=1` `FAIL (cases=9 passed=6 failed=1 setup=2)` | `RC=1` `FAIL (… failed=1 setup=1)` |
| `126 0 …` / `127 0 …` | `RC=2` `… cannot-verify=1` | identical |
| `2 2 0 …` (control) | `RC=2` `… cannot-verify=2` | identical |

The defect is observable only when a 126/127 is counted after another setup-class increment:
`nsetup=1` assigns rather than increments, so it discards what was already counted (a status 2, an
earlier 126, or a `2 2` prefix ahead of it). All
witness invocations exited 0 at the harness level; per-case RC is in the table (files
`runs/{pristine,mutated}-*.out/.exit`).

## Detector: the frozen audit on three byte states

Same bounded detector each time: `TMPDIR=$PWD/tmp python3 tool.py --runner <copy>` (the tool is
never edited; `TMPDIR` pinned inside seat scratch).

| bytes | exit | verdict line |
|---|---|---|
| pristine (`a7d3f2dd…`) | **0** | `CHECK head PASS … CHECK static PASS … CHECK runtime PASS vectors=15158 mismatched=0 … CHECK harness PASS reference cases=9; faults rejected=34/34` / `TALLY_AUDIT: PASS` |
| mutant (`a3ae612e…`) | **1** | `CHECK head PASS legs=9` / `CHECK static PASS legs=9 operands=9 nlegs=9` / `CHECK runtime FAIL vectors=15158 mismatched=1584; first: cfg(0,1) statuses 2 126 0 0 0 0 0 0 0: got (2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=1)'), want (2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')` / `CHECK harness PASS reference cases=9; faults rejected=34/34` / `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| restored (pristine bytes) | **0** | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, `runtime vectors=15158 mismatched=0` |

Head and static pass on the mutant by design: the edit is block-local; only the behavioral sweep
can see it.

## Where the kill comes from (and why the class was a residue)

Importing the frozen tool read-only in scratch (`analyze.py`, exit 0) records the exact vector
list `check_runtime` feeds to `run_vectors` and replays pristine/mutant through the tool's own
oracle (`tool.py:290`):

- 7561 vectors per config, 36 operand-stress runs, 2 configs → 15158 reported; mutant mismatches
  **792 per config / 1584 total**, exactly the tool's count; pristine **0** mismatches.
- Breakdown of the 792: `both 126 and 127` = 72 (36 position pairs × 2 orders); `exactly one of
  126/127` = 720 (a setup-class status at an earlier position, so the later `nsetup=1` resets it:
  e.g. `2 126`, `3 127`, `9 126`, plus the doubled `126 126` / `127 127` shapes);
  `single-nonzero-status` = **0**; `neither 126 nor 127` = **0**.
- The 2377 vectors that predate the co-occurrence sweep (2304 single-status + 55 count-pair + 18
  placement; `tool.py:379-402`) produce no mismatch; all 792 live in the 5184 co-occurrence
  vectors (`tool.py:403-414`; `CO = (1, 2, 3, 4, 5, 7, 9, 120, 126, 127, 128, 255)` at line 407,
  ordered pairs at lines 408-411). The assigned witness `[126,127,0…]` and its reversal are both
  present and both mismatch.
- This is the round-33 amendment (b) sweep, so the class that round-33 ReviewTool recorded as a
  **false PASS** at the pre-amendment bytes (`9dbbce62…`/608 lines, 2395 vectors; ReviewTool
  CRITICAL 2, `.ufo/waves/round-33/w1/ReviewTool.md`, sha256 `fcea7ed2…56dc`) is closed at the
  pin. Round-34 Holds names the class as unadopted pre-data (`corpus/lessons/round-34.md:57`),
  which is consistent: the sweep, not the sealed set, is what kills it.
- The round-33 sealed set contains no 126/127 arm (`grep 126 .ufo/evidence/round-33/heldout/*.json`
  exit 1), so this coverage is structural in the sweep, not a replay of a committed copy. That is
  an observation about the sealed set, not a defect in the deciding run (`ho_kill=8/8` measures
  those eight copies).

### The runner's own guard is blind to it

The embedded tally harness (`pristine.sh:2008-2032`: all-pass, one status 1 and one status 2 at
each of 9 positions, `[1,1,…]`, `[2,2,…]`, `[1,2,…]`, `[3,0,…]`; plus the drop-last-operand guard
stress at `2033-2040`) never constructs a 126/127 coexistence vector. Replayed through the same
driver, all 23 harness vectors plus the drop-operand stress give **0 differences** between
pristine and mutant (`analysis.py`: `harness_vectors_tried=23`, `differences=0`; drop-operand
both `SETUP (case-tally mismatch: cases=9 counted=8)`). `CHECK harness PASS` on the mutant is
expected — that check replays `REF_BLOCK`-derived faults against the harness, not the mutated
block. Only the tool's co-occurrence sweep separates the two.

## No false positive on the equivalent twin

Control (not the assigned defect probe): explicit arms `126) nsetup=$((nsetup + 1)) ;;` and
`127) nsetup=$((nsetup + 1)) ;;` inserted before `*)` (`mutant-accept-twin.sh`, sha256
`57315ca1aba8fc1da3e31e700068440377962b30d1ab39b62d7403913d0f7bc1`; `runs/twin.diff`).

- Audit: exit **0**, `TALLY_AUDIT: PASS`, `runtime vectors=15158 mismatched=0`.
- Equivalence (`equiv.py`, exit 0): 0 differences vs pristine over **15122 runs** across both
  configs (`config (0,1): 0`, `config (1,0): 0`); witness outputs identical on all four vectors tried.

So the kill is behavior-specific, not triggered by the mere presence of 126/127 arms.

## Restoration evidence

```
$ cp pristine.sh mutated.sh; echo "restore_cp_exit=$?"   # prints 0; final audit ran on these bytes
$ sha256sum mutated.sh pristine.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  mutated.sh
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
$ TMPDIR=$PWD/tmp python3 tool.py --runner "$PWD/mutated.sh" > runs/audit-restored.out; echo $? > runs/audit-restored.exit
… TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)   # exit 0
```

Mutant bytes are retained only as `mutant-from-json.sh` (sha `a3ae612e…`), reproducible from the
committed JSON. Head/static/runtime/harness results are in `runs/audit-{pristine,mutated,restored,twin}.out`.

## Command log (exit codes as captured, never `&&`)

| command | exit |
|---|---|
| `git clone -q --no-hardlinks <lane> …/ResidueTallyArmsCoexist/lane` | 0 |
| `git -C lane checkout -q --detach 0b99d48…` | 0 |
| `git -C lane rev-parse HEAD` (prints `0b99d48…`) | 0 |
| `git -C lane show 0b99d48:tools/tally-audit-v2.py > tool.py` | 0 |
| `git -C lane show 0b99d48:tools/mutate-and-run.sh > pristine.sh` | 0 |
| `sha256sum tool.py pristine.sh` (matches pins) | 0 |
| `git -C lane merge-base --is-ancestor c17e593b 0b99d48` | 0 |
| `git -C lane ls-tree 0b99d48 …/HeldOutTallyArms-02.json` (blob `618c59e1…`) | 0 |
| `diff -u pristine.sh mutated.sh` (expected difference) | 1 |
| `python3 -` JSON-edit replay → `mutant-from-json.sh` | 0 |
| `bash witness.sh <runner> <vector>` ×16 (6 pristine, 6 mutant, 4 twin) | 0 each |
| `python3 tool.py --runner pristine.sh` | 0 |
| `python3 tool.py --runner mutated.sh` | 1 |
| `python3 tool.py --runner mutant-accept-twin.sh` | 0 |
| `python3 analyze.py` | 0 |
| `python3 equiv.py` | 0 |
| `cp pristine.sh mutated.sh` + `sha256sum` | 0 |
| `python3 tool.py --runner mutated.sh` (restored) | 0 |

## Findings for round 35 (measurement-only; tool frozen)

1. **Class closed at the pin.** TallyArms-02 coexistence is killed by `7b11ba25…` through the
   co-occurrence sweep; a surviving-mutant Hold is not warranted for this class. No tool edit is
   proposed and none was made.
2. **Scope note for the Hold text.** The kill does not require both 126 and 127 in one vector:
   720 of 792 mismatches pair one of them with an earlier setup-class status (or a second copy of
   itself) because `nsetup=1` resets the count rather than adding to it. Pruning only one of the
   two statuses from `CO` would still leave killers (`[setup,126]`, `[126,126]`); removing both
   would not (`CO` line 407). [INFERENCE from the measured breakdown, not separately run.]
3. **Sealed-set coverage.** No committed sealed copy exercises 126/127 in the tally; this class is
   covered only by the tool's generated sweep, so a counter replay over sealed copies alone does
   not demonstrate it.

## Bounds compliance

- All work in `/fast/scratch/hyaku/tameshi-r34-seats/ResidueTallyArmsCoexist/` (clone, byte
  extractions, mutant/twin copies, harnesses, audit `TMPDIR`); lane read-only, no writes to it, no
  `MANIFEST.json`/templates/scripts/`.ufo/state`/watchdog/sibling repos/jj.
- No `git`/`jj` write commands (`clone` and `checkout` target only the seat scratch; `rev-parse`,
  `show`, `log`, `ls-tree`, `merge-base` are reads). No `agent://all`. No model parameter.
- Kill rule not invoked: the counter was never executed (default or otherwise). Only the frozen
  tool module was imported read-only inside scratch for vector-list replay (`analyze.py`,
  `equiv.py`), which is scratch-side analysis of the tool, not a counter run.
- No tool installs or upgrades this seat.

## Pointers

- Mutant edit and class source: `.ufo/evidence/round-32/heldout/HeldOutTallyArms-02.json:1-16` (sha
  `1ab0f644…15f8`); replay byte identity: seat `analyze.py` log / `mutant-from-json.sh`.
- Sweep: `tools/tally-audit-v2.py:372-440` (`check_runtime`), CO tuple `:407`, pair loops `:408-411`;
  oracle `:290-306`; configs `:265`.
- Runner tally: `tools/mutate-and-run.sh:1432-1439`; embedded harness vectors `:2008-2032` and
  guard stress `:2033-2040`.
- Prior survivor at pre-amendment bytes: `.ufo/waves/round-33/w1/ReviewTool.md` CRITICAL 2 and
  residual risk (sha `fcea7ed2…56dc`).
- Residue class as routed: `corpus/lessons/round-34.md:57`; `SCORECARD.md:1666-1668`;
  `LOG.md:1810-1813`.
- Receipt under attack: `.ufo/evidence/round-34/measure/c1-deciding-run.stdout:1` and `.exit` (`0`).

Report: .ufo/waves/round-34/w1/ResidueTallyArmsCoexist.md
