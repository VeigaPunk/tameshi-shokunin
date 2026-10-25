# RevAmendments — narration audit of contract amendments (round 43, w2)

Scope: `.ufo/evidence/round-43/contract.json` `amendments` array. Per amendment:
is `when` true (does the credited evidence file exist earlier than the deciding
run), is `rule_changed:false` consistent with its own commit's diff, and does it
change a target, predicate, or fixture's declared class.

**Audit snapshot.** The contract is a moving target: the array held 10 entries
at the ticket's freeze of record `3aee2c0` and **14** at my audit HEAD
`6b83a11` (A11-A14 landed *while wave-2 seats were running*; commits
08:05:44–08:10:15, 4 in ~5 min). Every check below names the commit it ran
against. The `.ufo/evidence/round-43/after/` directory contains only a
README as of `6b83a11` — **no deciding run has happened**, so every `when`
claim of the form "before the first deciding run" is currently satisfiable.

## Findings, by severity

### F1 (HIGH) — `amendments_note` is false at every freeze since A7, and now also for the predicate/target fields it specifically names

`contract.json` `amendments_note` (line 189 at `6b83a11`; identical text since
`53cb32b`/A8) says: *"No amendment changes claims.* (other than counter_sha256
and the class sentences restated verbatim), the predicate, the target, the
fixture set or the controls."*

Demonstrably false on three independent axes, all reproducible:

- **Class sentences were rewritten, not "restated verbatim."** The m7/m8/m10
  sentences were edited in `f0f2636` (A1) and m8/m10/m11/m12/m13 again in
  `114ffac` (A6); `claims.C2.classes` sha changes `7fd452e5 → 1b07c384 →
  ed4a0ffb` across the chain. `claims.C3.statement` was edited in `114ffac`
  and `3aee2c0` — a `claims.*` field that is neither a counter pin nor a
  class sentence, so it isn't even inside the note's own exception list.
- **The predicate and the target did change.** `claims.C1.target` at A11
  (`b510ad1`): `kill_fixture_reachable=1` → `kill_binding=1` plus a new
  `mutants_sha_ok=1` field. `claims.C3.target` at A12 (`bb36f80`): gained
  `held_refused=1 naive_agree=1 substitute=0`. `claims.C1.mutants_sha256`
  was added at A11. A11's own `effect` admits "the predicate gains two
  fields" and A12's admits "predicates gain fields" — while both carry
  `rule_changed:false` and the note says no amendment changes the
  predicate/target.
- **The controls did change.** A2 (`17f6ef0`) changed what `--control` runs
  (11 → 10 fixtures) — A2's own `effect` honestly says "control only," so
  the fault is specifically in the note's blanket sentence.

### F2 (HIGH) — `frozen_before` has been stale at every freeze since A8 and the worktree's uncommitted fix is stale-on-arrival

`frozen_before` at `6b83a11` still reads *"the freeze of record is 114ffacd…"*
(commit `114ffac`, A6/A7). A8's own `what` was to correct this text; A9, A10,
A11, A12, A13, A14 all landed after it without updating it. Measured against
the pinned instruments, `114ffacd` pins `901d947f/52961c37/8c8147e7/365bf958`
while `6b83a11` pins `601c1840/ab76cbd3/47a6afce/03a796c5` — the declared
freeze predates the instrument set by seven freeze commits; running the
current counters at `114ffacd` prints `self_pin=0` for all three claims.
During this audit the worktree gained an uncommitted edit naming `6b83a11` —
self-referential, so it is again wrong the moment it commits under a new hash.

### F3 (HIGH) — A11 and A12 carry `rule_changed:false` while changing `claims.*.target` text

- **A11** (`b510ad1`): `claims.C1.target` loses `kill_fixture_reachable=1`,
  gains `kill_binding=1` and `mutants_sha_ok=1`; `claims.C1.mutants_sha256`
  added. `effect` admits "the predicate gains two fields that bind it."
