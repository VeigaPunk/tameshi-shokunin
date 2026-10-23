# AttackTransientExit — exit/stdout tuple probe (round 35, wave 2)

Seat: `L1tameshi35.AttackTransientExit` (leaf). Assigned pin `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`
(lane tip at dispatch). Lane clone at `/fast/scratch/hyaku/tameshi-r35-seats/AttackTransientExit/lane`,
read-only; all mutants and receipts under `/fast/scratch/hyaku/tameshi-r35-seats/AttackTransientExit/`.

Frozen bytes actually audited (sha256, `sha256sum`, re-checked after every run):

```
ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885  lane/tools/tally-audit-v3.py
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  lane/tools/tally-audit-v2.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  lane/tools/mutate-and-run.sh
515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8  lane/.ufo/evidence/round-35/c1/c1-measure.py  (counter at the pin)
```

`tools/tally-audit-v3.py` at the current lane HEAD `68f2557` is byte-identical to the pin
(`git show HEAD:tools/tally-audit-v3.py | sha256sum` = `ef98fc53…`), so every finding below is against
current tool bytes, not only the dispatch pin.

## 1. What I attacked

C1 surface item (2): *"the compared tuple is the FULL stdout, not the first line"* (contract.json,
`claims[0].surface`), implemented in `run_vectors` (`tools/tally-audit-v3.py:376-398`) and mirrored in
the counter's `run_block` (`c1-measure.py:163-188`).

The runtime check never compares raw bytes. Each tally run's stdout is projected through a
one-line transport (`tally-audit-v3.py:392-398`):

```python
lines.append('out=$(tally %s ...); rc=$?; printf "R\\t%%s\\t%%s\\n" "$rc" "${out//$\'\\n\'/$\'\\x1f\'}"')
...
got = [ln.split('\t', 2) for ln in out.split('\n') if ln.startswith('R\t')]
return [(int(g[1]), (g[2] if len(g) > 2 else '').replace('\x1f', '\n')) for g in got]
```

The compared tuple is therefore a *projection* of the block's stdout with two non-injective rules:

1. **`$(...)` strips every trailing newline** (bash command substitution). A missing final LF, or any
   number of trailing blank lines, maps to the same projection.
2. **`0x0A → 0x1F` with no escaping, then `0x1F → 0x0A` on read.** Any literal US byte a copy emits is
   indistinguishable from a line break.

`oracle` (`tally-audit-v3.py:401+`) builds its expected string from bare `'\n'` joins, so the comparison
is exact *within the projection* and blind *across* it. My probe changes only the separator/newline
bytes at the smallest behavior-bearing point (one `printf` in the FAIL branch).

## 2. Result matrix

Copies built by the inherited attempt-1 builder `mk.py` from the pinned runner bytes; each edit asserted
to apply exactly once; lane never written. Detector = the tool's default mode, exit code + `CHECK` lines.
v3 vectors = 30316 (4 configs), v2 vectors = 15158 (2 configs).

| copy | real stdout divergence | v3 `ef98fc53` | v2 `7b11ba25` |
|---|---|---|---|
| `order-swap-fail` | lines reordered (FAIL) | **KILLED** runtime FAIL 3600 | KILLED |
| `order-swap-pass` | lines reordered (PASS) | **KILLED** runtime FAIL 40 | KILLED (20) |
| `trail-nl-missing` | final LF removed | **ACCEPTED** | ACCEPTED |
| `trail-blank-line` | extra trailing blank line | **ACCEPTED** | ACCEPTED |
| `interior-blank-line` | blank line between lines | **KILLED** 3600 | ACCEPTED (first-line blind) |
| `leading-blank-line` | blank line before line 1 | **KILLED** 3600 | KILLED |
| `us-separator` | `0x1F` instead of `0x0A` between the lines | **ACCEPTED** ← | **KILLED** ← regression |
| `sigpipe-ignore` | `trap '' PIPE`: exit 141→0 under a closed reader | **ACCEPTED** | ACCEPTED |
| `drop-rm` | workdir not removed on PASS | **ACCEPTED** | ACCEPTED |
| `stderr-noise` | stderr only | ACCEPTED (declared) | not run |

Exact FAIL-branch tuples (vector `1 0 0 0 0 0 0 0 0`, fixed root `/tmp/tameshi-r4-2-regression.consumer`,
`auto=0 KEEP=1`; `probe.py` and the byte loop in §9):

