# S073 — row draft (B09SrcOpen2, round 18 wave 1)

Provisional id S073. Lane registry at tip 183f87b899e6cae46be98d251cbc87fb5118f6ca ends at S064; the L1 renumbers if another row takes S073 first.

Duplicate check: no `man2/open` or `open(2)` row exists in `corpus/SOURCES.md` (grep, exit 1, no matches). Not a duplicate.

## Registry row

| S073 | Linux man-pages: open(2) — https://man7.org/linux/man-pages/man2/open.2.html | docs | A | open(2)'s access modes and open-time effects, for whether an O_RDWR open is a pure read input | §DESCRIPTION, O_TRUNC entry in the file creation flags list @ Linux man-pages 6.19 (footer 2026-02-08), fetched 2026-10-20 | O_RDWR requests read/write, and O_TRUNC truncates the file at open whenever the access mode allows writing, so an O_RDWR open with O_TRUNC is a write-capable input, not a pure read | mined | 2026-10-20 | 365d | .ufo/evidence/round-18/ |

## Gate

- URL: https://man7.org/linux/man-pages/man2/open.2.html
- Access date: 2026-10-20 (read tool, native fetch; page footer `Linux man-pages 6.19  2026-02-08`).
- Section/anchor: §DESCRIPTION, O_TRUNC entry (page lines 513-518 of the fetched text; the man7 page's `#DESCRIPTION` section, flag list `O_TRUNC`).
- Quote (verbatim, whitespace normalised across the man-page line wrap; 17 words, counted with `wc -w`):

  > the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0.

- Support for the purpose: the quote shows an open whose access mode is O_RDWR, with O_TRUNC, truncates the file at open time. An O_RDWR open is therefore not a pure read input.
- Limit (stated, not overclaimed): the quote is the O_TRUNC condition. The page does not say that O_RDWR alone, without O_TRUNC or O_CREAT, mutates the file at open. The same page at §DESCRIPTION (access-mode sentence, lines 92-94) says O_RDWR requests "read/write", which is the capability the trace must record.

## Decision

ADMIT as `mined` with a conditional. Status `mined` requires at least one `used-by` path citing the row (rule: `mined` = cited by ≥1 path). `.ufo/evidence/round-18/` is the provisional path from the Target; if the L1 does not cite the row from a knowledge entry or lesson, the status must be `queued`.
