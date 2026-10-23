# Round-35 w1 — RevengerRootShape

Seat: `tameshi-r35-w1-RevengerRootShape` (leaf revenger, godspeed). Lane pin at dispatch:
Frozen C1 counter `.ufo/evidence/round-35/c1/c1-measure.py` (per contract:
`78bb43ebf3d2a313951d9d89f470f2543023b1605326fe676eef3cdb7a947ef9`) read, not re-hashed.
Frozen bytes used (clone-verified sha256): runner `tools/mutate-and-run.sh`
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; tool
`tools/tally-audit-v3.py` `da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f`;

Slice assigned: **witness-shim root fidelity** — reverse-engineer the real runner's root values
(`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` vs `--workdir DIR`), attack v3's fixed root
strings, build a copy gated on the real root shape, and report whether the tool accepts a
divergent copy.

All scratch under `/fast/scratch/hyaku/tameshi-r35-seats/RevengerRootShape/` (lane checkout
read-only; no git mutations, no writes under `/home/vgpnk/Projects/shokunin/` except this report).
No tool installs (nothing needed; pacman untouched).

---

## 1. The real runner's root values (reverse-engineered)

`run_regression` constructs the root at `tools/mutate-and-run.sh:1357-1365`:

```bash
local root specs auto=0
FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")
if [[ -z "$WORKDIR" ]]; then
  root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX) || die_setup 'mktemp -d failed'
  auto=1
else
  root=$WORKDIR
  mkdir -p "$root" || die_setup "cannot create workdir: $root"
fi
```

- **auto=1** (runner's default, no `--workdir`): `root` is an absolute path under `/tmp` with
  basename prefix **`tameshi-r4-2-regression.`** + 6 random chars. Verified live with the pinned
  runner (scratch lane; legs SETUP on missing fleet repos — expected and irrelevant to the root):
  - `bash tools/mutate-and-run.sh --regression` → printed
    `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.Yl90i6 (kept)`, exit 2 (SETUP).
- **auto=0** (`--workdir DIR`): `root` = the caller's string verbatim (absolute or relative).
  Verified: `bash tools/mutate-and-run.sh --regression --workdir /tmp/r35-explicit-root-K` →
  `REGRESSION_WORKDIR: /tmp/r35-explicit-root-K (kept)`, exit 2.

## 2. What v3 simulates (the shim)

`tools/tally-audit-v3.py:340-341`:

```python
CONFIGS = (('tally-audit', '0', '1'), ('/tmp/tally-audit-work', '1', '0'),
           ('tally-audit-explicit', '0', '0'), ('/tmp/tally-audit-work-keep', '1', '1'))
```

`run_vectors` (line 358) drives each tally block with `local root=<literal> auto=<x> KEEP=<y>`
— a **fabricated root literal**, never the runner's real root construction. None of the four
literals can ever equal a real auto root (`/tmp/tameshi-r4-2-regression.*`; the two `/tmp`
literals use a different prefix, the two others are relative). `grep -F tameshi-r4-2-regression`
over the frozen v3 tool **and** the frozen C1 counter returns **no matches** — the real root
template exists nowhere in the measurement apparatus. The same fixed literals are duplicated in
`c1-measure.py:46-47` and its `run_block` (lines 136-160), so the deciding counter shares the
shim exactly.

## 3. Attack: a copy gated on the real root shape

Mutant built from the pinned runner bytes (one insertion after the tally loop, before the FAIL
guard; comment-blanked structural scans see no change, the gate is a runtime-only divergence):

```bash
if [[ $auto -eq 1 && "$root" == /tmp/tameshi-r4-2-regression.* ]]; then nfail=0; npass=$((npass+1)); fi
```

- `work/mutant-B-mutate-and-run.sh` sha256 `0c033fbd9537433f57780525d64297606e2f6354045f6521a29fa75490afe6cc`
  (pristine copy `work/pristine-mutate-and-run.sh` sha256 `a7d3f2dd…912eb9` = PIN_RUNNER).

**The tool accepts it (false-accept):**
```
python3 tools/tally-audit-v3.py --runner work/mutant-B-mutate-and-run.sh
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
EXIT=0
```
Baseline on pristine: same `TALLY_AUDIT: PASS`, `EXIT=0` (runner sha pinned). The audit ran
30,316 vectors × 4 configs + stress and saw **zero** divergence.

**But the copy diverges under the real runner's default root.** Driving the identical tally
blocks in the audit's own harness (same script shape, same env, only the root literal replaced by
a real `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` result):

