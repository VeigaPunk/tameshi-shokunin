# T54W1ExecDryBinder — dry-run binder input map (round 54, w1)

Seat: T54W1ExecDryBinder (leaf executor, calibration axis).
Item: for each of the 23 headings in `.ufo/evidence/round-54/c1/lost-headings-at-c0.json`, read the
cold-read ledger at C0 and union the section's prior entries' input paths; flag every path that is
(a) absent at C0, (b) `LOG.md`/`SCORECARD.md`, or (c) a file this round still edits. Name any heading
whose map is empty or entirely unstable.

**Deliverable:** `.ufo/waves/round-54/w1/T54W1ExecDryBinder-input-map.json`
(sha256 `8d8e7b416a33756a578d7dfe4d3ea1e31158275918c2c277cffa21620637cf96`, 1,422,436 bytes,
23 objects, key set exactly `{heading, inputs, dropped, unstable}`, heading order identical to
`lost-headings-at-c0.json`).

**Builder (runnable receipt):** `.ufo/waves/round-54/w1/T54W1ExecDryBinder-receipts/build-input-map.py`
(sha256 `e69ac1cde9cab83c8c756c99cc886434579065b6570d25530c3d8b7d3f6b9d6c`).
**Classifier:** `.ufo/waves/round-54/w1/T54W1ExecDryBinder-receipts/classify-headings.py`
(sha256 `d82beff8bfe3fc3e7f4f088aaeb0be3efdd128fefefc45dcdd916bcff1440601`).

No lane production file, counter, contract, freeze, ledger, wave spec or registry was edited. No
tool was installed (nothing needed installing).

## Method (exact commands)

