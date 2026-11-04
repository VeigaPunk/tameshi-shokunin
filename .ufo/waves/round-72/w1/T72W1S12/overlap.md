# T72W1S12 — sibling-overlap scan (read-only)

Scope: the fleet lane tree, not `/home/vgpnk/Projects/*-shokunin` literally.
`ls -d /home/vgpnk/Projects/*-shokunin` resolves to three dirs
(`kimi-shokunin`, `audio-shokunin-publish`, `tameshi-shokunin`); the lane tree
is `/home/vgpnk/Projects/shokunin/*-shokunin` (21 lanes). `mado-shokunin` and
`tameshi-shokunin` skipped per seat spec. Nothing was written outside this
directory.

## Method / commands (exact, run from `/home/vgpnk/Projects/shokunin`)

1. Lane enumeration:
   `ls -d /home/vgpnk/Projects/shokunin/*-shokunin | wc -l` → `21`.
2. Pass A (scoped dirs only, as specified):
   for each sibling lane,
   `grep -rlEi 'rekey|cold-?read|cost forecast|rekey-cost' "$L/tools" "$L/corpus/knowledge" "$L/plans"`.
   Hits: `kaidoku-shokunin` (4 `tools/round-50/oracle/*.tsv` + 1 knowledge),
   `kotodama-shokunin` (2 knowledge), `souji-shokunin` (`tools/impl-44.sh`,
   `tools/souji-census.impl-44.sh`), `tabi-shokunin` (15 plans/`corpus/knowledge`),
   `tsukuroi-shokunin` (`tools/score-pacnew-arm-r35b.py`, false positive).
3. Pass B (whole lane, excluding `.git .jj .ufo .scratch census node_modules`):
   `grep -rEl 'cold-?read|coldread|rekey-cost|rekey_cost|cost[ -]forecast|anchor[ -]drift|pointer[ -]drift|line-pointer' "$L"`.
4. Matched-line sampling per hit file:
   `grep -rEn '...same alternation...' "$L" | cut -c1-190`.
5. Forecast-instrument sweep:
   `grep -rln --include='*.py' --include='*.sh' --include='*.mjs' --include='*.js' --include='*.plan.md' -i forecast "$L"`.
6. Literal phrase: `grep -rli 'cost forecast' *-shokunin` (excl tameshi) → `0`.
7. Ledger-reader check: `grep -rln 'round-21/coldread\|coldread/ledger' *-shokunin`
   → 0 files outside `tameshi-shokunin/`.
8. Ownership scan: `grep -nEi 'own[s]?:|owns |pointer|anchor|citation|drift' "$L/PROVINCE.md"`
   for all 21 lanes (tameshi/mado excluded).
9. Outside the fleet root: `grep -rliE 'rekey|cold-?read|cost forecast|rekey-cost' /home/vgpnk/Projects/kimi-shokunin /home/vgpnk/Projects/audio-shokunin-publish`
   → 2 files, both `audio-shokunin-publish` (published mirror of `audio-shokunin`).
10. Merge package: `find /home/vgpnk/Projects/shokuknow/merge/tameshi -type f | wc -l` → `88`;
    per-file `grep -ci 'forecast'`, `grep -ciE 'cold.?read'`, `grep -ci 'rekey'`.

## Per-lane table

“Same mechanism” compares against this lane's two instruments:
`tools/pointer-recheck.py` (manifest rows: record bytes @record_rev, cited
pointer token, target span @target_rev, needle → hit/miss) and
`tools/rekey-cost.py` (newest ledger entry's `inputs` map ∩ planned paths →
predicted lost sections).

