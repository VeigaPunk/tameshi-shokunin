# T56W1ScribeScorecard — round-56 `SCORECARD.md` block (draft, wave 1)

- **seat:** T56W1ScribeScorecard (L1 `TameshiR56`, hyaku run 11, wave 1)
- **item:** draft the round-56 SCORECARD block — (a) the restated standing axis row
  for calibration whose score is the value the round-21 monitor actually reads at the
  commit the row names, (b) the two claim rows (C1, C2) with before / target /
  counting command / controls, (c) the round's planned-next line.
- **lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; base
  `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; frozen instrument set
  `c3e2ca9f020776b3d66c7af854fb82c834674fcf` (`.ufo/evidence/round-56/`, `freeze.json`
  `files` = 10, `amendments` = `[]`).
- **deliverable:** the block in §1, byte-exact — `T56W1ScribeScorecard-receipts/block.md`,
  sha256 `ef4166a64cc5025ea516f33332d3ad6fbcbccc284db1fd4d46b628b0f60ffad9`, 7 034 B.
- **writes:** this report and `T56W1ScribeScorecard-receipts/` only. No lane production
  file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`), no frozen
  instrument, no git mutation anywhere in the lane. The one commit this seat made is in
  a scratch clone (§4b), whose toplevel was asserted equal to the clone path first.

## 1. The exact block

Append at end of `SCORECARD.md` (the block starts with a blank line, so one blank line
separates it from the round-55 block). Nothing above it is edited.

```markdown
## Round 56 — cold-read floor re-key and standing-row restatement (calibration) + receipt-revision binding gate (operability) (2026-10-28)

L1 TameshiR56, hyaku run 11, attempt 1. Two claims on distinct axes,
pre-registered with both counters, the controls harness, the fifteen no-harm
monitors and the deciding script in `.ufo/evidence/round-56/contract.json`,
frozen at `c3e2ca9f` before any seat ran (`amendments: []`, ten frozen files);
base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`, whose content files are
byte-identical to `fa48c06c` on every claim path. Calibration is the lowest
non-retired axis and carries C1: at base the round-21 monitor reads
`covered=46 score=6 box3=false` while the standing row asserts 8 — the
round-55 routed defect R55.3. C2 repairs R55.5 (the deciding gate could not
compare the revision it certifies): one rule, one tool,
`tools/receipt-revision-gate.py`, and the round's own receipts gated at the
revision they certify.

### Standing axis table — re-stated at round 56 (base `981c5e8b`)

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| calibration | 6 | `python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV` prints `calibration_restraint_score=6` with `sections_covered=46/64` and `box3_full_page=false` at the commit named in the next cell. The round-54 row above asserted 8; the same command prints 6 at that row's own commit `d33053f7` (57/64 credited), so 8 was a stale standing value — 8 is the monitor's ceiling, not its reading. R55.3, repaired by this round | `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` | 56 |

The row states the score the monitor itself prints at the commit the row
names, never a target. **At the deciding revision this row is re-stated to the
monitor's own line at the content commit C0** — score cell = the printed
`calibration_restraint_score`, measured-commit cell = C0, both cells
`pending deciding run at <the L1 fills this>`; C1's arm 6 reads the LAST
`calibration` row at the revision and requires its score to equal the monitor
at that revision *and* at the commit it names, so a row asserting 8 before the
monitor prints 8 at C0 is R55.3's defect repeated (and R55.2's class: a number
no receipt carries).

### Round 56 — claims (frozen in `.ufo/evidence/round-56/contract.json`)

