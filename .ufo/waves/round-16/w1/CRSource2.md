# CRSource2 — C2 source report (doctest docs)

Seat: `TameshiR16.CRSource2` · Lane: tameshi-shokunin · Round 16, wave 1 · Leaf (no dispatch, no commits, no SOURCES.md edit).

## Behavior

Opened the Python doctest documentation page, recorded the access date, the version the page shows, and a ≤25-word exact quote with its location about checking that documentation examples still work as written. Drafted one `corpus/SOURCES.md` row (not written to that file). Nothing in the lane was modified.

## Evidence

### Source identity

| Field | Value | Evidence |
|---|---|---|
| URL | https://docs.python.org/3/library/doctest.html | `curl -sSfL -o doctest.html -w 'http=%{http_code} final=%{url_effective}\n'` → `http=200 final=https://docs.python.org/3/library/doctest.html` |
| Access date | 2026-10-20 (UTC) | `date -u +%Y-%m-%d` → `2026-10-20` |
| Version shown | Python 3.15.0 documentation | HTML `<title>` at `doctest.html:20`: `… — Python 3.15.0 documentation`; also `doctest.html:34` (search label) |
| Local interpreter (context only) | Python 3.14.8 | `python3 --version` → `Python 3.14.8`. The docs page is 3.15.0; the host interpreter is not the doc version. Not used as evidence. |
| Snapshot | sha256 `c734a569181d02f966d97a89dc120fe9e05f62e119e871880e813904840f46d6` | `sha256sum` over the fetched raw HTML, kept at `/tmp/tameshi-r16-CRSource2-x/doctest.html` |

### Quote and location

Quote (18 words, exact):

> To check that a module’s docstrings are up-to-date by verifying that all interactive examples still work as documented.

Location: module introduction, first bullet of the three-bullet list that follows "The `doctest` module searches for pieces of text…". In the raw HTML it spans `doctest.html:249–250` (`sed -n '245,252p'` output shows `<li><p>To check that a module’s docstrings are up-to-date by verifying that all` at 249 and `interactive examples still work as documented.</p></li>` at 250). Rendered-reader output shows the same bullet under the module heading, before "Simple Usage: Checking Examples in Docstrings". The quote is split across a line break in the HTML; the words are identical after joining with a space.

Corroborating sentence in the same intro (reader output, not in the quote budget): "…executes those sessions to verify that they work exactly as shown." (raw HTML `doctest.html` lines 246–247, same `<p>` block; the phrase wraps across the line break, so a single-line grep for "work exactly as shown" misses the body and only hits the meta tags at lines 11, 15, 16).

Check of the 25-word limit: the quote is 18 words, within the ≤25 limit. Verified with `python3` word split on the joined line.

### Commands and exits

| Command | Exit | Key output |
|---|---|---|
| `curl -sSfL … doctest.html` | 0 | `http=200 final=https://docs.python.org/3/library/doctest.html` |
| `sha256sum doctest.html` | 0 | `c734a569…46f6` |
| `grep -n 'docstrings are up-to-date' doctest.html` | 0 | `249: <li><p>To check that a module’s docstrings are up-to-date by verifying that all` |
| `grep -n 'still work as documented\|work exactly as shown'` | 0 | `250: interactive examples still work as documented.</p></li>`; the 'exactly as shown' hits at lines 11, 15, 16 are meta tags only, body wording wraps at lines 246–247 |
| `grep -n -o 'Python 3\.[0-9]*\.[0-9]* documentation'` | 0 | `Python 3.15.0 documentation` (lines 20, 34) |
| `date -u +%Y-%m-%d` | 0 | `2026-10-20` |
| `python3 --version` | 0 | `Python 3.14.8` (context only) |
| `python3` join-and-match over lines 249–250 | 0 | `exact 18` (quote found verbatim in the joined text; the single-line segment alone does not contain the full quote because it wraps) |

No tool was installed or upgraded. Tooling record: none.

### Lane context read (no edits)

