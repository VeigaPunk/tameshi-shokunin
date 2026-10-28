
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
