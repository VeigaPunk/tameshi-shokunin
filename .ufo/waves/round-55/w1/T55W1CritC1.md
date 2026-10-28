# T55W1CritC1 — attack on the C1 counter's design (calibration)

seat: T55W1CritC1 (critic, wave 1)
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
base: `0a2010acd1e92e4e332774050825e21bcfc7e079`
counter under attack: `.ufo/evidence/round-55/c1/measure.py`, scored in two byte sets

| byte set | sha256 | where |
|---|---|---|
| frozen | `77abe1e9daf40bec2c9d7a7c12724e766e2f98d222c287fde6097df819b60783` | freeze commit `631cd6455e58dce969310b4c0466c3383d9f5108` (also the entry in `freeze.json`) |
| amendment 5 | `711507e7b5bdd060a67b42162d043aabaef339408b3291a3c6ca39599d566dcd` | working-tree `c1/measure.py` at 14:00:09, scored while amendments 5-6 were being written |
| current (amendments 1-7) | `5e8f50d1815309e8c3a1c914191b6032b7dceff27ba42d87a676b3f78e30ac5e` | working-tree `c1/measure.py` at 14:12:07; `freeze.json` and `contract.json` both pin it (8 amendments) |

Receipt for the first row: `T55W1CritC1-receipts/counter-bytes.txt`.

## Verdict

**The C1 design is falsified.** A tree that performs **no correction at all** reaches
`total=0 C1_R55_PASS=true`, exit 0, under the frozen bytes, under amendment 5, and under the
current working bytes (amendments 1-7). My fixture's corrections section literally says it
makes no correction and that its strings were copied from the counter's own `--explain`
output; the counter scores it as ten calibrations. The two files that carry the stale text in
`corpus/` are deleted, and the stale text in `SCORECARD.md` is placed inside the exempt block
by inserting one heading line above it — not one byte of it is edited.

```
frozen  E1B-SELFDECLARED  total=0 C1_R55_PASS=true   T55W1CritC1-receipts/frozen-e1bselfdeclared.stdout
amended E1B-SELFDECLARED  total=0 C1_R55_PASS=true   T55W1CritC1-receipts/amended-e1bselfdeclared.stdout
```

The counter's three arms are all satisfied by properties the author controls, not by
properties the tree has:

- **premise** reads receipts under `.ufo/evidence/round-54/**`, which the round may edit
  (they are not in `contract.frozen_paths`), and never checks them against a digest;
- **stale** is a set of token regexes over three hand-picked files, where *a missing file
  reads as clean* and *any text inside the corrections block is exempt*;
- **corrected** is `token in corr`. There is no arm that ties the section's prose to a
  derivation, no receipt-pointer check, and no check that the section says anything at all.

Falsification is therefore not a matter of guessing the authors: the counter cannot
distinguish my non-repair from a repair, so `C1_R55_PASS=true` does not evidence calibration.

## The cheapest tree (E1B, four steps, no correction)

Built in a `git clone --shared` of the lane at BASE, every git call `-C "$D"`, toplevel
asserted equal to `$D` before the commit (`/fast/scratch/hyaku/tameshi-r55/T55W1CritC1/clones/g-declare`,
rev `b9317eff8a18`; amended run `h-declare`, rev `9bf882d8e30a`).

