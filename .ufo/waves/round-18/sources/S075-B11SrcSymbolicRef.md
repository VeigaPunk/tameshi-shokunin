# S075 (provisional) — git-symbolic-ref: attached vs detached HEAD

Decision: **row drafted, not a duplicate, not rejected.** Purpose: C2 P08 (resolving the branch when HEAD is attached vs detached).

Duplicate check: `grep -n -i "symbolic\|git-scm.com/docs" corpus/SOURCES.md` (lane root, 2026-10-20) returns only S062 and S063 (`git-rev-parse`, `git`); no row carries `git-symbolic-ref`. Registry note `Next unused id: S065` (`corpus/SOURCES.md:122`); id S075 is used as the assignment directs (see Flags).

## Registry row (draft, 13 cells, no `|` inside a cell)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S075 | git-symbolic-ref (Git manual) — https://git-scm.com/docs/git-symbolic-ref | docs | A | git's own definition of reading the symbolic HEAD: which branch it names, and the detached case | §DESCRIPTION (Typically you would give HEAD…), §OPTIONS -q/--quiet, §NOTES exit-status sentence @ git-scm.com manual page, fetched 2026-10-20; page version list runs to 2.56.0, last content change recorded at 2.48.0 | `git symbolic-ref HEAD` names the branch only when HEAD is attached; with -q a detached HEAD exits 1 silently and any other error exits 128, so a P08 resolver must branch on exit 1 rather than treat it as a failed read | mined | 2026-10-20 | on-release | .ufo/evidence/round-18/ |

## Gate

- URL: https://git-scm.com/docs/git-symbolic-ref
- Access date: 2026-10-20 (`read` extraction opened; raw HTML fetched with `curl -sL` exit 0 and the quotes below re-matched in the tag-stripped text).
- Anchor: §DESCRIPTION; §OPTIONS (`-q`, `--quiet`); §NOTES. Revision: manual page as served 2026-10-20; the page's version history reads "2.48.1 → 2.56.0 no changes".
- Quote A — §OPTIONS, `-q` / `--quiet` (24 words, `wc -w` = 24):
  > Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently.
- Quote B — §NOTES, exit-status paragraph (18 words, `wc -w` = 18):
  > with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs.
- Quote C — §DESCRIPTION, attached case (18 words, `wc -w` = 18):
  > Typically you would give HEAD as the <name> argument to see which branch your working tree is on.

Each quote is at most 25 words. Quote A grounds the detached case in `teaches`; quote B grounds the exit codes; quote C grounds the attached case.

## Flags for the L1

1. **Id.** Registry says next unused is S065 (`corpus/SOURCES.md:122`). S075 is the id the assignment names; S065–S074 look reserved for sibling drafts, since sibling file `sources/S076-B12SrcSubprocess.md` exists [INFERENCE]. The L1 confirms or renumbers.
2. **Status `mined`.** The census (`corpus/SOURCES.md:147`) requires each `used-by` path to exist. `.ufo/evidence/round-18/` exists (checked 2026-10-20), but it is a directory, not a citing file. The L1 keeps `mined` only once a knowledge entry or lesson cites S075; otherwise set `queued`.
3. `corpus/SOURCES.md` is not edited by this seat (append-only; the L1 installs the row).
