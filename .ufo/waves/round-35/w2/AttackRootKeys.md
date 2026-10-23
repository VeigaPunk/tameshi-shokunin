# Round-35 w2 — AttackRootKeys

Seat: `tameshi-r35-w2-AttackRootKeys` (leaf mutation-tester, godspeed). Slice: **root-key
fidelity of the v3 witness** — build copies gated on the real runner's root shapes
(`/tmp/tameshi-r4-2-regression.*` via `mktemp`, or a user `--workdir`), report whether v3 accepts a
divergent copy, and prove the limit.

Lane checkout (read-only): `/fast/scratch/hyaku/tameshi-r35-seats/AttackRootKeys/lane`, detached at
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Scratch: `…/AttackRootKeys/work/`. No installs, no
`pacman`, no writes under any git checkout or under `/home/…` except this report. All scratch files
named below are outside the lane.

Pins verified in the lane at `7da6e07` (all match `contract.json`):

| artifact | sha256 |
|---|---|
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` |
| `.ufo/evidence/round-35/c1/c1-measure.py` | `515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8` |

`git status --porcelain` in the lane is empty (exit 0); the sealed dir is **absent** at this pin
(`git ls-tree -r --name-only HEAD -- .ufo/evidence/round-35/c1/` lists the counter + 8 panel JSONs
only). The lane was a stale clone at `d16f9b5`; it was fetched and checked out to `7da6e07`
(`git fetch origin 7da6e07… && git checkout --detach`), no tracked byte edited.

---

## 1. Where A4's witness diverges from the runner it witnesses

The runner mints its auto root at `tools/mutate-and-run.sh:1360` (inside `run_regression`,
1357‑1365):

```bash
root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX) || die_setup 'mktemp -d failed'
```

`mktemp` replaces the **six** `X`s from `[A-Za-z0-9]`. Measured live, 8 draws:

```
35 /tmp/tameshi-r4-2-regression.s3ve6L
35 /tmp/tameshi-r4-2-regression.o30LYC
… (8/8 length 35, suffix = 6 alnum chars)
```

The amended witness is `tempfile.mkdtemp(prefix='tameshi-r4-2-regression.', dir='/tmp')`
(`tools/tally-audit-v3.py:365`; duplicated at `c1-measure.py:67`):

```
37 /tmp/tameshi-r4-2-regression.6899y9_c
37 /tmp/tameshi-r4-2-regression.bogtrozv
37 /tmp/tameshi-r4-2-regression.8_nrrnko
```

Two shape differences: **8** random chars vs 6, and every witness draw observed carries Python's
alphabet (lowercase/digits/`_`, e.g. `6899y9_c`), while all 8/8 real `mktemp` draws are alnum.

```
$ bash -c '[[ $1 =~ ^/tmp/tameshi-r4-2-regression\.[A-Za-z0-9]{6}$ ]] && echo MATCH || echo NOMATCH' _ /tmp/tameshi-r4-2-regression.pHcD9a
MATCH
$ … _ /tmp/tameshi-r4-2-regression.jiof59fo
NOMATCH
```

`contract.json:26` (C1 surface) says the auto triples run "with the runner's REAL auto root
(`/tmp/tameshi-r4-2-regression.XXXXXX`)" and `contract.json:35` (falsifier 1) names "a root-keyed
copy (divergent under the runner's real auto root) that the v3 tool accepts". A4's `change` text is
weaker ("carrying that exact prefix") and **is** implemented; the surface/falsifier promise the
root's *value/shape*, which is not. The gap between the two is the whole finding below.

Method note: every divergence measurement drives the **tool's own** extraction
(`v3.regression_body` → `tally_block` → `head_section` → `leg_names` → `run_vectors`), so the only
difference between compared runs is the root string handed to the block. Where the divergence is
outside the block, section 4 uses full end-to-end `--regression` runs of the pinned runner.

---

## 2. CRITICAL-1 — a root-**shape**-keyed failure mask is ACCEPTED (auto side, falsifier 1)

**Mutant M7** `work/mutants/M7_failmask_real6.sh`, sha256
`a38e19379e8e363a060dbc49220b21ae60b412dc3fbd3a5d7427d530c434c4e6`, one insertion after the tally
loop and before the FAIL guard (2 lines, comment included; FAIL-only so green runs are untouched):

```bash
  # r36: auto roots are minted as tameshi-r4-2-regression.XXXXXX
  if [[ $auto -eq 1 && $nfail -gt 0 && $root =~ ^/tmp/tameshi-r4-2-regression\.[A-Za-z0-9]{6}$ ]]; then nfail=0; npass=$((npass+1)); fi
