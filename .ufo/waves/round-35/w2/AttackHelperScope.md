# AttackHelperScope — round-35 w2 mutation seat

Seat: `L1tameshi35.AttackHelperScope` (leaf, godspeed; depth limit 3, no dispatch).
Lane pin at dispatch: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`; lane checkout is a detached
clone at that rev, never written (`git status --porcelain` = 0 lines before and after).
All scratch under `/fast/scratch/hyaku/tameshi-r35-seats/AttackHelperScope/`; all real-runner
workdirs under `/tmp`. No installs, no `pacman`, no mutating git/jj.

Assignment: reproduce the round-34 `ResidueHelperRefactor` class against v3 (top-level policy
helper, `nlegs` preserved, behavior changed under one config, tally block syntactically
pristine); name the exact class boundary with proof; then prove the limit with the cheapest copy
that changes real runner behavior while the tool still accepts; compare v2 vs v3 for a
v2-killed/v3-accepted regression.

## Verdict first

| # | mutant (sha256) | what it changes | v3 (this pin) | v2 (control) | counter `behavior()` | real runner |
|---|---|---|---|---|---|---|
| H2 | `f0465a64…076788` | top-level `regression_case_git`, 3 lines; **head+block byte-identical** | **PASS, exit 0** | PASS, exit 0 | `div=NONE` | default: **SETUP(0/9) → PASS(9/9), exit 2→0** |
| H1 | `c183ee52…9aa762` | top-level `tally_policy` + call in loop (round-34 v6) | **PASS, exit 0** | PASS, exit 0 | `div=NONE` | default: **SETUP(0/9) → PASS(9/9), exit 2→0** |
| H5 | `c6da1d3f…bb7008` | block gate on `${WORKDIR-}` | **PASS, exit 0** | PASS, exit 0 | `div=NONE` | explicit: **SETUP(0/9) → PASS(9/9), exit 2→0** |
| H6 | `42eeba27…6508fd0` | head `eval "st_$(printf js)=0"` | **PASS, exit 0** | PASS, exit 0 | `div=NONE` | default: SETUP passed=0→**1**, cannot-verify=9→**8** |
| H12 | `2cff23f6…3fbea31d` | block: `rm -rf "$root"` → `:` | **PASS, exit 0** | PASS, exit 0 | `div=NONE` | PASS stdout identical; workdir **kept vs removed** |
| **H3** | `f68cea97…ad3852c4` | block: verdict `\n` → `\x1f` (U+001F) | **PASS, exit 0, 30316/30316 ok** | **FAIL, exit 1, 15158/15158** | `div=NONE` (lossy) | stdout byte 0x0a→0x1f; `^REGRESSION_WORKDIR:` gone |
| H4 | `cd80a04a…b2fec20e` | block gate on `/tmp/tally-audit-work` (v2's retired literal) | PASS, exit 0 | FAIL, exit 1, 7579 | `div=NONE` | diverges only under `--workdir /tmp/tally-audit-work` |
| H7 | `c9106d0d…d63be79c` | same policy **inline** in the block (scope control) | **FAIL, exit 1, runtime 900** | FAIL, exit 1, 900 | `div=(1,0)` | same divergence |
| H8 | `c3c0665f…984f4c03` | counting loop moved to top-level `tally_legs()` | **SETUP, exit 2, no CHECK** | SETUP, exit 2 | `div=all four` (**label inversion**) | benign refactor: identical behavior |
| H9 | `eff823b5…35647cff2` | gate on real auto root shape (A4 witness) | **FAIL, exit 1, runtime 15158** | PASS, exit 0 | `div=(1,0),(1,1)` | masks under default run |
| H10 | `8c654bc7…813b57` | inert comment naming `st_js` | PASS, exit 0 | FAIL, exit 1 (head) | `div=NONE` | identical (intended v3 fix) |
| H11 | `d6c64469…387201` | NUL byte appended to PASS line | PASS, exit 0 | PASS, exit 0 | `div=NONE` | NUL emitted, stripped by `$()` |

Ranks: **CRITICAL** — H3 (v2 killed it, v3 accepts it, real stdout bytes differ; claim surface
"(2) FULL stdout" is false as implemented, and the frozen counter shares the lossy transport).
**BOUND** — H2/H1 (the ResidueHelperRefactor class, exact boundary below), H5 (A4 shim class on
an unmodeled runner global), H6 (head-check guarantee in the tool docstring is false), H8
(ground-truth label inversion / protocol hazard), H12 (workdir deletion is an unverified side
effect), H4 (retired v2 literal; **not** a real regression), H11 (NUL in transport).
**HYGIENE** — none beyond the above.

## 1. Pins, setup, and what was held fixed

Setup commands (exit 0 each):

```
mkdir -p /fast/scratch/hyaku/tameshi-r35-seats/AttackHelperScope
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r35-seats/AttackHelperScope/lane
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach 7da6e076…
```

Byte pins verified at the checkout (`sha256sum`, exit 0; `lane = .../AttackHelperScope/lane`):

| object | sha256 | expected |
|---|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` | contract `ef98fc53…` ✓ |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | contract ✓ |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | contract ✓ |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` | contract ✓ |
| `.ufo/evidence/round-35/c2/c2-measure.py` | `67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc` | contract ✓ |

`lane` HEAD = `7da6e076…`; `git status --porcelain | wc -l` = 0. `work/pristine.sh` is a byte
copy of the pinned runner (`a7d3f2dd…`). The tool bytes were used from `work/tool-v3.py` /
`work/tool-v2.py` (same sha), so even the lane file was never executed in place.

Mutants are separate files built from `work/pristine.sh` by `work/build.py`, `build2.py`, and
two inline builders; every edit asserts its exact occurrence count and the pristine sha before
writing; `bash -n` exits 0 on every mutant (`work/matrix/hygiene.txt` records the hashes).

Full mutant sha256 (all under `work/`):

```
h1-policy-call.sh    c183ee52af4731e71bdfaab8b57b19a90cd71e18b1f04e8dfaa060504b9aa762
h2-wrapper-gate.sh   f0465a64e21ec5c40065e510d25be76968ed6fd244518c7bbd2bbaa247076788
h3-sep-collision.sh  f68cea97cff64553d91a1f0d2fb13085228bddf9450cc433f0e7b56bad3852c4
h4-v2-literal.sh     cd80a04acebecfa8dcffb3e59d5af0d7abcf2af8b90874522136bbe7b2fec20e
h5-workdir-env.sh    c6da1d3f9f4af2ac301d152e7b6a19c74a118baf7a2514b97064d77641bb7008
h6-head-eval.sh      42eeba270c8e905c26d6f5be7d56f37cd541589330ada1c9012f741bc6508fd0
h7-inline-control.sh c9106d0d331028369099d1ef2ab8e0473f840e686d0642949ff46aabd63be79c
h8-loop-extract.sh   c3c0665fbde8829a10d466c8b8ab9cffe87ac3684792599979b8940a984f4c03
h9-root-shape.sh     eff823b52779110a7d6e43bb34bbb210b1054aace04bea7e345d13f35647cff2
h10-comment-names-leg.sh 8c654bc71aa5f4877ddec3a52ee458a2af6668aaaacca5f6cc0e812901813b57
h11-nul-byte.sh      d6c6446938b6836ba1bfb500ed09dc85f20d0b3fdb1d2defe281cb6251387201
h12-keep-workdir.sh  2cff23f641a2200776612bd6f84df1296baf03bcde7c1a4eb06d23773fbea31d
pristine.sh          a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
```

## 2. The ResidueHelperRefactor class against v3 — the exact boundary

### 2.1 What the oracle is allowed to see

v3's runtime check extracts exactly two slices of `run_regression`:
`head_section` (everything before `^[ \t]*local nlegs=`) and `tally_block` (from `local nlegs=`
to the function's final `}`) — `tools/tally-audit-v3.py:196-244`. It then executes **only the
block**, as a bash function, inside a fresh interpreter whose environment is
`{PATH, LC_ALL, HOME, TMPDIR}` plus three locals `root`, `auto`, `KEEP`
(`v3:335-348, 376-398`). The compared tuple is `(exit, decoded stdout)`; stderr is written to a
side file and never compared (`v3:379`). Consequences, by construction:

1. a **top-level definition** (helper) is not sourced — a call to it fails as
   `command not found`, on stderr, discarded;
2. the **head** is never executed at all (only scanned);
3. only `root`/`auto`/`KEEP` are supplied; every other runner global (`WORKDIR`, `SELF`,
   `FLEET_ROOT`, `MODE`, `BAND_*`, `TABLE_*`, …) is absent or different;
4. stderr, filesystem effects, and non-UTF-8/control bytes in stdout are not compared;
5. the runner's own harness is exercised only with **injected** reference/fault blocks
   (`v3:664-681`), never with the copy's own block.

The frozen counter has the same window: `behavior()` extracts (head, block) and `run_block()`
executes only the block under the same four triples (`c1-measure.py:163-185, 204-213`).

### 2.2 H2 — strongest form: the audited window is byte-identical

H2 edits `regression_case_git` (`tools/mutate-and-run.sh:1332-1343`), a top-level helper, to
return 0 after a failed leg when the runner's default state is active (dynamic scoping supplies
`run_regression`'s locals):

```sh
  local rc=$?
  [[ ${auto-0} -eq 1 && ${KEEP-0} -eq 0 ]] && return 0
  return $rc
