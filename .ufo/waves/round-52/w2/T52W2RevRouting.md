# T52W2RevRouting — kill-rate note + Kagi routing review

Read-only review of the CAND0 ledger supersession block and the wave-1 Kagi routing draft. No lane or Kagi files changed; no counters run and no claim decided.

## Findings

### HIGH — Kagi current HEAD does not match the reviewed pinned code

The routing draft says Kagi HEAD `69b61db4` still has the reviewed script blob. That is false: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse HEAD:corpus/drift-pins.sh` prints `8a2903dc977a1ef6ea0430b21d1760392ccc2827`, while `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh` prints the same blob for the pinned revision (this is the *historical* pin, not the HEAD blob). The draft's statement “the HEAD blob's sha256 is identical” therefore cannot be used as evidence of current live behavior. `git -C ... log -1 --format=%H -- corpus/drift-pins.sh` reports the pinned revision as last path-touch, which also does not establish that it is HEAD's content. Correction: say HEAD is `69b61db46be4ed955994f6f1d1cba522bc5f4e97`, its script blob is `8a2903…`, and the vulnerable lines are verified at the pinned `e64e81b8…` only; inspect the HEAD blob before asserting whether the defect remains live.

### MEDIUM — Kagi draft's proposed `grep -qxF "$3"` is not directly compatible with captured output

Pinned `corpus/drift-pins.sh:400-404` captures the whole command stream, then uses substring `grep -q "$3"`; the content-drift case expects generic `DRIFT` (`:410`), and the file reporter emits `DRIFT   %s %s` with its path at `:158`. `grep -qxF "$3"` against the existing `$out` would not match the emitted `DRIFT   …` line, nor safely express the specific symbol verdict. The alternative per-case regex also needs to match the actual emitted line and isolate or anchor the verdict field rather than permit arbitrary path text to satisfy it. Correct the suggestion to require parsing/filtering the canonical verdict record (or otherwise separating verdict from path-bearing diagnostics), then perform an exact/anchored comparison on that extracted field; add hostile-path and neutral-path regression cases. The oracle flaw itself is grounded at pinned `:158`, `:400`, `:403`; no claim is made about HEAD until its blob is checked.

### LOW — ledger note should describe the measurement without implying a general detection bound

CAND0's final sentence calls the recorded 2/10 “a floor on the gate's detecting power.” The record at `.ufo/evidence/round-51/c2/sweep/sweep.txt:31` is exactly 2 killed / 10, while the neutral-path counter-run cited by wave 1 reports 5/10 (`.ufo/waves/round-51/w1/T51LabSandboxLeak.md:95-102`). The intent is plausible, but “floor” can be read as a bound over arbitrary runs; evidence supports only that the recorded defect-id-path run measured 2/10 and that the separate neutral-path probe measured 5/10. Suggested exact replacement: “so the recorded defect-id-path run measured 2/10; a separate neutral-path counter-run measured 5/10.” The rest of the supersession numbers/pointers checked against the supplied receipts: 10 defects, 2 killed, 8 survived, 0 inconclusive, 20%; leg 10 at `after/c2.stdout:10`; regression 10/10 at `:22`; case-10 entry path is correct. The draft's claim that the suite itself “reported” 13 cases should remain scoped to the recorded `sweep.txt:6` receipt, not generalized to a later revision.

## Commands / evidence

- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse HEAD` → `69b61db46be4ed955994f6f1d1cba522bc5f4e97`.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse HEAD:corpus/drift-pins.sh` → `8a2903dc977a1ef6ea0430b21d1760392ccc2827`.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh` → same historical blob ID `8a2903…`.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin log -1 --format=%H -- corpus/drift-pins.sh` → `e64e81b8…`; path-touch is not a HEAD-content proof.
- Kagi pinned source lines: `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh`; relevant source ranges correspond to lines 158, 400-410.
- Ledger receipt: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show bcba8924894216268afc4171f06eb8c28e912b46:corpus/knowledge/fleet-kill-rate-ledger.md` (candidate block at end); recorded numbers at `.ufo/evidence/round-51/c2/sweep/sweep.txt:6,31` and `.ufo/evidence/round-51/after/c2.stdout:10,22`.

## Summary

- Correct the Kagi draft: the asserted HEAD blob identity is not established; actual HEAD tree blob differs from the cited historical blob.
- Do not recommend `grep -qxF "$3"` on the existing combined output; compare an extracted canonical verdict field instead.
- Ledger counts and leg pointers match receipts; rephrase “floor” as a result scoped to the two observed runs.
- No code changed; no counters run; no claim decision.