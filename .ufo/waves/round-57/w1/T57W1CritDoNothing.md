# T57W1CritDoNothing — do-nothing controls for the round-57 C1 and C2 counters (wave 1)

Lane base `5e3569969b532310d2b8a3d130901757a3df356b` (lane HEAD re-read at the end: unchanged). Lane untouched; every
control ran in a scratch `git clone --shared` checked out at BASE, with commits made only in that clone. Nothing was
installed or upgraded. Receipts: `T57W1CritDoNothing-receipts/`; control scripts: `T57W1CritDoNothing-receipts/scripts/`.

Staged counters were present at first look (`T57W1ExecC1Counter/stage/...c1/measure.py`, sha256 `936a520c…`;
`T57W1ExecC2Counter/stage/...c2/measure.py`, sha256 `7d49e3c4…`; `T57W1ExecExtract/stage/...c1/defects.json`, sha256
`bef2293b…`, 51 items). No polling was needed.

## Method (what each control does)

- C1 (`scripts/ctl_c1.py`): commit A adds the staged `defects.json` byte-identical and a copy of the staged counter with
  its `PIN_PENDING…` marker replaced by the `defects.json` sha256 (scratch only; the staged file is untouched; the
  printed `self=fec8bba613ef` is this pinned copy, not the staged `936a520c…`). Commit B is the ledger under test
  (base 49 rows unchanged, 51 new rows). Counter run: `--lane CLONE --rev B --work <empty> --explain`.
  - Excerpt rule for all rows: the first `git grep -i -F` hit (at BASE) of one of the item's keys on an admissible path
    (not a spot-check, not the ledger, not HARD, not SOFT unless the path ends with the key); excerpt = normalised line
    extended to >=15 chars, capped at 400 chars around the key. Evidence path = the file where the key occurs.
  - (a) `CTL_DECLINE`: every row `declined` with an 89-char reason stating that no work was done and no fix is claimed.
  - (b) `CTL_OPEN`: every row `open`, plus a `**Planned (round 58):**` paragraph in SCORECARD naming all 51 ids.
  - (c) `CTL_FAB`: every row `fixed`, `commit` = newest commit at BASE touching the evidence path (no freshness check).
  - extra `CTL_FAB_SEARCH` (adversarial): for each row, the first (key, hit) whose excerpt is absent at `routed_at` and
    carries no ACK words; commit = the newest commit after `routed_at` touching that path. Falls back to the literal
    excerpt where no candidate exists.
  - probe `CTL_FAB_TEXT` (not do-nothing, see F1): one commit after BASE that only quotes each excerpt into a new lane
    file; R56.7 quoted from its own round-56 spot-check line.
  - probe `CTL_FAB_TEXT_APPEND`: the same quotes appended to an existing file (`LOG.md`).
- C2 (`scripts/ctl_c2.py`): commit A adds the staged C2 counter and `mutants.json` byte-identical. Commit B is the edit
  under test. Counter run: `--lane CLONE --rev B --work <empty> --explain`.
  - (a) `CTL_HELP`: three gate rows whose argv is `python3 tools/receipt-revision-gate.py --help --receipt …`, expecting
    exits 0, 2 and 3 with named codes. Variant `CTL_HELP_HONEST` expects exit 1 (what the gate really returns).
  - (b) `CTL_HARD`: three gate rows against committed hard-wired receipts (`.ufo/evidence/round-57/c2/hardwired/`):
    positive (exit 0), unresolvable `--certified` (exit 2), strict mismatch `--certified HEAD` with no `--paths` (exit 3).
  - (c) `CTL_SKILL`: every `RECEIPT_*` token deleted from the SKILL `## Standing rules` section (5 tokens), no rows.
  - extra `CTL_STACK`: `CTL_HARD` rows + a SKILL gate/probe row with the 0/2/3 map + the verdict-cell corrected to
    `RECEIPT_REV_CONTENT_DRIFT` (the R56.2 correction), i.e. the cheap honest-looking set.
  - liveness `CTL_REF`: `CTL_STACK` plus one genuine drift row (receipt names BASE, HEAD changed `SKILL.md`,
    `--paths` lists it).
  - probe `CTL_SKILLMAP`: SKILL gate row whose verdict map reads `0 ok; 2 ok; 3 ok`, nothing else.

## Verdict lines (verbatim, final run; receipts `c1-controls.stdout`, `c2-controls.stdout`, probe files)

