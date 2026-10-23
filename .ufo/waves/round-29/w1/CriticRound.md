# Round 29 — round-shape critique

## Review verdict

**C1 still has exactly the rejection condition that defeated rounds 27–28.** The input freeze addresses a demonstrated cause, and three readers improve delivery redundancy, but neither guarantees 64/64. In particular, two passing reads cannot outvote one current blocking finding. The binding check improves evidence association, not content correctness.

**C2 names a different operation and frontier, provided the delivered work is the amended, source-supported reduction operation, not merely the already-known B5 witness.** The original C2 counter did accept cheap controls. The amended counter rejected every control reported in its port, but those receipts do not establish rejection of every possible shortcut or an isolated source-marker shortcut on an otherwise valid anchored fixture.

**None of round-28 routed items 1–4 is wholly without a route.** However, routing is not completion: item 2 has a source-recheck owner but no guaranteed disposition if stable drift requires a SOURCES correction; item 4's runner defect has a diagnosis/proposed-diff owner, explicitly not an implementation owner. Both interact with the frozen no-more-input-edits policy. Do not describe all four as repaired.

This is an advisory review finding, not a round judgment or admission decision.

Axes: **calibration** and **coverage**. Secondary exposure: freshness of source anchors and operability of the runner/closure. No new score or saturation claim is made.

## Evidence boundary

Paths below are lane-relative unless marked `fleet`. Content A is `9f3084bc60ad56aac01e4556ef4c7653df2f65e5`; the reviewed amended counter package is `09e4f273dd54edea382ea03f098eecb3628331c3`. The wave work orders are `.ufo/waves/round-29/make-spec-w1.py`. Control receipts are attributed to their writers, not represented as my reruns.

My isolated clone setup, both commands exiting 0 with no output:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 timeout 90 git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r29-CriticRound
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 timeout 90 git -C /tmp/tameshi-r29-CriticRound checkout --quiet --detach 09e4f273dd54edea382ea03f098eecb3628331c3
```

From that clone, this command exited 0:

```sh
timeout 30 sha256sum .ufo/evidence/round-29/c1-measure-v2.py .ufo/evidence/round-29/c2-measure-v2.py .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html
```

Observed:

```text
2ec2f1a02f73ba10136288abc06197cd73cb388c013db80af3a926959ed70491  .ufo/evidence/round-29/c1-measure-v2.py
adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c  .ufo/evidence/round-29/c2-measure-v2.py
3abede35b99770d2bf3d348a3481b28b9bd826395f1e0374ebf9d7e8f0a65e99  .ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html
```

These match `contract-amendment-2.json:14`, `contract-amendment-1.json:14`, and the frozen snapshot identity in the C2 amendment/counter.

## 1. C1: the same missed target, with useful but limited mitigations

### The unchanged failure condition

- `corpus/lessons/round-27-verifier-spotcheck.md:49-64`: round 27 ended at 60/64, restraint 6 and mismatch 1; its target was 64/64, restraint 8 and mismatch 0.
- `corpus/lessons/round-28-verifier-spotcheck.md:35-47`: round 28 reached 62/64 and then 63/64, still restraint 6/mismatch 1; neither head met the target.
- `contract-amendment-2.json:20-23`: C1 still requires complete strict coverage, restraint 8 and mismatch 0 at the landed head. A false predicate is an honest stop, not a smaller successful claim.
- `.ufo/waves/round-29/ctl/C1v2-rescore.txt:2-12`: the recorded baseline is 63/64 at `367ec0f1`, but 52/64 at A and at the first C2-amendment commit, with restraint 6/mismatch 1 throughout.

Recovering 52 to 63 would mostly recover this round's own invalidated evidence; it would not close the inherited last-section defect. C2 cannot compensate for a C1 miss.

### What genuinely changes the odds

| Planned change | Evidence | What it fixes; what it does not |
|---|---|---|
| All widely read edits precede A's cold reads | `contract.json:39`; `corpus/QUALITY.md:628-636`; work orders `:43-46` | Prevents repeating the known late-SOURCES/README/QUALITY invalidation mechanism, **if observed through final delivery**. Does not repair false instructions or stale external surfaces. |
| Three readers for each missing section | Work orders `:2-8,101-109` | The stated motivation is round 28 losing 12 of 38 seats to a provider limit. Adds redundant opportunities for a completed, correctly formed read; also adds opportunities to discover a real defect. No measured independence or numerical success probability follows from the count. |
| Pinned monitor plus stronger report binding | `c1-measure-v2.py:79-103,110-157`; amendment 2 `:7,20,24` | Fixes the v1 executable-identity problem and binds report revision/verdict as well as labels. Does not make an incorrect section correct or prove that roster/report labels establish independent reading. |
| Honest retention of failures | Work orders `:84-85`; monitor `.ufo/evidence/round-18/measure.py:635-638` | Preserves calibration. It is not a majority vote or a best-of-three success selection. |

My read-only delta inspection, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 timeout 30 git -C /tmp/tameshi-r29-CriticRound diff --stat 367ec0f1d79cb9b67d724f2962e7554a0841b1fc 09e4f273dd54edea382ea03f098eecb3628331c3 -- tools/mutate-and-run.sh corpus/SOURCES.md corpus/README.md corpus/QUALITY.md SHONEN.md SKILL.md
```

