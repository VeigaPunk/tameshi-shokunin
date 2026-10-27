# T53W2CritSemantic — wave-2 semantic re-read (cannot_see attack) of 6 sections at C**

Seat: T53W2CritSemantic (critic, wave 2 of 2, round 53). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit read: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C**), via git objects only
(`git -C <lane> show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:<path>`); the working tree was never read for content.

## Sections under review (frozen-rule split, verified against the frozen sectionizer)

Split rule: heading = `^#{1,3}(\s|$)` outside ``` fences; section = heading line through the line
before the next heading; trailing whitespace-only lines stripped; joined with `\n`; sha256 over
UTF-8 bytes with surrogateescape. My reimplementation and the frozen
`.ufo/evidence/round-18/measure.py:sectionize()` (extracted at C**, importlib-loaded) produced
identical ranges and digests for all six sections:

| Section | Lines at C** | section_sha256 |
|---|---|---|
| `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 924–936 | `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993` |
| `### Using the ledger` | 938–968 | `355743ed274b576d6119665499c8771044b53297308b19822ba73bf0ef9be1d1` |
| `### Reading a receipt — the discipline` | 970–1013 | `53cbbf610d088a5f03053909b56a53134693a822950741ed4119d6c7d650458b` |
| `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` | 1015–1024 | `0a7adb86a56848dd1b9e70de885461eae85ea1da4aaf0d5cafde321cc13a0a64` |
| `### The service's limits — what tameshi refuses to mutation-test` | 1257–1285 | `37d63abf882e89d8103fb2618d8622c78da60aecfac75352851687e42eea7590` |
| `### The map — where a reader enters, artifact by artifact` | 1396–1410 | `30d62e79a81d8e6dfcfc9076f0977b1e14016d527f5fd78e66aab407bd370bea` |

Cross-commit context: `git diff --stat C*..C**` touches only `SKILL.md` (97 lines), seven python
tools under `tools/` (bash-witness-study, context-capture, env-diff, evidence-disposition,
pin-disposition, registry-check, repeat-control — each +16/−18ish), and `.ufo/waves/round-53/w1/*`.
`tools/mutate-and-run.sh` is **byte-identical** at C* and C** (content sha256 `977de470…` at both —
verified with `git show <rev>:tools/mutate-and-run.sh | sha256sum`). `corpus/`, `plans/`, `LOG.md`,
`SCORECARD.md`, `PROVINCE.md`, `.ufo/evidence/`, and `.ufo/waves/round-52/` are unchanged
(`git diff --stat C*..C** -- <paths>` → 0 lines). The service-limits section bytes are identical at
C* and C** (same section sha `37d63abf…`), consistent with its wave-1-clean status.

# Fix verification (each wave-1 finding on these sections, re-checked at C**)

## S1 — leg ledger: the row-count sentence (wave-1 finding: stale-ledger-count)

Fixed sentence at C** (lines 933–936):

> the standing per-gate rate rows are `corpus/knowledge/fleet-kill-rate-ledger.md` (eight ledger rows — six in the §1/ER-2 table plus the round-16 and round-18 appends; the ninth and tenth cases, cite-check and drift-pins, are recorded in their own notes, not as ledger rows).

Verdict: **HOLDS at C**. Evidence:

- Ledger at C** (`git show C**:corpus/knowledge/fleet-kill-rate-ledger.md`, 441 lines): measured rows are §1 rows `| 1 |`–`| 4 |` at :45–48, ER-2 rows `| 5 |`,`| 6 |` at :276–277, the Round-16 block ("seventh row appended", :403) carrying the round-gate row at :410, and the Round-18 block ("eighth row appended", :424) carrying the sources-check row at :432. Total = **8**; the file's own numbering stops at eight.
- `grep -n '^#\{1,3\} ' ledger` → 15 headings (…366, 403, 424, 439); **no** round-26 or round-51 heading block. `grep -in 'round[ -]*26\|round[ -]*51\|ninth\|tenth'` → exactly one hit, the Round-52 supersession bullet at :441, which is a §3 cell correction, not a row.
- Ninth and tenth cases live in their own notes: `git ls-tree -r --name-only C** -- corpus/knowledge/ | grep mutation-case-` → 10 files, including `corpus/knowledge/mutation-case-kumitate-cite-check.md` and `corpus/knowledge/mutation-case-kagi-drift-pins.md`.
- The dated milestone parenthetical "(dated milestones: seven from round 16, eight from round 18, nine from round 26, ten from round 51)" is explicitly dated → hold under the wave rule.
- Supporting pointers re-verified: `git show 9f1d3c3:tools/mutate-and-run.sh` lines 72–109 are the r7-1 four-leg ledger comment (rates 8/10, 8/10, 6/10, 4/10 at :75–78); :511 = `PIN_JS`, :522 = `TABLE_MADO` (the recorded tables); `git show 4b7c682:tools/mutate-and-run.sh` :597 = `PIN_JS`, :620 = `TABLE_SOURCESCHECK` (the round-18 extended tables).

