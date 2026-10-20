# S14ShonenFormat — round 18 wave 1 — SHONEN.md canonical-form audit and replacement

Base rev: `183f87b899e6cae46be98d251cbc87fb5118f6ca` (branch master, lane worktree clean for
`SHONEN.md`). Current `SHONEN.md`: 13 lines, 1808 bytes, sha256
`6b7acb015cb72fde3642ed7c5b5d2fbfdc762fd2b0d32ccab13436830d2c7f80` (= `git show 183f87b:SHONEN.md`).

Axis framing: calibration (fixture craft / canonical form), operability no-harm. No file edited:
this report is the only write; the canonical replacement already staged by B17 is validated here,
with one optional trim.

## 1. Canonical shape and its mechanical rule

Sources, all read at their committed bytes:

- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:446` — file contract:
  "the seed block ... must diff byte-identical modulo `<name>` ..., and marks are confined to the
  box character plus one indented evidence line per box — `[x] <verifier-id>` or `[~]` with a
  resolvable pointer; no other prose, added boxes, or removed boxes".
- `PROTOCOL.md:453-462` — the verbatim 8-line seed (header, blank, intro, blank, four `- [ ]` boxes).
- `PROTOCOL.md:464-465` — `[~]` = lane-asserted, pointer required; `[x]` only with a named non-author
  verifier.
- `/home/vgpnk/Projects/kimi-shokunin/templates/mint/SHONEN.md:1-9` — wrapper HTML comment; it is
  metadata ("the block below"), not part of the seed. Canonical sibling files (`kagi`, `kake`,
  `chousa`, `kasegi`) do not carry it; its absence in tameshi is **not** a deviation.
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/SKILL.md:151-167` (`## Promotion gates`) —
  `[x] <verifier-id>` names its verifier; "The lane's own assessment is `[~]` with a resolvable
  pointer"; an `[x]` without a named non-author verifier counts as `[~]`.
- `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL-APPENDIX.md:30` —
  canonical-form incident class: "kotoba per-box prose" is a recorded variant defect.
- `corpus/lessons/round-17-verifier-spotcheck.md:450` (R17-CITATIONS, routed item 7) —
  "SHONEN's added correction prose also exceeds the canonical single-evidence-line format; resolve
  its format without treating this closure as promotion."

## 2. Observed current file (exact structure)

`awk '{printf "%d len=%d %s\n",NR,length,$0}' SHONEN.md` and `sed -n l SHONEN.md`:

| Line | Bytes | Role |
|---|---|---|
| 1 | 40 | `# tameshi-shokunin — Promotion checklist` — seed verbatim (name substituted) |
| 3 | 38 | `Promotion to shokunin requires all of:` — seed verbatim |
| 5, 7, 9, 12 | 87/71/62/56 | four box lines; byte-identical to the seed box text modulo `[ ]`→`[~]` (verified, 4/4) |
| 6, 8, 13 | 91/91/175 | one indented evidence line each: label + resolvable pointer |
| 10 | 503 | box-3 evidence line: narrative + three pointers |
| 11 | 570 | box-3 **second** indented line: `Correction (round 17, routed R16-C2c): ...` + two pointers |

Pointer resolution at base: `reports/round-1-calibration.md` is tracked; `## box-1` (:71), `## box-2`
(:105), `## box-4` (:167) each match exactly once (`grep -c '^## box-N$'` → 1/1/1). The round-16
ledger/measure/lesson and round-17 ledger targets are all tracked at base. No trailing whitespace
(`sed -n l` shows `$` immediately after content). Newline-terminated.

## 3. Deviations (every one found)

D1. **Two indented evidence lines under box 3** (SHONEN.md:10 and :11). Rule: one per box.
    — structural, unambiguous.

D2. **Correction prose inside the checklist** (SHONEN.md:11, 570 bytes): "Correction (round 17,
    routed R16-C2c): ... was wrong at 09ee1d0 on one bucket ...". Rule: "no other prose".
    — this is exactly the text R17-CITATIONS:450 routes to be resolved.