```

Extraction proof (import of v3's own extractors, `work/matrix/hygiene.txt`):

| file | head sha256 | block sha256 |
|---|---|---|
| `work/pristine.sh` | `8b293fbe1794ebe81ae104b1e37f3be238de334c17bb12ab65761fdcff310d41` | `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d` |
| `work/h2-wrapper-gate.sh` | **identical** | **identical** |

So head, block, `nlegs`, operands, and every byte the tool or the counter can observe are the
pristine ones. The tool prints a full PASS (`CHECK head/static/runtime/harness PASS`,
`CHECK runtime PASS vectors=30316 mismatched=0`, `EXIT=0`); the counter's `behavior()` returns
`div=NONE` for all four triples (`work/gt.out`). Under the real runner:

```
$ bash work/h2-wrapper-gate.sh --regression
REGRESSION: PASS (cases=9 passed=9; …)                  exit 0
REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.J6JbzK (removed on PASS; --keep retains)
$ bash work/h2-wrapper-gate.sh --regression --workdir /tmp/ahs-wd2-h2
REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)    exit 2   (identical to pristine)
```

(Pristine default: `SETUP (cases=9 passed=0 cannot-verify=9)`, exit 2,
`work/real/E-pristine-__regression.exit` = 2.) The wrapper makes the runner's only default mode
(`--regression`, auto workdir, no `--keep`) unable to fail any leg, while every audited byte is
pristine. This is the round-34 class in its purest form: **the fault is entirely outside the
window the oracle executes.**

### 2.3 H1 — the round-34 v6 shape, config-gated

H1 adds a top-level `tally_policy()` and one call after the `case` inside the tally loop; the
helper converts status 2 (`SETUP`) to pass only when `auto=1 && KEEP=0`, preserving
`npass+nfail+nsetup == nlegs`. v3: exit 0, `runtime PASS vectors=30316 mismatched=0`;
v2: exit 0, `15158/15158 ok`; counter: `div=NONE`. Mechanism, measured with the tool's own
driver shape for one vector `2 0 0 0 0 0 0 0 0` (`work/mech2.out`):

```
pristine : RC=2 OUT=<<REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: … (kept)>>
           STDERR_LINES=0
