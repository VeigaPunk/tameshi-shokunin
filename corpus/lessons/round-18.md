author: tameshi-shokunin (lane L1, round 18)

# Round 18 — eighth recorded case, routed-defect closure

Claims: **C1 depth** (lowest owned numeric axis, 7 → 8: the eighth recorded
mutation case, kumitate `scripts/sources-check.mjs`, leg `js-sources-check`)
and **C2 operability** (the eleven round-17 routed tool defects closed with
failure-backed selftests; ruler `.ufo/evidence/round-18/defect-probes.py`).
Calibration 8 is a no-harm monitor: the build moved inputs of 50 of 60
SKILL.md buckets; wave 2 re-read them into the round-18 ledger. Every item in
`round-17-verifier-spotcheck.md` §7 is worked below or routed. Waves:
`.ufo/waves/round-18/`.

## Gate

| # | Candidate | Decision | Reason |
|---|---|---|---|
| G1 | case-8 target kagi/kake gates outside PROVINCE `Owns` (kake `scripts/corpus-contract.mjs`) | reject | not a declared primary surface; would need service opt-in (`PROVINCE.md:7-11`, `service-optin-protocol.md`); kumitate `scripts/sources-check.mjs` is (w1 S05, C01) |
| G2 | case 8 = kumitate `sources-check.mjs` @ `0acb775`, spec + predictions committed before any mutant (`93d22aa`), hermetic suite, 8 byte-identical controls | admit | sweep 5/10, 10/10 predictions held; `--regression` cases=8 PASS (`.ufo/evidence/round-18/leg8-L1-check.txt`); w1 R01, K02, C05 conditions |
| G3 | leg-8 suite string `node "$MUTANT" --selftest` (bare) as first staged | reject | K02: not the pre-registered hermetic suite; the embedded leg now uses `suite.txt` verbatim |
| G4 | C2 ruler: guard probes `closed` when the mutant's selftest fails | reject as written | K04/K01: an always-red selftest would close every probe; a probe is `closed` only with a green pristine control in the same sandbox |
| G5 | C2 ruler committed with a base receipt before any fix (`aee4f36`, open=11/11) | admit | K01 condition C1; fixes landed later (`58e5d53`) |
| G6 | ruler v2 after the v1 tip run errored (P08 fixture unbound; probe child PATH lacked jj) | admit, disclosed | the v1 tip receipt is retained (`c2-probes-e08271a.txt`); v2 re-run on both revisions: base open=11, tip open=0 (`c2-probes-v2-*.txt`); wave-2 CriticC2Ruler attacks it |
| G7 | G2/G3 read `refs/heads/<branch>` only (contract D as written) | reject | V01: false-fails `registry-check --rev` clones; landed one shared anchor (lane.branch / attached branch; jj unbound → refuse; detached clone only when a ref contains it) |
| G8 | round-18 v2 manifest superseding the round-17 v2 manifest | reject | `check_supersedes_lineage` requires a v1 target (X07, K05); supersedes the round-14 v1 manifest like round 17 and records round-17 → round-18 in the registry |
| G9 | bind trace argv to the bucket's required commands this round (R17-CMD-BIND) | reject this round | K03: the spot-check offers the narrower claim; kept input-keyed credit, named corrections appended, QUALITY 33 forbids calling it command coverage |
| G10 | safety envelope for probes and seats (bwrap, fleet read-only, private HOME/TMPDIR, GIT_CONFIG_GLOBAL=/dev/null) | admit | N01: a /tmp clone with live sibling symlinks is not a write boundary |

Sources opened this round (rule 1 — URL, access date, quote ≤25 words with location):

