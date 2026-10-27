# T51W2Read04 — cold-read re-key reader: `### The boundaries — what a service run is not`

Seat: T51W2Read04 (wave 2, round 51, calibration). Candidate `6d8c11e378aa90b12650808e1b79270742935f15`, base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. Method: heading re-resolved at CAND (`git show 6d8c11e3:SKILL.md`, scratch copy), section read in full, every cited non-record surface read at CAND bytes via `git show`. No tools installed; no lane mutation; scratch `/fast/scratch/hyaku/tameshi-r51/T51W2Read04` (deleted before yield).

## Resolution

- Heading found at CAND **SKILL.md:858**; next heading `### The report shape — what the opting-in lane receives` at **:883** → section = **858-882** (25 lines).
- Section bytes at CAND are **identical to base**; section sha256 `fcfff5c18025e1dc585aca5e5725477099fcf178c29b57706ab2fbfd50a09e84`. It loses credit at CAND only through its pinned runner input (`input-drift:tools/mutate-and-run.sh`), not through any text change — exactly the case a trace-bound re-key exists for.
- The cited knowledge files are unchanged base↔CAND (`fleet-suite-census.md`, `mutation-case-mado-verify.md`: same byte counts both revs); the three SKILL.md pointers sit before the round-51 registry append and are byte-identical base↔CAND (verified lines 335, 377-378, 808-809).

## Pointer-by-pointer verification (all excerpts are CAND bytes)

