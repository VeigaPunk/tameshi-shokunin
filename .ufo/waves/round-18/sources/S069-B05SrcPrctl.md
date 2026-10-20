# S069 draft — B05SrcPrctl (round 18, wave 1)

Decision: **REJECTED** for the stated purpose (C2 P10, PR_SET_CHILD_SUBREAPER reparenting). Not a duplicate: no row in `corpus/SOURCES.md` carries the URL or the token `prctl` / `subreaper` (`grep -nE 'prctl|subreaper|SUBREAPER' corpus/SOURCES.md` exit 1, no matches, 2026-10-20).

## Row (provisional id S069; file states next unused id is S065 — L1 to reconcile)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S069 | prctl(2) — Linux manual page — https://man7.org/linux/man-pages/man2/prctl.2.html | docs | A | prctl(2) operation names only; not the semantics of PR_SET_CHILD_SUBREAPER | §DESCRIPTION (operation list, names only) and §SEE ALSO; man-pages 6.19, page footer 2026-02-08; fetched 2026-10-20 | REJECTED: this page lists PR_SET_CHILD_SUBREAPER by name and states no reparenting rule (absence swept, see Gate); flip: this URL's text states the nearest-living-ancestor reparenting rule in a revision, or the rule is cited from PR_SET_CHILD_SUBREAPER(2const) under its own row (see Lead) | rejected | 2026-10-20 | 180d | — |

## Gate

- URL: https://man7.org/linux/man-pages/man2/prctl.2.html
- Access date: 2026-10-20 (read tool; fetched again with `curl -fsSL` into a /tmp scratch dir, 26266 bytes, sha256 prefix ef698f6c5aab0224)
- Section/anchor: §DESCRIPTION, operation list (rendered line 91 of the fetched HTML); §SEE ALSO (lines 190–191 of fetched HTML)
- Verbatim quote (1 word, the only occurrence of the operation in §DESCRIPTION): `PR_SET_CHILD_SUBREAPER`
- Absence sweep (negative claim): `grep -inE 'reparent|orphan|subreaper' prctl2.html | sed 's/<[^>]*>//g'` returned only the operation-name line (91), the operation-name line for GET (92), and two SEE ALSO cross-links (190–191) plus two more link rows (262, 287). No reparenting sentence exists on this page. `grep -ci SUBREAPER` = 6.
- Footer evidence: `Linux man-pages 6.19 2026-02-08 prctl(2)`.

## Lead (opened, NOT drafted as a row here — for L1 to decide, likely S070)

- URL: https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html — opened 2026-10-20 (read tool), same man-pages 6.19 footer.
- Anchor: §DESCRIPTION, first paragraph after the SYNOPSIS.
- Verbatim quote, 23 words (counted with `wc -w` = 23; present once in the fetched page): `When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper.`
- This quote supports the purpose (orphans reparent to the subreaper). A row for it would be `docs`, tier A, scope = PR_SET_CHILD_SUBREAPER reparenting, and its `teaches` would open `supersedes`-free because S069 is rejected, not superseded.
