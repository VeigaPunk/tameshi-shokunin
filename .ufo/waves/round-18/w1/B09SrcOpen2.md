# B09SrcOpen2 — open(2) source row (round 18, wave 1)

## Behavior

Opened https://man7.org/linux/man-pages/man2/open.2.html with the read tool. The fetch succeeded on the first attempt; no mirror was used.

Duplicate check: `grep` of `corpus/SOURCES.md` for `man2/open`, `open.2`, `open(2)` returned no matches. The row is not a duplicate, so no `DUPLICATE` verdict.

Admitted, not rejected: the source states that O_TRUNC truncates the file at open when the access mode allows writing (O_RDWR or O_WRONLY). That supports the P05 purpose: an O_RDWR open is a write-capable input, not a pure read.

## Row and gate

The row draft and gate are in `.ufo/waves/round-18/sources/S073-B09SrcOpen2.md`.

- Id: S073 (provisional; the lane registry ends at S064 at tip 183f87b899e6cae46be98d251cbc87fb5118f6ca).
- Status: `mined`, conditional on a `used-by` citation. Provisional `used-by` is `.ufo/evidence/round-18/`.
- Quote: "the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0." — 17 words (`wc -w`), anchor §DESCRIPTION O_TRUNC entry, Linux man-pages 6.19 (2026-02-08).

## Evidence

- `grep` of SOURCES.md for `man2/open|open\(2\)|open\.2|O_TRUNC|S07[0-9]`: no matches for the open(2) URL.
- Registry shape: `awk -F'|'` gives 13 fields per row, i.e. 11 named cells plus the empty leading and trailing fields. The 62 rows all match that shape.
- Max registry id at lane tip: S064 (`grep -o '^| S[0-9]*' | sort -n | tail`).
- Quote location: the artifact lines 513-518 of the fetched page, and the footer line 1086 (`Linux man-pages 6.19 2026-02-08 open(2)`).

## Limits

- The quote is the O_TRUNC condition. The page does not say that O_RDWR alone, without O_TRUNC or O_CREAT, mutates the file at open. The access-mode sentence (lines 92-94) says O_RDWR requests read/write; that is the capability to record.
- Line numbers refer to the fetched text, not to a stable anchor on man7.

## Tools

No installs. Reads and greps only. No git writes, no GIT_* variables, no subagent dispatch.

## Notes for L1

- The Target's `used-by` and status `mined` only hold once a knowledge entry or lesson cites S073. Otherwise set `queued`.
- Renumber S073 if another round-18 row takes it first.

## Verdict

built — row drafted (S073, `mined` conditional on a citation), duplicate check clear, 17-word verbatim quote supports the purpose.
