# T48A2ScribeShonen — report (a2w1, scribe, axis calibration)

Item: draft the report's `## SHONEN` section (one line per `SHONEN.md` box, each pointer checked)
and evidence bullets for the three trend verdicts (`expansion`, `quality`, `discernment` per
`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md`) from round-48 records
at content `c7586b9a10effc63b4bd327f976edc094c1bdc17`. Deliverable:
`.ufo/waves/round-48/a2w1/T48A2ScribeShonen.draft.md` (237 lines).

Verdicts were **not** chosen — supporting and contrary evidence only, as the item required.

## Behavior

- Read the contract (`contract.json`, all ten amendments), `SHONEN.md`, `corpus/SOURCES.md:140-143`,
  `corpus/lessons/round-48.md` (all sections), `corpus/QUALITY.md:1382-1434`, `SCORECARD.md:2320-2367`,
  `LOG.md:2348,2359`, `reports/round-1-calibration.md:65-200`, `corpus/README.md` (coverage map),
  the committed round-48 receipts, and the a2w1 peer reports that bear on the trends
  (`T48W2ExecC1ProbeA.md`, `T48W2RevQuality.md`, `T48W2ScoutSpotcheck.md`).
- Opened every `SHONEN.md` pointer at the content revision. All four resolve; none can be `[x]`
  (no named non-author verifier in round 48) and none is `[ ]`.
- Ran the round-21 coldread monitor twice, read-only, into scratch (64 s and 61 s wall, exit 0):
  ```
  $ python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev c7586b9a10effc63b4bd327f976edc094c1bdc17      # .coldread-rev.json
  $ ... --rev 15b1521ea2e95d0d708059458c090e9f334adf32    # .coldread-15b1521.json
  SCORE=6 DEPTH=9 COVERED=57/64 BOX3_FULL_PAGE=False LEDGER_PRESENT=True      (both)
  SHONEN marks=~~~~ asserted=4 checked=0 untouched=0 box3_marked=True box3_ledger_link=True box3_points=False
  SOURCES rows=128 malformed=0
  ```
  My `.coldread-rev.json` is byte-identical to the digest the a2w1 executor recorded
  (`17e55ca0…`, `T48W2ExecC1ProbeA.md:137`) — an independent reproduction, not a copied number.
- No claim counter was run (not this seat's job); no mutation, no selftest sweep, no writes outside
  the three files listed under *Touched surfaces*.

## Draft `## SHONEN` lines (deliverable content, verbatim from the draft)

- `[~]` box 1 (`SHONEN.md:5-6`) — pointer `reports/round-1-calibration.md#box-1` resolves
  (file 26 651 B at `c7586b9a`, anchor `:71`, section to `:105`); lane assertion, no independent
  promotion verifier (`:100-103`); `SKILL.md` untouched at the revision, so no round-48 change
  bears on it.
- `[~]` box 2 (`SHONEN.md:7-8`) — pointer `#box-2` resolves (anchor `:105`); round-48 bearing:
  both round-48 entries are in `LOG.md` (`:2348` attempt 1, `:2359` attempt-2 correction).
- `[~]` box 3 (`SHONEN.md:9-10`) — pointer `.ufo/evidence/round-21/coldread/ledger.json` resolves
  (3 489 570 B at the revision); monitor state `box3_full_page=false`, `57/64` credited,
  `box3_points=false` → box 3 earns no point, score 6. Evidence base weakened *by this round*:
  committed base receipt `60` (`before/coldread-sections-at-base.stdout`) vs observed `57`.
- `[~]` box 4 (`SHONEN.md:11-12`) — pointer `#box-4` resolves (anchor `:176`); `PROVINCE.md`
  untouched at the revision and the four re-anchored documents are published docs, not
  sibling-owned ground; the round **rejected** the staged package copies instead of absorbing them
  (`corpus/lessons/round-48.md:91-96`).
- `[x]`: none. `[ ]`: none.

## Findings

**F1 — the restated calibration row carries a stale sub-measure no counted surface can see.**
`SCORECARD.md:2355` states "`box3_full_page=false`, 60 of 64 sections credited … runs 3 stable",
measured "round-48 content revision". Observed at both `15b1521` (the revision its own `--emit`
ran at) and `c7586b9a`: `57/64` (my two receipts above). The C1 counter reads only the integer:
`pick_line` for a `monitor` statement returns `str(json.loads(out)['calibration_restraint_score'])`
(`.ufo/evidence/round-48/calibration/measure.py:261-265`), so `runs 3 stable` passes with a
55→60→57-era figure inside the same evidence cell. Command that shows the mismatch:
`python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev c7586b9a…` → `COVERED=57/64`.
(In-scope for the L1 as a row erratum; I did not edit `SCORECARD.md`.)

**F2 — the QUALITY block appended at this revision fails its own criterion 97.**
`git -C <lane> cat-file -e c7586b9a:.ufo/evidence/round-48/quality/c94-96-falsifiers.stdout` →
absent; same for `control/c1-controls.stdout`; both also absent at tip `17cc5ce`. Criterion 94
(`corpus/QUALITY.md:1382`) and 95 (`:1400`) name those receipts; criterion 96 (`:1420`) names no
committed receipt at all. The committed red receipt
(`.ufo/evidence/round-48/quality/pointer-check-red-15b1521.stdout`) prints exactly these two
`MISSING` lines, and criterion 97's green leg ("the same command at the round-48 landing tip exits
0") is false at every observable revision. Independent of the a2w1 reviewer's F1, which reached the
same conclusion in `.ufo/waves/round-48/a2w1/T48W2RevQuality.md:19-56` (uncommitted peer report).

**F3 — this round's record edits cost three cold-read sections, and nothing went red.**
Committed base receipt `60` (`before/coldread-sections-at-base.stdout`), observed `57` at
`c7586b9a`; the seven uncovered headings include `## Mutation-sweep recipe`,
`## Restore discipline`, `### The map`, `## Repeated controls and gate registry`,
`## Pin disposition and provenance correction`. Same class as round 47's `PROVINCE.md` append
(`.ufo/evidence/round-47/quality/round46-lesson-dash-restored.md:127`: 60 → 55, score unchanged).
The no-harm monitor records the credited total but has no threshold on it, so 57 is not a red.

**F4 — SHONEN box 3 cannot be credited, and its pointer is not the reason.** Pointer resolves;
`box3_full_page=false` keeps `box3_points=false` and `calibration_restraint_score=6`
(`shonen` block of both receipts). The box's own parenthetical ("input-keyed monitor only") is
accurate; the `[~]` is not a self-assessment mismatch, but the evidence behind it is weaker at this
revision than at base (F3).

**F5 — trend evidence, both directions (verdict left to the L1).**
- expansion: supporting — 124→128 mined rows (`S265-S268`, `corpus/SOURCES.md:140-143`), all four
  cited by entries on line 1. Contrary — zero new `knowledge/` entries
  (`git diff --name-status 473336d9 c7586b9a -- corpus/knowledge/` → 4 `M`, 0 `A`; 58 entries at
  both revisions), all four rows "supersede X's anchor and quote only" (same documents), no
  coverage-map row added (`corpus/README.md` unchanged), and `SCORECARD.md:2365` says
  "Capabilities: none claimed this round".
- quality: supporting — four entries re-verified `2026-10-26` with located quotes; S266 restores the
  consequent round-45's dispute said was dropped; four criteria appended with lesson cites
  (`corpus/QUALITY.md:1382,1400,1420,1428`); one red-on-fixture/green receipt pair committed
  (`pointer-check-red-15b1521.stdout`, `pointer-check-selftest.stdout`). Contrary — F1, F2, F3
  above; S026's live re-fetch is not byte-identical to its snapshot (97 rotating-token bytes; quote
  still located) and that is disclosed for S108 but not for S026
  (`T48W2ScoutSpotcheck.md` §Spot-check 1, uncommitted peer report).
