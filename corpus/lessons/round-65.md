# tameshi round 65 — lesson (hyaku, 2026-11-01)

L1 `TameshiR65` (round 65). Base `7d7f9ca8044239ef5e99a6b0e007d1a7ac671ac2`
(= origin/master; the r64 verifier spot-check landing). Dispatch host: win32
(python 3.13.15 native `python`; MS Store `python3` stub; git
2.55.0.windows.3; `core.autocrlf=false` in the lane repo, no
`.gitattributes` — committed blobs carry whatever bytes were written).
Receipts: `.ufo/evidence/round-65/win-host/` — they land in the commit(s)
following the work commit (receipt-after-subject ordering, the r61–r64
precedent). A `--no-checkout` scratch clone rehearsed the whole pipeline
first (rehearsal revs `77d43995…` work / `92472f92…` rekey / `5535367d…`
traces re-landed); the rehearsal receipts it cites live in
`.ufo/evidence/round-65/win-host/rehearsal/`, and the clone is deleted with
the round's scratch.

## Carry-in addressed first (r64 non-author closure, all status-neutral)

1. **The empty tail commit `6876d746`.** Verified this round before any
   writing: `git diff-tree --stat 6876d746` prints nothing — the commit is
   EMPTY (its tree equals its parent `be76552d`), while its subject names
   receipt content ("post-landing tip-confirmation receipt (guard both
   floors, additivity C->D, self-sweep …)") that landed only in the
   successor `c7d28b19` (tip-confirmation.txt, +5 lines). Correction note of
   record: `.ufo/evidence/round-65/win-host/correction-note-r64-tail-commits.txt`
   — an empty commit carries no content; the receipt bytes each named run
   produced live where they landed, and this round states the convention
   that closes the class (below).
2. **`tip-confirmation.txt` carried only the round-floor line.** The r64
   subject claimed "guard both floors" but the landed file had only the
   `floor=d0baf616bb8a` line. Fixed by EXECUTION, not renaming: the guard was
   re-run this round at the exact revision pair the r64 file names —
   `python -I tools/coldread-precheck-portable.py --repo . --floor
   8b0042bde0ca… --cand 6876d7460c75… --work WORK` →
   `COLDREAD_PRECHECK floor=8b0042bde0ca floor_credited=46
   cand=6876d7460c75 cand_credited=64 lost=0 ok` + EQUIVALENCE 20/20, exit 0
   (receipt `.ufo/evidence/round-65/win-host/tipfix-hist-floor.txt`) — and
   the historic-floor line is appended to `.ufo/evidence/round-64/win-host/tip-confirmation.txt`
   under a dated header naming where the run's receipt lives. The r64
   "both floors" claim at that tip is now complete in bytes.
3. **`live-B-red.txt` truncated the LOST list.** The .txt lists the first 5
   of the 13 LOST headings; the complete set was already authoritative in
   `live-B-red.json` (counts.lost = 13, verified by the r64 closure). A
   dated receipt-completeness note is appended to the .txt (ASCII, binary
   append — the file carries cp1252-encoded em-dashes from its r64 writer)
   naming the JSON as the complete receipt; nothing in the .txt contradicts
   the JSON.

**The convention that closes defect 1's class, stated of record this round:**
a commit whose message names receipt content must carry those receipt bytes;
receipts land in the commit that names them; an empty commit carries no
content and is never a receipt carrier. The convention is mechanically
checked by C1's instrument below, whose sweep of the r64 round range flags
exactly `6876d746` (one BIND_DEFECT, receipt
`.ufo/evidence/round-65/win-host/live-bind-r64-range.txt`).

## Fresh-start duty

The contract's fresh-start block lists the last three REJECTED closures
(r58, r59, r60 verifier spot-checks). They were re-read before anything was
declared (`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`). The
premise is stale — r61, r62, r63 and r64 were all admitted — but the duty
was performed and each closure's standing ruling is honored this round:
r58's — certification needs positive controls that actually bind, and a
refused deciding run is the honest outcome (this round's C1 sweep has a
real-history red arm, not just synthetic ones); r59's — a counter must
discriminate a cheat family (criterion 111; both instruments' red arms are
proven against committed defective records plus synthetic always-pass
refusals); r60's — a round's no-harm guard must run ON this host at the
revision pair it claims (the portable precheck, digest `892a045d…`, ran at
every measured revision below; forecast + RED + green all on this host).

