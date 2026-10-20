# S072 — row draft (B08SrcJjWorkingCopy, round 18 wave 1)

Decision: **REJECTED** (not a duplicate). Provisional id S072; L1 assigns the final id (`SOURCES.md` lists S065 as next unused).

## Duplicate check

`grep -c 'docs.jj-vcs.dev/latest/working-copy' tameshi-shokunin/corpus/SOURCES.md` → `0`.
The purpose-bearing row already in the registry is S061 (`https://docs.jj-vcs.dev/latest/git-compatibility/`), a different URL. It is not a duplicate.

## Registry row

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S072 | Working copy (Jujutsu docs) — https://docs.jj-vcs.dev/latest/working-copy/ | docs | A | jj working-copy snapshot, conflict, ignore, workspace and stale-copy semantics (not colocated Git HEAD) | §Introduction ¶1 (`#introduction`) and §Stale working copy @ latest docs page (mkdocs-material 9.6.23 build; version unstated), fetched 2026-10-20 | REJECTED: the page defines working-copy snapshotting and stale-copy recovery but says nothing about colocated Git HEAD or bookmarks (zero article-body hits for colocat, HEAD, bookmark); the HEAD-versus-branch-tip claim stays with S061; flip: an official jj page stating what a colocated Git HEAD points at relative to the working-copy commit or a bookmark | rejected | 2026-10-20 | 180d | — |

## Gate

- URL: https://docs.jj-vcs.dev/latest/working-copy/
- Access date: 2026-10-20. `curl -sSL --max-time 30 <URL>` → exit 0, 47,694 B HTML; the `read` tool returned the same text.
- Section / anchor: §Introduction, paragraph 1 (`#introduction`), page "Working copy - Jujutsu docs".
- Verbatim quote (18 words; the source line break is joined with one space): "The working copy is where the current working-copy commit's files are written so you can interact with them."
- Word count: 18 (`len(q.split())`), within the 25-word cap. Quote present in the article text after whitespace normalisation (`q in txt` → True).
- Grounding: the quote fixes the page's scope as the working copy's files. It is the only sentence that touches the working-copy commit, and it does not reach Git HEAD.

Negative-claim sweep (the "absent from the page" claim):
- Article body (`<article>` extracted, whitespace-normalised, 1,048 words): `colocat` 0, `HEAD` 0, `bookmark` 0, `Git HEAD` 0.
- Raw-text grep (`sed -e 's/<[^>]*>//g' | grep -n -i -E 'git|colocat|HEAD|bookmark'`): the only body hits are `.gitignore`, `$XDG_CONFIG_HOME/git/ignore` and `$GIT_DIR/info/exclude` (ignored-files section). Sidebar navigation links "Bookmarks" and "Git compatibility" are not body content.
- Section ids on the page: `introduction`, `conflicts`, `ignored-files`, `workspaces`, `stale-working-copy`. None covers colocated Git.

Used-by is `—`: a rejected row is cited by no knowledge entry. The provisional path (`corpus/knowledge/` or `.ufo/evidence/round-18/`) applies only if the flip condition is met.
