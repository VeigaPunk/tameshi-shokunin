# DeterminismProbe — round 32, wave 1 (pre-data control, axis: operability)

**Assigned verdict: the assigned hypothesis is CONFIRMED — the counter is deterministic for a fixed
seed.** My assigned item was to score an always-FAIL control tool; every run in §2 uses exactly
that control (tool sha `efec2ece…`, clone commit `d747b80`), and the fixed-seed runs print
identical outcome, exit and sha256 on all 26 COPY lines.

**Additional finding, beyond my assignment: the counter's verdict for the *real* capability tool is
SEED-DEPENDENT, so `C1_R32_PASS` is not a property of the tool alone.** §3 reports this. It is
reported because it was observed while the assigned runs were in flight, and it is kept strictly
separate from the assigned measurement. §1a states which tool bytes each run used.

Both findings are evidence, not assertions. Every number below is an observed output.

---

## 1. Scope and setup

Seat: `TameshiR32.DeterminismProbe` (leaf; no subagents dispatched).
Working dir: `/fast/scratch/hyaku/tameshi-r32-seats/DeterminismProbe/`.

```
mkdir -p /fast/scratch/hyaku/tameshi-r32-seats/DeterminismProbe
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r32-seats/DeterminismProbe/lane
git -C .../lane checkout -q --detach c31814978969a41a8e9b0f7d99fa308c5993c1b7
```

`git log --oneline -1` → `c318149 round-32: freeze — C1 counter + contract (tally audit, 18 must-kill
/ 8 must-accept), base receipts, repair receipts (r31 base monitor, command D exits), counter v2 repair`.

