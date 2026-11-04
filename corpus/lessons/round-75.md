# tameshi round 75 — lesson

Round 75 (attempt 1), base `21ef81e99966198cf8cdb2c6d8e56aa3c482da56`
(`= origin/master`, clean tree — the **admitted** round-74 non-author closure,
`corpus/lessons/round-74-verifier-spotcheck.md` §7). Claims, counters, kill
rules, arms and controls are frozen **before any claim data** in
`plans/round-75.plan.md` (declaration commit
`640d3fccfba7f6fab8e0341723b0fe6dbc200570`; pre-data corrections 1 and 2 at
`7745d0e0` and `82f7a809`, append-only, both driven by the round's own wave
seats and the L1's pre-data controls). Round shape: one v1 wave, 12 seats
(4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects, so no labrat item exists; the planner seat stays
with the L1 per the orchestrator ruling.

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
  byte count equals the receipt's `content-length: 13970`; the repo's default
  branch is `main` (the `/master/` URL is GitHub raw's legacy alias; `/main/`
  returns the same bytes — the wave's source seat measured both plus a 404
  negative control). Header hygiene: `grep -ic set-cookie` → `0`; the only
  `authorization` occurrence is the `Vary: Authorization,Accept-Encoding`
  request directive, not a credential value.
- Quote 1 (extract line 24, 6 whitespace tokens): "**witness**: the assertion
  that must fail." — a row is scored against the assertion that **must** fail,
  not against the observation that something failed.
- Quote 2 (extract line 29, 12 whitespace tokens): "The suite went red **on its
  witness**. The test detects the defect." — the verdict is
  **witness-scoped**: red is not enough; red *on the named witness* is the kill.
- Quote 3 (extract line 31, 21 whitespace tokens): "The suite went red, but not
  on its witness. Caught by accident, not by the assertion that claims to cover
  it." — an accidental red banks as `accidental`, never as a kill; the harness
  scores the scope, not the colour.
- Supporting locator (the C1 fixtures rest on it): the `unapplied` row (extract
  line 38, 13 tokens): "The old literal matched nothing. The row injected no
  defect and tests **nothing**." — a row that cannot apply its binding is a
  *refusal*, never a pass; the same refusal discipline is what the C2
  instrument applies to an absent capability, an absent figure, a
  multiply-matching figure, and an instrument stdout without the figure.
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

Start: exit 0, 164 rows (`.ufo/evidence/round-75/census-start.txt`). End:
exit 0, 164 rows (`.ufo/evidence/round-75/census-end.txt`); no SOURCES row is
added (S006 re-opened in place), warnings only (18 × `W04` duplicate-url
across scopes and 1 × `W01 S101`, the standing set). Next unused id: S305.

## Claims

### R75-C1 — operability: the round-74 survivors become measured arms

**Before** (measured at base, receipt `.ufo/evidence/round-75/base-measure-c1.txt`):
`git show 21ef81e9:tools/wave-reconcile.py | sha256sum` →
`97bb9272afb6c243cf7fb2dfde7bd34b90b4bcd769974d112ca574fccafd21fa`;
`--selftest` → `WAVE_RECONCILE_SELFTEST: 15/15 pass`. Three single-edit mutants
built from those bytes each read `15/15 pass` (all three survive the whole
suite):

| mutant | the edit | what it widens |
|---|---|---|
| `M-C` record-bound printed | `_record_claim` binds `printed` to the decoded RECORD text (`_`) instead of `rec['span']` | a number delimited anywhere in the record passes for a number in the span |
| `roles-bypass` | `_record_claim(row, readers)` deleted from the `roles` branch only | roles rows skip the record-span binding |
| `attack-bypass` | the same deletion in the `attack_share` branch only | attack_share rows skip the record-span binding |

**After** (measured on the landed bytes at `4e610748`, receipt
`.ufo/evidence/round-75/c1-landed-battery.txt`): the landed tool
(`sha256 bf10c0e4…`) reads `WAVE_RECONCILE_SELFTEST: 18/18 pass`, and the lane
runner over the landed `tools/wave-reconcile-mutants.spec`
(`sha256 7becb33d…`; its first three `@defect` blocks byte-identical to
`21ef81e9:tools/wave-reconcile-mutants.spec`) prints `CONTROL: GREEN`, each of
the six defects `KILLED`, `MUTATE_RESTORE: OK` (target sha256 identical
before/after) and `MUTATE: DONE (target=wave-reconcile-arms-r75 defects=6
killed=6 survived=0 inconclusive=0 kill-rate=100%)`. Each of the three R75
mutants fails **only** its named arm (`arm16`, `arm17`, `arm18`; 17/18 each).
The legacy collateral kills are the Correction-2 matrix (`m2` → arm13+arm16;
span-rule → arm14+arm17+arm18), intrinsic because those mutants delete the
shared rules the new arms assert. The rule (iii) baseline diff
(`c1-arms1-15-diff.txt`) has no output: arms 1–15 are byte-identical.

### R75-C2 — calibration: the declared live figures re-derive from their instruments

**Before** (frozen counter at base, receipt
`.ufo/evidence/round-75/c2-before.txt`): `SELFSTATE: rows=17 match=9 stale=8
unexpected=7`, exit 1. Seven live figures were stale: commit-bind `4/4` vs
`7/7`; quoted-line `4/4` vs `5/5`; arm-liveness `4/4` vs `5/5` and `rows=3` vs
`rows=9`; anchor-drift `rows=4` vs `rows=16`; line-pointer `rows=8` vs
`rows=12`; additivity `rows=6` vs `rows=11`. The 17th row is a frozen
historical statement (`ADDRANGE: rows=6 met=6 unexpected=0` in the round-74
block) declared `expect: stale` so the instrument measures staleness on every
sweep.

**After** (receipt `.ufo/evidence/round-75/c2-after-r75.txt`, measured against
the repair commit `4e610748`): `SELFSTATE: rows=17 match=16 stale=1 unexpected=0`
exit 0, every live row `match`, `r74-frozen-addr-six expect=stale measured=stale
ok`; selftest `SELFSTATE_SELFTEST: 10/10 pass`. The nine capability cells are
superseded row-scoped (`apply-repairs-r75.py`): the seven in-population figures
plus `mutation sweep runner` (`80/80` → `107/107`) and `wave-record
reconciliation` (`12/12` → `18/18`), both outside the frozen population and
reported as out-of-population record repairs. The population itself is the
frozen tuple table in `.ufo/evidence/round-75/selfstate-control-scan.py`
(16 live figures on 10 capability rows, instrument rev `21ef81e9`) plus the
frozen row; the landed manifest matches it tuple-for-tuple.

## What was measured — controls and the freeze they forced

- **Control 4 (loose token), measured** (`.ufo/evidence/round-75/controls-c75b.txt`):
  a manifest whose live-row regex is a token common to doc and instrument but
  **not** the figure (the verdict prefix, or `dead=0`) prints
  `SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0 at base with **zero
  repairs**. The wave critic built this control and the L1 reproduced it; it is
  why Correction 2 freezes the population to the committed prototype's tuples —
  a manifest that differs from that table is not the counter.
- **Echo stub** (`.ufo/evidence/round-75/controls-c75.txt`): the pre-freeze
  scan's echo variant reads `stale=0`; the per-row `measured=` tokens and the
  frozen red row are the discriminator, not the summary count.
- **Instrument mutants** (wave seat T75W1M1): five single-edit mutants of the
  instrument contract (doc-copy, expect-ignored, absent-capability-match,
  zero-rows-success, doc-rev-ignored) are each killed by a named selftest arm;
  the C1 side's three new arms are each killed on their named arm.
- **Repair scoping** (wave seats T75W1R2, T75W1E3): every old token occurs 3–5×
  in `SCORECARD.md` (historical blocks quote the same figures), so the repairs
  are bound to the capability row by exact first-cell name; the applier refuses
  a wrong-scope or non-unique match (exit 2, no partial write).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `number-drift` / `stale-premise` | a live capability row printed a figure no instrument prints any more. Round-74 closure defect 3 (`corpus/lessons/round-74-verifier-spotcheck.md` §6 item 3) caught two by eye; the round-75 control scan measured the declared population (`.ufo/evidence/round-75/base-measure-c2.txt`, `rows=16 match=9 stale=7`, exit 1) and the wave then found two more live cells stale outside it (`mutation sweep runner` `80/80` vs `107/107`; `wave-record reconciliation` `12/12` vs `15/15`, `.ufo/waves/round-75/w1/T75W1E3/sweep.txt`). | `none` — no instrument read a capability figure back from the instrument that prints it; the two known cases were found by a spot-check, not by a gate. | `tools/selfstate-freshness.py` + `tools/selfstate-freshness.json` (16 frozen tuples + one frozen row, fail-closed setup) and QUALITY criterion 125; the seven in-population cells and the two out-of-population cells are superseded row-scoped. The `pin-disposition`/`evidence-disposition` cells stay as dated literals under the round-17 disclosure (`SCORECARD.md:655-659`) and are a named round-76 carry. |
| `reference-drift` | the pre-freeze control prototype derived its repo root from `__file__` and its first run measured nothing (`plans/round-75.plan.md:168-169`); the surviving corrected prototype names the root explicitly (`.ufo/evidence/round-75/selfstate-control-scan.py:8`). | the instrument's required `--repo` (the landed C2 instrument takes the root on argv and derives nothing). | explicit `--repo`, no derivation. A second instance of the same class: relocating an instrument into a plain temp dir broke `tools/rekey-cost.py`'s `__file__`-relative support blob; the landed runner materialises the support blob from the same pinned revision (`git cat-file`) instead of relying on the worktree. |
| `scope` | the L1's live-mode `tools/registry-check.py` run executed the registry row `verify-round15`, whose script writes `.ufo/evidence/round-15/attempt-5/` and `verification-5.json` into the lane (created 23:22, before the wave; red by construction — a round-15-era tool-source pin superseded in round 55). Hashes and listing: `.ufo/evidence/round-75/round15-residue.txt`; the files were removed, not landed. | `none` — the live mode warns that rows may write into the lane, but nothing in the round's checklist required the hermetic `--rev` form. | run `registry-check.py --rev <rev>` (clone under TMPDIR, never the lane) for verification passes; the live form is for the owning lane to run knowingly. |
| `attribution` | the pre-freeze C1 battery receipt certified the L1's scratch `cand.py` (`c5dffb12…`), not the seat candidate that was landed (`bf10c0e4…`); a receipt is evidence only for the revision it names. | the wave sentinel (T75W1SN1 §5.1) and the L1's own landing step. | re-ran the battery against the **landed** tool and spec (`c1-landed-battery.txt`), so the C1 after-state's receipt names the landed bytes. |

## Findings routed to round 76

- `adv-seatreports-require-printed-bypass` (wave seat T75W1R1): dropping
  `require_printed=True` only in the `seat_reports` branch survives 18/18; the
  next arm needs a printed-less `seat_reports` row.
- The `pin-disposition` (`18/18` vs `19/19`) and `evidence-disposition`
  (`34/34` vs `66/66`) capability cells remain dated literals; the round-17
  supersession line's own values (`95/95`, `56/56`) are stale too.
- `tools/receipt-exists.py --selftest` leaves its `TMPDIR` scratch dirs behind
  (the sentinel measured 8 → 24 during the wave); a disk-guard defect in that
  instrument, not in this round's tooling.
- Round-73 routed items 3–4 (the contradicted kill-rule sentence with no
  erratum; the 22-of-23 landed table and the `19 × W04` census sentence) and
  the round-74 cold-read pointer erratum remain open.

## Settlement errata (append-only)

WAVE-DONE arrived after all 12 seats settled. T75W1M1's final reproduction
supersedes the earlier sentence above saying five instrument mutants were
each killed: **four were killed; `--doc-rev`-ignored survived 10/10** on the
landed tool. The production implementation reads the requested revision
correctly; its selftest lacks a CLI-level arm proving that binding. This is a
named round-76 carry, not a five-of-five result.

The plan's corrections were made while the wave was running. In particular,
Correction 2 followed the critic's scored counterexample; calling both
corrections "pre-data" above is too broad. The original frozen-text defects
and the post-score tuple freeze remain admission defects for the non-author
closure to judge; the measured improvements do not retroactively validate
the original predicates.

The C2 instrument is demonstrated, but its repertoire row was not added to
the live Capabilities table this round. The "capability to enter" language in
SCORECARD is intent, not an acquired capability row; no capability-acquisition
credit is claimed.
