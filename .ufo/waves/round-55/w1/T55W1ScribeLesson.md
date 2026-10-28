# T55W1ScribeLesson — round-55 lesson skeleton (draft + reconciliation)

Seat: T55W1ScribeLesson (scribe), hyaku run 11, round 55, wave 1.
Role: UFO-FSD scribe — build the auditable artefact; do not edit the lane's
production files, do not commit the lane, do not rerun work to decorate a claim.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `0a2010ac`,
counter freeze `631cd645`.

## 1. Item and outcome

Item: draft `corpus/lessons/round-55.md` with `## Gate` (URL, access date,
<=25-word located quote, adopt/reject counts), `## Mistakes` (one mined
mistake), `## Round-54 routed defects - dispositions (this round)` (one row per
R54.1-R54.10, FIXED/REFUSED + evidence), and `## What the counters cannot see`,
matching the shape of `corpus/lessons/round-54.md`. Draft only; the L1 lands it.

Delivered:

- **the draft bytes**, complete and landable, at
  `.ufo/waves/round-55/w1/T55W1ScribeLesson-draft-round-55.md` (204 lines, 4
  required sections + a QUALITY pointer). It is the text to copy into
  `corpus/lessons/round-55.md`; every claim in it is backed by a receipt under
  `.ufo/waves/round-55/w1/T55W1ScribeLesson-receipts/`.
- **this report**, which includes the reconciliation below: the L1 had already
  created `corpus/lessons/round-55.md` (untracked, 80 lines) by the time the
  draft was ready. The draft is therefore offered as the replacement for that
  file, and the six divergences between the two are listed with the command
  that decides each.

Nothing in the lane was edited: no `SKILL.md`, `SCORECARD.md`, `LOG.md`,
`corpus/**` or `tools/**` write; no commit; no `git add` in the lane (the scratch
clones under `/fast/scratch/hyaku/tameshi-r55/T55W1ScribeLesson/` are the only
repos I committed in, each after asserting `git rev-parse --show-toplevel`).

## 2. Axes named (godspeed)