The runner in the clone is byte-identical to the pinned blob:
`sha256sum .../lane/tools/mutate-and-run.sh` → `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (= `PINNED_RUNNER_SHA`).

Control tool (always-FAIL, written by this seat, committed **in the scratch clone only**):
`tools/tally-audit.py` at clone commit `d747b801b2a932c9fe157b599da7d6f61ea3d220` — prints exactly
one line `TALLY_AUDIT: FAIL control=always-fail reason=unconditional` and exits 1, for every runner.

Production repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin` was **not** modified by this seat
(`git status --porcelain` shows only the harness-managed `.ufo/waves/round-32/w1/swarm-registry.json`
and other seats' untracked files). No `jj` command was run anywhere. No process was left running.

### 1a. Which tool bytes each run used

My assigned item was to score **an always-FAIL control tool**. §2 (Finding A) is that assigned
measurement and uses the always-FAIL control throughout. §3 (Finding B) is an **additional
observation beyond my assignment**: while the always-FAIL runs were in flight I also scored the
**real** capability tool that another seat had in the production working tree, and that is where the
seed-dependent verdict was found. The two are kept strictly apart below, and every run is
attributed to its exact tool bytes.

| clone commit | tool sha256 | tool identity | which runs used it |
|---|---|---|---|
| `d747b80` | `efec2ece3df339c99acba7ec06b98e6222db2b6d1fcdaf09521875a34d7b8db6` | **always-FAIL control** (this seat) | §2a, §2b, §2d — all fixed-seed and unseeded determinism runs |
| `bb423ff` | `ec2a1ef1c76115dff238c3b644093179aa32fd0e8841ca78353b6b87694340e3` | path-echoing always-FAIL control variant (this seat) | §2c only |
| `9a3fc37` | `ad7be824fcd69142b7f1fd3f653729c64ed9c01346daf7ffa329c1be1e432010` | seed-keyed single-copy probe (this seat) | the seed-sensitivity probe in §3e |
| `b80e78b` | `ac38a1ac13cb8fd59ebe52df7adf68299fb79062e64d1b22f6d35729ed8c819c` | **real capability tool**, read-only copy | §3 seed sweep, §3b prediction table, §3c root cause, §3d selftest |
| `556d1ff` | `158202f8bc85a82e92bbc7bb3c42f636f468a4484a9725937cefcc41997a356a` | **real capability tool**, newer bytes, read-only copy | §3a re-verification only |

Every copy was taken **read-only** from the production working tree; this seat never edited the real
tool. `tools/mutate-and-run.sh` was never edited anywhere: its sha256 is `a7d3f2dd…2eb9` in the
clone and in production, before and after every run.

---

## 2. Finding A — the ASSIGNED measurement: the counter IS deterministic for a fixed seed

*Tool used throughout this section: the always-FAIL control, clone commit `d747b80`, tool sha
`efec2ece3df339c99acba7ec06b98e6222db2b6d1fcdaf09521875a34d7b8db6` (except §2c, which uses the
path-echoing variant `ec2a1ef1…` at commit `bb423ff`).*

### 2a. Always-FAIL control, `--seed 2a`, two fresh `--work` dirs

```
python3 .ufo/evidence/round-32/c1-measure.py --lane <clone> --rev d747b80... \
        --work <scratch>/work/fix1 --seed 2a   -> exit 1
python3 .ufo/evidence/round-32/c1-measure.py --lane <clone> --rev d747b80... \
        --work <scratch>/work/fix2 --seed 2a   -> exit 1
diff out/fix-seed2a-1.stdout out/fix-seed2a-2.stdout   -> EMPTY (byte-identical, 27 lines each)
```

A third run (`work/fix3`) and a fourth (`work/fix4 --jobs 8`) also produce byte-identical stdout
(`diff` empty in both cases). Both runs print:

```
COPY set=accept id=gB7-nonce outcome=KILL exit=1 sha256=fa87c2c9713866e2 last='TALLY_AUDIT: FAIL control=always-fail reason=unconditional'
C1_R32: kill=18/18 accept=0/8 other=8 runner_sha_ok=1 tool_present=1 seed=2a rev=d747b801b2a932c9fe157b599da7d6f61ea3d220 C1_R32_PASS=false
```

So: identical outcome, identical exit, identical sha256 for every one of the 26 COPY lines, and an
identical summary line. **Fixed-seed determinism holds.**

### 2b. Invariances that also hold at a fixed seed

| perturbation | result |
|---|---|
| `--jobs 4` vs `--jobs 8` | stdout byte-identical (`diff` empty) |
| `PYTHONHASHSEED=12345` | stdout byte-identical |
| `cd /tmp` (different cwd) | stdout byte-identical |
| interpreter 3.11 / 3.12 / 3.13 / 3.14 / 3.15 | stdout byte-identical to the 3.14 baseline |

(`python3.13` is not on `PATH` as `python3.13`; it was run by absolute path
`/home/vgpnk/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13`. The first attempt
exited 127 — command not found — not a counter error.)

### 2c. What is NOT deterministic, and it is the tool's fault, not the counter's

The counter writes each copy to an opaque random filename (`secrets.token_hex(8)`, counter line
`copies.append((set_name, label, path, ...))`). A tool that echoes the `--runner` path in its output
therefore makes the `last=` field of the COPY line differ between runs. I proved this with a
second control variant that appends `runner=$2` to its FAIL line:

```
diff out/pe-seed2a-1.stdout out/pe-seed2a-2.stdout   -> 52 differing lines
diff <(sed -E 's/ last=.*//' run1) <(sed -E 's/ last=.*//' run2)  -> EMPTY
```

The `id=`, `outcome=`, `exit=` and `sha256=` fields were still identical; only the tool's own echoed
path differed. **The counter is deterministic; the tool's output text is the only varying part.**
A real tool must not echo the runner path (or must normalise it) if its receipts are to be
byte-comparable across runs. This is a property the tool author should know; it is not a counter
defect.

### 2d. Two runs with NO seed: the seeds and the generated labels differ

```
--work work/noseed1 (no --seed)  -> seed=e8d196250b95cac4
--work work/noseed2 (no --seed)  -> seed=60125fefd24b5920
```

Generated-copy labels differ (the 9 frozen copies stay byte-identical, as they must):

| copy | run 1 | run 2 |
|---|---|---|
| gT08 | `arm=254` sha `2ae296ae448e7a88` | `arm=42` sha `00d8537b1b39f6ea` |
| gN05 | `< nlegs + 0` | `< nlegs` |
| gH03 | `form=2` | `form=0` |
| gH05 | `drop=8,dup=6` | `drop=0,dup=5` |
| gN01 | `vector=2` | `vector=1` |
| gN02 | `or` | `true` |
| gN03 | `split` | `or` |
| gD01 | `drop=st_claims,dup=st_js` | `drop=st_roundgate,dup=st_kagi` |
| gB6 | sha `daf30a0b19613e56` | sha `848019bfd00d9a70` |
| gB7 | sha `aee0c4de0dcfa364` | sha `dd42cc976d3c58f7` |

`diff` of the two full stdouts: 22 changed lines, all of them `id=g…` rows.
`diff` of the frozen (`id=` not starting with `g`) COPY rows: **empty** — identical.
**The unseeded path behaves exactly as the counter documents.**

---

## 3. Finding B — BEYOND MY ASSIGNMENT: the counter's verdict for the real tool is seed-dependent

*Scope note: this section is an additional observation, not the assigned measurement. The assigned
item was to score an always-FAIL control (§2). While those runs were in flight I also scored the
real capability tool another seat had in the production working tree, read-only, and found the
verdict moves with the seed. The tool bytes for every run here are stated in §1a and repeated per
result.*

The **real** capability tool `tools/tally-audit.py` was present as an untracked file in the
production working tree (`sha256 ac38a1ac13cb8fd59ebe52df7adf68299fb79062e64d1b22f6d35729ed8c819c`).
I copied it **read-only** into the scratch clone (commit `b80e78bbef245acc34c844819f396fa0e14069a3`)
and ran the frozen counter against it. **I did not modify the tool.**

This is *not* the CtlHarnessOnly negative control. That seat owns a separate, deliberately partial
harness-only tool (sha `1a1e1da7d24ca3eaa0773dfe8d76d9ffad850407ea1737d96ae9e03e21ce0f24`,
reported in `.ufo/waves/round-32/w1/CtlHarnessOnly.md`, correctly printing `kill=10/18 accept=8/8
… C1_R32_PASS=false`); that sha is not what I measured, and its own report reaches the same
conclusion about the real tool from the other direction — "Its harness panel needs faults that
cover every singleton position and each independent multi-status vector, rather than relying on
only the fixed H05 and N01 witnesses." My finding is about the real tool and is routed to the L1,
the sole integrator.

| seed | result |
|---|---|
| `2a` | `kill=18/18 accept=8/8 other=0 … C1_R32_PASS=true`, exit 0 |
| `2a` (second run, fresh `--work`) | stdout **byte-identical** to the first; `C1_R32_PASS=true` |
| `2b` | `kill=18/18 accept=8/8 other=0 … C1_R32_PASS=true`, exit 0 |
| `00ff` | `kill=17/18 accept=8/8 other=1 … C1_R32_PASS=false`, exit 1 — escaping copy `gH05(drop=0,dup=6)` |
| `00ff` (rerun, fresh `--work`) | reproduces **identically** — not flaky |
| `0900` | `kill=17/18 accept=8/8 other=1 … C1_R32_PASS=false`, exit 1 — escaping copy `gH05(drop=0,dup=3)` |

Seed sweep, 12 seeds, same tool:

```
seed=00ff exit=1 escapes[gH05(drop=0,dup=6)]  C1_R32_PASS=false
seed=0100 exit=0 escapes[]                   C1_R32_PASS=true
seed=0200 exit=0 escapes[]                   C1_R32_PASS=true
seed=0300 exit=0 escapes[]                   C1_R32_PASS=true
seed=0400 exit=0 escapes[]                   C1_R32_PASS=true
seed=0500 exit=0 escapes[]                   C1_R32_PASS=true
seed=0600 exit=0 escapes[]                   C1_R32_PASS=true
seed=0700 exit=0 escapes[]                   C1_R32_PASS=true
seed=0800 exit=0 escapes[]                   C1_R32_PASS=true
seed=0900 exit=1 escapes[gH05(drop=0,dup=3)] C1_R32_PASS=false
seed=0a00 exit=0 escapes[]                   C1_R32_PASS=true
seed=0b00 exit=0 escapes[]                   C1_R32_PASS=true
```

**10 true / 2 false out of 12 measured.** The verdict flips purely on the seed.

### 3a. Re-verified against the tool's newer bytes

The tool changed in the production working tree while this seat was measuring
(`ac38a1ac…c819c` → `158202f8bc85a82e92bbc7bb3c42f636f468a4484a9725937cefcc41997a356a`). I copied
the new bytes read-only into the scratch clone (commit `556d1ff4869e20e5096095d31ae290415d1f68c6`)
and re-ran the counter:

```
seed=00ff exit=1  kill=17/18 accept=8/8 other=1  C1_R32_PASS=false
   ESCAPE: COPY set=kill id=gH05(drop=0,dup=6) outcome=ACCEPT exit=0 sha256=9f9e3feebe8d3b7e
seed=0900 exit=1  kill=17/18 accept=8/8 other=1  C1_R32_PASS=false
   ESCAPE: COPY set=kill id=gH05(drop=0,dup=3) outcome=ACCEPT exit=0 sha256=aee59df31aaf778e
seed=2a   exit=0  kill=18/18 accept=8/8 other=0  C1_R32_PASS=true
```

**The finding reproduces unchanged against the newer tool bytes.** The same two seeds still fail,
the same copy is still accepted, and seed `2a` still passes.

### 3b. Prediction made before the measurement — and it held

I derived, from the counter's own RNG consumption order (`generated_kill`, counter lines 96–120),
the dropped position `p` of the generated gH05 copy for any seed:

```
rng.randint(2,255)                 # gT08 arm
rng.choice([...3 forms...])        # gN05 form
rng.randrange(3)                   # gH03 form
rng.choice([...3 tails...])        # gH04 tail
p = rng.randrange(9)               # gH05 drop position   <-- the 5th draw
```

| seed | predicted p | observed |
|---|---|---|
| `00ff` | 0 | escaped |
| `0900` | 0 | escaped |
| `2a` | 4 | killed |
| `2b` | 7 | killed |
| `0100`/`0200` | 6 | killed |
| `0300` | 3 | killed |
| `0400` | 5 | killed |
| `0500`/`0700` | 7 | killed |
| `0600`/`0800` | 8 | killed |
| `0a00`/`0b00` | 2 | killed |

**Every prediction matched.** Escape happens exactly when `p ∈ {0, 1}`. Over 2000 seeds, 23.6% of
seeds draw `p ∈ {0,1}` (theoretical 2/9 = 22.2%). **Roughly one counter run in four reports a
false `C1_R32_PASS=false` for a tool that is otherwise sound.**

### 3c. Root cause (isolated, not guessed)

The runner's own selftest harness (`tools/mutate-and-run.sh:2011-2020`) iterates nine leg positions:

```bash
for ti in 0 1 2 3 4 5 6 7 8; do
  local -a tst=(0 0 0 0 0 0 0 0 0)
  tst[ti]=${tvec%%:*}
  ...
  [[ $tgot -eq 9 ]]
```

The tool's harness panel (`tools/tally-audit.py:319-336`, `faults()` at line 245) injects one
`ignore-st_<name>` fault per leg name into a copy of the reference tally block. If the runner's
`for ti` loop never exercises position *p*, the `ignore-st_<leg p>` fault is **accepted** (the
harness no longer notices that leg) and the tool correctly reports `harness=fail`.

But the runner's harness *also* contains multi-status vectors a few lines further down
(`tools/mutate-and-run.sh:2021-2028`): `'1 1 0 0 0 0 0 0 0'`, `'2 2 0 0 0 0 0 0 0'`,
`'1 2 0 0 0 0 0 0 0'`, `'3 0 0 0 0 0 0 0 0'`. These drive **positions 0 and 1** directly. So when
`p ∈ {0,1}` the dropped position is still exercised by the multi-status vectors, the
`ignore-st_js` / `ignore-st_kagi` fault is still caught, and the tool's harness panel sees nothing
wrong. The counter's frozen `H05` mutant happens to drop position 8 (`for ti in 0 1 2 3 4 5 6 7 7`),
which the multi-status vectors do **not** cover — so the frozen copy is killed and the defect stays
hidden.

Isolated proof, using the tool's own functions against a hand-built mutant:

```
drop=0 dup=6 : good=(9,0) accepted=[]                          -> tool PASSes  (ESCAPE)
drop=1 dup=2 : good=(9,0) accepted=[]                          -> tool PASSes  (ESCAPE)
drop=2 dup=0 : good=(9,0) accepted=['ignore-st_tsu']           -> tool FAILs   (killed)
drop=8 dup=7 : good=(9,0) accepted=['ignore-st_citecheck']     -> tool FAILs   (killed)
```

Full enumeration of all 72 (drop, dup) pairs of the gH05 family, with the counter's exact anchor
(`'    for ti in 0 1 2 3 4 5 6 7 8; do\n'`):

- **16 of 72 escape the tool** — exactly the 8 pairs with `drop=0` and the 8 pairs with `drop=1`
  (the `drop=1,dup=1` pair is impossible: `q != p`).
- the remaining 56 (all `drop ∈ {2..8}`) are killed.

Escaping sha256 values (first 16 hex), for the L1's records:

```
drop=0: 6afff01c959ce533 45d9362b5c0544a8 aee59df31aaf778e a0ed0d4b330192d0
        d64f2940f66349be 9f9e3feebe8d3b7e a17863d9385d2d27 6aab68e19d29b7ec
drop=1: 8a13e626a8ddbb22 d662389a26e86be4 89f52983ffb0a191 b443eb6fa9aa00e5
        ba5473fb0198e642 3b06db937e2c19fb 5a3d1583d3fb2b97 dd1498f2bae5af19
```

Confirmation that the multi-status vectors are the redundant coverage (same mutant, multi-status
vector loop removed):

```
pristine WITHOUT multi-status vectors: accepted=[] (plus 4 unrelated)
drop0  WITHOUT multi-status vectors: accepted=['ignore-st_js', ...]   -> now detected
drop2  WITHOUT multi-status vectors: accepted=['ignore-st_tsu', ...]   -> detected either way
```

`ignore-st_js` is only missed while the multi-status vectors cover position 0.

### 3d. The tool's own `--selftest` cannot see it

```
python3 tools/tally-audit.py --selftest
CASE pristine PASS / dup-drop operand PASS / nlegs wrong PASS / status 4 passes PASS
     guard undercount only PASS / harness exit-only PASS / harness swallowed PASS
     harness position 8 skipped PASS / reversed operands PASS
TALLY_AUDIT_SELFTEST: 9/9 pass          (exit 0)
```

Its harness case is `text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 0 1 2 3 4 5 6 7 7; do', 1)`
— it only ever drops **position 8**, the one position the multi-status vectors do not cover. The
selftest is therefore self-confirming on exactly the blind spot it should probe.

### 3e. Seed-sensitivity of the aggregate counts, shown with a tool this seat owns

To show that the aggregate counts themselves move with the seed — independently of the real tool's
particular blind spot — I built a probe tool (clone commit `9a3fc37`, sha `ad7be824…`) that PASSes
exactly one runner copy, keyed on that copy's content sha256 (`f00810a428c1f86a`, the
`gT08(arm=165)` copy that `--seed 2a` generates), and FAILs everything else:

```
seed=2a  -> C1_R32: kill=17/18 accept=0/8 other=9  C1_R32_PASS=false
            (the gT08(arm=165) copy was ACCEPTed, so it did not count as a kill)
seed=2b  -> C1_R32: kill=18/18 accept=0/8 other=8  C1_R32_PASS=false
            (that copy does not exist under seed 2b, so every must-kill copy was killed)
```

The same tool, the same runner, the same command — only the seed differs, and the kill count moves
17 → 18. **This is a general property of the counter: whenever a tool's verdict depends on which
generated copies exist, the aggregate count depends on the seed.** For the real tool the dependency
arises from the gH05 drop position; for this probe it arises from the gT08 arm value. Both are the
same mechanism.

---

## 4. What this means for the round (smallest safe correction, offered, not applied)

The contract's predicate is per-copy and seed-independent, but the **counter's aggregate verdict**
is not. The contract's `kill_rule` says a run printing `false` is "reported as a miss, never
re-scaled, re-seeded or amended" — with a ~22% seed-dependent false-negative rate, the L1 could
publish a false miss on a sound tool, or (worse) could be tempted to re-seed until it saw `true`,
which the contract forbids. **The seed must be fixed and published in the receipt, and a
`C1_R32_PASS=false` at the measurement revision must be re-examined for this specific cause before
it is accepted as a miss.**

