# RevengerSelftest — round 35 w2 (v3 selftest surface, replayed and attacked)

Seat: `L1tameshi35.RevengerSelftest` (leaf revenger, godspeed; no subagents, no installs).
Lane pin at dispatch: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.

Setup (target script, rerun because a stale clone of this lane sat at `d16f9b5a`; fetch + checkout):

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r35-seats/RevengerSelftest/lane        # exit 128 (dir existed) → reused
git fetch -q origin && git checkout -q --detach 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b   # exit 0
git rev-parse HEAD   # 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b
```

Pins verified at the checkout (sha256sum, all match contract.json frozen_artifacts):

| artifact | sha256 |
|---|---|
| `tools/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `tools/tally-audit-v2.py` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |

All scratch under `/fast/scratch/hyaku/tameshi-r35-seats/RevengerSelftest/work/`; lane checkout read-only
(no commits, no writes inside it). Tooling directive record: **no installs performed, no pacman** (nothing
needed; python3 + bash + git sufficed).

## 1. Selftest replay and reconciliation — 30/30, not 28/28

```
$ cd /fast/scratch/hyaku/tameshi-r35-seats/RevengerSelftest/lane
$ time python3 tools/tally-audit-v3.py --selftest
... every case line PASS (30 lines) ...
TALLY_AUDIT_V3_SELFTEST: 30/30 pass
real 5m48.769s   EXIT=0
```

The dispatch brief says "reconcile 28/28". **At this pin the selftest has 30 cases and prints 30/30,
exit 0.** Reconciliation of the delta: the brief's 28 matches the *pre-A4* tool bytes at
`d16f9b5a` (tool sha `da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f`, 808 lines;
I read its selftest before completing the checkout — exactly 28 case tuples, no real-root cases).
Amendment A4 added two cases at `tools/tally-audit-v3.py:789-790`:

- `('real-root gated mask', ...)` — want exit 1, check `runtime` → **PASS (exit 1)**: a copy whose
  tally block gates the verdict on `$root == /tmp/tameshi-r4-2-regression.*` is killed. This is the
  A4 class w1 seat RevengerRootShape opened (CRITICAL false-accept); the fixed apparatus closes it.
- `('comment names real root', ...)` — want exit 0 → **PASS (exit 0)**: an inert comment naming the
  real-root template stays accepted.

So the A4 coverage is present, seeded, and green at the pin. Case list spans `:757-787` plus the
round-35 comment/real-root block `:782-790`; the kill-cases' exits and named checks are asserted at
`:813`.

## 2. The attack — a real seeded-fault class the selftest does NOT contain

**Named class (round-34 Holds, carried unadopted into v3):** *preamble/head seeding* — a fault
confined to run_regression's HEAD (the region between the function opening and the tally start,
`tools/mutate-and-run.sh:1357-1365`), specifically the config-variable declarations the tally
block's verdict machinery reads (`auto`, `KEEP`, `root`) and the workdir-removal action. Round-34
lesson: "preamble seeding reproduced (head-local `auto` rename → real regression in BOTH runner
configs, workdir leak, tool PASSes — ResiduePreambleSeeding)". The selftest's 30 cases contain **no**
head-confined config-var fault: every head case is an `st_*` leg fault (`head masked` :761,
`head overwrite` :766-area) and every config case lives INSIDE the block (cases at `:777-783`).

Why the class is structurally invisible to the auditor at this pin:

- The runtime driver fabricates the declarations itself: `run_vectors` inlines only the tally block
  under `"  local root=%s auto=%s KEEP=%s"` (`tally-audit-v3.py:390`), so whatever the copy did to
  its own head declarations never executes under any of the four configs (`CONFIGS`, `:349-350`).
- `check_head` (`:432-463`) scans the head only for `st_*` leg assignments/occurrence counts; `auto`,
  `KEEP`, `root` and `rm` are out of its grammar.
- The oracle's compared tuple is `(exit, FULL stdout)` (`oracle`, `:400-421`); filesystem effects
  (the `rm -rf "$root"` at runner `:1466`) are not observed.

Two seeds built from the pinned runner bytes (single `str.replace`, both verified to apply; scratch
`work/m2_autostrip.sh`, `work/m1_rmstrip.sh`):

- **m2_autostrip** — `  local root specs auto=0\n` → `  local root specs\n` (runner `:1357`; the
  auto branch's `auto=1` at `:1361` and the block's `[[ $auto -eq 1 ...` at `:1464` are untouched).
  sha256 `c1cc67d191835208bae3b3ed1f0441c5871f9894c8673aa67060daae46ce93b1`.