```

Expected detector: `CHECK runtime FAIL` (the oracle must see FAIL→PASS under the real auto root).
Actual:

```
$ cd <lane> && TMPDIR=<scratch> python3 tools/tally-audit-v3.py --runner <work>/mutants/M7_failmask_real6.sh
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
EXIT=0
```

Receipt `work/v3-M7_failmask_real6.out` sha256 `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82`
(byte-identical stdout to the pristine baseline, `work/v3-pristine.out`, same hash). **Survives.**

Behavior under the runner's real default config — real root `/tmp/tameshi-r4-2-regression.pvFycN`
(len 35), `(auto=1,KEEP=0)`, vs the A4 witness `/tmp/tameshi-r4-2-regression.tu3rtjkr` (len 37):

| vector | pristine (real root) | M7 (real root) | M7 (witness root) |
|---|---|---|---|
| `0×9` | exit 0 PASS / removed | **identical** | identical |
| `1,0…` | exit 1 `FAIL (cases=9 passed=8 failed=1 setup=0)` / kept | **exit 0 `PASS (cases=9 passed=9 …)` / removed** | identical to pristine |
| `2,0…` | exit 2 SETUP / kept | identical | identical |
| `3,0…`, `255,0…` | exit 2 SETUP / kept | identical | identical |
| `1,2,0…` | exit 1 `FAIL (passed=7 failed=1 setup=1)` | **exit 2 `SETUP (passed=8 cannot-verify=1)`** | identical to pristine |
| `0,2,0…` | exit 2 SETUP / kept | identical | identical |

Real-root divergence: 2/7 vectors — a failing leg becomes a full PASS **and the workdir is deleted**
(`rm -rf "$root"` on the auto/keep-0 PASS branch, `mutate-and-run.sh:1465-1466`), destroying the
evidence of the failure. Witness-root divergence: 0/7 — the audit's ground truth cannot see it.

Pristine vs mutant under the **same** real root differ; M1
(`100a6c39fee1271891c93be462f11c2a6eeffb137acf301bd1b3676afeade0da`, unconditional
`nfail=0;npass+1` on the same shape, no `$nfail -gt 0` conjunct) diverges on **7/7** vectors
(the all-green run becomes `SETUP (case-tally mismatch: cases=9 counted=10)`), witness 0/7. M2
(`2aea347d9daa6ed12507b18ccc6ee66f4b59df30d5a16c5b2a7f4050d6adcf20`, `${#root} -eq 35`) behaves
identically to M1.

### 2a. The deciding counter is blind too — and can be turned into a false ACCEPT

`c1-measure.behavior()` runs the copy under the same four `CONFIGS` with the same 8-char witness
(`c1-measure.py:52-68, 204-214`). Measured divergence for these mutants: `diverge=[]` for M1, M2,
M7, M8, M10; only the prefix-glob M4 gives `(1,0),(1,1)`.

That is not merely a missing kill. `score_copies` (lines 285-316) computes, for `set=="accept"`:
`row['valid'] = not div` and `row['pass'] = (not div) and rc == 0`. So the same copy, submitted as
an **accept** specimen, is scored valid and passing. Exact run (frozen counter imported, the frozen
v3 bytes at the pin written out as the scored tool):

```
$ python3 - <<'EOF'   # (full script in this seat's shell history; key call below)
rows = cnt.score_copies([{'class':'root-shape-gated mask (M7) submitted as ACCEPT','set':'accept',
                          'file':'m7-accept.json','edits':[[anchor,(M7 insertion),1]]}],
                        runner_text, '<work>/acc/scored-tool.py', tmp)
EOF
scored tool sha256 ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885
COPY accept root-shape-gated mask (M7) submitted as ACCEPT m7-accept.json div=- rc=0 checks=- pass=True
ROWS [{… 'diverged_configs': [], 'rc': 0, 'valid': True, 'pass': True}]
```

The same copy labelled `kill` prints `INVALID: kill copy without behavioral divergence`
(`valid: False, pass: False`).

**Consequence for C1:** a specimen that masks a real FAIL into PASS under the runner's default
config can be counted toward `pub_accept`/`ho_accept` as a *passing accept*, because neither the tool
nor the counter's ground truth can see the divergence. C1's predicate sentence defines an accept
specimen as "behaviorally identical on every config and vector"; this one is not, yet
`C1_R35_PASS=true` is reachable with it. The kill side fails closed (`ho_invalid>0`) — the accept
side does not.

v2 on M7: `EXIT=0`, `TALLY_AUDIT: PASS` (`work/v2-M7_failmask_real6.out`). So this is **not** a
v2→v3 regression; it is the residual of the class A4 set out to close. v2 also accepts M1, M2, M4,
M5, M6, M8, M9, M10, M11, M12; the v2 PASS receipts checked (M1, M7, M10, M11, M12) share sha256
`e9444d03cf653fd28076078fbb22d03d83a0e870a1487069f0f869af26fae0f0`.

---

## 3. CRITICAL-2 — the explicit-workdir corner `(auto=0, absolute root)` is unswept

The four triples (`tally-audit-v3.py:349-350`, `c1-measure.py:52-53`) are

```python
((None,'1','0'), (None,'1','1'), ('tally-audit','0','1'), ('tally-audit-explicit','0','0'))
```

Both `auto=0` roots are **relative** literals of length 11 and 20. The runner's `--workdir` is
documented as a caller path and is absolute in practice (`mutate-and-run.sh:209`), so the corner
`auto=0 & root=/*` is never sampled. A gate on exactly that corner is invisible:

**M10** `work/mutants/M10_failmask_explicit_abs.sh`, sha256
`74dc014c3804a844cba5c33cad59175397ea2b36b2994809e00438266b903d5c`:

```bash
  # r36: absolute --workdir runs mask transient leg failures
  if [[ $auto -eq 0 && $nfail -gt 0 && $root == /* ]]; then nfail=0; npass=$((npass+1)); fi
```

```
$ python3 tools/tally-audit-v3.py --runner <work>/mutants/M10_failmask_explicit_abs.sh
CHECK runtime PASS vectors=30316 mismatched=0
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
EXIT=0
```

Behavior, real explicit root `/tmp/r35-explicit-root-probe.Gr7JFP` (len 35, `(auto=0,KEEP=0)`),
created by `mktemp -d /tmp/r35-explicit-root-probe.XXXXXX`:

| vector | pristine | M10 |
|---|---|---|
| `0×9` | exit 0 PASS / kept | identical |
| `1,0…` | exit 1 `FAIL (passed=8 failed=1 …)` | **exit 0 `PASS (passed=9 …)`** |
| `2,0…`,`3,0…`,`255,0…` | SETUP | identical |
| `1,2,0…` | exit 1 `FAIL (passed=7 failed=1 setup=1)` | **exit 2 `SETUP (passed=8 cannot-verify=1)`** |

Under both audit explicit literals (`tally-audit`, `(0,1)`; `tally-audit-explicit`, `(0,0)`):
`diverged=[]`. M8 (`0a3f4e7d45e7577080a5785e512143ba5561516cce4f99c14380ebe62a398257`,
`${#root} -gt 20`) is a weaker form of the same corner and is also accepted (`EXIT=0`), diverging
2/7 vectors under the real explicit path.

This reopens wave-1 seat RevengerRootShape's BOUND verbatim ("the explicit side admits no
independent evasion; only the auto-side prefix is unreachable"). The reason given there — the
`(1,0)/(1,1)` literals are absolute — is true but irrelevant: those are `auto=1` triples. The
`auto=0` literals are relative, so the absolute-vs-relative gate is unobservable exactly where it
matters. The same corner argument covers `./…` and `../…` caller roots: the two literals are bare
names, so no config samples a dot-relative explicit path either. Ranking: the claim's own definition
of a kill specimen ("divergent behavior under at least one of the four configs") is satisfied, so
this is claim-false (CRITICAL); if the L1 reads kill specimens as auto-root-only, it is at minimum a
fail-open coverage limit on the explicit half of A4.

---

## 4. CRITICAL-3 — code outside the tally block is neither run nor scanned: the cheapest accepted copy

`audit()` (`tally-audit-v3.py:683-687`) computes `head = head_section(body)` (everything before
`local nlegs=`) and `block = tally_block(body)`; `check_head` only validates leg-assignment
integrity in the head, and `check_runtime` *runs only the block*. Nothing else in `run_regression`
is executed or inspected. Insert one line after the last leg capture and before `local nlegs=`:

**M12** `work/mutants/M12_head_bare_exit.sh`, sha256
`a382753d0cf035d3b710ccce5055c168f8c91187fc9dbaf6611a2422ceefcbbd`, exactly:

```bash
  st_citecheck=$?
  exit 0
```

```
$ python3 tools/tally-audit-v3.py --runner …/M12_head_bare_exit.sh
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)   EXIT=0
$ bash …/M12_head_bare_exit.sh --regression
EXIT=0    (13 lines: 4 headers + 9 `REGRESSION_CASE … SETUP` lines; NO `REGRESSION:` verdict line)
```

That is one line, accepted, and it makes every real regression run report success at the process
level while all nine cases are SETUP.

**M11** `work/mutants/M11_head_early_exit.sh`, sha256
`819c5164ee3670bf0b010c4e0716be4e1116888d9c8f941656bc3efb496c52dc`, the root-keyed, well-formed
variant (gate on the same 6-char real-auto shape, prints a syntactically valid PASS and removes the
root). End-to-end on the pinned runner's own `--regression` path in this scratch clone:

```
PRISTINE  EXIT=2  REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)   REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.RDH0hC (kept)
M11       EXIT=0  REGRESSION: PASS  (cases=9 passed=9; …)              REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.h53lz7 (removed on PASS; --keep retains)
```

All nine `REGRESSION_CASE` lines are SETUP in the M11 run too; the early exit ignores them.
`--then-regression` blesses it as well:

```
$ python3 tools/tally-audit-v3.py --runner …/M11_head_early_exit.sh --then-regression
TALLY_AUDIT: PASS (…)
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
TALLY_AUDIT_REGRESSION: PASS (cases=9 legs=9 exit=0)
EXIT=0
```

Receipts: `v3-M11.out`, `v3-M12.out`, `v3-M11-then.out`, `e2e-pristine.out`
(`b3be98218da81ba8ab1109c18f774b986b01100a9ee9af1f11cada11bfcca2f4`), `e2e-M11.out`
(`a385775ecc83473c15501dc5ac84aae8f1c7b10e58d0c0108e05f3a19172fbd8`), `e2e-M12.out`
(`992a3ed95e3798184f35ac7e0e29a8024e5a53504e1241fd2b1773c0ed0fed8d`). Both accepted by v2 as
well. This satisfies falsifier 2 ("a kill specimen the v3 tool accepts (rc 0)") under the claim's
own definition of a kill specimen; it is outside the *tool's declared model* (the tally block), so
the L1 may rank it as a model boundary rather than a tool bug — but the model boundary is not stated
in C1, and `--then-regression` is presented as a whole-run check.

---

## 5. BOUND-1 (FAIL-CLOSED) — the frozen counter's tool pin is stale; the deciding run cannot pass

`c1-measure.py:46` pins `da23d3a2…` ("v3 at the round-35 freeze"), but the tool bytes at
the measured rev are `ef98fc53…` (the contract's own frozen pin; A4 changed the tool). Deciding-mode
`tool_sha_ok` compares against the constant (line 374), so the run fails:

```
$ python3 .ufo/evidence/round-35/c1/c1-measure.py --lane . --rev 7da6e076… --work <empty>
COPY kill  cfg00-accept-swap   … div=(0,0)      rc=1 checks=runtime pass=True
COPY kill  cfg11-pass-mask     … div=(1,1)      rc=1 checks=runtime pass=True
COPY accept comment-brace      … div=-          rc=0 checks=-       pass=True
COPY accept comment-esac       … div=-          rc=0 checks=-       pass=True
COPY accept comment-names-leg  … div=-          rc=0 checks=-       pass=True
COPY kill  root-keyed-auto-mask … div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  root-keyed-auto-zero … div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-branch-swap  … div=(1,0),(0,0) rc=1 checks=runtime pass=True
C1_R35: mode=deciding tool_present=1 tool_sha=ef98fc5367cdb12c tool_sha_ok=0 runner_sha_ok=1
        pub_kill=5/5 pub_accept=3/3 pub_slots=8 pub_distinct=8 ho_kill=0/0 ho_accept=0/0
        ho_invalid=0 ho_distinct=0 sealed_after_freeze=1 rev=7da6e076… C1_R35_PASS=false
EXIT=1
```

Two facts at once: the public panel is **5/5 kill, 3/3 accept, 8 distinct** at this pin (A4's prefix
class is genuinely closed — both root-keyed panel copies are killed under `runtime`), and the
measurement is blocked by a stale internal constant. Fail-closed, but it means `C1_R35_PASS=true`
is unreachable at `7da6e07` until the counter's `TOOL_SHA256` is reconciled (the contract re-pin in
`23bd903` did not reach this constant). Receipt `work/counter-pub.out` sha256
`855ef64fb68e37a5dc87c7499decea2059b87b698fd7648dd2acdca643525053` (reproduced twice, identical).

---

## 6. What I could NOT break (with proof)

- **Baseline / pristine.** `python3 tools/tally-audit-v3.py --runner tools/mutate-and-run.sh` →
  `TALLY_AUDIT: PASS`, `EXIT=0`, `runtime vectors=30316 mismatched=0` (`v3-pristine.out` sha256
  `46746e2b…`). No false kill.
- **The `(auto,KEEP)` sweep itself.** M3
  (`e354c7c3f2a17da67e0ad64e25efa9ef230d424d2d44b32cf815b0e0345bd72a`), gated on
  `auto=1 && KEEP=0`, is killed: `CHECK runtime FAIL mismatched=7579` (`v3-M3_autokeep.out`
  sha256 `ac367676…`). Round-34's `(0,0)/(1,1)` hole stays closed.
- **A4's prefix class.** M4 (real prefix glob
  `$root == /tmp/tameshi-r4-2-regression.*`, sha256 `f55805f2…`) → `runtime FAIL mismatched=15158`;
  M9 (same prefix with the FAIL-only conjunct, `bf828968…`) → `runtime FAIL mismatched=1800`
  (`v3-M4_tmpprefix.out` `f493315b…`, `v3-M9_failmask_tmpprefix.out` `5e28bb3a…`). This is the
  class RevengerRootShape authored, and v3 closes it while v2 accepts both.
