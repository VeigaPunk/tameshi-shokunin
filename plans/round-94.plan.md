# Round 94 — frozen plan (tameshi, L1 TameshiR94, attempt 1)

Base `a8f0e14bd400002324793d82030431696435d9a7` (round-93 verifier spot-check tip).
THIS FILE IS THE FREEZE. Nothing below changes after any seat scores.

Instrument revision: `7084358c732ebe1334c2eb9a352c3ed96b547f7c` (the instruments commit directly above this freeze). The counter bytes are
`.ufo/evidence/round-94/c1/measure-v94.py`, sha256 recorded in `claims.json`;
the driver bytes are `.ufo/evidence/round-94/c1/controls-v94.py`, sha256
recorded in `claims.json`.

Fresh-start duty: tameshi's fresh start was round 91. This is not a
fresh-start round. The round-93 non-author spot-check
(`corpus/lessons/round-93-verifier-spotcheck.md`) was read in full before
declaring; its 8 routed items are each answered in § Controls and § Records.
The stagnation nudge does not fire (round 93 entered the
`conjunct-disposition audit` capability inside window N=2), so the lowest
scored axis is calibration (8).

## Claim 1 (coverage) — the round-93 reader's routed fixes

### R94-C1 — fifth attempt at certifying the round-90 fleet-gate mutation case

Surface: the case note `corpus/knowledge/mutation-case-fleet-sources-census.md`
and the fleet's own registry gate `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
at fleet commit `f47ad6ba8d306f8125597401cb2ce45c1297a593` (read-only; the case
re-executes it under its own `selftest`). Spec copy
`.ufo/evidence/round-94/c1/census-mutants.json` (byte-identical to round 93,
sha256 `ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290`).

Instrument: `.ufo/evidence/round-94/c1/measure-v94.py`. It differs from round
93's counter (frozen, never edited) on exactly the properties round 93's own
routed list demanded:

1. **Externally anchored gate identity (QUALITY 163; routed item 3 / A3).**
   `GATE_COMMIT` and `GATE_SHA256` are constants in the counter's own
   self-pinned bytes. If the spec-derived `gate_commit`/`gate_sha256`
   disagree the counter `die`s with `C1_SETUP gate-identity-mismatch` (exit 2)
   before materializing or executing any gate — a lane commit that repoints
   the spec and regenerates `pins.json` can no longer make it execute a
   foreign gate while reporting `pin=true pins=true` (R93SN1 F1).
2. **Fence-aware coverage, path as its own cell (QUALITY 164; routed item 1 /
   A1).** The `coverage` scan runs through `block_lines` (S322: fenced rows
   are literal) and requires the note path as the first backtick-token of one
   cell of a pipe row, not a substring match.
3. **Real delimiter-width rule and decided remainder policy (QUALITY 165;
   routed item 2 / A2).** `tables()` returns the delimiter cells; a delimiter
   whose width differs from the header adds a `delim:` finding (`ids=false`).
   A data row whose cell count differs from the header is a GFM-legal
   remainder row when its single verdict token sits in the verdict column
   (S321: missing cells are empty, excess ignored) and is padded/truncated;
   it refuses with `width:` only when the verdict-bearing cells are ambiguous.
4. **Fixture-premise assertion (routed item 5 / M1).** The driver's
   `pos-honest-a13` fixture asserts, before any clone is committed, that the
   transformed note still parses to twelve verdict cells. A file-wide replace
   that corrupts the certified table can no longer pose as an honest control.
5. **Sealed driver environment (routed item 7 / M10).** Every `git` call the
   driver makes carries `GIT_NO_REPLACE_OBJECTS=1` and a scrubbed `GIT_*`
   (QUALITY 27); `--canary-selftest` proves an exported `GIT_DIR` cannot move
   a canary repository's HEAD.

