source: S313 execve(2), Linux manual page, man-pages 6.19 — https://man7.org/linux/man-pages/man2/execve.2.html — NOTES, "many attributes of the calling process remain unchanged (in particular, its PID)" and DESCRIPTION, "By default, file descriptors remain open across an execve()." (snapshot `.ufo/evidence/round-89/sources/s313-execve.2.html:463-464,254`; headers `s313.headers`; registry `corpus/SOURCES.md:189`); S314 strace(1), Linux manual page — https://man7.org/linux/man-pages/man1/strace.1.html — OPTIONS `-y`/`--decode-fds` "Prints paths associated with file descriptor arguments and with the AT_FDCWD constant." and `-v`/`--no-abbrev` "Prints unabbreviated versions of environment, stat, termios, etc. calls." (snapshot `.ufo/evidence/round-89/sources/strace.1.html:933,865`; headers `strace.headers`; registry `corpus/SOURCES.md:190`); own work — `tools/ledger-witness.py`, sha256 `0839f5875a7a3baf694d993316a2cca6b38b449561a76e0bf54dd1988ebf8d37` (`.ufo/evidence/round-89/pre-freeze/measure-a65e11c0.out:3`, committed at `a65e11c0`), against the frozen predicate, kill rule and declared limits in `plans/round-89.plan.md:24-103` (freeze `8876cca5`).
verified-at: 2026-11-06 — instrument and counter at `a65e11c0` (`pre-freeze/selftest.out`, `pre-freeze/measure-a65e11c0.out`, committed in `48383295`); the pre-freeze counter measured every conjunct except the SCORECARD row (`capability_row=0`, `pre-freeze/measure-a65e11c0.out:34`). The capability row is present at `ff7a4b06` (`SCORECARD.md:272`), but no landing counter output is among the committed receipts (`.ufo/evidence/round-89/landing/` holds the standing no-harm sweeps only), so this entry records the mechanism and its control evidence and does not print `C1_R89_PASS=true`.
recheck: `python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/ledger-witness.py --selftest | tail -1` → `LEDGER_WITNESS_SELFTEST: 21/21 pass`, exit 0; then `bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-89/measure.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin <REV> /home/vgpnk/Projects/shokunin <empty dir>` → `C1_R89 … honest_accepted=2/2 forgeries_refused=12/12 capability_row=1 C1_R89_PASS=true` (the landed reading; §7 records that this output is not yet among the committed receipts).

# Kernel-witnessed ledger audit — a printed figure is not evidence (round 89, R89-C1)

A counter that reads what the subject *prints* can be passed by a runner that
prints the figure without doing the work. Round 89 added the lane's first
instrument that does not read the figure at all: it runs the mutation ledger
under `strace(1)` and binds each declared leg to the kernel's own record of the
execs, the file bytes, the write syscalls and the exit statuses behind it.

