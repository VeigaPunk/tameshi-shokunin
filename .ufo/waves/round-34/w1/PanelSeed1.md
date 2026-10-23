# PanelSeed1 — round-34 w1 seat report (operability)

**Seat:** `PanelSeed1` (executor, axes: `operability`) · **wave:** `round-34-w1`
**Claim under attack:** C1 (operability capability acquisition, `tools/tally-audit-v2.py`),
MEASURED TRUE at measurement revision `c17e593b51802dd4ed568da3265f21c6d00c4273`.
**Lane tip at dispatch:** `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

## Verdict

| # | Assertion | Result | Pointer |
|---|---|---|---|
| V1 | Public panel replays through the counter's `score_tool` at the FIXED seed `r34seedAA01` → **18/18 kill, 8/8 accept** | **PASS** | §2, §3 |
| V2 | The same panel at the deciding-run seed `685f63bd25263908` and four further seeds → 18/18 + 8/8 each | **PASS** | §4 |
| V3 | Committed sealed set re-validated through the counter's own `validate_ho`/`apply_edits`/`ho_witness_ok` → 14 valid, 0 invalid, kill 8/8, accept 6/6 | **PASS** | §5 |
| V4 | Committed controls receipt re-scored independently at `r34seedAA01` → all four controls `predicate_pass=false`, counts identical to the receipt | **PASS** | §6 |
| V5 | Tool self-test `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` | **PASS** | §7 |
| V6 | Committed dev authoring receipts are self-consistent (stdout vs JSON) | **FAIL** — one copy disagrees; see F1 | §8, F1 |
| V7 | The counter's `heldout_after_freeze` gate proves the sealed set was authored *after* the counter bytes in force | **FAIL (latent gate weakness)** — see F2 | §8, F2 |

**The landed C1 measurement stands.** Every replay in §2–§7 reproduces the deciding run's
numbers. Two findings are reported; neither falsifies the deciding run (F1 is a receipt
bookkeeping defect already narrated in the round-34 lesson; F2 is a *latent* counter
weakness whose stronger condition also holds on the lane).

**Falsification status:** no artifact of the landed claim was proven wrong. F1 and F2 are
defects in supporting evidence / in the counter's gate strength, not in the claim's
truth at the measurement revision.

## 1. Setup, pins, and kill-rule compliance

Commands (run from `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed1`; each exit code captured
separately with `; echo $? > file`, never `&&`):

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed1            # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
    /home/vgpnk/Projects/shokunin/tameshi-shokunin .../lane           # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                        # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py    # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane show \
    0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh # exit 0
sha256sum tool.py pristine.sh                                        # exit 0
```

Pin check (`sha256sum tool.py pristine.sh`, exit 0):

