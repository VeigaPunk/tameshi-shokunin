# T55W1Revenger — why round 54's phase-B control cloned the freeze, and what a control that cannot repeat it looks like

Seat: T55W1Revenger (revenger, leaf). Round 55 / hyaku run 11, wave 1.
Scope: the phase-B control contract of `.ufo/evidence/round-54/control/controls.sh`, its gate in
`deciding-run.sh`, round-54 `contract.json`'s control list — and round 55's `controls.sh` checked
against the minimal shape that cannot repeat the error. Judges on **calibration**; milestone:
reconstruct round-54's control intent.

Everything below is measured on committed bytes or on clones of them. Lane state at the time of
writing: tip `133b2ce6` (`round-55: freeze amendment 8`), base `0a2010ac`, round-55 freeze resolved
from `631cd645` to `133b2ce` by amendments 1-8. No lane production file was edited; every fixture
lives under `/fast/scratch/hyaku` (scratch) and every clone's `rev-parse --show-toplevel` was
asserted equal to the clone before any commit in it.

---

## 1. The reconstructed contract (what the harness author intended)

Three artifacts agree, and none of them is the receipt:

1. **The harness header** (`.ufo/evidence/round-54/control/controls.sh:1-13`, unchanged since
   `441c26be`, the pre-seat commit):

   > "Phase A is scored at the FREEZE bytes, before any round work; phase B at the **final content
   > revision**, before the deciding run."
   > "Every control runs the **FROZEN counter bytes** (extracted from FREEZE into scratch), never
   > the working tree, over a `git clone --shared` of the lane **at the revision the control
   > names**."

2. **The signature** separates the two roles into two positional slots:
   `controls.sh b LANE FREEZE REV OUTDIR`. `FREEZE` is used *only* to extract the counter bytes
   (`git show "$FREEZE:$E/c1/measure.py"` …); `REV` is used *only* as the clone target
   (`clone_at "$LANE" "$REV" …`). The counter is then invoked with
   `--rev "$(git -C "$d" rev-parse HEAD)"`, i.e. the clone's own HEAD — so the receipt records the
   revision actually scored.

3. **The in-body comments and the contract**: `# CTL_POS — the real repair at REV must pass both
   counters`; `# CTL_EXIT0 — a tool made to print the class line but return 0 must fail C2`.
   `contract.json` `claims.C1.controls = [CTL_0, CTL_FAB, CTL_LOGINPUT, CTL_POS]`,
   `claims.C2.controls = [CTL_0, CTL_EXIT0, CTL_POS]`, with `CTL_POS_*` pre-registered **true** and
   the rest **false**.

So the intended contract is: **the instrument is frozen at FREEZE; the subject is the tree at REV;
the receipt records both**. A phase-B control is an assertion about the tree named by `REV`, using
the bytes frozen at `FREEZE`.

## 2. Why it cloned the freeze — the mechanism, in four facts

**Fact 1 — the harness never hardcoded FREEZE.** The phase-B clone line is `"$REV"` at *every*
revision of the file I checked (`441c26be`, `19c7558`, `077d431e`, `c2108100`), including the
phase-B block at `:142/+145/+149`. There is no code path that substitutes FREEZE for REV.

**Fact 2 — it was handed the freeze.** `controls-b.stdout`, unchanged across all five commits that
touch it, prints `rev=077d431e6996` on both `CTL_POS` lines. `077d431e` *is* the round-54 freeze
(`freeze.json` at that commit; `after/frozen.stdout` prints `freeze=077d431e6996…` while the round
decided at `rev=c21081008adb`). The counters echo their clone's HEAD, so the receipt itself names
the tree that was scored. The mismatch was printed in the receipt the round went on to cite as
proof.

**Fact 3 — the content revision did not exist when phase B ran.**
`controls-b.stdout` first appears in commit `7fa9a5e` (`2026-10-28 12:21:35`); `7fa9a5e^` **is**
`077d431e` (the freeze, `12:12:06`). The revision the round actually decided at, `c2108100`, is
`12:22:15` — **40 seconds after** the receipt was committed. So at the moment phase B ran, the only
commit that existed beyond the freeze's parent chain was the freeze itself; the "final content
revision" it was supposed to certify was not yet a commit. The harness had a correct parameter and
no correct value to put in it.

