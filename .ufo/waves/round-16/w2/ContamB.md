# ContamB — contamination audit of wave-1 cold-read seats CR14–CR27 (round 16, wave 2)

Seat `TameshiR16.ContamB` (sentinel, leaf). Scratch `/tmp/tameshi-r16w2-ContamB-Ekat13/`.
Attacked artifact: the 14 committed wave-1 reports `.ufo/waves/round-16/w1/CR14.md` … `CR27.md`
at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`, checked against the seats' own tool transcripts.
No installs or updates. No lane file written except this report.

**Verdict: holds.** None of the 35 ledger sections owned by CR14–CR27 has a verdict that rests
on contaminated content. Every opened path on the forbidden list was one that the seat's own
page range names (page-directed). Every other forbidden-surface touch exposed only file names,
or searched content and got zero forbidden hits. The contamination rule held. Disclosure did
not fully hold: 9 seats under-reported opens or listings in `opened`, and 1 seat over-reported.
Those are minor gaps; none of them changes a verdict.

## Rule applied (from wave-1 `spec1.json` context, read at `c699c8c`)

> "read the snapshot … only your assigned line range plus any file, command or URL your range
> explicitly names (and files those name, transitively, only as needed). Never open LOG.md,
> SCORECARD.md, SHONEN.md, plans/, reports/, corpus/lessons/, .ufo/waves/, other seats' reports,
> or this wave context's claims as evidence. List every opened path in `opened`."

Classification used:
- **page-directed**: the seat's own range names the path or line range.
- **margin**: snapshot lines next to the range, read to find section boundaries. Not named by
  the range.
- **listing-only**: names were exposed, not content.
- **contamination**: content from a forbidden or un-named surface reached the seat.

## Method (commands, exits)

| step | command | exit / key output |
|---|---|---|
| pin | `git show c699c8c:.ufo/evidence/round-16/coldread/SKILL.snapshot.md \| sha256sum` | `97cf436b…3580` (matches the wave-1 pin) |
| reports | `git show c699c8c:.ufo/waves/round-16/w1/CR{14..27}.md` → scratch; parse the last ```json block | 14/14 parsed, 1 block each |
| ranges | `spec1.json` `items[].prompt` for CR14–CR27 (`Read ONLY snapshot lines …`) | 794-857 … 1609-1705 |
| transcripts | `cat history://TameshiR16.CR{14..27}` | exit 0 each; tool arguments are cut to about 100 characters (not enough on its own) |
| full args | `~/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963…/TameshiR16/TameshiR16.CR{14..27}.jsonl` (seat session transcripts; not `agent.db*`, not credential files) | 439 tool calls with full arguments and results; time window 13:24:08Z–13:36:20Z |
| scan | regex over every call's arguments for forbidden paths / recursive search / SKILL ranges, then the full result of each hit read | listed below |
| ledger | committed `assemble.py` + snapshot + w1 reports, copied to a /tmp mirror: `python3 assemble.py --out /tmp/…/ledger.snapshot.json "<mirror>/.ufo/waves/round-16/w1/*.md"` | exit 0; `coverage: 51/51`; 36 `SKIPPED` (non-seat .md) |
| inbound | user/custom messages after the first prompt, in each seat jsonl | 0 in all 14 (no steering, no peer content injected) |

## Forbidden-list opens (content), all page-directed

| seat | call (ts) | path read | page anchor naming it | class | used for |
|---|---|---|---|---|---|
| CR14 | #7 13:24:43Z `read plans/round-6.plan.md:20-40`; #14 `:raw:23-25,30-34`; #40 `grep -n … plans/round-6.plan.md` | `plans/round-6.plan.md` | snapshot `:803` "`plans/round-6.plan.md:30-34`", `:825` "`:23-25`" | page-directed, with line overreach (20-22, 26-29, 35-40 shown by the first read) | 794 anchor re-check (`verified-record`) |
| CR17 | #21 13:27:27Z `read plans/round-7.plan.md:1-25` | `plans/round-7.plan.md` | snapshot `:1001` "`plans/round-7.plan.md:11-15`" | page-directed, overreach (1-10, 16-25) | 965 minor gap M6 (citation precision) |

