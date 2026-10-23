# LabratPanelReplay (tameshi r34 w1)

Observed 2026-10-23 (UTC). No packages installed; no tool upgrades needed. The seat ran only
the **public** panel (counter `public_panel` + `score_tool`) on **scratch copies**. The sealed
held-out set (`.ufo/evidence/round-33/heldout/`) was never read, replayed, or copied. The
counter's default mode was never invoked (kill rule respected) — the counter was `import`ed as
a module and only `public_panel`, `score_tool`, `run_tool_sandboxed` were called.

## Verdict

**The public panel holds on all four fixed seeds. Zero misses.**

| Seed | Panel | `score_tool` kill | `score_tool` accept | Wall | Misses |
|---|---|---|---|---|---|
| `a1b2c3d4e5f60718` | 26 (18 kill + 8 accept) | 18/18 | 8/8 | 216.6 s | 0 |
| `1a2b3c4d5e6f7081` | 26 (18 kill + 8 accept) | 18/18 | 8/8 | 184.7 s | 0 |
| `0011223344556677` | 26 (18 kill + 8 accept) | 18/18 | 8/8 | 162.2 s | 0 |
| `8899aabbccddeeff` | 26 (18 kill + 8 accept) | 18/18 | 8/8 | 233.5 s | 0 |

No copy and no seed produced a miss, so there is no copy/seed pair to name. Every kill copy
exited 1 with a last stdout line `TALLY_AUDIT: FAIL (...)`; every accept copy exited 0 with a
last stdout line `TALLY_AUDIT: PASS (...)`. 104 sandboxed tool runs total (26 copies × 4 seeds),
0 `TALLY_AUDIT: SETUP`, 0 timeouts, 0 non-`TALLY_AUDIT` exits.

**Vector counts the tool reports.** The tool reports `CHECK runtime ... vectors=15158` on
**every** copy of **every** seed — 104/104 — and `mismatched=0` on all 8 accept copies of every
seed. The value is seed-independent and copy-independent: it is fixed by the sweep geometry, not
by the panel. I derived `15158` independently from the tool's own vector construction (no bash
execution), and the derivation matches the tool's report exactly:

- 9 legs, 9 loop operands (`names=9 ops=9`)
- single-status sweep: 256 statuses × 9 positions = 2304 vectors
- count-pair sweep `count_vectors(9)` (failing+setup ≤ 9): 55 vectors
- position-varied mixes: 6 (failing, setup) shapes × 3 placements = 18 vectors
- co-occurrence: 36 unordered position pairs × 12 × 12 ordered status pairs = 5184 vectors
- subtotal 7561 vectors × 2 configs (`CONFIGS`) = 15122
- stress: 9 operands × {dup, drop} × 2 configs = 36
- **total = 15122 + 36 = 15158**

Command: `python3 /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/vecmath.py`
(prints `vectors_per_config=7561 ran=15122 stress=36 total=15158`, exit 0).

Peer seat `PanelSeed2`, on its independent seed `r34seedBB02`, reported the same
`vectors=15158 mismatched=0` — a second, independent confirmation of the number. Its report is
`.ufo/waves/round-34/w1/PanelSeed2.md`; it carries the same collision observation in the same
range form, so either seat's report may be cited for it without double-counting. (No sha256 of
the peer report is recorded here on purpose: the two seats cite each other, and each edit would
invalidate the other's hash. Read the peer file directly.)

## Pins (tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`)

Clone (exit 0):

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
```

`git -C .../lane rev-parse HEAD` → `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
`git -C .../lane status --porcelain` → empty, exit 0 (clone worktree clean).

Pinned bytes extracted with `git -C .../lane show <tip>:tools/...` (both exit 0):

| Artifact | sha256 | pin | match |
|---|---|---|---|
| `tools/tally-audit-v2.py` (scratch `tool.py`) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | `7b11ba25…8d10` | yes |
| `tools/mutate-and-run.sh` (scratch `pristine.sh`) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | `a7d3f2dd…2eb9` | yes |

The same two hashes are on the clone worktree files and on the live lane files
(`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/…`) — four locations, one hash each.

Counter bytes, taken from the tip blob (not the live worktree) and imported from scratch:

