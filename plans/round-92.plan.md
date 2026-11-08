# Round 92 — frozen plan (tameshi, L1 TameshiR92, attempt 1)

Base `63172b9889475103aeca976d37389d204010dd11` (round-91 verifier-spotcheck tip).
Instrument revision **`84904d41a31fb5ddde49e8bf1ad6fc2b489671a0`** — the C1 successor
counter, the battery driver, the S320 row, the lesson Gate and the round-92 spec copy.
Battery-driver revision **`f0ece7a3c74e7e2504dd3994d0efe0e88c3dcfb0`** (the driver of
record for every receipt; it is the A3 driver plus three mutant-phase repairs A4/A5/A6 —
`git diff 84904d41 f0ece7a3 -- .ufo/evidence/round-92/c1/controls-v92.py` — none of which
touches the state phase). This
file is committed on top of both and freezes the claim; nothing below changes after any
seat scores.

Fresh-start duty: tameshi's fresh start was round 91 (Amendment 62), so this round is not
a fresh-start round; the round-91 non-author spot-check
(`corpus/lessons/round-91-verifier-spotcheck.md`) was read in full before declaring, and
both of its routed lane defects are handled in this round's records (see § Records).

## Claim (one; coverage; sourced S320)

### R92-C1 — the third attempt at certifying the fleet-gate case note, under a sealed self-pinned counter

Surface: the case note `corpus/knowledge/mutation-case-fleet-sources-census.md` and the
fleet's own registry gate `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` at
fleet commit `f47ad6ba8d306f8125597401cb2ce45c1297a593` (read-only; the case re-executes
it under its own `selftest`). Spec copy
`.ufo/evidence/round-92/c1/census-mutants.json` (bytes identical to round 90's,
sha256 `ce8983d5…e290`).

Instrument: `.ufo/evidence/round-92/c1/measure-v92.py`, **sha256
`be5a9221b36983d6c45e983c398ee9c9c088b374d36fb17e2ae67f50ad749ea9`**, a successor to
round 91's frozen counter (never edited). It differs from v91 in exactly two properties,
both required by round 91's own routed list:

1. **self-pin (QUALITY 144).** The file carries `SELF_SHA256`, the sha256 of its own bytes
   with the single `SELF_SHA256 = "<64 hex>"` line removed; the first action of every run
   re-derives that digest and refuses (`C1_SETUP self-pin-mismatch`, exit 2) when it
   differs. The conjunct printed in the receipt is the result of that check, not a
   literal. Any post-freeze edit of the instrument is inert: it cannot print a verdict.
   The pin is re-derivable with one command:

       python3 -c 'import hashlib,re,sys; b=open(sys.argv[1],"rb").read(); \
         b=re.sub(rb"^SELF_SHA256 = \"[0-9a-f]{64}\"\n", b"", b, flags=re.M); \
         print(hashlib.sha256(b).hexdigest())' .ufo/evidence/round-92/c1/measure-v92.py

   must print `723562ed5b20e1a914d9addbce9007b8edf1c962c8237592dbac3b39e5509c2c`
   (the normalised digest; the raw file digest is the sha256 above).

2. **id-set refusal (QUALITY 143).** `parse_note` treats every Markdown table row as
   follows: a row whose first cell is id-shaped (`^[A-Za-z]{1,4}[_-]?[0-9]{1,4}$`) **or**
   that carries a `KILLED`/`SURVIVED` token must be keyed by exactly one id in the spec's
   set `C01`–`C12`, must carry exactly one verdict token, and that token must sit in the
   header-named `verdict` column; a duplicate id, a row outside the set, a verdict token
   on a non-id row, a second verdict column, and a note with more or fewer than one
   `verdict` header or than the twelve ids all make `ids=false` — refused, never skipped.
   A second verdict table under ids the lane does not key (`C001`–`C012`, `X1`–`X12`, …)
   therefore refuses the note instead of hiding behind it.

The seal (QUALITY 139) is unchanged from round 91: every git call carries
`GIT_NO_REPLACE_OBJECTS=1` with a scrubbed `GIT_*`, and a non-empty `git replace -l` in
the lane repo or the fleet repo refuses setup (exit 2).