## S2 — Using the ledger: the round-26 attribution (wave-1 finding: false attribution)

Fixed sentence at C** (line 963):

> Current anchors (round 52 re-anchor to the ten-leg table; the round-26 tool recorded :603-629): pins/revisions/tables `tools/mutate-and-run.sh:614-643`, first-four specs :671-849, inventory :83-108, ten dispatches :1459-1508.

Verdict: **HOLDS at C**. Evidence:

- Round-26 tool: `git show a08e85c:tools/mutate-and-run.sh` → `PIN_JS` at :603 … `TABLE_CITECHECK` at :629 (the full pins/revisions/tables block; no `TABLE_DRIFTPINS`, consistent with nine legs); `local nlegs=9` at :1430. The "recorded :603-629" attribution is exactly true.
- Current anchors on the C** tool blob (unchanged from C*, sha `977de470…`): :614 = `PIN_JS` … :643 = `TABLE_DRIFTPINS` ✓; :671 = `regression_specs() {` … :849 = `EOT` ✓; :83–108 = the `--regression` inventory header incl. "Leg 9's spec is the round-26 pre-registration committed in 622d31d" ✓; :1459 = first dispatch `regression_case_git js-kimi-census` … :1504–1508 = `bash-drift-pins` + `st_driftpins=$?` ✓; :139–143 = the 0/1/2 exit map ✓; :1519–1548 = FAIL/SETUP/tally/PASS-exit block ✓; :1275–1317 = `git show <rev>:<path>` materialization + pin-mismatch refusal ✓; :1302–1306 = the `REGRESSION_PIN` printf ✓; :78–79 = the `MUTATE: DONE|DEGRADED` / `MUTATE: SETUP` report lines ✓.
- "N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26, 10 since round 51" — `nlegs` read from the blobs: 9f1d3c3→4, a08e85c→9, and the C** blob carries ten dispatches with `TABLE_DRIFTPINS` ✓.

## S3 — Reading a receipt: the selftest tally (wave-1 finding: stale count)

Fixed item 7 at C** (lines 1007–1009):

> `bash tools/mutate-and-run.sh --selftest` at the pinned r7-1 tool printed `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0, tool sha256 `cf41efaa…` (a content sha, not a git revision; the tally is the pinned tool's, not the current command's — round 52: the same command prints `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0, at runner sha256 `977de470…` …)

Verdict: **HOLDS at C**, by execution. Evidence (both selftests run from scratch copies of the exact blobs, TMPDIR/cwd under my seat scratch):

