# Round 89 — plan and freeze (tameshi, attempt 1)

L1 TameshiR89 holds the canonical planner seat. Base `61990f3d8cd99932bfb0575e1c292e03d310b436`
(round-88 closure spot-check tip). Pre-freeze instrument commit
`a65e11c01a469336b74662d2e3c51ba6f174ac6f`.

## Fresh-start reads (Amendment 46)

Read before declaring: the last three rejected closures and their non-author spot-checks —
round 86 (MANIFEST 1299, `corpus/lessons/round-86-verifier-spotcheck.md`), round 87 (1320,
`round-87-verifier-spotcheck.md`), round 88 (1427, `round-88-verifier-spotcheck.md`). The common
root: each round froze a counter whose predicate read a figure the subject PRINTS (an 8/8 tally,
a census count, `REGRESSION: PASS (cases=11 …)`), and the wave then built a counterfeit that
prints the figure without the work (r86 `att3b-cheat`, r87 `cf-c`/`cf-oid`, r88 `parked`/`stub`/
`dupbase`). Round-88 routed item 1 asks for a counter that binds the executed leg set and keys
targets on blob identity, with `parked`, `stub` and `dupbase` re-run as controls.

## Stagnation nudge

Scored axes depth 10, calibration 8, freshness 9 are at or above the saturation line 8 and no
capability has entered since round 50 (window N = 2), so the lowest-axis obligation is waived
(`SCORECARD.md` §Saturation; re-derived by the round-88 closure §2.4). One claim.

## R89-C1 (operability — capability acquisition): kernel-witnessed ledger audit

**Surface.** A new tool, `tools/ledger-witness.py`, that runs `tools/mutate-and-run.sh
--regression` under strace(1) and binds the runner's declared ledger (parsed from its bytes) to
what the kernel observed — not to what the runner prints. Fifteen checks, W_PARSE … W_ENV,
documented in the tool's docstring: per declared leg the witness itself reads the pinned blob from
git, computes every spec-exact mutant sha256, and requires (a) a `git show REV:PATH` exec, (b) the
pristine copy exec'd by the leg's interpreter with exit 0, (c) every mutant path exec'd by the
interpreter the witness's PATH resolves, with the suite's exact argv, (d) the mutant bytes equal
to the computed sha256, (e) no write-class syscall on that file after its exec, (f) the kernel
exit of that exec equal to the recorded verdict, (g) no steering variable, per-defect
environment difference or runner-set rlimit, (h) legs, `(repo, path)` and blob pins pairwise
distinct, paths free of `''`, `.`, `..` components, and table values in {KILLED, SURVIVED}.

**Why the prior state lacked it.** Before this round the lane had no instrument that could tell
a runner that did the ledger's work from one that printed its figure (rounds 85–88; QUALITY 135
names the class). `tools/ledger-witness.py` does not exist at the base.

**Source.** S313 execve(2) (the PID is unchanged across exec, so an `env … node "$MUTANT"` chain
exits with the interpreter's code; fds stay open across exec, which is why writes are matched on
`-y`-decoded fd paths) and S314 strace(1) `-y`/`-v` (fd paths and unabbreviated environments are
printed). Both opened this round (`.ufo/evidence/round-89/sources/`).

**Counting command (frozen).**

```sh
bash .ufo/evidence/round-89/measure.sh <lane> <REV> /home/vgpnk/Projects/shokunin <empty work dir>
```

It reads every instrument from git objects at REV and prints `C1_R89 rev=… witness=…
selftest=p/n real=…(legs=11) honest_accepted=a/h forgeries_refused=r/n capability_row=0|1
C1_R89_PASS=true|false`, exit 0 iff true.