| Claim (axis) | Before | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|
| C1 — calibration (6 at base; the lowest non-retired axis; surface: the cold-read floor): the eighteen base-lost cold-read headings are re-read at one content commit, bound under one `rekey-r56-<c0>` directory, and the standing calibration row states the monitor's own score at the commit it names, so `C1_R56_PASS=true` | `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`, exit 1 (`.ufo/evidence/round-56/before/c1.stdout`; re-derived identically at base, `.ufo/waves/round-56/w1/T56W1ScribeScorecard-receipts/c1-at-base.stdout`) | `total=0`: precheck `cand_credited=64 lost=0 ok`; monitor `64/64 score=8 box3=true`; 18/18 headings bound with `read_rev=<c0>`; 18/18 committed reader reports whose `section_sha256` is the section's bytes at REV; no bound entry pinning LOG.md or SCORECARD.md; the last `calibration` row equal to the monitor at REV and at its own commit | `python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | pre-registered, verdicts not quoted before they run: `CTL_0_c1` (do-nothing at base), `CTL_SKIP_c1` (re-key entries removed), `CTL_FAB_c1` (one reader's section hash fabricated), `CTL_RESTATE_c1` (row asserts a score the monitor does not read), `CTL_POS_c1` (scored at PIN in a fresh clone); receipts `.ufo/evidence/round-56/control/` |
| C2 — operability (no numeric score; surface: the deciding gate's receipt binding): every receipt the lane certifies is bound to the revision it was measured against, and `tools/receipt-revision-gate.py` refuses the real receipts rounds 54 and 55 accepted, so `C2_R56_PASS=true` | `C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false`, exit 1 (`.ufo/evidence/round-56/before/c2.stdout`; re-derived identically at the freeze, `.ufo/waves/round-56/w1/T56W1ScribeScorecard-receipts/c2-at-freeze.stdout`); the round-54 gate that accepted the same control set is on record as `.ufo/evidence/round-54/after/deciding-run.exit` → `DECIDING_RUN_EXIT=0` | `total=0`: selftest 14/14; the three real red-before receipts refused with the codes above; the round's own control receipts accepted at the certified revision; the rule stated in `corpus/QUALITY.md` (falsifier: the gate's own refusal code on the round-54 receipt), `corpus/knowledge/receipt-revision-binding.md`, `SKILL.md` `## Standing rules` and a `tools/registry.json` cell naming three refusal codes | `python3 .ufo/evidence/round-56/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | pre-registered, verdicts not quoted before they run: `CTL_0_c2` (do-nothing at the freeze), `CTL_SKIP_c2` (the binding arm removed), `CTL_FAB_c2` (a receipt that only names the certified revision), `CTL_POS_c2` (scored at PIN in a fresh clone); receipts `.ufo/evidence/round-56/control/` |

