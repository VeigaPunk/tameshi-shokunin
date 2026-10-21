# SourceS075: re-open of registry row S075 (round 19, w1, advisory)

Seat: `TameshiR19-2.SourceS075` (scout, read-only). Date: 2026-10-21.
Scope: registry row S075 in `corpus/SOURCES.md`, its URL, and whether it
supports round-19 C1 (five routed round-18 metadata/receipt defects). I made
no registry or production edits. Only this report was written.

**Verdict: S075 holds as a row. Do not use it as round-19 C1 claim support
(it covers a different subject). Keep it unchanged.** One related residual
outside C1 is listed in §5.

## 1. Source re-opened

- URL: https://man7.org/linux/man-pages/man1/strace.1.html (HTML `<title>`
  "strace(1) - Linux manual page").
- `curl -sSL` → HTTP 200, 85,238 B, sha256
  `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6`, access
  2026-10-21T05:49:40Z. `curl -sSI` → `Last-Modified: Thu, 08 Oct 2026
  17:39:35 GMT`, ETag `"14cf6-65d57b70ec3c0"`.
- The page is **byte-identical** to the 2026-10-20 fetches: same sha256 and
  size in `.ufo/waves/round-17/w2/ReopenS060.md:18` and
  `.ufo/waves/round-18/w1/S16SourcesRowsAudit.md:20`, same Last-Modified in
  ReopenS060.md:19.
- Footer: `strace 7.1.0.62.c605d6 2026-06-25`, the same as S060's pin. The
  colophon says the page comes from the strace project's upstream Git
  (obtained 2026-08-04).
- Host cross-check: `pacman -Q strace` → `strace 7.2-1`. `strace -V` →
  `strace -- version 7.2`. In `/usr/share/man/man1/strace.1.gz` the `.TH` is
  `"2026-06-25" "strace 7.2"`. The quoted sentence is at roff:541 under
  `.SS Filtering` (534). `-f` is at roff:437-439 under `.SS Tracing` (385).
  The `%file` gloss is at roff:590.

**Located quotes** (verbatim, 18 words in total):

- "Traces only the specified set of system calls." (8 words). Location:
  §OPTIONS › Filtering › `-e trace=syscall_set`, line 385 of the
  tag-stripped page. Accessed 2026-10-21.
- "You can think of this as an abbreviation for
  --trace=open,stat,chmod,unlink,..." (10 words). Location: §Filtering ›
  `%file`, stripped lines 418-419. Accessed 2026-10-21.

Section placement in the stripped page:

| Section | Starts at line | Relevant entries |
|---|---|---|
| General | 218 | (ends at Startup) |
| Startup | 245 | |
| Tracing | 293 | `-f`/`--follow-forks` at 327-333 |
| Filtering | 381 | `-z` at 579 |
| Output format | 588 | `-o` at 751, `-q` at 788, `-s` at 819, `-y` at 930 |
| Statistics | 975 | |

## 2. Row S075, cell by cell

| Cell | Observed | Result |
|---|---|---|
| source/kind/tier | The page is the tool's own manual, rendered from upstream | holds: docs, tier A for strace option semantics |
| scope | "supersedes S060's anchor only" | holds; S060 row (SOURCES.md:69) is unedited |
| anchor | §Filtering quote, §Tracing `-f` | holds: verbatim, placement as in §1 |
| teaches: 16-name list | `trace-inputs.py:74-80` matches the row's list exactly, 16/16 in order | holds |
| teaches: argv | The list is passed as `-e trace=` at `:630-631` | holds |
| teaches: collector blob | sha256 `521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070`, the same at `7243e7f`, `21e7932` and the worktree | holds |
| teaches: `%file` records stat calls | The page's own `%file` gloss (quote 2) names `stat` | holds |
| teaches: no stat-only probes | No stat/access/readlink-family name is in the list | holds |
| status / used-by | `mined`; `corpus/lessons/round-18.md:108` cites S075 | holds |
| opened / recheck | 2026-10-20 / 180d, next due 2027-04-18 | not due |

Row stability (sha256 of the `grep '^| S0xx '` row line, newline included):

- S075 is
  `93dcebc9433e1a34c16c130bc59d1867e3a0975f352399d35d34e4a268d886ff` at
  `4b7c682`, `7243e7f` (frozen baseline), `21e7932` (HEAD/master, delivered)
  and in the worktree.
