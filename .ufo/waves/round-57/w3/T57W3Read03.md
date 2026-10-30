# T57W3Read03 — cold-read certification

Heading: `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`

- Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`.
- Frozen round-18 sectionizer: start **949**, end **962**, SHA256 `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993`.
- Axes: factual calibration, executable replay, pointer resolution, dated scope, zero source mutation.
- Recommendation: **verified-record**. Findings by severity: **none**.

## Executed sweep and evidence

All commands ran from the detached C0b scratch clone `/fast/scratch/hyaku/tameshi-r57/T57W3Read03/clone`. Source reads were pinned; the lane's uncommitted instruments were not treated as C0b content.

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read03-receipts/sweep.py
bash /fast/scratch/hyaku/tameshi-r57/T57W3Read03/clone/tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r57/T57W3Read03/regression
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read03/clone show 9f1d3c3:tools/mutate-and-run.sh
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read03/clone show 4b7c682:tools/mutate-and-run.sh
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read03/clone show a08e85c5d7f899e8a5992e20517edb1a380d79eb:tools/mutate-and-run.sh
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read03/clone show adf87899c70d616140a81185a8f9acbbdfb30392:.ufo/evidence/round-16/round-gate/runner-regression.txt
```

The driver ran the regression command once, not an additional replay. All commands above exited 0. Full outputs and command records are in the adjacent `T57W3Read03-receipts/` directory (`static.json`, `milestones.json`, `regression.json`, `regression.stdout`; per-leg `sweep.log` and `results.tsv`).

Observed output:

```text
949 962 430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993
standing ledger rows: section 1 + ER-2 = 6; round-16/18 appends = 2; total = 8
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

All ten tables matched their recorded rows, with zero inconclusive verdicts and zero flips. The four named original legs measured 8/10, 8/10, 6/10 and 4/10. Cited historical ranges `9f1d3c3:72-109,511-522` and `4b7c682:597-620` resolve to the documented legs, pins and tables. Historical seven/eight/nine milestones and the C0b ten-leg replay agree.

Read the section end to end, the standing ledger including supersessions, both later-case notes, and relevant README/SOURCES context. Eight means the eight tabular measured rows, not eight current runner legs. The round-52 drift-pins prose supersession does not add a tabular row. Cases nine and ten have their own notes. No contradictory section claim found.

## Notes, residual risk and verification gaps

- LSP unavailable (`xd://lsp`: `No such tool`); text searches were navigation only. No semantic reference-coverage claim is made.
- An auxiliary `git show 89722ddb:tools/mutate-and-run.sh` exited 128 (`fatal: invalid object name '89722ddb'`): that ledger value is a runner digest, not a section revision pointer. The C0b-pinned round-16 receipt supplied the seven-leg evidence instead. This is not a finding against the assigned section. The initial sectionizer setup also passed decoded text incorrectly; the successful recorded result uses raw bytes as required.
- One host/toolchain and recorded revisions only; this does not certify current successor gates, saturation, deterministic repeated controls, or other SKILL sections. No resume-continuity or identity-rerouting behavior is specified by this section.
- Sibling Git stores were exposed through scratch symlinks for read-only materialization. Mutants and execution state were scratch-only. No source edits or staged fix; no frozen evidence edits; no installations or PATH changes.

Self-evaluation: accuracy 4/5 (historical evidence is receipt-based, not a historical-runtime re-execution); completeness 5/5 (complete assigned section, pointers, claims, replay and both reports); clarity 4/5 (supporting full transcripts are split across receipts); actionability 5/5 (pinned identity, commands and verdict supplied); conciseness 4/5 (explicit setup failures add length). Overall 4.4/5. Improvements: retain receipt links when binding this record; do not promote its host- and pin-bounded result to a live-gate claim.
