# tameshi round 63 — lesson (hyaku, 2026-11-01)

L1 `TameshiR63` (round 63). Base `0b81e8f575627d8de2e3a9cf598d5360c42bfeb6`
(= origin/master; the r62 verifier spot-check landing). Dispatch host: win32
(python 3.13.15, git 2.55.0.windows.3, `core.autocrlf=false` in the user
config, no `.gitattributes` in the lane repo — committed blobs carry
whatever bytes were written). Receipts: `.ufo/evidence/round-63/win-host/` —
they land in the commit(s) following the work commit (receipt-after-subject
ordering, the r61/r62 precedent).

Fresh-start duty: the last three rejected closures (r58, r59, r60 —
`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`) were re-read before
anything was declared; r61 and r62 were admitted, so the fresh-start premise
is stale, but the duty was performed and the standing rulings were honored
(frozen spawning precheck host-infeasible; r60's substitute cross-revision
attribution unmeasured; counter-family extension an operator ruling; Linux
counting commands host-scoped per criterion 118). Ruled out this round, with
reasons: (a) any edit to `tools/coldread-precheck-portable.py` — the guarded
digest `892a045d…` is pinned and any probe edit re-owes the probe-arms
re-run; this round needs no probe change; (b) an UNpriced registry edit —
r62 priced any SOURCES byte change at an 18-section rekey and routed around;
r63 pays that price deliberately (C2), so the record edits ride the payment;
(c) building considerthese 2026-10-28 proposal 1 (receipt-existence linter)
— real, but it would compete with the rekey for round scope; recorded as a
proposal, its cited-receipt-exists core already criterion 108/116 ground.

## Claims

- **C1 (calibration, the lowest scored axis; routed defect RD5; sourced on
  new row S294, opened this round).** The RD5 correction becomes a standing
  convention with an instrument. Before: the r62 report's additivity
  receipts (`comm -23` → 0) measure 80 (LOG.md) and 30 (SCORECARD.md) on
  raw committed bytes — the work commit rewrote the r61 tail blocks LF→CRLF
  (plus one inserted blank line at LOG.md line 2) and the receipt stated no
  normalization (red-before receipt
  `.ufo/evidence/round-63/win-host/red-before/additivity-redbefore.txt`,
  recorded before any r63 content landed). After: `tools/additivity-receipt.py`
  (new) computes append-only receipts on committed bytes with the
  normalization declared — raw AND CR-normalized old-only/new-only counts,
  `eol_rewrite_disclosed`, the verbatim-prefix property (empties dropped on
  BOTH sides: an inserted blank line is an addition, not an alteration),
  append-only judged on the normalized comparison, `--require-raw` for
  contexts that must forbid rewrites; selftest 5/5 with the r62 defect shape
  as a green arm; the r62 pair re-measured by the tool (raw_old_only 79/29,
  norm_cr_old_only 0/0, prefix true, rewrite disclosed, exit 0); the
  SCORECARD erratum is the correction of record. This round's own appends to
  LOG.md / SCORECARD.md / QUALITY.md are binary appends in the file's own
  ending (no pre-existing byte touched), and the receipts-commit run on the
  r63 pair is expected to read `raw_old_only=0 eol_rewrite_disclosed=false`.
- **C2 (operability, verdict-only; capability; routed defects RD6 + the RD4
  registry-note site).** The RD6 proposal lands through the payment it was
  waiting for: QUALITY Criterion 120 appended (a described fix is
  grep-addressable in the shipped bytes, with the counting command in the
  claim), the RD4 wrong count repaired at its registry-note site
  (SOURCES.md "12 words" → "8 tokens", logged old → new in the registry
  note), new row S294 appended — the record edits stale the cold-read
  credit, and the r61 rebind run-book (analyze → union plan → manifest from
  genuine section re-reads → rebind) regenerates fresh input-keyed ledger
  entries with trace receipts, restoring the monitor to `lost=0`. The
  capability row `monitored-record rekey run-book` enters the table (first
  demonstrated round 61 as the batch rekeys; named run-book re-demonstrated
  end to end this round on a QUALITY+SOURCES edit pair).

## Gate