| Row | URL | Accessed | Quote (location) |
|---|---|---|---|
| S008 | https://arxiv.org/abs/2102.11378 | 2026-10-20 | "Mutants are selected based on the historical performance of mutation operators, further eliminating irrelevant mutants and improving mutant quality." (Abstract, item (3); arXiv:2102.11378v2) |
| S065 | https://docs.python.org/3/library/json.html | 2026-10-20 | "by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values" (§Standard Compliance and Interoperability › Infinite and NaN Number Values; inline code markup removed) |
| S066 | https://www.rfc-editor.org/rfc/rfc8259 | 2026-10-20 | "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted." (§6 Numbers) |
| S067 | https://man7.org/linux/man-pages/man2/prctl.2.html | 2026-10-20 | "PR_SET_CHILD_SUBREAPER" (§DESCRIPTION, operation list; the page has three occurrences in total; rejected row, quoted for its absence of a rule) |
| S068 | https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html | 2026-10-20 | "When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper." (§DESCRIPTION, first paragraph after SYNOPSIS) |
| S069 | https://man7.org/linux/man-pages/man2/setsid.2.html | 2026-10-20 | "The calling process will be the only process in the new process group and in the new session." (§DESCRIPTION ¶2) |
| S070 | https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables | 2026-10-20 | "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree" (§10.8 Environment Variables, Repository Locations; curly apostrophe as printed) |
| S071 | https://docs.jj-vcs.dev/latest/working-copy/ | 2026-10-20 | "The working copy is where the current working-copy commit's files are written so you can interact with them." (§Introduction ¶1; rejected row, quoted for scope) |
| S072 | https://man7.org/linux/man-pages/man2/open.2.html | 2026-10-20 | "the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0." (§DESCRIPTION, O_TRUNC entry) |
| S073 | https://docs.python.org/3/using/cmdline.html | 2026-10-20 | "If this is set, Python will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories" (§1.2 Environment variables, PYTHONPYCACHEPREFIX) |
| S074 | https://git-scm.com/docs/git-symbolic-ref | 2026-10-20 | "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently." (§OPTIONS, -q / --quiet) |

Registry changes: rows S065–S074 appended (S065, S066, S068, S069, S070, S072,
S073, S074 `mined`, used-by `corpus/knowledge/guard-kill-closure.md`; S067,
S071 `rejected`). S008 status `queued` → `mined`, used-by `—` →
`corpus/knowledge/mutation-case-kumitate-sources-check.md` (the only in-place
row change). Appended note correcting the S060 anchor (explicit syscall list,
not `%file`) and the S061 paragraph (¶3). Footer: `Next unused id: S065` →
`S075` (a replacement line, not a pure append). Drafts that duplicated S001,
S008 and S049 were not installed (`.ufo/waves/round-18/sources/`).

## Mistakes