The shipped builder hardcodes the lane path, so it runs from anywhere; this is the run that produced
the deliverable and the second run that reproduced the same sha256:

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r54/T54W1ExecDryBinder
export TMPDIR=$S/tmp && mkdir -p "$TMPDIR"
cd "$S"
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ExecDryBinder-receipts/build-input-map.py
```

The builder reads the ledger at C0 (`git -C <lane> show 59c38109bf11:.ufo/evidence/round-21/coldread/ledger.json`,
568 entries), selects every entry whose `heading` string equals the heading byte-for-byte, unions the
keys of each entry's `inputs` object (lane-relative paths — this is the field `inputs_view()` in
`.ufo/evidence/round-18/measure.py:321-327` verifies), computes
`sha256(git show C0:<path>)` for each path, and classifies:

- `dropped` = (a) `git show C0:<path>` does not resolve to a blob;
- `unstable` = (b) basename is `LOG.md` or `SCORECARD.md`, or (c) the path is in the round-54 edit set.

The round-54 edit set used for (c) is the union of
`git -C <lane> diff --name-only d33053f7552d..59c38109bf11` (20 paths: 11 under `.ufo/evidence/round-54/`
— assimilation, both counters, contract, controls, deciding-run, freeze, no-harm, `lost-headings-at-base`
— plus `SKILL.md`, `corpus/SOURCES.md`, `corpus/knowledge/scratch-root-contract.md`,
`corpus/lessons/round-54.md`, `tools/env-diff.py`, `tools/bash-witness-study.py`,
`tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry.json`) and
`git -C <lane> diff --name-only` (working-tree dirty: `corpus/QUALITY.md`).

## Result

All 23 headings produced a **non-empty** map, and **no** heading's map is entirely unstable, so no
section is unkeyable on this axis. Totals: 11,281 path entries across the 23 maps (7,725 distinct
paths; 3,556 entries are repeats of a path already listed under another heading), 0 dropped, 99
unstable flags over 10 unique paths: `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md`, `tools/bash-witness-study.py`, `tools/env-diff.py`,
`tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/registry.json`. The builder is
deterministic: two runs produced the same 23-object file with the same sha256. Builder stdout (first,
an interior and the last line; the full run is 24 lines, one per heading plus the `wrote` line):

```
wrote /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ExecDryBinder-input-map.json headings=23
## Standing rules                                                        prior=7 inputs=2500 dropped=0 unstable=9 
### The boundaries — what a service run is not                           prior=7 inputs=9 dropped=0 unstable=0 
### Round-26 gate/probe registry — report interop                        prior=4 inputs=74 dropped=0 unstable=5 
```

Per-heading table. `sha-hit` = at least one prior entry already carries the C0 section sha256 (so the
re-key only needs the input map); `sha-miss` = no prior entry does, so the re-key must also bind the
C0 section sha. `drift` = input paths of that heading's **last** ledger entry that fail at C0
(`input-drift`, excluding `IGNORED_INPUTS`).

| heading | C0 lines | C0 section sha | prior | map | eff | uns | drift | bind |
|---|---|---|---|---|---|---|---|---|
| ## Standing rules | 17-40 | `164390276b45` | 7 | 2500 | 2499 | 9 | 7 | sha-miss |
| ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | 142-256 | `c413b4268eb8` | 28 | 7706 | 7704 | 10 | 8 | sha-hit |
| ### The boundaries — what a service run is not | 869-893 | `9aa3c41cfd36` | 7 | 9 | 9 | 0 | 0 | sha-miss |
| ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | 932-945 | `430dd86f25b6` | 10 | 30 | 30 | 1 | 1 | sha-hit |
| ### Using the ledger | 946-977 | `808dad50760d` | 9 | 6 | 5 | 1 | 0 | sha-miss |
| ### The tick and the pin read | 1034-1082 | `ca86e98de294` | 10 | 29 | 29 | 1 | 1 | sha-hit |
| ### Triggers T1–T3 and the re-pin rule | 1083-1105 | `2350210704ef` | 11 | 89 | 89 | 6 | 5 | sha-hit |
| ### The service's limits — what tameshi refuses to mutation-test | 1265-1294 | `37d63abf882e` | 11 | 40 | 39 | 5 | 4 | sha-hit |
| ## The operator's runbook and the six-leg regression (round 10, measured) | 1295-1303 | `636e850f885c` | 15 | 12 | 11 | 2 | 1 | sha-hit |
| ### The operator's runbook — `corpus/knowledge/operator-runbook.md` | 1304-1324 | `c246d3743e0a` | 5 | 3 | 3 | 0 | 1 | sha-hit |
| ## Repeated controls and gate registry — round 12 | 1504-1523 | `2613c4fe5c89` | 20 | 169 | 168 | 3 | 2 | sha-hit |
| ### Gate/probe registry | 1524-1541 | `99285e24a71a` | 13 | 125 | 124 | 2 | 1 | sha-hit |
| ## Pin disposition and provenance correction — round 13 | 1542-1572 | `ad8d6c4010f2` | 24 | 34 | 33 | 4 | 3 | sha-hit |
| ### Round-13 gate/probe registry | 1573-1588 | `896722c49418` | 21 | 25 | 24 | 4 | 3 | sha-hit |
| ## Effective expectation reconciliation — round 14 | 1589-1622 | `9640e5dc426f` | 18 | 43 | 42 | 5 | 4 | sha-hit |
| ### Round-14 historical registry — superseded by round 15 | 1623-1634 | `06a6864fb05f` | 4 | 25 | 24 | 4 | 2 | sha-hit |
| ## Context gate classification and explicit exit classes — round 15 | 1635-1701 | `132cfb9ef1aa` | 19 | 43 | 42 | 6 | 5 | sha-hit |
| ### Round-15 gate/probe registry | 1702-1732 | `da6ef23c23f0` | 6 | 39 | 38 | 4 | 3 | sha-hit |
| ## Live-tree re-pin and entry-command monitor — round 17 | 1840-1871 | `037c9df3076f` | 21 | 79 | 78 | 8 | 6 | sha-hit |
| ### Round-17 gate/probe registry — re-pin and monitor | 1872-1880 | `8a92f71e046a` | 14 | 52 | 51 | 7 | 6 | sha-hit |
| ### Round-18 gate/probe registry — routed-defect closure | 1951-1963 | `1f0a60ec9983` | 19 | 72 | 71 | 7 | 5 | sha-hit |
| ### Round-21 gate/probe registry — finite environment differential | 1990-2129 | `eccd3ec82207` | 16 | 77 | 75 | 5 | 3 | sha-hit |
| ### Round-26 gate/probe registry — report interop | 2158-2197 | `cc23587b353f` | 4 | 74 | 74 | 5 | 10 | sha-miss |

`eff` = map size after dropping the counter's `IGNORED_INPUTS` (`SKILL.md`, the round-17 and round-21
ledger paths, `.ufo/evidence/round-18/measure.py:135-136`). `uns` counts unstable flags over the full
map, so the difference `map - eff` is exactly the ignored paths.

C0 line ranges and section shas come from
`python3 .ufo/waves/round-54/reader-section.py <lane> 59c38109bf11 "<heading>"`, exit 0 for all 23.
The reader returns the first heading match without checking for duplicates, so uniqueness was checked
separately by running the frozen round-18 `sectionize()` on `git show 59c38109bf11:SKILL.md`:
`64` sections, no duplicate headings, all 23 are members. The table shows 12-char prefixes of each
`section_sha256`; the reader prints any full value on demand, and the four sha-miss sections are given
in full under F2.

## Findings

**F1 — the map explains 19 of the 23 losses; four losses need a section-sha rebind as well.**
For 19 headings a prior entry already carries the C0 section sha256, so the section is bound and only
the inputs block credit. Every sha-matching entry fails `input_reason` at C0: checked per heading over
all such entries (1-19 entries each), the minimum failure count is 1-8 and no sha-matching entry
passes. The `drift` column below reports that heading's **last** ledger entry, which is the one a
writer would most likely carry; it drifts by 1-8 paths as well. The input map is therefore the
complete remaining requirement for those 19. Command and output (verbatim excerpt of the 24-line run):

```
$ python3 .ufo/waves/round-54/w1/T54W1ExecDryBinder-receipts/classify-headings.py
## Standing rules                                           17-40    sha_hit=False map= 2500 eff= 2499 uns= 9/ 8 lastfail= 7 -> section-sha-drift
## Mutation-sweep recipe — numbered steps; bounded cold-   142-256   sha_hit=True  map= 7706 eff= 7704 uns=10/ 9 lastfail= 8 -> input-drift
### The boundaries — what a service run is not             869-893   sha_hit=False map=    9 eff=    9 uns= 0/ 0 lastfail= 0 -> section-sha-drift
...
### Round-26 gate/probe registry — report interop         2158-2197  sha_hit=False map=   74 eff=   74 uns= 5/ 5 lastfail=10 -> section-sha-drift
Counter({'input-drift': 19, 'section-sha-drift': 4})
```

`sha_hit` is computed against the C0 `sectionize()` sha256 (the same value `reader-section.py` prints),
not against the heading string; the two verdicts partition the 23 headings exhaustively, with no
`credited-by-existing-entry` line, i.e. no prior entry credits at C0.

**F2 — the four sha-miss headings are nameable, and three of them are unchanged bytes.**
`## Standing rules` is the one section whose bytes C0 actually rewrote (the scratch-root bullet; base
section sha `09861d2ddad6...`, C0 `164390276b453ddb23bcb3633269217afc8ee9d47a9e470af6fece181a5743f7`,
+8 lines, both read with `reader-section.py`). Its hunk, from a unified diff of
`git show d33053f7552d:SKILL.md` against `git show 59c38109bf11:SKILL.md` restricted to the section's
lines (excerpt: the hunk adds 8 lines; first added line shown):

