# ReopenRejected — S067 / S071 re-opened at 01d586d

**Verdict: holds** — both REJECTED reasons reproduce on the live pages, and both flips are
concrete; two flip-wording defects remain (S067 clause 2 is a routing note already true via
S068; S071's flip is not URL-scoped and is already satisfied by S061's page). No row reopens
today.

## Register under test

`corpus/SOURCES.md` at `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`
(sha256 `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37`):

- **S067** — `corpus/SOURCES.md:76` — prctl(2), status `rejected`, used-by `—`.
- **S071** — `corpus/SOURCES.md:80` — jj Working copy, status `rejected`, used-by `—`.
- Cross-referenced rows at the same rev: **S068** `corpus/SOURCES.md:77`
  (PR_SET_CHILD_SUBREAPER(2const), `mined`) and **S061** `corpus/SOURCES.md:70`
  (Git compatibility, `mined`).
- No register drift while this seat ran: `git -C … diff --stat 01d586d HEAD -- corpus/SOURCES.md`
  printed nothing, exit 0 (git HEAD carries the same SOURCES.md bytes, checked
  2026-10-20T20:30Z).

Flip semantics come from the register's contract:
`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:34-35` —
"Rejected rows read `REJECTED: <reason>; flip: <what would change the verdict>`."
The contract is cited by bare name in `corpus/SOURCES.md:4` and is **not** in the lane tree at
01d586d (`git ls-tree -r --name-only 01d586d | grep -i contract` finds none); the fleet copy
above is the only one on disk (`find /home/vgpnk/Projects/shokunin -maxdepth 6 -name
'SOURCES-CONTRACT*'`).

## S067 — prctl(2)

### Live page

`curl -sS https://man7.org/linux/man-pages/man2/prctl.2.html` — exit 0, HTTP 200, 26266 bytes,
sha256 `ef698f6c5aab0224e9bf238ea1820160797c15d0adcee8b37fcaac7297866810`,
`Last-Modified: Thu, 08 Oct 2026 17:39:35 GMT`.

Page self-identifies as man-pages 6.19: footline `Linux man-pages 6.19 2026-02-08 prctl(2)`
(`$W/prctl.html:237`); COLOPHON names `man-pages-6.19.tar.gz`, HTML rendered 2026-09-09
(prctl.html:227-230). The row's anchor ("man-pages 6.19, page footer 2026-02-08") matches
exactly, and the bytes predate the row's 2026-10-20 fetch, so the recheck reads the same
revision.

### REJECTED reason — holds

- §DESCRIPTION opens at `prctl.html:80`. The operation list names
  `PR_SET_CHILD_SUBREAPER` and `PR_GET_CHILD_SUBREAPER` as bare entries
  (`prctl.html:91-92`); the list runs through `PR_FUTEX_HASH` and the page goes straight to
  §RETURN VALUE and §ERRORS — no per-operation prose anywhere.
- `grep -qi 'nearest still living ancestor' prctl.html` → **exit 1** (phrase absent).
- `grep -ciE 'reparent|orphan' prctl.html` → **0** (exit 1).
- All 10 `subreaper` occurrences (`grep -o -i | wc -l`) sit in the operation list, the
  §SEE ALSO entry (`PR_SET_CHILD_SUBREAPER(2const)` at `prctl.html:190`), or sidebar links
  (`prctl.html:262,287`) — names only, no rule.

→ "lists PR_SET_CHILD_SUBREAPER by name and states no reparenting rule" is true of the live
bytes.

### Flip — concrete; one clause is not a trigger

Row text: "flip: this URL's text states the nearest-living-ancestor reparenting rule in a
revision, or the rule is cited from PR_SET_CHILD_SUBREAPER(2const) under its own row (see S068)".

- **Clause 1 is executable and false today**: the exact rule language is absent from this URL,
  so the URL-scoped test is unambiguous (grep above).
- **Clause 2 cannot change this row's verdict**: the 2const page already carries the rule —
  "…that process will be reparented to the nearest still living ancestor subreaper"
  (`$W/subreaper2const.html:87-88`, same man-pages 6.19 / footline 2026-02-08, sha256
  `b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c`) — and S068 is already
  `mined` at the read rev (`corpus/SOURCES.md:77`). Read literally as an alternative flip
  trigger, clause 2 is **already true**, which would contradict status `rejected`.
