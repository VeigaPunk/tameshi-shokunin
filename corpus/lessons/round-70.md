# tameshi round 70 — lesson (hyaku, 2026-11-02)

L1 `TameshiR70` (round 70). Base `0c2573d7a316c297b5811aba5905919401edbc02`
(= origin/master; the commit that landed the r69 non-author closure).
Dispatch host: win32 (python 3.13.15 native `python`; git
2.55.0.windows.3; `core.autocrlf=false` in the lane repo). Receipts:
`.ufo/evidence/round-70/win-host/` — receipt-after-subject ordering (the
r61–r69 precedent): records land first, receipts follow in the same or the
next commit, and every commit message names only file tokens its tree
carries. The scratch is deleted with the round.

## Carry-in (r69 non-author closure — three status-neutral record defects, all addressed)

1. **Number drift in the r68-defect-1 correction narrative** (r69
   spot-check routed defect 1): the SCORECARD r68-corrections paragraph and
   the round-69 lesson both print the unanchored command as reading "4 at
   both the r67 tip and the r68 tip"; measured at this round's declaration,
   the unanchored count is 4 at the r68-tip candidates (`434a96e4`,
   `ec6852f3`, `e39f9ba0`) but 0 at BOTH r67-tip candidates (`859a736d` —
   the hash the paragraph cites — and `94b0fd7b`), and 5 at the r70 base
   `0c2573d7` (the r69 appends added an occurrence); the operative anchored
   measurement in the same sentence (0 at `859a736d` → 1 at `434a96e4`)
   verifies exactly. Correction of record: this lesson; the SCORECARD
   corrections paragraph (appended); the LOG erratum (appended); and the
   receipt that re-runs every printed command at the revision it names
   (`.ufo/evidence/round-70/win-host/carryin-correct-r70.txt` — the
   specific re-run output the r69 report cited by directory only, the
   closure's related pointer vagueness, fixed). The stale figures stand as
   the count-recheck instrument's measured red arms (rows
   `scorecard-r68corr-unanchored-r67tip` and `lesson-r69-unanchored-r67tip`,
   both reading drift ok on every sweep).
2. **Count nit: "20 receipt files"** at the R1 receipts commit — 19 files
   were ADDED at `89869bea` under `.ufo/evidence/round-69/win-host/`
   (diff-tree --diff-filter=A). Corrected here, in the corrections
   paragraph, and in the same receipt (command + output + exit).
3. **Count nit: "19 rehearsal receipts"** — 18 files exist under
   `rehearsal/` at `5eb09e84` and at the base. Corrected in the same places.

## Fresh-start duty

