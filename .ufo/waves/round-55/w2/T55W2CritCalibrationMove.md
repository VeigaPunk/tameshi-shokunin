# T55W2CritCalibrationMove — is C1 a real calibration move?

**Verdict: yes for the record, no for the counter's class claim.**

The ten corrections are tree-true: I re-derived nine of them with my own code (not the
counter's) and verified the tenth's external provenance directly, and the counter is red at
base / green at C0, so a do-nothing or transcription-only seat does **not** get the verdict.
But the counter does not "catch the same class again": six of ten rows have a hardcoded
empty stale arm, the corrections-exclusion zone runs to EOF, and eight plants of the *same
class* (a number the record asserts and the tree contradicts, with a plausible receipt named)
all read `C1_R55_PASS=true`. Under C1's frozen surface — the ten routed defects — the claim
is met; the generalisation the wave item asks about is falsified, with receipts below.

Impacted axis: **calibration (8)**. Nothing else moves. Premature-saturation check: the
frontier is not saturated by this claim, because the row-level arms are four-of-ten live.

## What I attacked

1. **C1's record vs the tree** — are the ten corrections actually derived, or plausible prose?
   (independent re-derivation, `verify.sh`)
2. **C1's counter vs a NEW defect of the same class** — plant one in a `git clone --shared`
   at C0 and see whether stale/derived structure fires. (`plants.sh`, `plants2.sh`, P12–P14)
3. **The record's own words about its counter** — the frozen amendments and
   `corpus/lessons/round-55.md` claim a predicate; does the implemented predicate match it?

Everything ran at `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` on clones of
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; no lane file was written or edited. Counter
bytes used were `.ufo/evidence/round-55/c1/measure.py` from the lane working tree, whose
sha256 is `5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e`, equal to the
freeze manifest entry (checked at HEAD too).

## Arm A — the record is calibrated (9/10 derived independently, 1/10 provenance-verified)

Command (receipt: `T55W2CritCalibrationMove-receipts/verify.stdout`, driver `verify.sh`):

```
bash .ufo/waves/round-55/w2/T55W2CritCalibrationMove-receipts/verify.sh \
     /home/vgpnk/Projects/shokunin/tameshi-shokunin 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
```

Output (trimmed to verdict-bearing lines):

```
R54.1  controls-b CTL_MISMATCH count / verdict        1 / CONTROLS_B: 2/3
R54.1  corrections state CTL_MISMATCH + 2/3           present,present
R54.2  frozen.stdout pointer(s)                       077d431e69965fa4673cd006ab64f6fc387f9e15
R54.3  receipt verdict token / total                  C2_R54_PASS=false / total=13
R54.4  sha256 of c2/measure.py at C0 vs freeze.json   8528ee85 vs 8528ee85 equal=yes
R54.5  recount w1/w2 findings, w2 non-empty sections  w1=28 w2=25 sections=12   (23+23 reader files)
R54.6  add-commit of swept seat file                  ff2a821
R54.7  rename-commit of forged reader                 7fa9a5e  (git log --follow)
R54.9  registry / receipt / live shokuknow            reviewers=5 attack=21/76 seats=76 / output=81 / live=81
R54.10 controls-a CTL_R53 line                        …rekeyed=0/7 …
```

Every value the corrections section states reproduces from the tree with expressions the
counter does not use (R54.4's digest is re-derived from the bytes at C0, not read out of
`freeze.json`; R54.5's counts come from a fresh traversal). R54.8's strongest claim — the
operator turn that the round-54 report called "fabricated" — verifies out of band, read-only:

```
$ python3 -c "…sqlite3 'file:/home/vgpnk/.omp/agent/history.db?mode=ro'…"
(690, 1793200335, '/home/vgpnk/Projects/shokunin', 'use m_glm53 instead of m_grok')
$ python3 -c "import datetime;print(datetime.datetime.utcfromtimestamp(1793200335).isoformat()+'Z')"
2026-10-28T15:12:15Z
$ grep -n scout /home/vgpnk/.omp/agent/config.yml
418:    scout: "@m_grok"
```

Row 690, the timestamp the correction names, and the `scout: "@m_grok"` value all hold. The
withdrawal of "fabricated" is therefore correct, not a softer restatement.

And the stale assertions really were removed in place (not merely quoted in the corrections
block) — at C0, outside the corrections block: `49280fe5`, `25 wave-1`, `22 wave-2`,
`total=14`, `84 staged`, `7883e0e5`, `fe70474d`, `CTL_POS_c1 true` → all absent; the
`rekeyed=7/7` occurrences that remain are the deciding-run verdict lines at
`c21081008adb`, which is what those receipts print.

Counter at base and at C0 (receipts `plants.stdout` P0, and the baseline run):

```
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
C1_R55: rev=9cf0146b94dd classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

The base line is byte-identical to the committed `before/c1.stdout`, so the do-nothing
control is genuinely refused, and `controls.sh`'s pre-registered `CTL_SKIP_c1` (paste every
corrected value, fix nothing) is refused for the right reason.

## Arm B — the counter does not generalise to the class

Plant matrix. Each row is an independent `git clone --shared` at C0, one committed edit, then
the frozen counter over it. "expected" is what the counter's own wording promises.

| # | plant | class | expected | observed (`C1_R55_PASS`) |
|---|-------|-------|----------|--------------------------|
| P0 | do nothing, at base `0a2010ac` | — | false | **false** (`total=10`) |
| P4b | exact R54.1 literal `CTL_POS_c1 true` put back before the corrections block | R54.1 | false | **false** (`stale=1`) |
| P9 | corrections section states `total=12` | R54.3 | false | **false** (`corrected=9/10`) |
| P8 | the receipt moves under the row (`total=13`→`15`), record untouched | R54.3 | false | **false** (`corrected=9/10`) |
| P10 | exact old digest `49280fe5` put back in SCORECARD | R54.4 | false | **true** ← stale arm is `[]` |
| P11 | exact old counts `25 wave-1; 22 wave-2 in 9 sections` put back | R54.5 | false | **true** ← stale arm is `[]` |
| P1 | fresh wrong number, plausible receipt: "round-54 C2 receipt printed `total=12`" | R54.3 | false | **true** |
| P2 | fresh wrong number, this round's receipt: "prints `grammar=7/9`" (receipt prints 6/9) | R54.3-shape | false | **true** |
| P3 | fresh wrong number in QUALITY.md: "receipt names `credited=58`" (prints 60) | R54.1-shape | false | **true** |
| P6 | fresh wrong freeze pointer `deadbeef0` in a SCORECARD row | R54.2 | false | **true** (stale scan matches only `7883e0e5\|fe70474d`) |
| P7 | fresh wrong number in LOG.md: "`total=12`" | R54.3 | false | **true** |
| P14 | duplicate authority drifts: `corpus/lessons/round-55.md` table says `staged=84` (receipt 81) | R54.9 | false | **true** |
| P5 | the pinned stale claims appended *inside* the corrections block | all | false | **true** |
| P13 | ER-R54-1 rewritten to false prose that still contains `CTL_MISMATCH` and `2/3` | R54.1 | false | **true** |
| P12 | receipt annotated "an earlier format printed total=99", no record edit | — | (no claim) | **false**, derived `total=99` |

Receipts: `plants.stdout`, `plants2.stdout`, `p1.stdout` … `p14.stdout` in
`T55W2CritCalibrationMove-receipts/`; drivers `plants.sh`, `plants2.sh`. Sample outputs:

```
PLANT P10_old_digest_49280fe5 (class R54.4, row has stale=[] )
exit=0
C1_R55: rev=e83a6e69b55e classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true

PLANT P1_fresh_total_12 (class R54.3)
exit=0
C1_R55: rev=0dbaff66d81c classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true

PLANT P5_stale_inside_corrections_to_EOF
exit=0
C1_R55: rev=a41ccedc0b55 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true

PLANT P13: false prose carrying the R54.1 tokens
counter_exit=0
C1_R55: rev=314c573b5bfe classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

### Why it cannot generalise (mechanism, from the frozen bytes)

- **Six of ten rows pass `[]` as the stale arm** — `measure.py:226,234,241,248,254,271`
  (R54.4, R54.5, R54.6, R54.7, R54.8, R54.10). Their `stale=0` is by construction, not by
  measurement, so the target's "zero stale hits outside the corrections section" is
  vacuously satisfied for those rows. P10 and P11 put the exact pinned defect text back and
  the verdict does not move.
- **The exclusion zone runs to EOF.** `corrections()` (`measure.py:67-80`) runs from the
  heading to the next `## ` line; the heading is SCORECARD line 2621 of 2702 and there is no
  later `## `, so every appended sentence of SCORECARD is inside the exclusion zone. P5
  re-states five pinned falsehoods there and stays green. This also means `SCORECARD.md`'s
  tail is a permanent blind spot for any future append.
- **The "derived" values are first-match regexes over receipt text, not the verdict line.**
  `re.search(r"total=(\d+)", bc)` (line 218) takes the first `total=` anywhere in the file, so
  P12 flips the counter red with no record change. Sensitivity is there; binding to the fact
  is not.
- **Two corrected arms are token presence.** R54.1 requires `"CTL_MISMATCH" in corr and
  "2/3" in corr` (line 205), which P13 satisfies with prose asserting the opposite; R54.8
  requires `"config.yml"`/`"fabricated"`/`"SUPERSEDED (round 55"` (line 255).
- **One premise arm is vacuous.** R54.8's premise is `bool(seat)` (line 254) — any non-empty
  seat file.

### The record overstates the counter

`corpus/lessons/round-55.md` writes, of the round-54 control defect: *"The counter for this
class is C1's `R54.1` row, which now requires the receipt's `CTL_MISMATCH`/`2/3` to appear in
the corrections section."* It discloses the token-presence design honestly, but claims the
row counters the class; P13 shows it counters a token. And freeze **amendment 5** states a
general predicate — *"no stale assertion may stand in the lane's records outside the
corrections section"* — implemented as four literal rows out of ten (P10, P11, P1, P7, P14).
This is a calibration defect of the same family C1 is chartered to repair: a frozen artifact
whose words describe more than it does.

## Both ways, then the decision

**For "bookkeeping a do-nothing control could have produced":** the counter is a ten-row
literal battery. Six rows cannot fail their stale arm; fresh instances of the class pass; the
corrections block is a self-exclusion zone; the one row the lesson calls "the counter for this
class" accepts false prose. Nothing in the counter stops a seat from transcribing the
spot-check's numbers and never touching the record beyond appending a section.

**Against:** that seat does not pass. `CTL_0`/`P0` is red at base, `CTL_SKIP_c1` is red, and
the numbers are not free — a wrong transcription fails (P9), a tree that moves under the row
fails (P8), and nine of ten values reproduce under independent derivation, with the tenth's
external provenance verified directly (row 690, 15:12:15Z, `config.yml:418`). The stale
assertions were removed *in place* and a re-introduction of one is caught (P4b).

**Decision:** C1 **is** a calibration move. It reconciles the lane's record to the tree at
the ten pinned points, the reconciliation is tree-true rather than plausible, and the
do-nothing and transcription controls are refused. Its counter is a **regression battery for
the ten pinned literals**, not a class detector: the phrase in the wave item, "a counter that
would catch the same class again", is **false as implemented** (eight green plants). Under
C1's frozen surface — `contract.json` C1.surface = the ten routed defects — the claim's
target is met, so this is **not a closure blocker**; it is a routed defect.

## Smallest safe correction

Two widenings of existing arms, no new arms, no new denominators, target text unchanged:

1. Replace `[]` with each row's own spot-check "Old:" literal
   (`corpus/lessons/round-54-verifier-spotcheck.md` R54.4/.5/.6/.7/.8/.10) as that row's
   stale pattern. Closes P10, P11 and makes "zero stale hits outside the corrections section"
   true for ten rows instead of four.
2. Terminate the corrections block with an explicit end marker (or make `corrections()` stop
   at EOF-with-sentinel) and scan the remainder. Closes P5 and removes the SCORECARD tail
   blind spot.

The only thing that meets "catch the same class again" is a new arm binding each receipt
quoted in the record set to the `name=value` it is quoted for (closes P1, P2, P3, P7, P14) —
that is a new arm with new denominators and a wider surface, so it belongs in a round-56
contract, not an amendment here.

**Admissibility:** phase A is running right now — `.ufo/evidence/round-55/control/` holds only
an uncommitted `controls-a.stdout` with the single line `CTL CTL_0_c1 …`, and no exit file. An
amendment is therefore still admissible by the round's rule ("pre-control"), but I do **not**
recommend re-freezing mid-control: C1's target is met, so the correction routes as a finding
with these receipts and the record-side wording (amendment 5, `corpus/lessons/round-55.md`) is
named as the thing to fix first.

## Bounds and hygiene

- No lane production file, frozen file, wave spec, fleet-root tracked file or PATH entry was
  written or edited. Fixtures were `git clone --shared` copies under
  `$HYAKU_SCRATCH/tameshi-r55/T55W2CritCalibrationMove` (`/fast/scratch/hyaku`), each asserted
  with `git rev-parse --show-toplevel` before any commit in it; the directory was removed
  after the receipts were captured.
- Census (read-only): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  tameshi` → `census_exit=0`.
- Tooling: nothing installed or upgraded this seat.
- Read-only reads outside the lane: `.ufo/evidence/round-54/control/*`,
  `/home/vgpnk/.omp/agent/history.db` (sqlite3 `mode=ro`), `/home/vgpnk/.omp/agent/config.yml`,
  live `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge` count.

## Artifacts opened

Lane (all at `9cf0146…` unless noted): `.ufo/evidence/round-55/{contract.json,freeze.json,
controls.sh,no-harm.sh,deciding-run.sh,c1/measure.py,c1/staged-at-freeze.txt,
before/c1.stdout,before/c2.stdout,control/controls-a.stdout}`; `SCORECARD.md`
(`## Round 54 …`, `## Round 55 - round-54 record corrections`); `corpus/QUALITY.md:1580-1600`;
`corpus/lessons/round-54.md`; `corpus/lessons/round-54-verifier-spotcheck.md`;
`corpus/lessons/round-55.md`; `LOG.md`; `.ufo/evidence/round-54/{freeze.json,
after/frozen.stdout,before/c2.stdout,control/controls-a.stdout,control/controls-b.stdout,
c2/measure.py}`; `.ufo/waves/round-54/w1-registry.json`, `.ufo/waves/round-54/{w1,w2}/*Read*.json`;
`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`; `.ufo/waves/round-54/w2/T54W2Sent01-receipts/`;
git history for `.ufo/waves/round-54/w2/T54W2Sent03.md` and the forged-reader rename.
Outside: `/home/vgpnk/.omp/agent/history.db`, `/home/vgpnk/.omp/agent/config.yml`,
`/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge`, `scripts/sources-census.sh`.

## Receipts in this directory

`plants.sh`, `plants2.sh`, `verify.sh` (runnable drivers); `plants.stdout`, `plants2.stdout`,
`verify.stdout`; per-plant counter output `p0.stdout`, `p1.stdout`, `p2.stdout`, `p3.stdout`,
`p4b.stdout`, `p5.stdout`, `p7.stdout`, `p8.stdout`, `p9.stdout`, `p10.stdout`, `p11.stdout`,
`p12.stdout`, `p13.stdout`, `p14.stdout` (note: `p4.stdout` is the mis-placed first attempt of
P4, whose plant landed inside the corrections exclusion zone — that accident is the evidence
for P5's blind spot and is kept rather than deleted).
