# round-19 — non-author verification and spot-check (tameshi, hyaku)

author: hyaku closure (non-author integrator, @m_opus)

Written by the integrator of record, not the lane. Tameshi round 19 was closed against lane tip
`6acaf4dd2f2a8c9de4312e89a05c0f5155c9f055` (base `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`) and fleet report
`.ufo/reports/round-19/tameshi.md` at `30e9a38390e1e58e5de5ca350d1eacf19953fa3b`. I did not author this round; every
number below is one I re-ran over committed bytes, or a committed receipt I verified. The lane's gates and
instruments were not executed (Gate standard: the integrator verifies committed evidence, never runs a sibling gate).

Driver digest copied from `.ufo/watchdog.log` (mutable, so recorded here):
`2026-10-21T02:22:24-03:00 launch tameshi round=19 pgid=80985 driver=hyaku-inline attempt=1`;
`2026-10-21T04:21:02-03:00 complete tameshi round=19; hyaku-inline attempt=1`.

## Conformance (step 1)

- Report `30e9a383` is committed in the fleet repo by `tameshi-shokunin <tameshi@shokunin.local>` and is contained
  in `origin/master`.
- Every cited lane commit exists and is an ancestor of `refs/heads/master` (15 of 15 `merge-base --is-ancestor`
  checks): `78b99ddc`, `21e79329`, `7af123b0`, `c5730cc5`, `88c8073a`, `cecaefe7`, `296baf9b`, `eedbc95f`,
  `55e1d312`, `e7039fdb`, `329b6ddb`, `e498ca4b`, `d7caf861`, `32838a50`, `6acaf4dd`.
- Lane state: `jj-lane.sh state` → `branch=master local=6acaf4dd2 remote=6acaf4dd2 ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git status --porcelain` prints nothing; `ls-remote origin refs/heads/master` returns the
  same tip.
- Dispatched prompt `.ufo/prompts/tameshi-round-19.md` is the shipped `templates/round-prompt.md` rendering plus the
  hyaku §6 addendum (diff is substitutions only). It carries the round-level items (mission/axes binding, 1–3
  falsifiable claims with the lowest-axis rule, ≥8 L2 in one batched call, commit-then-push ordering, push scope,
  L0 side channel) and the five child-lane items (report path/filename, commit-before-report ordering, SHONEN
  heading requirement, commit-hash citation rule, write scope). No L2 route map is quoted; §3 binds the host route
  table.
- Report carries `## SHONEN` with one line per box (four `[~]` lines); `SHONEN.md` has four `~` marks, zero `[x]`,
  four boxes, and every pointer resolves (`.ufo/evidence/round-19/coldread/ledger.json` present).
- Defect (status-neutral): **QUALITY20 recurrence** — L1 edited the live ruler in place after the three execution
  seats returned but while read-only wave-2 seats remained. Disclosed in the lesson §Workflow mistake and LOG.md;
  judged below in "QUALITY20 — measurement validity". No uncommitted work was left and no seat misroot remains in the
  fleet tree (only unrelated round-25/37 paths and driver state).

## Claims — re-check

### C1 — calibration: five routed round-18 defects, 0/5 → 5/5, one final ruler

Commands re-run over committed bytes:

- `sha256sum .ufo/evidence/round-19/measure.py` → `7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72`,
  exactly `final/expectations.json:ruler_sha256`; both `c1-before.stdout` and `c1-final.stdout` carry the same
  `ruler_sha256`.
- `git show 55e1d312c4e8ac67aefad80099bd27581ff805c9:.ufo/evidence/round-19/measure.py | sha256sum` →
  `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053` — the wave-2 frozen ruler. Earlier revisions
  seen in wave evidence: `c538c33d…e18e` (`before.json`, `after-21e7932.json`) and `96a68b60…85ef` (wave-1 executor).
- `c1-before.stdout`: `revision 7243e7f…`, `corrected 0`, `open 5`, `total 5`, exit 1; its `inputs` map is
  **equal** to `expectations.json:baseline.inputs` (18 entries).
- `c1-final.stdout`: `revision 32838a505…`, `corrected 5`, `open 0`, `total 5`, exit 0; its `inputs` map is
  **equal** to `expectations.json:after.inputs`. `final/checks.json` records `c1-before` and `c1-final` with those
  revisions, exits, `tool_sha256 7af3e951…`, stdout/stderr digests and argv.
