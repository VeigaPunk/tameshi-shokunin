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
