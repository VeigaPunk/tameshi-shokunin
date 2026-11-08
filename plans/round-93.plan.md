# Round 93 — frozen plan (tameshi, L1 TameshiR93, attempt 1)

Base `4a7e259b407d582d2010197f32d7524d6bed5370` (round-92 verifier spot-check tip).
Instrument revision **`855f0c1c59ee2af7f184d8de62d02cdd576eb94e`** — the C1 counter (rev A3,
single stray-verdict rule), on top of the pins commit `90ec4b33` and the driver commit
`69d377a0`. Battery driver of record: `.ufo/evidence/round-93/c1/controls-v93.py`, sha256
`400d8e0ffceadc3e9aa7d057ac16b5142f0f4b60626544133462b1067bc0da74`. This file is committed
on top of all three and freezes both claims; nothing below changes after any seat scores.

Fresh-start duty: tameshi's fresh start was round 91 (Amendment 62), so this is not a
fresh-start round. The round-92 non-author spot-check
(`corpus/lessons/round-92-verifier-spotcheck.md`) was read in full before declaring; its
routed defects 1-5 are each answered in § Records.

## Claim 1 (coverage) — the verdict-content reader

### R93-C1 — fourth attempt at certifying the round-90 fleet-gate mutation case

Surface: the case note `corpus/knowledge/mutation-case-fleet-sources-census.md` and the
fleet's own registry gate `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` at
fleet commit `f47ad6ba8d306f8125597401cb2ce45c1297a593` (read-only; the case re-executes it
under its own `selftest`). Spec copy `.ufo/evidence/round-93/c1/census-mutants.json`
(byte-identical to rounds 90-92, sha256 `ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290`).

Instrument: `.ufo/evidence/round-93/c1/measure-v93.py`, **sha256
`18903602aa040b7e258fd6c81491cfee4ea7bb0575784fe27e351587fe094c2d`** (self-pin normalised
digest `9a073d351dd23de2f61af95436e5cac1fa871193f7d52e0728553e9034cb99e2`, re-derivable
with the command in QUALITY 150). It differs from round 92's counter (frozen, never edited)
on exactly the properties round 92's own routed list demanded:

1. **Verdict content, not id shape (QUALITY 154).** A table is a verdict table only when
   its **header row** carries a `verdict` cell — the GFM table shape (S321: one header row
   and one delimiter row). Only rows inside that single table are keyed. An id-keyed table
   that asserts no verdict is not a verdict table and does not refuse the note; a second
   table carrying verdict tokens, under any header, does.
2. **Header from the header row only (QUALITY 155).** A data cell whose text is exactly
   `verdict` cannot create a second header.
3. **Decoy rejection (QUALITY 157).** `coverage` grades the **last** `corpus/README.md` row
   naming the note, so an appended denial defeats an earlier assertion; `source` requires a
   located quote of at most 25 words that **occurs in a committed source snapshot**, not an
   id+URL pair.
4. **No hand-copied constants (round-92 M5).** The spec and gate digests come from the
   committed `pins.json`, generated from git objects by `.ufo/evidence/round-93/c1/make-pins.py`;
   `make-pins.py --check` refuses (`PINS_DRIFT`) when a derived value disagrees.
5. **Fences are literal (S322).** A fenced block is skipped entirely; the `measured:` figure
   is read from block-level lines only. This is a **declared limit**, not an unstated hole.

Frozen predicate — the same condition as the counter's `ok = all(conj.values())` and its
receipt label `C1_R93_PASS=true`:

    selfpin ∧ pins ∧ spec ∧ pin ∧ green ∧ canary ∧ valid0 ∧ trivial0 ∧ inconclusive0 ∧
    unstable0 ∧ note ∧ verdict_tables ∧ ids ∧ mismatched0 ∧ figure ∧ witnessed ∧
    source ∧ coverage ∧ n_min

Counting command (frozen):

    python3 -I .ufo/evidence/round-93/c1/measure-v93.py --repo <lane> --rev REV --work <empty dir>