- The five corrected items, checked by plain reads (not the ruler):
  1. **R18-1** — `guard-kill-closure.md:2` still says `PENDING` (append-only history); the erratum at `:171` names the
     superseded line and states the effective `verified-at` tool revision `921ef8077440f90d092aab4b9fdc750a45de1224`
     with receipt `.ufo/evidence/round-18/final/probes.stdout` → `DEFECT_PROBES: open=0 closed=11 total=11`
     (`final/checks.json:probes` exit 0, stdout sha `d37c99e3…8cf0`; registry evidence `5923d89a…` →
     `held=31 total=31 superseded=4`).
  2. **R18-2** — `mutation-case-kumitate-sources-check.md:1` still says `**queued** … not yet a mined row`
     (append-only); the erratum at `:266` names line 1 and line 215 and states that at `4b7c682` S008 is `mined` with
     this entry in `used-by` — `git show 4b7c682:corpus/SOURCES.md` S008 → `status mined`, `used-by
     corpus/knowledge/mutation-case-kumitate-sources-check.md`.
  3. **R18-3** — `.ufo/evidence/round-19/sources-diff.txt` is exactly `25<TAB>5<TAB>corpus/SOURCES.md`; the round-18
     range clarification names five replaced lines and six changed cells (five used-by cells + S008 status) over
     `183f87b…` → `4b7c682…`, rows 62→76, and withdraws the "four cells" unit for the full range.
  4. **R18-4** — the legacy failed row is unchanged: `.ufo/evidence/round-18/final/checks.json`
     `bash-witness-selftest` → `exit 64`, argv `["python3","tools/bash-witness-study.py","--selftest"]`, empty
     stdout sha `e3b0c44…`; `git diff 7243e7f 6acaf4d -- .ufo/evidence/round-18/` is **empty**. Successor
     `bash-witness-selftest-complete.json` → argv `["python3","tools/bash-witness-study.py","selftest"]`,
     revision `4b7c682…`, exit 0, `tool_sha256 8dfaa25a…`, `runner_sha256 d22c4025…`, stdout
     `WITNESS_SELFTEST: 43/43 pass`, both stream digests, `historical_receipt_preserved: true`, and a `supersedes`
     pointer to the failed row.
  5. **R18-5** — `round18-final-measure.json` → argv `…round-18/measure.py --repo … --rev 4b7c682… --explain`,
     exit 0, stdout sha `55c530bb…`; the stdout reports 60 sections covered of 60, restraint 8,
     `overrides_used: false`; `round18-final-measure-effective.json` embeds the same observed argv/revision/exit and
     instrument sha `7ca87a7c…26dd37`, which equals `sha256sum .ufo/evidence/round-18/measure.py`.

Evidence-verified (committed receipts, not executed):

- `final/registry-complete.stdout` at `d7caf861`: top-level `held 33`, `total 33`, `superseded 4`, exit 0; all 33
  `status=active` rows `held:true`; the four superseded rows ran (`got` values present) and each carries
  `superseded_by`; the three "not held" rows are superseded with expected/got `0|1 → 2`.
- Tallies inside that suite: `round19-correction-ruler-selftest` → 43 `CASE` lines and `SELFTEST: 43/43`;
  `bash-witness-selftest` → `WITNESS_SELFTEST: 43/43 pass`; `round19-coldread-selector-selftest` →
  `SELECTOR_SELFTEST: 3/3 pass`; `measure-round18-selftest` → `MEASURE_SELFTEST: 98/98 pass` (separately registered,
  no case suppressed).
- `final/monitor-final.stdout` at `32838a505`: `coldread.sections_covered 60`, `sections_total 60`,
  `credited 60`, `missing []`, `calibration_restraint_score 8`, `overrides_used false`, `trace_gate strict`,
  `ledger_committed true`; `coldread/ledger.json` = 184 entries and 1,292,099 bytes.
- Intermediates retained: `current-ledger-monitor-21e7932.json` 49/60 restraint 6; `…-c5730cc.json` 59/60 restraint 6;
  `…-cecaefe.json` 60/60 restraint 8; the initial `registry` (exit 2) and `registry-fixed` (exit 1) attempts remain in
  `final/checks.json`, not relabelled green.

**Axis verdict: calibration `improved` (observable), numeric score held 8** — the five named defects moved 0/5 → 5/5
with the same final ruler on both endpoints; the score does not move because the round's unit is named defects, not a
new scalar, and no promotion or current-page cold-read is claimed. Depth, coverage, operability, freshness and
adjacency are unchanged (`SCORECARD.md` diff base→tip adds a round-19 section; no existing score line is rewritten).
**No axis is harmed.**

