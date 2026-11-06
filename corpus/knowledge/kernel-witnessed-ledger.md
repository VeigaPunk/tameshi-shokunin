source: S313 execve(2) (docs, tier A, mined) — https://man7.org/linux/man-pages/man2/execve.2.html, NOTES (`.ufo/evidence/round-89/sources/s313-execve.2.html:463-464`: "many attributes of the calling process remain unchanged (in particular, its PID)") and DESCRIPTION (`:254`: "By default, file descriptors remain open across an execve()."); S314 strace(1) (docs, tier A, mined) — https://man7.org/linux/man-pages/man1/strace.1.html, §Output format `-y` (`.ufo/evidence/round-89/sources/strace.1.html:933`: "Prints paths associated with file descriptor arguments and with the AT_FDCWD constant.") and `-v` (`:865`: "Prints unabbreviated versions of environment, stat, termios, etc. calls."); the ledger's own runner `tools/mutate-and-run.sh` @ `61990f3d` (read, not changed)
verified-at: 2026-11-06; instrument committed `a65e11c0` (pre-freeze); full counter at `a65e11c0` 2026-11-06T20:34:42Z (`.ufo/evidence/round-89/pre-freeze/measure-a65e11c0.out`); freeze `8876cca5` (`plans/round-89.plan.md`)
recheck: `python3 -I tools/ledger-witness.py --selftest` → `LEDGER_WITNESS_SELFTEST: 21/21 pass`; `bash .ufo/evidence/round-89/measure.sh <lane> <REV> /home/vgpnk/Projects/shokunin <empty dir>` → `C1_R89 … C1_R89_PASS=true` at the landing commit (receipt named in `SCORECARD.md` Round 89)

# Kernel-witnessed ledger audit (round 89, R89-C1)

## 1. The problem this answers

