# T57D4Rows5 — documentary row review

Axes: factual status support; commit-to-remedy support; evidence provenance; zero production mutation.

Scope: R54.8 and R54.9 only. Documentary/source reads and read-only git object inspection; no gate, counter, test, build, exploit, fixture, external target or additional runtime executed. No admission recommended. No tools installed. LSP device unavailable (`read xd://lsp` returned `No such tool`); text searches below are literal discovery, not semantic proof.

## Findings, by severity

### HIGH — R54.9 `fixed` is unsupported: the cited commit changes the population rather than correcting the entry count

Candidate: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553/stage/corpus/routed-defects.json`, row R54.9, inherited from `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w1/T57W1ScribeItemsR54x8to10/rows.json:35-59` and the w2 repair row. It claims `fixed` at `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` and uses “other 80 staged entries” plus `staged=81` knowledge files as evidence.

Observed command:

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=oneline 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- corpus/lessons/round-54.md .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`

Output includes the actual change: `- The other 84 staged` becomes `+ The other 80 staged` (both refer to `merge/tameshi` entries). It also appends the R54.8 SUPERSEDED block. Thus the hash genuinely identifies the edit, but does not prove its arithmetic correct.

Documentary output from `read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w2/T55W2RevRound54Wording-receipts/staged-count.stdout:1-29`:

- `entries = 86`; kinds: 81 new-file, 4 amendment, 1 folded-into-canonical.
- Knowledge `.md` files: 81; the round-53 adopted entry is still present.
- Entry arithmetic: `86 entries, round 53 adopted 1 -> 85 unadopted; minus the 1 named in round 54 = 84`.
- File arithmetic: `81 .md files; minus the 1 named in round 54 = 80`.

The unsupported step is treating the latter as the former. This exact regression is documented HIGH at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w2/T55W2RevRound54Wording.md:370-377`. The independent panel returns `open`, with this reason, at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR548R549.json:12-15`. Its adjudication sweep receipt `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR548R549-receipts/r54-9-regression-adjudication.txt:1-11` reports no adjudication in the searched lane records; the two staged-related resolutions concern mutability/freezing, not population semantics.

The wave-number half is supported: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md:2694-2696` records reviewers=5, attack=21/76, seats=76 (27.6%); the panel command/output log independently records those values at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR548R549-receipts/00-consolidated.txt:64-68`. Partial numerical repair does not support whole-row closure. Recommendation: retain open until the staged-population discrepancy is adjudicated or corrected with population-specific wording and evidence. Counter admissibility is not the basis of this finding.

## Per-id disposition

### R54.8 — candidate `open`: SUPPORTED under the original item's literal remedy

Original `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54-verifier-spotcheck.md:122` requires both seat supersession and a correction to the named round-54 lesson. The candidate accurately distinguishes the completed seat annotation from the missing round-54 lesson record. The observed git diff above adds the annotation but does not add an incident correction to round-54.md. The current lesson ends at line 135; candidate `after_patch` line 139 and its `<full hash ...>` are proposals, not landed evidence.

The panel's own existing command/output log at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR548R549-receipts/00-consolidated.txt:36-39` reports zero incident mentions in the named lesson; `:47-62` locates the replacement record in round-55.md and SCORECARD. Current source reads agree: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md:332-343` withdraws the authority claim and the fabricated-turn characterization; `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-55.md:62` records the incident. The instruction's historical existence is reported evidence here, not newly verified against host history.

Panel disagreement is explicit: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR548R549.json:7-10` says `fixed` only with the caveat that the named lesson remains silent, accepting the next-lesson errata convention. That convention may justify a separately explained disposition, but does not demonstrate the literal “append a correction to both” request was completed. No claim that the incident is entirely unrecorded is supported. Commit 9cf0146 semantically supports the partial correction, not an additional round-54 lesson patch.

### R54.9 — candidate `fixed`: UNSUPPORTED

Use the HIGH finding above. Recommended semantic status: open. The cited hash supports an actual edit and the wave half, but not the staged-entry conclusion.

## Candidate boundary and verification gaps

At the supplied C0b, neither assigned row is present in `corpus/routed-defects.json`. Observed read-only sweep:

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -n -e R54.8 -e R54.9 adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/routed-defects.json`

Output: none; exit 1. The live JSON selection likewise returned no rows. Therefore the per-id judgments above concern the located staged candidate, not a claim that either row is integrated at C0b. No dedicated w3 R54.8/R54.9 writer report was found by filename sweep; the w3 full-ledger stage carries the w1/w2 inherited rows, including a placeholder after_patch hash. Current integration remains UNVERIFIED. Existing reports are evidence of prior observations, not newly exercised measurements. No global saturation, canonical-runtime, rerouting, resume-continuity or no-harm result is established by this narrow documentary review.

Self-evaluation: accuracy 4/5 (historical receipts not rerun); completeness 4/5 (candidate integration unverified); clarity 4/5 (literal vs errata interpretation stated); actionability 4/5 (specific open-status recommendation); conciseness 4/5 (provenance retained). Overall 4.0/5. Highest-impact improvement requires adjudicating the recorded population disagreement, not executing a candidate gate.