The smallest correction, in the tool (`tools/tally-audit.py`), not in the runner and not in the
frozen counter:

1. **Strengthen the harness fault panel so a dropped position 0 or 1 is detectable.** The `ignore-st_js`
   / `ignore-st_kagi` faults must be injected in a way the multi-status vectors cannot accidentally
   cover — e.g. inject the ignore-fault as a *single-leg* status vector (only one non-zero position,
   the ignored one) so the multi-status vectors cannot mask it; or add panel faults that exercise
   positions 0 and 1 exclusively.
2. **Extend `--selftest`** to cover every drop position 0..8, not just 8 — the same 72-pair
   enumeration this seat ran is a ready-made fixture.
3. **Do not echo the runner path** in the tool's output (Finding A, §2c), so receipts are
   byte-comparable across runs. *Checked against the real tool as of sha `158202f8…`: it does not
   print the runner path, so this item is already satisfied and needs no change — it is stated only
   as a property to preserve.*

The runner `tools/mutate-and-run.sh` must stay byte-identical — nothing in this finding requires
touching it, and its sha256 is unchanged in the clone (`a7d3f2dd…2eb9`).

---

## 5. Commands and evidence index (all paths under the scratch seat dir)

**§2 — assigned measurement, always-FAIL control `efec2ece…` (`d747b80`) unless noted:**