D3. **Multiple evidence pointers in the box-3 block**: five distinct paths across two lines —
    `.ufo/evidence/round-16/coldread/ledger.json` (link target at :10 and repeated in text),
    `.ufo/evidence/round-16/measure.py` (:10), `reports/round-1-kaika-coldread.md` (:10),
    `corpus/lessons/round-16-verifier-spotcheck.md` (:11),
    `.ufo/evidence/round-17/coldread/ledger.json` (:11, only inside the prose line).
    Rule: `[~]` with **a** resolvable pointer; the pointer should be the evidence the assertion is
    measured against.

D4. **Line 10 repeats an overclaim the lane's own closure falsified**: "round-16 cold-read of
    every SKILL.md bucket ... wrong expectations repaired and re-read". `corpus/lessons/
    round-16-verifier-spotcheck.md:95-123` (§2) records one stale bucket (`## Effective
    expectation reconciliation — round 14`), 53/54, closure score 6. Keeping the claim in the
    promotion checklist means the checklist itself carries a known-wrong assertion, only
    contradicted by the next line.

D5. **Label prose on the otherwise-conforming lines** (:6, :8, :13): "lane assertion, no independent
    promotion verifier" (and on :13 additionally "PROVINCE.md Core list corrected by append
    (tsukuroi and mado gates), fleet round 1"). Each is one indented line with a resolvable
    pointer, so it passes the line rule; it is redundant prose (`[~]` already means lane
    assertion, SKILL.md:163-165). Minor. The staged replacement keeps this label (see §5, residual).

D6. **Forward-counting defect (not visible at base)**: box 3's block contains no
    `.ufo/evidence/round-18/coldread/ledger.json`. The round-18 measure looks for exactly that
    string (:113 `DEFAULT_LEDGER_PATH`, :131 `BOX3_LINK`, :680
    `BOX3_LINK in boxes[2][1]`), so at the round-18 landing the current file yields
    `box3_ledger_link: false` and restraint 6 even with a full 58/58 ledger — proven in §6.

Checked and **not** deviations:

- Seed header/intro/box wording: byte-identical modulo name and mark (4/4 boxes verified).
- Box count = 4; no added/removed box.
- Template wrapper HTML comment absent: not part of the seed (PROTOCOL.md:453-462); siblings omit it.
- `SCORECARD.md:67` cites `SHONEN.md:5-34`: that row is pinned to `284ab0f`, whose SHONEN is a
  36-line file with four `[x]` at :5/:12/:19/:27; it is not a claim about the current 13-line body.
- No other lane tool parses SHONEN: `grep -rn SHONEN tools/ scripts/` → no matches.

## 4. Counting-constraint mechanics (why the rewrite must have this exact shape)

Command C (`SCORECARD.md:75`, the calibration mark census):

```sh
git show "$REV:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); ...'
```

- Counts **lines** matching `^- \[([x~ ])\] ` at column 0. Current body: `boxes=4 checked=0
  asserted=4 untouched=0 asserted_mark_upper_bound=8` (exit 0, run at 183f87b). Indented prose
  cannot inflate the box count; unindented prose that happens to start `- [~] ` would, so removed
  prose must not be reflowed to column 0.
- `asserted_mark_upper_bound=min(8, 2*asserted)`; four `[~]` → 8. Changing any mark to `[x]`
  without a named non-author verifier both overclaims (SKILL.md:164-165) and drops this bound
  (the formula counts only `~`). Keep exactly four `[~]`.
- The rubric's remaining 2 points need independent promotion review; no SHONEN edit can earn them.

Cold-read measure (`.ufo/evidence/round-17/measure.py:120, 251-269, 665-667`; round-18 copy at
`.ufo/evidence/round-18/measure.py:113, 131, 680`):

- `shonen_boxes()` builds each box's block as the box line plus the **immediately following**
  indented non-empty lines; a blank line or a non-indented line closes the block. The ledger path
  must therefore sit on the single indented line directly under box 3 (or on the box line).
- `box3_link = BOX3_LINK in boxes[2][1]` is a substring test, and `BOX3_LINK` is the **round's**
  default ledger path: round-17's program looks for
  `.ufo/evidence/round-17/coldread/ledger.json`; round-18's looks for
  `.ufo/evidence/round-18/coldread/ledger.json`. The round-18 contract's ignored inputs include
  both ledger paths, but the box-3 link string is only the round-18 path.
- `box3_points = box3_marked and box3_link and cr['box3_full_page']`. So 2 points need: `[~]` at
  position 3 **and** the round-18 path in its block **and** 58/58 ledger coverage at the measured
  SKILL.md. Boxes 1, 2, 4 contribute 2 each when `[~]`.
- Measurement is round-keyed: running the round-17 program at a round-18 rev necessarily returns 6
  (it searches for the round-17 string). That is not a regression; derive each round's score with
  its own program. Verified: round-17 measure at 183f87b → 8; round-17 measure on the fixture
  below → 6.

## 5. Proposed canonical SHONEN.md (validated; already staged by B17)

Path `.ufo/waves/round-18/staged/SHONEN.md`, 12 lines, 739 bytes, sha256
`de1b1d986087fe9299a32b927888668830a12b55f998477c7a834baa9b56e6e4`. It replaces box 3's two
lines with one pointer line and trims box 4's label; boxes 1-2 labels are unchanged.

```markdown
# tameshi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  [lane assertion, no independent promotion verifier](reports/round-1-calibration.md#box-1)
- [~] At least one end-to-end domain task executed and logged in LOG.md
  [lane assertion, no independent promotion verifier](reports/round-1-calibration.md#box-2)
- [~] Instructions executable by an agent without oral context
  [lane assertion, no independent promotion verifier](.ufo/evidence/round-18/coldread/ledger.json)
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  [lane assertion, no independent promotion verifier](reports/round-1-calibration.md#box-4)
```

Against the canonical shape: header/intro and all four box lines are seed-verbatim modulo mark;
exactly one indented evidence line per box; no correction prose; one pointer per box; box 3 points
at the round's own input-keyed ledger. Command C on this file: `boxes=4 checked=0 asserted=4
untouched=0 asserted_mark_upper_bound=8`.

Residual prose in the staged bytes (D5-class): the repeated label "lane assertion, no independent
promotion verifier" is redundant with the `[~]` mark and is the only remaining text on an evidence
line that is not a pointer. Under PROTOCOL.md:446's "no other prose", replace the four labels with:

```text
  [round-1 calibration, box-1](reports/round-1-calibration.md#box-1)
  [round-1 calibration, box-2](reports/round-1-calibration.md#box-2)
  [round-18 cold-read ledger](.ufo/evidence/round-18/coldread/ledger.json)
  [round-1 calibration, box-4](reports/round-1-calibration.md#box-4)
```

(Validated with the current round-18 program on a fixture: 646 bytes, 12 lines, sha256
`f36714bfe85cac57619a69e1d55eced9aecb128fef99fe71c9f5c3bb08e0cd4e` → `box3_ledger_link=true`,
`box3_points=true`, restraint 8, `coldread 58/58`, `box3_full_page=true`. Same counters as the
staged bytes; only the link labels differ.)

## 6. Mechanical validation

All runs read committed bytes (lane worktree never written). Fixture = fresh `git clone` of the lane
at 183f87b under `/tmp/tameshi-r18w1-S14ShonenFormat-vCHe6r/repo19`, `GIT_*` scrubbed via `env -u`;
commits made only in the fixture. Round-18 tool bytes measured:
`.ufo/evidence/round-18/measure.py` sha256
`7ffbcff6ef642ec662b233a90c606db68f0e6a7a41639a46b7d3b5aa8e00ee1f` (untracked new lane file at
base, `git cat-file -e` → 128; contract F builder owns it).

1. **Current file, round-17 program** (`python3 .ufo/evidence/round-17/measure.py --repo <lane>
   --rev 183f87b`, exit 0): `boxes=4`, `asserted=4`, `box3_ledger_link=true`,
   `box3_points=true`; `coldread 58/58`, `box3_full_page=true`;
   `calibration_restraint_score=8`. The present file satisfies the round-17 constant — the defect
   is form, plus the round-18 link string.

2. **Build-state note (transient, resolved)**: while wave 1 was writing contract F, the round-18
   measure at 16:38-16:40 crashed `NameError: name 'strict' is not defined` at `measure.py:675`
   (exit 1, base and fixture). The owner updated the file at 16:42:15 (76090 bytes) and it now
   exits 0; every result below is from those current bytes, no repair applied. Flagged only so a
   stale read during the wave is not mistaken for a permanent state.

3. **Real round-18 program at base 183f87b** (exit 0): `box3_ledger_link=false`,
   `box3_points=false`, `calibration_restraint_score=6`, `coldread 0/58`,
   `box3_full_page=false` (no round-18 ledger at base). Red-before for the round-18 landing.

4. **Real round-18 program on a fixture rev** (staged SHONEN + round-17 ledger copied to
   `.ufo/evidence/round-18/coldread/ledger.json`, committed in the fixture only): `box3_marked=true`,
   `box3_ledger_link=true`, `box3_points=true`, `calibration_restraint_score=8`, `coldread 58/58`,
   `box3_full_page=true`, `ledger_committed=true`.

5. **Same fixture, base SHONEN + the same ledger state** (round-17 ledger still committed at the
   round-18 path): `box3_ledger_link=false`, `box3_points=false`,
   `calibration_restraint_score=6`, `coldread 58/58`, `box3_full_page=true`. This isolates the two
   lost points to the box-3 link string, not to coverage.

6. **Round-keyed control**: round-17 program at base → 8; round-17 program at the fixture rev → 6
   (it searches for the round-17 path). Expected cross-round behavior, not a regression.

7. **Command C on staged bytes**: `boxes=4 checked=0 asserted=4 untouched=0
   asserted_mark_upper_bound=8` (exit 0). Command C at 183f87b on the current file: same tally.

8. **Staged vs canonical seed**: `diff` (template name-substituted, wrapper comment stripped) shows
   only the mark change and the four added evidence lines; the four-line prefix is identical.

9. **Pointers**: `reports/round-1-calibration.md` anchors exist (each `grep -c '^## box-N$'` = 1);
   `.ufo/evidence/round-18/coldread/ledger.json` is absent at base
   (`git cat-file -e 183f87b:<path>` → 128) and must land with the SHONEN commit.

## 7. Where the removed prose goes

- The correction's substance is already committed: `corpus/lessons/round-16-verifier-spotcheck.md`
  §2 (:95-123: stale bucket, `75ed934d…` → `0673d2e5…`, exit 2 vs recorded 1/0) and §6 item 4
  (:231, R16-C2c). `LOG.md:1072` already records "SHONEN box-3 correction appended".
- B17's staged plan appends the removed SHONEN bytes verbatim to `LOG.md` (append-only, no rewrite).
  Either that append or a one-line LOG pointer to lesson §2 satisfies "move to LOG/lesson"; the
  verbatim append is the safer preservation and does not affect command C (LOG is not parsed).
- Nothing else depends on the removed prose: no lane tool reads SHONEN (§3, non-deviations).

## 8. Landing constraints / residual unknowns

- Install staged `SHONEN.md` **in the same commit** as `.ufo/evidence/round-18/coldread/ledger.json`;
  a SHONEN-only commit would leave box 3's pointer unresolvable and the box-3 string pointing at a
  missing blob (promotion gate requires a resolvable pointer).
- The round-18 ledger must cover 58/58 sections of the SKILL.md at the measured rev. At 183f87b
  the carried round-17 ledger does (58/58). Wave-2/3 SKILL.md edits require fresh entries for the
  changed sections; otherwise `box3_full_page` false → 6 regardless of form.
- The round-18 `measure.py` is an in-flight contract-F file; the sha256 in §6 is the byte set that
  produced every number above (exit 0 at 16:42). Re-run the landed bytes at the landing rev before
  quoting the score — an edit changes the tool and the score is only as durable as that pin.
  The box-3 rule is contract-fixed (one string, block substring, 58/58 coverage), so the format
  conclusion is independent of tool churn.
- Unknown: whether wave 2's assemble run adds `carried_from` markers that alter any entry's
  verifiability; the copied-ledger fixture proves schema `tameshi-coldread-ledger-v2` entries are
  accepted, not that the final carried ledger passes every gate.

Verdict: **falls** — current `SHONEN.md` is non-canonical (box 3: two indented evidence lines,
570 bytes of correction prose, five evidence pointers; the evidence line also repeats the falsified
round-16 full-page claim) and its box-3 block lacks the round-18 ledger string, costing 2 calibration
points at the round-18 landing; the staged 12-line replacement is canonical, keeps four `[~]` lines,
and measures 8 with 58/58 coverage.
