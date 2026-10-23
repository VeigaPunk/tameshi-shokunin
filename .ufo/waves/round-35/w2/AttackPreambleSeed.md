# AttackPreambleSeed — round-35 w2 (preamble seeding vs the A4 root witness)

Seat: `tameshi-r35-w2-AttackPreambleSeed` (leaf mutation-tester, godspeed). Dispatch pin
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/AttackPreambleSeed/`
(`lane/` is an attempt-1 leftover at `d16f9b5` and lacks the pin object; I did not mutate it —
`git cat-file -t 7da6e07` there is `fatal: could not get object info`. I cloned `lane-pin/` at the pin:
clone exit 0, `git rev-parse HEAD` = `7da6e076…e5b`). No writes outside scratch except this report.
No installs (python 3.14.8, bash 5.3.20 already present; pacman untouched).

Frozen bytes used (all re-hashed in `lane-pin/` and by `git show REV:`):

| artifact | sha256 | contract pin |
|---|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | same |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | same |

**Report-time lane drift (read-only observation, §9):** while this wave ran, the live lane advanced —
commit `f9df589` (A6) re-pinned the counter's `TOOL_SHA256`, and the worktree carries uncommitted A7 +
root-shape edits (tool `55601416a193…`, counter `4b383090903e…`; the worktree changed twice during my
read-only checks). **All verdicts below are for the dispatch-pin bytes in the table above.** §9 records
what the live snapshot changes: the §2 shape class is closed there by another seat's in-flight fix; the
§1 preamble class and the §3 literal regression are still accepted.

Baseline health: `python3 -I tools/tally-audit-v3.py --runner work/pristine.sh` → exit 0,
`CHECK runtime PASS vectors=30316 mismatched=0`, `CHECK harness PASS reference cases=9; faults rejected=34/34`,
`TALLY_AUDIT: PASS`, stdout sha256 `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82`.
**Every v3 run in this report that says PASS printed that exact sha256 and exit 0** (receipts under
`receipts/v3-*.out`), i.e. the tool cannot tell any of the copies below from the pristine runner.

Claim lines attacked: `contract.json:26` clause (4) (“the auto triples run with the runner's REAL auto root
… so a copy keyed on the real root value is observable”, amendment A4 at `contract.json:100-116`) and
`contract.json:27-28` (“kills every kill specimen … accepts every accept specimen”). The assigned class is
round-34 `ResiduePreambleSeeding` (`.ufo/waves/round-34/w1/ResiduePreambleSeeding.md` §2/§3.4, F1).

---

## 1. The assigned class against v3: a head-local seed/rename is still unaudited

`run_regression`'s head is everything before `local nlegs=` (`mutate-and-run.sh:1432`). `auto` is declared
at `:1357` and set at `:1361`; `KEEP` defaults at `:190`; `root` is built at `:1360`. The block reads
`$auto`/`$KEEP`/`$root` at `:1464` (the workdir-removal branch). v3 audits the *block* only:
`check_head` (`tally-audit-v3.py:432`) counts `st_*` leg names; the runtime driver *declares the block's free
variables itself* at `:390` (`local root=%s auto=%s KEEP=%s`) and never executes the head. So the head can
seed or rename those three names freely.

Mutants were built from the pinned bytes with asserted-unique anchors; the block is byte-identical in all
three (v3's own `regression_body`/`tally_block` used to check, block sha256
`e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`):

```
A-rename.sh   sha256 c915eedd0ffb4af018c51483ec0ca975a8171c8fb0bfd81a649e1354cadf0418
  -  local root specs auto=0        +  local root specs autodirs=0      (:1357)
  -    auto=1                       +    autodirs=1                     (:1361)
B-rootseed.sh sha256 973e226f2cc8201831af8441214500cfd585e7e3d58c2c44db73cabc47b1363b
  +  root=/tmp/tameshi-r35-preamble-seed        (inserted immediately before `local nlegs=`)
E-keepseed.sh sha256 9851a418c8e69e20d0ed6cb776d1b316a585ef29fdd090aa997a211d1c3f5824
  +  KEEP=1                                     (inserted immediately before `local nlegs=`)
