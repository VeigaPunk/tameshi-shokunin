# tameshi round 67 — lesson (hyaku, 2026-11-02)

L1 `TameshiR67` (round 67). Base `7362e15c0a60e685f0dfadb920582619002e150a`
(= origin/master; the commit that landed the r66 non-author closure's
spot-check). Dispatch host: win32 (python 3.13.15 native `python`; git
2.55.0.windows.3; `core.autocrlf=false` in the lane repo). Receipts:
`.ufo/evidence/round-67/win-host/` — receipt-after-subject ordering (the
r61–r66 precedent): records land first, receipts follow in the same or the
next commit, and every commit message names only file tokens its tree
carries. The scratch is deleted with the round.

## Carry-in addressed first (r66 non-author closure, four routed items, status-neutral)

All four landed at the corrections commit `436b60c5` (before this round's
declaration), append-only — the stale lines are preserved and stay flagged:

1. Lesson mistake row 4 (the K1b wrong-base pathspec slip: empty landing
   set) appended to `corpus/lessons/round-66.md` — it was missing while the
   round-66 report, the LOG measured entry, and the d5ab10ff message cited
   it as "mistakes 3–4".
2. The stale six-of-seven selftest figure (SCORECARD R66-C1 planned and
   measured rows, the LOG round-final receipts line, and the round-66
   lesson's pre-data Verdicts pin) corrected: the final checker bytes read
   `RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass` — receipt
   `.ufo/evidence/round-66/win-host/live-selftest-bind.txt`.
3. The own-range receipt pointer corrected: the receipt pins
   `469cde0f..5d969f4e`, not the erratum's cited `..e8e0f0e9` — this
   round re-ran both ranges at the pinned checker bytes and the pinned
   range's summary reproduces byte-identically (receipts
   `bind-own-range-r67.txt`, `bind-erratum-range-r67.txt`).
4. The "dropped from the tree" wording corrected: `b60ecab3` is an empty
   commit, its tree byte-identical to its parent's — no committed tree ever
   lost the lesson or the LOG; the d5ab10ff message carries the same
   phrasing and is never rewritten.

Plus the closure's routed defect 3 (registry-home sync): the capabilities
row still citing the r65-era four-of-four selftest is corrected by the
SCORECARD correction block (the registry home is append-only, so the note
is the sync). Instrument boundary found while measuring the before-state,
honestly: the standing quoted-line sweep does NOT flag the stale six-of-
seven cells as MISSING — they are byte-backed by
`.ufo/evidence/round-66/win-host/rehearsal/reh-selftest-bind.txt`, whose
preserved pre-correction bytes genuinely contain the old figure. A record
that misattributes a figure to the wrong receipt (the r66 defect class) is
beyond byte-backing; that semantic class stays inspection-caught (the
closure found it), and is recorded here as successor instrument work rather
than shipped as a heuristic this round (r59's ruling: no cheat-passable
arms).

## Fresh-start duty