Frozen predicate — the same condition as the counter's `ok = all(conj.values())`
and its receipt label `C1_R94_PASS=true`:

    selfpin ∧ pins ∧ spec ∧ pin ∧ green ∧ canary ∧ valid0 ∧ trivial0 ∧ inconclusive0 ∧
    unstable0 ∧ note ∧ verdict_tables ∧ ids ∧ mismatched0 ∧ figure ∧ witnessed ∧
    source ∧ coverage ∧ n_min

Counting command (frozen):

    python3 -I .ufo/evidence/round-94/c1/measure-v94.py --repo <lane> --rev REV --work <empty dir>

Additional frozen condition (same round): the committed control battery

    python3 -I .ufo/evidence/round-94/c1/controls-v94.py --lane <lane> \
      --rev <INSTRUMENT> --base a8f0e14bd400002324793d82030431696435d9a7 \
      --work <empty dir> --outdir <dir> --jobs 6

prints `C1_CONTROLS states=45 matched=45 mismatches=0 missing=0`, exit 0, with
the receipts committed under `.ufo/evidence/round-94/pre-freeze/controls/`.
The summary is derived from the receipts on disk (QUALITY 152) and every
pre-registered name must have a receipt; a missing receipt is a `MISSING` row
and fails the run. The driver's own canary:

    python3 -I .ufo/evidence/round-94/c1/controls-v94.py --canary-selftest
    → CANARY_SELFTEST: PASS, exit 0

**Claim wording (the sentence the closure measures):** at the instrument
revision the committed note yields `C1_R94_PASS=true`, exit 0, with
`verdict_tables=1 badrows=0 mismatched=0`; each of the six positive states
`pos-real`, `pos-fixture`, `pos-honest-a13`, `pos-honest-verdict-cell`,
`pos-fenced-hidden`, `pos-coverage-fenced-denial` yields `C1_R94_PASS=true`,
exit 0; and each of the thirty hostile states named in § Controls yields
`C1_R94_PASS=false`, exit 1, with **the conjunct named for that state** false.
No other state is claimed.

Before (do-nothing): at base `a8f0e14b` the round-94 spec path does not exist,
so the counter refuses at setup — `C1_SETUP spec-absent-at-rev`, exit 2
(`nowork-base` receipt).

Kill rule (any one kills C1):
- (a) an honest note state — the committed note, the committed note with an
  id-keyed table that asserts no verdict, the committed note with a data cell
  equal to `verdict`, or the committed note with a fenced inverted table — is
  refused by a rule stated in this plan;
- (b) one of the thirty named states fails to reach `C1_R94_PASS=false`/
  exit 1 with its named conjunct false;
- (c) the counter blob at the instrument revision differs from the stated
  sha256, or any receipt was produced by bytes other than that counter and the
  driver at the instrument revision;
- (d) a pre-registered control name has no receipt, or its receipt's stable
  lines cannot be reproduced, or the driver's summary counts a state it did not
  write;
- (e) a foreign gate committed by a lane commit (spec slug repointed + pins
  regenerated) is ever executed or ever reported with `pin=true` instead of
  refusing at setup (the C3 failure mode this round exists to close).

Declared limits (not kills — the plan and the instrument name the same set,
QUALITY 156):
- a fenced block is literal text (S322): a fenced inverted table or a fenced
  `measured:` line is not keyed and does not refuse, and the figure is the
  block-level one;
- a table with no `verdict` cell in its header row is not a verdict table
  (S321): an id-keyed table that asserts no verdict is never refused;
- a `verdict` cell outside the header row is a data cell (QUALITY 155);
- a verdict word in prose with fewer than two pipes on the line is not a table row;
- a cell containing an escaped `\|` is one cell (S321), so it does not shift
  the columns;
- the counter certifies the twelve cells, not how they were obtained: a note
  copying the predictions carries the same cells;
- `canary` and `unstable0` are declarations where C2 says so: the gate bytes are
  now anchored by `GATE_COMMIT`/`GATE_SHA256` in the self-pinned counter bytes,
  so no committed lane state can falsify the two-run stability conjunct
  (subject to (e) above);