Ruled out this round, with reasons: (a) any edit to
`tools/coldread-precheck-portable.py` — the guarded digest is pinned
(`892a045d…`) and any probe edit re-owes the probe-arms re-run; this round
needs no probe change (the machinery copies in scratch are byte-identical,
digest verified); (b) the standing r59–r62 rulings — frozen spawning
precheck host-infeasible, counter-family extension an operator ruling,
Linux-only counting commands host-scoped; (c) SKILL.md / QUALITY.md /
README.md / PROVINCE.md content edits — each extends the rekey payment
beyond the one SOURCES edit the sourced claim requires (measured pin sets
from r64: 9 SKILL / 6 QUALITY / 7 README / 13 SOURCES, QUALITY ⊂ SOURCES →
this round pays exactly one rekey); (d) the whole-history receipt sweep
(rounds 1–63) — scoped, unpriced future work, not smuggled; (e) adopting
MORE considerthese proposals — at most one per round; 2026-10-28 proposal 1's
byte-for-byte quoted-line half is this round's one adoption, proposals 2–5
stay unadopted.

## Claims (declared frozen pre-data in the SCORECARD planned block)

- **C1 (calibration, the lowest scored axis at 8; sourced on new row S296,
  opened this round; closes the r64 closure's routed defect 1 class).** The
  receipt-commit binding convention becomes mechanically checkable. New
  `tools/receipt-commit-bind.py`: for a commit range, every path ADDED under
  `.ufo/evidence/` whose basename (with, or — 8+ chars — without extension,
  delimited-token match, rule disclosed in the tool header) is named in a
  commit's message must exist in that commit's tree (`git ls-tree -r`,
  git objects only); violations are listed as BIND_DEFECT with exit 1; a
  range adding no evidence file exits 2 (fail-closed: no vacuous pass);
  selftest 4/4 (synthetic empty-commit-naming-a-receipt arm = the
  discrimination arm; carrying arm; vacuous-guard arm; usage arm). Before:
  the class exists undetected in history — `git cat-file -e
  6876d7460c75…:.ufo/evidence/round-64/win-host/tip-confirmation.txt` fails
  while `git log -1 --format=%B 6876d7460c75… | grep -c tip-confirmation`
  is 1 — and no instrument exists (`git ls-tree 7d7f9ca8 tools/` has no
  receipt-commit-bind). After: the sweep over the r64 round range
  `d0baf616..c7d28b19` reports exactly one BIND_DEFECT (`6876d746` naming
  `tip-confirmation`) — the historical defect discriminated — and the sweep
  over this round's own range reports zero findings exit 0, because this
  round's commit messages name only receipts they carry. Provenance ground:
  S296 — git's own words that recording a commit with the same tree as its
  parent is a mistake.
- **C2 (operability, verdict-only; capability; adopts considerthese
  2026-10-28 proposal 1's byte-for-byte quoted-line half — the ONE
  assimilation this round; its cited-receipt-exists half landed r64).** New
  `tools/quoted-line-exists.py`: quoted counter lines in a record must be
  byte-backed by committed receipt bytes. Document sweep: verdict-shaped
  backtick spans (shape rules disclosed in the tool header: lead token up
  to first '=', counter shape `field=…` or `TOKEN: value` with uppercase
  lead, ≥12 chars, no ellipsis/placeholder chars, command names denied) must
  appear as byte substrings of at least one receipt the record itself cites
  (full `.ufo/`+`tools/` paths; directory cites expand; bare basenames
  resolve by unique-basename match; fleet-root surface cites resolve via a
  named `--extra-root` filesystem check — the r64 cross-surface class).
  Explicit mode: one quote against one receipt at a pinned rev. Exit map
  0/1/2 with a fail-closed empty-document guard. Selftest 4/4 hermetic.
  Demonstration on the newest records (r64 lesson + r64 verifier spot-check
  at the round tip): every receipt-backed quote is byte-backed (backed=12)
  and the sweep names 4 unbacked quotes — the finding class the proposal
  wrote it for: records running ahead of their receipts (one verifier
  re-derivation line "SETS MATCH (miss=0 vs forecast confirmed)" is in no
  committed receipt; three are sha-abbreviated quote shapes —
  `cand=1763db52` against the receipt's `cand=1763db52b42c` — not
  byte-substrings). Honest reading: those are findings about the RECORDS'
  quote discipline, not about the underlying runs (each underlying run has a
  committed receipt; the abbreviations were narrative shorthand); they are
  disclosed, not repaired retroactively, and the tool's strict byte-for-byte
  standard is exactly what the proposal asked for. Capability rows
  `commit-message receipt binding sweep` and `quoted-line receipt
  backability` enter the SCORECARD capabilities table.

Causally separable: C1's checker needs no part of C2 and vice versa; each
lands as its own commit with its own demonstration.

## Gate

- Sourced row opened this round: **S296** (Git git-commit documentation,
  https://git-scm.com/docs/git-commit, fetched 2026-11-01, HTTP date Sun,
  01 Nov 2026 21:54:42 GMT; 122,852 B; sha256
  `08e87c56ec9e7609093dd8a63194848c2aa41bdf4a5a532ee258069512b66e07`;
  extract `.ufo/evidence/round-65/win-host/sources/s296-git-commit.html`).
  Located quote (§OPTIONS, `--allow-empty`, fetched-page line 2871; 18
  words): "Usually recording a commit that has the exact same tree as its
  sole parent commit is a mistake". Grounding: C1's whole class is the
  empty commit — message metadata claiming content the tree does not carry;
  git's own documented refusal shape is the convention's ground. Duplicate
  check: `grep -c git-scm.com/docs/git-commit corpus/SOURCES.md` → 0 at
  `7d7f9ca8` (URL unheld; S289/S293 hold the git-cat-file page, S294 the
  gitattributes page — different pages).
- Rejections: NONE this round — the one source opened (S296) was adopted as
  C1's claim ground; no row was opened and refused. Price-outs, with
  reasons: the git-pretty-formats page was considered as a second ground
  (%B subject extraction) and NOT opened — the tool reads `%B` via
  `git show -s --format=%B` whose behavior needs no documentation row to be
  verified (the receipt shows the extraction), so a row would be an
  unused-source row; staging a fetch to manufacture a rejection would be
  dishonest. The standing rejection remains S293 (within-scope duplicate of
  S289; its W04 census warning stands in both census runs).
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (155 rows; 17 W04 + 1 W01, all
  pre-existing, receipt in the round report) and exit 0 at round end
  (receipt `.ufo/evidence/round-65/win-host/census-end.txt`; 156 rows; the
  new S296 row census-clean, no new warning; the same 17 W04 + 1 W01 set).

## Mistakes

1. **treecommit directory-path args are REMOVALS (class:
   dir-path-arg-in-plumbing-commit; captured by the guard going RED with
   `trace-missing:…/traces/section-03.json` after the rekey — fail-closed,
   no bad credit was restored).** Evidence: the first rehearsal rekey commit
   `92472f92` passed `.ufo/evidence/round-65/rekey/traces` (a directory) to
   treecommit; its docs say a path missing on disk is removed, and a
   directory is not a file on disk, so the commit replaced the whole
   subtree with the empty tree (`git ls-tree <rev> -- .ufo/evidence/round-65/`
   → one line, the empty-tree sha `4b825dc6…`). The next guard stayed
   `lost=13 RED` because every fresh entry's trace gate read
   trace-missing. Fix: re-landed all 16 files with explicit file paths
   (`5535367d…`) → guard `lost=0 ok` at both floors. The practice this
   mines: the run-book's "file-path-only commit discipline" is not a style
   rule — a directory arg silently deletes; the lane's helper cannot express
   "add this directory".
2. **A bash sed strip with an unanchored pattern silently produced wrong
   paths (class: sed-strip-anchor-miss; captured by root-tree inspection
   before any live run).** Evidence: the first fix attempt built paths with
   `sed 's|.*/rehearsal/||'` — the clone-relative `ls` output has no
   leading `/rehearsal/`, so nothing was stripped and treecommit built a
   stray `rehearsal/` tree at the repo ROOT (`git ls-tree <rev>` shows it)
   instead of landing the receipt files. Caught by inspecting the resulting
   root tree before running any guard; the branch was reset with
   `update-ref` (CAS) and the commit redone with an anchored
   `sed 's|^rehearsal/||'`. No live commit was affected.
3. **Unbatched git spawns stall the instrument on big unions (class:
   per-spawn-cost-in-instrument; captured by the first tuning run exceeding
   the 120 s shell timeout).** Evidence: the first quoted-line sweep read
   each receipt with one `git show` spawn; the r64 lesson's dir cite
   `.ufo/evidence/round-64/win-host/` expanded the receipt set to 24,265
   files (after the prefix-span rule was fixed) and per-file spawns at
   Windows process cost did not finish. Fix: one `git cat-file --batch`
   process per sweep (the lane's batched-read pattern from
   coldread-precheck-portable.py) — full two-document sweep 3.2 s; plus the
   rule that single-segment prefix spans (`.ufo/`, `tools/` as prose) are
   skipped shapes, not directory cites.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question (`.ufo/l0-questions.md` at the fleet root, tameshi |
  round-60, option (b)) stands unanswered — an L1-only round, disclosed.
- A `--no-checkout` scratch clone rehearsed the whole pipeline before the
  live run: work commit `77d43995…` (SOURCES S296 draft + both tools) → RED
  `lost=13` at floor `7d7f9ca8` (the criterion-110 forecast, measured
  BEFORE the declaration; the 13 headings are exactly the r63/r64 manifest
  set, miss=0; receipts `rehearsal/rehearsal-red.out|.json`) → rekey
  `r65-batch-1` (REBIND OK sections=13 entries_added=13 ledger_before=706;
  machinery = the r64 as-run rebind re-driven at this round's constants,
  diff receipt `rehearsal/make-rebind-r65.diff`, 7 changed lines across 5
  sites, constants only) → green at the round floor AND the historic floor
  `8b0042bd` (46 → 64) at `5535367d…` after the traces were re-landed (see
  mistake 1) — receipts `rehearsal/rehearsal-C-guard.txt`,
  `rehearsal-C-guard-hist.txt`; additivity on both rehearsal pairs
  `raw_old_only=0` (`rehearsal-A-additivity-sources.txt`,
  `rehearsal-C-additivity-ledger.txt`). The clone is deleted with the
  scratch.
- The live run re-executes each stage at the live revisions; its receipts
  land with the commits per the receipt-after-subject ordering, and every
  commit message names only receipts that commit carries (C1's own rule,
  applied to this round's records; the final sweep receipt
  `live-bind-r65-range.txt` proves it for the whole round range).
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); SOURCES.md (LF) carries the row insertion and the tail
  note (pure 2-line insertion, old-lines-lost = 0);
  `.ufo/evidence/round-64/win-host/live-B-red.txt` and
  `tip-confirmation.txt` receive dated ASCII binary appends (growth, not
  change; the original bytes are untouched).

