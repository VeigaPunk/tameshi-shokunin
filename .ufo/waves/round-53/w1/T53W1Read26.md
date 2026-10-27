# T53W1Read26 — cold read of `### The tick and the pin read`

Seat: T53W1Read26 (leaf reader, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit (cand): `a41195dfc13a73958e4c5228ec196b28d03ded03`.
Heading: `### The tick and the pin read`.
Section at cand: lines **1023–1069** (next heading `### Triggers T1–T3 and the re-pin rule` at line 1071).
Section bytes: 47 lines, 4011 bytes, no trailing newline,
`section_sha256 = 0221fc822c87f3aff940aa6ed46e7b06cd649b37165f64d3400641c1d2256cda`.
Whole `SKILL.md` at cand: `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee` (2178 lines).
Lane section (same heading) is byte-identical at base `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`: the section was re-keyed, not edited, this round.

## Split reproduction (frozen monitor definition)

`git show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` was written to scratch and split at
`^#{1,3}(\s|$)` outside ``` fences: **63 headings**; the target is heading index 25 at line 1023; the next
heading is line 1071 `### Triggers T1–T3 and the re-pin rule`; trailing whitespace-only lines stripped, joined
with `\n`, hashed as UTF-8/surrogateescape without a trailing newline. Line range reproduced = **1023–1069**.

Independent cross-check (same bytes, shell):

```
git -C <lane> show <cand>:SKILL.md | sed -n '1023,1069p' | head -c -1 | sha256sum
→ 0221fc822c87f3aff940aa6ed46e7b06cd649b37165f64d3400641c1d2256cda
```

(`sed` alone gives 4012 bytes because it appends the final newline; `head -c -1` restores the no-trailing-newline
section bytes the spec defines.)

## Checks run

All reads were `git show <cand>:<path>` / read-only `git -C <repo> show <rev>:<path>`; no git or jj mutation,
no write outside this seat's w1 deliverables and its scratch.

1. **Section split / hash** — as above; reproduced twice (Python split and shell range).
2. **Tick idiom** — `shokunin@17c1fad:scripts/shokunin-watchdog.sh:3-5` reads
   "A lane's round ends when .ufo/reports/round-<N>/<lane>.md lands; … Tick 450s."; `:14` is
   `LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"` (no tameshi). Current fleet
   watchdog sets `INTERVAL=$TICK_SECONDS`, default 450 (`scripts/shokunin-watchdog.sh:52,61`), and
   `shokunin.conf:11` sets `TICK_SECONDS=450`.
3. **Conf migration** — `git log -1 5efb4114` = `2026-10-19T20:00:37-03:00` "substrate-neutral launch from
   shokunin.conf LANES …"; `git show 5efb4114:shokunin.conf` line 55 =
   `tameshi|tameshi-shokunin|depth + calibration (verification-fixture craft)`; current `shokunin.conf:55` the same.
4. **Branch resolver** — `scripts/hyaku/jj-lane.sh` has `cmd_state` (dispatched at `:839`), which resolves
   `lane_branch_git` (`git config --get lane.branch`, `:101-105`) first, else `detect_branch()` (`:118`), and prints
   `state branch=$branch …` (`:182`). Live run: `bash scripts/hyaku/jj-lane.sh state tameshi-shokunin` → rc 0,
   `state branch=master local=ace79e3d… remote=ace79e3d… ahead=0 behind=0 head=detached tracked=1 untracked=49`.
5. **`current` command form** — `git 2.56.0`;
   `git -C tameshi-shokunin rev-parse --verify --quiet --end-of-options "refs/heads/master^{commit}"` →
   `ace79e3df61266e9474e5c02086c0f7c79664580`, rc 0, and `git show <tip>:SKILL.md | sha256sum` works as written.
6. **ER-jj** — `corpus/knowledge/fleet-kill-rate-ledger.md:420` is the ER-jj block ("branch tip
   `refs/heads/<branch>` … canonical rule …"), with ER-jj2 at `:422` correcting the line anchor to the function name,
   which matches the section's "cite by name".
7. **Six recorded pins (table)** — verified against sibling git objects (read-only):
   kumitate@`175de6ba:scripts/kimi-census.mjs` = `83016d45`; kagi@`fecee874:corpus/surface-census.sh` = `275d8294`;
   tsukuroi@`165307fe:tools/tsukuroi-census.sh` = `084951be`; mado@`eead56b2:tools/mado-verify.sh` = `d7edaab4`;
   kagi@`fecee874:corpus/checklist-run.sh` = `7e5ec98b`; kumitate@`175de6ba:scripts/claims-check.mjs` = `e9a21b44`.
   The two `stale` moved tips also verify: tsukuroi@`aa136d69` = `bba6cdf6`; mado@`0c20a76f` = `90d50cdd`.
8. **Mado in-flight bytes** — `git -C mado-shokunin cat-file -e dc864c6a` → rc 128 (not an object; uncommitted, as the
   section's `drift` rule says). `0c20a76f:tools/mado-verify.sh` is 75,771 B, sha `90d50cdd…`.
9. **Tool and selftest** — `tools/mutate-and-run.sh` at cand prints its own sha on `MUTATE_TOOL:` (`:506`) and
   `REGRESSION_TOOL:` (`:1442`), matching the `held`/`moved` rule. Extracted the cand tree to scratch and ran
   `TMPDIR=<scratch>/tmp bash tools/mutate-and-run.sh --selftest` → last lines `MUTATE_SELFTEST: 107/107 pass`,
   `VERDICT: PASS`, rc 0 (6 s). The dated round-8 tool pin `cf41efaa…` exists as a historical blob of the same path
   (commit `9f1d3c339a70…`, committed `2026-10-14T16:06:31-03:00` = 19:06:31Z, before the 19:15:14Z tick).
10. **Scratch receipts** — `/tmp/w8-tameshi-t84/` does not exist (checked `ls`); both cited paths
    (`pin-read.txt`, `drift-demo.txt`) are absent. They are inside the section's explicitly timestamped round-8
    executed instance; the host scratch directive (`SKILL.md:25`) permits `/tmp` for files under 50 MB, and both are
    small files. Treated as dated evidence, not findings (see "Checked and not filed").
11. **Findings arithmetic** — 19:15:14Z + 6 min = 19:21:14Z, while the section's re-read stamp is 19:20:29Z
    (5 min 15 s). The page's twin record of the later tick (`SKILL.md:1188` at cand) already reads
    "five minutes later" for the same event.

## Holds (verified against the cand bytes and the pointed-at revisions)

- `scripts/shokunin-watchdog.sh:3-5` at fleet `17c1fad` (report-boundary round end + `Tick 450s.`) and `:14`
  (lane map without tameshi): **holds**.
- `since 5efb4114 (2026-10-19) the lanes live in shokunin.conf, which names tameshi (round 17)`: **holds**.
- `Tameshi's tick is still its own round series [I]`: an explicitly labelled inference, nothing contradicts it.
- `<branch>` = `branch=` field of `../scripts/hyaku/jj-lane.sh state <repo>`, `lane.branch` first else
  `detect_branch()`, cited by name: **holds** (see check 4).
- `current` rule (`git rev-parse --verify --quiet --end-of-options "refs/heads/<branch>^{commit}"`, `git show
  <tip>:<path>` sha256 == recorded pin, unresolvable branch → SETUP `rc 2`, absent path → equality fails): the command
  form works at git 2.56.0; `SETUP rc 2` is the fleet's could-not-evaluate class used elsewhere in the page.
- `stale` rule (recorded revision an ancestor + tip blob differs): consistent with the two stale rows, whose ancestor
  relation and moved tips were verified (check 7).
- `drift` rule (live sha ≠ tip blob, or non-empty porcelain; clean porcelain is not tip evidence under jj): consistent
  with the re-read bullet; the in-flight `dc864c6a…` is not in mado's object store (check 8).
- tool `held`/`moved` rule (`MUTATE_TOOL`/`REGRESSION_TOOL` sha): the tool emits both lines with `sha256=` of itself.
- The six-row table's pins and the `4 × current · 2 × stale · 0 × drift` tally: **holds** (check 7).
- The executed instance's host (`plazir27` = current hostname), tool pin (`cf41efaa…` = a real historical blob
  predating the tick), and predicates (the mado file at `0c20a76f` is `90d50cdd…`): **hold** as a dated record.
- `MUTATE_SELFTEST: 67/67` at round 8 and `at round 52 the tool prints MUTATE_SELFTEST: 107/107 pass`: the 107/107
  is reproduced at cand (check 9); 67/67 is explicitly dated to round 8 (prior receipt: `.ufo/waves/round-30/wC/ColdA03.md`
  executed the `cf41efaa…` blob and got 67/67).
- Falsifiers (superseded blob → `stale`; one appended line in a scratch copy → `drift`; untouched case → `current`):
  each follows from the table's own rules and was reproduced by prior seats (ColdA03); the mechanics hold.
- `The pin read is a timestamped observation, re-run at the next tick — never carried as a standing claim`: matches the
  page's later tick record.

## Findings

### F1 — interval misstated (5 min 15 s called "six minutes")

Quote (cand line 1057):

> `Re-read six minutes later (19:20:29Z)`

The section anchors the instance at `tick 2026-10-14T19:15:14Z` (line 1040). 19:15:14Z + 6 min = 19:21:14Z, not
19:20:29Z; the actual interval is 5 min 15 s. The same page already states "five minutes later" for the same event in
its round-9 record (`SKILL.md:1188`), and prior cold reads computed the same 5 m 15 s for this phrase
(`.ufo/waves/round-27/w1/Read17.md`, gap 6; `.ufo/evidence/round-51/coldread/reads/T51W2Read09.md:92`). The twin
section's wording was corrected; this instance was not. It fails as written.

### F2 — worktree miscount (six cases, four worktrees)

Quote (cand lines 1054–1055):

> `4 × current · 2 × stale · 0 × drift; tool held; all six worktrees clean`
> `(0 porcelain lines on every path) at the tick.`

The six cases live in four worktrees: the tool's own leg list at cand maps
`js-kimi-census`→kumitate, `bash-surface-census`→kagi, `bash-tsukuroi-census`→tsukuroi, `bash-mado-verify`→mado,
`bash-checklist-run`→kagi, `js-claims-check`→kumitate (`tools/mutate-and-run.sh`, leg block before `# Sources:`).
The section's own table shows the same collapse by repeating live HEADs: `175de6ba` for js-kimi-census and kumitate
claims-check; `fecee874` for bash-surface-census and kagi checklist-run. The page's twin record of the same six cases at
the next tick says exactly "all four sibling trees porcelain-clean (0 lines each) *at the tick*" (`SKILL.md:1184`).
"All six worktrees clean" therefore does not hold; the clean-worktree count is four (six paths across four trees).

## Checked and not filed

- **Absent `/tmp` receipts** (`/tmp/w8-tameshi-t84/pin-read.txt`, `/tmp/w8-tameshi-t84/drift-demo.txt`): both gone.
  They sit inside the explicitly timestamped round-8 executed instance (and the round-8 falsifier), the host scratch
  directive allows `/tmp` for files under 50 MB, and the table's content re-verifies from sibling git objects without
  them. Recorded as a dated-evidence caveat, not a finding (same disposition as round-30 ColdA03 / round-51 Read08).
- **`mtime 16:19:40` has no timezone**: the fleet's commit offsets are `-03:00`, which places it at 19:19:40Z, 49 s
  before the 19:20:29Z re-read; the section does not state the offset, but no stated value contradicts it.
- **"moves that path to `stale` and `drift`"**: the mado row already read `stale` at the tick, so the edit adds
  `drift`; the bold "**and**" is read as the dual label, not a transition claim. Not filed.
- **Round-52 taxonomy note** ("the three labels are not exhaustive — when the recorded revision is not an ancestor of
  the branch tip and the live file equals the tip blob, all three read no"): the stated conditions do not exclude
  `recorded pin == tip blob`, which would read `current`; the note is a dated round-52 annotation and its operative
  claim (a non-exhaustive taxonomy for rewritten history) is true. Not filed.
- **`unresolvable <branch> → SETUP rc 2`**: no committed tool implements the pin read (`jj-lane.sh state` exits 1);
  the row states the class the reader must apply, consistent with the fleet's exit-2 could-not-evaluate convention.
  No command output contradicts it; not filed.

## Scope / limits

- Read-only throughout: no git/jj mutation, no commit/push/fetch, nothing written under `.ufo/evidence/`, `tools/`,
  `corpus/` or `SKILL.md`. Writes: this report and `T53W1Read26.json` only, both under `.ufo/waves/round-53/w1/`.
- Tools installed/upgraded: **none**.
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read26/` (SKILL.md dump, cand tree extract, selftest TMPDIR);
  removed with `rm -rf` before yield.
- Not observable at cand: the live mado in-flight bytes (`dc864c6a…`, 99,716 B) and the 19:20:29Z worktree states —
  uncommitted and gone; the recorded HEAD blob and all six pins were verified instead.