| # | Raw pointer text | File · range | Verdict | Located excerpt (CAND) |
|---|---|---|---|---|
| 1 | `` `fleet-suite-census.md:288-291` `` ("census §5 scope") | corpus/knowledge/fleet-suite-census.md:288-291 | **holds** | ":288 **Scope of the offer, stated so it is not over-claimed:** single-edit mutants only (coordinated edits are unmeasured everywhere, matrix §7); hermetic suites only (no substrate-drift claim, matrix U5); results are per-revision and :290-291 per-host (no cross-host stability claim, matrix U5)." Sits in §5 (heading `## 5. Tameshi's standing service offer` :249; §6 starts :293), so "census §5 scope" is accurate. |
| 2 | `` `MUTATE_RESTORE` `` (inline symbol) | tools/mutate-and-run.sh:570,574 (emit); :77,:136,:1380,:1665 | **holds** | ":574 `MUTATE_RESTORE: OK (target-sha256 before=%s after=%s pristine-sha256=%s)`"; :570 the DRIFT arm. Symbol alive at CAND after the tenth-leg/TMPDIR edits. |
| 3 | `(SKILL.md:808-809)` — porcelain-clean opt-in precondition at open | SKILL.md:808-809 | **holds** | ":809 …and a porcelain-clean sibling tree at open." — item 1 of the opt-in contract (`### The opt-in contract` :806). Byte-identical to base. |
| 4 | `` "The target is never written" (`tools/mutate-and-run.sh:36-38`) `` | tools/mutate-and-run.sh:36-38 | **holds** (drift note) | CAND :37-38: "The target is / never written: every mutant is a fresh byte copy of the pinned pristine copy,". The comment block shifted **+1 line** vs base (the quoted phrase was at :36-37 at base); the quoted claim is still fully inside the cited range, but the sentence's tail ("and the target's sha256 before/after is the restore proof.") now ends at :39, one line past the range. Pointer holds for the quoted text; noted for calibration. |
| 5 | `(SKILL.md:377-378)` — fingerprints ≠ no-transient-write | SKILL.md:377-378 | **holds** | ":377 All substrate edits must stay in scratch. Before/after fingerprints establish endpoint identity, not that no transient :378 write occurred." Byte-identical to base. |
| 6 | `` `mutation-case-mado-verify.md:57-59` `` — sha pair | corpus/knowledge/mutation-case-mado-verify.md:57-59 | **holds** | ":58 `MUTATE_RESTORE: OK (target-sha256 before=d7edaab4…d0e13 after=d7edaab4…d0e13 :59 pristine-sha256=d7edaab4…d0e13)`; the fleet file was re-hashed after the probes too: unchanged." |
| 7 | `(SKILL.md:335)` — low rate is a report, not a failure | SKILL.md:335 | **holds** | ":335 **Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so does a <50 % — with the gap recorded in the table, not softened". Fair paraphrase; byte-identical to base. |
| 8 | `` `mutation-case-mado-verify.md:175-176` `` — Mado 40 % first below band | corpus/knowledge/mutation-case-mado-verify.md:175-176 | **holds** | ":175 …· 40 % (mado bash r6)**. :176 The fourth point is the first below the 50–80 band, and its cause is composition". |
| 9 | `` `mutation-case-mado-verify.md:66-72` `` — composition 4+6 | corpus/knowledge/mutation-case-mado-verify.md:66-72 | **holds** | ":66-68 4 defects … ("in-surface": D1, D2, D4, D6) and 6 at seams it predicted unasserted … Measured: **4/4 killed and 0/6 killed**; :71-72 The 40 % rate is composition, not a regression of the suite". Matches the section's "(4 in-surface + 6 out-of-surface, measured 4/4 and 0/6)". |
| 10 | `` `mutation-case-mado-verify.md:237-238, :240-260` `` — recommendations-only, unabsorbed | corpus/knowledge/mutation-case-mado-verify.md:237-238,240-260 | **holds** | ":237 **U6** — whether mado accepts any §8 recommendation is a decision of mado's lane; this note :238 records the findings unabsorbed." ; ":240 ## 8. Recommendation to the owner (mado) — recommendations only, no patch" with ranked items 1-7 ending :260. |
| 11 | re-pin `` `b56c6e57…` `` (inline) | corpus/knowledge/mutation-case-mado-verify.md:21 | **holds** | ":21 Re-pin at 17:46:15Z: sha256 `b56c6e57…2bcb`, 46850 B". The section's rounded form matches the file's own truncated rendering. |
| 12 | `` `mutation-case-mado-verify.md:17-23` `` — harness moved mid-round, drift recorded | corpus/knowledge/mutation-case-mado-verify.md:17-23 | **holds** | ":17 **Incident I1 — the harness itself moved mid-round, by a concurrent lane.** … :22 **Every number in this note is tied to `597e1419…`** … :23 Recorded, not smoothed; nothing was repaired." |
| 13 | `` `mutation-case-mado-verify.md:229-230` `` — sensitivity, not truth | corpus/knowledge/mutation-case-mado-verify.md:229-230 | **holds** | ":228-230 **U2** — suite sensitivity ≠ gate truth: nothing here measures whether the gate's verdicts against the *real* config planes are right; only what its suite can detect." |
| 14 | "(matrix row F)" — uncited inline premise | corpus/knowledge/fleet-suite-census.md:187,341 (matrix vocabulary) | **holds** (premise corroborated in the file the bullet already cites) | ":187 `F — coordinated edits`" column of census §3.2; ":341 U1 — coordinated multi-edit rewrites (matrix class F) are unmeasured for all six gates and remain the method's stated boundary (`arm-class-matrix.md:206-215`)." |
| 15 | "(corrected in round 27 after the cold read of seat Read09)" — provenance aside | .ufo/evidence/round-27/coldread/ at CAND | **holds** (corroborated, not load-bearing) | Read09 exists as a round-27 cold-read seat at CAND (`.ufo/evidence/round-27/coldread/assembled-w1.json:385-390` traces `Read09-1..6.json`; `assembled-residual.json:522`). The current :57-59 content is verified directly regardless. |

**Verdict: every pointer in the section holds at CAND; no absent pointer, no stale range, no unsupported load-bearing premise.**

## Strongest falsifiers checked (all failed to falsify)

