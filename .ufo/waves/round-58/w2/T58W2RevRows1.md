# T58W2RevRows1 — R50/R51 row re-verification

Candidate `8063d0a551fc5b3cb5a2d397da7353af53444534`; base `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Axes: calibration, provenance, evidence honesty.

## Findings (medium)

1. **R51.5 disagrees:** `corpus/routed-defects.json:1200-1226` marks fixed although only a staged handoff and lesson assertion exist. Canonical fleet `.ufo/reports/round-58/tameshi.md` is absent (git cat-file exit 128; worktree absent). The assessment itself says the canonical report omits the finding. Lesson `round-58.md:88` additionally says both lines 400/403 grep; pinned kagi source has output capture at 400, grep only at 403. Keep open until actual filing; correct the line claim.
2. **R51.6 disagrees:** `corpus/routed-defects.json:1229-1245` cites current round-58 Gate. Original `round-51.md:5-12` remains opened/touched-only and base→C0 diff is empty. Current candidates do not reconstruct old rejected candidates/reasons. Assessment itself says future practice only. Keep open or append actual historical correction.

## Per-row result

| ID | Base → installed | Review | Evidence |
|---|---|---|---|
| R50.1 | fixed → fixed | agree | Agree fixed at base and C0: S022 is mined with used-by path; round-51 lesson logs queued -> mined; round-51 no-harm explicitly replaces the population pin by the freshness score floor. |
| R50.2 | fixed → fixed | agree | Agree fixed at base and C0: both pbt-staged-id and shrink-case have substantive SKILL registry rows including kind, invocation, exit 2, selftest, pinned values and write scope. |
| R50.3 | fixed → fixed | agree | Agree fixed at base and C0: appended round-51 table explicitly supersedes the old coverage table, with F6 held round 50 and F10 held round 49. |
| R50.4 | open → open | agree | Agree open at base and C0: compound carried successor-counter/open-ledger debt remains explicitly preserved in newest Planned round 59; no claim that historical seven items are discharged. |
| R51.1 | fixed → fixed | agree | Agree fixed at base and C0: registry expects ten legs; pre-registered round-52 tools scope allows registry edit; committed probe names bcba8924894216268afc4171f06eb8c28e912b46 and isolated registry receipt reports held=1/1 EXIT=0. Historical receipt inspected, not rerun live interop. |
| R51.2 | fixed → fixed | agree | Agree fixed at base and C0: ten ledger legs and TMPDIR runner scope corrected; cited runner pointers resolve to relevant behavior; follow-on fresh-reader rekey commit 7fa9a5e0104bc181872401547987d6744f3b570d precedes base. Fix spans commits; single keyed excerpt is not the sole semantic evidence. |
| R51.3 | fixed → fixed | agree | Agree fixed at base and C0: appended correction names T51W2Read20, replaces code-written zero with seven located findings, identifies old ledger entry, and retains original history. Incidental first heading excerpt was not used as substantive proof. |
| R51.4 | open → open | agree | Agree open at base and C0: fleet-bound classification landed but compound item also requires missing round-51 C3 mutation attack; current Planned paragraph carries joint debt. No new discriminator receipt was supplied by row. |
| R51.5 | open → fixed | disagree | Disagree current fixed; agree base open: round-58 lesson/staged handoff are not evidence that the owed cross-domain item was filed in the canonical fleet report. The report does not exist at inspection, and row assessment itself says the next canonical report omits it. Lesson also falsely labels line 400 a grep; pinned source makes it output capture. |
| R51.6 | open → fixed | disagree | Disagree current fixed; agree base open: historical round-51 Gate still contains only opened/touched rows. Fix writes current round-58 Gate with current candidates, not a retrospective round-51 correction. Installed assessment explicitly says later Gate improves future practice only. |
| R51.7 | fixed → fixed | agree | Agree fixed at base and C0: appended round-52 supersession specifically replaces drift-pins unmeasured cell, identifies case 10 and quotes recorded 2/10 sweep plus ten-leg regression. |
| R51.8 | open → open | agree | Agree open at base and C0: deciding-run still uses last-touch commit ancestry rather than receipt-content freeze binding; no demonstrated failure discriminator is provided; newest Planned carries debt. |

## Executed sweep and output

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevRows1-receipts/audit.py /fast/scratch/hyaku/tameshi-r58/T58W2RevRows1/clone
R50.1 structural=None base=fixed now=fixed planned=False
R50.2 structural=None base=fixed now=fixed planned=False
R50.3 structural=None base=fixed now=fixed planned=False
R50.4 structural=None base=open now=open planned=True
R51.1 structural=None base=fixed now=fixed planned=False
R51.2 structural=None base=fixed now=fixed planned=False
R51.3 structural=None base=fixed now=fixed planned=False
R51.4 structural=None base=open now=open planned=True
R51.5 structural=None base=open now=fixed planned=False
R51.6 structural=None base=open now=fixed planned=False
R51.7 structural=None base=fixed now=fixed planned=False
R51.8 structural=None base=open now=open planned=True
```

The frozen judge accepts all 12 mechanically; independent semantic review rejects two fixed claims. All nine fixed rows have an actually introduced keyed witness, with full ancestry, excerpts, lengths, ACK_WORDS and base checks in receipts. Fix-revision and follow-on re-key commits precede base where claimed. Current Planned round 59 carries R50.4/R51.4/R51.8, but omits the two disputed fixed rows.

## Evidence and limits

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevRows1-receipts/audit.py`: reproducible sweep; `commands.json` preserves command/output; `audit-results.json` includes full row statements and base/C0 snippets.
- `semantic-deltas.json`, `independent-witnesses.json`, `historical-obligation-diff.json` preserve commit and substantive evidence.
- `external-report-and-kagi.json` records report absence and actual pinned kagi lines.
- LSP unavailable (`xd://lsp`: No such tool); git/text fallback was used, not presented as semantic reference proof.
- Historical ten-leg interop receipt inspected, not rerun. Open rows are supported as unresolved by their supplied evidence; this is not universal absence proof. Report filing may change after C0. C2 reproduction and runtime/resume contracts are outside this row-only slice.
- No tool installs or lane-file edits. Deleted /fast/scratch/hyaku/tameshi-r58/T58W2RevRows1 before reporting; only required report/receipt outputs remain.

Recommendation only; not an admission.