Additional frozen condition (same round): the committed control battery

    python3 -I .ufo/evidence/round-93/c1/controls-v93.py --lane <lane> \
      --rev 855f0c1c59ee2af7f184d8de62d02cdd576eb94e \
      --base 4a7e259b407d582d2010197f32d7524d6bed5370 \
      --work <empty dir> --outdir <dir> --jobs 6

prints `C1_CONTROLS states=35 matched=35 mismatches=0 missing=0`, exit 0, with the receipts
committed under `.ufo/evidence/round-93/pre-freeze/controls/`. The summary is derived from
the receipts on disk (QUALITY 152) and every pre-registered name must have a receipt; a
missing receipt is a `MISSING` row and fails the run.

**Claim wording (the sentence the closure measures):** at the instrument revision the
committed note yields `C1_R93_PASS=true`, exit 0, with `verdict_tables=1 badrows=0
mismatched=0`; each of the three positive states `pos-real`, `pos-honest-a13`,
`pos-honest-verdict-cell` yields `C1_R93_PASS=true`, exit 0; and each of the twenty-three
hostile states named in § Controls yields `C1_R93_PASS=false`, exit 1, with **the conjunct
named for that state** false. No other state is claimed.

Before (do-nothing): at base `4a7e259b` the round-93 spec path does not exist, so the
counter refuses at setup — `C1_SETUP spec-absent-at-rev`, exit 2 (`nowork-base` receipt).

Kill rule (any one kills C1):
- (a) an honest note state — the committed note, the committed note with an id-keyed table
  that asserts no verdict, or the committed note with a data cell equal to `verdict` — is
  refused by a rule stated in this plan;
- (b) one of the twenty-three named states fails to reach `C1_R93_PASS=false`/exit 1 with its
  named conjunct false;
- (c) the counter blob at `855f0c1c` differs from the stated sha256, or any receipt was
  produced by bytes other than that counter and the driver at `69d377a0`;
- (d) a pre-registered control name has no receipt, or its receipt's stable lines cannot be
  reproduced, or the driver's summary counts a state it did not write.

Declared limits (not kills — the plan and the instrument name the same set, QUALITY 156):
- a fenced block is literal text (S322): a fenced inverted table or a fenced `measured:`
  line is not keyed and does not refuse, and the figure is the block-level one;
- a table with no `verdict` cell in its header row is not a verdict table (S321): an
  id-keyed table that asserts no verdict is never refused;
- a `verdict` cell outside the header row is a data cell (QUALITY 155);
- a verdict word in prose with fewer than two pipes on the line is not a table row;
- a cell containing an escaped `\|` is one cell (S321), so it does not shift the columns;
- the counter certifies the twelve cells, not how they were obtained: a note copying the
  predictions carries the same cells;
- `green`, `canary` and `unstable0` are declarations where C2 says so: the gate bytes are
  pinned, so no committed lane state can falsify the two-run stability conjunct.

## Claim 2 (calibration) — auditable conjunct disposition

### R93-C2 — every conjunct falsifiable by a committed state, or declared with its reason

Surface: the **self-assessment** the counter's conjunct list makes about what it measures,
against the committed battery receipts. Round 92's matrix left five conjuncts survivable
and unstated (M8 → QUALITY 158); the round-92 spot-check routed the same defect as
R92-DEF-3.

Instrument: `tools/conjunct-disposition.py`, sha256
`1b1c6895ebf1d167900113030beebb071d04ed5e8bbb46988176c82b26764a9a`, and the manifest
`tools/conjunct-disposition.json`. The checker reads the counter's own `--conjuncts` key
list at a named revision, then requires for every key either a `state` row whose committed
receipt shows that conjunct **false** (or the named `C1_SETUP` token), or an
`unfalsifiable` row whose reason is at least 40 characters and names the seal/pin mechanism
that forbids a falsifier. A manifest key the counter does not print is a finding (a stale
self-assessment).