Round-17 mistakes found or routed by the non-author spot-check. Anchors at base
`183f87b899e6cae46be98d251cbc87fb5118f6ca`.

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| breadth overclaim: G5 "K02 holes 1–4 closed"; hole 1 still open | `corpus/lessons/round-17.md:22` "K02 holes 1–4 and R05 F1–F3 closed"; `.ufo/waves/round-17/w1/K02InputCreditHoles.md:24` hole 1 "no binding to traces or to the section's commands"; `.ufo/evidence/round-17/measure.py:368` `trace_reason` binds receipt inputs to entry inputs (`trace-input-unrecorded`) but never reads receipt `argv` or the page's commands (the other `argv` hits are the CLI `main(argv)` at `:1462`, `:1483` and the fixture at `:773`); closed holes: 2 at `:517` (`commands-unrecorded`), 3 by the overlay field whitelist (`:82-84`), 4 by `git cat-file blob` at `:184`; spot-check §5 G5 row at `round-17-verifier-spotcheck.md:324` | partial: wave 2 caught hole 2 (`round-17.md:81` "G5 claimed K02 hole 2 closed — wrong"), but QUALITY 24's sweep clause did not reach the G5 gate row at `:22`; no criterion ties the breadth of a gate reason to the command coverage it claims | Named erratum at `:22`: holes 2–4 closed, hole 1 (trace argv and page-command binding) open. Fix: bind each receipt's `argv` to the entry's `commands_executed` and to the section's extracted commands. Falsifier: on the round-17 bytes, a fixture whose receipt inputs are a subset of the trace but whose argv is unrelated to the entry's commands is credited (red-before); after the fix it must be refused. Until that check exists, the `:22` wording stays wrong. |
| guard admitted without a killing test (7 survivors) | `.ufo/waves/round-17/w2/MutateDispositionV2.md:54` (G3 tag-object, "survived; non-equivalent"), `:58` (G5 symlink-mode); `.ufo/waves/round-17/w2/MutateRegistryCheck.md:52` (M06 detached checkout), `:53` (M07 short-rev regex); `.ufo/waves/round-17/w2/MutateTraceInputs.md:52` (M01 O_RDWR), `:54` (M03 pycache prefix), `:55` (M04 execve); named but admitted at `corpus/lessons/round-17.md:87` ("Open, named, not closed by prose") | none for the kill requirement. QUALITY 17 (`corpus/QUALITY.md:77`) asks for literal exits and stable finding IDs, not a kill per guard. QUALITY 22 (`:116`) requires survivor treatment only for attribution repairs | Owner adds one killing selftest case per guard (round-18 owner lanes; round-18 probes P01–P07, contract A). Falsifier: each probe reads `open` at `183f87b` (mutant survives, selftest exit 0; seven open is the red-before) and `closed` after the case lands (selftest nonzero on the mutant, 0 on pristine). |
| unexecuted exit contract admitted (knowledge entry) | `corpus/knowledge/input-keyed-coldread-credit.md:75` "2 rev/blob/ledger missing"; `.ufo/evidence/round-17/measure.py:546-552` (missing default ledger → `'reason': 'no-ledger'`, selftest `exit0-no-ledger` at `:940`); `.ufo/waves/round-17/w2/KnowledgeEntryReview.md:54` (wave 2 executed it: default missing → exit 0; explicitly requested missing `--ledger-file` → exit 2); named after admission at `corpus/lessons/round-17.md:94` ("§5 states a missing ledger exits 2") | none. QUALITY 1 (`corpus/QUALITY.md:3`) makes the sentence falsifiable, but nothing requires running its exit line before admission; QUALITY 7 and 10 check the coverage row and header fields only | Append an erratum beneath `:75` (QUALITY 4, 26) separating absent default ledger (exit 0, `no-ledger`) from explicitly requested missing ledger (exit 2); keep the original line. Falsifier: a command check that runs each documented exit line must FAIL on the admitted sentence (expects 2 for the missing default; observes 0) and PASS on the erratum. |
| wrong cross-reference | `corpus/lessons/round-17.md:24` "K02 hole 5: one edit would uncredit the whole page"; `.ufo/waves/round-17/w1/K02InputCreditHoles.md:28` (hole 5 = reads of the live lane); `:30` (hole 7 = over-invalidation by the page, the reasoning G7 cites); spot-check §5 G7 row at `round-17-verifier-spotcheck.md:327` | none | Named correction "K02 hole 7" (QUALITY 4). Falsifier: a check that the cited hole's text names the page or section SHA must fail on "hole 5" and pass on "hole 7". |
| stale count presented as current | `corpus/lessons/round-17.md:22` "(89/89 selftest)"; committed spot-check tally `round-17-verifier-spotcheck.md:306` ("round-17 measure \| 94/94") and `:311-312` ("earlier measure tally is 89, not the final 94") | none. QUALITY 26 (`corpus/QUALITY.md:150`) covers stale receipts, not lesson prose | Dated correction naming 89 (earlier version) and 94 (final), each with its revision. Falsifier: rerunning the measure selftest at the cited revision must return the stated count; stating 89 as final must fail. The 94 figure is the spot-check's committed tally, not re-executed for this draft. |


Captured-by, re-read (wave-2 CriticMistakes): the column above names what
should have caught each mistake *at round-17 admission*. Round 18's own
criteria now capture rows 1, 2 and 5 (QUALITY 33, 29, 35), each shown able to
fail by a committed artifact: the defect-probe base receipt
(`.ufo/evidence/round-18/c2-probes-v2-183f87b.txt`, open=11/11) for row 2; the
appended errata for rows 3–5.

