# PanelSeed4 — round-34 w1 seat report

**Seat:** `tameshi-r34-w1-PanelSeed4` (executor, leaf). **Axis judged:** operability.
**Claim under attack:** C1 — operability capability acquisition, `tools/tally-audit-v2.py`,
MEASURED TRUE at measurement revision `c17e593b51802dd4ed568da3265f21c6d00c4273`.
**Lane tip at dispatch:** `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
**Scratch:** `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed4/`. No tools installed; no
pacman transaction attempted; the operator's pacman guard was respected throughout.

Everything below ran on scratch copies in that directory. The lane was cloned read-only and
its Git index/state was never written. The counter was **`import`ed as a module** and only
`public_panel`, `score_tool`, `run_tool_sandboxed`, `block_run`, `ho_witness_ok`,
`validate_ho`, `apply_edits`, `tally_block_of` were called — the counter's default-mode CLI
(the consumed kill rule) was **never** invoked.

## Verdict

| # | Assertion | Result | Pointer |
|---|---|---|---|
| V1 | Public panel replays through the counter's `score_tool` at the FIXED seed `r34seedDD04` → **18/18 kill, 8/8 accept** | **PASS** | §2 |
| V2 | Committed controls re-scored at the SAME fixed seed → all four `predicate_pass=false`, counts identical to the committed receipt | **PASS** | §3 |
| V3 | Committed sealed set replayed through the counter's own `validate_ho`/`apply_edits`/`ho_witness_ok` → 14 valid, 0 invalid, **kill 8/8, accept 6/6** | **PASS** | §4 |
| V4 | Frozen tool self-test → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | **PASS** | §5 |
| V5 | Every one of the 26 public panel labels independently justified **without consulting the tool** (50-vector / 18-stress block differential + 13-fault runner-owned harness differential) → **0 contradictions** | **PASS** | §6 |
| V6 | Tool, runner and counter are byte-identical at the measurement rev and the lane tip; sealed copies land after both freezes | **PASS** | §7 |
| V7 | The two committed dev authoring artifacts agree about every sealed copy | **FAIL** — one copy disagrees; see **F1** | §8 |
| V8 | The counter's `heldout_after_freeze` gate proves the bytes *in force* predate the sealed set | **FAIL (latent gate weakness)** — see **F2** | §8 |

**The landed C1 measurement stands.** Every replay reproduces the deciding run's numbers. F1
is an evidence-bookkeeping defect and F2 is a *latent* counter weakness; on this lane the
stronger freeze condition also holds, so neither falsifies the claim.

---

## 1. Setup — exact commands, exit codes, sha256s

All commands run from `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed4/`.

```bash
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed4                                   # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin lane                                      # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                               # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane log -1 --format='%H %s'
#  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7 round-34: C1 measured true at c17e593b ...
```

The lane checkout is detached at the tip and `git status --porcelain` is **empty** at the end
of the seat (`lane_status_exit=0`, §7) — every write went to the scratch dir except this one
report file.

### Byte pins (verified before any run)

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane show \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py          # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C lane show \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh      # exit 0
sha256sum tool.py pristine.sh
```

