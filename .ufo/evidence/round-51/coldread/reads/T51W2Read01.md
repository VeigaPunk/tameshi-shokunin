# T51W2Read01 — cold-read re-key

Seat: `T51W2Read01` (calibration). Candidate: `6d8c11e378aa90b12650808e1b79270742935f15`. Read the complete CAND blob section `SKILL.md:131-245`; next heading is at 246. Section SHA-256 (those numbered lines, excluding the next heading): `2a6ec82d7dcf8b54f4057913f32d4b31f1293327b87890c959e49d17801138d4`. It is unchanged from base in the section region; the working tree was dirty/ahead, so all findings below use `git show <rev>:<path>` candidate bytes. No LSP device/server was available for revision-pinned Markdown reads; candidate text was checked directly.

## Finding

Two runner citations in the section are stale at CAND, while their underlying claims remain true:

- Section line 174, raw pointer `tools/mutate-and-run.sh:425`: CAND line 425 is `d = hits[0]`; the `APPLY FAIL … old-string-count=%d expected=1` print is at 433-435 (printf at 434). At base, line 425 was that print. The CAND runner's pre-425 header/usage/TMPDIR hunks shift the anchor by nine lines.
- Section line 211, raw pointer `tools/mutate-and-run.sh:569-574`: CAND lines 569-574 are the restore-drift check and `MUTATE_RESTORE: OK`, not the cited division/DEGRADED behavior. CAND `pct` calculation is at 579 and `MUTATE: DEGRADED` at 581-583 (use `578-583` for the block). At base, 569-574 covered the cited behavior; the anchor moved by nine lines.

The behavior still holds: CAND runner totals the defect rows at 516, records each verdict class at 555-559, computes its rate against `total` at 579, and emits DEGRADED at 581. The driver also still emits the failing old-string count at 434. The runner is 2159 lines at CAND vs 2080 at base. The TMPDIR-related header/usage changes contribute to the early offset; later runner changes include the tenth-leg material. The section contains no tenth-leg count claim and no reference to the four panel tools updated for the ten-leg panel, so those updates do not independently falsify this section.

The section's `/tmp/<lane>-r<round>-<n>-work/` scratch statement holds against the cited Standing rules (`SKILL.md:25-27`) and the historical notes. CAND runner defaults scratch to `${TMPDIR:-/tmp}` and documents r51 TMPDIR honoring; this does not contradict the documented default namespace. The section's `all unique` evidence is attributed to the historical Kimi/Kagi drivers; the maintained runner instead enforces the uniqueness count and reports the failure count (no `all unique` literal in its CAND bytes).

## Structured row for `reads.json`