Observed:

```text
 corpus/QUALITY.md | 34 ++++++++++++++++++++++++++++++++++
 corpus/README.md  | 18 ++++++++++++++++++
 corpus/SOURCES.md |  2 +-
 3 files changed, 53 insertions(+), 1 deletion(-)
```

Thus the inspected pre-read package changes the three named inputs, not SKILL, SHONEN, or the runner. The reported 63→52 drop must remain visible alongside any subsequent recovery.

### Strongest tested counterexample: two successes plus one current failure

The frozen monitor explicitly sets `covered = credited > 0 and not vetoes` (`round-18/measure.py:627-638`). `entry_is_stale()` does not discard a failure merely because another reader passed (`:528-537`). I exercised that mechanism on an actually covered A section, using its existing valid input/trace data and appending a **synthetic** cohort of two success-shaped entries plus one `gap-blocking` entry. No fresh cold read or claimed execution was fabricated; this was an in-memory mechanism probe, not an appended committed ledger or a C1 measurement.

Command, cwd `/tmp/tameshi-r29-CriticRound`, exit 0, empty stderr:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 timeout 180 python3 /tmp/tameshi-r29-CriticRound/veto-probe.py
```

Observed:

```text
SYNTHETIC_COHORT: passing=2 failing=1; authentic existing input and trace bytes reused; no cold read represented
SECTION: start=1499 heading=### Gate/probe registry
BEFORE: credited=True vetoed=False
AFTER: credited=False vetoed=True reason=verdict:gap-blocking
COVERAGE: 52/64 -> 51/64
```

Reproduction logic: import the unchanged `round-18/measure.py`; load A's SKILL and round-21 ledger with `git show`; call `coldread(..., strict=True, explain=True)`; select the latest entry for a covered section whose `entry_reason(..., True)` is `None`; append three deep copies, changing only the third's verdict to `gap-blocking` and `blocking_gaps` to 1; call `coldread` again. The full probe is retained in the private clone at the command path.

**Impacted axis:** calibration. [INFERENCE] If any of the 12 fresh cohorts finds a real, non-stale blocking defect, extra passing readers cannot produce 64/64. With post-A edits limited to new files and specified appends, there is no promised same-round SKILL repair path. Repeating reads until one passes is not a safe correction.

The no-reader control also has a bounded lesson: `CtlC1Cheap.md:299-340` records K4 reaching monitor-only 53/64 without a reader, while whole-counter binding remained false. The v2 rescore retains `appended=12 bound=0`, PASS=false (`C1v2-rescore.txt:38-40`). This supports the binding check's usefulness, not a claim that its syntactic provenance bound disappeared. Amendment 2 `:24` explicitly records the uncompleted shortcut probe; it must not be reported as a passed control.

## 2. C2: different ground only as demonstrated reduction, not rediscovery

### Frontier and sourcing evidence

- `corpus/README.md:68-85` distinguishes open F6, fixture minimization, from the calibration monitor and F8 oracle anchoring. F6's next move is reduced fixture size plus a kill check; `:440-447` preregisters reduction, without claiming F6 held.
- Existing `corpus/knowledge/mutation-case-kagi-census.md:107-116` **already** contains the non-executable `asset exec -` B5 probe and the pristine-1/mutant-0 differential. A new filename for that witness alone is not new coverage.
- Bounded search across the frozen `corpus/knowledge/`, `SCORECARD.md` and `LOG.md`, pattern `\b(F6|ddmin)\b|delta[ -]debugging|fixture minimization|1-minimal`, found only `SCORECARD.md:1024` listing F6 as future work. This supports the claimed local novelty of the reduction operation, not a universal claim about every historical artifact or sibling.
- `corpus/SOURCES.md:35` identifies S024 as the Fuzzing Book reducer chapter, kind `book`, tier B, now mined with the proposed entry path. The pinned snapshot actually explains preserving the precise error at `:12075` and 1-minimality at `:13023`. I inspected the snapshot, not a live re-open; `ReopenS024` owns that re-open (`make-spec-w1.py:127-129`).
- Amendment 1 `:12-21` now requires an original pinned declaration, an actual B5 kill, the counter's own reduction, exact minimized units, a one-deletion check, source/count markers and a located quotation against the fixed snapshot. Work orders `:117-123` ask the builders to perform that operation.

That is causally different from C1. It is a bounded F6 coverage candidate; it does not establish general reducer coverage, global minimum size, or saturation. The reduced B5 kill is not itself novel.

### Cheap controls: v1 failed; v2's tested conjunction held

**Do not quote only `CtlC2Cheap`'s seven negative results.** The stronger design controls did reach the original predicate.

Recorded by `ctl/CriticC2Design.md:95-100,135-148`, using its frozen v1 counter at private HEAD `af694c1df7885487456c258f9a238d4dd377e9f3`:

```sh
timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /tmp/CriticC2Design-c2.py --repo /fast/scratch/hyaku/tameshi-r29-CriticC2Design --rev HEAD
```

Observed there, exit 0:

```text
C2_F6: fixture=present kill=1 units=2 one_minimal=1 entry_sourced=1 quote_located=1 rev=af694c1df7885487456c258f9a238d4dd377e9f3
PREDICATE: C2_F6_PASS=true
```

The control handwrote the known witness, claimed no reduction, supplied nonsense entry prose, and quoted only the source title. Other original-counter passes involved external absolute targets and a rewritten snapshot (`CriticC2Design.md:29-61`; amendment 1 `:7`). The amendment appropriately preserves these failures and redesigns before data, rather than calling the original controls adequate.

Under v2, `ctl/CtlC2v2Port.md:59-450` records do-nothing, malformed/seeded junk, empty fixtures, handwritten and external-target witnesses, escaping/link host manifests, a title-only quote, and a rewritten snapshot: all whole-predicate false. Its common command was:

```sh
timeout 900 python3 /tmp/CtlC2v2Port-c2v2.py --repo /fast/scratch/hyaku/tameshi-r29-CtlC2v2Port --rev HEAD
```

The most informative receipt is V7a (`:322-355`), exit 1:

```text
  oracle tests run: 3
