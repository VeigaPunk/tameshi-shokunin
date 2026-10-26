# T50Cross48 — C1 independent cross-coding, round 48 (R48.1..R48.6)

Seat: T50Cross48. Base tree: `e3729de862f73ae080d98fcf522a7081ce16e40a`. Routed at: `8ca67421111fa354b47b803358391d0b07fc6db9`. No `T50Disp*.*` files were read. All excerpts below were validated at base against the frozen counter's evidence rules (check_evidence + has_key + fixed-fresh) with a scratch replica; all validated clean.

Coding: **R48.1 fixed, R48.2 fixed, R48.3 fixed, R48.4 open, R48.5 fixed, R48.6 declined.**

## R48.1 — Cold-read credit — FIXED
Ask: restore credit for rounds 12/13/14 headings via successor ledger/refresh (or declare withdrawn); from now on run QUALITY 98 precheck on every candidate content revision before freezing it.
Evidence:
- `.ufo/evidence/round-49/quality/coldread-precheck-fc5ac743.stdout:1` — `COLDREAD_PRECHECK floor=8ca67421111f floor_credited=57 cand=fc5ac743fb42 cand_credited=64 lost=0 ok` (`git show e3729de:.ufo/evidence/round-49/quality/coldread-precheck-fc5ac743.stdout`).
- `.ufo/evidence/round-49/coldread/refresh-receipts.json:3` — reading-bound refresh, "not blind cold-read or recipe execution" (`git show e3729de:.ufo/evidence/round-49/coldread/refresh-receipts.json | nl -ba | sed -n '1,12p'`).
- `.ufo/evidence/round-49/deciding-run.sh:38` — precheck wired into the deciding run (`git show e3729de:.ufo/evidence/round-49/deciding-run.sh | nl -ba | sed -n '30,95p'`).
Tree support: the round-21 coldread measure at base (`python3 .ufo/evidence/round-21/coldread/measure.py --rev e3729de --repo <scratch clone>`) credits **64** sections with restraint score 8 (was 57 at routing). Commit `bda60768` (final content revision) added the precheck receipt; the file is absent at routed_at, so the excerpt is fresh.

## R48.2 — Deciding script — FIXED
Ask: write start and exit receipts before any output is read; drop receipt directories from the frozen path list.
Evidence: `.ufo/evidence/round-49/deciding-run.sh:8-9` (start/exit receipt semantics), `:46-48` (c1.start written before the counter runs; c1.end after; verdict tail read after both), `:32` (FROZEN path list names code and contract only — no receipt dir). Commit `14d03ea4` added the script (absent at routed_at). Gate 0 (`:29`) also refuses a second invocation.

## R48.3 — Pre-registered order — FIXED
Ask: score every control at freeze before any deciding run; declare any `--only` previews in contract and report.
Evidence: `.ufo/evidence/round-49/deciding-run.sh:6-7` (gate 0: exit 3, nothing run, unless every pre-registered control receipt is committed at REV in a commit descended from FREEZE — controls scored before any deciding run), `:23-24` (the required control receipts). SCORECARD.md:2388 records controls scored at freeze bytes and committed at `6885adb4` before wave 1/deciding. No `--only` previews were run in round 49 (`git grep -n -- "--only" e3729de -- .ufo/evidence/round-49/` finds only contract.json's fix description), so the disclosure clause had nothing to attach to.

## R48.4 — Carried items — OPEN
Compound; fixed only if every ask lands. At base:
- `tools/tally-audit-v2.py:135` and `tools/tally-audit-v3.py:234` still define `brace_depth_at` (`git grep -n "brace_depth_at" e3729de -- tools`) — neither deleted nor re-pinned.
- S205 has no SOURCES row at base (`git show e3729de:corpus/SOURCES.md | grep -c 1810.05286` → 0); F7 appears only as a scope label on the S041 row, no package candidate landed.
- No pinned-leg successor nor declared nondeterministic class for `six-leg regression ledger` appears in the round-49 tree or base SCORECARD planned paragraphs.
- No located-name (entry-author) check impl; no append-only rule for landed seat reports impl.
The newest `**Planned (round 50)` paragraph at base (SCORECARD.md:2410) names no R48.* id ("carried items from round 48's list") — the L1 must name R48.4 there for the open row to pass the counter.

## R48.5 — Corrections sweep — FIXED
Ask: SCORECARD's "pasted byte-exact" sentence should say axis rows carry the emitted clause after lane prose; append, do not rewrite.
Evidence: `SCORECARD.md:2382-2384` — appended section `### Round 48 — correction (appended in round 49)` with the corrected reading (19 capability rows byte-exact; 3 axis rows carry lane prose followed by the emitted `tool sha256 … runs 3 stable` clause). Commit `6db4b931` added it (verified by `git diff 6db4b931^ 6db4b931 -- SCORECARD.md`). The excerpt is absent at routed_at.

## R48.6 — SHONEN — DECLINED
Ask: none — the spot-check records all four boxes remain `[~]`, none fully checkable by a non-author, promotion stays operator-owned. `SHONEN.md:5-11` at base confirms the four `[~]` boxes with no independent promotion verifier. Reason (≥40 chars): no lane action is requested; promotion is operator-owned; no tree change can resolve the item.

## Method
- Read the frozen statement set (`.ufo/evidence/round-50/c1/defects.json` R48.* records), the counter (`measure.py`) evidence/status rules, and the round-48 spot-check routed list in full.
- For every fixed candidate, named the strongest counter-reason and checked it (recorded as `doubt` per item): e.g. precheck-after-freeze ordering (R48.1), non-counter receipts preceding start stamps (R48.2), gate-only enforcement (R48.3), prose-only correction (R48.5).
- Validated every evidence row in scratch against a replica of check_evidence/has_key/fixed-fresh (excerpt length 15–400, line span ≤30, key presence, ack-word absence, freshness vs routed_at, commit ancestry/touch). All rows passed.
- No frozen counter was run against the lane; the coldread measure was run only in a scratch clone as an observation.

## Summary
- R48.1 fixed: cold-read credit restored (57→64; rounds 12/13/14 re-credited by round 49's C1 refresh) and QUALITY 98 precheck runs on candidates (receipts at fc5ac743 and in the deciding run).
- R48.2 fixed: round-49 deciding-run.sh writes start/exit receipts before reading counter output and its frozen path list excludes receipt dirs (added by 14d03ea4).
- R48.3 fixed: gate 0 enforces controls-scored-before-deciding; round-49 controls committed at 6885adb4 before deciding; no `--only` previews ran.
- R48.4 open: dead `brace_depth_at` helpers still present (tally-audit-v2.py:135, v3.py:234); S205/F7, six-leg decision, located-name, append-only rule all absent; needs L1 planning of R48.4.
- R48.5 fixed: correction appended verbatim in SCORECARD.md (6db4b931), no rewrite.
- R48.6 declined: no lane ask; promotion operator-owned; all four SHONEN boxes still `[~]`.
- Deliverables: `.ufo/waves/round-50/w1/T50Cross48.json`, `.ufo/waves/round-50/w1/T50Cross48.md`.
