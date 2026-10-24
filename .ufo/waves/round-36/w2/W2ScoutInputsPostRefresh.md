# W2ScoutInputsPostRefresh — post-refresh descendant recon (round 36, wave 2)

## Attacked
C1 (calibration): the cold-read refresh commit `b455001` appended four L1 author
source re-anchor entries to `.ufo/evidence/round-21/coldread/ledger.json`; the
monitor then read credit 8 at `b455001e`. Question: did anything AFTER the
refresh commit modify the four sections' cited input paths, which would make the
tip reading differ from the measured 8?

## Refresh commit
`b455001e2589b3f4f471d94a3de7e5e549b9f54c`
"round-36: cold-read refresh — four L1 author source re-anchor entries
(recipe/restore-discipline/map/where-to-enter) with trace receipts, refresh
specs+receipts citing S103"

## Commits descending from the refresh commit

### Main line (master / HEAD; HEAD detached at fbb01cf)
1. `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` — "round-36: receipts — monitor
   before(796e08b)=6 / control(e423c41b)=6 / after(b455001e)=8 64-64, census
   exit 0 at b455001e (100 rows), depth guard 9/9, v2 deciding PASS at
   b455001e, empty-panel mutant v1 PASS / v2 FAIL"
2. `fbb01cf46f8437fd1264c1a3acc053c882fa2164` — "round-36 verifier spot-check
   (integrator, hyaku): non-author admit/reject" (= master = HEAD)