| lane | hits (pass A ∪ B) | instrument? | same mechanism? |
|---|---|---|---|
| audio-shokunin | `LOG.md:1448,1451`; `reports/round-90/r90-reviewer.md:71` | no | different — “SIGSEGV cold-read” is a crash-disclosure reading, not a ledger/cost. |
| audio-shokunin-publish | `LOG.md`, `reports/round-90/r90-reviewer.md` | no | different — published lane tree carrying the same SIGSEGV cold-read disclosure. |
| chousa-shokunin | `SCORECARD.md:1323`; `corpus/knowledge/claim-support-states-r24.md:77`; `corpus/lessons/round-46.md:82`, `round-47.md:97` | own-census check (SCORECARD row; source not opened) | different class/object — “fenced-heading chain anchor” drift inside its own claim registry; no line-pointer recheck, no cost forecast. |
| game-dev-2d-shokunin | `reports/round-76/r76-reviewer.md:29,107`; `round-104/r104-scout.md:187` | no | different — review findings (“no anchor drift”; one inline-comment drift), no instrument. |
| game-dev-3d-shokunin | `reports/round-102/lesson-critic.md:389`; `round-103/note/verify.md:502`; `round-107/r107-cards-crit.md:380`; `r107-rev-cards.md:309` | no | different — per-round pointer/line-pointer audits by hand (374 line-pointers), no standing instrument. |
| kaidoku-shokunin | `tools/round-50/oracle/c6430/c6490/g7581/g7582.oracle.tsv` (`etc/boot.d/core/rekey`, `rekey.service`); `LOG.md:1076`; knowledge `2026-10-19-arc3…:32` | no | different — “rekey” is a filesystem path in a package oracle; LOG mention is pointer-drift debt. |
| kake-shokunin | `corpus/QUALITY.md:284`; `README.md:245`; `lessons/round-26.md:55`, `round-27.md:167` | no | different — “cold-reader” is a fresh-reader role report; “inbound line-pointer correction register” is a ledger, not an instrument. |
| kama-shokunin | `tools/citation-provenance.py`; 6 lesson files | yes (citation tokens) | different — requires `cite(<rev>,<path>,sha256)` tokens and hashes the blob at that rev; no line span, no needle, no cost. |
| kasegi-shokunin | `lessons/round-26-verifier-spotcheck.md:71`, `round-31.md:107`, `round-33.md:93`, `round-49.md:73` | no | different instrument-wise, **closest experience**: M31-3/M33-3 are “registry append shifted cited SOURCES.md anchors” — the exact rekey-cost mechanism, recorded but never priced. |
| kengaku-shokunin | `lessons/round-36-…:91`, `round-37.md:61`, `round-59.md:71`; `corpus/evidence/round12-ladder/predict_r12.py` | prediction bundle, not cost | different — preregistered benchmark forecast; anchor drift is carried prose debt. |
| kotoba-shokunin | `lessons/round-3.md:22`, `round-58/59-…`; `plans/round-59.md:18`, `round-60.md:17`; `verifiers/check_correction_sweep.py:71,227` | sweep for superseded claims | different — STALE-vs-DECLARED pattern sweep; the `SHONEN.md:6` pointer drift is carried, not instrumented. |
| kotodama-shokunin | `lessons/round-49.md:264`; `reports/round-24/audit-typed.md:24`; `round-33/calib/C01-item-01.md:190`; `round-34/…:113,236`; `round-48/cov/…:341`; `tools/gates/argot-derivation-gate.py:34` | no | different — “forecast” is an argot term; `VERIFIED-CITE-DRIFT` is a verdict label in reports. |
| kumitate-shokunin | `scripts/cite-check.mjs:2594` (docstring: re-resolves every path/line/symbol/pin in `SKILL.md` + `corpus/**/*.md`) | yes (citation re-resolver) | same *class*, different object: its own docs against live trees; no manifest of record bytes @record_rev, no needle-in-span verdict, no cost projection. |
| lore-shokunin | `lessons/round-103.md:116` (M13) | no | different instrument-wise; M13 “line-anchor drift from an in-ledger insertion” is the rekey-cost phenomenon recorded as a lesson only. |
| mori-shokunin | `tools/mori-anchor-check.py`; `corpus/lessons/round-62/70`; `corpus/README.md:791` | **yes — nearest sibling instrument** | different mechanism/object: caller-supplied `LABEL\|LINE\|WORDS\|TEXT` anchors verified against one pinned local copy (source-row quote anchors + word counts); “citation hygiene only”, explicit NOT-list (not fetcher/parser/verdict). Its docstring: “Round 72 (C3, operability + capability acquisition)”. |
| revenger-shokunin | `LOG.md:1202-1206`; `SCORECARD.md:1396,1412`; `SKILL.md:148` (M42); `corpus/SOURCES.md:489` | yes (`reports/round-86/orphan_sweep7.py`) | same class, different object: `used-by` pointer drift by per-source citation-site accounting; does not read record bytes or spans. |
| souji-shokunin | `tools/impl-44.sh:446-459` (`declare -A REKEY`), same in `souji-census.impl-44.sh`; census artefacts | no (keying) | different — re-keys baseline rows by the `repo` column before comparison; “rekey” = row identity, no cost. |
| tabi-shokunin | `SKILL.md:1056,1317,1441`; `LOG.md:132,144`; `corpus/knowledge/packet-readiness-r7.md`; 12 plans/lessons | no | different — “packet cold-read verdict” is an unexecuted fresh-reader test of an approval packet, `[unknown]` since its r5; no ledger, no cost. |
| tsukuroi-shokunin | `corpus/knowledge/adjacency-anchors-r19.{md,json}`; `lessons/round-18/19/40/41`; `LOG.md:1538`; `SCORECARD.md:2856`; `tools/check-memory-pressure.py:1005,1010` | gate (`tools/check-adjacency-anchors.py` per r19 text) | different — adjacency-anchor census across sibling `PROVINCE.md` files; the memory-pressure hits are mutant case names (`duplicate-line-pointer`). Its r19 §7 is a **boundary precedent**, see below. |

