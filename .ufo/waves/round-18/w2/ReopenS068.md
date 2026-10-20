# ReopenS068 — independent re-open of SOURCES row S068

Seat: TameshiR18.ReopenS068 (leaf). Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Date: 2026-10-20. Lane reads only via `git show`; no lane writes except this report; no
selftest/gate run (none required by this ticket). Tool installs: none.

Source opened now: https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html
(read tool, then `curl -sSfL` to `/tmp/s068page.html`, exit 0; footer
`Linux man-pages 6.19 2026-02-08`, colophon fetch 2026-09-09).

## The row under test

`corpus/SOURCES.md:77` at the read rev (byte-identical to the staged row diffed below):

| cell | value |
|---|---|
| source | PR_SET_CHILD_SUBREAPER(2const) — Linux manual page — https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html |
| kind / tier | docs / A |
| scope | PR_SET_CHILD_SUBREAPER's reparenting rule: an orphaned process is reparented to the nearest still living ancestor subreaper |
| anchor | §DESCRIPTION, first paragraph after the SYNOPSIS @ man-pages 6.19 (footer 2026-02-08), fetched 2026-10-20 |
| teaches | when a process becomes orphaned, it is reparented to the nearest still living ancestor subreaper, so a subreaper sees descendants whose parent has exited; the page states the rule, not how a signal reaches a descendant that left its process group |
| status / opened / recheck | mined / 2026-10-20 / 180d |
| used-by | corpus/knowledge/guard-kill-closure.md |

Staged gate row `.ufo/waves/round-18/staged/lesson-round-18-gate.md:20` quotes the same
sentence with location "(§DESCRIPTION, first paragraph after SYNOPSIS)".

## Commands, exits, key output

| # | command | exit | output |
|---|---|---|---|
| 1 | `git show 01d586d:corpus/SOURCES.md \| grep -n S068` | 0 | `77:` the row; `207:` round-18 ledger line |
| 2 | `curl -sSfL <url> -o /tmp/s068page.html` | 0 | 9,879 bytes; sha256 `b805fe23c7251ad6c3d08a829ed755b80a8fa106929c67325c7122f3b126ef2c` |
| 3 | python: strip tags, collapse whitespace, substring test | 0 | `quote_present: True`; `count: 1`; `footer: Linux man-pages 6.19 2026-02-08` |
| 4 | `echo -n "$quote" \| wc -w` | 0 | `23` (limit 25; CORPUS.md:113-114) |
| 5 | python: split DESCRIPTION into blank-line paragraphs | 0 | 4 paragraphs; `quote in P1: False`, `quote in P2: True` |
| 6 | `git grep -n S068 01d586d -- .` | 0 | guard-kill-closure.md:1, :73, :83, :133; corpus/README.md:266; staged SOURCES/lesson; drafts |
| 7 | `git cat-file -e 01d586d:corpus/knowledge/guard-kill-closure.md` | 0 | EXISTS |
| 8 | corpus enum/tier awk (CORPUS.md:145) on staged SOURCES.md | 0 | no violations printed |
| 9 | duplicate-id check over `\| S… \|` rows | 0 | no duplicates; `Next unused id: S075` (SOURCES.md:208) |
| 10 | `diff` live `SOURCES.md:77` vs staged `corpus/SOURCES.md:77` | 0 | IDENTICAL |
| 11 | sha256 `corpus/SOURCES.md` live vs rev | 0 | both `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` |
| 12 | sha256 staged `lesson-round-18-gate.md` live vs rev | 0 | both `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` |
| 13 | grep fetched page for `process group` / `setsid` | 0 | 0 / 0 occurrences |
| 14 | `git cat-file -e 58e5d53^:corpus/knowledge/guard-kill-closure.md` | 128 | file created in 58e5d53, not earlier |
| 15 | `sed -n '73p' guard-kill-closure.md \| grep -cF "$quote"`; same on staged lesson `:20` | 0 / 0 | `1` / `1` |

## Findings

### F1 — Quote is verbatim — PASS

The sentence

> When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper.

occurs exactly once in the fetched page after tag stripping and whitespace normalisation
(command 3), with the man page's own punctuation. 23 words (`wc -w`, command 4) ≤ the
25-word gate rule (`/home/vgpnk/Projects/shokunin/CORPUS.md:113-114`).

### F2 — Anchor paragraph index is wrong — DEFECT (minor, non-blocking)

