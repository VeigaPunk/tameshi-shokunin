# T49SecRecipe — C1 section audit: `## Mutation-sweep recipe` (SKILL.md:131-245)

Seat: T49SecRecipe (critic, C1 section audit). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base: `8ca67421111fa354b47b803358391d0b07fc6db9`. Section bytes are identical at base, at HEAD
`455b2cd` and in the worktree (`git diff --stat 8ca67421 -- SKILL.md …` → empty; receipt R1), so
every line number below is a base line number.
Deliverable: `.ufo/waves/round-49/w1/T49SecRecipe.findings.json` (45 statements);
receipts: `.ufo/waves/round-49/w1/T49SecRecipe.receipts.txt` (R1-R10).

Result: **2 false, 3 unverifiable as written, 40 true**; 11 proposed fixes (5 substantive,
6 spacing-only). No `file:N` pointer is deleted and the heading is untouched by any fix.

## False (reported first)

1. **SKILL.md:142-144 — "kumitate `n/m pass` + `VERDICT:` (gates-survey-kumitate.md:19-31);"**
   `awk 'NR>=19&&NR<=26{print NR"|"$0}' corpus/knowledge/gates-survey-kumitate.md` (R2) shows
   two of the six rows do not use that shape: `:21` cite-check `62/62 cases passed (hermetic)` and
   `:22` surface-probe `42/42 cases passed`; only `:23-:26` print `n/m pass`. A reader who greps
   for the recipe's literal shape fails on two of the six cited suites, and
   `grep -n 'cases passed' corpus/knowledge/gates-survey-kumitate.md` → `21,22` (plus prose hits
   47/97/126) confirms the second format is the documented one for those two.
   Fix: `kumitate \`n/m pass\` (cite-check and surface-probe print \`n/m cases passed\`) + \`VERDICT:\` (gates-survey-kumitate.md:19-31);`

2. **SKILL.md:224-225 — "Re-run step 2's checks:"**
   Step 2 (`SKILL.md:150-151`, R3) records **seven** cells: path, full sha256, size, line count,
   mtime, repo revision, porcelain empty. Step 9 (`SKILL.md:224-226`) then re-runs four — line
   count and repo revision drop out of its own enumeration. The page already says the models do
   not establish the after-revision: `SKILL.md:388` "no after-repo revision was recorded" and
   `SKILL.md:391` "Its after-repo revision is likewise not established by those records"
   (`awk 'NR>=386&&NR<=391' SKILL.md`). Round 27's own cold reader flagged the identical mismatch
   (`.ufo/waves/round-27/w1/Read03.md` minor_gaps[0]) and the base text still carries it, so this
   is a surviving round-27 defect, not a new one.
   Fix: `Re-run step 2's checks (line count and repo revision included; neither model note records an after-revision — Restore discipline:386-391):`

## Unverifiable as written (assertion beyond the cited bytes)

3. **SKILL.md:171-174 — "print the count and first matching line, and require the literal line
   `all unique` — both lanes' drivers did exactly this"**
   The two cited ranges record the uniqueness assertion and `all unique` plus a "first-line match"
   (`corpus/knowledge/mutation-case-kimi-census.md:22-25`; `…kagi-census.md:44-47`, R4) — neither
   records a printed count. The drivers themselves no longer exist:
   `…kagi-census.md:271-272` "The old §7 commands depend on an unversioned scratch
   `mutate_driver.py`; they do not by themselves recreate that driver after scratch loss", and
   `SKILL.md:396-400` repeats it. The count-printing half has no checkable source.
   Fix: drop that half and point at the driver that prints counts today
   (`tools/mutate-and-run.sh:425`, `APPLY FAIL … old-string-count=`).