The after values are read from the deciding receipts under
`.ufo/evidence/round-56/after/`, never from this table (a deciding line that
differs voids the row); the measured-close subsection is appended after the
single deciding invocation and reads `pending deciding run at <the L1 fills
this>` until then. What the counters cannot see (contract `cannot_see`):
C1 — whether a reader actually read the section (a `section_sha256` is
computable from the tree without reading, so a fabricated report satisfies
arm 4; the wave's adversarial seats are the only guard); C2 — whether a
receipt that names the certified revision was produced by the run it claims
(a copied `rev=` token passes; the digest sidecar narrows but does not close
it).

Capabilities: **none claimed this round** (both counters are claim
instruments, not lane capabilities).

**Planned (round 57):** close C1's `cannot_see` — require each reader report
to carry a located quote (offset plus excerpt) the counter checks against the
section's bytes at REV, so a report that never opened the section cannot
credit, and keep one adversarial seat whose report must fail to credit; close
C2's `cannot_see` — the gate cannot tell a receipt produced by a run from one
carrying a copied `rev=` token, so route the digest sidecar into the gate and
extend it to the no-harm monitors' receipts (today only the counters and
controls are gated); carried from R55.6 — the next round's base sweep must show
no round-56 file untracked at closure, and from R55.7 — closure seats work in
scratch clones, never in the lane tree.
```

## 2. What each cell is anchored to

| block text | value | command / receipt |
|---|---|---|
| calibration score `6` | `calibration_restraint_score=6`, `sections_covered=46/64`, `box3_full_page=false` | `python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` → `receipts/monitor-base.txt` |
| "the same command prints 6 at that row's own commit `d33053f7` (57/64)" | `score=6 covered=57/64 box3=False` | same monitor `--rev d33053f7` → `receipts/monitor-d33053f7.txt` |
| measured-commit cell `981c5e8b…` | resolves to a commit, is an ancestor of any REV, and the monitor reads 6 there | `git rev-parse --verify 981c5e8b^{commit}`; static arm-6 parse in §4a |
| C1 before line | byte-identical to the round's before receipt | `.ufo/evidence/round-56/before/c1.stdout`; re-derived at base by this seat → `receipts/c1-at-base.stdout` (identical line, exit 1) |
| C2 before line | byte-identical to the round's before receipt | `.ufo/evidence/round-56/before/c2.stdout`; re-derived at the freeze by this seat → `receipts/c2-at-freeze.stdout` (identical line, exit 1) |
| `DECIDING_RUN_EXIT=0` (round 54) | the gate that accepted the same control set | `.ufo/evidence/round-54/after/deciding-run.exit` |
| control ids | C1: `CTL_0_c1`, `CTL_SKIP_c1`, `CTL_FAB_c1`, `CTL_RESTATE_c1`, `CTL_POS_c1`; C2: `CTL_0_c2`, `CTL_SKIP_c2`, `CTL_FAB_c2`, `CTL_POS_c2` | `contract.json` `claims.C1.controls` / `claims.C2.controls`; printed names in `.ufo/evidence/round-56/controls.sh:39-128` |
| "fifteen no-harm monitors" | `no_harm_monitors: 15`, and 15 `echo "NOHARM …"` lines in the harness | `contract.json`; `grep -c 'echo "NOHARM' .ufo/evidence/round-56/no-harm.sh` → 15 |
| "byte-identical to `fa48c06c` on every claim path" | `fa48c06c` resolves (`fa48c06c3669…`) and the diff is empty | `git diff --stat fa48c06c 981c5e8b -- SKILL.md SCORECARD.md LOG.md corpus tools` → no output |
| every hash the block names | `fa48c06c`, `c3e2ca9f`, `981c5e8b`, `d33053f7` all resolve | `git rev-parse --verify <h>^{commit}` ×4 |

Round-start conformance: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, trailer
`tameshi ok …/corpus/SOURCES.md`; `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md`
→ `140` (S001–S280) (`receipts/census.txt`).

## 3. The one integration obligation (what the L1 must fill)

The frozen counter's arm 6 is the authority on the row (`.ufo/evidence/round-56/c1/measure.py:255-281`):

- it takes the **last** table line whose first cell is exactly `calibration` and whose
  second cell is pure digits (`re.fullmatch(r'\d+', cells[1])` — a non-numeric score
  cell makes the row **invisible** and the counter silently falls back to the round-54
  row, which is the failing case);
- it takes the **first** token in the measured-commit cell that resolves as a commit
  (`re.findall(r'[0-9a-f]{7,40}', cells[3])`, first resolvable wins), so a stale hash
  must not precede the intended one in that cell;
- it requires `row_score == monitor(REV)`, `monitor(row_commit) == row_score`,
  `'round-21' in cells[2]`, and `re.search(r'\b56\b', cells[4])`.

Therefore, after the content commit C0 exists and the monitor prints its line there:

1. score cell ← the printed `calibration_restraint_score` at C0 (8 only if the monitor
   prints 8 there — 64/64 credited with box 3);
2. measured-commit cell ← C0 (and nothing else resolvable in that cell);
3. evidence cell ← the monitor command with its printed `score=`/`covered=`/`box3=`
   values at C0;
4. last-change cell stays `56`.

Both values are `pending deciding run at <the L1 fills this>` at this wave — the block
ships the *before* form (`6` at base, the only value any receipt carries today) because
filing 8 now is R55.3's defect repeated (a row asserting a score the tree does not
support) and R55.2's class (a quoted number no receipt contains). The placeholder lives
in the prose and in the measured-close stub, **never in the score cell** — see F5.

## 4. Falsification of this draft

**(a) Static parse against arm 6's own predicate** — over `git show HEAD:SCORECARD.md`
in the demo clone: `calibration_rows=8`, last row `cells=5`, `score='6'`,
`resolvable_tokens_in_commit_cell=['981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1']`,
`'round-21' in evidence: True`, `round56 in last-change: True ('56')`,
`row_commit_is_ancestor_of_HEAD=True`. Every conjunct of the predicate holds.

**(b) End-to-end, frozen counter, scratch clone** (`git clone --shared` of the lane,
`checkout --detach c3e2ca9f`, toplevel asserted = clone path, one commit
`74b8c3c52130329d53a9b1e9fe5e1e9ac8a96a1d` carrying the block):

```
EXPLAIN arm1-precheck exit=1 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=74b8c3c52130 cand_credited=46 lost=18 RED
EXPLAIN arm2-monitor covered=46 score=6 box3=False
EXPLAIN arm3-rekey dirs=[] c0=None
EXPLAIN arm4-readers 0/18
EXPLAIN arm6-restate row_score=6 row_commit=981c5e8b20a2 score_at_row=6 evidence='`python3 .ufo/evidence/round-21/coldread/measure.py --repo L' round='56'
C1_R56: rev=74b8c3c52130 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=6 total=4 C1_R56_PASS=false
```

(`receipts/demo-c1-with-block.stdout`.) The block moves the counter from `total=5` to
`total=4`: **arm 6 passes with the drafted row**, and the four remaining arms are the
wave-2 obligations (precheck, monitor, re-key, readers), not defects of the row.

**(c) The negative case is the frozen counter's own before line.** At base, with the
round-54 row standing, the same arm prints `row_score=8 row_commit=d33053f7552d
score_at_row=6 … restate=8 total=5` — i.e. the arm rejects exactly the stale assertion
this round repairs. The guard is the frozen arm, not my prose.

**(d) The SCORECARD append itself is credit-neutral — measured, not assumed.** In the
demo clone the monitor reads `score=6 covered=46/64` before and after the append
(`receipts/demo-monitor.txt`), and all 64 section sha256 are identical base→demo
(`section_sha_identical_base_vs_demo=64/64`). Mechanism: exactly one matched section
(`## The cadence's first scheduled tick, and the service's limits (round 9, measured)`,
sha `dcfb2df9002d`, credited at base) has entries that pin `SCORECARD.md`/`LOG.md`, and
only **one of its five** matching entries does (the 88-input `read_rev=eb7838b16490`
entry); the other four are pin-free, so the section stays credited when `SCORECARD.md`
changes (`receipts/section-pin-map.txt`). This is a fact about the ledger at base, not a
guarantee at REV: the deciding revision must be re-read by the monitor, which the
harness already does twice (`no-harm.sh` `coldread-floor` requires `score>=8` and
`credited>=64`; `deciding-run.sh` runs the precheck and the counters from REV bytes).

