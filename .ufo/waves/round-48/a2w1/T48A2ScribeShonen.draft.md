# T48A2ScribeShonen — draft: report `## SHONEN` section + trend-verdict evidence

Seat T48A2ScribeShonen (a2w1, scribe, axis calibration). Read-only on the lane; this file and
three receipts under `.ufo/waves/round-48/a2w1/` are the only writes. Observed at content
revision `c7586b9a10effc63b4bd327f976edc094c1bdc17` (lane HEAD at read time `17cc5ce`; the
four record files this draft reads are identical at both — `git diff --stat c7586b9 ..HEAD --
SCORECARD.md corpus/QUALITY.md corpus/lessons/round-48.md corpus/SOURCES.md` is empty).
Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ScribeShonen` removed before yield. No tool
installs.

Provenance of the numbers below, marked per bullet:

- **[O]** observed by this seat, with the command shown.
- **[R]** read from a committed receipt or record inside the lane (path:line given).
- **[W]** read from an untracked wave report under `.ufo/waves/round-48/` (a peer seat's
  working-tree artifact, not committed at `c7586b9a`).

My own coldread runs, kept as receipts beside this draft:

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev c7586b9a10effc63b4bd327f976edc094c1bdc17        # -> T48A2ScribeShonen.coldread-rev.json
$ ... --rev 15b1521ea2e95d0d708059458c090e9f334adf32      # -> T48A2ScribeShonen.coldread-15b1521.json
SCORE=6 DEPTH=9 COVERED=57/64 BOX3_FULL_PAGE=False LEDGER_PRESENT=True   (both revisions)
SHONEN marks=~~~~ asserted=4 checked=0 untouched=0 box3_marked=True box3_ledger_link=True box3_points=False
SOURCES rows=128 malformed=0
```

`sha256(.coldread-rev.json)` = `17e55ca072298ad58f062d7071f204c9fd5e9f25e9d7a5496f67c947d3e45a59`,
the same digest the a2w1 executor recorded for its own run at the same revision
(`.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeA.md:137`, **[W]** — an independent reproduction,
same bytes).

---

## SHONEN (draft text for the report)

Checklist `SHONEN.md` at `c7586b9a` (765 B, 4 boxes, lines 5-12; unchanged over
`473336d9..c7586b9a` — `git diff --stat 473336d9 c7586b9a -- SHONEN.md` empty, **[O]**).
Each pointer was opened at the same revision with `git show c7586b9a:<path>` /
`git cat-file -e`. No named non-author verifier exists in round 48, so no box can be `[x]`;
no box is untouched, so none is `[ ]`.

- `[~]` box 1 — "SKILL.md contains real decision tables, error patterns, checklists, cited
  sources" (`SHONEN.md:5-6`). Pointer `reports/round-1-calibration.md#box-1` **resolves**:
  file 26 651 B at `c7586b9a`, anchor `## box-1` at `:71` (the section runs to `## box-2` at
  `:105`), 33 lines of body. Lane assertion
  only — no independent promotion verifier (`reports/round-1-calibration.md:100-103`). No
  round-48 change bears on it: `SKILL.md` is untouched at the content revision
  (`git diff --stat 473336d9 c7586b9a -- SKILL.md` empty, **[O]**); round-48's prose landed in
  `corpus/QUALITY.md` and the lesson, not in SKILL.md.
- `[~]` box 2 — "At least one end-to-end domain task executed and logged in LOG.md"
  (`SHONEN.md:7-8`). Pointer `reports/round-1-calibration.md#box-2` **resolves**: anchor
  `## box-2` at `:105`. Round-48 bearing: `LOG.md` carries both round-48 entries — attempt 1 at
  `LOG.md:2348` and the attempt-2 correction at `LOG.md:2359` (**[R]**) — so the "logged in
  LOG.md" half is satisfied at the revision; the pointer still asserts the lane's own round-3
  execution trail, unverified by a non-author.
