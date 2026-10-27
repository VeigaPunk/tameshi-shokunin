# T53W2Read19 — wave-2 re-read of `### The tick and the pin read`

Seat: T53W2Read19 (leaf reader, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Candidate (C\*\*): `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`. Freeze: `7d8aaac676cbcb6379f57659e7c3c4c12150a815`.

- Heading: `### The tick and the pin read`
- Section at C\*\*: lines **1026–1073** (next heading `### Triggers T1–T3 and the re-pin rule` at 1074), 48 lines, no trailing newline
- `section_sha256 = ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805`
- Same heading at the freeze commit hashes to the **same** sha: the section bytes are identical at C\*\* and at the freeze revision.
- Findings: **0**

## Split reproduction (frozen monitor definition)

Bytes read from git objects only (`git -C <lane> show <rev>:SKILL.md`), never the working tree.

1. Loaded the frozen sectionizer itself (`.ufo/evidence/round-18/measure.py`, imported as a module) and called
   `sectionize(raw)` on the C\*\* `SKILL.md` blob: **64 sections**; the target is `start=1026 end=1074`
   heading `### The tick and the pin read`, `sha256=ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805`.
2. Recomputed the section bytes by hand with the same rule (heading line through the line before the next heading,
   trailing whitespace-only lines stripped, `\n`-joined, no trailing newline) and re-hashed: identical
   (`ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805`).
3. Independent shell cross-check of the same range:

```
git -C <lane> show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md \
  | sed -n '1026,1073p' | head -c -1 | sha256sum
→ ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805  -
```

4. Same procedure at the freeze `7d8aaac…`: 64 sections, `start=1026 end=1074`, sha `ca86e98de294306f…`.

## Fix verification (run first)

Both wave-1 findings for this section were filed against C\* `a41195dfc13a73958e4c5228ec196b28d03ded03`
(`.ufo/waves/round-53/w1/T53W1Read26.json`, F1 interval-misstated, F2 worktree-miscount).

`git -C <lane> diff a41195dfc13a73958e4c5228ec196b28d03ded03 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e -- SKILL.md`
contains exactly one hunk touching this section, and it carries both fixes:

```
-4 × `current` · 2 × `stale` · 0 × `drift`; tool `held`; all six worktrees clean
+4 × `current` · 2 × `stale` · 0 × `drift`; tool `held`; all four sibling
+trees porcelain-clean (six case paths across four worktrees;
+0 porcelain lines on every path) *at the tick*.
-- **Re-read six minutes later (19:20:29Z) — a live `drift`:** mado's in-flight
+- **Re-read five minutes later (19:20:29Z; the tick was 19:15:14Z — a 5 min 15 s gap) — a live `drift`:** mado's in-flight
```

### Fix 1 (F1, interval) — present and correct

C\*\* bytes (section line 36):

```
- **Re-read five minutes later (19:20:29Z; the tick was 19:15:14Z — a 5 min 15 s gap) — a live `drift`:** mado's in-flight
```

The wave-1 defect was `Re-read six minutes later (19:20:29Z)` against a `19:15:14Z` tick (6 min would be 19:21:14Z).
The C\*\* line now states the interval the record supports and carries the exact gap: 19:15:14Z + 5 min 15 s = 19:20:29Z.
The head phrase "five minutes later" is a rounded restatement immediately qualified by the exact `5 min 15 s` figure, and it
matches the page's twin record of the same event (`SKILL.md:1188` at C\*\*, "five minutes later"). The fix is in the bytes and
arithmetically exact; no residue of the "six minutes" wording exists anywhere in the section.

### Fix 2 (F2, worktree count) — present and correct

C\*\* bytes (section lines 32–34):

```
4 × `current` · 2 × `stale` · 0 × `drift`; tool `held`; all four sibling
trees porcelain-clean (six case paths across four worktrees;
0 porcelain lines on every path) *at the tick*.
```

Independently re-derived the worktree count from the pins themselves (`git -C <sibling> show <rev>:<path> | sha256sum`,
read-only, output below under Holds): the six cases resolve to **four** repos —
kumitate (`js-kimi-census`, `claims-check`), kagi (`bash-surface-census`, `checklist-run`), tsukuroi (`bash-tsukuroi-census`),
mado (`bash-mado-verify`) — i.e. six case paths across four worktrees, exactly as the fixed sentence says. The C\* wording
("all six worktrees clean") is gone. The page's twin record of the same six cases (`SKILL.md:1189` at C\*\*) independently
reads "all four sibling trees porcelain-clean (0 lines each)", so the fixed count is consistent page-wide.

## Holds (verified against C\*\* bytes + the pointed-at revisions)

All commands read-only (`git show`, `git -C <repo> show`, `grep`, `sed`, `sha256sum`, `hostname`); no git/jj mutation.

1. **Tick idiom** — `shokunin@17c1fad:scripts/shokunin-watchdog.sh:3-5` contains
   "A lane's round ends when .ufo/reports/round-<N>/<lane>.md lands" and "Tick 450s."; `:10` is `INTERVAL=450`; the cited
   range resolves. Current fleet watchdog still ticks 450 s (`scripts/shokunin-watchdog.sh:52,61`, `shokunin.conf:11`
   `TICK_SECONDS=450`) and still keys the round end on the lane report file (`:164`, `:444`). **Holds.**
2. **Lane map did not name tameshi (`:14`)** — `git show 17c1fad:scripts/shokunin-watchdog.sh | grep -n tameshi` → no match;
   line 14 is `LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"`. **Holds.**
3. **Conf migration** — `git show -s 5efb4114` = `2026-10-19T20:00:37-03:00`, subject "scripts: shokunin-watchdog.sh —
   substrate-neutral launch from shokunin.conf LANES …"; `git show 5efb4114:shokunin.conf` contains
   `tameshi|tameshi-shokunin|depth + calibration (verification-fixture craft)` (current `shokunin.conf:55` the same).
   Both `5efb4114` and `17c1fad` are ancestors of the fleet HEAD. **Holds.**
4. **Branch resolver** — `scripts/hyaku/jj-lane.sh` (fleet root; `../scripts/hyaku/jj-lane.sh` from the lane) has
   `state) shift; cmd_state "$@"` at `:839`; `cmd_state` resolves `lane_branch_git` (git config `lane.branch`) first, else
   `detect_branch()` (`:118`), and prints `state branch=$branch local=… remote=… ahead=… behind=… head=… tracked=… untracked=…`.
   The `branch=` field exists as the section says; ER-jj2 (`fleet-kill-rate-ledger.md:422`) confirms citing the helper by
   name, which the section does. **Holds.**
5. **ER-jj anchor** — `git show C**:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '420p'` is the ER-jj block
   ("…now reads the branch tip `refs/heads/<branch>`…"); same line at the freeze. **Holds.**
6. **Rule table vs the six recorded pins** — read-only re-derivation of every cell's blob sha:

```
kumitate@175de6ba:scripts/kimi-census.mjs      → 83016d45   (recorded 83016d45, current)
kagi@fecee874:corpus/surface-census.sh         → 275d8294   (recorded 275d8294, current)
tsukuroi@165307fe:tools/tsukuroi-census.sh     → 084951be   (recorded 084951be, stale)
mado@eead56b2:tools/mado-verify.sh             → d7edaab4   (recorded d7edaab4, stale)
kagi@fecee874:corpus/checklist-run.sh          → 7e5ec98b   (recorded 7e5ec98b, current)
kumitate@175de6ba:scripts/claims-check.mjs     → e9a21b44   (recorded e9a21b44, current)
tsukuroi@aa136d69:tools/tsukuroi-census.sh     → bba6cdf6   (live tip, stale row's new blob)
mado@0c20a76f:tools/mado-verify.sh             → 90d50cdd   (live tip, stale row's new blob and re-read's HEAD blob)
```

   The table's `pin vs live blob` cells, the `4 × current · 2 × stale · 0 × drift` tally and the `stale` rows' "branch-tip
   blob differs" condition all reproduce. **Holds.**
7. **Tool pin of the executed instance** — `git show 9f1d3c33:tools/mutate-and-run.sh | sha256sum` =
   `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (commit `2026-10-14T16:06:31-03:00` = 19:06:31Z,
   before the 19:15:14Z tick). The `cf41efaa…` tool pin is a real historical blob of the path the section names. **Holds.**
8. **`held` / `moved` rule** — `tools/mutate-and-run.sh` at C\*\* prints its own content sha on
   `MUTATE_TOOL: %s sha256=%s` (`:506`) and `REGRESSION_TOOL: %s sha256=%s` (`:1442`). **Holds.**
9. **Selftest claims in the falsifier bullet** — C\*\* bytes (section lines 44–45):

```
  doctored-pin refusal is a different arm, selftested
  `MUTATE_SELFTEST: 67/67` at round 8; at round 52 the tool prints `MUTATE_SELFTEST: 107/107 pass`): a case whose row points at a superseded blob reads