## Verdicts

- **C1, C2 — receipts land in the commit(s) following this lesson's work
  commits** (receipt-after-subject ordering). Expected receipts, pinned
  here pre-data: `RECEIPT_COMMIT_BIND_SELFTEST: 4/4 pass` exit 0;
  `QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass` exit 0; the r64-range sweep →
  `findings=1` exit 1 with the single BIND_DEFECT naming `6876d746`;
  this round's range sweep → `findings=0` exit 0; the quoted-line demo →
  `backed=12 missing=4` exit 1 with all four unbacked quotes named (the
  disclosed finding class above); the guard RED at the live work commit
  with `lost=13` matching the forecast (miss = 0 if identical), then
  `lost=0 ok` exit 0 at both floors at the rekey commit and at the tip;
  additivity `raw_old_only=0` on every landed pair (LOG.md, SCORECARD.md,
  SOURCES.md, ledger); census exit 0 at both ends; capability rows enter
  the SCORECARD capabilities table.

## Next-round carry

- Both instruments are standing: `receipt-commit-bind.py` should sweep the
  round range before any closure claims record discipline;
  `quoted-line-exists.py` makes quote-abbreviation a checkable event — if
  the lane wants sha-prefix shorthand in records, that is a DISCLOSED
  convention change (a rule edit in the tool, with its own receipt), not a
  silent relaxation.