| Artifact | sha256 | pin | match |
|---|---|---|---|
| `.ufo/evidence/round-33/c1/c1-measure.py` (amendment 6) | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | `f6b8868c…a07f28c` | yes |
| `.ufo/evidence/round-32/c1/c1-measure.py` (v1 panel generator) | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | (not separately pinned) | — |

The round-33 counter is copied into the scratch tree at
`ctr/.ufo/evidence/round-33/c1/c1-measure.py` with the round-32 sibling at the relative path
the counter's own `V1_PATH` expects, so `import c1r33` resolves v1 by its own frozen relative
path. Hashes re-verified after the copy (identical, above).

Controls receipt `.ufo/evidence/round-33/c1/controls-receipt.json` names
`counter_sha256: f6b8868c…a07f28c` and `runner_sha256: a7d3f2dd…2eb9` — both match the blobs
this seat ran, `all_false: true`, and all four controls carry `predicate_pass: false`.

## The replay

`driver.py` (scratch, `/fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/driver.py`)
imports the frozen counter as a module, builds the panel with the counter's own
`public_panel(pristine, seed)`, and scores it with the counter's own `score_tool`. The four
seeds are fixed literals in the driver: `a1b2c3d4e5f60718`, `1a2b3c4d5e6f7081`,
`0011223344556677`, `8899aabbccddeeff`.

```sh
cd /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay && python3 driver.py > driver.stdout 2>driver.stderr; echo $? > driver.exit
```

- exit: `0` (`driver.exit` = `0`)
- stderr: empty (`driver.stderr` = 0 bytes)
- wall: 797.09 s total across the four seeds
- results: `results.json` (per-copy table, per-copy `CHECK` lines, per-copy rc, last
  `TALLY_AUDIT:` line, per-seed wall time, per-seed `score_tool` aggregate)

The only instrumentation was a wrapper around `subprocess.run` that **records** each sandboxed
tool run's stdout so the per-copy `CHECK` lines and vector counts could be tabulated. It
returns the original `CompletedProcess` unchanged, so `score_tool`'s own verdicts are the
authoritative aggregate — the driver's per-copy table is derived from the same captured stdout.

### Panel composition (per seed)

Each seed yields exactly 26 copies: 18 kill + 8 accept. The panels differ across seeds:
4 distinct panel sha256 over the 4 seeds (`730ca684…`, `460ca601…`, `83bb0827…`, `cb1b252e…`),
with 5–8 differing copy labels per seed pair. The seeds therefore exercise genuinely different
mutant instances, not the same panel four times.

### Per-copy outcome, seed `a1b2c3d4e5f60718`

All 26 copies, with the tool's own reported runtime vector count and mismatch count:

