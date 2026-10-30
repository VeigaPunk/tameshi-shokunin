# T57D4Rows3 — documentary review of R54.3 / R54.4

Axes: semantic correctness, provenance, scope honesty. Documentary review only; no gate/counter execution, tests, mutation, admission, or production edits. No tools installed. LSP unavailable: `read xd://lsp` returned `No such tool`; text reads below are documentary evidence, not semantic-reference proof.

## Finding — medium: R54.4's unconditional `fixed` exceeds the original target

**Per-id result: R54.3 supported; R54.4 unsupported as complete original-item closure (supported as a lane erratum).**

The proposed row is `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR543xR544/rows.json:28-50`: `status=fixed`, `status_at_base=fixed`, commit `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Original R54.4 specifically identifies the report's “Bind and decide” digest, not absence of a correct digest elsewhere: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54-verifier-spotcheck.md:114`. Direct source read:

`read /home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md:116-125`

Observed output at line 122:

> The frozen counter's own bytes at the deciding revision are the freeze-manifest digest `d7749f84…` (c1) and `49280fe5…` (c2) — cite those, not the C1 blobs, which predate amendments 1–5.

The incorrect instruction therefore remains on the routed surface. The candidate itself acknowledges the outstanding fleet-report correction in its line-50 note. The writer report calls it “the open residue” at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR543xR544.md:90-95`.

There **is** a real, correctly attributed lane erratum: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md:2654-2657` gives `49280fe5` → `8528ee85`. The wave-2 panel agrees on `fixed` but its basis only cites this erratum and a counter result, not correction or explicit supersession at the original report: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR544R545.json:4-7`.

Recommendation: distinguish “lane erratum landed” from “original report corrected”; retain the operator-owned residual and do not use an unqualified fixed status as evidence that the named report now reads correctly. This is a documentary recommendation, not an admission decision. Ownership limits explain the residual; they do not establish its repair.

## R54.3 — supported, including the cited commit

Original item: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54-verifier-spotcheck.md:112`. The receipt directly prints `total=13`: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/before/c2.stdout:8`.

Read-only command executed:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --unified=2 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb^ 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- SCORECARD.md
```

Observed diff changes the C2 claim row from `unusable_exit2=3 docs=0 note=0 sources=0 total=14` to `... total=13`, removes the inverted parenthetical, and adds:

```text
+**ER-R54-3 - a quoted total no receipt contains.**
+Old: `total=14` in the C2 claim row. Corrected: `total=13`.
```

The same diff adds ER-R54-4 with the digest correction, establishing that commit's real but narrower contribution to R54.4 too.

R54.3's additional expansion-disclosure concern has documentary support: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w1/T55W1Rev02-receipts/R54.3-spotcheck-commit-attribution.txt:1-14` shows the short `before` at `441c26b`, expanded text at `19c7558`, unchanged text at `077d431e`, and the corresponding minus/plus lines. This supports the writer's correction of the spot-check's specific attribution; it is not a counter-acceptance argument.

The old wave-2 `open` verdict is explicitly void in its recorded receipt (`blind_panel_valid: False`, “Verdicts below are void”): `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR543xR544-receipts/cmd-panel-verdicts.txt:3-9`. The actual wave-3 re-seat returns `fixed`, citing the claim row and ER-R54-3: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ReseatR542R543.json:9-12`.

## Residual risk / verification gaps

- Reviewed the two proposed w3 row objects, not an assumed integrated ledger. Literal search found neither id in the live `corpus/routed-defects.json`; the attack ledger still has a different R54.4 disposition (`declined`). No integration claim is made.
- Historical ancestry/digest recalculations in writer receipts were read, not rerun. The correction commit's actual SCORECARD diff was inspected directly. No gate was executed and no prior PASS was adopted.
- Current candidate integration remains **UNVERIFIED**. Runtime identity, rerouting, saturation, resume preflight, and global 64/64 no-harm are outside this two-row documentary assignment.

Self-evaluation: accuracy 4/5 (historical receipt calculations not independently rerun); completeness 4/5 (integration outside scope); clarity/actionability/conciseness 4/5 each (scope distinction is necessarily explicit). Improvement priority: a named original-report supersession/correction would remove R54.4's ambiguity. Would the user agree: the output separates observed repair from remaining stale text without inventing a pass.