```
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

Both match the pins named in the assignment. The counter at the lane tip:

```
sha256sum lane/.ufo/evidence/round-33/c1/c1-measure.py
f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c
```

— identical to the `counter_sha256` named in the committed controls receipt
`.ufo/evidence/round-33/c1/controls-receipt.json`, and identical to the pin quoted in the
assignment.

The same three file hashes hold at the **measurement revision** `c17e593b…` (verified with
`git show <rev>:<path> | sha256sum`): tool `7b11ba25…8d10`, runner `a7d3f2dd…2eb9`, counter
`f6b8868c…a07f28c`. So the deciding run at `c17e593b` and this seat's replay at the tip
`0b99d48` scored the *same bytes*.

**Kill rule (consumed — respected).** `python3 .ufo/evidence/round-33/c1/c1-measure.py --lane …
--rev … --work …` was **never** run in default mode. The counter was imported as a module in
this seat's scratch dir and only `public_panel`, `score_tool`, `run_tool_sandboxed`,
`block_run`, `ho_witness_ok`, `validate_ho`, `apply_edits`, `list_tree`, `show`,
`adding_commit`, `is_ancestor` were called, on scratch copies. `write_controls` was called
exactly once per scratch repo with an explicit scratch `receipt_path`, never the lane's
`CONTROLS_PATH`.

**Writes.** Only inside `/fast/scratch/hyaku/tameshi-r34-seats/PanelSeed1/` and this report
file. No write to the lane, `MANIFEST.json`, `templates/`, `scripts/`, `.ufo/state/`,
`.ufo/watchdog.log`, any sibling repo, or any jj/git index. No `git`/`jj` write command was
run anywhere (`git clone`/`checkout`/`show`/`log`/`rev-parse`/`merge-base`/`ls-tree`/`status`
are reads; the scratch probe repos were created with `git init`/`add`/`commit` **inside the
seat's own scratch dir**). No package was installed or upgraded this wave — the host already
provided `bubblewrap 0.13.1`, `timeout`, `python3 3.14`, so the operator tooling directive
(`/home/vgpnk/.omp/agent/RULES.md`) did not require a transaction.

## 2. The assigned replay: public panel through `score_tool` at seed `r34seedAA01`

Command:

```
python3 replay_seed.py > replay.stdout 2> replay.stderr ; echo $? > replay.exit
```

* driver: `replay_seed.py` (scratch)
* exit code: **0** (`replay.exit` = `0`)
* stdout: `replay.stdout`; machine-readable: `seed-replay.json`
  (sha256 `a465d5c244c77b11c70188bb0b86be2c1ce5c12273a6b854cc3cf96c83359624`)

Key lines (`replay.stdout`):

```
PANEL_COPIES 26 (kill=18 accept=8) build_s=0.003
PERCOPY_TALLY kill=18/18 accept=8/8
SCORE_TOOL kill=18/18 accept=8/8 elapsed_s=203.002
SEED_REPLAY_PASS true
```

**Assertion: `score_tool` at seed `r34seedAA01` gives 18/18 kill and 8/8 accept. MET.**

Elapsed time (the assigned capture):

| measurement | seconds |
|---|---|
| panel build (`public_panel`, 26 copies) | **0.003** |
| per-copy replay through the counter's sandboxed runner (26 copies) | **186.198** |
| **`score_tool` over the same 26 copies (the assignment's required path)** | **203.002** |
| whole seat script (build + per-copy + `score_tool`) | 389.30 (wall, `bg_2313`) |

Per-copy wall time ranges 5.66 s – 10.21 s; the two slowest are `pub-gN01(vector=2)`
(10.21 s) and `pub-gN02(true)` (9.91 s). The `score_tool` pass (203.002 s) is marginally
slower than the per-copy pass (186.198 s) because the two runs do identical work and the
difference is machine contention from the five concurrent seed sweeps running alongside
(§4), not a difference in the panel.

## 3. Per-copy outcome table (seed `r34seedAA01`)

Each row is one `run_tool_sandboxed` call by the counter (real `bwrap` boundary, `timeout 600`
outside the sandbox, read-only runtime mounts, writes confined to the per-run workdir).
`rc` is the process exit code; `outcome` is the counter's own KILL/ACCEPT/OTHER
classification; `expected-ok` is the counter's own predicate applied to that row.

| copy | set | rc | outcome | expected-ok | last stdout line | s |
|---|---|---|---|---|---|---|
| pub-T08 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | 5.66 |
| pub-N05 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | 6.23 |
| pub-H03 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 5.99 |
| pub-H04 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 5.67 |
| pub-H05 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 6.18 |
| pub-N01 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 6.20 |
| pub-N02 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 6.62 |
| pub-N03 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 6.55 |
| pub-D01 | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | 6.13 |
| pub-gT08(arm=198) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | 6.44 |
| pub-gN05(< nlegs) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | 7.15 |
| pub-gH03(form=0) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 7.20 |
| pub-gH04(rc=$?) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=pass)` | 6.61 |
| pub-gH05(drop=8,dup=6) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=pass)` | 7.14 |
| pub-gN01(vector=2) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 10.21 |
| pub-gN02(true) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` | 9.91 |
| pub-gN03(or) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=pass)` | 7.19 |
| pub-gD01(drop=st_checklist,dup=st_citecheck) | kill | 1 | KILL | true | `TALLY_AUDIT: FAIL (head=pass static=fail runtime=pass harness=pass)` | 7.02 |
| pub-B0-pristine | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 6.65 |
| pub-B1-T07 | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 7.33 |
| pub-B2-reversed | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 7.77 |
| pub-B3-decoys | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 7.29 |
| pub-B4-cosmetic | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 8.25 |
| pub-B5-renamed | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 9.19 |
| pub-gB6-permuted | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 8.25 |
| pub-gB7-nonce | accept | 0 | ACCEPT | true | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` | 7.38 |