- `git show 9f1d3c3:tools/mutate-and-run.sh | sha256sum` → `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (the named r7-1 content sha).
- `bash mar-r7.sh --selftest` (the pinned r7-1 blob) → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0.
- `bash mar-Css.sh --selftest` (the C** blob, sha `977de470…`) → `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`, rc 0.
- Round-52 receipt exists at C**: `git show C**:.ufo/waves/round-52/w2/T52W2Fix06.selftest.out` tail → `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`.
- The rest of the section re-verified: anchors `:78-79` ✓, `:2010` (the exact-flip FAIL assertion behind the doctored-table corroboration) ✓, `plans/round-7.plan.md:11-15` = the round-7 attestation leg ("is ATTESTED read-only … The lane operates; tameshi attests.") ✓; item 2's "D is 15 for checklist-run, 10 for other current legs" matches the embedded tables; the dated `N=8/9/10` milestones are dated → holds.

## S4 — re-sweep cadence: "three readings per case" (wave-1 finding: self-contradicting count)

Fixed sentence at C** (lines 1019–1020):

> **the cadence is a pin read executed at the tick** — two readings per case, three triggers, one re-pin rule

Verdict: **HOLDS at C**. Evidence:

- "two readings per case" now matches the page's own reading map: C** :1032 `- **Per case, two readings:** the target's relation to each repo's branch-tip bytes … and the tool's relation to the last run`.
- "three triggers" = T1 (:1077), T2 (:1081), T3 (:1087) under `### Triggers T1–T3 and the re-pin rule` (:1075) ✓.
- "one re-pin rule" = the single "The re-pin rule." bullet at :1089 ✓.
- "the six-case confidence statement below" = `### Six-case confidence statement` at :1098 (below the section, which ends :1024), with six rows (:1105–1110) whose revision pins match the tick table's pins (:1049–1054) ✓.
- U9 pointer `fleet-kill-rate-ledger.md:235-237` → the three lines are exactly the U9 item carrying the quoted sentence verbatim ✓. "the policy" = ER-3 at ledger :285 ✓. No-daemon/no-timer and the [U] note are unchanged and consistent.
- Neighbour-drift sweep for this section: it contains no SKILL-internal line anchors (its only anchors are the ledger file pointer), so the +3-line top-of-file insertion cannot stale it. Its content did not change except the one word three→two.

## S5 — service's limits: wave-1 clean; read for drift caused by neighbours

The section bytes are identical at C* and C** (sha `37d63abf…`). All of its **corpus/external**
anchors re-verified at C**: `service-limits.md:4-5` (the role clause, spanning :4–5) ✓,
`service-optin-protocol.md:25-30` ✓, `:129-132` ("No live substrate read…") ✓, `:267-269` (U4) ✓,
`:86-91` (lane-scoped scratch) ✓, `fleet-suite-census.md:277-286` (queue projection) ✓,
`PROVINCE.md:14-18` + `:20` ✓, `fleet-kill-rate-ledger.md:156-158` ✓, `:220` (U2) ✓, `:35-36` ✓,
`:285` (ER-3) ✓, `:318` (ER-4) ✓. The negative claim "no cadence or ledger text names it" holds:
`git show C**:SKILL.md | awk NR 1005..1165 | grep service-limits` → **no hits**, and the ledger has
zero hits in 441 lines.

**But three of its SKILL-internal line anchors staled at C** — see Findings F1–F3.** Root cause:
fix pass 2's top-of-file hunk (`@@ -21,9 +21,12 @@`, the scratch-namespace rewording) inserted a
net +3 lines above every line below :31, and the wave-1-clean section's internal `SKILL.md` anchors
were not re-resolved. They were exact at C* (wave-1 seat T53W1Read24 check 7) and are wrong at C**.

## S6 — the map: three pointer fixes (wave-1 findings: stale pointer, truncated range, unsupported absolute)

All three fixed pointers **HOLD at C**:

1. Divergence-rule pointer is now name-based: "the runbook §'s "Pointer, not a second home" bullet"
   resolves at C** `SKILL.md:1309` — `- **Pointer, not a second home.** Its own rule: where it and an
   anchored source diverge, the anchored source governs …` ✓ (the old `:1294-1297` line anchor was
   correctly replaced; the bullet itself moved to :1309 and the name-based pointer survives such moves).
2. Ledger row: "(eight rows; the round-26 ninth and the round-51 tenth case have no row — the ninth
   lives in `corpus/knowledge/mutation-case-kumitate-cite-check.md` and the tenth's only ledger
   footprint is the §3 cell supersession at `fleet-kill-rate-ledger.md:439`)" — 8 rows verified as in
   S1; both notes exist at C**; the ledger's only case-10 footprint is the Round-52 block at :439
   (heading; the supersession bullet at :441 names case 10 and points at the note). "Only ledger
   footprint" is accurate within the ledger. ✓
3. Service-limits row: "this page carries the compact rendering (the `### The service's limits …`
   section's table)" — the named section exists at C** :1257–1285 with its 10-row refusal table (:1269–1278) ✓.