- **Gates on the witness's own shape.** M5 (`${#root} -eq 37`, `290a6d73…`) is killed
  (`CHECK runtime FAIL mismatched=15158`; receipt `v3-M5_witness8.out` `b4f08fcb…`). The audit is
  self-consistent with its own witness — which is precisely why a gate on the *real* shape
  (len 35 / 6 chars) escapes.
- **Accept side on the public panel.** 3/3 accept copies (comment classes) `rc=0`, `div=-`, and the
  pristine runner passes the full default audit (`EXIT=0`).
- **The tool's own selftest, run cleanly.** `python3 tools/tally-audit-v3.py --selftest` →
  `EXIT=0`, `TALLY_AUDIT_V3_SELFTEST: 30/30 pass` (receipt `v3-selftest-clean.out` sha256
  `3d3ef2bc575c18831230ed317efd3b1563b875d8613e2210ff863a67341def25`). Every seeded fault that is
  in the panel is rejected; §7.2 is about what the panel does **not** contain.
- **No v2→v3 regression found.** v2 kills exactly one of the thirteen probes (M3, the
  `auto=1 && KEEP=0` gate, which v3 also kills); v2 accepts the other twelve. Nothing v2 kills is
  accepted by v3, so the successor has no regression, and it gains three kills (M4, M5, M9). The
  survivors (§2-§4) are residual, not regressions.

