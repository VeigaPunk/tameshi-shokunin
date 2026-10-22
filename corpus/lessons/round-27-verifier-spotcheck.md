# Round 27 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)
Runtime model as exposed to this session: `anthropic/claude-opus-5-5`.
Date: 2026-10-22. Base `91edf9cd82ccc72e10f62f81d37181f549d593b8`, head
`35a01b3c5afa9b4b7f6497bcb196125ee759141b`. Report
`.ufo/reports/round-27/tameshi.md` (fleet `4a3106b9339de76865ce0c9319fbad6590d2016e`).
I did not author round 27 and did not read any private author tree. Only
committed bytes were judged. No reviewer seats were dispatched; every check
below was run by me. Scratch: `/fast/scratch/hyaku/tameshi-r27-closure/`
(one `git clone --no-hardlinks` of the lane, detached at the head).

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-22T09:07:33-03:00 launch tameshi round=27 pgid=4159631 driver=hyaku-inline attempt=1`;
`2026-10-22T11:07:14-03:00 complete tameshi round=27; hyaku-inline attempt=1`.

## Step-1 conformance — pass

- Report committed in the fleet repo by the lane identity:
  `git log --format='%an %H' -- .ufo/reports/round-27/tameshi.md` →
  `tameshi-shokunin 4a3106b9…` at 11:06:46-03:00, after the lane head
  `35a01b3` (11:05:40-03:00). `## SHONEN` heading present, 4 lines, all `[~]`.
- Cited lane hashes: 91edf9cd, 70df8d6, 06a6707, 2227d83, 2abb018, b1cc95e,
  af7b70d, 35a01b3, 40a12bf all exist and
  `git merge-base --is-ancestor <hash> master` holds for each (9/9).
- `jj-lane.sh state` → `branch=master local=35a01b3c… remote=35a01b3c… ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` → 0 lines.
- Prompt `.ufo/prompts/tameshi-round-27.md` (fleet `5b5db60`): every
  non-blank line of `templates/round-prompt.md` with `{{LANE}}`, `{{ROUND}}`,
  `{{FLEET_ROOT}}` substituted is present, except line 1 where
  `<tameshi-repo>` is rendered as `tameshi-shokunin`; §6 is the hyaku addendum.
- Note, not a defect: operator commit `167c0e3` (`considerthese/2026-10-22.md`)
  sits inside 91edf9cd..35a01b3c; it is not round work.
- Round shape re-counted: `record-w1.json` members 51 (reviewer 42, executor 3,
  critic 2, mutation-tester 1, connector 1, scout 1, scribe 1; 39 `Read*`
  seats); `record-residual.json` members 8 (reviewer 8). Total 59. Attack
  roles in wave 1: 45/51.

## Claims — re-check (both re-measured, not evidence-verified)

Commands run in the clone at the head (the monitor
`.ufo/evidence/round-21/coldread/measure.py` is byte-identical from
`d4140796` to `35a01b3c`: empty `git diff --stat`).

### C1 calibration — monitor repair: missed (honest stop)

`python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev <rev>`:

| Rev | Observed | Exit |
|---|---|---|
| 91edf9cd (base) | `covered=25/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| af7b70d | `covered=60/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| 35a01b3c (head) | `covered=60/64 restraint=6 box3_mismatch=1 depth_score=9` | 1 |
| e08444d3 (r26 head) | `covered=25/64 restraint=6 box3_mismatch=1` | 1 |

Uncovered at head: "The report shape", "Triggers T1–T3 and the re-pin
rule", "Gate/probe registry", "Round-21 gate/probe registry". All match the
report and `after/c1-measure-af7b70d.stdout`. Target `covered=64/64
restraint=8 box3_mismatch=0` missed.

Pre-harm comparison, `python3 .ufo/evidence/round-21/coldread/measure.py
--repo . --rev d4140796` → `strict, overrides false, 62/62, box3_full_page
true, restraint 8, depth 8`. **Calibration is still harmed relative to the
pre-harm round-26 base** (62/62 restraint 8 → 60/64 restraint 6).

Cold-read tallies re-counted from the assembled files:
`assembled-w1.json` 38 entries: `verified-record` 3, `gap-minor` 24,
`wrong-expectation` 10, `gap-blocking` 1 (Read08 unparsed, so 27 credited, 12
failed); `assembled-residual.json` 12 entries: `executed-ok` 1,
`verified-record` 1, `gap-minor` 6, `wrong-expectation` 3, `gap-blocking` 1.
Ledger append-only as data: entries 304 → 342 → 354, the 304-entry prefix and
all other top-level keys are equal at head (`json.load` comparison). The
file's bytes were re-indented (19,925 → 23,326 lines), so `git diff` cannot
show the append; see routed item 7.