**Predicate (frozen; the same sentence as the counter's header and its code).** At the measured
lane commit: the witness is present; its `--selftest` passes every arm; the REV runner and both
honest variants each print `LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS` with
exit 0; every one of the 12 forgery runners exits 1 with a line ending ` FAIL`; and the SCORECARD
capabilities table carries a row whose first cell is `ledger witness`. Label in the receipt:
`C1_R89_PASS=true`.

**Before.** `.ufo/evidence/round-89/pre-freeze/nowork-base.out`: at the base the counter prints
`witness=absent … C1_R89_PASS=false`, exit 1 (the do-nothing control).

**Target (one concrete value).** `C1_R89_PASS=true`, exit 0, at the landing commit, with
`selftest=21/21 real=PASS(legs=11) honest_accepted=2/2 forgeries_refused=12/12 capability_row=1`.

**Controls committed before this freeze.**
- No-work: the base (above).
- Forgery battery, 12 runners, each printing the runner's own success figure: nine built by
  `.ufo/evidence/round-89/controls/make-forgeries.py` (stub-lines, lazy, copy-sweep, late-write,
  liar-flip, env-steer, rlimit-steer, argv-steer, fake-interp) and the round-88 trio (parked, stub,
  dupbase) by `.ufo/waves/round-88/w1/T88E2-make-variants.py`. Expectations
  `.ufo/evidence/round-89/controls/expected.tsv` (written before the results were read).
- Positive controls: the REV runner and two honest variants (`honest-reorder`, `honest-rename`),
  so a witness that refuses everything, or recognizes only the known-good bytes, fails. Every
  generated runner carries a fresh random nonce line per measurement.
- Per-check isolation (round-88 M8): `--selftest` runs one fixture arm per check through the
  public `--audit` CLI; each arm must fire exactly its check (21 arms: base, 15 checks, four
  sub-arms, setup). Receipt `pre-freeze/selftest.out` (21/21).
- Full counter at the pre-freeze commit: `pre-freeze/measure-a65e11c0.out` (expected
  `C1_R89_PASS=false` only through `capability_row=0`, every other conjunct measured).

**Kill rule (frozen).** R89-C1 is killed if (a) the counter at the landing commit prints
anything but `C1_R89_PASS=true` exit 0; or (b) any committed runner variant (wave-built included;
its source committed under `.ufo/waves/round-89/`) that does not perform the ledger's real work
— for at least one declared leg, some mutant is not exec'd by the leg's interpreter on its
spec-exact bytes with the declared argv and environment, with a kernel exit equal to the recorded
verdict — is accepted (`LEDGER_WITNESS … PASS`, exit 0) by the landed witness, unless the variant
works only through a declared limit below; or (c) an honest variant (all the real work, ledger
call shape kept) built by the wave is refused for a reason other than a declared limit.

**Declared limits (out of model, stated before data).** L1 a process that edits the trace file,
the kept workdir after the run, or the witness itself (same uid); L2 a MAP_SHARED write mapping of
a mutant; L3 per-defect steering through process state or file content the trace does not
carry — the working directory, the inherited fd table (e.g. a closed stdout), signal
dispositions, an rlimit inherited from before the runner started, or files a runner plants in a
per-defect directory the environment names (a sandbox HOME/TMPDIR); L4 a runner that does all
the real work. The witness also parses ledger legs only in the runner's `regression_case_git`
call shape (a runner that declares legs in another shape is outside the witness's grammar and
fails W_PARSE).

**No-harm.** Nothing in `tools/mutate-and-run.sh` changes. Standing sweeps run at the landing:
runner `--selftest` (108/108), `tools/selfstate-freshness.py` sweep and `--pin-audit`,
`sources-census.sh validate` exit 0.

## Frontier step

- SOURCES: S313 (execve(2), man7, tier A) and S314 (strace(1) `-y`/`-v`, distinct scope from
  S060/S075's input observer). Census before/after in the report.
- Mistake mining into `corpus/lessons/round-89.md` `## Mistakes`.
- considerthese `2026-11-06.md` proposal 5 (docstring↔code scan) applied to the new tool.
- Assimilation: none this round (one claim; the package themes do not serve it).
- Routed round-88 items 2 (M7 table values) and 3 (fleet-root/`./` paths) are W_TABLE and W_PATH;
  item 5 (S312 word counts) is an appended correction.

## Wave

One v1 wave, 12 seats: 4 executor (one carries the bounded probe a labrat would, since the
validator refuses `labrat` — round-88 M2), 1 scout, 1 scribe, 1 connector, 2 reviewer, 2 critic,
1 mutation-tester. Attack seats (reviewer, critic, mutation-tester) 5/12 ≥ 25 %.