- **A12** (`bb36f80`): `claims.C3.target` gains three required fields
  (`held_refused=1 naive_agree=1 substitute=0`). `effect` admits "predicates
  gain fields … no target narrowed."

`rule_changed` is undefined in the contract, but under the only reading
consistent with the note (declared rule/target text unchanged) both flags are
wrong. Under the narrow "K/D/E/U sentence" reading A11 is technically safe
(the `rule` object is byte-unchanged across the whole chain — verified) but
the predicate's declared target text is not the same instrument that was
frozen. If the flag is to mean anything, these two entries understate.

### F4 (HIGH) — The prerun receipts inside the freeze certify superseded instruments

`git show 3aee2c0:.ufo/evidence/round-43/prerun/c1-at-freeze.stdout` prints
`freeze=114ffacd self_pin=1`; `c3-at-freeze.stdout` prints `selftest_cases=23`
while A10's selftest and the pinned tool have 24 cases (`grep -c "    case("`
on `3aee2c0:tools/staged-id-guard.py` = 24). `self_pin=1` at `114ffacd` is
only possible with the A5-era C1 bytes (`901d947f`), not the pinned
`0d0f81bd` — so the only PASS receipts for C1/C3 inside the freeze of record
measure instruments the pins no longer name. The same receipts also carry
`live_collisions=6`/`expected_collisions=6`, but `corpus/SOURCES.md` was
edited by the records commit `c5335c7` and the A10 control re-run prints
`expected_collisions=7` — the frozen receipts' live numbers are already
stale. Neither A9, A10, A11, A12, A13 nor A14 discloses or re-mints them;
A10 re-ran only the C2 *base* receipt (and that landed post-freeze in
`e20cf89`).

### F5 (MEDIUM) — A1's `effect` is falsified by its own commit

A1 (`f0f2636`) says *"the seven classes and the predicate C2_R43_PASS
(self_pin=1, classes=7, total=0) are byte-unchanged."* The same commit edits
`claims.C2.classes.m7`, `.m8`, `.m10` — new masking, new cite scope, new
supersedes semantics. The predicate was byte-unchanged; the class sentences
were not, so "byte-unchanged" overstates. (`why` itself is verified:
scratch copies at `487b8f0` print exactly `m7=7 m8=38 m10=9` pre-A1 and
`m12=1 m13=1` post-A1.)

### F6 (MEDIUM) — A6, A10 and A13 each claim "class sentences unchanged in meaning" while changing either the sentences or the enforced rule

- **A6** (`114ffac`) edited the m8/m10/m11/m12/m13 sentence text *and*
  widened m11's check from `cat-file -e …^{commit}` (commit-only) to
  `cat-file -e …` (any object) — a meaning change by any reading. The
  claim "unchanged in meaning" overstates; at most it is "sentences were
  rewritten to describe the new behaviour," which is a different thing.
- **A10** (`3aee2c0`) added two m12 failure conditions the frozen sentence
  does not state: `round_no != contract.round` and a non-empty field. The
  class sentence at the freeze (`"the newest '## Round N' SCORECARD block
  carries the field '**Planned (round N+1):**'"`) is weaker — a `## Round 44`
  block with `**Planned (round 45):**` satisfies the sentence but fails the
  code. A10's `effect` understates this as "unchanged in meaning."
- **A13** (`f551ca6`) rewrote m10's skip rule to require per-claim coverage
  (a superseder must re-assert *the same target* with the tree-correct
  value) yet `claims.C2.classes.m10` is byte-identical (`e40259f2` before
  and after A13/A14). Its `effect` says the sentence "now matches a
  per-claim repaired rule" — it does not; the sentence under-specifies the
  code, repeating the A6/A10 pattern.

### F7 (MEDIUM) — A10 moved the declared before-state observable without saying so