## Ownership conclusions

- **Cold-read cost accounting: no sibling claims it and none can.** Zero files
  outside `tameshi-shokunin/` name the round-21 ledger
  (`round-21/coldread|coldread/ledger` → 0). In sibling corpora “cold-read”
  means a fresh-reader role (kake, tabi), never a credit ledger. The literal
  “cost forecast” appears in 0 sibling files. The fleet root `SCORECARD.md`,
  `README.md`, `AGENTS.md`, `PROTOCOL.md`, `AXES.md` contain 0 `cold-read`
  mentions.
- **Line-pointer / anchor-drift instrumenting: scoped, never fleet-owned.**
  Each lane instruments its own docs: mori `mori-anchor-check.py` (quote
  anchors on a pinned copy), kama `citation-provenance.py` (rev-qualified
  token hashes), kumitate `cite-check.mjs` (citation re-resolution), revenger
  `orphan_sweep7.py` (`used-by` sites), chousa’s census chain-anchor gate.
  No lane names another lane’s pointers as its own class.
- **Boundary precedent, already fleet practice:** tsukuroi
  `corpus/knowledge/adjacency-anchors-r19.md` §7 — “These are pointer-drift
  reports … the owner decides whether and how to repoint. Tsukuroi edits no
  sibling file and prescribes no replacement text.” This matches tameshi
  `PROVINCE.md` “Out of province → report, never absorb.” Nothing to absorb.
- **Nearest concurrent adjacency:** mori’s round-72 C3 (`mori-anchor-check.py`)
  acquires a located-line anchor checker for its own S584 trail in the same
  round number. Same defect class, different object and mechanism; mori’s
  docstring itself scopes it (“citation hygiene only”, “not a SOURCES.md
  parser”). It is not this lane’s pointer-recheck and not a cold-read cost
  instrument.

## Merge package (/home/vgpnk/Projects/shokuknow/merge/tameshi/)

Readable: yes (88 files: `MERGE-REPORT.md`, `MERGE-REPORT.json`,
`SOURCES.append.md`, `amendments/corpus/knowledge/`, `knowledge/corpus/knowledge/`).
Cost-forecasting content: **none**. Match counts —
`MERGE-REPORT.md` forecast=0 coldread=0 rekey=0; `MERGE-REPORT.json` 0/0/0;
`SOURCES.append.md` 0/0/0. “Cost” survives only in staged knowledge titles
(`r8-predictive-test-selection-cost`, `r8-flaky-cost-baseline`,
`r7-llm-era-criteria-cost`, `llm-mutant-equivalence-cost`,
`delta-debugging-minimization-contract`) — test-selection pipeline cost, not
cold-read/rekey cost. The package (staged Oct 24, first id S153, 103 rows)
therefore neither competes with nor supplies a cost instrument.

## Decisive adjacent finding (intra-lane, not cross-lane)

While checking whether a *sibling* already owns cold-read cost accounting, the
same capability was found **in this lane’s own base tree**, which contradicts
`plans/round-72.plan.md` R72-C1 “Before”: “No instrument prices a planned
monitored-file edit against the cold-read ledger.” Evidence in the seat report
`.ufo/waves/round-72/w1/T72W1S12.md` §Defect; headline: at
`f20ba482c7441d4c75818e7cd8a3165fee7821a1`,
`tools/cold-read-forecast.py` (blob `3a3ad9ab…`, mode 100755, admitted as
`A:tools/cold-read-forecast.py` in
`.ufo/evidence/round-57/no-harm.sh:4,33`, and used as the planning-time pricer
in `SCORECARD.md:2924`) reproduces **all five single-path frozen arms and the
union arm exactly** (13/6/6/0/0/17, `sections_total=64`, rc 0, ~3.7 s per
run). No sibling overlap; the overlap is with the base tree.
