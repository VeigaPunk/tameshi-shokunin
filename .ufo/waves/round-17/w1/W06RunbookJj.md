# W06RunbookJj — jj-era audit of `corpus/knowledge/operator-runbook.md`

Lane: tameshi-shokunin · tip `98bea7da5801f4bc58e4187690ee1687c8a5061f` (branch `master`) · wave round-17 w1 · scope: runbook git/HEAD/branch/commit semantics + line-preserving corrections drafted here (not applied).

## Pins and lane state (observed)

| check | command | result |
|---|---|---|
| runbook live = committed | `sha256sum corpus/knowledge/operator-runbook.md`; `git show HEAD:…\|sha256sum`; `git show refs/heads/master:…\|sha256sum` | all `e1e349b69d798acb…`; exit 0; `wc -l` 511 (512 displayed lines) |
| lane is jj-colocated | `ls -d .jj` | `.jj` present, exit 0 |
| git HEAD | `git symbolic-ref -q HEAD` | rc=1 → **detached** |
| branch / bookmark | `bash scripts/hyaku/jj-lane.sh state <lane>` | `state branch=master local=98bea7da… remote=98bea7da… ahead=0 behind=0 head=detached tracked=2 untracked=5`, rc 0 |
| jj binary | `command -v jj; jj --version` | `/home/vgpnk/.local/bin/jj` 0.45.1 (present; **no jj call issued** by this audit) |

Observed: in this snapshot detached HEAD sits on the same commit as `master` (98bea7d), so no current reading is wrong. The hazard is structural: `jj-lane.sh:50-52` states "Colocated repos leave git HEAD detached on the working-copy commit", i.e. HEAD follows `@`, which can hold uncommitted/unbookmarked work [I]. Every "HEAD" instruction in the runbook therefore must read "branch tip" (bookmark `refs/heads/<branch>`).

## Findings — instructions that assume HEAD/branch/commit semantics

Each row: line · text now · problem · corrected line (one-for-one replacement; line count unchanged).

| # | line(s) | now (verbatim) | problem |
|---|---|---|---|
| F1 | 49 | `# (3) the six-case pin read — per case, ER-3's exact command set` | Defines no `<tip>`; claims ER-3 set, which still uses HEAD (see X1). |
| F2 | 51 | `git -C <owner-repo> show HEAD:<path> \| sha256sum` | HEAD = `@` in jj-colocated owners; may return uncommitted bytes, so "current" can read true/false against the wrong object. |
| F3 | 52 | `git -C <owner-repo> status --porcelain -- <path>  # worktree vs HEAD` | Comment names HEAD as the base; git status compares worktree to the index, not HEAD. |
| F4 | 53 | `git -C <owner-repo> merge-base --is-ancestor <REV> HEAD` | "moved past recorded revision" tested against `@`, not the bookmark. |
| F5 | 281 | `\| \`current\` \| \`git show HEAD:<path>\` sha == recorded pin \| …` | Reading-map rule keyed to HEAD. |
| F6 | 282 | `\| \`stale\` \| recorded revision is an ancestor of HEAD, live blob differs \| …` | Same. |
| F7 | 283 | `\| \`drift\` \| worktree differs from HEAD (porcelain non-empty, or live sha ≠ HEAD blob sha) \| …` | Same. |
| F8 | 298 | ``  cases). A `drift` reading waits for the commit, then re-pins`` | "the commit" is unspecified; in jj-era the owner's commit goes through `jj-lane.sh commit` and is cited by pushed hash. |
| F9 | 415 | ``3. **On `drift`:** wait for the commit, then re-pin; nothing is re-interpreted`` | Same as F8 in the operator loop (§8). |

Checked, no change needed:
- L355–356 `git show <rev>:<path>` — rev-addressed replay, not HEAD. (Optional [I]: `<rev>` should be a pushed hash.)
- L121 / L129–131 (git as dependency), L196 / L209 ("porcelain-clean" wording), L347–353 (`--regression`) — no HEAD/branch assumption.
- L440–441 "sibling trees read-only, all six clean" — porcelain wording only.
- No `commit`/`push`/`checkout`/`rebase`/`detached`/`branch` instruction exists beyond F8/F9; grep of `HEAD|[Cc]ommit|[Bb]ranch|git |…` over the whole runbook was the search used.

Records, not instructions — **leave unedited**; cover by errata (ER-R3 below):
- L30–31 "Tameshi HEAD at this write: `b8eb96e`" [O] (dated stamp).
- L316 table header `live (HEAD blob) | HEAD | worktree` and rows L318–323 (executed 2026-10-14 tick).
- L325–326, L330, L334–336 (executed headline, "moved HEADs", falsifier "HEAD blob").
- L492–493 ER-R1 "`git diff --numstat` … vs HEAD `b8eb96e`" — see X3.

## Cross-source divergences (out of this lane-write scope; routed, not edited)

Runbook says (L10–11, L248–249) the anchored source governs; the anchors below still say HEAD. A runbook correction therefore diverges from them and must be recorded as an append-only errata in the owner file, not smoothed.