1. **"The target is never written" vs the r51 runner change (tenth leg + TMPDIR).** Grepped every use of `TARGET` at CAND: the target is only resolved (`readlink -f` :487), pinned, read, and copied *from* (`cp -p "$TARGET_ABS" "$PRISTINE"` :501); no redirection or copy *into* the target exists. The r51 change moves WORKDIR/evidence to `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-run.XXXXXX"` (:149-160, :217, :491) and the regression root likewise (:1432); the tenth leg's suite runs in an `env -i` sandbox under `$WORKDIR` with its own HOME/TMPDIR (:1491). All writes stay in scratch; the claim remains true at CAND.
2. **"The tool emits no tree-clean check" vs CAND runner.** The only `status --porcelain` occurrences (:1974, :1986) are inside the selftest's GIT_*-scrub *canary fixture* (asserting the fixture canary clone's index/worktree stay unchanged) — not a tree-clean check emitted about the opting-in lane's tree during a run. Statement remains true at CAND.
3. **Tenth leg vs "Single-edit mutants only — coordinated rewrites are unmeasured".** The registered C2 spec (`.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec` at CAND) states "Each @old occurs exactly once in the pinned bytes" — single-edit mutants; its suite is "hermetic `env -i … bash "$MUTANT" --selftest`" — consistent with the hermetic-only boundary. No recorded leg contradicts the boundary bullets.
4. **Four panel-tool updates** (tools/tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, mte-interop.py — amendment 2). None is cited by this section (its only runner pointer is :36-38; the census/mado files did not change base↔CAND). No falsification surface.
5. **Line-drift of the runner citation** (falsifier candidate found, downgrade not falsification): the runner header comment gained one line above :36 by CAND, so the cited range no longer covers the sentence's final clause (see pointer 4). The quoted claim itself stays inside the range, so the pointer holds; a strict reader should prefer :37-39 for the whole sentence at CAND.

## Row for reads.json