h1       : RC=2 OUT=<<REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)\nREGRESSION_WORKDIR: … (kept)>>
           STDERR_LINES=9   first='bash: line 12: tally_policy: command not found'
h2       : RC=2 OUT identical, STDERR_LINES=0
```

The sandboxed stdout is byte-identical to pristine; the only trace of the helper is nine
discarded stderr lines. Real runner: default `PASS (cases=9 passed=9)` exit 0 vs pristine
`SETUP (0/9)` exit 2; explicit `--workdir`: unchanged `SETUP (0/9)` exit 2 — exactly one config
diverges (`work/real/E-h1-*`).

### 2.4 Scope controls isolate the cause

- **H7** — the same policy written inline in the loop: v3 **kills** it (`CHECK runtime FAIL
  vectors=30316 mismatched=900; first: cfg(1,0) statuses 2 0 … -> got PASS, want SETUP`,
  exit 1), v2 also kills (900). The fault is detectable when it is inside the block; the
  helper's *scope* is what hides it.
- **H8** — the round-34 v1 shape (counting loop moved into top-level `tally_legs()`): both
  tools **refuse** with `TALLY_AUDIT: SETUP (counting \`case $VAR in\` not found)`, exit 2, no
  CHECK line. Behaviourally this copy is identical to pristine in the real runner (the helper
  is defined before `run_regression`); see §4 for why this shape is a measurement hazard.

### 2.5 The class boundary, stated exactly

> v3 (and the frozen counter) certify behavior of **the bytes `run_regression` executes from
> `local nlegs=` to its closing brace, in an interpreter where only `root`, `auto`, `KEEP` exist
> and only `(exit, newline-normalized stdout)` is compared.** Any behavior reachable only
> through (a) a top-level definition, (b) the head section, (c) any other shell variable, (d)
> stderr, (e) a filesystem side effect, or (f) a stdout byte that collides with the transport
> (U+001F, NUL) is **outside the window and cannot be killed**.

The class is **not closed** at this pin. It is a *scope* boundary, not a tool bug: the
contract's kill rule defines behavior as the block under four triples, so the counter certifies
H1/H2 as `div=NONE` — i.e. as must-accept specimens — and the tool's acceptance is consistent
with that label. The limit is that "the runner" in C1 means the tally block, not
`mutate-and-run.sh`.

## 3. The limit: cheapest accepted copies that change real runner behavior

### 3.1 H5 — the A4 class reopened on an unmodeled global (`WORKDIR`)

`run_regression` reads its global `WORKDIR` (`tools/mutate-and-run.sh:1356-1365`); the tool's
explicit triples supply `root=<literal>, auto=0` but **never define `WORKDIR`**
(`v3:349-351, 386`). A one-line block gate is therefore invisible:

```sh
  if [[ -n ${WORKDIR-} ]]; then npass=$((npass+nsetup)); nsetup=0; fi
```

v3: PASS exit 0 (30316/0). v2: PASS exit 0. Counter: `div=NONE`. Real runner:
`--regression` → `SETUP (0/9)` exit 2 (unchanged); `--regression --workdir /tmp/ahs-wd2-h5` →
**`PASS (cases=9 passed=9)` exit 0**, workdir kept (`work/real/E-h5-*.exit`). This is the same
shim-fidelity class as the A4 CRITICAL (RevengerRootShape): a copy keyed on a real runner value
that the simulated triple does not carry. A4 fixed the auto **root value**; the explicit state
is still simulated with three invented variables instead of the runner's real state.

### 3.2 H4 — the explicit-root axis is a two-point sample

The explicit triples still use two fixed literals (`tally-audit`,
`tally-audit-explicit`, `v3:349-351`). A block keyed on **v2's retired literal**
(`/tmp/tally-audit-work`) is invisible to v3 (PASS, 30316/0) but real:
`bash h4 --regression --workdir /tmp/tally-audit-work` prints
`SETUP (cases=9 passed=1 cannot-verify=9)` versus pristine `passed=0` under the same workdir
(`work/real/E-h4-*`). The tool cannot universally quantify the explicit root; it samples two
strings. This is the residual of the A4 design, and it is why H4 is *not* a real v2→v3
regression (§4.5).

### 3.3 H6 — the head check's own guarantee is false for constructed names

The `head` check claims to catch "out-of-block masking/overwrites of leg statuses" and enforces
the twice-only rule by **literal substring count** (`v3:432-469`, message at `v3:461`). A
non-line-initial assignment built at run time never spells `st_js`:

```sh
  st_js=$?
  [[ ${auto-0} -eq 1 && ${KEEP-0} -eq 0 ]] && eval "st_$(printf js)=0"
```

Introspection with v3's own functions (`work/mech2.out`): raw `st_js` count = 2, code-view
count = 2, `check_head` → `(True, 'legs=9')`, block byte-identical to pristine. v3 PASS exit 0;
v2 PASS exit 0; counter `div=NONE`. Real runner default:
`SETUP (cases=9 passed=1 cannot-verify=8)` vs pristine `passed=0 cannot-verify=9`
(`work/real/E-h6-…exit` = 2). The head scan is sound against literal mentions, not against
constructed ones — the docstring sentence overstates it.

### 3.4 H12 — the workdir deletion is a side effect nobody compares

The docstring's fix #2 says the full-stdout comparison covers the `REGRESSION_WORKDIR` line
"which also decides whether the workdir is deleted" (`v3:20-26`). The line is compared; the
deletion is not. Replacing `rm -rf "$root"` with `:` inside the PASS branch (one statement) yields
v3 PASS (30316/0), v2 PASS, counter `div=NONE`. Direct witness with the block under a real
`/tmp/tameshi-r4-2-regression.*` root, vector all-zero, `auto=1 KEEP=0`
(`work/matrix/h12-witness.txt`):

```
pristine : WITNESS=removed  RC=0 FIRSTLINE=REGRESSION: PASS (cases=9 passed=9; …)
h12      : WITNESS=kept     RC=0 FIRSTLINE=REGRESSION: PASS (cases=9 passed=9; …)
```

Same exit, same stdout, opposite filesystem effect; the printed contract ("removed on PASS") is
false for H12 and no audited check notices.

### 3.5 H11 — NUL is dropped by the shell before comparison

Appending `\0` to the PASS line changes the emitted byte stream; `out=$(…)` strips NUL
(`bash: warning: command substitution: ignored null byte in input`, `captured_len=2 captured=ab`).
v3 PASS 30316/0; v2 PASS; counter `div=NONE`. Same family as H3: the transport is not
byte-faithful.

## 4. v2 → v3 comparison

### 4.1 CRITICAL — H3: v2 kills, v3 accepts a real stdout-framing change

**Mutant**: replace the newline that separates the verdict line from the `REGRESSION_WORKDIR`
line with U+001F in the four verdict `printf` formats of the tally block (four one-byte
substitutions). This is inside the block, config-independent, `nlegs`/counters untouched, head
untouched.

**v3 (this pin)** — `TMPDIR=$PWD/tmp python3 work/tool-v3.py --runner work/h3-sep-collision.sh`:

```
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)       EXIT=0
```

**v2 (the control)** — same detector, same bytes:

```
CHECK runtime FAIL vectors=15158 mismatched=15158; first: cfg(0,1) statuses 0 0 …: got
  (0, 'REGRESSION: PASS (…)\x1fREGRESSION_WORKDIR: tally-audit (kept)'),
  want (0, 'REGRESSION: PASS (…)')
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)       EXIT=1
```

**Root cause**, both frozen files: the driver encodes newlines as U+001F into its record format
and decodes U+001F back to newlines (`v3:392` and `v3:398`; counter `c1-measure.py:172` and
`:182`, `SEP='\x1f'` at `:55`). The mapping is not injective: any stdout containing a literal
U+001F is indistinguishable from one containing a newline. v2 compared the first line
(`${out%%$'\n'*}`) and therefore saw the whole joined string; v3's new "full stdout" channel
collapses the difference and reports **zero** mismatches across all 30,316 vectors.

**It is a real behavioral change, not a cosmetic one.** Real runs of the same runner path with
the same explicit workdir (`/tmp/ahs-same/runner.sh`, pristine then h3 bytes,
`work/real/same-*.out`; the runner's own sha line differs, so the last 80 bytes are compared):

```
$ cmp -l work/real/tail-pristine.bin work/real/tail-h3.bin
     35  12  37                    # 0x0a vs 0x1f, one byte, same offset
$ grep -c '^REGRESSION_WORKDIR:' work/real/E-pristine-__regression.out   → 1
$ grep -c '^REGRESSION_WORKDIR:' work/real/E-h3-sep-collision-__regression.out → 0
```

The runner's stdout no longer has two lines; `REGRESSION_WORKDIR:` is not line-addressable, so
every line-oriented consumer of the kept/removed contract breaks, while v3's oracle reports
byte-equality.

**The counter shares the defect**, so the deciding measurement cannot certify a fix:
`work/gt.out` shows `h3-sep-collision diverged_configs=NONE`. A sealed seat that authors H3 with
a byte-faithful harness produces a valid kill specimen, but `score_copies` sees `div=[]`, sets
`valid=False` (`c1-measure.py:306`) and increments `ho_invalid` → C1 can never PASS; a seat that
uses the counter's own transport certifies it as **accept** and the hole passes silently. Either
way the claim surface "(2) the compared tuple is the FULL stdout" is false as implemented, on
both the tool and the ground truth.

### 4.2 The rest of the v2→v3 diff, exhaustively

v2's only sources of strictness over v3 are: (i) first-line-only comparison, (ii) two fixed
root literals `tally-audit` / `/tmp/tally-audit-work`, (iii) raw-text scans (comments counted).
Every other change is a tightening (4 configs, real auto root, comment blinding, full-stdout):

- (i) is inverted by the transport collision → §4.1 (CRITICAL).
- (ii) → H4: v2 kills (7579 mismatches under cfg(1,0) with root `/tmp/tally-audit-work`), v3
  accepts. **Not a regression**: v2's cfg(1,0) combines `auto=1` with a fixed non-mktemp root —
  a state the runner cannot enter — and the copy is identical under v3's real triples and under
  the real auto run. Retiring that literal (A4) necessarily retires the only config that
  exercised H4. H4 is only real under an explicit `--workdir /tmp/tally-audit-work` (§3.2), which
  v2's cfg did not model either.
- (iii) → H10: v2 kills a benign comment naming `st_js` (`CHECK head FAIL … appears 3 times`,
  exit 1); v3 accepts (exit 0) because the copy is behaviorally identical (`div=NONE`). This is
  the intended round-35 false-kill fix, not a regression.
- Nothing else: `oracle()` gained a `cfg` argument but computes the same values; the vector set
  is unchanged; the harness panel is unchanged (v2 and v3 both report `34/34` on pristine).

**Conclusion**: exactly one v2-killed/v3-accepted *real* class exists at this pin — H3. It is
CRITICAL. H4 is the same comparison's only other instance, and it is an artifact of v2's retired
literal, not a behavior the runner can exhibit.

### 4.3 A4 and the intended v3 tightenings, verified independently

- **H9** (gate on `/tmp/tameshi-r4-2-regression.*`, RevengerRootShape's shape): v3 **kills**
  (`runtime FAIL vectors=30316 mismatched=15158; first: cfg(1,0) … got SETUP counted=10, want
  PASS`), v2 accepts (15158/0). A4 works at this pin; the wave-1 CRITICAL cannot be reopened on
  the root axis.
- **H10** — v3's comment-blind head scan accepts the inert comment that v2 false-killed. The
  fix is real and does not open a lexer hole I could exploit: `code_view` (`v3:150-193`)
  divergences from bash (e.g. `$'…\''` ANSI-C escapes) all make v3 *more* conservative (it
  fails to blank text bash ignores), never less; the only less-conservative case is a
  here-document body, and a here-document's `#` lines are comments in any shell that later
  executes them.

## 5. What I could NOT break (with proof)

- **The A4 root witness** — H9 is killed under cfg(1,0) with the real mktemp root; the panel's
  root-keyed copies are exercised by the same path; the selftest carries both a real-root kill
  seed (`v3:789`) and a real-root comment accept seed (`v3:790`). The class is closed **on the
  root value**; it remains open on other runner globals (H5) and other explicit-root literals
  (H4), which the contract does not name.
- **In-block behavior** — H7 (inline policy), and every panel/latent class: the oracle sweeps
  30,316 vectors × 4 configs and the stress pass (duplicate/drop operand) under every config.
  A runtime-visible fault inside the block with newline-clean stdout cannot survive.
- **The harness check** — 34/34 faults rejected on pristine; unchanged by any mutant that does
  not touch the harness region; both v2 and v3 report the same. v3 never runs the copy's own
  block through the runner's harness, but that is outside its documented check.
- **The sealed-provenance gate (A5)** — not attacked this seat (ReviewSealedGate owns it); I
  only confirm the frozen counter bytes at the pin.
- **Comment blinding as a hiding device** — no construction found where bash executes text that
  `code_view` blanks: v3's word-start rule is a subset of bash's (it omits `)`/`}`/`>`/`=`), and
  the quote-state divergence found (`$'…\''`) runs in the fail-closed direction. Proof is
  structural (the blanking rule at `v3:147-193`) plus H10's behaviorally-identical accept.

## 6. Restoration and hygiene

The mutation target was always a scratch copy; the pinned bytes were never overwritten. Final
state (all exit 0):

- **Restored bytes audited**: `cp work/pristine.sh work/restored.sh`; `sha256sum` =
  `a7d3f2dd…912eb9`; `python3 work/tool-v3.py --runner work/restored.sh` → `TALLY_AUDIT: PASS
  (head=pass static=pass runtime=pass harness=pass)`, exit 0, `runtime vectors=30316
  mismatched=0` (`work/matrix/v3-restored.out`). Same detector, same result as the pristine
  baseline taken before any mutant existed.

- `lane` HEAD `7da6e076…`, `git status --porcelain` = **0 lines**; the lane was only read
  (`cp` out, `git show`, `python3` imports). No lane file was written.
- `work/pristine.sh` = `a7d3f2dd…912eb9` before and after all probes (hash in
  `work/matrix/hygiene.txt`); v3/v2/counter/c2 shas unchanged = the pins above.
- All mutants are separate files with recorded shas; `bash -n` accepted every one.
- No writes under `/home/vgpnk/Projects/shokunin/` except this report; no mutating git/jj; no
  `pacman`; no installs (nothing was needed). Real-runner workdirs live in `/tmp`.

## 7. Command log (every command run with its exit)

| command | exit |
|---|---|
| `git clone -q --no-hardlinks … lane` (after removing the stale attempt-1 dir) | 0 |
| `git -C lane checkout -q --detach 7da6e076…` | 0 |
| `sha256sum` of the five pins (matches contract) | 0 |
| `python3 work/build.py`, `build2.py`, inline builders (H3/H11/H12) | 0 |
| `bash -n` on all 12 mutants | 0 each |
| `TMPDIR=… python3 tool-v3.py --runner pristine.sh` | 0 (`PASS`, 30316/0) |
| v3 on H1,H2,H3,H4,H5,H6,H7,H9,H10,H11,H12 | 0,0,**0**,0,0,0,1,1,0,0,0 |
| v3 on H8 | 2 (`SETUP (counting case not found)`) |
| v2 on pristine,H1,H2,H3,H4,H5,H6,H7,H9,H10,H11,H12 | 0,0,0,**1**,1,0,0,1,0,1,0,0 |
| v2 on H8 | 2 |
| `python3 work/groundtruth.py …` (frozen counter import; no deciding run) | 0 |
| real runner: pristine/H1/H2/H5/H6/H3/H4 default + explicit, plus same-path byte runs | exits in `work/real/E-*.exit` |
| `bash h1-policy-call.sh --selftest` | 1 (`MUTATE_SELFTEST: 98/106`, `VERDICT: FAIL`; the runner's own harness rejects the helper copy — an orthogonal detector v3 never runs) |

Key exit files: `work/matrix/*.exit`, `work/real/E-*.exit`. Tool stdout: `work/matrix/*.out`,
`work/v3-*.out`, `work/v2-*.out`.

## 8. Artifact index (absolute paths)

- Scratch root: `/fast/scratch/hyaku/tameshi-r35-seats/AttackHelperScope/`
- Prebuilt tools: `work/tool-v3.py`, `work/tool-v2.py`; pristine: `work/pristine.sh`
- Mutants: `work/h1-policy-call.sh` … `work/h12-keep-workdir.sh` (hashes in §Verdict table and
  `work/matrix/hygiene.txt`)
- Tool matrix: `work/matrix/matrix.txt`, `work/matrix/{v2,v3}-<mutant>.{out,err,exit}`
- Counter ground truth: `work/gt.out`, `work/gt2.out`, `work/groundtruth.py`
- Sandbox mechanism: `work/mech2.out`; workdir side effect: `work/matrix/h12-witness.txt`
- Real-runner receipts: `work/real/E-*.{out,err,exit}`, `work/real/same-*.out`,
  `work/real/tail-{pristine,h3}.bin`, `work/real/h3-cmp.txt`, `work/real/h3-lines.txt`
- Pins/restoration: `work/matrix/hygiene.txt`

Report: `.ufo/waves/round-35/w2/AttackHelperScope.md`
