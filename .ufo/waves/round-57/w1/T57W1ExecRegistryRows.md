# T57W1ExecRegistryRows — C2 registry content (staged)

Item: gate fixtures + 3 `gate` registry rows for `tools/receipt-revision-gate.py`. Nothing was edited in the lane; no lane git mutation. Scratch clone (`--shared`, detached at base `5e3569969b532310d2b8a3d130901757a3df356b`) + throwaway commit `e74e717f` (identity `fixture`, `-C` clone, toplevel asserted) deleted at exit.

## Staged files (L1 copies into the lane; paths relative to `stage/`)
- `tools/fixtures/receipt-gate/accept.receipt` — `VERDICT: rev=5e3569969b532310d2b8a3d130901757a3df356b C2_FIXTURE_PASS=true`
- `tools/fixtures/receipt-gate/drift.receipt` — same line, `rev=c34e2b1486714ad6c1c6cbe706599ddfc9d60d55` (parent of base; only `corpus/lessons/round-56-verifier-spotcheck.md` differs between it and base)
- `tools/fixtures/receipt-gate/drift.paths` — comment + `corpus/lessons/round-56-verifier-spotcheck.md`
- `tools/registry.json` — full new file = base bytes + 3 rows appended (json indent=1 round-trips base byte-identically; verified before appending). Patch: `../registry.json.patch` (`diff -u`, a/ b/ labels, against `git show 5e35699:tools/registry.json`; 83 added lines, kept OUTSIDE `stage/` so it is not copied into the lane).

No SKILL.md, SOURCES, QUALITY, README, knowledge entry touched (NO-HARM: nothing outside the new fixtures + registry.json; `tools/registry.json` is pinned only if a ledger entry pins it — L1 to check).

## Rows (keys match existing gate rows: name, kind, argv, expect{exit,stdout_contains}, timeout_s, source, status, tags)
| name | argv (cwd = clone root) | exit | source |
|---|---|---|---|
| `receipt-gate-accept` | `python3 tools/receipt-revision-gate.py --lane . --certified 5e35699… --receipt tools/fixtures/receipt-gate/accept.receipt:positive` | 0 | `tools/receipt-revision-gate.py@5e35699…:220` |
| `receipt-gate-content-drift` | `… --certified 5e35699… --paths tools/fixtures/receipt-gate/drift.paths --receipt tools/fixtures/receipt-gate/drift.receipt:positive` | 3 | `…@5e35699…:149-152` |
| `receipt-gate-unresolvable-certified` | `… --certified deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --receipt …/accept.receipt:positive` | 2 | `…@5e35699…:190-194` |
All `timeout_s` 60, `status` active, tags `["new-r57"]`. Source lines verified against the base blob: line 220 `return 0 if verdict == 'PASS' else 3`, 149-152 the CONTENT_DRIFT branch, 190-194 resolve + exit-2 return (the gate working-tree bytes equal base: empty `git diff` on the file).

## The three observed exits and exact stdout (receipts: `T57W1ExecRegistryRows-receipts/direct-*.stdout`, `direct-exits.txt`)
- exit 0:
  `GATE OK tools/fixtures/receipt-gate/accept.receipt role=positive revs=5e3569969b532310d2b8a3d130901757a3df356b`
  `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS`
- exit 3:
  `GATE REFUSED tools/fixtures/receipt-gate/drift.receipt role=positive revs=c34e2b14…d55 code=RECEIPT_REV_CONTENT_DRIFT rev=c34e2b14…d55 drift=corpus/lessons/round-56-verifier-spotcheck.md`
  `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED`
- exit 2:
  `GATE: error=unresolvable-certified receipts=1 verdict=REFUSED codes=RECEIPT_REV_UNRESOLVABLE`

## registry-check proof (clone HEAD `e74e717f1989acafd896ad14c0bb56b7b672b011`, `--root <clone> --rev HEAD`)
- `--only receipt-gate-accept`: `ROW … expect=0 got=0 held` · `REGISTRY_CHECK: held=1/1`
- `--only receipt-gate-content-drift`: `expect=3 got=3 held` · `held=1/1`
- `--only receipt-gate-unresolvable-certified`: `expect=2 got=2 held` · `held=1/1`
- `--tag new-r57`: `held=3/3 superseded=0`; all rc 0; no `non_hermetic_argv`. Receipts `registry-check-*.stdout`.
Not run: the full registry (contains a 900 s mutate-and-run row and uv rows) — an unrun check has not passed.

## Risks / notes for L1
- Rows resolve revisions in the clone: `5e35699` and `c34e2b1` must stay reachable (they are base ancestry; fine after integration since the integration commit descends from base).
- The `--lane .` form means the gate is run against the registry-check clone, not the live lane.
- The `:ROLE` argument is `positive`; a `verdict` role fixture is equivalent code path (same branch) and not separately row-covered.
- Gate mutants (3) and SKILL cell are other seats' items; these rows' stdout_contains pin the exact verdict line + code so a mutant changing exit mapping (0/2/3) or the drift code is caught by an exit or substring change.
- Tools installed: none.