Not breakable but noted: M6 (`2f03725c4513c1f75f25bb9adc2a98085b2b1875c1af98e86eb03adaf24b2f71`)
replaces `root=$(mktemp -d …)` with a fixed shared path `root=/tmp/tameshi-r4-2-regression.shared`;
v3 PASSES it (the root *construction* is outside the block). Real harm: concurrent regression runs
share one workdir and a PASS `rm -rf`s it under the other run. Out of the tool's declared model
(§4 is the sharper form of the same boundary).

---

## 7. HYGIENE

1. **Doc/implementation mismatch.** `tally-audit-v3.py:34,355` and `c1-measure.py:59` all write the
   root as `$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` while the implementation is
   `tempfile.mkdtemp` (8 chars, `_` allowed). The prose hides the exact gap §2 exploits.
2. **Selftest seeds only the prefix class.** The single root-keyed fault in `faults()`
   (`tally-audit-v3.py:789`) is `"$root" == /tmp/tameshi-r4-2-regression.*` — a glob that matches
   the 8-char witness as well as the 6-char real root. The selftest is otherwise sound (`30/30`
   clean, §6), but no fault keys on suffix length or alphabet, and the audit's harness check
   (`faults rejected=34/34` in every run above) uses the same panel. `34/34` therefore cannot detect
   a shape-keyed copy.
