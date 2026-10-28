# T56W2CritDoNothingC2 — C2 do-nothing control (critic seat, wave 2)

Round 56 wave 2 · lane `tameshi-shokunin` · content commit C0 = `c0137451f5b7f22d65f748fc69f1b181f55e1378` (lane HEAD, clean tree) · 2026-10-28.
Attack: build the cheapest trees that skip C2's claimed work and score each with the frozen counter in scratch clones at C0.

## Instruments (receipts: `T56W2CritDoNothingC2-receipts/instrument-hashes.txt`)

- `.ufo/evidence/round-56/c2/measure.py` sha256 `915580190cb1…ed6a` — the live **amended** counter (contract amendment 1 re-froze the instruments after commit `21eb3c6`; the goal header's `c3e2ca9f` is the pre-amendment freeze). This is what `deciding-run.sh` extracts at REV and runs, so it is the counter that matters; the freeze-era counter was cross-run once for comparison (v2 receipt).
- `tools/receipt-revision-gate.py` sha256 `c60772ceb0ce…69ac9` (bytes at C0), `control/frozen-surface.paths` sha256 `46c93f105b61…f7d8`.

Method: `git clone --shared` into `/fast/scratch/hyaku/tameshi-r56/T56W2CritDoNothingC2/<variant>`, `checkout --detach c0137451…`, minimal edit, `git add -A`, `rev-parse --show-toplevel` asserted equal to the fixture dir before every commit, then `measure.py --lane <clone> --rev <clone sha> --work <empty dir> --explain`. No lane production file and no frozen instrument was touched. No tools installed.

## Results

| # | Tree (on top of C0) | Verdict line (tail) | Arm moved | `C2_R56_PASS` |
|---|---|---|---|---|
| v1 | docs only — **nothing added**: all four docs cells are already in C0 (commit `c013745`, 614 insertions incl. SKILL +13, QUALITY +62, SOURCES +4, knowledge note +206, registry +33) | `own=own-receipts-missing docs=4/4 total=1 … false` | none vs C0 (vs freeze-era before: arm6 0/4→4/4, banked by C0) | **false** |
| v2 | two 79-byte stubs `control/controls-{a,b}.stdout`: `rev=c0137451…` + `CONTROLS_A: 7/7 as pre-registered` | `own=PASS docs=4/4 total=0 … true` @ `38895e5c3096` | arm5 own: missing→PASS | **true** |
| v3 | real round-54 slice (CTL_POS_c1) copied to both own paths, its single `rev=077d431e6996` rewritten to C0 | `own=PASS docs=4/4 total=0 … true` @ `b60a76ff7ca8` | arm5 own: missing→PASS | **true** |
| v4 | red-before receipts deleted (slice, sidecar, r54-surface.paths) | `red54=slice-missing … total=2 … false`, exit 1, no traceback | arm2: refuse→missing | false |
| v5 | bonus: red slice doctored in place (`rev=`→C0), original sidecar kept | `red54=RECEIPT_DIGEST_MISMATCH … total=2 … false` | arm2: hit→**miss** (correct) | false |
| v6 | weakest docs text (4 one-line cells, receipts/v6) | `docs=4/4 total=1 … false` | none (floor confirmed) | false |

## Answers to the item

1. **Docs-only, no control receipts (v1).** At C0 this variant is the null edit — C0 itself banks the entire docs arm (`docs=4/4` with zero new text). Verdict: `total=1`, fails only on arm5. Does not reach PASS.
2. **Two stub receipt files (v2).** `C2_R56_PASS=true` at clone commit `38895e5c3096`. Which arm moved: arm5 only. Why it passes: the `control` role requires only ≥1 *resolvable* `rev=` token that is ancestor-or-equal of certified; the `positive` role accepts the certified revision **or a content-identical one on `frozen-surface.paths` — and that surface does not list `control/controls-*.stdout`**, so any purely additive tree is "content-identical"; arm5 passes no required-line regex; and the `.sha256` siblings are copied **only if present** (sidecar-less receipts are accepted with no digest check at all). No control was ever run; 158 hand-written bytes.
3. **Round-54 slice, `rev=` rewritten (v3).** `C2_R56_PASS=true` at `b60a76ff7ca8`. A receipt actually produced by round 54's run, with one token rewritten, passes as *this* round's own control+positive evidence. Same arm5, same mechanism.
4. **Red-before receipts deleted (v4).** The "arms error instead of refuse" hypothesis is **false**: the counter names the missing arm (`red54=slice-missing`), keeps standing, exit 1. Deletion cannot reach PASS — and the deleted files are on the frozen surface, so the deciding run would additionally flag `FROZEN_UNCHANGED=0`.

**Weakest text that still scores `docs=4/4`** (v6, verified): one line in `corpus/QUALITY.md` containing `tools/receipt-revision-gate.py` and `RECEIPT_REV_CONTENT_DRIFT`; a knowledge note whose pre-`---` head is `source: S279` / `verified-at: …` / `recheck: …` (any *mined* S-number — S279/S280/S281 are `mined`, S282 `rejected` at C0; the counter never checks the row is about the note); `## Standing rules` containing the bare string `receipt-revision-gate`; a one-line `tools/registry.json` naming the gate path plus any three refusal codes. All four cells are substring checks — none requires truth, provenance, or a reader. **Enough?** Not alone (v6: `total=1`); but entirely enough once combined with the 158 stub bytes of v2 — which is precisely the do-nothing pass. `docs=4/4` is necessary, trivially forgeable, and not the load-bearing weakness; arm5 is.

## Critic findings

- **F1 (defect, fixable): arm 5 is the only digest-unpinned evidence arm.** Arm 2's red evidence is pinned (sidecar copied from REV and verified — see F2), arm 5's own receipts are not: absent siblings are silently accepted. *Smallest safe correction:* arm 5 requires and verifies `.sha256` siblings for both own receipts (new named refusal, mirroring arm 2) and passes the deciding run's `^CONTROLS_[AB]: ([0-9]+)/\1 as pre-registered` shape as a required-line regex. This raises forgery cost but cannot close provenance — computing the sidecar of a forgery is free — so the contract's `cannot_see` note remains true and must stay in the report.
- **F2 (attack that found nothing, sweep shown): red-evidence authenticity holds.** v5 doctored the red slice's `rev=` in place and kept the original sidecar: the gate's `check()` returns codes right after digest/resolve, *before* role/drift logic, so doctored bytes can never produce `RECEIPT_REV_CONTENT_DRIFT`; arm 2 requires that exact code and correctly scored a miss. The kill-rule's "refusal for the wrong reason is a miss" is enforced for red evidence. The asymmetry with arm 5 (F1) is the defect, not arm 2.
- **F3 (boundary, for the L1's report): the deciding run narrows but does not close the do-nothing pass.** It requires the six receipt files to exist (blob, non-empty, last touched after freeze), the `CONTROLS_A/B: n/n` self-consistent verdict lines, and then runs the *same* gate acceptance as arm 5. The v2 stub already matches the verdict shape (the `7/7` denominator is not checked against the actual phase-A emit count); adding two `0` exit files and matching sidecars (~150 more bytes) clears every deciding-run precondition. Genuine mitigation stays outside the counter: the L1 committing `controls.sh`'s actual stdout, and phase A/B actually running.
- **F4 (do-not-fix warning): do not extend the frozen-surface idea to the own receipts.** Adding `control/controls-*.stdout` to the gate's `--paths` surface would refuse the *legitimate* phase-B receipts too (they name PIN and are committed only at REV → drift-by-absence). Verified from `drifted_paths` logic; named so nobody "fixes" F1 that way.
- **F5 (historical note):** the freeze-era counter scored the same v2 tree `docs=3/4 / false` — its SOURCES status-column bug (amendment 1, cells[8]→cells[7]) made the knowledge cell unscorable, so pre-amendment C2 was unreachable in *both* directions. The amendment simultaneously made C2 reachable and made the 158-byte stub sufficient.

**Seat verdict:** the C2 do-nothing control **fails** — a tree that performs none of C2's claimed gate/receipt work reaches `C2_R56_PASS=true` (twice: v2 fabricated, v3 rewritten-borrowed). Whether F1 is judged a fixable defect or the documented `cannot_see` tradeoff is the canonical judge's call; the correction I would keep is arm-5 sidecar + verdict-line pinning, nothing more.

Bounds: fixtures under `/fast/scratch/hyaku/tameshi-r56/T56W2CritDoNothingC2` (removed after receipts were extracted); no mutating git outside fixture clones; `agent://all` never messaged; no installs (nothing needed).
