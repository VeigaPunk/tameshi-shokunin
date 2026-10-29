# T57W1ScribeSourcesRow — SOURCES rows draft (round 57, wave 1)

Lane: tameshi. Base: `5e3569969b532310d2b8a3d130901757a3df356b`. Seat wrote no lane production file; the lane `corpus/SOURCES.md` was byte-equal to base (sha256 `6c2096d8…a6d3`) when read.

## Result

Three rows drafted, one staged diff, one gate block, one machine-readable file, receipts.

| id | source | tier | status | why |
|---|---|---|---|---|
| S283 | GNU Grep Manual §2.3 Exit Status (scout A) | A | queued | grep's documented 0 selected / 1 none / 2 error map; `-q` carve-out recorded in teaches |
| S284 | Postmortem Culture (Google SRE Workbook, ch. 10) (scout B receipts) | A | queued | Google's own postmortem practice; the "factual artifact… free from personal judgments and subjective language" rule |
| S285 | Postmortems (Atlassian Incident Management Handbook) (scout B receipts) | B | rejected | vendor self-description, no outcome data; `REJECTED: …; flip: …` form |

Status deviations from the item, stated:
- Scout A proposed `mined` for S283. Set to `queued`: the item says `mined` only when an admitted knowledge entry cites the row, and the staged set has no knowledge entry citing it. Flip: when a knowledge entry citing S283 is admitted, set status `mined` and list that path in `used-by`.
- S284 is `queued` for the same reason (no staged knowledge entry cites it).

## Scout inputs

- Scout A (`T57W1ScoutSourceA.json`): present. Receipt re-derived by this seat: sha256 `517177d0…675f37` matches. Quote located at receipt lines 1208-1209 (23 words) and the `-q` carve-out at lines 1209-1211. Its `sysexits(3)` grounding candidate is already the mined row S090 (round-55 refusal), so no new row.
- Scout B (`T57W1ScoutSourceB.json`, `.md`): **absent** after six one-minute polls. Drafted against the candidates present in its receipt directory, as the item instructs. Its `accepted-source-sha256.txt` lists only the Google SRE Workbook page (sha `25b55c64…0bd22`), which is why S284 is the admitted row. S285 is my choice of rejected candidate (fetched, not in the accepted list). The SRE book ch. 15 page was also fetched (sha `ef876f0a…4656c5`) and is **not rowed**: no receipt records a decision for it. L1 to rule.

## Checks run

1. Census, applied patch (scratch copy of lane `corpus/`, `patch -p1` applied, result byte-equal to the scratch edit):
   `scripts/sources-census.sh validate --file corpus/SOURCES.md` run from a scratch root carrying `corpus/` and `tools/` → **exit 0**, 16 warnings (15 W04 duplicate-URL, 1 W01 S101), the same set as round 56, no E-codes. Receipt `T57W1ScribeSourcesRow-receipts/census-after.stdout`.
   Note: `--file` resolves `used-by` paths from the scratch root. A root without `corpus/knowledge` and `tools/` gives 171 false E11 errors; that control was discarded and is not evidence.
2. Shape (on applied copy): 145 rows (base 142); malformed rows (NF≠13) 0; duplicate ids 0; enum violations 0. Histogram: base `mined=114 queued=21 rejected=7` → after `mined=114 queued=23 rejected=8`. Receipt `sweeps.stdout`.
3. Negative sweeps on the lane corpus at base (receipt `sweeps-base-negative.stdout`): `gnu\.org/software/grep`, `sre\.google`, `atlassian\.com/incident`, `postmortem` → no match (exit 1). The three new URLs are not already rows. `sysexits` matches only S090 and round-55 history.
4. Sha re-derivation of the four scout receipts and quote location: `T57W1ScribeSourcesRow-receipts/quote-location-and-sha.stdout`. The Atlassian sentence is split by an `<a>` tag in the raw HTML; the quote is located with markup stripped (raw line 42055, extracted text line 2036).

## Artifacts

- Diff against base (27 lines, three rows + search-log bullet + id-allocation line): `.ufo/waves/round-57/w1/T57W1ScribeSourcesRow/stage/corpus/SOURCES.diff`.
  Hunks: after S282 (registry, three rows), after the round-56 search-log bullet (one bullet, preceded by a blank line), and the tail of `## Id allocation` (round-57 line, `Next unused id: S286`).
- Gate block (URL, access date 2026-10-28, located quotes, verdicts): `.ufo/waves/round-57/w1/T57W1ScribeSourcesRow/gate-block.md`.
- Machine-readable: `.ufo/waves/round-57/w1/T57W1ScribeSourcesRow.json` (parses).
- Receipts: `.ufo/waves/round-57/w1/T57W1ScribeSourcesRow-receipts/` (census outputs, sweeps, quote locations, `INDEX.txt`, extracted texts of the workbook and Atlassian pages and the grep manual, extraction script).

## Byte-change scope (NO-HARM)

`corpus/SOURCES.md` changes. That drops round-21 cold-read credit for any section keyed on it (the 64→50 pattern the item records). Not touched: `corpus/QUALITY.md`, `corpus/README.md`, `SKILL.md`, any knowledge entry. The L1 re-keys at wave 3 with C0 content-final.

## Findings for the L1

1. Apply with `patch -p1` from the lane root (labels `a/corpus/SOURCES.md`, `b/corpus/SOURCES.md`); re-run the census from the lane root (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`) after applying, since my census was on a scratch root.
2. The round-57 C2 knowledge/lesson entry is the only thing that can flip S283 to `mined`. If it cites S283, change status and `used-by` in the same diff.
3. SRE book ch. 15 (`https://sre.google/sre-book/postmortem-culture/`): fetched, not rowed. Decide: row (next unused id after S285, which would be S286 and move the "Next unused id" line) or leave as a lead.
4. Scout B's own `.json`/`.md` never landed. If it lands later with a different admitted set, the S284/S285 ids are the ones to reconcile.

## Tooling

No tools installed. No pacman, uv, npm or binary channel used. Python 3 standard library used for HTML text extraction in scratch only.

## Out of scope / not done

- No lane production file edited; no git/jj mutation in the lane or fleet repo.
- No `considerthese` proposal mined (the item did not name one).
- Scratch `$HYAKU_SCRATCH/tameshi-r57/T57W1ScribeSourcesRow` removed at the end of the seat.