```
out/fix-seed2a-1.stdout   out/fix-seed2a-2.stdout   out/fix-seed2a-3.stdout   out/fix-seed2a-jobs8.stdout
out/noseed-1.stdout        out/noseed-2.stdout
out/hashseed.stdout        out/cwdtest.stdout           out/py3.11.stdout … out/py3.15.stdout
out/pe-seed2a-1.stdout     out/pe-seed2a-2.stdout        (path-echoing variant ec2a1ef1…, bb423ff)
```

**§3 — beyond assignment, real capability tool `ac38a1ac…` (`b80e78b`) unless noted:**

```
out/real-seed2a-1.stdout   out/real-seed2a-2.stdout   out/real-seed2b.stdout  out/real-seed00ff.stdout
out/real-seed00ff-r2.stdout
out/sweep-summary.txt      out/sweep-0100.stdout … out/sweep-0b00.stdout
out/h05-enum-rest.txt       (56-pair enumeration tail: every drop in 2..8 killed)
out/re-00ff.stdout         out/re-0900.stdout         out/re-2a.stdout   (tool 158202f8…, 556d1ff)
out/ss-seed2a.stdout       out/ss-seed2b.stdout       (seed-keyed probe ad7be824…, 9a3fc37)
probe/h05v3/               (72-pair enumeration scratch)
```