C1 arm tallies from `C1_R57_TERMS` (zero = clean); `C1_R57_PASS` in each line.

| Control | Verdict line | Arm tallies (non-zero) |
|---|---|---|
| (base) `C1_CTL_0` | `C1_R57: self=fec8bba613ef rev=fa10d4ca0818 rows=0/51 agree=0/51 old49=ok fixed=0 declined=0 thisround=0 spot=ok total=77 C1_R57_PASS=false` | missing=51 fixed_short=20 this_round_short=6 |
| (a) `C1_CTL_DECLINE` | `C1_R57: self=fec8bba613ef rev=ca1061fb1165 rows=50/51 agree=50/51 old49=ok fixed=0 declined=50 thisround=0 spot=ok total=63 C1_R57_PASS=false` | missing=1 (R56.7) declined_over=36 fixed_short=20 this_round_short=6 |
| (b) `C1_CTL_OPEN` | `C1_R57: self=fec8bba613ef rev=47ee5569e444 rows=50/51 agree=50/51 old49=ok fixed=0 declined=0 thisround=0 spot=ok total=27 C1_R57_PASS=false` | missing=1 (R56.7) fixed_short=20 this_round_short=6 (open=50, open_unplanned=0) |
| (c) `C1_CTL_FAB` | `C1_R57: self=fec8bba613ef rev=516f5a6ef132 rows=50/51 agree=12/51 old49=ok fixed=50 declined=0 thisround=0 spot=ok total=45 C1_R57_PASS=false` | fixed_bad=38 missing=1 (R56.7) this_round_short=6 (fixed_short=0) |
| extra `C1_CTL_FAB_SEARCH` | `C1_R57: self=fec8bba613ef rev=150f07901367 rows=50/51 agree=42/51 old49=ok fixed=50 declined=0 thisround=0 spot=ok total=15 C1_R57_PASS=false` | fixed_bad=8 missing=1 (R56.7) this_round_short=6 |
| probe `C1_CTL_FAB_TEXT` | `C1_R57: self=fec8bba613ef rev=a22b42682354 rows=51/51 agree=51/51 old49=ok fixed=51 declined=0 thisround=51 spot=ok total=0 C1_R57_PASS=true` | none (repeat run: rev=ad81be89d30d, same tallies, PASS=true) |
| probe `C1_CTL_FAB_TEXT_APPEND` | `C1_R57: self=fec8bba613ef rev=0bab99f0a8b5 rows=51/51 agree=50/51 old49=ok fixed=51 declined=0 thisround=50 spot=ok total=1 C1_R57_PASS=false` | fixed_bad=1 (R53.5, `fixed-not-new`) |

C2 arms are `rows / executed / mutants / skill / codes / cell` (the shortfall of each, from the `EXPLAIN shortfall` lines).

