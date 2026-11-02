# tameshi round 66 — lesson (hyaku, 2026-11-01)

L1 `TameshiR66` (round 66). Base `469cde0fbfc9862493caba35016d5d6f6af98894`
(= origin/master; the r65 non-author closure landing `ced05ce1`'s spot-check
commit). Dispatch host: win32 (python 3.13.15 native `python`; MS Store
`python3` stub; git 2.55.0.windows.3; `core.autocrlf=false` in the lane
repo). Receipts: `.ufo/evidence/round-66/win-host/` — they land in the
commit(s) following the work commit (receipt-after-subject ordering, the
r61–r65 precedent), and per this round's C1 every commit message names only
receipt bytes that commit carries. A `--no-checkout` scratch clone plus a
plumbing-only work repo rehearsed the whole pipeline first (rehearsal work
`1a3b00b5cba4a5ec4ba5777996394ab22364fd44`, rekey `42488eb782d6c5b2ef069e1a010c8d10aecb6df1`
in the scratch repo); the rehearsal receipts it cites live in
`.ufo/evidence/round-66/win-host/rehearsal/`, and the scratch is deleted with
the round.

## Carry-in addressed first (r65 non-author closure, routed defect 1)

The r65 closure routed one defect to round 66: the frozen
`tools/receipt-commit-bind.py` candidates scope is blind to names of paths
that are added nowhere in the swept range — its sweep over
`7d7f9ca8..87e95597` read `named=0 findings=0` exit 0 on the range whose tip
commit `87e95597` is EMPTY while naming four receipts (the vacuous pass,
receipted at `.ufo/evidence/round-65/win-host/live-bind-erratum-sweep.txt`;
lesson mistake 5). Per the frozen-instrument discipline the fix was NOT
landed post-data in r65; it is this round's C1, declared frozen pre-data,
with the red-before (the `87e95597` case must flip from vacuous pass to
flagged) and the green-after (this round's own range sweeps clean). The
other routed items are standing, not round work: the L2 floor has no
dispatch surface on this host (the r60 L0 question at the fleet root stands
unanswered — an L1-only round, disclosed), and the SHONEN `[x]` marks remain
operator-owned.

## Fresh-start duty

The prompt's fresh-start block lists r58/r59/r60 (the last REJECTED
closures). They were re-read before anything was declared
(`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The premise is
stale — r61, r62, r63, r64 and r65 were all admitted — but the duty was
performed and each closure's standing ruling is honored this round:
r58's — certification needs positive controls that actually bind, and a
refused deciding run is the honest outcome (this round's instruments have
real-history red arms, not only synthetic ones); r59's — a counter must
discriminate a cheat family (the new liveness checker's selftest has
explicit live-row and dead-row arms, and its dead-arm demo is the landed
real defect shape, not a synthetic strawman); r60's — a round's no-harm
guard must run ON this host at the revision pair it claims (the portable
precheck, worktree sha256 `892a045d…`, ran at every measured revision
below; RED + green + rev mode all on this host).

Ruled out this round, with reasons: (a) any edit to
`tools/coldread-precheck-portable.py` — the guarded digest is pinned
(`892a045d…`) and any probe edit re-owes the probe-arms re-run; this round
needs no probe change; (b) SKILL.md / QUALITY.md / README.md / PROVINCE.md
content edits — each extends the rekey payment beyond the one SOURCES edit
the sourced claim requires (measured pin sets from r64: 9 SKILL / 6 QUALITY /
7 README / 13 SOURCES, QUALITY ⊂ SOURCES → this round pays exactly one
rekey); (c) a freshness-axis move — the r45 freshness counter is a frozen
Linux-host shape (`python3`, round-45 wave seat outputs in its predicate)
and reviving it is operator-priced future work, not smuggled into this
round; (d) a depth-axis move — depth is capped at 10 (r51), no room to move;
(e) the whole-history receipt sweep (rounds 1–62) — scoped, unpriced future
work; (f) adopting MORE considerthese proposals — at most one per round;
2026-10-28 proposal 2 (counter-arm liveness) is this round's one adoption,
proposals 3–5 stay unadopted; (g) the root-level `C:` tree oddity — live-lane
tree surgery, priced out since r65.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration, the lowest scored axis at 8; sourced on new row S297,
  opened this round; the r65 closure's routed defect 1).** The bind sweep's
  candidates scope stops being range-added-only. `tools/receipt-commit-bind.py`
  (the checker blob changes only this round, per the routing) gains two arms
  over every commit in the range: arm 2 — every full `.ufo/evidence/…` or
  `tools/…` span extracted from a commit message must resolve at that commit
  via `git cat-file -e <commit>:<path>` (S289's `-e` semantics, S091's
  `<commit>:<path>` spelling); arm 3 — every file-like token (basename with
  a disclosed receipt/tool extension) in a commit message must resolve to a
  path anywhere in that commit's tree, so naming content the tree does not
  carry is the flagged defect whether or not the range ever adds it. Arm 1
  (the frozen range-added rule) is unchanged, including its per-path
  first-hit counting. Selftest 4/4 → 6/6 (new arms: the nowhere-named red =
  the `87e95597` shape; the span-absent red). Fail-closed empty-range guard
  now requires no evidence adds AND no spans AND no tokens.
  Before (measured in rehearsal at the frozen bytes, receipt
  `rehearsal/reh-bind-frozen-vacuous.txt`): sweep `7d7f9ca8..87e95597` →
  `named=0 findings=0` exit 0 — the vacuous pass on a genuinely defective
  range. After (expected, forecast from rehearsal): selftest 6/6 exit 0;
  the same range → `findings=4` exit 1 naming exactly the four `87e95597`
  receipts (`names-unknown`), all honest commits reading `BIND_OK`; the r64
  range `d0baf616..c7d28b19` → still exactly 1 BIND_DEFECT (`6876d746`) —
  the frozen discriminator does not regress; the r65 clean range
  `7d7f9ca8..6db7e2fc` → `findings=0` exit 0; the full r65 range
  `7d7f9ca8..ced05ce1` → `named=9 carried=5 findings=8` exit 1 (arm 1's
  four + arm 3's four, all at `87e95597`); this round's own range →
  `findings=0` exit 0 (green-after).
- **C2 (operability, verdict-only; capability; adopts considerthese
  2026-10-28 proposal 2 — counter-arm liveness — the ONE assimilation this
  round).** New `tools/arm-liveness.py` + `tools/arm-liveness.json` (schema
  `tameshi-arm-liveness-v1`): every declared red arm of the receipt-family
  counters carries one committed input that must MOVE its tally — the
  checker extracts the instrument from git objects at the row's pinned
  revision (never a worktree), runs it `python -I` against the committed
  input, and marks the row `ARM_LIVE` only when the exit matches, the parsed
  tally ≥ expect_min and > baseline; otherwise `ARM_DEAD`. Manifest rows
  (scope disclosed in the file): bind r64-range red (findings≥1 at
  `d0baf616..c7d28b19`), quoted-line r64-records red (missing≥4 at the rekey
  tip), receipt-exists red (the r64 lesson at its own declaration commit
  `33cb4b0d` cites receipts that had not landed — missing≥5). Instrument
  revisions pinned at `469cde0f` so rows stay reproducible across later tool
  edits — the rows are C1-independent and the claim is causally separable.
  Selftest 4/4 hermetic (live row, dead row, vacuous manifest, usage).
  Before: no instrument (`git ls-tree 469cde0f tools/ | grep -c
  arm-liveness` → 0) and the r65 blind spot was found by inspection, not by
  any standing check. After (expected, forecast from rehearsal): selftest
  `ARM_LIVENESS_SELFTEST: 4/4 pass` exit 0; the standing manifest sweep →
  `rows=3 live=3 dead=0` exit 0; the dead-arm demo — a scratch manifest row
  pinning the FROZEN bind tool over `7d7f9ca8..87e95597` expecting
  findings≥1 reads `ARM_DEAD … findings=0` exit 1 (the r65 blind spot
  caught mechanically), and the same row re-pinned to this round's tool
  reads `ARM_LIVE … findings=4` exit 0.

Causally separable: C1's arms need no part of C2 and vice versa (C2's
standing rows run green with or without C1 — its instruments are pinned at
the pre-round tip). Each lands as its own commit with its own demonstration.

## Gate

- Sourced row opened this round: **S297** (Git git-diff-tree documentation,
  https://git-scm.com/docs/git-diff-tree, fetched 2026-11-01, HTTP date
  Mon, 02 Nov 2026 02:22:07 GMT; 256,810 B; sha256
  `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`;
  extract `.ufo/evidence/round-66/win-host/sources/s297-git-diff-tree.html`).
  Located quote (§OPTIONS, `--diff-filter`, fetched-page line 4016; 17
  words): "Select only files that are Added ( A ), Copied ( C ), Deleted
  ( D ), Modified ( M ), Renamed ( R )". Grounding: the frozen bind rule's
  candidates ARE diff-tree's range-added paths — the page is the authority
  for what the frozen scope could see (paths ADDED in base..tip) and
  therefore for the blind spot the round-66 arms close (a message naming a
  receipt the range never adds was invisible to `--diff-filter=A`).
  Duplicate check: `grep -c git-diff-tree corpus/SOURCES.md` → 0 at
  `469cde0f` (URL unheld; S289/S293 hold the git-cat-file page, S294 the
  gitattributes page, S296 the git-commit page — different pages).
- Rejections: NONE this round — the one source opened (S297) was adopted as
  C1's claim ground; no row was opened and refused. Price-outs, with
  reasons: the gitrevisions page (the `<commit>:<path>` object spelling) is
  already held as S091, so a row would be a within-scope duplicate — the
  r61 S293/S289 precedent applies and no new row was staged; staging a
  fetch to manufacture a rejection would be dishonest. The standing
  rejection S293 (within-scope duplicate of S289) keeps its W04 census
  marker.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (receipt `win-host/census-start.txt`;
  156 rows; 17 W04 + 1 W01, all pre-existing) and exit 0 at round end
  (receipt `.ufo/evidence/round-66/win-host/census-end.txt`; 157 rows; the
  new S297 row census-clean, no new warning; the same 17 W04 + 1 W01 set).

## Mistakes

1. **The liveness checker passed a relative `--repo` to instruments whose
   cwd it had just set to that repo (class: relative-repo-under-instrument-cwd;
   captured-by: the dead-arm demo pair in the scratch rehearsal — both rows
   read ARM_DEAD `tally=unparsed exit=2`, a setup exit where the frozen row
   owed `findings=0`).** Evidence: the first rehearsal run of the demo pair
   (`reh-demo-dead.txt` before the fix) shows `exit=2` — the extracted
   instrument's `git -C rehwork` resolved from inside `rehwork` itself, so
   every spawn failed and the checker nearly recorded a false "dead" verdict
   for a live arm. Fix: the checker resolves the repo path to absolute
   before use (`Path(a.repo).resolve()`); after the fix the pair reads the
   honest values (`findings=0` dead / `findings=4` live). The practice this
   mines: a checker that launches sub-instruments must pin ABSOLUTE paths —
   a demo that cannot fail is a probe, and this demo failed correctly.
2. **The scratch tree-builder replaced entries but silently dropped
   additions (class: rewrite-only-tree-builder; captured-by: `git
   diff-tree -r --name-status <parent> <work-commit>` before any guard
   run — the new tool files were missing from the rehearsal commit).**
   Evidence: the first rehearsal work commit `54d1d64e` shows only
   `M corpus/SOURCES.md` + `M tools/receipt-commit-bind.py` — the two NEW
   files (arm-liveness.py/.json) were absent because the builder only
   overrode entries already present in the parent listing. Fix: the builder
   appends parent-absent overrides (and deeper new subtrees) before
   mktree; the rebuilt work commit `1a3b00b5` diffs exactly
   `M SOURCES, A arm-liveness.json, A arm-liveness.py, M bind`. No live
   commit was affected; the miss was caught by inspecting the diff-tree
   before running anything against the commit.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question stands unanswered — an L1-only round, disclosed.
- The scratch rehearsal (plumbing-only; the lane index never touched):
  work commit `1a3b00b5…` (SOURCES S297 draft + the r66 bind tool +
  arm-liveness) → RED `lost=13` at floor `469cde0f` (cand_credited=51,
  exit 1; the 13 headings byte-equal IN ORDER to the r65 rehearsal
  manifest's — miss = 0 if the live work commit reproduces it; receipts
  `rehearsal/reh-red.out|.err`) → rebind `r66-batch-1` (REBIND OK
  sections=13 entries_added=13 ledger_before=719; machinery = the r65
  as-run rebind re-driven at this round's constants, diff receipt
  `rehearsal/reh-make-rebind-r66.diff`, 7 changed lines across 5 sites,
  constants only) → rekey commit `42488eb7…` → green `lost=0 ok` exit 0 at
  BOTH floors (round `469cde0f` 64 → 64, historic `8b0042bd` 46 → 64) +
  rev mode `credited=64/64` probe 20/20 (receipts `rehearsal/reh-green.out`,
  `reh-green-hist.out`, `reh-revmode.out`); additivity `raw_old_only=0` on
  both rehearsal pairs (SOURCES mid-file insertion `verbatim_prefix=false`
  disclosed, ledger `verbatim_prefix=false` disclosed;
  `reh-additivity-sources.txt`, `reh-additivity-ledger.txt`). The frozen
  tool's vacuous pass (`reh-bind-frozen-vacuous.txt`) and the demo pair
  (`reh-demo-dead.txt`, `reh-demo-live.txt`) were also rehearsed. The
  scratch is deleted with the round.
- The live run re-executes each stage at the live revisions; its receipts
  land with the commits per the receipt-after-subject ordering, and every
  commit message names only receipts that commit carries (C1's own rule).
  The run-book ends with a self-sweep of the round range AND a
  carries-what-it-names check of the tip commit (`git diff-tree` before
  push) — the r65 lesson's mined practice, applied.
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); SOURCES.md (LF) carries the row insertion and the tail
  note (pure 2-line insertion, old-lines-lost = 0). No other monitored file
  changes (PROVINCE.md, SKILL.md, README.md, corpus/QUALITY.md,
  tools/registry.json, the guarded probe, SHONEN.md, the leg ledger — all
  byte-identical base → tip; the no-harm story is SOURCES-only).

## Verdicts

- **C1, C2 — receipts land in the commit(s) following this lesson's work
  commits** (receipt-after-subject ordering). Expected receipts, pinned
  here pre-data: `RECEIPT_COMMIT_BIND_SELFTEST: 6/6 pass` exit 0;
  `ARM_LIVENESS_SELFTEST: 4/4 pass` exit 0; the frozen-tool vacuous
  receipt → `findings=0` exit 0 over `7d7f9ca8..87e95597`; the r66-tool
  sweep over the same range → `findings=4` exit 1 with the four
  `names-unknown` defects at `87e95597`; the r64-range sweep → `findings=1`
  exit 1 naming `6876d746` only; the r65 clean range → `findings=0`
  exit 0; the full r65 range → `findings=8` exit 1 (4+4, all at
  `87e95597`); this round's own range → `findings=0` exit 0; the liveness
  standing sweep → `rows=3 live=3 dead=0` exit 0; the demo pair →
  `ARM_DEAD findings=0` exit 1 (frozen pin) / `ARM_LIVE findings=4` exit 0
  (r66 pin); the guard RED at the live work commit with `lost=13` matching
  the forecast (miss = 0 if identical), then `lost=0 ok` exit 0 at both
  floors at the rekey commit and at the receipts tip, rev mode 64/64;
  additivity `raw_old_only=0` on every landed pair; census exit 0 at both
  ends; the capability row `counter-arm liveness check` enters the
  SCORECARD capabilities table.

## Next-round carry

- The bind checker's candidates scope is now message-complete: any future
  commit naming a receipt it does not carry is flagged by the sweep over
  its own range — the r63/r64/r65 record-discipline claims can cite a
  standing self-sweep.
- The liveness manifest is scoped to the receipt-family red arms; the
  remaining registry instruments' arms enter as successor rounds pin and
  verify their inputs (the manifest's note carries the scope flip).
- The rekey payment is again current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it
  (measured pin sets unchanged: 9 SKILL / 6 QUALITY / 7 README /
  13 SOURCES, QUALITY ⊂ SOURCES).
- The guarded probe digest `892a045d…` is unchanged this round; the
  probe-arms re-run obligation stays attached to any future probe edit.
- considerthese 2026-10-28 proposals 3–5 remain unadopted (at most one per
  round); proposal 2 is now adopted.
- Pre-existing tree oddity, observed not absorbed: the root-level `C:` tree
  (blob-sha identical from before r58). Out of scope again this round
  (live-lane tree surgery); recorded for the operator.


## Mistake 3 and the K1 correction (appended at the correction commit,
## 2026-11-01 — self-caught by diff-tree inspection immediately after the
## declaration commit, before any further stage ran)

3. **The declaration commit's pathspec list silently lost 21 of its 27
   paths (class: shell-var-pathspec-silent-noop; captured-by: `git
   diff-tree -r --name-status 469cde0f <K1>` run immediately after the
   commit — the mined r65 practice — which showed only the 6 literal
   paths landed while every `$R`-expanded rehearsal-receipt pathspec
   no-op'd).** Evidence: `b459653c49f262cc9a144d798410bfcb928e8758`
   (the declaration commit) carries census-start.txt, the S297 extract +
   headers, LOG, SCORECARD and the lesson — and NO rehearsal receipts —
   while its message says "rehearsal receipts (RED lost=13 miss=0, ...)".
   The r65 empty-commit class (a commit describing receipt content its
   tree does not carry), one commit after the round that fixed the
   instrument for it — caught this time by the practice mistake 4 mined,
   before push-dependent stages ran. Root cause observable: the
   `$R`-expanded pathspecs behaved as unset-variable expansions (leading
   `/` stripped by the helper, then a missing-file no-op REMOVAL — the
   helper's documented missing-on-disk-removes semantics), so the commit
   was built without them and no error surfaced; the same expansion
   verified correct in isolated test calls immediately after, so the
   trigger is the invocation shell of that one call, recorded here as
   undetermined-local-shell. The run-book practice mined: treecommit
   pathspec lists are written as LITERAL paths, never shell variables,
   and EVERY treecommit landing is verified with `git diff-tree -r
   --name-status <parent> <new>` before the next stage. Fix: the
   correction commit (this one) lands the 21 named receipt bytes; the
   round's receipts then land at the stages that produce them. The
   mechanical sweep is NOT tripped by this message (it names no file
   tokens — the record-discipline rule it checks is basename-naming, not
   prose description), and the record-level duty is met by this
   correction landing the described bytes.