- **m1_rmstrip** — delete `    rm -rf "$root"\n` (runner `:1466`, first of two occurrences; the
  second at `:2049` is the runner's own selftest region and is not the audited behavior).
  sha256 `1d3d121d43533e989f657998aad3751bbfd50ee397f6eeb8b629ae9fb2b80020`.

### Tool verdicts (the auditor's own CLI)

```
$ python3 tools/tally-audit-v3.py --runner ../work/m2_autostrip.sh
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)     EXIT=0
$ python3 tools/tally-audit-v3.py --runner ../work/m1_rmstrip.sh
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)     EXIT=0
```

Both false-accepts: 30,316 vectors × 4 configs, zero mismatches, all checks green.

### Real-runner-context divergence proof (witness harness, not the tool)

Harness `work/cx_<name>_<mode>.sh` replicates the runner's own variable context — the copy's head
declaration line verbatim (present for pristine, absent for m2), the runner's root construction
(`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` auto mode; a caller directory, workdir mode), the
`auto=1` the auto branch assigns (`:1361`), `KEEP=0`, nine zero legs — then runs the copy's extracted
tally+verdict region (the same span the tool extracts) and reports exit/stderr and whether the root
directory survived. Results:

| copy | mode | exit | stdout after the PASS line | root after |
|---|---|---|---|---|
| pristine | auto | 0 | `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.* (removed on PASS; --keep retains)` | GONE |
| m1_rmstrip | auto | 0 | byte-shape identical to pristine | **SURVIVED (leak)** |
| m2_autostrip | auto | 0 | identical (auto bound by the branch's `auto=1`) | GONE |
| pristine | workdir | 0 | `... (kept)` | SURVIVED |
| m1_rmstrip | workdir | 0 | `... (kept)` | SURVIVED |
| **m2_autostrip** | **workdir** | **1** | **missing entirely — bash `auto: unbound variable` at the `[[ $auto -eq 1 ...` line** | **SURVIVED (leak)** |

m2's real divergence is precisely of the class C1's apparatus claims to police: under the runner's
real `--workdir` PASS path the copy prints the PASS line, then dies with exit 1 (a FAIL-shaped exit)
and leaks the workdir; under the audit's matching explicit triples `(0,1)`/`(0,0)` the driver's own
`local ... auto=0` declaration restores pristine behavior, so all four configs agree and the copy is
accepted. m1 never diverges on the compared tuple at all — the "removed on PASS" line is printed and
the deletion never happens.

### Ranking: BOUND-1 and BOUND-2 (fail-open, live at the pin)

- **BOUND-1 (head-config invisibility, false-accept, non-fail-closed).** A copy that destroys or
  rewires the head declarations its own tally block reads is accepted by every check while the real
  runner regresses under `--workdir`. C1's letter survives — m2 is *definitionally* an accept
  specimen under the counter's tuple (identical on every driver config and vector), and the sealed
  authoring rule extracts only the tally block, so its four-triple protocol is blind on the same
  axis ([INFERENCE] for `c1-measure.py` specifically, not executed by this seat; w1 reports its
  driver duplicates the tool's shim shape). But the v3 docstring's fix-2 rationale ("the runner's
  kept/removed contract, which also decides whether the workdir is deleted", `:26-29`) is only half
  realized: the line is compared, the declarations that steer it and the deletion itself are not.
- **BOUND-2 (print-vs-do gap, false-accept, non-fail-closed).** The oracle compares stdout text;
  `rm -rf "$root"` is unobservable, so the kept/removed contract's action half can be stripped
  without any config or vector noticing. Same scope note as BOUND-1.

These do not reopen w1's RevengerRootShape class (the real-root gate at `:789` kills that construction,
case green above); they are the *adjacent* head-side residual that A4 did not touch.

## 3. What the 29th case would have to assert

Numbering first: at the brief's count (28 cases, the `d16f9b5a` bytes) the "29th" already exists —
cases #29/#30 at this pin are the A4 real-root pair, both green. The class named in §2 is therefore
the **31st case**, concretely:

```python
('head auto decl stripped',
 text.replace('  local root specs auto=0\n', '  local root specs\n', 1),
 1, 'runtime'),
```

I seeded that case into a scratch copy of the tool (`work/patched/tally-audit-v3.py`, sha256
`5c583378cc8787c134704cdb694a1bd27dcccf1fc46f67adda3563f5d19948b3`, runner beside it byte-identical
to the pin) and ran its selftest — see the result line below; expected and observed: the case **cannot
pass today**, because the tool accepts the copy (exit 0 ≠ want 1). A 31st case of this class is
therefore not seedable against v3 as-frozen; for it to assert a kill, the tool needs one of:

1. the driver replays the copy's own head-context lines (the `local root specs auto=0` declaration
   and the root/`auto=1` construction, runner `:1357-1365`) inside `tally()` instead of fabricating
   `local root=%s auto=%s KEEP=%s` (`:390`) — the driver then inherits whatever the copy did to its
   declarations; or
2. a structural head-decl check alongside `check_head` (the declarations `auto`/`KEEP`/`root` must
   appear in the head exactly as the block's free variables require); or
3. an effect assertion: after PASS vectors under the `(1,0)` auto triple, stat the auto root —
   `removed on PASS` must correspond to a vanished directory (closes m1 directly).

Executed proof (`work/patched/tally-audit-v3.py` run above, 5m37.208s wall):

```
CASE head auto decl stripped FAIL (exit 0)
TALLY_AUDIT_V3_SELFTEST: 30/31 pass
PATCHED_SELFTEST_EXIT=1
```

The seeded case fails exactly as the tool verdict predicts — the auditor accepts the m2 copy (exit 0,
all four configs agree), so a kill assertion is unseedable against v3 as frozen; the 30 original
cases are untouched and green, isolating the failure to the new case.

## 4. What I could NOT break (with proof)

- **Guard-divisibility / offset forms (round-34 ResidueGuard2Divisibility class) are closed at v3.**
  Three seeded guard-predicate faults replacing `npass + nfail + nsetup != nlegs` (runner `:1453`,
  sole occurrence):
  - m3 `> nlegs * 2` — `72d70640fefc34476e75d6411914bb682eb1d59c3a6a182d00f8f307cb027d6a` →
    `CHECK runtime FAIL vectors=30316 mismatched=72; first: stress dup operand 0 cfg(1,0): got 0
    'REGRESSION: PASS (cases=9 passed=10 ...' , want 2 'SETUP (case-tally mismatch ...'` → exit 1.
  - m4 `( npass + nfail + nsetup ) % 4 == 3` — `3b926b5e9cd840826c655bd5a6fd3c18ed0cef9f49e34858053261cd7bad75f8` → same shape, exit 1.
  - m5 `== 11` — `e2f6ae29cc6a88cb23df7dacdbdd0aaede92c5bff18a85fee259db39b8eeb420` → same shape, exit 1.
  Mechanism: every oracle vector sums to 9, but the operand-dup/drop stress (`:527-537`) drives sums
  {10, 8}; any guard predicate that does not trip exactly off-9 diverges from pristine on the stress
  and is killed. The divisibility survivors measured against v2 do not survive v3's stress.
- **The four-triple sweep is pinned by the selftest**: reverting `CONFIGS` to the two round-34
  triples would flip cases `cfg-gated accept swap (0,0)` and `cfg-gated pass mask (1,1)` (`:777-780`)
  to exit 0 → selftest red (their divergence exists only under the (0,0)/(1,1) configs).
- **Full-stdout comparison is pinned**: `workdir-branch condition swap` (`:781-782`) diverges only in
  the REGRESSION_WORKDIR line under the real-root auto triple — green (exit 1, `runtime`).
- **The real-root gate behaves as A4 claims**: `real-root gated mask` killed (exit 1, `runtime`),
  `comment names real root` accepted (exit 0) — both at `:789-790`.
- **30/30 reproducibility** at the pin (single full run, 5m48.769s, exit 0); every kill case's
  `replace()` anchor applies (the `body == text` guard at `:805` would flag no-ops).
- **Runner byte pins** unchanged throughout: all mutants derive from `a7d3f2dd…912eb9` by one
  replacement each; the frozen artifacts were never written.

## 5. Hygiene (selftest machinery)

- **H1 — one kill case does not pin its failing check.** `in-block 7-bit mask` (`:766`) is the only
  want=1 case with `check=None`; the pass rule at `:813` accepts ANY failing check for it. A tool
  regression that kills that copy via `head` or `static` instead of `runtime` would still score
  green. Cheap fix: `1, 'runtime'` (the in-block mask diverges only at runtime).
- **H2 — dead no-op** at `:814-815`: `if not ok and p.returncode == 2 and want != 2: ok = False`
  assigns False to a value already False. Vestigial; delete or make it informative.
- **H3 — `then_regression` has zero seeded coverage.** `--then-regression` (`:708-728`: REGRESSION
  line must exist and name `cases=<nlegs>`) is never exercised by any case; a defect in that reporting
  path ships green.
- **H4 — selftest re-baselines silently on the runner beside it.** Cases are built from
  `os.path.join(HERE, 'mutate-and-run.sh')` (`:697-699`); selftest mode pins no runner sha, so a
  stale or wrong runner beside the tool re-derives all 30 cases from different bytes and stays green.

## 6. Bounds compliance

Every path absolute; scratch confined to `/fast/scratch/hyaku/tameshi-r35-seats/RevengerSelftest/`
(work + lane clone); the only file created under
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/` is this report. No git mutations anywhere; no
frozen artifact edited; no pacman; no tool installs (record per directive: none). Leak hygiene: all
witness roots created during the harness runs were removed after capture.

## 7. Evidence index

| claim | artifact |
|---|---|
| selftest 30/30, exit 0, 5m48.769s | command in §1; run in lane clone at pin |
| pins | sha256sum output in header table |
| m1/m2 tool ACCEPT | §2 CLI transcripts (vectors=30316 mismatched=0) |
| m2 real divergence | `work/cx_m2_autostrip_workdir.sh` run: exit 1, `auto: unbound variable`, workdir line missing, root survived |
| m1 real divergence | `work/cx_m1_rmstrip_auto.sh` run: exit 0, stdout identical shape, `ROOT_SURVIVED` vs pristine `ROOT_GONE` |
| guard forms killed | §4 CLI transcripts (m3/m4/m5, 72 mismatches each, exit 1) |
| 31st-case construction | `work/patched/tally-audit-v3.py` (sha256 in §3), selftest result in §3 |
| mutant hashes | §2/§4; pristine `a7d3f2dd…912eb9` |
