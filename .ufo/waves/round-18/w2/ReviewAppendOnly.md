# ReviewAppendOnly — round 18, wave 2 (falsify)

Scope: append-only mechanics, base `183f87b899e6cae46be98d251cbc87fb5118f6ca` → read rev
`01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, plus the R17-KNOW-EXIT erratum's exit claims.
Clone: `/tmp/tameshi-r18w2-ReviewAppendOnly-XesSNk/fleet/tameshi-shokunin` (detached at
01d586dd; sibling lanes symlinked). Every git command ran with `env -u GIT_DIR -u GIT_WORK_TREE
-u GIT_INDEX_FILE -u GIT_COMMON_DIR`. measure.py runs used bwrap (fleet read-only, `--unshare-net`,
`env -i`, `GIT_CONFIG_GLOBAL=/dev/null`). The only write in the lane is this report. No tools
were installed or upgraded.

## Findings by severity

### Medium — M1: the SOURCES footer update deletes a line, against QUALITY 35 from the same commit

- `git diff --unified=0 183f87b 01d586dd -- corpus/SOURCES.md`, hunk `@@ -195 +207,2 @@`:
  `-- Next unused id: S065.` → `+- S065–S074: round-18 rows (…)` and `+- Next unused id: S075.`
  (T:207-208). Base line 195 is deleted.
- `corpus/QUALITY.md:262-265` (T; criterion 35, added in 58e5d53) says: "…and a SOURCES footer
  update is a literal append: it deletes no line." `QUALITY.md:273-274` lists "a SOURCES footer
  edit that was not a pure append" as a defect the criterion captures.
- `corpus/lessons/round-17-verifier-spotcheck.md:449` (R17 §7 item 7) routed this defect: "The
  SOURCES footer update is not a literal pure append."
- The staged lesson draft admits the break: `.ufo/waves/round-18/staged/lesson-round-18-gate.md:80-84`
  says "Footer (`## Id allocation`), not a pure append … The closure noted footer edits are not
  pure appends; this is the one."
- History: `git log -p 01d586dd -- corpus/SOURCES.md` shows the same pointer-line replacement in
  4acc607, 0c6e36d, 4d409d7, 0494c24, c699c8c, 2a22ade and 58e5d53.
- Impact: no bytes are lost, since git keeps the old line and T:207 restates S065. The problem is
  that criterion 35 fails on the commit that lands it, and the footer clause of R17 §7 item 7 is
  still open at the read rev. The L1 must reconcile the two: either append the pointer without
  deleting the old one, or give criterion 35 an explicit, dated pointer-line exception.

### Low — L1: the SOURCES old→new log is not in the tree at the read rev

- SOURCES-CONTRACT-v1.md:49-50 (fleet `.ufo/waves/kaika/`) says: "Only `status`, `recheck` and
  `used-by` change in place, and each change is logged old→new in the round lesson."
- `git cat-file -e 01d586dd:corpus/lessons/round-18.md` → exit 128 ("does not exist"). The S008
  old→new is recorded only in the staged draft (`staged/lesson-round-18-gate.md:42-44`). Rule 1's
  `## Gate` lines for S065–S074 are also only in that draft.
- `corpus/README.md:265` (T) already cites `lessons/round-18.md`, so that citation is dangling at
  the read rev.
- This is expected to close when the L1 lands the round lesson after this wave. Until then it is
  open.

### Low — L2: the S060/S061 correction does not use the contract's correction mechanism

- `corpus/SOURCES.md:85` (T) is a dated prose note under `## Registry`: "round-18 registry
  correction: S060 anchor and S061 paragraph (rows not edited)".
- SOURCES-CONTRACT-v1.md:50-51 says: "A correction is a new row whose `teaches` opens `supersedes
  S0NN —`." The Shape at :11-17 has no slot for notes in the Registry.
- The lane's precedent is rows: S047 corrects S041 and S048 clarifies S047 (T:200-201).
- At base there was no note between the table and `## Paths` (base:73 S064, :74 blank, :75
  `## Paths`).
- No bytes were lost: S060 and S061 are unedited, and line 19 is the only existing line changed
  in place.

### Low — L3: the entry S008 now points to is stale about S008, and the other used-by updates were not made

- `corpus/knowledge/mutation-case-kumitate-sources-check.md:1` (T) says S008 is "(paper, tier A,
  **queued** — … not yet a mined row)", and :215-216 says "S008 is `queued` with `used-by —`".
  `SOURCES.md:19` (T) has S008 `mined` with used-by set to that same entry.
