# tameshi round 74 — lesson

Round 74 (attempt 1), base `3d6ea1ee8e551e3baf94904384890e3a112088f0`
(`= origin/master`, clean tree — the **admitted** round-73 non-author closure,
`corpus/lessons/round-73-verifier-spotcheck.md` §7). Claims, counters, kill
rules, arms and controls are frozen **before any claim data** in
`plans/round-74.plan.md` (declaration commit `a7cd78ae`). Round shape: one v1
wave, 12 seats (4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1
mutation-tester · 1 connector · 1 sentinel), policy band 8–16. `labrat` is a
frozen-topology seat the validator rejects, so no labrat item exists; the
planner seat stays with the L1.

## Declared claims (frozen pre-data)

- **R74-C1 — operability (verdict-only).** The three arm gaps the round-73
  wave measured become arms of `tools/wave-reconcile.py`: arm13
  delimited-token, arm14 record-span substring, arm15 `seat_reports`
  top-level-only. Before: `12/12 pass` and the three named mutants survive;
  after: `15/15 pass` and a committed runner spec
  (`tools/wave-reconcile-mutants.spec`) kills all three on their named arms.
- **R74-C2 — calibration (the lowest scored numeric axis at 8; sourced on the
  re-opened S294 and the new S304).** `tools/additivity-range.py` +
  `tools/additivity-range.json`: append-only claims become a measured sweep
  over a declared commit range with a declared claim class per row, so the
  round-73 closure's two routed EOL rewrites stand as MEASURED declared
  violations.

## Gate — the sources (S294 re-opened, S304 opened)

**S294 — re-open, not a new row.** `gitattributes` is already held (round 63)
for the `text`/`eol` conversion layer; this round's instrument rests on the
same ground (a rewrite is a byte event, not a property of the file), so a
second row on the same URL would be a within-scope duplicate (CORPUS.md rule 2;
the S289/S293 precedent). The curation delta is a **re-open**: S294's
`used-by` cell gains `corpus/lessons/round-74.md` and this Gate carries fresh
located quotes.

- Source: Git, *gitattributes* documentation,
  <https://git-scm.com/docs/gitattributes>. Fetched 2026-11-04 (HTTP date
  `Wed, 04 Nov 2026 01:45:57 GMT`; 131,174 B; sha256
  `ceb3351f931ae86283f51416cf0042fd78265eda59e5af7d09e17581ec0f77f7`; extract
  `.ufo/evidence/round-74/sources/s294-gitattributes.html`, headers
  `.ufo/evidence/round-74/sources/s294-headers.txt`).
- Quote 1 (page lines 2667–2668, 13 words): "This attribute marks the path as
  a text file, which enables end-of-line conversion" — conversion is an
  *attribute of a path*, not a property of blob bytes.
- Quote 2 (page lines 2678–2679, 9 words): "Line endings are normalized to LF
  in the index" — normalization is an action on the index when the attribute
  layer applies.
- Quote 3 (page lines 2758–2759, 20 words): "While Git normally leaves file
  contents alone, it can be configured to normalize line endings to LF in the
  repository" — **absent that configuration, blob bytes are the bytes
  committed**, which is exactly the premise of the raw comparison: a CRLF→LF
  rewrite changes the blob, and only a declared normalization can hide it.
- **Admit:** S294's conversion-layer re-open (the three located quotes above;
  the round-63 scope cell stands as written).
- **Reject (standing, re-sampled):** a new `gitattributes` row for the
  round-74 ground — same URL, same document, within-scope duplicate; flip
  condition: the round-63 row is retired or the page is superseded by a new
  document, at which point the successor is a new document with a new row.

**S304 — a new row, a different document.** The `git-diff` page was unheld
(`grep -c 'git-scm.com/docs/git-diff[^-]' corpus/SOURCES.md` → `0` at
`3d6ea1ee`; the count of `1` belongs to the `git-diff-tree` row S297).

- Source: Git, *git-diff* documentation,
  <https://git-scm.com/docs/git-diff>. Fetched 2026-11-04 (HTTP date
  `Wed, 04 Nov 2026 01:46:16 GMT`; 229,283 B; sha256
  `05206b6fbf4c2bec4a433ebc497cf97016dd1843f8de87a6eca6681d0a6543a8`; extract
  `.ufo/evidence/round-74/sources/s304-git-diff.html`, headers
  `.ufo/evidence/round-74/sources/s304-headers.txt`).
