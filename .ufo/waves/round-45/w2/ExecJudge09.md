seat: ExecJudge09

# C1 falsify (w2) — independent re-judgment of S075, S090, S132

Non-author verdicts for the three wave-1 ledger entries. Inputs read at `ad5942c6e9858af19d00000b58439b321ddfa62b` (ledger + snapshots + author reports); lane worktree was at `1f9266ac6d4a107a16ca80a2b81c985df5ecad14` (wave-1 reports only on top). Scratch: `/tmp/tameshi-r45-ExecJudge09/`. No lane file written except this report.

## Verdicts

S075 agree — reviewer ExecJudge09 — live fetch of `https://man7.org/linux/man-pages/man1/strace.1.html` is byte-identical (sha equal) to the entry's `raw_sha256` and to the committed snapshot, and the quote sits in §Filtering immediately after the anchored `-e trace=syscall_set` text, defining a `syscall_set` element as a system call named explicitly — which supports the teaches claim that the collector passes an explicit syscall list rather than `%file`; the separate `-f` clause also still holds (`--follow-forks` at extract idx 10492, after the §Tracing heading at idx 9382, while §General is at idx 6714).
S090 agree — reviewer ExecJudge09 — live fetch is byte-identical (sha equal) to the entry's `raw_sha256` and to the committed snapshot, and the 25-token quote sits in §ERRORS of the FreeBSD 15.1-RELEASE page (page date `May 9, 2024` present in the snapshot) between the "meaning of the codes is approximately as follows" lead-in and the `EX_DATAERR` entry, stating the `EX_USAGE (64)` usage-error meaning the teaches claims; its tail `, a bad syntax in a parameter, or whatever.` appears in no row cell (`grep -c 'bad syntax\|or whatever' corpus/SOURCES.md` → `0`), so it was located from the snapshot, not pasted from the registry.
S132 agree — reviewer ExecJudge09 — live fetch is byte-identical (sha equal) to the entry's `raw_sha256` and to the committed snapshot, and the quote is the `D29` Title cell of the README's document table (`# Snapshot Testing: Benefits and Drawbacks |Id |Title |Url |`), which is exactly the row's anchor (`README row D29`) and the teaches claim that the table names the document; the quoted title wording is absent from every row cell.

## Provenance — sha256, three ways (all equal)

```
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecJudge09/S###.live '<row url>'   # all exit 0
gunzip -c .ufo/evidence/round-45/freshness/sources/S###.raw.gz > /tmp/tameshi-r45-ExecJudge09/S###.snap
sha256sum /tmp/tameshi-r45-ExecJudge09/S###.live /tmp/tameshi-r45-ExecJudge09/S###.snap
```

| row | ledger `raw_sha256` (ledger.json:401/513/697) | live fetch 2026-10-25 | committed snapshot | bytes |
|---|---|---|---|---|
| S075 | `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6` | `eedefecf…ea02f6` equal | `eedefecf…ea02f6` equal | 85238 |
| S090 | `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` | `1fc793a2…b45dbf` equal | `1fc793a2…b45dbf` equal | 59251 |
| S132 | `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea` | `8871d19c…1922ea` equal | `8871d19c…1922ea` equal | 10269 |

No dynamic-chrome drift on any of the three, so no `--extract` fallback comparison was needed; each quote was nevertheless also checked against the extracted text of today's *live* bytes: `S075 live_present=True`, `S090 live_present=True`, `S132 live_present=True`.

## Located context (from `measure.py --extract`, exit 0: S075 53082 B, S090 14288 B, S132 6814 B)

