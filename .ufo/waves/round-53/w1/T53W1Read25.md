# T53W1Read25 — cold-read of `### The six-leg regression — usage and this round's receipt`

Seat T53W1Read25 (lane repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, wave 1 of round 53).
Section read at content commit **C\* = `a41195dfc13a73958e4c5228ec196b28d03ded03`**, via git objects
only (`git -C <lane> show C*:SKILL.md`); the working tree was never the source of the bytes.

- heading: `### The six-leg regression — usage and this round's receipt`
- section span at C\*: 1-based lines **1308–1370** (63 lines; next heading
  `## Final pointers — the standing map at the arc's close (round 11, measured)` starts at 1372),
  trailing whitespace-only lines stripped, joined with `\n`, no trailing newline
- `section_sha256` = **`45fe934f6254c9f95e20f8444f4a6a435d1c818e07f84290e1a4a0de8b119232`**
- the heading is one of the 30 headings frozen in `.ufo/evidence/round-53/c1/lost-headings.json`
  (checked at C*: the file has 30 entries; both this `###` and its parent `##` are listed)

## Checks run

| # | check | outcome |
|---|---|---|
| 1 | `git show C*:SKILL.md` into scratch | 2178 lines, sha256 `c329d3c150200ff32c47cb218800fb87c014345a7f342e1b11c70f5cacfc83ee` |
| 2 | frozen splitter — `.ufo/evidence/round-18/measure.py:sectionize`, loaded with `importlib` (never reimplemented for the record hash) | unique match `start=1308 end=1371` (end exclusive), `sha256=45fe934f…`; 64 sections at C* |
| 3 | independent reimplementation of the same rule (fence toggle on `line.strip().startswith('```')`, regex `^#{1,3}(\s|$)`, strip trailing blank lines) | same span 1308–1370, same `45fe934f…` — the two agree |
| 4 | `git show C*:tools/mutate-and-run.sh` | 2159 lines, mode `100755`, blob `51fa5bc8`, content sha256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda` |
| 5 | `git diff --stat bcba8924 C* -- tools/ SKILL.md` | `tools/mutate-and-run.sh` **unchanged** between CAND0 and C* (the 7 C2-patched tools are `bash-witness-study.py`, `context-capture.py`, `env-diff.py`, `evidence-disposition.py`, `pin-disposition.py`, `registry-check.py`, `repeat-control.py`); SKILL.md differs |
| 6 | read every tool anchor the section carries, at C* | `:88-97` (ten leg lines), `:98-121` (sources), `:614-643` (pins+tables), `:850`/`:925` (leg-5/leg-6 spec heads), `:128-130`+`:1281-1302` (mode mirror), `:139-143` (exit map), `:1446` (`REGRESSION_EXPECT`), `:1459-1507` (ten dispatches), `:1860-1896` (exec-bit selftest arms), `:2024` (embedded-ledger check) — all resolve |
| 7 | parse `PIN_*`/`REV_*`/`TABLE_*` at C* and recount killed/total | `8/10, 8/10, 6/10, 4/10, 7/15, 7/10` — all six table rows of the section agree, and every recorded rev (`175de6ba`, `fecee874`, `165307fe`, `eead56b2`, `fecee874`, `175de6ba`) matches its `REV_*` |
| 8 | ledger at C* (`corpus/knowledge/fleet-kill-rate-ledger.md`, 441 lines) | `:85-88` reads "**cases 1 and 2 only**"; `:272` is the `**ER-2` heading and `:281` (inside it) reads "carries **four** materialized legs … `REGRESSION: PASS (cases=4 passed=4; …)`" |
| 9 | runbook at C* (`corpus/knowledge/operator-runbook.md`) | §7 lands at `:345`; `:374` reads "four legs at this revision (cases 1–4); cases 5/6 are **not embedded**" |
| 10 | `git show 6db1d220:SKILL.md` (base) for provenance of both findings | base `:925` = "Four legs at that revision …"; base `:1226-1228` contains "still not embedded … named debt" |
| 11 | `grep -n 'still not embedded' SKILL.md` at C* | only `:1281` (round-10 section) and `:1354` (this section) — **not** `:1226-1228` |
| 12 | `grep -n 'that revision' SKILL.md` at C* | only `:1352` (this section) |
| 13 | `git cat-file -t` on `75ed934d`, `cf41efaa`, `bcba8924`, C* | `75ed934d`/`cf41efaa` are **not** commit objects (they are tool content-sha prefixes, per `SKILL.md:1006`); `bcba8924` and C* are commits — so the section's "tool revision `75ed934d…`" / "stand at `cf41efaa…`" phrasing is sha-addressed, not a dead revision pointer |
| 14 | repo grep for `75ed934d` | `corpus/knowledge/closeout-r11.md:69` pins it to `75ed934dc86360f5…` (r10-2, 1 642 L, committed at `606716f`); `:301`/`:357`/`:382` agree; `:309-310` pair it with `--selftest 80/80` and the 21:00:24Z / 21:02:39Z receipts |

## Holds (pointers and counts verified against C\* bytes)

- Header anchors: `list :88-97` is the leg list (ten entries at C*, consistent with "ten since round 51");
  `sources :98-121`, `pins/tables :614-643`, `specs :850`, `:925`, `registry :1459-1507` all land on the
  described objects. The "line anchors re-read at CAND0 `bcba8924…`" claim is also true: the tool is
  byte-identical at CAND0 and C* (check 5), and the anchors resolve there too.
- Six-row table: every recorded rev and rate matches the pinned constants and the embedded tables (check 7).
- "**default scratch `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX` (TMPDIR honoured since r51)**":
  code at `:1432` and the r51 comment at `:149-150` agree.
- Scratch lifecycle ("removed on PASS unless `--keep`, kept on FAIL/SETUP, never removed when `--workdir`
  was given"): the `auto`/`KEEP` block `:1522-1547` — PASS+auto+no-keep removes (`:1542-1544`), FAIL keeps
  (`:1522`), SETUP keeps (`:1528`), `--workdir` sets `auto=0` (`:1434-1436`). Holds.
- Exit map `0/1/2` at `:139-143`; the r30 tally-SETUP branch listed there is also labelled SETUP, so the
  section's three-way summary is not contradicted.
- "Each `REGRESSION_PIN` line now carries the blob's `mode=`": printf at `:1302`; mode mirror at
  `:1285-1300`; selftest arms at `:1860-1896`; the embedded-ledger check at `:2013-2035` with leg-count
  agreement `calls=10 specs=10 nlegs=10` at `:2030-2034`. Holds.
- "`REGRESSION_EXPECT` lists … ten at CAND0 (`:1446`)": ten paired arguments printed at C*.
- The "107/107 at CAND0" parenthetical: CAND0's tool content sha is `977de470…`, the same runner pin
  `SKILL.md:1006` records for the round-52 `MUTATE_SELFTEST: 107/107 pass` measurement. Holds.
- The receipt's `/tmp/w10-t10-4-ev/` scratch and `80/80` selftest are a **dated** execution record
  (`2026-10-14T21:02:39Z`), corroborated by `plans/round-10-record-draft.md:339-340` (workdir contents,
  `regression.log 21:02:39Z`, `tool-at-run.txt`) and `corpus/knowledge/closeout-r11.md:309-310`. Dated
  milestone → HOLD, not a scratch-directive violation (the host directive is dated 2026-10-25).
- "Named debt, not smoothed": the ledger still carries no row recording the leg registry
  (`grep -n 'registry|six-leg|ten-leg|ten legs'` over the ledger at C* returns nothing), and
  `fleet-kill-rate-ledger.md:85-88` / `:281` read exactly as quoted. Holds.
- "The runbook's §7 is the operator's rendering of this command as of round 10 (four legs then …)":
  runbook §7 `:345`, `:374` "four legs at this revision". Holds.

## Findings (2)

### F1 — the round-7 quote and its "now reads" correction both describe bytes that are gone

Verbatim from the section at C\*:

```
Four legs at
  this revision" (`:925-929`; dated there since round 16; the section now reads "that revision")
```

**Why it fails.** `SKILL.md:925-929` at C* reads, verbatim:

```
replayed at its pinned original revision. Round 7 recorded four legs at
r7-1 (dated milestones: seven from round 16, eight from round 18, nine from
round 26, ten from round 51) — `js-kimi-census`
```

The phrase "Four legs at this revision" is not there, and the asserted correction ("the section now reads
"that revision"") is not there either: `grep -n 'that revision' SKILL.md` at C* returns only the citing line
itself (`:1352`). At the base commit `6db1d220` the claim was true — line 925 read
"Four legs at that revision (r7-1; seven since round 16; …)" — so this round's own fix pass rewrote the
round-7 sentence and left this citation un-rebased. Class: stale cross-reference (self-inflicted drift).

### F2 — the round-9 caveat is quoted and cited at lines that no longer carry it

Verbatim from the section at C\*:

```
the round-9 caveat that cases 5–6 were
  "still not embedded — named debt" (`:1226-1228`; ER-4 caveat (a))
```

**Why it fails.** At C*, lines 1226–1228 read "The legs replay their pinned blobs — git-materialized
(`tools/mutate-and-run.sh:1222-1303`), so the two `stale` substrates cannot move them; re-verified at this
boundary, since all four legs matched while cases 3–4" — the receipt prose, not the cases 5–6 caveat. The
caveat now sits at `:1229-1230`: "Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at
r10-2 …): their rows carried no `REGRESSION` line at this boundary — named debt, not smoothed". The quoted
phrase "still not embedded" survives only at `:1281` (the round-10 section) and in this section itself
(`:1354`), so both the quotation and the line range are stale. At `6db1d220` the range did contain the
phrase ("Cases 5–6 were still not embedded at this boundary … line — named debt, not smoothed"), which is
why the citation was correct when written; the same fix pass that rewrote the round-9 sentence (the
self-contradiction named in `corpus/lessons/round-53.md`, "Mistakes") shifted it. Class: drifted quote +
stale line range.

## Provenance of the drift

Both findings are the class this round's own QUALITY criterion 104 targets — "a citation whose receipt does
not establish the cited clause". Neither is inherited: both citations were accurate against the base commit
`6db1d220` and became false when the fix pass rewrote the referenced sections at C*. Evidence for both
directions is in checks 10–12; the base bytes come from `git show 6db1d220:SKILL.md`, never the working tree.

## Not claimed / out of scope

- The section's dated measurement claims (r10-2 receipt 21:02:39Z, `80/80`, `cases=6 passed=6`, the `mode=`
  pin lines) were **not re-executed**. They are dated milestones with corroborating records (checks 13, 14,
  plus `plans/round-10-record-draft.md`); a re-run would not turn them into present-tense claims, and no
  receipt is contradicted by a C* byte.
- I did not run `--selftest`/`--regression` at C*. The only current-tense numeric claim a run could move is
  the CAND0 `107/107`, already bound to the content sha `977de470…` that the round-52 measurement
  (`SKILL.md:1006`) and the round-51 reads record.
- No finding is raised against the C2 axis from this section: the only scratch default it names for a tool
  honours `TMPDIR` (`:1432`); the runbook §7's hardcoded `/tmp` line belongs to another section.
- The section's aggregate credit (C1_R53) is the L1 counter's to decide; this report claims only the section
  bytes, the hash, and two evidenced findings.

## Tooling and scratch

- No tools installed or upgraded (nothing needed; git + python3 sufficed).
- Scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read25/` (SKILL.md copy, tool copy, ledger/runbook
  copies, section bytes, quote extracts) is deleted before yielding; no file was written outside
  `.ufo/waves/round-53/w1/` and that scratch dir.
- No git/jj mutating command was run anywhere; the only git calls were `show`, `cat-file`, `ls-tree`,
  `diff --stat`, `rev-parse --show-toplevel`.
