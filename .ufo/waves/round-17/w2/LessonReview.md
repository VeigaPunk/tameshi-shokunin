# Lesson review — `corpus/lessons/round-17.md` @ `eb7838b`

Seat: `TameshiR17.LessonReview-2` (leaf; no delegation).
Target: `corpus/lessons/round-17.md` at `eb7838b16490ca7ba17ea3242ade76a61f744af2`
(`sha256 0047f2492b0e0d273ebb96ee85c7f88ff1fa5a606ad3c6a066df927a16ca0dc5`, 59 lines; 9 Gate rows
at `:18-26`, 8 Mistakes rows at `:52-59`).
Scope: every Gate and Mistakes row's evidence pointer must resolve and say what the row claims;
mistake classes must be distinct; any round-17 mistake in `.ufo/waves/round-17/w1/` missing from
the table is reported.
Method: one fleet-mirror clone at `/tmp/tameshi-r17w2-LessonReview-2-Q9MpSR/fleet/tameshi-shokunin`
(`git clone` + `git checkout --detach eb7838b…`, exit 0), siblings symlinked. All executions ran
from the clone; git writes were confined to that `/tmp` clone (one probe commit). No `jj`, no
lane write except this report, no installs or upgrades.

## Verdict summary

- **Gate: 7 of 9 rows hold as written. G5 is partly false** (executed counterexample: K02 hole 2
  still credits end-to-end in strict mode). **G7's pointer names the wrong K02 hole** (substance
  holds).
- **Mistakes: all 8 rows' pointers resolve and support the row.** `partial sweep`'s fix is
  incomplete against the criterion it cites (12 of S10's 19 statements unamended at this rev).
- **Two round-17 defects found in wave 1 are missing from the table** (stale SCORECARD capability
  counts; the `2a22ade` evidence-disposition selftest was red under its own scrub).
- The 8 classes are distinct mechanisms.
- The **C1 headline is not reproducible at this rev**: the wave-2 ledger is absent, so strict
  `measure.py --rev eb7838b` gives `box3_full_page: false`, `score 6`.

## Findings by severity

### F1 — HIGH — G5 claims "K02 holes 1–4 … closed"; hole 2 credits end-to-end

Lesson `:22` (G5, admit) states: "K02 holes 1–4 and R05 F1–F3 closed in `measure.py` (89/89
selftest)". Executed proof that hole 2 is open:

1. `measure.py`'s class gate is unchanged from v1: `entry_credit_reason()` (`measure.py:430-466`)
   credits `class=record` + `verdict=verified-record` with `commands_executed_count=0`.
2. `bucket-commands.json` — the map K02 correction 2 says must drive the class gate — is used by
   **no** `.py` in the lane: `grep -rn 'bucket-commands' --include='*.py' .` → no output.
3. End-to-end probe in the clone. One ledger entry for the round-14 section at `eb7838b`
   (`start 1563`, section sha `c121412bd8cf27b0f93b731ae0b43033870c429a5ebe14de77b234a2ada236a7`),
   `class=record`, `verdict=verified-record`, `blocking_gaps=0`, `wrong_expectations=0`,
   `commands_executed_count=0`, `inputs={".ufo/evidence/round-17/dispositions.json":
   "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f"}`. The ledger was committed
   in the clone (probe rev `b84fd763c6459356448dd7552c1fa0085e10619c`), so **no override flag** was
   used:
   ```
   python3 .ufo/evidence/round-17/measure.py --rev b84fd763c6459356448dd7552c1fa0085e10619c
   exit 0
   overrides_used False   trace_gate strict   score 6
   SECTION {'credited': True, 'heading': '## Effective expectation reconciliation — round 14',
            'reason': 'credited', 'start': 1563, 'vetoed': False}
   ```
   This is exactly K02 hole 2 ("the seat picks `class`; `record` + `verified-record` + 0 commands";
   K02 table row 2) and R05 F2's accepted residual, applied to an instruction bucket that
   `bucket-commands.json` marks `executes_commands=yes`.
4. What is closed: holes 3–4 (`OVERLAY_FIELDS` + `overlay-field-forbidden`, `measure.py:125-128,
   1263-1264`; `ls_tree_mode` + `input-not-blob`, `:318-336`; selftest cases `input-not-blob-dir`,
   `input-not-blob-symlink`, `overlay-field-forbidden`) and the **empty-inputs** form of F2
   (`inputs={}` → `inputs-unrecorded`). Hole 1 is narrowed (`traces-unrecorded`,
   `trace-input-unrecorded`, `trace-reason` `:360-415`) but the trace `argv` is never compared to
   `commands_executed`, and the section's extracted commands are never required — the half of K02
   correction 1 that `bucket-commands.json` was built for is unenforced.