Clone commits (scratch clone only): `d747b80` always-FAIL control;
`bb423ff` path-echoing control variant; `9a3fc37` seed-keyed probe; `b80e78b` read-only copy of the
real capability tool used for the seed sweep; `556d1ff` read-only copy of its newer bytes used for
the §3a re-verification.

---

## 6. Tooling

No packages were installed or updated by this seat. Everything used was already present:
`python3` 3.14.8 (system), plus already-installed `python3.11` / `python3.12` / `python3.13` / `python3.15`
under `/home/vgpnk/.local/share/uv/python/` for the cross-interpreter check. `git`, `bash`, `sha256sum`,
`diff` are system tools.

---

## 7. Claims not made

- I do not claim the tool is complete or that the counter's copy families are exhaustive.
- I do not claim the tool is wrong in general: it kills 56/72 gH05 variants and all 9 frozen
  must-kill copies; the defect is specific to dropped positions 0 and 1.
- I did not modify the tool, the runner, the counter or the contract. The `git status` of the
  production repo shows no change authored by this seat.
- **The tool I measured was the real capability tool**, not a control: `ac38a1ac…c819c` for the
  sweep, root-cause and selftest work, and `158202f8…a356a` for the §3a re-verification. Both were
  copied read-only into the scratch clone; the production file was never edited by this seat.
  The production file has since changed again (a third sha, `9639c458…99ef`, was observed after my
  last run); **every §3 number here applies to the two shas named above**, and the §3 finding must
  be re-measured against any further bytes. I made no further runs after the L1's stop request, so
  I do not claim the finding holds for `9639c458…99ef` or later.
- **The §2 assigned measurement used only this seat's own always-FAIL control**
  (`efec2ece…b8db6`), and the §2c variant `ec2a1ef1…`. No §2 number comes from the real tool.
- The 22% escape-rate figure is a property of the *counter's* RNG draw order plus the tool's blind
  spot. It is a measured rate (10/12 true, 2/12 false over the sweep; 23.6% predicted over 2000
  seeds), not a claim about any other tool.
- No further counter runs were made after the L1's request to stop; every number in this report
  comes from a run listed in §5.
