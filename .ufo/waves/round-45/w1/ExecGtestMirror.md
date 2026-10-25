seat: ExecGtestMirror

# C2 scratch mirror dry run — exact recipe and failure modes

Scope: dry-run of the round-45 C2 integration in a scratch Git repo (no lane
writes except this report). Scratch: `/tmp/tameshi-r45-ExecGtestMirror.0aAo6F`
(`D`), clone of freeze `3310e7be803516ca5934b4e949d91bcec824b179` via
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 3310e7be… | tar -x -C "$D"`.

## Recipe that passes (baseline commit B0 = `5a30850`)

1. Scratch init: `D=$(mktemp -d) && git -C "$D" init -q -b m`; toplevel check
   `git -C "$D" rev-parse --show-toplevel` == `$D` (verified, `TOPLEVEL_OK`).
2. Archive extract into `$D` (verified, `ARCHIVE_OK`).
3. Append two registry rows after the last `## Registry` row (S160, line 130)
   and before the blank line / `## Paths`: S256 (advanced.md) and S257
   (primer.md), each 13 `|`-fields, status `mined`, opened `2026-10-25`,
   recheck `180d`. Source cell first URL is the upstream URL; anchor cell
   contains the snapshot path `.ufo/evidence/round-45/coverage/sources/googletest-{advanced,primer}.md`
   plus a sha256 prefix that matches the committed snapshot blob:
   `05546ed6` (advanced, 2457 lines) and `03d756ab` (primer, 482 lines)
   (`sha256sum` of the archived blobs). used-by cell names the knowledge entry
   path exactly: `corpus/knowledge/r8-gtest-order-and-seed.md` /
   `corpus/knowledge/r8-gtest-primer-independence.md`.
4. Knowledge entries `corpus/knowledge/r8-gtest-order-and-seed.md` /
   `r8-gtest-primer-independence.md`: line 1 `source:` cites the row id
   (S256/S257), line 2 `verified-at: 2026-10-25`, line 3 `recheck: 180d`,
   then one straight-double-quoted quote copied verbatim from the snapshot
   (see quote forms below).
5. Index both in `corpus/README.md` as backticked `` `knowledge/<file>` ``
   (added a `## Round 45` coverage-map table).
6. `git -C "$D" add -A && git -C "$D" -c user.name=scratch -c user.email=scratch@scratch.invalid commit -qm <msg>`
7. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/coverage/measure.py --lane "$D" --rev m`
   → `C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true`, exit 0.
8. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$D"/corpus/SOURCES.md`
   → exit 0, `file ok …/corpus/SOURCES.md`, only pre-existing W04/W01 warnings
   (S047/S048/S075/S076/S077/S078/S081/S092/S104/S160 W04, S101 W01); zero E codes.

Counter selftest: 10/10 PASS, `C2_R45_SELFTEST: cases=10 failed=0`, `VERDICT: PASS`, exit 0.

## Mutation matrix (each from pristine baseline, committed, measured at `--rev m`)

| Mut | Mutation | Counter output | Verdict |
|---|---|---|---|
| B0 | baseline | `C2_R45: self_pin=1 rows=2 entries=2 indexed=2 row_ids=S256,S257 rev=m C2_R45_PASS=true` | PASS |
| B1 | S256 quote drops markdown link brackets: snapshot has `the [GoogleTest Primer](primer.md) and`, entry quotes `the GoogleTest Primer and` | `REFUSED corpus/knowledge/r8-gtest-order-and-seed.md no located quote` → `entries=1 indexed=1 … PASS=false` | REFUSED |
| B2 | curly “ ” delimiters around a valid quote (S256) | both ENTRI lines, `entries=2 indexed=2 … PASS=true` | ACCEPTED |
| B3 | quote whose source text spans two snapshot lines, written one-line in the entry (primer lines 14–15: `It's a pain to debug a test that succeeds or fails as a result of other tests.`) | `entries=2 indexed=2 … PASS=true` | ACCEPTED |
| B4 | S256 anchor without the sha prefix | `rows=1 entries=1 indexed=1 row_ids=S257 … PASS=false` (S256 entry silently skipped, no REFUSED: `cites no googletest row`) | rows drop |
| B5 | S256 used-by path typo (`…r8-gtest-order-and-seedd.md`) | `REFUSED corpus/knowledge/r8-gtest-order-and-seed.md not in used-by` → `entries=1 indexed=1 … PASS=false` | REFUSED |
| B6 | primer entry path removed from README | `ENTRY corpus/knowledge/r8-gtest-primer-independence.md (not indexed)` → `entries=2 indexed=1 … PASS=false` | unindexed |
| B7 | single-quote delimiters `'…'` | `REFUSED corpus/knowledge/r8-gtest-order-and-seed.md no located quote` → `entries=1 … PASS=false` | REFUSED |
| B8 | newline inside the quoted span in the entry | `REFUSED corpus/knowledge/r8-gtest-primer-independence.md no located quote` → `entries=1 … PASS=false` | REFUSED |