- a fully-correct fence table plus a second fenced table that ALSO passes is
  not a refusal: the fence limit is a limit.

## Claim 2 (calibration) — auditable conjunct disposition with a state-named reason test

### R94-C2 — every conjunct falsifiable by a committed state, or declared with a
state/digest-naming reason, and never below the frozen falsifiable floor

Surface: the **self-assessment** the counter's conjunct list makes about what
it measures, against the committed battery receipts. Round 93's checker
accepted any unfalsifiable reason carrying a mechanism word ("the pin
forbids it"); its own cheat (a 19× all-unfalsifiable manifest) printed
`findings=0` (A4 / QUALITY 160). This round's checker requires a battery
state or a pin digest in the reason, and the round freezes a minimum
falsifiable count.

Instrument: `.ufo/evidence/round-94/conjunct-disposition-v94.py` and the
manifest `.ufo/evidence/round-94/conjunct-disposition.json`. The checker reads
the counter's own `--conjuncts` key list at a named revision, then requires
for every key either a `state` row whose committed receipt shows that conjunct
**false** (or the named `C1_SETUP` token), or an `unfalsifiable` row whose
reason is at least 40 characters, names the seal/pin mechanism, **and** names
a concrete battery state (e.g. `state timeout`) or a pin digest (a 64-hex
digest, a 12+-hex fragment, `GATE_COMMIT`/`GATE_SHA256`/`SPEC_PATH`/`PINS_PATH`).
A manifest key the counter does not print is a finding (a stale
self-assessment).

Frozen predicate:

    DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0      (exit 0)
    DISPOSITION --min-falsifiable 17  same output                      (exit 0)
    DISPOSITION_SELFTEST: 8/8 pass                                     (exit 0)

Counting command (frozen):

    python3 -I .ufo/evidence/round-94/conjunct-disposition-v94.py --lane <lane> --rev REV --min-falsifiable 17
    python3 -I .ufo/evidence/round-94/conjunct-disposition-v94.py --selftest

Before (do-nothing): at base `a8f0e14b` neither the manifest nor the checker
exists, so the command refuses at setup — `DISPOSITION_SETUP
counter-absent-at-rev`, exit 2 (the checker is run at base with the manifest
path absent; receipt in § Controls).

Kill rule (any one kills C2):
- (a) the checker prints `findings=0` while a conjunct key the counter prints
  has no row, a row names an unknown key, a `state` row's receipt does not move
  its conjunct, or an `unfalsifiable` reason is shorter than 40 characters,
  names no mechanism, or names no battery state and no pin digest;
- (b) fewer than 17 of the 19 rows carry a `state` (a row may become
  `unfalsifiable` only with a state/digest-naming reason, and every such row
  is counted and printed);
- (c) the selftest cannot fail: a case that must produce a finding (including
  the A4 mechanism-word cheat) produces none, or the clean case produces one;
- (d) the checker or manifest blob at the named revision differs from the
  sha256 named here.

## Controls (produced before the freeze, committed with it)

Driver `.ufo/evidence/round-94/c1/controls-v94.py` (instrument revision);
receipts and summary under `.ufo/evidence/round-94/pre-freeze/controls/`.
Every state is a `git clone --shared` of the lane at the instrument revision,
checked out detached, one edit committed under the fixture identity
`r94-fixture`, and read by the counter blob extracted from that revision
(never the working tree). `--only` is run only by seats for a single state.

Positive states (the claim's honest side):

| state | edit on the honest state | expected |
|---|---|---|
| `pos-real` | none (the committed note, registry, lesson, README) | `C1_R94_PASS=true`, exit 0 |
| `pos-fixture` | a synthetic 12-row honest note | `C1_R94_PASS=true`, exit 0 |
| `pos-honest-a13` | the note's §2b impact table reformatted so its ids are their own cells — the round-92 kill | `C1_R94_PASS=true`, exit 0 |
| `pos-honest-verdict-cell` | the note plus a non-verdict table holding a data cell exactly `verdict` and a bolded id | `C1_R94_PASS=true`, exit 0 |
| `pos-fenced-hidden` | the real note plus a fenced inverted table (12 rows) | `C1_R94_PASS=true`, exit 0 (S322 fence is a limit, not a refusal) |
| `pos-coverage-fenced-denial` | a fenced README denial row after the committed assertion | `C1_R94_PASS=true`, exit 0 (A1 fix) |

Hostile states (one named conjunct each; 30 states named here, plus the gate-foreign setup control = 31 named non-positive states, = the frozen count):

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
| `sharp-source-wrongquote` | S322's quote replaced by a quote not in the snapshot | `source=false`, exit 1 |
| `sharp-width-lastrow` | last data row wider with two verdict tokens | `ids=false`, exit 1 |
| `sharp-width-firstrow` | first data row wider with two verdict tokens | `ids=false`, exit 1 |
| `sharp-position-nodup` | verdict token moved out of the verdict column, no duplicate | `ids=false`, exit 1 |
| `sharp-two-verdict-cols` | header with two `verdict` columns | `ids=false`, exit 1 |
| `sharp-figure-two` | two `measured:` lines | `figure=false`, exit 1 |
| `sharp-delim-5-4` | 5-cell header over a 3-cell delimiter | `ids=false`, exit 1 (A2) |
| `gate-foreign` | spec `gate.path` repointed to `scripts/shokunin-watchdog.sh` with its real sha | setup refusal `gate-identity-mismatch`, exit 2 (A3) |

Setup controls: `nowork-base` (counter at base `a8f0e14b`) → `C1_SETUP spec-absent-at-rev`,
exit 2; `selfpin-edit` (the counter with one appended comment) → `C1_SETUP self-pin-mismatch`,
exit 2; `replace-honest` (honest note committed + `git replace` to a false note) →
`C1_SETUP replace-refs-present`, exit 2.

Removal mutants (a state the frozen counter refuses, and removing one rule turns it into the
cheat — QUALITY 149). D01-D04 remove exactly one rule each; D05 removes a named pair, said
so here:

| mutant | rule removed | state | expected |
|---|---|---|---|
| `D01` | the stray-verdict scan (one rule, one place) | `renamed-result` | `C1_R94_PASS=true` (the cheat returns) |
| `D02` | the denial-token list emptied | `coverage-denial` | `C1_R94_PASS=true` |
| `D03` | the `pins` conjunct forced true | `pins-mutated` | `C1_R94_PASS=true` |
| `D04` | the `figure` check forced true | `figure` | `C1_R94_PASS=true` |
| `D05` | the table-count rule **and** the out-of-set rule **and** the id-set equality (a named triple) | `hidden-c001` | `C1_R94_PASS=true` |

Mutant counters are studied with the `SELF_SHA256` line recomputed for the edited bytes (a
mutation study, as in round 92); the frozen bytes stay pinned and unedited.

## Wave

One v1 wave `r94-w1`, 14 seats: executor 3, scribe 1, scout 2, reviewer 2,
critic 1, mutation-tester 1, sentinel 1, connector 1 + security-reviewer 1 +
simplifier 1 (the last two are adversarial/bounding seats the policy's
≥25% attack share counts via sentinel/connector; the wave total stays inside
band 8–16). Attack seats by the policy's role set (reviewer, critic,
mutation-tester, labrat) = 4/14 = 29%; counting sentinel, connector,
security-reviewer and simplifier as adversarial seats too it is 8/14 = 57%.
The L1 holds the planner seat (the validator refuses `planner`). Items:
independent reproduction of the twelve verdicts outside the counter; no-harm
sweeps at base and at the instrument revision; the battery replayed from
committed bytes; the C2 manifest audited row by row under the new reason test;
the note's round-94 status block; S321/S322/S320 re-fetched independently;
a parser-premise audit against the real note (delim + remainder + fence); a
code review of the reader; a freeze-conformance review; a kill attempt under
rule (a) on the honest-note side and under rule (b) on the hostile side;
a kill attempt under rule (e) (the foreign-gate swap); a mutation matrix over
the reader including the eight sharp rules; a safety audit of both drivers
(receipt guard, sealed env, canary); and the sibling-overlap scan that QUALITY
163-166 class needs (does any existing lane tool already anchor a gate identity
in self-pinned bytes?). No residual call is planned.

## Assimilation and considerthese

Assimilation: none — no staged `merge/tameshi/` theme serves a table-shape
reader; the statement is recorded in the report's Sources & frontier section,
which is permitted.
considerthese: `considerthese/2026-11-07.md` idea 5 (receipt write safety) is
implemented this round as the driver's `write_receipt()` (`O_NOFOLLOW`, never
overwrite) with its receipt as evidence; idea 1 (hardening lint) is re-run over
the new counter and the new driver. Idea 3 (same-shape bet alarm) is applied
as a Gate rejection candidate (see the lesson).