**Fact 4 — the numbers are the fingerprint of a half-carrying tree.** Replaying the *frozen* round-54
counter bytes over a clone at the freeze reproduces the receipt byte-for-byte
(`T55W1Revenger-receipts/freeze-scored-counters.stdout`):

```
C1_R54: rev=077d431e6996 … credited=60 lost=4 rekeyed=3/7 readers=6/7 monitor=6/60 unstable=0 total=4 C1_R54_PASS=false
C2_R54: rev=077d431e6996 tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true
```

That is exactly the `2/3`: **C2 passes at the freeze because C2's work (`99c3bc88`) is an ancestor
of the freeze, while C1's work — the 23-heading re-key — landed at `7fa9a5e`, which is not.** One
pre-registered `true` was reachable on that tree and one was not. The receipt is not a broken
instrument; it is a correct measurement of a tree that carried half the round.

**Fact 5 — the harness was right, and one argument proves it.** Re-running the *same committed
round-54 bytes* with `REV=c21081008adb` (`T55W1Revenger-receipts/r54-phaseB-at-certified-rev.stdout`):

```
CTL CTL_POS_c1 … rev=c21081008adb … credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 … total=0 C1_R54_PASS=true
CTL CTL_POS_c2 … rev=c21081008adb … total=0 C2_R54_PASS=true
CTL CTL_EXIT0  … C2_R54_PASS=false
CONTROLS_B: 3/3 as pre-registered
```

