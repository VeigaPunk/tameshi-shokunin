# ReviewPanelCardinality — r37 w1 (panel cardinality, calibration axis)

Reviewer: L1-tameshi-r37-attempt2.ReviewPanelCardinality · 2026-10-24 · read-only git plumbing against the live lane at HEAD `e6185d5f0b63a6963205110cb098f2f1eca27622`. No lane index/jj/`.ufo/state` mutation; no tools installed (none needed).

## Verdict

PASS on the frozen-predicate reading. The nine source specimens re-derive exactly from the pinned r36 source tree, and the committed empty panel is a distinct tree object carrying zero specimen entries. One precision note (INFO) on the literal "zero entries" phrasing; no defect against contract.json.

## 1. Nine source specimens re-derived from the pinned r36 source tree

Pinned rev `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` resolves as a commit and its panel path resolves to the frozen tree:

```
$ git rev-parse d9c496b19371b779ce0eec6dfee1b049b27a3a2d:.ufo/evidence/round-35/c1/panel
4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e        # == contract.json frozen source_panel_tree
$ git ls-tree -r -t 4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e
100644 blob 0907da461a5d78c6c8ef599c4fe45f35e6c69cc6  cfg00-accept-swap.json
100644 blob a078a07c8885e8723e5496f0d90c087dbb5951c5  cfg11-pass-mask.json
100644 blob c2fb6a314ca26ebb970307d3257659ebbe633b72  comment-brace.json
100644 blob ff9965696b1b9e7586452788eb02eabfd48a2e38  comment-esac.json
100644 blob 2850e894a7c8a416afc7b89e7380ae6bd754ea77  comment-names-leg.json
100644 blob 15734910279f895fb2239613b1b587d8c73b0be2  root-keyed-auto-mask.json
100644 blob cac9307d3d4dd720f4637590383f50031535790d  root-keyed-auto-zero.json
100644 blob 113278de2ce89c22cbd068e6c8ccd38a46c39c5f  root-keyed-shape6.json
100644 blob f685dfd75d43046eb52c5e2a65d769044db3bafc  workdir-branch-swap.json
```

Exactly 9 blobs; count and sorted name-set equal `source_specimens` in the committed manifest (`.ufo/evidence/round-37/control/empty-panel/manifest.json`, 9/9, no diff). Content re-derived as sha256 per blob:

| specimen | sha256 |
|---|---|
| cfg00-accept-swap.json | `c5e5c65257235eb0c9e16dc9227182267bc1d8b85db0c280ab2f556bd3052d46` |
| cfg11-pass-mask.json | `f5da18e89dd5df6175e565149ec28fde2fb357c8b237e6c8a812251fbb6d5c30` |
| comment-brace.json | `8fbf2436fce2172dda4485851b838ec036ee10e242b0dfe7df4c38d08b8e9f33` |
| comment-esac.json | `2f10fb95d209f9c2a9492282424fe764b8c5e1b2e0c5e6d5a81deb6c2e25b276` |
| comment-names-leg.json | `e39a524babea863f918cd531ad834b81ca700b997492933f847ad592ed183a5a` |
| root-keyed-auto-mask.json | `c02c7851934d4f0b2bdf5319eb731da3ecfe302c9fcd86994188e22dd5a86ddc` |
| root-keyed-auto-zero.json | `d6e26e1abb31f31ff8d772724ae3c4ef3e123f7cb956a68c49f3e1134f1295f5` |
| root-keyed-shape6.json | `a8950eb9cd9869ab8e838edaafd64fd3cb2518e1337e2c50370aa81ebfc84768` |
| workdir-branch-swap.json | `920a0e3d565fa7d196ad4b713dc8501463437714f4cab1075a9a2f34d26b6027` |

This matches the frozen counters' own derivation rule (`c1-measure.py@d9c496b:279-294`, `load_copies_rev`: ls-tree names ending `.json`, `manifest.json` excluded per HYGIENE-1).

## 2. Committed empty panel — distinct tree, zero specimen entries

```
$ git rev-parse c2b08d70427921998677c780930c448a4ecefcf1:.ufo/evidence/round-37/control/empty-panel
50e588b6f53b479b71a828c3e3c9cbb1743ae56c        # type: tree (cat-file -t)
$ git ls-tree -r 50e588b6f53b479b71a828c3e3c9cbb1743ae56c
100644 blob dce2e57c9c1372c8f1e9991afb63b4b386d90a9d  manifest.json
entries=1
```

- **Distinct**: `50e588b6…` is a different tree object from the source panel tree `4f3d8af5…` (9 entries) — same identity at replay `panel_rev=c2b08d70427921998677c780930c448a4ecefcf1`, at final evidence rev `32826f37eb40afa6b2497425eecc95e23dacc5ee`, and at HEAD. Ancestry verified: `d9c496b` and `c2b08d70` are both ancestors of `32826f37` (measure.py's `merge-base --is-ancestor` receipt requirement independently holds).
- **Zero specimen entries**: the single entry is the manifest itself; both frozen counters exclude it by name (`manifest.json` never a specimen, c1-measure.py@d9c496b:287), and the committed receipts report `pub_slots=0 pub_distinct=0` (`.ufo/evidence/round-37/control/replay-at-final-control.stdout` → `EMPTY_PANEL_REPLAY: source_tree=4f3d8af5… source_specimens=9 empty_specimens=0 … v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true`; `counter_rev=d9c496b…`). Manifest frozen predicate `expected_specimen_count: 0` holds.
- **No working-tree drift**: `git hash-object` of the working manifest = committed blob `dce2e57c…`.
- Frozen kill-rule receipt intact at final rev: `calibration/after-control-final.stdout` → `C1_R37: unresolved_control_inputs=0 … manifest_ok=1 receipts_ok=1 rev=32826f37… C1_R37_PASS=true`.

## 3. Findings by severity

- **[INFO] Ticket phrasing vs. literal tree cardinality.** "A distinct tree object with zero entries" is literally true only for the canonical SHA-1 empty tree `4b825dc642cb6eb9a060e54bf8d69288fbee4904` (content-addressing makes any zero-entry tree identical to it — a zero-entry tree *distinct from the canonical object* is impossible in this repo, SHA-1, 40-char oids). The ODB census (`cat-file --batch-all-objects --batch-check`, 4569 trees) shows exactly one zero-byte tree, that object; its only referencing commit is `172e82d4f2c1857cd4f31109e06b660d604fa8e7` (empty root tree, empty message, held by `refs/jj/keep/172e82d4…`), which is **not** an ancestor of `32826f37` or HEAD — incidental jj state outside the evidence lineage. The lane's designed committed empty panel is the one-entry tree `50e588b6…` (manifest only), which satisfies the frozen `expected_specimen_count: 0` predicate via the counters' manifest exclusion. No contract text requires a literal zero-entry tree object; no repair indicated.
- No blocking, major, or minor defects found in scope.

## Residual risk / verification gaps

- I verified the replay/counter receipts against committed objects statically (digests, markers, ancestry, tree identity); I did not re-execute the counters (out of this ticket's scope; ExecEmptyPanelReplay covers the live replay, and this note is read-only).
- The specimen digests above are sha256 content re-derivations; the frozen artifacts pin no per-specimen digests to cross-check against (manifest pins names + counts only), so equality of names/blobs to the pinned tree is the binding check — it holds.
