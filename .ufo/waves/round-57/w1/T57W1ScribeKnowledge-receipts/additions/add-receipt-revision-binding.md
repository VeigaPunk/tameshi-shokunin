
## Errata — round 57 (R56.3 repair, 2026-10-28)

Corrections are additive; the frontmatter and the body above keep their freeze-era wording.

### ER-R57-K1 — the `recheck:` value is now 19/19

The frontmatter `recheck:` line still names the freeze-era `GATE_SELFTEST: 14/14 pass`.
ER-R56-K2 recorded that amendment 1 changed the gate; this block makes the current value
the one the entry runs. The recheck is `python3 tools/receipt-revision-gate.py --selftest`,
which must print `GATE_SELFTEST: 19/19 pass` with exit 0. It does at base `5e3569969b53`
with gate sha256 `c60772ce…0569ac9` (`.ufo/waves/round-57/w1/T57W1ScribeKnowledge-receipts/gate-sweep.stdout`,
last two lines). Where this block and the frontmatter line disagree, this block governs; the
frontmatter line is not rewritten, per the append-only rule.

The gate's exit map and the code each refusal emits are indexed in
`knowledge/gate-row-exit-map.md` (round 57), which measures the same gate at the same revision.