```
@@ -15,0 +16,8 @@
+- **The scratch root has three arms.** A tool that allocates scratch through
```

`### The boundaries — what a service run is not`, `### Using the ledger` and
`### Round-26 gate/probe registry — report interop` have **identical** section shas at base and at C0
(`9aa3c41cfd365e32cc8e1feb1155e0be96df016dd5ea5c6d3ffa80aa8df3ba63`,
`808dad50760d693bc9e952a32a08cff129a74fd56163876aa3b656f9a9775d04`,
`cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`; only their start lines shift
861->869, 938->946, 2150->2158 because the Standing-rules bullet pushed everything down). Their
sha-miss is not a C0 edit: their last ledger entries were read at revisions whose section text differed
(`02ec217c4d0a`, `651773ab9e32`), and each of those entries does match its own section sha at its own
`read_rev` — verified, so no entry is dishonest, the text simply moved between then and C0.

**F3 — no heading is unkeyable; the maps range from 3 to 7,706 paths.** Nothing is empty and nothing
is entirely unstable. The most stable map is `### The operator's runbook — corpus/knowledge/operator-runbook.md`
(3 inputs, 0 unstable) and the least stable is `### Round-26 gate/probe registry — report interop`
(74 inputs, 5 unstable: all four tool scripts C0 rewrote — `tools/env-diff.py`,
`tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/pin-disposition.py` — plus
`tools/registry.json`; its map does not list `SKILL.md`). Its map still holds 69 stable paths, so it
is re-keyable; the risk is only that a re-key pinning those paths at C0 drifts if the wave edits them
again before the deciding revision.

**F4 — the union is the right shape but larger than the newest map for three headings.** Comparing the
union against the heading's last ledger entry (both after `IGNORED_INPUTS`): 19 of 23 are identical in
size, 1 differs by one path (`### The operator's runbook ...`, 3 vs 2), and 3 are larger —
`### The boundaries — what a service run is not` (9 vs 3),
`### Round-14 historical registry — superseded by round 15` (24 vs 13) and
`### Round-26 gate/probe registry — report interop` (74 vs 70). Of the union's 7,706 paths for the
mutation-sweep heading, 7,704 are already in its newest entry, so the union does not add much there;
the size comes from the heading having been read 28 times.