Frozen predicate — the same condition as the counter's `ok = all(conj.values())` and its
receipt label `C1_R92_PASS=true`:

    selfpin ∧ pin ∧ spec ∧ green ∧ canary ∧ invalid0 ∧ trivial0 ∧ inconclusive0 ∧
    unstable0 ∧ note ∧ ids ∧ mismatched0 ∧ figure ∧ witnessed ∧ source ∧ coverage ∧ n_min

Counting command (frozen):

    python3 -I .ufo/evidence/round-92/c1/measure-v92.py --repo <lane> --rev REV --work <empty dir>

Additional frozen condition of the claim (same round): the committed control battery

    python3 -I .ufo/evidence/round-92/c1/controls-v92.py --lane <lane> \
      --rev 84904d41a31fb5ddde49e8bf1ad6fc2b489671a0 \
      --base 63172b9889475103aeca976d37389d204010dd11 \
      --work <empty dir> --outdir <dir> --jobs 5

prints `C1_CONTROLS states=25 matched=25 mismatches=0`, exit 0, with the receipts
committed under `.ufo/evidence/round-92/pre-freeze/controls/`. The summary is derived by
the driver from the receipts on disk; a receipt the run did not write cannot be counted.

Before (do-nothing): at base `C1_SETUP spec-absent-at-rev`, exit 2 (the round-92 spec
path does not exist at `63172b98`). Target: `C1_R92_PASS=true`, exit 0, at the landing
revision, and `C1_CONTROLS states=25 matched=25 mismatches=0` on the committed battery.

Kill rule (any one kills C1):
- (a) any committed state — lane or scratch clone, any seat's — that does not hold the
  twelve true verdicts reaches `C1_R92_PASS=true` while the note presents different
  verdicts (a second table, an escaped-pipe row, a fenced table, a hidden duplicate, a
  prose verdict), or an honest note is refused by a rule stated above;
- (b) a non-author execution of the gate's own `selftest` on a spec mutant yields a
  verdict different from the note's row;
- (c) the committed counter blob at the instrument revision differs from the sha256 named
  above, or any battery receipt was produced by bytes other than the counter at
  `84904d41` and the driver at `f0ece7a3`;
- (d) a control state in the committed battery is scored MATCH while its receipt does not
  show the pre-registered outcome (the driver's summary is derived from the receipts; a
  hand-edit of the summary is a kill).