`claims.C2.before_state` says `m12=1`. With the pinned post-A10 counter the
base run prints `m12=2` (`**Planned_(round_43):**` missing *and* the
block-round mismatch — reproduced live: `python3
.ufo/evidence/round-43/calibration/measure.py --lane LANE --rev 487b8f0…
--freeze 6b83a11` → `m12=2 … total=3`). The -A10 receipt
(`before/c2-at-base-A10.stdout`) records the same. A10's `effect` mentions
the re-run but not that it changed the observable `claims.C2.before_state`
declares — a claims-level observable invalidated by an amendment whose own
flag is `rule_changed:false`.

### F8 (MEDIUM) — A5's `why` misattributes a pre-declared defect to A4; the frozen text was never corrected

A5 says `tool_sha_ok=0` happened "because A4 had moved the single top-level
tool_sha256 to the guard tool." False: at the first freeze `697d2f1`
`tool_sha256` was *already* the guard sha (`8140945a…`; guard blob at that
commit = `8140945a`, census pin = `784de4c`). A4 only rotated it to
`efa5f129`. `tool_sha_ok` was 0 at `17f6ef0` before A4 existed. The
committed `w1/RevProvenance.md` §5 (line 73 at `3aee2c0`) states the same
correction explicitly, so the contract's `why` text contradicts the frozen
seat evidence it cites — and was never amended. Understates the defect's
provenance (pre-declared, not amendment-introduced).

### F9 (MEDIUM) — A10 and A11 both say "during wave 1" but were committed after the wave-1 records commit

`c5335c7` (records: all wave-1 seat reports, SCORECARD, LOG) is 08:00:58;
`3aee2c0` (A10) is 08:02:31; `b510ad1` (A11) is 08:05:44. A10's and A11's
`when` fields read "during wave 1." The seat evidence they cite (CritC3Maps,
CritC2Gaming, RevC1Counter) was produced during wave 1, but the amendments
themselves — and A10's C2-counter change, and A11's edits to a C2-recorded
record (`corpus/lessons/round-43.md`, undisclosed in `what`) — landed after
the wave was closed. Overstates the temporal claim by omission; see also F10.

### F10 (LOW) — A4's `effect` understates the blast radius of the pin it moves

A4 rotates `tool_sha256` to `efa5f129` for "capability repair under the
frozen predicate" of C3. But that top-level key was the exact key the
(pre-A5) C1 counter compared the census tool against — so A4's pin move is
also a C1-visible change, unmentioned in its `effect`. It "worked" only in
the sense that the C1 comparison was already broken (F8). Minor, but it is
the actual reason A5's narration got its causality wrong.

### F11 (LOW) — A12's own freeze was pin/blob inconsistent for ~2 minutes; the entry doesn't say so

At `bb36f80` (A12), `claims.C1.counter_sha256=b56a34d` while the C1 blob was
`3d1ff3d` — `self_pin=0` at the freeze itself (verified by pin/blob sweep
over all 15 commits: `bb36f80` is the only MISMATCH). A13's `why` discloses
it correctly; A12's `what`/`effect` don't. The deciding run is protected only
because A13 fixed it before that run existed.

### F12 (LOW) — Wave-2 amendments cite uncommitted evidence files

A12-A14 credit `w2/MutC3Held.md`, `w2/RevC3Tool2.md`, `w2/RevC1Predicate.md`,
`w2/MutC2m10Superseder.md` — all present in the worktree but **untracked**
(`git status --porcelain .ufo/waves/round-43/w2/` shows the whole directory
`??`). `git cat-file -e` fails for every one at the freeze commits. The
`when` clause ("exist earlier than the deciding run") currently holds via the
worktree alone; if wave-2 reports are ever reaped differently than committed,
the cited evidence evaporates from the record.

## Verified — no finding

- **`when` for A1-A3 is true.** `.ufo/waves/round-43/` contains zero files at
  `697d2f1`, `f0f2636`, `17f6ef0` (`git ls-tree -r` empty) — no seat had run.
  A4-A14 cite committed wave-1 reports at `c5335c7`, all present
  (`git cat-file -e` OK for all eleven).