## Records (r93 routed defects)

- **R93-A1 (M6 fence-blind coverage):** the README scan runs through
  `block_lines` and requires the path as its own cell (QUALITY 164). Positive
  `pos-coverage-fenced-denial` and hostile `coverage-denial` are both in the
  battery; the fence test is the state the probe4 case built.
- **R93-A2 (M7 width):** `tables()` returns the delimiter cells; a
  `delim:` finding is added (QUALITY 165); the remainder-row policy is
  pad/truncate when the single verdict token sits in the verdict column,
  refuse when it is ambiguous. `sharp-delim-5-4`, `sharp-width-firstrow` and
  `sharp-width-lastrow` discriminate both halves.
- **R93-A3 (M5 HIGH):** `GATE_COMMIT`/`GATE_SHA256` constants in the
  self-pinned bytes; the counter `die`s with `gate-identity-mismatch` before
  any gate is executed (QUALITY 163). `gate-foreign` is its battery state.
- **R93-A4 (C2 substring test):** the reason must name a battery state or a
  pin digest; `--min-falsifiable 17` is part of the frozen predicate, and the
  selftest's new 8th case rejects the mechanism-word cheat.
- **R93-M1 (fixture premise):** the battery asserts `pos-honest-a13` parses
  to twelve cells before committing the fixture (QUALITY 162, applied).