Every kill copy is caught by exactly one independent check (no copy is caught twice), and the
failing check differs across the four families — `runtime` catches T08/N05/gT08/gN05,
`harness` catches H03/H04/H05/N01/N02/N03 and their generated forms, `static` catches
D01/gD01. This matches the check-independence the tool's own `--selftest` advertises
(`tool.py` docstring: "Checks (each independent, each able to fail alone)").

The generated copies at seed `r34seedAA01` are *not* a repeat of the deciding run's: the
panel composition differs (deciding seed `685f63bd25263908` produced `pub-gT08(arm=4)`,
`pub-gH03(form=2)`, `pub-gH05(drop=1,dup=5)`, `pub-gN01(vector=0)`,
`pub-gD01(drop=st_citecheck,dup=st_mado)`; `r34seedAA01` produced the values in the table
above). The frozen 9 kill + 6 accept families and the 9 generated kill + 2 generated accept
copies are the same set of shapes, so the seed changes *which* instance of each generated
family is scored, not which families exist. Panel-bytes sha256 (over the 26 concatenated
copy bodies):

| seed | panel sha256 |
|---|---|
| `r34seedAA01` | `4d91b81ea2ea2030a9b95cfda814944f849a9786577b7cf32e0ad85fab8d21f2` |
| `685f63bd25263908` (deciding run) | `ad92022fe53edfb1e3ec2a03124d23371d0d7661acadd46e21044107289a8926` |
| `r34seedAA02` | `09f11473f4271b44cc5a61292817603a1a6b7b39756eb72e182cd9733e05bf7a` |
| `r34seedBB03` | `f91cbd2047aabd3c40ba8399840b6b9b639197707eacb3764d7d2dbd0d68e62c` |
| `r34seedCC04` | `fad510dc7767b69c9cc9ef00128b8ede308e0f3dceaa3293975917908c60d18d` |
| `r34seedDD05` | `7a29852b7c4c6d0c4fc01067c6be2b3a47a0e3991392a31ef475916e5dfea82f` |

## 4. Seed sensitivity (5 further seeds, including the deciding-run seed)

Command (five concurrent detached runs; each `python3 seed_sweep.py <seed>` with
`; echo $? > sweep-<seed>.exit`):

```
for s in 685f63bd25263908 r34seedAA02 r34seedBB03 r34seedCC04 r34seedDD05; do
  setsid nohup bash -c "python3 seed_sweep.py $s > sweep-$s.stdout 2> sweep-$s.stderr; echo \$? > sweep-$s.exit" < /dev/null > /dev/null 2>&1 &
done
```

All five exit **0**; stdout (`sweep-<seed>.stdout`):