- `[~]` box 3 — "Instructions executable by an agent without oral context" (`SHONEN.md:9-10`).
  Pointer `.ufo/evidence/round-21/coldread/ledger.json` **resolves**: present at `c7586b9a`,
  3 489 570 B (`git cat-file -e` + `-s`, **[O]**). The monitor state at that revision, from my
  own run: `box3_full_page=false`, `sections_covered=57/64`, `shonen.box3_marked=true`,
  `shonen.box3_ledger_link=true`, `shonen.box3_points=false` → box 3 earns none of its two
  points, `calibration_restraint_score=6` (**[O]**, `T48A2ScribeShonen.coldread-rev.stdout`).
  Round-48 bearing is adverse: the committed base receipt says 60 credited
  (`.ufo/evidence/round-48/before/coldread-sections-at-base.stdout` → `COLDREAD_SECTIONS_CREDITED=60`,
  **[R]**), so the round-48 record edits cost three credited sections; the seven uncovered
  headings include `## Mutation-sweep recipe`, `## Restore discipline` and `### The map`
  (**[O]**, same receipt). State cannot rise to `[x]` (no non-author verifier) and must not
  drop to `[ ]` (the pointer resolves and the box is marked).
- `[~]` box 4 — "No cross-domain bleed (PROVINCE.md still accurate)" (`SHONEN.md:11-12`).
  Pointer `reports/round-1-calibration.md#box-4` **resolves**: anchor `## box-4` at `:176`.
  Round-48 bearing: `PROVINCE.md` is untouched at the content revision (6 334 B, empty diff vs
  base, **[O]**), and the round's four re-anchored documents (Google Testing Blog, PIT docs,
  bwrap `bwrap.xml`, TF `golden_tests?hl=zh-cn`) are published docs, not sibling-owned ground;
  the round **rejected** the staged package copies of the same documents rather than absorbing
  them (`corpus/lessons/round-48.md:91-96`, **[R]**), which is the PROVINCE "report, don't
  absorb" rule working. Unverified by a non-author.

Closing line for the section: `[x]`: none — no named non-author verifier exists in round 48
(`corpus/lessons/round-48.md:16-19`: "The non-author spot-check is the closure's"; LEARNING.md
counts a lane-dispatched seat as the lane). `[ ]`: none.

### Pointer-resolution table (what was opened)

| box | pointer as written | resolution at `c7586b9a` |
|---|---|---|
| 1 | `reports/round-1-calibration.md#box-1` | present, anchor `:71` |
| 2 | `reports/round-1-calibration.md#box-2` | present, anchor `:105` |
| 3 | `.ufo/evidence/round-21/coldread/ledger.json` | present, 3 489 570 B |
| 4 | `reports/round-1-calibration.md#box-4` | present, anchor `:176` |

Findings from that check (for the L1, not edits to SHONEN.md, which is outside this seat's
bounds):

1. All four pointers resolve; no box's state is contradicted by reason of a dead pointer.
2. Box 3's pointer resolves but its *credit* does not follow from it: the monitor reads the
   ledger's coverage and prints `box3_full_page=false`; the SHONEN line's own parenthetical
   already says "input-keyed monitor only", which is accurate.
3. Box 3's evidence base is weaker at `c7586b9a` than at base (57 vs 60 credited sections),
   which is a property of the round's own record edits, not of the pointer.

---

## Trend-verdict evidence (the L1 chooses the verdicts; one each per LEARNING.md)

Verdict vocabulary and the three trend definitions are
`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md` §"The three trends".
No verdict is proposed here.

### expansion

Observable: "net new admitted entries on uncovered ground, each citing its coverage-map row;
frontier areas entered; new kinds of source; a capability admitted to `SCORECARD.md`."

Supporting:

- Four new mined registry rows, each `supersedes T —` in its teaches cell:
  `S265`/S026, `S266`/S048, `S267`/S093, `S268`/S108 at `corpus/SOURCES.md:140-143` (**[R]**);
  registry rows 124 → 128 (`git show 473336d9:corpus/SOURCES.md | grep -c '^| S[0-9]'` = 124,
  same at `c7586b9a` = 128, **[O]**).
