# Round-35 w2 — AttackSpanTail

Seat: `tameshi-r35-w2-AttackSpanTail` (leaf mutation-tester, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (verified: lane checkout at that commit; lane
`git status --porcelain` empty). Slice: **the audited span boundary** — `regression_body` /
`tally_block` / `check_runtime`: the tool executes only the text from `local nlegs=` to the
function's last brace, so everything between the last leg capture and `local nlegs=` is checked
by token rules but never executed.

All scratch under `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/`; the lane checkout
was read-only; no writes under `/home/vgpnk/Projects/shokunin/` except this report; no git
mutation; no subagent dispatch (leaf); no installs and no `pacman` (nothing needed).

Pinned bytes relied on (sha256, re-verified at the end):

```
ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885  tools/tally-audit-v3.py @ 7da6e07
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tools/tally-audit-v2.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh (pristine copy == pin)
515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8  .ufo/evidence/round-35/c1/c1-measure.py @ 7da6e07
```

The fleet **working tree moved mid-wave**: at 18:38 it carried `tools/tally-audit-v3.py`
`ec236de2826fce3fe5660c04f2144006cb4eafca90c974a3dc3de0ba4dd7b435` and `c1-measure.py`
`b9ee1042aa3ec5b83a8545e7d6e596b054d02ecadcf3e1f02f7c294ce052bf15` (uncommitted; new
`_tally_start`/`_block_end` decoy fix, a literal "mention" rule, and `unsafe_block`). Those edits
are other seats', not mine. Every mutant below was scored against **both** revisions; the class
survives both.

---

## 1. The span, measured

`tally_block` (v3:229-238) cuts `body[START_RE first match : cv.rfind('}')]`; `head_section`
(v3:240-244) is everything before the same match; `check_runtime` (v3:499-568) runs **only that
block** in a synthetic `tally()` driver. Measured on the pinned runner (tool's own functions,
`w2/span_driver.py` import):

```
file_bytes        106218
run_regression    body 68425..75302   (6877 B)
head              5314 B   (77.3% of the function)
audited block     1562 B   (22.7%)     starts at byte 73739
gap               body[73737:73739] == "\n\n"   (between `st_citecheck=$?` and `local nlegs=`)
```

The runtime oracle therefore never executes 77.3% of `run_regression`. The `head` check
(v3:432-470) enforces only: line-anchored `st_*=` forms, exactly one bare `st_x=$?` per leg, and
`head_code.count(name) == 2`. Any code that changes a status **without spelling a leg name** is
invisible to every check.

Method for the behavioural claim: `w2/span_driver.py` prepends the post-capture head region
(text between `st_citecheck=$?` and `local nlegs=`) to the block cut by the **tool's own**
`regression_body`/`tally_block`, runs (exit, FULL stdout) under the four `CONFIGS` with the real
`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` root shared by pristine and copy, over
all-zero, one-1, one-2, one-3, one-255, mixed-1-2, mixed-0-1. The end-to-end runs below execute
the **real runner CLI** (`bash <copy> --regression [--keep|--workdir DIR]`), where each auto run
gets its own mktemp root (paths compared by verdict/count wording, not by random suffix). In this
isolated clone the nine legs all return SETUP (sibling fleet repos absent) — a real runner state;
the vector probe additionally proves FAIL→PASS.

## 2. CRITICAL — the head region is executed by the runner but never by the oracle

**Witness A (most damaging): computed-name leg mask, head-only.**
File `w2/work/m-maskall.sh`, sha256 `bf932a36d3bee736ff9cd470c53fb891627aab239ccbf919c09bbbe8cc98c6a3`.
Inserted two bytes before the audited span (after `st_citecheck=$?`):

```bash
  for n in js kagi tsu mado checklist claims roundgate sourcescheck citecheck; do eval "st_$n=0"; done
```

No literal leg name appears: `head_code.count('st_js')` stays 2 (declaration + capture); the
line does not match `^[ \t]*st_[A-Za-z0-9_]+=`; `leg_names`/`operands`/`nlegs` unchanged. The
block text is byte-identical to pristine (`block_sha=e163133c0f54bb0c`, 1562 B — measured).

Detector and output:

```
$ python3 <lane>/tools/tally-audit-v3.py --runner .../m-maskall.sh     # tool sha ef98fc53 (pin)
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)     EXIT=0
```

Same command against the live working-tree tool (`ec236de2`, with the wave-2 mention rule and
decoy fix): `TALLY_AUDIT: PASS`, `EXIT=0` (`out/live-m-maskall.txt`). v2 (`7b11ba25`) also
accepts it: `TALLY_AUDIT: PASS`, `EXIT=0` (`out/v2-m-maskall.txt`) — the class predates v3.

Real runner, all four configs (`out/e2e-*.txt`, exits in `out/e2e-rc.txt`):

| config | pristine (a7d3f2dd) | m-maskall (bf932a36) |
|---|---|---|
| `--regression` | exit **2** `SETUP (cases=9 passed=0 cannot-verify=9)` | exit **0** `PASS (cases=9 passed=9 …)`; workdir removed |
| `--regression --keep` | exit 2, same SETUP line | exit 0, PASS, `(kept)` |
| `--regression --workdir /tmp/r35-explicit-…` | exit 2 | exit 0 |
| `--regression --workdir … --keep` | exit 2 | exit 0 |

Vector-level (same real auto root both sides, `out/span-driver.txt`): divergence **6/7 vectors
under every one of the four triples**; e.g. `one-1` pristine `(1, FAIL … setup=0)` → copy
`(0, PASS …)`; `one-2/3/255` `SETUP` → `PASS`; `mixed-0-1` `FAIL` → `PASS`. `all-zero` is the
only identical vector (masking a 0 changes nothing).

**Witness B (single-leg, one line):** `m-mask1.sh` sha256
`abed8816a3307a9ab1b61a7e9b40d3403dce44413a1b28965a54ec29ab291efe`, `n=js; eval "st_$n=0"`.
Tool `PASS` at both revisions; real runner `SETUP (cases=9 passed=1 cannot-verify=8)` vs
pristine `passed=0`; vector `one-1` `FAIL`→`PASS`, 5/7 vectors × 4/4 configs.

**Measurement blindness (decisive):** the frozen counter's ground truth is
`tally_block(text)` → `behavior(block)` (c1-measure.py:132-158, 204-220) — the **same span**.
`w2/counter_span_probe.py` (runs the counter's own functions):

```
m-root/m-mask1/m-maskall/m-keyed/m-commentbrace   diverged_configs=-   -> counter would score: ACCEPT
```

Re-run against the live counter (`b9ee1042`): identical — all five `ACCEPT`, and
`unsafe_block(tally_block(text)[1])` returns `None` for every head mutant. A head-only witness
is therefore unscorable by C1 **as instrumented**: no sealed or public specimen in this frame can
express it. The public panel confirms the data gap: all five kill and three accept JSONs anchor
inside the block (`if [[ $nfail -gt 0 ]];`, `esac\n  done`, `if [[ $auto -eq 1 …`) — none
anchors before `local nlegs=` (panel listing in §7).

**Ranking: CRITICAL for the claim's scope as written** — the predicate sentence says a kill
specimen is "divergent behavior under at least one of the four configs"; this copy diverges from
pristine under **all four real configs**, including a full SETUP→PASS verdict flip, and the v3
check that advertises "catches out-of-block masking/overwrites of leg statuses" returns PASS.
Honest caveat: because the contract's operating kill rule extracts the same span, C1-as-measured
cannot count this class; the finding falsifies the prose guarantee and the head check's stated
capability, and it marks the measurement's ground truth as span-limited.

## 3. CRITICAL (cheapest accepted real-behaviour change) — one assignment

`w2/work/m-root.sh`, sha256 `dc37e8e172e41012404a74651bd6e56543bac0d4ad9f7bb987e71ccc65302c88`.
Inserted in the same 2-byte gap, a single bare assignment:

```bash
  root=/tmp/r35-span-attack-root
```

- Tool at pin **and** live: `TALLY_AUDIT: PASS`, `EXIT=0` (`out/v3-m-root.txt`, `out/live-m-root.txt`).
- Real runner: `REGRESSION_WORKDIR: /tmp/r35-span-attack-root` under **all four** configs
  (pristine prints its own mktemp root, or the caller's `--workdir`); on PASS under the default
  auto config the copy's `rm -rf "$root"` targets a directory the run never created and leaves
  the real workdir behind. Full-stdout divergence **7/7 vectors × 4/4 configs**
  (`out/span-driver.txt` m-root).
- The live counter's new filesystem gate does not see it: `unsafe_block(tally_block(copy)[1])`
  scans the block only → `None`; applied to the whole text it would flag **pristine** too
  (`specimen reassigns root`), so the gate is scope-blind to the head.
- Witness is inert on disk: `/tmp/r35-span-attack-root` was never created (`ls` → No such file).

This is the "cheapest copy that changes real runner behavior in a way the tool still ACCEPTS":
21 bytes, no structural change, no token the checks look for.

## 4. BOUND — the limit is not closable: harness-keyed evasion

`w2/work/m-keyed.sh`, sha256 `e11de89f0044c6a33ebe46255bcbe2d9d2ccd5f76a0ea89ffdbce07c1c20ab42`,
one line **inside** the block:

```bash
  if [[ ${BASH_SOURCE[0]} != */p[0-9]*.sh && ${BASH_SOURCE[0]} != */b[0-9]*.sh ]]; then npass=$nlegs; nfail=0; nsetup=0; fi
```

The tool's driver writes `p<N>.sh`, the counter's writes `b<N>.sh`; the real runner is a named
file. Kept tuple:

- `TALLY_AUDIT: PASS (… runtime=pass …) vectors=30316 mismatched=0`, `EXIT=0` at the pin
  (`out/pin-m-keyed.txt`) and live (`out/live-m-keyed.txt`).
- Real runner: `PASS (cases=9 passed=9 …)` under **all four** configs vs pristine `SETUP
  (cases=9 passed=0 cannot-verify=9)` (`out/e2e-m-keyed-*.txt`); vector probe 6/7 × 4/4
  (`out/span-driver-keyed-final.txt`).
- Counter: `diverged_configs=-` → ACCEPT.

A behavioural oracle cannot separate a block that introspects its own harness; naming the driver
`mutate-and-run.sh` or scrubbing `BASH_SOURCE` only moves the signal surface (`$0`, `$-`, `HOME`,
`TMPDIR`, parent pid are all readable). Recorded as a **BOUND on any extract-and-run oracle**, not
a fixable check. (A cheap static tripwire — flag `${BASH_SOURCE` / `${0` in the block — would catch
this instance but not the class.)

## 5. What I could NOT break (fail-closed proofs)

1. **In-span, whole-stdout, four-config sweep works.** `m-inspan.sh` (sha
   `4f1d07ba6a9e8e26d6588b4d9a042ef3198ffdc86f840d414d9468991bd918ed`) flips the PASS workdir
   branch to `if [[ $KEEP -eq 0 ]]`. v3:
   `CHECK runtime FAIL vectors=30316 mismatched=10; first: cfg(0,0) statuses 0 0 …: got '…(removed on PASS; --keep retains)', want '…(kept)'`,
   `TALLY_AUDIT: FAIL`, `EXIT=1`. The round-35 fix #2 catches a WORKDIR-line-only defect **inside**
   the span exactly at the config that exposes it.
2. **The head literal-token rule is fail-closed.** `m-lit.sh` (sha
   `ba583243c01000d711ecd7416a92d98e6cdfeee8a6686f48e33dbb9e20fe7298`) with `st_js=0`:
   `CHECK head FAIL … non-bare leg assignment(s) in the head: st_js=0; leg st_js assigned 2 times; leg st_js appears 3 times`,
   `TALLY_AUDIT: FAIL`, `EXIT=1`. Any construction that *spells* the name (bare, `eval 'st_js=0'`,
   `read -r st_js`, `printf -v st_js`) is refused; only name **computation** evades (§2).
3. **A4 (real auto-root witness) is closed at this pin.** Wave-1's mutant-B gate re-inserted
   verbatim (`m-rootkeyed.sh`, sha `80a4fd7c9e987ec75ef833b0ac75c03e74fc21cdafbbe061b7d2df44a03b9b6e`):
   `CHECK runtime FAIL vectors=30316 mismatched=15158; first: cfg(1,0) … got SETUP(case-tally mismatch counted=10) want PASS`,
   `TALLY_AUDIT: FAIL`, `EXIT=1` — the auto triples now run under
   `/tmp/tameshi-r4-2-regression.88cek2ps`. I could not reopen RevengerRootShape's class.
4. **No v2→v3 capability regression (bounded negative).** v2 is strictly weaker except that its
   raw-text scans are not comment-blind: v2 accepts the identical head hole (`m-maskall`
   `TALLY_AUDIT: PASS`, `EXIT=0`; `m-root` likewise), so the class was not *caught* by v2. The
   only verdict delta on the panel is `m-commentbrace` (sha
   `6de635b0c94dac919139c4d95b66aa5d94a57f3aa73b987362a8d12036ca8e5f`, an inert `# … }` comment plus
   the head mask): v2 `TALLY_AUDIT: SETUP (tally start `local nlegs=` not found)`, `EXIT=2`;
   v3/live `TALLY_AUDIT: PASS`, `EXIT=0`. v2's refusal is a **parse refusal** (raw brace counting
   stops at the comment `}`), not a behavioural catch — it accepts the same behaviour without the
   comment. Round-35 fix #3 (comment-blind scanning) therefore removed a false refusal, not a
   real catch. Residual lexical edge measured: `bash -c 'echo hi >#/tmp/xx'` is a bash comment
   near `newline` (bash treats `#` after `>` as a comment) while `code_view` does not — that
   direction makes v3 scan **more**, i.e. fail-closed. No construct found where bash executes
   text that `code_view` blanks.
5. **Adversarial block text cannot move the span end under the live fix** (it now uses last-match
   start + first depth-0 `}`); the head mutants place code strictly before the start, so the fix
   neither helps nor hurts them — confirmed by the live-tool PASS verdicts in §2-§4.

## 6. Exact commands

```bash
# lane
git clone --no-hardlinks … /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/lane
git -C …/lane fetch -q origin && git -C …/lane checkout -q --detach 7da6e076   # exit 0, HEAD 7da6e07

# tool verdicts (pin ef98fc53 via the lane at 7da6e07; live ec236de2 via the fleet working tree)
python3 …/lane/tools/tally-audit-v3.py --runner …/m-maskall.sh   # exit 0  PASS
python3 …/lane/tools/tally-audit-v3.py --runner …/m-keyed.sh     # exit 0  PASS
python3 …/tools/tally-audit-v3.py    --runner …/m-maskall.sh     # exit 0  PASS (live bytes)
python3 …/tools/tally-audit-v2.py    --runner …/m-maskall.sh     # exit 0  PASS (control)
python3 …/tools/tally-audit-v2.py    --runner …/m-commentbrace.sh # exit 2  SETUP refusal (control)
python3 …/lane/tools/tally-audit-v3.py --runner …/m-lit.sh        # exit 1  head FAIL
python3 …/lane/tools/tally-audit-v3.py --runner …/m-inspan.sh     # exit 1  runtime FAIL
python3 …/lane/tools/tally-audit-v3.py --runner …/m-rootkeyed.sh  # exit 1  runtime FAIL 15158

# real runner, four configs
bash …/work/pristine.sh  --regression                          # exit 2
bash …/work/m-maskall.sh --regression                          # exit 0
bash …/work/m-maskall.sh --regression --keep                   # exit 0
bash …/work/m-maskall.sh --regression --workdir /tmp/r35-explicit-m-maskall          # exit 0
bash …/work/m-maskall.sh --regression --workdir /tmp/r35-explicit-m-maskall-k --keep # exit 0

# vector-level (tool's own span, real auto root shared both sides; seven vectors × four triples)
python3 …/w2/span_driver.py
python3 …/w2/counter_span_probe.py
```

## 7. Witness table

| copy | sha256 (short) | v3 pin | v3 live | v2 | real-runner divergence |
|---|---|---|---|---|---|
| pristine | a7d3f2dd | PASS 0 | PASS 0 | PASS 0 | — (baseline) |
| m-maskall (head eval loop) | bf932a36 | **PASS 0** | **PASS 0** | **PASS 0** | SETUP→PASS, 4/4 cfg, 6/7 vec |
| m-mask1 (head one leg) | abed8816 | **PASS 0** | **PASS 0** | **PASS 0** | passed 0→1; FAIL→PASS one-1, 5/7 |
| m-root (head `root=`) | dc37e8e1 | **PASS 0** | **PASS 0** | PASS 0 | WORKDIR line + rm target, 7/7 × 4/4 |
| m-keyed (harness-keyed) | e11de89f | **PASS 0** | **PASS 0** | — | SETUP→PASS, 4/4 cfg, 6/7 |
| m-commentbrace | 6de635b0 | PASS 0 | — | SETUP 2 | SETUP→PASS, 6/7 × 4/4 |
| m-lit (literal head mask) | ba583243 | FAIL 1 head | — | — | (refused) |
| m-inspan (in-span WORKDIR) | 4f1d07ba | FAIL 1 runtime | — | — | (caught) |
| m-rootkeyed (wave-1 A4 gate) | 80a4fd7c | FAIL 1 runtime | — | — | (caught; A4 closed) |

Public panel anchor inventory (`c1/panel/`): `cfg00-accept-swap`, `cfg11-pass-mask`,
`comment-brace`, `comment-esac`, `comment-names-leg`, `root-keyed-auto-mask`,
`root-keyed-auto-zero`, `workdir-branch-swap` — every edit string is in-block
(`if [[ $nfail -gt 0 ]];`, `esac\n  done`, `if [[ $auto -eq 1 …`, `st_js=$?`, `0) npass=…`);
**zero** head-anchored specimens, so the panel cannot cover this seam.

## 8. Restoration / integrity evidence

- All mutations are **copies** under `w2/work/`; no frozen byte was edited. `pristine.sh` sha256
  was `a7d3f2dd…912eb9` at copy time and again at the end — the pin, unchanged.
- The lane checkout at `7da6e07` was clean before and after (`git status --porcelain` empty); its
  `tools/tally-audit-v3.py` hashes to `ef98fc53…` and `tools/mutate-and-run.sh` to `a7d3f2dd…`.
- Fleet `tools/tally-audit-v2.py` (`7b11ba25…`) and `tools/mutate-and-run.sh` (`a7d3f2dd…`) are
  unchanged. Fleet `tools/tally-audit-v3.py` / `c1-measure.py` / `contract.json` were modified by
  other seats mid-wave (18:38, uncommitted); I only read them — every live-bytes verdict above
  records the exact hash of the bytes it exercised.
- No tool installs or upgrades were performed (none needed); `pacman` untouched.

## 9. Routing

- **CRITICAL:** the audited span excludes all code before `local nlegs=` from execution (77.3% of
  `run_regression`); a computed-name leg mask (or a one-line `root=` reassignment) flips the real
  `--regression` verdict under all four configs while v3 reports `vectors=30316 mismatched=0`,
  at pin **and** at the live wave-2 revision. Fix direction: either execute the whole
  `run_regression` head under the same four-config driver (synthetic leg statuses + the real
  capture lines), or refuse any head text that is not a capture/declaration/blank line — the
  head's only legitimate content is `local st_*` + nine bare `st_x=$?`.
- **BOUND:** harness-keyed evasion is outside any extract-and-run oracle; record it in the lesson
  rather than adding a check, and consider naming the audit driver after the runner as a cheap
  partial mitigation.
- **BOUND (counter):** the deciding counter shares the span *and* the naming, so C1-as-measured
  cannot score head divergences; any future fix must move the counter and the tool together, or
  the measurement will keep blessing span-limited specimens.
- **HYGIENE:** `unsafe_block(tally_block(copy_text)[1])` is scope-blind to the head (and flags
  pristine if applied to the full text); contract `frozen_artifacts.tool_sha256` (ef98fc53) no
  longer matches the working tree (ec236de2).