- Quote (page line 4157, 11 words): "Ignore carriage-return at the end of line
  when doing a comparison." — the CR-blind comparison is an **option you
  declare**, never the default; that is why the sweep carries two claim
  classes and prints both numbers instead of silently choosing one.
- **Admit:** S304 (status `mined`, recheck `180d`, `used-by`
  `corpus/lessons/round-74.md`).
- **Reject:** nothing on this row's ground; the sibling candidate (the
  `gitattributes` page again) was refused as a duplicate, above.
- Header hygiene: both fetches were checked for `set-cookie` and credential
  fields — `grep -ic set-cookie` → `0` on both (the round-73 sentinel finding:
  Cloudflare set a `__cf_bm` cookie on the RFC fetch; nothing leaks here).

## What was measured — R74-C1 (operability, arms)

**Before** (receipt `.ufo/evidence/round-74/base-measure-r74.txt` at
`a7cd78ae`): `python3 -I -X utf8 tools/wave-reconcile.py --selftest` →
`WAVE_RECONCILE_SELFTEST: 12/12 pass`. The three mutants the round-73 wave
measured as survivors were rebuilt by wave seat T74W1E1 from the pristine
bytes: `m2` (delimited tautology) 12/12, the two-line `span-not-in-record`
guard deleted 12/12, `seat_reports` any-depth 12/12.

**After** (receipts `.ufo/evidence/round-74/battery-r74.txt`,
`sweep-after-arms-r74.txt`; measured commit `2bbf9796`, tool sha256
`9532c12b186e4f5dd011f3d59cd38f23caf6f14de4c137da555863d575c4133d`, 23,238 B):

```
$ python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
WAVE_RECONCILE_SELFTEST: 15/15 pass                       exit 0
$ bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
    --defects tools/wave-reconcile-mutants.spec \
    --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <scratch>
CONTROL: GREEN (exit=0 …)
DEFECT m2-delimited-tautology: KILLED (exit=1 …)
  | SELFTEST arm13-printed-undelimited-refused    FAIL (got=drift want=setup)
DEFECT span-rule-removed: KILLED (exit=1 …)
  | SELFTEST arm14-span-not-in-record-refused     FAIL (got=drift want=setup)
DEFECT seat-reports-any-depth: KILLED (exit=1 …)
  | SELFTEST arm15-seatreports-top-level-only     FAIL (got=drift want=meet)
MUTATE_RESTORE: OK (target-sha256 before=9532c12b… after=9532c12b…)
MUTATE: DONE (target=wave-reconcile-arms defects=3 killed=3 survived=0 inconclusive=0 kill-rate=100%)
```

Each mutant dies on its **named** arm only (13/14/15 in order), so the arms are
load-bearing and not redundant. The standing six-row sweep is unchanged:
`WAVE_RECONCILE: rows=6 met=6 unexpected=0` exit 0
(`.ufo/evidence/round-74/sweep-after-arms-r74.txt`).

The fixture repair arm15 forced is part of the measurement: `SEAT_FILES` was
`x/…` while the artifact dir key is `wave`, so the listing prefix matched
nothing and arm3 (`seat_reports` drift) had been passing on `files=0` since
round 73. The paths now live under `wave/`, so arm3 measures `printed=11
files=12` for the right reason and the nested `wave/nested/deep.md` gives
arm15 its discrimination (top-level 12 = meet; any-depth 13 = drift).

## What was measured — R74-C2 (calibration, range additivity)

**Before** (same receipt + `.ufo/evidence/round-74/range-scan-r74.txt`): no
range mode (`grep -c rev-list tools/additivity-receipt.py` → `0`). The existing
tool's default judgement on the round-73 `LOG.md` rewrite pair prints
`raw_old_only=3484 … norm_cr_old_only=0 eol_rewrite_disclosed=true` and exits
**0** — a clean-looking receipt for a rewrite; on the `corpus/QUALITY.md` pair
it prints `raw_old_only=1593`, `norm_cr_old_only=5`, exit 1, with the class
never declared.

**After** (receipt `.ufo/evidence/round-74/addr-r74.txt`; measured commit
`2e0ac486`):