1. In `SCORECARD.md`, insert one heading line, `## Round 55 - round-54 record corrections`,
   immediately **above** the round-54 block (the file's last `## ` section). Everything after
   it to EOF becomes the exempt block: the five stale lines (the `CTL_POS_c1 true` row,
   both `7883e0e5` sentences, `total=14`, `fe70474d`) are never touched.
2. Under it write the sentence *"no correction was made this round; the strings below are
   copied from the counter's own `--explain` output."* and then the ten derived tokens the
   counter itself prints (`CTL_MISMATCH 2/3`, `077d431e`, `total=13`, `8528ee85
   c2/measure.py`, `w1=28 w2=25 sections=12`, `ff2a821`, `renamed 7fa9a5e`, `config.yml
   fabricated`, `reviewers=5 attack=21/76 seats=76 staged=81`, `controls-a.stdout
   rekeyed=0/7 r53-counter-at-88afa941`).
3. `git rm corpus/QUALITY.md corpus/lessons/round-54.md` (−1721 lines of record).
4. Commit. Run the frozen counter: `total=0`, exit 0.

Why each arm passes:

| arm | mechanism |
|---|---|
| premise 10/10 | every premise receipt is present at base and untouched; `row()` requires nothing more |
| stale 0 | `scan()` does `if body is None: continue` — a deleted record file contributes nothing (`measure.py:82-96`); `SCORECARD.md` is `body.replace(corrections(...), "")` — the block, not the assertion, is the unit of exemption |
| corrected 10/10 | each arm is a substring test against `corr`; `corrections()` is "text between the heading and the next `## `" (`measure.py:66-80`), so the block is whatever the author declares it to be |

The tree file itself: `T55W1CritC1-receipts/e1b-tree.txt` (corrections block, the −1721-line
deletion, and `LOG.md:2500` still calling `7883e0e5` "the freeze pointer the deciding run
uses" while the receipt says `077d431e`).

### The no-harm gate sees the edit, not the falsehood

`no-harm.sh` on the same rev: 14 ok, 1 RED (`T55W1CritC1-receipts/no-harm-on-e1b.stdout`);
the RED is `coldread-floor score=6 credited=58` against a required 8/64. I isolated the
cause rather than assuming it (`T55W1CritC1-receipts/coldread-isolation.stdout`):

| tree | change | coldread |
|---|---|---|
| BASE `0a2010ac` | none | score=8 credited=64 ok |
| `m-only-scorcard` | the corrections heading + token block in `SCORECARD.md` only | score=8 credited=64 ok |
| `m-only-delete` | `git rm` the two `corpus/` record files only | score=6 credited=58 RED |
| `m-only-hyphen` | the typography edits only (`positive-control`, `84  staged`) | score=6 credited=58 RED |

So the gate is byte-sensitive to exactly the two record files and blind to the corrections
section: six cold-read credits are bound to those files' bytes, and *any* change to them —
correction, cosmetic change, or deletion — loses the same six. Two consequences:

- My tree is not gate-free, but neither is the honest repair: clearing the R54.1/R54.9 stale
  patterns requires editing those two files, so both trees owe the same six-section re-key.
  The re-key certifies that a reader re-read a section at the content commit; it does not
  check that the record is now true. The gate therefore adds an identical cost to a
  non-repair and to a repair, and cannot tell them apart.
- `tools-scope`, `ledger-not-shrunk`, `sources-not-shrunk`, the coverage monitors and
  `registry-row-names-unchanged` are ok on the deleting tree: the only thing that noticed the
  1721-line record deletion was an unrelated cold-read byte check.

### Against the newest bytes (5e8f50d1, amendments 1-7)

The L1 amended the c1 counter twice after the freeze (amendments 5 and 7; 6 is c2-only). I
re-scored the exploit against the current bytes rather than leaving the finding pinned to a
superseded revision (`T55W1CritC1-receipts/latest-delete.stdout`, `latest-cosmetic.stdout`,
`latest-provenance.stdout`):

```
n-latest-delete    rev=a1bb5e04d62a  C1_R55: ... stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
n-latest-cosmetic  rev=4a54ab063b35  C1_R55: ... stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
n-latest-prov      rev=d5f6ad6c49bd  C1_R55: ... total=0 C1_R55_PASS=true  (R54.4 derived=c2 digest=deadbeef)
```

Two amendments landed in between and they are the L1's, not mine:

- **Amendment 7** closed two of my preliminary observations: `staged_count()` now reads the
  committed `.ufo/evidence/round-55/c1/staged-at-freeze.txt` instead of
  `/home/vgpnk/Projects/shokuknow` (the E8 non-hermetic path), and R54.8's seat arm now
  requires `SUPERSEDED (round 55` rather than any occurrence of "superseded" (the E10 seat
  token). To reach `total=0` on the current bytes my tree therefore adds four lines of
  boilerplate — the `output=81` receipt and one `SUPERSEDED (round 55 …` line — and still
  corrects nothing: the ten defects' false assertions are deleted or hidden exactly as before.
- The structural holes are untouched: `corrections()`/`scan()` are byte-identical to the
  frozen version, so absence-as-compliance, the positional exemption and token-presence all
  survive; R54.2/R54.3/R54.9 still pass their own single-file tuples (R54.2's
  `("SCORECARD.md",)` at latest line 212), so `LOG.md`'s `7883e0e5` still scores clean; R54.10
  still hard-codes `r53-counter-at-88afa941` (latest line 273); only `Setup` is caught (line
  323); the verdict still does not assert `len(rows)`.

Credit where due: the amendment cycle is real — it fixed the wrapped-line blindness, the
record-set omission, the live staged path and the pre-existing token, each found by a wave-1
seat. It did not touch the three properties this seat falsifies.

## Five further counterexamples (all measured)

### E2B — typography only, nothing deleted, nothing corrected

Same inserted heading and token block; `positive control` → `positive-control` on **every**
line of `corpus/QUALITY.md` and `corpus/lessons/round-54.md`; `84 staged` → `84  staged`.
Every false claim stays readable. `total=0` on the frozen bytes, on amendment 5, and on the
current bytes (`frozen-e2bcosmetic.stdout`, `amended-e2bcosmetic.stdout`,
`latest-cosmetic.stdout`; revs `88ed0c2334a6`, `e56a6eb75515`, `4a54ab063b35`).

This also defeats **amendment 5**: the amendment's `scan_span` catches the one line whose
words are split across a wrap (`corpus/lessons/round-54.md@4260 ... positive control ...
requires rekeyed=7/7`), but a hyphen and a doubled space on the other lines put the exact
same falsehood back out of reach. An amended arms race over spellings is not a fix; the
record's claim has to be re-derived, not pattern-matched.

### E5B — false provenance: the counter certifies a digest the tree does not have

Take E2B, then set `.ufo/evidence/round-54/freeze.json`'s `files["c2/measure.py"]` to
`deadbeef000…` and write `deadbeef` in the corrections block instead of `8528ee85`.
`R54.4 ok`, `total=0`, on both byte sets.

```
record certifies:   deadbeef…
actual sha256 of .ufo/evidence/round-54/c2/measure.py at that rev: 8528ee8555da…
```

Receipt: `T55W1CritC1-receipts/e5b-provenance.txt`. The cause is `derive_freeze_digest()`
(`measure.py:98`): it reads the digest **from a manifest**, and nothing in the counter ever
hashes the counter bytes it is certifying. R54.4 is a record-to-record check in a claim whose
whole subject is record-to-tree agreement. The manifest is itself editable this round
(`.ufo/evidence/round-54/**` is not in `frozen_paths`).

### E10 — the "derived" values are steerable by the author

Add `.ufo/waves/round-54/w1/T54W1Read99.json` (`{"findings":[{"id":"X1"},{"id":"X2"}]}`).
`finding_counts()` (`measure.py:108`) globs by filename regex and counts; the counter now
derives `w1=30` and accepts `w1=30 w2=25 sections=12` — `R54.5 ok`. Receipt:
`frozen-e10-steer.stdout`, `amended-e10-steer.stdout`. The derivation reads a set the author
can extend; it is not anchored to the round-54 registry.

### E8 — the verdict depended on a live external project (closed by amendment 7)

Scoring the passing tree with `--staged-root <empty dir>` gave
`premise=9/10 ... total=1`. The default was `STAGED_DEFAULT =
"/home/vgpnk/Projects/shokuknow"` (`measure.py:39` in the frozen/amendment-5 bytes), globbed
at measure time (`measure.py:142`). The same revision therefore scored PASS or FAIL depending
on a mutable working copy outside the lane, outside the freeze, and outside the counter's
arguments (`frozen-e8-stagedroot.stdout`, `amended-e8-stagedroot.stdout`). **Amendment 7
closed this**: `staged_count()` now reads the committed
`.ufo/evidence/round-55/c1/staged-at-freeze.txt`. The finding is kept because it is what the
frozen and amendment-5 bytes did, and because the shape (a premise read from something other
than the revision) is what F4 still exhibits.

### Nine classes still PASS

Delete `row("R54.6", …)` from a copy of the frozen counter and run it at the E1B tree:

```
C1_R55: ... classes=9 ... total=0 C1_R55_PASS=true    exit 0
```

The verdict (`measure.py:278-284`) computes `total` from whatever rows exist; it never
asserts `len(rows) == 10` or the class-id set. A future amendment that drops or mis-indents a
class still reports `PASS=true`; only a human comparing the printed `classes=N` would notice.
Receipt: `T55W1CritC1-receipts/nine-class.stdout`.

## The four questions in the item

**Can a tree that does NO work reach `total=0` by writing a corrections section with the
right literals?** Not with literals alone — my replay of `CTL_SKIP_c1` (tokens appended at
EOF, stale untouched) scores `total=4` (`frozen-e0-skip.stdout`), so that control's premise
holds for the exact shape it tests. But add one heading line above the offending record
region and delete the two non-SCORECARD record files, and yes: `total=0`, twice, with a
section that states it is not a correction. The literals are not even guessed — `--explain`
prints them.

**Is the stale scan's file scope right?** On the spotcheck lesson, yes: `RECORD`
(`measure.py:34-38`) is `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`;
`corpus/lessons/round-54-verifier-spotcheck.md` is not read, which is correct — that file
legitimately quotes the wrong values while describing the defects (`total=14` at :63,
`rekeyed=7/7` at :44, `7883e0e5` at :110). The complement is wrong in two ways.
(a) `LOG.md` carried R54.2's false pointer at base (`LOG.md:2500`, "the freeze pointer the
deciding run uses", for `7883e0e5`) and was not in `RECORD`; amendment 5 adds it, but
(b) R54.2, R54.3 and R54.9 call `scan()` with their own single-file tuples
(`measure.py:206,214,256`), so `RECORD` membership binds only R54.1 — on the amended counter
`LOG.md`'s false pointer still scores `R54.2 stale=0` (`amended-e1bselfdeclared.stdout`).
Also unscanned: `SKILL.md`. The right scope is per class, over every record that states that
class's claim, with the spotcheck the only legitimate exclusion.

**Corrections section last in the file / a second `## ` heading intervenes?** The block is
*first heading wins, first following `## ` ends it*; a duplicate heading does not end it
because the `startswith(HEADING)` test runs before the `## ` break (frozen `measure.py:66-80`).

- **Last section** → the block runs to EOF. That is the exploit: the exemption is positional,
  so wrapping the round-54 block with one heading above it exempts the whole block. It also
  means the exemption grows: anything appended after the last heading, later, is exempt.
  Level-3 headings (`### Round 54 — measured close`) do not end the block, so nested
  subsections are exempt too.
- **Second `## ` intervenes** → the block is truncated at that heading. Measured
  (`i-frozen-intervene`, `eb5a9a1e8c7a`; amended copy `0ead04cd2bfa`): `corrections()` returns length 0, the tokens after
  the break are invisible (`classes_corrected=0/10`) and the stale lines after the break come
  back into scope (`stale=3`) → `total=10`. So an author who writes the round-55 block
  between the corrections heading and its content loses all ten corrections silently. This
  is a fail-closed fragility for the author and a fail-open hole for the record: the same
  boundary decides both.
- **Duplicate heading** → the two blocks are concatenated (70 lines, `corr_len=5268`) but the
  concatenation is not a contiguous substring of the file, so `body.replace(corr, "")` fails
  and the SCORECARD exemption collapses (`contiguous=False`, `stale=3`, `total=3`). Receipts:
  `probes.stdout`, `frozen-e4dupe.stdout`, `amended-e4dupe.stdout`.

Because the exemption is an exact-string identity rather than a region, a copy of the block
placed anywhere also has every duplicate removed by `str.replace` — a second laundering path
that needs no heading at all.

**Does `premise` ever fail quietly?** A premise miss always fails its class, so there is no
case of a class passing on a dead premise. But there are four quiet behaviours:

1. **Crash reads as miss.** `except Setup` is the only handler (`measure.py:291-294`); any
   other exception exits **1**, the same code as a failed class, with no verdict line. Feed
   `.ufo/evidence/round-54/freeze.json` = `{"files": []}` and the counter dies with
   `AttributeError: 'list' object has no attribute 'get'` at `measure.py:126`
   (`frozen-e7-crash.stdout`). A broken instrument is scored as a failed claim.
2. **A premise can be satisfied by an edited receipt.** R54.4's premise is `bool(digest)`
   where the digest comes from a mutable manifest (E5B); R54.1's premise is two substrings of
   a mutable receipt.
3. **A premise could fail on host state.** R54.9 (E8); closed by amendment 7's committed
   staged receipt.
4. **Half of R54.8 was already true at base.** The "seat file marked superseded" arm was
   `"superseded" in seat.lower()`, and the base seat file already contains the word in an
   unrelated round-50 sentence (`T54W1ExecStraceNoise.md:299`, "the round-50 directive
   superseded it"). It was satisfied with zero work; **amendment 7 closed it** by requiring
   `SUPERSEDED (round 55`. (Same class of defect, still open: R54.10's
   `r53-counter-at-88afa941` is a **hard-coded literal** in the counter, not a derivation —
   latest `measure.py:273` — so one of the ten "derived" arms cannot be derived at all.)

## Impacted axes

- **calibration (8) — the C1 claim itself.** The claim's surface is "the lane's records must
  agree with the tree". The counter establishes agreement between an author-authored block
  and a token list, over records the author may delete or hide. `C1_R55_PASS=true` is
  therefore not evidence of calibration; the claim as written can be certified by a tree that
  is strictly worse than base (two records gone).
- **evidence standard / operability of the round's instrument.** A frozen instrument was
  edited during wave 1 and the manifest was not updated (below); a crash and an honest miss
  are indistinguishable by exit code; the verdict does not assert its own denominator.
- **no-harm** constrains the edit, not the content: cold-read credit is byte-bound to the two
  record files, so every C1 repair — the honest one included — owes the same six-section
  re-key. No monitor's predicate asks whether a correction was made, so the gate does not
  compensate for the counter's blindness; it adds the same cost to a non-repair.

## Freeze-state observation (reported, not fixed)

While this seat ran, the working-tree counter changed twice under it. The state I scored at
14:00 and the reconciled state at 14:12:

```
14:00  freeze.json (working) pins c1/measure.py at  77abe1e9…   (3 amendments)
       working c1/measure.py is                      711507e7…   (mtime 14:00:09)
       contract.json (working) records               5 amendments
14:12  freeze.json and contract.json both pin        5e8f50d1…   (8 amendments, 8 = c2 only)
```

At 14:00 the manifest digest and the counter bytes disagreed and the manifest listed 3
amendments against the contract's 5; by 14:12 the L1 had reconciled both files and the
manifest matches the bytes. `controls.sh` extracts the counter from the FREEZE **commit**, so
a control scored between those states would have run `77abe1e9` while the amendment's intent
was `711507e7`. I scored all three byte sets and pinned every result to a digest
(`counter-bytes.txt`, `latest-*.stdout`); I did not edit any frozen byte, contract, manifest
or script. This is a record of the window, not an accusation — but a seat that verified
digests during it would have seen `FROZEN_UNCHANGED` false, and the window is why my three
byte sets exist.

## Smallest safe correction

The falsifier dies with two changes; the rest closes the sibling holes. I propose them as a
patch to the counter (to be committed, with `freeze.json`'s digest and an amendment note
updated in the same commit — never edited in place):

1. **Absence is not compliance.** In `scan()` (and `scan_span()`), `body is None` must fail
   the class, not `continue`. Simplest: in `classes()` require
   `all(exists(lane, rev, p) for p in RECORD)` as a premise of every class (or a fourth
   `present` arm folded into `ok`).
2. **Exempt a grammar, not a region.** Drop the positional block. Have `corrections()`
   return only lines matching one correction grammar, e.g.
   `^- R54\.(10|[1-9]) old: .+ -> new: .+ \(receipt: [^)]+\)$`, and exempt only those lines.
   Then the round-54 claim table cannot be hidden by placing a heading above it, the token
   soup fails (no `old:`/`->`/receipt), and the receipt pointer the contract asks for is
   enforced. Keep `HEADING` as a required, exactly-once marker so a missing or duplicated
   section fails rather than silently changing scope.
3. **Bind the value to the tree, not to another record.** R54.4 must compute
   `sha256(c2/measure.py at rev)` and require it to equal both the quoted digest and
   `freeze.json`'s entry. R54.2 must require the quoted pointer to equal the receipt's
   `freeze=` and forbid any other 8-hex pointer in the section. R54.5 must count only reader
   files named by the round-54 `w1-registry.json`. R54.10's `88afa941` must be derived from
   the receipt's filename, not hard-coded.
4. **One record set.** Every class's stale scan takes `RECORD`; remove the per-class file
   tuples at `measure.py:195,206,214,256`. Then adding `LOG.md` (amendment 5) actually binds.
5. **Assert the denominator.** `if len(rows) != 10 or {r["id"] for r in rows} != {...}:
   raise Setup(...)`, so a lost class is `could-not-evaluate`, not `PASS`.
6. **Separate crash from miss.** Wrap `main()` in `except Exception` → `C1_SETUP:
   could-not-evaluate: <type>: <msg>`, exit 2; keep 1 for one or more failed classes.
7. **Hermetic derivation.** Delete `STAGED_DEFAULT` as a live path: take the staged count
   from a lane-committed artefact or a value frozen in the contract, and freeze `staged=81`
   in `contract.json`. A deciding run must not depend on `/home/vgpnk/Projects/shokuknow`.
8. **R54.8's seat arm** must match a line that names the correction
   (e.g. `Superseded .*R54\.8`), not any occurrence of "superseded" (base already has one).

With (1), (2), the R54.4 half of (3), and (5), all of E1B, E1-delete, E2B, E5B and the
nine-class verdict fail. I am not asserting a counter can judge whether a correction's prose
is *fair* (the contract's `cannot_see` concedes that); it can and must refuse to certify a
tree that made no correction.

## Sweep that found nothing (shown, so the nulls are visible)

- **Base reproduces the committed before-receipt exactly**: `premise=10/10 stale=4
  classes_corrected=0/10 total=10` (`frozen-base.stdout` ≡ `.ufo/evidence/round-55/before/c1.stdout`).
  The harness is faithful; the exploits above are not harness artefacts.
- **`CTL_SKIP`'s premise holds for its own shape**: tokens at EOF with no stale work →
  `total=4` (`frozen-e0-skip.stdout`). The hole is that the control's shape is the *only*
  skip shape tested.
- **Spotcheck lesson correctly excluded** from `RECORD` (it legitimately quotes every wrong
  value: `:44`, `:63`, `:110`).
- **Base stale hits are genuine**: I read all four (SCORECARD 2583/2564/2567/2608, QUALITY
  1590, round-54 101/51) — each is the false assertion the spotcheck named, so the frozen
  patterns produce no false positive at base. (They are, however, pure token matches: `7883e0e5`
  is flagged even where a line also prints the correct `freeze=077d431e`, so the cheapest way
  to clear R54.2 is to move or delete the sentence, not to correct it.)
- **Intervening heading and duplicate heading fail closed** for the author (E3c `total=10`,
  E4 `total=3`); the fail-open direction is the two absent/hidden-record paths above.
- **Premise misses are loud** in the row and in `total` (E8, premise=9/10); the quiet paths
  are the four listed under question 4.

## Reproduction

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r55/T55W1CritC1
# fixtures (clone --shared at BASE, toplevel asserted, one commit each)
python3 $S/drive3.py    # E1B, E2B, E4, E5B (frozen + amendment-5 bytes)
python3 $S/drive4.py    # E3c intervening heading + corrections() readout
python3 $S/drive5.py    # R54.5 steerability; R54.8 base token
python3 $S/drive6.py    # the same exploit against the current bytes (5e8f50d1)
# the decisive run, frozen bytes
python3 $S/code/c1-frozen.py --lane $S/clones/g-declare \
  --rev b9317eff8a18 --work $(mktemp -d) --explain
# and the amended bytes at the same tree
python3 $S/code/c1-amended.py --lane $S/clones/h-declare \
  --rev 9bf882d8e30a --work $(mktemp -d) --explain
```

No lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) was
edited; nothing was written outside `.ufo/waves/round-55/w1/T55W1CritC1*` and the seat
scratch. No mutating git command was run in the lane; every commit is in a scratch clone. No
tool was installed or upgraded this seat (python3 and git only), so there is no tooling entry
to record.
