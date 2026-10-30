# Blind re-seat: R51.5 / R51.6

Axes: calibration, evidence completeness, blindness preservation. Recommendation only: **open / open** under the assignment's cited-surface and filed-report requirements.

## Scope and identity

All repository reads and history commands used `/fast/scratch/hyaku/tameshi-r57/T57W3ReseatR515R516/clone`, a shared clone detached at `5e3569969b532310d2b8a3d130901757a3df356b`. No ledger was opened. No lane git command, alternate runtime, lane mutation, or frozen-path edit was performed. Only the required output artifacts were written into the lane. No tools installed.

The item numbering is positional under `## Routed defects for the lane next round` in `corpus/lessons/round-51-verifier-spotcheck.md:124-133`: item 5 is cross-domain routing and item 6 Gate completeness. The separate inline `R51.5` at lesson line 98 denotes a different mutation-attack issue and is not this assignment's positional item.

`xd://lsp` returned `No such tool`; semantic references/definition/diagnostics were unavailable. Literal searches and committed bytes/history were used, not presented as semantic proof.

## Findings

### R51.5 — open: routing draft is present, report filing is unestablished

The cited requirement at spot-check line 130 is to file the kagi finding **in the next report**. Commit `0de85158dfcc4d100e0c0e6dbcfb35925b48f04b` adds `.ufo/waves/round-52/w1/T52W1ScribeKagiRoute.md:1-9`, which describes the defect and owner. The wave-2 review at `.ufo/waves/round-52/w2/T52W2RevRouting.md:11-13` rejects its direct `grep -qxF` recommendation. `corpus/lessons/round-52.md:15` says the report recommends an extracted verdict field; that assertion is not the report bytes. There is no round-52 report in the allowed clone. Thus partial work exists, but a qualifying filed-report repair cannot be established.

**Verification gap:** the round-52 closure points to a fleet report, outside this seat's permitted clone. This open verdict does not assert that an external fleet report never existed. It refuses to treat a later lesson's claim as proof of the requested fix.

### R51.6 — open: cited historical Gate unchanged

`corpus/lessons/round-51.md:5-12` contains S272/S273 admits and touched rows, with no rejected candidates. The file is byte-unchanged since the spot-check's introduction. `corpus/lessons/round-52.md:12-15` does list rejections for round 52; this is prospective improvement, not a change to the cited defective round-51 section. No withdrawal or qualifying repair to that surface was found.

## Commands and observed output

All following git invocations used `git -C /fast/scratch/hyaku/tameshi-r57/T57W3ReseatR515R516/clone` (abbreviated `git -C "$C"` below; `$C` is exactly that absolute directory).

```text
git -C "$C" rev-parse HEAD
5e3569969b532310d2b8a3d130901757a3df356b

git -C "$C" log --format='%H %s' --diff-filter=A -- corpus/lessons/round-51-verifier-spotcheck.md
ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 round-51 verifier spot-check (integrator, hyaku): non-author admit/reject

git -C "$C" diff ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 HEAD -- corpus/lessons/round-51.md
[empty stdout; successful exit]

git -C "$C" ls-tree -r --name-only HEAD .ufo/reports reports
.ufo/reports/round-1/tameshi.md
reports/r10-aud-t10.md
reports/r11-aud-t11.md
reports/r7-aud-t7.md
reports/r8-aud-t8.md
reports/r8-ver-t8.md
reports/r9-aud-t9.md
reports/r9-ver-t9.md
reports/round-1-calibration.md
reports/round-1-kaika-coldread.md

git -C "$C" log --format='%H %s' ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4..HEAD -- .ufo/waves/round-52/w1/T52W1ScribeKagiRoute.md
0de85158dfcc4d100e0c0e6dbcfb35925b48f04b round-52: wave-1 evidence (36 seats) and wave-2 spec
```

Executed Python derivation through the Python tool, with `root = Path('/fast/scratch/hyaku/tameshi-r57/T57W3ReseatR515R516/clone')`:

```python
raw = (root/'corpus/lessons/round-51.md').read_text()
gate = raw.split('## Gate\n', 1)[1].split('\n## ', 1)[0]
print('ROUND51_GATE_REJECT_LINES', [
    (i, l) for i, l in enumerate(raw.splitlines(), 1)
    if l in gate.splitlines() and 'reject' in l.lower()
])
print('ROUND52_REPORT_EXISTS', (root/'.ufo/reports/round-52/tameshi.md').exists())
```

Observed:

```text
ROUND51_GATE_REJECT_LINES []
ROUND52_REPORT_EXISTS False
```

The full round-51 Gate and the round-52 draft/review were also directly read via ranged file reads. No runtime gate execution was needed for these documentary defects. No code changes or checks are proposed outside this scope.