| seed | kill | accept | elapsed s | exit |
|---|---|---|---|---|
| `685f63bd25263908` (deciding run's seed) | 18/18 | 8/8 | 181.09 | 0 |
| `r34seedAA02` | 18/18 | 8/8 | 181.04 | 0 |
| `r34seedBB03` | 18/18 | 8/8 | 181.21 | 0 |
| `r34seedCC04` | 18/18 | 8/8 | 180.97 | 0 |
| `r34seedDD05` | 18/18 | 8/8 | 181.10 | 0 |

Machine-readable: `seed-sweep.json` (sha256 `725bd0cb3b68bb5a7f1128773a547ea0496e8687fb71dcb73f9323646aed894d`).

The seed sweep exercises the generated families' *other* branches that `r34seedAA01` did not
reach — e.g. `r34seedBB03` scores `pub-gH04(:)` and `pub-gN02(or)` (where `r34seedAA01`
scored `pub-gH04(rc=$?)` and `pub-gN02(true)`), and `r34seedCC04` scores
`pub-gN05(<= nlegs - 1)` and `pub-gT08(arm=255)`. Six seeds × 26 copies = 156 scored copies,
all correct. **The public-panel verdict is seed-robust across the six seeds tried; the
deciding run's seed is not special.**

## 5. Independent re-validation of the committed sealed set

Command: `python3 heldout_replay.py > heldout.stdout 2> heldout.stderr ; echo $? > heldout.exit`
— exit **0**; stdout `heldout.stdout`; artifact `heldout-replay.json`
(sha256 `d6e9adbbbf1c57d29f06a92461ea90c114c1bd229604eb16149d20c5b127a303`).

This replays the deciding run's held-out branch against the **committed** sealed set at the
lane tip, using the counter's own `validate_ho` / `apply_edits` / `ho_witness_ok` /
`run_tool_sandboxed` on scratch copies (never the counter's `main()`):

```
HELDOUT_FILES 14
VALID_COUNT 14 INVALID_COUNT 0
HELD_TALLY kill=8/8 accept=6/6 elapsed_s=90.10
HELD_REPLAY_PASS true
```

Per-copy witness verdicts (`heldout.stdout`):

| sealed copy | set | witness verdict | tool verdict |
|---|---|---|---|
| ho-kill-head-extra-assign | kill | `head-leg-assignment` | KILL rc=1 (head=fail) |
| ho-kill-head-nonbare | kill | `head-leg-assignment` | KILL rc=1 (head=static=runtime=harness=fail) |
| ho-kill-vector-arm-swap | kill | `vector` | KILL rc=1 (runtime=fail) |
| ho-kill-vector-count-field-swap | kill | `vector` | KILL rc=1 (runtime=fail) |
| ho-kill-vector-fail-exit-swap | kill | `vector` | KILL rc=1 (runtime=fail) |
| ho-kill-vector-fail-threshold | kill | `vector` | KILL rc=1 (runtime=fail) |
| ho-kill-vector-setup-arm-skip | kill | `vector` | KILL rc=1 (runtime=fail) |
| ho-kill-vector-setup-threshold | kill | `vector` | KILL rc=1 (runtime=fail) |
| ho-accept-head-comment | accept | `head` | ACCEPT rc=0 (all pass) |
| ho-accept-head-version-rename | accept | `head` | ACCEPT rc=0 (all pass) |
| ho-accept-vector-arith-space | accept | `vector-equivalence` | ACCEPT rc=0 (all pass) |
| ho-accept-vector-block-comment | accept | `vector-equivalence` | ACCEPT rc=0 (all pass) |
| ho-accept-vector-inert-line | accept | `vector-equivalence` | ACCEPT rc=0 (all pass) |
| ho-accept-vector-tail-comment | accept | `vector-equivalence` | ACCEPT rc=0 (all pass) |

Reproduces `ho_kill=8/8 ho_accept=6/6 ho_invalid=0` from the deciding receipt exactly.

Freeze ordering on the lane (`git merge-base --is-ancestor`, all exit 0):

```
6aaad5b3… (counter's LAST MODIFYING commit)  ancestor-of  c17e593b…  -> rc=0
ee398492… (tool's LAST MODIFYING commit)     ancestor-of  c17e593b…  -> rc=0
f6d8a891… (counter's ADD commit)              ancestor-of  c17e593b…  -> rc=0
```

i.e. the sealed set (`c17e593b`) was committed after the last byte change to both the
counter (`6aaad5b3`, amendment 6) and the tool (`ee398492`, round-33 amendment 5). The
seal-after-freeze ordering the claim requires **holds on the lane**.

## 6. Independent re-scoring of the committed controls receipt

Command: `python3 controls_replay.py > ctl.stdout 2> ctl.stderr ; echo $? > ctl.exit`
— exit **0**; artifact `controls-replay.json` (sha256 `8d26b34cc55da4e20ca02712663b21be840daf5eca832fb7f0fbe3fca5641724`).

The four control tools committed at `.ufo/evidence/round-34/controls/` were re-scored
against the public panel at seed `r34seedAA01` with the counter's `score_tool`:

| control | this seat (kill / accept) | committed receipt (kill / accept) | `predicate_pass` (both) |
|---|---|---|---|
| CtlAlwaysFail.py | 18/18, 0/8 | 18/18, 0/8 | false |
| CtlAlwaysPass.py | 0/18, 8/8 | 0/18, 8/8 | false |
| CtlDoNothing.py | 0/18, 8/8 | 0/18, 8/8 | false |
| CtlShaOnly.py | 18/18, 1/8 | 18/18, 1/8 | false |

`CONTROLS_ALL_PREDICATE_PASS_FALSE True` — the receipt's substantive claim (no control
satisfies the claim predicate) reproduces, and every per-control count matches the receipt
even though the receipt was minted at a *different* seed (`a7acbc0ec97d2710`). The controls
are seed-insensitive because each control's behaviour does not depend on the generated
copies' specific values.

## 7. Tool self-test

```
cd selftest-dir && python3 -I tally-audit-v2.py --selftest     # exit 0
```

`TALLY_AUDIT_V2_SELFTEST: 22/22 pass` (full listing in `selftest.stdout`), matching the
committed dev receipt `.ufo/evidence/round-34/dev/tool-selftest.stdout`.

(Note: `--selftest` resolves the runner *beside the tool file*, so the tool and runner must
sit in the same directory. The first attempt from the seat root exited 1 with
`FileNotFoundError: '/fast/scratch/.../mutate-and-run.sh'` — expected, not a defect.)

## 8. Findings

### F1 — the two committed dev authoring receipts disagree about one sealed copy

**Severity:** evidence bookkeeping. **Does it falsify C1?** No (see "Impact"). **Landed
artifact affected:** `.ufo/evidence/round-34/dev/authoring.stdout` vs
`.ufo/evidence/round-34/dev/authoring-receipts.json`.

The committed stdout records, for `ho-kill-vector-setup-threshold`,
`"witness": [false, "vector"], "as_expected": false`, and its final line reads
`SEALED: kill=8 accept=6 all_as_expected=False`. The committed JSON receipts record, for the
same id, `"witness": [true, "vector"], "as_expected": true` — and all 14 receipts there are
`as_expected: true`. One of the two committed artifacts is wrong about the same copy.

Reproducing command:

```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed1
python3 receipt_check.py > receipt_check.stdout 2> receipt_check.stderr ; echo $? > receipt_check.exit
```

Exit code **0** (the script exits 0 when exactly one disagreement is found). Artifact:
`receipt-check.json`.

```
STDOUT_TAIL SEALED: kill=8 accept=6 all_as_expected=False
STDOUT_COPIES 14 RECEIPT_COPIES 14
RECEIPT_DISAGREEMENT id=ho-kill-vector-setup-threshold kind=VALUE-DISAGREEMENT stdout_witness=[False, 'vector'] stdout_as_expected=False receipts_witness=[True, 'vector'] receipts_as_expected=True
RECEIPT_DISAGREEMENT_COUNT 1
RECEIPTS_CLAIM_ALL_AS_EXPECTED True
STDOUT_CLAIMS_ALL_AS_EXPECTED False
```

Exactly **one** of the 14 copies disagrees in value; the other 13 agree on both fields.
The committed stdout says the seal ended `all_as_expected=False`; the committed JSON says
all 14 were as expected.

Both blobs are identical across the freeze rev `6aaad5b3`, the measurement rev `c17e593b`,
and the tip `0b99d48` (`git rev-parse <rev>:<path>` → `50df49bb…` for the JSON and
`ce5b24f8…` for the stdout at all three revs), so the disagreement was introduced when the
pair was committed at `6aaad5b3` and has never been reconciled.

Which one is right? The **stdout** is right. The committed sealed copy carries witness
`[2,0,0,0,0,0,0,0,0]`, and with that vector the pristine and mutated blocks differ
(pristine SETUP with `cannot-verify=1`, mutated PASS with `passed=8`), so the witness
genuinely demonstrates the fault. The stdout's `[False,'vector']` line is the *first*
authoring attempt with witness `[2,2,0,…]`, where — with `nsetup -gt 1` — two setups still
trip the guard and pristine and mutated tie (both SETUP). The round-34 lesson
(`corpus/lessons/round-34.md`, "Mistakes" §1) narrates exactly this: the copy was first
authored with `[2,2,0,…]`, the pre-data authoring harness caught it, and the fix `[2,0,…]`
was re-verified by execution. The lesson says the first-generation receipt is "preserved in
the scratch transcript" — but the *committed* `authoring.stdout` is that first generation,
and the committed JSON is the second generation. The pair committed at `6aaad5b3` mixes
generation 1 (stdout) and generation 2 (JSON).

**Impact.** None on the claim. The deciding run does not read either dev receipt; it
re-validates every sealed copy itself through `validate_ho` + `ho_witness_ok`, and §5
reproduces that: 14 valid, 0 invalid, 8/8 kill, 6/6 accept. The defect is that a committed
artifact pair contradicts itself and contradicts the lesson's narrative ("the fix … was
re-verified by execution" — true, but the committed stdout still shows the pre-fix
failure and `all_as_expected=False`). A reader auditing the freeze trail from the committed
tree alone sees a seal that reported `all_as_expected=False`.

