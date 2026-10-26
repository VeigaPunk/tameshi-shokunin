# T49W2RevLesson — review of `corpus/lessons/round-49.md` at `f181a961` (round 49, wave 2, falsify)

Seat: T49W2RevLesson (leaf reviewer). Item: review the round-49 lesson at the candidate content revision
`f181a961ae44061af486f600e5ea257d2baf78f8` — `## Gate` (every new row: URL, access date, ≤ 25-word located quote;
≥ 1 admit and ≥ 1 reject from the assimilation set; status/recheck/used-by changes logged old → new), `## Mistakes`
(class · evidence pointer · captured-by · fix · able-to-fail shown), the considerthese section, and every evidence
pointer resolving at `f181a961` (pointer-check run per its usage line). I did not author what I attack; I decide no
claim and ran no counter (not even `--selftest` of a claim counter — none is in this item's scope).

Method and bounds: read-only on the lane; all lesson/evidence bytes read through `git show`/`ls-tree`/`cat-file` at
`f181a961` (never the moving worktree); wave-1 receipts extracted at that revision into scratch
`/fast/scratch/hyaku/tameshi-r49/T49W2RevLesson` (deleted before this report was finished — every command below is
re-runnable against the lane, and every output quoted is observed). Live probes: `curl` only (doi.org, Crossref,
smallbone.se, cs.tufts.edu). Nothing under `/home/vgpnk/.local/state/`; no `c2-WITNESS/CTL_FIX/CTL_ABSENT.stdout`
opened (my item does not name them); no model passed; no `agent://all` message. Tooling: **zero installs or
upgrades** (pdftotext 26.08.0, curl 8.x, python3 3.14.8, git as present; pacman untouched — host transactions
paused). Writes: this report and `T49W2RevLesson.s170.pdf` (the one live-fetched artifact my findings cite; its
sha256 equals the sha already recorded in the committed receipt `T49ScribePkgCraftAuthor.s170-reopen.txt`).

---

## Verified (holds) — with the command that shows each

**Gate rows S269/S270 (contract v1 rule 1).** Both rows exist at `corpus/SOURCES.md:144-145` at `f181a961`
(`git -C LANE diff 8ca67421… f181a961… -- corpus/SOURCES.md` → 5 insertions, 0 deletions; `--numstat` → `5 0`).
- URL + access date + size + sha256: `fetch-receipts.json` at `.ufo/waves/round-49/w1/T49ScribeRows.src/` records
  HTTP 200 / 194,315 B / `bfddcaa6…` and 200 / 1,269,821 B / `eaee48f9…`, fetched 2026-10-26T20:33Z;
  `sha256sum` of the committed snapshots reproduces both digests exactly, and the independent executor copies match
  (`sha256sum .ufo/waves/round-49/w1/T49ExecSrcQuickCheck/quickcheck-icfp00-icfp-2000-course-copy.pdf` →
  `bfddcaa6…`; `T49ExecSrcSmallbone/receipt.json` → `eaee48f9…`) — the lesson's "independent fetches, identical
  sha256" is true.
- Quotes verbatim at the claimed locations (my own `pdftotext` over the committed snapshots, not the wave-1
  extracts): QuickCheck Abstract quote on PDF p. 1 (= printed 268; Crossref `page 268-279`,
  `T49ScribeRows.src/crossref.json`); the `collect`/histogram quote on PDF p. 3 (= printed 270) immediately under
  the `2.4 Monitoring Test Data` heading; Smallbone quote on PDF p. 39 whose extracted first line is the printed
  folio `34`, under `2.10 Generating Test Data`. Word counts 20, 14, 19 — all ≤ 25. The pilot's further anchors
  also verify: §3.2 "Generators for User-Defined Types" + the `sized` sentence on PDF p. 4 (= printed 271);
  §5.1.4 "A False Sense of Security" + the "false sense of security" sentence on PDF p. 7 (= printed 274) — a
  plain-text extraction interleaves the two columns, but `pdftotext -layout -f 7 -l 7` shows the sentence in the
  left column under the `5.1.4` heading; `creating custom generators is sometimes necessary to get correct
  results` is on printed p. 34 as the pilot says. The pilot's own recheck commands return the expected values
  (`grep -c 'that fit the program at hand' smallbone.txt` → 1; `grep -c 'print out a histogram of these values'
  quick.txt` → 1).
- "the ACM DL answered 302 → 403": `T49ExecSrcQuickCheck/doi-resolution-headers.txt` shows `HTTP/2 302` with
  `location: https://dl.acm.org/doi/10.1145/351240.351266` then `HTTP/2 403`.
- Recheck/used-by/status: both rows `mined | 2026-10-26 | 365d | corpus/knowledge/pbt-generator-pilot.md`.
- "Rows touched old → new: none" and "no prose was stripped": the diff is additions-only (numstat `5 0`).
- The stale "Next unused id: S265" note corrected by an appended note: the diff appends the Round-48 correction
  line plus `Round 49: two rows added by document …` plus `Next unused id: S271`.

**Assimilation (≥ 1 admit, ≥ 1 reject — 2 admits, 2 rejects, 1 deferred).**
- Id-collision numbers verified from the committed receipt files: `wc -l` over
  `.ufo/waves/round-49/w1/T49ExecIdGuard/{reg-ids,staged-ids,collisions}` → 128 / 103 / 8, collisions exactly
  S153–S160; `reg-indented2-collisions` → 9 (the 8 + S182) vs `reg-indented2-col0collisions` → 8 — the lesson's
  "9 under `^ {0,3}`, 8 at column zero" is exact.
- Quarantine: `quarantine-tameshi-count.txt` → `rows=17`; `quarantine-S182-hits.txt`/`-S183-hits.txt` → `0`/`0`;
  the receipt's §4 shows S182's DOI once as never-checked `S134` (register line 365) and S183's document zero
  times — the lesson's sentence is exact.
- S183 anchor correction verified in the PDF: the quote is at §2.10, printed p. 34 (PDF p. 39); printed p. 44
  (PDF p. 49) begins `3.4 shr: Problems with Partiality` and `grep -ci generator` over that page → 0. The
  package's staged row (`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md:37`) really anchors
  "§4.1 … p. 44", and staged S182's row (`:36`) really says "§Abstract and §1 Introduction" — the lesson
  characterizes both accurately.
- Reject 1 (`r4-quickcheck-primary-correction.md`) independently reproduced: `git -C LANE grep -c
  '10.1145/1660572.1660575' 8ca67421… -- .` → no hits; `git log --all -S'10.1145/1660572.1660575'` → 5 commits,
  all 2026-10-26 round-49 commits (the DOI enters the lane only with this round's own attack records);
  `curl -sI https://doi.org/10.1145/1660572.1660575` → `HTTP/2 404`; Crossref API → `Resource not found.`
- Reject 2 (`pbt-generator-craft-author.md`) grounds verified: my own fetch of S170's carrier
  (`curl -fsSL https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quviq-testing.pdf`) → sha256 `35dddba5…`
  (equals the committed receipt's re-open sha) and `pdftotext -layout | grep 'toy example'` → abstract line
  "…sions made for testing stateful code, via a toy example in C." — the entry's "not toy examples" premise is
  false as the receipt says; `git log --all -S'| S116 |' -- corpus/SOURCES.md` → 0 commits and no S116 row at
  `f181a961` (the "resolves to no tameshi row" claim holds, and never held); S019/S020 are held tier-A rows
  (`corpus/SOURCES.md:30-31` at `f181a961`).
- Deferred (`pbt-generator-as-fixture.md`): `T49ScribePkgAsFixture.md` §0 says "ADMIT narrowly — two rows, one
  method entry — conditional on the nine edits in §3", E1 names the two rows (staged S157 JOSS Hypothesis, S166
  Zenn) re-opened 2026-10-26, and the flip-to-refuse is "if the L1 will not open both rows in this round" — the
  lesson's deferred bullet matches on every element.

**Mistakes rows 1–3 (class · evidence pointer · captured-by · fix · able-to-fail).**
- Row 1 evidence: round-48 `contract.json` `freeze_plan` step 2 really pre-registers the order ("…and before any
  deciding or control scoring… the controls are scored and committed"); the timestamps are exactly as the lesson
  prints — `after/c1-a3.start`/`.end` = 15:34:20Z/16:20:54Z, `control/c1-controls-a3.start`/`.end` =
  16:21:02Z/19:35:25Z (8-second gap); `corpus/lessons/round-48-verifier-spotcheck.md` defects 2–3 say the same.
  Captured-by "none (QUALITY 69 and 88 do not reach a claim counter's control order)": criterion 69 (QUALITY.md:784)
  binds data-wave binding conditions, criterion 88 the no-harm monitors at base — neither reaches control order.
  Fix + able-to-fail: `deciding-run.sh` gate 0 refuses on all three conditions — receipts
  `T49ScribeMistake.gate0-a.stdout` → `DECIDING_REFUSED control-receipt-missing …c1-controls.stdout`,
  `gate0-c.stdout` → `DECIDING_REFUSED second-invocation c1`, and `T49ExecMistakeGate.md` shows the third shape
  (`control-receipt-not-after-freeze`, incl. the literal ancestor-of-freeze variant) — every case exit 3 with
  empty receipt dirs; QUALITY criterion 99 exists at `f181a961` (`corpus/QUALITY.md`, "### Criterion 99 — a
  control is scored and committed before the deciding run…", round-49 append) and its text matches the lesson.
- Row 2 evidence: `.ufo/evidence/round-48/quality/coldread-precheck-red-c7586b9.stdout` prints exactly three
  `LOST` lines — rounds 14, 13, 12 — with drifted inputs including `corpus/SOURCES.md` and the three knowledge
  notes (the C2 record edits), tail `cand_credited=57 lost=3 RED`. Captured-by QUALITY 98 verified
  (QUALITY.md:1436 block). The fix's first half (restored by C1, record files read through git blobs) matches the
  contract's C1 durability predicate; the second half is F1 below.
- Row 3 evidence: `SCORECARD.md:2326` at `f181a961` is verbatim the sentence claiming every evidence cell is the
  `--emit` output "pasted byte-exact"; `emit-15b1521.stdout:115-117` is exactly the three `EMIT_AXIS` rows whose
  SCORECARD cells carry lane prose; the appended correction exists (`SCORECARD.md:2382`, "### Round 48 —
  correction (appended in round 49)", text matches); the checker receipt
  `T49ScribeMistake.emit-verbatim.stdout` ends `EMIT_VERBATIM ok=19 mismatch=3 rev=c7586b9a10ef`.

**"Found this round" bullets.**
- C2-counter bullet: `T49CritC2Contract.md` F1 (pristine guard reachable in the generator's cwd; a differential
  generator `confirmed` on 2/2 probe mutants) and F2 (no sandbox; panel readable from the lane at REV) are as
  summarized; F3's "the round's dump has 393 distinct cases of 400" reproduced by my own count over the committed
  `T49ExecGenerator.pristine.dump.jsonl` → 400 lines, 393 distinct `(registry, staged, map)`.
- C1-counter bullet: `T49MutC1Counter.md` — 28 mutants, 14 killed, 14 survived; selftest never calls `measure()`;
  M14/M10 flip the label. Exact.
- Deciding-script bullet: `T49RevDeciding.md` F1 (working-tree execution) verified by reading
  `deciding-run.sh:44,47`; F2's shape verified at `deciding-run.sh:42` (`PANEL_NOT_REVEALED` sets `rc=1` and
  continues — the refusal fix F2 recommends was **not** applied to the frozen script; the bullet sits under
  "routed, not claimed as fixed", and the panel sha is indeed checked by the counter itself).
- Ledger-digest bullet: `ledger.json:24170` records
  `".ufo/evidence/round-14/context-missing-env.json": "9a3a3f9b5a62…e2f3a4b"`; my own
  `sha256sum` of the blob at `f181a961` → `1ee9d09bc527…52aa208` — never matched, and the digest's tail is a
  visible placeholder pattern; `T49RevengerLapse.md` §6.1 documents it.
- Guard-docstring bullet: `T49RevGuardExit.md` confirms analysis `refused` → exit 1 while the docstring's exit
  paragraph names exit 1 only for an inadmissible map; the guard is unedited since base (0 commits) and
  sha-matches the contract pin.

**considerthese.** `considerthese/2026-10-26.md` exists in the lane at `f181a961`; proposal 3 is "Recurring-defect
tracker for closures" with the operator's example "(uncommitted selftest receipts: round 45, fixed 46, back in
47)". Every number in the lesson's paragraph matches `T49ScribeConsider.md`: 9 closures (rounds 40–48), 44
status-neutral defects, 26 classes, 10 recurring classes carrying 24 rows; the four criterion-backed recurrences
(pointer-unresolvable under 72/81/97; record-drift after 35; monitor-false-red after 88;
standing-row-unreproducible after 92); the measured-rule criteria 87/91 with zero recurrence; and the round-47
byte-level fact — I re-derived it myself: `git -C LANE ls-tree --name-only 03facb22 -- .ufo/evidence/round-47/`
lists no `selftest/` directory. The round's own selftest receipts are committed at `f181a961`
(`.ufo/evidence/round-49/control/c{1,2}-selftest.{stdout,exit}` all present in `git ls-tree`).

**C1 section.** Extractor pointer count 90 verified (`c1-pointers-at-base-8ca67421.json`); the seats' tally is
exactly the lesson's — summing `base_verdict` over `T49Read01..18.rows.json` → `{'holds': 80, 'stale': 2,
'absent': 3, 'unresolved': 5}` (90). Forty-five corrections = `corrections.json` 44 + `corrections_pass2` 1, and
the category breakdown is exact (12 false, 6 unverifiable, 2 stale, 1 off-by-one, 2+3 bare, 2 placeholder, 9
whitespace, 8 precision — classified from the rows' `why`/`old`/`new` fields). The off-by-one landed:
`SKILL.md:221` at `f181a961` cites `mutation-case-kagi-census.md:111-114, :118-122, :252-254`, and at base line
251 is blank with the B10 clause on 252–254 (`cat -A` over `git show 8ca67421:corpus/knowledge/mutation-case-kagi-census.md`).
"Outside the seven sections" for SKILL.md:1509/1555 is true: the heading map at `f181a961` puts 1509 in
`### Gate/probe registry` (1499–1516) and 1555 in `### Round-13 gate/probe registry` (1548–1562) — separate
credited sections, matching the monitor's UNCOVERED spans (r12 1479–1498, r13 1517–1547). Executor claims:
"every exit reproduces" holds (R12: all 12 verdict/exit claims; R13: both commands + selftests; R14: 5/5 rows),
and the "two places" of decision-table-vs-printed-ids drift are R12's M2 ("Could not evaluate baseline" is a
string the tool never emits) and R13's M3 ("clean" gloss vs `metadata_consistent reason=ok`).

**pointer-check per its usage line.** `python3 .ufo/evidence/round-48/quality/pointer-check.py --selftest` →
`POINTER_CHECK_SELFTEST: cases=4 failed=0` (exit 0). On the lesson:
`python3 .ufo/evidence/round-48/quality/pointer-check.py --lane LANE --rev f181a961… --file
corpus/lessons/round-49.md --start "# Round 49 lesson"` →
`MISSING .ufo/waves/round-49/w1/T49Read01` + `POINTERS: file=corpus/lessons/round-49.md checked=25 missing=1
skipped=2 rev=f181a961…`, **exit 1** (findings F1/F2). All other checked tokens resolve at `f181a961`; the two
skipped tokens are the glob/brace forms attacked below and `c{1,2}-selftest.{stdout,exit}` (the latter's
referents all exist). Bare-name pointers not covered by the tool were resolved manually: `T49Sec*.findings.json`
(7), `T49ExecR1{2,3,4}Cmd.md` (3), `T49ScoutRecipeLines.md`, `T49ScribeMistake.emit-verbatim.stdout`,
`T49CritC2Contract.md`, `T49MutC1Counter.md`, `T49RevDeciding.md`, `T49RevengerLapse.md`, `T49RevGuardExit.md`,
`T49ScribePkgQuickCheckCorr.md`, `T49ScribePkgCraftAuthor.md`, `T49ScribePkgAsFixture.md`,
`T49ScribeConsider.md`, `T49ExecIdGuard.md`(+dir), `T49ScribeRows.src/`(+`fetch-receipts.json`),
`T49ExecSrcQuickCheck/`, `T49ExecSrcSmallbone/` — all present at `f181a961`.

---

## Findings

### F1 (medium) — Mistakes row 2 cites a wave-2 receipt path that resolves to nothing at the reviewed revision
- Attacks: `corpus/lessons/round-49.md:87` (Mistakes row 2, fix cell), backticked token
  `` `.ufo/waves/round-49/w2/T49W2ExecPrecheck.*` ``.
- Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only f181a961ae44061af486f600e5ea257d2baf78f8 -- .ufo/waves/round-49/w2/`
- Observed: empty output — the w2 tree contains zero paths at `f181a961`. The files exist only as uncommitted
  worktree files produced by this wave (`ls` shows `T49W2ExecPrecheck.coldread-precheck.stdout`, `.stderr`,
  `no-harm.stdout`, …).
- Why it matters: this is precisely the round-48 mined defect class that `pointer-check.py` was built for
  (a record citing a receipt that does not exist yet at the revision that lands it — QUALITY 97's lesson), and
  the automated check cannot see this instance: the token's `*` lands in pointer-check's SKIP set (its summary
  prints `skipped=2`). QUALITY 97's own text gives the remedy: "A record drafted before its receipts exist
  either waits for them or names them in words as pending." The pointer heals at the final tip only if the named
  receipts are actually committed; nothing automated will flag it if they are not.

### F2 (low-medium) — pointer-check exits 1 on the lesson: the `T49Read01` range token resolves to no path
- Attacks: `corpus/lessons/round-49.md:66`, backticked token `` `.ufo/waves/round-49/w1/T49Read01` `` in the
  range shorthand "`T49Read01`-`18`".
- Command: the pointer-check invocation above (selftest passes, so the detector is healthy).
- Observed: `MISSING .ufo/waves/round-49/w1/T49Read01` … `checked=25 missing=1 skipped=2`, exit 1.
  `git cat-file -e 'f181a961:.ufo/waves/round-49/w1/T49Read01'` fails; the seats' artifacts are
  `T49Read01.md` … `T49Read18.md` (all present). A landing defect per QUALITY 97; per that criterion's remedy it
  is corrected by an appended erratum (the range means `T49Read01.md`–`T49Read18.md`), never by rewriting.

### F3 (low) — the audit tally "12 false, 6 unverifiable" is the corrections count, not the critics' count
- Attacks: `corpus/lessons/round-49.md:66-67` — "Seven section critics audited every non-pointer statement
  (`T49Sec*.findings.json`): 12 false, 6 unverifiable."
- Command: `python3 -c` tally of `verdict` over the seven `T49Sec*.findings.json` at `f181a961`.
- Observed: `TOTAL {'false': 15, 'true': 113, 'unverifiable': 7}` — the critics' own files record **15 false +
  7 unverifiable**, not 12 + 6. The 12/6 figures are the *corrected* counts (they match `corrections.json`
  exactly: 44 + 1 rows; category counts verified). The four-finding gap is disposed in the artifacts —
  SKILL.md:1509/1555 re-judged true-but-stale and routed (lesson:75, disclosed — though the critics had marked
  both `false`, which the lesson does not say); Map 1385b ("before quoting any rate — the row is the standing
  receipt") absorbed into corrections row 22's rewrite of the same bullet (its new text adds "(eight rows; the
  round-26 ninth case has no row yet)"); Promotion 1466-1467 ("not the historical training closeout") absorbed
  into row 29's rewrite of the same sentence — but the lesson never reconciles the tallies, so a reader
  comparing the lesson against the cited findings.json files meets an unexplained four-row gap.

### F4 (low) — "the six record-free entries survived 17-20 rounds" overstates its own receipt
- Attacks: `corpus/lessons/round-49.md:78-80` — "…88 of 94 earlier entries carried a record file and lapsed
  within a median of one round, while the six record-free entries survived 17-20 rounds."
- Command: read `T49RevengerLapse.md` §4 (committed at `f181a961`).
- Observed: "**6 of 94** entries carry none. Their survival: 20, 18, 18, 17 rounds, plus two round-17/18
  originals that died in their own round (0 and 1) on tool/note edits." Four of the six survived 17–20 rounds;
  two survived 0–1. The lesson's "the six … survived 17-20" is false for two of the six it names; "the four
  later record-free entries survived 17-20 rounds" is what the receipt shows.

### F5 (low) — "Flip: none" elides the receipt's stated flip condition
- Attacks: `corpus/lessons/round-49.md:50-53` (reject of `r4-quickcheck-primary-correction.md`), sentence
  "Flip: none — the premise is false, not unverified."
- Command: read `T49ScribePkgQuickCheckCorr.md` (committed at `f181a961`).
- Observed: the receipt carries an explicit "**Flip condition (conjunction; each item is one command away from
  checkable)**" with four items (campaign-scoped anchoring, resolution-based DOI statement, corrected locators,
  rows re-opened 2026-10-26), then concludes that even flipped, "the economical landing is the two rows … plus
  one sentence of the F10 inference …; the correction narrative then carries no F10 content." The conclusion
  supports refusing the entry *as an entry*, but the lesson's flat "Flip: none" does not match the receipt's
  explicit flip heading — and the sibling rejects both name their flips, so the Gate's own convention is
  inconsistent here.

### F6 (low) — one executor-flagged section discrepancy has no correction and no lesson disposition (R12's M3)
- Attacks: `corpus/lessons/round-49.md:67-69` (the executor summary) together with
  `corrections.json` at `f181a961`.
- Command: `grep -c 'controls-UNIQUE\|tameshi-r12-' corrections.json` → `0`; read `T49ExecR12Cmd.md` §M3.
- Observed: `T49ExecR12Cmd.md` M3 — `SKILL.md:1503`'s write-scope glob ("isolated `/tmp/tameshi-r12-*`
  selftest") overlaps the recipe's own example path `/tmp/tameshi-r12-controls-UNIQUE` (`SKILL.md:1492`). No
  correction row touches it and the lesson's summary reports only "every exit reproduces" and the two
  wording-drift places. The line sits in `### Gate/probe registry` (1499–1516), outside the seven re-keyed
  sections, so the same restraint that held back 1509/1555 applies — but then it belongs beside the "Not
  applied" disclosure (lesson:75), which names only two sentences. (R13's M3 — the exit-0 gloss "clean" at
  `SKILL.md:1553`, likewise outside the seven — is at least disclosed as one of the "two places".)

### F7 (observation) — reads.json re-derives base verdicts differently from the tally the lesson quotes, without a note
- Attacks: `corpus/lessons/round-49.md:65-66` vs `.ufo/evidence/round-49/c1/reads.json` (both at `f181a961`).
- Command: `python3` join of `reads.json` rows against `c1-pointers-at-base-8ca67421.json` on `(heading, ordinal)`.
- Observed: reads.json has 94 rows (all distinct pointers); over the 90 extractor pointers its `base_verdict` is
  `{'holds': 75, 'new': 2, 'stale': 3, 'absent': 5, 'unresolved': 5}`, and 4 rows are pointers the frozen
  extractor does not catch (bare file names, all `holds` — consistent with the "3 bare file names qualified"
  corrections). The lesson's 80/2/5/3 matches the *seats'* rows.json tally exactly and is attributed to them
  ("read by eighteen seats"), which is accurate — but nothing in the lesson or reads.json explains the
  re-derivation delta or the 94-vs-90 surplus; a reader reconciling the two committed records meets different
  numbers with no note. (The 18-seat claim itself is fine: reads.json's 20 distinct reader strings are the 18
  seats plus the L1 for two correction-introduced pointers plus one variant string.)

---

## Residual risk and verification gaps

- I ran no counter and no `--selftest` of a claim counter (bounds; the deciding run is the L1's). Nothing here is
  a verdict.
- I did not re-verify all 45 corrections' old→new against the SKILL.md diff; I verified the total (44+1), the
  category counts, and the off-by-one end to end (base blank line 251 → `:252-254` cited at `f181a961`).
- `T49ScribeConsider.md`'s 44-row defect table was re-derived by that seat only for row 42 and the receipt
  inventory; I verified its headline numbers against its own table and re-derived the round-47 selftest absence
  myself, but did not re-audit each of the 44 rows against the nine spot-check files.
- The S269/S270 quotes were verified against the committed, sha-pinned snapshots (which match two independent
  wave-1 fetches and the rows' digests), not against a fresh fetch of the two URLs today.
- F1's disposition belongs to the L1: commit the named wave-2 receipts before the final REV (they exist as
  worktree files now) or reword the pointer as pending per QUALITY 97; F2's is a one-line appended erratum.

## Summary

- Gate rows S269/S270 fully verify: quotes verbatim at the claimed pages in sha-pinned snapshots (20/14/19 words), sizes+sha256 match two independent fetches, Crossref pp. 268-279, ACM 302→403, recheck 365d, used-by pilot; SOURCES diff additions-only (5/0); stale Next-unused-id note corrected.
- Assimilation verifies end to end: 2 admits + 2 rejects + 1 deferred; collision numbers (128/103/8; 9-vs-8 column-zero proof), quarantine (17 rows; S182/S183 zero hits), the S183 anchor correction (§2.10 printed p. 34, not §4.1 p. 44), the DOI reject (404 at doi.org/Crossref; zero pre-round-49 occurrences) and the craft-author grounds (S170 "via a toy example in C" re-fetched, sha match; S116 never a row) all reproduce.
- Mistakes rows 1-3: every pointer resolves at `f181a961` and says what the lesson claims; gate-0 able-to-fail shown (three refusal shapes, exit 3, empty dirs); criterion 99 exists.
- Two pointer-resolution defects: the w2 precheck receipt path (row 2) resolves only after wave-2 receipts land and is invisible to pointer-check (glob-skipped) — F1; the `T49Read01` range token is MISSING (pointer-check exit 1) — F2.
- Numeric imprecisions: audit tally 12/6 vs findings.json 15/7 with the four-row gap unreconciled (F3); "six record-free entries survived 17-20" though two died at 0-1 (F4); "Flip: none" vs the receipt's flip condition (F5); R12's M3 undisposed (F6); reads.json base_verdict re-derivation unexplained (F7).
- considerthese verifies against its receipt and the round-47 tree; the round's selftest receipts are committed.
- pointer-check on the lesson: `checked=25 missing=1 skipped=2`, exit 1 (selftest 4/4 pass).
- No counter run, no claim decided; lane writes: this report + `T49W2RevLesson.s170.pdf`; zero tool installs; scratch deleted.