- discernment: supporting — two `### Reject` blocks each with a decisive cite and a `Flip:`
  (`corpus/lessons/round-48.md:91-96`, `:98-104`), the mis-cited `PROVINCE.md:14-18` reason
  withdrawn by appended erratum (`:207-284`) and turned into QUALITY 94; four Gate quotes inside
  the 25-word bound with their required phrases (`:21-24`). Contrary — **no outside spot-check exists
  for round 48**: the lesson says the spot-check is the closure's (`:16-19`), LEARNING.md counts a
  lane-dispatched seat as the lane, and the a2w1 spot-check returned `AGREE … narrowly` / `AGREE`
  with a byte-reproducibility caveat (`T48W2ScoutSpotcheck.md`); criterion 94's own falsifier is
  form-only (`T48W2RevQuality.md` F4) and F2's receipt is absent.

## Gates

- Pointer resolution (all four SHONEN boxes): pass — `git show c7586b9a:<path>` + anchor grep,
  `git cat-file -e`/`-s` for the ledger (3 489 570 B).
- Coldread monitor, two revisions: exit 0, score 6 both; **57/64** vs the committed base 60.
- Pointer check over the QUALITY round-48 block, by `git cat-file -e`: **fail** at `c7586b9a` and
  `17cc5ce` (2 absent receipts) — the same result the committed red receipt records for `15b1521`.
- Not exercised (out of this seat's item): `C1_R48_PASS` / `C2_R48_PASS` deciding runs, C1 CTL_A-E,
  `falsifiers.sh` blocks, census at the content revision, any mutation pass.

## Touched surfaces

Writes, all under `.ufo/waves/round-48/a2w1/`:

| path | sha256 | note |
|---|---|---|
| `T48A2ScribeShonen.draft.md` | `05c8c35305fd8082…` | the deliverable (237 lines) |
| `T48A2ScribeShonen.coldread-rev.json` | `17e55ca072298ad5…` | monitor at `c7586b9a`, 255 565 B |
| `T48A2ScribeShonen.coldread-15b1521.json` | `7763df7ca4f9ee93…` | monitor at `15b1521`, 255 565 B |
| `T48A2ScribeShonen.coldread-rev.stdout` | `20eff99b0d592ed6…` | command, both summaries, uncovered list |

Nothing under `corpus/`, `tools/`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `.git`, `.jj` was written;
no `git` or `jj` mutating command was run; `git status --porcelain -- corpus tools SCORECARD.md` is
empty after my runs (the monitor writes nothing into the repo — `PYTHONDONTWRITEBYTECODE=1`,
scratch `TMPDIR`). Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ScribeShonen` removed
(`test -d` → absent). Disk at start: 606 G free on `/fast`; no ENOSPC.

## Out of scope / limits

- No verdict selected for any of the three trends; no `SCORECARD.md` erratum written (F1 is the L1's
  to file); `SHONEN.md` not edited.
- The peer reports cited as **[W]** (`T48W2ExecC1ProbeA.md`, `T48W2RevQuality.md`,
  `T48W2ScoutSpotcheck.md`) are uncommitted working-tree artifacts at `c7586b9a`; their claims are
  reported as theirs, except where my own receipt reproduces them (the coldread digest does).
- Tooling: nothing installed or upgraded (no `pacman`, no `uv`, no `npm`).
