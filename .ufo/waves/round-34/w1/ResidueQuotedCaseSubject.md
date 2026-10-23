# ResidueQuotedCaseSubject — C1 residue class: quoted `case` subject, measurement-only

Round 34 / wave 1 / mutation-tester seat. Lane tip at dispatch and at every run: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ResidueQuotedCaseSubject/` (every write here + this file).
No tool installed or upgraded; no network fetch; lane untouched (§8). The tool pin stays frozen — **no tool edit is proposed as landed work**; the only output is the measurement plus a round-35 Hold sketch (§7).

## 1. Setup and pins

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/ResidueQuotedCaseSubject                                  # clone_exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../ResidueQuotedCaseSubject/lane                        # clone_exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                                               # checkout_exit=0
git -C .../lane rev-parse HEAD  -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                              # revparse_exit=0
git -C .../lane show 0b99d48...:tools/tally-audit-v2.py  > tool.py                                       # show_tool_exit=0
git -C .../lane show 0b99d48...:tools/mutate-and-run.sh   > pristine.sh                                   # show_runner_exit=0
```

| artifact | sha256 | pin | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |

Both hashes re-verified after all runs (`probe/restored.sha256`: `tool.py 7b11ba25…8d10`, `pristine.sh a7d3f2dd…2eb9`). Every command in this report captured its own exit code with `cmd; echo $? > file`; no `&&` chains, no git/jj write command, and `c1-measure.py` was **never** run in default mode (§3).

## 2. The defect probed — one token, subject form only

The class under test is the round-34 Holds entry "quoted case subject" (`lane/corpus/lessons/round-34.md:56-57`), and mechanically it is a single regex in the frozen tool:

- `tool.py:177` `CASE_RE = re.compile(r'case[ \t]+\$([A-Za-z_][A-Za-z0-9_]*)[ \t]+in\b')` — the subject must be a bare `$ident`.
- `tool.py:190-199` `counting_case()` gates everything: no `CASE_RE` match with ≥2 counter increments ⇒ ``raise CannotAudit('counting `case $VAR in` not found')``.
- `tool.py:202-240` `tally_loop()` calls `counting_case()` first, so **loop identification never runs** when the subject is not bare.
- `tool.py:176` `OPERAND_RE` in the same parsing section already tolerates `"$st_x"` and `${st_x}` — the asymmetry is internal to the tool, not a deliberate subject restriction.
- `tool.py:555-577` `audit()` builds all four check results in one list literal (`:566`), so a `CannotAudit` from `check_static` aborts before any `CHECK …` line prints: one locator miss costs head+static+runtime+harness at once.

Copy mutations (each anchor asserted unique: `grep -n '^    case \$st in$' pristine.sh` → `1434:`, `grep_uniq_exit=0`; edits via the `edit` tool):

| copy | subject change | extra change | sha256 (mutated) |
|---|---|---|---|
| `probe/base.sh` | — | — | `a7d3f2dd…2eb9` (= pin) |
| `probe/quoted-correct.sh` | `case $st in` → `case "$st" in` | — | `2f4b75070d5083df656697c3b5c1223663730aac59845ac1f4635d96eb4291cf` |
| `probe/braced-correct.sh` | `case $st in` → `case ${st} in` | — | `5adb13e41ebcd935e10b72fdf05e9d5e269348054244a8df0edf3041a3e01bdb` |
| `probe/quoted-fault.sh` | `case $st in` → `case "$st" in` | `1) nfail=$((nfail + 1))` → `1) nsetup=$((nsetup + 1))` (sum-preserving fail→setup fold) | `a7db9b14d8bc4da4f0af90b1b59e8a3a4c721812dec72236279d54175ce88e68` |
| `probe/unquoted-fault.sh` | — | same fold, unquoted control | `1391fe5cd90a543e00ddae12fd379e3ad7b2b4e8d396aef6e27e65cf181e8581` |

Mutant bytes are preserved for audit under `probe/as-mutated/` (`probe/as-mutated/mutant.sha256`, same five hashes); the probed files themselves were restored (§8).

## 3. Detector

Primary detector = the frozen tool on a scratch runner copy, run identically on pristine, mutated and restored bytes:

```
python3 tool.py --runner /fast/scratch/hyaku/tameshi-r34-seats/ResidueQuotedCaseSubject/probe/<copy>.sh
  > probe/<copy>.out 2> probe/<copy>.err; echo $? > probe/<copy>.rc
```

Secondary detector = the round-33 counter's **own** verdict predicates, imported as a module (authorized; no default-mode invocation). `probe/score_probe.py` calls `run_tool_sandboxed` (bwrap boundary) and `score_tool` from `lane/.ufo/evidence/round-33/c1/c1-measure.py:245-283`:
`KILL = rc==1 && 'TALLY_AUDIT: FAIL'`, `ACCEPT = rc==0 && 'TALLY_AUDIT: PASS'`, else `OTHER`.

Baseline first, as required: pristine bytes must PASS or the probe is inconclusive.

## 4. Actual outputs