**3/3.** The counter, the harness and the pre-registration were all sound. The defect was a wrong
argument, and the harness had no guard and no receipt of its arguments (`OUTDIR`, the 5th
positional, is parsed and **never used** — neither round writes anything to it, so the only trace of
an invocation is the counter line's `rev=`).

## 3. Why the error survived: the gate cannot see a failed control

`deciding-run.sh:52-59` is the whole control gate, and it is byte-identical in rounds 54 and 55:

* each of the four receipts must be a **blob at REV**, **non-empty**, and its **last touching
  commit** must descend from FREEZE;
* plus `grep -q '^CONTROLS_A: [0-9]*/[0-9]* as pre-registered'` (and the same for `B`).

Executed verbatim against the committed bytes at `c2108100` (`gate-reproduction.stdout`):

```
controls-a.stdout blob 853  descends-from-freeze=yes      controls-a verdict: GREP PASSES
controls-a.exit   blob 104  descends-from-freeze=yes
controls-b.stdout blob 654  descends-from-freeze=yes      controls-b verdict: GREP PASSES
controls-b.exit   blob 104  descends-from-freeze=yes
controls-b.exit    = 1
controls-b verdict = CONTROLS_B: 2/3 as pre-registered
CTL_MISMATCH lines = 1
  CONTROLS_B: 0/3  -> ACCEPTED
  CONTROLS_B: 2/3  -> ACCEPTED
  CONTROLS_B: 3/3  -> ACCEPTED
```

Three independent blindnesses, any one of which would have convicted it:

1. the regex requires a *shape*, not `n == m` — `0/3` opens the gate;
2. `controls-b.exit` contained `1` and its **value is never read** (only its size);
3. the receipt's own `rev=077d431e6996` is **never compared** to the deciding `REV=c2108100`, although
   the gate has both strings in hand.

That is why a red control (`CTL_MISMATCH`, `2/3`, exit 1) opened the deciding run
(`DECIDING_RUN_EXIT=0`), and then four records (`SCORECARD.md:2583`, `corpus/QUALITY.md:1590`,
`corpus/lessons/round-54.md:74,101`, report `:162`) asserted the opposite of the receipt. The prose
failure is routed as R54.1 and is being corrected on the record side; the *instrument* failure is
this gate, and it is untouched.

One further laundering step deserves naming: commit `5564954` **re-stated** both receipts at the
freeze with the hand-written trailer `# receipt re-stated at the round-54 freeze 077d431e (bytes
unchanged; the verdict line above stands)`. The trailer's inference is exactly backwards — the
harness's bytes being unchanged says nothing about the verdict, because the verdict is a function of
the tree at `REV`, not of the harness. The stated reason ("the gate requires their last commit to
descend from it") shows the pressure: the gate rewards touching the receipts after the freeze, which
is how a failing control receipt ends up looking durable.

## 4. Round 55's `controls.sh` checked against the minimal shape

Frozen at `.ufo/evidence/round-55/controls.sh` (sha in `freeze.json`; unchanged through
amendments 1-8). Its header claims the R54.1 repair: *"is RE-SCORED at that same revision (round 54's
phase-B control cloned the freeze commit, which predates the work it was meant to certify - routed
as R54.1)"*.

**Q1 — does it re-score at the revision it certifies? Mechanically yes; as a guarantee no.**

Yes, in the sense that matters for the measurement: phase B clones `$REV` (`:121`) and every counter
is invoked with `--rev "$(git -C clone rev-parse HEAD)"` through `score()`, and both `CTL_POS` lines
echo the scored revision. Run at the current tip (`r55-phaseB-at-HEAD.stdout`):

```
CTL CTL_POS_c1 C1_R55: rev=133b2ce6d4d8 … stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
CTL CTL_POS_c2 C2_R55: rev=133b2ce6d4d8 … grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```

Both positive controls fire at the revision the round will certify, and the receipt names it.

No, in the sense the round-54 error requires: **round 54's phase B already cloned `$REV`**. The
clone line is the same in both files (`clone_at "$LANE" "$REV" pos`), so the round-55 header
describes a repair the code does not (and never needed to) make. Nothing in the round-55 harness
refuses a caller who hands it the freeze. Demonstrated with the exact round-54 mistake
(`r55-phaseB-freeze-as-rev.stdout`, `FREEZE=REV=631cd645`):

```
CTL CTL_POS_c1 C1_R55: rev=631cd6455e58 … total=10 C1_R55_PASS=false
CTL_MISMATCH CTL_POS_c1 expected=true actual=false
CTL CTL_POS_c2 C2_R55: rev=631cd6455e58 … total=20 C2_R55_PASS=false
CTL_MISMATCH CTL_POS_c2 expected=true actual=false
```

It **scored the freeze and carried on** — no refusal, no `REV != FREEZE` check, no
`merge-base --is-ancestor FREEZE REV`, no `rev-list --count FREEZE..REV`. The mismatch is the only
signal, and Section 3 shows the gate does not read signals.

**Q2 — does it refuse a control that could not fire? No, in three distinct ways.**

*(a) No subject guard.* The guard below is the whole missing check, and it behaves correctly on the
three cases that matter: `REFUSE` at the freeze (`count=0`), `REFUSE` for a non-descendant,
`ADMIT` at `c2108100` (`count=3`). It does not exist in either round's harness.

*(b) No receipt binding, and the gate is unchanged.* The whole control-gate block of round-55
`deciding-run.sh` (`from ^CONTROLS= to controls-b-verdict-missing`) is **byte-for-byte identical**
to round 54's (`gate-identical-r54-vs-r55.stdout`, produced by `diff` on the two `sed` ranges). So
round 55 inherits the `0/3`-passes hole, the never-read-`.exit` hole, and the never-compared-`rev=`
hole, with no change at all. The phase-B clone expression is likewise the same in both files
(`phaseb-clone-line-identical.stdout`: `controls.sh:142` vs `controls.sh:121`,
`d=$(clone_at "$LANE" "$REV" pos) || exit 2`) — the round-55 header comment describes a repair the
code never needed.

*(c) A mutation control whose anchor is dead — and it aborts the phase.* `CTL_BREAK_c2` (`:127-140`)
mutates `tools/repeat-control.py` at the literal
`emit_err(f"repeat-control: could-not-evaluate: {exc}")` and asserts `count == 1`. The landed fix
(the round's own C0, `9cf0146`, and the tip) writes `{message}`, not `{exc}`
(`ctl-break-anchor.stdout`):

```
literal {exc}    count=0
literal {message} count=1
regex name-invariant count=1  ['emit_err(f"repeat-control: could-not-evaluate: {message}")']
```

So the anchor is dead at the base, at the round-55 freeze, and at the tip. Consequence, observed
twice (`r55-phaseB-at-HEAD.stdout`, `r55-phaseB-freeze-as-rev.stdout`): the python assert raises, the
following `gitcommit` finds nothing to commit, `|| exit 2` fires, and **phase B exits 2 without ever
printing `CONTROLS_B`**:

```
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
AssertionError: anchor not unique: 0
HEAD detached at 133b2ce
nothing to commit, working tree clean
exit=2
```

That is fail-*closed* (the gate then refuses with `controls-b-verdict-missing`), but it means
**round 55's phase B cannot produce the receipt its own gate requires at any revision** unless the
frozen `controls.sh` is amended.

The §5 patch's tooth 4 repairs exactly this, and it is verified: replacing the literal anchor with the
name-invariant regex at `133b2ce` in a fixture clone lets the mutation apply, and the counter then
reads the break it is supposed to detect (`ctl-break-fires-with-invariant-anchor.stdout`):

```
C2_R55: rev=7fc3ea834e33 grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

— `8/9`: the break costs exactly the one mode it targets, so `check CTL_BREAK_c2 false` passes and the
receipt can be produced. Since `controls.sh` is in `frozen_paths` and pinned by `freeze.json`,
this is a blocking fact for the L1, not a seat fix.

*(d) A derived value that is empty at every revision.* `CTL_SKIP_c1` builds a values-only corrections
block from `ADD` and `REN`, where
`REN=$(git -C "$LANE" log --format=%H --diff-filter=R "$REV" -- .ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json | head -1 | cut -c1-7)`.
Rename pairing needs **both** sides in the pathspec, so the single-path form yields nothing
(`ctl-skip-ren-derivation.stdout`):

```
at 0a2010a   REN=''       ADD=ff2a821
at 631cd64   REN=''       ADD=ff2a821
at 133b2ce   REN=''       ADD=ff2a821
# with the rename SOURCE path also in the pathspec: 7fa9a5e
```

The control's own comment says it pastes "a corrections block carrying **every** corrected value";
for R54.7 it pastes an empty one. The control still reads `false` (stale hits remain), so it does not
invert, but it is weaker than advertised and it never exercises the "correct value, no fix" case for
that class.

## 5. The minimal correct shape of a phase-B control

Four teeth. Each is cheap, each convicts round-54's actual receipt, and none is present in round 55.

1. **Refuse a subject that cannot carry the claim** (harness, before anything is scored):
   `REV` resolves; `merge-base --is-ancestor FREEZE REV`; `rev-list --count FREEZE..REV > 0`.
   Exit 3, print nothing, write no verdict. (*Tested; behaves as intended.*)
2. **Bind the receipt to the certified revision** (gate): every `CTL` line already carries
   `rev=<12 hex>`; require it to be a prefix of `REV`. Round-54's receipt says `rev=077d431e6996`
   against `REV=c2108100` — one grep convicts it.
3. **Read the verdict instead of matching its shape** (gate): require
   `^CONTROLS_B: ([0-9]+)/\1 as pre-registered$` (n == m) **and** `controls-b.exit` content `0`.
   Round-54's own receipt fails both (`2/3`, `1`).
4. **A mutation control must prove it fired, and must refuse by name**: assert exactly one anchor,
   anchor on an identifier-invariant form (`\{[a-z_]+\}` rather than `{exc}`), and on failure print
   `CTL_BREAK_c2 CANNOT-FIRE anchor-absent` and exit 3 — never abort the phase with a traceback that
   leaves no verdict line.
5. *(Hygiene)* The harness should write its receipt (stdout + exit code + the argv it was given) into
   `OUTDIR`, which both rounds parse and ignore. That is the only way the invocation itself becomes
   auditable — and "no one re-stated a receipt afterwards" becomes checkable.

### Patch (proposed; `controls.sh` and `deciding-run.sh` are frozen this round — report only)

```diff
--- .ufo/evidence/round-55/controls.sh
+++ .ufo/evidence/round-55/controls.sh
@@ if [ "$PHASE" = b ]; then
+  # A phase-B control asserts something about the tree at REV. Refuse a REV that
+  # cannot carry the work (REV == FREEZE, a non-descendant, or zero commits beyond
+  # the freeze): such a control could not fire, and its receipt must not exist.
+  git merge-base --is-ancestor "$FREEZE" "$REV" 2>/dev/null \
+    || { echo "CONTROLS_REFUSED rev-not-beyond-freeze REV=$REV FREEZE=$FREEZE"; exit 3; }
+  [ "$(git rev-list --count "$FREEZE..$REV")" -gt 0 ] \
+    || { echo "CONTROLS_REFUSED rev-carries-no-work REV=$REV FREEZE=$FREEZE"; exit 3; }
   # CTL_POS -- the real repair AT THE REVISION IT CERTIFIES must pass both counters.
   d=$(clone_at "$LANE" "$REV" pos) || exit 2
@@ CTL_BREAK_c2
-  old = 'emit_err(f"repeat-control: could-not-evaluate: {exc}")'
-  assert src.count(old) == 1, "anchor not unique: %d" % src.count(old)
-  path.write_text(src.replace(old, 'emit_err(f"repeat-control: setup: RuntimeError: {exc}")'))
+  old = re.compile(r'emit_err\(f"repeat-control: could-not-evaluate: \{([a-z_]+)\}"\)')
+  hits = old.findall(src)
+  assert len(hits) == 1, "CANNOT-FIRE anchor-absent or ambiguous: %d" % len(hits)
+  path.write_text(old.sub(lambda m: 'emit_err(f"repeat-control: setup: RuntimeError: {%s}")'
+                          % m.group(1), src))
```

```diff
--- .ufo/evidence/round-55/deciding-run.sh
+++ .ufo/evidence/round-55/deciding-run.sh
@@ control gate  (replaces the two `grep -q '^CONTROLS_[AB]: [0-9]*/[0-9]* ...'` lines)
+# n == m with m > 0, the exit receipt says 0, and every CTL_POS line names the revision being decided.
+for p in a b; do
+  s="$LANE/$E/control/controls-$p.stdout"; x="$LANE/$E/control/controls-$p.exit"
+  awk -v U="CONTROLS_${p^^}:" '$1==U {split($2,v,"/"); if (v[1]!=v[2] || v[1]+0==0) bad=1}
+                                END {exit bad}' "$s" \
+    || { echo "DECIDING_REFUSED controls-$p-not-all-passed"; exit 3; }
+  [ "$(head -1 "$x")" = 0 ] \
+    || { echo "DECIDING_REFUSED controls-$p-exit-nonzero"; exit 3; }
+  awk -v want="rev=${REV:0:12}" '/^CTL / && /CTL_POS/ && index($0, want)==0 {bad=1} END {exit bad}' "$s" \
+    || { echo "DECIDING_REFUSED controls-$p-scored-a-different-revision"; exit 3; }
+done
```

## 6. Answers to the two questions, stated plainly

| Question | Round 54 | Round 55 (as frozen at `133b2ce`) |
|---|---|---|
| Does phase B score the revision it certifies? | Not in fact (it scored `077d431e`, the freeze, because `c2108100` did not yet exist). The harness was capable: same bytes give `3/3` at `c2108100`. | Yes mechanically — clones `$REV`, counters echo it (`rev=133b2ce6d4d8`, both `true`). But nothing refuses a wrong `REV`, and round 54 already had this same line. |
| Does it refuse a control that could not fire? | No. It *reported* the mismatch (`CTL_MISMATCH`, `2/3`, exit 1) and the gate ignored it; the records then asserted the opposite. | No. No subject guard; the gate still accepts `0/3` and still never reads `.exit` or `rev=`; and `CTL_BREAK_c2`'s anchor is dead at every revision, so phase B aborts with exit 2 and no `CONTROLS_B` line at all. |

**The one-line reconstruction:** phase B is parameterised correctly and was handed the freeze because
the revision it was meant to certify did not exist yet; the harness recorded that fact in its own
receipt (`rev=077d431e6996`), and the deciding gate — which checks presence, size and ancestry, but
never `n == m`, never the exit value, never the scored revision — opened anyway.

**Residual risk for this round (stated, not fixed):** round 55's phase B will certify what it is
handed. If the L1 hands it the current freeze (`133b2ce`) instead of a content revision that carries
the work, the harness will score the freeze, find both controls true (they already are at `133b2ce`,
see `r55-phaseB-at-HEAD.stdout`), and the gate will accept the receipt — a *clean* repeat of R54.1
with no mismatch line to give it away. The `rev=`-prefix check in §5 tooth 2 is the only thing that
catches that case, and it is not in the frozen gate.

## 7. Frozen-file defects found (reported, not fixed)

| # | File | Defect | Evidence | Severity |
|---|---|---|---|---|
| F1 | `round-55/controls.sh:134` | `CTL_BREAK_c2` anchor `{exc}` never exists (tree has `{message}`) → assert fires → phase B exits 2 with no `CONTROLS_B` verdict. | `ctl-break-anchor.stdout`; `r55-phaseB-at-HEAD.stdout` | **blocking** — phase B cannot produce the receipt the gate requires |
| F2 | `round-55/controls.sh:58-59` | `CTL_SKIP_c1`'s `REN` derivation returns empty at every revision (single-path `--diff-filter=R` cannot pair a rename). | `ctl-skip-ren-derivation.stdout` | medium — the "every corrected value" claim is false for R54.7 |
| F3 | `round-55/deciding-run.sh:55` (and round-54 `:58`) | Gate accepts any `n/m`, including `0/3`; never reads `controls-*.exit`; never compares the receipts' `rev=` to `REV`. | `gate-reproduction.stdout` | **high** — this is the hole R54.1 came through |
| F4 | both `controls.sh` | `OUTDIR` (arg 5) is parsed and never used; no invocation receipt is ever written, so a caller cannot be audited. | `grep -c '$OUT'` → 0 in both | medium — invites the "re-stated" receipt |
| F5 | round-55 `deciding-run.sh:50-52` | Requires each receipt's *last touching commit* to descend from FREEZE, which rewards re-committing a stale receipt after the freeze (exactly commit `5564954`). | `git log` of the receipts; `5564954` message | medium — incentive to launder |

Frozen-boundary statement: `.ufo/evidence/round-55/{contract.json,freeze.json,c1/measure.py,c2/measure.py,no-harm.sh,deciding-run.sh,controls.sh}` and the round-54 counterparts are untouched by this seat. F1-F5 are the report; the patch in §5 is the proposal. I believe F1 is a genuine blocking defect in a frozen file and say so rather than repairing it.

Note on the round-55 contract text: `claims.C2.target` now reads *"9/9 allocating modes (… and
`registry-check --rev`)"* and the counter reads `grammar=9/9` — consistent at `133b2ce`. Earlier in
this session the same file read `8/8` at `631cd645`; that is the round's own amendment 8, not a defect.

## 8. Confidence

| Claim | Confidence | Basis |
|---|---|---|
| Phase B was handed the freeze; the harness never hardcoded it | **high** | clone line identical at four revisions; receipt's own `rev=077d431e6996`; replay at `c2108100` gives `3/3` |
| Why: the certified revision did not exist yet | **high** | `7fa9a5e^ == 077d431e`; receipt first committed `12:21:35`; `c2108100` at `12:22:15`; freeze-scored replay reproduces the receipt byte-for-byte |
| Author intent = score at REV with FREEZE bytes | **high** | header, signature, in-body comments, pre-registered verdicts all agree |
| The gate, not the harness, let the failure through | **high** | gate executed verbatim: `exit=1`, `2/3`, `1 CTL_MISMATCH` → opens; regex accepts `0/3` |
| Round 55 re-scores at `REV` | **high** | observed: `rev=133b2ce6d4d8`, both `true` |
| Round 55 does not refuse a control that could not fire | **high** | guard absent by inspection; freeze-as-`REV` run scored and continued; anchor dead at 3 revisions; gate regex unchanged |
| Phase B as frozen cannot emit `CONTROLS_B` | **high** | observed twice, exit 2, traceback, no verdict line |
| That the round will actually be handed a wrong `REV` | unknown / L1's call | flagged in §6 |

## 9. Sweeps run that found nothing (so the nulls are visible)

* `git log --format=%H --diff-filter=R <REV> -- <single new path>` at base, freeze and tip: empty at
  all three (this is F2, not a null).
* `grep -n 'REV.*FREEZE\|FREEZE.*REV'` over round-55 `controls.sh`: only the usage comment and the
  positional binding; no guard.
* `grep -n 'rev='` over both `deciding-run.sh`: only `frozen.stdout`; the receipts' `rev=` is never
  compared.
* `grep -n 'cat.*\.exit\|read.*exit'` over both `deciding-run.sh`: matches only `coldread-precheck.exit`
  and `census.exit`; the control `.exit` files are never read.
* Reproducibility of the control-cited revisions: `7df0e0426c98` (round-54 `CTL_EXIT0`) and
  `042655edec78` / `de700f6ccc7c` (round-54 `CTL_FAB` / `CTL_LOGINPUT`) exist in **no** ref
  (`git cat-file -t` → not a valid object; 0 refs contain them). That is expected — the negative
  controls commit inside throwaway `git clone --shared` scratch — but it means those receipts pin
  revisions nobody can inspect; only re-running the harness reproduces them. Not a defect; recorded so
  no one mistakes it for one.

## 10. Deliverables

* Report: `.ufo/waves/round-55/w1/T55W1Revenger.md` (this file)
* Machine-readable findings: `.ufo/waves/round-55/w1/T55W1Revenger.json`
* Receipts (11 files): `.ufo/waves/round-55/w1/T55W1Revenger-receipts/`
  * `r54-phaseB-at-certified-rev.stdout` — round-54 phase B at `c2108100` → `CONTROLS_B: 3/3`, exit 0
  * `r55-phaseB-at-HEAD.stdout` — round-55 phase B at `133b2ce` → both `CTL_POS` true at `rev=133b2ce6d4d8`, then exit 2
  * `r55-phaseB-freeze-as-rev.stdout` — round-55 phase B handed the freeze → two `CTL_MISMATCH`, exit 2
  * `gate-reproduction.stdout` — the gate's own lines against the committed round-54 bytes
  * `freeze-scored-counters.stdout` — frozen counters at `077d431e` reproduce the receipt byte-for-byte
  * `ctl-skip-ren-derivation.stdout` — `REN` empty at every revision
  * `ctl-break-anchor.stdout` — `{exc}` count 0, `{message}` count 1, regex count 1
  * `gate-identical-r54-vs-r55.stdout` — the control-gate block is byte-for-byte unchanged in round 55
  * `phaseb-clone-line-identical.stdout` — the phase-B clone expression is the same line in both harnesses
  * `ctl-break-fires-with-invariant-anchor.stdout` — with the §5 anchor the break control fires (`grammar=8/9`, PASS false); with the frozen `{exc}` it aborts
  * `gate-teeth-exercised.stdout` — the proposed gate teeth refuse `2/3`, `0/3` and a receipt scored at another revision; admit only `3/3` at REV
* Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → **exit 0**
  (140 `| S### |` rows at the time of reading; the seat spec's 139 was the pre-S280 state).
* Tooling: no installs or upgrades; nothing written to any PATH directory.
* Lane writes: **only** the three paths above (report, json, receipts dir). No production file edited.