- Four entries now cite this round's rows in `source:` on line 1
  (`corpus/knowledge/{repeated-control-precondition,incremental-pin-disposition,regression-tally-completeness,r8-golden-update-flag}.md`,
  **[O]**) — i.e. every new row is *used*, none is registry-only.
- Weak supporting item: `S268` opens the zh-cn localized page, a page variant the lane held
  only in English (`S107`); the lesson scopes it as tier B wording support and keeps `S107`
  the tier-A statement (`corpus/lessons/round-48.md:71-89`, **[R]**). Read as a new *surface
  of an old document*, not new ground.

Contrary:

- No new `knowledge/` entry was admitted: `git diff --name-status 473336d9 c7586b9a --
  corpus/knowledge/` → four `M`, zero `A` (**[O]**); the directory holds 58 entries at both
  revisions. LEARNING.md's expansion unit is the *admitted entry*, not the row.
- All four rows supersede held documents (the teaches cells read "supersedes X's anchor and
  quote only", `corpus/SOURCES.md:140-143`), so no frontier area was entered and no
  coverage-map row was added: `corpus/README.md` is unchanged over `473336d9..c7586b9a`
  (**[O]**).
- No capability admitted: `SCORECARD.md:2365` — "Capabilities: none claimed this round (the two
  counters are claim instruments, not lane capabilities)" (**[R]**).
- The round's own least reachable expansion artifact, the package (`merge/tameshi`), was
  rejected wholesale on dedupe (`corpus/lessons/round-48.md:91-96`, **[R]**).

### quality

Observable: "entries re-verified, deepened, or superseded by stronger ones; `verified-at`
freshness"; `improved` when "a weaker entry is superseded by a stronger one, or stale entries
re-verify, with no admitted entry failing its re-check"; `harmed` when "an entry is found false
or stale and left unmarked".

Supporting:

- Four entries re-verified at `2026-10-26` with located quotes, and each re-anchor is narrower
  than what it replaces: S266 supplies the consequent round-45's non-author dispute said the
  old quote dropped (`corpus/lessons/round-48.md:26-42`, **[R]**); S267 reaches the sixth
  `--unshare-all` flag with its try-else-skip wording, which answers round-45's `CritJudge03`
  dispute (`:44-69`, **[R]**); S265/S268 carry located offsets and byte counts.
- Four `QUALITY.md` criteria appended, each citing a round-48 lesson line: 94
  (`corpus/QUALITY.md:1382`), 95 (`:1400`), 96 (`:1420`), 97 (`:1428`) (**[O]**); 94-96 are
  grounded in the round's own refusals and mistakes.
- One falsifier of the new block is red on a fixture and green on a repaired form with a
  committed receipt: `.ufo/evidence/round-48/quality/pointer-check-red-15b1521.stdout` (two
  `MISSING`, exit 1) and `pointer-check-selftest.stdout` (4 cases, 0 failed) (**[R]**).

Contrary:

- Criteria 94 and 95 cite falsifier receipts that exist at **no committed revision**:
  `git cat-file -e c7586b9a:.ufo/evidence/round-48/quality/c94-96-falsifiers.stdout` → absent;
  `git cat-file -e c7586b9a:.ufo/evidence/round-48/control/c1-controls.stdout` → absent; both
  also absent at the current tip `17cc5ce` (**[O]**). Criterion 96 names no committed receipt
  at all (`corpus/QUALITY.md:1420-1426`, **[R]**). This is the block failing the round's own
  criterion 97, and the committed red receipt is the proof it is still live at the landing
  revision — the same "receipt cited before it existed" defect the round records as a mistake
  (`corpus/lessons/round-48.md:356-360`, **[R]**).
- The calibration standing row restates an unread figure that the monitor contradicts:
  `SCORECARD.md:2355` says "60 of 64 sections credited"; the monitor prints 57/64 at the
  revision the row was emitted from (`15b1521`) **and** at the content revision (**[O]**).
  The C1 counter cannot see it — `pick_line` for a `monitor` statement returns only
  `str(json.loads(out)['calibration_restraint_score'])`
  (`.ufo/evidence/round-48/calibration/measure.py:261-265`, **[R]**) — so an `runs 3 stable`
  row carries a stale sub-measure that no counted surface rejects.
