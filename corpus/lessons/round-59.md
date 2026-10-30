# tameshi round 59 — lesson (hyaku run 11, 2026-10-30)

L1 `TameshiR59a2` (attempt 2; attempt 1 `TameshiR59` left the w1 wave dispatched and ended without a report). Base `b83f1bfc7b302f22e89d9631ac7e6ac87ea78c2a`; contract `.ufo/evidence/round-59/contract.json`; counter `.ufo/evidence/round-59/measure.py`; freeze `e9cc34bec3f0c670550552bcc962563e7ae3ca58`; tool commit (measured) `93acc996cbb7bfed27112e797c9d2392ff4aa6b3`.

## Claims

- **C1 (operability, capability acquisition).** `tools/executor-source-pin.py` enters: it compares each verifier-declared executor source Git blob in a candidate commit to the same path in a verifier-supplied trusted commit. Frozen predicate: 24 CLI fixtures (six classes × four path spellings) pass; skipped-work and always-accept controls fail. Stagnation-nudge frontier move (calibration 8, depth 10, freshness 9 sit at or above the saturation line; no capability since round 50), named in `SCORECARD.md`.

## Gate

- Sourced row opened this round: **S289**, Git `git-cat-file` documentation (2.56.0), https://git-scm.com/docs/git-cat-file, accessed 2026-10-30. Located quote (§DESCRIPTION, first sentence, 17 words): "Output the contents or other properties such as size, type or delta information of one or more objects." It grounds `teaches`: object inspection, not execution attestation; `--textconv`/`--filters` transform content, so a raw `cat-file blob` comparison binds committed bytes. The knowledge entry `corpus/knowledge/executor-source-binding.md` cites S289.
- Rejected candidates this round: none recorded.
- Id collision check: `grep -c S289 corpus/SOURCES.md` before the append → 0 (registry max S288).
- Status, recheck and used-by changes to existing rows, old → new: none.
- Census before (round start): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0; rows 148; W04 warnings 16 (pre-existing duplicate URLs); W01 S101 (pre-existing).
- Census after: exit 0; rows 149 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); malformed rows 0; tiers A=131 B=14 C=4; W04 warnings 16 (unchanged); W01 S101 unchanged.
- Assimilation: none (no `merge/tameshi/` package adopted this round; no shokuknow registry append).
- `considerthese/`: not mined this round. Proposals 4 and 5 of `considerthese/2026-10-28.md` stay carried.

## Mistakes