Rounds 85–88 each froze a counter whose predicate read a figure the certified subject
PRINTS — an 8/8 tally (r86), a census (r87), the runner's own `REGRESSION: PASS
(cases=11 passed=11 …)` (r88) — and each time the wave built a counterfeit that printed the
figure without the work: r86 `att3b-cheat`, r87 `cf-c`/`cf-oid`, r88 `parked`, `stub` and
`dupbase` (`corpus/lessons/round-88-verifier-spotcheck.md` §2.3). QUALITY 135 names the class:
a printed figure must be bound to what the subject executed. A counter that only parses more
of the subject's output does not close it: round 88's `executed-set-check.py` bound the
per-leg `REGRESSION_CASE … PASS` lines to the declared names, and the round-89 `stub-lines`
forgery prints exactly those lines while executing nothing
(`.ufo/evidence/round-89/pre-freeze/measure-a65e11c0.out`, `C1_R89_FORGERY stub-lines`).

## 2. The design

`tools/ledger-witness.py --run` copies the runner under test into a shadow fleet (sibling
repos symlinked, so the runner's `FLEET_ROOT` resolves to the real object stores), starts it
from a clean declared environment (PATH, HOME, LC_ALL, TMPDIR) under
`strace -f -q -y -v -s 4096` with an explicit syscall list (exec, open/creat, rename/link/
symlink/truncate, the write family, setrlimit/prlimit64), and audits the trace, the kept
workdir and the runner's output. The witness never trusts a figure the runner prints for
anything but W_RUN; every other check is computed by the witness from git objects and the
kernel's record:

| Check | Binds |
|---|---|
| W_PARSE, W_TABLE, W_PATH, W_DUP | the declared ledger itself: legs in the `regression_case_git` shape, every variable/spec resolvable, table values in {KILLED, SURVIVED} (r88 M7), paths free of `''`/`.`/`..` components (r88 dupbase, fleet-root latent), names, `(repo, path)` and blob pins pairwise distinct (QUALITY 135) |
| W_PIN, W_SPEC | the witness's own `git cat-file blob REV:PATH` equals the PIN; its own spec parser applies each defect exactly once; spec ids = table ids |
| W_RUN | the printed figure (exit 0, one PASS line per declared leg, the summary) — necessary, never sufficient |
| W_MAT | a successful `git … show REV:PATH` exec per leg |
| W_CONTROL | the pristine copy exec'd by the leg's interpreter, exit 0, bytes = the pinned blob |
| W_EXEC | every mutant exec'd by the interpreter the witness's PATH resolves (same file by realpath), with the suite's exact argv tail |
| W_CONTENT | every mutant file's sha256 = the witness's own spec-applied blob |
| W_ORDER | no write-class syscall on that exact file (absolute, `-y`-decoded) after its first exec |
| W_VERDICT | the kernel exit of that exec's pid (S313: the pid survives `exec env … node`) = the recorded verdict |
| W_EXTRA | no interpreter exec of an undeclared mutant/pristine path under the workdir |
| W_ENV | no steering variable (NODE_OPTIONS, BASH_ENV, LD_PRELOAD, BASH_FUNC_*, …); each mutant's exec environment (S314 `-v`) equals the control's after MUTANT/DEFECT_ID and the sandbox id token are normalized; no rlimit set outside an audited interpreter |

## 3. Evidence

- Selftest: one fixture arm per check through the public `--audit` CLI, each firing exactly its
  own check (round-88 M8), plus base, four sub-arms and a setup arm: `21/21`
  (`.ufo/evidence/round-89/pre-freeze/selftest.out`).
- Full counter at the pre-freeze commit `a65e11c0` (`pre-freeze/measure-a65e11c0.out`): the
  real runner `legs=11 witnessed=11 findings=0 … PASS`; both honest variants (`honest-reorder`,
  `honest-rename`, each with a fresh nonce line) PASS; all 12 forgeries exit 1 with FAIL —
  stub-lines (W_MAT, W_CONTROL, W_EXEC, W_CONTENT), lazy (W_EXEC), copy-sweep (W_CONTENT,
  W_VERDICT), late-write (W_ORDER, W_VERDICT), liar-flip (W_VERDICT, one finding), env-steer
  (W_EXEC: `BASH_ENV` ends `bash -c` before any interpreter exec), rlimit-steer (W_ENV only;
  every verdict still matched), argv-steer (W_EXEC), fake-interp (W_EXEC, W_VERDICT, W_ENV),
  parked and stub (W_RUN, W_MAT, W_CONTROL, W_EXEC, W_CONTENT), dupbase (W_PATH, W_DUP).
- The base `61990f3d` has no witness: `pre-freeze/nowork-base.out` (`witness=absent …
  C1_R89_PASS=false`, exit 1).
- Cost: one traced regression run of the eleven legs takes about 11 minutes wall and leaves a
  1.6 GB trace tree in scratch (development run, round 89); an untraced run takes about 4.5.

## 4. What it does not see (declared before data, `plans/round-89.plan.md`)

L1 a same-uid process that edits the trace, the kept workdir or the witness; L2 a MAP_SHARED
write mapping; L3 per-defect steering through state the trace does not carry — working
directory, inherited fd table, signal dispositions, an rlimit inherited from before the run, or
files planted in a per-defect directory the environment names; L4 a runner that does all the
work. A runner that declares legs outside the `regression_case_git` call shape fails W_PARSE.
L3 is the next frontier: the witness proves that each mutant ran, on its exact bytes, with the
control's argv and environment, and how the kernel says it ended — not that nothing else about
its process was arranged per defect.

## 5. What the round-89 wave proved (the claim was killed; this entry keeps the design)

- **Path spelling is not identity.** Three runners from `.ufo/waves/round-89/w1/T89E2-make-counterfeits.py`
  (`hardlink`, `dirswap`, `symlink`) exec a one-line stub at every audited path and install the
  spec-exact bytes afterwards through another name; the witness prints `legs=11 witnessed=11
  findings=0 … PASS` with no gate run (`T89E2.md`; reproduced in
  `.ufo/evidence/round-89/landing/t89e2-reproduced-by-l1.txt`). W_ORDER and W_CONTENT need
  (dev, inode) of file and directory at the exec, or a hash at the exec (QUALITY 137).
- **A counter over an instrument needs a counterfeit instrument.** `T89C1-counterfeit-witness.py`
  runs nothing, answers by control name, and reaches `C1_R89_PASS=true`; the selftest conjunct
  accepts any `n/n` (QUALITY 138).
- **L3 is real.** `umask 0777` plus stdout on `/dev/full` for recorded-KILLED defects is accepted
  and manufactures a false KILLED row on a fixture (`T89E4.md`). A kernel exit binds the verdict
  to an exec, not to the mutant's behaviour; the honest statement of what the witness proves is
  "the declared legs ran on their pinned bytes, with the declared argv and environment, and
  these are the kernel exits".
- Honest variants from a second author (`T89E3.md`, two runners) were accepted; the trace parser
  survived crafted edge cases except where noted in `T89C2.md` (dirfd-relative `execveat`
  fails closed; aliasing is the M6 class).

## Coverage-map row (appended round 90)

Appended; the entry above is unchanged. Its coverage-map row is
`corpus/README.md` § "Round 90 — coverage-map repair (round-89 closure item 1)":
Frontier, not Core, because R89-C1 was killed by its own rule (round-89 closure
§2.3). The row cites the same mined sources as this entry, S313 and S314.