- **`why` for A1-A4 reproduced exactly** on scratch counter copies at
  `--rev 487b8f0` (permitted rev): `m7=7 m8=38 m10=9` (pre-A1) →
  `m12=1 m13=1` (post-A1); control `11/11 killed=5` (pre-A2) →
  `10/10 killed=4` (post-A2); `--tool-file` FileNotFoundError (pre-A3);
  two-entry map refused `['map has a target that is not an S-id']` (pre-A4).
- **No target string changed at A1-A10.** SHA-256 over the three `target`
  strings is identical across `697d2f1..3aee2c0`. (A11/A12 then changed them — F3.)
- **No fixture's declared class changed anywhere in the chain.** The
  `FIXTURES` dict (12 fixtures, `want` maps) is byte-identical between
  `697d2f1` and `6b83a11` (diff empty, 179 lines each).
- **The K/D/E/U rule object is byte-unchanged** across all commits (sha
  `6d08d081` throughout) — so A5's "repaired to the frozen sentence" is true
  (the reachability clause was pre-declared at `697d2f1`), and A9's live-failure
  gate and `--probe-mutant` `dead_code_only` verdict are alignment, not a
  sentence change.
- **Pin/blob agreement holds at every commit except `bb36f80`** (F11).
  At `6b83a11` all four pins match their blobs; `mutants_sha256` =
  `b3abab06` = sha256 of `487b8f0:.ufo/evidence/round-42/census/mutants.json`.
- **A8's `effect` is accurate** for its own commit: `53cb32b` touches only
  `frozen_before`, `amendments_note`, and the A8 entry. (The note it wrote
  is what later became false — F1.)

## Residual risk

1. The deciding run must run against `6b83a11` (or later): at `3aee2c0`'s
   own declared `frozen_before` the instrument set disagrees with the pins.
   If any receipt or dispatch hard-codes `114ffacd` as the freeze of record,
   every counter will print `self_pin=0`.
2. `amendments_note` and `frozen_before` have been wrong at five consecutive
   freezes (A8-A13) and patched after the fact — the narration is always one
   freeze behind the instrument. Any wave-2 seat quoting the note inherits
   the staleness.
3. m10/m12 code-vs-sentence divergence (F6) means C2's declared class text
   under-describes what the predicate enforces: a deciding run can print
   `m12`/`m10` hits that the frozen sentences cannot explain. Calibration
   depends on the sentence being the audit contract for the class.
4. A11/A13/A14 changed C2-recorded records (`corpus/lessons/round-43.md`)
   inside freeze commits; if the deciding run scans those records at
   measurement rev, the record set differs from what wave-1 seat reports
   measured.
5. Uncommitted worktree edits were still landing during this audit; A15+
   may already exist by the time this report is read. Re-run the pin/blob
   sweep and the `amendments`-length check before the deciding run.

## Verification commands

```bash
# per-amendment contract diffs
git diff <A-commit>^ <A-commit> -- .ufo/evidence/round-43/contract.json
# pin/blob sweep (the F11 mismatch pops out at bb36f80)
for c in 697d2f1 f0f2636 17f6ef0 5cd2154 114ffac 53cb32b 273c047 c5335c7 \
         3aee2c0 e20cf89 b510ad1 bb36f80 f551ca6 6b83a11; do …; done
# A1 numbers (scratch copy, permitted --rev 487b8f0)
python3 /tmp/m-697.py --lane LANE --rev 487b8f0… --freeze 697d2f1   # m7=7 m8=38 m10=9
python3 /tmp/m-A1.py  --lane LANE --rev 487b8f0… --freeze f0f2636   # m12=1 m13=1
# A2 control
python3 /tmp/c1-697.py --lane LANE --rev 487b8f0… --freeze 697d2f1 --control  # 11/11 k=5
# current C2 at base vs before_state
python3 .ufo/evidence/round-43/calibration/measure.py --lane LANE \
  --rev 487b8f0… --freeze 6b83a11    # prints m12=2, not the declared m12=1
```

Tools installed: none (used in-repo python3 + git only; pacman untouched per
host pause). Scratch copies under `/tmp/tameshi-r43-w2-RevAmendments/`
(deletable).
