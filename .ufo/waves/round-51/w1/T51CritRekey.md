# T51CritRekey — attack on the re-key route C2 and C3 depend on (cold-read constraint)

Seat: T51CritRekey. Lane: tameshi-shokunin. Base: `9962033fd7a75aa2f2847e979dd687a5d28505a1` (lane tip at round start).
Scope: the round-21 cold-read monitor's credit mechanics, the exact set of credited sections that a byte change to
`tools/mutate-and-run.sh` drops, and, per section, the statements a tenth leg (C2) or a TMPDIR-default change could
make false, with what a re-key reader must verify. No claim is decided here; this feeds wave-2 reader items and the L1's re-key.

## 1. Monitor mechanics (how credit drops)

- Round-21 cold-read `measure.py` delegates to the frozen round-18 selector (`.ufo/evidence/round-21/coldread/measure.py:18-21`).
- An entry is credited iff (a) shape/class pass, (b) `commands_executed_count>0`, (c) every recorded input's sha256
  equals the blob at REV (`input_failures`, round-18 measure.py:330-350 → `input-drift:<path>`), (d) traces validate.
- A section is covered iff at least one entry with that section's sha credits and no non-stale entry vetoes
  (round-18 measure.py:611-656). A drifted entry does not veto, but it also stops crediting — so a section whose **every**
  matching entry pins the runner's sha goes uncovered the moment any runner byte changes.
- Command that shows the base state: `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev 9962033…`
  → `sections_covered=64/64`, `reasons: credited 64`, `calibration_restraint_score=8`.

## 2. Confirmed drop set: 20 sections

Predicted from the ledger: sections whose base entry set is entirely runner-pinning (nrunnerpin == nentries > 0).
Confirmed by simulation (scratch clone of the lane at base + one appended byte to `tools/mutate-and-run.sh`, committed
`45ea5934a7b144878b966e81456b72ce803f5d53`; `measure.py --repo CLONE --rev 45ea5934` → `covered=44/64`; receipts
copied: `.ufo/waves/round-51/w1/T51CritRekey-sim-measure.json`, `T51CritRekey-sim-receipt.txt`, `T51CritRekey-selftest.log`).

Dropped (start line / heading):

| start | heading |
|---|---|
| 131 | ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence |
| 375 | ## Restore discipline — before/after identity, not continuous non-write proof |
| 827 | ### The protocol — ordered, fail-closed |
| 858 | ### The boundaries — what a service run is not |
| 921 | ## The leg ledger — replay, receipt, and how it is read (round 7, measured) |
| 933 | ### Using the ledger |
| 965 | ### Reading a receipt — the discipline |
| 1021 | ### The tick and the pin read |
| 1164 | ### The tick, executed |
| 1212 | ### The receipt at this boundary |
| 1272 | ## The operator's runbook and the six-leg regression (round 10, measured) |
| 1302 | ### The six-leg regression — usage and this round's receipt |
| 1380 | ### The map — where a reader enters, artifact by artifact |
| 1499 | ### Gate/probe registry |
| 1754 | ## Seventh recorded case and full-page cold-read — round 16 |
| 1806 | ### Round-16 gate/probe registry |
| 1814 | ## Live-tree re-pin and entry-command monitor — round 17 |
| 1846 | ### Round-17 gate/probe registry — re-pin and monitor |
| 1905 | ## Eighth recorded case — round 18 |
| 2132 | ### Round-26 gate/probe registry — report interop |

If C2 and C3 both land, section 1499 drops twice: once from the runner-input drift (all four entries pin the runner)
and once from its own sha changing when C3 appends rows (`no-ledger-entry`). The re-key must publish a new entry for the
new sha **and** bind the new runner sha.

## 3. Base facts observed (readers will compare against these)

- `bash tools/mutate-and-run.sh --selftest` at base (TMPDIR=scratch) → `MUTATE_SELFTEST: 106/106 pass` / `VERDICT: PASS`, exit 0.
- SKILL.md quotes selftest tallies: `67/67` at lines 1003 and 1064 (both bound in text only to `cf41efaa…`, the round-7/9 tool rev — already inconsistent with the base 106/106 if read as current), `80/80` at lines 1336 and 1424 (historical round-10 receipts at `75ed934d…`, correctly framed).
- The runner's tenth leg will change the regression receipts (`cases=9` → `cases=10`) and grow the selftest tally; every quote above must be re-checked against the new bytes.