- **R93-M9 (receipt guard):** `receipt_path()` uses `lexists` (never follows a
  dangling symlink) and `write_receipt()` opens with `O_EXCL | O_NOFOLLOW`;
  the outdir summary is also never overwritten, and a planted
  `<name>.rerun-9.out` no longer outranks a fresh receipt (the lowest unused
  index wins).
- **R93-M10 (driver env):** every `git` call the driver makes carries the
  sealed environment; `--canary-selftest` prints `PASS`.
- **R93-M8 (rule-level states):** the eight `sharp-*` states from R93M1 are
  battery members, each moving its named rule; the mutation matrix in the
  wave re-scores the two halves that were SURVIVED in round 93 (D14, D22).

## Amendments (post-wave, pre-file)

### A1 — the C2 checker's reason test was weaker than the frozen sentence (pre-data instrument repair)

The frozen C2 sentence requires an `unfalsifiable` reason to name "a battery state ... or a
pin digest". Rev 1 (`8ec7924e…`) tested a regex over the prose, and the *word* `state`
satisfied it: a 96-character mechanism-only manifest ("… so no such state exists and none
can be built") printed `findings=1` — only the `--min-falsifiable` floor rejected it
(`.ufo/evidence/round-94/pre-freeze/c2-cheat-mechanism-word.out`, rev-1 run retained in
`c2-cheat-mechanism-word.rev1.out` if kept). Rev 2 required `state <name>` where `<name>`
is a receipt that exists in the receipt directory, plus a 12+-hex digest alternative; rev 3
also fixes the default manifest path (rev 1/2 read `tools/conjunct-disposition.json`, the
round-93 manifest, so the reason test ran on the wrong bytes — found when the real manifest
reported two findings while the same reasons passed when read from the correct file).

No claim wording, predicate, state expectation or target changes. `claims.json` names rev 1
as `instrument_sha256`; the operative instrument is **rev 3, sha256
`6d4d270644b036cdd7106a5ab24be05b5d05ed01919f7f9ce24090977bdf9b7e`**, and rev 1 is
retained as the defect witness. All C2 receipts in
`.ufo/evidence/round-94/pre-freeze/c2-*.out` are produced by rev 3 at
`6a2a1fdd35d15d3958f9860beb2569b443760b46`. Kill rule (d) is read with that substitution:
the checker blob at the named revision is rev 3's.

This is a pre-data repair: it landed (`67ce02ba`, `6a2a1fdd`) before any seat scored a C2
verdict, and the sentence it enforces is the sentence frozen above. A seat that audits the
rev-1 bytes and reports the hole is corroborating this amendment, not falsifying the claim.

Appended here if a wave artifact falsifies this record's own mechanics, in the
round-93 A1-A6 form: the claim, predicate and state expectations never change;
only statements about the record are corrected, each citing the artifact that
falsified it.


### A2 — the reader keys 4-space-indented literal blocks (R94C1 A8, A8b)

The plan's §Declared limits say "a fenced block is literal text (S322)"; it does not name
CommonMark *indented* code blocks (4+ spaces), which are literal for the same reason. The
reader therefore keys them: R94C1 appended a 4-space-indented 12-row wrong-verdict table
(`R94C1-A8-indented-code.out`: `verdict_tables=false ids=false`, exit 1) and a single
4-space literal `| C01 | KILLED |` line (`R94C1-A8b-indent-token.out`: `stray-verdict:297`,
exit 1); both are honestly additive examples that leave the twelve measured cells intact.
Narrowed wording: **the reader's unkeyed presentation class is exactly fenced blocks; a
4-space-indented literal block is keyed, so a note that embeds a wrong-verdict line in
indented code is refused. That refusal is a declared limit, not a false red on the twelve
cells.** Routed to round 95: exempt `^ {4,}` lines in `block_lines()` (when not a list
continuation) and add the control `pos-indented-literal` to the battery.

### A3 — the self-pin strips every pin line (R94R1 F1)

`SELF_PIN_RE` is applied with `re.M` and `re.sub`, so *every* `SELF_SHA256 = "<hex>"` line
is removed before hashing. A counter carrying a second, different pin line before the
`__main__` guard is therefore invisible to the digest: `R94R1-tampered-counter-demo.py`
(an `EVIL = True` insertion plus a second pin) runs the modified reader with
`C1_R94_PASS=true`. This does not falsify C1's wording — kill rule (c) binds the blob
sha256 (`a22563b0…`) and that check is external — but it does narrow QUALITY 150's reading:
**the self-pin certifies that the executed bytes are self-consistent under a strip-all
normalisation; it does not certify that they are the pinned bytes. Identity is bound by
the plan's kill rule (c) and `claims.json`, not by the conjunct alone.** Routed to round
95: require exactly one pin line (`len(SELF_PIN_RE.findall(bytes)) == 1`) before the digest,
and add the R94R1 demo as a battery state.

### A4 — cell splitting diverges from GFM on a double backslash (R94R1 F2)

`split_cells` treats `\\|` as an escaped pipe inside one cell; GFM's backslash processing
turns `\\` into a literal backslash and then the `|` separates. A note whose verdict column
is preceded by `\\|` therefore shows one thing to a human re-read and keys another
(`R94R1-probe.out`). The committed note contains no backslash in its verdict rows, so no
state in the battery moves and the twelve cells are unaffected; this is a **declared
limit**: the reader's cell boundaries are its own and are certified only for notes without
backslash escapes adjacent to a pipe. Routed to round 95: normalise `\\` before `\|` and
add a control with the witness row.

### A5 — the delimiter rule needs three hyphens where GFM allows one (R94R1 F3)

`DELIM_RE` requires `-{3,}` per cell. A GFM-legal table written with `|--|--|` is not
recognised as a table at all, so its rows fall to the stray-verdict scan and the note is
refused with 12 `stray-verdict` findings (`R94R1-probe.out`, probes P5/P36). Narrowed
wording: **the reader recognises a delimiter cell only with three or more hyphens; a
one- or two-hyphen delimiter is a non-table, and a verdict-bearing row under it is refused
as a stray verdict.** The committed note uses `|---|`, so its twelve cells are unaffected.
Routed to round 95: accept `-{1,}` per S321 and add a two-hyphen control.

### A6 — receipt provenance is ancestry, not a per-receipt digest (R94R2 F1, F2)

R94R2 found that no per-receipt `CONTROL_INSTRUMENT` line existed in the committed set and
that 43 of 45 receipts were uncommitted at its read. Both are now addressed in the tree:
the 45 receipts, the driver's summary and the driver's own stdout
(`.ufo/evidence/round-94/pre-freeze/controls-run.log`, carrying
`CONTROL_INSTRUMENT sha256=a22563b0…` and `C1_CONTROLS states=45 matched=45`) are committed
at `4dc919ac` and `b98b0864`, and `.ufo/evidence/round-94/pre-freeze/controls/C1-summary.txt`
is committed with them. Residual limit, stated: **per-receipt byte provenance is carried by
the `parent=` line and by re-runnability, not by a per-receipt instrument digest**; the
fixture clone revisions are ephemeral and not in the lane's object store. Routed to round
95: have the driver write a `counter_sha=` line into every `run_ctl` receipt.

### A7 — the C2 checker reads receipts from the working tree (R94SN1 F1-F3)

The plan's C2 surface says a `state` row's *committed* receipt must show the conjunct
false. The checker reads the counter and the manifest from `--rev` but reads the receipt
files from `--receipts` on the filesystem, without a git seal: an ambient `GIT_DIR` or a
`refs/replace` entry can substitute the counter/manifest blobs (R94SN1 F1), a
working-tree receipt can differ from the committed one (F2), and a hand-written receipt
carrying a matching `C1_CONJUNCTS` line satisfies a state row without the counter ever
running (F3). Narrowed wording: **C2 certifies the manifest-to-receipt mapping and the
counts, over the receipt bytes present in the tree at the run; receipt authenticity is not
part of C2 — it is bound by C1's own battery replay (R94E3 re-ran the full 45-state battery
from committed bytes twice into one outdir and matched every stable line) and by kill rule
(c).** The run cited in the claim used exactly the receipt bytes committed at `4dc919ac`
(the checker was run after that commit and the tree was clean for those paths; `git status`
on the controls directory is empty at the run's revision `6a2a1fdd`). Routed to round 95:
seal the checker's git reads (`GIT_NO_REPLACE_OBJECTS`, scrubbed `GIT_*`), read receipts
from `--rev` object store, refuse a receipt whose `counter_sha=` does not equal the counter
blob, and keep a hand-written-receipt control as a battery state.

### A8 — twelve rule-level mutants survive the battery (R94M1)

R94M1's 38-defect matrix scores `killed:26 survived:12` (`R94M1-results.json`,
`R94M1.md`). The survivors name rules whose removal no committed state detects: `green`
(E04), `canary` (E05, declared unfalsifiable), `unstable0` (E09), the two-run count (E10),
`out-of-set` (E13), `position` (E15), `width` (E16), figure anchoring (E20), coverage's
own-cell half (E26), the trivial detector's `rc is None` arm (E29), the one-verdict-column
rule (E30), and the spec-count half (E32). The claim sentence is unaffected — it is about
the thirty named states, which all refuse with their named conjunct false — but QUALITY 158
is **conjunct-level only** for this reader: these twelve rules have no discriminating state.
Routed to round 95: one state per survivor (the round-93 M8 list minus the four this round
added), and a mutation-matrix row in the plan that names the survivors as it does here.
