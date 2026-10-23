# QualityGate — round 34 wave 1 (tameshi-r34-w1-QualityGate)

Scope: check `corpus/QUALITY.md` against this round's new evidence — does any criterion cover the
round-34 mistake class (authoring prediction validated by assertion instead of execution,
`corpus/lessons/round-34.md` `## Mistakes` row 1)? If none, draft the exact criterion text
(report-only; the lane is not edited) and name the lesson row it cites.

## 1. Setup and pin verification (all commands run as written; exit codes captured with `; echo $?`)

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/QualityGate \
  && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
       /home/vgpnk/Projects/shokunin/tameshi-shokunin \
       /fast/scratch/hyaku/tameshi-r34-seats/QualityGate/lane \
  && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../QualityGate/lane \
       checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
# setup_exit=0
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py    # exit 0
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh # exit 0
sha256sum tool.py pristine.sh
git -C lane rev-parse HEAD
```

- `tool.py` = `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` — matches the
  frozen tool pin.
- `pristine.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — matches the
  frozen runner pin.
- `HEAD` = `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` — lane tip at dispatch.
- Counter at tip: `sha256(.ufo/evidence/round-33/c1/c1-measure.py)` =
  `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — matches the amendment-6
  pin (`f6b8868c…a07f28c`).
- History: `git log -3 --format='%H %s'` prints tip `0b99d48e` (deciding-run receipt + lesson),
  then `c17e593b` ("sealed held-out set authored after the amendment-6 counter freeze … per-copy
  authoring receipts"), then `9dd3174c` (controls receipt at the amended rev) — matches the
  round order in the lesson header.
- Deciding receipt: `.ufo/evidence/round-34/measure/c1-deciding-run.exit` = `0`; `.stdout` reads
  `C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18
  v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1
  seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true` —
  byte-identical to the dispatched claim. The deciding run stands; nothing here re-opens it.

The kill rule was consumed: the counter was never run in default mode. It was imported as a
module in scratch (allowed) and only `block_run` / `ho_witness_ok` / `apply_edits` /
`tally_block_of` were called on scratch copies.

## 2. Coverage answer: NO criterion covers the round-34 mistake class

Evidence: `corpus/QUALITY.md` at `0b99d48e` is 844 lines, criteria 1–71 (read in full via
overlapping ranges `:1-300`, `:301-580`, `:578-600`, `:584-844`, `:800-844`). Rounds 32/33
appended no criteria (freeze rounds) — the last section is "Criterion appended — round 31 claim
C1" (criterion 71). The class "an authoring prediction validated by assertion instead of
execution" is not covered. Nearest misses, all rejected:

| Criterion | Why it does not cover |
|---|---|
| 6 (round 1, MK-2/3) | Governs *reporting* of pre-registered predictions in entries (executed outcome in the same entry; miss becomes errata). Says nothing about how an authored fixture expectation is validated at authoring time, and never requires rejecting a non-discriminating copy. |
| 15 (round 14) | Wrong failure mode: a *setup error* that happens to produce the expected exit code. The r34 case is an authored prediction that was wrong (non-discriminating), not a mis-provenanced retained expectation. |
| 29 (round 17) | Guard-removal coverage of lane tool selftests. About guard *code*, not authored held-out expectations. |
| 12 (round 12) | Frozen-witness *replay* (prior exposure, integrity). Replay side; authoring-side validation is out of scope. |
| 44 (round 21) | Mutation population *anchors* re-checked at freeze rev. Anchors, not witnesses/verdicts. |
| 48/49 (round 24) | Repair discipline: frozen predicate fails at base, holds after; per-trigger fixtures. Scoped to routed hardening-gap repairs, not sealed-set authoring; the r34 case was caught pre-commit, no repair claim was made. |
| 54/55 (round 27/29) | Run receipts bound to tool/input bytes; re-run at measured revision. About run receipts, not authored expectations. |
| 64/65 (round 30) | Counter identity-blindness; verdict-only counters vs "runs the code" claims. Counter properties, not fixture authoring. |

The r34 class is real and distinct: an authored *prediction* (expected witness vector) was
initially checked only by an assertion over the authored copy (the witness gate), and would have
landed a non-discriminating must-kill (pristine and mutated tie) had the gate not returned
false. No criterion requires execution-derived discrimination at authoring time, rejects ties,
or mandates retaining the rejected first generation.

## 3. Lesson Mistakes #1 — evidence chain verified

Lesson row cited: `corpus/lessons/round-34.md` `## Mistakes` row 1
(class: "an authoring prediction validated by assertion instead of execution").

- Guard mechanics in the pinned tool: `tool.py` REF_BLOCK lines 82–87 —
  `if [[ $nsetup -gt 0 ]]` → `REGRESSION: SETUP (… cannot-verify=%s)`, `exit 2`.
- Sealed copy `.ufo/evidence/round-33/heldout/ho-kill-vector-setup-threshold.json`: edit
  `[[ $nsetup -gt 0 ]]` → `[[ $nsetup -gt 1 ]]` (exactly one edit), final witness
  `[2,0,0,0,0,0,0,0,0]` — the fixed single-setup vector, as the lesson states.
- Frozen counter, `c1-measure.py:184-231`: for kill+vector, `ho_witness_ok` requires
  `pb != mb` (blocks differ) and `block_run(pb, vec) != block_run(mb, vec)` — i.e. discrimination
  is defined by *executing* both tally blocks on the witness vector.
- Live falsifier (scratch `witness-falsify.py`, imports the frozen counter as a module, exit 0;
  bwrap sandbox exercised by `block_run` exactly as in the deciding run):

