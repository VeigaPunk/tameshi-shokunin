# X06 — disposition anchor guards

## Axes

- **Depth:** use one authoritative committed anchor for both v2 provenance guards.
- **Calibration:** discriminate JJ lane state, unbound JJ workspaces, and detached registry-check clones; retain the annotated-tag and symlink-mode survivor falsifiers.

## Scoped implementation

Staged `tools/evidence-disposition.py` from `183f87b899e6cae46be98d251cbc87fb5118f6ca` at `.ufo/waves/round-18/staged/tools/evidence-disposition.py`; executable mode is `755`.

- `:460` computes one anchor label and commit per evaluation. `lane.branch` wins; otherwise an attached `refs/heads/*` is used. An unbound `.jj` workspace fails with `historical_input_unavailable`. An unbound detached non-JJ harness uses checked-out `HEAD` only if a local or remote-tracking ref contains it.
- `:528` checks G3 exact-commit identity and ancestry against the anchor commit; `:601` checks G2's live bytes against the same anchor tree. `:1622-1630` resolves the anchor once and passes it to both guards.
- Selftest additions exercise tag-object refusal (`:2850`), symlink-mode refusal (`:2881`), JJ with `lane.branch=master` (`:2190`, `:2213`), unbound JJ refusal (`:2863`), remote-only registry clone admission after a later tool move (`:2869`), and detached HEAD with no containing ref (`:2875`).

## Verification evidence

Sandbox clone: `/tmp/tameshi-r18w1-X06DispositionGuards-ZcTPFc/clone`, commit `135e84b` on branch `master`. The clone contains committed staged `tools/evidence-disposition.py`, staged `tools/bash-witness-study.py`, and both round-18 manifests. The sandbox wrapper ran with an isolated environment and no network.

- `/tmp/tameshi-r18-L1-sbx.sh /tmp/tameshi-r18w1-X06DispositionGuards-ZcTPFc /tmp/tameshi-r18w1-X06DispositionGuards-ZcTPFc/clone python3 tools/evidence-disposition.py --selftest` — **exit 0**, `SELFTEST: PASS (63/63)`; all 63 case lines passed.
- Same wrapper, `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json` — **exit 0**, `EVIDENCE_DISPOSITION: clean exit=0 expected=12 effective=11 superseded=1 passed=11 failed=0 findings=0`. Retained historical hashes: bash-witness `49e9e5e2…`, mutate-and-run `75ed934d…`, pin-disposition `29725397…`.
- Same wrapper, `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json` — **exit 1**, `EVIDENCE_DISPOSITION: failed exit=1 ... findings=1`; the finding is `expected_contains_missing` for `producer_before`.
- Base-versus-staged JJ acceptance witness via `/tmp/tameshi-r18-L1-sbx.sh ... python3 /tmp/tameshi-r18w1-X06DispositionGuards-ZcTPFc/jj-witness.py` — driver **exit 0**. Base 183f87b bytes: **exit 2**, `historical_input_unavailable`, detail `rev 72735d070880f31f25a5af3828e5748a7adc08da is not an ancestor of HEAD`. Staged bytes on the same fixture: **exit 0**, `clean`, no findings.
- Sandbox facts: `bwrap --version` — exit 0, `bubblewrap 0.13.1`; `jj --version` — exit 0, `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`; `git rev-parse --short HEAD && git symbolic-ref --short HEAD` in the clone — exit 0, `135e84b` / `master`.

No tool was installed or updated. No Git write occurred in the lane repository; clone commits and JJ/Git fixtures were confined to `/tmp`. LSP was unavailable in the exposed tool inventory.

Verdict: **holds** — shared anchor behavior, survivor kills, JJ base/staged contrast, selftest, and both real-manifest outcomes were observed.