# T58W2Read14 — cold read

Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`

Section: ## Live-tree re-pin and entry-command monitor — round 17 (1857–1888)

SHA256: `6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac`

Verdict: **gap-minor** (recommendation only).

## Findings — minor

The section’s recipe-3 registry replay exits 1 at C0. Isolated retries establish two persistent failures:

- `sources-census`: expected 0, got 1; `no-id-or-path-cite: S280 corpus/knowledge/scratch-root-contract.md (Errors.html)`; `SOURCES_CENSUS: VIOLATIONS`.
- `verify-round15`: expected 0, got 1; `registered-tool-source-pin: FAIL` for `tools/context-capture.py`, observed `831b781054d701d7347df62c4044eb274a775967aaf0ce3d49bef4056b111d8d`, pinned `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`.

Full commands and literal output are in the adjacent JSON and receipts. The monitor honestly reports differences; these outcomes do not satisfy their registered expectations or the section’s re-pin/supersede discipline.

## Sweep and calibration

- Read the entire assigned section at C0, lines 1857–1888. Frozen sectionizer hash computed from git show bytes, not reimplemented.
- Disposition before reproduces exit 1 with producer_before; after reproduces exit 0, effective=11 and superseded=1; text mode emits all three HISTORICAL records. Historical guard selftest passes 66/66, including detached-anchor, tree-id, dangling, shallow, replace-ref, GIT_DIR, forbidden/unneeded/uncommitted cases.
- First registry run started before scratch sibling links existed, so mutate-and-run-regression and mte-interop-check had setup failures. These are NOT findings: both held in isolated replays after read-only sibling symlinks were installed. The two reported rows failed again after that repair.
- S061 is retained historical source with S076 correcting its paragraph anchor; this is stale-but-true, not a false claim. Cited evidence-disposition.py line ranges still resolve to the claimed logic and fixture.
- LSP unavailable: reading xd://lsp returned No such tool. Used literal search and source reading; no semantic-LSP proof claimed.
- Residual risk: no independent formal proof of the broad every-lane-tool GIT_* scrub assertion; source inspection and registered/selftests support the named paths. No resume/rerouting/saturation behavior is introduced by this section.
- No tools installed. Scratch deleted before yield.

## Executed commands

- `python3 -c "import importlib.util,subprocess; p='/home/vgpnk/Projects/shokunin/tameshi-shokunin'; s=importlib.util.spec_from_file_location('m',p+'/.ufo/evidence/round-18/measure.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); raw=subprocess.check_output(['git','-C',p,'show','8063d0a551fc5b3cb5a2d397da7353af53444534:SKILL.md']); sec=next(x for x in m.sectionize(raw) if x['heading']=='## Live-tree re-pin and entry-command monitor — round 17'); print(sec['start'],sec['end'],sec['sha256'])"` → 0
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --dispositions /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/.ufo/evidence/round-18/dispositions-before.json --json` → 1
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --dispositions /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/.ufo/evidence/round-18/dispositions.json --json` → 0
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/evidence-disposition.py --selftest` → 0
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/evidence-disposition.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --dispositions /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/.ufo/evidence/round-18/dispositions.json` → 0
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/registry-check.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534` → 1
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/registry-check.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --only mutate-and-run-regression --only sources-census --only verify-round15 --only mte-interop-check --json` → 0
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/registry-check.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --only mutate-and-run-regression --json` → 0
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/registry-check.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --only sources-census --json` → 1
- `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone/tools/registry-check.py --root /fast/scratch/hyaku/tameshi-r58/T58W2Read14/clone --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --only verify-round15 --json` → 1

## Self-evaluation

Accuracy 4/5: literal receipts distinguish persistent failures from initial missing-sibling setup errors. Completeness 4/5: full section and recipes covered; broad environment claim remains source/selftest-supported rather than exhaustively proven. Clarity 4/5: adjacent JSON preserves long diagnostics. Actionability 4/5: exact two row failures identified. Conciseness 4/5: raw command output retained separately.
