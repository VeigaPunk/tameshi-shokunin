# B14ErJjCorrections — R17-CITATIONS staged corrections

Base: lane `183f87b899e6cae46be98d251cbc87fb5118f6ca` (master). Fleet anchor checked at fleet `5d8a3b5` (cited by the round-17 spot-check) and fleet `ae12f33` (current HEAD, `scripts/hyaku/jj-lane.sh` tracked, worktree clean per `git status --porcelain`).

## 1. Anchor verification

| Claim | Evidence | Result |
|---|---|---|
| `detect_branch` is at line 115 | `git show 5d8a3b5:scripts/hyaku/jj-lane.sh \| grep -n '^detect_branch()'` → `115:detect_branch() { # <dir>`; same at `ae12f33` | holds |
| Cited `jj-lane.sh:53-65` is the resolver | `sed -n 53,65p` at fleet root: `jj-lane.sh init …`, `commit …`, `push …`, `state …`, exit-code and output help lines (inside `usage()`, which starts at line 50) | **falls** — stale anchor points at help text |
| Citation sites at base | `git grep -n 'jj-lane.sh:53-65\|53.65' 183f87b8 -- corpus SKILL.md` | 4 ER-jj notes + 1 ER-R3 note (runbook) + `SKILL.md:1029` (reading rule) + `corpus/lessons/round-17-verifier-spotcheck.md:447` (lesson record; not staged, lessons are historical) |

Note on the function's role (for the ER-jj2 wording): `detect_branch()` returns a branch **name**: the attached HEAD's branch (`symbolic-ref -q HEAD`), else `origin/HEAD`. The tip is still resolved separately from `refs/heads/<branch>`. The corrected block says exactly that and nothing more.

## 2. Staged copies (ER-jj2 block appended at EOF; base bytes are an exact prefix)

All five base files end with a newline and their cited note is the final block, so the append point is EOF. Proof per file: `cmp <(git show 183f87b8:<f>) <(head -c <base-bytes> <staged>)` → identical; `tail -c +<base+1> <staged> | cmp - <block>` → identical.

| Staged file (under `.ufo/waves/round-18/staged/corpus/knowledge/`) | base bytes | staged bytes | base lines → staged | cited note |
|---|---|---|---|---|
| `fleet-kill-rate-ledger.md` | 40058 | 40636 | 420 → 422 | ER-jj `:420` |
| `incremental-pin-disposition.md` | 27034 | 27612 | 386 → 388 | ER-jj `:386` |
| `service-limits.md` | 22311 | 22889 | 279 → 281 | ER-jj `:279` |
| `verification-patterns-fleet.md` | 40254 | 40832 | 309 → 311 | ER-jj `:309` |
| `operator-runbook.md` | 32249 | 33515 | 514 → 516 | ER-R3 `:514` (block 2, below) |

Block for the four ER-jj notes (`block-ejj.txt`, one line, preceded by a blank line):

```
**ER-jj2 (round 18, 2026-10-20; append-only).** The line anchor `../scripts/hyaku/jj-lane.sh:53-65` in the ER-jj note above is stale: that range is the `usage()` help text, not the branch resolver. The resolver the note means is the function `detect_branch()` in `scripts/hyaku/jj-lane.sh` (fleet root); it returns a branch name (the attached HEAD's branch, else `origin/HEAD`), and the tip is still `refs/heads/<branch>`. Cite it by function name, not by line. This block corrects only the anchor: the reading rule above is unchanged and dated records are not re-interpreted.
```

## 3. operator-runbook.md — ER-R3 mechanism record (appended, nothing reverted)

Spot-check claim checked: the round-17 commit `2a22ade` changed the runbook in place. `git diff 606716f 183f87b8 -- corpus/knowledge/operator-runbook.md` shows these in-place edits to existing text:
- step-(3) header: `per case, ER-3's exact command set` → `per case; <tip> = the owner's branch tip …`; the `show HEAD:<path>`, `merge-base --is-ancestor <REV> HEAD` lines → `<tip>` forms;
- §6 reading-table rows `current`/`stale`/`drift` rewritten from HEAD to `<tip>`;
- re-pin rule: `waits for the commit, then re-pins` → `waits for the owner's jj-lane commit (cite the pushed hash), then re-pins`;
- on-drift step: same rewording.

