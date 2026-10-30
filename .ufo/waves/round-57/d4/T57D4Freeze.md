# T57D4Freeze — documentary freeze review

Status: **UNVERIFIED candidate; no admission recommendation.** Axes: input coverage, mapping consistency, truthful run provenance. Read-only source/report inspection; no candidate gate, generator, controls, counter, test or build executed. No installations, delegation, commits or production edits.

## Findings (severity order)

### High — executed monitor instruments and external census are outside the frozen surface

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/contract.json:175-199` lists only round-57 evidence and tools files. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/no-harm.sh:16-28` executes round-21 coldread and round-45/46/47 freshness/coverage instruments, none listed. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/deciding-run.sh:157-158` executes the round-48 precheck; `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh:11-15` in turn executes the round-21 monitor. The actual integrity loop only hashes manifest entries (`deciding-run.sh:100-117`). Thus its freeze-to-REV integrity statement does not cover all executed monitoring logic. This is a static coverage defect, not evidence that anyone changed those instruments.

Additionally `deciding-run.sh:32,189-190` executes `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` from the live fleet selected by `DECIDING_FLEET`; recording `FLEET=...` is not recording script/config bytes or a committed census runtime. It cannot establish one fully frozen runtime for the census portion.

Documentary command/output: `functions.read` on the absolute `no-harm.sh:1-220` returned line 16 `CR=$(python3 .ufo/evidence/round-21/coldread/measure.py ...`, line 18 round-45 freshness, line 20 round-45 coverage, line 26 round-46 coverage, and line 28 round-47 coverage. `functions.read` on the absolute `deciding-run.sh:1-260` returned line 189 `{ echo "FLEET=$FLEET"; "$FLEET/scripts/sources-census.sh" validate --root "$FLEET" tameshi; } ...`. Contract read returned the complete 24-entry frozen list without these paths.

Required correction before a freeze claim: enumerate immutable instrument inputs separately from intentionally variable scored content, reconcile their path mapping, and identify census implementation/configuration bytes. No such repair was performed here.

### Medium — generator and deciding-run disagree on representable inputs

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/freeze-gen.py:49-50,96-110` accepts verbatim `tools/`, round-21 and round-48 paths, plus round-57-relative paths. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/deciding-run.sh:90-104` accepts only `tools/` and round-57 paths. Its inverse at lines 98-99 also treats every non-tools key as round-57-relative. A manifest generated with round-21/48 instruments added to the contract would therefore not be consumable by the canonical deciding-run. This is a source-derived incompatibility; the present list contains neither prefix, so it is not a claim that the present list already triggers this refusal.

Documentary command/output: `functions.read` on the absolute generator `:1-240` returned `VERBATIM_PREFIXES = ("tools/", ".ufo/evidence/round-21/", ".ufo/evidence/round-48/")` at line 50. The deciding-run read returned `if p.startswith('tools/'):` at line 93, `if p.startswith(E + '/'):` at line 95, and `return None` at line 97. Round-45/46/47 instruments and `.ufo/waves/round-57/...` provenance paths are unmappable by both implementations.

The C1 seat blobs have an indirect hash check through panel.files (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/measure.py:259-266`), so describing all seat content as wholly unpinned would overstate the gap once a real panel pin exists. However wave-results membership is read separately at lines 249-252 and is not freeze-listed; the currently shipped panel pin remains the pending marker at line 111.

Required correction: one shared mapping contract, covering the instruments/provenance that must be frozen. Do not treat generator acceptance as deciding-run acceptance.

### Medium — frozen-notes asserts automatic protection of unlisted control files that code does not provide

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/contract.json:200` says: `control/ is listed by its two file names, and a third file in control/ changes the frozen set and needs its own amendments entry`.

Neither implementation enumerates that directory. Generator lines 152-180 derive keys only from literal frozen_paths; deciding-run lines 100-117 do the same against the manifest. An added, unlisted third path is not itself a manifest-key change. Planned controls receipts are in fact added later (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/controls.sh:11-14`), and deciding-run checks their existence, ancestry, verdict and digest at lines 137-153 rather than freeze-list membership. The sentence is false as an assertion of implemented automatic coverage; an amendment requirement could only be a separate documentary policy.

Documentary command/output: `functions.read` on the absolute contract `:200:raw` returned the quoted sentence. Generator read returned `for path in frozen_paths:` at line 156; deciding-run read returned `for p in co.get('frozen_paths', []):` at line 101. Neither returned a directory enumeration in that integrity logic.

Required correction: distinguish the literal frozen input set from later control receipt outputs and documentary amendment policy.

## Existing freeze / controls assertions

No false assertion of a completed freeze or controls run was found in the inspected current status records. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/contract.json:201` explicitly says `UNVERIFIED candidate; no freeze and no admission claimed`. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/LOG.md:2588-2589` says no freeze was committed and no control ran; lines 2605-2611 retain the unpinned/candidate distinction. `/home/vgpnk/Projects/shokunin/.ufo/reports/round-57/tameshi.md:3,16-17,39-42,64-66` labels the historical stop, scratch dry runs, and untested end-to-end tooling rather than asserting successful controls.

Absence sweep (read-only commands and observed output):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only HEAD -- .ufo/evidence/round-57/freeze.json .ufo/evidence/round-57/control .ufo/evidence/round-57/after
```

Output:
```
.ufo/evidence/round-57/control/gen_ledger.py
.ufo/evidence/round-57/control/gen_registry.py
```

The tool directory read of `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/control` likewise returned only those two generators; the evidence root listing contained no freeze.json. A later read-only command `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD` returned `120a055d78b0f35f7f72c4c2a005ef7770f6d458`. These observations are not an atomic repository snapshot and not a run receipt.

## Residual risk and verification gaps

- LSP device unavailable: requesting `xd://lsp` returned `No such tool: xd://lsp`; caller/definition/diagnostic requests could not be made. Text/source reads are documentary evidence, not semantic-server proof.
- Scoped diff command `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b HEAD -- .ufo/evidence/round-57/deciding-run.sh .ufo/waves/round-57/freeze-gen.py .ufo/evidence/round-57/contract.json` reported three additions, 669 inserted lines; the changed sources were read directly with line anchors. Repository may change concurrently.
- No execution supports successful freeze regeneration, controls, final 64/64 no-harm, or admission. No same-identity rerouting or saturation result is established by this review. Resume continuity is outside these scripts' stated contract, not verified here.
- Recommendation only: retain UNVERIFIED; fix source/prose inconsistencies before any future permitted canonical run. No judgment, integration or admission was performed.

Self-evaluation: accuracy 4/5 (static inference, not runtime proof); completeness 4/5 (scoped source/records covered, no execution permitted); clarity 4/5 (absolute citations are lengthy); actionability 4/5 (mapping/coverage corrections identified, not implemented by reviewer); conciseness 4/5 (command evidence intentionally retained). Overall 4.0/5. Improvements: canonicalize input mapping and distinguish frozen inputs from later outputs; obtain permitted canonical receipts before making success claims. User-agreement check: review-only limits and unverified status are explicit.