- Sourced row opened this round: **S294** (gitattributes documentation,
  https://git-scm.com/docs/gitattributes, fetched 2026-11-01, HTTP date
  Sun, 01 Nov 2026 14:09:12 GMT; 131,046 B; sha256
  `56f2e80e4afadac4458da6c8e0e952e514eba23a125383eab1931cc6210e9d30`;
  extract `.ufo/evidence/round-63/win-host/sources/s294-gitattributes.html`).
  Located quote (§`text` attribute, "Set" paragraph, fetched-page lines
  2678–2679; 18 words): "Setting the text attribute on a path enables
  end-of-line conversion on checkin and checkout as described above."
  Grounding: C1's convention rests on the premise that line-ending
  conversion is a declared per-path attribute layer, not a property of blob
  bytes — this repo holds no `.gitattributes`
  (`git ls-tree 0b81e8f5 -- .gitattributes` → empty; `git check-attr text
  eol -- LOG.md SCORECARD.md` → unspecified) and `core.autocrlf=false`, so
  committed blobs are verbatim bytes and byte comparisons must declare
  normalization. Duplicate check: `git show 0b81e8f5:corpus/SOURCES.md |
  grep -c gitattributes` → 0 (URL unheld).
- Registry edit logged (CORPUS.md rule 2 in-place fields): the round-61
  note's "the §Output batch framing, 12 words" → "8 tokens" (the r62
  erratum RD4 site; the quote is 8 whitespace-separated tokens, re-verified
  against the live S289 page and the r61 extract this round). Row S294
  appended (153 → 154); no held row's status/recheck/used-by changed.
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (153 rows; 17 W04 + 1 W01, all
  pre-existing; receipt in the round report) and exit 0 at round end
  (receipt lands with the receipts commit; the new S294 row is
  census-clean, and the S293 W04 stands as that rejection's marker).

## Mistakes

1. **A normalization check written asymmetrically disagrees with the truth
   it re-derived (class: normalization-asymmetry-in-instrument; caught
   pre-landing by running the instrument on the real pair).** Evidence: the
   first `prefix_ok` dropped empty lines from the base side only, so the
   first real-pair run printed `verbatim_prefix=false` for LOG.md while the
   CR-stripped empty-dropped content IS a verbatim prefix of the tip (the
   r62 commit inserted one blank line at LOG.md line 2; with empties
   dropped on both sides the prefix holds — re-derived directly from the
   blobs). Captured-by: this round's own pre-landing run of the new tool on
   the r62 pair (output in session; corrected receipt
   `.ufo/evidence/round-63/win-host/additivity/r62-pair.txt` shows
   `verbatim_prefix=true` after the fix). Fix: empties dropped on both
   sides, the property's definition written into the tool's docstring, and
   the red arm set re-run (selftest 5/5 after the fix). The practice this
   mines: a new instrument's first run against the REAL data it was built
   for is part of building it — the disagreement was the finding, not a
   failure.
2. **The instrument's first selftest failed on a bytes/str API slip before
   it passed (class: instrument-first-run-shakeout).** Evidence: `body` was
   a `str` and the ARM-ALTER/ARM-DELETE builders called `bytes.replace`;
   also the first CLI wiring made `--selftest` demand the measurement
   arguments. Captured-by: the selftest run (TypeError traceback + argparse
   exit 2). Fix: both corrected; the shipped selftest passes 5/5. Recorded
   because "the tool passed on the first try" is the claim a reader would
   otherwise assume, and the shakeout is part of the receipt trail.

3. **A directory path is a silent no-op in the plumbing helper, and a
   backslash glob path mangles into nested tree names (class:
   commit-plumbing-path-discipline; caught by the pre-landing rehearsal).**
   Evidence: the rehearsal's first rekey commit passed
   `.ufo/evidence/round-63/rekey/traces` (a directory) to treecommit — not
   an isfile, so it no-op'd; the second attempt built relative paths from
   Windows backslash globs (`f.rsplit('/', 1)[1]` on a path with no `/`
   yields the whole string), landing the 13 traces under a mangled
   `traces/traces/...` tree. Both surfaced as `trace-missing:` in the
   precheck's credit rule (a trace named by an entry must exist as a blob
   at the measured rev) with credited stuck at 51/64 across two commits.
   Captured-by: the scratch-clone rehearsal receipts (clone revs
   `9b3d0644`, `a46cb113`, `15750f66` — credited 51/64 at all three)
   versus `f0eefec9` (64/64 after the file-path fix). Fix: the run-book
   commits trace receipts one file path each, forward slashes,
   `os.path.relpath`-derived; the live rekey commits carry the traces
   individually.

