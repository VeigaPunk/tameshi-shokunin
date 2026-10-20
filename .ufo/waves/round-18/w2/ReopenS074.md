# ReopenS074 — S074 (git-symbolic-ref) re-opened

Seat ReopenS074. Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (2026-10-20).
Lane files were opened with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show
<rev>:<path>` (not from the working tree); the page was fetched today.

## Inputs

| input | sha256 |
|---|---|
| `corpus/SOURCES.md` @ rev | `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` |
| `.ufo/waves/round-18/staged/lesson-round-18-gate.md` @ rev | `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` |
| `corpus/knowledge/guard-kill-closure.md` @ rev | `9312bdebd4e93d427ea32d3db8652f95530237477b49ffecffdf4e4ac49991fb` |
| `.ufo/waves/round-18/sources/S075-B11SrcSymbolicRef.md` @ rev (draft; quotes A–C) | `a9ba0067f21b034c5ac4291a51698e08fdceebafc4283cedd9d408c1fc567bbb` |
| https://git-scm.com/docs/git-symbolic-ref, fetched 2026-10-20 | `d706904473082a0ef07ed8eedd2c4d94be25dac852e58ff3b017048828c38872` |

Tier/kind definitions: `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`.
Note: `corpus/SOURCES.md:4` names `SOURCES-CONTRACT-v1.md`, but no file of that name is in the
lane tree at the rev (`git ls-tree -r --name-only <rev> | grep -i sources-contract` → no lines,
exit 1); the fleet copy above is the one used.

## Row shape

`corpus/SOURCES.md:83`, 13 cells (`awk -F'|'` NF=13). Cells: kind `docs`, tier `A`, status
`mined`, opened `2026-10-20`, recheck `on-release`, used-by
`corpus/knowledge/guard-kill-closure.md`.

Census in a detached clone at the rev, run from the lane root with the contract's own snippets:
rows=72; malformed rows (`NF!=13`)=0; enum violations (kind/tier/status)=0; duplicate ids=0;
mined used-by paths missing on disk=0. Clone/checkout exited 0; `HEAD=01d586ddb…`.

## 1. Gate quote — verified verbatim, 24 words, anchor correct

Installed quote (`.ufo/waves/round-18/staged/lesson-round-18-gate.md:26`, stated location
`(§OPTIONS, -q / --quiet)`):

> Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently.

- Fetch: `curl -sSL … -w 'HTTP=%{http_code} URL=%{url_effective}'` → `HTTP=200
  URL=https://git-scm.com/docs/git-symbolic-ref`, curl exit 0.
- Verbatim: after tag stripping and whitespace normalisation (the method the lesson states),
  the quote matches the page text exactly (`quote_present=True`). In raw HTML it sits in the
  `<dd>` after `<dt id="Documentation/git-symbolic-ref.txt--q">-q</dt>` /
  `<dt id="Documentation/git-symbolic-ref.txt---quiet">--quiet</dt>`; the HTML writes
  `&lt;name&gt;`, rendered `<name>` — exactly the lesson's line-35 caveat.
- Count: `wc -w` = **24** (limit 25).
- Anchor: body `OPTIONS` heading at normalised-text index 2680, quote at 2743, body `NOTES`
  heading at 3427 — the quote is inside §OPTIONS. (The occurrences at 190–217 are the table of
  contents; body headings are DESCRIPTION 2092, OPTIONS 2680, NOTES 3427, SEE ALSO 4007.)
- Revision claims in the row's anchor cell: the page contains
  `git-symbolic-ref last updated in 2.48.0` and `2.48.1 → 2.56.0 no changes` — exactly the row's
  "page version list runs to 2.56.0, last content change recorded at 2.48.0".

## 2. Row anchor — verified

- §DESCRIPTION: `Typically you would give HEAD as the <name> argument to see which branch your
  working tree is on.` at index 2236, between body DESCRIPTION (2092) and OPTIONS (2680).
- §NOTES exit-status sentence: `git symbolic-ref will exit with status 0 if the contents of the
  symbolic ref were printed correctly, with status 1 if the requested name is not a symbolic ref,
  or 128 if another error occurs.` at index 3815, between NOTES (3427) and SEE ALSO (4007).
- §OPTIONS `-q` / `--quiet`: verified in §1.

## 3. Teaches vs page — no overstatement; one unmarked inference