```
$ python3 -I tools/additivity-range.py --repo . --manifest tools/additivity-range.json
ADDRANGE_ROW r73-log-declaration-append  … expect=hold     measured=hold     ok | walked=1 changed=1 worst=17cd19396b36 raw_old_only=0 …
ADDRANGE_ROW r73-log-post-wave-append    … expect=hold     measured=hold     ok | walked=1 changed=1 worst=e309f59f4007 raw_old_only=0 …
ADDRANGE_ROW r73-log-eol-rewrite         … expect=violated measured=violated ok | walked=1 changed=1 worst=862e88444817 raw_old_only=3484 norm_cr_old_only=0 …
ADDRANGE_ROW r73-quality-append          … expect=hold     measured=hold     ok | walked=1 changed=1 worst=be1199d3874d raw_old_only=0 …
ADDRANGE_ROW r73-quality-criterion-pin   … expect=violated measured=violated ok | walked=1 changed=1 worst=21a7332f4d53 raw_old_only=1593 norm_cr_old_only=5 …
ADDRANGE_ROW r73-log-range-total         … expect=violated measured=violated ok | walked=1 changed=1 worst=3d6ea1ee8e55 raw_old_only=3484 norm_cr_old_only=0 …
ADDRANGE: rows=6 met=6 unexpected=0                       exit 0
ADDRANGE_TOTALS raw_old_only=8561 norm_cr_old_only=5
```

The two round-73 closure defects now stand as measured rows at their own
commits (routed defects 1 and 2 of
`corpus/lessons/round-73-verifier-spotcheck.md` §6), and the tool's own
selftest carries the three classes as arms:
`ADDITIVITY_RANGE_SELFTEST: 8/8 pass` (clean append holds; EOL rewrite
violates the raw class; the same rewrite reads `hold` under the content class;
a flipped `expect` measures `unexpected=1`; the pair kind; zero rows, an
unresolvable rev and an unknown claim are setup exit 2).

**Number note (honesty).** The closure printed `raw_old_only` 3,759 (LOG) and
1,915 (QUALITY) for its range views; this instrument's set-based predicate
measures 3,484 and 1,593 at the same own-commit pairs (and 3,484 for the LOG
range total). The difference is the predicate (set difference collapses
duplicate lines; the closure's accounting counted lines). The defect class —
raw lines removed, normalized zero — is identical under both.

**Controls** (receipt `.ufo/evidence/round-74/controls-r74.txt`).

1. **Class distinction.** The same rows under `claim: append-only-content`:
   the LOG rewrite reads `hold` (`norm_cr_old_only=0`) while its `raw_old_only`
   stays 3,484; the QUALITY row reads **violated** (`norm_cr_old_only=5`) —
   because that commit also contains the declared criterion-122 re-pin. The
   two classes are distinct measurements, and the QUALITY row is the proof that
   the content class is not blind: it sees the real edit and nothing else.
   **Frozen-text defect:** plan control clause (iv) said the flipped manifest
   "reads hold for both" rewrite rows; the QUALITY row cannot read hold because
   of those 5 lines. Reported, never repaired after data (the r72/r73
   precedent). The claim is unaffected: its predicate is the six-row line.
2. **Expect flip.** `r73-log-eol-rewrite` with `expect: hold` →
   `ADDRANGE: rows=6 met=5 unexpected=1` exit 1 — the red row is load-bearing.
3. **Do-nothing.** The existing per-pair tool exits 0 on the LOG rewrite pair
   with no `ADDRANGE` line; it cannot reach the frozen line.
4. **Echo stub.** A six-line shell stub prints `ADDRANGE: rows=6 met=6
   unexpected=0` and exit 0 **without any git read** — the summary tally alone
   is spoofable (the round-73 S07 counter-cheat class, restated). The stub's
   `ADDRANGE_TOTALS` line reads `raw_old_only=0 norm_cr_old_only=0` against the
   real `8561` / `5`, so the totals line carries derived populations the tally
   does not; the line is a receipt, never an authenticator.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| unsubstituted-template | the first `w1-spec.json` shipped literal `{lane}` and `{scratch}` in all 12 item texts: `item()` composed the prompt without the `.replace()` pass the shared context got, and the validator's `plan` output shows it verbatim (`.ufo/waves/round-74/w1-plan.json`). Caught before the ready file. | the renderer's own plan output (a seat would have read `Read {lane}/plans/…` and stopped); nothing in the round's checklist counted the braces. | `item()` now substitutes and asserts no placeholder survives (`gen-spec.py`), the spec was regenerated (28,380 B) and validated exit 0 before dispatch. |
| fixture-prefix-drift | arm15's first run read `FAIL (got=drift want=meet)`: `SEAT_FILES` used `x/…` paths while the artifact dir key is `wave`, so the prefix filter matched nothing and arm3 had measured `files=0` since round 73 (a passing arm on the wrong population). | the new arm: a discriminator that expected `meet` cannot pass on a zero population. | the fixture paths moved under `wave/` (arm3 now measures `files=12`, arm15 `12` vs the any-depth mutant's `13`); the round's own mutant battery re-proves arm15. |
| frozen-control-unattainable | plan control clause (iv) claims both rewrite rows read `hold` under `append-only-content`; measured, `corpus/QUALITY.md` reads `violated` (`norm_cr_old_only=5`) because that commit carries the criterion-122 re-pin. | wave seat T74W1R2, which measured the parent pair independently and refused to report `hold`. | reported as a frozen-text defect with the measurement; the operative predicate (the six-row line) is unchanged and the class distinction is demonstrated on the LOG row plus the QUALITY row's 5-line visibility. |