3. **Counter duplicates the witness rather than importing it** (`c1-measure.py:52-68` vs
   `v3:349-365`). They agree today by hand; any fix must touch both or they drift.
4. The two explicit literals are *relative* while the runner's own documented `--workdir` usage is
   absolute; even a purely defensive witness should include one absolute caller path under each
   KEEP value.

---

## 8. Restoration / evidence trail

- Lane: `git status --porcelain` **empty** (0 lines), `HEAD = 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`;
  the four pinned sha256s were re-hashed after the last probe and are unchanged (`ef98fc53…`,
  `7b11ba25…`, `a7d3f2dd…`, `515b0b1b…`). No file under `…/lane`, `.ufo/state/`,
  `/home/vgpnk/Projects/shokunin/` (other than this report) or any sibling lane was written.
  Temporary roots minted for the probes (real `mktemp` roots, the witness roots, the explicit probe
  root) were deleted after their outputs were captured; the end-to-end cleanup loop reported the
  pristine and M7 roots `EXISTS` (deleted) and the M11 root `GONE` (the copy itself `rm -rf`'d it on
  its synthetic PASS — the behaviour under test).
- Mutants (byte files, outside the lane), all under
  `/fast/scratch/hyaku/tameshi-r35-seats/AttackRootKeys/work/mutants/`:

  | file | sha256 | v3 | v2 |
  |---|---|---|---|
  | `pristine-mutate-and-run.sh` | `a7d3f2dd…912eb9` | PASS 0 | PASS 0 |
  | `M1_sixchar_regex.sh` | `100a6c39…ade0da` | **PASS 0** | PASS 0 |
  | `M2_len35.sh` | `2aea347d…adcf20` | **PASS 0** | PASS 0 |
  | `M3_autokeep.sh` | `e354c7c3…5bd72a` | FAIL 1 | FAIL 1 |
  | `M4_tmpprefix.sh` | `f55805f2…9bfca` | FAIL 1 | PASS 0 |
  | `M5_witness8.sh` | `290a6d73…3ea0286` | FAIL 1 | PASS 0 |
  | `M6_fixed_shared_root.sh` | `2f03725c…24b2f71` | **PASS 0** | PASS 0 |
  | `M7_failmask_real6.sh` | `a38e1937…34c4e6` | **PASS 0** | PASS 0 |
  | `M8_failmask_explicit_long.sh` | `0a3f4e7d…398257` | **PASS 0** | PASS 0 |
  | `M9_failmask_tmpprefix.sh` | `bf828968…d8d5bb` | FAIL 1 | PASS 0 |
  | `M10_failmask_explicit_abs.sh` | `74dc014c…b903d5c` | **PASS 0** | PASS 0 |
  | `M11_head_early_exit.sh` | `819c5164…96c52dc` | **PASS 0** | PASS 0 |
  | `M12_head_bare_exit.sh` | `a382753d…efcbbd` | **PASS 0** | PASS 0 |

