# tameshi round 95 — frozen declarations (plan)

Lane `tameshi` (verification-fixture craft). Round 95, attempt 1. Base (lane tip at
round start): `02ff6290945dde18062a366799a774abb50fb365`, branch `master`.

Round 94 landed `rejected-honest-stop`: C1 verified, C2 did not (the frozen
`DISPOSITION_SELFTEST: 8/8` sentence against the operative `9/9` receipt). Its non-author
spot-check (`corpus/lessons/round-94-verifier-spotcheck.md`) routed eight record defects
and eight instrument defects (`plans/round-94.plan.md` §A2–A8). This round answers them
and declares **two claims**, each frozen before any scored receipt exists.

Axes: depth + calibration (lane axes). C1 moves **coverage** (new presentation surfaces the
note reader now governs), C2 moves **calibration** (the audit's evidence binding). No axis
is re-scored in this file; verdicts are measured in the round report.

---

## Claims (frozen before data)

### C1 — coverage: the note reader governs five presentation classes it did not govern

- **Axis:** coverage (new governed surfaces: indented code, a double backslash before a
  pipe, a one/two-hyphen delimiter, and a second self-pin line).
- **Surface:** `corpus/knowledge/mutation-case-fleet-sources-census.md` read by the
  successor counter `.ufo/evidence/round-95/c1/measure-v95.py`.
- **Wording (frozen):** at the instrument revision, the honest committed note yields
  `C1_R95_PASS=true` exit 0 with `verdict_tables=1 badrows=0 mismatched=0`; the battery
  `.ufo/evidence/round-95/c1/controls-v95.py` prints exactly
  `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0`; the five states added over
  round 94's forty-five are `indent-code-row`, `indent-token`, `escaped-backslash-pipe`,
  `two-hyphen-delimiter` and `double-pin`, and their receipts print exactly:
  `indent-code-row` exit 0 / `C1_R95_PASS=true`;
  `indent-token` exit 0 / `C1_R95_PASS=true`;
  `escaped-backslash-pipe` exit 0 / `C1_R95_PASS=true`;
  `two-hyphen-delimiter` exit 0 / `C1_R95_PASS=true`;
  `double-pin` exit 2 / `C1_SETUP self-pin-line-count`.
- **Counter:** `python3 -I .ufo/evidence/round-95/c1/measure-v95.py --repo <lane> --rev REV --work <empty dir>`
- **Battery:** `python3 -I .ufo/evidence/round-95/c1/controls-v95.py --lane <lane> --rev <instrument rev> --base <base rev> --work <empty dir> --outdir <dir> --jobs 6`
- **Predicate:** `C1_R95_PASS=true` (counter); `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0` (battery).
- **Before:** at base `02ff6290` the successor counter does not exist (`C1_SETUP
  spec-absent-at-rev` when the baked SPEC path is read at base); round 94's counter at
  `6a2a1fdd` refuses the four note fixtures and executes the double-pinned counter to
  `C1_R94_PASS=true` (the four before-state receipts, §Controls before-column).
- **After:** the battery prints 50/50 and each added receipt prints the line above.
- **Kill rules:**
  - a: an honest note state (the committed note; a fixture note with the twelve cells; a
    fenced inverted table) is refused by a rule stated in this plan;
  - b: one of the five added states fails to print its declared line;
  - c: the counter blob at the instrument revision differs from the `claims.json` sha256,
    or a receipt was produced by other bytes;
  - d: a pre-registered state has no receipt, or the driver's summary counts a state it
    did not write;
  - e: the five fixtures are refused by the **before** counter for a reason other than the
    class this round names (i.e. the before-witness does not reproduce the routed defect).
- **Declared limits:** the reader recognises a delimiter cell with one or more hyphens
  (GFM §4.10 as quoted in the lesson); an indented line is literal unless it continues a
  list item; the self-pin certifies one and only one pin line before hashing, not that the
  executed bytes are the pinned bytes (identity stays bound by kill rule (c)).

### C2 — calibration: the disposition audit reads receipt bytes from the object store

- **Axis:** calibration (the audit's evidence binding: which bytes the verdict is read
  from, and whether a receipt can be forged or substituted after the fact).
- **Surface:** `.ufo/evidence/round-95/conjunct-disposition-v95.py` + the committed
  manifest `.ufo/evidence/round-95/conjunct-disposition.json`, audited against the
  committed battery receipts under `.ufo/evidence/round-95/pre-freeze/controls/`.
- **Wording (frozen):** at the instrument revision the checker prints
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0` exit 0 against the
  committed manifest and the receipts it names; every receipt named by the manifest's
  seventeen state rows carries a `counter_sha=<64 hex>` line equal to the sha256 of the
  counter blob at the `--rev` it is read from; the checker refuses with exit 1 and the
  named finding `receipt-absent-at-rev` a receipt that exists only in the working tree,
  and refuses with exit 1 and the named finding `receipt-counter-sha-mismatch` a committed
  receipt whose `counter_sha=` line is absent or differs from that digest; the round-94
  checker at `6a2a1fdd` prints `findings=0` exit 0 on both forged receipt sets; and the
  v95 checker refuses at setup with `DISPOSITION_SETUP replace-refs-present` when the
  lane clone carries a `refs/replace` entry naming the counter or manifest blob.
- **Counter:** `python3 -I .ufo/evidence/round-95/conjunct-disposition-v95.py --lane <lane> --rev REV --min-falsifiable 17`
- **Battery:** `python3 -I .ufo/evidence/round-95/conjunct-disposition-v95.py --selftest`
- **Predicate:** `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`
- **Before:** at base the successor checker does not exist
  (`DISPOSITION_SETUP counter-absent-at-rev`); the round-94 checker at `6a2a1fdd` accepts
  both forged receipt sets (`findings=0`) because it reads receipts from the filesystem
  and never reads a `counter_sha=` line.
- **After:** the positive prints 19/17/2/0; the two forged sets print exit 1 with the
  named findings; the selftest prints `DISPOSITION_SELFTEST: 11/11 pass`; the 50 committed
  battery receipts each carry the matching `counter_sha=`.
- **Kill rules:**
  - a: `findings=0` while a printed conjunct key has no row, a row names an unknown key, a
    state row's receipt does not move its conjunct, or an `unfalsifiable` reason is shorter
    than 40 characters, names no mechanism, or names no battery state and no pin digest;
  - b: fewer than 17 of the 19 rows carry a state;
  - c: the selftest cannot fail: a case that must produce a finding produces none, or the
    clean case produces one;
  - d: the checker or manifest blob at the named revision differs from the `claims.json`
    sha256;
  - e: a receipt that exists only in the working tree, or carries a wrong `counter_sha=`,
    is accepted;
  - f: a `refs/replace` entry is present and the checker proceeds instead of refusing at
    setup.
- **Declared limits:** authenticity of a hand-written receipt that carries the correct
  `counter_sha=` is not certified by this checker — the `counter_sha=` line binds the
  receipt to the counter blob, not to the driver run; driver-produced provenance is
  declared in the lesson as the remaining gap. `--receipts` is read from the object store
  at `--rev`; the checker does not execute the counter.

---

## Controls — the five added C1 states (pre-registered expectations)

Fixture notes are written by the driver into a scratch clone at the instrument revision;
the counter is extracted from the clone's object store. `pos-fixture` is round 94's
fixture shape (12 rows, `| id | arm | verdict | witness |`, `measured: 5/12 killed`).

| state | fixture | expected at v95 | before (v94 at `6a2a1fdd`) |
|---|---|---|---|
| `indent-code-row` | honest note + a 4-space-indented wrong-verdict table + a 4-space-indented `measured: 99/12 killed` line | exit 0, `C1_R95_PASS=true` | exit 1, `verdict_tables=false` |
| `indent-token` | honest note + a single 4-space-indented `\| C01 \| KILLED \|` line | exit 0, `C1_R95_PASS=true` | exit 1, `ids=false` (`stray-verdict`) |
| `escaped-backslash-pipe` | fixture note whose witness cell of row C01 ends `C:\\` (a literal backslash then the cell boundary) | exit 0, `C1_R95_PASS=true` | exit 1, `ids=false` (cells merge) |
| `two-hyphen-delimiter` | fixture note with delimiter `\|--\|--\|--\|--\|` | exit 0, `C1_R95_PASS=true` | exit 1, `ids=false` (stray verdicts) |
| `double-pin` | counter copy with a second `SELF_SHA256 = "<64 hex>"` line inserted before the `__main__` guard | exit 2, `C1_SETUP self-pin-line-count` | exit 0, `C1_R94_PASS=true` (R94R1 demo) |

Existing 45 states keep their round-94 expectations (the driver's `states()` table is the
authority; the report re-derives counts from receipts).

## Controls — C2 forged receipt sets (pre-registered)

Both are built in a scratch clone at the instrument revision:

| artifact | construction | v95 expected | v94 at `6a2a1fdd` |
|---|---|---|---|
| `forge-handwritten` | a receipt file named for a manifest state, hand-written with a matching `C1_CONJUNCTS` line, placed only in the working tree (never committed) | exit 1, `receipt-absent-at-rev` | exit 0, `findings=0` |
| `forge-counter-sha` | a committed receipt (in a scratch clone) whose `counter_sha=` line is `0`×64 | exit 1, `receipt-counter-sha-mismatch` | exit 0, `findings=0` |
| `forge-replace-ref` | `git replace` the counter blob inside the scratch clone | exit 2, `DISPOSITION_SETUP replace-refs-present` | exit 0, reads the substituted blob |

## Do-nothing controls (cheapest control that skips the work; frozen counter)

| id | command | expected |
|---|---|---|
| `c1-nowork-base` | the v95 counter with `--rev <base>` (its baked SPEC path is absent there) | exit 2, `C1_SETUP spec-absent-at-rev` |
| `c1-nowork-v94` | the v94 counter at `6a2a1fdd` on the five fixtures | the before column above (target not met) |
| `c2-nowork-base` | the v95 checker with `--rev <base>` | exit 2, `DISPOSITION_SETUP counter-absent-at-rev` |
| `c2-nowork-v94` | the v94 checker at `6a2a1fdd` on `forge-worktree` and `forge-counter-sha` | `findings=0` (target not met) |

If any do-nothing control meets the target, the counter or the target is wrong and the
round is re-declared before data.

---

## Round-94 routed defects answered by this round

| id | routed item | landing |
|---|---|---|
| 1 | C2 tally `8/8` vs operative `9/9` | erratum in `corpus/lessons/round-95.md` § Erratum, naming the superseded sentence; QUALITY 169 |
| 2 | report Sources & frontier counts | recount with the spot-check's command; the round-95 census prints the authoritative histogram |
| 3 | prefile row count and R94SN1 reasons | the round-95 ledger regenerates rows against this round's artifacts only |
| 4 | plan vs wave roster | this plan's §Wave declares 12 seats; the executed dispatch is committed beside it |
| 5 | sentinel F4–F7, F9 routing | answered in §A7 work: object-store reads (F2), counter_sha (F1), replace/GIT seal (F1), symlink receipt test (F5), no `/tmp` receipt root (F9) |
| 6 | lesson pointer to the aggregate line | `corpus/lessons/round-95.md` cites `pre-freeze/controls-run.log` for the aggregate |
| 7 | `--jobs 6` vs `--jobs 12` | the frozen battery command above says `--jobs 6` and the receipts record the invocation |
| 8 | wave naming (`r94-w1` vs the validator default) | this round's wave is `w1` (the default), so the closure's default command passes |

From `plans/round-94.plan.md` §A2–A8: A2 indented code, A3 single pin line, A4 double
backslash, A5 one/two-hyphen delimiter, A6 per-receipt `counter_sha=`, A7 sealed C2
checker with object-store receipts and the hand-written-receipt control, A8 one
discriminating state per survivor (A8 is measured this round, not claimed: the
mutation-tester reproduces all twelve survivors against the v95 battery and classifies each
as killed / subsumed / invariant with a receipt).

## Wave

One v1 wave `w1`, 12 seats: executor 4, scribe 1, scout 1, reviewer 2, critic 1,
mutation-tester 1, sentinel 1, connector 1 (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-95/w1-spec.json`).
Attack share 7/12 by role. The L1 holds the planner seat (§3 mapping: planner → L1).