```

Detector (same bytes, three copies):

| copy | v3 exit | v3 stdout sha | v2 exit | v2 stdout sha |
|---|---|---|---|---|
| `A-rename` | **0** | `46746e2b…4e82` | 0 | `e9444d03…e0f0` |
| `B-rootseed` | **0** | `46746e2b…4e82` | 0 | `e9444d03…e0f0` |
| `E-keepseed` | **0** | `46746e2b…4e82` | 0 | `e9444d03…e0f0` |

### 1.1 Ground truth A (rename): both runner configs die on the PASS path

Real `run_regression` bytes, only the leg *source* stubbed (`regression_case_git()` at
`mutate-and-run.sh:1332` replaced by `return 0`; `run_regression` itself byte-identical, block identical).
Command shape: `bash gt/<case>/tools/mutate-and-run.sh --regression [--workdir DIR]`.

| config | pristine stub (`afbbc4be…`) | A rename stub (`5cf2e64d…`) |
|---|---|---|
| default (`auto=1,KEEP=0`) | rc **0**, `PASS (cases=9 passed=9…)` + `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.zKaCrK (removed on PASS…)` | rc **1**, prints `PASS` then stderr `…/mutate-and-run.sh: line 1455: auto: unbound variable`; **no workdir line; root `fIkXb5` left behind** |
| `--workdir DIR` (`auto=0`) | rc **0**, `PASS` + `…/wd-pristine.pass (kept)` | rc **1**, prints `PASS` then the same `auto: unbound variable`; **no workdir line** |

This is not an equivalent mutant: under both real configs the copy prints a green PASS and then exits 1
(`set -u` at `:175`; read site `:1464`), and the default config leaks the workdir. From the runner's own
bytes: a driver that seeds `root` and `KEEP` but omits `auto` reproduces it for the *pristine* block —
stdout `REGRESSION: PASS …`, `RC=1`, stderr `auto: unbound variable` — proving the head is the only supplier
of the variable the block reads.

### 1.2 Ground truth B (root seed): both configs name a nonexistent workdir; PASS path deletes a fixed path and leaks the real one

Real runner, real leg source (no stub), `--regression`:

| config | pristine (`a7d3f2dd…`) | B (`973e226f…`) |
|---|---|---|
| default (legs SETUP in scratch) | rc 2 `SETUP (cannot-verify=9)`; `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.3VYdPY (kept)`; that root exists | rc 2 `SETUP`; names `/tmp/tameshi-r35-preamble-seed (kept)` — **that path does not exist**; real root `Jl45Zk` exists and is unreported |
| `--workdir DIR` | `REGRESSION_WORKDIR: …/wd-B-rootseed.real (kept)`; DIR exists | names `/tmp/tameshi-r35-preamble-seed`; DIR exists, unreported |

PASS path (leg source stubbed to all-pass, `run_regression` verbatim): pristine rc 0, `(removed on PASS)`
for the real mktemp root and removes it. B rc 0, prints
`REGRESSION_WORKDIR: /tmp/tameshi-r35-preamble-seed (removed on PASS; --keep retains)` and `rm -rf`s **that
path**: a canary planted at `/tmp/tameshi-r35-preamble-seed/canary` is **deleted** (`seed_alive=False`),
while the real root `/tmp/tameshi-r4-2-regression.jWuaTg` is **left behind** (`leaked_roots=[('/tmp/tameshi-r4-2-regression.jWuaTg', True)]`).
With `--workdir DIR` the same copy prints the fixed path `(kept)` instead of DIR. One added head line; the
block is byte-identical.

### 1.3 Ground truth E (KEEP seed): silent workdir leak on the default PASS path

Stub all-pass, default config: pristine rc 0, `(removed on PASS…)`; E rc 0, prints `(kept)` for the real
root and **does not remove it** (`hCHAEz` exists after the run). Explicit `--workdir` config is unchanged
(both keep). One config changed — a weaker seed than B, included for completeness.

**Verdict for §1: CRITICAL (false-accept of a real regression), exactly the round-34 class, still open.**
v3's head/static/runtime/harness all PASS on all three copies, with stdout byte-identical to pristine. The
round-34 routing asked for “a head-definition coverage check (every non-leg name the block reads must be
declared/assigned before the block)” — v3 did not adopt it; the runtime shim still supplies `auto`, `KEEP`
and `root` from outside.

---

## 2. Reopening A4 at one level deeper: the simulated auto root has the wrong *shape*

A4 replaced the fixed literals with a real `/tmp` directory carrying the prefix
(`tally-audit-v3.py:354-369`), but the directory is made by **Python** `tempfile.mkdtemp`
(`:365`): suffix **8 chars, lowercase+digits+underscore**. The runner's root is
`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` (`mutate-and-run.sh:1360`): suffix **6 chars,
mixed case**. Measured with this host's tools:

```
python3 tempfile.mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')
  -> /tmp/tameshi-r4-2-regression.8bj6xeaj   suffix_len 8
mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX
  -> /tmp/tameshi-r4-2-regression.WFoDGT     suffix_len 6
```

So a copy keyed on the *real root's shape* (`??????` = exactly six characters after the dot) is invisible to
every v3 config and **fires on the real runner's default config**:

```
C1-shape-mask.sh   sha256 cbf9ba87c05d9288b7a04f8d18f1f41eb32e6eb7d898db0b98bdb5c712dd4308
  +  if [[ $auto -eq 1 && "$root" == /tmp/tameshi-r4-2-regression.?????? && $nfail -gt 0 ]]; then
       nfail=0; npass=$((npass+1)); fi                       (one line, before the FAIL guard)
C2-shape-forced.sh sha256 56877a81b20387116c2f8ad1d41a8e020551a5d82ba8a1b7bf16174f5d4ecb0d
  +  if [[ $auto -eq 1 && "$root" == /tmp/tameshi-r4-2-regression.?????? ]]; then
       npass=$nlegs; nfail=0; nsetup=0; fi                    (one line, same place)
```

| detector | C1 | C2 |
|---|---|---|
| `python3 -I tools/tally-audit-v3.py --runner …` | **exit 0**, `runtime PASS vectors=30316 mismatched=0`, `TALLY_AUDIT: PASS` | **exit 0**, same PASS |
| `python3 -I tools/tally-audit-v2.py --runner …` | exit 0 PASS | exit 0 PASS |
| frozen counter `behavior`/`diverge` vs pristine (all four triples) | `divergent_configs=[]` → labelled accept/identical | `divergent_configs=[]` → labelled accept/identical |

**Ground truth, real root vs the audit's shim.** Same pristine block, same vector, driver root is the only
difference:

```
REAL  /tmp/tameshi-r4-2-regression.5L44mo   (6 chars)
  pristine: RC=1  FAIL (cases=9 passed=8 failed=1 setup=0) + WORKDIR … (kept)
  C1      : RC=0  PASS (cases=9 passed=9 …)               + WORKDIR … (removed on PASS; --keep retains)