```
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Both match the dispatch pins, and match the same paths inside the lane worktree. The counter
at the tip hashes `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`, matching
the frozen counter pin, the `counter_sha256` field of the committed controls receipt, and the
counter blob at the amended rev `6aaad5b3` (§7).

---

## 2. Public panel replay at the FIXED seed `r34seedDD04`

```bash
python3 replay.py > replay.stdout 2> replay.stderr; echo "replay_exit=$?" > replay.exit
# replay.exit: replay_exit=0
```

`replay.py` (sha256 `88a3b0221d71a26536344fc78a9cc9e03ebb7ee1f425c036ff96ce06f6011af4`) imports
the lane counter, builds `public_panel(pristine_runner_bytes, 'r34seedDD04')`, and runs the
panel **twice**:

- a per-copy pass calling the counter's own `run_tool_sandboxed` (to capture per-copy detail),
- an aggregate pass calling the counter's own `score_tool` (the required assertion).

```
PINS tool_sha256=7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10 ok=True
PINS runner_sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 ok=True
COUNTER loaded sha256=f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c
PANEL copies=26 kill=18 accept=8 seed=r34seedDD04
SCORE_TOOL kill=18/18 accept=8/8 seconds=214.02
REPLAY_RESULT pass=True kill=18/18 accept=8/8
```

**Assertion holds: 18/18 must-kill, 8/8 must-accept.**

### Elapsed time

| Pass | Wall |
|---|---|
| per-copy detail pass (26 sandboxed tool runs) | **167.79 s** (sum of per-copy 167.69 s) |
| aggregate `score_tool` pass (26 sandboxed tool runs) | **214.02 s** |
| total `replay.py` wall | **381.86 s** |

Per-copy range 4.91 s – 10.92 s. No timeout, no `TALLY_AUDIT: SETUP`, no non-`TALLY_AUDIT`
exit in either pass.

### Per-copy outcomes table

| # | set | copy id | tool exit | last stdout line | hit | s |
|---|---|---|---|---|---|---|
| 1 | kill | `pub-T08` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | yes | 5.29 |
| 2 | kill | `pub-N05` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | yes | 5.08 |
| 3 | kill | `pub-H03` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 5.28 |
| 4 | kill | `pub-H04` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 4.91 |
| 5 | kill | `pub-H05` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 5.25 |
| 6 | kill | `pub-N01` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 5.28 |
| 7 | kill | `pub-N02` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 5.02 |
| 8 | kill | `pub-N03` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.02 |
| 9 | kill | `pub-D01` | 1 | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | yes | 6.26 |
| 10 | kill | `pub-gT08(arm=138)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | yes | 5.89 |
| 11 | kill | `pub-gN05(< nlegs)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | yes | 5.81 |
| 12 | kill | `pub-gH03(form=1)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.20 |
| 13 | kill | `pub-gH04(rc=$?)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.55 |
| 14 | kill | `pub-gH05(drop=3,dup=8)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.68 |
| 15 | kill | `pub-gN01(vector=3)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.22 |
| 16 | kill | `pub-gN02(or)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.21 |
| 17 | kill | `pub-gN03(or)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | yes | 6.72 |
| 18 | kill | `pub-gD01(drop=st_mado,dup=st_kagi)` | 1 | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | yes | 7.35 |
| 19 | accept | `pub-B0-pristine` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 7.09 |
| 20 | accept | `pub-B1-T07` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 6.53 |
| 21 | accept | `pub-B2-reversed` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 8.36 |
| 22 | accept | `pub-B3-decoys` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 10.92 |
| 23 | accept | `pub-B4-cosmetic` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 8.30 |
| 24 | accept | `pub-B5-renamed` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 6.85 |
| 25 | accept | `pub-gB6-permuted` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 6.88 |
| 26 | accept | `pub-gB7-nonce` | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | yes | 6.74 |

Machine-readable: `replay-result.json` (per-copy `rc`, `last`, `hit`, `seconds`, body sha256).

**Surface attribution.** Reading the `head/static/runtime/harness` breakdown across the 18
kill copies: 4 are killed on `runtime` (T08, N05, gT08, gN05), 2 on `static` (D01, gD01), 12
on `harness` (the H/N families and their generated variants). `head=fail` never fires on the
public panel — the head surface is exercised only by the sealed set (§4). Each kill copy is
killed by exactly one check, and every accept copy passes all four.

---

## 3. Controls re-scored at the same fixed seed (fixture discrimination)

The committed controls receipt was minted at seed `a7acbc0ec97d2710`, not at mine. To show
that my 18/18 + 8/8 is a *discriminating* result and not a panel that passes anything, the
four committed control tools were re-scored against the **same** `r34seedDD04` panel.

```bash
python3 controls_check.py > controls.stdout 2> controls.stderr; echo "controls_exit=$?" > controls.exit
# controls.exit: controls_exit=0
```

```
CTL CtlAlwaysFail.py kill=18/18 accept=0/8  predicate_pass=False
CTL CtlAlwaysPass.py kill=0/18  accept=8/8  predicate_pass=False
CTL CtlDoNothing.py  kill=0/18  accept=8/8  predicate_pass=False
CTL CtlShaOnly.py    kill=18/18 accept=1/8  predicate_pass=False
CONTROLS_RESULT all_false=True tools=4
```

All four fail the predicate, and the counts are **identical** to the committed
`.ufo/evidence/round-33/c1/controls-receipt.json` (`0/18`+`8/8`, `0/18`+`8/8`, `18/18`+`0/8`,
`18/18`+`1/8`). The committed receipt is seed-robust on this second, independent seed.
Control blob hashes at the tip: `CtlAlwaysFail 101dd5b6…`, `CtlAlwaysPass ed13d65e…`,
`CtlDoNothing 7587926d…`, `CtlShaOnly 4bc16067…` (first 16 hex).

---

## 4. Sealed held-out arm replayed against the deciding receipt

```bash
python3 heldout_check.py > heldout.stdout 2> heldout.stderr; echo "heldout_exit=$?" > heldout.exit
# heldout.exit: heldout_exit=0
```

Replicates the counter's held-out logic without default mode: for each of the 14 committed
sealed copies it applies the edits, runs the amendment-6 set-aware witness gate
(`ho_witness_ok`), counts invalid copies, then scores each valid copy with the tool.

```
HELDOUT files=14
HELDOUT_RESULT kill=8/8 accept=6/6 invalid=0 seconds=91.42
HELDOUT_MATCH_DECIDING_RECEIPT=True
```

| copy | set | witness | tool exit | last line |
|---|---|---|---|---|
| `ho-accept-head-comment` | accept | head | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `ho-accept-head-version-rename` | accept | head | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `ho-accept-vector-arith-space` | accept | vector-equivalence | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `ho-accept-vector-block-comment` | accept | vector-equivalence | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `ho-accept-vector-inert-line` | accept | vector-equivalence | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `ho-accept-vector-tail-comment` | accept | vector-equivalence | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| `ho-kill-head-extra-assign` | kill | head-leg-assignment | 1 | `TALLY_AUDIT: FAIL (head=fail static=pass runtime=pass harness=pass)` |
| `ho-kill-head-nonbare` | kill | head-leg-assignment | 1 | `TALLY_AUDIT: FAIL (head=fail static=fail runtime=fail harness=fail)` |
| `ho-kill-vector-arm-swap` | kill | vector | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| `ho-kill-vector-count-field-swap` | kill | vector | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| `ho-kill-vector-fail-exit-swap` | kill | vector | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| `ho-kill-vector-fail-threshold` | kill | vector | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| `ho-kill-vector-setup-arm-skip` | kill | vector | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| `ho-kill-vector-setup-threshold` | kill | vector | 1 | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |

Machine-readable: `heldout-result.json` (per-copy witness reason, mutated-body sha256, rc,
last line). This reproduces the deciding receipt's `ho_kill=8/8 ho_accept=6/6 ho_invalid=0`
exactly. The `head` surface is exercised only here (two head kill copies, two head accept
copies), which is why it never fires on the public panel.

---

## 5. Frozen tool self-test

```bash
mkdir -p toolprobe && cp tool.py toolprobe/tally-audit-v2.py && cp pristine.sh toolprobe/mutate-and-run.sh
cd toolprobe && python3 tally-audit-v2.py --selftest > selftest.stdout 2> selftest.stderr
# tool_selftest_exit=0
```

```
TALLY_AUDIT_V2_SELFTEST: 22/22 pass
```

All 22 cases pass: the pristine runner is accepted (exit 0) and all 21 defect runners are
rejected with the check each is designed to trip (`static`, `head`, `runtime`, `harness`),
including `reversed operands`, `aux wrapper loop`, `aux pre-count loop` and `second extraction
line` accepted at exit 0. This is an independent confirmation that the tool's own checks are
able to fail — the property the public panel depends on.

---

## 6. Independent, tool-free justification of every panel label

This is the seat's craft contribution. The public arm has **no witness gate**: unlike the
sealed arm (where `ho_witness_ok` proves each kill copy is a genuine fault independently of the
tool), the 18 public must-kill and 8 must-accept labels are trusted *by construction* and
scored *by the tool under test*. If tool and panel were jointly wrong, the public arm could not
see it. So I built an oracle that never consults the tool.

```bash
python3 oracle3.py > oracle3.stdout 2> oracle3.stderr; echo "oracle3_exit=$?" > oracle3.exit
# oracle3.exit: oracle3_exit=0
```

`oracle3.py` (sha256 `fe95eb76d9b1bd527a5a3610693a928c75847fe3cc08fbf171a14ff180876461`) uses
two differentials against the **pristine runner** (the frozen reference), never against the
tool:

**Surface A — tally-block behaviour.** For each copy, its tally block is compared with the
pristine block over **50 status vectors** (all-pass, then statuses {1,2,4,138,255} at each of
the 9 positions, plus 4 multi-status mixes) and **18 stressed variants** (each of the 9 loop
operands *duplicated* and *removed*). Stress is keyed by **leg name**, not by position, so a
copy whose operand *order* differs is compared on the same leg and is not falsely flagged.
A must-accept copy must be behaviour-preserving; a must-kill copy whose block differs must
differ on some vector.

**Surface B — runner-owned harness soundness.** The runner's own `--selftest` extracts its
tally block from *its own file* and asserts the harness detects faults. So a **known-faulty
block is spliced into the copy's file** and the copy's own selftest is run. A sound harness
rejects the fault (a `tally harness:` case FAILs); a weakened harness accepts it.
The **13-fault panel** is built from the pristine runner's own block — deliberately *not* the
tool's panel: `printf-count-swap`, `guard-overcount-only`, `status-3-passes`,
`setup-dropped-when-fail`, and `ignore-leg-<leg>` for each of the nine legs. The pristine
harness rejects **13/13** (`undetected=-`), so the panel is sound before it is used.

**Result: 0 contradictions in 26 copies.**

| copy | set | Surface A (block behaviour) | Surface B (harness soundness) | verdict |
|---|---|---|---|---|
| `pub-T08` | kill | differs (plain=9, stress=153) | harness identical to pristine | kill-justified |
| `pub-N05` | kill | differs (plain=0, stress=9) | harness identical to pristine | kill-justified |
| `pub-H03` | kill | preserving | missed 2/13 faults | kill-justified |
| `pub-H04` | kill | preserving | missed 13/13 faults | kill-justified |
| `pub-H05` | kill | preserving | missed 1/13 faults | kill-justified |
| `pub-N01` | kill | preserving | missed 1/13 faults | kill-justified |
| `pub-N02` | kill | preserving | missed 1/13 faults | kill-justified |
| `pub-N03` | kill | preserving | missed 2/13 faults | kill-justified |
| `pub-D01` | kill | differs (plain=14, stress=252) | harness identical to pristine | kill-justified |
| `pub-gT08(arm=138)` | kill | differs (plain=9, stress=153) | harness identical to pristine | kill-justified |
| `pub-gN05(< nlegs)` | kill | differs (plain=0, stress=9) | harness identical to pristine | kill-justified |
| `pub-gH03(form=1)` | kill | preserving | missed 2/13 faults | kill-justified |
| `pub-gH04(rc=$?)` | kill | preserving | missed 13/13 faults | kill-justified |
| `pub-gH05(drop=3,dup=8)` | kill | preserving | missed 1/13 faults | kill-justified |
| `pub-gN01(vector=3)` | kill | preserving | missed 1/13 faults | kill-justified |
| `pub-gN02(or)` | kill | preserving | missed 1/13 faults | kill-justified |
| `pub-gN03(or)` | kill | preserving | missed 2/13 faults | kill-justified |
| `pub-gD01(drop=st_mado,dup=st_kagi)` | kill | differs (plain=13, stress=234) | harness identical to pristine | kill-justified |
| `pub-B0-pristine` | accept | preserving | harness identical to pristine | accept-justified |
| `pub-B1-T07` | accept | preserving | harness identical to pristine | accept-justified |
| `pub-B2-reversed` | accept | preserving | harness identical to pristine | accept-justified |
| `pub-B3-decoys` | accept | preserving | harness identical to pristine | accept-justified |
| `pub-B4-cosmetic` | accept | preserving | harness identical to pristine | accept-justified |
| `pub-B5-renamed` | accept | preserving | rejected all 13 | accept-justified |
| `pub-gB6-permuted` | accept | preserving | harness identical to pristine | accept-justified |
| `pub-gB7-nonce` | accept | preserving | rejected all 13 | accept-justified |

Wall: 1174.07 s. Machine-readable: `oracle3-result.json`.

Reading of the table, which is the useful part:

- The 6 block-surface kill copies (T08, N05, D01 and their `g` variants) are *behaviourally*
  different from the pristine runner, independent of any audit tool. `N05`/`gN05` differ **only
  under operand stress** (`stress=9`, `plain=0`) — exactly the case a plain-vector oracle would
  miss, which is why the counter's runtime check stresses the loop. `gT08(arm=138)` differs
  only for status 138, which is why the sweep must reach every status, not a fixed set.
- The 12 harness-family kill copies have a **byte-identical tally block** and are justified
  purely on Surface B. `H04`/`gH04` accept *every* fault (13/13 missed); `H05` misses exactly
  the one leg whose position the copy dropped; `gH05` misses exactly `st_mado` (the dropped
  index 3); `gN01(vector=3)` misses exactly `status-3-passes` (the vector it deleted);
  `N02`/`gN02` miss the fault only the deleted stress case can catch. Each weakness is specific
  and matches the copy's name.
- All 8 accept copies are behaviour-preserving **and** their harness (where it differs at all —
  `B5-renamed` renames a counter, `gB7-nonce` adds comments) still rejects all 13 faults.

**This closes the gap the public arm leaves open: every one of the 26 labels is independently
justified, and none is contradicted.**

---

## 7. Byte identity, ancestry and freeze ordering

```bash
# identity across revs
for rev in c17e593b51802dd4ed568da3265f21c6d00c4273 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7; do
  git show $rev:tools/tally-audit-v2.py | sha256sum
  git show $rev:tools/mutate-and-run.sh | sha256sum
  git show $rev:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum
done
```

Both revisions yield, in order, `7b11ba25…8d10`, `a7d3f2dd…2eb9`, `f6b8868c…a07f28c` — the
three frozen artifacts are **byte-identical at the measurement rev and the lane tip**. The 14
sealed copies are likewise byte-identical across the two revs (`diff` of the per-file sha256
listing exits `0`).

Ancestry and freeze:

```bash
git merge-base --is-ancestor c17e593b5180... 0b99d48ed4e3...   # exit 0
git log --diff-filter=A --format='%H %s' 0b99d48ed4e3... -- <path>   # adding commits
```

| artifact | adding commit |
|---|---|
| `tools/tally-audit-v2.py` | `f6d8a891` round-33 freeze |
| `.ufo/evidence/round-33/c1/c1-measure.py` | `f6d8a891` round-33 freeze |
| `.ufo/evidence/round-33/c1/controls-receipt.json` | `9dd3174c` round-34 controls receipt minted at amended rev |
| `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` | `0b99d48e` tip |
| all 14 `.ufo/evidence/round-33/heldout/*.json` | `c17e593b` |

`9dd3174 → c17e593 → 0b99d48` in that order; the controls receipt is present at `c17e593b`;
the counter blob at the amended rev `6aaad5b3` hashes `f6b8868c…a07f28c`, matching the
receipt's `counter_sha256`. `git status --porcelain` on the clone is empty at the end
(`lane_status_exit=0`).

---

## 8. Findings

### F1 — the two committed dev authoring artifacts disagree about one sealed copy

**Severity:** evidence bookkeeping. **Does it falsify C1?** No. **Artifacts:**
`.ufo/evidence/round-34/dev/authoring.stdout` vs
`.ufo/evidence/round-34/dev/authoring-receipts.json`, both added at the same commit
`6aaad5b3`.

For `ho-kill-vector-setup-threshold` the stdout records
`"witness": [false, "vector"], "as_expected": false` and its final line reads
`SEALED: kill=8 accept=6 all_as_expected=False`; the JSON records
`"witness": [true, "vector"], "as_expected": true`, and all 14 of its receipts are
`as_expected: true`. Exactly one of the 14 copies disagrees.

**Which is right — adjudicated, not assumed.** Both witness vectors were replayed through the
counter's own amendment-6 gate:

```bash
python3 witness_check.py > witness.stdout 2> witness.stderr; echo "witness_exit=$?" > witness.exit
# witness.exit: witness_exit=0
```

```
COMMITTED sealed copy: id=ho-kill-vector-setup-threshold set=kill witness.vector=[2, 0, 0, 0, 0, 0, 0, 0, 0]
COMMITTED witness gate -> (True, 'vector')
FIRST-ATTEMPT witness [2,2,0,...] gate -> (False, 'vector')
BEHAVIOUR committed [2,0,0,...]    pristine=(2,'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)') mutated=(0,'REGRESSION: PASS (cases=9 passed=8; ledger legs exact: kille') differ=True
BEHAVIOUR first-attempt [2,2,0,...] pristine=(2,'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)') mutated=(2,'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)') differ=False
TOOL verdict on committed copy -> KILL rc=1 'TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'
ADJUDICATION JSON_IS_RIGHT
```

The **JSON is right**: it agrees with the committed sealed copy's actual witness vector
`[2,0,0,…]`, which genuinely separates pristine (`SETUP`, exit 2) from mutated (`PASS`,
exit 0), so the gate returns `(True, 'vector')`. The **stdout line is the stale
first-generation capture** using the pre-fix witness `[2,2,0,…]`, where two setups still trip
the `nsetup -gt 1` guard and pristine and mutated tie at `SETUP` — the defect the round-34
lesson's *Mistakes* §1 narrates. The stdout was never regenerated after the fix, so the
committed pair is unreconciled.

Two consequences worth routing:

1. `.ufo/evidence/round-34/dev/authoring.stdout` is a **stale first-generation capture**, and
   its final line `SEALED: … all_as_expected=False` reads as a seal failure to anyone who
   opens it first. It should be regenerated from the final generation, or renamed to say it is
   the preserved first generation.
2. `corpus/lessons/round-34.md` (Mistakes §1, `fix:`) points at
   `.ufo/evidence/round-34/dev/authoring-receipts.json` as holding the **first generation**.
   It does not — the JSON holds the corrected generation and the first generation lives in
   `authoring.stdout`. The pointer is off by one file.

Not a claim falsification: the counter re-derives each sealed copy's witness from the committed
JSONs at run time, and its `ho_invalid=0` is reproduced in §4 regardless of these dev receipts.

### F2 — the counter's `heldout_after_freeze` gate proves less than its name

**Severity:** counter weakness (latent on this lane). **Does it falsify C1?** No — the stronger
condition also holds here. **Artifact:** `.ufo/evidence/round-33/c1/c1-measure.py` (byte-pinned;
**no edit made or proposed**, routed for a future counter version).

The gate computes `adding_commit(...)` with `git log --diff-filter=A`, i.e. the commit that
**first added** the file, not the commit that last **modified** it:

```python
self_add = adding_commit(lane, rev, SELF_PATH)   # --diff-filter=A
tool_add = adding_commit(lane, rev, TOOL)         # --diff-filter=A
add      = adding_commit(lane, rev, path)         # --diff-filter=A, per sealed copy
freeze_ok = is_ancestor(self_add, add) and is_ancestor(tool_add, add)
heldout_after_freeze = int(freeze_ok and ho_kt + ho_at > 0)
```

So it asserts "the sealed copies were committed after the counter was *first* committed", not
"after the counter bytes *in force* were committed". A counter amended *after* the sealed set
was authored still satisfies it — and the receipt-attestation rule does not close this, because
re-minting the receipt at the amended rev matches the amended counter and yields
`controls_ok=1`.

**Measured on this lane:**

```bash
python3 freeze_check.py > freeze.stdout 2> freeze.stderr; echo "freeze_exit=$?" > freeze.exit
# freeze.exit: freeze_exit=0
```

```
COUNTER first_add=f6d8a891f1d966c5c3cdda385090da3a6e804675 last_modify=6aaad5b389e7eed426ec3b452617bcbf9bf7f35a
TOOL    first_add=f6d8a891f1d966c5c3cdda385090da3a6e804675 last_modify=ee3984924c4d52703209f8b971717c975898f4ba
COUNTER AMENDED AFTER FIRST ADD: True
TOOL    AMENDED AFTER FIRST ADD: True
FREEZE_RESULT weak_gate_holds=True strong_condition_holds=True counter_amended_after_first_add=True
```

Both the counter and the tool **were** amended after their first add (counter: amendment 6 at
`6aaad5b3`; tool: amendment 5 at `ee398492`). All 14 sealed copies were added at `c17e593b`,
which descends from both *last-modify* commits as well — so the stronger condition that the
gate's name implies holds too, and **the C1 result is unaffected**. The weakness is latent, not
exploited: it would only matter if a counter amendment landed after the sealed set. A future
counter version should gate on `git log -1 --format=%H REV -- path` (last modify) rather than
`--diff-filter=A`.

### O1 — the public panel's 18 kill slots exercise only 14 distinct faults (observation)

Not a defect and not a falsification — recorded because the wave is about fixture strength.
Under seed `r34seedDD04` the panel is 26 slots but **22 distinct bodies**; the kill arm is
**18 slots / 14 distinct bodies**; the accept arm is 8/8 distinct. The four duplicate pairs are
`pub-H04`=`pub-gH04(rc=$?)`, `pub-N02`=`pub-gN02(or)`, `pub-N03`=`pub-gN03(or)`,
`pub-N05`=`pub-gN05(< nlegs)` — in each case the generated variant re-drew exactly the frozen
mutation. The same redundancy exists under the deciding seed `685f63bd25263908` (4 pairs,
22/26 distinct, with `pub-T08`=`pub-gT08(arm=4)` this time).

The counter scores **slots**, and asserts `v1kt == 18` / `v1at == 8`, so the numbers are
correct as defined — but the effective fault diversity behind `v1_kill=18/18` is 14, not 18.
Reproducing command:

```bash
python3 -c "... public_panel(runner_b,'r34seedDD04') ... sha256 per body ..."   # exit 0
# distinct bodies 22 of 26; kill slots 18 distinct 14; accept slots 8 distinct 8
```

If the generator were made to reject a re-draw that collides with an already emitted body, the
same 18 slots would cover 18 faults. Routed as an observation only.

---

## 9. Instrument corrections made during the seat (honest record)

My first two oracles produced false alarms. They are recorded here so that their outputs are
not mistaken for findings against the landed artifact; only `oracle3.py` is cited as evidence.

| version | design | false contradictions | why it was wrong |
|---|---|---|---|
| v1 (`oracle-result.json`) | tally block vs pristine, 14 vectors, no stress | 15 | no operand stress (misses guard weakenings), vector set missed the injected arm status, and it measured the block surface for copies whose defect is in the *harness* |
| v2 (`oracle2-result.json`) | leg-name-keyed stress + harness fault panel | 4 | no all-pass vector (the guard is only reachable when `nfail==nsetup==0`), fault panel had only 2 legs (a dropped-position weakness needs the dropped leg), and no unknown-status fault (needed for the deleted `3 0 …` vector) |
| v3 (`oracle3-result.json`) | 50 vectors incl. all-pass; 18 name-keyed stresses; 13-fault panel, one per leg | **0** | — |

Each gap was diagnosed and closed; v3's panel is first validated against the pristine harness
(13/13 rejected) before being applied to the copies. `oracle.py` (v1) and `oracle2.py` exit 1
by design (they report contradictions); `oracle3.py` exits 0.

---

## 10. Risks, limits, and what this seat did not do

- **Judge.** No verdict is rendered on C1 beyond "the replays reproduce". The deciding run
  stands. F1 and F2 are routed, not remediated; the tool, runner, counter, receipt and sealed
  set were **not** edited.
- **Default mode.** The counter's default-mode CLI was never executed (kill rule consumed).
  All measurements call its functions on scratch copies.
- **Held-out copies were read** (they are the claim's sealed evidence and the §4 replay is in
  scope); they were not re-authored, re-scored at another seed, or copied into the lane.
- **The public arm's labels** are now independently justified (§6), but the *sealed* arm's
  labels rest on the counter's own witness gate plus the tool's verdict; I re-ran the gate and
  the tool but did not build an independent witness oracle for the sealed set beyond it.
- **Seed scope.** This seat used exactly one seed (`r34seedDD04`). Seed robustness is covered
  by sibling seats (`PanelSeed1`, `PanelSeed2`, `PanelSeed3`, `LabratPanelReplay`).
- **No packages installed, no tool upgrades, no pacman transaction.** Nothing to record under
  the operator's tooling directive.

## 11. Repro inventory (scratch dir `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed4/`)

| file | sha256 (short) | exit | produces |
|---|---|---|---|
| `replay.py` | `88a3b022…` | 0 | `replay-result.json`, `replay.stdout` |
| `controls_check.py` | `d0a110d4…` | 0 | `controls-result.json` |
| `heldout_check.py` | `c777227d…` | 0 | `heldout-result.json` |
| `witness_check.py` | `3344e7fc…` | 0 | `witness-adjudication.json` |
| `freeze_check.py` | `82dc19c6…` | 0 | `freeze-result.json` |
| `oracle3.py` | `fe95eb76…` | 0 | `oracle3-result.json` |
| `oracle.py` (v1) | — | 1 | `oracle-result.json` (superseded) |
| `oracle2.py` (v2) | — | 1 | `oracle2-result.json` (superseded) |
| `selftest_probe.py` | — | 0 | `probe-result.json` (superseded) |
| `toolprobe/` | — | 0 | `selftest.stdout`: `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` |