The prompt's fresh-start block lists r58/r59/r60 (the last REJECTED
closures). They were re-read before anything was declared
(`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The premise is
stale — r61 through r69 were all admitted (r69: closure `0c2573d7`,
admitted=true) — but the duty was performed and each standing ruling is
honored: r58's — positive controls must actually bind and a refused
deciding run is the honest outcome (this round's forecasts were measured
against the base bytes BEFORE the declaration: the rehearsal receipts under
`.ufo/evidence/round-70/win-host/rehearsal/` are the pre-data runs; no
control was re-rolled); r59's — a counter must discriminate a cheat family
on committed real inputs (C1's red arms are the lane's own routed
real-history records — the closure-caught drift figures — not manufactured
inputs, and the instrument refuses the always-match cheat by construction:
a row whose span or printed token is not in the record bytes reads ERROR,
not ok); r60's — a round's no-harm guard must run ON this host at the
revision pair it claims (the portable precheck, worktree blob sha256
`892a045d…`, runs at every measured pair below; RED + greens + rev all on
this host), and r60's routed D3 — "pin one decomposition to the counting
command" — is exactly the class C1 standing-measures.

Ruled out this round, with reasons: (a) any freshness-score move — the
r45 counter stays operator-priced future work (the r68/r69 pricing stands);
C1 and C2 are calibration/operability instruments, the freshness score is
not touched and not re-measured; (b) SKILL.md / QUALITY.md / README.md /
PROVINCE.md content edits — each extends the rekey payment beyond the one
SOURCES edit the sourced claim requires; (c) the deeper backing boundary —
a full attestation-chain semantics for the quoted-line checker stays named
successor work with no routed demand (the r69 carry stands); (d) the
figure-attribution manifest's LOG-stale-figure successor row — kept in
reserve as the r68 lesson held it (no routed demand); (e) anchor-drift
successor rows for the kaika/round-4x snapshot extracts (S269/S270) — the
waves extracts exist in-tree but the papers are PDFs and the sweep's
heading extraction is html.parser (S300), an HTML surface; a PDF heading
parser is a different mechanism, named successor work rather than a
half-faked row; (f) the arm-liveness --only row filter — priced, not routed
(r68 lesson); (g) adopting MORE considerthese proposals — proposals 3–5
(2026-10-28) remain unadopted, none fits the round's routed work; the
count-recheck instrument is the closure-routed printed-count class, not a
listed proposal; (h) the root-level `C:` tree oddity — live-lane tree
surgery, priced out since r65, recorded for the operator.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration — the lowest scored numeric axis at 8; capability
  acquisition; sourced on new row S301, opened this round — Git git-grep
  documentation).** `tools/count-recheck.py` + `tools/count-recheck.json`
  (new; schema `tameshi-count-recheck-v1`): a record's printed counting
  figure must still be the count its named command produces at the revision
  the record names — a manifest row pins (the record bytes at a revision,
  the exact record span that carries the figure, the printed integer, the
  counting command of record `git grep -c [-E] <pattern> <rev> -- <path>`,
  S301's --count contract), the row verifies only when the measured count
  matches the expectation, and an expect=drift row MEASURES the drift on
  every sweep, never assumes it; the span binding requires the pinned span
  to be a byte substring of the record and the printed integer to occur in
  the span as a delimited token; zero matches print nothing and exit 1,
  which the checker reads as the count 0 (measured on this host,
  disclosed — the page carries no exit-status section); unresolvable
  records are setup exit 2 before any row effect; a zero-row manifest is
  refused exit 2. Standing manifest: seven rows — the two routed-defect red
  arms (the SCORECARD r68-corrections paragraph's and the r69 lesson's
  "reads 4 at both tips" figures: printed 4, recount 0 at `859a736d`,
  expect drift) and five green arms pinning the operative anchored figures
  beside them (0/1 at the named revisions). Before (measured at the base
  bytes): no instrument exists (`git ls-tree 0c2573d7 tools/ | grep -c
  count-recheck` → 0) and the drift is measurable pre-instrument: the
  unanchored recount reads 0 at `859a736d` where both records print 4
  (receipt `carryin-correct-r70.txt`). After (forecast = rehearsal; live
  receipts at the round receipts commit): selftest
  `COUNT_RECHECK_SELFTEST: 6/6 pass` exit 0 (rehearsed pre-data,
  `reh-count-selftest.txt`; live receipt `count-selftest-r70.txt`); the
  standing sweep `COUNT_RECHECK: rows=7 met=7 unexpected=0` exit 0 with
  both red arms reading expect=drift printed=4 measured=0 ok (rehearsed,
  `reh-count-standings.txt`; live receipt `count-standings-r70.txt`);
  manifest id-grep → 7; S301 anchored grep 0 → 1; registry rows 160 → 161;
  the capability row enters the table, cited by its anchored form.
- **C2 (operability, verdict-only): the two standing manifests grow with
  their named successor rows, checker blobs unchanged.** (i)
  `tools/arm-liveness.json` grows 6 → 7 rows: `bind-r69-own-range-red` —
  the r69 lesson mistake 5's named successor — pins
  `tools/receipt-commit-bind.py` at `5541abaf` (the blob is byte-identical
  at the base, `git rev-parse` both = `c3e6a88e…`, verified before the row
  was authored) over the r69 own range `434a96e4..89869bea`, tally findings
  expect ≥2 exit 1: the rekey commit `b59ca7fe` names `red-decode-r69.txt`
  and `reh-red-decode-r69.txt` one commit before they land (`89869bea`
  carries them). Before: no r69-range row exists (`grep -c bind-r69
  tools/arm-liveness.json` → 0 at the base) and the sweep over that range
  reads findings=2 (the r69 disclosed erratum receipt
  `tip-self-sweep-r69.txt`; re-measured this round,
  `reh-bind-r69-range.txt`: commits=6 evidence=58 named=26 carried=25
  spans=3 bare=27 findings=2, exit 1). After: `ARM_LIVENESS: rows=7 live=7
  dead=0` exit 0 with `ARM_LIVE bind-r69-own-range-red tally=findings=2
  exit=1` (rehearsed, `reh-arm-live-standings-r70.txt`; live receipt
  `arm-live-standings-r70.txt`); the checker selftest unchanged 5/5;
  manifest id-grep → 7; the arm-liveness capability row synced append-only
  (its r69-era figures stand at the r69 bytes; old → new in this lesson).
  (ii) `tools/anchor-drift-sweep.json` grows 4 → 16 rows: the r69 lesson's
  next-round carry executed — every held row with a committed win-host
  snapshot extract whose bytes verify enters (S289's page via the r61
  re-open extract, S294, S295, S296, S297, S298; each blob's sha256
  re-computed at the base against its recorded digest — all six match),
  two rows each: the page h1 (resolution proof, the s299-page-h1
  precedent) and the page's own section heading that the anchor cell
  locates, extracted from the pinned snapshot bytes this round, never
  recalled (S295's cell locates its quote by fetched-page line and its
  "Generation definition" resolves to the page's own "5.1.3 Generation"
  heading — disclosed in the row; the page carries no exact "Concepts"
  heading; S289's cell names §DESCRIPTION, an exact match on the
  uppercase git-page form). Before: manifest id-grep 4 at the base. After:
  `ANCHOR_DRIFT: rows=16 met=16 unexpected=0` exit 0 with the S299 red arm
  still measured expect=absent measured=absent ok (rehearsed,
  `reh-anchor-standings-r70.txt`; live receipt `anchor-standings-r70.txt`);
  manifest id-grep → 16; the anchor-drift capability row synced
  append-only (old → new in this lesson).

Causally separable: C1 is two new files + the SOURCES row; C2 is
manifest-data edits to two existing manifests; neither needs the other
(the C2 sweeps run manifest rows only; the C1 sweep runs the new tool at
its new bytes against committed records).

## Shared no-harm story (declared forecast, then measured)

The SOURCES edit (one row + one tail note, the r67–r69 edit shape) is the
round's only monitored-file change: the live RED at the C1 SOURCES work
commit is forecast at lost=13 with cand_credited=51 — the SAME 13 headings
as the r68 AND r69 measured sets and this round's rehearsal (decoded
comparison receipt `reh-red-decode-r70.txt`: equal in order to both,
miss = 0), paid by the `r70-batch-1` rekey (the r69 as-run machinery
re-driven at this round's constants; 13 fresh input-keyed entries; ledger
771 → 784) restoring lost=0 ok exit 0 at BOTH floors (round `0c2573d7`
64 → 64, historic `8b0042bd` 46 → 64) plus rev mode 64/64, probe 20/20.
Additivity raw_old_only=0 on every landed pair (SOURCES mid-file row
insertion + tail note, verbatim_prefix=false disclosed; LOG/SCORECARD
appends pure). PROVINCE.md, SKILL.md, README.md, corpus/QUALITY.md,
tools/registry.json, SHONEN.md, tools/mutate-and-run.sh and the guarded
probe stay blob-identical base → tip; corpus/SOURCES.md is the only
monitored file in the round's diffs, rekeyed. The round's new tool files
and manifest edits are in no cold-read section's input union (verified
against the r69 union plan's 7702 union paths before the declaration —
tools/count-recheck.py, tools/count-recheck.json,
tools/anchor-drift-sweep.json, tools/arm-liveness.json and
tools/receipt-commit-bind.py all absent; SOURCES.md present, rekeyed).
Census exit 0 at both ends; registry rows 160 → 161 (S301).

## Gate

- Sourced row opened this round: **S301** (Git git-grep documentation,
  https://git-scm.com/docs/git-grep, fetched 2026-11-02, HTTP date Mon,
  02 Nov 2026 06:50:37 GMT; 87627 B; sha256
  `07b9f902e6d3e22a476e408fcb4091599cd5dff48764d0af10abee5cb6c0f2a8`;
  extract `.ufo/evidence/round-70/win-host/sources/s301-git-grep.html`,
  snapshot-pinned per the r41 docs-clock lesson). Located quote (the
  --count option paragraph; 13 words): "Instead of showing every matched
  line, show the number of lines that match." Grounding: the count-recheck
  rows recount a record's printed figure with `git grep -c [-E] <pattern>
  <rev> -- <path>` — the page's --count contract ("show the number of
  lines that match") is the definition of what the recount measures; the
  zero-match shape (no output, exit 1 → the count 0) is measured on this
  host and disclosed in the tool docstring (the page carries no
  exit-status section). The page and scope are previously unheld: `git
  show 0c2573d7:corpus/SOURCES.md | grep -c 'docs/git-grep'` → 0 at the
  base; the held-page grep ran BEFORE the fetch was staged (the r68
  mistake-3 discipline); no within-scope duplicate — S289/S293 hold the
  git-cat-file page, S294 gitattributes, S296 git-commit, S297
  git-diff-tree, S298 git-rev-list, S091 gitrevisions, all different
  pages.
- Rejections: one candidate refused before staging — the Python subprocess
  documentation (the natural ground for the stage-runner design first
  sketched): docs.python.org/3/library/subprocess.html is already held as
  S049 (r14), so a row would be a within-scope duplicate (CORPUS.md rule 2;
  the S293/S285 precedent); the instrument's command of record moved to
  git grep, whose defining page is genuinely unheld. No other candidate
  was staged — staging a fetch to manufacture a row would be dishonest
  (the r66 S091 precedent). The standing rejections S293 and S285 keep
  their census markers.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (receipt `census-start-r70.txt`; the
  pre-existing 17 W04 + 1 W01 set) and exit 0 at round end at both shapes
  (receipts `census-end-r70.txt` at the fleet root and
  `census-end-lanetip-r70.txt`; the fleet-root `tameshi-shokunin` path is
  a symlink to this lane repo on this host, disclosed — both receipts
  carry the same validated state, 161 rows, S301 census-clean).

## Mistakes (mined this round, all self-caught in the scratch before any
## live measurement depended on them)

1. **The selftest fixture's red arms cited a defect its bytes did not
   carry (class: fixture-figure-not-in-span; captured-by: the first
   count-recheck selftest run reading 3/6 — arm 1 MISMATCH measured=3,
   arms 2 and 3 ERROR printed-token-absent-in-span, before any standing
   sweep).** The toy record carried only the true figure, so the drift
   arms pinned spans in which their printed integer did not occur — the
   checker's span binding refused them, correctly, and the first arm's
   count pattern had been assumed ("a" matches 2 lines) instead of derived
   from the fixture bytes (3 lines match). Fix: the fixture record carries
   BOTH the true figure and a stale draft figure ("said 2 gates"), and the
   pattern re-derived from the data bytes; the selftest then reads 6/6
   (receipt `reh-count-selftest.txt`). The mined practice: a selftest
   fixture's red arms need their defect to EXIST in the fixture bytes —
   the r69 manifest-row-from-memory practice one level down; fixture
   expectations are read off the fixture bytes, never assumed.
2. **A receipt generator ran counting commands through the host shell
   (class: win32-shell-quoting-masked-fallback; captured-by: reading the
   first correction-receipt draft — its own lines read exit 255 and empty
   counts on the anchored commands).** The draft ran the commands with
   subprocess shell=True; on this host that shells through cmd.exe, which
   does not strip single quotes, so git received quoted garbage (exit 255)
   while an `out or '0'` fallback printed a fake 0 over the failure — a
   fabricated figure one read away from landing in a receipt. Fix: every
   counting command in the receipt runs as argv stages with no shell, exit
   codes named, no fallback masking; the receipt was regenerated
   (`carryin-correct-r70.txt`). The r69 codec discipline extended: the
   host shell is part of the console surface — a shaped command line is
   not a command; argv lists only, and a fallback that substitutes a value
   on failure is a fabrication vector, removed on sight.
3. **A located quote searched from memory of a different page (class:
   quote-from-memory; captured-by: the page-text search reading zero hits
   — the first S301 quote searched the fetched git-grep page for the GNU
   grep phrasing "Suppress normal output; instead print", recalled from
   the held grep manual, not the page's own words).** The git-scm page
   phrases the --count option differently. Fix: the located quote read off
   the fetched bytes ("Instead of showing every matched line, show the
   number of lines that match.") and its word count derived from those
   bytes (13 words). The r69 mistake-2 practice applied to source rows:
   quotes are read off the pinned bytes, never recalled.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question stands unanswered — an L1-only round, disclosed.
- The declaration commit lands first (this lesson, the SCORECARD
  corrections + planned block, the LOG declared entry, the S301 extract +
  fetch headers, the round-start census receipt, and the rehearsal receipts
  under `.ufo/evidence/round-70/win-host/rehearsal/` — every pre-data run
  this forecast rests on), verified by diff-tree before the next stage.
- The live run: C1's SOURCES row lands alone (the C1 SOURCES work commit —
  the RED is measured at this commit, forecast above); the count-recheck
  tool + manifest follow (the C1 tool work commit); the two manifest
  successor-row edits land (the C2 work commit); the rekey run-book
  re-drives the r69 machinery at this round's constants (the
  constants-only diff receipted as `make-rebind-r70.diff`); the guards run
  on this host at every claimed pair; the receipts land per the
  receipt-after-subject ordering; every landing is verified with
  `git diff-tree -r --name-status` before the next stage, and the round
  ends with a self-sweep of the round range plus a carries-what-it-names
  check of the tip commit before push.
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); corpus/lessons appends are LF; SOURCES.md (LF) carries
  the row insertion and the tail note. No other monitored file changes.

## Verdicts (receipts land in the commit(s) following the work commits;
## expected receipts, pinned here pre-data)

- C1: `COUNT_RECHECK_SELFTEST: 6/6 pass` exit 0 (receipt
  `count-selftest-r70.txt`, the live run from the landed bytes); the
  standing sweep `COUNT_RECHECK: rows=7 met=7 unexpected=0` exit 0 with
  both red arms reading expect=drift printed=4 measured=0 ok (receipt
  `count-standings-r70.txt`); manifest id-grep → 7; S301 grep 0 → 1;
  registry rows 160 → 161; the capability row enters the table (anchored
  grep 0 → 1).
- C2: `ARM_LIVENESS: rows=7 live=7 dead=0` exit 0 with `ARM_LIVE
  bind-r69-own-range-red tally=findings=2 exit=1` (receipt
  `arm-live-standings-r70.txt`; the checker selftest unchanged 5/5,
  receipt `arm-liveness-selftest-r70.txt`); `ANCHOR_DRIFT: rows=16 met=16
  unexpected=0` exit 0 with the red row expect=absent measured=absent ok
  (receipt `anchor-standings-r70.txt`); manifest id-greps 7 and 16; the
  arm-liveness and anchor-drift capability rows synced append-only (the
  r67-correction-4 precedent; the r69-era figures stand at the r69 bytes;
  old → new in this lesson).
- Shared: the RED at the C1 SOURCES work commit reads lost=13 RED exit 1
  with cand_credited=51 and the 13 LOST heading lines equal in order to
  the r68 AND r69 sets (miss = 0; receipt `live-red-r70.out` with the JSON
  receipt `red-receipt-r70.json` and the decoded comparison
  `red-decode-r70.txt`), then the rebind summary line REBIND OK
  sections=13 entries_added=13 ledger_before=771 (receipt
  `rebind-stdout-r70.txt`; ledger 771 → 784; machinery constants-only
  diff `make-rebind-r70.diff`) → lost=0 ok exit 0 at BOTH floors at the
  rekey commit (receipts `live-green-r70.out`: round floor `0c2573d7`
  64 → 64; `live-green-hist-r70.out`: historic `8b0042bd` 46 → 64) plus
  rev mode credited=64/64 probe 20/20 (receipt `live-revmode-r70.out`);
  additivity raw_old_only=0 on SOURCES (base → the C1 SOURCES work commit;
  verbatim_prefix=false disclosed — the mid-file row insertion + tail
  note; receipt `additivity-sources-r70.txt`), on the ledger (C1 SOURCES
  work commit → rekey commit; verbatim_prefix=false disclosed — the
  mid-file entries-array insertion; receipt `additivity-ledger-r70.txt`),
  and on the LOG/SCORECARD pairs at the tip receipts commit (receipt
  `additivity-logscorecard-r70.txt`); the tip guards at both floors + rev
  (`live-tip-guard-r70.out`, `live-tip-guard-hist-r70.out`,
  `live-tip-revmode-r70.out`), the tip invariant sweeps
  (`qline-tip-log-r70.txt`, `qline-tip-scorecard-r70.txt`,
  `qline-green-round-70.txt` — this lesson sweeps clean), the round-range
  self-sweep (`tip-self-sweep-r70.txt` — forecast findings zero exit 0),
  and the census end receipts (`census-end-r70.txt` at the fleet root,
  exit 0; `census-end-lanetip-r70.txt` at the lane-tip shape, 161 rows).
  No owned axis harmed: depth 10, freshness 9, calibration 8 unchanged
  (no depth or freshness surface touched — PROVINCE.md, SKILL.md,
  README.md, corpus/QUALITY.md, tools/registry.json, SHONEN.md,
  tools/mutate-and-run.sh and the guarded probe
  `tools/coldread-precheck-portable.py` (blob sha256 `892a045d…`)
  blob-identical base → tip; the diff-tree check over those paths is
  empty and corpus/SOURCES.md is the only monitored file in the round's
  diffs, rekeyed).

## Next-round carry

- count-recheck successor rows: any future routed numeric record defect
  with an in-lane record enters as its round routes it; fleet-repo records
  (the round reports) are outside the lane tree — the two report-side
  count nits stay corrected by receipt only, with no standing row (a
  host-specific fleet-root path in a committed manifest would be
  non-portable; disclosed).
- anchor-drift successor rows for the kaika/round-4x snapshot extracts
  (S269/S270, the waves trees): the extracts exist in-tree but are PDFs;
  the sweep's heading extraction is html.parser (S300), an HTML surface;
  a PDF heading parser is a different mechanism — named successor work.
- The backing boundary (the r69 carry) stands: a full attestation-chain
  semantics for the quoted-line checker is named successor work (no
  routed demand).
- The rekey payment is current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it.
- The guarded probe digest `892a045d…` is unchanged; the probe-arms
  re-run obligation stays attached to any future probe edit.
- considerthese 2026-10-28 proposals 3–5 remain unadopted; proposals 1–2
  are fully landed (r65/r68, r66).
- Pre-existing tree oddity, observed not absorbed: the root-level `C:`
  tree. Out of scope again; recorded for the operator.

4. **The plumbing helper silently drops absolute paths (class:
   absolute-paths-dropped-by-helper; captured-by: the round's own self-sweep
   reading findings=19 exit 1 against the pinned findings=0 forecast - the
   sweep reads commits=6 evidence=32 named=14 carried=14 spans=4 bare=37
   findings=19, all names-unknown at the receipts commit `22807192`).** The
   receipts commit's message named 19 receipt files its tree does not carry:
   the 20 receipt paths were passed to treecommit as absolute paths; the
   helper commits repo-relative paths and silently ignored the rest, so
   `22807192` carried only LOG.md and SCORECARD.md while its message named
   the receipts. Fix: disclosed in the LOG and the SCORECARD errata and this
   mistake (all landing with the receipts-repair commit - the r66/r67/r69
   erratum precedents: the forecast reported as measured, never re-scoped),
   the receipts land with that commit, the landed history stays, and a
   future bind-erratum manifest row may pin the `22807192` pair as its
   standing red arm (the r69 mistake-5 pattern). The mined practice: pass
   repo-relative paths ONLY, and verify the landing with
   `git diff-tree -r --name-status` BEFORE the commit message is written -
   the carries-what-it-names check runs on the landed tree, not on the
   intended one; the round's own C2 instrument class caught the round.