**(e) What would falsify the draft:** landing it verbatim at a REV where the monitor
reads 8 (arm 6 then fails on `row_score != score`), or filling the score cell with 8
before the monitor prints 8 at C0 (a number no receipt carries). Both are the same
obligation stated in §3.

## 5. Findings routed to the L1

- **F1 — the row is a measurement, not a target; it must be re-stated once after C0.**
  The block ships `6 @ 981c5e8b`, which is what the monitor prints there. The final row
  at the deciding revision must be the monitor's line at C0 (§3). One edit, two cells.
- **F2 — the measured-commit cell must hold exactly one resolvable token.** Arm 6 takes
  the first resolvable one; leaving `d33053f7` in that cell (e.g. as a comparison) makes
  the arm compare against the wrong commit and fail. The `d33053f7` comparison belongs
  in the evidence cell, where it is now.
- **F3 — a non-numeric score cell is invisible to arm 6.** `pending …` in the score cell
  would make the counter fall back to the round-54 row and fail for the wrong reason, so
  the placeholder is confined to the prose and the measured-close stub.
- **F4 — table width.** The item asked for the table's five columns, so both tables here
  are five columns and the axis is carried inside the claim cell
  (`C1 — calibration (6 at base; …)`); round-54's claims table was six columns with a
  separate `Axis` column. Nothing parses either table — splitting the axis back out is a
  free one-cell edit if the L1 prefers the lane's earlier convention.