## Gate — census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… warnings only (18 × W04, 1 × W01 S101)
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

Start: exit 0, 163 rows (`.ufo/waves/round-74/census-start-r74.txt`). After the
round's append: 164 rows plus S294's in-place `used-by` change, exit 0
(`.ufo/waves/round-74/census-end-r74.txt`).

## Appended — corrections (wave seats S1 and R2, append-only)

1. **Quote 2's line numbers.** The Gate block above cites S294 Quote 2 at page
   lines `2678–2679`; seat T74W1S1 re-fetched the page (byte-identical sha256)
   and measured the 9-word string "Line endings are normalized to LF in the
   index" at **lines 2679–2680**. The quote, its scope and its use are
   unchanged; the page line numbers are corrected here, not in the block above
   (append-only discipline).
2. **The plan's arm15 illustration.** `plans/round-74.plan.md` describes the
   nested fixture as `x/nested/deep.md`; the landed fixture constant puts every
   seat path under `wave/` (the artifact dir key), so the nested file is
   `wave/nested/deep.md`. With the `x/` prefix the listing filter matches
   nothing and the arm would measure a zero population — the round's own
   `## Mistakes` row records that failure and the repair.
3. **The plan's control-4 wording.** It says "the same eight-row manifest" for
   a six-row manifest; the number is a typo, the class-control procedure is the
   one measured in `## What was measured — R74-C2` (controls 1) — and its
   clause (iv) is the frozen-text defect recorded above.

## Appended — arm hardening (wave seat T74W1R1) and the final measured bytes

Seat T74W1R1 measured that arms 13 and 14 asserted only "some SetupError": a
mutant that renamed either diagnostic to an unrelated refusal kept the suite at
15/15. The arms now assert their **named** refusal
(`printed-not-in-span` / `span-not-in-record`) through `arm_raises()`, which
prints `got=setup:<reason> want=setup:<reason>`; the arm count is unchanged and
`arm_raises()` cannot make a passing suite easier (it compares the reason the
tool already produced). Re-run on the hardened bytes (tool sha256
`97bb9272afb6c243cf7fb2dfde7bd34b90b4bcd769974d112ca574fccafd21fa`; the block
above cites the pre-hardening `9532c12b…`, 23,238 B, as measured before the
seat returned):

```
$ python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -3
SELFTEST arm13-printed-undelimited-refused    ok (got=setup:printed-not-in-span want=setup:printed-not-in-span)
SELFTEST arm14-span-not-in-record-refused     ok (got=setup:span-not-in-record want=setup:span-not-in-record)
SELFTEST arm15-seatreports-top-level-only     ok (got=meet want=meet)
WAVE_RECONCILE_SELFTEST: 15/15 pass                       exit 0
$ bash tools/mutate-and-run.sh … (the frozen spec)
CONTROL: GREEN (exit=0 …)
DEFECT m2-delimited-tautology: KILLED (exit=1 …)
DEFECT span-rule-removed: KILLED (exit=1 …)
DEFECT seat-reports-any-depth: KILLED (exit=1 …)
MUTATE: DONE (target=wave-reconcile-arms defects=3 killed=3 survived=0 inconclusive=0 kill-rate=100%)
```