- The same entry, at :216-218, says S001, S052, S056 and S057 "need this entry added to used-by".
  At T that has not been done:
  - S001 used-by = `corpus/knowledge/mutation-score-semantics.md`
  - S052, S056, S057 used-by = `corpus/knowledge/mutation-case-kumitate-round-gate.md`
  
  The entry's `source:` header (:1) cites all four rows. Contract :40-41 defines used-by as the
  citing paths.
- The contract census passes ("missing used-by" printed nothing) because it checks only that
  paths exist, not that the list is complete.
- The entry is now landed, so under criterion 35 the :1/:215 fix has to be an appended erratum.

### Low — L4: the KNOW-EXIT erratum heading has no calendar date

- `input-keyed-coldread-credit.md:77` reads "## Errata — round 18 (R17-KNOW-EXIT, entry-local)".
  QUALITY.md:277-278 requires: "The named erratum must exist in the file under its own dated
  heading."
- Other blocks from the same commit carry `2026-10-20`, for example `operator-runbook.md:516`
  ER-jj2 and `lessons/round-17.md:98`.
- [INFERENCE] This passes if "round 18" counts as a date; criterion 35 does not say.

### Info

- **I1 — two wording nits in the erratum.**
  - :123-124 says the strict receipt "does not show the bucket at all". In fact the receipt lists
    the bucket's section (`start` 1563) three times — receipt lines 245, 615 and 713 — with reason
    `no-ledger`. What it lacks is only the bucket's credited/input-drift state.
  - :102 calls `measure.py:93-95` "usage text". Those lines are the module docstring; `measure.py
    --help` (rc 0) prints no exit split.
- **I2 — PROVINCE citation.** `PROVINCE.md:80-81` cites kumitate `PROVINCE.md:15` for the contract
  `kumitate-sources-v1`. Line 15 (same at 0acb775 and live) names `scripts/sources-check.mjs`
  but not the contract. The contract id is at kumitate `scripts/sources-check.mjs:4` and `:55`
  @0acb775.
- **I3 — staged draft line ranges.** `staged/lesson-round-18-gate.md:85-86` lists "Unchanged:
  lines 1–18, 20–73, and 75–194". That omits base:74 (the blank line before `## Paths`), which is
  also unchanged (now T:86).
- **I4 — calibration of criterion 35's check.** The `git diff --numstat` "zero deleted lines" check
  gives a false positive when the appended-to file has no final newline. In 2a22ade,
  `service-limits.md` and `verification-patterns-fleet.md` show numstat 3/1 each, yet the parent
  bytes are an exact prefix (only the EOF newline changed). All 11 bases at 183f87b end in `\n`,
  so numstat and the byte-prefix test agree in this wave. `cmp -n <base_size>` is the stronger
  test.
- **O1 — out of scope, routed to the L1 / ReviewSkillDiff.** `SHONEN.md` is 2+/3- in 58e5d53. It
  rewrites evidence lines 10-11 and 13 in place, deleting the round-17 appended "Correction
  (round 17, routed R16-C2c)" prose. QUALITY.md:262-266 lists "a SHONEN correction" among
  corrections that are appended and "never rewritten in place". R17 §7 item 7 (spot-check
  :450-451) asks for SHONEN's format to be resolved. [INFERENCE] The canonical single-line SHONEN
  format and criterion 35 pull against each other here.
- **Other files with deletions B..T** (not in scope; code and page edits): SKILL.md 39/10,
  tools/bash-witness-study.py 122/12, tools/evidence-disposition.py 345/23,
  tools/mutate-and-run.sh 102/28, tools/registry-check.py 625/31, tools/registry.json 141/4.
  192 files changed in total.

## Verified: the ten append-only files hold

Method: `cmp -s -n <base_bytes> base tip` on `git show REV:path` bytes, plus
`git diff --numstat 183f87b 01d586dd -- <f>`. Results:

- All ten bases end in `\n`.
- The appended bytes contain no CR characters, and every tip ends in `\n`.
- `git log --numstat 183f87b..01d586dd -- <11 files>` lists only commit 58e5d53. Of the five
  commits in the range, no intermediate commit rewrites and restores.
- The `.ufo/waves/round-18/staged/` copies are byte-identical to T for the 8 files that have one;
  README and PROVINCE have no staged copy.

