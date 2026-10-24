# LabratPanelOrigin — round-36 w1 probe (read-only)

## Hypothesis under test
The v2 deciding run's `pub_distinct=9` is computed by `distinct_bodies` over the 9
public panel copies — i.e. the set `sha256(runner_text + copy.edits)` has
cardinality 9 over `.ufo/evidence/round-35/c1/panel` at the measurement commit.

## What I attacked
- Claim: **C2** (depth surface; `c1-measure-v2.py` adds frozen 6/3/9 public-slot
  cardinality + distinctness asserts).
- Receipt under test: `.ufo/evidence/round-36/after/c1v2-at-b455001e.stdout`
  line 17 — `… pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 …
  rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=true`
  (exit file `c1v2-at-b455001e.exit`: `EXIT=0`).

## Independent verification (own code, not the counter)
Probe script: `/fast/scratch/hyaku/tameshi-r36-seats/LabratPanelOrigin/probe.py`
(does not import the frozen counter; re-implements panel enumeration from
committed bytes, strict-count sequential `str.replace` edit application, and
sha256 body hashing).

Commands run (all read-only):
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log -1 b455001e…` →
  measurement commit is the round-36 cold-read refresh commit.
- `git -C … ls-tree -r --name-only b455001e… -- .ufo/evidence/round-35/c1/panel`
  → **exactly 9 `.json` files, no manifest.json** (`manifest.json` exclusion is
  moot; there is none).
- `git -C … show b455001e…:<path>` per panel file + `tools/mutate-and-run.sh`.
- `python3 probe.py` (runner at REV sha256 = pinned
  `a7d3f2dd…`; `panel_json_files=9`, `panel_copies=9`,
  `distinct_body_sha256=9`, `VERDICT … match_v2_receipt=True`).
- `sha256sum` on the three frozen artifacts in the working tree:
  `c1-measure-v2.py` = `9eb8944c…` ✓, `tally-audit-v3.py` = `6188db16…` ✓,
  `mutate-and-run.sh` = `a7d3f2dd…` ✓.

## Observed facts
- `distinct_bodies` (v2 file lines 409–414) hashes `runner_text` after applying
  each copy's `edits`, falling back to hashing `c['file']` if edits fail to
  apply. It counts **distinct post-edit runner-body texts**, not distinct
  behaviors — an accept copy still contributes a body.
- In the deciding run, `pub` comes from `load_copies_rev(lane, rev,
  '.ufo/evidence/round-35/c1/panel')` (lines 296–311) — committed bytes at REV,
  not the working tree.
- My independent pass over the 9 committed docs yields 9 copies (6 `kill`,
  3 `accept` — matching the receipt's `pub_kill=6/6 pub_accept=3/3`) and **9
  distinct body sha256s** with no collisions; no copy's edits failed to apply.
- 7 of 9 copies carry multi-line edits inside `run_regression`'s tally region;
  `comment-esac` (line 1435) and `workdir-branch-swap` (line 1464) are minimal
  single-line mutations. All 9 resulting bodies are distinct anyway.
- `pub_distinct` covers only the public panel; the sealed set feeds
  `ho_distinct` (receipt: `ho_distinct=7`), a separate quantity — the 9 cannot
  have leaked from sealed copies.

## Verdict
**AGREE.** `pub_distinct=9` is exactly `distinct_bodies` = |{sha256(edited
body)}| over the 9 public panel copies at `b455001e`; an independent
recomputation from committed bytes reproduces 9/9 distinct bodies, and the
receipt's per-copy rows account for all 9 slots (6 kill + 3 accept). No
evidence of coincidence (duplicate bodies masked by hash, filename-fallback
inflation, or sealed-set leakage).

## Residual unknowns / caveats
- `distinct_bodies` is a textual-distinctness count, not a behavioral one (by
  design; the frozen target is the r35 receipt's 9). The per-copy `div`/`rc`
  columns in the receipt already cover behavioral ground truth.
- I did not re-execute the full v2 run (sealed set provenance, behavior
  vectors) — out of scope for this single-hypothesis probe; the sealed
  provenance is asserted by `sealed_after_freeze=1` in the receipt.

## Tooling
No installs; stock `git` + `python3` only.