4. **SKILL.md:176-177 — "The cited historical notes do not establish that particular round-2
   guard."**
   Referent is ambiguous and the two readings have opposite truth values.
   `grep -nE 'all unique|new != old|no-op' …kimi-census.md …kagi-census.md` (R4) returns no
   `new != old`/no-op hit, so on the no-op reading the sentence is true; but the round-2
   uniqueness guard **is** established at `kimi-census.md:22-25` and `kagi-census.md:44-47`
   (the sentence two lines earlier credits exactly that), so on that reading it is false.
   Fix: name the guard ("…that the round-2 driver carried the `new != old` no-op guard.").

5. **SKILL.md:210-211 — "inconclusive runs are excluded from the denominator and named beside
   it."**
   Neither model exercised the rule (`kimi-census.md:29-30` "No inconclusive run";
   `kagi-census.md:50`), so it is presented as measured method without a measurement. The lane's
   standing instrument uses the opposite denominator: `tools/mutate-and-run.sh:570`
   `pct=$(( (200 * killed + total) / (2 * total) ))` over **all** defects, with
   `:571-574` marking the run DEGRADED and exiting 1 (`awk 'NR>=569&&NR<=574' …`, R5). Section and
   instrument disagree in silence.
   Fix: label it a design choice and name the instrument's contrasting denominator.

## True, content correct but the token is fused (typography of numbers)

All six are correct values rendered unreadable/unselectable; each fix restores spaces only and
keeps every pointer.

- **:146** "`VERDICT: PASS`, exit0" — `kimi-census.md:20-21` prints `exit 0` (R8). Fix → `exit 0`.
- **:147** "and bash16 enumerated cases," — `kagi-census.md:33-35` (16 cases, 14 executed +2 skipped,
  R4/R8). Fix → `and bash: 16 enumerated cases,`.
- **:193** "denominators43 and16" — 43 (`kimi-census.md:32-33`) and 16 (`kagi-census.md:51`) are
  right. Fix → `denominators 43 and 16`.
- **:241** "Round2:7.0s for11 runs, nodev24.21.0" — `kimi-census.md:21,30-31` (R8). Fix →
  `Round 2: 7.0 s for 11 runs, node v24.21.0`.
- **:242** "round3:11.0s for11 runs against a280s bound" — `kagi-census.md:50-53` (R8). Fix →
  `round 3: 11.0 s for 11 runs against a 280 s bound`.
- **:243-244** "Kimi U5 at204-205; Kagi U5 at203-204." — both pointers resolve
  (`kimi-census.md:204-205`, `kagi-census.md:203-204`, R8). Fix → `U5 at 204-205; Kagi U5 at 203-204.`

The same de-spacing damage sits elsewhere on the page (`SKILL.md:387` "hash83016d45",
"43273B", ":389" "unchanged09:47:15"), so this is a page-level rendering regression, not six
independent typos; a page-wide sweep is the L1's call, the six entries above are this section's.

## True (evidence exercised, no fix proposed)

Every remaining number, count, status sentence and command line in 131-245 was checked against
its cited bytes and, where possible, against the pinned artifacts:

- **:134-135 "round 16's full-page cold-read executed it end to end (two seats; Errata — round 16)."
  This was the strongest counterexample I could build and it did not land.** Both seats really
  executed it: `.ufo/waves/round-16/w1/CR04a.md` (step 1-10 table, pinned-rev sweep) and
  `CR04b.md` (same on the moved worktree bytes); the ledger agrees
  (`{start:131, seats:['CR04a','CR04b'], verdict:'gap-minor', blocking_gaps:0,
  commands_executed_count:18}`, R7); `SKILL.md:1726` is the erratum row recording the repair. The
  one shortfall is minor and already declared by the seats: step 10's corpus row stayed L1 scope
  (`CR04b.md` minor gap 1), which is why the ledger says `gap-minor` and not `executed-ok`. The
  statement is at the ledger's precision, not overstated.
- **:134 "The recipe is intended to be self-contained;"** — a cold reader authored the missing
  driver from the section alone and it caught its own non-unique `old` (`CR04a.md` step 5,
  "I authored one in ~80 lines from the description alone"). The reproducibility caveat
  (`kagi-census.md:271-272`, `SKILL.md:396-400`) belongs to Restore discipline item 6, not here.
