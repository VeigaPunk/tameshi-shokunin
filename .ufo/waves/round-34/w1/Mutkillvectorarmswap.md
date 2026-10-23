# Mutkillvectorarmswap — round-34 w1 mutation probe

Seat: mutation-tester (leaf, no dispatch). Claim under attack: **C1** (operability capability
acquisition, `tools/tally-audit-v2.py`) MEASURED TRUE at revision
`c17e593b51802dd4ed568da3265f21c6d00c4273`; deciding receipt
`.ufo/evidence/round-34/measure/c1-deciding-run.stdout` (sha256
`3e28149f94f2e5d832e680285306f0166029858982cfc5ae32bd4f19c9a9b05c`) and
`c1-deciding-run.exit` = `0` (sha256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`),
which reports `ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true`. Lane tip at dispatch:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.

Scratch root (all writes here, plus this one report):
`/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorarmswap/`. Kill rule consumed: the counter CLI
was never run in default mode; the counter was imported as a module from the pinned lane path and
only its functions (`validate_ho`, `apply_edits`, `tally_block_of`, `block_run`, `ho_witness_ok`,
`run_tool_sandboxed`, `bwrap_argv`) were called on scratch copies.

## 0. Verdict summary

| probe | expected | actual | verdict |
|---|---|---|---|
| pristine baseline | rc 0, PASS | rc 0, `TALLY_AUDIT: PASS`, 15158 vectors / 0 mismatched, harness 34/34 | green |
| **assigned `ho-kill-vector-arm-swap` (kill)** | rc 1, FAIL | rc 1, `TALLY_AUDIT: FAIL … runtime=fail`, 15142/15158 mismatched | **KILLED**, consistent with `ho_kill=8/8` |
| restored bytes | rc 0, PASS | rc 0, PASS, hashes unchanged | exact restore |
| 3 unconditional in-family arm swaps | KILL | KILL ×3 | no survivor |
| cosmetic clone (accept control) | ACCEPT | ACCEPT | consistent |
| **F1** kill-arm-swap keyed to witness-shim `$root` | (attack) witness `True vector` | tool **ACCEPT** rc 0, 0 mismatched | **opposite of set — critical** |
| **F2** kill-arm-swap keyed to "not an audit literal root" | (attack) witness `True vector` | tool **ACCEPT** rc 0, 0 mismatched; lethal in every real config | **opposite of set — critical (tool miss)** |
| **F3** accept-arm-swap keyed to real `(auto=0,KEEP=0)` | (attack) witness `True vector-equivalence` | tool **ACCEPT** rc 0; lethal under `--workdir` | **false accept — C1-relevant** |

The assigned copy under attack is a genuine defect, the tool kills it on the intended surface, and
the deciding run's `ho_kill=8/8` is consistent with this probe. The adversarial findings target the
witness gate and the audit's fixed config table, not the landed receipt (see §3.5).

## 1. Setup and pin verification (before any run)

```console
$ mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorarmswap && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
    git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorarmswap/lane; echo $? > clone_rc.txt
$ env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C …/lane checkout -q --detach 0b99d48e…; echo $? > checkout_rc.txt
clone_rc=0  checkout_rc=0
$ env … git -C lane rev-parse HEAD
0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
$ env … git -C lane show 0b99d48e…:tools/tally-audit-v2.py > tool.py;     echo tool_extract_rc=$?
tool_extract_rc=0
$ env … git -C lane show 0b99d48e…:tools/mutate-and-run.sh > pristine.sh; echo runner_extract_rc=$?
runner_extract_rc=0
$ sha256sum tool.py pristine.sh
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh
```

All pins match the ticket exactly (`preflight` record in `results.jsonl`: `pins_ok: true`; tool
`7b11ba25…8d10`, runner `a7d3f2dd…2eb9`, counter `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`).
The sealed copy is byte-identical at the fleet path and at `c17e593b`:
`git -C lane show c17e593b:.ufo/evidence/round-33/heldout/ho-kill-vector-arm-swap.json | sha256sum` (scratch clone) =
`aa5e12e33effebf44cff3f71f79a753ee37115dfbead040ac7e599dea8812a30` = the working-tree file. The
lane checkout stayed detached at the dispatch tip and `git status --porcelain` was empty.

Detector, identical for pristine, mutated and restored bytes: the frozen counter's
`run_tool_sandboxed(tool, copy, work)` — real `python3 -I /w/tool.py --runner /w/copy.sh` under
`bwrap` (`timeout` outside the sandbox) — plus a supplementary capture with the same `bwrap` argv
(`probe.run_full`) that keeps the full `CHECK` lines; the two agree on `(rc, last line)` for every
run (`wrapper_agrees: true`). Tool bytes in every run were
`7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`.

## 2. Assigned copy: mutation, witness, verdict

The JSON's single edit (old string occurs exactly once in the tip bytes, asserted by
`apply_edits`; `old_len=66`, `new_len=66`):

```
-old  "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n"
+new  "      0) nfail=$((nfail + 1)) ;;\n      1) npass=$((npass + 1)) ;;\n"
```

Built from `pristine.sh` with the counter's own `apply_edits` →
`mutated-assigned.sh`, sha256 `c2da7c59d0ccfd0a3a2934303ec2f07bfb27708a991306f54c2b60c6ab25ea1b`,
106538 bytes (same size as pristine; the two arms are equal-length).

Witness (`ho_witness_ok` on scratch copies; `results.jsonl` stage `witness`):

```console
validate_ho ok; witness True 'vector' (vector [1,0,0,0,0,0,0,0,0])
a (pristine block) = (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
b (mutant block)   = (1, 'REGRESSION: FAIL (cases=9 passed=1 failed=8 setup=0)')
```

Detector, three byte states:

| bytes | copy sha256 | outcome | rc | last line |
|---|---|---|---|---|
| pristine `pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT | 0 | `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)` |
| sealed mutant `mutated-assigned.sh` | `c2da7c59d0ccfd0a3a2934303ec2f07bfb27708a991306f54c2b60c6ab25ea1b` | **KILL** | **1** | `TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)` |
| restored `pristine.sh` (re-audit) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | ACCEPT | 0 | `TALLY_AUDIT: PASS (… runtime=pass …)` |

The kill was earned on the tally surface, not incidentally:
`CHECK runtime FAIL vectors=15158 mismatched=15142; first: cfg(0,1) statuses 0 0 0 0 0 0 0 0 0:
got (1, 'REGRESSION: FAIL (cases=9 passed=0 failed=9 setup=0)'), want (0, 'REGRESSION: PASS
(cases=9 passed=9; …)')`; head/static/harness all PASS (`logs/assigned.log`,
`results.jsonl` stage `tool_run` label `assigned-kill-copy`). As an independent corroboration, the
runner's own `--selftest` on the mutant reports `MUTATE_SELFTEST: 98/106 pass / VERDICT: FAIL`,
with eight tally-harness failures (`results.jsonl` stage `runner_selftest` tag `assigned-mutant`).

**Verdict for the assigned copy: KILLED, as its label demands.** The deciding receipt's
`ho_kill=8/8` is consistent with this copy.

## 3. Adversarial: witness-valid copies the tool labels opposite to their set

### 3.1 Why a pure-semantics in-family variant cannot escape

The witness vector is itself in the tool's oracle sweep:

- Both extractors return the same block text for these bytes: the counter's `tally_block_of` and
  the tool's `tally_block`/`regression_body` agree for pristine and for the mutant (1562 chars
  each; `results.jsonl` stage `block_extraction`: `pristine_extractors_agree: true`,
  `mutant_extractors_agree: true`; pristine block sha `e163133c…2215d`, mutant `b3c604ed…c17c1`).
- `ho_witness_ok` for a kill+vector copy requires `pb != mb` and
  `block_run(pb, vec) != block_run(mb, vec)` at the declared vector
  (`c1-measure.py:184-220`; `block_run` compares `(rc, first stdout line)` under a fixed shim,
  `c1-measure.py:154-181`).
- `tally-audit-v2.py`'s runtime check sweeps every status 0..255 at every leg position — including
  `[1,0,…,0]` — under two configs (`tool.py:381`, `tool.py:265`), against an oracle of the
  pristine semantics (`tool.py:290-302`), and the pristine block matches that oracle on all 15158
  vector×config runs (baseline `mismatched=0`).

Therefore any divergence that is a function of the block text and status vector alone, visible at
the witness vector, also makes the tool's runtime check fail; the tool's label then equals the
witness-set label. Measured controls, all built by `apply_edits` (old occurs once), all witness
`True vector`, all **KILLED**:

| variant (sha256 of bytes) | mutant witness output | tool |
|---|---|---|
| `fam-swap-0-2` (`2e83c197…c1d5bd5`) | `(1, FAIL passed=0 failed=1 setup=8)` | KILL rc 1 |
| `fam-swap-1-2` (`58280cb4…6aca4`) | `(2, SETUP passed=8 cannot-verify=1)` | KILL rc 1 |
| `fam-rotate-all` (`0251755f…94a1b77`) | `(1, FAIL passed=0 failed=8 setup=1)` | KILL rc 1 |
| `fam-cosmetic-respace` (accept, `f9bfc65d…ff548`) | identical to pristine | ACCEPT rc 0 |

So within the *shim-insensitive* family no surviving construction exists. The escape has to read a
value that differs between the witness shim and **both** audit configs.

### 3.2 F1 — witness-shim channel (exact requested criterion): witness-valid kill, tool PASS

The witness shim is `local root=r auto=0 KEEP=1` (`c1-measure.py:167`); the audit's configs set
`root` to `tally-audit` and `/tmp/tally-audit-work` (`tool.py:265`, injected at `tool.py:279`).
Keying the arm swap on the shim's `root` produces a copy that is defective only where the witness
runs. Exact JSON (`variantA-rootkeyed.sh`, sha256
`bcf2e1b2c6b15663b91694bde3bfc8d6c297b4897e9345fbf87b731dfa5a1dae`):

```json
{
 "id": "adv-kill-rootkeyed-arm-swap",
 "author": "tameshi-r34-w1-Mutkillvectorarmswap",
 "set": "kill",
 "edits": [
  {
   "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n",
   "new": "      0) if [[ \"$root\" == r ]]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;\n      1) if [[ \"$root\" == r ]]; then npass=$((npass + 1)); else nfail=$((nfail + 1)); fi ;;\n"
  }
 ],
 "witness": {
  "vector": [1, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Observed: `validate_ho ok`; `ho_witness_ok = True 'vector'`;
`a = (1, '… passed=8 failed=1 …')`, `b = (1, '… passed=1 failed=8 …')`; **real pinned tool:
`ACCEPT`, rc 0, `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`,
`CHECK runtime PASS vectors=15158 mismatched=0`, harness 34/34**
(`results.jsonl` stage `variantA_expectation`; `logs/adv.log`). It is labelled `kill` and the tool
says PASS — opposite.

Control proving the key value is the seam: the same construction keyed on the tool's own literal
(`[[ "$root" == tally-audit ]]`, `variantA-control.sh`, sha256 `2aa663cf…2e025a`) is
**witness-invalid** (`False 'vector'`, because under the shim `root=r` the gate is false and the
block is pristine) and the tool **KILLS** it (`rc 1, runtime=fail, 7571 mismatched`). The tool is
not blind to the construction shape; it is blind to the shim's private value.

Boundary: F1's fault is a witness-only phantom — in every real `--regression` invocation (`root` is
a mktemp `/tmp/tameshi-r4-2-regression.XXXXXX` path or a user `--workdir`; `pristine.sh:1357-1364`)
the gate is false and the block is pristine (the only exception is a `--workdir` literally named
`r`). Impact is against the *witness gate*: a sealed
"must-kill" can be certified without being a defect. If sealed, the counter would score it as
not-killed and `ho_kill == ho_kt` would fail (fail-closed), so it cannot produce a false
`C1_R33_PASS`. This is the same `$root=r` shim channel the fail-threshold seat found independently
in a different family (`Mutkillvectorfailthreshold.md` §3.2, Finding A) — independent
reproduction, not a one-off.

### 3.3 F2 — audit-config literal sniffing: witness-valid kill, tool PASS, fault real in every real run

Key the swap to be **active outside the audit's two fixed roots**; then it is active under the real
default (mktemp root, `auto=1 KEEP=0`) and under `--workdir` (`auto=0 KEEP=0`), and inert only in
the audit. Exact JSON (`adv-kill-auditroot-sniff-arm-swap.sh`, sha256
`fdf158d1f198f7c04e63a9b14f7415138fadc8ed4f988199f6a1e4fbd14f5234`):

```json
{
 "id": "adv-kill-auditroot-sniff-arm-swap",
 "author": "tameshi-r34-w1-Mutkillvectorarmswap",
 "set": "kill",
 "edits": [
  {
   "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n",
   "new": "      0) if [[ \"$root\" != tally-audit && \"$root\" != /tmp/tally-audit-work ]]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;\n      1) if [[ \"$root\" != tally-audit && \"$root\" != /tmp/tally-audit-work ]]; then npass=$((npass + 1)); else nfail=$((nfail + 1)); fi ;;\n"
  }
 ],
 "witness": {
  "vector": [1, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Observed: witness `True 'vector'` (`a` passed=8 failed=1 vs `b` passed=1 failed=8); **real pinned
tool: `ACCEPT`, rc 0, PASS, 0 mismatched, harness 34/34** (`results.jsonl` stage
`evade_expectation`). Opposite of the `kill` label.

Where it is lethal — the tool's own block runner, one witness vector, four configs
(`results.jsonl` stage `config_matrix`):

| config `(root, auto, KEEP)` | pristine vs oracle | mutant vs oracle | lethal |
|---|---|---|---|
| `/tmp/tameshi-r4-2-regression.A1B2C3`, `1`, `0` (real default shape) | match | **mismatch** | yes |
| `/tmp/tameshi-r4-2-regression.A1B2C3`, `0`, `0` (real `--workdir`) | match | **mismatch** | yes |
| `tally-audit`, `0`, `1` (audit config A) | match | match | no |
| `/tmp/tally-audit-work`, `1`, `0` (audit config B) | match | match | no |

So this is not a phantom: the audit's PASS is a genuine false negative for a fault active in every
real invocation (the only exceptions are `--workdir` values literally equal to the two audit
literals, which never occur in practice). Boundary: the runner's own `--selftest` extracts the
tally block and runs it with `root=selftest-tally auto=0 KEEP=1` (`pristine.sh:2003`), which
does hit this gate — it reports `MUTATE_SELFTEST: 98/106 pass / VERDICT: FAIL` with 8 tally-harness
failures (`results.jsonl` `runner_selftest` tag `A2-auditroot-sniff`). The fleet's selftest gate
would catch F2; `tally-audit-v2.py` alone does not.

### 3.4 F3 — real `(auto=0, KEEP=0)` gap: witness-valid accept copy that is not semantics-preserving

The audit sweeps exactly `(0,1)` and `(1,0)` (`tool.py:265`). Two real runner combinations are
never swept: `(auto=0, KEEP=0)` (`--regression --workdir DIR` without `--keep`) and `(1,1)`
(`--keep` without `--workdir`) (`pristine.sh:1357-1364`, `KEEP=0` default at `:190`, `--keep` at
`:2067`). The `(0,0)` combination is the exact invocation the tool's own `--then-regression
--workdir` runs (`tool.py:580-583`). Keying the arm swap on that combination
yields an accept-labelled copy that the witness certifies equivalent and the tool accepts, while
the tally is inverted in that real invocation. Exact JSON
(`adv-accept-autokeep-gap-arm-swap.sh`, sha256
`16d59cfb313fe7a0c567e840381f3d4b3334c57e6debce9fef6e90d664555551`):

```json
{
 "id": "adv-accept-autokeep-gap-arm-swap",
 "author": "tameshi-r34-w1-Mutkillvectorarmswap",
 "set": "accept",
 "edits": [
  {
   "old": "      0) npass=$((npass + 1)) ;;\n      1) nfail=$((nfail + 1)) ;;\n",
   "new": "      0) if [[ $auto -eq 0 && $KEEP -eq 0 ]]; then nfail=$((nfail + 1)); else npass=$((npass + 1)); fi ;;\n      1) if [[ $auto -eq 0 && $KEEP -eq 0 ]]; then npass=$((npass + 1)); else nfail=$((nfail + 1)); fi ;;\n"
  }
 ],
 "witness": {
  "vector": [1, 0, 0, 0, 0, 0, 0, 0, 0]
 }
}
```

Observed: `validate_ho ok`; `ho_witness_ok = True 'vector-equivalence'` (`a == b`, mutant bytes
differ); **real pinned tool: `ACCEPT`, rc 0, PASS, 0 mismatched, harness 34/34**; and the runner's
own `--selftest` also passes (`MUTATE_SELFTEST: 106/106 pass`) because it runs `(0,1)`
(`results.jsonl` stages `evade_expectation`, `config_matrix`, `runner_selftest`).

Config matrix (same method as §3.3): lethal (`mutant != oracle`) at `(…/tameshi-r4-2-regression.A1B2C3, 0, 0)`;
inert at `(…,1,0)`, `(tally-audit,0,1)`, `(/tmp/tally-audit-work,1,0)`.

Impact: an accept-set copy can be witness-equivalent at the shim, tool-ACCEPTED, and genuinely
wrong under a real `--workdir` sweep. Because the counter scores `accept` by the tool's PASS
(`c1-measure.py:420-422`), such a copy would be counted in `ho_accept` and **C1 could be recorded
true with a defective accept copy in the panel** — unlike F1/F2 this direction is not fail-closed.
This probe does not examine the six landed accept copies; it proves the acceptance criterion admits
such a copy. Neither the audit nor the runner's selftest sees it.

### 3.5 Impact and boundary

- The tool is correct on the assigned copy and on every unconditional in-family construction
  (§2, §3.1). The deciding receipt stands as an observation; `ho_kill=8/8` is consistent with this
  copy, and no landed artifact is proven wrong here.
- The amended `ho_witness_ok` certifies behaviour **under its private shim** (`root=r auto=0
  KEEP=1`, cleared environment), not in the artifact's real config space. On the kill side that
  admits phantom must-kills (F1) and, in a fixed-config context, real misses the tool cannot see
  (F2); on the accept side it admits a defective copy that both the witness and the tool bless
  (F3).
- Root cause shared by F1-F3: the witness and the audit both run the block under *fixed literal*
  configuration values, so any construction keyed to those values partitions runs into "witness",
  "audit" and "real" lanes. The audit's own DevGuard rationale ("a guard weakened by a conjunct
  over `$auto/$KEEP/$root` … diverges under the other [config]", `tool.py:272-277`) covers the
  endpoints `(0,1)`/`(1,0)` but not the real combinations `(0,0)` and `(1,1)` (F3 uses `(0,0)`),
  and fixed `root` literals are trivially sniffable (F2).
- Recommended next-wave direction (no edits made this wave; artifacts frozen): witness
  `block_run` should use the audit's config triples and an explicitly set environment
  (`--setenv`, since `bwrap --clearenv` discards the `env=` dict), and/or require divergence to
  persist under a second config; the audit should add `(0,0)`/`(1,1)` and randomise/parameterise
  the root value (or run the real `--regression --workdir` replay and compare per-case counts)
  rather than sweeping two fixed literals.

## 4. Restoration evidence

- `sha256sum tool.py pristine.sh`: unchanged before/after all runs
  (`7b11ba25…8d10`, `a7d3f2dd…2eb9`); counter `f6b8868c…a07f28c` and sealed JSON
  `aa5e12e3…2a30` unchanged (`results.jsonl` stage `restore_check`, all `ok: true`).
- Pristine bytes re-audited after the mutant runs: `ACCEPT`, rc 0, `mismatched=0`
  (`results.jsonl` stage `tool_run` label `pristine-after`).
- Lane untouched: the scratch clone at the dispatch tip is clean (`git -C lane status --porcelain`
  → empty; HEAD still `0b99d48e…`, `results.jsonl` stage `lane_clean_check`). Every mutant exists
  only under the scratch root (`mutated-assigned.sh`, `variantA-*.sh`, `variantB-*.sh`, `adv-*.sh`,
  `fam-*.sh`). In the fleet tree, `git status --porcelain` after the report write shows
  `?? .ufo/waves/round-34/w1/` (the untracked wave directory that holds this report and its
  siblings' reports) plus the pre-existing `?? .ufo/evidence/round-34/dev/*` receipts (mtime
  16:23-16:27, before this seat started); this seat wrote only
  `.ufo/waves/round-34/w1/Mutkillvectorarmswap.md`.
- No `git`/`jj` write command was run anywhere; the lane index was never touched.

## 5. Tooling

No installs or upgrades: `bwrap` 0.13.1, Python 3.14.8, coreutils, git were already present and
sufficient. No pacman transactions (host-wide pause respected).

## 6. Reproduce

All commands run from the scratch root; each stage writes `results.jsonl` and its own log.

```console
S=/fast/scratch/hyaku/tameshi-r34-seats/Mutkillvectorarmswap; cd $S
python3 probe.py preflight > logs/preflight.log 2>&1; echo $? > logs/preflight.exit   # pins_ok true
python3 probe.py baseline  > logs/baseline.log  2>&1; echo $? > logs/baseline.exit    # ACCEPT rc 0
python3 probe.py assigned  > logs/assigned.log  2>&1; echo $? > logs/assigned.exit    # exit 0; copy KILL rc 1
python3 probe.py blocks    > logs/blocks.log    2>&1; echo $? > logs/blocks.exit      # extractors agree
python3 probe.py family    > logs/family.log    2>&1; echo $? > logs/family.exit      # 3 KILL + 1 ACCEPT
python3 probe.py adv       > logs/adv.log       2>&1; echo $? > logs/adv.exit         # F1 opposite, B opposite
python3 probe.py evade     > logs/evade.log     2>&1; echo $? > logs/evade.exit       # F2 opposite; F3 false accept
python3 probe.py probe     > logs/probe.log     2>&1; echo $? > logs/probe.exit       # tool block-runner probe
python3 probe.py selftest  > logs/selftest.log  2>&1; echo $? > logs/selftest.exit    # runner --selftest x4
python3 probe.py restore   > logs/restore.log   2>&1; echo $? > logs/restore.exit     # hashes + lane clean
```

Observed stage exit codes (`logs/*.exit`): `preflight=0 baseline=0 assigned=0 blocks=0 family=0
adv=0 evade=0 probe=0 selftest=0 restore=0`; every tool outcome quoted above is the counter
wrapper's `rc` field in `results.jsonl`, captured per run.

The variants are rebuilt from the pinned `pristine.sh` by the counter's own `apply_edits`; the
exact edit strings and witness vectors are the JSON in §3.2-§3.4. `probe.py` imports the counter
read-only from the lane path (`sys.dont_write_bytecode = True`) and is the only script written for
this probe.

## 7. Files (all under the scratch root unless noted)

- `probe.py`, `results.jsonl` (78 records), `logs/*.log`, `logs/*.exit`, `clone_rc.txt`,
  `checkout_rc.txt`, `lane_head.txt`.
- `tool.py`, `pristine.sh` (pinned extracts), `mutated-assigned.sh`, `variantA-rootkeyed.sh`,
  `variantA-control.sh`, `variantB-nsetupkeyed.sh`, `adv-kill-auditroot-sniff-arm-swap.sh`,
  `adv-accept-autokeep-gap-arm-swap.sh`, `fam-swap-0-2.sh`, `fam-swap-1-2.sh`,
  `fam-rotate-all.sh`, `fam-cosmetic-respace.sh`, `work/**` (per-run sandboxes).
- Report: `.ufo/waves/round-34/w1/Mutkillvectorarmswap.md` (fleet tree; the one sanctioned write).
