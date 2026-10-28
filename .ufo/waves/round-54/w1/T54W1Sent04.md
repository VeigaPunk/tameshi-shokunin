# T54W1Sent04 — sentinel attack: "print the class but exit 0", and "traceback on the same arm"

Axes: operability, calibration. Milestone: abuse the instruments.

Surface attacked: the frozen C2 counter `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c2/measure.py`
(blob identical at freeze `441c26be`, at `59c38109bf11`, and at `3146479c2138`; sha256
`b4684a3f555e8cbfda6fc9c7208827a3816a60cf53186269fdec41d5025e9e49`, 191 lines — shipped byte-exact as
`T54W1Sent04-receipts/counter-frozen-b4684a3f.py`).

Every run below evaluates the lane tree at `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0).
This seat edited no lane file: its only writes are in `.ufo/waves/round-54/w1/T54W1Sent04*`.
All git clones/fixtures live under `$HYAKU_SCRATCH/tameshi-r54/T54W1Sent04` and are deleted (§7).

## 0. The two clauses under attack

Frozen counter, `counter-frozen-b4684a3f.py:113-116`:

```
113|        ok = (rc == 2 and 'could-not-evaluate' in text and str(unusable) in text
114|              and 'Traceback (most recent call last)' not in text)
115|        exit2 += ok
116|        naming += ('could-not-evaluate' in text and str(unusable) in text)
```

`ok` (accumulated into `unusable_exit2`) is the operative cell and carries three independent
guards: exit code 2, the class string, and *no traceback*. `naming` is a pure diagnostic: it
never looks at the exit code or the traceback. The item below attacks each guard separately.

## 1. Instrument proxy: how a patch reaches the tree the counter measures (disclosed)

`measure.py` runs `git clone --shared <lane> <work>/clone` + `git -C <work>/clone checkout <rev>`
before running any tool (`counter-frozen-b4684a3f.py:99-103`), so a patch held only in a scratch
working tree is discarded. The seat bounds forbid `git commit` / `git add` / `git reset`
anywhere, so the patch is injected at the one point where the counter materialises its own tree:

`T54W1Sent04-receipts/git` (sha256 `5c516788fbc0f27a69d47d1926b1ef8aee889514c35d8f95306437f2ce2ad138`) is a
git on `PATH` that passes every invocation through to `/usr/bin/git` and, after a *successful*
`git -C <work>/clone checkout`, runs `git -C <work>/clone apply <patch>`. It writes nothing
except that patch, into the throwaway clone the counter itself created, and it only fires when
the repo path is `<SHIM_WORK>/clone`.

The counter file itself is never modified (sha printed in every receipt). Each run's receipt
ends with `git -C <work>/clone diff`, i.e. the exact bytes the counter measured — the patch is
in the tree, not in the counter.

## 2. Run 1 — ATTACK A: print the class, exit 0

Target: `tools/env-diff.py --selftest`, unusable-TMPDIR arm. Exact patch bytes
(`T54W1Sent04-receipts/attackA-env-diff-exit0.patch`, sha256
`098cddd22092ddd1183c220386a005c11fb6b3af08f3030092266addf38e665f`, 440 bytes):

```
--- a/tools/env-diff.py
+++ b/tools/env-diff.py
@@ -231,8 +231,8 @@
     if a.selftest:
         try:
             return selftest()
         except ScratchRootUnusable as exc:
             print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
-            return 2
+            return 0
     if not a.contract or not a.out or not 1 <= a.jobs <= 3:
         p.error("--contract and --out are required; --jobs must be 1..3")
```

Command (driver `T54W1Sent04-receipts/run-attack.sh`, full output in
`T54W1Sent04-receipts/run-a-frozen-counter.out`):

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r54/T54W1Sent04; R=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1Sent04-receipts
env S="$S" PATCH="$R/attackA-env-diff-exit0.patch" WORK="$S/work-a2" COUNTER="$S/measure-frozen.py" sh "$R/run-attack.sh"
```

Output (verdict line, verbatim):

```
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=6 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
COUNTER_RC=1
```

and, in the same output, the one cell that moved (the other six `EXPLAIN unusable` lines stay
`rc=2`, verbatim in the receipt):

```
EXPLAIN unusable env-diff rc=0 line='ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory:'
```

