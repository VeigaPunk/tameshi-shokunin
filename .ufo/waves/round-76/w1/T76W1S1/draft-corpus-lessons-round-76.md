# tameshi round 76 — lesson

<!-- DRAFT by seat T76W1S1 (godspeed). The L1 lands canonical bytes; every
     PLACEHOLDER marker below must be resolved by the L1 / scout / wave seats
     before landing. -->

Round 76 (attempt 1), base `451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0`
(`= origin/master`, clean tree — the round-75 non-author closure verdict
commit, `corpus/lessons/round-75-verifier-spotcheck.md` §7,
verdict `rejected-honest-stop`). Claims, counters, kill rules, arms and
controls are frozen **before any claim data** in
`plans/round-76.plan.md` (declaration commit
`5b7bbe1afa209b477bc71872d2424f6993e5c69d`; no pre-data corrections this
round — the two claims were frozen together with their design-phase
candidates, batteries and measured kill matrices in the same commit, and the
wave seats re-derive them independently). Round shape: one v1 wave, 12 seats
(4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a
frozen-topology seat the validator rejects, so no labrat item exists; the
planner seat stays with the L1 per the orchestrator ruling.

Saturation state at round start (`SCORECARD.md`): scored axes depth 10,
calibration 8, freshness 9 — all at or above the saturation line 8. No
capability entered the table at round 75 (the settlement errata declined
acquisition credit), so one capability-less completed round sits inside the
stagnation window (N = 2) and the nudge does **not** fire. C2 works the
lowest scored numeric axis (calibration 8).

## Gate — the source (S006 re-opened)

**S006 — re-open, not a new row.** `shmutant README (BWBama85/shmutant)` is
already held (opened 2026-10-19, tier A `code`, status `mined`, recheck `90d`,
anchor cell `shmutant's own bash mutation verdict semantics`) at page
`currentOid 7eefc73010ad6342b80e3ed43915503e02c90618`
(`corpus/SOURCES.md:17`; re-opened with fresh quotes at round 75,
`corpus/lessons/round-75.md` `## Gate`). This round's two arms rest on the
same document's §The three verdicts and §How a row is run — the
witness-scoped verdict and the refuse-what-you-cannot-apply discipline — so a
second row on the same URL would be a within-scope duplicate (CORPUS.md rule
2; the S289/S293 precedent). The curation delta is a **re-open**: S006's
`used-by` cell gains `corpus/lessons/round-76.md` and this Gate carries fresh
located quotes fetched this round. The row's status, `recheck` and anchor
stay as written (append-only).

<!-- WHERE THE SCOUT'S QUOTES GO — the scout seat fetches the README fresh this
     round and lands the receipts under `.ufo/evidence/round-76/sources/`.
     SKELETON (mirrors round-75.md `## Gate`):

- Source: shmutant README, BWBama85/shmutant. The row's canonical URL is
  <https://github.com/BWBama85/shmutant>; the document opened this round is
  the README at
  <https://raw.githubusercontent.com/BWBama85/shmutant/master/README.md>.
  Fetched PLACEHOLDER-ACCESS-DATE (HTTP/2 `200`; HTTP date
  PLACEHOLDER-HTTP-DATE; PLACEHOLDER-BYTES B; sha256
  PLACEHOLDER-SHA256; extract
  `.ufo/evidence/round-76/sources/s006-shmutant-readme.md`, headers
  `.ufo/evidence/round-76/sources/s006-headers.txt`). The extract's measured
  byte count equals the receipt's `content-length:`; the repo's default
  branch is `main` (the `/master/` URL is GitHub raw's legacy alias).
  Header hygiene: `grep -ic set-cookie` → PLACEHOLDER; the only
  `authorization` occurrence is the `Vary: Authorization,Accept-Encoding`
  request directive, not a credential value.
- Quote 1 (extract line PLACEHOLDER, N whitespace tokens): PLACEHOLDER —
  the round-75 quote was "**witness**: the assertion that must fail."
  (extract line 24, 6 tokens); re-quote fresh and confirm byte-identity.
- Quote 2 (extract line PLACEHOLDER, N tokens): PLACEHOLDER — round-75's was
  "The suite went red **on its witness**. The test detects the defect."
  (extract line 29, 12 tokens).
- Quote 3 (extract line PLACEHOLDER, N tokens): PLACEHOLDER — round-75's was
  "The suite went red, but not on its witness. Caught by accident, not by
  the assertion that claims to cover it." (extract line 31, 21 tokens).
- Supporting locator (the C1 fixtures rest on it): the `unapplied` row
  (extract line PLACEHOLDER, N tokens): PLACEHOLDER — round-75's was
  "The old literal matched nothing. The row injected no defect and tests
  **nothing**." (extract line 38, 13 tokens).

  END SKELETON -->

- **Admit:** S006's witness-scoped re-open (the fresh located quotes above;
  the row's status, recheck and anchor stand as written).
- **Reject (standing, re-sampled):** a new `shmutant` row at the current
  bytes — same URL, same document, within-scope duplicate (CORPUS.md rule 2;
  the S289/S293 and S073/S103 precedent). Flip condition: S006 is retired or
  the README is superseded by a new document, at which point the successor is
  a new document with a new row.
- S006 `used-by` old → new:
  `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md, corpus/lessons/round-12.md, corpus/lessons/round-75.md`
  → `corpus/knowledge/witness-scoped-kill-verdict.md, corpus/knowledge/mutation-score-semantics.md, corpus/lessons/round-12.md, corpus/lessons/round-75.md, corpus/lessons/round-76.md`.

### Gate — census

Start: exit 0, 164 rows (`.ufo/evidence/round-76/census-start.txt`; the
receipt's warning set is the standing 18 × `W04` duplicate-url plus 1 ×
`W01 S101`, and its final line reads
`tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`).
End: PLACEHOLDER (expected exit 0, 164 rows, receipt
`.ufo/evidence/round-76/census-end.txt`; no SOURCES row is added — S006
re-opened in place; warnings only, the standing set). Next unused id: S305.

## Claims

### R76-C1 — operability: the two round-75 survivors become measured arms

**Named survivors (round-75 carry).**
`adv-seatreports-require-printed-bypass` — dropping `require_printed=True` in
the `seat_reports` branch only survives the round-75 18-arm suite; measured
again at base this round: `.ufo/waves/round-76/l1/mut-base-bypass.out`,
`18/18 pass` on base bytes. `--doc-rev-ignored` — the selfstate instrument
mutant survived the round-75 battery 10/10 (`corpus/lessons/round-75.md`
Settlement errata); re-measured at base:
`.ufo/waves/round-76/l1/mut-base-docrev.out`, `10/10 pass`.

**Before** (measured at base `451ed5cb`, receipts in the design-phase commit
`5b7bbe1a`):
`git show 451ed5cb:tools/wave-reconcile.py | sha256sum` →
`bf10c0e490e78e3f98fdb580442916e685968a94ff8c3fc977dead4b74a7f791`;
`python3 -I -X utf8 tools/wave-reconcile.py --selftest` →
`WAVE_RECONCILE_SELFTEST: 18/18 pass` exit 0; the bypass mutant on base bytes
reads `18/18 pass`.
`git show 451ed5cb:tools/selfstate-freshness.py | sha256sum` →
`3b09676340fc63007d3a1e5de3e54471feddb22024a2f40bd4b3b469f560eba6`;
`python3 -I -X utf8 tools/selfstate-freshness.py --selftest` →
`SELFSTATE_SELFTEST: 10/10 pass` exit 0; the doc-rev-ignored mutant on base
bytes reads `10/10 pass`.
The design-phase base-tool survivor receipt
`.ufo/waves/round-76/l1/base-survivors.txt` carries all four lines verbatim:
`WAVE_RECONCILE_SELFTEST: 18/18 pass` (bypass mutant on base bytes, sha256
`58aeebc1a47e7cead2024bba9a33e9b318f299333f6346dc4248b0f448ddfd1a`),
`SELFSTATE_SELFTEST: 10/10 pass` (doc-rev-ignored mutant on base bytes,
sha256 `2e4bb03c7d499c7a6a8e3737545dd0297ff209c35a675c4e19cfca312ac9605a`),
and the two pristine base selftest lines.

**After** (PLACEHOLDER — landing receipts are produced by the L1 at the
landing rev; the design-phase expected values, already measured on the
pre-data candidate `.ufo/waves/round-76/l1/bat-wr.out` whose target sha256 is
the candidate `ca05ec1544…`, are):
`tools/wave-reconcile.py` gains `arm19-seatreports-printed-required` (a
`seat_reports` row whose record carries no `printed` value refuses with
`record-printed-absent`; the wrapper also catches the TypeError the bypass
mutant raises, so the suite stays runnable under mutation);
`SELFTEST_ARMS` 18 → 19 → `WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0.
`tools/selfstate-freshness.py` gains `ARM11_doc_rev_cli_binding` (the real
CLI runs as a subprocess against a two-state git fixture; rev1 doc `4/4` vs
worktree doc `9/9`; reading `--doc-rev` must measure
`rows=1 match=1 stale=0 unexpected=0` exit 0); `SELFTEST_ARMS` 10 → 11 →
`SELFSTATE_SELFTEST: 11/11 pass` exit 0.
`tools/wave-reconcile-mutants.spec` gains the seventh defect
`adv-seatreports-require-printed-bypass` (the exact single edit; first six
blocks byte-identical to base).
The battery over the landed bytes prints `CONTROL: GREEN`,
`MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0
inconclusive=0 kill-rate=100%)` and `MUTATE_RESTORE: OK` byte-identical, with
the kill matrix: `m2-delimited-tautology` → arm13 + arm16 (r75 collateral,
unchanged); `span-rule-removed` → arm14 + arm17 + arm18 (unchanged);
`seat-reports-any-depth` → arm15; `mc-record-bound` → arm16;
`roles-bypass` → arm17; `attack-bypass` → arm18;
`adv-seatreports-require-printed-bypass` → **arm19 only**
(got=`printed-none-reached-comparison` — verbatim from
`.ufo/waves/round-76/l1/bat-wr.out`).
The five instrument mutants (rebuilt single edits on the landed bytes) each
die on their named arm: `echo-doc-token` → ARM2 (collateral ARM3 + ARM9,
disclosed); `expect-ignored` → ARM2; `capability-absent-deflected` → ARM4;
`zero-rows-success` → ARM6; `doc-rev-ignored` → ARM11 only.
Landed receipts: PLACEHOLDER (e.g.
`.ufo/evidence/round-76/c1-landed-battery.txt`,
`.ufo/evidence/round-76/c1-arms1-15-diff.txt`,
`.ufo/evidence/round-76/selfstate-landed-battery.txt` — L1 names the actual
paths).

### R76-C2 — calibration: the routed dated-literal cells re-derive from their instruments

**Before** (measured at base, receipt
`.ufo/waves/round-76/l1/c2-before-r76.txt`): with the extended 20-row
manifest `.ufo/waves/round-76/l1/selfstate-freshness-r76.json` and
`--doc-rev 451ed5cb`:
`SELFSTATE: rows=20 match=16 stale=4 unexpected=2` exit 1 — verbatim tail of
the receipt, with the two unexpected rows reading
`SELFSTATE_ROW r76-pin-disposition-selftest capability=six-leg content-disposition probe expect=match measured=stale UNEXPECTED doc_figure=18/18 measured_figure=19/19 instrument_exit=0`
and
`SELFSTATE_ROW r76-evidence-disposition-selftest capability=effective expectation reconciliation expect=match measured=stale UNEXPECTED doc_figure=34/34 measured_figure=66/66 instrument_exit=0`,
and the frozen span row reading
`SELFSTATE_ROW r76-r17-evidence-disposition expect=stale measured=stale ok span_figure=56/56 measured_figure=66/66 instrument_exit=0`.
(Token uniqueness pre-checked per the plan: pin-disposition stdout carries
exactly one `\d+/\d+` match `19/19`; evidence-disposition exactly one,
`66/66` — this seat re-verified both instruments' current tokens at base:
`pin-disposition.py --selftest` prints `SELFTEST: PASS (19/19)` and
`evidence-disposition.py --selftest` prints `SELFTEST: PASS (66/66)`.)

**After** (PLACEHOLDER — landing receipt produced at the landing rev;
expected): the two capability cells are superseded row-scoped — `six-leg
content-disposition probe` quotes `SELFTEST: PASS (19/19)` and `effective
expectation reconciliation` quotes `SELFTEST: PASS (66/66)`, the instruments'
own output format; a round-76 supersession line is appended directly after
the round-17 disclosure naming the current tokens with receipts (`107/107`
and `cases=10` as the two named bash gaps, `19/19`, `66/66`) and stating that
the round-17 values stand as dated history; and
`python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --doc-rev <landing-rev>`
reads `SELFSTATE: rows=20 match=18 stale=2 unexpected=0` exit 0, with the
frozen `r74-frozen-addr-six` row and `r76-r17-evidence-disposition` the two
stale-ok rows and every live row `match`. The landed manifest's three new
rows equal the plan's frozen tuple table byte-wise (the tuple freeze — the
table IS the counter).
Landed receipts: PLACEHOLDER (e.g.
`.ufo/evidence/round-76/c2-after-r76.txt` — L1 names the actual path).

## What was measured — controls and routed payments

- **Controls (pre-data).** Do-nothing: at base both survivors pass everything
  (receipts above), so both after-states are unreachable without the arms.
  The always-fail control: each new arm passes on the unmutated candidate and
  fails only under its mutant. The no-op guard: every spec edit is
  `count(old)==1` asserted by the runner (fail-closed), and the `@new`
  differs from `@old`. The design-phase battery on the candidate measures the
  full frozen matrix (`.ufo/waves/round-76/l1/bat-wr.out`):
  `MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0
  inconclusive=0 kill-rate=100%)` with `CONTROL: GREEN` and
  `MUTATE_RESTORE: OK (target-sha256 before=ca05ec15… after=ca05ec15…
  pristine-sha256=ca05ec15…)`.
- **receipt-exists scratch leak (routed payment, r75 wave finding).**
  Red-before measured this round: `.ufo/evidence/round-76/receipt-exists-leak-r76.txt`
  reads `selftest rc=0`, two leftover dirs
  (`receipt-exists-selftest-sv64ydyk`, `receipt-exists-selftest-sv64ydyk-extra`),
  `leftover_count=2`, `expected_green_after_fix: leftover_count=0`. The
  candidate fix cleans up in `finally` via `shutil.rmtree` (the S299 form);
  green-after receipt: PLACEHOLDER. The selftest stays `4/4 pass`.
- **Out-of-population record repair (disclosed).** After C1 lands, the
  `wave-record reconciliation` capability cell (`18/18`) is superseded to
  the new `19/19` token with the battery receipt — outside C2's frozen
  population (r75 precedent, Correction 2 item 2). PLACEHOLDER for the
  landed cell bytes.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `scratch-leak` | `tools/receipt-exists.py --selftest` leaves its scratch dirs behind: the red-before receipt `.ufo/evidence/round-76/receipt-exists-leak-r76.txt` measures a `TMPDIR` dir count of 0 → 2 during one `--selftest` (`leftover_count=2`, both dirs named `receipt-exists-selftest-*`). The instrument predates the S279 caller-deletion duty's enforcement sweep. | the S279 caller-deletion duty (the standing rule the instrument never enforced); measured red-before this round as a routed payment, not by a gate. | cleanup in `finally` via `shutil.rmtree` (the S299 form); green-after receipt must read `leftover_count=0` and the selftest stays `4/4 pass`. PLACEHOLDER for the green-after receipt path. |
| `attribution` | the design-phase C1 battery receipt `.ufo/waves/round-76/l1/bat-wr.out` certifies the L1's scratch candidate (`MUTATE_RESTORE` names target-sha256 `ca05ec1544…` = `.ufo/waves/round-76/l1/cand-wr-19.py`), not the tool bytes that will be landed; a receipt is evidence only for the revision it names. Same class as the round-75 lesson's `attribution` row. | the plan's own kill-rule design (the wave seats must re-derive on landed bytes; the L1's landing step re-runs the battery against the landed tool and spec). | re-run the battery against the **landed** tool and spec at the landing rev so the C1 after-state's receipt names the landed sha256; the candidate receipt stays cited only as the pre-data design measurement. PLACEHOLDER for the landed battery receipt path. |

## Findings routed to round 77

<!-- SKELETON — the wave's attack seats and the closure fill this. Known,
     already-named items the round carries (from the plan and pre-data
     receipts): -->

- The two named bash gaps stay routed until a runner widening: the round-17
  line's `95/95` (mutation-sweep selftest; current token `107/107`) and
  `cases=7` (current `cases=10`) are printed by bash instruments, and the
  selfstate runner spawns `python3 -I` scripts only — they cannot enter the
  population without widening the runner, which is not this round's claim.
  The round-17 values stand as dated history under the round-76 disclosure
  line.
- PLACEHOLDER (wave attack findings: any survivor found by the reviewer /
  critic / mutation-tester seats, with the surviving selftest line and the
  exact edit).
- PLACEHOLDER (closure-routed defects, mirroring the round-75 spotcheck §6
  shape).

## Routed-queue reconciliation (round-75 spotcheck §6 item 3)

The round-75 spotcheck's item 3 lists round-73 routed items 3–4 as open; the
round-75 report already corrected two of them in the correcting-round form,
and this round pays the remaining ones, so the queue stops double-listing:

- **Corrected by the round-75 report (recorded here, not re-paid):** the
  round-73 report's 22-of-23 landed-changes table (`e309f59f` missing) and
  its `19 × W04` census sentence (receipt reads 18) — both corrected in
  `.ufo/reports/round-75/tameshi.md` (the correcting-round form the r74
  spotcheck defect 6 names).
- **Paid this round:** the round-73 plan erratum (appended to
  `plans/round-73.plan.md` — the contradicted kill-rule sentence at its
  lines 80–82; draft in this wave's T76W1S1 seat dir) and the round-74 S294
  `used-by` old→new lesson append (appended to `corpus/lessons/round-74.md`,
  append-only; draft in this wave's T76W1S1 seat dir).

## Settlement errata

PLACEHOLDER (append-only; mirror the round-75 lesson's settlement errata
shape — anything the wave settles after the first write is disclosed here,
not relabelled pre-data).
