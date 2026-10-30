# T58W2Read03: verified-record

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`
- Section: `## The leg ledger — replay, receipt, and how it is read (round 7, measured)`; SKILL.md lines 949–962.
- Frozen round-18 section sha256: `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993`.
- Axes: factual correctness; executable pointers; calibrated evidence.

## Findings

None in the assigned section. Recommendation only, not admission.

## Executed sweep

`TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W2Read03/tmp bash /fast/scratch/hyaku/tameshi-r58/T58W2Read03/clone/tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r58/T58W2Read03/regression`

Exit 0. Runner sha256: `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`.

```text
REGRESSION_TABLE js-kimi-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_TABLE bash-surface-census: match=10/10 recorded-killed=8 measured-killed=8 survived=2 inconclusive=0 flips=0
REGRESSION_TABLE bash-tsukuroi-census: match=10/10 recorded-killed=6 measured-killed=6 survived=4 inconclusive=0 flips=0
REGRESSION_TABLE bash-mado-verify: match=10/10 recorded-killed=4 measured-killed=4 survived=6 inconclusive=0 flips=0
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

Full executed commands and outputs: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read03-receipts/commands.json`; full replay stdout: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read03-receipts/regression.stdout`. Sectionizer command is included verbatim in commands.json, uses importlib to load the frozen measure.py, and reports `949 962 430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993`.

Historic `9f1d3c3` ranges 72–109 and 511–522 resolve to the four-leg inventory and expectations; `4b7c682` range 597–620 resolves to eight pin/table entries. The standing ledger has eight substantive rate rows: §1=4, ER-2=2, round16=1, round18=1. Round52's drift-pins cell supersession is prose, not an additional rate-table row. Other SKILL.md ledger references preserve the dated/current distinction.

## Residual risk and verification gaps

LSP device unavailable (`xd://lsp`: No such tool); text fallback is not semantic-reference proof. Replay reads sibling pinned git objects through scratch symlinks and executes copies, not live gates. No cross-host or live-gate result claimed. C2 forgery adjudication is outside this one-section reader result; this PASS does not admit C2.

Exploratory instrumentation errors (str instead of bytes to sectionize; broad row selectors) were corrected and are not candidate findings. No tools installed. No lane source edited. Scratch deleted before yield.

## Self-evaluation

Accuracy 4: pinned execution and citation outputs support the result; no cross-host claim. Completeness 4: full assigned section and ten-leg replay covered; LSP unavailable. Clarity 4: commands separated into receipts to keep the report short. Actionability 4: exact candidate/hash and replay command supplied; reproducer requires sibling git objects. Conciseness 4: machine report retains exploratory sweeps for transparency. Overall 4.0. Improvement: keep future exploratory selectors section-scoped from the start. User-agreement check: evidence is explicit and no admission is implied.