- **X1** `corpus/knowledge/fleet-kill-rate-ledger.md:290-291` (ER-3 command set: `git -C <owner-repo> show HEAD:<path>`, `git … status --porcelain`) and `:293` ("drift … wait for the commit, then re-pin"). Owner: ledger lane. Proposed appended errata: "ER-R-jj (2026-10-20): in jj-colocated owners the HEAD read means the branch bookmark (`scripts/hyaku/jj-lane.sh state` field `local=`); the command set is re-stated in operator-runbook.md §0 (ER-R3). Rows above unchanged."
- **X2** `SKILL.md:1033-1035` (reading map: `git show HEAD:<path>`, "ancestor of HEAD", "worktree differs from its HEAD"). Owner: tameshi method lane. Proposed: replace `HEAD` with "branch tip (bookmark, `jj-lane.sh state` `local=`)" in those three cells; record as a method change in the round-17 SKILL.md note.
- **X3** (pre-jj, minor) ER-R1 L492–493: `git diff --numstat` with no ref compares worktree to **index**, not HEAD; the "vs HEAD" wording is a misstatement [I] (coincides with HEAD only when nothing is staged). Numbers stand at their timestamp; errata only.

## Draft corrections (apply as one-for-one line replacements; numbering unchanged)

Replace line 49:
```
# (3) the six-case pin read — per case; <tip> = owner branch bookmark: `bash scripts/hyaku/jj-lane.sh state <owner-repo>`, field local= (never HEAD; ER-R3)
```
Replace line 51:
```
git -C <owner-repo> show <tip>:<path> | sha256sum      # is the recorded revision the branch-tip blob?
```
Replace line 52:
```
git -C <owner-repo> status --porcelain -- <path>      # worktree vs git index (tracked-change hygiene; jj-lane state uses the same)
```
Replace line 53:
```
git -C <owner-repo> merge-base --is-ancestor <REV> <tip>  # moved past the recorded revision?
```
Replace line 281:
```
| `current` | `git show <tip>:<path>` sha == recorded pin (`<tip>` = branch bookmark, not HEAD) | swept bytes are the gate's live blob |
```
Replace line 282:
```
| `stale` | recorded revision is an ancestor of `<tip>`, live blob differs | gate moved past the recorded revision; the table is historical, not wrong |
```
Replace line 283:
```
| `drift` | worktree differs from the branch tip (porcelain non-empty, or live sha ≠ tip blob sha) | uncommitted bytes; a hygiene reading — git-materialized replays are already immune |
```
Replace line 298:
```
  cases). A `drift` reading waits for the owner's jj-lane commit (cite the pushed hash), then re-pins
```
Replace line 415:
```
3. **On `drift`:** wait for the owner's jj-lane commit (cite the pushed hash), then re-pin; nothing is re-interpreted
```

Append after line 512 (errata append-only; existing numbering untouched):
```

**ER-R3 — jj-era reading of "HEAD" (appended 2026-10-20 by W06RunbookJj; O/I).** Lane and owner repos are jj-colocated: git HEAD is detached and follows the working-copy commit `@`, not the branch bookmark (`scripts/hyaku/jj-lane.sh:50-52`; observed in tameshi: `jj-lane.sh state` → `branch=master local=98bea7da… head=detached`). Wherever this runbook's commands or the §6 reading map say HEAD, read the branch tip: the bookmark `refs/heads/<branch>` = the `local=` field of `jj-lane.sh state <owner-repo>`. Cited hashes are the pushed hash. The 2026-10-14 executed tables (§6, §9) and ER-R1/ER-R2 are records and are not re-interpreted; [U] whether HEAD tracked the branch at their read times is not measured here. The ledger ER-3 and SKILL.md:1033–1035 carry the same HEAD wording and are routed as divergences (X1, X2).

**ER-R4 — ER-R1 wording (O/I).** `git diff --numstat` with no ref compares the worktree to the index, not HEAD; the "vs HEAD" phrase in ER-R1 is a misstatement [I]. The recorded numbers stand at their timestamp.
```

## Commit path (not executed)

This audit wrote only this report. No commits, no `jj` calls, no git writes. If L1 applies the drafts, commit through the lane helper only, with a repo-relative path:
`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh commit /home/vgpnk/Projects/shokunin/tameshi-shokunin --as <lane-id> -m "<msg>" -- corpus/knowledge/operator-runbook.md` — `<lane-id>` not verified [U].

## Tool installs / updates

None. jj 0.45.1 at `~/.local/bin/jj` was already present; not invoked.

## Out of scope / not touched

Ledger, SKILL.md, service-limits, tools/* — read only where cited; no edits. No subagent dispatch (leaf).

## Verdict

**built** — drafts for every HEAD/branch/commit instruction in operator-runbook.md (F1–F9) are written above as one-for-one line replacements plus append-only errata (ER-R3, ER-R4); cross-source divergences X1–X3 routed to their owners; not applied to the runbook.
