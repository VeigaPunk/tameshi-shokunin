# tameshi round 75 — lesson

Round 75 (attempt 1), base `21ef81e99966198cf8cdb2c6d8e56aa3c482da56`
(`= origin/master`, clean tree — the **admitted** round-74 non-author closure,
`corpus/lessons/round-74-verifier-spotcheck.md` §7). Claims, counters, kill
rules, arms and controls are frozen **before any claim data** in
`plans/round-75.plan.md` (declaration commit
`640d3fccfba7f6fab8e0341723b0fe6dbc200570`; pre-freeze correction 1 at
`7745d0e0`, append-only, carrying the L1's own 18-arm candidate battery).
Round shape: one v1 wave, 12 seats (4 executor · 1 scribe · 1 scout · 2
reviewer · 1 critic · 1 mutation-tester · 1 connector · 1 sentinel; attack
seats 4 = 33.3 %), policy `scripts/hyaku/ufo-wave-policy.json`, band 8–16.
`labrat` is a frozen-topology seat the validator rejects, so no labrat item
exists; the planner seat stays with the L1 per the orchestrator ruling.

Saturation state at round start (`SCORECARD.md`): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. A
capability entered the table at round 74 (`round-range additivity sweep`), so
the stagnation window (N = 2) is **not** exceeded and the nudge does not fire.
C2 works the lowest scored numeric axis (calibration 8).

## Gate — the source (S006 re-opened)

**S006 — re-open, not a new row.** `shmutant README (BWBama85/shmutant)` is
already held (opened 2026-10-19, tier A `code`, status `mined`, recheck `90d`,
anchor cell `shmutant's own bash mutation verdict semantics`) at page
`currentOid 7eefc73010ad6342b80e3ed43915503e02c90618`
(`corpus/SOURCES.md:17`). This round's three arms rest on the same document's
§The three verdicts and §How a row is run — the witness-scoped verdict and the
refuse-what-you-cannot-apply discipline — so a second row on the same URL would
be a within-scope duplicate (CORPUS.md rule 2; the S289/S293 precedent). The
curation delta is a **re-open**: S006's `used-by` cell gains
`corpus/lessons/round-75.md` and this Gate carries fresh located quotes. The
row's status, `recheck` and anchor stay as written (append-only).

- Source: shmutant README, BWBama85/shmutant. The row's canonical URL is
  <https://github.com/BWBama85/shmutant>; the document opened this round is the
  README at
  <https://raw.githubusercontent.com/BWBama85/shmutant/master/README.md>.
  Fetched 2026-11-04 (HTTP/2 `200`; HTTP date `Wed, 04 Nov 2026 02:22:03 GMT`;
  13,970 B; sha256
  `960577288ed5c5eb80f42669fcb30bf254b9a917ae2bde3a117888056ef354e2`; extract
  `.ufo/evidence/round-75/sources/s006-shmutant-readme.md`, headers
  `.ufo/evidence/round-75/sources/s006-headers.txt`). The extract's measured
  byte count equals the receipt's `content-length: 13970`. Header hygiene:
  `grep -ic set-cookie` → `0`; no credential-bearing header value. Held-page
  dedupe: `grep -c 'BWBama85/shmutant' corpus/SOURCES.md` → `1`. Identity note:
  the row's held anchor names `currentOid 7eefc730…` (its 2026-10-19 open),
  while this re-open's quotes are located on the fresh `master` extract — if the
  page has moved past that oid, the quotes above stand on the fresh bytes and
  the row's anchor stays as written; `<L1 fills: the snapshot-identity pair
  (held oid vs fresh head) and, if they differ, the one-line disclosure.>`
- Quote 1 (extract line 24, 6 whitespace tokens): "**witness**: the assertion
  that must fail." — a row is scored against the assertion that **must** fail,
  not against the observation that something failed. The fixture rule the new
  arms inherit: an arm is a witness, and a red for any other reason is not its
  kill (plan kill rule (ii), corrected pre-freeze).
- Quote 2 (extract line 29, 12 whitespace tokens): "The suite went red **on its
  witness**. The test detects the defect." — the verdict is
  **witness-scoped**: red is not enough; red *on the named witness* is the kill.
- Quote 3 (extract line 31, 21 whitespace tokens): "The suite went red, but not
  on its witness. Caught by accident, not by the assertion that claims to cover
  it." — an accidental red banks as `accidental`, never as a kill; the harness
  scores the scope, not the colour.
- Supporting locators on the same snapshot (the C1 fixtures rest on these two,
  and they are verified here with the three above): the `unapplied` row
  (extract line 38, 13 tokens): "The old literal matched nothing. The row
  injected no defect and tests **nothing**." — a row that cannot apply its
  binding is a *refusal*, never a pass; and the whole-token rule (extract lines
  101–102, 13 tokens): "carries the witness as a whole token (`parse-empty` is
  not found in `parse-empty-list`)" — a witness is a whole token, never a
  substring, which is exactly the `M-C` class the round installs (a delimited
  occurrence anywhere in the record is not a delimited occurrence *inside the
  bound span*).
- Verification of the quotes (this seat's own, not the fetch seat's):
  `grep -c -F` on each single-line quote → `1`; the two-line quote is the exact
  substring spanning extract lines 101–102, and `grep -n -F` locates both
  endpoints (`that carries the witness as a whole token` at 101,
  `` `parse-empty-list` `` at 102). Line spans and token counts above are
  measured on the extract at the sha256 recorded above. The L1's own reading
  (`.ufo/evidence/round-75/sources/s006-quotes.txt`) carries the same three
  primary locators (witness definition, `killed`, `accidental`).
- **Admit:** S006's witness-scoped re-open (the three located quotes above; the
  row's status, recheck and anchor stand as written).
- **Reject (standing, re-sampled):** a new `shmutant` row at the current bytes —
  same URL, same document, within-scope duplicate (CORPUS.md rule 2; the
  S289/S293 and S073/S103 precedent). Flip condition: S006 is retired or the
  README is superseded by a new document, at which point the successor is a new
  document with a new row.
- S006 `used-by` old → new:
  `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md, corpus/lessons/round-12.md`
  → `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md, corpus/lessons/round-12.md, corpus/lessons/round-75.md`.

### Gate — census

Start: exit 0, 164 rows (`.ufo/evidence/round-75/census-start.txt`; row count
re-derived by this seat with `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` →
`164` at the declaration tip, whose `tools/` bytes are identical to the base —
`git diff --stat 21ef81e9..7745d0e0 -- tools/` is empty). Warnings only — 18 ×
`W04` duplicate-url across scopes and 1 × `W01 S101`, the standing set.

After: `<L1 fills: end-census exit code and row count. The round adds no SOURCES
row (S006 is re-opened in place), so the expected row count is 164; the receipt
must be committed under .ufo/evidence/round-75/ and read exit 0.>`

## Claims

### R75-C1 — operability: the three round-74 survivors become measured arms

**Before** (measured at base, receipt `.ufo/evidence/round-75/base-measure-c1.txt`):
`git show 21ef81e9:tools/wave-reconcile.py | sha256sum` →
`97bb9272afb6c243cf7fb2dfde7bd34b90b4bcd769974d112ca574fccafd21fa`; the same
sha256 at the declaration tip (`sha256sum tools/wave-reconcile.py`).
`python3 -I -X utf8 <pristine> --selftest` → `WAVE_RECONCILE_SELFTEST: 15/15
pass`, exit 0. Three single-edit mutants built from those bytes each read
`15/15 pass`:

| mutant | the edit | what it widens |
|---|---|---|
| `M-C` record-bound printed | `_record_claim` binds `printed` to the decoded RECORD text instead of `rec['span']` | a number delimited anywhere in the record passes for a number in the span |
| `roles-bypass` | `_record_claim(row, readers)` deleted from the `roles` branch only | roles rows skip the record-span binding |
| `attack-bypass` | the same deletion in the `attack_share` branch only | attack_share rows skip the record-span binding |

Verdict: the 15-arm suite reads `15/15` on pristine **and on all three
mutants** → `M-C`, `roles-bypass` and `attack-bypass` SURVIVE. Do-nothing
control: installing no arm leaves `15/15` and every named mutant alive.

**After (frozen target; not yet measured on the landed bytes).** Three arms are
added — `arm16-printed-span-not-record` (`printed` must be delimited INSIDE the
bound span, not merely somewhere in the record), `arm17-record-claim-live-on-roles`
and `arm18-record-claim-live-on-attack-share` (each branch binds the record span
before measuring) — and each R75 mutant dies on its named arm and on no other.
The six-defect runner spec (`tools/wave-reconcile-mutants.spec`, three round-74
defects plus three new ones) kills all six.

Counting commands (frozen in the plan):

```sh
python3 -I -X utf8 tools/wave-reconcile.py --selftest | tail -1
bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
  --defects tools/wave-reconcile-mutants.spec \
  --suite 'python3 -I -X utf8 "$MUTANT" --selftest' \
  --workdir "$HYAKU_SCRATCH/tameshi-r75/l1/battery" --label wave-reconcile-arms-r75
```

Target after-state: `WAVE_RECONCILE_SELFTEST: 18/18 pass` exit 0; the battery
prints `CONTROL: GREEN`, each of the three new defects `KILLED` with its FAIL
line on its **named** arm only (`arm16`/`arm17`/`arm18`), the suite at `17/18`
under each new mutation, `MUTATE_RESTORE: OK` byte-identical, and `MUTATE: DONE
(… defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)`.

**Measured after-state:** `<L1 fills: the two commands' exact output at the
landing tip, plus the measured commit and the tool sha256. This seat measured no
after-state.>` The L1's pre-freeze candidate battery
(`.ufo/evidence/round-75/l1-c1-battery.txt`, candidate sha256 `c5dffb12…`,
25,410 B) already reads `18/18 pass` and `defects=6 killed=6`, but those are the
**candidate's** bytes, not the landed tool's — it is evidence for correction 1,
not for the claim.

**Kill rule (frozen, with pre-freeze correction 1).** C1 fails if (i) any of the
three named R75 mutants still passes every arm; (ii) any of the three R75
mutants is killed by an arm other than its own named arm (corrected pre-freeze;
the plan's first wording could not hold once `arm16` also exercised
`delimited()` and `arm17`/`arm18` the record-span guard — a pre-existing mutant
must keep its named-arm kill, and collateral failures of the round-74 mutants on
the new shared-code arms are expected and are not disqualifying: measured
pre-freeze, `m2` fails `arm13` and `arm16`, the span-rule mutant fails `arm14`,
`arm17` and `arm18`); (iii) any pre-existing arm 1–15 changes its `ok`/`got`
outcome; (iv) the arm count is not exactly 18; (v) a new arm fails on the
unmutated copy (an always-fail arm is not a kill); or (vi) the battery control
is not GREEN or the restore is not byte-identical.

### R75-C2 — calibration: the live capability figures re-derive from their instruments

**Before** (measured at base, receipt `.ufo/evidence/round-75/base-measure-c2.txt`):
the pre-freeze control scan
(`.ufo/evidence/round-75/selfstate-control-scan.py`) reads the SCORECARD
`## Capabilities` table at `21ef81e9` and compares 16 declared figure spans
against the lane instruments that print them:
`SELFSTATE_CONTROL: rows=16 match=9 stale=7`, exit 1. The seven stale figures
are the commit-bind selftest (`4/4` vs `7/7`), the quoted-line selftest (`4/4`
vs `5/5`), the arm-liveness selftest (`4/4` vs `5/5`), the arm-liveness standing
sweep (`rows=3 live=3 dead=0` vs `rows=9 live=9 dead=0`), the anchor-drift sweep
(`rows=4` vs `rows=16`), the line-pointer sweep (`rows=8` vs `rows=12`) and the
additivity sweep (`rows=6` vs `rows=11`). At the declaration tip
`tools/selfstate-freshness.py` and `tools/selfstate-freshness.json` do not exist
(`ls` → `No such file or directory`).

**After (frozen target; not yet measured).** `tools/selfstate-freshness.py` +
`tools/selfstate-freshness.json`: a declared population of 17 rows — 16 live
capability figures (`mode: capability`, located by exact first-cell name in the
`## Capabilities` section at `--doc-rev`) and 1 frozen historical statement
(`mode: span`: the round-74 block's `ADDRANGE: rows=6 met=6 unexpected=0` line,
`expect: stale`). Each row carries the figure regex and the instrument (path,
pinned rev, argv); the instrument is extracted from git objects at its rev and
run `python -I -X utf8` with `TMPDIR` honoured, and its stdout is searched with
the same regex. `match` when the doc's figure equals the instrument's;
`expect: match|stale` makes a divergence `unexpected`. An absent capability row
or absent figure is a **setup refusal (exit 2)**, never a pass.

Counting command (frozen in the plan):

```sh
python3 -I -X utf8 tools/selfstate-freshness.py --repo . \
  --manifest tools/selfstate-freshness.json --doc-rev <rev> | tail -1
```

Target after-state at the landing tip: `SELFSTATE: rows=17 match=16 stale=1
unexpected=0`, exit 0, with every live row reading `match` and the frozen row
reading `SELFSTATE_ROW r74-frozen-addr-six expect=stale measured=stale ok`.

**Measured after-state:** `<L1 fills: the counting command's exact output at the
landing tip, plus the measured commit. This seat measured no after-state.>`

The seven live repairs this forces (SCORECARD capability cells, superseded in
place with the historical receipts left untouched; carried as a row manifest in
`.ufo/evidence/round-75/repairs-r75-l1.json`): commit-bind `4/4` → `7/7`;
quoted-line `4/4` → `5/5`; arm-liveness `4/4` → `5/5` and `rows=3` → `rows=9`;
anchor-drift `rows=4` → `rows=16`; line-pointer `rows=8` → `rows=12`;
additivity `rows=6` → `rows=11`.

**Kill rule (frozen).** C2 fails if (i) `unexpected≠0` at the landing tip;
(ii) any declared live capability row is absent from the table or its figure
regex matches nothing (setup refusal is a failure to measure, not a pass);
(iii) the frozen red row does not measure `stale`; (iv) the row population is
not exactly 17; or (v) a row's `measured` value is not the instrument's own
stdout token (an echo/copy of the doc is not a measurement — the instrument
prints `measured=` per row and the receipt carries the raw instrument stdout).

**Before-state note for the same instrument.** The plan predicts `SELFSTATE:
rows=17 match=9 stale=8 unexpected=7` exit 1 when the new instrument is pointed
at `21ef81e9`. That line is a **frozen expectation, not a measurement** — the
instrument did not exist at freeze time. `<L1 fills: the measured base-state line
once the instrument exists, or names the plan's line as the expectation.>`

**Controls (pre-data, `.ufo/evidence/round-75/controls-c75.txt`).** (1)
Do-nothing: the same scan at `21ef81e9` reads `stale=7`, so
`unexpected=0` is unreachable by doing nothing. (2) Echo stub: a counter that
copies the doc's own figure reads `stale=0`; the count alone is not
self-authenticating, so the receipt carries the per-row `measured=` tokens and
the frozen red row must read `stale` on every sweep. (3) Always-fail arm: an arm
that fails on the unmutated copy is visible on it (the control reads
`15/16`), so it cannot be counted as a kill. (4) Row-deletion: a manifest row
whose capability no longer resolves is a setup refusal (exit 2), so deleting a
row cannot lower the count.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `number-drift` / `stale-premise` | a live capability row printed a figure no instrument prints any more. Round-74 closure defect 3 (`corpus/lessons/round-74-verifier-spotcheck.md` §6 item 3) caught two by eye — `SCORECARD.md:262` quoted `WAVE_RECONCILE_SELFTEST: 12/12 pass` while the tip printed `15/15`, and `:264` quoted `rows=6` while its own cited tip receipt read `rows=11`. The round-75 control scan then measured the whole population: seven of sixteen declared live figures stale (`.ufo/evidence/round-75/base-measure-c2.txt`, `SELFSTATE_CONTROL: rows=16 match=9 stale=7`, exit 1). | `none` — no instrument read a capability figure back from the instrument that prints it; the two known cases were found by a spot-check, not by a gate, and the other five were invisible until a counter was written to compare spans against stdout. | `tools/selfstate-freshness.py` + `tools/selfstate-freshness.json` (16 live rows + 1 frozen row; each `measured` token is the pinned instrument's own stdout, an absent row or figure is setup exit 2) and the new QUALITY criterion 125 (draft: `.ufo/waves/round-75/w1/T75W1S1/quality-criterion.md`). |
| `reference-drift` | the pre-freeze control prototype derived its repo root from `__file__` and its first run measured nothing (`plans/round-75.plan.md:168-169`, the mistake named at freeze time). The surviving corrected prototype names the root explicitly instead (`LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'`, `.ufo/evidence/round-75/selfstate-control-scan.py:8`), and the receipt it produced reads `SELFSTATE_CONTROL: rows=16 match=9 stale=7` (`.ufo/evidence/round-75/base-measure-c2.txt`). | the instrument's required `--repo` (the C2 instrument takes the root on argv and derives nothing); the corrected prototype's explicit constant is the same rule in fixture form. | explicit `--repo`, no derivation: the instrument requires the repository path on argv, and the prototype names the lane root as a constant rather than computing it from `__file__`. A root that cannot be named is a setup refusal, never a silent zero-population sweep. |