```
pristine        rc=1 len=115 sha256=a41969a01d33a703cb0d1922c139bb92ce99100754a3a7de6814f2afe0b81387 lines=2
  b'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.consumer (kept)\n'
us-separator    rc=1 len=115 sha256=435862412d9d0070af39cf5985fce5cf88b6ee99a01ccd9e97cbc1db431a6443 lines=1
  b'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\x1fREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.consumer (kept)\n'
trail-nl        rc=1 len=114 sha256=98e52992be494d15787a529ab36fb9e1fff2acde11671239bbac35d6c3c75afb LF=False
  b'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.consumer (kept)'
trail-blank     rc=1 len=116 sha256=05717cb2d315af8a083ff21ea8b0be176d24872d9ce7a087551c5bf03a872498 lines=3
  b'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.consumer (kept)\n\n'
interior-blank  rc=1 len=116 sha256=eb6918531dcf1e8edf7c8fa3ff8c20b60a7f44b15d2409406307180ef1da1221 lines=3
leading-blank   rc=1 len=116 sha256=6edecef15223cabf6ea5afceff1858d9ba1cbc54bbcdea635c4e21632693bcf2 lines=3
```

## 3. CRITICAL — the `0x1F` transport collision: a copy v2 killed and v3 accepts

`us-separator` differs from the pinned runner by exactly one `printf` (`diff -u`, mutant sha256
`d0d68ad9f0771d1919400740aadaf935d8d50ea79a059b42c943247e766142df`):

```diff
@@ -1439,9 +1439,8 @@
   if [[ $nfail -gt 0 ]]; then
-    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
-      "$nlegs" "$npass" "$nfail" "$nsetup"
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
+    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\037REGRESSION_WORKDIR: %s (kept)\n' \
+      "$nlegs" "$npass" "$nfail" "$nsetup" "$root"
     exit 1
   fi
```

**v3 ACCEPTS it** — exit 0:

```
$ python3 lane/tools/tally-audit-v3.py --runner mutants/us-separator.sh; echo $?
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
0
```

**v2 KILLS it** — exit 1:

```
$ python3 lane/tools/tally-audit-v2.py --runner mutants/us-separator.sh; echo $?
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime FAIL vectors=15158 mismatched=1800; first: cfg(0,1) statuses 1 0 0 0 0 0 0 0 0: got (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\x1fREGRESSION_WORKDIR: tally-audit (kept)'), want (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)')
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: FAIL (head=pass static=pass runtime=fail harness=pass)
1
```

Why v2 caught it: v2's transport truncates at the first *real* newline
(`"${out%%$'\n'*}"`, `tally-audit-v2.py:268-283`), so the single US-joined line never matched the
expected first line. v3 replaced that truncation with a sentinel round-trip, which is **strictly weaker
in this dimension**: an in-band separator emitted by the copy is rewritten into exactly the two lines the
oracle expects.

Behaviourally the copy diverges on **every** config and **every** message-bearing vector — raw stdout
hashes differ while the tool's projection is identical (`probe.py`, all four triples):

```
cfg=(auto=1,KEEP=0) vec=one-1: pristine rc=1 len=118 sha=4c186e1d1468b796
                               us-sep    rc=1 len=118 sha=dd745389b7358a3d   (1 line vs 2)
    NORMALISED identical: (1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.hnttb3ol (kept)')  match_to_oracle=True
cfg=(auto=1,KEEP=1) same pair (4c186e1d… / dd745389…)
cfg=(auto=0,KEEP=1) pristine 1221d702f406a3fb / us-sep 2733da33e87bc99c
cfg=(auto=0,KEEP=0) pristine 70869daf43f98087 / us-sep 174e0e8933baf0c7
```

Consumer-visible: under the FAIL vector, `grep -c '^REGRESSION_WORKDIR'` returns **1** for pristine and
**0** for the copy; line count 2 vs 1; `rc=1` both. The runner's two-line output contract is broken by a
copy the audit certifies as byte-equivalent.

Claims falsified:

- C1 surface (2) "the compared tuple is the FULL stdout" — false; it is the full *projection*. The
  projection is not injective in `0x0A`/`0x1F` and not length-preserving at the tail.
- C1 predicate "kills every kill specimen (divergent behavior under at least one of the four configs;
  failing check exactly `runtime`)" — this specimen diverges under all four and the failing check is
  none: `runtime PASS`.
- Per the seat's ranking rule ("a class v2 caught and v3 now accepts is a CRITICAL regression"): v2
  caught it (exit 1, `runtime FAIL`), v3 accepts it (exit 0, `runtime PASS`). **CRITICAL.**

## 4. The oracle has the same blind spot (independence failure)

