# T55W1ScribeQuality — QUALITY criterion 106, and the erratum that 105's own falsifier forced

seat: scribe (leaf member; no subagent dispatch)
axis named for this item: **calibration** (the round's lowest non-retired axis, 8)
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base: `0a2010acd1e92e4e332774050825e21bcfc7e079`
counter freeze: `631cd6455e58dce969310b4c0466c3383d9f5108`
date: 2026-10-28

This seat wrote no lane production file. Everything below is a draft, a patch, or a receipt
under `.ufo/waves/round-55/w1/T55W1ScribeQuality-receipts/`. The lane worktree was dirty from
other seats' in-flight integration for the whole session; the in-place correction at
`corpus/QUALITY.md:1590` is theirs, and the patch is written against those bytes, not base.

---

## 1. Deliverables

| path (under `.ufo/waves/round-55/w1/`) | what it is |
|---|---|
| `T55W1ScribeQuality.md` | this report |
| `T55W1ScribeQuality-receipts/criterion-106.md` | the exact block to append (55 lines: criterion 106 + `## Erratum — 2026-10-28` for 105) |
| `T55W1ScribeQuality-receipts/quality-106.patch` | append-only diff of that block against the worktree `corpus/QUALITY.md` |
| `T55W1ScribeQuality-receipts/c106-controls.py` | the criterion's check (four arms) |
| `T55W1ScribeQuality-receipts/rescore-positive.sh` | round-54 phase B with the clone taken at the revision it certifies |
| `…-receipts/c106-fail.stdout`, `.exit` | the falsifier run on the round-54 receipt: exit 1 |
| `…-receipts/c106-pass.stdout`, `.exit` | the re-scored control at `c2108100`: exit 0 |
| `…-receipts/c106-pass-check.stdout`, `.exit`, `.rev` | the checker on the re-scored receipt + the round-55 records: pass |
| `…-receipts/c106-paraphrase-mutant.*` | verbatim quote present plus a contradicting restatement: one `paraphrase` fail |
| `…-receipts/c106-rev-mutant.*` | line quoted verbatim but attributed to the freeze commit: one `rev` fail |
| `…-receipts/c1-on-integration-snapshot.stdout` | frozen C1 over the integrated tree **with** criterion 106: `total=0` |
| `…-receipts/quality-106-applycheck.stdout` | `patch -p1 --dry-run` against the worktree bytes |

Patch shape: 1 hunk, `0` removed lines, `+47` non-blank added lines, 5505 bytes; criteria
`30 -> 31`; one `## Erratum` heading added; `patch -p1 --dry-run` prints
`checking file corpus/QUALITY.md` and exits 0.

---

## 2. The draft, verbatim

Fenced for reading; the bytes the lane should append are `criterion-106.md`, and the patch is
the same bytes in diff form.

```
## Criteria appended — round 55 (2026-10-28)

### Criterion 106 — a pre-registered control is scored at the revision it certifies, and its verdict line is quoted

A control that certifies a revision is scored at that revision. A control cloned at a
freeze commit, a base commit or any other ancestor measures the tree before the work it
is meant to prove, so its verdict carries nothing about the claim; the defect does not
show in the verdict word either, because such a control prints the same line shape as a
live one. Two things are therefore read from the receipt, because the author can supply
neither from memory: the `rev=<sha>` its own line carries, which must resolve to the
revision the claim certifies, and the verdict line itself, which the record quotes
verbatim. Restating a control in the author's words turns the instrument into a second
assertion — round 54's phase-B control was cloned at the freeze commit `077d431e`
(predating the re-key `7fa9a5e`), printed the short fall `rekeyed=3/7` with
`CTL_MISMATCH … expected=true actual=false` and `CONTROLS_B: 2/3`, and four record files
reported it as a control that fired (routed as R54.1; [ER-R54-1]). A control scored at a
freeze commit may be reported as a freeze-time measurement, but it cannot be the arm
that certifies a later revision.

Check that can fail: `python3 .ufo/waves/round-55/w1/T55W1ScribeQuality-receipts/c106-controls.py --lane LANE --rev REV --certifies CERT --control NAME=PATH --record PATH [--expect NAME=true]` reads each named receipt from `REV`'s objects and runs four arms: `rev` — the control's own `rev=` token resolves to CERT; `verdict` — the same line's `…_PASS=` equals the pre-registered expectation; `quote` — some `--record` carries that line whitespace-normalized and verbatim; `paraphrase` — no record restates the control after naming it: within a 120-character forward claim window, a bare `true`/`false` or a `key=value` for a key the receipt's line carries with another value. It prints `OK <name> …` per passing control, `FAIL <name> <arm> …` per failure, then `C106: controls=N pass=N fail=N`; exit 0 iff `fail=0`, 1 on any failed arm, 2 on setup (a receipt or record absent at REV, an unresolvable revision, a non-repository LANE, no `--record`).

Lesson: `corpus/lessons/round-54-verifier-spotcheck.md` R54.1 — the control that was
recorded as firing, the receipt that says it did not, and the four files that restated it.

Falsifier that must fail: at base `0a2010ac` the round-54 receipt
`.ufo/evidence/round-54/control/controls-b.stdout` prints its control at
`rev=077d431e6996 … rekeyed=3/7 … total=4 C1_R54_PASS=false`, then
`CTL_MISMATCH CTL_POS_c1 expected=true actual=false` and `CONTROLS_B: 2/3`, exit 1,
while the round-54 claim certifies `c21081008adb`; the check exits 1 with
`FAIL CTL_POS_c1 rev`, `FAIL CTL_POS_c1 verdict`, `FAIL CTL_POS_c1 quote` (no base
record carries the line), and `FAIL CTL_POS_c1 paraphrase` on `SCORECARD.md`'s bare
`true` and on the lesson's restated re-key count
(receipt `.ufo/waves/round-55/w1/T55W1ScribeQuality-receipts/c106-fail.stdout`). That
same control re-scored at the certified revision passes: it prints
`rev=c21081008adb … credited=64 lost=0 rekeyed=7/7 … total=0 C1_R54_PASS=true` with
`CONTROLS_B: 1/1 as pre-registered` (in the same receipts directory,
`c106-pass.stdout`, produced by `rescore-positive.sh`).

## Erratum — 2026-10-28

**QUALITY 105's falsifier is the receipt that refutes its claim (found by R54.1).**
Criterion 105 landed with a falsifier saying its round-54 arm fires on the control and
prints the full re-key count there. The receipt that falsifier names,
`.ufo/evidence/round-54/control/controls-b.stdout`, prints that control at
`rev=077d431e6996` with `rekeyed=3/7`, then `CTL_MISMATCH CTL_POS_c1 expected=true
actual=false` and `CONTROLS_B: 2/3`, exit 1: the arm never fired, because the control
was cloned at the freeze commit instead of the revision it was meant to certify. The
false text is quoted in full in `SCORECARD.md`'s
`## Round 55 - round-54 record corrections` (ER-R54-1), the only place the old values
may stand. Criterion 105's rule is not withdrawn — an arm is proven only where it must
fire — and its falsifier now stands corrected in place; the quote obligation that would
have caught the restatement is criterion 106. The independent positive at the certified
revision is `.ufo/evidence/round-54/after/c1.stdout`: `rev=c21081008adb … credited=64
lost=0 … total=0 C1_R54_PASS=true`.
```

Why the erratum does not reproduce 105's old falsifier word for word: the frozen C1 R54.1
stale arm scans `corpus/QUALITY.md` for the token pair `positive control` … `rekeyed=7/7`
within 160 columns and for the literal `CTL_POS_c1 true`; quoting the old sentence inside
the erratum would re-arm that stale hit in the very file the round is cleaning. Criterion 35's
"name the false text and its replacement" is met by naming it, pointing to the full quote in
`SCORECARD.md`'s corrections section (the one block the counter excludes), and naming the
replacement that now stands at 105. 105 is not deleted, not renumbered, not softened.

---

## 3. Falsifier demonstration

The check reads every receipt and record from git objects at `--rev`; `--certifies` is the
revision the claim names. Four runs, each with its own receipt:

| run | command (abridged; full argv in the receipt's report line) | observed | exit |
|---|---|---|---|
| fail (the falsifier) | `c106-controls.py --lane LANE --rev 0a2010ac --certifies c21081008adb --control CTL_POS_c1=.ufo/evidence/round-54/control/controls-b.stdout --record SCORECARD.md --record corpus/QUALITY.md --record corpus/lessons/round-54.md --expect CTL_POS_c1=true` | `FAIL … rev scored_at=077d431e6996 certifies=c21081008adb`; `FAIL … verdict line=C1_R54_PASS=false expected=true`; `FAIL … paraphrase SCORECARD.md+294678 bare true receipt=false`; two `FAIL … paraphrase` on the lesson's `rekeyed=7/7`; `FAIL … quote NOT_QUOTED …`; `C106: controls=1 pass=0 fail=1` | 1 |
| pass (re-scored at the certified revision) | `rescore-positive.sh LANE 077d431e c2108100` — the committed phase-B script with one variable changed (clone at REV), frozen counter bytes `sha256=d7749f84…` | `CTL CTL_POS_c1 C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true`; `CONTROLS_B: 1/1 as pre-registered` | 0 |
| pass (checker over that receipt + the round-55 records) | `c106-controls.py --lane <fixture clone at c2108100> --rev HEAD --certifies c2108100 --control CTL_POS_c1=fixture/cpos-at-c2108100.stdout --record fixture/quote.md --record SCORECARD.md --record corpus/QUALITY.md --record corpus/lessons/round-54.md --expect CTL_POS_c1=true` | `OK CTL_POS_c1 rev=c21081008adb …`; `C106: controls=1 pass=1 fail=0`; fixture rev `95add361e91f` | 0 |
| mutant: paraphrase beside the verbatim quote | same, reading `fixture/restated.md` too | `FAIL CTL_POS_c1 paraphrase fixture/restated.md+61 rekeyed=3/7 receipt=rekeyed=7/7` — quote arm still satisfied, so this isolates `paraphrase` | 1 |
| mutant: verbatim quote of a line attributed to the freeze | same, reading `fixture/cpos-freeze.stdout` + its quote | `FAIL CTL_POS_c1 rev scored_at=077d431e6996 certifies=c21081008adb` — verdict and quote arms pass, so this isolates `rev` | 1 |

The two mutants matter because the falsifier run fails all four arms at once; without them a
dead `rev` arm or a `quote` arm satisfied by the `paraphrase` scan would look healthy
(criterion 105's own lesson). Fixture commits were made only in `git clone --shared` clones
under scratch, after `git -C "$D" rev-parse --show-toplevel` printed that clone; no lane or
fleet repository was mutated.

---

## 4. Calibration safety of the append

- Both frozen R54.1 stale patterns over the patched QUALITY bytes: `SCAN CTL_POS_c1_true hits=0`,
  `SCAN posctl_rekey_7of7 hits=0` (the second is byte-identical to
  `.ufo/evidence/round-55/c1/measure.py:173`).
- Frozen C1 over an integration snapshot — the worktree's tracked changes applied to a clone
  at the freeze commit, plus this block — prints
  `C1_R55: rev=ebf4dc3dfd67 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true`,
  exit 0 (`c1-on-integration-snapshot.stdout`). That snapshot is a scratch commit and says
  nothing about the lane's own content revision; it shows only that this block does not
  disturb C1's ten classes.
- The same two patterns over the whitespace-normalized whole document — the arm the worktree's
  C1 counter is gaining in an in-flight amendment (`scan_span`, flattening whitespace so a
  hard-wrapped claim cannot hide) — also find nothing: `SPAN CTL_POS_c1_true matches=0`,
  `SPAN posctl_rekey_7of7 matches=0`; the block contains no `positive control` phrase at all,
  so the pair cannot be assembled across a line break either.
- The append adds no `SKILL.md` text, so the cold-read floor monitor
  (`.ufo/evidence/round-21/coldread/measure.py`, `credited>=64`) is untouched by this seat.

---

## 5. What the L1 must do with this

1. Append `criterion-106.md` to `corpus/QUALITY.md` (or `patch -p1 < quality-106.patch`) and
   commit the receipts directory: criterion 106's `Check that can fail` cites
   `.ufo/waves/round-55/w1/T55W1ScribeQuality-receipts/c106-controls.py`, so that path must
   exist at the content revision for the citation to resolve (criterion 104's rule).
2. Round 55 must satisfy its own criterion 106. The frozen `controls.sh` phase B already
   clones at `REV` (the round-54 defect is fixed there), so the `rev` arm passes; the new
   obligation is the quote: carry the round-55 phase-B `CTL CTL_POS_c1 …` line verbatim in
   the round-55 `SCORECARD.md` block (the same block that carries `CONTROLS_B`), then run
   `c106-controls.py --certifies <deciding rev> --control CTL_POS_c1=.ufo/evidence/round-55/control/controls-b.stdout --record SCORECARD.md`. Without the verbatim line the check
   reports `NOT_QUOTED` on the round's own record — correctly.
3. Do not renumber or delete 105; the erratum is the correction path.

---

## 6. Findings (reported, not repaired — not this seat's files)

**F1 — the amended frozen bytes need a freeze commit of their own, and the base C1 receipt was
produced by the older counter.**
Stable observation: gate 0 of the frozen deciding run, replayed against the named freeze,
prints `FREEZE_INTEGRITY: OK files=6 amendments=0` for `631cd64`, so the manifest and the
bytes agree *inside that commit* — while `deciding-run.sh:65-66` requires
`FREEZE_UNCHANGED=1` over `FREEZE..REV` for `contract.json c1/measure.py c2/measure.py
freeze.json …`. During this seat's run the worktree carried amended frozen bytes:
`contract.json = 5de4f37b14db` (amendments 1-5 recorded in it), `c2/measure.py = d6ca1d851bb0`,
and `c1/measure.py = 711507e7b5bd`, which is the freeze-commit bytes plus 25 lines: `LOG.md`
added to `RECORD` and a new `scan_span()` whitespace-normalized arm. At the end of the run the
worktree `freeze.json` listed amendments 1-3 and pinned `contract=ed6871e17697`,
`c1=77abe1e9daf4`, `c2=ab3ae7514691` — none of which matched those worktree bytes at the moment
of reading. This is reported as a snapshot, not as a defect: the L1 was visibly mid re-freeze.
The requirement it has to meet is mechanical — those bytes must land in a **new freeze commit**
that re-pins `freeze.json` (digests and the full amendment list) and must be the `FREEZE`
argument the deciding run gets; landing them in the content commit prints
`FROZEN_UNCHANGED=0` and the deciding run exits 1.
Second half, same class as R54.4: `.ufo/evidence/round-55/before/c1.stdout` was produced by the
counter bytes frozen at `631cd64` (`77abe1e9daf4`). If the amended counter (`711507e7b5bd`) is
the one that decides, the base line the claim is measured against and the deciding line come
from different bytes — either re-derive the base receipt with the deciding bytes and say so, or
state in the round-55 block which bytes produced each line.
Command: the `FREEZE_INTEGRITY` replay (inline python from `deciding-run.sh:20-42`),
`sha256sum` of the worktree paths vs `freeze.json['files']`, and
`git diff 631cd64 -- .ufo/evidence/round-55/c1/measure.py` (25 added lines, shown above).

**F2 — the base C2 receipt changed after the freeze.** `.ufo/evidence/round-55/before/c2.stdout`
is `77721c4a3397` in the worktree and is not in `frozen_paths` or the manifest, but the
contract's `C2.before` text is a paraphrase of it and its line count is the number the C2 claim
is written against. Regenerating it is defensible (the amended counter prints it), but the
regeneration should be disclosed in the round-55 block next to the receipt, or a reader cannot
tell which counter bytes produced the "before" the target is measured from.
Command: `git status --porcelain` (`M .ufo/evidence/round-55/before/c2.stdout`) and
`sha256sum` as above.

**F3 — scratch under `tameshi-r55/` is not isolated from sweeping.** Between two of this
seat's calls, `$HYAKU_SCRATCH/tameshi-r55/T55W1ScribeQuality/` was removed by something outside
this seat (a sibling's cleanup), and a duplicate run of this seat's own rescore truncated
`c106-pass.stdout` mid-write. Both were rebuilt; every receipt cited here comes from a single
uninterrupted run, and the rescore script now uses `$$`-suffixed scratch and refuses to print a
control verdict when the counter produced none (`RESCORE counter-exit=` + exit 2 on a setup
refusal). Reported so the closure does not read a vanished fixture directory as a missing
receipt.

---

## 7. Not done, named

- No lane production file edited (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`
  are untouched by this seat), no commit, no push, no `jj`.