Seat T74W1R1 also measured that removing `_record_claim` from only the
`roles`/`attack_share` branches leaves 15/15: arm14 therefore must not be
described as covering the round-73 every-kind binding hardening. This lesson
does not claim that; the hardening's own arms are T73W1S03's and the round-73
record stands.

## Appended — Gate: wave attacks (adopted, refuted, carried)

- **T74W1R1 (reviewer) — `[adopted]` named-refusal assertions for arms 13/14.**
  Landed (see above); the frozen kill rule's clause (iii) (pre-existing arms
  unchanged) and the arm count are untouched.
- **T74W1R1 — `[disclosed]` arm3's population moved.** The fixture repair
  changes arm3's hidden detail from `files=0` to `files=12` (and `13` under
  W2) while its exposed `got=drift`/`ok` stay unchanged. The round does not
  claim the old population was unchanged; it claims the outcome was.
- **T74W1R1 — `[carried]` arm14 is not exhaustive kind coverage.** A selective
  bypass of `_record_claim` on roles/attack_share alone survives; the next
  round's arm.
- **T74W1R2 (reviewer) — `[adopted]` the echo stub is rejected by the totals
  line.** It measured that an expect-only stub prints the frozen summary with
  zero git reads, and that it cannot print `ADDRANGE_TOTALS raw_old_only=8561
  norm_cr_old_only=5` (the independently confirmed sums 3484 + 1593 + 3484 and
  0 + 5 + 0). The round states the summary line is a receipt, never an
  authenticator; the totals line is the derived-population field that makes the
  echo stub insufficient for THIS frozen line.
- **T74W1R2 — `[confirmed]` the frozen normalized/content clauses are
  unattainable for the QUALITY row** (norm 5, not 0). Frozen-text defect,
  reported above; the operative predicate (the six-row line) stands.
- **T74W1M1 (mutation-tester) — `[measured]` independent arm liveness.** Its
  four self-designed mutants (plus the three named) were scored against the
  three new arms; the kill matrix in `T74W1M1.md` names which arm catches which
  and which new arm catches nothing. The 12 pre-existing arms still pass on its
  arm-added copy.
- **T74W1S1 (scribe) — `[confirmed]` the fetch and locators** (byte-identical
  sha256, no credential headers, 4/5 quotes exact, one line-number correction
  above) and an independent plain-git re-derivation of the two rewrite rows
  under its own line-counting predicate (raw 3801/3759 and 1925/1920 across the
  range, CR-blind 42/0 and 10/5 at the same commits): different predicates,
  same defect class, and the direction of every number agrees with the
  instrument's set-based 3484/1593.
- **T74W1SN1 (sentinel) — `SECRETS=0`, `TMPDIR` honoured** by
  `tools/mutate-and-run.sh` in all three modes, `SCOPE` 0/12, and no hardcoded
  `/tmp` root in the round's design (`plans/round-74.plan.md:172` is the line
  that requires honouring it).
- **T74W1SC1 (scout) — `[adopted as evidence]` the registry's `source` anchor
  is format-only** (never opened or compared to `argv`) and `scratch_root` is
  documentation prose nothing reads. The four rows this round added are honest
  under that contract; the round does not claim the anchors are verified by the
  monitor.
- **T74W1CN1 (connector) — `[reported]` cross-lane census** (`rev-list` 598
  files, `append-only` 3159, `ignore-cr-at-eol` 4, `norm_cr` 6): the mechanism
  is not claimed general on this census; PROVINCE's two-lane bar is unmet until
  a sibling gate ships a range-additivity sweep of its own.

Correction to the T74W1M1 bullet above (measured, append-only): no new arm is
dead — M-A, M-B and M-D are each killed by the arm they target (arm13, arm14,
arm15) — but a **fourth independent mutant survives all fifteen**:
`M-C` binds the printed integer to the whole RECORD text instead of the row's
span and reads `15/15 pass`. The fixture population has no row whose number is
delimited in the record but not inside its span, so arm13 cannot distinguish
span-bound from record-bound delimitedness; that arm is the named next-round
carry (`T74W1M1.md` §4–§5). The claim is unaffected — the three frozen mutants
die on their named arms — but this lesson does not present the suite as
covering the rule's binding scope.