Mistakes made this round (mined from wave 2; same columns):

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| criterion broken by its own landing | `58e5d53` replaced the SOURCES footer line `Next unused id: S065.` while QUALITY 35 (same commit) forbids it; `.ufo/waves/round-18/w2/ReviewAppendOnly.md` M1, `ReviewQuality18.md` | QUALITY 35 (new, same commit) | footer line restored, new pointer appended; corrections as `supersedes` rows S075–S078 (CORPUS.md rule 2). Falsifier: `git diff --numstat 183f87b <final> -- corpus/SOURCES.md` deletions = the four allowed used-by cells only |
| receipt taken on a staged, not landed, instrument | `.ufo/evidence/round-18/leg8-L1-check.txt` ran a `/tmp` runner whose leg-8 suite was still the bare `node "$MUTANT" --selftest` (`ReviewCase8Entry.md`); the guarded suite was installed after | none (no rule that a cited receipt names the instrument sha it ran) | case-8 entry ER8-5 discloses it; the landed-runner replays (w2 RerunC1, CR21, CR22, CR49: `cases=8 passed=8`) replace it. Falsifier: a receipt cited for a claim must print the runner sha256 equal to the landed blob |
| ruler unable to grade the fixed state | v1 probes errored at the tip (`.ufo/evidence/round-18/c2-probes-e08271a.txt`: P01/P02 pristine red without jj on PATH; P08 fixture unbound) | none | ruler v2 (two hunks) re-run on both revisions; w2 CriticC2Ruler/RerunC2Before judged it equal-application. Falsifier: v2 at base must still read open=11 (it does) |
| fixed-tool claim wider than its probe | P08 binds `master`, P11 exports two variables, P09 two literals: a hardcoded-`master` fix and a three-name unset pass both probe and selftest; finite `timeout_s` ≥ 2147484 still crashed (`ReviewGuardKillEntry.md` H3, `ReviewSkillDiff.md` F1) | QUALITY 29 (partly: guards, not probe breadth) | timeout capped at 86400 with two selftest cases (registry-check 48/48); guard-kill-closure EG-3 bounds what "closed" certifies; the two probe-breadth gaps are round-19 debt |
| post-wave edits invalidated wave-2 credit | the round-18 ledger row, SOURCES rows and SKILL repairs after wave 2 moved inputs of ~40 buckets (measure `--explain` at `9ee1c80`) | none | re-reads by the same seats at the final rev; lesson: land every corpus append before the cold-read wave |

## Wave 2 (falsify) — what changed the round

- C1 holds (RerunC1, CriticC1Depth, CR21/CR22/CR49 replays `cases=8 passed=8`);
  survivors probed (four non-equivalent, S_KIND help-only); kill attribution
  5/5; the case-8 ledger row was missing (CR16, CR18, CR31, CR33) and is now
  appended to `knowledge/fleet-kill-rate-ledger.md`.
- C2 holds as measured (RerunC2After, RerunC2Before, CriticC2Ruler) with the
  probe-breadth limits above; 18 mutation survivors in the new code are named
  round-19 debt (Mutate*18 reports).
- Twelve SKILL.md wrong expectations were found and repaired in place, line
  counts kept (CR02, CR13, CR15, CR16, CR18, CR21, CR27, CR31, CR33, CR40, CR42,
  CR43, CR46, CR47, CR48, CR50; ReviewMigration, ReviewSkillDiff).
- Risk observed: the tsukuroi leg flipped B8/B9/B10 once each under heavy
  load (CR20, CR44: 1 of 24 runs), so `--regression` is not load-proof (F3).
- Open, routed: `.ufo/evidence/round-16/measure.py` unscrubbed GIT_*;
  registry-check adopted-orphan signalling (SentinelKillCode);
  `git-env-canary.py` runs rows without isolation (SentinelProbeEnvelope);
  simplifications (SimplifyRound18) deferred.

## Gate addendum — correction rows and final checks (2026-10-20)

| Row | URL | Accessed | Quote (location) |
|---|---|---|---|
| S075 | https://man7.org/linux/man-pages/man1/strace.1.html | 2026-10-20 | "Traces only the specified set of system calls." (§Filtering, `-e trace=syscall_set`; supersedes S060's anchor) |
| S076 | https://docs.jj-vcs.dev/latest/git-compatibility/ | 2026-10-20 | "Convince jj to update .git/HEAD to point to the working-copy commit's parent" (§Converting, recipe comment; detached-HEAD prose is §Colocated ¶3; supersedes S061's anchor) |
| S077 | https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html | 2026-10-20 | "When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper." (§DESCRIPTION ¶2; supersedes S068's anchor) |
| S078 | https://man7.org/linux/man-pages/man2/open.2.html | 2026-10-20 | "These request opening the file read-only, write-only, or read/write, respectively." (§DESCRIPTION access modes; supersedes S072's O_TRUNC overstatement) |

These four mined correction rows cite this lesson. S001, S052, S056 and S057
used-by each changed from their previous value to that value plus
`corpus/knowledge/mutation-case-kumitate-sources-check.md`; all other cells
of those rows stayed unchanged. The final census is 76 rows
(A67 B7 C2; mined48 queued23 rejected5), not the earlier 72-row snapshot.
The final registered census first failed because this lesson did not literally
cite S076; this Gate addendum repairs that missing back-reference.