- No `corpus/SOURCES.md` row: this seat opened no external source — every claim above is a lane
  artifact (`git show`, a frozen counter, a receipt). Census observed as
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
  `ok …/corpus/SOURCES.md`; 140 rows match the registry shape
  `^ {0,3}\| S[0-9]{3,} \|` and 141 lines anywhere contain an `| S### |` cell (the assignment's
  "139 rows" is the round-start floor; the worktree is above it, from other seats' rows).
- No `LOG.md` entry, no `corpus/lessons/round-55.md` text, no `SCORECARD.md` round-55 block:
  other seats own those, and 106's `Lesson:` line cites the round-54 spot-check, not a
  round-55 lesson section whose text does not exist yet.
- No tool installed or upgraded.
- Scratch (`/fast/scratch/hyaku/tameshi-r55/T55W1ScribeQuality*`) removed at the end of the
  last fixture run; the receipts above are the durable copies.

---

## 8. Provenance (sha256, first 16 hex; full hashes reproducible from the files)

```
a9890eef0ea13642  c1-on-integration-snapshot.stdout
42c1b6315cf1b9d8  c106-controls.py
4355a46b19d348dc  c106-fail.exit / c106-paraphrase-mutant.exit / c106-rev-mutant.exit  (all "1")
5d506031de44001b  c106-fail.stdout
0da2e6aedbf5dd28  c106-pass-check.stdout
2617afef6e9b8828  c106-paraphrase-mutant.stdout
9ab4805e1ff532a5  c106-rev-mutant.stdout
e1ba936159e7a641  c106-pass.stdout
41dc5a81c745bd6d  criterion-106.md
d89136ed7557c599  quality-106.patch
ff383317c7e0a0d1  quality-106-applycheck.stdout
169d74bc37684d6d  rescore-positive.sh
9a271f2a916b0b6e  c106-pass.exit / c106-pass-check.exit  (both "0")
```

Frozen counter bytes used by the rescore: `.ufo/evidence/round-54/c1/measure.py` at
`077d431e` → blob `e96da3547e3d`, `sha256=d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812`
(the digest `freeze.json@077d431e` pins for that path).