| Control | Verdict line | Arms (rows, executed, mutants, skill, codes, cell) |
|---|---|---|
| (base) `C2_CTL_0` | `C2_R57: self=7d49e3c493b3 rev=16cc995c1bf4 gate_rows=0 exits=none held=0/0 mutants=0/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=11 C2_R57_PASS=false` | 6, 0, 3, 1, 0, 1 |
| (a) `C2_CTL_HELP` | `C2_R57: self=7d49e3c493b3 rev=0e5a1fbdd53f gate_rows=3 exits=0,2,3 held=0/3 mutants=0/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=8 C2_R57_PASS=false` | 0, 3, 3, 1, 0, 1 |
| (a') `C2_CTL_HELP_HONEST` | `C2_R57: self=7d49e3c493b3 rev=db1475fd62aa gate_rows=3 exits=none held=3/3 mutants=0/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=8 C2_R57_PASS=false` | 3, 0, 3, 1, 0, 1 |
| (b) `C2_CTL_HARD` | `C2_R57: self=7d49e3c493b3 rev=19a96326273b gate_rows=3 exits=0,2,3 held=3/3 mutants=1/3 skill_row=0 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=4 C2_R57_PASS=false` | 0, 0, 2, 1, 0, 1 (M3 killed by the exit-2 row; M1, M2 survived) |
| (c) `C2_CTL_SKILL` | `C2_R57: self=7d49e3c493b3 rev=aa6b9f68c8f2 gate_rows=0 exits=none held=0/0 mutants=0/3 skill_row=0 codes_known=0/0 standing_cell=WRONG:none total=12 C2_R57_PASS=false` | 6, 0, 3, 1, 1, 1 |
| extra `C2_CTL_STACK` | `C2_R57: self=7d49e3c493b3 rev=0a835bc03df6 gate_rows=3 exits=0,2,3 held=3/3 mutants=1/3 skill_row=1 codes_known=4/4 standing_cell=ok total=2 C2_R57_PASS=false` | 0, 0, 2, 0, 0, 0 (M1, M2 survived) |
| probe `C2_CTL_SKILLMAP` | `C2_R57: self=7d49e3c493b3 rev=2179478a25f8 gate_rows=0 exits=none held=0/0 mutants=0/3 skill_row=1 codes_known=4/4 standing_cell=WRONG:RECEIPT_REV_MISMATCH total=10 C2_R57_PASS=false` | 6, 0, 3, 0, 0, 1 |
| liveness `C2_CTL_REF` | `C2_R57: self=7d49e3c493b3 rev=48e9d4b99a9c gate_rows=4 exits=0,2,3 held=4/4 mutants=3/3 skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R57_PASS=true` | 0, 0, 0, 0, 0, 0 (M1 killed by the drift row, got=0; M2 got=3 with the needle missing; M3 by the unresolvable row, got=0) |

Every do-nothing control (a), (b), (c) fails on every claim arm it cannot satisfy. No do-nothing control reaches PASS.

## Findings

**F1 — counter defect, C1 `fixed` arm: a commit that only quotes excerpts reaches `C1_R57_PASS=true`.** Probe
`C1_CTL_FAB_TEXT` (receipt `c1-probe-fab-text.stdout`): one commit after BASE creates `corpus/lessons/round-57-quotes.md`
containing the 51 literal excerpts; each row is `fixed` with that commit. Result: `total=0 C1_R57_PASS=true`.
Mechanism: `measure()`/`judge()` check freshness as `then = show(routed_at, path)`; `if then is not None and excerpt in then:
continue`. A path that did not exist at `routed_at` gives `then = None`, so it counts as fresh; the commit that created it
touches it; the excerpt is not ACK-worded. Nothing checks that the commit repairs anything.
Arm: `fixed` (fresh-excerpt rule) and therefore `thisround`. Proposed fix (both parts needed):
 (i) refuse a keyed evidence path that is absent at `routed_at` (`then is None` -> `fixed_bad`). Closes the new-file route.
 (ii) the keyed evidence path must be named by the item's own spot-check text (a basename or path token), or the fixing commit's
 message must name the item id `R<n>.<m>`. Feasibility is unverified beyond a proxy: 32 of 51 items carry a path-like key
 (`.py/.md/.json/.sh/.stdout/.txt/.yml/.ts`; `receipts/feasibility-path-keys.stdout`); the other 19 rely on the commit-message
 rule.
Residual, measured: the same quotes appended to an existing file (`LOG.md`, probe `C1_CTL_FAB_TEXT_APPEND`) give
`agree=50/51`, total 1, from R53.5 `fixed-not-new`, which is a freshness artefact of my excerpt choice, not a barrier. (i)
alone does not close the route; (ii) is required.

**F2 — target defect, C1: R56.7 has no admissible evidence at BASE.** Its three keys (`no byte changed`, `D-CF1`,
`grew between`) hit only the round-56 spot-check (excluded by name), `.ufo/waves/round-46/w2/T46ReobsD.md` (SOFT, excluded
because it does not end with a key), and nothing else (`receipts/r56.7-keys.stdout`, command `git grep -n -i -F -e KEY BASE`).
Every control therefore shows `missing=1`, and no honest row for R56.7 can agree until a non-excluded lane file carries the
key text. Proposed fix: the freeze step asserts that every item key has at least one admissible BASE hit (this check would
have caught R56.7 before freeze), and R56.7's keys are re-chosen from text the fix will legitimately write (for example the
round-57 lesson's correction of the phrase).

**F3 — reporting defect, C1: `fixed=` counts rows that fail their own checks.** `C1_CTL_FAB` prints `fixed=50` with
`agree=12/51`, `fixed_bad=38`, `fixed_short=0`: `stat[status] += 1` runs before the evidence checks. This does not create a
PASS route (any fault makes `total>0`), but the verdict line overstates. Proposed fix: count `fixed`/`declined` only for
agreeing rows, or add `fixed_agree=`.

**F4 — weak agree arm, C1: a search-based do-nothing agrees on 42 of 51 rows.** `C1_CTL_FAB_SEARCH` (receipt
`c1-controls.stdout`) cites historical commits that touched unrelated lane files whose later text contains the key (for
example R50.1 cites `.ufo/evidence/round-51/coldread/reads/T51W2Read03.md` at commit `02ec217`). The counter's
`cannot_see` names semantic support; the size of this (42/51) argues for F1(ii) as the first repair, since the fixed
commit's stated purpose would then be checkable.

**F5 — counter defect, C2 `skill` arm is presence-only.** `C2_CTL_SKILLMAP` (receipt `c2-probe-skill-bogus-map.stdout`): a
gate row whose Verdict-map cell is `0 ok; 2 ok; 3 ok` gives `skill_row=1`. `skill_row_ok()` checks only that the whole
tokens 0, 2 and 3 appear. Proposed fix: the cell must carry the code names the counter already computes from its own
fixtures for exits 2 and 3 (`RECEIPT_REV_UNRESOLVABLE`, and `RECEIPT_REV_CONTENT_DRIFT` for exit 3), plus `PASS` for exit 0.

**F6 — no defect found, C2 mutants arm works as designed.** Hard-wired rows kill only M3 (`CTL_HARD`, mutants=1/3):
M1 and M2 act on the drift branch, which no hard-wired row reaches. `CTL_STACK` (the cheap honest-looking set) fails
on exactly those two. The genuine drift row in `CTL_REF` kills all three and passes. This confirms the mutants arm separates
hollow rows from real gate exercise.

**F7 — harness fault in my first C2 run (not a counter defect).** My first C2 rows had an invalid `source` field
(`'round-57 do-nothing control'`); `registry-check` rejects it (`rows[57].source must be <file>@<7-40 hex rev>:<line>`),
so the executed arm reported `rc=2 error` for every row, including the hard-wired ones. The counter reported that
correctly. Fixed in `ctl_c2.py` (`source` = `SKILL.md@<BASE>:1541`); all C2 numbers above come from the fixed script.

## Limits

- The C1 controls use a pinned scratch copy of the staged counter (the pin is the staged `defects.json` sha256). The L1 must
  still set the real pin and rerun; the `self=` values above are the scratch copy's.
- C1 liveness (a real, non-quoted fix set reaching PASS) is not shown here: no genuine repair set was in scope. The only
  C1 PASS I observed is F1's probe.
- `CTL_FAB_TEXT` and `CTL_FAB_TEXT_APPEND` are probes that write fabricated fixed-claims on purpose, to test the counter.
  They are not do-nothing controls and should not be taken as lane evidence.
- The C1 literal excerpt is a line-based window, not "the file's first 15-400 characters"; the excerpt is the first grep hit
  of an admissible file that contains the key, which is the closest mechanical reading of the brief.
- Not run: the counters' own selftests and mutant batteries (other seats' scope); the no-harm monitors; any check against
  a populated lane ledger.

