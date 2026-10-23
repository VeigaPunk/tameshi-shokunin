# PanelSeed2 — round-34 w1 seat report

**Seat:** `PanelSeed2` (role executor, axis: operability)
**Claim under attack:** C1 — operability capability acquisition, `tools/tally-audit-v2.py`,
MEASURED TRUE at measurement revision `c17e593b51802dd4ed568da3265f21c6d00c4273`.
**Verdict:** the C1 public-panel claim REPRODUCES on an independent seed. No finding against any
landed artifact. One panel-composition observation is recorded below (it is a property of the
frozen panel generator, not a tool defect and not a falsification of the deciding run).

Everything below was executed in this seat's scratch dir
`/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed2/`. The lane was cloned read-only and never
written to; the counter was imported **as a module** only — its default-mode CLI was never run.

---

## 1. Setup — exact commands, exit codes, sha256s

All commands run from `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed2/`.

```bash
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed2                      # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin lane                        # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane rev-parse HEAD
#  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7   (== the dispatch lane tip)
```

### Byte pins verified before any run

| artifact | pinned sha256 | observed sha256 | source of observation |
|---|---|---|---|
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | **identical** | `git show 0b99d48:tools/tally-audit-v2.py \| sha256sum`; also `sha256sum lane/tools/tally-audit-v2.py`; also `git show HEAD:tools/tally-audit-v2.py` in the fleet repo |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | **identical** | same three sources; `pristine.sh` sha256 == pin |
| `.ufo/evidence/round-33/c1/c1-measure.py` (counter) | `f6b8868c…a07f28c` | **identical** | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — lane checkout, fleet repo HEAD, and `git show 0b99d48:.ufo/evidence/round-33/c1/c1-measure.py` |
| `.ufo/evidence/round-33/c1/controls-receipt.json` | (not pinned by the brief) | `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa` | lane working tree == `git show 0b99d48:…` |

The three pinned bytes are also identical at the **deciding revision** `c17e593b` itself
(`git show c17e593b:tools/tally-audit-v2.py` → `7b11ba25…8d10`;
`git show c17e593b:tools/mutate-and-run.sh` → `a7d3f2dd…2eb9`;
`git show c17e593b:.ufo/evidence/round-33/c1/c1-measure.py` → `f6b8868c…a07f28c`),
so the tool/runner/counter under test are the exact bytes the deciding run consumed.

The tool was also exercised from the lane checkout copy
(`lane/tools/tally-audit-v2.py`, same sha) and produced identical verdicts, so nothing depends on
the extraction step.

**Lane untouched:** `git -C lane status --porcelain` → empty output, exit 0, after every run in
this report. `git -C lane rev-parse HEAD` still `0b99d48…`. No git/jj write command was issued
anywhere; no sibling repo, `MANIFEST.json`, `templates/`, `scripts/`, `.ufo/state/`,
`.ufo/watchdog.log`, lane jj state or lane Git index was touched.

---

## 2. The replay

Harness: `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed2/replay.py` (written by this seat).
It **imports** the frozen counter with `importlib.util.spec_from_file_location` and calls only
`public_panel` and `score_tool` / `run_tool_sandboxed` on scratch copies — the counter's
default-mode CLI (`--lane/--rev/--work`) was never invoked (the kill rule).

```bash
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed2
python3 replay.py > replay.stdout 2> replay.stderr; echo $? > replay.exit
#  -> replay.exit = 0
```

* Seed: **`r34seedBB02`** (fixed by the brief), passed to `public_panel(pristine, seed)`.
* Pristine runner bytes: `pristine.sh` (`git show 0b99d48:tools/mutate-and-run.sh`), 106 538 bytes.
* Tool under test: `tool.py` (pinned bytes above).
* Work dir: `…/PanelSeed2/work` (scratch only).

### 2.1 Panel shape (deterministic)

```
panel_total=26 kill=18 accept=8
```

Panel digest (sha256 over label‖set‖body for all 26 copies) =
`a0582a191cc7fbfd8dd1062267716954a3ac8c968c4c51b602621b40bc2b97a6`.
Computed twice in two separate processes (`digest-twice.txt`, exit 0): identical both times —
the panel is a pure function of the seed.

### 2.2 Per-copy outcomes table (26/26 correct, zero misses)

Counter-verdict rule as implemented in `run_tool_sandboxed`/`score_tool`: kill hit ⇔
`rc == 1 and last.startswith('TALLY_AUDIT: FAIL')`; accept hit ⇔
`rc == 0 and last.startswith('TALLY_AUDIT: PASS')`.

