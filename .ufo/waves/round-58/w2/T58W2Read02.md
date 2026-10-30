# T58W2Read02 — scoped cold re-read

- Heading: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`
- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`
- Frozen round-18 sectionize: lines 159–273, SHA256 `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da`.
- Recommendation: **verified-record**. No demonstrated false statement or failing recipe command at C0.

## Sweep and evidence

Read the complete assigned section and its taxonomy, restore, source-note and historical cold-reader pointers. The base→C0 `git diff -- SKILL.md` produced no output. All eight directly named file/record pointers resolved; source anchors support the quoted historical counts, pins, token-only kill, costs and caveats.

Executed command (full absolute argv and output retained in `T58W2Read02-receipts/commands.json`):

```sh
bash /fast/scratch/hyaku/tameshi-r58/T58W2Read02/clone/tools/mutate-and-run.sh --target /fast/scratch/hyaku/tameshi-r58/T58W2Read02/pristine.mjs --defects /fast/scratch/hyaku/tameshi-r58/T58W2Read02/js.spec --suite 'node "$MUTANT" --selftest' --workdir /fast/scratch/hyaku/tameshi-r58/T58W2Read02/sweep --timeout 30 --tail 2
```

Exit 0; `CONTROL: GREEN`, `KIMI_CENSUS_SELFTEST: 43/43 pass`, `VERDICT: PASS`; **8 killed, 2 survived, 0 inconclusive, 80%**. D1/D3 27/43; D4 40/43; D5 42/43; D6/D7/D9 41/43; D8 40/43. All denominators remained 43. Full failing labels and suite streams retained under `T58W2Read02-receipts/js-evidence/`.

Uniqueness probe printed ten `old-string-count=1` lines and `all unique (10 defects)`. `cp -p` and `cmp` exited 0. Survivor commands with generated `.pristine.mjs` filenames returned the expected drift exit 1: D2 `+23 more` versus pristine `+22 more`; D10 K2 `frozen=24` versus pristine `25`. Endpoint SHA, size and mtime matched; `MUTATE_RESTORE: OK`.

Runtime: node v26.12.0, Python 3.14.8, bash 5.3.20. Sweep durations and exact command output: `T58W2Read02-receipts/js-sweep.txt`. This is a fresh JS replay, not a new full-page credit or admission.

## Residual risk and verification gaps

- Bash historical facts were re-read, not freshly replayed; cross-host generality remains unmeasured.
- Maintained runner does not itself enforce the recipe's verdict/count-aware adjudication or conclusive-only denominator; these limitations are explicitly disclosed by the recipe, not newly discovered contradictions.
- `xd://lsp` is unavailable; source inspection is textual fallback, not semantic caller proof.
- Initial probe filename guesses failed, were corrected after artifact discovery, and remain transparently in command receipts. Not findings against C0.
- Historical one-off drivers remain unavailable; maintained manifest replay is not recovery of those files.

No tools installed/updated. No source changes. **Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2Read02` deleted before handoff.**

## Calibration self-check

Accuracy 4/5 (historical bash claims checked against records only); completeness 4/5 (one scoped section, no fresh bash replay); clarity 4/5 (long command receipts separate from conclusions); actionability 5/5 (exact candidate/hash/commands retained); conciseness 4/5 (required provenance adds detail). Overall 4.2/5. Improvement: a fresh controlled bash replay would strengthen historical-record corroboration, not change this bounded finding set.
