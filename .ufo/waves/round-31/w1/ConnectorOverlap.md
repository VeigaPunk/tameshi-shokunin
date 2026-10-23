# ConnectorOverlap — round 31 wave 1 (read-only sibling overlap)

Verdict: no blocking duplicate found. `kumitate-shokunin` is the only sibling with a tracked in-tree checker that re-derives its own SCORECARD tallies (`scripts/proxy-check.mjs`, contract `kumitate-proxy-v1`); its `corpus/knowledge/executable-scorecard.md` is adjacent, lane-specific prior art and should be cited, not copied. `kotoba-shokunin` has two doctest-like verification notes that can serve as format references. Other siblings expose SCORECARD capability/axis tables with command evidence pointers but no found in-tree runner. Tameshi's C1 predicate and 10 capability rows remain lane-local; no production files changed.

Axes: calibration (C1; SCORECARD `| Axis | Score (0–10) |` rows) and depth (guardrail; capability rows). Adjacency is the judged surface.

## Search method

- Siblings: all 20 `/home/vgpnk/Projects/shokunin/*-shokunin` directories except `tameshi-shokunin`.
- `git -C <sibling> grep -nE '^\| (Capability|Axis) \|' HEAD -- SCORECARD.md`
- `git -C <sibling> grep -lnEi 'executable (scorecard|documentation)' HEAD -- corpus/knowledge`
- `git -C <sibling> ls-files | grep -iE 'scorecard|proxy-check|c1-measure|measure'` (excluding `.ufo/` and `reports/`)
- Read-only only: no Git writes, no tool execution, no sibling file edits.

## Table

| Sibling | path:line | Overlap | duplicate / conflict / could serve |
|---|---|---|---|
| kumitate-shokunin | `corpus/knowledge/executable-scorecard.md:1` (with `scripts/proxy-check.mjs`) | Executable re-derivation of SCORECARD terms/axes and `## Axes` cross-check; 17-key stanza grammar, exit 0/1/2/64 | could serve as prior art/pattern; not a duplicate because terms, pins and axes are kumitate-specific |
| kumitate-shokunin | `SCORECARD.md:324`, `:1720` | Axis table and capability table carrying command evidence pointers (`operability`, `coverage:*`) | conflict risk if imported as tameshi rows; cite only |
| kotoba-shokunin | `corpus/knowledge/corpus-integrity-round11.md:1`, `corpus/knowledge/harness-verifier-round10.md:1` | Human-readable half of verifier with commands and expected outputs ("executable" documentation) | could serve as note format; not duplicate content |
| kengaku-shokunin | `SCORECARD.md:774` (also `:860`, `:920`, `:967`) | Capability tables with `Evidence / command` columns | format overlap only; no in-tree scorecard checker found outside `.ufo/` |
| chousa-shokunin | `SCORECARD.md:463` (and multiple later capability tables) | Many `Capability | What it can now do | Evidence pointer | First-working round` tables | format overlap only; no in-tree scorecard checker found outside `.ufo/` |

## Evidence

- `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin grep -nE '^\| (Capability|Axis) \|' HEAD -- SCORECARD.md` returned `SCORECARD.md:324` and `:1720`.
- `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-files | grep -iE 'scorecard|proxy-check'` returned `corpus/knowledge/executable-scorecard.md` and `scripts/proxy-check.mjs`.
- `git -C /home/vgpnk/Projects/shokunin/kotoba-shokunin grep -lnEi 'executable' HEAD -- corpus/knowledge` included `corpus/knowledge/corpus-integrity-round11.md` and `corpus/knowledge/harness-verifier-round10.md`.
- Across all siblings, the only tracked non-`.ufo`/non-`reports` scorecard checker found was `kumitate-shokunin/scripts/proxy-check.mjs`.

## Proposed move

Keep tameshi C1 lane-local. If an executable-doc entry is needed in `corpus/knowledge/`, cite kumitate's `executable-scorecard.md` and kotoba's verifier notes as prior art and state the tameshi-specific command/output contract; do not copy their term sets, pins, or axis mappings. No sibling files should be edited.

## Risks / verification

- Risk: importing kumitate's stanza grammar or term names would create a false second convention and conflict with tameshi's frozen C1 predicate.
- Risk: treating kengaku/chousa capability tables as executable checks would overstate them; their rows are evidence pointers, not demonstrated in-tree runners.
- Verification performed: read-only `git -C` grep/ls-tree/rev-parse and file reads only. No counters, gates, selftests, builds, or production edits were run. Frozen predicate and base prefix condition for C1 remain unchanged.
Report: .ufo/waves/round-31/w1/ConnectorOverlap.md