- **calibration** (the round's claim axis): the lesson is a record, so every
  number and pointer in it is a calibration surface. Moves kept: quote word
  counts re-counted by script; every derived value re-derived from its receipt;
  the census row count measured, not copied.
- **operability**: the Gate's adopted row is the only new source, and the note
  that cites it is the operator-facing contract; a wrong citation in the Gate
  propagates to the note.
- **discernment**: the reject is stated with the rule that actually applies (see
  finding F3 — the landed text's citation does not say what it claims).
- **honesty**: three blind spots were *demonstrated* rather than asserted
  (section 5, F5-F6), and each is shipped as a receipt.

## 3. The draft, by section

- `## Gate` — one row opened (S280, GNU Coding Standards §4.4): URL, access date
  2026-10-28, HTTP 200 / 7147 B, the row's reader extraction
  (`assimilation/S280-gnu-errors.txt`, sha256 `edcaf94b…`) plus two independent
  full-page fetches that are byte-identical (`54c55cd4…`), and a 10-word located
  quote at byte 5020 with the two literal forms at byte 5415. The admit says what
  the row *does not* buy: the page never mentions an exit status, so exit 2 and
  stderr are lane declarations. S277-S279 are named as held rows, not reopened.
  One candidate refused (FreeBSD `sysexits(3)`): already held as S090, CORPUS
  rule 2 admits a held-source row only in the `supersedes S0NN —` form, and the
  document deprecates itself. Counts line: 1 adopted, 1 refused, 0 re-pointed,
  0 retired; registry 139 -> 140; census exit 0.
- `## Mistakes` — one mined mistake: **a control scored at a revision that
  predates the work it certifies.** Evidence: `controls-b.stdout`'s own line
  (`rev=077d431e6996 … rekeyed=3/7 … C1_R54_PASS=false`), the `CTL_MISMATCH`
  line, `CONTROLS_B: 2/3`, plus `git merge-base --is-ancestor 077d431e 7fa9a5e`
  = 0 (the control's revision is an ancestor of the re-key commit; freeze
  12:12:06, re-key 12:21:35, deciding `c2108100` 12:22:15). captured-by: none —
  the harness took the revision as an argument, the deciding run never reads the
  `rev=` on the control's line, and the round-54 C1 counter never reads control
  receipts. fix: this round's `controls.sh` phase B clones at `REV`; QUALITY 106;
  and the residual is named (F5).
- `## Round-54 routed defects - dispositions (this round)` — ten rows, each with
  the receipt the value is derived from (see section 6).
- `## What the counters cannot see` — the contract's two declared blind spots,
  plus three demonstrated ones and the gate's own (section 5).
- `## QUALITY criterion` — a pointer to 106 (owned by T55W1ScribeQuality), not a
  second wording of it.

Deliberate differences from `round-54.md`'s shape: the Gate carries explicit
adopt/reject counts; the dispositions rows cite a receipt per class; the
cannot-see section carries commands, not just the contract's sentences; the
QUALITY criterion is a pointer so the lesson cannot disagree with
`corpus/QUALITY.md`.

## 4. Reconciliation against the landed `corpus/lessons/round-55.md`

The landed file exists (untracked, 80 lines). These are the six places where it
and the evidence disagree; each fix is a one-line edit or a replacement by the
draft.

| # | landed text (verbatim) | decided by | corrected value |
|---|---|---|---|
| 1 | `Census at round end: exit 0, 141 rows.` | `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` -> `140`; census `ok … exit 0` | **140** |
| 2 | sysexits quote `(14 words)` | script count of the quoted sentence | **15** |
| 3 | S280 quote `(19 words)` | script count | **17 words + one `...` token** |
| 4 | `a within-scope duplicate URL (CORPUS.md rule 2, census W04)` | `CORPUS.md:116-118` (rule 2 is *append-only*); `sources-census.sh:33` (W04 is a warning that "does not affect clean lanes") | reason = S090 holds the URL and rule 2 admits a held-source row only as `supersedes S0NN —`; W04 is not a rule and does not fail a lane |
| 5 | can't-see section: only the contract's two sentences | receipts `blindspot-*.stdout`, `log-outside-record.stdout` | add the three demonstrated blind spots (F5-F7) |
| 6 | R54.6 `the sweep commit is named`; R54.7 `with the rename commit` | `git log -1 --format=%h -- <path>` | name them: `ff2a821`, `7fa9a5e` |

Two smaller notes, not defects: the header's `content commit C0 (this commit's
parent chain)` names no sha (the draft leaves the sha to the L1 rather than
guess); the second `## Mistakes` entry (wrapped-text predicate) is a pre-score
near-miss found by the L1's own dry run — it is honest, but it should say
"near-miss, caught before any control scored" so it is not read as a fired
defect.

## 5. Findings (each with the command that produced it)

**F1 — `LOG.md` still carries two values of the routed classes, and C1 cannot
see them.** `c1/measure.py` scans `RECORD = ("SCORECARD.md",
"corpus/QUALITY.md", "corpus/lessons/round-54.md")`. At base and still now:

```
$ git grep -n -E '7883e0e5|wave-1 reader findings' 0a2010ac -- LOG.md
LOG.md:2500:`7883e0e5` (one mechanical C1 arm bug, found by the binder dry run before any
LOG.md:2509:wave-1 reader findings adjudicated and fixed — stale line anchors including
$ sed -n '2499,2501p;2508,2509p' LOG.md
`7883e0e5` (one mechanical C1 arm bug, found by the binder dry run before any
control score — the freeze pointer the deciding run uses). Claims: C1
SKILL three-arm rule, lesson Gate/Mistakes, QUALITY 105); C1 `99c3bc88` (25
wave-1 reader findings adjudicated and fixed — stale line anchors including
```

`:2500` is R54.2's exact false claim ("the freeze pointer the deciding run
uses", one commit before the re-key) and `:2508-2509` is R54.5's count (25 vs the
readers' 28). The round's `total=0` is true of three files; it is not true of the
lane's record. Recommendation: correct both in place (record edit, L1's call) or
ship the sentence as drafted ("at base, `LOG.md` … carried two values").
Receipt: `receipts/log-outside-record.stdout`.

**F2 — the landed lesson's census count is off by one** (reconciliation #1).
`receipts/census.stdout` (census `ok`, exit 0) and the row grep both give 140.

**F3 — `CORPUS.md rule 2` is cited for a rule it does not contain.** The fleet
contract says:

```
2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
   is logged old→new in the round lesson. A correction is a new row whose `teaches` opens
   `supersedes S0NN —`.
```