## What I opened / checked

- `.ufo/evidence/round-54/c1/lost-headings-at-c0.json` (23 headings, order preserved in the JSON).
- Ledger at C0: `.ufo/evidence/round-21/coldread/ledger.json` via `git show`, 568 entries.
- `.ufo/evidence/round-18/measure.py` at C0: `inputs_view` (321-327), `input_failures` (330-350),
  `input_reason` (353-359), `IGNORED_INPUTS` (135-136), `entry_reason` (513-526), the `by_sha` index
  and section->entry matching in `coldread()` (602-612). This is why the map is the right artifact:
  credit is a function of the section sha and the per-entry input shas at the measured revision.
- All 23 section bindings via `.ufo/waves/round-54/reader-section.py` at C0, and the four sha-miss
  sections again at base `d33053f7552d` and at each last-entry `read_rev`.
- Round-54 edit set via `git diff --name-only` (committed and working tree) — read-only commands.
- Conformance: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` exits `0` (`tameshi ok .../corpus/SOURCES.md`; the W01/W04
  lines are pre-existing advisories), and `git show 59c38109bf11:corpus/SOURCES.md` carries 139
  `| Snnn |` rows with S277-S279 present.
- Re-checked at the end of the run against the then-current `git diff --name-only` (siblings were
  editing concurrently: `M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/SOURCES.md`,
  `M corpus/knowledge/change-aware-resweep-cadence.md`, `M corpus/lessons/round-54.md`,
  `M tools/env-diff.py`). Every dirty path that occurs in any of the 23 maps is flagged unstable;
  `corpus/knowledge/change-aware-resweep-cadence.md` occurs in none of them, so the map needs no
  rebuild for it.

Validation sweeps run (all clean):

```
# every input path entry is a blob, not a dir/gitlink, at C0 (11,281 path entries)
$ git -C <lane> cat-file -t <C0>:<path>   # x11281
non-blob inputs: [] 0
# emitted JSON shape
objects 23 keysets {('heading', 'inputs', 'dropped', 'unstable')}
heading order preserved: True
all shas 64 hex: True
dropped total 0
unstable total 99
```

## Risks / limits

- `inputs` is only the entries' lane-relative map. `external_inputs` (cross-lane reads such as
  `kumitate-shokunin@...`) are deliberately excluded: they are not lane blobs, so every one of them
  would report `dropped` and the flag would stop meaning "absent at C0".
- `unstable` is path-based, as specified: a path is flagged if this round edits it, not if its bytes
  changed relative to the reading. A file the wave touches *after* the build is therefore not flagged;
  `corpus/QUALITY.md` is flagged only because it was already dirty. The list is a snapshot of
  `git diff` at build time, not a promise about the deciding revision.
- `SKILL.md` appears in 17 of the 23 maps and is always flagged unstable (C0 edits it). It is also in
  `IGNORED_INPUTS`, so pinning it can never fail a credit; the flag is correct but not load-bearing.
  The round-21 ledger appears in 2 maps (`## Mutation-sweep recipe ...`, `### Round-21 gate/probe
  registry ...`) and the round-17 ledger in none; both ledger paths are in `IGNORED_INPUTS` too, so
  they cannot fail a credit and neither is flagged unstable (this round does not edit them).
- The builder trusts ledger order for "last entry"; 19 of 23 headings share last-read rev
  `651773ab9e32`, which is consistent with a single carried read, but the field is not a timestamp.

## Receipts

- `.ufo/waves/round-54/w1/T54W1ExecDryBinder-input-map.json` — the map (23 objects).
- `.ufo/waves/round-54/w1/T54W1ExecDryBinder-receipts/build-input-map.py` — the builder, runnable as
  documented above; it writes only the map.
- `.ufo/waves/round-54/w1/T54W1ExecDryBinder-receipts/classify-headings.py` — the classifier behind
  the table and F1; it derives the lane path from its own location and writes nothing.
- Scratch `$HYAKU_SCRATCH/tameshi-r54/T54W1ExecDryBinder/` is removed on exit
  (`trap 'rm -rf -- "$S"' EXIT`). The two receipt scripts recompute every number in this report from
  git objects alone; no intermediate file is needed to reproduce it.
- No tool installed, upgraded or removed; no `pacman`/`uv`/`npm` transaction run.