| # | label | set | outcome | rc | tool verdict line | hit | elapsed |
|---|---|---|---|---|---|---|---|
| 1 | `pub-T08` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | ✔ | 4.18 s |
| 2 | `pub-N05` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | ✔ | 4.53 s |
| 3 | `pub-H03` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 4.39 s |
| 4 | `pub-H04` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 5.02 s |
| 5 | `pub-H05` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 5.28 s |
| 6 | `pub-N01` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 4.83 s |
| 7 | `pub-N02` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 5.20 s |
| 8 | `pub-N03` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 4.96 s |
| 9 | `pub-D01` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | ✔ | 5.21 s |
| 10 | `pub-gT08(arm=230)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | ✔ | 5.51 s |
| 11 | `pub-gN05(< nlegs + 0)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | ✔ | 4.96 s |
| 12 | `pub-gH03(form=2)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 5.77 s |
| 13 | `pub-gH04(rc=$?)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 6.26 s |
| 14 | `pub-gH05(drop=6,dup=4)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 5.93 s |
| 15 | `pub-gN01(vector=0)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 5.64 s |
| 16 | `pub-gN02(true)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 6.16 s |
| 17 | `pub-gN03(split)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | ✔ | 6.34 s |
| 18 | `pub-gD01(drop=st_tsu,dup=st_citecheck)` | kill | KILL | 1 | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | ✔ | 6.77 s |
| 19 | `pub-B0-pristine` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 6.49 s |
| 20 | `pub-B1-T07` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 6.09 s |
| 21 | `pub-B2-reversed` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 6.63 s |
| 22 | `pub-B3-decoys` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 7.37 s |
| 23 | `pub-B4-cosmetic` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 7.13 s |
| 24 | `pub-B5-renamed` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 6.59 s |
| 25 | `pub-gB6-permuted` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 8.35 s |
| 26 | `pub-gB7-nonce` | accept | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | ✔ | 10.89 s |

Misses: **none** (0 kill misses, 0 accept misses).
Machine-readable copy: `…/PanelSeed2/panel-outcomes.json` (exit 0, written by `replay.py`).

### 2.3 Authoritative aggregate (the counter's own `score_tool`)

```
score_tool_result kill=18/18 accept=8/8
ASSERT kill=18/18 accept=8/8 -> PASS
```

`replay.exit` = **0**. This is the counter's `score_tool` on the same 26 copies and the same
pinned tool — not my own re-implementation of the pass/fail rule.

**Determinism re-run** (fresh work dir `work2`, same seed, same bytes):

```bash
python3 -c "… c1.score_tool('tool.py', cs, '…/work2') …" > rerun.stdout 2> rerun.stderr
# rerun.exit = 0
# RERUN seed=r34seedBB02 kill=18/18 accept=8/8 elapsed=151.22
# RERUN_RESULT=PASS
```

### 2.4 Elapsed time

| measurement | value |
|---|---|
| per-copy detail pass (26 sandboxed tool runs, one per copy) | **156.50 s** |
| `score_tool` aggregate pass (26 sandboxed tool runs) | **213.34 s** |
| combined `replay.py` wall time (both passes) | **369.89 s** |
| independent `score_tool` re-run in a fresh work dir | **151.22 s** |
| per-copy sandboxed run | 4.18 s – 10.89 s (mean ≈ 6.0 s) |
| tool `--selftest` (22 cases, each spawning a nested audit) | 156.50 s |

Machine variance across the two `score_tool` passes (151 s vs 213 s) is host-load noise; the
verdict set is identical.

### 2.5 The tool's own reported check detail

Full stdout of one sandboxed run against the pristine runner (`check-lines.txt`, exit 0):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

`vectors=15158` is **geometry-fixed**, not seed-dependent — confirmed identical on a mutated
copy (`check-detail.txt`, exit 0):

```
=== pub-H04 rc=1
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness FAIL reference cases=9; faults rejected=0/34; accepted: label fail-exits-0 …
TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)
```

(The `harness` check is the one that catches `pub-H04`: the mutated runner's own harness accepts
0 of its 34 known-faulty tally blocks.) A second mutated copy shows the harness check being
*partially* defeated while the tool still fails it
(`pub-gH05(drop=6,dup=4)`: `harness FAIL … faults rejected=32/34; accepted: ignore-st_roundgate
ignore-alone-st_roundgate`) — the tool's verdict is FAIL either way, so the must-kill is met.

---

## 3. Independent corroborations of the frozen artifacts

**3.1 The controls receipt satisfies the counter's own `controls_ok` predicate.**
The predicate in `c1-measure.py:main` is
`receipt.counter_sha256 == sha256(self) and receipt.all_false is True and all(rows.predicate_pass is False)`.
Recomputed in this seat (exit 0):

```
controls_ok_predicate=True (all_false=True rows_ok=True counter_sha_match=True)
control_tools=['CtlDoNothing.py', 'CtlAlwaysPass.py', 'CtlAlwaysFail.py', 'CtlShaOnly.py']
```