## 4. Per-section at-risk statements and reader checks

Runner line anchors cited inside these sections (all shift when C2 edits the runner; anchors are checked by name, not by number):
`tools/mutate-and-run.sh` lines 36-38 (target-never-written), 83-108 (spec inventory header), 85-89 (leg list), 90-97 (sources), 104-106 (mode mirror), 115-119 (exit map), 126-136 (PASS/FAIL/SETUP), 425 (driver `--check` print), 511-522 (pins), 550-559 (pins/tables), 569-574 (DEGRADED division), 597-620 and 603-629 (recorded tables), 657-839 (first-four specs), 733-791 (materialization), 766/841 (spec files), 932-960 (chmod), 1104-1175 (mode/SHA validation), 1132-1141 (registry), 1159-1160 (REGRESSION_PIN), 1273-1294 (statuses), 1364-1384, 1384-1428 (dispatches), 1384-1450 (aggregation), 1432 (nlegs=9), 1488-1527 (selftest arms).

### 131-245 Mutation-sweep recipe
- At-risk: line 174 cites `tools/mutate-and-run.sh:425`; line 211 cites `:569-574` — anchors shift with any insertion; the named behaviour (driver prints failing count; DEGRADED when inconclusive) must still exist at the new anchor.
- Reader checks: resolve both anchors in the new runner bytes; run `bash tools/mutate-and-run.sh --target ...` shape unchanged; confirm the recipe's step text (options, exit semantics) still matches the runner's CLI.

### 375-404 Restore discipline
- At-risk: line 399-400 "Use the maintained `bash tools/mutate-and-run.sh --regression` ledger replay for those pinned cases; it does not recover the old driver" — must still replay *all* pinned cases; if the tenth leg is the only addition this stays true, but a reader must confirm `--regression` exits 0 and reports `cases=10 passed=10` from a clone at REV.
- Reader checks: run `--regression` in a scratch clone at the candidate rev; confirm restore discipline text (fingerprints, no checkout-restore) is not contradicted by the runner's restore step.

### 827-857 The protocol — ordered, fail-closed
- At-risk: line 829-831 pins the harness to a historical commit (`git show b58b26fb:tools/mutate-and-run.sh`) — unchanged by C2; the *example command* (line 834-835) is unchanged. No count claim here.
- Reader checks: the runner still accepts `--target/--defects/--suite/--workdir`; `MUTATE: SETUP`, exit 2 semantics unchanged; control-first and restore-re-check steps unchanged.

### 858-882 The boundaries
- At-risk: line 865 cites `tools/mutate-and-run.sh:36-38` ("the target is never written") — anchor shifts; the property must hold for the new leg's target (kagi `corpus/drift-pins.sh`).
- Reader checks: re-resolve line 36-38; confirm the new leg materializes into scratch and never writes the target (the C2 sweep already ran restore green — check the receipt's restore line).

### 921-932 The leg ledger
- At-risk: line 925 "… seven since round 16; eight since round 18; nine since round 26" — the count chain is a present-tense description of the runner; with a tenth leg it understates (needs "ten since round 51"). Line 929 cites runner anchors `:72-109`, `:511-522`, `:597-620`. Line 931 "eight rows" refers to `fleet-kill-rate-ledger.md`, not the runner (unaffected unless C2 appends there).
- Reader checks: report the new count chain; verify the leg table (legs 1-9 + new kagi drift-pins leg) is complete and each leg's recorded rate row exists; resolve the anchors.

### 933-964 Using the ledger
- At-risk: line 937 default scratch `/tmp/tameshi-r4-2-regression.XXXXXX` (false if a TMPDIR-default change lands); line 940 anchors `:126-136,1273-1294,1364-1384`; line 943 anchors `:1104-1175`, `:1159-1160`; line 948 `:1384-1450 since round 26`; line 950 "N=… 9 since round 26"; line 960 "Current anchors (round 26): pins/revisions/tables `:603-629`, first-four specs :657-839, inventory :83-108, nine dispatches :1384-1428" — the "nine dispatches" and the anchors all go stale.
- Reader checks: default scratch literal still in runner; ten dispatches now; anchors re-resolved; the receipt clause `cases=N passed=N` guidance updated to N=10.

### 965-1009 Reading a receipt
- At-risk: line 950's sibling claim (N=9 since round 26) also appears here as the closing-line rule (line ~985: "N=8 since round 18, N=9 since round 26"); line 1002-1003 `MUTATE_SELFTEST: 67/67 pass` — already stale at base (106/106), will drift further with the tenth leg.
- Reader checks: run `--selftest` in a scratch clone; record the new tally; flag the 67/67 quotes as stale regardless of C2; verify the receipt-reading discipline (block, not last line; PASS exact; FAIL names rows; SETUP not a verdict) is still what the runner prints.

### 1021-1068 The tick and the pin read
- At-risk: line 1064 parenthetical `MUTATE_SELFTEST: 67/67` (same stale tally); the section's pin-read mechanics cite the round-9 six-case table — historical, but the harness-sha compare (`REGRESSION_TOOL`) must still work with a ten-leg runner.
- Reader checks: same tally check; confirm the tick's "tool held" comparison is unaffected by the runner change (its logic doesn't depend on leg count).