- S075, extract idx 12420 (9 tokens): `… Filtering -e trace = syscall_set -e t = syscall_set --trace = syscall_set Traces only the specified set of system calls. syscall_set is defined as [ ! ] value [ , value ], and value can be one of the following: |QUOTE syscall Traces specific system call, specified by its name| (see syscalls(2) for a reference, but also see NOTES ). ? value …`. Raw HTML at the same point: `<b>Filtering</b>` heading, then the `syscall` definition-list item — body text at the row's anchor (`corpus/SOURCES.md:84`), not title/nav/footer. The quote's odd wording ("Traces specific system call") is upstream's own text, reproduced faithfully; the omitted parenthetical is a cross-reference only, so the claim is not truncated away.
- S090, extract idx 11049 (25 tokens): `… The successful exit is always indicated by a status of 0, or EX_OK . Error numbers begin at EX__BASE … The meaning of the codes is approximately as follows: |QUOTE EX_USAGE (64) The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, a bad syntax in a parameter, or whatever.| EX_DATAERR (65) The input data was incorrect in some way …`. Page header in the same snapshot: `sysexits(3) - FreeBSD 15.1-RELEASE and Ports.quarterly Manual Pages`, page date `May 9, 2024` — matches the row anchor (`corpus/SOURCES.md:99`).
- S132, extract idx 3882 (8 tokens): `… |D28|Effective Snapshot Testing - Kent C. Dodds |https://kentcdodds.com/blog/effective-snapshot-testing | |D29|QUOTE Snapshot Testing: Use With Care - Randy Coulman| |https://randycoulman.com/blog/2016/09/06/snapshot-testing-use-with-care/ | |D30|Episode #86: SwiftUI Snapshot Testing - Point-Free …`. The table is the README's own document list (`# Snapshot Testing: Benefits and Drawbacks |Id |Title |Url |`), so the fragment states the naming claim the row makes (`corpus/SOURCES.md:121`).

## Registry rows read (cells that define what the source must still support)

```
grep -nE '^ {0,3}\| S(075|090|132) ' corpus/SOURCES.md
84:| S075 | strace(1) — Linux manual page — https://man7.org/…/strace.1.html | … | supersedes S060's anchor only: the syscall filter the lane collector actually passes | §Filtering `-e trace=syscall_set` … | … the collector passes an explicit list (…) not `%file`; … `-f` is under §Tracing, not §General | mined | 2026-10-20 | …
99:| S090 | sysexits(3) (FreeBSD 15.1 manual page) — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | … | §ERRORS, EX_USAGE entry @ FreeBSD 15.1 page dated May 9, 2024, fetched 2026-10-22 | EX_USAGE (64) The command was used incorrectly … | mined | 2026-10-22 | …
121:| S132 | Snapshot Testing document table — https://raw.githubusercontent.com/…/README.md | … | README row D29, raw README opened 2026-10-24, sha256 8871d19c | the table names Snapshot Testing: Use With Care among its primary documents | mined | 2026-10-24 | …
```

All three are in the population (status `mined`, id ≤ S160, row URL byte-equal to the entry URL). Quote-length and copied-from-row guards checked independently: `quote_in_cells=False` for all three (fold-normalized containment test against source+scope+anchor+teaches), token counts 9 / 25 / 8.

## Counter (permitted `--check`, freeze rev — never the deciding run)

```
python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecJudge09/S###.json --snapdir /tmp/tameshi-r45-ExecJudge09
CHECK S075 verified ok   exit=0
CHECK S090 verified ok   exit=0
CHECK S132 verified ok   exit=0
```

(`S###.json` = the ledger entry verbatim; `S###.raw` = the decompressed snapshot.)

## Notes / risks (no dispute raised)

- S075 and S060 are two rows over one page (`man7.org/…/strace.1.html`); the two entries carry the same `raw_sha256` and different quotes, so no double counting of a single quote, but L1 may want the shared-URL fact on record.
- S090's quote is exactly 25 tokens — the upper bound of the 6-25 window; any later shortening of that sentence upstream would drop it, so the entry is at the edge of the predicate.
- S132's quote is a table cell: it states the document title only, which is the whole of that row's teaches claim, but it cannot carry any stronger assertion about the document's content.
- Environment: `/tmp` is a separate 128 G filesystem and was at 100% (`df -h /tmp`: 787 M avail) mid-run — one `cp` batch failed `No space left on device` before succeeding on retry; inodes 85% used. Peers writing large fixtures under `/tmp` (e.g. `/tmp/r35audit13` 15 G, `/tmp/tameshi-r45-ExecGtestMirror` 3.9 G) are close to exhausting it; a full `/tmp` will silently break other seats' fetch/extract steps.
- Tooling: nothing installed or updated; no pacman/uv/npx transaction attempted (pacman transactions are paused host-wide).

## Files written

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-45/w2/ExecJudge09.md` (this report)
- `/tmp/tameshi-r45-ExecJudge09/reviews.json` (3 reviews, all `agree`, `report` = `.ufo/waves/round-45/w2/ExecJudge09.md`)