The prompt's fresh-start block lists r58/r59/r60 (the last REJECTED
closures). They were re-read before anything was declared
(`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The premise is
stale — r61 through r66 were all admitted — but the duty was performed and
each standing ruling is honored: r58's — positive controls must actually
bind, and a refused deciding run is the honest outcome (this round's
forecasts were measured against the base bytes BEFORE the declaration, and
where one forecast proved wrong — the stale-cell red-demo above — the claim
was re-shaped to the measured truth before declaring, not re-scoped after
data); r59's — a counter must discriminate a cheat family (the manifest
rows added this round pin REAL-history red inputs — the r65 empty-commit
erratum range and the r66 own-range erratum — no synthetic arms); r60's — a
round's no-harm guard must run ON this host at the revision pair it claims
(the portable precheck, worktree sha256 `892a045d…`, runs at every measured
pair below; RED + green + rev mode all on this host).

Ruled out this round, with reasons: (a) any edit to
`tools/coldread-precheck-portable.py` — the guarded digest is pinned
(`892a045d…`) and any probe edit re-owes the probe-arms re-run; this round
needs no probe change; (b) SKILL.md / QUALITY.md / README.md / PROVINCE.md
content edits — each extends the rekey payment beyond the one SOURCES edit
the sourced claim requires; (c) a freshness-axis move — the r45 counter is
a frozen Linux-host shape, reviving it is operator-priced future work;
(d) a depth-axis move — depth is capped at 10, no room to move; (e) a new
figure-misattribution instrument (see the carry-in section: the class
needs semantic attribution, a design round of its own — disclosing the
boundary beats shipping a heuristic); (f) manifesting the no-harm guard's
RED arm this round — the arm-liveness checker has no per-row scratch-dir
slot, so the precheck's required `--work` path would either litter the
worktree or hard-code a host path, and a checker blob change re-owes the
r66 selftest/demo re-runs; named for a successor round that changes the
checker deliberately; (g) the whole-history receipt sweep — scoped,
unpriced future work; (h) adopting MORE considerthese proposals — at most
one per round, and none of proposals 3–5 fits this round's routed work;
the round adopts none; (i) the root-level `C:` tree oddity — live-lane
tree surgery, priced out since r65.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration, the lowest scored numeric axis at 8; the move is
  record-attribution honesty).** The four carry-in corrections land
  append-only and verifiably (greps below), and the round's own appends
  satisfy the byte-backing discipline: the standing quoted-line sweep over
  the LOG and the SCORECARD at the round tip reads EXACTLY the base
  missing and absent counts (the round introduces zero unbacked quotes and
  zero absent path cites), and the round-67 lesson sweeps clean from birth.
  Before (measured at the base bytes, receipts
  `qline-red-log-base.txt`, `qline-red-scorecard-base.txt`,
  `qline-red-round-66.txt`): LOG totals `missing=40 skipped=40` with
  8 absent path cites; SCORECARD totals `missing=10 skipped=178` with
  6 absent path cites; the round-66 lesson totals `missing=2 skipped=7`
  with none absent — both its missing quotes named (the full-range
  forecast shape — named nine, carried five, findings eight, the receipt
  printing the spans and bare counts in between so the contiguous
  forecast string exists in no receipt — and the pre-fix demo shape —
  tally unparsed, exit two, the pre-fix run's bytes were overwritten by
  the fixed re-run; both are pre-data forecast shapes whose committed
  receipts never contained those exact contiguous substrings; they stay
  as written — append-only lesson, not routed items); mistake-row-4
  grep 0; correction-marker greps 0. After (expected, forecast):
  mistake-row-4 grep 1; SCORECARD correction-marker grep 4; LOG
  corrections-entry grep 1; tip sweeps — LOG `missing=40 skipped=40`
  with the same 8 absent, and SCORECARD `missing=10 skipped=178` with
  the same 6 absent, UNCHANGED (every new quote backed by a cited
  receipt: the correction block cites
  `.ufo/evidence/round-66/win-host/live-selftest-bind.txt` and
  `live-bind-own-range.txt`, the entries cite this round's receipts);
  the round-67 lesson sweep reads zero missing and zero absent, exit 0.
- **C2 (operability, verdict-only; sourced on new row S298, opened this
  round).** The counter-arm liveness manifest grows its two declared
  successor rows (the r66 manifest note's scope flip, executed): the
  bind checker's erratum-range red arm — the r65 vacuous-pass case — and
  the bind checker's own-range red arm — the r66 self-caught erratum —
  both pinned at `5541abaf` (the corrected r66 checker bytes; the
  revision each row was verified against), both with real-history
  committed inputs, zero synthetic arms. Before (measured at the base
  bytes): `rows=3 live=3 dead=0` exit 0 (receipt
  `arm-live-standings-base-r67.txt`); manifest id-grep 3. After
  (expected, forecast): manifest id-grep 5; standing sweep
  `rows=5 live=5 dead=0` exit 0 with the two new rows reading
  `ARM_LIVE bind-erratum-range-red tally=findings=4 exit=1` and
  `ARM_LIVE bind-own-range-red tally=findings=42 exit=1` (receipt
  `arm-live-standings-r67.txt`); checker selftest unchanged 4/4 (no
  checker blob change — the rows are data).

Causally separable: C1 is records-only (SCORECARD/LOG/lesson bytes); C2 is
one manifest file; neither needs the other.

## Shared no-harm story (declared forecast, then measured)

The SOURCES edit (one row + one tail note, the r66 edit shape) is the
round's only monitored-file change: the live RED at the C2 work commit is
forecast at `lost=13 RED` with `cand_credited=51` — the SAME 13 headings as
the r66 measured RED, byte-equal in order (the section set that pins
SOURCES bytes; nothing else changes), miss = 0 required — paid by the
`r67-batch-1` rekey (the r66 as-run machinery re-driven at this round's
constants; 13 fresh input-keyed entries; ledger 732 → 745) restoring
`lost=0 ok` exit 0 at BOTH floors (round `7362e15c` 64 → 64, historic
`8b0042bd` 46 → 64) plus rev mode 64/64, probe 20/20. Additivity
`raw_old_only=0` on every landed pair (SOURCES mid-file insertion
`verbatim_prefix=false` disclosed; LOG/SCORECARD pure appends; ledger
mid-file insertion disclosed). PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md, tools/mutate-and-run.sh
and the guarded probe stay blob-identical base → tip. Census exit 0 at
both ends; registry rows 157 → 158 (S298). The round-range self-sweep
reads `findings=0` exit 0 — every commit message names only file tokens
its tree carries (the K1 range already verified: commits=1, evidence=4,
named=4, carried=4).

## Gate

- Sourced row opened this round: **S298** (Git git-rev-list documentation,
  https://git-scm.com/docs/git-rev-list, fetched 2026-11-01, HTTP date
  Mon, 02 Nov 2026 07:36:10 GMT; 254,766 B; sha256
  `7b7f21135a3e9007ae2c6a2986330abd5a690f3b49b03c3b90cd82dc90a03d62`;
  extract `.ufo/evidence/round-67/win-host/sources/s298-git-rev-list.html`).
  Located quote (§DESCRIPTION first paragraph, fetched-page line 3330;
  14 words): "List commits that are reachable by following the parent
  links from the given commit(s)". Grounding: the bind sweep's range walk
  is `git rev-list --reverse base..tip` — rev-list enumerates COMMITS by
  parent links, not changes, so an empty commit (same tree as its parent)
  is still in the walk with its message; that is exactly why the two
  manifest rows added this round are meaningful standing red arms over the
  r65 erratum range `7d7f9ca8..87e95597` (whose tip commit `87e95597` adds
  nothing) and why the frozen scope (S297: diff-tree's range-added paths)
  could never see them. The page and scope are previously unheld:
  `grep -c git-rev-list corpus/SOURCES.md` → 0 at the base (the held
  git-scm pages are cat-file S289/S293, revisions S091, attributes S294,
  commit S296, diff-tree S297 — different pages).
- Rejections: NONE this round — the one source opened was adopted as C2's
  claim ground. Price-outs, with reasons: the git-ls-tree documentation
  (the authority for the quoted-line tool's path-resolution rule) was NOT
  fetched — no claim rests on it this round, and staging a fetch to
  manufacture a row would be dishonest (the r66 S091 precedent); the
  git-log documentation — same disposition, no resting claim. The standing
  rejection S293 (within-scope duplicate of S289) keeps its W04 census
  marker.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (receipt `census-start-r67.txt`; the
  pre-existing 17 W04 + 1 W01 set) and exit 0 at round end (receipt
  `census-end-r67.txt` at the receipts tip; the same pre-existing set; the
  new S298 row census-clean).

## Mistakes (mined this round, all self-caught in the scratch before any
## live measurement depended on them)

1. **A tool extracted from git objects under a renamed file fails its
   selftest with a false 0/4 (class: extracted-blob-sibling-name;
   captured-by: the pre-data selftest run — arm 1 failed with rc=2 "can't
   open file …quoted-line-" before any sweep was trusted).** The
   quoted-line tool's selftest re-invokes itself as a hardcoded sibling
   filename (`quoted-line-exists.py` next to the script), so extracting
   the blob as `quoted-line-7362e15c.py` broke all four arms with usage
   exits, which would have read as a broken instrument. Fix: extract
   pinned blobs under the exact committed basename in their own scratch
   directory; the selftest then reads 4/4 (receipt
   `qline-selftest-r67.txt`). The mined practice: a pinned-blob harness
   preserves committed basenames — a selftest that cannot find itself is
   a harness defect, not an instrument defect.
2. **A cp1252 console crashes a UTF-8 record sweep mid-run (class:
   ansi-stdout-under-isolated-python; captured-by: the SCORECARD sweep
   aborting with UnicodeEncodeError on the arrow character inside a quoted
   span — `python -I` ignores the dispatch env's UTF-8 flag
   (PYTHONUTF8=1), so stdio fell back to the
   ANSI code page).** LOG.md and SCORECARD.md quote spans contain
   non-ASCII bytes; the sweep's stdout died before the TOTAL line on this
   host's default code page. Fix: run isolated tools with `python -I -X
   utf8` (UTF-8 mode sets stdio encoding explicitly — env vars stay
   ignored, which is the point of `-I`); all sweeps re-run clean and the
   receipts are UTF-8. The mined practice: on this host the invocation
   contract for record-sweeping tools is `-I -X utf8`, not `-I` alone.
3. **An exit code captured after a command substitution in the same echo
   reads the substitution's status, not the tool's (class:
   exit-code-capture-after-substitution; captured-by: the first sweep loop
   printing EXIT=0 for all three documents including the one that had just
   crashed — the `$(basename …)` substitution ran before `$?` expanded and
   reset it).** The red sweeps' first receipts would have recorded rc=0 on
   a crashing run — a false green on the exact instrument this round
   relies on. Fix: store `rc=$?` immediately after the command, before any
   substitution; the re-run receipts carry the true exits (1/1/1). The
   mined practice: exit codes are captured into a variable on the next
   line, never inline after a substitution.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question stands unanswered — an L1-only round, disclosed.
- The corrections commit `436b60c5` landed first with its receipts (the
  before-greps, the round-66 lesson sweep, both bind re-runs), verified by
  diff-tree (exactly 7 paths) and by the round-range bind sweep over
  `7362e15c..436b60c5` — summary `commits=1 evidence=4 named=4 carried=4`,
  findings zero (receipt `self-sweep-k1-r67.txt`, summary byte-identical
  to the pre-landing verification run).
- The live run: C2's manifest rows land with the S298 row in the C2 work
  commit; the RED is measured at that commit (forecast above); the rekey
  run-book re-drives the r66 machinery at this round's constants (the
  constants-only diff is receipted as `make-rebind-r67.diff`); the guards
  run on this host at every claimed pair; the receipts land per the
  receipt-after-subject ordering; every landing is verified with
  `git diff-tree -r --name-status` before the next stage, and the round
  ends with a self-sweep of the round range plus a carries-what-it-names
  check of the tip commit before push.
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); corpus/lessons appends are LF; SOURCES.md (LF) carries
  the row insertion and the tail note (pure 2-line insertion,
  old-lines-lost = 0). No other monitored file changes.

## Verdicts (receipts land in the commit(s) following the work commits;
## expected receipts, pinned here pre-data)

- C1: the correction greps at the tip read mistake-row-4 = 1, SCORECARD
  correction markers = 4, LOG corrections entry = 1; the tip sweeps
  (receipts `qline-tip-log.txt`, `qline-tip-scorecard.txt`) read LOG
  `missing=40 skipped=40` with the same 8 absent and SCORECARD
  `missing=10 skipped=178` with the same 6 absent, unchanged from the
  base receipts, and the round-67 lesson sweep reads zero missing, zero
  absent, exit 0 (`qline-green-round-67.txt`).
- C2: `ARM_LIVENESS_SELFTEST: 4/4 pass` exit 0 (receipt
  `arm-liveness-selftest-r67.txt`); manifest id-grep 5; the
  standing sweep reads `rows=5 live=5 dead=0` exit 0 with the two new
  ARM_LIVE lines as forecast; the two row receipts
  (`bind-erratum-range-r67.txt`, `bind-own-range-r67.txt`, landed at the
  corrections commit) carry the pinned summaries
  `commits=7 evidence=47 named=0 carried=0 spans=2 bare=8 findings=4` and
  `commits=6 evidence=42 named=43 carried=22 spans=3 bare=47 findings=42`.
- Shared: the RED at the C2 work commit reads `lost=13 RED` exit 1 with
  the 13 headings byte-equal in order to the r66 set (miss = 0; receipt
  `live-red-r67.out`), then the rebind summary line
  `REBIND OK sections=13 entries_added=13 ledger_before=732` (receipt
  `rebind-stdout-r67.txt`) and `lost=0 ok` exit 0 at both floors at the
  rekey commit and the receipts tip, rev mode 64/64 probe 20/20
  (receipts `live-green-r67.out`, `live-green-hist-r67.out`,
  `live-revmode-r67.out`, `live-tip-guard-r67.txt`,
  `live-tip-guard-hist-r67.txt`, `live-tip-revmode-r67.txt`);
  additivity `raw_old_only=0` on every landed pair (receipts
  `additivity-sources-r67.txt`, `additivity-logscorecard-r67.txt`,
  `additivity-ledger-r67.txt`); census exit 0 at both ends; registry
  rows 157 → 158; the round-range self-sweep over `7362e15c..436b60c5`
  plus the round's own commits reads findings zero exit 0
  (`tip-self-sweep-r67.txt`).

## Next-round carry

- The liveness manifest now pins five real-history red arms; the remaining
  receipt-family arm without a committed red input is the additivity
  counter (no real-history failure exists to pin — manufacturing one
  would be synthetic); the no-harm guard's RED arm needs a checker
  scratch-slot first (ruled out above).
- The figure-misattribution class (a record attributing a figure to the
  wrong receipt while the figure exists in cited bytes) is now a NAMED,
  disclosed instrument boundary — the natural successor calibration
  instrument, designed against the r59 cheat-family ruling.
- The rekey payment is current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it.
- The guarded probe digest `892a045d…` is unchanged; the probe-arms
  re-run obligation stays attached to any future probe edit.
- considerthese 2026-10-28 proposals 3–5 remain unadopted; proposal 1's
  byte-backing half is already landed (r65) and its semantic
  figure-attribution half is the named boundary above.
- Pre-existing tree oddity, observed not absorbed: the root-level `C:`
  tree. Out of scope again (live-lane tree surgery); recorded for the
  operator.