### 1164-1211 The tick, executed
- At-risk: line 1168-1169 cites `tools/mutate-and-run.sh:511-518` for the PIN_*/REV_* fields; the six-row table is a timestamped round-9 observation (stays true as history).
- Reader checks: resolve `:511-518`; confirm the observation is not carried as a standing claim (line 1188-1189 already says so).

### 1212-1229 The receipt at this boundary
- At-risk: line 1218 (67/67 — historical round-9 receipt, correctly dated), line 1219-1221 `cases=4 passed=4` (historical), line 1225 anchor `:733-791`, line 1227-1228 "Cases 5-6 are still not embedded — named debt" (a historical debt, resolved by round 10 — already superseded text; a reader should not "fix" it, only note it).
- Reader checks: anchors; nothing present-tense except the replay claim, which now includes ten legs.

### 1272-1280 Operator runbook / six-leg regression (round 10)
- At-risk: the heading and narrative are dated to round 10; "six-leg regression" is historical. No present-tense count. The runbook pointer (line 1283-1286) references `operator-runbook.md` §3 "six-case ledger" — that file is not in the runner's input closure, but a reader should note whether the runbook's own count needs a reader item of its own (out of scope here; its sha is not pinned to the runner via this ledger's inputs for this section? — entry inputs for 1272 do include the runner).
- Reader checks: confirm the section presents round-10 history (it does); no update needed for the tenth leg except keeping the narrative truthful if any line implies currentness (lines 1283-1286 are bound to round 10 receipts).

### 1302-1364 The six-leg regression — usage and receipt
- At-risk: line 1304-1308 "At tool revision `75ed934d…` … replays **six** embedded legs (list `:85-89`; sources `:90-97`; pins/tables `:550-559`; specs `:766`, `:841`; registry `:1132-1141` — line anchors as read at `75ed934d…`, the sha governs)" — anchors are explicitly bound to an old sha (the section itself teaches "the sha governs"), so they are safe as history but must be re-verified for the new runner; line 1320-1322 default `/tmp/tameshi-r4-2-regression.XXXXXX` and "removed on PASS unless --keep" — flag for a TMPDIR-default change; line 1323 exit map `:115-119`; line 1328 `:104-106`, `:932-960`; line 1331 `:1488-1527`; line 1336 `80/80` (historical); line 1341 `cases=6` (historical); line 1343 "REGRESSION_EXPECT lists six recorded rates" (historical).
- Reader checks: the same six-leg table stays as history; verify the new runner's regression receipt shape matches the discipline (cases=10); verify defaults unchanged.

### 1380-1395 The map
- At-risk: line 1384 "the lane has held nine cases since round 26" (present-tense) → ten since round 51; line 1385 "eight rows; the round-26 ninth case has no row yet" (about `fleet-kill-rate-ledger.md` — unaffected unless C2 appends a row there; C2's knowledge entry is a `mutation-case-*.md` and a SOURCES row, not this ledger); line 1390 "six at round 11; seven since round 16; eight since round 18; nine since round 26" (mutation-case file count — if C2 adds `mutation-case-kagi-drift-pins.md`, this becomes ten); line 1391 "six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26" (the instrument row — must become "ten since round 51").
- Reader checks: each of these three count chains; whether a new mutation-case note exists post-C2; whether `fleet-kill-rate-ledger.md` gained a row.

### 1499-1516 Gate/probe registry — deep dive (C3 home)
Current shape: 8 columns (Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner), two rows (lines 1503-1504: `python3 tools/repeat-control.py`, `python3 tools/bash-witness-study.py`).
- At-risk (C3): every added row must be verified by a reader against the C3 predicate (`c3/measure.py` docstring + contract `contract.json` C3):
  1. Row names a real tool in `tools/` from the frozen 30 (`c3/tools-base.json`) or any `tools/*.py|*.sh` carrying `selftest`.
  2. Exactly one backticked self-test command of the form `python3 [-I]|bash tools/T …selftest…` with **no shell metacharacters** inside the command.
  3. Verdict map names 0 and 1 and the usage code, and the row's `--r51-no-such-flag` probe exits with a declared code (run it in a scratch clone).
  4. The self-test exits 0 from a clone at REV and its **last line prints the finding id recorded in the row**.
  5. Pinned-value paths exist at REV or are `none` (check each literal path).
  6. Write scope matches observed behaviour (isolated selftest scratch; no lane writes).
  7. Owner `tameshi`.
- At-risk (C2 coupling): line 1506 "Registry scope is these round-12 instruments; no new conformance assertion is made about the historical runner" — becomes false if C3 adds a runner row or rows for non-round-12 tools in this section; either the clause must be amended (a further SKILL.md byte change inside this same section — still one re-key) or the rows must be scoped to avoid contradicting it.
- At-risk (runner): all four current entries pin the runner; the runner edit alone drops this section even before C3's edit. The re-key must bind both new inputs (new section sha, new runner sha).
- Line 1508's BashWitness declaration pin `75ed934d…` is historical and unrelated.

### 1754-1805 Seventh recorded case
- At-risk: line 1762 "cases=7 at round 16; cases=8 since round 18; cases=9 since round 26" (present-tense tail) → becomes "cases=10 since round 51"; line 1770-1772 reproduce commands use `--label js-round-gate` and `--workdir` (unchanged); line 1780-1782 TMPDIR guidance (unchanged semantics).
- Reader checks: count chain; reproduce command still valid (the flags still exist).

### 1806-1813 Round-16 registry
- At-risk: line 1810 runner row "selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage" — the exit map must still hold for the ten-leg runner (selftest still 0/1; regression map unchanged); the row is a 4-column old-style row (no verdict-map/owner cells) — it is not the C3 home, but a reader should confirm the *exits* claim stays true.
- Reader checks: `--selftest` exit codes; `--regression` exit map; `--r51-no-such-flag`-style usage still 64.

### 1814-1845 Live-tree re-pin
- At-risk: line 1831 "A repo path has no `.git` of its own inside a git super-repo | Runner regression leg: SETUP `repo_identity_mismatch`, exit 2" — the new kagi leg's target repo (kagi-shokunin, a sibling lane) must still be runnable as a cloned object-store read; the super-repo guard must apply to the tenth leg too (the sweep ran in a scratch clone — verify the receipt shows no identity mismatch).
- Reader checks: run `--regression` from a clone; confirm the new leg passes the identity guard (exit 0) and that a super-repo-poisoned invocation still refuses with SETUP 2.

### 1846-1854 Round-17 registry
- At-risk: line 1852 runner row "as the round-16 row; a borrowed repo identity is SETUP 2" — same exit-map and identity-guard claim as above.
- Reader checks: same as 1806/1831.

### 1905-1924 Eighth recorded case
- At-risk: line 1915 "cases=8 passed=8 at the round-18 runner (cases=9 passed=9 from round 26 on, ninth leg js-cite-check; seat Read34)" — present-tense tail → becomes cases=10 from round 51 on, tenth leg (kagi drift-pins).
- Reader checks: count chain; the statement "ninth leg js-cite-check" remains as history.

### 2132-2136 Round-26 registry
- At-risk: line 2136 "leg set not equal to the nine ledger legs" (mte-interop `--check` SETUP clause) and "mte-interop-check (9/9)" — both become ten/10; the row is the C3-adjacent home for mte-interop (already a conforming 8-cell row: kind, entry command, verdict map incl. 0/1/2/64, self-test `--selftest` with a finding id "17/17"/"9/9", write scope, owner tameshi).
- Reader checks: after C2, `tools/mte-interop.py --check` must see ten legs and report 10/10; the row's "9/9" must be updated to the new tally (a byte change inside this section → its sha changes → this section also needs a re-key entry; it is in the dropped set anyway).

## 5. Re-key route notes for the L1

1. **One re-key pass after both edits.** C2 and C3 both change the runner; C3 also changes SKILL.md section 1499. Re-key only at the final candidate rev (round-49 method: `.ufo/evidence/round-49/c1/refresh.py` — append one entry per target section, trace-bound via `tools/trace-inputs.py` in a `--shared` clone at CAND). Re-keying twice doubles the risk of a mid-way sha mismatch.
2. **The 20 sections above are the minimum reader set.** 44 sections survive the runner change untouched; only these 20 need re-key entries. Section 1499 needs it for two independent reasons.
3. **Line anchors shift; readers must resolve by name, not number.** The runner has ~10 distinct anchor clusters cited across the 20 sections (listed in §4); a tenth leg inserted into `regression_specs`/dispatches will move everything below it. Reader items should ask for the *resolved* anchor, not the old number.
4. **Fixing stale tallies inside re-keyed sections is allowed but must be part of the same candidate** — any SKILL.md byte change to a section changes its sha and must be re-keyed in the same refresh (the 67/67 quotes at lines 1003/1064 and the count chains are the natural fixes; if fixed, the reader item is "confirm the new tally matches the new bytes").
5. **TMPDIR defaults**: statements at 937, 1320-1322, 1767 only break if the runner's default scratch template changes. C2 does not need to change it; readers confirm the literals remain.
6. **C3's registry row for the runner must be written against post-C2 bytes**: its finding id (last line of `--selftest`) will carry a new tally; the row's verdict map must keep 0/1 + usage; the regression evidence in the row (if any) must say `cases=10`.
7. **C2's sweep receipt already exists** (`.ufo/evidence/round-51/c2/sweep/`) — readers may cite it for the "green control / restore OK" checks rather than re-running the sweep; they still must run the *selftest* against the new bytes to check the tally/finding id.

## 6. Evidence commands

- `python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 9962033fd7a75aa2f2847e979dd687a5d28505a1` → 64/64 credited.
- Simulation: `git clone -q --shared LANE $D/lane`; append one byte to `tools/mutate-and-run.sh`; commit; `python3 .ufo/evidence/round-21/coldread/measure.py --repo $D/lane --rev 45ea5934a7b144878b966e81456b72ce803f5d53` → 44/64, dropped list in §2 (receipt `T51CritRekey-sim-receipt.txt`).
- `TMPDIR=$S bash tools/mutate-and-run.sh --selftest` at base → `MUTATE_SELFTEST: 106/106 pass` (receipt `T51CritRekey-selftest.log`).

## Summary

- Monitor mechanics confirmed from the frozen round-18 selector: a section drops when every matching ledger entry's input shas drift; the runner is pinned by exactly 20 credited sections.
- Simulation at base (one runner byte) drops exactly those 20 — 64→44 covered; receipts copied to wave-1 dir.
- The 20 sections carry the present-tense count chains ("nine since round 26", "nine dispatches", "cases=9 since round 26") plus ~10 runner-line-anchor clusters; all are the reader-verification set for the re-key.
- Two tally quotes (67/67 at lines 1003/1064) are already stale at base (106/106); readers should disclose, and any fix belongs in the same re-key candidate.
- Registry section 1499 drops twice (runner drift + C3 sha change); its line 1506 scope clause and the mte-interop "9/9" row are the only prose at cross-purposes with C3/C2.
- Re-key must run once after both C2 and C3 land, keyed to the final candidate sha, with per-section reader items from §4.
