# tameshi round 69 — lesson (hyaku, 2026-11-02)

L1 `TameshiR69` (round 69). Base `434a96e47d0875dad21777cd68be2075925b068c`
(= origin/master; the commit that landed the r68 non-author closure).
Dispatch host: win32 (python 3.13.15 native `python`; git
2.55.0.windows.3; `core.autocrlf=false` in the lane repo). Receipts:
`.ufo/evidence/round-69/win-host/` — receipt-after-subject ordering (the
r61–r68 precedent): records land first, receipts follow in the same or the
next commit, and every commit message names only file tokens its tree
carries. The scratch is deleted with the round.

## Carry-in (r68 non-author closure — two status-neutral defects, both addressed)

1. **Capability-row counting command under-specified** (r68 spot-check
   routed defect 1): the printed command
   (`git show <rev>:SCORECARD.md | grep -c 'figure-attribution check'`,
   unanchored) reads 4 at the r68 tip — the claim, verdict and correction
   rows also carry the phrase — so it cannot measure the capability row's
   entry. The anchored form is the command of record and reads 0 at the
   r67 tip → 1 at the r68 tip (re-measured this round, both shapes:
   unanchored 4 at `859a736d` and 4 at `434a96e4`; anchored 0 at
   `859a736d`, 1 at `434a96e4`). Correction entry, never a rewrite: the
   LOG carries the erratum, the SCORECARD carries the appended correction
   paragraph, and every counting command this round prints is an anchored
   form. This is also why the r69 capability-row command below is cited
   anchored (`grep -cE '^\| anchor-drift sweep'`).
2. **S299 anchor naming drift** (r68 spot-check routed defect 2): the S299
   anchor cell locates the rmtree quote in the section named "Directory
   deletion operations"; the page's — snapshot and live agree — section
   heading is "Directory and files operations". Rows are append-only and
   the anchor is not an in-place-editable cell under contract v1, so the
   correction of record is threefold: this lesson; the round-69 SOURCES
   tail note (the next note touching S299); and — the standing form — the
   anchor-drift sweep's manifest carrying the drift as a measured red arm
   (the row s299-anchor-as-written: the cell's heading vs the row's own
   pinned r68 snapshot, expect=absent, measured=absent, ok) beside the
   true heading (s299-anchor-as-on-page, expect=present, measured=present,
   ok) on the same snapshot. The drift stays measured until a superseding
   row carries the corrected heading (CORPUS.md rule 2's correction
   mechanism).

## Fresh-start duty