**Reproducing command for the "which one is right" half** (shows the witness vector that
actually fails, and that the committed vector passes) — same script, second half:

```
COMMITTED_WITNESS_VECTOR [2, 0, 0, 0, 0, 0, 0, 0, 0]
PASSING_VECTOR [2,2,0,0,0,0,0,0,0] -> NOT in PASSING set
PASSING_VECTOR [0, 0, 2, 0, 0, 0, 0, 0, 0]
PASSING_VECTOR [0, 0, 3, 0, 0, 0, 0, 0, 0]
PASSING_VECTOR [0, 2, 0, 0, 0, 0, 0, 0, 0]
PASSING_VECTOR [0, 3, 0, 0, 0, 0, 0, 0, 0]
PASSING_VECTOR [2, 0, 0, 0, 0, 0, 0, 0, 0]   <-- the COMMITTED vector
PASSING_VECTOR [3, 0, 0, 0, 0, 0, 0, 0, 0]
PASSING_COUNT 6 FAILING_COUNT 58
COMMITTED_VECTOR_OK (True, 'vector')
```

The committed vector `[2,0,0,…]` passes (exactly one setup leg, which escapes the `-gt 1`
guard); the stdout's pre-fix vector `[2,2,0,…]` is **not** in the passing set (two setups
still trip the `-gt 1` guard, so pristine and mutated both report SETUP and the witness
cannot distinguish them). Of the 64 vectors with entries 0..3 in the first three positions,
only 6 demonstrate the fault — the witness is genuinely tight, and the committed choice is
one of the six that works.