and the census's own header says `W04 same URL across scopes (warnings do not
affect clean lanes)`. So the landed "(CORPUS.md rule 2, census W04)" overstates
both: rule 2 is append-only, and W04 is a tolerated warning. The refusal is still
right (S090 holds the URL); the citation should be rule 2's *supersedes* form,
plus the deprecation. Receipt: `receipts/corpus-rule2-and-w04.stdout`.

**F4 — two quote word counts are wrong in the landed Gate** (reconciliation
#2/#3). Measured with a script over the exact quoted strings (receipt:
`receipts/quote-word-counts.stdout`).

**F5 — the deciding run does not tie a control's printed revision to `REV`.**
`deciding-run.sh:46-52` checks `git cat-file -e`, blob-ness, size > 0 and
`merge-base --is-ancestor FREEZE <receipt commit>`; it never compares the
`rev=` on the `CTL` line with `REV`. So the class this lesson mines survives
structurally in the gate: a control cloned at the freeze and committed after it
would pass. The lesson says this in `## Mistakes` and again under "The gate
itself"; the frozen script is not edited (contract: frozen). Receipt:
`receipts/f5-deciding-run-control-check.stdout`.

**F6 — C1's stale scan is token-literal, and the corrections section is
excluded wholesale.** Two demonstrations on a snapshot clone of the lane
worktree (`692bdd12`, C1 `total=0` there), each committed in scratch and scored
with the frozen counter:

```
# paraphrase the false claim back into the C1 claim row
old: CTL_POS_c1 `CTL_MISMATCH` `2/3` at the revision it cloned
new: CTL_POS_c1: true (the counter's positive control)
-> C1_R55: rev=b267f8178507 … stale=0 … total=0 C1_R55_PASS=true

# append a NEW wrong assertion inside the corrections section
+ **ER-R54-99 - planted.** The round-54 freeze pointer is `7883e0e5` and
  `CTL_POS_c1 true` at every revision.
-> C1_R55: rev=1ba9aee40e15 … stale=0 … total=0 C1_R55_PASS=true
```

Both receipts carry their reproduce recipe. This is the material addition the
draft makes to `## What the counters cannot see`.