The C1 counter cannot arbitrate this class either. At the pin (`c1-measure.py` sha `515b0b1b…`) and at
HEAD (`d27e6769…`) its transport is the same sentinel encoding — `SEP = '\x1f'` (line 55), the
`${out//$'\n'/$'\x1f'}` printf (line 172), the `replace('\x1f','\n')` read (line 182) — and its
`behavior`/`diverge` are defined over that projection (`c1-measure.py:204-217`). Running the counter's
own oracle on both blocks:

```
COUNTER diverge(pristine, us-separator) = []      # all four configs, 267 vectors each
cfg=(auto=1,KEEP=0) tuples=267 divergent=False
   pristine[2]=(1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression._9zvwqcm (kept)')
   us-sep  [2]=(1, 'REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)\nREGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression._9zvwqcm (kept)')
(groups (1,1), (0,1), (0,0) identically divergent=False)
raw, same vector: pristine sha256=97eeb7b2b3e8ad4a… (2 lines) / us-sep c1e64eb9914191e8… (1 line)
```

Consequence: the sealed-authoring ground truth would **label this copy an accept specimen** (behaviourally
identical), so the measurement can never fail on it — the object-under-test and its oracle share a
non-injective encoding. By the seat rule, ground truth is behaviour, and behaviour (raw `(rc, full stdout)`)
diverges; so the specimen is a kill specimen that both the tool and the counter misclassify. This is the
precise way C1 is false: not "the panel happens to miss a class", but "the comparison operator is lossy
and the oracle reuses it".

Minimal repair: carry the block's stdout out-of-band rather than inline. Either (a) run each vector in its
own bash process and compare `(rc, hashlib.sha256(stdout))` against an oracle hash over the exact bytes,
or (b) emit records with an explicit byte length (`printf 'R\t%s\t%s\n' "$rc" "${#out}"` + the raw bytes
on a separate fd), or (c) hex/base64 the captured bytes. Any of these makes the tuple injective; the
counter must adopt the identical encoding independently (or, better, compute expected bytes directly and
diff them).

## 5. BOUNDs (real, fail-open, but not claims-false on this evidence)

**BOUND-1 — final newline is not compared (both tools).** `trail-nl-missing`
(`b49989bd…`): rc=1, 114 bytes, sha `98e52992…`, `LF=False`, versus pristine 115 bytes / `a41969a0…`.
`$(...)` strips it; v3 exit 0 and v2 exit 0. No consumer-observable difference (`grep`, `read`, regex all
parse identically); it falsifies the word "FULL" at byte level but not the round-34 hold fix #2 targets.

**BOUND-2 — trailing blank lines are not compared (both tools).** `trail-blank-line` (`e7af0414…`):
rc=1, 116 bytes, sha `05717cb2…`, 3 newlines. v3 exit 0, v2 exit 0. An *interior* blank line is caught
(v3 FAIL 3600), so the blind spot is exactly the post-command-substitution tail.

**BOUND-3 — SIGPIPE disposition / exit 141 is invisible (both tools).** `sigpipe-ignore`
(`cb4799fc…`) adds `trap '' PIPE` at the top of the tally block. Deterministic closed-reader probe
(pipe read end closed before spawn): pristine `rc=-13` (killed by SIGPIPE = shell 141), copy `rc=0`.
The audit's transport drains the pipe (`capture_output`), so both project identically and v3/v2 exit 0.
Real only when the runner's stdout reader closes early (`--regression | head -1`); not observable in any
drained run.

**BOUND-4 — the removal decision is printed, never checked (both tools).** `drop-rm` (`1d3d121d…`)
keeps the `(removed on PASS; --keep retains)` line but deletes the `rm -rf`. Under the runner default
(`auto=1 KEEP=0`, PASS): pristine `dir_exists_after=False`, copy `dir_exists_after=True`, stdout identical
in shape; both tools exit 0. This is an *accept* specimen under the contract's own ground truth (identical
`(exit, stdout)`), so the tool is not wrong to accept it — but the tool's stated rationale for comparing
the WORKDIR line ("which also decides whether the workdir is deleted", docstring line 20) is only half
enforced: the wording is compared, the side effect is not. Rank BOUND, not CRITICAL.

## 6. What I could NOT break (proofs)

- **Line order, both branches.** `order-swap-fail` FAIL branch: v3 `runtime FAIL`, 3600 mismatches, first
  `got 1 'REGRESSION_WORKDIR: … (kept) | REGRESSION: FAIL (…)' want 1 'REGRESSION: FAIL (…) | REGRESSION_WORKDIR: … (kept)'`.
  `order-swap-pass` PASS branch: v3 `runtime FAIL`, 40 mismatches. Full-stdout comparison catches order.
