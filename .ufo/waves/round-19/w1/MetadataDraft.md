# Round 19 w1 — MetadataDraft (C1 knowledge metadata defects)

Seat: `TameshiR19-2.MetadataDraft`. Leaf member; no subagent dispatch. Read-only against production; this file is the only write.
Installs/updates: none. No builds, tests, linters, formatters, or lane selftests run.
Baseline: `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` (round-18 spot-check). Observed tip: `21e7932` (round-19 commit `round-19: correct routed metadata and retain effective historical receipts`, on `refs/heads/master`).
Scope: lesson `corpus/lessons/round-18-verifier-spotcheck.md` §5 defects 1 and 2 only. Defects 3–5 belong to other seats.

## Verdict

- The two knowledge metadata defects are **already durably corrected** at committed `21e7932`, each by an append-only dated errata block. I did not need to draft the named corrections from scratch; I checked the committed prose against the sources and receipts it cites (table below).
- Both named errata are factually accurate on every checkable point I tested.
- Residual stale phrases that the named errata do **not** name exist in the same two entries. They are not among the five routed defects, but they are the same defect class. Optional append-only addenda are drafted in §4.
- Counts for C1 scope (two knowledge defects only): baseline 0/2 corrected → HEAD 2/2 corrected. This does not establish the 5/5 aggregate; that depends on defects 3–5, which I did not examine.

## 1. Commands and observed outcomes

