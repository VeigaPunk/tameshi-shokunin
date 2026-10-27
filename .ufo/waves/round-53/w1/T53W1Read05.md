# T53W1Read05 — cold-read of `## Pin disposition and provenance correction — round 13`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (read-only; all reads via `git show` / `git cat-file` at the content commit, never the working tree)
- Content commit: `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Section bytes: SKILL.md lines 1524–1554 (heading line through the line before `### Round-13 gate/probe registry`), trailing whitespace-only lines stripped, no trailing newline
- `section_sha256 = ad8d6c4010f2c584a8fd34795625d66ab1a7ffcc91463a49e6d122ca06e4bf15`
- Findings: **none** (`"findings": []`)

## Section identification (two independent splits agree)

1. Independent monitor-recipe split (headings matching `^#{1,3}(\s|$)` outside ``` fences; blank-tail strip; join with `\n`; sha256 over UTF-8 with `surrogateescape`):

```
heading idx(0based) [1523] line 1524
next heading line 1555 '### Round-13 gate/probe registry'
nlines 30
sha ad8d6c4010f2c584a8fd34795625d66ab1a7ffcc91463a49e6d122ca06e4bf15
```

2. Frozen round-18 sectionize (`.ufo/evidence/round-18/measure.py`, extracted at C* and imported):

```
{'start': 1524, 'end': 1554, 'heading': '## Pin disposition and provenance correction — round 13',
 'sha256': 'ad8d6c4010f2c584a8fd34795625d66ab1a7ffcc91463a49e6d122ca06e4bf15'}
```

Both agree on the 1524–1554 range and the digest; the working tree was never read for the section text.

## Commands run (both documented recipe commands, at C* bytes)

Tool bytes at C* equal the working-tree bytes, so the documented invocations exercise exactly the C* files (`tools/pin-disposition.py` `ae4a6763…`, `tools/witness-metadata.py` `df339068…`, both confirmed with `git show C*:<path> | sha256sum`). Scratch `TMPDIR` and `PYTHONDONTWRITEBYTECODE=1` were set; cwd = lane root, as the section directs ("Recipe from this lane root:").

1. `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → **exit 0**

```
schema pin-disposition-v1 status ok
root /home/vgpnk/Projects/shokunin
counts {'legs': 6, 'unchanged': 1, 'changed': 5, 'unavailable': 0}
result_reuse not_established
not_compared 8
[('js-kimi-census','verified','changed'), ('bash-surface-census','verified','changed'),
 ('bash-tsukuroi-census','verified','changed'), ('bash-mado-verify','verified','changed'),
 ('bash-checklist-run','verified','unchanged'), ('js-claims-check','verified','changed')]
observed_at 2026-10-27T13:30:18Z   tool_sha256 ae4a6763cd5d90087931622d8737797f703c0df16fdf4d2002b68ee0c54bf787
```

2. `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json --json` → **exit 0**

```
{"companion": "…/.ufo/evidence/round-13/witness-metadata.json", "companion_in_lane": true, "exit": 0,
 "id": "metadata_consistent", "inputs_verified": ["summary","declaration","declared","rerun_summary"],
 "lane_root": "/home/vgpnk/Projects/shokunin/tameshi-shokunin",
 "normalized_kind": "declared-witness mapping (not a blind preregistration)", "reason": "ok"}
```

The verdict matches the literal `metadata_consistent` vocabulary the section's table implies and the tool's `EXPECTED_VERDICT_ID` (`tools/witness-metadata.py` line 108). No writes landed outside the seat scratch.

## Holds — verified against C* bytes

Each item below is a section statement followed by the check that makes it hold at C*.

| Section statement (verbatim) | Check |
|---|---|
| `Sources: S003 and PIT precision correction S047 (historical S041 retained);` | `git show C*:corpus/SOURCES.md` rows: `:14` S003 (StrykerJS incremental docs), `:50` S041 (PIT incremental analysis), `:56` S047 "Incremental analysis (PIT docs), precision correction". All three present; S041 retained alongside S047. |
| `` `corpus/knowledge/incremental-pin-disposition.md` `` | File exists at C* (`git ls-tree -r C*`), and its own `source:`/`source-correction:` header and §1 carry the S003/S041/S047 quotations the section's method rests on ("Pin match is not a reuse licence…"). |
| `outside routed ` + `` `corpus/lessons/round-12-verifier-spotcheck.md` `` + `, Routed defects item 3;` | `git show C*:corpus/lessons/round-12-verifier-spotcheck.md` — `## Routed defects and residuals`, item 3 at `:146` is "**Tameshi next round:** replace brittle host-addendum line citations with the named planner-ruling section in an append-only correction … Disclose/repair the already named nested `declaration.kind=null` metadata defect only through new evidence without rewriting the frozen declaration." That is exactly this section's subject (append-only correction + new-evidence companion). |
| `runtime receipts in ` + `` `.ufo/evidence/round-13/` `` + `.` | `git ls-tree -r C* -- .ufo/evidence/round-13/` lists 16 receipts, including `pin-manifest.json`, `pin-dispositions.json`, `witness-metadata.json`, `witness-metadata-old-null.json`, `producer-oracle-repair.json`, `verification-verdict.json`. |
| `\| Recorded target bytes equal the current worktree \| Report ` + `` `unchanged` `` + ` content \| …` | Live run emits `content_status`/`worktree.status` = `unchanged` for `bash-checklist-run`; vocabulary in `tools/pin-disposition.py` docstring `worktree … status unchanged\|changed\|unavailable`. |
| `\| Readable verified pin differs from current bytes \| Report ` + `` `changed` `` + ` content \| …` | Same run: five legs `content_status=changed`, all six `pinned.status=verified`. |
| `\| Repo, commit, path or pin cannot be evaluated \| Report ` + `` `unavailable` `` + `, with reason \| …` | `tools/pin-disposition.py` `repo_identity()` returns named refusal arms (`repo_missing`, `repo_symlink`, `repo_not_directory`, `repo_outside_root`) and the document reports `unavailable` with `reason`; counts key `unavailable: 0` present in the live run. |
| `\| All three content identities agree \| Keep ` + `` `result_reuse=not_established` `` + ` \| …` | Live run: top-level `result_reuse: not_established` and every leg row carries the literal (`js-kimi-census … not_established`); tool docstring: "`result_reuse` literal \"not_established\" on every row". |
| `\| Frozen summary kind is null but the frozen declaration's top-level kind is explicit \| …` | `git show C*:.ufo/evidence/round-12/BashWitness/summary.json` → top-level `kind` null, `declaration.kind` null (sha256 `acc01268…`); `declaration.json` → top-level `kind = 'declared-witness mapping (not a blind preregistration)'` (sha256 `e8d2024a…`); companion `declaration.kind_source = "declaration.json#/kind (explicit frozen top-level field)"`. |
| `\| … \| Retain original bytes and add checked normalized companion \| Preserve the exact non-blind kind and exposure disclosure; no retroactive preregistration \|` | Companion `witness-metadata.json`: `frozen_bytes_rewritten: false`, `measured_claim_unchanged: true`, `original_nested.state = historical-null-preserved`, `prior_exposure: true`, `blind: false`; the `--check` run above verifies the pinned digests of summary/declaration/declared/rerun. |
| `1. Read the manifest's recorded source and the output's ` + `` `not_compared` `` + ` list before the rows.` | `pin-manifest.json` carries `source: "tools/mutate-and-run.sh:84-89 (leg/path table), :542-553 (PIN_*/REV_* pairs), :1112-1140 (six ledger leg calls)"` plus `derived_from.sha256 = 75ed934d…`; the live output carries `not_compared` with 8 entries. The cited line ranges are exact **for that pinned blob**: `git cat-file blob 4a5bf43073b8…` (`sha256 75ed934d…`) gives lines 84–89 = the six-leg table, 542–553 = the `PIN_*`/`REV_*` pairs, 1112–1140 = the `regression_case_git` ledger calls. (The current runner at C* is `977de470…` with ten legs, so the numbers are historical-by-pin, not live — see "considered and rejected" below.) |
| `2. ` + `` `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` `` | Ran verbatim from the lane root: exit 0, `status: ok`, `manifest` resolved under this lane, `root` = the named fleet root. |
| `observes only hashes and git metadata. Retain stdout with its sibling branch-tip commits before treating it as a dated reading. It executes no sibling gate.` | `tools/pin-disposition.py` normal mode runs only `subprocess.run(["git", "-C", repo_abs] + args, …)` (`git_run`, lines 225–247) with a scrubbed `GIT_*` env and `GIT_OPTIONAL_LOCKS=0`; the only non-git spawn is `[sys.executable, SELF]` inside `--selftest` (line 931), which the recipe does not invoke. Output carries per-leg `head.commit`/`head.branch`/`head_differs_from_branch` branch-tip fields (`js-kimi-census head commit d23892ad44b4`), so stdout is retainable as a dated reading. |
| `3. ` + `` `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` `` + ` checks the new companion against digest-anchored frozen sources.` | Ran verbatim: exit 0, `metadata_consistent`, `inputs_verified: summary, declaration, declared, rerun_summary`; tool comment (line 112): "validated against the digest-pinned documents, never against the live tools on disk". |
| `4. The original round-12 summary and rerun summary retain their historical null fields.` | Both frozen summaries at C* still carry `declaration.kind = null` and digests `acc01268…` (canonical) / `6726421f…` (rerun), both equal to the companion's `frozen_declaration` and `scope.uncovered_null_observations` digests. |
| `The companion normalizes the canonical summary only; the rerun null is explicitly outside its normalized scope.` | Companion keys: `scope.covered_null_observations` = `summary.json#/declaration/kind`; `scope.uncovered_null_observations` = rerun `summary.json#/declaration/kind`, `disposition: named-residual-uncorrected`. |
| `The producer's wrong-nesting bug is fixed separately for future summary generation; its regression selftest asserts the exact top-level exposed kind.` | `tools/bash-witness-study.py` at C* `build_summary` reads `"kind": declaration.get("kind")` (top level) whereas the pre-fix source `.ufo/evidence/round-13/producer-before.py:787` reads `declaration.get("declared", {}).get("kind")`; the fixed file's selftest asserts `check("summary preserves top-level exposed declaration kind", qsummary["declaration"]["kind"] == "declared-witness mapping (not a blind preregistration)")`. `producer-oracle-repair.json` records nested-getter mutant exit1 `40/41 pass`, repaired getter exit0 `41/41 pass`, identical new literal check in both sources. |
| `5. Do not rerun a sibling's gate to obtain closure evidence. A non-author closure verifies committed receipts and their measured revision.` | Normative and consistent with the receipts: this read verified committed round-13 artifacts (`pin-dispositions.json`, `witness-metadata.json`, `producer-oracle-repair.json`) rather than executing a sibling lane's gate. No sibling gate was run by this seat. |

## Considered and rejected as findings (both hold at C*)

1. **`Sources: S003 and PIT precision correction S047 (historical S041 retained);` vs the later S048 correction.** At C* `corpus/SOURCES.md:57` carries `S048 | Incremental analysis (PIT docs), object-neutral precision`, and `corpus/knowledge/incremental-pin-disposition.md:5` records `source-correction: S048 … supersedes S047's test-versus-mutation paraphrase`, repeated by this page's own registry note (`PIT source clarification: S048 supersedes S047's object-specific paraphrase; retain only the supported distinction "item 4 is prioritisation, not a reuse skip"`). Rejected as a finding because S047 remains the recorded precision correction of S041 (`incremental-pin-disposition.md:67`, `:70`: "S047 records this precision correction … S041's earlier … cell is superseded by S047; the original row is retained"), and nothing in this section relies on the superseded test-versus-mutation paraphrase — the table's four checks are byte/verdict vocabulary only. The section is a dated round-13 record and the supersession is stated one heading later; calling it a false statement would be a wrong expectation.

2. **The manifest's recorded source line numbers are stale against the *live* runner.** They are stale only against the current file (`977de470…`, ten legs; `PIN_*` now at 614–633), and exact against the manifest's own `derived_from.sha256 = 75ed934d…` blob, which step 1 explicitly binds the reader to ("the manifest's **recorded** source"). Verified in the pinned blob: 84–89 six-leg table, 542–553 `PIN_*`/`REV_*`, 1112–1140 `regression_case_git` calls — all byte-exact. Rejected as a finding: the statement instructs reading a pinned historical source and that source resolves exactly.

No other statement failed: every path, command, flag, verdict code, digest, scope key and selftest claim listed above was checked against C* bytes or against an executed run of the exact documented command.

## Limits of this read

- Findings are empty by evidence, not by abstention: the two candidates I could construct are disproved above. Semantic fairness of "no findings" for a frozen record section is a wave-2/closure question, not one this seat can self-certify.
- The live fleet-root probe read current sibling worktrees (statuses `1 unchanged / 5 changed`), which necessarily differs from the round-13 receipt's `3/3/0`; the section's decision table, not those values, is what was checked.
- I did not run either tool's `--selftest` (the section claims no selftest command; those claims belong to `### Round-13 gate/probe registry`).
- Tooling: no installs or upgrades were needed (python3 + git only). Scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read05` held the extracted section, run outputs and the run-local `TMPDIR`, and was deleted before yield.