SHIM  /tmp/tameshi-r4-2-regression.48b1mtdj (8 chars, v3's auto_root)
  pristine: RC=1  FAIL … (kept)
  C1      : RC=1  FAIL … (kept)          identical to pristine
```

End-to-end with the real runner's root construction and one deliberately failing leg (leg source stubbed;
`run_regression` verbatim):

```
pristine.onefail        rc=1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)   leaked root /tmp/tameshi-r4-2-regression.5IOesb
C1-shape-mask.onefail   rc=0  REGRESSION: PASS (cases=9 passed=9 …)                 no leaked root (removed on PASS)
```

C2 is stronger: with the **real, unstubbed leg source** in scratch all nine legs are `SETUP`
(`pristine.real` rc 2 `SETUP (cannot-verify=9)`, workdir kept). C2 turns that into rc 0
`PASS (cases=9 passed=9 …)` and deletes the workdir — “cannot verify” → green. It does so for any
fail/setup mix as well, since it sets all three counters.

**Contrast proving the residual is exactly the *shape*, not the root axis**: the two A4 panel copies that
gate on the prefix (`/tmp/tameshi-r4-2-regression.*`, `panel/root-keyed-auto-mask.json`,
`panel/root-keyed-auto-zero.json`) are both killed by v3 (exit 1, `CHECK runtime FAIL`), and v3's own
selftest seeds the same prefix form (`tally-audit-v3.py:789`). Only the six-character shape is unswept.

**Verdict: CRITICAL.** `contract.json:26` clause (4) says a copy keyed on the real root value is observable.
It is not: a one-line, block-side, real-regression copy (A4's own routed class, masked failure → PASS, or
SETUP → PASS) is accepted with `runtime PASS, mismatched=0`, and the frozen counter's ground truth — which
builds the same 8-char root at `c1-measure.py:67` — also sees no divergence. Fix direction: build the auto
root with the runner's own construction (`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`) or force the
suffix shape (6 mixed-case bytes) in both the tool and the counter; add a shape-keyed kill copy to the panel.

**Status at report time: CLOSED in the live worktree (not at the pin, not by this seat).** The uncommitted
live tool (`55601416…`) changed `auto_root` to generate the runner's exact six-alphanumeric mixed-case shape
(comment attributes it to wave-2 seat `ScoutRunnerConfigs`); re-running my copies against a scratch snapshot
of those bytes kills both C1 and C2 (`exit 1`, `runtime FAIL mismatched=1800`, first mismatch
`cfg(1,0) statuses 1 0 0 0 0 0 0 0 0`), and the live counter (`4b383090…`) now reports
`divergent=[(None,'1','0'), (None,'1','1')]` for each. The pin-scoped reproduction above remains the proof
that the dispatch bytes were blind, and the panel still has no shape-keyed copy: **add one** so the fix
cannot regress.

---

## 3. v2 → v3: a class v2 killed and v3 now accepts

v2's CONFIGS (`tally-audit-v2.py:265`) contain the literal root `/tmp/tally-audit-work`; v3's
(`tally-audit-v3.py:349-350`) replaced it with the real auto root and `tally-audit-explicit`. A copy gated
on `/tmp/tally-audit-work` therefore loses its only witness in v3 — while that exact string is still a
legitimate caller-supplied `--workdir` under which `auto=0` and the block reads `$root` verbatim.

```
D-oldliteral.sh  sha256 8e9feb4956b357cb9666c5922ea89a3129186dc1eda2a0990e9cd3d2a2924cec
  +  if [[ "$root" == /tmp/tally-audit-work && $nfail -gt 0 ]]; then nfail=0; npass=$((npass+1)); fi
     (one line, before the FAIL guard; head byte-identical to pristine)
```

| detector | result |
|---|---|
| v3 | **exit 0**, `CHECK runtime PASS vectors=30316 mismatched=0`, `TALLY_AUDIT: PASS` (receipt `receipts/v3-D-oldliteral.out`) |
| v2 | **exit 1**, `CHECK runtime FAIL vectors=15158 mismatched=900; first: cfg(1,0) statuses 1 0 0 0 0 0 0 0 0: got (0, 'REGRESSION: PASS (cases=9 passed=9…)'), want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')` (receipt `receipts/v2-D-oldliteral.out`) |

Ground truth for the real invocation (`--workdir /tmp/tally-audit-work`, one failing leg through the stubbed
leg source; `run_regression` verbatim):

```
pristine.onefail   rc=1  REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)  WORKDIR: /tmp/tally-audit-work (kept)
D-oldliteral       rc=0  REGRESSION: PASS (cases=9 passed=9 …)                WORKDIR: /tmp/tally-audit-work (kept)
```

The mutant fires only for that workdir string (it is inert under the real auto root and under
`tally-audit`/`tally-audit-explicit`), so this is narrow — but it is a genuine real-behavior change on a
valid invocation, v2 caught it, and v3 does not.

**Verdict: CRITICAL by the dispatch rule (“a class v2 caught and v3 now accepts is a CRITICAL regression”).**
Fix direction: add `('/tmp/tally-audit-work', '0', '0')` (or sweep a small set of absolute caller workdirs)
to v3's CONFIGS; in general, do not delete a simulated literal without replacing its witness when that
literal remains a real invocation.

---

## 4. Adjacent apparatus defect — real at the pin, RESOLVED upstream during this wave (A6)

The frozen counter's own tool pin was stale relative to A4. At `7da6e07`:

```
git show 7da6e07:tools/tally-audit-v3.py | sha256sum
  -> ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885
c1-measure.py:46  TOOL_SHA256 = 'da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f'  # pre-A4 bytes at d16f9b5
c1-measure.py:374 tool_sha_ok = tool_bytes is not None and (a.tool is not None or tool_sha == TOOL_SHA256)
```

`contract.json` A4 `pins_new.tool_sha256` is `ef98fc53…`, so a deciding-mode run at any rev ≥ the amendment
prints `tool_sha_ok=0` and `C1_R35_PASS=false` before any specimen is scored (the control mode with
`--tool` bypasses the check, which is why the v2 control receipts look healthy). I did **not** invoke the
counter's deciding mode (kill rule respected); the equality is computed directly from the committed bytes.
Fix is one constant; it is pre-data and must land before the deciding run. I did not touch the file.

**Resolved before this report landed:** commit `f9df589` ("A6 — counter TOOL_SHA256 re-pinned to the A4 v3
bytes (caught pre-data by wave-2 seat CriticPredicate)") sets the constant to `ef98fc53…`, so at REV
`7da6e07` the deciding check would now pass. This section is a corroborating pin-scoped observation, not an
open finding. Note for the L1: the live worktree tool is `55601416…` (A7 + root-shape); if that is committed,
the counter must be re-pinned again before the deciding run.

---

## 5. Why a green C1 would not catch any of this (the limit, stated as coverage)

The frozen counter's ground truth is behaviour of the *extracted block* under its four triples
(`c1-measure.py:52-68,163-217`). For every copy in §1-§3 it returns `divergent_configs=[]` (measured by
importing the frozen module and calling `behavior`/`diverge` on the commit bytes; no counter mode run):

```
AT PIN (tool ef98fc53 / counter 515b0b1b):
  A-rename []   B-rootseed []   E-keepseed []   C1-shape-mask []   C2-shape-forced []   D-oldliteral []
  counter auto_root: /tmp/tameshi-r4-2-regression.6mprqg1c  suffix_len 8   -> all six accept/identical
LIVE SNAPSHOT (counter 4b383090…, root shape fixed by the in-flight amendment):
  A-rename []   B-rootseed []   E-keepseed []   D-oldliteral []      -> still accept/identical
  C1-shape-mask [(None,'1','0'),(None,'1','1')]   C2-shape-forced [(None,'1','0'),(None,'1','1')]
  counter auto_root: /tmp/tameshi-r4-2-regression.tKRBW7  suffix_len 6
```

So, at the pin the apparatus cannot author any of them as a sealed *kill* (the kill rule requires divergence
under one of its own triples) and would score them accept/identical. The live root-shape fix makes C1/C2
authorable as kills, but the head-seeded copies (A/B/E) and the literal-keyed copy (D) remain invisible to
the counter even after it. That is the precise reason the tool can be green while accepting them: the
claim's “kill specimen” is block-defined, while the tool's object is the runner. The finding is still
CRITICAL in the dispatch's sense (v3 accepts a real regression), but the C1 *predicate over its own
specimens* is not literally contradicted — the guarantee is narrower than “audits the runner's --regression
behaviour”, which is what clause (4) advertises. Seal seats cannot close the head-seeded class by authoring;
it needs a tool/counter head check.

---

## 6. What I could NOT break (bounded negatives, with the proof)

- **Block-side prefix root gate (the A4 panel class)**: `panel/root-keyed-auto-mask.json` and
  `panel/root-keyed-auto-zero.json` applied to pristine both give v3 **exit 1**,
  `CHECK runtime FAIL`, `TALLY_AUDIT: FAIL` (copies `work/panel-root-keyed-auto-mask.sh` sha
  `eff823b52779110a…`, `…auto-zero.sh` `62bdbb10ff5fcf05…`). A4's prefix witness works; only the shape is open.
- **Full-stdout comparison is live**: `ctl-workdir-line` (block text `(removed on PASS; --keep retains)` →
  `(dropped)`, one occurrence) → v3 exit 1, `runtime FAIL mismatched=10` (cfg(1,0)), while v2 exits 0 /
  identical stdout. So the r33/r34 second-line class is genuinely closed by v3 and this is a live-detector
  control, not merely a code reading.
- **Head leg-variable axis is live**: `ctl-head-assign` (insert `st_js=0` after `st_js=$?`) → v3 and v2 both
  exit 1, `CHECK head FAIL … non-bare leg assignment(s) … st_js appears 3 times`. The head check works for
  the leg names; it simply has no rule for `auto`/`KEEP`/`root`.
- **Block-side four-config sweep / comment classes / harness faults**: not re-litigated here (other seats
  own the panel and the selftest); I did not run `--selftest` or the other six panel copies, and make no
  claim about them. The pristine audit itself is healthy (30316 vectors, 0 mismatches; 34/34 faults).
- **v2 is not stronger in general**: v2 accepted A, B, C1, C2 and E (all exit 0, sha `e9444d03…`), so only D
  is a v2-caught/v3-accepted class in this slice. v3's full-stdout and four-config work is real (above).
- **Byte-pins**: all four artifacts hashed at REV match the contract; the runner is byte-identical
  throughout (no runner edit was made or proposed).

---

## 7. Ranking and fix directions

Status column is at the dispatch pin; §9 gives the live worktree re-run.

1. **CRITICAL at pin — preamble seeding still unaudited** (§1, **still open in the live snapshot**): rename/
   seed of `auto`, `root`, `KEEP` in the head; real regressions in both configs (A/B); v3 stdout
   byte-identical to pristine. Live tool `55601416…` still returns PASS on A, B, E. Fix: head-coverage check
   (every non-leg name the block reads must be declared/assigned in the head) or execute the head with the
   block; round-34 F1's recommendation, still not adopted.
2. **CRITICAL at pin — v2→v3 regression** (§3, **still open in the live snapshot**): v2 kills the
   `/tmp/tally-audit-work` key, v3 (and the live A7 tool) accepts; real for `--workdir /tmp/tally-audit-work`.
   Fix: restore that literal as an explicit config.
3. **CRITICAL at pin — A4 reopened by root shape** (§2, **CLOSED in the live worktree** by the in-flight
   six-char `auto_root` fix attributed to ScoutRunnerConfigs; live tool kills C1/C2, live counter diverges).
   Keep the finding as the pin-scoped proof; add a shape-keyed panel copy so the fix is regression-tested.
4. **RESOLVED upstream — counter `TOOL_SHA256` stale** (§4): fixed by A6 (`f9df589`) before this report
   landed; remains a caution to re-pin if the A7/shape tool is committed.
5. **BOUND** (§5): the counter's block-level ground truth shared the shim at the pin; after the live root
   fix it still cannot see head-seeded or literal-keyed copies (A/B/E/D `divergent=[]`), so a green C1 is not
   evidence those classes are closed. This is the limit, not a defect fixable by authoring.

## 8. Restoration, hygiene, repro

- `work/pristine.sh` sha256 = `a7d3f2dd…912eb9` after every probe; `cmp` against
  `git show 7da6e07:tools/mutate-and-run.sh` bytes = **True**; v3 re-run on it at the end: exit 0,
  stdout sha `46746e2b…4e82`, identical to the first run (`receipts/v3-pristine-restored.out`).
  Mutants are separate files; no pinned artifact was edited in place, so nothing needed restoring.
- `lane-pin/` HEAD `7da6e07…`, `git status --porcelain` empty. Tool bytes untouched.
- Installs: none; pacman never invoked.
- Scratch-only side effect disclosed: default-config runner runs were cleaned by diffing
  `/tmp/tameshi-r4-2-regression.*` around each run; a concurrent seat's 8-char tool shim created during a
  run could have been included in that diff and removed (the tool recreates it via `auto_root()` on demand;
  no divergence is expected because the block deletes its own root on PASS anyway). Explicit workdirs were
  created under scratch or the exact `/tmp/tally-audit-work` literal and removed after.
- Repro (scratch root; all paths absolute):

```
S=/fast/scratch/hyaku/tameshi-r35-seats/AttackPreambleSeed
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
git clone -q --no-hardlinks "$L" $S/lane-pin && git -C $S/lane-pin checkout -q --detach 7da6e07…
sha256sum $S/lane-pin/tools/{tally-audit-v3.py,tally-audit-v2.py,mutate-and-run.sh}
# rebuild the seven copies exactly as §1-§3 (separate files under $S/work; anchors in the text above)
for c in pristine A-rename B-rootseed C1-shape-mask C2-shape-forced D-oldliteral E-keepseed; do
  python3 -I $S/lane-pin/tools/tally-audit-v3.py --runner $S/work/$c.sh; echo "v3 $c exit=$?"
  python3 -I $S/lane-pin/tools/tally-audit-v2.py --runner $S/work/$c.sh; echo "v2 $c exit=$?"
done
# ground truth: bash $S/gt/<case>/tools/mutate-and-run.sh --regression [--workdir DIR]
# (PASS-path cases use the leg-source stub: regression_case_git() { return 0; } — run_regression verbatim)
# shim split: run each block with local root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX) auto=1 KEEP=0
# vs root=$(python3 -c 'import tempfile;print(tempfile.mkdtemp(prefix="tameshi-r4-2-regression.",dir="/tmp"))')
```

Receipts: `$S/receipts/v3-*.out`, `$S/receipts/v2-*.out`, `$S/gt/*.out|*.err`. Key hashes: v3 PASS stdout
`46746e2b…4e82`; v2 pristine `e9444d03…e0f0`; v2 D-kill `1c20a857ae4f7310f6fd75f459e4c04d8e99802a2ec6e30fa92fc646e528e88e`;
copies `a7d3f2dd`(pristine) / `c915eedd`(A) / `973e226f`(B) / `cbf9ba87`(C1) / `56877a81`(C2) /
`8e9feb49`(D) / `9851a418`(E); blocks byte-identical `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`
for A/B/E.

---

## 9. Lane drift at report time — live worktree re-run (read-only snapshot)

The live lane is being amended concurrently. What I observed (read-only; I wrote nothing in the lane):

- commit `f9df589` — A6: counter `TOOL_SHA256` → `ef98fc53…` (fixes §4; caught independently by
  wave-2 seat CriticPredicate); commit `68f2557` re-ran the before/control receipts.
- uncommitted worktree edits: v3 tool (`55601416a193a2e9c15f17aa45d6a6b6f24651f9dc55b145f68471f614337a4b`
  at the snapshot) adds the last-`local nlegs=`/depth-0 extraction (AttackPerIndexParse), the head
  non-assignment mention rule (SealKillHeadRead), and the **six-char mixed-case `auto_root`** fix;
  counter (`4b383090903e7837326eb1cb9934737ed52e09af8b4a737ac6e061a286bdc70d`) adds A7 (`unsafe_block`
  root/`rm -rf` gate) and the same root-shape fix. The worktree hash changed twice while I was reading it.

Copies of those bytes were taken to scratch (`work/live-v3-55601416a193.py`,
`work/live-c1-4b383090903e.py`) and the same seven copies were re-run (receipts `receipts/live/*.out`):

| copy | live v3 `55601416…` | live counter `4b383090…` |
|---|---|---|
| pristine | exit 0 PASS | — |
| A-rename | **exit 0 PASS** (`46746e2b…`) | `divergent=[]` |
| B-rootseed | **exit 0 PASS** (`46746e2b…`) | `divergent=[]`, `unsafe_block=None` |
| E-keepseed | **exit 0 PASS** (`46746e2b…`) | `divergent=[]` |
| C1-shape-mask | **exit 1** `runtime FAIL mismatched=1800`, first `cfg(1,0)` one-fail | `divergent=[(None,'1','0'),(None,'1','1')]` |
| C2-shape-forced | **exit 1** `runtime FAIL mismatched=1800` | same two configs |
| D-oldliteral | **exit 0 PASS** (`46746e2b…`) | `divergent=[]` |

So the live snapshot closes §2 (shape) and leaves §1 (preamble: A/B/E) and §3 (literal: D) fully open.
Because the worktree is mutable, these are snapshot results, not a verdict at a commit. The L1 should:
(1) commit the A7/shape tool, (2) re-pin the counter's `TOOL_SHA256` to the new blob **and** update the
contract pins in the same commit, (3) add one shape-keyed kill copy to the panel so the fix is
regression-tested, and (4) re-run the seven copies above at the committed revision to confirm the split.