Declared limits (not kills): fenced code blocks and HTML tables are not keyed (they are
not Markdown tables the note presents as its verdict table); verdict words in prose are
ignored; the counter certifies that the twelve cells are true, not how they were obtained
(a note copying the predictions carries the same cells — round 90's critic probe); the
canary shows the copy runs, not which selftest arm executed a mutated line; the
`GIT_NO_REPLACE_OBJECTS` half of the seal is not outcome-distinguishable while the
`replace -l` gate is present (the battery records D01 alone as redundant, D01+D02 as the
removal that turns a refusal into a PASS); a table row with an escaped `\|` inside a cell
shifts the columns and refuses, which is strict but not explored by the note.

## Controls (pre-freeze, committed before this file)

Driver `.ufo/evidence/round-92/c1/controls-v92.py` (rev `f0ece7a3`,
sha256 `083790e392f7e5c4f8004c6baa7dc75b0e3b0393aa7629a061ee09f6acd464e1`); receipts and
summary under `.ufo/evidence/round-92/pre-freeze/controls/`. Every state is a
`git clone --shared` of the lane at `84904d41`, checked out detached, one edit committed
under the fixture identity `r92-fixture`, and read by the counter blob extracted from
`84904d41` (never the working tree):

| state | edit on the honest state | expected |
|---|---|---|
| `pos-real` | none (the real note, registry row and lesson at `84904d41`) | `C1_R92_PASS=true`, exit 0 |
| `pos-fixture` | a synthetic 12-row honest note | `C1_R92_PASS=true`, exit 0 |
| `nowork-base` | no edit; the counter read at base `63172b98` | `C1_SETUP spec-absent-at-rev`, exit 2 |
| `nowork-note-absent` | the note deleted | `ids=false`, `note=false`, exit 1 |
| `out-of-set` | a second table `C001`–`C012` with inverted verdicts | `ids=false`, exit 1 |
| `out-of-set-letters` | a second table `X1`–`X12` | `ids=false`, exit 1 |
| `unkeyed-row` | a verdict-bearing row whose first cell is not an id | `ids=false`, exit 1 |
| `dup-row` | a duplicate `C02` row with the opposite verdict | `ids=false`, exit 1 |
| `position` | the verdict token in the witness column, not the named column | `ids=false`, exit 1 |
| `inverted` | the presented table's twelve verdicts inverted | `mismatched0=false`, exit 1 |
| `figure` | `measured: 6/12 killed` | `figure=false`, exit 1 |
| `source` | S320's status `mined` → `queued` | `source=false`, exit 1 |
| `coverage` | every README line naming the note removed | `coverage=false`, exit 1 |
| `spec-mutated` | one mutant's `new` edited (spec bytes change) | `spec=false`, exit 1 |
| `noop-mutant` | one mutant `new` == `old` | `invalid0=false`, exit 1 |
| `syntax-mutant` | one mutant's `new` is a bash syntax error | `invalid0=false`, exit 1 |
| `trivial-mutant` | one mutant's `new` breaks `validate` (gawk error) | `trivial0=false`, exit 1 |
| `witness-same` | C02's witness edited to agree with pristine | `witnessed=false`, exit 1 |
| `pin-mismatch` | the spec's gate sha256 zeroed | `pin=false`, exit 1 |
| `selfpin-edit` | the counter bytes with one appended comment, run on the honest state | `C1_SETUP self-pin-mismatch`, exit 2 |
| `replace-honest` | honest note committed + `git replace` to a false note | `C1_SETUP replace-refs-present`, exit 2 |
| `replace-false-sealed` | false note committed + `git replace` to the honest note | `C1_SETUP replace-refs-present`, exit 2 |
| `D01` | counter mutant: `git replace -l` gate removed, run on `replace-honest` | `C1_R92_PASS=true` (removal detected), exit 0 |
| `D01D02` | counter mutant: gate + `GIT_NO_REPLACE_OBJECTS` removed, run on `replace-false-sealed`'s state | `C1_R92_PASS=true` (the cheat), exit 0 |
| `D03` | counter mutant: self-pin assert removed + id shape narrowed to `C\d\d` + unkeyed rule removed, run on `out-of-set` | `C1_R92_PASS=true` (the round-91 cheat), exit 0 |

`D01` is the arm QUALITY 149 names: the state is one the frozen counter refuses, and
removing the refusal turns it into a PASS, so the gate is load-bearing. `D03` re-creates
round 91's exact failure (a hidden three-digit table plus no pin) and shows both defences
are what stop it. Mutants are studied with the `SELF_SHA256` line recomputed for the
edited bytes (a mutation study cannot run under a pin that forbids edits); the frozen
bytes stay pinned and unedited — that is the property the pin protects.

## Wave

One v1 wave `r92-w1`, 11 seats (attack seats 5: two reviewers, one critic, one
mutation-tester, one sentinel = 45 %). Items: independent reproduction of the twelve
verdicts outside the counter (T92E1); no-harm sweeps at base and instrument revision
(T92E2); reproduction of the battery from committed bytes (T92E3); the note's
status-addendum draft (T92SC1); independent S320 verification (T92S1); a parser-premise
audit of the real note (T92S2); counter code review (T92R1); freeze conformance (T92R2);
a kill attempt under rule (a) (T92C1); a mutation matrix of the counter (T92M1); a driver
safety audit (T92SN1). The L1 holds the planner seat (the validator refuses `planner`);
no residual call is planned.

## Assimilation and considerthese

Assimilation: none — no staged `merge/tameshi/` theme serves a sealed-counter successor.
considerthese: `2026-11-07.md` idea 1 (inherited-hardening lint for every new counter) is
mined this round; it lands as `tools/hardening-lint.py` plus a QUALITY criterion citing
the file and the date, with this round's counter as the positive case (8/8) and the
round-91 counter as the state shown to fail (5/8: no self-pin, no id-set refusal).

## Records (r91 routed defects)

- Routed defect 1 (stale counts at the r91 landing): append-only corrections in `LOG.md`
  and `corpus/lessons/round-91.md`; the frozen `plans/round-91.plan.md:201` cell is named,
  never edited.
- Routed defect 2 (`claims.json` freeze rev mismatch): `.ufo/waves/round-92/claims.json`
  names the instrument revision `84904d41…` and the driver revision `f0ece7a3…` — the
  revisions whose bytes every receipt certifies — and this plan names the same two; the
  plan-filing commit is their child, so the two cannot disagree.