The prompt's fresh-start block lists r58/r59/r60 (the last REJECTED
closures). They were re-read before anything was declared
(`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The premise is
stale — r61 through r68 were all admitted (r68: closure `434a96e4`,
admitted=true) — but the duty was performed and each standing ruling is
honored: r58's — positive controls must actually bind and a refused
deciding run is the honest outcome (this round's forecasts were measured
against the base bytes BEFORE the declaration: the rehearsal receipts
under `.ufo/evidence/round-69/win-host/rehearsal/` are the pre-data runs);
r59's — a counter must discriminate a cheat family (C1's red arm is the
r67 lesson's own named defect class — a receipt whose only carrier for a
quote is its own miss-record line — refused by construction and
red-arm-tested as selftest arm 5; the frozen bytes demonstrably accept
that carrier, which is the cheat side); r60's — a round's no-harm guard
must run ON this host at the revision pair it claims (the portable
precheck, worktree blob sha256 `892a045d…`, runs at every measured pair
below; RED + green + rev mode all on this host).

Ruled out this round, with reasons: (a) any freshness-score move — the
r45 counter stays a frozen Linux-host shape (the r68 pricing stands); C2
is an operability instrument, the freshness score is not touched and not
re-measured; (b) SKILL.md / QUALITY.md / README.md / PROVINCE.md content
edits — each extends the rekey payment beyond the one SOURCES edit the
sourced claim requires; (c) a new arm-liveness manifest row for the
exclusion — measured in rehearsal: NO standing quote loses or gains
backing under the exclusion (the totals are byte-identical at both
recorded tips), so no real-history tally-moving input exists to pin, and
manufacturing one would be synthetic (the r59 ruling); the manifest stays
at its 6 rows; (d) the deeper backing boundary — a cited sweep receipt's
non-miss-record lines (its QUOTE backed lines naming genuine raw
receipts) still carry spans transitively, so the backing relation remains
monotone in cited bytes; a full attestation-chain semantics is a checker
redesign with no routed demand; named successor work; (e) the
figure-attribution manifest's LOG-stale-figure successor row — kept in
reserve as the r68 lesson held it (no routed demand); (f) the arm-liveness
--only row filter — priced, not routed (r68 lesson); (g) adopting MORE
considerthese proposals — at most one per round; 2026-10-28 proposals 3–5
stay unadopted, none fits the round's routed work; (h) the root-level
`C:` tree oddity — live-lane tree surgery, priced out since r65, recorded
for the operator.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration, the lowest scored numeric axis at 8; the r67
  lesson mistake 4's named successor work — the self-referential-backing
  exclusion, executed).** `tools/quoted-line-exists.py` v2: the backing
  scans (the doc sweep and the explicit receipt/quote mode) remove each
  cited receipt's miss-record lines — the checker's own QUOTE MISSING
  output lines, which print the missing span bytes — before the substring
  test; a receipt that quotes a verdict line inside its own miss record
  is the record of a miss, not backing for the figure
  (corpus/lessons/round-67.md, mistake 4: "a receipt that quotes a
  MISSING line records a miss, it does not back the figure"). Selftest
  4/4 → 5/5 (arm 5 the selfref red: a record whose quote appears in the
  cited receipt ONLY inside a QUOTE MISSING line reads MISSING with exit
  1, while its genuinely-carried sibling quote stays backed — the
  exclusion is the thing under test). Before (measured at the base
  bytes, receipts `reh-qline-log-old.txt`, `reh-qline-sc-old.txt` and
  the r67-tip pair under `rehearsal/`): the frozen checker carries no
  exclusion (`git show 434a96e4:tools/quoted-line-exists.py | grep -c
  MISS_RECORD_LINE` → 0) and its first-backing-receipt attribution names
  a miss-record-only carrier for 35 of the r68-tip LOG's 114 backed
  quotes and 11 of its SCORECARD's 346 (the same counts at the r67 tip:
  35 of 109 and 11 of 338) — the false-carrier class standing unmeasured
  since r67. After (forecast = rehearsal; live receipts at the round
  receipts commit): selftest 5/5; the same four standing pairs re-swept
  at the exclusion bytes read totals byte-identical (missing 5 / 0 at
  both recorded tips; backed 114 / 346 and 109 / 338) with the 46 false
  carriers re-pointed to receipts whose bytes carry the quote outside a
  miss-record line (receipt `qline-carrier-r69.txt`); AND the r67
  erratum's mechanism narrative is corrected by measurement: no standing
  quote was ever solely miss-record-backed — the counts' r67 movement
  (LOG missing 40 → 5, SCORECARD 10 → 0) rode the cited base receipts'
  non-miss-record lines and later-landed receipts, so the exclusion
  changes no verdict, only the attribution of record. Standing tip
  sweeps at the r69 bytes forecast LOG missing=5 / SCORECARD missing=0 —
  the round's own appends introduce zero unbacked quotes (the r67
  decomposition invariant, now under the stricter scan).
- **C2 (operability, verdict-only; capability acquisition; sourced on
  new row S300, opened this round — Python html.parser documentation).**
  `tools/anchor-drift-sweep.py` + `tools/anchor-drift-sweep.json` (new;
  schema `tameshi-anchor-drift-v1`): a held row's anchor heading must
  still be the heading the row's own pinned snapshot carries — a manifest
  row pins (the snapshot path at a revision, the exact heading string the
  anchor cell names, expect present|absent), the snapshot blob is read
  from git objects at the pinned revision (never a worktree), its h1–h6
  texts are parsed through an html.parser.HTMLParser subclass (S300 is
  the parser contract: the instance calls handler methods on start tags,
  end tags, text, comments and other markup; convert_charrefs decodes
  entities), whitespace-normalized with the trailing paragraph mark
  dropped, and the row verifies only when the measured presence matches
  the expectation; an expect=absent row MEASURES the drift on every
  sweep, never assumes it; unresolvable snapshots are setup exit 2
  before any row effect; a zero-row manifest is refused exit 2. Standing
  manifest: four rows — the r68 routed defect as the measured red arm
  (S299's cell heading "Directory deletion operations" vs its own pinned
  r68 snapshot: expect absent), the true heading green ("Directory and
  files operations" vs the same snapshot: expect present), the page h1
  green ("shutil — High-level file operations"), and S300's own class
  heading green ("html.parser — Simple HTML and XHTML parser" vs its
  snapshot, pinned at the declaration revision). Before (measured at the
  base bytes): no instrument exists (`git ls-tree 434a96e4 tools/ | grep
  -c anchor-drift` → 0) — the drift was caught by the non-author closure
  reading the page, not by any standing check — and the drift itself is
  measurable pre-instrument: the cell's heading occurs 0 times in the
  pinned snapshot bytes while the page's heading occurs 3 times (grep -cF
  on `.ufo/evidence/round-68/win-host/sources/s299-shutil.html`).
  After (expected, forecast from the rehearsals): selftest
  ANCHOR_DRIFT_SELFTEST: 5/5 pass exit 0; the standing sweep
  ANCHOR_DRIFT: rows=4 met=4 unexpected=0 exit 0 with the red row
  reading expect=absent measured=absent ok; manifest id-grep → 4; S300
  anchored grep 0 → 1; registry rows 159 → 160; the capability row
  enters the table, cited by its anchored form.

Causally separable: C1 is one checker blob (tools/quoted-line-exists.py);
C2 is two new files + the SOURCES row; neither needs the other (the C1
sweeps read committed history only; the C2 sweep runs the new tool at its
new bytes against pinned snapshots).

## Shared no-harm story (declared forecast, then measured)

The SOURCES edit (one row + one tail note, the r67/r68 edit shape) is the
round's only monitored-file change: the live RED at the C2 SOURCES work
commit is forecast at lost=13 with cand_credited=51 — the SAME 13
headings as the r68 measured set and this round's rehearsal (decoded
comparison receipt `reh-red-decode-r69.txt`: equal in order, miss = 0),
paid by the `r69-batch-1` rekey (the r68 as-run machinery re-driven at
this round's constants; 13 fresh input-keyed entries; ledger 758 → 771)
restoring lost=0 ok exit 0 at BOTH floors (round `434a96e4` 64 → 64,
historic `8b0042bd` 46 → 64) plus rev mode 64/64, probe 20/20. Additivity
raw_old_only=0 on every landed pair (SOURCES mid-file row insertion +
tail note, verbatim_prefix=false disclosed; LOG/SCORECARD appends pure;
ledger mid-file insertion disclosed). PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe stay blob-identical base →
tip. The C1 checker file is in no cold-read section's input union
(verified against the r68 union plan's 7702 union paths before the
declaration — neither quoted-line-exists.py nor arm-liveness.json nor any
anchor-drift path appears), so the checker commit cannot stale any
section. Census exit 0 at both ends; registry rows 159 → 160 (S300).

## Gate

- Sourced row opened this round: **S300** (Python html.parser
  documentation, https://docs.python.org/3/library/html.parser.html,
  fetched 2026-11-02, HTTP last-modified Mon, 02 Nov 2026 13:31:34 GMT;
  55260 B; sha256
  `c72bed36ea96e5bc99ffa64f6d653c286efb08b35371293b25b16a259d109316`;
  extract `.ufo/evidence/round-69/win-host/sources/s300-htmlparser.html`,
  snapshot-pinned per the r41 docs-clock lesson). Located quote (the
  class-description paragraph under the page's single class heading; 24
  words): "An HTMLParser instance is fed HTML data and calls handler
  methods when start tags, end tags, text, comments, and other markup
  elements are encountered." Grounding: the sweep's heading extraction
  subclasses HTMLParser and overrides
  handle_starttag/handle_endtag/handle_data to collect h1–h6 text, with
  convert_charrefs decoding entities — the described handler contract is
  the mechanism the sweep runs on. The page and scope are previously
  unheld: `git show 434a96e4:corpus/SOURCES.md | grep -c html.parser` →
  0 at the base; no within-scope duplicate — S153/S154 hold the
  ast/pathlib pages, S278/S279 the tempfile source and docs page, S299
  the shutil page, all different documents.
- Rejections: NONE this round — the first candidate passed the held-page
  grep BEFORE the fetch was staged (the r68 mistake-3 discipline) and was
  adopted. Price-outs, with reasons: the Python re / difflib
  documentation — no claim rests on either (the exclusion is byte-line
  surgery over the checker's own recorded output shape; no new library
  surface), and staging a fetch to manufacture a row would be dishonest
  (the r66 S091 precedent, r67/r68 price-outs repeated). The standing
  rejections S293 (within-scope duplicate of S289) and S285 keep their
  census markers.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (receipt `census-start-r69.txt`; the
  pre-existing 17 W04 + 1 W01 set) and exit 0 at round end at both
  shapes (receipts `census-end-r69.txt` at the fleet root and
  `census-end-lanetip-r69.txt` at the lane-tip shape; the new S300 row
  census-clean, 160 rows).

## Mistakes (mined this round, all self-caught in the scratch before any
## live measurement depended on them)

1. **The r67 erratum's mechanism narrative was an unmeasured attribution
   (class: lesson-mechanism-unmeasured; captured-by: the rehearsal
   carrier diff — under the exclusion the totals are byte-identical at
   both recorded tips while exactly 46 first-backing-receipt attributions
   re-point).** The r67 lesson explained the tip-count movement (LOG
   missing 40 → 5, SCORECARD 10 → 0) as the previously-missing quotes
   becoming "byte-backed by the record of their own missingness" — the
   base-sweep receipts' QUOTE MISSING lines as the carrier. The round's
   measurement: no standing quote is solely miss-record-backed — under
   the exclusion every previously-backed quote STAYS backed (missing 5/0
   at the r67 tip and the r68 tip, totals byte-identical), and the
   miss-record lines were the first-sorted FALSE CARRIER for 46
   attributions: the frozen checker named a receipt that merely records
   the quote's absence as the backing carrier. The movement's actual
   carriers were the cited base receipts' non-miss-record lines (their
   QUOTE backed lines naming genuine raw receipts) and later-landed
   receipts. Fix: the exclusion lands as named (the false-carrier
   attribution is real and now refused and re-pointed), and the r67
   mechanism claim is corrected here — append-only; the r67 bytes stand.
   The mined practice: a lesson's causal narrative is a claim like any
   other; when a checker change touches the mechanism, the narrative is
   re-measured before successor work builds on it.
2. **A manifest row authored from memory of the page, not from its bytes
   (class: manifest-row-from-memory; captured-by: the first rehearsal
   standings reading the h1 row expect=present measured=absent
   MISMATCH).** The round's first standing-manifest draft pinned the
   shutil page h1 as "Miscellaneous operating system services" (a byline
   recalled from memory); the snapshot's actual h1 reads "shutil —
   High-level file operations". Fix: extract the snapshot's heading set
   first, author the rows from the extracted bytes, re-run — rows=3
   met=3 unexpected=0 (receipt `reh-anchor-standings.txt`; the extract
   receipt `reh-anchor-s300-extract.txt`). The mined practice: manifest
   expectations are read off the pinned bytes, never recalled — the
   pre-data forecast rule applied one level down.
3. **A receipt's stdout written through a cp1252 console mangled every
   em-dash (class: console-codec-in-stdout-receipt; captured-by: reading
   the first RED rehearsal receipt draft — the LOST heading lines read
   mojibake where the r68 receipt carries UTF-8 em-dashes).** Plain
   `python -I` ignores PYTHONUTF8, so the precheck's stdout took the
   console codec. Fix: every receipt-generating run takes
   `python -I -X utf8` (the figure-attribution r68 receipt shape) and
   the receipt was regenerated; the tool-written JSON receipt (UTF-8 by
   construction) was clean throughout, and the decoded comparison names
   both sides' codecs (`reh-red-decode-r69.txt`). The r68 mistake-1
   codec discipline extended: it applies to the console, not only to
   stored files.
4. **Selftest arm 5 called fixture helpers outside their defining scope
   (class: fixture-scope-vs-new-arm; captured-by: the selftest dying
   with NameError: blob is not defined — and, after the first fix, again
   with _env is not defined — before any arm fired).** The v1 selftest
   keeps the blob lambda and the env helper as locals of the fixture
   builder; the new arm referenced them from selftest's scope. Fix: the
   arm inlines its hash-object runs and its env dict (arm 4's inline
   style); the selftest then reads 5/5 (receipt `reh-qline-selftest.txt`).
   The r68 mistake-2 practice one level down: a new arm brings its own
   helpers to its own scope, and the selftest runs before any standing
   sweep.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this
  host; the r60 L0 question stands unanswered — an L1-only round,
  disclosed.
- The declaration commit lands first (this lesson, the SCORECARD
  corrections + planned block, the LOG declared entry, the S300 extract
  + fetch headers, the round-start census receipt, and the rehearsal
  receipts under `.ufo/evidence/round-69/win-host/rehearsal/` — every
  pre-data run this forecast rests on), verified by diff-tree before the
  next stage.
- The live run: C1's checker lands alone (the C1 work commit); C2's
  SOURCES row lands alone (the C2 SOURCES work commit — the RED is
  measured at this commit, forecast above); the anchor-drift tool +
  manifest follow (the C2 work commit; the manifest pins the S299
  snapshots at the base revision and the S300 snapshot at the declaration
  revision — pin the revision you verified against, never tip); the
  rekey run-book re-drives the r68 machinery at this round's constants
  (the constants-only diff receipted as `make-rebind-r69.diff`); the
  guards run on this host at every claimed pair; the receipts land per
  the receipt-after-subject ordering; every landing is verified with
  `git diff-tree -r --name-status` before the next stage, and the round
  ends with a self-sweep of the round range plus a carries-what-it-names
  check of the tip commit before push.
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); corpus/lessons appends are LF; SOURCES.md (LF) carries
  the row insertion and the tail note (pure 2-line insertion,
  old-lines-lost = 0). No other monitored file changes.

## Verdicts (receipts land in the commit(s) following the work commits;
## expected receipts, pinned here pre-data)

- C1: `QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass` exit 0 (receipt
  `qline-selftest-r69.txt`, the live run from the landed bytes; the
  frozen-bytes selftest stays 4/4 at its own revision, receipt
  `qline-selftest-r68.txt`); the four standing pairs re-swept at the
  exclusion bytes — totals byte-identical to the frozen receipts,
  carriers re-pointed (receipt `qline-carrier-r69.txt`, the live twin of
  the rehearsal `reh-qline-carrier-diff.txt`); the standing tip sweeps
  LOG missing=5 / SCORECARD missing=0 (`qline-tip-log-r69.txt`,
  `qline-tip-scorecard-r69.txt` — the same known 5 LOG escapes and zero
  SCORECARD escapes, now under the stricter scan); the capability-row
  sync note (selftest 4/4 → 5/5 at the r69 bytes; the r65 figures stand
  at the r65 bytes) appended, not edited in place.
- C2: `ANCHOR_DRIFT_SELFTEST: 5/5 pass` exit 0 (receipt
  `anchor-selftest-r69.txt`; rehearsed pre-data,
  `reh-anchor-selftest.txt`); the standing sweep
  ANCHOR_DRIFT: rows=4 met=4 unexpected=0 exit 0 with the red row
  expect=absent measured=absent ok (receipt `anchor-standings-r69.txt`;
  rehearsed, `reh-anchor-standings.txt`); manifest id-grep → 4; S300
  grep 0 → 1; registry rows 159 → 160; the capability row enters the
  table (anchored grep 0 → 1).
- Shared: the RED at the C2 SOURCES work commit reads lost=13 RED exit 1
  with cand_credited=51 and the 13 LOST heading lines equal in order to
  the r68 set (miss = 0; receipt `live-red-r69.out` with the JSON
  receipt `red-receipt-r69.json` and the decoded comparison
  `red-decode-r69.txt`), then the rebind summary line REBIND OK
  sections=13 entries_added=13 ledger_before=758 (receipt
  `rebind-stdout-r69.txt`; ledger 758 → 771; machinery constants-only
  diff `make-rebind-r69.diff`) → lost=0 ok exit 0 at BOTH floors at the
  rekey commit (receipts `live-green-r69.out`: round floor `434a96e4`
  64 → 64; `live-green-hist-r69.out`: historic `8b0042bd` 46 → 64) plus
  rev mode credited=64/64 probe 20/20 (receipt `live-revmode-r69.out`);
  additivity raw_old_only=0 on SOURCES (base → the C2 SOURCES work
  commit; verbatim_prefix=false disclosed — the mid-file row insertion +
  tail note; receipt `additivity-sources-r69.txt`), on the ledger (C2
  work commit → rekey commit; verbatim_prefix=false disclosed — the
  mid-file entries-array insertion; receipt `additivity-ledger-r69.txt`),
  and on the LOG/SCORECARD pairs at the tip receipts commit (receipt
  `additivity-logscorecard-r69.txt`); the tip guards at both floors +
  rev (`live-tip-guard-r69.out`, `live-tip-guard-hist-r69.out`,
  `live-tip-revmode-r69.out`), the tip invariant sweeps
  (`qline-tip-log-r69.txt`, `qline-tip-scorecard-r69.txt`,
  `qline-green-round-69.txt` — this lesson sweeps clean), the
  round-range self-sweep (`tip-self-sweep-r69.txt` — forecast findings
  zero exit 0), and the census end receipts (`census-end-r69.txt` at the
  fleet root, exit 0; `census-end-lanetip-r69.txt` at the lane-tip
  shape, 160 rows). No owned axis harmed: depth 10, freshness 9,
  calibration 8 unchanged (no depth or freshness surface touched —
  PROVINCE.md, SKILL.md, README.md, corpus/QUALITY.md,
  tools/registry.json, SHONEN.md, tools/mutate-and-run.sh and the
  guarded probe `tools/coldread-precheck-portable.py` (blob sha256
  `892a045d…`) blob-identical base → tip; the diff-tree check over those
  paths is empty and corpus/SOURCES.md is the only monitored file in the
  round's diffs, rekeyed).

## Next-round carry

- The backing boundary (this round's measured correction of the r67
  erratum): a cited sweep receipt's non-miss-record lines still carry
  spans transitively; a full attestation-chain semantics for the
  quoted-line checker is named successor work (no routed demand).
- The anchor-drift manifest's natural successor rows: every held row
  with a committed snapshot extract (S289, S294, S295, S296, S297, S298
  and the kaika/round-4x snapshot rows) enters as successor rounds verify
  each snapshot's headings; the S299 red arm stays until a superseding
  row carries the corrected heading.
- The rekey payment is current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it.
- The guarded probe digest `892a045d…` is unchanged; the probe-arms
  re-run obligation stays attached to any future probe edit.
- considerthese 2026-10-28 proposals 3–5 remain unadopted; proposal 1 is
  fully landed (r65 byte-backing half, r68 semantic half) and proposal 2
  is landed (r66).
- Pre-existing tree oddity, observed not absorbed: the root-level `C:`
  tree. Out of scope again; recorded for the operator.


5. **The rekey commit's message named two receipts one commit before they
   land (class: message-names-future-receipts; captured-by: the round's
   own self-sweep reading findings=2 exit 1 against the pinned findings=0
   forecast — receipt `tip-self-sweep-r69.txt`: commits=6 evidence=58
   named=26 carried=25).** The rekey commit `b59ca7fe`'s message names
   `red-decode-r69.txt` and `reh-red-decode-r69.txt` (the decoded RED
   comparisons), which land at the receipts commit — the
   carries-what-it-names rule (r66 lesson; the r66 correction attempt's
   own-range defect is the same class at 42 findings, left standing and
   flagged by the standing sweep). Fix: disclosed in the LOG and the
   SCORECARD at the tip receipts commit (the r67 tip-count erratum
   precedent — the forecast reported as measured, never re-scoped), the
   landed history stays, and the round-66 manifest pattern names the
   pair as successor manifest-row work. The mined practice: the
   carries-what-it-names rule applies at EACH commit — a receipt named
   in a commit message exists in that commit's tree, or the message does
   not name it; receipts land with or before the commit that names them,
   never after.
