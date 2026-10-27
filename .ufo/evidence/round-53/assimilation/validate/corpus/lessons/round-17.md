author: tameshi-shokunin (lane L1, round 17)

# Round 17 — live-tree re-pin, entry-command monitor, input-keyed cold-read credit

Repair-first round after round 16 closed rejected-harmed
(`round-16-verifier-spotcheck.md`). Claims: **C1 calibration** (input-keyed
cold-read credit; box 3 re-earned on a full re-read under it) and **C2
operability** (the round-14 disposition gate returns its admitted 0 clean at
the branch tip again; an entry-command monitor grades every registered
command). Routed defects R16-OP1, C2a, C2b, C2c, EV1, MON1 are all worked
this round; the jj-migration findings for this lane are fixed or declined
below. Waves: `.ufo/waves/round-17/`.

## Gate

| # | Candidate | Decision | Reason |
|---|---|---|---|
| G1 | v2 disposition manifests waiving all four `tools/` inputs (X02 first draft) | reject | K03: a blanket waiver hid a one-line edit to an unchanged `tools/pin-disposition.py` (model gate 0 clean where v1 exits 2). Landed manifests waive only the two moved instruments; the tool refuses an unneeded waiver (`historical_input_unneeded`) |
| G2 | v2 manifests waiving `tools/mutate-and-run.sh` and `tools/pin-disposition.py` at `4acc607` with G1–G7 guards | admit | moves are committed (`historical_input_uncommitted` otherwise), rev is an ancestor commit, git runs hermetic; v1 behaviour byte-equal (X01 differential) |
| G3 | grading the disposition row against SKILL.md:1681's "returns 2 by design" | reject | K01 O4, K04 O2: that text relabelled the harm; the row is graded against its admitted outcome, 0 clean (SCORECARD:246) |
| G4 | sha-only cold-read credit (round-16 rule) | reject | M01: a behaviour-changing mutant of `tools/evidence-disposition.py` left 54/54 credited; the round-14 bucket was credited while its recipe exited 2 |
| G5 | input-keyed credit with class-independent gate, trace binding, veto aggregation | admit | K02 holes 1–4 and R05 F1–F3 closed in `measure.py` (89/89 selftest); red-before on real bytes (credited at `e69b488`, `input-drift` at `09ee1d0`) |
| G6 | `--inputs-overlay` numbers as the claimed score | reject | K06 condition 7: overlays are demonstrations; a cited score uses no override (`overrides_used: false`) |
| G7 | including every seat-opened file (SKILL.md, the ledger) as an input | reject | K02 hole 5: one edit would uncredit the whole page; the bucket is keyed by its own section sha already |
| G8 | `probes.mjs` `FXROOT` guard (JjAudit §1.4) | reject this round | round-16 evidence bytes stay immutable; default root is `/tmp` and the override is operator-set only (C03) |
| G9 | jj-lane helper `commit` fail-closed on missing auto-track config (JjAudit R3) | reject (not lane scope) | fleet-owned `scripts/hyaku/jj-lane.sh`; live repo config already carries `snapshot.auto-track = "none()"` (S20) |

Sources opened this round (rule 1 — URL, access date, quote ≤25 words with location):

| Row | URL | Accessed | Quote (location) |
|---|---|---|---|
| S058 | https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems-final.pdf | 2026-10-20 | "record the values/hashes of dependencies used last time, and if something has changed, the key is dirty and must be rebuilt" (§4.2.2 Verifying Traces, p. 79:14) |
| S059 | https://bazel.build/remote/caching | 2026-10-20 | "Then, two users with different compilers installed will wrongly share cache hits because the outputs are different but they have the same action hash." (§Known issues, "Bazel does not track tools outside a workspace") |
| S060 | https://man7.org/linux/man-pages/man1/strace.1.html | 2026-10-20 | "Traces all system calls that take a file name as an argument." (OPTIONS → Filtering → `-e trace=` → `%file`) |
| S061 | https://docs.jj-vcs.dev/latest/git-compatibility/ | 2026-10-20 | "Convince jj to update .git/HEAD to point to the working-copy commit's parent" (§Converting a workspace into a colocated workspace, recipe comment) |
| S062 | https://git-scm.com/docs/git-rev-parse | 2026-10-20 | "Show the (by default, absolute) path of the top-level directory of the working tree. If there is no working tree, report an error." (OPTIONS → Options for Files → `--show-toplevel`) |
| S063 | https://git-scm.com/docs/git | 2026-10-20 | "a list of directories that Git should not chdir up into while looking for a repository directory" (ENVIRONMENT VARIABLES → The Git Repository → `GIT_CEILING_DIRECTORIES`) |
| S064 | https://bazel.build/basics/hermeticity | 2026-10-20 | "The output of an action can be cached, and the action need not be run again unless inputs change." (§Benefits) |

