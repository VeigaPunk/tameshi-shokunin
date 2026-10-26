# T50ExecAppendOnly — checker for the carried append-only rule on landed seat reports

Seat: `T50ExecAppendOnly` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
round-50 base `e3729de862f73ae080d98fcf522a7081ce16e40a`, lane HEAD at work
`4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`. Read-only on the lane; the only writes are the
deliverable below and its receipts under `.ufo/waves/round-50/w1/`.

Task: build `seat-report-append-only.py LANE FROM TO` for the carried append-only rule for
landed seat reports, prove it can fail on a fixture, then run it read-only over
`round-43 base..round-44 tip` and `e3729de^..e3729de`. The rule's provenance is
`corpus/lessons/round-48-verifier-spotcheck.md:117` ("an append-only rule for landed seat
reports"), carried into `SCORECARD.md:2410` ("carried items from round 48's list"); the
silent-rewrite class is named at `corpus/lessons/round-48.md:310` and `:312`.

## Deliverable and behaviour

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-50/w1/T50ExecAppendOnly/seat-report-append-only.py`
(7954 bytes, sha256 `cee1a2dddf6ed7a1dcd13cfb2993f491314fa0713b3064d575eed243d8cbce4f`;
`receipts/00-toolchain.txt:5`).

- Enumerates every file under `.ufo/waves/round-*/` present at `FROM` with
  `git ls-tree -r -z --full-tree FROM -- .ufo/waves` and filters
  `^\.ufo/waves/round-[^/]+/` (`seat-report-append-only.py:41`, `:81-100`).
- A file is `REWRITTEN` when it is absent at `TO` (`deleted`), when its bytes at `TO` are not
  a byte prefix of its bytes at `FROM` (`prefix-lost`), or when one side is not a blob.
  Blobs are read through one persistent `git cat-file --batch` process per side; the prefix
  test is `new.startswith(old)` (`:159-193`).
- Output: `REWRITTEN<TAB><path><TAB><reason>` per violation, then
  `SUMMARY<TAB>checked=<FROM count><TAB>rewritten=<count>`.
- Exit 0 = none rewritten, 1 = some, 2 = setup error (usage, missing lane, not a repository,
  unresolvable revision, git failure) (`:196-223`). Stdlib only; only `rev-parse`, `ls-tree`
  and `cat-file` are invoked, so the work tree, index and refs are never written.

## Fixture proof (it can fail)

`sh .ufo/waves/round-50/w1/T50ExecAppendOnly/receipts/fixture-driver.sh SCRATCH RECEIPTS CHECKER`
creates a `mktemp -d -p "$S"` repo, runs `git init -q`, asserts
`git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit
(`receipts/fixture/00-fixture.path:2-3`), and drives the cases below. All names are relative
to `receipts/fixture/`; each `<case>.exit` is the observed status.

| Case | Tree change | Exit | Key stdout |
|---|---|---|---|
| `01-append` | trailing bytes added to A.md and B.md, C.md new | **0** | `SUMMARY checked=2 rewritten=0` (`01-append.stdout`) |
| `02-edit-in-place` | A.md's second line changed | **1** | `REWRITTEN .ufo/waves/round-01/A.md prefix-lost` (`02-edit-in-place.stdout`) |
| `03-deleted` | B.md removed | **1** | `REWRITTEN .ufo/waves/round-01/B.md deleted` (`03-deleted.stdout`) |
| `04-truncated` | C.md loses its last line | **1** | `REWRITTEN .ufo/waves/round-01/C.md prefix-lost` |
| `05-non-round-ignored` | `.ufo/waves/other/n.md` rewritten | **0** | `SUMMARY checked=2 rewritten=0` |
| `06-identical` | FROM == TO | **0** | `SUMMARY checked=2 rewritten=0` |
| `07-renamed` | C.md -> C2.md inside the round tree | **1** | old path reported `deleted` |
| `08-bad-rev` | unresolvable FROM | **2** | `ERROR: cannot resolve revision 'no-such-revision'...` (`08-bad-rev.stderr`) |
| `09-missing-arg` | no arguments | **2** | `usage: seat-report-append-only.py LANE FROM TO` (`09-missing-arg.stderr`) |
| `10-non-repo` | LANE is a plain directory | **2** | `git rev-parse --show-toplevel failed` (`10-non-repo.stderr`) |
| `11-missing-lane` | LANE does not exist | **2** | `ERROR: LANE is not a directory` (`11-missing-lane.stderr`) |

Observed driver verdicts: `receipts/fixture/driver.log` — 16 `PASS` lines, 0 `FAIL`
(`01-append exit=0`, `02-edit-in-place exit=1`, ..., `append case checked 2 round files at
FROM, 0 rewritten`).

## Scale proof on real lane bytes

`sh receipts/clone-driver.sh SCRATCH RECEIPTS CHECKER LANE` clones the lane with
`git clone -q --shared` into scratch, asserts the clone's toplevel equals the clone dir
(`receipts/clone-scale/00-clone.path:2-3`), checks out `487b8f0…`, then commits two probes:

- append to `.ufo/waves/round-20/plan1.err` -> exit **0**, `SUMMARY checked=2819 rewritten=0`
  (`receipts/clone-scale/01-append.stdout`).
- prepend a line to landed seat report `.ufo/waves/round-42/w1/MutC1M10.md` -> exit **1**,
  `REWRITTEN .ufo/waves/round-42/w1/MutC1M10.md prefix-lost`
  (`receipts/clone-scale/02-rewrite.stdout`).

Driver verdicts: `receipts/clone-scale/driver.log` (4 `PASS`, 0 `FAIL`). This shows the
checker reads the same 2819 real round files it reports as checked and separates append from
rewrite on lane content, not only on synthetic files.

## Lane runs over the two requested ranges

Commands (checker is the deliverable path; `L` = lane):

```
python3 .ufo/waves/round-50/w1/T50ExecAppendOnly/seat-report-append-only.py "$L" \
  487b8f0da89fa0e2b8bea6930068accbf36e70a9 5891bdb77aba8489683533ae4cdd3b49b5e2626b
python3 .ufo/waves/round-50/w1/T50ExecAppendOnly/seat-report-append-only.py "$L" \
  'e3729de862f73ae080d98fcf522a7081ce16e40a^' e3729de862f73ae080d98fcf522a7081ce16e40a
```

Range endpoints are pinned: round-43 `base_rev` is `487b8f0…`
(`.ufo/evidence/round-43/contract.json:6`); round-44 tip is `5891bdb…`, the parent of the
round-45 freeze `3310e7b` (`git -C "$L" log --oneline -1 3310e7b^` -> `5891bdb round-44
verifier spot-check`).

| Range | Exit | Checked | Rewritten | Receipt |
|---|---|---|---|---|
| `487b8f0..5891bdb` | **0** | 2819 | 0 | `receipts/lane/r43base-r44tip.{stdout,exit}` |
| `e3729de^..e3729de` | **0** | 3979 | 0 | `receipts/lane/r49spot.{stdout,exit}` |

The zeros are correct for the files that exist at `FROM`, but they cannot cover the round-43
or round-49 artifacts themselves: those files are all added inside their ranges, so they are
never `FROM` files (the round-43 base precedes every round-43 artifact). Over the assigned
ranges git reports **no** modified or deleted round file, only additions (`A=114` and `A=0`),
so the checker has nothing to flag. The checker agrees with git's `M`/`D` set exactly, both
directions, for all four ranges run (`receipts/lane/crosscheck.stdout`); the target class is
exercised by running from each artifact's adding commit.

`e3729de^..e3729de` adds exactly one path outside the checked tree,
`corpus/lessons/round-49-verifier-spotcheck.md` (`git -C "$L" diff --name-status e3729de^
e3729de` -> `A corpus/lessons/round-49-verifier-spotcheck.md`); 3979 round files were
checked and none changed. Runtime: 27 ms and 31 ms (`receipts/lane/timing.stdout`).

### Adding-commit windows (the target class)

Run from each landed artifact's adding commit to the round tip; all four exit 1 and report
only files whose bytes were rewritten. Every run receipt has a sibling `.revs` file carrying
`from`, `to`, `tool_sha256` (`cee1a2dd…`), `exit` and the `SUMMARY` line, so no receipt
depends on a naming shorthand:

| Range (short ids) | Exit | Checked | Rewritten findings | Receipt |
|---|---|---|---|---|
| `c5335c70..83beaf98` | **1** | 2856 | 9 round-43 wave-1 reports (`CritC2Vacuous`, `CritC3Maps`, `MutC3Selftest`, `RevC2Classes`, `RevC3Tool`, `RevProvenance`, `RevReportDraft`, `ScribeLessonGate`, `ScribeQuality`) | `receipts/lane/addcommit-r43wave1-r44repair.*` |
| `edd4ca44..03facb22` | **1** | 3193 | `.ufo/waves/round-47/w1/T47ConnCross.md` | `receipts/lane/addcommit-r47deciding-wrapup.*` |
| `6b5ea3b1..03facb22` | **1** | 3186 | `round-47/build-spec-w2-draft.txt` deleted; `round-47/build-spec.py`; `round-47/w1/T47CritC1Control.md` | `receipts/lane/addcommit-r47inflight-wrapup.*` |
| `9b9b2a01..fc5ac743` | **1** | 3787 | `round-49/build-spec-w2.py`; `round-49/w1/T49RevengerLapse.md` | `receipts/lane/addcommit-r49content-r49rekey.*` |

The `T47ConnCross.md` finding is the silent rewrite already recorded at
`corpus/lessons/round-48.md:310` (+228/-214), and the nine round-43 reports are the ones
quantified under the known case below; the checker reproduces both.

### Mutation proof that the checker itself can fail

`receipts/c100-falsifier.py CHECKER SCRATCH RECEIPT_DIR` builds its own fixture (append,
in-place rewrite that grows the file, deletion, non-round edit) and stages three broken
copies of the checker. The pristine copy passes all four cases; every mutant prints exactly
one `FAIL ` line and is therefore caught as a wrong instrument:

```
PASS pristine append-r0 exit=0; PASS pristine rewrite-r1 exit=1
PASS pristine delete-r1 exit=1; PASS pristine non-round-r0 exit=0
FAIL mutant=prefix-to-length case=rewrite-r1 mutant_exit=0 pristine_exit=1
FAIL mutant=drop-deleted case=delete-r1 mutant_exit=0 pristine_exit=1
FAIL mutant=widen-scope case=non-round-r0 mutant_exit=1 pristine_exit=0
mutants recognised as wrong: 3/3
CRITERION-100-FALSIFIER-OK
```

(`receipts/quality/c100-falsifiers.{stdout,exit}` exit 0; exact replacements in
`receipts/mutation/mutations.txt`, raw per-mutant runs in `receipts/mutation/`.) The final
marker is the entry point the round-50 scribe's criterion 100 asks for; it is emitted only
when all pristine cases pass and all three mutants are detected.

## The known case: `.ufo/waves/round-43/w1/RevC2Classes.md`

The modification was flagged at round-43 closure as an uncommitted worktree edit:
`corpus/lessons/round-43-verifier-spotcheck.md:12` ("`git status --porcelain` shows a modified
committed wave-1 reviewer note ... its diff updates A13 pin/line references; it is not
clean") and routed at `:64` ("Restore or explicitly disposition the modified tracked file").
The round-44 lesson records the disposition at `corpus/lessons/round-44.md:85` ("retain and
commit the updated reviewer note as round-44 inherited evidence"), and `LOG.md:2269` says it
"is retained and committed under round 44".

**Was it ever committed? Yes — exactly once, in round 44, not in round 43.**

- At round-43 measurement `3c4003f` the committed bytes are sha256
  `8cf4e254…`; the same blob is still at round-43 spot-check commit `506e99c` (round-44
  base) and at round-44 freeze `05b3bd2`, `8bffd9b` and `315453b`
  (`receipts/lane/revc2-history.stdout`; command `git -C "$L" show <rev>:.ufo/waves/round-43/w1/RevC2Classes.md | sha256sum`).
- Along HEAD ancestry, the first and only commit whose tree carries the modified note is
  `83beaf980f246412368f89fbe7758375c8ca21e0` "round-44: repair citation masking and
  supersede S089 anchor" — `git -C "$L" diff --numstat 506e99c 83beaf9 --
  .ufo/waves/round-43/w1/RevC2Classes.md` -> `61 46`; new sha256 `72fe6559…`; it is the only
  commit in `git -C "$L" log --oneline 506e99c..83beaf9 -- <path>`. (`git log --all` also
  lists `refs/jj/keep/*` snapshots with the same blob; `git merge-base --is-ancestor` places
  them off HEAD, so they are jj keep refs, not lane history.) The edit that was dirty at
  round-43 closure is committed, but as round-44 inheritance, not as round-43 history.
- There is a second, separate in-place rewrite of the same file **inside** round 43:
  added at `c5335c7` (242 lines), rewritten at `3c4003f` (`git -C "$L" diff --numstat c5335c7
  3c4003f -- <path>` -> `213 230`). That rewrite was committed in round 43.

The checker catches both events and nothing else in those ranges:

```
seat-report-append-only.py "$L" 3c4003f6e97e5c787e7538b2eb35d62f49783aaf 5891bdb77aba8489683533ae4cdd3b49b5e2626b
  REWRITTEN  .ufo/waves/round-43/w1/RevC2Classes.md  prefix-lost
  SUMMARY    checked=2896  rewritten=1              (exit 1, receipts/lane/r43records-r44tip.*)
seat-report-append-only.py "$L" c5335c7 3c4003f6e97e5c787e7538b2eb35d62f49783aaf
  9 x REWRITTEN ... prefix-lost
  SUMMARY    checked=2856  rewritten=9              (exit 1, receipts/lane/r43wave1-r43records.*)
```

The nine round-43 reports rewritten at `3c4003f` are `CritC2Vacuous.md`, `CritC3Maps.md`,
`MutC3Selftest.md`, `RevC2Classes.md`, `RevC3Tool.md`, `RevProvenance.md`,
`RevReportDraft.md`, `ScribeLessonGate.md`, `ScribeQuality.md`; their numstat
(`git -C "$L" diff --numstat c5335c7 3c4003f -- <nine paths>`, captured in
`receipts/lane/revc2-history.stdout`) shows deletions in eight of the nine (e.g.
`RevC2Classes.md 213 230`, `CritC3Maps.md 199 188`, `ScribeQuality.md 168 94`). This is the
largest real instance of the class the rule targets, and the checker reports it exactly.

## Operability notes and risks

- **Revision-only.** Uncommitted worktree edits are invisible by design; the checker compares
  two committed trees. This is why no live `HEAD..worktree` run is offered: at round-50 HEAD
  the wave-1 seat reports are not committed yet, so a checker that insists on revisions will
  see nothing (or, for a different tool that reads the worktree, fail setup). Run it at a
  committed tip.
- **Scope is the assigned glob, not only `*.md`.** Specs, dispatch JSON, registries and
  receipts under `.ufo/waves/round-*/` are checked too; an in-place correction of any of them
  is flagged. Non-round paths under `.ufo/waves/` are ignored (tested).
- **Rename = deletion of the old path** (tested). A mode-only `chmod` is not a rewrite,
  because the rule is on bytes; `git` would still list it as `M`.
- **Non-blob entries** (gitlinks) would be reported `source-not-a-blob` / `target-not-a-blob`;
  none exists in any range tested.
- **Prerequisites.** Python 3 stdlib; git new enough for `rev-parse --end-of-options`
  (>= 2.24; host has 2.56.0). A bare repository or a shallow clone that lacks the `FROM`
  object exits 2, which is the intended setup-error channel.
- **Cost.** One `ls-tree` per revision and two `cat-file --batch` streams; peak memory is one
  `FROM` blob plus one `TO` blob. Largest wave blob at `5891bdb` is 437,262 bytes
  (`git ls-tree -r -l 5891bdb -- .ufo/waves | sort -k4 -n | tail -1`); 27-31 ms for
  2.8-4.0k files.
- **Tooling.** No installs or upgrades; pacman was not used (host-wide pause respected). Tools
  used: Python 3.14.8, git 2.56.0 (`receipts/00-toolchain.txt`).
- **Verification limits.** No lane state was written: deliverable and receipts only. The
  checker's agreement with git was shown on four ranges; it was not run against every
  historical range in the lane.

## Receipts

`receipts/00-toolchain.txt`; `receipts/fixture-driver.sh`, `receipts/fixture/` (11 cases +
`driver.stdout`, `results.txt`, `driver.log`, `violation-output.txt`, `00-fixture.path`,
`fixture-history.txt`); `receipts/clone-driver.sh`, `receipts/clone-scale/` (same shape);
`receipts/c100-falsifier.py`, `receipts/quality/c100-falsifiers.{stdout,stderr,exit}`,
`receipts/mutation/` (`mutations.txt` plus seven case triples); `receipts/lane/` (`r43base-r44tip`, `r49spot`,
`addcommit-r43wave1-r44repair`, `addcommit-r47deciding-wrapup`,
`addcommit-r47inflight-wrapup`, `addcommit-r49content-r49rekey`,
`r43records-r44tip`, `r43wave1-r43records`, `r43records-r44repair`,
`revc2-history.stdout`, `crosscheck.stdout`, `timing.stdout`; each run receipt has a
`.revs` sibling with FROM, TO, checker sha256, exit and SUMMARY). The scratch trees were removed
after the runs; `00-fixture.path` and `00-clone.path` record the scratch location of the
toplevel assertion only, and every claim in this report rests on commit ids and commands.

## Summary

Built `seat-report-append-only.py` (LANE FROM TO: every `.ufo/waves/round-*/` file at FROM must be a byte prefix at TO, else deleted/rewritten; exit 0/1/2; stdlib + read-only git).
Proof it fails: 11 fixture cases 16/16 PASS, clone-scale 4/4 on 2819 real lane files, and three staged mutants (prefix→length, deleted-branch, widened scope) each print `FAIL mutant=...` before `CRITERION-100-FALSIFIER-OK`.
Assigned ranges exit 0: `487b8f0..5891bdb` (2819 checked, 0 rewritten) and `e3729de^..e3729de` (3979 checked, 0 rewritten), matching git's M/D sets exactly; all their round artifacts are added inside the ranges, so none is a FROM file.
Adding-commit windows all exit 1: 9 round-43 reports (`c5335c70..83beaf98`), `T47ConnCross.md` (+228/-214), 3 round-47 files, 2 round-49 files.
Known case: the round-43 `RevC2Classes.md` modification was **never committed in round 43** (`506e99c` still has sha256 `8cf4e254…`).
It **was committed in round 44 at `83beaf9`** (+61/-46, `72fe6559…`) as inherited evidence; its earlier in-round rewrite at `3c4003f` (+213/-230) was committed in round 43.
Runtime 27-31 ms for 2.8-4.0k files, two blobs at a time; no installs, no lane writes beyond this report and its receipts under `w1/`.
