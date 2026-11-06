# Round 89 — lesson (tameshi)

Base `61990f3d`; pre-freeze `a65e11c0` (instrument, controls, sources) and `48383295`
(full counter receipt); freeze `8876cca5` (`plans/round-89.plan.md`); landing `ff7a4b06`.
One claim, R89-C1 (operability, capability acquisition): `tools/ledger-witness.py`.

## Fresh-start reads

Amendment 46 fresh start. Read before declaring: rounds 86, 87, 88 (MANIFEST 1299, 1320,
1427) and their spot-checks. All three were honest stops of one class — a counter whose
predicate read a figure the certified subject prints, passed by a counterfeit that printed
it (r86 `att3b-cheat`, r87 `cf-c`/`cf-oid`, r88 `parked`/`stub`/`dupbase`). Round-88 routed
item 1 asked for an executed-set binding with blob-keyed targets and those three re-run as
controls. This round's answer moves the evidence channel off the subject's output entirely.

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S313 execve(2), man7 | admit (A, `mined`) | https://man7.org/linux/man-pages/man2/execve.2.html, fetched 2026-11-06 19:55:57 GMT, 43619 B, sha256 `ea744b04…d309` (`.ufo/evidence/round-89/sources/s313-execve.2.html`) | "many attributes of the calling process remain unchanged (in particular, its PID)" (12 words, snapshot line 463-464): the witness reads each verdict from the kernel exit of the pid that exec'd the interpreter, through `exec env -i … node "$MUTANT"`. "By default, file descriptors remain open across an execve()." (9 words, line 254): W_ORDER matches writes on `-y`-decoded fd paths, not only opens. |
| S314 strace(1), man7 | admit (A, `mined`) | https://man7.org/linux/man-pages/man1/strace.1.html, fetched 2026-11-06 19:55:58 GMT, 85238 B, sha256 `eedefecf…02f6` (`…/sources/strace.1.html`) | "Prints paths associated with file descriptor arguments and with the AT_FDCWD constant." (12 words, line 933) and "Prints unabbreviated versions of environment, stat, termios, etc. calls." (9 words, line 865) — the `-y` and `-v` contracts the witness's W_ORDER and W_ENV read. Scope distinct from S060/S075 (input observer over lane commands); census W04 (same URL, other scope) is the expected warning. |
| A third strace row under S060/S075's scope | reject | same page | within-scope duplicate (CORPUS rule 2); S314 states a new scope, the output contract the witness parses. Flip: a different strace document (e.g. strace's own `NEWS`) stating a changed `-y` format. |
| S315 Licker & Rice, "Detecting Incorrect Build Rules" (ICSE 2019), author manuscript | admit as `queued` (A, paper) — a frontier row for the round-90 successor, cited by no entry yet | https://api.repository.cam.ac.uk/server/api/core/bitstreams/306a073f-e1a0-4a49-93fd-2e3303c4c1ea/content, fetched by the L1 2026-11-06 21:05:06 GMT, 286638 B, sha256 `ceff92a9…2a4f` (`.ufo/evidence/round-89/sources/s315-mkcheck.pdf`; candidate found by wave seat T89S1) | "dependency graphs defined by users of build tools cannot be trusted" (11 words, §II-B p. 3, `pdftotext -layout` lines 165-167): the published precedent for checking a declared account of work against a syscall trace, conceding (p. 6, line 332: "some edges might be missing from the recovered graph") that the trace can miss edges — the shape of this round's declared limits. |
| mkcheck2 (ICSE 2026, eBPF), Lprov (ACSAC 2018), TraceCode, SLSA provenance | reject (T89S1's alternatives, `.ufo/waves/round-89/w1/T89S1.md` §(b)) | not re-opened by the L1 | mkcheck2's paper text is paywalled (no located quote); Lprov's object is attack provenance, not verification; TraceCode duplicates S060/S075's scope; SLSA is a declaration format, the thing the witness refuses to trust. Flip: an open mkcheck2 manuscript with a located quote. |
| Claim candidate: another print-binding counter (r88 routed item 1 as worded, `REGRESSION_CASE` names bound to declarations) | reject | `.ufo/evidence/round-89/landing/m1-r88-check-vs-stub-lines.txt` | the round-88 `executed-set-check.py` accepts `stub-lines` (declared=11 executed_pass=11 … ok, exit 0), so binding more printed lines is the same class (M1). Flip: none — superseded by kernel observation. |
| Assimilation (`merge/tameshi/`) | none this round | — | one claim; no staged theme serves it. |
| considerthese `2026-11-06.md` idea 5 (docstring↔code scan) | applied to the new tool | `considerthese/2026-11-06.md:42` | `.ufo/evidence/round-89/landing/docstring-vs-code.txt`: 15 docstring check ids = 15 `CHECKS` = 15 emitted; a doctored copy (one emitter renamed) prints `docstring_not_emitted=W_EXTRA`, so the scan can fail. |

SOURCES `status`/`used-by` changes: S313 new (`used-by` corpus/knowledge/kernel-witnessed-ledger.md,
corpus/lessons/round-89.md); S314 new (same); S315 new, `queued` (`used-by`
corpus/lessons/round-89.md). No existing row touched. Rows 172 → 175.

Correction appended for round 88 (closure routed item 5): the S312 quote "Return True if the
binary data starts with the specified prefix, otherwise return False." is **14** words, not 15,
and "raises ValueError when the subsequence sub is not found" is **12**, not 13 (`wc -w`); both
stay under 25. The filed S312 row and `lessons/round-88.md` are not rewritten.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | the round-88 fix for the print-forgery class (QUALITY 135, `executed-set-check.py`) still read the subject's output: it binds `REGRESSION_CASE <leg>: PASS` lines to the declarations, and a forgery that prints those lines while executing nothing passes it | `.ufo/evidence/round-89/landing/m1-r88-check-vs-stub-lines.txt` (`EXECUTED_SET: declared=11 executed_pass=11 … ok`, exit 0) | none — QUALITY 135 asked for the printed names to equal the parsed ones, which a printer satisfies | QUALITY 136: bind to an observer outside the subject (kernel exec/exit record of bytes the counter computed). Shown able to fail: the witness refuses `stub-lines` (W_MAT, W_CONTROL, W_EXEC, W_CONTENT; `landing/measure-ff7a4b06.out`) |
| M2 | instrument development: the prlimit64 parser read `NULL ` (trailing space from an `<unfinished …>`/`resumed>` join) as a SET call, so the honest runner drew 9720 false W_ENV findings | development run `run-real2` (first audit `findings=9785 checks=W_ENV FAIL`; re-audit after the fix `findings=0 … PASS`, `.ufo/evidence/round-89/controls/dev-receipts/real2.reaudit`) | the positive control (the real runner must PASS) — it fired before any freeze | strip each argument after the join; the `W_ENV:rlimit` selftest arm (a real SET outside an interpreter) still fires, `pre-freeze/selftest.out` |
| M3 | instrument development: environment normalization replaced the file under test in EVERY value, so the control's `PRISTINE=` became `<FILE>` while each mutant's did not — 65 false W_ENV findings on six honest legs (10 each on js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, js-claims-check; 15 on bash-checklist-run) | same development run (`W_ENV leg=js-kimi-census … differs from the control's`) | the positive control | normalize only `MUTANT` (must equal the file) and `DEFECT_ID` (must equal the id), and the id elsewhere only as a path token; `W_ENV:diff` arm still fires |
| M4 | instrument development: W_ORDER keyed writes by basename across legs, so two legs whose targets share a basename would refuse each other — observed as 11 cross-leg W_ORDER findings on the `dupbase` forgery's duplicated leg; an honest runner with two same-named targets would have been refused | development audit of `run-dupbase` (11 W_ORDER) vs the re-audit (`W_PATH,W_DUP` only, `dev-receipts/dupbase.reaudit`) | none — `dupbase` was a forgery and failed anyway, so no control would have shown the false refusal | exact absolute paths from `-y` annotations and dirfd-joined relative names; basename only for an unanchored relative path; the `W_ORDER` arm still fires on an exact-path write |
| M5 | expectation miss, recorded before results: `env-steer` was expected to fire W_ENV but fired W_EXEC — `BASH_ENV` makes `bash -c` exit before any interpreter exec, so the environment check never sees a mutant exec | `.ufo/evidence/round-89/controls/expected.tsv` (appended note) | the expectations file, written before results were read | none needed for the predicate (rc/verdict bind, not check ids); the lesson: a steering forgery that also kills the wrapper is caught upstream by W_EXEC, so W_ENV's own coverage comes from `rlimit-steer` and `fake-interp`, not from `env-steer` |
| M6 | **the kill.** W_ORDER and W_CONTENT bind "the bytes that ran" to "the bytes audited" by path SPELLING: a hard link to a decoy inode, a case directory swapped by `mv` after the execs, or a symlink at the audited path lets a runner exec a one-line stub at every audited path and install the spec-exact bytes afterwards through another name; the witness prints `legs=11 witnessed=11 findings=0 … PASS` with no gate suite run | `.ufo/waves/round-89/w1/T89E2.md` (`accepted:hardlink,dirswap,symlink`); reproduced by the L1 on the committed runners, `.ufo/evidence/round-89/landing/t89e2-reproduced-by-l1.txt`; same root in T89R1 K1 and T89C2 D3 (fixture C12/C13) | none — the freeze modelled writes through the audited name (late-write, the fd and link probes) and declared MAP_SHARED (L2), not aliasing; M4's own fix (basename → exact path) is what let `dirswap` through, since the moved directory keeps the basename | QUALITY 137 (object identity: (dev, inode) of file and directory at exec, or hash at exec). Not built this round — the frozen witness is not repaired after data. Able to fail: the three T89E2 runners are committed controls the round-90 successor must refuse |
| M7 | the counter certified an INSTRUMENT but had no counterfeit-instrument control: a 53-line file that runs nothing and answers by control NAME reaches `C1_R89_PASS=true`; the selftest conjunct accepts any `n/n` (`0/0` passes); `legs=11` is a literal in the counter's format string; control names (`honest-*`, `stub-lines.sh`) and selftest fixture paths (`<tmp>/W_DUP/…`) disclose the class | `.ufo/waves/round-89/w1/T89C1.md` objections 1, 3, 6, 7; `T89C1-measure.out`, `T89C1-measure-selftest00.out` | the §9 rule ("build the cheapest control that skips the claimed work") — read by the lane as "the tool is absent at the base", which skips the artifact, not the work | QUALITY 138. Able to fail: `T89C1-counterfeit-witness.py` is committed and passes the round-89 counter today; a successor counter must fail it |
| M8 | QUALITY 134 analog missed: `controls/expected.tsv` (the pre-result expectations) first-adds in the SAME commit `a65e11c0` as the verdict-carrying `dev-receipts/*`, so git cannot order the expectations before the results; only the writing order (and the appended M5 note) can | `.ufo/waves/round-89/w1/T89R2.md` item 4 | QUALITY 134 and its checker `.ufo/evidence/round-88/mistakes/prereg-order.sh` — applicable, not run before the commit | commit expectation files alone, before any receipt; the expectations earn no git-ordered priority this round (disclosed, not re-dated) |
| M9 | round-88 routed item 6 (R-3 M6/M8/M9 successors; R-4 unbacked LOG quotes and unregistered retained instruments) was neither addressed nor stated as carried in the round-89 freeze or landing | `T89R2.md` NONCONFORMANT-2 | the closure's routed list, read but not mirrored into the plan | stated as carried in `## Routed to round 90` below; `tools/ledger-witness.py` is a new retained instrument not yet in `tools/registry.json` (adds to R-4) |
| M10 | per-check isolation (round-88 M8) was met per check id, not per sub-condition: the witness's selftest kills the mandatory weakening of 14/15 checks, but W_CONTROL's exit branch and W_ENV's deny-list branch survive (no arm reaches them; the battery's `env-steer` is refused upstream by W_EXEC) | `.ufo/waves/round-89/w1/T89M1.md` (`15/23-killed`; survivors D09, D16 and six more) | none | one arm per branch, not per check id; routed |