**Verdict A: caught. `C2_R54_PASS=false`, `unusable_exit2=6` (7→6).**
The tool still prints the class and names the TMPDIR value, so `naming` stays 7/7; only the
exit-code guard separates the attack from the contract. An earlier run of the same patch
(`unusable_exit2=6 … usable_ok=6 … total=2`, 353 s; transcript only, not tee'd) and this run (`total=1`, 129 s) differ only
in the usable arm — see §5.

Arm-level ablation on the patched tree, rubric recomputed verbatim from the counter
(`T54W1Sent04-receipts/ablation-arms.out`):

```
== ATTACK A env-diff, TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Sent04/never-created (never created)
rc=0  counter_ok=False  counter_naming=True  traceback_in_text=False
last_line="ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyak"
```

## 3. Run 2 — ATTACK B: same arm, but with a traceback

Target: `tools/pin-disposition.py --selftest` (a *different* tool), unusable-TMPDIR arm. It keeps
the naming line and the exit code 2 and adds a traceback — the case a rc+naming-only check would
wave through. Exact patch bytes (`T54W1Sent04-receipts/attackB-pin-disposition-traceback.patch`,
sha256 `2d62e936bc7093e860687eb39f319776bba7231f2be9f287a60fb16cbbc268a4`, 499 bytes):

```
--- a/tools/pin-disposition.py
+++ b/tools/pin-disposition.py
@@ -1396,8 +1396,10 @@
     if argv == ["--selftest"]:
         try:
             return selftest()
         except ScratchRootUnusable as exc:
             sys.stderr.write("pin-disposition.py: could-not-evaluate: {}\n".format(exc))
+            import traceback
+            traceback.print_exc()
             return 2
     if "--selftest" in argv:
         return invalid_input("invalid_usage", "--selftest takes no other arguments")
```

Command (full output `T54W1Sent04-receipts/run-b-frozen-counter.out`):

```
rm -rf "$S/work-b"
env S="$S" PATCH="$R/attackB-pin-disposition-traceback.patch" WORK="$S/work-b" COUNTER="$S/measure-frozen.py" sh "$R/run-attack.sh"
```

Output (verdict line, verbatim):

```
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=6 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
COUNTER_RC=1
```

the pin cell in the same output:

```
EXPLAIN unusable pin-disposition rc=2 line="ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratc"
```

**Verdict B: caught — by the traceback clause alone.** Exit code is 2 and both strings are
present (`naming=7`), so the rc guard and `naming` both let this tool through; only
`'Traceback (most recent call last)' not in text` rejects it.

Arm-level ablation (`T54W1Sent04-receipts/ablation-arms.out`):

```
== ATTACK B pin-disposition, TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Sent04/never-created (never created)
rc=2  counter_ok=False  counter_naming=True  traceback_in_text=True
traceback_lines=1
last_line="ScratchRootUnusable: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/…"
```

The rule also holds against the peer-amended counter that was uncommitted in the working tree at
`3146479c2138` (sha256 `49280fe55bd9361c284ddb1b9e757fd3ec3267f60eed4ca587e1bfe446b718c8`,
receipt `run-b-amended-counter.out`):

```
C2_R54: rev=59c38109bf11 tools=7 unusable_exit2=6 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=1 C2_R54_PASS=false
```

## 4. Result summary

| run | counter bytes | patch | unusable_exit2 | naming | total | PASS |
|---|---|---|---|---|---|---|
| baseline (unmodified) | b4684a3f (see note) | none | 7 | 7 | 1 | false (usable_ok=6, §5) |
| A (env-diff → 0) | b4684a3f | A | **6** | 7 | 2 | **false** |
| A rerun | b4684a3f | A | **6** | 7 | 1 | **false** |
| B (pin-disposition → rc2+traceback) | b4684a3f | B | **6** | 7 | 1 | **false** |
| B on amended counter | 49280fe5 | B | **6** | 7 | 1 | **false** |

The baseline row is transcribed in `T54W1Sent04-receipts/run-baseline-unmodified.out`; that one
run predates the driver's counter-hash echo (the counter file was not hashed at the time), and its
`usable_ok=6` matches the frozen traced-rc behaviour while contradicting the plain-rc amendment —
the attack runs above are the ones pinned to a printed sha256.

The instrument is not fooled by either attack: the exit-code guard catches A, the traceback
guard catches B, and neither attack can be expressed as `PASS=true`. Two consequences for
calibration:

1. `naming` is not a check. It reads 7/7 under both attacks; a reader who treats `naming=7` as
   "the exit class is contracted across seven tools" is misreading the verdict line. Only
   `unusable_exit2` carries that claim (`counter-frozen-b4684a3f.py:113-116`).
2. The traceback clause is load-bearing, not cosmetic: B would pass a rc+string-only rubric
   (rc=2, class present, TMPDIR named) while emitting a traceback at the operator.

## 5. Finding (operability/calibration): the frozen `usable` arm is not hermetic

Severity: **medium** — it is the one arm of the frozen counter whose verdict is not reproducible
from the same rev and the same counter bytes, and it is the arm that decides claim C2's third
sentence ("7/7 exit 0 … on a usable root with no mkdir under /tmp").

Evidence, frozen counter at `59c38109bf11`, identical input tree and TMPDIR; the runs differ only
in how long they took:

| wall time of the whole counter run | usable_ok |
|---|---|
| 353 s (attack A, first run; transcript only) | 6 |
| 347 s (baseline, unmodified; run-baseline-unmodified.out) | 6 |
| 129 s (attack A rerun) | 7 |
| 110 s (attack B) | 7 |

The failing cell is always `registry-check` (both 6-runs printed
`EXPLAIN usable registry-check rc=1 tmp_mkdirs=0`). Cause, measured directly in a `git clone
--shared` of the lane checked out at C0 with a fresh usable TMPDIR
(`T54W1Sent04-receipts/registry-usable-arm-probe.out`):

```
== ARM 1: plain run (no tracer)
rc=0  fails=0  tail='SELFTEST: PASS (51 cases)'

== ARM 2: exact command the frozen counter uses on its usable arm
rc=1  mkdir-/tmp-hits=0
  SELFTEST_CASE timeout-kills-setsid-pipe FAIL (exit=1 elapsed=4.979s survivor=False marker=False)
  SELFTEST_CASE timeout-kills-setpgid-pipe FAIL (exit=1 elapsed=5.099s survivor=False marker=False)
  SELFTEST: FAIL (2 of 51 cases: timeout-kills-setsid-pipe, timeout-kills-setpgid-pipe)
```

Same tree, same TMPDIR, same interpreter (3.14.8), one variable: the tracer. The two failing cases
are exactly the timeout-kill timing tests; reproduced twice independently
(`elapsed=9.804s`/`8.247s` in the first probe, `4.979s`/`5.099s` in the shipped one, against ~1.6 s
unwrapped). mkdir-under-/tmp hits are 0 in both arms, so the arm's *substance* is intact — only its
rc measurement is contaminated.

So `usable_ok` measures the tracer (and host load) in addition to the tool, for a selftest that
deliberately exercises timeout-kill timing. The frozen claim "7/7 exit 0 on a usable root" is not
reproducible at C0 with the frozen counter: I measured 6/7 twice and 7/7 twice.

Smallest remediation: the rc arm should be the plain run (`usable_ok += (rc_plain == 0 and
hits == 0)`), with the traced run contributing only the mkdir census — exactly the amendment
already sitting uncommitted in the working tree at `3146479c2138` (`counter-frozen-b4684a3f.py:129-134`
replaced). This seat did not apply it (no lane writes) and this measurement is independent of it.
Under that amended counter, the attack in §3 still fails (`unusable_exit2=6`), so the amendment
does not weaken the exit class.

## 6. Scope, and what this seat did not measure

Attacked/measured: the three guards of `ok` (rc, class string, traceback) for two of the four
C0-patched tools, and the stability of the `usable` arm. Not measured here (no receipt, not
claimed): the `docs` cell test (`'TMPDIR'`, `'empty'`, `'could-not-evaluate'` as bare substrings of
a registry cell, `counter-frozen-b4684a3f.py:138-150`), the `note`/`sources` gate
(`counter-frozen-b4684a3f.py:152-169`), and the `empty` arm. Those belong to other seats; I ran no
partial experiment on them and make no statement about them.

Other observations from the runs: the lane's `HEAD` moved under this seat
(`59c3810` → `99c3bc8` → `3146479c2138` → `097985c18b9a`) and `c2/measure.py` was edited
uncommitted mid-flight, so every receipt above pins both the rev (`59c3810…`) and the counter
sha256 it actually executed.

## 7. Reproduce, and scratch hygiene

Reproduce (any empty `WORK` dir, from a machine with `strace`):

```
export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r54/T54W1Sent04
R=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1Sent04-receipts
mkdir -p "$S" && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 441c26be:.ufo/evidence/round-54/c2/measure.py > "$S/measure-frozen.py"
env S="$S" PATCH="$R/attackA-env-diff-exit0.patch"             WORK="$S/work-a" COUNTER="$S/measure-frozen.py" sh "$R/run-attack.sh"
env S="$S" PATCH="$R/attackB-pin-disposition-traceback.patch"  WORK="$S/work-b" COUNTER="$S/measure-frozen.py" sh "$R/run-attack.sh"
```

Fixtures shipped: `git` (shim), `run-attack.sh` (driver), both `.patch` files,
`counter-frozen-b4684a3f.py`, and the six `.out` receipts.

Scratch: `$HYAKU_SCRATCH/tameshi-r54/T54W1Sent04` (1.3 GB: clone fixtures plus the frozen-counter
copy) was removed after the receipts were copied out —

```
rm -rf -- "$S"; echo "RM_RC=$?"          -> RM_RC=0
test -e "$S" && echo STILL_PRESENT || echo SCRATCH_REMOVED   -> SCRATCH_REMOVED
```

so no seat tree is left behind.

Tooling: nothing installed or upgraded (no package, no `uv tool`, no PATH write).

Census at report time: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `ok …/corpus/SOURCES.md`, exit 0 (only informational W04 duplicate-url rows).