- A live re-fetch of S026 is **not** byte-identical to the snapshot (97 differing bytes, all
  rotating Blogger tokens; the quote is still located): `.ufo/waves/round-48/a2w1/T48W2ScoutSpotcheck.md`
  §Spot-check 1 (**[W]**). The lesson discloses this for S108 (seven live fetches, seven
  digests, two text variants — `corpus/lessons/round-48.md:372-376`, **[R]**) but not for S026.
- The round's record edits themselves cost cold-read credit: 60 → 57 credited sections
  (**[O]**, my two receipts plus the committed base receipt). The same class is noted for the
  round-47 `PROVINCE.md` append in `.ufo/evidence/round-47/quality/round46-lesson-dash-restored.md:127`
  (60 → 55 credited, score 6 unchanged),
  quoted by the a2w1 executor's probe (`.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeA.md:74`, **[W]**).

### discernment

Observable: "gate decisions vs the outside spot-check; `QUALITY.md` criteria"; `improved` when
"the spot-check agrees with the gate on admits *and* rejects, or a disagreement becomes a
lesson that adds a grounded `QUALITY.md` criterion".

Supporting:

- Two `### Reject` blocks, each with a decisive cite and a checkable `Flip:`: staged copies of
  the four documents refused on the dedupe rule (`corpus/lessons/round-48.md:91-96`, **[R]**);
  `r8-predictive-test-selection-cost.md` refused on **QUALITY 10** with the withdrawn weaker
  `PROVINCE.md:14-18` cite named (`:98-104`, **[R]**).
- A disagreement *did* become a grounded criterion: the round-47 closure's routed defect 4
  (wrong decisive cite) is corrected in an appended erratum (`:207-284`, **[R]**) and QUALITY
  94 is written from it, with the lesson cite on the criterion (`corpus/QUALITY.md:1382-1397`).
- The Gate's four quotes carry the required phrases and the ≤25-word bound
  (`corpus/lessons/round-48.md:21-24`; S267 is exactly 25 tokens, **[R]**) — the gate is
  checkable from the record alone, which is the precondition for an outside spot-check.

Contrary:

- No outside spot-check exists for round 48. The lesson says so in terms — "The non-author
  spot-check is the closure's (LEARNING.md: a seat this lane dispatched is still the lane)"
  (`corpus/lessons/round-48.md:16-19`, **[R]**) — so the trend's own observable ("the
  spot-check agrees with the gate on admits *and* rejects") is **unmet in-round**.
- The a2w1 spot-check is a lane seat and its verdicts are agree-with-caveat, not clean
  agreements: `AGREE (admit)` for S266, `AGREE` with the note that a byte-identical live
  re-fetch of S026 is unavailable, `AGREE (reject), narrowly` for the package entry that
  explicitly says the rejection is about provenance, not content
  (`T48W2ScoutSpotcheck.md` §Spot-check 1-2, **[W]**).
- Criterion 94's own falsifier is form-only and its bad fixture synthetic, and the historical
  refusal it was written from is outside the checker's domain — `reject_check` scans
  `### Reject` blocks only (`T48W2RevQuality.md` F4, **[W]**); and the receipt that criterion
  94 names does not exist at any revision (**[O]**, above). A criterion whose falsifier cannot
  replay the case it cites leaves the disagreement learned in prose only.

---

## Limits of this draft

- No counter was run: this seat ran the round-21 coldread monitor twice (read-only, into
  scratch) and read committed/working-tree receipts for everything else. `C1_R48_PASS` and
  `C2_R48_PASS` are not addressed here; the deciding run and its receipts are the L1's.
- The trend bullets cite `.ufo/waves/round-48/a2w1/*.md` as **[W]**: those reports are
  uncommitted working-tree artifacts at `c7586b9a`, so a closure judge must treat them as
  lane-seat evidence, not committed records.
- SHONEN.md was not edited (out of this seat's bounds); the section above is draft text.
