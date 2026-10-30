# T57D4Rows2 — documentary row review

Axes: semantic calibration; fixing-commit provenance; evidence completeness. Recommendation only; candidate integration remains **UNVERIFIED**, with no admission granted.

## Scope and candidate identity

The current lane `corpus/routed-defects.json` contains only the historical 49 rows; the read query `.defects[] | select(.id == "R53.7" or .id == "R54.2")` returned no output. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:corpus/routed-defects.json` likewise showed only those historical rows. The candidate rows reviewed here are the explicit assembly in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/attack-ledger.json:1583-1606,1673-1691`; these are not represented as integrated lane rows. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR537xR542/` was empty and the filename sweep found no corresponding writer report.

## Findings by severity

### Medium — R53.7: fixed/full-resolution claim unsupported

**Per-id result: unsupported as written.** Candidate status and status_at_base both say `fixed`, citing `19c75588b3c581a0dc84ea87e09d33d88a99ac8e`. Its note asserts that historical round-53 wording survives **only** in immutable records. But `/home/vgpnk/Projects/shokunin/tameshi-shokunin/LOG.md:2491-2493` still states `three read revisions, inputs pinned at C7`. This contradicts the note's exhaustive assertion and leaves the original historical pin claim uncorrected at that reader-facing location.

Original request: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-53-verifier-spotcheck.md:84` asks to restate the round-53 pin claim or re-pin. Candidate evidence `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/integrate/binder.py:142,166-167,183-184` does support separate C0/read_rev and PIN values for the **round-54 successor**, but does not itself repair or accurately restate the round-53 inputs. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54.md:124-126` acknowledges the imprecision and calls this fixed; its explanation likewise describes the successor mechanism, not the actual old pins.

Panel corroboration: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR537R538.md:5-10` returns **open (partial)**, records the remaining LOG assertion and historical ledger discrepancies, and explicitly does not establish that later rows close them. Its counts are prior-seat observations, not reproduced measurements here. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2RepairR536xR537.md:12-16,58-61` also distinguishes fixing-commit tie failure from semantic repair; counter acceptance is not the basis of this finding.

Observed documentary sweep (specialized grep, not a runtime check): `grep(pattern="R53\\.7|inputs pinned at C7|C7.*pin|pin.*C7", path=ABS_LOG;ABS_SCORECARD;ABS_ROUND54_LESSON;ABS_ROUND55_LESSON;ABS_ROUND56_LESSON)` returned LOG.md:2492 and round-54.md:124-126 only. Exact material output: `2492: three read revisions, inputs pinned at C7). Deciding run at 88afa941:` and `124: - **R53.7** ("inputs pinned at C7" was imprecise) — FIXED: the binder records` followed by the separate-read_rev/PIN explanation. The concrete defect is the overbroad full-resolution/only-immutable assertion; successor hardening is supported.

## Supported row

### R54.2 — supported for the lane record; external repair not established

**Per-id result: supported with the candidate's explicit external-residue qualification.** Original item `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-54-verifier-spotcheck.md:110` identifies three differing pointers versus receipt `077d431e`. Fixing commit `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` changes both active SCORECARD claims to `077d431e` and adds ER-R54-2 explicitly superseding all three former pointers, including the fleet report's `097985c1`.

Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb -- /home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md`. Material output: removed `7883e0e5 is the freeze pointer`, added `one freeze pointer ... 077d431e`; replaced measured-close `freeze fe70474d` with `freeze 077d431e`; added `Old: ... 097985c1 in the fleet report. Corrected: one pointer, 077d431e (5 amendments)` with the deciding receipt citation. Command `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin merge-base --is-ancestor 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb 5e3569969b532310d2b8a3d130901757a3df356b` completed successfully with empty output, supporting fixed-at-base provenance.

Current documentary corroboration: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md:2642-2647` and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/after/frozen.stdout:1` (`FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 ...`). Valid re-seat `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ReseatR542R543.md:11-24` agrees **fixed in the lane record**, expressly not certifying external fleet bytes. Original w2 panel `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR542R543.md:9-15` declared its own blindness breach and void verdict; it is not an independent valid contrary panel. No unconditional 'one pointer everywhere including repaired fleet report' conclusion is supported.

## Residual risk / verification gaps

- Candidate rows are available in a local assembly, absent from the inspected canonical ledger and C0b ledger. No installation, final revision or counter acceptance is certified.
- R53.7's historical input discrepancies were not recomputed; their panel numbers remain attributed observations. Finding rests on directly read source text and its mismatch with the candidate note.
- No external fleet-file repair or freshness claim is verified. R54.2 support is limited to the lane's explicit superseding correction.
- LSP device unavailable: reading `xd://lsp` returned `No such tool`. All searches were literal documentary fallback, not semantic caller proof.
- No candidate gates, tests, builds, exploits, external targets, commits, production edits, tool installs or upgrades. Only git object/history reads, source/report reads and the two authorized report writes.

Self-evaluation: accuracy 4/5 (assembly identity disclosed, no runtime proof); completeness 4/5 (both ids covered, external bytes deliberately unverified); clarity 4/5 (lane closure versus external residue separated); actionability 4/5 (R53.7 exact overclaim named); conciseness 4/5 (command evidence adds necessary length). Overall 4.0/5. Highest-impact improvement to the evidence is a candidate-specific documentary restatement of the old pin claim, not a counter pass. User agreement expected because supported and unsupported scopes are explicit.