C2_F6_V2: fixture=present anchored=0 kill_original=1 units_original=2 units_minimized=2 ddmin_match=1 kill=1 one_minimal=1 entry_sourced=1 quote_located=0 rev=1c3563d500c6407feae1da365a668d379205441a
PREDICATE: C2_F6_V2_PASS=false
```

This is a rejected conjunction, not proof that each component discriminates skipped work. The nonsense entry still satisfies `entry_sourced`; the handwritten witness is stopped by `anchored=0`, and the title by `quote_located=0`. The port reports no anchored control. It therefore does not isolate a nonsense/source-label entry on a valid anchored reduction with a qualifying authentic quotation. I did not observe a complete v2 bypass and do not claim one.

**Impacted axes:** coverage and calibration. The code intentionally checks source/count markers rather than entry prose (`c2-measure-v2.py:277-297`); amendment 1 `:21` leaves prose quality to review. A green fixture counter alone must not be described as independently establishing source-supported understanding. The counter's actual reduction is useful work even when the participant did not manually perform it. Preserve that distinction rather than treating automatic reduction as no reduction.

## 3. Exact routing of round-28 items 1–4

Source obligations: `corpus/lessons/round-28-verifier-spotcheck.md:87-92`.

| Item | Route visible in the plan | Remaining gap, not silently counted as fixed |
|---|---|---|
| 1. Missing Round-18 registry credit; restore restraint/mismatch; edit inputs before reads | C1 amendment 2 `:12,20-23`; three-reader construction `make-spec-w1.py:101-109`; input-order criterion 56 | Outcome still depends on every required section being covered at the final head. Three attempts are not three votes. |
| 2. S059 pinned digest drift | `ReopenS059`, work orders `:130-132`, including repeated fetches and a decision between nondeterministic HTML and stable content drift | This is an investigation route. S059 still carries the old markdown digest (`SOURCES.md:68`), and the inspected delta changes only S024 in that file. If a supersedes row is needed, editing SOURCES after A conflicts with criterion 56/contract `:39`; the work order does not provide an authorized implementation route. A nondeterminism note can instead satisfy the routed alternative if the evidence actually supports it. |
| 3. Close against one final head; no post-completion landing/report rewrite | Criterion 57, `QUALITY.md:638-645`; `ReviewR1Edits` and `ScribeMistakes`, work orders `:145-149` | Routed by an already-landed criterion, not by C1's Boolean. Only final delivery/closure can exercise the named-head invariant. |
| 4. Carry round-27 items 4, 5, 6: README wording, QUALITY amendments, runner leg sum | README correction `:431-438`; QUALITY 55 `:613-626`; `ReviewR1Edits` `:148-149`; `MutateLegSum` `:138-140` | README/QUALITY have landed routes. Runner work is explicitly a mutation diagnosis plus unified diff **in its report only, never applied**. `tools/mutate-and-run.sh:1430-1459` still tallies statuses without comparing their sum to `nlegs`; the pre-read delta contains no runner edit. This is not a completed operational fix. |

The extra `RegistryNoHarm` and `RerunCensusA` tasks (`make-spec-w1.py:133-137`) are useful no-harm/frontier checks, but neither substitutes for the S059 disposition or runner implementation.

Criterion 50 (`QUALITY.md:540-550`) calls for explicit item identities and counted checks or recorded dispositions, including deferral with an owner. The above map shows routes; it does not turn their investigative outputs into closure. The final round report needs that same identity-level accounting.

## Smallest safe correction

1. **Keep the frozen C1 target and every failing read.** Describe the third reader as delivery redundancy/falsification, never majority voting. If a current blocking finding prevents 64/64 under the frozen edit discipline, retain the honest stop and name the exact section; do not let C2 erase the repeated calibration miss or change the predicate after data.
2. **Use only the amended C2 predicate for current results, retaining the failed original controls.** Require the delivered anchored original, replayed reduction, committed minimized witness, and a meaningful source-supported entry. Report only the controls actually exercised. The existing v2 receipts support their full-conjunction failures, not the universal statement that every cheap control fails.
3. **Separate routed from resolved for all four items.** For S059, record the evidence-backed branch and disposition. For the runner, record the proposed correction and an explicit implementation owner/disposition; do not call a report-only diff a landed fix. Do not silently edit widely read inputs or the runner after A contrary to the frozen policy. Any unresolved conflict with “repair first” is a disclosed contract issue for the canonical judge, not something this critic can waive.
4. **Close once at the declared final head.** Exercise criterion 57 at that boundary and do not rewrite the report or continue landing afterward. This is a fixable delivery discipline, unlike an unresolved C1 miss or unsupported coverage claim, which cannot be traded away.

## Isolation and completion

Only this report was written in the lane. The clone and mechanism probe were confined to my own `/tmp`; no lane/fleet Git write, `jj` command, production edit, subagent dispatch, model call, integration, or judging runtime was used. All launched shell commands were bounded and returned; no service or process tree remains running. No tool was installed or updated. No complete C1/C2 after-state or final closure check was executed by me.

Report: `.ufo/waves/round-29/w1/CriticRound.md`