- `corpus/SOURCES.md:10–11`: registry table header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (11 columns, no `|` inside cells per the contract).
- `corpus/SOURCES.md:172`: `- Next unused id: S052.`
- Existing docs rows with the same host: `S049` (`corpus/SOURCES.md:58`, Python subprocess docs, Python 3.15.0 served 2026-10-20). S052 is a separate doctest row; no duplicate of S049.
- Contract: `./.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26–30` (tier A = primary/authoritative for scope: spec, official docs, source code, original paper, maintainer statement, the lane's own re-runnable gate output). `:34–35` (`teaches` = one grounded learner benefit). `:45–48` (Rule 1: round lesson `## Gate` records URL, access date, and ≤25-word quote with location). `:22` (id is next unused, never reused).
- Discrepancy (minor, not blocking): `corpus/SOURCES.md:4` says the contract is `SOURCES-CONTRACT-v1.md`; the file exists at `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, not at lane root or `corpus/`. A bare path lookup fails. Recorded for the lane; no edit made.
- `CORPUS.md` referenced by round-15 audit notes is not at the lane root (`grep` on `tameshi-shokunin/CORPUS.md` → exit 2, no such file); the fleet-root copy at `./CORPUS.md` was not opened because it is outside this target.

## Draft SOURCES.md row (not written)

Id is `S052` (next unused, `corpus/SOURCES.md:172`). Row must be inserted by the single owner (L1) when it admits the row. Draft:

```
| S052 | doctest — Test interactive Python examples — https://docs.python.org/3/library/doctest.html | docs | A | executable documentation examples: checking that documented interactive examples still run as written | module introduction, first bullet of the three-bullet list (raw HTML lines 249–250) @ Python 3.15.0 documentation, page fetched 2026-10-20 | a reader can execute the interactive examples in documentation and check each against its shown output, so the prose claim that an example works becomes a checkable claim | queued | 2026-10-20 | on-release | — |
```

Cell checks: 11 cells, no `|` inside any cell (verified by eye: only the 10 separators plus leading/trailing pipes). `kind` `docs` is in the contract enum. `tier` `A` is the official docs for the stated scope. `status` `queued` because no `used-by` path cites it yet (`mined` requires ≥1 `used-by` path, contract `:36`). `recheck` `on-release` matches the versioned docs (3.15.0 shown); a `365d` cadence would be equally defensible — the choice is the row owner's.

Learner benefit for the SKILL cold-read: a cold reader can run a documented example and compare its output with the one printed in the page, rather than trusting the prose. The page's own words support this: "…executes those sessions to verify that they work exactly as shown" (intro, same block as the quote).

## Findings

1. Quote and access date are grounded: URL returns HTTP 200, version shown is 3.15.0, quote is an exact 18-word match at `doctest.html:249–250`.
2. The row is draftable as `S052`, tier A, kind `docs`, scope `executable documentation examples`, status `queued` until a `used-by` path exists.
3. Lane doc drift: `corpus/SOURCES.md:4` names `SOURCES-CONTRACT-v1.md` without its real path (`.ufo/waves/kaika/`). Minor.

## Recommendations (bounded)

- L1 admits S052 only if a SKILL cold-read or knowledge entry cites it; otherwise leave it `queued` with `used-by` `—`.
- Record the URL, access date `2026-10-20`, and the 18-word quote with `doctest.html:249–250` in the round lesson `## Gate` (contract Rule 1); this report is the source for that entry.
- Optionally correct the `corpus/SOURCES.md:4` contract path in the next lane edit by the owner of that file. Not done here.

## Opened paths

- https://docs.python.org/3/library/doctest.html (reader and raw fetch)
- `/tmp/tameshi-r16-CRSource2-x/doctest.html` (scratch copy, sha256 above)
- `corpus/SOURCES.md` lines 1–33, 58–60, 172 (read/grep)
- `corpus/README.md` (grep only, tier/kind search; no tier definition there)
- `./.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` lines 16–63 (contract rules)
- `./CORPUS.md` (existence check only; not opened)

## Out of scope / not done

- No edit to `corpus/SOURCES.md`, SKILL.md, SCORECARD.md, LOG.md, SHONEN.md, PROVINCE.md, QUALITY.md, README.md, or any sibling repo. No commits.
- No cold-read of SKILL.md (that is the CR* seats' job; this seat's target is the source row only).
- No messages sent (no blockers; no interface-critical detail).