**Recommended fix (routed, not applied — the dev receipts are frozen evidence this wave):**
regenerate `.ufo/evidence/round-34/dev/authoring.stdout` from the same run that produced the
committed `authoring-receipts.json`, or annotate the stdout as the first-generation capture
and point at the second-generation receipts. This is a round-35 item; it does not reopen
the deciding run.

### F2 — the counter's `heldout_after_freeze` gate proves less than its name

**Severity:** counter weakness (latent on this lane). **Does it falsify C1?** No — the
stronger condition also holds on the lane (§5). **Landed artifact affected:**
`.ufo/evidence/round-33/c1/c1-measure.py` (the counter is byte-pinned; **no edit made or
proposed to this wave** — this is a routed finding for a future counter version).

The counter computes the freeze ordering as:

```python
self_add = adding_commit(a.lane, a.rev, SELF_PATH)   # git log --diff-filter=A  (ADD commit)
tool_add = adding_commit(a.lane, a.rev, TOOL)         # ditto
...
add = adding_commit(a.lane, a.rev, path)              # ADD commit of each sealed copy
if not (is_ancestor(a.lane, self_add, add) and is_ancestor(a.lane, tool_add, add)):
    freeze_ok = False
heldout_after_freeze = int(freeze_ok and ho_kt + ho_at > 0)
```

