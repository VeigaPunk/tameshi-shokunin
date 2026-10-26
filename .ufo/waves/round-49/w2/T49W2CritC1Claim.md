# T49W2CritC1Claim — C1 claim attack

## Result

**No falsification of the measured score found; one provenance/naming discrepancy merits clarification.** This is a probe, not the deciding verdict.

- The requested round-21 monitor command returned `calibration_restraint_score: 8`, `sections_covered: 64`, `sections_total: 64`, `uncovered_headings: []`, and `ledger_present: true` (exit 0). Command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev f181a961ae44061af486f600e5ea257d2baf78f8`.
- The same output reports `shonen.boxes: 4`, all marks `~`, `box3_marked: true`, `box3_ledger_link: true`, `box3_points: true`; the cited box-3 line is `SHONEN.md:9-10`, pointing to `.ufo/evidence/round-21/coldread/ledger.json`. The box remains explicitly a lane assertion / input-keyed monitor only, not an independent promotion verifier (`SHONEN.md:9-10`). Thus the numeric 6→8 is supported as the unchanged monitor's output and the `[~]` policy is not represented as independent proof.
- Ledger has seven entries with `read_rev=9b9b2a016adcf2fab2e0cb1ef89ef78f454b8ec6`, one for each targeted section; each has `class: record`, `verdict: verified-record`, and points to its respective `section-1.json` … `section-7.json` trace (`.ufo/evidence/round-21/coldread/ledger.json`, command: `git show f181a961ae44061af486f600e5ea257d2baf78f8:.ufo/evidence/round-21/coldread/ledger.json`). In each entry's `inputs`, none of `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, or `corpus/README.md` occurs as a live input. Where those records are cited, the trace receipt places them in `records_via_blob` instead (e.g. refresh receipt for section 1, `refresh-receipts.json`, command `git show f181a961ae44061af486f600e5ea257d2baf78f8:.ufo/evidence/round-49/coldread/refresh-receipts.json`).
- Trace provenance is consistent with trace-inputs receipts: `section-1.json:2` has schema `tameshi-trace-inputs-v1`; `:8-20` records scratch root/revision and exit 0; `:31-38` has the hashed inputs. The refresh receipt records its reader script and section-specific direct/record inputs. This supports the claimed trace shape, though the receipt's captured read command is an inline Python command (`section-1.json:3-13`), rather than an argv spelling of `tools/trace-inputs.py` itself.
- `reads.json` has 94 rows, schema `tameshi-r49-reads-v1` (`.ufo/evidence/round-49/c1/reads.json:1-4`; `git show ...:.../reads.json`). Every actual `T49ReadNN` seat named by the seven ledger entries appears in `rows[].reader`; however the additional section-owner names (`T49SecRecipe`, `T49SecRestore`, `T49SecMap`, `T49SecPromotion`, `T49SecR12`, `T49SecR13`, `T49SecR14`) do not appear as row readers. They appear only in the ledger `seats` lists. If “seats named” means every listed seat, that test is not met; if it means the actual pointer readers, those are present. Smallest correction: label/partition `seats` into readers vs integration/section owners, or add the missing section-owner read rows only if they actually performed pointer reads. Do not claim those seven names are reads.json readers.
- The SKILL diff command was `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --unified=2 8ca67421111fa354b47b803358391d0b07fc6db9 f181a961ae44061af486f600e5ea257d2baf78f8 -- SKILL.md`. It reports 92 changed lines (46 additions/46 deletions), with hunks within the recipe and restore sections (e.g. lines 141–239 and 375–404 in the displayed candidate context); no evidence from the diff indicated edits outside the seven target sections.
- The frozen C1 counter selftest was run only in its allowed `--selftest` mode and observed `C1_R49_SELFTEST: cases=34 failed=0`. This does not test the claim predicate or durability.

## Counterexample / impacted axis / smallest safe correction

Potential evidence-accounting counterexample: ledger `seats` contains section-owner identifiers not represented among the `reads.json` readers, despite the question's seat-presence criterion. This affects **calibration evidence provenance**, not the observed monitor score. Clarify the ledger role semantics and assert only the actual readers against read rows. The round-21 monitor does credit 64/64 and score 8, but that alone does not establish semantic support of excerpts or durability under record append; the contract explicitly notes those boundaries. No deciding C1 verdict is made here.

## Summary

- Monitor probe: score 8; 64/64 credited.
- Seven new entries use non-record live inputs; record citations are blob-read in trace receipts.
- Reader seats appear in reads.json; seven section-owner seat labels do not.
- SHONEN box 3 is `[~]` with ledger link, explicitly lane-asserted.
- No out-of-target SKILL edits observed in requested diff.
- C1 selftest: 34/34 passed; not a predicate verdict.
