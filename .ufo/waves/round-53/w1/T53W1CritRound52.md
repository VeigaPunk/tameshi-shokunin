# T53W1CritRound52 — R52.6/R52.2 conformance audit (round-52 routed defects vs. current tree)

Seat: T53W1CritRound52 (wave-1 critic). Scope: read-only verification of routed defects
R52.1–R52.6 from `corpus/lessons/round-52-verifier-spotcheck.md` against the lane tree.
Content commit C* = `a41195dfc13a73958e4c5228ec196b28d03ded03`; base = `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`.
No scratch dirs created; no tools installed; no git mutations run (read-only `git log/show/grep/ls-tree/diff` only).

## Verdict table

| defect | routed demand | observed at tree | verdict |
|---|---|---|---|
| R52.1 | re-run frozen re-key/deciding pipeline for the 19 lost sections | folded into round-53 C1 (30-heading re-key); wave-1 readers in flight; deciding run pending | OPEN (in-flight, expected) |
| R52.2 | append LOG.md round-52 entry naming bcba892→f1a3246 + wrap-up disposition | entry present at C* (added in a41195d); absent at base | CLOSED at C* |
| R52.3 | re-derive the "8 over-count" verdict under one written counting rule; correct lesson row if warranted | re-derivation seat T53W1ExecR523 dispatched in wave 1 (`spec-w1.json` items); no deliverable on disk yet | OPEN (seat exists, output pending) |
| R52.4 | commit the 4 untracked round-52 w3 paths or revert | all 4 paths committed at 6db1d220 | CLOSED |
| R52.5 | tools/ `dir="/tmp"` hardcodes honour TMPDIR | grep for `dir\s*=\s*["']/tmp` over `tools/` at C* prints nothing (exit 1); 9 hits across 7 tools at base | CLOSED at C* (counter confirmation pending) |
| R52.6 | round-report conformance repairs | applies to the round-53 report, which does not exist yet | OPEN by construction |

## Evidence

### R52.2 — LOG.md round-52 entry (CLOSED)

- `git -C …/tameshi-shokunin show 6db1d220:LOG.md | grep -ciE "round 52|round-52"` → `0` (no entry at base).
- Pickaxe: `git log --format='%h %s' -S "round 52 (honest stop" --oneline -- LOG.md` → `a41195d round-53: C* content commit — … LOG r52+r53 entries …` (single commit, appended this round).
- At C*: `git show a41195d:LOG.md` tail contains `## 2026-10-27 — round 52 (honest stop, run wrap-up)` naming landed commits `bcba8924` → `f1a32461` (tip), the closure `c1d49d7`, the salvage `6db1d220`, and the wrap-up disposition — exactly the content R52.2 demanded ("append, never rewrite": the entry is a new trailing heading; the base→C* diff on LOG.md is `+36 -0`, both new entries).
- Entry is also at HEAD (`ace79e3`): `git status --porcelain` shows no LOG.md modification, and `ace79e3` descends from `a41195d`.
- Note the entry correctly cites the round-52 report at fleet commit `53fdd555`, which repairs spotcheck defect (a) at the LOG level (the report body itself still contains the false "not committed/pushed" sentence — historical, R52.6 covers future reports).

### R52.4 — w3 files committed at 6db1d220 (CLOSED)

- `git show 6db1d220 --stat` (subject "round-52 w3: commit wave markers and integrate script (closure salvage)") adds all four paths the spotcheck listed as untracked:
  - `.ufo/evidence/round-52/integrate/build-readers.py`, `.ufo/waves/round-52/w3.ready`, `.ufo/waves/round-52/w3.ready.dispatched` → `git ls-tree -r --name-only 6db1d220 -- <3 paths>` = 3.
  - `.ufo/waves/round-52/w3/` → `git ls-tree -r --name-only 6db1d220 -- .ufo/waves/round-52/w3/` = 77 files.
- Current `git status --porcelain` carries no round-52 untracked paths — nothing of round 52 remains uncommitted. (The untracked entries now on the tree are all round-53 wave-1 outputs — see watch item below.)