- **F5 — R55.4 avoided by construction.** The controls cells name the nine pre-registered
  ids and say "verdicts not quoted before they run"; no control outcome appears in the
  block. The L1 fills outcomes only from `.ufo/evidence/round-56/control/` after the runs.
- **F6 — the planned line is a proposal, grounded in the contract's own `cannot_see` and
  in the round-55 routed defects.** C1's `cannot_see` (a `section_sha256` is computable
  without reading) and C2's (a copied `rev=` token passes) are quoted verbatim from
  `contract.json`; R55.6/R55.7 are the spot-check's items 6 and 7. The L1 owns or drops
  any of the three.
- **F7 — depth and freshness are deliberately not restated.** No claim this round
  touches them and this seat measured neither, so no number is filed for them; their
  round-54 rows stand as dated literals.

## 6. Conformance of this seat

| requirement | observation |
|---|---|
| writes confined to `.ufo/waves/round-56/w1/` | `git -C <lane> status --porcelain` shows this report and its receipts directory only (plus the pre-existing untracked round-56 evidence/wave dirs of other seats) |
| no lane production or frozen-instrument edit | `SCORECARD.md`, `SKILL.md`, `LOG.md`, `corpus/**`, `tools/**`, `.ufo/evidence/round-56/**` untouched; the block is a draft, the row experiment ran in a clone |
| no mutating git in the lane | the only commit is in `/fast/scratch/hyaku/tameshi-r56/T56W1ScribeScorecard/clone-demo`; `git -C "$D" rev-parse --show-toplevel` was asserted equal to `$D` before the commit |
| scratch | `HYAKU_SCRATCH=/fast/scratch/hyaku`, seat dir `tameshi-r56/T56W1ScribeScorecard` (clone + work dirs + receipts), removed after the receipts were copied |
| tools installed | none (no package manager, no `uv tool`, no binary) |
| census | exit 0, 140 rows, at round start |

## 7. Out of scope for this seat (other seats / the L1)

The C2 content (`tools/registry.json` cell, `corpus/knowledge/receipt-revision-binding.md`,
`corpus/QUALITY.md` criterion, `SOURCES.md` row, `SKILL.md` `## Standing rules` rule);
the LOG entry, the lesson and the report skeleton; the instruments' falsification (arm
liveness, gate fuzz/mutants, controls/deciding/no-harm dry runs, freeze discipline); the
18-heading drift map, pinned-input set and receipt inventory recon; the re-key itself and
the 18 reader reports (wave 2); and the integration of this block into `SCORECARD.md`,
which only the L1 performs.

## 8. Artifact paths

- report: `.ufo/waves/round-56/w1/T56W1ScribeScorecard.md`
- block (byte-exact): `.ufo/waves/round-56/w1/T56W1ScribeScorecard-receipts/block.md`
- receipts: `…/T56W1ScribeScorecard-receipts/` — `monitor-base.txt`,
  `monitor-d33053f7.txt`, `c1-at-base.stdout`, `c2-at-freeze.stdout`,
  `demo-monitor.txt`, `demo-c1-with-block.stdout`, `section-pin-map.txt`, `census.txt`