## Appended — counter extension and the fixes the wave forced (seats C1, R2)

Wave seat T74W1C1 measured that **every frozen `commits` row spanned exactly
one commit**, so the pre-existing per-pair recipe reproduced the frozen line
and the totals: the range mode was carried by no row. Adopted in-round, with
the frozen six-row line kept as the claim's predicate and re-run at the frozen
commit:

- the manifest grows to **11 rows** and now carries two whole-range walks —
  `r73-log-range-walk` (`a3dd3574..3d6ea1ee`, 24 commits walked, 4 changed,
  worst `862e8844`) and `r73-quality-range-walk` (21 walked, worst `21a7332f`)
  — plus the three missing commit-pairs (`corpus/SOURCES.md` at `be1199d3` and
  `1d118c14`, `LOG.md` at `bbb7b189`), so all eight monitored-file commit-pairs
  of the round-73 range are covered;
- the walk's product is the **attribution**: a `pair` row over the same
  endpoints prints `worst=3d6ea1ee` and cannot name the middle commit, measured
  in `controls-r74.txt` control 5;
- the extended line is `ADDRANGE: rows=11 met=11 unexpected=0` exit 0 with
  `ADDRANGE_TOTALS kind=commits-union keys=8 raw_old_only=5079
  norm_cr_old_only=7` (`.ufo/evidence/round-74/addr-r74.txt`); the frozen
  six-row predicate re-runs byte-identically at `2e0ac486`
  (`rows=6 met=6 unexpected=0`, `.ufo/evidence/round-74/frozen-six-row-r74.txt`).

Two defects the same seat found, both fixed in the tool:

- **Totals double-counted.** The first totals line summed rows, so the pair row
  and the single-commit row added `LOG.md@862e8844` twice (`8561`); the union is
  now over `kind: commits` rows keyed `(file, worst commit)` → `5079 / 7`.
- **`walked=` printed the changed count** (it was passed twice); it now prints
  `len(rev-list)` and `changed=` the changed count, and the frozen six rows'
  verdicts are unchanged by the fix.

**Labels corrected (seat C1).** `be1199d3` is the S066 **damage** commit (the
`used-by` append that collapsed the row to eight fields — the round-73
`destructive-prefix-edit` mistake), and `1d118c14` is the **repair**. Both
measure `raw_old_only=1`; neither note calls the damage commit a repair.

**Echo-stub disclosure (updated).** With the totals line now containing the
derived union, a stub that types those numbers can print them too
(`controls-r74.txt` control 3). No printed line is an authenticator: the
defence is that the numbers are re-derivable per row (and were re-derived
independently by seats T74W1E4, T74W1R2 and T74W1C1), never that the line is
unforgeable.

**Class control, re-measured on the 11 rows** (control 1): under
`append-only-content` the LOG rows read `hold` (the rewrite is invisible) while
the rows whose commits also changed content read `violated` (`corpus/QUALITY.md`
norm 5; `corpus/SOURCES.md` norm 1 twice), i.e. `rows=11 met=7 unexpected=4`.
That is the class distinction working as designed — and it is the second,
stronger measurement of the frozen-text defect recorded above (clause (iv)
cannot read `hold` "for both" rewrite rows; here four rows legitimately cannot).

**Frozen-text defects (C1, recorded not repaired).** The plan's expected
`MUTANTS:` token is never printed by the runner (it prints `MUTATE: DONE
(target=… defects=3 killed=3 survived=0 inconclusive=0 kill-rate=100%)`,
receipt `battery-r74.txt`), and kill-rule (v)'s "an always-fail arm is not a
kill" reads inverted as written; the operative C1 counters (15/15, killed=3,
named-arm kills, 12 pre-existing arms unchanged) are unaffected.

## Appended — S294 `used-by` old→new (round 76)

The round-74 verifier spotcheck's defect 5 records that this lesson's Gate
named only the added path; the old→new pair lived in the round's report and
the SOURCES `Round 74` note. Recorded here, append-only, so the lesson
carries its own curation delta:

- S294 (`gitattributes`) `used-by` old → new: `corpus/lessons/round-63.md`
  → `corpus/lessons/round-63.md, corpus/lessons/round-74.md`.