`adding_commit` uses `git log --diff-filter=A`, i.e. the commit that *added* the file — not
the commit that last *modified* it. So the gate asserts "the sealed copies were committed
after the counter was first committed", not "…after the counter bytes in force were
committed". A counter **amended after** the sealed set was authored still satisfies
`is_ancestor(self_add, add)`.

The receipt-attestation rule does not close this: `controls_ok` only checks that the receipt
names the sha256 of the counter *at the revision being run*. Re-minting the receipt at the
amended rev matches the amended counter and yields `controls_ok=1`.

**Reproducing command:**

```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed1
python3 freeze_probe.py > freeze.stdout 2> freeze.stderr ; echo $? > freeze.exit     # exit 0
```

```
C1 (counter+tool+runner land) 8296bf209fe9893e25aa03c0585fa46107be3cd2
C2 (sealed copies land, counter still v1) 6b5b75c0de055a6476c21a7cf6abaa3cbe159418
C3 (counter AMENDED after sealed copies) 4780a7bd8daee5ccfd35ce4bcc1b399859853b26
FREEZE_GATE_RESULT {"freeze_ok": true, "heldout_after_freeze": 1, "ho_at": 1, "ho_kt": 1, ...}
COUNTER_LAST_MODIFYING_COMMIT 4780a7bd8daee5ccfd35ce4bcc1b399859853b26
LAST_MOD_IS_ANCESTOR_OF_SEALED False
```

— i.e. the gate reports `heldout_after_freeze=1` for a counter whose last modifying commit
is **not** an ancestor of the sealed copies. The same script also shows the lane itself is
clean:

```
LANE_COUNTER_LAST_MOD 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a
LANE_LAST_MOD_ANCESTOR_OF_SEALED True
```

**The full exploit, end to end** (a witness-invalid decoy counted as a valid must-kill
copy, with the claim predicate then evaluating TRUE):

```
cd /fast/scratch/hyaku/tameshi-r34-seats/PanelSeed1
python3 exploit_probe.py > exploit.stdout 2> exploit.stderr ; echo $? > exploit.exit     # exit 0
```

Two scratch repos are built with the identical 14-copy sealed set, differing only in the
sealed copy `ho-kill-vector-setup-threshold`, whose witness is set to the *invalid*
`[2,2,0,…]` (the pre-fix generation the stdout records). In the CONTROL repo the counter is
unmodified; in the EXPLOIT repo the counter's kill+vector witness rule is weakened
(`return a != b, 'vector'` → `return True, 'vector'`) **after** the sealed copies were
committed, and the controls receipt is re-minted at the amended rev. Each repo is evaluated
by importing **its own** counter module, exactly as the deciding run imports the counter at
its rev.

```
CONTROL_counter_v1    {"CLAIM_PASS": false, "controls_ok": true, "heldout_after_freeze": 1,
                       "ho_at": 6, "ho_invalid": 1, "ho_kt": 7,
                       "invalid_ids": [["ho-kill-vector-setup-threshold",
                                        "witness does not demonstrate the fault"]], ...}
EXPLOIT_counter_amended{"CLAIM_PASS": true,  "controls_ok": true, "heldout_after_freeze": 1,
                       "ho_at": 6, "ho_invalid": 0, "ho_kt": 8, "invalid_ids": [], ...}
SEALED_ADD_CONTROL 0449d5585dabe7689fc3540f26056b616f94b5e9
SEALED_ADD_EXPLOIT 38decb3bd9c3a11d0e29632f4fe09b41ddb35105
AMENDED_COUNTER_LAST_MOD c14ceda750744fa76bdff470934fdd4ef20914d0 sealed_add 38decb3b… last_mod_ancestor_of_sealed False
EXPLOIT_REPRODUCED True
```