### jj/keep working-copy snapshot commits (reachable only via `refs/jj/keep/*`)
Enumerated with `git log --all --oneline --ancestry-path b455001..HEAD` (the
`--all` widens the positive endpoint set to every ref, surfacing descendants
ancestral only to jj keep-pins). All six are content-free snapshots — each tree
is byte-identical to a main-line commit's tree (verified `git rev-parse
<c>^{tree}`):

| snapshot  | tree identical to | parent    |
|-----------|-------------------|-----------|
| 972346c   | b455001           | b455001   |
| 12edb47   | d9c496b           | b455001   |
| 4d954ea   | d9c496b           | d9c496b   |
| efa0df9   | fbb01cf           | d9c496b   |
| 40eea6a   | fbb01cf           | d9c496b   |
| 652de9d   | fbb01cf           | fbb01cf   |

They introduce **no content beyond the two main-line commits**.

## Files touched post-refresh (union of all descendants)

`d9c496b` added 22 receipt files, all under `.ufo/evidence/round-36/`:
- `after/c1v2-at-b455001e.{exit,stderr,stdout}`, `after/census-at-b455001e.{exit,stdout}`,
  `after/depthD-at-b455001e.stdout`, `after/monitor-at-796e08b.{exit,stderr,stdout}`,
  `after/monitor-at-b455001e.{exit,stderr,stdout}`, `after/sources-rows-at-b455001e.txt`
- `control/monitor-at-e423c41b.{exit,stderr,stdout}`, `control/v1-at-emptypanel.{exit,stderr,stdout}`,
  `control/v2-at-emptypanel.{exit,stderr,stdout}`

`fbb01cf` added 1 file:
- `corpus/lessons/round-36-verifier-spotcheck.md`

Working tree at tip: `git status --porcelain` shows only untracked
`.ufo/waves/round-36/w1/` (wave evidence; not tracked content, not an input path).

## Four new ledger entries — cited input paths (union, 9)

From `ledger.json` `entries[-4:]` (refresh specs at
`.ufo/evidence/round-36/coldread/refresh-specs.json`, all read at
`e423c41ba253357ab8c8513f0376dad9d38ab248`):

| entry | section (SKILL.md lines) | input paths |
|-------|--------------------------|-------------|
| 1 | 131–245 "## Mutation-sweep recipe" | SKILL.md (implicit section source), LOG.md, SCORECARD.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md, corpus/knowledge/closeout-r11.md, corpus/knowledge/survivor-fixture-minimization.md, tools/mutate-and-run.sh |
| 2 | 375–404 "## Restore discipline" | SKILL.md, corpus/README.md, tools/mutate-and-run.sh |
| 3 | 1380–1395 "### The map" | SKILL.md, corpus/README.md, corpus/knowledge/closeout-r11.md, tools/mutate-and-run.sh |
| 4 | 1436–1448 "### Where to enter" | SKILL.md, corpus/knowledge/closeout-r11.md |

Union: `SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/closeout-r11.md`,
`corpus/knowledge/survivor-fixture-minimization.md`, `tools/mutate-and-run.sh`.

**Intersection with post-refresh touched files: EMPTY.** The only `corpus/`
file touched is the new `corpus/lessons/round-36-verifier-spotcheck.md`, which
is not cited by any of the four entries.

## Byte verification at tip (fbb01cf)

All 9 input paths sha256-verified against ledger-recorded hashes — all MATCH:

| path | sha256 (ledger == tip) |
|------|------------------------|
| SKILL.md | 2381873162fc21db… |
| LOG.md | a2223dc239aaa37c… |
| SCORECARD.md | 1b0124a79a81c75b… |
| corpus/QUALITY.md | f7382e201ba34f27… |
| corpus/README.md | 7c0fe513ac1999d1… |
| corpus/SOURCES.md | 16fae0a17acc934c… |
| corpus/knowledge/closeout-r11.md | f0894bf65aee32d8… |
| corpus/knowledge/survivor-fixture-minimization.md | 116b56236bc468c8… |
| tools/mutate-and-run.sh | a7d3f2dd7d47511a… (== frozen pin) |

Section bodies: all four match the recorded `skill_sha256`/`sha256` under the
ledger convention `sha256(b''.join(lines[start-1:end]).rstrip(b'\n'))`
(identified by testing conventions; plain join without the trailing-newline
rstrip does NOT match — convention note for future re-checks).

Also verified: `git diff b455001..HEAD -- .ufo/evidence/round-21/coldread/ledger.json`
is empty — the ledger itself was not amended after the refresh commit.

## Exact commands run (cwd = /home/vgpnk/Projects/shokunin/tameshi-shokunin)

- `git log --oneline -20`; `git status -sb`
- `git log --name-status --format='=== %h %s' b455001..HEAD`
- `git show --stat --format='%h %s' b455001`
- `git rev-parse b455001 d9c496b fbb01cf HEAD`
- `git branch -a --contains b455001`; `git tag --contains b455001`
- `git log --all --oneline --ancestry-path b455001..HEAD`
- `git for-each-ref --format='%(refname) %(objectname:short)'`; `git stash list`; `git status --porcelain`
- `git show --stat --format='...' {40eea6a,652de9d,efa0df9,12edb47,4d954ea,972346c}`
- `git for-each-ref --contains <c>` for each of the six snapshots
- `git rev-parse <c>^{tree}` comparisons (snapshot trees vs b455001/d9c496b/fbb01cf)
- `git diff --stat b455001..HEAD -- .ufo/evidence/round-21/coldread/ledger.json`
- Python (stdlib json+hashlib): loaded `ledger.json`, extracted `entries[-4:]`,
  unioned `inputs` maps, sha256-verified each union path's tip bytes, and
  re-hashed each section body `lines[start-1:end]` (with `.rstrip(b'\n')`)
  against `skill_sha256`.

## Verdict

**CLEAN — no disclosure required.** No commit after the refresh commit
`b455001e` modified any of the four sections' cited input paths: the only
post-refresh changes are round-36 evidence receipts under `.ufo/evidence/` and
one new lesson file. The six jj/keep snapshot descendants are tree-identical to
main-line commits and add nothing. All nine cited input files and all four
SKILL.md section bodies are byte-identical at tip `fbb01cf` to the hashes the
ledger entries recorded at read_rev `e423c41`. The tip reading equals the
measured 8.