§DESCRIPTION is four paragraphs (command 5):

- P1: "If set is nonzero, set the \"child subreaper\" attribute of the calling process; if set is zero, unset the attribute."
- P2: "A subreaper fulfills the role of init(1) for its descendant processes. **When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper.** Subsequently, ... getppid(2) ... SIGCHLD ... wait(2) ..."
- P3: not inherited by fork(2)/clone(2); preserved across execve(2).
- P4: session-management rationale.

The quoted sentence is the second sentence of **P2**, not P1. The stated anchor
"first paragraph after the SYNOPSIS" therefore points at the set/unset sentence, where the
quote is absent. The defect is inherited from the wave-1 draft
`.ufo/waves/round-18/sources/S069-B05SrcPrctl.md` (Lead, anchor bullet), and is carried
unchanged into `corpus/SOURCES.md:77` and `.ufo/waves/round-18/staged/lesson-round-18-gate.md:20`.
It blocks no downstream use (section named correctly, sentence findable by search,
`corpus/knowledge/guard-kill-closure.md` cites only "§DESCRIPTION"), but the locator as
written is false. Correct wording: `§DESCRIPTION ¶2 (the paragraph beginning "A subreaper
fulfills ...") @ man-pages 6.19 (footer 2026-02-08)`.

### F3 — Teaches cell does not overstate the page — PASS

- "an orphaned process is reparented to the nearest still living ancestor subreaper" —
  direct restatement of P2.
- "so a subreaper sees descendants whose parent has exited" — supported by the very next
  sentences: the orphan's `getppid(2)` returns the subreaper's PID and on termination the
  subreaper receives `SIGCHLD` and can `wait(2)`.
- The negative clause "the page states the rule, not how a signal reaches a descendant that
  left its process group" is true: 0 occurrences of "process group" and 0 of "setsid" in the
  page (command 13). The page's P4 mentions "session management frameworks" generically and
  no group/session signal semantics.
- Nothing in the teaches cell claims the fork/exec inheritance facts (P3) or the
  session-management use (P4), so no reach beyond the page.

### F4 — Tier / kind fit — PASS

`docs` is an allowed kind and `A` is allowed for "official docs" scoped to the semantics of
this syscall constant (`/home/vgpnk/Projects/shokunin/CORPUS.md:94-97`), consistent with
sibling man-page rows (S067 `docs`/`A`, S069 `docs`/`A`, S072 `docs`/`A`). The contract's
enum check prints nothing on the staged registry (command 8). Revision pin is present
(man-pages 6.19, footer 2026-02-08), so the "never a bare homepage" anchor rule is met.

### F5 — used-by path exists and cites S068 — PASS

`corpus/knowledge/guard-kill-closure.md` exists at the read rev (command 7, exit 0) and
cites S068 at:

- `:1` — `source:` header lists "S068 — PR_SET_CHILD_SUBREAPER(2const) §DESCRIPTION"
- `:73` — "Subreaper rule. … Quote: \"When a process becomes orphaned … subreaper.\" [src: S068, …]"
  (the same 23-word quote, byte-identical — command 15, grep count 1)
- `:83` — "The reparenting rule is S068 above."
- `:133` — "The subreaper page is row S068 once B13 installs it."

`status: mined` is therefore satisfied. `corpus/README.md:266` also cites S068, but the
contract's used-by column names knowledge entries/lessons, so the index file is correctly
not listed.

## Non-blocking observation (outside the required checks)

`corpus/knowledge/guard-kill-closure.md:133` still says "The subreaper page is row S068
**once B13 installs it**", while the row is already installed in the same landing commit
(58e5d53; file created there, command 14). This is stale wave-1 future tense in the used-by
entry, not a source-row defect; the citation itself is valid.

## Remaining unknowns

- None on the quote, word count, teaches accuracy, tier/kind, or used-by.
- The paragraph-index defect is reported, not fixed (no lane edits by this seat).

## Verdict

**Partial** — the S068 row holds on quote (verbatim, 23 words), teaches accuracy, tier/kind
(`docs`/A), and used-by (`corpus/knowledge/guard-kill-closure.md`, four citations); the sole
defect is the anchor's paragraph index: the quote is §DESCRIPTION ¶2 ("A subreaper
fulfills…"), not the "first paragraph after the SYNOPSIS" as stated in `SOURCES.md:77` and
`staged/lesson-round-18-gate.md:20` — non-blocking, fix the anchor wording.