All four controls are `predicate_pass=false`; `all_false=true`; the receipt's `counter_sha256`
matches the counter bytes at the dispatch tip. This is the `controls_ok=1(ok)` term of the
deciding receipt, reproduced from bytes rather than read off the receipt line.

**3.2 The deciding-run receipt on disk matches the claim text.**
`.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (and `.exit` = `0`) contains exactly:

```
C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true
```

**3.3 The sandbox boundary the counter builds is real.**
Probed with the counter's own `bwrap_argv` (exit 0):

```
write_usr=DENIED
write_workdir=ALLOWED
net=DENIED
leftover_us_probe=False
```

`/usr` is read-only inside the sandbox, the per-run workdir is writable, the network namespace is
unshared (no egress), and no probe file escaped to the host. `bwrap 0.13.1`, `python3 3.14.8`
(`bwrap --version`, `python3 -V`).

**3.4 The tool's own `--selftest` passes.**
Run from a scratch dir containing the pinned tool beside the pinned runner (the tool resolves the
runner as `HERE/mutate-and-run.sh`; without it the selftest dies with `FileNotFoundError` and
exit 1 — an ergonomics wart, not a defect):

```
CASE pristine PASS (exit 0) … CASE reversed operands PASS (exit 0)
TALLY_AUDIT_V2_SELFTEST: 22/22 pass
```

`selftest2.exit` = 0. All 22 named fault classes are rejected or accepted as designed, including
the round-32 escape classes (`dup-drop operand`, `nlegs wrong`, `head masked`, `status 4 passes`,
`guard undercount only`, `in-block 7-bit mask`, `aux wrapper loop`, `aux pre-count loop`,
`second extraction line`, `reversed operands`).

---

## 4. Observation (not a falsification) — panel composition: duplicate kill mutants

**Observation.** The frozen counter's public-panel generator (`v1.generated_kill` +
`v1.frozen_kill` in `.ufo/evidence/round-32/c1-measure.py`) can emit a *generated* kill mutant
whose body is **byte-identical** to a *frozen* kill mutant. The tool still kills every copy it is
handed, so the C1 verdict is unaffected; the observation is about how much distinct coverage
"18/18" denotes.

**The invariant to state** (it is a range, not a fixed number — the count moves with the seed):

> The public panel is **18 kill copies but 14–17 distinct kill mutants** (seed-dependent); the
> **accept set is always 8/8 distinct**.

Across the eight distinct seeds measured by the two seats of this wave (`r34seedBB02`,
`a1b2c3d4e5f60718`, `1a2b3c4d5e6f7081`, `0011223344556677`, `8899aabbccddeeff`,
`685f63bd25263908` = deciding-run seed, `a7acbc0ec97d2710` = controls-receipt seed) the
distinct-kill-body count spans **14–17**: deciding seed 14, controls seed 15, 15 / 16 / 16 / 17
on the sibling's four seeds, 17 on this seat's seed. No single fixed number applies — a wave
that cites one seed's count would over- or under-state the coverage.

Measured (sha256 of each copy body; exit 0 for all three seeds):

| seed | kill copies | **distinct kill bodies** | colliding label pairs |
|---|---|---|---|
| `r34seedBB02` (this seat) | 18 | **17** | `pub-H04` ≡ `pub-gH04(rc=$?)` |
| `685f63bd25263908` (deciding run's seed) | 18 | **14** | `pub-T08`≡`pub-gT08(arm=4)`, `pub-N05`≡`pub-gN05(< nlegs)`, `pub-H04`≡`pub-gH04(rc=$?)`, `pub-N03`≡`pub-gN03(or)` |
| `a7acbc0ec97d2710` (controls receipt's seed) | 18 | **15** | `pub-N05`≡`pub-gN05(< nlegs)`, `pub-H04`≡`pub-gH04(rc=$?)`, `pub-N01`≡`pub-gN01(vector=2)` |

Accept sets are 8/8 distinct at every seed.

Direct confirmation that the collision is byte equality, not just similar structure
(`difflib` over the two full bodies, exit 0):

```
H04_lines=2081 gH04_lines=2081 identical=True
diff_lines=0
```

**Reproducing command** (run from `…/PanelSeed2/`, counter imported as a module, lane untouched):

```bash
python3 -c "
import importlib.util, hashlib
spec=importlib.util.spec_from_file_location('c1r33','lane/.ufo/evidence/round-33/c1/c1-measure.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
p=open('pristine.sh','rb').read()
for seed in ['r34seedBB02','685f63bd25263908','a7acbc0ec97d2710']:
    cs=c1.public_panel(p,seed)
    for s in ('kill','accept'):
        sub=[(l,b) for l,ss,b in cs if ss==s]
        d={}
        for l,b in sub: d.setdefault(hashlib.sha256(b).hexdigest(),[]).append(l)
        print(seed,s,len(sub),len(d),[v for v in d.values() if len(v)>1])
"
# exit 0
```

**Why it is not a falsification.** The tool kills every copy, including both members of each
colliding pair (rows 4 and 13 above are the same bytes and both score KILL). The deciding run's
`v1_kill=18/18` claim is literally true of the 18 copies it scored. What changes is the
*interpretation*: "18/18 kill" is 18 copies but 14–17 distinct kill mutants, so the public
panel's distinct-kill coverage is narrower than the copy count suggests. The **sealed held-out
set** (8 must-kill + 6 must-accept, authored after the counter freeze) is the arm the deciding
run leans on for independent coverage; this seat did not touch it — it stays sealed.

**Suggested disposition for the wave (not mine to execute):** record as a Holds item for a
future counter amendment — e.g. have `public_panel` assert that generated mutants are
distinct from the frozen ones (or dedupe), and report distinct-mutant counts alongside the
copy counts in the receipt. Nothing in the landed C1 claim needs amending to stand.

**Independent corroboration (cross-seat).** The sibling seat `LabratPanelReplay` (report
`.ufo/waves/round-34/w1/LabratPanelReplay.md`, 285 lines, sha256
`35d5d41d578c4733bce5db751147d861dfd975c43e2a80563084a4c9ceecc252` — that seat's FROZEN report;
it deliberately records no hash of this report, so the two citations cannot invalidate each
other) reproduced this observation
independently on four
further fixed seeds — distinct kill bodies 15 / 16 / 16 / 17 for seeds `a1b2c3d4e5f60718` /
`1a2b3c4d5e6f7081` / `0011223344556677` / `8899aabbccddeeff` — and confirmed the same 14/18 at
the deciding-run seed `685f63bd25263908` and 15/18 at the controls seed `a7acbc0ec97d2710`, with
accept sets always 8/8 distinct. Their reproduction script is
`/fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/panelcomp.py` (exit 0). Eight seeds
across two seats place the effective distinct-kill coverage of the public panel at 14–17, moving
with the seed, and confirm it is a property of the frozen generator rather than of any one
seed. That seat also wrote the observation up explicitly as a panel-composition observation and
**not** a finding against the C1 claim — consistent with this seat's §4.

Two further independent confirmations from the same sibling, matching this seat's own
measurements: `vectors=15158` on 104/104 copies across their four seeds (this seat measured the
same N on both a pristine and a mutated copy), and a geometry-only derivation of that number
(7561 vectors/config × 2 configs = 15122, + 36 stress vectors = 15158) that matches the tool's
own reported count exactly — i.e. the runtime sweep size is a property of the audit geometry,
not of the seed.

---

## 5. Scope, bounds and tool record

* Writes: only `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed2/**` (scratch) and this one
  report file `.ufo/waves/round-34/w1/PanelSeed2.md`. The lane clone was never written to
  (`git -C lane status --porcelain` empty after all runs). No git/jj write command anywhere.
* The sealed set `.ufo/evidence/round-33/heldout/` was **not** read, scored, or modified.
* The counter's default-mode CLI was **never** run (kill rule respected); it was imported as a
  module and only `public_panel`, `run_tool_sandboxed` and `score_tool` were called, all on
  scratch copies under this seat's work dir.
* No frozen artifact was edited: tool `7b11ba25…8d10`, runner `a7d3f2dd…2eb9`, counter
  `f6b8868c…a07f28c`, controls receipt `f1e62421…de3aa` — all byte-identical before and after.
* **Tool installs: none.** `bubblewrap 0.13.1` and `python3 3.14.8` were already present on the
  host and are the only tools needed; no package was installed or upgraded, so the
  operator tool-channel directive (RULES.md, read at `/home/vgpnk/.omp/agent/RULES.md`) required
  no action and the pacman pause was not touched. Nothing was installed via `uv tool`/`npx`/
  `~/.local/bin`.
* I dispatched no subagent; this is a leaf seat with a single (unused) labrat allowance.

## 6. Bottom line

C1's public-panel claim reproduces independently at seed `r34seedBB02`: **kill 18/18,
accept 8/8, zero misses**, via the counter's own `score_tool` (exit 0), re-confirmed by an
identical re-run in a fresh work dir, with the tool, runner and counter all verified
byte-identical to the dispatch-tip pins. The tool's own `--selftest` passes 22/22 and the
counter's sandbox boundary is verified effective. The deciding run stands. The single
observation recorded (§4) concerns how many *distinct* kill mutants "18/18" denotes, is
reproducible, and does not falsify any landed artifact.