```json
{
  "seat": "T51W2Read01",
  "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "section_lines": "SKILL.md:131-245",
  "section_sha256": "2a6ec82d7dcf8b54f4057913f32d4b31f1293327b87890c959e49d17801138d4",
  "pointers": [
    {"raw":"mutation-case-kimi-census.md:4-7","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"4-7","verdict":"holds","excerpt":"5-7: scratch copies; no live ~/.kimi-code read; runs use --selftest or --root at an empty scratch dir."},
    {"raw":"mutation-case-kagi-census.md:24-38","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"24-38","verdict":"holds","excerpt":"24-35: mktemp fixtures, substrate-gated verb cases skip on absent handler, 14 executed plus 2 skips; 36-38 records handler-present caveat."},
    {"raw":"gates-survey-kumitate.md:19-31","file":"corpus/knowledge/gates-survey-kumitate.md","ranges":"19-31","verdict":"holds","excerpt":"21-26: case-count summary lines and VERDICT: PASS; cite-check/surface-probe use 'cases passed', other rows include n/m pass; 28-31 describes mkdtemp fixtures."},
    {"raw":"mutation-case-kimi-census.md:20-21","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"20-21","verdict":"holds","excerpt":"20-21: KIMI_CENSUS_SELFTEST: 43/43 pass / VERDICT: PASS, exit 0, node v24.21.0."},
    {"raw":"mutation-case-kagi-census.md:27-35,42-43","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"27-35,42-43","verdict":"holds","excerpt":"33-35: skip cases count in SELFTEST: PASS (16 cases), 14 hermetic executions plus 2 substrate-gated; 42-43: green control, exit 0."},
    {"raw":"mutation-case-kimi-census.md:13-16","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"13-16","verdict":"holds","excerpt":"Artifact sha256, 896 lines, 43273 B, mtime, pinned repo revision, and clean path status."},
    {"raw":"mutation-case-kagi-census.md:13-17","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"13-17","verdict":"holds","excerpt":"Artifact sha256/size/886 newlines; explicitly says the 887th line has no trailing newline; mtime, revision, clean path status."},
    {"raw":"corpus/README.md G-R2-1 row","file":"corpus/README.md","ranges":"row G-R2-1 (line 11)","verdict":"holds","excerpt":"README line 11 says the surveyed 79294/357fb245 was an intermediate dirty-tree state never committed and records the corrected pin."},
    {"raw":"gates-survey-kagi.md errata block","file":"corpus/knowledge/gates-survey-kagi.md","ranges":"§10 :503; Errata (round 2) :545; G-R2-1 :554-556","verdict":"holds","excerpt":"G-R2-1 says the claim-ledger pin was corrected from 79294/357fb245 to committed 79301/93c5827202b9cdec."},
    {"raw":"mutation-case-kagi-census.md:44-45","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"44-45","verdict":"holds","excerpt":"44-45: each defect is a one-exact-string replacement on a fresh cp -p copy, cmp-verified."},
    {"raw":"mutation-case-kimi-census.md:41-53, :155-166","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"41-53; 155-166","verdict":"holds","excerpt":"41-53 is the ten-defect table; 155-166 is the ten-edit D1-D10 reproduction manifest."},
    {"raw":"mutation-case-kimi-census.md:183-191","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"183-191","verdict":"holds","excerpt":"§5 E1 retains the incorrect D7 pre-run expectation and explains the measured miss."},
    {"raw":"mutation-case-kagi-census.md:184-191","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"184-191","verdict":"holds","excerpt":"§5 E1 records verdict predictions 10/10 and failing-case counts 6/10, including B2/B3/B6 misses."},
    {"raw":"tools/mutate-and-run.sh:425","file":"tools/mutate-and-run.sh","ranges":"425","verdict":"absent/stale anchor; claim holds elsewhere","excerpt":"CAND :425 is `d = hits[0]`; `APPLY FAIL … old-string-count=%d` is :433-435 (printf :434)."},
    {"raw":"mutation-case-kimi-census.md:22-25","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"22-25","verdict":"holds","excerpt":"22-25: old string occurs exactly once, --check reports all unique, first-line match on all ten."},
    {"raw":"mutation-case-kagi-census.md:44-47","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"44-47","verdict":"holds","excerpt":"44-47: fresh pristine copy; driver asserts one occurrence and --check reports all unique."},
    {"raw":"mutation-case-kimi-census.md:26-28","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"26-28","verdict":"holds","excerpt":"Per-defect stdout, exit code, mutant sha256, and aggregate results are retained."},
    {"raw":"mutation-case-kagi-census.md:48-49","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"48-49","verdict":"holds","excerpt":"Per-defect combined output, exit, mutant sha256, wall time, case summary, and aggregate are retained."},
    {"raw":"mutation-case-kimi-census.md:30-33; mutation-case-kagi-census.md:27-35,50-53","file":"corpus/knowledge/mutation-case-kimi-census.md; corpus/knowledge/mutation-case-kagi-census.md","ranges":"kimi 30-33; kagi 27-35,50-53","verdict":"holds","excerpt":"Kimi says all 11 runs have definitive verdicts and the full 43-case denominator; Kagi says 14+2 skips and every run retains /16 accounting."},
    {"raw":"mutation-case-kimi-census.md:59-76","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"59-76","verdict":"holds","excerpt":"§1 failing-case labels for D4-D9 and D1/D3; the quoted labels are present."},
    {"raw":"mutation-case-kagi-census.md:67,82-103","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"67; 82-103","verdict":"holds","excerpt":":67 B1 is 1/16 FAIL; :84 carries the exact undeclared-file bad-case grammar and :82-103 provides labels."},
    {"raw":"mutation-case-kagi-census.md:88-91","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"88-91","verdict":"holds","excerpt":"B4 exit still matched; token assertion, not exit, killed the mutant."},
    {"raw":"mutation-case-kimi-census.md:44-53","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"44-53","verdict":"holds","excerpt":"D2 (:45) and D10 (:53) rows are green 43/43 survivors."},
    {"raw":"tools/mutate-and-run.sh:569-574","file":"tools/mutate-and-run.sh","ranges":"569-574","verdict":"absent/stale anchor; claim holds elsewhere","excerpt":"CAND :569-574 is restore drift/OK handling; pct is :579 and MUTATE: DEGRADED is :581-583 (block :578-583)."},
    {"raw":"mutation-case-kimi-census.md:29-31","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"29-31","verdict":"holds","excerpt":"8/10, no inconclusives, 11 runs in 7.0s against 300s timeout."},
    {"raw":"mutation-case-kagi-census.md:50-53","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"50-53","verdict":"holds","excerpt":"8/10, no inconclusives, 11 runs in 11.0s against 280s per-run bound."},
    {"raw":"mutation-case-kimi-census.md:82-99","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"82-99","verdict":"holds","excerpt":"D2 empty-root probe differs by one id/+23 vs +22 more; D10 reports frozen=24 vs 25."},
    {"raw":"mutation-case-kagi-census.md:111-114, :118-122, :252-254","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"111-114,118-122,252-254","verdict":"holds","excerpt":"B5 probe is SURFACE OK (exec 644) vs DIVERGED; B10 is ok=0 vs ok=1; §7 repeats expected outputs."},
    {"raw":"mutation-case-kimi-census.md:34-35","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"34-35","verdict":"holds","excerpt":"Kimi restore proof: before/after sha equal, size and mtime unchanged, clean path status."},
    {"raw":"mutation-case-kagi-census.md:54-56","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"54-56","verdict":"holds","excerpt":"Kagi restore proof: before/after sha equal, size/mtime unchanged, clean path status, pristine copy cmp-identical."},
    {"raw":"SKILL.md:377-378","file":"SKILL.md","ranges":"377-378","verdict":"holds","excerpt":"All edits stay in scratch; before/after fingerprints prove endpoint identity, not absence of transient writes."},
    {"raw":"mutation-case-kimi-census.md §1, §3-§6","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"§1, §3-§6","verdict":"holds","excerpt":"Headings §1 Kill-rate table; §3 What the suite protects; §4 Reproduce; §5 Calibration and errata; §6 Unknowns exist."},
    {"raw":"mutation-case-kagi-census.md §1-§7","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"§1-§7","verdict":"holds","excerpt":"Sections §1 through §7 (Reproduce) exist in candidate bytes."},
    {"raw":"mutation-case-kimi-census.md U5 at 204-205","file":"corpus/knowledge/mutation-case-kimi-census.md","ranges":"204-205","verdict":"holds","excerpt":"U5: kill-rate stability across node versions/hosts only measured on node v24.21.0, this host, 2026-10-14."},
    {"raw":"mutation-case-kagi-census.md U5 at 203-204","file":"corpus/knowledge/mutation-case-kagi-census.md","ranges":"203-204","verdict":"holds","excerpt":"U5: kill-rate stability across hosts/toolchains measured only on this host, 2026-10-14."},
    {"raw":"Standing rules","file":"SKILL.md","ranges":"25-27","verdict":"holds","excerpt":"Scratch namespace is /tmp/<lane>-r<round>-<n>-*/ from first write; substrate is never a mutation target."},
    {"raw":"Errata — round 16","file":"SKILL.md","ranges":"1707; 1726","verdict":"holds","excerpt":"Errata heading at 1707; row 1726 records round-16 recipe execution by CR04a and CR04b (two seats)."}
  ],
  "strongest_possible_falsifier_checked": "Compared the two runner citations against both base and CAND runner blobs, because the tenth-leg/TMPDIR changes could shift pointers. Both citations were correct at base but stale at CAND: :425 now misses the count print, and :569-574 now points to restore handling rather than pct/DEGRADED. Also checked whether the round-16 two-seat premise was confused with the 30-seat page-wide read; the errata row identifies CR04a/CR04b. Checked that the four panel-tool updates are not claimed by this section.",
  "residual_unverified_prose": "Section says 'corrected in round 27, seat Read03'; the claimed report path does not exist in the CAND tree, so that historical attribution was not independently verified. It is not needed to support the adjacent SKILL.md:377-378 endpoint-identity statement.",
  "findings": [
    {"severity":"low","finding":"Two stale line anchors in tools/mutate-and-run.sh; cited behavior remains present at CAND :434 and :578-583 respectively."}
  ]
}
```

## Residual risk / verification gaps

- `SKILL.md:228` also says “corrected in round 27, seat Read03”; `.ufo/waves/round-27/w2/Read03.md` is absent from the CAND tree, so that attribution could not be independently checked. The cited endpoint-identity correction itself is present at `SKILL.md:377-378`.
- All cited non-record surfaces and the README record row were inspected at CAND. No tools/tests were run. The section's historical scratch paths describe its cited historical runs, not this wave's host-guard scratch root.