- **:136** scratch namespace matches `SKILL.md:25-28` and both notes (`kimi:5,171`; `kagi:4,242`).
- **:138-139** `--selftest` alone does not establish hermeticity — `kagi-census.md:24-30` proves it
  by the fixture builder plus the two gated skip cases.
- **:144** "`SELFTEST: PASS (n cases)` includes its enumerated skip entries" — the pinned gate
  increments `cases` in both branches (`.ufo/evidence/round-12/BashWitness/pristine.sh:816,822`,
  sha256 `275d8294…53009f` = the kagi pin; R6) and prints `PASS (%s cases)` at `:846`.
- **:145-146** `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 — `kimi-census.md:20-21`,
  reproduced at the pinned sha by `CR04a.md` step 1.
- **:147-148** "14 executed +2 skipped" — `kagi-census.md:33-35`.
- **:149** a red control has no kill denominator — the standing driver says the same
  (`tools/mutate-and-run.sh:530-533`, `cannot attribute kills`).
- **:150-152** the seven-cell pin record — `kimi-census.md:13-16`; `kagi-census.md:13-17`.
- **:153-154** "that gate's 887th line carries no trailing newline" — `kagi-census.md:14-15`; on the
  sha-matched pinned copy `tail -c1 … | xxd -p` → `63` ('c') (R6).
- **:154-156** the dirty-intermediate re-pin — `corpus/README.md:11` (G-R2-1 row,
  `git cat-file -t 357fb24554cd0447` → fatal: not a valid object name) and
  `corpus/knowledge/gates-survey-kagi.md:554-561`.
- **:158-160** `mkdir`/`cp -p`/`cmp` — `kimi-census.md:171-172`; `kagi-census.md:44-45,242-243`.
- **:162-163** "8-12 defects, one per class" — the next section (246-313) carries the entry
  template (`:254-262`) and a 12-row catalog (`:293-306`); CR04a ran 12, CR04b 11. Nuance handed to
  the L1: under the notes' own labels the manifests repeat classes (`kimi:44-48` D1/D2, D4/D5;
  `kagi:70-71` B4/B5), so the rule holds only in the catalog's finer vocabulary — round-27
  `Read03.md` minor gap 3, still open.
- **:165-166** the 10-defect manifest — `kimi-census.md:44-53`, `:155-166`.
- **:166-168** pre-registration / E1 kept — `kimi-census.md:185-191` (D7 missed, kept);
  `kagi-census.md:186-191` (case counts miscalled, kept).
- **:171-173** `count(old)==1` + literal `all unique` — `kimi-census.md:23-24`;
  `kagi-census.md:45-46,245`.
- **:175-176** `new != old` required of future drivers — enforced today by
  `tools/mutate-and-run.sh:52,403,1615` ("no-op edit refuses (exit 2)"; R9).
- **:177-178** count ≠1 aborts — lived: `CR04a.md` step 5 hit `UNIQUENESS FAILURE` on D9
  (`count=2`, `:292`+`:305`) and no mutant ran before the string was re-derived.
- **:183-184** 300 s / 280 s bounds — `kimi-census.md:31`; `kagi-census.md:52-53`.
- **:185-187** retention differences — `kimi-census.md:26-28` vs `kagi-census.md:48-49` (wall time +
  summary added).
- **:195-196** verbatim failing labels — `kimi-census.md:59-78`.
- **:198** `SELFTEST: FAIL (1/16 cases)` — correct string, and I verified it from the artifact, not
  the note: the pinned gate's epilogue is `printf 'SELFTEST: FAIL (%s/%s cases)\n'` at
  `pristine.sh:847` (R6). Citation note for the pointer seats: the cited `:82-103` carries the
  bad-case line (`:84`) but not the summary; the note's table shows only `1/16` / FAIL at `:67`.
- **:200-202** B4 token-only kill — `kagi-census.md:88-91`
  (`bad-case 07 symlink-swap want exit=1 token=SURFACE LINK got exit=1`).
- **:205-206** "a finding, never a footnote" — `kimi-census.md:44-45`, `:135-142`.
- **:211-212** 8/10, no inconclusive, 11 runs, 7.0 s — `kimi-census.md:29-31`; round 3 8/10,
  11.0 s — `kagi-census.md:50-53`.
- **:216-217** D2 `+23 more` vs `+22 more`, D10 `frozen=24` vs 25 — `kimi-census.md:90-99`.
- **:218-220** B5 `SURFACE OK … (exec 644)` exit 0 / pristine `SURFACE DIVERGED … no execute bit`
  exit 1; B10 `ok=0` vs `ok=1` — `kagi-census.md:111-114,118-122`, repeated at `:252-254`.
- **:225-226** restore cells — `kimi-census.md:34-35`; `kagi-census.md:54-56`.
- **:228** "(SKILL.md:377-378; corrected in round 27, seat Read03)" — `SKILL.md:377-378` is the
  endpoint-identity sentence and round 27's `Read03.md` verdict is `wrong-expectation` with the
  step-9 "absence of writes" quote as `wrong_expectations[0]` (R10); the repair is in the base text.
- **:229** "Full checklist below (Restore discipline)" — `SKILL.md:375-403`.
- **:234-237** model sections `kimi §1,§3-§6` and `kagi §1-§7` all exist (headers at kimi
  `:39/:109/:148/:183/:193`, kagi `:62/:128/:162/:184/:193/:211`); counts are quoted from run
  summaries only.
- **:240** cost profile = wall time + timeout + versions — both notes carry all three.
- **:243-244** cross-host stability unknown — U5 rows: `kimi-census.md:204-205`,
  `kagi-census.md:203-204`.

## Method and limits

- Read-only on the lane: `git diff`/`git show`, `awk`, `grep`, `sha256sum`, `tail`, one `python3`
  read of the committed round-16 ledger. No counter invocation, no `--selftest`, no writes to the
  lane, its Git index or its jj state; nothing read under `/home/vgpnk/.local/state/`; neither
  forbidden C2 stdout file opened.
- Scratch: `/fast/scratch/hyaku/tameshi-r49/T49SecRecipe/` (one base-byte copy used to verify
  uniqueness of the 11 proposed `skill_old` strings); removed before this report was written.
- Not my lane's call: line pointers themselves (other seats), whether any correction is applied,
  and the C1 label. Pointer-shaped observations I met but did not score: the `:251-253` citation
  reaches the sensitivity sentence only through `:252-254`, and `:198`'s summary string is not
  inside `:82-103`.
- Tooling: no installs or upgrades (pacman paused; nothing needed). No model passed.

## Summary
- 45 statements in SKILL.md:131-245 checked against base bytes and the pinned artifacts: 2 false, 3 unverifiable, 40 true.
- False: `:142-144` "kumitate `n/m pass`" (cite-check/surface-probe print `n/m cases passed`) and `:224-225` "Re-run step 2's checks" (two of the seven cells silently dropped; a round-27 defect still open).
- Unverifiable: `:171-174` printed-count claim (drivers unversioned/lost), `:176-177` ambiguous "round-2 guard", `:210-211` inconclusive-exclusion rule that neither model exercised and the standing driver reverses.
- The strongest counterexample I could build — "round 16 executed it end to end" — held: two seats, a ledger entry, an erratum row; only step 10's corpus row stayed L1 scope, which the ledger already scores gap-minor.
- Numbers behind the cost profile, kill rates, probes, pin/restore and E1 rows all match their cited bytes; six fused tokens (`:146,147,193,241,242,243`) are the section's copy-paste damage.
- 11 proposed fixes: 5 substantive, 6 spacing-only; none deletes a `file:N` pointer, none renames the heading.
- Deliverables: `T49SecRecipe.findings.json`, `T49SecRecipe.receipts.txt` (R1-R10), this report; scratch removed.