## Frontier step

- `corpus/SOURCES.md`: S320/S321/S322 re-opened (used-by appends to `corpus/lessons/round-95.md`);
  S323 admitted new (CommonMark §4.4 Indented code blocks) with its fetch, snapshot and
  ≤25-word located quote in the lesson's `## Gate`.
- Census before: recorded at round start in the lesson/report; census after at round end.
- One mistake mined into `corpus/lessons/round-95.md` `## Mistakes` (class · evidence ·
  captured-by · fix), from round 94's C2 tally miss or a round-95 wave artifact.
- The sourced claim is C1: its indented-code and delimiter rules cite S323/S321 rows opened
  this round.

## Out of scope

No sibling gate code is edited; no fleet-root script or template is touched; no MANIFEST
entry; no `.scratch/` write; no host sysctl change; no pacman transaction (paused).

---

## Amendments (pre-data, before any scored receipt)

### A1 — `escaped-backslash-pipe` fixture precision (L1 before-state control)

The first construction (a four-column note whose witness cell ended `C:\\` before a
space-separated delimiter) does **not** discriminate: the round-94 counter pads the short
row, the verdict stays in its column, and it prints `C1_R94_PASS=true`
(`.ufo/evidence/round-95/pre-freeze/before-v94/escaped-backslash-pipe.out` from the first
run was replaced). The discriminating fixture is a **five-column** note
`| id | arm | path | verdict | witness |` whose C01 row is
`| C01 | fixture arm | C:\\|KILLED | differs |`: the v95 split gives five cells with the
verdict in column 4; the v94 split swallows the delimiter and gives four cells
(`width:9:cells=4`), so it prints `C1_R94_PASS=false`, exit 1. The claim wording, predicate
and expected after-line are unchanged; only the fixture construction is pinned here.

