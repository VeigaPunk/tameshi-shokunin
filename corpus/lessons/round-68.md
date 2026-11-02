# tameshi round 68 — lesson (hyaku, 2026-11-02)

L1 `TameshiR68` (round 68). Base `859a736deb1e26fd16a0cbd10f6bab0636c7a3a2`
(= origin/master; the commit that landed the r67 non-author closure).
Dispatch host: win32 (python 3.13.15 native `python`; git
2.55.0.windows.3; `core.autocrlf=false` in the lane repo). Receipts:
`.ufo/evidence/round-68/win-host/` — receipt-after-subject ordering (the
r61–r67 precedent): records land first, receipts follow in the same or the
next commit, and every commit message names only file tokens its tree
carries. The scratch is deleted with the round.

## Carry-in (r67 non-author closure)

The r67 closure (`859a736d`) admitted round 67 clean: no routed defects.
The one note — the round-67 report's "7 changed lines" machinery-diff
figure against the receipt's 6 changed pairs — was ruled constants-only
substance, verified, no action needed. Nothing to land; this round starts
from the r67 tip with an empty carry-in.

## Fresh-start duty

The prompt's fresh-start block lists r58/r59/r60 (the last REJECTED
closures). They were re-read before anything was declared
(`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The premise is
stale — r61 through r67 were all admitted — but the duty was performed and
each standing ruling is honored: r58's — positive controls must actually
bind and a refused deciding run is the honest outcome (this round's
forecasts were measured against the base bytes BEFORE the declaration: the
rehearsal receipts under `.ufo/evidence/round-68/win-host/rehearsal/` are
the pre-data runs, and the RED forecast is the decoded-identical r67
shape, miss = 0, receipt `reh-red-decode-r68.txt`); r59's — a counter
must discriminate a cheat family (the figure-attribution instrument's
cheat family is the anywhere-in-cited-set relaxation: the committed
control `controls/cheat-anywhere-passes-red.txt` shows the set-matcher
passing the exact pair the instrument flags, because the figure IS in the
round's other receipt — the r59 rule that a skip-the-work strategy must
fail the counter is met by construction: the named-receipt binding is the
work); r60's — a round's no-harm guard must run ON this host at the
revision pair it claims (the portable precheck, worktree blob sha256
`892a045d…`, runs at every measured pair below; RED + green + rev mode
all on this host).

Ruled out this round, with reasons: (a) any edit to
`tools/coldread-precheck-portable.py` — the guarded digest is pinned
(`892a045d…`) and any probe edit re-owes the probe-arms re-run; C2 runs
the probe as an instrument at pinned bytes and needs no probe change;
(b) SKILL.md / QUALITY.md / README.md / PROVINCE.md content edits — each
extends the rekey payment beyond the one SOURCES edit the sourced claim
requires; (c) a freshness-axis move — the r45 counter is a frozen
Linux-host shape, reviving it is operator-priced future work; (d) a
depth-axis move — depth is capped at 10, no room to move; (e) the
quoted-line self-referential-backing exclusion (the r67 lesson's mistake-4
successor sweep work) — a second checker-blob change in the same round
would double the deliberate re-run surface (this round already changes
the arm-liveness checker deliberately) without a routed demand; named for
a successor round that changes that checker deliberately; (f)
manifesting the additivity counter's red arm — no real-history failure
exists to pin; manufacturing one would be synthetic (r59 ruling); (g) the
whole-history receipt sweep — scoped, unpriced future work; (h) adopting
MORE considerthese proposals — at most one per round; this round adopts
proposal 1's semantic half via C1 (its byte-backing half landed r65;
proposals 3–5 do not fit the round's routed work); (i) the root-level
`C:` tree oddity — live-lane tree surgery, priced out since r65,
recorded for the operator.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration, the lowest scored numeric axis at 8; capability
  acquisition; adopts considerthese 2026-10-28 proposal 1's semantic
  half — the figure-attribution instrument the r67 lesson named as the
  successor calibration instrument).** `tools/figure-attribution.py` +
  `tools/figure-attribution.json` (new; schema
  `tameshi-figure-attribution-v1`): a record figure pinned to ONE named
  receipt must be a byte substring of BOTH the record's committed bytes
  and that receipt's committed bytes, both read from git objects at
  pinned revisions (never a worktree); rows declare `expect`
  attributed|misattributed so the standing red arm MEASURES
  misattributed on every sweep, never assumes it; unresolvable inputs
  are setup exit 2 before any row effect; a zero-row manifest is
  refused exit 2. Standing manifest: three real-history rows pinned at
  `859a736d` — the r66 stale selftest figure (expect misattributed: the
  SCORECARD R66-C1 cells' figure against the live receipt reading
  seven-of-seven), the same figure against its true carrier (expect
  attributed: the round-66 lesson's pre-data pin vs the preserved
  rehearsal receipt — attribution-specificity, the flip a set-matcher
  cannot see), and the correction of record (expect attributed: the
  R67-correction figure vs the live receipt). Before (measured at the
  base bytes, receipts `reh-figattn-selftest.txt`,
  `reh-figattn-standings.txt`, `reh-figattn-cheat.txt`): no instrument
  exists (`git ls-tree 859a736d tools/` carries no figure-attribution
  path), and the anywhere-in-cited-set matcher passes the red pair —
  `CHEAT_ANYWHERE: found=1 cited=2 (set-matcher: pass=true)` — the r66
  defect class was caught by a human, not by any standing check. After
  (expected, forecast): selftest
  `FIGURE_ATTRIBUTION_SELFTEST: 7/7 pass` exit 0 (arms: attributed,
  misattributed-met, mismatch-caught, figure-absent, unresolvable
  exit 2, vacuous-manifest exit 2, usage exit 2); standing sweep
  `FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0` exit 0 with
  `FIGURE_ROW r66-stale-selftest-figure-red expect=misattributed
  measured=misattributed ok`; the capability row enters the table.
- **C2 (operability, verdict-only; sourced on new row S299, opened this
  round — Python shutil documentation).** The arm-liveness checker
  gains the per-row scratch slot the r67 lesson named as the
  precondition: an args literal `{work}` is replaced by a FRESH
  `tempfile.mkdtemp` directory per row, deleted with the run together
  with the per-row instrument extraction directory (which earlier
  rounds leaked on disk) via `shutil.rmtree(..., ignore_errors=True)`
  in a finally — mkdtemp's caller-deletion duty is held S279, rmtree's
  contract is S299. Selftest 4/4 → 5/5 (arm 5: the toy-work instrument
  moves its tally ONLY when the slot actually supplied the directory —
  findings=0 without it, so the slot itself is the thing under test).
  The manifest grows 5 → 6 rows: the no-harm guard's RED arm — the last
  manifestable receipt-family arm without a committed input — enters as
  `precheck-sources-red`, pinning
  `tools/coldread-precheck-portable.py` at `859a736d` (blob sha256
  `892a045d…`, the guarded digest) over the committed pair floor
  `7362e15c` / cand `ab67ddd6`, tally `lost` expect ≥13, baseline 0,
  exit 1 (the r67 receipt `live-red-r67.out` is the pinned record).
  Before (measured at the base bytes, receipts
  `reh-liveness-selftest.txt`, `reh-liveness-standings.txt`): checker
  selftest 4/4; manifest 5 rows; no `{work}` literal in the checker
  bytes; the standing sweep runs 5 rows. After (expected, forecast):
  selftest `ARM_LIVENESS_SELFTEST: 5/5 pass` exit 0; standing sweep
  `ARM_LIVENESS: rows=6 live=6 dead=0` exit 0 with
  `ARM_LIVE precheck-sources-red tally=lost=13 exit=1`; manifest
  id-grep 5 → 6; S299 grep 0 → 1; registry 158 → 159. The arm-liveness
  capability row is NOT edited in place: under the additivity discipline
  the registry home is append-only, so the r68 sync (selftest 5/5, rows
  6 live 6 at the r68 bytes; the r66 figures stand for the r66 bytes)
  is a note in the round-68 measured block — the r67 correction-4
  precedent — and the old → new figures are logged in this lesson.

Causally separable: C1 is two new files (tool + manifest); C2 is the
arm-liveness checker + manifest + the SOURCES row; neither needs the
other (the C1 sweeps read committed history only; the C2 sweep runs the
checker at its new bytes against pinned instruments).

## Shared no-harm story (declared forecast, then measured)

The SOURCES edit (one row + one tail note, the r67 edit shape) is the
round's only monitored-file change: the live RED at the C2 work commit is
forecast at `lost=13 RED` with `cand_credited=51` — the SAME 13 headings
as the r67 measured RED and this round's rehearsal (decoded comparison
receipt `reh-red-decode-r68.txt`: equal in order, miss = 0), paid by the
`r68-batch-1` rekey (the r67 as-run machinery re-driven at this round's
constants; 13 fresh input-keyed entries; ledger 745 → 758) restoring
`lost=0 ok` exit 0 at BOTH floors (round `859a736d` 64 → 64, historic
`8b0042bd` 46 → 64) plus rev mode 64/64, probe 20/20. Additivity
`raw_old_only=0` on every landed pair (SOURCES mid-file row insertion +
tail note, `verbatim_prefix=false` disclosed; LOG/SCORECARD appends
pure; ledger mid-file insertion disclosed). PROVINCE.md, SKILL.md,
README.md, corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe stay blob-identical base →
tip. Census exit 0 at both ends; registry rows 158 → 159 (S299). The
round-range self-sweep reads `findings=0` exit 0 — every commit message
names only file tokens its tree carries.

Cost profile to record: the standing arm-liveness sweep is now
minutes-scale on this host (measured ~3.0 min for the 6-row sweep at the
rehearsal) — the precheck row runs two full monitor passes at the
committed pair; every other row is seconds-scale. Recorded so a reader
does not read the slower sweep as a hung instrument.

## Gate

- Sourced row opened this round: **S299** (Python shutil documentation,
  https://docs.python.org/3/library/shutil.html, fetched 2026-11-02,
  HTTP last-modified Mon, 02 Nov 2026 09:15:24 GMT; 120937 B; sha256
  `34f6ec56608e2deb03b3b8c971bd62585e5075c70bcff84aa60b0143bef197e8`;
  extract `.ufo/evidence/round-68/win-host/sources/s299-shutil.html`,
  snapshot-pinned per the r41 docs-clock lesson). Located quote
  (§Directory deletion operations, rmtree first paragraph; 19 words):
  "Delete an entire directory tree; path must point to a directory (but
  not a symbolic link to a directory)". Grounding: the arm-liveness
  checker's round-68 per-row scratch slot hands each instrument a fresh
  mkdtemp directory and removes it — with the per-row instrument
  extraction directory — in a finally via `shutil.rmtree(...,
  ignore_errors=True)`; the same paragraph's ignore_errors semantics
  ("If ignore_errors is true, errors resulting from failed removals
  will be ignored") are why the cleanup can never mask a row verdict.
  The page and scope are previously unheld: `grep -c shutil
  corpus/SOURCES.md` → 0 at `859a736d`; no within-scope duplicate —
  S278/S279 hold the Lib/tempfile.py source and the tempfile docs page
  (mkdtemp's creation side), S153/S154 the ast/pathlib pages, different
  documents.
- Rejections: NONE this round — the one new row was adopted. One
  candidate was REFUSED before staging: the Python tempfile
  documentation as the S299 candidate — the page is already held as
  S279, so a row would be a within-scope duplicate (CORPUS.md rule 2;
  the S293 precedent); the pre-staging grep that caught it is mined as
  mistake 3 below, and the claim's ground moved to the genuinely unheld
  rmtree page. Price-outs, with reasons: the git-ls-tree documentation
  was NOT fetched — no claim rests on it this round (both new/changed
  tools read blobs via cat-file-shaped `git show REV:path`, held S289),
  and staging a fetch to manufacture a row would be dishonest (the r66
  S091 precedent, r67 price-out repeated); the git-log documentation —
  same disposition. The standing rejection S293 (within-scope duplicate
  of S289) keeps its W04 census marker.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (receipt `census-start-r68.txt`; the
  pre-existing 17 W04 + 1 W01 set) and exit 0 at round end (receipts
  `census-end-r68.txt` at the fleet root and
  `census-end-lanetip-r68.txt` at the lane-tip shape; the same
  pre-existing set; the new S299 row census-clean).

## Mistakes (mined this round, all self-caught in the scratch before any
## live measurement depended on them)

1. **A decode codec inherited from the wrong round's note flips a
   byte-identity verdict (class: decode-codec-attrition;
   captured-by: the rehearsal RED decode reading `equal in order:
   False` on sets that are byte-identical).** The r67 lesson records
   that "the r66 receipt is cp1252-encoded, this round's is UTF-8";
   this round's first decode script applied cp1252 to the r67 receipt
   (`reh/r67-red-ref.txt`), mojibake-ing every em-dash and failing the
   comparison. Fix: decode each receipt by its own recorded encoding —
   the r67 receipt is UTF-8 — and re-compare: rehearsal_lost=13,
   ref67_lost=13, equal_in_order=True, miss=0 (receipt
   `reh-red-decode-r68.txt`). The mined practice: a decoded comparison
   names the codec of EVERY side in its receipt, and a False verdict on
   an expected-identical pair is investigated byte-wise before any
   record depends on it (here the "difference" was pure decode
   artifact — the underlying LOST sets never moved).
2. **A module-scope name used by new code but imported only inside a
   function crashes the selftest before any arm fires (class:
   import-scope-vs-new-call-site; captured-by: the pre-data selftest
   run dying with `NameError: name 'shutil' is not defined` at the
   first row's cleanup).** The arm-liveness v2 cleanup moved
   `shutil.rmtree` into `check_row`'s new finally, but the module
   imported shutil only inside `selftest`'s own finally (the v1 shape);
   the first selftest run crashed with exit 1 and a traceback — caught
   before any sweep was trusted. Fix: `import shutil` at module scope;
   the selftest then reads 5/5 (receipt `reh-liveness-selftest.txt`).
   The mined practice: a checker change that adds a call site must move
   the callee's import to the scope of the NEW call site, and the
   selftest runs before any standing sweep (the r67 mistake-1
   discipline: a broken harness read is a harness defect, caught
   pre-data).
3. **The staged sourced-row candidate was a within-scope duplicate of a
   held page (class: staged-row-duplicate; captured-by: the
   pre-staging held-page grep — `grep -c tempfile corpus/SOURCES.md` →
   2 at the base, S278/S279).** The round's first S299 candidate was
   the Python tempfile documentation (mkdtemp's caller-deletion duty,
   the natural ground for the scratch slot); the page is already held
   as S279, and appending it would have been the S293/S285 duplicate
   class. Fix: the candidate was refused before staging (CORPUS.md
   rule 2) and the row moved to the genuinely unheld page its other
   half rests on — shutil's rmtree contract (`grep -c shutil` → 0).
   The mined practice: the held-page grep runs BEFORE the fetch is
   staged into a row, not after; the refusal and its reason are
   recorded in the Gate, not silently dropped.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this
  host; the r60 L0 question stands unanswered — an L1-only round,
  disclosed.
- The declaration commit lands first (this lesson, the SCORECARD planned
  block, the LOG declared entry, the S299 extract + fetch headers, the
  round-start census receipt, and the rehearsal receipts under
  `.ufo/evidence/round-68/win-host/rehearsal/` — every pre-data run this
  forecast rests on), verified by diff-tree before the next stage.
- The live run: C1's tool + manifest land in the C1 work commit; C2's
  checker + manifest + the S299 row land in the C2 work commit; the RED
  is measured at that commit (forecast above); the rekey run-book
  re-drives the r67 machinery at this round's constants (the
  constants-only diff is receipted as `make-rebind-r68.diff`); the
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

- C1: `FIGURE_ATTRIBUTION_SELFTEST: 7/7 pass` exit 0 (receipt
  `figattn-selftest-r68.txt`, the live run from the landed bytes); the
  standing sweep `FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0` exit 0
  (receipt `figattn-standings-r68.txt`) with the red row
  `FIGURE_ROW r66-stale-selftest-figure-red expect=misattributed
  measured=misattributed ok`; the cheat control
  `CHEAT_ANYWHERE: found=1 cited=2 (set-matcher: pass=true)` beside the
  instrument's verdict on the same pair (receipt
  `cheat-anywhere-passes-red.txt` under `controls/`); the capability
  row grep 0 → 1.
- C2: `ARM_LIVENESS_SELFTEST: 5/5 pass` exit 0 (receipt
  `arm-liveness-selftest-r68.txt`); manifest id-grep 6; the standing
  sweep `ARM_LIVENESS: rows=6 live=6 dead=0` exit 0 with
  `ARM_LIVE precheck-sources-red tally=lost=13 exit=1` (receipt
  `arm-live-standings-r68.txt`; base standings at 5 rows receipted as
  `arm-live-standings-base-r68.txt` from the r67 checker bytes); the
  bind checker selftest unchanged (`bind-selftest-r68.txt` 7/7) and the
  quoted-line selftest unchanged (`qline-selftest-r68.txt` 4/4) — no
  other checker blob changed; S299 grep 0 → 1; registry 158 → 159.
- Shared: the RED at the C2 work commit reads `lost=13 RED` exit 1 with
  cand_credited=51 and the 13 LOST heading lines equal in order to the
  r67 set (miss = 0; receipt `live-red-r68.out` with a decoded
  comparison receipt `red-decode-r68.txt`), then the rebind summary
  line `REBIND OK sections=13 entries_added=13 ledger_before=745`
  (receipt `rebind-stdout-r68.txt`; ledger 745 → 758; machinery
  constants-only diff `make-rebind-r68.diff`) → `lost=0 ok` exit 0 at
  BOTH floors at the rekey commit (receipts `live-green-r68.out`: round
  floor `859a736d` 64 → 64; `live-green-hist-r68.out`: historic
  `8b0042bd` 46 → 64) plus rev mode credited=64/64 probe 20/20
  (receipt `live-revmode-r68.out`); additivity `raw_old_only=0` on
  SOURCES (base → C2 work commit; `verbatim_prefix=false` disclosed —
  the mid-file row insertion + tail note; receipt
  `additivity-sources-r68.txt`), on the ledger (C2 work commit → rekey
  commit; `verbatim_prefix=false` disclosed — the mid-file
  entries-array insertion; receipt `additivity-ledger-r68.txt`), and
  on the LOG/SCORECARD pairs at the tip receipts commit (receipt
  `additivity-logscorecard-r68.txt`); the tip guards at both floors +
  rev (`live-tip-guard-r68.out`, `live-tip-guard-hist-r68.out`,
  `live-tip-revmode-r68.out`), the tip invariant sweeps
  (`qline-tip-log.txt`, `qline-tip-scorecard.txt`,
  `qline-green-round-68.txt` — this lesson sweeps clean), the
  round-range self-sweep (`tip-self-sweep-r68.txt` — forecast findings
  zero exit 0), and the census end receipts (`census-end-r68.txt` at
  the fleet root, exit 0; `census-end-lanetip-r68.txt` at the
  lane-tip-shaped fleet root, 159 rows). No owned axis harmed: depth
  10, freshness 9, calibration 8 unchanged (no depth or freshness
  surface touched — PROVINCE.md, SKILL.md, README.md, corpus/QUALITY.md,
  tools/registry.json, SHONEN.md, tools/mutate-and-run.sh and the
  guarded probe `tools/coldread-precheck-portable.py` (blob sha256
  `892a045d…`) blob-identical base → tip; `git diff-tree -r
  --name-status 859a736d <tip> -- PROVINCE.md SKILL.md README.md
  corpus/QUALITY.md tools/registry.json SHONEN.md
  tools/mutate-and-run.sh tools/coldread-precheck-portable.py` is empty
  and corpus/SOURCES.md is the only monitored file in the round's
  diffs, rekeyed).

## Next-round carry

- The figure-attribution manifest pins three real-history rows; the
  natural successor rows are the LOG's own stale figure cell (the
  round-final receipts line — same class, held in reserve to keep the
  manifest at real-history pairs only) and any future misattribution
  the closures route.
- The quoted-line self-referential-backing exclusion (r67 mistake 4)
  stays named successor work: a checker-blob change of its own.
- The rekey payment is current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it.
- The guarded probe digest `892a045d…` is unchanged; the probe-arms
  re-run obligation stays attached to any future probe edit.
- The standing arm-liveness sweep is minutes-scale since the precheck
  row entered (cost profile above); a successor round may want a
  `--only` row filter — priced, not routed.
- considerthese 2026-10-28 proposals 3–5 remain unadopted; proposal 1
  is now fully landed (byte-backing half r65, semantic half this
  round).
- Pre-existing tree oddity, observed not absorbed: the root-level `C:`
  tree. Out of scope again; recorded for the operator.
4. **A receipt-generation command built with a relative path ran nothing
   and drafted a false receipt (class: relative-path-in-receipt-command;
   captured-by: reading the controls receipt's first draft before
   landing it — the set-matcher line read a python Errno 2 and
   `cheat rc=2` where the rehearsal had measured `CHEAT_ANYWHERE:
   found=1 cited=2 (set-matcher: pass=true)`).** The controls receipt
   for the cheat family was first generated with a `$PWD/../../..`
   relative path that resolved outside the workspace; the receipt would
   have landed a failed run as if it were the control. The same slip
   recurred on the first ledger-additivity attempt (the tool path
   resolved relative to the scratch cwd, `rc=2` with the receipt
   containing only the traceback). Fix: both regenerated — the cheat
   run with the absolute scratch path, the additivity run from the lane
   cwd — and the landed bytes carry the true runs (`controls/
   cheat-anywhere-passes-red.txt`: found=1, cheat rc=0;
   `additivity-ledger-r68.txt`: `raw_old_only=0 ... rc=0`). The mined
   practice: receipt-generation commands take absolute paths or run
   from a pinned cwd, and a receipt whose verdict contradicts its
   rehearsal is read before it is landed, never shipped. Both were
   caught pre-landing by reading what the command had actually
   produced — the appendix discipline the r66 K1b slip class needs.