- S060 is
  `5481e5e8555f61c73d09882a98188e0f13d9638703208364120f097110c5d2cd` at
  `183f87b`, `4b7c682`, `7243e7f`, `21e7932` and in the worktree.
- `diff` of baseline→worktree `corpus/SOURCES.md` exits 1 (the files
  differ). It changes only the S049 row and adds one search-log entry.

Round 19 did not touch S075 or S060.

## 3. Relation to C1

- None of R18-1..R18-5 (verifier §5; `lessons/round-19.md:17-21`) is about
  strace or trace filtering. `round-19.md` does not cite S075; its C1 source
  is S049.
- S075 appears in R18-3 only as something being counted. I re-ran `git diff -U0 183f87b 4b7c682 --
  corpus/SOURCES.md`:
  - S075 is one of the 25 added lines.
  - The 5 deleted lines are S001, S008, S052, S056 and S057, which matches
    `sources-diff.txt` (`25 5`), QUALITY 38 and R18-3.
  - S060 is not in the deleted lines.
  - This shows the correction was appended rather than edited in place. It
    does not make S075 a source for R18-3.
- `census-start.txt:6`: the W04 duplicate-URL warning for S075 is expected,
  because superseding rows reuse the URL. The same warning is in round-18
  `census-end.txt:4`, and the round-18 spotcheck (lines 157-158) explains it.

## 4. Tier, limits, recommendation

Tier A, limited to strace's documented option semantics. Limits:

- It documents options. It does not show what any historical trace recorded,
  or that the collector ran.
- It says nothing about receipts, metadata, errata or diff counts.
- The man7 page is labelled with a development version (7.1.0.62) while the
  host has the 7.2 release. Only the quoted sentences and the placement of
  `-f` and `%file` were compared; they are identical.
- The version pin is held by reference ("as in S060").
- [INFERENCE] The collector also passes `-z`/`--successful-only` (§Filtering,
  stripped line 579). That drops failed-open probes from the trace too.
  Neither S060 nor S075 claims or anchors this. It is a gap, not a falsehood.

**Recommendation: do not cite S075 as round-19 C1 support.** Its subject is
not C1's subject, and citing a correct source that does not bear on the claim
would launder support. Keep the row byte-unchanged. Do not add `round-19.md`
to its used-by, and make no change to its status or tier.

## 5. Residual outside C1 (observation; no expansion claim)

`corpus/knowledge/input-keyed-coldread-credit.md:1`, the `source:` line,
still cites S060 as "§Filtering `%file`, §General `-f`, §Output format
`-y`". These are exactly the two anchors S075 supersedes.

- The line is byte-identical at `7243e7f`, at `21e7932` and in the worktree.
- The file's only errata block (line 77, R17-KNOW-EXIT) is scoped to §5 and
  the `measure-*.json` citation, and says "Lines 1–75 are unchanged".
- Round 18 saw this (`.ufo/waves/round-18/w1/S16SourcesRowsAudit.md:67`;
  `S20OperatorTeachings.md:119-121`, "separate edit, not made here").
- Grepping `corpus/` and `.ufo/waves/round-19/` finds no record of it as open
  debt.

This is the QUALITY 37 class, but it is not one of verifier §5's five routed
items, so C1's 0/5→5/5 count is unaffected. Concrete failing criterion: any
round-19 statement that stale source or superseded-anchor metadata is
corrected lane-wide is false at line 1 of that file. L1 decides whether to
record it as named open debt.

## 6. Commands (all read-only)

- `curl -sSL` and `curl -sSI` on the URL.
- `sha256sum`.
- `env -i … git cat-file -p REV:path` for `183f87b`, `4b7c682`, `7243e7f`,
  `21e7932`.
- `git cat-file -t`, `git log`, `git merge-base --is-ancestor`: the baseline
  is an ancestor of `21e7932`.
- `git diff -U0 183f87b 4b7c682 -- corpus/SOURCES.md`.
- `diff` of the baseline vs worktree SOURCES.md.
- `zcat` of the host man page; `pacman -Q`; `strace -V`.
- Python in-memory parsing of `/tmp/tameshi-r19-S075/strace.1.html`.

Every exit was 0 except `diff -q`, which exited 1 because the files differ.
Scratch is `/tmp/tameshi-r19-S075/` (disposable). No tool was installed or
updated.

## 7. Unknowns

- Whether man7 will re-render the page for 7.2.
- Drift between 7.1.0.62 and 7.2 outside the compared lines.
- Whether any round-19 artifact not yet landed will cite S075. None does at
  `21e7932` or in the worktree.