Wave-found classes inside the declared limits (recorded, not kills): T89E4 — a runner that runs
each recorded-KILLED defect with `umask 0777` and fd 1/2 on `/dev/full` is accepted on the real
ledger (`T89E4-h1b-umask-witness.out`, PASS) and manufactures an accepted false KILLED row on a
fixture (`T89E4-h1d-fixture-witness.out`); a per-defect variable naming a planted sandbox file
is accepted (H2) — both L3 ("process state or file
content the trace does not carry"); T89C1 objection 4 — an `mmap(MAP_SHARED)` twin of
`late-write` is L2 by declaration but is a trace-set gap (`mmap` is not traced), not a model
boundary; T89R1 K1 part 2 — `io_uring` writes bypass the traced write family. T89E3's two honest
variants were accepted (`accepted-all`), so kill rule (c) did not fire.

M2–M4's "before" counts (9720, 65, 11) come from development audits whose outputs were left in
scratch and reaped; they are unbacked by any committed receipt and are stated as narrative only
(the round-87 M3 / R-4 class, repeated). The committed `dev-receipts/*.reaudit` files are the
after-fix audits of the same traces, and the fixes' arms are in `pre-freeze/selftest.out`.

## Verdict — R89-C1 (operability, capability acquisition)

The frozen counter prints `C1_R89_PASS=true` at the landing `ff7a4b06`
(`.ufo/evidence/round-89/landing/measure-ff7a4b06.out`; independently T89E1 `conjuncts-met` at
the freeze), so kill rule (a) does not fire. **Kill rule (b) fires**: three committed wave
runners that perform none of the ledger's work are accepted, and none works through L1–L4 (M6).
R89-C1 is killed by its own pre-registered rule. The counter's own weaknesses (M7) would make
the claim unprovable even without (b). Nothing is narrowed after data: the predicate, counter,
limits and witness bytes stay as frozen. The capability row stays in `SCORECARD.md` annotated
**not admitted**. Lane reading: honest stop, no axis harmed (the runner is unchanged; standing
sweeps `landing/selfstate-ff7a4b06.txt`, `pins-ff7a4b06.txt`, `registry-figure.txt`,
`pointer-recheck.txt` all exit 0; cold-read precheck `credited=24/72` at base and landing).

## Routed to round 90 (status-neutral)

1. Successor witness keyed on object identity (QUALITY 137): record (dev, inode) of each audited
   file and its case directory at the exec, refuse aliased writes and identity changes; trace
   `mmap`/`mprotect` and refuse `io_uring_setup`; T89E2's `hardlink`/`dirswap`/`symlink` and both
   probes as committed controls.
2. Successor counter (QUALITY 138): derive every conjunct from the witness's output and an
   independent expectation; compare the selftest to the committed arm list; randomize control
   file names and fixture dirs; `T89C1-counterfeit-witness.py` as the counterfeit-instrument
   control that must fail before the freeze.
3. Per-branch selftest arms (M10); expectations committed alone first (M8).
4. L3 is now measured, not hypothetical (T89E4 `umask`, planted sandbox files): either narrow the
   claim's sentence to "the declared leg set ran on its pinned bytes with the declared argv and
   environment and these kernel exits", or design an unpredictable sandbox.
5. Carried from round 88 item 6: R-3 (M6/M8/M9 successors) and R-4 (16 unbacked LOG counter
   quotes, 2 in round-86's lesson; retained instruments unregistered — now including
   `tools/ledger-witness.py`).

## Learning trends (lane's reading; the closure decides)

- expansion: improved — a new knowledge entry on ground the lane did not hold (kernel-observed
  verification of a runner's work, `corpus/knowledge/kernel-witnessed-ledger.md`, citing the
  mined S313/S314) and a queued frontier row (S315).
- quality: unchanged — no held entry re-verified or superseded.
- discernment: improved — the wave killed the claim, and the kill and four other mistakes are
  mined with criteria 136–138, each tied to a committed control that shows the failure.

## Round-90 corrections (append-only)

The text above is not rewritten; these corrections answer the round-89 closure's
routed items 2 and 3 (`round-89-verifier-spotcheck.md` §6).

1. `## Trend` says "the kill and four other mistakes". The `## Mistakes` table holds
   M1-M10: the kill (M6) and nine others. Corrected reading: the kill and nine other mistakes
   became lessons; QUALITY 136-138 are the grounded criteria among them.
2. The `## Gate` row rejecting mkcheck2 gives the reason "paywalled". It was not shown to
   be a paywall: at closure the ACM page and its PDF answered HTTP 403 behind a bot
   challenge, and no open manuscript was found. Corrected reason: the paper text was not retrievable at fetch time,
   so no quote could be located. The decision
   (reject) and its flip condition (an open manuscript with a located quote) are unchanged.