```
first-gen [2,2,0,...]: pristine=(2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')
                       mutated =(2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')
                       tie=True
ho_witness_ok(first-gen) = (False, 'vector')
committed [2,0,...]: pristine=(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')
                     mutated =(0, 'REGRESSION: PASS (cases=9 passed=8; ledger legs exact: …)')
                     differ=True
ho_witness_ok(committed) = (True, 'vector')
```

Every quantitative claim in the lesson row reproduces from committed bytes: the tie (both
SETUP), the `(False, 'vector')` gate result, the fixed vector, and pristine
SETUP(cannot-verify=1) vs mutated PASS(passed=8).

## 4. Findings

**F1 (Low) — the lesson's able-to-fail proof is not committed; pointer names a file that cannot
show it.** `corpus/lessons/round-34.md` Mistakes #1 fix clause: "shown able to fail by the caught
receipt itself (`.ufo/evidence/round-34/dev/authoring-receipts.json` first generation, preserved
in the scratch transcript)". The committed file contains 14 rows (14 unique ids), every one
`as_expected=true` — the caught first-generation receipt (witness `[2,2,0,…]`,
`(False, 'vector')`) exists only in the L1's scratch transcript, outside the repo. This is in
tension with criterion 9 (evidence a claim rests on is copied into the repo before the commit
that cites it) and criterion 2 (every claim carries a source). Mitigation: the failure is
re-provable from committed bytes alone (§3 falsifier), so the lesson's substance stands; what is
missing is the retained discriminating artifact.

Reproducing commands (lane root, read-only):

```
python3 -c "import json;rows=json.load(open('.ufo/evidence/round-34/dev/authoring-receipts.json'));print(len(rows), sorted(set(str(r['as_expected']) for r in rows)))"
# -> 14 ['True']
git log -1 --format='%h %s' -- .ufo/evidence/round-34/dev/authoring-receipts.json
# -> 6aaad5b round-34: amendment 6 set-aware witness gate (pre-authoring, pre-data) + … + dev receipts
```

**O2 (observation, no defect proven) — receipts landed with the amendment, not with the sealed
set.** `authoring-receipts.json` last changed at `6aaad5b` (the amendment-6 commit), while
`c17e593b`'s subject advertises "per-copy authoring receipts" but did not touch the file. The
authoring session necessarily pre-dates the `6aaad5b` commit, which is consistent with the
lesson's "PRE-AUTHORING" ordering claim; noted only because the commit subjects read as if the
receipts belong to the sealed-set commit.

No other defect found in the checked chain (pins, deciding receipt, exit code, sealed copy,
receipt census, counter sha — §1/§3).

## 5. Drafted criterion (report-only; would be appended to corpus/QUALITY.md)

Cites lesson row: `corpus/lessons/round-34.md` `## Mistakes` row 1.

```markdown
## Criterion appended — round 34 (2026-10-23)

72. Round 34. An authored expectation in a sealed held-out copy — a predicted witness vector or
    verdict — is validated by executing the real pristine and mutated programs on it before the
    copy commits, and the per-copy authoring receipt records that executed pair. An expectation
    whose pristine and mutated executions tie (same exit and first stdout line) is rejected
    before commit, and the rejected first generation is retained as committed evidence beside
    the accepted row, never only in a scratch transcript. The gate that scores a copy (witness
    gate, selftest, oracle) validates the copy only by consuming executed pristine/mutant
    outcomes; an authored prediction is never validated by the assertion that scores it.
    Captured by: `corpus/lessons/round-34.md` `## Mistakes` row 1 — the
    `ho-kill-vector-setup-threshold` copy was first authored with witness `[2,2,0,…]`; with the
    mutant guard `$nsetup -gt 1` two setups still trip the pristine `-gt 0` guard, pristine and
    mutated tie (both SETUP), and the witness gate returned `(False, 'vector')`; the fix
    (witness `[2,0,…]`, single setup escapes the `-gt 1` guard) was re-verified by execution —
    pristine SETUP(cannot-verify=1) vs mutated PASS(passed=8). Falsifier: import the frozen
    amendment-6 counter (`.ufo/evidence/round-33/c1/c1-measure.py`, sha256 `f6b8868c…a07f28c`)
    as a module on the pinned runner bytes (`tools/mutate-and-run.sh`, sha256 `a7d3f2dd…2eb9`
    at `0b99d48e`) and call `block_run` / `ho_witness_ok`: vector `[2,2,0,0,0,0,0,0,0]` gives
    pristine = mutated = `(2, 'REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)')` and
    `(False, 'vector')`; the committed vector `[2,0,0,0,0,0,0,0,0]`
    (`.ufo/evidence/round-33/heldout/ho-kill-vector-setup-threshold.json`) gives
    `(2, 'REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)')` vs
    `(0, 'REGRESSION: PASS (cases=9 passed=8; …)')` and `(True, 'vector')`. A receipts file in
    which every row reads `as_expected=true` cannot demonstrate the rule able to fail; the
    falsifier above is the check that can fail.
```

## 6. Tooling record

No tools installed or upgraded this seat (per operator directive 2026-10-19 and the round-34
pacman pause): `python3`, `git`, `sha256sum`, and the host's `bwrap` (exercised by the counter's
own `block_run`) were sufficient.

## 7. Residual risk and verification gaps

- The historical first-generation receipt bytes were not available (scratch transcript of the
  L1, not in the repo); the `[2,2,0,…]` shape is taken from the lesson text, and the falsifier
  reconstructs the failure from that vector rather than from the historical bytes.
- `ho_witness_ok`'s other branches (head/equivalence) were read but not exercised here; sibling
  mutants (e.g. `MutCounterdropblockidentical`, `MutCounterdropequivalencebytes`) cover them.
- Only criterion-coverage of the named round-34 mistake class was in scope; QUALITY 1–71 were
  enumerated against that class, not re-audited generally.