Abbreviations used below: a bare `pre-freeze/…` or `controls/…` path is under
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-89/`; a bare
`ledger-witness.py:NN` is the pinned, frozen tool at `tools/ledger-witness.py`
(sha256 `0839f587…8ebf8d37`).

## 0. The problem — counters that read a printed figure (rounds 85–88)

The lane's three rejected closures share one root, stated in the round-89 plan's
fresh-start reads (`plans/round-89.plan.md:11-16`): each round froze a counter
whose predicate read a figure the subject PRINTS — "an 8/8 tally, a census
count, `REGRESSION: PASS (cases=11 …)`" — and the wave then built a counterfeit
that printed that figure without the work. Round 86 shipped `att3b-cheat`,
round 87 `cf-c`/`cf-oid`, round 88 `parked`/`stub`/`dupbase`
(`plans/round-89.plan.md:14`). In each round the frozen counter read exactly the
figure the counterfeit printed (`plans/round-89.plan.md:12-14`), so the counter
could not separate the work from its announcement.

Two consequences follow, and they are the design constraints of the witness:

1. **The subject's stdout cannot be evidence of work.** It can only be a cheap
   consistency gate — the witness keeps exactly one such check (`W_RUN`) and it
   cannot carry a leg by itself.
2. **Distinctness must be keyed on object identity, not spelling.** Round 88's
   `dupbase` exists because a second leg could name the same blob under a
   respelled path (`kagi-shokunin/./corpus/surface-census.sh`,
   `controls/dev-receipts/dupbase.reaudit:2`) and pass a per-path check.

The witness's own problem statement names the class: before round 89 the lane
"had no instrument that could tell a runner that did the ledger's work from one
that printed its figure (rounds 85–88; QUALITY 135)" (`plans/round-89.plan.md:38-39`).

## 1. What the witness does

`--run` (`ledger-witness.py:682-726`):

- Shadows the runner into `<scratch>/fleet/tameshi-shokunin/tools/mutate-and-run.sh`
  and symlinks each repo the declared legs name into that shadow fleet root, so the
  runner reads the real repositories while its `--workdir` and its own bytes live in
  scratch (`ledger-witness.py:695-712`).
- Starts it from a **clean declared environment** — exactly `PATH`, `HOME`,
  `LC_ALL=C.UTF-8`, `TMPDIR=<scratch>/tmp` (`ledger-witness.py:715-716`) — so any
  steering variable an audited exec carries was introduced by the runner itself
  (that is what `W_ENV` then reports).
- Traces `bash <shadow> --regression --workdir <scratch>/wd` with
  `strace -f -q -y -v -s 4096 -e signal=none -e trace=execve,execveat,openat,…,prlimit64`
  (`ledger-witness.py:89-94`), one output file, stdout+stderr to
  `<scratch>/runner.out`.
- Audits the same way `--audit` does: runner bytes + trace + kept workdir +
  stdout + exit code in, findings out. `--selftest` drives one fixture arm per
  check through that same public `--audit` path (`ledger-witness.py:885-916`), so
  the checks are exercised as an observer, not as a privileged branch.

Verdict line: `LEDGER_WITNESS: legs=<n> witnessed=<m> findings=<k> checks=<ids|-> PASS|FAIL`;
exit 0 PASS, 1 FAIL, 2 setup. FAIL is `findings != 0` **or**
`witnessed != legs` (`ledger-witness.py:636-648`) — note that a run can reach
`witnessed=11` and still fail on global findings (`rlimit-steer`, below).

## 2. The fifteen checks — what each binds

Each row cites the docstring clause (`ledger-witness.py:11-46`) and the code path
that enforces it.

| check | binds | how |
|---|---|---|
| `W_PARSE` | the declaration itself | runner bytes must declare ≥1 leg in the `regression_case_git` call shape; every `PIN_`/`REV_`/`TABLE_` variable and embedded spec a leg names must resolve (`:116-183`, problems raised at `:412-414`) |
| `W_TABLE` | the recorded verdict vocabulary | every table value ∈ {KILLED, SURVIVED}; a bad value excludes that defect from the verdict comparison rather than being compared as text (`:449-452`) |
| `W_PATH` | path spelling as a distinctness hazard | fleet-relative; first component a directory name; no `''`, `.`, `..` component (`path_ok`, `:383-390`) |
| `W_DUP` | leg identity | leg names, `(repo, path)` pairs and blob sha256 pins pairwise distinct — content-addressed, so respelling a path does not create a leg (`:434-441`) |
| `W_PIN` | the pin against git, not against the file on disk | the witness's own `git -C <repo> cat-file blob REV:PATH` (`git_blob`, `:365-381`), after requiring the repo to be its own toplevel, must sha256 to the declared `PIN_` (`:459-466`) |
| `W_SPEC` | the defect set | the witness applies each defect to the pinned blob itself: every `@old` occurs exactly once; spec ids equal table ids (`:467-487`) |
| `W_RUN` | stdout, as a consistency gate only | exit 0; one `REGRESSION_CASE <leg>: PASS` per declared leg and no non-PASS case line; `REGRESSION: PASS (cases=N passed=N` with N = leg count (`:421-432`) |
| `W_MAT` | the materialization step | the trace contains a successful `git … show REV:PATH` execve per leg — the runner actually asked git for the pinned bytes (`:489-493`) |
| `W_CONTROL` | the pristine run | pristine copy exec'd **by the leg's interpreter** under the same `interp_match` identity, kernel exit 0, and file bytes equal to the pinned blob (`:598-607`) |
| `W_EXEC` | per-defect execution | the mutant path is the interpreter's **script argument** (`node|bash|python3 [-I] "$MUTANT" …`), not merely somewhere in argv — so `argv-steer` cannot satisfy it; the exec'd file must also be the interpreter the witness's own `PATH` resolves, and `argv[1:]` must equal the suite's exact `[flag] target tail` (`interp_match`, `:392-404`; `:27-28`, `:505-519`) |
| `W_CONTENT` | the bytes that were executed | each mutant file left in the workdir sha256-equals the digest the witness computed from `blob.replace(old, new, 1)` (`:612-616`) |
| `W_ORDER` | the file after its exec | no write-class syscall touches that path after its first interpreter exec: write-opens, `write`/`pwrite`/`ftruncate`… on an `-y`-decoded fd, and `rename`/`link`/`symlink`/`truncate` naming it (`:31-34`, `:307-333`, `:573-590`) |
| `W_VERDICT` | the verdict | the mutant exec's **own pid** exit, as the kernel reported it: 0 → SURVIVED; n ∉ {0,124,126,127} → KILLED; 124/126/127 or a signal → INCONCLUSIVE; must equal the recorded table value (`:35-37`, `:617-630`) |
| `W_EXTRA` | the unaccounted work | no interpreter exec of a `mutant-*.target.*` / `pristine.target.*` path under the workdir that no declared leg accounts for (`:38-39`, `:520-524`) |
| `W_ENV` | the process climate around the exec | no `NODE_OPTIONS`, `NODE_PATH`, `BASH_ENV`, `ENV`, `SHELLOPTS`, `BASHOPTS`, `PYTHONSTARTUP`, `PYTHONPATH`, `PYTHONHOME`, `PYTHONINSPECT`, `LD_PRELOAD`, `LD_AUDIT`, `LD_LIBRARY_PATH`, `PROMPT_COMMAND` or `BASH_FUNC_*` on an audited exec; each mutant exec's environment equals its leg's control environment after normalizing `MUTANT`, `DEFECT_ID` and the sandbox id token; and no rlimit is set except by an audited interpreter after its own exec (`:40-45`, `:526-565`) |

Three shapes are worth naming because they are what the counterfeits attack:

- **`W_VERDICT` reads a pid, not a table.** The witness groups trace events by
  pid, takes the first interpreter exec of a given expected path, and then the
  first exit of *that* pid after it (`exit_after`, `:567-571`). `liar-flip` — a
  runner that runs the real work and then writes the opposite table — is caught
  with a single finding: `W_VERDICT leg=py-kake-ledger-guard defect S_RED_FILES
  observed SURVIVED recorded KILLED` (`controls/dev-receipts/liar-flip.reaudit:1`).
- **`W_ORDER` needs fds, not just paths.** A mutant that is exec'd and then
  rewritten through a descriptor opened before the exec would pass a
  path-only check; this is exactly the case S313 line 254 says the kernel
  permits.
- **`W_ENV` compares environments, not just denylists.** `env-steer` is not
  caught by its denylist hit alone: `BASH_ENV` makes the suite's `bash -c` exit
  before any interpreter exec, so the run collapses to
  `witnessed=0 findings=115 checks=W_EXEC` (`controls/expected.tsv:20-22`).

## 3. Why `strace -f -y -v`

- `-f` follows forks (`strace.1.html:327-331`), and the ledger's work is a tree:
  `bash` runner → `git show` → `bash -c` → interpreter → mutants. Without it the
  execs that matter are never in the file.
- `-y` decodes each fd argument to its path (`strace.1.html:933`). This is load
  bearing twice over: `W_ORDER` matches writes on fd-decoded paths (a write to a
  mutant can arrive through a descriptor opened before it, S313 line 254), and
  relative opens anchor on the decoded dirfd (`anchored_paths`,
  `ledger-witness.py:336-352`).
- `-v` prints environments unabbreviated (`strace.1.html:865`), which is what
  makes "each mutant exec's environment equals its control's" a comparison the
  observer can actually perform.
- The PID semantics come from S313 line 463-464: an exec does not create a
  process, so `env -i … node "$MUTANT"` exits under the pid that called exec, and
  the recorded exit status is the interpreter's — the verdict.
- `-s 4096` and `-e signal=none` are reader bounds: long argv/env strings must
  not be elided mid-token, and signal lines are noise for this audit
  (`ledger-witness.py:89-94`).

`W_RUN` is the one check that reads stdout, and it is deliberately redundant:
`stub-lines` satisfies it (it prints the case lines and the summary) and still
fails `W_MAT,W_CONTROL,W_EXEC,W_CONTENT`; `stub` fails `W_RUN` as well
(`pre-freeze/measure-a65e11c0.out:32-33`).

## 4. Evidence (pre-freeze, instrument `0839f587…8ebf8d37`)

### 4.1 Per-check isolation — 21/21

`--selftest` runs 21 arms: a base arm that must pass, one arm per check (15), four
sub-arms (`W_EXEC:argv`, `W_EXEC:interp`, `W_ENV:diff`, `W_ENV:rlimit`) and a
setup arm that must return 2. Every arm fired exactly its own check
(`pre-freeze/selftest.out:1-23`), ending `LEDGER_WITNESS_SELFTEST: 21/21 pass`
exit 0 (`pre-freeze/selftest.out:22-23`); the counter records `selftest=21/21`
(`pre-freeze/measure-a65e11c0.out:34`).

This is the round-88 M8 lesson applied: a check that has never fired on a fixture
built to trip it is indistinguishable from dead code.

### 4.2 The no-work control

At the base revision the counter is a do-nothing: the tool does not exist, so the
counter prints `witness=absent … C1_R89_PASS=false`, exit 1, and the direct
`git cat-file -e 61990f3d:tools/ledger-witness.py` says
`path 'tools/ledger-witness.py' exists on disk, but not in '61990f3d'`, exit 128
(`pre-freeze/nowork-base.out:2-7`).

### 4.3 Positive controls — the real runner and two honest variants

Full counter at `a65e11c0` (nonce `910c82e4867e0013`, `pre-freeze/measure-a65e11c0.out:4`;
window start `2026-11-06T20:17:35Z`, end `2026-11-06T20:34:42Z`, `:2,36`; the real runner,
the 12 forgeries and the 2 honest variants all go through one `xargs -P 7`
(`../measure.sh:45-48`)):

- the runner at REV: `rc=0 LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS`
  (`pre-freeze/measure-a65e11c0.out:19`), the same 11 legs and verdict as the
  offline re-audit (`controls/dev-receipts/real2.reaudit:1-12`) —
  `js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`,
  `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`, `js-round-gate`,
  `js-sources-check`, `js-cite-check`, `bash-drift-pins`, `py-kake-ledger-guard`;
- `honest-reorder` and `honest-rename`: each `rc=0`, same PASS line
  (`pre-freeze/measure-a65e11c0.out:25-26`), counted as `honest_accepted=2/2`
  (`:34`). Both were appended to `controls/expected.tsv:17-19` only after the
  development runs had been read and **before** any honest variant ran — the
  header states the ordering (`controls/expected.tsv:17`).

The honest pair is the anti-degenerate control: a witness that refuses everything,
or one that recognizes only the runner's exact bytes, fails here.

### 4.4 The forgery battery — 12/12 refused

Nine runners from `controls/make-forgeries.py` plus the round-88 trio from
`.ufo/waves/round-88/w1/T88E2-make-variants.py` (`plans/round-89.plan.md:72-76`).
Every counterfeit **exits 0**; every one is refused with exit 1 and a line ending
` FAIL` (all figures `controls/dev-receipts/observed.tsv:2-13`, matching
`pre-freeze/measure-a65e11c0.out:20-33`; `forgeries_refused=12/12` at `:34`):

| forgery | what it forges | runner rc | witness rc | findings | checks fired | witnessed |
|---|---|---|---|---|---|---|
| `stub-lines` | prints the case lines, never runs git | 0 | 1 | 263 | W_MAT, W_CONTROL, W_EXEC, W_CONTENT | 0 |
| `stub` | prints case + summary, does nothing | 0 | 1 | 264 | W_RUN, W_MAT, W_CONTROL, W_EXEC, W_CONTENT | 0 |
| `lazy` | runs the pristine copy in place of every mutant | 0 | 1 | 115 | W_EXEC | 0 |
| `copy-sweep` | copies mutants, runs the pristine each time | 0 | 1 | 177 | W_CONTENT, W_VERDICT | 0 |
| `late-write` | runs mutants, rewrites them after the exec | 0 | 1 | 177 | W_ORDER, W_VERDICT | 0 |
| `liar-flip` | real work, one recorded verdict flipped (kake `S_RED_FILES`), leg prints PASS | 0 | 1 | 1 | W_VERDICT | 10 |
| `env-steer` | `BASH_ENV` steers the suite | 0 | 1 | 115 | W_EXEC | 0 |
| `rlimit-steer` | sets an rlimit around the suite | 0 | 1 | 115 | W_ENV | 11 |
| `argv-steer` | mutant in argv, not as the script argument | 0 | 1 | 115 | W_EXEC | 0 |
| `fake-interp` | execs a shim, not the leg's interpreter | 0 | 1 | 123 | W_EXEC, W_VERDICT, W_ENV | 3 |
| `parked` | round-88 parked variant | 0 | 1 | 24 | W_RUN, W_MAT, W_CONTROL, W_EXEC, W_CONTENT | 10 |
| `dupbase` | round-88 respelled duplicate leg | 0 | 1 | 2 | W_PATH, W_DUP | 10 |

Two readings matter. `rlimit-steer` shows the `witnessed` count is not the
verdict: all 11 legs are witnessed, yet the run FAILs on global `W_ENV` findings
(`observed.tsv:12`). `dupbase` shows why identity is content-keyed: its only two
findings are the duplicate pin and the `./` path (`controls/dev-receipts/dupbase.reaudit:1-2`).

### 4.5 Observed check sets vs the pre-registered expectations

`controls/expected.tsv` was written before any forgery result was read
(`controls/expected.tsv:1-2`). The frozen predicate binds exit code + verdict
label, and the check-set column is marked informative (`controls/expected.tsv:2`).
Comparing it anyway, every row matches verbatim except two: one superset
(`fake-interp`: expected `W_EXEC`, observed `W_EXEC,W_VERDICT,W_ENV`,
`observed.tsv:4`) and one substitution (`env-steer`: expected `W_ENV`, observed
`W_EXEC`, `observed.tsv:2`). The
substitution has a recorded cause: `BASH_ENV` makes the suite's `bash -c` exit
before the interpreter exec, so no mutant is ever exec'd and `W_EXEC` fires
first (`controls/expected.tsv:20-22`). Under the frozen predicate both still
count as refusals; the check-set deviation is bookkeeping for a future
counter, not an acceptance.

## 5. Declared limits (L1–L4, stated before the data)

From `plans/round-89.plan.md:95-103`, reproduced because a witness without its
limits is an overreach:

- **L1** a process that edits the trace file, the kept workdir after the run, or
  the witness itself (same uid).
- **L2** a `MAP_SHARED` write mapping of a mutant — the write never becomes a
  traced write syscall on a path.
- **L3** per-defect steering through process state or file content the trace does
  not carry: the working directory, the inherited fd table (e.g. a closed
  stdout), signal dispositions, an rlimit inherited from before the runner
  started, or files a runner plants in a per-defect directory the environment
  names (a sandbox `HOME`/`TMPDIR`).
- **L4** a runner that does all the real work — that is not a counterfeit.

Plus the grammar limit: legs are parsed only in the runner's
`regression_case_git` call shape; another declaration shape is outside the
witness's grammar and fails `W_PARSE` (`plans/round-89.plan.md:101-103`).

The limits are not hypothetical corners: L3's sandbox-`HOME` clause is the exact
affordance the `py-kake-ledger-guard` suite uses (`h="$WORKDIR/sandbox-$DEFECT_ID"`,
`tools/mutate-and-run.sh:1591` at `28ec588`; see
`corpus/knowledge/mutation-case-kake-ledger-guard.md` §2). A fixture planted
inside that sandbox is steering the witness does not see.

## 6. Reproduce

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r89/<seat>
S=$(mktemp -d -p /fast/scratch/hyaku/tameshi-r89/<seat> w.XXXXXX)
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/ledger-witness.py \
  --run \
  --runner /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  --fleet /home/vgpnk/Projects/shokunin \
  --scratch "$S"
```

Last line, PASS (per-run wall time is not recorded in the receipts; the whole
pre-freeze counter's window is `pre-freeze/measure-a65e11c0.out:2,36`):

```
LEDGER_WITNESS: legs=11 witnessed=11 findings=0 checks=- PASS
```

Offline re-audit of a kept run (the path the selftest arms use):

```sh
python3 -I tools/ledger-witness.py --audit --runner R --fleet "$S/fleet" \
  --trace "$S/trace.txt" --workdir "$S/wd" --stdout "$S/runner.out" --rc N
```

Whole counter (the real runner, the 12 forgeries and the 2 honest variants, one
`xargs -P 7`; `../measure.sh:45-48`):
`bash .ufo/evidence/round-89/measure.sh <lane> <REV> /home/vgpnk/Projects/shokunin <empty dir>`.

## 7. What this entry does not claim

- It does not claim the counter passed at the landing commit. At the pre-freeze
  commit every conjunct is measured except the SCORECARD row:
  `selftest=21/21 real=PASS(legs=11) honest_accepted=2/2 forgeries_refused=12/12
  capability_row=0 C1_R89_PASS=false` (`pre-freeze/measure-a65e11c0.out:34`).
  The capability row exists at `ff7a4b06` (`SCORECARD.md:272`), but the landing
  counter output is not among the committed receipts this draft read:
  `.ufo/evidence/round-89/landing/` contains `docstring-vs-code.txt`,
  `pins-ff7a4b06.txt`, `pointer-recheck.txt`, `registry-figure.txt` and
  `selfstate-ff7a4b06.txt` — the standing no-harm sweeps, not a `measure.sh`
  run. `C1_R89_PASS=true` therefore appears in this entry only as the predicate
  it would have to satisfy, never as a measured value.
- It does not claim completeness against future forgeries. The kill rule's clause
  (b) makes every committed counterfeit a live control: a wave-built variant that
  does not do the ledger's work for at least one declared leg, and is accepted,
  kills the claim (`plans/round-89.plan.md:86-93`).
- It does not claim the witness replaces behavioural review of the *suites*. It
  audits whether the ledger's declared work happened on the declared bytes; what
  those bytes assert is the mutation-case entries' business.

Drafted by wave seat T89SC1 (scribe) from committed receipts at `a65e11c0`. The
L1 has since landed a shorter entry at the path S313/S314 name
(`corpus/knowledge/kernel-witnessed-ledger.md`, `ff7a4b06`, 72 lines); this draft
is a candidate expansion for that file — per-check mechanism, receipt line
numbers, the observed-vs-pre-registered check sets and a reproduce section — not
a competing claim. No measurement was re-run for this draft.
