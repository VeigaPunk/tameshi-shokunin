done — SOURCES contract checklist, next ID, duplicate rules, and search-log template.

## Checklist for this round’s source rows

- [ ] Allocate **S079** as the next unused ID; IDs are append-only and never reused. S038–S039 were retired and remain gaps. The registry currently ends at S078; its Id allocation footer also says S079 (and the round-20 note retains that next ID).
- [ ] Open each proposed source in the round that writes its row. In the round lesson’s `## Gate`, record that row’s canonical URL, access date, and an exact located quote of at most 25 words grounding `teaches` (identify its section/page/line and revision or publication date as applicable). A correction is a new row whose `teaches` begins `supersedes S0NN —`; do not rewrite immutable cells of the prior row.
- [ ] Add the row under `## Registry` using the 11 defined columns: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`. `source` is a title plus canonical URL or DOI (repo path/command for `own-work`); `scope` names the claim/topic; `teaches` states one grounded learner benefit (a rejection gives its reason and flip condition). Use an allowed `kind` (`spec`, `docs`, `paper`, `code`, `tool`, `dataset`, `talk`, `book`, `community`, `own-work`); tier A/B/C scoped to the stated scope (community cannot be A); status `queued|mined|rejected`; ISO opened date; valid ISO date, cadence such as `90d`/`180d`, or symbolic recheck. Give an exact anchor, not a bare homepage. No cell may contain `|`.
- [ ] Use `queued` for an opened source worth mining; `mined` only when at least one `used-by` path cites it; `rejected` rows retain the reason and the condition that would flip the verdict. Put repo-relative knowledge/lesson paths in comma-separated `used-by`, or `—`. Add a path to `used-by` only when the citing entry exists; validator E11 checks mined-row paths on disk. Add an ordered `## Paths` sequence when recording a study path; leads remain bullets under `## Leads (unopened)`, not registry rows.
- [ ] Add one Search log note for each bounded search, with the fields below. Keep the count/exclusion basis and stop rationale explicit; a negative claim must carry its sweep.
- [ ] For any in-place metadata change, change only `status`, `recheck`, and/or `used-by`; in the lesson’s `## Gate`, name the row and record each changed cell as exact old → new. State unchanged mutable fields and that immutable cells were not edited. If `status` changes to `mined`, log the accompanying `used-by` addition and ensure its path exists. The round-20 Gate’s S049 old/new `used-by` example is a useful format.
- [ ] Run the read-only lane validator and report its warnings separately from errors. Existing W04 warnings do not make validation fail by themselves.

## Duplicate URL behavior (maintained census)

`scripts/sources-census.sh` extracts the first `http://` or `https://` URL in the source cell, removes a fragment and one trailing slash, removes the scheme, and lowercases the portion before the first `/` (or the entire remaining value when there is no slash). The path is not lowercased. It does not perform broader URL canonicalization. Comparisons use this normalized URL and the trimmed scope.

- **W04 warning:** a normalized URL already present under a different scope. It is advisory and does not change a clean validation exit code. It may also appear for rejected or superseding rows because the W04 check is independent of status and the `supersedes` exemption.
- **E04 error:** a repeated normalized URL in the same scope when a prior row in that URL/scope group is non-rejected, the current row is not `rejected`, and the current `teaches` does not contain `supersedes S` followed by at least three digits. The rejected-row exemption is pairwise/stateful: a rejected row alone does not trigger E04; after a non-rejected row exists in the group, a later non-rejected duplicate without `supersedes` does. A same-scope correction with the required `supersedes S0NN` text is exempt from E04.

The current registry produced W04 for S047, S048, S075, S076, S077, and S078 (reused URLs across distinct scopes); the validator still exited 0. These are warnings, not duplicate-ID or same-scope E04 findings.

## Search-log template

```markdown
- YYYY-MM-DD — **<bounded search name>**. Question/query: <the question and query terms>. Where searched: <sources, indexes, canonical URLs, repositories, or bounded corpus; include method/date as useful>. Identified <n> · screened <n> · included <n> (<what was included, including row IDs if any>) · excluded <n> (<reasons, with counts or item references>). Stop rationale: <why this bounded search answers the question; note any unexhausted scope or inaccessible sources>. <If applicable: source-row/status/recheck/used-by changes are recorded in the round lesson’s `## Gate`.>
```

## Evidence and checks

- `/home/vgpnk/Projects/shokunin/CORPUS.md:64-129` — frozen SOURCES v1 Shape and Rules: row fields and tier/status meanings; rule 1 Gate quote requirement; rule 2 append-only mutable fields and old→new logging; rule 5 search-log fields and negative-claim sweep.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` — Registry currently has S001–S037 and S040–S078; `## Search log`, `## Leads (unopened)`, and `## Id allocation` document the search-note precedent, retired S038–S039, and next unused S079. The round-20 source reopening records its S049 mutable-cell transition.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:599-605,643-653` — URL normalization and W04/E04 conditions; header lines 24-33 define the validator codes and warning/error distinction. Selftest lines 361-381 cover W04 warning exit and rejected-pair E04 exemption.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-18.md:29-50,104-119` — new-row URL/date/quote table, registry change log, and correction-row Gate addendum. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-20.md:35-40` — explicit old `used-by` → new `used-by`, with status/recheck and immutable cells stated unchanged.

Exact validator command and result:

```text
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-21 /home/vgpnk/Projects/shokunin/tameshi-shokunin
exit=0
```

Output: W04 for S047, S048, S075–S078, followed by `tameshi-shokunin\tok\t/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`. No tools were installed or updated.