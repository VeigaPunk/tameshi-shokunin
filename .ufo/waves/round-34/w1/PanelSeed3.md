# PanelSeed3 — round-34 w1 seat report

Seat: `tameshi-r34-w1-PanelSeed3` (executor). Axis: **operability**.
Scope: replay the public panel through the round-33 C1 counter's `score_tool` with the FIXED
seed `r34seedCC03`; assert 18/18 kill and 8/8 accept; capture the per-copy outcomes table
and elapsed time.

Claim under attack: C1 (operability capability acquisition, `tools/tally-audit-v2.py`)
MEASURED TRUE at measurement revision `c17e593b51802dd4ed568da3265f21c6d00c4273`; deciding
receipt `C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18
v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1
seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true`, exit 0.

## Verdict

**REPLAY PASSED.** The public panel under the fixed seed `r34seedCC03` scores
**18/18 must-kill** and **8/8 must-accept** through the counter's own `score_tool`, reproduced
**three independent times** (aggregate pass + per-copy detail pass + timed pass), with
identical per-copy verdicts every time. The landed artifact behaves as claimed.

One fixture-strength finding (F1, LOW — does not affect the landed verdict): the public
panel's 18 must-kill **copies** represent only **16 distinct fault bodies** under the fixed
seed (14 under the deciding run's seed). The generated half of the panel re-draws from the
same mutation space as the frozen half, so some "generated" copies are byte-identical clones
of a frozen copy. The counter counts copies, not distinct shapes, so `v1_kill=18/18`
overstates the distinct-shape coverage of the public panel by 2 (fixed seed) to 5
(deciding seed). Detailed in F1 with a reproducing command.

---

## 1. Environment and setup (exact commands, exit codes)

All work under `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3/`. The lane clone is
read-only; the only writes were the seat scratch dir and this report file.

```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane                                    # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                                   # exit 0
```

| command | exit | observed |
|---|---|---|
| `git -C .../lane rev-parse HEAD` | 0 | `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (detached at the dispatch tip) |
| `git -C .../lane show 0b99d48e…:tools/tally-audit-v2.py > tool.py` | 0 | — |
| `sha256sum tool.py` | 0 | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` — **matches the frozen tool pin** |
| `git -C .../lane show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh` | 0 | — |
| `sha256sum pristine.sh` | 0 | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — **matches the frozen runner pin** |
| `git -C .../lane show 0b99d48e…:.ufo/evidence/round-33/c1/c1-measure.py \| sha256sum` | 0 | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — matches the amendment-6 counter pin given in the brief |
| `git -C .../lane ls-tree -r --name-only 0b99d48e… -- .ufo/evidence/round-33/heldout \| wc -l` | 0 | `14` (8 `ho-kill-*` + 6 `ho-accept-*`) |
| `git -C .../lane status --porcelain` (in the clone) | 0 | empty — lane worktree unmodified |
| `git status --porcelain` (in the fleet repo) | 0 | only sibling-seat untracked files (`…/round-34/dev/c1-deciding-run.*`, `.ufo/waves/round-34/w1/`) — no tracked-file modification by this seat |

Sandbox prerequisites present: `bwrap` → `/usr/bin/bwrap`, `bubblewrap 0.13.1`
(`bwrap --version` exit 0); `python3` → `Python 3.14.8` (exit 0).

Full transcript: `…/PanelSeed3/setup_exitcodes.txt`.

## 2. Method — kill rule respected

The kill rule is **CONSUMED**: the counter's default mode was **never** invoked. No
`python3 .ufo/evidence/round-33/c1/c1-measure.py --lane … --rev … --work …` was run in default
mode anywhere in this seat. Instead the counter was **imported as a module** into the seat's
scratch dir and its own functions were called on scratch copies:

* `c1.public_panel(pristine, 'r34seedCC03')` — builds the 26-copy public panel;
* `c1.score_tool(tool_path, copies, work)` — the **authoritative aggregate**;
* `c1.run_tool_sandboxed(tool, copy, work)` — per-copy runs, using the identical verdict
  logic `score_tool` applies internally (counter lines 265–284: `rc == 1 and
  last.startswith('TALLY_AUDIT: FAIL')` for kill; `rc == 0 and last.startswith('TALLY_AUDIT:
  PASS')` for accept).

Each run is a real `bwrap` boundary (`c1.bwrap_argv`: `--unshare-all --die-with-parent
--new-session --clearenv`, read-only `/usr /bin /lib /lib64 /etc`, `--tmpfs /tmp`, the run
dir `--bind`ed to `/w`), `timeout` outside the sandbox, per-copy workdir, stdout only.
The tool under test was the pinned blob extracted from the tip commit — never edited.

Driver scripts (all in the seat scratch dir):
`replay_panel.py` (aggregate + detail + JSON/TSV output), `replay_timed.py` (pass 3, per-copy
timing), `panel_compare.py`, `panel_determinism.py`, `fixture_sweep.py`,
`distinct_families.py`, `clone_check.py`, `coverage_sweep.py`, `heldout_distinct.py`.

## 3. Result — 18/18 kill, 8/8 accept

### 3.1 Aggregate via the counter's `score_tool` (authoritative)

`SCORE_TOOL_RESULT kill=18/18 accept=8/8` — exit 0.

### 3.2 Per-copy outcomes table (fixed seed `r34seedCC03`)

`hit` = the counter's verdict predicate. `copy_sha256` = sha256 of the mutated runner bytes
actually fed to the tool, so every row is independently checkable.

| idx | label | set | outcome | rc | hit | last stdout line | copy sha256 (16) |
|---|---|---|---|---|---|---|---|
| 0 | pub-T08 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `12ad1d9076a55050` |
| 1 | pub-N05 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `e1ef181c1e621962` |
| 2 | pub-H03 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `2ac4ce5344e6100a` |
| 3 | pub-H04 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `0dc1e6b07452f610` |
| 4 | pub-H05 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `adf6763d6524f342` |
| 5 | pub-N01 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `c0a32ec4e69d3cb0` |
| 6 | pub-N02 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `31128639afc3e57a` |
| 7 | pub-N03 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `741907e82ca7e907` |
| 8 | pub-D01 | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | `71a66c5a611d408f` |
| 9 | pub-gT08(arm=6) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `90c1dbd864de7448` |
| 10 | pub-gN05(< nlegs) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `e1ef181c1e621962` |
| 11 | pub-gH03(form=2) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `7f1787411f0ff16c` |
| 12 | pub-gH04(true) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `eceff075da31e6d4` |
| 13 | pub-gH05(drop=2,dup=6) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `4c70742fbb26f336` |
| 14 | pub-gN01(vector=0) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `71d7c5f20bfccac6` |
| 15 | pub-gN02(or) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | `31128639afc3e57a` |
| 16 | pub-gN03(split) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | `16566843890d60ab` |
| 17 | pub-gD01(drop=st_tsu,dup=st_mado) | kill | KILL | 1 | 1 | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | `c557f5cecb5bd9eb` |
| 18 | pub-B0-pristine | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `a7d3f2dd7d47511a` (= pristine runner) |
| 19 | pub-B1-T07 | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `91066af826f69ecb` |
| 20 | pub-B2-reversed | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `7d3d5a5f34fe3595` |
| 21 | pub-B3-decoys | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `7c76617e87c11c49` |
| 22 | pub-B4-cosmetic | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `137a7ba8a58c52772` |
| 23 | pub-B5-renamed | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `f66fe32a4ea7ce76` |
| 24 | pub-gB6-permuted | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `2962db3316f352e0` |
| 25 | pub-gB7-nonce | accept | ACCEPT | 0 | 1 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | `1a3c3bec36403646` |

Machine-readable: `…/PanelSeed3/replay_table.tsv` (TSV) and `…/PanelSeed3/replay.json`
(full rows incl. copy sha256 and per-pass aggregates).

**18/18 kill hits, 8/8 accept hits — no copy landed in `OTHER` (no timeout, no rc∉{0,1},
no `TALLY_AUDIT: SETUP`).**

### 3.3 Reproducibility — three independent passes

| pass | script | what it did | kill | accept | elapsed | exit |
|---|---|---|---|---|---|---|
| 1 | `replay_panel.py` | `c1.score_tool` aggregate | 18/18 | 8/8 | 214.09 s | 0 |
| 2 | `replay_panel.py` | per-copy detail (`run_tool_sandboxed`) | 18/18 | 8/8 | 187.60 s | 0 |
| 3 | `replay_timed.py` | per-copy detail, timed | 18/18 | 8/8 | 218.29 s | 0 |

(the first invocation of `replay_panel.py`, later re-run for the final artefacts, reported
aggregate 160.76 s and detail 236.48 s with the identical 18/18 + 8/8 result — the spread is
machine load, not verdict drift. Exit codes recorded in `replay.exit` = 0 and `pass3.exit` = 0.)

### 3.4 Elapsed time

* Whole panel, one full 26-copy sweep: **160.76 – 236.48 s** wall across four sweeps
  (aggregate + detail, twice), plus a separate timed sweep at **218.29 s**.
* Per-copy (pass 3): **min 5.04 s, median 8.25 s, max 16.33 s** (n=26).
  Slowest: `pub-B5-renamed` 16.33 s, `pub-B4-cosmetic` 11.74 s, `pub-gB7-nonce` 11.15 s,
  `pub-gB6-permuted` 9.64 s.
* Driver cost is dominated by the tool's own runtime sweep: `CHECK runtime PASS
  vectors=15158` — the tool evaluates 15,158 status vectors per copy, which is why each
  copy costs seconds rather than milliseconds.
* Reproduce: `python3 replay_timed.py` in the seat scratch dir (~220 s), or
  `python3 replay_panel.py` (~400 s, does both aggregate and detail).

### 3.5 Panel determinism

`public_panel(pristine, 'r34seedCC03')` is byte-deterministic: two calls in one process
produce identical labels, sets and bodies (`PANEL_DETERMINISTIC seed=r34seedCC03
identical=True`). Panel shape is 26 = 18 kill + 8 accept for every seed tried (10 seeds
sampled in `panel_determinism.py`; 51 seeds in `fixture_sweep.py`; 403 seeds in
`coverage_sweep.py`), confirming the counter's hard-coded `v1kt == 18 and v1at == 8`
(counter line ~415) is a property of the generator, not of the seed.

## 4. Findings

### F1 (LOW — fixture strength; the landed verdict is unaffected)

**The public panel's 18 must-kill copies represent fewer than 18 distinct fault shapes.**
The generated half of `public_panel` re-draws from the same mutation space as the frozen
half, so a "generated" copy can come out byte-identical to a frozen copy. The counter's
predicate counts **copies** (`v1k == v1kt` with `v1kt == 18`), so `v1_kill=18/18` overstates
distinct-shape coverage.

Measured (fixed seed `r34seedCC03`):

* 18 must-kill copies → **16 distinct bodies**; 2 clones:
  * `pub-gN05(< nlegs)` — sha `e1ef181c1e621962…` — byte-identical to frozen `pub-N05`
  * `pub-gN02(or)` — sha `31128639afc3e57a…` — byte-identical to frozen `pub-N02`
* 8 must-accept copies → **8 distinct bodies** (no redundancy on the accept side).

Measured (the deciding run's recorded seed `685f63bd25263908`):

* 18 must-kill copies → **14 distinct bodies**; 4 clones:
  `pub-gT08(arm=4)` == `pub-T08` (`12ad1d9076a55050…`),
  `pub-gN05(< nlegs)` == `pub-N05`,
  `pub-gH04(rc=$?)` == `pub-H04` (`0dc1e6b07452f610…`),
  `pub-gN03(or)` == `pub-N03` (`741907e82ca7e907…`).

**Seed sensitivity.** Over 403 seeds (`coverage_sweep.py`) the distinct must-kill count ranges
**13 – 18**: histogram `{13: 17, 14: 37, 15: 119, 16: 124, 17: 84, 18: 22}`. The deciding
run's seed landed at 14 — near the weak end. The fixed seed `r34seedCC03` lands at 16.

**Mechanism** (source: `.ufo/evidence/round-32/c1-measure.py`, `generated_kill`, lines 96–138):
each generator draws parameters from a set that overlaps the frozen generator's own
parameters. E.g. `generated_kill` L100 draws `form = rng.choice(['< nlegs', '< nlegs + 0',
'<= nlegs - 1'])` and L101 rewrites the same `GUARD` line the frozen `N05` rewrites
(L86: `GUARD.replace('!= nlegs', '< nlegs')`) — selecting `'< nlegs'` reproduces `N05` byte
for byte. The same overlap holds for `gT08`/`T08` (arm `4`), `gH03`/`H03` (form 0),
`gH04`/`H04` (tail `rc=$?`), `gH05`/`H05` (drop 8, dup 7), `gN01`/`N01` (vector 2),
`gN02`/`N02` (or), `gN03`/`N03` (or), `gD01`/`D01` (drop `st_citecheck`, dup `st_js`).
Empirically, **all nine** generated kill stems are clone-capable (`distinct_families.py`,
300 probe seeds).

**Impact assessment.** The landed measurement is **not** invalidated: the tool really does
exit 1 on all 18 copies and exit 0 on all 8, and a clone is a legitimate member of its
family — the counter's predicate is satisfied exactly as written. What is overstated is the
*inferred* coverage: a reader taking "18 public must-kill families" as 18 independent fault
shapes is wrong by 2 (fixed seed) to 5 (deciding seed). The redundant copies also make the
panel slightly cheaper to satisfy than it looks — but since the clones are exact duplicates
of copies that must also be killed, they add no *new* discrimination, only re-weighting.

**Counter-consideration (why this is LOW, not a measurement defect).** The claim's real
attack surface is the **sealed** held-out set, and that set has **no** redundancy: 8 must-kill
copies → **8 distinct bodies**, 6 must-accept → **6 distinct bodies**, zero cross-set overlap,
zero copies equal to the pristine runner (`heldout_distinct.py`; sha256 prefixes:
kill `c8615c3e…`, `bafb6e0d…`, `c2da7c59…`, `38cdf560…`, `82edd80e…`, `17496eb0…`,
`2fd82958…`, `44ae5f1e…`; accept `dc8fd28c…`, `c70bd0b3…`, `671a331d…`, `5f111e99…`,
`8f3b6032…`, `2a2b7305…`). The sealed set is where the discriminating power lives, and it
is clean. The public panel's redundancy is a *panel-design* weakness (a future panel wanting
maximum per-seed distinct coverage should de-duplicate the generated half against the frozen
half), not a defect in the landed tool, the counter, or the deciding run.

**Reproduce:**

```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3
python3 clone_check.py       # per-seed clone list + distinct counts  (exit 0)
python3 coverage_sweep.py    # 403-seed distinct-coverage sweep      (exit 0)
python3 distinct_families.py # clone-capable stem determination       (exit 0)
python3 heldout_distinct.py  # sealed-set distinctness (clean)         (exit 0)
```

`clone_check.py` output for the fixed seed:

```
seed=r34seedCC03
  kill: copies=18 distinct_bodies=16 redundant_copies=2
  accept: copies=8 distinct_bodies=8 redundant_copies=0
    REDUNDANT sha=e1ef181c1e621962 labels=['pub-N05', 'pub-gN05(< nlegs)'] sets=['kill']
    REDUNDANT sha=31128639afc3e57a labels=['pub-N02', 'pub-gN02(or)'] sets=['kill']
```

### F2 (NONE) — the landed tool's stdout contract matches the counter's wording

The contract predicate requires the **last stdout line** to begin with `TALLY_AUDIT:`, while
the counter actually takes the **last `TALLY_AUDIT:`-prefixed** line
(`run_tool_sandboxed`: `next((x for x in reversed(lines) if x.startswith('TALLY_AUDIT:')), '')`).
These coincide in practice: the tool prints the four `CHECK` lines and then the
`TALLY_AUDIT:` line as the final stdout line, and nothing follows it. Verified directly on
a must-kill copy (`pub-T08`) and a must-accept copy (pristine):

```
# kill copy, tool exit 1
n_lines=5 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)' \
  starts_with_TALLY_AUDIT=True