## Quote forms the counter accepts (for the scribes)

- ACCEPTED: straight double quotes `"…"`; curly `“…”` (folded to straight);
  multi-line source spans — the snapshot's normalized text is whitespace-folded
  (`' '.join(text.split())` plus unicode-quote/nbsp/zwsp mapping), so a quote
  whose source crosses snapshot lines matches when written on one line in the
  entry (verified B3).
- REJECTED: single quotes `'…'` (QUOTE_RE only matches `"…"`/`“…”`); a literal
  newline inside the quoted span; any verbatim mismatch with the snapshot —
  markdown syntax in the source text (`*emphasis*`, `[link](url)`, backticks)
  must be copied exactly (B1; the same failure hit baseline B0's first primer
  quote `A test suite contains one or many tests.` because the snapshot has
  `A *test suite* contains one or many tests.` → `no located quote`).
- Constraints: quoted span 10–400 raw chars; after fold 6–25 whitespace tokens
  (inclusive); match is an exact substring of the folded snapshot.
- The counter scans the WHOLE entry file for any matching quote — a second,
  valid quote elsewhere in the file masks a broken one (observed during B1;
  each production entry should carry exactly one quoted sentence).

## Other counter mechanics confirmed

- `entry_ok` cites rows from line 1 only (`source:` line, `\bS\d{3,}\b`);
  the row must be `mined` and in the entry's own used-by cell (split on `,`/`;`,
  stripped).
- Index check: `corpus/README.md` must contain `` `knowledge/<file>` `` or
  `` `corpus/knowledge/<file>` `` anywhere (backticked; verified B6).
- Rows are read from `corpus/SOURCES.md` at REV; anchor snapshot path must
  exist at REV and an 8+ hex sha prefix in the anchor cell must prefix the
  blob's sha256 (B4). Rows outside `## Registry` (e.g. `## Paths`) are not
  counted by the counter and fail census E12.
- `self_pin=1` held in every run (committed measure.py identical to the lane's).
- Census: new rows parse as 13 fields; no pipe in any cell; `opened` ≤ today;
  `recheck 180d` valid; used-by paths exist on disk (E11 clean). W04 for S160
  is the pre-existing duplicate-URL warning, unrelated to the append.

## Commands and outputs (evidence)

- Baseline commit `cb84da3` (initial append), `5a30850` (B0 after quote fix).
- `python3 …/coverage/measure.py --lane "$D" --rev m` (B0): exit 0, full line above.
- `sources-census.sh validate --file "$D"/corpus/SOURCES.md`: exit 0; `file ok …`; warnings list above.
- Selftest exit 0 (10/10).
- Snapshot sha prefixes: advanced `05546ed6`, primer `03d756ab`, testing `44c56c61` (unused by rows).

## Risks / notes for the L1

- The scrub recipe depends on the freeze committing the snapshot blobs at
  `.ufo/evidence/round-45/coverage/sources/` (they are present at
  `3310e7be…`); anchors must name those exact paths.
- Keep each knowledge entry's quote to one sentence; copy the snapshot text
  verbatim including any inline markdown; prefer sentences with no markdown
  emphasis (e.g. advanced line 1977 `This helps to reveal bad dependencies between tests.`,
  primer line 101 `GoogleTest assertions are macros that resemble function calls.`).
- Rows must be appended inside `## Registry` (after S160, before `## Paths`).
- No blockers; all six requested breaks reproduced plus two extra quote-form
  breaks (B7/B8).

Files changed: scratch repo only (`/tmp/tameshi-r45-ExecGtestMirror.0aAo6F`)
plus this report.