Frozen predicate:

    DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0      (exit 0)
    DISPOSITION_SELFTEST: 6/6 pass                                     (exit 0)

Counting command (frozen):

    python3 -I tools/conjunct-disposition.py --lane <lane> --rev REV
    python3 -I tools/conjunct-disposition.py --selftest

Before (do-nothing): at base `4a7e259b` neither the manifest nor the checker exists, so the
command refuses at setup — `DISPOSITION_SETUP counter-absent-at-rev`, exit 2 (the checker
is run at base with the manifest path absent; receipt in § Controls).

Kill rule (any one kills C2):
- (a) the checker prints `findings=0` while a conjunct key the counter prints has no row, a
  row names an unknown key, a `state` row's receipt does not move its conjunct, or an
  `unfalsifiable` reason is shorter than 40 characters or names no mechanism;
- (b) fewer than 17 of the 19 rows carry a `state` (a row may become `unfalsifiable` only
  with a reason of the second kind, and every such row is counted and printed);
- (c) the selftest cannot fail: a case that must produce a finding produces none, or the
  clean case produces one;
- (d) the checker or manifest blob at the named revision differs from the sha256 named here.

## Controls (produced before the freeze, committed with it)

Driver `.ufo/evidence/round-93/c1/controls-v93.py` (rev `69d377a0`, sha256
`400d8e0f…da74`); receipts and summary under
`.ufo/evidence/round-93/pre-freeze/controls/`. Every state is a `git clone --shared` of the
lane at `855f0c1c`, checked out detached, one edit committed under the fixture identity
`r93-fixture`, and read by the counter blob extracted from that revision (never the working
tree).

