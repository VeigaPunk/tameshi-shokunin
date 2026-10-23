# [seat ColdReadMeasureReceipt] — round-34 w1 cold-read: measure/ + dev/ receipts

Verdict: **AGREE** — the deciding-run receipt and the dev receipts are internally consistent
with the pinned artifacts at the measurement revision. Every claim below was re-derived in
`/fast/scratch/hyaku/tameshi-r34-seats/ColdReadMeasureReceipt/` against a detached clone at
lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`; no lane writes, no default-mode counter
run (kill rule consumed — module import only).

## Pins (re-derived, match)

| artifact | expected sha256 | observed |
|---|---|---|
| `tools/tally-audit-v2.py` @ `c17e593b` and @ tip | `7b11ba25…8d10` | `git show c17e593b:tools/tally-audit-v2.py \| sha256sum` → `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` ✓ |
| `tools/mutate-and-run.sh` @ `c17e593b` | `a7d3f2dd…2eb9` | `git show c17e593b:tools/mutate-and-run.sh \| sha256sum` → `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` ✓ |
| `.ufo/evidence/round-33/c1/c1-measure.py` @ `6aaad5b` and @ tip | `f6b8868c…7f28c` | both → `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` ✓ |

`git diff --stat c17e593b..0b99d48 -- .ufo/evidence/round-33 tools/` → empty (frozen inputs
unchanged between measurement revision and tip).

## measure/ — deciding-run receipt

- `.ufo/evidence/round-34/measure/c1-deciding-run.exit` = `0`; `.stdout` = the recorded
  `C1_R33_PASS=true` line at `rev=c17e593b…` `seed=685f63bd25263908`. Committed at `0b99d48`
  (same commit that lands the SCORECARD row).
- `controls_ok=1(ok)` independently re-evaluated per counter logic (c1-measure.py:362-369):
  committed `controls-receipt.json` has `all_false=true`, `counter_sha256=f6b8868c…7f28c`
  (= counter bytes at both minted rev `6aaad5b` and tip), 4 rows all `predicate_pass=false`,
  `runner_sha256` = pinned runner. `controls/mint.stdout` exit 0 agrees row-for-row.
- `heldout_after_freeze=1` re-derived: adding-commit of counter and tool = `f6d8a891`;
  all 14 `heldout/*.json` adding-commits = `c17e593b`; `git merge-base --is-ancestor
  f6d8a891 c17e593b` → 0 for every file.
- `ho_invalid=0`, `ho_kill=8/8`, `ho_accept=6/6` corroborated by the authoring re-verification
  below (14/14 witnesses pass and verdicts as expected on the sealed bytes at tip, which are
  identical to `c17e593b` per the empty diff).

## dev/ — receipts re-run

Chosen re-runs (all three, not one): witness probes, tool selftest, authoring receipts;
plus a full public-panel re-score with the deciding seed.

1. **witness-probes** (`dev/witness-probes.json`, 8/8): `python3 probes.py` → exit 0.
   All 8 `(ok, detail)` pairs byte-identical to the receipt
   (`Q1-comment-accept → (True,'vector-equivalence')`, `Q3-inert-head-kill →
   (False,'head-edit-cannot-kill')`, `Q3b-ridealong-accept → (False,'head-with-block-edit')`,
   `K-extra-leg-assign-kill → (True,'head-leg-assignment')`, `K-nonbare-leg-kill →
   (True,'head-leg-assignment')`, `A-inert-head-accept → (True,'head')`,
   `A-head-with-block → (False,'head-with-block-edit')`, `KV-block-identical →
   (False,'block-identical')`); `receipt_match: True`. Probe edits reconstructed cold:
   inert comment on the `local st_js …` decl line; extra `st_js=0` after `st_js=$?`;
   non-bare `st_kagi=$(($? & 127))`; lethal arm `npass=$((npass + 2))` for ride-along.
2. **tool-selftest** (`dev/tool-selftest.stdout`, 22/22): `TMPDIR=scratch python3 m/tool.py
   --selftest` → exit 0, `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, all 22 `CASE … PASS` lines
   including the two quoted in the receipt (`second extraction line`, `reversed operands`).
3. **authoring-receipts** (`dev/authoring-receipts.json`, 14/14): `python3 author_verify.py`
   → exit 0, `DRIFT: 0 rows differ`. For each sealed JSON: `validate_ho` → `apply_edits`
   (unique old-string) → `ho_witness_ok` under real bwrap → `run_tool_sandboxed` on pinned
   tool bytes; every row matches the committed receipt exactly — `edits_ok:true`,
   witness `[true,'head-leg-assignment'|'head'|'vector'|'vector-equivalence']`,
   tool `[KILL,1,'TALLY_AUDIT: FAIL (…)']` for the 8 kill copies and
   `[ACCEPT,0,'TALLY_AUDIT: PASS (…)']` for the 6 accept copies.
4. **public panel** (`dev/panel.stdout` + deciding-run `v1_*` fields):
   `python3 panel_rerun.py` → exit 0, `panel copies: 26 kill: 18 accept: 8`,
   `PANEL: kill=18/18 accept=8/8` — matches `dev/panel.stdout` (`18/18 + 8/8`) and the
   deciding run's `v1_kill=18/18 v1_accept=8/8` with the same recorded seed
   `685f63bd25263908`.

## Observation (not a measurement defect)

`dev/authoring.stdout` records `ho-kill-vector-setup-threshold` with
`"witness": [false, "vector"], "as_expected": false` and `SEALED: kill=8 accept=6
all_as_expected=False`, while `authoring-receipts.json` (same commit `6aaad5b`) has
`[true, "vector"], as_expected: true`. This is the lesson's documented first-generation
run (`corpus/lessons/round-34.md` Mistake 1: the copy was first authored with witness
`[2,2,0,…]` — two setups still trip `-gt 1`, the witness tied, caught pre-commit; fixed to
`[2,0,…]` and re-verified by execution). My re-verification confirms the JSON side is the
current truth: the sealed fixture's witness vector is `[2,0,…]` → `(True,'vector')`, tool
verdict `KILL`. The `.stdout` is stale provenance committed alongside the corrected
receipt — a mildly confusing pairing, harmless: the deciding run re-executed every
witness anyway (`ho_invalid=0`).

## Commands & exits (all in `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadMeasureReceipt/`)

- `python3 probes.py` → exit 0 (witness gate re-run, 8/8 + receipt byte-match)
- `TMPDIR=$PWD/tmp python3 m/tool.py --selftest` → exit 0 (22/22)
- `python3 author_verify.py` → exit 0 (14/14 rows, 0 drift, `all_as_expected=True`)
- `python3 panel_rerun.py` → exit 0 (`panel copies: 26 kill: 18 accept: 8` / `PANEL: kill=18/18 accept=8/8`)
- `sha256sum m/tool.py m/mutate-and-run.sh m/round-33/c1/c1-measure.py` → all three pins match
- No installs; tools used: python3.13, bwrap 0.13.1, git — all pre-existing.