### A2 — `double-pin` fixture precision (the decoy goes before the real pin line)

A second `SELF_SHA256` line inserted **after** the real constant is the one Python executes,
so the counter dies `self-pin-mismatch` and the state does not discriminate (measured:
`.ufo/evidence/round-95/pre-freeze/before-v94/double-pin.out` records the corrected run;
the after-insert variant printed `C1_SETUP self-pin-mismatch`, exit 2). The fixture is the
decoy line `SELF_SHA256 = "000…0"` inserted **before** the real pin line: the executed
constant stays the real digest, v94 prints `C1_R94_PASS=true`, exit 0, and the v95 count
rule refuses with `C1_SETUP self-pin-line-count`. Claim wording, predicate and after-line
unchanged.

### A3 — before-column re-measured (L1 do-nothing control, committed receipts)

Measured with the round-94 counter at `6a2a1fdd`
(`.ufo/evidence/round-95/pre-freeze/before-v94/*.out`): `indent-code-row` exit 1
(`verdict_tables=false`, `dup:` badrows), `indent-token` exit 1 (`ids=false`,
`stray-verdict:365`), `escaped-backslash-pipe` exit 1 (`ids=false`, `width:9:cells=4`),
`two-hyphen-delimiter` exit 1 (`ids=false`), `double-pin` exit 0 (`C1_R94_PASS=true`).
This is the frozen `c1-nowork-v94` control: it does not meet the after-target.