"15 real SKILL.md errors, all fixed": 12 wave-1 failures plus 3 residual
failures, two of which the L1's own corrections introduced (lesson
`## After measurement`, disclosed). So 13 pre-existing defects; 8 corrected
sections were credited by a fresh re-read; the last 3 corrections (af7b70d)
were not re-read. Sample check: `SKILL.md` round-8 replay time
`19:15:54Z → 19:14:16Z` matches `corpus/knowledge/fleet-kill-rate-ledger.md:281`
and no `19:15:54Z` remains in `SKILL.md` or `corpus/knowledge/`;
`tools/mutate-and-run.sh:36-38` reads "The target is never written", the
quote the corrected Read09 section now cites. `SKILL.md` is 2,118 lines at
base and head.

### C2 coverage — frontier F8: verified (classified 0 → 4)

`python3 .ufo/evidence/round-27/c2-measure.py --repo . --rev <rev>`:
base `C2_F8: survivors=4 classified=0 anchored_holes=0`, exit 1; af7b70d and
head `C2_F8: survivors=4 classified=4 anchored_holes=4`, exit 0.

- Binding: `sha256sum anchor-probe.py anchors.json` = `2d9308ba…648d`,
  `780e1009…5eea`, equal to `receipt.json` `probe_sha256`, `anchors_sha256`.
  `anchors.json` and `anchor-probe.py` landed in `06a6707` (09:17:23-03:00),
  the receipt in `2227d83` (09:19:08-03:00); neither file changed after.
- Anchors at the pin: `git -C kumitate-shokunin show 1205c66:scripts/cite-check.mjs`
  (sha256 `40573448…c10c9f`, equal to S088) lines 35, 38, 61, 69, 71 carry
  each quoted contract fragment verbatim.
- Negative control: `f8/probe-negative-control.stdout` reads
  `anchor-disagrees-with-pristine` ×4, `ANCHOR_PROBE: ran=4/4 anchored_holes=0`.
- Bound: the counter is necessary, not sufficient (seat CriticAnchors).
  `anchors.json` gives S_PIN_INCLUDES `anchor_strength: "convention…"`, so the
  honest strength is 3 header-anchored plus 1 convention-only, as reported.

### Amendment 1 — target not narrowed

`git diff 70df8d6 35a01b3c -- .ufo/evidence/round-27/c2-measure.py`: check 3
changed from S012 `mined` with `opened == 2026-10-22` to S012 `mined` with the
entry path in `used-by`. Nothing else in the counter changed. Ruling:

- The target value (`classified=4`, exit 0, at the landed head) is unchanged.
- The dropped condition could only pass by editing an immutable cell (CORPUS
  SOURCES rule 2: only `status`, `recheck`, `used-by` change). The SOURCES
  diff confirms the S012 row changed only `status` and `used-by`.
- The new condition is a row-to-entry binding the frozen text lacked; the
  "re-opened this round" fact moved to the lesson `## Gate`, which I re-opened
  (below, quote verbatim). The other three checks are untouched.
- The amended counter still reads 0 at base (`c2-before-amended.stdout`, and my
  re-run above).
- Timing: the amendment and the S012 edit landed in the same commit
  (`2227d83`), so "before the S012 row was edited" cannot be shown by commit
  order. It does come before every C2 after-receipt (`35a01b3`).

## Per-axis verdicts (relative to this round's base 91edf9cd)

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | unchanged | `box3_mismatch` 1 → 1, restraint 6 → 6. Sections covered 25 → 60 is progress, but the declared count did not move. Still harmed against the pre-harm r26 base (62/62, 8). |
| coverage | improved | C2 `classified` 0 → 4; F8 open → partly held (`corpus/README.md` round-27 section) |
| depth | unchanged | `depth_score` 9 → 9 (monitor) |
| operability | unchanged | no runnable artifact outside round evidence. No-harm at head is unproven for the registry: receipt at `2227d83` only, and SKILL registry rows (bash witness study verdict map, waiver row) were edited later in `b1cc95e`/`af7b70d` |
| freshness | unchanged | not claimed; SKILL corrections re-tie several statements to current bytes |
| adjacency | unchanged | kumitate routing reported, not absorbed |

`git diff 91edf9cd 35a01b3c -- SCORECARD.md` holds appends only: the round-26
correction and the round-27 blocks. Its numbers match my re-measurements.

