# Round 38 — self-assessment reconciliation (calibration) + golden-comparison three-outcome verdict (depth)

lane: tameshi · round: 38 · L1: TameshiR38 (Kimi fresh L1) · date: 2026-10-24
contract: `.ufo/evidence/round-38/contract.json` (frozen before any data run; base rev
`ea8f14aa5780084dc96a0fb0d2a50fd35eb93c8a`)

## Gate

Theme: golden / snapshot fixture discipline (frontier row **F4**, open in
`corpus/README.md`). One theme, one knowledge entry admitted, two registry rows cited by
it and nothing else.

### Candidates considered

| candidate | source ids | decision |
|---|---|---|
| `golden-comparison-verdict.md` (staged, round 1) | S105, S106 | **admitted** — re-grounded by this round; PROVINCE scope ok (the lane owns the reusable verification-fixture method); QUALITY bar met (observation separated from inference; boundary stated) |
| `r3-golden-comparison-vendor-verdict.md` (staged, round 3) | S127 | **rejected** — same theme and a second vendor, but this round admits one entry per opened source pair; S127 was not opened by this round, and a row this round cannot re-ground may not be written. Flip: a later round that opens S127 itself may admit it |
| `r8-golden-update-flag.md` (staged, round 8) | S161, S162 | **rejected** — the update-flag half of the theme is already carried by S106's located quote; a second entry would restate the same ground without adding an opened source. Flip: a round that opens S161/S162 and shows the update path in a different comparator may admit it |
| `r3-snapshot-fixture-update-paths.md` (staged, round 3) | S0xx | **rejected** — snapshot practice is a different surface from the exit-status lattice; admitting it would widen the theme beyond one. Flip: a round whose theme is snapshot practice may admit it |

### Admitted (1) — rows opened and re-grounded by this round

**S105 — POSIX `diff` utility specification (The Open Group Base Specifications Issue 7)**
URL `https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html`
accessed 2026-10-24; fetched bytes sha256 `dda9f57dac3b2420966b5f4d14417b84dfc76ac7c4bb14ead5e901af86a1de5a`
(792 lines). Anchor: §EXIT STATUS (lines 564-574) and §ENVIRONMENT VARIABLES, entries LANG
(162), LC_ALL (166), TZ (191).
Located quote (14 words, §EXIT STATUS, lines 564-574):
"0 No differences were found. 1 Differences were found. >1 An error occurred."

**S106 — Package golden provides a function for comparing arbitrary text data to a golden
file (google/golden)**
URL `https://raw.githubusercontent.com/google/golden/master/golden.go`
accessed 2026-10-24; fetched bytes sha256 `4b2c2ad039c45a548216588cc38bb954c3356d3d76b675e7e09a019f02de4e9f`
(113 lines). Anchor: `Compare` doc comment (lines 72-73) and the `shouldUpdateGolden()`
branch (line 78).
Located quote (21 words, `Compare` doc comment, lines 72-73):
"If the -update_golden flag is set, this function will overwrite the contents of goldenFile with the actual value."

The campaign's `opened` date (2026-10-23) and its quotes prove nothing about this lane;
both sources were fetched by this round's writer on 2026-10-24 and the quotes above are
located in the bytes this round fetched.

### Rejections carried in the standing registry (touched this round)

No standing row's `status`, `recheck` or `used-by` changed this round, except that the
**SCORECARD standing `sources-registry` row** was re-stated (99 -> 103 rows) because the
lane registry now holds 103 rows; the row count is the thing the frozen calibration
counter checks, so leaving it stale would be a self-assessment mismatch, not a curation
decision.

### Assimilation mechanics (item 10) — receipts

- Source repo read-only: `/home/vgpnk/Projects/shokuknow` was read only. No campaign tool
  was run there.
- Id collision check, scratch, with the 0-3-leading-space extractor:
  `reg-ids=101 staged-ids=96 collisions=0` (`.ufo/waves/round-38/assimilation/reg-ids`,
  `staged-ids`, `collisions`). The lane's ids run S001-S104 and the staged set runs
  S105-S200, so no id is renumbered and no citation is re-pointed.
- Guard proof (the guard must be shown able to fail): a scratch registry with the indented
  row `  | S002 |` produced `collisions=1` under the 0-3-space pattern and `collisions=0`
  under a column-zero-only pattern. The guard is not vacuous.