4. **The RD5 defect class recurred in this round's own amendment script
   (class: universal-newlines-rewrite; caught by the diff-stat review
   before push).** Evidence: the pre-commit amendment that sharpened the
   planned block's guard wording opened SCORECARD.md in text mode without
   `newline=''` on the read side, so every CRLF became LF on the
   byte-identical-content write back — commit `8616d47`'s diff-stat shows
   SCORECARD.md 3202 insertions / 3131 deletions (the whole file), exactly
   the RD5 rewrite shape the round's C1 exists to disclose. Captured-by:
   the round's own landing review (the `git diff --stat` line; the
   additivity instrument's `eol_rewrite_disclosed` would have flagged it).
   Fix: byte-level restoration before anything was pushed (`b'
' ->
   b'
'` over a verified CR-free file; content re-verified against the
   base: verbatim prefix true, raw_old_only 0), the restored bytes land
   with the rekey commit, and this lesson records it. The practice this
   mines: every record-file write in this lane is a BINARY operation or it
   is a rewrite; text-mode convenience is the RD5 class.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question (`.ufo/l0-questions.md`, tameshi | round-60, option
  (b)) stands unanswered — an L1-only round, disclosed here.
- The C2 rekey ran through the r61 machinery re-driven at this round's
  bytes: analyze (projected stale set), union plan, manifest authored from
  this round's genuine section re-reads with patterns dry-run against the
  pin revision's git objects, rebind (section + input re-reads, per-section
  trace receipts, fresh input-keyed ledger entries), monitor re-run. A
  scratch-clone rehearsal (content-identical commits via the same plumbing
  helper) preceded the live run: it fixed the stale set (13 sections),
  validated the rebind end to end (64/64 restored at rehearsal tip
  `f0eefec9`), validated the receipts-commit safety (SCORECARD/LOG appends
  after the rekey keep `lost=0` in both floor modes), and produced mistake
  3; the live run is the receipted one.
- SOURCES.md is deliberately edited in place at exactly two sites (the new
  table row after S293, the "12 words" label repair, the round note at the
  tail); LOG.md/SCORECARD.md/QUALITY.md are binary appends only. The
  additivity practice check covers the append-only files (LOG.md,
  SCORECARD.md, QUALITY.md, the new lesson); SOURCES.md is a rule-2
  in-place-editable registry, out of the append-only convention's scope by
  its own contract.

## Verdicts

- **C1, C2 — receipts land in the commit(s) following this lesson's work
  commit** (receipt-after-subject ordering). Expected receipts, pinned
  here pre-data: `ADDITIVITY_SELFTEST: 5/5 pass` exit 0; the r62 pair
  measured `raw_old_only=79/29 norm_cr_old_only=0/0 verbatim_prefix=true
  eol_rewrite_disclosed=true` exit 0; the r63 pair (head → work commit)
  measured `raw_old_only=0 eol_rewrite_disclosed=false` on the append-only
  files; the precheck at the work commit RED with `input-drift:corpus/QUALITY.md`
  / `input-drift:corpus/SOURCES.md` on the stale set, then `lost=0 ok`
  exit 0 at the post-rekey tip.

## Next-round carry

- The `tameshi-additivity-receipt-v1` receipt is the standing form for
  append-only claims on line-ending-sensitive record files; any round that
  rewrites endings in an append-only file should show
  `eol_rewrite_disclosed=true` with the rewrite priced, not a bare "0".
- The guarded probe digest `892a045d…` is unchanged this round; the
  probe-arms re-run obligation stays attached to any future probe edit.
- The rekey payment is again current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it. The
  run-book (analyze → union → manifest → rebind → monitor) is scripted and
  re-runnable; a next rekey should reuse it rather than re-derive.
- considerthese 2026-10-28 proposal 1 (receipt-existence linter) remains
  the top unadopted proposal; criterion 120 (landed this round) covers its
  counting-command half for fix claims, not its cited-receipt-exists half.