**Pristine** (`probe/base.rc` = `0`):

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=15158 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

| copy | exit | stdout (verdict line) | counter predicate |
|---|---|---|---|
| `base` | **0** | `TALLY_AUDIT: PASS (…)` | ACCEPT |
| `quoted-correct` | **2** | TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found) | OTHER |
| `braced-correct` | **2** | same line | OTHER |
| `unquoted-fault` | **1** | `CHECK runtime FAIL vectors=15158 mismatched=1800; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0: got (2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)'), want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')` → `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` | KILL |
| `quoted-fault` | **2** | TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found) | OTHER |

Sandboxed cross-check (`probe/score_probe.out`, `score_probe.rc=0`):

```
base            set=accept outcome=ACCEPT rc=0 last='TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)'
quoted-correct  set=accept outcome=OTHER  rc=2 last='TALLY_AUDIT: SETUP (counting `case $VAR in` not found)'
braced-correct  set=accept outcome=OTHER  rc=2 last='TALLY_AUDIT: SETUP (counting `case $VAR in` not found)'
unquoted-fault  set=kill   outcome=KILL   rc=1 last='TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)'
quoted-fault    set=kill   outcome=OTHER  rc=2 last='TALLY_AUDIT: SETUP (counting `case $VAR in` not found)'
SCORE kill=1/2 accept=1/3
```

**The kill detector never fires behind a quoted subject, and it fires normally on the same fault unquoted.** The whole verdict — not just one check — collapses to exit 2, because the abort happens while `audit()` assembles the result list (`tool.py:555-577`, list at `:566`), so no `CHECK` line is emitted at all.

## 5. Is the abstention justified? No — the quoting is behaviourally inert

