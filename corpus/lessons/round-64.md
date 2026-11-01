# tameshi round 64 — lesson (hyaku, 2026-11-01)

L1 `TameshiR64` (round 64). Base `d0baf616bb8a9fc1be6394e370e0f30a952470af`
(= origin/master; the r63 verifier spot-check landing). Dispatch host: win32
(python 3.13.15, git 2.55.0.windows.3, `core.autocrlf=false`, no
`.gitattributes` — committed blobs carry whatever bytes were written).
Receipts: `.ufo/evidence/round-64/win-host/` — they land in the commit(s)
following the work commit (receipt-after-subject ordering, the r61–r63
precedent). A `--no-checkout` scratch clone (content-identical, the same
plumbing helper) rehearsed the whole pipeline first; the rehearsal receipts
it cites live in `.ufo/evidence/round-64/win-host/rehearsal/`, and the clone
is deleted with the round's scratch.

Carry-in addressed first, as routed: the r63 non-author closure left two
status-neutral observations. (1) `rekey_round: 61` labels the 13 r63-created
ledger entries — root cause located this round: the field is a hardcoded
constant in the as-run rebind tool (mistake 4); the precision correction is
C1's `rekey_batch` field, landed in the data (49 entries), in the convention
of record, and in the shipped r64 machinery. (2) no fresh Gate reject row —
this round's `## Gate` states its reject sample explicitly.

Fresh-start duty: the last three rejected closures (r58, r59, r60 —
`corpus/lessons/round-{58,59,60}-verifier-spotcheck.md`) were re-read before
anything was declared. The premise is stale (r61, r62 and r63 were all
admitted), but the duty was performed and the standing rulings honored:
r58's — certification needs positive controls that actually bind, and a
refused deciding run is the honest outcome; r59's — a counter must
discriminate a cheat family, not a do-nothing control (criterion 111); r60's
— a round's no-harm guard must be verified ON this host at the same revision
pair it claims (the portable precheck, digest `892a045d…`, runs in seconds
here and ran at every measured rev below). Ruled out this round, with
reasons: (a) any edit to `tools/coldread-precheck-portable.py` — the guarded
digest is pinned and any probe edit re-owes the probe-arms re-run; this round
needs no probe change (the round-64 win-host copy is byte-identical, digest
verified `892a045d…`); (b) the standing r59–r62 rulings — frozen spawning
precheck host-infeasible, counter-family extension an operator ruling, Linux
counting commands host-scoped; (c) SKILL.md / QUALITY.md / README.md /
PROVINCE.md edits — each extends the rekey payment (measured pin sets: 9
sections pin SKILL.md, 6 QUALITY.md, 7 README.md, 13 SOURCES.md; the 6 are a
subset of the 13, so this round pays exactly one rekey for the SOURCES edit);
(d) a full-corpus receipt sweep over every lesson since round 1 — the tool
exists after this round, the deciding demonstration is scoped to the newest
round's records, and a whole-history sweep is future work priced honestly
here rather than a smuggled claim.

## Claims