- Remaining anchors re-verified: `operator-runbook.md:349-351` ("Default scratch is a fresh
  `mktemp -d /tmp/…`") ✓; `tools/mutate-and-run.sh:149-150` ("(r51 honours TMPDIR)") ✓ (tool
  unchanged); runbook §3 "six rows" — the six measured cases table at :147–154 has exactly 6 rows ✓;
  10 `mutation-case-*.md` files ✓; `corpus/README.md:125/326/614` ✓; `LOG.md:316-317` ✓.
- Semantics of the TMPDIR sentence: the runner still uses `${TMPDIR:-/tmp}` (fallback when TMPDIR is
  unset) and honours TMPDIR when set — the row says only "the runner honours TMPDIR", which is true
  at C**; the round-53 strict-TMPDIR refusal convention landed in the seven python tools, not in
  mutate-and-run.sh, so no neighbour contradiction. Hold.

# Findings

Three findings, all in the wave-1-clean `### The service's limits` section, all caused by the
round's own fix pass shifting lines below the top-of-file insertion. A fresh reader at C** resolving
these anchors lands on the wrong bytes.

## F1 — row (c) anchor `:823-825` no longer carries "The service never edits, repairs or re-pins the gate"

Quote (byte-exact, row c anchor cell):

> `:823-825`

Claim anchored: row (c) "A moved substrate without a re-pin — the service never edits, repairs or re-pins a gate".

Evidence. At C** those three lines are the tail of the clause-mapped-defect-spec item:

```
823|defects over six clauses — A verdict token · B UNKNOWN-never-CLEAN · C exit
824|map · D declared-plane census · E sha comparison · F reader fallback
825|(`mutation-case-mado-verify.md:51-55`).
```

The sentence the row paraphrases moved to **:826**: `4. Nothing else. The service never edits, repairs or re-pins the gate; a …` (C* dump for comparison: the sentence was at :823–825 — the whole item sat exactly inside the cited range at C*; the fix-pass insertion at :21–31 shifted it +3). The quoted content is **absent at the cited lines** → stale pointer at C**.

## F2 — row (f) anchor `:879-881` no longer carries the "Sensitivity, not truth" bullet

Quote (byte-exact, row f anchor cell):

> `:879-881`

Claim anchored: row (f) "Product semantics — whether a gate's verdicts are right — never measured — sensitivity ≠ truth".

Evidence. At C** those three lines are the tail of the harness-pin bullet:

```
879|  mid-round by a concurrent lane (re-pin `b56c6e57…`); every number stays tied
880|  to the executed revision and the drift is recorded, not smoothed
881|  (`mutation-case-mado-verify.md:17-23`).
```

The "**Sensitivity, not truth** — a sweep measures what the suite can detect, never whether the gate's verdicts are right" bullet is at **:882–884** at C** (it was :879–881 at C* — see the C* dump; +3 shift). The quoted content is **absent at the cited lines** → stale pointer at C**.

## F3 — row (b) anchors `:813-817` and `:840-844` truncated by the +3 shift

Quote (byte-exact, row b anchor cell):

> `:813-817`; `:840-844`

Claim anchored: row (b) "No one-command hermetic suite — refused before any suite runs — the request shape requires it; spec/control failures are `MUTATE: SETUP`, exit 2, no headline".

Evidence. At C**:

- `:813-817` = the tail of the pinned-revision item (:813–815) plus only the **first two lines** of
  the hermetic-suite item, which now runs :816–820 (`2. **A one-command hermetic suite** invocable
  against a copy — mado's gate` at :816, `takes \`bash "$MUTANT" --selftest\`; …` at :817). At C*
  the range covered the item's full five lines (:813–817).
- `:840-844` = "Pin + pristine" (:841–842) and the spec-parse item's first two lines (:843–844); the
  line the row's "`MUTATE: SETUP`, exit 2, no headline" clause points at —
  `` `MUTATE: SETUP (<reason>)`, exit 2 — no headline. `` — is now at **:845**, one line outside the
  cited range. The string `MUTATE: SETUP` is absent from :840–844.