| file | base→tip bytes | prefix | numstat add/del | base sha256 → tip sha256 | appended block |
|---|---|---|---|---|---|
| corpus/knowledge/fleet-kill-rate-ledger.md | 40058→40636 | yes | 2/0 | ac7f69d9… → 1c06c6ba… | ER-jj2 :422 |
| corpus/knowledge/incremental-pin-disposition.md | 27034→27612 | yes | 2/0 | 8ac942f5… → 0cc87300… | ER-jj2 :388 |
| corpus/knowledge/input-keyed-coldread-credit.md | 5076→8808 | yes | 72/0 | 1fad5a57… → 0c45dccb… | Errata :77 (base 75 lines, blob f5b961b6…) |
| corpus/knowledge/operator-runbook.md | 32249→33515 | yes | 2/0 | 531571cb… → 8b2e185f… | ER-jj2 :516 |
| corpus/knowledge/service-limits.md | 22311→22889 | yes | 2/0 | 2b2fd1ab… → 4fa8f039… | ER-jj2 :281 |
| corpus/knowledge/verification-patterns-fleet.md | 40254→40832 | yes | 2/0 | f49d1f1b… → 814f471a… | ER-jj2 :311 |
| corpus/lessons/round-17.md | 12705→15463 | yes | 10/0 | 21376ed9… → 8fd1d36d… | Correction :98 |
| corpus/QUALITY.md | 9866→18797 | yes | 128/0 | 94572f6a… → ffed5023… | Criteria 29-36 :169 |
| corpus/README.md | 30033→31214 | yes | 17/0 | 2f0fcb19… → cce90336… | Round 18 :258 |
| PROVINCE.md | 3749→4383 | yes | 12/0 | 49715af2… → 8006da5d… | Core append :73 |
| corpus/SOURCES.md | 43553→52074 | **no** (expected) | 15/2 | ac82b2df… → 1d4b5910… | enumerated below |

### Content checks on the appended blocks

- **ER-jj2 (5 files).**
  - The mechanism record holds: 2a22ade shows `operator-runbook.md` at 11/9. The deleted lines
    are the step-(3) `show HEAD:<path>` and `merge-base --is-ancestor <REV> HEAD` lines and the
    §6 rows `current`/`stale`/`drift`.
  - Live fleet `scripts/hyaku/jj-lane.sh` (sha256 3369dc27…, read live, not pinned): `usage()`
    is :50-63 (heredoc help :53-61, `exit 64` :62) and `err()` is :65. `detect_branch()` is
    :115-126: `symbolic-ref -q HEAD` → `refs/heads/*`, else `refs/remotes/origin/HEAD`. Both
    match the ER-jj2 text.
- **round-17.md correction (:98-108).**
  - `round-17.md:22` (G5, "89/89") and `:24` ("K02 hole 5") read as quoted.
  - measure.py anchors all check out: `OVERLAY_FIELDS` :134, selftest `overlay-field-forbidden`
    :1358, `cat_file_blob` :182-184, `commands-unrecorded` :517, `trace_reason` :368 (body ends
    :424).
  - Spot-check :306 reads `94/94 | d25d3d04`, and :327 gives G7 as hole 7.
  - `NoHarmSelftests.md:57` reads 89/89, with f348adc3 at :80.
  - K02InputCreditHoles.md: hole 5 (:28) is live-lane reads; hole 7 (:30) is page
    over-invalidation.
  - `measure.py --selftest` → rc 0, `MEASURE_SELFTEST: 94/94 pass`.
- **PROVINCE.**
  - `git -C kumitate show 0acb7752…:scripts/sources-check.mjs | sha256sum` → `6a293a72…258f`,
    as stated.
  - Lines 7-11 name the kumitate `scripts/*` primary surfaces.
  - Citation nit: see I2.
- **README.**
  - `.ufo/evidence/round-18/sources-check/control/repeat-hashes.json`: runs=8,
    all_exits_zero=true, distinct_stdout_sha256=1 ("8 byte-identical runs").
  - The `lessons/round-18.md` citation is dangling at T (L1).

## SOURCES.md, every change enumerated

`git diff --unified=0 183f87b 01d586dd -- corpus/SOURCES.md` has 3 hunks: 15 lines added, 2
deleted.

1. **`@@ -19 +19 @@` — S008 changed in place: one row, two cells** (cell-level diff, splitting
   on ` | `):
   - `status`: `queued` → `mined`
   - `used-by`: `—` → `corpus/knowledge/mutation-case-kumitate-sources-check.md`
   
   The other 9 cells are byte-identical. Both changed cells are in the contract's mutable set
   (SOURCES-CONTRACT-v1.md:49), so the edit is permitted. Counted as cells, "exactly one in-place
   S008 cell change" is **false (it is two)**; counted as rows it is true (one). The staged draft
   (:42-44) states two cells correctly.
2. **`@@ -73,0 +74,12 @@` — inserted after S064:**
   - T:74-83: ten rows, S065–S074
   - T:84: blank line
   - T:85: the dated S060/S061 correction note (L2)
   
   Base :74 (blank) and :75 (`## Paths`) carry over unchanged as T:86-87.
3. **`@@ -195 +207,2 @@` — footer:** base :195 `- Next unused id: S065.` is deleted. T:207
   (`- S065–S074: …` range line) and T:208 (`- Next unused id: S075.`) are added (M1).