## Proposed fixes, in order

1. C1 `fixed` arm: refuse keyed paths absent at `routed_at`; require the item id in the fixing commit message or the
   keyed path named by the item's spot-check text (F1). Re-run `CTL_FAB_TEXT` (must fail) and `CTL_FAB_TEXT_APPEND`.
2. C1 target: key admissibility check at freeze; re-key R56.7 (F2).
3. C1 reporting: count only agreeing rows into `fixed=`/`declined=` (F3).
4. C2 `skill` arm: require the exit-2/exit-3 code names and PASS in the verdict-map cell (F5). Re-run `CTL_SKILLMAP` (must fail).

## Receipts

`T57W1CritDoNothing-receipts/`: `c1-controls.stdout` (full C1 set, final scripts), `c2-controls.stdout` (full C2 set, final
scripts), `c1-probe-fab-text.stdout`, `c1-probe-fab-text-append.stdout`, `c2-probe-skill-bogus-map.stdout`,
`r56.7-keys.stdout`, `inputs.stdout` (staged sha256 values, lane HEAD), `feasibility-path-keys.stdout`, `scripts/ctl_c1.py`,
`scripts/ctl_c2.py`. Counter run form: `python3 <clone>/.ufo/evidence/round-57/c{1,2}/measure.py --lane <clone> --rev <rev>
--work <empty dir> --explain`.