Partial phrases survive ("A one-command hermetic suite" at :816; "before any suite run" at :844), but
both ranges are wrong for the full content they anchor (truncated item; the SETUP line outside by
one). Same +3 root cause as F1/F2 (at C* both ranges were exact — wave-1 seat Read24 check 7).

# Notes recorded, not promoted to findings

- **S5 negative-claim scope `:1010-1154` is now short by ~6 lines**: the six-case confidence
  statement it covers now ends at :1160 (C**), because +3 lines landed above and +2 more inside the
  cadence region. The claim itself ("no cadence or ledger text names it") still holds — grep over
  C** :1005–1165 finds zero `service-limits` mentions, and the ledger has none — so a reader can
  still verify the claim within the cited span. Recorded as drift; the span is a scope, not a
  quoted-content pointer, and its content resolves.
- **S6 ledger anchor `:439` lands on the block heading** ("## Round 52 — §3 drift-pins cell
  superseded"); the supersession bullet itself is :441. The row's phrase "the §3 cell supersession
  at `fleet-kill-rate-ledger.md:439`" names the block that starts at :439 — recorded, not promoted
  (the wave-1 reader made the same observation and the fix pass chose to keep the block pointer).
- **S1/S2 "dated milestone" chains** (seven/eight/nine/ten legs and cases) are explicitly dated and
  match the tree; holds under the wave rule.
- **Calibration note for the L1**: F1–F3 are genuine C** defects but are cheaply repairable
  (re-resolve three anchor ranges to `:826-828`, `:882-884`, `:816-820`/`:843-845`, or convert to
  name-based pointers as S6's fix did). They do not touch the C1 cold-read floor's semantic content:
  the six sections' theses are all true at C** as far as this seat could measure.

# Checks run (commands → outcomes), condensed

- Split+hash: my fence-aware splitter vs frozen `sectionize()` on `git show C**:SKILL.md` — identical ranges/digests for all six (table above).
- `git diff --stat C*..C**` → SKILL.md +97, 7 python tools, `.ufo/waves/round-53/w1/*` only; `tools/mutate-and-run.sh` sha `977de470…` at both; `corpus/ plans/ LOG.md SCORECARD.md PROVINCE.md .ufo/evidence/ .ufo/waves/round-52/` unchanged (0-line diff).
- Ledger row inventory, headings, round-26/51 grep, both case-note paths (outputs quoted above).
- `git show a08e85c:tools/mutate-and-run.sh` :603–629 dump + `nlegs=9`; `git show 9f1d3c3:…` :72–109, :511–522; `git show 4b7c682:…` :597–620 (S1/S2 pointers).
- Executed selftests on pinned blobs: r7-1 → `67/67`, C** → `107/107` (S3 fix, by measurement).
- C** tool anchors spot-checked: :139-143, :614-643, :671-849, :83-108, :1459-1508, :1275-1317, :1302-1306, :78-79, :2010, :149-150, :1519-1548, :1247-1459-1517.
- C** SKILL cadence region :1005–1165 dumped; "two readings" :1032, T1–T3 :1075-1088, re-pin rule :1089, six-case table :1098-1110, U9 pointer ledger :235-237.
- C* vs C** line dumps at :810-826, :838-846, :877-883, :1008-1016, :1150-1160 (F1–F3 evidence).
- S5 corpus anchors, S6 corpus/LOG/README/runbook anchors (outputs quoted above).

# Scratch and tooling

- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2CritSemantic/` (mkdir -p; held `SKILL-Css.md`,
  `SKILL-Cs.md`, `ledger-Css.md`, `mar-r7.sh`, `mar-Css.sh`, `split.py`, `sections.json`, six
  section files — all well under 50 MB; deleted with `rm -rf` before yield).
- Tooling installed/upgraded: **none** (system `git`, `python3`, `bash`, `sha256sum`, `awk`, `grep`
  sufficed). No pacman transaction attempted (pacman paused host-wide). No network access.
- No git/jj mutating command was run anywhere; every git call was `show`/`cat-file`/`log`/`diff`/
  `ls-tree` against the lane repo. Write scope respected: only this report under
  `.ufo/waves/round-53/w2/` plus the scratch tree (removed).