- Mutants are the pinned runner plus exactly one inserted hunk: `cmp` of
  `work/mutants/pristine-mutate-and-run.sh` against the lane's runner exits 0 (byte-identical), and
  `diff -u` against each mutant shows one `+` block (M7/M10: a comment + one `if`; M11: the
  shape-gated PASS/`rm -rf`/`exit 0`; M12: the single line `exit 0`). Nothing else in the runner
  differs.
- Receipts (`work/*.out`): `v3-pristine.out`, `v3-M1..M12`, `v3-M11-then.out`,
  `v2-*`, `e2e-pristine.out`, `e2e-M7.out`, `e2e-M11.out`, `e2e-M12.out`, `counter-pub.out`.
  The PASS receipts for pristine/M1/M2/M6/M7/M8/M10/M11/M12 share one sha256
  (`46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82`) because the audit's stdout is
  byte-identical across them — the tool cannot tell them apart, which is the finding.
- No installs or upgrades were performed; `pacman` was not invoked.

---

## 9. Ranked summary and fix directions

| rank | finding | evidence |
|---|---|---|
| **CRITICAL-1** | A4's "real auto root" is an 8-char `tempfile.mkdtemp`, not the runner's 6-char `mktemp` root; a FAIL-only mask gated on the real shape (M7) is accepted (`runtime PASS 30316/0`) and diverges FAIL→PASS+`rm -rf` on the real config. Falsifier 1 literally. Counter blind; same copy scored `accept pass=True`. | §2, §2a |
| **CRITICAL-2** | The explicit triples sample only two relative literals; `(auto=0, absolute caller root)` is unswept and M10 is accepted while diverging FAIL→PASS on any real `--workdir`. Reopens RevengerRootShape's explicit-side BOUND. | §3 |
| **CRITICAL-3** | Head-region code is never executed or scanned: M11 (root-keyed early exit) and the 1-line M12 `exit 0` are accepted; end-to-end SETUP→PASS, workdir deleted; `--then-regression` also PASS. | §4 |
| **BOUND-1** | Frozen counter's `TOOL_SHA256` is the pre-A4 tool (`da23d3a2`), so the deciding run at this pin reports `tool_sha_ok=0` and `C1_R35_PASS=false` (fail-closed, measurement-blocking). | §5 |
| **BOUND-2** | Root *construction* is outside the model (M6 accepted; shared-suffixed root under concurrency). | §6 |
| **HYGIENE** | Doc/impl XXXXXX mismatch; selftest seeds prefix only; duplicated witness; relative-only explicit literals. | §7 |

Fix direction (one line each): (a) mint the witness with the runner's own constructor —
`subprocess.run(['mktemp','-d','/tmp/tameshi-r4-2-regression.XXXXXX'])` — or replicate `[A-Za-z0-9]{6}`
exactly, in **both** v3 and the counter; (b) add `(auto=0, KEEP=0, /tmp/<abs>)` and
`(auto=0, KEEP=1, /tmp/<abs>)` to the triple set (the root is not part of the `(auto,KEEP)` key and
must not be pinned to relative literals); (c) decide whether anything outside the tally block is in
the model — if yes, add a whole-function behavioral comparison (or at minimum reject `exit`/`return`
and non-bare statements between the last leg capture and `local nlegs=`); (d) fix
`c1-measure.py:46`, and re-seed the selftest with a shape-keyed fault so `34/34` means what it says.