- **Blank lines with position.** `interior-blank-line` and `leading-blank-line`: v3 `runtime FAIL`, 3600
  each. (v2 accepted the interior one — v3 is stronger there, which is the correct direction of fix #2.)
- **stderr-only** (`ae8e1459…`): v3 exit 0, by documented design (stdout-only comparison, round-32 M1).
- **Structural checks are not leaked into by printf-only copies**: head/static/harness PASS on every
  mutant above, so the runtime oracle is the *sole* defence on this face and the defect sits squarely in
  round-35 fix #2, not in the round-34 checks.
- **No mismatch-count hiding**: the projected counts (`cases/passed/failed/setup`) are reconstructed and
  compared exactly; I found no separator placement that alters them without also altering the projection
  in a detectable way. Only line *structure* is collidable.
- **Pinned runner untouched**: `git -C lane status --porcelain` = 0 lines; runner sha `a7d3f2dd…` before
  and after all runs; tool sha `ef98fc53…`, v2 sha `7b11ba25…`.

## 7. Coverage gap

`python3 lane/tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 30/30 pass` at the pin.
No selftest case emits an in-band `0x1F` or drops a trailing newline from the tally block, so the
self-test cannot see either class. A runner-copy case built with `\037` (expected `runtime` FAIL) would
fail today and would have caught this regression; a trailing-newline case needs the byte-level tuple fix
first (otherwise it cannot be expressed).

## 8. Hygiene

- `run_vectors` docstring still says *"return [(rc, stdout first line)]"* (`tally-audit-v3.py:377`) and
  the module docstring's runtime item still says "Exact stdout first line and exit code compared"
  (line 77), stale after fix #2. The oracle docstring's "FULL stdout" (line 402) is the claim this seat
  falsifies at byte level.
- Known and not re-reported: the counter at the pin `515b0b1b…` still carries the stale `TOOL_SHA256`
  constant that amendment A6 fixes at HEAD (`f9df589`/`68f2557`); the counter at HEAD is `d27e6769…`.
- No installs, no `pacman`, no mutating git/jj. `/fast` had 1.8 GB free at start; heavy temp dirs were
  placed in `/tmp`. The scratch lane already existed from attempt 1 at `d16f9b5` (setup's clone refused,
  `fatal: destination path … already exists`); I fetched `7da6e07` incrementally from the lane and
  checked it out detached (`FETCH_OK`/`CHECKOUT_OK`, `rev-parse HEAD` = `7da6e076c2e2…`). The inherited
  `mk.py` mutant builder was re-run against the pinned runner bytes and every edit asserted single-match.

## 9. Reproduction

```sh
S=/fast/scratch/hyaku/tameshi-r35-seats/AttackTransientExit; cd "$S"
python3 mk.py                                            # builds mutants/*.sh, prints sha256 each
python3 lane/tools/tally-audit-v3.py --runner mutants/us-separator.sh;      echo "v3 exit=$?"
python3 lane/tools/tally-audit-v2.py --runner mutants/us-separator.sh;      echo "v2 exit=$?"
python3 probe.py lane/tools/mutate-and-run.sh mutants/us-separator.sh      # raw vs projected tuples, 4 triples
# counter oracle on the same two blocks (HEAD counter extracted to c1-measure-head.py, sha d27e6769…):
python3 -c "import importlib.util,tempfile; s=importlib.util.spec_from_file_location('c','c1-measure-head.py'); c=importlib.util.module_from_spec(s); s.loader.exec_module(c); t=tempfile.mkdtemp(); a=c.behavior(open('lane/tools/mutate-and-run.sh').read(),t); b=c.behavior(open('mutants/us-separator.sh').read(),t); print(c.diverge(a,b))"
```

Receipts retained: `work/v3-*.out`, `work/v2-*.out`, `work/probe-pristine-us.out`, `mutants/*.sh`,
`mk.py`, `probe.py`, `c1-measure-head.py`.

## 10. Verdict

**CRITICAL** at `ef98fc53…` (and at HEAD, same bytes): the round-35 "whole-stdout" fix compares a
non-injective newline projection, so a copy whose real stdout differs only in the LF/US separator is
accepted (`TALLY_AUDIT: PASS`, exit 0) while v2 killed it (`runtime FAIL`, exit 1); the C1 counter's
ground truth shares the same projection and reports `diverge = []`. **BOUND**: final-newline removal,
trailing blank lines, SIGPIPE/141 disposition, and the unobserved workdir removal. **Closed**: line
order (both branches), interior/leading blank lines, stderr-only, and every structure-side check.