Positive states (the claim's honest side):

| state | edit on the honest state | expected |
|---|---|---|
| `pos-real` | none (the committed note, registry, lesson, README) | `C1_R93_PASS=true`, exit 0 |
| `pos-fixture` | a synthetic 12-row honest note | `C1_R93_PASS=true`, exit 0 |
| `pos-honest-a13` | the note's §2b impact table reformatted so its ids are their own cells — the round-92 kill | `C1_R93_PASS=true`, exit 0 |
| `pos-honest-verdict-cell` | the note plus a non-verdict table holding a data cell exactly `verdict` and a bolded id | `C1_R93_PASS=true`, exit 0 |

Hostile states (one named conjunct each):

| state | edit | expected |
|---|---|---|
| `hidden-c001` | appended second verdict table `C001`-`C012` | `verdict_tables=false`, exit 1 |
| `hidden-x` | appended second verdict table `X1`-`X12` | `verdict_tables=false`, exit 1 |
| `renamed-result` | appended id-keyed table with header `result` and two verdict tokens | `ids=false`, exit 1 |
| `pseudo-row` | a bare pipe line `\| C02 \| … \| KILLED \|` with no delimiter row | `ids=false`, exit 1 |
| `position` | C12's verdict token moved out of the verdict column | `ids=false`, exit 1 |
| `drop-c12` | the verdict table with C12 removed | `ids=false`, exit 1 |
| `dup-row` | a duplicate C02 row with the opposite verdict | `ids=false`, exit 1 |
| `inverted` | the twelve verdicts inverted | `mismatched0=false`, exit 1 |
| `note-absent` | the note deleted | `note=false`, exit 1 |
| `pins-mutated` | `pins.json` `gate_sha256` zeroed | `pins=false`, exit 1 |
| `spec-shape` | a duplicate mutant id | `spec=false`, exit 1 |
| `short-spec` | one mutant removed (11 mutants) | `n_min=false`, exit 1 |
| `pin-mismatch` | the spec's gate sha256 zeroed | `pin=false`, exit 1 |
| `noop-mutant` | one mutant `new` == `old` | `valid0=false`, exit 1 |
| `syntax-mutant` | one mutant `new` is a bash syntax error | `valid0=false`, exit 1 |
| `trivial-mutant` | one mutant's `new` breaks `validate` | `trivial0=false`, exit 1 |
| `timeout` | `timeout_s` 0.001 — the M19 state round 92 lacked | `inconclusive0=false`, exit 1 |
| `figure` | `measured: 6/12 killed` | `figure=false`, exit 1 |
| `witness-same` | C02's witness edited to agree with pristine | `witnessed=false`, exit 1 |
| `source-noquote` | S322's located quote removed from the lesson | `source=false`, exit 1 |
| `source-status` | S321's status `mined` → `queued` | `source=false`, exit 1 |
| `coverage-denial` | a README row appended naming the note and denying it | `coverage=false`, exit 1 |
| `coverage-absent` | every README line naming the note removed | `coverage=false`, exit 1 |

Setup controls: `nowork-base` (counter at base `4a7e259b`) → `C1_SETUP spec-absent-at-rev`,
exit 2; `selfpin-edit` (the counter with one appended comment) → `C1_SETUP self-pin-mismatch`,
exit 2; `replace-honest` (honest note committed + `git replace` to a false note) →
`C1_SETUP replace-refs-present`, exit 2.

Removal mutants (a state the frozen counter refuses, and removing one rule turns it into the
cheat — QUALITY 149). D01-D04 remove exactly one rule each; D05 removes a named pair, said
so here:

| mutant | rule removed | state | expected |
|---|---|---|---|
| `D01` | the stray-verdict scan (one rule, one place) | `renamed-result` | `C1_R93_PASS=true` (the cheat returns) |
| `D02` | the denial-token list emptied | `coverage-denial` | `C1_R93_PASS=true` |
| `D03` | the `pins` conjunct forced true | `pins-mutated` | `C1_R93_PASS=true` |
| `D04` | the `figure` check forced true | `figure` | `C1_R93_PASS=true` |
| `D05` | the table-count rule **and** the out-of-set rule **and** the id-set equality (a named triple) | `hidden-c001` | `C1_R93_PASS=true` |

Mutant counters are studied with the `SELF_SHA256` line recomputed for the edited bytes (a
mutation study, as in round 92); the frozen bytes stay pinned and unedited.

## Wave

One v1 wave `r93-w1`, 12 seats: executor 3, scribe 1, scout 2, reviewer 2, critic 1,
mutation-tester 1, sentinel 1, connector 1. Attack seats by the policy's role set
(reviewer, critic, mutation-tester, labrat) = 4/12 = 33 %; counting sentinel and connector
as adversarial seats too it is 6/12 = 50 %. The L1 holds the planner seat (the
validator refuses `planner`). Items: independent reproduction of the twelve verdicts outside
the counter; no-harm sweeps at base and at the instrument revision; the battery replayed from
committed bytes; the C2 manifest audited row by row; the note's round-93 status block; S321
and S322 re-fetched independently; a parser-premise audit against the real note; a code
review of the reader; a freeze-conformance review; a kill attempt under rule (a) on the
honest-note side and under rule (b) on the hostile side; a mutation matrix over the reader; a
safety audit of both drivers; and the sibling-overlap scan that QUALITY 154/155/157 class
needs (does any existing lane tool already implement a verdict-content table reader?). No
residual call is planned.

## Assimilation and considerthese

Assimilation: none — no staged `merge/tameshi/` theme serves a table-shape reader; the
statement is recorded in the report's Sources & frontier section, which is permitted.
considerthese: `considerthese/2026-11-07.md` idea 5 (receipt write safety) is implemented
this round as the driver's `receipt_path()` (`<name>.rerun-<n>.out`, never overwrite) with
its receipt as evidence; `hardening-lint.py` (idea 1) is re-run over the new counter.

## Records (r92 routed defects)

- **R92-DEF-1 (M5, stale wave-spec constants):** `.ufo/waves/round-93/make-spec.py` derives
  every constant from `git cat-file` at the named revisions and **refuses** (`SPEC_CONST_DRIFT`)
  when a value disagrees with `plans/round-93.plan.md`; the counter's own digests come from
  `pins.json`, not from a hand-copied hex. Receipts: the generator's own output plus the
  `pins` conjunct.
- **R92-DEF-2 (M4, receipt overwrite):** `controls-v93.py` writes `<name>.rerun-<n>.out`
  when a receipt already exists; its first run and its re-run are both citable. Demonstrated
  by running the battery twice into one outdir (receipts `C1-summary.txt` plus the `.rerun-1`
  files).
- **R92-DEF-3 (M8, incomplete conjunct coverage):** answered by C2 and by the `timeout`
  state (the M19 falsifier round 92 proved killable and did not build).
- **R92-DEF-4 (record mechanics):** the summary is derived from receipts on disk and a
  missing receipt is a `MISSING` row (M1); the battery counts what it declares.
- **R92-DEF-5 (successor property):** QUALITY 154/155/157 are implemented in the reader and
  each has a positive and a hostile state (`pos-honest-a13`, `pos-honest-verdict-cell`,
  `hidden-c001`, `renamed-result`, `coverage-denial`).

## Amendments (post-wave, pre-file)

Appended here if a wave artifact falsifies this record's own mechanics, in the round-92 A1-A5
form: the claim, predicate and state expectations never change; only statements about the
record are corrected, each citing the artifact that falsified it.
Both claims' predicates, counters and state expectations are unchanged by A1-A6. What follows
narrows the *wording* to what the instruments enforce, each amendment citing the wave artifact
that falsified the wider reading (§8 of the round contract; Amendment 59).

### A1 — `coverage` is fence-blind (R93R1 finding 2; `R93R1.md`, `R93R1-probe4.py`)

The §Declared limits sentence "a fenced block is literal text (S322): … not keyed" is true of
the *note reader* and false of the `coverage` conjunct: that scan reads every line of
`corpus/README.md` whose text names the note's path, fenced or not, and takes the last one.
Measured: a fenced README row appended after a committed denial sets `coverage=true` (false
green), and a fenced denial after an assertion sets it false (false red). Narrowed wording:
**`coverage` = the last *line* in `corpus/README.md` that names the note's path, without the
fence rule; a fenced README row is therefore keyed by `coverage`.** Routed to round 94: run the
README scan through `block_lines` and require the path as its own cell, not a substring.

### A2 — the width rules are stricter than GFM and unstated (R93R1 finding 1, R93C1 finding 1, R93S1 observation, R93M1 §4.7)

Two width rules exist and neither is named in §Declared limits. (i) `tables()` returns no
delimiter row, so the check `len(delim) != len(header)` compares the header to the first *data*
row; a delimiter row with the wrong cell count is never checked, so a GFM-invalid table is
still keyed (`R93R1` probe; `R93C1-A5`). (ii) Every verdict-table data row whose cell count
differs from the header refuses, which is stricter than S321's remainder-row allowance
("The header row must match the delimiter row in the number of cells." is the delimiter rule;
GFM pads or truncates remainder rows — R93S1, `s321.txt:4585-4587`). Narrowed wording: **the
reader certifies the twelve cells and the named states; it does not certify that the table is a
valid GFM table, and it refuses a data row of non-header width.** Routed to round 94: return
the delimiter cells from `tables()` and add a `delim` finding; decide pad/truncate vs refuse.

### A3 — the seal's root of trust is the lane's own spec (R93SN1 F1, `R93SN1-probe18.log`)

§Declared limits says "the gate bytes are pinned, so no committed lane state can falsify the
two-run stability conjunct". R93SN1 falsified the wider reading: `pin` compares the spec's
declared digest to the blob the same spec names, and `pins` compares the derived values to a
`pins.json` the lane also commits, so one lane commit that repoints `census-mutants.json` and
regenerates `pins.json` makes the counter materialise and **execute a foreign gate** while
printing `pin=true pins=true green=true canary=true` (`R93SN1-probe18.log`, control arm
marker absent). The frozen certificate is **revision-bound**: it is true of the spec bytes at
`855f0c1c`, and the counter blob is bound by kill rule (c). Narrowed wording: **the certificate
certifies the fleet gate only at the instrument revision; the seal is self-consistent, not
externally anchored.** Routed to round 94: anchor `gate_commit`/`gate_sha256` in the counter's
own self-pinned bytes and `die` (never report a conjunct false) when the derived identity
disagrees.

### A4 — C2's "names the seal" test is a substring match (R93SN1 F8, `pre-freeze/c2-cheat-all-unfalsifiable.out`)

The checker accepts an `unfalsifiable` row when the reason is >= 40 characters and contains one
of `pin`, `sealed`, `seal`, `gate bytes`, `GIT_`, `pinned`, `replace`. A manifest whose 19 rows
all say "the pin forbids it" therefore prints `findings=0` — measured, committed at
`pre-freeze/c2-cheat-all-unfalsifiable.out` (`rows=19 falsifiable=0 unfalsifiable=19 findings=0`,
exit 0). C2's wording names the counts (`falsifiable=17`), and kill rule (b) rejects that
manifest, so C2 is not falsified; but the checker's *rule* is weaker than "names the mechanism
that forbids the falsifier". Narrowed wording: **C2 audits conjunct-level falsifiability and the
manifest's counts; it does not by itself reject a zero-state manifest.** Routed to round 94:
`--min-falsifiable N` and a reason test that names a state or a pin digest, not a word.

### A5 — C2's `canary` reason is scoped to the frozen spec (R93SN1 F1)

The manifest's `canary` row says "no committed lane state can make it false". Under A3's
repointed spec that is false (a foreign gate can swallow the inserted `exit 97`). The
declaration holds for the gate bytes the frozen spec names, which is what the battery measured
twice (`timeout` state, `canary=true` both runs). The manifest is a frozen artifact and is not
edited; the narrowing is recorded here and routed to round 94 with A3's remediation.

### A6 — record corrections (R93R2 F1-F5)

- **F1/F2 (receipt provenance):** per-state receipts carry no `CONTROL_INSTRUMENT sha256=` line
  (the driver prints it once to its own stdout) and the fixture clone revisions are not in the
  lane object store, so byte provenance is textual. Mitigation, measured: R93E3 re-ran the
  battery from committed bytes into one outdir twice — `C1_CONTROLS states=35 matched=35
  mismatches=0 missing=0` both times, stable lines identical, and the instrument digest
  independently re-derived from the working tree and from the blob at `855f0c1c`
  (`R93E3.md`). Residual limit: no per-receipt instrument line.
- **F3 (freeze_note wording):** `claims.json` `freeze_note` calls the pins commit and the driver
  "ancestors" of the instrument revision; the graph has `855f0c1c` (counter) then `69d377a0`
  (driver), so the driver is its **descendant**. The three named revisions are correct; the
  word is not. Recorded, not edited (frozen artifact).
- **F4 (green):** §Declared limits calls `green`, `canary` and `unstable0` "declarations"; `green`
  has a falsifying committed state (`timeout`, `green=false`) and C2's manifest names it. The
  sentence is corrected to: `canary` and `unstable0` are declarations (subject to A5), `green`
  is falsifiable.
- **F5 (C2 `--rev`):** the C2 counting command reproduces at any revision where both the counter
  and the manifest exist (`9bf52b03` onward); at `855f0c1c` the manifest is absent and the
  checker refuses `DISPOSITION_SETUP manifest-absent-at-rev`. The frozen predicate is measured at
  the landing revision, not at the instrument revision.
- **M1 rule-granularity:** QUALITY 158 is satisfied at *conjunct* granularity (all 19 keys move
  or are declared) and not at *rule* granularity (8 reader rules have no discriminating state:
  source's occurrence half, both width halves, position, figure-exactly-one, verdict-column
  count, fence, spec count). C2 audits conjuncts; the rule-level gap is routed to round 94 and
  recorded in the lesson's `## Mistakes`.