1. **Counter accepts a fingerprint cheat (class: non-discriminating counter).** Evidence: `.ufo/waves/round-59/w1/T59W1S62/stage/cheat-fp.py` (never reads `--trusted`; recognises the counter's constant commit message and blob text) run through the frozen counter at `e9cc34bec3f0c670550552bcc962563e7ae3ca58` → `passed=24/24 C1_R59_PASS=true` (`.ufo/evidence/round-59/controls/cheat-cheat-fp.out`). The sequence cheat `cheat-seq.py` (fixed 0,1,1,0,2,1 by invocation count) also scores 24/24 (`cheat-cheat-seq.out`). Captured-by: **none** — the freeze's controls were tool-absent and do-nothing only (S61: 0/8/8/0/12), and a constant-recognising tool was not among them. Fix: successor counter `.ufo/evidence/round-59/successor/measure-nonce.py` (per-run nonce in fixture contents and commit message; class order shuffled). Shown able to fail: fingerprint 16/24, sequence 10/24, hashonly 20/24, always-accept 8/24, skipped-work 0/24; real tool 24/24 (`successor/succ-*.out`). The fix is shown able to fail; it is a successor instrument and does not re-score C1. Frozen-counter amendment is routed to the next round.
2. **Counter blind to multi-path invocations (class: coverage hole in the predicate).** Evidence: `T59W1S32.json` headline — the frozen counter invokes the tool with one `--path` per call, so a first-path-only strawman scores 24/24. Captured-by: none. Fix: not yet landed; routed to the successor counter (it must invoke all declared paths in one call). Carried as F11's open residual.
3. **Handoff addressed to a dead L1 (class: orchestration).** Evidence: `.ufo/waves/round-59/w1.ready` names `l1: TameshiR59`; the wave dispatched at 11:28 (`w1.ready.dispatched`); attempt 1 ended without a report at 11:58 (`.ufo/watchdog.log` line 2001). WAVE-DONE for w1 therefore routes to a dead id. Captured-by: none. Fix: `agent://Main` asked (12:10) to deliver WAVE-DONE to `TameshiR59a2`; the ready file is never rewritten (wave rule).
4. **Seat outputs incomplete (class: wave evidence).** Evidence: `.ufo/waves/round-59/w1-results.json` (64 settled seats; `T59W1S27` terminal output empty); `.ufo/waves/round-59/w1/` has no `T59W1S26.md`, `T59W1S27.md`, `T59W1S28.md`, and no `.json` for `T59W1S26`, `S27`, `S28`, `S37`, `S49`. `T59W1S49` staged the tool (`stage/tools/executor-source-pin.py`, sha256 `a7636e34…037`) but wrote no structured result; its terminal output carries the report. Captured-by: none (the wave validator checks counts, not seat outputs). Fix: `T59W1S27` gets no review credit; the staged S49 tool was taken and measured by L1 (the counter is the authority, not the seat's probe count).

5. **Frozen contract has no `coldread_forecast` (class: conformance, QUALITY criterion 110).** Evidence: `.ufo/evidence/round-59/contract.json` top-level keys carry no forecast; criterion 110 requires one from round 58 on. The round's planned content edits to monitored files (`corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/executor-source-binding.md`) are therefore unpriced. Captured-by: none (the freeze check does not test the key). Fix: not repaired — the freeze is immutable for this round; the forecast key is a successor-contract requirement, and the cold-read credit impact is named here, not measured.

## Attack findings on the staged gate (retained, not admitted as claims)

- `T59W1S34`: a trusted-mode mutant survives the frozen counter; a targeted detector kills it.
- `T59W1S40`: a declared-path mutant survives the frozen counter.
- `T59W1S57`: repository-local `refs/replace` would redirect object reads; the staged tool passes `--no-replace-objects` on every git call and env-scrubs `GIT_*` (`T59W1S49.md` replace probe: changed still exits 1).
- `T59W1S35`: porcelain textconv/gitattributes subversion; the tool uses only plumbing (`ls-tree -z`, `cat-file blob`, `rev-parse`).
- `T59W1S30`: NUL paths cannot reach argv; the NUL guard is defence-in-depth.
- `T59W1S61`: do-nothing strategies score 0/8/8/0/12 — the frozen target is unreachable by do-nothing, but reachable by the fingerprint cheat (Mistake 1).
- `T59W1S38` (critic): strict `text=True` decoding and `errors='replace'` comparison are both unsound designs; the staged tool decodes nothing (raw `cat-file blob` bytes, `bytes !=` comparison), so neither attack lands on the staged tool.
- `T59W1S39` (reviewer): the frozen counter's 24 fixtures have no empty-blob cell; an empty-blob-unsound tool scores 24/24. The staged tool compares blob object ids and raw bytes, so an empty declared blob is handled by the same path (not a separate branch); the gap is in the counter.
- `T59W1S31` (mutation-tester): a duplicate-path `continue`→`break` mutant survives the frozen counter (one `--path` per call) and is killed by a targeted two-path probe. Same family as Mistake 2.
- `T59W1S33` (reviewer): exec-bit flip 755→644 with an equal blob is on the claim boundary. Decision (L1): the contract declares blob equality over declared sources and the knowledge entry states the executable bit is not required; exit 0 stays, and the boundary is recorded, not enlarged.
- `T59W1S36` (reviewer): a naive oracle under `GIT_DIR` redirection with a forged HEAD returns BOUND; the staged tool strips `GIT_*` and passes `--no-replace-objects`, and the frozen counter scrubs the same variables before any call.
- Staged-tool observation (L1 read of `tools/executor-source-pin.py:249-256`): a blob-read plumbing failure maps to DRIFT (exit 1), not UNAVAILABLE (exit 2). Fail-closed, not an acceptance path, and no frozen cell exercises it; routed to the successor tool review.

## Verdicts

- **C1, measured.** Before (base `b83f1bfc`, tool absent): `passed=0/24 C1_R59_PASS=false reason=tool-absent` (`.ufo/evidence/round-59/before.stdout`). After (`93acc996`): `passed=24/24 C1_R59_PASS=true` (`.ufo/evidence/round-59/after/cert.out`). Controls at freeze `e9cc34bec`: always-accept `passed=8/24 C1_R59_PASS=false`; skipped-work `passed=0/24 C1_R59_PASS=false` (`.ufo/evidence/round-59/controls/`). The claim verifies under its frozen predicate; the predicate is cheat-passable (Mistake 1), so the 24/24 certifies the declared fixture cells, not blob comparison as such. Operator ruling requested.

## Next-round carry

- Frozen-counter amendment (multi-path invocation; nonce fixtures) before any C2-like claim: the successor instrument is the candidate.
- Multi-path blind spot (Mistake 2).
- Seat-output completeness check in the wave validator (Mistake 4).
- Successor tool review: blob-read plumbing failure exit class (Staged-tool observation above).
- Empty-blob cell in the successor counter (`T59W1S39`).
- Cold-read forecast key in the successor contract (Mistake 5).