Contract census at T (SOURCES-CONTRACT-v1.md:64-81 commands, run in the clone):

- rows 72 (base 62)
- malformed 0
- tiers A=63, B=7, C=2
- status mined=44, queued=23, rejected=5 (base 35/24/3, matching staged :88)
- duplicates: none
- enum violations: none
- missing used-by: none

New rows: every mined row's used-by is `corpus/knowledge/guard-kill-closure.md`; the rejected
rows S067 and S071 have `—`.

## KNOW-EXIT erratum: the exit claims hold

`measure.py` is the same blob at 183f87b and T (bc4c0c53…; sha256 d25d3d04…).
`git diff --stat 183f87b 01d586dd -- .ufo/evidence/round-17/` is empty, so the cited evidence is
retained. Probe results (script `/tmp/…/knowexit.sh` under bwrap):

| probe | argv | rc | key output |
|---|---|---|---|
| p1 default ledger absent | `--rev 98bea7d` (ledger.json absent at 98bea7d) | 0 | no-ledger 54/54; overrides_used false; trace_gate strict |
| p1 full rev | `--rev 98bea7da5801f4bc58e4187690ee1687c8a5061f` | 0 | stdout **byte-identical** to `redbefore/measure-98bea7d-strict.json` (sha256 5f7d13ff… both). This turns the erratum's "exit 0 follows" inference into an observation |
| p2 synthetic absent | `--repo /tmp/…/synth --rev 73fb87c0…` (183f87b with ledger.json removed, /tmp clone) | 0 | no-ledger 58/58 |
| p3 missing explicit ledger | `--rev 183f87b --ledger-file /tmp/…/no-such-dir/ledger.json` | 2 | `ledger-file-unreadable` |
| p4 / p5 | `--ledger-rev 000…1:…` / `--ledger-rev 183f87b:no/such/ledger.json` | 2 / 2 | `ledger-rev-missing` / `ledger-blob-missing` |
| p6 / p7 | `--rev 000…1` / `--rev 40f8e1f3…` (root commit) | 2 / 2 | `rev-missing` / `blob-missing` [tools/mutate-and-run.sh, corpus/SOURCES.md] |
| p8 / p9 | `--inputs-overlay` missing / with key `verdict` | 2 / 2 | `overlay-unreadable` / `overlay-field-forbidden` |
| p10 / p11 | no args / `--rev -x` | 64 / 64 | `UsageParser.error` → `SystemExit(64)` (:143-147) |
| p12 control | `--rev 183f87b` (default ledger present) | 0 | credited 58/58, box3 true, ledger_committed true |

`knowexit.sh` itself exited 1. That came from its trailing `[ -s p12.err ] && echo` on an empty
stderr file, not from a probe failure. Likewise, the selftest wrapper's exit 1 is a trailing
`grep -c` that counted 0 FAIL lines.

Line anchors in the erratum, all exact:

- `measure.py:535-553` (no-ledger branch :541-553, `return out` :553)
- `:1545-1547` (default ledger path)
- `:1520-1543` (explicit-ledger exits)
- `:1554-1592` (overlay exits)
- `:1598` (`return 0`)
- `:93-95` (docstring exit split)
- `:403-412` and `:368-380`

Other erratum claims:

- The only receipt-`argv` reference is the fixture at :773.
- `bucket-commands` has zero hits.
- `coldread/traces/CR01/1.json` argv is `bash -c 'git -C … show eb7838b…:SKILL.md | sha256sum'`.
- §2's four receipts match exactly: three overlay runs (`overrides_used` true,
  `inputs_overlay_merged` 1, `trace_gate` legacy), e69b488 credited, 09ee1d0 and 98bea7d
  `input-drift:tools/mutate-and-run.sh`, and the strict receipt has no `error` key.

## Residual risk and verification gaps

- I checked only the eleven assigned files plus a numstat scan of the whole range. The other 181
  changed files were not reviewed for append-only rules (O1 and the list above).
- `jj-lane.sh` was read live, not at a pinned fleet revision. ER-jj2 cites it by function name,
  which matches what I read.
- Not checked: the staged lesson's Gate quotes against the sources, the content of QUALITY
  criteria 29-34 and 36, and anything in the C1/C2 claims beyond these files.
- M1 and L1 depend on what the L1 lands after this wave: the round lesson, and either a footer
  erratum or a change to criterion 35.

Verdict: partial — all ten files are pure appends (exact byte prefix, 0 deleted lines, one commit) and the KNOW-EXIT erratum's exit claims hold (rc 0 for a missing default ledger, rc 2 for a missing `--ledger-file`), but SOURCES.md's S008 change is one row with two cells, and its footer update deletes a line, which contradicts QUALITY 35 landed in the same commit.