| # | Command (run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`) | Observed |
|---|---|---|
| 1 | `git log --format='%h %an %cI %s' -n 3 -- corpus/knowledge/guard-kill-closure.md` | `21e7932` (2026-10-21T02:48:27-03:00, `tameshi-shokunin`) is latest touching commit; prior `9ee1c80`, `58e5d53`. |
| 2 | `git log ... -- corpus/knowledge/mutation-case-kumitate-sources-check.md` | Same `21e7932` head. |
| 3 | `git merge-base --is-ancestor 921ef80… HEAD` / `4b7c682… HEAD` | Both ancestors. `refs/heads/master` = `21e7932`. `git merge-base --is-ancestor 21e7932 master` → on master. |
| 4 | `git status --porcelain -- corpus/knowledge corpus/SOURCES.md` | Empty: the two knowledge files and SOURCES are clean. (Other lanes have uncommitted edits to `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-19.md`; not touched by me.) |
| 5 | `git show 7243e7f:<file> \| grep -c 'Erratum R18-'` | guard-kill: 0; mutation-case: 0. |
| 6 | `git show 7243e7f:<file>` lines 1–2 grep `PENDING\|queued` | guard-kill line 2 stale `Landed-tip results: PENDING`; mutation-case line 1 stale `S008 … **queued** … not yet a mined row`. Both 1. |
| 7 | `grep -c 'Erratum R18-' <file>` at working tree (= `21e7932` for these files) | guard-kill: 1 (`## Erratum R18-1`, line 171); mutation-case: 1 (`## Erratum R18-2`, line 266). |
| 8 | `git diff --numstat 7243e7f HEAD -- <two knowledge files>` | guard-kill `21 0`; mutation-case `12 0`. **Zero deleted lines** in both. |
| 9 | `git diff 78b99dd 21e7932 -- <two files> \| grep -c '^-[^-]'` | 0. |
| 10 | `sha256sum .ufo/evidence/round-18/final/probes.stdout` | `d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0`. |
| 11 | `grep -A12 '"probes"' .ufo/evidence/round-18/final/checks.json` | argv `defect-probes.py --rev 921ef8077440f90d092aab4b9fdc750a45de1224`, exit 0, `stdout_sha256` `d37c99e3…eb8cf0` (matches #10). |
| 12 | `grep 'DEFECT_PROBES' .ufo/evidence/round-18/final/probes.stdout` | `DEFECT_PROBES: open=0 closed=11 total=11`. |
| 13 | Python parse of `.ufo/evidence/round-18/final/registry-branch-aligned.stdout` | `rows`=35; status counts `active`=31, `superseded`=4; top-level `held`=31, `total`=31, `superseded`=4, `exit`=0, `rev`=`5923d89ac491ec3d296905561a8ab0faf3fda65a`. |
| 14 | `git show 4b7c682:corpus/SOURCES.md \| grep '^| S008 '` | Status cell `mined`, date 2026-10-19, used-by `corpus/knowledge/mutation-case-kumitate-sources-check.md`. |
| 15 | Used-by last-cell at `4b7c682` for S001, S008, S052, S056, S057 | S001 → `mutation-score-semantics.md`, `mutation-case-kumitate-sources-check.md`; S008 → `mutation-case-kumitate-sources-check.md`; S052/S056/S057 → `mutation-case-kumitate-round-gate.md`, `mutation-case-kumitate-sources-check.md`. |
| 16 | `grep -rn 'S008' corpus/ \| grep -i 'queued\|not yet a mined'` | Hits: mutation-case line 1 (named by R18-2), line 215 (**not named**), line 268 (R18-2 itself), `corpus/lessons/round-18.md:47` (historical change record), spot-check line 189 (the defect statement). |
| 17 | `grep -rln 'Landed-tip results: PENDING' corpus/` | `guard-kill-closure.md` (line 2, named by R18-1) and the spot-check lesson (quoting the defect). |
| 18 | `git show 4b7c682:…/guard-kill-closure.md \| sed -n 2p` and `…/mutation-case… \| sed -n 1p` | Confirm the stale text is what the lesson describes at `4b7c682`. |
| 19 | `git show 21e7932 --stat` | Round-19 commit touches 26 files; the two knowledge files are +21/0 and +12/0. `corpus/SOURCES.md` is +9/−1: the one deleted line is the S049 row, with `corpus/lessons/round-19.md` appended to its used-by cell. Not a metadata defect in scope; noted only. |

## 2. Named-erratum check (what is already committed)

### Defect 1 — `corpus/knowledge/guard-kill-closure.md` line 2

Committed text: `## Erratum R18-1 — verified-at metadata (2026-10-21, round 19)` at line 171 of `21e7932`.

| Claim in R18-1 | Check | Result |
|---|---|---|
| Supersedes line 2 `Landed-tip results: PENDING (filled by L1 after landing)` | #6, #18 | Matches the stale line at `7243e7f`/`4b7c682`. Pass. |
| Also supersedes PENDING statements at lines 10, 53, 65, 91, 97, 114, 118, 120, 122, 132, 134, 136 | #17 and line scan of `21e7932` | Lines 10, 53, 65, 91, 97, 114, 118, 120, 122, 132, 136 literally contain `PENDING`/"not yet at the landed tip"/"Every landed-tip number is PENDING". **Line 134** (`Not run: no after-landing probe run …`) names no `PENDING` token; it is a landed-tip "not run" statement, so including it is a reasonable reading, not a literal match. Pass with that note. |
| Effective verified-at = tool revision `921ef80…` | #3, #11 | Ancestor of HEAD; checks.json argv pins it; exit 0. Pass. |
| Receipt `final/probes.stdout` shows `open=0 closed=11 total=11` | #12 | Matches. Pass. |
| Receipt SHA recorded in `final/checks.json` row `probes` | #10, #11 | `d37c99e3…eb8cf0` equal. Pass. |
| Registry evidence `5923d89`, 31 active held, four superseded | #13 | `held` 31, `active` 31, `superseded` 4, `rows` 35, `rev` 5923d89. Pass. |
| EG-3 limits and 18 survivors remain open | Lesson §2 C2, EG-3 text at line 154–162 | Consistent. Pass. |

Verdict: correction accurate; append-only (0 deleted lines, #8, #9).

### Defect 2 — `corpus/knowledge/mutation-case-kumitate-sources-check.md` line 1

Committed text: `## Erratum R18-2 — source metadata (2026-10-21, round 19)` at line 266 of `21e7932`.

| Claim in R18-2 | Check | Result |
|---|---|---|
| Supersedes line 1's S008 `queued` / `not yet a mined row` | #6 | Matches. Pass. |
| At `4b7c682`, S008 is `mined` with this entry in used-by | #14 | Pass. |
| Effective S008 metadata: paper, tier A, mined | #14 (row columns `paper | A | … | mined`) | Pass. |
| ER8-1 already recorded the transition | Errata ER8-1 text (line ~226–229): "S008 is `mined` since `58e5d53`" | Consistent with the SOURCES row. Pass. |
| Verify with that revision's SOURCES.md, not the entry alone | Advisory | Accepted. |

Verdict: correction accurate; append-only (0 deleted lines, #8, #9).

## 3. Residual stale statements not named by the existing errata

These are outside the five routed defects as the lesson lists them. They are the same class, so I list them with evidence. None is a claim-verdict change.

1. **`corpus/knowledge/mutation-case-kumitate-sources-check.md:215-216`** (§6 Limits): "Registry and corpus obligations (L1, not done here): S008 is `queued` with `used-by —`; citing it here needs the L1 to mine it and set used-by." At `21e7932` and `4b7c682`, S008 is `mined` with used-by set (#14). R18-2 names only line 1, so this sentence is still uncorrected. Also the "need this entry added to used-by" clause for S001/S052/S056/S057 is now satisfied (#15).
2. **`corpus/knowledge/guard-kill-closure.md:99`** (§5): "`GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` are sourced to git(1) S063 once its anchor is widened (§5)." At `4b7c682`, the S063 row contains `ENVIRONMENT VARIABLES` text (line 72 of `SOURCES.md`, grep output in the session). The widening is recorded as done, so the future tense is stale. Also: S063's used-by at `4b7c682` lists only `corpus/lessons/round-17.md`, not `guard-kill-closure.md`. That is a SOURCES used-by gap for the kumitate-side registry; route it, do not edit the registry from this seat.
3. **`corpus/knowledge/guard-kill-closure.md:133`** (§7): "The subreaper page is row S068 once B13 installs it." S068 exists at `4b7c682` with used-by `corpus/knowledge/guard-kill-closure.md` (#15 family grep). The future tense is stale.
4. Optional, same family: **`guard-kill-closure.md:3`** recheck line says `--rev <branch tip>`. R18-1 itself warns against an unpinned branch-tip claim ("do not replace them with an unpinned `<branch tip>` claim"). The recheck line is an instruction rather than a claim; I leave it to the lane's judgement.

## 4. Optional append-only addenda (draft prose, not applied)

Use only if the lane chooses to close §3 items; the existing R18-1 and R18-2 stay unchanged. Each addendum must be appended at the end of its file, with the date and round named.

### For `corpus/knowledge/guard-kill-closure.md` (append after the R18-1 block)

```
## Erratum R18-1a — residual future-tense statements (2026-10-21, round 19)

This correction supersedes two statements in the body that R18-1 did not name.
Line 99 (§5) says `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` are sourced to S063
"once its anchor is widened". The S063 row at `4b7c682` already carries the
ENVIRONMENT VARIABLES anchor text, so the widening is done. Line 133 (§7) says the
subreaper page is row S068 "once B13 installs it". Row S068 exists at `4b7c682`.
Verify both with that revision's `corpus/SOURCES.md`, not with this entry alone.
```

### For `corpus/knowledge/mutation-case-kumitate-sources-check.md` (append after the R18-2 block)

```
## Erratum R18-2a — unnamed S008 status in §6 (2026-10-21, round 19)

This correction supersedes the §6 Limits sentence beginning "Registry and corpus
obligations (L1, not done here): S008 is `queued` with `used-by —`". R18-2 named
only line 1. At `4b7c682`, `corpus/SOURCES.md` lists S008 as `mined` with this
entry in used-by, and S001, S052, S056 and S057 also list this entry in used-by.
The "needs the L1 to mine it" and "need this entry added to used-by" obligations
are therefore satisfied as recorded in ER8-1.
```

## 5. Proposed disposition for C1 accounting

- Defect 1 (guard-kill line 2): durably corrected at `21e7932` by R18-1; verified accurate by #5–#12.
- Defect 2 (mutation-case line 1): durably corrected at `21e7932` by R18-2; verified accurate by #14–#15.
- Residual same-class items §3.1–§3.3: not corrected; drafts in §4 if the lane adopts them.
- Measured here: 2 of 2 knowledge metadata defects with committed, append-only, revision-pinned corrections (baseline 0 of 2). Not measured here: defects 3–5, and any aggregate 5/5 claim.

## 6. Limits of this seat

- Read-only against the repo, from the committed tree at `21e7932` plus clean working-tree status for the two knowledge files. I did not run any lane gate, selftest, or the defect-probes tool; receipts were checked as bytes and counts, not re-executed.
- The `4b7c682` checks used committed blobs (`git show`), not the working tree.
- The registry "held" arithmetic is from the receipt JSON as committed; I did not re-run `registry-check`.
- Quotations: none quoted beyond short tokens from the repo; no external sources opened.
- Installs: none.