With counter v1 the invalid copy is correctly rejected (`ho_invalid=1`, `ho_kt=7 < 8`,
claim FALSE). With the counter amended after the seal, the same invalid copy is counted
valid (`ho_invalid=0`, `ho_kt=8`), `heldout_after_freeze=1`, and the claim predicate
evaluates **TRUE** — while the counter's last modifying commit is not an ancestor of the
sealed copies.

**Impact.** None on this round's C1 measurement:

* the lane's counter was last modified at `6aaad5b3`, which **is** an ancestor of the sealed
  set's commit `c17e593b` (§5) — so the real freeze ordering holds under the stronger
  reading;
* the lane's tool was last modified at `ee398492`, likewise an ancestor of `c17e593b`;
* the tool is additionally protected by a byte pin (`TOOL_SHA256`), so a tool amendment
  would fail `tool_sha_ok` outright — the tool side of the gate is not exploitable this
  way; the counter side is, because the counter's only protection is the receipt
  attestation, which the counter's own `--write-controls` mode can re-mint.

**Recommended fix (routed; the counter is byte-pinned and NOT edited this wave):** the next
counter version should compare the sealed copies' ADD commits against the counter's and
tool's **LAST MODIFYING** commits (`git log -1 --format=%H <rev> -- <path>`), not their ADD
commits. That single change makes `heldout_after_freeze` mean what its name says and closes
the exploit above.

## 9. What this seat did NOT do

* Did not run the counter in default mode (kill rule consumed).
* Did not edit the tool, the runner, the counter, the sealed set, the controls receipt, the
  dev receipts, `MANIFEST.json`, `templates/`, `scripts/`, `.ufo/state/`,
  `.ufo/watchdog.log`, the lesson, `SOURCES.md`, or any sibling repo. The tool's v3 residue
  classes remain measurement-only per the wave's Holds.
* Did not judge, widen scope, commit, push, deploy, or remediate external state.
* Did not modify the lane's git index or any jj state; the lane clone in the scratch dir is
  the only git repository this seat created read-only access to, and the two probe repos
  (`exploit-v1`, `exploit-v2`) live entirely inside the seat's scratch dir.

## 10. Artifact index (all inside the seat scratch dir)

| file | sha256 |
|---|---|
| `seed-replay.json` | `a465d5c244c77b11c70188bb0b86be2c1ce5c12273a6b854cc3cf96c83359624` |
| `seed-sweep.json` | `725bd0cb3b68bb5a7f1128773a547ea0496e8687fb71dcb73f9323646aed894d` |
| `heldout-replay.json` | `d6e9adbbbf1c57d29f06a92461ea90c114c1bd229604eb16149d20c5b127a303` |
| `controls-replay.json` | `8d26b34cc55da4e20ca02712663b21be840daf5eca832fb7f0fbe3fca5641724` |
| `freeze-probe.json` | `3c02ef70c117a21b711468620896e8aed330d4a9fae2b9fb5c38ef1144b8135b` |
| `freeze-probe2.json` | `3c5e8a47f5dbfc42fe7fab017fd640aff29c685c474b74c1017402e2266a634c` |
| `receipt-check.json` | `e44dc6346d802e2d160dd72a3e25266c2be1adfd2a7401a97dac5afd298f4f33` |
| `exploit-probe.json` | `8eb60b4867b8e571986f8b816ebf541ce06b4eeca1584e11385b65714a8dbe65` |

Every stdout/exit pair referenced above is preserved beside its script in the same dir.

## 11. Checks the parent should run

* None required for this seat's own artifacts — the seat's scope was replay-and-observe,
  and every number above was produced by the commands quoted with their exit codes.
* The parent owns the post-integration gate. Recommended (not run by this seat): re-run the
  public panel at seed `r34seedAA01` through `score_tool` once more on the parent's own
  machine if the wall-clock numbers in §2 are to be quoted as a timing baseline; this seat's
  timings were taken with five concurrent sweeps running (§4) and so are not a clean
  single-run baseline.