**F7 — C2's lazy arm is a negative control.** `c2/measure.py:201` is
`ok = rc == exp`, so a lazy mode passes on its exit code alone; `lazy=5/5` says
no allocation happened on the path the unusable `TMPDIR` took, not that the mode
cannot allocate. The draft says so explicitly; the landed lesson says something
close ("cannot distinguish 'allocates nothing' from 'allocates only after its
preconditions fail'") without the line.

**F8 (observation, not a lane defect) — the round-54 spot-check's receipt-history
claim is imprecise.** It says `controls-b.stdout` is "committed, unchanged
across all 5 revisions that touch it"; `git log -- <path>` returns **two**
commits, and the bytes differ (a two-line re-statement footer was added at
`5564954`). Every verdict line is identical, so R54.1 stands; the parenthetical
is wrong on both counts. My draft uses the accurate phrasing. Receipt:
`receipts/f8-controls-b-history.stdout`.

**F9 (naming risk) — the refused candidate's extraction is named
`S281-sysexits.txt` while `SOURCES.md` reserves S281 as the next unused id.**
A later round that appends S281 for an unrelated source inherits a receipt name
that reads like a row. Not a defect; flagging because the round is about ids and
pointers.

## 6. Dispositions evidence (R54.1-R54.10)

Every value below was re-derived from the lane at base `0a2010ac` (or from the
receipt it names); the receipt files are in
`.ufo/waves/round-55/w1/T55W1ScribeLesson-receipts/`. The frozen counter reads
all ten `ok` on the lane worktree snapshot (`receipts/c1-base-and-snapshot.stdout`,
`total=0`, `classes_corrected=10/10`).

| id | derived value | receipt (lane path) | disposition |
|---|---|---|---|
| R54.1 | `CTL_MISMATCH` + `2/3`; control rev `077d431e` is an ancestor of the re-key `7fa9a5e` | `.ufo/evidence/round-54/control/controls-b.stdout` lines 1,2,5 | FIXED (3 in-place + ER-R54-1) |
| R54.2 | freeze pointer `077d431e` | `.ufo/evidence/round-54/after/frozen.stdout` | FIXED (ER-R54-2; fleet report `097985c1` recorded only) |
| R54.3 | `total=13` | `.ufo/evidence/round-54/before/c2.stdout` | FIXED (ER-R54-3) |
| R54.4 | c2 digest `8528ee85` | `.ufo/evidence/round-54/freeze.json`; `sha256sum` of the deciding bytes | FIXED (ER-R54-4) |
| R54.5 | `w1=28 w2=25 sections=12` | committed `w1/*Read*.json` (23 files) and `w2` (23 files) | FIXED (ER-R54-5) |
| R54.6 | sweep commit `ff2a821`; all three blobs present | `git log -1 -- <each path>` | FIXED, forward (ER-R54-6) |
| R54.7 | rename `7fa9a5e`, `R100`; old path absent | `git log --diff-filter=R -M --name-status` | FIXED (ER-R54-7) |
| R54.8 | `config.yml:418` reads `scout: "@m_grok"`; seat ends with SUPERSEDED | seat file tail; `~/.omp/agent/config.yml` | FIXED (ER-R54-8; the lesson records the incident) |
| R54.9 | `reviewers=5 attack=21/76 seats=76 staged=81` | `.ufo/waves/round-54/w1-registry.json`; `glob` count 81 | FIXED (ER-R54-9) |
| R54.10 | `controls-a` `rekeyed=0/7`; `0/30` in `r53-counter-at-88afa941.stdout` | both control receipts | FIXED (ER-R54-10) |

## 7. Gates I ran (outcome, not re-run to decorate)

| gate | command | outcome |
|---|---|---|
| source census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | exit 0; W04 warnings only; 140 rows |
| C1 at base | frozen `c1/measure.py --rev 0a2010ac --work <empty> --explain` | `premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` (matches `before/c1.stdout`) |
| C1 on the worktree snapshot | same bytes, `--rev 692bdd12` (scratch clone: lane at `631cd645` + every worktree-modified file) | `premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true` |
| C1 with the draft installed | same, plus the draft as `corpus/lessons/round-55.md` | `total=0 C1_R55_PASS=true` (the lesson landing does not disturb the scan) |
| quote counts | script over the exact quoted strings | see F4 |
| control receipt history | `git log -- <path>` + per-rev `sha256sum` | two commits; verdict lines identical |
| deciding-run control check | read `deciding-run.sh:46-52` | no `rev=` comparison (F5) |
| config.yml | `grep -n scout ~/.omp/agent/config.yml` | `418:    scout: "@m_grok"` |

Not run by me: the deciding invocation, the controls, no-harm, the C2 counter.
Those are the L1's or other seats' gates; my draft makes no claim about their
outputs beyond the paths where their receipts land.

## 8. Touched surfaces / out of scope

Wrote: `.ufo/waves/round-55/w1/T55W1ScribeLesson.md` (this file),
`…/T55W1ScribeLesson-draft-round-55.md`, `…/T55W1ScribeLesson-receipts/**`.
Read (no writes): the lane at base, the round-55 contract/contract-adjacent
files, the round-54 control receipts and spot-check, `CORPUS.md` (fleet root),
`tools/registry.json`, `~/.omp/agent/config.yml` (line 418 only).

Out of scope, deliberately: landing the lesson or any `SCORECARD.md` /
`LOG.md` / `corpus/**` edit (the L1 integrates); the fleet report's own stale
values (R54.1's fourth place, R54.2's `097985c1`) which are outside the lane;
editing the frozen counters, contract, controls or deciding script (report, do
not fix); the C2 counter's arms (other seats).

## 9. Tooling

No installs or upgrades: `curl` (present), `python3` (present), `git` (present)
covered every step. Nothing was written to any PATH directory. Scratch lived at
`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeLesson` and was removed at the end
of the seat; the snapshot clone revs quoted in the receipts
(`692bdd12`, `b267f817`, `1ba9aee4`) were scratch-only and are gone with it — the
receipts carry their reproduce recipe, and the lane-resolvable evidence is the
base receipts they name.

## 10. Artifacts

- draft: `.ufo/waves/round-55/w1/T55W1ScribeLesson-draft-round-55.md`
- receipts: `.ufo/waves/round-55/w1/T55W1ScribeLesson-receipts/`
  (`c1-base-and-snapshot.stdout`, `c1-with-lesson-draft.stdout`,
  `blindspot-paraphrase.stdout`, `blindspot-corr-section.stdout`,
  `log-outside-record.stdout`, `corpus-rule2-and-w04.stdout`,
  `census.stdout`, `r541…r5410-*.txt`, `sources/{gnu-errors,sysexits}.html`)
