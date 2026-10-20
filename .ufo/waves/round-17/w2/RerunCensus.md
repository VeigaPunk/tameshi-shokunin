# RerunCensus — census re-execution at eb7838b (round-17, wave 2)

Target rev: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (lane `master`).
Execution clone: `/tmp/tameshi-r17w2-RerunCensus-smuLoR/fleet/tameshi-shokunin`, fleet-mirror layout, detached at the rev.
The clone's `corpus/SOURCES.md` is byte-identical to the rev blob: file sha256 `ac82b2df0ffd44f4e3e74e90cdae2a2eac6bc72ed557dd428c45397f97c828d5`, blob `4191202bfb2b9b3246319db7248896982ef32731`; the live lane file has the same sha256.
No tool installs or updates were needed; host `gawk 5.4.1` / `bash 5.3.20`. Census script sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.

## 1. Maintained validate — live lane, read-only

```
$ cd /tmp && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

- No `E`-code findings. `W04` is in the warning band: script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:16` ("exit: 0 clean or warnings"), `:18` ("lanes never change status"), `:33` ("W04 ... warnings do not affect clean lanes"); the message is emitted at `:645`.
- The two warnings are pre-existing, not introduced by the round-17 delta: the same two `W04` lines appear at `98bea7d` (validate `--file` on an exported tree of that rev; exit 0, same `S047`/`S048` text, plus `ok`). Rows `S047`/`S048` are identical in both revs (`corpus/SOURCES.md:56-57`), and `corpus/SOURCES.md:188-189` records why they share the PIT URL ("same PIT URL, no new source").
- Read-only confirmed: after the run the live file sha is unchanged and `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain corpus/SOURCES.md` is empty.

## 2. Frozen manual census — CORPUS.md:131-149, run on `git show eb7838b:corpus/SOURCES.md`

Commands are the block at `/home/vgpnk/Projects/shokunin/CORPUS.md:131-149`, run verbatim on the rev blob (and again on the checkout, identical); the `used-by` existence snippet was run from the clone lane root so the paths resolve. Results:

| check | command outcome (`corpus/SOURCES.md` at eb7838b) |
|---|---|
| rows | **62** |
| malformed rows (NF!=13) | **0** |
| tier histogram | **A=54 B=6 C=2** (sums to 62) |
| status histogram | **mined=35 queued=24 rejected=3** (sums to 62) |
| duplicate ids | empty (must print nothing) |
| enum violations / tier inflation | empty (must print nothing) |
| mined rows with missing `used-by` | empty (must print nothing) |

All three "must print nothing / must print 0" expectations in the frozen section hold.

Independent maintained-parser cross-check, same file:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file <clone>/corpus/SOURCES.md
file	rows	62
file	tier.A	54
file	tier.B	6
file	tier.C	2
file	status.mined	35
file	status.queued	24
file	status.rejected	3
FLEET	rows	62
FLEET	tier.invalid	0
FLEET	status.invalid	0
FLEET	missing	0
EXIT=0
```

The live lane run (`census --root /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokunin/tameshi-shokunin`) prints the same 62 / 54 / 6 / 2 / 35 / 24 / 3 with `invalid 0`, `missing 0`, exit 0. Manual numbers and maintained numbers agree exactly.

New-row column detail (`corpus/SOURCES.md:67-73`): every row `NF=13`; all `status=mined`, `opened=2026-10-20`, allowed `recheck` values (`730d`, `90d`, `on-release`, `180d`); `used-by` is `corpus/knowledge/input-keyed-coldread-credit.md` for S058/S059/S060/S064 (sha256 `1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c`) and `corpus/lessons/round-17.md` for S061/S062/S063 (sha256 `0047f2492b0e0d273ebb96ee85c7f88ff1fa5a606ad3c6a066df927a16ca0dc5`); both files exist at the rev.

## 3. Delta `98bea7d..eb7838b` on `corpus/SOURCES.md` — did any prior row change?

No. `git diff --numstat` is `9	1	corpus/SOURCES.md`; `--stat` reports 1 file changed, 9 insertions(+), 1 deletion(-). With `-U0` the deleted lines are exactly one, the footer line `- Next unused id: S058.`; the added lines are the seven registry rows `S058`–`S064` (new lines 67–73), the new allocation bullet `- S058–S064: round-17 rows (...)` (line 194), and `- Next unused id: S065.` (line 195). The hunk is `@@ -64,6 +64,13 @@`.

Row-only diff (both revs filtered to `^\| S[0-9]{3,}`) prints only `55a56,62`: a pure append of 7 lines after row 55. Every one of the 55 pre-existing row lines is byte-identical across the range, so no prior row's `status`, `recheck`, `used-by`, or any other cell changed in place.

Census at `98bea7d` for the delta: rows **55**, malformed 0, **A=47 B=6 C=2**, **mined=28 queued=24 rejected=3**, missing 0. Delta to eb7838b: +7 rows, +7 tier A, +7 mined; tier B/C and queued/rejected unchanged — exactly the seven new A/mined rows, internally consistent.

## 4. Non-blocking observations

- The id list has a gap at `S038`/`S039` (id-continuity check `seq 1..64` minus present ids returns `S038 S039`). This is recorded as intentional at `corpus/SOURCES.md:183-185`: "S038–S039 allocated, never written, retired — never reused or renumbered ... A census gap at S038–S039 is this note, not a lost row." Not a census defect and unchanged by this delta.
- `S047`/`S048` `W04` is a documented cross-scope duplicate (`corpus/SOURCES.md:188-189`), warning band, exit 0; present identically at `98bea7d`.
- `corpus/SOURCES.md:191` (S050 allocation note) reads `measured at6431478` — missing space before the commit id. Pre-existing at `98bea7d` (line 184), outside this diff, not a registry row, no validator/census effect; noted only as calibration observation.
- No `E12` row-shaped source outside `## Registry`, no duplicate ids, no enum violations appeared in any run.

## Verdict

**Holds** — at `eb7838b16490ca7ba17ea3242ade76a61f744af2` the live-lane `validate` exits 0 with only the two pre-existing `W04` warnings, the frozen manual census reads 62 rows / 0 malformed / A=54 B=6 C=2 / mined=35 queued=24 rejected=3 with every "must be empty/0" check empty, and the `98bea7d..eb7838b` diff of `corpus/SOURCES.md` is a pure seven-row append (S058–S064) plus the `Next unused id` footer update, with no prior row changed.
