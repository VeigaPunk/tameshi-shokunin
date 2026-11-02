# tameshi round 71 — lesson (hyaku, 2026-11-02)

L1 `TameshiR71` (round 71). Base `4ed9ce1c52e2952fb0ec06eb542f30b6df0f88f3`
(= origin/master; the commit that landed the r70 non-author closure, verdict
admitted). Dispatch host: win32 (python 3.13.15 native `python`; git
2.55.0.windows.3; `core.autocrlf=false` in the lane repo; GNU sed 4.9 on
PATH — load-bearing for C1's engine of record, probe receipt
`reh-sed-probe.txt`). Receipts: `.ufo/evidence/round-71/win-host/` —
receipt-after-subject ordering (the r61–r70 precedent): records land first,
receipts follow in the same or the next commit, and every commit message
names only file tokens its tree carries; the treecommit paths are
repo-relative (the r70 lesson mistakes 4–5) and every landing is verified
with `git diff-tree -r --name-status` before the next stage. The scratch is
deleted with the round.

## Carry-in (r70 non-author closure — admitted clean; three items, all addressed)

1. **The named successor, executed this round (C2):** the r70 spot-check
   §6.2 called a bind-erratum manifest row pinning the `22807192` +
   `6e6cf2f7` pair "a reasonable next-round carry" (the same pair the r70
   lesson mistakes 4–5 named). C2 lands exactly those two rows.
2. **SHONEN promotion-review note (operator-side):** all four boxes remain
   `[~]` lane assertions with pointers; no independent promotion verifier
   has written `[x]`; promotion review is an operator-triggered act.
   Nothing this round changes the boxes; disclosed again in the report.
3. **The L2-minimum prompt item (operator-side):** the r70 spot-check §6.1
   routed the prompt renderer's missing L2-minimum item to the operator.
   The surface still does not exist on this host; the r60 L0 question
   stands unanswered; an L0 line naming the routed item is appended this
   round (append-only, never blocking). L1-only round, disclosed.

## Fresh-start duty