stderr bytes: 0
```

Reproduce:
```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3/lastline
timeout 300 python3 ../tool.py --runner m.sh > out.txt 2> err.txt; echo "exit=$?"
python3 -c "ls=open('out.txt').read().splitlines(); print(len(ls), repr(ls[-1]))"
```

No defect: the counter's `TALLY_AUDIT:`-prefix scan is a *looser* reading of the same
contract, and the tool satisfies the strict reading too. Recorded so the discrepancy is not
mistaken for a latent hole.

### F3 (NONE) — no other issue found in the replayed path

* Every copy landed in a decisive state; no `OTHER` outcome, no timeout, no `SETUP`.
* The tool never wrote to the runner (`tools/mutate-and-run.sh` is read-only in the copy; the
  accept copy `pub-B0-pristine` has sha `a7d3f2dd…` — identical to the pinned runner — so the
  tool left it byte-identical).
* The tool emitted **0 bytes on stderr** on both a must-kill and a must-accept copy, so the
  stdout-only comparison path is not contaminated.
* The fixed-seed panel differs from the deciding-seed panel in 8 of 26 copies (all in the
  generated half; the frozen half is seed-invariant, `panel_compare.py`), so the fixed seed
  is a genuinely different panel, not a re-run of the same one — the replay exercised
  mutants the deciding run did not.

## 5. Residual risk / verification gaps

* **The kill rule is consumed, so this seat did not and could not re-execute the deciding
  run.** This replay exercises the public-panel half of the counter's predicate (the
  `v1_kill`/`v1_accept` fields of the receipt) at a **different seed** than the deciding
  run's `685f63bd25263908`; it does not recompute `ho_kill=8/8`, `ho_accept=6/6`,
  `ho_invalid=0` or `heldout_after_freeze=1`. Those receipt fields were read from the
  committed bytes (see `ReviewPinChain.md`, same wave) but not recomputed here.
* The sealed-set distinctness check (F1's counter-consideration) applies the counter's
  `validate_ho` + `apply_edits` to the 14 sealed JSONs and dedups the resulting bodies; it
  does **not** re-run the sealed copies through the tool. The tool's behaviour on the sealed
  set is attested by the deciding receipt, not re-measured by this seat.
* Timing figures are single-host, single-wave measurements under concurrent wave load
  (dozens of sibling seats running); the 160–236 s sweep spread reflects that load, not
  tool nondeterminism. Verdicts were identical in all passes.
* `public_panel` is a pure function of `(pristine, seed)` — confirmed — but the counter's
  default-mode path additionally gates on the controls receipt and the held-out ancestry
  check, neither of which is reachable from a module-level replay. This seat therefore
  confirms the **panel-scoring** half of C1 only.

## 6. Tooling

**No installs, no upgrades, no pacman transactions.** The operator's tooling directive
(`/home/vgpnk/.omp/agent/RULES.md`, read at seat start) permits installing helpers, but none
was needed: system `git`, `sha256sum`, `python3` 3.14.8 and `bwrap` 0.13.1 sufficed. The
2026-10-20 pacman pause ruling was respected (no `pacman` invocation of any kind). Channel /
version / reason record: **no tool installed or updated — reason: task fully served by
preinstalled tooling.**

## 7. Artefacts (seat scratch dir `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3/`)

| file | content |
|---|---|
| `lane/` | read-only `--no-hardlinks` clone, detached at `0b99d48e…` |
| `tool.py`, `pristine.sh` | pinned blobs extracted from the tip commit; sha256 verified |
| `setup_exitcodes.txt` | exit codes + sha256s for the setup commands |
| `replay_panel.py` | aggregate (`score_tool`) + detail passes |
| `replay_timed.py` | third pass, per-copy timing |
| `replay.stdout`, `replay.exit` | transcript and exit code (0) of the final replay |
| `replay.json`, `replay_table.tsv` | per-copy table incl. copy sha256 and elapsed times |
| `pass3.stdout`, `pass3.exit`, `replay_pass3.json` | timed pass transcript/exit and timing data |
| `panel_compare.py`, `panel_compare.json` | fixed-seed vs deciding-seed panel diff |
| `panel_determinism.py` | panel determinism + 10-seed shape check |
| `fixture_sweep.py` | 51-seed fixture-robustness sweep (shape, pristine-equality, cross-set dups) |
| `distinct_families.py`, `clone_check.py`, `coverage_sweep.py` | F1 evidence (clone pairs, distinct counts, 403-seed sweep) |
| `heldout_distinct.py` | sealed-set distinctness (clean: 8/8 kill, 6/6 accept distinct) |
| `lastline/` | stdout-tail check for F2 |

## 8. Reproduction (single command)

```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed3
python3 replay_panel.py   # -> SCORE_TOOL_RESULT kill=18/18 accept=8/8, exit 0 (~400 s)
```