No CR14–CR27 seat opened the content of `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `reports/`,
`corpus/lessons/`, any `.ufo/waves/` file other than its own report, or `spec1.json` /
`dispatch1.json` / `assignments1.json`.

Pages that named forbidden anchors the seat **refused** (rule respected; record left unverified
and said so in the report):
- CR23: `LOG.md:303-309`, `plans/round-11.plan.md:13,:20-25,:80-103` (snapshot 1367-1375, 1440). See CR23.md:46, :65, :139.
- CR25: `corpus/lessons/round-12-verifier-spotcheck.md` (snapshot 1521).
- CR26: `corpus/lessons/round-13-verifier-spotcheck.md` (1565).
- CR27: `corpus/lessons/round-15.md`, `corpus/lessons/round-14-verifier-spotcheck.md` (1612-1613). The directory was listed only; this is disclosed at CR27.md:41-44 and as minor gap #2 on section 1609.

## Forbidden-surface touches that exposed names only, or zero hits

| seat | call | what | exposure | disclosed in `opened`? |
|---|---|---|---|---|
| CR15 | #5 13:24:22Z `grep -rn "arm-class-matrix\|fleet-suite-census\|mutation-case-mado-verify" --include='*.md' -l . \| head -30` | recursive search over the whole lane, including forbidden dirs | **file names only** (`-l`): `./SKILL.md`, 13 `plans/*`, `./reports/r11-aud-t11.md`, `./.ufo/waves/round-13/w1/MadoPin.md` | no |
| CR17 | #7 13:24:43Z `grep -n 'cf41efaa\|CF41EFAA' -r tools/ corpus/ plans/ \| head -20` | content search that included `plans/` | **0 plans/ lines returned**: all 20 output lines are `corpus/knowledge/*` (head cut-off) | no |
| CR17 | #34 `ls .ufo/waves/round-16/w1` | listing | names (`AttrCritic.md … CR19.md, CR21.md`) | no |
| CR20 | #30 `ls .ufo/waves/round-16/w1 \| head` | listing | names | no |
| CR21 | #1 13:24:09Z `ls -la .ufo/waves/round-16/w1/` | listing | only `swarm-registry.json` existed | no |
| CR22 | #17 `mkdir -p …/w1 && ls …/w1/` | listing | names (CR19/CR24/CR25 …) | no |
| CR23 | #10 `ls plans/`; #13 `git show --name-only 606716f`, `git log -- plans/round-11.plan.md` | names and commit metadata | names incl. `LOG.md`, `SCORECARD.md`, `reports/r10-aud-t10.md` | yes ("plans/ directory listing only") |
| CR23 | #45 `ls -la .ufo/waves/round-16/` | listing | names (`spec1.json`, `dispatch1.json` …) | no |
| CR26 | #5 13:25:17Z `glob tameshi-shokunin` (lane root) | full tree listing | names incl. `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-15/w{1,2}/*` | no |
| CR27 | #16 13:28:16Z `grep -rn 'Gate standard' *.md tools/` from lane root | content search over `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md` | **one hit only: `SKILL.md:1614`**, which is inside its own range (1609-1705); 0 hits in the forbidden files | no ("lane root listing" only) |
| CR27 | #19 `ls … corpus/lessons/` | listing (page names two lessons files) | names | yes (CR27.md:98) |

## Out-of-range SKILL snapshot reads

| seat (range) | out-of-range lines read | class |
|---|---|---|
| CR14 (794-857) | 858-861 (#45) | margin |
| CR15 (858-920) | 845-857, 921-935 (`sed -n '845,935p'`, #3) | margin; **not disclosed** |
| CR17 (965-1009) | 955-964, 1010-1015 (#1, #2); heading inventory of lines 1-1010 (`awk 'NR<=1010 && /^#{1,3} /' \| tail -30`, #3) | margin plus out-of-range headings; the inventory is **not disclosed** |
| CR18 (1010-1091) | 811-812 (#5) | page-directed (`:1084` "(:811-812)") |
| CR19 (1092-1154) | 1085-1091, 1155-1160 (#3) | margin, disclosed |
| CR20 (1155-1245) | 1246-1255 margin; 1015-1022, 1069-1090 | margin + page-directed (`:1162` "`:1019`", `:1232` "`:1069-1090`"), disclosed |
| CR21 (1246-1271) | 1240-1245, 1272-1285 margin; 810-850, 875-885 | margin + page-directed (`:1259-1263` cite `:813-817`, `:840-844`, `:823-825`, `:879-881`), with overreach |
| CR22 (1272-1364) | 925-929, 1218-1228, 1250-1254, 965-1008 | page-directed (`:1346`, `:1347`, `:1296`, `:1353`) |
| CR23 (1365-1463) | 120-141, 960-1010, 1012-1096, 1225-1300, 1318-1365 | page-directed (`:131`, `:965-1008`, `:1017-1053`, `:1069-1090`, `:1230-1244`, `:1246-1270`, `:1294-1297`, `:1324-1363`) with overreach. Whole-page grep `recorded rev\|pin read\|per case, ER-3` (#17, 71 lines; context incl. 944-948, 1157, 1166, 1310) was used to locate a cited range. Historical `git show 284ab0f^:SKILL.md` 1360-1363 is byte-identical to snapshot 1360-1363 (`diff` → only the EOF-newline marker differs), so it added no new content |
| CR24 (1464-1516) | none | clean |
| CR25 (1517-1562) | 1500-1516 (#2) | margin. **Over-declared**: `opened` says "lines 1479-1562", but the transcript has a single read starting at 1500 |
| CR26 (1563-1608) | 1555-1562, 1609-1610 (#1) | margin; **not disclosed** |
| CR27 (1609-1705) | 1600-1608 (#1) | page-directed (`:1630`, `:1636` "registry … above") |

Grep of every report for citations of these margin lines (`CR15 8[45]x/92x-93x`, `CR17 955-964/1010-1015`,
`CR19 1085-1091/1155-1160`, `CR21 1240-1245/1272-1285`, `CR25 1500-1516`, `CR26 1555-1562`,
`CR23 944-948/1157/1166/1310`): the only hits are boundary statements ("next heading at …")
or substrings inside sha256 values. No finding or verdict cites margin content.

Paths outside the forbidden list that were opened because the page named them: CR15
`arm-class-matrix.md` (snapshot "matrix row F", an implicit name), CR21 `PROVINCE.md:1-47`
(`:1262` "`PROVINCE.md:14-18`, `:20`"), CR23 `corpus/README.md` (`:1392`), CR24
`/home/vgpnk/Projects/shokunin/PROTOCOL.md:55-75` (`:1469` "`../PROTOCOL.md:63–68`"), CR26/CR27
`corpus/SOURCES.md` (S-ids). CR16/CR18/CR22 read `~/.omp/agent/RULES.md` because the wave
contract says to; it is not used as evidence.

## Affected ledger verdicts

The re-assembled ledger (committed `assemble.py`, w1 reports only) has exactly one seat per
section for 794–1676, so every touch maps to exactly one entry:

| entry | ledger verdict (w1) | touch | effect |
|---|---|---|---|
| 794 | verified-record | CR14 `plans/round-6.plan.md` (page-directed) | none: the anchor is named by the page |
| 965 | gap-minor (6 minor) | CR17 `plans/round-7.plan.md` (page-directed); `plans/` grep (0 hits) | none: M6 rests on the page-named file |
| 1365 / 1380 / 1449 | gap-minor / gap-minor / verified-record | CR23 refused `LOG.md` and `plans/round-11.plan.md` | the record is unverified because of the rule (stated at CR23.md:46, :139); this is a calibration limit, not contamination |
| 1517, 1563, 1609 | gap-minor ×3 | the named `corpus/lessons/*` sources were refused | same: unverified because of the rule; disclosed for 1609 |

All other entries owned by CR14–CR27 have no forbidden-surface touches. **No verdict flips.**

## Side findings in the audited reports (accuracy, not contamination)

1. **CR27, section 1609, minor gap #1 is partly wrong.** The gap reads "no PROTOCOL.md exists
   in the lane or its git history". The seat searched only the lane (`find .`, `git log -- PROTOCOL.md`).
   The file exists at the fleet root: `grep -n 'Gate standard' /home/vgpnk/Projects/shokunin/PROTOCOL.md`
   → `375:## Gate standard`. CR24's range already used `../PROTOCOL.md` (snapshot `:1469`).
   The gap is still real, because the bare path at `:1614` does not resolve from the lane. The
   "absent" claim and the recommendation to create the file (CR27.md:37, :83) are wrong. The
   repair at `c699c8c` is correct anyway: `SKILL.md:1614` now reads "`../PROTOCOL.md` §Gate
   standard", and the errata row at `SKILL.md:1731` says "(fleet root; the lane holds none)".
2. **CR14's `rm -rf /tmp/w5-mado-m52-selftest.wauxVY` (#48, 13:28:58Z) removed its own
   scratch, not foreign scratch.** `grep -r wauxVY /tmp/tameshi-r16-CR14-3092/` →
   `sweep/evidence/D2.out: fixtures kept: /tmp/w5-mado-m52-selftest.wauxVY`. That directory was
   created by CR14's own killed-D2 selftest. This is consistent with service limit (j) "foreign
   scratch never removed".

## Bounded recommendations (for the L1; this seat edits nothing)

- Resolve the rule conflict: the forbidden list (`plans/`, `LOG.md`, `corpus/lessons/`) and
  "files your range names" disagree for sections 794, 965, 1365, 1517, 1563 and 1609. Seats
  went different ways: CR14 and CR17 opened the files, CR23, CR25, CR26 and CR27 refused. State
  one precedence (e.g. "page-named lines only, exact range"). Otherwise the same rule gives
  verified-record on one section and unverified-by-rule on another.
- Ask every seat to put recursive searches and directory listings in `opened` (CR15 #5, CR17 #7/#34,
  CR20 #30, CR21 #1, CR22 #17, CR23 #45, CR26 #5, CR27 #16 were missing). Also ask for exact line
  spans instead of a bare file path (CR14, CR15, CR26 margins; CR25's over-declared 1479).
- Mark the 1609 minor-gap text "absent" as superseded by the `../PROTOCOL.md` repair, so the
  ledger does not carry the false absence claim.

## Limits

- `history://` cuts tool arguments to about 100 characters. The full-argument evidence comes
  from the seats' session `.jsonl` transcripts, read only for these 14 seats.
- Searches whose results were cut off by `head` (CR15 #5 `-l | head -30`, CR17 #7 `| head -20`)
  are judged on what the seat actually saw, not on what the full search would have matched.
- The committed tree has no `ledger.json`, so "ledger verdict" here means the w1-only
  re-assembly in `/tmp/tameshi-r16w2-ContamB-Ekat13/ledger.snapshot.json`. The L1's final
  ledger may also apply w2 inputs and overrides.