```

   `MUTATE_SELFTEST: 67/67` is explicitly dated "at round 8" (the cf41efaa-era
   count; round-9 ledger receipt at `fleet-kill-rate-ledger.md:341` records `MUTATE_SELFTEST: 67/67 pass` at that tool);
   "at round 52 the tool prints `MUTATE_SELFTEST: 107/107 pass`" matches the committed round-52 receipt
   `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out` (commit `7ff81a5`, last lines `MUTATE_SELFTEST: 107/107 pass`,
   `VERDICT: PASS`) and the tool's printf (`:2125`). `tools/mutate-and-run.sh` is byte-identical between base `6db1d220` and
   C\*\* (`git diff --stat` empty), so the C\*\* runner is the one those receipts measured. **Holds.**
10. **Doctored-pin arm** — the runner's selftest covers the distinct refuse arm (`regression pin mismatch is SETUP (exit 2)`,
    `regression engine fails a doctored table`): `SETUP (pin mismatch: recorded=… materialized=…)` at `:1314`. **Holds.**
11. **Executed-instance predicates that are checkable now** — host `plazir27` = current `hostname`; the re-read's
    `vs HEAD blob 90d50cdd…` is the mado branch-tip blob (row 6); `dc864c6a…` is not an object in mado's store (consistent
    with the section's own "uncommitted/unpushed bytes" drift definition); mtime 16:19:40 at the fleet's `-03:00` offset is
    19:19:40Z, 49 s before the 19:20:29Z re-read. **Holds.**
12. **"The pin read is a timestamped observation, re-run at the next tick — never carried as a standing claim"** — nothing in
    the section presents the six-row table as a current reading; the rows are scoped "*at the tick*". **Holds.**

## Findings

**None.** Every statement in the section either reproduces from git objects at C\*\* / at the revisions it names, or is an
explicitly dated historical record. Both wave-1 findings are fixed in the C\*\* bytes and the fixes are correct.

## Checked and not filed

- **`/tmp/w8-tameshi-t84/pin-read.txt` and `/tmp/w8-tameshi-t84/drift-demo.txt`** — inside the dated round-8 executed instance
  ("tick 2026-10-14T19:15:14Z"); the host scratch directive permits `/tmp` for files under 50 MB and both are small; the
  table re-verifies from sibling git objects without them. Dated evidence, not a live receipt claim → hold.
- **"moves that path to `stale` **and** `drift`"** — the mado row already read `stale` at the tick, so the re-read adds
  `drift`; the bold "**and**" is read as the dual label (the row now satisfies both rules), not as a from-nothing transition.
  Same disposition as wave-1. Not filed.
- **Round-52 note "the three labels are not exhaustive"** — the stated conditions (recorded rev not an ancestor; live file ==
  tip blob) do not exclude `current` when the recorded pin also equals the tip blob; the note's operative claim (the taxonomy
  is not exhaustive for rewritten history) is true and the wording was accepted by the round-52 wave-3 review
  (`T52W3RevApplied4.md`). Not filed.
- **"since `5efb4114` … the lanes live in `shokunin.conf`"** — `shokunin.conf` existed earlier (fleet `e0b4d9b3`, 2026-10-13,
  two lanes, no tameshi; tameshi entered at `9ee70596`, 2026-10-14), but the **driver** has sourced its lane map from the conf
  only since `5efb4114`, which is what the sentence (subject: "the fleet driver idiom") says. Not filed.
- **`mtime 16:19:40` without an offset** — the fleet's commits are `-03:00`; converted it lands 49 s before the re-read. No
  stated value contradicts it. Not filed.
- **"all four sibling trees porcelain-clean"** — the parenthetical defines the measurement as "0 porcelain lines on every
  path", i.e. the per-path `git status --porcelain -- <path>` reads; read together the sentence claims exactly what was
  measured. Not filed.

## Scope / limits

- Read-only throughout: no git/jj mutation, no commit/push/fetch, nothing written under `.ufo/evidence/`, `tools/`, `corpus/`
  or `SKILL.md`, and no sibling/fleet file touched. Writes: only `T53W2Read19.json` and this report under
  `.ufo/waves/round-53/w2/`.
- Tools installed/upgraded: **none** (no pacman; PACMAN GUARD respected; nothing needed installing).
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read19/` (C\*\* `SKILL.md` blob, section extraction, split script);
  removed with `rm -rf` before yield — no leftover tree.
- Not observable now: the 19:20:29Z live mado bytes (`dc864c6a…`, 99,716 B, mtime 16:19:40) and the 19:15:14Z per-path
  porcelain states — uncommitted and gone. The recorded HEAD blobs and all six pins were verified instead.