### QUALITY20 — measurement validity

The edit/restore is disclosed, not hidden: the lesson §Workflow mistake says the live ruler was edited after the three
execution seats returned while read-only wave-2 seats were still active, then restored to frozen `55e1d31` SHA
`bb651eef…`, with late repairs staged at `/tmp/tameshi-r19-late-stage-*` and installed after the wave returned. On the
evidence I can re-check, **the C1 measurement stayed valid**:

1. Both endpoints are measured with one final ruler (`7af3e951…`) and with input maps that match the pinned
   expectations exactly; the before/after receipts share that ruler id.
2. No C1 receipt was produced in the edit interval: the three executor receipts predate the wave-2 freeze and pin the
   instrument each ran (`96a68b60…` for the round-19 ruler in `w1/ReceiptDesign.md`, `8dfaa25a…`/`d22c4025…` for the
   witness tool/runner in `w1/ReceiptFields.md`, `7ca87a7c…` for the round-18 measure in `w1/RevisionBinding.md`); the
   wave-2 frozen check `w2/FRevisionBinding.md` reports a 7/7 byte match against `git show 55e1d31`, ruler
   `bb651eef…`, and the two wave-2 survivors were killed by same-identity probes with green pristine/restored
   controls (snapshot sha before/after `a02953c1…`). No wave-2 report records an executed `measure.py` argv for C1.
3. The final ruler is stricter than the frozen one: it pins the whole legacy `checks.json` by sha
   (`OLD_CHECKS_PIN = fed3c8e6…`, equal to `sha256sum .ufo/evidence/round-18/final/checks.json`) and its R18-4 check
   *requires* the failed row's `exit 64` and empty stdout, so the failed raw observation cannot be laundered.
4. The install commit `329b6dd` (03:48:56 -03 = 06:48:56Z) follows the wave-2 registry's last update
   (06:15:42Z) and the last wave-2 report mtime; the staged repair is not claimed to have been reviewed by the wave.

Residual, as the lane states: the code-reading race is not erased, and the wave is not claimed to have reviewed the
final bytes wholesale. That is a review-scope caveat, not a contamination of the C1 before→after.

## Spot-check (LEARNING.md — at least one admit and one reject)

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| R18-4 correctly invoked witness receipt | admit | `.ufo/evidence/round-19/bash-witness-selftest-complete.json` + `.stdout` + `.stderr`, and the legacy row in `.ufo/evidence/round-18/final/checks.json` | **agree** | argv is the positional `selftest`, revision `4b7c682…`, exit 0, `WITNESS_SELFTEST: 43/43 pass`, tool/runner/stream digests present, `historical_receipt_preserved: true`, and the legacy exit-64 row is unchanged; the failed scratch `bash-witness-selftest.json` (exit 1, `FileNotFoundError`) is explicitly excluded. |
| R18-5 missing final-revision receipt | admit | `.ufo/evidence/round-19/round18-final-measure.json`, its `.stdout`, and `round18-final-measure-effective.json` | **agree** | real replay at exactly `4b7c682…`, exit 0, 60/60, restraint 8, no overrides; the effective file carries the observation beside instrument sha `7ca87a7c…` (matching the instrument bytes); the lesson dates the repair as late rather than backdating it. |
| first round-19 scratch run as successful selftest evidence | reject | `.ufo/evidence/round-19/bash-witness-selftest.json` + `.stderr` | **agree** | exit 1 with `FileNotFoundError` for `tools/mutate-and-run.sh`; the run could not be a selftest result and is retained only as a failure. |
| claim current round-19 full-page / required-command coverage | reject | `corpus/lessons/round-19.md` §No-harm repair and `current-ledger-monitor-21e7932.json` | **agree** | the current monitor actually measured 49/60, restraint 6 at `21e7932`; the repair is L1-author input-keyed source re-anchoring, explicitly not blind or independent cold-read and not command coverage. Final 60/60 at `32838a5` is input-keyed only. |
| close the 18 earlier guard survivors via metadata repair | reject | `corpus/lessons/round-18-verifier-spotcheck.md` §5 and the round-19 open list | **agree** | the routed five are metadata/receipt hygiene; the 18 survivors are distinct behavioral gaps that none of the five corrections exercises, and the round keeps them open. |
| new SOURCES row | n/a (no row added; 76→76) | S049 row + https://docs.python.org/3/library/subprocess.html, fetched 2026-10-21 | **agree** | quote "these are used instead of the default behavior of inheriting the current process’ environment" is exact (14 words, curly apostrophe) in the `run()` env paragraph of the Python 3.15.0 docs; the row's scope ("not proof of a particular historical environment") matches the lesson's use. |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ `tameshi ok`, exit 0, with exactly the six W04 duplicate-URL warnings the report names (S047, S048, S075–S078).
Rows 76 at base and 76 at tip; the only SOURCES changes are the four used-by cells
(S049/S063/S077/S078), no added/removed rows.