| Copy | set | rc | verdict | vectors | mismatched | last `TALLY_AUDIT:` line |
|---|---|---|---|---|---|---|
| pub-T08 | kill | 1 | KILL | 15158 | 1674 | `FAIL (head=pass static=pass runtime=fail harness=pass)` |
| pub-N05 | kill | 1 | KILL | 15158 | 18 | `FAIL (head=pass static=pass runtime=fail harness=pass)` |
| pub-H03 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=pass runtime=pass harness=fail)` |
| pub-H04 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=pass runtime=pass harness=fail)` |
| pub-H05 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=pass runtime=pass harness=fail)` |
| pub-N01 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=pass runtime=pass harness=fail)` |
| pub-N02 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=pass runtime=pass harness=fail)` |
| pub-N03 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=pass runtime=pass harness=fail)` |
| pub-D01 | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=fail runtime=pass harness=pass)` |
| pub-gT08(arm=74) | kill | 1 | KILL | 15158 | 18 | `FAIL (… runtime=fail …)` |
| pub-gN05(< nlegs) | kill | 1 | KILL | 15158 | 18 | `FAIL (… runtime=fail …)` |
| pub-gH03(form=0) | kill | 1 | KILL | 15158 | 0 | `FAIL (… harness=fail)` |
| pub-gH04(:) | kill | 1 | KILL | 15158 | 0 | `FAIL (… harness=fail)` |
| pub-gH05(drop=2,dup=7) | kill | 1 | KILL | 15158 | 0 | `FAIL (… harness=fail)` |
| pub-gN01(vector=1) | kill | 1 | KILL | 15158 | 0 | `FAIL (… harness=fail)` |
| pub-gN02(true) | kill | 1 | KILL | 15158 | 0 | `FAIL (… harness=fail)` |
| pub-gN03(or) | kill | 1 | KILL | 15158 | 0 | `FAIL (… harness=fail)` |
| pub-gD01(drop=st_mado,dup=st_citecheck) | kill | 1 | KILL | 15158 | 0 | `FAIL (head=pass static=fail …)` |
| pub-B0-pristine | accept | 0 | ACCEPT | 15158 | 0 | `PASS (head=pass static=pass runtime=pass harness=pass)` |
| pub-B1-T07 | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |
| pub-B2-reversed | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |
| pub-B3-decoys | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |
| pub-B4-cosmetic | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |
| pub-B5-renamed | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |
| pub-gB6-permuted | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |
| pub-gB7-nonce | accept | 0 | ACCEPT | 15158 | 0 | `PASS (…all pass…)` |

The other three seeds have the same shape with their own generated labels (e.g. seed
`8899aabbccddeeff`: `pub-gT08(arm=233)`, `pub-gN05(< nlegs + 0)`, `pub-gN03(split)`,
`pub-gD01(drop=st_kagi,dup=st_citecheck)`) and the same verdicts. Full tables for all four seeds
are in `results.json`; the aggregate line printed by the driver is:

```text
seed=a1b2c3d4e5f60718 panel=26 (kill=18 accept=8) score_tool kill=18/18 accept=8/8 wall=216.6s misses=0 seed_ok=True
seed=1a2b3c4d5e6f7081 panel=26 (kill=18 accept=8) score_tool kill=18/18 accept=8/8 wall=184.7s misses=0 seed_ok=True
seed=0011223344556677 panel=26 (kill=18 accept=8) score_tool kill=18/18 accept=8/8 wall=162.2s misses=0 seed_ok=True
seed=8899aabbccddeeff panel=26 (kill=18 accept=8) score_tool kill=18/18 accept=8/8 wall=233.5s misses=0 seed_ok=True
WROTE /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/results.json overall_ok=True
```

## Independent cross-checks

### 1. Hand-written bwrap, outside the counter's helper

`spot.py` runs the pinned tool under a **hand-written** bwrap argv (not the counter's
`run_tool_sandboxed`) on one kill copy and one accept copy, then runs the same two copies
through the counter's helper and asserts the two paths agree. Exit 0.

```text
--- kill-T08 (manual bwrap) rc=1 ---
   CHECK head PASS legs=9
   CHECK static PASS legs=9 operands=9 nlegs=9
   CHECK runtime FAIL vectors=15158 mismatched=1674; first: cfg(0,1) statuses 4 0 0 0 0 0 0 0 0: …
   CHECK harness PASS reference cases=9; faults rejected=34/34
   TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
--- accept-B0 (manual bwrap) rc=0 ---
   CHECK head PASS legs=9
   CHECK static PASS legs=9 operands=9 nlegs=9
   CHECK runtime PASS vectors=15158 mismatched=0
   CHECK harness PASS reference cases=9; faults rejected=34/34
   TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