The 89/89 claim itself is true: `python3 .ufo/evidence/round-17/measure.py --selftest` →
`MEASURE_SELFTEST: 89/89 pass`, exit 0. The false part is the closure of hole 2.

Impact: a Gate admission rests on a premise a wave-2 seat can falsify with one ledger entry; an
instruction bucket can still be credited by a seat-declared `record` read.

### F2 — MEDIUM — two round-17 mistakes found in wave 1 are absent from `## Mistakes`

**(a) Stale SCORECARD capability counts (K05 §3 H2; X13 "Findings for the L1" item 2).** The
round-17 tool edits changed the counts; the capability rows still quote the old ones at `eb7838b`:

| Row | States | Observed at `eb7838b` |
|---|---|---|
| `SCORECARD.md:241` | `MUTATE_SELFTEST: 80/80` | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 95/95 pass`, exit 0 |
| `SCORECARD.md:242` | `REGRESSION: PASS (cases=6 …)` | `mutate-and-run-regression` held in the baseline run; X05 `:139` and V02 §2 record `cases=7` |
| `SCORECARD.md:244` | `18/18 PASS0` | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)` |
| `SCORECARD.md:246` | `PASS34/34 exit0` | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (56/56)` |

K05 `:65` named this "stated outcomes that this round's own tool edits will falsify … the r16 harm
class"; X13 `:61-65` repeats it. The table's `stale receipt` row covers a different artifact (the
round-16 runner-sha file), so this is a distinct instance of the same class, unrecorded.

**(b) `evidence-disposition` selftest was red at the build-landing commit.** The committed
`c2-after-2a22ade.txt` records `ROW evidence-disposition-selftest expect=0 got=1 differs` (exit 1).
`eb7838b` is precisely the fix: `_selftest_git_env()` now supplies `GIT_AUTHOR_*`/`GIT_COMMITTER_*`
because `GIT_CONFIG_GLOBAL=/dev/null` had left `commit-tree` without an identity
(`git show eb7838b -- tools/evidence-disposition.py`, 22 lines; commit message names the cause).
Only the commit message records it; the lesson's `environment leak` row says the tools now scrub and
each has a canary case, but a reader never learns that the new selftest was red at the first landing
commit. Class: selftest-fixture hermeticity (the scrub removed the identity the fixture needed).

Both are real round-17 defects found by wave-1 seats/monitor, fixed in-round, and would belong in
the table's own vocabulary (`stale receipt` / `environment leak` neighbours).

### F3 — MEDIUM — C1's "box 3 re-earned" is not reproducible at the lesson's rev

Lesson `:6-8` states C1 as "input-keyed cold-read credit; box 3 re-earned on a full re-read under
it". At the lesson's own commit the ledger does not exist
(`git cat-file -e eb7838b:.ufo/evidence/round-17/coldread/ledger.json` → exit 128
`does not exist`), so the acceptance command for C1 returns:
```
python3 .ufo/evidence/round-17/measure.py --rev eb7838b16490ca7ba17ea3242ade76a61f744af2
exit 0   overrides False   score 6   box3 False   ledger_present False
```
The 8 depends on a wave-2 ledger that has not been committed. This is not a Gate/Mistakes row, but
it is the lesson's headline claim and should be future-tense until that ledger lands.

### F4 — LOW — G7's evidence pointer names the wrong K02 hole

Lesson `:24` (G7, reject) says "K02 hole 5: one edit would uncredit the whole page; the bucket is
keyed by its own section sha already". In `w1/K02InputCreditHoles.md`, **hole 5** is "Reads of the
live lane from a 'clone' run"; the quoted reasoning is **hole 7**, "Over-invalidation by the page
itself (and by the ledger and SHONEN)", with correction 5 ("Exclude the page and the ledger from
seat-opened inputs"). The substance holds: `IGNORED_INPUTS = frozenset(('SKILL.md',
DEFAULT_LEDGER_PATH))` (`measure.py:125`), and a one-bucket page edit leaves the other 53 credited
(S10-derived rule). A reader following "hole 5" lands on an unrelated attack.

### F5 — LOW — M5's fix does not discharge the sweep clause it cites

Lesson `:56` says the fix is "QUALITY 24's sweep clause". QUALITY 24 (`corpus/QUALITY.md:136-142`)
requires "every mention of the old outcome is swept in that round". At `eb7838b`, 12 of S10's 19
statements are unchanged:

- `SCORECARD.md:246` (34/34 selftest, replaced live-tree outcome), `:571` (54/54, calibration 6→8),
  `:586` (calibration improved 6→8), `:588` (operability "unchanged", "by design").
- `LOG.md:1036` (C2 6→8), `:1041-1042` (54/54), `:1044` (`--rev 09ee1d0` restraint 8).
- `corpus/README.md:231-233` ("are superseded").
- `corpus/lessons/round-16.md:6,23,63`: no errata block at this rev —
  `git show eb7838b:corpus/lessons/round-16.md | grep -n 'round 17\|Errata'` → empty.
- `corpus/knowledge/incremental-pin-disposition.md:362` (exit 1 wording).

The row's enumerated claims are true: the round-14 recipe steps 2–3 now say
"**Historical (round 14, runner `75ed934d…`)**" and give the `git archive 28aeef4` replay
(`SKILL.md:1581-1586`); `:1601` and `:1681` point at the live v2 entry; the line-count and
round-16 full-page claims are superseded by the round-17 correction paragraph
(`SKILL.md:1855-1867`, exact text "Both statements stay as written; this paragraph supersedes
them"). The gap is that the criterion cited demands the other 12 too.

### F6 — LOW — two pointer imprecisions

- **M6's repair commands are self-referential.** Lesson `:57` asserts the L1 used
  `git read-tree 98bea7d` and `update-ref --no-deref HEAD 98bea7d`. `git grep` over `eb7838b` finds
  those strings only in `corpus/lessons/round-17.md:57`; neither `w1/R04ReviewContractB.md` nor
  `w1/N01TraceGitSafety.md` names the commands. R04 quotes the reflog message and verifies HEAD
  `98bea7d…` + 1296-file index, so the outcome is evidenced; the commands are not.
- **M7's "four knowledge entries" undercounts by one.** Four ER-jj append-only entries do read the
  branch tip (`fleet-kill-rate-ledger.md:420`, `incremental-pin-disposition.md:386`,
  `service-limits.md:279`, `verification-patterns-fleet.md:309`); `operator-runbook.md:49,281`
  (ER-R3) is a fifth knowledge file that does. Cosmetic.

## Gate rows — line-by-line

| Row | Claim checked | Result |
|---|---|---|
| G1 `:18` | blanket waiver hid an edit; landed manifests waive only the two moved instruments; the tool refuses an unneeded waiver | **holds.** `dispositions.json` `historical_inputs` = `mutate-and-run.sh`, `pin-disposition.py` at `4acc607`; an added waiver of `tools/witness-metadata.py` → exit 2 `historical_input_unneeded` ("live bytes still equal the expected pin; the waiver is unnecessary"). K03 T1 and X01's follow-up (`exit 2 historical_input_unneeded … L1 must narrow`) support the history |
| G2 `:19` | moves committed, rev an ancestor, git hermetic; v1 byte-equal (X01 differential) | **holds.** Guards G1–G7 in the tool docstring (`evidence-disposition.py:39-60`); `GIT_NO_REPLACE_OBJECTS`/`GIT_GRAFT_FILE`/shallow/`show-toplevel`/ancestor checks at `:361-454`; the v2 after-run passing G3 proves the rev is an ancestor of `eb7838b`; X01 `:160-171` records the byte-equal differential |
| G3 `:20` | the ":1681 by-design" text relabelled the harm; grade against 0 clean (SCORECARD:246) | **holds.** K01 O4 (`:80-100`) and K04 O2 (`:83-91`) say exactly that; `SCORECARD.md:246` records "after CLEAN0, eleven effective+one superseded" |
| G4 `:21` | a behaviour-changing mutant left 54/54 credited; the bucket was credited while its recipe exited 2 | **holds.** M01 table `:70-74`: pristine/mutant/restored all `54/54`, `box3_full_page true`, `restraint 8`, selected bucket credited; mutant is `return 2`→`return 0` at `:1081` |
| G5 `:22` | K02 holes 1–4 and R05 F1–F3 closed; 89/89 selftest; red-before | **partly false — F1.** 89/89 reproduced; red-before reproduced (`redbefore/measure-e69b488.json` → bucket `credited`; `measure-09ee1d0.json` → `input-drift:tools/mutate-and-run.sh`); hole 2 open by execution |
| G6 `:23` | overlays are demonstrations; a cited score uses no override | **holds.** K06 condition 7 `:81-85` says exactly this; `measure.py` reports `overrides_used` and strict mode refuses absent traces; strict `--rev eb7838b` → `overrides False` |
| G7 `:24` | page/ledger must not be inputs | **substance holds, pointer wrong — F4** (`IGNORED_INPUTS` `measure.py:125`; K02 hole 7, not 5) |
| G8 `:25` | `probes.mjs` FXROOT guard stays backlog | **holds.** JjAudit `:96` names the hazard; C03 B20/G2 (`:65`, `:132`) declines with the immutable-evidence reason |
| G9 `:26` | jj-lane helper auto-track fail-closed is fleet scope; live config already `none()` | **holds.** JjAudit R3 `:301-308`; S20 fact 10 (`:23`) records `snapshot.auto-track = "none()"` |

## Mistakes rows — line-by-line

| Row | Pointer | Result |
|---|---|---|
| credit-drift `:52` | spotcheck §2; V03; `w2/CalibCritic.md:120,140`; QUALITY 23; `redbefore/measure-*.json` | **holds.** Spotcheck §2 ("The ledger credits a bucket by its section sha … its recipe then exited 2"); V03 §5 proposes the same class; CalibCritic `:120` ("section hashes alone do not validate dependencies") and `:140` (condition 4); QUALITY 23 `:127-135`; the two red-before files show `credited` → `input-drift:tools/mutate-and-run.sh` |
| expectation relabelling `:53` | round-16 `SKILL.md:1681`; round-16.md:63; V01; QUALITY 24; v2 manifests; op1 red-before | **holds.** `98bea7d:SKILL.md:1681` says "returns 2 `expected_input_digest_mismatch` by design"; `round-16.md:63` Captured-by "the gate itself (by design)"; V01 §5 ("RR10 graded it gap-blocking … RX5 verified the weakened text faithfully"); v2 after exit 0 / before exit 1; `op1-redbefore-98bea7d.txt` exit 2 |
| monitor scope `:54` | V02; held=10/11 at c699c8c; QUALITY 25; 98bea7d differs exit 1 | **holds.** V02 §2 table says `held = 10/11`; `c2-before-98bea7da….txt` shows `evidence-disposition-round17 expect=0 got=2 differs`, `held=22/23`, exit 1 |
| stale receipt `:55` | runner-sha256.txt; c699c8c runner; 05a2247 move; R07 | **holds.** Receipt first line `89722ddb…` = `git show c699c8c:tools/mutate-and-run.sh`; `05a2247`/`98bea7d` = `0673d2e5…`; appended dated correction, original line kept |
| partial sweep `:56` | closure §3; S10's 19; QUALITY 15 (partial); recipe/`:1601`/`:1681`; correction paragraph | **literal claims hold; fix incomplete — F5** |
| environment leak `:57` | R04/N01; 12:29:33; e16adb7; 3 fixture files; QUALITY 27; 95/95; 89/95 mutant | **holds.** R04 `:24-48`; N01 `:16-27`; commit chain verified `98bea7d → f8832ef → 0559c60 → e16adb7` (final HEAD `e16adb7`), index `exec.sh noexec.sh target.sh`; runner selftest `95/95 pass`, exit 0; X05 `:141` mutant `89/95`, canary HEAD moved; five tools scrub and each has a case (registry canary `:665-669`; measure `git-env-scrubbed` `:1283-1286`; trace `env-scrubbed` `:891-897`; assemble decoy `:1406-1412`; evidence-disposition `v2-gitdir-env`) — plus F6's command caveat |
| jj HEAD semantics `:58` | `pin-disposition.py:318`; `jj/head-vs-branch.sh` exit 1; detect_branch; selftest case; SKILL 1027-1035; four knowledge entries | **holds.** `98bea7d:tools/pin-disposition.py:318` reads `HEAD^{commit}`; running the fixture on those bytes → exit 1 ("head observation used detached HEAD … jj @- snapshot"); on the landed tool → exit 0; `detect_branch` `:324`, `head_differs_from_branch` `:426`; `SELFTEST_CASE detached-head-uses-branch-tip PASS` (19/19); SKILL `:1027-1035` (`refs/heads/<branch>^{commit}`, "never a jj working-copy HEAD"); four ER-jj entries (F6's fifth-file note) |
| repo identity `:59` | `git -C "$repo"` no guard; JjAudit §2.2, S062; `repo_identity_mismatch`; 86/88 mutant | **holds.** JjAudit §2.2 ("`mutate-and-run.sh:1000-1035` does not [guard]"); guard at `tools/mutate-and-run.sh:1053`; X05 `:55` mutant `86/88, VERDICT: FAIL, exit 1` |

## Mistake classes — distinct?

Yes. The eight mechanisms are separable: `credit-drift` (credit predicate missing a dimension),
`expectation relabelling` (rewriting the stated outcome to match the harm), `monitor scope` (test
selection), `stale receipt` (a receipt naming a superseded digest), `partial sweep` (corrections not
propagated to mentions), `environment leak` (inherited `GIT_*` redirecting fixture commits), `jj
HEAD semantics` (colocated `HEAD` is `@-`), `repo identity` (git answers from the super-repo).
Closest pair, `stale receipt` vs `partial sweep`, differs in artifact and fix (one file vs a
page-wide mention sweep); V03's distinction table separately separates `credit-drift` from
`reference-drift`, `stale-expectation`, `stale-premise` and `vacuous`.

## Commands and exits (all in the clone unless stated)

| Command | Exit | Key line |
|---|---|---|
| `python3 .ufo/evidence/round-17/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 89/89 pass` |
| `python3 .ufo/evidence/round-17/measure.py --rev eb7838b…` | 0 | `overrides False score 6 box3 False ledger_present False` |
| `python3 .ufo/evidence/round-17/measure.py --rev b84fd76…` (single record/0-cmd entry) | 0 | `overrides_used False`, `trace_gate strict`, section `credited: True` |
| `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json` | 0 | `EVIDENCE_DISPOSITION: clean … effective=11 superseded=1` |
| same with `dispositions-before.json` | 1 | `status=failed`, finding `expected_contains_missing` |
| same with an added waiver of `tools/witness-metadata.py` | 2 | `historical_input_unneeded` |
| `python3 tools/registry-check.py --rev eb7838b… --registry tools/registry.json --tag baseline` | 0 | `REGISTRY_CHECK: held=23/23 superseded=1` (151.09 s) |
| `bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 95/95 pass` |
| `python3 tools/pin-disposition.py --selftest` | 0 | `SELFTEST: PASS (19/19)` |
| `python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (56/56)` |
| `bash .ufo/evidence/round-17/jj/head-vs-branch.sh <98bea7d tool>` | 1 | "head observation used detached HEAD … jj @- snapshot" |
| `bash .ufo/evidence/round-17/jj/head-vs-branch.sh tools/pin-disposition.py` | 0 | "head observation used master's tip … branch-safe" |
| `git cat-file -e eb7838b:.ufo/evidence/round-17/coldread/ledger.json` | 128 | `does not exist in 'eb7838b…'` |

## Residual risk and verification gaps

- **C1 waits on the wave-2 ledger.** The landing rev has no `ledger.json`; F3 is a sequencing
  observation, not a statement that the eventual ledger will fail. Re-run the C1 form after the
  ledger is committed at a 40-hex rev.
- **Live-lane reflog not read.** The contract forbids lane git writes; a read-only reflog read was
  not attempted. M6's repair-command wording therefore rests on the lesson, not an independent
  receipt (F6).
- **`pin-disposition-read` is a declared external live-fleet row** (`tools/registry.json` `argv`
  names `/home/vgpnk/Projects/shokunin`, `"external": true`). Its `held` in the 23/23 run is a
  declaration-permitted non-hermetic read (K04 P7), not a clone-only reproduction. No lesson row
  claims otherwise.
- **`--regression` was not run directly.** Its baseline row held inside the 23/23 run; X05/V02
  record `cases=7`. The stale `cases=6` text in F2(a) is therefore evidenced by those reports and
  the held row, not by a separate regression invocation.
- **Tool installs/updates: none.**

Verdict: **partial** — 7/9 Gate rows and all 8 Mistakes rows hold against their pointers; G5's
"K02 hole 2 closed" is false by execution (strict-mode credit with a `record`/0-command entry),
G7 cites the wrong K02 hole, the `partial sweep` fix leaves 12/19 statements unswept, and two
wave-1 round-17 defects (stale SCORECARD counts, the `2a22ade` selftest hermeticity break) are
missing from the table.

Report: `.ufo/waves/round-17/w2/LessonReview.md`
