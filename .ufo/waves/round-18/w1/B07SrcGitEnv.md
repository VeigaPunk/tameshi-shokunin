# B07SrcGitEnv — S071 source row draft (round 18, wave 1)

Verdict: **built** — one row drafted and admitted as a draft (provisional id S071, tier B, status `mined` as dispatched); not a duplicate, not rejected.

## Scope
- Target: frontier step for C2 P11 / R17-GIT-ENV (GIT_DIR / GIT_WORK_TREE / GIT_INDEX_FILE vs repository discovery).
- Owned write: `.ufo/waves/round-18/sources/S071-B07SrcGitEnv.md` (row, Gate, duplicate sweep).
- Report write: this file (`.ufo/waves/round-18/w1/B07SrcGitEnv.md`, per the Report line).
- No lane file edited; no git write; no subagent; no install (pacman paused; no tool was needed — `read`, `grep`, `awk`, `wc`, `grep -o`, `od` were enough).

## Commands and results
1. Read `CORPUS.md` § "SOURCES.md — where a shokunin learns" and `corpus/SOURCES.md` (contract v1 shape, 13-column row, kinds/tiers/status enums, rules 1–6, census commands). Result: rows S001–S064 present; § Id allocation says next unused id S065.
2. Opened `https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables` with `read`. Result: HTTP text, 371 lines; §10.8 "Environment Variables", subsection "### Repository Locations" (2nd edition) is in the first 300 lines. No mirror needed.
3. Duplicate sweep: `_grep` for `git-scm\.com|Environment-Variables|GIT_WORK_TREE|GIT_INDEX_FILE` over `corpus/SOURCES.md`. Result: no `git-scm.com/book` row; hits only S061, S062, S063 (other URLs). Verdict: not a duplicate.
4. Quote byte check: `grep -o "If this isn.t specified, Git walks up the directory tree" artifact://85088 | od -c` → bytes `342 200 231` at the apostrophe, i.e. U+2019 as in the draft. `grep -c "" artifact://85088` → 371.
5. Quote word count: `printf '%s' "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree" | wc -w` → **18** (limit 25).
6. Row shape: `awk -F'|' '/^\| S071 \|/ {…}'` → `NF=13`, `tier=B`, `status=mined`; exit 0.
7. `used-by` path check: `test -e .ufo/evidence/round-18` → exit 0 (directory exists; holds `census-start.txt`).

## Gate evidence
- URL: https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables — access 2026-10-20.
- Anchor: §10.8 Environment Variables › Repository Locations (2nd ed.).
- Quote (18 words, verbatim): "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree"
- Supports: the default repository discovery (upward walk) that a GIT_DIR export overrides, the premise of P11.

## Findings and caveats
- Tier B (textbook), not A. The normative statement of the same variables is S063 (git(1), 2.56.0 docs, A); S071 corroborates and adds two lines S063's teaches cell does not name: with GIT_DIR and no work-tree override the cwd is the working-tree top level; GIT_INDEX_FILE applies to non-bare repositories only. The book text reads: "If `--git-dir` or `GIT_DIR` is specified but none of `--work-tree`, `GIT_WORK_TREE` or `core.worktree` is specified, the current working directory is regarded as the top level of your working tree." [INFERENCE: the P11 fixture should cite S063 for the override rule and S071 only as corroboration.]
- Id conflict: the dispatch's provisional S071 differs from the contract's next unused S065; sibling drafts already use S065 (`S065-B01SrcStrykerStates.md`) and S076 (`S076-B12SrcSubprocess.md`). The L1 allocates the final id.
- Status conflict: the dispatch asked for `mined`, but the contract defines `mined` as cited by at least one `used-by` path. The `used-by` value is a directory placeholder (`.ufo/evidence/round-18/`); the census's `mined` check passes only because the directory exists. The L1 should replace it with the citing file and confirm `mined` (or set `queued` until cited).
- Not run: the full `corpus/SOURCES.md` census (`scripts/sources-census.sh` / the manual awk lines) — the row is not yet appended to the registry, so the census would not see it. The L1 applies the row and runs the census.

## Out-of-scope items
- Appending the row to `corpus/SOURCES.md` (not my file; the L1 installs it).
- Writing the citing knowledge entry or P11 note (`used-by` target).
- Tool installs or upgrades: none.

## Artifact paths
- `.ufo/waves/round-18/sources/S071-B07SrcGitEnv.md` (row + Gate + duplicate sweep)
- `.ufo/waves/round-18/w1/B07SrcGitEnv.md` (this report)

Final: built — S071 draft row admitted (tier B, mined as dispatched; id and used-by for L1 decision).