```json
{
  "seat": "T51W2Read04",
  "heading": "### The boundaries — what a service run is not",
  "cand": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "section_lines_cand": "858-882",
  "section_sha256": "fcfff5c18025e1dc585aca5e5725477099fcf178c29b57706ab2fbfd50a09e84",
  "section_identical_to_base": true,
  "read_method": "git show at CAND for SKILL.md and every cited non-record file; runner/census/mado byte-compared against base",
  "verdict": "holds",
  "pointers": [
    {"raw": "census §5 scope, `fleet-suite-census.md:288-291`", "file": "corpus/knowledge/fleet-suite-census.md", "ranges": "288-291", "verdict": "holds", "excerpt": "Scope of the offer, stated so it is not over-claimed: single-edit mutants only … hermetic suites only (no substrate-drift claim, matrix U5); results are per-revision and per-host", "note": "sits in §5 (heading :249, §6 at :293)"},
    {"raw": "`MUTATE_RESTORE`", "file": "tools/mutate-and-run.sh", "ranges": "570,574,1380,1665", "verdict": "holds", "excerpt": "MUTATE_RESTORE: OK (target-sha256 before=%s after=%s pristine-sha256=%s)"},
    {"raw": "(SKILL.md:808-809)", "file": "SKILL.md", "ranges": "808-809", "verdict": "holds", "excerpt": "…and a porcelain-clean sibling tree at open.", "note": "byte-identical to base"},
    {"raw": "\"The target is never written\" (`tools/mutate-and-run.sh:36-38`)", "file": "tools/mutate-and-run.sh", "ranges": "36-38", "verdict": "holds", "excerpt": ":37 The target is / :38 never written: every mutant is a fresh byte copy of the pinned pristine copy,", "note": "comment shifted +1 line vs base; sentence tail now at :39, just outside the cited range; quote itself inside"},
    {"raw": "(SKILL.md:377-378)", "file": "SKILL.md", "ranges": "377-378", "verdict": "holds", "excerpt": "Before/after fingerprints establish endpoint identity, not that no transient write occurred", "note": "byte-identical to base"},
    {"raw": "`mutation-case-mado-verify.md:57-59`", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "57-59", "verdict": "holds", "excerpt": "MUTATE_RESTORE: OK (target-sha256 before=d7edaab4…d0e13 after=d7edaab4…d0e13 pristine-sha256=d7edaab4…d0e13)"},
    {"raw": "(SKILL.md:335)", "file": "SKILL.md", "ranges": "335", "verdict": "holds", "excerpt": "Bands are a report convention, not a pass/fail gate.", "note": "byte-identical to base"},
    {"raw": "`mutation-case-mado-verify.md:175-176`", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "175-176", "verdict": "holds", "excerpt": "The fourth point is the first below the 50–80 band"},
    {"raw": "`mutation-case-mado-verify.md:66-72`", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "66-72", "verdict": "holds", "excerpt": "4 in-surface (D1, D2, D4, D6) + 6 out-of-surface … Measured: 4/4 killed and 0/6 killed … composition, not a regression"},
    {"raw": "`mutation-case-mado-verify.md:237-238, :240-260`", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "237-238,240-260", "verdict": "holds", "excerpt": "U6 — whether mado accepts any §8 recommendation is a decision of mado's lane; this note records the findings unabsorbed / ## 8. Recommendation … recommendations only, no patch"},
    {"raw": "(re-pin `b56c6e57…`)", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "21", "verdict": "holds", "excerpt": "Re-pin at 17:46:15Z: sha256 `b56c6e57…2bcb`, 46850 B"},
    {"raw": "`mutation-case-mado-verify.md:17-23`", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "17-23", "verdict": "holds", "excerpt": "Incident I1 — the harness itself moved mid-round, by a concurrent lane … Recorded, not smoothed; nothing was repaired."},
    {"raw": "`mutation-case-mado-verify.md:229-230`", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": "229-230", "verdict": "holds", "excerpt": "U2 — suite sensitivity ≠ gate truth"},
    {"raw": "(matrix row F)", "file": "corpus/knowledge/fleet-suite-census.md", "ranges": "187,341", "verdict": "holds", "excerpt": "| F — coordinated edits | / U1 — coordinated multi-edit rewrites (matrix class F) are unmeasured for all six gates", "note": "uncited inline premise, corroborated in the census file the bullet already cites"},
    {"raw": "(corrected in round 27 after the cold read of seat Read09)", "file": ".ufo/evidence/round-27/coldread/", "ranges": "assembled-w1.json:385-390", "verdict": "holds", "excerpt": "Read09-1..6.json traces registered for round-27 w1", "note": "provenance aside, corroborated; current :57-59 verified directly"}
  ],
  "falsifiers_checked": [
    "no-write claim vs r51 runner TMPDIR/tenth-leg change: TARGET only read+pinned+copied-from (:487,:501); WORKDIR under mktemp TMPDIR (:491,:1432); tenth-leg sandbox under $WORKDIR (:1491) — claim stays true",
    "no-tree-clean-check claim vs CAND runner: only porcelain uses are the selftest canary fixture (:1974,:1986), not a lane-tree check — claim stays true",
    "single-edit-only claim vs tenth leg: C2 spec 'Each @old occurs exactly once in the pinned bytes', hermetic env -i suite — consistent",
    "four panel-tool updates: not cited by this section; census/mado unchanged base↔CAND — no surface",
    "runner citation line drift: quote shifted from :36-37 to :37-38 at CAND; range 36-38 still brackets the quote, sentence tail moved to :39 — holds, downgraded note"
  ]
}
```

## Residual risk / gaps

- The provenance aside "corrected in round 27 after the cold read of seat Read09" was corroborated (Read09 is a round-27 cold-read seat at CAND) but I did not diff the round-27 correction itself; the pointer's current content is verified directly, so this does not affect the verdict.
- I did not execute the runner; the no-write/no-tree-clean findings are byte-level code reads at CAND (:487,:501,:491,:1432,:1491,:1974,:1986), not a runtime trace.
- Scratch files under `/fast/scratch/hyaku/tameshi-r51/T51W2Read04` (SKILL blobs, runner/census/mado dumps, section extracts) are deleted before yield; no other writes were made.