- Staged rows are campaign-schema and a byte-exact append fails the lane's own census
  (the staged rows carry NF=14, i.e. 12 columns, because their `recheck` cells hold
  escaped pipes). The append block was therefore transformed in scratch: `recheck` reduced
  to a bare cadence (`365d` / `180d`, the re-verify commands recorded here and in the
  knowledge entry's `recheck:` field), no literal or escaped pipe in any cell, `used-by`
  naming exactly the one admitted entry that cites the row, `status` = `mined`, `opened`
  = this round's access date, `teaches` = 18 and 22 words.
- Validate before append: the scratch mirror
  (`.ufo/waves/round-38/assimilation/validate/`, a copy of the lane `corpus/` plus the
  append block plus `tools/`) was gated with
  `scripts/sources-census.sh validate --file .ufo/waves/round-38/assimilation/validate/corpus/SOURCES.md`
  -> **exit 0** (warnings only; `.ufo/waves/round-38/assimilation/census-scratch.stdout`).
  Only then were the two rows appended to `corpus/SOURCES.md` (101 -> 103 rows).
- Quarantine: the tameshi slice of the campaign absent-defect register was derived with the
  contract's `awk` into `.ufo/waves/round-38/assimilation/quarantine-slice`. Every row in
  that slice is quarantined and none was adopted this round: adoption would require a
  hand-check of each cited source, and this round adopted nothing from the register.
  A prose reason class ("could not be fetched", "named no locator") marks a row
  *unreachable*, not fabricated.

### considerthese (mined once)

One unimplemented proposal from `considerthese/2026-10-24.md` is mined this round:
**proposal 2, "Unreachable-provenance check"** — "Flag any receipt that cites a revision not
reachable from the lane repo." The pointer it names was opened: the round-36 empty-panel
receipts cite `91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`, which is absent from the lane
object database (`git cat-file -e` fails) and which round 37 had to supersede with a
committed specification. Grounded through that pointer, the proposal becomes QUALITY
criterion 76 and is carried by claim C1's counter, which counts self-assessment
divergences against the observed tree. No other proposal was mined.

### Spot-check request (for the round's non-author closure)

Re-open S105 and S106 from the URLs above and confirm: (a) the located quotes are verbatim
in the fetched bytes and within 25 words; (b) the anchored line numbers still point at
those quotes; (c) the admitted entry's three-outcome table is carried by the quotes and
makes no claim beyond them; (d) at least one admit and one reject in this Gate are agreed
or disagreed with, each with a reason.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| self-assessment drift — a standing SCORECARD row stated a registry row count (99) that the committed registry did not hold (101) | `.ufo/evidence/round-35/c2/c2-measure.py` class m6 at `ea8f14aa5780084dc96a0fb0d2a50fd35eb93c8a`: "MISMATCH m6 SCORECARD standing row says 99 rows, SOURCES.md has 101" | QUALITY criterion 76 (new this round) | the standing row is re-stated to the count the committed registry holds (103 rows after this round's two appends), and the frozen counter re-checks it at every deciding run |
| misrooted seat output — a lane seat report was written into the fleet root instead of the lane repo, so the lane's own record counted one residual report fewer than it claimed, and the round-37 closure routed the mismatch | fleet root `.ufo/waves/round-37/residual/ResCorrections.md` (untracked, tameshi-attributable) against the lane's `.ufo/waves/round-37/residual/` (5 files) | QUALITY criterion 77 (new this round) | the file was copied byte-exact into the lane repo (cmp verified, sha256 `46ff0665557454638b91fde3630688802aa8a08dd77bf77fd49da9a7f4a82115`), the fleet-root copy and its empty directories were deleted, and the frozen counter's class m3 now reads zero |
| campaign-schema append — the staged rows would have been appended byte-exact and would have failed the lane's own census (NF=14 rows, escaped pipes in `recheck`) | `.ufo/waves/round-38/assimilation/append-block.md` (transformed) vs `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` lines 7-8 | CORPUS.md rule 4 and the census gate | the append block was transformed in scratch and gated with the census on a scratch mirror (exit 0) before the first append |

## Holds

- The lane's own gates were **not** audited for expected-value write paths: F4's census
  measurement ("update paths that write expected values without an explicit flag") is
  still unmeasured. This round admits the rule, not the measurement.
- `cmp`, `git diff --exit-code` and other comparators have their own exit lattices; the
  three-outcome rule is scoped to POSIX `diff` and is not generalised.
- The generalisation of the rule to the lane's own fixtures is a later round's work; no
  fixture in the lane's tool chain was changed to a golden comparison this round.