`probe/block_compare.py` (imports `tool.py`, calls its own `run_vectors` on each copy's extracted tally block — execution only, no locator) over 6 vectors incl. `0…0`, `1,0…`, `2,0…`, `1,2,0…`, `0…,1`, `4,0…` (`block_compare.rc=0`):

```
base==quoted-correct: True      base==braced-correct: True
base==quoted-fault  : False     base==unquoted-fault: False
quoted-fault==unquoted-fault: True
```

- `"$st"` and `${st}` are the same bash subject semantics and produce byte-identical `(rc, first stdout line)` on every vector; the exit-2 is therefore a **locator refusal of a correct runner**, not a sound refusal of a broken one.
- The fold fault is real and execution-visible (fail leg reported as SETUP instead of FAIL), and identical whether quoted or not — the quoting changes nothing about the fault, only whether the tool can see it.

## 6. The class is already present in the sealed suite, and the frozen tool refuses it

Census over all 36 sealed copies at the tip, edits applied to the pinned runner via the counter's own `apply_edits`, then the extracted tally block handed to `counting_case` (`probe/sealed_probe.py`, `sealed_probe.rc=0`):

```
MISSES: 3/36
ACCEPT-MISSES: ['HeldOutRefactor-a1', 'HeldOutRefactor-a2', 'HeldOutTallyArms-04']
```

| sealed copy | set | subject form in the tally block | JSON blob at tip | derived body sha256 |
|---|---|---|---|---|
| `HeldOutRefactor-a1` | accept | `case $1 in` (digit subject) | `a4696d7371a4f4090b0a48d1cf329d41a70fcdf3` | `d26e730d9e0d51e8bc2fd4296009ef5249500743905811ffdd8a4ee1d849f5ac` |
| `HeldOutRefactor-a2` | accept | `case "$st" in` | `c791471a5a0faed92dde4f016856d799de240618` | `b79df45a003bf9212db827c60d61f6c163345da36121c0d439ee892b3d476458` |
| `HeldOutTallyArms-04` | accept | `case $((st == 0 ? 0 : st == 1 ? 1 : 2)) in` | `9a195d073e7c1339fdb58868ab0e0bf8dfeccf90` | `e87e02a1b8dfc51cabed05273364a92364867812e9569261b895d2fd2361c312` |

All three sealed in commit `24a5a5bb598ae919546715267d76f814efaf8912` (blob shas read with `git rev-parse 0b99d48…:…`, read-only). The frozen tool on each (`run_tool_sandboxed`, `sealed_probe.out`):

```
SEALED-RUN HeldOutRefactor-a1   set=accept outcome=OTHER rc=2 last='TALLY_AUDIT: SETUP (counting `case $VAR in` not found)'
SEALED-RUN HeldOutRefactor-a2   set=accept outcome=OTHER rc=2 last='TALLY_AUDIT: SETUP (counting `case $VAR in` not found)'
SEALED-RUN HeldOutTallyArms-04  set=accept outcome=OTHER rc=2 last='TALLY_AUDIT: SETUP (counting `case $VAR in` not found)'
```

Their blocks are behaviourally identical to the pinned runner on 8 vectors including two full-spectrum mixes (`probe/sealed_block_compare.py`, rc=0):

```
base==HeldOutRefactor-a1: True
base==HeldOutRefactor-a2: True
base==HeldOutTallyArms-04: True
```

**Why the deciding run still stands.** The receipt's `v1_accept=8/8` is scored over `public_panel(runner_b, seed)` (`c1-measure.py:286-295`), whose accept half is `frozen_accept` (`B0-pristine, B1-T07, B2-reversed, B3-decoys, B4-cosmetic, B5-renamed`, round-32 `c1-measure.py:140-158`) plus `generated_accept` (`gB6-permuted, gB7-nonce`, `:161-168`). None of those eight changes the `case` subject: their edits are guard arithmetic, operand order, decoy comments, arm spacing, `tgot`→`tcount` rename and nonce comments. The `ho_*` half is `.ufo/evidence/round-33/heldout/` — 14 copies, zero subject-form misses (§6 census). So the class was **outside the measured sample**, and `C1_R33_PASS=true` was not earned on it. Counterfactual, grounded on the predicates at `c1-measure.py:427-431`: had any one of the three sealed accepts been in the panel, it would score `OTHER`, so `v1a != v1at` (and `v1at` would exceed 8), making `C1_R33_PASS=false`. The deciding line is not wrong; it is silent on this class. `[INFERENCE]` only on the counterfactual arithmetic; the three `OTHER` verdicts are measured.

## 7. Verdict and the round-35 Hold

**Mutant:** quoted (and, by the same regex, braced / arithmetic / digit) `case` subject on a behaviourally identical tally block, with and without a counting fault behind it.
**Expected detector:** `CHECK static`/`runtime` FAIL → exit 1 (the fault is inside the tool's kill power — proven by `unquoted-fault`).
**Output:** exit 2, `TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found)`, no `CHECK` line.
**Verdict: the kill does NOT happen — the class survives as an abstention (`OTHER`), not as a false PASS.** Concretely:
- `quoted-fault` (a genuine fail→setup fold) is not killed (rc 2, not rc 1) — `kill=1/2`.
- `quoted-correct` / `braced-correct` (correct runners) are refused (rc 2, not rc 0) — `accept=1/3`.
- The three sealed accept copies above are refused today by the pinned tool.

This is a coverage/operability finding about the audit, exactly as routed in `corpus/lessons/round-34.md:56-57`; it does not license a contract change, and it is measured, not adopted.

No path to a false ACCEPT was found: `tally_loop` is unreachable without `counting_case`, and when a counting case *is* locatable the runtime check executes the whole block against an oracle built from the head's leg names, so a count-changing fault surfaces as a runtime mismatch (measured: 1800/15158 vectors). The cost of this class is a lost verdict, both directions. `[INFERENCE]` on the absence of a decoy construction that both identifies and still matches the oracle; the measured evidence is that every locator miss observed lands in `OTHER`.

Hold sketch for round 35 (measurement only — pin stays `7b11ba25…8d10`, no tool bytes touched): make the counting-case locator subject-form-agnostic (accept `"$var"`, `${var}`, `$((…))`, `$N`, or locate the case structurally by ≥2 counter increments) and make `audit()` emit the checks it did complete before reporting `SETUP`, so one locator miss does not erase head/harness findings. Acceptance for that Hold is measurable with the probes here: `quoted-correct`, `braced-correct`, `quoted-fault` and the three sealed bodies must move from `OTHER` to ACCEPT/ACCEPT/KILL/ACCEPT.

## 8. Restoration and containment evidence

- Restored from the pin: `cp pristine.sh probe/{quoted-correct,braced-correct,quoted-fault,unquoted-fault}.sh` (`restore_exit=0`). After: `sha256sum probe/*.sh` — all five including `base.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; `cmp -s pristine.sh probe/<each>.sh` → `0` for all five (`probe/restored.sha256` records the post-restore hashes).
- Detector re-run on restored bytes: `probe/restored-audit.rc=0` and `probe/restored-audit2.rc=0`, both `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`, `vectors=15158 mismatched=0`, `faults rejected=34/34`.
- Frozen artifacts re-hashed after every run: `tool.py 7b11ba25…8d10`, `pristine.sh a7d3f2dd…2eb9` — pins intact; the tool was never written to (only imported read-only in `probe/block_compare.py` / `probe/sealed_block_compare.py`).
- Lane: `git -C lane status --porcelain` produced no output (`status_exit=0`), `rev-parse HEAD` = `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (`rev_exit=0`). No git/jj write anywhere, no `MANIFEST.json`/`.ufo/state/`/`.ufo/watchdog.log`/sibling-repo touch.
- Evidence files under `probe/`: `base.sh`, `quoted-correct.sh`, `braced-correct.sh`, `quoted-fault.sh`, `unquoted-fault.sh`, `as-mutated/{*,mutant.sha256}`, `restored.sha256`, `score_probe.{py,out,err,rc}`, `block_compare.{py,out,err,rc}`, `sealed_probe.{py,out,err,rc}`, `sealed_block_compare.{py,out,err,rc}`, `sealed/*.sh`, `*.out`/`*.err`/`*.rc` per audit run.
- Installs/upgrades this seat: **none** (python3/bwrap/git already present; no pacman, no uv, no network).