Registry changes: rows S058–S064 added, status `mined` (used-by
`knowledge/input-keyed-coldread-credit.md` for S058, S059, S060, S064; this
lesson for S061, S062, S063); no existing row's status, recheck or used-by
changed. Id-allocation footer: next unused S058 → S065.

Spot-check: the outside admit/reject sample is the separate non-author
closure's duty; not claimed here.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| credit-drift | `round-16-verifier-spotcheck.md` §2 (round-14 bucket credited on section sha while its recipe exited 2); `.ufo/waves/round-17/w1/V03ShaOnlyOrigin.md`: round-16 wave-2 CalibCritic named input drift (`w2/CalibCritic.md:120,140`) and it was dropped unrecorded | none (no QUALITY criterion keyed credit to inputs) | QUALITY 23. `.ufo/evidence/round-17/measure.py`: same ledger, same overlay — bucket `credited` at `e69b488`, `input-drift:tools/mutate-and-run.sh` at `09ee1d0` (`redbefore/measure-*.json`); selftest red-before case. Shown able to fail on real bytes |
| expectation relabelling | round-16 `SKILL.md:1681` and `lessons/round-16.md:63` recorded the round-14 gate's exit 2 as "by design"; `w1/V01R16RunnerBreak.md` (RR10 graded it `gap-blocking`, RX5 later `executed-ok` on the amended text) | the lane's own re-pin rule (SKILL.md:1083-1084) — not applied | QUALITY 24. Superseding v2 manifests: `--root . --dispositions .ufo/evidence/round-17/dispositions.json` → 0 clean, red-before `op1-redbefore-98bea7d.txt` (exit 2). The row keeps its admitted outcome, 0 |
| monitor scope | round-16 ToolsNoHarm ran nine selftests only (`w1/V02ToolsNoHarmScope.md`); a registered-command run at `c699c8c` gives `held=10/11` | none | QUALITY 25. `tools/registry-check.py` over `tools/registry.json`; graded at `98bea7d` with the round-17 registry the disposition capability differs (exit 1) — the monitor fails on the harm it missed |
| stale receipt | `.ufo/evidence/round-16/round-gate/runner-sha256.txt` named the `c699c8c` runner after `05a2247` moved it (R16-EV1) | none | QUALITY 26. Dated correction appended to the receipt; original line kept (`w1/R07RunnerShaReceipt.md`: nothing pins the file) |
| partial sweep | closure §3: only SKILL.md:1681 was annotated; `w1/S10MentionSweep.md` found 19 stale outcome statements, including recipe steps 2–3 and the errata's line-count claim | QUALITY 15 (partial) | QUALITY 24's sweep clause. Recipe steps 2–3 marked historical with the working archived invocation; :1601/:1681 point at the live v2 entry; the line-count claim and the round-16 full-page claim are superseded by the round-17 section's correction paragraph |
| environment leak | wave 1, 12:29:33: seat R04 ran `GIT_DIR=<live lane>/.git bash tools/mutate-and-run.sh --selftest` from a `/tmp` clone; the selftest's fixture commits landed in the live lane (HEAD detached at `e16adb7`, index = 3 fixture files). L1 restored HEAD and index (`git read-tree 98bea7d`, `update-ref --no-deref HEAD 98bea7d`, reflog message names the repair); no file bytes were lost (`w1/R04ReviewContractB.md`, `w1/N01TraceGitSafety.md`) | none (round-16 G5 scrubbed the suite string only, not the selftest fixtures) | QUALITY 27. Runner `git_clean()`/`fixture_commit()` scrub every inherited `GIT_*`; the selftest's canary case (exported `GIT_DIR` to a canary) fails on the unscrubbed mutant (89/95, canary HEAD moved) and passes 95/95 on the landed runner; registry-check, measure, trace-inputs, assemble and evidence-disposition scrub too, each with a decoy/canary selftest case |
| jj HEAD semantics | `tools/pin-disposition.py:318` read sibling `HEAD^{commit}` (`JjAuditTameshi.md` §2.3); `.ufo/evidence/round-17/jj/head-vs-branch.sh` on the committed tool exits 1 (reads the detached commit's bytes) | none | Branch-tip resolution (`detect_branch`), head rows carry `branch` and `head_differs_from_branch`; selftest case `detached-head-uses-branch-tip`; SKILL.md:1027-1035 and four knowledge entries read the branch tip (S061) |
| repo identity | `tools/mutate-and-run.sh` read `git -C "$repo"` with no identity check; a lane dir without `.git` inside the fleet super-repo is answered from the super-repo (`JjAuditTameshi.md` §2.2, S062) | none | `repo_identity_mismatch` SETUP guard; the guard-removed mutant fails the new selftest case (86/88 at first build) |

## Same-round falsification (wave 2) and residual

Wave 2: 99 seats (58 cold reads, 41 attacks) at `eb7838b`. Seven m_opus
seats died on provider errors and were not respawned: CriticC1, CriticC2,
CriticNoHarm, CriticSeparability, RegistryProvenance, SentinelLanded (429),
SentinelTraceEscape (Devin quota). What held: RerunOP1 and TamperV2Matrix
(17/17 tamper rows exit 2 with the stated ids; v1 path byte-equal), RerunC2Before
(22/23, only the disposition capability differs) and RerunC2After (23/23
baseline, 28/28 full, superseded 1), RerunRunnerGuard (95/95, cases=7, canary
`.git` digest unchanged under an exported `GIT_DIR`), RerunPinBranch (fixture
exit 1 on the old tool, 0 on the landed one), RerunRedBefore, NoHarmSelftests
(16/16 entry points green, strictly additive counts), SiblingImpact (no sibling
gate pins the moved bytes; mado's live regression passed on the landed runner),
all seven source re-opens, RerunCensus.

Additional mistakes found by wave 2:

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| producer/consumer drift | `w2/ReviewMeasureV2Code.md`: measure checked receipt `external` for live-lane reads while trace-inputs writes them to `live_lane_reads`; a real offending receipt was credited | none (selftest fixture used the impossible shape) | measure/assemble read `live_lane_reads`; a live read is bound only when it is a `.git/` read or the bytes equal the blob at the rev (`live-lane-read-bound` selftest case; the old real-shape fixture now fails as `live-lane-read:`) |
| class dodge | `w2/LessonReview.md` finding 1: a zero-command `record` entry with any verified input credited a bucket at a committed rev | G5 claimed K02 hole 2 closed — wrong | `commands-unrecorded`: an entry credits only with commands_executed_count>0 and committed traces; selftest `record-zero-cmd-commands-unrecorded` |
| stale present tense | wave 2 found 7 wrong expectations: CR13 (POLICY exit shape), CR27 (fleet lane map), CR28 (T1 live cells, replay receipt), CR51 (selftest exit sentence), CR54 (round-16 assemble exits), CR57/CR58 (missing-ledger exit, step-3/4 commit ordering) | the full-page cold read itself | repaired in place, line counts kept; buckets queued for residual fresh reads |
| hermeticity of a selftest | `registry-check --rev` (scrubbed env, `GIT_CONFIG_GLOBAL=/dev/null`) turned `evidence-disposition --selftest` red: fixture `commit-tree` had no identity | the monitor itself (QUALITY 25 worked as designed) | `_selftest_git_env()` pins identity and scrubs `GIT_*`; fixed in `eb7838b` |
| false criterion | `w2/QualityCriteriaReview.md`: QUALITY 27 false as landed (`bash-witness-study.py` and the jj fixture did not scrub) | the criterion's own red-before demand | QUALITY 28 correction; fixture now scrubs and proves it on a canary; `bash-witness-study.py` scrub is open debt (pinned by round-13 `expected.json`) |
| seat-caused lane damage | see `## Mistakes`, environment leak | — | — |

Open, named, not closed by prose: selftest survivors (MutateDispositionV2: G3
tag-object and G5 symlink-mode guards; MutateRegistryCheck: detached-checkout
and short-rev source regex; MutateTraceInputs: O_RDWR exclusion, pycache prefix,
execve guard — each guard's behaviour is correct, the selftests do not pin it);
registry-check NaN/Infinity `timeout_s` crash and setsid-escapable timeout
(ReviewRegistryCheckCode); evidence-disposition G2/G3 compare against `HEAD`,
not the branch tip (HeadSweepRecheck); knowledge entry
`input-keyed-coldread-credit.md` §5 states a missing ledger exits 2 (it exits 0
`no-ledger`); duplicated sectionizer/path predicates across measure and assemble
(SimplifyNewTools); `bash-witness-study.py:337-341` env scrub.

## Correction — round 18 wave 1 (append-only, 2026-10-20)

Earlier lines are unchanged. Pinned base: `183f87b899e6cae46be98d251cbc87fb5118f6ca`. Checked against: `.ufo/evidence/round-17/measure.py` at the base (sha256 `d25d3d04…`); `corpus/lessons/round-17-verifier-spotcheck.md` §4–§5 and §7; `.ufo/waves/round-17/w1/K02InputCreditHoles.md`; `.ufo/waves/round-17/w2/NoHarmSelftests.md:57`.

1. **Line 22 (G5) overstates the K02 closure.** It reads: "K02 holes 1–4 and R05 F1–F3 closed in `measure.py` (89/89 selftest)". Read it as: holes 3 and 4 are closed (`OVERLAY_FIELDS` at measure.py:134 with the `overlay-field-forbidden` selftest case at :1358; `cat_file_blob` at measure.py:182–184, so a directory key is `input-missing`); the zero-command part of hole 2 is closed (`commands-unrecorded`, measure.py:517); the input-to-trace part of hole 1 is closed (`trace_reason`, measure.py:368–426: `trace-input-unrecorded`, `trace-input-drift`, `live-lane-read`). Still open: the command binding that K02 hole 1 (fix item 1) and hole 2 (fix item 2) require. `trace_reason` never reads a trace receipt's `argv` or `rev` (the only `argv` in measure.py is the selftest fixture at :773), so `commands_executed` is not bound to receipt argv and the receipt rev is not bound to `read_rev`. No `commands-unbound` or `class-mismatch` reason exists. Neither measure.py nor assemble.py reads `coldread/bucket-commands.json`, so the seat's `class` is not checked against the page. [INFERENCE from the code path, not run]: a `record` entry with commands>0 and a trace that passes `trace_reason` still credits. The spot-check (§5 G5 row, line 324; §7 item 2, lines 423–427) reaches the same finding. Routed as R17-CMD-BIND.
2. **Line 24 (G7) points at the wrong hole.** It reads "K02 hole 5". The pointer should read **K02 hole 7**: `K02InputCreditHoles.md` hole 7 is over-invalidation by the page itself (SKILL.md is in every seat's inputs). Hole 5 is reads of the live lane from a clone run. The spot-check §5 G7 row (line 327) gives the same reading.
3. **Line 22 (G5) dates the measure selftest at 89.** The 89 is the W2 receipt at eb7838b: `.ufo/waves/round-17/w2/NoHarmSelftests.md:57` records `MEASURE_SELFTEST: 89/89 pass` for `measure.py` at eb7838b (sha256 `f348adc3…`). The final measure selftest at 183f87b (`measure.py` sha256 `d25d3d04…`) prints `MEASURE_SELFTEST: 94/94 pass`, exit 0, reproduced in a clone with the GIT_* scrub; the spot-check §4 table (line 306) records 94/94 for the same bytes. These are versioned receipts for different bytes and are not interchangeable. 89 is not the final selftest count.

The G5 row's decision (admit) is not rewritten here; this block narrows only the stated reason and the two pointers.