| context | vector | pristine | mutant |
|---|---|---|---|
| REAL auto root | 1 failing leg | exit 1 `FAIL (cases=9 passed=8 failed=1 setup=0)` | **exit 0 `PASS (cases=9 passed=9 …)`** |
| REAL auto root | 1 fail + 1 setup | exit 1 `FAIL` | **exit 2 `SETUP (cases=9 passed=8 cannot-verify=1)`** |
| audit root (1,0) `/tmp/tally-audit-work` | 1 failing leg | exit 1 FAIL | exit 1 FAIL (identical) |
| audit root (1,1) `/tmp/tally-audit-work-keep` | 1 failing leg | exit 1 FAIL | exit 1 FAIL (identical) |
| audit root (0,1) `tally-audit` | 1 failing leg | exit 1 FAIL | exit 1 FAIL (identical) |
| audit root (0,0) `tally-audit-explicit` | 1 failing leg | exit 1 FAIL | exit 1 FAIL (identical) |
| REAL explicit `--workdir` root (auto=0) | 1 failing leg | exit 1 FAIL | exit 1 FAIL (identical; gate requires auto=1) |

Under the real default `--regression` run, a failing leg is masked into a full PASS (exit 0,
workdir removed) — a silent kill-rate-masking defect — while the frozen v3 audit blesses the copy
(`TALLY_AUDIT: PASS`, exit 0). A weaker variant zeroing only `nfail` (mutant-A,
`850c5de8598a4a13cb06d8564e4059c75823dd9840aa359ab10f92fc1f51d723`) is also accepted PASS and
diverges real-root FAIL → SETUP.

## 4. Ranking

- **CRITICAL — false-accept, non-fail-closed (round-34 witness-shim fidelity class, still open).**
  v3 completed the (auto,KEEP) sweep count, but the four triples are simulated with fixed root
  literals that never match the runner's real root values. The claim's guarantee ("kills every
  kill specimen — divergent behavior under at least one of the four configs") is false for
  root-value-keyed constructions: a copy divergent under the runner's real default config is
  ACCEPTED. The frozen C1 counter shares the identical fixed-root shim, so this class is also
  invisible to the deciding measurement's ground truth (it would score this copy accept-by-counter
  and accept-by-tool). Fix direction: pin the witness to the runner's actual root construction —
  run the driver with `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` for the auto
  triples and with a representative real absolute `--workdir` value for the explicit triples
  (and audit that the copy under test does not rewrite the root construction itself).
- **BOUND — explicit-workdir side.** A gate keyed to absolute-vs-relative roots would be caught by
  the audit's (1,0)/(1,1) configs (their literals are absolute), so the explicit side admits no
  independent evasion; only the auto-side prefix is unreachable by the audit.
- **HYGIENE — `c1-measure.py:46-47` duplicates the fixed literals instead of importing them**
  from the tool; a fix to v3's shim must touch both to stay in lockstep.

## 5. What I could NOT break (with proof)

- The four-triple sweep count and full-stdout comparison behave exactly per reference on pristine
  (30,316 vectors × 4 configs, 0 mismatches; `EXIT=0`), and the REGRESSION_WORKDIR kept/removed
  wording distinctions are exercised under every config.
- The `head`/`static`/`harness` checks: untouched by the gate and still PASS on the mutant; a
  root-gate copy cannot hide from them (they are orthogonal to the root axis).
- The real auto root could not be observed through a full green `--regression` run in this
  environment (fleet sibling repos are outside the lane; legs SETUP), so the verdict-level proof
  uses the audit's own driver with the runner's real root construction — the minimal and exact
  axis of the shim.

Evidence trail: commands, exit codes and byte identities above; all artifacts under
`/fast/scratch/hyaku/tameshi-r35-seats/RevengerRootShape/work/` (mutant-A/B, pristine copy).