Miss found: the status command comment at the step-(3) block (base line 52) still reads `# worktree vs HEAD`, although ER-R3 says all HEAD readings were substituted. Recorded, not edited in place.

Block for the runbook (`block-r3.txt`, appended after the ER-R3 note; contains the ER-jj2 anchor correction plus the mechanism record):

```
**ER-jj2 (round 18, 2026-10-20; append-only).** The line anchor `../scripts/hyaku/jj-lane.sh:53-65` in the ER-R3 note above is stale: that range is the `usage()` help text, not the branch resolver. The resolver is the function `detect_branch()` in `scripts/hyaku/jj-lane.sh` (fleet root), which returns a branch name (the attached HEAD's branch, else `origin/HEAD`); the tip is still `refs/heads/<branch>`. Cite it by function name, not by line. Mechanism record: the round-17 ER-R3 substitutions (landed in commit `2a22ade`) were made in place, not appended, which the append-only rule does not allow. They are the step-(3) command block (the header, `show <tip>:<path>`, and `merge-base --is-ancestor <REV> <tip>`), the §6 reading-table rows for `current`, `stale` and `drift`, the drift sentence of the re-pin rule, the on-drift reading step, and the step-(3) header wording that dropped "ER-3's exact command set". They are not reverted here. Known miss, not edited in place: the status command's comment (`git -C <owner-repo> status --porcelain -- <path>`, "worktree vs HEAD") still reads HEAD, though ER-R3 says every HEAD reading now reads the branch tip. The executed records (the 2026-10-14 tables, ER-R1, ER-R2) are unchanged and are not re-interpreted.
```

## 4. SKILL.md:1029 — drafted append (L1 decides; not staged, not written to SKILL.md)

Proposed append after the reading-rule block at `SKILL.md:1027-1035`:

```
**Round-18 anchor note (append-only).** The `../scripts/hyaku/jj-lane.sh:53-65` anchor in the reading rule above is stale; that range is the `usage()` help text. The branch-name resolver is the function `detect_branch()` in `scripts/hyaku/jj-lane.sh` (fleet root), cited by function name; the tip is `refs/heads/<branch>`. The rule itself is unchanged.
```

## 5. Observations for the L1 / fleet owner (not acted on)

- `detect_branch()` comment says "Branch detection used ONLY by init", but it is also called in `cmd_state` (working-tree `scripts/hyaku/jj-lane.sh:162`) and at lines 387 and 391. Comment/use mismatch in fleet-owned code.
- `detect_branch()` reads `symbolic-ref -q HEAD`. In a detached colocated jj state that is empty, so it falls through to `origin/HEAD`, which may not be the lane's branch. Callers consult `lane.branch` config first (`lane_branch_git`, line 98), which limits the exposure. [INFERENCE from code reading; not exercised.]
- `corpus/lessons/round-17-verifier-spotcheck.md:447` also cites `:53–65`. Lesson records are historical; left unchanged, flagged for the L1.

## 6. Scope, tools, writes

- Writes: five staged files under `.ufo/waves/round-18/staged/corpus/knowledge/`, this report, and scratch under `/tmp/tameshi-r18w1-B14ErJjCorrections-9KqVhg/`.
- No edits to live lane files, no git writes, no jj use, no subagent dispatch, no SKILL.md edit, no messages sent.
- Tools installed/updated: none.
- Checks not run: no lane selftests (not assigned).

Verdict: built (five staged ER-jj2 corrections proven prefix-identical; SKILL.md:1029 append drafted; runbook mechanism record drafted; the stale anchor is confirmed as `usage()` text at both cited fleet revisions).