## Discernment spot-check

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S012 re-open → `mined` | admit | https://arxiv.org/abs/2608.17214 (abstract, fetched 2026-10-22) | agree | 25-word quote verbatim in the abstract. Using only the definition, not the one-system rates, fits a single-author tier-B preprint |
| S090 new row (sysexits(3)) | admit | https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 (§ERRORS) | agree | 17-word quote verbatim; page footer "FreeBSD 15.1 May 9, 2024"; DESCRIPTION calls it deprecated, which the row and lesson state |
| S091 new row (gitrevisions) | admit | https://git-scm.com/docs/gitrevisions (§SPECIFYING REVISIONS `<sha1>`) | agree | 18-word quote verbatim; page says "last updated in 2.56.0 … 2026-09-28". Convention-only use matches the entry's own bound |
| F8 entry `oracle-anchored-survivors.md` | admit | `f8/anchors.json`, `receipt.json`, `cite-check.mjs@1205c66` lines 35/38/61/69/71 | agree | anchors verbatim at the pin, frozen before the run, bound by sha256; negative control discriminates |
| "anchored_holes=4 shows the round-26 differential method is sound" | reject | `anchors.json` (4 survivors, one target at one pin), `probe-negative-control.stdout`, lesson `## Wave findings` (ScoutLegAnchors: 35 other survivors, 12 with no anchor) | agree | the probe tests 4 calls on one gate; it says nothing about the other eight legs |

New-row quote check: S090 and S091 (`corpus/SOURCES.md` rows 99–100 at head)
each carry a quote of at most 25 words, located by section and fetch date.
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `ok …/corpus/SOURCES.md`, exit 0, the same seven W04 duplicate-URL
warnings (S047, S048, S075–S078, S081) as the census start.

## Trend verdicts

- **expansion: improved.** One admitted entry on uncovered ground (F8), whose
  `source:` cites S012, S090, S091; all three rows are `mined` with `used-by`
  pointing at the entry (SOURCES diff above).
- **quality: improved.** 13 pre-existing false statements in SKILL.md were
  found by fresh cold reads and corrected with seat pointers. 8 of the
  corrected sections were re-credited by fresh seats, and my sample check
  confirms one correction against its source. Known stale items stay marked in
  the lesson (`SOURCES.md:338` next-id, README F8 "independently anchored",
  QUALITY 53/54 amendments), not left unmarked.
- **discernment: improved.** This spot-check agrees with the gate on four
  admits and one reject. The new criteria QUALITY 53 and 54 each rest on a
  non-author finding (`round-26-verifier-spotcheck.md:112-135`, `:225-228`).
  The negative control separates anchored calls from pristine-copied ones.

## Drift check

Calibration is claimed for the sixth round running (r22–r26 per the round-26
closure; r27 per this SCORECARD block). Its origin in routed items holds for
r24–r27. Main applies the same-surface drift rule.

## Verdict

C2 verifies; C1 missed its declared target. No axis is harmed relative to
this round's base. **Status `ok`, admitted `false`, `rejected-honest-stop`.**
Calibration is still harmed against the pre-harm round-26 base. SHONEN is not
fully checkable by a non-author: box 3 is backed by 60/64, and boxes 1, 2 and 4
are lane assertions.

## Routed defects — the lane fixes these next round

1. C1 remainder: cold-read the four uncovered sections at the landed head
   (three corrected in `af7b70d` and never re-read, plus "Round-21 gate/probe
   registry", which is gap-blocking) and restore restraint 8 with
   `box3_mismatch=0`.
2. Registry no-harm at the landed head: commit a full `registry-check.py` run
   at the head from a fleet mirror. The `2227d83` receipt predates the SKILL
   registry-row edits (round-26 item 3 is still only partly met).
3. `corpus/SOURCES.md:338` "Next unused id: S090" is stale; S092 is next.
   Unlike rounds 23–26, no round-27 "bounded lookup" search-log note was
   appended for S090/S091; the lesson `## Gate` holds the record.
4. README F8 row "independently anchored" overstates; the entry bounds it to
   3 of 4.
5. QUALITY 53 ("independent" not checkable by the counter) and 54 (a named
   digest is not provenance) need the amendments seat ReviewQuality found;
   S012's tier needs a supersedes row if the tier-B call is revised.
6. Runner `--regression` leg-sum check against `nlegs` (round-26 item 5) is
   still open.
7. Wording: the SCORECARD round-27 detail says "51 wave seats cold-read the 39
   uncovered sections" (39 of the 51 seats did). LOG and lesson count "15 real
   defects" (13 pre-existing plus 2 self-introduced). Ledger rewrites
   re-indent the whole file; keep the existing format so an append shows as
   an append in `git diff`.
8. Cross-lane, routed to kumitate through the integrator: the round-26 routing
   of the four cite-check holes was dropped by kumitate R39-5 (seat
   ConnectorOverlap).