- **C1 (calibration, the lowest scored axis at 8; sourced on new row S295,
  opened this round; closes the r63 closure's carry-in observation 1).** The
  ledger's run-book batch attribution becomes explicit, addressable, and
  self-recording. Before: the 49 run-book entries carry only
  `rekey_round: 61` across read_revs `19d7e996…` / `0a29e3cf…` /
  `8616d47…` — r61's two batches and r63's batch are indistinguishable by
  that label alone, and the root cause is a hardcoded constant in the as-run
  rebind tool (`'rekey_round': 61`), not a data decision. After: every
  run-book entry carries `rekey_batch` (insert-before pure insertions, CRLF,
  49 lines: `r61-batch-1` 18, `r61-batch-2` 18, `r63-batch-1` 13), the
  convention is stated of record — `rekey_round` is the run-book GENERATION
  id (61, the round that defined the run-book), `rekey_batch` is the
  EXECUTING run id — and the r64 rebind machinery itself writes
  `rekey_batch: r64-batch-1` on its 13 fresh entries, so the next run-book
  run self-identifies (the field is grep-addressable in the shipped bytes,
  criterion 120's shape). Provenance ground: S295 (W3C PROV-DM) — a derived
  record's provenance binds it to the activity that produced it and the
  generation event. Measured no-harm: the ledger edit alone leaves the guard
  green (`lost=0 ok` at rehearsal A) — the frozen selector's credit rule
  IGNORES the ledger as an input (selector binding, precheck line 69) and no
  credited entry pins it; both facts measured this round, not assumed.
- **C2 (operability, verdict-only; capability; adopts considerthese
  2026-10-28 proposal 1's cited-receipt-exists half — the ONE unimplemented
  proposal this round adopts; ground re-opened on held row S289).** New tool
  `tools/receipt-exists.py`: a cited-receipt existence sweep on committed
  bytes — for each named document read at a pinned revision
  (`git show REV:path`, never the worktree), extract candidate evidence
  paths (backtick spans, line-scoped per the r41 m8 lesson, `.ufo/` and
  `tools/` prefixes, skip-listed suffix shapes disclosed in the header), and
  resolve each with `git cat-file -e REV:path` (blob or tree — the r53.2
  cited-directory class included); `--extra-root` resolves the lane's
  fleet-root-surface cites with a named, disclosed filesystem check.
  Four-arm selftest (green / red exit 1 / usage exit 2 / extra-root), all
  hermetic under TMPDIR. Demonstration on the newest round's records: the
  r63 lesson + r63 verifier spot-check, 16 paths checked, missing=0,
  extra=2 — the sweep genuinely catches the cross-surface class (see Gate)
  and names where each path resolves. The SOURCES edits that carry the
  round's sourcing stale the 13 SOURCES-pinning sections; the r61 rekey
  run-book (reused, not re-derived — the machinery is the r63 as-run copy
  re-driven with only the round constants changed) regenerates them as
  `r64-batch-1` with trace receipts and restores the monitor. Capability row
  `receipt-existence sweep` enters the table. Criterion-109 note: the tool's
  verdict lines and 0/1/2 exit map are self-documented in its header; no
  SKILL.md exit-map row exists, so criterion 109's registry-row requirement
  is not triggered — recorded so the reader does not have to re-derive it.

## Gate

- Sourced row opened this round: **S295** (W3C PROV-DM,
  https://www.w3.org/TR/prov-dm/, fetched 2026-11-01, HTTP date Sun,
  01 Nov 2026 18:29:22 GMT; 271,572 B; sha256
  `5c925c21bc96c285b25017c3b90d82cf74251d07713b71fcb81ca60f873c9e88`;
  extract `.ufo/evidence/round-64/win-host/sources/s295-prov-dm.html`).
  Located quote (§Concepts, Generation definition, fetched-page line 1224;
  13 words): "Generation is the completion of production of a new entity by
  an activity." Grounding: C1's `rekey_batch` is a provenance batch id — it
  names the run-book activity that generated the entries, which is exactly
  PROV-DM's generation relation between entity and activity. Duplicate
  check: `grep -c prov-dm corpus/SOURCES.md` → 0 at `d0baf616` (URL
  unheld).
- Re-open of held row **S289** (CORPUS rule 2), logged old → new in the
  round-64 registry note: used-by
  `corpus/knowledge/executor-source-binding.md, corpus/lessons/round-61.md`
  → `…, corpus/lessons/round-61.md, corpus/lessons/round-64.md`. Fresh fetch
  2026-11-01 byte-identical to the r61 extract (79,360 B, sha256
  `624464ef7a3d64de06038200bff85ac09389a9d217d379dd660aa6b5165048d7`);
  new located quote for C2's existence ground (§OPTIONS `-e`, fetched-page
  lines 2246–2247; 12 words): "Exit with zero status if <object> exists and
  is a valid object." The row's status and recheck are unchanged.
- **Reject sample, stated explicitly (the r63 closure's carry-in item 2):**
  fresh rejections this round: NONE — both sources opened this round
  (S295, the S289 re-open) were adopted as claim grounds; no row was
  opened and refused. Price-outs, with reasons: the git-ls-tree
  documentation was considered as a second existence mechanism and NOT
  opened — C2's bytes resolve paths through `cat-file -e` alone, so a row
  would be an unused-source row, and staging a fetch to manufacture a
  rejection would be dishonest; the full-history receipt sweep is priced
  out under Claims (d) above. The standing rejection remains the census's
  reject marker: S293 (within-scope duplicate of S289, kept as the
  rejection record; its W04 warning stands in both census runs below).
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` → exit 0 at round start (154 rows; 17 W04 + 1 W01, all
  pre-existing) and exit 0 at round end (receipt
  `.ufo/evidence/round-64/win-host/census-end.txt`; 155 rows; the new S295
  row census-clean, no new warning; the same 17 W04 + 1 W01 set).

## Mistakes

1. **The instrument invented a git flag that does not exist (class:
   option-invention-in-instrument; captured by the selftest's green arm
   failing on a fixture where the object EXISTS).** Evidence: the first
   `path_exists` called `git cat-file -e --quiet`, and the selftest's
   green arm printed `RECEIPT_EXISTS_MISSING` for a path that was present;
   the probe run shows `error: unknown option 'quiet'` (exit 129) —
   `-e` already suppresses all output per its own spec. Fix: the flag is
   gone; the missing-object error goes to stderr and is captured, not
   printed; selftest 3/3 → 4/4 after the extra-root arm was added. The
   practice this mines: a red arm proves the failure path, but only a GREEN
   arm on a real object proves the success path — the invented flag passed
   every red arm and failed every green one.
2. **Bounded scan-back in byte surgery (class: bounded-assumption-in-byte-
   surgery; captured by the first rehearsal run, fail-closed).** Evidence:
   the first ledger-edit draft located an entry's `read_rev` by scanning
   back at most 400 lines from its `rekey_round` line; in the real ledger
   the in-entry distance reaches 2,504 and 7,709 lines (inputs dicts of
   rekey entries), so the scan returned None and the tool's
   expected-49-insertions gate refused to write. Fix: a forward pass that
   tracks the current entry's read_rev (read_rev precedes rekey_round
   inside every entry), plus the pre-existing idempotence and count gates
   kept as the fail-closed backstop. No bad bytes were written at any
   point.
3. **Constant slips in the same surgery, both fail-closed (class:
   prefix-map-constant-typo).** Evidence: the batch map key was typed as 7
   hex chars (`8616d47`) against an 8-char slice, and the first read_rev
   parse left a trailing comma — both runs refused with
   `unknown/missing read_rev` instead of writing a wrong batch id. Fix:
   8-char key, `rstrip('",')`. Recorded because the refusals are the
   discipline working, and a reader of the final green run deserves to see
   that it was not green on the first try.
4. **An inherited constant in as-run tooling mislabels its outputs (class:
   inherited-constant-in-as-run-tooling; captured-by: the r63 non-author
   closure's observation 1 — this round located the root cause and landed
   the fix).** Evidence: `'rekey_round': 61` is hardcoded in the r61 as-run
   rebind and inherited verbatim by the r63 as-run copy
   (`git show a18c20f0:.ufo/evidence/round-63/win-host/coldread-rekey-rebind-r63.py`
   carries it), so the 13 r63-created entries are labeled with r61's
   generation id and carry no run id. Fix: C1 — the data-level
   `rekey_batch` insertions and the convention of record, plus the r64
   machinery copy emitting `rekey_batch: r64-batch-1` (diff receipt:
   `make-rebind-r64.diff` in the rehearsal receipts). The r63 report's
   reading ("r63's rebind runs under the r61 run-book") is confirmed
   correct and now carries a field that says so.

## What was actually executed

- The L2 floor (one batched AgentSwarm call) has no surface on this host;
  the r60 L0 question (`.ufo/l0-questions.md` at the fleet root,
  tameshi | round-60, option (b)) stands unanswered — an L1-only round,
  disclosed here.
- A `--no-checkout` scratch clone (the lane tree carries an
  NTFS-uncheckoutable path, `a:b.txt` in the r57 wave receipts — the
  worktree cannot check out, plumbing and the plumbing-commit helper can)
  rehearsed every stage before the live run: A (ledger edit alone,
  `37d1bca1`: guard `lost=0 ok`, additivity `raw_old_only=0`,
  3 distinct inserted lines), B (SOURCES edits + tool + receipts,
  `b5568919`: RED `cand_credited=51 lost=13` — the measured forecast,
  same 13 headings as the r63 manifest), C (rekey `r64-batch-1`,
  `1144148e`: `lost=0 ok` at the round floor AND the historic floor
  `8b0042bd`, probe 20/20 both). The live run re-executes each stage; its
  receipts land with the commits.
- The rekey reused the r63 as-run machinery re-driven at this round's
  constants (the r63 carry note asked for exactly this): union plan at the
  pin (13 sections, all inputs in-tree), manifest carried from the r63
  manifest (SKILL.md byte-unchanged since r61; section shas re-verified at
  the pin by the tool's own section-sha check), rebind with trace
  receipts, monitor restored.
- LOG.md / SCORECARD.md appends are binary appends in each file's own
  ending (CRLF); SOURCES.md (LF) carries the row insertion, the S289
  cell edit, and the tail note; the ledger edits are pure insertions
  (CRLF). SOURCES.md is a rule-2 in-place-editable registry, outside the
  append-only convention's scope by its own contract.

## Verdicts

- **C1, C2 — receipts land in the commit(s) following this lesson's work
  commit** (receipt-after-subject ordering). Expected receipts, pinned here
  pre-data: `RECEIPT_EXISTS_SELFTEST: 4/4 pass` exit 0; the demo sweep at
  the tip `docs=2 paths=16 missing=0 extra=2` exit 0 with the two
  `RECEIPT_EXISTS_EXTRA` lines naming `.ufo/l0-questions.md` and
  `.ufo/reports/round-63/tameshi.md` at the fleet root;
  `git show <base>:<ledger> | grep -c '"rekey_batch"'` → 0 → 49 at the C1
  commit → 62 at the rekey commit (batches 18/18/13/13); the guard RED at
  the C2 work commit with `lost=13` and `lost=` matching the forecast
  (miss = 0 if identical), then `lost=0 ok` exit 0 at both floors at the
  rekey commit and at the tip; additivity on the landed pairs
  `raw_old_only=0` (LOG.md, SCORECARD.md, the ledger at both edit points).

## Next-round carry

- `receipt-exists.py` is a standing instrument: any round citing evidence
  receipts can sweep its named docs at their landing rev; the
  whole-history sweep (rounds 1–63) is scoped, unpriced work for a round
  that wants it — findings would be record defects of the cited-path
  class (the r53.2 precedent), not failures of this tool.
- The `rekey_batch` convention is now in the data, the lesson, and the
  machinery; the next run-book run should set its own batch id in the
  tool copy (the constant is one string).
- The guarded probe digest `892a045d…` is unchanged this round; the
  probe-arms re-run obligation stays attached to any future probe edit.
- The rekey payment is again current at the round tip: any further
  QUALITY/SOURCES/PROVINCE/README/SKILL/pinned-tool edit re-owes it. The
  measured pin sets for pricing (9 SKILL / 6 QUALITY / 7 README / 13
  SOURCES, QUALITY ⊂ SOURCES) are recorded in this lesson's ruled-out
  list for the next round's planning.
- considerthese 2026-10-28 proposals 2–5 remain unadopted (at most one
  per round; proposal 1's cited-receipt-exists half is adopted this
  round, its byte-for-byte quoted-line half remains open).