counter run_tool_sandboxed pub-T08         outcome=KILL   rc=1 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'
counter run_tool_sandboxed pub-B0-pristine outcome=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
```

The counter's helper and a hand-written sandbox agree on both verdicts and on the
`vectors=15158` figure.

### 2. The sandbox is real

Same `spot.py` run, sandbox probe under the same bwrap argv:

```text
usr_write_rc=1        (write to /usr denied)
w_write_rc=0          (write to the bound workdir allowed)
dns_rc=2              (name resolution denied — no network)
usr_probe_exists=2    (the probe file is not visible at /usr inside the sandbox)
host /usr/__labrat_probe_w exists: False
```

Nothing was written outside the scratch tree; the host `/usr` was untouched.

### 3. The tool's own selftest

With the pinned runner placed beside the tool (`selftest/tally-audit-v2.py` +
`selftest/mutate-and-run.sh`, both byte-identical to the pins):

```sh
python3 /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/selftest/tally-audit-v2.py --selftest
```

exit 0, `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` — all 22 seeded fault cases behave as declared.

## Observations (not findings against the claim)

**The 18 kill copies are not 18 distinct mutants.** The counter's public panel mixes 9 frozen
kill families with 9 seed-generated ones, and a generated copy can be **byte-identical** to a
frozen one. Distinct kill bodies per seed: 15 (`a1b2c3d4e5f60718`), 16 (`1a2b3c4d5e6f7081`),
16 (`0011223344556677`), 17 (`8899aabbccddeeff`). At the deciding-run seed
`685f63bd25263908` it is 14/18; at the controls seed `a7acbc0ec97d2710` it is 15/18. The 8
accept copies are always 8/8 distinct.

Reproducing command (exit 0):

```sh
python3 /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/panelcomp.py
```

Example output lines:

```text
seed=a1b2c3d4e5f60718   kill copies=18 distinct=15 dups=3 | accept copies=8 distinct=8 dups=0
     kill dup 2ac4ce5344e6: ['pub-H03', 'pub-gH03(form=0)']
     kill dup 741907e82ca7: ['pub-N03', 'pub-gN03(or)']
     kill dup e1ef181c1e62: ['pub-N05', 'pub-gN05(< nlegs)']
seed=685f63bd25263908   kill copies=18 distinct=14 dups=4 | accept copies=8 distinct=8 dups=0
     kill dup 0dc1e6b07452: ['pub-H04', 'pub-gH04(rc=$?)']
     kill dup 12ad1d9076a5: ['pub-T08', 'pub-gT08(arm=4)']
```

This is a property of the frozen v1 panel generator (the generated copy is drawn from the same
one-line edit space as the frozen copy), not a tool defect: the tool kills every copy it is
handed, and the counter's `v1_kill=18/18` counts copies, not distinct mutants. It does mean the
public panel's *effective* kill coverage is 14–17 distinct fault classes rather than 18, and
that figure moves with the seed — no single fixed number applies. Peer seat `PanelSeed2`
observed the same collision property independently at its own seed, so the wave sees one
observation across two seats. Worth carrying into round 35 as a panel-composition note; it does
not bear on the deciding run, which stands.

**Timing.** 797.09 s for 104 sandboxed tool runs (26 copies × 4 seeds), i.e. ~7.7 s per copy.
Per-seed wall time ranged 162.2 s – 233.5 s; the spread is host load, not seed content — every
seed ran the same 26-copy workload with the same `vectors=15158` sweep.

## Lane hygiene

- Writes confined to `/fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay/` and this one
  report file.
- `git -C .../lane status --porcelain` → empty (clone worktree clean).
- Live lane `git status --porcelain -- tools/tally-audit-v2.py tools/mutate-and-run.sh
  .ufo/evidence/round-33 .ufo/evidence/round-34` shows only three untracked files
  (`.ufo/evidence/round-34/dev/c1-deciding-run.{exit,stderr,stdout}`) that predate this seat
  (mtimes 16:25–16:27 local; this seat started 16:42) and were produced by the L1's dev run,
  not by this seat.
- `.ufo/evidence/round-33/heldout/` was never opened by this seat; its directory hash
  (`sha256sum … | sha256sum` → `9d13a4957c40a3ad06aad2c0d5ce24e8a55b8e545f39712cfd06df8ea7e8cdca`)
  was taken as a read-only existence check only.
- No git/jj write command was run anywhere. The counter's default mode
  (`c1-measure.py --lane … --rev … --work …`) was never executed.

## Reproduction

```sh
cd /fast/scratch/hyaku/tameshi-r34-seats/LabratPanelReplay
python3 driver.py   > driver.stdout 2>driver.stderr; echo $? > driver.exit   # 4 seeds, 797 s
python3 vecmath.py                                                       # vectors=15158 derivation
python3 panelcomp.py                                                     # panel composition / collisions
python3 panels.py                                                        # panel distinctness across seeds
python3 spot.py                                                           # independent bwrap + sandbox probe
```

Scratch artifacts: `driver.py`, `driver.stdout`, `driver.stderr`, `driver.exit`, `results.json`,
`vecmath.py`, `panelcomp.py`, `panels.py`, `spot.py`, `probe.py`, `tool.py`, `pristine.sh`,
`ctr/`, `work/`, `selftest/`.
