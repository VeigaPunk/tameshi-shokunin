# ReviewCase8Entry — review of `corpus/knowledge/mutation-case-kumitate-sources-check.md` @ 01d586dd

Seat: TameshiR18.ReviewCase8Entry (reviewer, wave 2). Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.
Entry sha256 `79f629b4b5b3790c480a2ce854513dded61642cd7731bb74a4e9d302a7eac0ce` (219 lines).
Axes: calibration (are the entry's numbers, shas, lines and timestamps true, and are its sources right?), depth (is the case-8 record sound?). I also watched operability: every command ran in a `/tmp` clone, under bwrap with the fleet read-only.

Clone: `/tmp/tameshi-r18w2-ReviewCase8Entry-5ODMxT/fleet/tameshi-shokunin` at the read rev (`git rev-parse HEAD` → `01d586dd…`, exit 0), siblings symlinked. This report is my only lane write. I installed nothing. No `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` or `GIT_COMMON_DIR` was set. Kumitate reads used `git --no-optional-locks -C` (read-only).

Every number, sha, line and timestamp in the entry was checked. 26 claim groups hold (table at the end). 5 findings are Medium, 11 are Low and 5 are Info. Survivor non-equivalence is correctly marked PENDING.

## Medium

**M1. K_ROWS's kill does not depend on awk, and the entry says it does.** Entry §6 `:196-200` says K_ROWS's kill channel is the awk parity check, so K_ROWS is "a result on an awk-present host only" and the spec has no "second, non-host-gated witness". §3 `:147-148` says D1 is touched "without the second, non-host-gated witness". All three statements are false.

- The recorded sweep already shows a second channel. `sweep/sweep.txt:75`, inside the K_ROWS block `:74-82`, is a FAIL detail line, `exit=0 last=SOURCES_CHECK: CLEAN (rows=4 tiers=A:2,…)`. That is the S1000 check, failing before the awk FAIL at `:79`. The tally is `41/46` (`:81`), which means 5 checks failed, not 1.
- The pre-registration already names a non-awk witness. `predictions.json:43` says "…and the clean fixture also pins rows=1".
- The pinned code asserts `rows` in four checks that do not use awk: `sources-check.mjs:589` (clean, `rows=1`), `:690` (indented, `rows=4`), `:816` (`--json` `counts.rows === 1`) and `:824` (S1000, `rows=2`). Only `:866` is the awk parity check.
- I measured it. `python3 run-mutants.py` replayed the exact `suite.txt` string under bwrap (exit 0). K_ROWS is KILLED with 5 FAILs: `clean fixture returns CLEAN`, `1-3-space … normalized`, `--json prints one parseable contract object`, `S1000 is accepted and counted`, and `frozen awk census parity`.
- I then ran with awk absent: `run-mutants.py --no-awk-path <dir with node, sh, env, mkdir only>`, exit 0. The control is `45/45 pass`, with the parity check printing `SKIP … awk is unavailable`, exit 0. K_ROWS is `41/45 pass`, exit 1, **KILLED**. The full 10-defect table is unchanged with awk absent: 5 KILLED and 5 SURVIVED, with the same IDs.
- Correction: K_ROWS has four non-host-gated witnesses. The leg table is portable to hosts without awk; this was measured for all ten defects. The spec touches D1, D3 and D5 of K02's test (`w1/K02CaseDepthValue.md:145-156`), not only D3 and D5.

**M2. "44 of 46 checks assert `(exit, kind)` only" (§3 `:123`) is false at the pin.** In the pinned selftest, 29 checks assert exit plus finding kind (the 23 table cases with expected exits at `:592-674`, plus `:740`, `:745`, `:751`, `:775`, `:781` and `:809`). Another 3 compare the exact FAIL-CLOSED final line (`:799-800`). The other 14 assert something else: verdict-line prefixes or counters (`:589`, `:690`, `:768`, `:824`), finding counts and `id=` fragments (`:710-711`, `:725-726`), the constant list length (`:756`), meta-checks (`:785`, `:804`), JSON fields (`:816`), usage or contract text (`:829`, `:833`, `:837`) and awk parity (`:866`).

My replay shows the same thing at runtime: checks #1, #25, #26, #35, #39, #41, #42 and #46 fail under mutants, so at least 8 checks assert more than `(exit, kind)`. The number comes from `w1/S19CaseOwnerRecon.md:57`, and that same paragraph lists at least 10 exceptions to it. The entry also contradicts itself: `:139-140` cites check 32 asserting `entries_with_source=0 legacy=1`. The qualitative point for the five survivors still stands; the count does not.

**M3. The source header says S008 is queued, but S008 is mined.** Header `:1` reads "S008 … **queued** — … not yet a mined row", and §6 `:215-216` says "S008 is `queued` with `used-by —`". The entry first appears in `58e5d53`. At `58e5d53`, `e08271a` and `01d586dd`, `corpus/SOURCES.md:19` has S008 as `mined` with used-by `corpus/knowledge/mutation-case-kumitate-sources-check.md` (checked with `git show <rev>:corpus/SOURCES.md`, exit 0). So the header was never true at any commit. The L1's staged gate (`.ufo/waves/round-18/staged/lesson-round-18-gate.md:42`) records the queued→mined flip.

**M4. "S066 record" points at the wrong registry row.** Header `:1` and §1 `:80` cite the Q1 quote as "S066 record". In the registry, S066 is RFC 8259 (`corpus/SOURCES.md:75`, used-by `guard-kill-closure.md`). The file the entry means, `.ufo/waves/round-18/sources/S066-B02SrcGoogleMutation.md:1-3`, is titled "S066 draft — DUPLICATE S008". The ID S066 was then reassigned (`staged/lesson-round-18-gate.md:48`, "S066 ← draft S068 (RFC 8259)").

Parsers read the token as a citation. I ran kumitate's gate on the clone as a probe only, since it is not tameshi's gate: `node sources-check.mjs --self <clone> --today 2026-10-20` (exit 1). It prints `USED_BY_ASYMMETRY corpus/knowledge/mutation-case-kumitate-sources-check.md:1 S066 used-by omits …`; its header regex is at `:370`.

The quote itself is correct. I fetched https://arxiv.org/abs/2102.11378 and Q1 is verbatim, abstract item (3), 19 words. Fix: cite S008 (mined) for Q1, and refer to the draft by its path without the bare `S066` token.

**M5. The measured file has no registry row, and four cited rows do not list this entry in `used-by`.**

- *No row for the target.* Every earlier kumitate target has a code-kind row: S032 kimi-census, S037 claims-check, S053 round-gate. Case 7's header opens `source: S053`. `scripts/sources-check.mjs` has no row; searching `corpus/SOURCES.md` finds only S008's used-by path. This conflicts with `corpus/QUALITY.md:27-30` (criterion 10). R01 raised it in wave 1 (`w1/R01CaseAcceptance.md:16,40`) and it is still open at the read rev.
- *Used-by not updated.* Contract v1 defines `used-by` as the "paths of the knowledge entries or lessons citing the row" (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:40-41`). The used-by cells of S001, S052, S056 and S057 omit this entry (`corpus/SOURCES.md:12,61,65,66`). The entry names this obligation itself (`:215-219`), but the L1 changed only S008 (`staged/lesson-round-18-gate.md:42`, "the only change to an existing row"). The lane's own gate does not catch this: `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `SOURCES_CENSUS: CLEAN`, exit 0, because it checks only the row-to-entry direction. The kumitate probe flags five asymmetries for this entry: S001, S052, S056, S057 and S066.
- *Coverage map incomplete.* `corpus/README.md:265` lists sources "S001, S008", while case 7's row `:226` lists all of its sources. The row also cites `lessons/round-18.md`, which does not exist at the read rev (`git cat-file -e` failed).

## Low

- **L1. Case 7's suite is the same bytes, not just the same shape** (`:28-29`). `.ufo/evidence/round-16/round-gate/suite.txt` and `.ufo/evidence/round-18/sources-check/suite.txt` are byte-identical: both sha256 `6e550d5a…`, `cmp` exit 0. The runner strings at `tools/mutate-and-run.sh:1346` and `:1351` are also identical. SKILL.md `:1910-1911` states it correctly.
- **L2. Wrong hash abbreviation** (`:34`). The entry writes `e0880a5a…e5`, but the hash ends `…44665e5f`, so `e5` is not its suffix. Elsewhere the entry uses the true last four hex digits, e.g. `…258f`.
- **L3. The L1's check receipt ran different runner bytes.** `.ufo/evidence/round-18/leg8-L1-check.txt:10` names `repo=/tmp/tameshi-r18-L1-leg8-qXUNVy/…`. The runner in that mirror has sha256 `701a95cb…` (97,009 B, mtime 16:48:57 -0300, the mirror's creation time). It differs from the landed `d22c4025…` only at `:1351`, where its js-sources-check suite is the bare `node "$MUTANT" --selftest`. So the receipt exercised the unguarded suite, not the `suite.txt` string that §5 `:171-172` says is embedded. [INFERENCE: based on the receipt's path and an mtime unchanged since creation.]

  The runner prints `REGRESSION_TOOL … sha256=` (`:1299`), so the 17-line receipt is a filtered excerpt, contrary to QUALITY 21. The entry does disclaim that the receipt names no runner (`:181-183`). The claim still holds on the landed bytes: I ran `bash tools/mutate-and-run.sh --regression` at 01d586dd under bwrap. It took 196 s and exited 0. Output: `REGRESSION_TOOL … sha256=d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`, `REGRESSION_TABLE js-sources-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0`, `REGRESSION_CASE js-sources-check: PASS`, `REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)`. All 8 legs passed; output sha256 `1ac57fca…`, kept in scratch.
- **L4. Draft-time statements are now stale.**
  - `:43-45`: the sweep and control directories are no longer untracked; they were committed in 58e5d53.
  - `:174-183`: "not installed / installed-runner receipt pending" is out of date. The leg was installed in 58e5d53; `tools/mutate-and-run.sh` sha `d22c4025…` equals the staged copy (`cmp` exit 0), and the L3 run is the installed-runner receipt.
  - `:219`: the coverage-map row now exists (README `:265`).
- **L5. The repeat controls were not run with the `suite.txt` string** (`:32`). `control/repeat/command.txt:5-7` shows a direct `env -i … node sources-check.mjs --selftest` argv (cwd `materialized`, TMPDIR `private/tmp`). The stdout is the same anyway: it matches `control.txt:6`, and my replay of the `suite.txt` string also gave `e0880a5a…`.
- **L6. "The first mutant ran at 19:41:29Z"** (`:52-53`). That time is the runner's start stamp, printed before the control (`93d22aa:tools/mutate-and-run.sh:485`, `:522`). In `/tmp`, two placeholder "dummy" mutants, R18D1 and R18D2, ran on the same blob at 16:40:41 -0300 (19:40:41Z), in `/tmp/tameshi-r4-2-regression.p545BJ/js-sources-check/defects.tsv`. That is still 20 s after 93d22aa. Every copy of the file older than the commit hashes to pristine `6a293a72…`, and K02's M1–M7 ran between 16:41:48 and 16:42:38 -0300. So "committed before any mutant ran" holds. [INFERENCE: based on `/tmp` mtimes.]
- **L7. Bare line cites point at the wrong repo.** `:13` `SKILL.md:605`, `:160` `SKILL.md:629-630`, `:197` `LOG.md:1496-1498` and `:208` `SCORECARD.md:1616` are kumitate's files. They are correct at 0acb7752, d933e15 and 1770305. Read lane-relative, they land on tameshi `SKILL.md:605` (kagi census text) and `:629-630` (unrelated). The other two point past the end of tameshi's files at 01d586dd: `LOG.md` has 1,083 lines and `SCORECARD.md` has 645.
- **L8. The two SCORECARD reads do not disagree** (`:209-210`). Both are right for the revision each read: kumitate `SCORECARD.md:1616` is 42/42 at 0acb7752 and 46/46 at d933e15 and 1770305.
- **L9. Tail length** (`:108`). Each suite tail in the sweep is 8 lines, not about seven (`sweep.txt:12-19`, `:21-28`, `:39-46`, `:75-82`).
- **L10. The SKILL.md eighth-case table** (`SKILL.md:1917-1921`):
  - It drops the PENDING qualifier on non-equivalence that the entry carries.
  - Its row 3 "does not pin" cell, "detail text and non-row counters", fits neither S_FILE_READ nor S_DUP_LINE. S_FILE_READ changes the fail-closed kind in a per-entry read arm the suite never reaches (pin `:355-356`). S_DUP_LINE changes the finding's `line` field (pin `:477`).
- **L11. Small evidence-file defects.**
  - `control/hazard-summary.md:1` is titled "Round-16 …", and `:3` ends with "run: " followed by nothing.
  - `PROVINCE.md:80-81` cites kumitate `PROVINCE.md:15` for the contract `kumitate-sources-v1`, but that id appears only at `sources-check.mjs:55`. It is not in kumitate's PROVINCE.md or SKILL.md at 0acb7752.

## Info

- **I1. The per-check attribution gap (`:107-118`) can now be closed.** In my replay, every killed defect's predicted check is among its FAILs:
  - K_KIND: `TIER_ENUM: fixture…`, plus the indented-rows check and the declared-kinds meta-check.
  - K_EXIT: both exit-64 checks.
  - K_STRICT: `--strict promotes warnings to drift`.
  - K_CLOSED: `SOURCES_MISSING: fail-closed exit 2`, plus the fail-closed meta-check.
  - K_ROWS: see M1.
- **I2. Survivors are correctly marked PENDING** (`:150-163`), which meets the acceptance condition. Witnesses already exist: R01's in-lane report (`w1/R01CaseAcceptance.md:28-34`) and my own run, `python3 witness.py` (bwrap, exit 0). On every probe, mutant and pristine had the same exit but different stdout:
  - S_KIND: the `findings:` usage line drops `RECHECK_OVERDUE`.
  - S_VERDICT: `DRIFT (ENTRY_HEADER_REQUIRED)` becomes `DRIFT [ENTRY_HEADER_REQUIRED]`.
  - S_DUP_LINE: `SOURCES.md:13` becomes `:14`.
  - S_ENTRY_COUNT: `entriesWithSource` 8 becomes 16.
  - S_FILE_READ: with an unreadable knowledge file (mode 000, euid 1000), `FAIL-CLOSED (READ_FAILED)` becomes `FAIL-CLOSED (SOURCES_MISSING)`.

  A closure must therefore argue at the stdout or verdict-line level, not on exit. S_VERDICT and S_ENTRY_COUNT already differ inside the recorded suite's own stdout: replay sha `9a45a5d1…` and `b8b78cfa…` against control `e0880a5a…`, and `sweep.txt:94` shows `entries_with_source=2`.
- **I3. The S052 mapping is a family analogy, not operator identity** (`:67-74`, `:203`). The Stryker page lists 16 mutator groups, of which StrykerJS supports 14. The five the entry names are a subset. Stryker's String Literal mutator is `FilledStringToEmpty`, and its Array Declaration mutator turns `[1, 2, 3, 4]` into `[ ]`. So none of the six non-numeric edits is a mutant Stryker would generate.
- **I4. The node version is not cited.** `node v24.21.0` (`:187`) is backed by `w1/C01KumitateOverlap.md:115` and `w1/C05SourcesAdjacency.md:40`, and this host is also v24.21.0.
- **I5. "C05 proposed such tags before the spec was committed" (`:193-194`) cannot be checked from lane records.** C05's scratch files date from 16:38:38–16:39:02 -0300, before 93d22aa, but when the report was delivered is not recorded.

## Verified claims (held at 01d586dd)

| Claim (entry line) | Check | Result |
|---|---|---|
| Pin rev, subject, last touch (`:19-20`) | `git log -1 0acb7752`; `git log -1 1770305 -- scripts/sources-check.mjs` | `round-34: fix SOURCES Markdown row parsing`; last touch `0acb775` |
| Blob `6b57424f…` at 0acb775 and HEAD 1770305 (`:20-21`) | `git rev-parse <rev>:scripts/sources-check.mjs` | `6b57424fc5a2…` at both (and at d933e15) |
| sha256 `6a293a72…258f`, 897 lines, 43,497 B, mode 100755 (`:21`, `:1`, `:3`) | `git show … \| sha256sum`; `wc -lc`; `git ls-tree` | exact |
| 46/46, `VERDICT: PASS`, exit 0; stdout 6,274 B, sha `e0880a5a…` (`:23-24`, `:33`) | replay of the `suite.txt` string | exact; same stdout sha as `control.txt:6` |
| 8 runs, exit 0, empty stderr, one stdout hash; `controls_match` exit 0 (`:32-36`) | `control/repeat-hashes.json`, `run-*.exit`, `repeat-control.stdout:12`, `.exit` | true |
| Hazard canary unchanged (44 entries), TMPDIR clone clean, 46/46 (`:38-42`) | `hazard-*.json` | true |
| 93d22aa committer date `16:40:21-03:00`; committed files; spec sha `c8d24cb4…408c91` (`:2`, `:49-52`) | `git show --stat 93d22aa`; `sha256sum` | true (4 cited files plus census-start.txt) |
| Sweep 19:41:29Z after the commit; 68 s (`:2`, `:53`) | `sweep.txt:2,8` (context commit 93d22aa) | true |
| Ten `@old` anchors, count=1 at :293/:114/:492/:483/:434/:182/:247/:251/:368/:356; unindented S_KIND count 5 (`:55-60`) | Python exact count on the pin | exact |
| Composition 5/5; each prediction names a case and a reason (`:62-65`) | `predictions.json` | true |
| Q1 verbatim, 19 words (`:79-80`) | arXiv abstract item (3) | true (but see M4 on the ID) |
| Runner `fb6d86d5…` = base runner (`:84-86`) | `git show 93d22aa:tools/mutate-and-run.sh \| sha256sum` | equal (also at 183f87b) |
| CONTROL GREEN, `MUTATE_RESTORE: OK`, `SWEEP_TARGET_RECHECK: PASS`, inconclusive 0 (`:86-89`) | `sweep.txt:11,110,112,116` | true |
| Result table: all ids, edits, lines, predicted, measured, exits, tallies (`:92-103`) | `sweep.txt:20-109,118-131` and my replay | exact; my replay reproduces every tally |
| `MUTATE_EVIDENCE` is in /tmp (`:113-115`) | `sweep.txt:111` | true |
| :356/:357 zero-statement lines; S19 §2 quote; check 32 (`:124-140`) | `w1/S19CaseOwnerRecon.md:57,75` | true |
| `FINDING_KINDS` read in exactly 3 places, :108/:130/:784 (`:130-131`) | grep on the pin | true |
| READ_FAILED fixture fails at `readdirSync` (`:142-144`) | pin `:344-349`, `:539` (`knowledgeIsFile`), `:790` | true; the entry's "not re-verified" hedge can be dropped |
| PENDING on all five survivors (`:150-163`) | read | true (I2) |
| Table string = runner `:620`; spec embed `:1015`; case `:1349-1352`; tuple `:1879`; suite byte-identical to `suite.txt` (`:167-176`) | Python compare of the runner and the files | exact; embedded spec sha `c8d24cb4…` |
| `git grep js-sources-check -- tools` empty at 183f87b and 93d22aa (`:174-175`) | `git grep -c` | empty (10 hits from 58e5d53 on) |
| L1 receipt lines (`:177-181`) | `leg8-L1-check.txt:12,14,15,17` | quoted correctly (see L3) |
| tameshi `PROVINCE.md:7-11`; kumitate `PROVINCE.md:15`, `SKILL.md:605`, `:629-630`, `LOG.md:1496-1498` (`:8-15`, `:160`, `:197`) | `sed` at the read rev and on kumitate at three revs | true (see L7 on qualification) |
| `sources-check.mjs:23-36` header map (W03 :23, W02 :25, overdue :31/:35) (`:212-214`) | pin read | true |
| Case 7 cross-refs: mkdtemp variance; §6 bwrap (`:35`, `:204-206`) | `mutation-case-kumitate-round-gate.md:29,145` | true |
| SKILL.md eighth case and PROVINCE round-18 append numbers (5/10, 10/10, pin, mode, `cases=8 passed=8`, lines 7-11) | `SKILL.md:1905-1915`, `PROVINCE.md:73-83` | consistent with the entry and with my run |

## Residual risk and verification gaps

- L3, L6 and I5 rest on `/tmp` mtimes and paths ([INFERENCE]). Files could have been changed or deleted without trace.
- I did not re-run X10's hazard or strace probes, or C05's fleet/kagi fixtures. Their summaries were checked only against their own JSON and log files.
- There is no `lsp` device in this inventory, and the entry is markdown. Code claims rest on direct reads of the pinned blob and on execution, never on grep alone.
- The kumitate gate run on the tameshi clone is a probe, not tameshi's gate. Its USED_BY_ASYMMETRY output supports M4 and M5 only together with the contract text.
- Scratch receipts stay in `/tmp/tameshi-r18w2-ReviewCase8Entry-5ODMxT` and are not lane evidence:
  - `regression-01d586dd.txt` sha `1ac57fca…`
  - `work-full/summary.json` `1786b6c0…`
  - `work-noawk/summary.json` `09c28e65…`
  - `run-mutants.py` `1698d55c…`
  - `kumitate-sources-check-on-tameshi.txt` `66b61240…`

  If the L1 cites them, copy them in first (QUALITY 9).

Verdict: **partial.** Every measured case-8 fact reproduces at 01d586dd: 5/10 killed, 10/10 predictions, all pins, lines and timestamps, and the landed runner's `--regression` passes with `cases=8 passed=8`. Survivors are correctly marked PENDING. But the entry states false limits and counts (K_ROWS awk-only, 44/46, case-7 suite bytes), has a stale and wrong source header (S008 shown as queued, S066 pointing at the wrong row, no row for the target) and leaves used-by symmetry unmet.