Row teaches: `` `git symbolic-ref HEAD` names the branch only when HEAD is attached; with -q a
detached HEAD exits 1 silently and any other error exits 128, so a P08 resolver must branch on
exit 1 rather than treat it as a failed read ``.

Behaviour check, git 2.56.0 in `/tmp`, `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u
GIT_COMMON_DIR` on every call:

- attached: `git symbolic-ref HEAD` → `refs/heads/master`, exit 0.
- detached: `git symbolic-ref -q HEAD` → empty stdout, empty stderr, exit **1**.
- detached without `-q`: `git symbolic-ref HEAD` → `fatal: ref HEAD is not a symbolic ref`, exit **128**.
- another error, not a repository: `git symbolic-ref -q HEAD` → exit **128**.
- invalid name: `git symbolic-ref -q 'refs/heads/bad..name'` → exit **128** (`fatal: No such ref`).

The page's `-q` text ("non-zero status silently") plus the NOTES sentence (1 / 128) ground the
row's sentence, and behaviour confirms it. Observation, not a row defect: the NOTES sentence is
unconditional, but git 2.56.0 exits 128 without `-q`; the row's "with -q" scoping is the
behaviourally correct reading. A nonexistent valid-looking ref under `-q`
(`git symbolic-ref -q refs/heads/nosuch`) exits 1, consistent with the page's "not a symbolic
ref" bucket, so "any other error" covers genuine errors (128).

Minor gap: the final clause, "so a P08 resolver must branch on exit 1 rather than treat it as a
failed read", is a design inference the page does not state and it carries no `[INFERENCE]`
marker. The round's own convention marks the analogous S066 clause
`[INFERENCE: refusing it is a design choice]`
(`.ufo/waves/round-18/staged/lesson-round-18-gate.md:66`). Non-blocking: the factual clauses are
grounded.

## 4. Tier / kind — fit

Contract (`SOURCES-CONTRACT-v1.md`): kind enum includes `docs`; tier A is "primary or
authoritative for that scope (spec, official docs, source code, original paper, maintainer
statement, …)". The source is the official Git manual page for `git-symbolic-ref`, scoped to
reading HEAD: `docs` / `A` fit. `status=mined` is consistent with a citing used-by path;
`recheck=on-release` is an allowed symbolic cadence; `opened=2026-10-20` is an ISO date. No `|`
inside any cell (NF=13); no tier inflation (the `community`-never-A rule does not apply).

## 5. Used-by — exists and cites S074; one pointer gap

`corpus/knowledge/guard-kill-closure.md` exists at the rev (sha256 above) and cites S074 at:

- `:1` — `source:` header: `S074 — git-symbolic-ref §OPTIONS -q, §NOTES, https://git-scm.com/docs/git-symbolic-ref…`;
- `:47` — substantive: "S074 bears on step 3. … [src: S074, quotes A–C]."

The claim at `:47` matches the page and the measured behaviour. Minor gap: "quotes A–C" is not
defined in that file; the three quotes exist only in the draft
`.ufo/waves/round-18/sources/S075-B11SrcSymbolicRef.md:18-23` (quote A line 19, quote B line 21,
quote C line 23), which the knowledge entry does not name. The citation still names S074 and its
claim is true; the pointer is not self-contained.

## Findings

1. **Verified** — the gate quote is verbatim at §OPTIONS `-q`/`--quiet` under the stated
   normalisation, is 24 words, and the row's version/revision claims match the served page.
2. **Verified** — all three anchor locations exist in their stated sections; the row parses as
   13 cells and the registry census is clean (no malformed row, enum violation, duplicate id, or
   missing used-by path).
3. **Verified** — the teaches cell's factual clauses match the page and git 2.56.0 behaviour
   (exit 0 attached; 1 silent detached with `-q`; 128 on a genuine error).
4. **Minor** — the teaches cell's final design clause is an unmarked inference (S066 precedent,
   gate line 66); grounding for the factual core is present.
5. **Minor** — the round Gate quotes only quote A; the codes "1"/"128" rest on the §NOTES
   sentence, which the row's anchor names but the Gate does not quote (draft quote B, 18 words,
   covers them and was not installed).
6. **Minor** — the used-by citation "[src: S074, quotes A–C]" is defined only in the draft, not
   in the citing file.

No blocking gap and no false claim found.

Verdict: **holds** — S074 verifies at `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; the remaining
gaps are non-blocking documentation pointers.