- Contract v1 defines the field as a single "<what would change the verdict>" (`…:34-35`);
  clause 2 is a routing note (the rule stays under S068's row), not a verdict change.

Recommendation: drop clause 2 from the flip or fold it into clause 1 — "a revision of this
URL states or cites the rule from PR_SET_CHILD_SUBREAPER(2const) (the rule itself remains
S068)". **Reopen now: no.**

## S071 — jj Working copy

### Live page

`curl -sS https://docs.jj-vcs.dev/latest/working-copy/` — exit 0, HTTP/2 200, 47694 bytes,
sha256 `947d0c56c02f9c10b4c14e8aaa8cc3f435f7650536ab9386ef6a52f1d64ff3c7`; ETag only, no
`Last-Modified`. Canonical `https://docs.jj-vcs.dev/latest/working-copy/`; generator
`mkdocs-material-9.6.23`; version config `{"alias": true, "provider": "mike"}` and no `0.4x`
version string anywhere in the page → the row's "mkdocs-material 9.6.23 build; version
unstated" holds.

### REJECTED reason — holds

Article body = `<article>` inner HTML, tags stripped and entities unescaped (6467 chars).
Headings present: `working-copy`, `introduction` (`$W/jjwc.html:2000`), `conflicts`,
`ignored-files`, `workspaces`, `stale-working-copy` (`jjwc.html:2078`) — exactly the scope's
five sections.

- Body counts: `colocat` **0**, `HEAD` **0**, `bookmark` **0** (`grep -qi` exits 1 for each).
- Whole-page hits are chrome only: 3 `bookmark` occurrences = `<link rel="next"
  href="../bookmarks/">` + nav link + nav label "Bookmarks"; 29 `HEAD` occurrences =
  `<head>`/`</head>`/`md-header*` components. None is article prose.
- §Introduction ¶1 defines the working copy and automatic commit of changed files; §Stale
  working copy gives stale detection, `jj workspace update-stale`, and the recovery commit —
  matching the row's "defines working-copy snapshotting and stale-copy recovery".

→ "zero article-body hits for colocat, HEAD, bookmark" is exact.

### Flip — concrete but mis-scoped and already satisfied

Row text: "flip: an official jj page stating what a colocated Git HEAD points at relative to
the working-copy commit or a bookmark".

- The statement is concrete and exists on an official jj page: §Colocated Jujutsu/Git
  workspaces ¶2 — "jj commands will usually put the Git repo in a "detached HEAD" state…"
  (`$W/jj-gitcompat.html:2235`) — plus §Converting a workspace into a colocated workspace
  recipe comment "# Convince jj to update .git/HEAD to point to the working-copy commit's
  parent" (`jj-gitcompat.html:2319`). Fetched 2026-10-20: HTTP 200, 61334 bytes, sha256
  `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254`.
- That page is already **S061** (`corpus/SOURCES.md:70`, `mined`, fetched 2026-10-20), whose
  teaches states exactly "jj leaves Git detached at the working-copy commit's parent, so
  `git rev-parse HEAD` is not the bookmark tip". So the flip's literal subject ("an official
  jj page") is **already true at the read rev**; only the URL-scoped reading ("this page") is
  false today, and only that reading changes this row's verdict (contract v1:34-35).
- The row's own teaches already says "the HEAD-versus-branch-tip claim stays with S061"; the
  flip as written would therefore duplicate S061 instead of flipping S071.

Recommendation: replace with "a revision of this URL states what a colocated Git HEAD points
at relative to the working-copy commit or a bookmark". **Reopen now: no**; no new row is
needed — S061 already carries the statement.

## Falsification result

- **F1 (S067)** — reason holds; flip concrete in clause 1; clause 2 is already true via S068
  and is not a verdict condition. Non-blocking wording defect; tighten before the 180d recheck.
- **F2 (S071)** — reason holds; flip concrete but already satisfied off-URL by S061's page, so
  it cannot serve as a reopening test for this row. Needs URL scoping.
- **F3 (common)** — both flip fields contain a clause that does not change this row's verdict
  and is already true at the read rev; contract v1 asks for a single "<what would change the
  verdict>".
- Non-blocking observation: `prctl.html` `Last-Modified` 2026-10-08 postdates its COLOPHON
  render date 2026-09-09 while still declaring man-pages 6.19 / 2026-02-08 [INFERENCE: site
  re-render/touch]; the version anchor still matches, so the row is unaffected.

## Commands and exits

| command | exit | result |
|---|---|---|
| `curl -sS -o prctl.html https://man7.org/linux/man-pages/man2/prctl.2.html` | 0 | HTTP 200, 26266 B, sha256 ef698f6c… |
| `curl -sS -o jjwc.html https://docs.jj-vcs.dev/latest/working-copy/` | 0 | HTTP 200, 47694 B, sha256 947d0c56… |
| `curl -sS -o jj-gitcompat.html https://docs.jj-vcs.dev/latest/git-compatibility/` | 0 | HTTP 200, 61334 B, sha256 db9c9a76… |
| `curl -sS -o subreaper2const.html https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html` | 0 | HTTP 200, 9879 B, sha256 b805fe23… |
| `grep -qi 'nearest still living ancestor' prctl.html` | 1 | phrase absent |
| `grep -ciE 'reparent\|orphan' prctl.html` | 1 | 0 |
| `grep -qiE 'colocat\|bookmark' jjwc-body.txt` | 1 | absent |
| `grep -qi HEAD jjwc-body.txt` | 1 | absent |
| Python `<article>` extraction + counts | 0 | body 6467 chars; colocat 0, HEAD 0, bookmark 0 |
| `grep -o -i subreaper prctl.html \| wc -l` | 0 | 10, all name/link positions |
| `grep -n 'Convince jj' jj-gitcompat.html` | 0 | line 2319 |
| `git show 01d586d:corpus/SOURCES.md \| sha256sum` | 0 | 1d4b5910… |
| `git diff --stat 01d586d HEAD -- corpus/SOURCES.md` | 0 | empty |

Scratch: `/tmp/tameshi-r18w2-ReopenRejected-MO8l8D` (`$W` above). No tools were installed or
upgraded. No writes outside this report.

## Inputs and hashes

- `corpus/SOURCES.md` @ 01d586d — sha256 `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37`
- `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` — sha256
  `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119`
- Live URLs and their sha256 are listed above; line anchors are into the fetched copies.

## Unresolved

- The contract copy used for F3 is the fleet file named under "Register under test"; SOURCES.md
  cites it by bare name and the lane tree at 01d586d has no such file. If a different copy is
  authoritative, F3's citation weakens, but the ambiguity findings stand on the row text alone.
- No blockers.

**Verdict: holds** — both REJECTED reasons reproduce on the live pages and both flips are
concrete; S071's flip is already satisfied by S061's official page and must be URL-scoped, and
S067's second flip clause should be dropped or folded into the first.