### R52.5 — tools/ grep empty at C* (CLOSED at C*; counter confirmation pending)

- At C*: `git grep -nE "dir[[:space:]]*=[[:space:]]*[\"']/tmp" a41195dfc13a73958e4c5228ec196b28d03ded03 -- tools/` → no output, exit 1. This is the exact regex family the frozen C2 predicate greps for.
- At base: same grep prints 9 hits across 7 tools — `tools/bash-witness-study.py:1241`, `tools/context-capture.py:27,1625`, `tools/env-diff.py:61`, `tools/evidence-disposition.py:2351`, `tools/pin-disposition.py:706`, `tools/registry-check.py:766,917`, `tools/repeat-control.py:597` — matching the round-53 LOG entry's "7 tool /tmp hardcodes honour TMPDIR" and the contract's C2 `before` (registry-check.py:766, env-diff.py:61). Before → after: 9 hits → 0 at C*.
- The frozen C2 counter still has to print `C2_R53_PASS=true` at the deciding run (its SKILL.md arm — "SKILL.md names no /tmp scratch path for either tool" — and the TMPDIR selftest exits are the counter's checks, outside this seat's four items).

### R52.3 — re-derivation seat T53W1ExecR523 (OPEN: dispatched, output pending)

- `jq -r '.items[] | .seat' .ufo/waves/round-53/spec-w1.json` lists `T53W1ExecR523` among the 44 wave-1 seats (4 executors: T53W1ExecR523, T53W1ExecRegCheck, T53W1ExecTmpVerify, T53W1LabLint). The seat exists this wave as routed.
- At the time of this audit no `T53W1ExecR523.*` deliverable exists under `.ufo/waves/round-53/w1/` (directory currently holds reader outputs only). "Dispatched" ≠ "landed": the conformance section may cite this seat only once its report is on disk and, if it corrects the lesson row, the correction is committed.

## What remains open for the round-53 report's conformance section

1. **R52.1 / C1** — the re-key itself: 30/30 reader JSONs, ledger entries with provenance under `rekey-r53-<C0>/`, the frozen coldread precheck printing GREEN at the measured revision, and the C1 counter passing at the deciding run. Until then R52.1 stays open by definition.
2. **R52.3** — T53W1ExecR523's re-derivation must land, and if the "8 over-count" verdict changes, the lesson row is corrected under one written counting rule; the routed "consider a QUALITY criterion for reviewer-seat quote truncation" is a round-53 decision the L1 still owes a yes/no.
3. **R52.5 / C2** — grep-empty is verified at C* by this seat; the conformance section should rest the claim on the frozen C2 counter's `C2_R53_PASS=true` receipt at the deciding run, not on this grep alone.
4. **R52.6** — applies to the round-53 report being written this round: per-box SHONEN lines (one line per box, no single `[~]` blanket), "Landed changes" and "Before → after measurements" sections, no false not-committed/not-pushed sentences, trend verdicts inside the allowed vocabulary. Also carry forward spotcheck items (f) and (g) as style guidance: print the census row count in the receipt body, and keep reader-delivered counts consistent with committed reader JSONs.
5. **Round-53 analog of R52.4 (watch item)** — the tree currently carries untracked round-53 wave-1 outputs (reader JSON/MD pairs, `spec-w2.json`, `.ufo/evidence/round-53/{assimilation,census-mid.stdout,integrate,verify-freeze.*}`). This is normal mid-wave, and the kill rule already demands a clean working tree at the deciding run; but the round-53 report's conformance section should note the commit that lands them (same disposition R52.4 required of round 52).

## Fixed-vs-tradeoff note

Nothing found here is a tradeoff the judge must reject. One flag for the L1, not a defect: the R52.2 entry was added in the same commit (`a41195d`) that carries the round-53 content fixes, so "round-52 entry present" is true at C* and HEAD but was never true at any intermediate post-freeze revision — if the deciding run measures a revision other than C*, re-verify the entry exists there (it does at HEAD; it does not exist between `218bc6b` and `a41195d`'s parent — no such intermediate revision is in the landed history, so no live risk).