- The r64 spot-check's four unbacked quotes are record findings, disclosed
  this round; a successor round may append a dated annotation to that
  lesson's receipts (growth, not change) if the operator wants them
  marked resolved — not done unilaterally here.
- The rekey payment is again current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it
  (measured pin sets unchanged: 9 SKILL / 6 QUALITY / 7 README /
  13 SOURCES, QUALITY ⊂ SOURCES).
- The guarded probe digest `892a045d…` is unchanged this round; the
  probe-arms re-run obligation stays attached to any future probe edit.
- considerthese 2026-10-28 proposals 2–5 remain unadopted (at most one per
  round); proposal 1 is now fully adopted (both halves).
- Pre-existing tree oddity, observed not absorbed: the lane tree carries a
  root-level `C:` tree (blob-sha identical from before r58; an old-host
  NTFS accident). Out of scope to remove this round (tree surgery on the
  live lane); recorded here so a future round or the operator can price it.


## Mistakes 4 and 5 (appended at the receipts tip, 2026-11-01 — found by
## inspection before closure; both fail-closed or disclosed, none silent)

4. **The tip-receipts commit repeated the exact class C1 checks (class:
   receipts-named-not-carried; captured-by: root-tree/diff inspection
   before closure).** Evidence: K7 `87e955975ff6f4fcfcc953ed8fe93ea37804b1df`
   ("round 65 tip receipts…") names live-tip-guard.txt,
   live-tip-guard-hist.txt, live-bind-full-range.txt and
   live-additivity-final.txt but is an EMPTY commit — `git diff-tree
   5740805d 87e95597` prints nothing; the four receipt files were written
   to the scratch and never copied into the lane worktree before the
   commit, so treecommit saw every path missing-on-disk and changed
   nothing. The r64 routed defect's shape, reproduced by the very round
   that shipped the checker for it — and NOT caught by the frozen sweep,
   which is mistake 5. Fix: this commit lands the four named receipt
   bytes plus the sweep receipt; the run-book practice mined: the run-book
   must END with a self-sweep AND a carries-what-it-names check of its own
   tip commit — a commit that names receipts verifies with
   `git diff-tree <parent> <commit>` before pushing.
5. **The frozen sweep rule has a blind spot for names of paths that exist
   nowhere in the range (class: candidates-scope-blind-spot; captured-by:
   the K7 incident — the sweep over `7d7f9ca8..87e95597` reads
   `named=0 findings=0` exit 0 because live-tip-guard.txt was never ADDED
   in the range, so the naming check never fired; receipt
   `.ufo/evidence/round-65/win-host/live-bind-erratum-sweep.txt` records
   that vacuous pass).** Evidence: the frozen rule's candidates are paths
   ADDED in the range; a commit naming an evidence path that exists
   nowhere in the range produces `named=0` — the checker's own vacuous
   pass on a genuinely defective range. Fix, routed to round 66 as the
   checker's next arm (NOT landed post-data this round — the counter is
   not edited after its demos ran): also extract full `.ufo/evidence/…`
   and `tools/…` path spans from each commit message and require
   `git cat-file -e <commit>:<path>` for each, so naming a path that
   exists nowhere is itself the flagged defect. The frozen demonstrations
   stand as measured (the r64-range red arm, where the named file WAS
   range-added; the r65-range clean sweep); this erratum names their
   scope.
