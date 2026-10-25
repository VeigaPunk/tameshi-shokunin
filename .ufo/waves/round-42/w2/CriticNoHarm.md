# CriticNoHarm — round 42 wave 2 (FALSIFY): attack "no axis harmed"

Seat: L1Tameshi42.CriticNoHarm (critic, read-only). Accessed 2026-10-25. Lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin.
Range attacked: base `c77c2b7e` → integration tip `a21845f5`. No counter was run, so no deciding-run rule applies. No scratch clone was made and no tools were installed.

## Findings

### F1 — Only 5 of the 104 changed paths are modified; the other 99 are added
`git diff --name-status c77c2b7e64d2e356381441ecf94abac03e984606 a21845f523b75adbd3e3f7a62af91294db224ad9 | awk '$1!="A"'` →
`M LOG.md`, `M SCORECARD.md`, `M corpus/QUALITY.md`, `M corpus/README.md`, `M corpus/SOURCES.md`. The `--stat` total is 104 files, +11806/−2.

### F2 — Four append-only files are pure byte-prefix appends (survives)
`git diff -U0 B T -- <f> | grep '^@@'`: each file has one hunk, starting after the last base line. The hunks are LOG `-2166,0 +2167,49`, SCORECARD `-1993,0 +1994,27`, QUALITY `-997,0 +998,50` and README `-524,0 +525,15`.
`cmp <(git show B:f) <(git show T:f | head -c $(git show B:f | wc -c))` → `prefix-OK` for all four. This passes QUALITY criterion 35's check (corpus/QUALITY.md:276, numstat shows 0 deleted lines). QUALITY adds only `### Criterion 81` and `### Criterion 82`; no existing criterion was renumbered.

### F3 — SOURCES.md has two in-place edits, both allowed and logged (survives)
`git diff --numstat B T -- corpus/SOURCES.md` → `10 2`. The hunks are at `@@ -12 +12` (S001), `@@ -123 +123` (S153), `@@ -124,0 +125,4` (S155–S158 appended) and `@@ -440,0 +445,4` (footer, a literal append that deletes no line).
- I split each row on pipes and compared every cell. Only the `used-by` cell changed in S001 and S153; every other cell is byte-identical (`identical-except-used-by`).
- The rule allows it: /home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-50 says "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson."
- The log is present and exact: corpus/lessons/round-42.md:89-92. The old and new cells match `git show B|T:corpus/SOURCES.md` for both rows.
- This has precedent: SOURCES.md deletions in round 41 (`baa18b7`, del=2) and in about 25 earlier round commits.

### F4 — No closed round's evidence changed (survives)
`git diff --stat B T -- '.ufo/evidence/round-[0-9]*' '.ufo/waves/round-[0-9]*' ':!.ufo/evidence/round-42' ':!.ufo/waves/round-42'` → empty.
The supersede files (`.ufo/waves/round-42/supersede/round-41-residual-receipt.json` and `round-20-outcomes.json`) are additions. Whether they are semantically valid as repairs is the C1 critics' question, not this seat's.

### F5 — Criterion 80 is not triggered, and no pin is torn (survives)
Criterion 80 (corpus/QUALITY.md:967-973) applies when a round "changes a tool's or a counter's bytes".
- `git diff --name-status B T -- tools '*measure*.py' | awk '$1!="A"'` → empty. No tool or counter was modified; `tools/write-path-census-v4.py` is new.
- Pin sweep: I took the base sha256 of each modified file and ran `git grep -F <first 16 hex>` over the contracts, counters, SCORECARD.md and corpus/ at base. All five files have zero pins.
- At the tip, the whole repo has only two hits. `.ufo/waves/round-41/w1/ExecRowFormat.md:54` quotes the README digest and `.ufo/waves/round-41/w1/ScoutRegistry.md:74` quotes the SOURCES digest. Both are closed-round seat observations, not contract fields, capability rows or registry anchors, so they are outside criterion 80.
- Counter pins held from freeze to tip: `sha256` of `calibration/measure.py` is `9782a5a0…` and of `census/measure.py` is `3c3727ec…`. Both match `claims.C1.counter_sha256` and `claims.C2.counter_sha256`.
- C2's `V3_SHA`/`V2_SHA` constants (census/measure.py:67-68) held in the labelled pre-run: `.ufo/evidence/round-42/prerun/c2-at-5f739acf.stdout` shows `v3_sha_ok=1 v2_sha_ok=1`.
- Registry snapshot anchors: `cd .ufo/evidence/round-42/sources && sha256sum -c sha256.txt` → all 5 files OK. Their byte sizes (12155, 20845, 328434, 2988) match the S155–S158 anchor cells.

### F6 — The strongest counterexample: the frozen contract changed after the freeze (survives, as a designed slot)
`git diff --name-status 322b5cd3 a21845f5 -- .ufo/evidence/round-42/contract.json` → `M`, numstat `38 1`. The one deleted line is `"post_freeze_amendments": []`; the slot is now filled with P1–P4.
- A semantic compare that removes `post_freeze_amendments` from both sides gives `contract equal outside post_freeze_amendments: True`.
- All four amendments are `before_data: true` and `rule_changed: false`.
- The frozen contract's digest `437afc7d…` is quoted only in wave-1 seat reports (`ReviewContract.md:40`, `MutC1SelfPin.md`), not in any counter.
- Both counters read their pin from the contract at the freeze commit, not at REV: calibration/measure.py:369 `Repo(lane, freeze).read(CONTRACT_REL)` and census/measure.py:367 `show(lane, freeze, CONTRACT_REL)`. The amendments therefore cannot move `self_pin` or the predicate.
- Residual tradeoff, not a defect: `.ufo/waves/round-42/w1/ReviewContract.md:40` says "no post-freeze amendment". That was true when the seat ran, but it is now stale against the tip.

## Impacted axes
Calibration and depth: neither is harmed by a pin break, an in-place append-only edit or a closed-evidence change.

## Smallest safe correction
None required. Optional: a reader-facing note that `ReviewContract.md:40` predates P1–P4.

SURVIVES
