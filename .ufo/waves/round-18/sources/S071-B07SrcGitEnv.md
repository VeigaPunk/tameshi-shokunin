# S071 draft — B07SrcGitEnv (round 18, wave 1)

Decision: **ADMIT as draft row** (`mined`, provisional id S071). Not a duplicate: no `git-scm.com/book` URL exists in `tameshi-shokunin/corpus/SOURCES.md` (grep sweep, 2026-10-20, Gate below). Not rejected: the page carries the repository-location definitions the C2 P11 probe rests on.

## Row (13 cells, provisional id)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S071 | Pro Git, 2nd ed., §10.8 Environment Variables — https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables | book | B | GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE as repository-location overrides; secondary to the normative S063 | §10.8 Environment Variables, subsection Repository Locations @ 2nd-edition page, fetched 2026-10-20 (page version and last-modified not shown) | GIT_DIR names the .git folder and, when unset, git walks up parent directories; with GIT_DIR set and no work-tree override the cwd is the top level of the working tree; GIT_INDEX_FILE relocates the index for non-bare repositories only | mined | 2026-10-20 | 180d | .ufo/evidence/round-18/ |

Notes on the row:
- Tier B, not A: a textbook is strong secondary under the SOURCES tier rule. The normative statement of the same variables is S063 (git(1), Git 2.56.0 docs, tier A); S071 corroborates it and adds the cwd-as-top-level and GIT_INDEX_FILE lines that S063's teaches cell does not name.
- `used-by` is provisional: `.ufo/evidence/round-18/` is a directory, which the census `[ -e ]` check accepts. The L1 replaces it with the citing file path (for example the P11 probe note or a `corpus/knowledge/` entry) when it lands the citation.
- `mined` is the status the dispatch asked for. The contract defines `mined` as cited by at least one `used-by` path; until a citing file exists, the L1 should decide `queued` versus `mined`. The `mined rows whose used-by paths do not exist` census prints `missing:` for a path that is not yet written.
- Id: the dispatch names S071 as provisional. `SOURCES.md` § Id allocation says the next unused id is S065, and sibling drafts in `.ufo/waves/round-18/sources/` already use S065 and S076. The L1 allocates the final id.

## Gate (round-lesson form, rule 1)

- URL: https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables
- Access date: 2026-10-20 (read tool, HTML converted to text; 371 lines, the Repository Locations section lies within lines 1–300).
- Anchor: §10.8 Git Internals — Environment Variables, subsection "Repository Locations" (2nd edition).
- Quote (18 words; emphasis markup removed; apostrophe is U+2019 as printed, confirmed by byte check on the fetched body):
  > GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree
- Word count: `printf '%s' "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree" | wc -w` → 18.
- Why it grounds the purpose: the quoted sentence states the default repository discovery (upward walk) that a GIT_DIR export replaces. The companion sentences cover GIT_WORK_TREE and GIT_INDEX_FILE but are not quoted here, to stay within 25 words.

## Duplicate sweep

Command: `grep -nE 'git-scm\.com|Environment-Variables|GIT_WORK_TREE|GIT_INDEX_FILE' tameshi-shokunin/corpus/SOURCES.md`, 2026-10-20.
Result: no `git-scm.com/book` row. Hits are S061 (jj docs), S062 (git-rev-parse docs, `git-scm.com/docs/git-rev-parse`) and S063 (git(1) docs, `git-scm.com/docs/git`), none of which is this URL. Verdict: not a duplicate; proceed.