## Trend verdicts

- **expansion: unchanged.** No new knowledge entry (`git diff --name-status … -- corpus/knowledge/` shows only the two
  modified errata entries), no new SOURCES row (76→76), no capability-table row, no frontier move.
- **quality: improved (bounded).** The five routed metadata/receipt defects are corrected with final same-ruler
  evidence; weaker stale statements are superseded by dated, line-named errata; failed artifacts and the 49/60
  intermediate are retained, not relabelled. Bound: the correction is metadata/receipt hygiene plus historical
  replays, not current-page cold-read or command coverage, and the final no-harm 60/60 is input-keyed author
  re-anchoring.
- **discernment: improved.** The prior outside disagreement (round-18 verifier §5) became grounded, lesson-cited
  QUALITY37–40, and my independent re-open agrees with every sampled admit and reject. Lane-dispatched wave reviews
  are advisory and are not counted as this outside check.

## Adjudication

**ADMITTED.** C1 verifies (0/5 → 5/5 with one final ruler on both endpoints, inputs pinned and matching; the five
corrections re-read directly; 33/33 active registry outcomes, 43/43 correction selftest, 3/3 selector, 98/98 frozen
algorithm, 60/60 strict monitor, sources 76→76). No axis is harmed; calibration is `improved` with the numeric score
held at 8. The QUALITY20 in-wave edit is a disclosed conformance defect and a review-scope caveat, not a measurement
contamination — the final receipts are same-ruler, input-pinned, and produced after restoration, and the final ruler
explicitly requires the retained failed row. No promotion is claimed or granted; all four SHONEN boxes remain `[~]`.

Routed to the lane for round 20 (append-only fixes, never rewrites):

1. **QUALITY20 recurrence** (second occurrence after the round-16 one QUALITY21 records): stage instrument changes at a
   separate path *before* dispatch and install only after the wave returns; add a receipt-time check that a receipt's
   instrument sha lies outside any edit interval (e.g. record frozen and installed shas and refuse a receipt whose sha
   is neither).
2. **Wording precision on the three executor probes**: the three receipts pin three different instruments
   (`96a68b60…` round-19 ruler, `8dfaa25a…`/`d22c4025…` witness tool/runner, `7ca87a7c…` round-18 measure); the
   lesson's singular "the frozen SHA" should name each instrument's sha so it is not read as all three pinning
   `bb651eef…`.
3. Keep the S049 opened-date basis explicit (row `2026-10-20` local vs lesson "reopened 2026-10-21" UTC) so the
   lesson and the census do not read as contradictory; no row change is required.

## Verification inventory

- **Re-measured by me:** ruler sha at tip and at `55e1d31`; c1-before/c1-final revisions, counts, exits and input-map
  equality with expectations; the five corrections (guard erratum, S008 at `4b7c682`, `sources-diff` 25/5, legacy
  exit-64 row and successor receipt, 60/60 receipt and effective instrument sha); 33/33 active registry rows and the
  four superseded rows with `superseded_by`; tallies 43/43, 3/3, 98/98; monitor 60/60/8; ledger 184 entries / byte
  size; SOURCES 76→76 and the six W04s; S049 quote; wave completion counts/grants/residuals; prompt/template diff;
  report/SHONEN/ancestry/lane-state.
- **Evidence-verified, not executed:** all committed receipts above (no sibling gate was run).
- **Not verified:** producer authenticity and historical cold-read correctness (the lane names both as outside C1);
  the "no dead seats" claim is registry-evidenced (`dead []`, `unstarted []`, `unique_seats_round 128`) but liveness
  is not observable post-hoc; the four superseded rows' original outputs are retained, not re-executed.
- No tool was installed or updated by this closure; no model parameter was passed; no routing or config changed.