The prompt's fresh-start block lists r58/r59/r60 (the last REJECTED
closures). They were re-read before anything was declared
(`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The premise is
stale — r61 through r70 were all admitted (r70: closure `4ed9ce1c`,
verdict admitted) — but the duty was performed and each standing ruling is
honored: r58's — positive controls must actually bind and a refused
deciding run is the honest outcome (this round's forecasts were measured
against the base bytes BEFORE the declaration: the rehearsal receipts under
`.ufo/evidence/round-71/win-host/rehearsal/` are the pre-data runs; no
control was re-rolled); r59's — a counter must discriminate a cheat family
on committed real inputs (C1's red arms are the lane's own routed
real-history records — the r48 closure's routed pointer defect and the
PROVINCE r16 append's measured-stale claim — not manufactured inputs, and
the pointer binding refuses the always-match cheat by construction: a row
whose token is not in the record bytes reads ERROR, not ok; the r70
count-recheck discipline one instrument over); r60's — a round's no-harm
guard must run ON this host at the revision pair it claims (the portable
precheck, worktree blob sha256 `892a045d…` unchanged, runs at every
measured pair below; RED + greens + rev all on this host).

Ruled out this round, with reasons: (a) any freshness-score move — the r45
counter stays operator-priced future work (the r68/r69/r70 pricing stands);
C1 and C2 are calibration/operability instruments, the freshness score is
not touched and not re-measured; (b) SKILL.md / QUALITY.md / README.md
content edits — each extends the rekey payment beyond the one SOURCES edit
the sourced claim requires; (c) the PROVINCE.md erratum append for the
`:85-91` pointer — a PROVINCE edit is a monitored edit and would extend the
rekey payment further; the stale cell stands append-only with the drift
standing as a measured red arm, and the correction of record is this
lesson (a successor round may carry the PROVINCE append as its routed
work); (d) the anchor-drift successor rows for the kaika/round-4x snapshot
extracts (S269/S270) — PDFs, and the sweep's heading extraction is
html.parser (S300), an HTML surface; a PDF heading parser is a different
mechanism, named successor work rather than a half-faked row (carried); (e)
the deeper backing boundary — a full attestation-chain semantics for the
quoted-line checker stays named successor work with no routed demand (the
r69/r70 carry stands); (f) the figure-attribution manifest's LOG-stale-
figure successor row — kept in reserve (no routed demand); (g) the
arm-liveness --only row filter — priced, not routed (r68 lesson); (h)
adopting MORE considerthese proposals — proposals 3–4 (2026-10-28) remain
unadopted; proposal 5 IS adopted this round as C1 (at most one per round);
(i) count-recheck successor rows — no routed numeric record defect exists
this round; (j) the root-level `C:` tree oddity — live-lane tree surgery,
priced out since r65, recorded for the operator.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration — the lowest scored numeric axis at 8; capability
  acquisition; sourced on new row S302, opened this round — the GNU sed
  manual; adopts considerthese 2026-10-28 proposal 5, the one assimilation
  this round).** `tools/pointer-recheck.py` + `tools/pointer-recheck.json`
  (new; schema `tameshi-pointer-recheck-v1`): a record's cited line
  pointer must still point at the content the record claims, at the
  revisions the record names — a manifest row pins (the record bytes at a
  revision, the exact cited pointer token as it occurs in the record, the
  target path at a revision, the 1-indexed inclusive line span, the
  needle — the content the record claims the span carries); the span
  engine of record is `git cat-file blob <rev>:<path> | sed -n
  'START,ENDp'` (S302: §4.4 Range Addresses — the inclusive address range;
  §4.3's numeric form grounds single-line spans), staged as argv lists
  with no shell (the r70 mistake-2 discipline), sed load-bearing (not
  spawnable = setup exit 2, could-not-evaluate, never a silent fallback);
  the span is read from git objects, never a worktree; a span past the
  last line prints nothing (measured on this host) and reads as a miss;
  needles match as UTF-8 bytes, mid-line needles are terminator-agnostic
  (selftest arm 5 measures the CRLF case); the pointer binding requires
  the token to occur in the record bytes, else the row is an ERROR (the
  always-match cheat refused by construction); expect=hit|miss rows so the
  standing red arm MEASURES the drift on every sweep; unresolvable records
  or targets are setup exit 2 before any row effect; a zero-row manifest
  is refused exit 2. Standing manifest: eight rows, all pinned at the base
  `4ed9ce1c` whose bytes were verified pre-declaration — the two r48 red
  arms (the routed line-pointer defect: the lesson's Supersede rows cite
  `corpus/SOURCES.md:140`/`:141` for S267/S268; those lines hold S265/S266,
  the rows sit at 142/143 — expect=miss, measured), the PROVINCE r16 red
  arm (`:85-91`; lines 85–91 carry the ledger header plus legs 1–4, leg 7
  `js-round-gate` sits at 94 — expect=miss, measured; the ten-leg ledger
  sits at 88–97), and five green arms beside them (the r48 erratum's two
  corrected pointers 142/143, the non-author spotcheck's `142-143`, the
  verdict-table's `SCORECARD.md:13-14` and `LOG.md:68`). Selftest 7/7
  hermetic (hit-met, miss-met, mismatch-caught, pointer-absent, crlf-span,
  unresolvable, vacuous-usage). Before (measured at the base bytes): no
  instrument exists (`git ls-tree 4ed9ce1c tools/ | grep -c
  pointer-recheck` → 0) and the drift is measurable pre-instrument: the
  85–91 span holds no `js-round-gate` line (grep → 0) while line 94 does,
  and line 140 holds no `| S267 |` (grep → 0) while 142 does (receipt
  `base-measure-r71.txt`). After (forecast = rehearsal; live receipts at
  the round receipts commit): selftest `POINTER_RECHECK_SELFTEST: 7/7
  pass` exit 0 (rehearsed pre-data, `reh-pointer-selftest.txt`; live
  receipt `pointer-selftest-r71.txt`); the standing sweep `POINTER_RECHECK:
  rows=8 met=8 unexpected=0` exit 0 with all three red arms reading
  expect=miss measured=miss ok (rehearsed, `reh-pointer-standings-r71.txt`;
  live receipt `pointer-standings-r71.txt`); manifest id-grep → 8; S302
  anchored grep 0 → 1; registry rows 161 → 162; the capability row enters
  the table, cited by its anchored form.
- **C2 (operability, verdict-only): the standing arm-liveness manifest
  grows with its named successor rows, checker blob unchanged.**
  `tools/arm-liveness.json` grows 7 → 9 rows: `bind-r70-receipts-red` —
  the r70 lesson mistake 4's named successor and the r70 spot-check §6.2's
  suggested carry — pins the bind checker at `5541abaf` (the blob is
  byte-identical at the base, `git rev-parse` both = `c3e6a88e…`, verified
  before the rows were authored) over the r70 range `0c2573d7..22807192`,
  tally findings expect ≥19 exit 1: the receipts commit names 19 receipt
  files its tree does not carry; and `bind-r70-repair1-red` — the r70
  lesson mistake 5's named successor (the recurrence) — over
  `0c2573d7..6e6cf2f7`, tally findings expect ≥39 exit 1. Before: no r70
  rows exist (`grep -c bind-r70 tools/arm-liveness.json` → 0 at the base)
  and both sweeps read their disclosed figures (re-measured this round,
  `reh-bind-r70-receipts-range.txt` findings=19 exit 1 and
  `reh-bind-r70-repair1-range.txt` findings=39 exit 1 — the same numbers
  the r70 errata disclose). After: `ARM_LIVENESS: rows=9 live=9 dead=0`
  exit 0 with `ARM_LIVE bind-r70-receipts-red tally=findings=19 exit=1`
  and `ARM_LIVE bind-r70-repair1-red tally=findings=39 exit=1` (rehearsed,
  `reh-arm-live-standings-r71.txt`; live receipt
  `arm-live-standings-r71.txt`); the checker selftest unchanged 5/5; the
  arm-liveness capability row synced append-only (its r70-era figures
  stand at the r70 bytes; old → new in this lesson).

Causally separable: C1 is two new files + the SOURCES row; C2 is
manifest-data edits to one existing manifest; neither needs the other (the
C2 sweep runs manifest rows only; the C1 sweep runs the new tool at its
new bytes against committed records).

## Shared no-harm story (declared forecast, then measured)

The SOURCES edit (one row + one tail note, the r67–r70 edit shape) is the
round's only monitored-file change: the live RED at the C1 SOURCES work
commit is forecast at lost=13 with cand_credited=51 — the SAME 13 headings
as the r68, r69 AND r70 measured sets and this round's rehearsal (decoded
comparison receipt `reh-red-decode-r71.txt`: equal in order to both
reference sets, miss = 0), paid by the `r71-batch-1` rekey (the committed
r67 as-run machinery re-driven at this round's constants; 7 constants-only
changed pairs, every changed line constants-only: docstring round, trace
path, round/batch/carried_from/rekey_batch fields, and the stale round-64
reader string fixed to round 71 — the diff receipted as
`make-rebind-r71.diff`; 13 fresh input-keyed entries; ledger 784 → 797)
restoring lost=0 ok exit 0 at BOTH floors (round `4ed9ce1c` 64 → 64,
historic `8b0042bd` 46 → 64) plus rev mode 64/64, probe 20/20. Additivity
raw_old_only=0 on every landed pair (SOURCES mid-file row insertion + tail
note, verbatim_prefix=false disclosed; LOG/SCORECARD appends pure; the
capability-row insertion disclosed). PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe
`tools/coldread-precheck-portable.py` (blob sha256 `892a045d…`) stay
blob-identical base → tip; corpus/SOURCES.md is the only monitored file in
the round's diffs, rekeyed. The round's new tool files and manifest edits
are in no cold-read section's input union (verified against the r70 union
plan's 7702 unique union paths before the declaration —
tools/pointer-recheck.py, tools/pointer-recheck.json and
tools/arm-liveness.json all absent; SOURCES.md present, rekeyed; the r70
plan's 13 heading+sha256+span verified equal to the r69 plan's, so the r71
plan carries the same 13 sections — receipt `reh-union-check-r71.txt`).
Census exit 0 at both ends; registry rows 161 → 162 (S302).

## Gate

- Sourced row opened this round: **S302** (GNU sed manual,
  https://www.gnu.org/software/sed/manual/sed.html, fetched 2026-11-02,
  HTTP date Mon, 02 Nov 2026 21:01:17 GMT; no Last-Modified header served;
  Content-Length 415310; sha256
  `511edd60a6f5034d4f28ca1dbe0772bbfd4c9865aaf6c0f85e2f05d4294b6bac`;
  extract `.ufo/evidence/round-71/win-host/sources/s302-sed.html`,
  snapshot-pinned per the r41 docs-clock lesson). Located quote (the §4.4
  Range Addresses first paragraph; 20 words; fetched page lines 2445–2448):
  "An address range matches lines starting from where the first address
  matches, and continues until the second address matches (inclusively)".
  Grounding: the pointer-recheck rows re-extract a record's cited span
  with `sed -n 'START,ENDp'` over the pinned blob — the page's §4.4 range
  contract (inclusive, first-line = line 1) is the definition of what the
  span carries; §4.3's numeric-address form ("Specifying a line number
  will match only that line in the input", page line 2255) grounds the
  single-line spans the red arms pin. The page and scope are previously
  unheld: `git show 4ed9ce1c:corpus/SOURCES.md | grep -c
  'gnu.org/software/sed'` → 0 at the base; the held-page grep ran BEFORE
  the fetch was staged (the r68 mistake-3 discipline); no within-scope
  duplicate — S273 holds the Bash manual (tiswww.case.edu author copy +
  gnu.org bash node page, a different manual), S004 mutants.rs, S289/S293
  git-cat-file, S301 git-grep, all different pages.
- Rejections: none staged. The design decision the row does NOT record —
  the span engine was first sketched as python-native line slicing, which
  would have needed no new source — is recorded here instead: making sed
  the ACTUAL engine (not a prose analogy) is what moved the grounding to
  the sed manual; staging a fetch to manufacture a row would be dishonest
  (the r66 S091 precedent). The standing rejections S293 and S288 keep
  their census markers.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (receipt `census-start-r71.txt`; the
  pre-existing 17 W04 + 1 W01 set) and exit 0 at round end at both shapes
  (receipts `census-end-r71.txt` at the fleet root and
  `census-end-lanetip-r71.txt` at the lane-tip shape; the fleet-root
  `tameshi-shokunin` path is a symlink to this lane repo on this host,
  disclosed — both receipts carry the same validated state, 162 rows, S302
  census-clean).

## Mistakes (mined this round, both self-caught in the scratch before any
## live measurement depended on them)

1. **The selftest fixture's red arm cited a pointer its record bytes did
   not carry (class: fixture-pointer-not-in-record; captured-by: the first
   pointer-recheck selftest run reading 6/7 — arm 5 ERROR
   pointer-absent-in-record, before any standing sweep).** The toy record
   carried only the data.md pointers, so the CRLF arm's row pinned a
   `win.md:2-2` token that occurs nowhere in the record — the checker's
   pointer binding refused it, correctly. Fix: the fixture record carries
   the win.md pointer too (the arm verifies the CRLF span semantics through
   a token the record actually cites); the selftest then reads 7/7
   (receipt `reh-pointer-selftest.txt`). The r70 mistake-1 practice
   recurring one instrument over, caught the same way: a selftest
   fixture's red arms need their defect to EXIST in the fixture bytes —
   fixture expectations are read off the fixture bytes, never assumed.
2. **A rehearsal receipt ran through the host console encoding (class:
   console-codec-masking-receipt; captured-by: reading the first RED
   rehearsal receipt draft — its LOST heading lines carried the em-dash
   mangled through the cp1252 console, not UTF-8).** The first
   `reh-red-r71.out` run invoked the precheck without `-X utf8`, so the
   redirected stdout was encoded through the host console codepage (the
   r70 lesson's mistake-2 surface, one receipt over). Fix: re-run with
   `-I -X utf8` before any decode depended on it; the receipt reads UTF-8
   (the decode receipt names the encoding per file, the r69/r70 codec
   discipline); the mangled first draft was discarded in the scratch, it
   never entered a receipt or a claim.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question stands unanswered — an L1-only round, disclosed; an
  L0 line naming the r70 spot-check's routed prompt-fidelity item is
  appended to `.ufo/l0-questions.md` this round (append-only, never
  blocking).
- The declaration commit lands first (this lesson, the SCORECARD planned
  block, the LOG declared entry, the S302 extract + fetch headers, the
  round-start census receipt, and the rehearsal receipts under
  `.ufo/evidence/round-71/win-host/rehearsal/` — every pre-data run this
  forecast rests on), verified by diff-tree before the next stage.
- The live run: C1's SOURCES row lands alone (the C1 SOURCES work commit —
  the RED is measured at this commit, forecast above); the pointer-recheck
  tool + manifest follow (the C1 tool work commit); the arm-liveness
  successor-row edit lands (the C2 work commit); the rekey run-book
  re-drives the committed r67 machinery at this round's constants (the
  constants-only diff receipted as `make-rebind-r71.diff`); the guards run
  on this host at every claimed pair; the receipts land per the
  receipt-after-subject ordering; every landing is verified with
  `git diff-tree -r --name-status` before the next stage, and the round
  ends with a self-sweep of the round range plus a carries-what-it-names
  check of the tip commit before push.
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); corpus/lessons appends are LF; SOURCES.md (LF) carries
  the row insertion and the tail note; the JSON manifests stay LF. No
  other monitored file changes.

## Verdicts (receipts land in the commit(s) following the work commits;
## expected receipts, pinned here pre-data)

- C1: `POINTER_RECHECK_SELFTEST: 7/7 pass` exit 0 (receipt
  `pointer-selftest-r71.txt`, the live run from the landed bytes); the
  standing sweep `POINTER_RECHECK: rows=8 met=8 unexpected=0` exit 0 with
  the three red arms reading expect=miss measured=miss ok (receipt
  `pointer-standings-r71.txt`); manifest id-grep → 8; S302 grep 0 → 1;
  registry rows 161 → 162; the capability row enters the table (anchored
  grep 0 → 1).
- C2: `ARM_LIVENESS: rows=9 live=9 dead=0` exit 0 with `ARM_LIVE
  bind-r70-receipts-red tally=findings=19 exit=1` and `ARM_LIVE
  bind-r70-repair1-red tally=findings=39 exit=1` (receipt
  `arm-live-standings-r71.txt`; the checker selftest unchanged 5/5,
  receipt `arm-liveness-selftest-r71.txt`); manifest id-grep → 9; the
  arm-liveness capability row synced append-only (the r67-correction-4
  precedent; the r70-era figures stand at the r70 bytes; old → new in
  this lesson).
- Shared: the RED at the C1 SOURCES work commit reads lost=13 RED exit 1
  with cand_credited=51 and the 13 LOST heading lines equal in order to
  the r68, r69 AND r70 sets and this round's rehearsal (miss = 0; receipt
  `live-red-r71.out` with the JSON receipt `red-receipt-r71.json` and the
  decoded comparison `red-decode-r71.txt`), then the rebind summary line
  REBIND OK sections=13 entries_added=13 ledger_before=784 (receipt
  `rebind-stdout-r71.txt`; ledger 784 → 797; machinery constants-only
  diff `make-rebind-r71.diff`, 7 changed pairs) → lost=0 ok exit 0 at
  BOTH floors at the rekey commit (receipts `live-green-r71.out`: round
  floor `4ed9ce1c` 64 → 64; `live-green-hist-r71.out`: historic
  `8b0042bd` 46 → 64) plus rev mode credited=64/64 probe 20/20 (receipt
  `live-revmode-r71.out`); additivity raw_old_only=0 on SOURCES (base →
  the C1 SOURCES work commit; verbatim_prefix=false disclosed — the
  mid-file row insertion + tail note; receipt
  `additivity-sources-r71.txt`), on the ledger (C1 SOURCES work commit →
  rekey commit; verbatim_prefix=false disclosed — the mid-file
  entries-array insertion; receipt `additivity-ledger-r71.txt`), and on
  the LOG/SCORECARD pairs at the receipts commit (receipt
  `additivity-logscorecard-r71.txt`); the tip guards at both floors + rev
  (`live-tip-guard-r71.out`, `live-tip-guard-hist-r71.out`,
  `live-tip-revmode-r71.out`), the tip invariant sweeps
  (`qline-tip-log-r71.txt`, `qline-tip-scorecard-r71.txt`,
  `qline-green-round-71.txt` — this lesson sweeps clean), the round-range
  self-sweep (`tip-self-sweep-r71.txt` — forecast findings zero exit 0),
  and the census end receipts (`census-end-r71.txt` at the fleet root,
  exit 0; `census-end-lanetip-r71.txt` at the lane-tip shape, 162 rows).
  No owned axis harmed: depth 10, freshness 9, calibration 8 unchanged
  (no depth or freshness surface touched — PROVINCE.md, SKILL.md,
  README.md, corpus/QUALITY.md, tools/registry.json, SHONEN.md,
  tools/mutate-and-run.sh and the guarded probe
  `tools/coldread-precheck-portable.py` (blob sha256 `892a045d…`)
  blob-identical base → tip; the diff-tree check over those paths is
  empty and corpus/SOURCES.md is the only monitored file in the round's
  diffs, rekeyed; the round's tool files and manifest edits are in no
  section's input union — verified against the r70 union plan's 7702
  unique union paths pre-declaration, receipt `reh-union-check-r71.txt`).

## Next-round carry

- pointer-recheck successor rows: any future routed stale-pointer defect
  with an in-lane record enters as its round routes it; the PROVINCE
  `:85-91` correction — a PROVINCE.md append is a monitored edit that
  re-owes the rekey payment, so it is named successor work for a round
  that prices it (the stale cell stands measured by the red arm until
  then); the drift discovery sweep (the pointer scan that found the
  PROVINCE instance) is repeatable from the manifest's row vocabulary.
- count-recheck successor rows: as routed only (none this round).
- anchor-drift successor rows for the kaika/round-4x snapshot extracts
  (S269/S270): PDFs; the sweep's heading extraction is html.parser (S300),
  an HTML surface; a PDF heading parser is a different mechanism — named
  successor work (carried).
- The backing boundary (the r69/r70 carry) stands: a full
  attestation-chain semantics for the quoted-line checker is named
  successor work (no routed demand).
- The rekey payment is current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it.
- The guarded probe digest `892a045d…` is unchanged; the probe-arms
  re-run obligation stays attached to any future probe edit.
- considerthese 2026-10-28 proposals 3–4 remain unadopted; proposal 5 is
  adopted this round (C1); proposals 1–2 landed r64/r66, r65/r68.
- Pre-existing tree oddity, observed not absorbed: the root-level `C:`
  tree. Out of scope again; recorded for the operator.
